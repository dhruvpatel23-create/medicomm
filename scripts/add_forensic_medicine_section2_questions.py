import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "forensic-medicine"
SUBJECT_TITLE = "Forensic Medicine"
SOURCE_PDF = "fmt1"


def sentence_case(text):
    return text[:1].upper() + text[1:] if text else text


def clean_subject(text):
    return re.sub(r"\s+(is|are|was|were|commonly)$", "", text.strip(), flags=re.I)


def polish_prompt(prompt):
    text = re.sub(r"\s+", " ", str(prompt).strip()).rstrip(" .:")
    lower = text.lower()
    if lower.endswith(" is caused by anticholinergic alkaloids such as"):
        return "Which anticholinergic alkaloids cause datura poisoning?"
    if lower.endswith(" is predominantly"):
        subject = clean_subject(text[:-14])
        return f"What is the predominant toxic action of {subject[:1].lower() + subject[1:]}?"
    if lower.endswith(" is commonly associated with"):
        subject = clean_subject(text[:-28])
        return f"What is {subject[:1].lower() + subject[1:]} commonly associated with?"
    if lower.endswith(" is exemplified by"):
        subject = clean_subject(text[:-17])
        return f"What exemplifies {subject[:1].lower() + subject[1:]}?"
    if lower.endswith(" poisoning with"):
        subject = clean_subject(text[:-15])
        return f"{sentence_case(subject)} poisoning with which substance?"
    if lower.endswith(" is seen in"):
        subject = clean_subject(text[:-11])
        return f"{sentence_case(subject)} is seen in what?"
    if lower.endswith(" is found at the"):
        subject = clean_subject(text[:-16])
        return f"{sentence_case(subject)} is found at which site?"
    if lower.endswith(" classically causes"):
        subject = clean_subject(text[:-19])
        return f"What does {subject[:1].lower() + subject[1:]} classically cause?"
    if lower.endswith(" poisoning by"):
        subject = clean_subject(text[:-13])
        return f"{sentence_case(subject)} poisoning by which substance?"
    if lower.endswith(" associated with"):
        subject = clean_subject(text[:-15])
        return f"{sentence_case(subject)} is associated with what?"
    if lower.endswith(" exposure to"):
        subject = clean_subject(text[:-12])
        return f"{sentence_case(subject)} exposure to what?"
    if lower.endswith(" by inhibiting"):
        subject = clean_subject(text[:-13])
        return f"{sentence_case(subject)} by inhibiting which target?"
    if lower.endswith(" to form"):
        subject = clean_subject(text[:-8])
        return f"{sentence_case(subject)} to form what?"
    if lower.endswith(" smells like"):
        subject = clean_subject(text[:-12])
        return f"What does {subject[:1].lower() + subject[1:]} smell like?"
    if lower.endswith(" is primarily a"):
        subject = clean_subject(text[:-15])
        return f"What is {subject[:1].lower() + subject[1:]} primarily?"
    if lower.endswith(" damages the"):
        subject = clean_subject(text[:-12])
        return f"{sentence_case(subject)} damages which structure?"
    if lower.endswith(" commonly causes"):
        subject = clean_subject(text[:-16])
        return f"What does {subject[:1].lower() + subject[1:]} commonly cause?"
    if lower.endswith(" triad of opioid poisoning is"):
        return "What is the classic triad of opioid poisoning?"
    if lower.endswith(" can be reversed by"):
        subject = clean_subject(text[:-19])
        return f"What can reverse {subject[:1].lower() + subject[1:]}?"
    if lower.endswith(" is mainly"):
        subject = clean_subject(text[:-10])
        return f"What is {subject[:1].lower() + subject[1:]} mainly?"
    if lower.endswith(" reuptake of"):
        subject = clean_subject(text[:-10])
        return f"{sentence_case(subject)} reuptake of which neurotransmitters?"
    if lower.endswith(" as"):
        subject = clean_subject(text[:-3])
        return f"What is {subject[:1].lower() + subject[1:]} best classified as?"
    if lower.endswith(" through"):
        subject = clean_subject(text[:-8])
        return f"{sentence_case(subject)} through what mechanism?"
    if lower.endswith(" primarily inhibit"):
        subject = clean_subject(text[:-17])
        return f"What do {subject[:1].lower() + subject[1:]} primarily inhibit?"
    if lower.endswith(" primarily a"):
        subject = clean_subject(text[:-12])
        return f"What is {subject[:1].lower() + subject[1:]} primarily?"
    if lower.endswith(" predominantly"):
        subject = clean_subject(text[:-14])
        return f"What is {subject[:1].lower() + subject[1:]} predominantly?"
    if lower.endswith(" associated with"):
        subject = text[:-15].strip()
        return f"What is {subject[:1].lower() + subject[1:]} associated with?"
    if lower.endswith(" screens for"):
        subject = clean_subject(text[:-12])
        return f"What does {subject[:1].lower() + subject[1:]} screen for?"
    if lower.endswith(" most often results from"):
        subject = clean_subject(text[:-24])
        return f"What does {subject[:1].lower() + subject[1:]} most often result from?"
    if lower.endswith(" is usually due to"):
        subject = clean_subject(text[:-18])
        return f"What is {subject[:1].lower() + subject[1:]} usually due to?"
    if lower.endswith(" is typically"):
        subject = clean_subject(text[:-13])
        return f"What is {subject[:1].lower() + subject[1:]} typically?"
    if lower.endswith(" release of"):
        subject = clean_subject(text[:-11])
        return f"{sentence_case(subject)} release of which neurotransmitter?"
    if lower.endswith(" typically produces"):
        subject = clean_subject(text[:-19])
        return f"What does {subject[:1].lower() + subject[1:]} typically produce?"
    if lower.endswith(" classically linked to"):
        subject = clean_subject(text[:-22])
        return f"What is {subject[:1].lower() + subject[1:]} classically linked to?"
    if lower.endswith(" suggests"):
        subject = clean_subject(text[:-8])
        return f"What does {subject[:1].lower() + subject[1:]} suggest?"
    if lower.endswith(" includes tolerance, craving and"):
        subject = clean_subject(text[:-33])
        return f"{sentence_case(subject)} includes tolerance, craving and what?"
    if lower.endswith(" means"):
        subject = clean_subject(text[:-6])
        return f"What does {subject[:1].lower() + subject[1:]} mean?"
    if lower.endswith(" occur when"):
        subject = clean_subject(text[:-11])
        return f"When do {subject[:1].lower() + subject[1:]} occur?"
    if lower.endswith(" is useful because many drugs or metabolites are"):
        subject = clean_subject(text[:-47])
        return f"Why is {subject[:1].lower() + subject[1:]} useful?"
    if lower.endswith(" commonly uses"):
        subject = clean_subject(text[:-13])
        return f"What does {subject[:1].lower() + subject[1:]} commonly use?"
    if lower.endswith(" important in drug testing because it"):
        subject = clean_subject(text[:-37])
        return f"Why is {subject[:1].lower() + subject[1:]} important in drug testing?"
    if lower.endswith(" best prevented by"):
        subject = clean_subject(text[:-18])
        return f"How is {subject[:1].lower() + subject[1:]} best prevented?"
    if lower.endswith(" exposure"):
        return f"{sentence_case(text)}?"
    if lower.endswith(" may occur through"):
        subject = clean_subject(text[:-18])
        return f"{sentence_case(subject)} may occur through which routes?"
    if lower.endswith(" means measuring"):
        subject = clean_subject(text[:-16])
        return f"What does {subject[:1].lower() + subject[1:]} mean?"
    if lower.endswith(" exposed to"):
        subject = clean_subject(text[:-11])
        return f"{sentence_case(subject)} exposed to which poison?"
    if lower.endswith(" because it affects"):
        subject = clean_subject(text[:-19])
        return f"Why is {subject[:1].lower() + subject[1:]} especially dangerous in children?"
    if lower.endswith(" exposure records"):
        return f"{sentence_case(text)}?"
    if text.endswith(("?", ".")):
        return text
    return f"{text}?"


