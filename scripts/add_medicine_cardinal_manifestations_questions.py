import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Cardinal Manifestations and Presentation of Diseases"
CHAPTER_ORDER = 2
SOURCE_PDF = "medicine 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def q(prompt, answer, wrong, explanation, clinical=False):
    return {
        "prompt": prompt.strip(),
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "high" if clinical else "moderate",
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("Pain and Headache Syndromes", [
        q("Acute pain is most useful clinically because it usually", "Signals tissue injury and localizes the diagnostic search", ["Always proves psychogenic disease", "Excludes serious illness if mild", "Requires opioids before assessment"], "Pain timing, site, radiation and associated features guide early differential diagnosis."),
        q("Visceral pain is often poorly localized because visceral afferents", "Enter the spinal cord bilaterally and converge with somatic pathways", ["Have no spinal connections", "Are carried only by motor fibers", "Always bypass the thalamus"], "Convergence and sparse visceral sensory mapping make visceral pain diffuse or referred."),
        q("A patient has tearing chest pain radiating to the back with unequal arm blood pressures. The most urgent diagnosis is", "Aortic dissection", ["Costochondritis", "Stable angina", "Gastroesophageal reflux"], "Abrupt severe transfixing pain with pulse or pressure asymmetry is classic for dissection.", True),
        q("Neuropathic pain is suggested by", "Burning pain with allodynia or electric shock-like quality", ["Only dull pressure after exercise", "Pain relieved permanently by antacids", "Painless swelling only"], "Neuropathic pain reflects nerve injury and often has burning, shooting or allodynic features."),
        q("Referred pain from diaphragmatic irritation is commonly felt at the", "Shoulder tip", ["Umbilicus only", "Heel", "Mandibular angle only"], "C3-C5 phrenic afferents refer pain to the shoulder region."),
        q("A woman has unilateral throbbing headache with nausea, photophobia and worsens with activity. The most likely diagnosis is", "Migraine", ["Cluster headache", "Trigeminal neuralgia", "Subarachnoid hemorrhage"], "Migraine commonly causes unilateral pulsatile headache with nausea and light sensitivity.", True),
        q("The red flag in headache that most strongly suggests subarachnoid hemorrhage is", "Thunderclap onset reaching maximum intensity within seconds to minutes", ["Mild bilateral pressure after work", "Long history of identical headaches", "Relief after sleep"], "Explosive maximal-at-onset headache requires urgent evaluation for hemorrhage."),
        q("Cluster headache classically presents with", "Strictly unilateral orbital pain with ipsilateral autonomic features", ["Bilateral band-like pain without autonomic features", "Jaw claudication only", "Pain triggered only by neck flexion"], "Cluster attacks are severe, unilateral, orbital or temporal, and associated with lacrimation, rhinorrhea or ptosis."),
        q("A 72-year-old has new temporal headache, jaw claudication and elevated ESR. The immediate priority is", "Start glucocorticoids to prevent visual loss", ["Give triptan first", "Reassure as tension headache", "Delay treatment until biopsy is complete"], "Giant cell arteritis threatens vision and treatment should not wait for biopsy.", True),
        q("Pain out of proportion to examination in an ischemic limb suggests", "Acute compartment syndrome or critical ischemia", ["Simple cellulitis only", "Benign muscle strain", "Chronic venous pigmentation"], "Severe disproportionate pain is a danger sign for ischemic tissue injury.", True),
    ]),
    ("Fever, Hyperthermia and Hypothermia", [
        q("Fever differs from hyperthermia because fever involves", "An elevated hypothalamic temperature set point", ["Failure of cytokine signaling", "Normal thermoregulation with heat loss only", "Absence of prostaglandins"], "Fever is regulated pyrexia mediated by endogenous pyrogens and prostaglandin E2."),
        q("Rigors during fever most strongly suggest", "Rapid rise in set point often seen with bacteremia", ["Normal sleep transition", "Pure anxiety without physiologic change", "Hypothyroidism"], "Shaking chills occur as the body generates heat to meet a higher set point."),
        q("A patient on antipsychotics has hyperthermia, severe rigidity, autonomic instability and high CK. The likely syndrome is", "Neuroleptic malignant syndrome", ["Uncomplicated viral fever", "Serotonin deficiency", "Simple heat rash"], "Dopamine blockade can cause rigidity, hyperthermia, autonomic instability and rhabdomyolysis.", True),
        q("Fever of unknown origin requires attention to", "Duration, documented temperature, repeated examination and targeted testing", ["Empiric steroids for all patients", "Single normal blood count to exclude disease", "Avoiding travel history"], "FUO evaluation depends on verifying fever and repeatedly reassessing evolving clues."),
        q("Relative bradycardia with fever may be seen in", "Typhoid fever and some intracellular infections", ["Every bacterial pneumonia", "Pheochromocytoma only", "Acute hemorrhage"], "Pulse-temperature dissociation can occur in typhoid, brucellosis, legionella and drug fever."),
        q("A marathon runner collapses with core temperature 41 C, confusion and hot skin. The priority is", "Immediate rapid cooling with supportive resuscitation", ["Oral paracetamol as sole therapy", "Observation until sweating returns", "Empiric levothyroxine"], "Heat stroke is hyperthermia with CNS dysfunction and needs rapid cooling.", True),
        q("Drug fever is supported by", "Fever without toxicity that resolves after stopping the culprit drug", ["Mandatory rash in every case", "Positive blood culture", "Hypothermia after antibiotics"], "Drug fever can occur without rash or eosinophilia and improves after withdrawal."),
        q("Hypothermia can mask infection because it", "May blunt fever and inflammatory signs, especially in elderly or frail patients", ["Always excludes sepsis", "Prevents arrhythmia", "Raises leukocyte counts reliably"], "Older, septic or exposed patients may present cold rather than febrile."),
        q("An elderly septic patient is confused with temperature 35 C and hypotension. The best interpretation is", "Severe infection can present with hypothermia and delirium", ["Sepsis is excluded by absence of fever", "Only environmental cold exposure is possible", "Antibiotics are contraindicated"], "Hypothermia in sepsis is a high-risk presentation, not reassurance.", True),
        q("Antipyretic response is diagnostically unreliable because", "Malignant, inflammatory and infectious fevers may all transiently improve", ["Only viral fevers respond", "Cancer fever never responds", "Bacterial fever always worsens"], "Temperature fall after antipyretics does not identify etiology.", True),
    ]),
    ("Fatigue, Weight Change and Edema", [
        q("Clinically significant fatigue should be evaluated first by", "Clarifying duration, sleep, mood, medications, systemic symptoms and functional impact", ["Ordering only vitamin levels", "Assuming malingering", "Avoiding medication review"], "Fatigue has metabolic, inflammatory, psychiatric, sleep-related and drug causes."),
        q("Unintentional weight loss is concerning when it is", "More than 5 percent of body weight over 6 to 12 months", ["Only 0.5 kg after exercise", "Voluntary dieting", "Stable for years"], "Sustained unintentional loss suggests malignancy, chronic infection, endocrine or inflammatory disease."),
        q("A patient has weight loss, heat intolerance, tremor and tachycardia. The likely cause is", "Hyperthyroidism", ["Hypothyroidism", "Nephrotic syndrome", "Addison disease only"], "Thyrotoxicosis increases metabolic rate and adrenergic symptoms.", True),
        q("Generalized edema results from increased hydrostatic pressure, reduced oncotic pressure, lymphatic obstruction or", "Renal sodium and water retention", ["High arterial oxygen saturation", "Low serum potassium alone", "Increased red cell mass only"], "Edema reflects imbalance of Starling forces, lymph drainage or renal salt handling."),
        q("Low serum albumin causes edema mainly by", "Reducing plasma oncotic pressure", ["Increasing hemoglobin affinity", "Blocking lymph nodes directly", "Increasing platelet count"], "Albumin holds fluid intravascularly; hypoalbuminemia favors interstitial fluid accumulation."),
        q("A young adult has periorbital edema, frothy urine and heavy proteinuria. The syndrome is", "Nephrotic syndrome", ["Right heart failure", "Cirrhosis without renal disease", "Myxedema coma"], "Proteinuria with hypoalbuminemia causes edema and foamy urine.", True),
        q("Pitting edema is most typical of", "Excess interstitial fluid from heart, renal, liver or venous disease", ["Pure myxedema", "Localized lipoma", "Urticaria only"], "Pitting reflects mobile interstitial fluid displaced by pressure."),
        q("Cachexia differs from simple starvation because it includes", "Inflammation-driven muscle loss not fully reversed by calories alone", ["Only water loss", "Increased bone density", "No metabolic change"], "Cachexia is mediated by inflammatory and neurohormonal pathways."),
        q("A patient with progressive dyspnea, raised JVP, hepatomegaly and bilateral leg edema most likely has", "Right-sided heart failure", ["Isolated iron deficiency", "Migraine", "Primary adrenal insufficiency only"], "Systemic venous congestion causes JVP elevation, hepatic congestion and dependent edema.", True),
        q("Bilateral leg edema that worsens during the day and improves overnight suggests", "Dependent edema from venous insufficiency or systemic fluid overload", ["Acute arterial occlusion", "Cluster headache", "Ototoxicity"], "Gravity-dependent edema is common in venous and systemic volume states.", True),
    ]),
    ("Syncope, Dizziness and Weakness", [
        q("Syncope is defined by", "Transient loss of consciousness from global cerebral hypoperfusion", ["Any fall without recall", "Vertigo without collapse", "Focal seizure aura only"], "True syncope is brief, self-limited and due to reduced cerebral blood flow."),
        q("The most concerning syncope history is", "Syncope during exertion or while supine", ["Fainting after seeing blood", "Prodrome with nausea in a hot room", "Brief lightheadedness on standing"], "Exertional or supine syncope raises concern for arrhythmia or structural heart disease."),
        q("A patient collapses during exercise and has a harsh systolic murmur that increases with Valsalva. The likely cause is", "Hypertrophic obstructive cardiomyopathy", ["Vasovagal syncope", "Benign positional vertigo", "Panic attack"], "Exertional syncope with dynamic systolic murmur suggests HOCM.", True),
        q("Orthostatic hypotension is diagnosed by", "Fall in systolic pressure at least 20 mmHg or diastolic at least 10 mmHg after standing", ["Any pulse below 100/min", "Raised blood pressure while lying", "Headache after meals only"], "Orthostatic vitals document impaired blood pressure maintenance on standing."),
        q("Vertigo most specifically means", "Illusory movement or spinning sensation", ["General fatigue", "Loss of consciousness", "Diffuse weakness"], "Vertigo is a vestibular symptom, not simply lightheadedness."),
        q("Brief vertigo triggered by rolling in bed with no hearing loss suggests", "Benign paroxysmal positional vertigo", ["Meniere disease", "Vestibular schwannoma", "Cerebellar hemorrhage always"], "BPPV causes seconds-long positional vertigo from canalith movement.", True),
        q("True motor weakness should be distinguished from fatigue because weakness implies", "Reduced power on examination", ["Only sleepiness", "Pain anywhere", "Low motivation alone"], "Objective power loss localizes disease to muscle, neuromuscular junction, nerve, cord or brain."),
        q("Proximal symmetric weakness with difficulty climbing stairs suggests", "Myopathy", ["Distal sensory neuropathy only", "Isolated vestibular disease", "Migraine aura"], "Myopathies often affect proximal limb girdle muscles."),
        q("A patient has fluctuating ptosis, diplopia and weakness worse later in the day. The likely diagnosis is", "Myasthenia gravis", ["Polymyalgia rheumatica", "Meniere disease", "Vasovagal syncope"], "Fatigable ocular and bulbar weakness is typical of myasthenia.", True),
        q("Acute ascending weakness with areflexia after diarrhea suggests", "Guillain-Barre syndrome", ["BPPV", "Iron deficiency alone", "Cluster headache"], "Postinfectious ascending weakness with areflexia suggests acute inflammatory polyradiculoneuropathy.", True),
    ]),
    ("Chest Pain, Dyspnea and Palpitations", [
        q("Typical anginal chest pain is classically", "Retrosternal pressure provoked by exertion and relieved by rest or nitrates", ["Sharp pain lasting one second", "Pain only with palpation", "Burning only after spicy food"], "Angina reflects demand ischemia and has predictable exertional features."),
        q("Pleuritic chest pain is pain that", "Worsens with inspiration or coughing", ["Improves with deep breath", "Occurs only after meals", "Is always cardiac"], "Inflammation of pleura or adjacent structures causes respiratory variation."),
        q("A patient has acute pleuritic chest pain, dyspnea, tachycardia and hemoptysis after surgery. The likely diagnosis is", "Pulmonary embolism", ["Stable angina", "Esophageal spasm", "Costochondritis only"], "Postoperative immobility plus pleuritic pain and dyspnea is classic for PE.", True),
        q("Orthopnea is most closely associated with", "Left-sided heart failure", ["Migraine", "Ureteric colic", "Hypocalcemia"], "Recumbency increases venous return and pulmonary congestion in left heart failure."),
        q("Paroxysmal nocturnal dyspnea occurs because", "Pulmonary congestion worsens after lying down during sleep", ["Bronchi permanently dilate", "Pain fibers stop firing", "Blood glucose always falls"], "Fluid redistribution and increased venous return can wake patients with breathlessness."),
        q("A patient with asthma has silent chest, exhaustion and falling oxygen saturation. This indicates", "Life-threatening airflow obstruction", ["Mild bronchospasm", "Hyperventilation syndrome only", "Resolved attack"], "A quiet chest during severe asthma suggests minimal air movement and impending failure.", True),
        q("Palpitations with abrupt onset and termination suggest", "Paroxysmal tachyarrhythmia", ["Gradual deconditioning only", "Chronic anemia only", "Pneumonia without tachycardia"], "Sudden start-stop episodes are typical of reentrant arrhythmias."),
        q("The most important first test during ongoing palpitations is usually", "Electrocardiogram", ["Serum amylase", "Colonoscopy", "Skin biopsy"], "ECG during symptoms can identify rhythm, conduction and ischemia."),
        q("A young patient has episodic palpitations, sweating, headache and severe hypertension. The cause to consider is", "Pheochromocytoma", ["BPPV", "Nephrotic syndrome", "Tension headache"], "Catecholamine surges cause paroxysmal hypertension, palpitations, sweating and headache.", True),
        q("Sharp chest pain relieved by sitting forward with diffuse ST elevation suggests", "Acute pericarditis", ["Aortic stenosis", "Stable COPD", "Peptic ulcer disease"], "Pericarditis causes positional pleuritic pain and diffuse ECG changes.", True),
    ]),
    ("Cough, Hemoptysis and Respiratory Presentations", [
        q("Cough lasting more than 8 weeks is generally classified as", "Chronic cough", ["Acute cough", "Hyperacute cough", "Terminal cough only"], "Duration helps separate acute infection from chronic airway, reflux, drug or lung disease."),
        q("The common causes of chronic cough in nonsmokers with normal chest radiograph include asthma, upper airway cough syndrome and", "Gastroesophageal reflux disease", ["Acute appendicitis", "Migraine", "Nephrolithiasis"], "Postnasal drip, asthma and GERD are common chronic cough causes."),
        q("A patient on an ACE inhibitor develops dry cough with normal examination. The best next step is", "Stop or substitute the ACE inhibitor if clinically appropriate", ["Start tuberculosis treatment immediately", "Ignore medication history", "Give opioids indefinitely"], "ACE inhibitors can cause persistent dry cough due to bradykinin accumulation.", True),
        q("Massive hemoptysis is dangerous primarily because of", "Airway obstruction and asphyxiation", ["Loss of iron over years", "Hyperglycemia", "Migraine trigger"], "Death in massive hemoptysis usually results from airway flooding rather than exsanguination."),
        q("Rust-colored sputum classically suggests", "Pneumococcal pneumonia", ["Asthma alone", "Pulmonary edema only", "Viral rhinitis"], "Pneumococcal pneumonia may produce blood-tinged rusty sputum."),
        q("A smoker has weight loss, persistent cough and recurrent hemoptysis. The key diagnosis to exclude is", "Lung cancer", ["Simple allergic rhinitis", "Benign positional vertigo", "Tension headache"], "Hemoptysis with systemic symptoms in a smoker requires malignancy evaluation.", True),
        q("Pink frothy sputum in severe dyspnea suggests", "Pulmonary edema", ["Dry pleurisy", "Uncomplicated sinusitis", "Stable angina only"], "Alveolar flooding from pulmonary edema produces frothy blood-tinged sputum."),
        q("Stridor indicates obstruction at the level of", "Upper airway or large central airway", ["Small peripheral alveoli only", "Renal pelvis", "Colon"], "Stridor is a high-pitched sound from turbulent flow through narrowed upper airway."),
        q("A child develops fever, drooling, muffled voice and inspiratory stridor. The immediate concern is", "Acute epiglottitis with threatened airway", ["Simple bronchitis", "Migraine", "Gastroenteritis"], "Drooling, toxic appearance and stridor indicate dangerous supraglottic obstruction.", True),
        q("Digital clubbing with chronic cough and purulent sputum suggests", "Bronchiectasis or chronic suppurative lung disease", ["Acute viral fever only", "Iron overdose", "Panic disorder"], "Clubbing plus chronic purulent sputum points toward structural lung disease such as bronchiectasis.", True),
    ]),
    ("Gastrointestinal and Hepatobiliary Presentations", [
        q("Dysphagia to solids that later progresses to liquids suggests", "Mechanical esophageal obstruction", ["Primary motility disorder from onset", "Functional heartburn only", "Oropharyngeal weakness only"], "Progressive solid-first dysphagia is concerning for stricture or malignancy."),
        q("Dysphagia to solids and liquids from onset suggests", "Esophageal motility disorder", ["Small bowel obstruction", "Hemorrhoids", "Appendicitis"], "Simultaneous solid-liquid dysphagia points to impaired peristalsis or sphincter relaxation."),
        q("An elderly man has progressive dysphagia, weight loss and iron deficiency anemia. The likely diagnosis to exclude is", "Esophageal carcinoma", ["Achalasia only", "Viral gastritis", "Irritable bowel syndrome"], "Progressive dysphagia with weight loss is an alarm presentation for cancer.", True),
        q("Bilious vomiting implies obstruction distal to the", "Ampulla of Vater", ["Mouth", "Upper esophageal sphincter", "Pylorus always"], "Bile enters the duodenum at the ampulla, so bilious emesis implies distal access to bile."),
        q("Severe epigastric pain radiating to the back with high lipase suggests", "Acute pancreatitis", ["Acute cystitis", "Migraine", "Nephrotic syndrome"], "Pancreatic inflammation causes epigastric pain radiating posteriorly and elevated lipase."),
        q("A patient with cirrhosis vomits large amounts of blood and is hypotensive. The priority diagnosis is", "Variceal upper gastrointestinal bleeding", ["Hemorrhoids", "Anal fissure", "Simple dyspepsia"], "Portal hypertension predisposes to life-threatening variceal hemorrhage.", True),
        q("Painless jaundice with weight loss and palpable gallbladder suggests", "Pancreatic head malignancy", ["Gilbert syndrome", "Acute viral rhinitis", "Hemolysis only"], "Obstructive painless jaundice with Courvoisier sign suggests malignant obstruction."),
        q("Dark urine and pale stools in jaundice indicate", "Conjugated hyperbilirubinemia with cholestasis", ["Unconjugated bilirubin only", "No bilirubin disorder", "Pure anemia"], "Conjugated bilirubin is water soluble and appears in urine; lack of bile pigments lightens stool."),
        q("Right lower quadrant pain migrating from periumbilical area with fever suggests", "Acute appendicitis", ["Peptic ulcer without perforation", "Migraine", "Stable angina"], "Visceral periumbilical pain localizing to RLQ reflects appendiceal inflammation reaching parietal peritoneum.", True),
        q("Chronic watery diarrhea that persists during fasting suggests", "Secretory diarrhea", ["Osmotic diarrhea", "Constipation", "Pure dysphagia"], "Secretory diarrhea continues despite fasting and may cause large-volume stool.", True),
    ]),
    ("Renal, Urinary and Fluid-Electrolyte Presentations", [
        q("Oliguria in adults is commonly defined as urine output less than", "400 mL per day", ["2 L per day", "5 L per day", "Only one missed void", "10 mL per kg per hour"], "Oliguria indicates markedly reduced urine output and requires prompt assessment."),
        q("Prerenal azotemia is suggested by", "Low renal perfusion with avid sodium and water retention", ["Primary glomerular rupture always", "Absent ADH", "Excess urine sodium despite hypovolemia"], "Hypovolemia or low effective arterial volume reduces GFR before intrinsic injury occurs."),
        q("A vomiting patient has hypotension, dry mucosa, high BUN:creatinine ratio and concentrated urine. The likely process is", "Prerenal acute kidney injury", ["Postrenal obstruction only", "Nephrotic syndrome", "Diabetes insipidus"], "Volume depletion causes prerenal AKI with urea reabsorption and concentrated urine.", True),
        q("Nephritic syndrome is characterized by", "Hematuria, hypertension, reduced GFR and variable proteinuria", ["Massive proteinuria without cells only", "Isolated glycosuria", "Pure urinary retention"], "Glomerular inflammation causes blood, casts, hypertension and renal impairment."),
        q("Nephrotic-range proteinuria in adults is usually", "More than 3.5 g/day", ["More than 150 mg/day", "Any positive dipstick", "Less than 30 mg/day"], "Nephrotic syndrome requires heavy proteinuria with edema and hypoalbuminemia."),
        q("A patient has cola-colored urine, edema and red cell casts after pharyngitis. The likely syndrome is", "Acute glomerulonephritis", ["Renal colic", "Cystitis only", "Diabetes insipidus"], "Hematuria with RBC casts and edema after infection suggests nephritic glomerular disease.", True),
        q("Polyuria with polydipsia and very dilute urine suggests", "Diabetes insipidus or primary polydipsia", ["Complete urinary obstruction", "Acute appendicitis", "Cluster headache"], "Water diuresis causes large volumes of dilute urine."),
        q("Dysuria with frequency and urgency most strongly suggests", "Lower urinary tract infection", ["Migraine", "Aortic dissection", "Achalasia"], "Bladder mucosal inflammation causes dysuria, frequency and urgency."),
        q("Flank pain radiating to groin with hematuria is typical of", "Ureteric colic from stone", ["Acute hepatitis", "Stable asthma", "Tension headache"], "A ureteric stone causes colicky flank-to-groin pain and microscopic or gross hematuria.", True),
        q("Severe hyponatremia most urgently threatens the patient by causing", "Cerebral edema with seizures or coma", ["Isolated jaundice", "Hemoptysis", "Clubbing"], "Low extracellular sodium drives water into brain cells and can produce neurologic emergencies.", True),
    ]),
    ("Hematologic, Immune and Skin Presentations", [
        q("Anemia becomes symptomatic mainly because it", "Reduces oxygen delivery to tissues", ["Raises serum sodium", "Blocks bile flow", "Increases oncotic pressure"], "Fatigue, dyspnea and tachycardia reflect reduced oxygen-carrying capacity."),
        q("Pancytopenia points to disease affecting", "Bone marrow production or peripheral destruction/sequestration", ["Only the gallbladder", "Only vestibular apparatus", "Only esophageal motility"], "Reduction in all three cell lines suggests marrow failure, infiltration, hypersplenism or immune destruction."),
        q("A patient has fever, bruising, pallor and blasts on peripheral smear. The likely diagnosis is", "Acute leukemia", ["Iron deficiency alone", "Atopic dermatitis", "Stable angina"], "Marrow replacement by blasts causes anemia, thrombocytopenia, infection and circulating blasts.", True),
        q("Petechiae usually indicate", "Platelet number or platelet function abnormality", ["Deep factor deficiency only", "Pure cholestasis", "Peripheral neuropathy"], "Small nonblanching spots arise from capillary bleeding often due to platelet disorders."),
        q("Hemarthrosis is most typical of", "Coagulation factor deficiency", ["Thrombocytopenia only", "Urticaria", "Iron deficiency without bleeding"], "Deep joint bleeding is characteristic of hemophilia and related factor defects."),
        q("A young man has recurrent knee hemarthroses and prolonged aPTT with normal platelet count. The likely disorder is", "Hemophilia", ["Immune thrombocytopenia", "Vitamin B12 deficiency", "Sickle trait only"], "Factor VIII or IX deficiency causes deep bleeding and isolated aPTT prolongation.", True),
        q("Generalized lymphadenopathy suggests", "Systemic infection, autoimmune disease or malignancy", ["Only local skin trauma", "Normal aging always", "Simple dehydration"], "Multiple nodal regions require a systemic differential."),
        q("Urticaria consists of", "Transient pruritic wheals from dermal edema", ["Fixed scaly plaques only", "Nonblanching purpura", "Deep nodules with necrosis only"], "Histamine-mediated superficial dermal edema causes itchy wheals."),
        q("A patient develops hypotension, wheeze and urticaria minutes after injection. The immediate treatment is", "Intramuscular epinephrine", ["Oral antihistamine alone", "Delayed skin biopsy", "Loop diuretic"], "Anaphylaxis with airway or circulatory compromise requires immediate epinephrine.", True),
        q("A nonblanching palpable purpuric rash on legs with renal findings suggests", "Small-vessel vasculitis", ["Simple urticaria", "Tinea corporis", "Vitiligo"], "Palpable purpura reflects inflamed vessels with extravasated blood and may involve kidneys.", True),
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
                "id": f"medicine-cardinal-{topic_slug}-{question_order:02d}",
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
    if len(questions) != 90:
        raise AssertionError(f"Expected 90 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 90:
        raise AssertionError("Duplicate cardinal manifestation question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 90 Cardinal Manifestations questions.")


if __name__ == "__main__":
    main()
