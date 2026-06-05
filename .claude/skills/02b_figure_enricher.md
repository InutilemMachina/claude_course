---
name: 02b_figure_enricher
title: 02b_figure_enricher — Ábra-meta gazdagító (image_rag bootstrap)
type: skill
tags: [meta, skill]
role: 🤖
status: active
version: 1.2
updated: 2026-06-05
description: Ha `02_mineru_to_catalog.py` futott (standard), Claude CSAK a `visual_content`-et tölti (`Read(image)` + leírás) és finomítja a keywords draft-ot. caption + text_context gépileg előtöltve. Fallback (ha csak `02_image_extraction` futott): teljes backend-chain (MinerU > PyMuPDF4LLM > Tesseract > Claude Read). Használd a 02* lépések után, a 03 előtt.
---

# 02b_figure_enricher

## 1. Cél

### Ha `02_mineru_to_catalog.py` futott (standard pipeline, v1.2 viselkedés)

A `figure_catalog.json` mezőinek döntő többsége **gépileg előtöltve** (caption, text_context, keywords draft). Claude 02b-ben **csak** a következőket csinálja:

1. **`visual_content`**: minden bejegyzésnél `Read(image)` → 1-3 mondatos leírás (amit csak vizuálisan látni).
2. **`keywords` finomítás**: ha a szkript draft < 3 tag, vagy ha a vizuális tartalom lényeges új tag-eket hoz (pl. „surge line", „pressure ratio").

**Ez drasztikusan csökkenti a session-munkát**: caption-keresés + text extraction → Claude már nem csinálja.

### Ha csak `02_image_extraction.py` futott (fallback pipeline)

Teljes mező-kitöltés szükséges: caption, text_context, visual_content, keywords — a §3.1 backend-chain szerint.

**Input:** `2_clean_inputs/figure_catalog.json` (v4 séma) · **Output:** ugyanaz, `visual_content` kitöltve, `_status: "draft"`. A 😎 véglegesítés (`caption_verified:true`) külön gesztus.

## 2. Bemenetek

| Fájl | Honnan (skill) | Tartalom |
|:-----|:---------------|:---------|
| `2_clean_inputs/figure_catalog.json` | `02_image_extraction` | v4 séma, strukturális mezők kitöltve, meta-mezők többsége `null`/`[]` |
| `1_raw_inputs/*.pdf`, `*.pptx` | `01_source_collector` | Szövegkontextus forrása (born-digital PDF text-stream / PPTX szöveg) |
| `2_clean_inputs/<stem>/text/pNNN.txt` | `02_image_extraction` OCR-cache | Szkennelt PDF-oldalak OCR-szövege (ha Tesseract elérhető volt) |
| `2_clean_inputs/<stem>/images/pNNN_figNNN.png` | `02_image_extraction` | A kép-fájlok — Claude `Read`-eli |
| `2_clean_inputs/<stem>/mineru/{<stem>.md, <stem>_content_list.json, images/}` | `02c_mineru_layout` (opcionális) | Layout-aware markdown + captionpárosítás + LaTeX formula. Ha létezik → preferenciát kap |

**Előfeltétel:** `02_image_extraction` lefutott, a katalógus v4 sémában van, `needs_crop:true` bejegyzésekhez a manuális vágás opcionálisan kész.

## 3. Eljárás 🤖

Forrásonként dolgozunk: egy forrás-PDF szövegét **egyszer** olvasuk be (cache), majd ábránként töltjük a meta-mezőket.

### 3.1. Source-loop — backend-preferencia chain (v1.1)

Az image_rag_OCR sprint komparatív kutatása (lásd `.claude/sprints/image_rag/ocr_lab/decision.md`) szerint a `text_context` legjobb forrása forrás-típustól függ. A skill **négy-rétegű preferencia chain**-t követ source-onként:

```
1. MinerU       (2_clean_inputs/<stem>/mineru/<stem>.md + _content_list.json)
       ↓ ha hiányzik VAGY a forrás-szegmens üres
2. PyMuPDF4LLM  (born-digital text-stream — pip install pymupdf4llm)
       ↓ ha üres (szkennelt)
3. Tesseract    (2_clean_inputs/<stem>/text/pNNN.txt — a 02 cache-elte)
       ↓ ha üres VAGY magyar oldalon char_count < 0.7 × PyMuPDF-mérce
4. Claude Read fallback  (Read PNG → értsd meg → Write text/pNNN.txt — idempotens cache)
```

Minden `source_file` egyedi értékére (a `catalog["sources"]` kulcsain iterálva):

