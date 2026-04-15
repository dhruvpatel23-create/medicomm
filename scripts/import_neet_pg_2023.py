import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = Path(r"f:\pyqs\Neet-PG-2023-previous-year-question-pdf.pdf")
TARGET_FILES = [
    ROOT / "data" / "practice-question-bank.json",
    ROOT / "public" / "practice-question-bank.json",
]

EXAM_ID = "neet-pg-2023"
EXAM_TITLE = "NEET PG 2023 PYQs"
EXAM_YEAR = 2023

PDF_SUBJECT_TO_EXISTING = {
    "anatomy": "anatomy",
    "physiology": "physiology",
    "biochemistry": "biochemistry",
    "pathology": "pathology",
    "microbiology": "microbiology",
    "pharmacology": "pharmacology",
    "psm": "community-medicine",
    "forensic medicine": "forensic-medicine",
    "ent": "ent",
    "ophthalmology": "ophthalmology",
    "medicine": "general-medicine",
    "surgery": "general-surgery",
    "gynaecology & obstetrics": "obgyn",
    "pediatrics": "pediatrics",
    "orthopaedics": "orthopedics",
    "psychiatry": "psychiatry",
    "dermatology": "dermatology",
    "anaesthesia": "anesthesia",
    "radiology": "radiology",
}

QUESTION_BLOCK_PATTERN = re.compile(
    r"""Ques\s+No:\s*(?P<num>\d+)\s*
\s*Subject:\s*(?P<subject>.+?)\s*
\s*Topic:\s*(?P<topic>.+?)\s*
\s*Sub-Topic:\s*(?P<subtopic>.*?)\s*
(?P<prompt>.*?)\s*O1:\s*(?P<o1>.*?)\s*O2:\s*(?P<o2>.*?)\s*O3:\s*(?P<o3>.*?)\s*O4:\s*(?P<o4>.*?)\s*Ans:\s*(?P<ans>[1-4])\b""",
    re.S,
)


def normalize_space(value: str) -> str:
    return " ".join(str(value or "").replace("\u00a0", " ").split()).strip()


def normalize_key(value: str) -> str:
    return normalize_space(value).lower()


def load_pdf_text() -> str:
    reader = PdfReader(str(PDF_PATH))
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    text = text.replace("\r", "")
    return re.sub(r"(?m)^\s*PrepLadder\s*$", "", text)


def parse_questions(text: str, subject_meta_by_id: dict) -> list[dict]:
    blocks = [block.strip() for block in re.split(r"(?=Ques No:\s*\d+)", text) if block.strip().startswith("Ques No:")]
    questions = []

    for block in blocks:
        match = QUESTION_BLOCK_PATTERN.search(block)
        if not match:
            number_match = re.search(r"Ques No:\s*(\d+)", block)
            question_number = number_match.group(1) if number_match else "unknown"
            raise ValueError(f"Could not parse question block {question_number}.")

        question_number = int(match.group("num"))
        pdf_subject = normalize_key(match.group("subject"))
        subject_id = PDF_SUBJECT_TO_EXISTING.get(pdf_subject)

        if not subject_id or subject_id not in subject_meta_by_id:
            raise ValueError(f"Unsupported subject '{match.group('subject')}' for question {question_number}.")

        subject_meta = subject_meta_by_id[subject_id]
        options = [normalize_space(match.group(f"o{idx}")) for idx in range(1, 5)]
        answer_index = int(match.group("ans")) - 1
        answer = options[answer_index]

        questions.append(
            {
                "id": f"{EXAM_ID}-q{question_number:03d}",
                "questionNumber": question_number,
                "year": EXAM_YEAR,
                "examId": EXAM_ID,
                "examTitle": EXAM_TITLE,
                "subject": subject_meta["subject"],
                "subjectId": subject_meta["subjectId"],
                "subjectTitle": subject_meta["subjectTitle"],
                "yearId": subject_meta["yearId"],
                "topic": normalize_space(match.group("topic")),
                "subtopic": normalize_space(match.group("subtopic")),
                "prompt": normalize_space(match.group("prompt")),
                "options": options,
                "answerIndex": answer_index,
                "answer": answer,
                "explanation": f"Correct answer: {answer}",
                "imageUrls": [],
            }
        )

    if len(questions) != 200:
        raise ValueError(f"Expected 200 questions, found {len(questions)}.")

    return questions


def build_subject_meta(subjects: list[dict]) -> dict:
    return {
        subject["id"]: {
            "subject": subject["title"],
            "subjectId": subject["id"],
            "subjectTitle": subject["title"],
            "yearId": subject["yearId"],
        }
        for subject in subjects
    }


def upsert_exam(data: dict) -> None:
    exams = data.setdefault("exams", [])
    exams = [exam for exam in exams if exam.get("id") != EXAM_ID]
    exams.insert(
        0,
        {
            "id": EXAM_ID,
            "title": EXAM_TITLE,
            "year": EXAM_YEAR,
            "questionCount": 200,
        },
    )
    data["exams"] = exams


def merge_questions(data: dict, questions: list[dict]) -> None:
    by_subject_id: dict[str, list[dict]] = {}
    for question in questions:
        by_subject_id.setdefault(question["subjectId"], []).append(question)

    for subject in data["subjects"]:
        subject_questions = subject.get("questions", [])
        subject_questions = [question for question in subject_questions if question.get("examId") != EXAM_ID]
        subject_questions.extend(by_subject_id.get(subject["id"], []))
        subject_questions.sort(key=lambda item: (-int(item["year"]), int(item["questionNumber"])))
        subject["questions"] = subject_questions


def main() -> None:
    source_data = json.loads(TARGET_FILES[0].read_text(encoding="utf-8"))
    subject_meta_by_id = build_subject_meta(source_data["subjects"])
    questions = parse_questions(load_pdf_text(), subject_meta_by_id)

    for target_file in TARGET_FILES:
        data = json.loads(target_file.read_text(encoding="utf-8"))
        upsert_exam(data)
        merge_questions(data, questions)
        target_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Updated {target_file} with {len(questions)} NEET PG 2023 questions.")


if __name__ == "__main__":
    main()
