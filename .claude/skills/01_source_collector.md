---
name: 01_source_collector
title: 01_SOURCE_COLLECTOR — Forrásgyűjtés, elnevezés és citations.json
type: skill
tags: [meta, skill]
role: 😎+🤖
status: active
version: 1.6
updated: 2026-06-07
description: Heti források gyűjtése 1_raw_inputs/-ba egységes névvel, weblapok PDF-ként (képekkel!), eredeti→új név szótárral és citations.json-nal; használd a 00_init után, forrásgyűjtéskor — opcionális Deep Research-csel. Több jelölt + 😎-egyeztetés; 😎 saját fájlt is betehet; re-entry új forrásra (§3.8) stabil kulcsokkal.
---

# 01_SOURCE_COLLECTOR

## 1. Cél

A heti forrásokat (PDF, PPTX, weblap) `1_raw_inputs/`-ba rendezi **egységes néven**,
**visszakövethető** eredeti→új leképezéssel, és felépíti a `citations.json` bibliográfiát.
Opcionálisan **Deep Research**-csel bővít; a zárt hozzáférésűeknél szól, amit 😎 utólag letölt,
azt **retroaktívan** elnevezi és beírja.

**Input:** meglévő forrásfájlok + URL-ek (😎-tól) · **Output:** `1_raw_inputs/` (átnevezve) + `citations.json`

## 2. Bemenetek

| Adat | Forrás | Tartalom |
|:-----|:-------|:---------|
| Forrásfájlok (PDF/PPTX) | Felhasználó | Tankönyvek, előadások, cikkek |
| URL lista | Felhasználó | Weboldalak, cikk-linkek, DOI |
| `subject_status.md` | 00_init | Tantárgy terv (téma, szint → a kereséshez) |

**Előfeltétel:** `00_init` lefutott; `1_raw_inputs/` létezik.

## 3. Eljárás 😎+🤖

### 3.1. Forrásigény 😎+🤖

Kérdezd meg: **„Van már forrásod? Gyűjtsek-e még releváns anyagot?"** — 😎 dönt.
Ez a kérdés a gyűjtés végén megismételhető, amíg 😎 le nem zárja.

### 3.2. Naming convention 🤖

```
<szerzo><ev>_<tipus>.<ext>
```

| Mező | Szabály | Példa |
|:-----|:--------|:------|
| `<szerzo>` | Első szerző vezetékneve, kisbetű, ékezet nélkül | `gravdahl`, `oppenheim` |
| `<ev>` | Megjelenési év (4 jegy) | `1999` |
| `_<tipus>` | Lásd típustáblázat | `_paper`, `_book` |
| `.<ext>` | Lehetőleg `pdf` | `.pdf` |

| Kód | Mit jelent |
|:----|:-----------|
| `paper` | Folyóirat- vagy konferenciacikk |
| `book` | Teljes könyv |
| `chapter` | Könyvfejezet |
| `slides` | Előadásdiasor (PDF/PPTX) |
| `webpage` | Weboldal (PDF-ként mentve) |
| `report` | Technikai jelentés |
| `thesis` | Disszertáció |
| `NA` | Hiányzó adat |

Azonos szerző + év: `a`/`b`/`c` suffix (pl. `gravdahl1999a_book.pdf`).
A `<tipus>` megegyezik a `citations.json` `type` mezőjével (ez vezérli az IEEE-formátumot).

### 3.3. Forrásgyűjtés — opcionális Deep Research 🤖+😎

Ha 😎 kéri, Claude `WebSearch`-csel keres:
1. **Kulcscikkek** — leggyakrabban hivatkozott alapcikkek
2. **Oktatási anyagok** — lecture notes, tutorial, review (didaktikailag hasznos)
3. **Hazai/intézményi forrás** — ha van, preferált

**Több jelölt + 😎-egyeztetés (kötelező elv):** ne ragadd meg automatikusan az első
találatot. Gyűjts **több jelöltet**, és tisztázd 😎-val, *mire van valójában szüksége*
(mélység, áttekintés vs. mélyfúrás, hazai nyelv). A 😎 dönt — egy
gyenge/sovány forrás egyoldalú felvétele helyett kérj megerősítést vagy kínálj választást.

**😎 által betett fájl:** a 😎 maga is bedobhat fájlt a `1_raw_inputs/`-ba. Az ilyen
forrást Claude **retroaktívan** kezeli (átnevezés a 3.2 konvencióra + `citations.json`
bővítés a következő szabad kulcson, lásd 3.7–3.8).

**Access-detektálás** (tesztelt heurisztika): a forrás-URL-t lekérve, ha
`status < 400` és `content-type == application/pdf` → **open** → letöltés `1_raw_inputs/`-ba.
Egyébként → **closed**: listázd a **DOI + URL**-t, és **szólj 😎-nak**, hogy töltse le kézzel (→ 3.7).

### 3.4. Weblap → PDF 🤖 — **képekkel együtt** (vizuális gazdagság)

