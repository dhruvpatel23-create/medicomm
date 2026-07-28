import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Central Nervous System Infections"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("cns-infective-syndromes", "Infective Syndromes of Central Nervous System", [
        q("A patient has fever, headache, neck stiffness, photophobia, and altered sensorium. The syndrome to urgently exclude is:", "Meningitis", ["Cellulitis", "Cholera", "Cystitis"], "Meningitis classically presents with fever, headache, meningism, and altered mental status."),
        q("Focal seizures, personality change, and fever suggest brain parenchymal involvement, best termed:", "Encephalitis", ["Rhinitis", "Urethritis", "Impetigo"], "Encephalitis involves brain parenchyma and causes altered behavior, seizures, or focal deficits."),
        q("A ring-enhancing brain lesion with fever in an otitis media patient suggests:", "Brain abscess", ["Viral meningitis only", "Tetanus", "Botulism"], "Brain abscess can follow contiguous ear/sinus infection or hematogenous spread."),
        q("CSF in acute bacterial meningitis typically shows:", "Neutrophils, high protein, and low glucose", ["Lymphocytes, normal glucose, low protein", "Eosinophils only, high glucose", "No cells, no protein"], "Pyogenic meningitis causes neutrophilic pleocytosis, elevated protein, and hypoglycorrhachia."),
        q("CSF in most viral meningitis typically shows:", "Lymphocytic pleocytosis with normal glucose", ["Neutrophils with very low glucose always", "No cells and high glucose", "Only RBCs"], "Viral meningitis is usually lymphocytic with normal glucose and modest protein elevation."),
        q("Lumbar puncture should be delayed for brain imaging first when there is:", "Papilledema or focal neurological deficit suggesting raised intracranial pressure", ["Mild sore throat", "Normal sensorium", "Simple fever only"], "LP in raised intracranial pressure can risk herniation; obtain imaging when red flags exist."),
        q("Empiric bacterial meningitis antibiotics should be given:", "Immediately after blood cultures if LP is delayed", ["Only after culture final report", "After 1 week observation", "Only if rash appears"], "Treatment delay worsens outcomes; blood cultures should not postpone therapy."),
        q("A petechial rash with meningitis strongly suggests:", "Meningococcemia", ["Cryptococcosis", "Tetanus", "Polio"], "Neisseria meningitidis can cause meningitis with petechiae/purpura and shock."),
        q("A chronic meningitis pattern over weeks with basilar enhancement suggests:", "Tuberculous meningitis", ["Acute influenza", "Botulism", "Cholera"], "TB meningitis is subacute/chronic and often basal, with cranial nerve palsies and hydrocephalus."),
        q("Raised intracranial pressure in meningitis is dangerous because it can cause:", "Brain herniation and reduced cerebral perfusion", ["Improved antibiotic entry always", "Immediate cure", "Only hearing gain"], "CNS infection-associated edema can cause life-threatening pressure effects."),
    ]),
    ("bacterial-meningitis", "Bacterial Meningitis", [
        q("A college student has meningitis with petechial rash and Gram-negative diplococci in CSF. The organism is:", "Neisseria meningitidis", ["Streptococcus pneumoniae", "Listeria monocytogenes", "Haemophilus influenzae"], "Meningococcus is a Gram-negative diplococcus associated with petechial rash."),
        q("An elderly alcoholic patient with meningitis and lancet-shaped Gram-positive diplococci likely has:", "Streptococcus pneumoniae", ["N. meningitidis", "E. coli", "Cryptococcus"], "Pneumococcus is a leading adult meningitis cause and is encapsulated."),
        q("Neonatal meningitis with Gram-positive rods showing tumbling motility suggests:", "Listeria monocytogenes", ["S. agalactiae", "N. meningitidis", "H. influenzae"], "Listeria causes neonatal/elderly/pregnancy meningitis and has tumbling motility."),
        q("Late-onset neonatal meningitis commonly includes:", "Group B Streptococcus", ["Vibrio cholerae", "Mycobacterium leprae", "Treponema pallidum pertenue"], "S. agalactiae is a major neonatal sepsis/meningitis cause."),
        q("Hib meningitis has decreased dramatically due to vaccine against:", "Polyribosylribitol phosphate capsule", ["Lipid A", "M protein", "Flagellin"], "Hib conjugate vaccine targets PRP capsule."),
        q("Adjunctive dexamethasone in suspected bacterial meningitis is used mainly to reduce:", "Inflammation-mediated neurologic complications such as hearing loss", ["Bacterial growth in culture", "Need for antibiotics", "CSF glucose"], "Steroids blunt inflammatory injury, especially in pneumococcal/Hib contexts when timed early."),
        q("Close contacts of meningococcal meningitis require chemoprophylaxis because:", "Nasopharyngeal carriage can spread invasive disease", ["The organism is vector-borne", "It spreads by stool only", "Contacts always have chronic meningitis"], "Meningococcus colonizes the nasopharynx and spreads via respiratory droplets."),
        q("Rifampicin, ciprofloxacin, or ceftriaxone may be used for prophylaxis of contacts of:", "Neisseria meningitidis", ["Tetanus", "Rabies", "Naegleria"], "These agents eradicate meningococcal carriage in exposed close contacts."),
        q("Tuberculous meningitis CSF usually shows:", "Lymphocytes, high protein, and low glucose", ["Neutrophils, normal protein, high glucose", "No cells", "Only eosinophils"], "TB meningitis causes chronic lymphocytic meningitis with low glucose."),
        q("Lyme neuroborreliosis is caused by:", "Borrelia burgdorferi", ["Leptospira interrogans", "Treponema pallidum pertenue", "Rickettsia rickettsii"], "Borrelia burgdorferi can cause meningitis, facial palsy, and radiculopathy."),
    ]),
    ("tetanus", "Tetanus", [
        q("A farmer develops trismus, risus sardonicus, and painful spasms after a contaminated wound. The toxin blocks release of:", "GABA and glycine", ["Acetylcholine at NMJ", "Dopamine", "Histamine"], "Tetanospasmin prevents inhibitory neurotransmitter release, causing spastic paralysis."),
        q("Clostridium tetani is best described as:", "Anaerobic spore-forming Gram-positive bacillus", ["Aerobic Gram-negative coccus", "Acid-fast bacillus", "Encapsulated yeast"], "C. tetani is a spore-forming anaerobic Gram-positive rod."),
        q("The classic drumstick appearance of C. tetani is due to:", "Terminal spores", ["Capsule", "Flagellar tuft", "Bipolar staining"], "Terminal spores distend the bacillus, creating drumstick morphology."),
        q("Tetanus toxin reaches the CNS mainly by:", "Retrograde axonal transport", ["Bloodstream crossing only", "Mosquito inoculation", "Direct CSF injection"], "Tetanospasmin travels retrograde along nerves to inhibitory interneurons."),
        q("A tetanus-prone wound in an unimmunized patient requires:", "Tetanus immunoglobulin plus toxoid vaccination and wound care", ["Only antibiotics", "Only vaccine with no immunoglobulin", "No prophylaxis"], "TIG neutralizes unbound toxin while vaccine induces active immunity."),
        q("Tetanus disease does not reliably produce immunity because:", "Very small toxin amounts cause disease without adequate antibody response", ["The toxin is not antigenic", "Spores destroy antibodies", "It is viral"], "Patients recovering from tetanus still need vaccination."),
        q("Neonatal tetanus is commonly linked to:", "Contaminated umbilical stump and lack of maternal immunization", ["Breast milk antibodies", "Clean delivery", "BCG scar"], "Unclean cord care and absent maternal antitoxin predispose to neonatal tetanus."),
        q("Metronidazole in tetanus management is used to:", "Kill vegetative C. tetani in the wound", ["Neutralize bound toxin", "Reverse spasms instantly", "Provide active immunity"], "Antibiotics reduce toxin production but do not affect toxin already bound."),
        q("Autonomic instability in severe tetanus can cause:", "Labile hypertension, tachycardia, and arrhythmias", ["Watery diarrhea only", "Hypothyroidism", "Hydrocele"], "Severe tetanus affects autonomic output and requires ICU care."),
        q("The most effective population prevention of tetanus is:", "Routine toxoid immunization with boosters", ["Natural infection", "Boiling water only", "Mosquito control"], "Tetanus toxoid vaccination induces protective antitoxin antibodies."),
    ]),
    ("viral-meningitis-myelitis", "Viral Meningitis and Myelitis: Poliomyelitis, Coxsackievirus Infections, and Others", [
        q("The most common cause group of aseptic viral meningitis is:", "Enteroviruses", ["Poxviruses", "Hepadnaviruses", "Orthomyxoviruses only"], "Enteroviruses, including coxsackie and echoviruses, commonly cause aseptic meningitis."),
        q("A child develops fever followed by asymmetric flaccid paralysis. The classic virus is:", "Poliovirus", ["Rabies virus", "HSV-1", "EBV"], "Poliovirus can destroy anterior horn cells causing acute flaccid paralysis."),
        q("Poliovirus primarily damages:", "Anterior horn cells of spinal cord", ["Posterior columns only", "Basal ganglia", "Peripheral myelin only"], "Motor neuron destruction produces lower motor neuron weakness."),
        q("Poliovirus is transmitted mainly by:", "Fecal-oral route", ["Tick bite", "Dog bite", "Sexual contact only"], "Poliovirus replicates in the gut and spreads fecal-orally."),
        q("Oral polio vaccine has the advantage of:", "Inducing intestinal mucosal immunity", ["No live virus", "No herd effect", "No fecal shedding ever"], "OPV induces gut immunity and can reduce transmission, but rarely reverts."),
        q("Vaccine-associated paralytic polio is a rare risk of:", "Oral live attenuated polio vaccine", ["Inactivated polio vaccine", "Tetanus toxoid", "Hib conjugate"], "OPV contains live attenuated virus that can rarely revert to neurovirulence."),
        q("Hand-foot-mouth disease with aseptic meningitis can be caused by:", "Coxsackievirus", ["Diphtheria toxin", "M. tuberculosis", "Cryptococcus"], "Enteroviruses such as Coxsackie can cause vesicular disease and meningitis."),
        q("CSF PCR is useful in viral meningitis because it:", "Rapidly detects viral nucleic acid", ["Measures antibody titer only after months", "Cultures bacteria", "Shows spores"], "Molecular tests can identify enterovirus/HSV and guide management."),
        q("Acute flaccid myelitis has been associated with:", "Enterovirus D68", ["Hepatitis B", "Rotavirus", "Molluscum contagiosum"], "EV-D68 has been linked to outbreaks of acute flaccid myelitis."),
        q("Supportive care in viral meningitis is appropriate when:", "Bacterial meningitis and treatable viral causes have been reasonably excluded", ["The patient is in shock", "CSF shows Gram-positive diplococci", "There is purpura fulminans"], "Most viral meningitis is self-limited, but dangerous mimics must be excluded."),
    ]),
    ("viral-encephalitis", "Viral Encephalitis and Encephalopathy", [
        q("A patient has fever, seizures, personality change, and temporal lobe MRI abnormalities. Treat empirically for:", "HSV encephalitis", ["Rabies only", "Dengue only", "Polio"], "HSV-1 encephalitis classically involves temporal lobes and requires urgent acyclovir."),
        q("HSV encephalitis is diagnosed rapidly by:", "HSV PCR in CSF", ["Widal test", "ASO titer", "India ink"], "CSF PCR is the test of choice for HSV encephalitis."),
        q("Rabies virus reaches the CNS primarily by:", "Retrograde axonal transport from bite site", ["Fecal-oral spread", "RBC invasion", "Portal venous spread"], "Rabies travels along peripheral nerves to the CNS."),
        q("Negri bodies are found in:", "Rabies", ["HSV encephalitis", "Japanese encephalitis", "Prion disease"], "Negri bodies are cytoplasmic inclusions classically in rabies-infected neurons."),
        q("Hydrophobia in rabies occurs because:", "Painful pharyngeal spasms are triggered by attempts to swallow", ["Patient is dehydrated only", "Virus infects kidney only", "Water contains toxin"], "Rabies causes encephalitis with spasms triggered by swallowing or air currents."),
        q("Japanese encephalitis is transmitted by:", "Culex mosquito", ["Dog bite", "Sandfly", "Body louse"], "JE virus is a flavivirus transmitted by Culex mosquitoes, with pigs/wading birds in the cycle."),
        q("West Nile neuroinvasive disease is more severe in:", "Older or immunocompromised patients", ["Only neonates after honey", "Only patients with leprosy", "Only vaccinated contacts"], "Age and immunosuppression increase risk of encephalitis/paralysis."),
        q("Nipah virus outbreaks are linked to:", "Bats with possible pig or date palm sap exposure", ["Freshwater snails", "Dog tapeworm", "Body louse"], "Nipah is a henipavirus reservoired in fruit bats and can cause encephalitis."),
        q("Prion diseases are caused by:", "Misfolded prion protein inducing abnormal folding", ["Enveloped RNA virus", "Gram-positive bacillus", "Protozoan cyst"], "Prions lack nucleic acid and cause transmissible spongiform encephalopathies."),
        q("Subacute sclerosing panencephalitis is a late complication of:", "Measles virus infection", ["Mumps vaccine only", "Rabies PEP", "Adenovirus gastroenteritis"], "SSPE is a progressive late measles complication, prevented by vaccination."),
    ]),
    ("parasitic-fungal-cns", "Parasitic and Fungal Infections of Central Nervous System", [
        q("A patient with seizures has multiple ring-enhancing brain lesions with scolex. The diagnosis is:", "Neurocysticercosis", ["Hydatid lung disease", "Cerebral malaria only", "Cryptococcosis"], "Neurocysticercosis is caused by Taenia solium larvae in CNS."),
        q("Humans develop cysticercosis after ingesting:", "Taenia solium eggs", ["Taenia saginata cysticerci", "Ascaris eggs only", "Echinococcus adult worms"], "Ingested T. solium eggs release larvae that disseminate to tissues."),
        q("A swimmer develops rapidly fatal meningoencephalitis after warm freshwater exposure. The likely organism is:", "Naegleria fowleri", ["Acanthamoeba", "Toxoplasma", "Cryptococcus"], "Naegleria causes primary amebic meningoencephalitis via cribriform plate."),
        q("Naegleria fowleri enters the CNS through:", "Olfactory mucosa and cribriform plate", ["GI portal vein", "Mosquito bite", "Dog bite"], "Water forced into the nose can introduce trophozoites to olfactory nerves."),
        q("Acanthamoeba CNS disease usually presents as:", "Chronic granulomatous amebic encephalitis in immunocompromised hosts", ["Acute flaccid paralysis in children only", "Rapid food poisoning", "Pseudomembrane"], "Acanthamoeba/Balamuthia cause subacute/chronic encephalitis."),
        q("AIDS patient with ring-enhancing brain lesions and positive IgG most likely has:", "Toxoplasma gondii encephalitis", ["Naegleria", "Rabies", "Polio"], "Toxoplasma reactivation causes focal CNS lesions in advanced HIV."),
        q("Toxoplasma infection is acquired from:", "Cat feces oocysts or tissue cysts in undercooked meat", ["Mosquitoes", "Freshwater snails", "Body lice"], "Cats are definitive hosts; humans acquire oocysts or tissue cysts."),
        q("Cryptococcal meningitis in AIDS is diagnosed by:", "CSF cryptococcal antigen or India ink capsule demonstration", ["Widal test", "Weil-Felix", "ASO"], "Cryptococcus has a polysaccharide capsule detected by antigen tests/India ink."),
        q("Cryptococcus neoformans is associated with exposure to:", "Pigeon droppings", ["Raw crab", "Dog bite", "Tick bite"], "Cryptococcus can be found in soil contaminated with pigeon droppings."),
        q("Fungal meningitis usually has CSF pattern of:", "Chronic lymphocytic meningitis with raised protein and low or normal glucose", ["Pure neutrophils with normal protein always", "No cells", "Only RBCs"], "Fungal CNS disease often mimics TB with chronic lymphocytic CSF abnormalities."),
    ]),
]


def main():
    questions = []
    for topic_index, (slug, topic, rows) in enumerate(TOPICS):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        for question_index, row in enumerate(rows, 1):
            options = list(row["wrong"])
            answer_index = (topic_index + question_index - 1) % 4
            options.insert(answer_index, row["answer"])
            questions.append({**BASE, "id": f"micro-cns-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "microbiology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 6 or len(questions) != 60:
        raise AssertionError(f"Expected 6 topics and 60 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 60:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
