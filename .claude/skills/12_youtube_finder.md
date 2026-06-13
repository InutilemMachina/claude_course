---
name: 12_youtube_finder
title: 12_youtube_finder -- A tananyag gazdagítása Youtube videókkal
type: skill
tags: [meta, skill]
role: 😎+🤖
status: active
version: 2.1
updated: 2026-06-13
description: A publikálható jegyzet/prezentáció kijelölt koncepcióihoz Youtube videókat/shortsokat rendel kontextuális horgonnyal + „Nézd és elemezd" feladattal (Mayer CTML + retrieval), és csatolmányként regisztrálja; használd a 08_quality_reviewer PUBLIKÁLHATÓ döntése után, opcionális gazdagító lépésként. Didaktikai metaprompt előtöltve; regiszter-mechanika backlog.
---

# 12_YOUTUBE_FINDER

<!-- A `role` dönti el, hogyan fut a lépés: 🐍 script, 🤖 Claude, 😎+🤖 ember+Claude.
     A skill törzse legyen tömör; nehéz részletek külön fájlba (progresszív feltárás). -->

## 1. Cél

A 😎 által kijelölt koncepciókhoz kontextuálisan **horgonyzott** YouTube-videót/shortot rendel,
köré tanulási feladatot épít (Mayer CTML + retrieval practice), és a jegyzetben/előadásban
csatolmányként (**📎▶**) jelöli. A videók listája később bővül/szűkül, ezért **külön regiszterben**
tartjuk nyilván — **overlay + regiszter** modell a `5_asset_outputs/`-ban (§3.2).

**Input:** publikálható `N_Jegyzet.md` (+ `N_Prezentacio.md`) · **Output:** regiszter-bejegyzés (`5_asset_outputs/`) + stabil `<!-- ENRICH: <id> -->` horgony a wip-ben

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

**A csatolmány-blokk formátuma (a regiszterben tárolva, lásd §3.2):**

```markdown
> 📎▶ **Videó — {koncepció}** [link]
> Keresés: `{search query}` · Kritérium: {1}; {2}; {3}
> **Nézd és elemezd** ({mm:ss}-nél):
> 1. {kérdés — csak a videóból válaszolható}
> 2. {kérdés}
```

**Checkpoint (😎):** a konkrét videó kiválasztása és a horgony helye 😎 jóváhagyással.

### 3.2. Overlay + regiszter modell (a 6-fájlos visszaírás helyett)

A gazdagítás **overlay-réteg**, nem a kész fájlok patch-elése (Q-04 megoldása). Három elem:

1. **Stabil horgony a wip-ben:** a 😎 által kijelölt helyre egyetlen sor kerül a
   `4_wip_outputs/N_Jegyzet.md`-be (és/vagy `N_Prezentacio*.md`-be): `<!-- ENRICH: <id> -->`
   (pl. `<!-- ENRICH: v1 -->`). A wip tartalma egyébként **érintetlen** marad (camera-ready elv).
2. **Regiszter (`5_asset_outputs/`):** a tényleges csatolmány-blokk a hét közös
   `5_asset_outputs/enrichment_register.md` táblájában él (12 és 13 közösen tölti). Egy sor =
   egy `<id>`. A videó-lista bővülése/szűkülése csak a regisztert érinti, a wip-et nem.
3. **Újrakonvertálás (nem patch):** a `6_clean_outputs` előállításakor a konverzió a
   `<!-- ENRICH: <id> -->` horgonyt a regiszterből oldja fel a látható `> 📎▶ …` blokká. Így a
   kész DOCX/PPTX a wip + regiszterből **újragenerálódik**, nem 6 külön fájlt patchelünk.

**Regiszter-séma** (`5_asset_outputs/enrichment_register.md`):

```markdown
# Gazdagítási regiszter — {tárgy} {N}. hét

| id | típus | horgony (wip hely) | koncepció | link | meta | verzió | dátum | állapot |
|----|-------|--------------------|-----------|------|------|--------|-------|---------|
| v1 | 📎▶ | §2.3 | tömegáram-fluktuáció | https://youtu.be/… | Keresés: `…`; Krit: … | 1.1 | 2026-09-15 | ✅ |
```

- `id`: stabil (`v1`, `v2`, … videóhoz; `nb1`, … notebookhoz — 13). **Soha nem változik** (a horgony
  emiatt stabil; egy link-csere csak a `link` cellát írja át, az `id`-t nem).
- `verzió` / `dátum`: melyik termék-kiadásban (és mikor) került be — a `_republish.py` tölti automatikusan.
- `állapot`: ⚙️ keresés alatt · ✅ jóváhagyott link · ❌ elvetve. A `meta` a §3.1 blokk forrásmezőit hordozza.

