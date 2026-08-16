import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Critical Care Medicine"
CHAPTER_ORDER = 8
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
    ("Approach to Critical Illness and ICU Care", [
        q("In Medicine 1 chapter 293, the common broad categories of shock include hypovolemic, cardiogenic and", "High-cardiac-output shock with decreased systemic vascular resistance", ["Pure restrictive shock from low TLC", "Primary neurologic shock from high ICP only", "Hepatic synthetic failure without circulatory change"], "Chapter 293 summarizes common shock categories as hypovolemic, cardiogenic and high-output hypotension from decreased SVR.", page=2025),
        q("Static right atrial pressure is unreliable for predicting fluid responsiveness; chapter 293 notes that a better bedside clue is", "Change in right atrial pressure with spontaneous respiration", ["Single random serum sodium", "Skin temperature alone", "Baseline hemoglobin only"], "The shock approach notes that respiratory variation in right atrial pressure predicts fluid responsiveness better than static pressure.", page=2025),
        q("A hypotensive patient has vomiting, diarrhea, low JVP and improves after IV fluids. Which shock category fits best?", "Hypovolemic shock", ["Cardiogenic shock", "Anaphylactic shock", "Obstructive sleep apnea"], "Chapter 293 links decreased intravascular volume from losses with fluid-responsive hypovolemic shock.", True, page=2025),
        q("A hypotensive patient has increased JVP, crackles and S3 or S4 gallops. Which shock pattern is suggested?", "Cardiogenic shock", ["Fluid-responsive hypovolemic shock", "Uncomplicated obstructive sleep apnea", "Primary hyperventilation syndrome"], "Medicine 1 describes cardiogenic shock clues as increased intravascular volume, gallops, edema, crackles and pulmonary edema.", True, page=2025),
        q("The most common cause of high-cardiac-output hypotension with decreased systemic vascular resistance is", "Sepsis", ["Myasthenia gravis", "Primary pneumothorax", "Iron deficiency"], "Chapter 293 identifies sepsis as the most common cause of high-output hypotension.", page=2025),
        q("Type IV respiratory failure in critical illness results from", "Hypoperfusion of respiratory muscles in shock", ["Pleural fluid transudation only", "Bronchial asthma alone", "Upper airway snoring"], "Medicine 1 chapter 293 defines type IV respiratory failure as respiratory muscle hypoperfusion in shock.", page=2027),
        q("A patient in shock is using marked respiratory effort; chapter 293 notes that intubation and ventilation can help by", "Redistributing cardiac output away from respiratory muscles to vital organs", ["Increasing hemoglobin concentration instantly", "Removing all need for fluids", "Treating sepsis without antibiotics"], "Mechanical ventilation can reduce respiratory muscle oxygen demand while shock is treated.", True, page=2027),
        q("Before a spontaneous breathing trial, stable oxygenation in chapter 293 includes PaO2/FIO2 greater than 200 and PEEP", "5 cm H2O or less", ["20 cm H2O or more", "Exactly zero in every patient", "Greater than 30 cm H2O"], "Daily screening for ventilator liberation includes stable oxygenation with PEEP <=5 cm H2O.", page=2027),
        q("A spontaneous breathing trial should be stopped if the respiratory rate is greater than 35/min for more than", "5 minutes", ["10 seconds", "1 hour", "24 hours"], "Chapter 293 lists RR >35/min for >5 min among SBT failure criteria.", page=2027),
        q("In the ICU, ventilator-associated events correlate strongly with", "Duration of intubation and mechanical ventilation", ["Number of family visits", "Use of lateral chest x-ray", "Daily serum calcium"], "The ICU infection section emphasizes timely removal of invasive devices because risk rises with device duration.", True, page=2029),
    ]),
    ("ARDS and Mechanical Ventilatory Support", [
        q("Medicine 1 chapter 294 states that most ARDS cases are caused by pneumonia and sepsis, followed by aspiration, trauma, multiple transfusions and", "Drug overdose", ["Hypothyroidism alone", "Simple anxiety", "Stable hypertension"], "Chapter 294 lists common ARDS etiologies, with pneumonia and sepsis accounting for most cases.", page=2031),
        q("The natural history of ARDS is classically divided into exudative, proliferative and", "Fibrotic phases", ["Hemorrhagic phases", "Neoplastic phases", "Syncopal phases"], "Medicine 1 describes three ARDS phases: exudative, proliferative and fibrotic.", page=2031),
        q("In the exudative phase of ARDS, injury to alveolar capillary endothelium and type I pneumocytes causes", "Protein-rich edema in interstitial and alveolar spaces", ["Pure pleural air without edema", "Isolated airway smooth muscle spasm", "Portal venous thrombosis"], "The exudative phase features loss of the tight alveolar barrier and protein-rich edema.", page=2031),
        q("A septic patient develops acute hypoxemia with bilateral infiltrates and poor compliance. Which ARDS mechanism best explains the hypoxemia?", "Intrapulmonary shunting from dependent alveolar edema and collapse", ["Low hemoglobin synthesis only", "Hyperventilation syndrome", "Primary metabolic alkalosis"], "Chapter 294 links dependent edema/collapse to decreased compliance, shunt and hypoxemia.", True, page=2031),
        q("A ventilated patient has severe ARDS with PaO2/FIO2 below 150 mm Hg. Which positioning strategy reduced 28-day mortality in a trial cited in Medicine 1?", "Prone positioning", ["Left lateral decubitus only", "Sitting upright without ventilation", "Trendelenburg positioning"], "Chapter 294 notes prone positioning reduced 28-day mortality in severe ARDS.", True, page=2033),
        q("Recruitment maneuvers in ARDS transiently increase PEEP to recruit atelectatic lung, but Medicine 1 notes that they", "Have not established a mortality benefit", ["Are always curative", "Should replace all ventilation", "Are contraindicated in every ARDS patient"], "Recruitment maneuvers can improve oxygenation, but mortality benefit has not been established.", page=2033),
        q("Mechanical ventilation is primarily used to assist or replace spontaneous breathing and improve oxygenation by applying high-oxygen-content gas and", "Positive pressure", ["Negative abdominal pressure only", "Pleural drainage", "Intracoronary contrast"], "Chapter 295 describes MV as supporting ventilation and oxygenation using oxygen-rich gas and positive pressure.", page=2035),
        q("Hypoxemic respiratory failure is present when arterial oxygen saturation below 90% persists despite", "An increased inspired oxygen fraction", ["Normal room air only", "A low respiratory rate in sleep", "A normal platelet count"], "Medicine 1 defines hypoxemic failure as SaO2 <90% despite increased FIO2, usually due to V/Q mismatch or shunt.", page=2035),
        q("A comatose patient with PaCO2 62 mmHg has ventilatory failure. In chapter 295, hypercarbic failure usually reflects decreased minute ventilation or increased", "Physiologic dead space", ["Serum albumin", "Pleural protein ratio", "Left ventricular ejection fraction"], "Hypercarbic failure occurs when alveolar ventilation is inadequate due to low minute ventilation or increased dead space.", True, page=2035),
        q("A patient has been ventilated for 12 days and is expected to need ongoing support. Medicine 1 says tracheostomy is generally indicated if MV is needed for more than", "10 to 14 days", ["24 hours", "48 hours", "3 days",], "Chapter 296 notes that when MV is needed for >10-14 days, planned tracheostomy is generally indicated.", True, page=2039),
    ]),
    ("Shock, Sepsis and Cardiac Arrest", [
        q("In septic shock resuscitation, Medicine 1 recommends crystalloids as first-line fluids and recommends against", "Hydroxyethyl starches", ["Balanced oxygen delivery", "Blood cultures", "Source control"], "The sepsis section recommends crystalloids and advises against hydroxyethyl starches for volume replacement.", page=2044),
        q("After adequate circulating volume, vasopressors are used in sepsis to", "Maintain perfusion of vital organs", ["Sterilize blood cultures", "Remove pulmonary edema instantly", "Lower lactate by assay interference"], "Medicine 1 states vasopressors are recommended after adequate volume to maintain vital-organ perfusion.", page=2044),
        q("Compared with dopamine in shock trials, norepinephrine had fewer adverse events, including", "Arrhythmias", ["Cataracts", "Pleural effusions", "Hypercalcemia"], "The book cites evidence favoring norepinephrine over dopamine, including fewer arrhythmias.", page=2055),
        q("A patient with septic shock remains hypotensive after fluids. Which first-line vasopressor is reasonable according to Medicine 1?", "Norepinephrine", ["Oral theophylline", "Subcutaneous insulin alone", "Inhaled albuterol"], "Norepinephrine is described as a reasonable first-line vasopressor based on randomized comparisons with dopamine.", True, page=2055),
        q("In cardiogenic shock after MI, supportive therapy should be initiated simultaneously with diagnostic evaluation including ECG, chest x-ray, ABG, lactate and", "Initial echocardiography", ["Colonoscopy", "Sleep study", "Skin prick testing"], "Chapter 298 calls initial echocardiography invaluable for identifying the underlying cause of cardiogenic shock.", page=2053),
        q("Shock associated with a first inferior MI should prompt a search for RV involvement or", "A mechanical complication", ["Chylothorax", "Obstructive sleep apnea", "Stable asthma"], "Medicine 1 notes inferior MI with shock should raise concern for mechanical cause or right ventricular involvement.", page=2053),
        q("A post-MI patient develops pulmonary edema and shock from acute severe mitral regurgitation. The diagnosis is confirmed by", "Echocardiography", ["Urinalysis", "Spirometry", "Pleural ADA"], "Chapter 298 says acute severe MR after MI is confirmed by echocardiography.", True, page=2057),
        q("Free wall rupture after MI classically causes sudden pulseless electrical activity due to", "Cardiac tamponade", ["Bronchospasm", "Septic vasodilation", "Pleural empyema"], "Medicine 1 describes free wall rupture causing sudden loss of pulse, BP and consciousness with sinus rhythm from tamponade.", True, page=2057),
        q("The out-of-hospital chain of survival begins with recognition of sudden cardiac arrest, rapid CPR with chest compressions and", "Defibrillation as quickly as possible", ["Delayed angiography before CPR", "Routine corticosteroids", "Immediate CT before compressions"], "Chapter 299 emphasizes early recognition, chest compressions and rapid defibrillation in the chain of survival.", page=2063),
        q("During CPR, chest compressions should be given at a rate of", "100 to 120 per minute", ["20 to 40 per minute", "40 to 60 per minute", "160 to 200 per minute"], "Medicine 1 states chest compressions should be initiated without delay at 100-120/min with full recoil.", True, page=2063),
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
                "id": f"medicine-critical-care-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate critical care question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 30 book-based Critical Care Medicine questions.")


if __name__ == "__main__":
    main()
