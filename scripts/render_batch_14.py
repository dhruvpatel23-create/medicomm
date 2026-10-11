import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont, ImageOps

ROOT = Path(r"d:\medullaprep\dhruv1")
SRC_DIR = ROOT / "public" / "uploads"
OUT_DIR = ROOT / "output" / "imagegen" / "ophthalmology-2017-2019-img1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1200, 900

def get_font(size, bold=False):
    fonts = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for f in fonts:
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

# 1. aiims-2018-ophthalmology-q015: Port-Wine Stain (Nevus Flammeus)
def render_q015():
    src = Image.open(SRC_DIR / "yellowfool-aiims-2018-ophthalmology-q015-p2931-i1.jpg").convert("RGBA")
    sw, sh = src.size
    crop_box = (0, 0, sw, int(sh * 0.94))
    cropped = src.crop(crop_box)
    
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    target_h = int(H * 0.92)
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (target_w, target_h), 255)
    draw_m = ImageDraw.Draw(mask)
    border_px = 35
    for i in range(border_px):
        alpha = int(255 * (i / border_px))
        draw_m.rectangle([i, i, target_w - 1 - i, target_h - 1 - i], outline=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(15))
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y), mask)
    
    out_p = OUT_DIR / "medicomm-img1-aiims-2018-ophthalmology-q015.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 2. aiims-2018-ophthalmology-q017: Oculomotor Palsy 9-Gaze Montage
def render_q017():
    src = Image.open(SRC_DIR / "yellowfool-aiims-2018-ophthalmology-q017-p2932-i1.jpg").convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    
    target_h = int(H * 0.90)
    scale = target_h / src.height
    target_w = int(src.width * scale)
    resized = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Contrast(resized)
    resized = enhancer.enhance(1.25)
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([x - 3, y - 3, x + target_w + 2, y + target_h + 2], outline=(60, 60, 60, 255), width=2)
    canvas.paste(resized, (x, y))
    
    out_p = OUT_DIR / "medicomm-img1-aiims-2018-ophthalmology-q017.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 3. neet-pg-2018-ophthalmology-q007: Endophthalmitis with Hypopyon
def render_neet_2018_q007():
    src = Image.open(SRC_DIR / "yellowfool-neet-pg-2018-ophthalmology-q007-p2992-i1.jpg").convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    
    target_h = int(H * 0.92)
    scale = target_h / src.height
    target_w = int(src.width * scale)
    resized = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (target_w, target_h), 0)
    dm = ImageDraw.Draw(mask)
    dm.ellipse([20, 20, target_w - 20, target_h - 20], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(30))
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y), mask)
    
    out_p = OUT_DIR / "medicomm-img1-neet-pg-2018-ophthalmology-q007.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 4. aiims-2019-ophthalmology-q001: Choroidal Melanoma Fundus
def render_q001_2019():
    src = Image.open(SRC_DIR / "yellowfool-aiims-2019-ophthalmology-q001-p2962-i1.jpg").convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    
    dia = int(H * 0.92)
    resized = src.resize((dia, dia), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (dia, dia), 0)
    dm = ImageDraw.Draw(mask)
    dm.ellipse([0, 0, dia, dia], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(3))
    
    x = (W - dia) // 2
    y = (H - dia) // 2
    canvas.paste(resized, (x, y), mask)
    
    out_p = OUT_DIR / "medicomm-img1-aiims-2019-ophthalmology-q001.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 5. aiims-2019-ophthalmology-q002: Titmus Stereotest Fly
def render_q002_2019():
    src = Image.open(SRC_DIR / "yellowfool-aiims-2019-ophthalmology-q002-p2963-i1.jpg").convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    
    target_h = int(H * 0.92)
    scale = target_h / src.height
    target_w = int(src.width * scale)
    resized = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Process pale background pixels to black
    pix = resized.load()
    rw, rh = resized.size
    for py in range(rh):
        for px in range(rw):
            r, g, b, a = pix[px, py]
            if r > 195 and g > 185 and b > 175:
                pix[px, py] = (0, 0, 0, 255)
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y))
    
    out_p = OUT_DIR / "medicomm-img1-aiims-2019-ophthalmology-q002.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 6. aiims-2019-ophthalmology-q003: Barbed Fish Hook Injury
def render_q003_2019():
    src = Image.open(SRC_DIR / "yellowfool-aiims-2019-ophthalmology-q003-p2963-i2.jpg").convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    
    target_h = int(H * 0.92)
    scale = target_h / src.height
    target_w = int(src.width * scale)
    resized = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (target_w, target_h), 255)
    dm = ImageDraw.Draw(mask)
    border_px = 30
    for i in range(border_px):
        alpha = int(255 * (i / border_px))
        dm.rectangle([i, i, target_w - 1 - i, target_h - 1 - i], outline=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(15))
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y), mask)
    
    out_p = OUT_DIR / "medicomm-img1-aiims-2019-ophthalmology-q003.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 7. aiims-2019-ophthalmology-q006: Swinging Flashlight Test
