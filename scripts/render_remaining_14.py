import math
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

ROOT = Path(r"d:\medullaprep\dhruv1")
SRC_DIR = ROOT / "public" / "uploads"
OUT_DIR = ROOT / "output" / "imagegen" / "ophthalmology-2017-2019-img1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_W, TARGET_H = 1200, 900

def create_black_canvas(w=TARGET_W, h=TARGET_H):
    return Image.new("RGBA", (w, h), (0, 0, 0, 255))

def fit_on_black(img, target_w=TARGET_W, target_h=TARGET_H, pad=20):
    canvas = create_black_canvas(target_w, target_h)
    max_w = target_w - 2 * pad
    max_h = target_h - 2 * pad
    scale = min(max_w / img.width, max_h / img.height)
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2
    canvas.paste(resized, (x, y))
    return canvas.convert("RGB")

print("Helper functions defined.")
