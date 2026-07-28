import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
TARGET_CHAPTERS = {"Respiratory System", "Excretory System"}


def clean(prompt):
    prompt = prompt.replace(" ____", "").replace("____", "")
    if "complete the statement:" in prompt or "Select the best completion for:" in prompt:
        prompt = prompt.replace('."', '"')
    return prompt


def main():
    for path in DATA_PATHS:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        changed = 0
        for question in data.get("questions", []):
            if question.get("subjectId") != "physiology":
                continue
            if question.get("chapterTitle") not in TARGET_CHAPTERS:
                continue
            old = question.get("prompt", "")
            new = clean(old)
            if new != old:
                question["prompt"] = new
                changed += 1
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Cleaned {changed} prompts in {path}.")


if __name__ == "__main__":
    main()
