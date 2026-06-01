"""
build_due_potx.py
=================
Proper PowerPoint template (.potx) a DUE vizuális nyelvből.

Kimenet: templates/due_presentation_master.potx
- 12 named layout a New Slide panelben
- Minden layout tartalmazza a teljes DUE chrome-ot (navy sáv, logo, footer)
- Placeholder-ek: title, body (h1/h2/h3 szintek), dt, ftr, sldNum
- h3 harmadrendű cím is definiálva
"""

import os
import shutil
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Konstansok
# ---------------------------------------------------------------------------
SLIDE_W  = 12192119
SLIDE_H  = 6858000
C_NAVY   = "0D1B3E"
C_ORANGE = "ED7D31"
C_WHITE  = "FFFFFF"
C_DARK   = "212121"
C_GRAY   = "7A8A9E"
C_FOOTLINE = "D0D8E4"
C_LIGHT_BG = "F5F7FA"

NS = (
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
)
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

MEDIA_SRC = Path("templates/due_unpacked/ppt/media")
OUT_DIR   = Path("templates/_potx_build")
FINAL_OUT = Path("templates/due_presentation_master.potx")

# ---------------------------------------------------------------------------
# XML segédfüggvények
# ---------------------------------------------------------------------------

def sp(id_, name, x, y, cx, cy, fill_xml, line_xml="", txbody_xml="", style_xml="", ph_xml=""):
    cNvSpPr = '<p:cNvSpPr/>' if not ph_xml else '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    nvPr    = f'<p:nvPr>{ph_xml}</p:nvPr>' if ph_xml else '<p:nvPr/>'
    return f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{id_}" name="{name}"/>
    {cNvSpPr}
    {nvPr}
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {fill_xml}{line_xml}
  </p:spPr>
  {style_xml}
  {txbody_xml}
</p:sp>"""


def cxnsp(id_, name, x, y, cx, cy, line_w=9525, color=C_FOOTLINE):
    return f"""
<p:cxnSp>
  <p:nvCxnSpPr>
    <p:cNvPr id="{id_}" name="{name}"/>
    <p:cNvCxnSpPr/>
    <p:nvPr/>
  </p:nvCxnSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="line"><a:avLst/></a:prstGeom>
    <a:ln w="{line_w}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln>
  </p:spPr>
</p:cxnSp>"""


def pic(id_, name, descr, x, y, cx, cy, rid="rId1"):
    return f"""
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="{id_}" name="{name}" descr="{descr}"/>
    <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="{rid}"/>
    <a:stretch/>
  </p:blipFill>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
</p:pic>"""


def solidFill(c): return f'<a:solidFill><a:srgbClr val="{c}"/></a:solidFill>'
def noFill():     return '<a:noFill/>'
def noLine():     return '<a:ln><a:noFill/></a:ln>'


def rpr(lang="hu-HU", sz=1600, bold=False, color=C_DARK, typeface="Calibri", italic=False):
    b  = ' b="1"' if bold else ' b="0"'
    i  = ' i="1"' if italic else ''
    return (f'<a:rPr lang="{lang}" sz="{sz}"{b}{i} dirty="0">'
            f'{solidFill(color)}'
            f'<a:latin typeface="{typeface}"/>'
            f'</a:rPr>')


def simple_txbody(txt, sz=1600, bold=False, color=C_DARK, typeface="Calibri",
                  anchor="ctr", align="l", wrap="square", italic=False):
    return f"""<p:txBody>
  <a:bodyPr wrap="{wrap}" anchor="{anchor}"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle/>
  <a:p>
    <a:pPr algn="{align}"/>
    <a:r>{rpr("hu-HU", sz, bold, color, typeface, italic)}<a:t>{txt}</a:t></a:r>
  </a:p>
