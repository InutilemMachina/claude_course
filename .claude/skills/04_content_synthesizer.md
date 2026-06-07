---
name: 04_content_synthesizer
title: 04_CONTENT_SYNTHESIZER — Mindmap-vezérelt tartalom-szintézis
type: skill
tags: [meta, skill]
role: 🤖
status: active
version: 1.5
updated: 2026-06-06
description: Claude a jóváhagyott mindmap alapján koherens, vizuálisan gazdag tananyag-jegyzetet ír. Minden mindmap-csomópont egy szekció. Minden fejezet 🔭 A Nagykép blokkal (analógiás Epitome) indul, az MSc-levezetések worked example formában. A MinerU markdown az elsődleges szöveg- és formula/tábla-forrás — ezeket ne gépeld újra, a MinerU-ból vedd. Mermaid diagramok, LaTeX képletek, IEEE hivatkozások kötelezők.
---

# 04_CONTENT_SYNTHESIZER

## 1. Cél

A 03_mindmap_builder által generált és 😎 által jóváhagyott mindmap alapján Claude
koherens, vizuálisan gazdag wip-jegyzetet ír (`4_wip_outputs/N_Jegyzet.md`).

**Input:** `3_mindmap/mindmap.md` (status: approved) + `2_clean_inputs/**/*.md`
**Output:** `4_wip_outputs/N_Jegyzet.md`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `3_mindmap/mindmap.md` | 03_mindmap_builder | Jóváhagyott hierarchikus mindmap |
| `2_clean_inputs/<stem>/mineru/<stem>.md` | 02_mineru_to_catalog | **Elsődleges szövegforrás** — szekciónként olvasd, fejezetek szerint citálj. Formulák és táblák innen jönnek, ne gépeld újra. |
| `1_raw_inputs/citations.json` | 01_source_collector | Forrás-metaadatok (IEEE citáláshoz) |
| `2_clean_inputs/figure_catalog.json` | 02_mineru_to_catalog | Elérhető ábrák + caption + text_context (placeholder-elhelyezéshez) |

**Előfeltétel:** `3_mindmap/mindmap.md` tartalmazza `status: approved`-t; `2_clean_inputs/<stem>/mineru/<stem>.md` elérhető (ha nem: raw PDF fallback, de minőségromlással).

## 3. Eljárás

### 3.1. A mindmap mint tartalomjegyzék

Az L1 ágak = `##` fejlécek. Az L2 csomópontok = `###` alfejlécek. Tartsd ezt a hierarchiát.

```
ROOT → #  (Dokumentum cím)
L1   → ## (Fejezet)
L2   → ### (Alfejezet)
L3   → #### (opcionális, csak ha nagyon indokolt)
```

### 3.2. Szekció-sablonok

**Minden `##` fejezethez:**

```markdown
## N. Fejezet neve

> 🔭 **A Nagykép — N. Fejezet neve**
>
> [3-4 mondatos „nagykép" (Epitome) EGYETLEN `>` sorban (ne tördeld kézzel): a fejezet magját egy hétköznapi, kézzelfogható analógiával bemutató bekezdés. **Zsargon nélkül** — ez a fejezet-szintű Zoom-out. A blockquote-formátum részletei: [06_summarize_box_injector](06_summarize_box_injector.md) §3.3.]

> 🎯 **Cél:** [egyetlen, **Bloom-igével** megfogalmazott tanulási cél a szakaszra (pl. „Különböztesd meg…", „Vezesd le…", „Hasonlítsd össze…"). Ez adja a constructive alignment (08) cél-oldalát, és a prezi szakasz-nyitó diája is ezt használja újra.]

[Csak ha a fejezet új alapfogalmat igényel — Előfeltételek blokk:]

> 🧱 **Előfeltételek**
>
> - **Fogalom1** — nulla-előtudás szintű definíció.
>
> - **Fogalom2** — … (annyi fogalom, amennyi a fejezet megértéséhez nélkülözhetetlen; nem fixen 3, nem kötelező)

[Bevezető mondat: mi ez, miért fontos — 1-2 mondat.]

### N.1 Alfejezet neve

**Szakasz-nyitó csoport:** a `🔭 A Nagykép`, `🎯 Cél` és (ha van) `🧱 Előfeltételek` blokkok
**közvetlenül egymást követik** (külön blockquote-ok, `>` üres sorral elválasztva, közéjük próza
nélkül) — ahogy a szakasz végén az `❔ Ellenőrizd magad` és `💡 Összegzés` is egymást követi.
A bevezető próza a csoport **után** kezdődik.

[Szöveges kifejtés, forrás-hivatkozásokkal. [1], [2] stb.]

$$\text{Kulcsképlet ha releváns}$$

ahol [jelölések magyarázata].

```mermaid
flowchart LR / TD / sequenceDiagram
    [Diagram a szakasz fő összefüggéseiről]
```

> 💡 **Összegzés — N. Alfejezet neve**
>
> **Kulcsgondolat:** [1 mondat]
>
> **Kulcsfogalmak:** fogalom1, fogalom2, fogalom3
>
> **Képletek:** $Eq.X.Y$ — rövid megnevezés (ha van)
```

