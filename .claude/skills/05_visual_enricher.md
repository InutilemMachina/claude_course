---
name: 05_visual_enricher
title: 05_VISUAL_ENRICHER — Ábrabeillesztés és összegző dobozok
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-06-01
description: figure_catalog alapján ábrák beillesztése a jegyzetbe, fejezetek végére összegző dobozok elhelyezése.
---

# 05_VISUAL_ENRICHER

## 1. Cél

A `figure_catalog.json`-ban leltározott ábrákat beilleszti a megfelelő fejezet-szakaszokba,
és minden fejezet végére összegző dobozt helyez el.

**Input:** `4_wip_outputs/N_Jegyzet.md` + `2_clean_inputs/figure_catalog.json`
**Output:** `4_wip_outputs/N_Jegyzet.md` (gazdagítva, in-place)

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 04_content_synthesizer | WIP jegyzet szöveg |
| `2_clean_inputs/figure_catalog.json` | 02_source_extractor | Ábrák metaadatai + `suggested_section` |

**Előfeltétel:** `04_content_synthesizer` lefutott; `figure_catalog.json` nem üres.

## 3. Eljárás

### 3.1. Figure mapper futtatása

```powershell
python scripts/05_figure_mapper.py --week N --subject "Jelatvitel"
```

- Beolvassa `figure_catalog.json`-t
- `suggested_section` alapján a megfelelő fejezet után illeszti be az ábrát
- Ha `suggested_section` null: `<!-- FIGURE: {id} — elhelyezendő -->` placeholder

### 3.2. Ábrabeillesztés formátuma

```markdown
![{caption}]({filename})
*{id} — {caption}* (Forrás: {source}, {page}. o.)
```

### 3.3. Összegző dobozok elhelyezése

Minden `## Fejezetnév` blokk végére:

```markdown
> 📦 **Összegző — Fejezetnév**
> **Kulcsgondolat:** [1-2 mondatos lényeg]
> **Kulcsfogalmak:** fogalom1, fogalom2, fogalom3
> **Képletek:** $Eq.X.Y$ — rövid megnevezés
```

### 3.4. Manuális finomhangolás

Claude ellenőrzi a beillesztett ábrákat:
- Kontextuálisan illeszkedik-e az adott fejezethez?
- Placeholder-ek feloldása vagy megtartása (ha nem illeszthető)

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Jegyzet.md` | Gazdagított verzió, ábrahivatkozásokkal és összegző dobozokkal |

## 5. Ellenőrzés

- [ ] Minden `figure_catalog` bejegyzés beillesztve vagy placeholder-rel jelezve
- [ ] Összegző doboz minden `##` fejezet végén megjelenik
- [ ] Képútvonalak érvényesek (relatív, létező fájl)
- [ ] `<!-- FIGURE: -->` placeholder-ek számát naplózd (felhasználó eldönti mi legyen velük)

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Ábra duplikáltan jelenik meg | Script kétszer futott | `N_Jegyzet.md` visszaállítás git-ből + újrafuttatás |
| `suggested_section` nem talál fejezetet | Fejezetnév változott 04-ben | `figure_catalog.json` manuális frissítés |
| Összegző doboz hiányos fejezetnél | `##` heading elmaradt a szintézisben | 04 kimenetet javítani, majd újrafuttatni |
| Képfájl hiányzik | MinerU nem mentette | `<!-- FIGURE: {id} — MISSING -->` jelölés |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [04_content_synthesizer.md](04_content_synthesizer.md) — upstream
- [06_typesetter.md](06_typesetter.md) — downstream

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
- `05_figure_mapper.py` a `09_figure_mapper.py` másolata — egységesítés szükséges lehet

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
