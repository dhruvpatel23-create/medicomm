import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF_PATH = Path(r"F:\pyqs\Pyqs neet inict the yellowfool.pdf")
CHAPTER_COUNTS_PATH = ROOT / "pdf_question_stats" / "chapter_counts.csv"
OUTPUT_IMAGE_DIRS = [
    ROOT / "runtime-data" / "uploads",
    ROOT / "data" / "uploads",
    ROOT / "public" / "uploads",
]
TARGET_FILES = [
    ROOT / "data" / "practice-question-bank.json",
    ROOT / "public" / "practice-question-bank.json",
]

PDF_SOURCE_NAME = "Pyqs neet inict the yellowfool.pdf"

SUBJECT_META = {
    "Anatomy": {"id": "anatomy", "title": "Anatomy", "yearId": "first-year"},
    "Physiology": {"id": "physiology", "title": "Physiology", "yearId": "first-year"},
    "Biochemistry": {"id": "biochemistry", "title": "Biochemistry", "yearId": "first-year"},
    "Pathology": {"id": "pathology", "title": "Pathology", "yearId": "second-year"},
    "Microbiology": {"id": "microbiology", "title": "Microbiology", "yearId": "second-year"},
    "Pharmacology": {"id": "pharmacology", "title": "Pharmacology", "yearId": "second-year"},
    "Community Medicine": {"id": "community-medicine", "title": "Community Medicine", "yearId": "third-year"},
    "Forensic Medicine": {"id": "forensic-medicine", "title": "Forensic Medicine", "yearId": "third-year"},
    "ENT": {"id": "ent", "title": "ENT", "yearId": "third-year"},
    "Ophthalmology": {"id": "ophthalmology", "title": "Ophthalmology", "yearId": "third-year"},
    "Medicine": {"id": "general-medicine", "title": "General Medicine", "yearId": "final-year"},
    "Surgery": {"id": "general-surgery", "title": "General Surgery", "yearId": "final-year"},
    "Obstetrics & Gynecology": {"id": "obgyn", "title": "Obstetrics and Gynaecology", "yearId": "final-year"},
    "Pediatrics": {"id": "pediatrics", "title": "Pediatrics", "yearId": "final-year"},
    "Orthopedics": {"id": "orthopedics", "title": "Orthopedics", "yearId": "final-year"},
    "Psychiatry": {"id": "psychiatry", "title": "Psychiatry", "yearId": "final-year"},
    "Dermatology": {"id": "dermatology", "title": "Dermatology", "yearId": "final-year"},
    "Anesthesia": {"id": "anesthesia", "title": "Anesthesia", "yearId": "final-year"},
}

SUBJECT_ALIASES = {
    "Obstetrics and Gynecology": "Obstetrics & Gynecology",
    "Paediatrics": "Pediatrics",
}

EXAM_IDS = {
    "NEET PG": "neet-pg",
    "AIIMS": "aiims",
    "INI-CET": "ini-cet",
}

QUESTION_HEADING = re.compile(r"(?m)^Question\s+(\d+):\s*$")
SOLUTION_HEADING = re.compile(r"(?m)^Solution to Question\s+(\d+):\s*$")
OPTION_HEADING = re.compile(r"(?m)^([a-d])\)\s*")
ANSWER_KEY_LINE = re.compile(r"(?m)^\s*(\d{1,3})\s+([a-d])\s*$")
PAGE_NUMBER_LINE = re.compile(r"(?m)^\s*\d{1,5}\s*$")
IMAGE_PROMPT_PATTERN = re.compile(
    r"\b(image|shown|marked|identify|depict|visual|histology|photograph|specimen|x-ray|radiograph|ct|mri|spotter)\b",
    re.IGNORECASE,
)
OPTION_LABEL_PATTERN = re.compile(r"^[A-D1-9]$", re.IGNORECASE)


