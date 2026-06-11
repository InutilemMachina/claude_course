---
name: 12_youtube_finder
title: 12_youtube_finder -- A tananyag gazdagítása Youtube videókkal
type: skill
tags: [meta, skill]
role: 😎+🤖
status: planned
version: 1.2
updated: 2026-06-11
description: A publikálható jegyzet/prezentáció kijelölt koncepcióihoz Youtube videókat/shortsokat rendel kontextuális horgonnyal + „Nézd és elemezd" feladattal (Mayer CTML + retrieval), és csatolmányként regisztrálja; használd a 08_quality_reviewer PUBLIKÁLHATÓ döntése után, opcionális gazdagító lépésként. Didaktikai metaprompt előtöltve; regiszter-mechanika backlog.
---

# 12_YOUTUBE_FINDER

<!-- A `role` dönti el, hogyan fut a lépés: 🐍 script, 🤖 Claude, 😎+🤖 ember+Claude.
     A skill törzse legyen tömör; nehéz részletek külön fájlba (progresszív feltárás). -->

## 1. Cél

A 😎 által kijelölt koncepciókhoz kontextuálisan **horgonyzott** YouTube-videót/shortot rendel,
köré tanulási feladatot épít (Mayer CTML + retrieval practice), és a jegyzetben/előadásban
csatolmányként (**📎▶**) jelöli. A videók listája később bővül/szűkül, ezért **külön regiszterben**
tartjuk nyilván — a regiszter-mechanika (fájlnév, csatolmány-szintaxis) még **nyitott** (backlog).

**Ez a verzió a didaktikai metapromptot tölti elő; a `status: planned` marad.**

**Input:** publikálható `N_Jegyzet.md` (+ `N_Prezentacio.md`) · **Output:** horgonyzott videó-feladat + (később) regiszter-bejegyzés

## 2. Bemenetek

| Fájl | Honnan (skill) | Tartalom |
|:-----|:---------------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 08_quality_reviewer | Publikálható jegyzet (videó-jelölés alapja) |
| `4_wip_outputs/N_Prezentacio.md` | 10_presentation_maker | Prezentáció (opcionális, ide is kerülhet csatolmány) |

**Előfeltétel:** `08_quality_reviewer` döntése `PUBLIKÁLHATÓ`. A kimeneti fázisban fut, a 09/10/11-gyel párhuzamosan (opcionális gazdagítás).

## 3. Eljárás

### 3.1. Didaktikai metaprompt (🤖 — előtöltve)

**Olvasandó bemenet:** a publikálható `N_Jegyzet.md` és a 😎 által kijelölt koncepció(k).

**Feladat lépésről lépésre:**

1. **Rugalmas horgonyzás:** a 😎 kijelölés dönti el, hogy a videó **szakasz-** (a releváns `##`
   `💡 Összegzés` után) vagy **fejezet-szinten** (a `🗺️` után) kerül-e be. Definiáld pontosan,
   melyik bekezdés/blokk után jelenjen meg — ne csak „valahova" javasolj.
2. **Videó-keresési specifikáció:** adj meg egy pontos **search query**-t és egy **3-pontos
   kritériumrendszert** a beillesztendő videóra (pl. „max 5 perc; animáció, amely a tömegáram
   fluktuációját mutatja; kerüli a komplex képleteket").
3. **„Nézd és elemezd" feladat (retrieval + CTML):** a videó alá 2 irányított kérdés, amelyek
   válasza **kizárólag a videó vizuális eleméből** olvasható ki (ne legyen a jegyzetből
   visszamondható). Adj **time-stamp**-et a megfigyelési pontra (pl. „2:30-nál figyeld a
   tömegáram előjelét") — ez a *segmenting* elv videóra vetítve.

**Kimenet formátuma (csatolmány-jelölés a jegyzetben):**

```markdown
> 📎▶ **Videó — {koncepció}** [link]
> Keresés: `{search query}` · Kritérium: {1}; {2}; {3}
> **Nézd és elemezd** ({mm:ss}-nél):
> 1. {kérdés — csak a videóból válaszolható}
> 2. {kérdés}
```

**Checkpoint (😎):** a konkrét videó kiválasztása és a horgony helye 😎 jóváhagyással.

### 3.2. Regiszter-mechanika — NYITOTT (backlog)

A videók **külön regiszterben** (táblázatos fájl) való nyilvántartása, a csatolmány stabil
hivatkozása és a bővülés/szűkülés kezelése még tervezés alatt → [project_status.md](../project_status.md).
Ez a skill addig csak a fenti didaktikai metapromptot szolgáltatja.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `N_.../fajl` | leírás |

## 5. Teszt

Reprodukálható teszteset — minden skillnek legyen (lásd [Instructions §12](../Instructions.md)).

- **Fixture (bemenet):** melyik anyag — `test_sources/atg` (sok kis forrás) vagy `test_sources/dft` (1 könyv) — és hova kerül (`test_outputs/<tárgy>/N_het/...`).
- **Akció:** a §3 konkrét parancsa / Claude-feladata.
- **Várt kimenet:** a sikeres eredmény (fájl, struktúra, kulcsérték).
- **Eval:** hogyan dől el, hogy jó (`08_quality_check.py`, Claude review, vagy `git diff`).

## 6. Ellenőrzés

- [ ] Ellenőrzési pont 1
- [ ] Ellenőrzési pont 2

## 7. Hibakezelés

<!-- SZABÁLY: Minden felfedezett hibát ÉS megoldást ide kell dokumentálni azonnal.
     Ne hozz létre külön pitfalls fájlt. Ha a hiba más lépést is érint, ott is jegyezd.
     Formátum: tömör táblázat-sor (Tünet | Ok | Megoldás). -->

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| tünet leírása | gyökérok | konkrét megoldás |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- upstream: [08_quality_reviewer.md](08_quality_reviewer.md) · párhuzamos: [13_jupyter_catalogizer.md](13_jupyter_catalogizer.md)

## 9. Visszajelzések 😎+🤖

- 💬 A didaktikai metaprompt (§3.1) előtöltve. A **regiszter-mechanika nyitott** (§3.2, backlog).

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-06 | 1.1 | §1 + §3.1 didaktikai metaprompt előtöltve (rugalmas horgony, keresési spec, „Nézd és elemezd" CTML + time-stamp); §3.2 regiszter-mechanika backlogba. `status: planned` marad. |
| YYYY-MM-DD | 1.0 | Létrehozva |
| 2026-06-11 | 1.2 | role-notáció standardizálva (😎+🤖). |
