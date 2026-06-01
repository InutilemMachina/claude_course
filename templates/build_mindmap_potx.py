"""
build_mindmap_potx.py
=====================
DUE "mindmap" variáns PowerPoint sablon (.potx).

A sima DUE sablon (build_due_potx.py) kibővítése: minden content layoutra
egy jobb oldali MINDMAP SIDEBAR (breadcrumb navigáció) kerül + függőleges
col_separator. A sidebar az adott dia helyét mutatja a fejezet-hierarchiában.

A bizonyított assemble_potx() pipeline-t használja (build_due_potx.py),
így minden tanulság beépül (type=blank, fld id, theme2, webext rels, lxml).

Kimenet: templates/due_mindmap_master.potx
Generálás: python templates/build_mindmap_potx.py
"""

import importlib.util
from pathlib import Path

# Import the proven builder module
_spec = importlib.util.spec_from_file_location(
    "build_due_potx", str(Path(__file__).parent / "build_due_potx.py"))
bp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bp)

# Reuse helpers
sp, cxnsp, solidFill, noFill = bp.sp, bp.cxnsp, bp.solidFill, bp.noFill
content_chrome, title_ph, footer_phs = bp.content_chrome, bp.title_ph, bp.footer_phs
layout_xml, layout_rels = bp.layout_xml, bp.layout_rels
assemble_potx = bp.assemble_potx
SLIDE_W, SLIDE_H = bp.SLIDE_W, bp.SLIDE_H
C_NAVY, C_ORANGE, C_WHITE, C_GRAY, C_FOOTLINE = (
    bp.C_NAVY, bp.C_ORANGE, bp.C_WHITE, bp.C_GRAY, bp.C_FOOTLINE)

# ---------------------------------------------------------------------------
# Mindmap-variáns konstansok (a template mérései alapján)
# ---------------------------------------------------------------------------
# Mindmap sidebar (jobb oldali breadcrumb sáv)
MM_X = 8825023
MM_Y = 1296000
MM_W = 2935096
MM_H = 4977573
# Függőleges elválasztó a fő tartalom és a mindmap között
SEP_X = 8851103
SEP_Y = 1296000
SEP_H = 4986000
# Fő tartalom (keskenyebb, hogy elférjen a sidebar)
MAIN_X = 432000
MAIN_Y = 1296000
MAIN_W = 8393022          # SEP_X - MAIN_X - kis rés
MAIN_H = 4977573
# Mindmap breadcrumb színek (a mindmap template-ből)
C_MM_ORANGE = "D4622A"    # sorszám prefix
C_MM_DARK   = "1A1A2E"    # szöveg

FINAL_OUT = Path("templates/due_mindmap_master.potx")
BASE_PPTX = Path("templates/due_refactored.pptx")


# ---------------------------------------------------------------------------
# Mindmap-specifikus shape-ek
# ---------------------------------------------------------------------------

def mindmap_separator(id_=20):
    """Függőleges elválasztó vonal a mindmap sidebar bal szélén."""
    return cxnsp(id_, "col_separator", SEP_X, SEP_Y, 0, SEP_H,
                 line_w=9525, color=C_FOOTLINE)


