"""Merge audited import records and saved explanations; validate every attachment."""
import argparse
import json
from collections import Counter
from pathlib import Path

from explain_fmge import valid_note

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/fmge-audit"
MISSING_SOURCE_VISUALS = {
    "fmge-2019-december-q140", "fmge-2019-december-q240",
    "fmge-2020-december-q011", "fmge-2020-december-q265",
    "fmge-2022-june-q058",
    "fmge-2024-january-q005", "fmge-2024-january-q006",
    "fmge-2024-january-q009", "fmge-2024-january-q012", "fmge-2024-january-q013",
    "fmge-2024-june-q003", "fmge-2024-june-q026",
    "fmge-2025-january-part-2-q086",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-incomplete", action="store_true", help="For local integration checks only")
    args = parser.parse_args()
    bank = json.loads((OUT / "parsed-bank.json").read_text(encoding="utf-8"))
    generated = {}
    usage = Counter()
    for path in sorted((OUT / "explanations").glob("*.json"), key=lambda p: p.stat().st_mtime):
        batch = json.loads(path.read_text(encoding="utf-8"))
        usage.update({key: value for key, value in batch.get("usage", {}).items() if isinstance(value, int)})
        for q in batch.get("questions", []):
            if valid_note(q):
                generated[q["id"]] = q
    overrides_path = ROOT / "data/fmge-editorial-notes.json"
    overrides = json.loads(overrides_path.read_text(encoding="utf-8")) if overrides_path.exists() else {}
    missing, reviewed, ids, assets = [], [], set(), set()
    for session in bank["sessions"]:
        session["questionCount"] = len(session["questions"])
        for q in session["questions"]:
            if not q["explanation"] and q["id"] in generated:
                notes = generated[q["id"]]
                q.update({key: notes[key] for key in ["explanation", "educationalObjective", "reasoningChain", "optionExplanations", "reviewNote"]})
                q["explanationOrigin"] = "ai-assisted"
            q.update(overrides.get(q["id"], {}))
            if not q["explanation"]:
                missing.append(q["id"])
            source_notes = []
            if q["id"] in MISSING_SOURCE_VISUALS:
                assert not q["imageUrls"], f"Recheck visual status: {q['id']}"
                source_notes.append("The uploaded PDF refers to a visual that is absent from the source. The original question and recall key are retained.")
            counts = Counter(q["options"])
            if len(counts) < 4:
                q["originalOptions"] = q["options"][:]
                q["options"] = [f"{option} [source option {chr(65 + i)}]" if counts[option] > 1 else option for i, option in enumerate(q["options"])]
                q["answer"] = q["options"][q["answerIndex"]]
                source_notes.append("The source repeats an answer choice; original option positions are preserved.")
            if q.get("answerOrigin") == "editorial-recovery":
                source_notes.append("The source omits its answer key; this answer was recovered from the clinical findings.")
            q["sourceNote"] = " ".join(source_notes)
            if q.get("reviewNote") or source_notes:
                reviewed.append({"id": q["id"], "sourceNote": q["sourceNote"], "reviewNote": q.get("reviewNote", "")})
            assert q["id"] not in ids, f"Duplicate ID {q['id']}"
            ids.add(q["id"])
            assert len(q["options"]) == 4 and all(q["options"]) and len(set(q["options"])) == 4, q["id"]
            assert q["answer"] == q["options"][q["answerIndex"]] and q["prompt"], q["id"]
            for url in q["imageUrls"] + q["explanationImageUrls"]:
                assert (ROOT / "public" / url.lstrip("/")).is_file(), url
                assets.add(url)
    report = {
        "questionCount": len(ids), "assetCount": len(assets),
        "questionImageCount": sum(len(q["imageUrls"]) for s in bank["sessions"] for q in s["questions"]),
        "explanationImageCount": sum(len(q["explanationImageUrls"]) for s in bank["sessions"] for q in s["questions"]),
        "sessions": [{"id": s["id"], "title": s["title"], "count": s["questionCount"], "files": s["sourcePdfs"]} for s in bank["sessions"]],
        "missingExplanations": missing, "sourceAndReviewNotes": reviewed,
        "explanationOrigins": dict(Counter(q["explanationOrigin"] for s in bank["sessions"] for q in s["questions"])),
        "savedGenerationUsage": dict(usage),
        "sourceNumberGaps": {"2023 January": [102], "2025 January Part 1": [65, 133], "2025 January Part 2": [98, 99, 100, 110, 113]},
    }
    (OUT / "final-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if missing and not args.allow_incomplete:
        raise SystemExit(f"Not publishing: {len(missing)} explanations remain")
    (ROOT / "data/fmge-question-bank.json").write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: report[key] for key in ["questionCount", "assetCount", "explanationOrigins"]}))
    print(f"Missing explanations: {len(missing)}")


if __name__ == "__main__":
    main()
