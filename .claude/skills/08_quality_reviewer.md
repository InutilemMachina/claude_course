---
name: 08_quality_reviewer
title: 08_QUALITY_REVIEWER — Minőségellenőrzés és publikálhatóság
type: skill
tags: [meta, skill]
role: 🤖,😎
status: active
version: 1.2
updated: 2026-06-03
description: Script-alapú lint + Claude Explore review; publikálhatóság ≥3/5 esetén 09-13 indul, különben vissza 04-hez.
---

# 08_QUALITY_REVIEWER

## 1. Cél

Automatizált script és Claude review kombináció alapján meghatározza, hogy a WIP jegyzet
publikálható-e, vagy vissza kell küldeni a content synthesizer lépéshez.

**Input:** `4_wip_outputs/N_Jegyzet.md`
**Output:** `4_wip_outputs/N_Review.md` + publikálhatósági döntés

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 07_typesetter | Tipográfiailag normalizált jegyzet |
| `3_mindmap/mindmap.md` | 03_mindmap_builder | Approved mindmap (fedettség-ellenőrzéshez) |

**Előfeltétel:** `07_typesetter` lefutott; `mindmap.md` `status: approved`.

## 3. Eljárás

### 3.1. Automatizált quality check

```powershell
python scripts/08_quality_check.py --week N --subject "Jelatvitel"
```

Ellenőrzési szempontok:
- Fejezet-fedettség: minden mindmap L1 ág jelen van-e?
- Minimum terjedelem: `##` fejezetek legalább 3 bekezdéssel?
- LaTeX hiány: egyetlen képlet sem jelenik meg egy képletintenzív témában?
- Hivatkozások: a `citations.json` bejegyzések `[1]`, `[2]` formában megjelennek-e?
- Összegző blokkok: minden `##` alfejezet végén van-e `> 💡 Összegzés` blokk, és minden `#` fejezet zárásánál `> 🗺️ Fejezet összegfoglalása` blokk? (formátum: [06_summarize_box_injector](06_summarize_box_injector.md) §3.1–3.2)

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
Átlag ≥ 3.0 → Publikálható → 09_question_bank + 10_presentation_maker + 11_bsc_export
                              (+ 12_youtube_finder, 13_jupyter_catalogizer opcionális) indul
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
- [07_typesetter.md](07_typesetter.md) — upstream
- [04_content_synthesizer.md](04_content_synthesizer.md) — visszaküldési cél
- [09_question_bank.md](09_question_bank.md) — downstream (ha publikálható)

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
- ⚡ HIBA: a `08_quality_check.py` a citációkat `<sup>[N]</sup>`-ként számolja, de a kanonikus formátum `[N]` (Instructions §8) — a „Kevés citáció" figyelmeztetés false negatív. Számláló bővítendő `\[\d+\]`-re. (project_status B-12)

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (mint 07_quality_reviewer) |
| 2026-06-03 | 1.1 | Átszámozva 07→08; downstream 09–13, script 08_quality_check.py |
| 2026-06-03 | 1.2 | §3.1 összegző-doboz check átírva a kétszintű sémára (`💡 Összegzés` per `##`, `🗺️ Fejezet összegfoglalása` per `#`) |
