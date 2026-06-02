---
name: 01_source_collector
title: 01_SOURCE_COLLECTOR — Forrásgyűjtés és citations_seed
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-06-01
description: URL-ek és PDF-ek összegyűjtése 1_raw_inputs/-ba, majd citations_seed.json inicializálása.
---

# 01_SOURCE_COLLECTOR

## 1. Cél

A felhasználó által megadott URL-eket és PDF fájlokat `1_raw_inputs/`-ba rendezi,
és létrehozza a `citations_seed.json` bibliográfiai alapot a downstream lépések számára.

**Input:** URL lista + PDF fájlok (felhasználótól)
**Output:** `1_raw_inputs/` fájlok + `citations_seed.json`

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

### 3.3. citations_seed.json létrehozása

```powershell
# Manuálisan vagy segédscripttel
python scripts/01_citations_seed_init.py --week N --subject "Jelatvitel"
```

`citations_seed.json` formátum:

```json
[
  {
    "id": "Proakis2001",
    "author": "Proakis, J. G.",
    "title": "Digital Signal Processing",
    "year": 2001,
    "filename": "Proakis_2001_DSP.pdf",
    "url": null,
    "pages": "1-45"
  },
  {
    "id": "Wiki_DFT",
    "author": null,
    "title": "Discrete Fourier Transform",
    "year": 2024,
    "filename": null,
    "url": "https://en.wikipedia.org/wiki/Discrete_Fourier_transform",
    "pages": null
  }
]
```

**Kötelező mezők:** `id`, `title`. Többi mező `null` megengedett, de töltsd ki ahol tudod.

### 3.4. Keressek még anyagot?

A sources összegyűjtése után: **"Keressek még releváns anyagot?"** — felhasználó dönt,
mielőtt a 02-es lépés indul.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `1_raw_inputs/*.pdf` | Nyers PDF forrásanyagok |
| `1_raw_inputs/*.url` | URL hivatkozások |
| `1_raw_inputs/citations_seed.json` | Bibliográfiai metaadatok |

## 5. Ellenőrzés

- [ ] Minden PDF megnyitható (nem sérült)
- [ ] `citations_seed.json` valid JSON, `id` mezők egyediek
- [ ] Minden `filename` értéke létező fájlra mutat `1_raw_inputs/`-ban
- [ ] URL-ek elérhetők (gyors manuális ellenőrzés)

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `JSONDecodeError` a citations_seed-nél | Trailing comma vagy szintaxishiba | JSON linterre futtatni |
| PDF nem nyílik meg MinerU-ban | Jelszóvédett PDF | Jelszó eltávolítása vagy kizárás |
| Duplikált `id` mezők | Kézzel szerkesztett JSON | `id` értékek egyediségét ellenőrizni |
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
