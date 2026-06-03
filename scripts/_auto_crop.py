"""
_auto_crop.py -- Pillow-alapú auto-crop utility.
Fehér háttéren lévő ábrákból levágja a margókat.
Csak born-digital (vektoros) PNG-kre alkalmazandó.
"""
from pathlib import Path
from PIL import Image, ImageOps

WHITESPACE_THRESHOLD = 245   # px < ennél = tartalom (0..255 skálán)
MIN_CROP_RATIO = 0.08        # legalább 8% eltávolított terület → érdemes vágni
PADDING = 10                 # px padding a bbox körül


def auto_crop(img_path: Path) -> tuple[bool, float | None]:
    """
    Megpróbálja automatikusan kivágni az ábra-régiót fehér háttérből.

    Visszatér: (cropped: bool, ratio: float | None)
      - cropped=True  → crop történt, img_path helyben felülírva
      - cropped=False → nem érdemes / sikertelen
      - ratio         → levágott terület aránya (0..1), vagy None hiba esetén
    """
    try:
        img = Image.open(img_path).convert("RGB")
        w, h = img.size

        # Grayscale → bináris kép: tartalom=0, fehér=255
        gray = img.convert("L")
        binary = gray.point(lambda px: 0 if px < WHITESPACE_THRESHOLD else 255, "L")

        # getbbox() a nem-fekete pixeleket keresi → invertálás kell
        inverted = ImageOps.invert(binary)
        bbox = inverted.getbbox()

        if bbox is None:
            # Teljesen fehér kép
            return False, 0.0

        x1, y1, x2, y2 = bbox
        w_crop = x2 - x1
        h_crop = y2 - y1
        ratio = 1.0 - (w_crop * h_crop) / (w * h)

        if ratio < MIN_CROP_RATIO:
            return False, ratio

        # PADDING hozzáadása, képhatáron belül maradva
        x1 = max(0, x1 - PADDING)
        y1 = max(0, y1 - PADDING)
        x2 = min(w, x2 + PADDING)
        y2 = min(h, y2 + PADDING)

        cropped = img.crop((x1, y1, x2, y2))
        cropped.save(str(img_path), "PNG")
        return True, ratio

    except Exception as e:
        print(f"  AUTO-CROP HIBA ({img_path.name}): {e}")
        return False, None
