import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Disorders Associated with Environmental Exposures"
CHAPTER_ORDER = 15
SOURCE_PDF = "medicine 1"
TOPIC = "Disorders Associated with Environmental Exposures"


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
    q("Altitude illness is likely to occur above what altitude, although it has been documented lower?", "2500 m", ["500 m", "1000 m", "8000 m only"], "Chapter 453 states that altitude illness is likely above 2500 m but has been documented at 1500-2500 m.", page=3333),
    q("The benign form of altitude illness is acute mountain sickness, whereas HACE and HAPE are", "Life-threatening", ["Always asymptomatic", "Non-hypoxic disorders", "Limited to sea level"], "Medicine 1 contrasts AMS as benign with HACE and HAPE as life-threatening altitude illnesses.", page=3333),
    q("A trekker rapidly reaches 3860 m and develops headache, nausea and malaise. Which prevention drug is effective when started before ascent?", "Acetazolamide", ["Ginkgo biloba", "Spironolactone", "Antacids"], "Chapter 453 states acetazolamide 125-250 mg twice daily started before ascent is effective for AMS prevention, while Ginkgo biloba is ineffective.", True, page=3335),
    q("Acetazolamide prevents acute mountain sickness by producing metabolic acidosis and", "Hyperventilation", ["Bronchoconstriction", "Fluid retention", "Hypoglycemia"], "Medicine 1 explains acetazolamide's useful effect as metabolic acidosis that drives hyperventilation.", page=3335),
    q("High-altitude pulmonary edema is a noncardiogenic pulmonary edema with normal pulmonary artery", "Wedge pressure", ["Oxygen content", "Wall thickness", "Venous lactate"], "Chapter 453 describes HAPE as noncardiogenic pulmonary edema with normal pulmonary artery wedge pressure.", page=3336),
    q("A climber with HAPE-prone history asks about prevention. Tadalafil decreases HAPE risk by acting as a", "Phosphodiesterase-5 inhibitor", ["Beta-lactam antibiotic", "Anticholinergic", "Chelator"], "Medicine 1 notes that tadalafil, a phosphodiesterase-5 inhibitor, decreased HAPE risk by 65% in one study.", True, page=3336),
    q("At high altitude, asthmatic patients should carry all medications including oral", "Glucocorticoids", ["Warfarin", "Radioiodine", "Prussian blue"], "Chapter 453 advises asthmatic individuals at altitude to carry all medications, including oral glucocorticoids with instructions.", page=3338),
    q("Low-risk pregnant women are generally not at special risk ascending to 3000 m, but going higher is", "Unadvisable", ["Mandatory", "Protective against hypoxemia", "A treatment for preeclampsia"], "Medicine 1 says higher than 3000 m is unadvisable for pregnant women because oxygen saturation drops steeply.", page=3338),
    q("The largest proportion of heat loss in hypothermia occurs through", "Radiation", ["Respiration only", "Evaporation only", "Conduction only"], "Chapter 454 lists radiation as 55-65% of heat loss.", page=3339),
    q("Hypothermia should be confirmed by measuring core temperature, preferably at", "Two sites", ["One infrared tympanic reading only", "The forehead only", "Room temperature"], "Medicine 1 recommends core temperature measurement at two sites and warns against relying solely on infrared tympanic thermography.", True, page=3340),
    q("In hypothermic ventricular fibrillation below 30 C, Medicine 1 says one defibrillation attempt is warranted, then further attempts should wait until", "Some rewarming occurs", ["The patient reaches 20 C", "Activated charcoal is given", "Frostbite blisters are debrided"], "Chapter 454 advises one defibrillation attempt below 30 C and deferring further attempts until 1-2 C rewarming.", True, page=3340),
    q("Airway rewarming in hypothermia uses heated humidified oxygen at", "40-45 C", ["10-15 C", "20-25 C", "60-70 C"], "Chapter 454 lists heated humidified oxygen at 40-45 C as a convenient active core rewarming option.", page=3341),
    q("Before thawing frostbite, the frozen part should be protected with no", "Friction or massage", ["Elevation", "Core temperature stabilization", "Medical assessment"], "Table 454-4 says to protect the frozen part and avoid friction or massage.", page=3342),
    q("A mountaineer has frozen toes. Rewarming should immerse the part in circulating water at", "37-40 C", ["0-4 C", "20-25 C", "50-55 C"], "Medicine 1 frostbite treatment recommends thermometer-monitored circulating water at 37-40 C until distal flush.", True, page=3342),
    q("Heatstroke is suggested by exposure to heat stress, CNS dysfunction and elevated", "Core temperature", ["Serum calcium only", "Radioiodine uptake", "Bone density"], "Chapter 455 describes heatstroke by heat exposure, CNS dysfunction and elevated core temperature as the diagnostic triad.", True, page=3345),
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
            "id": f"medicine-environmental-exposures-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate environmental exposure question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 15 book-based Disorders Associated with Environmental Exposures questions.")


if __name__ == "__main__":
    main()
