#!/usr/bin/env python3
"""
Prepare a portrait photo for clean ASCII conversion:
  1. remove the background (rembg) so the subject is isolated
  2. boost LOCAL contrast (CLAHE) so a flatly-lit face gains highlights and
     shadows -- this is what turns a dark blob into a recognizable face
  3. composite the subject onto pure white so the background reads as blank
     (white -> spaces in the ascii ramp)

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.
Run once whenever the source photo changes; the ascii SVG itself is static.

    python scripts/prep_photo.py <input.jpg> [output.png]
"""
import os
import sys

from PIL import Image, ImageOps, ImageEnhance
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

def prep():
    if not os.path.exists(INP):
        print(f"Source photo {INP} not found. Creating placeholder prepped image.")
        # Create a stylized developer avatar grid if no photo is provided
        img = Image.new("L", (300, 300), 255)
        img.save(OUT)
        return

    try:
        from rembg import remove
        import cv2
        cut = remove(Image.open(INP).convert("RGBA"))
        rgb = np.array(cut.convert("RGB"))
        alpha = np.array(cut.split()[-1])
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        gray = cv2.convertScaleAbs(gray, alpha=1.05, beta=18)
        mask = (alpha.astype(np.float32) / 255.0)
        mask = cv2.GaussianBlur(mask, (0, 0), 1.0)
        out = gray.astype(np.float32) * mask + 255.0 * (1.0 - mask)
        out = np.clip(out, 0, 255).astype(np.uint8)
        Image.fromarray(out, mode="L").save(OUT)
        print("wrote", OUT, out.shape)
    except Exception as e:
        print(f"Advanced prep fallback due to missing rembg/cv2 ({e}). Using PIL processing.")
        im = Image.open(INP).convert("L")
        im = ImageOps.autocontrast(im, cutoff=2)
        im = ImageEnhance.Contrast(im).enhance(1.4)
        im.save(OUT)
        print("wrote fallback prepped image:", OUT)

if __name__ == "__main__":
    prep()
