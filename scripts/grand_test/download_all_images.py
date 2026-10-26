import urllib.request
import urllib.parse
import json
import ssl
import subprocess
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT_DIR = r"D:\medullaprep\dhruv1\public\uploads\grand_test"
os.makedirs(OUT_DIR, exist_ok=True)

IMAGE_TARGETS = [
    ("fmge-gt1-q001", ["Radial nerve Gray817", "Radial nerve arm", "Radial nerve anatomy"]),
    ("fmge-gt1-q003", ["Cavernous sinus Gray570", "Cavernous sinus", "Cavernous sinus anatomy"]),
    ("fmge-gt1-q038", ["Tendon xanthoma", "Xanthoma tendon", "Xanthoma"]),
    ("fmge-gt1-q046", ["Cherry red spot macula", "Cherry red spot retina", "Cherry-red spot"]),
    ("fmge-gt1-q052", ["Hodgkin Disease, Reed-Sternberg Cell", "Reed-Sternberg cell", "Reed-Sternberg"]),
    ("fmge-gt1-q055", ["Signet ring cell carcinoma", "Signet ring cells stomach", "Signet ring cell"]),
    ("fmge-gt1-q058", ["Amyloidosis, Congo red", "Congo red amyloidosis", "Amyloid Congo red"]),
    ("fmge-gt1-q060", ["Papillary thyroid carcinoma fine needle aspiration", "Papillary thyroid carcinoma nuclei", "Papillary thyroid carcinoma"]),
    ("fmge-gt1-q066", ["Cryptococcus neoformans using an India ink", "Cryptococcus neoformans India ink", "Cryptococcus neoformans"]),
    ("fmge-gt1-q067", ["Negri bodies rabies", "Negri body rabies", "Negri bodies"]),
    ("fmge-gt1-q069", ["Plasmodium falciparum gametocyte", "Plasmodium falciparum ring form", "Plasmodium falciparum"]),
    ("fmge-gt1-q132", ["Central retinal artery occlusion fundus", "Central retinal artery occlusion", "Retinal artery occlusion"]),
    ("fmge-gt1-q134", ["Dendritic corneal ulcer due to HSV", "Dendritic corneal ulcer", "Herpes simplex keratitis"]),
    ("fmge-gt1-q151", ["Inferior STEMI ECG", "Inferior myocardial infarction ECG", "STEMI ECG"]),
    ("fmge-gt1-q158", ["Hypersegmented neutrophil", "Hypersegmented PMN", "Megaloblastic anemia blood smear"]),
    ("fmge-gt1-q169", ["Scrub typhus eschar", "Tsutsugamushi eschar", "Eschar scrub typhus"]),
    ("fmge-gt1-q174", ["Dawson fingers MRI", "Dawson fingers", "Multiple sclerosis Dawson fingers"]),
    ("fmge-gt1-q177", ["Gout crystals polarized", "Urate crystals polarized", "Gout crystals"]),
    ("fmge-gt1-q182", ["Bamboo spine ankylosing spondylitis", "Bamboo spine", "Ankylosing spondylitis spine x-ray"]),
    ("fmge-gt1-q185", ["Tetralogy of Fallot X-ray", "Boot shaped heart", "Tetralogy of Fallot chest x-ray"]),
    ("fmge-gt1-q189", ["Intussusception ultrasound target", "Intussusception ultrasound", "Intussusception donut sign"]),
    ("fmge-gt1-q192", ["Respiratory distress syndrome infant x-ray", "Hyaline membrane disease x-ray", "Infant respiratory distress syndrome x-ray"]),
    ("fmge-gt1-q196", ["Koplik spots measles", "Koplik spots", "Koplik's spots"]),
    ("fmge-gt1-q198", ["Rickets X-ray wrist", "Rickets X-ray", "Rickets wrists"]),
    ("fmge-gt1-q199", ["Psoriasis plaque", "Psoriasis vulgaris", "Plaque psoriasis"]),
    ("fmge-gt1-q201", ["Pemphigus vulgaris immunofluorescence", "Pemphigus vulgaris IF", "Pemphigus vulgaris histology"]),
    ("fmge-gt1-q218", ["Small bowel obstruction X-ray", "Small bowel obstruction abdominal x-ray", "Bowel obstruction x-ray"]),
    ("fmge-gt1-q221", ["Achalasia barium swallow", "Achalasia cardia barium", "Achalasia bird beak"]),
    ("fmge-gt1-q224", ["Familial adenomatous polyposis gross", "Familial adenomatous polyposis", "FAP polyps colon"]),
    ("fmge-gt1-q233", ["Clear cell renal cell carcinoma histopathology", "Clear cell renal cell carcinoma", "Renal cell carcinoma histology"]),
    ("fmge-gt1-q241", ["Colles fracture X-ray", "Colles' fracture x-ray", "Colles fracture"]),
    ("fmge-gt1-q245", ["Osteochondroma X-ray", "Osteochondroma", "Exostosis x-ray"]),
    ("fmge-gt1-q261", ["Polycystic ovary ultrasound", "PCOS ultrasound", "Polycystic ovarian syndrome ultrasound"]),
    ("fmge-gt1-q270", ["Dysgerminoma histology", "Dysgerminoma ovary", "Dysgerminoma"]),
    ("fmge-gt1-q278", ["Trichomonas vaginalis phase contrast", "Trichomonas vaginalis wet mount", "Trichomonas vaginalis"]),
    ("fmge-gt1-q284", ["Gallstone ultrasound", "Gallbladder stone ultrasound", "Gallstones ultrasound shadow"]),
    ("fmge-gt1-q291", ["Retinoblastoma leukocoria", "Retinoblastoma eye", "Retinoblastoma"]),
    ("fmge-gt1-q293", ["Central retinal vein occlusion fundus", "Central retinal vein occlusion", "CRVO fundus"]),
    ("fmge-gt1-q296", ["Vestibular schwannoma MRI", "Acoustic neuroma MRI", "Vestibular schwannoma"])
]

def search_wikimedia(query):
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(api_url, headers={"User-Agent": "MedullaPrep/1.0 (contact@medullaprep.com)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            data = json.loads(r.read())
            pages = data.get("query", {}).get("pages", {})
            for pid, info in pages.items():
                title = info.get("title", "")
                if any(title.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                    url = info["imageinfo"][0]["url"]
                    return title, url
    except Exception as e:
        pass
    return None, None

def download_file(url, out_path):
    cmd = [
        "curl.exe", "-s", "-L",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        url,
        "-o", out_path
    ]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return True
    return False

results = {}
for qid, queries in IMAGE_TARGETS:
    dest_path = os.path.join(OUT_DIR, f"{qid}.jpg")
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        print(f"[{qid}] Already downloaded ({os.path.getsize(dest_path)} bytes)")
        results[qid] = f"/uploads/grand_test/{qid}.jpg"
        continue
    
    found = False
    for q in queries:
        title, url = search_wikimedia(q)
        if url:
            print(f"[{qid}] Found '{title}' via '{q}'")
            if download_file(url, dest_path):
                print(f"[{qid}] Successfully downloaded to {dest_path} ({os.path.getsize(dest_path)} bytes)")
                results[qid] = f"/uploads/grand_test/{qid}.jpg"
                found = True
                break
    if not found:
        print(f"[{qid}] FAILED to download any image for queries: {queries}")

print(f"\nTotal downloaded successfully: {len(results)} of {len(IMAGE_TARGETS)}")
