---
name: 11_bsc_export
title: 11_BSC_EXPORT — BSc szűrés és pandoc camera-ready DOCX
type: skill
tags: [meta, skill]
role: 🤖->🐍
status: active
version: 1.2
updated: 2026-06-07
description: MSc tartalom kiszűrése és pandoc segítségével DUE arculatú DOCX fájlok generálása BSc és teljes verzióban. A LaTeX képletek NATÍV Word-egyenletként (OMML / Cambria Math, nem kép) — a 10 lépés `_omml.py` elvével konzisztens.
---

# 11_BSC_EXPORT

## 1. Cél

A `4_wip_outputs/N_Jegyzet.md`-ből MSc tartalmak kiszűrésével BSc változatot készít,
majd mindkettőt pandoc segítségével camera-ready DOCX-re konvertálja.

**Input:** `4_wip_outputs/N_Jegyzet.md`
**Output:** `5_clean_outputs/N_Jegyzet.docx` + `5_clean_outputs/N_Jegyzet_bsc.docx`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 08_quality_reviewer | Publikálható minőségű, teljes (BSc+MSc) jegyzet |
| `templates/due_jegyzet_template.docx` | templates/ | DUE arculati sablon |

**Előfeltétel:** `08_quality_reviewer` döntése `PUBLIKÁLHATÓ`; pandoc telepítve; sablon elérhető.

## 3. Eljárás

### 3.1. BSc szűrés

```powershell
python scripts/11-1_bsc_filter.py --week N --subject "Jelatvitel"
```

- `<!-- MSc -->` … `<!-- /MSc -->` blokkok teljes eltávolítása
- `[MSc]` prefix eltávolítása a szövegből
- Output: `4_wip_outputs/N_Jegyzet_bsc_filtered.md` (átmeneti fájl)

### 3.2. Pandoc DOCX export — teljes verzió

```powershell
python scripts/11-2_pandoc_export.py --input "4_wip_outputs/N_Jegyzet.md" `
    --output "5_clean_outputs/N_Jegyzet.docx" `
    --template "templates/due_jegyzet_template.docx" `
    --week N --subject "Jelatvitel"
```

### 3.3. Pandoc DOCX export — BSc verzió

```powershell
python scripts/11-2_pandoc_export.py --input "4_wip_outputs/N_Jegyzet_bsc_filtered.md" `
    --output "5_clean_outputs/N_Jegyzet_bsc.docx" `
    --template "templates/due_jegyzet_template.docx" `
    --week N --subject "Jelatvitel"
```

### 3.3a. Natív egyenletek (OMML / Cambria Math) — kötelező elv

A LaTeX képletek a DOCX-ben **natív, szerkeszthető Word-egyenletek** legyenek (Office Math /
Cambria Math), **SOHA nem kép**. Ez a 10 lépés [`_omml.py`](../../scripts/_omml.py) elvével
egységes — a WordprocessingML a `m:oMath`-ot közvetlenül a bekezdésbe ágyazza, így a `$...$`
**szövegközi**, a `$$...$$` **saját-soros** egyenletként folyik.

- **Pandoc:** a `docx` író a `$...$`/`$$...$$`-t **alapból natív OMML-egyenletté** konvertálja —
  ne add meg a `--webtex` flaget (az **képet** csinál) és kerüld a `--mathml`-t is (a docx-nál
  az OMML a natív). Egyszerűen hagyd a pandoc-ot a forrásbeli `$...$` jelöléssel dolgozni.
- **Egy forrás-konvenció** (`$...$` / `$$...$$` a jegyzetben) → PPTX (10, `_omml.py`) és DOCX (11,
  pandoc) is natív Cambria Math. Ha a pandoc-lánc valamiért nem ad OMML-t, a `_omml.py`
  `tex_to_omath()` közvetlenül is használható a DOCX-bekezdésbe injektálva.

### 3.4. Átmeneti fájl törlése

```powershell
Remove-Item "4_wip_outputs/N_Jegyzet_bsc_filtered.md"
```

### 3.5. Manuális ellenőrzés

- Mindkét DOCX megnyitható Wordben
- Arculati sablon stílusok érvényesülnek (fejléc, betűtípus)
- LaTeX képletek **natív Word-egyenletként** (Office Math / Cambria Math, **NEM kép**) — kattintva szerkeszthetők
- BSc verzióban nincs `[MSc]` szöveg

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `5_clean_outputs/N_Jegyzet.docx` | Teljes (BSc+MSc) camera-ready DOCX |
| `5_clean_outputs/N_Jegyzet_bsc.docx` | BSc-only camera-ready DOCX |

## 5. Ellenőrzés

- [ ] Mindkét DOCX fájl létezik és megnyitható
- [ ] BSc verzióban nincs `<!-- MSc -->` szöveg vagy `[MSc]` prefix
- [ ] Sablon stílusok alkalmazva (nem alapértelmezett Word stílusok)
- [ ] Fejezetek számozása megmarad a DOCX-ben
- [ ] Képek beágyazva (nem hiányzó hivatkozásként)

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `pandoc: command not found` | Pandoc nincs telepítve | `winget install JohnMacFarlane.Pandoc` |
| Képletek **képként** jelennek meg a DOCX-ben | `--webtex`/`--mathjax` flag (képet/HTML-t csinál) | A flag elhagyása — a `docx` író alapból **natív OMML**-t ad; szükség esetén `_omml.py tex_to_omath()` (§3.3a) |
| Képletek nyers `$...$`-ként maradnak | a forrás nem `$`-jelölést használ, vagy a math kiterjesztés ki van kapcsolva | A jegyzetben `$...$`/`$$...$$` jelölés; pandoc `+tex_math_dollars` (alap) |
| Sablon stílusok hiányoznak | Template path hibás | Abszolút útvonal megadása |
| BSc-ben maradó MSc tartalom | Regex nem match-el a blokk határon | `11-1_bsc_filter.py` regex-et debug-olni |
| Képek hiányoznak a DOCX-ben | Relatív útvonal a Markdown-ban | `--resource-path` flag pandocnak |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [08_quality_reviewer.md](08_quality_reviewer.md) — upstream
- [Instructions.md](../../Instructions.md) — DUE arculati szabályok

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (mint 10_bsc_export) |
| 2026-06-03 | 1.1 | Átszámozva 10→11; scriptek 11-1/11-2 |
| 2026-06-07 | 1.2 | §3.3a **natív egyenlet-elv** (OMML / Cambria Math, nem kép) — a 10 `_omml.py`-vel egységes; pandoc alap-OMML (ne `--webtex`); §3.5/§6 frissítve. Forrás-konvenció: `$...$`/`$$...$$` → PPTX+DOCX natív Cambria Math. |
