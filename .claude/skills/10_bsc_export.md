---
name: 10_bsc_export
title: 10_BSC_EXPORT — BSc szűrés és pandoc camera-ready DOCX
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-06-01
description: MSc tartalom kiszűrése és pandoc segítségével DUE arculatú DOCX fájlok generálása BSc és teljes verzióban.
---

# 10_BSC_EXPORT

## 1. Cél

A `4_wip_outputs/N_Jegyzet.md`-ből MSc tartalmak kiszűrésével BSc változatot készít,
majd mindkettőt pandoc segítségével camera-ready DOCX-re konvertálja.

**Input:** `4_wip_outputs/N_Jegyzet.md`
**Output:** `5_clean_outputs/N_Jegyzet.docx` + `5_clean_outputs/N_Jegyzet_bsc.docx`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 07_quality_reviewer | Publikálható minőségű, teljes (BSc+MSc) jegyzet |
| `templates/due_jegyzet_template.docx` | templates/ | DUE arculati sablon |

**Előfeltétel:** `07_quality_reviewer` döntése `PUBLIKÁLHATÓ`; pandoc telepítve; sablon elérhető.

## 3. Eljárás

### 3.1. BSc szűrés

```powershell
python scripts/10-1_bsc_filter.py --week N --subject "Jelatvitel"
```

- `<!-- MSc -->` … `<!-- /MSc -->` blokkok teljes eltávolítása
- `[MSc]` prefix eltávolítása a szövegből
- Output: `4_wip_outputs/N_Jegyzet_bsc_filtered.md` (átmeneti fájl)

### 3.2. Pandoc DOCX export — teljes verzió

```powershell
python scripts/10-2_pandoc_export.py --input "4_wip_outputs/N_Jegyzet.md" `
    --output "5_clean_outputs/N_Jegyzet.docx" `
    --template "templates/due_jegyzet_template.docx" `
    --week N --subject "Jelatvitel"
```

### 3.3. Pandoc DOCX export — BSc verzió

```powershell
python scripts/10-2_pandoc_export.py --input "4_wip_outputs/N_Jegyzet_bsc_filtered.md" `
    --output "5_clean_outputs/N_Jegyzet_bsc.docx" `
    --template "templates/due_jegyzet_template.docx" `
    --week N --subject "Jelatvitel"
```

### 3.4. Átmeneti fájl törlése

```powershell
Remove-Item "4_wip_outputs/N_Jegyzet_bsc_filtered.md"
```

### 3.5. Manuális ellenőrzés

- Mindkét DOCX megnyitható Wordben
- Arculati sablon stílusok érvényesülnek (fejléc, betűtípus)
- LaTeX képletek konvertálódtak (Office Math vagy ábra)
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
| LaTeX képletek nem renderelnek | pandoc nem talál math renderer | `--mathml` vagy `--webtex` flag |
| Sablon stílusok hiányoznak | Template path hibás | Abszolút útvonal megadása |
| BSc-ben maradó MSc tartalom | Regex nem match-el a blokk határon | `10-1_bsc_filter.py` regex-et debug-olni |
| Képek hiányoznak a DOCX-ben | Relatív útvonal a Markdown-ban | `--resource-path` flag pandocnak |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [07_quality_reviewer.md](07_quality_reviewer.md) — upstream
- [Instructions.md](../../Instructions.md) — DUE arculati szabályok

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