1. **Forrás-szöveg betöltése a chain mentén:**
   - **L1 (MinerU)**: ha létezik `<stem>/mineru/<stem>.md`, töltsd be; ha létezik `<stem>/mineru/<stem>_content_list.json`, parse-old a `text_level`/`type=image`/`img_caption` mezőket — ezek a `caption`, `visual_content`, `text_context` elsődleges forrásai. Heading-szintek a 03 mindmap-nek is.
   - **L2 (PyMuPDF4LLM)**: `import pymupdf4llm; pymupdf4llm.to_markdown(pdf, pages=[…])` oldalonkénti vagy forrás-szintű MD. Born-digital pontosabb mint Tesseract.
   - **L3 (Tesseract cache)**: olvasd a `text/pNNN.txt`-t. Ha hiányzik a 02 nem futtatott OCR-t (pl. nincs Tesseract binary) → L4.
   - **L4 (Claude Read fallback)**: ha az oldalhoz nincs használható szöveg, ÉS a `images/pNNN_fig*.png` (vagy szkennelt oldal-render) létezik, akkor a session `Read`-eli a PNG-t, kiolvassa a látható szöveget magyar diakritikákkal és `Write`-tal idempotensen kiírja a `text/pNNN.txt`-be. Ezt **egyszer csinálja oldalanként** (cache hit esetén skip).
   - PPTX: `python-pptx` text-frame iteration (változatlan).
2. **A forráshoz tartozó figures listázása**: `catalog["sources"][src]["figures"]`.
3. **Minden figure-re** (`fig_id` sorrendben):
   - `Read` az image fájl a `path` mezőből → vizuális tartalom megértése.
   - A `page` mező alapján a forrás-szövegben lokalizáld a kép környezetét (felirat + körülvevő bekezdés). MinerU `_content_list.json` esetén a `page_idx == page-1` és `img_caption` mezők közvetlen találat.
   - Töltsd ki a meta-mezőket (lásd 3.2.).
4. **Mentés**: forrás végén egy `save_catalog()` hívás. A `_status` automatikusan újraszámolódik (`un-processed → draft`).

**Megjegyzés:** a chain nem kötelező, csak ajánlott. Ha csak Tesseract output van (mert `02c_mineru_layout` nem futott), a skill változatlanul működik.

### 3.2. Mezők kitöltési szabályai

| Mező | Tartalom | Forrás | Validáció |
|------|----------|--------|-----------|
| `caption` | Az ábra eredeti felirata, paragrafus-szennyezés nélkül. Csak akkor írd át, ha bizonyíthatóan jobb. | `Read(image)` + forrás-szöveg | Pont nélkül NE végződjön egy paragrafus-folytatással. |
| `caption_verified` | Soha NE állítsd `true`-ra — ez kizárólag a 😎 gesture. | — | 02b mindig hagyja `false`-on. |
| `visual_content` | 1-3 mondat magyarul: mit ábrázol vizuálisan. Diagram-típus, tengelyek/címkék, fő elemek, esetleg trend. **Nem** értelmezés, hanem leírás. | `Read(image)` | Ne tartalmazzon "az ábra…" sablont; legyen specifikus. |
| `text_context` | 1-3 mondat: milyen koncepció / téma kerül elő a szövegkörnyezetben. Inline jelölheti a hivatkozási helyeket: "Hivatkozás: p3 (Section 2 intro)". | forrás-szöveg page körül + OCR-cache ha van | Forráshoz hű, ne extrapoláljon. |
| `keywords` | 3-8 kulcsszó. Logók/dekorációk: `["logo"]` vagy `["decoration"]`. | visual_content + text_context | Konkrét, kereshető tag-ek. |
| `notes` | NE szerkeszd — ez a 😎 free space-e. | — | 02b sosem ír bele (egyetlen kivétel: `"⚠️ scanned, no OCR text"` ha tényleg semmi context). |

### 3.2.0. Az `_status` mező (derivált, ne szerkeszd)

A 02 script automatikusan újraszámolja minden `save_catalog()` előtt. **4-állapotú** (Block 9):

| `_status` | Feltétel | Mit jelent |
|-----------|----------|------------|
| `complete` | `caption_verified:true` ÉS `visual_content` kitöltve | Teljesen kész, 05 retrieval használhatja |
| `caption-ok` | `caption_verified:true`, de `visual_content:null` | Caption jóváhagyva, 02b bootstrap hiányzik |
| `draft` | `visual_content` kitöltve, de `caption_verified:false` | 02b futott, 😎 jóváhagyás hiányzik |
| `un-processed` | Sem `caption_verified`, sem `visual_content` | 02b még nem futott |

**`_` prefix konvenció**: a `_status` mezőt — és minden `_`-szel kezdődő mezőt — csak a script kezeli. A `_meta` blokk is script-managed (csak `schema_version`, `last_updated`, `_guide` van benne). Az útmutató a JSON melletti `CATALOG_GUIDE.md` fájlban él.

A 02b skill célja: `un-processed` → `draft` (visual_content kitöltése). A `caption-ok` → `complete` átmenetet is a 02b hozhatja, ha a captionnel együtt a visual_content-et is tölti. A végleges `complete` átmenetet a 😎 csinálja a `caption_verified:true` flippeléssel.

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
- `text_context`: rövid magyarázat hogy honnan származik (pl. `"slide-deck branding footer"`)

