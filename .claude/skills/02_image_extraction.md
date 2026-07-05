---
name: 02_image_extraction
title: 02_image_extraction — Forrás-feldolgozó (MinerU → figure_catalog v4)
type: skill
tags: [meta, skill]
role: 🐍+🤖
status: active
version: 3.1
updated: 2026-06-13
description: MinerU-vel dolgozza fel a PDF forrásokat (PPTX-hez python-pptx), egységes pNNN_figNNN.png néven képeket nyer ki 2_clean_inputs/-ba, és felépíti a figure_catalog.json (v4)-t — caption + text_context + keywords-draft gépileg, MinerU _content_list.json-ból. Használd a 01_source_collector után, a 02b_figure_enricher előtt.
---

# 02_image_extraction

## 1. Cél

A `1_raw_inputs/` forrásokból a **MinerU** kinyeri a képeket `2_clean_inputs/<stem>/images/`-ba
**egységes `pNNN_figNNN.png` névvel**, és felépíti a `figure_catalog.json` (v4) katalógust forrás
szerint csoportosítva. A MinerU `_content_list.json`-jából a script **gépileg kitölti** a
`caption`, `text_context` és `keywords` (draft) mezőket — ez a korábbi regex-alapú detekció
gyökérok-megoldása. A `visual_content` mező `null` marad; azt a 02b_figure_enricher Claude-fázisa tölti.

**Input:** `1_raw_inputs/*.pdf`, `*.pptx` · **Output:** `2_clean_inputs/<stem>/images/` + `figure_catalog.json` (v4)

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `1_raw_inputs/*.pdf` | 01_source_collector | Átnevezett PDF-ek (born-digital és szkennelt) |
| `1_raw_inputs/*.pptx` | 01_source_collector | Átnevezett PPTX előadások |
| `1_raw_inputs/citations.json` | 01_source_collector | Fájlnév → citáció-kulcs (catalog-hoz) |

**Előfeltétel:** **conda `mineru` env** elérhető (lásd §3.1); `python-pptx` telepítve (PPTX-ághoz);
`1_raw_inputs/` nem üres. A MinerU minden PDF-típust kezel (born-digital + szkennelt OCR-rel), így
külön Tesseract-lépés nem kell.

## 3. Eljárás 🐍+🤖

### 3.1. MinerU conda env — reprodukálható setup (egyszeri, kritikus út)

A script a MinerU-t külön conda env-ben hívja (`conda run -n mineru mineru …`), hogy a MinerU
nehéz függőségei (torch, modellek) ne szennyezzék a projekt-env-et. Egyszeri felállítás:

```powershell
conda create -n mineru python=3.11 -y
conda activate mineru
pip install mineru            # a MinerU CLI; modell-letöltés a MinerU saját dokumentációja szerint
mineru --help                 # ellenőrzés: a CLI elérhető
conda deactivate
```

A script a `MINERU_ENV = "mineru"` konstanssal hivatkozik az env-re. GPU-hoz: `--backend
vlm-auto-engine` vagy `--device cuda` (lásd §3.2 flag-ek).

### 3.1a. Javasolt env-struktúra — jövőbeli refaktor (dokumentáció, NEM kötelező)

> ℹ️ Ez **ajánlás**, nem a jelenlegi futtatás előfeltétele. A működő pipeline ma az egyetlen `mineru`
> env-et használja (§3.1). Az alábbi tagolás a függőség-izolációt és a reprodukalhatóságot javítja;
> bevezetése külön, szándékos lépés (ne futtatás közben történjen).

A nehezék (torch/MinerU-modellek) és a könnyű összeállító-lépések szétválasztása négy env-re:

| Env | Szerep | Fő függőségek |
|:----|:-------|:-------------|
| `mineru_env` | A jelenlegi `mineru` env **átnevezve** (kompatibilitási baseline) | `mineru`, torch |
| `extractor_env` | Kinyerés: PDF-eszközök + teljes MinerU | `mineru[all]`, `pymupdf`, PDF-vágó/-kalibráló eszközök (`_pdf_book_split.py` függőségei) |
| `implementer_env` | Összeállítási lépések (07–13: számozás, nav, pandoc/pptx export) | `python-pptx`, `lxml`, `latex2mathml`, pandoc-híd |
| `play_env` | Jupyter notebook generálás / interaktív kísérletezés | `jupyter`, `nbformat` |

**environment.yml ajánlás:** minden env-hez verziózott `environment.yml` (nem ad-hoc `pip install`), hogy a
setup `conda env create -f environment.yml`-lel reprodukálható legyen. A script-oldali env-konstansok
(`MINERU_ENV`) ekkor `mineru_env`/`extractor_env`-re állnak; a lépésenkénti `conda run -n <env>` hívás
izolálja a függőségeket. Bevezetéskor a `02_mineru_to_catalog.py` `MINERU_ENV` konstansa és a
downstream (07–13) script-hívások env-referenciái egységesen frissítendők.

