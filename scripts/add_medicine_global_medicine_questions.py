import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Global Medicine"
CHAPTER_ORDER = 17
SOURCE_PDF = "medicine 1"
TOPIC = "Global Medicine"


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
    q("Medicine 1 describes global health as improving the health of all people and achieving health equity worldwide, with emphasis on", "Transnational problems", ["Only private hospital financing", "Only rare single-gene disorders", "Only elective surgery"], "Chapter 460 defines global health around health improvement, worldwide equity and transnational problems.", page=3391),
    q("In 2015, Medicine 1 states that 10.7% of the world's population lived on less than what amount per day?", "$1.90 U.S.", ["$10 U.S.", "$25 U.S.", "$100 U.S."], "Chapter 460 uses <$1.90 U.S. per day as a standard measure of extreme poverty and gives 10.7% for 2015.", page=3393),
    q("Global health equity emphasizes equitable access to", "High-value health interventions", ["Only low-cost interventions regardless of effect", "Only genetic testing panels", "Only hospital-based specialty procedures"], "Medicine 1 uses global health equity to stress equitable access to high-value interventions.", page=3395),
    q("In 2015, approximately how many people worldwide were living with HIV infection?", "38.8 million", ["3.8 million", "388,000", "388 million"], "Chapter 460 states approximately 38.8 million people worldwide were living with HIV infection in 2015.", page=3395),
    q("A clinician planning HIV services in a low-income setting applies lessons from HIV/AIDS to tuberculosis and malaria care. The chapter frames this as overcoming barriers to prevention, diagnosis and", "Care", ["Genetic recombination", "Heat transfer", "Snake identification"], "Medicine 1 uses HIV/AIDS and other diseases to discuss barriers to prevention, diagnosis and care and ways to overcome them.", True, page=3391),
    q("The WHO-recommended minimum health workforce density cited in Medicine 1 is 4.45 physicians, nurses and midwives per", "1000 persons", ["100 persons", "10,000 persons", "100,000 persons"], "Chapter 460 cites WHO's minimum of 4.45 physicians, nurses and midwives per 1000 persons.", page=3397),
    q("The emigration of physicians and nurses from resource-poor countries to opportunities abroad is called the", "Brain drain", ["Inverse-care law", "Herd immunity", "Precision medicine"], "Medicine 1 calls this workforce migration the brain drain.", page=3397),
    q("A rural district has most of its population outside cities but most clinical officers and nurses in urban facilities. This illustrates", "Rural-urban health workforce disparity", ["Dengue serotype immunity", "Genomic imprinting", "Altitude acclimatization"], "Chapter 460 describes rural-urban disparities in health care personnel as mirroring disparities of wealth and health.", True, page=3397),
    q("In 2015, diabetes caused an estimated 1.5 million deaths, with more than 80% occurring in", "Low- and middle-income countries", ["Only high-income countries", "Only island nations", "Only countries without cities"], "Medicine 1 states that more than 80% of diabetes deaths occurred in low- and middle-income countries.", page=3399),
    q("Persistently elevated blood pressure above 180/110 in sub-Saharan Africa is described as often undetected, untreated and", "Uncontrolled", ["Always mild", "Curative", "Protective"], "Chapter 460 notes that blood pressure above 180/110 often goes undetected, untreated and uncontrolled in that setting.", page=3399),
    q("A nurse-run rural clinic in Africa needs essential medicines for severe hypertension. Medicine 1 argues that such centers must quickly gain access to", "Antihypertensive medications", ["Antivenom only", "PET scanners", "Genome sequencers"], "Chapter 460 states rural health centers must gain access to antihypertensive medications.", True, page=3399),
    q("An estimated how many people lack access to essential health services?", "400 million", ["4 million", "40 million", "4 billion"], "Chapter 461 states an estimated 400 million people lack access to essential health services.", page=3401),
    q("The preponderance of emerging infectious diseases are", "Zoonotic in origin", ["Always vector-free", "Exclusively bacterial", "Limited to hospitals"], "Medicine 1 cites review data showing most emerging infectious disease events are zoonotic.", page=3402),
    q("A pregnant woman infected with Zika virus in the first trimester asks about fetal microcephaly risk. Medicine 1 gives an approximate first-trimester risk of", "8%", ["0.08%", "50%", "90%"], "Chapter 461 reports Zika-associated microcephaly risk around 8% after first-trimester infection.", True, page=3404),
    q("Universal health coverage can be considered along population covered, services underwritten and percentage of", "Costs paid", ["Genes sequenced", "Mosquitoes trapped", "Hospitals commercialized"], "Chapter 462 describes three axes of coverage: proportion of population, range of services and percentage of costs paid.", True, page=3409),
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
            "id": f"medicine-global-medicine-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate global medicine question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 15 book-based Global Medicine questions.")


if __name__ == "__main__":
    main()
