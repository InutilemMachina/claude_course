---
title: image_rag sprint plan (Block 8 — v4 reset)
type: sprint_plan
status: active
created: 2026-06-04
---

# image_rag sprint — Block 8 (v4 schema + OCR + rewind)

## Cél

A korábbi sprintekben (v1 → v2 → v3) felhalmozódott séma-zaj és patch-történet helyett **egy clean v4 reset**: a `figure_catalog.json` egyszerű, ember-olvasható, ön-dokumentáló katalógus szemantikus retrieval-hez (image_rag).

A branch `main`-ről újra létrehozva — a korábbi 10 commit-os tanulási folyamatot a 2 commit-os clean implementáció váltja:

1. `feat(image_rag): v4 schema + OCR + 02/02b skill rewrite` — infrastruktúra
2. `feat(image_rag): atg/1_het sprint setup — captions + pilot meta` — adat

## Mit nyertünk a v4-gyel

- **11 mező / entry** (volt 15) logikus sorrendben
- **Forrás szerinti csoportosítás** (`sources["<file>"]`) — code-folding-ban össze-csukható
- **Derived `_status` mező** (`un-processed | draft | verified`) — egyetlen ránézésre tudni hol tart az entry
- **Egységes `pNNN_figNNN.png` naming** — eltűnt a 4 különböző konvenció
- **OCR-cache (`text/pNNN.txt`)** szkennelt PDF-oldalakhoz
- **Önmagát dokumentáló katalógus** (`_meta._usage.example_entry`)
- **Tiszta git history** — csak 2 commit a v4 állapothoz

## Mit ejtettünk

- `source_file` és `citation_key` denormalizált entry-mezők → parent `sources` dict-ben élnek
- `figure_label` → caption-ből derivable, drift-veszély nélkül
- `references_in_source` → bele a `text_context`-be inline-szöveg formában
- `suggested_section` → YAGNI (05_figure_mapper hozzá tudja adni amikor implementálva lesz)
- `_crop_tasks.{py,md}` round-trip → `needs_crop:true` flag a pending lista

## Implementáció

### Infrastruktúra (commit 1)

- [`scripts/02_image_extraction.py`](../../../scripts/02_image_extraction.py) — teljes rewrite v4-re
- [`.claude/skills/02_image_extraction.md`](../../skills/02_image_extraction.md) — v2.9
- [`.claude/skills/02b_figure_enricher.md`](../../skills/02b_figure_enricher.md) — új skill (v1.0)
- [`.claude/pipeline.md`](../../pipeline.md) — v1.4 (02b regisztráció)

### Adat (commit 2 — ez a folder)

- `image_rag_plan.md` (ez a fájl)
- `review_notes.md` — sprint-szintű észrevételek
- `apply_caption_fixes.py` — 28 caption + caption_verified:true a Block 1 NOTE-okból
- `apply_meta_bootstrap.py` — 8 pilot entry (chattopadhyay + tavakoli) visual_content + text_context + keywords

A stable lookup-kulcs mindenhol **(source_file, fájlnév-utolsó-komponens)** — a `fig_NNN` ID-k forráscsere esetén eltolódhatnak (lásd `review_notes.md` a v3 sprintből megtalált bug).

## Verifikáció

```powershell
# 1. Wipe + fresh regen
Remove-Item -Recurse -Force test_outputs/atg/1_het/2_clean_inputs
New-Item -ItemType Directory test_outputs/atg/1_het/2_clean_inputs

# 2. 02 fresh extraction
python scripts/02_image_extraction.py --week-dir test_outputs/atg/1_het
python scripts/02_image_extraction.py --week-dir test_outputs/atg/1_het --source gravdahl1999_chapter.pdf --pages "4,5,6,7,8,10,12,13,15,16,18,20,22,25,28,37,40"
python scripts/02_image_extraction.py --week-dir test_outputs/atg/1_het --source tavakoli2004_paper.pdf --pages "2,2,3,3,3"

# 3. Block 1 captions + Block 4 pilot meta
python .claude/sprints/image_rag/apply_caption_fixes.py
python .claude/sprints/image_rag/apply_meta_bootstrap.py

# 4. Schema validation
python -c "import json; d=json.load(open('test_outputs/atg/1_het/2_clean_inputs/figure_catalog.json',encoding='utf-8')); assert d['_meta']['schema_version']==4; assert 'example_entry' in d['_meta']['_usage']; print('OK v4')"
```

## Backlog (Block 4b és tovább)

- A maradék ~50 entry meta-bootstrap-ja (gravdahl 17 ábra, hari/nagy 8, wikipedia 3, nagyi 31)
- `05_figure_integrator` szemantikus retrieval `keywords` + `text_context` alapon

## Tanulságok a korábbi (rewind előtti) sprintekből

A rewind előtt felmerült és megőrzendő tanulságok beleépítve a v4 implementációba:

- **fig_id nem stabil forráscsere esetén** → minden apply_*.py stable-key `(source_file, fname)`-en lookupol.
- **Auto-crop nem elég szövegközi vektoros ábrákhoz** (chattopadhyay 3% margólevágás) → `needs_crop:true` a downstream-nek jelzi.
- **Sok forrásnál nincs OCR** (gravdahl, tavakoli scanned PDF) → Block 8 OCR pipeline beépítés.
- **Brand-logók nem méret-alapon szűrhetők** (DLI/3N logók MIN_AREA fölött) → 02b szemantikus jelölés `keywords:["logo"]`.
- **Caption regex túl megengedő** ("Figure N: ...\\." átszalad a következő bekezdésbe) → 02b geometriai caption-zóna (PyMuPDF blocks), nem regex.