def render_q006_2019():
    src = Image.open(SRC_DIR / "yellowfool-aiims-2019-ophthalmology-q006-p2965-i1.jpg").convert("RGBA")
    sw, sh = src.size
    cropped = src.crop((0, 0, sw, int(sh * 0.90)))
    
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    target_h = int(H * 0.88)
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Replace white pixels with pure black
    pix = resized.load()
    rw, rh = resized.size
    for py in range(rh):
        for px in range(rw):
            r, g, b, a = pix[px, py]
            if r > 240 and g > 240 and b > 240:
                pix[px, py] = (0, 0, 0, 0)
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y), resized)
    
    draw = ImageDraw.Draw(canvas)
    font_large = get_font(32, bold=True)
    draw.text((x + int(target_w * 0.28), y + 10), "R", fill=(255, 255, 255, 255), font=font_large, anchor="mm")
    draw.text((x + int(target_w * 0.72), y + 10), "L", fill=(255, 255, 255, 255), font=font_large, anchor="mm")
    
    out_p = OUT_DIR / "medicomm-img1-aiims-2019-ophthalmology-q006.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 8. aiims-2019-ophthalmology-q009: Diabetic Macular Ischemia FFA
def render_q009_2019():
    src = Image.open(SRC_DIR / "yellowfool-aiims-2019-ophthalmology-q009-p2966-i1.jpg").convert("RGBA")
    sw, sh = src.size
    cropped = src.crop((int(sw * 0.05), int(sh * 0.09), int(sw * 0.95), int(sh * 0.91)))
    
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    target_h = int(H * 0.90)
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Contrast(resized)
    resized = enhancer.enhance(1.3)
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y))
    
    out_p = OUT_DIR / "medicomm-img1-aiims-2019-ophthalmology-q009.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 9. aiims-2019-ophthalmology-q011: Outer Plexiform Layer Histology
def render_q011_2019():
    src = Image.open(SRC_DIR / "yellowfool-aiims-2019-ophthalmology-q011-p2967-i1.jpg").convert("RGBA")
    sw, sh = src.size
    cropped = src.crop((0, 0, sw, int(sh * 0.98)))
    
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    target_h = int(H * 0.92)
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y))
    
    draw = ImageDraw.Draw(canvas)
    arrow_tip_x = x + int(target_w * 0.83)
    arrow_tip_y = y + int(target_h * 0.485)
    arrow_start_x = x + int(target_w * 0.98)
    arrow_start_y = arrow_tip_y
    
    draw.line([(arrow_start_x, arrow_start_y), (arrow_tip_x, arrow_tip_y)], fill=(255, 215, 0, 255), width=5)
    draw.polygon([
        (arrow_tip_x, arrow_tip_y),
        (arrow_tip_x + 18, arrow_tip_y - 10),
        (arrow_tip_x + 14, arrow_tip_y),
        (arrow_tip_x + 18, arrow_tip_y + 10)
    ], fill=(255, 215, 0, 255))
    
    out_p = OUT_DIR / "medicomm-img1-aiims-2019-ophthalmology-q011.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 10. aiims-2019-ophthalmology-q013: Anterior Ethmoidal Nerve Block
def render_q013_2019():
    src = Image.open(SRC_DIR / "yellowfool-aiims-2019-ophthalmology-q013-p2981-i1.jpg").convert("RGBA")
    sw, sh = src.size
    cropped = src.crop((0, 0, sw, int(sh * 0.90)))
    
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    target_h = int(H * 0.92)
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Neutralize faint blue MARROW watermark
    pix = resized.load()
    rw, rh = resized.size
    for py in range(rh):
        for px in range(rw):
            r, g, b, a = pix[px, py]
            if b > g + 10 and r > 150:
                pix[px, py] = (r, g, max(0, g - 5), a)
    
    mask = Image.new("L", (target_w, target_h), 255)
    dm = ImageDraw.Draw(mask)
    for i in range(40):
        alpha = int(255 * (i / 40))
        dm.rectangle([i, i, target_w - 1 - i, target_h - 1 - i], outline=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(20))
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y), mask)
    
    out_p = OUT_DIR / "medicomm-img1-aiims-2019-ophthalmology-q013.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 11. neet-pg-2019-ophthalmology-q005: Orbital Floor Blowout Fracture CT
def render_neet_2019_q005():
    src = Image.open(SRC_DIR / "yellowfool-neet-pg-2019-ophthalmology-q005-p3010-i1.jpg").convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    
    target_h = int(H * 0.92)
    scale = target_h / src.height
    target_w = int(src.width * scale)
    resized = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Contrast(resized)
    resized = enhancer.enhance(1.2)
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y))
    
    draw = ImageDraw.Draw(canvas)
    cx = x + int(target_w * 0.70)
    cy = y + int(target_h * 0.66)
    rx = int(target_w * 0.13)
    ry = int(target_h * 0.25)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(0, 210, 255, 255), width=3)
    
    out_p = OUT_DIR / "medicomm-img1-neet-pg-2019-ophthalmology-q005.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 12. neet-pg-2019-ophthalmology-q009: Ex-PRESS Glaucoma Implant
