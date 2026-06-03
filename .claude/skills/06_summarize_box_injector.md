---
name: 06_summarize_box_injector
title: 06_SUMMARIZE_BOX_INJECTOR — Összegző dobozok
type: skill
tags: [meta, skill]
role: 🤖
status: active
version: 2.0
updated: 2026-06-03
description: Minden `##` alfejezet végére `💡 Összegzés`, minden `#` fejezet zárásánál `🗺️ Fejezet összegfoglalása` blokk in-place beszúrása.
---

# 06_SUMMARIZE_BOX_INJECTOR

## 1. Cél

Az ábrákkal gazdagított jegyzetbe kétszintű összegzést illeszt:

- **Mikroszint** — minden `##` szintű alfejezet végére `💡 Összegzés` blokk.
- **Makroszint** — minden `#` szintű fejezet zárásánál (a `## Hivatkozásjegyzék` előtt) `🗺️ Fejezet összegfoglalása` blokk.

Az ábrabeillesztés külön, megelőző lépés: [05_figure_integrator](05_figure_integrator.md).

**Input:** `4_wip_outputs/N_Jegyzet.md`
**Output:** `4_wip_outputs/N_Jegyzet.md` (összegző blokkokkal, in-place)

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 05_figure_integrator | Ábrákkal gazdagított WIP jegyzet |

**Előfeltétel:** `05_figure_integrator` lefutott.

## 3. Eljárás

### 3.1. `💡 Összegzés` — minden `##` alfejezet végén

A `##` szintű alfejezet utolsó érdemi tartalma (szöveg / képlet / diagram / ábra) után, közvetlenül a következő `##` (vagy `#`) heading előtt:

```markdown
> 💡 **Összegzés — Alfejezet neve**
> **Kulcsgondolat:** [1-2 mondatos lényeg]
> **Kulcsfogalmak:** fogalom1, fogalom2, fogalom3
> **Képletek:** $Eq.X.Y$ — rövid megnevezés (ha van)
```

### 3.2. `🗺️ Fejezet összegfoglalása` — minden `#` fejezet zárásánál

A `#` szintű fejezet utolsó `##` alfejezete (és annak `💡 Összegzés` blokkja) után, a következő `#` heading vagy a `## Hivatkozásjegyzék` előtt:

```markdown
> 🗺️ **Fejezet összegfoglalása — Fejezet címe**
>
> **Fő üzenet:** [2-3 mondat, ami az egész fejezetet összefogja]
>
> **Mit tudsz most:**
> - [3-6 bullet — a fejezet `##` alfejezeteinek kulcsgondolatai egyetlen ívben]
>
> **Kulcsképletek:** $Eq.X.Y$, $Eq.X.Z$ — rövid címkével
>
> **Kapcsolódás:** [hová vezet tovább — következő fejezet/hét, vagy a tárgy egészében hol helyezkedik el]
```

### 3.3. Tartalmi szabályok

- **`💡 Összegzés`** csak az adott `##` alfejezet tartalmát tükrözze — ne vezessen be új fogalmat.
- **`🗺️ Fejezet összegfoglalása`** a `#` alá tartozó `##` alfejezeteket integrálja egyetlen narratívába; mutasson rá a fejezet belső ívére, ne csak ismételje a `💡` blokkokat.
- **Kulcsgondolat / Fő üzenet:** mondatok, nem felsorolás.
- **Kulcsfogalmak:** alfejezetben 3–6, fejezetszinten az ívet visszaadó bullet-lista.
- **Képletek:** csak ténylegesen szereplő `(Eq.X.Y)` jelölésű képletek, rövid megnevezéssel.
- A `## Hivatkozásjegyzék` és a `## Tartalomjegyzék` blokkokba **nem** kerül `💡 Összegzés`.

### 3.4. Idempotencia

A lépés ismételhető: ha már létezik `💡 Összegzés` vagy `🗺️ Fejezet összegfoglalása` blokk az adott heading alatt, azt felülírja (nem duplikálja).

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Jegyzet.md` | `💡 Összegzés` + `🗺️ Fejezet összegfoglalása` blokkokkal kiegészített verzió |

## 5. Ellenőrzés

- [ ] `💡 Összegzés` blokk minden `##` alfejezet végén (a `## Hivatkozásjegyzék` és `## Tartalomjegyzék` kivételével)
- [ ] `🗺️ Fejezet összegfoglalása` blokk minden `#` fejezet zárásánál
- [ ] A blokkok csak az adott szakaszban szereplő fogalmakra / képletekre hivatkoznak
- [ ] A `> 💡` és `> 🗺️` blockquote formátum egységes
- [ ] Nincs duplikáció (idempotencia, §3.4)

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `💡 Összegzés` hiányzik egy `##` alfejezetnél | `##` heading elmaradt a szintézisben | 04 kimenetet javítani, majd újrafuttatni |
| `🗺️` blokk a `## Hivatkozásjegyzék` után került | Heading-felismerés nem szűrte ki | A Hivatkozásjegyzék elé mozgatni; szűrőfeltétel pontosítása |
| Blokk új, szakaszon kívüli fogalmat tartalmaz | Claude túláltalánosított | Tartalom szűkítése a szakasz fogalmaira |
| Blokk duplikáltan jelenik meg | Idempotencia-szabály (§3.4) megsérült | `N_Jegyzet.md` visszaállítás git-ből + újrafuttatás |
| Régi `📦 Összegző` blokkok maradtak vissza | Korábbi (v1.x) kimenet | Manuális csere `💡 Összegzés` / `🗺️ Fejezet összegfoglalása`-ra a §3.1–3.2 sablon szerint |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [05_figure_integrator.md](05_figure_integrator.md) — upstream
- [07_typesetter.md](07_typesetter.md) — downstream

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
-

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-03 | 1.0 | Létrehozva (05_visual_enricher összegző-doboz részéből kiválasztva) |
| 2026-06-03 | 2.0 | `📦 Összegző` (egyetlen `##`-szintű doboz) helyett kétszintű séma: `💡 Összegzés` minden `##` alfejezet végén, `🗺️ Fejezet összegfoglalása` minden `#` fejezet zárásánál; idempotencia-szabály (§3.4) |
