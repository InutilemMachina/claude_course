---
title: Project Status — claude_course
type: project_status
tags: [meta]
updated: 2026-06-01
---

# Project Status — claude_course

## Aktuális fázis

**Lépésteszt-kész** — minden skill (00–10) és script megvan, számozás rendezett.
Következő: `atg` és `dft` teszteseteken végigjárni a teljes pipeline-t lépésről lépésre.

## Elkészült (✅)

- ✅ Repo struktúra (`claude_course/`)
- ✅ `CLAUDE.md`, `Instructions.md`, `pipeline.md`
- ✅ `skill_template.md`
- ✅ Skills 00–10: mind elkészült (03 + 04 sarokkövek)
- ✅ Scripts: portolva, refaktorálva, átnevezve az `NN-M_name` sémára
- ✅ Script számozási séma alkotmányosan rögzítve (`Instructions.md §5.1`)
- ✅ Meta-fájlok deduplikálva — "egy utasítás egy helyen" elv érvényesítve
- ✅ `00_init_course.py`: `WEEK_SUBDIRS` javítva (`3_raw_outputs` → `3_mindmap`)
- ✅ `15_backlog_index.py` → `_backlog_index.py` (utility, nem pipeline-lépés)
- ✅ `08_ieee_renderer.py` → `_ieee_renderer.py` (utility, nem lépés-specifikus)
- ✅ `startswith('#')` bug javítva a `_backlog_index.py`-ban

## Backlog (🔲)

- 🔲 B-01: `atg` pipeline lépésteszt (01 → 10, megállva minden checkpointnál)
- 🔲 B-02: `dft` pipeline lépésteszt (1 könyvfejezet feldolgozása)
- 🔲 B-03: `_ieee_renderer.py` UUID→filename patch — citációs rendszer tesztelése
- 🔲 B-04: `00_init_course.py` tesztelése az új `3_mindmap/` mappastruktúrával
- 🔲 B-05: `11_notebook_maker` skill (Jupyter szemléltetés) — jövőbeni lépés
- 🔲 B-06: YouTube/médialink szekció az `08_question_bank`-ban — jövőbeni lépés

## Nyitott kérdések (❔)

- ❔ Q-01: DUE template DOCX portolása — `templates/` mappába szükséges-e?

## Változásjegyzék

| Dátum | Esemény |
|-------|---------|
| 2026-06-01 | Repo inicializálva; CLAUDE.md, Instructions.md, pipeline.md, 03+04 skill kész |
| 2026-06-01 | Scripts refactor: subn, modul regex, resolve_week centralizálva, 3_mindmap fix |
| 2026-06-01 | Meta-fájlok deduplikálva; "egy utasítás egy helyen" elv érvényesítve |
| 2026-06-01 | Script számozási séma: NN-M_name séma bevezetve, fájlok átnevezve |
