---
name: 09_presentation_maker
title: 09_PRESENTATION_MAKER — MARP prezentáció és PPTX generálás
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-06-01
description: Approved mindmap és végleges jegyzet alapján MARP Markdown prezentáció és PPTX fájl generálása.
---

# 09_PRESENTATION_MAKER

## 1. Cél

A végleges jegyzetből és az approved mindmap-ből MARP-kompatibilis prezentációt generál,
majd `09_pptx_gyarto.py`-val PPTX-re konvertálja.

**Input:** `4_wip_outputs/N_Jegyzet.md` + `3_mindmap/mindmap.md`
**Output:** `4_wip_outputs/N_Prezentacio.md` + `5_clean_outputs/N_Prezentacio.pptx`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 07_quality_reviewer | Publikálható minőségű jegyzet |
| `3_mindmap/mindmap.md` | 03_mindmap_builder | Approved mindmap, navigátor diához |
| `2_clean_inputs/figure_catalog.json` | 02_source_extractor | Ábrák diákba illesztéséhez |

**Előfeltétel:** `07_quality_reviewer` döntése `PUBLIKÁLHATÓ`; MARP CLI telepítve.

## 3. Eljárás

### 3.1. MARP Markdown generálása

Claude generálja a `N_Prezentacio.md`-t az alábbi szabályok szerint:

**Dia-struktúra:**

```markdown
---
marp: true
theme: default
paginate: true
---

# {Tantárgy} — {N}. hét
## {Téma neve}

---

<!-- Dia 2: Navigátor mindmap -->
## Áttekintés

\`\`\`mermaid
flowchart LR
    [teljes mindmap másolata ide]
\`\`\`

---

## {L1 Ág 1}

- Kulcspont 1
- Kulcspont 2

\`\`\`mermaid
[vagy ábra]
\`\`\`

---
```

**Kötelező szabályok:**
- **2. dia = navigátor mindmap** — a teljes `flowchart LR` Mermaid blokk
- **Minden dián 1 Mermaid diagram VAGY 1 ábra** — kötelező vizuális elem
- Szöveg: max 5 bullet point / dia, max 10 szó / bullet
- Képletek: `$$...$$` MARP LaTeX blokkban
- Diák száma: tipikusan `(mindmap L1 ágak × 3) + 2` (cím + navigátor)

### 3.2. PPTX generálás

```powershell
python scripts/09_pptx_gyarto.py --week N --subject "Jelatvitel"
```

- MARP CLI-vel konvertál: `marp N_Prezentacio.md --pptx`
- Output: `5_clean_outputs/N_Prezentacio.pptx`
- Ellenőrzés: slide count, képek beágyazva

### 3.3. Manuális ellenőrzés

- Minden dián van vizuális elem?
- Navigátor dia (2.) érthető és teljes?
- PPTX megnyitható PowerPointban?

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Prezentacio.md` | MARP Markdown, minden dián vizuális elemmel |
| `5_clean_outputs/N_Prezentacio.pptx` | Végleges PowerPoint |

## 5. Ellenőrzés

- [ ] 2. dia tartalmazza a teljes navigátor mindmapet
- [ ] Minden dia rendelkezik Mermaid blokkkal VAGY ábrabeillesztéssel
- [ ] PPTX megnyitható és olvasható
- [ ] Dia-szám ésszerű (nem több mint 40 dia / hét)
- [ ] LaTeX képletek rendereltek a PPTX-ben

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| MARP `Parse error` Mermaid blokknál | Speciális karakter a mindmapben | Mindmap-ben: `"`, `'`, `()` cseréje |
| PPTX képek hiányoznak | Relatív útvonal a MARP-ban | Abszolút útvonalak vagy `--allow-local-files` flag |
| Túl sok szöveg egy dián | Claude nem tartotta a 5-bullet szabályt | Manuálisan rövidíteni vagy diát kettéosztani |
| `marp: command not found` | MARP CLI nincs telepítve | `npm install -g @marp-team/marp-cli` |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [07_quality_reviewer.md](07_quality_reviewer.md) — upstream
- [03_mindmap_builder.md](03_mindmap_builder.md) — navigátor dia forrása

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
