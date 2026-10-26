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

SPECIFIC = [
    ("fmge-gt1-q134", "Herpes keratitis"),
    ("fmge-gt1-q174", "Multiple sclerosis periventricular MRI"),
    ("fmge-gt1-q199", "Psoriasis vulgaris"),
    ("fmge-gt1-q221", "Achalasia x-ray"),
    ("fmge-gt1-q296", "Schwannoma MRI")
]

for qid, q in SPECIFIC:
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(q)}&gsrnamespace=6&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json"
    req = urllib.request.Request(api_url, headers={"User-Agent": "MedullaPrepBot/2.0 (medullaprep.learning@gmail.com)"})
    with urllib.request.urlopen(req, context=ctx) as r:
        data = json.loads(r.read())
        pages = data.get("query", {}).get("pages", {})
        for pid, info in pages.items():
            title = info.get("title", "")
            if any(title.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                iinfo = info.get("imageinfo", [{}])[0]
                url = iinfo.get("thumburl") or iinfo.get("url")
                print(f"{qid} -> {title} -> {url}")
                dest = os.path.join(OUT_DIR, f"{qid}.jpg")
                cmd = [
                    "curl.exe", "-s", "-L",
                    "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    url,
                    "-o", dest
                ]
                subprocess.run(cmd)
                if os.path.exists(dest) and os.path.getsize(dest) > 10000:
                    print(f"  Saved {dest} ({os.path.getsize(dest)} bytes)")
                    break