Weblapot **PDF-ként** ments (nem `.url`-ként), és **a képekkel együtt** — szöveg-only mentés
**tilos**, mert sérti a vizuális gazdagság elvét ([Instructions §7](../../Instructions.md)), és a
05/02 lépés sem talál belőle ábrát.

**Általános, forrásfüggetlen megoldás — headless Chromium `--print-to-pdf`.** Bármely URL-re
működik (úgy renderel, ahogy egy böngésző, a képekkel együtt), és **csak egy Chromium-binárist**
igényel — semmilyen Python-csomagot vagy site-specifikus API-t. Chromium-motor gyakorlatilag
minden gépen van: **Edge** (Win10/11 beépített), **Chrome**, vagy a projektbe már telepített
`chrome-headless-shell` (B-15). A böngésző-CLI a kanonikus mód:

```powershell
# Edge (vagy chrome.exe / chrome-headless-shell.exe — azonos flagek)
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" `
  --headless=new --disable-gpu --no-pdf-header-footer --no-first-run `
  --user-data-dir="<temp_profil>" --virtual-time-budget=20000 `
  --print-to-pdf="1_raw_inputs\<szerzo><ev>_webpage.pdf" "<URL>"
```

- A `--virtual-time-budget=20000` (≈ a script-világ `waitUntil:'networkidle'` megfelelője) megvárja
  a lusta/aszinkron tartalom (képek) betöltődését a nyomtatás előtt.
- Azonos motor scriptből (Playwright/Puppeteer): `page.goto(URL,{waitUntil:'networkidle'})` →
  `page.pdf({printBackground:true})`. Ugyanaz a Chromium, ha van scripting-runtime.

**Csak ha egyáltalán nincs Chromium-bináris** a gépen:
1. **Kézi:** [SingleFile](https://github.com/gildas-lormeau/SingleFile) bővítmény Edge/Chrome-ban.
2. **😎-ra bízás:** kérd meg 😎-t, hogy mentse/töltse fel a fájlt (→ 3.7).

> ⛔ **NEM általános megoldások** — ne ezekre építs:
> - **Site-specifikus render-endpoint** (pl. Wikipedia `…/api/rest_v1/page/pdf/{Title}`): a legtöbb
>   oldalon **nincs** ilyen, ezért nem módszer, csak ritka, oldalankénti kényelem.
> - **Sovány, kép nélküli szöveg-PDF** (pl. a kinyert szöveg `fitz`-be írva): a vizuális gazdagság
>   elvét sérti (Instructions §7), a 02/05 nem talál belőle ábrát — **tilos**.
>
> **Verifikáció (kötelező):** a mentett PDF tartalmazzon képeket (`fitz`: `page.get_images()`
> összege > 0). Ha 0 kép, a mentés hibás → másik módszer.

### 3.5. Átnevezés + provenance 🤖

Minden gyűjtött fájlt nevezz át a 3.2 konvencióra. A provenance (eredeti→új leképezés)
az `original_filename` mezőben él a `citations.json`-ban — külön szótárfájl nem kell.

### 3.6. citations.json 🤖

A `1_raw_inputs/citations.json` kulcs = hivatkozás száma (`"1"`, `"2"`, …) = szövegbeli `[1]`.
A `filename` az **új** névre mutat; az `original_filename` megőrzi az eredeti nevet (provenance).
A kész outputba (`## Hivatkozásjegyzék`) csak `author`/`title`/`year`/`venue`/`url` kerül — a fájlnevek nem.

```json
{
  "_meta": {"subject": "atg", "week": 1},
  "1": {
    "type": "book",
    "author": "J. T. Gravdahl",
    "title": "Compressor Surge and Rotating Stall",
    "year": 1999,
    "venue": "Springer",
    "filename": "gravdahl1999_book.pdf",
    "original_filename": "D6 kieg - gravdahl1999-Book--Compressor Surge and Rotating Stall.pdf"
  },
  "2": {
    "type": "webpage",
    "author": null,
    "title": "Compressor stall",
    "year": 2024,
    "url": "https://en.wikipedia.org/wiki/Compressor_stall",
    "filename": "wikipedia2024_webpage.pdf",
    "original_filename": "https://en.wikipedia.org/wiki/Compressor_stall"
  }
}
```

- **Kötelező:** `type`, `title`. A többi `null`/elhagyható.
- A `## Hivatkozásjegyzék` listát ebből rendereli a [`_ieee_renderer.py`](../../scripts/_ieee_renderer.py).

### 3.7. Retroaktív kezelés 😎→🤖

Amit 😎 utólag tölt le (closed access): Claude **átnevezi** a konvencióra,
és bővíti a `citations.json`-t (`filename` + `original_filename`).

### 3.8. Re-entry — új forrás később a pipeline-ban 😎→🤖

