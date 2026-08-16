import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Consultative Medicine"
CHAPTER_ORDER = 19
SOURCE_PDF = "medicine 1"
TOPIC = "Consultative Medicine"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def q(prompt, answer, wrong, explanation, clinical=False, page=None):
    return {
        "prompt": prompt.strip(),
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "high" if clinical else "moderate",
        "tags": ["clinical"] if clinical else [],
        "sourcePdfPageStart": page,
        "sourcePdfPageEnd": page,
    }


QUESTIONS = [
    q("Medicine 1 defines consulting as seeking advice from someone with expertise in a particular", "Area", ["Drug dose only", "Insurance plan only", "Laboratory machine"], "Chapter 465 defines consultation as seeking advice from someone with expertise in a particular area.", page=3439),
    q("Traditional forms of medical consultation include in-hospital consultation and", "Outpatient consultation", ["Frostbite thawing", "Genomic imprinting", "Snakebite first aid"], "Chapter 465 lists in-hospital and outpatient consultations as traditional consultation forms.", page=3439),
    q("Contemporary consultation forms include e-consultations, telemedicine evaluations and remote medical", "Second opinions", ["Chemotherapy only", "Autopsies", "Defibrillation attempts"], "Medicine 1 describes e-consultations, telemedicine evaluations and remote second opinions as contemporary forms.", page=3439),
    q("Curbside consults are often incomplete or flawed; as a general rule, they should be", "Avoided", ["Preferred for complex problems", "Used instead of documentation", "Limited to emergency surgery only"], "Chapter 465 states curbside consults are often incomplete or flawed and generally should be avoided.", page=3440),
    q("A resident gives a curbside consult. Medicine 1 notes that the supervising physician is responsible for the trainee's", "Recommendations", ["Blood pressure only", "Travel history only", "Family pedigree only"], "Chapter 465 states that when a resident or fellow provides a curbside consult, the supervising physician is responsible for recommendations.", True, page=3440),
    q("Preeclampsia with severe features includes severe blood pressure elevation greater than", "160/110 mmHg", ["120/70 mmHg", "130/80 mmHg", "140/90 mmHg only"], "Chapter 466 lists severe BP elevation >160/110 mmHg among severe features of preeclampsia.", page=3441),
    q("HELLP syndrome is a subtype of severe preeclampsia and stands for hemolysis, elevated liver enzymes and", "Low platelets", ["Low proteinuria", "Low glucose", "Low TSH"], "Medicine 1 defines HELLP as hemolysis, elevated liver enzymes and low platelets.", page=3441),
    q("A pregnant patient has hypertension, proteinuria, headache, pulmonary edema and platelets below 100,000/uL before term. Which management issue is central?", "Balancing maternal and fetal risks", ["Avoiding all monitoring", "Delaying delivery until 42 weeks", "Treating only fetal macrosomia"], "Chapter 466 states preeclampsia management is challenging because it balances maternal and fetal health simultaneously.", True, page=3441),
    q("Pregnant women with surgically repaired congenital heart disease should be jointly managed by an obstetrician and", "Cardiologist", ["Dermatologist only", "Pathologist only", "Radiation oncologist only"], "Medicine 1 recommends joint management by a cardiologist and obstetrician familiar with these problems.", page=3442),
    q("Supraventricular tachycardia in pregnancy is treated similarly to the nonpregnant state, and fetal tolerance of adenosine and calcium channel blockers is", "Acceptable", ["Prohibited in all cases", "Unknown and never used", "Only acceptable after delivery"], "Chapter 466 states treatment is the same as in nonpregnant patients and fetal tolerance of adenosine/calcium channel blockers is acceptable.", page=3442),
    q("A pregnant woman with peripartum cardiomyopathy has persistent abnormal left-ventricular function after recovery. She should be counseled to avoid", "Pregnancy", ["Vaccination", "Echocardiography", "Salt restriction"], "Medicine 1 says women without normal baseline LV function after peripartum cardiomyopathy should avoid pregnancy.", True, page=3442),
    q("All pregnant women should be screened for", "Hepatitis B", ["Thallium", "APOE4", "Cadmium"], "Chapter 466 states all pregnant women should be screened for hepatitis B.", page=3445),
    q("A hepatitis B surface antigen carrier delivers an infant. The infant should receive hepatitis B vaccine and hepatitis B immune globulin preferably within", "72 hours", ["7 days", "3 months", "1 year"], "Medicine 1 recommends HBIG as soon as possible after birth and preferably within the first 72 hours.", True, page=3445),
    q("Poor perioperative functional capacity is defined as inability to walk four blocks or climb two flights of stairs, corresponding to less than", "4 METs", ["1 MET", "10 METs", "20 METs"], "Chapter 467 defines poor exercise tolerance as inability to meet a MET level of 4 or comparable activities.", page=3447),
    q("A patient with moderate or greater functional capacity of at least 4 METs is awaiting elective noncardiac surgery. Medicine 1 generally recommends no further", "Noninvasive cardiac testing", ["Vaccination", "Medication reconciliation", "Hepatitis B screening"], "Chapter 467 states patients with >=4 METs functional capacity generally should not undergo further noninvasive cardiac testing before elective noncardiac surgery.", True, page=3447),
]


def build_questions():
    if len(QUESTIONS) != 15:
        raise AssertionError(f"Expected 15 questions, got {len(QUESTIONS)}")
    if sum(1 for row in QUESTIONS if "clinical" in row.get("tags", [])) < 5:
        raise AssertionError("Expected at least 5 clinical questions")
    topic_slug = slugify(TOPIC)
    questions = []
    for question_order, row in enumerate(QUESTIONS, 1):
        questions.append({
            "id": f"medicine-consultative-medicine-{topic_slug}-{question_order:02d}",
            "subjectId": SUBJECT_ID,
            "subjectTitle": SUBJECT_TITLE,
            "chapterTitle": CHAPTER,
            "chapterOrder": CHAPTER_ORDER,
            "topic": TOPIC,
            "topicTitle": TOPIC,
            "topicOrder": 1,
            "source": "ai",
            "sourcePdf": SOURCE_PDF,
            "imageUrls": [],
            **row,
        })
    return questions


def update(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    questions = build_questions()
    data["questions"] = [
        item for item in data.get("questions", [])
        if not (item.get("subjectId") == SUBJECT_ID and item.get("chapterTitle") == CHAPTER)
    ] + questions
    if len({item["id"] for item in questions}) != 15:
        raise AssertionError("Duplicate consultative medicine question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 15 book-based Consultative Medicine questions.")


if __name__ == "__main__":
    main()
