---
name: 02_source_extractor
title: 02_SOURCE_EXTRACTOR — MinerU PDF + HTML/PPTX extraktor
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-06-01
description: 1_raw_inputs/ forrásokból Markdown szöveg és figure_catalog.json kinyerése MinerU és egyedi extractorok segítségével.
---

# 02_SOURCE_EXTRACTOR

## 1. Cél

A `1_raw_inputs/` nyers forrásokból tisztított Markdown szöveget és ábrakatalógust nyerünk ki,
hogy a 03_mindmap_builder és 04_content_synthesizer egységes formátumban dolgozzon.

**Input:** `1_raw_inputs/*.pdf`, `*.url`, `*.pptx`
**Output:** `2_clean_inputs/{forrás}/{forrás}.md` + `2_clean_inputs/figure_catalog.json`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `1_raw_inputs/*.pdf` | 01_source_collector | Nyers PDF forrásanyagok |
| `1_raw_inputs/*.url` | 01_source_collector | URL hivatkozások |
| `1_raw_inputs/*.pptx` | 01_source_collector | PowerPoint előadások |
| `1_raw_inputs/citations_seed.json` | 01_source_collector | Bibliográfiai metaadatok |

**Előfeltétel:** MinerU telepítve és futtatható; `1_raw_inputs/` nem üres.

## 3. Eljárás

### 3.1. PDF extraktor — MinerU

```powershell
python scripts/02-1_mineru_pipeline.py --week N --subject "Jelatvitel"
```

- Minden PDF-et külön almappában dolgoz fel: `2_clean_inputs/{forrás_neve}/`
- Kimenet: `{forrás_neve}.md` + `images/` almappa ábrafájlokkal
- `figure_catalog.json` automatikusan frissül

### 3.2. Web/HTML extraktor

```powershell
python scripts/02-2_source_extractor.py --mode url --week N --subject "Jelatvitel"
```

- `.url` fájlokból letölti és Markdown-ra konvertálja a tartalmat
- Képek: `2_clean_inputs/{forrás_neve}/images/`-be mentve

### 3.3. PPTX extraktor

```powershell
python scripts/02-2_source_extractor.py --mode pptx --week N --subject "Jelatvitel"
```

- Diákból szöveg + ábra kinyerés
- Mermaid diagram-javaslat komment formában ahol logikailag lehetséges

### 3.4. figure_catalog.json struktúra

```json
[
  {
    "id": "fig_001",
    "source": "Proakis_2001_DSP",
    "page": 23,
    "filename": "2_clean_inputs/Proakis_2001_DSP/images/fig_001.png",
    "caption": "Block diagram of a digital communication system",
    "suggested_section": null
  }
]
```

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `2_clean_inputs/{forrás}/{forrás}.md` | Tisztított Markdown, képhivatkozásokkal |
| `2_clean_inputs/{forrás}/images/` | Kinyert ábrafájlok |
| `2_clean_inputs/figure_catalog.json` | Összes ábra metaadatai |

## 5. Ellenőrzés

- [ ] Minden PDF-hez létrejött `.md` fájl
- [ ] `figure_catalog.json` valid JSON és nem üres (ha volt ábra a forrásban)
- [ ] Markdown fájlok olvashatók, nem tartalmaznak OCR szemetet (>10% zaj → újrafuttatás)
- [ ] Képútvonalak a `.md`-ben relatívak és létező fájlokra mutatnak

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| MinerU `CUDA out of memory` | Túl nagy PDF / GPU memória | `--device cpu` flag; oldalszám-korlát |
| Üres `.md` output | Szkenelt (nem OCR) PDF | MinerU OCR mode: `--ocr true` |
| `figure_catalog.json` hiányzó bejegyzések | Raszteres ábra felismerés sikertelen | Manuális bejegyzés; `suggested_section: null` |
| PPTX képlet `.pptx`-ben `####` | Math blokk konverzió hiba | Kézzel javítandó LaTeX-re |
| URL letöltés timeout | Lassú szerver / captcha | Manuális mentés HTML-ként + `--mode html` |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [03_mindmap_builder.md](03_mindmap_builder.md) — következő lépés
- [05_visual_enricher.md](05_visual_enricher.md) — figure_catalog fogyasztó

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
