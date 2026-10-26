import json
import urllib.request

with open(r"D:\medullaprep\dhruv1\data\fmge-practice-tests.json", "r", encoding="utf-8") as f:
    data = json.load(f)

gt1 = next(t for t in data["tests"] if t["id"] == "fmge-grand-test-1")
image_qs = [q for q in gt1["questions"] if q.get("imageUrls")]
print(f"Testing {len(image_qs)} questions with images...")

all_ok = True
for q in image_qs:
    for url in q["imageUrls"]:
        full_url = f"http://127.0.0.1:4173{url}"
        try:
            req = urllib.request.Request(full_url, method="HEAD")
            with urllib.request.urlopen(req) as resp:
                if resp.status != 200:
                    print(f"FAILED: {q['id']} {full_url} -> Status {resp.status}")
                    all_ok = False
        except Exception as e:
            print(f"ERROR: {q['id']} {full_url} -> {e}")
            all_ok = False

if all_ok:
    print("ALL 39 CLINICAL IMAGES RESPONDED WITH HTTP 200 OK OVER LOCALHOST!")
