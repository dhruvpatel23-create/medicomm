import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
TARGET_CHAPTERS = {"Respiratory System", "Excretory System"}


def clean_stem(prompt):
    stem = prompt.strip().rstrip(":").strip()
    stem = re.sub(r"\s+", " ", stem)
    return stem


def naturalize(prompt, answer, offset):
    stem = clean_stem(prompt)
    if stem.endswith("?"):
        return stem
    lower = stem.lower()

    incomplete_endings = (
        " by",
        " in",
        " into",
        " from",
        " of",
        " to",
        " due to increased",
        " through",
        " because",
        " and",
        " toward",
        " over",
        " with",
        " mainly by",
    )

    templates = [
        'Which option correctly completes this statement: "{stem}"?',
        'In standard physiology, complete the statement: "{stem}"',
        'Select the best completion for: "{stem}"',
        'For the statement "{stem}", which option is correct?',
        'Which answer makes this statement true: "{stem}"?',
    ]

    def completion():
        return templates[offset % len(templates)].format(stem=stem)

    if lower.startswith("a patient ") or lower.startswith("an ") or lower.startswith("a "):
        if lower.endswith(incomplete_endings):
            return completion()
        if " because " in lower:
            return f"{stem}. What best explains this finding?"
        if " due to " in lower:
            return f"{stem}. Which mechanism is most likely involved?"
        if " which " in lower or " what " in lower:
            return stem + "?"
        return f"{stem}. Which option fits best?"

    direct_patterns = [
        (r"^The (.+) is the volume of air$", r"Which option describes the volume of air called the \1?"),
        (r"^(.+) means$", r"What does \1 mean?"),
        (r"^(.+) equals$", r"How is \1 calculated?"),
        (r"^(.+) consists of$", r"What structures make up \1?"),
        (r"^(.+) carries$", r"What does \1 carry?"),
        (r"^(.+) carry$", r"What do \1 carry?"),
        (r"^(.+) follows$", r"What principle does \1 follow?"),
        (r"^(.+) measures$", r"What does \1 measure?"),
        (r"^(.+) is used to assess$", r"What does \1 assess clinically?"),
        (r"^(.+) is used to estimate$", r"What does \1 estimate?"),
        (r"^(.+) is located mainly in$", r"Where is \1 located mainly?"),
        (r"^(.+) is present in$", r"Where is \1 present?"),
        (r"^(.+) is mainly$", r"What is \1 mainly?"),
        (r"^(.+) is usually$", r"Which statement is true about \1?"),
        (r"^(.+) are characteristic of$", r"What are \1 characteristic of?"),
        (r"^(.+) are important in$", r"What role do \1 have?"),
        (r"^(.+) depends importantly on$", r"What does \1 depend on?"),
        (r"^(.+) decreases$", r"What does \1 decrease?"),
    ]
    for pattern, repl in direct_patterns:
        if re.search(pattern, stem, flags=re.IGNORECASE):
            question = re.sub(pattern, repl, stem, flags=re.IGNORECASE)
            question = question[:1].upper() + question[1:]
            question = re.sub(r"\b(Pulmonary|Chronic|Gas)\b", lambda m: m.group(1).lower(), question, count=1)
            return question[0].upper() + question[1:]

    return completion()


def update_file(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    changed = 0
    targets = [
        question
        for question in data.get("questions", [])
        if question.get("subjectId") == "physiology" and question.get("chapterTitle") in TARGET_CHAPTERS
    ]

    for index, question in enumerate(targets):
        if question.get("subjectId") != "physiology":
            continue
        if question.get("chapterTitle") not in TARGET_CHAPTERS:
            continue
        old_prompt = question.get("prompt", "")
        new_prompt = naturalize(old_prompt, question.get("answer", ""), index)
        if new_prompt != old_prompt:
            question["prompt"] = new_prompt
            changed += 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main():
    for path in DATA_PATHS:
        changed = update_file(path)
        print(f"Naturalized {changed} prompts in {path}.")


if __name__ == "__main__":
    main()