### 3.2. Automatikus futtatás 🐍

```powershell
python scripts/02_mineru_to_catalog.py --week-dir test_outputs/atg/1_het
```

- **Minden PDF** → MinerU dolgozza fel (born-digital és szkennelt egyaránt); a `_content_list.json`-ból
  a script gépileg tölti: `caption` (MinerU image_caption), `text_context` (±3 szomszédos szöveg-entry),
  `keywords` (draft: caption + szakaszcím + top-szavak).
- **PPTX** → `python-pptx` fallback: dia-képek PNG-ként; a dia szövege a `text_context`.
- **Determinisztikus mezők** (`id`, `page`, `path`, `needs_crop`) → script számolja.

**Hasznos flag-ek:** `--source X.pdf` (egy forrás), `--workers N` (párhuzam), `--backend` / `--device`
(GPU), `--no-resume` (MinerU teljes újrafuttatás), `--dry-run` (nem ír fájlt).

### 3.3. Crop-szabály — mit tartsunk benn, mit vágjunk ki

A felirat (`Figure N: …`) **NEM része a vágott képnek**. A `caption` mező strukturált adat; a
downstream lépések (04 jegyzet, 10 MARP, 11 DOCX, 05 figure_integrator) programatikusan illesztik a
felirat-szöveget az ábra mellé. A `needs_crop:true` bejegyzések manuális vágást kérhetnek.

| Tartsd benn | Vágd ki |
|-------------|---------|
| Diagram/grafikon teljes tartalma | `Figure N: <leírás>` aláíró sor |
| Tengely-feliratok (PR, Mass flow) | Oldal-fejléc / lábjegyzet / oldalszám |
| Belső címkék (Surge line, A/B/C pontok) | Az ábra fölötti/alatti bekezdés-szöveg |
| Sub-pane betűk: a), b), c), d) | Brand-fejléc, vízjel |

## 4. Kimenetek

| Fájl/mappa | Tartalom |
|:-----------|:---------|
| `2_clean_inputs/<stem>/images/pNNN_figNNN.png` | Kinyert PNG (egységes naming) |
| `2_clean_inputs/<stem>/mineru/` | MinerU nyers kimenete (`_content_list.json`, layout) |
| `2_clean_inputs/figure_catalog.json` | Ábra-katalóg v4 (`_meta` + `sources` csoportosítva) |

**Fájlnév-konvenció: `pNNN_figNNN.png` mindenhol** (forrástípustól függetlenül). Egy oldalon több
ábra esetén folyamatos `_fig001`, `_fig002`, ... számozás.

**`figure_catalog.json` séma (v4):**

Útmutató a JSON melletti **`CATALOG_GUIDE.md`** fájlban (generált, a 02 script hozza létre a
`2_clean_inputs/` mellé). Tartalmazza: `_` prefix konvenció, 4-állapotú `_status` táblázat, mezők
leírása, example entry.

```json
{
  "_meta": {
    "schema_version": 4,
    "last_updated": "YYYY-MM-DD",
    "_guide": "CATALOG_GUIDE.md"
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

**`_status` derivation (a script számolja, ne szerkeszd kézzel) — 4 állapot:**

| `_status` | Feltétel | Mit jelent |
|-----------|----------|------------|
| `complete` | `caption_verified:true` ÉS `visual_content` kitöltve | Teljesen kész, 05 retrieval használhatja |
| `caption-ok` | `caption_verified:true`, de `visual_content:null` | Caption jóváhagyva, 02b bootstrap hiányzik |
| `draft` | `visual_content` kitöltve, de `caption_verified:false` | 02b futott, 😎 jóváhagyás hiányzik |
| `un-processed` | Sem `caption_verified`, sem `visual_content` | 02b még nem futott |

**Idempotencia szabály (incremental rebuild esetén):**
- Strukturális mezők (`id`, `page`, `path`, `needs_crop`): a script soha nem írja felül a meglévőt; csak fűz új bejegyzést a megfelelő `sources[<src>]["figures"]` listához.
- Meta-mezők (`caption`, `visual_content`, stb.): a script üresen hagyja az új bejegyzéseknél; a meglevő bejegyzések meta-mezőit **érintetlenül hagyja** (a `--no-resume` az egész MinerU-futást indítja újra, de a katalógus meta-mezőit így sem törli).
- `_status`: a `save_catalog` minden mentésnél újraszámolja.

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het/1_raw_inputs/` (PDF + PPTX források).
- **Akció (dry-run):** `python scripts/02_mineru_to_catalog.py --week-dir test_outputs/atg/1_het --dry-run`
- **Várt kimenet (dry-run):** forrásonként a feldolgozandó MinerU-futás kiírva, katalógus nem íródik.
- **Akció (éles):** `python scripts/02_mineru_to_catalog.py --week-dir test_outputs/atg/1_het`
- **Eval:** `figure_catalog.json` valid JSON, `_meta.schema_version == 4`; a `caption`/`text_context`/`keywords`
  mezők gépileg kitöltve (nem `null`/üres) ott, ahol a MinerU adott adatot; minden entry `_status` mezője a 4 érték egyike.

