import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Medicine and Social Sciences"
CHAPTER_ORDER = 9
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
    ("social-medicine-determinants", "Social Medicine and Social Determinants of Health", 1, [
        q("Social medicine primarily studies health in relation to what?", "Social, economic and environmental conditions", ["Only surgical anatomy", "Only drug chemistry", "Only radiological shadows"], "Social medicine links health and disease with social organization and living conditions."),
        q("A social determinant of health is best described as what?", "Condition in which people are born, grow, live, work and age", ["Only a bacterial toxin", "Only a genetic mutation", "Only a laboratory reagent"], "Social determinants are upstream conditions shaping health opportunities and risks."),
        q("Poverty affects health mainly by influencing nutrition, housing, education and what?", "Access to health care", ["Blood group", "Eye colour", "Height of hospital building"], "Poverty affects multiple determinants including care access."),
        q("A child repeatedly develops diarrhoea because the family lacks safe water and sanitation. Which determinant is most important?", "Environmental and socioeconomic determinant", ["ABO incompatibility", "Drug allergy only", "Random genetic drift"], "Unsafe living conditions are social/environmental determinants of disease.", True),
        q("Health inequity refers to health differences that are avoidable and what?", "Unfair", ["Always genetic", "Always beneficial", "Only seasonal"], "Inequities are unjust and preventable differences between groups."),
        q("Social gradient in health means health generally improves with increasing what?", "Socioeconomic position", ["Mosquito density", "Hospital queue length", "Rainfall only"], "Many health outcomes follow a gradient across social classes."),
        q("Intersectoral coordination in health means collaboration between health sector and what?", "Other development sectors", ["Only one private clinic", "Only pharmacies", "Only laboratories"], "Health outcomes depend on sectors such as education, housing, sanitation and labour."),
        q("A slum improvement project provides safe water, toilets and waste disposal. Which public health approach is this?", "Intersectoral action on determinants", ["Only tertiary care", "Only case fatality calculation", "Only drug trial blinding"], "Improving living conditions requires action beyond clinical services.", True),
        q("Social security measures protect health by reducing which vulnerability?", "Economic hardship during illness or old age", ["Vaccine potency", "Vector density only", "Incubation period"], "Social security reduces health effects of poverty and dependency."),
        q("A widow with no income cannot afford treatment for diabetes. Which public health concern is illustrated?", "Social vulnerability affecting health care access", ["High specificity", "Herd immunity", "Vector competence"], "Economic and social vulnerability can block access and worsen chronic disease.", True),
    ]),
    ("behaviour-culture-health", "Culture, Behaviour and Health", 2, [
        q("Health behaviour refers to actions taken by individuals that affect what?", "Health status", ["Only blood group", "Only climate", "Only census date"], "Health behaviours include actions that promote, protect or harm health."),
        q("Illness behaviour is best described as how people respond when they do what?", "Perceive symptoms or illness", ["Receive a vaccine only", "Enter school", "Count population"], "Illness behaviour includes symptom appraisal and care-seeking."),
        q("Culture influences health by shaping diet, beliefs, customs and what?", "Health-seeking practices", ["Chromosome number", "Enzyme structure only", "Blood pressure cuff size"], "Cultural norms influence perception of illness and use of services."),
        q("A mother delays ORS because diarrhoea is believed to be caused by teething and not illness. What is the barrier?", "Cultural belief affecting care-seeking", ["Vaccine failure", "Laboratory contamination", "High sensitivity"], "Beliefs can delay appropriate care even when services exist.", True),
        q("A taboo against certain foods during pregnancy may increase risk of what?", "Maternal undernutrition", ["Rabies", "Noise-induced deafness", "Lead poisoning only"], "Food taboos can reduce intake of needed nutrients."),
        q("Stigma in disease control is important because it may reduce what?", "Disclosure and treatment seeking", ["Pathogen virulence always", "Vaccine cold chain", "Rainfall"], "Stigma can hide illness and delay diagnosis/treatment."),
        q("Community participation improves health programmes mainly by increasing relevance and what?", "Acceptance", ["Drug resistance", "False positives", "Incubation period"], "Participation increases ownership, trust and uptake."),
        q("A TB patient stops visiting clinic because neighbours shame him. Which social factor affects treatment?", "Stigma", ["Herd immunity", "Randomization", "Lead-time bias"], "Stigma can interrupt adherence and contact tracing.", True),
        q("Behaviour change communication aims to support adoption of what?", "Healthy practices", ["Unsafe injections", "Delayed referral", "Food adulteration"], "BCC uses communication strategies to promote healthier behaviours."),
        q("A village handwashing campaign uses local leaders and repeated demonstrations. Which principle is being used?", "Culturally appropriate behaviour change", ["Only hospital isolation", "Only census enumeration", "Only blinding"], "Messages work better when adapted to local culture and trusted channels.", True),
    ]),
    ("health-education-communication", "Health Education and Communication", 3, [
        q("Health education aims to help people gain knowledge and develop what?", "Healthy attitudes and practices", ["Only drug stock", "Only hospital beds", "Only birth certificates"], "Health education supports informed choices and behaviour change."),
        q("The first step in planning health education is usually to identify what?", "Health problem and target audience", ["Printer colour", "Final exam date", "Hospital profit"], "Planning begins with needs assessment and audience definition."),
        q("Two-way communication is preferred in health education because it allows what?", "Feedback and clarification", ["Only lecturing", "No questions", "Reduced understanding"], "Interactive communication improves understanding and trust."),
        q("An ANM explains ORS preparation and asks the mother to demonstrate it. Which method is being used?", "Demonstration with feedback", ["Mass media only", "Randomization", "Diagnostic confirmation"], "Return demonstration checks skill acquisition.", True),
        q("Mass media is most useful for reaching which audience?", "Large population", ["Only one patient in clinic", "Only ICU staff", "Only laboratory workers"], "Mass media can rapidly spread messages to many people."),
        q("Interpersonal communication is especially useful for what?", "Counselling and individual doubts", ["Only national census", "Only weather forecasting", "Only mortality coding"], "Face-to-face communication helps address personal concerns."),
        q("IEC stands for information, education and what?", "Communication", ["Chemotherapy", "Certification", "Calculation"], "IEC is a standard health promotion approach."),
        q("A family refuses immunization due to fear of fever after vaccine. What should the health worker do?", "Counsel about benefits, minor adverse events and when to seek care", ["Force vaccination without explanation", "Ignore the family forever", "Stop all outreach"], "Respectful counselling can address misconceptions and improve acceptance.", True),
        q("Evaluation of health education should assess whether the intended audience changed knowledge and what?", "Behaviour or practice", ["Blood group", "Rainfall", "Road length only"], "Programme evaluation looks at process, learning and behavioural outcomes."),
        q("After a nutrition session, mothers correctly prepare complementary food at home. What outcome improved?", "Practice", ["Vector density", "Specificity", "Hospital bed ratio"], "Observed correct preparation reflects behaviour/practice change.", True),
    ]),
    ("family-community-social-problems", "Family, Community and Social Problems in Health", 4, [
        q("Family is important in community medicine because it is a basic unit of what?", "Health care and social support", ["Vector breeding only", "Laboratory testing only", "Hospital finance only"], "Family influences care, behaviour, nutrition and support."),
        q("A nuclear family consists mainly of husband, wife and whom?", "Unmarried children", ["All relatives over three generations", "Only neighbours", "Only grandparents"], "Nuclear family includes parents and dependent unmarried children."),
        q("Community diagnosis involves identifying health problems and what?", "Available resources and priorities", ["Only drug brands", "Only hospital paint", "Only weather charts"], "Community diagnosis assesses needs, determinants and resources."),
        q("A health team maps households, water sources and disease clusters before planning intervention. What is this process?", "Community diagnosis", ["Case-control matching", "Drug dispensing only", "Autopsy audit"], "Community diagnosis guides local health planning.", True),
        q("Domestic violence is a public health issue because it affects physical, mental and what?", "Social well-being", ["Only eye colour", "Only blood group", "Only rainfall"], "Violence has broad health and social consequences."),
        q("Substance abuse affects communities by increasing injuries, illness and what?", "Social and family disruption", ["Vaccine potency", "Food fortification", "Herd immunity only"], "Substance misuse harms health, work, family and safety."),
        q("Urbanization may worsen health when it leads to overcrowding and what?", "Poor sanitation", ["Universal clean housing", "Zero pollution", "No migration"], "Rapid unplanned urbanization creates slums and environmental risks."),
        q("A family with alcohol dependence, domestic conflict and school absenteeism needs which approach?", "Multisectoral support with health and social services", ["Only antibiotic course", "Only vector fogging", "Only birth registration"], "Complex social problems require coordinated medical, counselling and social interventions.", True),
        q("Social support protects health mainly by reducing stress and improving what?", "Coping and care-seeking", ["Pathogen mutation", "Water hardness", "Incubation period"], "Support networks influence resilience and access to help."),
        q("An elderly person living alone misses medicines and meals. Which community intervention is most relevant?", "Family/community support and linkage to services", ["Only school health check", "Only rabies vaccination", "Only mosquito larvicide"], "Social isolation in older adults needs community support and service linkage.", True),
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
                "id": f"community-medicine-social-sciences-{slug}-{i:02d}",
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