A `💡 Összegzés` (minden `##` alfejezet végén) és a `🗺️ Fejezet összegfoglalása` (minden `#` fejezet zárásánál) blokkok formátumát és tartalmi szabályait a [06_summarize_box_injector](06_summarize_box_injector.md) §3 definiálja kanonikusan; a 04 itt csak helyet készít — a tényleges injekciót a 06 végzi.

### 3.3. Vizuális kötelezettségek

- **Minden `##` fejezet tartalmaz legalább 1 Mermaid diagramot** (fejezet végén, összegző előtt)
- **Diagram típus döntési fa:**
  - Folyamat/mechanizmus → `flowchart TD`
  - Hierarchia/összefüggések → `flowchart LR`
  - Összehasonlítás → Markdown table (nem Mermaid)
  - Időbeli lefolyás → `sequenceDiagram`
- Ha `figure_catalog.json` tartalmaz releváns ábrát: `<!-- FIGURE: {fig_id} -- {leírás} -->` placeholder beillesztése
- Ha nincs ábra: a placeholder elegendő — a 05_figure_integrator fogja kezelni

**Felirat-konvenció (kanonikus: [Instructions §7.1](../../Instructions.md)):**

- **Ábra (kép):** felirat a kép **alatt** — `*i. ábra. Önálló koherens feliratmondat. [forrás / saját szerk.]*`
- **Mermaid-diagram / flowchart:** ez is számozott ábra (**saját szerk.**) — a diagram **alatt**: `*i. ábra. Mit mutat a diagram, egész mondatban. [saját szerk.]*`
- **Táblázat:** felirat a tábla **fölött** — `*i. táblázat. Önálló koherens feliratmondat. [forrás / saját szerk.]*`
- Számozás dokumentumon belül folytonos, ábra/táblázat **külön** sorozat, előfordulási sorrendben.
- A felirat **önállóan koherens**: a vizuál + felirat a szövegből kiemelve is megálljon.

### 3.4. Formulák és táblák — MinerU-ból, ne kézzel

**LaTeX formulák:** a MinerU `<stem>.md`-ben `$...$` / `$$...$$` formátumban már kinyerve. Másold át pontosan — ne gépeld újra, ne konvertáld. Ha a forrásban számozva van (`Eq. 3.1`), az `Eq.X.Y` referencia megtartandó.

**Táblák:** a MinerU Markdown-táblát ad. Másold át közvetlenül a megfelelő szekció alá. Ne rajzolj ASCII-táblát a helyén.

**Ellenőrzés:** ha egy fejezet MinerU markdown-jában tábla vagy formula van, a szintézisben is szerepelnie kell — nem hagyható ki szövegre cserélve.

### 3.5. Hivatkozások

- Minden kulcsmegállapítás után: `[1]`, `[2]` stb. (a `citations.json` kulcsai szerint)
- Közvetlen idézetnél: `„szöveg"` [1, p.XX]
- Képlet eredeténél: `(Eq.X.Y)` vagy `(p.XX)` ha a forrás tartalmazza

### 3.6. Hivatkozásjegyzék (kötelező)

A fájl végén:

```markdown
## Hivatkozásjegyzék

[1] Szerző, C.D. *Cím.* Kiadó, Év.
[2] Szerző, E.F. „Cikkcím." *Folyóirat* vol(sz), oldal, Év.
[3] Felhasználó. „Weblapnév." URL (elérve: YYYY-MM-DD).
```

A `citations.json` tartalmából automatikusan renderelhető `_ieee_renderer.py`-val.

### 3.7. Teljes dokumentum struktúra

```markdown
---
title: {tantárgy} — {N}. hét: {témacím}
type: wip_notes
tags: [prod/test, notes]
subject: {tantárgy}
week: N
source_mindmap: ../3_mindmap/mindmap.md
created: YYYY-MM-DD
---

# {Témacím}

**Szint:** BSc/MSc | **Tantárgy:** {tantárgy} | **Hét:** N

---

## Tartalomjegyzék

[automatikusan generálódik a 07-2_heading_numberer.py után]

---

## 1. Fejezet neve
...

## 2. Fejezet neve
...

---

## Hivatkozásjegyzék

[IEEE lista]
```

### 3.8. MSc-tartalom kezelése

Ha a mindmapben `[MSc]` jelölésű csomópont van:
- A szövegben: `<!-- MSc -->` kommentblokk nyitja, `<!-- /MSc -->` zárja
- A 11_bsc_export skill ezeket kiszűri a BSc-verzióból

**Worked example az MSc-levezetéseknél (worked-example effect):** ahol egy MSc-blokk
képletet *vezet le* (pl. Greitzer-egyenletek, Moore–Greitzer, B-paraméter), ne csak a
végeredményt közöld — add meg a **lépésről lépésre kidolgozott levezetést** (kiindulás →
köztes lépések → eredmény), a jelölések magyarázatával. Alacsony előtudásnál a kidolgozott
példa többet ér, mint az önálló feladatmegoldás. A LaTeX-et továbbra is a MinerU `.md`-ből
vedd (§3.4), a *levezetés szövege* a Te hozzáadott didaktikai értéked.

