---
title: OCR Lab — döntés
type: decision
sprint: image_rag_OCR
status: draft
date: 2026-06-05
---

# OCR Lab — Döntés és ajánlás

## TL;DR

**3-rétegű stratégia** lép a `02 → 02b` pipeline-ba:

| Réteg | Backend | Mit szolgál ki | Mikor |
|---|---|---|---|
| **L1 — primary OCR** | **Tesseract** (`text/pNNN.txt`) | 02b `text_context` mező | szkennelt oldalakra `_try_ocr_page` (már az 02 script része) |
| **L2 — born-digital primary** | **PyMuPDF4LLM** (forrás-szintű `.md`) | 02b `text_context` mező (pontosabb mint Tesseract render-újra-OCR) | text-stream van a PDF-ben |
| **L3 — layout/formula/cross-step** | **MinerU** (`<stem>/auto/{md,content_list.json,images}`) | 03 mindmap, 07 typesetter, 09 question_bank, 05 figure_integrator | **új 02c lépés**, opcionális, source-onként |
| **Fallback** | **Claude Read** (session-szintű) | `text/pNNN.txt` upsert | csak akkor, ha Tesseract magyar diakritikája gyenge ÉS nincs MinerU |

A `02b_figure_enricher` skill **továbbra is** a `text/pNNN.txt`-ből olvas `text_context`-hez (kompatibilis), de jelölhet preference-t MinerU `_content_list.json`-re ha létezik.

## Pareto-front (output minőség × install cost × time × cross-step value)

```
  cross-step value (max 12)
   12 |
   11 |                                   MinerU ●        ● Claude Read
   10 |
    8 |
    7 |              PyMuPDF4LLM ●
    6 |
    4 |
    3 |     Tesseract ●
    2 |
    1 +-------------------------------------------------- install cost
        0           1           2           3
        (claude_read,         (tesseract)  (mineru)
         pymupdf4llm)
```

- **PyMuPDF4LLM**: Pareto-optimal `(install=0, value=7)` born-digitalra
- **MinerU**: Pareto-optimal `(install=3, value=11)` magas érték layout-igényes use-case-ekre
- **Claude Read**: Pareto-optimal `(install=0, value=11, quality=3)` de skálázhatatlan
- **Tesseract**: dominált hu-magyar oldalakon (0.59 char ratio), versenyképes en-angol szkenneltre

## Hipotézisek értékelése

| H | Eredmény |
|---|---|
| **H1** — Tesseract elég `text_context`-hez | **RÉSZBEN** — angol scanned: igen (0.94 char ratio); magyar slides: **NEM** (0.59 char ratio + diakritika hibás) |
| **H2** — MinerU érdemi plusz downstream-nek | **IGEN** — `$50\%$` LaTeX formula, `Fig. 1.` képpárosítás, `# Heading` detection mért a tavakoli p2-3 sample-en. Cross-step Σ=11 vs. Tesseract Σ=3 |
| **H3** — Claude Read önmagában elég atg/1_het-re | **IGEN minőségileg** (15/15 oldal hibátlan magyar diakritika), **NEM batch-méretre** (manuális, ~30s/page) |
| **H4** — hibrid Pareto-jobb | **IGEN** — minden forrás-típusra megvan az ideális backend; a 3-rétegű stratégia ezt fedi le |

## Mérési alap

- **15 oldal × 4 forrás** komparatív futtatás: `test_outputs/_ocr_lab/atg_1_het/{tesseract,mineru,pymupdf4llm,claude_read}/`
- **`metrics.json`**: backend-onként times_per_page + char_counts + errors + availability
- **`score_template.md`**: per-backend manual rubric 7+ dimenzión
- **MinerU pilot (tavakoli p2-3)**: konkrét sample látott formula-LaTeX, képpárosítás, heading-detection

## Implementációs következmények (D fázis)

1. **02 script — változatlan.** A `_try_ocr_page` Tesseract-tal aktiválódik (binary + hun.traineddata most már megvan a gépen).
2. **02b skill (v1.0 → v1.1)** §3.1 új sub-lépés:
   - Born-digital forrásnál: ha PyMuPDF4LLM `.md` létezik a forrás mellett → használd az `text_context` elsődleges forrásaként (text-stream pontosabb mint a 02 `_try_ocr_page` early-return).
   - Ha MinerU output `<stem>/auto/_content_list.json` létezik → `caption` és `visual_content` preferenciát kap a MinerU caption-pairingjéből.
   - Ha Tesseract output magyar oldalon char count < 80% PyMuPDF text-stream-jéhez képest → Claude Read fallback (Read PNG → Write text).
