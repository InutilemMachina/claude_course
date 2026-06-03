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
1. ✅ `skill_template.md` best-practice overhaul → B-07 részben.
2. ✅ Skillek tesztje: `00_init` + `01_source_collector` + `02_image_extraction` — mind sablon-konform, verifikált → B-08 kész.
3. ✅ `03_mindmap_builder` tesztelve: skill spec javítva (v1.1), mindmap draft generálva `atg/1_het` — checkpoint vár.

**02_image_extraction — lezárt fejlesztések (2026-06-03):**
- Átnevezés: `02_source_extractor` → `02_image_extraction` (skill + script + összes hivatkozás)
- Vektoros ábra detektálás born-digital PDF-eknél (`get_drawings()` + false positive szűrő)
- Wikipedia false positive javítás (vízszintes elválasztók + apró elemek kizárva)
- `_crop_tasks.md`: caption mező hozzáadva szkennelt oldalakhoz
- Kettős tördelés kezelése: straddle oldal félbevágása PyMuPDF `show_pdf_page(clip=...)` segítségével
- PDF darabolás multi-week forráshoz (`hesselmann1983_ch01/02/03.pdf`)
- Tesztfutás: `atg/1_het` → 36 kép; `dft` 3 het → 23 kép; mind `needs_crop: true` ahol várható
- Skill + Instructions + Backlog frissítve (kettős tördelés, front matter, gyökérok-elv, TOC-alapú határdetektálás ötlet)

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
- ✅ B-08: 00, 01, 02 skillek tesztelve és sablon-konformra hozva — **kész**
- 🔲 B-09: `_ieee_renderer` — ismeretlen évnél `é.n..` dupla pont (kozmetikai); a fallback paper-formátum trailing pontját rendezni

## Ötletek — jövőbeni megfontolásra (💡)

- 💡 **Automatikus fejezethatár-detektálás kettős tördelésű PDF-eknél — TOC-alapú megközelítés:** a tartalomjegyzék oldalait OCR-ezve közvetlenül megkapjuk a fejezet → könyvoldal-szám leképezést. Ebből a PDF-oldal index és az oldalpáritás (páros/páratlan könyvoldal = bal/jobb fél) pontosan kiszámítható — anélkül, hogy minden oldalt végig kellene szkennelni. Csak 1-2 TOC oldalt kell feldolgozni. Ez a gyökér-megközelítés: a könyv saját struktúráját használjuk a struktúra feltárásához.


- 💡 **Range-alapú shared sources:** ha egy forrás több egymást követő hétre vonatkozik, de nem az összesre, a tárgy mappán belül egy tartomány-névvel ellátott shared mappa lehetne megoldás. Pl.:
  ```
  3-6_shared_sources/   ← 3.–6. hét közös forrása
  8-12_shared_sources/  ← 8.–12. hét közös forrása
  ```
  Így az 1 fájl → sok hét (minden hétre) és az 1 fájl → néhány hét (range) eset is lefedett, anélkül hogy a fájlt n-szer kellene másolni. A script keresési sorrendje: `1_raw_inputs/` → `../0_shared_sources/` → `../<tól>-<ig>_shared_sources/` (ahol a hét száma a tartományba esik).

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
| 2026-06-03 | `02_image_extraction`: átnevezés, vektoros detektálás, false positive fix, kettős tördelés kezelés, PDF-split, dft+atg tesztfutás lezárva |
| 2026-06-03 | `03_mindmap_builder`: skill spec v1.1 (input: `1_raw_inputs/` direkt PDF-olvasás, nem `2_clean_inputs/*.md`); mindmap draft: `atg/1_het/3_mindmap/mindmap.md` |
