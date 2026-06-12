---
name: 02b_figure_enricher
title: 02b_figure_enricher — Ábra-meta gazdagító (image_rag bootstrap)
type: skill
tags: [meta, skill]
role: 🤖
status: active
version: 2.0
updated: 2026-06-12
description: A `02_mineru_to_catalog.py` után Claude CSAK a `visual_content`-et tölti (`Read(image)` + 1-3 mondatos leírás) és finomítja a keywords draft-ot. A caption + text_context gépileg előtöltve (MinerU). Használd a 02 után, a 03 előtt.
---

# 02b_figure_enricher

## 1. Cél

A `02_mineru_to_catalog.py` a `figure_catalog.json` mezőinek döntő többségét **gépileg előtölti**
(caption, text_context, keywords draft). Claude 02b-ben **csak** a következőket csinálja:

1. **`visual_content`**: minden bejegyzésnél `Read(image)` → 1-3 mondatos leírás (amit csak vizuálisan látni).
2. **`keywords` finomítás**: ha a script-draft < 3 tag, vagy ha a vizuális tartalom lényeges új tag-eket hoz (pl. „surge line", „pressure ratio").

**Ez minimális, izolált Claude-munka** (12. döntés): a caption-keresést és a text-extraction-t a
MinerU már elvégezte; Claude csak a képet nézi meg és írja le.

**Input:** `2_clean_inputs/figure_catalog.json` (v4 séma) · **Output:** ugyanaz, `visual_content` kitöltve, `_status: "draft"`. A 😎 véglegesítés (`caption_verified:true`) külön gesztus.

## 2. Bemenetek

| Fájl | Honnan (skill) | Tartalom |
|:-----|:---------------|:---------|
| `2_clean_inputs/figure_catalog.json` | `02_image_extraction` | v4 séma; strukturális + `caption`/`text_context`/`keywords`-draft gépileg kitöltve, `visual_content` még `null` |
| `2_clean_inputs/<stem>/images/pNNN_figNNN.png` | `02_image_extraction` | A kép-fájlok — Claude `Read`-eli |
| `2_clean_inputs/<stem>/mineru/{<stem>.md, <stem>_content_list.json}` | `02_image_extraction` (MinerU) | Layout-aware markdown + caption-párosítás (ha extra kontextus kell egy ábrához) |

**Előfeltétel:** `02_image_extraction` lefutott, a katalógus v4 sémában van, `needs_crop:true` bejegyzésekhez a manuális vágás opcionálisan kész.

## 3. Eljárás 🤖

Forrásonként dolgozunk: a `catalog["sources"]` kulcsain iterálva, ábránként töltjük a `visual_content`-et.

### 3.1. Source-loop

Minden `source_file`-ra (a `catalog["sources"]` kulcsain):

1. **A forráshoz tartozó figures listázása**: `catalog["sources"][src]["figures"]`.
2. **Minden figure-re** (`fig_id` sorrendben):
   - `Read` az image fájl a `path` mezőből → vizuális tartalom megértése.
   - Töltsd ki a `visual_content`-et (1-3 mondat, lásd §3.2).
   - Ellenőrizd a `keywords` draftot; ha < 3 tag vagy a kép új lényeges tag-et kínál, egészítsd ki.
   - A `caption` és `text_context` **gépileg kész** — csak akkor nyúlj hozzá, ha bizonyíthatóan hibás
     (pl. a caption paragrafus-szennyezett). Extra kontextushoz a MinerU `<stem>.md` / `_content_list.json`
     olvasható.
3. **Mentés**: forrás végén egy `save_catalog()` hívás. A `_status` automatikusan újraszámolódik (`un-processed → draft`).

### 3.2. Mezők kitöltési szabályai

| Mező | Tartalom | Forrás | Validáció |
|------|----------|--------|-----------|
| `caption` | A MinerU által előtöltött felirat. Csak akkor írd át, ha bizonyíthatóan jobb (paragrafus-szennyezés). | MinerU (előtöltve) | Pont nélkül NE végződjön egy paragrafus-folytatással. |
| `caption_verified` | Soha NE állítsd `true`-ra — ez kizárólag a 😎 gesture. | — | 02b mindig hagyja `false`-on. |
| `visual_content` | 1-3 mondat magyarul: mit ábrázol vizuálisan. Diagram-típus, tengelyek/címkék, fő elemek, esetleg trend. **Nem** értelmezés, hanem leírás. | `Read(image)` | Ne tartalmazzon "az ábra…" sablont; legyen specifikus. |
| `text_context` | A MinerU által előtöltött szövegkörnyezet (±3 szomszédos entry). Csak akkor finomítsd, ha üres vagy félrevezető. | MinerU (előtöltve) | Forráshoz hű, ne extrapoláljon. |
| `keywords` | 3-8 kulcsszó. Logók/dekorációk: `["logo"]` vagy `["decoration"]`. | visual_content + text_context | Konkrét, kereshető tag-ek. |
| `notes` | NE szerkeszd — ez a 😎 free space-e. | — | 02b sosem ír bele. |

### 3.2.0. Az `_status` mező (derivált, ne szerkeszd)

A 02 script automatikusan újraszámolja minden `save_catalog()` előtt. **4-állapotú** (Block 9):

| `_status` | Feltétel | Mit jelent |
|-----------|----------|------------|
| `complete` | `caption_verified:true` ÉS `visual_content` kitöltve | Teljesen kész, 05 retrieval használhatja |
| `caption-ok` | `caption_verified:true`, de `visual_content:null` | Caption jóváhagyva, 02b bootstrap hiányzik |
| `draft` | `visual_content` kitöltve, de `caption_verified:false` | 02b futott, 😎 jóváhagyás hiányzik |
| `un-processed` | Sem `caption_verified`, sem `visual_content` | 02b még nem futott |

