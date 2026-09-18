"""Find content matches against existing PYQs before an additive import."""
import difflib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "output/yellowfool-remaining"


def normalized(value):
    return re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKC", value).lower()).strip()


def prompt(q):
    return normalized(" ".join(filter(None, [q.get("subtopic"), q.get("prompt")])))


def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def main():
    bank = json.loads((ROOT / "data/practice-question-bank.json").read_text(encoding="utf-8"))
    results = []
    for subject in bank["subjects"]:
        path = STAGE / f"{subject['id']}.json"
        if not path.exists():
            continue
        incoming = json.loads(path.read_text(encoding="utf-8"))
        incoming_prompts = {q["id"]: prompt(q) for q in incoming}
        for old in subject["questions"]:
            if old.get("source") in {"ai", "usmle"}:
                continue
            old_prompt = prompt(old)
            best = None
            for new in incoming:
                if new["examId"] != old.get("examId"):
                    continue
                new_prompt = incoming_prompts[new["id"]]
                tokens_a, tokens_b = set(old_prompt.split()), set(new_prompt.split())
                overlap = len(tokens_a & tokens_b) / max(1, min(len(tokens_a), len(tokens_b)))
                if overlap < .4:
                    continue
                score = similarity(old_prompt, new_prompt)
                options = similarity(" ".join(sorted(map(normalized, old.get("options", [])))), " ".join(sorted(map(normalized, new["options"]))))
                rank = score * .8 + options * .2
                if best is None or rank > best[0]:
                    best = (rank, new, score, options)
            if best and best[2] >= .45:
                _, new, score, options = best
                results.append(dict(subject=subject["id"], oldId=old["id"], newId=new["id"], promptScore=round(score, 3), optionScore=round(options, 3), oldPrompt=old_prompt, newPrompt=prompt(new), oldOptions=old["options"], newOptions=new["options"], oldAnswer=old.get("answer"), newAnswer=new["answer"]))
    (STAGE / "duplicate-candidates.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(results)} candidate matches; {sum(r['promptScore'] >= .9 and r['optionScore'] >= .9 for r in results)} strong matches")
    for r in results:
        if r["promptScore"] < .9 or r["optionScore"] < .9:
            print(json.dumps({k: v for k, v in r.items() if k not in {'oldOptions','newOptions'}}, ensure_ascii=True))


if __name__ == "__main__":
    main()
