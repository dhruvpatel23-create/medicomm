# -*- coding: utf-8 -*-
"""
FMGE Grand Test 1 - Part 1: Block 2
Pathology (13 Qs) + Microbiology (13 Qs) + Pharmacology (13 Qs) + Forensic Medicine (10 Qs) = 49 Questions (Q052 - Q100)
Strict adherence to 2026 NBE pattern, clinical vignettes, option-by-option review.
Zero textbook citations.
"""

QUESTIONS = [
    # ==========================================
    # PATHOLOGY (13 Questions: Q052 - Q064)
    # ==========================================
    {
        "id": "fmge-gt1-q052",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Hematopathology - Hodgkin Lymphoma",
        "prompt": "A 24-year-old male presents with painless enlargement of left supraclavicular lymph nodes, night sweats, and low-grade fever. Excisional lymph node biopsy reveals large binucleated giant cells with prominent eosinophilic inclusion-like nucleoli resembling 'owl eyes', surrounded by a reactive background of lymphocytes, plasma cells, and eosinophils. Which cell type is the diagnostic hallmark of this malignancy?",
        "options": [
            "Reed-Sternberg cell",
            "Gaucher cell",
            "Langerhans giant cell",
            "Touton giant cell"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe clinical presentation of young adult B-symptoms (fever, night sweats, weight loss) and painless cervical lymphadenopathy is classic for Hodgkin lymphoma. The microscopic pathognomonic hallmark is the Reed-Sternberg (RS) cell: a giant cell derived from germinal center B cells, containing bilobed or multilobed nuclei with prominent, eosinophilic, inclusion-like nucleoli surrounded by a clear halo ('owl-eye' appearance). RS cells characteristically express CD15 and CD30.\n\nOption Review:\n- Option A is correct because classical Reed-Sternberg cells are the diagnostic neoplastic cells of Hodgkin lymphoma.\n- Option B is incorrect because Gaucher cells are lipid-laden macrophages with a 'wrinkled tissue paper' cytoplasm seen in Gaucher disease.\n- Option C is incorrect because Langhans giant cells have a horseshoe-shaped arrangement of nuclei seen in granulomatous conditions like tuberculosis.\n- Option D is incorrect because Touton giant cells have a ring of nuclei surrounding central cytoplasm with a foamy peripheral border seen in xanthomas.\n\nKey Takeaway: Reed-Sternberg cells displaying characteristic 'owl-eye' binucleated morphology are the diagnostic hallmark of classic Hodgkin lymphoma.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Reed-Sternberg_cell.jpg/640px-Reed-Sternberg_cell.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q053",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Renal Pathology - Nephrotic Syndrome (Membranous)",
        "prompt": "A 48-year-old male presents with bilateral pedal edema and heavy proteinuria (6.5 g/24 h). Renal biopsy reveals diffuse thickening of the glomerular basement membrane on light microscopy, silver methenamine staining shows a 'spike and dome' pattern, and electron microscopy demonstrates subepithelial electron-dense deposits. Which primary glomerular disease is present?",
        "options": [
            "Minimal change disease",
            "Membranous nephropathy",
            "Focal segmental glomerulosclerosis",
            "Post-streptococcal glomerulonephritis"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nMembranous nephropathy is the most common cause of primary nephrotic syndrome in non-diabetic Caucasian adults. In ~70% of primary cases, autoantibodies against the M-type phospholipase A2 receptor (PLA2R) on podocytes form in situ immune complexes. On electron microscopy, these immune deposits are situated in the subepithelial space (between podocyte foot processes and the glomerular basement membrane). Over time, the GBM lays down matrix around the deposits, producing the pathognomonic 'spike and dome' pattern on silver stains.\n\nOption Review:\n- Option A is incorrect because minimal change disease shows normal glomeruli on light microscopy and diffuse effacement of podocyte foot processes without immune deposits.\n- Option B is correct because membranous nephropathy shows diffuse basement membrane thickening with subepithelial deposits and 'spike and dome' architecture.\n- Option C is incorrect because FSGS shows sclerosis involving segments of some glomeruli, typically with hyalinosis and podocyte detachment.\n- Option D is incorrect because PSGN presents with nephritic syndrome (hematuria, hypertension) and subepithelial 'humps' on electron microscopy.\n\nKey Takeaway: Membranous nephropathy is characterized by diffuse GBM thickening, subepithelial immune deposits, and a 'spike and dome' appearance on silver stain.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q054",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Cardiovascular Pathology - Myocardial Infarction Timelines",
        "prompt": "A 58-year-old male dies suddenly 4 days after an acute transmural anterior myocardial infarction. Histopathological examination of the infarcted left ventricular myocardium reveals extensive coagulation necrosis with complete loss of cardiomyocyte nuclei (ghost cells), dense neutrophilic infiltration, and early phagocytosis by macrophages at the borders. What is the most feared mechanical complication occurring during this specific post-infarct window?",
        "options": [
            "Ventricular free wall rupture",
            "Fibrinous pericarditis",
            "Dressler syndrome",
            "Left ventricular aneurysm"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nBetween 3 to 7 days post-myocardial infarction, extensive macrophage infiltration and proteolytic enzyme release digest the necrotic tissue, rendering the myocardium structurally weakest. This is the period of peak incidence for life-threatening cardiac rupture complications: 1) Ventricular free wall rupture leading to acute hemopericardium and cardiac tamponade; 2) Interventricular septum rupture causing acute VSD; 3) Papillary muscle rupture (most commonly posteromedial) causing acute severe mitral regurgitation and pulmonary edema.\n\nOption Review:\n- Option A is correct because free wall rupture typically peaks between days 3 to 7 when necrotic myocardium is maximally softened by macrophage digestion.\n- Option B is incorrect because fibrinous pericarditis (friction rub) occurs earlier, between days 1 to 3.\n- Option C is incorrect because Dressler syndrome is an autoimmune pericarditis that develops 2 to 8 weeks post-MI.\n- Option D is incorrect because ventricular aneurysm is a late complication occurring months post-MI as collagen scar stretches under ventricular pressure.\n\nKey Takeaway: Mechanical cardiac rupture (free wall, septum, or papillary muscle) peaks 3 to 7 days post-myocardial infarction when macrophage infiltration and tissue breakdown are maximal.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q055",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Gastrointestinal Pathology - Gastric Adenocarcinoma",
        "prompt": "A 55-year-old male presents with persistent epigastric pain, early satiety, and progressive weight loss. Upper endoscopy reveals an ulcerated infiltrative lesion in the gastric antrum. Microscopic examination demonstrates discohesive signet-ring cells with abundant intracellular mucin displacing the nucleus to the periphery, infiltrating the muscularis propria. Loss of function of which adhesion molecule is characteristic of diffuse gastric carcinoma?",
        "options": [
            "E-cadherin",
            "Vascular endothelial growth factor",
            "Beta-catenin",
            "Fibronectin"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAccording to the Lauren classification, gastric adenocarcinoma is divided into intestinal and diffuse types. Diffuse gastric carcinoma (linitis plastica) is characterized by discohesive, infiltrative single cells or small clusters containing large cytoplasmic vacuoles of mucin that push the nucleus against the cell membrane, forming classic 'signet-ring cells'. The molecular hallmark of hereditary and sporadic diffuse gastric cancer is loss of the cell-cell adhesion glycoprotein E-cadherin, encoded by the CDH1 gene. Without E-cadherin, tumor cells fail to form glands and diffusely infiltrate the gastric wall.\n\nOption Review:\n- Option A is correct because CDH1 mutations resulting in loss of E-cadherin expression drive diffuse (signet-ring) gastric cancer.\n- Option B is incorrect because VEGF promotes angiogenesis, but is not the specific primary defect causing discohesive signet-ring morphology.\n- Option C is incorrect because beta-catenin interacts with E-cadherin, but CDH1 loss itself is the cardinal mutation.\n- Option D is incorrect because fibronectin is an extracellular matrix glycoprotein rather than the epithelial adhesion molecule.\n\nKey Takeaway: Diffuse gastric carcinoma is characterized by signet-ring cells and is molecularly driven by loss of E-cadherin (CDH1) function.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Signet_ring_cell_carcinoma_histopathology.jpg/640px-Signet_ring_cell_carcinoma_histopathology.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q056",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "General Pathology - Types of Necrosis",
        "prompt": "A 66-year-old female with long-standing atrial fibrillation presents with acute onset of right-sided hemiplegia and aphasia. Brain MRI demonstrates an acute ischemic infarction in the territory of the left middle cerebral artery. What characteristic type of necrosis develops in central nervous system infarctions?",
        "options": [
            "Coagulative necrosis",
            "Liquefactive necrosis",
            "Caseous necrosis",
            "Fibrinoid necrosis"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nIn the central nervous system, ischemic injury results in liquefactive necrosis. Unlike other solid organs (such as the kidney, heart, and spleen), which undergo coagulative necrosis with preservation of basic tissue architecture for days, brain tissue is rich in lipids and hydrolytic lysosomal enzymes released by microglia and infiltrating neutrophils. Rapid enzymatic digestion of dead cells transforms the infarcted parenchyma into a viscous liquid mass (cerebral softening or encephalomalacia), eventually leaving a cystic fluid-filled cavity surrounded by a glial scar (astrogliosis).\n\nOption Review:\n- Option A is incorrect because coagulative necrosis occurs in ischemic infarctions of all solid visceral organs EXCEPT the brain.\n- Option B is correct because cerebral infarctions characteristically manifest as liquefactive necrosis.\n- Option C is incorrect because caseous necrosis is a friable, cheese-like necrosis characteristic of tuberculous granulomas.\n- Option D is incorrect because fibrinoid necrosis occurs in immune vasculitis and malignant hypertension where immune complexes and fibrin deposit in vessel walls.\n\nKey Takeaway: Ischemic strokes characteristically undergo liquefactive necrosis due to high brain lipid content and rapid hydrolytic enzymatic digestion.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q057",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Hematopathology - Chronic Myeloid Leukemia (CML)",
        "prompt": "A 52-year-old male is found to have massive splenomegaly on routine physical examination. Complete blood count reveals leukocytosis (WBC 145,000/microL) with a full spectrum of granulocytic precursors (myelocytes, metamyelocytes, band forms) and marked basophilia. The leukocyte alkaline phosphatase (LAP) score is low (12). Cytogenetic analysis demonstrates a reciprocal translocation between chromosomes 9 and 22. What fusion oncoprotein possesses constitutive tyrosine kinase activity in this disorder?",
        "options": [
            "BCR-ABL1",
            "PML-RARA",
            "MYC-IGH",
            "BCL2-IGH"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe clinical presentation of middle-aged patient with massive splenomegaly, marked granulocytic leukocytosis with basophilia, and a low LAP score is classic for Chronic Myeloid Leukemia (CML). The genetic hallmark of CML is the Philadelphia chromosome, t(9;22)(q34;q11.2). This reciprocal translocation fuses the ABL1 proto-oncogene from chromosome 9 with the BCR gene on chromosome 22, generating a BCR-ABL1 chimeric oncoprotein with unregulated, constitutive tyrosine kinase activity that drives uncontrolled granulopoiesis. It is treated with targeted tyrosine kinase inhibitors like imatinib.\n\nOption Review:\n- Option A is correct because the BCR-ABL1 fusion oncoprotein is the molecular driver of CML.\n- Option B is incorrect because PML-RARA arises from t(15;17) in Acute Promyelocytic Leukemia (APL), responsive to all-trans retinoic acid.\n- Option C is incorrect because MYC-IGH arises from t(8;14) in Burkitt lymphoma, driving c-myc overexpression.\n- Option D is incorrect because BCL2-IGH arises from t(14;18) in Follicular lymphoma, inhibiting apoptosis.\n\nKey Takeaway: The Philadelphia chromosome t(9;22) produces the BCR-ABL1 fusion tyrosine kinase, which is the diagnostic and therapeutic target in CML.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q058",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Immunopathology - Amyloidosis Staining",
        "prompt": "A 68-year-old male with multiple myeloma presents with congestive heart failure and carpal tunnel syndrome. An abdominal fat pad biopsy is performed to evaluate for systemic amyloidosis. Light microscopy using Congo red stain reveals pink-red amorphous deposits. Under polarized light microscopy, which characteristic optical property confirms the presence of cross-beta-pleated amyloid fibrils?",
        "options": [
            "Apple-green birefringence",
            "Golden-yellow fluorescence",
            "Metachromatic violet staining",
            "Prussian blue positive granular reaction"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAmyloidosis is characterized by the extracellular deposition of misfolded protein fibrils arranged in a cross-beta-pleated sheet conformation. In light microscopy, Congo red dye intercalates between the beta-sheets, staining the deposits salmon-pink. Under polarized light microscopy, the regular parallel orientation of the Congo red-amyloid complex splits polarized light into two rays with different refractive indices, producing pathognomonic 'apple-green birefringence'.\n\nOption Review:\n- Option A is correct because Congo red-stained amyloid exhibits apple-green birefringence under polarized light.\n- Option B is incorrect because golden-yellow fluorescence is not an amyloid confirmation property (Thioflavin T produces yellow-green fluorescence under UV, but Congo red polarization is the gold standard).\n- Option C is incorrect because metachromatic violet staining occurs with crystal violet or methyl violet, but is less specific than Congo red polarization.\n- Option D is incorrect because Prussian blue stains ferric iron deposits (hemosiderin) blue.\n\nKey Takeaway: Congo red staining displaying apple-green birefringence under polarized light is the diagnostic gold standard for amyloid fibril deposition.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Amyloidosis%2C_Congo_red.jpg/640px-Amyloidosis%2C_Congo_red.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q059",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Neoplasia - Tumor Suppressor p53",
        "prompt": "A 28-year-old female presents with an osteosarcoma of the femur. Detailed family history reveals that her mother died of premenopausal breast cancer at age 32, her maternal uncle had a soft-tissue sarcoma, and her brother developed an adrenocortical carcinoma. Genetic sequencing reveals a germline mutation in the TP53 gene (Li-Fraumeni syndrome). What is the primary cellular function of the p53 protein in normal cells during DNA damage?",
        "options": [
            "Arrests the cell cycle at the G1/S transition to allow DNA repair",
            "Phosphorylates the retinoblastoma protein to promote E2F release",
            "Activates telomerase to prevent cellular senescence",
            "Directly unwinds damaged DNA strands during replication"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe p53 protein, encoded by the TP53 tumor suppressor gene on chromosome 17p, is known as the 'guardian of the genome'. In response to DNA damage, cellular stress, or hypoxia, p53 levels rise. Active p53 acts as a transcription factor that upregulates p21 (CDKN1A), an inhibitor of cyclin-dependent kinases (CDKs). Inhibition of CDKs prevents retinoblastoma protein (Rb) phosphorylation, arresting the cell cycle at the G1/S checkpoint to allow DNA repair. If damage is irreparable, p53 upregulates BAX and PUMA to induce apoptosis.\n\nOption Review:\n- Option A is correct because p53 primarily arrests the cell cycle at G1/S via p21 induction to permit repair or trigger apoptosis.\n- Option B is incorrect because Rb phosphorylation promotes cell cycle progression, whereas p53 inhibits this process.\n- Option C is incorrect because telomerase activation is an oncogenic mechanism, not a tumor suppressor action.\n- Option D is incorrect because DNA helicases unwind DNA, which is not the function of p53.\n\nKey Takeaway: The p53 tumor suppressor arrests the cell cycle at the G1/S transition via p21 upregulation to permit DNA repair or trigger apoptosis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q060",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Endocrine Pathology - Papillary Thyroid Carcinoma",
        "prompt": "A 34-year-old woman presents with a painless, solitary cold nodule in the right lobe of the thyroid gland. Fine needle aspiration biopsy reveals papillae lined by cells with ground-glass nuclei, optical clearing ('Orphan Annie eyes'), intranuclear cytoplasmic pseudoinclusions, and concentric laminated calcifications. Which diagnosis is established by these cytological features?",
        "options": [
            "Follicular thyroid carcinoma",
            "Papillary thyroid carcinoma",
            "Medullary thyroid carcinoma",
            "Anaplastic thyroid carcinoma"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nPapillary thyroid carcinoma (PTC) is the most common thyroid malignancy (~85% of cases), typically presenting in young adult females and associated with prior head/neck radiation exposure or RET/PTC rearrangements and BRAF V600E mutations. The diagnosis is based on pathognomonic nuclear features: 1) Optically clear chromatin resulting in empty-appearing nuclei ('Orphan Annie eye' nuclei); 2) Intranuclear grooves ('coffee-bean' nuclei); 3) Intranuclear cytoplasmic pseudoinclusions. Concentrically laminated, calcified microcalcifications called psammoma bodies are present in approximately 50% of cases.\n\nOption Review:\n- Option A is incorrect because follicular carcinoma requires histological demonstration of capsular or vascular invasion, which cannot be diagnosed by FNA, and lacks Orphan Annie nuclei.\n- Option B is correct because Orphan Annie eye nuclei, pseudoinclusions, and psammoma bodies are diagnostic of papillary thyroid carcinoma.\n- Option C is incorrect because medullary thyroid carcinoma arises from parafollicular C-cells and shows amyloid stroma with calcitonin positivity.\n- Option D is incorrect because anaplastic thyroid carcinoma presents in the elderly as a rapidly enlarging, aggressive mass with pleomorphic giant cells.\n\nKey Takeaway: Papillary thyroid carcinoma is diagnosed by nuclear clearing ('Orphan Annie eyes'), nuclear grooves, pseudoinclusions, and psammoma bodies.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Papillary_thyroid_carcinoma_fine_needle_aspiration_biopsy.jpg/640px-Papillary_thyroid_carcinoma_fine_needle_aspiration_biopsy.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q061",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Pulmonary Pathology - Asbestos Bodies",
        "prompt": "A 62-year-old shipyard worker presents with progressive exertional dyspnea and persistent dry cough. High-resolution chest CT shows bilateral lower lobe interstitial fibrosis and diaphragmatic pleural plaques. Bronchoalveolar lavage reveals golden-brown, beaded, dumbbell-shaped fibers with a transparent central core that stain intensely positive with Prussian blue. What are these characteristic structures called?",
        "options": [
            "Ferruginous bodies",
            "Asteroid bodies",
            "Schaumann bodies",
            "Charcot-Leyden crystals"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAsbestosis is an occupational pneumoconiosis seen in shipyard workers, pipefitters, insulators, and construction workers. Inhaled asbestos fibers lodge in small airways and are engulfed by alveolar macrophages, which coat the fibers with iron-rich ferritin and proteins. This produces golden-brown, elongated, beaded rods with clubbed or dumbbell-shaped ends known as asbestos bodies (ferruginous bodies). Because they are encrusted with hemosiderin, they stain deep blue with Prussian blue (Perls' stain).\n\nOption Review:\n- Option A is correct because ferruginous (asbestos) bodies are golden-brown, beaded, dumbbell-shaped fibers encrusted with iron.\n- Option B is incorrect because asteroid bodies are star-shaped inclusions within giant cells seen in sarcoidosis.\n- Option C is incorrect because Schaumann bodies are laminated calcific basophilic inclusions seen in sarcoidosis.\n- Option D is incorrect because Charcot-Leyden crystals are bipyramidal crystals derived from eosinophil major basic protein seen in asthma.\n\nKey Takeaway: Ferruginous bodies are dumbbell-shaped, iron-protein coated asbestos fibers that stain positive with Prussian blue in asbestosis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q062",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Vascular Pathology - Polyarteritis Nodosa (PAN)",
        "prompt": "A 44-year-old male with chronic hepatitis B infection presents with fever, weight loss, severe abdominal pain after meals, and wrist drop. Blood pressure is 170/100 mmHg. Angiography reveals multiple microaneurysms alternating with segmental stenoses ('string-of-pearls') in mesenteric and renal arteries. Biopsy of a medium-sized artery demonstrates transmural necrotizing inflammation with fibrinoid necrosis. What size of blood vessels is primarily involved in polyarteritis nodosa?",
        "options": [
            "Large elastic arteries",
            "Medium-sized muscular arteries",
            "Small postcapillary venules",
            "Arterioles and capillaries only"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nPolyarteritis nodosa (PAN) is a systemic necrotizing vasculitis that characteristically targets medium-sized muscular arteries (such as the renal, mesenteric, and coronary vessels), with approximately 30% of cases linked to chronic hepatitis B virus infection. Histopathology reveals segmental, transmural necrotizing inflammation with fibrinoid necrosis. Coexistence of acute destructive lesions with fibrous healing in adjacent segments weakens the vessel wall, creating microaneurysms alternating with stenoses that produce the classic 'string-of-pearls' or 'rosary sign' on angiography. Crucially, pulmonary vessels are characteristically spared.\n\nOption Review:\n- Option A is incorrect because large elastic arteries (aorta and main branches) are involved in Takayasu arteritis and Giant Cell Arteritis.\n- Option B is correct because PAN is the prototypical necrotizing vasculitis of medium-sized muscular arteries.\n- Option C is incorrect because small postcapillary venules are involved in leukocytoclastic (hypersensitivity) vasculitis.\n- Option D is incorrect because small vessels (arterioles, capillaries) are involved in microscopic polyangiitis and Granulomatosis with Polyangiitis (ANCA-associated).\n\nKey Takeaway: Polyarteritis nodosa (PAN) is a necrotizing vasculitis of medium-sized muscular arteries associated with hepatitis B, producing 'string-of-pearls' aneurysms while sparing pulmonary circulation.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q063",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Bone Pathology - Osteosarcoma Histopathology",
        "prompt": "A 16-year-old boy presents with progressive pain and swelling over the distal femur. Plain radiograph shows a mixed lytic and blastic lesion in the metaphysis with periosteal elevation producing a Codman triangle and a 'sunburst' pattern of spiculation. Biopsy demonstrates malignant pleomorphic spindle cells. What pathognomonic matrix production by malignant osteoblasts is required to establish the diagnosis of osteosarcoma?",
        "options": [
            "Osteoid matrix",
            "Chondroid matrix",
            "Fibrous matrix",
            "Osteoclast giant cells"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nOsteosarcoma is the most common primary malignant bone tumor in children and adolescents (second peak in elderly with Paget disease), typically arising in the metaphysis of long bones (around the knee in >50% of cases: distal femur, proximal tibia). Radiography reveals bone destruction, soft-tissue extension, Codman triangle (periosteal lifting), and 'sunburst' periosteal reaction. Histopathologically, osteosarcomas show marked pleomorphism, hyperchromasia, and frequent mitoses, but the essential, definitive histological diagnostic criteria is the direct production of unmineralized bone matrix (osteoid) by malignant mesenchymal osteoblast cells.\n\nOption Review:\n- Option A is correct because the direct synthesis of osteoid matrix by malignant cells is the absolute diagnostic criterion for osteosarcoma.\n- Option B is incorrect because chondroid matrix is characteristic of chondrosarcoma (though chondroblastic osteosarcoma may have cartilage, osteoid is still mandatory).\n- Option C is incorrect because fibrous matrix is found in fibrosarcomas.\n- Option D is incorrect because osteoclast giant cells are the primary feature of giant cell tumor of bone (osteoclastoma).\n\nKey Takeaway: Direct synthesis of osteoid matrix by malignant tumor cells is the indispensable histopathological criterion for osteosarcoma.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q064",
        "subjectId": "pathology",
        "subjectTitle": "Pathology",
        "topic": "Female Genital Pathology - Complete vs Partial Hydatidiform Mole",
        "prompt": "A 22-year-old woman at 11 weeks of gestation presents with painless vaginal bleeding. Transvaginal ultrasound demonstrates an enlarged uterus filled with a diffuse echogenic mass containing multiple small cystic spaces ('snowstorm' pattern), with no detectable fetal parts. Serum beta-hCG is 240,000 mIU/mL. Evacuation reveals grape-like vesicles. Cytogenetic analysis reveals a 46,XX karyotype entirely of paternal origin. What is this gestational trophoblastic disease?",
        "options": [
            "Partial hydatidiform mole",
            "Complete hydatidiform mole",
            "Choriocarcinoma",
            "Placental site trophoblastic tumor"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nHydatidiform moles are gestational trophoblastic diseases. A complete mole arises when an enucleated egg is fertilized by a single haploid sperm that duplicates its DNA (46,XX, ~90%) or by two sperm (46,XY), resulting in purely androgenetic/paternal genetic material. Grossly, all villi are hydropic, resembling 'bunches of grapes'. Histologically, there is diffuse, circumferential trophoblastic proliferation, marked villous edema (cisterns), and total absence of fetal tissue. Extremely high beta-hCG and a 'snowstorm' ultrasound are classic. It carries a 2% to 3% risk of choriocarcinoma.\n\nOption Review:\n- Option A is incorrect because a partial mole is triploid (69,XXY), contains both maternal and paternal DNA, features focal trophoblastic hyperplasia, and usually contains identifiable fetal parts with lower beta-hCG.\n- Option B is correct because 46,XX androgenetic karyotype, absence of fetal parts, grape-like vesicles, and massive beta-hCG define a complete hydatidiform mole.\n- Option C is incorrect because choriocarcinoma is a malignant tumor composed of sheets of syncytiotrophoblasts and cytotrophoblasts without chorionic villi.\n- Option D is incorrect because placental site trophoblastic tumor produces intermediate trophoblasts and low beta-hCG.\n\nKey Takeaway: Complete hydatidiform moles have a 46,XX androgenetic paternal karyotype, diffuse hydropic villi, marked beta-hCG elevation, and no fetal parts.",
        "imageUrls": []
    },

    # ==========================================
    # MICROBIOLOGY (13 Questions: Q065 - Q077)
    # ==========================================
    {
        "id": "fmge-gt1-q065",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Bacteriology - Mycobacterium tuberculosis Media",
        "prompt": "A 35-year-old male with HIV infection (CD4 count 180 cells/microL) presents with a 4-week history of cough, hemoptysis, evening fever, and night sweats. Sputum examination by Ziehl-Neelsen staining shows acid-fast bacilli. The sputum sample is inoculated onto an egg-based solid medium containing malachite green to inhibit contaminating oral flora. What is this standard solid culture medium?",
        "options": [
            "Loeffler serum slope",
            "Lowenstein-Jensen medium",
            "MacConkey agar",
            "Thayer-Martin agar"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nLowenstein-Jensen (LJ) medium is the classic, selective egg-based solid medium used worldwide for culturing Mycobacterium tuberculosis. Its ingredients include coagulated whole eggs (providing lipids for mycobacterial growth), mineral salts, asparagine, and glycerol (or pyruvate for M. bovis). Malachite green is added as a selective inhibitory agent to suppress the growth of non-mycobacterial gram-positive and gram-negative oral commensal flora. Colonies of M. tuberculosis typically take 2 to 6 weeks to appear and are rough, tough, and buff-colored (non-pigmented cream-colored colonies resembling breadcrumbs).\n\nOption Review:\n- Option A is incorrect because Loeffler serum slope is used for rapid enrichment of Corynebacterium diphtheriae.\n- Option B is correct because Lowenstein-Jensen (LJ) medium is the classic egg-based medium for Mycobacterium tuberculosis.\n- Option C is incorrect because MacConkey agar is a selective and differential medium for enteric gram-negative bacilli (distinguishing lactose fermenters).\n- Option D is incorrect because Thayer-Martin medium is a selective chocolate agar enriched with antibiotics used to isolate Neisseria gonorrhoeae.\n\nKey Takeaway: Lowenstein-Jensen (LJ) medium is an egg-based culture medium with malachite green used to isolate Mycobacterium tuberculosis, producing rough, tough, and buff colonies.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q066",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Mycology - Cryptococcus neoformans",
        "prompt": "A 40-year-old male with advanced AIDS presents with headache, lethargy, and neck stiffness. Lumbar puncture yields clear CSF with opening pressure of 280 mm H2O. An India ink wet mount preparation of the CSF reveals budding yeast cells surrounded by a wide, clear, unstained gelatinous halo against the dark background. Which pathogenic fungus is responsible for this opportunistic meningoencephalitis?",
        "options": [
            "Candida albicans",
            "Cryptococcus neoformans",
            "Histoplasma capsulatum",
            "Aspergillus fumigatus"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nCryptococcus neoformans is an encapsulated, opportunistic, basidiomycetous yeast found in soil enriched with pigeon droppings. It is the leading cause of fungal meningitis in immunocompromised patients, particularly those with HIV/AIDS (CD4 < 100/microL). Its major virulence factor is an extensive glucuronoxylomannan polysaccharide capsule that inhibits phagocytosis. On India ink negative staining, the large capsule repels the ink particles, appearing as a clear, prominent halo surrounding the spherical budding yeast. Culture on birdseed (Niger seed) agar produces brown-black colonies due to melanin synthesis via phenoloxidase.\n\nOption Review:\n- Option A is incorrect because Candida albicans produces pseudohyphae and germ tubes, and lacks a thick polysaccharide capsule.\n- Option B is correct because Cryptococcus neoformans is encapsulated and highlighted by negative staining with India ink.\n- Option C is incorrect because Histoplasma capsulatum is an intracellular dimorphic fungus found inside macrophages in bone marrow and reticuloendothelial system.\n- Option D is incorrect because Aspergillus fumigatus forms acute-angle (45-degree) branching septate hyphae.\n\nKey Takeaway: Cryptococcus neoformans is an encapsulated yeast visualized as a clear halo on India ink staining of CSF in AIDS patients.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Cryptococcus_neoformans_using_an_India_ink_stain_PHIL_3771_lores.jpg/640px-Cryptococcus_neoformans_using_an_India_ink_stain_PHIL_3771_lores.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q067",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Virology - Rabies Virus & Negri Bodies",
        "prompt": "A 10-year-old boy presents with agitation, hydrophobia, aerophobia, hypersalivation, and painful pharyngeal spasms 6 weeks after a stray dog bite on his hand. Despite intensive care, he succumbs to encephalitis. Postmortem histopathological examination of the brain reveals eosinophilic, sharply demarcated, round intracytoplasmic inclusions within the Purkinje cells of the cerebellum and pyramidal cells of the hippocampus. What are these diagnostic inclusions called?",
        "options": [
            "Cowdry A bodies",
            "Negri bodies",
            "Guarnieri bodies",
            "Councilman bodies"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nRabies is caused by the rabies virus (a bullet-shaped, negative-sense, single-stranded RNA Rhabdovirus). Following a bite from an infected mammal (dog, bat), the virus binds to nicotinic acetylcholine receptors at the neuromuscular junction and travels via retrograde axonal transport along peripheral sensory/motor nerves at 50 to 100 mm/day to reach the dorsal root ganglia and spinal cord, ascending rapidly to the central nervous system. The diagnostic microscopic hallmark is the Negri body: an eosinophilic, sharply defined, round or oval intracytoplasmic inclusion containing viral nucleocapsids, found in hippocampal pyramidal cells and cerebellar Purkinje cells.\n\nOption Review:\n- Option A is incorrect because Cowdry A bodies are eosinophilic intranuclear inclusions seen in Herpes simplex virus and Varicella zoster virus infections.\n- Option B is correct because Negri bodies are intracytoplasmic inclusions pathognomonic for rabies encephalitis.\n- Option C is incorrect because Guarnieri bodies are cytoplasmic inclusions found in smallpox (variola/vaccinia).\n- Option D is incorrect because Councilman bodies are apoptotic hepatocytes seen in acute yellow fever and viral hepatitis.\n\nKey Takeaway: Negri bodies are pathognomonic intracytoplasmic eosinophilic inclusions found in pyramidal cells of the hippocampus and Purkinje cells in rabies.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Negri_bodies.jpg/640px-Negri_bodies.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q068",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Bacteriology - Vibrio cholerae Culture Media",
        "prompt": "Following a flood, multiple villagers present with sudden onset of effortless, painless, voluminous watery diarrhea resembling 'rice water' with a fishy odor. Stool examination demonstrates darting motility on dark-field microscopy, which is inhibited by specific antiserum. Stool samples are plated onto Thiosulfate-Citrate-Bile Salts-Sucrose (TCBS) agar. What color colonies develop due to sucrose fermentation by Vibrio cholerae?",
        "options": [
            "Yellow colonies",
            "Green colonies",
            "Pink colonies",
            "Black colonies"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nVibrio cholerae is a comma-shaped, gram-negative, highly motile (single polar flagellum with 'darting' motility) facultative anaerobe that causes cholera through its cholera toxin (choleragen), which ribosylates Gs to activate adenylyl cyclase, leading to massive secretion of chloride and water. The selective and differential solid medium of choice is TCBS (Thiosulfate-Citrate-Bile Salts-Sucrose) agar. The high alkaline pH (8.6) and bile salts suppress intestinal commensals. V. cholerae actively ferments sucrose, dropping the pH and turning the bromothymol blue and thymol blue indicators from green to bright yellow.\n\nOption Review:\n- Option A is correct because Vibrio cholerae ferments sucrose on TCBS agar, producing characteristic large, bright yellow colonies.\n- Option B is incorrect because non-sucrose fermenting Vibrios (such as Vibrio parahaemolyticus and Vibrio vulnificus) produce green or blue-green colonies.\n- Option C is incorrect because pink colonies on MacConkey agar represent lactose fermenters (like E. coli).\n- Option D is incorrect because black colonies on Wilson-Blair or bismuth sulfite medium indicate Salmonella typhi (H2S production).\n\nKey Takeaway: Vibrio cholerae produces bright yellow colonies on TCBS agar due to sucrose fermentation at alkaline pH.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q069",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Parasitology - Plasmodium falciparum Identification",
        "prompt": "A 30-year-old traveler returning from sub-Saharan Africa presents with high-grade daily spikes of fever, severe headache, confusion, and dark urine ('blackwater fever'). Peripheral blood smear with Giemsa stain reveals multiple delicate ring forms within individual erythrocytes, applique (marginal) forms, and characteristic banana- or crescent-shaped gametocytes. Which species of Plasmodium is responsible?",
        "options": [
            "Plasmodium vivax",
            "Plasmodium falciparum",
            "Plasmodium malariae",
            "Plasmodium ovale"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nPlasmodium falciparum is the most virulent human malaria parasite, capable of infecting erythrocytes of all ages, leading to high parasitemia and severe complications (cerebral malaria, acute renal failure, blackwater fever due to massive intravascular hemolysis). Peripheral smear stained with Giemsa reveals pathognomonic diagnostic clues: 1) Delicate, tiny ring forms (trophozoites) with multiple rings inside a single RBC; 2) Applique/accole forms (rings adhering to the outer periphery of the RBC membrane); 3) Absence of intermediate schizonts in peripheral blood (due to sequestration of infected RBCs in deep capillary beds via PfEMP-1 binding to CD36/ICAM-1); 4) Crescent-shaped or banana-shaped gametocytes.\n\nOption Review:\n- Option A is incorrect because Plasmodium vivax infects reticulocytes, produces enlarged RBCs with Schuffner dots and rounded gametocytes.\n- Option B is correct because banana-shaped gametocytes, multiple delicate rings, and applique forms are diagnostic of Plasmodium falciparum.\n- Option C is incorrect because Plasmodium malariae infects older RBCs and produces characteristic 'band forms' and rosette schizonts.\n- Option D is incorrect because Plasmodium ovale causes oval-shaped RBCs with fimbriated edges and James dots.\n\nKey Takeaway: Crescent- or banana-shaped gametocytes and multiple delicate rings per erythrocyte on Giemsa stain are diagnostic of Plasmodium falciparum.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Plasmodium_falciparum_gametocyte_PHIL_5944_lores.jpg/640px-Plasmodium_falciparum_gametocyte_PHIL_5944_lores.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q070",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Bacteriology - Clostridium tetani Spores",
        "prompt": "A 45-year-old farmer steps on a rusted nail. Five days later, he presents with stiffness of the jaw, inability to open his mouth (trismus), and sustained facial spasm producing a characteristic grinning expression (risus sardonicus). Gram stain of anaerobic wound culture reveals gram-positive bacilli with terminal, round, bulging spores giving a 'drumstick' or tennis racket appearance. What neurotoxin is produced by this organism?",
        "options": [
            "Tetanospasmin",
            "Botulinum neurotoxin",
            "Diphtheria toxin",
            "Shiga toxin"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nClostridium tetani is an obligate anaerobic, spore-forming, gram-positive bacillus found in soil and animal feces. Under anaerobic conditions, its terminal round spores germinate into vegetative bacilli with a classic 'drumstick' morphology. C. tetani produces tetanospasmin, a potent AB metalloproteinase neurotoxin. The toxin is taken up at the neuromuscular junction and travels via retrograde intra-axonal transport to the spinal cord and brainstem, where its light chain cleaves synaptobrevin (VAMP), a SNARE protein. This prevents exocytosis of inhibitory neurotransmitters (GABA and glycine) from Renshaw interneurons, disinhibiting alpha motor neurons and resulting in painful, generalized spastic contractions.\n\nOption Review:\n- Option A is correct because tetanospasmin cleaves synaptobrevin to block GABA/glycine release, producing spastic tetanus.\n- Option B is incorrect because botulinum toxin also cleaves SNARE proteins, but acts at the peripheral neuromuscular junction to block acetylcholine release, causing flaccid paralysis.\n- Option C is incorrect because diphtheria toxin ribosylates EF-2, inhibiting host protein synthesis in the pharynx and myocardium.\n- Option D is incorrect because Shiga toxin cleaves 60S ribosomal rRNA, causing hemolytic uremic syndrome.\n\nKey Takeaway: Clostridium tetani produces 'drumstick' terminal spores and secretes tetanospasmin, which cleaves synaptobrevin to block inhibitory GABA and glycine release.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q071",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Virology - Hepatitis B Serological Markers",
        "prompt": "A 28-year-old nurse undergoes routine serological testing 6 months following an accidental needle-stick injury. Her results reveal: HBsAg negative, Anti-HBs positive (titer >100 mIU/mL), Anti-HBc total negative, and HBeAg negative. What is the correct clinical interpretation of this serological profile?",
        "options": [
            "Acute hepatitis B infection",
            "Natural recovery from past infection with immunity",
            "Immunity induced by hepatitis B vaccination",
            "Chronic hepatitis B carrier state"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nThe hepatitis B surface antigen (HBsAg) is the first marker to appear during acute infection and indicates active viral presence. The hepatitis B core antigen (HBcAg) is an internal viral protein; antibodies against it (anti-HBc IgM in acute infection, anti-HBc IgG in past or chronic infection) develop only when the immune system encounters the whole replicating virus (natural infection). In contrast, the recombinant hepatitis B vaccine contains solely purified recombinant HBsAg particles. Consequently, vaccinated individuals produce protective anti-HBs antibodies, but remain strictly negative for anti-HBc.\n\nOption Review:\n- Option A is incorrect because acute infection shows positive HBsAg and positive IgM anti-HBc.\n- Option B is incorrect because natural recovery from infection confers both anti-HBs and anti-HBc IgG positivity.\n- Option C is correct because isolated anti-HBs positivity with negative anti-HBc indicates vaccine-induced immunity.\n- Option D is incorrect because chronic carrier status is defined by persistence of HBsAg for >6 months.\n\nKey Takeaway: Isolated anti-HBs positivity in the absence of anti-HBc confirms immunity resulting from hepatitis B vaccination.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q072",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Bacteriology - Staphylococcus aureus vs S. epidermidis",
        "prompt": "A 70-year-old male with an indwelling prosthetic hip joint develops low-grade joint pain and swelling. Blood cultures grow gram-positive cocci in clusters that are catalase-positive. When inoculated onto rabbit plasma, the organism fails to produce a clot (coagulase-negative). On Mueller-Hinton agar, the isolate is susceptible to novobiocin (zone of inhibition >16 mm). What is the most likely pathogen?",
        "options": [
            "Staphylococcus aureus",
            "Staphylococcus epidermidis",
            "Staphylococcus saprophyticus",
            "Streptococcus pyogenes"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nGram-positive cocci in clusters are staphylococci (catalase-positive, distinguishing them from streptococci). Staphylococci are classified into coagulase-positive (Staphylococcus aureus) and coagulase-negative staphylococci (CoNS). The two medically important CoNS species are differentiated by novobiocin disk susceptibility: Staphylococcus epidermidis is novobiocin-sensitive, whereas Staphylococcus saprophyticus (a cause of UTI in sexually active young females) is novobiocin-resistant (mnemonic: NO Staph: Novobiocin-resistant = Saprophyticus, Sensitive = Epidermidis). S. epidermidis produces a robust polysaccharide slime biofilm that adheres tenaciously to prosthetic hardware.\n\nOption Review:\n- Option A is incorrect because Staphylococcus aureus is coagulase-positive.\n- Option B is correct because Staphylococcus epidermidis is coagulase-negative and novobiocin-sensitive.\n- Option C is incorrect because Staphylococcus saprophyticus is coagulase-negative but novobiocin-resistant.\n- Option D is incorrect because Streptococcus pyogenes is catalase-negative and forms chains.\n\nKey Takeaway: Staphylococcus epidermidis is a coagulase-negative, novobiocin-sensitive staphylococcus that causes biofilm-mediated prosthetic device infections.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q073",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Parasitology - Entamoeba histolytica",
        "prompt": "A 32-year-old male presents with right upper quadrant pain, low-grade fever, and a history of dysentery 3 weeks ago. Abdominal ultrasound demonstrates a solitary hypoechoic cyst in the right lobe of the liver. Aspiration reveals thick, odorless, reddish-brown fluid resembling 'anchovy sauce'. Stool microscopy reveals cysts with four nuclei and chromatoid bars with rounded ends. Which protozoan parasite is the causative agent?",
        "options": [
            "Giardia lamblia",
            "Entamoeba histolytica",
            "Echinococcus granulosus",
            "Balantidium coli"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nEntamoeba histolytica is an intestinal protozoan transmitted via ingestion of mature quadrinucleate cysts in contaminated food or water. Trophozoites invade the colonic mucosa, creating characteristic 'flask-shaped' ulcers and amebic dysentery. Trophozoites can enter the portal circulation and travel to the liver, where they cause liquefactive necrosis of hepatocytes, forming an amebic liver abscess (most commonly solitary in the right lobe). The aspirated fluid is sterile, thick, and chocolate-brown/reddish ('anchovy sauce' or 'chocolate sauce' pus). Trophozoites in stools uniquely show ingested erythrocytes (erythrophagocytosis).\n\nOption Review:\n- Option A is incorrect because Giardia lamblia infects the duodenum, causing non-invasive malabsorptive diarrhea with foul-smelling, fatty stools, without liver abscesses.\n- Option B is correct because Entamoeba histolytica produces amebic liver abscess with characteristic 'anchovy sauce' aspirate.\n- Option C is incorrect because Echinococcus granulosus forms hydatid cysts with 'hydatid sand' containing hooklets, filled with clear fluid that can cause anaphylaxis if punctured.\n- Option D is incorrect because Balantidium coli is a ciliated protozoan causing colitis but not typical liver abscesses.\n\nKey Takeaway: Amebic liver abscess caused by Entamoeba histolytica produces sterile, reddish-brown 'anchovy sauce' pus with trophozoites demonstrating erythrophagocytosis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q074",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Bacteriology - Corynebacterium diphtheriae Media & Elek Test",
        "prompt": "A 6-year-old unimmunized child presents with sore throat, cervical lymphadenopathy ('bull neck'), and a thick, leathery, dirty-gray pseudomembrane over the tonsils and posterior pharynx that bleeds on attempts to dislodge it. Swabs are plated on selective potassium tellurite medium, yielding gunmetal-black colonies. Albert staining demonstrates metachromatic granules. Which in vitro test is performed to confirm the production of diphtheria exotoxin?",
        "options": [
            "Elek gel precipitation test",
            "Schick test",
            "Widal agglutination test",
            "Weil-Felix test"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nCorynebacterium diphtheriae is a pleomorphic, club-shaped, non-spore-forming gram-positive rod arranged in angular 'V' or 'L' formations (Chinese letter pattern). On Albert's stain, metachromatic (volutin/polyphosphate) granules stain violet-black against a green cytoplasm. Selective culture on blood tellurite agar (McLeod's medium) or Tinsdale agar yields characteristic gunmetal-black or gray colonies due to tellurite reduction. Because non-toxigenic strains also colonize the throat, pathogenicity requires confirmation of diphtheria exotoxin production (encoded by the tox gene of a lysogenic beta-corynephage). The standard in vitro immunodiffusion method is the Elek gel precipitation test, where an antitoxin-impregnated filter paper strip produces precipitin lines with toxigenic colonies.\n\nOption Review:\n- Option A is correct because the Elek test is the definitive in vitro gel precipitation assay used to demonstrate diphtheria exotoxigenicity.\n- Option B is incorrect because the Schick test is an obsolete in vivo intradermal test to determine susceptibility/immunity to diphtheria, not an in vitro diagnostic toxin test.\n- Option C is incorrect because the Widal test detects agglutinating antibodies against Salmonella antigens.\n- Option D is incorrect because the Weil-Felix test detects antibodies to Rickettsiae using Proteus antigens.\n\nKey Takeaway: Diphtheria toxin production is confirmed in vitro by the Elek gel precipitation test; organism produces metachromatic granules and black colonies on tellurite agar.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q075",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Bacteriology - Streptococcus pneumoniae vs S. viridans",
        "prompt": "A 65-year-old male with chronic obstructive pulmonary disease presents with high fever, pleuritic chest pain, and 'rusty' sputum. Sputum culture on sheep blood agar produces alpha-hemolytic colonies with a central indentation ('draughtsman' or carrom-coin appearance). The isolate is optochin-sensitive (zone diameter >14 mm) and soluble in 10% sodium deoxycholate (bile-soluble). Which organism is the most common cause of community-acquired pneumonia in adults?",
        "options": [
            "Streptococcus pneumoniae",
            "Streptococcus viridans",
            "Streptococcus pyogenes",
            "Enterococcus faecalis"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nStreptococcus pneumoniae (pneumococcus) is a lancet-shaped, gram-positive diplococcus with a polysaccharide capsule that serves as its primary virulence factor. On blood agar, it produces partial (green) alpha-hemolysis with autolysis creating 'draughtsman' colonies. It is definitively differentiated from oral Viridans streptococci by two laboratory tests: 1) Optochin (ethylhydrocupreine) disk sensitivity: S. pneumoniae is sensitive, while Viridans group streptococci are resistant; 2) Bile solubility test: S. pneumoniae lyses in 10% sodium deoxycholate (bile-soluble), whereas Viridans streptococci remain insoluble and turbid. Mnemonic: OVRPS (Optochin: Viridans Resistant, Pneumococci Sensitive).\n\nOption Review:\n- Option A is correct because Streptococcus pneumoniae is alpha-hemolytic, optochin-sensitive, and bile-soluble.\n- Option B is incorrect because Streptococcus viridans is alpha-hemolytic but optochin-resistant and bile-insoluble.\n- Option C is incorrect because Streptococcus pyogenes (Group A Strep) produces clear beta-hemolysis and is bacitracin-sensitive.\n- Option D is incorrect because Enterococcus faecalis is gamma-hemolytic, grows in 6.5% NaCl, and hydrolyzes esculin.\n\nKey Takeaway: Streptococcus pneumoniae is distinguished from Viridans streptococci by its sensitivity to optochin and solubility in bile salts.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q076",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Immunology - Type I Hypersensitivity",
        "prompt": "Within 5 minutes of receiving an intramuscular injection of penicillin, a 30-year-old male develops generalized urticaria, wheezing, angioedema of the lips, and severe hypotension (blood pressure 60/30 mmHg). This life-threatening anaphylactic reaction is mediated by cross-linking of which class of antibodies bound to high-affinity Fc receptors on tissue mast cells and basophils?",
        "options": [
            "Immunoglobulin M",
            "Immunoglobulin G",
            "Immunoglobulin E",
            "Immunoglobulin A"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nSystemic anaphylaxis is the prototypical Type I (immediate) hypersensitivity reaction. During the sensitization phase, allergen exposure triggers helper T cells (Th2) to secrete IL-4 and IL-13, driving B-cell class-switching to Immunoglobulin E (IgE). Circulating IgE binds with high affinity to Fc-epsilon-RI receptors on tissue mast cells and circulating basophils. Upon re-exposure, the bivalent or multivalent allergen binds and cross-links adjacent surface-bound IgE molecules. This induces explosive degranulation, releasing preformed mediators (histamine, tryptase) and newly synthesized lipid mediators (leukotrienes C4, D4, E4, and PAF), causing profound systemic vasodilation, capillary leakage, and bronchoconstriction.\n\nOption Review:\n- Option A is incorrect because IgM is the pentameric antibody produced in primary immune responses, mediating agglutination and complement activation.\n- Option B is incorrect because IgG mediates Type II (cytotoxic) and Type III (immune complex) hypersensitivity.\n- Option C is correct because IgE antibodies bound to mast cell Fc-epsilon-RI receptors mediate immediate Type I hypersensitivity and anaphylaxis.\n- Option D is incorrect because IgA is the dimeric secretory immunoglobulin protecting mucosal surfaces.\n\nKey Takeaway: Type I hypersensitivity (anaphylaxis) is mediated by allergen cross-linking of specific IgE antibodies bound to Fc-epsilon-RI receptors on mast cells.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q077",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "topic": "Virology - Human Immunodeficiency Virus Diagnostic Algorithm",
        "prompt": "A 35-year-old high-risk individual undergoes HIV screening. Under current diagnostic guidelines, the recommended initial screening assay is a fourth-generation combination enzyme immunoassay. What two targets are simultaneously detected by this fourth-generation assay to narrow the diagnostic window period?",
        "options": [
            "HIV-1/2 antibodies and p24 viral capsid antigen",
            "HIV-1 RNA and reverse transcriptase enzyme",
            "gp120 envelope glycoprotein and CD4 receptors",
            "gp41 transmembrane protein and p17 matrix protein"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nModern HIV testing algorithms use a 4th-generation combination immunoassay as the primary initial screening test. This assay simultaneously detects both anti-HIV-1 and anti-HIV-2 IgM and IgG antibodies, as well as the uncomplexed HIV-1 p24 capsid core antigen. Because the viral p24 protein appears in plasma approximately 10 to 14 days following infection (prior to seroconversion, when antibodies only appear after 3 to 4 weeks), fourth-generation assays dramatically narrow the diagnostic window period, enabling early detection during the acute infection phase.\n\nOption Review:\n- Option A is correct because 4th-generation assays detect both HIV-1/2 antibodies and the viral p24 antigen.\n- Option B is incorrect because HIV RNA is detected by nucleic acid testing (NAT/PCR), which is used as a confirmatory or acute discordance test.\n- Option C is incorrect because gp120 is the outer envelope protein and CD4 is the host cell receptor.\n- Option D is incorrect because gp41 and p17 are not the dual targets utilized in 4th-generation combo screening assays.\n\nKey Takeaway: Fourth-generation HIV combination screening assays simultaneously detect HIV-1/2 antibodies and the p24 capsid antigen, shortening the diagnostic window.",
        "imageUrls": []
    },

    # ==========================================
    # PHARMACOLOGY (13 Questions: Q078 - Q090)
    # ==========================================
    {
        "id": "fmge-gt1-q078",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Autonomic Pharmacology - Organophosphate Antidotes",
        "prompt": "A 28-year-old agricultural worker is brought to the emergency department after accidentally spraying an insecticide. He presents with pin-point pupils, profuse salivation, wheezing with bilateral coarse crackles, diarrhea, and bradycardia. Atropine is administered immediately to reverse muscarinic symptoms. Which antidote must be administered simultaneously to reactivate phosphorylated acetylcholinesterase at nicotinic neuromuscular junctions?",
        "options": [
            "Physostigmine",
            "Pralidoxime",
            "Neostigmine",
            "N-acetylcysteine"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nOrganophosphate insecticides irreversibly inhibit acetylcholinesterase (AChE) by phosphorylating the serine hydroxyl group at the enzyme's esteratic site. This causes massive acetylcholine accumulation at muscarinic receptors (producing DUMBBELLS symptoms: Diarrhea, Urination, Miosis, Bradycardia, Bronchospasm/Bronchorrhea, Emesis, Lacrimation, Salivation) and nicotinic receptors (producing muscle fasciculations followed by flaccid muscle paralysis). Atropine blocks muscarinic receptors, reversing life-threatening bronchorrhea and bradycardia, but has zero effect on nicotinic receptors. Pralidoxime (2-PAM) is an oxime that nucleophilically attacks the phosphate group, dephosphorylating and reactivating acetylcholinesterase, thereby restoring muscle strength before 'aging' (covalent chemical stabilization) occurs.\n\nOption Review:\n- Option A is incorrect because physostigmine is a tertiary carbamate AChE inhibitor used for anticholinergic toxicity (atropine overdose); giving it in organophosphate poisoning would be fatal.\n- Option B is correct because pralidoxime reactivates phosphorylated acetylcholinesterase, reversing nicotinic muscle weakness.\n- Option C is incorrect because neostigmine is an AChE inhibitor used in myasthenia gravis.\n- Option D is incorrect because N-acetylcysteine is the specific antidote for acetaminophen (paracetamol) toxicity.\n\nKey Takeaway: Pralidoxime (2-PAM) reactivates phosphorylated acetylcholinesterase at nicotinic sites in organophosphate toxicity, complementing atropine's muscarinic blockade.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q079",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Central Nervous System - Antiepileptic Adverse Effects",
        "prompt": "An 18-year-old female with focal-to-bilateral tonic-clonic seizures has been treated with an antiepileptic drug for 8 months. During a routine dental visit, she is found to have marked fibrous overgrowth of her gingival margins covering the crowns of her teeth, along with coarse facial features and hirsutism. Which antiepileptic agent is most characteristically associated with gingival hyperplasia?",
        "options": [
            "Sodium valproate",
            "Phenytoin",
            "Carbamazepine",
            "Levetiracetam"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nPhenytoin is a classic first-generation antiepileptic drug that prolongs the inactivated state of voltage-gated neuronal Na+ channels. It exhibits zero-order (saturation) elimination kinetics at therapeutic concentrations. Characteristic chronic adverse drug reactions include: 1) Gingival hyperplasia (in ~50% of patients, caused by upregulation of platelet-derived growth factor stimulating gingival fibroblast proliferation); 2) Hirsutism and coarsening of facial features; 3) Peripheral neuropathy and cerebellar ataxia (nystagmus); 4) Megaloblastic anemia (folate antagonism); 5) Fetal hydantoin syndrome (teratogenicity); 6) Osteomalacia (induction of vitamin D catabolism).\n\nOption Review:\n- Option A is incorrect because sodium valproate causes hepatotoxicity, pancreatitis, weight gain, alopecia, and neural tube defects.\n- Option B is correct because phenytoin is classic for gingival hyperplasia, hirsutism, and zero-order elimination.\n- Option C is incorrect because carbamazepine is associated with bone marrow suppression (agranulocytosis/aplastic anemia), SIADH (hyponatremia), and Stevens-Johnson syndrome.\n- Option D is incorrect because levetiracetam binds SV2A and is associated with neuropsychiatric adverse effects (irritability, mood changes).\n\nKey Takeaway: Phenytoin characteristically causes gingival hyperplasia, hirsutism, cerebellar ataxia, and operates under zero-order elimination kinetics.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q080",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Cardiovascular Pharmacology - Malignant Hyperthermia Antidote",
        "prompt": "During induction of general anesthesia for an emergency laparotomy, a 30-year-old male receives succinylcholine and sevoflurane. Within 10 minutes, he develops severe masseter muscle spasm, generalized rigidity, hypercapnia refractory to hyperventilation, and body temperature rising to 41.0°C. Which specific antidote must be administered intravenously to treat malignant hyperthermia?",
        "options": [
            "Dantrolene sodium",
            "Neostigmine methylsulfate",
            "Flumazenil",
            "Naloxone hydrochloride"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nMalignant hyperthermia is a life-threatening, autosomal dominant pharmacogenetic hypermetabolic crisis triggered by volatile inhalational anesthetics (halothane, isoflurane, sevoflurane) or the depolarizing neuromuscular blocker succinylcholine. In susceptible individuals harboring mutations in the ryanodine receptor (RYR1) or CACNA1S genes, exposure triggers uncontrolled release of Ca2+ from the sarcoplasmic reticulum into the myoplasm. Massive calcium activates ATPases and actomyosin cross-bridges, producing sustained muscle rigidity, profound hyperthermia, metabolic acidosis, rhabdomyolysis, and hyperkalemia. The specific, life-saving antidote is dantrolene sodium, which binds directly to RyR1 channels and blocks calcium release.\n\nOption Review:\n- Option A is correct because dantrolene directly blocks the sarcoplasmic ryanodine receptor (RyR1), shutting down calcium efflux.\n- Option B is incorrect because neostigmine inhibits acetylcholinesterase and would worsen depolarizing neuromuscular blockade and fasciculations.\n- Option C is incorrect because flumazenil is a benzodiazepine antagonist.\n- Option D is incorrect because naloxone is an opioid receptor antagonist.\n\nKey Takeaway: Dantrolene sodium is the specific antidote for malignant hyperthermia, acting by blocking RyR1 channels on the sarcoplasmic reticulum.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q081",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Cardiovascular Pharmacology - Adenosine for PSVT",
        "prompt": "A 24-year-old female presents to the emergency department with sudden onset of regular palpitations and lightheadedness. The ECG displays narrow-complex tachycardia at a rate of 190 bpm with retrogradely conducted P waves, consistent with paroxysmal supraventricular tachycardia (PSVT). Vagal maneuvers fail to terminate the arrhythmia. Which drug is the first-line intravenous agent of choice for rapid conversion to sinus rhythm?",
        "options": [
            "Adenosine",
            "Amiodarone",
            "Lidocaine",
            "Digoxin"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nParoxysmal supraventricular tachycardia (PSVT), commonly due to atrioventricular nodal reentrant tachycardia (AVNRT), involves a micro-reentry circuit utilizing the AV node. In hemodynamically stable patients who fail vagal maneuvers (carotid sinus massage, Valsalva), intravenous adenosine is the first-line drug of choice. Adenosine binds to A1 purinergic receptors in the AV node, activating inhibitory G-proteins that stimulate inward rectifier K+ currents and inhibit L-type Ca2+ currents. This produces transient, profound hyperpolarization and complete AV nodal conduction block, breaking the reentry circuit. Because its plasma half-life is <10 seconds, it must be given as a rapid IV bolus followed by an immediate saline flush.\n\nOption Review:\n- Option A is correct because adenosine is the drug of choice for rapid acute termination of stable narrow-complex PSVT.\n- Option B is incorrect because amiodarone is a broad-spectrum class III antiarrhythmic used primarily for ventricular arrhythmias and atrial fibrillation.\n- Option C is incorrect because lidocaine (Class Ib) acts selectively on ischemic ventricular myocardium, with no efficacy in AV nodal supraventricular arrhythmias.\n- Option D is incorrect because digoxin has an onset of action of hours and is not used for acute emergency cardioversion of PSVT.\n\nKey Takeaway: Intravenous adenosine is the first-line pharmacologic drug of choice for terminating acute paroxysmal supraventricular tachycardia (PSVT).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q082",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Cardiovascular Pharmacology - Digoxin Toxicity & Mechanism",
        "prompt": "A 72-year-old female with congestive heart failure and atrial fibrillation on chronic digoxin therapy presents with nausea, vomiting, yellow-tinted blurred vision (xanthopsia), and palpitations. ECG reveals atrial tachycardia with 2:1 AV block. Which cellular transport protein is directly inhibited by digoxin to increase cardiac inotropy?",
        "options": [
            "Sodium-potassium ATPase",
            "Sarcoplasmic reticulum calcium ATPase",
            "Sodium-calcium exchanger",
            "L-type voltage-gated calcium channel"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nDigoxin increases myocardial contractility by directly and reversibly inhibiting the extracellular potassium-binding site of the cardiac sarcolemmal Na+/K+-ATPase pump. Inhibition of this pump increases intracellular Na+ concentration. High intracellular Na+ reduces the concentration gradient driving the sodium-calcium exchanger (NCX), decreasing the extrusion of Ca2+ out of the myocyte. The resulting elevation in cytosolic Ca2+ is taken up into the sarcoplasmic reticulum by SERCA, yielding increased calcium release during subsequent action potentials, producing a positive inotropic effect. Toxicity manifests as GI upset, visual halos/xanthopsia, and arrhythmias (PVCs, junctional tachycardia, bidirectional VT).\n\nOption Review:\n- Option A is correct because digoxin directly binds and inhibits the myocardial Na+/K+-ATPase.\n- Option B is incorrect because SERCA is responsible for sequestering calcium into the sarcoplasmic reticulum during diastole.\n- Option C is incorrect because the Na+/Ca2+ exchanger (NCX) is secondarily slowed due to reduced Na+ gradients, not directly inhibited by digoxin.\n- Option D is incorrect because L-type calcium channels are blocked by dihydropyridines and non-dihydropyridines (verapamil/diltiazem).\n\nKey Takeaway: Digoxin directly inhibits the sarcolemmal Na+/K+-ATPase, secondarily increasing intracellular calcium concentration to enhance myocardial inotropy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q083",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Antimicrobial Pharmacology - Red Man Syndrome",
        "prompt": "A 40-year-old hospitalized patient with severe MRSA bacteremia receives an intravenous infusion of vancomycin. Within 10 minutes of rapid infusion, he develops intense erythema, flushing, and pruritus over his face, neck, and upper torso, accompanied by mild hypotension. What is the pharmacological mechanism responsible for this adverse reaction?",
        "options": [
            "Direct non-IgE-mediated histamine release from mast cells",
            "IgE-mediated Type I anaphylactic degranulation",
            "Circulating immune complex deposition in dermal capillaries",
            "Direct competitive antagonism of alpha-1 adrenergic receptors"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\n'Red Man syndrome' (vancomycin infusion reaction) is an adverse reaction caused by the rapid intravenous administration of vancomycin. It is an anaphylactoid (pseudoallergic) reaction resulting from the direct, non-immunological stimulation of mast cells and basophils by the glycopeptide antibiotic, causing massive, rate-dependent release of histamine. It is NOT mediated by preformed IgE antibodies. Symptoms include intense flushing, erythematous rash on the face and neck, and hypotension. It is prevented or managed by slowing the infusion rate (infusing over at least 60 to 120 minutes) and premedicating with antihistamines.\n\nOption Review:\n- Option A is correct because Red Man syndrome is caused by rate-dependent direct non-IgE-mediated histamine release.\n- Option B is incorrect because true IgE-mediated anaphylaxis is independent of infusion speed and presents with bronchospasm and hives across the entire body.\n- Option C is incorrect because immune complex deposition mediates Type III hypersensitivity (serum sickness), which takes days to develop.\n- Option D is incorrect because vancomycin has no adrenergic receptor blocking activity.\n\nKey Takeaway: Vancomycin-induced Red Man syndrome is a rate-dependent pseudoallergic reaction caused by direct, non-IgE-mediated mast cell histamine release.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q084",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Toxicology - Acetaminophen Toxicity & Antidote",
        "prompt": "An 18-year-old female is brought to the emergency department 6 hours after ingesting 25 tablets of acetaminophen (500 mg each) in a suicide attempt. Hepatic toxicity from acetaminophen overdose results from the saturation of normal glucuronidation and sulfation pathways, shunting the drug into cytochrome P450 to produce a toxic metabolite. What antidote acts as a glutathione substitute to detoxify this reactive intermediate?",
        "options": [
            "N-acetylcysteine",
            "Deferoxamine",
            "Dimercaprol",
            "Methylene blue"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAt therapeutic doses, >90% of acetaminophen (paracetamol) is metabolized by hepatic glucuronidation and sulfation into non-toxic conjugates. A minor fraction (~5%) is oxidized by CYP2E1 into N-acetyl-p-benzoquinone imine (NAPQI), a highly reactive, toxic electrophilic intermediate that is rapidly conjugated with hepatic glutathione (GSH) to form harmless mercapturic acid. In overdose, sulfation and glucuronidation are saturated, and hepatic glutathione stores are depleted by >70%. Unbound NAPQI covalently binds to cysteine groups on hepatic proteins, causing centrilobular (Zone 3) hepatic necrosis. Intravenous or oral N-acetylcysteine (NAC) restores hepatic glutathione reserves and acts as a direct glutathione surrogate to bind NAPQI.\n\nOption Review:\n- Option A is correct because N-acetylcysteine (NAC) regenerates glutathione to detoxify the reactive metabolite NAPQI.\n- Option B is incorrect because deferoxamine is a specific chelator for acute iron poisoning.\n- Option C is incorrect because dimercaprol (BAL) is a heavy metal chelating agent for arsenic, gold, and mercury poisoning.\n- Option D is incorrect because methylene blue is the antidote for methemoglobinemia.\n\nKey Takeaway: N-acetylcysteine treats acetaminophen overdose by replenishing hepatic glutathione stores to neutralize the toxic metabolite NAPQI.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q085",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Antimicrobial Pharmacology - Aminoglycoside Toxicity",
        "prompt": "A 58-year-old male with Pseudomonas aeruginosa sepsis is treated with intravenous gentamicin and piperacillin-tazobactam. On day 6 of therapy, routine laboratory testing reveals a rise in serum creatinine from 0.9 mg/dL to 2.4 mg/dL. He also complains of high-frequency hearing loss and persistent tinnitus. Which dual toxicities are classic for aminoglycoside antibiotics?",
        "options": [
            "Nephrotoxicity and ototoxicity",
            "Hepatotoxicity and peripheral neuropathy",
            "Cardiotoxicity and pulmonary fibrosis",
            "Bone marrow suppression and pancreatitis"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAminoglycosides (gentamicin, tobramycin, amikacin, streptomycin) are polycationic bactericidal antibiotics that bind the 30S ribosomal subunit to cause misreading of mRNA. Because of their polar structure, they are eliminated entirely unchanged by glomerular filtration. Aminoglycosides accumulate in renal proximal tubular cells via endocytosis mediated by megalin, generating reactive oxygen species and causing acute tubular necrosis (non-oliguric nephrotoxicity). They also accumulate in the perilymph and endolymph of the inner ear, destroying auditory hair cells in the organ of Corti and vestibular hair cells, resulting in irreversible sensorineural hearing loss, tinnitus, and ataxia (ototoxicity).\n\nOption Review:\n- Option A is correct because aminoglycosides are notoriously nephrotoxic (acute tubular necrosis) and ototoxic (cochlear/vestibular damage).\n- Option B is incorrect because hepatotoxicity is classic for isoniazid, pyrazinamide, and acetaminophen.\n- Option C is incorrect because cardiotoxicity is associated with anthracyclines (doxorubicin) and pulmonary fibrosis with bleomycin/amiodarone.\n- Option D is incorrect because bone marrow suppression is associated with chloramphenicol, linezolid, and ganciclovir.\n\nKey Takeaway: Aminoglycosides produce dose- and duration-dependent nephrotoxicity (reversible ATN) and ototoxicity (irreversible sensorineural hearing loss).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q086",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Cardiovascular Pharmacology - ACE Inhibitor Adverse Effects",
        "prompt": "A 54-year-old male with hypertension and type 2 diabetes mellitus is started on enalapril. Three weeks later, he presents complaining of a dry, hacking, non-productive nocturnal cough that has disrupted his sleep. Physical examination and chest radiograph are normal. The accumulation of which peptide mediator in the pulmonary tract is responsible for ACE inhibitor-induced cough?",
        "options": [
            "Bradykinin",
            "Angiotensin II",
            "Endothelin-1",
            "Atrial natriuretic peptide"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAngiotensin-Converting Enzyme (ACE, also known as kininase II) has dual physiological substrates: it converts angiotensin I to vasoconstrictor angiotensin II, and it concurrently degrades bradykinin and substance P into inactive peptide fragments. When an ACE inhibitor (captopril, enalapril, ramipril) is administered, bradykinin degradation is blocked. Elevated levels of bradykinin and substance P accumulate in the upper respiratory tract and lungs, where they sensitize sensory unmyelinated C-fibers, triggering bronchoconstriction and a persistent, dry, hacking cough in 5% to 20% of patients. Substituting with an Angiotensin Receptor Blocker (ARB, e.g., losartan) resolves the cough because ARBs do not inhibit kininase II.\n\nOption Review:\n- Option A is correct because accumulation of bradykinin and substance P due to kininase II inhibition causes ACE inhibitor-induced dry cough and angioedema.\n- Option B is incorrect because angiotensin II levels are reduced by ACE inhibitors.\n- Option C is incorrect because endothelin-1 is a vasoconstrictor peptide not degraded by ACE.\n- Option D is incorrect because atrial natriuretic peptide (ANP) is degraded by neprilysin, not ACE.\n\nKey Takeaway: ACE inhibitor-induced dry cough is mediated by the accumulation of bradykinin and substance P resulting from the inhibition of kininase II.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q087",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Endocrine Pharmacology - Metformin Lactic Acidosis",
        "prompt": "A 62-year-old male with type 2 diabetes mellitus is scheduled for an urgent contrast-enhanced CT scan of the abdomen. His baseline serum creatinine is 1.8 mg/dL (eGFR 38 mL/min/1.73 m2). The radiologist instructs the team to withhold his metformin prior to contrast administration. What rare but potentially fatal metabolic complication of metformin is exacerbated by contrast-induced acute kidney injury?",
        "options": [
            "Lactic acidosis",
            "Diabetic ketoacidosis",
            "Hypoglycemic coma",
            "Hyperosmolar hyperglycemic state"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nMetformin is a biguanide that serves as first-line therapy for type 2 diabetes. Its primary mechanism of action is activation of AMP-activated protein kinase (AMPK), which suppresses hepatic gluconeogenesis and improves peripheral insulin sensitivity. In mitochondria, metformin inhibits mitochondrial complex I, reducing ATP synthesis and decreasing hepatic pyruvate carboxylase activity. Pyruvate is redirected into lactate via lactate dehydrogenase. Metformin is excreted unchanged by the kidneys. If renal impairment occurs (e.g., from iodinated contrast-induced nephropathy), metformin accumulates, producing severe, life-threatening lactic acidosis. Consequently, metformin is contraindicated in advanced renal disease and withheld during iodinated contrast administration.\n\nOption Review:\n- Option A is correct because metformin accumulation in the setting of renal failure causes life-threatening lactic acidosis.\n- Option B is incorrect because diabetic ketoacidosis occurs in type 1 diabetes or SGLT2 inhibitor use (euglycemic DKA).\n- Option C is incorrect because metformin does not stimulate insulin secretion and has a very low intrinsic risk of hypoglycemia.\n- Option D is incorrect because hyperosmolar hyperglycemic state is triggered by severe hyperglycemia and dehydration, not by metformin.\n\nKey Takeaway: Metformin inhibits mitochondrial complex I and can cause fatal lactic acidosis if it accumulates during renal failure or contrast nephropathy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q088",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Antimicrobial Pharmacology - Gray Baby Syndrome",
        "prompt": "A 4-day-old preterm infant receives high-dose intravenous chloramphenicol for suspected neonatal meningitis. On the third day of treatment, the neonate becomes lethargic, vomits, exhibits hypothermia, ashen-gray skin discoloration, abdominal distension, and progressive cardiovascular collapse. This 'gray baby syndrome' occurs due to the deficiency of which neonatal hepatic enzyme?",
        "options": [
            "UDP-glucuronosyltransferase",
            "Cytochrome P450 3A4",
            "Glutathione S-transferase",
            "Alcohol dehydrogenase"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nChloramphenicol is a broad-spectrum bacteriostatic antibiotic that binds reversibly to the 50S ribosomal subunit, inhibiting peptidyl transferase. Chloramphenicol is normally cleared by hepatic glucuronidation to an inactive metabolite. Neonates, especially premature infants, possess two critical developmental deficiencies: 1) Immature hepatic UDP-glucuronosyltransferase (UGT) activity; 2) Low renal glomerular filtration rate. When exposed to standard or high doses of chloramphenicol, the unmetabolized active drug accumulates to toxic levels, disrupting mitochondrial protein synthesis and uncoupling oxidative phosphorylation, precipitating 'gray baby syndrome' characterized by ashen cyanosis, hypothermia, flaccidity, and fatal circulatory collapse.\n\nOption Review:\n- Option A is correct because deficiency of neonatal hepatic UDP-glucuronosyltransferase leads to toxic chloramphenicol accumulation and gray baby syndrome.\n- Option B is incorrect because CYP3A4 is a phase I oxidative enzyme not primarily responsible for chloramphenicol clearance.\n- Option C is incorrect because glutathione S-transferase conjugates acetaminophen metabolites, not chloramphenicol.\n- Option D is incorrect because alcohol dehydrogenase metabolizes ethanol and methanol.\n\nKey Takeaway: Chloramphenicol causes gray baby syndrome in neonates due to immature hepatic UDP-glucuronosyltransferase activity and low renal clearance.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q089",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Anticoagulants - Heparin-Induced Thrombocytopenia",
        "prompt": "A 56-year-old male receives unfractionated heparin following orthopedic surgery. On postoperative day 7, his platelet count drops precipitously from 240,000/microL to 75,000/microL, and he develops acute deep vein thrombosis in his left calf. What is the immunological mechanism of heparin-induced thrombocytopenia (HIT Type II)?",
        "options": [
            "Antibodies against platelet factor 4-heparin complexes activating platelets",
            "Direct toxic megakaryocyte suppression by unfractionated heparin",
            "IgE-mediated mast cell degranulation triggering splenic sequestration",
            "Autoantibodies against the platelet glycoprotein IIb/IIIa receptor"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nHeparin-Induced Thrombocytopenia (HIT Type II) is a prothrombotic immune-mediated adverse drug reaction that occurs 5 to 10 days following heparin exposure. Polyanionic heparin binds to positively charged platelet factor 4 (PF4) released by platelets, forming an immunogenic macromolecular complex. Patients generate IgG autoantibodies directed against this PF4-heparin complex. The Fc domains of these IgG antibodies bind to Fc-gamma-RIIa receptors on adjacent platelets, triggering massive, widespread platelet activation and consumption (thrombocytopenia). Platelet activation releases procoagulant microparticles that cause catastrophic venous and arterial thrombosis ('white clot syndrome'). Heparin must be stopped immediately and replaced with a direct thrombin inhibitor (argatroban).\n\nOption Review:\n- Option A is correct because HIT Type II is caused by IgG antibodies against PF4-heparin complexes that bind Fc-gamma-RIIa receptors to activate platelets.\n- Option B is incorrect because direct non-immune benign platelet aggregation causes HIT Type I (mild, early drop in platelets without thrombosis).\n- Option C is incorrect because IgE is not involved in HIT.\n- Option D is incorrect because antibodies against GPIIb/IIIa cause immune thrombocytopenia (ITP), causing bleeding rather than severe thrombosis.\n\nKey Takeaway: HIT Type II is driven by IgG antibodies against PF4-heparin complexes that activate platelets via Fc-gamma-RIIa receptors, causing paradoxically severe thrombosis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q090",
        "subjectId": "pharmacology",
        "subjectTitle": "Pharmacology",
        "topic": "Gastrointestinal Pharmacology - Proton Pump Inhibitors",
        "prompt": "A 45-year-old male with severe peptic ulcer disease and Barrett esophagus is started on omeprazole. Proton pump inhibitors are prodrugs that undergo acid-catalyzed activation inside the secretory canaliculi of gastric parietal cells. What specific membrane enzyme is irreversibly inhibited by active sulfenamide intermediates of omeprazole?",
        "options": [
            "H+/K+-ATPase",
            "Na+/K+-ATPase",
            "Ca2+-ATPase",
            "H+/Cl- symporter"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nProton pump inhibitors (PPIs: omeprazole, esomeprazole, pantoprazole) are weak bases that accumulate selectively in the acidic environment of the gastric parietal cell secretory canaliculi (pH < 1.0). In this highly acidic canalicular space, the prodrug is protonated and converted into active, tetracyclic sulfenamide intermediates. The active sulfenamide forms covalent disulfide bonds with cysteine residues (particularly Cys813) on the extracellular domain of the gastric H+/K+-ATPase pump (the final common pathway of acid secretion). This causes permanent, irreversible enzyme inhibition, suppressing both basal and stimulated gastric acid production until new enzyme molecules are synthesized (24 to 48 hours).\n\nOption Review:\n- Option A is correct because PPIs covalently and irreversibly inhibit the gastric H+/K+-ATPase pump.\n- Option B is incorrect because the Na+/K+-ATPase is inhibited by cardiac glycosides (digoxin).\n- Option C is incorrect because Ca2+-ATPases pump calcium into the endoplasmic reticulum (SERCA) or out of the cell.\n- Option D is incorrect because chloride enters the lumen via independent apical cystic fibrosis conductance regulator (CFTR) and other chloride channels.\n\nKey Takeaway: Proton pump inhibitors irreversibly inhibit the gastric parietal cell H+/K+-ATPase pump by forming covalent disulfide bonds with cysteine residues.",
        "imageUrls": []
    },

    # ==========================================
    # FORENSIC MEDICINE & TOXICOLOGY (10 Questions: Q091 - Q100)
    # ==========================================
    {
        "id": "fmge-gt1-q091",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Thanatology - Postmortem Changes (Rigor Mortis)",
        "prompt": "A forensic pathologist conducts an autopsy on an adult male discovered deceased in his locked bedroom in temperate climate conditions. Examination demonstrates complete rigor mortis involving all joints of the face, neck, upper limbs, trunk, and lower limbs. Livor mortis on the back is fixed and does not blanch on firm thumb pressure. No signs of abdominal greenish discoloration or putrefaction are observed. What is the most accurate estimated postmortem interval (time since death)?",
        "options": [
            "1 to 2 hours",
            "4 to 6 hours",
            "12 to 18 hours",
            "36 to 48 hours"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nIn temperate climates, the timeline of postmortem changes follows classic sequential phases: 1) Algor mortis (cooling) begins immediately; 2) Livor mortis (hypostasis) appears within 1 to 2 hours and becomes 'fixed' (non-blanching due to hemolysis and pigment diffusion into dermal tissues) between 6 to 10 hours; 3) Rigor mortis (Nysten's rule: starts in involuntary heart muscle, then eyelids, jaw, neck, upper extremities, trunk, and lower extremities) begins in 2 to 3 hours, takes approximately 12 hours to become fully established in all joints, remains established for 12 hours (12 to 24 hours), and passes off in the same order over the next 12 hours (24 to 36 hours); 4) Putrefaction (greenish discoloration in right iliac fossa) begins at 36 to 48 hours. Fully established rigor in all limbs with fixed livor and no putrefaction indicates a postmortem interval of 12 to 18 hours.\n\nOption Review:\n- Option A is incorrect because at 1 to 2 hours, rigor mortis is absent and livor mortis is just beginning and fully blanches.\n- Option B is incorrect because at 4 to 6 hours, rigor is only partially established (upper body) and livor still blanches on pressure.\n- Option C is correct because fully established rigor mortis throughout the body with fixed livor mortis indicates 12 to 18 hours postmortem.\n- Option D is incorrect because by 36 to 48 hours, rigor has completely passed off (secondary flaccidity) and prominent putrefaction (marbling, foul odor) is present.\n\nKey Takeaway: Fully established rigor mortis across all joints combined with fixed livor mortis and absence of putrefaction indicates a time since death of 12 to 18 hours.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q092",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Thanatology - Postmortem Changes (Cadaveric Spasm)",
        "prompt": "A body is recovered from a river. On external examination, a clump of riverbed weeds and mud is found tightly gripped in the deceased's hand. The pathologist finds that the fingers cannot be unclasped without using extreme physical force, while the rest of the body muscles remain completely flaccid. What specific postmortem phenomenon is demonstrated?",
        "options": [
            "Rigor mortis",
            "Cadaveric spasm",
            "Heat stiffening",
            "Cold stiffening"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nCadaveric spasm (instantaneous rigor) is a rare condition in which a group of voluntary muscles that were in a state of intense, agitated physical contraction immediately prior to death remains stiffened immediately at the moment of death, completely bypassing the normal period of primary flaccidity. It usually affects the hands or arms and is triggered by sudden, violent deaths accompanied by severe emotional or physical stress (e.g., drowning victim grasping weeds/mud, suicide victim clutching a weapon, soldier gripping a rifle). It cannot be simulated postmortem and is definitive evidence that the individual was alive at the time of entering the water.\n\nOption Review:\n- Option A is incorrect because rigor mortis develops gradually after a period of primary muscular flaccidity and affects all muscles uniformly.\n- Option B is correct because instantaneous focal contracture of hands grasping objects at the moment of death defines cadaveric spasm.\n- Option C is incorrect because heat stiffening is caused by coagulation of muscle proteins by heat (>65°C), producing a 'pugilistic attitude'.\n- Option D is incorrect because cold stiffening is caused by the freezing of body fluids and fats at temperatures below 0°C.\n\nKey Takeaway: Cadaveric spasm involves instantaneous stiffening of muscles at the moment of death without preceding primary flaccidity, proving antemortem grasping.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q093",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Forensic Asphyxia - Hanging vs Strangulation",
        "prompt": "A 32-year-old female is found dead in her bedroom with a ligature around her neck. Autopsy reveals a ligature mark that is circular, horizontal, situated below the thyroid cartilage, and completely encircles the neck with a continuous uniform depth. Subcutaneous extravasation of blood is prominent beneath the mark. What mode of asphyxial death is indicated by these features?",
        "options": [
            "Complete hanging",
            "Ligature strangulation",
            "Manual strangulation",
            "Smothering"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nDifferentiating hanging from ligature strangulation is a classic medicolegal task: 1) Hanging: The ligature mark is typically oblique, non-continuous (interrupted at the suspension knot), situated high in the neck (above the thyroid cartilage), with depth deepest opposite the knot and tapering towards it. Fracture of the hyoid bone is more common in hanging. 2) Ligature strangulation (homicidal): The ligature mark is completely horizontal, circular (completely encircling the neck), continuous, and situated lower down at or below the level of the thyroid cartilage, with uniform depth and prominent underlying subcutaneous contusions.\n\nOption Review:\n- Option A is incorrect because hanging produces an oblique, non-continuous ligature mark located high in the neck above the thyroid cartilage.\n- Option B is correct because a horizontal, continuous, circular ligature mark situated below the thyroid cartilage is pathognomonic for ligature strangulation.\n- Option C is incorrect because manual strangulation (throttling) produces crescentic fingernail abrasions and fingertip contusions on the neck without a linear ligature mark.\n- Option D is incorrect because smothering involves mechanical occlusion of external air passages (nose and mouth) without neck marks.\n\nKey Takeaway: A continuous, horizontal ligature mark situated at or below the thyroid cartilage indicates homicidal ligature strangulation rather than hanging.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q094",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Ballistics - Firearm Injury Ranges",
        "prompt": "An autopsy is performed on a victim of a gunshot fatality. The entrance wound on the chest shows a circular central defect surrounded by an abrasion collar, a zone of burning (singeing of hair), dense black soot deposition (blackening), and unburnt powder grains embedded deeply into the dermis (tattooing). What was the firing range of the weapon?",
        "options": [
            "Contact range",
            "Close range",
            "Distant range",
            "Intermediate range"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nIn forensic ballistics, firearm entrance wounds are classified by firing range: 1) Contact range: Gun muzzle pressed against skin; produces stellate/bursting margins over bone (due to expanding blast gases), muzzle impression/abrasion, and soot/powder inside the wound track; 2) Close range (near-discharge, within 1 to 2 feet): Characterized by singeing/burning of hair (flame effect), dense black soot deposit that can be wiped off (blackening/smoke effect), and unburnt powder grains embedded in skin (tattooing/stippling that cannot be washed off); 3) Intermediate range: Blackening and burning are absent, but powder tattooing is still present; 4) Distant range (>2 to 3 feet): Flame, soot, and powder do not reach the target; produces only a clean circular hole with an abrasion collar and grease collar (dirt ring).\n\nOption Review:\n- Option A is incorrect because contact range shows muzzle imprint and muzzle blast lacerations with internal deposition of soot.\n- Option B is correct because burning, blackening, and tattooing together define a close-range (near) gunshot wound.\n- Option C is incorrect because distant range wounds show only an abrasion and grease ring without burning, soot, or tattooing.\n- Option D is incorrect because intermediate range wounds exhibit tattooing without flame burning and soot blackening.\n\nKey Takeaway: The presence of flame burning, soot blackening, and powder tattooing around a firearm entrance wound indicates a close-range (near) discharge.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q095",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Forensic Toxicology - Celphos (Aluminium Phosphide)",
        "prompt": "A 22-year-old farmer is rushed to the hospital after ingesting a grain preservative pesticide tablet (Celphos). He presents with severe epigastric pain, frequent vomiting, garlic-like breath, refractory cardiogenic shock, and metabolic acidosis. In the stomach, aluminium phosphide reacts with moisture and hydrochloric acid to release which lethal mitochondrial toxin?",
        "options": [
            "Phosphine gas",
            "Hydrogen cyanide",
            "Carbon monoxide",
            "Phosgene"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAluminium phosphide (marketed as Celphos, Quickphos, Alphos) is a common grain fumigant used for agricultural storage in India. Upon contact with moisture or gastric hydrochloric acid, it undergoes a chemical reaction: AlP + 3HCl -> AlCl3 + PH3, rapidly liberating phosphine gas (PH3). Phosphine has a characteristic pungent garlic or decaying-fish odor. It is rapidly absorbed and functions as a systemic protoplasmic poison, non-competitively inhibiting cytochrome c oxidase in the mitochondrial electron transport chain. This blocks cellular respiration, triggering oxidative stress and massive free-radical generation, resulting in refractory cardiogenic shock, arrhythmias, and acute lung injury. There is no specific antidote; management is supportive.\n\nOption Review:\n- Option A is correct because aluminium phosphide liberates lethal phosphine gas upon contact with gastric acid.\n- Option B is incorrect because hydrogen cyanide is released from cyanide salts.\n- Option C is incorrect because carbon monoxide is produced by incomplete combustion of hydrocarbons.\n- Option D is incorrect because phosgene is a toxic industrial choking gas used in chemical warfare.\n\nKey Takeaway: Aluminium phosphide (Celphos) releases phosphine gas upon contact with gastric acid, inhibiting mitochondrial cytochrome c oxidase and causing refractory cardiogenic shock.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q096",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Forensic Toxicology - Heavy Metal Poisoning (Arsenic)",
        "prompt": "A 40-year-old factory worker presents with peripheral sensorimotor neuropathy (glove-and-stocking pattern), hyperpigmentation of the trunk resembling a 'raindrop' appearance, and palmoplantar hyperkeratosis. Examination of his fingernails demonstrates transverse, white, non-palpable bands running across the nail plate. What are these diagnostic bands associated with chronic arsenic poisoning called?",
        "options": [
            "Muehrcke lines",
            "Aldrich-Mees lines",
            "Beau lines",
            "Lindsay nails"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nChronic arsenic toxicity (arsenicosis) from contaminated groundwater or industrial exposure presents with classic manifestations: 1) Cutaneous: 'Raindrop' pattern hyperpigmentation on the trunk, punctuated by palmoplantar hyperkeratotic papules; 2) Neurological: Symmetrical distal sensorimotor polyneuropathy ('glove-and-stocking' sensory loss and foot drop); 3) Vascular: 'Black foot disease' (peripheral gangrene); 4) Ungual: Aldrich-Mees lines (transverse white bands crossing the entire width of the fingernails and toenails, resulting from arsenic deposition in the nail matrix during periods of acute intoxication). Because arsenic has a high affinity for keratin sulfhydryl groups, it can be detected in hair and nail clippings for months to years.\n\nOption Review:\n- Option A is incorrect because Muehrcke lines are paired, white transverse lines in the vascular nail bed (which disappear with digital pressure) seen in severe hypoalbuminemia.\n- Option B is correct because Aldrich-Mees lines are transverse white nail bands characteristic of arsenic (and thallium) poisoning.\n- Option C is incorrect because Beau lines are transverse depressions or grooves across the nail plate caused by temporary cessation of nail matrix growth during severe systemic illness.\n- Option D is incorrect because Lindsay nails ('half-and-half nails') show proximal white and distal reddish-brown bands seen in chronic kidney disease.\n\nKey Takeaway: Aldrich-Mees lines are transverse white bands across the nails pathognomonic for arsenic poisoning, accompanied by 'raindrop' pigmentation and hyperkeratosis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q097",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Forensic Thanatology - Drowning Tests",
        "prompt": "A decomposed corpse is recovered from a lake. The police suspect the victim was murdered and thrown into the water postmortem. The forensic pathologist extracts samples from the femoral bone marrow and performs microscopic analysis after acid digestion. The presence of which acid-resistant, silica-walled microscopic unicellular algae in closed bone marrow confirms antemortem drowning?",
        "options": [
            "Diatoms",
            "Dinoflagellates",
            "Cyanobacteria",
            "Paramecium"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nDiatom testing (Gettler's test / Diatom test) is a crucial medicolegal method to establish whether drowning was antemortem or postmortem. Diatoms are aquatic microscopic unicellular algae (Chrysophyta) with extracellular silica cell walls (frustules) that resist acid digestion. When an individual drowns antemortem, inhalation of water carries diatoms into the alveoli. The high alveolar pressure ruptures alveolar capillaries, allowing diatoms to enter the pulmonary venous circulation and travel through the left heart into systemic arterial circulation, lodging in closed organs like the brain, kidneys, and femoral bone marrow. Conversely, in a dead body dumped into water, lack of circulation prevents diatoms from penetrating closed bone marrow cavities.\n\nOption Review:\n- Option A is correct because the identification of diatoms in closed bone marrow confirms antemortem drowning.\n- Option B is incorrect because dinoflagellates cause red tides and ciguatera/shellfish poisoning, not the drowning diatom test.\n- Option C is incorrect because cyanobacteria are photosynthetic bacteria lacking the rigid silica frustule necessary to survive acid digestion.\n- Option D is incorrect because Paramecia are ciliated protozoa without silica shells.\n\nKey Takeaway: Demonstration of diatoms in the closed femoral bone marrow is definitive proof of antemortem drowning.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q098",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Forensic Traumatology - Mechanical Injuries",
        "prompt": "A 25-year-old male is struck on the forearm with a solid wooden baton during an assault. Physical examination reveals two parallel, linear, red bruised tracks separated by an uninjured, pale, central zone of skin ('tram-line' bruise). What type of weapon characteristically produces this pattern of contusion?",
        "options": [
            "Sharp-edged razor blade",
            "Cylindrical or rod-shaped blunt weapon",
            "Flat broad wooden plank",
            "Heavy spherical iron ball"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nA 'tram-line' bruise (railway track contusion) is a pattern contusion characteristically produced by a blow from a weapon with a circular, cylindrical, or rod-like cross-section (such as a lathi, police baton, iron rod, or cane). When the cylindrical weapon impacts the skin, the maximum direct compressive force directly under the center of the rod crushes blood vessels flat without rupturing them. The blood is displaced laterally into adjacent marginal capillaries, which stretch and rupture under high hydraulic pressure, creating two parallel linear bruised lines separated by a pale central strip of intact, non-bruised skin.\n\nOption Review:\n- Option A is incorrect because a razor blade produces a sharp incised wound, not a contusion.\n- Option B is correct because a cylindrical or rod-shaped blunt object (e.g., lathi or baton) characteristically produces tram-line bruises.\n- Option C is incorrect because a flat broad wooden plank produces a diffuse, uniform rectangular contusion without the central pale zone.\n- Option D is incorrect because a spherical ball produces a circular or oval contusion.\n\nKey Takeaway: Tram-line bruises (two parallel contusions with a central pale zone) are pathognomonic for blunt trauma from a cylindrical rod or lathi.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q099",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Forensic Jurisprudence - Medical Negligence & Consent",
        "prompt": "During a routine laparoscopic appendectomy, the surgeon observes that the patient's right ovary contains a simple, asymptomatic 2 cm follicular cyst. Without obtaining prior consent from the patient or her family, the surgeon resects the ovary. The patient subsequently files a civil lawsuit. Which legal doctrine applies when a surgeon operates on a patient beyond the scope of informed consent?",
        "options": [
            "Medical battery",
            "Res ipsa loquitur",
            "Novus actus interveniens",
            "Contributory negligence"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nPerforming a surgical procedure or removing an organ without the patient's informed consent, in the absence of an immediate life-threatening emergency, constitutes civil and criminal medical battery (unlawful physical touching / assault). In medical jurisprudence, the landmark ruling in Samira Kohli vs. Dr. Prabha Manchanda established that consent given for a specific surgical procedure (e.g., appendectomy) cannot be extended to perform an additional, non-emergency procedure (e.g., oophorectomy or hysterectomy) merely because the surgeon deems it beneficial. Unless explicit consent for the additional procedure was obtained or a sudden emergency imperiling life arose, the unauthorized surgery constitutes battery.\n\nOption Review:\n- Option A is correct because unauthorized surgical intervention beyond the scope of informed consent constitutes medical battery.\n- Option B is incorrect because 'res ipsa loquitur' ('the thing speaks for itself') applies when an injury would not have occurred without negligence (e.g., leaving a mop in the abdomen).\n- Option C is incorrect because 'novus actus interveniens' refers to an independent intervening act that breaks the chain of causation.\n- Option D is incorrect because contributory negligence occurs when the patient's own negligence contributes to their injury.\n\nKey Takeaway: Performing an unconsented, non-emergency procedure during surgery constitutes medical battery under Indian and international jurisprudence.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q100",
        "subjectId": "forensic-medicine",
        "subjectTitle": "Forensic Medicine",
        "topic": "Forensic Toxicology - Methanol Poisoning & Formic Acid",
        "prompt": "A 42-year-old male is admitted with severe metabolic acidosis, vomiting, tachypnea, and visual disturbances described as 'being in a snowstorm'. Fundoscopy reveals bilateral optic disc hyperemia and retinal edema. Blood testing confirms acute methanol toxicity following consumption of illicit bootleg liquor (hooch). The accumulation of which toxic metabolite of methanol causes retinal toxicity and blindness?",
        "options": [
            "Formaldehyde",
            "Formic acid",
            "Glycolic acid",
            "Oxalic acid"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nMethanol is a toxic alcohol used as an industrial solvent and adulterant in illicit alcohol ('spurious liquor' or 'hooch'). Methanol is metabolized in the liver by alcohol dehydrogenase (ADH) to formaldehyde, which is rapidly converted by aldehyde dehydrogenase to formic acid (formate). Formic acid is the primary toxic metabolite responsible for both the profound high-anion-gap metabolic acidosis and end-organ ocular damage. Formate directly inhibits cytochrome c oxidase in the retinal pigment epithelium and optic nerve, impairing ATP production and causing optic disc hyperemia, edema, and permanent blindness ('snowstorm vision'). Treatment involves fomepizole or ethanol (ADH inhibitors) and hemodialysis.\n\nOption Review:\n- Option A is incorrect because formaldehyde is an extremely transient intermediate rapidly converted into formic acid.\n- Option B is correct because formic acid (formate) accumulates and directly causes retinal toxicity and severe metabolic acidosis.\n- Option C is incorrect because glycolic acid is a toxic metabolite of ethylene glycol.\n- Option D is incorrect because oxalic acid is a metabolite of ethylene glycol that forms calcium oxalate crystals in the kidneys.\n\nKey Takeaway: Methanol toxicity causes profound metabolic acidosis and blindness ('snowstorm vision') due to the accumulation of its toxic metabolite, formic acid.",
        "imageUrls": []
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(QUESTIONS)} questions in Part 1 Block 2.")
    for q in QUESTIONS:
        assert len(q["options"]) == 4, f"{q['id']} does not have 4 options"
        assert 0 <= q["answerIndex"] <= 3, f"{q['id']} invalid answerIndex"
        for opt in q["options"]:
            assert not opt.endswith(";"), f"{q['id']} option ends with semicolon: {opt}"
            assert "(" not in opt or any(c.isdigit() for c in opt), f"{q['id']} option has explanatory bracket: {opt}"
    print("All 49 questions passed structural assertions.")
