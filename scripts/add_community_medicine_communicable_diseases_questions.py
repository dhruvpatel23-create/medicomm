import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Epidemiology of Communicable Diseases"
CHAPTER_ORDER = 3
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
    ("respiratory-infections", "Respiratory infections", 1, [
        q("Tuberculosis is transmitted mainly through which route?", "Airborne droplet nuclei", ["Faeco-oral route", "Direct skin penetration", "Vector bite"], "Pulmonary TB spreads by inhalation of droplet nuclei from infectious cases."),
        q("The most important source of tuberculosis infection in the community is usually which case?", "Sputum-positive pulmonary case", ["Latent TB infection only", "Healed calcified lesion", "Extrapulmonary TB without discharge"], "Infectious pulmonary cases drive community transmission."),
        q("BCG vaccine is given primarily to prevent severe forms of which disease in children?", "Tuberculosis", ["Diphtheria", "Pertussis", "Influenza"], "BCG protects especially against severe childhood TB such as miliary TB and TB meningitis."),
        q("A child exposed to an infectious pulmonary TB case is found asymptomatic but tuberculin positive. What does this suggest?", "TB infection without active disease", ["Confirmed sputum-positive TB", "Diphtheria carrier state", "Measles incubation only"], "A positive tuberculin test after exposure may indicate infection, not necessarily active disease.", True),
        q("Measles is highly infectious mainly during which period?", "Catarrhal stage and early rash", ["Only after rash disappears", "Only during convalescence", "Only after vaccination"], "Measles spreads efficiently before and around rash onset."),
        q("Koplik spots are classically associated with which respiratory infection?", "Measles", ["Tuberculosis", "Influenza", "Mumps"], "Koplik spots are an early sign of measles."),
        q("Pertussis is characterized by paroxysmal cough followed by which feature?", "Inspiratory whoop", ["Rose spots", "Hydrophobia", "Black eschar"], "Whooping cough has paroxysms with inspiratory whoop, especially in children."),
        q("During a measles outbreak in a school, the most useful immediate control measure for susceptible contacts is what?", "Immunization of susceptible children", ["Mass antimalarial treatment", "Chlorination of wells only", "Dog vaccination"], "Measles outbreak control includes rapid immunization of susceptible contacts.", True),
        q("Diphtheria severe toxicity is caused mainly by what?", "Exotoxin", ["Endotoxin shock only", "Eggs in sputum", "Larval migration"], "Diphtheria toxin causes local membrane and systemic complications."),
        q("A child with grey pharyngeal membrane and bull neck needs urgent treatment with what?", "Diphtheria antitoxin and antibiotics", ["ORS only", "Rabies vaccine only", "Albendazole only"], "Suspected diphtheria requires prompt antitoxin plus antibiotics and isolation.", True),
    ]),
    ("intestinal-infections", "Intestinal infections", 2, [
        q("Cholera is transmitted mainly by which route?", "Faeco-oral route through contaminated water or food", ["Airborne droplet nuclei", "Sexual contact only", "Tick bite"], "Cholera spreads through ingestion of contaminated water or food."),
        q("The stool in typical cholera is classically described as what?", "Rice-water stool", ["Currant jelly stool", "Black tarry stool", "Pea soup sputum"], "Profuse watery rice-water stools are typical of cholera."),
        q("The immediate life-saving treatment in cholera is what?", "Rapid fluid and electrolyte replacement", ["Antitoxin only", "Surgery", "Steroid pulse"], "Deaths in cholera are mainly due to dehydration and shock."),
        q("A village reports sudden profuse watery diarrhoea in many adults after a feast. What is the first public health priority?", "Rehydration and outbreak control measures", ["Mass chemotherapy for malaria", "BCG campaign", "Dog bite prophylaxis"], "Cholera-like outbreaks require urgent rehydration plus water, sanitation and surveillance action.", True),
        q("Typhoid fever is caused by which organism?", "Salmonella Typhi", ["Vibrio cholerae", "Shigella dysenteriae", "Entamoeba histolytica"], "Enteric fever is commonly caused by Salmonella Typhi."),
        q("A chronic typhoid carrier usually harbours organisms in which site?", "Gall bladder", ["Lung apex", "Peripheral nerves", "Red blood cells"], "Chronic carriage is often associated with gall bladder colonization."),
        q("Poliomyelitis spreads predominantly through which route?", "Faeco-oral route", ["Mosquito bite", "Dog bite", "Sexual route only"], "Poliovirus commonly spreads through faecal contamination."),
        q("A child with acute flaccid paralysis must be reported because surveillance targets which disease?", "Poliomyelitis", ["Leprosy", "Tetanus", "Plague only"], "AFP surveillance is essential for detecting poliovirus transmission.", True),
        q("Hepatitis A is commonly transmitted by which route?", "Faeco-oral route", ["Blood transfusion mainly", "Airborne spread", "Vector bite"], "HAV is an enterically transmitted viral hepatitis."),
        q("After floods, a community has increased diarrhoeal disease risk. Which preventive measure is most important?", "Safe water and sanitation", ["Indoor residual spraying only", "BCG revaccination", "Vitamin A alone"], "Water safety, sanitation and hygiene are central to preventing intestinal infections.", True),
    ]),
    ("arthropod-borne-infections", "Arthropod-borne infections", 3, [
        q("Malaria is transmitted by which vector?", "Female Anopheles mosquito", ["Aedes mosquito", "Culex mosquito", "Sandfly"], "Human malaria is transmitted by infected female Anopheles mosquitoes."),
        q("Dengue is transmitted mainly by which mosquito?", "Aedes aegypti", ["Anopheles culicifacies", "Culex quinquefasciatus", "Mansonia mosquito"], "Aedes aegypti is the principal dengue vector."),
        q("Filariasis in India is commonly transmitted by which vector?", "Culex mosquito", ["Hard tick", "Tsetse fly", "Rat flea"], "Bancroftian filariasis is commonly transmitted by Culex quinquefasciatus."),
        q("A patient with high fever, thrombocytopenia and severe body ache during monsoon is suspected dengue. Which vector control advice is most relevant?", "Remove stagnant clean water containers", ["Avoid only night-time outdoor exposure", "Boil milk", "Control rats only"], "Aedes breeds in clean stagnant water and bites mainly during daytime.", True),
        q("Kala-azar is transmitted by which vector?", "Sandfly", ["Aedes mosquito", "Louse", "Housefly"], "Visceral leishmaniasis is transmitted by sandflies."),
        q("Japanese encephalitis is transmitted mainly by which mosquito?", "Culex mosquito", ["Anopheles only", "Aedes aegypti only", "Sandfly"], "JE virus is transmitted by Culex mosquitoes, often linked to pigs and paddy fields."),
        q("The definitive host and reservoir pattern in malaria control focuses on which source?", "Human cases carrying gametocytes", ["Only cattle", "Only dogs", "Only soil"], "Mosquitoes acquire infection from human gametocyte carriers."),
        q("A village near paddy fields reports encephalitis cases in children. Which disease should be suspected?", "Japanese encephalitis", ["Cholera", "Diphtheria", "Tetanus"], "JE occurs in rural settings with Culex breeding and amplifying hosts.", True),
        q("Integrated vector management combines environmental, biological and which other measures?", "Chemical control and personal protection", ["Only hospital isolation", "Only surgery", "Only food fortification"], "Vector control uses multiple locally appropriate methods."),
        q("A malaria programme monitors slide positivity rate. What does this indicator measure?", "Proportion of examined blood smears positive for malaria parasite", ["Mosquito density only", "Case fatality rate", "Vaccine efficacy"], "SPR is a surveillance indicator for malaria transmission among tested fever cases.", True),
    ]),
    ("zoonoses", "Zoonoses", 4, [
        q("Zoonoses are diseases naturally transmitted between humans and which hosts?", "Vertebrate animals", ["Only plants", "Only insects", "Only fungi in soil"], "Zoonoses involve natural transmission between vertebrate animals and humans."),
        q("Rabies is transmitted most commonly to humans through what?", "Bite of an infected dog", ["Contaminated water", "Mosquito bite", "Airborne dust"], "Dog bite is the most common source of human rabies in endemic settings."),
        q("The incubation period of rabies is influenced strongly by which factor?", "Site and severity of bite", ["Blood group", "Hair colour", "Height"], "Bites closer to CNS and severe exposures shorten incubation."),
        q("A child has a category III dog bite with bleeding. What is required besides wound washing and vaccine?", "Rabies immunoglobulin", ["BCG", "ORS", "Antimalarial prophylaxis"], "Category III rabies exposure requires vaccine plus rabies immunoglobulin infiltration.", True),
        q("Plague is classically transmitted by which vector?", "Rat flea", ["Aedes mosquito", "Sandfly", "Louse only"], "Rat fleas transmit Yersinia pestis between rodents and humans."),
        q("Leptospirosis is commonly acquired through contact with water contaminated by which animal excreta?", "Rat urine", ["Dog saliva only", "Bird feathers", "Cow milk only"], "Leptospira are shed in urine, especially by rodents."),
        q("Brucellosis is associated with exposure to infected animals and which food item?", "Unpasteurized milk", ["Boiled rice", "Chlorinated water", "Refined sugar"], "Brucellosis can spread through raw milk and occupational animal exposure."),
        q("After floods, fever with calf tenderness and conjunctival suffusion suggests which zoonosis?", "Leptospirosis", ["Rabies", "Plague", "Hydatid disease"], "Floodwater exposure to rat urine is a classic leptospirosis risk.", True),
        q("Hydatid disease is caused by larval stage of which parasite?", "Echinococcus granulosus", ["Plasmodium vivax", "Vibrio cholerae", "Wuchereria bancrofti"], "Dogs are definitive hosts and humans may develop hydatid cysts."),
        q("A shepherd with liver cysts and dog exposure most likely has which disease?", "Hydatid disease", ["Dengue", "Japanese encephalitis", "Typhoid"], "Livestock-dog cycle and hepatic cysts suggest echinococcosis.", True),
    ]),
    ("surface-infections", "Surface infections", 5, [
        q("Trachoma primarily affects which structure?", "Conjunctiva", ["Liver", "Kidney", "Lung alveoli"], "Trachoma is a chronic conjunctival infection caused by Chlamydia trachomatis."),
        q("The SAFE strategy is used for control of which disease?", "Trachoma", ["Tuberculosis", "Malaria", "Cholera"], "SAFE means surgery, antibiotics, facial cleanliness and environmental improvement."),
        q("Leprosy primarily affects skin and which nerves?", "Peripheral nerves", ["Optic nerve only", "Auditory nerve only", "Phrenic nerve only"], "Mycobacterium leprae affects skin and peripheral nerves."),
        q("A patient with hypopigmented anaesthetic skin patch should be evaluated for which disease?", "Leprosy", ["Dengue", "Cholera", "Pertussis"], "Anaesthetic skin lesions are a cardinal feature of leprosy.", True),
        q("Multidrug therapy for leprosy is important mainly to prevent what?", "Drug resistance and transmission", ["Vitamin deficiency", "Mosquito breeding", "Food adulteration"], "MDT cures infection and reduces resistance/transmission."),
        q("Tetanus occurs after contamination of wounds by spores of which organism?", "Clostridium tetani", ["Vibrio cholerae", "Salmonella Typhi", "Plasmodium falciparum"], "C. tetani spores enter wounds and produce neurotoxin."),
        q("Neonatal tetanus is prevented most effectively by clean delivery practices and what?", "Maternal tetanus immunization", ["BCG at birth only", "ORS", "Iron tablets only"], "Maternal immunization protects the newborn through transplacental antibodies."),
        q("A newborn develops inability to suck and spasms on day 7 after cord application of cow dung. Which disease is likely?", "Neonatal tetanus", ["Measles", "Polio", "Rabies"], "Unclean cord care can introduce tetanus spores.", True),
        q("Yaws is transmitted mainly through which route?", "Direct skin contact", ["Airborne droplet nuclei", "Mosquito bite", "Faeco-oral route"], "Yaws spreads by direct contact with infectious skin lesions."),
        q("A community programme for scabies should emphasize treatment of cases and which group?", "Close contacts", ["Only newborns", "Only food handlers", "Only pet dogs"], "Scabies spreads by close contact, so contacts often need treatment.", True),
    ]),
    ("emerging-reemerging", "Emerging and re-emerging infectious diseases", 6, [
        q("Emerging infectious diseases are infections that have newly appeared or are doing what?", "Increasing in incidence or geographic range", ["Always eradicated", "Never transmissible", "Only laboratory artefacts"], "Emerging diseases are new or rapidly increasing threats."),
        q("Re-emerging infections are diseases that were controlled but are now doing what?", "Increasing again", ["Completely extinct", "Only genetic disorders", "Non-infectious only"], "Re-emergence means return or increase after decline."),
        q("A major driver of emerging infections is which factor?", "Ecological change and human-animal interaction", ["Perfect sanitation", "Universal immunity", "No travel"], "Land use change, animal contact, travel and climate can promote emergence."),
        q("A cluster of severe pneumonia caused by a novel virus is detected in multiple countries. What public health action is most urgent?", "Surveillance, reporting and containment measures", ["Ignore until mortality reaches 100%", "Only vitamin distribution", "Stop all routine immunization"], "Emerging threats require early detection, reporting, isolation/contact measures and risk communication.", True),
        q("Antimicrobial resistance is considered an emerging public health problem because it causes what?", "Reduced effectiveness of standard treatment", ["Higher vaccine coverage always", "Lower hospital stay always", "No need for diagnosis"], "Resistance threatens treatment and infection control."),
        q("Nipah virus outbreaks are linked epidemiologically with bats and which route in some settings?", "Contaminated date palm sap or animal exposure", ["Chlorinated water", "Only sexual transmission", "Tick bite only"], "Nipah has bat reservoirs and can spill over through contaminated food or animals."),
        q("Pandemic potential is greatest when an infection has efficient human transmission and what?", "Population susceptibility", ["No incubation period ever", "No international travel", "Zero mutation"], "A susceptible population and sustained transmission favour spread."),
        q("A hospital sees unusual fever with bleeding in a traveller from an outbreak area. What is the safest first response?", "Immediate isolation and notification", ["Send home without advice", "Mass antibiotic use in the city", "Delay until culture confirmation only"], "Suspected high-risk emerging infections require isolation and public health notification.", True),
        q("One Health approach links human health with animal health and what?", "Environmental health", ["Only hospital billing", "Only surgery", "Only medical education"], "One Health recognizes connected human-animal-environment disease ecology."),
        q("Reappearance of diphtheria in a poorly immunized community mainly indicates failure of what?", "Sustained vaccination coverage", ["Vector control", "Water chlorination only", "Rabies prophylaxis"], "Vaccine-preventable disease re-emergence often reflects immunity gaps.", True),
    ]),
    ("hospital-acquired-infections", "Hospital acquired infections", 7, [
        q("Hospital acquired infection is also called what?", "Nosocomial infection", ["Zoonosis", "Endemic equilibrium", "Incubation period"], "Nosocomial infections are acquired in healthcare settings."),
        q("A common source of healthcare-associated urinary infection is which device?", "Urinary catheter", ["Stethoscope only", "Pulse oximeter only", "Thermometer only"], "Catheter-associated UTI is a frequent HAI."),
        q("The single most important measure to prevent hospital infection transmission is what?", "Hand hygiene", ["Daily chest X-ray", "Universal antibiotics", "Longer admission"], "Hand hygiene is central to infection prevention and control."),
        q("A patient develops fever and purulent discharge from an operative wound three days after surgery. Which infection category is likely?", "Surgical site infection", ["Congenital infection", "Vector-borne infection", "Food poisoning only"], "Postoperative wound infection is a surgical site HAI.", True),
        q("Standard precautions should be applied to which patients?", "All patients", ["Only HIV-positive patients", "Only ICU patients", "Only children"], "Standard precautions assume all blood/body fluids may be infectious."),
        q("Biomedical waste segregation should be done at which point?", "Point of generation", ["After transport to landfill", "Only at district office", "After mixing all waste"], "Correct segregation must occur where waste is produced."),
        q("Antibiotic stewardship aims mainly to reduce inappropriate antimicrobial use and what?", "Antimicrobial resistance", ["Bed occupancy only", "Oxygen demand", "Birth rate"], "Stewardship improves antimicrobial use and limits resistance."),
        q("An ICU has rising ventilator-associated pneumonia rates. Which bundle element is relevant?", "Elevating head end and ventilator care practices", ["Stopping hand hygiene", "Routine reuse of suction catheters", "No oral care"], "VAP prevention uses bundled practices including head elevation and aseptic care.", True),
        q("Isolation precautions are selected based on what?", "Mode of transmission", ["Patient income", "Hospital floor number", "Disease spelling"], "Contact, droplet and airborne precautions depend on transmission route."),
        q("A patient with suspected pulmonary tuberculosis in hospital should be placed under which precautions?", "Airborne precautions", ["Only food precautions", "No precautions", "Vector precautions"], "Infectious pulmonary TB requires airborne infection control measures.", True),
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
                "id": f"community-medicine-communicable-{slug}-{i:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": order,
                "options": opts,
                "answerIndex": opts.index(ans),
                "answer": ans,
            })
    return out


def validate(qs):
    if len(qs) != 70:
        raise ValueError(f"Expected 70, got {len(qs)}")
    if len({q["id"] for q in qs}) != 70:
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