A 01 **nem csak a pipeline elején** futhat: egy későbbi checkpointon (jellemzően a
[`08_quality_reviewer`](08_quality_reviewer.md) §3.5 csatornáján) a 😎 jelezheti, hogy egy téma
új forrást igényel. Ekkor a 01 **újra belép**, de inkrementálisan:

- **Új `citations.json`-kulcs** a következő szabad sorszámon — a **meglévő kulcsok soha nem
  változnak** (a szövegbeli `[N]` hivatkozások stabilak maradnak).
- Az új forrás végigmegy a szokásos láncon: 01 (elnevezés + citations) → 02 (kinyerés) → 04
  (integráció **csak az érintett szekcióba**).
- A `_meta.week` változatlan; a forrás a meglévő heti mappába (`1_raw_inputs/`) kerül.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `1_raw_inputs/<szerzo><ev>_<tipus>.<ext>` | Átnevezett források (weblap is PDF) |
| `1_raw_inputs/citations.json` | Bibliográfia (IEEE-hez) + provenance (`original_filename`) |

## 5. Teszt

Fixture-alapú teszt (verifikált mechanizmusokkal):

- **Fixture:** `test_sources/atg/*` (6 PDF + 2 PPTX) → `1_raw_inputs/`; +1 weblap URL.
- **Akció:** átnevezés a 3.2 szerint; weblap→PDF a 3.4 Playwright-snippettel; `citations.json` felépítése (`filename` + `original_filename`).
- **Várt kimenet + verifikáció (lefuttatva):**
  - Weblap→PDF: a „Compressor stall" wiki → **5 oldalas, valid PDF** (`page.pdf()`).
  - Access-detektálás: arXiv-PDF → `application/pdf` = **open**; ScienceDirect → `text/html` = **closed**.
  - Minden `citations.json` `filename` létező fájlra mutat; `_ieee_renderer --dry-run` mind a típust (book/chapter/paper/slides/webpage/report/thesis) helyes IEEE-listává rendereli.
- **Eval:** „hiányzó fájl: nincs"; a renderelt szekció `[1]…[N]` típus-helyes.

## 6. Ellenőrzés

- [ ] Minden fájl a 3.2 konvenció szerint van elnevezve
- [ ] `citations.json` minden bejegyzésnél `original_filename` kitöltve
- [ ] Weblapok valid PDF-ként mentve (`%PDF` fejléc, >0 oldal)
- [ ] `citations.json` valid JSON; minden `filename` létező fájlra mutat
- [ ] Closed-access források jelölve, 😎 értesítve (3.7)

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `page.pdf()` hibázik | Nem headless Chromium | SingleFile bővítmény (3.4 alternatíva) kézzel |
| Forrás nem tölthető | Closed access / paywall | DOI+URL listázása → 😎 manuálisan tölti (3.7) |
| `JSONDecodeError` | Trailing comma / szintaxis | JSON linter |
| Duplikált kulcs | Kézi szerkesztés | `"1"`, `"2"`… egyediség |
| Ütköző fájlnév (szerző+év) | Azonos szerző+év | `a`/`b`/`c` suffix (3.2) |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- upstream: [00_init.md](00_init.md) · downstream: [02_image_extraction.md](02_image_extraction.md)
- [_ieee_renderer.py](../../scripts/_ieee_renderer.py) — a citations.json fogyasztója

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
| 2026-06-02 | 1.1 | Egységes `citations.json` (a `citations_seed` + a nem létező init-script megszűnt); `type`-alapú IEEE séma; `[1]` jelölés |
| 2026-06-03 | 1.2 | Sablonhoz igazítva: `role`, triggerelő `description`, §5 Teszt, upstream/downstream linkek |
| 2026-06-03 | 1.3 | Ideális forgatókönyv: naming convention, Deep Research + access-detektálás, weblap→PDF (Playwright, tesztelt), `_source_map.md` provenance, retroaktív kezelés; renderer `report`/`thesis`-re bővítve |
| 2026-06-03 | 1.4 | Provenance `citations.json`-ba (`original_filename` mező); `_source_map.md` kivezetett |
| 2026-06-07 | 1.5 | §3.8 **re-entry**: a 01 a pipeline közepén is futhat (08 §3.5 revíziós csatorna „új forrás" ága); inkrementális `citations.json`-bővítés a következő szabad kulcson, meglévő kulcsok stabilak. |
| 2026-06-07 | 1.6 | §3.3 **több jelölt + 😎-egyeztetés** (ne az első/sovány forrást ragadd meg; tisztázd, mire van szükség; 😎 saját fájlt is betehet); §3.4 **weblap→PDF képekkel** — a *general* megoldás a **headless Chromium `--print-to-pdf`** (csak böngésző-bináris kell: Edge/Chrome/chrome-headless-shell — nincs Python-csomag, nincs site-API); a site-specifikus render-endpoint (Wikipedia REST) és a sovány szöveg-PDF **explicit nem-általánosként** kizárva; kötelező kép-verifikáció. Edge-gel bizonyítva. (`quality_review_test` tanulság.) |
