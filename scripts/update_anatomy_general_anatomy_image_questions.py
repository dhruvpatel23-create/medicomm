import json
import shutil
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont

DATA = Path("runtime-data/users.json")
BOOK = Path(r"F:\books\general anatomy.pdf")
CHAPTER = "General Anatomy"
UPLOAD_DIR = Path("runtime-data/uploads")


def render_crop(name, page_index, crop, marker=None):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    out = UPLOAD_DIR / name
    doc = fitz.open(BOOK)
    page = doc[page_index]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    temp = UPLOAD_DIR / f"_{name}"
    pix.save(temp)
    image = Image.open(temp).convert("RGB")
    width, height = image.size
    left, top, right, bottom = crop
    box = (int(left * width), int(top * height), int(right * width), int(bottom * height))
    cropped = image.crop(box)
    draw = ImageDraw.Draw(cropped)
    if marker:
        kind = marker.get("kind", "arrow")
        x = int(marker["x"] * cropped.width)
        y = int(marker["y"] * cropped.height)
        if kind == "number":
            r = 24
            draw.ellipse((x - r, y - r, x + r, y + r), fill=(220, 38, 38), outline=(255, 255, 255), width=4)
            try:
                font = ImageFont.truetype("arial.ttf", 28)
            except Exception:
                font = ImageFont.load_default()
            text = marker.get("text", "1")
            draw.text((x - 8, y - 15), text, fill=(255, 255, 255), font=font)
        else:
            start = (max(5, x - 105), max(5, y - 60))
            end = (x, y)
            draw.line((start, end), fill=(220, 38, 38), width=8)
            draw.polygon([(x, y), (x - 28, y - 6), (x - 12, y - 28)], fill=(220, 38, 38))
    cropped.save(out, quality=92)
    temp.unlink(missing_ok=True)
    for folder in ["data/uploads", "public/uploads", "dist/uploads"]:
        target_dir = Path(folder)
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, target_dir / out.name)
    return f"/uploads/{name}"


ASSETS = {
    "intro_surface": render_crop("anatomy-general-introduction-surface-marker.png", 14, (0.18, 0.40, 0.86, 0.89), {"x": 0.72, "y": 0.68}),
    "intro_palpation": render_crop("anatomy-general-introduction-palpation-marker.png", 14, (0.22, 0.03, 0.79, 0.38), {"kind": "number", "x": 0.50, "y": 0.45, "text": "1"}),
    "skeleton_types": render_crop("anatomy-general-skeleton-long-bone-marker.png", 43, (0.05, 0.03, 0.94, 0.55), {"x": 0.28, "y": 0.45}),
    "skeleton_classification": render_crop("anatomy-general-skeleton-classification-marker.png", 40, (0.06, 0.15, 0.94, 0.82), {"kind": "number", "x": 0.49, "y": 0.22, "text": "1"}),
    "joints_cartilaginous": render_crop("anatomy-general-joints-cartilaginous-marker.png", 70, (0.08, 0.02, 0.92, 0.42), {"x": 0.55, "y": 0.45}),
    "joints_synovial": render_crop("anatomy-general-joints-synovial-marker.png", 68, (0.07, 0.30, 0.94, 0.86), {"kind": "number", "x": 0.62, "y": 0.54, "text": "2"}),
    "muscles_smooth": render_crop("anatomy-general-muscles-smooth-marker.png", 96, (0.08, 0.05, 0.48, 0.32), {"x": 0.47, "y": 0.40}),
    "muscles_cardiac": render_crop("anatomy-general-muscles-cardiac-marker.png", 96, (0.45, 0.05, 0.93, 0.32), {"kind": "number", "x": 0.53, "y": 0.48, "text": "1"}),
    "cardio_artery": render_crop("anatomy-general-cardiovascular-artery-marker.png", 116, (0.05, 0.20, 0.95, 0.82), {"x": 0.55, "y": 0.45}),
    "cardio_vessels": render_crop("anatomy-general-cardiovascular-vessels-marker.png", 112, (0.05, 0.28, 0.95, 0.86), {"kind": "number", "x": 0.36, "y": 0.58, "text": "1"}),
    "lymph_relation": render_crop("anatomy-general-lymphatic-relation-marker.png", 136, (0.06, 0.03, 0.94, 0.55), {"x": 0.63, "y": 0.48}),
    "lymph_drainage": render_crop("anatomy-general-lymphatic-drainage-marker.png", 134, (0.06, 0.22, 0.94, 0.85), {"kind": "number", "x": 0.50, "y": 0.45, "text": "1"}),
    "nervous_neuron": render_crop("anatomy-general-nervous-neuron-marker.png", 154, (0.06, 0.03, 0.94, 0.58), {"x": 0.63, "y": 0.52}),
    "nervous_polarity": render_crop("anatomy-general-nervous-polarity-marker.png", 154, (0.05, 0.46, 0.95, 0.92), {"kind": "number", "x": 0.39, "y": 0.45, "text": "1"}),
    "skin_lines": render_crop("anatomy-general-skin-tension-lines-marker.png", 186, (0.05, 0.03, 0.95, 0.46), {"x": 0.54, "y": 0.38}),
    "skin_fascia": render_crop("anatomy-general-skin-fascia-marker.png", 182, (0.06, 0.21, 0.94, 0.84), {"kind": "number", "x": 0.46, "y": 0.55, "text": "1"}),
    "ct_orbit": render_crop("anatomy-general-connective-orbit-marker.png", 208, (0.05, 0.03, 0.95, 0.50), {"x": 0.58, "y": 0.45}),
    "ct_pulley": render_crop("anatomy-general-connective-pulley-marker.png", 208, (0.05, 0.40, 0.95, 0.85), {"kind": "number", "x": 0.52, "y": 0.45, "text": "1"}),
    "radio_xray": render_crop("anatomy-general-radiography-xray-marker.png", 218, (0.05, 0.03, 0.95, 0.48), {"x": 0.55, "y": 0.46}),
    "radio_density": render_crop("anatomy-general-radiography-density-marker.png", 216, (0.05, 0.20, 0.95, 0.82), {"kind": "number", "x": 0.42, "y": 0.48, "text": "1"}),
}


