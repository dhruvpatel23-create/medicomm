# -*- coding: utf-8 -*-
import json
import os
import shutil
import re

p1_path = r"D:\medullaprep\dhruv1\scripts\grand_test\part1_complete.json"
p2_path = r"D:\medullaprep\dhruv1\scripts\grand_test\part2_complete.json"
target_path = r"D:\medullaprep\dhruv1\data\fmge-practice-tests.json"
backup_path = r"D:\medullaprep\dhruv1\data\fmge-practice-tests.backup.json"

with open(p1_path, "r", encoding="utf-8") as f:
    p1 = json.load(f)

with open(p2_path, "r", encoding="utf-8") as f:
    p2 = json.load(f)

print(f"Loaded Part 1: {len(p1)} questions")
print(f"Loaded Part 2: {len(p2)} questions")
assert len(p1) == 150, f"Part 1 length is {len(p1)}, expected 150"
assert len(p2) == 150, f"Part 2 length is {len(p2)}, expected 150"

all_questions = p1 + p2
assert len(all_questions) == 300, f"Total length is {len(all_questions)}, expected 300"

# Enrich with source fields if not present
for idx, q in enumerate(all_questions):
    expected_id = f"fmge-gt1-q{idx+1:03d}"
    assert q["id"] == expected_id, f"ID mismatch at {idx}: expected {expected_id}, got {q['id']}"
    assert len(q["options"]) == 4, f"{q['id']} does not have 4 options"
    assert 0 <= q["answerIndex"] <= 3, f"{q['id']} invalid answerIndex"
    
    q["source"] = "fmge"
    q["sourceBank"] = "fmge"
    q["sourceExam"] = "FMGE Grand Test 1"
    q["sourcePdf"] = "FMGE-2026-Grand-Test-1.pdf"
    q["sourcePage"] = idx + 1
    if "imageUrls" not in q:
        q["imageUrls"] = []

# Backup existing file
if os.path.exists(target_path) and not os.path.exists(backup_path):
    shutil.copyfile(target_path, backup_path)
    print(f"Created backup at: {backup_path}")

with open(target_path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_test = {
    "id": "fmge-grand-test-1",
    "title": "FMGE Grand Test 1",
    "questions": all_questions
}

# Check if test already exists in tests list
existing_idx = None
for i, t in enumerate(data.get("tests", [])):
    if t.get("id") == "fmge-grand-test-1":
        existing_idx = i
        break

if existing_idx is not None:
    data["tests"][existing_idx] = new_test
    print(f"Updated existing 'fmge-grand-test-1' at index {existing_idx}")
else:
    data["tests"].append(new_test)
    print(f"Appended 'fmge-grand-test-1' as test #{len(data['tests'])}")

# Write to target
with open(target_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {target_path} ({os.path.getsize(target_path)} bytes)")
