---
name: 02_image_extraction
title: 02_image_extraction — Ábra-kinyerő (PDF/PPTX → PNG + figure_catalog v4)
type: skill
tags: [meta, skill]
role: 🐍+🤖
status: active
version: 2.9
updated: 2026-06-04
description: PDF/PPTX forrásokból egységes pNNN_figNNN.png néven képeket nyerünk ki 2_clean_inputs/-ba, felépítjük a figure_catalog.json (v4)-t image_rag meta-mezőkkel, és szkennelt PDF-eknél OCR-cache-t (text/pNNN.txt) készítünk. Használd a 01_source_collector után, a 02b_figure_enricher előtt.
---

# 02_image_extraction

## 1. Cél

A `1_raw_inputs/` forrásokból PNG képeket nyerünk ki `2_clean_inputs/<stem>/images/`-ba **egységes `pNNN_figNNN.png` névvel** (forrástípustól függetlenül), felépítjük a `figure_catalog.json` (v4) katalógust forrás szerint csoportosítva, és szkennelt PDF-oldalakhoz **OCR szövegcache-t** (`text/pNNN.txt`) készítünk. A szöveg-szintézist a 02b_figure_enricher Claude-fázisa végzi.

**Input:** `1_raw_inputs/*.pdf`, `*.pptx` · **Output:** `2_clean_inputs/<stem>/images/`, `text/` + `figure_catalog.json` (v4)

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `1_raw_inputs/*.pdf` | 01_source_collector | Átnevezett PDF-ek (born-digital és szkennelt) |
| `1_raw_inputs/*.pptx` | 01_source_collector | Átnevezett PPTX előadások |
| `1_raw_inputs/citations.json` | 01_source_collector | Fájlnév → citáció-kulcs (catalog-hoz) |

**Előfeltétel:** `pymupdf` és `python-pptx` telepítve; `1_raw_inputs/` nem üres. **OCR opcionális**: `pytesseract` + Pillow + Tesseract binary (`tesseract-ocr-eng` + `tesseract-ocr-hun`). Ha nem elérhető → WARN, OCR-cache üres marad, nem hard error.

## 3. Eljárás 🐍+🤖

### 3.1. Automatikus futtatás 🐍

```powershell
python scripts/02_image_extraction.py --week-dir test_outputs/atg/1_het
```

- **Born-digital PDF:** beágyazott raszterek + ha üres oldal vektoros ábrával, oldal-render + auto-crop; dekoráció/logó (<10 000 px²) kihagyva.
- **PPTX:** dia-képek kinyerése PNG-ként; `slide N` = `page N` a katalógusban.
- **Szkennelt PDF (>50% oldal = teljes oldalas kép):** kihagyja + figyelmeztetés:
  `⚠️ Használd: --source <fájlnév> --pages <oldalszámok> (Claude azonosítja)`

### 3.2. Szkennelt forrás — Claude azonosítja az ábra-oldalakat 🤖

Ha az automatikus futás szkennelt forrást jelez, Claude elolvassa a PDF-et és azonosítja mely oldalakon van releváns ábra:

> „Olvasd el a `gravdahl1999_chapter.pdf`-et és add meg, mely oldalakon van ábra."

Claude visszaad egy oldallistát (pl. `5, 12, 23`), majd:

```powershell
python scripts/02_image_extraction.py \
  --week-dir test_outputs/atg/1_het \
  --source gravdahl1999_chapter.pdf --pages "5,12,12,12"
```

- **Szkennelt oldal:** teljes oldal renderelve PNG-ként (`p005_fig001.png`, `p012_fig001..003.png`), `needs_crop:true`. **OCR egyszerre lefut** → `text/p005.txt`, `text/p012.txt`.
- **Born-digital oldal (specific_pages-en belül):** beágyazott képek alapján mentés; ha csak vektoros ábra → oldal-render + auto-crop.

#### Crop-szabály — mit tartsunk benn, mit vágjunk ki

A felirat (`Figure N: …`) **NEM része a vágott képnek**. A `caption` mező strukturált adat; a downstream lépések (04 jegyzet, 10 MARP, 11 DOCX, 05 figure_integrator) programatikusan illesztik a felirat-szöveget az ábra mellé.

