---
name: NN_skill_name
title: NN_SKILL_NAME -- Rövid cím
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: YYYY-MM-DD
description: Egy mondatos leírás a skill céljáról és helyéről a pipeline-ban.
---

# NN_SKILL_NAME

## 1. Cél

Mi a lépés feladata? Mi a bemenete és kimenete egy mondatban?

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `N_raw_inputs/fajl` | előző lépés | leírás |

**Előfeltétel:** Mi kell teljesülni a futtatáshoz?

## 3. Eljárás

### 3.1. Lépés

```powershell
# Parancs példa
```

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `N_outputs/fajl` | leírás |

## 5. Ellenőrzés

- [ ] Ellenőrzési pont 1
- [ ] Ellenőrzési pont 2

## 6. Hibakezelés

<!-- SZABÁLY: Minden felfedezett hibát ÉS megoldást ide kell dokumentálni azonnal.
     Ne hozz létre külön pitfalls fájlt. Ha a hiba más lépést is érint, ott is jegyezd.
     Formátum: tömör táblázat-sor (Tünet | Ok | Megoldás). -->

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| tünet leírása | gyökérok | konkrét megoldás |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések.
     Lezárt tétel → Változásjegyzékbe, törlés innen. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| YYYY-MM-DD | 1.0 | Létrehozva |
