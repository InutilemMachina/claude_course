---
name: 10_presentation_maker
title: 10_PRESENTATION_MAKER — MARP prezentáció és PPTX generálás
type: skill
tags: [meta, skill]
role: 🤖+🐍
status: active
version: 1.12
updated: 2026-06-13
description: Approved mindmap és végleges jegyzet alapján MARP prezentáció és PPTX, KÉT variánsban (default fejléc-breadcrumb / mindmap oldalsáv-TOC) ugyanabból a navigációs modellből (_nav_util.py). Kötött dia-architektúra (Cím → Áttekintés → szakaszonként Nyitó/belső/Záró → Végső → Hivatkozásjegyzék); kötött `>` keret-blokk-rend (🧭/🔭/🎯/💡/🗺️) a jegyzet újrahasznosításával; belső diák tiszta tananyag; navigáció = SZÖVEG (TOC/breadcrumb), tartalmi diagramok = előrenderelt Mermaid-PNG (10-1); .potx idx-szerződés (idx0/idx1/idx5); kétoszlopos layout; beszédes diák; számozott feliratok.
---

# 10_PRESENTATION_MAKER

## 1. Cél

A végleges jegyzetből és az approved mindmap-ből MARP-kompatibilis prezentációt generál,
majd `10_pptx_gyarto.py`-val PPTX-re konvertálja.

**Input:** `4_wip_outputs/N_Jegyzet.md` + `3_mindmap/mindmap.md`
**Output:** `4_wip_outputs/N_Prezentacio.md` + `6_clean_outputs/N_Prezentacio.pptx`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 08_quality_reviewer | Publikálható minőségű jegyzet |
| `3_mindmap/mindmap.md` | 03_mindmap_builder | Approved mindmap, navigátor diához |
| `2_clean_inputs/figure_catalog.json` | 02_image_extraction | Ábrák diákba illesztéséhez |

A `3_mindmap/mindmap.md`-t a [`_nav_util.py`](../../scripts/_nav_util.py) parse-olja
**navigációs modellé** (ROOT → szakaszok → alszakaszok) — ebből áll elő
mindkét variáns tájékozódása (breadcrumb / TOC), nem renderelt képből.

**Előfeltétel:** `08_quality_reviewer` döntése `PUBLIKÁLHATÓ`; MARP CLI telepítve.

## 3. Eljárás

### 3.0. Variáns-modell — default / mindmap

