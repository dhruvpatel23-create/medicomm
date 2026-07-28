import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Preventive Medicine in Obstetrics, Paediatrics and Geriatrics"
CHAPTER_ORDER = 7
BASE = {
    "subjectId": "community-medicine",
    "subjectTitle": "Community Medicine",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "sourcePdf": "parks 1.pdf",
    "chapterOrder": CHAPTER_ORDER,
    "imageUrls": [],
}


def q(prompt, answer, wrong, explanation, clinical=False):
    return {
        "prompt": prompt,
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "moderate",
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("preventive-obstetrics", "Preventive Obstetrics and Antenatal Care", 1, [
        q("The main purpose of antenatal care is early detection of risk and what?", "Promotion of safe motherhood", ["Vector control", "Cancer chemotherapy", "Rabies surveillance"], "Antenatal care monitors mother and fetus, detects complications and promotes safe delivery."),
        q("A minimum antenatal package should include blood pressure recording and testing for what?", "Anaemia and urine abnormalities", ["Mosquito species", "Visual acuity only", "Dog bite category"], "ANC screens for anaemia, pre-eclampsia, infections and other risks."),
        q("Iron-folic acid supplementation in pregnancy primarily prevents which common condition?", "Anaemia", ["Rabies", "Dengue", "Scabies"], "Iron-folic acid reduces nutritional anaemia in pregnancy."),
        q("A pregnant woman at 32 weeks has headache, BP 160/110 mmHg and pedal oedema. What is the priority?", "Urgent evaluation for pre-eclampsia", ["Routine advice only", "Delay until delivery pain", "Only vitamin A"], "Severe hypertension with symptoms in pregnancy suggests pre-eclampsia and needs urgent care.", True),
        q("Tetanus immunization in pregnancy protects mainly against which outcome?", "Maternal and neonatal tetanus", ["Measles", "Malaria", "Typhoid"], "Maternal tetanus immunization protects mother and newborn through antibodies."),
        q("Birth preparedness includes identifying place of delivery, transport and what?", "Skilled birth attendance", ["Mosquito nets only", "Cancer screening only", "School enrolment"], "Preparedness reduces delays in seeking and reaching obstetric care."),
        q("High-risk pregnancy approach is used to identify women who need what?", "Closer monitoring and referral", ["No antenatal visits", "Only home remedies", "Avoid institutional delivery"], "High-risk mothers require appropriate referral and supervision."),
        q("A primigravida with severe pallor and breathlessness is found Hb 6 g/dL. Which prevention programme component failed or needs strengthening?", "Anaemia prevention and early antenatal detection", ["Dog vaccination", "Vector fogging", "Leprosy MDT"], "Severe anaemia indicates need for early screening, supplementation and referral.", True),
        q("Postnatal care is important because many maternal deaths occur during which period?", "Early postpartum period", ["Only adolescence", "Only menopause", "Only before conception"], "The postpartum period carries risk of haemorrhage, sepsis and hypertensive complications."),
        q("A woman develops heavy bleeding after delivery at home. Which public health measure most directly prevents death?", "Skilled delivery care with emergency obstetric referral", ["Delayed transport", "Only oral iron", "No birth plan"], "Skilled care and timely referral reduce maternal mortality from postpartum haemorrhage.", True),
    ]),
    ("preventive-paediatrics", "Preventive Paediatrics and Child Health", 2, [
        q("Growth monitoring in children is used mainly to detect what early?", "Growth faltering and undernutrition", ["Hypertension in adults", "Cataract", "Occupational injury"], "Serial growth charts help detect malnutrition and illness early."),
        q("Exclusive breastfeeding is recommended for the first how many months of life?", "6 months", ["1 month", "2 years without food", "5 years"], "Exclusive breastfeeding for 6 months supports nutrition and infection protection."),
        q("Complementary feeding should be started at what age?", "6 months", ["At birth", "After 2 years", "Only after school entry"], "At 6 months breast milk alone is insufficient for energy and micronutrients."),
        q("A 7-month-old infant is still exclusively breastfed and has poor weight gain. What counselling is needed?", "Start appropriate complementary feeding while continuing breastfeeding", ["Stop all breastfeeding immediately", "Give only water", "Delay feeding till 1 year"], "Complementary foods should begin at 6 months with continued breastfeeding.", True),
        q("Integrated management of neonatal and childhood illness uses what approach?", "Syndromic assessment and classification", ["Only specialist MRI", "Only autopsy", "Only adult BP screening"], "IMNCI uses simple signs to classify and manage common childhood illnesses."),
        q("Oral rehydration therapy prevents death in diarrhoea mainly by correcting what?", "Dehydration", ["Blindness", "Anaemia only", "Hypertension"], "ORS replaces water and electrolytes lost in diarrhoea."),
        q("Vitamin A supplementation in children prevents which eye condition?", "Xerophthalmia", ["Cataract only", "Glaucoma", "Trachoma always"], "Vitamin A prevents nutritional blindness due to deficiency."),
        q("A child with diarrhoea has sunken eyes and drinks eagerly. What should be assessed and managed first?", "Degree of dehydration", ["Blood group", "Visual acuity", "Hearing threshold"], "Diarrhoeal illness management is based on dehydration assessment.", True),
        q("Under-five mortality rate is a sensitive indicator of child health and what?", "Socioeconomic development", ["Only hospital paint quality", "Only mosquito species", "Only adult literacy"], "U5MR reflects nutrition, infection control, maternal care and living conditions."),
        q("A 2-year-old with bilateral pitting oedema and wasting needs urgent care for which condition?", "Severe acute malnutrition", ["Simple obesity", "Normal growth", "Mild fever only"], "Oedema and severe wasting suggest SAM requiring protocol-based management.", True),
    ]),
    ("school-adolescent-health", "School and Adolescent Health", 3, [
        q("School health services primarily aim to promote health through screening, health education and what?", "Healthy school environment", ["Only curative surgery", "Only hospital admission", "Only death registration"], "School health includes examination, immunization, nutrition, environment and education."),
        q("A school health examination should commonly include assessment of vision and what?", "Growth and nutritional status", ["Only income tax", "Only property records", "Only vehicle licence"], "School screening detects common health, nutrition and developmental problems."),
        q("Mid-day meal programme contributes to child health mainly by improving nutrition and what?", "School attendance", ["Vector breeding", "Smoking rates in adults", "Birth registration only"], "School meals support nutrition and education participation."),
        q("A teacher notices a child sitting close to the blackboard and copying poorly. Which school health action is indicated?", "Vision screening and referral", ["Rabies prophylaxis", "Malaria mass drug administration", "No action"], "Visual defects are common school health problems and need correction.", True),
        q("Adolescent health programmes address nutrition, mental health, substance misuse and what?", "Reproductive and sexual health", ["Only geriatric falls", "Only cataract surgery", "Only neonatal jaundice"], "Adolescent services cover physical, mental, nutritional and reproductive health needs."),
        q("Weekly iron-folic acid supplementation in adolescents targets prevention of what?", "Anaemia", ["Tuberculosis", "Rabies", "Leprosy"], "WIFS reduces adolescent anaemia."),
        q("Life skills education is important for adolescents because it improves what?", "Decision-making and coping abilities", ["Only height", "Only blood group", "Only vaccine potency"], "Life skills support healthy behaviour and psychosocial development."),
        q("An adolescent girl has fatigue, pallor and poor school performance. Which public health intervention is most relevant?", "Anaemia screening and iron-folic acid supplementation", ["Only deworming of dogs", "Only cataract camp", "Only old age pension"], "Adolescent anaemia affects health and learning and is addressed through WIFS and nutrition measures.", True),
        q("School sanitation programmes reduce disease by improving water, toilets and what?", "Hand hygiene", ["Television time", "Classroom colour", "Shoe brand"], "WASH in schools prevents enteric infections and improves attendance."),
        q("A school reports repeated diarrhoea outbreaks after lunch. Which preventive area should be investigated first?", "Food hygiene and safe water", ["Genetic counselling", "Geriatric screening", "TB chemotherapy only"], "Food and water safety are key in school diarrhoeal outbreaks.", True),
    ]),
    ("geriatric-preventive-medicine", "Geriatric Preventive Medicine", 4, [
        q("Geriatric preventive care focuses on healthy ageing, early disease detection and what?", "Maintenance of functional ability", ["Only fertility control", "Only neonatal care", "Only vector control"], "The goal is preserving independence and quality of life."),
        q("A common geriatric public health problem is increased risk of what?", "Falls", ["Measles in all elders", "Neonatal tetanus", "Congenital rubella"], "Falls are common and preventable causes of disability in older adults."),
        q("Comprehensive geriatric assessment includes medical, functional, psychological and what?", "Social assessment", ["Only blood group", "Only caste certificate", "Only rainfall record"], "Older adults need multidimensional assessment."),
        q("An elderly woman with poor vision, loose rugs and previous fall needs which intervention?", "Fall risk assessment and home safety modification", ["Only ORS", "BCG vaccination", "No follow-up"], "Fall prevention includes vision correction, medication review, exercise and environmental safety.", True),
        q("Polypharmacy in older adults increases risk of which problem?", "Adverse drug reactions", ["Improved immunity always", "No interactions", "Reduced falls always"], "Multiple medications increase drug interaction and adverse effect risk."),
        q("Screening for hypertension and diabetes in older adults is useful because these conditions are often what?", "Asymptomatic initially", ["Always painful", "Always infectious", "Always congenital"], "Common chronic diseases may be silent and detectable by screening."),
        q("Immunization of older adults may include influenza and which vaccine depending on guidelines and risk?", "Pneumococcal vaccine", ["Only BCG every month", "Only OPV", "Only measles vaccine in all elders"], "Selected adult vaccines reduce serious respiratory infections."),
        q("An elderly man living alone has weight loss, sadness and poor sleep. Which issue should be screened?", "Depression", ["Neonatal sepsis", "Polio AFP", "Pregnancy"], "Depression is common, under-recognized and treatable in older adults.", True),
        q("Rehabilitation in geriatrics aims mainly to restore function and prevent what?", "Dependence", ["Birth defects", "Vector breeding", "Food adulteration"], "Rehabilitation helps older adults regain independence."),
        q("An older stroke survivor receives physiotherapy, assistive devices and caregiver training. Which care component is this?", "Geriatric rehabilitation", ["Antenatal care", "School health", "Mass immunization only"], "Post-stroke rehabilitation reduces disability and caregiver burden.", True),
    ]),
]


