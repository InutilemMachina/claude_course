---
title: Instructions
type: project_constitution
tags: [meta]
version: 1.1
updated: 2026-06-02
description: Projekt-szintű elvek, jelölések és dokumentációs szabványok.
---

# Instructions

## 1. Cél

Claude-natív tananyagfejlesztési pipeline. Nincs NLM-függőség.
A pipeline az oktató tradicionális munkafolyamatát modellezi Claude segítségével.

## 2. Alapelvek

- Az egyszerűbb megoldás előnyösebb.
- Egy fájl = egy cél.
- Minden információ csak egyetlen kanonikus helyen szerepel.
- A dokumentáció legyen rövid, világos, szabványos.
- A pipeline legyen lehetőleg automatizált, determinisztikus és minimalista.
- A részletek ne ismétlődjenek különböző fájlokban.
- **A megértés diktálja a struktúrát** — nem a fejezetek, hanem a fogalmi összefüggések.
- **A problémát a gyökérokánál kell kijavítani** — tüneti kezelés helyett az ok megszüntetése.

## 3. Dokumentációs hierarchia

A lista egyben **tekintély-sorrend**: ütközés esetén a feljebb álló dokumentum írja felül az alatta lévőt. A „mi mire való" funkcionális index: [CLAUDE.md §4](CLAUDE.md).

1. [CLAUDE.md](CLAUDE.md)
2. [Instructions.md](Instructions.md)
3. [.claude/pipeline.md](.claude/pipeline.md)
4. [.claude/project_status.md](.claude/project_status.md)
5. [.claude/skills/](.claude/skills/)
6. [scripts/](scripts/)

## 4. Jelöléstan

### 4.1. Emoji státuszok
- 🔲: TODO
- ✅: KÉSZ / OK
- ⚙️: FÉLKÉSZ / WIP
- ❌: NOK / HIÁNYZIK
- ❔: KÉRDÉS / NYITOTT
- ⚠️: VIGYÁZAT / FONTOS
- 🚦: CHECKPOINT:
    - 🔴: ÁLLJ / STOP
    - 🟡: FELTÉTELESEN TOVÁBB ENGEDVE (feltétel dokumentálásával)
    - 🟢: MEHET
- ⚡: HIBA / inkonzisztencia
- 💬: NOTE
- 💡: IDEA

Ezeket az emoji státuszokat mindig a szöveggel is ki kell egészíteni, pl.: `💡 IDEA: Az ötlet`
Te használhatod őket, de a user szinte soha nem illeszti be azokat, pl.:  `IDEA: Az ötlet`

### 4.2. Szerepkörök

| Jelölés | Szerep | Használat |
|---|---|---|
| 😎 | Felhasználó | Manuális döntés, jóváhagyás, checkpoint |
| 🤖 | Claude | Pipeline-lépések, dokumentumfrissítés |
| 🐍 | Python script | Konverzió, audit, tömeges feldolgozás |
| 💻 | Terminál / shell | Fájlműveletek, script futtatás |

## 5. Nevezéktan

### 5.1. Fájlnév konvenció

- Meta-, skill- és script-fájlok neve: angol.
- Meta- és skillfájlok tartalma: magyar (esetleges angol kifejezésekkel).
- Szóköz tilos. Alulvonás használható.
- Pipeline lépések sorszámozása stabil maradjon.

**Script számozási séma** (`scripts/` mappa):

| Típus | Séma | Példa |
|-------|------|-------|
| Egy script egy lépéshez | `NN_name.py` | `05_figure_mapper.py` |
| Több script egy lépéshez | `NN-M_name.py` | `02-1_mineru_pipeline.py` |
| Megosztott segédkönyvtár | `_name.py` | `_citations_util.py` |

- `NN`: pipeline lépés sorszáma (00–13), párhuzamos a skill-számokkal
- `M`: lépésen belüli sorrend (1, 2, ...)
- `_` prefix: nem lépés-specifikus utility — nincs hozzá külön skill

### 5.2. YAML fejléc — `tags` séma

| Scope-tag | Jelentés | Hol |
|---|---|---|
| `meta` | Projekt-infrastruktúra | `.claude/`, gyökér |
| `skill` | Pipeline-lépés protokollja | `.claude/skills/` |
| `test` | Teszt-tananyag | `test_outputs/` |
| `prod` | Éles tantárgyi tananyag | tantárgy-mappa |

## 6. Mappastruktúra