def normalize_space(value: str) -> str:
    value = str(value or "").replace("\u00a0", " ").replace("\x00", "")
    value = value.replace("&lt;", "<").replace("&gt;", ">").replace("", "-")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def decode_private_font(value: str) -> str:
    decoded = []
    for char in value:
        codepoint = ord(char)
        if 0xE000 <= codepoint <= 0xE0FF:
            low = codepoint & 0xFF
            decoded.append(chr(low + 0x20 if low < 0x40 else low))
        else:
            decoded.append(char)
    return "".join(decoded)


def clean_page_text(raw_text: str) -> str:
    decoded = decode_private_font(raw_text)
    lines = []
    for line in decoded.replace("\r", "").splitlines():
        stripped = line.strip()
        if not stripped or stripped == "@the.yellowfool":
            continue
        lines.append(stripped)
    return "\n".join(lines)


def subject_key(value: str) -> str:
    return SUBJECT_ALIASES.get(value, value)


def slugify(value: str) -> str:
    value = normalize_space(value).lower()
    value = value.replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def exam_id(exam: str, year: int) -> str:
    return f"{EXAM_IDS[exam]}-{year}"


def exam_title(exam: str, year: int) -> str:
    return f"{exam} {year} PYQs"


def load_chapters(subject_ids: set[str] | None) -> list[dict]:
    chapters = []
    with CHAPTER_COUNTS_PATH.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if not row.get("start_pdf_page"):
                continue
            subject = subject_key(row["subject"])
            meta = SUBJECT_META.get(subject)
            if not meta:
                continue
            if subject_ids and meta["id"] not in subject_ids:
                continue
            year = int(row["year"])
            questions = int(row["questions"])
            chapters.append(
                {
                    "chapterNo": int(row["chapter_no"]),
                    "title": row["title"],
                    "subject": subject,
                    "exam": row["exam"],
                    "examGroup": row["exam_group"],
                    "year": year,
                    "expectedQuestions": questions,
                    "startPage": int(row["start_pdf_page"]),
                    "endPage": int(row["end_pdf_page"]),
                    "printedPage": int(row["printed_page"]),
                    "subjectMeta": meta,
                }
            )
    return sorted(chapters, key=lambda chapter: chapter["chapterNo"])


def split_numbered_blocks(pattern: re.Pattern, text: str) -> dict[int, str]:
    matches = list(pattern.finditer(text))
    blocks = {}
    for index, match in enumerate(matches):
      number = int(match.group(1))
      start = match.end()
      end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
      blocks[number] = text[start:end].strip()
    return blocks


def parse_answer_key(question_text: str) -> dict[int, str]:
    return {int(number): letter for number, letter in ANSWER_KEY_LINE.findall(question_text)}


def strip_answer_key_lines(text: str) -> str:
    text = ANSWER_KEY_LINE.sub("", text)
    return PAGE_NUMBER_LINE.sub("", text).strip()


def parse_question_block(block: str) -> tuple[str, list[str]]:
    block = strip_answer_key_lines(block)
    option_matches = list(OPTION_HEADING.finditer(block))
    if len(option_matches) < 4:
        raise ValueError("Could not find four options.")

    prompt = block[: option_matches[0].start()].strip()
    options = []
    for index, match in enumerate(option_matches[:4]):
        start = match.end()
        end = option_matches[index + 1].start() if index < 3 else len(block)
        option = normalize_space(block[start:end])
        options.append(option)

    return normalize_space(prompt), options


def get_page_images(reader: PdfReader, page_number: int) -> list[dict]:
    page = reader.pages[page_number - 1]
    images = []
    for image_index, image in enumerate(page.images, start=1):
        size = getattr(image.image, "size", None)
        if not size:
            continue

        width, height = size
        if width >= 1800 and height <= 600:
            continue

        extension = Path(image.name).suffix.lower() or ".png"
        if extension == ".jpe":
            extension = ".jpg"

        images.append(
            {
                "index": image_index,
                "name": Path(image.name).stem,
                "bytes": image.data,
                "extension": extension,
            }
        )
    return images


