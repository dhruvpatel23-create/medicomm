import hashlib
import html
import json
from pathlib import Path

ROOT = Path(r"d:\medullaprep\dhruv1")
OUT = ROOT / "output" / "imagegen" / "ophthalmology-2017-2019-img1"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

reviews = {
    "aiims-2017-ophthalmology-q001": "Retroillumination slit lamp view through dilated pupil following cataract surgery showing Posterior Capsular Opacification (PCO) / After-cataract with clustered globular translucent Elschnig's pearls behind the IOL optic; pure black #000000 background; DAILYROUNDS watermark removed.",
    "aiims-2017-ophthalmology-q003": "Grayscale Fundus Fluorescein Angiography (FFA) of Proliferative Diabetic Retinopathy (PDR) showing leaking hyperfluorescent Neovascularization Elsewhere (NVE) along the superotemporal arcade and microaneurysms on pure black background; zero watermarks.",
    "aiims-2017-ophthalmology-q004": "Neutral stylized clinical portrait of upper orbital region in primary gaze showing Right Eye Esotropia (convergent strabismus due to right 6th nerve / abducens palsy): right eye deviated inward, left eye fixating straight ahead; DAILYROUNDS watermark removed; pure black background.",
    "aiims-2017-ophthalmology-q006": "Optical ray diagram of Myopia: eyeball cross-section with cornea, lens, optical axis, and parallel incoming light rays refracting to a sharp focal point anterior to the vertical retinal plane; pure black background; zero text spoilers.",
    "aiims-2017-ophthalmology-q007": "High-magnification anterior segment view of nasal Pterygium: fleshy triangular vascularized subconjunctival fold crossing limbus and encroaching onto clear cornea over pupil margin; glistening surface; pure black framing; zero watermarks.",
    "aiims-2017-ophthalmology-q011": "Slit lamp examination demonstrating Dynamic Contour Tonometry (Pascal Tonometer) measuring IOP: tonometer probe gently apposed to cornea with digital LCD screen displaying tack-sharp readout 'IOP: 14.6 mmHg' and 'OPA: 2.8'; stylized profile model; pure black background.",
    "aiims-2017-ophthalmology-q013": "Sagittal anatomical dissection of the orbit showing globe, extraocular muscles, optic nerve, ciliary ganglion, with a single slim gold pointer precisely targeting the Medial Rectus muscle belly (supplied by CN III from superior colliculus level); pure black background; zero spoiler labels.",
    
    "aiims-2018-ophthalmology-q005": "High-power authentic retinal histopathology (H&E stain, 400x) showing smooth dome-shaped eosinophilic hyaline Drusen nodule between Bruch's membrane and RPE with melanin granules; panel letter 'C' in crisp sans-serif; zero spoiler text.",
    "aiims-2018-ophthalmology-q006": "Late-phase Fundus Fluorescein Angiography (FFA) demonstrating Cystoid Macular Edema (CME): pathognomonic petaloid / flower-petal pooling of fluorescein dye in cystic spaces around fovea and hot leaking optic disc; circular fundus on pure black background.",
    "aiims-2018-ophthalmology-q009": "Dual-panel clinical presentation of Bull's Eye Maculopathy (chloroquine retinopathy): left circular panel color fundus photo showing macular ring of RPE atrophy; right circular panel FFA showing corresponding hyperfluorescent window defect ring; pure black background.",
    "aiims-2018-ophthalmology-q013": "Retinal histopathology cross-section (H&E stain, 400x) clearly stratifying retinal layers with clean horizontal black pointer precisely targeting the Inner Plexiform Layer (IPL); zero answer spoilers; zero watermarks.",
    "aiims-2018-ophthalmology-q014": "Close-up optical textbook illustration of Bifocal corrective eyeglasses resting on an open book, showing the curved semicircular reading segment dividing line with magnified text underneath; pure black framing; zero watermarks.",
    "aiims-2018-ophthalmology-q015": "Stylized clinical portrait of child with unilateral facial Port-Wine Stain (nevus flammeus) in right V1/V2 dermatome (Sturge-Weber syndrome / glaucoma); DAILYROUNDS watermark removed; pure black background vignette.",
    "aiims-2018-ophthalmology-q017": "9-cardinal gaze motility montage demonstrating Left Oculomotor Nerve (CN III) Palsy: primary gaze shows ptosis and down-and-out deviation; impaired elevation, depression, and adduction with preserved abduction; high-contrast panels on pure black background.",
    "neet-pg-2018-ophthalmology-q007": "Clinical anterior segment macro view of acute postoperative endophthalmitis showing intense ciliary injection, corneal haze, and a distinct horizontal hypopyon fluid level in anterior chamber; pure black background vignette; zero watermarks.",
    
    "aiims-2019-ophthalmology-q001": "Circular fundus photograph of Choroidal Melanoma: elevated dark brown-pigmented dome in posterior pole with overlying lipofuscin clumps and draped retinal vessels; pure solid black #000000 background; zero watermarks.",
    "aiims-2019-ophthalmology-q002": "Titmus Stereotest apparatus showing open booklet with 3D housefly and Wirt graded circles, alongside cross-polarized 3D glasses on solid black background; zero watermarks; no answer text.",
    "aiims-2019-ophthalmology-q003": "High-magnification ocular trauma view of metallic barbed fish hook penetrating cornea into anterior chamber with peaked teardrop pupil; pure black background vignette; zero watermarks.",
    "aiims-2019-ophthalmology-q006": "3-stage clinical diagram of Swinging Flashlight Test for Relative Afferent Pupillary Defect (RAPD / Marcus Gunn pupil): baseline, left eye illumination (normal bilateral constriction), and right eye illumination (paradoxical bilateral dilation); MARROW watermark removed; bold 'R' and 'L' labels.",
    "aiims-2019-ophthalmology-q009": "Fundus Fluorescein Angiography (FFA) of Diabetic Macular Ischemia: markedly enlarged and irregular foveal avascular zone (FAZ) with extensive perifoveal capillary dropout; high contrast on pure black background; zero watermarks.",
    "aiims-2019-ophthalmology-q011": "High-power retinal histology (H&E stain, 400x) with restyled slim gold pointer precisely indicating the Outer Plexiform Layer (OPL); answer key text artifact removed; zero spoiler labels; authentic morphology.",
    "aiims-2019-ophthalmology-q013": "Surgical anatomical illustration of Anterior Ethmoidal Nerve Block: needle trajectory inserted at medial canthus / frontoethmoidal suture; MARROW watermark 100% removed; pure black background; zero answer spoilers.",
    "neet-pg-2019-ophthalmology-q005": "Coronal facial CT scan (bone window) of Orbital Floor Blowout Fracture showing disrupted floor with herniation of orbital fat and inferior rectus into maxillary sinus ('hanging drop' sign); restyled cyan elliptical marker; pure black background.",
    "neet-pg-2019-ophthalmology-q006": "High-magnification anterior segment view of nasal Pterygium: fleshy triangular fibrovascular tissue encroaching onto cornea; glistening reflex; solid pure black #000000 frame; zero watermarks.",
    "neet-pg-2019-ophthalmology-q009": "Ex-PRESS Glaucoma Filtration Device: dual diagram showing top precision metallic shunt with retention spur and bottom anterior chamber cross-section showing drainage under scleral flap; MARROW watermark 100% removed; bold sans-serif anatomical labels.",
    "neet-pg-2019-ophthalmology-q010": "Optical diagnostic instrument photograph of Maddox Rod trial disc with red parallel cylindrical rods and handle beside silver penlight, isolated on solid pure black #000000 background; zero watermarks.",
    "neet-pg-2019-ophthalmology-q011": "Multi-stage Cover-Uncover Test clinical diagram demonstrating Esophoria and Exophoria: binocular fixation, occlusion producing deviation, and unocclusion recovery movement; MARROW watermark 100% removed; crisp bold labels."
}

