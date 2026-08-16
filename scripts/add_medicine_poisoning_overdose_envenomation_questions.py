import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Poisoning, Drug Overdose, and Envenomation"
CHAPTER_ORDER = 14
SOURCE_PDF = "medicine 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def q(prompt, answer, wrong, explanation, clinical=False, page=None):
    return {
        "prompt": prompt.strip(),
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "high" if clinical else "moderate",
        "tags": ["clinical"] if clinical else [],
        "sourcePdfPageStart": page,
        "sourcePdfPageEnd": page,
    }


TOPICS = [
    ("Heavy Metal Poisoning", [
        q("K x-ray fluorescence instruments measure lead levels in bone, which reflect", "Cumulative exposure over many years", ["Only exposure in the last hour", "Serum calcium balance", "Immediate arterial oxygenation"], "Chapter 449 states that KXRF measures bone lead, reflecting cumulative exposure over many years, unlike blood lead which mostly reflects recent exposure.", page=3297),
        q("Blood lead levels mostly reflect", "Recent exposure", ["Lifetime cumulative exposure", "Renal calcium excretion only", "Histamine fish poisoning"], "Medicine 1 contrasts blood lead as mainly recent exposure with bone lead as cumulative exposure.", page=3297),
        q("Serious cadmium poisoning in Japan caused itai-itai disease, named for painful", "Bone fractures", ["Respiratory paralysis", "Serotonin syndrome", "Tick paralysis"], "Chapter 449 describes itai-itai disease as cadmium-induced bone toxicity leading to painful fractures.", page=3297),
        q("A patient from a mining-contaminated region has severe bone pain, fractures and renal calciuric effects after food and water exposure. Which metal is most likely?", "Cadmium", ["Thallium", "Lithium", "Iron"], "Medicine 1 links cadmium contamination of food and water with bone toxicity, fractures and renal calciuric effects.", True, page=3297),
        q("A chronically exposed patient develops increased risk of coronary heart disease, stroke and lung function impairment. Which heavy metal exposure fits Medicine 1?", "Arsenic", ["Lithium", "Calcium", "Sodium"], "The heavy metal chapter lists arsenic exposure associations including coronary heart disease, stroke and lung function impairment.", True, page=3297),
        q("Thallium is absorbed by ingestion, inhalation and through the", "Skin", ["Retina only", "Joint cartilage", "Spleen only"], "Chapter 449 states that thallium is absorbed through the skin as well as by ingestion and inhalation.", page=3300),
        q("Severe thallium poisoning follows a single ingested dose greater than 1 g or greater than", "8 mg/kg", ["0.08 mg/kg", "80 mg/kg only", "800 mg/kg"], "Medicine 1 gives severe poisoning thresholds of >1 g or >8 mg/kg.", page=3300),
        q("A patient with suspected acute thallium ingestion presents within 4-6 hours. Induced emesis or gastric lavage may be indicated, and which oral agent prevents absorption?", "Prussian blue", ["Naloxone", "Cyproheptadine", "Vitamin K"], "Chapter 449 states Prussian blue prevents thallium absorption and is given orally.", True, page=3300),
        q("Unlike many other metal poisonings, thallium poisoning may be less severe when activated charcoal interrupts", "Enterohepatic circulation", ["Pulmonary ventilation", "Bone remodeling", "Thyroid uptake"], "Medicine 1 notes activated charcoal may reduce thallium severity by interrupting enterohepatic circulation.", page=3300),
        q("A poisoned patient has nausea, abdominal pain, hematemesis followed by confusion, psychosis and coma after radiopaque metal ingestion. Which poisoning fits best?", "Thallium poisoning", ["Scombroid poisoning", "Tick paralysis", "Fire ant sting"], "Chapter 449 describes thallium poisoning with early GI symptoms followed by neuropsychiatric findings and notes thallium is radiopaque.", True, page=3300),
    ]),
    ("Poisoning and Drug Overdose Management", [
        q("Medicine 1 table 450-1 classifies poisoning physiologic states as stimulated, depressed, discordant and", "Normal", ["Febrile only", "Cyanotic only", "Hypervolemic"], "The poisoning differential table organizes poisonings by physiologic state including normal.", page=3302),
        q("AGMA-inducing poisonings in table 450-1 include ethylene glycol, methanol, iron and", "Salicylate", ["Warfarin", "Penicillin", "Epinephrine"], "Medicine 1 lists alcohol ketoacidosis, ethylene glycol, iron, methanol, other alcohols, salicylate and toluene as AGMA inducers.", page=3302),
        q("Fundamental poisoning management begins with supportive care including airway protection, oxygenation and", "Hemodynamic support", ["Routine thrombolysis", "Radioiodine scanning", "Bone marrow biopsy"], "Table 450-3 includes airway protection, oxygenation/ventilation, treatment of arrhythmias and hemodynamic support.", page=3304),
        q("During the pretoxic phase before symptoms begin, the highest treatment priority is", "Decontamination", ["Psychiatric referral only", "Delayed imaging only", "No treatment until symptoms"], "Chapter 450 states that before onset of poisoning, decontamination is the highest priority and treatment is based on history.", page=3304),
        q("A patient arrives soon after a potentially lethal ingestion but is not yet symptomatic. Which intervention goal has highest priority in this pretoxic phase?", "Prevent further poison absorption", ["Wait for toxicity before acting", "Start chronic anticoagulation", "Perform thyroid scintigraphy"], "Medicine 1 emphasizes decontamination to prevent absorption during the pretoxic phase.", True, page=3304),
        q("Activated charcoal is the preferred gastrointestinal decontamination method in most situations because it has comparable or greater efficacy and fewer", "Contraindications and complications", ["Antidotes", "Electrolytes", "Hormones"], "Chapter 450 states charcoal is preferred over ipecac or gastric lavage because of efficacy and fewer contraindications and complications.", page=3306),
        q("The generally recommended activated charcoal dose is", "1 g/kg body weight", ["1 mg/kg", "10 mg total", "100 g/kg"], "Medicine 1 gives 1 g/kg as the generally recommended activated charcoal dose.", page=3306),
        q("Activated charcoal is not recommended after corrosive ingestion because it obscures", "Endoscopy", ["Pulse oximetry", "ECG", "Urinalysis"], "Chapter 450 notes charcoal is not recommended for corrosives because it obscures endoscopy.", True, page=3306),
        q("A cyclic antidepressant overdose causes ventricular tachydysrhythmias with QRS prolongation. Specific treatment is hypertonic sodium", "Bicarbonate", ["Chloride only", "Iodide", "Fluoride"], "Table 450-4 recommends hypertonic sodium bicarbonate or saline for ventricular tachydysrhythmias with QRS prolongation in cyclic antidepressant poisoning.", True, page=3310),
        q("A patient on SSRI and tramadol develops agitation, hyperreflexia, myoclonus, diarrhea, fever and tachycardia. Severe cases may benefit from", "Cyproheptadine", ["Prussian blue", "CroFab only", "Vitamin K"], "Medicine 1 describes serotonin syndrome and notes cyproheptadine may help severe cases after stopping offending agents.", True, page=3313),
    ]),
    ("Snakebite, Marine and Arthropod Envenomation", [
        q("The most important prehospital care for venomous snakebite is rapid transport to a facility with supportive care and", "Antivenom therapy", ["MRI only", "Routine incision and suction", "Hyperbaric oxygen only"], "Chapter 451 states rapid transport to a facility equipped for ABC support and antivenom is the most important prehospital care.", page=3315),
        q("After snakebite, jewelry or tight clothing near the bite should be removed to avoid constriction from anticipated", "Soft-tissue swelling", ["Hypothermia", "Migraine", "Hyperglycemia"], "Medicine 1 advises removing jewelry and tight clothing because swelling is anticipated.", page=3315),
        q("Incising and applying suction to a snakebite should be avoided because these measures worsen local tissue damage and increase", "Infection risk", ["Antivenom availability", "Serum sodium", "Bone density"], "Chapter 451 states incision/suction exacerbate tissue damage, increase infection risk and are not effective.", page=3315),
        q("A hiker is bitten by a pit viper. Friends want to cut and suction the wound. The best advice is", "Avoid incision and suction and arrange rapid transport", ["Apply ice and electric shock", "Capture the snake by hand", "Delay transport until swelling stops"], "Medicine 1 discourages incision/suction and prioritizes rapid transport for snakebite care.", True, page=3315),
        q("In U.S. and Canadian venomous snakebite management, prophylactic antibiotics are unnecessary unless prehospital care included incision or", "Mouth suction", ["Photographing the snake", "Splinting the limb", "Removing jewelry"], "Table 451-1 states prophylactic antibiotics are unnecessary unless incision or mouth suction was used.", page=3317),
        q("A snakebite victim has severe pain but evolving coagulopathy is a concern. Medicine 1 advises avoiding salicylates/NSAIDs and using acetaminophen and/or", "Opioids", ["Warfarin", "Methotrexate", "Activated charcoal"], "The management table recommends acetaminophen and/or opioids while avoiding salicylates and NSAIDs.", True, page=3317),
        q("Scombroid poisoning symptoms usually develop within", "15-90 minutes", ["6 days", "3 months", "Several years"], "Chapter 451 states symptoms of scombroid poisoning develop within 15-90 minutes after ingestion.", page=3324),
        q("A patient develops flushing, tingling of lips, nausea and abdominal discomfort 30 minutes after eating unrefrigerated tuna. The most likely diagnosis is", "Scombroid poisoning", ["Tick paralysis", "Thallium poisoning", "Brown recluse necrosis"], "Medicine 1 describes scombroid poisoning after dark/red-fleshed fish with symptoms beginning 15-90 minutes after ingestion.", True, page=3324),
        q("Tick paralysis usually begins with symmetric lower-extremity weakness about how long after tick attachment?", "6 days", ["15 minutes", "1 hour", "6 months"], "Chapter 452 states weakness begins symmetrically in the lower extremities 6 days after tick attachment.", page=3326),
        q("A child has ascending symmetric weakness, absent reflexes, normal sensation and normal lumbar puncture; a tick is found in the scalp. The key treatment is", "Removal of the tick", ["High-dose glucocorticoids", "Hypertonic sodium bicarbonate", "Prussian blue"], "Medicine 1 states diagnosis depends on finding the tick and removal generally leads to rapid improvement.", True, page=3326),
    ]),
]


