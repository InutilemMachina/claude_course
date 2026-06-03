---
title: COURSE_DEVELOPMENT_TEMPLATE.MD -- Tantárgyfejlesztési sablon
type: meta
tags: [meta, sablon]
updated: 2026-05-29
description: Új tantárgynál másolandó egységes sablon. Egyesíti a korábbi context_sablon + project_status_sablon tartalmát. Másold ide: [TantargyNeve]/.claude/context.md
---

# COURSE DEVELOPMENT -- [TantargyNeve]

_Másold a tantárgy `.claude/context.md`-jébe, és töltsd ki. Session elején Claude beolvassa._

## 1. Alapadatok
- **Tantárgy neve:**
- **Szint:** BSc / MSc / mindkettő
- **Félév:** X hetes, heti X óra
- **Célcsoport:** (szak, év)

## 2. Tematika és pipeline státusz

| Hét | Téma | NLM notebook | 01-02 | 03-04 | 05-07 | 08-10 | 11-12 | 13-14 |
|-----|------|--------------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 1 | | | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 2 | | | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 3 | | | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

_Státuszok: ❌ TODO · ⚙️ folyamatban · ✅ kész_

**Lépéscsoportok:**
- `01-02`: Forrásgyűjtés + NLM notebook setup (Prompt B)
- `03-04`: MinerU/forrás-extraktor + NLM DFS queries
- `05-07`: Assemble + Excerpt + Citations
- `08-10`: Mindmap + Képek + ToC
- `11-12`: Typesetter + 11b minőség + Prezentáció
- `13-14`: Kérdésbank + BSc filter → 5_clean_outputs

## 3. Aktuális állapot (session-szintű)
- **Utolsó kész lépés:**
- **Következő lépés:**
- **Blokkolók:** (nincs)
- **Legutóbbi döntések:** (nincs)

## 4. Célok
- BSc szint:
- MSc szint:

## 5. Stílusirányelvek
- Nyelv: magyar szöveg, kétnyelvű terminológia (pl. "termogram / thermogram")
- Jegyzet sablon: `templates/due_jegyzet_template.docx`
- Prezentáció sablon: `templates/due_prenetation_template.pptx`
- Kérdésbank: feleletválasztós A/B/C/D, SZINT:2-5

## 6. NLM notebook konfiguráció
- Notebook neve:
- Notebook URL:
- Prompt B (Custom Instructions): beállítva ❌/✅

---

# KITÖLTÖTT PÉLDA -- Műszaki Diagnosztika

> _Kitöltött minta. A saját context.md-t ennek analógiájára készítsd el._

## 1. Alapadatok
- **Tantárgy neve:** Műszaki Diagnosztika
- **Szint:** BSc + MSc (kétszintű)
- **Félév:** 14 hetes, heti 2 × 90 perc (előadás + labor)
- **Célcsoport:** Gépészmérnök BSc/MSc, 3-4. év

## 2. Tematika és pipeline státusz

| Hét | Téma | NLM notebook | 01-02 | 03-04 | 05-07 | 08-10 | 11-12 | 13-14 |
|-----|------|--------------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 1 | Hőkamerás diagnosztika | Termografia_NLM | ✅ | ✅ | ⚙️ | ❌ | ❌ | ❌ |
| 2 | Termográfia mérési módszerek | Termografia_NLM | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 3 | Rezgésdiagnosztika | Rezges_NLM | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## 3. Aktuális állapot
- **Utolsó kész lépés:** 1. hét 03-04 (MinerU + DFS)
- **Következő lépés:** 1. hét 05 assemble
- **Blokkolók:** nincs
- **Legutóbbi döntések:** Rezgésdiagnosztika külön notebookba

## 4. Célok
- BSc szint: Diagnosztikai módszerek felismerése, alapvető mérési elvek, tipikus hibamódok.
- MSc szint: Mérési adatok kiértékelése, statisztikai módszerek, rendszerszintű diagnosztika.

## 5. Stílusirányelvek
- Nyelv: magyar, kétnyelvű terminológia
- Kérdésbank: A/B/C/D, SZINT:2-5

## 6. NLM notebook konfiguráció
- Notebook neve: Termografia_NLM
- Prompt B: beállítva ✅

# Változásjegyzék
- 2026-05-29 -- M5: `context_sablon.md` + `project_status_sablon.md` egyesítve ide
- 2026-05-26 -- (context_sablon) lépésszámok 01-14 csoportokra
- 2026-05-21 -- eredeti sablonok létrehozva
