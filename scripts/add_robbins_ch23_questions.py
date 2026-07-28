import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Breast"
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
    ("normal-inflammatory", "Normal Breast, Mastitis, and Inflammatory Lesions", [
        q("easy", "The breast terminal duct lobular unit is the usual origin of:", "Most breast carcinomas", ["Skeletal muscle tumors", "Renal cysts", "Thyroid nodules"], "Most epithelial breast lesions arise from terminal duct lobular units."),
        q("easy", "Acute mastitis most often occurs during:", "Lactation", ["Menopause only", "Childhood only", "Fetal life"], "Lactational mastitis follows bacterial entry through nipple fissures."),
        q("easy", "Fat necrosis of breast may follow:", "Trauma", ["HPV infection", "Bile obstruction", "Iron overload"], "Trauma can damage adipose tissue and mimic carcinoma."),
        q("moderate", "The common organism in lactational mastitis is:", "Staphylococcus aureus", ["Schistosoma haematobium", "Giardia lamblia", "Hepatitis C virus"], "S. aureus commonly causes acute suppurative mastitis."),
        q("moderate", "Mammary duct ectasia commonly causes:", "Periareolar inflammation and nipple discharge", ["Nephrotic syndrome", "Cervical dysplasia", "Hydronephrosis"], "Duct dilation and rupture provoke inflammation near the nipple."),
        q("moderate", "Fat necrosis can show calcification and:", "Foamy macrophages", ["Schiller-Duval bodies", "Auer rods", "Koilocytes"], "Necrotic fat elicits macrophages, giant cells, and calcification."),
        q("moderate", "Granulomatous mastitis may clinically mimic:", "Breast carcinoma", ["Renal colic", "Appendicitis", "Endometriosis"], "A firm inflammatory mass can resemble cancer."),
        q("high", "A lactating woman develops a painful erythematous breast with fever, leukocytosis, and a localized abscess. Culture grows gram-positive cocci. Which diagnosis is most likely?", "Acute bacterial mastitis", ["Mammary duct ectasia", "Fat necrosis", "Fibroadenoma"], "Lactational mastitis is commonly caused by S. aureus."),
        q("high", "A woman develops a firm irregular breast mass after blunt trauma. Biopsy shows necrotic adipocytes, foamy macrophages, multinucleated giant cells, and calcification. Which lesion is present?", "Fat necrosis", ["Invasive ductal carcinoma", "Phyllodes tumor", "Papilloma"], "Fat necrosis can form a hard mass and calcifications."),
        q("high", "A middle-aged woman has periareolar pain, nipple discharge, and a subareolar mass. Histology shows dilated ducts filled with secretions and plasma cell-rich inflammation. Which condition fits?", "Mammary duct ectasia", ["Lactational adenoma", "DCIS", "Medullary carcinoma"], "Duct ectasia causes periductal chronic inflammation and discharge."),
    ]),
    ("fibrocystic", "Fibrocystic Change and Nonproliferative Breast Disease", [
        q("easy", "Fibrocystic change is a common benign disease of the:", "Breast", ["Ovary", "Kidney", "Thyroid"], "Fibrocystic change is common in breast tissue."),
        q("easy", "Breast cysts are usually:", "Benign", ["Always invasive", "Always metastatic", "Lymphomas"], "Simple cysts are nonproliferative benign lesions."),
        q("easy", "Apocrine metaplasia is commonly seen in:", "Fibrocystic change", ["Seminoma", "Wilms tumor", "Cervical CIN"], "Apocrine metaplasia is a benign cyst lining change."),
        q("moderate", "Nonproliferative fibrocystic change generally has:", "No significant increased cancer risk", ["Very high cancer risk", "Obligate carcinoma transformation", "Only sarcoma risk"], "Cysts and fibrosis alone do not substantially raise risk."),
        q("moderate", "Fibrocystic change may cause mammographic:", "Calcifications", ["Hydronephrosis", "Bone metastases", "Pneumothorax"], "Calcifications may be detected on screening."),
        q("moderate", "Blue-dome cysts contain:", "Fluid-filled cystic spaces", ["Keratin pearls", "Trophoblasts", "Cartilage only"], "Gross cysts can appear blue because of fluid."),
        q("moderate", "Stromal fibrosis in fibrocystic change can produce:", "Palpable firmness", ["Hematuria", "Jaundice", "Ascites"], "Fibrosis may create a firm nodular area."),
        q("high", "A woman has cyclic breast pain and nodularity. Biopsy shows cysts, stromal fibrosis, and apocrine metaplasia without epithelial hyperplasia or atypia. What is the cancer risk?", "Little to no increased risk", ["Very high risk", "Risk equal to BRCA mutation", "Obligate invasive cancer"], "Nonproliferative fibrocystic change has minimal risk."),
        q("high", "A screening mammogram shows calcifications, and biopsy reveals benign cysts lined by apocrine cells with surrounding fibrosis but no atypical proliferation. Which diagnosis is most likely?", "Fibrocystic change", ["DCIS", "Invasive lobular carcinoma", "Phyllodes tumor"], "Cysts, fibrosis, and apocrine metaplasia are fibrocystic change."),
        q("high", "A gross breast specimen contains multiple fluid-filled blue cysts, and microscopy shows flattened or apocrine epithelial lining with dense fibrous stroma. Which benign process is present?", "Nonproliferative fibrocystic change", ["Atypical ductal hyperplasia", "Medullary carcinoma", "Lobular carcinoma in situ"], "Blue-dome cysts are a classic benign fibrocystic feature."),
    ]),
    ("proliferative", "Proliferative Breast Disease Without Atypia", [
        q("easy", "Usual ductal hyperplasia is a proliferation of:", "Ductal epithelial and myoepithelial cells", ["Only adipocytes", "Only lymphocytes", "Only smooth muscle"], "UDH fills ducts with mixed epithelial cells."),
        q("easy", "Intraductal papilloma commonly presents with:", "Nipple discharge", ["Hematuria", "Jaundice", "Ascites"], "Papillomas often cause bloody or serous nipple discharge."),
        q("easy", "Sclerosing adenosis is a benign proliferation of:", "Lobular acini", ["Ureteric epithelium", "Cervical squamous cells", "Ovarian germ cells"], "Sclerosing adenosis increases acini within lobules."),
        q("moderate", "Proliferative breast disease without atypia carries:", "Slightly increased cancer risk", ["No possible risk", "BRCA-level risk", "Certain cancer"], "Risk is modestly increased."),
        q("moderate", "Radial scar can mimic carcinoma because it is:", "Stellate and fibrotic", ["Purely cystic", "Always encapsulated", "Composed of cartilage"], "Radial scars have central fibrosis and radiating ducts."),
        q("moderate", "Papilloma is composed of papillary fronds with:", "Fibrovascular cores", ["Schiller-Duval bodies", "Auer rods", "Keratin pearls"], "Papillomas grow on fibrovascular cores within ducts."),
        q("moderate", "Sclerosing adenosis preserves:", "Myoepithelial layer", ["Tumor invasion", "Necrotic comedo cores", "Lymphovascular emboli"], "Benign glands retain myoepithelial cells."),
        q("high", "A woman has spontaneous bloody nipple discharge. Excision shows a small subareolar intraductal lesion with branching fibrovascular cores lined by epithelial and myoepithelial cells. Which lesion is likely?", "Intraductal papilloma", ["DCIS", "Fibroadenoma", "Fat necrosis"], "Intraductal papillomas commonly cause bloody discharge."),
        q("high", "A mammographic stellate lesion resembles carcinoma, but biopsy shows a central fibroelastotic core with radiating entrapped ducts and preserved myoepithelial cells. Which benign lesion is present?", "Radial scar", ["Invasive ductal carcinoma", "Phyllodes tumor", "LCIS"], "Radial scar can mimic cancer radiologically and grossly."),
        q("high", "A breast biopsy shows crowded small glands in lobules with stromal fibrosis, but immunostains demonstrate intact myoepithelial cells around glands. Which lesion is most likely?", "Sclerosing adenosis", ["Tubular carcinoma", "Invasive lobular carcinoma", "Comedo DCIS"], "Sclerosing adenosis is benign but can mimic carcinoma."),
    ]),
    ("atypia-insitu", "Atypical Hyperplasia, DCIS, and LCIS", [
        q("easy", "Ductal carcinoma in situ is confined by the:", "Basement membrane", ["Pleura", "Renal capsule", "Serosa"], "DCIS does not invade through the basement membrane."),
        q("easy", "LCIS is often associated with loss of:", "E-cadherin", ["VHL", "HFE", "CFTR"], "Lobular neoplasia commonly loses E-cadherin."),
        q("easy", "Comedo necrosis is a pattern of:", "DCIS", ["Fibroadenoma", "Fat necrosis only", "Mastitis"], "Comedo DCIS has central necrosis in ducts."),
        q("moderate", "Atypical ductal hyperplasia resembles low-grade:", "DCIS", ["Invasive sarcoma", "Medullary carcinoma", "Paget disease only"], "ADH has some features of low-grade DCIS but is limited."),
        q("moderate", "LCIS is often:", "Multifocal and bilateral", ["Always palpable", "Always calcified", "Always inflammatory"], "LCIS can be incidental, multifocal, and bilateral."),
        q("moderate", "DCIS often presents on mammography as:", "Microcalcifications", ["Bone sclerosis", "Hydronephrosis", "Pleural effusion"], "Calcifications are a common screening clue."),
        q("moderate", "Paget disease of nipple is usually associated with underlying:", "DCIS or invasive carcinoma", ["Fibroadenoma only", "Simple cyst only", "Fat necrosis only"], "Malignant cells extend into nipple epidermis."),
        q("high", "A mammogram detects clustered microcalcifications. Biopsy shows malignant epithelial cells filling ducts with central necrotic debris, but myoepithelial cells and basement membrane remain intact. Which lesion is present?", "Ductal carcinoma in situ", ["Invasive ductal carcinoma", "LCIS", "Fibroadenoma"], "DCIS is malignant ductal proliferation without invasion."),
        q("high", "A breast biopsy shows discohesive cells expanding lobules, often with signet-ring forms, and immunostaining shows loss of E-cadherin without stromal invasion. Which diagnosis fits?", "Lobular carcinoma in situ", ["DCIS", "Invasive ductal carcinoma", "Papilloma"], "LCIS is a lobular neoplasia with E-cadherin loss."),
        q("high", "A woman has eczematous nipple changes. Biopsy shows malignant glandular cells scattered within epidermis, and imaging reveals underlying ductal carcinoma. Which condition is this?", "Paget disease of nipple", ["Lichen sclerosus", "Mammary duct ectasia", "Acute mastitis"], "Paget disease represents epidermal spread of carcinoma cells."),
    ]),
    ("benign-tumors", "Fibroadenoma, Phyllodes Tumor, and Stromal Lesions", [
        q("easy", "The most common benign breast tumor in young women is:", "Fibroadenoma", ["Angiosarcoma", "Medullary carcinoma", "LCIS"], "Fibroadenoma is common in young women."),
        q("easy", "Fibroadenoma is a benign tumor of stromal and:", "Epithelial components", ["Trophoblasts", "Renal tubules", "Squamous cervix"], "Fibroadenomas are biphasic fibroepithelial tumors."),
        q("easy", "Phyllodes tumor has leaf-like:", "Architecture", ["Necrosis only", "Koilocytosis", "Amyloid"], "Phyllodes tumors form cleft-like leaf-like spaces."),
        q("moderate", "Fibroadenomas are often:", "Well-circumscribed and mobile", ["Fixed and ulcerated always", "Diffuse inflammatory lesions", "Purely malignant"], "They are classically rubbery, mobile masses."),
        q("moderate", "Phyllodes tumor is more common in:", "Older women than fibroadenoma", ["Newborns only", "Men only", "Pregnancy always"], "Phyllodes tumors tend to occur later than fibroadenomas."),
        q("moderate", "Malignant phyllodes tumor metastasizes mainly by:", "Hematogenous spread", ["Ductal exfoliation", "Nipple epidermal spread", "Milk ducts only"], "Sarcomatous stroma can spread through blood."),
        q("moderate", "Fibroadenoma growth is often influenced by:", "Estrogen", ["Acrolein", "HPV E6", "Urate"], "Fibroadenomas may enlarge during pregnancy."),
        q("high", "A young woman has a firm, rubbery, freely mobile breast mass. Excision shows a well-circumscribed biphasic lesion with compressed ducts in fibrous stroma. Which tumor is likely?", "Fibroadenoma", ["Phyllodes tumor", "Invasive carcinoma", "Fat necrosis"], "Fibroadenoma is a benign circumscribed fibroepithelial tumor."),
        q("high", "A middle-aged woman has a large rapidly enlarging breast mass. Histology shows leaf-like clefts, hypercellular stroma, and increased stromal mitoses. Which fibroepithelial tumor is most likely?", "Phyllodes tumor", ["Fibroadenoma", "Intraductal papilloma", "DCIS"], "Phyllodes tumor is a stromal-rich leaf-like fibroepithelial tumor."),
        q("high", "A breast stromal tumor shows marked stromal atypia, infiltrative borders, overgrowth, and numerous mitoses, while epithelial elements are benign. Which component determines malignant behavior?", "Stromal component", ["Ductal epithelial component", "Nipple epidermis", "Myoepithelial calcification"], "Phyllodes tumor behavior depends on stromal features."),
    ]),
    ("invasive-types", "Invasive Breast Carcinoma: Major Histologic Types", [
        q("easy", "The most common invasive breast carcinoma is:", "Invasive ductal carcinoma no special type", ["Tubular carcinoma", "Mucinous carcinoma", "Angiosarcoma"], "NST/ductal carcinoma is the most common invasive type."),
        q("easy", "Invasive lobular carcinoma often shows loss of:", "E-cadherin", ["BRCA protein only", "Hemoglobin", "CFTR"], "Loss of E-cadherin produces discohesive cells."),
        q("easy", "Mucinous carcinoma produces abundant:", "Extracellular mucin", ["Keratin pearls only", "Bone matrix", "Amyloid always"], "Tumor cells float in pools of mucin."),
        q("moderate", "Invasive lobular carcinoma often grows in:", "Single-file pattern", ["Papillary fibrovascular cores", "Comedo ducts only", "Leaf-like clefts"], "Discohesive cells infiltrate in single files."),
        q("moderate", "Tubular carcinoma generally has:", "Good prognosis", ["Very poor prognosis always", "No gland formation", "Trophoblast differentiation"], "Tubular carcinoma is a well-differentiated favorable subtype."),
        q("moderate", "Medullary pattern carcinoma is associated with:", "Prominent lymphocytic infiltrate", ["No immune cells", "Schiller-Duval bodies", "Michaelis-Gutmann bodies"], "Medullary-like tumors have pushing borders and lymphocytes."),
        q("moderate", "Inflammatory carcinoma presents with peau d'orange due to:", "Dermal lymphatic invasion", ["Simple eczema", "Fibroadenoma compression", "Milk stasis only"], "Tumor emboli block dermal lymphatics."),
        q("high", "A breast mass is hard and irregular. Biopsy shows malignant epithelial cells forming tubules and nests within dense desmoplastic stroma. Which invasive carcinoma is most likely?", "Invasive ductal carcinoma no special type", ["Mucinous carcinoma", "Fibroadenoma", "LCIS"], "Invasive ductal carcinoma NST commonly induces desmoplasia."),
        q("high", "A breast biopsy shows small discohesive tumor cells infiltrating stroma in single-file cords, with signet-ring cells and absent E-cadherin staining. Which carcinoma type is present?", "Invasive lobular carcinoma", ["Invasive ductal carcinoma NST", "Tubular carcinoma", "Papillary carcinoma"], "Invasive lobular carcinoma loses E-cadherin and grows single-file."),
        q("high", "A patient has rapid breast enlargement, erythema, edema, and peau d'orange without a discrete mass. Biopsy shows carcinoma emboli in dermal lymphatics. Which diagnosis is most likely?", "Inflammatory breast carcinoma", ["Acute mastitis only", "Fibroadenoma", "Mammary duct ectasia"], "Inflammatory carcinoma is defined clinically and involves dermal lymphatics."),
    ]),
    ("molecular-risk", "Breast Cancer Risk Factors and Molecular Subtypes", [
        q("easy", "BRCA1 mutation increases risk of:", "Breast and ovarian carcinoma", ["Wilms tumor only", "Cervical LSIL only", "Leiomyoma only"], "BRCA1 is a hereditary breast-ovarian cancer gene."),
        q("easy", "Estrogen receptor-positive tumors may respond to:", "Endocrine therapy", ["Antibiotics only", "Iron chelation", "Appendectomy"], "ER-positive cancers can be treated with anti-estrogen strategies."),
        q("easy", "HER2-positive breast cancers may respond to:", "Trastuzumab", ["Warfarin", "Metformin", "Acyclovir"], "Trastuzumab targets HER2 overexpression/amplification."),
        q("moderate", "Triple-negative breast cancer lacks ER, PR, and:", "HER2", ["E-cadherin always", "Keratin", "p53"], "Triple-negative tumors are ER-negative, PR-negative, HER2-negative."),
        q("moderate", "BRCA1-associated cancers are often:", "Triple-negative", ["Always HER2-positive", "Always mucinous", "Always benign"], "Many BRCA1 cancers are basal-like/triple-negative."),
        q("moderate", "Luminal A breast cancers are usually:", "ER-positive and lower grade", ["ER-negative and HER2 amplified", "Sarcomas", "Only in men"], "Luminal A tumors tend to be hormone receptor positive."),
        q("moderate", "The strongest prognostic factor in breast carcinoma is:", "Axillary lymph node status", ["Tumor color", "Breast size", "Nipple discharge alone"], "Nodal metastasis is a major prognostic marker."),
        q("high", "A breast carcinoma is ER-positive, PR-positive, HER2-negative, low grade, slowly proliferative, and likely to respond to endocrine therapy. Which molecular subtype is most consistent?", "Luminal A", ["HER2-enriched", "Basal-like", "Triple-negative medullary"], "Luminal A cancers are hormone receptor positive and lower grade."),
        q("high", "A young woman with BRCA1 mutation develops a high-grade invasive carcinoma that lacks ER, PR, and HER2 expression but expresses basal cytokeratins. Which subtype is favored?", "Basal-like triple-negative carcinoma", ["Luminal A carcinoma", "HER2-enriched carcinoma", "Mucinous carcinoma"], "BRCA1-associated cancers are commonly basal-like/triple-negative."),
        q("high", "A breast cancer shows HER2 amplification by testing and strong complete membranous staining on immunohistochemistry in invasive tumor cells. Which targeted treatment class is most directly relevant?", "Anti-HER2 therapy", ["Anti-estrogen therapy only", "Antibiotic therapy", "Iron chelation"], "HER2-positive tumors may respond to trastuzumab and related agents."),
    ]),
    ("clinical-pathology", "Breast Carcinoma Clinical Features, Spread, and Staging", [
        q("easy", "Breast carcinoma commonly spreads first to:", "Axillary lymph nodes", ["Spleen only", "Appendix", "Thymus"], "Axillary nodes are common regional drainage sites."),
        q("easy", "Peau d'orange reflects edema of:", "Skin", ["Bone marrow", "Endometrium", "Renal pelvis"], "Dermal lymphatic obstruction causes skin edema."),
        q("easy", "Sentinel lymph node biopsy assesses:", "Regional nodal spread", ["Serum calcium", "Uterine invasion", "Renal function"], "Sentinel node status evaluates early lymphatic spread."),
        q("moderate", "Breast cancer commonly metastasizes to bone, lung, liver, and:", "Brain", ["Appendix only", "Gallbladder only", "Thyroid only"], "These are common distant metastatic sites."),
        q("moderate", "Skin dimpling in breast cancer can result from:", "Cooper ligament retraction", ["Milk production", "Cyst rupture only", "Duct ectasia only"], "Tumor fibrosis can pull on suspensory ligaments."),
        q("moderate", "Nipple retraction can occur when tumor involves:", "Lactiferous ducts and stroma", ["Renal tubules", "Ovarian follicles", "Ureter"], "Fibrosis near ducts can retract the nipple."),
        q("moderate", "Tumor size is part of:", "TNM staging", ["Gleason grading", "Ann Arbor staging only", "FIGO cervical cytology"], "T category reflects tumor size and extent."),
        q("high", "A breast carcinoma has a small primary tumor but metastasis in multiple axillary lymph nodes on sentinel node evaluation. Which clinicopathologic factor most strongly worsens prognosis?", "Regional lymph node involvement", ["Apocrine metaplasia", "Cyst formation", "Breast pain"], "Axillary nodal metastasis is a major prognostic variable."),
        q("high", "A woman has a hard breast carcinoma causing nipple retraction and skin dimpling. These changes are best explained by tumor-associated fibrosis pulling on ducts and Cooper ligaments.", "Desmoplastic stromal reaction", ["Simple lactational change", "Benign apocrine metaplasia", "Acute abscess drainage"], "Desmoplasia and stromal invasion can distort skin and nipple."),
        q("high", "A surgeon injects tracer near a breast tumor and removes the first draining axillary node to evaluate early regional spread. Which procedure is being performed?", "Sentinel lymph node biopsy", ["Core needle biopsy only", "Mastectomy margin inking", "Fine needle aspiration of cyst"], "Sentinel node biopsy samples the first lymphatic drainage node."),
    ]),
    ("male-gynecomastia", "Male Breast, Gynecomastia, and Special Populations", [
        q("easy", "Gynecomastia is enlargement of male:", "Breast tissue", ["Prostate only", "Testis only", "Bladder wall"], "Gynecomastia is benign male breast enlargement."),
        q("easy", "Male breast carcinoma most commonly occurs as:", "Invasive ductal carcinoma", ["Invasive lobular carcinoma", "Fibroadenoma", "Mature teratoma"], "Men have few lobules, so lobular tumors are rare."),
        q("easy", "Klinefelter syndrome increases risk of:", "Male breast cancer", ["Cervical carcinoma", "Wilms tumor", "Endometriosis"], "Klinefelter syndrome raises male breast cancer risk."),
        q("moderate", "Gynecomastia often results from increased estrogen-to:", "Androgen ratio", ["Progesterone ratio only", "Insulin ratio", "Bile acid ratio"], "Relative estrogen excess stimulates ductal tissue."),
        q("moderate", "Histology of gynecomastia shows:", "Ductal epithelial hyperplasia with stromal edema", ["Lobular carcinoma in situ", "Comedo necrosis", "Schiller-Duval bodies"], "Male gynecomastia features ductal proliferation and edema."),
        q("moderate", "Male breast cancer often presents as a:", "Subareolar mass", ["Diffuse ovarian cyst", "Renal colic", "Vulvar plaque"], "Male breast tumors commonly arise near the nipple."),
        q("moderate", "BRCA2 mutation is especially associated with:", "Male breast carcinoma", ["Bartholin cyst", "Leiomyoma", "Choriocarcinoma"], "BRCA2 increases male breast cancer risk."),
        q("high", "A man with cirrhosis develops bilateral tender subareolar breast enlargement. Biopsy shows ductal epithelial proliferation and edematous stroma without lobule formation. Which diagnosis fits?", "Gynecomastia", ["Male breast carcinoma", "Fibroadenoma", "Fat necrosis"], "Cirrhosis can increase estrogen effect and cause gynecomastia."),
        q("high", "An older man has a firm subareolar breast mass with nipple retraction. Biopsy shows invasive malignant duct-forming epithelial cells. Which carcinoma type is most likely?", "Invasive ductal carcinoma", ["Invasive lobular carcinoma", "Yolk sac tumor", "Leiomyosarcoma"], "Male breast cancer is usually invasive ductal carcinoma."),
        q("high", "A man with Klinefelter syndrome and family history of BRCA2 mutation develops a unilateral hard breast mass. Which inherited or chromosomal context raises his cancer risk?", "Klinefelter syndrome and BRCA2 mutation", ["Turner syndrome and VHL mutation", "CFTR mutation only", "HFE mutation only"], "Both Klinefelter syndrome and BRCA2 increase male breast carcinoma risk."),
    ]),
    ("therapy-markers", "Predictive Markers, Biopsy Interpretation, and Treatment Correlations", [
        q("easy", "ER testing in breast cancer predicts response to:", "Hormonal therapy", ["Antibiotics", "Dialysis", "Antifungals"], "ER positivity predicts benefit from endocrine treatment."),
        q("easy", "HER2 is assessed because it predicts response to:", "Targeted anti-HER2 therapy", ["Appendectomy", "Iron therapy", "Antivirals"], "HER2 amplification guides targeted therapy."),
        q("easy", "Core needle biopsy is used to sample:", "Breast lesions", ["Only cervical lesions", "Only renal stones", "Only bile ducts"], "Core biopsy provides tissue architecture for diagnosis."),
        q("moderate", "Myoepithelial cell markers help distinguish in situ disease from:", "Invasive carcinoma", ["Fibrocystic cysts", "Mastitis", "Gynecomastia"], "Invasion lacks a myoepithelial layer."),
        q("moderate", "Calcifications in DCIS often reflect:", "Necrotic intraductal debris", ["Bone metastasis", "Gallstones", "Urate stones"], "Comedo necrosis may calcify in ducts."),
        q("moderate", "Ki-67 is a marker of:", "Cell proliferation", ["Estrogen synthesis", "Mucin secretion", "Calcium deposition"], "Ki-67 estimates proliferative activity."),
        q("moderate", "A positive surgical margin means tumor is present at:", "Ink on specimen edge", ["Sentinel node only", "Skin surface only", "Radiology report only"], "Ink on tumor indicates involved margin."),
        q("high", "A breast biopsy shows malignant epithelial cells within ducts, but p63 and smooth muscle myosin staining highlight a continuous myoepithelial layer. Which broad category is supported?", "In situ carcinoma", ["Invasive carcinoma", "Sarcoma", "Lymphoma"], "Myoepithelial preservation supports noninvasive ductal disease."),
        q("high", "A lumpectomy specimen for invasive carcinoma has tumor cells touching the inked surgical edge on microscopic examination. Which pathology finding indicates need for margin consideration?", "Positive surgical margin", ["Negative sentinel node", "Apocrine metaplasia", "Low Ki-67 alone"], "Tumor at ink means the excision margin is involved."),
        q("high", "A breast carcinoma is ER-negative, PR-negative, and HER2-negative with high proliferation index and basal-like invasive morphology. Which treatment implication follows from this receptor profile?", "Endocrine and HER2-targeted therapies are unlikely to help", ["Tamoxifen is strongly indicated", "Trastuzumab alone is curative", "No chemotherapy can be used"], "Triple-negative cancers lack ER/PR/HER2 therapeutic targets."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch23-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 23 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch23-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 23 questions")
    print(f"Removed {total_removed} existing Chapter 23 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 23 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