| Tartsd benn | Vágd ki |
|-------------|---------|
| Diagram/grafikon teljes tartalma | `Figure N: <leírás>` aláíró sor |
| Tengely-feliratok (PR, Mass flow) | Oldal-fejléc / lábjegyzet / oldalszám |
| Belső címkék (Surge line, A/B/C pontok) | Az ábra fölötti/alatti bekezdés-szöveg |
| Sub-pane betűk: a), b), c), d) | Brand-fejléc, vízjel |

### 3.3. OCR — szkennelt oldalakhoz

A 02 script minden szkennelt oldal-rendernél megpróbál OCR-t:

1. **Cache-hit**: ha `2_clean_inputs/<src>/text/p{NNN}.txt` már létezik és nem üres → skip.
2. **Born-digital check**: `page.get_text("text").strip()` ha nem üres → OCR felesleges (text stream van).
3. **Tesseract elérhetőség**: ha `pytesseract` import sikertelen vagy a binary nincs PATH-on → WARN, skip.
4. **OCR**: `pytesseract.image_to_string(pixmap, lang="eng+hun")` az imént rendelt képen.
5. **Mentés**: `text/p{NNN}.txt`.

A `02b_figure_enricher` ezt fogyasztja a `text_context` és inline hivatkozások feltöltéséhez.

## 4. Kimenetek

| Fájl/mappa | Tartalom |
|:-----------|:---------|
| `2_clean_inputs/<stem>/images/pNNN_figNNN.png` | Kinyert PNG (egységes naming) |
| `2_clean_inputs/<stem>/text/pNNN.txt` | OCR szövegcache (csak szkennelt oldalakhoz) |
| `2_clean_inputs/figure_catalog.json` | Ábra-katalóg v4 (`_meta` + `sources` csoportosítva) |

**Fájlnév-konvenció: `pNNN_figNNN.png` mindenhol** (forrástípustól függetlenül). A korábbi `_img`, `_page`, `slide` prefixek megszűntek. Egy oldalon több ábra esetén folyamatos `_fig001`, `_fig002`, ... számozás.

**`figure_catalog.json` séma (v4):**

```json
{
  "_meta": {
    "schema_version": 4,
    "last_updated": "YYYY-MM-DD",
    "subject": "atg",
    "week": 1,
    "_usage": {
      "_": "Útmutató 😎-nak...",
      "roles": { ... },
      "value_convention": { ... },
      "_status_derivation": { ... },
      "fields": { ... },
      "example_entry": { ... },
      "where_to_write_observations": { ... }
    }
  },
  "sources": {
    "chattopadhyay2013_paper.pdf": {
      "citation_key": "3",
      "figures": [
        {
          "id": "fig_001",
          "page": 2,
          "path": "2_clean_inputs/chattopadhyay2013_paper/images/p002_fig001.png",

          "needs_crop": false,

          "caption": "Figure 1: Tree diagram of compressor instability",
          "caption_verified": false,

          "visual_content": "Hierarchikus fa-diagram...",
          "text_context": "Bevezető szekció vége; taxonómia... Hivatkozás: p3.",
          "keywords": ["compressor instability", "stall", "surge"],

          "_status": "draft",
          "notes": []
        }
      ]
    }
  }
}
```

**Mezőfolyam (logikus sorrend):**
1. Identitás: `id`, `page`, `path`
2. Operatív státusz: `needs_crop`
3. Ember-olvasható: `caption`, `caption_verified`
4. Szemantikus (retrieval): `visual_content`, `text_context`, `keywords`
5. Összegző + user: `_status` (derived), `notes`

**`_status` derivation (a script számolja, ne szerkeszd kézzel):**
- `verified` ← `caption_verified == true`
- `draft` ← `visual_content` kitöltve, de `caption_verified == false`
- `un-processed` ← `visual_content == null`

