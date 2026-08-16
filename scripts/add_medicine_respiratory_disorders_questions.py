import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Disorders of the Respiratory System"
CHAPTER_ORDER = 7
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
    ("Diagnosis of Respiratory Disorders", [
        q("In Medicine 1 chapter 278, most respiratory diseases presenting with cough or dyspnea are grouped into obstructive, restrictive and which third major category?", "Abnormalities of the pulmonary vasculature", ["Primary disorders of erythropoiesis", "Diseases limited to the upper airway", "Disorders of hepatic ventilation"], "Chapter 278 classifies common respiratory presentations into obstructive lung disease, restrictive disorders and pulmonary vascular abnormalities.", page=1943),
        q("Which group is listed as obstructive lung disease in the opening approach to respiratory disorders?", "Asthma, COPD, bronchiectasis and bronchiolitis", ["Idiopathic pulmonary fibrosis, kyphoscoliosis and pleural effusion", "Pulmonary embolism, pulmonary hypertension and venoocclusive disease", "Sarcoidosis, cirrhosis and nephrosis"], "Medicine 1 names asthma, COPD, bronchiectasis and bronchiolitis as airway-predominant obstructive disorders.", page=1943),
        q("A patient with chronic cough and dyspnea is being evaluated. Which history is essential because it raises risk for COPD, bronchogenic lung cancer and some parenchymal lung diseases?", "Current and previous cigarette smoking with pack-years", ["Daily water intake", "Hand dominance", "Childhood vaccination scar"], "Chapter 278 emphasizes asking all respiratory patients about cigarette smoking and quantifying pack-years.", True, page=1944),
        q("Which home exposure in chapter 278 is specifically relevant to hypersensitivity pneumonitis-type respiratory disease?", "Excrement from pet birds", ["Filtered drinking water", "Use of cotton clothing", "Sleeping on a firm mattress"], "The book lists home exposures such as pet bird excrement among inhalational exposures to explore.", page=1944),
        q("Initial chest imaging in many respiratory disorders generally begins with ultrasound or", "A plain chest radiograph, preferably posteroanterior and lateral films", ["Pulmonary angiography in every patient", "PET scan before examination", "Mediastinoscopy"], "Chapter 278 recommends chest ultrasound or plain chest radiography as early imaging in most respiratory evaluations.", page=1945),
        q("A bedside ultrasound rapidly detects pneumothorax, pleural effusion and consolidation in an acutely dyspneic patient. This use is supported in which diagnostic chapter?", "Approach to the Patient with Disease of the Respiratory System", ["Disorders of the Mediastinum only", "Sleep Apnea only", "Lung Transplantation only"], "Medicine 1 chapter 278 notes ultrasound can rapidly diagnose pneumothorax, pleural effusion and consolidation.", True, page=1945),
        q("During forced spirometry, which value is the amount of air exhaled in the first second?", "FEV1", ["FVC", "TLC", "RV"], "Chapter 280 defines FEV1 as the volume exhaled in the first second of the forced vital capacity maneuver.", page=1951),
        q("A reduced FEV1/FVC ratio on spirometry most classically indicates", "Airflow obstruction", ["Pure anemia", "Left ventricular systolic dysfunction", "Primary metabolic acidosis"], "Medicine 1 describes FEV1/FVC as typically reduced in airflow obstruction, though severe air trapping may sometimes mask this.", page=1951),
        q("A contrast CT pulmonary angiography is ordered for acute pleuritic dyspnea because CT with contrast is useful for assessing", "Pulmonary emboli in the pulmonary vasculature", ["Bone marrow cellularity", "Esophageal motility only", "Coronary plaque calcium only"], "The diagnostic procedures chapter notes CT with contrast is particularly useful for pulmonary emboli and vascular assessment.", True, page=1954),
        q("Bronchoalveolar lavage during bronchoscopy samples", "Cells and organisms from alveolar spaces", ["Only the pleural cavity", "Only mediastinal lymph nodes", "Only chest wall muscle"], "Chapter 280 explains that wedging the bronchoscope and instilling saline allows BAL sampling of alveolar cells and organisms.", True, page=1956),
    ]),
    ("Asthma and COPD", [
        q("Medicine 1 identifies the major risk factor for asthma as", "Atopy", ["Alpha-1 antitrypsin deficiency", "Left heart failure", "Hepatic hydrothorax"], "Chapter 281 states that atopy is the major risk factor for asthma and that non-atopic individuals have low risk.", page=1958),
        q("Which clinical pattern is a major risk factor for death from asthma in chapter 281?", "Poorly controlled disease with frequent bronchodilator inhaler use", ["Mild intermittent symptoms with good ICS adherence", "Isolated allergic rhinitis without wheeze", "Normal peak flow variation"], "Medicine 1 lists poorly controlled asthma with frequent bronchodilator use, poor ICS adherence and previous near-fatal admissions as death-risk factors.", page=1958),
        q("A child with eczema and allergic rhinitis has recurrent wheeze. Which risk background from Medicine 1 best explains the asthma risk?", "Atopic disease", ["SERPINA1 null allele", "Tuberculous pleuritis", "Pleural NT-proBNP elevation"], "Asthma commonly coexists with atopic dermatitis and allergic rhinitis, with allergic rhinitis present in many asthmatic patients.", True, page=1958),
        q("The usual inflammatory pattern in asthma is characterized by infiltration of", "Eosinophils", ["Megakaryocytes", "Plasma cells only", "Hepatocytes"], "Chapter 281 describes eosinophil infiltration as the common inflammatory pattern, while some severe asthma is neutrophilic.", page=1961),
        q("Mast cells in asthma are activated by allergens mainly through", "An IgE-dependent mechanism", ["A bilirubin-dependent mechanism", "Direct hemoglobin oxidation", "Loss of surfactant protein A only"], "Medicine 1 explains that allergens activate mast cells through IgE, producing acute bronchoconstrictor responses.", page=1961),
        q("An asthmatic patient has rising use of albuterol. According to chapter 281, increased SABA use indicates", "Asthma is not controlled", ["The patient is cured", "ICS should always be stopped", "Airflow obstruction is impossible"], "The asthma chapter states that increased use of short-acting beta2 agonists indicates poor control.", True, page=1965),
        q("COPD is defined in Medicine 1 as persistent respiratory symptoms and airflow limitation that is", "Not fully reversible", ["Always completely reversible", "Only present during sleep", "Due solely to pleural fluid"], "Chapter 286 defines COPD as persistent symptoms and airflow limitation that is not fully reversible.", page=1990),
        q("Emphysema is anatomically defined by", "Destruction of lung alveoli with air-space enlargement", ["Grossly purulent pleural fluid", "Upper airway collapse during sleep", "Lymphocytic pleural exudate"], "Medicine 1 defines emphysema as alveolar destruction with enlargement of air spaces.", page=1990),
        q("A smoker with COPD has the greatest site of increased airway resistance in airways of what size?", "Airways 2 mm or less in diameter", ["Mainstem bronchi only", "Trachea only", "Pleural lymphatics only"], "Chapter 286 states the major site of increased resistance in most COPD patients is airways <=2 mm diameter.", True, page=1992),
        q("Which three COPD interventions are stated to improve survival?", "Smoking cessation, oxygen for chronic hypoxemia and LVRS in selected emphysema", ["Chronic oral steroids, theophylline and antibiotics for all", "Cough suppressants, sedatives and bed rest", "Routine bronchoscopy, PET scanning and mediastinoscopy"], "Medicine 1 chapter 286 lists smoking cessation, oxygen therapy in chronically hypoxemic patients and selected lung volume reduction surgery as survival-improving interventions.", True, page=1996),
    ]),
    ("Interstitial, Pleural, Ventilatory and Sleep Disorders", [
        q("Diffuse parenchymal lung diseases include more than 200 heterogeneous conditions affecting lung parenchyma with varying degrees of", "Inflammation and fibrosis", ["Hyperbilirubinemia and jaundice", "Thrombocytosis and bleeding", "Valvular stenosis"], "Chapter 287 introduces ILD as many disorders of lung parenchyma with inflammation and fibrosis.", page=1999),
        q("Most patients eventually diagnosed with ILD come to attention with", "Progressive exertional dyspnea or persistent dry cough", ["Massive hematemesis", "Painless hematuria", "Acute monoarthritis"], "Medicine 1 states that progressive exertional dyspnea and persistent dry cough are common presenting complaints in ILD.", page=1999),
        q("A 67-year-old man has gradual dyspnea, dry cough, basal rales, clubbing and HRCT showing subpleural basal honeycombing. Which diagnosis best matches Medicine 1?", "Idiopathic pulmonary fibrosis", ["Acute asthma", "Chylothorax", "Primary spontaneous pneumothorax"], "Chapter 287 describes IPF as older-age ILD with basal crackles, clubbing and UIP-pattern HRCT with honeycombing and traction bronchiectasis.", True, page=2002),
        q("The HRCT pattern that supports IPF includes subpleural reticulation with posterior basal predominance plus honeycombing and traction bronchiectasis, collectively called", "Usual interstitial pneumonia pattern", ["Miliary pattern", "Tree-in-bud pattern only", "Cardiogenic edema pattern"], "Medicine 1 calls this combination a UIP pattern.", page=2002),
        q("Light's criteria classify pleural fluid as exudate if pleural fluid/serum protein is greater than", "0.5", ["0.1", "1.5", "5.0"], "Chapter 288's pleural effusion algorithm uses pleural fluid/serum protein >0.5, pleural fluid/serum LDH >0.6 or pleural LDH >2/3 upper normal serum limit.", page=2007),
        q("A pleural NT-proBNP above 1500 pg/mL is virtually diagnostic of effusion due to", "Congestive heart failure", ["Chylothorax", "Pneumothorax", "Sarcoidosis"], "Medicine 1 states pleural fluid NT-proBNP >1500 pg/mL is virtually diagnostic for heart-failure-related pleural effusion.", True, page=2007),
        q("Empyema refers to", "A grossly purulent pleural effusion", ["Air in the mediastinum", "A dry cough from ILD", "Upper airway collapse during sleep"], "Chapter 288 defines empyema as a grossly purulent effusion.", page=2007),
        q("Tuberculous pleural effusion is usually an exudate with predominantly", "Small lymphocytes", ["Neutrophils only with no lymphocytes", "Eosinophils above 80% in every case", "Malignant epithelial cells always"], "Medicine 1 describes tuberculous pleural fluid as an exudate with predominantly small lymphocytes.", page=2008),
        q("A sleepy obese patient snores, has witnessed gasping and morning headaches. Medicine 1 says the most common daytime symptom of OSAHS is", "Excessive sleepiness", ["Hemoptysis", "Pleuritic chest pain", "Digital clubbing"], "Chapter 291 states the most common daytime symptom is excessive sleepiness, though some women report fatigue.", True, page=2015),
        q("Chronic hypercapnia with normal respiratory muscle strength, normal pulmonary function and normal alveolar-arterial oxygen difference should suggest", "A respiratory drive disorder", ["Pleural tuberculosis", "Primary pneumothorax", "Usual interstitial pneumonia"], "Chapter 290 advises shifting focus to respiratory drive and neuromuscular disorders when the ventilatory apparatus does not explain chronic hypercapnia.", True, page=2012),
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
                "id": f"medicine-respiratory-disorders-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate respiratory disorder question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 30 book-based Disorders of the Respiratory System questions.")


if __name__ == "__main__":
    main()
