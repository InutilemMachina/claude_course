---
name: NN_skill_name
title: NN_SKILL_NAME -- Rövid cím
type: skill
tags: [meta, skill]
role: 🐍 | 🤖 | 😎+🤖
status: active
version: 1.0
updated: YYYY-MM-DD
description: <Mit csinál a lépés>; használd, amikor <konkrét trigger / bemenet áll elő>. Triggerelő mondat (mi + mikor), nem csak „miről szól". Pl.: „PDF/URL forrásokat rendez 1_raw_inputs/-ba és citations.json-t hoz létre; használd a 00_init után, új heti forrásgyűjtéskor."
---

# NN_SKILL_NAME

<!-- A `role` dönti el, hogyan fut a lépés: 🐍 script, 🤖 Claude, 😎+🤖 ember+Claude.
     A skill törzse legyen tömör; nehéz részletek külön fájlba (progresszív feltárás). -->

## 1. Cél

Egy mondat: mi a lépés feladata.

**Input:** <fő bemenet egy sorban> · **Output:** <fő kimenet egy sorban>

## 2. Bemenetek

| Fájl | Honnan (skill) | Tartalom |
|:-----|:---------------|:---------|
| `N_.../fajl` | előző lépés | leírás |

**Előfeltétel:** Mi kell teljesülni a futtatáshoz?

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
- **Eval:** hogyan dől el, hogy jó (`07_quality_check.py`, Claude review, vagy `git diff`).

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
- upstream: [NN_előző.md](NN_prev.md) · downstream: [NN_következő.md](NN_next.md)

## 9. Visszajelzések 😎+🤖

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések.
     Lezárt tétel → Változásjegyzékbe, törlés innen. -->

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| YYYY-MM-DD | 1.0 | Létrehozva |
