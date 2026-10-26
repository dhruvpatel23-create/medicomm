import json

with open(r"D:\medullaprep\dhruv1\data\fmge-practice-tests.json", "r", encoding="utf-8") as f:
    data = json.load(f)

gt1 = next(t for t in data["tests"] if t["id"] == "fmge-grand-test-1")
for q in gt1["questions"]:
    if q.get("imageUrls"):
        print(f"{q['id']} | {q['subjectId']} | {q['topic']} | {q['options'][q['answerIndex']]}")
