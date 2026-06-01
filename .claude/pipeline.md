---
title: Pipeline.md — claude_course
type: meta
status: active
version: 1.0
updated: 2026-06-01
description: Claude-natív tananyagfejlesztési pipeline. NLM-mentes.
---

# PIPELINE.MD — claude_course

## 1. A tradicionális oktató → Claude leképezés

| Oktató | Claude-pipeline |
|--------|-----------------|
| Célcsoport, tanterv | `00_init` — context.json |
| Anyaggyűjtés | `01_source_collector` |
| Olvas → megért → szintetizál | `02_source_extractor` + `03_mindmap_builder` |
| **Elmetérkép** | **03 kimenet: mindmap** (😎 revideálja) |
| Word: ír, hivatkozik, képek, egyenletek | `04_content_synthesizer` |
| Word → PowerPoint | `09_presentation_maker` |
| Vizsgakérdések (Moodle MCQ) | `08_question_bank` |
| Jupyter notebook | 🔲 jövőbeni `11_notebook_maker` |

**Kulcselv:** A megértés diktálja a struktúrát — nem a fejezetek, hanem a fogalmi összefüggések.

## 2. Lépések és IO

| Input | Felelős | Lépés | Automatizáltság | Output |
|:------|:--------|:------|:----------------|:-------|
| Célcsoport, hetek, tantárgy | 😎 | [`00_init`](skills/00_init.md) — `00_init_course.py` | 🐍 | `context.json` + mappák |
| URL-ek, PDF-ek, PPTX-ek | 😎+🤖 | [`01_source_collector`](skills/01_source_collector.md) | 🤖+😎 | `1_raw_inputs/` + `citations_seed.json` |
| `1_raw_inputs/` | 🐍 | [`02_source_extractor`](skills/02_source_extractor.md) — MinerU + HTML/PPTX | 🐍 | `2_clean_inputs/` + `figure_catalog.json` |
| `2_clean_inputs/` | 🤖 | [`03_mindmap_builder`](skills/03_mindmap_builder.md) — olvas, szintetizál | 🤖 🚦😎 | `3_mindmap/mindmap.md` (flowchart LR) |
| `3_mindmap/mindmap.md` | 🤖 | [`04_content_synthesizer`](skills/04_content_synthesizer.md) — mindmap-vezérelt szintézis | 🤖 🚦 | `4_wip_outputs/N_Jegyzet.md` |
| `4_wip_outputs/N_Jegyzet.md` | 🤖 | [`05_visual_enricher`](skills/05_visual_enricher.md) — figure_catalog + összegzők | 🤖 | `4_wip_outputs/N_Jegyzet.md` (gazdagítva) |
| `4_wip_outputs/N_Jegyzet.md` | 🐍 | `06_typesetter.py` | 🐍 | `4_wip_outputs/N_Jegyzet.md` (lint) |
| `4_wip_outputs/N_Jegyzet.md` | 🐍+🤖 | [`07_quality_reviewer`](skills/07_quality_reviewer.md) — `07_quality_check.py` | 🐍+🤖 🚦😎 | `4_wip_outputs/N_Review.md` |
| `4_wip_outputs/N_Jegyzet.md` | 🤖 | [`08_question_bank`](skills/08_question_bank.md) — mindmap-alapú MCQ | 🤖 | `4_wip_outputs/N_Kerdesbank.md` |
| `4_wip_outputs/N_Jegyzet.md` | 🤖+🐍 | [`09_presentation_maker`](skills/09_presentation_maker.md) — MARP → PPTX | 🤖+🐍 | `4_wip_outputs/N_Prezentacio.md` + `5_clean_outputs/N_Prezentacio.pptx` |
| `4_wip_outputs/N_Jegyzet.md` | 🐍 | [`10_bsc_export`](skills/10_bsc_export.md) — `10_bsc_filter.py` + pandoc | 🐍 | `5_clean_outputs/N_Jegyzet[_bsc].docx` |

## 2.1 Vizualizáció

