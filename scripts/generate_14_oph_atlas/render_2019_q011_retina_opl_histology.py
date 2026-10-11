import random
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

def generate_retina_opl_histology(output_path):
    W, H = 1200, 900
    random.seed(101)

    # Base image: Pitch black background
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))

    # Histological slice dimensions: centered frame
    x0, y0, x1, y1 = 80, 60, 1120, 840
    slice_w = x1 - x0
    slice_h = y1 - y0

    # Retinal Layers from Outer (top/scleral side) to Inner (bottom/vitreal side):
    # Layer 1 (y0 to y0+60): Choroid / Bruch's membrane / RPE (pigmented cuboidal cells)
    # Layer 2 (y0+60 to y0+160): Photoreceptor Layer (IS/OS - inner & outer segments of rods and cones, eosinophilic palisades)
    # Layer 3 (y0+160 to y0+175): Outer Limiting Membrane (OLM - fine eosinophilic line)
    # Layer 4 (y0+175 to y0+330): Outer Nuclear Layer (ONL - dense basophilic nuclei of photoreceptors, 8-10 cell layers thick)
    # Layer 5 (y0+330 to y0+430): OUTER PLEXIFORM LAYER (OPL - synaptic fibrillar eosinophilic meshwork) <- TARGET
    # Layer 6 (y0+430 to y0+570): Inner Nuclear Layer (INL - basophilic nuclei of bipolar, horizontal, amacrine cells, 4-6 cell layers)
    # Layer 7 (y0+570 to y0+700): Inner Plexiform Layer (IPL - thick eosinophilic synaptic neuropil)
    # Layer 8 (y0+700 to y0+745): Ganglion Cell Layer (GCL - spaced large somas with prominent nucleoli)
    # Layer 9 (y0+745 to y0+780): Nerve Fiber Layer (NFL - horizontal eosinophilic axons) & Inner Limiting Membrane (ILM)

    histo = Image.new("RGBA", (slice_w, slice_h), (245, 230, 235, 255))
    hdraw = ImageDraw.Draw(histo)

    # 1. Background tissue staining gradients (Eosinophilic pink/peach foundation)
    for y in range(slice_h):
        # Vary background pink intensity
        v = int(235 + 15 * math.sin(y * 0.02))
        hdraw.line([(0, y), (slice_w, y)], fill=(v, v - 30, v - 15, 255))

    # 2. Layer 1: RPE & Choroid (y: 0 to 60)
    # Dark brown melanin granules and cuboidal pigment cells
    for _ in range(3500):
        rx = random.randint(0, slice_w - 1)
        ry = random.randint(0, 55)
        # Melanin brown granules
        c = random.choice([(60, 35, 20), (45, 25, 15), (75, 45, 25), (90, 55, 30)])
        hdraw.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=c)

    # 3. Layer 2: Photoreceptor Outer/Inner Segments (y: 60 to 160)
    # Eosinophilic vertical parallel rod & cone palisades
    for x in range(0, slice_w, 2):
        shade = random.randint(180, 220)
        hdraw.line([(x, 60), (x, 160)], fill=(shade + 20, shade - 30, shade, 180), width=1)
        # Inner segments mitochondria eosinophilia
        if random.random() < 0.3:
            y_top = random.randint(120, 150)
            y_bot = y_top + random.randint(4, 10)
            hdraw.ellipse([x - 1, y_top, x + 1, y_bot], fill=(210, 110, 140, 220))

    # 4. Layer 3: Outer Limiting Membrane (y: 160 to 165)
    # Thin eosinophilic junctional band
    for x in range(slice_w):
        hdraw.point((x, 162 + int(math.sin(x * 0.05))), fill=(180, 70, 100, 220))

    # 5. Layer 4: OUTER NUCLEAR LAYER (ONL, y: 165 to 320)
    # Densely packed small, round, intensely basophilic nuclei (rods & cones)
    # Hematoxylin deep purple/blue nuclei
    for _ in range(6500):
        nx = random.randint(2, slice_w - 3)
        ny = random.randint(168, 316)
        r = random.choice([3.5, 4.0, 4.5])
        col = random.choice([(70, 30, 85), (55, 20, 75), (80, 40, 95), (65, 25, 80)])
        hdraw.ellipse([nx - r, ny - r, nx + r, ny + r], fill=col)

    # 6. Layer 5: OUTER PLEXIFORM LAYER (OPL, y: 320 to 420) <- TARGET STRUCTURE
    # Fine eosinophilic reticular synaptic network between photoreceptor terminals and bipolar/horizontal dendrites
    # Delicate pink mesh with fine horizontal/oblique fibrillar texture
    for _ in range(3000):
        fx = random.randint(0, slice_w - 15)
        fy = random.randint(325, 415)
        length = random.randint(6, 18)
        angle = random.uniform(-0.3, 0.3)
        ex = fx + length * math.cos(angle)
        ey = fy + length * math.sin(angle)
        hdraw.line([(fx, fy), (ex, ey)], fill=(215, 130, 160, 160), width=1)
    # Occasional spherule/pedicle synaptic terminals
    for _ in range(400):
        sx = random.randint(0, slice_w - 1)
        sy = random.randint(330, 410)
        hdraw.ellipse([sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5], fill=(195, 100, 135, 180))

    # 7. Layer 6: INNER NUCLEAR LAYER (INL, y: 420 to 550)
    # Moderately packed basophilic nuclei (bipolar, horizontal, amacrine, Müller cells)
    # Slightly larger and more oval than ONL nuclei
    for _ in range(3800):
        nx = random.randint(2, slice_w - 3)
        ny = random.randint(425, 545)
        rx = random.choice([4.0, 4.5, 5.0])
        ry = random.choice([4.5, 5.0, 5.5])
        col = random.choice([(75, 35, 90), (60, 25, 80), (85, 45, 100), (95, 50, 110)])
        hdraw.ellipse([nx - rx, ny - ry, nx + rx, ny + ry], fill=col)

    # 8. Layer 7: INNER PLEXIFORM LAYER (IPL, y: 550 to 670)
    # Thick eosinophilic synaptic layer
    for _ in range(4500):
        fx = random.randint(0, slice_w - 20)
        fy = random.randint(555, 665)
        length = random.randint(8, 22)
        angle = random.uniform(-0.4, 0.4)
        ex = fx + length * math.cos(angle)
        ey = fy + length * math.sin(angle)
        hdraw.line([(fx, fy), (ex, ey)], fill=(220, 140, 165, 170), width=1)

    # 9. Layer 8: GANGLION CELL LAYER (GCL, y: 670 to 720)
    # Large, spaced multipolar neurons with abundant pale basophilic cytoplasm and large prominent nucleoli
    for gx in range(40, slice_w - 40, 85):
        gy = random.randint(680, 710)
        # Cytoplasm
        hdraw.ellipse([gx - 14, gy - 11, gx + 14, gy + 11], fill=(190, 130, 165, 230))
        # Nucleus
        hdraw.ellipse([gx - 7, gy - 6, gx + 7, gy + 6], fill=(90, 45, 105, 255))
        # Nucleolus
        hdraw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(45, 15, 60, 255))

    # 10. Layer 9: NERVE FIBER LAYER (NFL, y: 720 to 760) & ILM (y: 760)
    # Smooth horizontal eosinophilic nerve axons
    for y in range(720, 755, 2):
        hdraw.line([(0, y), (slice_w, y)], fill=(225, 150, 175, 200), width=1)
    # Inner Limiting Membrane (thin glossy line)
    hdraw.line([(0, 758), (slice_w, 758)], fill=(170, 70, 95, 255), width=2)

    # Apply soft microscopy optical blur for authentic photomicrograph appearance
    histo = histo.filter(ImageFilter.GaussianBlur(radius=0.7))

    # Paste histological slice onto black base
    base.paste(histo, (x0, y0))

    # Border frame for histology specimen slide
    draw_base = ImageDraw.Draw(base)
    draw_base.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=(51, 65, 85), width=2)

    # TARGET ARROW: POINTING DIRECTLY TO THE OUTER PLEXIFORM LAYER (OPL)
    # Target coordinate: y in slice is ~370 (y in full canvas is y0 + 370 = 430)
    target_x = x0 + 480
    target_y = y0 + 370

    # Draw slim, elegant question arrow (red/gold with high contrast)
    arrow_start_x = target_x - 180
    arrow_start_y = target_y - 120

    # Arrow shaft
    draw_base.line([(arrow_start_x, arrow_start_y), (target_x, target_y)], fill=(245, 158, 11), width=4)

    # Arrowhead
    angle = math.atan2(target_y - arrow_start_y, target_x - arrow_start_x)
    head_len = 18
    p1 = (target_x, target_y)
    p2 = (target_x - head_len * math.cos(angle - math.pi / 7), target_y - head_len * math.sin(angle - math.pi / 7))
    p3 = (target_x - head_len * math.cos(angle + math.pi / 7), target_y - head_len * math.sin(angle + math.pi / 7))
    draw_base.polygon([p1, p2, p3], fill=(245, 158, 11))

    # Question Marker Tag Pill (Strictly neutral without answer spoiler text)
    tag_w, tag_h = 160, 42
    tx0 = arrow_start_x - tag_w - 15
    ty0 = arrow_start_y - tag_h // 2
    draw_base.rounded_rectangle([tx0, ty0, tx0 + tag_w, ty0 + tag_h], radius=8, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    # Leader line to tag
    draw_base.line([(tx0 + tag_w, arrow_start_y), (arrow_start_x, arrow_start_y)], fill=(245, 158, 11), width=2)

    # Tag Text: "MARKED LAYER" (Zero spoiler)
    # Use PIL default font or simple text
    draw_base.text((tx0 + tag_w // 2, ty0 + tag_h // 2), "MARKED LAYER", fill=(245, 158, 11), anchor="mm")

    base.save(output_path, "PNG")
    return True

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/q011_retina_opl_histology.png")
    res = generate_retina_opl_histology(out)
    print("Q011 Retina OPL Histology:", res, out.exists())
