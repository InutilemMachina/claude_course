---
name: 05_figure_integrator
title: 05_FIGURE_INTEGRATOR — Ábrabeillesztés
type: skill
tags: [meta, skill]
role: 🤖+🐍
status: active
version: 2.0
updated: 2026-06-12
description: A 04 által elhelyezett `<!-- FIGURE: src/id -->` placeholdereket a 05_figure_mapper.py determinisztikusan feloldja v4-katalógus lookuppal (kép-út + citáció + oldal); a magyar, önálló koherens feliratot Claude finomítja (Instructions §7.1).
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
| `4_wip_outputs/N_Jegyzet.md` | 04_content_synthesizer | WIP jegyzet `<!-- FIGURE: src/id -->` placeholderekkel |
| `2_clean_inputs/figure_catalog.json` | 02_image_extraction | Ábrák v4-metaadatai (path, caption, citation_key, page) |

**Előfeltétel:** `04_content_synthesizer` lefutott és elhelyezte a `<!-- FIGURE: src/id -->` placeholdereket; `figure_catalog.json` v4 sémájú, nem üres.

## 3. Eljárás

### 3.1. Placeholder-feloldás 🐍 (determinisztikus)

A 04 (Claude) oda helyez `<!-- FIGURE: <forrás>/<fig_id> -->` placeholdert, ahova ábra kerül. A
script ezeket **determinisztikusan** feloldja a v4-katalógusból (kép-út + citáció-kulcs + oldalszám):

```powershell
python scripts/05_figure_mapper.py --week-dir test_outputs/<tárgy>/N_het
```

- Minden `<!-- FIGURE: src/id -->` → kép-blokk (lásd §3.2); a `src` lehet teljes fájlnév vagy stem.
- A kép-út `../2_clean_inputs/<stem>/images/...`-ra oldódik (a jegyzet a `4_wip_outputs/`-ban van).
- Hiányzó kép → `<!-- FIGURE: src/id — MISSING: <path> -->` jelölés (nem tör be vakon).
- Feloldatlan (`src/id` nincs a katalógusban / forrás nélkül többértelmű) → a placeholder marad + napló.
- `--dry-run`: csak jelentés, a jegyzetet nem írja át. Idempotens (nincs placeholder → 0 csere).

### 3.2. Ábrabeillesztés formátuma

A felirat a kép **alatt**, számozott, önálló koherens mondat (kanonikus: [Instructions §7.1](../../Instructions.md)):

```markdown
![{rövid alt}]({rel_path})
*{i}. ábra. Önálló koherens feliratmondat. [Forrás: {[N]}, {page}. o. / saját szerk.]*
```

- `{i}` = futó sorszám a feloldáskor; a **folytonos** dokumentumon belüli újraszámozást a
  [`07-3_figure_numberer.py`](07_typesetter.md) véglegesíti (a Mermaid-diagramok is e sorozat részei).
- A script a **katalógus-captiont** írja a felirat-mondatba — ez gyakran angol (MinerU). A magyar,
  önálló koherens mondatra a Claude finomítja (§3.3).

### 3.3. Manuális finomhangolás 🤖

Claude a feloldás után átnézi az ábrákat:
- A katalógus-caption magyar, önálló koherens **mondattá** írása (Instructions §7.1).
- Kontextuálisan illeszkedik-e az adott fejezethez? A rövid `alt` szöveg pontosítása.
- Feloldatlan/MISSING placeholderek kezelése (👁 napló alapján).

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Jegyzet.md` | Ábrahivatkozásokkal gazdagított verzió |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het` — `1_Jegyzet.md` + `figure_catalog.json` (v4).
- **Akció:** `python scripts/05_figure_mapper.py --week-dir test_outputs/atg/1_het --dry-run`.
- **Várt kimenet:** a már feloldott fixture-ön **0 placeholder** (idempotens no-op); szintetikus
  `<!-- FIGURE: chattopadhyay2013_paper/fig_001 -->` placeholderre a kép-blokk
  `![…](../2_clean_inputs/chattopadhyay2013_paper/images/p002_fig001.png)` + `*N. ábra. … [3], 2. o.*`.
- **Eval:** §6 ellenőrzőlista (képútvonalak léteznek, MISSING/feloldatlan naplózva).

## 6. Ellenőrzés

- [ ] Minden `<!-- FIGURE: src/id -->` feloldva, MISSING-jelölve, vagy naplózva (feloldatlan)
- [ ] Képútvonalak érvényesek (`../2_clean_inputs/...`, létező fájl)
- [ ] A feloldatlan/MISSING placeholderek száma naplózva (felhasználó dönt)
- [ ] Idempotens: feloldott jegyzeten újrafuttatás 0 cserét ad

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Ábra duplikáltan jelenik meg | a 04 két placeholdert tett ugyanahhoz | a felesleges placeholder törlése a jegyzetből |
| `feloldatlan: src/id` napló | a placeholder `src/id`-je nincs a katalógusban | a 04 placeholder vagy a katalógus forrás/id egyeztetése |
| `MISSING: <path>` jelölés | a katalógus `path`-ja nem létező fájlra mutat | MinerU (02) újrafuttatása az adott forráshoz |
| `[HIBA] nem v4 séma` | régi katalógus | 02 regen v4-re |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- [04_content_synthesizer.md](04_content_synthesizer.md) — upstream
- [06_summarize_box_injector.md](06_summarize_box_injector.md) — downstream

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
- ✅ A `05_figure_mapper.py` v4-átírva (P2.5, 8. döntés, B-10 lezárva): a régi lapos-séma + fantom
  VLM/NLM/Qfig logika helyett valódi determinisztikus `<!-- FIGURE: src/id -->` → kép-blokk feloldás
  v4-katalógus lookuppal. Idempotens, `--dry-run`-os. A magyar feliratot Claude finomítja (§3.3).

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (mint 05_visual_enricher) |
| 2026-06-03 | 1.1 | Szétválasztva: összegző dobozok → 06_summarize_box_injector; átnevezés figure_integrator-ra; TODO lezárva |
| 2026-06-06 | 1.2 | §3.2 felirat-formátum a kanonikus sémára: `i. ábra. Önálló koherens mondat. [forrás / saját szerk.]` a kép alatt (Instructions §7.1); folytonos ábraszámozás (Mermaid is). |
| 2026-06-11 | 1.3 | §Teszt pótolva (atg/1_het); §5→§10 átszámozva (sablon-konform). |
| 2026-06-12 | 2.0 | **05_figure_mapper.py v4-átírás (P2.5, 8. döntés, B-10):** valódi 🐍 placeholder-feloldás (`<!-- FIGURE: src/id -->` → kép-blokk) v4-katalógus lookuppal; CLI `--week-dir`+`--dry-run`; MISSING/feloldatlan napló; idempotens. A korábbi lapos-séma + fantom VLM/NLM/Qfig logika kivezetve. §2/§3/§5/§6/§7 a valóságra. |