## 6. Ellenőrzés

- [ ] Minden PDF-hez létrejöttek a PNG-k `pNNN_figNNN.png` névvel
- [ ] `figure_catalog.json` valid JSON, séma v4 (`_meta.schema_version == 4`)
- [ ] `caption` / `text_context` / `keywords` (draft) gépileg kitöltve a MinerU-adatból
- [ ] Minden entry-n `_status` érték a 4 érték közül egy (`complete`/`caption-ok`/`draft`/`un-processed`)
- [ ] Új bejegyzések: `visual_content:null`, `notes:[]` alapértékkel
- [ ] Képútvonalak (`path`) létező fájlokra mutatnak
- [ ] Idempotens: újrafuttatás nem duplikál ÉS nem írja felül a meglévő meta-mezőket

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `conda: command not found` / env-hiba | nincs `mineru` conda env | §3.1 setup: `conda create -n mineru …` |
| `mineru: command not found` (env-en belül) | a MinerU CLI nincs telepítve az env-be | `conda activate mineru && pip install mineru` |
| MinerU lassú / OOM CPU-n | nagy PDF, CPU pipeline | `--backend vlm-auto-engine --device cuda` (ha van GPU); vagy `--workers 1` |
| `HIBA: python-pptx nincs telepítve` | Hiányzó csomag (PPTX-ág) | `pip install python-pptx` |
| PPTX → 0 kép | Vektoros/EMF tartalom (nincs PICTURE shape) | Normál; a PPTX szövegét Claude olvassa közvetlenül |
| `needs_crop:true` bejegyzés, de nincs PNG | `--dry-run` volt | Futtasd le `--dry-run` nélkül |
| `HIBA: nem v4 séma` | Régi katalógus | Wipe + regen, vagy manuális migráció |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- upstream: [01_source_collector.md](01_source_collector.md) · downstream: [02b_figure_enricher.md](02b_figure_enricher.md), [03_mindmap_builder.md](03_mindmap_builder.md)
- [05_figure_integrator.md](05_figure_integrator.md) — `figure_catalog.json` szemantikus fogyasztó
- Sprint-háttér: [ocr_lab/decision.md](../sprints/image_rag/ocr_lab/decision.md) (MinerU-first döntés)

## 9. Visszajelzések

- 💬 NOTE: A regex-alapú caption-detekció (PyMuPDF-korszak) szisztematikus hibáit (regex-túlcsordulás,
  fig↔Figure index-csúszás, sortörés-kötőjel) a MinerU `image_caption` + geometriai layout váltja ki —
  ez volt a MinerU-first döntés fő indoka.
- 💬 NOTE: `nagy2023_slides.pptx` típusú PPTX → képek PLACEHOLDER (type=14) shape-ekben; XML-alapú
  (`blipFill`) detektálás kell a python-pptx-ágban (a `shape_type==13` feltétel nem elégséges).

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (MinerU + 02-2 extractor) |
| 2026-06-03 | 2.0–2.6 | PyMuPDF-átállás: szkennelt detektálás, `--source/--pages`, PPTX `blipFill`, vektoros detektálás, auto-crop, `_crop_tasks` |
| 2026-06-04 | 2.9–2.10 | v4 séma + OCR-cache + `pNNN_figNNN.png` egységes naming; `_status` 4-állapotú; `CATALOG_GUIDE.md` generálva. |
| 2026-06-12 | 3.0 | **MinerU-only (P2.3, 4. döntés):** a kanonikus script `02_mineru_to_catalog.py`; PyMuPDF-fallback (`02_image_extraction.py`), `02c_mineru_layout.py` és árva `_crop_tasks.py` törölve; a skill-doksi a standard MinerU-útvonalat írja le (D11); §3.1 conda `mineru` env reprodukálható setup; caption/text_context/keywords gépi kitöltés a MinerU `_content_list.json`-ból; Tesseract-OCR-ág megszűnt (MinerU kezeli a szkennelt PDF-et). |
| 2026-06-13 | 3.1 | §3.1a **javasolt env-struktúra** (dokumentáció, nem kötelező): `mineru`→`mineru_env` átnevezés, külön `extractor_env` (PDF-eszközök + `mineru[all]`), `implementer_env` (07–13 összeállítás), `play_env` (jupyter); `environment.yml`-alapú reprodukálható setup ajánlás. |
