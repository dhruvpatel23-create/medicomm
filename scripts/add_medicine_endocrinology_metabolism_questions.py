import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Endocrinology and Metabolism"
CHAPTER_ORDER = 12
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
    ("Endocrine Principles and Pituitary Disorders", [
        q("Medicine 1 states that the endocrine system is evaluated primarily by measuring", "Hormone concentrations", ["Serum albumin fractions", "Urinary casts", "Arterial oxygen tension"], "Chapter 369 emphasizes hormone concentration measurement as the primary method for endocrine evaluation.", page=2649),
        q("Endocrine deficiency disorders are generally treated with physiologic", "Hormone replacement", ["Tumor debulking only", "Antibiotic suppression", "Dialysis"], "The approach chapter states that endocrine deficiency disorders are treated with physiologic hormone replacement.", page=2649),
        q("Most endocrine hormone excess conditions are caused by benign glandular", "Adenomas", ["Thrombi", "Abscesses", "Casts"], "Chapter 369 notes that hormone excess is usually due to benign glandular adenomas.", page=2649),
        q("A patient with unexplained hypoglycemia has a sarcoma secreting an IGF-II precursor. The hypoglycemia is partly due to cross-talk with insulin and", "IGF-I receptors", ["TSH receptors", "AVP receptors", "Calcitonin receptors"], "Medicine 1 describes IGF-II precursor from tumors causing hypoglycemia through insulin and IGF-I receptor binding.", True, page=2653),
        q("PTH and PTH-related peptide both bind to the receptor called", "PTH1R", ["TSHR", "V2 receptor", "RET"], "Chapter 370 explains that PTH and PTHrP bind the PTH1R receptor in bone and kidney.", page=2653),
        q("Reduction of thyroid hormone triggers increased TRH and", "TSH", ["AVP", "Aldosterone", "Calcitonin"], "The anterior pituitary physiology chapter uses thyroid hormone feedback on TRH and TSH as a classic feedback example.", page=2659),
        q("A patient with low thyroid hormone has a rapid rise in TRH and TSH. This illustrates", "Negative feedback regulation", ["Osmotic diuresis", "Reverse cholesterol transport", "Ligand-independent signaling"], "Chapter 371 explains that reduced thyroid hormone releases feedback inhibition, increasing TRH and TSH.", True, page=2659),
        q("Positive feedback in endocrine physiology is illustrated by estrogen-mediated stimulation of the midcycle", "LH surge", ["PTH suppression", "Insulin inhibition", "Cortisol nadir"], "Medicine 1 identifies the estrogen-mediated midcycle LH surge as the main example of positive feedback.", page=2659),
        q("A child with septo-optic dysplasia has optic nerve hypoplasia, micropenis and short stature. The pituitary defect most likely includes", "Growth hormone deficiency", ["Primary hyperaldosteronism", "Medullary thyroid carcinoma", "Hyperparathyroidism"], "Chapter 372 states that septo-optic dysplasia can cause diabetes insipidus, GH deficiency and sometimes TSH deficiency.", True, page=2664),
        q("A sellar mass grows superiorly because the sellar diaphragm offers least resistance, producing local mass effects. This is typical of", "Pituitary adenoma extension", ["Primary hyperparathyroidism", "Gout", "Hemochromatosis"], "The pituitary tumor chapter notes that pituitary adenomas often extend suprasellarly because the sellar diaphragm offers least resistance.", True, page=2670),
    ]),
    ("Neurohypophysis, Thyroid and Adrenal Disorders", [
        q("The most important physiologic action of AVP is to reduce water excretion by promoting", "Urine concentration", ["Calcium excretion", "Thyroid iodination", "Insulin secretion"], "Chapter 374 states that AVP's key physiologic action is reducing water excretion by concentrating urine.", page=2684),
        q("In the absence of AVP, the distal tubule and medullary collecting duct are impermeable to", "Water", ["Glucose", "Iodide", "Cortisol"], "Medicine 1 describes these renal segments as water-impermeable without AVP.", page=2684),
        q("A nauseated patient develops a sudden 50- to 100-fold rise in plasma AVP. Which stimulus is responsible?", "Nausea", ["Mild pain alone", "Low TSH", "Hypercalcemia"], "The AVP chapter describes emetic stimuli such as nausea as extremely potent AVP secretagogues.", True, page=2684),
        q("In hypovolemic hyponatremia, fluid restriction and AVP antagonists are", "Contraindicated", ["First-line therapy", "Diagnostic tests", "Required before saline"], "Chapter 374 states that fluid restriction and AVP antagonists aggravate hypovolemia and are contraindicated.", True, page=2692),
        q("Graves disease thyroid scanning classically shows an enlarged gland with increased uptake distributed", "Homogeneously", ["Only in one cold nodule", "Only in the posterior pituitary", "In the adrenal medulla"], "The thyroid testing chapter describes Graves disease as diffuse homogeneous increased tracer uptake.", page=2698),
        q("A patient with thyrotoxicosis has very low radioiodine uptake after postpartum thyroiditis. The low uptake is best explained by", "Follicular cell damage and TSH suppression", ["Excess ACTH", "PTHrP secretion", "Ovarian failure"], "Medicine 1 notes that subacute, viral and postpartum thyroiditis have low uptake from follicular damage and TSH suppression.", True, page=2698),
        q("Thyroid scintigraphy should be performed for thyroid nodules when serum TSH is", "Subnormal", ["High-normal only", "Unavailable in all cases", "Elevated after thyroidectomy only"], "Chapter 375 says scintigraphy is not routine for nodules but should be performed if TSH is subnormal.", page=2698),
        q("Graves disease accounts for what proportion of thyrotoxicosis in Medicine 1?", "60-80%", ["1-2%", "10%", "100%"], "Chapter 377 states that Graves disease accounts for 60-80% of thyrotoxicosis.", page=2703),
        q("The adrenal cortex produces glucocorticoids, mineralocorticoids and", "Adrenal androgen precursors", ["Thyroxine", "Insulin", "Parathyroid hormone"], "Chapter 379 lists cortisol, aldosterone and DHEA-type androgen precursors as adrenal cortical hormone classes.", page=2719),
        q("A patient with pheochromocytoma plus medullary thyroid carcinoma history should be tested for which inherited syndrome gene?", "RET", ["BTK", "PKD2", "HFE"], "The pheochromocytoma chapter states that personal or family history of MTC strongly suggests MEN2 and should prompt RET testing.", True, page=2746),
    ]),
    ("Reproductive, Sex and Gender-Based Medicine", [
        q("Autoimmune polyendocrine syndromes are divided in Medicine 1 into two major categories, APS-1 and", "APS-2", ["MEN-4", "LADA", "SIADH"], "Chapter 382 states that APS is generally divided into APS-1 and APS-2.", page=2756),
        q("Kearns-Sayre syndrome is a mitochondrial DNA disorder associated with ophthalmoplegia, progressive weakness and endocrine abnormalities including", "Hypoparathyroidism", ["Primary hyperuricemia only", "Medullary thyroid cancer only", "Familial hypocalciuric hypercalcemia only"], "Medicine 1 lists hypoparathyroidism, primary gonadal failure, diabetes mellitus and hypopituitarism in Kearns-Sayre syndrome.", page=2760),
        q("DIDMOAD syndrome is also termed", "Wolfram syndrome", ["Turner syndrome", "MEN2A", "Kallmann syndrome"], "Chapter 382 identifies DIDMOAD as diabetes insipidus, diabetes mellitus, optic atrophy and deafness, also called Wolfram syndrome.", page=2760),
        q("A phenotypically normal adolescent girl has primary amenorrhea and congenital absence of the vagina with renal agenesis. Which syndrome should be considered?", "Mayer-Rokitansky-Kuster-Hauser syndrome", ["Graves disease", "Pheochromocytoma", "Alport syndrome"], "Medicine 1 states MRKH syndrome should be considered in otherwise phenotypically normal females with primary amenorrhea and vaginal absence.", True, page=2769),
        q("Long-term anabolic-androgenic steroid use suppresses LH and FSH and inhibits endogenous testosterone production and", "Spermatogenesis", ["AVP release", "PTH secretion", "Bile acid absorption"], "Chapter 385 notes that long-term AAS use suppresses the HPT axis and spermatogenesis.", page=2787),
        q("A male bodybuilder stops long-term anabolic steroid use and develops fatigue, sexual dysfunction, infertility and depressed mood. The mechanism is suppression of the", "Hypothalamic-pituitary-testicular axis", ["Renin-angiotensin system", "Vitamin D axis", "Urea cycle"], "Medicine 1 describes marked HPT-axis suppression after stopping long-term AAS.", True, page=2787),
        q("Functional hypogonadotropic delayed puberty may be caused by chronic disease, malnutrition, excessive exercise and", "Eating disorders", ["Thyroid nodule autonomy", "Medullary thyroid carcinoma", "Familial hypercholesterolemia"], "The delayed puberty table lists eating disorders among functional hypogonadotropic causes.", page=2794),
        q("A patient with dysmenorrhea fails NSAIDs and oral contraceptives. Medicine 1 says this suggests a pelvic disorder such as", "Endometriosis", ["Diabetes insipidus", "Cushing syndrome", "Osteitis fibrosa"], "Chapter 386 states that failure of NSAIDs and/or oral contraceptives suggests a pelvic disorder such as endometriosis.", True, page=2799),
        q("Menopause is diagnosed retrospectively after how long of amenorrhea?", "12 months", ["1 week", "3 months", "5 years"], "Chapter 388 defines menopause as permanent cessation of menstruation diagnosed after 12 months of amenorrhea.", page=2803),
        q("Contraindications to systemic postmenopausal hormone therapy include unexplained vaginal bleeding, liver disease, VTE and history of", "Breast cancer", ["Appendicitis", "Gout", "Diabetes insipidus"], "Medicine 1 lists breast cancer or other estrogen-dependent cancer among contraindications to systemic hormone therapy.", True, page=2810),
    ]),
    ("Obesity, Diabetes, Lipids and Metabolic Syndrome", [
        q("Obesity is associated with menstrual abnormalities, especially in women with", "Upper body obesity", ["Low HDL only", "Primary adrenal failure", "Low AVP"], "Chapter 394 notes that obesity has long been associated with menstrual abnormalities, particularly upper body obesity.", page=2843),
        q("Most obese women with oligomenorrhea have", "Polycystic ovarian syndrome", ["SIADH", "X-linked agammaglobulinemia", "Wilson disease"], "Medicine 1 states that most obese women with oligomenorrhea have PCOS.", page=2843),
        q("A woman with obesity and PCOS loses weight and resumes normal cycles. Medicine 1 notes weight loss often restores", "Normal menses", ["Radioiodine uptake", "PTH secretion", "Serum ceruloplasmin"], "Chapter 394 states that weight loss often restores normal menses in obese women with PCOS.", True, page=2843),
        q("Bariatric procedures generally produce what average total body weight loss?", "30-35%", ["1-2%", "5%", "80-90%"], "Chapter 395 states that bariatric procedures generally produce 30-35% average total body weight loss.", page=2850),
        q("In type 1 diabetes mellitus, Medicine 1 lists propensity to develop", "Ketoacidosis", ["Pheochromocytoma", "Hypercalciuria only", "Primary infertility only"], "The diabetes classification chapter contrasts type 1 DM by need for insulin and propensity for ketoacidosis.", page=2859),
        q("A lean adult initially labeled type 2 diabetes has GAD autoantibodies and progressive insulin need. This is most consistent with", "Latent autoimmune diabetes of the adult", ["Ketosis-prone type 2 diabetes", "Wolfram syndrome only", "Familial hypercholesterolemia"], "Medicine 1 describes LADA as phenotypic type 2 diabetes with autoimmune markers such as GAD autoantibodies.", True, page=2859),
        q("Type 2 diabetes is often associated with insulin resistance, hypertension, cardiovascular disease, dyslipidemia and", "Polycystic ovarian syndrome", ["Diabetes insipidus", "Hypoparathyroidism only", "Scleroderma renal crisis"], "Chapter 396 lists PCOS among associated conditions in type 2 diabetes.", page=2859),
        q("Hypoglycemia is most commonly caused by drugs used to treat diabetes mellitus or exposure to other drugs including", "Alcohol", ["Iodine contrast only", "Calcium carbonate", "Vitamin D"], "Chapter 399 states that hypoglycemia is most commonly caused by diabetes drugs or other drugs including alcohol.", page=2883),
        q("A diabetic patient on insulin is found confused and sweaty after alcohol intake. Which diagnosis is most directly suggested by the chapter's common causes?", "Drug-associated hypoglycemia", ["Primary hyperparathyroidism", "Adrenal incidentaloma", "Osteoporosis"], "Medicine 1 identifies diabetes treatment drugs and alcohol exposure as common causes of hypoglycemia.", True, page=2883),
        q("Central adiposity is a key feature driving recognition of", "Metabolic syndrome", ["Septo-optic dysplasia", "Alport syndrome", "Thyroiditis factitia"], "Chapter 401 states that central adiposity is a key feature of metabolic syndrome.", True, page=2903),
    ]),
    ("Bone, Mineral and Intermediary Metabolism", [
        q("Bone resorption is carried out mainly by multinucleated cells called", "Osteoclasts", ["Osteocytes only", "Thyrocytes", "Gonadotropes"], "Chapter 402 describes osteoclasts as multinucleated cells responsible for bone resorption.", page=2910),
        q("PTH and 1,25-dihydroxyvitamin D act on osteoblast receptors to help assure", "Mineral homeostasis", ["Erythropoiesis", "Gastric emptying", "AVP release"], "Medicine 1 notes that PTH and active vitamin D act on osteoblasts to assure mineral homeostasis and influence bone cells.", page=2910),
        q("Vitamin D deficiency treatment should usually be combined with supplementation of", "Calcium", ["Warfarin", "Iodide", "Insulin"], "Chapter 403 states vitamin D should be repleted with calcium supplementation because consequences relate to impaired mineral ion homeostasis.", page=2921),
        q("A patient with CKD cannot 1-hydroxylate vitamin D adequately. Which metabolite is appropriate because it does not require that activation step?", "Calcitriol", ["Cholecalciferol only", "Ergocalciferol only", "Tolvaptan"], "Medicine 1 recommends calcitriol or doxercalciferol when 1-hydroxylation is impaired.", True, page=2921),
        q("Primary hyperparathyroidism manifestations involve primarily the kidneys and", "Skeletal system", ["Larynx", "Retina", "Bronchi"], "Chapter 403 states that HPT manifestations primarily involve kidneys and skeleton.", page=2927),
        q("A patient with hyperparathyroidism has recurrent stones. Before 1970, kidney involvement in HPT was commonly due to calcium deposition or", "Recurrent nephrolithiasis", ["Uric acid overproduction", "Glomerular crescents only", "Papillary necrosis only"], "Medicine 1 explains renal involvement in HPT as nephrocalcinosis or recurrent nephrolithiasis.", True, page=2927),
        q("FRAX estimates 10-year risk for major osteoporosis-related fractures and", "Hip fracture", ["Pancreatitis", "Thyrotoxicosis", "Diabetic ketoacidosis"], "Chapter 404 describes FRAX as calculating 10-year major osteoporotic and hip fracture risk.", page=2948),
        q("Chronic glucocorticoid therapy can increase fracture risk within", "3 months", ["10 years only", "1 day", "30 years"], "Medicine 1 states fractures increase within 3 months of steroid treatment.", page=2959),
        q("A patient on chronic glucocorticoids develops early trabecular bone loss and vertebral fracture risk. This is", "Glucocorticoid-induced osteoporosis", ["Wilson disease", "Pheochromocytoma", "LADA"], "Chapter 405 emphasizes osteoporosis and fractures as serious side effects of chronic glucocorticoid therapy.", True, page=2959),
        q("A child becomes symptomatic only after fructose or sucrose ingestion, with vomiting, jaundice and hypoglycemia. The likely disorder is", "Hereditary fructose intolerance", ["Essential fructosemia", "Alport syndrome", "Calcium oxalate arthritis"], "Medicine 1 describes aldolase B deficiency as hereditary fructose intolerance, triggered by fructose or sucrose and causing hepatic and renal illness.", True, page=3015),
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
                "id": f"medicine-endocrinology-metabolism-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate endocrinology/metabolism question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 50 book-based Endocrinology and Metabolism questions.")


if __name__ == "__main__":
    main()
