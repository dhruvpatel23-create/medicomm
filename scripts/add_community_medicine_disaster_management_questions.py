import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Disaster Management"
CHAPTER_ORDER = 12
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
    ("concepts-cycle", "Concepts and Disaster Cycle", 1, [
        q("A disaster is best described as an event that overwhelms local capacity and requires what?", "External assistance", ["Routine outpatient care only", "No organized response", "Only private treatment"], "Disasters exceed the coping capacity of the affected community."),
        q("A hazard becomes a disaster mainly when it affects a vulnerable population and causes what?", "Serious disruption and losses", ["Only rainfall", "Only media attention", "Only road traffic"], "Hazard, exposure and vulnerability together determine disaster impact."),
        q("The disaster management cycle includes prevention, mitigation, preparedness, response and what?", "Recovery", ["Randomization", "Sterilization", "Screening only"], "Recovery restores services and livelihoods after the emergency phase."),
        q("An earthquake-prone city retrofits hospitals before an earthquake occurs. This is an example of what?", "Mitigation", ["Triage", "Rehabilitation only", "Case definition"], "Mitigation reduces the impact of future hazards.", True),
        q("Preparedness mainly refers to activities done before a disaster to improve what?", "Readiness for response", ["Birth rate", "Drug taste", "Bed colour"], "Preparedness includes planning, drills, stockpiles and training."),
        q("Early warning systems are most useful because they allow timely what?", "Preparedness and evacuation", ["Autopsy only", "Tax collection", "Blood grouping of all people"], "Warnings help communities take protective action before impact."),
        q("Vulnerability in disasters is increased by poverty, poor housing and what?", "Limited access to services", ["High literacy only", "Strong buildings", "Good communication"], "Social and structural factors shape disaster risk."),
        q("A coastal village receives cyclone alerts and shifts people to shelters before landfall. Which phase is this?", "Preparedness and response", ["Reconstruction only", "Epidemiological transition", "Screening validation"], "Warnings and evacuation bridge preparedness into immediate response.", True),
        q("Disaster risk is commonly understood as a function of hazard, exposure and what?", "Vulnerability", ["Blood pressure", "Incubation period", "Fertility rate"], "Risk rises when hazards affect exposed and vulnerable communities."),
        q("The aim of disaster management is to reduce loss of life, suffering and what?", "Damage to property and environment", ["Hospital profit only", "Examination marks", "Drug branding"], "Disaster management protects people, infrastructure and the environment.", True),
    ]),
    ("response-triage-relief", "Response, Triage and Relief", 2, [
        q("In mass casualty management, triage is used to sort patients according to what?", "Urgency of treatment and chance of survival", ["Alphabetical name order", "Patient income", "Hospital registration number"], "Triage prioritizes care when needs exceed immediately available resources."),
        q("The first priority in disaster response is usually to ensure what?", "Safety and lifesaving care", ["Long-term research only", "Billing records", "Routine vaccination cards"], "Immediate response focuses on rescue, safety, first aid and lifesaving treatment."),
        q("The triage category for immediate life-saving intervention is commonly represented by which colour?", "Red", ["Green", "Black", "Blue only"], "Red indicates immediate priority in many triage systems."),
        q("Walking wounded patients with minor injuries are commonly assigned which triage colour?", "Green", ["Red", "Black", "Yellow only"], "Green indicates minor injuries where treatment can be delayed."),
        q("A victim is unconscious with airway obstruction after a building collapse. Which triage category is most appropriate?", "Immediate priority", ["Minor priority", "Routine follow-up only", "No assessment needed"], "Airway compromise needs immediate lifesaving intervention.", True),
        q("A disaster medical relief camp should first organize registration, triage, treatment and what?", "Referral of serious cases", ["Cosmetic services", "Routine job placement", "Only school admissions"], "Relief camps need referral pathways for patients needing higher care."),
        q("Dead body management after disaster should emphasize identification, dignity and what?", "Proper documentation", ["Mass anonymous disposal", "Avoiding all records", "Public display"], "Documentation and respectful handling protect families and legal processes."),
        q("A large flood displaces families into a shelter. Which service is immediately essential?", "Safe water, sanitation and basic medical care", ["Elective surgery camps only", "Dental whitening", "Routine driving tests"], "Shelters must prevent dehydration, infection and sanitation-related outbreaks.", True),
        q("Incident command systems are useful during disasters because they create what?", "Clear coordination and command structure", ["More duplicate orders", "No accountability", "Only individual action"], "Defined roles improve coordination across agencies."),
        q("Psychological first aid after disasters mainly provides safety, calming, practical help and what?", "Connection to supports", ["Forced detailed debriefing", "Sedation for everyone", "Isolation of all survivors"], "Psychological first aid supports coping without forcing traumatic retelling.", True),
    ]),
    ("public-health-priorities", "Public Health Priorities", 3, [
        q("The major public health priorities after disasters include water, sanitation, shelter, food and what?", "Disease surveillance", ["Cosmetic surgery", "Routine licensing", "Luxury transport"], "Surveillance detects outbreaks early in displaced populations."),
        q("After floods, diarrhoeal disease risk increases mainly due to contamination of what?", "Drinking water", ["Vaccination cards", "Hospital uniforms", "Road signs"], "Flooding can contaminate water supplies and disrupt sanitation."),
        q("In temporary shelters, overcrowding most increases risk of which infections?", "Respiratory infections", ["Only fluorosis", "Only cataract", "Only diabetes"], "Crowding facilitates droplet and airborne spread."),
        q("A relief camp reports multiple cases of watery diarrhoea. What is the most urgent public health action?", "Ensure safe water, ORS and outbreak investigation", ["Close all latrines", "Stop handwashing", "Delay reporting for one month"], "Rapid control needs case management, water safety and surveillance.", True),
        q("Vector control after floods is important because stagnant water may increase breeding of what?", "Mosquitoes", ["Earthworms only", "Bedbugs only", "House dust mites only"], "Standing water can increase mosquito breeding and vector-borne disease risk."),
        q("The minimum emergency water requirement is planned to prevent dehydration and maintain what?", "Basic hygiene", ["Eye colour", "Road width", "School grades"], "Water supply in emergencies must cover drinking, cooking and hygiene needs."),
        q("Food relief should prioritize safety, adequate calories and needs of vulnerable groups such as children and whom?", "Pregnant women", ["Only athletes", "Only administrators", "Only tourists"], "Children, pregnant women, elderly people and the ill need special attention."),
        q("A measles outbreak is feared in an overcrowded camp with many unimmunized children. Which preventive action is important?", "Rapid immunization and vitamin A where indicated", ["Stop surveillance", "Give antibiotics to all adults only", "Ignore mild fever"], "Measles spreads rapidly in camps; vaccination campaigns reduce mortality.", True),
        q("Sanitation in disaster shelters mainly aims to prevent faeco-oral transmission by safe excreta disposal and what?", "Hand hygiene", ["Open defecation", "Waste mixing", "Unsafe food storage"], "Latrines, handwashing and waste disposal reduce enteric disease."),
        q("Public health surveillance after disaster should be simple, timely and focused on what?", "Priority epidemic-prone diseases", ["Rare genetic traits only", "Bank accounts", "Hospital paint quality"], "Emergency surveillance targets diseases needing rapid action.", True),
    ]),
    ("planning-rehabilitation", "Planning and Rehabilitation", 4, [
        q("A hospital disaster plan should clearly define roles, communication, supplies and what?", "Patient flow during emergencies", ["Cafeteria recipes", "Staff hobbies", "Only wall posters"], "Hospital plans must organize triage, surge capacity, referral and logistics."),
        q("Mock drills are conducted in disaster preparedness mainly to test what?", "Plans and team readiness", ["Drug expiry only", "Patient income", "Hospital decoration"], "Drills reveal gaps in coordination, timing, equipment and training."),
        q("A vulnerability assessment before disasters helps identify people and places at what?", "Higher risk", ["Higher examination score", "Lower blood group", "Better furniture"], "Mapping vulnerable groups helps target preparedness and mitigation."),
        q("A district stocks ORS, chlorine tablets and emergency medicines before monsoon. This is an example of what?", "Preparedness", ["Rehabilitation only", "Triage coding", "Vital registration"], "Pre-positioning supplies improves response speed.", True),
        q("Rehabilitation after disaster aims to restore physical, psychological and what?", "Social and economic functioning", ["Only laboratory reports", "Only exam attendance", "Only hospital paint"], "Recovery includes health, livelihoods, housing and social support."),
        q("Community participation in disaster management improves response because local people know local risks and what?", "Available resources", ["National stock prices", "Drug patents", "Bed linen brands"], "Community involvement makes preparedness and response more practical."),
        q("Risk communication during disasters should be clear, consistent and what?", "Trustworthy", ["Secretive", "Contradictory", "Delayed intentionally"], "People act better when messages are accurate, timely and credible."),
        q("After a cyclone, a family loses its home and livelihood. Which phase addresses long-term housing and income restoration?", "Rehabilitation and recovery", ["Immediate triage only", "Incubation period", "Vector density estimation only"], "Recovery extends beyond rescue to rebuilding lives and services.", True),
        q("Intersectoral coordination in disasters involves health services working with police, transport, water supply and whom?", "Local administration", ["Only pharmacists", "Only printers", "Only examiners"], "Disaster response requires coordinated action across multiple sectors."),
        q("A school in an earthquake zone teaches drop-cover-hold and evacuation routes. This is best classified as what?", "Community preparedness", ["Case-control study", "Hospital audit only", "Post-mortem care"], "Training communities before hazards improves survival and orderly evacuation.", True),
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
                "id": f"community-medicine-disaster-management-{slug}-{i:02d}",
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
