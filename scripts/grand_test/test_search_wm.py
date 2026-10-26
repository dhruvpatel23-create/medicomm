import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def find_image(query):
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrnamespace=6&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(api_url, headers={"User-Agent": "MedullaPrep/1.0 (contact@medullaprep.com)"})
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            data = json.loads(r.read())
            pages = data.get("query", {}).get("pages", {})
            for pid, info in pages.items():
                title = info.get("title", "")
                if any(title.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                    url = info["imageinfo"][0]["url"]
                    return title, url
    except Exception as e:
        print("Error:", e)
    return None, None

tests = [
    "Reed Sternberg cell",
    "Koplik spots",
    "Auspitz sign psoriasis",
    "Bamboo spine x-ray",
    "Achalasia barium swallow"
]

for t in tests:
    title, url = find_image(t)
    print(f"{t} -> {title} -> {url}")