def has_compact_visual_options(question: dict) -> bool:
    options = [normalize_space(option) for option in question.get("options", [])]
    return len(options) == 4 and all(OPTION_LABEL_PATTERN.match(option) or "■" in option for option in options)


def is_visual_question(question: dict) -> bool:
    searchable_text = " ".join([question.get("prompt", ""), *question.get("options", [])])
    return bool(IMAGE_PROMPT_PATTERN.search(searchable_text) or has_compact_visual_options(question))


def chapter_question_images(reader: PdfReader, chapter: dict, page_texts: list[str]) -> list[dict]:
    images = []

    for page_number in range(chapter["startPage"], chapter["endPage"] + 1):
        text = normalize_space(page_texts[page_number - 1])
        if SOLUTION_HEADING.search(text) or re.search(r"(?m)^Detailed Explanations\s*$", text):
            break

        for image in get_page_images(reader, page_number):
            images.append({**image, "pageNumber": page_number})

    return images


def page_layout_items(reader: PdfReader, page_number: int) -> list[dict]:
    page = reader.pages[page_number - 1]
    images_by_name = defaultdict(list)
    for image in get_page_images(reader, page_number):
        images_by_name[image["name"]].append(image)

    items = []

    def add_item(item: dict) -> None:
        items.append({**item, "order": len(items)})

    def visitor_text(text, _cm, tm, _font_dict, _font_size):
        match = re.search(r"Question\s+(\d+):", text.strip())
        if match:
            add_item(
                {
                    "type": "question",
                    "questionNumber": int(match.group(1)),
                    "pageNumber": page_number,
                    "y": float(tm[5]),
                }
            )

    def visitor_operand_before(operator, args, cm, _tm):
        if operator != b"Do" or not args:
            return

        image_name = str(args[0]).lstrip("/")
        image_bucket = images_by_name.get(image_name)
        if not image_bucket:
            return

        image = image_bucket.pop(0)
        add_item(
            {
                **image,
                "type": "image",
                "pageNumber": page_number,
                "y": float(cm[5]),
            }
        )

    page.extract_text(visitor_text=visitor_text, visitor_operand_before=visitor_operand_before)
    return items


def chapter_layout(reader: PdfReader, chapter: dict, page_texts: list[str]) -> tuple[dict[int, dict], list[dict]]:
    question_positions = {}
    images = []

    for page_number in range(chapter["startPage"], chapter["endPage"] + 1):
        text = normalize_space(page_texts[page_number - 1])
        if SOLUTION_HEADING.search(text) or re.search(r"(?m)^Detailed Explanations\s*$", text):
            break

        for item in page_layout_items(reader, page_number):
            if item["type"] == "question":
                question_positions.setdefault(item["questionNumber"], item)
            elif item["type"] == "image":
                images.append(item)

    images.sort(key=lambda item: (item["pageNumber"], -item["y"], item["index"]))
    return question_positions, images


def image_is_after_question_before_next(image: dict, current_position: dict, next_position: dict | None) -> bool:
    if image["pageNumber"] < current_position["pageNumber"]:
        return False
    if image["pageNumber"] == current_position["pageNumber"] and image["y"] >= current_position["y"]:
        return False

    if next_position is None:
        return True

    if image["pageNumber"] > next_position["pageNumber"]:
        return False
    if image["pageNumber"] == next_position["pageNumber"] and image["y"] <= next_position["y"]:
        return False

    return True


def image_is_after_question_by_order(image: dict, current_position: dict, next_position: dict | None) -> bool:
    if image["pageNumber"] < current_position["pageNumber"]:
        return False
    if image["pageNumber"] == current_position["pageNumber"] and image["order"] <= current_position["order"]:
        return False

    if next_position is None:
        return True

    if image["pageNumber"] > next_position["pageNumber"]:
        return False
    if image["pageNumber"] == next_position["pageNumber"] and image["order"] >= next_position["order"]:
        return False

    return True


