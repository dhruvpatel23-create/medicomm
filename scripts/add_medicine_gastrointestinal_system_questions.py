import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Disorders of the Gastrointestinal System"
CHAPTER_ORDER = 10
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
    ("Approach, Endoscopy and Esophageal Disease", [
        q("In Medicine 1 chapter 314, the two main functions of the gastrointestinal tract are nutrient assimilation and", "Waste elimination", ["Erythropoiesis", "Ventilation", "Urine concentration"], "Chapter 314 describes the GI tract as serving two main functions: assimilating nutrients and eliminating waste.", page=2177),
        q("The lower esophageal sphincter normally helps prevent", "Oral reflux of gastric contents", ["Bile formation", "Colonic fermentation", "Pancreatic enzyme activation"], "The esophageal overview states that the lower esophageal sphincter prevents reflux of gastric contents.", page=2177),
        q("Achalasia is characterized by impaired esophageal body peristalsis and", "Incomplete lower esophageal sphincter relaxation", ["Excess gastric acid secretion only", "Rapid gastric emptying", "Colonic mucosal ulceration"], "Medicine 1 lists achalasia among delayed transit disorders and defines it by impaired peristalsis with incomplete LES relaxation.", page=2178),
        q("A patient has progressive dysphagia and weight loss. Which investigation is a common indication according to the GI endoscopy table?", "Upper endoscopy", ["Spirometry", "Electroencephalography", "Renal biopsy"], "The common indications table lists dysphagia and weight loss among indications for upper endoscopy.", True, page=2180),
        q("Iron-deficiency anemia in a patient with GI symptoms suggests", "Mucosal blood loss", ["Pure adrenal failure", "Primary hyperventilation", "Excess vitamin B12 intake"], "Chapter 314 notes that iron-deficiency anemia suggests mucosal blood loss.", page=2180),
        q("Colonoscopy is described in chapter 315 as the gold standard for imaging", "The colonic mucosa", ["The myocardium", "The renal pelvis", "The alveolar wall"], "Medicine 1 states that colonoscopy is the gold standard for imaging the colonic mucosa.", page=2183),
        q("Capsule endoscopy is most useful because it visualizes small bowel mucosa beyond the reach of", "A conventional endoscope", ["A chest radiograph", "A bladder catheter", "A pulmonary artery catheter"], "Chapter 315 describes capsule endoscopy as allowing visualization of small bowel mucosa beyond conventional endoscopic reach.", page=2183),
        q("A patient with obscure gastrointestinal bleeding has nondiagnostic EGD and colonoscopy. Which endoscopic test is most directly suited to inspect the small bowel mucosa?", "Capsule endoscopy", ["Flexible bronchoscopy", "Cystoscopy", "Arthroscopy"], "The endoscopy chapter lists capsule endoscopy for obscure GI bleeding and small bowel evaluation.", True, page=2180),
        q("A patient with suspected esophageal stricture undergoes barium radiography. Sensitivity is improved when the study is performed with", "A 13-mm barium tablet", ["A lactose breath test", "A water deprivation test", "A methacholine challenge"], "Medicine 1 notes that barium radiography sensitivity for esophageal strictures is greater when combined with a 13-mm barium tablet.", True, page=2210),
        q("A patient with suspected achalasia has normal structural imaging. Which functional test is specifically useful?", "Esophageal manometry", ["Sweat chloride testing", "Audiometry", "Bone densitometry"], "Chapter 314 describes esophageal manometry as useful when achalasia is suspected.", True, page=2181),
    ]),
    ("Peptic Ulcer, Malabsorption and Inflammatory Bowel Disease", [
        q("The stomach secretes intrinsic factor, which is needed for absorption of", "Vitamin B12", ["Vitamin C", "Iron only", "Folate only"], "The GI function section states that the stomach secretes intrinsic factor for vitamin B12 absorption.", page=2177),
        q("Gastric outlet obstruction can develop from peptic ulcer disease or", "Gastric cancer", ["Migraine", "Asthma", "Hyperthyroidism only"], "Medicine 1 lists peptic ulcer disease and gastric cancer as causes of gastric outlet obstruction.", page=2178),
        q("A patient with chronic diarrhea has bulky greasy stools. This finding most strongly suggests", "Malabsorption", ["Pure irritable bowel syndrome", "Isolated anxiety", "Upper airway disease"], "Chapter 314 states that steatorrhea develops with malabsorption.", True, page=2179),
        q("A patient with epigastric pain has persistent vomiting from gastric outlet obstruction. Which underlying disorder is specifically listed as a cause?", "Peptic ulcer disease", ["Aortic stenosis", "Nephrolithiasis", "Pneumothorax"], "Medicine 1 lists peptic ulcer disease as a cause of gastric outlet obstruction.", True, page=2178),
        q("Pus and blood in stool are more characteristic of inflammatory bowel disease than", "Irritable bowel syndrome", ["Acute myocardial infarction", "Renal tubular acidosis", "Hypothyroid coma"], "The altered bowel habits section contrasts fecal mucus in IBS with pus and blood in IBD.", page=2179),
        q("Crohn disease can cause small-intestinal obstruction through", "Inflammatory strictures", ["Lower esophageal sphincter relaxation", "Alveolar collapse", "Coronary vasospasm"], "Chapter 314 lists Crohn disease among causes of small-intestinal obstruction from stricturing disease.", page=2178),
        q("CT or MR enterography is used in inflammatory bowel disease to quantify", "Disease intensity", ["Creatinine clearance", "Airway resistance", "Left ventricular ejection fraction"], "The imaging section notes that specialized CT or MR enterography quantifies IBD intensity.", page=2181),
        q("A patient with chronic diarrhea has fecal urgency, blood and pus. Which diagnosis group is favored over IBS?", "Inflammatory bowel disease", ["Functional constipation", "Biliary colic", "Benign positional vertigo"], "Medicine 1 says pus and blood characterize IBD, while mucus is common in IBS.", True, page=2179),
        q("Endoscopic mucosal biopsies are used to evaluate inflammatory, infectious and", "Neoplastic disease", ["Pulmonary hypertension", "Cardiac arrhythmia", "Bone marrow failure only"], "Chapter 314 states that endoscopic mucosal biopsies evaluate inflammatory, infectious and neoplastic disease.", page=2181),
        q("A patient with suspected Crohn disease limited to the small intestine is an appropriate candidate for which endoscopic modality from table 314-2?", "Capsule endoscopy", ["Laryngoscopy", "Pleural biopsy", "Coronary angiography"], "The common indications table lists suspected small-intestinal Crohn disease under capsule endoscopy.", True, page=2180),
    ]),
    ("Intestinal, Colorectal and Acute Abdominal Disorders", [
        q("The most common cause of small-intestinal obstruction listed in Medicine 1 is", "Adhesions", ["Colon cancer", "Hyperthyroidism", "Vitamin B12 deficiency"], "Chapter 314 states that small-intestinal obstruction most commonly results from adhesions.", page=2178),
        q("The most common cause of colonic obstruction listed in chapter 314 is", "Colon cancer", ["Celiac disease", "Achalasia", "Gastroparesis"], "Medicine 1 identifies colon cancer as the most common cause of colonic obstruction.", page=2178),
        q("IBS may produce constipation, diarrhea or", "An alternating bowel pattern", ["Obstructive jaundice only", "Hematemesis only", "Portal hypertension only"], "The altered bowel habits section notes that IBS can produce constipation, diarrhea or alternating bowel habits.", page=2179),
        q("A patient with crampy abdominal pain, vomiting, distention and previous abdominal surgery most likely has small-bowel obstruction due to", "Adhesions", ["Achalasia", "Barrett esophagus", "Hemorrhoids"], "Adhesions are the most common cause of small-intestinal obstruction in Medicine 1, especially after surgery.", True, page=2178),
        q("A patient with ileus has marked vomiting and upper gut distention. Nasogastric tube suction is used to", "Decompress the upper gut", ["Ablate Barrett mucosa", "Screen for colon cancer", "Treat chronic hepatitis"], "The therapy section states that nasogastric tube suction decompresses the upper gut in ileus or mechanical obstruction.", True, page=2182),
        q("Transplantation of donor feces into the colon is accepted and effective for recurrent refractory", "Clostridium difficile colitis", ["Acute viral hepatitis A", "Biliary colic", "Achalasia"], "Chapter 314 describes fecal microbiota transplantation as accepted effective therapy for recurrent refractory C. difficile colitis.", page=2182),
        q("Radionuclide scans in brisk GI hemorrhage help localize bleeding sites to direct endoscopy, angiography or", "Surgery", ["Spirometry", "Hemodialysis", "Phototherapy"], "The scintigraphy section notes that radionuclide scans localize brisk hemorrhage to guide endoscopy, angiography or surgery.", page=2181),
        q("A patient with recurrent refractory C. difficile colitis after standard therapy is considered for colonoscopic donor stool infusion. This is", "Fecal microbiota transplantation", ["ERCP", "Esophageal manometry", "Barium swallow"], "Medicine 1 notes transplantation of donor feces by colonoscopy or enema for recurrent refractory C. difficile colitis.", True, page=2182),
        q("Colonoscopy can be therapeutic in acute colonic pseudoobstruction by", "Withdrawing luminal gas", ["Increasing portal pressure", "Activating trypsinogen", "Secreting intrinsic factor"], "Chapter 314 lists colonoscopic withdrawal of luminal gas for some cases of acute colonic pseudoobstruction.", page=2182),
        q("A patient with brisk lower GI bleeding needs localization before therapy. Which nuclear medicine test role is described in chapter 314?", "Radionuclide scan to localize the bleeding site", ["Secretin stimulation to measure acid", "MR angiography for aneurysm screening", "Sweat chloride testing"], "Medicine 1 describes radionuclide scans as localizing bleeding sites in brisk hemorrhage to direct therapy.", True, page=2181),
    ]),
    ("Liver, Biliary and Pancreatic Disorders", [
        q("ERCP is commonly indicated for jaundice, cholangitis, gallstone pancreatitis and", "Pancreaticobiliary drainage", ["Colon cancer screening", "Spirometry calibration", "Renal stone dissolution"], "The common indications table lists pancreaticobiliary conditions and drainage under ERCP.", page=2180),
        q("MR methods can image pancreaticobiliary ducts to exclude neoplasm, stones and", "Sclerosing cholangitis", ["Asthma", "Glomerulonephritis", "Aortic regurgitation"], "The imaging section states that MR methods image ducts to exclude neoplasm, stones and sclerosing cholangitis.", page=2181),
        q("A patient with suspected acute cholecystitis has an equivocal ultrasound. Biliary scintigraphy complements ultrasound in assessing for", "Cholecystitis", ["Achalasia", "Celiac sprue", "Hemorrhoids"], "Chapter 314 states that biliary scintigraphy complements ultrasound for cholecystitis assessment.", True, page=2181),
        q("A patient with jaundice and suspected bile duct stones needs a test that can also provide pancreaticobiliary drainage. Which procedure fits best?", "ERCP", ["Capsule endoscopy", "Flexible sigmoidoscopy", "Esophageal manometry"], "Medicine 1 table 314-2 lists jaundice, bile duct stones and pancreaticobiliary drainage as ERCP indications.", True, page=2180),
        q("Liver biopsy is performed for abnormal liver chemistries, unexplained jaundice and after transplant to exclude", "Rejection", ["Achalasia", "Appendicitis", "Gastric outlet obstruction"], "The histopathology section lists post-transplant liver biopsy to exclude rejection.", page=2181),
        q("The pancreas normally secretes 1500-3000 mL per day of isosmotic alkaline fluid with pH", "Greater than 8", ["Less than 2", "Exactly 7.0", "Less than 5 only"], "Chapter 341 describes pancreatic exocrine secretion as 1500-3000 mL/day of isosmotic alkaline fluid with pH greater than 8.", page=2437),
        q("Acute pancreatitis results when proteolytic enzymes are activated in the pancreatic acinar cell rather than", "The intestinal lumen", ["The alveolus", "The renal pelvis", "The bone marrow"], "The pancreatitis chapter describes premature intrapancreatic enzyme activation as central to autodigestion.", page=2439),
        q("A patient has severe epigastric pain radiating to the back and serum lipase more than three times normal. This meets which diagnostic criterion pair for acute pancreatitis?", "Typical pain plus enzyme elevation", ["Mucus stool plus normal imaging", "Dysphagia plus barium tablet retention", "Ascites plus low albumin only"], "Medicine 1 diagnosis requires two of three: typical epigastric/back pain, lipase or amylase at least threefold elevated, or imaging findings.", True, page=2440),
        q("The recommended initial emergency imaging modality for acute pancreatitis is", "Abdominal ultrasound", ["Barium enema", "Colonoscopy", "Brain MRI"], "Chapter 341 recommends abdominal ultrasound in the emergency ward as initial diagnostic imaging, especially for gallstone disease.", page=2440),
        q("A patient with acute pancreatitis has BUN over 25 mg/dL, impaired mental status, SIRS, age over 60 and pleural effusion. These variables make up which severity score?", "BISAP", ["CHA2DS2-VASc", "CURB-65 only", "MELD-Na"], "Medicine 1 lists BISAP as BUN, impaired mental status, SIRS, age over 60 and pleural effusion.", True, page=2443),
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
                "id": f"medicine-gastrointestinal-system-{topic_slug}-{question_order:02d}",
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
    if len(questions) != 40:
        raise AssertionError(f"Expected 40 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 40:
        raise AssertionError("Duplicate gastrointestinal question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 40 book-based Disorders of the Gastrointestinal System questions.")


if __name__ == "__main__":
    main()
