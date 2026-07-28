import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Endocrine System"
BASE = {"subjectId": "pathology", "subjectTitle": "Pathology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(difficulty, prompt, answer, distractors, explanation):
    if difficulty not in {"easy", "moderate", "high"}:
        raise ValueError(difficulty)
    options = [answer, *distractors]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {"difficulty": difficulty, "prompt": prompt, "options": options, "answerIndex": 0, "answer": answer, "explanation": explanation}


def jumble(question, desired_index):
    answer = question["answer"]
    distractors = [option for option in question["options"] if option != answer]
    options = distractors[:]
    options.insert(desired_index, answer)
    question["options"] = options
    question["answerIndex"] = desired_index
    return question


TOPICS = [
    ("pituitary-adenomas", "Pituitary Adenomas and Hyperpituitarism", [
        q("easy", "The most common pituitary adenoma secretes:", "Prolactin", ["Calcitonin", "Aldosterone", "Parathyroid hormone"], "Prolactinomas are the most common functioning pituitary adenomas."),
        q("easy", "Growth hormone excess in adults causes:", "Acromegaly", ["Cretinism", "Addison disease", "Myxedema"], "After epiphyseal closure, GH excess causes acromegaly."),
        q("easy", "ACTH-producing pituitary adenoma causes:", "Cushing disease", ["Graves disease", "Conn syndrome", "Diabetes insipidus"], "Pituitary ACTH excess is Cushing disease."),
        q("moderate", "Prolactinoma may cause:", "Galactorrhea and amenorrhea", ["Tetany", "Hematuria", "Exophthalmos only"], "Prolactin excess suppresses gonadotropin secretion."),
        q("moderate", "Somatotroph adenomas are associated with elevated:", "IGF-1", ["Calcitonin", "Renin", "Catecholamines"], "GH acts largely through hepatic IGF-1 production."),
        q("moderate", "Pituitary macroadenomas commonly cause visual symptoms by compressing the:", "Optic chiasm", ["Facial nerve", "Cerebellum", "Retina only"], "Suprasellar extension can compress the optic chiasm."),
        q("moderate", "Pituitary adenomas are usually:", "Benign monoclonal tumors", ["Metastatic carcinomas", "Granulomatous infections", "Vascular malformations only"], "Most pituitary adenomas are benign epithelial neoplasms."),
        q("high", "A woman has amenorrhea, infertility, and milky nipple discharge. MRI shows a pituitary adenoma, and serum testing reveals marked prolactin elevation. Which tumor is most likely?", "Prolactinoma", ["Somatotroph adenoma", "Corticotroph adenoma", "Craniopharyngioma"], "Prolactinoma causes hyperprolactinemia with galactorrhea and amenorrhea."),
        q("high", "An adult develops enlarged hands, coarse facial features, diabetes, hypertension, and elevated serum IGF-1 due to a pituitary mass. Which clinical syndrome is present?", "Acromegaly", ["Gigantism", "Cushing syndrome", "Sheehan syndrome"], "GH excess after epiphyseal closure causes acromegaly."),
        q("high", "A patient has central obesity, purple striae, proximal muscle weakness, hyperglycemia, and high ACTH from a basophilic pituitary adenoma. Which endocrine disorder is this?", "Cushing disease", ["Addison disease", "Graves disease", "Primary hyperaldosteronism"], "Cushing disease is ACTH-dependent hypercortisolism caused by pituitary adenoma."),
    ]),
    ("pituitary-hypofunction", "Hypopituitarism, Diabetes Insipidus, and Sellar Lesions", [
        q("easy", "Posterior pituitary ADH deficiency causes:", "Central diabetes insipidus", ["SIADH", "Graves disease", "Hyperparathyroidism"], "Loss of ADH causes inability to concentrate urine."),
        q("easy", "Sheehan syndrome follows postpartum:", "Pituitary ischemic necrosis", ["Thyroid carcinoma", "Parathyroid adenoma", "Adrenal hemorrhage only"], "Postpartum hemorrhage can infarct the enlarged pituitary."),
        q("easy", "Craniopharyngioma often contains:", "Calcification", ["Amyloid only", "Keratin pearls always", "Auer rods"], "Craniopharyngioma is often cystic and calcified."),
        q("moderate", "Central diabetes insipidus causes:", "Polyuria with dilute urine", ["Oliguria with casts", "Hematuria", "Steatorrhea"], "ADH deficiency causes water diuresis."),
        q("moderate", "Craniopharyngioma arises from remnants of:", "Rathke pouch", ["Thyroglossal duct", "Urachus", "Vitelline duct"], "It derives from embryonic Rathke pouch remnants."),
        q("moderate", "Pituitary apoplexy means sudden hemorrhage into:", "Pituitary adenoma", ["Thyroid follicle", "Adrenal cortex", "Pancreatic islet"], "Hemorrhage or infarction within adenoma can cause acute symptoms."),
        q("moderate", "Hypopituitarism usually becomes symptomatic after loss of:", "Most anterior pituitary tissue", ["One thyroid follicle", "One adrenal nodule", "One parathyroid gland only"], "Large reserve means extensive destruction is needed."),
        q("high", "A woman cannot lactate after severe postpartum hemorrhage and later develops amenorrhea, fatigue, hypothyroidism, and secondary adrenal insufficiency. Which pituitary disorder is most likely?", "Sheehan syndrome", ["Prolactinoma", "Nelson syndrome", "Graves disease"], "Ischemic necrosis of pituitary after postpartum shock causes Sheehan syndrome."),
        q("high", "A child has headaches, visual field defects, growth retardation, and a suprasellar cystic calcified mass with wet keratin. Which sellar lesion is most likely?", "Craniopharyngioma", ["Pituitary prolactinoma", "Meningioma", "Medullary thyroid carcinoma"], "Craniopharyngioma is a Rathke pouch tumor with calcification and keratin."),
        q("high", "After head trauma, a patient develops intense thirst, hypernatremia, dehydration, and large volumes of dilute urine that improve with desmopressin. Which hormone is deficient?", "Antidiuretic hormone", ["Aldosterone", "Insulin", "Parathyroid hormone"], "Central diabetes insipidus is caused by ADH deficiency."),
    ]),
    ("thyroid-hyper", "Hyperthyroidism and Graves Disease", [
        q("easy", "The most common cause of endogenous hyperthyroidism is:", "Graves disease", ["Hashimoto thyroiditis", "Medullary carcinoma", "Riedel thyroiditis"], "Graves disease is the leading endogenous cause."),
        q("easy", "Graves disease is caused by antibodies stimulating the:", "TSH receptor", ["Insulin receptor", "ACTH receptor", "PTH receptor"], "TSI antibodies activate the TSH receptor."),
        q("easy", "Hyperthyroidism typically lowers serum:", "TSH", ["T3", "T4", "Calcitonin only"], "Pituitary TSH is suppressed by high thyroid hormone."),
        q("moderate", "Graves ophthalmopathy is related to:", "Autoimmune activation of orbital fibroblasts", ["Bacterial abscess", "Parathyroid adenoma", "Pituitary infarct"], "Orbital fibroblasts produce glycosaminoglycans and inflammation."),
        q("moderate", "Diffuse scalloping of colloid in thyroid follicles suggests:", "Graves disease", ["Papillary carcinoma", "Riedel thyroiditis", "Amyloid goiter"], "Active follicles resorb colloid, producing scalloped margins."),
        q("moderate", "Toxic multinodular goiter usually lacks:", "Ophthalmopathy", ["Hyperthyroidism", "Nodular enlargement", "Low TSH"], "Ophthalmopathy is characteristic of Graves disease."),
        q("moderate", "Thyroid storm is a severe form of:", "Thyrotoxicosis", ["Hypothyroidism", "Hyperparathyroidism", "Diabetes insipidus"], "Thyroid storm is life-threatening severe thyrotoxicosis."),
        q("high", "A woman has weight loss, heat intolerance, tremor, diffuse goiter, exophthalmos, pretibial skin changes, and antibodies that stimulate the TSH receptor. Which diagnosis is most likely?", "Graves disease", ["Hashimoto thyroiditis", "Subacute thyroiditis", "Toxic adenoma only"], "Graves disease causes autoimmune hyperthyroidism with ophthalmopathy."),
        q("high", "A thyroidectomy specimen from a hyperthyroid patient shows diffuse follicular hyperplasia, tall crowded epithelium, papillary infoldings, and scalloped colloid. Which mechanism drives this morphology?", "TSH receptor-stimulating autoantibodies", ["Iodine deficiency only", "RET mutation", "Amyloid deposition"], "TSI antibodies mimic TSH and stimulate follicular cells."),
        q("high", "An elderly patient with multinodular goiter develops atrial fibrillation, weight loss, low TSH, and high thyroid hormone without eye findings. Which disorder is most likely?", "Toxic multinodular goiter", ["Graves disease", "Hashimoto thyroiditis", "Medullary carcinoma"], "Toxic multinodular goiter causes hyperthyroidism without Graves ophthalmopathy."),
    ]),
    ("thyroid-hypo-thyroiditis", "Hypothyroidism and Thyroiditis", [
        q("easy", "The most common cause of hypothyroidism in iodine-sufficient regions is:", "Hashimoto thyroiditis", ["Graves disease", "Toxic adenoma", "Papillary carcinoma"], "Autoimmune Hashimoto thyroiditis is common in iodine-sufficient areas."),
        q("easy", "Hashimoto thyroiditis is autoimmune destruction of the:", "Thyroid", ["Pituitary", "Adrenal medulla", "Parathyroid"], "Hashimoto disease destroys thyroid follicles."),
        q("easy", "Subacute granulomatous thyroiditis often follows:", "Viral infection", ["Radiation only", "Pituitary infarction", "MEN2"], "De Quervain thyroiditis often follows viral illness."),
        q("moderate", "Hashimoto thyroiditis is associated with antibodies to:", "Thyroid peroxidase", ["TSH receptor stimulating antibody only", "Calcitonin", "Insulin"], "Anti-TPO and anti-thyroglobulin antibodies are common."),
        q("moderate", "Hashimoto thyroiditis increases risk of thyroid:", "MALT lymphoma", ["Medullary carcinoma only", "Parathyroid adenoma", "Pheochromocytoma"], "Chronic lymphoid inflammation can give rise to MALT lymphoma."),
        q("moderate", "Riedel thyroiditis causes:", "Hard fibrosing thyroid mass", ["Painful viral thyroiditis only", "Diffuse toxic hyperplasia", "C-cell amyloid"], "Riedel thyroiditis is dense thyroid fibrosis."),
        q("moderate", "Subacute granulomatous thyroiditis is typically:", "Painful", ["Always painless", "A malignant tumor", "Caused by iodine excess only"], "It often causes a tender thyroid."),
        q("high", "A woman has fatigue, weight gain, cold intolerance, high TSH, and a firm thyroid. Biopsy shows lymphoid follicles with Hurthle cell change. Which disease is likely?", "Hashimoto thyroiditis", ["Graves disease", "Toxic multinodular goiter", "Medullary carcinoma"], "Hashimoto thyroiditis causes autoimmune hypothyroidism with lymphoid follicles."),
        q("high", "A patient develops painful thyroid enlargement after an upper respiratory infection. Biopsy shows disrupted follicles with granulomatous inflammation and giant cells around colloid. Which thyroiditis is present?", "Subacute granulomatous thyroiditis", ["Hashimoto thyroiditis", "Riedel thyroiditis", "Silent thyroiditis"], "De Quervain thyroiditis is painful and granulomatous."),
        q("high", "A patient has a rock-hard thyroid fixed to surrounding tissues, and biopsy shows dense fibrosis replacing thyroid and extending beyond capsule. Which condition is most likely?", "Riedel thyroiditis", ["Graves disease", "Papillary carcinoma", "Toxic adenoma"], "Riedel thyroiditis is invasive fibrosing thyroiditis."),
    ]),
    ("thyroid-tumors", "Thyroid Nodules and Thyroid Tumors", [
        q("easy", "The most common thyroid malignancy is:", "Papillary thyroid carcinoma", ["Medullary carcinoma", "Anaplastic carcinoma", "Follicular carcinoma"], "Papillary carcinoma is the most common thyroid cancer."),
        q("easy", "Medullary thyroid carcinoma arises from:", "Parafollicular C cells", ["Follicular cells", "Parathyroid chief cells", "Adrenal chromaffin cells"], "C cells produce calcitonin and give rise to medullary carcinoma."),
        q("easy", "Follicular thyroid carcinoma spreads mainly by:", "Hematogenous spread", ["Lymphatics only", "Milk ducts", "Perineural spread only"], "Follicular carcinoma tends to invade blood vessels."),
        q("moderate", "Papillary carcinoma nuclei are described as:", "Orphan Annie eye nuclei", ["Coffee-bean nuclei", "Reed-Sternberg nuclei", "Auer rod nuclei"], "Cleared overlapping nuclei are classic."),
        q("moderate", "Psammoma bodies suggest:", "Papillary thyroid carcinoma", ["Follicular adenoma", "Hashimoto thyroiditis only", "Riedel thyroiditis"], "Papillary thyroid carcinoma may contain psammoma bodies."),
        q("moderate", "Medullary carcinoma often contains stromal:", "Amyloid", ["Colloid only", "Keratin", "Mucin pools"], "Amyloid is derived from calcitonin peptides."),
        q("moderate", "Follicular carcinoma diagnosis requires invasion of:", "Capsule or vessels", ["Nuclear grooves only", "Lymphoid follicles", "Scalloped colloid"], "Invasion distinguishes follicular carcinoma from adenoma."),
        q("high", "A thyroid nodule shows branching papillae with fibrovascular cores, nuclear grooves, inclusions, overlapping clear nuclei, and psammoma bodies on microscopy. Which carcinoma is most likely?", "Papillary thyroid carcinoma", ["Follicular carcinoma", "Medullary carcinoma", "Anaplastic carcinoma"], "Papillary carcinoma is diagnosed by characteristic nuclei."),
        q("high", "A solitary thyroid tumor has uniform follicles but shows definite capsular and vascular invasion on extensive sampling of the capsule. Which diagnosis is established by invasion?", "Follicular thyroid carcinoma", ["Follicular adenoma", "Papillary carcinoma", "Hashimoto thyroiditis"], "Follicular carcinoma requires capsular or vascular invasion."),
        q("high", "A patient with MEN2 has a thyroid tumor made of polygonal neuroendocrine cells with amyloid stroma and elevated calcitonin. Which thyroid carcinoma is present?", "Medullary thyroid carcinoma", ["Papillary carcinoma", "Follicular carcinoma", "Hurthle cell adenoma"], "Medullary carcinoma arises from C cells and secretes calcitonin."),
    ]),
    ("parathyroid-calcium", "Parathyroid Disease and Calcium Disorders", [
        q("easy", "Primary hyperparathyroidism most often results from:", "Parathyroid adenoma", ["Thyroiditis", "Pituitary infarction", "Adrenal adenoma"], "A single adenoma is the common cause."),
        q("easy", "Parathyroid hormone increases serum:", "Calcium", ["Sodium only", "T3", "Cortisol"], "PTH raises calcium levels."),
        q("easy", "Hypocalcemia may cause:", "Tetany", ["Exophthalmos", "Galactorrhea", "Peau d'orange"], "Low calcium increases neuromuscular excitability."),
        q("moderate", "Secondary hyperparathyroidism is commonly caused by:", "Chronic kidney disease", ["Papillary thyroid carcinoma", "Prolactinoma", "Pheochromocytoma"], "CKD causes phosphate retention and low vitamin D."),
        q("moderate", "Osteitis fibrosa cystica is associated with:", "Hyperparathyroidism", ["Hypothyroidism", "Diabetes insipidus", "Hashimoto thyroiditis"], "PTH excess increases bone resorption and fibrosis."),
        q("moderate", "Primary hyperparathyroidism produces:", "Hypercalcemia and hypophosphatemia", ["Hypocalcemia and hyperphosphatemia", "Low PTH", "Low alkaline phosphatase only"], "PTH increases calcium and phosphate wasting."),
        q("moderate", "Parathyroid carcinoma is suggested by:", "Invasion and metastasis", ["Chief cells alone", "Low calcium", "No capsule"], "Definitive malignancy requires invasion or metastasis."),
        q("high", "A patient has kidney stones, bone pain, abdominal discomfort, and depression. Laboratory studies show high calcium, low phosphate, and elevated PTH from a single enlarged gland. Which diagnosis fits?", "Primary hyperparathyroidism from adenoma", ["Secondary hyperparathyroidism", "Hypoparathyroidism", "Medullary thyroid carcinoma"], "Parathyroid adenoma is the common cause of primary hyperparathyroidism."),
        q("high", "A patient with chronic kidney disease has hypocalcemia, hyperphosphatemia, low vitamin D activation, and diffuse parathyroid gland hyperplasia with elevated PTH. Which disorder is present?", "Secondary hyperparathyroidism", ["Primary hyperparathyroidism", "MEN2B", "Pheochromocytoma"], "CKD stimulates compensatory parathyroid hyperplasia."),
        q("high", "A patient after thyroid surgery develops perioral numbness, muscle cramps, positive Chvostek sign, and low calcium due to loss of parathyroid function. Which condition is present?", "Hypoparathyroidism", ["Primary hyperparathyroidism", "Graves disease", "Cushing syndrome"], "Postoperative parathyroid injury can cause hypocalcemic tetany."),
    ]),
    ("adrenal-cortex", "Adrenal Cortical Hyperfunction and Insufficiency", [
        q("easy", "Cushing syndrome is caused by excess:", "Cortisol", ["Aldosterone only", "Insulin", "Calcitonin"], "Glucocorticoid excess causes Cushing syndrome."),
        q("easy", "Conn syndrome is primary excess of:", "Aldosterone", ["Cortisol", "Epinephrine", "PTH"], "Primary hyperaldosteronism is Conn syndrome."),
        q("easy", "Addison disease is primary adrenal:", "Insufficiency", ["Medullary tumor", "Hyperplasia only", "C-cell carcinoma"], "Addison disease is chronic primary adrenal cortical failure."),
        q("moderate", "Primary adrenal insufficiency causes increased:", "ACTH", ["TSH only", "Insulin", "Calcitonin"], "Low cortisol removes feedback inhibition."),
        q("moderate", "Hyperaldosteronism commonly causes:", "Hypertension and hypokalemia", ["Hypotension and hyperkalemia", "Hypocalcemia", "Galactorrhea"], "Aldosterone retains sodium and wastes potassium."),
        q("moderate", "Waterhouse-Friderichsen syndrome is adrenal hemorrhage often due to:", "Meningococcemia", ["HPV infection", "Hashimoto disease", "MEN1"], "Sepsis can cause bilateral adrenal hemorrhage."),
        q("moderate", "Adrenal cortical adenomas are usually:", "Yellow because of lipid", ["Black because of melanin", "Green because of bile", "Blue because of mucin"], "Steroid-producing cortical cells contain lipid."),
        q("high", "A patient has central obesity, moon facies, purple striae, proximal weakness, hypertension, osteoporosis, and hyperglycemia from a cortisol-secreting adrenal tumor. Which syndrome is present?", "Cushing syndrome", ["Addison disease", "Conn syndrome only", "Pheochromocytoma"], "Cortisol excess causes Cushing syndrome."),
        q("high", "A patient has hypertension, muscle weakness, metabolic alkalosis, suppressed renin, and persistent hypokalemia due to an aldosterone-producing adrenal cortical adenoma. Which syndrome is present?", "Primary hyperaldosteronism", ["Secondary hyperaldosteronism", "Addison disease", "MEN1"], "Conn syndrome causes aldosterone excess with suppressed renin."),
        q("high", "A patient has fatigue, weight loss, hypotension, hyperpigmentation, salt craving, nausea, abdominal pain, hyponatremia, hyperkalemia, and autoimmune adrenal cortical destruction. Which diagnosis is most likely?", "Addison disease", ["Cushing disease", "Pheochromocytoma", "Primary hyperparathyroidism"], "Primary adrenal failure causes high ACTH and mineralocorticoid deficiency."),
    ]),
    ("adrenal-medulla-men", "Pheochromocytoma, Paraganglioma, and MEN Syndromes", [
        q("easy", "Pheochromocytoma arises from adrenal:", "Medulla", ["Cortex", "Capsule", "Zona glomerulosa only"], "Pheochromocytoma is a chromaffin cell tumor."),
        q("easy", "Pheochromocytoma secretes:", "Catecholamines", ["Insulin", "Calcitonin only", "PTH"], "Catecholamine excess causes episodic hypertension."),
        q("easy", "MEN1 classically involves parathyroid, pituitary, and:", "Pancreatic endocrine tumors", ["Medullary thyroid carcinoma", "Papillary thyroid carcinoma", "Ovarian tumors"], "MEN1 is the 3 Ps."),
        q("moderate", "Pheochromocytoma shows chromaffin cells arranged in:", "Zellballen nests", ["Papillary fronds", "Comedo ducts", "Follicles with colloid"], "Zellballen architecture is characteristic."),
        q("moderate", "MEN2 is caused by mutation in:", "RET", ["MEN1", "BRCA1", "HFE"], "RET activating mutations cause MEN2."),
        q("moderate", "MEN2A includes medullary thyroid carcinoma, pheochromocytoma, and:", "Parathyroid hyperplasia", ["Pituitary adenoma", "Gastrinoma always", "Thymoma"], "MEN2A includes parathyroid disease."),
        q("moderate", "MEN2B includes mucosal neuromas and:", "Marfanoid habitus", ["Pancreatic gastrinoma", "Pituitary prolactinoma", "Parathyroid adenoma always"], "MEN2B has mucosal neuromas and marfanoid habitus."),
        q("high", "A patient has episodic headache, sweating, palpitations, and severe hypertension. An adrenal medullary tumor shows nests of chromaffin cells with sustentacular cells. Which tumor is likely?", "Pheochromocytoma", ["Adrenocortical adenoma", "Neuroblastoma", "Medullary thyroid carcinoma"], "Pheochromocytoma secretes catecholamines and shows zellballen nests."),
        q("high", "A patient has medullary thyroid carcinoma and pheochromocytoma with a germline activating RET mutation. Primary hyperparathyroidism is also present. Which syndrome is most likely?", "MEN2A", ["MEN1", "MEN2B", "Carney complex"], "MEN2A includes MTC, pheochromocytoma, and parathyroid disease."),
        q("high", "A young patient has mucosal neuromas on the lips, marfanoid habitus, medullary thyroid carcinoma, and adrenal pheochromocytoma due to RET mutation. Which syndrome is present?", "MEN2B", ["MEN1", "MEN2A", "VHL only"], "MEN2B features mucosal neuromas, marfanoid habitus, MTC, and pheochromocytoma."),
    ]),
    ("endocrine-pancreas", "Endocrine Pancreas and Islet Cell Tumors", [
        q("easy", "Insulinoma causes:", "Hypoglycemia", ["Hypercalcemia", "Hyperthyroidism", "Hyperkalemia only"], "Insulin excess lowers glucose."),
        q("easy", "Gastrinoma causes:", "Zollinger-Ellison syndrome", ["Cushing disease", "Conn syndrome", "Graves disease"], "Gastrin excess causes acid hypersecretion and ulcers."),
        q("easy", "Glucagonoma is associated with:", "Necrolytic migratory erythema", ["Exophthalmos", "Tetany", "Galactorrhea"], "Glucagonoma causes diabetes and characteristic rash."),
        q("moderate", "VIPoma causes watery diarrhea, hypokalemia, and:", "Achlorhydria", ["Hyperchlorhydria", "Hypocalcemia", "Hypothyroidism"], "VIPoma causes WDHA syndrome."),
        q("moderate", "Pancreatic neuroendocrine tumors stain for:", "Chromogranin and synaptophysin", ["Desmin and myogenin", "GFAP only", "Thyroglobulin only"], "These markers support neuroendocrine differentiation."),
        q("moderate", "Insulinoma symptoms improve with:", "Glucose administration", ["Calcium restriction", "Thyroid hormone", "Aldosterone blockade only"], "Hypoglycemic symptoms are relieved by glucose."),
        q("moderate", "Gastrinomas may be associated with:", "MEN1", ["MEN2B only", "Hashimoto thyroiditis", "Graves disease"], "MEN1 can include pancreatic endocrine tumors."),
        q("high", "A patient has fasting confusion, sweating, low plasma glucose, elevated insulin, and relief after glucose administration. Imaging finds a small pancreatic endocrine tumor. Which tumor is most likely?", "Insulinoma", ["Gastrinoma", "Glucagonoma", "VIPoma"], "Insulinoma causes Whipple triad with inappropriate insulin secretion."),
        q("high", "A patient has recurrent peptic ulcers in unusual locations, diarrhea, and markedly increased gastric acid due to a duodenal or pancreatic endocrine tumor. Which tumor is likely?", "Gastrinoma", ["Insulinoma", "Somatostatinoma", "Medullary thyroid carcinoma"], "Gastrinoma causes Zollinger-Ellison syndrome."),
        q("high", "A patient has diabetes, anemia, weight loss, and a blistering erythematous rash migrating around the groin and lower abdomen. Which islet cell tumor is suggested?", "Glucagonoma", ["Insulinoma", "VIPoma", "Parathyroid adenoma"], "Glucagonoma causes necrolytic migratory erythema and diabetes."),
    ]),
    ("diabetes-endocrine", "Diabetes Mellitus and Endocrine Complications", [
        q("easy", "Type 1 diabetes is due to destruction of pancreatic:", "Beta cells", ["Alpha cells only", "C cells", "Chief cells"], "Autoimmune beta-cell destruction causes type 1 diabetes."),
        q("easy", "Type 2 diabetes is strongly associated with:", "Insulin resistance", ["ADH deficiency", "RET mutation", "TSH receptor antibodies"], "Insulin resistance is central to type 2 diabetes."),
        q("easy", "Diabetic ketoacidosis is most typical of:", "Type 1 diabetes", ["MEN2A", "Graves disease", "Conn syndrome"], "Absolute insulin deficiency predisposes to ketoacidosis."),
        q("moderate", "Islet amyloid in type 2 diabetes is derived from:", "Amylin", ["Insulin receptor", "Calcitonin", "Thyroglobulin"], "Amylin is co-secreted by beta cells."),
        q("moderate", "Insulitis is characteristic of:", "Type 1 diabetes", ["Type 2 diabetes only", "Pheochromocytoma", "Graves disease"], "Autoimmune lymphocytes infiltrate islets."),
        q("moderate", "Advanced glycation end products contribute to:", "Diabetic microvascular disease", ["Graves ophthalmopathy", "Pheochromocytoma", "Parathyroid adenoma"], "AGEs damage vessels and basement membranes."),
        q("moderate", "Diabetes causes nodular glomerulosclerosis called:", "Kimmelstiel-Wilson lesions", ["Orphan Annie nuclei", "Call-Exner bodies", "Zellballen nests"], "Nodular diabetic glomerulosclerosis is Kimmelstiel-Wilson disease."),
        q("high", "A child presents with polyuria, polydipsia, weight loss, ketoacidosis, and lymphocytic inflammation of pancreatic islets with beta-cell depletion. Which diabetes mechanism is most likely?", "Autoimmune beta-cell destruction", ["Insulin resistance only", "Glucagonoma secretion", "RET activation"], "Type 1 diabetes is autoimmune beta-cell loss."),
        q("high", "An obese adult with hyperglycemia develops insulin resistance, islet amyloid deposition, beta-cell dysfunction, nephropathy, neuropathy, and retinopathy over many years. Which diabetes type is favored?", "Type 2 diabetes mellitus", ["Type 1 diabetes mellitus", "Central diabetes insipidus", "MEN1"], "Type 2 diabetes features insulin resistance and islet amyloid."),
        q("high", "A long-standing diabetic patient develops nodular glomerulosclerosis, retinal microaneurysms, peripheral neuropathy, and accelerated atherosclerosis over time. Which biochemical process broadly drives these chronic vascular complications?", "Nonenzymatic glycation of proteins", ["TSH receptor stimulation", "Calcitonin amyloid deposition", "ADH deficiency"], "AGE formation contributes to chronic diabetic complications."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch24-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 24 questions, got {len(chapter_questions)}")
    topic_counts = Counter(q["topic"] for q in chapter_questions)
    if len(topic_counts) != 10 or any(count != 10 for count in topic_counts.values()):
        raise ValueError(f"Bad topic distribution: {topic_counts}")
    expected = Counter({"easy": 3, "moderate": 4, "high": 3})
    for topic in topic_counts:
        counts = Counter(q["difficulty"] for q in chapter_questions if q["topic"] == topic)
        if counts != expected:
            raise ValueError(f"Bad difficulty distribution for {topic}: {counts}")
    for question in chapter_questions:
        options = question["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Bad options: {question['id']}")
        if question["answer"] != options[question["answerIndex"]]:
            raise ValueError(f"Bad answer: {question['id']}")
    short_high = [q["id"] for q in chapter_questions if q["difficulty"] == "high" and len(q["prompt"].split()) < 24]
    if short_high:
        raise ValueError(f"High-level prompts too short: {short_high[:5]}")
    if all_questions is not None:
        ids = [q.get("id") for q in all_questions]
        duplicates = [qid for qid, count in Counter(ids).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate ids: {duplicates[:10]}")


def main():
    chapter_questions = build_questions()
    validate(chapter_questions)
    total_removed = 0
    for data_path in DATA_PATHS:
        data = json.loads(data_path.read_text(encoding="utf-8-sig"))
        existing = data.get("questions", [])
        kept = [
            question for question in existing
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch24-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 24 questions")
    print(f"Removed {total_removed} existing Chapter 24 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 24 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