def replacement(prompt, answer, wrong, explanation, image_key):
    return {
        "prompt": prompt,
        "answer": answer,
        "wrong": wrong,
        "explanation": explanation,
        "imageUrls": [ASSETS[image_key]],
    }


UPDATES = {
    "anatomy-general-introduction-01": replacement("In the marked book figure, the examiner is palpating an artery on the dorsum of the foot. Which subdivision of anatomy is being applied?", "Surface anatomy", ["Histology", "Comparative anatomy", "Physical anthropology"], "Surface anatomy correlates deeper structures such as arteries with surface landmarks used clinically.", "intro_surface"),
    "anatomy-general-introduction-02": replacement("The numbered image shows contracted muscle being examined in a living subject. This is an example of:", "Living anatomy", ["Cadaveric anatomy", "Embryology", "Genetics"], "Living anatomy studies structures in living subjects by inspection, palpation, imaging, and functional examination.", "intro_palpation"),
    "anatomy-general-skeleton-01": replacement("In the marked figure of bone classification, the arrow indicates a bone with a shaft and expanded ends. This bone type is:", "Long bone", ["Flat bone", "Sesamoid bone", "Pneumatic bone"], "Long bones have a diaphysis and epiphyses and act as levers for movement.", "skeleton_types"),
    "anatomy-general-skeleton-02": replacement("In the numbered skeleton figure, the marked axial framework primarily functions as:", "Support and protection of vital organs", ["Production of synovial fluid", "Voluntary contraction", "Impulse conduction"], "The skeleton provides support, protection, leverage, mineral storage, and marrow spaces.", "skeleton_classification"),
    "anatomy-general-joints-01": replacement("The marked figure represents an amphiarthrosis between vertebral bodies. Structurally, this is a:", "Secondary cartilaginous joint", ["Plane synovial joint", "Fibrous suture", "Primary cartilaginous joint"], "Intervertebral symphyses are secondary cartilaginous joints united by fibrocartilage.", "joints_cartilaginous"),
    "anatomy-general-joints-02": replacement("In the numbered joint diagram, the marked cavity-containing articulation is best classified as:", "Synovial joint", ["Suture", "Gomphosis", "Synchondrosis"], "Synovial joints have a joint cavity, capsule, synovial membrane, and articular cartilage.", "joints_synovial"),
    "anatomy-general-muscles-01": replacement("The arrow marks non-striated spindle-shaped muscle cells in the book figure. Which muscle type is shown?", "Smooth muscle", ["Skeletal muscle", "Cardiac muscle", "Dense regular connective tissue"], "Smooth muscle is non-striated, involuntary, and typically spindle-shaped with central nuclei.", "muscles_smooth"),
    "anatomy-general-muscles-02": replacement("The numbered muscle image shows branching striated fibers joined by intercalated discs. This tissue is:", "Cardiac muscle", ["Smooth muscle", "Skeletal muscle", "Hyaline cartilage"], "Cardiac muscle is striated, involuntary, branching, and connected by intercalated discs.", "muscles_cardiac"),
    "anatomy-general-cardiovascular-system-01": replacement("The marked vessel-wall diagram emphasizes the thick muscular middle coat. Which layer is primarily indicated?", "Tunica media", ["Tunica intima", "Tunica adventitia", "Endocardium"], "Tunica media contains smooth muscle and elastic tissue and is especially prominent in arteries.", "cardio_artery"),
    "anatomy-general-cardiovascular-system-02": replacement("In the numbered cardiovascular figure, the marked vessel carries blood away from the heart. It should be classified as:", "Artery", ["Vein", "Lymphatic", "Venule"], "Arteries are defined by direction of blood flow away from the heart, not by oxygen content.", "cardio_vessels"),
    "anatomy-general-lymphatic-system-01": replacement("The arrow in the lymphatic-circulatory relation figure points to drainage returning tissue fluid toward the venous system. This system is:", "Lymphatic system", ["Portal venous system", "Arterial tree", "Synovial system"], "The lymphatic system returns excess interstitial fluid and proteins to the venous circulation.", "lymph_relation"),
    "anatomy-general-lymphatic-system-02": replacement("The numbered lymphatic image represents blind-ended channels in tissues. Their main function is to:", "Absorb excess interstitial fluid", ["Generate arterial pulse", "Secrete bile", "Produce myelin"], "Lymph capillaries begin blindly and collect tissue fluid that is returned to veins.", "lymph_drainage"),
    "anatomy-general-nervous-system-01": replacement("In the marked neuron diagram, the arrow points to a process conducting impulses away from the cell body. This process is the:", "Axon", ["Dendrite", "Synapse", "Nissl body"], "The axon carries impulses away from the soma; dendrites usually carry impulses toward it.", "nervous_neuron"),
    "anatomy-general-nervous-system-02": replacement("The numbered diagram demonstrates dynamic polarity of neurons. In a typical neuron, impulse flow in dendrites is:", "Toward the soma", ["Away from the soma", "Only across myelin", "Only through Schwann cells"], "Dendrites generally conduct impulses toward the cell body, while axons conduct away.", "nervous_polarity"),
    "anatomy-general-skin-and-fasciae-01": replacement("The marked lines on the skin figure are surgically important because incisions parallel to them:", "Gap less and heal with a better scar", ["Always avoid arteries", "Do not need sutures", "Prevent all infection"], "Skin tension/cleavage lines reflect dermal collagen orientation; parallel incisions usually heal better.", "skin_lines"),
    "anatomy-general-skin-and-fasciae-02": replacement("In the numbered skin/fascia figure, the marked subcutaneous layer corresponds mainly to:", "Superficial fascia", ["Deep fascia", "Articular cartilage", "Periosteum"], "Superficial fascia is the subcutaneous loose connective tissue and fat between skin and deep fascia.", "skin_fascia"),
    "anatomy-general-connective-tissue-ligaments-raphe-01": replacement("The marked orbital connective tissue structure in the figure restrains displacement of an extraocular muscle. It is best described as a:", "Check ligament", ["Synovial bursa", "Sesamoid bone", "Motor end plate"], "Check ligaments are fascial connective tissue specializations that limit excessive muscle movement.", "ct_orbit"),
    "anatomy-general-connective-tissue-ligaments-raphe-02": replacement("The numbered fibrous pulley-like structure in the book figure represents dense connective tissue organized mainly to:", "Redirect or restrain tendon/muscle pull", ["Conduct nerve impulses", "Form red marrow", "Secrete synovial fluid"], "Fibrous pulleys and retinacula are dense connective tissue structures that guide or restrain tendons/muscles.", "ct_pulley"),
    "anatomy-general-principles-of-radiography-01": replacement("In the marked radiography figure, the bright white regions correspond to structures that are:", "Radiopaque", ["Radiolucent", "Anechoic", "Hypointense on all MRI sequences"], "Radiopaque structures attenuate X-rays strongly and appear white on a radiograph.", "radio_xray"),
    "anatomy-general-principles-of-radiography-02": replacement("The numbered radiography image is testing image density. Air-filled regions on plain X-ray appear black because they are:", "Radiolucent", ["Radiopaque", "Calcified", "Metallic"], "Air allows X-rays to pass through easily, creating black radiolucent areas on X-ray.", "radio_density"),
}


