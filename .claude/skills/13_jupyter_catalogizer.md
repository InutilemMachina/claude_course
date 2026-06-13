---
name: 13_jupyter_catalogizer
title: 13_jupyter_catalogizer -- A tananyag gazdagítása Jupyter notebook-okkal
type: skill
tags: [meta, skill]
role: 😎+🤖
status: active
version: 2.1
updated: 2026-06-13
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
nyilván — **overlay + regiszter** modell a `5_asset_outputs/`-ban (§3.2, közös a 12-vel).

**Input:** publikálható `N_Jegyzet.md` (+ `N_Prezentacio.md`) · **Output:** regiszter-bejegyzés (`5_asset_outputs/`) + stabil `<!-- ENRICH: <id> -->` horgony a wip-ben

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

**A csatolmány-blokk formátuma (a regiszterben tárolva, lásd §3.2):**

```markdown
> 📎🧪 **Interaktív notebook — {koncepció}** [link]
> **Jóslat:** {mérnöki kérdés az animáció előtt}
> **Állítható:** {a hallgató által változtatható paraméter(ek)}
> **Magyarázd meg:** {mit kell a megfigyelés után reflektálnia}
```

**Checkpoint (😎):** a notebook kiválasztása/elkészítése és a horgony helye 😎 jóváhagyással.

### 3.2. Overlay + regiszter modell (közös a 12-vel)

Ugyanaz az overlay+regiszter mechanizmus, mint a [12_youtube_finder §3.2](12_youtube_finder.md)-ben —
**egy közös** `5_asset_outputs/enrichment_register.md` tartja nyilván a videókat ÉS a notebookokat
(Q-04 megoldása, nincs 6-fájlos visszaírás). A 13 sajátosságai:

- **Típus:** `📎🧪`; **id:** `nb1`, `nb2`, … (a videók `v1`, `v2`).
- **Horgony a wip-ben:** `<!-- ENRICH: nb1 -->` a 😎-kijelölt helyen; a wip egyébként érintetlen.
- **A `meta` mező** a POE-blokk forrásmezőit hordozza (Jóslat / Állítható / Magyarázd meg).
- A notebook-fájl a `5_asset_outputs/`-ban él (vagy külső link); a regiszter-sor `link` mezője mutat rá.

**Életciklus (verziózott újra-export):** közös a 12-vel — a `scripts/_republish.py` kezeli a
negyedéves kört (bump + regiszter-stamp + fizikai archív + `--enrich` újra-export); a 😎 lépés-utasítása
a [subject_working_method.md „Gazdagítási kör"](../../subject_working_method.md)-ben. Részletek:
[12_youtube_finder §3.3](12_youtube_finder.md).

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `5_asset_outputs/enrichment_register.md` | A notebook-bejegyzés (`nb<id>`, link, POE-blokk mezői) — közös regiszter a 12-vel |
| `5_asset_outputs/*.ipynb` | A kész, animált notebook (vagy külső link a regiszterben) |
| `4_wip_outputs/N_Jegyzet.md` (+ `N_Prezentacio*.md`) | `<!-- ENRICH: nb<id> -->` stabil horgony a 😎-kijelölt helyen |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het` — publikálható `1_Jegyzet.md` (📎🧪 kompresszortérkép-koncepció).
- **Akció:** 😎 kijelöl egy ábrát/koncepciót; 🤖 a §3.1 POE-metaprompt szerint notebook-blokkot gyárt,
  majd §3.2 szerint regisztrálja (`nb1` sor a közös `5_asset_outputs/enrichment_register.md`-ben) és
  `<!-- ENRICH: nb1 -->` horgonyt tesz a wip kijelölt helyére.
- **Várt kimenet:** a regiszter tartalmaz egy `nb1` sort (típus 📎🧪, link, POE-meta); a wipben a horgony a helyén.
- **Eval:** §6 ellenőrzőlista; a horgony `<id>`-je 1:1 egyezik a regiszter `id`-jével.

## 6. Ellenőrzés

- [ ] Minden `<!-- ENRICH: nb<id> -->` horgonyhoz pontosan egy regiszter-sor (és fordítva)
- [ ] A notebook elérhető (a regiszter-link érvényes: `5_asset_outputs/*.ipynb` vagy külső URL)
- [ ] A POE-szerkezet teljes (Jóslat + Állítható paraméter + Magyarázd meg)
- [ ] A wip tartalma a horgony-soron kívül érintetlen (camera-ready elv)

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

- 💬 A didaktikai metaprompt (§3.1, POE) előtöltve. A **regiszter-mechanika rögzítve** (§3.2, közös
  overlay+regiszter a 12-vel). A register-aware automatizált horgony-feloldás (10/11) még backlog.

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-06 | 1.1 | §1 + §3.1 didaktikai metaprompt előtöltve (POE 3-cella: Predict–Observe–Explain, magyarázat-visszatartás, rugalmas horgony) — a Socratic Coding helyett, mert a projekt nem tanít programozást; §3.2 regiszter-mechanika backlogba. `status: planned` marad. |
| YYYY-MM-DD | 1.0 | Létrehozva |
| 2026-06-12 | 2.0 | **Véglegesítés (P2.6, 9. döntés):** §3.2 közös overlay+regiszter modell a 12-vel (`5_asset_outputs/enrichment_register.md`, `📎🧪`/`nb<id>`, stabil `<!-- ENRICH: nb<id> -->` horgony; Q-04 megoldása); §4/§5/§6 placeholderek kitöltve; `status: planned → active`. |
| 2026-06-13 | 2.1 | **Életciklus megépítve (B-26):** §3.2 verziózott újra-export pointer (`_republish.py`, közös a 12-vel); a kézi backlog megszűnt. |
