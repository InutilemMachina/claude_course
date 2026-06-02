---
name: 01_source_collector
title: 01_SOURCE_COLLECTOR — Forrásgyűjtés és citations.json
type: skill
tags: [meta, skill]
status: active
version: 1.1
updated: 2026-06-02
description: URL-ek és PDF-ek összegyűjtése 1_raw_inputs/-ba, majd a citations.json bibliográfia létrehozása.
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

## 3. Eljárás

### 3.1. PDF-ek elhelyezése

PDF-eket másold be közvetlenül:

```
{tantargy}/{N}_het/1_raw_inputs/{forras_nev}.pdf
```

Konvenció: `{szerzo}_{ev}_{kulcsszo}.pdf` — pl. `Proakis_2001_DSP.pdf`

### 3.2. URL-ek mentése

Minden URL-t egy `.url` szövegfájlba mentsd:

```
{tantargy}/{N}_het/1_raw_inputs/{kulcsszo}.url
```

Tartalma egyetlen sor: a teljes URL.

### 3.3. citations.json létrehozása

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

### 3.4. Keressek még anyagot?

A sources összegyűjtése után: **"Keressek még releváns anyagot?"** — felhasználó dönt,
mielőtt a 02-es lépés indul.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `1_raw_inputs/*.pdf` | Nyers PDF forrásanyagok |
| `1_raw_inputs/*.url` | URL hivatkozások |
| `1_raw_inputs/citations.json` | Bibliográfiai metaadatok (IEEE-hez) |

## 5. Ellenőrzés

- [ ] Minden PDF megnyitható (nem sérült)
- [ ] `citations.json` valid JSON, a kulcsok egyediek (`"1"`, `"2"`, …)
- [ ] Minden `filename` értéke létező fájlra mutat `1_raw_inputs/`-ban
- [ ] URL-ek elérhetők (gyors manuális ellenőrzés)

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `JSONDecodeError` a citations.json-nél | Trailing comma vagy szintaxishiba | JSON linterre futtatni |
| PDF nem nyílik meg MinerU-ban | Jelszóvédett PDF | Jelszó eltávolítása vagy kizárás |
| Duplikált kulcsok | Kézzel szerkesztett JSON | A `"1"`, `"2"`, … kulcsok egyediségét ellenőrizni |
| Hiányzó `author` mező | Ismeretlen szerző | `null` — elfogadható |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [02_source_extractor.md](02_source_extractor.md) — következő lépés

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
| 2026-06-02 | 1.1 | Egységes `citations.json` (a `citations_seed` + a nem létező init-script megszűnt); `type`-alapú IEEE séma; `[1]` jelölés |
