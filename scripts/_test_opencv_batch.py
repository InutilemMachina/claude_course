"""
OpenCV k=15 batch teszt — minden available teszt-képre.
Kimenet: _test_opencv_batch/ mappa debug képekkel + összefoglaló táblázat.
"""
import cv2
import numpy as np
from pathlib import Path

BASE = Path(r"C:\Users\lasz\claude_course\test_outputs\atg\1_het\2_clean_inputs")
OUT  = BASE / "_test_opencv_batch"
OUT.mkdir(exist_ok=True)

KSIZE = 15
THRESHOLD = 240

def source_type(img_path: Path) -> str:
    p = str(img_path)
    if "gravdahl" in p:    return "scanned"
    if "tavakoli" in p:    return "scanned"
    if "chattopadhyay" in p and "fig" in img_path.name: return "vector-born-digital"
    if "chattopadhyay" in p and "img" in img_path.name: return "raster-born-digital"
    if "nagy" in p:        return "pptx-slide"
    if "wikipedia" in p:   return "web-raster"
    return "unknown"

def opencv_k15(img_path: Path):
    img = cv2.imread(str(img_path))
    if img is None:
        return None
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, THRESHOLD, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (KSIZE, KSIZE))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    largest = max(contours, key=cv2.contourArea)
    x, y, cw, ch = cv2.boundingRect(largest)
    area_ratio = (cw * ch) / (w * h)
    # Mentjük: eredeti + piros bbox + kivágott crop
    debug = img.copy()
    cv2.rectangle(debug, (x, y), (x+cw, y+ch), (0, 0, 255), 4)
    crop = img[y:y+ch, x:x+cw]
    return {"bbox": (x, y, x+cw, y+ch), "area": area_ratio,
            "orig_size": (w, h), "crop_size": (cw, ch),
            "debug": debug, "crop": crop}

# Összes kép (nem test_ prefixű)
images = sorted([
    p for p in BASE.rglob("*.png")
    if "_test" not in str(p) and p.is_file()
])

print(f"{'Fájl':<45} {'Típus':<22} {'Orig':<14} {'Crop':<14} {'Area%':>6}  {'Értékelés'}")
print("-" * 115)

results = []
for img_path in images:
    stype = source_type(img_path)
    res = opencv_k15(img_path)
    if res is None:
        print(f"  SKIP: {img_path.name}")
        continue

    w, h = res["orig_size"]
    cw, ch = res["crop_size"]
    ar = res["area"]
    # Heurisztikus értékelés
    if ar > 0.90:
        verdict = "NINCS HATÁS (kép maga is figure)"
    elif ar > 0.75:
        verdict = "GYENGE (<25% eltávolítva)"
    elif ar > 0.45:
        verdict = "KÖZEPES (szöveg maradhat)"
    else:
        verdict = "JÓ (>55% eltávolítva)"

    short = img_path.parent.parent.name[:12] + "/" + img_path.name[:20]
    print(f"  {short:<45} {stype:<22} {w}x{h:<8} {cw}x{ch:<8} {ar:>6.1%}  {verdict}")

    # Debug kép mentése
    stem = img_path.parent.parent.name[:10] + "_" + img_path.stem
    cv2.imwrite(str(OUT / f"{stem}_bbox.png"), res["debug"])
    cv2.imwrite(str(OUT / f"{stem}_crop.png"), res["crop"])

    results.append({
        "name": short, "type": stype,
        "orig": (w, h), "crop": (cw, ch), "area": ar, "verdict": verdict
    })

# Összefoglaló forrás-típusonként
print("\n" + "=" * 60)
print("ÖSSZEFOGLALÓ forrástípusonként:")
by_type = {}
for r in results:
    t = r["type"]
    by_type.setdefault(t, []).append(r["area"])

for t, areas in sorted(by_type.items()):
    avg = sum(areas) / len(areas)
    mn, mx = min(areas), max(areas)
    print(f"  {t:<25} n={len(areas)}  avg={avg:.1%}  min={mn:.1%}  max={mx:.1%}")

print(f"\nDebug képek: {OUT}  ({len(list(OUT.glob('*.png')))} fájl)")