items = []
list_data = json.loads((ROOT / "scripts" / "all_27_detailed_review.json").read_text(encoding="utf-8"))

for item in list_data:
    q_id = item["id"]
    png_name = f"medicomm-img1-{q_id}.png"
    src_name = f"source-{q_id}.jpg"
    png_path = OUT / png_name
    src_path = OUT / src_name
    
    assert png_path.is_file(), f"Missing PNG: {png_name}"
    assert src_path.is_file(), f"Missing Source: {src_name}"
    
    item_review = {
        "id": q_id,
        "sourceFile": src_name,
        "filename": png_name,
        "visuallyReviewed": True,
        "review": reviews[q_id],
        "sha256": digest(png_path),
        "targetUrl": f"/uploads/{png_name}"
    }
    items.append(item_review)

(OUT / "reviewed-images.json").write_text(json.dumps(items, indent=2), encoding="utf-8")
print(f"Wrote {len(items)} reviewed items to reviewed-images.json")

# Generate HTML review gallery
cards = []
for i in items:
    cards.append(f'''<article style="background:#1e1e1e;border-radius:8px;padding:16px;margin-bottom:24px;border:1px solid #333;">
  <h2 style="margin:0 0 12px 0;color:#38bdf8;">{html.escape(i["id"])}</h2>
  <div style="display:flex;gap:16px;align-items:flex-start;">
    <div style="flex:1;">
      <p style="color:#94a3b8;margin:0 0 8px 0;font-weight:bold;font-size:14px;">Original Source PYQ Reference</p>
      <img src="{i["sourceFile"]}" style="max-width:100%;border-radius:6px;border:1px solid #444;" alt="Source">
    </div>
    <div style="flex:1;">
      <p style="color:#34d399;margin:0 0 8px 0;font-weight:bold;font-size:14px;">Medicomm /img1 Educational Illustration (Copyright-Safe)</p>
      <img src="{i["filename"]}" style="max-width:100%;border-radius:6px;border:1px solid #444;" alt="Replacement">
    </div>
  </div>
  <div style="margin-top:12px;background:#111;padding:10px 14px;border-radius:6px;border-left:4px solid #38bdf8;">
    <p style="color:#e2e8f0;margin:0;font-size:14px;line-height:1.5;"><strong>Scientific &amp; Visual Verification:</strong> {html.escape(i["review"])}</p>
  </div>
</article>''')

gallery_html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Ophthalmology 2017-2019 /img1 Review Gallery</title>
  <style>
    body {{ background:#0f172a; color:#f8fafc; font-family:system-ui,-apple-system,sans-serif; margin:24px auto; max-width:1200px; padding:0 16px; }}
    h1 {{ font-size:26px; border-bottom:2px solid #334155; padding-bottom:12px; color:#f1f5f9; }}
    .badge {{ display:inline-block; padding:4px 10px; background:#0ea5e9; color:#fff; border-radius:12px; font-size:12px; font-weight:bold; margin-left:12px; vertical-align:middle; }}
  </style>
</head>
<body>
  <h1>Ophthalmology 2017, 2018 &amp; 2019: Source vs. Medicomm /img1 Visual Verification <span class="badge">27 of 27 Verified</span></h1>
  {''.join(cards)}
</body>
</html>'''

(OUT / "review-gallery.html").write_text(gallery_html, encoding="utf-8")
print("Wrote review-gallery.html")
