import json
import re
from collections import defaultdict
from pathlib import Path

from pypdf import PdfReader


ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_JSON_PATH = ROOT_DIR / "data" / "practice-question-bank.json"
PUBLIC_OUTPUT_JSON_PATH = ROOT_DIR / "public" / "practice-question-bank.json"
OUTPUT_IMAGE_DIR = ROOT_DIR / "data" / "uploads"

EXAM_SPECS = [
    {
        "id": "neet-pg-2020",
        "title": "NEET PG 2020 PYQs",
        "year": 2020,
        "pdfPath": Path(r"f:\pyqs\Neet-PG-2020-PYQs.pdf"),
        "expectedQuestionCount": 300,
    },
    {
        "id": "neet-pg-2021",
        "title": "NEET PG 2021 PYQs",
        "year": 2021,
        "pdfPath": Path(r"f:\pyqs\NEET-PG-2021-PYQs.pdf"),
        "expectedQuestionCount": 200,
    },
    {
        "id": "neet-pg-2022",
        "title": "NEET PG 2022 PYQs",
        "year": 2022,
        "pdfPath": Path(r"f:\pyqs\NEET-PG-2022-PYQs.pdf"),
        "expectedQuestionCount": 200,
    },
]

YEAR_GROUPS = {
    "first-year": {"title": "1st Year", "subtitle": "Core foundation subjects"},
    "second-year": {"title": "2nd Year", "subtitle": "Para-clinical depth building"},
    "third-year": {"title": "3rd Year", "subtitle": "Bridge subjects and diagnostics"},
    "final-year": {"title": "Final Year", "subtitle": "Major clinical subjects"},
}

SUBJECT_MAP = {
    "Anatomy": {"id": "anatomy", "title": "Anatomy", "yearId": "first-year"},
    "Physiology": {"id": "physiology", "title": "Physiology", "yearId": "first-year"},
    "Biochemistry": {"id": "biochemistry", "title": "Biochemistry", "yearId": "first-year"},
    "Pathology": {"id": "pathology", "title": "Pathology", "yearId": "second-year"},
    "Microbiology": {"id": "microbiology", "title": "Microbiology", "yearId": "second-year"},
    "Pharmacology": {"id": "pharmacology", "title": "Pharmacology", "yearId": "second-year"},
    "PSM": {"id": "community-medicine", "title": "Community Medicine", "yearId": "third-year"},
    "Forensic Medicine": {"id": "forensic-medicine", "title": "Forensic Medicine", "yearId": "third-year"},
    "ENT": {"id": "ent", "title": "ENT", "yearId": "third-year"},
    "Ophthalmology": {"id": "ophthalmology", "title": "Ophthalmology", "yearId": "third-year"},
    "Medicine": {"id": "general-medicine", "title": "General Medicine", "yearId": "final-year"},
    "Surgery": {"id": "general-surgery", "title": "General Surgery", "yearId": "final-year"},
    "Gynaecology & Obstetrics": {"id": "obgyn", "title": "Obstetrics and Gynaecology", "yearId": "final-year"},
    "Pediatrics": {"id": "pediatrics", "title": "Pediatrics", "yearId": "final-year"},
    "Orthopaedics": {"id": "orthopedics", "title": "Orthopedics", "yearId": "final-year"},
    "Psychiatry": {"id": "psychiatry", "title": "Psychiatry", "yearId": "final-year"},
    "Dermatology": {"id": "dermatology", "title": "Dermatology", "yearId": "final-year"},
    "Anaesthesia": {"id": "anesthesia", "title": "Anesthesia", "yearId": "final-year"},
    "Radiology": {"id": "radiology", "title": "Radiology", "yearId": "third-year"},
}

QUESTION_PATTERN = re.compile(
    r"Subject:\s*(.*?)\s*"
    r"Topic:\s*(.*?)\s*"
    r"Sub-Topic:\s*(.*?)\s*"
    r"(.*?)\s*"
    r"O1:\s*(.*?)\s*"
    r"O2:\s*(.*?)\s*"
    r"O3:\s*(.*?)\s*"
    r"O4:\s*(.*?)\s*"
    r"Ans:\s*([1-4])",
    re.S,
)

