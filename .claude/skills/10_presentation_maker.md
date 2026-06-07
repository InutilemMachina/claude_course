---
name: 10_presentation_maker
title: 10_PRESENTATION_MAKER — MARP prezentáció és PPTX generálás
type: skill
tags: [meta, skill]
role: 🤖+🐍
status: active
version: 1.4
updated: 2026-06-06
description: Approved mindmap és végleges jegyzet alapján MARP prezentáció és PPTX. Kötött dia-architektúra (Cím → Áttekintés → szakaszonként Nyitó/belső/Záró → Végső → Hivatkozásjegyzék); kötött `>` keret-blokk-rend (🧭/🔭/🎯/💡/🗺️) a jegyzet újrahasznosításával; belső diák tiszta tananyag; előrenderelt Mermaid-algráf-PNG-k (10-1_mermaid_render.py); kétoszlopos layout; beszédes diák; számozott feliratok.
---

# 10_PRESENTATION_MAKER

## 1. Cél

A végleges jegyzetből és az approved mindmap-ből MARP-kompatibilis prezentációt generál,
majd `10_pptx_gyarto.py`-val PPTX-re konvertálja.

**Input:** `4_wip_outputs/N_Jegyzet.md` + `3_mindmap/mindmap.md`
**Output:** `4_wip_outputs/N_Prezentacio.md` + `5_clean_outputs/N_Prezentacio.pptx`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 08_quality_reviewer | Publikálható minőségű jegyzet |
| `3_mindmap/mindmap.md` | 03_mindmap_builder | Approved mindmap, navigátor diához |
| `2_clean_inputs/figure_catalog.json` | 02_image_extraction | Ábrák diákba illesztéséhez |

**Előfeltétel:** `08_quality_reviewer` döntése `PUBLIKÁLHATÓ`; MARP CLI telepítve.

## 3. Eljárás

### 3.1. MARP Markdown generálása

Claude generálja a `N_Prezentacio.md`-t az alábbi szabályok szerint:

**Dia-architektúra (kötött sorrend):**

```
1.  Címdia
2.  Áttekintés (kétoszlop):  bal: > 🗺️ A Nagykép (fejezet)  | jobb: navigator.png (csak szakaszok)
    minden szakaszhoz (1..N):
      ├─ Szakasz-NYITÓ (kétoszlop): bal: keret-blokkok (lásd lent) | jobb: secK.png algráf
      ├─ belső tartalmi dia/diák   : TISZTA tananyag, keret-blokk nélkül (legfeljebb 💡)
      └─ Szakasz-ZÁRÓ (kétoszlop)  : bal: keret-blokkok (reflexió)   | jobb: secK.png algráf
N+.  Végső összegző (kétoszlop): bal: > 🗺️ Fejezet összegfoglalása | jobb: navigator.png
utolsó. Hivatkozásjegyzék
```

**A kiemelt `>` blokkok szigorú rendje (CSAK keret-diákon):** a `>`-vel kezdődő blokkok kizárólag
az Áttekintő, a szakasz-nyitó/záró és a végső diákon jelennek meg, az alábbi **kötött sorrendben**.
A belső tartalmi diák ettől mentesek — ott legfeljebb egy `> 💡` állhat.

| Keret-dia | `>` blokkok kötött sorrendje | Forrás (újrahasznosítás) |
|:----------|:-----------------------------|:--------------------------|
| Áttekintés | `> 🗺️ **A Nagykép:**` | jegyzet `🗺️` „Fő üzenet" |
| Szakasz-nyitó | `> 🧭 **Hely az ívben:**` → `> 🔭 **A Nagykép:**` → `> 🎯 **Cél:**` | 🧭 származtatott; 🔭/🎯 a jegyzet `##` blokkjaiból |
| Szakasz-záró | `> 🔭 **A Nagykép — visszatekintés:**` → `> 💡 **Összegzés:**` | 🔭 rövid visszautalás; 💡 a jegyzet `💡` blokkjából (reflexió, nem ismétlés) |
| Végső | `> 🗺️ **Fejezet összegfoglalása:**` | jegyzet `🗺️` blokk |