def question_pages_for_chapter(chapter: dict, page_texts: list[str]) -> dict[int, set[int]]:
    pages_by_question = defaultdict(set)
    active_question = None

    for page_number in range(chapter["startPage"], chapter["endPage"] + 1):
        text = normalize_space(page_texts[page_number - 1])
        if not text:
            continue

        solution_match = SOLUTION_HEADING.search(text)
        detail_match = re.search(r"(?m)^Detailed Explanations\s*$", text)
        question_matches = list(QUESTION_HEADING.finditer(text))
        page_stop = min(
            [match.start() for match in (solution_match, detail_match) if match],
            default=len(text),
        )

        if active_question is not None and page_stop > 0:
            pages_by_question[active_question].add(page_number)

        for index, match in enumerate(question_matches):
            if match.start() >= page_stop:
                continue
            active_question = int(match.group(1))
            pages_by_question[active_question].add(page_number)

        if solution_match or detail_match:
            break

    return pages_by_question


def write_question_image(file_name: str, image_bytes: bytes) -> str:
    for directory in OUTPUT_IMAGE_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / file_name).write_bytes(image_bytes)
    return f"/uploads/{file_name}"


def medicomm_atlas_image_url(question: dict, image_slot: int = 1) -> str:
    suffix = f"-i{image_slot}" if image_slot > 1 else ""
    return f"/uploads/medicomm-atlas-{question['id']}{suffix}.png"


def attach_images_to_questions(
    reader: PdfReader,
    chapter: dict,
    questions: list[dict],
    page_texts: list[str],
    write_images: bool,
) -> None:
    if not questions:
        return

    question_positions, available_images = chapter_layout(reader, chapter, page_texts)
    used_images = set()

    for question_index, question in enumerate(questions):
        if not is_visual_question(question):
            continue

        current_position = question_positions.get(question["questionNumber"])
        if not current_position:
            continue

        next_question = questions[question_index + 1] if question_index + 1 < len(questions) else None
        next_position = question_positions.get(next_question["questionNumber"]) if next_question else None
        image = next(
            (
                candidate
                for candidate in available_images
                if (candidate["pageNumber"], candidate["index"]) not in used_images
                and image_is_after_question_before_next(candidate, current_position, next_position)
            ),
            None,
        )
        if not image:
            image = next(
                (
                    candidate
                    for candidate in available_images
                    if (candidate["pageNumber"], candidate["index"]) not in used_images
                    and image_is_after_question_by_order(candidate, current_position, next_position)
                ),
                None,
            )
        if not image:
            continue

        used_images.add((image["pageNumber"], image["index"]))
        file_name = (
            f"yellowfool-{question['examId']}-{question['subjectId']}"
            f"-q{question['questionNumber']:03d}-p{image['pageNumber']}-i{image['index']}{image['extension']}"
        )
        image_url = write_question_image(file_name, image["bytes"]) if write_images else f"/uploads/{file_name}"
        question["imageUrls"] = [image_url]
        question["images"] = [image_url]
        question["sourceImageUrls"] = [image_url]
        question["atlasImageTargetUrls"] = [medicomm_atlas_image_url(question)]
        question["assetNote"] = (
            "Pending Medicomm atlas conversion from the original PDF image; preserve question image order."
        )


def cleanup_subject_images(subject_ids: set[str]) -> None:
    for directory in OUTPUT_IMAGE_DIRS:
        if not directory.exists():
            continue
        for subject_id in subject_ids:
            for image_path in directory.glob(f"yellowfool-*-{subject_id}-q*"):
                try:
                    image_path.unlink()
                except PermissionError:
                    continue


