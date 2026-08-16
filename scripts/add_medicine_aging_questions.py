import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Aging"
CHAPTER_ORDER = 18
SOURCE_PDF = "medicine 1"
TOPIC = "Aging"


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
    q("Medicine 1 describes the aging process as a major risk factor underlying disease and disability in", "Developed nations", ["Only newborns", "Tropical infections only", "Snakebite mortality only"], "Chapter 463 states that aging is the major risk factor underlying disease and disability in developed nations.", page=3413),
    q("Most definitions of aging include progressive decline in structure and function with impaired maintenance and", "Repair systems", ["Venom neutralization", "Iodine uptake", "Bile secretion"], "The biology of aging chapter defines aging by progressive decline, impaired maintenance and repair, increased disease susceptibility and reduced reproductive capacity.", page=3413),
    q("The Gompertz observation links human aging with an exponential increase in risk of", "Mortality", ["Altitude illness only", "Drug absorption", "Genomic imprinting"], "Medicine 1 notes Gompertz recognized aging as associated with exponential mortality risk over time.", page=3413),
    q("A researcher explains aging as a trade-off between resources for germ cells and soma cells. This is the", "Disposable soma theory", ["Grandmother hypothesis", "Brain drain", "Inverse-care law"], "Chapter 463 describes Kirkwood and Holliday's disposable soma theory as a germ-versus-soma maintenance trade-off.", True, page=3415),
    q("Lipofuscin is a brown autofluorescent pigment within lysosomes and is considered a characteristic histologic feature of", "Aging cells", ["Acute heatstroke", "Snakebite", "Zika infection"], "Medicine 1 describes lipofuscin accumulation in lysosomes as a characteristic feature of aging cells.", page=3416),
    q("Age-related impairment of protein quality maintenance is called impaired", "Proteostasis", ["Hemostasis", "Osmosis", "Phagocytosis only"], "Chapter 463 defines proteostasis as maintenance of protein quality through folding and degradation, impaired with aging.", page=3416),
    q("Aging-related proteostasis defects may contribute to aggregation of tau, beta-amyloid and alpha-synuclein in", "Neurodegenerative diseases", ["Scorpionfish stings", "Frostbite", "Thallium absorption"], "Medicine 1 links age-related proteostasis changes to protein aggregation in dementia and Parkinson disease.", True, page=3416),
    q("APOE4 is described as a risk factor for Alzheimer disease and", "Cardiovascular disease", ["Hypothermia", "Tick paralysis", "Celiac disease only"], "Chapter 463 notes APOE4 is a risk factor for Alzheimer disease and cardiovascular disease and may explain reduced life span association.", page=3417),
    q("Caloric restriction is usually defined as reducing total caloric intake by about", "30% without malnutrition", ["5% with malnutrition", "70% without fluids", "100% fasting only"], "Medicine 1 defines caloric restriction as about 30% reduction in calories without malnutrition.", page=3418),
    q("A geriatric patient has falls, urinary incontinence and possible elder neglect. Medicine 1 emphasizes these as potentially reversible and treatable conditions that are often", "Underdiagnosed", ["Always incurable", "Irrelevant to care", "Limited to pediatrics"], "Chapter 464 lists fall risk, urinary incontinence, and elder abuse/neglect as underdiagnosed treatable conditions detectable with screening.", True, page=3420),
    q("In geriatric care, functional ability and quality of life, rather than cure alone, are key", "Goals of care", ["Contraindications", "Lab artifacts", "Drug classes"], "Medicine 1 lists functional ability and quality of life as key goals in older adults.", page=3420),
    q("Comprehensive geriatric assessment is proposed in geriatric oncology to better predict which older adults will tolerate and benefit from", "Cancer treatment", ["Altitude ascent", "Activated charcoal", "Gene imprinting"], "Chapter 464 notes geriatric oncology uses comprehensive assessment to guide cancer treatment tolerance and benefit.", page=3428),
    q("About what proportion of older community-dwelling adults fall annually?", "One in three", ["One in twenty", "All older adults", "One in one hundred"], "Medicine 1 states about one in three older community-dwelling adults and one in two long-term care residents fall annually.", True, page=3428),
    q("Adverse drug events causing hospitalization in older adults most commonly involve warfarin/antiplatelet agents and insulin or other", "Hypoglycemic agents", ["Antacids only", "Topical emollients", "Artificial tears"], "Chapter 464 identifies warfarin/antiplatelets and insulin/hypoglycemics as main culprits in ADE-related hospitalizations.", True, page=3430),
    q("For insomnia in older adults, nonpharmacologic sleep hygiene includes avoiding caffeine, alcohol and cigarettes after", "Lunch", ["Breakfast only", "Midnight", "Exercise only"], "Table 464-14 lists avoiding caffeine, alcohol and cigarettes after lunch as a sleep hygiene rule.", page=3436),
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
            "id": f"medicine-aging-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate aging question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 15 book-based Aging questions.")


if __name__ == "__main__":
    main()
