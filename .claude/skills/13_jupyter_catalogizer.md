---
name: 13_jupyter_catalogizer
title: 13_jupyter_catalogizer -- A tananyag gazdagítása Jupyter notebook-okkal
type: skill
tags: [meta, skill]
role: 😎+🤖
status: planned
version: 1.1
updated: 2026-06-06
description: A publikálható jegyzet/prezentáció kijelölt ábráihoz/koncepcióihoz kész, animált Jupyter notebookokat rendel Predict–Observe–Explain (POE) struktúrával (nem programozást tanít), és csatolmányként regisztrálja; használd a 08_quality_reviewer PUBLIKÁLHATÓ döntése után, opcionális gazdagító lépésként. Didaktikai metaprompt előtöltve; regiszter-mechanika backlog.
---

# 13_JUPYTER_CATALOGIZER

<!-- A `role` dönti el, hogyan fut a lépés: 🐍 script, 🤖 Claude, 😎+🤖 ember+Claude.
     A skill törzse legyen tömör; nehéz részletek külön fájlba (progresszív feltárás). -->

## 1. Cél

A 😎 által kijelölt ábrákhoz/koncepciókhoz **kész, animált** Jupyter notebookot rendel, köré
**Predict–Observe–Explain (POE)** tanulási struktúrát épít, és a jegyzetben/előadásban
csatolmányként (**📎🧪**) jelöli. A projekt **nem programozást tanít** — a notebook kész animáció,
amelyet a hallgató paraméterez; ezért a klasszikus „Socratic Coding / skeleton code" helyett a
POE-minta illik. A notebookok hosszú távon bővülnek, ezért **külön regiszterben** tartjuk
nyilván — a regiszter-mechanika (fájlnév, csatolás) még **nyitott** (backlog).

**Ez a verzió a didaktikai metapromptot tölti elő; a `status: planned` marad.**

**Input:** publikálható `N_Jegyzet.md` (+ `N_Prezentacio.md`) · **Output:** horgonyzott POE-feladat + (később) regiszter-bejegyzés

## 2. Bemenetek

| Fájl | Honnan (skill) | Tartalom |
|:-----|:---------------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 08_quality_reviewer | Publikálható jegyzet (notebook-jelölés alapja) |
| `4_wip_outputs/N_Prezentacio.md` | 10_presentation_maker | Prezentáció (opcionális, ide is kerülhet csatolmány) |

**Előfeltétel:** `08_quality_reviewer` döntése `PUBLIKÁLHATÓ`. A kimeneti fázisban fut, a 09/10/11-gyel párhuzamosan (opcionális gazdagítás).

## 3. Eljárás

### 3.1. Didaktikai metaprompt (🤖 — előtöltve)

**Olvasandó bemenet:** a publikálható `N_Jegyzet.md` és a 😎 által kijelölt ábra/koncepció.

**POE-minta (Predict–Observe–Explain)** — a kész, animált notebookhoz 3-cellás szerkezet:

1. **Predict (markdown jóslat-cella):** mérnöki kérdés, amelyre a hallgató az animáció előtt
   *megjósolja* a választ (pl. „Mit gondol, mi történik a szállítási nyomással, ha a szivattyú
   fordulatszámát növeljük?"). Ez a *generation effect*-et mozgósítja.
2. **Observe (futtatható animációs cella):** a kész animáció, amelynek paramétereit a hallgató
   állíthatja. **Magyarázat-visszatartás:** a paramétert ő mozgatja, de a *miértet* nem kapja
   készen.
3. **Explain (markdown reflexió-cella):** a hallgató saját szavaival megmagyarázza a jóslata és
   a megfigyelt viselkedés eltérését.

**Rugalmas horgonyzás:** a 😎 kijelölés dönti el, hogy a notebook **szakasz-** (a releváns `##`
`💡 Összegzés` után) vagy **fejezet-szinten** (a `🗺️` után) kerül be.

**Kimenet formátuma (csatolmány-jelölés a jegyzetben):**

```markdown
> 📎🧪 **Interaktív notebook — {koncepció}** [link]
> **Jóslat:** {mérnöki kérdés az animáció előtt}
> **Állítható:** {a hallgató által változtatható paraméter(ek)}
> **Magyarázd meg:** {mit kell a megfigyelés után reflektálnia}
```

**Checkpoint (😎):** a notebook kiválasztása/elkészítése és a horgony helye 😎 jóváhagyással.

### 3.2. Regiszter-mechanika — NYITOTT (backlog)

A notebookok **külön regiszterben** (táblázatos fájl) való nyilvántartása, a fájlnév-konvenció
és a csatolmány stabil hivatkozása még tervezés alatt → [project_status.md](../project_status.md).
Ez a skill addig csak a fenti didaktikai metapromptot szolgáltatja.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `N_.../fajl` | leírás |

## 5. Teszt

Reprodukálható teszteset — minden skillnek legyen (lásd [Instructions §12](../../Instructions.md)).

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
- upstream: [08_quality_reviewer.md](08_quality_reviewer.md) · párhuzamos: [12_youtube_finder.md](12_youtube_finder.md)

## 9. Visszajelzések 😎+🤖

- 💬 A didaktikai metaprompt (§3.1, POE) előtöltve. A **regiszter-mechanika nyitott** (§3.2, backlog).

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-06 | 1.1 | §1 + §3.1 didaktikai metaprompt előtöltve (POE 3-cella: Predict–Observe–Explain, magyarázat-visszatartás, rugalmas horgony) — a Socratic Coding helyett, mert a projekt nem tanít programozást; §3.2 regiszter-mechanika backlogba. `status: planned` marad. |
| YYYY-MM-DD | 1.0 | Létrehozva |
