---
name: 05_figure_integrator
title: 05_FIGURE_INTEGRATOR — Ábrabeillesztés
type: skill
tags: [meta, skill]
role: 🤖+🐍
status: active
version: 1.1
updated: 2026-06-03
description: figure_catalog alapján ábrák beillesztése a jegyzet megfelelő fejezet-szakaszaiba.
---

# 05_FIGURE_INTEGRATOR

## 1. Cél

A `figure_catalog.json`-ban leltározott ábrákat beilleszti a megfelelő fejezet-szakaszokba.
Az összegző dobozok elhelyezése külön lépés: [06_summarize_box_injector](06_summarize_box_injector.md).

**Input:** `4_wip_outputs/N_Jegyzet.md` + `2_clean_inputs/figure_catalog.json`
**Output:** `4_wip_outputs/N_Jegyzet.md` (ábrákkal gazdagítva, in-place)

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 04_content_synthesizer | WIP jegyzet szöveg |
| `2_clean_inputs/figure_catalog.json` | 02_image_extraction | Ábrák metaadatai + `suggested_section` |

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

### 3.3. Manuális finomhangolás

Claude ellenőrzi a beillesztett ábrákat:
- Kontextuálisan illeszkedik-e az adott fejezethez?
- Placeholder-ek feloldása vagy megtartása (ha nem illeszthető)

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Jegyzet.md` | Ábrahivatkozásokkal gazdagított verzió |

## 5. Ellenőrzés

- [ ] Minden `figure_catalog` bejegyzés beillesztve vagy placeholder-rel jelezve
- [ ] Képútvonalak érvényesek (relatív, létező fájl)
- [ ] `<!-- FIGURE: -->` placeholder-ek számát naplózd (felhasználó eldönti mi legyen velük)

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Ábra duplikáltan jelenik meg | Script kétszer futott | `N_Jegyzet.md` visszaállítás git-ből + újrafuttatás |
| `suggested_section` nem talál fejezetet | Fejezetnév változott 04-ben | `figure_catalog.json` manuális frissítés |
| Képfájl hiányzik | MinerU nem mentette | `<!-- FIGURE: {id} — MISSING -->` jelölés |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [04_content_synthesizer.md](04_content_synthesizer.md) — upstream
- [06_summarize_box_injector.md](06_summarize_box_injector.md) — downstream

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
- ⚡ HIBA: a `05_figure_mapper.py` inkompatibilis a v4 `figure_catalog.json`-nal (beágyazott `_meta`+`sources` sémát laposként olvas), és valójában nem szúr be képet — csak `inserted_after_paragraph`-ot ír a katalógusba. A `<!-- FIGURE: source/fig_id -->` placeholder-feloldást (skill §3.3) jelenleg Claude végzi kézzel. Script-átírás: [project_status.md](../project_status.md) B-10.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (mint 05_visual_enricher) |
| 2026-06-03 | 1.1 | Szétválasztva: összegző dobozok → 06_summarize_box_injector; átnevezés figure_integrator-ra; TODO lezárva |