**`_` prefix konvenció**: a `_status` mezőt — és minden `_`-szel kezdődő mezőt — csak a script kezeli. A `_meta` blokk is script-managed (csak `schema_version`, `last_updated`, `_guide` van benne). Az útmutató a JSON melletti `CATALOG_GUIDE.md` fájlban él.

A 02b skill célja: `un-processed` → `draft` (visual_content kitöltése). A végleges `complete` átmenetet a 😎 csinálja a `caption_verified:true` flippeléssel.

### 3.2.1. `un-processed` / `no-results` / `true-false` konvenció

A katalógus mezői három állapotúak (a boolean kettő):

| Slug | JSON | Jelentés | Példa |
|------|------|----------|-------|
| `un-processed` | `null` | feldolgozás nem futott le | `visual_content: null` |
| `no-results` | `[]` | feldolgozva, de üres eredmény | `keywords: []` egy log entry-n |
| `true-false` | `bool` | tudottan pozitív/negatív | `caption_verified: false` |

### 3.3. Logo / dekoráció kezelés

Ha egy bejegyzés képtartalma kizárólag brand-logó vagy díszítő grafika:
- `visual_content`: `"Brand-logó: <név>"` vagy `"Díszítő grafika"`
- `keywords`: tartalmazzon `"logo"` vagy `"decoration"` tag-et
- `caption_verified`: `false` marad

Séma-bővítés (pl. `keep:false`) NEM szükséges — a 05 retrieval a `"logo" in keywords` szűrővel kihagyja.

### 3.4. Idempotencia

A skill csak akkor írja felül a mezőt, ha **null vagy üres** volt. `caption_verified:true` bejegyzéseket meg sem érinti.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `2_clean_inputs/figure_catalog.json` | v4, kitöltött `visual_content`-tel, `_status` átáll `un-processed → draft`-ra. `_meta.last_updated` frissül. |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het/2_clean_inputs/figure_catalog.json` friss regen (a MinerU-mezők kitöltve, minden entry `visual_content:null` → `_status:"un-processed"`).
- **Akció:** a session ábránként `Read(image)` → `visual_content` kitöltése + keywords finomítás; forrás végén `save_catalog()`.
- **Várt:** minden feldolgozott bejegyzésnél `visual_content` nem-null (≥10 karakter); `caption_verified` változatlanul `false`; `_status:"draft"`. `_meta.last_updated` ma.
- **Eval:** spot-check 2-3 bejegyzésnél: `visual_content` egyezik a kép tartalmával; `keywords` konkrét, kereshető.

## 6. Ellenőrzés

- [ ] Feldolgozott bejegyzéseknek van `visual_content` (nem null, ≥10 karakter)
- [ ] `text_context` nem null (MinerU-előtöltés vagy 02b-finomítás)
- [ ] `keywords` ≥1 elem (logók: `["logo"]` is OK)
- [ ] Logók `keywords: ["logo"]`-val jelölve (NEM kapnak részletes meta-t)
- [ ] `caption_verified` 02b által NEM lett `true` (csak 😎-tól)
- [ ] `_status` minden bejegyzésnél a 4 érték egyike
- [ ] Idempotens újrafuttatás: a `caption_verified:true` bejegyzéseken 0 változás

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `Read(image)` hibás karaktert ad | PNG sérült vagy nem PNG | Nézd meg a fájlméretet; ha 0 byte, `02` újra futtatása |
| Üres / félrevezető `text_context` | MinerU nem talált szomszédos szöveget (pl. képoldal) | Finomítsd a MinerU `<stem>.md`-ből; ha tényleg nincs, hagyd a MinerU-értéket |
| `caption` és kép nem egyezik | MinerU caption-párosítás félrement | Caption korrekció: írd át manuálisan; a 😎 állít `caption_verified:true`-t |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- upstream: [02_image_extraction.md](02_image_extraction.md) (`02_mineru_to_catalog.py`) · downstream: [03_mindmap_builder.md](03_mindmap_builder.md), [05_figure_integrator.md](05_figure_integrator.md)
- Sprint kontextus: [.claude/sprints/image_rag/image_rag_plan.md](../sprints/image_rag/image_rag_plan.md)

## 9. Visszajelzések 😎+🤖

- 💬 NOTE: Az image_rag retrieval (05) hatékonysága a `keywords` minőségén áll vagy bukik. Cél: 3-5 közepes specifikusságú tag/ábra.
- 💡 IDEA: Egy jövőbeli verzió embedding-alapú retrieval-hez `keyword_embedding: [...]` mezőt gyűjthet — most lexikális (TF-IDF/BM25) elég.

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-04 | 1.0 | Létrehozva (image_rag sprint, Block 8). v4 katalógus séma. atg/1_het pilot: chattopadhyay + tavakoli (8 ábra). |
| 2026-06-05 | 1.1 | image_rag_OCR sprint. §3.1 backend-preferencia chain (MinerU > PyMuPDF4LLM > Tesseract > Claude Read). |
| 2026-06-05 | 1.2 | MinerU-first pipeline. §1 kettéválasztva (standard vs fallback). Claude feladata redukálva. |
| 2026-06-12 | 2.0 | **MinerU-only minimalizálás (P2.3, 12. döntés):** a fallback-ág + 4-rétegű OCR-chain (PyMuPDF4LLM / Tesseract / Claude Read / `text/pNNN.txt` cache) eltávolítva — a caption + text_context gépileg kész (MinerU); 02b csak `visual_content` + keyword-finomítás. §3.1 source-loop egyszerűsítve; §7 Tesseract/02c sorok törölve; pilot-script hivatkozás kivezetve. |
