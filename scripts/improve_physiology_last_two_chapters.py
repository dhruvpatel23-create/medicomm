import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
TARGET_CHAPTERS = {"Nerve Muscle Physiology", "Blood and Immune System"}


def make_prompt(question, index):
    topic = question["topic"]
    old_prompt = question["prompt"].strip().rstrip(".?:")
    lowered = old_prompt.lower()

    if lowered.startswith("what is "):
        subject = old_prompt[8:]
        return f"Which option best defines {subject} in {topic}?"
    if lowered.startswith("which ") or lowered.startswith("why ") or lowered.startswith("how "):
        return f"{old_prompt}?"
    if lowered.startswith("normal ") or lowered.startswith("the normal "):
        return f"Which option correctly states the normal physiological value or feature: {old_prompt}?"
    if " is due to deficiency of" in lowered:
        return f"A bleeding disorder question asks the deficient factor: {old_prompt}. Which option is correct?"
    if " is derived from" in lowered or " are derived from" in lowered:
        return f"In a haematology exam, {old_prompt}. Which precursor is correct?"
    if "clinical" in question.get("tags", []):
        return f"Clinical application in {topic}: {old_prompt}. Which option best explains it?"
    if index % 2 == 0:
        return f"In {topic}, which option is the best answer for this source-book statement: {old_prompt}?"
    return f"Which option is most accurate regarding this {topic} concept: {old_prompt}?"


def make_explanation(question):
    topic = question["topic"]
    answer = question["answer"]
    old = question["explanation"].rstrip(".")
    return (
        f"{answer} is correct. {old}. In an exam stem on {topic}, this option is preferred because it links "
        "the source-book fact to the underlying physiological mechanism, while the other options describe a "
        "different cell type, protein, pathway or clinical setting."
    )


def improve_file(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    counters = {}
    changed = 0
    for question in data.get("questions", []):
        if question.get("subjectId") != "physiology" or question.get("chapterTitle") not in TARGET_CHAPTERS:
            continue
        topic = question.get("topic", "")
        counters[topic] = counters.get(topic, 0) + 1
        question["prompt"] = make_prompt(question, counters[topic])
        question["explanation"] = make_explanation(question)
        changed += 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Improved {changed} questions in {path}.")


def main():
    for path in DATA_PATHS:
        improve_file(path)


if __name__ == "__main__":
    main()