### 3.3. Életciklus — verziózott újra-export (a `6_clean` reconversion)

A gazdagítás **időben bővül** (negyedéves körök). Egy kör mechanizált, a 😎 lépés-utasítása a
[subject_working_method.md „Gazdagítási kör"](../../subject_working_method.md) szekcióban. A gépi rész:

- **Horgony-feloldás:** a `_enrich_util.resolve_anchors` a `<!-- ENRICH: <id> -->`-t a látható blokká
  oldja (csak `✅` sorok); a `11-2_pandoc_export.py --enrich` és `10_pptx_gyarto.py --enrich` ezt hívja.
- **Verziózás + archív:** a `scripts/_republish.py --week-dir <hét>` egy körben: bump (MINOR),
  regiszter-stamp (új `✅` sorok `verzió`+`dátum`), a meglévő `6_clean` termék **archiválása**
  (`6_clean_outputs/archive/{N}_…_v{előző}.…`), majd újra-export `--enrich`-csel.
- **Verziójegyzék:** a DOCX végére a regiszterből generált `## Verziójegyzék` kerül
  (pl. `v1.1 (2026-09-15): +2 📎▶ (§2.3, §3.1), +1 📎🧪 (§4.2)`).

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `5_asset_outputs/enrichment_register.md` | A videó-bejegyzés (id, link, keresés/kritérium, „Nézd és elemezd" blokk) |
| `4_wip_outputs/N_Jegyzet.md` (+ `N_Prezentacio*.md`) | `<!-- ENRICH: <id> -->` stabil horgony a 😎-kijelölt helyen |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het` — publikálható `1_Jegyzet.md` (📎▶ kompresszortérkép-koncepció).
- **Akció:** 😎 kijelöl egy koncepciót; 🤖 a §3.1 metaprompt szerint videó-blokkot gyárt, majd §3.2
  szerint regisztrálja (`v1` sor a `5_asset_outputs/enrichment_register.md`-ben) és `<!-- ENRICH: v1 -->`
  horgonyt tesz a wip kijelölt helyére.
- **Várt kimenet:** a regiszter tartalmaz egy `v1` sort (típus 📎▶, link, meta); a wipben a horgony a helyén.
- **Eval:** §6 ellenőrzőlista; a horgony `<id>`-je 1:1 egyezik a regiszter `id`-jével.

## 6. Ellenőrzés

- [ ] Minden `<!-- ENRICH: <id> -->` horgonyhoz pontosan egy regiszter-sor (és fordítva)
- [ ] A regiszter-link érvényes, kattintható videó-URL
- [ ] A „Nézd és elemezd" kérdések **csak a videóból** válaszolhatók (nem a jegyzetből)
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
- upstream: [08_quality_reviewer.md](08_quality_reviewer.md) · párhuzamos: [13_jupyter_catalogizer.md](13_jupyter_catalogizer.md)

## 9. Visszajelzések 😎+🤖

- 💬 A didaktikai metaprompt (§3.1) előtöltve. A **regiszter-mechanika rögzítve** (§3.2, overlay +
  `5_asset_outputs/enrichment_register.md`). A register-aware automatizált horgony-feloldás a
  konverzióban (10/11) még backlog — addig a 😎 kézzel illeszt a regiszterből.

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-06 | 1.1 | §1 + §3.1 didaktikai metaprompt előtöltve (rugalmas horgony, keresési spec, „Nézd és elemezd" CTML + time-stamp); §3.2 regiszter-mechanika backlogba. `status: planned` marad. |
| YYYY-MM-DD | 1.0 | Létrehozva |
| 2026-06-11 | 1.2 | role-notáció standardizálva (😎+🤖). |
| 2026-06-12 | 2.0 | **Véglegesítés (P2.6, 9. döntés):** §3.2 overlay+regiszter modell (`5_asset_outputs/enrichment_register.md` + stabil `<!-- ENRICH: <id> -->` horgony; 6_clean újrakonvertál, nem patchel — Q-04 megoldása); §4/§5/§6 placeholderek kitöltve; `status: planned → active`. A register-aware konverzió (10/11) backlog. |
| 2026-06-13 | 2.1 | **Életciklus megépítve (B-26):** regiszter-séma +`verzió`/`dátum`; §3.3 verziózott újra-export (`_republish.py`: bump + stamp + fizikai archív + `--enrich`); `## Verziójegyzék` a DOCX-be. A kézi backlog megszűnt. |