IMAGE_PROMPT_PATTERN = re.compile(
    r"\b(image|shown|graph|mri|ct|x-ray|radiograph|mrcp|ultrasonography|biopsy-image|histological image|"
    r"histopathological image|depicted|test kit|arrow|capnograph|barium|instrument|film|pedigree chart)\b|"
    r"(given below|shown below|show below|following finding)",
    re.I,
)


def clean_text(value):
    normalized = re.sub(r"\s+", " ", value or "").strip()
    normalized = normalized.replace("PrepLadder", "").strip()
    normalized = normalized.replace("bugging yeasts", "budding yeasts")
    normalized = normalized.replace("Pot-translation", "Post-translation")
    normalized = normalized.replace("Ancyclostoma", "Ancylostoma")
    normalized = normalized.replace("Immunofluroscence", "Immunofluorescence")
    normalized = normalized.replace("Chemiluminiscence", "Chemiluminescence")
    normalized = normalized.replace("Cryptosopridia", "Cryptosporidia")
    normalized = normalized.replace("Parainfulenza", "Parainfluenza")
    normalized = normalized.replace("perfringes", "perfringens")
    normalized = normalized.replace("Gemeprost", "Latanoprost") if normalized == "Gemeprost" else normalized
    normalized = normalized.replace("Ill", "III")
    return normalized.strip(" :")


def parse_questions(reader, exam_spec):
    full_text = "\n".join((page.extract_text() or "") for page in reader.pages).replace("\x00", "")
    parts = re.split(r"Ques No:\s*(\d+)\s*", full_text)
    parsed = []

    for index in range(1, len(parts), 2):
        question_number = int(parts[index])
        body = parts[index + 1]
        match = QUESTION_PATTERN.search(body)
        if not match:
            raise ValueError(f"Unable to parse question {question_number} for {exam_spec['id']}.")

        raw_subject = clean_text(match.group(1))
        subject_meta = SUBJECT_MAP.get(raw_subject)
        if not subject_meta:
            raise ValueError(
                f"Unsupported subject mapping for '{raw_subject}' in question {question_number} ({exam_spec['id']})."
            )

        options = [clean_text(match.group(group_index)) for group_index in range(5, 9)]
        answer_index = int(match.group(9)) - 1

        parsed.append(
            {
                "id": f"{exam_spec['id']}-q{question_number:03d}",
                "questionNumber": question_number,
                "year": exam_spec["year"],
                "examId": exam_spec["id"],
                "examTitle": exam_spec["title"],
                "subject": raw_subject,
                "subjectId": subject_meta["id"],
                "subjectTitle": subject_meta["title"],
                "yearId": subject_meta["yearId"],
                "topic": clean_text(match.group(2)),
                "subtopic": clean_text(match.group(3)),
                "prompt": clean_text(match.group(4)),
                "options": options,
                "answerIndex": answer_index,
                "answer": options[answer_index],
                "explanation": f"Correct answer: {options[answer_index]}",
                "imageUrls": [],
            }
        )

    expected_count = exam_spec["expectedQuestionCount"]
    if len(parsed) != expected_count:
        raise ValueError(f"Expected {expected_count} questions for {exam_spec['id']}, found {len(parsed)}.")

    return parsed


def build_question_page_ranges(reader, questions):
    question_start_pages = {}

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        for match in re.findall(r"Ques No:\s*(\d+)", page_text):
            question_number = int(match)
            question_start_pages.setdefault(question_number, page_number)

    page_ranges = {}
    for question in questions:
        question_number = question["questionNumber"]
        next_question_number = question_number + 1
        start_page = question_start_pages[question_number]
        next_start_page = question_start_pages.get(next_question_number, len(reader.pages))
        end_page = start_page if next_start_page <= start_page else next_start_page
        page_ranges[question_number] = {"start": start_page, "end": end_page}

    return page_ranges


def collect_non_banner_images(reader):
    non_banner_images = defaultdict(list)

    for page_number, page in enumerate(reader.pages, start=1):
        for image_index, image in enumerate(page.images, start=1):
            size = getattr(image.image, "size", None)
            if not size:
                continue

            width, height = size
            if width >= 1800 and height <= 600:
                continue

            non_banner_images[page_number].append(
                {
                    "index": image_index,
                    "name": image.name,
                    "bytes": image.data,
                    "extension": Path(image.name).suffix or ".png",
                }
            )

    return non_banner_images


