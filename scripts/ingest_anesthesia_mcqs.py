import json
import os
import re

ANESTHESIA_DB = r"C:\Users\Hp\.gemini\antigravity\scratch\anesthesia_mcq_database"
MASTER_FILE = os.path.join(ANESTHESIA_DB, "anesthesia_master_mcq_bank.json")

MEDULLA_DIR = r"D:\medullaprep\dhruv1"
DATA_USERS = os.path.join(MEDULLA_DIR, "data", "users.json")
RUNTIME_USERS = os.path.join(MEDULLA_DIR, "runtime-data", "users.json")
DATA_BANK = os.path.join(MEDULLA_DIR, "data", "practice-question-bank.json")
PUBLIC_BANK = os.path.join(MEDULLA_DIR, "public", "practice-question-bank.json")

CHAPTER_TITLES = {
    1: "Anatomy, Physiology and Applied Physics",
    2: "Historical Milestones in Anesthesia",
    3: "Preoperative Checkup",
    4: "Fluids",
    5: "Blood Transfusion",
    6: "Monitoring in Anesthesia",
    7: "Glimpse of General Anesthesia",
    8: "Inhalational Anesthetics",
    9: "Intravenous Anesthetic Agents",
    10: "Muscle Relaxants",
    11: "Local Anesthetics",
    12: "Central Neuraxial Blocks",
    13: "Peripheral Nerve Blocks",
    14: "Anesthesia and Cardiac Disease",
    15: "Anesthesia for Respiratory Diseases",
    16: "Anesthesia for Central Nervous Diseases",
    17: "Anesthesia for Liver Diseases",
    18: "Anesthesia for Renal Diseases",
    19: "Anesthesia for Endocrine Disorders",
    20: "Anesthesia for Patients with Neuromuscular Diseases",
    21: "Anesthesia for Immune-Mediated and Infectious Diseases",
    22: "Anesthesia for Disorders of Blood",
    23: "Neurosurgical Anesthesia",
    24: "Anesthesia for Obstetrics",
    25: "Pediatric Anesthesia",
    26: "Geriatric Anesthesia",
    27: "Anesthesia for Obese Patients",
    28: "Anesthesia for Laparoscopy",
    29: "Anesthesia for Ophthalmic Surgeries",
    30: "Anesthesia for ENT Surgery",
    31: "Anesthesia in Trauma Patients",
    32: "Anesthesia for Orthopedic Surgery",
    33: "Nonoperating Room Anesthesia",
    34: "Anesthesia at Remote Locations",
    35: "Anesthesia for Daycare Surgeries",
    36: "Pain and Anesthesia",
    37: "Gases Used in Anesthesia: Road to Mountain",
    38: "Complications in Anesthesia",
    39: "The Newer Concept in Anesthesia: Artificial Intelligence",
    40: "Cardiopulmonary Resuscitation",
    41: "Anesthesiology: Ethics, Career, Medication, and Medical Errors",
    42: "Postanesthesia Care Unit",
    43: "Basics of Ventilator",
    44: "Intensive Care Unit",
    45: "Anesthesia Workstation",
    46: "Equipment for Airway Management",
    47: "Oxygen Delivery Devices",
    48: "Sterilization of Anesthesia Equipment"
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
    text = re.sub(r'Puneet\s+Khanna', 'Clinical Anesthesia Principles', text, flags=re.I)
    text = re.sub(r'Shashikant\s+Sharma', 'Standard Anesthesiology Guidelines', text, flags=re.I)
    return text.strip()

def normalize_explanation(exp):
    if isinstance(exp, dict):
        parts = []
        if "correct" in exp: parts.append(f"Correct: {exp['correct']}")
        for k in ["A", "B", "C", "D"]:
            if k in exp: parts.append(f"Option {k}: {exp[k]}")
        exp = "\n\n".join(parts)
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
    batches = [f"batch_{i:02d}.json" for i in range(1, 7)]
    all_raw_qs = []

    for b in batches:
        bpath = os.path.join(ANESTHESIA_DB, b)
        if not os.path.exists(bpath):
            print(f"Error: {b} does not exist!")
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

        qid = f"anesthesia-ai-ch{ch_num:02d}-q{t_order:02d}"

        norm_q = {
            "id": qid,
            "subjectId": "anesthesia",
            "subjectTitle": "Anesthesia",
            "subject": "Anesthesia",
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
            filtered = [q for q in existing if not (q.get("subjectId") == "anesthesia" and q.get("source") == "ai")]
            updated_questions = filtered + standardized
            udata["questions"] = updated_questions

            with open(upath, "w", encoding="utf-8") as f:
                json.dump(udata, f, indent=2, ensure_ascii=False)
            print(f"Updated {upath}: total questions = {len(updated_questions)} (added {len(standardized)} Anesthesia MCQs).")

    # 2. Update Medulla data/practice-question-bank.json and public/practice-question-bank.json
    for bpath in [DATA_BANK, PUBLIC_BANK]:
        if os.path.exists(bpath):
            with open(bpath, "r", encoding="utf-8") as f:
                bank = json.load(f)

            subjects = bank.get("subjects", [])
            anes_sub = None
            for s in subjects:
                if s.get("id") == "anesthesia":
                    anes_sub = s
                    break

            if not anes_sub:
                anes_sub = {
                    "id": "anesthesia",
                    "title": "Anesthesia",
                    "yearId": "final-year",
                    "questionCount": 0,
                    "questions": []
                }
                subjects.append(anes_sub)

            official_qs = [q for q in anes_sub.get("questions", []) if q.get("source") != "ai"]
            new_anes_qs = official_qs + standardized
            anes_sub["questions"] = new_anes_qs
            anes_sub["questionCount"] = len(new_anes_qs)

            bank["subjects"] = subjects
            bank["exam"] = bank.get("exam", {})
            bank["exam"]["questionCount"] = sum(s.get("questionCount", len(s.get("questions", []))) for s in subjects)

            with open(bpath, "w", encoding="utf-8") as f:
                json.dump(bank, f, indent=2, ensure_ascii=False)
            print(f"Updated {bpath}: Anesthesia now has {len(new_anes_qs)} questions ({len(official_qs)} PYQs + {len(standardized)} AI topic-wise questions).")

    print("\nANESTHESIA INGESTION COMPLETE!")

if __name__ == "__main__":
    main()