def mindmap_sidebar_ph(id_=21):
    """
    Mindmap breadcrumb sidebar — body placeholder (idx=5).
    A fill-script tölti fel a fejezet-hierarchia útvonalával.
    """
    ph = '<p:ph type="body" idx="5"/>'
    cNvSpPr = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    txb = f"""<p:txBody>
  <a:bodyPr wrap="square" numCol="1"><a:noAutofit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="l" defTabSz="180000">
      <a:spcBef><a:spcPts val="300"/></a:spcBef>
      <a:buNone/>
      <a:defRPr lang="hu-HU" sz="1100" b="1" dirty="0">
        {solidFill(C_MM_DARK)}
        <a:latin typeface="Calibri"/>
      </a:defRPr>
    </a:lvl1pPr>
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>Mindmap navigáció</a:t></a:r></a:p>
</p:txBody>"""
    return f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{id_}" name="mindmap_body"/>
    {cNvSpPr}
    <p:nvPr>{ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{MM_X}" y="{MM_Y}"/><a:ext cx="{MM_W}" cy="{MM_H}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {txb}
</p:sp>"""


def mindmap_chrome():
    """A mindmap-specifikus extra elemek: separator + sidebar placeholder."""
    return mindmap_separator(20) + mindmap_sidebar_ph(21)


# ---------------------------------------------------------------------------
# Content layout mindmap-sidebar-rel
# ---------------------------------------------------------------------------

def build_mm_content_layout(name, hint_title, hint_body,
                            h1_sz=1500, h2_sz=1400, h3_sz=1300):
    """
    Mindmap content layout: chrome + (keskeny) title + (keskeny) body
    + mindmap sidebar + footer.
    """
    chrome  = content_chrome("rId2")
    # Title: keskenyebb, hogy ne lógjon a sidebar fölé
    title   = title_ph(13, MAIN_X, 342556, 8393022, 430887, hint=hint_title)
    # Main body: keskeny
    body    = bp.body_ph(14, MAIN_X, MAIN_Y, MAIN_W, MAIN_H,
                         h1_sz=h1_sz, h2_sz=h2_sz, h3_sz=h3_sz, hint=hint_body)
    mm      = mindmap_chrome()
    footers = footer_phs(15)
    shapes = chrome + title + body + mm + footers
    xml = layout_xml(name, "blank", shapes)
    rels = layout_rels([("rId2", "image2.png")], master_idx=1)
    return xml, rels


def build_mm_section_layout():
    """
    Mindmap szakaszfejléc: navy bal panel + szám + cím + mindmap sidebar jobbra.
    A sima szakaszfejléchez képest a leírás helyett mindmap sidebar van.
    """
    cNvSpPr = '<p:cNvSpPr/>'
    cNvSpPr_locked = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'

    navy_left = sp(2, "section_bg_left", 0, 0, 5120689, SLIDE_H,
                   solidFill(C_NAVY), bp.noLine(), bp.empty_txbody())
    bottom = sp(3, "bottom_stripe", 0, 6678000, SLIDE_W, 180000,
               solidFill(C_ORANGE), bp.noLine(), bp.empty_txbody())
    acc_line = cxnsp(4, "section_accent_line", 5120688, 0, 0, SLIDE_H,
                     line_w=9525, color=C_ORANGE)
    logo = bp.logo_small(5, "rId2")

    # Section number
    num_txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="b"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle><a:lvl1pPr algn="l">
    <a:defRPr lang="hu-HU" sz="7200" b="1" dirty="0">{solidFill(C_ORANGE)}<a:latin typeface="Garamond"/></a:defRPr>
  </a:lvl1pPr></a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>01</a:t></a:r></a:p>
</p:txBody>"""
    num_sp = f"""
<p:sp>
  <p:nvSpPr><p:cNvPr id="6" name="section_number"/>{cNvSpPr_locked}<p:nvPr><p:ph idx="1"/></p:nvPr></p:nvSpPr>
  <p:spPr><a:xfrm><a:off x="432000" y="2738835"/><a:ext cx="4544689" cy="1200329"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{noFill()}</p:spPr>
  {num_txb}
</p:sp>"""

    # Section title
    title_txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="t"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle><a:lvl1pPr algn="l">
    <a:defRPr lang="hu-HU" sz="2400" b="1" dirty="0">{solidFill(C_WHITE)}<a:latin typeface="Garamond"/></a:defRPr>
  </a:lvl1pPr></a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>Fejezet neve</a:t></a:r></a:p>
</p:txBody>"""
    title_sp = f"""
<p:sp>
  <p:nvSpPr><p:cNvPr id="7" name="section_title"/>{cNvSpPr_locked}<p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>
  <p:spPr><a:xfrm><a:off x="432000" y="3566160"/><a:ext cx="4544689" cy="830997"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{noFill()}</p:spPr>
  {title_txb}
</p:sp>"""

    # Section description (a navy panel és a mindmap között)
    desc_txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="ctr"><a:noAutofit/></a:bodyPr>
  <a:lstStyle><a:lvl1pPr algn="l">
    <a:defRPr lang="hu-HU" sz="1600" b="0" dirty="0">{solidFill(C_MM_DARK)}<a:latin typeface="Calibri"/></a:defRPr>
  </a:lvl1pPr></a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>A fejezet témájának rövid összefoglalója.</a:t></a:r></a:p>
</p:txBody>"""
    desc_sp = f"""
<p:sp>
  <p:nvSpPr><p:cNvPr id="8" name="section_description"/>{cNvSpPr_locked}<p:nvPr><p:ph type="body" idx="2"/></p:nvPr></p:nvSpPr>
  <p:spPr><a:xfrm><a:off x="5264687" y="1296000"/><a:ext cx="3560335" cy="3421449"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{noFill()}</p:spPr>
  {desc_txb}
</p:sp>"""

    mm = mindmap_chrome()
    shapes = navy_left + bottom + acc_line + logo + num_sp + title_sp + desc_sp + mm
    xml = layout_xml("DUE Mindmap Szakaszfejléc", "blank", shapes)
    rels = layout_rels([("rId2", "image2.png")], master_idx=1)
    return xml, rels


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def main():
    layout_builders = [
        # 1. Cím — nincs mindmap (a sima címdiát használja)
        ("slideLayout1", bp.build_layout_01_cim),
        # 2. Szakaszfejléc mindmap-pal
        ("slideLayout2", build_mm_section_layout),
        # 3-6. Content layoutok mindmap sidebar-ral
        ("slideLayout3", lambda: build_mm_content_layout(
            "DUE MM Tartalom (TOC)", "Tartalom",
            "1. Fejezet\n  1.1. Szakasz\n    1.1.1. Alszakasz")),
        ("slideLayout4", lambda: build_mm_content_layout(
            "DUE MM H1 Fejezet", "1. Fejezet neve",
            "▶ Első pont\n▶ Második pont\n▶ Harmadik pont")),
        ("slideLayout5", lambda: build_mm_content_layout(
            "DUE MM H2 Szakasz", "1.1. Szakasz neve",
            "  – Első alszakasz pont\n  – Második alszakasz pont")),
        ("slideLayout6", lambda: build_mm_content_layout(
            "DUE MM H3 Alszakasz", "1.1.1. Alszakasz neve",
            "    · Részlet A\n    · Részlet B",
            h1_sz=1400, h2_sz=1350, h3_sz=1300)),
        # 7. Kép+Szöveg (sima — a kép foglalja a jobb oldalt, nincs külön mindmap)
        ("slideLayout7", bp.build_layout_07_kep_szoveg),
        # 8. Ábra (sima — teljes szélességű ábra)
        ("slideLayout8", bp.build_layout_08_abra),
        # 9. Táblázat (sima)
        ("slideLayout9", bp.build_layout_09_tablazat),
        # 10. Irodalomjegyzék mindmap-pal
        ("slideLayout10", lambda: build_mm_content_layout(
            "DUE MM Irodalomjegyzék", "Irodalomjegyzék",
            "[1] Szerző (évszám). Cím. Kiadó.\n[2] Szerző (évszám). Cím.")),
        # 11. Üres tartalom mindmap-pal
        ("slideLayout11", lambda: build_mm_content_layout(
            "DUE MM Üres tartalom", "Dia cím", "")),
        # 12. Változásjegyzék (sima content, nincs mindmap)
        ("slideLayout12", lambda: bp.build_content_layout(
            "DUE Változásjegyzék", 12,
            "Változásjegyzék", "Verzió  Dátum  Szerző  Leírás")),
    ]
    assemble_potx(BASE_PPTX, FINAL_OUT, layout_builders)


if __name__ == "__main__":
    main()