A prezentáció **két, párhuzamos kivitelben** készül, ugyanabból a navigációs modellből
(a `mindmap.md` fa + „hol vagyok"):

| Variáns | Tájékozódás | Sablon | MARP rendition | PPTX |
|:--------|:------------|:-------|:---------------|:-----|
| **default** | (akár többsoros) **fejléc-breadcrumb**, nincs oldalsáv | `due_presentation_default_master.potx` | `N_Prezentacio_default.md` | `N_Prezentacio.pptx` |
| **mindmap** | jobb oldali **sorszámozott TOC** (szöveg), aktuális kiemelve | `due_presentation_mindmap_master.potx` | `N_Prezentacio_mindmap.md` | `N_Prezentacio_mindmap.pptx` |

**Egy authored forrás, két rendition.** A 🤖 EGY MARP forrást ír (`N_Prezentacio.md`); a
navigációs helyeket a meglévő `_prezi_assets/(navigator|secN).png` keret-dia-képek jelölik.
A két rendition ebből **gépileg** áll elő: [`10-2_nav_inject.py`](../../scripts/10-2_nav_inject.py)
(MARP) és [`10_pptx_gyarto.py --variant`](../../scripts/10_pptx_gyarto.py) (PPTX), mindkettő a
`_nav_util.py` modelljét hívva.

**Stabil potx↔python szerződés:** a kitöltés kizárólag **placeholder-idx** alapú —
`idx0`=cím, `idx1`=body, `idx2`=kép, `idx3`=felirat, `idx5`=`mindmap_body` (TOC oldalsáv).
A két `.potx` ezt már expozeálja; a generátor a layoutot **logikai szerep** szerint választja
(COVER/SECTION/TOC/H1–H3/KEP/ABRA/TABLA/IROD), így a `MM`/`Mindmap` névkülönbség rejtve marad.

> 💬 NOTE: A `default` az alapértelmezett kimenet (visszafelé kompatibilis). A 🤖 **kérdezze meg
> a 😎-t**, kell-e a `mindmap` variáns is — ha igen, `--variant both`.

### 3.1. MARP Markdown generálása

Claude generálja a `N_Prezentacio.md`-t az alábbi szabályok szerint:

**Dia-architektúra (kötött sorrend):**

```
1.  Címdia
2.  Áttekintés (kétoszlop):  bal: > 🗺️ A Nagykép (fejezet)  | jobb: NAV-hely (navigator.png)
    minden szakaszhoz (1..N):
      ├─ Szakasz-NYITÓ (kétoszlop): bal: keret-blokkok (lásd lent) | jobb: NAV-hely (secK.png)
      ├─ belső tartalmi dia/diák   : TISZTA tananyag, keret-blokk nélkül (legfeljebb 💡)
      └─ Szakasz-ZÁRÓ (kétoszlop)  : bal: keret-blokkok (reflexió)   | jobb: NAV-hely (secK.png)
N+.  Végső összegző (kétoszlop): bal: > 🗺️ Fejezet összegfoglalása | jobb: NAV-hely (navigator.png)
utolsó. Hivatkozásjegyzék
```

**NAV-hely:** a keret-diák jobb oszlopában a navigációt a `_prezi_assets/(navigator|secN).png`
képhivatkozás **jelöli** — a render ezt **szöveggé** cseréli (mindmap → TOC; default → breadcrumb).
A 🤖 a forrásban a szokott módon írja a navigator/secK képet; a `10-2`/`10_pptx_gyarto` cseréli.

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

### 3.1a-bis. Navigáció vs. tartalmi diagram — kötelező megkülönböztetés

- **Navigáció = SZÖVEG.** A keret-diák jobb oldali tájékozódását (TOC / breadcrumb) a
  navigációs modellből renderelt szöveg adja (`10-2` / `10_pptx_gyarto`), **nem** kép.
  A forrásban a `navigator`/`secN` képhivatkozás csak jelölő — a render lecseréli.
- **Tartalmi diagram = PNG.** A **jegyzetből vett valódi** folyamatábrákat a **belső
  tartalmi diákon** továbbra is Mermaid→PNG-ként ágyazzuk be (`10-1`, lásd §3.1a). Ezeknek
  saját, beszédes fájlnevük van (NEM `navigator`/`secN`), így a navigáció-csere nem érinti őket.

### 3.1a-ter. Képek FIT módban (levágás nélkül)

A `ph.insert_picture()` python-pptx-ben **fill/crop** módban működik — a képet a placeholder
arányához igazítja és **levágja** a széleit. **Ez tilos.**

A generátor ezért `insert_img_fit(slide, ph, img_path, md_dir)` segédfüggvényt alkalmaz:
1. Pillow-val beolvassa a kép tényleges pixel-méreteit.
2. `scale = min(ph_w/img_w, ph_h/img_h)` — arányőrző scale (letterbox, nem crop).
3. `slide.shapes.add_picture(path, left, top, new_w, new_h)` — szabad shape-ként, a placeholder
   koordinátái közé centrálva.

**Elv: a kép SOHA nem vágódik le; a placeholder a maximális kiterjedést definiálja.**
Ha Pillow nem elérhető (`pip install Pillow`), a függvény fill/crop fallbackre vált (figyelmeztetéssel).

### 3.1a. Tartalmi Mermaid-diagram → PNG előrenderelés (`10-1_mermaid_render.py`)

A MARP **nem** rendereli a Mermaidot natívan (kódként jelenne meg a PPTX-ben), ezért a belső
diák **jegyzetből vett** diagramjait előre PNG-vé alakítjuk. (A navigáció ettől független:
azt szöveggé rendereljük, lásd §3.0 / §3.1a-bis — nem készül `navigator.mmd`/`secN.mmd` PNG.)

**Munkamenet:**
1. Írd meg a tartalmi `.mmd` fájlokat a `4_wip_outputs/_prezi_assets/` mappába (beszédes névvel, pl. `surge_ciklus.mmd`) a jegyzet diagramjai alapján.
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

### 3.1c-bis. Egy alszakasz / dia — tilos az összevonás

- Minden dia **EGY alszakaszt** tárgyal; TILOS a tartomány-összevonás a címben (pl. „2.1–2.3", „5.1–5.5"). Minden alszakasznak saját diája van.
- Ha egy alszakasz content-igényes (sok kép/sok szöveg), több részre bomlik, a címben jelölve: „3.1. … **(1/2)**", „3.1. … **(2/2)**" (dia-ismétlés ugyanazzal az alszakaszcímmel, sorszámozott rész-jelöléssel). A navigáció (TOC/breadcrumb) szempontjából mindkét rész ugyanahhoz a csomóponthoz tartozik.
- A szakasz-NYITÓ diák a keret-blokkokat (🧭/🔭/🎯) viszik, és a generátor a **DUE Szakaszfejléc** (mindmap variánsban **DUE Mindmap Szakaszfejléc**) mintára képezi őket.
- A mindmap variánsban a TOC-oldalsáv MINDEN dián megjelenik (a képes/táblázatos diákon is).

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

### 3.1d. Hivatkozásjegyzék-dia — teljes forrás→PPTX lánc

- A záró **Hivatkozásjegyzék** dia a jegyzet **teljes** Hivatkozásjegyzékét viszi át
  (mind az `[1]…[N]` tétel), IEEE-sorrendben. A generátor csak azt tudja megjeleníteni,
  ami a forrásban (`N_Prezentacio.md` ← `N_Jegyzet.md`) szerepel — **nem talál ki** tételeket.
- **Forrás→PPTX lánc:** ha a jegyzet irodalomjegyzéke hiányos (pl. csak `[1]` a `[2]/[3]`
  helyett), a PPTX is hiányos lesz. A teljesség a **jegyzet** (04/06) és a MARP-forrás
  felelőssége; a prezentáció-generátor hűen tükröz. Ellenőrizd, hogy a `N_Prezentacio.md`
  Hivatkozásjegyzék-diája a jegyzet **összes** tételét tartalmazza a PPTX-futtatás előtt.

### 3.1e. Navigációs kép ≠ ábra — felirat-tilalom

- A navigációs jelölő képek (`navigator.png` / `secN.png`) **nem tananyag-ábrák**: a render
  ezeket szöveggé (TOC/breadcrumb) cseréli, ezért **TILOS** hozzájuk **számozott ábrafeliratot**
  (`*i. ábra. …*`) írni. Legfeljebb rövid, szám nélküli leíró felirat állhat (§3.1 felirat-konvenció).
- A számozott ábrafeliratok **kizárólag** a belső tartalmi diák **valódi** ábráit illetik.

### 3.2. Renditionök és PPTX generálás

```powershell
# 1) tartalmi diagramok PNG-be (ha van .mmd; navigáció NEM ide tartozik)
python scripts/10-1_mermaid_render.py --week-dir <tárgy>/<N_het>
# 2) látható MARP renditionök (default + mindmap)
python scripts/10-2_nav_inject.py --week-dir <tárgy>/<N_het> --variant both
# 3) PPTX (alap: default; --variant both mindkettőt)
python scripts/10_pptx_gyarto.py --week-dir <tárgy>/<N_het> --variant both
```

- A `10_pptx_gyarto.py` a `.potx` layoutjait használja **python-pptx**-szel (nem MARP CLI):
  a stílus a sablonból örökl, a script csak a placeholdereket (idx) tölti.- Sablonválasztás variáns szerint: `default` → `due_presentation_default_master.potx`;
  `mindmap` → `due_presentation_mindmap_master.potx`. (`--template` felülírja.)
- Output: `6_clean_outputs/N_Prezentacio.pptx` (default) [+ `N_Prezentacio_mindmap.pptx`].
- Ellenőrzés: slide count; mindmap variánsban az `idx5` TOC kitöltve a content/keret diákon
  (ábra/tábla kivételével); default variánsban a content diák címe többsoros breadcrumb.

```powershell
# a .potx mesterek módosítása után (font/bullet/sidebar):
python templates/build_due_potx.py ; python templates/build_mindmap_potx.py
```

**Környezet-előfeltételek (script-futtatás előtt, KÖTELEZŐ):**
- `cwd == claude_course`, a megfelelő conda-env aktiválva (implementer_env / play_env).
- **MinerU[all]** (02 kivonat) · **Node + `@mermaid-js/mermaid-cli`** (10-1 PNG-render) ·
  **`lxml` + `latex2mathml`** (natív OMML-képlet; hiánya → nyers `$`-szöveg, lásd fenti NOTE) ·
  **Pillow** (FIT-kép, §3.1a-ter).
- Proxy mögött: `NO_PROXY=localhost,127.0.0.1` a headless Chromium- és a helyi eszköz-
  eléréshez, különben a mermaid-render **némán** elhalhat.
- **Csendes fallback tilos:** ha a lánc (OMML / mermaid / kép) nem elérhető, a script
  látható figyelmeztetést ad és nem-nulla kóddal lép ki (P0-őr), nem degradál némán.

> 💬 NOTE: A LaTeX képletek **natív PowerPoint-egyenletté** (OMML) alakulnak a
> [`_omml.py`](../../scripts/_omml.py)-val: `$...$` **szövegközi** (a mondatban folyik),
> `$$...$$` **saját-soros** középre zárt block. A lánc LaTeX→MathML (`latex2mathml`)→OMML
> (Office `MML2OMML.XSL`, lxml XSLT). Így nem kép, hanem szerkeszthető egyenlet. A markdown-
> táblák valódi PPTX-táblák; a body font **Aptos ~18pt**, a display-címek **Garamond**.
> *(Telepítés: `pip install latex2mathml`; az XSLT a telepített Office-ból jön. Fallback: ha a
> lánc nem elérhető, a `$`-jeles szöveg marad.)*

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
| `6_clean_outputs/N_Prezentacio.pptx` | Végleges PowerPoint |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het` — `1_Jegyzet.md`.
- **Akció:** `10-1_mermaid_render.py` + `10-2_nav_inject.py` + `10_pptx_gyarto.py --variant {default,mindmap}`.
- **Várt kimenet:** `6_clean_outputs/1_Prezentacio.pptx` (+ `_mindmap`), natív OMML képletek, FIT-képek.
- **Eval:** PPTX megnyitható, képletek rendereltek; §6 ellenőrzőlista.

## 6. Ellenőrzés

- [ ] Dia-architektúra a §3.1 szerint: Cím → Áttekintés → szakaszonként (Nyitó → belső → Záró) → Végső → Hivatkozásjegyzék
- [ ] A `>` keret-blokkok **csak** a keret-diákon, a §3.1 táblázat **kötött sorrendjében** (🧭→🔭→🎯 nyitó; 🔭→💡 záró)
- [ ] A belső tartalmi diák tiszta tananyag, keret-blokk nélkül (legfeljebb egy `> 💡`)
- [ ] **Navigáció = szöveg:** a keret-diák jobb oldala NAV-hely (`navigator`/`secN` jelölő), amit a render TOC/breadcrumb szöveggé cserél — **nem** marad navigációs PNG a kész deckben
- [ ] **Tartalmi diagram = PNG:** a belső diák jegyzetből vett diagramjai előrenderelt PNG-k (beszédes névvel); **nincs nyers Mermaid-kód**
- [ ] **mindmap variáns:** az `idx5` TOC minden content/keret dián kitöltve (ábra/tábla diák kivételével), az aktuális csomópont kiemelve
- [ ] **default variáns:** a content diák címe (idx0) többsoros breadcrumb (szakasz-útvonal)
- [ ] **default Áttekintés (Dia2):** a body a teljes hierarchikus TOC-ot (`expansion="full"`) mutatja, sosem üres (üres fa esetén a Nagykép-szövegre esik vissza)
- [ ] **Hivatkozásjegyzék:** a záró dia a jegyzet **összes** `[1]…[N]` tételét viszi (forrás→PPTX teljesség, §3.1d); nav-képekhez **nincs** számozott felirat (§3.1e)
- [ ] A `🔭/🎯/💡/🗺️` blokkok a jegyzetből újrahasznosítva (nem újraírva); a záró 💡 reflexió, nem ismétlés
- [ ] Belső diák: szillogizmus-ív (premissza→konklúzió), Bloom-igék a body-ban, beszédes/felolvasható (§3.1c)
- [ ] Feliratok a séma szerint (valódi ábra alatt / tábla fölött, számozott, önálló koherens)
- [ ] PPTX megnyitható; LaTeX képletek rendereltek
- [ ] Egy alszakasz / dia; nincs „N.M–N.K" összevont cím; a többrészes diák címében (k/n) jelölés
- [ ] A szakasz-nyitók a Szakaszfejléc mintával készülnek (szám + cím + leírás)
- [ ] A body font Aptos ~18pt; a prózán nincs ▶ bullet; a táblák valódi PPTX-táblák; a képletek natív OMML-egyenletek (nem kép)
- [ ] A képes/ábrás diákon a kép **levágás nélkül** jelenik meg (FIT mód, §3.1a-ter) — a placeholder határolja, de nem vágja
- [ ] mindmap variánsban a TOC-oldalsáv minden dián jelen van (képes/táblázatos diákon is)

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| A mindmap variánsban üres az oldalsáv (nincs TOC) | Hiányzó/rossz `mindmap.md`, vagy nem a `mindmap` variáns fut | `--mindmap <path>` ellenőrzése; `--variant mindmap`/`both`; a `_nav_util.parse_mindmap` a `mindmap.md` első ```mermaid``` blokkját várja |
| A TOC/oldalsáv sorai **üresek** (a fa parse-olódik, de nincs cím) | A Mermaid-címkék **idézőjel nélküliek** (`A[1. Cím]`), a régi regex csak idézőjeleset (`A["…"]`) fogadott | Megoldva: a `_nav_util._NODE_DECL` immár idézőjeles ÉS idézőjel nélküli címkét is parse-ol |
| A **default Áttekintés (Dia2)** body üres | A `render_toc(root, None)` `current-section` bővítése üres TOC-ot ad, ha nincs aktuális csomópont | Megoldva: a `add_toc_overview` `expansion="full"`-t hív (teljes hierarchia) + body-fallback a `_prezi_assets` Nagykép-szövegre |
| A Hivatkozásjegyzék-dia hiányos (`[2]/[3]` hiányzik) | **Forrás-oldali** hiány: a jegyzet/MARP-forrás irodalomjegyzéke hiányos | A jegyzet **teljes** Hivatkozásjegyzéke kell (§3.1d); a generátor nem talál ki tételeket |
| A TOC/breadcrumb rossz csomópontot emel ki | A dia címének vezető száma nem oldható fel a fában, vagy a `secN` kép száma téves | A dia címe `N.` / `N.M.` számmal kezdődjön, vagy a NAV-kép `secN` száma egyezzen a szakasszal |
| Navigációs PNG marad a kész deckben | A nav-kép neve nem `navigator`/`secN` mintájú | A navigációs képet `_prezi_assets/(navigator|secN).png` névvel jelöld; a tartalmi ábrák kapjanak más nevet |
| Tartalmi Mermaid kódként jelenik meg | MARP nem rendereli natívan | `10-1_mermaid_render.py` futtatása, `![](_prezi_assets/…png)` beágyazás (§3.1a) |
| `10-1_mermaid_render.py` némán hibázik / nincs PNG | puppeteer-config útja egyszeres `\`-sel, hiányzó chromium, vagy a sandbox blokkol | Forward-slash `executablePath`; `chrome-headless-shell` telepítése; futtatás sandbox nélkül (B-15) |
| Rossz layout / hiányzó placeholder | A `.potx` layout-neve nem egyezik a szerep-táblával, vagy hiányzó idx | `LAYOUTS` tábla és a `.potx` layout-nevek egyeztetése; a kitöltés idx-hiánytűrő (csendben kimarad) |
| Kétoszlopos MARP dia nem tördel (rendition) | Hiányzó `style:` vagy rossz `<div class="columns">` | A frontmatter `style:` blokk és a `<div>` szerkezet ellenőrzése (§3.1) |
| PPTX kép hiányzik | Rossz relatív útvonal a MARP-ban | A `md_dir`-hez képest oldódik fel; abszolút vagy helyes relatív út |
| Ábra-placeholder **levágja** a kép széleit | `ph.insert_picture()` fill/crop mód | `insert_img_fit()` alkalmaz — ha mégis vágás látszik: Pillow telepítve? (`pip install Pillow`); fallback a fill módra vált (§3.1a-ter) |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- [08_quality_reviewer.md](08_quality_reviewer.md) — upstream
- [03_mindmap_builder.md](03_mindmap_builder.md) — navigátor dia forrása

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-08 | 1.8 | **Képek FIT módban** (§3.1a-ter): `ph.insert_picture()` fill/crop cserélve `insert_img_fit()` (Pillow letterbox-scale + `add_picture`, soha nem vágja a képet); §5/§6 frissítve. |
| 2026-06-07 | 1.7 | 😎 vizuális revízió: **natív OMML-egyenletek** (`_omml.py`: inline `$...$` + block `$$...$$`, LaTeX→MathML→OMML) a kép-alapú képlet helyett — szövegközi és saját-soros egyenletek a helyükön; render_content **W=0 placeholder-bug** javítva (mind a 4 xfrm-dimenzió kiírva); markdown lista-jelölők/emfázis a body-ban tisztítva; `.potx` mesterek átnevezve (`due_presentation_default_master` / `…mindmap_master`). |
| 2026-06-07 | 1.6 | 😎 minőségi revízió: egy-alszakasz/dia (tilos összevonás) + (k/n) többrészes; szakasz-nyitók Szakaszfejléc-mintával; .potx mesterek: Garamond cím + **Aptos 18pt** body, ▶ bullet eltávolítva, mindmap-oldalsáv minden layouton (7/8/9 is); valódi PPTX-táblák; LaTeX→PNG képlet (_latex_png.py, matplotlib mathtext). |
| 2026-06-07 | 1.5 | 😎 visszajelzés: **két variáns** (default fejléc-breadcrumb / mindmap oldalsáv-TOC) közös **navigációs modellből** ([`_nav_util.py`](../../scripts/_nav_util.py)). §3.0 variáns-modell + **stabil potx↔python idx-szerződés** (idx0/idx1/idx5) + logikai szerep→layout leképezés; §3.1a-bis **navigáció=szöveg / tartalmi diagram=PNG** megkülönböztetés; a navigációt a `(navigator|secN).png` jelölő helyettesíti (nincs navigációs Mermaid-PNG). Új [`10-2_nav_inject.py`](../../scripts/10-2_nav_inject.py) (MARP renditionök); `10_pptx_gyarto.py` `--variant {default,mindmap,both}`, `.potx`-natív python-pptx. §3.2/§5/§6 frissítve. |
| 2026-06-06 | 1.4 | 😎 visszajelzés: **kötött dia-architektúra** (szakasz-nyitó/záró keret + tiszta belső diák) és **kötött `>` keret-blokk-rend** (🧭→🔭→🎯 / 🔭→💡), a jegyzet `🔭/🎯/💡/🗺️` blokkjainak újrahasznosításával; §3.1a **működő Mermaid→PNG render** (`10-1_mermaid_render.py`, chrome-headless-shell, B-15 megoldva), szakaszonkénti algráf-bontás; §3.2 kétlépcsős build; §5/§6 frissítve. |
| 2026-06-06 | 1.3 | 😎 visszajelzés: **kétoszlopos** layout (`<div class="columns">` + `style:`); §3.1a **Mermaid→PNG előrenderelés** (MARP nem rendereli natívan, B-15); §3.1b jegyzet-blokkok a prezin (`🔭 A Nagykép`, `💡`, `🗺️`); §3.1c **beszédes, felolvasható** diák; felirat-konvenció (Instructions §7.1); §3.3/§5/§6 frissítve. |
| 2026-06-06 | 1.2 | **Didaktikai metaprompt**: §3.1 arisztotelészi szillogizmus-váz (premissza→konklúzió) a body-ban; Bloom-igék a body-ban (cím marad a hierarchiából); rugalmas tömörség a merev 5/10 helyett (normál / forgatókönyv / ábra-dia, Mayer CTML signaling–segmenting–contiguity); §5 négy új checklist-sor. |
| 2026-06-01 | 1.0 | Létrehozva (mint 09_presentation_maker) |
| 2026-06-03 | 1.1 | Átszámozva 09→10; script 10_pptx_gyarto.py |
| 2026-06-11 | 1.9 | §Teszt pótolva (atg/1_het); §5→§10 átszámozva (sablon-konform). |
| 2026-06-11 | 1.10 | MSc-kivezetés: a navigációs modellből a `[MSc]` tag eltávolítva. |
| 2026-06-12 | 1.11 | Mappa-migráció (P2.2): PPTX-kimenet `5_clean_outputs` → `6_clean_outputs` (§1/§3/§4 + `10_pptx_gyarto.py`). |
