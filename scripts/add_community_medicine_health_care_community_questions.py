import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Health Care of the Community"
CHAPTER_ORDER = 19
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
    ("primary-health-care", "Primary Health Care", 1, [
        q("Primary health care is essential health care made universally accessible to individuals and families through what?", "Their full participation", ["Tertiary hospitals only", "Private insurance only", "Urban specialists only"], "Primary health care emphasizes universal access, community participation and appropriate technology."),
        q("The Alma-Ata declaration is most closely associated with which concept?", "Primary health care", ["Hospital accreditation only", "Genetic counselling", "Incineration"], "Alma-Ata placed primary health care at the centre of health for all."),
        q("The principles of primary health care include equitable distribution, community participation, intersectoral coordination and what?", "Appropriate technology", ["Luxury technology only", "No referral", "Only curative care"], "Primary health care should be equitable, participatory, intersectoral and practical."),
        q("A village health plan is prepared with panchayat members, ASHAs and local families. Which PHC principle is shown?", "Community participation", ["Blinding", "Randomization", "Autoclaving"], "Community participation involves people in decisions affecting their health.", True),
        q("Equitable distribution in health care means services should be available according to what?", "Need", ["Income only", "Political influence", "Distance from capital only"], "Equity prioritizes access for those with greater health need."),
        q("Appropriate technology in primary health care should be scientifically sound, acceptable and what?", "Affordable", ["Complex always", "Imported only", "Unavailable locally"], "Appropriate technology fits local needs, resources and culture."),
        q("Intersectoral coordination is needed because health depends on sectors such as education, agriculture and what?", "Water and sanitation", ["Only radiology", "Only pharmacy sales", "Only laboratory staining"], "Many health determinants lie outside medical services."),
        q("A diarrhoea control plan combines ORS, safe water, sanitation and nutrition education. Which PHC principle is highlighted?", "Intersectoral coordination", ["Single-drug therapy only", "No prevention", "Hospital-only care"], "Diarrhoea control requires coordinated action beyond treatment alone.", True),
        q("Primary health care gives emphasis to prevention, promotion, treatment and what?", "Rehabilitation", ["Only certification", "Only compensation", "Only research"], "PHC includes promotive, preventive, curative and rehabilitative care."),
        q("A remote hamlet receives regular antenatal visits, immunization and basic treatment near home. Which goal is being served?", "Accessible primary health care", ["Only tertiary care", "Medical tourism", "Forensic medicine"], "Care close to communities improves access and coverage.", True),
    ]),
    ("levels-referral", "Levels of Health Care and Referral", 2, [
        q("Health care is commonly organized into primary, secondary and what level?", "Tertiary level", ["Quaternary statistics", "Domestic level only", "Unplanned level"], "The three broad care levels are primary, secondary and tertiary."),
        q("Primary level care is usually the first contact between the community and what?", "Health system", ["Medical college only", "Supreme court", "Pharmaceutical industry"], "Primary care is the first level of contact for essential health services."),
        q("Secondary care generally provides more specialized services through facilities such as what?", "District hospitals", ["Only home kitchens", "Only schools", "Only census offices"], "Secondary care includes referral hospitals with specialist services."),
        q("Tertiary care is characterized by highly specialized services and what?", "Advanced diagnostic and treatment facilities", ["Only village outreach", "Only family folders", "Only health talks"], "Tertiary centres provide advanced specialist and super-specialist care."),
        q("A PHC refers a woman with obstructed labour to a first referral unit. What is this process called?", "Referral", ["Screening", "Randomization", "Notification"], "Referral transfers patients needing higher-level care to appropriate facilities.", True),
        q("An effective referral system requires communication, transport and what?", "Feedback to the referring facility", ["No records", "Only patient memory", "No follow-up"], "Referral feedback supports continuity of care."),
        q("A subcentre is closest to the community and usually serves as the most peripheral unit for what?", "Primary health services", ["Tertiary surgery", "Medical college teaching", "Advanced radiotherapy"], "Subcentres deliver basic outreach and primary health services."),
        q("A child with severe pneumonia is identified by an ASHA and sent urgently to a higher facility. Which function is shown?", "Early recognition and referral", ["Vital registration only", "Water testing", "Census enumeration"], "Community-level workers identify danger signs and link patients to care.", True),
        q("Continuity of care means patients receive coordinated care over time across different what?", "Levels of the health system", ["Weather zones", "Blood groups", "Exam centres"], "Continuity prevents gaps when patients move between providers or facilities."),
        q("A diabetic patient is diagnosed at a district hospital and followed monthly at a nearby PHC. Which care principle is shown?", "Continuity and linkage of care", ["No referral", "Only emergency care", "Duplicate treatment"], "Linked care allows specialist input with local follow-up.", True),
    ]),
    ("health-infrastructure-workers", "Health Infrastructure and Workers", 3, [
        q("A subcentre in rural health services is commonly staffed by ANMs and what other frontline worker?", "Male health worker", ["Radiotherapy physicist", "Cardiac surgeon", "Forensic expert"], "Subcentre staff provide basic preventive, promotive and selected curative services."),
        q("A primary health centre functions as a referral unit for subcentres and provides integrated what?", "Primary health care", ["Only super-speciality care", "Only medical tourism", "Only private insurance"], "PHCs support subcentres and provide first-level medical care."),
        q("A community health centre usually serves as a higher referral centre with specialist services for how many PHCs?", "Several PHCs", ["No PHCs", "Only one household", "Only one school"], "CHCs are referral units above PHCs with specialist care."),
        q("ASHAs mainly act as community-level link workers between households and what?", "Health services", ["Banks only", "Police stations only", "Pharmaceutical factories"], "ASHAs mobilize communities and link families to health care."),
        q("An ASHA motivates a pregnant woman for ANC, institutional delivery and immunization. What role is she performing?", "Community mobilization and service linkage", ["Surgical care", "Laboratory diagnosis only", "Drug manufacturing"], "ASHAs support awareness, mobilization and access to services.", True),
        q("Anganwadi workers under ICDS mainly support supplementary nutrition, preschool education and what?", "Growth monitoring", ["Advanced surgery", "Blood banking", "Radiotherapy"], "Anganwadi centres provide nutrition and early childhood services."),
        q("The village health sanitation and nutrition committee promotes local planning and what?", "Community participation", ["Tertiary surgery", "Drug licensing", "Medical certification only"], "VHSNCs support decentralized health action at village level."),
        q("A malnourished child is weighed monthly at an anganwadi and counselled for feeding. Which service is shown?", "Growth monitoring and nutrition counselling", ["Emergency obstetric surgery", "Cancer radiotherapy", "Occupational compensation"], "Anganwadi services include child growth monitoring and nutrition education.", True),
        q("Multipurpose health workers are important because they deliver several programmes through what approach?", "Integrated service delivery", ["Single disease only", "No home visits", "Only inpatient care"], "Multipurpose workers provide multiple primary health services in the field."),
        q("A health worker provides immunization, antenatal follow-up, malaria slides and health education during field visits. Which concept fits?", "Multipurpose worker approach", ["Tertiary specialization", "No outreach", "Private-only care"], "Field workers commonly deliver integrated services for several programmes.", True),
    ]),
    ("community-diagnosis-services", "Community Diagnosis and Services", 4, [
        q("Community diagnosis means identifying and quantifying health problems and resources of what?", "A defined community", ["Only one hospital ward", "Only a drug list", "Only one laboratory"], "Community diagnosis studies health needs and available resources in a population."),
        q("Community diagnosis helps plan services according to local needs and what?", "Priorities", ["Doctor preference only", "Drug colour", "Building height"], "It guides priority setting and resource allocation."),
        q("Important components of community diagnosis include demography, morbidity, mortality and what?", "Environmental conditions", ["Only handwriting", "Only staff uniforms", "Only pharmacy profit"], "Community diagnosis covers population, health status, services and environment."),
        q("A PHC team surveys households and finds high anaemia, poor diet and low IFA compliance. What is the next use of this information?", "Plan a local intervention", ["Ignore the findings", "Stop all ANC", "Only change registers"], "Community diagnosis should lead to action based on identified needs.", True),
        q("Comprehensive health care includes promotive, preventive, curative and what services?", "Rehabilitative services", ["Only billing", "Only certification", "Only police reporting"], "Comprehensive care covers the full spectrum of health needs."),
        q("Family folder records help health workers maintain continuing information on what?", "Household health status", ["Only hospital furniture", "Only medicine colour", "Only weather"], "Family records support continuity, follow-up and community assessment."),
        q("Home visiting is useful in community health because it allows assessment of family environment and what?", "Health practices", ["Only hospital profit", "Only medical college rank", "Only X-ray quality"], "Home visits reveal living conditions, risks and care practices."),
        q("During a home visit, an ANM finds a newborn is cold, poorly feeding and lethargic. What should she do?", "Refer urgently for danger signs", ["Wait one month", "Only give a poster", "Ignore if no fever"], "Poor feeding and lethargy in a newborn are danger signs needing urgent care.", True),
        q("Community-based rehabilitation aims to improve quality of life of persons with disability through health, education, livelihood and what?", "Social inclusion", ["Isolation", "No follow-up", "Only hospital admission"], "CBR promotes inclusion and functioning within the community."),
        q("A child with cerebral palsy receives physiotherapy guidance, assistive support and school linkage near home. Which service is this?", "Community-based rehabilitation", ["Only tertiary admission", "Vital registration", "Mass chemoprophylaxis"], "Community-based rehabilitation supports function and participation close to home.", True),
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
                "id": f"community-medicine-health-care-community-{slug}-{i:02d}",
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
