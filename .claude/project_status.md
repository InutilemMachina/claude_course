---
title: Project Status — claude_course
type: project_status
tags: [meta]
updated: 2026-06-01
---

# Project Status — claude_course

## Aktuális fázis

**End-to-end átfésülés folyamatban** — a belépési ponttól lépésről lépésre, `atg` + `dft` teszttárgyakon.
Kész: meta-réteg (CLAUDE/Instructions/pipeline) + `00_init` állomás.
Következő: `01_source_collector` állomás.

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
- ✅ Meta-réteg átfésülve: CLAUDE.md index, soft-cap, vertikális Mermaid, D1/D2 deduplikáció
- ✅ `00_init` állomás: `context.json` fikció → `subject_status.md` (frontmatter gépi, törzs emberi); sablon NLM-mentes; tábla auto-generált, igazított

## Backlog (🔲)

- 🔲 B-01: `atg` pipeline lépésteszt (01 → 10, megállva minden checkpointnál)
- 🔲 B-02: `dft` pipeline lépésteszt (1 könyvfejezet feldolgozása)
- 🔲 B-03: `_ieee_renderer.py` UUID→filename patch — citációs rendszer tesztelése
- ✅ B-04: `00_init_course.py` tesztelve (`3_mindmap/` + subject_status generálás) — **kész**
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
| 2026-06-02 | E2E átfésülés indul: meta-réteg rendberakva (soft-cap, vertikális diagram, dedup) |
| 2026-06-02 | `00_init`: `context` → `subject_status.md`, NLM-mentes sablon, auto-kitöltött frontmatter + igazított státusz-tábla |
