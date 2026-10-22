import json
import os
import re

SOURCE_MASTER = r"C:\Users\Hp\.gemini\antigravity\scratch\radiology_mcq_database\radiology_master_mcq_bank.json"
MEDULLA_DIR = r"D:\medullaprep\dhruv1"

DATA_USERS = os.path.join(MEDULLA_DIR, "data", "users.json")
RUNTIME_USERS = os.path.join(MEDULLA_DIR, "runtime-data", "users.json")
DATA_BANK = os.path.join(MEDULLA_DIR, "data", "practice-question-bank.json")
PUBLIC_BANK = os.path.join(MEDULLA_DIR, "public", "practice-question-bank.json")

CHAPTER_ORDER = {
    "Introduction to Radiology": 1,
    "Radiation Biology and Radiation Protection": 2,
    "Imaging Techniques": 3,
    "Contrast Media": 4,
    "Approach to Reviewing X-rays": 5,
    "Brain and Spine": 6,
    "Breast Imaging": 7,
    "Cardiovascular Imaging": 8,
    "Chest Imaging": 9,
    "Gastrointestinal and Abdominal Imaging": 10,
    "Obstetrics and Gynecology Imaging": 11,
    "Head and Neck Imaging": 12,
    "Interventional and Vascular Radiology": 13,
    "Musculoskeletal Radiology": 14,
    "Pediatric Radiology": 15,
    "Urogenital Imaging": 16,
    "Normal and Reference Images": 17,
    "High-Yield Cross-Chapter Modules": 18,
    "Additional High-Yield Cross-Chapter Topics": 18
}

def clean_chapter_title(raw):
    raw = str(raw).strip()
    # Strip "Chapter X:"
    raw = re.sub(r'^Chapter\s*\d+\s*:\s*', '', raw, flags=re.I)
    return raw.strip()

def main():
    print(f"Loading master MCQs from: {SOURCE_MASTER}")
    with open(SOURCE_MASTER, "r", encoding="utf-8") as f:
        master_qs = json.load(f)

    print(f"Loaded {len(master_qs)} master MCQs.")

    # Convert to Medulla format
    converted_qs = []
    topic_order_tracker = {}

    for idx, q in enumerate(master_qs, 1):
        raw_ch = q.get("chapter", "")
        ch_title = clean_chapter_title(raw_ch)

        # Match chapter order
        ch_order = 19
        for k, v in CHAPTER_ORDER.items():
            if k.lower() in ch_title.lower() or ch_title.lower() in k.lower():
                ch_order = v
                ch_title = k
                break

        topic_name = str(q.get("topic", "")).strip()
        if ch_title not in topic_order_tracker:
            topic_order_tracker[ch_title] = {}
        if topic_name not in topic_order_tracker[ch_title]:
            topic_order_tracker[ch_title][topic_name] = len(topic_order_tracker[ch_title]) + 1
        topic_order = topic_order_tracker[ch_title][topic_name]

        # Options normalization
        raw_opts = q.get("options", {})
        if isinstance(raw_opts, dict):
            opt_list = [raw_opts.get("A", ""), raw_opts.get("B", ""), raw_opts.get("C", ""), raw_opts.get("D", "")]
        elif isinstance(raw_opts, list):
            opt_list = (raw_opts + ["", "", "", ""])[:4]
        else:
            opt_list = ["", "", "", ""]

        opt_list = [str(o).strip() for o in opt_list]

        corr_letter = str(q.get("correct_answer", "A")).strip().upper()
        letter_to_idx = {"A": 0, "B": 1, "C": 2, "D": 3}
        ans_idx = letter_to_idx.get(corr_letter, 0)
        ans_text = opt_list[ans_idx] if ans_idx < len(opt_list) else opt_list[0]

        diff_raw = str(q.get("difficulty", "Medium")).strip().lower()
        if "easy" in diff_raw:
            diff = "easy"
        elif "hard" in diff_raw:
            diff = "hard"
        else:
            diff = "moderate"

        qid = f"radiology-ai-ch{ch_order:02d}-t{topic_order:02d}-q{idx:04d}"

        medulla_q = {
            "id": qid,
            "subjectId": "radiology",
            "subjectTitle": "Radiology",
            "subject": "Radiology",
            "yearId": "third-year",
            "examId": "ai-generated",
            "examTitle": "AI Topic-wise Questions",
            "year": None,
            "questionNumber": idx,
            "source": "ai",
            "imageUrls": [],
            "images": [],
            "chapterTitle": ch_title,
            "chapterOrder": ch_order,
            "topic": topic_name,
            "topicTitle": topic_name,
            "topicOrder": topic_order,
            "difficulty": diff,
            "prompt": str(q.get("question", "")).strip(),
            "options": opt_list,
            "answerIndex": ans_idx,
            "answer": ans_text,
            "explanation": str(q.get("explanation", "")).strip()
        }
        converted_qs.append(medulla_q)

    print(f"Successfully converted {len(converted_qs)} questions to Medulla format.")

    # 1. Update data/users.json and runtime-data/users.json
    for upath in [DATA_USERS, RUNTIME_USERS]:
        if os.path.exists(upath):
            with open(upath, "r", encoding="utf-8") as f:
                udata = json.load(f)

            # Remove any existing radiology AI questions to avoid duplicates
            existing = udata.get("questions", [])
            filtered = [q for q in existing if not (q.get("subjectId") == "radiology" and q.get("source") == "ai")]
            updated_questions = filtered + converted_qs
            udata["questions"] = updated_questions

            with open(upath, "w", encoding="utf-8") as f:
                json.dump(udata, f, indent=2, ensure_ascii=False)
            print(f"Updated {upath}: {len(updated_questions)} total questions (added {len(converted_qs)} Radiology MCQs).")

    # 2. Update data/practice-question-bank.json and public/practice-question-bank.json
    for bpath in [DATA_BANK, PUBLIC_BANK]:
        if os.path.exists(bpath):
            with open(bpath, "r", encoding="utf-8") as f:
                bank = json.load(f)

            subjects = bank.get("subjects", [])
            radiology_sub = None
            for s in subjects:
                if s.get("id") == "radiology":
                    radiology_sub = s
                    break

            if not radiology_sub:
                radiology_sub = {
                    "id": "radiology",
                    "title": "Radiology",
                    "yearId": "third-year",
                    "questionCount": 0,
                    "questions": []
                }
                subjects.append(radiology_sub)

            # Keep existing official PYQs, remove old AI radiology questions
            official_qs = [q for q in radiology_sub.get("questions", []) if q.get("source") != "ai"]
            new_radiology_qs = official_qs + converted_qs
            radiology_sub["questions"] = new_radiology_qs
            radiology_sub["questionCount"] = len(new_radiology_qs)

            # Update total question count
            bank["subjects"] = subjects
            bank["exam"] = bank.get("exam", {})
            bank["exam"]["questionCount"] = sum(s.get("questionCount", len(s.get("questions", []))) for s in subjects)

            with open(bpath, "w", encoding="utf-8") as f:
                json.dump(bank, f, indent=2, ensure_ascii=False)
            print(f"Updated {bpath}: Radiology now has {len(new_radiology_qs)} questions ({len(official_qs)} PYQs + {len(converted_qs)} AI questions).")

    print("\nINGESTION COMPLETE!")

if __name__ == "__main__":
    main()
