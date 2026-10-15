import json
import re
import subprocess
import sys
from pathlib import Path

# Add project root to sys.path so we can import orthopedics_data modules
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.orthopedics_data.ch01_to_ch08 import CHAPTERS as CH01_08
from scripts.orthopedics_data.ch09_to_ch16 import CHAPTERS as CH09_16
from scripts.orthopedics_data.ch17_to_ch24 import CHAPTERS as CH17_24
from scripts.orthopedics_data.ch25_to_ch32 import CHAPTERS as CH25_32
from scripts.orthopedics_data.ch33_to_ch42 import CHAPTERS as CH33_42

ALL_CHAPTERS = CH01_08 + CH09_16 + CH17_24 + CH25_32 + CH33_42

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "orthopedics"
SUBJECT_TITLE = "Orthopedics"
SOURCE_PDF = "Essential Orthopaedics"
YEAR_ID = "final-year"

# Grouping the 42 book topics into 10 cohesive clinical chapters
CHAPTER_GROUPING = {
    # 1. General Orthopaedics & Fracture Principles
    1: (1, "General Orthopaedics & Fracture Principles"),
    2: (1, "General Orthopaedics & Fracture Principles"),
    3: (1, "General Orthopaedics & Fracture Principles"),
    4: (1, "General Orthopaedics & Fracture Principles"),
    5: (1, "General Orthopaedics & Fracture Principles"),
    6: (1, "General Orthopaedics & Fracture Principles"),
    7: (1, "General Orthopaedics & Fracture Principles"),
    8: (1, "General Orthopaedics & Fracture Principles"),

    # 2. Upper Limb Injuries & Fractures
    13: (2, "Upper Limb Injuries & Fractures"),
    14: (2, "Upper Limb Injuries & Fractures"),
    15: (2, "Upper Limb Injuries & Fractures"),
    16: (2, "Upper Limb Injuries & Fractures"),

    # 3. Lower Limb Injuries & Fractures
    17: (3, "Lower Limb Injuries & Fractures"),
    18: (3, "Lower Limb Injuries & Fractures"),
    19: (3, "Lower Limb Injuries & Fractures"),
    20: (3, "Lower Limb Injuries & Fractures"),
    21: (3, "Lower Limb Injuries & Fractures"),

    # 4. Pediatric & Congenital Orthopaedics
    9: (4, "Pediatric & Congenital Orthopaedics"),
    25: (4, "Pediatric & Congenital Orthopaedics"),
    26: (4, "Pediatric & Congenital Orthopaedics"),
    39: (4, "Pediatric & Congenital Orthopaedics"),

    # 5. Spine & Spinal Cord Disorders
    29: (5, "Spine & Spinal Cord Disorders"),
    30: (5, "Spine & Spinal Cord Disorders"),
    31: (5, "Spine & Spinal Cord Disorders"),
    32: (5, "Spine & Spinal Cord Disorders"),
    33: (5, "Spine & Spinal Cord Disorders"),

    # 6. Orthopaedic Infections
    22: (6, "Orthopaedic Infections"),
    23: (6, "Orthopaedic Infections"),
    24: (6, "Orthopaedic Infections"),

    # 7. Bone Tumours & Tumour-like Conditions
    28: (7, "Bone Tumours & Tumour-like Conditions"),

    # 8. Arthritis, Degenerative & Soft Tissue Disorders
    34: (8, "Arthritis, Degenerative & Soft Tissue Disorders"),
    35: (8, "Arthritis, Degenerative & Soft Tissue Disorders"),
    36: (8, "Arthritis, Degenerative & Soft Tissue Disorders"),

    # 9. Neuromuscular, Metabolic & Miscellaneous Bone Diseases
    10: (9, "Neuromuscular, Metabolic & Miscellaneous Bone Diseases"),
    11: (9, "Neuromuscular, Metabolic & Miscellaneous Bone Diseases"),
    27: (9, "Neuromuscular, Metabolic & Miscellaneous Bone Diseases"),
    37: (9, "Neuromuscular, Metabolic & Miscellaneous Bone Diseases"),
    38: (9, "Neuromuscular, Metabolic & Miscellaneous Bone Diseases"),

    # 10. Operative Orthopaedics, Arthroplasty & Rehabilitation
    12: (10, "Operative Orthopaedics, Arthroplasty & Rehabilitation"),
    40: (10, "Operative Orthopaedics, Arthroplasty & Rehabilitation"),
    41: (10, "Operative Orthopaedics, Arthroplasty & Rehabilitation"),
    42: (10, "Operative Orthopaedics, Arthroplasty & Rehabilitation"),
}


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def build_questions():
    if len(ALL_CHAPTERS) != 42:
        raise ValueError(f"Expected 42 original topics, got {len(ALL_CHAPTERS)}")

    questions = []
    chapter_counts = {}

    for ch_num, topic_title, ch_tier, rows in ALL_CHAPTERS:
        parent_order, parent_title = CHAPTER_GROUPING[ch_num]
        chapter_counts[parent_title] = chapter_counts.get(parent_title, 0) + len(rows)

        slug = slugify(topic_title)
        expected_len = 10 if ch_tier == "hard" else 5
        if len(rows) != expected_len:
            raise ValueError(f"Topic {ch_num}: {topic_title} ({ch_tier}) expected {expected_len} questions, got {len(rows)}")

        for q_idx, row in enumerate(rows, 1):
            q_id = f"ortho-ch{parent_order:02d}-t{ch_num:02d}-{slug[:25]}-{q_idx:02d}"
            item = {
                "id": q_id,
                "subjectId": SUBJECT_ID,
                "subjectTitle": SUBJECT_TITLE,
                "chapterTitle": parent_title,
                "chapterOrder": parent_order,
                "topic": topic_title,
                "topicTitle": topic_title,
                "topicOrder": ch_num,
                "yearId": YEAR_ID,
                "source": "ai",
                "sourcePdf": SOURCE_PDF,
                "imageUrls": [],
                **row,
            }
            questions.append(item)

    print(f"Grouped 42 topics into {len(chapter_counts)} Chapters:")
    for ch_order in sorted(set(v[0] for v in CHAPTER_GROUPING.values())):
        ch_name = next(v[1] for v in CHAPTER_GROUPING.values() if v[0] == ch_order)
        print(f"  Chapter {ch_order}: {ch_name} -> {chapter_counts[ch_name]} questions")

    print(f"\nTotal questions compiled: {len(questions)}")
    return questions