def parse_chapter(chapter: dict, page_texts: list[str], reader: PdfReader, write_images: bool) -> list[dict]:
    text = "\n".join(page_texts[chapter["startPage"] - 1 : chapter["endPage"]])
    text = normalize_space(text)

    explanation_marker = re.search(r"(?m)^Detailed Explanations\s*$", text)
    if explanation_marker:
        question_area = text[: explanation_marker.start()]
        explanation_area = text[explanation_marker.end() :]
    else:
        first_solution = SOLUTION_HEADING.search(text)
        if not first_solution:
            raise ValueError(f"No explanations found for {chapter['title']}.")
        question_area = text[: first_solution.start()]
        explanation_area = text[first_solution.start() :]

    answer_key = parse_answer_key(question_area)
    question_blocks = split_numbered_blocks(QUESTION_HEADING, question_area)
    explanation_blocks = split_numbered_blocks(SOLUTION_HEADING, explanation_area)

    parsed = []
    meta = chapter["subjectMeta"]
    current_exam_id = exam_id(chapter["exam"], chapter["year"])
    current_exam_title = exam_title(chapter["exam"], chapter["year"])

    for question_number in sorted(question_blocks):
        prompt, options = parse_question_block(question_blocks[question_number])
        answer_letter = answer_key.get(question_number)
        answer_index = "abcd".index(answer_letter) if answer_letter in "abcd" else -1
        answer = options[answer_index] if 0 <= answer_index < len(options) else ""
        explanation = normalize_space(explanation_blocks.get(question_number, ""))

        parsed.append(
            {
                "id": f"{current_exam_id}-{meta['id']}-q{question_number:03d}",
                "questionNumber": question_number,
                "sourceQuestionNumber": question_number,
                "year": chapter["year"],
                "examId": current_exam_id,
                "examTitle": current_exam_title,
                "subject": meta["title"],
                "subjectId": meta["id"],
                "subjectTitle": meta["title"],
                "yearId": meta["yearId"],
                "topic": chapter["title"],
                "subtopic": "",
                "prompt": prompt,
                "options": options,
                "answerIndex": answer_index,
                "answer": answer,
                "explanation": explanation or (f"Correct answer: {answer}" if answer else ""),
                "difficulty": "exam",
                "source": "official",
                "sourceExam": chapter["exam"],
                "sourceExamGroup": chapter["examGroup"],
                "chapterTitle": chapter["title"],
                "sourcePdf": PDF_SOURCE_NAME,
                "sourcePdfPageStart": chapter["startPage"],
                "sourcePdfPageEnd": chapter["endPage"],
                "tags": [chapter["exam"], str(chapter["year"]), meta["title"], chapter["title"]],
                "imageUrls": [],
                "images": [],
            }
        )

    if chapter["expectedQuestions"] and len(parsed) != chapter["expectedQuestions"]:
        raise ValueError(
            f"{chapter['title']}: expected {chapter['expectedQuestions']} questions, parsed {len(parsed)}."
        )

    missing_answers = [question["questionNumber"] for question in parsed if question["answerIndex"] < 0]
    missing_explanations = [question["questionNumber"] for question in parsed if not question["explanation"]]
    if missing_answers:
        raise ValueError(f"{chapter['title']}: missing answers for questions {missing_answers}.")
    if missing_explanations:
        raise ValueError(f"{chapter['title']}: missing explanations for questions {missing_explanations}.")

    attach_images_to_questions(reader, chapter, parsed, page_texts, write_images)
    return parsed


def build_exam_entries(questions: list[dict]) -> list[dict]:
    counts = defaultdict(int)
    for question in questions:
        counts[(question["examId"], question["examTitle"], question["year"])] += 1
    return [
        {"id": exam_id_value, "title": title, "year": year, "questionCount": count}
        for (exam_id_value, title, year), count in sorted(counts.items(), key=lambda item: (item[0][2], item[0][0]))
    ]


def recompute_exam_entries(data: dict) -> None:
    existing_titles = {exam.get("id"): exam.get("title") for exam in data.get("exams", [])}
    counts = defaultdict(int)
    years = {}
    titles = {}
    for subject in data.get("subjects", []):
        for question in subject.get("questions", []):
            current_exam_id = question.get("examId")
            if not current_exam_id:
                continue
            counts[current_exam_id] += 1
            years[current_exam_id] = question.get("year")
            titles[current_exam_id] = question.get("examTitle") or existing_titles.get(current_exam_id) or current_exam_id

    data["exams"] = [
        {
            "id": current_exam_id,
            "title": titles[current_exam_id],
            "year": years[current_exam_id],
            "questionCount": count,
        }
        for current_exam_id, count in sorted(counts.items(), key=lambda item: (years.get(item[0]) or 0, item[0]))
    ]


