---
title: OCR Lab — komparatív kutatási design
type: research_design
sprint: image_rag_OCR
status: active
created: 2026-06-05
---

# OCR Lab — komparatív kutatási design

## 1. Cél

Az `image_rag_OCR` branch nem előre választott backendre tervezi a `figure_catalog.json` `text_context` (és kapcsolódó szemantikus mezők) feltöltését, hanem **mért komparatív vizsgálat** alapján dönt. A kísérlet input-szettje fixed; minden backend ugyanazt kapja; az output külön mappákba kerül; az értékelés egy 7 dimenziós rubrika.

## 2. Hipotézisek

| H | Állítás | Hogyan dől el |
|---|---|---|
| **H1** | A Tesseract eng+hun elegendő `text_context` minőséghez a tipikus szkennelt scientific PDF-en | char count + magyar diakritika hibaarány (5 oldal × ~50 mondat) |
| **H2** | MinerU érdemi pluszt ad: (a) `02b` caption-pairing layout-aware, (b) downstream 03 mindmap struktúrája, (c) 07 typesetter képlet-LaTeX, (d) 09 question_bank tábla-MD | "added value" rubrika (5. fejezet) |
| **H3** | A Claude Read fallback önmagában (Tesseract+MinerU nélkül) képes ellátni atg/1_het szkennelt forrásait | end-to-end bootstrap próba 2 oldalon, fej-fej Tesseract-tal |
| **H4** | A 3 backend kombinációja (Tesseract default → MinerU layout-igényes oldalakon → Read fallback hibákra) Pareto-jobb mint bármelyik önmagában | döntési mátrix Pareto-frontján |

## 3. Fixed input set

15 oldal, 4 forrásból, vegyes típus:

| Forrás | Oldalak | Típus | Miért |
|---|---|---|---|
| `gravdahl1999_chapter.pdf` | 4, 5, 10, 25, 40 | Scanned scientific | Reprezentatív; magyar+angol vegyes |
| `tavakoli2004_paper.pdf` | 2, 3 | Scanned, angol | Tisztán angol baseline |
| `chattopadhyay2013_paper.pdf` | 2, 3, 4 | Born-digital kéthasábos | Olvasási sorrend teszt |
| `nagyi2013_eloadas.pdf` | 5, 12, 18, 24, 30 | Born-digital előadás, magyar | Magyar minta + várhatóan képlet |

A pontos oldalakat a `scripts/_ocr_lab_runner.py` `INPUT_MANIFEST` konstans tartalmazza.

## 4. Backend-jelöltek

| Backend | Adapter | Output formátum | Kockázat |
|---|---|---|---|
| Tesseract | `_run_tesseract` | `text/pNNN.txt` | nincs Tesseract binary; telepítendő |
| MinerU | `_run_mineru` | `<stem>/auto/{md,content_list.json,images/}` | 1–5 min/PDF, conda env |
| Marker | `_run_marker` | `<stem>.md + meta.json` | opcionális; CPU lassú |
| docTR | `_run_doctr` | `text + bbox JSON` | opcionális; magyar diakritika kérdéses |
| PyMuPDF4LLM | `_run_pymupdf4llm` | `<stem>.md` | csak born-digital |
| Claude Read | `_run_claude_read` | `text/pNNN.txt` (skill írja, runner csak méri) | manuális, session-keretes |

## 5. Értékelési mátrix

| Dimenzió | Skála | Mérés |
|---|---|---|
| Pipeline-fit | 0–3 | mennyi feldolgozás kell, hogy a `text_context` mezőbe kerüljön |
| Cross-step value (03 mindmap) | 0–3 | struktúra-felismerés (heading-ek, listák) használható-e |
| Cross-step value (04 synthesizer) | 0–3 | idézet-források minősége |
| Cross-step value (07 typesetter) | 0–3 | képlet-LaTeX, tábla-MD elérhető-e |
| Cross-step value (09 question_bank) | 0–3 | tábla-MD, kvantitatív adat |
| Time/page | sec | `time.perf_counter()` runner-szinten |
| Capability flags | bool×5 | scanned · hungarian · formula→LaTeX · table→MD · two-column-ordering |
| Output quality | 0–3 | magyar diakritika hibaarány, fals szóhatárok, sorrend |
| Install cost | 0–3 | friction (0 = pip; 3 = külön env + GB-os modellek) |
| Idempotencia | bool | újrafuttatás safe |

Összes pont: max 3 + 12 + 3 = **18 / backend** (idő és capability külön Pareto-tengelyen).

## 6. Döntési kapuk

1. **Ha H1 igaz**: `default = Tesseract`; Claude Read fallback; MinerU backlog.
2. **Ha H2 igaz**: kétutas — Tesseract a 02-ben, MinerU mint új 02c lépés downstream-nek; 02b a `text/`-ből olvas.
3. **Ha H3 igaz és H1 hamis**: Claude Read elsődleges, Tesseract opcionális.
4. **Ha H4 igaz**: 02 backend-prefer chain CLI-flaggel vagy env-varral.

## 7. Output-struktúra

```
test_outputs/_ocr_lab/atg_1_het/
  ├── input_manifest.json
  ├── tesseract/<src>/text/pNNN.txt
  ├── mineru/<src>/auto/...
  ├── marker/<src>.md
  ├── doctr/<src>/pNNN.json
  ├── claude_read/<src>/text/pNNN.txt
  ├── pymupdf4llm/<src>.md
  ├── metrics.json              # gépi, runner írja
  ├── score_template.md         # manual rubric, user/Claude tölti
  └── decision.md               # narratíva + ajánlás
```

## 8. Szándékosan kihagyva

| Eszköz | Indok |
|---|---|
| Azure/GCP/AWS OCR | API kulcs + költség + offline cél |
| Mistral OCR / GPT-4o Vision API | nincs előfizetés |
| GOT-OCR / DeepSeek-OCR / Qwen2.5-VL | GPU-igényes, scope-cap |
| OCRmyPDF | csak PDF→PDF text-layer, strukturált output nincs |

## 9. Hivatkozások

- `.claude/skills/02b_figure_enricher.md`
- `scripts/02_image_extraction.py`
- `C:\Users\lasz\claude_play\.claude\skills\03_mineru_extractor.md` (referencia minta)
- [`scripts/_ocr_lab_runner.py`](../../../../scripts/_ocr_lab_runner.py)