def validate_questions(questions):
    if len(questions) != 325:
        raise AssertionError(f"Expected exactly 325 questions, got {len(questions)}")

    ids = set()
    chapters = set()
    topics = set()
    for q in questions:
        if q["id"] in ids:
            raise AssertionError(f"Duplicate ID found: {q['id']}")
        ids.add(q["id"])
        chapters.add(q["chapterTitle"])
        topics.add(q["topic"])

        if len(q["options"]) != 4:
            raise AssertionError(f"Question {q['id']} does not have 4 options")
        if len(set(q["options"])) != 4:
            raise AssertionError(f"Question {q['id']} has duplicate options")
        if q["answer"] != q["options"][q["answerIndex"]]:
            raise AssertionError(f"Question {q['id']} answer mismatch: {q['answer']} vs {q['options'][q['answerIndex']]}")
        if not q["explanation"] or len(q["explanation"]) < 15:
            raise AssertionError(f"Question {q['id']} has inadequate explanation")
        if not any(tag in q["tags"] for tag in ["clinical", "hard-recall"]):
            raise AssertionError(f"Question {q['id']} missing clinical or hard-recall tag")

    if len(chapters) != 10:
        raise AssertionError(f"Expected exactly 10 chapters, got {len(chapters)}")
    if len(topics) != 42:
        raise AssertionError(f"Expected exactly 42 topics, got {len(topics)}")

    clinical_qs = sum(1 for q in questions if "clinical" in q["tags"])
    hard_recall_qs = sum(1 for q in questions if "hard-recall" in q["tags"])
    print(f"Validation passed: 325/325 valid questions across 10 Chapters and 42 Topics ({clinical_qs} Clinical Vignettes, {hard_recall_qs} Hard Recall).")


def update_database(path, questions):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    existing_qs = [
        item for item in data.get("questions", [])
        if not (item.get("subjectId") == SUBJECT_ID and item.get("source") == "ai")
    ]
    data["questions"] = existing_qs + questions
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {path} with {len(questions)} orthopedics questions (total questions in file: {len(data['questions'])}).")


def main():
    questions = build_questions()
    validate_questions(questions)

    for p in DATA_PATHS:
        update_database(p, questions)

    # Sync to practice-question-bank
    print("\nRunning sync_ai_questions_to_practice_bank.mjs...")
    subprocess.run(["node", "scripts/sync_ai_questions_to_practice_bank.mjs"], check=True)
    print("Database sync complete!")


if __name__ == "__main__":
    main()
