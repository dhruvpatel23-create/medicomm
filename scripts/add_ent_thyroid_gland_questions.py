import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ent"
SUBJECT_TITLE = "ENT"
CHAPTER = "Thyroid Gland and Its Disorders"
CHAPTER_ORDER = 6
SOURCE_PDF = "ent 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def punctuate(prompt):
    prompt = prompt.strip()
    if prompt[-1] in ".?!:":
        return prompt
    replacements = [
        (". The most likely diagnosis is", ". What is the most likely diagnosis?"),
        (". The likely diagnosis is", ". What is the likely diagnosis?"),
        (". The next step is", ". What is the next step?"),
        (". The best treatment is", ". What is the best treatment?"),
        (". This suggests", ". What does this suggest?"),
        (". This points toward", ". What does this point toward?"),
    ]
    for old, new in replacements:
        if prompt.endswith(old):
            return f"{prompt[:-len(old)]}{new}"
    if prompt.lower().endswith(("what does this suggest", "what is the most likely diagnosis", "what is the next step", "what is the best treatment")):
        return f"{prompt}?"
    if prompt.startswith(("Which ", "What ", "Why ", "How ", "When ", "Where ")):
        return f"{prompt}?"
    return f"{prompt}:"


def q(prompt, answer, wrong, explanation, clinical=False, difficulty=None):
    options = [answer, *wrong]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {
        "prompt": punctuate(prompt),
        "options": options,
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty or ("high" if clinical else "moderate"),
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("Thyroid Anatomy, Embryology and Physiology", [
        q("The thyroid gland develops from endoderm at the", "Foramen cecum", ["Pyriform fossa", "Second branchial cleft", "Rathke pouch"], "The thyroglossal duct descends from the foramen cecum to the neck."),
        q("The thyroid isthmus usually lies over tracheal rings", "Second to fourth", ["First only", "Sixth to eighth", "Below the sternal angle"], "The isthmus crosses the upper trachea, commonly rings 2 to 4."),
        q("A midline neck cyst moves with tongue protrusion. What is the most likely diagnosis", "Thyroglossal duct cyst", ["Branchial cyst", "Dermoid of parotid", "Laryngocele"], "Attachment to the tract near the foramen cecum makes it move with tongue protrusion.", True),
        q("The superior thyroid artery is a branch of the", "External carotid artery", ["Internal carotid artery", "Subclavian artery", "Brachiocephalic vein"], "It arises from the external carotid and supplies the upper pole."),
        q("The recurrent laryngeal nerve is closely related to the", "Inferior thyroid artery", ["Facial artery", "Lingual artery", "Anterior jugular vein"], "This relationship is crucial during thyroidectomy."),
        q("After thyroidectomy, a patient has breathy hoarseness and aspiration of liquids. What does this suggest", "Recurrent laryngeal nerve injury", ["Hypoglossal nerve injury", "External carotid injury", "Glossopharyngeal neuralgia"], "RLN palsy causes glottic insufficiency, hoarseness and aspiration.", True),
        q("The external branch of superior laryngeal nerve supplies the", "Cricothyroid muscle", ["Posterior cricoarytenoid", "Palatoglossus", "Sternothyroid"], "Cricothyroid tenses the vocal fold and helps produce high pitch."),
        q("Thyroid hormone synthesis requires iodide uptake and", "Organification by thyroid peroxidase", ["Calcitonin binding", "Parathyroid hormone release", "Reverse T3 secretion"], "TPO oxidizes iodide and couples iodotyrosines."),
        q("A singer loses ability to reach high notes after upper-pole ligation during thyroidectomy. The nerve injured is", "External superior laryngeal nerve", ["Recurrent laryngeal nerve", "Hypoglossal nerve", "Marginal mandibular nerve"], "External SLN injury weakens cricothyroid and affects pitch.", True),
        q("Thyroid follicular cells secrete", "T3 and T4", ["Calcitonin", "Parathyroid hormone", "Cortisol"], "Follicular cells synthesize thyroid hormones; C cells secrete calcitonin.", True),
    ]),
    ("Clinical Evaluation, Thyroid Function Tests and Imaging", [
        q("The most sensitive screening test for primary thyroid dysfunction is", "Serum TSH", ["Serum calcium alone", "Neck X-ray", "Urine iodine only"], "TSH changes early in primary hypo- or hyperthyroidism."),
        q("High TSH with low free T4 indicates", "Primary hypothyroidism", ["Central hypothyroidism", "Subclinical hyperthyroidism", "Medullary carcinoma"], "A failing thyroid causes low T4 and compensatory TSH rise."),
        q("A woman has fatigue, weight gain, constipation, high TSH and low free T4. What is the diagnosis", "Primary hypothyroidism", ["Graves disease", "Toxic adenoma", "Thyroid storm"], "Symptoms and labs fit overt primary hypothyroidism.", True),
        q("Low TSH with high free T4 indicates", "Thyrotoxicosis", ["Primary hypothyroidism", "Euthyroid sick syndrome only", "Hypoparathyroidism"], "Suppressed TSH with raised hormone confirms biochemical thyrotoxicosis."),
        q("Thyroid ultrasound is especially useful to assess nodule composition and", "Cervical lymph nodes", ["Vocal pitch", "Serum TSH", "Airway resistance only"], "Ultrasound characterizes nodules and nodal disease."),
        q("A solitary thyroid nodule has microcalcifications, irregular margins and taller-than-wide shape on ultrasound. What does this suggest", "High malignancy risk", ["Simple colloid cyst", "Subacute thyroiditis", "Diffuse Graves goiter"], "These sonographic features are suspicious for thyroid cancer.", True),
        q("Radionuclide thyroid scan is most useful when TSH is", "Suppressed", ["Markedly high", "Normal in every nodule", "Not measured"], "A low TSH suggests autonomous function, where scintigraphy can classify hot nodules."),
        q("A thyroid nodule with suppressed TSH is hot on scan. The risk of malignancy is generally", "Low", ["Very high in every case", "Same as cold nodule", "Diagnostic of medullary cancer"], "Hyperfunctioning nodules are rarely malignant."),
        q("A patient has a thyroid nodule and low TSH. What is the next useful investigation", "Radionuclide thyroid scan", ["Immediate total thyroidectomy for all", "Serum amylase", "Audiogram"], "Scintigraphy helps identify autonomous hot nodules.", True),
        q("Fine needle aspiration cytology is used to evaluate", "Suspicious or appropriately sized thyroid nodules", ["All normal thyroid glands", "Every case of viral sore throat", "Only hyperthyroid symptoms"], "FNAC is central to risk stratification of thyroid nodules.", True),
    ]),
    ("Goiter, Iodine Deficiency and Benign Thyroid Enlargement", [
        q("Diffuse endemic goiter is most commonly related to", "Iodine deficiency", ["Excess calcitonin", "EBV infection", "Mumps"], "Low iodine reduces hormone synthesis and increases TSH drive."),
        q("A multinodular goiter usually represents", "Repeated cycles of hyperplasia and involution", ["Acute bacterial abscess", "Single embryonic cyst", "Pure medullary cancer"], "Long-standing stimulation causes nodularity and fibrosis."),
        q("A woman from an iodine-deficient region has diffuse painless thyroid enlargement and normal hormones. What is likely", "Simple goiter", ["Thyroid storm", "Subacute thyroiditis", "Anaplastic cancer"], "Euthyroid diffuse enlargement in endemic area suggests simple goiter.", True),
        q("Retrosternal goiter may produce", "Tracheal compression", ["Sensorineural hearing loss", "Posterior epistaxis", "Ranula"], "Large descending goiters can compress the airway or great veins."),
        q("Pemberton sign indicates thoracic inlet obstruction when arm elevation causes", "Facial congestion or distress", ["Tongue deviation", "Vertigo", "Watery rhinorrhea"], "Raising arms worsens venous/airway compression by a retrosternal goiter."),
        q("A patient with large goiter develops dyspnea when lying flat and positive Pemberton sign. What does this suggest", "Retrosternal goiter with compressive symptoms", ["Mild allergic rhinitis", "Vocal nodule", "Mumps"], "Orthopnea and Pemberton sign indicate significant thoracic inlet compression.", True),
        q("A dominant nodule in multinodular goiter should be evaluated because it may harbor", "Malignancy", ["Adenoid tissue", "Ear cholesteatoma", "Salivary stone"], "New, hard or dominant nodules require malignancy exclusion."),
        q("Surgery for benign goiter is considered for compression, cosmesis, suspicion of cancer or", "Toxic multinodular goiter", ["Small stable asymptomatic gland", "Normal ultrasound only", "Mild transient URI"], "Symptoms, malignancy concern and hyperfunction are common indications."),
        q("A long-standing multinodular goiter becomes toxic in an elderly patient with weight loss and palpitations. What is the diagnosis", "Toxic multinodular goiter", ["Hashimoto hypothyroidism", "De Quervain thyroiditis", "Thyroglossal cyst"], "Autonomous nodules can produce thyrotoxicosis after years.", True),
        q("Iodine supplementation prevents endemic goiter mainly by restoring", "Thyroid hormone synthesis", ["Parathyroid growth", "Calcitonin secretion", "Recurrent laryngeal function"], "Adequate iodine permits normal T3/T4 synthesis and reduces TSH stimulation.", True),
    ]),
    ("Hyperthyroidism, Graves Disease and Thyroid Storm", [
        q("The commonest cause of hyperthyroidism in many settings is", "Graves disease", ["Hashimoto thyroiditis", "Anaplastic carcinoma", "Riedel thyroiditis"], "Graves is an autoimmune TSH receptor-stimulating disease."),
        q("Graves disease is caused by antibodies that stimulate the", "TSH receptor", ["Calcitonin receptor", "Insulin receptor", "Parathyroid receptor"], "TSI activates the TSH receptor and increases hormone production."),
        q("A young woman has weight loss, tremor, diffuse goiter and exophthalmos. What is the most likely diagnosis", "Graves disease", ["Subacute thyroiditis", "Papillary carcinoma", "Simple colloid goiter"], "Diffuse toxic goiter with eye signs is classic Graves disease.", True),
        q("Pretibial myxedema is associated with", "Graves disease", ["Medullary carcinoma", "Iodine deficiency alone", "Thyroglossal cyst"], "It is an autoimmune dermopathy seen in Graves disease."),
        q("Antithyroid drugs reduce hormone synthesis by inhibiting", "Thyroid peroxidase", ["Thyroglobulin storage only", "Calcitonin release", "TSH secretion from pituitary directly"], "Methimazole and PTU inhibit organification and coupling."),
        q("A patient on antithyroid medication develops fever and sore throat. What is the urgent concern", "Agranulocytosis", ["Mumps", "Otosclerosis", "Benign aphthae"], "Fever/sore throat on antithyroid drugs requires urgent neutrophil count.", True),
        q("Propranolol helps thyrotoxicosis by controlling adrenergic symptoms and reducing", "Peripheral T4 to T3 conversion at high doses", ["TSH receptor antibodies", "Thyroid cancer spread", "Parathyroid hormone"], "Beta blockade reduces tremor, tachycardia and partly T3 generation."),
        q("Radioiodine is contraindicated in", "Pregnancy", ["Older age alone", "Small toxic nodule always", "Past tonsillitis"], "Radioiodine can damage the fetal thyroid."),
        q("A febrile thyrotoxic patient has delirium, tachyarrhythmia and heart failure after surgery. What is the diagnosis", "Thyroid storm", ["Myxedema coma", "Viral pharyngitis", "Hypocalcemia"], "Severe decompensated thyrotoxicosis with systemic toxicity is thyroid storm.", True),
        q("Initial treatment of thyroid storm includes beta blocker, antithyroid drug, iodine after thionamide and", "Glucocorticoids with supportive care", ["Immediate radioiodine", "Observation only", "Calcium infusion only"], "Storm treatment blocks synthesis, release, conversion and adrenergic effects.", True),
    ]),
    ("Hypothyroidism and Thyroiditis", [
        q("The commonest cause of hypothyroidism in iodine-sufficient areas is", "Hashimoto thyroiditis", ["Graves disease", "Toxic adenoma", "Medullary carcinoma"], "Autoimmune thyroid destruction is a leading cause."),
        q("Hashimoto thyroiditis is associated with antibodies against thyroid peroxidase and", "Thyroglobulin", ["TSH only", "Calcitonin only", "Insulin only"], "Anti-TPO and anti-thyroglobulin antibodies are common."),
        q("A woman has painless firm goiter, hypothyroidism and high anti-TPO antibodies. What is the diagnosis", "Hashimoto thyroiditis", ["Graves disease", "Subacute thyroiditis", "Riedel thyroiditis"], "Autoimmune hypothyroidism with firm goiter fits Hashimoto disease.", True),
        q("Subacute granulomatous thyroiditis usually follows viral illness and causes", "Painful tender thyroid", ["Painless hard fixed mass", "Watery rhinorrhea", "Parotid stone"], "De Quervain thyroiditis is painful and often post-viral."),
        q("ESR in subacute thyroiditis is typically", "Raised", ["Always zero", "Diagnostic of medullary cancer", "Unrelated to inflammation"], "Markedly raised ESR supports subacute thyroiditis."),
        q("A patient has fever, anterior neck pain radiating to jaw and transient thyrotoxicosis after URI. What is likely", "Subacute thyroiditis", ["Toxic multinodular goiter", "Papillary carcinoma", "Simple goiter"], "Painful post-viral thyroiditis causes release thyrotoxicosis.", True),
        q("Postpartum thyroiditis is usually", "Autoimmune and often transient", ["Bacterial abscess", "Always malignant", "Caused by iodine excess only"], "It may cause hyperthyroid and hypothyroid phases after delivery."),
        q("Riedel thyroiditis is characterized by", "Dense fibrosing thyroid disease", ["Soft cystic thyroid", "Pure Graves ophthalmopathy", "Acute suppuration only"], "Fibrosis can mimic invasive cancer and compress structures."),
        q("A patient has a rock-hard thyroid fixed to surrounding structures with compressive symptoms but inflammatory fibrosis on biopsy. What is likely", "Riedel thyroiditis", ["Simple colloid cyst", "Mumps", "Vocal nodule"], "Riedel disease produces invasive-like fibrosis.", True),
        q("Myxedema coma is treated urgently with thyroid hormone, supportive care and", "Glucocorticoids until adrenal insufficiency is excluded", ["Radioiodine", "Antithyroid drugs", "Silver nitrate"], "Stress-dose steroids are given before or with thyroid hormone in severe hypothyroidism.", True),
    ]),
    ("Thyroid Nodules, FNAC and Risk Stratification", [
        q("Most thyroid nodules are", "Benign", ["Malignant", "Medullary", "Anaplastic"], "The majority of thyroid nodules are non-malignant."),
        q("A cold nodule on radionuclide scan means", "Reduced tracer uptake compared with surrounding thyroid", ["Guaranteed cancer", "Guaranteed infection", "Excess tracer uptake"], "Cold nodules are nonfunctioning but not automatically malignant."),
        q("A 30-year-old has a solitary hard thyroid nodule and cervical lymphadenopathy. What is the next step", "Ultrasound-guided FNAC of suspicious lesion", ["Ignore because age is young", "Start radioiodine without diagnosis", "Tonsillectomy"], "Suspicious nodule and nodes require cytologic diagnosis.", True),
        q("Bethesda reporting is used for", "Thyroid cytology", ["Audiometry", "Sleep study", "Epistaxis grading"], "The Bethesda system classifies thyroid FNAC results."),
        q("Bethesda II usually means", "Benign cytology", ["Malignant cytology", "Nondiagnostic only", "Medullary carcinoma always"], "Bethesda II is benign, with follow-up based on clinical and ultrasound risk."),
        q("A thyroid FNAC report says Bethesda VI. What does this mean", "Malignant cytology", ["Benign colloid nodule", "Nondiagnostic aspirate", "Atypia only"], "Bethesda VI indicates malignancy and usually needs surgery.", True),
        q("Suspicious ultrasound features include microcalcifications, irregular margins and", "Taller-than-wide shape", ["Purely spongiform pattern", "Comet-tail artifact only", "Thin regular cyst wall"], "These features increase malignancy risk."),
        q("A cystic thyroid nodule with comet-tail artifacts is most suggestive of", "Benign colloid nodule", ["Anaplastic carcinoma", "Medullary carcinoma", "Lymphoma"], "Comet-tail artifact in a cystic colloid nodule is reassuring."),
        q("A patient has a 1.5 cm hypoechoic taller-than-wide nodule with microcalcifications. What does this suggest", "High-suspicion thyroid nodule", ["Simple goiter only", "Subacute thyroiditis", "Toxic hot nodule"], "The combination of suspicious ultrasound signs warrants FNAC.", True),
        q("Rapid enlargement of a thyroid nodule with hoarseness is concerning for", "Invasive malignancy", ["Benign stable colloid cyst", "Mild hypothyroidism only", "Simple allergy"], "Rapid growth and vocal cord symptoms are red flags.", True),
    ]),
    ("Differentiated Thyroid Cancer: Papillary and Follicular", [
        q("The commonest thyroid malignancy is", "Papillary thyroid carcinoma", ["Follicular carcinoma", "Medullary carcinoma", "Anaplastic carcinoma"], "Papillary carcinoma is the most frequent thyroid cancer."),
        q("Papillary thyroid carcinoma commonly spreads by", "Lymphatics to cervical nodes", ["Only hematogenous liver spread", "Perineural spread only", "No spread"], "Cervical nodal metastasis is common."),
        q("A young woman has thyroid nodule with cervical nodes; FNAC shows nuclear grooves and inclusions. What is likely", "Papillary thyroid carcinoma", ["Follicular adenoma", "Medullary carcinoma", "Riedel thyroiditis"], "Papillary carcinoma has characteristic nuclear features and nodal spread.", True),
        q("Orphan Annie eye nuclei are associated with", "Papillary thyroid carcinoma", ["Subacute thyroiditis", "Graves disease", "Anaplastic carcinoma"], "Optically clear nuclei are a classic papillary carcinoma feature."),
        q("Follicular carcinoma is diagnosed histologically by capsular or", "Vascular invasion", ["Amyloid stroma alone", "Orphan Annie nuclei only", "Psammoma body only"], "Cytology cannot reliably distinguish adenoma from carcinoma without invasion."),
        q("A follicular-pattern thyroid lesion on FNAC cannot be called carcinoma until surgery shows", "Capsular or vascular invasion", ["High TSH only", "Painful tenderness", "Raised ESR"], "Follicular carcinoma requires proof of invasion.", True),
        q("Follicular thyroid carcinoma tends to spread", "Hematogenously to bone and lung", ["Only to tonsils", "Only by salivary ducts", "Never outside thyroid"], "Vascular invasion permits distant spread."),
        q("Total thyroidectomy is favored in selected differentiated thyroid cancers to allow radioactive iodine therapy and", "Thyroglobulin surveillance", ["Calcitonin surveillance", "TSH receptor blocking only", "Avoid all follow-up"], "After total thyroidectomy, thyroglobulin helps detect recurrence."),
        q("After total thyroidectomy for papillary cancer, rising thyroglobulin suggests", "Residual or recurrent differentiated thyroid tissue/cancer", ["Cured disease always", "Medullary carcinoma marker", "Hypocalcemia only"], "Thyroglobulin should be low after ablation of thyroid tissue.", True),
        q("Radioactive iodine is useful in differentiated thyroid cancer because tumor cells may", "Concentrate iodine", ["Secrete insulin", "Produce PTH", "Block TSH"], "Papillary and follicular cancers often retain iodine uptake.", True),
    ]),
    ("Medullary, Anaplastic and Thyroid Lymphoma", [
        q("Medullary thyroid carcinoma arises from", "Parafollicular C cells", ["Follicular cells", "Parathyroid chief cells", "Thymic epithelial cells"], "C cells secrete calcitonin."),
        q("The tumor marker for medullary thyroid carcinoma is", "Calcitonin", ["Thyroglobulin", "AFP", "PSA"], "Calcitonin is used for diagnosis and follow-up."),
        q("A thyroid tumor has amyloid stroma and high calcitonin. What is the diagnosis", "Medullary thyroid carcinoma", ["Papillary carcinoma", "Follicular adenoma", "Riedel thyroiditis"], "Medullary carcinoma produces calcitonin and amyloid deposits.", True),
        q("Medullary thyroid carcinoma may be part of", "MEN 2 syndrome", ["MEN 1 only", "Turner syndrome only", "CHARGE association"], "MEN2 is associated with RET mutations and medullary carcinoma."),
        q("Before surgery in MEN2-related medullary carcinoma, it is essential to exclude", "Pheochromocytoma", ["Otitis media", "Nasal polyp", "Aphthous ulcer"], "Undiagnosed pheochromocytoma can cause perioperative crisis."),
        q("A patient with MEN2 has thyroid nodule and episodic hypertension. What must be addressed before thyroidectomy", "Pheochromocytoma", ["Simple goiter", "Mumps", "Sialolithiasis"], "Pheochromocytoma is treated first to prevent catecholamine crisis.", True),
        q("Anaplastic thyroid carcinoma typically presents as", "Rapidly enlarging hard neck mass with compressive symptoms", ["Slow painless childhood cyst", "Meal-time swelling", "Transient viral pain"], "It is aggressive and often presents with invasion."),
        q("A 75-year-old has rapidly enlarging thyroid mass, stridor and vocal cord palsy. What is most concerning", "Anaplastic thyroid carcinoma", ["Simple colloid goiter", "Hashimoto thyroiditis only", "Toxic adenoma"], "Rapid growth with airway and nerve invasion suggests anaplastic cancer.", True),
        q("Primary thyroid lymphoma is associated with", "Hashimoto thyroiditis", ["Graves ophthalmopathy only", "Iodine excess only", "Mumps"], "Chronic autoimmune thyroiditis increases lymphoma risk."),
        q("Rapid thyroid enlargement in a patient with Hashimoto thyroiditis should raise suspicion for", "Thyroid lymphoma", ["Simple aphthous ulcer", "Warthin tumor", "Choanal atresia"], "New rapid enlargement in Hashimoto disease needs lymphoma exclusion.", True),
    ]),
    ("Thyroid Surgery, Complications and Postoperative Care", [
        q("The most feared immediate airway complication after thyroidectomy is", "Neck hematoma", ["Aphthous ulcer", "Mumps", "Otitis externa"], "A tense hematoma can rapidly compress the airway."),
        q("A patient develops respiratory distress and tense neck swelling soon after thyroidectomy. What is the next step", "Open the wound urgently and secure airway", ["Wait for morning rounds", "Give oral antihistamine only", "Do audiogram"], "Post-thyroidectomy hematoma is an airway emergency.", True),
        q("Hypocalcemia after thyroidectomy is usually due to", "Parathyroid devascularization or removal", ["Facial nerve injury", "Stapes fixation", "Nasal cycle"], "Parathyroid injury lowers PTH and calcium."),
        q("Perioral tingling and carpopedal spasm after thyroidectomy suggest", "Hypocalcemia", ["Hyperthyroidism", "Medullary spread", "Vocal nodule"], "Neuromuscular irritability after surgery suggests low calcium."),
        q("A patient has Chvostek sign one day after total thyroidectomy. What should be checked", "Serum calcium and PTH", ["Serum amylase only", "Audiogram", "Nasal endoscopy"], "Early hypocalcemia requires biochemical confirmation and treatment.", True),
        q("Bilateral recurrent laryngeal nerve injury causes", "Airway obstruction from bilateral vocal cord immobility", ["Only high-pitch voice loss", "Meal-time salivary pain", "Posterior epistaxis"], "Bilateral cords may lie near midline, causing stridor."),
        q("External superior laryngeal nerve injury causes difficulty with", "High-pitched voice", ["Tongue protrusion", "Nasal breathing only", "Salivary flow"], "Cricothyroid weakness impairs pitch elevation."),
        q("Thyroid storm after thyroid surgery is prevented by", "Rendering toxic patients euthyroid before operation", ["Avoiding all calcium checks", "Removing adenoids", "No beta blocker ever"], "Elective surgery in thyrotoxicosis requires preparation."),
        q("A Graves patient undergoes emergency surgery without control and develops fever, delirium and tachycardia. What is this", "Thyroid storm", ["Myxedema coma", "Hypocalcemia only", "Laryngeal web"], "Uncontrolled thyrotoxicosis can decompensate perioperatively.", True),
        q("The strap muscles are separated in midline during thyroidectomy mainly to expose", "Thyroid gland safely through an avascular plane", ["Middle ear", "Pyriform sinus", "Parotid duct"], "Midline approach minimizes bleeding and provides access to the gland.", True),
    ]),
    ("Special Thyroid Conditions and Neck Mass Differentials", [
        q("Thyroglossal duct cyst is commonly located", "In the midline near the hyoid", ["Posterior triangle", "Parotid tail", "Supraclavicular fossa only"], "The tract passes near or through the hyoid region."),
        q("Definitive treatment of thyroglossal duct cyst is", "Sistrunk operation", ["Simple incision drainage only", "Superficial parotidectomy", "Radioiodine alone"], "Sistrunk removes cyst, tract and central hyoid to reduce recurrence."),
        q("A child has recurrent infected midline neck swelling moving with tongue protrusion. What is the best treatment after infection settles", "Sistrunk operation", ["Simple aspiration only", "Total thyroidectomy", "Tonsillectomy"], "Definitive surgery is delayed until acute infection settles.", True),
        q("Lingual thyroid occurs when thyroid tissue fails to", "Descend from foramen cecum", ["Form vocal cords", "Open Wharton duct", "Drain maxillary sinus"], "Failure of descent leaves ectopic thyroid at the tongue base."),
        q("Before removing a suspected lingual thyroid, it is important to confirm", "Presence of normally located thyroid tissue", ["Normal hearing", "Nasal patency only", "Tonsil size"], "Lingual thyroid may be the only functioning thyroid tissue."),
        q("A girl has dysphagia and a tongue-base mass; scan shows no thyroid in the neck. What is likely", "Lingual thyroid", ["Ranula", "Adenoid hypertrophy", "Peritonsillar abscess"], "Ectopic thyroid at tongue base can be the only thyroid tissue.", True),
        q("A branchial cyst is usually located along the", "Anterior border of sternocleidomastoid", ["Midline over hyoid only", "Parotid duct opening", "Thyroid isthmus"], "Second branchial cleft cysts commonly present in the lateral neck."),
        q("A lateral neck cyst in a young adult can mimic benign disease, but in older adults cystic neck mass requires exclusion of", "Metastatic squamous carcinoma", ["Simple mumps only", "Otosclerosis", "Aphthous ulcer"], "Cystic nodal metastases can resemble branchial cysts."),
        q("An adult has a new cystic lateral neck mass and tonsillar asymmetry. What is the priority", "Evaluate for metastatic head-neck malignancy", ["Assume congenital cyst only", "Drain repeatedly without biopsy", "Ignore if painless"], "Adult cystic neck masses need malignancy workup.", True),
        q("Ectopic thyroid tissue can enlarge under TSH stimulation and present as", "Midline or tongue-base mass", ["External auditory canal mass", "Posterior epistaxis", "Parotid stone"], "Ectopic thyroid behaves like thyroid tissue and may enlarge when stimulated.", True),
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
                "id": f"ent-thyroid-{topic_slug}-{question_order:02d}",
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
    if len(questions) != 100:
        raise AssertionError(f"Expected 100 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 100:
        raise AssertionError("Duplicate ENT thyroid question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ENT thyroid questions.")


if __name__ == "__main__":
    main()