</p:txBody>"""


def empty_txbody(anchor="ctr"):
    return f'<p:txBody><a:bodyPr anchor="{anchor}"/><a:lstStyle/><a:p><a:endParaRPr/></a:p></p:txBody>'


# ---------------------------------------------------------------------------
# DUE chrome blokkok
# ---------------------------------------------------------------------------

def title_bar_bg(id_=10):
    fill = solidFill(C_NAVY)
    line = noLine()
    txb  = empty_txbody()
    return sp(id_, "title_bar_bg", 0, 0, SLIDE_W, 1080000, fill, line, txb)


def logo_small(id_=11, rid="rId1"):
    return pic(id_, "logo_small", "due_logo_pici.png",
               11256119, 152426, 792000, 775148, rid)


def separator_footer(id_=12):
    return cxnsp(id_, "separator_footer", 432000, 6426000, 11328119, 0)


def content_chrome(img_rid="rId1"):
    """Három shared chrome elem: navbar, logo, footer-vonal."""
    return title_bar_bg(10) + logo_small(11, img_rid) + separator_footer(12)


# ---------------------------------------------------------------------------
# Placeholder-ek
# ---------------------------------------------------------------------------

def title_ph(id_=13, x=432000, y=342556, cx=10248119, cy=430887,
             font="Garamond", sz=2200, color=C_WHITE, align="l", placeholder_hint="", hint=""):
    ph   = '<p:ph type="title"/>'
    fill = noFill()
    txb  = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="ctr"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="{align}">
      <a:defRPr lang="hu-HU" sz="{sz}" b="1" dirty="0">
        {solidFill(color)}
        <a:latin typeface="{font}"/>
      </a:defRPr>
    </a:lvl1pPr>
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>{hint or placeholder_hint or "Dia cím"}</a:t></a:r></a:p>
</p:txBody>"""
    cNvSpPr = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    return f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{id_}" name="slide_title"/>
    {cNvSpPr}
    <p:nvPr>{ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {fill}
  </p:spPr>
  {txb}
</p:sp>"""


def center_title_ph(id_=13, x=720000, y=1260000, cx=9888119, cy=2520000):
    ph  = '<p:ph type="ctrTitle"/>'
    cNvSpPr = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="b"><a:noAutofit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="l">
      <a:defRPr lang="hu-HU" sz="3400" b="1" dirty="0">
        {solidFill(C_WHITE)}
        <a:latin typeface="Garamond"/>
      </a:defRPr>
    </a:lvl1pPr>
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>Előadás főcíme</a:t></a:r></a:p>
</p:txBody>"""
    return f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{id_}" name="slide_main_title"/>
    {cNvSpPr}
    <p:nvPr>{ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {txb}
</p:sp>"""


def subtitle_ph(id_=14, x=720000, y=4140000, cx=10752119, cy=338554):
    ph  = '<p:ph type="subTitle" idx="1"/>'
    cNvSpPr = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="t"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="l">
      <a:defRPr lang="hu-HU" sz="1500" b="0" i="1" dirty="0">
        {solidFill(C_GRAY)}
        <a:latin typeface="Aptos"/>
      </a:defRPr>
    </a:lvl1pPr>
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>Egyetem neve · Képzés neve · Intézet neve · Tantárgy neve</a:t></a:r></a:p>
</p:txBody>"""
    return f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{id_}" name="slide_subtitle"/>
    {cNvSpPr}
    <p:nvPr>{ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {txb}
</p:sp>"""


def body_ph(id_=14, x=432000, y=1296000, cx=11328119, cy=4977573, idx=1,
            h1_sz=1500, h2_sz=1400, h3_sz=1300, hint="Szöveg beírása"):
    """Body placeholder h1/h2/h3 szintekkel, orange marker stílussal."""
    ph  = f'<p:ph type="body" idx="{idx}"/>'
    cNvSpPr = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'

    def lvl(n, sz, margin, indent, buChar):
        m_attr = f' marL="{margin}" indent="{indent}"' if margin else ''
        return f"""<a:lvl{n}pPr algn="l" defTabSz="180000"{m_attr}>
        <a:spcBef><a:spcPts val="300"/></a:spcBef>
        <a:spcAft><a:spcPts val="100"/></a:spcAft>
        <a:buChar char="{buChar}"/>
        <a:defRPr lang="hu-HU" sz="{sz}" b="0" dirty="0">
          {solidFill(C_DARK)}
          <a:latin typeface="Calibri"/>
        </a:defRPr>
      </a:lvl{n}pPr>"""

    txb = f"""<p:txBody>
  <a:bodyPr wrap="square" numCol="1"><a:noAutofit/></a:bodyPr>
  <a:lstStyle>
    {lvl(1, h1_sz, 0, 0, "▶")}
    {lvl(2, h2_sz, 342900, -342900, "–")}
    {lvl(3, h3_sz, 685800, -342900, "·")}
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>{hint}</a:t></a:r></a:p>
</p:txBody>"""
    return f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{id_}" name="content_body"/>
    {cNvSpPr}
    <p:nvPr>{ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {txb}
</p:sp>"""


def footer_phs(start_id=15, date_fld=True):
    """Három footer placeholder: dátum (bal), szerző (közép), oldalszám (jobb)."""
    def _footer_sp(id_, name, ph_xml, x, y, cx, cy, align, text_xml):
        cNvSpPr = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        footer_rpr = (f'<a:defRPr sz="850" b="0" dirty="0">'
                      f'{solidFill(C_GRAY)}'
                      f'<a:latin typeface="Calibri"/>'
                      f'</a:defRPr>')
        txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="t"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="{align}">{footer_rpr}</a:lvl1pPr>
  </a:lstStyle>
  {text_xml}
</p:txBody>"""
        return f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{id_}" name="{name}"/>
    {cNvSpPr}
    <p:nvPr>{ph_xml}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {txb}
</p:sp>"""

    # a:fld requires a unique id attribute (GUID format)
    date_text = ('<a:p>'
                 '<a:fld id="{5BCAD085-E8A6-8845-BD4E-CB4CCA059FC4}" type="datetimeFigureOut">'
                 '<a:rPr lang="hu-HU" smtClean="0"/>'
                 '<a:t>2026.01.01.</a:t></a:fld>'
                 '<a:endParaRPr lang="hu-HU"/></a:p>')
    auth_text = '<a:p><a:r><a:rPr lang="hu-HU" sz="1000" dirty="0"/><a:t>Előadó neve</a:t></a:r></a:p>'
    page_text = ('<a:p>'
                 '<a:fld id="{C1FF6DA9-008F-8B48-92A6-B652298478BF}" type="slidenum">'
                 '<a:rPr lang="hu-HU" smtClean="0"/>'
                 '<a:t>‹#›</a:t></a:fld>'
                 '<a:endParaRPr lang="hu-HU"/></a:p>')

    d = _footer_sp(start_id,   "footer_date",
                   '<p:ph type="dt" sz="half" idx="10"/>',
                   432000, 6462000, 2160000, 324000, "l", date_text)
    a = _footer_sp(start_id+1, "footer_author",
                   '<p:ph type="ftr" sz="quarter" idx="11"/>',
                   0, 6462000, SLIDE_W, 246221, "ctr", auth_text)
    p = _footer_sp(start_id+2, "footer_page",
                   '<p:ph type="sldNum" sz="quarter" idx="12"/>',
                   10680119, 6462000, 1080000, 324000, "r", page_text)
    return d + a + p


# ---------------------------------------------------------------------------
# Layout assembler
# ---------------------------------------------------------------------------

def layout_xml(name, layout_type, shapes_xml, bg_xml=""):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<p:sldLayout {NS} type="{layout_type}">
  <p:cSld name="{name}">
    {bg_xml}
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      {shapes_xml}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""


def layout_rels(img_targets=None, master_idx=1):
    """Build _rels XML for a layout. img_targets: list of (rId, target) tuples."""
    entries = [f'  <Relationship Id="rId{master_idx}" '
               f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" '
               f'Target="../slideMasters/slideMaster1.xml"/>']
    if img_targets:
        for rid, target in img_targets:
            entries.append(
                f'  <Relationship Id="{rid}" '
                f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                f'Target="../media/{target}"/>')
    rels = "\n".join(entries)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{rels}
</Relationships>"""


# ---------------------------------------------------------------------------
# Az egyes layoutok
# ---------------------------------------------------------------------------

def build_layout_01_cim():
    """DUE Cím — teljes navy background, cím, alcím, szerző, dátum."""
    bg = f"""<p:bg>
  <p:bgPr>
    {solidFill(C_NAVY)}
    <a:effectLst/>
  </p:bgPr>
</p:bg>"""

    # Orange left accent stripe
    accent = sp(2, "accent_stripe", 0, 0, 180000, SLIDE_H,
                solidFill(C_ORANGE), noLine(), empty_txbody())

    # Watermark logo placeholder area (top right, semi-transparent)
    wm = pic(3, "watermark_logo", "due_logo_nagy.png",
             7224119, 2545200, 5760000, 5760000, rid="rId2")

    # Title orange rule separator
    rule = cxnsp(4, "title_rule", 720000, 3960000, 4320000, 0,
                 line_w=19050, color=C_ORANGE)

    # Main title (ctrTitle ph)
    main_title = center_title_ph(5, 720000, 1260000, 9888119, 2520000)

    # Subtitle
    subti = subtitle_ph(6, 720000, 4140000, 10752119, 338554)

    # Author (custom, no ph)
    auth_txb = simple_txbody("Dr. Előadó neve", sz=1200, color=C_WHITE,
                              typeface="Calibri", anchor="t", align="l")
    author_sp = sp(7, "footer_author", 720000, 5850000, 5040000, 292388,
                   noFill(), "", auth_txb)

    # Date
    date_txb = simple_txbody("2026.01.01.", sz=850, color=C_GRAY,
                              typeface="Calibri", anchor="t", align="l")
    date_sp = sp(8, "footer_date", 720000, 6354000, 2880000, 246221,
                 noFill(), "", date_txb)

    shapes = accent + wm + rule + main_title + subti + author_sp + date_sp
    xml = layout_xml("DUE Cím", "blank", shapes, bg)
    # rId1=slideMaster, rId2=image1.png (nagy logo), master is rId1
    rels = layout_rels([("rId2", "image1.png")], master_idx=1)
    return xml, rels


def build_layout_02_szakasz():
    """DUE Szakaszfejléc — navy bal panel, narancs alap, szám, cím, leírás."""
    # Navy left panel
    navy_left = sp(2, "section_bg_left", 0, 0, 5120689, SLIDE_H,
                   solidFill(C_NAVY), noLine(), empty_txbody())

    # Orange bottom stripe
    bottom = sp(3, "bottom_stripe", 0, 6678000, SLIDE_W, 180000,
                solidFill(C_ORANGE), noLine(), empty_txbody())

    # Vertical accent line
    acc_line = cxnsp(4, "section_accent_line", 5120688, 0, 0, SLIDE_H,
                     line_w=9525, color=C_ORANGE)

    # Logo
    logo = logo_small(5, "rId2")

    # Section number placeholder (custom idx)
    num_ph = '<p:ph idx="1"/>'
    num_txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="b"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="l">
      <a:defRPr lang="hu-HU" sz="7200" b="1" dirty="0">
        {solidFill(C_ORANGE)}
        <a:latin typeface="Garamond"/>
      </a:defRPr>
    </a:lvl1pPr>
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>01</a:t></a:r></a:p>
</p:txBody>"""
    cNvSpPr_locked = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    num_sp = f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="6" name="section_number"/>
    {cNvSpPr_locked}
    <p:nvPr>{num_ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="432000" y="2738835"/><a:ext cx="4544689" cy="1200329"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {num_txb}
</p:sp>"""

    # Section title placeholder
    title_txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="t"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="l">
      <a:defRPr lang="hu-HU" sz="2400" b="1" dirty="0">
        {solidFill(C_WHITE)}
        <a:latin typeface="Garamond"/>
      </a:defRPr>
    </a:lvl1pPr>
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>Fejezet neve</a:t></a:r></a:p>
</p:txBody>"""
    title_ph_sp = f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="7" name="section_title"/>
    {cNvSpPr_locked}
    <p:nvPr><p:ph type="title"/></p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="432000" y="3566160"/><a:ext cx="4544689" cy="830997"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {title_txb}
</p:sp>"""

    # Description placeholder
    desc_txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="ctr"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="l">
      <a:defRPr lang="hu-HU" sz="1600" b="0" dirty="0">
        {solidFill(C_DARK)}
        <a:latin typeface="Calibri"/>
      </a:defRPr>
    </a:lvl1pPr>
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>A fejezet témájának rövid összefoglalója.</a:t></a:r></a:p>
</p:txBody>"""
    desc_sp = f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="8" name="section_description"/>
    {cNvSpPr_locked}
    <p:nvPr><p:ph type="body" idx="2"/></p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="5768689" y="2767280"/><a:ext cx="6279430" cy="1323439"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {desc_txb}
</p:sp>"""

    shapes = navy_left + bottom + acc_line + logo + num_sp + title_ph_sp + desc_sp
    xml = layout_xml("DUE Szakaszfejléc", "blank", shapes)
    rels = layout_rels([("rId2", "image2.png")], master_idx=1)
    return xml, rels


def build_content_layout(name, layout_idx, hint_title, hint_body,
                         h1_sz=1500, h2_sz=1400, h3_sz=1300):
    """Általános content layout: chrome + title ph + body ph + footer ph-ok."""
    chrome = content_chrome("rId2")
    title  = title_ph(13, 432000, 342556, 10248119, 430887, hint=hint_title)
    body   = body_ph(14, 432000, 1296000, 11328119, 4977573,
                     h1_sz=h1_sz, h2_sz=h2_sz, h3_sz=h3_sz, hint=hint_body)
    footers = footer_phs(15)
    shapes = chrome + title + body + footers
    xml = layout_xml(name, "blank", shapes)
    rels = layout_rels([("rId2", "image2.png")], master_idx=1)
    return xml, rels


def build_layout_07_kep_szoveg():
    """DUE Kép + Szöveg — bal: bullet lista, jobb: kép, caption."""
    chrome  = content_chrome("rId2")
    title   = title_ph(13, 432000, 342556, 10248119, 430887, hint="Kép és szöveg")

    # Left body placeholder
    cNvSpPr_locked = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    left_ph = '<p:ph type="body" idx="1"/>'
    left_txb = f"""<p:txBody>
  <a:bodyPr wrap="square"><a:noAutofit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="l">
      <a:defRPr lang="hu-HU" sz="1400" dirty="0">
        {solidFill(C_DARK)}<a:latin typeface="Calibri"/>
      </a:defRPr>
    </a:lvl1pPr>
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>Szöveg beírása</a:t></a:r></a:p>
</p:txBody>"""
    left_sp = f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="14" name="col_left_body"/>
    {cNvSpPr_locked}
    <p:nvPr>{left_ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="432000" y="1296000"/><a:ext cx="6003903" cy="4986000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {left_txb}
</p:sp>"""

    # Vertical separator
    vsep = cxnsp(20, "col_separator", 6615903, 1296000, 0, 4986000,
                 line_w=9525, color=C_FOOTLINE)

    # Right image placeholder
    img_ph = '<p:ph type="pic" idx="2"/>'
    img_sp = f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="15" name="col_right_image"/>
    {cNvSpPr_locked}
    <p:nvPr>{img_ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="6795903" y="1296000"/><a:ext cx="4964216" cy="3739500"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8EDF2"/></a:solidFill>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="ctr"/>
      <a:r><a:rPr lang="hu-HU" sz="1200" dirty="0">
        {solidFill(C_GRAY)}</a:rPr><a:t>[Kép beillesztése]</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>"""

    # Figure caption
    cap_txb = simple_txbody("1. ábra: Felirat", sz=1100, color=C_GRAY, typeface="Calibri", anchor="t")
    cap_sp = sp(16, "figure_caption", 6795903, 5107500, 4964216, 338554,
                noFill(), "", cap_txb, ph_xml='<p:ph idx="3"/>')

    footers = footer_phs(17)
    shapes = chrome + title + left_sp + vsep + img_sp + cap_sp + footers
    xml = layout_xml("DUE Kép+Szöveg", "blank", shapes)
    rels = layout_rels([("rId2", "image2.png")], master_idx=1)
    return xml, rels


def build_layout_08_abra():
    """DUE Ábra — teljes szélességű kép + felirat."""
    chrome  = content_chrome("rId2")
    title   = title_ph(13, 432000, 342556, 10248119, 430887, hint="Ábra")

    cNvSpPr_locked = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
    img_ph = '<p:ph type="pic" idx="1"/>'
    img_sp = f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="14" name="figure_image"/>
    {cNvSpPr_locked}
    <p:nvPr>{img_ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="432000" y="1296000"/><a:ext cx="11328119" cy="4410000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8EDF2"/></a:solidFill>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="ctr"/>
      <a:r><a:rPr lang="hu-HU" sz="1400" dirty="0">
        {solidFill(C_GRAY)}</a:rPr><a:t>[Ábra beillesztése]</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>"""

    fig_sep = cxnsp(15, "figure_separator", 432000, 5742000, 11328119, 0)

    cap_txb = simple_txbody("1. ábra: Felirat szövege", sz=1100, color=C_GRAY,
                             typeface="Calibri", anchor="t")
    cap_sp = sp(16, "figure_caption", 432000, 5814000, 11328119, 338554,
                noFill(), "", cap_txb)

    footers = footer_phs(17)
    shapes = chrome + title + img_sp + fig_sep + cap_sp + footers
    xml = layout_xml("DUE Ábra", "blank", shapes)
    rels = layout_rels([("rId2", "image2.png")], master_idx=1)
    return xml, rels


def build_layout_09_tablazat():
    """DUE Táblázat — table placeholder + felirat."""
    chrome  = content_chrome("rId2")
    title   = title_ph(13, 432000, 342556, 10248119, 430887, hint="Táblázat")

    cNvSpPr_locked = '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'

    # Table title
    tbl_title_txb = f"""<p:txBody>
  <a:bodyPr wrap="square" anchor="t"><a:spAutoFit/></a:bodyPr>
  <a:lstStyle>
    <a:lvl1pPr algn="l">
      <a:defRPr lang="hu-HU" sz="1100" b="1" i="1" dirty="0">
        {solidFill(C_ORANGE)}<a:latin typeface="Calibri"/>
      </a:defRPr>
    </a:lvl1pPr>
  </a:lstStyle>
  <a:p><a:r><a:rPr lang="hu-HU" dirty="0"/><a:t>1. táblázat: Felirat szövege</a:t></a:r></a:p>
</p:txBody>"""
    tbl_title_sp = f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="14" name="table_title"/>
    {cNvSpPr_locked}
    <p:nvPr><p:ph idx="1"/></p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="432000" y="1296000"/><a:ext cx="11328119" cy="338554"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {noFill()}
  </p:spPr>
  {tbl_title_txb}
</p:sp>"""

    title_sep = cxnsp(15, "table_title_separator", 432000, 1656000, 11328119, 0)

    tbl_ph = '<p:ph type="tbl" idx="2"/>'
    tbl_sp = f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="16" name="data_table"/>
    {cNvSpPr_locked}
    <p:nvPr>{tbl_ph}</p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="432000" y="1728000"/><a:ext cx="11328119" cy="4554000"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="E8EDF2"/></a:solidFill>
  </p:spPr>
  <p:txBody>
    <a:bodyPr anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="ctr"/>
      <a:r><a:rPr lang="hu-HU" sz="1200" dirty="0">
        {solidFill(C_GRAY)}</a:rPr><a:t>[Táblázat beillesztése]</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>"""

    footers = footer_phs(17)
    shapes = chrome + title + tbl_title_sp + title_sep + tbl_sp + footers
    xml = layout_xml("DUE Táblázat", "blank", shapes)
    rels = layout_rels([("rId2", "image2.png")], master_idx=1)
    return xml, rels


# ---------------------------------------------------------------------------
# Slide Master
# ---------------------------------------------------------------------------

def build_slide_master():
    """Frissített slideMaster: DUE fontok és az összes layout referenciája."""
    return """<?xml version="1.0" encoding="utf-8"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgRef idx="1001">
        <a:schemeClr val="bg1"/>
      </p:bgRef>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2"
            accent1="accent1" accent2="accent2" accent3="accent3"
            accent4="accent4" accent5="accent5" accent6="accent6"
            hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483721" r:id="rId1"/>
    <p:sldLayoutId id="2147483722" r:id="rId2"/>
    <p:sldLayoutId id="2147483723" r:id="rId3"/>
    <p:sldLayoutId id="2147483724" r:id="rId4"/>
    <p:sldLayoutId id="2147483725" r:id="rId5"/>
    <p:sldLayoutId id="2147483726" r:id="rId6"/>
    <p:sldLayoutId id="2147483727" r:id="rId7"/>
    <p:sldLayoutId id="2147483728" r:id="rId8"/>
    <p:sldLayoutId id="2147483729" r:id="rId9"/>
    <p:sldLayoutId id="2147483730" r:id="rId10"/>
    <p:sldLayoutId id="2147483731" r:id="rId11"/>
    <p:sldLayoutId id="2147483732" r:id="rId12"/>
  </p:sldLayoutIdLst>
  <p:txStyles>
    <p:titleStyle>
      <a:lvl1pPr algn="l" defTabSz="457200" rtl="0" eaLnBrk="1" latinLnBrk="0">
        <a:defRPr sz="2200" b="1" kern="1200">
          <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
          <a:latin typeface="Garamond"/>
        </a:defRPr>
      </a:lvl1pPr>
    </p:titleStyle>
    <p:bodyStyle>
      <a:lvl1pPr algn="l" defTabSz="457200">
        <a:defRPr sz="1500">
          <a:solidFill><a:srgbClr val="212121"/></a:solidFill>
          <a:latin typeface="Calibri"/>
        </a:defRPr>
      </a:lvl1pPr>
      <a:lvl2pPr marL="342900" indent="-342900" algn="l">
        <a:defRPr sz="1400">
          <a:solidFill><a:srgbClr val="212121"/></a:solidFill>
          <a:latin typeface="Calibri"/>
        </a:defRPr>
      </a:lvl2pPr>
      <a:lvl3pPr marL="685800" indent="-342900" algn="l">
        <a:defRPr sz="1300">
          <a:solidFill><a:srgbClr val="212121"/></a:solidFill>
          <a:latin typeface="Calibri"/>
        </a:defRPr>
      </a:lvl3pPr>
    </p:bodyStyle>
    <p:otherStyle>
      <a:defRPr lang="hu-HU">
        <a:latin typeface="Calibri"/>
      </a:defRPr>
    </p:otherStyle>
  </p:txStyles>
</p:sldMaster>"""


def build_master_rels():
    lines = []
    for i in range(1, 13):
        lines.append(
            f'  <Relationship Id="rId{i}" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
            f'Target="../slideLayouts/slideLayout{i}.xml"/>')
    lines.append(
        '  <Relationship Id="rId13" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" '
        'Target="../theme/theme1.xml"/>')
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        + "\n".join(lines) + "\n</Relationships>"
    )


# ---------------------------------------------------------------------------
# Content Types & Presentation XML
# ---------------------------------------------------------------------------

def build_content_types(n_layouts=12):
    layout_entries = "\n".join(
        f'  <Override PartName="/ppt/slideLayouts/slideLayout{i}.xml" '
        f'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
        for i in range(1, n_layouts + 1)
    )
    return f"""<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="png"  ContentType="image/png"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/theme/theme1.xml"
    ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/ppt/presProps.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>
  <Override PartName="/ppt/viewProps.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>
  <Override PartName="/ppt/tableStyles.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>
  {layout_entries}
  <Override PartName="/docProps/core.xml"
    ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml"
    ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""


def build_presentation_xml():
    return f"""<?xml version="1.0" encoding="utf-8"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                saveSubsetFonts="1">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="custom"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""


def build_prs_rels():
    return """<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster"
    Target="slideMasters/slideMaster1.xml"/>
  <Relationship Id="rId2"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps"
    Target="presProps.xml"/>
  <Relationship Id="rId3"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps"
    Target="viewProps.xml"/>
  <Relationship Id="rId4"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles"
    Target="tableStyles.xml"/>
</Relationships>"""


def build_root_rels():
    return """<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    Target="ppt/presentation.xml"/>
  <Relationship Id="rId2"
    Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"
    Target="docProps/core.xml"/>
  <Relationship Id="rId3"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties"
    Target="docProps/app.xml"/>
</Relationships>"""


def build_theme():
    """DUE színséma: navy (accent1), orange (accent2)."""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="DUE">
  <a:themeElements>
    <a:clrScheme name="DUE Palette">
      <a:dk1><a:sysClr lastClr="000000" val="windowText"/></a:dk1>
      <a:lt1><a:sysClr lastClr="ffffff" val="window"/></a:lt1>
      <a:dk2><a:srgbClr val="{C_NAVY}"/></a:dk2>
      <a:lt2><a:srgbClr val="F5F7FA"/></a:lt2>
      <a:accent1><a:srgbClr val="{C_NAVY}"/></a:accent1>
      <a:accent2><a:srgbClr val="{C_ORANGE}"/></a:accent2>
      <a:accent3><a:srgbClr val="{C_GRAY}"/></a:accent3>
      <a:accent4><a:srgbClr val="A3B4C8"/></a:accent4>
      <a:accent5><a:srgbClr val="2E75B6"/></a:accent5>
      <a:accent6><a:srgbClr val="70AD47"/></a:accent6>
      <a:hlink><a:srgbClr val="0563C1"/></a:hlink>
      <a:folHlink><a:srgbClr val="954F72"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="DUE Fonts">
      <a:majorFont>
        <a:latin typeface="Garamond"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:majorFont>
      <a:minorFont>
        <a:latin typeface="Calibri"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="DUE">
      <a:fillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:gradFill rotWithShape="1">
          <a:gsLst>
            <a:gs pos="0"><a:schemeClr val="phClr"><a:tint val="50000"/></a:schemeClr></a:gs>
            <a:gs pos="100000"><a:schemeClr val="phClr"><a:shade val="50000"/></a:schemeClr></a:gs>
          </a:gsLst>
          <a:lin ang="5400000" scaled="0"/>
        </a:gradFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:fillStyleLst>
      <a:lnStyleLst>
        <a:ln w="6350" cap="flat" cmpd="sng" algn="ctr">
          <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
          <a:prstDash val="solid"/>
        </a:ln>
        <a:ln w="12700" cap="flat" cmpd="sng" algn="ctr">
          <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
          <a:prstDash val="solid"/>
        </a:ln>
        <a:ln w="19050" cap="flat" cmpd="sng" algn="ctr">
          <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
          <a:prstDash val="solid"/>
        </a:ln>
      </a:lnStyleLst>
      <a:effectStyleLst>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle>
          <a:effectLst>
            <a:outerShdw blurRad="40000" dist="23000" dir="5400000" rotWithShape="0">
              <a:srgbClr val="000000"><a:alpha val="35000"/></a:srgbClr>
            </a:outerShdw>
          </a:effectLst>
        </a:effectStyle>
      </a:effectStyleLst>
      <a:bgFillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"><a:tint val="95000"/></a:schemeClr></a:solidFill>
        <a:gradFill rotWithShape="1">
          <a:gsLst>
            <a:gs pos="0"><a:schemeClr val="phClr"><a:tint val="95000"/></a:schemeClr></a:gs>
            <a:gs pos="100000"><a:schemeClr val="phClr"><a:shade val="95000"/></a:schemeClr></a:gs>
          </a:gsLst>
          <a:lin ang="5400000" scaled="0"/>
        </a:gradFill>
      </a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>"""


def minimal_xml(root):
    return f'<?xml version="1.0" encoding="utf-8"?>{root}'


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def write(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")


def assemble_potx(base_pptx, final_out, layout_builders,
                  master_builder=None, master_rels_builder=None, theme_builder=None):
    """
    Újrahasználható .potx összeállító (a tanulságok beépítve).

    Stratégia: egy meglévő, valid .pptx-ből indul (ZIP-struktúra),
    és csak a slideLayout-okat, a slideMaster-t és a theme1-et cseréli ki.
    Az összes slide-ot eltávolítja, a content-type-ot template-re állítja.

    Tanulságok (KRITIKUS):
      - Minden layout type="blank" (nem titleAndContent stb.) — különben a
        PowerPoint placeholder-validációja elutasítja a fájlt.
      - Minden <a:fld>-nek kell egyedi id GUID attribútum.
      - A theme2.xml (notesMaster) NEM törölhető, csak a theme1.xml cserélődik.
      - A root _rels/.rels-ből a webextension-referencia törlendő.
      - XML-patch lxml-lel (nem regex a kompakt XML-en).

    Paraméterek:
      base_pptx          : valid forrás .pptx (Path)
      final_out          : kimeneti .potx (Path)
      layout_builders    : [(fname, builder_fn)] — builder_fn -> (xml, rels)
      master_builder     : opcionális; default build_slide_master
      master_rels_builder: opcionális; default build_master_rels
      theme_builder      : opcionális; default build_theme
    """
    base_pptx = Path(base_pptx)
    final_out = Path(final_out)
    if not base_pptx.exists():
        raise FileNotFoundError(f"Alap fájl nem található: {base_pptx}")

    n_layouts = len(layout_builders)

    # Build layout content dict
    new_layouts: dict[str, bytes] = {}
    for fname, builder in layout_builders:
        xml, rels = builder()
        new_layouts[f"ppt/slideLayouts/{fname}.xml"] = xml.encode("utf-8")
        new_layouts[f"ppt/slideLayouts/_rels/{fname}.xml.rels"] = rels.encode("utf-8")

    new_master = (master_builder or build_slide_master)().encode("utf-8")
    new_master_rels = (master_rels_builder or build_master_rels)().encode("utf-8")
    new_theme = (theme_builder or build_theme)().encode("utf-8")

    skip_prefixes = (
        "ppt/slides/",
        "ppt/notesSlides/",
        "ppt/slideLayouts/",
        "ppt/slideMasters/",
    )
    skip_exact = {"ppt/theme/theme1.xml"}

    from lxml import etree as ET

    CT_NS   = "http://schemas.openxmlformats.org/package/2006/content-types"
    RELS_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
    CT_PPT  = "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"
    CT_POTX = "application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"
    CT_SL   = "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"
    CT_SM   = "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"
    CT_TH   = "application/vnd.openxmlformats-officedocument.theme+xml"
    REL_SLIDE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
    REL_NOTES = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide"

    def patch_content_types(data: bytes) -> bytes:
        root = ET.fromstring(data)
        for ov in list(root.findall(f"{{{CT_NS}}}Override")):
            pn = ov.get("PartName", "")
            if any(pn.startswith(f"/ppt/{p}/")
                   for p in ("slides","notesSlides","slideLayouts","slideMasters","theme","webextensions")):
                root.remove(ov)
        for ov in root.findall(f"{{{CT_NS}}}Override"):
            if ov.get("ContentType") == CT_PPT:
                ov.set("ContentType", CT_POTX)
        for ov in list(root.findall(f"{{{CT_NS}}}Override")):
            if "webextension" in ov.get("PartName", ""):
                root.remove(ov)
        def add_override(part, ct):
            ov = ET.SubElement(root, f"{{{CT_NS}}}Override")
            ov.set("PartName", part)
            ov.set("ContentType", ct)
        add_override("/ppt/slideMasters/slideMaster1.xml", CT_SM)
        add_override("/ppt/theme/theme1.xml", CT_TH)
        for i in range(1, n_layouts + 1):
            add_override(f"/ppt/slideLayouts/slideLayout{i}.xml", CT_SL)
        return ET.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

    def patch_prs_rels(data: bytes) -> bytes:
        root = ET.fromstring(data)
        for rel in list(root.findall(f"{{{RELS_NS}}}Relationship")):
            if rel.get("Type", "") in (REL_SLIDE, REL_NOTES):
                root.remove(rel)
        return ET.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

    def patch_root_rels(data: bytes) -> bytes:
        root = ET.fromstring(data)
        for rel in list(root.findall(f"{{{RELS_NS}}}Relationship")):
            tgt = rel.get("Target", "")
            if "webextension" in tgt or "taskpane" in tgt:
                root.remove(rel)
        return ET.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

    def patch_presentation(data: bytes) -> bytes:
        root = ET.fromstring(data)
        ns_p = "http://schemas.openxmlformats.org/presentationml/2006/main"
        lst = root.find(f"{{{ns_p}}}sldIdLst")
        if lst is not None:
            root.remove(lst)
        return ET.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

    final_out.unlink(missing_ok=True)
    with zipfile.ZipFile(base_pptx) as zin, \
         zipfile.ZipFile(final_out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            fn = item.filename
            if any(fn.startswith(p) for p in skip_prefixes):
                continue
            if fn in skip_exact:
                continue
            if fn.startswith("ppt/webextensions/"):
                continue
            data = zin.read(fn)
            if fn == "[Content_Types].xml":
                data = patch_content_types(data)
            elif fn == "_rels/.rels":
                data = patch_root_rels(data)
            elif fn == "ppt/_rels/presentation.xml.rels":
                data = patch_prs_rels(data)
            elif fn == "ppt/presentation.xml":
                data = patch_presentation(data)
            zout.writestr(item, data)
        for path, content in new_layouts.items():
            zout.writestr(path, content)
        zout.writestr("ppt/slideMasters/slideMaster1.xml", new_master)
        zout.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", new_master_rels)
        zout.writestr("ppt/theme/theme1.xml", new_theme)

    print(f"Kész: {final_out}")
    print(f"Méret: {final_out.stat().st_size // 1024} KB")


def main():
    """
    Stratégia: a meglévő due_refactored.pptx-ből indul (valid ZIP-struktúra),
    és csak a slideLayout-okat, a slideMaster-t és a theme-t cseréli ki.
    Az összes slide-ot eltávolítja, a content-type-ot template-re állítja.
    """
    BASE_PPTX = Path("templates/due_refactored.pptx")
    if not BASE_PPTX.exists():
        raise FileNotFoundError(f"Alap fájl nem található: {BASE_PPTX}")

    # Layouts to inject
    layout_builders = [
        ("slideLayout1",  build_layout_01_cim),
        ("slideLayout2",  build_layout_02_szakasz),
        ("slideLayout3",  lambda: build_content_layout(
            "DUE Tartalom (TOC)", 3,
            "Tartalom", "1. Fejezet\n  1.1. Szakasz\n    1.1.1. Alszakasz")),
        ("slideLayout4",  lambda: build_content_layout(
            "DUE H1 Fejezet", 4,
            "1. Fejezet neve", "▶ Első pont\n▶ Második pont\n▶ Harmadik pont")),
        ("slideLayout5",  lambda: build_content_layout(
            "DUE H2 Szakasz", 5,
            "1.1. Szakasz neve", "  – Első alszakasz pont\n  – Második alszakasz pont")),
        ("slideLayout6",  lambda: build_content_layout(
            "DUE H3 Alszakasz", 6,
            "1.1.1. Alszakasz neve",
            "    · Részlet A\n    · Részlet B\n    · Részlet C",
            h1_sz=1400, h2_sz=1350, h3_sz=1300)),
        ("slideLayout7",  build_layout_07_kep_szoveg),
        ("slideLayout8",  build_layout_08_abra),
        ("slideLayout9",  build_layout_09_tablazat),
        ("slideLayout10", lambda: build_content_layout(
            "DUE Irodalomjegyzék", 10,
            "Irodalomjegyzék", "[1] Szerző (évszám). Cím. Kiadó.\n[2] Szerző (évszám). Cím.")),
        ("slideLayout11", lambda: build_content_layout(
            "DUE Üres tartalom", 11, "Dia cím", "")),
        ("slideLayout12", lambda: build_content_layout(
            "DUE Változásjegyzék", 12,
            "Változásjegyzék", "Verzió  Dátum  Szerző  Leírás")),
    ]

    assemble_potx(BASE_PPTX, FINAL_OUT, layout_builders)


if __name__ == "__main__":
    main()
