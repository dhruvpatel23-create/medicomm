import json
import re
import subprocess
import sys
from pathlib import Path

# Add project root to sys.path so we can import dermatology_data modules
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scripts.dermatology_data.sec01_intro import CHAPTERS as SEC01
from scripts.dermatology_data.sec02_infections import CHAPTERS as SEC02
from scripts.dermatology_data.sec03_inflammatory import CHAPTERS as SEC03
from scripts.dermatology_data.sec04_pigment_tumors import CHAPTERS as SEC04
from scripts.dermatology_data.sec05_vascular import CHAPTERS as SEC05
from scripts.dermatology_data.sec06_appendages import CHAPTERS as SEC06
from scripts.dermatology_data.sec07_systemic_photo import CHAPTERS as SEC07
from scripts.dermatology_data.sec08_hiv_sti import CHAPTERS as SEC08
from scripts.dermatology_data.sec09_therapeutics import CHAPTERS as SEC09

ALL_TOPICS = SEC01 + SEC02 + SEC03 + SEC04 + SEC05 + SEC06 + SEC07 + SEC08 + SEC09

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "dermatology"
SUBJECT_TITLE = "Dermatology"
YEAR_ID = "final-year"

# Grouping the 32 topics into 9 cohesive clinical sections
SECTION_GROUPING = {
    # 1. Introduction to Skin Disorders (Topics 1-2)
    1: (1, "Introduction to Skin Disorders"),
    2: (1, "Introduction to Skin Disorders"),

    # 2. Infections and Infestations (Topics 3-9)
    3: (2, "Infections and Infestations"),
    4: (2, "Infections and Infestations"),
    5: (2, "Infections and Infestations"),
    6: (2, "Infections and Infestations"),
    7: (2, "Infections and Infestations"),
    8: (2, "Infections and Infestations"),
    9: (2, "Infections and Infestations"),

    # 3. Inflammatory Disorders (Topics 10-17)
    10: (3, "Inflammatory Disorders"),
    11: (3, "Inflammatory Disorders"),
    12: (3, "Inflammatory Disorders"),
    13: (3, "Inflammatory Disorders"),
    14: (3, "Inflammatory Disorders"),
    15: (3, "Inflammatory Disorders"),
    16: (3, "Inflammatory Disorders"),
    17: (3, "Inflammatory Disorders"),

    # 4. Pigmentary Disorders and Tumors (Topics 18-19)
    18: (4, "Pigmentary Disorders and Tumors"),
    19: (4, "Pigmentary Disorders and Tumors"),

    # 5. Disorders of Vascular System (Topics 20-21)
    20: (5, "Disorders of Vascular System"),
    21: (5, "Disorders of Vascular System"),

    # 6. Disorders of Skin Appendages (Topics 22-25)
    22: (6, "Disorders of Skin Appendages"),
    23: (6, "Disorders of Skin Appendages"),
    24: (6, "Disorders of Skin Appendages"),
    25: (6, "Disorders of Skin Appendages"),

    # 7. Systemic Disease and Photoaggravated Disorders (Topics 26-29)
    26: (7, "Systemic Disease and Photoaggravated Disorders"),
    27: (7, "Systemic Disease and Photoaggravated Disorders"),
    28: (7, "Systemic Disease and Photoaggravated Disorders"),
    29: (7, "Systemic Disease and Photoaggravated Disorders"),

    # 8. HIV and Sexually Transmitted Infections (Topics 30-31)
    30: (8, "HIV and Sexually Transmitted Infections"),
    31: (8, "HIV and Sexually Transmitted Infections"),

    # 9. Therapeutics (Topic 32)
    32: (9, "Therapeutics"),
}


def build_questions():
    built = []
    total_clinical = 0
    total_hard_recall = 0

    for topic_order, topic_name, difficulty, q_list in ALL_TOPICS:
        sec_order, sec_title = SECTION_GROUPING[topic_order]

        for q_idx, item in enumerate(q_list, start=1):
            q_id = f"derm_ch{topic_order:02d}_q{q_idx:02d}"
            is_clinical = item.get("clinical", False)
            if is_clinical:
                total_clinical += 1
            else:
                total_hard_recall += 1

            correct_ans = item["correct"]
            distractors = item["distractors"]
            all_options = [correct_ans] + distractors

            # Validation checks
            assert len(all_options) == 4, f"{q_id} does not have exactly 4 options"
            assert len(set(all_options)) == 4, f"{q_id} has duplicate options: {all_options}"
            assert len(item["question"].strip()) > 10, f"{q_id} has empty/short question"
            assert len(item["explanation"].strip()) > 10, f"{q_id} has empty/short explanation"

            # Check that options are not paragraphs (max 25 words)
            for opt in all_options:
                word_count = len(opt.split())
                assert word_count <= 15, f"{q_id} option too long ({word_count} words): '{opt}'"

            question_obj = {
                "id": q_id,
                "subjectId": SUBJECT_ID,
                "subjectTitle": SUBJECT_TITLE,
                "chapterOrder": sec_order,
                "chapterTitle": sec_title,
                "topic": topic_name,
                "topicTitle": topic_name,
                "topicOrder": topic_order,
                "difficulty": "high" if difficulty == "hard" else "medium",
                "question": item["question"].strip(),
                "prompt": item["question"].strip(),
                "options": all_options,
                "answerIndex": 0,
                "correctAnswer": 0,  # 0-indexed; correct is first
                "answer": correct_ans,
                "explanation": item["explanation"].strip(),
                "clinical": is_clinical,
                "type": "clinical-vignette" if is_clinical else "hard-recall",
                "tags": ["clinical"] if is_clinical else ["recall"],
                "yearId": YEAR_ID,
                "source": "ai",
                "imageUrls": [],
            }
            built.append(question_obj)

    print(f"Total topics processed: {len(ALL_TOPICS)}")
    print(f"Total questions compiled: {len(built)}")
    print(f"Clinical vignettes: {total_clinical}, Hard recall: {total_hard_recall}")

    # Check for forbidden book mentions anywhere in the compiled questions
    forbidden_pattern = re.compile(r'textbook of derm|khanna|valia|neena|bolognia|fitzpatrick|roddac', re.IGNORECASE)
    forbidden_matches = 0
    for q_item in built:
        blob = json.dumps(q_item)
        if forbidden_pattern.search(blob):
            print(f"WARNING: Forbidden mention found in {q_item['id']}")
            forbidden_matches += 1
    assert forbidden_matches == 0, f"Found {forbidden_matches} forbidden book/author mentions!"
    print("Zero forbidden book or author mentions verified!")

    return built


def update_database(questions):
    for path in DATA_PATHS:
        if not path.exists():
            print(f"Warning: {path} not found")
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        existing_qs = data.get("questions", [])

        # Remove previous dermatology questions if any exist
        filtered_qs = [q for q in existing_qs if q.get("subjectId") != SUBJECT_ID]
        new_qs = filtered_qs + questions

        data["questions"] = new_qs

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Updated {path} with {len(questions)} dermatology questions (total: {len(new_qs)}).")


def main():
    questions = build_questions()
    update_database(questions)

    print("\nRunning sync_ai_questions_to_practice_bank.mjs...")
    result = subprocess.run(["node", "scripts/sync_ai_questions_to_practice_bank.mjs"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    print("Database sync complete!")


if __name__ == "__main__":
    main()
