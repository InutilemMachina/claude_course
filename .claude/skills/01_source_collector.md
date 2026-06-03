---
name: 01_source_collector
title: 01_SOURCE_COLLECTOR — Forrásgyűjtés, elnevezés és citations.json
type: skill
tags: [meta, skill]
role: 😎+🤖
status: active
version: 1.4
updated: 2026-06-03
description: Heti források gyűjtése 1_raw_inputs/-ba egységes névvel, weblapok PDF-ként, eredeti→új név szótárral és citations.json-nal; használd a 00_init után, forrásgyűjtéskor — opcionális Deep Research-csel.
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

**Access-detektálás** (tesztelt heurisztika): a forrás-URL-t lekérve, ha
`status < 400` és `content-type == application/pdf` → **open** → letöltés `1_raw_inputs/`-ba.
Egyébként → **closed**: listázd a **DOI + URL**-t, és **szólj 😎-nak**, hogy töltse le kézzel (→ 3.7).

### 3.4. Weblap → PDF 🤖

Weblapot **PDF-ként** ments (nem `.url`-ként). Tesztelt mód — Playwright headless print:

```js
async (page) => {
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 });
  await page.pdf({ path: '1_raw_inputs/<szerzo><ev>_webpage.pdf', format: 'A4', printBackground: true });
}
```

Alternatíva (kézi): [SingleFile](https://github.com/gildas-lormeau/SingleFile) bővítmény Edge/Chrome-ban (önálló HTML/PDF).

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
