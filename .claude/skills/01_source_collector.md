---
name: 01_source_collector
title: 01_SOURCE_COLLECTOR — Forrásgyűjtés és citations.json
type: skill
tags: [meta, skill]
role: 😎+🤖
status: active
version: 1.2
updated: 2026-06-03
description: Forrás-PDF-ek/URL-ek rendezése 1_raw_inputs/-ba és a citations.json bibliográfia felépítése; használd a 00_init után, új heti forrásgyűjtéskor, a 02 extrakció előtt.
---

# 01_SOURCE_COLLECTOR

## 1. Cél

A felhasználó által megadott URL-eket és PDF fájlokat `1_raw_inputs/`-ba rendezi,
és létrehozza a `citations.json` bibliográfiát a downstream lépések számára.

**Input:** URL lista + PDF fájlok (felhasználótól)
**Output:** `1_raw_inputs/` fájlok + `citations.json`

## 2. Bemenetek

| Adat | Forrás | Tartalom |
|:-----|:-------|:---------|
| URL lista | Felhasználó | Weboldalak, SlideShare, YouTube-transkript |
| PDF fájlok | Felhasználó | Tankönyvek, előadásanyagok, cikkek |
| `subject_status.md` | 00_init | Tantárgy terv + heti státusz |

**Előfeltétel:** `00_init` sikeresen lefutott, `1_raw_inputs/` mappa létezik.

## 3. Eljárás 😎+🤖

### 3.1. PDF-ek elhelyezése 😎

PDF-eket másold be közvetlenül:

```
{tantargy}/{N}_het/1_raw_inputs/{forras_nev}.pdf
```

Konvenció: `{szerzo}_{ev}_{kulcsszo}.pdf` — pl. `Proakis_2001_DSP.pdf`

### 3.2. URL-ek mentése 😎

Minden URL-t egy `.url` szövegfájlba mentsd:

```
{tantargy}/{N}_het/1_raw_inputs/{kulcsszo}.url
```

Tartalma egyetlen sor: a teljes URL.

### 3.3. citations.json létrehozása 🤖

A `citations.json`-t 🤖 Claude (vagy 😎 kézzel) tölti ki a `1_raw_inputs/` forrásai
alapján — nincs hozzá külön script. Kulcs = a hivatkozás száma (`"1"`, `"2"`, …),
ami megegyezik a szövegbeli `[1]`, `[2]` jelöléssel.

```json
{
  "_meta": {"subject": "atg", "week": 1},
  "1": {
    "type": "book",
    "author": "Gravdahl, J. T.",
    "title": "Compressor Surge and Rotating Stall",
    "year": 1999,
    "venue": "Springer",
    "filename": "gravdahl1999-Book.pdf",
    "pages": "1-45"
  },
  "2": {
    "type": "webpage",
    "author": null,
    "title": "Compressor stall",
    "year": 2024,
    "url": "https://en.wikipedia.org/wiki/Compressor_stall"
  }
}
```

- **`type`:** `paper` · `book` · `chapter` · `slides` · `webpage` (az IEEE formátumot vezérli).
- **Kötelező:** `type`, `title`. A többi `null`/elhagyható, de töltsd ki ahol tudod.
- **`filename`** a `1_raw_inputs/` fájlra mutat; webpage-nél `url`.
- A `## Hivatkozásjegyzék` listát ebből rendereli a [`_ieee_renderer.py`](../../scripts/_ieee_renderer.py).

### 3.4. Keressek még anyagot? 😎

A sources összegyűjtése után: **"Keressek még releváns anyagot?"** — felhasználó dönt,
mielőtt a 02-es lépés indul.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `1_raw_inputs/*.pdf` | Nyers PDF forrásanyagok |
| `1_raw_inputs/*.url` | URL hivatkozások |
| `1_raw_inputs/citations.json` | Bibliográfiai metaadatok (IEEE-hez) |

## 5. Teszt

- **Fixture (bemenet):** `test_sources/atg/*` (8 forrás: 6 PDF + 2 PPTX) → bemásolva `test_outputs/atg/1_het/1_raw_inputs/`-ba.
- **Akció:** 🤖 Claude kitölti a `citations.json`-t a §3.3 séma szerint, valódi `filename`-ekkel (6 bejegyzés: book / chapter / paper×2 / slides / webpage).
- **Várt kimenet:** valid `citations.json`; minden `filename` létező fájlra mutat; a `_ieee_renderer.py --dry-run` mind a 6 forrást IEEE-listává rendereli, hibátlanul.
- **Eval:** „hiányzó fájl: nincs"; a renderelt szekció `[1]`…`[6]` típus-helyes formátummal generálódik.

## 6. Ellenőrzés

- [ ] Minden PDF megnyitható (nem sérült)
- [ ] `citations.json` valid JSON, a kulcsok egyediek (`"1"`, `"2"`, …)
- [ ] Minden `filename` értéke létező fájlra mutat `1_raw_inputs/`-ban
- [ ] URL-ek elérhetők (gyors manuális ellenőrzés)

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `JSONDecodeError` a citations.json-nél | Trailing comma vagy szintaxishiba | JSON linterre futtatni |
| PDF nem nyílik meg MinerU-ban | Jelszóvédett PDF | Jelszó eltávolítása vagy kizárás |
| Duplikált kulcsok | Kézzel szerkesztett JSON | A `"1"`, `"2"`, … kulcsok egyediségét ellenőrizni |
| Hiányzó `author` mező | Ismeretlen szerző | `null` — elfogadható |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- upstream: [00_init.md](00_init.md) · downstream: [02_source_extractor.md](02_source_extractor.md)

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
| 2026-06-02 | 1.1 | Egységes `citations.json` (a `citations_seed` + a nem létező init-script megszűnt); `type`-alapú IEEE séma; `[1]` jelölés |
| 2026-06-03 | 1.2 | Sablonhoz igazítva: `role: 😎+🤖`, triggerelő `description`, §3 szerep-jelzések, §5 Teszt (verifikált `atg`-n), upstream/downstream linkek |
