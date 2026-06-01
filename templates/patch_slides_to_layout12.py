"""
patch_slides_to_layout12.py
Egyszeri patch: content slides (2,4-12) chrome-elemeit eltávolítja,
mert azok már a slideLayout12-ben vannak.

Futtatás: python templates/patch_slides_to_layout12.py
"""

import re
import os

UNPACKED = "templates/due_unpacked/ppt"

# Slides to patch (slide1=title, slide3=section — those stay on slideLayout7)
CONTENT_SLIDES = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Shape names to remove (now inherited from slideLayout12)
CHROME_NAMES = {"title_bar_bg", "logo_small", "separator_footer"}


def remove_chrome_shapes(xml: str) -> tuple[str, list[str]]:
    """Remove title_bar_bg, logo_small, separator_footer shapes from slide XML."""
    removed = []

    def is_chrome_block(block: str) -> str | None:
        m = re.search(r'<p:cNvPr[^>]+name="([^"]+)"', block)
        return m.group(1) if m and m.group(1) in CHROME_NAMES else None

    # We need to remove:
    # 1. <p:sp>...</p:sp> blocks with chrome name (title_bar_bg)
    # 2. <p:pic>...</p:pic> blocks with chrome name (logo_small)
    # 3. <p:cxnSp>...</p:cxnSp> blocks with chrome name (separator_footer)

    for tag in ("p:sp", "p:pic", "p:cxnSp"):
        pattern = rf'<{tag}>.*?</{tag}>'
        def replacer(m):
            name = is_chrome_block(m.group(0))
            if name:
                removed.append(name)
                return ""
            return m.group(0)
        xml = re.sub(pattern, replacer, xml, flags=re.DOTALL)

    # Clean up double blank lines left behind
    xml = re.sub(r'\n(\s*\n){2,}', '\n\n', xml)
    return xml, removed


def patch_slide_rels(rels_path: str) -> None:
    """Switch layout reference from slideLayout7 to slideLayout12, remove rId3 (image)."""
    with open(rels_path, encoding="utf-8") as f:
        content = f.read()

    # Change layout reference
    content = content.replace(
        "slideLayouts/slideLayout7.xml",
        "slideLayouts/slideLayout12.xml"
    )

    # Remove rId3 (was logo_small image, now in layout)
    content = re.sub(
        r'\s*<Relationship Id="rId3"[^/]*/image[^>]*/>\n?',
        '\n',
        content
    )

    with open(rels_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    for n in CONTENT_SLIDES:
        slide_path = os.path.join(UNPACKED, f"slides/slide{n}.xml")
        rels_path = os.path.join(UNPACKED, f"slides/_rels/slide{n}.xml.rels")

        # Patch XML
        with open(slide_path, encoding="utf-8") as f:
            xml = f.read()

        patched, removed = remove_chrome_shapes(xml)

        with open(slide_path, "w", encoding="utf-8") as f:
            f.write(patched)

        # Patch rels
        patch_slide_rels(rels_path)

        print(f"slide{n}: removed {removed}")

    print("Done. Run pack.py to rebuild the PPTX.")


if __name__ == "__main__":
    main()
