import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Occupational Health"
CHAPTER_ORDER = 13
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
    ("concepts-hazards", "Concepts and Occupational Hazards", 1, [
        q("Occupational health aims to promote and maintain the highest degree of physical, mental and what well-being of workers?", "Social well-being", ["Genetic purity", "Hospital income", "Only muscular strength"], "Occupational health protects total worker well-being in relation to work."),
        q("Occupational hazards are commonly classified as physical, chemical, biological, mechanical and what?", "Psychosocial hazards", ["Astrological hazards", "Only dietary hazards", "Only hereditary hazards"], "Workplace hazards include physical, chemical, biological, mechanical and psychosocial factors."),
        q("A worker exposed to excessive heat, noise and radiation is exposed to which class of occupational hazards?", "Physical hazards", ["Biological hazards only", "Psychosocial hazards only", "Nutritional hazards"], "Heat, noise, vibration and radiation are physical workplace hazards."),
        q("A quarry worker develops chronic cough and breathlessness after years of dust exposure. Which occupational hazard is most likely?", "Dust exposure", ["Excess iodine", "Low literacy only", "Poor handwriting"], "Inhaled mineral dust can cause pneumoconiosis and chronic respiratory symptoms.", True),
        q("Ergonomic hazards mainly arise from poor work design, posture and what?", "Repetitive movements", ["Clean drinking water", "Immunization", "Adequate lighting only"], "Repetition, awkward posture and forceful work contribute to musculoskeletal disorders."),
        q("The most effective occupational health approach is to prevent hazards at what stage?", "At the source", ["After disability only", "After retirement", "Only during compensation"], "Control at source is preferred over relying only on treatment after exposure."),
        q("Occupational disease usually develops because of exposure related to what?", "Work environment or work process", ["Only family history", "Only school attendance", "Only climate season"], "Occupational diseases are caused or aggravated by workplace exposures."),
        q("A nurse handling blood samples without gloves is at risk of which type of occupational hazard?", "Biological hazard", ["Noise hazard", "Heat hazard", "Ergonomic hazard only"], "Healthcare workers can acquire infections from blood and body-fluid exposure.", True),
        q("Occupational health services include pre-placement examination, periodic examination and what?", "Health education and workplace surveillance", ["Only tax collection", "Only drug advertisement", "Only sports coaching"], "Worker health checks, education and workplace monitoring are core services."),
        q("A clerk develops neck and wrist pain after long computer work with poor workstation setup. Which hazard is most likely?", "Ergonomic hazard", ["Ionizing radiation", "Lead poisoning", "Silicosis"], "Poor posture and repetitive computer work commonly cause ergonomic strain.", True),
    ]),
    ("dust-lung-diseases", "Dust and Occupational Lung Diseases", 2, [
        q("Pneumoconiosis refers to lung disease caused by inhalation of what?", "Dust", ["Clean oxygen", "Vitamins", "Pure water"], "Pneumoconiosis results from deposition and reaction to inhaled dust."),
        q("Silicosis is caused by inhalation of dust containing free crystalline what?", "Silica", ["Lead", "Mercury", "Cotton fibre only"], "Free silica dust causes silicosis in mining, quarrying and sandblasting."),
        q("Silicosis is classically associated with increased susceptibility to which infection?", "Tuberculosis", ["Rabies", "Measles only", "Hookworm"], "Silica exposure impairs lung defenses and increases tuberculosis risk."),
        q("A stone cutter has progressive dyspnoea and upper-lobe nodular fibrosis. Which occupational disease is likely?", "Silicosis", ["Asbestosis", "Byssinosis", "Bagassosis"], "Stone cutting exposes workers to silica dust causing nodular pulmonary fibrosis.", True),
        q("Asbestosis is caused by exposure to which occupational fibre?", "Asbestos", ["Coal tar only", "Sugarcane dust", "Cotton dust only"], "Asbestos fibres cause pulmonary fibrosis and pleural disease."),
        q("Asbestos exposure is strongly associated with mesothelioma and which cancer?", "Bronchogenic carcinoma", ["Retinoblastoma", "Osteosarcoma only", "Thyroid adenoma"], "Asbestos increases risk of lung cancer and malignant mesothelioma."),
        q("Byssinosis is commonly seen in workers exposed to dust from what?", "Cotton", ["Silica stone", "Asbestos sheets", "Lead battery plates"], "Cotton dust exposure can cause byssinosis in textile workers."),
        q("A textile worker gets chest tightness on the first working day after a weekend. Which disease is suggested?", "Byssinosis", ["Silicosis", "Asbestosis", "Anthrax"], "Byssinosis may cause Monday chest tightness among cotton textile workers.", True),
        q("Coal workers' pneumoconiosis is due to inhalation of what?", "Coal dust", ["Mercury vapour", "Vinyl chloride", "Pesticide spray only"], "Coal dust exposure can cause simple or complicated pneumoconiosis."),
        q("Dust control in workplaces is best achieved by wet methods, enclosure, ventilation and what?", "Personal respiratory protection when needed", ["Open dry sweeping", "More overtime", "Ignoring symptoms"], "Engineering controls are primary; respirators add protection where exposure remains.", True),
    ]),
    ("chemical-physical-hazards", "Chemical and Physical Hazards", 3, [
        q("Lead poisoning commonly affects the nervous system, gastrointestinal tract and what?", "Blood formation", ["Hair colour only", "Lens transparency only", "Tooth eruption only"], "Lead interferes with haem synthesis and causes neurological and abdominal features."),
        q("The characteristic line on gums in chronic lead poisoning is called what?", "Burtonian line", ["Koplik spot", "Bitot spot", "Kayser-Fleischer ring"], "A blue-black Burtonian line may appear on gums in chronic lead exposure."),
        q("A battery factory worker has abdominal colic, anaemia and wrist drop. Which poisoning is likely?", "Lead poisoning", ["Mercury poisoning", "Fluoride toxicity", "Carbon dioxide exposure"], "Lead can cause abdominal colic, anaemia, neuropathy and wrist drop.", True),
        q("Mercury poisoning classically affects the nervous system and may cause tremor and what?", "Erethism", ["Mottled enamel", "Monday fever", "Night blindness"], "Chronic mercury exposure can cause tremor, behavioural change and erethism."),
        q("Benzene exposure is dangerous because it can depress bone marrow and cause what?", "Leukaemia", ["Dental caries", "Cataract only", "Hookworm"], "Benzene is a marrow toxin and leukemogen."),
        q("Noise-induced hearing loss first commonly affects which frequencies?", "High frequencies", ["Only low frequencies", "Only speech frequencies at first", "No frequencies"], "Occupational noise damage often begins at high frequencies."),
        q("Permissible exposure limits are used to control exposure to workplace hazards over what?", "Specified time periods", ["Patient age only", "Hospital ownership", "Blood group"], "Exposure standards define acceptable concentrations or levels for defined durations."),
        q("A factory worker near loud machinery develops gradual bilateral high-frequency hearing loss. Which preventive measure is important?", "Noise control and hearing protection", ["More salt intake", "Only eye drops", "Unsafe open burning"], "Engineering noise control and ear protection reduce noise-induced hearing loss.", True),
        q("Heat stress in workers is prevented by ventilation, rest pauses, fluids and what?", "Acclimatization", ["Recapping needles", "Extra dust exposure", "Skipping breaks"], "Acclimatization and work-rest cycles help prevent heat illness."),
        q("A furnace worker becomes dizzy, hot and confused during work. Which condition is the urgent concern?", "Heat stroke", ["Silicosis", "Lead line", "Byssinosis"], "CNS dysfunction with hyperthermia suggests heat stroke needing urgent cooling.", True),
    ]),
    ("prevention-legislation-services", "Prevention, Legislation and Services", 4, [
        q("The hierarchy of control gives highest priority to eliminating the hazard and what?", "Substitution with a safer process", ["Compensation after disease", "Longer shifts", "More paperwork only"], "Elimination and substitution are preferred over relying only on PPE."),
        q("Engineering controls in occupational health include enclosure, isolation and what?", "Local exhaust ventilation", ["Only warning posters", "Only treatment camps", "Only worker transfer"], "Engineering controls reduce exposure at or near the source."),
        q("Personal protective equipment is best considered what level of control?", "Last line of defence", ["First and only control", "Replacement for all engineering controls", "Unnecessary in all work"], "PPE helps but should not replace source and engineering controls."),
        q("A spray painter refuses masks in a poorly ventilated room. Which control should be prioritized?", "Improve ventilation and ensure appropriate PPE", ["Increase exposure time", "Close all windows permanently", "Ignore symptoms"], "Chemical exposure control uses ventilation, safer materials and PPE.", True),
        q("Pre-placement medical examination is done mainly to assess fitness for what?", "Specific job hazards", ["Marriage eligibility", "School admission", "Driving speed only"], "Pre-placement assessment matches worker health with job demands and hazards."),
        q("Periodic medical examination of workers helps detect occupational disease at what stage?", "Early stage", ["Only after death", "After retirement only", "Only during litigation"], "Regular surveillance detects early effects before severe disability."),
        q("The Factories Act in India includes provisions related to worker health, safety and what?", "Welfare", ["University admissions", "Family planning targets only", "Road tolls"], "Factories legislation covers health, safety and welfare of workers."),
        q("A new employee joins a pesticide manufacturing unit. Which occupational health step is most appropriate before work starts?", "Pre-placement examination and hazard briefing", ["Ignore baseline health", "Only final compensation", "No training until illness"], "Baseline assessment and training are needed before exposure begins.", True),
        q("Occupational health education should teach workers about hazards, symptoms, safe practices and what?", "Use of protective equipment", ["Political voting only", "Hospital billing", "Unrelated cosmetics"], "Training helps workers recognize risks and use controls correctly."),
        q("A worker with suspected occupational asthma improves away from work and worsens on return. What is the key preventive action?", "Identify and control the workplace trigger", ["Only treat at home while exposure continues", "Increase exposure", "Stop all surveillance"], "Occupational asthma control requires reducing or removing the causative exposure.", True),
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
                "id": f"community-medicine-occupational-health-{slug}-{i:02d}",
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
