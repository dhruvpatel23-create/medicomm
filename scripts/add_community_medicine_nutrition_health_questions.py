import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Nutrition and Health"
CHAPTER_ORDER = 8
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
    ("nutrition-concepts", "Nutrients, Balanced Diet and Nutritional Assessment", 1, [
        q("A balanced diet is one that provides all nutrients in proper amount and what?", "Correct proportion", ["Only excess calories", "Only protein", "Only vitamins without energy"], "A balanced diet supplies energy and nutrients in appropriate amounts and proportions."),
        q("The major source of energy in most Indian diets is which nutrient?", "Carbohydrate", ["Vitamin C", "Iron", "Calcium"], "Cereals and carbohydrates provide much of the energy in typical Indian diets."),
        q("Dietary proteins are especially important for growth and what?", "Tissue repair", ["Only vision", "Only blood clotting", "Only tooth colour"], "Proteins support growth, repair, enzymes and many body functions."),
        q("A 2-year-old has low weight-for-age on growth chart. Which assessment is being used?", "Anthropometry", ["Serology only", "Radiography", "Vital registration"], "Weight-for-age is an anthropometric nutritional assessment measure.", True),
        q("Body mass index is calculated from weight divided by what?", "Height squared", ["Age", "Waist only", "Pulse rate"], "BMI = weight in kg divided by height in metres squared."),
        q("Mid-upper arm circumference is commonly used for screening which condition in young children?", "Acute malnutrition", ["Hypertension", "Cataract", "Hearing loss"], "MUAC is a simple field measure for acute malnutrition."),
        q("Diet survey by 24-hour recall mainly estimates what?", "Recent food intake", ["Lifetime genetic risk", "Vector density", "Water hardness"], "A 24-hour recall records foods consumed during the previous day."),
        q("A child with bilateral pitting oedema and severe wasting should be classified as having what?", "Severe acute malnutrition", ["Normal nutrition", "Overweight", "Mild anaemia only"], "Oedema and severe wasting are signs of severe acute malnutrition.", True),
        q("Recommended dietary allowances are designed to meet nutrient needs of which group?", "Nearly all healthy persons in a category", ["Only sick persons", "Only athletes", "Only newborns"], "RDA covers requirements of almost all healthy individuals in a defined group."),
        q("A pregnant woman receives diet counselling to increase protein, iron and folate intake. Which public health goal is being supported?", "Maternal and fetal nutrition", ["Vector control", "Rabies prevention", "Cancer registry"], "Maternal nutrition affects pregnancy outcome and fetal growth.", True),
    ]),
    ("protein-energy-malnutrition", "Protein Energy Malnutrition and Childhood Undernutrition", 2, [
        q("Protein energy malnutrition is most common in which vulnerable group?", "Young children", ["Healthy adult men only", "Elderly athletes only", "All newborns with normal weight"], "PEM is especially important in infants and preschool children."),
        q("Marasmus is characterized mainly by severe wasting and what?", "Absence of oedema", ["Marked oedema always", "Hypertension", "Jaundice always"], "Marasmus presents with severe wasting without nutritional oedema."),
        q("Kwashiorkor is characterized prominently by what?", "Bilateral pitting oedema", ["High BMI", "No growth failure", "Only night blindness"], "Nutritional oedema is characteristic of kwashiorkor."),
        q("A child with visible severe wasting but no oedema is most consistent with which condition?", "Marasmus", ["Obesity", "Scurvy", "Rickets only"], "Severe wasting without oedema suggests marasmus.", True),
        q("Growth faltering is best detected by plotting serial measurements on what?", "Growth chart", ["Weather chart", "Family pedigree only", "Blood group table"], "Growth charts reveal deviations from expected growth."),
        q("The immediate causes of childhood undernutrition include inadequate diet and what?", "Disease", ["High literacy", "Excess immunization", "Safe sanitation always"], "Undernutrition results from inadequate intake and infections, shaped by underlying factors."),
        q("Severe acute malnutrition management first requires checking for danger signs and what?", "Medical complications", ["Eye colour", "Caste", "School grade"], "SAM care begins with assessment for complications needing facility-based treatment."),
        q("A severely wasted child is lethargic and hypothermic. What is the priority?", "Urgent facility-based management", ["Routine home advice only", "Delay feeding for 1 week", "Only deworming"], "SAM with complications needs urgent inpatient protocol-based care.", True),
        q("Exclusive breastfeeding helps prevent undernutrition partly by reducing which problem?", "Infections and unsafe feeding exposure", ["All genetic disorders", "All congenital anomalies", "All injuries"], "Breastfeeding improves nutrition and protects against infections."),
        q("A community programme combines growth monitoring, supplementary feeding and infection control. Which condition is being addressed?", "Childhood undernutrition", ["Rabies", "Hypertension only", "Cataract"], "Integrated nutrition and health measures reduce undernutrition.", True),
    ]),
    ("micronutrient-deficiencies", "Micronutrient Deficiencies and Public Health Control", 3, [
        q("Iron deficiency commonly causes which public health problem?", "Anaemia", ["Night blindness only", "Goitre only", "Dental fluorosis"], "Iron deficiency is a leading cause of nutritional anaemia."),
        q("Vitamin A deficiency primarily affects which organ system?", "Eye", ["Kidney only", "Heart valves", "Middle ear"], "Vitamin A deficiency causes xerophthalmia and night blindness."),
        q("Iodine deficiency in pregnancy can cause impaired development of which fetal system?", "Brain", ["Gall bladder", "Appendix", "Skin hair only"], "Iodine is essential for thyroid hormone and brain development."),
        q("A preschool child has Bitot spots and night blindness. Which deficiency is most likely?", "Vitamin A deficiency", ["Iron deficiency", "Iodine deficiency", "Fluoride excess"], "Bitot spots and night blindness are signs of vitamin A deficiency.", True),
        q("Universal salt iodization prevents which disorder group?", "Iodine deficiency disorders", ["Protein energy malnutrition only", "Scurvy only", "Beriberi only"], "Iodized salt is the main population strategy for iodine deficiency prevention."),
        q("Fluorosis is caused by excess intake of which element?", "Fluoride", ["Iron", "Iodine", "Zinc"], "High fluoride exposure can cause dental and skeletal fluorosis."),
        q("Vitamin D deficiency in children causes which condition?", "Rickets", ["Pellagra", "Scurvy", "Beriberi"], "Vitamin D deficiency impairs bone mineralization and causes rickets."),
        q("A school survey finds many adolescent girls with pallor and low haemoglobin. Which intervention is most relevant?", "Iron-folic acid supplementation", ["Rabies vaccine", "BCG revaccination", "Vector fogging"], "Adolescent anaemia control includes IFA supplementation and nutrition measures.", True),
        q("Niacin deficiency classically causes dermatitis, diarrhoea and what?", "Dementia", ["Diplopia", "Deafness", "Diabetes"], "Pellagra is described by the three Ds: dermatitis, diarrhoea and dementia."),
        q("A child with bowed legs, delayed milestones and poor sunlight exposure likely has deficiency of which vitamin?", "Vitamin D", ["Vitamin B12", "Vitamin K only", "Vitamin C only"], "Rickets from vitamin D deficiency presents with bone deformities.", True),
    ]),
    ("nutrition-programmes-food-safety", "Nutrition Programmes, Food Safety and Diet-Related Disorders", 4, [
        q("Supplementary nutrition under child development services primarily targets young children and which group?", "Pregnant and lactating women", ["Only adult men", "Only industrial workers", "Only police staff"], "ICDS-type services focus on children, pregnant women and lactating mothers."),
        q("Mid-day meal programme supports school children by improving nutrition and what?", "School attendance", ["Mosquito control", "Hospital admission", "Death certification"], "School meals improve nutrition and encourage attendance."),
        q("Food fortification means adding what to food?", "Micronutrients", ["Pathogens", "Insecticides", "Excess salt only"], "Fortification increases content of essential micronutrients in commonly eaten foods."),
        q("A village anganwadi provides supplementary food, growth monitoring and nutrition education. Which service platform is this?", "Integrated child development services", ["Rabies clinic", "TB microscopy centre", "Blood bank"], "Anganwadi services deliver child nutrition, preschool education and health linkage.", True),
        q("Food adulteration is a public health concern because it may reduce quality and cause what?", "Health hazards", ["Improved nutrition always", "Guaranteed sterility", "Better digestion always"], "Adulterants can be toxic or reduce food quality."),
        q("Food poisoning prevention depends strongly on safe food handling and what?", "Proper storage and cooking", ["Longer queues", "More colouring agents", "No hand washing"], "Food hygiene prevents microbial contamination and toxin formation."),
        q("Obesity is defined as excess body fat that increases risk of what?", "Morbidity", ["All infections disappearing", "Better immunity always", "Zero mortality"], "Obesity raises risk of diabetes, hypertension, CVD and other conditions."),
        q("An adult with BMI 31 kg/m2 and central obesity is counselled on diet and activity. Which condition is being addressed?", "Obesity", ["Marasmus", "Kwashiorkor", "Scurvy"], "BMI above 30 kg/m2 is obesity in standard adult classification.", True),
        q("Double burden of malnutrition means coexistence of undernutrition and what?", "Overnutrition or diet-related NCDs", ["Only tuberculosis", "Only rabies", "Only malaria"], "Communities may face both deficiencies and obesity/NCD risks."),
        q("After a wedding meal, many guests develop vomiting and diarrhoea within hours. Which public health event is suspected?", "Food poisoning outbreak", ["Vitamin A deficiency", "Goitre epidemic", "Fluorosis only"], "Clustering of acute gastroenteritis after common food exposure suggests food poisoning.", True),
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
                "id": f"community-medicine-nutrition-health-{slug}-{i:02d}",
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
