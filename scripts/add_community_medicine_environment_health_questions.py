import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Environment and Health"
CHAPTER_ORDER = 10
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
    ("water-health", "Water and Health", 1, [
        q("The most important requirement of drinking water is that it should be what?", "Free from pathogenic organisms", ["Coloured and sweet", "Always mineral-free", "Warm before drinking"], "Safe water should be microbiologically safe and acceptable."),
        q("Residual chlorine in piped water indicates what?", "Continuing disinfecting action", ["Absence of all minerals", "High hardness only", "Unsafe sewage mixing always"], "Residual chlorine protects against contamination after treatment."),
        q("The presumptive coliform test is used as an indicator of what?", "Faecal contamination of water", ["Protein deficiency", "Air pollution", "Noise exposure"], "Coliform organisms indicate possible faecal contamination."),
        q("A village reports diarrhoea after a pipeline leak near a drain. Which investigation is most relevant first?", "Bacteriological testing for faecal contamination", ["Audiometry", "Spirometry only", "Vision screening"], "Waterborne outbreaks require testing water safety and contamination source.", True),
        q("Slow sand filtration removes organisms mainly through which layer?", "Biological layer or schmutzdecke", ["Metal pipe wall", "Storage tank roof", "Chlorine cylinder"], "The surface biological layer is central to slow sand filter action."),
        q("Hardness of water is mainly due to salts of calcium and which other element?", "Magnesium", ["Iodine", "Fluorine only", "Sodium chloride only"], "Calcium and magnesium salts cause water hardness."),
        q("Excess fluoride in drinking water can cause which condition?", "Dental and skeletal fluorosis", ["Night blindness", "Scurvy", "Beriberi"], "High fluoride intake produces dental mottling and skeletal fluorosis."),
        q("A child from a high-fluoride area has mottled enamel. Which environmental exposure is responsible?", "Excess fluoride in drinking water", ["Low iodine", "High carbon monoxide", "Low protein"], "Dental fluorosis is linked to excess fluoride exposure during tooth development.", True),
        q("Safe water supply prevents many diseases transmitted by which route?", "Faeco-oral route", ["Only sexual route", "Only vector route", "Only genetic route"], "Water safety prevents cholera, typhoid, hepatitis A/E and other enteric infections."),
        q("After floods, the best immediate household-level measure to make water safer is what?", "Boiling or appropriate chlorination", ["Adding sugar", "Leaving water uncovered", "Mixing with river water"], "Emergency water safety relies on boiling/chlorination and safe storage.", True),
    ]),
    ("air-noise-radiation", "Air, Noise and Radiation Pollution", 2, [
        q("Air pollution is best defined as harmful concentration of contaminants in what?", "Atmosphere", ["Drinking water only", "Food grains only", "Soil only"], "Air pollution involves contaminants in ambient or indoor air."),
        q("Particulate matter is important because small particles can penetrate deeply into which system?", "Respiratory tract", ["Urinary bladder", "Bone marrow only", "Middle ear only"], "Fine particles reach lower airways and increase cardiopulmonary risk."),
        q("Carbon monoxide causes toxicity mainly by binding which molecule?", "Haemoglobin", ["Albumin only", "Bile salts", "Insulin"], "CO forms carboxyhaemoglobin, reducing oxygen delivery."),
        q("A family using coal stove indoors develops headache and cherry-red discoloration. Which exposure is likely?", "Carbon monoxide", ["Fluoride", "Iodine", "Chlorine residual"], "CO poisoning causes headache, hypoxia and sometimes cherry-red colour.", True),
        q("Indoor air pollution in rural homes is commonly linked to use of what?", "Biomass fuels", ["Iodized salt", "Boiled water", "ORS"], "Biomass fuel smoke contributes to respiratory disease."),
        q("Noise pollution can cause permanent damage to which function?", "Hearing", ["Taste only", "Renal filtration", "Bone growth"], "Chronic loud noise can cause noise-induced hearing loss."),
        q("The unit commonly used to measure sound intensity level is what?", "Decibel", ["Candela", "Calorie", "Millimetre of mercury"], "Noise level is expressed in decibels."),
        q("A factory worker with high-frequency hearing loss after years of machinery exposure likely has what?", "Noise-induced hearing loss", ["Trachoma", "Fluorosis", "Beriberi"], "Occupational noise exposure commonly affects high-frequency hearing first.", True),
        q("Ionizing radiation is hazardous mainly because it can damage what?", "DNA", ["Only hair colour", "Only taste buds", "Only sweat glands"], "Ionizing radiation can cause DNA breaks and cancer risk."),
        q("A radiology technician should use shielding and dosimetry mainly to reduce what?", "Occupational radiation exposure", ["Water hardness", "Food adulteration", "Vector density"], "Radiation protection follows time, distance, shielding and monitoring principles.", True),
    ]),
    ("waste-sanitation-housing", "Waste Disposal, Sanitation and Housing", 3, [
        q("Excreta disposal is important because faeces may contaminate water, food and what?", "Soil", ["Sunlight", "Oxygen only", "Vaccines"], "Unsafe excreta disposal spreads enteric pathogens through environment."),
        q("A sanitary latrine should prevent access of flies to what?", "Human excreta", ["Clean utensils", "Vaccines", "Clothing only"], "Fly-proof excreta disposal interrupts faeco-oral transmission."),
        q("Solid waste management begins with storage and what at source?", "Segregation", ["Open dumping", "Burning everywhere", "Mixing biomedical waste"], "Segregation at source improves safe handling and disposal."),
        q("A community with open defecation and repeated hookworm infection needs which intervention?", "Sanitary excreta disposal and footwear/health education", ["Only cataract surgery", "Only rabies vaccine", "Only BP screening"], "Soil contamination and barefoot exposure promote hookworm transmission.", True),
        q("Composting is a method used for disposal of which waste?", "Biodegradable solid waste", ["Radioactive waste only", "Needles only", "Mercury only"], "Organic waste can be decomposed into compost under controlled conditions."),
        q("Biomedical waste segregation should occur at which point?", "Point of generation", ["After final dumping", "After mixing with municipal waste", "Only at state office"], "Biomedical waste must be segregated where it is produced."),
        q("Overcrowding in housing increases transmission of which type of infections?", "Respiratory infections", ["Only snakebite", "Only fluorosis", "Only scurvy"], "Crowding facilitates droplet and airborne spread."),
        q("A child has recurrent respiratory infections in a poorly ventilated overcrowded room. Which housing factor is important?", "Overcrowding and poor ventilation", ["High iodine", "Low water hardness", "Excess sunlight"], "Crowding and poor ventilation increase respiratory infection risk.", True),
        q("Ventilation in housing is important because it removes heat, odours and what?", "Air contaminants", ["All nutrients", "All vaccines", "All soil"], "Ventilation improves indoor air quality."),
        q("After a needle-stick injury from improper hospital waste disposal, which failure is most likely?", "Unsafe biomedical waste handling", ["Safe water treatment", "School nutrition", "Birth registration"], "Sharps waste requires segregation, puncture-proof containers and safe disposal.", True),
    ]),
    ("climate-disasters-environmental-health", "Climate Change, Disasters and Environmental Health Protection", 4, [
        q("Climate change affects health partly by increasing frequency of heat waves and what?", "Extreme weather events", ["Blood group changes", "Antibiotic potency", "Vaccine freezing only"], "Climate change influences heat, disasters, vector ecology, food and water security."),
        q("Heat waves most directly increase risk of which condition?", "Heat-related illness", ["Iodine deficiency", "Rabies", "Leprosy"], "High ambient temperature can cause heat exhaustion and heat stroke."),
        q("Disaster management cycle includes mitigation, preparedness, response and what?", "Recovery", ["Randomization", "Sterilization only", "Case fatality only"], "Disaster management spans prevention/mitigation through recovery."),
        q("During a heat wave, an elderly person living alone is found confused and very hot. What is the immediate concern?", "Heat stroke", ["Simple myopia", "Dental fluorosis", "Scabies"], "Heat stroke causes hyperthermia with CNS dysfunction and needs urgent cooling.", True),
        q("Environmental health impact assessment is used to predict health effects of what?", "Development projects or policies", ["Only blood culture", "Only drug dosage", "Only autopsy"], "Impact assessment anticipates environmental and health consequences."),
        q("Vector-borne disease patterns may change with climate because climate affects vector breeding and what?", "Survival and distribution", ["Human blood group", "Vaccine vial colour", "Hospital bed count only"], "Temperature and rainfall influence vector ecology."),
        q("Floods increase risk of diarrhoeal disease mainly through contamination of what?", "Water supplies", ["X-ray films", "Vaccination cards", "Hearing aids"], "Flooding can contaminate drinking water and disrupt sanitation."),
        q("After flooding, a district prioritizes safe water, sanitation and ORS stocks. Which health risk is being addressed?", "Waterborne diarrhoeal disease", ["Only noise pollution", "Only refractive error", "Only dental caries"], "Flood response must prevent and treat diarrhoeal disease.", True),
        q("Environmental surveillance in public health helps detect hazards in air, water, food and what?", "Soil or workplace environments", ["Only bank accounts", "Only school marks", "Only postal codes"], "Surveillance tracks environmental exposures relevant to health."),
        q("A factory releases untreated effluent into a river used downstream for drinking water. Which public health action is needed?", "Environmental control and water safety enforcement", ["Ignore if water looks clear", "Only vitamin tablets", "Only road safety campaign"], "Industrial pollution requires regulatory control and protection of drinking water.", True),
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
                "id": f"community-medicine-environment-health-{slug}-{i:02d}",
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