```mermaid
flowchart TD
    subgraph INIT["① Előkészítés"]
        I0["00 init\n🐍\ncontext.json + mappák"]
        I1["01 source_collector\n😎 + 🤖\n1_raw_inputs/"]
        I0 --> I1
    end

    subgraph EXT["② Forrás-feldolgozás"]
        E1["02 source_extractor\n🐍\nMinerU + HTML/PPTX\n→ 2_clean_inputs/\n+ figure_catalog.json"]
    end

    subgraph UNDERSTAND["③ Megértés — sarokkő"]
        U1["03 mindmap_builder\n🤖\nforrások olvasása\n→ mindmap draft"]
        U2{"😎 Checkpoint\nRevízió + MSc jelölés\n→ 3_mindmap/mindmap.md"}
        U1 --> U2
    end

    subgraph CREATE["④ Tartalom-alkotás"]
        C1["04 content_synthesizer\n🤖\nmindmap-vezérelt szintézis\n+ Mermaid diagramok\n+ IEEE hivatkozások\n→ 4_wip_outputs/N_Jegyzet.md"]
        C2["05 visual_enricher\n🤖\nfigure_catalog beillesztés\n+ összegző dobozok\n→ 4_wip_outputs/N_Jegyzet.md"]
        C1 --> C2
    end

    subgraph QUALITY["⑤ Minőség"]
        Q1["06 typesetter\n🐍\n06_typesetter.py"]
        Q2["07 quality_reviewer\n🐍 + 🤖\nmetrikák + Explore review\n→ N_Review.md"]
        Q3{"😎 Checkpoint\npublikálhatóság ≥ 3/5"}
        Q1 --> Q2 --> Q3
    end

    subgraph OUTPUT["⑥ Kimenetek — párhuzamosan"]
        O1["08 question_bank\n🤖\nMoodle MCQ\nA–D alternatívák"]
        O2["09 presentation_maker\n🤖 + 🐍\nMARP → PPTX\n1 vizuális/dia"]
        O3["10 bsc_export\n🐍\n10_bsc_filter\n→ 5_clean_outputs/\n.docx camera-ready"]
    end

    INIT --> EXT --> UNDERSTAND --> CREATE --> QUALITY
    Q3 -->|"🟢 OK"| O1 & O2 & O3
    Q3 -->|"🔴 Javít"| C1
```

## 3. Checkpointok

| Checkpoint | Feltétel | Következő lépés |
|:-----------|:---------|:----------------|
| 03 után 🚦 | Mindmap revideálva, [MSc] jelölés kész, struktúra jóváhagyva | 04 content_synthesizer |
| 07 után 🚦 | Publikálhatóság ≥ 3/5, N_Review.md jóváhagyva | 08 + 09 + 10 párhuzamosan |

## 4. Vizuális gazdagítás — kötelező

| Réteg | Kötelező | Eszköz |
|-------|----------|--------|
| Navigátor mindmap | ✅ minden outputban | Mermaid flowchart LR |
| Szekciós diagram | ✅ ha ≥3 fogalom összefügg | Mermaid (típus a tartalomtól függ) |
| Valódi ábra | ⚙️ ha MinerU kinyerte | `figure_catalog.json` alapján |
| MARP vizuális | ✅ minden dián | Mermaid VAGY ábra |

## 5. Mappastruktúra (tantárgy-szintű)

```
{tantargy}/
└── {N_het}/
    ├── 1_raw_inputs/       😎  nyers PDF-ek, HTML-ek, PPTX-ok
    │   └── citations_seed.json
    ├── 2_clean_inputs/     🐍  MinerU + extraktor kimenetek
    │   ├── {forrás}/
    │   │   ├── images/
    │   │   └── {forrás}.md
    │   └── figure_catalog.json
    ├── 3_mindmap/          🤖  mindmap (Claude generálta, user revideálta)
    │   └── mindmap.md          (flowchart LR, [MSc] prefixek)
    ├── 4_wip_outputs/      🤖  work-in-progress outputok
    │   ├── N_Jegyzet.md        (Mermaid diagramok + összegzők + IEEE refs)
    │   ├── N_Kerdesbank.md
    │   ├── N_Prezentacio.md
    │   └── N_Review.md
    └── 5_clean_outputs/    ✅  camera-ready végtermékek
        ├── N_Prezentacio.pptx
        ├── N_Jegyzet.docx
        └── N_Jegyzet_bsc.docx
```

## 6. Citáció-rendszer

```json
// citations.json — fájlnév-alapú, IEEE-kompatibilis
{
  "_meta": {"subject": "...", "week": 1},
  "1": {"author": "...", "title": "...", "year": "...", "filename": "...", "pages": "..."},
  "2": {"author": "...", "title": "...", "url": "...", "accessed": "2026-06-01"}
}
```

- Szövegben: `[S1]`, `[S2]` stb.
- Minden wip és clean outputban kötelező: `## Hivatkozásjegyzék` (IEEE formátum)
- Generálás: `08_ieee_renderer.py` (fájlnév-alapú lookup)

## 7. Agent architektúra

| Típus | Lépések | Indok |
|-------|---------|-------|
| Szekvenciális (foreground) | 02→03→04→05→06→07 | Output-függőség; checkpointok |
| Párhuzamos (background) | 08 ‖ 09 ‖ 10 | Független outputok |
| Interaktív (inline) | 03 checkpoint, 07 checkpoint | Emberi döntés szükséges |

Az agent-prompt minden skill esetén a skill `§3 Eljárás` szekciója alapján generálódik.

## 8. Nyitott pontok

- 🔲 TODO: `00_init_course.py` portolása és tesztelése
- 🔲 TODO: `08_ieee_renderer.py` UUID→filename patch elkészítése
- 🔲 TODO: `11_notebook_maker` skill (Jupyter szemléltetés) — jövőbeni lépés

## Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (claude_play archív alapján, NLM-mentes) |
