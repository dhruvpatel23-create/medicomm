import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Hospital Waste Management"
CHAPTER_ORDER = 11
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
    ("principles-classification", "Principles and Classification", 1, [
        q("Biomedical waste is waste generated during diagnosis, treatment or immunization of whom?", "Human beings or animals", ["Only healthy school children", "Only municipal sweepers", "Only pharmaceutical shops"], "Biomedical waste arises from healthcare, animal care, research and related biological activities."),
        q("The first and most important step in hospital waste management is what?", "Segregation at source", ["Final dumping", "Mixing before weighing", "Transport to landfill first"], "Correct segregation at the point of generation determines safe handling and treatment."),
        q("Most waste from healthcare facilities is usually which type?", "General non-hazardous waste", ["Radioactive waste", "Cytotoxic waste only", "Sharps waste only"], "Only a smaller fraction of healthcare waste is hazardous or infectious."),
        q("A ward attendant mixes food wrappers with blood-soaked dressings. Which principle has failed?", "Segregation of general and biomedical waste", ["Bed occupancy calculation", "Outpatient registration", "Ventilation planning"], "Mixing makes otherwise non-hazardous waste require biomedical waste handling.", True),
        q("Infectious hospital waste is important because it may transmit pathogens to patients, workers and whom?", "Waste handlers", ["Only radiologists", "Only pharmacists", "Only health economists"], "Waste handlers and sanitation staff are at risk if infectious waste is not segregated safely."),
        q("Anatomical waste from surgery belongs to which broad group?", "Biomedical waste", ["Domestic recyclable waste", "Office stationery waste", "Ordinary kitchen waste"], "Human tissues and organs from healthcare are biomedical waste requiring prescribed disposal."),
        q("Hospital waste management aims to prevent infection, injury and what?", "Environmental pollution", ["Hospital publicity", "Patient billing", "Bed numbering"], "Safe management protects people and the environment."),
        q("A clinic starts separating waste only after it reaches the common storage room. What is the main error?", "Segregation is delayed beyond the point of generation", ["Too much hand hygiene", "Too early reporting", "Excessive ventilation"], "Segregation must occur where the waste is generated, not after mixing.", True),
        q("Expired medicines and cytotoxic drugs are considered hazardous mainly because of what?", "Chemical and toxic effects", ["High water content only", "Better nutritional value", "Low temperature"], "Pharmaceutical and cytotoxic waste can harm handlers and the environment."),
        q("Needles, blades and broken glass are grouped as sharps because they can cause what?", "Puncture or cut injuries", ["Only bad odour", "Only water hardness", "Only noise exposure"], "Sharps injuries can transmit blood-borne infections.", True),
    ]),
    ("segregation-colour-coding", "Segregation and Colour Coding", 2, [
        q("Colour-coded containers are used in biomedical waste management to link waste type with what?", "Correct treatment and disposal route", ["Hospital wall colour", "Patient diet plan", "Ambulance parking"], "Colour coding standardizes segregation, transport and final treatment."),
        q("Human anatomical waste is commonly discarded in which colour-coded bag?", "Yellow bag", ["Blue box", "White translucent container", "Green municipal bin"], "Yellow category includes anatomical and soiled infectious wastes destined for appropriate treatment."),
        q("Soiled waste such as blood-stained cotton and dressings is placed in which bag?", "Yellow bag", ["Black office bin", "Blue cardboard box", "White sharps container"], "Blood-soaked dressings are infectious soiled waste and go in the yellow category."),
        q("Used plastic IV tubing and catheters are generally placed in which colour category after disinfection?", "Red bag", ["Yellow anatomical bag", "White sharps container", "Domestic wet waste bin"], "Contaminated recyclable plastic items are collected in the red category for disinfection and recycling."),
        q("Waste sharps including needles are placed in which container?", "White translucent puncture-proof container", ["Yellow soft bag", "Red soft bag", "Open paper carton"], "Sharps need puncture-proof, leak-proof, tamper-proof containers."),
        q("Broken contaminated glassware is usually collected in which colour category?", "Blue container", ["White sharps container only", "Red plastic bag", "Green kitchen bin"], "Glassware and metallic implants are handled in the blue category."),
        q("A nurse throws a used needle into a yellow bag after giving an injection. What is the correct action?", "Place it in a white puncture-proof sharps container", ["Leave it on the tray", "Put it with food waste", "Recap and keep in pocket"], "Needles must go into puncture-proof sharps containers to prevent injury.", True),
        q("An IV set is discarded with anatomical waste in a yellow bag. Which category should it usually enter?", "Red category", ["Blue category only", "White sharps category", "Municipal dry waste"], "Contaminated recyclable plastic tubing belongs to the red category after proper disinfection.", True),
        q("Colour-coded bags should be placed close to the site of waste generation mainly to improve what?", "Immediate correct segregation", ["Patient admission rate", "Drug procurement", "Radiology reporting"], "Bins at point of care make correct source segregation practical."),
        q("A broken medicine vial from a ward should not be mixed with food waste because it belongs to which stream?", "Glassware waste stream", ["General biodegradable stream", "Paper record stream", "Kitchen compost stream"], "Glassware requires separate collection and treatment to prevent injury and contamination.", True),
    ]),
    ("sharps-infection-safety", "Sharps and Infection Safety", 3, [
        q("The major occupational infection risk after needle-stick injury is transmission of which viruses?", "Hepatitis B, hepatitis C and HIV", ["Measles, mumps and rubella", "Dengue, malaria and filaria", "Rabies, polio and cholera"], "Blood-borne viruses are the key concern after sharps injuries."),
        q("Used needles should preferably be destroyed or mutilated soon after use to prevent what?", "Reuse and needle-stick injury", ["Improved sterility", "Higher vaccine potency", "Better record keeping"], "Needle destruction reduces injury and illegal reuse."),
        q("Recapping a used needle is discouraged because it increases risk of what?", "Needle-stick injury", ["Protein deficiency", "Water contamination only", "Excess ventilation"], "Recapping is a common cause of accidental needle injury."),
        q("A laboratory technician sustains a needle-stick injury. What should be done immediately?", "Wash the wound and report for post-exposure management", ["Suck the wound", "Ignore if painless", "Apply soil over the wound"], "Immediate washing, reporting, risk assessment and prophylaxis are needed.", True),
        q("Sharps containers should be puncture-proof, leak-proof and what?", "Tamper-proof", ["Transparent cloth bags", "Always open", "Made of thin paper"], "Sharps containers must prevent leakage, puncture and unauthorized access."),
        q("When should a sharps container generally be closed and sent for disposal?", "When it reaches the recommended fill level", ["Only when overflowing", "After needles spill out", "After one year"], "Overfilled containers increase puncture injury risk."),
        q("Hand hygiene and personal protective equipment in waste handling mainly protect against what?", "Contact with infectious material", ["Noise-induced deafness", "Dental fluorosis", "Population ageing"], "Gloves, masks and hand hygiene reduce exposure during handling."),
        q("A housekeeping worker is pricked while compressing a bag of mixed ward waste. Which preventable error is most likely?", "Sharps were not segregated into a puncture-proof container", ["Too much ventilation", "Excess chlorination", "Wrong outpatient ticket"], "Sharps should never be placed in soft bags that may be compressed.", True),
        q("Blood bags and visibly blood-contaminated waste require careful disposal because they may contain what?", "Infectious agents", ["Only harmless salts", "Only clean water", "Only oxygen"], "Blood and body-fluid contamination creates infection risk."),
        q("Training of doctors, nurses and waste handlers is essential because safe waste management depends on what?", "Correct practice by every category of staff", ["Only purchase of bins", "Only hospital size", "Only patient age"], "All staff who generate or handle waste must know segregation and safety practices.", True),
    ]),
    ("treatment-disposal-rules", "Treatment, Disposal and Rules", 4, [
        q("Incineration is used for selected biomedical waste mainly to achieve what?", "High-temperature destruction", ["Nutrient fortification", "Water softening", "Noise reduction"], "Incineration destroys suitable infectious and anatomical waste by high heat."),
        q("Autoclaving treats infectious waste mainly by using steam under what?", "Pressure", ["Sunlight only", "Dry soil", "Freezing"], "Autoclaving uses saturated steam under pressure to disinfect waste."),
        q("Deep burial may be permitted for biomedical waste disposal mainly in what setting?", "Rural or remote areas where access to common treatment is limited", ["Any urban hospital routinely", "Hospital kitchen", "Office record room"], "Deep burial is restricted and used where common treatment facilities are unavailable."),
        q("A small rural facility without access to a common biomedical waste treatment facility asks about disposal of permitted waste. Which option may be allowed under rules?", "Deep burial as per prescribed safeguards", ["Open roadside dumping", "Throwing into a river", "Mixing with market waste"], "Deep burial is allowed only under specified conditions and safeguards.", True),
        q("Liquid biomedical waste should generally be treated before discharge into what?", "Drains or sewers", ["Patient files", "Sharps boxes", "Food plates"], "Liquid waste must meet prescribed disinfection and discharge standards."),
        q("Common biomedical waste treatment facilities are useful because they provide what?", "Centralized treatment and disposal", ["Patient diagnosis", "Medical college admission", "Personal diet counselling"], "Common facilities help smaller healthcare units manage waste safely and lawfully."),
        q("The occupier of a healthcare facility is responsible for ensuring what?", "Safe segregation, storage, transport and disposal of biomedical waste", ["Only cafeteria menu", "Only ambulance colour", "Only ward decoration"], "Biomedical waste rules place responsibility on healthcare facilities that generate waste."),
        q("Untreated biomedical waste should not be stored beyond the prescribed time limit mainly to prevent what?", "Putrefaction, infection risk and nuisance", ["Better compost quality", "Higher oxygen level", "Improved billing"], "Prolonged storage increases odour, microbial growth and exposure risk."),
        q("A hospital sends untreated infectious waste with municipal waste to a dumping ground. What is the key violation?", "Biomedical waste must receive prescribed treatment and disposal", ["Waste was weighed", "The bag was too visible", "The ward was cleaned"], "Biomedical waste cannot be mixed with municipal waste and dumped untreated.", True),
        q("Records, labels and bar-code or tracking systems in biomedical waste management help ensure what?", "Accountability from generation to disposal", ["Patient blood group change", "Higher bed occupancy", "Drug taste improvement"], "Documentation and tracking support monitoring, compliance and traceability.", True),
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
                "id": f"community-medicine-hospital-waste-management-{slug}-{i:02d}",
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
