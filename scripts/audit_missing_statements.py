"""Audit reference-only choices; --apply marks candidates without deleting questions."""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANKS = ["practice-question-bank.json", "fmge-question-bank.json", "usmle-module-bank.json"]
LABEL = r"(?:[1-9]|[a-f]|i|ii|iii|iv|v|vi|vii|viii|ix|x)"
TOKEN = re.compile(rf"\b{LABEL}\b", re.I)
WORDS = re.compile(r"\b(?:and|or|only|both|all|of|the|above|are|is|correct|incorrect|statements|true|false)\b", re.I)
MARKER = re.compile(rf"(?:^|\s|[;(])({LABEL})\s*[.)\]:\-–]\s*[A-Za-z]", re.I)
AUDIT = "missing-reference-list-v1"
# Reviewed exceptions: choices directly name numbered anatomy, not list entries.
INTRINSIC_LABELS = {
    "anatomy-head-neck-vessels-lymph-development-15",
    "anatomy-thorax-bones-joints-thorax-06",
    "fmge-2025-july-part-1-q118",
}


def questions(value):
    if isinstance(value, dict):
        if "prompt" in value and "options" in value:
            yield value
        else:
            for child in value.values():
                yield from questions(child)
    elif isinstance(value, list):
        for child in value:
            yield from questions(child)


def reference_choice(value):
    if not isinstance(value, str):
        return False
    value = value.split("Answer Key")[0].strip()
    value = re.sub(r"^[a-d][.)]\s*", "", value, flags=re.I)
    if re.fullmatch(r"[+\-]?\s*\d+(?:\.\d+)?\s*D", value, re.I):
        return False
    # Measurements, decimals, ratios, fractions, ranges and tumour stages are answers.
    if re.fullmatch(r"\d+(?:[.:/\-]\d+)*\.?", value):
        if not re.fullmatch(r"[1-9](?:-[1-9]){2,}", value):
            return False
    if re.fullmatch(r"[IVX]+\s*[A-C]", value, re.I):
        return False
    if len(TOKEN.findall(value)) < 2:
        return False
    return not re.sub(r"[\s,;:&().+\-/–]+", "", TOKEN.sub("", WORDS.sub("", value)))


def classify(q):
    if q.get("id") in INTRINSIC_LABELS:
        return None
    if sum(reference_choice(o) for o in q.get("options", [])) < 2:
        return None
    stem = "\n".join(str(q.get(k) or "") for k in ("prompt", "subtopic", "leadIn"))
    # Roman numerals can name actual anatomy rather than omitted list entries.
    if re.search(r"pharyngeal arch|cranial nerve|clotting factor|coagulation factor", stem, re.I):
        if all(not re.search(r"\d", str(o)) for o in q["options"]):
            return None
    labels = set(m.group(1).lower() for m in MARKER.finditer(stem))
    if len(labels) >= 2 or stem.count("●") >= 2 or any(q.get(k) for k in ("statements", "laboratoryFindings", "table", "tables")):
        return None
    images = q.get("imageUrls") or q.get("images") or q.get("imageUrl")
    return "image-review-required" if images else "likely-missing-list"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    rows, scanned = [], 0
    for name in BANKS:
        path = ROOT / "data" / name
        if not path.exists():
            continue
        bank = json.loads(path.read_text(encoding="utf-8-sig"))
        for q in questions(bank):
            scanned += 1
            status = classify(q)
            if status:
                rows.append({
                    "bank": name, "id": q["id"],
                    "subject": q.get("subjectTitle") or q.get("subject") or q.get("subjectId", ""),
                    "exam": q.get("examTitle") or q.get("examId", ""),
                    "status": status, "prompt": q["prompt"], "options": q["options"],
                    "imageUrls": q.get("imageUrls") or q.get("images") or [],
                })
    lookup = {(r["bank"], r["id"]): r for r in rows}
    if args.apply:
        for folder in ("data", "public", "dist"):
            for name in BANKS:
                path = ROOT / folder / name
                if not path.exists():
                    continue
                bank = json.loads(path.read_text(encoding="utf-8-sig"))
                changed = False
                for q in questions(bank):
                    row = lookup.get((name, q["id"]))
                    if row:
                        note = (
                            "Content review: answer choices refer to a numbered or lettered list "
                            "that appears to be missing from this question."
                            if row["status"] == "likely-missing-list" else
                            "Content review: check the question image for the numbered or lettered "
                            "list referenced by the answer choices; it is absent from the question text."
                        )
                        q["statementAudit"] = {"audit": AUDIT, "status": row["status"], "note": note}
                        changed = True
                    elif q.get("statementAudit", {}).get("audit") == AUDIT:
                        del q["statementAudit"]
                        changed = True
                if changed:
                    path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                    print("Marked", path.relative_to(ROOT))
    out = ROOT / "output" / "missing-statements"
    out.mkdir(parents=True, exist_ok=True)
    counts = dict(Counter(r["status"] for r in rows))
    (out / "report.json").write_text(json.dumps({
        "questionsScanned": scanned, "counts": counts, "questions": rows,
        "limitations": "Heuristic review flags, not source verification. Images require visual review. "
        "Questions with existing labelled lists are excluded; partially missing lists may not be detected.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (out / "report.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["bank", "id", "subject", "exam", "status", "prompt", "options", "imageUrls"])
        writer.writeheader()
        writer.writerows(rows)
    summary = [f"# Missing statement audit\n\nScanned {scanned} questions.\n",
               f"Review flags: {counts}.\n",
               "These are suspected content gaps, not source-verified errors. No questions were deleted.\n",
               "| Subject | Likely missing list | Image review required |", "| --- | ---: | ---: |"]
    for subject in sorted(set(r["subject"] for r in rows)):
        c = Counter(r["status"] for r in rows if r["subject"] == subject)
        summary.append(f"| {subject} | {c['likely-missing-list']} | {c['image-review-required']} |")
    (out / "README.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(json.dumps({"scanned": scanned, "counts": counts}))


if __name__ == "__main__":
    main()
