"""Extract the remaining subjects without changing any existing question banks."""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import import_yellowfool_pyqs as importer


def main():
    subject = sys.argv[1]
    chapters = importer.load_chapters({subject})
    reader = importer.PdfReader(str(importer.DEFAULT_PDF_PATH))
    texts = [""] * len(reader.pages)
    pages = sorted({p for c in chapters for p in range(c["startPage"], c["endPage"] + 1)})
    for index, page in enumerate(pages):
        texts[page - 1] = importer.clean_page_text(reader.pages[page - 1].extract_text() or "")
        if index % 100 == 0:
            print(f"{subject}: extracted {index}/{len(pages)} pages", flush=True)
    if subject == "psychiatry":
        last = chapters[-1]
        starts = []
        for page in range(last["startPage"], last["endPage"] + 1):
            match = re.match(r"(Radiology (AIIMS|INI-CET|NEET) (\d{4})[^\n]*)", texts[page - 1])
            if match:
                starts.append((page, match))
        assert len(starts) == 15
        chapters[-1] = {**last, "endPage": starts[0][0] - 1, "expectedQuestions": 9}
        for index, (page, match) in enumerate(starts):
            exam = "NEET PG" if match[2] == "NEET" else match[2]
            chapters.append({**last, "title": match[1], "subject": "Radiology", "exam": exam,
                "examGroup": "NEET PG" if exam == "NEET PG" else "AIIMS/INI-CET", "year": int(match[3]),
                "startPage": page, "endPage": starts[index + 1][0] - 1 if index + 1 < len(starts) else last["endPage"],
                "expectedQuestions": 0, "subjectMeta": {"id": "radiology", "title": "Radiology", "yearId": "final-year"}})
    questions = []
    for chapter in chapters:
        batch = []
        for session in importer.split_chapter_sessions(chapter, texts):
            batch.extend(importer.parse_chapter(session, texts, reader, True, len(batch)))
        if chapter["expectedQuestions"]:
            assert len(batch) == chapter["expectedQuestions"], chapter["title"]
        questions.extend(batch)
    for q in questions:
        assert q["prompt"] and len(q["options"]) == 4 and all(q["options"]), q["id"]
        assert 0 <= q["answerIndex"] < 4 and q["answer"] == q["options"][q["answerIndex"]], q["id"]
        assert q["explanation"], q["id"]
        if q["explanation"] == f"Correct answer: {q['answer']}":
            print(f"REVIEW explanation: {q['id']} pages {q['sourcePdfPageStart']}-{q['sourcePdfPageEnd']}", flush=True)
    grouped = defaultdict(list)
    for q in questions:
        grouped[q["subjectId"]].append(q)
    for subject_id, batch in grouped.items():
        target = importer.ROOT / "output" / "yellowfool-remaining" / f"{subject_id}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"STAGED {subject_id}: {len(batch)} questions; {sum(bool(q['imageUrls']) for q in batch)} with images", flush=True)


if __name__ == "__main__":
    main()
