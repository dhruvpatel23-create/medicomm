import json
import os
import re

PSYCHIATRY_DB = r"C:\Users\Hp\.gemini\antigravity\scratch\psychiatry_mcq_database"
MASTER_FILE = os.path.join(PSYCHIATRY_DB, "psychiatry_master_mcq_bank.json")

MEDULLA_DIR = r"D:\medullaprep\dhruv1"
DATA_USERS = os.path.join(MEDULLA_DIR, "data", "users.json")
RUNTIME_USERS = os.path.join(MEDULLA_DIR, "runtime-data", "users.json")
DATA_BANK = os.path.join(MEDULLA_DIR, "data", "practice-question-bank.json")
PUBLIC_BANK = os.path.join(MEDULLA_DIR, "public", "practice-question-bank.json")

CHAPTER_TITLES = {
    1: "Diagnosis and Classification in Psychiatry",
    2: "Psychiatric History and Examination",
    3: "Organic (Including Symptomatic) Mental Disorders",
    4: "Psychoactive Substance Use Disorders",
    5: "Schizophrenia",
    6: "Mood Disorders",
    7: "Other Psychotic Disorders",
    8: "Neurotic, Stress-related and Somatoform Disorders",
    9: "Disorders of Adult Personality and Behaviour",
    10: "Sexual Disorders",
    11: "Sleep Disorders",
    12: "Behavioural Syndromes Associated with Psychological Disturbances and Physiological Factors",
    13: "Mental Retardation",
    14: "Child Psychiatry",
    15: "Psychopharmacology",
    16: "Other Biological Methods of Treatment",
    17: "Psychoanalysis",
    18: "Psychological Treatments",
    19: "Emergency Psychiatry",
    20: "Legal and Ethical Issues in Psychiatry",
    21: "Community Psychiatry"
}

def clean_escapes(text):
    out = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == '\\':
            if i + 1 < n and text[i+1] in ['"', '\\', '/', 'b', 'f', 'n', 'r', 't']:
                out.append(text[i:i+2])
                i += 2
            elif i + 5 < n and text[i+1] == 'u' and all(c in '0123456789abcdefABCDEF' for c in text[i+2:i+6]):
                out.append(text[i:i+6])
                i += 6
            else:
                out.append('\\\\')
                i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)

def clean_text(text):
    if text is None: return ""
    text = str(text)
    text = re.sub(r'Niraj\s+Ahuja', 'Clinical Psychiatry Principles', text, flags=re.I)
    text = re.sub(r'A\s+Short\s+Textbook\s+of\s+Psychiatry', 'Comprehensive Psychiatry Review', text, flags=re.I)
    return text.strip()

def normalize_explanation(exp):
    if isinstance(exp, dict):
        parts = []
        if "correct" in exp: parts.append(f"Core Concept: {exp['correct']}")
        parts.append("\nOption Analysis:")
        for k in ["A", "B", "C", "D"]:
            if k in exp: parts.append(f"• Option {k}: {exp[k]}")
        exp = "\n".join(parts)
    return clean_text(exp)

def normalize_options(opts):
    if isinstance(opts, dict):
        return [clean_text(opts.get(k, "")) for k in ["A", "B", "C", "D"]]
    elif isinstance(opts, list):
        return [(clean_text(o)) for o in (opts + ["", "", "", ""])[:4]]
    return ["", "", "", ""]

def load_batch_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    try:
        return json.loads(raw)
    except Exception:
        fixed = clean_escapes(raw)
        return json.loads(fixed)

