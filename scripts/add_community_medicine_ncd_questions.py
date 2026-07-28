import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Epidemiology of Chronic Non-Communicable Diseases and Conditions"
CHAPTER_ORDER = 4
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
    ("ncd-concepts-risk-factors", "Concepts, Risk Factors and Prevention of NCDs", 1, [
        q("Non-communicable diseases are generally characterized by which feature?", "Long duration and slow progression", ["Short incubation only", "Transmission by vectors", "Always cured by antibiotics"], "NCDs are usually chronic conditions with prolonged course."),
        q("The epidemiological transition is marked by a shift from infectious diseases to what?", "Chronic non-communicable diseases", ["Only neonatal tetanus", "Only parasitic infestations", "No disease burden"], "As societies develop, chronic diseases become a larger share of morbidity and mortality."),
        q("A common modifiable risk factor for many NCDs is what?", "Tobacco use", ["Blood group", "Eye colour", "Birth order only"], "Tobacco is a major shared risk factor for cardiovascular disease, cancer and chronic lung disease."),
        q("A 45-year-old sedentary smoker with central obesity attends a health camp. Which prevention level is counselling for lifestyle change?", "Primary prevention", ["Secondary prevention only", "Tertiary prevention only", "Primordial diagnosis"], "Risk factor reduction before disease onset is primary prevention.", True),
        q("Primordial prevention aims mainly to prevent what?", "Emergence of risk factors", ["Complications after stroke", "False positive tests", "Death certification"], "Primordial prevention stops social and environmental patterns that create risk factors."),
        q("Population strategy for NCD prevention aims to shift what?", "Risk distribution of the whole community", ["Only treatment of severe cases", "Only hospital admissions", "Only genetic testing"], "Population strategy reduces average risk across the population."),
        q("High-risk strategy in NCD prevention focuses on whom?", "Individuals with increased risk", ["All newborns only", "Only dead persons", "Only infectious cases"], "High-risk strategy identifies and manages people at elevated risk."),
        q("A city bans smoking in public places. Which prevention approach does this best represent?", "Population strategy", ["Only case treatment", "Clinical trial blinding", "Passive surveillance"], "Policy measures reduce exposure across the community.", True),
        q("The main behavioural risk factors for NCDs include unhealthy diet, physical inactivity, tobacco and what?", "Harmful use of alcohol", ["BCG scar", "Mosquito density", "Unsafe water only"], "WHO highlights tobacco, alcohol, diet and physical inactivity as major shared risk factors."),
        q("A worker with normal BP begins regular exercise and salt reduction to avoid hypertension. This is best classified as what?", "Primary prevention", ["Disability limitation", "Rehabilitation", "Terminal care"], "Healthy behaviour before disease development is primary prevention.", True),
    ]),
    ("cardiovascular-hypertension-diabetes", "Cardiovascular Diseases, Hypertension and Diabetes", 2, [
        q("Hypertension is a major risk factor for which event?", "Stroke", ["Rabies", "Measles", "Cholera"], "Raised blood pressure strongly increases stroke and cardiovascular risk."),
        q("Coronary heart disease is most closely linked with which pathological process?", "Atherosclerosis", ["Demyelination", "Haemolysis", "Larval migration"], "Atherosclerosis underlies most coronary artery disease."),
        q("A major modifiable dietary risk factor for hypertension is high intake of what?", "Salt", ["Vitamin C", "Iodine only", "Folate only"], "Excess sodium intake contributes to raised blood pressure."),
        q("A 52-year-old man with BP 166/100 mmHg is detected at screening. What is the next public health step?", "Confirm diagnosis and initiate risk-based management", ["Ignore because asymptomatic", "Give rabies vaccine", "Declare epidemic"], "Screening positives need confirmation and management to reduce complications.", True),
        q("Diabetes mellitus increases risk of blindness mainly through which complication?", "Diabetic retinopathy", ["Trachoma only", "Cataract from measles", "Night blindness only"], "Retinopathy is a major microvascular complication of diabetes."),
        q("Central obesity is commonly assessed in community programmes using which measure?", "Waist circumference", ["Arm span only", "Head circumference", "Shoe size"], "Waist circumference reflects abdominal adiposity and cardiometabolic risk."),
        q("The metabolic syndrome includes central obesity, hypertension, dyslipidaemia and what?", "Impaired glucose regulation", ["Acute diarrhoea", "Rabies exposure", "Anaemia only"], "Metabolic syndrome clusters cardiometabolic risk factors."),
        q("A diabetic patient with loss of foot sensation needs regular foot care to prevent which outcome?", "Diabetic foot ulcer", ["Measles rash", "Hydatid cyst", "Diphtheria membrane"], "Neuropathy and vascular disease predispose to diabetic foot ulcers.", True),
        q("Primary prevention of coronary heart disease includes tobacco cessation and what?", "Healthy diet and physical activity", ["Long-term bed rest", "Avoiding all vaccines", "Increasing trans fats"], "Lifestyle modification reduces CHD risk."),
        q("A community programme measures BP and blood glucose in adults over 30 years. Which prevention level is this?", "Secondary prevention", ["Primordial prevention only", "Rehabilitation only", "Palliative care only"], "Screening to detect disease early is secondary prevention.", True),
    ]),
    ("cancer", "Cancer Epidemiology and Prevention", 3, [
        q("Cancer burden in a population is commonly described using incidence and which other measure?", "Mortality", ["Vector density", "Attack rate only", "Incubation period"], "Cancer epidemiology tracks incidence, mortality and survival."),
        q("Tobacco use is strongly associated with cancer of which site?", "Lung", ["Appendix only", "Spleen", "Gall bladder only"], "Smoking is the leading preventable cause of lung cancer."),
        q("Human papillomavirus infection is causally linked with which cancer?", "Cervical cancer", ["Typhoid carrier state", "Hydatid disease", "Kala-azar"], "High-risk HPV types cause cervical cancer."),
        q("A woman undergoes VIA/Pap screening for cervical cancer while asymptomatic. Which prevention level is this?", "Secondary prevention", ["Primary prevention only", "Tertiary prevention only", "Rehabilitation"], "Cancer screening detects preclinical disease or precancerous lesions.", True),
        q("Hepatitis B vaccination helps prevent which cancer?", "Hepatocellular carcinoma", ["Cervical cancer", "Skin melanoma only", "Oral cancer only"], "HBV immunization reduces chronic infection and liver cancer risk."),
        q("Oral cancer prevention in India strongly emphasizes avoidance of tobacco and what?", "Areca nut/betel quid use", ["Milk boiling only", "Mosquito nets", "Iodized salt"], "Smokeless tobacco and areca nut are major oral cancer risks."),
        q("Warning signals of cancer include non-healing ulcer and what?", "Unusual bleeding or lump", ["Transient common cold", "Normal appetite", "Immediate wound healing"], "Persistent lumps, bleeding and non-healing ulcers need evaluation."),
        q("A man with a persistent oral ulcer and history of chewing tobacco should be referred to rule out which condition?", "Oral cancer", ["Dengue", "Filariasis", "Cholera"], "Persistent oral lesions in tobacco users are suspicious for malignancy.", True),
        q("Population-based cancer registry is important because it measures what?", "Cancer occurrence in a defined population", ["Only hospital bed occupancy", "Mosquito breeding", "Water chlorination"], "Registries provide incidence and survival data for planning."),
        q("A screening test for cancer is useful only if early detection is followed by what?", "Effective diagnostic confirmation and treatment", ["No referral", "Only reassurance", "Delay until symptoms are severe"], "Screening programmes require diagnosis and treatment pathways.", True),
    ]),
    ("chronic-respiratory-mental-neurological", "Chronic Respiratory, Mental and Neurological Conditions", 4, [
        q("Chronic obstructive pulmonary disease is most strongly associated with which exposure?", "Tobacco smoke", ["Clean drinking water", "BCG vaccine", "Vitamin C intake"], "Smoking is the major preventable COPD risk factor."),
        q("Indoor air pollution from biomass fuel particularly increases risk of what?", "Chronic respiratory disease", ["Poliomyelitis", "Rabies", "Scabies only"], "Biomass smoke exposure contributes to chronic airway disease."),
        q("Asthma is characterized physiologically by what?", "Variable airflow obstruction", ["Permanent complete airway closure in all cases", "Only restrictive lung disease", "No inflammatory component"], "Asthma causes variable, often reversible airflow limitation."),
        q("A woman cooking daily with biomass fuel in a poorly ventilated kitchen develops chronic cough and breathlessness. Which risk factor is important?", "Indoor air pollution", ["Hard water", "Iodine deficiency", "Dog bite"], "Household smoke exposure is a major chronic respiratory risk, especially in poorly ventilated homes.", True),
        q("Depression as a public health problem is important because it contributes strongly to what?", "Disability burden", ["Only mosquito breeding", "Only infant mortality from diarrhoea", "Water hardness"], "Mental disorders contribute substantially to years lived with disability."),
        q("Suicide prevention programmes commonly focus on early identification of depression and what?", "Crisis support and restriction of lethal means", ["Increasing pesticide access", "Avoiding counselling", "No follow-up"], "Suicide prevention uses mental health care, crisis intervention and means restriction."),
        q("Epilepsy is a chronic neurological condition characterized by recurrent what?", "Seizures", ["Fever only", "Diarrhoea", "Skin ulcers only"], "Epilepsy involves recurrent unprovoked seizures."),
        q("A young adult with depression expresses suicidal intent. What is the immediate priority?", "Ensure safety and urgent mental health assessment", ["Send home alone", "Only advise vitamins", "Wait for annual survey"], "Suicidal ideation requires immediate safety planning and professional assessment.", True),
        q("Stroke disability can be reduced after acute care by which public health measure?", "Rehabilitation", ["Stopping physiotherapy", "Avoiding BP control", "No family education"], "Rehabilitation limits disability and improves function after stroke."),
        q("A stroke survivor receives physiotherapy and speech therapy to regain function. Which prevention level is this?", "Tertiary prevention", ["Primary prevention", "Primordial prevention", "Specific protection only"], "Rehabilitation after disease is tertiary prevention.", True),
    ]),
    ("injuries-disabilities-obesity", "Injuries, Disabilities, Obesity and Other Chronic Conditions", 5, [
        q("Road traffic injuries are best classified as which public health problem?", "Non-communicable condition/injury burden", ["Vector-borne disease", "Water-borne infection", "Zoonosis only"], "Injuries are included in the broader NCD and chronic condition burden."),
        q("The Haddon matrix is used mainly for prevention of what?", "Injuries", ["Measles", "Typhoid", "Leprosy"], "Haddon matrix organizes injury prevention by host, agent, environment and time phase."),
        q("Helmet use for two-wheeler riders is an example of what?", "Specific protection", ["Case finding only", "Rehabilitation only", "Chemoprophylaxis for malaria"], "Helmets protect against head injury before an event."),
        q("A city enforces seat-belt laws and speed control to reduce deaths. Which strategy is being used?", "Injury prevention through environmental and legislative measures", ["Treatment of cholera", "Vector control only", "Cancer chemotherapy"], "Road safety requires policy, enforcement and environmental measures.", True),
        q("Body mass index is calculated using weight and what?", "Height squared", ["Waist alone", "Age cubed", "Pulse rate"], "BMI = weight in kg divided by height in metres squared."),
        q("Obesity increases risk of diabetes, hypertension and which other condition?", "Coronary heart disease", ["Rabies", "Diphtheria", "Scabies"], "Obesity is a cardiometabolic risk factor."),
        q("Disability limitation aims to prevent what?", "Progression from impairment to handicap/disability", ["Initial exposure to every risk factor", "All infections only", "Birth registration"], "Disability limitation reduces consequences of established disease or impairment."),
        q("An obese adult with knee pain is counselled for weight reduction to prevent progression of osteoarthritis. Which risk factor is being addressed?", "Excess body weight", ["Mosquito density", "Unsafe injection only", "Lack of BCG"], "Obesity increases mechanical load and chronic disease risk.", True),
        q("Community-based rehabilitation emphasizes care and support at which level?", "Within the community", ["Only tertiary hospital ICU", "Only mortuary", "Only laboratory"], "CBR integrates rehabilitation into community and family settings."),
        q("A patient with permanent limb weakness receives assistive devices and vocational support. This is best described as what?", "Rehabilitation", ["Primordial prevention", "Mass chemoprophylaxis", "Outbreak investigation"], "Rehabilitation restores function and social participation after disability.", True),
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
                "id": f"community-medicine-ncd-{slug}-{i:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": order,
                "options": opts,
                "answerIndex": opts.index(ans),
                "answer": ans,
            })
    return out


def validate(qs):
    if len(qs) != 50:
        raise ValueError(f"Expected 50, got {len(qs)}")
    if len({q["id"] for q in qs}) != 50:
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