def render_neet_2019_q009():
    src = Image.open(SRC_DIR / "yellowfool-neet-pg-2019-ophthalmology-q009-p3012-i1.jpg").convert("RGBA")
    sw, sh = src.size
    cropped = src.crop((0, 0, sw, int(sh * 0.90)))
    
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    target_h = int(H * 0.88)
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    pix = resized.load()
    rw, rh = resized.size
    for py in range(rh):
        for px in range(rw):
            r, g, b, a = pix[px, py]
            if r > 240 and g > 240 and b > 240:
                pix[px, py] = (0, 0, 0, 0)
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y), resized)
    
    draw = ImageDraw.Draw(canvas)
    font_bold = get_font(20, bold=True)
    draw.text((x + int(target_w * 0.88), y + int(target_h * 0.52)), "Conjunctiva", fill=(255, 255, 255, 255), font=font_bold)
    draw.text((x + int(target_w * 0.88), y + int(target_h * 0.61)), "Scleral flap", fill=(255, 255, 255, 255), font=font_bold)
    
    out_p = OUT_DIR / "medicomm-img1-neet-pg-2019-ophthalmology-q009.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 13. neet-pg-2019-ophthalmology-q010: Maddox Rod
def render_neet_2019_q010():
    src = Image.open(SRC_DIR / "yellowfool-neet-pg-2019-ophthalmology-q010-p3013-i1.jpg").convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    
    target_h = int(H * 0.90)
    scale = target_h / src.height
    target_w = int(src.width * scale)
    resized = src.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    pix = resized.load()
    rw, rh = resized.size
    for py in range(rh):
        for px in range(rw):
            r, g, b, a = pix[px, py]
            if r > 165 and g > 165 and b > 160 and abs(r - g) < 25 and abs(g - b) < 25:
                pix[px, py] = (0, 0, 0, 255)
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y))
    
    out_p = OUT_DIR / "medicomm-img1-neet-pg-2019-ophthalmology-q010.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

# 14. neet-pg-2019-ophthalmology-q011: Cover-Uncover Test
def render_neet_2019_q011():
    src = Image.open(SRC_DIR / "yellowfool-neet-pg-2019-ophthalmology-q011-p3013-i2.jpg").convert("RGBA")
    sw, sh = src.size
    cropped = src.crop((0, 0, sw, int(sh * 0.92)))
    
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    target_h = int(H * 0.90)
    scale = target_h / cropped.height
    target_w = int(cropped.width * scale)
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    pix = resized.load()
    rw, rh = resized.size
    for py in range(rh):
        for px in range(rw):
            r, g, b, a = pix[px, py]
            if r > 240 and g > 240 and b > 240:
                pix[px, py] = (0, 0, 0, 0)
    
    x = (W - target_w) // 2
    y = (H - target_h) // 2
    canvas.paste(resized, (x, y), resized)
    
    draw = ImageDraw.Draw(canvas)
    font_bold = get_font(22, bold=True)
    font_med = get_font(18, bold=True)
    
    draw.text((x + int(target_w * 0.22), y + int(target_h * 0.26)), "Esophoria", fill=(255, 255, 255, 255), font=font_bold, anchor="mm")
    draw.text((x + int(target_w * 0.76), y + int(target_h * 0.44)), "Eye moves", fill=(0, 210, 255, 255), font=font_med, anchor="mm")
    
    draw.text((x + int(target_w * 0.22), y + int(target_h * 0.74)), "Exophoria", fill=(255, 255, 255, 255), font=font_bold, anchor="mm")
    draw.text((x + int(target_w * 0.76), y + int(target_h * 0.94)), "Eye moves", fill=(0, 210, 255, 255), font=font_med, anchor="mm")
    
    out_p = OUT_DIR / "medicomm-img1-neet-pg-2019-ophthalmology-q011.png"
    canvas.convert("RGB").save(out_p, "PNG", optimize=True)
    print("Saved:", out_p.name)

def main():
    print("Starting rendering of remaining 14 images...")
    render_q015()
    render_q017()
    render_neet_2018_q007()
    render_q001_2019()
    render_q002_2019()
    render_q003_2019()
    render_q006_2019()
    render_q009_2019()
    render_q011_2019()
    render_q013_2019()
    render_neet_2019_q005()
    render_neet_2019_q009()
    render_neet_2019_q010()
    render_neet_2019_q011()
    print("All remaining 14 images successfully rendered!")

if __name__ == "__main__":
    main()