def main():
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    seen = set()
    for question in data.get("questions", []):
        update = UPDATES.get(question.get("id"))
        if not update:
            continue
        seen.add(question["id"])
        options = list(update["wrong"])
        answer_index = question["answerIndex"]
        options.insert(answer_index, update["answer"])
        question["prompt"] = update["prompt"]
        question["options"] = options
        question["answer"] = update["answer"]
        question["explanation"] = update["explanation"]
        question["imageUrls"] = update["imageUrls"]
        question["difficulty"] = "very high"
    missing = sorted(set(UPDATES) - seen)
    if missing:
        raise AssertionError(f"Missing questions to update: {missing}")
    qs = [q for q in data.get("questions", []) if q.get("subjectId") == "anatomy" and q.get("chapterTitle") == CHAPTER]
    if len(qs) != 100:
        raise AssertionError(f"Expected 100 General Anatomy questions, got {len(qs)}")
    image_count = sum(1 for q in qs if q.get("imageUrls"))
    if image_count < 20:
        raise AssertionError(f"Expected at least 20 image questions, got {image_count}")
    if any(q["answer"] != q["options"][q["answerIndex"]] for q in qs):
        raise AssertionError("Bad answer index after update")
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {len(UPDATES)} General Anatomy questions with rendered/cropped book images.")


if __name__ == "__main__":
    main()
