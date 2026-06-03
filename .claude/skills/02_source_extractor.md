---
name: 02_source_extractor
title: 02_SOURCE_EXTRACTOR — Ábra-kinyerő (PDF/PPTX → PNG + figure_catalog)
type: skill
tags: [meta, skill]
role: 🐍+🤖
status: active
version: 2.1
updated: 2026-06-03
description: PDF/PPTX forrásokból PNG képeket nyerünk ki 2_clean_inputs/-ba és felépítjük a figure_catalog.json-t; szkennelt könyvekhez Claude azonosítja az ábra-oldalakat, majd --source/--pages futtatással kinyerjük őket. Használd a 01_source_collector után, a 03_mindmap_builder előtt.
---

# 02_SOURCE_EXTRACTOR

## 1. Cél

A `1_raw_inputs/` forrásokból PNG képeket nyerünk ki `2_clean_inputs/<stem>/images/`-ba,
és felépítjük a `figure_catalog.json`-t a downstream 05_visual_enricher számára.
A szöveg-szintézist Claude végzi közvetlenül — itt **csak ábrák** kellenek.

**Input:** `1_raw_inputs/*.pdf`, `*.pptx` · **Output:** `2_clean_inputs/` képek + `figure_catalog.json`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `1_raw_inputs/*.pdf` | 01_source_collector | Átnevezett PDF-ek (born-digital és szkennelt) |
| `1_raw_inputs/*.pptx` | 01_source_collector | Átnevezett PPTX előadások |
| `1_raw_inputs/citations.json` | 01_source_collector | Fájlnév → citáció-kulcs (catalog-hoz) |

**Előfeltétel:** `pymupdf` és `python-pptx` telepítve; `1_raw_inputs/` nem üres.

## 3. Eljárás 🐍+🤖

### 3.1. Automatikus futtatás 🐍

```powershell
python scripts/02_source_extractor.py --week-dir test_outputs/atg/1_het
```

- **Born-digital PDF:** beágyazott képek kinyerése; dekoráció/logó (<10 000 px²) kihagyva.
- **PPTX:** dia-képek kinyerése PNG-ként.
- **Szkennelt PDF (>50% oldal = teljes oldalas kép):** kihagyja + figyelmeztetés:
  `⚠️ Használd: --source <fájlnév> --pages <oldalszámok> (Claude azonosítja)`

### 3.2. Szkennelt forrás — Claude azonosítja az ábra-oldalakat 🤖

Ha az automatikus futás szkennelt forrást jelez, Claude elolvassa a PDF-et és azonosítja
mely oldalakon van releváns ábra:

> „Olvasd el a `gravdahl1999_chapter.pdf`-et és add meg, mely oldalakon van ábra."

Claude visszaad egy oldallistát (pl. `5, 12, 23`), majd:

```powershell
python scripts/02_source_extractor.py \
  --week-dir test_outputs/atg/1_het \
  --source gravdahl1999_chapter.pdf --pages "5,12,23"
```

- **Szkennelt oldal:** teljes oldal renderelve PNG-ként (`p005_page.png`), `needs_crop: true`.
- **Born-digital oldal:** oldalanként **annyi PNG**, ahány kép van rajta.
- A crop-ot 😎 végzi manuálisan a `needs_crop: true` bejegyzéseknél.

### 3.3. figure_catalog.json bővítése

A script idempotens — meglévő katalógust betölti, új bejegyzéseket fűz hozzá.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `2_clean_inputs/<stem>/images/<img>.png` | Kinyert PNG (born-digital vagy oldal-render) |
| `2_clean_inputs/figure_catalog.json` | Ábra-katalóg (id, source, page, filename, needs_crop, citation_key) |

**`figure_catalog.json` séma:**

```json
[
  {
    "id": "fig_001",
    "source_file": "chattopadhyay2013_paper.pdf",
    "citation_key": "3",
    "page": 3,
    "image_index": 1,
    "filename": "2_clean_inputs/chattopadhyay2013_paper/images/p003_img001.png",
    "needs_crop": false,
    "caption": null,
    "suggested_section": null
  }
]
```

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het/1_raw_inputs/` (6 PDF + 1 PPTX, az 01-teszt kimenetéből).
- **Akció (automatikus):** `python scripts/02_source_extractor.py --week-dir test_outputs/atg/1_het --dry-run`
- **Várt kimenet (dry-run, verifikált):**
  - `chattopadhyay2013_paper.pdf` → 1 kép (born-digital, p3)
  - `gravdahl1999_book.pdf`, `gravdahl1999_chapter.pdf`, `tavakoli2004_paper.pdf` → szkennelt, 1-1 figyelmeztetés + `--source/--pages` utasítás
  - `wikipedia2024_webpage.pdf` → 3 kép
  - `nagy2023_slides.pptx` → 0 kép (vektoros tartalom, nincs PICTURE shape)
- **Akció (szkennelt, --pages):** `--source gravdahl1999_chapter.pdf --pages "5,12,12,12"` → p5: 1 PNG, p12: 3 PNG (`fig001/002/003`), mind `needs_crop: true`
- **Eval:** `figure_catalog.json` valid JSON; `needs_crop: true` bejegyzések jelöltek; a figyelmeztető üzenet tartalmazza a pontos parancsot.

## 6. Ellenőrzés

- [ ] Minden born-digital PDF-hez létrejöttek a PNG-k
- [ ] Szkennelt forrásokhoz figyelmeztetés + pontos `--source/--pages` utasítás jelenik meg
- [ ] `figure_catalog.json` valid JSON, `needs_crop: true` ahol kell
- [ ] Képútvonalak (`filename`) létező fájlokra mutatnak
- [ ] Idempotens: újrafuttatás nem duplikál

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `HIBA: PyMuPDF nincs telepítve` | Hiányzó csomag | `pip install pymupdf` |
| `HIBA: python-pptx nincs telepítve` | Hiányzó csomag | `pip install python-pptx` |
| PPTX → 0 kép | Vektoros/EMF tartalom (nem PICTURE shape) | Normál; a PPTX szövegét Claude olvassa közvetlenül |
| Szkennelt forrás összes oldala figyelmeztet | >50% szkennelt → helyes | Claude azonosítja az ábra-oldalakat, majd `--pages` |
| `needs_crop: true` bejegyzés, de nincs PNG | `--dry-run` volt | Futtasd le `--dry-run` nélkül |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- upstream: [01_source_collector.md](01_source_collector.md) · downstream: [03_mindmap_builder.md](03_mindmap_builder.md)
- [05_visual_enricher.md](05_visual_enricher.md) — `figure_catalog.json` fogyasztó

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
- 💬 NOTE: `nagy2023_slides.pptx` → 0 kép mert vektoros/EMF formátum (nem PICTURE type=13). Normál viselkedés; a PPTX szövegét Claude olvassa.

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (MinerU + 02-2 extractor) |
| 2026-06-03 | 2.0 | Teljes újraírás: MinerU kiváltva PyMuPDF-fel (csak ábrák, nem szöveg); szkennelt PDF detektálás + Claude-alapú oldalazonosítás + `--source/--pages`; 02-1 + 02-2 egyesítve; verifikált atg-n |
| 2026-06-03 | 2.1 | `--pages` ismétléssel N kép/oldal (N külön fájl, N catalog bejegyzés); `image_index` kivezetett; `_source_map.md` eltávolítva (provenance → `citations.json original_filename`) |
