import urllib.request
import urllib.parse
import json
import ssl
import subprocess
import os
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT_DIR = r"D:\medullaprep\dhruv1\public\uploads\grand_test"

# Specific, targeted queries for the remaining ones
REMAINING_TARGETS = [
    ("fmge-gt1-q046", ["Cherry-red spot", "Macula cherry red", "Tay Sachs retina"]),
    ("fmge-gt1-q066", ["Cryptococcus neoformans India ink", "Cryptococcus ink", "Cryptococcus neoformans"]),
    ("fmge-gt1-q132", ["Central retinal artery occlusion", "Retinal artery occlusion", "CRAO retina"]),
    ("fmge-gt1-q134", ["Dendritic ulcer cornea", "Herpes simplex keratitis", "Herpes keratitis"]),
    ("fmge-gt1-q169", ["Scrub typhus eschar", "Tsutsugamushi eschar", "Eschar mite"]),
    ("fmge-gt1-q174", ["Multiple sclerosis MRI Dawson fingers", "Dawson fingers MRI", "Dawson's fingers"]),
    ("fmge-gt1-q182", ["Bamboo spine", "Ankylosing spondylitis spine", "Ankylosing spondylitis X-ray"]),
    ("fmge-gt1-q185", ["Tetralogy of Fallot heart x-ray", "Boot shaped heart", "Tetralogy of Fallot"]),
    ("fmge-gt1-q192", ["Respiratory distress syndrome newborn x-ray", "Hyaline membrane disease", "Infant respiratory distress syndrome"]),
    ("fmge-gt1-q198", ["Rickets wrist x-ray", "Rickets cupping", "Rickets legs"]),
    ("fmge-gt1-q199", ["Psoriasis vulgaris plaque", "Plaque psoriasis back", "Psoriasis"]),
    ("fmge-gt1-q218", ["Small bowel obstruction x-ray", "Mechanical bowel obstruction x-ray", "Ileus x-ray"]),
    ("fmge-gt1-q221", ["Achalasia barium", "Achalasia bird beak", "Achalasia cardia"]),
    ("fmge-gt1-q233", ["Clear cell renal cell carcinoma", "Renal cell carcinoma histopathology", "Renal cell carcinoma"]),
    ("fmge-gt1-q241", ["Colles fracture x-ray", "Distal radius fracture x-ray", "Colles' fracture"]),
    ("fmge-gt1-q245", ["Osteochondroma x-ray", "Exostosis bone x-ray", "Osteochondroma"]),
    ("fmge-gt1-q261", ["Polycystic ovary ultrasound", "PCOS ovary ultrasound", "Polycystic ovaries"]),
    ("fmge-gt1-q270", ["Dysgerminoma histology", "Dysgerminoma ovary", "Ovarian dysgerminoma"]),
    ("fmge-gt1-q278", ["Trichomonas vaginalis", "Trichomoniasis wet mount", "Trichomonas"]),
    ("fmge-gt1-q284", ["Gallstone ultrasound", "Gallstones acoustic shadow", "Gallbladder ultrasound"]),
    ("fmge-gt1-q291", ["Retinoblastoma leukocoria", "Retinoblastoma cat's eye", "Retinoblastoma child"]),
    ("fmge-gt1-q293", ["Central retinal vein occlusion", "CRVO fundus", "Retinal vein occlusion"]),
    ("fmge-gt1-q296", ["Vestibular schwannoma MRI", "Acoustic neuroma MRI", "Vestibular schwannoma"])
]

def search_wikimedia_thumb(query):
    # Search with iiurlwidth=800 to get CDN thumbnail
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json"
    req = urllib.request.Request(api_url, headers={"User-Agent": "MedullaPrepBot/1.2 (medullaprep.learning@gmail.com)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
            data = json.loads(r.read())
            pages = data.get("query", {}).get("pages", {})
            for pid, info in pages.items():
                title = info.get("title", "")
                if any(title.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                    iinfo = info.get("imageinfo", [{}])[0]
                    # prefer thumburl from CDN, fallback to url
                    url = iinfo.get("thumburl") or iinfo.get("url")
                    if url:
                        return title, url
    except Exception as e:
        print(f"  [API error for '{query}']: {e}")
    return None, None

def download_with_curl(url, dest_path):
    cmd = [
        "curl.exe", "-s", "-L",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        url,
        "-o", dest_path
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 5000:
        return True
    return False

for qid, queries in REMAINING_TARGETS:
    dest = os.path.join(OUT_DIR, f"{qid}.jpg")
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        print(f"Skipping {qid}, already {os.path.getsize(dest)} bytes.")
        continue
    
    # remove bad file if exists
    if os.path.exists(dest):
        os.remove(dest)
        
    downloaded = False
    for q in queries:
        time.sleep(1.2)  # avoid rate limiting
        title, url = search_wikimedia_thumb(q)
        if url:
            time.sleep(0.8)
            if download_with_curl(url, dest):
                print(f"[{qid}] Successfully saved from '{title}' ({os.path.getsize(dest)} bytes)")
                downloaded = True
                break
            else:
                print(f"  [{qid}] Failed download from {url}")
    if not downloaded:
        print(f"[{qid}] Failed across all queries: {queries}")
