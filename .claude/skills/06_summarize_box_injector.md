---
name: 06_summarize_box_injector
title: 06_SUMMARIZE_BOX_INJECTOR — Összegző dobozok
type: skill
tags: [meta, skill]
role: 🤖
status: active
version: 2.3
updated: 2026-06-11
description: Minden `##` alfejezet végére `💡 Összegzés`, minden `#` fejezet zárásánál `🗺️ Fejezet összegfoglalása`, minden `##` fejezet zárásánál `❔ Ellenőrizd magad` retrieval-kérdés (válaszok a `🔑 Megoldókulcs` szekcióban) in-place beszúrása.
---

# 06_SUMMARIZE_BOX_INJECTOR

## 1. Cél

Az ábrákkal gazdagított jegyzetbe kétszintű összegzést illeszt:

- **Mikroszint** — minden `##` szintű alfejezet végére `💡 Összegzés` blokk.
- **Makroszint** — minden `#` szintű fejezet zárásánál (a `## Hivatkozásjegyzék` előtt) `🗺️ Fejezet összegfoglalása` blokk.
- **Retrieval** — minden `##` fejezet zárásánál `❔ Ellenőrizd magad` kérdés-blokk a `💡` elé; a válaszok elkülönítve a `## 🔑 Megoldókulcs` szekcióban (dokumentum vége).

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

### 3.3. `❔ Ellenőrizd magad` + `🔑 Megoldókulcs` — retrieval practice

**Kérdés-blokk** minden `##` fejezet zárásánál, közvetlenül a fejezet `💡 Összegzés` blokkja
**elé** (a tanuló előbb előhív, csak utána látja a konszolidált összegzést):

```markdown
> ❔ **Ellenőrizd magad — N. Fejezet neve**
>
> 1. [Előhívásra kényszerítő kérdés — emlékezetből, nem visszaolvasással.]
>
> 2. [Akár több kérdés a fejezet kulcsfogalmaira / képleteire.]
```

⚠️ **Formátum-szabály (blockquote-integritás):** a blockquote-on belül **minden
tartalmi sort `>` üres sor válasszon el** — a számozott kérdéseket és a `🧱 Előfeltételek`
bulletjeit is. Ha két `>` tartalmi sor `>` üres sor nélkül követi egymást, a renderelők egy része
külön blockquote-okra darabolja a blokkot. A folyó prózát (pl. `🔭 A Nagykép`) egyetlen `>` sorba
írd, ne tördeld kézzel.

A **válasz itt nem jelenik meg.** A válaszok elkülönítve, a dokumentum végén (a
`## Hivatkozásjegyzék` **elé**) gyűlnek össze egyetlen szekcióban, fejezetenként, a
kérdés-számozáshoz igazítva:

```markdown
## 🔑 Megoldókulcs

**1. Fejezet neve**
1. [Válasz az 1. kérdésre — tömör, de teljes.]
2. [Válasz a 2. kérdésre.]

**2. Fejezet neve**
1. …
```

Így a kérdés és a válasz térben elkülönül → a retrieval practice megmarad (nincs spoiler az
olvasás közben). A kérdés→válasz párosítás a fejezetnév + sorszám alapján egyértelmű.

### 3.4. Tartalmi szabályok

- **`💡 Összegzés`** csak az adott `##` alfejezet tartalmát tükrözze — ne vezessen be új fogalmat.
- **`🗺️ Fejezet összegfoglalása`** a `#` alá tartozó `##` alfejezeteket integrálja egyetlen narratívába; mutasson rá a fejezet belső ívére, ne csak ismételje a `💡` blokkokat.
- **Kulcsgondolat / Fő üzenet:** mondatok, nem felsorolás.
- **Kulcsfogalmak:** alfejezetben 3–6, fejezetszinten az ívet visszaadó bullet-lista.
- **Képletek:** csak ténylegesen szereplő `(Eq.X.Y)` jelölésű képletek, rövid megnevezéssel.
- A `## Hivatkozásjegyzék`, `## Tartalomjegyzék` és `## 🔑 Megoldókulcs` blokkokba **nem** kerül `💡 Összegzés`, `🗺️` vagy `❔` blokk.
- **`❔ Ellenőrizd magad`:** előhívásra kényszerítő kérdés (emlékezetből), nem visszaolvasásra; a válasz kizárólag a `🔑 Megoldókulcs`-ban. A kérdések a fejezet kulcsfogalmait / képleteit célozzák.

### 3.5. Idempotencia