def build():
    out = []
    for slug, topic, order, rows in TOPICS:
        for i, row in enumerate(rows, 1):
            shift = (order + i) % 4
            opts = row["options"][shift:] + row["options"][:shift]
            ans = row["answer"]
            out.append({
                **BASE,
                **row,
                "id": f"community-medicine-obg-paeds-geriatrics-{slug}-{i:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": order,
                "options": opts,
                "answerIndex": opts.index(ans),
                "answer": ans,
            })
    return out


def validate(qs):
    if len(qs) != 40:
        raise ValueError(f"Expected 40, got {len(qs)}")
    if len({q["id"] for q in qs}) != 40:
        raise ValueError("Duplicate IDs")
    for _, topic, _, _ in TOPICS:
        topic_qs = [q for q in qs if q["topic"] == topic]
        clinical = sum("clinical" in q.get("tags", []) for q in topic_qs)
        if len(topic_qs) != 10 or clinical < 3:
            raise ValueError(f"{topic}: {len(topic_qs)} questions, {clinical} clinical")
    for item in qs:
        if item["answer"] != item["options"][item["answerIndex"]]:
            raise ValueError(item["id"])


def update(path, qs):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    ids = {q["id"] for q in qs}
    data["questions"] = [q for q in data.get("questions", []) if q.get("id") not in ids] + qs
    data["questions"].sort(key=lambda q: q.get("id", ""))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    qs = build()
    validate(qs)
    for path in DATA_PATHS:
        update(path, qs)
        print(f"Added {len(qs)} community medicine questions to {path}.")
    for _, topic, _, _ in TOPICS:
        print(f"- {topic}: 10 questions")


if __name__ == "__main__":
    main()
