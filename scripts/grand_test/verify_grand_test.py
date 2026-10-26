# -*- coding: utf-8 -*-
import json
import re
from collections import Counter

path = r"D:\medullaprep\dhruv1\data\fmge-practice-tests.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

tests = data["tests"]
print(f"Total tests in file: {len(tests)}")
for t in tests:
    print(f" - {t['id']} | {t['title']} | {len(t['questions'])} questions")

gt1 = next(t for t in tests if t["id"] == "fmge-grand-test-1")
qs = gt1["questions"]
assert len(qs) == 300, f"Expected 300 questions, got {len(qs)}"

# Blueprint check
blueprint_expected = {
    "anatomy": 17,
    "physiology": 17,
    "biochemistry": 17,
    "pathology": 13,
    "microbiology": 13,
    "pharmacology": 13,
    "forensic-medicine": 10,
    "community-medicine": 30,
    "ophthalmology": 15,
    "ent": 15,
    "general-medicine": 33,
    "general-surgery": 32,
    "obgyn": 30,
    "pediatrics": 15,
    "orthopedics": 5,
    "dermatology": 5,
    "psychiatry": 5,
    "anesthesia": 5,
    "radiology": 5,
    "radiotherapy": 5
}

subject_counts = Counter(q["subjectId"] for q in qs)
print("\n--- SUBJECT DISTRIBUTION AUDIT ---")
mismatches = []
for sub, expected in sorted(blueprint_expected.items()):
    actual = subject_counts.get(sub, 0)
    status = "OK" if actual == expected else "MISMATCH"
    print(f"  {sub:22s}: actual {actual:2d} / expected {expected:2d} -> {status}")
    if actual != expected:
        mismatches.append(f"{sub}: actual {actual} != expected {expected}")

assert not mismatches, f"Subject count mismatches: {mismatches}"

# Part 1 vs Part 2 check
p1_qs = qs[:150]
p2_qs = qs[150:]
print(f"\nPart 1: {len(p1_qs)} questions (IDs: {p1_qs[0]['id']} to {p1_qs[-1]['id']})")
print(f"Part 2: {len(p2_qs)} questions (IDs: {p2_qs[0]['id']} to {p2_qs[-1]['id']})")

# Image questions count
with_images = [q for q in qs if q.get("imageUrls") and len(q["imageUrls"]) > 0]
print(f"Questions with clinical visual media: {len(with_images)}")

# Check for textbook citations
textbooks = ['harrison', 'robbins', 'guyton', 'ganong', 'bailey & love', 'bailey and love', 'ghai', 'park', 'dutta', 'shaw', 'nelson', 'first aid', 'marriott']
errors = []
for idx, q in enumerate(qs):
    expected_id = f"fmge-gt1-q{idx+1:03d}"
    if q["id"] != expected_id:
        errors.append(f"ID error: {q['id']} vs {expected_id}")
    if len(q["options"]) != 4:
        errors.append(f"{q['id']}: not 4 options")
    if not (0 <= q["answerIndex"] <= 3):
        errors.append(f"{q['id']}: invalid answerIndex {q['answerIndex']}")
    for opt in q["options"]:
        if opt.endswith(";"):
            errors.append(f"{q['id']}: trailing semicolon in option: {opt}")
        if "(" in opt and not any(c.isdigit() for c in opt):
            errors.append(f"{q['id']}: explanatory bracket in option: {opt}")
        if opt.lower() in ['all of the above', 'none of the above', 'both a and b']:
            errors.append(f"{q['id']}: prohibited option: {opt}")

    full_text = (q["prompt"] + " " + q["explanation"]).lower()
    for tb in textbooks:
        if re.search(r'\b' + re.escape(tb) + r'\b', full_text):
            if tb == 'park' and any(k in full_text for k in ['parkinson', 'parkland', 'car park']):
                continue
            if tb == 'harrison' and any(k in full_text for k in ['sulcus', 'groove']):
                continue
            errors.append(f"{q['id']}: mentions textbook {tb}")

if errors:
    print(f"\nAUDIT FAILED with {len(errors)} errors:")
    for err in errors[:10]:
        print("  *", err)
    exit(1)
else:
    print("\nAUDIT PASSED 100%! All 300 questions are strictly compliant with every rule.")
