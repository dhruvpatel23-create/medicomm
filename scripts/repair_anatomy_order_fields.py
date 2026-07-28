import json
import runpy
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SCRIPT_PATHS = [
    Path("scripts/add_anatomy_general_anatomy_questions.py"),
    Path("scripts/add_anatomy_upper_limb_questions.py"),
    Path("scripts/add_anatomy_lower_limb_questions.py"),
    Path("scripts/add_anatomy_thorax_questions.py"),
    Path("scripts/add_anatomy_abdomen_questions.py"),
    Path("scripts/add_anatomy_head_neck_brain_questions.py"),
]
CHAPTER_ORDER = {
    "General Anatomy": 1,
    "Upper Limb": 2,
    "Lower Limb": 3,
    "Thorax": 4,
    "Abdomen": 5,
    "Head and Neck": 6,
    "Brain": 7,
}


def topic_orders():
    orders = {}
    for script_path in SCRIPT_PATHS:
        namespace = runpy.run_path(str(script_path))
        if "CHAPTERS" in namespace:
            for chapter, topics in namespace["CHAPTERS"].items():
                for index, (_, topic, _) in enumerate(topics, 1):
                    orders[(chapter, topic)] = index
        else:
            chapter = namespace["CHAPTER"]
            for index, (_, topic, _) in enumerate(namespace["TOPICS"], 1):
                orders[(chapter, topic)] = index
    return orders


def main():
    runtime = json.loads(DATA_PATHS[0].read_text(encoding="utf-8-sig"))
    anatomy = [q for q in runtime.get("questions", []) if q.get("subjectId") == "anatomy"]
    orders = topic_orders()

    for path in DATA_PATHS:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if path != DATA_PATHS[0]:
            data["questions"] = [q for q in data.get("questions", []) if q.get("subjectId") != "anatomy"] + anatomy
        changed = 0
        for question in data.get("questions", []):
            if question.get("subjectId") != "anatomy":
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
        data["questions"].sort(key=lambda q: q.get("id", ""))
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Repaired/synced anatomy in {path}; changed {changed} order fields.")


if __name__ == "__main__":
    main()