**Idempotencia szabály (incremental rebuild esetén):**
- Strukturális mezők (`id`, `page`, `path`, `needs_crop`): a script soha nem írja felül a meglévőt; csak fűz új bejegyzést a megfelelő `sources[<src>]["figures"]` listához.
- Meta-mezők (`caption`, `visual_content`, stb.): a script üresen hagyja az új bejegyzéseknél; a meglevő bejegyzések meta-mezőit **érintetlenül hagyja**. A meta-feltöltést a 02b_figure_enricher végzi.
- `_status`: a `save_catalog` minden mentésnél újraszámolja.
- `_meta._usage`: új katalógusba beleíródik; meglévőben hagyjuk (manuális edit megőrizve).

**Önmagát dokumentáló:** a `_meta._usage` blokk tartalmazza a `roles`, `value_convention`, `_status_derivation`, `fields`, `example_entry` szakaszokat — a felhasználó a JSON tetején minden szabályt + egy teljes példa-entry-t lát.

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het/1_raw_inputs/` (PDF + PPTX források).
- **Akció (automatikus):** `python scripts/02_image_extraction.py --week-dir test_outputs/atg/1_het --dry-run`
- **Várt kimenet (dry-run):**
  - Born-digital PDF-ek és PPTX → kép-számok kiírva
  - Szkennelt források → figyelmeztetés + `--source/--pages` utasítás
- **Akció (szkennelt, --pages):** `--source gravdahl1999_chapter.pdf --pages "5,12,12,12"` → p5: 1 PNG, p12: 3 PNG (mind `_fig001..003`), mind `needs_crop:true`, és `text/p005.txt` + `text/p012.txt` OCR-cache.
- **Eval:** `figure_catalog.json` valid JSON, `_meta.schema_version == 4`; `needs_crop:true` bejegyzések jelöltek; OCR cache létezik a szkennelt oldalakhoz; minden entry `_status` mezője az 3 értékből egyik.

## 6. Ellenőrzés

- [ ] Minden born-digital PDF-hez létrejöttek a PNG-k `pNNN_figNNN.png` névvel
- [ ] Szkennelt forrásokhoz figyelmeztetés + pontos `--source/--pages` utasítás
- [ ] `figure_catalog.json` valid JSON, séma v4 (`_meta.schema_version == 4`)
- [ ] Minden entry-n `_status` érték az 3 érték közül egy (`un-processed`/`draft`/`verified`)
- [ ] Új bejegyzések: minden új mező alapértékkel kitöltve (`caption:null`, `visual_content:null`, `keywords:[]`, `notes:[]`)
- [ ] Képútvonalak (`path`) létező fájlokra mutatnak
- [ ] OCR cache (`text/pNNN.txt`) létezik a szkennelt oldalakhoz (vagy WARN ha Tesseract nem elérhető)
- [ ] Idempotens: újrafuttatás nem duplikál ÉS nem írja felül a meglévő meta-mezőket

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `HIBA: PyMuPDF nincs telepítve` | Hiányzó csomag | `pip install pymupdf` |
| `HIBA: python-pptx nincs telepítve` | Hiányzó csomag | `pip install python-pptx` |
| `⚠️ OCR kihagyva (pytesseract... nem elérhető)` | Hiányzó OCR-dependency | `pip install pytesseract Pillow` + Tesseract binary install |
| PPTX → 0 kép | Vektoros/EMF tartalom (nincs PICTURE shape) | Normál; a PPTX szövegét Claude olvassa közvetlenül |
| Szkennelt forrás összes oldala figyelmeztet | >50% szkennelt → helyes | Claude azonosítja az ábra-oldalakat, majd `--pages` |
| `needs_crop:true` bejegyzés, de nincs PNG | `--dry-run` volt | Futtasd le `--dry-run` nélkül |
| `HIBA: nem v4 séma` | Régi katalógus | Wipe + regen, vagy manuális migráció |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- upstream: [01_source_collector.md](01_source_collector.md) · downstream: [02b_figure_enricher.md](02b_figure_enricher.md), [03_mindmap_builder.md](03_mindmap_builder.md)
- [05_figure_integrator.md](05_figure_integrator.md) — `figure_catalog.json` szemantikus fogyasztó

## 9. Visszajelzések

- 💬 NOTE: `nagy2023_slides.pptx` típusú PPTX → képek PLACEHOLDER (type=14) shape-ekben vannak. XML-alapú (`blipFill`) detektálással kinyerhetők. A `shape_type==13` feltétel nem elégséges.
- 💬 NOTE: A born-digital vektoros oldalak (pl. chattopadhyay fa-diagramok) auto-crop alacsony (3-5%) margólevágást ad — szövegközi ábráknál ez nem elég, manuális crop szükséges. A `needs_crop:true` jelzi.

### 9.1. Caption auto-detekció — 3 gyökérok (atg/1_het tanulság)

Korábbi regex-alapú caption-detekció szisztematikus hibái (mind átkerül a 02b Claude-fázisba):
1. **Regex-túlcsordulás "Figure N: ...\\."** — a `[^.\n]{3,250}\.` minta a felirat MELLETTI szöveg első pontjáig olvas. Ha a felirat pont nélkül végződik (pl. "Figure 1: Tree diagram of compressor instability"), átszalad a következő bekezdés első mondatába. **Fix:** geometriai caption-zóna (PyMuPDF `get_text("blocks")` — a kép `bbox` alatti legközelebbi szövegblokk).
2. **fig_N ↔ Figure N(.M) index-csúszás** — a fájlnév-index nem feltétlenül egyezik a forrás-sorszámmal. **Fix:** `figure_label`-t (ha visszahozzuk) a caption SZÖVEGÉBŐL parse-oljuk, nem a fájlnévből; jelenleg a v4 séma kihagyja, on-demand számolható.
3. **Sortörés-kötőjel + speciális karakter** — "vo- lute", `ξ`, sub-pane (a) b) c) d)) lemarad. **Fix:** `re.sub(r"-\s*\n", "", txt)` + `unicodedata.normalize("NFC", txt)`.

### 9.2. Naming-konvenció döntés (v2.9, 2026-06-04)

A korábbi 4 különböző mintát (`pNNN_figNNN`, `pNNN_imgNNN`, `slideNNN_imgNNN`, `pNNN_page`) **egyesítettük `pNNN_figNNN.png`-re** mindenhol. A `fig` vs `img` és `slide` vs `p` distinkciók implementáció-belsőek; downstream-nek mindegy. Egy oldalon több ábra esetén folyamatos `_fig001`, `_fig002`, ...

### 9.3. Önmagát dokumentáló katalógus (v2.9)

A `_meta._usage` blokkban az új `example_entry` mező egy teljes, fiktív példa-entry (id: `fig_000_EXAMPLE`) — a 😎 a JSON tetején azonnal lát egy kitöltött mintát minden mezővel.

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (MinerU + 02-2 extractor) |
| 2026-06-03 | 2.0 | Teljes újraírás: MinerU kiváltva PyMuPDF-fel; szkennelt PDF detektálás + Claude-alapú oldalazonosítás + `--source/--pages` |
| 2026-06-03 | 2.1 | `--pages` ismétléssel N kép/oldal; `image_index` kivezetett |
| 2026-06-03 | 2.2 | PPTX extractor: XML-alapú `blipFill` detektálás (minden shape-típus) |
| 2026-06-03 | 2.3 | `specific_pages` mód: vektoros ábra detektálás born-digital oldalon |
| 2026-06-03 | 2.4 | Auto-crop (`_auto_crop.py`) + `_crop_tasks.md` |
| 2026-06-03 | 2.5 | `_crop_tasks.md`: minden katalógus-bejegyzés listázva, caption-auto-detekció |
| 2026-06-03 | 2.6 | `_crop_tasks.md` markdown táblázat formátum |
| 2026-06-04 | 2.9 | **v4 séma + OCR + naming-konvenció (Block 8)**: `_meta + sources` csoportosítás, 11 mező logikus sorrendben, `_status` derived flag, `_usage.example_entry` self-documenting, `pNNN_figNNN.png` egységes naming, pytesseract OCR-cache szkennelt oldalakhoz (`text/pNNN.txt`), `_crop_tasks.{py,md}` round-trip eltávolítva. A v2 / v3 közbenső sémák (image_rag branch evolúció) törölve a rewind-dal — a main-en csak v1 séma volt, az image_rag újra létrehozva v4-gyel egyenesen. |
