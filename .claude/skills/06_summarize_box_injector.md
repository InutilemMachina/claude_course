---
name: 06_summarize_box_injector
title: 06_SUMMARIZE_BOX_INJECTOR — Összegző dobozok
type: skill
tags: [meta, skill]
role: 🤖
status: active
version: 1.0
updated: 2026-06-03
description: Minden fejezet végére összegző doboz (kulcsgondolat, kulcsfogalmak, képletek) elhelyezése a jegyzetben.
---

# 06_SUMMARIZE_BOX_INJECTOR

## 1. Cél

Az ábrákkal gazdagított jegyzet minden `## Fejezet` blokkjának végére összegző dobozt
helyez el. Az ábrabeillesztés külön, megelőző lépés: [05_figure_integrator](05_figure_integrator.md).

**Input:** `4_wip_outputs/N_Jegyzet.md`
**Output:** `4_wip_outputs/N_Jegyzet.md` (összegző dobozokkal, in-place)

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 05_figure_integrator | Ábrákkal gazdagított WIP jegyzet |

**Előfeltétel:** `05_figure_integrator` lefutott.

## 3. Eljárás

### 3.1. Összegző dobozok elhelyezése

Minden `## Fejezetnév` blokk végére:

```markdown
> 📦 **Összegző — Fejezetnév**
> **Kulcsgondolat:** [1-2 mondatos lényeg]
> **Kulcsfogalmak:** fogalom1, fogalom2, fogalom3
> **Képletek:** $Eq.X.Y$ — rövid megnevezés
```

### 3.2. Tartalmi szabályok

- **Kulcsgondolat:** a fejezet lényege 1-2 mondatban, nem felsorolás.
- **Kulcsfogalmak:** a fejezetben bevezetett 3-6 fogalom.
- **Képletek:** a fejezet központi képletei, rövid megnevezéssel (ha van).
- A doboz a fejezetben ténylegesen szereplő tartalmat tükrözze — ne vezessen be új fogalmat.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Jegyzet.md` | Összegző dobozokkal kiegészített verzió |

## 5. Ellenőrzés

- [ ] Összegző doboz minden `##` fejezet végén megjelenik
- [ ] A doboz csak a fejezetben szereplő fogalmakra/képletekre hivatkozik
- [ ] A `> 📦` blockquote formátum egységes

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Összegző doboz hiányos fejezetnél | `##` heading elmaradt a szintézisben | 04 kimenetet javítani, majd újrafuttatni |
| Doboz új, fejezeten kívüli fogalmat tartalmaz | Claude túláltalánosított | Dobozt a fejezet tartalmára szűkíteni |
| Doboz duplikáltan jelenik meg | Lépés kétszer futott | `N_Jegyzet.md` visszaállítás git-ből + újrafuttatás |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [05_figure_integrator.md](05_figure_integrator.md) — upstream
- [07_typesetter.md](07_typesetter.md) — downstream

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
-

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-03 | 1.0 | Létrehozva (05_visual_enricher összegző-doboz részéből kiválasztva) |