def q(prompt, answer, wrong, explanation, clinical=False):
    prompt = polish_prompt(prompt)
    options = [answer, *wrong]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {
        "prompt": prompt,
        "options": options,
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "high" if clinical else "moderate",
        "tags": ["clinical"] if clinical else [],
    }


CHAPTERS = [
    ("toxicology-principles-inorganic", "Section 2: Toxicology Principles, Corrosives and Inorganic Poisons", 3, [
        ("toxicology-duties", "General Toxicology: Duties, Samples and Diagnosis", [
            q("In a suspected poisoning case, what is the first duty of the treating doctor?", "Resuscitate and treat the patient", ["Wait for police permission", "Preserve viscera before airway care", "Issue a final opinion immediately"], "Emergency care takes priority; medico-legal documentation and sample preservation follow stabilization."),
            q("Which history is most useful for reconstructing acute poisoning?", "Substance, dose, route, time and treatment already given", ["Only the patient's occupation", "Only the brand of clothes", "Only the place of birth"], "Dose, route and time help predict toxicity, decontamination value and antidote choice."),
            q("Which specimen is especially important in a living case of suspected alcohol or volatile poisoning?", "Blood collected in a sealed container", ["Hair only", "Dry clothing only", "Unsealed vomitus only"], "Blood is central for quantitative alcohol and many volatile poison analyses."),
            q("A patient arrives after unknown tablet ingestion with coma and shallow breathing. What is the immediate priority?", "Airway protection and ventilatory support", ["Detailed handwriting analysis", "Postmortem viscera preservation", "Age estimation by dentition"], "In poisoning, airway, breathing and circulation are managed before specific diagnosis.", True),
            q("Why should vomitus or gastric lavage fluid be preserved in poisoning?", "It may contain unabsorbed poison", ["It proves suicidal intent", "It replaces blood analysis", "It identifies fingerprints better than glass"], "Gastric contents can demonstrate recently ingested poison."),
            q("Which record best protects the evidentiary value of toxicology samples?", "Seal, label and chain-of-custody documentation", ["Verbal handover only", "Unsigned case sheet", "Photograph without sample number"], "A documented chain of custody links the sample to the patient and prevents tampering allegations."),
            q("What is a negative toxicology report best understood to mean?", "The tested poison was not detected by the methods used", ["No poisoning is possible", "Death was natural in every case", "The sample was definitely adequate"], "A negative report must be interpreted with history, sample quality, delay and laboratory scope."),
            q("A pesticide container is found beside an unconscious farmer. His clothes smell of chemical and pupils are pinpoint. What should be sent with biological samples?", "The suspected container or label", ["Only a death certificate", "Only dental chart", "Only a police sketch"], "The container helps identify formulation and guides targeted analysis.", True),
            q("Which feature favors chronic poisoning over acute poisoning?", "Gradual symptoms with repeated exposure history", ["Sudden collapse after one ingestion", "Single contact gunshot wound", "Immediate drowning signs"], "Chronic poisoning develops after repeated or prolonged exposure."),
            q("A hospital discards the first gastric lavage sample after suspected poisoning and sends only later clear washings. What is the main problem?", "Loss of the sample most likely to contain poison", ["Inability to determine sex", "Failure to prove drowning", "Wrong fingerprint pattern"], "The first lavage is usually most concentrated and most useful toxicologically.", True),
        ]),
        ("gastric-decontamination", "Decontamination, Elimination and Antidote Principles", [
            q("When is gastric lavage most justifiable?", "Early presentation after potentially life-threatening ingestion", ["Every poisoning after two days", "Routine corrosive ingestion", "Any alert patient with trivial dose"], "Lavage has limited indications and is weighed against aspiration or perforation risk."),
            q("Which poisoning is a classic contraindication to gastric lavage?", "Strong corrosive ingestion", ["Recent severe barbiturate ingestion with protected airway", "Early iron ingestion under expert care", "Life-threatening ingestion within one hour"], "Corrosives risk perforation and further mucosal injury during lavage."),
            q("Activated charcoal works mainly by what mechanism?", "Adsorption of toxins within the gastrointestinal tract", ["Chemical neutralization of every acid", "Increasing renal filtration directly", "Chelation of all metals"], "Charcoal binds many poisons and reduces absorption if given appropriately."),
            q("A patient took a large sustained-release drug dose 30 minutes ago and is alert. Which decontamination method is most likely to help?", "Activated charcoal if the drug is charcoal-adsorbable", ["Immediate formalin lavage", "Forced drowning test", "No observation needed"], "Early charcoal can reduce absorption of many drug ingestions.", True),
            q("Which substance is poorly adsorbed by activated charcoal?", "Strong acids and alkalis", ["Many sedative drugs", "Tricyclic antidepressants", "Carbamazepine"], "Charcoal is ineffective for corrosives, alcohols, metals and some small molecules."),
            q("Forced alkaline diuresis can enhance elimination of which poison?", "Salicylates", ["Cyanide gas", "Carbon monoxide", "Strong alkali"], "Urinary alkalinization traps weak acids such as salicylate in urine."),
            q("Chelation therapy is used mainly for poisoning by what class of substances?", "Heavy metals", ["Asphyxiant gases only", "Simple alcohol only", "Sharp-force trauma"], "Chelators bind metals and increase elimination."),
            q("A child with lead toxicity is treated with a chelating agent. What is the goal of therapy?", "Bind lead and promote its excretion", ["Increase lead deposition in bone", "Convert lead to cyanide", "Prevent all anemia instantly"], "Chelation reduces toxic metal burden by forming excretable complexes.", True),
            q("An antidote that physiologically antagonizes poison action is exemplified by", "Atropine in organophosphorus poisoning", ["Water after drowning", "Formalin for viscera", "Suturing a laceration"], "Atropine blocks muscarinic effects of excess acetylcholine."),
            q("A patient with severe opioid toxidrome improves rapidly after naloxone. What principle is demonstrated?", "Receptor antagonism by an antidote", ["Chelation of metal", "Mechanical decontamination", "Postmortem diffusion"], "Naloxone competitively antagonizes opioid receptors and reverses respiratory depression.", True),
        ]),
        ("corrosive-acids", "Mineral Acids and Corrosive Acid Poisoning", [
            q("What type of necrosis is produced by strong mineral acids?", "Coagulative necrosis", ["Liquefactive necrosis", "Fat necrosis only", "Caseous necrosis"], "Acids denature proteins and form an eschar that limits deeper penetration compared with alkalis."),
            q("Which acid classically produces yellow staining of skin and mucosa?", "Nitric acid", ["Sulfuric acid", "Hydrochloric acid", "Oxalic acid"], "Nitric acid causes yellow xanthoproteic staining by reacting with proteins."),
            q("Which acid is strongly dehydrating and chars organic material?", "Sulfuric acid", ["Nitric acid", "Acetic acid", "Carbonic acid"], "Sulfuric acid produces brown-black charring due to dehydration."),
            q("A patient has yellow stains around the mouth after ingesting a corrosive liquid. Which acid is most likely?", "Nitric acid", ["Hydrochloric acid", "Oxalic acid", "Sulfurous acid"], "Yellow xanthoproteic staining points toward nitric acid.", True),
            q("Why is alkali ingestion often more deeply destructive than acid ingestion?", "Liquefactive necrosis permits deeper penetration", ["Acids never injure the stomach", "Alkalis only stain skin", "Alkalis are always neutralized by saliva"], "Alkalis dissolve tissue planes and penetrate deeply."),
            q("What is the key danger in attempting blind gastric lavage after corrosive ingestion?", "Perforation of the injured gut", ["Failure to detect fingerprints", "Immediate adipocere formation", "False hyoid fracture"], "Corrosives weaken tissues; instrumentation can perforate esophagus or stomach."),
            q("Which late complication is important after corrosive ingestion?", "Esophageal stricture", ["Hyoid fracture", "Washerwoman changes", "Rifling marks"], "Healing after deep burns can lead to fibrosis and stricture."),
            q("A patient survives acid ingestion but develops progressive dysphagia weeks later. What complication is likely?", "Esophageal stricture", ["Cadaveric spasm", "Carbon monoxide poisoning", "Diatom embolism"], "Corrosive injury heals with scarring that can narrow the esophagus.", True),
            q("Which clinical feature is most urgent after corrosive ingestion?", "Airway edema or respiratory distress", ["Mild skin dryness only", "Old dental caries", "Tattooed fingerprint pattern"], "Upper airway edema can rapidly compromise breathing."),
            q("A child drinks toilet cleaner and has drooling, oral burns and stridor. What should be prioritized?", "Airway assessment and supportive care", ["Forced emesis", "Blind gastric lavage", "Immediate discharge"], "Airway risk is central in corrosive ingestion; vomiting and blind lavage are dangerous.", True),
        ]),
        ("corrosive-alkalis", "Alkalis, Phenol and Household Corrosives", [
            q("What tissue effect is typical of strong alkalis?", "Liquefactive necrosis with deep penetration", ["Coagulative eschar only", "Simple erythema without damage", "Carbon monoxide formation"], "Alkalis saponify fats and dissolve proteins, allowing deep tissue injury."),
            q("Which household exposure commonly causes alkali burns?", "Drain cleaner", ["Table salt", "Glucose powder", "Clean drinking water"], "Drain cleaners may contain sodium or potassium hydroxide."),
            q("Phenol poisoning may produce what characteristic local finding?", "White leathery burns with phenolic odor", ["Yellow xanthoproteic stain", "Cherry-red lividity only", "Washerwoman hands"], "Phenol causes local anesthetic, white leathery corrosive burns and systemic toxicity."),
            q("A factory worker splashes phenol on skin and feels little pain despite white leathery burns. Why can pain be deceptively mild?", "Phenol has local anesthetic action", ["Phenol cannot penetrate skin", "Phenol is only a dye", "Phenol immediately forms adipocere"], "Phenol can numb tissue while causing serious corrosive injury.", True),
            q("What is the safest general approach to corrosive poisoning management?", "Supportive care and early specialist assessment", ["Routine emesis", "Neutralization with strong opposite chemical", "Blind gastric lavage in all patients"], "Management focuses on airway, shock, pain control and endoscopic/surgical assessment."),
            q("Why is chemical neutralization of a swallowed corrosive avoided?", "Exothermic reaction and further injury may occur", ["It always prevents strictures", "It improves chain of custody", "It identifies sex"], "Neutralization can generate heat and worsen tissue damage."),
            q("Which finding suggests antemortem corrosive ingestion at autopsy?", "Inflamed eroded mucosa with vital reaction", ["Only postmortem drying", "Clean cut skin margins", "Rifling grooves"], "Vital inflammation supports injury during life."),
            q("A patient ingests caustic soda and develops severe retrosternal pain and drooling. Which tissue injury is expected?", "Liquefactive necrosis of upper gastrointestinal mucosa", ["Coagulative necrosis limited to lips only", "Mechanical hyoid fracture", "Pulmonary diatoms"], "Caustic soda is an alkali and penetrates deeply through liquefactive necrosis.", True),
            q("What should be preserved when household corrosive poisoning is alleged?", "Container, remaining fluid and biological samples", ["Only a skull x-ray", "Only footwear", "Only fingerprint powder"], "Source material helps confirm the corrosive and concentration."),
            q("A bathroom cleaner bottle and gastric contents are sent separately with seals and labels. What is the forensic value?", "Correlation of suspected source with biological evidence", ["Proof of drowning", "Determination of stature", "Proof of firearm range"], "Matching the container contents with patient samples strengthens the toxicological reconstruction.", True),
        ]),
        ("arsenic", "Arsenic and Irritant Metallic Poisons", [
            q("Acute arsenic poisoning commonly resembles which illness?", "Acute gastroenteritis", ["Meningitis only", "Myocardial infarction only", "Rabies"], "Vomiting, abdominal pain and rice-water diarrhea can mimic gastroenteritis."),
            q("Which chronic skin finding is associated with arsenic poisoning?", "Raindrop pigmentation and hyperkeratosis", ["Cherry-red lividity", "Lichtenberg figures", "Washerwoman hands"], "Chronic arsenic causes pigmentary changes and palmar-plantar hyperkeratosis."),
            q("Mees lines are classically seen in poisoning with", "Arsenic", ["Carbon monoxide", "Alcohol", "Cannabis"], "Transverse white nail lines may follow arsenic or other systemic insults."),
            q("A person develops severe vomiting, rice-water stools, hypotension and garlic odor after suspected poison ingestion. Which poison is likely?", "Arsenic", ["Phenol", "Morphine", "Lead"], "Acute arsenic causes severe GI irritation and may have garlic odor.", True),
            q("Which sample is useful for detecting chronic arsenic exposure?", "Hair and nails", ["Only expired air", "Only fingerprints", "Only cerebrospinal fluid in all cases"], "Arsenic is deposited in keratin-rich tissues over time."),
            q("Why can arsenic poisoning be confused with cholera?", "Profuse watery diarrhea and dehydration", ["Pinpoint pupils alone", "Contact burns", "Hyoid fracture"], "The GI presentation of acute arsenic can resemble cholera."),
            q("Which antidotal approach is used for significant arsenic poisoning?", "Chelation therapy", ["Naloxone alone", "Atropine alone", "Pure oxygen only"], "Chelators such as dimercaprol or succimer may be used depending on setting."),
            q("A chronically exposed smelter worker has neuropathy, palmar hyperkeratosis and transverse white nail lines. What exposure is suggested?", "Arsenic", ["Carbon monoxide", "Cyanide", "Kerosene"], "Skin changes, neuropathy and Mees lines support chronic arsenic exposure.", True),
            q("What type of poison is arsenic trioxide classically considered?", "Irritant metallic poison", ["Mechanical poison", "Simple asphyxiant", "Deliriant plant poison"], "Arsenic is a metallic irritant poison with GI and systemic effects."),
            q("A suspected arsenic death is exhumed months after burial. Why may analysis still be useful?", "Arsenic can persist in hair, nails and tissues", ["Arsenic evaporates completely", "Only fresh blood is useful", "Arsenic destroys all bones"], "Arsenic is relatively stable and can be detected long after death.", True),
        ]),
        ("lead", "Lead Poisoning", [
            q("Chronic lead poisoning commonly affects which system?", "Hematopoietic and nervous systems", ["Only hair follicles", "Only fingerprints", "Only dental enamel"], "Lead interferes with heme synthesis and damages peripheral and central nerves."),
            q("Basophilic stippling in lead poisoning is seen in", "Red blood cells", ["Neutrophils only", "Platelets only", "Hepatocytes only"], "Lead inhibits enzymes in heme synthesis and causes ribosomal RNA aggregation."),
            q("Burtonian line is found at the", "Gum margin", ["Cornea", "Palm crease", "Sole"], "A blue line may appear on gums due to lead sulfide deposition."),
            q("A battery worker has abdominal colic, wrist drop, anemia and blue gum line. Which poisoning is likely?", "Lead poisoning", ["Arsenic poisoning", "Cyanide poisoning", "Phenol poisoning"], "Occupational exposure plus colic, neuropathy and Burtonian line suggest lead.", True),
            q("Lead palsy classically causes", "Wrist drop", ["Foot gangrene only", "Facial burns", "Hyoid fracture"], "Radial nerve involvement causes extensor weakness and wrist drop."),
            q("Which enzyme inhibition contributes to anemia in lead poisoning?", "Ferrochelatase and ALA dehydratase inhibition", ["Acetylcholinesterase activation", "Cytochrome oxidase activation", "Alcohol dehydrogenase excess"], "Lead impairs heme synthesis by inhibiting these enzymes."),
            q("Which investigation helps support lead exposure?", "Blood lead level", ["Diatom test", "Bullet rifling comparison", "Cephalic index"], "Blood lead level is central for diagnosis and severity assessment."),
            q("A child with pica has developmental delay, anemia and abdominal pain. X-ray shows dense metaphyseal bands. What is the likely poison?", "Lead", ["Mercury", "Cannabis", "Oxalic acid"], "Children with pica can ingest lead paint; metaphyseal lead lines support exposure.", True),
            q("Which chelator is used in severe lead poisoning?", "Calcium disodium EDTA", ["Naloxone", "Flumazenil only", "Atropine only"], "EDTA and other chelators increase lead elimination in selected cases."),
            q("A painter with chronic exposure develops wrist drop and anemia with basophilic stippling. What mechanism explains the anemia?", "Impaired heme synthesis", ["Massive hemolysis from ABO antibodies", "Surfactant deficiency", "Cyanide-mediated histotoxic hypoxia"], "Lead blocks heme synthesis enzymes and causes anemia.", True),
        ]),
        ("mercury", "Mercury Poisoning", [
            q("Erethism is a feature of chronic poisoning by", "Mercury", ["Lead", "Carbon monoxide", "Oxalic acid"], "Chronic mercury exposure can cause behavioral change, irritability and tremor."),
            q("Which triad suggests chronic mercury poisoning?", "Tremor, gingivitis and erethism", ["Miosis, bronchorrhea and fasciculations", "Cherry-red lividity and headache", "Yellow staining and dysphagia"], "Mercury affects nervous system and gums."),
            q("Acrodynia in children is associated with", "Mercury exposure", ["Cyanide exposure", "Drowning", "Hanging"], "Pink disease or acrodynia is linked to mercury sensitivity/exposure."),
            q("A thermometer factory worker develops tremor, excessive salivation, gum inflammation and personality change. Which poison is likely?", "Mercury", ["Lead", "Arsenic", "Carbon monoxide"], "Occupational mercury exposure produces tremor, gingivitis and erethism.", True),
            q("Minamata disease was caused by exposure to", "Methyl mercury", ["Ethyl alcohol", "Cyanide gas", "Sulfuric acid"], "Industrial methyl mercury contamination caused severe neurologic disease."),
            q("Which organ system is especially affected by organic mercury?", "Central nervous system", ["Only skin epidermis", "Only hyoid bone", "Only dental enamel"], "Organic mercury is neurotoxic and crosses the blood-brain barrier."),
            q("What is mercurial tremor classically described as?", "Fine tremor progressing to coarse intention tremor", ["Absent tendon reflexes only", "Pure sensory loss only", "Instant paralysis"], "Tremor is a hallmark of chronic mercury toxicity."),
            q("A fishing-community outbreak shows ataxia, constricted visual fields and fetal neurodevelopmental harm after contaminated seafood. What toxin is implicated?", "Methyl mercury", ["Lead acetate", "Phenol", "Oxalic acid"], "Methyl mercury biomagnifies in fish and injures nervous tissue.", True),
            q("Which sample may help in chronic mercury assessment?", "Urine for inorganic mercury exposure", ["Only breath for all forms", "Diatoms in marrow", "Ligature mark swab"], "Urine is useful for inorganic mercury exposure monitoring."),
            q("A chronically exposed worker has gum changes, salivation and behavioral irritability. Which classic syndrome is present?", "Erethism with mercurialism", ["Cafe coronary", "Immersion syndrome", "Burking"], "Personality and behavioral changes are part of chronic mercurialism.", True),
        ]),
        ("phosphorus", "Phosphorus and Related Irritant Poisons", [
            q("Yellow phosphorus is classically associated with which odor?", "Garlic odor", ["Bitter almond only", "Phenolic odor", "Kerosene odor"], "Phosphorus may impart a garlic-like odor to breath or vomitus."),
            q("Which organ is severely affected in phosphorus poisoning?", "Liver", ["Only hyoid bone", "Only dental pulp", "Only cornea"], "Phosphorus is hepatotoxic and can cause fatty degeneration and liver failure."),
            q("What is luminous vomitus associated with?", "Phosphorus poisoning", ["Lead poisoning", "Carbon monoxide poisoning", "Alcohol intoxication"], "Phosphorescence may be seen in vomitus in yellow phosphorus poisoning."),
            q("A person ingests rat paste and develops vomiting with garlic odor followed by jaundice and hepatic failure. Which poison is likely?", "Yellow phosphorus", ["Lead", "Mercury", "Cannabis"], "Rat paste poisoning with delayed liver failure is typical of yellow phosphorus.", True),
            q("Which phase may occur after initial gastrointestinal symptoms in phosphorus poisoning?", "A deceptive symptom-free period", ["Immediate skeletonization", "Instant hyoid fracture", "Permanent immunity"], "A latent period can precede hepatic and systemic deterioration."),
            q("Why is phosphorus poisoning dangerous even after early symptoms settle?", "Delayed hepatic failure may develop", ["It always becomes non-toxic", "It only affects skin color", "It prevents absorption"], "Clinical improvement may be followed by severe liver injury."),
            q("Which postmortem finding may be seen in phosphorus poisoning?", "Fatty degeneration of liver", ["Washerwoman hands only", "Rifling marks", "Ligature groove"], "Phosphorus causes fatty change and hepatic necrosis."),
            q("A patient with suspected yellow phosphorus ingestion has early vomiting but feels better after a day. What concern remains?", "Delayed liver injury", ["No further toxicity possible", "Only dental staining", "Only firearm injury"], "The latent phase can be followed by hepatic failure.", True),
            q("Which product is an important modern source of yellow phosphorus poisoning in some settings?", "Rodenticide paste", ["Ink eraser only", "Toothpaste", "Normal saline"], "Rat killer paste may contain yellow phosphorus."),
            q("A suspected rat-paste poisoning case requires serial monitoring of which function?", "Liver function", ["Hearing threshold only", "Cephalic index", "Fingerprint ridge count"], "Hepatic injury determines severity and prognosis.", True),
        ]),
        ("cyanide-co", "Cyanide, Carbon Monoxide and Asphyxiant Gases", [
            q("Cyanide causes death primarily by inhibiting", "Cytochrome oxidase", ["Acetylcholinesterase only", "Ferrochelatase only", "Alcohol dehydrogenase"], "Cyanide blocks cellular respiration and causes histotoxic hypoxia."),
            q("Which odor may be associated with cyanide?", "Bitter almond odor", ["Garlic odor", "Phenolic odor", "Rotten egg in every case"], "Some people can detect bitter almond odor, but not all."),
            q("Carbon monoxide binds hemoglobin to form", "Carboxyhemoglobin", ["Methemoglobin only", "Sulfhemoglobin only", "Oxyhemoglobin only"], "CO has high affinity for hemoglobin and impairs oxygen delivery."),
            q("A family sleeping in a closed room with a faulty heater develops headache and confusion; one person dies. Which poison is most likely?", "Carbon monoxide", ["Cyanide salt", "Lead", "Phenol"], "Incomplete combustion in enclosed spaces produces CO.", True),
            q("Which color of lividity is classically linked to carbon monoxide poisoning?", "Cherry red", ["Green", "Dark brown only", "Yellow"], "Carboxyhemoglobin can produce bright cherry-red blood and lividity."),
            q("What is the main treatment principle in carbon monoxide poisoning?", "High-flow oxygen or hyperbaric oxygen when indicated", ["Atropine alone", "Chelation with EDTA", "Forced emesis"], "Oxygen accelerates dissociation of carbon monoxide from hemoglobin."),
            q("Hydrogen sulfide classically smells like", "Rotten eggs", ["Bitter almonds", "Phenol", "Kerosene"], "H2S may smell of rotten eggs, though olfactory fatigue can occur."),
            q("A worker cleaning a sewer collapses suddenly with rotten-egg odor at the site. Which gas is likely?", "Hydrogen sulfide", ["Carbon dioxide only", "Nitric acid vapor", "Oxygen"], "Sewer gas exposure can cause rapid H2S toxicity.", True),
            q("Which mechanism best explains cyanide toxicity?", "Cells cannot utilize oxygen despite adequate oxygen delivery", ["Blood cannot clot", "Skin undergoes mummification", "Bone marrow produces diatoms"], "Cyanide produces histotoxic hypoxia by blocking oxidative phosphorylation."),
            q("A laboratory worker exposed to cyanide collapses rapidly with seizures and severe lactic acidosis. What is the immediate toxic mechanism?", "Histotoxic hypoxia", ["Liquefactive corrosion", "Mechanical asphyxia", "Lead colic"], "Failure of cellular oxygen use leads to rapid collapse and lactic acidosis.", True),
        ]),
        ("alcohols", "Ethyl Alcohol and Toxic Alcohols", [
            q("Ethyl alcohol is primarily a", "Central nervous system depressant", ["Strong corrosive", "Metallic irritant", "Mechanical poison"], "Ethanol depresses cortical and brainstem function in a dose-dependent manner."),
            q("Which enzyme converts ethanol to acetaldehyde?", "Alcohol dehydrogenase", ["Acetylcholinesterase", "Cytochrome oxidase", "Ferrochelatase"], "Alcohol dehydrogenase catalyzes the first step of ethanol metabolism."),
            q("What specimen is preferred for quantitative alcohol analysis in medico-legal cases?", "Blood", ["Dry hair only", "Fingerprints", "Ligature material only"], "Blood alcohol concentration is the standard quantitative measure."),
            q("A driver smells of alcohol, has slurred speech and impaired coordination after a crash. Which test best quantifies intoxication?", "Blood alcohol concentration", ["Diatom test", "Dental charting", "Hyoid x-ray"], "BAC provides objective quantification in medico-legal alcohol assessment.", True),
            q("Methanol poisoning characteristically damages the", "Optic nerve and retina", ["Hyoid bone", "Skin ridges", "Dental pulp only"], "Formic acid from methanol metabolism causes visual toxicity and acidosis."),
            q("Ethylene glycol poisoning commonly causes", "Metabolic acidosis and renal injury", ["Cherry-red lividity only", "Erethism", "Yellow xanthoproteic staining"], "Oxalate metabolites injure kidneys and cause acidosis."),
            q("Which treatment blocks toxic metabolite formation in methanol poisoning?", "Fomepizole", ["Atropine", "Naloxone", "EDTA"], "Fomepizole inhibits alcohol dehydrogenase."),
            q("A patient develops blurred vision, abdominal pain and severe metabolic acidosis after illicit liquor. Which poisoning is likely?", "Methanol", ["Ethanol alone", "Lead", "Mercury"], "Visual symptoms and acidosis after illicit alcohol suggest methanol.", True),
            q("Why can postmortem alcohol interpretation be difficult?", "Alcohol may be produced by decomposition", ["Alcohol cannot be measured", "Alcohol always evaporates instantly", "Alcohol proves homicide"], "Putrefaction can generate ethanol, complicating interpretation."),
            q("A patient has flank pain, acidosis and calcium oxalate crystals after ingesting antifreeze. Which poison is likely?", "Ethylene glycol", ["Methanol", "Phenol", "Arsenic"], "Ethylene glycol metabolites produce oxalate crystals and renal failure.", True),
        ]),
    ]),
    ("organic-drug-agricultural-poisons", "Section 2: Organic, Drug, Agricultural and Animal Poisons", 4, [
        ("opioids", "Opioids and Sedative-Hypnotic Poisons", [
            q("The classic triad of opioid poisoning is", "Coma, pinpoint pupils and respiratory depression", ["Fever, rash and arthritis", "Jaundice, tremor and gum line", "Hyperthermia, dry skin and mydriasis"], "Opioids depress respiratory centers and produce miosis and coma."),
            q("Which antidote reverses opioid toxicity?", "Naloxone", ["Atropine", "Pralidoxime", "EDTA"], "Naloxone is an opioid receptor antagonist."),
            q("Barbiturate poisoning primarily causes", "Central nervous system and respiratory depression", ["Liquefactive burns", "Metallic gum line", "Diatom embolism"], "Sedative-hypnotics depress brain function and ventilation."),
            q("A young adult is found unconscious with slow breathing, cyanosis and pinpoint pupils beside injection paraphernalia. Which antidote is indicated?", "Naloxone", ["Pralidoxime", "Dimercaprol", "Calcium gluconate"], "The opioid toxidrome with respiratory depression is treated with naloxone.", True),
            q("Which feature helps distinguish opioid poisoning from organophosphorus poisoning?", "Absence of marked bronchorrhea and fasciculations", ["Pinpoint pupils alone", "Coma alone", "History of collapse"], "Both may cause miosis, but cholinergic secretions and fasciculations suggest OP poisoning."),
            q("What is the major cause of death in opioid overdose?", "Respiratory depression", ["Esophageal stricture", "Renal colic", "Hyoid fracture"], "Fatal opioid toxicity is usually due to hypoventilation and hypoxia."),
            q("Which drug can precipitate withdrawal in an opioid-dependent patient?", "Naloxone", ["Activated charcoal", "Vitamin K", "Oxygen"], "Naloxone rapidly displaces opioids and can trigger acute withdrawal."),
            q("A poisoned patient improves after naloxone but becomes drowsy again two hours later. What is the likely reason?", "Naloxone duration is shorter than the opioid", ["Naloxone caused lead toxicity", "The diagnosis must be drowning", "Antidotes never need repeat dosing"], "Long-acting opioids may outlast naloxone, requiring observation and repeat dosing.", True),
            q("Benzodiazepine overdose can be reversed by", "Flumazenil", ["Naloxone", "Atropine", "Pralidoxime"], "Flumazenil antagonizes benzodiazepine receptors but is used cautiously."),
            q("A patient with mixed unknown overdose has seizures after flumazenil. Why is flumazenil used cautiously?", "It can precipitate seizures in dependent or mixed-overdose patients", ["It causes corrosive burns", "It chelates calcium", "It produces cyanide"], "Flumazenil may be dangerous in benzodiazepine dependence or proconvulsant co-ingestion.", True),
        ]),
        ("cannabis-cocaine", "Cannabis, Cocaine and Stimulants", [
            q("Cannabis intoxication commonly causes", "Euphoria, altered perception and conjunctival congestion", ["Profuse bronchorrhea and miosis", "Blue gum line", "Deep corrosive burns"], "Cannabis affects perception, mood and coordination."),
            q("The active principle of cannabis is mainly", "Delta-9-tetrahydrocannabinol", ["Morphine", "Atropine", "Nicotine"], "THC is the principal psychoactive cannabinoid."),
            q("Cocaine causes toxicity mainly by blocking reuptake of", "Catecholamines", ["Acetylcholine only", "Calcium only", "Lead ions"], "Cocaine increases synaptic catecholamines, causing sympathetic excess."),
            q("A partygoer has agitation, hypertension, tachycardia, dilated pupils and chest pain after snorting a white powder. Which drug is likely?", "Cocaine", ["Opium", "Lead", "Phenol"], "Cocaine produces a sympathomimetic toxidrome and can cause myocardial ischemia.", True),
            q("Which serious cardiac complication is associated with cocaine?", "Myocardial ischemia and arrhythmia", ["Esophageal stricture only", "Basophilic stippling", "Hyoid fracture"], "Coronary vasospasm and sympathetic stimulation can cause ischemia and arrhythmias."),
            q("Amphetamine intoxication resembles which toxidrome?", "Sympathomimetic toxidrome", ["Cholinergic toxidrome", "Opioid toxidrome", "Corrosive syndrome"], "Stimulants cause agitation, tachycardia, hypertension and hyperthermia."),
            q("Which finding favors stimulant overdose over opioid overdose?", "Mydriasis with agitation", ["Pinpoint pupils with coma", "Respiratory depression alone", "Slow pulse and hypothermia"], "Stimulants activate the sympathetic system; opioids depress respiration and constrict pupils."),
            q("A student using amphetamine tablets develops severe agitation, hyperthermia, sweating and hypertension. What is the toxidrome?", "Sympathomimetic toxicity", ["Opioid toxicity", "Metallic irritant poisoning", "Corrosive poisoning"], "Amphetamines produce sympathetic excess and dangerous hyperthermia.", True),
            q("Cannabis use can impair driving mainly by affecting", "Reaction time, attention and coordination", ["Heme synthesis", "Hyoid bone strength", "Gastric corrosion"], "Psychomotor impairment is medico-legally important in driving."),
            q("A driver with red eyes, slowed reaction time and impaired coordination tests positive for THC. What is the forensic relevance?", "Drug-impaired driving", ["Drowning", "Lead colic", "Mercury erethism"], "Cannabis-related psychomotor impairment can affect driving ability.", True),
        ]),
        ("anticholinergic-deliriants", "Anticholinergic and Deliriant Poisons", [
            q("Datura poisoning is caused by anticholinergic alkaloids such as", "Atropine and scopolamine", ["Morphine and codeine", "Lead and mercury", "Cyanide and sulfide"], "Datura contains tropane alkaloids with antimuscarinic effects."),
            q("Which pupil finding is typical of anticholinergic poisoning?", "Dilated pupils", ["Pinpoint pupils", "Irregular postmortem pupils only", "No pupillary effect"], "Antimuscarinic action causes mydriasis and blurred vision."),
            q("Which clinical pattern suggests anticholinergic toxicity?", "Dry hot skin, mydriasis, delirium and urinary retention", ["Salivation, lacrimation and miosis", "Cherry-red lividity", "Blue gum line"], "Anticholinergic poisoning produces dryness, hyperthermia, delirium and retention."),
            q("A child eats datura seeds and develops dry mouth, flushed skin, dilated pupils, fever and delirium. What poisoning is likely?", "Datura poisoning", ["Opioid poisoning", "Organophosphorus poisoning", "Arsenic poisoning"], "Datura produces a classic anticholinergic toxidrome.", True),
            q("Which feature distinguishes anticholinergic poisoning from organophosphorus poisoning?", "Dry skin and absent secretions", ["Miosis and salivation", "Bronchorrhea", "Fasciculations"], "OP poisoning is wet and cholinergic; anticholinergic toxicity is dry."),
            q("Which antidote may be considered in severe anticholinergic poisoning under expert care?", "Physostigmine", ["Naloxone", "Pralidoxime", "EDTA"], "Physostigmine increases acetylcholine centrally and peripherally but has risks."),
            q("Datura seeds are important medico-legally because they may be used for", "Stupefying or robbery", ["Confirming drowning", "Estimating stature", "Firearm matching"], "Deliriant effects can incapacitate victims."),
            q("A traveler becomes delirious after accepting food from a stranger; he has dry mouth, mydriasis and urinary retention. What criminal use is suggested?", "Stupefying with datura", ["Burking", "Lead adulteration", "Carbon monoxide exposure"], "Datura may be used to stupefy victims for robbery.", True),
            q("What is the expected skin condition in anticholinergic poisoning?", "Hot and dry", ["Cold and wet with bronchorrhea", "Yellow and corrosively stained", "Cherry red from CO only"], "Sweating is reduced due to muscarinic blockade."),
            q("A patient with delirium, hyperthermia and dry axillae is misdiagnosed as organophosphorus poisoning. Which finding argues against OP poisoning?", "Dryness of secretions", ["Altered sensorium", "Tachycardia", "History uncertainty"], "OP poisoning typically causes excessive secretions rather than dryness.", True),
        ]),
        ("organophosphorus", "Organophosphorus and Carbamate Insecticides", [
            q("Organophosphorus compounds inhibit", "Acetylcholinesterase", ["Cytochrome oxidase", "Ferrochelatase", "Alcohol dehydrogenase"], "OP compounds cause accumulation of acetylcholine at synapses."),
            q("Which muscarinic feature is typical of OP poisoning?", "Bronchorrhea", ["Dry mouth", "Mydriasis", "Urinary retention"], "Muscarinic excess causes secretions, bronchospasm, bradycardia and miosis."),
            q("Which nicotinic feature may occur in OP poisoning?", "Fasciculations", ["Blue gum line", "Yellow staining", "Cherry-red lividity"], "Nicotinic receptor stimulation causes fasciculations and weakness."),
            q("A farmer presents with miosis, salivation, bronchorrhea, wheeze and fasciculations after spraying pesticide. What is the diagnosis?", "Organophosphorus poisoning", ["Datura poisoning", "Methanol poisoning", "Lead poisoning"], "The cholinergic toxidrome after pesticide exposure is typical of OP poisoning.", True),
            q("Atropine treats which component of OP poisoning?", "Muscarinic effects", ["Aging of enzyme directly", "Nicotinic weakness fully", "All seizures alone"], "Atropine blocks muscarinic receptors and dries secretions."),
            q("Pralidoxime is most useful before", "Aging of phosphorylated acetylcholinesterase", ["Development of lividity", "Dental eruption", "Adipocere formation"], "Oximes reactivate cholinesterase before the OP-enzyme bond becomes irreversible."),
            q("Intermediate syndrome in OP poisoning involves", "Weakness of neck, respiratory and proximal limb muscles", ["Delayed esophageal stricture", "Blue gum line", "Washerwoman hands"], "Intermediate syndrome can cause respiratory failure after initial cholinergic crisis."),
            q("An OP-poisoned patient improves after atropine but later develops neck flexor and respiratory muscle weakness. What syndrome is this?", "Intermediate syndrome", ["Cafe coronary", "Erethism", "Burking"], "Intermediate syndrome appears after acute crisis and may require ventilatory support.", True),
            q("Carbamates differ from many OP compounds because cholinesterase inhibition is usually", "Reversible and shorter acting", ["Always permanent", "Unrelated to acetylcholine", "Only corrosive"], "Carbamates carbamylate cholinesterase reversibly."),
            q("A pesticide-poisoned patient has pinpoint pupils and massive secretions. What bedside endpoint suggests adequate atropinization?", "Drying of bronchial secretions with improved ventilation", ["Persistent bronchorrhea", "Development of gum line", "Appearance of diatoms"], "Atropine dosing is guided clinically by drying secretions and respiratory improvement.", True),
        ]),
        ("organochlorine-pyrethroid", "Organochlorines, Pyrethroids and Herbicides", [
            q("Organochlorine insecticides are important because they are", "Persistent and bioaccumulative", ["Rapidly destroyed in seconds", "Purely corrosive", "Always harmless to humans"], "Many organochlorines persist in environment and accumulate in fat."),
            q("DDT is an example of", "Organochlorine insecticide", ["Organophosphorus compound", "Opioid", "Heavy metal"], "DDT is a classic organochlorine."),
            q("Organochlorine poisoning commonly causes", "CNS stimulation and seizures", ["Profuse cholinergic secretions only", "Blue gum line", "Esophageal stricture"], "These compounds can produce neurologic excitation."),
            q("A child develops seizures after accidental exposure to an old pesticide powder stored at home. The compound is suspected to be DDT. What class is it?", "Organochlorine", ["Carbamate", "Opioid", "Corrosive alkali"], "DDT belongs to organochlorine insecticides.", True),
            q("Pyrethroid exposure commonly produces", "Paresthesia and irritant symptoms", ["Burtonian line", "Methyl mercury syndrome", "Diatoms in marrow"], "Pyrethroids often cause sensory irritation and mild neurologic symptoms."),
            q("Paraquat poisoning is feared because it causes", "Progressive pulmonary fibrosis", ["Instant hyoid fracture", "Only reversible miosis", "Dental erosion only"], "Paraquat selectively accumulates in lungs and causes oxidative injury."),
            q("What is the key target organ in severe paraquat poisoning?", "Lung", ["Hyoid bone", "Dental pulp", "Fingerprints"], "Fatal paraquat poisoning often involves progressive lung injury."),
            q("A patient ingests herbicide and later develops severe hypoxia with progressive pulmonary fibrosis. Which poison is likely?", "Paraquat", ["DDT", "Cannabis", "Lead"], "Paraquat poisoning causes delayed lung fibrosis and respiratory failure.", True),
            q("Why is dermal decontamination important after pesticide exposure?", "Ongoing skin absorption can continue toxicity", ["It proves manner of death", "It replaces airway care", "It creates antidote"], "Removing contaminated clothing and washing skin reduce further absorption."),
            q("A farm worker spills pesticide on clothes and continues working for hours before cholinergic symptoms develop. What should be done early?", "Remove contaminated clothing and wash skin", ["Keep clothes sealed on body", "Induce vomiting only", "Ignore dermal exposure"], "Dermal absorption is clinically important in pesticide poisoning.", True),
        ]),
        ("plant-cardiac", "Plant Poisons: Cardiac and Irritant Plants", [
            q("Oleander contains cardiac glycosides that act like", "Digitalis", ["Morphine", "Atropine", "Cyanide"], "Oleander glycosides inhibit Na+/K+-ATPase and can cause arrhythmias."),
            q("Which ECG problem is feared in oleander poisoning?", "Serious arrhythmias", ["Only sinus tachycardia in all cases", "No cardiac effect", "Hyoid fracture"], "Cardiac glycosides can produce bradyarrhythmias and ventricular arrhythmias."),
            q("Abrus precatorius seeds contain", "Abrin", ["Ricin", "Nicotine", "Atropine"], "Abrus seeds contain the toxalbumin abrin."),
            q("A patient develops vomiting and dangerous bradyarrhythmia after ingesting yellow oleander seeds. Which poison is likely?", "Cardiac glycosides", ["Opioid alkaloids", "Lead salts", "Phenol"], "Yellow oleander ingestion causes cardiac glycoside toxicity.", True),
            q("Ricin is derived from", "Castor bean", ["Datura seed", "Opium poppy", "Oleander leaf"], "Ricin is a toxalbumin from Ricinus communis."),
            q("Toxalbumins primarily inhibit", "Protein synthesis", ["Acetylcholinesterase only", "Alcohol metabolism", "Heme synthesis only"], "Ricin and abrin inactivate ribosomes and inhibit protein synthesis."),
            q("Which plant poison is historically used in cattle poison and homicidal preparations after seed decortication?", "Abrus precatorius", ["Cannabis sativa", "Papaver somniferum", "Datura alba"], "Abrus seeds become more dangerous when the hard coat is broken."),
            q("A crushed rosary pea seed is injected into a puncture wound, followed by severe local reaction and systemic toxicity. Which toxin is involved?", "Abrin", ["Nicotine", "THC", "Methanol"], "Abrus precatorius seeds contain abrin, a potent toxalbumin.", True),
            q("Calotropis latex is mainly a", "Irritant plant poison", ["Simple asphyxiant", "Pure opioid", "Heavy metal"], "Calotropis latex irritates skin, eyes and mucosa."),
            q("A child develops oral burning, vomiting and mucosal irritation after chewing an irritant garden plant. Which class best fits?", "Irritant plant poisoning", ["Opioid poisoning", "Carbon monoxide poisoning", "Lead palsy"], "Many plant saps and seeds cause local irritation and gastrointestinal symptoms.", True),
        ]),
        ("animal-bites", "Snakebite and Animal Poisons", [
            q("Cobra venom is predominantly", "Neurotoxic", ["Purely nephrotoxic only", "Only corrosive", "Only sedative"], "Elapid venoms commonly cause neuromuscular paralysis."),
            q("Viper venom is commonly associated with", "Hemotoxicity and coagulopathy", ["Pure anticholinergic delirium", "Only optic neuritis", "Only cannabis-like euphoria"], "Viper bites can cause bleeding, shock, renal injury and clotting abnormalities."),
            q("The 20-minute whole blood clotting test screens for", "Coagulopathy in snakebite", ["Blood alcohol", "Diatoms", "Lead level"], "Failure to clot suggests venom-induced consumption coagulopathy."),
            q("A snakebite victim has ptosis, dysphagia and respiratory weakness with minimal local swelling. Which venom effect is likely?", "Neurotoxicity", ["Corrosive necrosis", "Lead neuropathy", "Carbon monoxide hypoxia"], "Elapid neurotoxicity affects neuromuscular transmission and respiration.", True),
            q("What is the definitive treatment for systemic venomous snakebite?", "Appropriate anti-snake venom", ["Atropine alone", "Naloxone alone", "Forced emesis"], "Antivenom neutralizes circulating venom when indicated."),
            q("Which first-aid measure is harmful in snakebite?", "Cutting and suction of the bite wound", ["Immobilization", "Rapid transport", "Reassurance"], "Incision and suction increase injury and do not reliably remove venom."),
            q("Scorpion sting commonly causes serious toxicity through", "Autonomic storm", ["Heme synthesis blockade", "Liquefactive GI burns", "Diatom embolism"], "Severe scorpion envenomation causes autonomic effects and myocarditis/pulmonary edema."),
            q("A child after scorpion sting has sweating, salivation, hypertension and pulmonary edema. Which drug is classically useful in many protocols?", "Prazosin", ["Naloxone", "EDTA", "Pralidoxime"], "Prazosin counteracts alpha-adrenergic effects in severe scorpion sting.", True),
            q("Bee sting fatality most often results from", "Anaphylaxis", ["Lead colic", "Methyl mercury toxicity", "Datura delirium"], "Hypersensitivity reactions can rapidly cause airway compromise and shock."),
            q("A person collapses with wheeze, urticaria and hypotension minutes after multiple bee stings. What is the immediate concern?", "Anaphylactic shock", ["Chronic arsenic poisoning", "Carbon monoxide poisoning", "Opioid overdose"], "Rapid allergic reaction after stings requires emergency anaphylaxis treatment.", True),
        ]),
        ("food-poisoning", "Food Poisoning and Bacterial Toxins", [
            q("Staphylococcal food poisoning is usually due to", "Preformed enterotoxin", ["Invasion of blood in every case", "Cyanide formation", "Lead contamination"], "Preformed toxin causes rapid vomiting after contaminated food."),
            q("The incubation period in staphylococcal food poisoning is typically", "Short, often a few hours", ["Several weeks", "Months", "Years"], "Preformed toxin causes rapid onset."),
            q("Botulism causes paralysis by blocking release of", "Acetylcholine", ["Dopamine only", "Lead ions", "Carboxyhemoglobin"], "Botulinum toxin prevents acetylcholine release at neuromuscular junctions."),
            q("Several people develop vomiting within 3 hours of eating cream pastries at a function. Which toxin is likely?", "Staphylococcal enterotoxin", ["Botulinum toxin", "Lead", "Datura"], "Rapid vomiting after dairy/cream food suggests preformed staphylococcal toxin.", True),
            q("Botulism typically produces", "Descending flaccid paralysis", ["Ascending spastic paralysis", "Severe corrosive burns", "Blue gum line"], "Cranial nerve involvement and descending weakness are typical."),
            q("Which food source is classically linked to botulism?", "Improperly canned food", ["Fresh boiled water", "Plain sugar", "Sterile saline"], "Anaerobic storage can allow Clostridium botulinum toxin production."),
            q("Mushroom poisoning with delayed severe hepatic failure suggests", "Amanita phalloides", ["Cannabis", "Datura only", "Oleander"], "Amanita toxins can cause delayed liver failure after initial GI symptoms."),
            q("A patient develops GI upset after wild mushrooms, improves briefly, then develops jaundice and liver failure. Which mushroom is likely?", "Amanita phalloides", ["Psilocybin mushroom only", "Edible button mushroom", "Datura"], "Amanita poisoning has a latent period followed by hepatic injury.", True),
            q("Which feature suggests preformed toxin food poisoning?", "Rapid onset vomiting after shared food", ["Symptoms only after years", "No relation to meals", "Only hyoid fracture"], "Preformed toxins cause clustered, short-incubation illness."),
            q("A wedding cluster has abrupt vomiting in many guests within hours, but little fever. What is the most likely mechanism?", "Ingestion of preformed toxin", ["Chronic metal accumulation", "Anticholinergic delirium", "Snake envenomation"], "Short incubation and prominent vomiting point to preformed toxin.", True),
        ]),
        ("drug-abuse-forensics", "Drug Abuse, Dependence and Medico-Legal Testing", [
            q("Drug dependence includes tolerance, craving and", "Compulsive use despite harm", ["Improved judgment always", "Absence of withdrawal", "Only legal prescription"], "Dependence is behavioral and physiological adaptation with continued use despite harm."),
            q("Tolerance means", "Reduced response requiring higher dose for same effect", ["Instant allergy", "No drug effect ever", "Legal immunity"], "Repeated exposure can reduce effect at the same dose."),
            q("Withdrawal symptoms occur when", "A dependent person stops or reduces the drug", ["A drug is first prescribed always", "A sample is sealed", "A body decomposes"], "Neuroadaptation produces symptoms after cessation."),
            q("A long-term opioid user develops lacrimation, diarrhea, yawning, cramps and piloerection after stopping heroin. What is this syndrome?", "Opioid withdrawal", ["Organophosphorus poisoning", "Datura poisoning", "Lead colic"], "Autonomic and GI symptoms occur when opioids are withdrawn.", True),
            q("Urine drug screening is useful because many drugs or metabolites are", "Detectable for longer than in blood", ["Never excreted", "Only visible as fingerprints", "Always proof of intoxication at the time"], "Urine often has a longer detection window but may not prove current impairment."),
            q("What is a limitation of urine drug screening?", "It may not prove impairment at the time of sampling", ["It cannot detect any metabolite", "It proves exact dose always", "It replaces chain of custody"], "Detection window and impairment window differ."),
            q("Confirmatory drug testing commonly uses", "Chromatography-mass spectrometry methods", ["Cephalic index", "Diatom microscopy", "Hyoid x-ray"], "Screen positives are often confirmed by more specific analytical methods."),
            q("A workplace urine screen is positive for cannabinoids, but the worker denies intoxication during duty. What is the key limitation?", "Urine positivity may reflect past use rather than current impairment", ["Cannabis cannot be detected in urine", "The result proves exact dose", "No chain of custody is needed"], "THC metabolites can persist after acute impairment has resolved.", True),
            q("Chain of custody is especially important in drug testing because it", "Prevents disputes about sample identity and tampering", ["Increases drug concentration", "Acts as an antidote", "Determines age"], "Legal drug tests require documented collection and transfer."),
            q("A sealed urine sample for a medico-legal drug test lacks patient identifiers and seal signatures. What is the main defect?", "Sample identity and integrity can be challenged", ["The drug is neutralized", "The patient is automatically innocent", "The test becomes therapeutic"], "Unlabeled or poorly sealed samples may be rejected or disputed.", True),
        ]),
        ("occupational-environmental", "Occupational and Environmental Poisoning", [
            q("Occupational poisoning is best prevented by", "Substitution, engineering controls and personal protection", ["Only treating severe cases", "Avoiding documentation", "Increasing exposure time"], "Prevention follows hierarchy of controls and safe work practices."),
            q("Which route is important in solvent exposure?", "Inhalation", ["Only bone contact", "Only fingerprints", "Only dental filling contact"], "Volatile solvents are commonly absorbed through lungs."),
            q("Pesticide poisoning in workers may occur through", "Dermal and inhalational exposure", ["Only heredity", "Only x-ray exposure", "Only drowning"], "Workplace exposure often involves skin and respiratory routes."),
            q("A spray worker develops poisoning after using pesticide without gloves or mask. Which route is most plausible?", "Dermal and inhalational absorption", ["Only dental absorption", "Only skeletal uptake", "Only sound exposure"], "Pesticides can be absorbed through skin and inhaled as aerosols.", True),
            q("Biological monitoring in occupational poisoning means measuring", "Toxin or effect markers in biological samples", ["Only workplace attendance", "Only salary records", "Only shoe size"], "Blood, urine or enzyme levels may show exposure or biological effect."),
            q("Cholinesterase monitoring is useful in workers exposed to", "Organophosphorus pesticides", ["Carbon monoxide only", "Cannabis only", "Nitric acid only"], "Reduced cholinesterase activity indicates OP/carbamate exposure effect."),
            q("Environmental lead exposure is especially dangerous in children because it affects", "Neurodevelopment", ["Only hair color", "Only fingerprint class", "Only hyoid bone"], "Lead harms the developing nervous system even at low exposure."),
            q("A child living near battery recycling has learning difficulty, abdominal pain and elevated blood lead. What is the public health concern?", "Environmental lead poisoning", ["Drowning outbreak", "Datura robbery", "Snakebite cluster"], "Battery recycling can contaminate soil and dust with lead.", True),
            q("What is the key medico-legal value of workplace exposure records?", "They link disease pattern with occupational hazard", ["They replace clinical examination", "They prove homicide always", "They serve as antidote"], "Exposure records support causation assessment and prevention."),
            q("Several factory workers develop similar neurologic symptoms after a ventilation failure during solvent use. What investigation is most important?", "Workplace exposure assessment with biological monitoring", ["Exhumation of unrelated bodies", "Firearm comparison", "Dental age estimation"], "Clustered occupational illness requires exposure reconstruction and biological testing.", True),
        ]),
    ]),
]


