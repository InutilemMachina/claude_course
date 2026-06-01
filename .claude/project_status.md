---
title: Project Status — claude_course
type: project_status
tags: [meta]
updated: 2026-06-01
---

# Project Status — claude_course

## Aktuális fázis

**Lépésteszt-kész** — minden skill (00–10) és script megvan.
Következő: `atg` és `dft` teszteseteken végigjárni a teljes pipeline-t lépésről lépésre.

## Elkészült (✅)

- ✅ Repo struktúra (`claude_course/`)
- ✅ `CLAUDE.md`, `Instructions.md`, `pipeline.md`
- ✅ `skill_template.md`
- ✅ Skills 00–10: mind elkészült (03 + 04 sarokkövek)
- ✅ Scripts: 14 fájl portolva/átnevezve
- ✅ Scripts refactor: deduplikáció, `subn`, modul-szintű regex-ek, `resolve_week` centralizálva
- ✅ `00_init_course.py`: `WEEK_SUBDIRS` javítva (`3_raw_outputs` → `3_mindmap`)
- ✅ Meta-fájlok deduplikálva (Instructions §13, pipeline §5, §8 → referenciák)

## Backlog (🔲)

- 🔲 B-01: `atg` pipeline lépésteszt (01 → 10, megállva minden checkpointnál)
- 🔲 B-02: `dft` pipeline lépésteszt (1 könyvfejezet feldolgozása)
- 🔲 B-03: `08_ieee_renderer.py` UUID→filename patch — citációs rendszer tesztelése
- 🔲 B-04: `00_init_course.py` tesztelése az új `3_mindmap/` mappastruktúrával
- 🔲 B-05: `15_backlog_index.py` — `startswith('#')` bug javítás (section-break túl széles)
- 🔲 B-06: `11_notebook_maker` skill (Jupyter szemléltetés) — jövőbeni lépés
- 🔲 B-07: YouTube/médialink szekció az `08_question_bank`-ban — jövőbeni lépés
- 🔲 B-08: `02_mineru_pipeline.py` vs `02_source_extractor.py` — melyik az aktuális? Tisztázandó.

## Nyitott kérdések (❔)

- ❔ Q-01: DUE template DOCX portolása — `templates/` mappába szükséges-e?
- ❔ Q-02: `templates/assets2/` mappa — felesleges maradvány? Törölhető?
- ❔ Q-03: `06_heading_numberer.py` — nincs pipeline-lépés hozzárendelve; a 06 skill-be beépítendő?

## Változásjegyzék

| Dátum | Esemény |
|-------|---------|
| 2026-06-01 | Repo inicializálva; CLAUDE.md, Instructions.md, pipeline.md, 03+04 skill kész |
| 2026-06-01 | Scripts refactor: subn, modul regex, resolve_week centralizálva, 3_mindmap fix |
| 2026-06-01 | Meta-fájlok deduplikálva; project_status frissítve (B-01–B-08 lezárva) |
