---
name: 09b_moodle_export
title: 09b_MOODLE_EXPORT — Kérdésbank → Moodle XML konverzió
type: skill
tags: [meta, skill]
role: 🐍
status: planned
version: 1.3
updated: 2026-06-12
description: N_Kerdesbank.md → Moodle XML konverzió. Heti vagy aggregált mód, --no-explanation kapcsoló. Script: scripts/09b_moodle_export.py
---

# 09b_MOODLE_EXPORT

## 1. Cél

A `N_Kerdesbank.md` (emberi forrás) Moodle-kompatibilis XML-lé alakítása.
Szűrhető magyarázat-megjelenítés szerint.
Futtatható hetente vagy az összes hétre aggregáltan (vizsgaidőszak előtt).

**Input:** `4_wip_outputs/N_Kerdesbank.md` (egy vagy több hét)
**Output:** `6_clean_outputs/N_Kerdesbank.xml` (heti) / `6_clean_outputs/vizsgabank.xml` (aggregált)

## 2. Script hívása

```bash
# Heti export, magyarázattal
python scripts/09b_moodle_export.py --subject atg --week 1

# Heti export, magyarázat nélkül
python scripts/09b_moodle_export.py --subject atg --week 1 --no-explanation

# Aggregált export — összes hét (vizsgaidőszak előtt)
python scripts/09b_moodle_export.py --subject atg --aggregate
```

### 2.1 Paraméterek

| Paraméter | Értékek | Leírás |
|:----------|:--------|:-------|
| `--subject` | pl. `atg` | Tantárgy neve (könyvtár) |
| `--week N` | egész szám | Adott hét kérdésbankját dolgozza fel |
| `--aggregate` | flag | Összes hét `N_Kerdesbank.md`-ját összevonja |
| `--no-explanation` | flag | Kihagyja a magyarázatot a Moodle-feedbackből |

## 3. Bemenet-értelmezés (parsing)

A script a `N_Kerdesbank.md` struktúráját olvassa:

```
## {L1 szekció}           → Moodle kategória-tag
**K{N}.** `(2-5)` {kérdés}   → question text + tag-ek
→ *N_Jegyzet: §...*       → nem kerül Moodle-ba (belső review-mező)
A) / B) / C) / D)         → answer choice-ok
> *Helyes: {X} — ...*     → correct answer azonosítás + feedback szöveg
```

**Magyarázat:**
- alapértelmezés: `generalfeedback` = a `> *Helyes: ...*` szövege
- `--no-explanation`: `generalfeedback` üres

## 4. Moodle XML séma

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
  <question type="multichoice">
    <name>
      <text>K{N} — {tantárgy} {hét}. hét</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[{kérdés szövege}]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text><![CDATA[{magyarázat — üres ha --no-explanation}]]></text>
    </generalfeedback>
    <defaultgrade>1</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <correctfeedback format="html"><text>Helyes!</text></correctfeedback>
    <partiallycorrectfeedback format="html"><text></text></partiallycorrectfeedback>
    <incorrectfeedback format="html"><text>Helytelen.</text></incorrectfeedback>
    <answer fraction="100" format="html">
      <text><![CDATA[{helyes válasz szövege}]]></text>
      <feedback format="html"><text></text></feedback>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[{hibás válasz szövege}]]></text>
      <feedback format="html"><text></text></feedback>
    </answer>
    <!-- további hibás válaszok -->
    <tags>
      <tag><text>depth:{2|3|4|5}</text></tag>
      <tag><text>L1:{szekció neve}</text></tag>
      <tag><text>week:{N}</text></tag>
    </tags>
  </question>
  <!-- további kérdések -->
</quiz>
```

**Tagek magyarázata:**
- `depth:N` → nehézségi szint szerinti szűrés vizsgán
- `L1:{szekció}` → témakör szerinti szűrés
- `week:N` → hét szerinti szűrés aggregált bankban

## 5. Kimenetek

| Fájl | Mód | Tartalom |
|:-----|:----|:---------|
| `6_clean_outputs/N_Kerdesbank.xml` | heti | Adott hét kérdésbankja Moodle XML-ben |
| `6_clean_outputs/vizsgabank.xml` | aggregált | Összes hét kérdésbankja összevonva |

## 6. Ellenőrzés

- [ ] XML well-formed (xmllint vagy Python `xml.etree.ElementTree` parse)
- [ ] Kérdések száma egyezik a `.md` szűrt kérdésszámával
- [ ] Minden kérdésnél pontosan 1 `fraction="100"` answer
- [ ] Tagek kitöltve minden kérdésnél
- [ ] `--no-explanation` esetén `generalfeedback` valóban üres

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Parse hiba | kérdés-blokk nem zárult le | `.md` manuális ellenőrzése, `09_question_bank` §6 |
| Helyes válasz nem azonosítható | `> *Helyes: X*` sor formátuma eltér | Regex lazítása vagy `.md` manuális javítása |
| Üres XML | nincs kérdés a `.md`-ben | Ellenőrizni a `**K{N}.**` tageket a `.md`-ben |
| Kétszer annyi kérdés aggregáltban | Dupla futtatás | Script idempotens legyen: XML újraírja, nem appendálja |

## 8. Nyitott kérdések

| # | Kérdés | Állapot |
|:--|:-------|:--------|
| Q1 | **Képlet-renderelés:** Moodle számos math-motort támogat (MathJax `\(...\)`, TeX-filter `$$...$$`, MathML). Nem tudni, melyiket konfigurálja az adott intézmény. **Javaslat:** `--math-format` paraméter a scriptbe (`latex` / `mathjax` / `tex-filter` / `strip`); default: `latex` (változatlanul hagyja a `$...$` jelölést, a Moodle-adminnak kell a MathJax-szűrőt bekapcsolni). Addig, amíg ez tisztázatlan, a képletet tartalmazó kérdések XML-exportja kockázatos. | ❔ tisztázandó intézményi Moodle-konfiggal |

## 9. Hivatkozások

- [09_question_bank.md](09_question_bank.md) — upstream, a `.md` forrás spec-je
- [pipeline.md](../pipeline.md) — §2 kimeneti fázis
- [Instructions.md](../../Instructions.md) — §6 mappastruktúra

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-07 | 1.0 | Létrehozva: markdown-first Moodle-export spec, heti+aggregált mód, BSc/MSc+depth tagek |
| 2026-06-11 | 1.1 | status: active → planned (a `09b_moodle_export.py` még nem létezik — őszinte spec); §9/§10 (Hivatkozások/Változásjegyzék) számozás rendezve. |
| 2026-06-12 | 1.2 | MSc-kivezetés (P2.1): `--level bsc/msc` és BSc/MSc szintszűrés eltávolítva; parsing formátumból `(BSc|MSc)` törölve; XML-tagekből BSc/MSc törölve. Mappa-migráció (P2.2): XML-kimenet `5_clean_outputs` → `6_clean_outputs`. |
| 2026-06-12 | 1.3 | Névkonvenció (P2.7, 10. döntés): a planned script `09-1_moodle_export.py` → `09b_moodle_export.py` (1:1 a skill nevével; Instructions §5.1 betűs-alskill szabály). `status: planned` marad. |
