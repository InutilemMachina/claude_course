---
name: 04_content_synthesizer
title: 04_CONTENT_SYNTHESIZER — Mindmap-vezérelt tartalom-szintézis
type: skill
tags: [meta, skill]
role: 🤖
status: active
version: 1.1
updated: 2026-06-03
description: Claude a jóváhagyott mindmap alapján koherens, vizuálisan gazdag tananyag-jegyzetet ír. Minden mindmap-csomópont egy szekció. Mermaid diagramok, LaTeX képletek, IEEE hivatkozások kötelezők.
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
| `2_clean_inputs/{forrás}.md` | 02_image_extraction | Forrásszövegek (referencia olvasáshoz) |
| `1_raw_inputs/citations.json` | 01_source_collector | Forrás-metaadatok (IEEE citáláshoz) |
| `2_clean_inputs/figure_catalog.json` | 02_image_extraction | Elérhető ábrák listája |

**Előfeltétel:** `3_mindmap/mindmap.md` tartalmazza `status: approved`-t.

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

[Bevezető mondat: mi ez, miért fontos — 1-2 mondat.]

### N.1 Alfejezet neve

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

### 3.4. Hivatkozások

- Minden kulcsmegállapítás után: `[1]`, `[2]` stb. (a `citations.json` kulcsai szerint)
- Közvetlen idézetnél: `„szöveg"` [1, p.XX]
- Képlet eredeténél: `(Eq.X.Y)` vagy `(p.XX)` ha a forrás tartalmazza

### 3.5. Hivatkozásjegyzék (kötelező)

A fájl végén:

```markdown
## Hivatkozásjegyzék

[1] Szerző, C.D. *Cím.* Kiadó, Év.
[2] Szerző, E.F. „Cikkcím." *Folyóirat* vol(sz), oldal, Év.
[3] Felhasználó. „Weblapnév." URL (elérve: YYYY-MM-DD).
```

A `citations.json` tartalmából automatikusan renderelhető `_ieee_renderer.py`-val.

### 3.6. Teljes dokumentum struktúra

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

### 3.7. MSc-tartalom kezelése

Ha a mindmapben `[MSc]` jelölésű csomópont van:
- A szövegben: `<!-- MSc -->` kommentblokk nyitja, `<!-- /MSc -->` zárja
- A 11_bsc_export skill ezeket kiszűri a BSc-verzióból

### 3.8. Mentés és checkpoint

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
| 2026-06-01 | 1.0 | Létrehozva (NLM 04+05 kiváltása, Claude-natív) |
| 2026-06-03 | 1.1 | Sablon-sor: `📦 Összegző` → `💡 Összegzés` (`##` alfejezet végén); `🗺️ Fejezet összegfoglalása` placeholder a `#` fejezet zárásánál — kanonikus formátum a 06 skillben |
