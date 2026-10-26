import json
import os

p_runtime = r"D:\medullaprep\dhruv1\runtime-data\users.json"
p_tests = r"D:\medullaprep\dhruv1\data\fmge-practice-tests.json"

with open(p_tests, "r", encoding="utf-8") as f:
    tests_data = json.load(f)

gt1 = next(t for t in tests_data["tests"] if t["id"] == "fmge-grand-test-1")
gt1_img_map = {q["id"]: q.get("imageUrls", []) for q in gt1["questions"]}

with open(p_runtime, "r", encoding="utf-8") as f:
    runtime_data = json.load(f)

attempts = runtime_data.get("fmgeTestAttempts", [])
updated_count = 0
for a in attempts:
    if a.get("testId") == "fmge-grand-test-1":
        for q in a.get("questions", []):
            qid = q["id"]
            if qid in gt1_img_map:
                q["imageUrls"] = gt1_img_map[qid]
                if q["imageUrls"]:
                    updated_count += 1

with open(p_runtime, "w", encoding="utf-8") as f:
    json.dump(runtime_data, f, indent=2, ensure_ascii=False)

print(f"Successfully patched active attempt in runtime-data with {updated_count} local image URLs!")