A lépés ismételhető: ha már létezik `💡 Összegzés`, `🗺️ Fejezet összegfoglalása` vagy
`❔ Ellenőrizd magad` blokk az adott heading alatt — vagy `## 🔑 Megoldókulcs` szekció a
dokumentumban —, azt felülírja (nem duplikálja).

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Jegyzet.md` | `💡 Összegzés` + `🗺️ Fejezet összegfoglalása` blokkokkal kiegészített verzió |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het` — `1_Jegyzet.md` (szintetizált, ábrákkal).
- **Akció:** §3 — `💡 Összegzés` / `🗺️ Fejezet összegfoglalása` / `❔ Ellenőrizd magad` + `🔑 Megoldókulcs` injektálása.
- **Várt kimenet:** Minden `##` végén 💡, minden `#` zárásánál 🗺️, dokumentumvégi 🔑.
- **Eval:** §6 ellenőrzőlista + idempotencia (újrafuttatás 0 duplikátum).

## 6. Ellenőrzés

- [ ] `💡 Összegzés` blokk minden `##` alfejezet végén (a `## Hivatkozásjegyzék` és `## Tartalomjegyzék` kivételével)
- [ ] `🗺️ Fejezet összegfoglalása` blokk minden `#` fejezet zárásánál
- [ ] `❔ Ellenőrizd magad` kérdés-blokk minden `##` fejezet zárásánál, a `💡` elé
- [ ] `## 🔑 Megoldókulcs` szekció a dokumentum végén, a `## Hivatkozásjegyzék` elé, fejezetenként
- [ ] A `🔑`-ban minden `❔` kérdéshez van válasz (fejezetnév + sorszám egyezik); a kérdés-blokk válasz nélküli
- [ ] A blokkok csak az adott szakaszban szereplő fogalmakra / képletekre hivatkoznak
- [ ] A `> 💡`, `> 🗺️`, `> ❔` blockquote formátum egységes
- [ ] Nincs duplikáció (idempotencia, §3.5)

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `💡 Összegzés` hiányzik egy `##` alfejezetnél | `##` heading elmaradt a szintézisben | 04 kimenetet javítani, majd újrafuttatni |
| `🗺️` blokk a `## Hivatkozásjegyzék` után került | Heading-felismerés nem szűrte ki | A Hivatkozásjegyzék elé mozgatni; szűrőfeltétel pontosítása |
| Blokk új, szakaszon kívüli fogalmat tartalmaz | Claude túláltalánosított | Tartalom szűkítése a szakasz fogalmaira |
| Blokk duplikáltan jelenik meg | Idempotencia-szabály (§3.5) megsérült | `N_Jegyzet.md` visszaállítás git-ből + újrafuttatás |
| `❔` kérdés a választ is tartalmazza | Spoiler — a válasz a kérdés-blokkban maradt | Válasz áthelyezése a `🔑 Megoldókulcs`-ba; a `❔` csak kérdés |
| `🔑 Megoldókulcs` hiányzik / nem párosítható | Szekció kimaradt vagy a számozás csúszott | Szekció pótlása a `## Hivatkozásjegyzék` elé; fejezetnév + sorszám szinkron a `❔` blokkokkal |
| `❔` / `🧱` blokk a 07 typesetter után külön blockquote-okra esett | A listaelemek `>` üres sor nélkül követték egymást (Rule D valódi üres sort szúrt be) | Minden `>` tartalmi sort `>` üres sorral elválasztani (§3.3 formátum-szabály); a `🔑` szekció normál markdown, ezt nem érinti |
| Régi `📦 Összegző` blokkok maradtak vissza | Korábbi (v1.x) kimenet | Manuális csere `💡 Összegzés` / `🗺️ Fejezet összegfoglalása`-ra a §3.1–3.2 sablon szerint |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- [05_figure_integrator.md](05_figure_integrator.md) — upstream
- [07_typesetter.md](07_typesetter.md) — downstream

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
-

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-06 | 2.2 | Címke-emoji: `❓` → `❔ Ellenőrizd magad` (Instructions §4.1 KÉRDÉS-jelölés). |
| 2026-06-06 | 2.1 | **Retrieval practice**: új `❔ Ellenőrizd magad` kérdés-blokk minden `##` fejezet zárásánál a `💡` elé, és elkülönített `## 🔑 Megoldókulcs` szekció a dokumentum végén (spoiler-mentes előhívás, Learning Scientists). §3.3 új; §3.4/3.5 átszámozva; idempotencia, ellenőrzés, hibakezelés kiterjesztve. |
| 2026-06-03 | 1.0 | Létrehozva (05_visual_enricher összegző-doboz részéből kiválasztva) |
| 2026-06-03 | 2.0 | `📦 Összegző` (egyetlen `##`-szintű doboz) helyett kétszintű séma: `💡 Összegzés` minden `##` alfejezet végén, `🗺️ Fejezet összegfoglalása` minden `#` fejezet zárásánál; idempotencia-szabály (§3.4) |
| 2026-06-11 | 2.3 | §Teszt pótolva (atg/1_het); §5→§10 átszámozva (sablon-konform). |
