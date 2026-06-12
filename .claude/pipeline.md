---
title: Pipeline.md — claude_course
type: meta
status: active
version: 3.0
updated: 2026-06-12
description: Claude-natív tananyagfejlesztési pipeline, NotebookLM mentesen.
---

# PIPELINE.MD — claude_course

## 0. Hogyan működik az egész? (amatőr-áttekintés)

Ez **nem** egy „indítsd el és gyere vissza a késztermékért" batch-folyamat. **Interaktív,
ember-felügyelt szerzői hurok**: a 😎 (te, az oktató) irányítasz, a 🤖 (Claude) végzi a
szellemi gyártás zömét, a 🐍 (scriptek) a determinisztikus, megbízható átalakításokat.

A fonal egyszerű nyelven, egy héten belül:

1. **Beállítás** (00–01): megadod a tárgyat/heteket; forrásokat gyűjtesz (PDF/URL/PPTX).
2. **Feldolgozás** (02–02b): a MinerU kinyeri a képeket + felépíti az ábra-katalógust; Claude
   leírja, mit ábrázolnak a képek.
3. **🚦 GATE 1 — elmetérkép** (03): Claude megérti az anyagot és **elmetérképet** rajzol. **Te
   birtoklod**: eldöntöd a szkópot és a mélységet. Ez a legfontosabb sarokkő.
4. **Megírás** (04–06): a mindmap vezérletével Claude megírja a jegyzetet, beilleszti az ábrákat
   és az összegző dobozokat.
5. **Tördelés** (07): terminológia-egységesítés + determinisztikus fejezet/ábra-számozás.
6. **🚦 GATE 2 — publikálhatóság** (08): minőség-ellenőrzés. **Te döntesz**: publikálható, vagy
   célzott revíziót kérsz (vissza 04-re, új forrásnál 01-re).
7. **Kimenetek** (09–11): kérdésbank, prezentáció (PPTX), camera-ready DOCX — a véglegesített
   wip **tiszta konverziója** a `6_clean_outputs/`-ba.
8. **Gazdagítás** (12–13, opcionális): te koncepciókat jelölsz ki, Claude videót/notebookot rendel
   hozzá; ezek **overlay-ként** a `5_asset_outputs/` regiszterbe kerülnek (lásd 12/13 §3.2).

### A te szerepeid (human-in-the-loop)

| 😎-szerep | Hol | Mit csinálsz |
|-----------|-----|--------------|
| **Setup** | 00, 01 | tárgy/hetek/célok; forrás-válogatás (több jelölt), saját fájl, zárt hozzáférés letöltése |
| **Spot-check** | 02/02b, 04, 05, 06, 07 | ránézel az eredményre — könnyű felügyelet, nem gate |
| **🚦 GATE 1 — mindmap** | 03 után | **birtoklod az elmetérképet**: szkóp, mélység, mit metsz |
| **🚦 GATE 2 — publikálhatóság** | 08 után | publikálsz/visszaküldesz; célzott revíziót injektálsz → hurok 04-re |
| **Kijelölő** | 12, 13 | rámutatsz koncepciókra/ábrákra; a 🤖 gyárt; **nem automatikus** |

