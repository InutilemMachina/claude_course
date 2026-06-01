---
name: 07_quality_reviewer
title: 07_QUALITY_REVIEWER — Minőségellenőrzés és publikálhatóság
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-06-01
description: Script-alapú lint + Claude Explore review; publikálhatóság ≥3/5 esetén 08-10 indul, különben vissza 04-hez.
---

# 07_QUALITY_REVIEWER

## 1. Cél

Automatizált script és Claude review kombináció alapján meghatározza, hogy a WIP jegyzet
publikálható-e, vagy vissza kell küldeni a content synthesizer lépéshez.

**Input:** `4_wip_outputs/N_Jegyzet.md`
**Output:** `4_wip_outputs/N_Review.md` + publikálhatósági döntés

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 06_typesetter | Tipográfiailag normalizált jegyzet |
| `3_mindmap/mindmap.md` | 03_mindmap_builder | Approved mindmap (fedettség-ellenőrzéshez) |

**Előfeltétel:** `06_typesetter` lefutott; `mindmap.md` `status: approved`.

## 3. Eljárás

### 3.1. Automatizált quality check

```powershell
python scripts/07_quality_check.py --week N --subject "Jelatvitel"
```

Ellenőrzési szempontok:
- Fejezet-fedettség: minden mindmap L1 ág jelen van-e?
- Minimum terjedelem: `##` fejezetek legalább 3 bekezdéssel?
- LaTeX hiány: egyetlen képlet sem jelenik meg egy képletintenzív témában?
- Hivatkozások: `citations_seed.json` bejegyzések `[@id]` formában megjelennek-e?
- Összegző dobozok: minden `##` fejezet rendelkezik-e `> 📦` blokkal?

### 3.2. Claude Explore review

Claude értékeli az alábbi 5 szempont szerint (1–5 skálán):

| Szempont | Leírás |
|:---------|:-------|
| **Teljesség** | Minden mindmap L1 ág lefedett? |
| **Mélység** | BSc szintű magyarázat elegendő? Képletek, példák jelen? |
| **Koherencia** | Fejezetek logikusan következnek egymásból? |
| **Forrásintegráció** | Hivatkozások beépítve, nem csak felsorolva? |
| **Olvashatóság** | Tipográfia, tagolás, összegzők rendben? |

Eredmény: **átlag pontszám** (1–5), szöveges indoklással.

### 3.3. Döntési logika

```
Átlag ≥ 3.0 → Publikálható → 08_question_bank + 09_presentation_maker + 10_bsc_export indul
Átlag < 3.0 → Visszaküldés → 04_content_synthesizer kap revision note-ot
```

### 3.4. Review mentése

```
4_wip_outputs/N_Review.md
```

Tartalom: script kimenet + Claude értékelés + döntés + revision note (ha <3.0).

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Review.md` | Részletes minőségi értékelés, döntéssel |

## 5. Ellenőrzés

- [ ] `N_Review.md` tartalmaz numerikus pontszámot minden szempontnál
- [ ] Döntés egyértelmű: `PUBLIKÁLHATÓ` vagy `VISSZAKÜLDÉS`
- [ ] Ha visszaküldés: konkrét revision note-ok a 04-es lépés számára
- [ ] Script kimenet csatolva a review-hoz

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Script `KeyError` a mindmap-nél | Mindmap nem `status: approved` | 03-at lezárni, approved státuszt beállítani |
| Claude pontozás szélsőséges (1-es vagy 5-ös) | Nincs elegendő kontextus | Mindmap és forrásokat is betölteni a reviewhoz |
| `N_Review.md` nem keletkezik | Script crash | Naplót ellenőrizni; manuális review is elfogadható |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [06_typesetter.md](06_typesetter.md) — upstream
- [04_content_synthesizer.md](04_content_synthesizer.md) — visszaküldési cél
- [08_question_bank.md](08_question_bank.md) — downstream (ha publikálható)

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