def main():
    batches = [f"batch_{i:02d}.json" for i in range(1, 4)]
    all_raw_qs = []

    for b in batches:
        bpath = os.path.join(PSYCHIATRY_DB, b)
        if not os.path.exists(bpath):
            print(f"Waiting/Error: {b} does not exist yet.")
            continue
        qs = load_batch_file(bpath)
        print(f"Loaded {len(qs)} questions from {b}")
        all_raw_qs.extend(qs)

    print(f"Total raw questions collected: {len(all_raw_qs)}")

    standardized = []
    chapter_topic_counts = {}

    for idx, q in enumerate(all_raw_qs, 1):
        ch_num = q.get("chapterNumber")
        if not ch_num or not isinstance(ch_num, int):
            ch_title = q.get("chapterTitle", "")
            for num, title in CHAPTER_TITLES.items():
                if title.lower() in ch_title.lower() or ch_title.lower() in title.lower():
                    ch_num = num
                    break
        if not ch_num:
            ch_num = ((idx - 1) // 10) + 1

        ch_title = CHAPTER_TITLES.get(ch_num, f"Chapter {ch_num}")

        chapter_topic_counts[ch_num] = chapter_topic_counts.get(ch_num, 0) + 1
        t_order = chapter_topic_counts[ch_num]

        opt_list = normalize_options(q.get("options"))
        corr_letter = str(q.get("correct_answer", q.get("answer", "A"))).strip().upper()
        letter_to_idx = {"A": 0, "B": 1, "C": 2, "D": 3}
        ans_idx = letter_to_idx.get(corr_letter, 0)
        ans_text = opt_list[ans_idx]

        diff_raw = str(q.get("difficulty", "moderate")).strip().lower()
        if "easy" in diff_raw:
            diff = "easy"
        elif "hard" in diff_raw:
            diff = "hard"
        else:
            diff = "moderate"

        qtype = str(q.get("type", "Clinical")).strip().title()
        if qtype not in ["Clinical", "Factual"]:
            qtype = "Clinical"

        qid = f"psychiatry-ai-ch{ch_num:02d}-q{t_order:02d}"

        norm_q = {
            "id": qid,
            "subjectId": "psychiatry",
            "subjectTitle": "Psychiatry",
            "subject": "Psychiatry",
            "yearId": "final-year",
            "examId": "ai-generated",
            "examTitle": "AI Topic-wise Questions",
            "year": None,
            "questionNumber": idx,
            "source": "ai",
            "imageUrls": [],
            "images": [],
            "chapterTitle": ch_title,
            "chapterOrder": ch_num,
            "topic": ch_title,
            "topicTitle": ch_title,
            "topicOrder": t_order,
            "difficulty": diff,
            "type": qtype,
            "prompt": clean_text(q.get("question", "")),
            "options": opt_list,
            "answerIndex": ans_idx,
            "answer": ans_text,
            "explanation": normalize_explanation(q.get("explanation", ""))
        }
        standardized.append(norm_q)

    # Save Master File
    with open(MASTER_FILE, "w", encoding="utf-8") as out:
        json.dump(standardized, out, indent=2, ensure_ascii=False)
    print(f"Saved master file ({len(standardized)} questions) to: {MASTER_FILE}")

    # 1. Update Medulla data/users.json and runtime-data/users.json
    for upath in [DATA_USERS, RUNTIME_USERS]:
        if os.path.exists(upath):
            with open(upath, "r", encoding="utf-8") as f:
                udata = json.load(f)

            existing = udata.get("questions", [])
            filtered = [q for q in existing if not (q.get("subjectId") == "psychiatry" and q.get("source") == "ai")]
            updated_questions = filtered + standardized
            udata["questions"] = updated_questions

            with open(upath, "w", encoding="utf-8") as f:
                json.dump(udata, f, indent=2, ensure_ascii=False)
            print(f"Updated {upath}: total questions = {len(updated_questions)} (added {len(standardized)} Psychiatry MCQs).")

    # 2. Update Medulla data/practice-question-bank.json and public/practice-question-bank.json
    for bpath in [DATA_BANK, PUBLIC_BANK]:
        if os.path.exists(bpath):
            with open(bpath, "r", encoding="utf-8") as f:
                bank = json.load(f)

            subjects = bank.get("subjects", [])
            psych_sub = None
            for s in subjects:
                if s.get("id") == "psychiatry":
                    psych_sub = s
                    break

            if not psych_sub:
                psych_sub = {
                    "id": "psychiatry",
                    "title": "Psychiatry",
                    "yearId": "final-year",
                    "questionCount": 0,
                    "questions": []
                }
                subjects.append(psych_sub)

            official_qs = [q for q in psych_sub.get("questions", []) if q.get("source") != "ai"]
            new_psych_qs = official_qs + standardized
            psych_sub["questions"] = new_psych_qs
            psych_sub["questionCount"] = len(new_psych_qs)

            bank["subjects"] = subjects
            bank["exam"] = bank.get("exam", {})
            bank["exam"]["questionCount"] = sum(s.get("questionCount", len(s.get("questions", []))) for s in subjects)

            with open(bpath, "w", encoding="utf-8") as f:
                json.dump(bank, f, indent=2, ensure_ascii=False)
            print(f"Updated {bpath}: Psychiatry now has {len(new_psych_qs)} questions ({len(official_qs)} PYQs + {len(standardized)} AI topic-wise questions).")

    print("\nPSYCHIATRY INGESTION COMPLETE!")

if __name__ == "__main__":
    main()
