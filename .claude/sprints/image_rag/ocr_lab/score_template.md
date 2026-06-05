---
title: OCR Lab — manual score rubric
type: scoring
sprint: image_rag_OCR
status: filled
date: 2026-06-05
---

# OCR Lab — manual score rubric (4 backend × 7+ dimenzió)

Skála: **0 = nem alkalmas / hiányzik · 1 = gyenge · 2 = OK · 3 = kiváló**.
Bool flagek: ✓ / ✗.

## Char-count alapú objektív arány (Tesseract / Claude Read)

| Forrás-csoport | Ratio | Értelmezés |
|---|---:|---|
| Scanned scientific angol (gravdahl + tavakoli) | **0.94** | Tesseract ~teljes szöveg |
| Hungarian slides (nagyi) | **0.59** | Tesseract csak FELÉT adja vissza, + diakritika hibás |
| Born-digital angol (chattopadhyay) | **0.98** | Tesseract ~teljes szöveg |

## Time/page

| Backend | s/page | Megjegyzés |
|---|---:|---|
| PyMuPDF4LLM | 0.35 | csak born-digital |
| Tesseract | 1.32 | CPU |
| MinerU | 1.0 (range-averaged) | tényleges per-page ~30–40s (model init + layout + OCR + képek), batch-szel amortizálódik |
| Claude Read | ~30 (kézi) | becslés: szem + gépelés/oldal (én nem mérem) |

## Per-backend score (1–3 + bool)

### 1. Tesseract
| Dimenzió | Pont | Indok |
|---|:---:|---|
| Pipeline-fit (text_context-hez) | **2** | Plain text közvetlenül `text/pNNN.txt`-be megy |
| Cross-step 03 mindmap (struktúra) | 1 | Heading nem felismert; vakszöveg |
| Cross-step 04 synthesizer (idézet) | 2 | Idézhető angolul; magyarul gyenge |
| Cross-step 07 typesetter (formula/tábla) | 0 | Sem LaTeX, sem MD-tábla |
| Cross-step 09 question_bank (tábla) | 0 | Tábla-szerkezet elveszik |
| Output quality | 2 (en) / 1 (hu) | hu diakritika hibás (centrifugalis ≠ centrifugális) |
| Install cost | 2 | binary nincs PATH-ban, hun.traineddata manual download |
| Idempotencia | ✓ | overwrite safe |
| Capability — scanned | ✓ | Fő use-case |
| Capability — hungarian | ✗ | Diakritika eltűnik |
| Capability — formula → LaTeX | ✗ | — |
| Capability — table → MD | ✗ | — |
| Capability — two-column ordering | ✗ | Sorrend-keveredés várható (chattopadhyay-n ad hoc OK volt) |

### 2. PyMuPDF4LLM
| Dimenzió | Pont | Indok |
|---|:---:|---|
| Pipeline-fit | **3** | Markdown közvetlen, born-digitalra |
| Cross-step 03 | 2 | Heading-ek megmaradnak |
| Cross-step 04 | 3 | Pontos szövegidézés (text stream) |
| Cross-step 07 | 1 | Néha matek-szöveg, LaTeX nem |
| Cross-step 09 | 1 | Egyszerű táblák OK; komplex nem |
| Output quality | 3 (born-digital) / 0 (scanned) | gravdahl 57 char/oldal — gyakorlatilag semmi |
| Install cost | 0 | `pip install pymupdf4llm` (PyMuPDF már megvolt) |
| Idempotencia | ✓ | — |
| scanned | ✗ | Csak text-stream |
| hungarian | ✓ | text-stream UTF-8 |
| formula → LaTeX | ✗ | — |
| table → MD | ✓ | text-stream MD |
| two-column ordering | ~ | Jellemzően OK |

