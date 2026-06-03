---
title: Project Status — claude_course
type: project_status
tags: [meta]
updated: 2026-06-01
---

# Project Status — claude_course

## Aktuális fázis

**End-to-end átfésülés folyamatban** — a belépési ponttól lépésről lépésre, `atg` + `dft` teszttárgyakon.
Kész: meta-réteg (CLAUDE/Instructions/pipeline) + `00_init` + `01_source_collector` (citáció-rendszerrel).

**Haladás (skill-tesztelési kör):**
1. ✅ `skill_template.md` best-practice overhaul (role, triggerelő description, §3 dual-mód, §5 Teszt) → B-07 részben.
2. ⚙️ Skillek tesztje a sablon szerint: ✅ `00_init` (+őszinte napló), ✅ `01_source_collector` (ideális forgatókönyv: naming + Deep Research + weblap→PDF Playwright-tel + provenance + retroaktív, valódi `atg`-n tesztelve), 🔲 `02_source_extractor` → B-08.
3. 🔲 Állomás-túra: `02_source_extractor` (MinerU, `3_raw_outputs` rejtély) — ugyanaz a lépés, mint a B-08 02-teszt.

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
- ✅ B-03: Citáció-rendszer egységesítve — egyetlen `citations.json` (`type`-alapú IEEE), `[1]` jelölés, NLM-kód törölve, `_ieee_renderer` tesztelve — **kész**
- ✅ B-04: `00_init_course.py` tesztelve (`3_mindmap/` + subject_status generálás) — **kész**
- 🔲 B-05: `11_notebook_maker` skill (Jupyter szemléltetés) — jövőbeni lépés
- 🔲 B-06: YouTube/médialink szekció az `08_question_bank`-ban — jövőbeni lépés
- 🔲 B-07: `skill_template.md` best-practice felülvizsgálata — felépítés + hol éljen (`.claude/` vs `templates/`)
- 🔲 B-08: 00, 01, 02 skillek aprólékos, end-to-end tesztelése `atg` + `dft`-n (draft→teszt→eval→fix, [Instructions §12](../Instructions.md)); a többi skill ezt követi — 00 ✅, 01 ✅, 02 hátra
- 🔲 B-09: `_ieee_renderer` — ismeretlen évnél `é.n..` dupla pont (kozmetikai); a fallback paper-formátum trailing pontját rendezni

## Nyitott kérdések (❔)

- ❔ Q-01: DUE template DOCX portolása — `templates/` mappába szükséges-e?
- ❔ Q-02: A `subject_status.md` (sablon: `subject_status_template.md`) mikor és ki által töltődik ki — különösen a §5 kérdésbank-beállítás a `08_question_bank` skill véglegesítése után? (😎 induláskor vagy 🤖 a 08 konfigjából?)
- ❔ Q-03 (B-07-hez): A `.claude/skills/` lépés-dokumentumok maradjanak protokoll-doksik, vagy váljanak valódi, hívható Claude-skillekké (`SKILL.md` + `name`/`description`)? — Mindent a maga idejében; a B-07/B-08 keretében döntjük el.

## Változásjegyzék

| Dátum | Esemény |
|-------|---------|
| 2026-06-01 | Repo inicializálva; CLAUDE.md, Instructions.md, pipeline.md, 03+04 skill kész |
| 2026-06-01 | Scripts refactor: subn, modul regex, resolve_week centralizálva, 3_mindmap fix |
| 2026-06-01 | Meta-fájlok deduplikálva; "egy utasítás egy helyen" elv érvényesítve |
| 2026-06-01 | Script számozási séma: NN-M_name séma bevezetve, fájlok átnevezve |
| 2026-06-02 | E2E átfésülés indul: meta-réteg rendberakva (soft-cap, vertikális diagram, dedup) |
| 2026-06-02 | `00_init`: `context` → `subject_status.md`, NLM-mentes sablon, auto-kitöltött frontmatter + igazított státusz-tábla |
| 2026-06-02 | Citáció-rendszer: egyetlen `citations.json` (`type`-alapú), `[1]` jelölés, halott NLM-kód törölve `_citations_util`-ból, `_ieee_renderer` út+mező javítva és tesztelve |
