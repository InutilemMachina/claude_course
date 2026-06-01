---
name: 00_init
title: 00_INIT — Tantárgy inicializálás és mappastruktúra
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-06-01
description: Új tantárgy pipeline-jának inicializálása — context.json és heti mappastruktúra létrehozása.
---

# 00_INIT

## 1. Cél

Új tantárgy esetén létrehozza a `context.json` konfigurációt és a teljes heti mappastruktúrát,
hogy a downstream lépések egységes útvonalakon dolgozhassanak.

**Input:** Tantárgy neve, hetek száma, szint (BSc/MSc)
**Output:** `context.json` + `{tantargy}/{N_het}/` mappák (1_raw_inputs … 5_clean_outputs, 3_mindmap)

## 2. Bemenetek

| Adat | Forrás | Tartalom |
|:-----|:-------|:---------|
| Tantárgy neve | Felhasználó | pl. `Jelatvitel` |
| Hetek száma | Felhasználó | egész szám, pl. `12` |
| Szint | Felhasználó | `BSc` vagy `MSc` |

**Előfeltétel:** A projekt gyökérkönyvtár létezik és írható.

## 3. Eljárás

### 3.1. context.json létrehozása

```powershell
python scripts/00_init_course.py --subject "Jelatvitel" --weeks 12 --level BSc
```

Generált `context.json` struktúra:

```json
{
  "subject": "Jelatvitel",
  "weeks": 12,
  "level": "BSc",
  "created": "YYYY-MM-DD",
  "base_path": "{tantargy}/"
}
```

### 3.2. Mappastruktúra

A script minden hétre létrehozza:

```
{tantargy}/
  {N}_het/
    1_raw_inputs/
    2_clean_inputs/
    3_mindmap/
    4_wip_outputs/
    5_clean_outputs/
```

### 3.3. Ellenőrzés

```powershell
# Mappák meglétének gyors ellenőrzése
Get-ChildItem -Path "{tantargy}" -Recurse -Directory | Select-Object FullName
```

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `context.json` | Tantárgy metaadatok, szint, hetek száma |
| `{tantargy}/{N}_het/1_raw_inputs/` | Üres — forrásgyűjtésre vár |
| `{tantargy}/{N}_het/3_mindmap/` | Üres — mindmap buildernek |
| `{tantargy}/{N}_het/5_clean_outputs/` | Üres — végleges outputoknak |

## 5. Ellenőrzés

- [ ] `context.json` jól formált JSON és tartalmaz `subject`, `weeks`, `level` mezőket
- [ ] Minden hétre (`1` … `N`) létrejött mind a 6 almappa
- [ ] `3_mindmap/` mappa minden hétnél jelen van (újítás!)
- [ ] Script naplója nem tartalmaz `ERROR` sort

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `FileExistsError` a mappáknál | Már inicializált tantárgy | `--force` flag vagy manuális törlés |
| `context.json` hiányzó mező | Régi script verzió | Script frissítése, `3_mindmap` ág hozzáadása |
| Hetek száma 0 | Rossz CLI paraméter | `--weeks` értékét ellenőrizd |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [01_source_collector.md](01_source_collector.md) — következő lépés

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
- `3_mindmap/` mappa kezelése tesztelendő az új script verzióval

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
