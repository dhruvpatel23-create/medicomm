import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Neurologic Disorders"
CHAPTER_ORDER = 13
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
    ("Neurologic Diagnosis, Localization and Imaging", [
        q("Medicine 1 emphasizes that the first clues to neurologic localization usually come from the", "History", ["Serum sodium alone", "ECG", "Chest radiograph"], "Chapter 415 states that the first clues to defining the anatomic area of involvement appear in the history.", page=3025),
        q("A stocking-glove sensory loss pattern suggests disease of the", "Peripheral nerves", ["Brainstem", "Pituitary gland", "Cerebellar vermis only"], "The neurologic approach chapter contrasts stocking-glove sensory loss with peripheral nerve disease.", page=3025),
        q("A sensory level, focal back pain and incontinence suggest a lesion in the", "Spinal cord", ["Peripheral nerve only", "Neuromuscular junction", "Muscle"], "Medicine 1 lists focal back pain, sensory level and incontinence as signs favoring spinal cord origin.", True, page=3025),
        q("Cerebral localization is supported by seizures, abnormal mental status and", "Visual field abnormalities", ["Sparing of sensation", "Pure ptosis with exertion", "Stocking-glove sensory loss"], "Table 415-2 lists seizures, cognitive impairment, visual field abnormalities and unilateral deficits as cerebral signs.", page=3030),
        q("Brainstem disease can produce crossed weakness and sensory abnormalities of the head and", "Limbs", ["Kidneys", "Liver", "Adrenal cortex"], "Table 415-2 describes crossed head and limb findings as localizing to the brainstem.", page=3030),
        q("A patient has right facial weakness with left arm and leg weakness. This pattern best localizes to the", "Brainstem", ["Peripheral nerve", "Muscle", "Neuromuscular junction"], "Crossed weakness involving face on one side and limbs on the other is listed as a brainstem localization clue.", True, page=3030),
        q("Neuromuscular junction disease typically causes bilateral weakness involving face and proximal limbs with", "Sparing of sensation", ["Sensory level", "Visual field cut", "Aphasia"], "Table 415-2 describes neuromuscular junction disorders as bilateral weakness with exertional worsening and preserved sensation.", page=3030),
        q("Spinal angiography may be used before aortic aneurysm repair to identify the artery of", "Adamkiewicz", ["Heubner", "Charcot", "Berry"], "Chapter 416 notes spinal angiography may identify the artery of Adamkiewicz before aortic aneurysm repair.", page=3039),
        q("A patient with suspected cavernous sinus thrombosis has orbital pain, chemosis, fever and cranial nerves III, IV and VI palsies. The most frequent cause is infection-related", "Cavernous sinus thrombosis", ["Alzheimer disease", "Migraine aura", "Myopathy"], "Chapter 433 describes this life-threatening cavernous sinus syndrome and identifies thrombosis secondary to infection as the most frequent cause.", True, page=3172),
        q("The Glasgow Coma Scale assesses motor function, verbal responses and", "Eye opening", ["Deep tendon reflex grade only", "Pupillary color", "Serum glucose"], "Chapter 435 states that GCS grades TBI by motor, verbal and eye-opening responses.", True, page=3183),
    ]),
    ("Seizures, Stroke and Headache Disorders", [
        q("In pregnancy, antiepileptic therapy should generally use monotherapy at the lowest effective dose when possible, especially during the", "First trimester", ["Postpartum year only", "Third trimester only", "Last 24 hours before delivery"], "Chapter 418 recommends effective drug therapy with monotherapy at the lowest effective dose when possible, especially in the first trimester.", page=3068),
        q("Pregnant women taking antiepileptic drugs should also take", "Folate", ["Calcitonin", "Warfarin", "Radioiodine"], "Medicine 1 recommends folate because antifolate effects of anticonvulsants may contribute to neural tube defects.", page=3068),
        q("A pregnant patient on phenytoin is near delivery. To reduce neonatal vitamin K-dependent clotting factor deficiency, the mother should receive oral", "Vitamin K", ["Vitamin B12", "Vitamin E only", "Calcium carbonate"], "Chapter 418 recommends oral vitamin K in the last 2 weeks of pregnancy for mothers taking enzyme-inducing antiepileptic drugs.", True, page=3068),
        q("Carbamazepine, phenytoin, phenobarbital and topiramate can reduce oral contraceptive efficacy by", "Enzyme induction", ["Increasing prolactin", "Blocking AVP", "Chelating calcium"], "The contraception section notes that these antiepileptic drugs decrease oral contraceptive efficacy through enzyme induction and other mechanisms.", page=3068),
        q("In acute stroke MRI, the difference between poor perfusion and diffusion deficit estimates the ischemic", "Penumbra", ["Aura", "Plaque", "Myelin sheath"], "Chapter 420 identifies diffusion-perfusion mismatch as an estimate of the ischemic penumbra.", page=3079),
        q("A patient 2.5 hours after aphasia and right-sided weakness has restricted diffusion in the left basal ganglia. This supports", "Acute ischemic stroke", ["Myasthenia gravis", "Fibromyalgia", "Chronic fatigue syndrome"], "The ischemic stroke chapter illustrates acute stroke with diffusion-weighted MRI soon after focal deficit onset.", True, page=3079),
        q("Routine intracranial stenting for symptomatic intracranial atherosclerosis was found harmful compared with aggressive", "Medical therapy", ["No therapy", "Pituitary surgery", "Plasma exchange"], "Chapter 421 summarizes SAMMPRIS as showing medical therapy superior and routine intracranial stenting harmful.", page=3091),
        q("Migraine is described as the most common headache-related neurologic cause of disability and affects about 15% of women and", "6% of men", ["60% of men", "1% of women", "Equal 50% of all adults"], "Chapter 422 states migraine affects about 15% of women and 6% of men over a year.", page=3096),
        q("A recurrent headache with photophobia, phonophobia, movement sensitivity, nausea and vomiting is most consistent with", "Migraine", ["Lacunar infarct", "ALS", "Cavernous sinus thrombosis"], "Medicine 1 describes migraine as episodic headache with light, sound or movement sensitivity and often nausea/vomiting.", True, page=3096),
        q("About 20-25% of migraine patients have a fourth phase called", "Aura", ["Postictal coma", "Myelitis", "Myokymia"], "Chapter 422 describes prodrome, headache and postdrome, with aura in about 20-25%.", True, page=3096),
    ]),
    ("Dementia, Movement and Ataxic Disorders", [
        q("Alzheimer disease most often presents with insidious loss of", "Episodic memory", ["Pain sensation", "Hearing only", "Deep tendon reflexes"], "Chapter 423 states typical AD presents with insidious episodic memory loss followed by slowly progressive dementia.", page=3108),
        q("Microscopic pathology of Alzheimer disease includes amyloid-beta plaques and neurofibrillary tangles composed of hyperphosphorylated", "Tau", ["Alpha-synuclein only", "Dystrophin", "Myelin basic protein"], "Medicine 1 describes AD neuritic plaques containing amyloid beta and NFTs made of hyperphosphorylated tau.", page=3108),
        q("A 74-year-old develops slowly progressive episodic memory loss and medial temporal atrophy. The most likely diagnosis is", "Alzheimer disease", ["Guillain-Barre syndrome", "Essential tremor", "Cavernous sinus syndrome"], "Chapter 423 describes typical amnestic AD with medial temporal atrophy and progressive dementia.", True, page=3108),
        q("The most common genetic cause of familial or sporadic frontotemporal dementia and ALS is an expansion in", "C9ORF72", ["HFE", "RET", "PKD1"], "Chapter 424 identifies noncoding C9ORF72 expansions as the most common genetic cause of FTD and ALS.", page=3115),
        q("CADASIL is linked to mutation in the", "NOTCH3 gene", ["AIRE gene", "BTK gene", "CFTR gene"], "The vascular dementia chapter states CADASIL is linked to NOTCH3 on chromosome 19.", page=3118),
        q("A mid-adult patient has small vessel strokes, progressive dementia and extensive white matter disease. Which diagnosis is suggested?", "CADASIL", ["Migraine without aura", "Myasthenia gravis", "Chronic fatigue syndrome"], "Medicine 1 describes CADASIL as small vessel strokes, progressive dementia and extensive white matter disease beginning in mid-adult life.", True, page=3118),
        q("True cerebellar ataxia should be distinguished from vestibular disease because cerebellar ataxia lacks prominent", "Vertiginous complaints", ["Imbalance", "Unsteady gait", "Coordination difficulty"], "The ataxia section states true cerebellar ataxia is devoid of significant dizziness or perception of movement.", page=3119),
        q("In progressive ataxia, Medicine 1 stresses that the most important management goal is to identify", "Treatable disease entities", ["Only genetic labels", "Untreatable dementia", "Benign headache"], "Chapter 431 states the most important goal is identifying treatable causes of ataxia.", page=3158),
        q("A patient with ataxia from gluten-sensitive enteropathy may improve with a", "Gluten-free diet", ["High-iodine diet", "Warfarin", "Radioiodine"], "The ataxia treatment section notes that ataxia with antigliadin antibodies and gluten-sensitive enteropathy may improve with a gluten-free diet.", True, page=3158),
        q("Vitamin E deficiency can cause ataxia, so serum vitamin E levels should be measured in selected patients and deficiency treated with", "Vitamin E therapy", ["Tolvaptan", "Thrombolysis", "Levodopa"], "Medicine 1 lists vitamin E deficiency as a treatable ataxia cause and recommends vitamin E therapy for rare affected patients.", True, page=3158),
    ]),
    ("Spinal Cord and Demyelinating Disorders", [
        q("Multiple sclerosis is an autoimmune disease of the central nervous system characterized by inflammation, demyelination, gliosis and", "Neuronal loss", ["Urate deposition", "Amyloid in myocardium", "Exocrine pancreatic failure"], "Chapter 436 defines MS by chronic inflammation, demyelination, gliosis and neuronal loss.", page=3188),
        q("MS plaques are said to be disseminated in time and", "Space", ["Blood", "Urine", "Bile"], "Medicine 1 notes MS plaques develop at different times and CNS locations, i.e., disseminated in time and space.", page=3188),
        q("A young adult has optic neuritis followed months later by spastic paraparesis with separate CNS lesions. This pattern supports", "Multiple sclerosis", ["Peripheral neuropathy only", "Myopathy", "Essential tremor"], "MS is characterized by CNS lesions separated in time and space, often affecting optic nerve and spinal cord.", True, page=3188),
        q("Acute disseminated encephalomyelitis initial treatment is with high-dose", "Glucocorticoids", ["Warfarin", "Levodopa", "Pyridostigmine only"], "Chapter 436 states ADEM is initially treated with high-dose glucocorticoids.", page=3202),
        q("ADEM patients who fail to respond within a few days may benefit from plasma exchange or", "Intravenous immunoglobulin", ["Radioiodine", "Spinal stenting", "Oral contraceptives"], "Medicine 1 recommends plasma exchange or IVIG for ADEM not responding to glucocorticoids.", page=3202),
        q("Because ADEM and MS overlap at presentation, follow-up should include routine surveillance", "Imaging", ["Bone density only", "Colonoscopy", "Thyroid scintigraphy"], "Chapter 436 states surveillance imaging after ADEM recovery is crucial to recognize subclinical MS activity.", True, page=3202),
        q("Neuromyelitis optica spectrum disorder is associated with antibodies to", "Aquaporin-4", ["Amyloid beta", "Dystrophin", "BTK"], "Chapter 437 notes opticospinal MS-like cases with AQP-4 antibodies represent NMOSD.", page=3204),
        q("Up to 40% of neuromyelitis optica patients have a systemic", "Autoimmune disorder", ["Primary bone tumor", "Isolated renal stone", "Pheochromocytoma"], "Medicine 1 states up to 40% of NMO patients have systemic autoimmune disorders such as SLE or Sjogren syndrome.", page=3204),
        q("A patient with NMO attack fails high-dose methylprednisolone. Which empiric acute therapy is used?", "Plasma exchange", ["Bariatric surgery", "Intracranial stenting", "Oral vitamin K"], "Chapter 437 states plasma exchange is used for acute NMO episodes that do not respond to glucocorticoids.", True, page=3204),
        q("Given the unfavorable untreated natural history of NMO, most patients require prophylaxis against", "Relapses", ["Migraine triggers", "Calcium stones only", "Seizure contraception failure only"], "Medicine 1 recommends relapse prophylaxis for most NMO patients.", True, page=3204),
    ]),
    ("Peripheral Nerve, Neuromuscular Junction and Muscle Disorders", [
        q("Most plexopathy evaluations include imaging with MRI and", "Electrodiagnostic evaluations", ["ERCP", "Thyroid scintigraphy", "Colonoscopy"], "Chapter 438 notes most patients with plexopathies undergo MRI and EDx evaluations.", page=3225),
        q("Radiation-induced plexopathy may develop months or years after therapy and is", "Dose dependent", ["Always congenital", "Never painless", "Caused by BTK mutation"], "Medicine 1 describes radiation-induced plexopathy as delayed and dose dependent.", page=3225),
        q("Tumor invasion of the brachial plexus is usually painful and more commonly affects the", "Lower trunk", ["Upper trunk", "Optic nerve", "Cerebellar vermis"], "Chapter 438 contrasts painful lower-trunk tumor invasion with often painless upper-trunk radiation injury.", page=3225),
        q("A cancer survivor has painless upper-trunk plexopathy and EMG shows myokymic discharges. Which cause is strongly suggested?", "Radiation-induced plexopathy", ["Tumor invasion", "Migraine", "Alzheimer disease"], "Medicine 1 states myokymic discharges strongly suggest radiation-induced damage.", True, page=3225),
        q("Anti-Hu paraneoplastic neuropathy manifests as selective damage to sensory nerve bodies in the", "Dorsal root ganglia", ["Anterior horn only", "Cerebellar cortex", "Pituitary stalk"], "Chapter 439 describes anti-Hu paraneoplastic neuropathy as a sensory neuronopathy affecting dorsal root ganglia.", page=3232),
        q("More than half of subacute sensory neuronopathy cases are paraneoplastic, primarily related to", "Small-cell lung cancer", ["Papillary thyroid cancer", "Colon polyp", "Renal cyst"], "Medicine 1 states more than half are paraneoplastic and primarily related to lung cancer, mostly SCLC.", page=3232),
        q("A smoker develops asymmetric dysesthesias progressing to severe sensory ataxia and anti-Hu antibody positivity. The underlying tumor to search for is most often", "Small-cell lung cancer", ["Medullary thyroid carcinoma", "Prolactinoma", "Parathyroid adenoma"], "The anti-Hu section links this sensory neuronopathy most often to small-cell lung cancer.", True, page=3232),
        q("In myasthenia gravis follow-up, spirometry with forced vital capacity and inspiratory/expiratory pressures is important to monitor", "Respiratory status", ["Liver fibrosis", "Bone density", "Radioiodine uptake"], "Chapter 440 recommends FVC and respiratory pressure monitoring when assessing MG treatment and status.", page=3239),
        q("A patient with myasthenia gravis develops worsening weakness after a new medication. Medicine 1 advises that drugs known to exacerbate MG should be", "Avoided whenever possible", ["Used at maximum dose", "Given only with iodine", "Combined with warfarin"], "The MG chapter states listed drugs that can exacerbate weakness should be avoided whenever possible.", True, page=3239),
        q("Chronic fatigue syndrome is characterized by persistent unexplained fatigue causing severe impairment in", "Daily functioning", ["Serum calcium only", "Visual acuity only", "Spleen filtration"], "Chapter 442 defines CFS by persistent unexplained fatigue with severe impairment in daily functioning.", True, page=3254),
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
                "id": f"medicine-neurologic-disorders-{topic_slug}-{question_order:02d}",
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
    if len(questions) != 50:
        raise AssertionError(f"Expected 50 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 50:
        raise AssertionError("Duplicate neurologic question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 50 book-based Neurologic Disorders questions.")


if __name__ == "__main__":
    main()