def build():
    out = []
    for chapter_slug, chapter_title, chapter_order, topics in CHAPTERS:
        for topic_order, (slug, topic, rows) in enumerate(topics, 1):
            if len(rows) != 10:
                raise ValueError(f"{topic} has {len(rows)} questions")
            clinical = sum("clinical" in row.get("tags", []) for row in rows)
            if clinical != 3:
                raise ValueError(f"{topic} has {clinical} clinical questions")
            for index, row in enumerate(rows, 1):
                answer = row["answer"]
                shift = (chapter_order + topic_order + index) % 4
                opts = row["options"][shift:] + row["options"][:shift]
                out.append({
                    **row,
                    "id": f"fmt-section2-{chapter_slug}-{slug}-{index:02d}",
                    "subject": SUBJECT_TITLE,
                    "subjectId": SUBJECT_ID,
                    "subjectTitle": SUBJECT_TITLE,
                    "chapterTitle": chapter_title,
                    "chapterOrder": chapter_order,
                    "topic": topic,
                    "topicTitle": topic,
                    "topicOrder": topic_order,
                    "source": "ai",
                    "sourcePdf": SOURCE_PDF,
                    "imageUrls": [],
                    "options": opts,
                    "answerIndex": opts.index(answer),
                    "answer": answer,
                })
    return out