def build_questions():
    questions = []
    for topic_order, (topic, rows) in enumerate(TOPICS, 1):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        clinical_count = sum(1 for row in rows if "clinical" in row.get("tags", []))
        if clinical_count != 4:
            raise ValueError(f"{topic} has {clinical_count} clinical questions, expected 4")
        topic_slug = slugify(topic)
        for question_order, row in enumerate(rows, 1):
            questions.append({
                "id": f"medicine-poisoning-overdose-envenomation-{topic_slug}-{question_order:02d}",
                "subjectId": SUBJECT_ID,
                "subjectTitle": SUBJECT_TITLE,
                "chapterTitle": CHAPTER,
                "chapterOrder": CHAPTER_ORDER,
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "source": "ai",
                "sourcePdf": SOURCE_PDF,
                "imageUrls": [],
                **row,
            })
    return questions


def update(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    questions = build_questions()
    data["questions"] = [
        item for item in data.get("questions", [])
        if not (item.get("subjectId") == SUBJECT_ID and item.get("chapterTitle") == CHAPTER)
    ] + questions
    if len(questions) != 30:
        raise AssertionError(f"Expected 30 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 30:
        raise AssertionError("Duplicate poisoning/overdose/envenomation question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 30 book-based Poisoning, Drug Overdose, and Envenomation questions.")


if __name__ == "__main__":
    main()
