---
title: image_rag sprint — review notes (😎)
type: sprint_notes
status: active
created: 2026-06-04
---

# image_rag review notes

> Sprint-szintű megfigyelések (😎). Egy-egy ábrához tartozó megjegyzés a katalógusban (`figure_catalog.json` `notes` mező), itt a folyamat-szintű észrevételek élnek.
>
> Formátum: emoji-prefix + 1-2 mondat. Lezárt tétel → áthúzva vagy a [pl. 02_image_extraction] skill `§9` / `image_rag_plan.md`-be merge-elve, majd innen törölve.

## Aktuális

<!-- ide írd a megjegyzéseidet review közben -->

## Backlog / nyitott pontok

- ⚠️ DESIGN: A `fig_NNN` ID-k NEM stabilak forráscsere esetén (alfabetikus sorrend miatt). A v3 sprintben kiderült: `nagy2023_slides.pptx → hari2025_slides.pptx` swap 56/67 fig_id-t eltolt. Ezért minden `apply_*.py` sprint-script **(source_file, fájlnév)** kulcson lookupol. A downstream `05_figure_mapper` is ezt kell tegye, ne fig_id-re építse a hivatkozásait.

- 💡 IDEA: A meta-bootstrap (02b) skill jelenleg manuálisan futtatott `apply_meta_bootstrap.py` formában él (hard-coded META dict). Egy automatizált változat egy Python script lehetne, ami önállóan végigmegy a katalóguson, image-eket `Read`-eli, source-szöveget `get_text()`-eli, és az LLM-mel tölti — de ez egy külön sprint témája.

## Lezárt megfigyelések

- ✅ DONE (Block 8): OCR (pytesseract) integrálva a `02_image_extraction`-be — szkennelt page-renderelt oldalakhoz `text/pNNN.txt` cache. A 02b enricher fallback-ként olvassa, ha a forrás-PDF text-stream üres. Tesseract binary opcionális; ha nincs → WARN, nem hard error.

- ✅ DONE (Block 8): Naming-konvenció egyesítve `pNNN_figNNN.png`-re minden forrástípuson (PDF born-digital + scanned + PPTX). A korábbi `_img`, `_page`, `slide` prefixek eltüntek.

- ✅ DONE (Block 8): Séma v4 — 15 mező → 11, logikus sorrendben, `_status` derived flag, `_meta._usage.example_entry` ön-dokumentációval.