def validate(qs):
    if len(qs) != 200:
        raise ValueError(f"Expected 200, got {len(qs)}")
    if len({q["id"] for q in qs}) != 200:
        raise ValueError("Duplicate IDs")
    for _, chapter_title, _, _ in CHAPTERS:
        chapter_qs = [q for q in qs if q["chapterTitle"] == chapter_title]
        clinical = sum("clinical" in q.get("tags", []) for q in chapter_qs)
        if len(chapter_qs) != 100 or clinical != 30:
            raise ValueError(f"{chapter_title}: {len(chapter_qs)} questions, {clinical} clinical")
    for item in qs:
        if not item["prompt"].endswith(("?", ".")):
            raise ValueError(f"Bad punctuation: {item['id']}")
        if item["options"][item["answerIndex"]] != item["answer"]:
            raise ValueError(f"Answer mismatch: {item['id']}")


def update(path, qs):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    ids = {item["id"] for item in qs}
    data["questions"] = [item for item in data.get("questions", []) if item.get("id") not in ids] + qs
    data["questions"].sort(key=lambda item: item.get("id", ""))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    qs = build()
    validate(qs)
    for path in DATA_PATHS:
        update(path, qs)
        print(f"Added {len(qs)} FMT Section 2 questions to {path}.")
    for _, chapter_title, _, _ in CHAPTERS:
        print(f"- {chapter_title}: 100 questions, 30 clinical")


if __name__ == "__main__":
    main()
