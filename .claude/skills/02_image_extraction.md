---
name: 02_image_extraction
title: 02_image_extraction — Ábra-kinyerő (PDF/PPTX → PNG + figure_catalog)
type: skill
tags: [meta, skill]
role: 🐍+🤖
status: active
version: 2.6
updated: 2026-06-03
description: PDF/PPTX forrásokból PNG képeket nyerünk ki 2_clean_inputs/-ba és felépítjük a figure_catalog.json-t; szkennelt könyvekhez Claude azonosítja az ábra-oldalakat, majd --source/--pages futtatással kinyerjük őket. Használd a 01_source_collector után, a 03_mindmap_builder előtt.
---

# 02_image_extraction

## 1. Cél

A `1_raw_inputs/` forrásokból PNG képeket nyerünk ki `2_clean_inputs/<stem>/images/`-ba,
és felépítjük a `figure_catalog.json`-t a downstream 05_figure_integrator számára.
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
python scripts/02_image_extraction.py --week-dir test_outputs/atg/1_het
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

#### ⚠️ Speciális PDF-formátumok — figyelj ezekre szkennelés előtt

**1. Könyv előoldalak (front matter) — ne dobd ki:**
Könyveknél a tényleges tartalom nem az 1. PDF-oldalon kezdődik — borító, copyright, tartalomjegyzék, előszó tipikusan 3–6 PDF-oldalt tesz ki. Ne feltételezd, hogy PDF p1 = könyv 1. fejezete. A fejezet-határokat a fejezet-címek alapján azonosítsd. **A tartalomjegyzéket tartalmazó oldal(ak) értékes inputok — jóformán egy kész mindmap — maradjanak benne a fejezet-splitben (tipikusan a ch01 PDF-be).**

**2. Kettős tördelés (dual-page layout):**
Ha a PDF-oldal képe extrém széles és alacsony (képarány > 1.5, pl. 2332×500 px), valószínűleg egy szkennelt könyvből két könyvoldalt látunk egymás mellett egy PDF-lapon. Következmények:
- 1 PDF-oldal = 2 könyvoldal → a crop-nak először félbe kell vágni, majd az ábrára szűkíteni
- Ha mindkét oldalon van ábra: `--pages N,N` (dupla hivatkozás)
- A kettős tördelés tényét jegyezd fel a `_crop_tasks.md` fejlécébe
- **Fejezet-split határán lévő „átlógó" oldal:** ha egy PDF-oldal bal fele az egyik fejezet végét, jobb fele a következő fejezet elejét tartalmazza, azt az oldalt **félbe kell vágni** — bal fele az előző fejezetfájl végére, jobb fele a következő fejezetfájl elejére kerül. Nem duplikálunk, nem hagyunk ki. Ez determinisztikus: teli vagy üres oldaltól független. (`page.show_pdf_page(..., clip=fitz.Rect(...))`)
- **Ideiglenes lapok (`_page_scan/` és hasonlók) törlése kötelező** — szemetet nem hagyunk magunk után. A scan elvégzése után azonnal takarítani kell.

```powershell
python scripts/02_image_extraction.py \
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
| `2_clean_inputs/figure_catalog.json` | Ábra-katalóg (id, source, page, filename, needs_crop, caption, citation_key) |
| `2_clean_inputs/_crop_tasks.md` | Crop-feladatlista — forrásonként markdown táblázat (`✓ \| id \| fájl \| oldal \| útvonal \| Caption`), **minden** képet listáz; `[x]` ha kész, `[ ]` ha vár. Caption cella üres ha nincs felirat, vagy `?` prefixszel ha auto-detektált, de bizonytalan. |

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
- **Akció (automatikus):** `python scripts/02_image_extraction.py --week-dir test_outputs/atg/1_het --dry-run`
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
- [05_figure_integrator.md](05_figure_integrator.md) — `figure_catalog.json` fogyasztó

## 9. Visszajelzések

- 💬 NOTE: `nagy2023_slides.pptx` → képek PLACEHOLDER (type=14) shape-ekben vannak, nem PICTURE (type=13)-ban. XML-alapú (`blipFill`) detektálással 8 kép kinyerhető. A `shape_type == 13` feltétel nem elégséges: az emberek változatos módszerekkel szerkesztenek PPTX-et.
- 💬 NOTE: `gravdahl1999_chapter.pdf` (62 oldalas, 100% szkennelt) — Claude 17 ábra-oldalt azonosított (Fig 1.1–1.17). 0 fals pozitív, 0 fals negatív. Manuális crop szükséges (szkennelt ág).
- 💬 NOTE: `chattopadhyay2013_paper.pdf` — p3 raszteres kép (`needs_crop: false`), p2+p4 vektoros fa-diagramok → auto-crop 25% margólevágással (`needs_crop: false`).

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (MinerU + 02-2 extractor) |
| 2026-06-03 | 2.0 | Teljes újraírás: MinerU kiváltva PyMuPDF-fel (csak ábrák, nem szöveg); szkennelt PDF detektálás + Claude-alapú oldalazonosítás + `--source/--pages`; 02-1 + 02-2 egyesítve; verifikált atg-n |
| 2026-06-03 | 2.1 | `--pages` ismétléssel N kép/oldal (N külön fájl, N catalog bejegyzés); `image_index` kivezetett; `_source_map.md` eltávolítva (provenance → `citations.json original_filename`) |
| 2026-06-03 | 2.2 | PPTX extractor: `shape_type==13` → XML-alapú `blipFill` detektálás (minden shape-típus, GROUP rekurzív); `lxml`-függőség hozzáadva |
| 2026-06-03 | 2.3 | `specific_pages` mód: born-digital oldalon nincs raszterkép → vektoros ábra detektálás, oldalrenderelés + `needs_crop: true` (chattopadhyay fadiagramok) |
| 2026-06-03 | 2.4 | Auto-crop (`_auto_crop.py`): vektoros render után Pillow `getbbox()`, fehér margók levágása, `needs_crop: false` ha ≥8% eltávolítva; `_crop_tasks.md` generálás + `--sync-crop-tasks` flag (`_crop_tasks.py`) |
| 2026-06-03 | 2.5 | `_crop_tasks.md`: minden katalógus-bejegyzés listázva (nem csak `needs_crop:true`); `[x]/[ ]` checkbox tükrözi `needs_crop`-ot. Caption-mező soronként, auto-detekció `Figure N(.M)?: …` mintával PDF/PPTX szövegből; bizonytalan találatnál `Caption?:` előtag (több caption az oldalon vagy index-mismatch). Sync visszaírja a `Caption:` (NEM `?`-es) szövegeket a `caption` mezőbe. |
| 2026-06-03 | 2.6 | `_crop_tasks.md` formátum: forrásonként markdown táblázat (`✓ \| id \| fájl \| oldal \| útvonal \| Caption`), `·` elválasztó helyett `\|`. Bizonytalan caption jelölése: cella eleji `?` prefix (a megerősítéshez töröld). Sync a táblázat-sorokat parse-olja. |
