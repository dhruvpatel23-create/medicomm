import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Disorders of the Kidney and Urinary Tract"
CHAPTER_ORDER = 9
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
    ("Renal Physiology and Acute Kidney Injury", [
        q("In Medicine 1 chapter 303, movement of solute sequentially across apical and basolateral membranes is called", "Cellular transport", ["Paracellular transport", "Glomerular filtration", "Tubular obstruction"], "Chapter 303 distinguishes cellular transport across cell membranes from paracellular transport between adjacent cells.", page=2091),
        q("The proximal tubule contains leaky epithelia best suited for", "Bulk fluid reabsorption", ["Fine final sodium regulation only", "Urine storage", "Erythropoiesis"], "Medicine 1 notes that leaky proximal tubule epithelia permit high-capacity fluid reabsorption.", page=2093),
        q("The proximal tubule reabsorbs approximately what fraction of filtered sodium chloride and water?", "60%", ["10%", "25%", "100%"], "Chapter 303 states the proximal tubule reabsorbs about 60% of filtered NaCl and water.", page=2095),
        q("A patient given acetazolamide develops alkaline urine. Which proximal tubular process is being inhibited?", "Carbonic anhydrase-dependent bicarbonate reabsorption", ["Aldosterone-mediated potassium secretion", "Urea recycling in inner medulla", "ADH insertion of aquaporin-2 only"], "Carbonic anhydrase inhibitors block proximal tubule bicarbonate reabsorption and alkalinize urine.", True, page=2095),
        q("Type A intercalated cells in the collecting duct primarily mediate", "Acid secretion through an apical H+-ATPase", ["Glucose reabsorption by SGLT", "Renin secretion", "Urea filtration"], "Medicine 1 describes type A intercalated cells as acid-secreting cells with apical proton pumps.", page=2097),
        q("AKI is defined in chapter 304 as impairment of kidney filtration and excretory function over", "Days to weeks", ["Seconds only", "Decades only", "A fixed period of exactly 6 months"], "Chapter 304 defines AKI as impaired filtration and excretion developing over days to weeks.", page=2099),
        q("The traditional three broad categories of AKI are prerenal azotemia, intrinsic renal disease and", "Postrenal obstruction", ["Nephrotic syndrome", "Renal tubular acidosis", "Polycystic kidney disease"], "Medicine 1 divides AKI into prerenal, intrinsic and postrenal causes.", page=2099),
        q("A dehydrated patient has rising BUN/creatinine, low JVP and rapid improvement after restoring perfusion. Which AKI category is most likely?", "Prerenal azotemia", ["Acute interstitial nephritis", "Postrenal obstruction", "Renal vein thrombosis"], "Prerenal azotemia is due to inadequate renal plasma flow and is rapidly reversible when perfusion is restored.", True, page=2099),
        q("Which drug combination poses a particularly high risk for prerenal azotemia by blocking afferent vasodilation and efferent vasoconstriction?", "NSAID plus ACE inhibitor or ARB", ["Acetaminophen plus folate", "Insulin plus glucose", "Levothyroxine plus vitamin D"], "NSAIDs limit renal prostaglandin-mediated afferent vasodilation, while ACE inhibitors/ARBs limit efferent vasoconstriction.", True, page=2101),
        q("Contrast nephropathy typically begins 24-48 hours after exposure, peaks within 3-5 days and usually resolves within", "1 week", ["1 hour", "6 months", "5 years"], "Chapter 304 describes the usual course of contrast nephropathy as rise in creatinine after 24-48 h, peak at 3-5 days and recovery within a week.", True, page=2103),
    ]),
    ("Chronic Kidney Disease, Dialysis and Glomerular Disease", [
        q("In Medicine 1, chronic kidney disease is generally defined by kidney damage or reduced GFR persisting for at least", "3 months", ["24 hours", "1 week", "10 years"], "The CKD chapter uses chronicity of at least 3 months to distinguish CKD from acute kidney injury.", page=2111),
        q("The most common global causes of CKD and kidney failure include diabetes mellitus and", "Hypertension", ["Migraine", "Asthma", "Otitis media"], "Medicine 1 emphasizes diabetes and hypertension as leading causes of CKD and end-stage kidney disease.", page=2111),
        q("A patient with long-standing CKD has fatigue, normal MCV anemia and no bleeding. Reduced renal production of which hormone best explains this?", "Erythropoietin", ["Aldosterone", "Insulin", "Thyroxine"], "Loss of renal endocrine function in CKD contributes to normocytic anemia through reduced erythropoietin.", True, page=2111),
        q("A patient with advanced kidney failure develops anorexia, nausea, pruritus and confusion from retained solutes. This clinical syndrome is called", "Uremia", ["Nephrolithiasis", "Renal colic", "Postrenal diuresis"], "Advanced kidney failure produces uremic manifestations from solutes normally cleared by the kidneys.", True, page=2111),
        q("Hemodialysis removes solutes across a semipermeable membrane primarily by", "Diffusion down concentration gradients", ["Active secretion by renal tubules", "Bile excretion", "Pulmonary ventilation"], "Dialysis substitutes for kidney solute clearance using diffusion across a semipermeable membrane.", page=2121),
        q("Peritoneal dialysis uses which structure as the dialysis membrane?", "The peritoneal membrane", ["The pleura", "The mitral valve", "The bladder neck"], "Medicine 1 describes peritoneal dialysis as using the patient's peritoneal membrane for solute and water exchange.", page=2121),
        q("A dialysis patient develops fever and cloudy peritoneal effluent. Which complication should be suspected?", "Peritonitis", ["Aortic stenosis", "Pneumothorax", "Hyperthyroidism"], "Cloudy effluent with fever in peritoneal dialysis is classic for peritonitis.", True, page=2121),
        q("Nephritic glomerular disease classically presents with hematuria, reduced GFR and", "Hypertension", ["Pure glucosuria", "Isolated high serum calcium", "Low serum amylase"], "Glomerular inflammation commonly causes hematuria, impaired filtration, salt retention and hypertension.", page=2132),
        q("Nephrotic syndrome is characterized by heavy proteinuria, hypoalbuminemia and", "Edema", ["Polycythemia", "Hyperventilation", "Pupillary dilation"], "Protein loss with reduced oncotic pressure produces edema in nephrotic syndrome.", page=2132),
        q("A patient has edema, frothy urine, serum albumin 2.1 g/dL and heavy proteinuria. Which glomerular syndrome fits best?", "Nephrotic syndrome", ["Prerenal azotemia", "Renal colic", "Type 1 renal tubular acidosis"], "The combination of heavy proteinuria, hypoalbuminemia and edema is nephrotic syndrome.", True, page=2132),
    ]),
    ("Cystic Kidney Disease, Nephrolithiasis and Urinary Obstruction", [
        q("Autosomal dominant polycystic kidney disease is associated with mutations in", "PKD1 and PKD2", ["HBB and HBA", "CFTR only", "BRCA1 and BRCA2"], "Medicine 1 table 309-1 lists PKD1 and PKD2 for ADPKD.", page=2151),
        q("Extrarenal features of ADPKD include liver and pancreatic cysts, hypertension and", "Subarachnoid hemorrhage from intracranial aneurysm", ["Primary adrenal failure", "Bronchial asthma", "Myasthenia gravis"], "The inherited cystic disease table and text highlight intracranial aneurysm/subarachnoid hemorrhage risk in ADPKD.", page=2151),
        q("A patient with ADPKD and family history of intracranial aneurysm asks about screening. Medicine 1 notes presymptomatic screening may be done by", "MR angiography", ["Plain KUB x-ray", "Spirometry", "Skin prick testing"], "ADPKD patients with positive family history of intracranial aneurysm may undergo MR angiography screening.", True, page=2153),
        q("A man with an affected parent is found to have multiple cysts in both kidneys. Which diagnosis is supported by this family pattern and imaging?", "Autosomal dominant polycystic kidney disease", ["Von Hippel-Lindau disease only", "Acute tubular necrosis", "Type 1 renal tubular acidosis"], "Chapter 309 states ADPKD diagnosis is usually by compatible family history and multiple bilateral renal cysts.", True, page=2153),
        q("Von Hippel-Lindau disease is an autosomal dominant cancer syndrome caused by mutations in", "The VHL tumor-suppressor gene", ["UMOD", "MUC1", "NPHP1"], "Medicine 1 describes VHL as an autosomal dominant condition due to VHL tumor-suppressor gene mutations.", page=2155),
        q("Risk of stone formation more than doubles when urine output is below", "1 L/day", ["5 L/day", "10 L/day", "500 mL/hour"], "Chapter 312 states stone risk more than doubles when urine output is <1 L/day.", page=2169),
        q("A recurrent calcium oxalate stone former has low urine volume. The most important modifiable preventive measure is", "Increase fluid intake to raise urine volume", ["Restrict all dietary calcium completely", "Avoid all potassium-rich foods", "Take vitamin C supplements"], "Fluid intake is the main determinant of urine volume and low urine volume is a common modifiable stone risk.", True, page=2169),
        q("More than half of first-time stone formers will have recurrence within", "10 years", ["1 week", "1 month", "50 years"], "Medicine 1 chapter 312 notes that more than half of first-time stone formers recur within 10 years.", page=2171),
        q("Obstruction to urine flow causes stasis and elevated urinary tract pressure, producing", "Obstructive nephropathy", ["Membranous nephropathy", "Respiratory alkalosis", "Hepatic encephalopathy"], "Chapter 313 defines obstructive nephropathy as kidney disease from urinary tract obstruction.", page=2173),
        q("An older man has unexplained renal failure; obstruction is suspected. The diagnostic algorithm first recommends", "Insert a bladder catheter", ["Start amphotericin", "Give thrombolysis", "Perform coronary angiography"], "Medicine 1 chapter 313's algorithm begins suspected obstruction workup with bladder catheterization.", True, page=2175),
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
                "id": f"medicine-kidney-urinary-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate kidney/urinary question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 30 book-based Disorders of the Kidney and Urinary Tract questions.")


if __name__ == "__main__":
    main()