```text
claude_course/
├── CLAUDE.md
├── Instructions.md
├── .claude/
│   ├── pipeline.md
│   ├── project_status.md
│   ├── skill_template.md
│   └── skills/
│       └── NN_skill.md
├── scripts/
├── templates/
│   └── assets/
└── {tantargy}/
    └── {N_het}/
        ├── 1_raw_inputs/
        ├── 2_clean_inputs/
        ├── 3_mindmap/
        ├── 4_wip_outputs/
        └── 5_clean_outputs/
```

## 7. Vizuális gazdagítás — kötelező szabály

Minden tananyag-output "képnehéz": vizuálisan erősen támogatott.

| Réteg | Szabály |
|-------|---------|
| Navigátor mindmap | Minden output tetején link; MARP 2. diája |
| Szekciós diagram | Minden mindmap-csomóponthoz, ha ≥3 fogalom összefügg |
| Valódi ábra | MinerU-kinyert PNG; különben `<!-- FIGURE: ... -->` placeholder |
| MARP vizuális | Minden dián 1 Mermaid VAGY ábra — kötelező |

Diagram-típus döntési fa:
- Folyamat/szekvencia → `flowchart TD`
- Hierarchia/fa → `flowchart LR`
- Időbeli lefolyás → `sequenceDiagram`
- Összehasonlítás → Markdown table
- Összefoglaló → 📦 doboz (blockquote + bullets)

## 8. Hivatkozási szabály

- IEEE forrásjegyzék (`## Hivatkozásjegyzék`) kötelező MINDEN wip és clean outputban.
- Szövegbeli hivatkozás és lista is `[1]`, `[2]` … (IEEE-szabvány).
- Forrás: `1_raw_inputs/citations.json`; a listát a `_ieee_renderer.py` rendereli `type` szerint:

| `type` | IEEE-formátum |
|--------|---------------|
| `paper` / `slides` | `[N] Szerző, "Cím," *Forrás*, Év.` |
| `book` | `[N] Szerző, *Cím*, Kiadó, Év.` |
| `chapter` | `[N] Szerző, "Cím," in *Könyv*, Év.` |
| `report` | `[N] Szerző, "Cím," *Intézmény*, tech. rep., Év.` |
| `thesis` | `[N] Szerző, "Cím," Ph.D. dissertation, *Intézmény*, Év.` |
| `webpage` | `[N] Szerző, "Cím," *Forrás*. [Online]. Available: URL.` |

## 9. Szerkesztési szabályok

- Csak a szükséges részt módosítsd.
- Kerüld a teljes fájlok fölösleges újragenerálását.
- A redundancia csökkentése elsődleges szempont.

## 10. Változtatási rend

### 10.1. Soft-cap — a projekt ne bokrosodjon

Irányelv, nem szigorú szabály: **a kevesebb néha több.** Törekedj a meglévő fájlok *helyi* javítására ahelyett, hogy újabb és újabb fájlok jönnének létre.

- Először a meglévő fájlt javítsd; új fájl csak akkor, ha tényleg nem fér el sehol.
- Új skill: indokold, miért nem fér el meglévőben.
- Időnként nézd át, mi vonható össze vagy törölhető.

Tájékoztató mérce: `python scripts/_backlog_index.py`.

## 11. Visszajelzések protokoll

A szimbólumok jelentése: §4.1. A bejegyzések helye:

- **Skill-specifikus** megfigyelés/TODO/kérdés → az adott skill `§8 Visszajelzések`.
- **Projekt-szintű** → [project_status.md](.claude/project_status.md) (Backlog / Nyitott kérdések).

**Inline TODO/NOTE a szövegtörzsben TILOS** — minden bejegyzés a dedikált szekcióba kerül.

## 12. Skill-fejlesztési módszertan

**Fejlesztési ciklus:** `draft skill → lépésteszt → eval → fix → commit`

1. Skill draft a `skill_template.md` alapján (vagy `/skill-creator`)
2. Teszt: 1-2 forrás, 1 fejezet — egyszerű bemenet
3. Eval: `08_quality_check.py` + Claude Explore review
4. Gap-azonosítás: mi hiányzik, mi rossz formátumú?
5. Fix: skill `§3 Eljárás` + `§6 Hibakezelés` frissítése
6. Commit: hard-cap ellenőrzés

## 13. Nyitott pontok

→ Backlog kezelése: [project_status.md](.claude/project_status.md).
7. pont: "- Összefoglaló → 📦 doboz (blockquote + bullets)" még kitérünk rá, hogy hogyan sikerül.
[ ] Minden clean outputs-nak legyen majd egy fejléce és lábléce, de azt még meg kell tervezni