Séma-bővítés (pl. `keep:false`) NEM szükséges — a 05 retrieval a `"logo" in keywords` szűrővel kihagyja.

### 3.4. Idempotencia

A skill csak akkor írja felül a mezőt, ha **null vagy üres** volt. `caption_verified:true` bejegyzéseket meg sem érinti.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `2_clean_inputs/figure_catalog.json` | v4, kitöltött szemantikus mezőkkel, `_status` átáll `un-processed → draft`-ra. `_meta.last_updated` frissül. |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het/2_clean_inputs/figure_catalog.json` friss regen (minden entry `_status:"un-processed"`).
- **Akció (pilot):** `python .claude/sprints/image_rag/apply_meta_bootstrap.py` → 8 bejegyzés (chattopadhyay + tavakoli) feltöltve.
- **Várt:** 8 bejegyzésnél minden szemantikus mező nem-null/nem-üres; `caption_verified:true` (Block 1 bugfix); `_status:"verified"`. `_meta.last_updated` ma.
- **Eval:** spot-check 2-3 bejegyzésnél: `visual_content` egyezik a kép tartalmával; `text_context` a forrás-szöveg lényegét adja.

## 6. Ellenőrzés

- [ ] Feldolgozott bejegyzéseknek van `visual_content` (nem null, ≥10 karakter)
- [ ] `text_context` nem null
- [ ] `keywords` ≥1 elem (logók: `["logo"]` is OK)
- [ ] Logók `keywords: ["logo"]`-val jelölve (NEM kapnak részletes meta-t)
- [ ] `caption_verified` 02b által NEM lett `true` (csak 😎-tól)
- [ ] `_status` minden bejegyzésnél a 3 érték egyike
- [ ] Idempotens újrafuttatás: a `_status: "verified"` bejegyzéseken 0 változás

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `Read(image)` hibás karaktert ad | PNG sérült vagy nem PNG | Nézd meg a fájlméretet; ha 0 byte, `02` újra futtatása |
| Szkennelt forrásnál üres szövegkörnyezet | OCR nem futott (Tesseract hiánya) | Aktiválható L4 Claude Read fallback (lásd §3.1) — nincs külső dep. Vagy: `pip install pytesseract` + UB-Mannheim Tesseract binary (PATH-ra vagy `C:\Program Files\Tesseract-OCR`); magyar nyelv: `hun.traineddata` `~/.tessdata/` alá + `TESSDATA_PREFIX` env-var |
| Magyar oldalon Tesseract diakritika hibás (pl. „centrifugalis" ≠ „centrifugális") | Tesseract LSTM gyengeség `hun` modellen low-DPI render-újra-OCR-en | Preferálj PyMuPDF4LLM-et (born-digital) vagy MinerU-t (`-l latin`); end-game Claude Read fallback. Mérés alapja: 0.59 char ratio nagyi-n (lásd ocr_lab/decision.md) |
| MinerU output dupla `<stem>/auto/` szint | MinerU 2.7.6 mindig `<output>/<stem>/auto/`-ba ír | A `02c_mineru_layout.py` flat-eli `2_clean_inputs/<stem>/mineru/`-ra `shutil.move`-val |
| `caption` és kép nem egyezik | Auto-detekció félrement (lásd 02 §9.1) | Caption korrekció: írd át manuálisan; user `caption_verified:true`-t állít |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- upstream (standard): `scripts/02_mineru_to_catalog.py` · upstream (fallback): [02_image_extraction.md](02_image_extraction.md) · downstream: [03_mindmap_builder.md](03_mindmap_builder.md), [05_figure_integrator.md](05_figure_integrator.md)
- Sprint kontextus: [.claude/sprints/image_rag/image_rag_plan.md](../sprints/image_rag/image_rag_plan.md)

## 9. Visszajelzések 😎+🤖

- 💬 NOTE: Az image_rag retrieval (05) hatékonysága a `keywords` minőségén áll vagy bukik. Cél: 3-5 közepes specifikusságú tag/ábra.
- 💡 IDEA: Egy jövőbeli verzió embedding-alapú retrieval-hez `keyword_embedding: [...]` mezőt gyűjthet — most lexikális (TF-IDF/BM25) elég.

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-05 | 1.2 | MinerU-first pipeline. §1 kettéválasztva (standard vs fallback). Claude feladata redukálva: csak `visual_content` + keywords finomítás ha 02_mineru_to_catalog futott. |
| 2026-06-05 | 1.1 | image_rag_OCR sprint. §3.1 backend-preferencia chain (MinerU > PyMuPDF4LLM > Tesseract > Claude Read). §7 új sorok: magyar diakritika gyengeség, MinerU dupla-szint. Hivatkozás: `.claude/sprints/image_rag/ocr_lab/decision.md`. |
| 2026-06-04 | 1.0 | Létrehozva (image_rag sprint, Block 8). v4 katalógus séma. atg/1_het pilot: chattopadhyay + tavakoli (8 ábra). |
