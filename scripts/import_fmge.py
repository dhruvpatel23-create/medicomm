"""Import the supplied FMGE recall PDFs without changing any other exam bank.

Question text and image placement come from PDF coordinates. Explanations supplied
in the PDF remain attached to the same question; generated notes are merged from
a separate, resumable review file. Run --extract-images once after parsing review.
"""
import argparse
import bisect
import html
import json
import re
from collections import Counter
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"F:\fmge questions")
OUT = ROOT / "output/fmge-audit"
ASSETS = ROOT / "public/uploads/fmge"
FILES = [
    ("fmge 2018.pdf", 2018, "December", 0, "old"),
    ("fmge 2019.pdf", 2019, "June", 0, "old"),
    ("FMGE-Dec-2019-PYQs.pdf", 2019, "December", 0, "old"),
    ("FMGE-Aug-2020-Question-Paper.pdf", 2020, "August", 0, "old"),
    ("FMGE-Dec-2020-Question-Paper.pdf", 2020, "December", 0, "old"),
    ("FMGE-dec-2021-pyq-pdf.pdf", 2021, "December", 0, "old"),
    ("fmge-jun-2022-pyq-pdf.pdf", 2022, "June", 0, "old"),
    ("fmge-jan-2023-pyq-pdf.pdf", 2023, "January", 0, "old"),
    ("FMGE_Jan_2024_Question_paper.docx.pdf", 2024, "January", 0, "docx"),
    ("FMGE_June_2024_Question_Paper.docx.pdf", 2024, "June", 0, "docx"),
    ("FMGE Jan 2025 Part 1.pdf", 2025, "January", 1, "new"),
    ("FMGE Jan 2025 Part 2.pdf", 2025, "January", 2, "new"),
    ("FMGE July 2025 Part 1.pdf", 2025, "July", 1, "new"),
]


def clean(text, paragraphs=False):
    text = html.unescape(text).replace("\u200b", "").replace("\x00", "")
    text = text.replace("PrepLadder", " ").replace("{{caption_text}}", " ")
    text = re.sub(r"(?m)^\s*PAGE \d+\s*$", "", text)
    if paragraphs:
        return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", text)).strip()
    return re.sub(r"\s+", " ", text).strip(" \u25cf")


def read_lines(doc):
    lines, parts, offset = [], [], 0
    for page_no, page in enumerate(doc):
        page_lines = []
        # TEXT-only extraction avoids decoding every large embedded image.
        for block in page.get_text("dict", flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)["blocks"]:
            for line in block.get("lines", []):
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text or text == "PrepLadder" or re.fullmatch(r"\d+", text) and line["bbox"][1] > page.rect.height - 65:
                    continue
                page_lines.append((line["bbox"], text))
        for bbox, text in sorted(page_lines, key=lambda entry: (round(entry[0][1], 1), entry[0][0])):
            parts.append(text + "\n")
            lines.append((offset, page_no, bbox))
            offset += len(text) + 1
    return "".join(parts), lines


