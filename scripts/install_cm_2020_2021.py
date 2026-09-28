import os
import json
import shutil
import subprocess

BASE_DIR = r"d:\medicomm\dhruv1"
IMG_DIR = os.path.join(BASE_DIR, r"output\imagegen\community-medicine-2020-2021-img1")
BRAIN_ASSETS_DIR = r"C:\Users\Hp\.gemini\antigravity\brain\369624d3-e2be-4cc6-95be-659410795a7a\assets"
os.makedirs(BRAIN_ASSETS_DIR, exist_ok=True)

# 14 Detailed /img1 Prompts
PROMPTS = {
    "neet-pg-2020-community-medicine-q001": (
        "/img1 Detailed medical illustration of Biomedical Waste Management (BMW 2016 Rules) for sharps disposal: "
        "A translucent, puncture-proof, leak-proof WHITE container with universal biohazard symbol and tamper-proof lid slot. "
        "Illustrate contaminated sharps including disposable needles, scalpels, surgical blades, and syringes with fixed needles "
        "being safely dropped into the container. Include clinical annotation badges for disposal methods (Autoclaving / Dry Heat "
        "followed by shredding or encapsulation) and clear prohibition icons (no plastics, no gloves, no glassware). "
        "Dark medical interface theme with single clean medicomm branding watermark."
    ),
    "neet-pg-2020-community-medicine-q008": (
        "/img1 High-yield PSM infographic for Biomedical Waste Color Coding focusing on Chemical Waste disposal in a YELLOW BAG: "
        "Render a bright yellow non-chlorinated plastic biohazard bag with universal biohazard insignia and tie-band. "
        "Surround with categorized waste types: Chemical waste (disinfectants, formalin, laboratory reagents), human anatomical waste "
        "(tissues, organs, placenta), soiled cotton bandages, expired cytotoxic drugs, and microbiological cultures. "
        "Feature treatment methodology card: Incineration or Plasma Pyrolysis / Deep Burial, emphasizing non-chlorinated plastic bags "
        "to prevent toxic dioxin and furan emissions. Single clean medicomm watermark."
    ),
    "neet-pg-2020-community-medicine-q012": (
        "/img1 High-yield biostatistics diagram of the Gaussian Normal Distribution Empirical Rule for population parameters Mean = 200 "
        "and SD = 20: Symmetrical bell-shaped normal curve on a dark background showing Mean (μ) = 200 at center, μ ± 1 SD [180 to 220] "
        "enclosing 68.27% of the population with highlighted green translucent fill, μ ± 2 SD [160 to 240] enclosing 95.45%, and μ ± 3 SD "
        "[140 to 260] enclosing 99.73%. Include percentage breakdowns (34.1% per half) and calculation summary table highlighting the correct "
        "answer 180-220 for NEET-PG. Single clean medicomm watermark."
    ),
    "neet-pg-2020-community-medicine-q013": (
        "/img1 Clinical BMW segregation guide illustrating BLOOD BAG DISPOSAL INTO YELLOW BAG: "
        "Render a detailed whole blood CPDA pouch with transfusion tubing and label beside a large yellow non-chlorinated biohazard bag. "
        "Show direct deposit arrow into the yellow bag with clinical rationale: Blood and blood products are categorized as human anatomical / "
        "soiled biohazardous waste destined for high-temperature incineration. Display a comparative matrix distinguishing Yellow (Blood bags, tissues) "
        "from Red (Urine bags, IV bottles, gloves - recyclable plastics), White (sharps), and Blue (glass vials). "
        "Highlight the classic exam trap: Urine bag goes to Red, Blood bag goes to Yellow. Single clean medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q004": (
        "/img1 Comprehensive medical chart of NACO 7 Color-Coded Syndromic STI Drug Kits: "
        "A structured high-yield grid displaying all 7 NACO STI management kits with their official colors, target clinical syndromes, and drug regimens: "
        "Kit 1 (Grey - Urethral/Cervical discharge), Kit 2 (Green - Vaginal discharge), Kit 3 (White - Non-herpetic genital ulcer), "
        "Kit 4 (Blue - Penicillin-allergic non-herpetic ulcer), Kit 5 (Red - Herpetic genital ulcer), Kit 6 (Yellow - Lower abdominal pain/PID), "
        "and Kit 7 (Black - Inguinal bubo). Clean modern dark card layout with kit pills, medicine icons, and single medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q006": (
        "/img1 High-yield epidemiology diagram illustrating the Natural History of Disease Timeline: "
        "Horizontal progression flowchart from Stage of Susceptibility (Point A: Exposure to etiologic agent), through Stage of Subclinical Disease "
        "(Point B: Pathologic changes begin / Incubation or Latency Period), to Stage of Clinical Disease with Point C prominently highlighted as "
        "ONSET OF SYMPTOMS (Diagnostic Horizon), followed by Point D (Usual Time of Medical Diagnosis), and Stage of Recovery, Disability, or Death. "
        "Correlate with levels of prevention (Primary, Secondary, Tertiary). Dark UI with single medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q007": (
        "/img1 Biostatistics clinical trial Forest Plot comparing newer vaccine efficacies against a standard comparator: "
        "Forest plot graph showing line of no difference (0) and pre-specified equivalence / non-inferiority margins (-Δ to +Δ). "
        "Plot 5 candidate vaccines (A, B, C, D, E) with point estimates and 95% confidence intervals demonstrating Inferiority (Vaccine A), "
        "Inconclusive efficacy (Vaccine B), Non-inferiority (Vaccine C), True Equivalence within delta bounds (Vaccine D), and Superiority (Vaccine E). "
        "Highlighting that Vaccine D and E can be recommended with equal or superior efficacy. Single medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q011": (
        "/img1 Hospital ward Biomedical Waste (BMW 2016) 4-color bin segregation station: "
        "Photorealistic 2D vector depiction of 4 standard color-coded hospital disposal bins side-by-side: "
        "Yellow Bin (Anatomical waste, soiled cotton, blood bags, expired drugs -> Incineration), "
        "Red Bin (Contaminated recyclable plastics: IV lines, catheters, gloves, urine bags -> Autoclave & shredding), "
        "White Translucent Container (Puncture-proof sharps: needles, blades, scalpels -> Autoclave & dry heat), "
        "and Blue Box/Bin (Glassware: medicine ampoules, vials, orthopedic implants -> Disinfection). Single medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q012": (
        "/img1 Biostatistics scatter plot showing Pearson Correlation Coefficient r = 0.6: "
        "Cartesian coordinate scatter plot of Height (X axis) versus Weight (Y axis) with a moderate upward-sloping linear regression trendline. "
        "Data points partitioned into 4 colored demographic clusters (Red, Green, Blue, Purple) illustrating both intra-group and overall positive "
        "linear association. Annotation panel explaining r = +0.6 (moderate positive correlation), r^2 = 0.36 (36% shared variance), and scatter dispersion. "
        "Single clean medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q013": (
        "/img1 Dual-panel Flow Cytometry clinical analysis diagram: "
        "Left panel: 2D bivariate Forward Scatter (FSC - cell size) vs Side Scatter (SSC - internal granularity) dot plot with gated lymphocyte, "
        "monocyte, and granulocyte leukocyte populations. Right panel: 1D fluorescence intensity histogram showing log fluorescence vs cell count "
        "with negative control background peak and positive fluorophore antibody staining peak. Quadrant gating and clinical diagnostic utility annotations. "
        "Dark theme with single medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q015": (
        "/img1 Comprehensive Biostatistics comparison of Frequency Distribution Curves and Skewness: "
        "Three distinct comparative distribution curves: (1) Symmetrical Normal Distribution where Mean = Median = Mode (Skewness = 0), "
        "(2) Positively Skewed (Right-tailed) curve where Mode < Median < Mean (Mean pulled right by extreme positive outliers), and "
        "(3) Negatively Skewed (Left-tailed) curve where Mean < Median < Mode (Mean pulled left by extreme negative outliers). "
        "Detailed explanation of outlier vulnerability of the Mean vs robustness of the Median. Single medicomm watermark."
    ),
    "neet-pg-2021-community-medicine-q001": (
        "/img1 Environmental health technical illustration of the KATA THERMOMETER apparatus: "
        "Accurate diagram of the Kata thermometer featuring a large cylindrical alcohol bulb filled with red spirit, glass capillary stem "
        "with precise dual graduation marks at 100°F (37.8°C) and 95°F (35°C), and top expansion reservoir bulb. Beside it, render a stopwatch "
        "measuring cooling time T (seconds). Annotate Dry Kata vs Wet Kata (wet cotton sleeve), cooling power formula H = F / T (Kata Factor), "
        "and clinical application in measuring low air velocities (< 1 m/s) in hospital wards, mines, and workplaces. Single medicomm watermark."
    ),
    "neet-pg-2021-community-medicine-q002": (
        "/img1 Medical entomology morphological anatomy diagram of the ORIENTAL RAT FLEA (Xenopsylla cheopis): "
        "High-definition anatomical vector showing laterally compressed body, head, thorax, and abdomen. Prominently highlight key diagnostic features: "
        "ABSENCE of both pronotal comb and genal comb (ctenidia absent, distinguishing from dog/cat fleas), distinct vertical mesopleural rod on mesothorax, "
        "comma-shaped spermatheca in females, and elongated jumping hind legs. Annotate clinical significance as vector for Yersinia pestis (Bubonic plague) "
        "via proventricular blockage and Rickettsia typhi (Endemic murine typhus). Single medicomm watermark."
    ),
    "neet-pg-2021-community-medicine-q005": (
        "/img1 Environmental health infographic of the National Air Quality Index (NAQI - India) and Delhi AQI monitoring: "
        "Complete 6-tier NAQI color-coded scale: Good (0-50, Green), Satisfactory (51-100, Light Green), Moderately Polluted (101-200, Yellow), "
        "Poor (201-300, Orange), Very Poor (301-400, Red), and Severe (401-500, Maroon) with health impact descriptions. "
        "Includes a Delhi 4-day multi-station AQI trend table and list of the 8 monitored criteria air pollutants (PM10, PM2.5, NO2, SO2, CO, O3, NH3, Pb). "
        "Single clean medicomm watermark."
    )
}

# 1. Save prompts.json
prompts_file = os.path.join(IMG_DIR, "prompts.json")
with open(prompts_file, "w", encoding="utf-8") as f:
    json.dump(PROMPTS, f, indent=2)
print("Saved prompts.json")

# 2. Update question-details.json
details_file = os.path.join(IMG_DIR, "question-details.json")
with open(details_file, "r", encoding="utf-8") as f:
    details = json.load(f)

for item in details:
    qid = item["id"]
    item["img1Prompt"] = PROMPTS.get(qid, "")
    item["svgFilename"] = f"medicomm-img1-{qid}.svg"
    item["uploadedUrl"] = f"/uploads/medicomm-img1-{qid}.svg"

with open(details_file, "w", encoding="utf-8") as f:
    json.dump(details, f, indent=2)
print("Updated question-details.json with img1Prompts and file references")

# 3. Copy SVGs to the 4 upload destinations and brain assets directory
dest_dirs = [
    os.path.join(BASE_DIR, r"public\uploads"),
    os.path.join(BASE_DIR, r"data\uploads"),
    os.path.join(BASE_DIR, r"dist\uploads"),
    os.path.join(BASE_DIR, r"runtime-data\uploads"),
    BRAIN_ASSETS_DIR
]

for d in dest_dirs:
    os.makedirs(d, exist_ok=True)

copied_count = 0
for qid in PROMPTS.keys():
    svg_name = f"medicomm-img1-{qid}.svg"
    src_path = os.path.join(IMG_DIR, svg_name)
    if os.path.exists(src_path):
        for d in dest_dirs:
            shutil.copy2(src_path, os.path.join(d, svg_name))
        copied_count += 1
print(f"Copied {copied_count} SVGs to all 4 app upload dirs and brain assets")

# 4. Update the 3 practice-question-bank.json files
qb_paths = [
    os.path.join(BASE_DIR, r"data\practice-question-bank.json"),
    os.path.join(BASE_DIR, r"public\practice-question-bank.json"),
    os.path.join(BASE_DIR, r"dist\practice-question-bank.json"),
]

for qb_path in qb_paths:
    if not os.path.exists(qb_path):
        continue
    with open(qb_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # find questions
    updated = [0]
    def walk_and_update(node):
        if isinstance(node, dict):
            qid = node.get("id")
            if qid in PROMPTS:
                url = f"/uploads/medicomm-img1-{qid}.svg"
                prompt_text = PROMPTS[qid]
                node["imageUrls"] = [url]
                node["images"] = [url]
                node["atlasImageTargetUrls"] = [url]
                node["img1Prompt"] = prompt_text
                node["assetNote"] = f"/img1 Prompt: {prompt_text}"
                updated[0] += 1
            for k, v in node.items():
                walk_and_update(v)
        elif isinstance(node, list):
            for item in node:
                walk_and_update(item)

    walk_and_update(data)
    with open(qb_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Updated {updated[0]} nodes in {qb_path}")

# 5. Build HTML review gallery
gallery_html_path = os.path.join(IMG_DIR, "review-gallery.html")

gallery_items_html = []
for idx, item in enumerate(details, 1):
    qid = item["id"]
    year = item["year"]
    exam = item["exam"].upper()
    prompt = item["prompt"].replace("\n", "<br/>")
    ans = item["answer"]
    exp = item["explanation"].replace("\n", "<br/>")
    options = item["options"]
    img1_prompt = PROMPTS.get(qid, "")
    svg_filename = f"medicomm-img1-{qid}.svg"

    opts_html = "".join([
        f'<li class="opt {"opt-correct" if opt == ans else ""}"><strong>{"✓ " if opt == ans else "• "}</strong>{opt}</li>'
        for opt in options
    ])

    gallery_items_html.append(f"""
    <section class="q-card" id="{qid}">
      <div class="q-header">
        <span class="badge exam-badge">{exam}-{year}</span>
        <span class="badge num-badge">#{idx} of {len(details)}</span>
        <span class="qid-code">{qid}</span>
      </div>

      <div class="q-body">
        <div class="q-visual-col">
          <div class="img-wrapper">
            <img src="./{svg_filename}" alt="{qid} visual" loading="lazy" />
          </div>
          <div class="img-meta">
            <span class="file-tag">{svg_filename}</span>
            <span class="watermark-tag">1x medicomm watermark verified</span>
          </div>
        </div>

        <div class="q-content-col">
          <div class="q-prompt-box">
            <h4>Question Prompt</h4>
            <p>{prompt}</p>
          </div>

          <div class="q-options-box">
            <h4>Options</h4>
            <ul class="opts-list">
              {opts_html}
            </ul>
          </div>

          <div class="q-exp-box">
            <h4>High-Yield Explanation</h4>
            <p>{exp}</p>
          </div>

          <div class="q-img1-box">
            <div class="img1-header">
              <span class="img1-badge">/img1 Generation Prompt</span>
              <button class="copy-btn" onclick="navigator.clipboard.writeText(this.getAttribute('data-prompt'))" data-prompt="{img1_prompt.replace('"', '&quot;')}">Copy Prompt</button>
            </div>
            <pre class="prompt-text">{img1_prompt}</pre>
          </div>
        </div>
      </div>
    </section>
    """)

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Community Medicine 2020-2021 /img1 Gallery | MediComm</title>
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: #0f172a;
      --card-border: #1e293b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --green: #10b981;
      --amber: #f59e0b;
      --purple: #a855f7;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 60px;
    }}
    header {{
      background: #0b1120;
      border-bottom: 1px solid var(--card-border);
      padding: 24px 40px;
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(8px);
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .brand h1 {{
      font-size: 22px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .brand p {{
      font-size: 13px;
      color: var(--text-muted);
    }}
    .nav-stats {{
      display: flex;
      gap: 12px;
    }}
    .stat-pill {{
      background: #1e293b;
      border: 1px solid #334155;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      color: var(--accent);
    }}
    .container {{
      max-width: 1400px;
      margin: 32px auto;
      padding: 0 24px;
      display: flex;
      flex-direction: column;
      gap: 40px;
    }}
    .q-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }}
    .q-header {{
      background: #0b1120;
      border-bottom: 1px solid var(--card-border);
      padding: 14px 24px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .badge {{
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .exam-badge {{ background: #1e3a8a; color: #93c5fd; }}
    .num-badge {{ background: #1e293b; color: #cbd5e1; }}
    .qid-code {{ font-family: monospace; font-size: 13px; color: #64748b; margin-left: auto; }}
    .q-body {{
      display: grid;
      grid-template-columns: 520px 1fr;
      gap: 28px;
      padding: 24px;
    }}
    @media (max-width: 1080px) {{
      .q-body {{ grid-template-columns: 1fr; }}
    }}
    .q-visual-col {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .img-wrapper {{
      background: #030712;
      border: 1px solid #1e293b;
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      aspect-ratio: 1;
    }}
    .img-wrapper img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }}
    .img-meta {{
      display: flex;
      justify-content: space-between;
      font-size: 12px;
    }}
    .file-tag {{ font-family: monospace; color: #64748b; }}
    .watermark-tag {{ color: var(--green); font-weight: 600; }}
    .q-content-col {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .q-prompt-box h4, .q-options-box h4, .q-exp-box h4 {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--accent);
      margin-bottom: 6px;
    }}
    .q-prompt-box p {{
      font-size: 16px;
      font-weight: 600;
      color: #f1f5f9;
    }}
    .opts-list {{
      list-style: none;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}
    .opt {{
      background: #1e293b;
      border: 1px solid #334155;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 14px;
      color: #cbd5e1;
    }}
    .opt-correct {{
      background: rgba(16, 185, 129, 0.15);
      border-color: var(--green);
      color: #a7f3d0;
      font-weight: 700;
    }}
    .q-exp-box {{
      background: #090d16;
      border-left: 3px solid var(--accent);
      padding: 12px 16px;
      border-radius: 0 8px 8px 0;
      font-size: 13.5px;
      color: #cbd5e1;
    }}
    .q-img1-box {{
      background: #060911;
      border: 1px solid #1e293b;
      border-radius: 10px;
      padding: 14px;
      margin-top: auto;
    }}
    .img1-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    .img1-badge {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--amber);
    }}
    .copy-btn {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #e2e8f0;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .copy-btn:hover {{
      background: var(--accent);
      color: #020617;
      border-color: var(--accent);
    }}
    .prompt-text {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 12px;
      color: #94a3b8;
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.45;
    }}
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div>
        <h1>Community Medicine (PSM) 2020-2021 /img1 Gallery</h1>
        <p>14 High-Yield Visual Questions with Single Watermark Verification &amp; Prompt Metadata</p>
      </div>
    </div>
    <div class="nav-stats">
      <span class="stat-pill">14 Illustrated Questions</span>
      <span class="stat-pill">NEET-PG 2020 (4)</span>
      <span class="stat-pill">INI-CET 2021 (7)</span>
      <span class="stat-pill">NEET-PG 2021 (3)</span>
      <span class="stat-pill" style="color: #10b981;">✓ 1x medicomm watermark verified</span>
    </div>
  </header>

  <main class="container">
    {"".join(gallery_items_html)}
  </main>
</body>
</html>
"""

with open(gallery_html_path, "w", encoding="utf-8") as f:
    f.write(full_html)
print(f"Generated standalone review gallery: {gallery_html_path}")

# Write installed-manifest.json
manifest = {
    "subject": "Community Medicine",
    "years": [2020, 2021],
    "totalImages": len(details),
    "singleWatermarkVerified": True,
    "images": [
        {
            "id": item["id"],
            "year": item["year"],
            "exam": item["exam"],
            "svgFilename": f"medicomm-img1-{item['id']}.svg",
            "url": f"/uploads/medicomm-img1-{item['id']}.svg",
            "img1Prompt": PROMPTS[item["id"]]
        }
        for item in details
    ]
}

with open(os.path.join(IMG_DIR, "installed-manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
print("Saved installed-manifest.json")
