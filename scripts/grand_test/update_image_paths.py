import json
import os

target_path = r"D:\medullaprep\dhruv1\data\fmge-practice-tests.json"
p1_path = r"D:\medullaprep\dhruv1\scripts\grand_test\part1_complete.json"
p2_path = r"D:\medullaprep\dhruv1\scripts\grand_test\part2_complete.json"
uploads_dir = r"D:\medullaprep\dhruv1\public\uploads\grand_test"

valid_images = set(os.listdir(uploads_dir))

def update_questions(qs):
    count = 0
    for q in qs:
        qid = q["id"]
        img_name = f"{qid}.jpg"
        if img_name in valid_images:
            q["imageUrls"] = [f"/uploads/grand_test/{img_name}"]
            count += 1
        else:
            q["imageUrls"] = []
    return count

# Update fmge-practice-tests.json
with open(target_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for t in data["tests"]:
    if t["id"] == "fmge-grand-test-1":
        cnt = update_questions(t["questions"])
        print(f"Updated {cnt} questions in fmge-practice-tests.json")

with open(target_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Update part1_complete.json
if os.path.exists(p1_path):
    with open(p1_path, "r", encoding="utf-8") as f:
        p1 = json.load(f)
    cnt1 = update_questions(p1)
    print(f"Updated {cnt1} questions in part1_complete.json")
    with open(p1_path, "w", encoding="utf-8") as f:
        json.dump(p1, f, indent=2, ensure_ascii=False)

# Update part2_complete.json
if os.path.exists(p2_path):
    with open(p2_path, "r", encoding="utf-8") as f:
        p2 = json.load(f)
    cnt2 = update_questions(p2)
    print(f"Updated {cnt2} questions in part2_complete.json")
    with open(p2_path, "w", encoding="utf-8") as f:
        json.dump(p2, f, indent=2, ensure_ascii=False)

print("SUCCESS: All image paths updated to local /uploads/grand_test/ paths!")