3. **Új 02c_mineru_layout.py** (opcionális lépés a pipeline-ban):
   - `python scripts/02c_mineru_layout.py --week-dir <het> [--source X.pdf]`
   - `conda run -n mineru` wrap + `-l` lang detection (manifest-szerű mapping a per-forrás nyelvre)
   - Output flat-elve: `2_clean_inputs/<stem>/mineru/{md,content_list.json,images}` (a MinerU `<stem>/auto/` dupla-szintje `shutil.move`-val felszámolva)
4. **pipeline.md** v1.4 → v1.5: 02c regisztrálva, függőség `02 → 02c → 02b`.
5. **`apply_meta_bootstrap_full.py`** (E fázis) idempotens, preferencia chain-t követi: MinerU > PyMuPDF4LLM/Claude-Read > Tesseract.

## Backlogba

- Marker pilot (most kihagyva — MinerU már bizonyított)
- docTR pilot
- OCR-bbox alapú crop-finomítás
- MinerU vlm-auto-engine backend (GPU)
- `02c` automatikus indítása a 02 után — most explicit user-aktus

## Update — háttér MinerU futás végeztével (2026-06-05 ~14:55)

A teljes 4-forrás MinerU futás (mind a 4 PDF, valid `-s`/`-e` range-szel) lefutott. Eredmények:

| Forrás | MinerU output méret | Időtartam | Magyar diakritika |
|---|---:|---:|:---:|
| chattopadhyay2013_paper (3 oldal, en) | 1.6 MB | gyors | n/a |
| tavakoli2004_paper (2 oldal, scanned en) | 1.4 MB | gyors | n/a |
| gravdahl1999_chapter (37 oldal, scanned en) | 24 MB | ~10 min | n/a |
| nagyi2013_eloadas (22 oldal, born-digital **hu**) | 19 MB | ~5 min | **TÖKÉLETES** |

**Mért minta** nagyi/MinerU markdown elejéből:

> # Centrifugális szivattyúk
> A centrifugális szivattyúk esetén a lapát-elhaladási frekvenciát PV-vel jelöljük (Pump Vane), ami a lapátszám és a forgási frekvencia szorzatával egyenlő. […] Az áramlási csatorna hirtelen meghajlása, ami az áramlás útját zavarja, esetleg ha a szivattyú, vagy ventilátor rosszul pozícionált a házában. […] Ezek a párabuborékok eljutnak olyan helyre, ahol a nyomás nagyobb, mint ami a gőzfázis jelenlétét lehetővé teszi, és a buborékok összeroppannak.

Egyetlen apró hiba: második heading-ben „Cenrtifugális" (typo). A többi diakritika (ő, ű, é, á, í, ó, ú) hibátlan. Heading-szintek (`# … `) felismerve, képek külön JPG-ben image-ref-ekkel.

**Score-frissítés:** a MinerU `-l latin` magyar minőség **2 → 3** (kiváló). Cross-step value **11 → 12 (max)**.

**Következmény a chain-re:** ha MinerU futott (`02c_mineru_layout`), akkor MAGYAR oldalra is preferenciát kap **L1 minden esetben** — nem csak layout-igényes oldalra. A `text_context` minősége egyenértékű vagy jobb mint a Claude Read fallbacké, és batch-szerűen, deterministic módon. Ez a 4-rétegű chain optimalizálható:
```
L1 = MinerU (ha létezik <stem>/mineru/)
L2 = PyMuPDF4LLM (gyors text-stream, born-digital)
L3 = Tesseract (csak ha sem L1, sem L2 nincs)
L4 = Claude Read fallback (utolsó, kézi)
```

## Mit nem mértünk meg, de tudni érdemes

- **MinerU teljes idő atg/1_het 4 forrásra**: ~15-20 perc batch (mért, nem becsült). Egyszeri befektetés/hét, érdemes a heti pipeline részévé tenni.
- **Marker / docTR** explicit benchmark — backlogba (MinerU már bizonyítottan elég).

## Linkek

- `research_design.md` — eredeti hipotézisek + design
- `score_template.md` — kitöltött rubrika
- `../../../test_outputs/_ocr_lab/atg_1_het/metrics.json` — gépi metrikák
- `../../../scripts/_ocr_lab_runner.py` — runner script