**Emoji-kulcs:** `🗺️` fejezet-nagykép/összefoglalás · `🧭` didaktikai hely az ívben · `🔭` szakasz-nagykép (analógia) · `🎯` Bloom-igés cél · `💡` reflexió/összegzés. A `🔭/🎯/💡/🗺️` a jegyzetből jön (04/06), a `🧭` prezi-specifikus (a `🗺️` „Kapcsolódás"-ból / a szakasz ívbeli helyéből származtatva).

**További kötelező szabályok:**
- **Minden dián 1 vizuális elem** — keret-diákon a jobb oldali algráf (`secK.png` / `navigator.png`), belső diákon valódi ábra/táblázat.
- **Kétoszlopos elrendezés** a keret-diákon és ahol értelmes (`<div class="columns">…</div>`, a `style:` a frontmatterben); tisztán ábra-központú belső dián egyoszlopos nagy kép is jó.
- Képletek: `$$...$$` MARP LaTeX blokkban.
- **Diaszám:** nincs felső korlát — a megértés érdekében bátran „felfelé kerekíts" (több belső dia, ha a téma indokolja).

**Felirat-konvenció (kanonikus: [Instructions §7.1](../../Instructions.md)):** a belső tartalmi
diákon számozott, önálló koherens felirat — valódi ábra **alatt** (`*i. ábra. …*`), táblázat
**fölött** (`*i. táblázat. …*`). A keret-diákon ismétlődő szakasz-algráf rövid, szám nélküli
leíró felirattal szerepel (pl. „A 3. szakasz felépítése. [saját szerk.]").

### 3.1a. Mermaid → PNG előrenderelés (`10-1_mermaid_render.py`)

A MARP **nem** rendereli a Mermaidot natívan (kódként jelenne meg a PPTX-ben), ezért a prezi
diagramjait előre PNG-vé alakítjuk. **Algráf-bontás:** a navigátort szakaszonkénti algráfokra
bontjuk — `navigator.mmd` (csak `ROOT → N1..N` szakaszok) az áttekintőre/végsőre, és `secK.mmd`
(`Nk → Nk1..Nkm`) minden szakasz nyitó/záró diájára.

**Munkamenet:**
1. Írd meg a `.mmd` fájlokat a `4_wip_outputs/_prezi_assets/` mappába (`navigator.mmd`, `sec1.mmd`, …) a `3_mindmap/mindmap.md` részfái alapján.
2. Renderelés PNG-be:

```powershell
python scripts/10-1_mermaid_render.py --week-dir <tárgy>/<N_het>
```

A script minden `_prezi_assets/*.mmd`-t azonos nevű `.png`-vé alakít, és a prezi `![](_prezi_assets/secK.png)`-ként hivatkozza.

**Render-előfeltételek (egyszeri, [project_status.md](../project_status.md) B-15):**
- headless Chromium: `npx puppeteer browsers install chrome-headless-shell`
- mermaid-cli böngésző-letöltés nélkül: `PUPPETEER_SKIP_DOWNLOAD=true npm install @mermaid-js/mermaid-cli` (a `test_outputs/_tools/`-ba; a script innen keresi a `cli.js`-t, vagy a `MMDC_CLI` env-ből)
- a script a puppeteer-configot maga állítja elő (`executablePath` **forward-slash** úttal + `--no-sandbox`)

⚠️ A headless böngésző indítása a futtató sandboxát igényelheti kikapcsolva (a chromium-alfolyamat különben némán elhal). Ugyanez a script a jegyzet saját szerkesztésű Mermaid-ábráinak PNG-be rendereléséhez is használható (pl. DOCX-exporthoz).

### 3.1b. Jegyzet-blokkok újrahasznosítása

A keret-diák `>` blokkjai **a jegyzet meglévő elemeit hasznosítják újra** (nem újraírják):
a `🔭 A Nagykép`, `🎯 Cél` (04), a `💡 Összegzés` és a `🗺️ Fejezet összegfoglalása` (06) blokkok
szövegét told a megfelelő keret-diára a §3.1 táblázat kötött rendje szerint. A belső tartalmi
diák ettől mentesek (tiszta tananyag). Így a prezi és a jegyzet egyetlen forrásból konzisztens.

### 3.1c. Beszédes diák (felolvasható)

A diák lehetnek **beszédesebbek**, mint a jegyzet-bulletek: a body olyan teljes, koherens
állításokból álljon, hogy az előadó **felolvasva** is összefüggő szöveget kapjon. A tömörség a
*vizuális* elemen van, nem a nyelvi csonkításon — kerüld a táviratstílust, ha az a felolvasott
előadást széttördelné.

**Arisztotelészi szillogizmus-váz (tartalmi diák):** a kötött cím alatt a *body* lehetőleg
deduktív ívet kövessen — **fő premissza** (általános szabály) → **mellékpremissza** (konkrét
helyzet) → **konklúzió** (mi következik a gyakorlatban). Nem minden dián kell mind a három
explicit címke, de a logikai sorrend legyen felismerhető.

**Bloom-igék a body-ban:** a felütés/bullet tartalmazzon megfigyelhető cselekvő igét
(„Azonosítsuk a bottleneck-et", „Rendszerezzük az erőforrásokat"); a **cím marad szigorúan**
a fejezet/szakasz-hierarchiából, oda nem kerül Bloom-ige.

**Rugalmas tömörség — Claude diánként dönti el a megfelelő formát** (a merev 5/10 helyett),
irányadó esetek:
- **normál tartalmi dia:** ~6 bullet / ~15 szó;
- **forgatókönyv-dia** (folyamat lépésről lépésre, pl. „Kavitáció forgatókönyve: 1→2→3"):
  több rövid, **sorszámozott** bullet, egyenként ~3-6 szó (Mayer *segmenting + signaling*);
- **ábra-/táblázat-dia:** ha a dián kép + képaláírás vagy táblázat + felirat a fő tartalom,
  a dia **az ábráról szól** — minimális body-szöveg, a vizuális elem és a felirat viszi az
  üzenetet (Mayer *multimédia + contiguity*: a magyarázat az ábrarész mellett).

### 3.2. PPTX generálás

```powershell
# 1) diagramok PNG-be (ha még nem futott)
python scripts/10-1_mermaid_render.py --week-dir <tárgy>/<N_het>
# 2) PPTX
python scripts/10_pptx_gyarto.py --week N --subject "Jelatvitel"
```

- Előbb a Mermaid-algráfok renderelése (§3.1a), utána a MARP CLI konvertál: `marp N_Prezentacio.md --pptx`
- Output: `5_clean_outputs/N_Prezentacio.pptx`
- Ellenőrzés: slide count, képek beágyazva

### 3.3. Manuális ellenőrzés

- Minden dián van vizuális elem (előrenderelt PNG vagy valódi ábra/tábla)?
- **Nincs nyers Mermaid-kódblokk** a diákon (mind PNG-vé renderelve)?
- Navigátor dia (2.) érthető és teljes?
- A kétoszlopos diák jól tördelnek (szöveg balra, vizuál jobbra)?
- A feliratok a séma szerint (ábra alatt / tábla fölött, számozott)?
- PPTX megnyitható PowerPointban?

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Prezentacio.md` | MARP Markdown, minden dián vizuális elemmel |
| `5_clean_outputs/N_Prezentacio.pptx` | Végleges PowerPoint |

## 5. Ellenőrzés

- [ ] Dia-architektúra a §3.1 szerint: Cím → Áttekintés → szakaszonként (Nyitó → belső → Záró) → Végső → Hivatkozásjegyzék
- [ ] A `>` keret-blokkok **csak** a keret-diákon, a §3.1 táblázat **kötött sorrendjében** (🧭→🔭→🎯 nyitó; 🔭→💡 záró)
- [ ] A belső tartalmi diák tiszta tananyag, keret-blokk nélkül (legfeljebb egy `> 💡`)
- [ ] Minden dia rendelkezik vizuális elemmel; **nincs nyers Mermaid-kód** (minden diagram előrenderelt PNG)
- [ ] A keret-diák jobb oldalán a megfelelő algráf (`navigator.png` / `secK.png`)
- [ ] A `🔭/🎯/💡/🗺️` blokkok a jegyzetből újrahasznosítva (nem újraírva); a záró 💡 reflexió, nem ismétlés
- [ ] Belső diák: szillogizmus-ív (premissza→konklúzió), Bloom-igék a body-ban, beszédes/felolvasható (§3.1c)
- [ ] Feliratok a séma szerint (valódi ábra alatt / tábla fölött, számozott, önálló koherens)
- [ ] PPTX megnyitható; LaTeX képletek rendereltek

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Mermaid kódként jelenik meg a dián (nem ábra) | MARP nem rendereli a Mermaidot natívan | `10-1_mermaid_render.py` futtatása, `![](_prezi_assets/…png)` beágyazás (§3.1a) |
| `10-1_mermaid_render.py` némán hibázik / nincs PNG | A puppeteer-config útja egyszeres `\`-sel (érvénytelen JSON), vagy hiányzó chromium, vagy a sandbox blokkolja a böngészőt | Forward-slash `executablePath`; `chrome-headless-shell` telepítése; a futtatást sandbox nélkül (B-15 előfeltételek) |
| MARP `Parse error` Mermaid blokknál | Speciális karakter a mindmapben | Mindmap-ben: `"`, `'`, `()` cseréje |
| Kétoszlopos dia nem tördel | Hiányzó `style:` a frontmatterben vagy rossz `<div class="columns">` | A frontmatter `style:` blokk és a `<div>` szerkezet ellenőrzése (§3.1) |
| PPTX képek hiányoznak | Relatív útvonal a MARP-ban | Abszolút útvonalak vagy `--allow-local-files` flag |
| Túl sok szöveg egy dián | Claude nem tartotta a 5-bullet szabályt | Manuálisan rövidíteni vagy diát kettéosztani |
| `marp: command not found` | MARP CLI nincs telepítve | `npm install -g @marp-team/marp-cli` |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [08_quality_reviewer.md](08_quality_reviewer.md) — upstream
- [03_mindmap_builder.md](03_mindmap_builder.md) — navigátor dia forrása

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-06 | 1.4 | 😎 visszajelzés: **kötött dia-architektúra** (szakasz-nyitó/záró keret + tiszta belső diák) és **kötött `>` keret-blokk-rend** (🧭→🔭→🎯 / 🔭→💡), a jegyzet `🔭/🎯/💡/🗺️` blokkjainak újrahasznosításával; §3.1a **működő Mermaid→PNG render** (`10-1_mermaid_render.py`, chrome-headless-shell, B-15 megoldva), szakaszonkénti algráf-bontás; §3.2 kétlépcsős build; §5/§6 frissítve. |
| 2026-06-06 | 1.3 | 😎 visszajelzés: **kétoszlopos** layout (`<div class="columns">` + `style:`); §3.1a **Mermaid→PNG előrenderelés** (MARP nem rendereli natívan, B-15); §3.1b jegyzet-blokkok a prezin (`🔭 A Nagykép`, `💡`, `🗺️`); §3.1c **beszédes, felolvasható** diák; felirat-konvenció (Instructions §7.1); §3.3/§5/§6 frissítve. |
| 2026-06-06 | 1.2 | **Didaktikai metaprompt**: §3.1 arisztotelészi szillogizmus-váz (premissza→konklúzió) a body-ban; Bloom-igék a body-ban (cím marad a hierarchiából); rugalmas tömörség a merev 5/10 helyett (normál / forgatókönyv / ábra-dia, Mayer CTML signaling–segmenting–contiguity); §5 négy új checklist-sor. |
| 2026-06-01 | 1.0 | Létrehozva (mint 09_presentation_maker) |
| 2026-06-03 | 1.1 | Átszámozva 09→10; script 10_pptx_gyarto.py |
