---
name: 11_docx_export
title: 11_DOCX_EXPORT — Pandoc camera-ready DOCX
type: skill
tags: [meta, skill]
role: 🐍
status: active
version: 2.0
updated: 2026-06-12
description: Publikálható Jegyzet pandoc-alapú camera-ready DOCX konverziója DUE arculattal; natív Word-egyenlet (OMML / Cambria Math, nem kép). Használd a 08_quality_reviewer PUBLIKÁLHATÓ döntése után.
---

# 11_DOCX_EXPORT

## 1. Cél

A `4_wip_outputs/N_Jegyzet.md`-ből pandoc segítségével DUE arculatú camera-ready DOCX-et készít.
A LaTeX képletek NATÍV Word-egyenletként (OMML / Cambria Math, nem kép).

**Input:** `4_wip_outputs/N_Jegyzet.md`
**Output:** `6_clean_outputs/N_Jegyzet.docx`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 08_quality_reviewer | Publikálható minőségű Jegyzet |
| `templates/due_jegyzet_template.docx` | templates/ | DUE arculati sablon |

**Előfeltétel:** `08_quality_reviewer` döntése `PUBLIKÁLHATÓ`; pandoc telepítve; sablon elérhető.

## 3. Eljárás

### 3.1. Pandoc DOCX export

```powershell
python scripts/11-2_pandoc_export.py --week-dir "test_outputs/<tárgy>/N_het"
```

**Automatikus lépések a scriptben:**
- `--toc` (tartalomjegyzék, mélység=3) alapból bekapcsolt; kikapcs.: `--no-toc`
- Mermaid-blokkok PNG-vé renderelése (mmdc; ugyanaz az infrastruktúra mint a 10-1); kikapcs.: `--no-mermaid`
- Template: `templates/due_jegyzet_template.docx`; hiánykor figyelmeztetés + alapstílus
- A script kiírja a template teljes elérési útját (`Template: ...`)

### 3.2. Natív egyenletek (OMML / Cambria Math) — kötelező elv

A LaTeX képletek a DOCX-ben **natív, szerkeszthető Word-egyenletek** legyenek (Office Math /
Cambria Math), **SOHA nem kép**. Ez a 10 lépés [`_omml.py`](../../scripts/_omml.py) elvével egységes.

- **Pandoc:** a `docx` író a `$...$`/`$$...$$`-t **alapból natív OMML-egyenletté** konvertálja —
  ne add meg a `--webtex` flaget (az **képet** csinál) és kerüld a `--mathml`-t is (a docx-nál
  az OMML a natív).
- **Egy forrás-konvenció** (`$...$` / `$$...$$` a jegyzetben) → PPTX (10, `_omml.py`) és DOCX (11,
  pandoc) is natív Cambria Math. Ha a pandoc-lánc valamiért nem ad OMML-t, a `_omml.py`
  `tex_to_omath()` közvetlenül is használható.

### 3.3. Manuális ellenőrzés

- DOCX megnyitható Wordben
- Arculati sablon stílusok érvényesülnek (fejléc, betűtípus)
- LaTeX képletek **natív Word-egyenletként** (Office Math / Cambria Math, **NEM kép**) — kattintva szerkeszthetők

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `6_clean_outputs/N_Jegyzet.docx` | Camera-ready DOCX, DUE arculattal |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het` — `1_Jegyzet.md` + `due_jegyzet_template.docx`.
- **Akció:** `python scripts/11-2_pandoc_export.py --week-dir test_outputs/atg/1_het`
- **Várt kimenet:** `6_clean_outputs/1_Jegyzet.docx` (DUE sablon, natív OMML, beágyazott képek).
- **Eval:** DOCX megnyitható Wordben; §6 ellenőrzőlista.

## 6. Ellenőrzés

- [ ] DOCX létezik és megnyitható
- [ ] Sablon stílusok alkalmazva (nem alapértelmezett Word stílusok)
- [ ] Fejezetek számozása megmarad a DOCX-ben
- [ ] Képek beágyazva (nem hiányzó hivatkozásként)
- [ ] LaTeX képletek natív Word-egyenletként (szerkeszthető, nem kép)

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `pandoc: command not found` | Pandoc nincs telepítve | `winget install JohnMacFarlane.Pandoc` |
| Tartalomjegyzék hiányzik | `--no-toc` flag, vagy régi scriptverzió | Ne add meg a `--no-toc` flagot |
| Mermaid-blokkok kódként jelennek meg | mmdc / node nem elérhető | `WARN mermaid-cli / node nem elérhető` üzenet: `10-1_mermaid_render.py` env-setupja szükséges (project_status B-15) |
| Képletek **képként** jelennek meg a DOCX-ben | `--webtex`/`--mathjax` flag | A flag elhagyása — a `docx` író alapból **natív OMML**-t ad; szükség esetén `_omml.py tex_to_omath()` (§3.2) |
| Képletek nyers `$...$`-ként maradnak | forrás nem `$`-jelölést használ | A jegyzetben `$...$`/`$$...$$` jelölés; pandoc `+tex_math_dollars` (alap) |
| Sablon stílusok hiányoznak | Template path hibás | Abszolút útvonal megadása |
| Képek hiányoznak a DOCX-ben | Relatív útvonal a Markdown-ban | `--resource-path` flag pandocnak |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- [08_quality_reviewer.md](08_quality_reviewer.md) — upstream
- [Instructions.md](../../Instructions.md) — DUE arculati szabályok

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (mint 10_bsc_export) |
| 2026-06-03 | 1.1 | Átszámozva 10→11; scriptek 11-1/11-2 |
| 2026-06-07 | 1.2 | §3.3a **natív egyenlet-elv** (OMML / Cambria Math, nem kép) — a 10 `_omml.py`-vel egységes; pandoc alap-OMML (ne `--webtex`); §3.5/§6 frissítve. |
| 2026-06-11 | 1.3 | §Teszt pótolva (atg/1_het); §5→§10 átszámozva; role 🤖+🐍. |
| 2026-06-12 | 2.0 | MSc-kivezetés (P2.1): 11-1_bsc_filter lépés eltávolítva, BSc-verzió megszűnt; tiszta pandoc DOCX export maradt; `5_clean_outputs`→`6_clean_outputs`; fájl átnevezve `11_bsc_export`→`11_docx_export`; role→🐍. |