A három állapot (EREDETI → CÉL → VALÓS) és a CÉL-lefedettség a [§2.1 Vizualizáció](#21-vizualizáció--eredeti--cél--valós)-ban; a két gate a [§3 Checkpointok](#3-checkpointok)-ban.

## 1. A tradicionális oktató → Claude leképezés

| Oktató | Claude-pipeline |
|--------|-----------------|
| Célcsoport, tanterv | `00_init` — subject_status.md |
| Anyaggyűjtés | `01_source_collector` |
| Olvas → megért → szintetizál | `02_image_extraction` + `03_mindmap_builder` |
| **Elmetérkép** | **03 kimenet: mindmap** (😎 revideálja) |
| Word: ír, hivatkozik, képek, egyenletek, táblázatok, diagrammok | `04_content_synthesizer` + `05_figure_integrator` + `06_summarize_box_injector` |
| Word → PowerPoint | `10_presentation_maker` |
| Vizsgakérdések (Moodle MCQ) | `09_question_bank` |
| Youtube search | `12_youtube_finder` (😎-kijelölt overlay) |
| Jupyter notebook | `13_jupyter_catalogizer` (😎-kijelölt overlay) |

**Kulcselv:** → [Instructions.md §2](../Instructions.md). A 12/13 **nem** automatikus: a 😎 jelöl ki
koncepciókat, a 🤖 gyárt, az eredmény overlay-ként a `5_asset_outputs/` regiszterbe kerül (a wip
csak stabil horgonyt kap), a `6_clean_outputs` ebből + a wip-ből **újrakonvertál** (lásd §0, 12/13 §3.2).

## 2. Lépések és IO

| Input | Felelős | Lépés | Automatizáltság | Output |
|:------|:--------|:------|:----------------|:-------|
| Célcsoport, hetek, tantárgy | 😎 | [`00_init`](skills/00_init.md) — `00_init_course.py` | 🐍 | `subject_status.md` + mappák |
| URL-ek, PDF-ek, PPTX-ek | 😎+🤖 | [`01_source_collector`](skills/01_source_collector.md) | 🤖+😎 | `1_raw_inputs/` + `citations.json` |
| `1_raw_inputs/` + `citations.json` | 🐍 | [`02_image_extraction`](skills/02_image_extraction.md) — `02_mineru_to_catalog.py` (MinerU, conda `mineru` env); caption+text_context+keywords-draft gépi | 🐍 | `2_clean_inputs/` képek + `figure_catalog.json` (v4) |
| `2_clean_inputs/figure_catalog.json` | 🤖 | [`02b_figure_enricher`](skills/02b_figure_enricher.md) — `visual_content` + `keywords` finomítás (csak ez marad Claude-ra) | 🤖 | ugyanaz, `visual_content` + végleges `keywords` kitöltve |
| `2_clean_inputs/` | 🤖 | [`03_mindmap_builder`](skills/03_mindmap_builder.md) — olvas, szintetizál | 🤖 🚦😎 | `3_mindmap/mindmap.md` (flowchart LR) |
| `3_mindmap/mindmap.md` | 🤖 | [`04_content_synthesizer`](skills/04_content_synthesizer.md) — mindmap-vezérelt szintézis | 🤖 🚦 | `4_wip_outputs/N_Jegyzet.md` |
| `4_wip_outputs/N_Jegyzet.md` (FIGURE-placeholderek) | 🤖+🐍 | [`05_figure_integrator`](skills/05_figure_integrator.md) — `05_figure_mapper.py` placeholder-feloldás (v4 lookup) + Claude felirat-finomítás | 🤖+🐍 | `4_wip_outputs/N_Jegyzet.md` (beillesztett ábrák) |
| `4_wip_outputs/N_Jegyzet.md` | 🤖 | [`06_summarize_box_injector`](skills/06_summarize_box_injector.md) — összegző dobozok | 🤖 | `4_wip_outputs/N_Jegyzet.md` (összegzők) |
| `4_wip_outputs/N_Jegyzet.md` | 🤖+🐍 | [`07_typesetter`](skills/07_typesetter.md) — Claude terminológia-pass + `07-2_heading_numberer.py` + `07-3_figure_numberer.py` | 🤖+🐍 | `4_wip_outputs/N_Jegyzet.md` (egységesítés + fejezet/ábra-számozás) |
| `4_wip_outputs/N_Jegyzet.md` | 🐍+🤖 | [`08_quality_reviewer`](skills/08_quality_reviewer.md) — `08_quality_check.py` | 🐍+🤖 🚦😎 | `4_wip_outputs/N_Review.md` |
| `4_wip_outputs/N_Jegyzet.md` | 🤖 | [`09_question_bank`](skills/09_question_bank.md) — mindmap-alapú MCQ | 🤖 | `4_wip_outputs/N_Kerdesbank.md` |
| `4_wip_outputs/N_Jegyzet.md` | 🤖+🐍 | [`10_presentation_maker`](skills/10_presentation_maker.md) — tartalmi Mermaid→PNG (`10-1_mermaid_render.py`) + navigáció-injektálás (`10-2_nav_inject.py`) + `.potx`-natív PPTX (`10_pptx_gyarto.py --variant`). Két variáns: **default** (fejléc-breadcrumb) / **mindmap** (oldalsáv-TOC), közös navigációs modellből (`_nav_util.py`); a PPTX a `.potx` mesterekből (Garamond cím + Aptos body) készül, valódi táblákkal és **natív OMML-egyenletekkel** (Cambria Math, `_omml.py` — nem kép) | 🤖+🐍 | `4_wip_outputs/N_Prezentacio.md` (+ `_default`/`_mindmap`) + `6_clean_outputs/N_Prezentacio.pptx` (+ `_mindmap`) |
| `4_wip_outputs/N_Jegyzet.md` | 🐍 | [`11_docx_export`](skills/11_docx_export.md) — pandoc (`11-2`) | 🐍 | `6_clean_outputs/N_Jegyzet.docx` |
| `4_wip_outputs/N_Jegyzet.md` (+ `N_Prezentacio.md`) | 🤖+😎 | [`12_youtube_finder`](skills/12_youtube_finder.md) — videó-overlay (😎-kijelölt) | 🤖+😎 | `5_asset_outputs/enrichment_register.md` (📎▶) + `<!-- ENRICH: v* -->` horgony |
| `4_wip_outputs/N_Jegyzet.md` (+ `N_Prezentacio.md`) | 🤖+😎 | [`13_jupyter_catalogizer`](skills/13_jupyter_catalogizer.md) — notebook-overlay (😎-kijelölt) | 🤖+😎 | `5_asset_outputs/enrichment_register.md` (📎🧪) + `<!-- ENRICH: nb* -->` horgony |

> **VALÓS-státusz** (a fenti „Automatizáltság" a TERVET mutatja; ez a tényleges script-lét): `🐍✅`
> valódi futó script — **00, 02, 05, 07-2/07-3, 08, 10-1/10-2/10_pptx, 11-2**. `🤖` Claude-kézi (nincs
> script) — **02b, 03, 04, 06, 09**. `😎+🤖` kézi — **01, 12, 13**. `⏳` tervezett — **09b** (Moodle, a
> script még nem létezik). A teljes őszinte folyam: §2.1.c VALÓS.

## 2.1 Vizualizáció — EREDETI → CÉL → VALÓS

A folyamatot **három állapotban** mutatjuk, hogy a terv–valóság ív (és a rés) látható legyen
(őszinte napló, Instructions §2):

- **EREDETI** — az eredeti, naiv elképzelés (lineáris, minden „automatikus").
- **CÉL** — amit megterveztünk (a `plan_3` cél-gráfja: MinerU-only, szint-semleges, overlay+regiszter, camera-ready).
- **VALÓS** — ami MOST ténylegesen megépült, őszinte végrehajtó-jelöléssel.

### 2.1.a EREDETI — eredeti elképzelés

A kiinduló feltevés: lineáris lánc, minden lépés „automatikus", a kimenetek „párhuzamosak", a 😎
csak 2 gate-en avatkozik be.

```mermaid
flowchart LR
    A["00 init"] --> B["01 sources"] --> C["02 (+02b)"] --> G1{"03 🚦"} --> D["04"] --> E["05"] --> F["06"] --> H["07"] --> G2{"08 🚦"}
    G2 --> O["09 ‖ 10 ‖ 11 ‖ 12 ‖ 13<br>(párhuzamos kimenetek)"]
```

### 2.1.b CÉL — a megtervezett cél (plan_3)

Ezt céloztuk meg: egyetlen MinerU-út, szint-semleges metszés a GATE 1-en, valódi 05-script, 07-2/07-3,
GATE 2 revízió-hurokkal, camera-ready `6_clean`, és a 12/13 overlay+regiszter (nincs 6-fájlos visszaírás).

```mermaid
flowchart TD
    T00["00 init 🐍<br>→ 6 almappa"] --> T01["01 sources 😎+🤖"]
    T01 --> T02["02 extract 🐍<br>MinerU-ONLY (1 út)"]
    T02 --> T02b["02b enrich 🤖<br>(minimális)"]
    T02b --> TG1{"🚦 GATE 1 😎<br>szkóp+mélység<br>(szint-semleges)"}
    TG1 --> T04["04 synthesize 🤖<br>(MSc nélkül)"]
    T04 --> T05["05 figures 🤖+🐍<br>(valódi script)"]
    T05 --> T06["06 summaries 🤖"] --> T07["07 typeset 🐍<br>07-2 + 07-3"]
    T07 --> TG2{"🚦 GATE 2 😎<br>publikál? + revízió"}
    TG2 -->|revízió| T04
    TG2 -->|🟢| TCONV["tiszta determinisztikus<br>konverzió"]
    TCONV --> TOUT
    subgraph TOUT["6_clean_outputs — szint-semleges"]
      U09["09 q_bank 🤖<br>(09b Moodle planned)"]
      U10["10 prezi 🤖+🐍<br>(2 variáns)"]
      U11["11 export 🐍<br>tiszta DOCX"]
    end
    TG2 -.->|😎 kijelöl| TENR
    subgraph TENR["5_asset_outputs — overlay + regiszter"]
      U12["12 youtube 😎+🤖"]
      U13["13 jupyter 😎+🤖"]
    end
    TENR -.->|stabil link a regiszterből| TCONV
```

### 2.1.c VALÓS — jelenlegi valóság

A **fő, őszinte** gráf. Jelmagyarázat: `🐍✅` valódi futó script · `🤖` Claude-kézi (nincs script) ·
`😎` emberi · `⏳` tervezett/backlog. A folyam **ciklikus, ember-a-hurokban**.

```mermaid
flowchart TD
    S00["00 init<br>🐍✅ 00_init_course.py"] --> S01["01 sources<br>😎+🤖 — NINCS script<br>(kézi + WebSearch + Edge→PDF)"]
    S01 --> S02["02 extract<br>🐍✅ 02_mineru_to_catalog.py<br>(conda mineru env)"]
    S02 --> S02b["02b enrich<br>🤖 — NINCS script (Read image)"]
    S02b --> S03["03 mindmap<br>🤖 — NINCS script"]
    S03 --> G1{"🚦 GATE 1 — 😎<br>birtokolja a mindmapet · STOP"}
    G1 --> S04["04 synthesize<br>🤖 — NINCS script"]
    S04 --> S05["05 figures<br>🤖 + 🐍✅ 05_figure_mapper.py"]
    S05 --> S06["06 summaries<br>🤖 — NINCS script"]
    S06 --> S07["07 typeset<br>🤖 terminológia + 🐍✅ 07-2/07-3"]
    S07 --> S08["08 quality<br>🐍✅ 08_quality_check.py + 🤖 review"]
    S08 --> G2{"🚦 GATE 2 — 😎<br>publikál? · STOP"}
    G2 -->|"revízió: meglévő forrás"| S04
    G2 -->|"revízió: új forrás"| S01
    G2 -->|"🟢 finalize wip"| CONV["tiszta konverzió"]
    CONV --> OUT
    subgraph OUT["6_clean_outputs (a gate után, egymástól függetlenül)"]
      O09["09 q_bank 🤖<br>09b Moodle ⏳ planned"]
      O10["10 prezi 🤖+🐍✅<br>(2 variáns)"]
      O11["11 export 🐍✅<br>pandoc DOCX"]
    end
    G2 -.->|"😎 kijelöl (opcionális)"| ENR
    subgraph ENR["5_asset_outputs — overlay (😎-vezérelt, kézi)"]
      O12["12 youtube 😎+🤖"]
      O13["13 jupyter 😎+🤖"]
    end
    ENR -.->|"regiszter + ENRICH-horgony<br>újrakonverzió: ⏳ B-26 (ma kézi)"| CONV
```

**Spot-check** (😎 ránéz, **nem** gate): 02/02b, 04, 05, 06, 07 — a folyam nem áll meg, csak a 2 🚦-gate-nél (03, 08).

### 2.1.d Lefedettség — a VALÓS lefedi a CÉL-t?

| CÉL-elem (plan_3) | VALÓS | hol |
|---|---|---|
| 02 MinerU-only (fallback törölve) | ✅ | P2.3 |
| szint-semleges (MSc ki): 03/04/09/10/11 | ✅ | P2.1 |
| 05 valódi 🐍 placeholder-feloldás | ✅ | P2.5 |
| 07 = 07-2+07-3 (07-1 törölve, NLM-mentes) | ✅ | P2.4 |
| mappa 5_asset + 6_clean | ✅ | P2.2 |
| 6_clean camera-ready (tiszta konverzió) | ✅ | P2.9 |
| 5_asset overlay+regiszter modell | ✅ | P2.6 |
| heading-hierarchia / 06 szintek | ✅ | B-14 |
| **09b Moodle** | ⏳ `planned` | a CÉL maga is így tervezte (10. döntés) |
| **register-aware újrakonverzió** | ⏳ B-26 | a CÉL a modellt kérte, az auto-konverziót nem |

→ **A VALÓS lefedi a CÉL-t.** A két `⏳` nem rés, hanem a CÉL által szándékosan későbbre tett tétel
(09b planned, B-26 backlog) — a tervezett scope teljesült.

## 3. Checkpointok

| Checkpoint | Feltétel | Következő lépés |
|:-----------|:---------|:----------------|
| 03 után 🚦 | Mindmap revideálva, szkóp+mélység metszés kész, struktúra jóváhagyva | 04 content_synthesizer |
| 08 után 🚦 | Publikálhatóság ≥ 3/5, N_Review.md jóváhagyva | 09 + 10 + 11 egymástól függetlenül (opc. 12, 13 overlay) |

A 08-checkpointon a 😎 a PUBLIKÁLHATÓ döntés ellenére is kérhet **célzott revíziót** (a Review
`## 6` csatornáján, [08 §3.5](skills/08_quality_reviewer.md)). Forrás-stratégia szerinti routing:
**meglévő forrás** → vissza 04-hez; **új forrás** → vissza 01 → 02 → 04. A revízió után 07 → 08 újrafut.

## 4. Vizuális gazdagítás

A kötelező vizuális rétegek és a diagram-típus döntési fa **kanonikus helye**:
[Instructions.md §7](../Instructions.md). A pipeline-ban ezt a `04`, `05` (ábrák a
`figure_catalog.json`-ból) és `06` lépések valósítják meg (06: `💡 Összegzés` per `###` szakasz,
`🗺️ Fejezet összegfoglalása` per `##` fejezet — heading-hierarchia: [Instructions §7](../Instructions.md);
formátum: [06 §3](skills/06_summarize_box_injector.md)).

## 5. Mappastruktúra

→ Kanonikus: [Instructions.md §6](../Instructions.md) (`1_raw_inputs` … `5_asset_outputs`, `6_clean_outputs`).
A **camera-ready elv** ([Instructions §6.1](../Instructions.md)): a tartalom egyetlen helye a wip; a
`6_clean_outputs/` a véglegesített wip tiszta, determinisztikus konverziója — sosem szerkesztjük kézzel.

## 6. Citáció-rendszer

→ Kanonikus formátum (IEEE, `type`-alapú) és a `## Hivatkozásjegyzék` kötelezettség:
[Instructions.md §8](../Instructions.md). A `1_raw_inputs/citations.json` séma és kitöltése:
[01_source_collector](skills/01_source_collector.md); renderelés: `_ieee_renderer.py`.

## 7. Human-in-the-loop modell

A pipeline **interaktív, ember-felügyelt szerzői hurok**, nem batch és nem „background agent"-ek
raja. A 😎-szerepek a [§0](#0-hogyan-működik-az-egész-amatőr-áttekintés) tábláján; a mechanika:

| Mód | Lépések | Mit jelent |
|-----|---------|------------|
| **Szekvenciális** | 02→03→04→05→06→07→08 | output-függőség; minden lépés után a 😎 ránézhet (spot-check) |
| **Gate (emberi döntés)** | 03 🚦, 08 🚦 | a hurok itt **megáll** a 😎 jóváhagyásáig (§3) |
| **Kimenet** | 09, 10, 11 | a 08-gate után, a véglegesített wip-ből; egymástól függetlenek (de nem „párhuzamos agent") |
| **Overlay (😎-vezérelt)** | 12, 13 | a 😎 kijelöl, a 🤖 gyárt; nem automatikus (§0, 12/13 §3.2) |

Minden lépés végrehajtási protokollja a saját skill `§3 Eljárás` szekciójában él — a pipeline csak
a sorrendet és a gate-eket rögzíti.

## 8. Nyitott pontok

→ Backlog és nyitott kérdések kanonikus helye: [project_status.md](project_status.md).

## Változásjegyzék

<!-- Konvenció (Instructions): a legfrissebb változás LEGALUL (kronológiai, növekvő sorrend). -->

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (claude_play archív alapján, NLM-mentes) |
| 2026-06-02 | 1.1 | Mermaid vertikalizálva + `<br>` sortörés-javítás; D1/D2 deduplikáció (vizuális → Instructions §7, IEEE → §8); 05 script a táblába |
| 2026-06-03 | 1.2 | 05 szétválasztva: 05_figure_integrator + 06_summarize_box_injector; 06–10 lépések +1 átszámozva (→ 07–11), scriptek párhuzamosan; 12_youtube_finder + 13_jupyter_catalogizer beillesztve a kimeneti fázisba |
| 2026-06-03 | 1.3 | §4: 06 kimenete `📦 Összegző` (egyszintű) → kétszintű (`💡 Összegzés` per `##` + `🗺️ Fejezet összegfoglalása` per `#`) |
| 2026-06-04 | 1.4 | **image_rag sprint (Block 8)**: 02b_figure_enricher beillesztve a 02 és 03 közé; `figure_catalog.json` séma v4 (`_meta + sources` csoportosítva, 11 mező logikus sorrendben, `_status` derived flag, `_usage.example_entry` self-documenting); egységes `pNNN_figNNN.png` naming-konvenció; OCR-cache szkennelt PDF-ekhez. Sprint plan: [.claude/sprints/image_rag/image_rag_plan.md](sprints/image_rag/image_rag_plan.md) |
| 2026-06-05 | 1.5 | **image_rag_OCR sprint**: 02c_mineru_layout opcionális lépés (MinerU layout/formula/képpárosítás) `02 → 02c → 02b` chain-ben. 02b_figure_enricher v1.1: backend-preferencia chain (MinerU > PyMuPDF4LLM > Tesseract > Claude Read). Komparatív kutatás: [.claude/sprints/image_rag/ocr_lab/decision.md](sprints/image_rag/ocr_lab/decision.md). |
| 2026-06-05 | 1.6 | **MinerU-first pipeline**: `02_mineru_to_catalog.py` a standard 02 lépés (caption+text_context+keywords draft gépileg auto-kitöltve MinerU _content_list.json-ból); `02_image_extraction.py` fallback marad. `02b_figure_enricher` csak `visual_content` + keywords finomítás = Claude-only minimális munka. Sprint: [ocr_lab/decision.md](sprints/image_rag/ocr_lab/decision.md). |
| 2026-06-12 | 2.0 | **„Egyetlen igazság" átfésülés (P2.8, 17. döntés):** §0 amatőr-áttekintés + HITL-szereptábla az elejére; §7 „Agent architektúra" → őszinte human-in-the-loop modell (nincs „background agent"); §2 IO-tábla 02-duplikáció összevonva (MinerU-only) + 10 kimenet `6_clean`; §4/§5/§6 redundancia → kanonikus pointerek (Instructions §6/§7/§8); minden inline TODO megválaszolva/törölve; 12/13 „tervezett" → 😎-overlay; changelog sorrend növekvőre; verzió 1.6 → 2.0. |
| 2026-06-12 | 2.1 | **Aktualizálás a P2/B-14 után:** §4 heading-modell `💡` per `###` szakasz / `🗺️` per `##` fejezet (B-14); §2 IO 10-es lépés „LaTeX→PNG" → **natív OMML** (a `_latex_png.py` törlése után); a „párhuzamosan" szóhasználat „egymástól függetlenül"-re (§2.1 gráf + §3) a §7 őszinte modelljéhez igazítva. |
| 2026-06-12 | 3.0 | **§2.1 EREDETI → CÉL → VALÓS:** az egyetlen idealizált gráf helyett három állapot-gráf (EREDETI naiv lineáris, CÉL = plan_3 célgráf, VALÓS = őszinte jelenlegi: `🐍✅`/`🤖`/`😎`/`⏳` jelöléssel, 2 STOP-gate, revízió-hurok, overlay-ág) + §2.1.d Lefedettség-tábla (a VALÓS lefedi a CÉL-t; 09b/B-26 szándékosan későbbi). §2 IO-tábla alá kompakt „VALÓS-státusz" (tényleges script-lét). §0 horgony frissítve. |