### 3.9. Mentés és checkpoint

```
4_wip_outputs/N_Jegyzet.md
```

A 04 kimenet draft — a 05_figure_integrator (ábra-beillesztés) és 06_summarize_box_injector (összegzők) fogják gazdagítani.
Nincs kötelező emberi checkpoint a 04 után, de a szerzőnek ajánlott átnézni.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Jegyzet.md` | YAML + TJ-hely + fejezetek + diagramok + hivatkozásjegyzék |

## 5. Ellenőrzés

- [ ] Minden L1 mindmap-ág `##` fejezetként szerepel?
- [ ] `🔭 A Nagykép` blokk minden `##` fejezet nyitásánál (analógia, zsargon nélkül)?
- [ ] `🎯 Cél` blokk (Bloom-igés) minden `##` fejezet nyitásánál, a `🔭` után?
- [ ] Ábra-/táblázat-/Mermaid-feliratok a §3.3 séma szerint (számozott, önálló koherens)?
- [ ] `🧱 Előfeltételek` blokk ott, ahol a fejezet új alapfogalmat igényel?
- [ ] MSc-levezetések worked example (lépésről lépésre) formában?
- [ ] Minden `##` fejezetnél van Mermaid diagram?
- [ ] `💡 Összegzés` blokk minden `##` alfejezet végén?
- [ ] `🗺️ Fejezet összegfoglalása` blokk minden `#` fejezet zárásánál? (→ 06_summarize_box_injector)
- [ ] `[1]`, `[2]` hivatkozások a szövegben?
- [ ] `## Hivatkozásjegyzék` a fájl végén?
- [ ] `[MSc]` csomópontok `<!-- MSc -->...<!-- /MSc -->` blokkban?
- [ ] YAML frontmatter `source_mindmap` mezővel?

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Fejezetek nem fedik a mindmapet | Figyelmen kívül hagyott L1 ág | Mindmap újraolvasás; fejezet hozzáadása |
| Mermaid szintaxishiba | Speciális karakter | Érvénytelen karakterek cseréje |
| Üres hivatkozásjegyzék | citations.json nem olvasva | Kézzel kitölteni, majd _ieee_renderer.py |
| MinerU markdown hiányzik | `02_mineru_to_catalog` nem futott | Fallback: raw PDF, de formulák/táblák elvesznek — jelezd a szövegben |
| Formula kézzel begépelve, eltér a forrástól | MinerU markdown figyelmen kívül hagyva | A `<stem>.md` LaTeX-ét másold pontosan, ne szintetizáld |
| [MSc] blokk nem záródik | Hiányzó `<!-- /MSc -->` | Keresés és pótlás |
| `💡 Összegzés` / `🗺️ Fejezet összegfoglalása` hiányzik | Kimaradt a sablonból | Pótlás 06_summarize_box_injector-ben (kanonikus formátum: ott §3.1–3.2) |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md) — §2 Lépések és IO
- [03_mindmap_builder.md](03_mindmap_builder.md) — upstream skill
- [05_figure_integrator.md](05_figure_integrator.md) — downstream skill
- [Instructions.md](../../Instructions.md) — §7 Vizuális gazdagítás, §8 Hivatkozási szabály

## 8. Visszajelzések

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-06 | 1.5 | Új `🎯 Cél` blokk (Bloom-igés tanulási cél) minden `##` fejezet nyitásába, a `🔭` után — a Biggs constructive alignment (08) cél-oldala, a prezi szakasz-nyitó diája újrahasznosítja; §5 checklist. |
| 2026-06-06 | 1.4 | Címke: `🔭 Epitome` → `🔭 A Nagykép`; §3.3 ábra-/táblázat-/Mermaid-felirat konvenció (számozott, önálló koherens, [Instructions §7.1](../../Instructions.md)); §5 felirat-checklist. |
| 2026-06-06 | 1.3 | **Didaktikai metaprompt**: §3.2 `🔭 Epitome` (analógiás nagykép, zsargon nélkül) + opcionális `🧱 Előfeltételek` minden `##` fejezet nyitásába (Reigeluth elaboráció, fejezet-szintű explicit Zoom-out); §3.8 worked-example szabály az MSc-levezetésekhez; §5 három új checklist-sor. |
| 2026-06-01 | 1.0 | Létrehozva (NLM 04+05 kiváltása, Claude-natív) |
| 2026-06-05 | 1.2 | MinerU-first: §2 MinerU `.md` elsődleges szövegforrás; §3.4 új szekció (formulák+táblák MinerU-ból, ne kézzel); §3.5–3.9 átszámozva; §6 két új hibasor. |
| 2026-06-03 | 1.1 | Sablon-sor: `📦 Összegző` → `💡 Összegzés` (`##` alfejezet végén); `🗺️ Fejezet összegfoglalása` placeholder a `#` fejezet zárásánál — kanonikus formátum a 06 skillben |