def ensure_subjects(data: dict) -> None:
    subjects = data.setdefault("subjects", [])
    by_id = {subject["id"]: subject for subject in subjects}
    for meta in SUBJECT_META.values():
        if meta["id"] not in by_id:
            subjects.append({**meta, "questionCount": 0, "questions": []})


def merge_into_bank(data: dict, questions: list[dict], selected_subject_ids: set[str]) -> None:
    ensure_subjects(data)

    question_ids = {question["id"] for question in questions}
    imported_exam_ids = {question["examId"] for question in questions}
    subject_questions = defaultdict(list)
    for question in questions:
        subject_questions[question["subjectId"]].append(question)

    for subject in data["subjects"]:
        if subject["id"] not in selected_subject_ids:
            continue
        existing = [
            question
            for question in subject.get("questions", [])
            if question.get("source") == "ai"
            or (
                question.get("id") not in question_ids
                and question.get("sourcePdf") != PDF_SOURCE_NAME
                and question.get("examId") not in imported_exam_ids
            )
        ]
        existing.extend(subject_questions.get(subject["id"], []))
        existing.sort(key=lambda item: (int(item.get("year") or 0), str(item.get("examId") or ""), int(item.get("questionNumber") or 0)))
        subject["questions"] = existing
        subject["questionCount"] = len(existing)

    recompute_exam_entries(data)
    data["exam"] = {
        "id": "neet-aiims-inicet-pyqs",
        "title": "NEET PG + AIIMS/INI-CET PYQs",
        "questionCount": sum(len(subject.get("questions", [])) for subject in data["subjects"]),
    }


def parse_subject_args(values: list[str]) -> set[str] | None:
    if not values:
        return None
    selected = set()
    by_id = {meta["id"]: meta for meta in SUBJECT_META.values()}
    by_slug = {slugify(meta["title"]): meta for meta in SUBJECT_META.values()}
    for value in values:
        key = slugify(value)
        meta = by_id.get(value) or by_slug.get(key)
        if not meta:
            raise SystemExit(f"Unknown subject '{value}'.")
        selected.add(meta["id"])
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description="Import decoded Yellowfool NEET/AIIMS/INI-CET PYQs.")
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF_PATH)
    parser.add_argument("--subject", action="append", default=[], help="Subject id/title to import. Repeatable.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    selected_subject_ids = parse_subject_args(args.subject)
    chapters = load_chapters(selected_subject_ids)
    if not chapters:
        raise SystemExit("No chapters matched the requested subject filter.")
    selected_chapter_subject_ids = {chapter["subjectMeta"]["id"] for chapter in chapters}

    if not args.dry_run:
        cleanup_subject_images(selected_chapter_subject_ids)

    reader = PdfReader(str(args.pdf))
    page_texts = [clean_page_text(page.extract_text() or "") for page in reader.pages]

    questions = []
    for chapter in chapters:
        questions.extend(parse_chapter(chapter, page_texts, reader, not args.dry_run))

    selected_ids = {question["subjectId"] for question in questions}
    summary = defaultdict(int)
    for question in questions:
        summary[(question["subjectTitle"], question["sourceExam"], question["year"])] += 1

    print(f"Parsed {len(questions)} questions from {len(chapters)} chapters.")
    print(f"Attached images to {sum(1 for question in questions if question['imageUrls'])} questions.")
    for (subject, exam, year), count in sorted(summary.items()):
        print(f"  {subject} | {exam} {year}: {count}")

    if args.dry_run:
        return

    for target in TARGET_FILES:
        data = json.loads(target.read_text(encoding="utf-8"))
        merge_into_bank(data, questions, selected_ids)
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Updated {target}.")


if __name__ == "__main__":
    main()