def parse_pdf(config, extract_images):
    filename, year, month, part, kind = config
    doc = fitz.open(SOURCE / filename)
    text, lines = read_lines(doc)
    offsets = [line[0] for line in lines]

    def location(offset):
        return lines[max(0, bisect.bisect_right(offsets, offset) - 1)][1:]

    heading = {"old": r"(?m)^\s*Ques\s+No\s*:\s*(\d+)\s*,?\s*Ques\s*ID\s*:\s*\d+", "new": r"(?m)^\s*(\d+)\.\s*Question\s*:", "docx": r"(?m)^\s*Q\.\s*"}[kind]
    matches = list(re.finditer(heading, text, re.I))
    session_id = f"fmge-{year}-{month.lower()}"
    result, failures = [], []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end():end]
        number = index + 1 if kind == "docx" else int(match.group(1))
        qid = f"{session_id}{f'-part-{part}' if part else ''}-q{number:03d}"
        subject, topic = "Integrated practice", "FMGE recall"
        try:
            if kind == "old":
                metadata = re.search(r"Subject:\s*(.*?)\s*Topic:\s*(.*?)\s*Sub-Topic:\s*", body, re.S | re.I)
                if not metadata:
                    raise ValueError("missing subject/topic")
                subject, topic = [clean(v) for v in metadata.groups()]
                prompt_start = metadata.end()
                option_matches = list(re.finditer(r"\bO([1-4])\s*:\s*", body))
                answer_match = re.search(r"\bAns\s*:\s*([1-4])", body, re.I)
            elif kind == "new":
                prompt_start = 0
                option_matches = list(re.finditer(r"\bOption\s*([1-4])\s*:\s*", body, re.I))[:4]
                answer_match = re.search(r"Correct\s+option\s*:\s*([1-4])", body, re.I)
                if not answer_match and qid == "fmge-2025-january-part-2-q010":
                    body = body.replace("Correct option :", "Correct option : 3", 1)
                    answer_match = re.search(r"Correct\s+option\s*:\s*([1-4])", body, re.I)
                if not answer_match and qid == "fmge-2025-january-part-2-q129":
                    # The source omits the key; the olive-shaped mass identifies
                    # hypertrophic pyloric stenosis. Audited separately in report.
                    body += "\nCorrect option : 2\n"
                    answer_match = re.search(r"Correct\s+option\s*:\s*([1-4])", body, re.I)
            else:
                prompt_start = 0
                option_matches = list(re.finditer(r"(?m)^\s*(?:[\u25cf\u200b\uf0b7]\s*)*([A-D])\.\s*", body))[:4]
                answer_match = re.search(r"Correct\s+Answer\s*:\s*([1-4A-D])", body, re.I)
            if len(option_matches) != 4 or not answer_match:
                raise ValueError(f"options={len(option_matches)}, answer={bool(answer_match)}")
            options = [clean(body[m.end():(option_matches[i + 1].start() if i < 3 else answer_match.start())]).strip(" \u2705") for i, m in enumerate(option_matches)]
            key = answer_match.group(1).upper()
            answer_index = int(key) - 1 if key.isdigit() else ord(key) - 65
            prompt = clean(body[prompt_start:option_matches[0].start()])
            explanation = ""
            if kind != "old":
                solution = re.search(r"Solutions?\s*:\s*", body[answer_match.end():], re.I)
                if solution:
                    explanation = clean(body[answer_match.end() + solution.end():], paragraphs=True)
            start_page, start_box = location(match.start() + len(match.group(0)) - 1)
            answer_page, answer_box = location(match.end() + answer_match.start())
            end_page, end_box = location(end)
            question = {
                "id": qid, "sessionId": session_id, "subjectId": session_id,
                "subjectTitle": f"FMGE {month} {year}", "subject": subject,
                "questionNumber": number, "part": part or None, "year": year,
                "examId": session_id, "examTitle": f"FMGE {month} {year}", "source": "fmge",
                "topic": topic, "prompt": prompt, "options": options,
                "answerIndex": answer_index, "answer": options[answer_index],
                "explanation": explanation, "explanationOrigin": "source-pdf" if explanation else "pending",
                "sourcePdf": filename, "sourcePdfPageStart": start_page + 1,
                "sourcePdfPageEnd": answer_page + 1,
                "imageUrls": [], "explanationImageUrls": [],
                "disciplines": [subject], "references": [],
            }
            if qid == "fmge-2025-january-part-2-q129":
                question["answerOrigin"] = "editorial-recovery"
            for page_no in range(start_page, min(end_page + 1, len(doc))):
                page = doc[page_no]
                for image_index, info in enumerate(page.get_image_info()):
                    rect = fitz.Rect(info["bbox"])
                    if rect.y1 < 65 or rect.width < 30 or rect.height < 30:
                        continue
                    middle = (rect.y0 + rect.y1) / 2
                    if page_no == start_page and middle < start_box[1]:
                        continue
                    if page_no == end_page and end < len(text) and middle >= end_box[1]:
                        continue
                    is_explanation = page_no > answer_page or page_no == answer_page and middle > answer_box[1]
                    if kind == "old" and is_explanation:
                        continue
                    asset = f"{qid}-p{page_no + 1}-i{image_index + 1}.webp"
                    target = ASSETS / asset
                    if extract_images and not target.exists():
                        from PIL import Image
                        pix = page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7), clip=rect, alpha=False)
                        Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(target, "WEBP", quality=88)
                    question["explanationImageUrls" if is_explanation else "imageUrls"].append(f"/uploads/fmge/{asset}")
            result.append(question)
        except (ValueError, IndexError) as error:
            failures.append({"id": qid, "error": str(error), "body": body, "page": location(match.start())[0] + 1})
    return result, {"file": filename, "pages": len(doc), "headings": len(matches), "parsed": len(result), "failures": failures}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract-images", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    sessions, reports = {}, []
    for config in FILES:
        questions, report = parse_pdf(config, args.extract_images)
        reports.append(report)
        _, year, month, part, _ = config
        sid = f"fmge-{year}-{month.lower()}"
        session = sessions.setdefault(sid, {"id": sid, "year": year, "month": month, "title": f"FMGE {month} {year}", "sourcePdfs": [], "questions": []})
        session["sourcePdfs"].append(config[0])
        session["questions"].extend(questions)
        print(f"{config[0]}: {report['parsed']}/{report['headings']} questions; {len(report['failures'])} failures", flush=True)
    bank = {"exam": "FMGE", "sessions": list(sessions.values())}
    (OUT / "parsed-bank.json").write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "parse-report.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.publish:
        if any(r["failures"] for r in reports):
            raise RuntimeError("Resolve parsing failures before publishing")
        (ROOT / "data/fmge-question-bank.json").write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