def attach_images(questions, page_ranges, non_banner_images, exam_spec):
    OUTPUT_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    assigned_pages = set()

    for question in questions:
        if not IMAGE_PROMPT_PATTERN.search(question["prompt"]):
            continue

        question_number = question["questionNumber"]
        page_range = page_ranges[question_number]
        candidate_pages = [
            page_number
            for page_number in range(page_range["start"], page_range["end"] + 1)
            if non_banner_images.get(page_number)
        ]

        selected_page = None
        for page_number in candidate_pages:
            if page_number not in assigned_pages:
                selected_page = page_number
                break

        if selected_page is None:
            continue

        image_urls = []
        for image_asset_index, image in enumerate(non_banner_images[selected_page], start=1):
            extension = image["extension"] or ".png"
            file_name = f"practice-{exam_spec['id']}-q{question_number:03d}-{image_asset_index}{extension}"
            output_path = OUTPUT_IMAGE_DIR / file_name
            output_path.write_bytes(image["bytes"])
            image_urls.append(f"/uploads/{file_name}")

        if image_urls:
            question["imageUrls"] = image_urls
            assigned_pages.add(selected_page)


def build_library(all_questions):
    ordered_questions = sorted(all_questions, key=lambda item: (-item["year"], item["questionNumber"], item["subjectTitle"]))
    subjects = []

    for subject_name, meta in SUBJECT_MAP.items():
        subject_questions = [question for question in ordered_questions if question["subject"] == subject_name]
        if not subject_questions:
            continue

        subjects.append(
            {
                "id": meta["id"],
                "title": meta["title"],
                "yearId": meta["yearId"],
                "questionCount": len(subject_questions),
                "questions": subject_questions,
            }
        )

    years = []
    for year_id, year_meta in YEAR_GROUPS.items():
        year_subjects = [subject["id"] for subject in subjects if subject["yearId"] == year_id]
        if not year_subjects:
            continue

        years.append(
            {
                "id": year_id,
                "title": year_meta["title"],
                "subtitle": year_meta["subtitle"],
                "subjectIds": year_subjects,
            }
        )

    exams = [
        {
            "id": exam_spec["id"],
            "title": exam_spec["title"],
            "year": exam_spec["year"],
            "questionCount": len([question for question in ordered_questions if question["examId"] == exam_spec["id"]]),
        }
        for exam_spec in EXAM_SPECS
    ]

    return {
        "exam": {
            "id": "neet-pg-pyqs",
            "title": "NEET PG PYQs",
            "questionCount": len(ordered_questions),
        },
        "exams": exams,
        "years": years,
        "subjects": subjects,
    }


def import_exam(exam_spec):
    if not exam_spec["pdfPath"].exists():
        raise FileNotFoundError(f"PDF not found at {exam_spec['pdfPath']}")

    reader = PdfReader(str(exam_spec["pdfPath"]))
    questions = parse_questions(reader, exam_spec)
    page_ranges = build_question_page_ranges(reader, questions)
    non_banner_images = collect_non_banner_images(reader)
    attach_images(questions, page_ranges, non_banner_images, exam_spec)
    return questions


def main():
    imported_questions = []

    for exam_spec in EXAM_SPECS:
        questions = import_exam(exam_spec)
        linked_images = sum(1 for question in questions if question["imageUrls"])
        print(
            f"Imported {len(questions)} questions for {exam_spec['title']} with images attached to {linked_images} questions."
        )
        imported_questions.extend(questions)

    library = build_library(imported_questions)
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_PATH.write_text(json.dumps(library, indent=2, ensure_ascii=True), encoding="utf-8")
    PUBLIC_OUTPUT_JSON_PATH.write_text(json.dumps(library, indent=2, ensure_ascii=True), encoding="utf-8")
    print(f"Wrote merged practice library with {library['exam']['questionCount']} questions to {OUTPUT_JSON_PATH}")
    print(f"Wrote public practice library to {PUBLIC_OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
