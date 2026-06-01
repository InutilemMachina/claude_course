---
title: Instructions
type: project_constitution
tags: [meta]
version: 1.0
updated: 2026-06-01
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
- Az agent-ek száma legyen a lehető legkisebb.
- A részletek ne ismétlődjenek különböző fájlokban.
- **A megértés diktálja a struktúrát** — nem a fejezetek, hanem a fogalmi összefüggések.

## 3. Dokumentációs hierarchia

1. [CLAUDE.md](CLAUDE.md) — belépési pont és index
2. [Instructions.md](Instructions.md) — stabil projekt-alkotmány
3. [.claude/pipeline.md](.claude/pipeline.md) — futási gráf és lépések
4. [.claude/project_status.md](.claude/project_status.md) — aktuális iterációs állapot + Backlog
5. [.claude/skills/](.claude/skills/) — egy-egy lokális skill (§6: hibakezelés, §8: visszajelzések)
6. [scripts/](scripts/) — végrehajtó automatizmusok

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

### 4.2. Szerepkörök

| Jelölés | Szerep | Használat |
|---|---|---|
| 😎 | Felhasználó | Manuális döntés, jóváhagyás, checkpoint |
| 🤖 | Claude | Pipeline-lépések, dokumentumfrissítés |
| 🐍 | Python script | Konverzió, audit, tömeges feldolgozás |
| 💻 | Terminál / shell | Fájlműveletek, script futtatás |

## 5. Nevezéktan

### 5.1. Fájlnév konvenció

- Meta- és skillfájlok neve: angol.
- Meta- és skillfájlok nyelve: magyar (esetleges angol kifejezésekkel).
- Szóköz tilos. Alulvonás használható.
- Pipeline lépések sorszámozása stabil maradjon.

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
- Formátum: `[1] Szerző. *Cím.* Kiadó, Év.` vagy `[1] Szerző. "Cím." URL (elérve: dátum).`
- Hivatkozás a szövegben: `[S1]`, `[S2]` stb.

## 9. Szerkesztési szabályok

- Csak a szükséges részt módosítsd.
- Kerüld a teljes fájlok fölösleges újragenerálását.
- A redundancia csökkentése elsődleges szempont.

## 10. Változtatási rend

### 10.1. Hard-cap szabály — ne nőjön a komplexitás

**Minden commit net-flat vagy csökkenjen.** Új hozzáadáshoz ekvivalens komplexitás-csökkentés tartozik.
Mérce: `python scripts/15_backlog_index.py` output — **nem nőhet**.

- Új TODO a `§8 Visszajelzések`-be → zárj le egy régit ugyanott.
- Új script → vagy törölj egyet, vagy mergelj kettőt.
- Új skill → indokold miért nem fér el meglévőben.

## 11. Visszajelzések protokoll

| Jelölés | Típus | Mikor |
|---|---|---|
| 🔲 TODO | Elvégzendő feladat | Ha a módosítás nem azonnali |
| 💬 NOTE | Megfigyelés, tapasztalat | Ha a jövőbeni futtatáshoz releváns |
| ❔ QUESTION | Nyitott kérdés | Ha döntés szükséges |
| ⚠️ WARNING | Fontos korlát | Ha figyelmen kívül hagyva hibát okoz |

**Inline TODO/NOTE a szövegtörzsben TILOS** — minden bejegyzés a saját fájl dedikált szekciójába kerül.

## 12. Skill-fejlesztési módszertan

**Fejlesztési ciklus:** `draft skill → lépésteszt → eval → fix → commit`

1. Skill draft a `skill_template.md` alapján (vagy `/skill-creator`)
2. Teszt: 1-2 forrás, 1 fejezet — egyszerű bemenet
3. Eval: `07_quality_check.py` + Claude Explore review
4. Gap-azonosítás: mi hiányzik, mi rossz formátumú?
5. Fix: skill `§3 Eljárás` + `§6 Hibakezelés` frissítése
6. Commit: hard-cap ellenőrzés

## 13. Nyitott pontok

→ Backlog kezelése: [project_status.md](.claude/project_status.md).