### 3. MinerU (2.7.6, pipeline backend, `-l latin` magyar / `-l en` angol)
| Dimenzió | Pont | Indok |
|---|:---:|---|
| Pipeline-fit | **3** | Markdown + `_content_list.json` + képek + captionok strukturáltan |
| Cross-step 03 | **3** | Heading-szintek detektálva (`# 3. FUNDAMENTALS…`) |
| Cross-step 04 | **3** | Tisztított szöveg, captionok |
| Cross-step 07 | **3** | `$50\%$` LaTeX formula (mért, tavakoli p2 sample) |
| Cross-step 09 | 2 | Tábla-MD jellemzően OK (jelen szetten kevés tábla) |
| Output quality | 3 (en) / **3 (hu)** | Magyar diakritika **MÉRT** kifogástalan a nagyi mintán (Centrifugális, járókerék, sajátfrekvenciája hibátlanul). Egy minor typo egy heading-ben („Cenrtifugális"). |
| Install cost | **3** | külön conda env, ~1-2 GB ML modell-download |
| Idempotencia | ~ | `<stem>/auto/` újrafutáskor felülíródik |
| scanned | ✓ | PaddleOCR backend |
| hungarian | ~ | csak `latin` lang közelít |
| formula → LaTeX | ✓ | **MÉRT** |
| table → MD | ✓ | dokumentáltan |
| two-column ordering | ✓ | layout-aware |

### 4. Claude Read (session-szintű, manual)
| Dimenzió | Pont | Indok |
|---|:---:|---|
| Pipeline-fit | **3** | Strukturált szöveg + ábra-leírás egyszerre |
| Cross-step 03 | **3** | Tartalom+címek kombinálva |
| Cross-step 04 | **3** | Idézhető pontosan |
| Cross-step 07 | 2 | LaTeX-et explicit kérni kell |
| Cross-step 09 | 3 | Tábla-MD kérésre, kontextus-aware |
| Output quality | **3 mindenre** | nagyi: "centrifugális szivattyúk" hibátlanul |
| Install cost | **0** | Nincs külső dep |
| Idempotencia | ✓ | Write overwrite |
| scanned | ✓ | egyenértékű image-ből |
| hungarian | ✓ | tökéletes |
| formula → LaTeX | ✓ kérésre | — |
| table → MD | ✓ kérésre | — |
| two-column ordering | ✓ | szövegértés-alapú |

**Hátrány:** kézi, nem batch — 15 oldal ~30 perc; egy teljes hét 67 oldalához ~2 óra session-idő.

## Cross-step value összesítő (max 12)

| Backend | 03 | 04 | 07 | 09 | Σ |
|---|:--:|:--:|:--:|:--:|--:|
| Tesseract | 1 | 2 | 0 | 0 | **3** |
| PyMuPDF4LLM | 2 | 3 | 1 | 1 | **7** |
| MinerU | 3 | 3 | 3 | 3 | **12** |
| Claude Read | 3 | 3 | 2 | 3 | **11** |

## Pareto-pontok (output minőség × install cost × time)

| Backend | Quality (hu) | Install | Time | Pareto-szerep |
|---|:--:|:--:|:--:|---|
| PyMuPDF4LLM | 3 (born-d.) / 0 (scanned) | 0 | 0.35s | **Pareto-optimal** born-digitalra |
| Tesseract | 1 (hu) / 2 (en) | 2 | 1.3s | dominált hu-n MinerU-tól; en-en kiegyenlített |
| MinerU | 2 (hu) / 3 (en) | 3 | 1.0–40s | **Pareto-optimal** layout+formula igényen |
| Claude Read | 3 mindenre | 0 | manuális | **Pareto-optimal** quality+install |

## Tanulság — hipotézisekre

- **H1 (Tesseract elég):** Részben — **csak angol szkenneltre**. Magyaron (nagyi) 0.59 char ratio + hiányzó diakritika → minőség sub-par.
- **H2 (MinerU érdemi plusz):** **IGEN** — `$50\%$` LaTeX, képpárosítás (`Fig. 1.`), heading-detection mért. Cross-step Σ=11, holott Tesseract Σ=3.
- **H3 (Claude Read elég):** **IGEN minőségileg** — magyaron is tökéletes. Skálázhatatlanság a korlát.
- **H4 (hibrid Pareto):** **IGEN** — minden forrás-típusra van Pareto-optimal backend.
