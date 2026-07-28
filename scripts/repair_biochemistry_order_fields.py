import json
import runpy
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SCRIPT_PATHS = [
    Path("scripts/add_biochemistry_chemical_basis_questions.py"),
    Path("scripts/add_biochemistry_general_metabolism_questions.py"),
    Path("scripts/add_biochemistry_clinical_applied_questions.py"),
    Path("scripts/add_biochemistry_nutrition_questions.py"),
    Path("scripts/add_biochemistry_molecular_biology_questions.py"),
]
CHAPTER_ORDER = {
    "Chemical Basis of Life": 1,
    "General Metabolism": 2,
    "Clinical and Applied Biochemistry": 3,
    "Nutrition": 4,
    "Molecular Biology": 5,
}


def topic_orders():
    orders = {}
    for script_path in SCRIPT_PATHS:
        namespace = runpy.run_path(str(script_path))
        chapter = namespace["CHAPTER"]
        for index, (_, topic, _) in enumerate(namespace["TOPICS"], 1):
            orders[(chapter, topic)] = index
    return orders


def main():
    orders = topic_orders()
    for path in DATA_PATHS:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        changed = 0
        for question in data.get("questions", []):
            if question.get("subjectId") != "biochemistry":
                continue
            chapter = question.get("chapterTitle")
            topic = question.get("topic")
            new_chapter_order = CHAPTER_ORDER[chapter]
            new_topic_order = orders[(chapter, topic)]
            if question.get("chapterOrder") != new_chapter_order:
                question["chapterOrder"] = new_chapter_order
                changed += 1
            if question.get("topicOrder") != new_topic_order:
                question["topicOrder"] = new_topic_order
                changed += 1
            question["topicTitle"] = topic
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Repaired {changed} order fields in {path}.")


if __name__ == "__main__":
    main()
