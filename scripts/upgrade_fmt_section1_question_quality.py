import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
PREFIX = "fmt-section1-"
CLINICAL_NUMBERS = {"04", "08", "10"}
RECALL_NUMBERS = {"05", "09"}


def upgraded_prompt(item):
    original = item.get("prompt", "").rstrip(" ?")
    qnum = item.get("id", "")[-2:]
    stem = original[0].upper() + original[1:] if original else original

    if qnum == "01":
        return f"{stem}:"
    if qnum == "02":
        return f"{stem}:"
    if qnum == "03":
        return f"{stem}:"
    if qnum == "06":
        return f"{stem}:"
    if qnum == "07":
        return f"{stem}:"
    return item.get("prompt", "")


def upgraded_explanation(item):
    explanation = item.get("explanation", "").strip()
    topic = item.get("topic", "this topic")
    return (
        f"{explanation} The incorrect options relate to other forensic procedures, mechanisms or legal contexts and do "
        f"not answer this specific point in {topic.lower()}."
    )


def update(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    changed = 0
    for item in data.get("questions", []):
        qid = str(item.get("id", ""))
        if not qid.startswith(PREFIX):
            continue
        qnum = qid[-2:]
        if qnum in CLINICAL_NUMBERS or qnum in RECALL_NUMBERS:
            continue
        item["prompt"] = upgraded_prompt(item)
        item["explanation"] = upgraded_explanation(item)
        item["difficulty"] = "high" if qnum in {"03", "07"} else "moderate"
        changed += 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def validate(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    qs = [q for q in data.get("questions", []) if str(q.get("id", "")).startswith(PREFIX)]
    if len(qs) != 200:
        raise ValueError(f"{path}: expected 200 FMT Section 1 questions, got {len(qs)}")
    upgraded = [
        q for q in qs
        if q.get("id", "")[-2:] not in CLINICAL_NUMBERS | RECALL_NUMBERS
    ]
    if len(upgraded) != 100:
        raise ValueError(f"{path}: expected 100 upgraded non-clinical questions, got {len(upgraded)}")
    for item in qs:
        if item["options"][item["answerIndex"]] != item["answer"]:
            raise ValueError(f"Answer mismatch: {item['id']}")


def main():
    for path in DATA_PATHS:
        changed = update(path)
        validate(path)
        print(f"Upgraded {changed} FMT Section 1 non-clinical questions in {path}.")


if __name__ == "__main__":
    main()
