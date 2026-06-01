---
title: Project Status — claude_course
type: project_status
tags: [meta]
updated: 2026-06-01
---

# Project Status — claude_course

## Aktuális fázis

**Inicializálás** — repo felépítés, meta-fájlok, sarokkő skill-ek kész.
Következő: skill-ek iteratív fejlesztése + lépésteszt.

## Elkészült (✅)

- ✅ Repo struktúra (`claude_course/`)
- ✅ `CLAUDE.md`, `Instructions.md`, `pipeline.md`
- ✅ `skill_template.md`
- ✅ `03_mindmap_builder.md` (sarokkő skill)
- ✅ `04_content_synthesizer.md` (sarokkő skill)
- ✅ Scripts: 14 fájl portolva/átnevezve

## Folyamatban (⚙️)

- ⚙️ Skill-ek: 00, 01, 02, 05, 06, 07, 08, 09, 10 — stub szinten szükségesek

## Backlog (🔲)

- 🔲 B-01: `01_source_collector.md` skill megírása
- 🔲 B-02: `02_source_extractor.md` skill megírása
- 🔲 B-03: `05_visual_enricher.md` skill megírása
- 🔲 B-04: `06_typesetter.md` skill megírása (06_typesetter.py már portolva)
- 🔲 B-05: `07_quality_reviewer.md` skill megírása
- 🔲 B-06: `08_question_bank.md` skill megírása
- 🔲 B-07: `09_presentation_maker.md` skill megírása
- 🔲 B-08: `10_bsc_export.md` skill megírása
- 🔲 B-09: `08_ieee_renderer.py` UUID→filename patch (citations rendszer)
- 🔲 B-10: `00_init_course.py` tesztelése az új mappastruktúrával (`3_mindmap/` mappa)
- 🔲 B-11: Lépésteszt TC1 (surge/stall/choke) — 03+04 skill-ekkel
- 🔲 B-12: Lépésteszt TC2 (Randall könyv) — 03+04 skill-ekkel
- 🔲 B-13: `11_notebook_maker` skill (Jupyter szemléltetés) — jövőbeni lépés

## Nyitott kérdések (❔)

- ❔ Q-01: DUE template DOCX portolása — `templates/` mappába szükséges-e?
- ❔ Q-02: `figure_catalog.json` formátuma változott-e? (claude_play 09_figure_mapper.py kompatibilitás)

## Változásjegyzék

| Dátum | Esemény |
|-------|---------|
| 2026-06-01 | Repo inicializálva; CLAUDE.md, Instructions.md, pipeline.md, 03+04 skill kész |
