import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Health Programmes in India"
CHAPTER_ORDER = 5
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
    ("rmncha-immunization", "RMNCH+A and Universal Immunization Programmes", 1, [
        q("The RMNCH+A strategy covers reproductive, maternal, newborn, child health and which additional group?", "Adolescents", ["Geriatric patients only", "Industrial workers only", "Veterinary staff"], "RMNCH+A integrates services across life stages including adolescents."),
        q("Janani Suraksha Yojana primarily promotes which health behaviour?", "Institutional delivery", ["Home delivery without skilled care", "Avoidance of antenatal care", "Delayed breastfeeding"], "JSY is a safe motherhood intervention promoting institutional delivery."),
        q("A key objective of antenatal care under national programmes is early detection of what?", "High-risk pregnancy", ["Only eye disease", "Only dental caries", "Only rabies exposure"], "ANC screens for maternal and fetal risk and links women to care."),
        q("A pregnant woman with severe anaemia is identified by an ASHA during village follow-up. Which programme area is being served?", "Maternal health under RMNCH+A", ["Vector control only", "Leprosy elimination only", "Food adulteration control"], "Anaemia detection and referral in pregnancy is part of maternal health services.", True),
        q("The Universal Immunization Programme is aimed mainly at preventing what?", "Vaccine-preventable diseases", ["All cancers", "All genetic disorders", "Only occupational injuries"], "UIP protects children and pregnant women from selected vaccine-preventable diseases."),
        q("Cold chain in immunization programmes is maintained to preserve what?", "Vaccine potency", ["Needle sharpness", "Register colour", "Syringe volume only"], "Many vaccines lose potency if not kept at recommended temperature."),
        q("Full immunization coverage is an important indicator for which group?", "Children in the eligible age group", ["Only elderly men", "Only school teachers", "Only animal handlers"], "Immunization coverage measures programme reach among eligible children."),
        q("A health worker finds frozen DPT vaccine in an ice-lined refrigerator. What is the concern?", "Loss of vaccine potency due to freezing", ["Improved potency", "No effect on any vaccine", "Conversion to oral vaccine"], "Freeze-sensitive vaccines can be damaged by freezing.", True),
        q("Vitamin A prophylaxis in child health programmes primarily prevents which condition?", "Nutritional blindness", ["Tuberculosis", "Hypertension", "Rabies"], "Vitamin A prevents xerophthalmia and reduces child morbidity in deficient populations."),
        q("A child missing scheduled vaccines is identified during outreach. What is the best programme action?", "Catch-up immunization according to schedule", ["Restart all vaccines from birth only", "Ignore missed doses", "Give antibiotics instead"], "Dropouts should be brought back through tracking and catch-up immunization.", True),
    ]),
    ("communicable-disease-programmes", "Communicable Disease Control Programmes", 2, [
        q("The National Tuberculosis Elimination Programme focuses on diagnosis and treatment using which public health principle?", "Early case detection and complete treatment", ["Only isolation for life", "No notification", "Treatment without diagnosis"], "TB control depends on detecting infectious cases and ensuring effective treatment."),
        q("Directly observed treatment in TB control is intended mainly to improve what?", "Treatment adherence", ["Mosquito control", "Birth registration", "Water chlorination only"], "Observation/support helps patients complete therapy."),
        q("The National Vector Borne Disease Control Programme covers diseases transmitted mainly by what?", "Vectors", ["Food additives", "Genetic mutations", "Road traffic"], "NVBDCP addresses malaria, dengue, chikungunya, JE, kala-azar and filariasis."),
        q("A fever case in a malaria-endemic village is tested with RDT and treated based on result. Which programme activity is this?", "Early diagnosis and complete treatment", ["Cancer screening", "School health only", "Blindness control"], "Malaria control emphasizes prompt diagnosis and complete treatment.", True),
        q("Integrated Disease Surveillance Programme is designed primarily for what?", "Early detection and response to outbreaks", ["Only hospital billing", "Only surgery scheduling", "Only drug procurement"], "IDSP strengthens surveillance for epidemic-prone diseases."),
        q("Leprosy control relies on early diagnosis and which treatment strategy?", "Multidrug therapy", ["Single-dose vitamin A only", "BCG revaccination only", "ORS only"], "MDT cures leprosy and reduces transmission and disability."),
        q("HIV/AIDS control programmes emphasize prevention, testing, counselling and what?", "Antiretroviral therapy services", ["Only vector control", "Only cataract surgery", "Only iodized salt"], "HIV programmes combine prevention with counselling/testing and ART."),
        q("A migrant worker tests HIV positive and is linked to counselling plus ART centre. Which programme component is being used?", "Care, support and treatment services", ["Oral rehydration programme", "Blindness control", "Rabies control only"], "Linkage to ART is a core HIV programme service.", True),
        q("Elimination of lymphatic filariasis uses mass drug administration mainly to reduce what?", "Microfilaria reservoir in the community", ["Road accidents", "Protein deficiency", "Hypertension"], "MDA reduces parasite load and interrupts transmission."),
        q("A district reports clustering of acute diarrhoeal cases through IDSP. What should follow?", "Rapid outbreak investigation and control measures", ["Wait for annual report only", "Stop all immunization", "Declare eradication"], "Surveillance signals should trigger field investigation and response.", True),
    ]),
    ("ncd-nutrition-health-promotion", "NCD, Nutrition and Health Promotion Programmes", 3, [
        q("NPCDCS addresses prevention and control of diabetes, cardiovascular disease, stroke and which major group?", "Cancer", ["Measles only", "Cholera only", "Rabies only"], "NPCDCS covers major NCDs including cancer, diabetes, CVD and stroke."),
        q("Opportunistic screening under NCD programmes commonly includes blood pressure and what?", "Blood glucose", ["Sputum AFB only", "Dog bite category", "Mosquito species"], "NCD screening commonly includes hypertension and diabetes risk detection."),
        q("A major goal of tobacco control programme is reduction of exposure to what?", "Tobacco use and second-hand smoke", ["Iodized salt", "ORS", "Vitamin A"], "Tobacco control targets active and passive tobacco exposure."),
        q("A 42-year-old man at a PHC is screened for BP, diabetes and oral cancer risk. Which programme area is this?", "NCD screening and prevention", ["AFP surveillance", "Pulse polio booth", "Kala-azar vector control"], "Adult screening for common NCDs is part of NCD programme activities.", True),
        q("The National Health Programme for control of iodine deficiency disorders promotes use of what?", "Iodized salt", ["Unboiled milk", "High-sugar diet", "Raw water"], "Universal salt iodization prevents iodine deficiency disorders."),
        q("Anaemia control programmes commonly use iron-folic acid supplementation and what?", "Dietary counselling and deworming where indicated", ["Rabies immunoglobulin", "BCG scar check", "Vector density mapping only"], "Anaemia control combines supplementation, diet, deworming and maternal-child interventions."),
        q("National programme for prevention and control of fluorosis focuses on safe water and what?", "Early diagnosis and management", ["Mass antimalarial treatment", "Only vaccination", "TB notification"], "Fluorosis control includes surveillance, safe water and clinical management."),
        q("A school health visit gives weekly iron-folic acid tablets to adolescents. Which public health problem is being targeted?", "Anaemia", ["Trachoma only", "Rabies", "Dengue"], "WIFS targets adolescent anaemia using weekly iron-folic acid supplementation.", True),
        q("Health promotion differs from disease control because it aims to enable people to do what?", "Increase control over determinants of health", ["Avoid all services", "Receive only curative care", "Stop community participation"], "Health promotion strengthens capacity and environments for health."),
        q("A village campaign combines diet advice, exercise groups and tobacco cessation counselling. What is the main programme approach?", "Lifestyle risk reduction", ["Only secondary TB treatment", "Only outbreak response", "Only disability certification"], "Integrated health promotion reduces shared NCD risk factors.", True),
    ]),
    ("national-health-missions-support", "National Health Mission and Supportive Health Programmes", 4, [
        q("The National Health Mission aims mainly to strengthen which level of care?", "Primary and public health systems", ["Only private tertiary hospitals", "Only overseas care", "Only mortuary services"], "NHM strengthens accessible, affordable and quality public health services."),
        q("ASHA is primarily a link between the community and which system?", "Public health services", ["Only police department", "Only veterinary clinics", "Only pharmacies"], "ASHA acts as a community-level health activist and link worker."),
        q("Village Health Sanitation and Nutrition Day is intended to deliver which type of services?", "Outreach health, nutrition and sanitation services", ["Only surgery", "Only post-mortem", "Only specialist ICU care"], "VHSND provides community outreach for maternal-child health, nutrition and sanitation."),
        q("An ASHA motivates a pregnant woman for ANC, institutional delivery and immunization. What is her role here?", "Community mobilization and linkage to services", ["Laboratory confirmation only", "Hospital administration only", "Drug manufacturing"], "ASHA supports awareness, mobilization and service linkage.", True),
        q("Ayushman Bharat Health and Wellness Centres emphasize which approach?", "Comprehensive primary health care", ["Only inpatient surgery", "Only international travel medicine", "Only autopsy services"], "HWCs expand primary care beyond selective services."),
        q("The National Programme for Control of Blindness focuses strongly on control of which avoidable cause?", "Cataract", ["Rabies", "Dengue", "Typhoid"], "Cataract has been a major avoidable cause of blindness targeted by the programme."),
        q("National Mental Health Programme aims to integrate mental health care with which level?", "General health care", ["Only prison services", "Only radiology units", "Only blood banks"], "The programme promotes accessible mental healthcare through general health services."),
        q("A district camp identifies cataract patients and links them for surgery. Which programme is this?", "National Programme for Control of Blindness", ["NTEP", "NVBDCP", "IDSP"], "Cataract detection and surgical linkage is a blindness control activity.", True),
        q("Programme monitoring commonly uses indicators to assess coverage, quality and what?", "Impact", ["Weather only", "Hospital paint colour", "Staff handwriting"], "Monitoring and evaluation assess inputs, process, outputs, outcomes and impact."),
        q("If a PHC has low immunization coverage despite vaccine supply, which programme function needs strengthening?", "Microplanning and community mobilization", ["Autopsy reporting", "Cancer chemotherapy", "Port quarantine only"], "Low coverage often requires better planning, tracking, outreach and mobilization.", True),
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
                "id": f"community-medicine-health-programmes-{slug}-{i:02d}",
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
