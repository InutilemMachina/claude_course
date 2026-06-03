---
name: 12_youtube_finder
title: 12_youtube_finder -- A tananyag gazdagítása Youtube videókkal
type: skill
tags: [meta, skill]
role: 🤖,😎
status: planned
version: 1.0
updated: 2026-06-03
description: A publikálható jegyzet/prezentáció kijelölt koncepcióihoz Youtube videókat/shortsokat rendel és csatolmányként regisztrálja; használd a 08_quality_reviewer PUBLIKÁLHATÓ döntése után, opcionális gazdagító lépésként.
---

# 12_YOUTUBE_FINDER

<!-- A `role` dönti el, hogyan fut a lépés: 🐍 script, 🤖 Claude, 😎+🤖 ember+Claude.
     A skill törzse legyen tömör; nehéz részletek külön fájlba (progresszív feltárás). -->

## 1. Cél

Egy mondat: Még nem tudom pontosan, de valami olyasmire gondoltam, hogy bizonyos koncepciókat kijelölök a tananyagban, amihez majd külön Youtube shorts-okat vagy Youtube videókat keresünk, továbbá regisztrálja azt retrospektív a tananyagban (jegyzet/előadás), mint egy csatolmányt 📽 és egy külön fájlban táblázatként. Mivel a videók listája később változhat (bővül, szűkül), így ki kell találni, hogy hogyan regisztráljuk azokat.

**Input:** <fő bemenet egy sorban> · **Output:** <fő kimenet egy sorban>

## 2. Bemenetek

| Fájl | Honnan (skill) | Tartalom |
|:-----|:---------------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 08_quality_reviewer | Publikálható jegyzet (videó-jelölés alapja) |
| `4_wip_outputs/N_Prezentacio.md` | 10_presentation_maker | Prezentáció (opcionális, ide is kerülhet csatolmány) |

**Előfeltétel:** `08_quality_reviewer` döntése `PUBLIKÁLHATÓ`. A kimeneti fázisban fut, a 09/10/11-gyel párhuzamosan (opcionális gazdagítás).

## 3. Eljárás

Töltsd ki a `role`-nak megfelelő ágat; a másikat töröld.

### 3.1. Ha 🐍 script-lépés

```powershell
python scripts/NN_xxx.py --subject "<tantárgy>" --week N
```

A parancsnak **léteznie kell és lefutnia** (ne fantom-script). Írd le, mit csinál és mely flag-ekkel.

### 3.2. Ha 🤖 Claude-lépés

- **Olvasandó bemenet:** mely fájl(oka)t olvassa be Claude.
- **Feladat:** mit tegyen, lépésről lépésre (döntési pontok, pl. MSc-jelölés).
- **Kimenet formátuma:** a pontos struktúra/sablon, amit elő kell állítania.
- **Checkpoint (😎):** ha emberi jóváhagyás kell a továbblépéshez.

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

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések.
     Lezárt tétel → Változásjegyzékbe, törlés innen. -->

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| YYYY-MM-DD | 1.0 | Létrehozva |
