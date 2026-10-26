# -*- coding: utf-8 -*-
"""
FMGE Grand Test 1 - Part 2: Block 3
Obstetrics & Gynecology (30 Qs: Q251-Q280) + Radiology (5 Qs: Q281-Q285) + Radiotherapy (5 Qs: Q286-Q290) + Ophthalmology (5 Qs: Q291-Q295) + ENT (5 Qs: Q296-Q300) = 50 Questions (Q251 - Q300)
Strict adherence to 2026 NBE pattern, clinical vignettes, option-by-option review.
Zero textbook citations.
"""

QUESTIONS = [
    # ==========================================
    # OBSTETRICS & GYNECOLOGY (30 Questions: Q251 - Q280)
    # ==========================================
    {
        "id": "fmge-gt1-q251",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Ectopic Pregnancy Medical Management",
        "prompt": "A 26-year-old female presents with 6 weeks of amenorrhea, mild vaginal spotting, and left lower quadrant pain. Transvaginal ultrasound demonstrates an unruptured left tubal ectopic pregnancy measuring 2.4 cm in diameter without cardiac activity, and no free peritoneal fluid. Serum beta-hCG is 1,850 mIU/mL. The patient is hemodynamically stable. What is the pharmacological medical treatment of choice?",
        "options": [
            "Intramuscular methotrexate",
            "Oral mifepristone",
            "Intramuscular progesterone",
            "Oral misoprostol"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nEctopic pregnancy occurs when a blastocyst implants outside the endometrial cavity (>95% in the fallopian tube, most commonly the ampulla). In hemodynamically stable patients with unruptured tubal ectopic pregnancies, medical management with intramuscular methotrexate (a folic acid antagonist that inhibits dihydrofolate reductase, halting rapidly dividing trophoblastic cells) is the first-line treatment of choice. Ideal eligibility criteria for single-dose methotrexate (50 mg/m2 BSA) include: 1) Hemodynamically stable; 2) Baseline serum beta-hCG < 5,000 mIU/mL; 3) Ectopic gestational sac diameter < 3.5 to 4.0 cm; 4) Absence of embryonic cardiac motion on transvaginal ultrasound; 5) Patient compliant with post-treatment beta-hCG monitoring on days 4 and 7.\n\nOption Review:\n- Option A is correct because intramuscular methotrexate is the established medical therapy of choice for unruptured ectopic pregnancy.\n- Option B is incorrect because mifepristone is an antiprogestin used for medical termination of intrauterine pregnancy.\n- Option C is incorrect because progesterone sustains pregnancy and is contraindicated.\n- Option D is incorrect because misoprostol is a prostaglandin E1 analog used for uterine evacuation.\n\nKey Takeaway: Intramuscular methotrexate is the medical therapy of choice for unruptured ectopic pregnancy in stable patients with beta-hCG < 5,000 mIU/mL and mass < 3.5 cm.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q252",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Eclampsia & Magnesium Sulfate Regimen",
        "prompt": "A 24-year-old primigravida at 34 weeks of gestation presents with severe preeclampsia and suddenly develops a generalized tonic-clonic convulsion. Intravenous magnesium sulfate is administered using the Pritchard regimen to control eclampsia. Which physiological clinical sign is the most sensitive early clinical indicator of magnesium toxicity and must be checked before each maintenance dose?",
        "options": [
            "Presence of deep tendon knee jerk reflex",
            "Maternal pupil size",
            "Bowel sounds",
            "Visual acuity"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nMagnesium sulfate (MgSO4) is the anticonvulsant drug of choice for the prevention and treatment of eclamptic convulsions (superior to phenytoin and diazepam). In the Pritchard regimen, a 14 g loading dose (4 g IV + 10 g deep IM) is followed by 5 g IM maintenance every 4 hours. Therapeutic serum magnesium concentration is 4 to 7 mEq/L (2.0 to 3.5 mmol/L). Magnesium toxicity produces a predictable sequence of neurological and cardiovascular depression: 1) Loss of deep tendon patellar (knee-jerk) reflex occurs first at 8 to 10 mEq/L; 2) Respiratory depression (<12 breaths/min) occurs at 12 mEq/L; 3) Cardiac arrest in diastole occurs at >15 to 20 mEq/L. Therefore, before administering each maintenance dose, three clinical checks are mandatory: (1) Patellar reflex present; (2) Respiratory rate >= 16/min; (3) Urine output >= 30 mL/hour over preceding 4 hours. If toxicity develops, the specific antidote is 10% intravenous calcium gluconate (10 mL given over 10 minutes).\n\nOption Review:\n- Option A is correct because the loss of the patellar deep tendon reflex is the earliest sensitive sign of magnesium toxicity.\n- Option B is incorrect because pupil size is unaffected in early magnesium toxicity.\n- Option C is incorrect because bowel sounds do not correlate with toxic magnesium levels.\n- Option D is incorrect because visual disturbances are symptoms of severe preeclampsia, not magnesium toxicity.\n\nKey Takeaway: The presence of the patellar knee-jerk reflex is the most sensitive early clinical indicator ensuring safety before each dose of magnesium sulfate.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q253",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Postpartum Hemorrhage Uterotonic Agents",
        "prompt": "A 28-year-old female with a known history of severe bronchial asthma delivers a 3.8-kg infant. Following placental delivery, she develops primary postpartum hemorrhage due to uterine atony. Despite bimanual uterine compression and oxytocin infusion, uterine bleeding persists. Which second-line uterotonic agent is strictly contraindicated in patients with bronchial asthma?",
        "options": [
            "Carboprost tromethamine",
            "Methylergonovine",
            "Misoprostol",
            "Tranexamic acid"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nPrimary Postpartum Hemorrhage (PPH) is most commonly caused by uterine atony (>80% of cases). Uterotonic pharmacology must be tailored to maternal comorbidities: 1) Oxytocin is the first-line agent of choice for prophylaxis and treatment; 2) Methylergonovine (Methergine): An ergot alkaloid causing sustained tetanic myometrial contraction and systemic peripheral vasoconstriction; it is strictly CONTRAINDICATED in patients with hypertension, preeclampsia, or ischemic heart disease; 3) 15-methyl Prostaglandin F2-alpha (Carboprost tromethamine): A potent uterotonic that causes bronchoconstriction and pulmonary vasoconstriction; it is strictly CONTRAINDICATED in patients with bronchial asthma; 4) Misoprostol (PGE1 analog): Safe in asthma and hypertension.\n\nOption Review:\n- Option A is correct because Carboprost (PGF2-alpha) causes bronchospasm and is contraindicated in asthmatic patients.\n- Option B is incorrect because methylergonovine is contraindicated in hypertensive disorders, not asthma.\n- Option C is incorrect because misoprostol (PGE1) does not cause bronchoconstriction and is safe in asthma.\n- Option D is incorrect because tranexamic acid is an antifibrinolytic agent that is safe in asthmatic patients.\n\nKey Takeaway: Prostaglandin F2-alpha (Carboprost) is contraindicated in postpartum hemorrhage patients with asthma due to the risk of severe bronchoconstriction.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q254",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Antepartum Hemorrhage (Abruptio vs Previa)",
        "prompt": "A 32-year-old gravida 3 para 2 with chronic hypertension presents at 34 weeks of gestation with sudden onset of severe, continuous abdominal pain, dark vaginal bleeding, and dizziness. On abdominal examination, the uterus is tense, woody hard, and exquisitely tender, and uterine height exceeds dates. Fetal heart sounds are bradycardic (100 bpm). What is the most likely diagnosis?",
        "options": [
            "Abruptio placentae",
            "Placenta previa",
            "Uterine rupture",
            "Vasa previa"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAntepartum hemorrhage (APH) is bleeding from or into the genital tract after 20 to 24 weeks of gestation. The two major causes are distinguished by classic clinical features: 1) Abruptio Placentae (premature separation of a normally situated placenta): Characterized by sudden, severe, continuous abdominal/back pain, dark venous vaginal bleeding (or concealed hemorrhage), tense, hypertonic, tender ('woody-hard') uterus, maternal hypertension, and early fetal distress or fetal demise; 2) Placenta Previa: Characterized by painless, causeless, recurrent, bright red vaginal bleeding; soft, non-tender uterus; normal fetal heart rate; and high presenting part. Digital vaginal examination is strictly CONTRAINDICATED in placenta previa.\n\nOption Review:\n- Option A is correct because painful dark vaginal bleeding with a tense, tender, woody-hard uterus is diagnostic of abruptio placentae.\n- Option B is incorrect because placenta previa presents with painless, bright red bleeding and a soft, non-tender uterus.\n- Option C is incorrect because uterine rupture causes sudden cessation of contractions and palpable fetal parts outside the uterus.\n- Option D is incorrect because vasa previa causes painless fetal bleeding upon membrane rupture with fetal demise.\n\nKey Takeaway: Abruptio placentae is characterized by painful dark bleeding, uterine hypertonicity, a woody-hard tender uterus, and fetal distress.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q255",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Cardinal Movements of Labor",
        "prompt": "During the mechanism of normal vertex labor in a left occipito-anterior (LOA) presentation, the fetal head descends through the pelvic cavity and contacts the pelvic floor. Resistance from the pelvic floor and levator ani muscles causes the fetal chin to be pressed firmly against the fetal chest. What cardinal movement of labor is produced by this action, converting the presenting diameter to the smaller suboccipitobregmatic diameter (9.5 cm)?",
        "options": [
            "Flexion",
            "Internal rotation",
            "Extension",
            "Restitution"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe cardinal movements of labor in cephalic presentations occur in a coordinated sequence: 1) Engagement; 2) Descent; 3) Flexion: As the descending head meets resistance from the cervix, pelvic walls, or pelvic floor (gutter of levator ani), the fetal neck flexes, pressing the chin against the chest. Flexion substitutes the smaller suboccipitobregmatic diameter (9.5 cm) for the larger occipitofrontal diameter (11.5 cm), facilitating passage through the pelvis; 4) Internal rotation: The occiput rotates 1/8th of a circle (45 degrees) anteriorly toward the pubic symphysis; 5) Extension: The head is born by extension around the subpubic arch; 6) Restitution: The neck untwists, turning the head 45 degrees back to align with the shoulders; 7) External rotation: The shoulders rotate internally into the anteroposterior diameter, causing the head to rotate another 45 degrees externally; 8) Expulsion: Delivery of anterior shoulder, posterior shoulder, and body.\n\nOption Review:\n- Option A is correct because flexion presses the chin against the sternum, presenting the favorable 9.5 cm suboccipitobregmatic diameter.\n- Option B is incorrect because internal rotation aligns the anteroposterior axis of the head with the pelvic outlet.\n- Option C is incorrect because extension delivers the head past the vulva.\n- Option D is incorrect because restitution untwists the neck after head delivery.\n\nKey Takeaway: Flexion occurs as the descending head encounters pelvic floor resistance, substituting the smaller 9.5 cm suboccipitobregmatic diameter for delivery.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q256",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Cardiotocography Fetal Heart Decelerations",
        "prompt": "During electronic fetal heart monitoring in active labor, the cardiotocograph (CTG) demonstrates recurrent decelerations of the fetal heart rate. Each deceleration begins after the peak of the uterine contraction, reaches its lowest point (nadir) well after the contraction peak, and returns to baseline only after the contraction has fully resolved. What clinical condition is signaled by these late decelerations?",
        "options": [
            "Uteroplacental insufficiency",
            "Fetal head compression",
            "Umbilical cord compression",
            "Physiological fetal sleeping state"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIntrapartum cardiotocography (CTG) decelerations are classified into three distinct physiological types based on their relationship to uterine contractions: 1) Early decelerations: Symmetrical, gradual decrease in fetal heart rate where the nadir coincides exactly with the peak of the contraction (mirror image). They are caused by physiological fetal head compression triggering a vagal reflex, and are benign; 2) Late decelerations: Gradual decrease in FHR that begins after the contraction starts, reaches its nadir AFTER the contraction peak, and returns to baseline after the contraction ends. They are caused by uteroplacental insufficiency (reduced intervillous blood flow during contractions leading to transient fetal hypoxia, anaerobic metabolism, and chemoreceptor stimulation), indicating fetal hypoxia and acidosis; 3) Variable decelerations: Abrupt drop in FHR (<30 seconds to nadir) variable in onset and shape (V- or W-shaped), caused by umbilical cord compression.\n\nOption Review:\n- Option A is correct because late decelerations result from uteroplacental insufficiency and indicate fetal hypoxia.\n- Option B is incorrect because fetal head compression produces benign early decelerations.\n- Option C is incorrect because umbilical cord compression produces abrupt variable decelerations.\n- Option D is incorrect because fetal sleep reduces baseline variability, but does not produce recurrent late decelerations.\n\nKey Takeaway: Late decelerations on CTG begin after the contraction peak and signify uteroplacental insufficiency and fetal hypoxia.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q257",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Gestational Diabetes Mellitus (DIPSI Criteria)",
        "prompt": "In an antenatal clinic in India, a 24-year-old primigravida at 26 weeks of gestation undergoes screening for Gestational Diabetes Mellitus (GDM) using the non-fasting Single-Step Diabetes in Pregnancy Study Group of India (DIPSI) guidelines. She is administered a 75-gram oral glucose load regardless of the timing of her last meal, and venous plasma glucose is drawn at 2 hours. What plasma glucose cutoff value is diagnostic of gestational diabetes under DIPSI guidelines?",
        "options": [
            "Venous plasma glucose >= 140 mg/dL",
            "Venous plasma glucose >= 120 mg/dL",
            "Venous plasma glucose >= 160 mg/dL",
            "Venous plasma glucose >= 200 mg/dL"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe Government of India and the Diabetes in Pregnancy Study Group of India (DIPSI) recommend a single-step non-fasting 75-gram oral glucose tolerance test for universal screening and diagnosis of Gestational Diabetes Mellitus (GDM) in resource-limited antenatal clinics. The pregnant woman is given 75 g of anhydrous glucose dissolved in 300 mL of water, consumed over 5 to 10 minutes, irrespective of the time of her last meal. A 2-hour venous plasma glucose concentration >= 140 mg/dL (>=7.8 mmol/L) is diagnostic of GDM. If 2-hour plasma glucose is between 120 and 139 mg/dL, it is classified as gestational impaired glucose tolerance (GIGT) requiring lifestyle management.\n\nOption Review:\n- Option A is correct because a 2-hour venous plasma glucose >= 140 mg/dL confirms GDM under DIPSI guidelines.\n- Option B is incorrect because 120 mg/dL is the threshold for impaired glucose tolerance.\n- Option C is incorrect because 160 mg/dL is an unnecessarily high cutoff.\n- Option D is incorrect because 200 mg/dL diagnoses overt pre-existing diabetes.\n\nKey Takeaway: Under DIPSI guidelines, a 2-hour venous plasma glucose >= 140 mg/dL following a 75 g oral glucose challenge confirms Gestational Diabetes Mellitus.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q258",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Rh Isoimmunization & Anti-D Immunoglobulin",
        "prompt": "An Rh-negative unimmunized primigravida (indirect Coombs test negative) delivers a healthy Rh-positive infant. Following delivery, fetal red blood cells enter maternal circulation. To prevent maternal Rh(D) alloimmunization, intramuscular anti-D immunoglobulin (RhoGAM) should be administered within 72 hours of delivery. What is the standard prophylactic dose of anti-D immunoglobulin administered postpartum in India to neutralize up to 15 mL of fetal Rh-positive red blood cells (30 mL of whole blood)?",
        "options": [
            "300 micrograms",
            "150 micrograms",
            "50 micrograms",
            "500 micrograms"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nRh(D) alloimmunization occurs when an Rh(D)-negative mother is exposed to Rh(D)-positive fetal erythrocytes entering maternal circulation during delivery, miscarriage, amniocentesis, or trauma. The maternal immune system produces anti-D antibodies (initially IgM, followed by IgG that crosses the placenta in subsequent pregnancies to cause severe fetal hemolytic disease / hydrops fetalis). Prophylactic administration of exogenous anti-D immunoglobulin (RhIg) rapidly binds and clears fetal Rh-positive RBCs before maternal B-cell sensitization occurs. The standard postpartum prophylactic dose is 300 micrograms (1,500 IU) administered intramuscularly within 72 hours of delivery. A 300 microgram dose neutralizes up to 15 mL of fetal packed red cells or 30 mL of fetal whole blood (quantified by the Kleihauer-Betke acid elution test).\n\nOption Review:\n- Option A is correct because 300 micrograms is the standard full prophylactic postpartum dose of anti-D immunoglobulin.\n- Option B is incorrect because 150 micrograms is inadequate for a standard 30 mL fetomaternal hemorrhage.\n- Option C is incorrect because 50 micrograms is a micro-dose used for first-trimester abortions or miscarriages (<12 weeks).\n- Option D is incorrect because 500 micrograms exceeds the routine unquantified dose.\n\nKey Takeaway: The standard postpartum prophylactic dose of anti-D immunoglobulin is 300 micrograms (1,500 IU) given intramuscularly within 72 hours of delivery to an Rh-negative mother.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q259",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Gynecology - Cervical Cancer Screening (Bethesda System)",
        "prompt": "A 38-year-old female undergoes routine cervical cancer screening. Liquid-based cytology reveals high-grade squamous intraepithelial lesion (HSIL), and HPV DNA co-testing is positive for high-risk HPV genotype 16. What is the mandatory next step in the clinical management of a patient with an HSIL cytology report?",
        "options": [
            "Colposcopy and directed cervical biopsies",
            "Repeat cytology in 12 months",
            "Immediate total abdominal hysterectomy",
            "Empiric cryotherapy without biopsy"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIn cervical cancer screening, high-risk human papillomavirus (primarily HPV genotypes 16 and 18, which express E6 and E7 oncoproteins that inactivate p53 and Rb respectively) causes cervical intraepithelial neoplasia (CIN). High-grade squamous intraepithelial lesion (HSIL) on Pap cytology encompasses CIN 2, CIN 3, and carcinoma in situ, carrying a 20% to 30% risk of underlying invasive cervical cancer. According to ASCCP and international screening guidelines, any report of HSIL mandates immediate diagnostic colposcopy and directed cervical biopsies (applying 3% to 5% acetic acid to identify acetowhite lesions and Lugol's iodine to identify Schiller-positive, iodine-negative areas), along with endocervical curettage (ECC) if the squamocolumnar transformation zone is not fully visualized. Observation or repeating cytology in 12 months is unsafe.\n\nOption Review:\n- Option A is correct because colposcopy with directed biopsies is the mandatory immediate diagnostic investigation for HSIL.\n- Option B is incorrect because repeating cytology in 12 months is unsafe for high-grade lesions.\n- Option C is incorrect because hysterectomy without tissue confirmation of invasion depth is inappropriate.\n- Option D is incorrect because ablative therapy (cryotherapy) cannot be performed without a histological diagnosis to rule out invasive carcinoma.\n\nKey Takeaway: A cervical cytology result of HSIL mandates immediate colposcopy and directed cervical biopsies to detect high-grade dysplasia or invasive carcinoma.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q260",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Gynecology - Endometriosis Pathophysiology & Diagnosis",
        "prompt": "A 28-year-old nulliparous female presents with chronic pelvic pain, progressive secondary dysmenorrhea, deep dyspareunia, and painful defecation during menses (dyschezia). Bimanual pelvic examination reveals tender, nodular induration in the pouch of Douglas and fixed retroversion of the uterus. Transvaginal ultrasound shows a persistent bilateral ovarian cystic mass with homogeneous, low-level internal echoes ('ground-glass' appearance). What is the gold-standard diagnostic modality for endometriosis?",
        "options": [
            "Diagnostic laparoscopy with tissue biopsy",
            "Pelvic magnetic resonance imaging",
            "Serum CA-125 measurement",
            "Endometrial aspiration biopsy"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nEndometriosis is defined as the presence of functional endometrial stroma and glands in ectopic locations outside the uterine cavity, most commonly the ovaries (forming endometriomas or 'chocolate cysts'), pouch of Douglas, uterosacral ligaments, and pelvic peritoneum. Ectopic tissue undergoes cyclic bleeding and chronic inflammation, leading to dense fibrosis and pelvic adhesions. Clinical hallmarks include the triad of severe secondary dysmenorrhea, deep dyspareunia, and infertility, along with dyschezia and fixed retroverted uterus. Diagnostic laparoscopy with direct visual inspection (identifying blue-black 'powder-burn' or 'gun-metal' peritoneal lesions) and histological confirmation of endometrial glands, stroma, and hemosiderin-laden macrophages is the definitive gold standard for diagnosis and staging.\n\nOption Review:\n- Option A is correct because diagnostic laparoscopy with histological confirmation is the gold standard for diagnosing endometriosis.\n- Option B is incorrect because MRI reliably identifies endometriomas, but lacks sensitivity for superficial peritoneal implants.\n- Option C is incorrect because serum CA-125 may be non-specifically elevated, but has poor specificity.\n- Option D is incorrect because endometrial aspiration samples normal eutopic endometrium inside the cavity.\n\nKey Takeaway: Diagnostic laparoscopy with histological visualization of ectopic endometrial glands and stroma is the gold standard for diagnosing endometriosis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q261",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Endocrine Gynecology - Polycystic Ovary Syndrome (Rotterdam Criteria)",
        "prompt": "A 24-year-old female presents with oligomenorrhea (only 3 menstrual cycles in the past year), marked facial hirsutism, and treatment-resistant acne. Her BMI is 31 kg/m2. Pelvic ultrasound reveals enlarged ovaries with an increased stromal echogenicity and 15 small peripheral follicles (2 to 9 mm in diameter) arranged along the capsule in a 'string-of-pearls' appearance. Under the Rotterdam consensus criteria, how many of the three diagnostic features must be met to diagnose polycystic ovary syndrome (PCOS)?",
        "options": [
            "At least two of the three criteria",
            "All three criteria must be present",
            "Only one criterion is sufficient",
            "Serum insulin resistance must be documented"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe Rotterdam consensus criteria are the international standard for diagnosing Polycystic Ovary Syndrome (PCOS). Diagnosis requires the presence of at least TWO of the following THREE criteria (after excluding other etiologies like congenital adrenal hyperplasia, Cushing syndrome, hyperprolactinemia, and androgen-secreting tumors): 1) Oligo- or anovulation (irregular, infrequent, or absent menstrual periods); 2) Clinical and/or biochemical signs of hyperandrogenism (hirsutism, acne, male-pattern alopecia, or elevated free/total testosterone); 3) Polycystic ovarian morphology on pelvic ultrasound (presence of >= 20 follicles measuring 2-9 mm in diameter in either ovary, and/or ovarian volume >= 10 mL, displaying a classic 'necklace' or 'string-of-pearls' pattern). This patient fulfills all 3 criteria, definitively establishing PCOS.\n\nOption Review:\n- Option A is correct because the Rotterdam criteria require at least two of the three features for diagnosis.\n- Option B is incorrect because fulfilling all three is not mandatory.\n- Option C is incorrect because a single isolated criterion is insufficient.\n- Option D is incorrect because while insulin resistance is common, it is not a formal diagnostic criterion.\n\nKey Takeaway: Under the Rotterdam criteria, PCOS is diagnosed when at least two of three features are present: ovulatory dysfunction, hyperandrogenism, and polycystic ovarian morphology.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/PCOS_ultrasound.jpg/640px-PCOS_ultrasound.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q262",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Ovarian Neoplasms - Granulosa Cell Tumor",
        "prompt": "A 58-year-old postmenopausal female presents with vaginal bleeding and an asymptomatic unilateral pelvic mass. Endometrial biopsy reveals complex endometrial hyperplasia without atypia. Pelvic ultrasound demonstrates a solid-cystic left adnexal mass measuring 7 cm. Oophorectomy is performed. Histopathology reveals sheets of uniform cells with grooved 'coffee-bean' nuclei arranged in small follicle-like structures surrounding an acidophilic central lumen containing degenerated eosinophilic fluid (Call-Exner bodies). What is the diagnosis?",
        "options": [
            "Granulosa cell tumor",
            "Dysgerminoma",
            "Serous cystadenocarcinoma",
            "Krukenberg tumor"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nGranulosa cell tumor is the most common malignant sex cord-stromal tumor of the ovary, occurring predominantly in postmenopausal women (~50-55 years). These tumors actively synthesize and secrete estrogens (estradiol). Unopposed estrogen hypersecretion stimulates the endometrium, producing postmenopausal uterine bleeding and driving endometrial hyperplasia (~25-50%) or well-differentiated endometrial adenocarcinoma (~10%). Hallmark histopathological features include: 1) Monotonous, small, round-to-oval cells with pale nuclei featuring longitudinal nuclear grooves resembling 'coffee beans'; 2) Call-Exner bodies: Pathognomonic small, gland-like, rosetting rings of granulosa cells surrounding central eosinophilic, periodic acid-Schiff (PAS)-positive fluid. Serum inhibin B is an established tumor marker used for monitoring disease recurrence.\n\nOption Review:\n- Option A is correct because estrogen secretion, coffee-bean nuclei, and Call-Exner bodies define ovarian granulosa cell tumor.\n- Option B is incorrect because dysgerminoma is a germ cell tumor seen in young females with elevated LDH, featuring sheets of polygonal cells with clear cytoplasm and fibrous septa containing lymphocytes.\n- Option C is incorrect because serous cystadenocarcinoma produces psammoma bodies and elevated CA-125.\n- Option D is incorrect because Krukenberg tumor is a metastatic signet-ring cell adenocarcinoma, most commonly from gastric cancer.\n\nKey Takeaway: Ovarian granulosa cell tumors produce estrogen, causing postmenopausal bleeding, and display coffee-bean nuclei with pathognomonic Call-Exner bodies on histology.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q263",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Contraception - Intrauterine Contraceptive Devices (Cu-T 380A)",
        "prompt": "A 26-year-old para 1 female requests long-acting reversible contraception. After counseling, she chooses a Copper-T 380A intrauterine device (IUD). What is the approved maximum duration of contraceptive efficacy for the Cu-T 380A IUD, and what is its primary mechanism of action?",
        "options": [
            "Effective for 10 years, primarily acting by spermicidal foreign body reaction",
            "Effective for 5 years, primarily acting by suppression of ovulation",
            "Effective for 3 years, primarily acting by thickening cervical mucus",
            "Effective for 1 year, primarily acting by fallopian tube occlusion"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe Copper-T 380A (Cu-T 380A) is a highly effective, long-acting reversible contraceptive (LARC). The '380' denotes the total surface area of copper (380 mm2) wound around its polyethylene T-frame. The approved duration of effective contraception is 10 years (with clinical studies confirming efficacy up to 12 years). Its primary mechanism of action is non-hormonal: 1) Continuous release of copper ions (Cu2+) and the physical presence of the IUD induce a sterile, foreign-body inflammatory reaction in the endometrial cavity; 2) Copper ions are directly toxic and spermicidal, inhibiting sperm motility, capacitation, and the acrosome reaction, thereby preventing fertilization before an egg can be reached; 3) Secondarily, it alters endometrial receptivity to prevent implantation if fertilization occurs. In contrast, the levonorgestrel IUD (Mirena) is effective for 5 to 8 years and acts via progestogenic cervical mucus thickening and endometrial atrophy.\n\nOption Review:\n- Option A is correct because the Cu-T 380A is approved for 10 years and acts primarily via copper-induced spermicidal and foreign body inflammatory mechanisms.\n- Option B is incorrect because Cu-T 380A does not suppress systemic hypothalamic-pituitary-ovarian ovulation, and is effective for 10 years, not 5.\n- Option C is incorrect because cervical mucus thickening is the mechanism of progestin-only pills and implants.\n- Option D is incorrect because tubal occlusion describes permanent sterilization, not IUD action.\n\nKey Takeaway: The Copper-T 380A IUD is approved for 10 years of continuous contraception and functions primarily by producing a spermicidal and inflammatory intrauterine environment.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q264",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Infections - Pelvic Inflammatory Disease (PID)",
        "prompt": "A 22-year-old sexually active female presents with bilateral lower abdominal pain, abnormal foul-smelling vaginal discharge, dyspareunia, and fever. Pelvic examination demonstrates exquisite pain on movement of the cervix ('cervical motion tenderness' / Chandelier sign) and bilateral adnexal tenderness. What empirical outpatient antibiotic regimen is recommended by CDC guidelines for acute pelvic inflammatory disease?",
        "options": [
            "Single-dose intramuscular ceftriaxone plus oral doxycycline and oral metronidazole for 14 days",
            "Oral ciprofloxacin monotherapy for 7 days",
            "Oral azithromycin single dose alone",
            "Intramuscular penicillin G benzathine single dose"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nPelvic Inflammatory Disease (PID) is an ascending polymicrobial infection of the upper female genital tract (endometrium, fallopian tubes, ovaries, and pelvic peritoneum) originating from the endocervix. The most common initiating sexually transmitted pathogens are Neisseria gonorrhoeae and Chlamydia trachomatis, frequently complicated by secondary anaerobic vaginal flora and enteric bacteria. Diagnostic criteria require pelvic pain plus >= 1 minimum clinical sign: 1) Cervical motion tenderness (Chandelier sign); 2) Uterine tenderness; 3) Adnexal tenderness. To prevent devastating long-term reproductive sequelae (tubal infertility, ectopic pregnancy, chronic pelvic pain), empirical broad-spectrum outpatient therapy must be initiated immediately: Intramuscular Ceftriaxone (500 mg single dose, to cover N. gonorrhoeae) PLUS oral Doxycycline (100 mg twice daily for 14 days, to cover C. trachomatis) PLUS oral Metronidazole (500 mg twice daily for 14 days, to cover anaerobes).\n\nOption Review:\n- Option A is correct because ceftriaxone IM plus 14 days of doxycycline and metronidazole is the guideline-directed regimen for acute PID.\n- Option B is incorrect because fluoroquinolone monotherapy has high rates of gonococcal resistance and fails to cover anaerobes.\n- Option C is incorrect because single-dose azithromycin is inadequate for upper genital tract pelvic infection.\n- Option D is incorrect because benzathine penicillin treats Treponema pallidum (syphilis), not PID.\n\nKey Takeaway: Outpatient management of PID requires IM ceftriaxone combined with 14 days of oral doxycycline and metronidazole to cover gonorrhea, chlamydia, and anaerobes.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q265",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Normal Labor (Active Phase & Partogram)",
        "prompt": "According to updated World Health Organization (WHO) labor guidelines, what rate of cervical dilatation defines the transition from the latent phase to the active first stage of labor in spontaneous vertex singleton deliveries?",
        "options": [
            "Cervical dilatation of 5 cm or greater with regular uterine contractions",
            "Cervical dilatation of 2 cm with irregular contractions",
            "Cervical effacement of 50% regardless of dilatation",
            "Spontaneous rupture of fetal membranes regardless of dilatation"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe first stage of labor is divided into: 1) Latent phase: Characterized by slow, gradual cervical effacement and dilatation, typically lasting up to 12 to 20 hours; 2) Active phase: Characterized by rapid, progressive cervical dilatation. In modern consensus guidelines (WHO, ACOG, and NICE), the threshold defining the onset of the active first stage of labor is a cervical dilatation of 5 cm (or 4 to 5 cm) in the presence of regular, painful uterine contractions, because cervical dilatation accelerates substantially only after 5 cm. In the WHO modified partogram, cervical progress is plotted against an 'Alert line' (representing an expected dilatation of 1 cm/hour) and an 'Action line' drawn 4 hours parallel to the right of the Alert line. Crossing the Action line indicates protracted active phase or arrest of labor, mandating active intervention (amniotomy, oxytocin augmentation, or cesarean delivery).\n\nOption Review:\n- Option A is correct because cervical dilatation of >=5 cm with regular contractions defines the active first stage of labor.\n- Option B is incorrect because 2 cm is within the latent phase of labor.\n- Option C is incorrect because effacement alone without significant dilatation does not mark active labor.\n- Option D is incorrect because rupture of membranes can occur before labor onset (PROM) and does not define active labor.\n\nKey Takeaway: The active first stage of labor begins at 5 cm of cervical dilatation with regular contractions, plotted on the partogram to monitor progress.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q266",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Shoulder Dystocia Emergency Maneuvers",
        "prompt": "Following the delivery of the fetal head in a 4.1-kg infant of a diabetic mother, the head retracts tightly back against the maternal perineum ('turtle sign'), and the anterior shoulder impacts behind the maternal symphysis pubis. Gentle downward traction fails to achieve delivery. What is the immediate first-line non-operative maneuver recommended to resolve shoulder dystocia?",
        "options": [
            "McRoberts maneuver combined with suprapubic pressure",
            "Fundal pressure applied firmly over the uterine fundus",
            "Zavanelli maneuver with cephalic replacement",
            "Immediate symphysiotomy"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nShoulder dystocia is an unpredictable obstetric emergency where the anterior fetal shoulder impacts against the maternal pubic symphysis (or posterior shoulder against sacral promontory) after delivery of the head. It is heralded by the 'turtle sign' (recoil of the fetal chin against the perineum). The immediate, highly effective first-line intervention (successful in >90% of cases) is the McRoberts maneuver: The mother's hips are hyperflexed and abducted tightly against her abdomen. This rotates the pubic symphysis cephalad and flattens the lumbosacral angle, widening the pelvic inlet. Simultaneously, an assistant applies downward and lateral suprapubic pressure (Rubin I maneuver) over the anterior fetal shoulder to disimpact and adduct it beneath the symphysis. Fundal pressure is strictly CONTRAINDICATED as it impacts the shoulder harder and causes uterine rupture or brachial plexus avulsion.\n\nOption Review:\n- Option A is correct because the McRoberts maneuver with suprapubic pressure is the primary first-line intervention for shoulder dystocia.\n- Option B is incorrect because fundal pressure is dangerous, ineffective, and strictly contraindicated.\n- Option C is incorrect because the Zavanelli maneuver (pushing the head back into the vagina for emergency cesarean) is a last-resort maneuver after internal techniques fail.\n- Option D is incorrect because symphysiotomy is an extreme second-line destructive surgery.\n\nKey Takeaway: The McRoberts maneuver (maternal hip hyperflexion) combined with suprapubic pressure is the first-line intervention of choice for shoulder dystocia.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q267",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Gynecologic Oncology - Endometrial Carcinoma Risk Factors",
        "prompt": "A 62-year-old obese female with a history of nulliparity, type 2 diabetes mellitus, and hypertension presents with painless postmenopausal vaginal bleeding for 2 months. Transvaginal ultrasound demonstrates an endometrial stripe thickness of 14 mm. What is the primary hormonal mechanism driving Type I endometrioid adenocarcinoma of the endometrium?",
        "options": [
            "Prolonged unopposed estrogen stimulation",
            "Excessive continuous progesterone exposure",
            "High circulating follicle-stimulating hormone",
            "Suppression of adrenal androgens"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nEndometrial carcinoma is the most common gynecological malignancy in developed countries, classified into two types: 1) Type I (Endometrioid adenocarcinoma, ~80%): Directly driven by prolonged, chronic, unopposed estrogen stimulation without adequate counterbalancing progesterone. In postmenopausal or obese women, peripheral aromatization of adrenal androstenedione to estrone by excess adipose tissue aromatase produces continuous estrogenic stimulation. Unopposed estrogen binds to nuclear estrogen receptors, driving continuous endometrial glandular proliferation, leading from simple hyperplasia to atypical hyperplasia (endometrial intraepithelial neoplasia / EIN), and ultimately invasive adenocarcinoma. Mutations in PTEN (60-80%) and microsatellite instability (MSI) are hallmarks; 2) Type II (Serous/Clear cell, ~20%): Estrogen-independent, arising in atrophic endometrium in older women, driven by TP53 mutations with aggressive behavior.\n\nOption Review:\n- Option A is correct because prolonged unopposed estrogen stimulation is the cardinal driver of Type I endometrioid adenocarcinoma.\n- Option B is incorrect because progesterone opposes estrogen and induces secretory differentiation, protecting against endometrial cancer.\n- Option C is incorrect because elevated FSH is a normal postmenopausal finding, not an oncogenic driver.\n- Option D is incorrect because excess adrenal androgens are aromatized to estrone, contributing to disease.\n\nKey Takeaway: Prolonged unopposed estrogen stimulation is the fundamental pathophysiological mechanism driving Type I endometrioid adenocarcinoma.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q268",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Gynecology - Uterine Leiomyomas (Fibroids)",
        "prompt": "A 35-year-old nulligravida presents with heavy, prolonged menstrual bleeding (menorrhagia) leading to severe iron deficiency anemia, along with lower pelvic pressure. Bimanual examination reveals an irregularly enlarged, firm, non-tender uterus. Transvaginal ultrasound demonstrates a 4 cm round, well-circumscribed, hypoechoic mass located directly beneath the endometrium, distorting the uterine cavity. Which anatomical subtype of uterine fibroid is most prone to causing heavy menorrhagia and infertility?",
        "options": [
            "Submucosal leiomyoma",
            "Intramural leiomyoma",
            "Subserosal leiomyoma",
            "Pedunculated subserosal leiomyoma"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nUterine leiomyomas (fibroids) are benign monoclonal smooth muscle neoplasms arising from the myometrium. They are classified by anatomical location relative to the uterine wall: 1) Submucosal leiomyomas (FIGO Type 0, 1, 2): Develop directly beneath the endometrium and project into the uterine cavity. Even small submucosal fibroids ulcerate the overlying endometrial vascular bed, impair myometrial contractility, and distort the endometrial architecture, making them the most symptomatic subtype causing heavy menstrual bleeding (menorrhagia), severe anemia, and recurrent implantation failure/infertility; 2) Intramural leiomyomas: Reside within the thickness of the myometrium, causing menorrhagia and bulk symptoms; 3) Subserosal leiomyomas: Project outward from the peritoneal surface, presenting primarily with bulk compression of adjacent bladder or bowel rather than heavy vaginal bleeding.\n\nOption Review:\n- Option A is correct because submucosal leiomyomas distort the endometrial cavity and are the primary cause of severe menorrhagia and infertility.\n- Option B is incorrect because intramural fibroids require larger size to produce comparable bleeding.\n- Option C is incorrect because subserosal fibroids rarely cause abnormal uterine bleeding.\n- Option D is incorrect because pedunculated subserosal fibroids present with torsion or pressure symptoms.\n\nKey Takeaway: Submucosal leiomyomas directly distort the endometrial cavity and are the most common fibroid subtype causing heavy menorrhagia and reproductive impairment.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q269",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Active Management of Third Stage of Labor (AMTSL)",
        "prompt": "Following the vaginal delivery of a healthy term neonate, the obstetrician performs Active Management of the Third Stage of Labor (AMTSL) to prevent postpartum hemorrhage. According to WHO guidelines, what are the three standard components of AMTSL?",
        "options": [
            "Administration of a prophylactic uterotonic drug, controlled cord traction, and delayed cord clamping",
            "Immediate manual removal of placenta, forceful cord traction, and oxytocin",
            "Immediate cord clamping, fundal pressure, and ergotamine injection",
            "Intravenous tranexamic acid, routine episiotomy, and ice pack application"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nActive Management of the Third Stage of Labor (AMTSL) is a proven evidence-based package of interventions that reduces the incidence of primary postpartum hemorrhage by approximately 60%: 1) Administration of a prophylactic uterotonic agent: 10 International Units (IU) of oxytocin administered intramuscularly (or IV) immediately following the delivery of the baby (after ruling out a second twin); 2) Controlled Cord Traction (CCT / Brandt-Andrews maneuver): Gentle traction on the clamped umbilical cord with one hand, combined with simultaneous upward and backward counter-pressure on the lower uterine segment above the pubic symphysis with the other hand to prevent uterine inversion; 3) Delayed cord clamping (clamping after 1 to 3 minutes, unless immediate resuscitation is required), along with routine abdominal palpation to confirm uterine contraction.\n\nOption Review:\n- Option A is correct because administration of a uterotonic (oxytocin), controlled cord traction, and delayed cord clamping form the pillars of AMTSL.\n- Option B is incorrect because routine manual removal of the placenta and forceful traction are dangerous and contraindicated.\n- Option C is incorrect because fundal pressure is contraindicated due to the risk of uterine inversion.\n- Option D is incorrect because tranexamic acid and routine episiotomy are not routine components of third-stage management.\n\nKey Takeaway: AMTSL includes administration of 10 IU oxytocin, controlled cord traction with counter-pressure, and delayed cord clamping to prevent postpartum hemorrhage.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q270",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Gynecology - Ovarian Germ Cell Tumors (Dysgerminoma)",
        "prompt": "An 18-year-old female presents with lower abdominal pain and a palpable pelvic mass. Pelvic ultrasound reveals an 8 cm solid left ovarian mass. Serum tumor markers show markedly elevated lactate dehydrogenase (LDH) and beta-hCG, with normal alpha-fetoprotein. Histopathology reveals sheets of large, uniform polygonal cells with clear, glycogen-rich cytoplasm, distinct cell borders, and prominent central nucleoli, separated by thin fibrous septa heavily infiltrated by lymphocytes. What is the most common malignant germ cell tumor of the ovary?",
        "options": [
            "Dysgerminoma",
            "Yolk sac tumor",
            "Choriocarcinoma",
            "Immature teratoma"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nDysgerminoma is the most common malignant ovarian germ cell tumor, accounting for ~50% of germ cell malignancies, typically occurring in adolescent and young women (<30 years of age). It is the ovarian histological counterpart of testicular seminoma. Histopathology is distinctive: Large, round-to-polygonal cells with clear, pale glycogen-filled cytoplasm, well-defined cell borders, and rounded nuclei with prominent nucleoli, arranged in sheets or cords separated by delicate fibrous connective tissue septa that are characteristically infiltrated by mature T-lymphocytes. The serum tumor marker of choice is serum Lactate Dehydrogenase (LDH), which is consistently elevated, with occasionally elevated beta-hCG if syncytiotrophoblastic giant cells are present. Dysgerminomas are exquisitely radiosensitive and chemosensitive (treated with BEP: bleomycin, etoposide, cisplatin) with high cure rates.\n\nOption Review:\n- Option A is correct because sheets of clear cells separated by lymphocyte-infiltrated fibrous septa and elevated LDH define dysgerminoma.\n- Option B is incorrect because yolk sac (endodermal sinus) tumor shows Schiller-Duval bodies and elevated alpha-fetoprotein (AFP).\n- Option C is incorrect because choriocarcinoma shows syncytiotrophoblasts and cytotrophoblasts with massive beta-hCG elevation and hematogenous metastasis.\n- Option D is incorrect because immature teratoma contains immature embryonic neuroectodermal rosettes.\n\nKey Takeaway: Dysgerminoma is the most common malignant ovarian germ cell tumor, characterized by sheets of clear cells with lymphocytic septa and elevated serum LDH.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Dysgerminoma_histopathology.jpg/640px-Dysgerminoma_histopathology.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q271",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Twin Pregnancy Chorionicity",
        "prompt": "A 28-year-old female undergoes a first-trimester routine ultrasound at 11 weeks of gestation for a spontaneous twin pregnancy. The sonographer identifies a single placenta with two separate amniotic sacs. At the intertwin membrane-placental junction, a thickened triangular projection of placental tissue is seen wedging between the two layers of chorion (the 'lambda' or 'twin-peak' sign). What type of chorionicity and amnionicity is confirmed by the lambda sign?",
        "options": [
            "Dichorionic diamniotic twin pregnancy",
            "Monochorionic diamniotic twin pregnancy",
            "Monochorionic monoamniotic twin pregnancy",
            "Conjoined twin pregnancy"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nDetermining chorionicity in the first trimester (11 to 14 weeks) is the single most critical ultrasound assessment in multiple gestations because monochorionic twins share a single placenta and carry high risks of vascular complications (Twin-to-Twin Transfusion Syndrome [TTTS], Twin Anemia-Polycythemia Sequence [TAPS], selective fetal growth restriction): 1) Dichorionic Diamniotic (DCDA): Two separate chorions and two amrions. At the base of the intertwin dividing membrane, placental tissue extends into the intertwin space, creating a triangular tissue wedge known as the 'lambda' sign (twin-peak sign), and the membrane thickness is >2 mm; 2) Monochorionic Diamniotic (MCDA): A single chorion with two amnions. The dividing membrane consists of only two thin layers of amnion without intervening chorionic tissue, inserting abruptly into the flat placenta at a right angle to form the 'T' sign, with a membrane thickness <2 mm.\n\nOption Review:\n- Option A is correct because the 'lambda' (twin-peak) sign is pathognomonic for a dichorionic diamniotic twin pregnancy.\n- Option B is incorrect because monochorionic diamniotic twins display the 'T' sign.\n- Option C is incorrect because monochorionic monoamniotic twins lack an intertwin dividing membrane entirely.\n- Option D is incorrect because conjoined twins show fused fetal bodies sharing organs.\n\nKey Takeaway: The 'lambda' (twin-peak) sign on first-trimester ultrasound confirms a dichorionic diamniotic twin pregnancy, whereas the 'T' sign indicates monochorionicity.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q272",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Cervical Insufficiency & Cerclage",
        "prompt": "A 26-year-old gravida 3 para 0 presents for pre-conceptional counseling with a history of two consecutive second-trimester pregnancy losses at 18 and 20 weeks. In both prior pregnancies, she experienced sudden, painless cervical dilatation followed by rupture of membranes and rapid delivery of an intact, living fetus. Transvaginal ultrasound in the current pregnancy at 13 weeks reveals an asymptomatic cervical length of 18 mm. What prophylactic surgical intervention is indicated for cervical insufficiency?",
        "options": [
            "Cervical cerclage stitch",
            "Intramuscular betamethasone",
            "Oral indomethacin therapy",
            "Emergency cesarean section"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nCervical insufficiency (incompetence) is the inability of the uterine cervix to retain an intrauterine pregnancy in the absence of clinical contractions or labor. The classic clinical presentation is recurrent, painless, silent cervical dilatation in the second trimester (typically between 16 and 24 weeks), leading to prolapse of fetal membranes into the vagina, rupture of membranes, and expulsion of an immature fetus. Risk factors include previous cervical trauma (cervical conization, loop electrosurgical excision procedure [LEEP], mechanical cervical dilation for D&C). In patients with a classic history or a short cervical length (<25 mm) before 24 weeks, elective prophylactic cervical cerclage (McDonald or Shirodkar transvaginal purse-string suture placed at the level of the internal os at 12 to 14 weeks of gestation) is the established intervention of choice. The suture is electively removed at 36 to 37 weeks.\n\nOption Review:\n- Option A is correct because elective cervical cerclage mechanically reinforces the incompetent internal os.\n- Option B is incorrect because corticosteroids are indicated between 24 and 34 weeks for fetal lung maturation.\n- Option C is incorrect because indomethacin is a tocolytic for acute preterm labor, not an anatomic repair for silent cervical opening.\n- Option D is incorrect because cesarean section is not indicated at 13 weeks.\n\nKey Takeaway: Prophylactic cervical cerclage (McDonald or Shirodkar suture) is the treatment of choice for cervical insufficiency, placed at 12 to 14 weeks of gestation.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q273",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Gynecology - Vulvar Malignancies (Paget Disease of the Vulva)",
        "prompt": "A 68-year-old postmenopausal female presents with persistent, intractable vulvar pruritus for 18 months. Physical examination reveals a well-demarcated, erythematous, eczematoid plaque with scattered white hyperkeratotic crusts resembling 'strawberries and cream' involving the left labium majus. Punch biopsy reveals large, pale, vacuolated intraepithelial cells infiltrating the epidermis. The cells stain positive with periodic acid-Schiff (PAS) and mucicarmine. What is the diagnosis?",
        "options": [
            "Extramammary Paget disease of the vulva",
            "Vulvar lichen sclerosus",
            "Squamous cell carcinoma of the vulva",
            "Lichen simplex chronicus"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nExtramammary Paget disease of the vulva is a rare intraepithelial glandular adenocarcinoma seen predominantly in postmenopausal Caucasian women. Clinically, it presents with long-standing, severe vulvar pruritus and a characteristic well-demarcated, velvety red, pruritic, eczematoid plaque with islands of white epithelial hyperkeratosis, often described as a 'strawberries and cream' appearance. Histologically, it is characterized by Paget cells: large, solitary or clustered intraepithelial cells with abundant pale, clear, mucinous cytoplasm and large pleomorphic nuclei. Because Paget cells contain mucin, they stain intensely positive with periodic acid-Schiff (PAS) with diastase resistance, mucicarmine, and cytokeratin 7 (CK7). In contrast to Paget disease of the breast (where >95% have an underlying ductal carcinoma), vulvar Paget disease is most commonly intraepithelial (~80%), though ~20% may harbor an underlying sweat gland or adnexal adenocarcinoma.\n\nOption Review:\n- Option A is correct because the 'strawberries and cream' plaque with intraepithelial mucin-positive Paget cells defines Paget disease of the vulva.\n- Option B is incorrect because lichen sclerosus presents with porcelain-white atrophic patches with labial resorption and epidermal thinning.\n- Option C is incorrect because invasive squamous cell carcinoma shows keratin pearls and intercellular bridges, negative for mucicarmine.\n- Option D is incorrect because lichen simplex chronicus is benign epidermal thickening due to chronic rubbing.\n\nKey Takeaway: Extramammary Paget disease of the vulva presents as an eczematoid 'strawberries and cream' plaque with intraepithelial mucicarmine-positive Paget cells.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q274",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Hyperemesis Gravidarum & Wernicke Encephalopathy",
        "prompt": "A 22-year-old primigravida at 9 weeks of gestation is admitted with intractable nausea, vomiting, weight loss exceeding 10% of her pre-pregnancy weight, ketonuria, and severe dehydration (hyperemesis gravidarum). She is started on rapid intravenous infusion of 5% dextrose in water without vitamin supplementation. Three days later, she develops horizontal nystagmus, bilateral lateral rectus palsy, confusion, and gait ataxia. Deficiency of which vitamin was precipitated by glucose administration?",
        "options": [
            "Thiamine (Vitamin B1)",
            "Pyridoxine (Vitamin B6)",
            "Niacin (Vitamin B3)",
            "Cobalamin (Vitamin B12)"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nHyperemesis gravidarum is severe, persistent nausea and vomiting of early pregnancy associated with ketosis, electrolyte abnormalities (hypokalemia, hypochloremic metabolic alkalosis), and weight loss >5% of pre-pregnancy body weight. Patients rapidly deplete their limited endogenous reserves of water-soluble vitamins, particularly thiamine (vitamin B1), which last only 2 to 3 weeks. Thiamine pyrophosphate (TPP) is an indispensable cofactor for carbohydrate metabolism (pyruvate dehydrogenase and alpha-ketoglutarate dehydrogenase). Infusing intravenous dextrose solutions in a thiamine-depleted patient increases carbohydrate flux through glycolysis, consuming all remaining thiamine stores. Pyruvate cannot be converted to acetyl-CoA, triggering severe lactic acidosis and selective neuronal necrosis in the mammillary bodies and periaqueductal gray matter, precipitating acute Wernicke encephalopathy (triad: confusion, ophthalmoplegia/nystagmus, and ataxia). Thiamine must ALWAYS be administered prior to or concurrently with IV glucose in hyperemesis.\n\nOption Review:\n- Option A is correct because acute thiamine (vitamin B1) deficiency triggered by dextrose infusion causes Wernicke encephalopathy.\n- Option B is incorrect because pyridoxine is used for routine nausea, but deficiency does not produce Wernicke encephalopathy.\n- Option C is incorrect because niacin deficiency causes pellagra (diarrhea, dermatitis, dementia).\n- Option D is incorrect because vitamin B12 stores in the liver last for 3 to 5 years.\n\nKey Takeaway: Intravenous glucose administration in patients with hyperemesis gravidarum without thiamine supplementation can precipitate acute Wernicke encephalopathy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q275",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Gynecology - Asherman Syndrome",
        "prompt": "A 28-year-old female presents with secondary amenorrhea and infertility following a vigorous curettage performed for retained products of conception after a postpartum hemorrhage 8 months ago. Cyclic monthly lower abdominal cramping without menstrual bleeding is reported. Normal secondary sexual characteristics are present. Progestin challenge test fails to induce withdrawal bleeding, and combined estrogen-progestin challenge also yields no bleeding. Normal serum FSH, LH, and estradiol levels are present. What is the diagnosis?",
        "options": [
            "Asherman syndrome",
            "Sheehan syndrome",
            "Premature ovarian insufficiency",
            "Polycystic ovary syndrome"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAsherman syndrome (intrauterine adhesions / synechiae) is an acquired anatomical cause of secondary amenorrhea resulting from destruction and obliteration of the endometrial basal layer (stratum basalis). It is typically provoked by vigorous or overzealous sharp curettage of a recently gravid uterus (postpartum or post-abortion curettage), during which the denuded anterior and posterior myometrial surfaces adhere to form fibrous synechiae. Because the functional endometrium is replaced by fibrous scar tissue, the uterine end-organ is completely unresponsive to endogenous or exogenous sex steroids. Consequently, both the progestin withdrawal challenge AND the combined estrogen-progesterone challenge fail to produce withdrawal bleeding (outflow tract / uterine cause of amenorrhea). Hysteroscopy is the diagnostic and therapeutic gold standard, allowing direct visualization and hysteroscopic adhesiolysis.\n\nOption Review:\n- Option A is correct because intrauterine adhesions following postpartum curettage with negative estrogen-progestin withdrawal define Asherman syndrome.\n- Option B is incorrect because Sheehan syndrome results from pituitary ischemic necrosis, presenting with failure of lactation, low gonadotropins, and positive bleeding if estrogen/progesterone are administered.\n- Option C is incorrect because premature ovarian failure is characterized by hypergonadotropic hypogonadism (markedly elevated FSH/LH).\n- Option D is incorrect because PCOS patients bleed following a progestin challenge.\n\nKey Takeaway: Asherman syndrome is caused by intrauterine fibrous adhesions following vigorous post-pregnancy curettage, diagnosed by negative estrogen-progestin withdrawal and confirmed by hysteroscopy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q276",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Bishop Score & Cervical Ripening",
        "prompt": "A 41-week pregnant primigravida is evaluated for induction of labor. An internal pelvic examination is performed to calculate the Bishop score: the cervix is 2 cm dilated (1 point), 50% effaced (1 point), soft in consistency (2 points), mid-position (1 point), and the fetal presenting part is at station -1 (1 point), yielding a total Bishop score of 6. What minimum Bishop score is generally considered 'favorable', indicating a high likelihood of successful vaginal delivery with oxytocin alone?",
        "options": [
            "Bishop score of 8 or greater",
            "Bishop score of 4 or less",
            "Bishop score of 5 exactly",
            "Bishop score of 2 or less"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe Bishop score is a standardized pre-induction scoring system that evaluates the cervical readiness and favorability for induction of labor based on five components (scored 0 to 2 or 3 points each): 1) Cervical Dilatation (cm); 2) Effacement (%); 3) Consistency (firm, medium, soft); 4) Position (posterior, mid, anterior); 5) Station of the presenting part relative to the ischial spines (-3 to +2). Maximum score is 13. Interpretation: 1) Bishop score >= 8: Favorable (ripe) cervix. The probability of successful vaginal induction is high and similar to spontaneous labor; induction can proceed directly with intravenous oxytocin or amniotomy; 2) Bishop score <= 6: Unfavorable (unripe) cervix. Direct oxytocin induction carries a high failure rate and prolonged labor. Pre-induction cervical ripening with prostaglandins (dinoprostone PGE2 gel/insert or misoprostol PGE1) or mechanical dilators (Foley balloon catheter) is recommended prior to oxytocin.\n\nOption Review:\n- Option A is correct because a Bishop score >= 8 indicates a favorable cervix with a high success rate for labor induction.\n- Option B is incorrect because <= 4 represents an unfavorable, unripe cervix requiring cervical ripening.\n- Option C is incorrect because 5 is unfavorable.\n- Option D is incorrect because <= 2 represents a completely closed, posterior, firm cervix.\n\nKey Takeaway: A Bishop score >= 8 indicates a ripe, favorable cervix with a high probability of successful induction of labor with oxytocin.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q277",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Preeclampsia Diagnostic Criteria",
        "prompt": "A 26-year-old primigravida at 32 weeks of gestation presents for routine antenatal care. Her blood pressure is 150/95 mmHg on two occasions 4 hours apart. Urinalysis demonstrates 2+ protein (24-hour urine protein is 450 mg). She has no headache, visual disturbances, or epigastric pain. Platelet count is 210,000/microL and serum creatinine is 0.7 mg/dL. What hypertensive disorder of pregnancy is diagnosed?",
        "options": [
            "Preeclampsia without severe features",
            "Preeclampsia with severe features",
            "Gestational hypertension",
            "Chronic hypertension"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nPreeclampsia is defined as new-onset hypertension (systolic BP >= 140 mmHg and/or diastolic BP >= 90 mmHg on two occasions >= 4 hours apart) occurring AFTER 20 weeks of gestation in a previously normotensive woman, accompanied by either: 1) Proteinuria (>= 300 mg/24-hour urine collection, or protein-to-creatinine ratio >= 0.3, or dipstick 1+ to 2+); OR 2) In the absence of proteinuria, new-onset end-organ dysfunction (thrombocytopenia < 100,000, renal insufficiency with creatinine > 1.1, impaired liver enzymes, pulmonary edema, or new-onset visual/cerebral symptoms). In this patient, blood pressure >= 140/90 with confirmed proteinuria (>300 mg/24h) and absence of severe features (BP < 160/110, normal platelets, normal creatinine, no CNS symptoms) establishes the diagnosis of Preeclampsia without severe features.\n\nOption Review:\n- Option A is correct because new-onset hypertension and proteinuria after 20 weeks without end-organ damage defines preeclampsia without severe features.\n- Option B is incorrect because severe features require BP >= 160/110, platelets < 100,000, elevated transaminases, or neurological symptoms.\n- Option C is incorrect because gestational hypertension is hypertension after 20 weeks WITHOUT proteinuria or end-organ dysfunction.\n- Option D is incorrect because chronic hypertension is present prior to pregnancy or before 20 weeks of gestation.\n\nKey Takeaway: Preeclampsia is diagnosed by new-onset hypertension (>= 140/90) and proteinuria (>= 300 mg/24h) arising after 20 weeks of gestation.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q278",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Gynecology - Vaginitis Differential (Trichomonas vs Bacterial Vaginosis vs Candida)",
        "prompt": "A 26-year-old sexually active female presents with a profuse, malodorous, frothy, greenish-yellow vaginal discharge, accompanied by severe vulvar itching and dysuria. Speculum examination reveals marked erythema of the vaginal walls and punctate mucosal hemorrhages on the cervix ('strawberry cervix'). Wet mount microscopy of the discharge reveals motile, flagellated, pear-shaped protozoa with an undulating membrane. What is the diagnosis?",
        "options": [
            "Trichomoniasis",
            "Bacterial vaginosis",
            "Vulvovaginal candidiasis",
            "Chlamydia cervicitis"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nVaginitis is differentiated by characteristic discharge, physical signs, and wet mount findings: 1) Trichomoniasis (Trichomonas vaginalis): Sexually transmitted protozoan infection; presents with copious, malodorous, frothy, greenish-yellow discharge, vulvar irritation, vaginal pH > 4.5, punctate cervical petechial hemorrhages ('strawberry cervix' / colpitis macularis), and motile, flagellated trophozoites displaying jerky motility on saline wet mount. Treatment is oral metronidazole (2 g single dose or 500 mg twice daily for 7 days), with MANDATORY simultaneous treatment of sexual partners; 2) Bacterial Vaginosis (Gardnerella vaginalis): Thin, homogenous, grayish-white discharge, fishy odor on adding 10% KOH (positive Whiff test), vaginal pH > 4.5, and 'clue cells' (vaginal epithelial cells studded with bacteria, obscuring cell borders); 3) Vulvovaginal Candidiasis: Thick, white, curdy 'cottage cheese' discharge, pseudohyphae on 10% KOH, normal pH (<4.5).\n\nOption Review:\n- Option A is correct because frothy greenish-yellow discharge, strawberry cervix, and motile flagellated protozoa define trichomoniasis.\n- Option B is incorrect because bacterial vaginosis features grayish discharge, fishy odor, and clue cells without cervical petechiae.\n- Option C is incorrect because candidiasis produces thick cottage cheese discharge and pseudohyphae.\n- Option D is incorrect because Chlamydia is an intracellular bacterium causing mucopurulent cervicitis without flagellated protozoa.\n\nKey Takeaway: Trichomoniasis presents with frothy greenish discharge, a 'strawberry cervix', and motile flagellated protozoa on wet mount, requiring metronidazole therapy for both partners.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Trichomonas_vaginalis_phase_contrast.jpg/640px-Trichomonas_vaginalis_phase_contrast.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q279",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Obstetrics - Postpartum Uterine Inversion Management",
        "prompt": "Immediately following delivery of the placenta with vigorous umbilical cord traction and fundal pressure, a 28-year-old female develops severe lower abdominal pain, sudden massive postpartum hemorrhage, and profound neurogenic shock. On examination, the uterine fundus is absent from its normal position on abdominal palpation, and a large, dark-red, velvety mass protrudes through the dilated cervix into the vagina. What is the immediate first step in the manual management of acute uterine inversion?",
        "options": [
            "Immediate manual replacement of the fundus before administering uterotonics",
            "Immediate intravenous ergometrine infusion to contract the uterus",
            "Urgent surgical hysterectomy as the initial step",
            "Packing the vagina with gauze without repositioning"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAcute puerperal uterine inversion is a catastrophic obstetric emergency where the uterine fundus turns inside out and prolapses into the endometrial cavity or through the cervix into the vagina, most commonly provoked by excessive cord traction on an unseparated placenta combined with fundal pressure in an uncontracted uterus. Patients collapse in disproportionate neurogenic and hemorrhagic shock (due to peritoneal traction on ovaries and broad ligaments triggering profound vasovagal response). Management rules: 1) Immediate manual reduction (Johnson maneuver): The operator grasps the inverted fundus with the fingers in the posterior fornix and thumb anteriorly, applying steady upward pressure toward the umbilicus to reposition the fundus through the cervical constriction ring; 2) Crucial sequence: Manual reduction must be performed IMMEDIATELY before the cervical ring contracts around the fundus and BEFORE administering any uterotonics (uterotonics contract the constriction ring and trap the inverted fundus, making manual reduction impossible). Uterotonics are given only AFTER complete anatomical replacement is verified.\n\nOption Review:\n- Option A is correct because immediate manual replacement (Johnson maneuver) before administering uterotonics is the critical initial life-saving step.\n- Option B is incorrect because administering uterotonics before repositioning causes cervical spasm, locking the uterus in the inverted position.\n- Option C is incorrect because surgical approaches (Huntington or Haultain procedure) are reserved only if immediate manual reduction fails.\n- Option D is incorrect because vaginal packing does not reduce the inversion.\n\nKey Takeaway: Acute uterine inversion requires immediate manual replacement using the Johnson maneuver before administering any uterotonic agents.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q280",
        "subjectId": "obgyn",
        "subjectTitle": "Obstetrics & Gynecology",
        "topic": "Gynecologic Oncology - Complete Hydatidiform Mole Follow-Up",
        "prompt": "A 22-year-old female undergoes suction evacuation for a histologically confirmed complete hydatidiform mole. To monitor for the development of gestational trophoblastic neoplasia (invasive mole or choriocarcinoma), serial quantitative serum beta-hCG measurements are scheduled. What is the standard surveillance protocol for monitoring serum beta-hCG following molar evacuation?",
        "options": [
            "Weekly until three consecutive normal levels, then monthly for 6 months",
            "Monthly for 1 month then discharge from clinic",
            "Single measurement at 6 weeks post-evacuation only",
            "Daily measurements for 14 days then yearly"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nFollowing suction curettage of a complete hydatidiform mole, approximately 15% to 20% of patients progress to persistent Gestational Trophoblastic Neoplasia (GTN), either as an invasive mole (chorioadenoma destruens) or highly malignant choriocarcinoma. Serial quantitative measurement of serum beta-hCG is the definitive biomarker for post-molar surveillance. Standard protocol: 1) Measure serum beta-hCG every 1 to 2 weeks until levels become undetectable (<5 mIU/mL) for 3 consecutive weeks; 2) Once normal, continue monthly beta-hCG measurements for 6 consecutive months; 3) The patient must maintain strict, reliable contraception (oral contraceptive pills preferred; barrier methods acceptable) throughout the entire 6-month surveillance period to prevent pregnancy, which would elevate beta-hCG and confound disease monitoring. Persistent plateau or rising beta-hCG values diagnose GTN, warranting chemotherapy (methotrexate or actinomycin D).\n\nOption Review:\n- Option A is correct because weekly measurements until normal x3 followed by monthly monitoring for 6 months is the standard post-molar protocol.\n- Option B is incorrect because 1 month is inadequate to detect malignant transformation.\n- Option C is incorrect because a single test cannot establish a trend or monitor regression.\n- Option D is incorrect because daily testing is unnecessary and yearly fails to provide surveillance.\n\nKey Takeaway: Following molar evacuation, serum beta-hCG is monitored weekly until normal for 3 weeks, followed by monthly surveillance for 6 months with reliable contraception.",
        "imageUrls": []
    },

    # ==========================================
    # RADIOLOGY (5 Questions: Q281 - Q285)
    # ==========================================
    {
        "id": "fmge-gt1-q281",
        "subjectId": "radiology",
        "subjectTitle": "Radiodiagnosis",
        "topic": "Computed Tomography - Hounsfield Units Scale",
        "prompt": "On a diagnostic computed tomography (CT) scan of the abdomen, tissue density is quantitatively measured in Hounsfield Units (HU). The CT attenuation scale is standardized using the attenuation values of air and pure water. What is the baseline Hounsfield Unit value assigned to pure water under standard conditions?",
        "options": [
            "0 Hounsfield Units",
            "-1,000 Hounsfield Units",
            "+1,000 Hounsfield Units",
            "+100 Hounsfield Units"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe Hounsfield Unit (HU) scale is a linear transformation of the original linear attenuation coefficient measurement in computed tomography, calibrated against standard reference substances: 1) Pure water is arbitrarily defined as 0 HU at standard temperature and pressure; 2) Air has the lowest attenuation, defined as -1,000 HU; 3) Fat displays negative attenuation, typically -50 to -100 HU; 4) Soft tissues (muscle, liver, spleen) range from +30 to +60 HU; 5) Acute clotted blood ranges from +60 to +80 HU; 6) Dense cortical bone has high attenuation, ranging from +700 to +1,000+ HU.\n\nOption Review:\n- Option A is correct because pure water is defined as 0 HU on the CT attenuation scale.\n- Option B is incorrect because -1,000 HU is the designated value for air.\n- Option C is incorrect because +1,000 HU corresponds to dense cortical bone.\n- Option D is incorrect because +100 HU represents high-density hematoma or contrast enhancement.\n\nKey Takeaway: On the CT Hounsfield scale, pure water is defined as 0 HU, air is -1,000 HU, and dense bone is +1,000 HU.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q282",
        "subjectId": "radiology",
        "subjectTitle": "Radiodiagnosis",
        "topic": "Chest Radiology - Silhouette Sign",
        "prompt": "An upright chest radiograph in a 55-year-old male with acute pneumonia demonstrates an area of homogeneous alveolar consolidation that completely obscures and blurs the sharp radiographic contour of the right heart border, while the right hemidiaphragm remains clearly visible. In which anatomical lobe of the lung is the consolidation located?",
        "options": [
            "Right middle lobe",
            "Right lower lobe",
            "Right upper lobe",
            "Left lingula"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe 'silhouette sign' (Felson's silhouette sign) is a fundamental radiological principle: the normal radiographic border between two adjacent anatomical structures is formed because they have different radiodensities (e.g., water-density right atrium silhouetted against air-density adjacent lung). When lung parenchyma adjacent to a cardiovascular border becomes opacified (by consolidation, atelectasis, fluid, or mass), the density difference is lost, and the normal border becomes obscured or obliterated: 1) Loss of the right heart border: Indicates disease in the right middle lobe (medial segment, which anatomically abuts the right atrium); 2) Loss of the right hemidiaphragm: Indicates disease in the right lower lobe (which sits atop the diaphragm); 3) Loss of the left heart border: Indicates disease in the lingular segments of the left upper lobe.\n\nOption Review:\n- Option A is correct because the right middle lobe anatomically abuts the right heart border; its consolidation eliminates the right cardiac silhouette.\n- Option B is incorrect because right lower lobe consolidation obliterates the right hemidiaphragm, not the right heart border.\n- Option C is incorrect because right upper lobe consolidation does not contact the cardiac silhouette.\n- Option D is incorrect because the lingula abuts the left heart border.\n\nKey Takeaway: Obliteration of the right cardiac border on a frontal chest radiograph (positive silhouette sign) localizes the consolidation to the right middle lobe.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q283",
        "subjectId": "radiology",
        "subjectTitle": "Radiodiagnosis",
        "topic": "Magnetic Resonance Imaging - T1 vs T2 Signal Characteristics",
        "prompt": "A radiologist reviews an MRI of the brain in a patient with suspected multiple sclerosis. On T1-weighted images, cerebrospinal fluid inside the cerebral ventricles appears dark (hypointense), while white matter appears hyperintense relative to gray matter. On T2-weighted images, what is the signal intensity of fluid-containing structures such as cerebrospinal fluid (CSF)?",
        "options": [
            "Hyperintense signal",
            "Hypointense signal",
            "Isointense signal",
            "Signal void"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nMagnetic Resonance Imaging (MRI) relies on radiofrequency pulse sequences and relaxation times (T1 and T2) of hydrogen protons in tissue water and fat: 1) T1-weighted imaging: Short repetition time (TR) and short echo time (TE). Tissues with high fat content (myelinated white matter, subcutaneous fat) have short T1 relaxation times and appear bright (hyperintense). Water and fluid (CSF, urine, edema) have long T1 times and appear dark (hypointense). T1 is ideal for anatomical detail; 2) T2-weighted imaging: Long TR and long TE. Water and free fluid have long T2 relaxation times and appear bright (hyperintense, 'H2O is bright on T2'). Fat appears relatively intermediate/dark. T2 is ideal for detecting pathology, edema, demyelination, and inflammation.\n\nOption Review:\n- Option A is correct because water and CSF appear bright (hyperintense) on T2-weighted MRI sequences.\n- Option B is incorrect because water is dark (hypointense) on T1-weighted images.\n- Option C is incorrect because intermediate signal is seen in solid parenchyma.\n- Option D is incorrect because signal void is produced by cortical bone and rapid flow in patent blood vessels.\n\nKey Takeaway: On MRI, fluid and CSF appear dark (hypointense) on T1-weighted images and bright (hyperintense) on T2-weighted images.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q284",
        "subjectId": "radiology",
        "subjectTitle": "Radiodiagnosis",
        "topic": "Ultrasound Physics - Acoustic Shadowing vs Enhancement",
        "prompt": "During an abdominal ultrasound of the right upper quadrant, an echogenic focus measuring 12 mm is identified inside the gallbladder lumen. Immediately deep to this echogenic structure, there is a band-like dark region characterized by an absence of reflected ultrasound sound waves. What acoustic artifact confirms the presence of a true calcified gallstone?",
        "options": [
            "Posterior acoustic shadowing",
            "Posterior acoustic enhancement",
            "Mirror-image artifact",
            "Ring-down reverberation artifact"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIn diagnostic ultrasonography, artifacts are produced by physical interactions of sound waves with tissues: 1) Posterior Acoustic Shadowing: Occurs when the ultrasound beam encounters a highly reflective or highly attenuating structure (such as a calcified gallstone, renal calculus, or dense bone). Nearly all sound energy is either reflected back or absorbed at the anterior interface. Consequently, virtually no acoustic waves penetrate into deeper tissues, casting a dark, anechoic band (acoustic shadow) behind the object. This shadow is an essential diagnostic feature confirming a true calculus; 2) Posterior Acoustic Enhancement: Occurs behind low-attenuation fluid structures (cysts, full bladder, gallbladder lumen). Because sound passes through fluid with minimal attenuation, tissues deep to the fluid receive stronger sound waves and appear falsely bright (enhanced); 3) Mirror artifact: Occurs across specular reflectors (diaphragm).\n\nOption Review:\n- Option A is correct because posterior acoustic shadowing is an anechoic shadow cast behind dense attenuating structures like gallstones.\n- Option B is incorrect because posterior acoustic enhancement produces increased brightness behind fluid cysts.\n- Option C is incorrect because mirror-image artifacts duplicate lesions across the diaphragm.\n- Option D is incorrect because ring-down artifacts are caused by gas bubbles in the bowel.\n\nKey Takeaway: Posterior acoustic shadowing is an anechoic dark zone behind a reflective or dense structure that serves as a hallmark of gallstones and renal calculi.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Gallstone_ultrasound.jpg/640px-Gallstone_ultrasound.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q285",
        "subjectId": "radiology",
        "subjectTitle": "Radiodiagnosis",
        "topic": "Radiation Protection - Radiation Units & ALARA Principles",
        "prompt": "In diagnostic radiology and occupational radiation safety, radiation dose is quantified using standardized physical and biological units. Which international standard unit measures the 'equivalent dose' and 'effective dose' of ionizing radiation, taking into account the relative biological effectiveness of different radiation types on human tissues?",
        "options": [
            "Sievert",
            "Gray",
            "Becquerel",
            "Roentgen"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nStandardized units of ionizing radiation quantify distinct physical and biological properties: 1) Absorbed Dose (Gray, Gy): The amount of physical energy deposited by ionizing radiation per unit mass of matter (1 Gy = 1 Joule per kilogram). It reflects physical energy absorbed, regardless of biological damage; 2) Equivalent Dose & Effective Dose (Sievert, Sv): Takes the absorbed dose (Gy) and multiplies it by a radiation weighting factor (WR) to account for biological harm from different radiation types (e.g., alpha particles do 20x more damage than X-rays for the same Gy), and a tissue weighting factor (WT) to reflect organ susceptibility. The Sievert (or millisievert, mSv) is the standard international unit for radiation protection and regulatory occupational dose limits; 3) Becquerel (Bq): Unit of radioactivity (1 disintegration/second); 4) Roentgen (R): Historical unit measuring air ionization.\n\nOption Review:\n- Option A is correct because the Sievert (Sv) is the unit of equivalent dose and effective biological dose.\n- Option B is incorrect because the Gray (Gy) measures physical absorbed dose without biological weighting.\n- Option C is incorrect because the Becquerel measures radioactivity source activity.\n- Option D is incorrect because the Roentgen is a legacy unit for exposure in air.\n\nKey Takeaway: The Sievert (Sv) is the unit of equivalent and effective radiation dose, measuring the biological effect of ionizing radiation on human tissues.",
        "imageUrls": []
    },

    # ==========================================
    # RADIOTHERAPY (5 Questions: Q286 - Q290)
    # ==========================================
    {
        "id": "fmge-gt1-q286",
        "subjectId": "radiotherapy",
        "subjectTitle": "Radiotherapy",
        "topic": "Radiation Oncology - Brachytherapy",
        "prompt": "A 48-year-old female with Stage IIB cervical cancer receives external beam radiotherapy followed by intracavitary brachytherapy using an intrauterine tandem and vaginal ovoids. What is the defining characteristic that distinguishes brachytherapy from external beam teletherapy?",
        "options": [
            "Placing a sealed radioactive source directly inside or immediately adjacent to the tumor target",
            "Directing high-energy megavoltage X-rays from a linear accelerator located 100 cm away",
            "Administering systemic unsealed oral radionuclides that circulate throughout the bloodstream",
            "Delivering non-ionizing focused ultrasound energy to induce thermal tissue ablation"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nRadiation therapy modalities are categorized based on the geometry between the radiation source and the patient: 1) Teletherapy (External Beam Radiotherapy / EBRT): The radiation source is positioned at a distance from the patient (typically 80 to 100 cm), generated by a linear accelerator (LINAC, producing megavoltage photons or electrons) or Cobalt-60 teletherapy unit; 2) Brachytherapy ('short-distance' radiotherapy): Sealed radioactive isotope sources (e.g., Iridium-192, Cesium-137, Iodine-125) are placed directly inside (interstitial, e.g., prostate/breast), within body cavities (intracavitary, e.g., cervical tandem and ovoids), or on the surface of the tumor. Because radiation intensity decreases exponentially with the square of the distance (the inverse-square law: I = 1/d2), brachytherapy delivers a very high radiation dose directly to the tumor while sparing adjacent critical normal organs (bladder and rectum in cervical cancer).\n\nOption Review:\n- Option A is correct because placing sealed radioactive sources within or adjacent to the tumor defines brachytherapy.\n- Option B is incorrect because delivering radiation from a distant linear accelerator defines teletherapy.\n- Option C is incorrect because unsealed systemic radioisotopes define systemic metabolic radionuclide therapy (e.g., Iodine-131 for thyroid cancer).\n- Option D is incorrect because focused ultrasound is thermal ablation, not ionizing radiotherapy.\n\nKey Takeaway: Brachytherapy involves placing sealed radioactive sources directly inside or adjacent to the tumor, exploiting the inverse-square law to deliver high local doses with rapid fall-off.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q287",
        "subjectId": "radiotherapy",
        "subjectTitle": "Radiotherapy",
        "topic": "Radiobiology - The 4 Rs of Radiobiology",
        "prompt": "In clinical radiation oncology, total curative radiation doses (e.g., 60 to 70 Gray) are delivered in multiple small daily fractions (e.g., 2 Gray per fraction, 5 days per week over 6 to 7 weeks) rather than as a single massive dose. Fractionation exploits the classic '4 Rs' of radiobiology. Which mechanism allows surviving normal tissues to mend sublethal DNA damage between daily radiation fractions?",
        "options": [
            "Repair of sublethal DNA damage",
            "Repopulation of surviving clonogens",
            "Redistribution through the cell cycle",
            "Reoxygenation of hypoxic tumor cells"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe biological rationale for fractionating radiation doses is governed by the '4 Rs' of radiobiology: 1) Repair: Normal healthy cells have superior enzymatic mechanisms to repair sublethal DNA double-strand breaks compared to cancer cells. Providing an interval of >= 6 to 24 hours between fractions allows normal tissues to repair sublethal damage; 2) Redistribution: Cells in resistant phases (S-phase) progress into radiosensitive phases (G2/M) by the time of the next fraction; 3) Reoxygenation: Hypoxic tumor cells (which are 2.5 to 3 times more radioresistant due to lack of the oxygen fixation effect) become reoxygenated as the outer aerobic tumor layer shrinks, restoring radiosensitivity; 4) Repopulation: Surviving tumor and normal stem cells proliferate during the treatment course. Fractionation spares normal tissues through Repair, while killing cancer cells through Reoxygenation and Redistribution.\n\nOption Review:\n- Option A is correct because repair of sublethal DNA damage in normal cells between fractions is the primary protective effect of fractionation.\n- Option B is incorrect because repopulation refers to cell division during prolonged treatment courses.\n- Option C is incorrect because redistribution moves tumor cells into radiosensitive G2/M phases.\n- Option D is incorrect because reoxygenation enhances tumor kill by overcoming hypoxia.\n\nKey Takeaway: The 4 Rs of radiobiology (Repair, Redistribution, Reoxygenation, Repopulation) explain the therapeutic advantage of fractionated radiotherapy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q288",
        "subjectId": "radiotherapy",
        "subjectTitle": "Radiotherapy",
        "topic": "Radiobiology - Radiosensitivity of Malignancies",
        "prompt": "Different human neoplasms exhibit widely variable intrinsic sensitivity to ionizing radiation, governed by Bergonie and Tribondeau's law of radiobiology. Based on intrinsic radioresponsiveness, which of the following malignancies is classified as exquisitely radiosensitive?",
        "options": [
            "Testicular seminoma",
            "Osteosarcoma",
            "Renal cell carcinoma",
            "Malignant melanoma"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe radiosensitivity of tumors is broadly classified into three categories based on the radiation dose required for eradication: 1) Exquisitely Radiosensitive (cured by doses < 30 to 40 Gy): Germ cell tumors (Testicular seminoma, Ovarian dysgerminoma), Hematological malignancies (Hodgkin and non-Hodgkin lymphoma, Leukemia, Myeloma), Neuroblastoma, and Wilms tumor; 2) Moderately Radiosensitive (require doses of 50 to 70 Gy): Epithelial carcinomas (Squamous cell carcinomas of head/neck, cervix, and esophagus; Adenocarcinomas of breast, prostate, lung, and rectum); 3) Radioresistant (require doses > 70 Gy, poorly responsive to standard radiotherapy): Osteosarcoma, Chondrosarcoma, Soft tissue sarcomas, Malignant melanoma, and Renal cell carcinoma. Testicular seminoma is famously cured with very low doses (~20 to 25 Gy).\n\nOption Review:\n- Option A is correct because testicular seminoma is one of the most exquisitely radiosensitive solid tumors in humans.\n- Option B is incorrect because osteosarcoma is highly radioresistant and primarily treated with surgery and chemotherapy.\n- Option C is incorrect because renal cell carcinoma is notoriously radioresistant.\n- Option D is incorrect because melanoma has high capacity for sublethal damage repair and is radioresistant.\n\nKey Takeaway: Testicular seminoma and lymphomas are exquisitely radiosensitive tumors that respond to low doses of ionizing radiation.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q289",
        "subjectId": "radiotherapy",
        "subjectTitle": "Radiotherapy",
        "topic": "Radiotherapy Toxicity - Acute vs Late Complications",
        "prompt": "A 54-year-old male receives definitive external beam radiotherapy (70 Gray) combined with concurrent cisplatin for locally advanced squamous cell carcinoma of the tonsil. Both parotid glands receive a mean dose exceeding 30 Gray. Within weeks, he develops persistent, severe dryness of the mouth (xerostomia), loss of taste, and rampant dental caries. What is the primary cause of chronic radiation-induced xerostomia in head and neck cancer patients?",
        "options": [
            "Radiation-induced apoptosis and fibrosis of parotid serous acinar cells",
            "Autoimmune destruction of minor sublingual salivary glands",
            "Bilateral transection of the chorda tympani nerves",
            "Complete pharmacological blockade of muscarinic M3 receptors"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nXerostomia (dry mouth) is the most frequent and debilitating long-term complication of head and neck radiotherapy. The major salivary glands (especially the parotid glands, which produce ~60% to 65% of total saliva, rich in serous watery secretion) are highly radiosensitive. Serous acinar cells in the parotid glands undergo early, dose-dependent interphase cell death (apoptosis) at relatively low radiation doses. Doses exceeding a mean threshold of 26 to 30 Gray cause irreversible loss of functioning acinar tissue, microvascular endarteritis, and progressive parenchymal fibrosis. Salivary flow drops by >80%, altering oral flora, predisposing to rapid cervical dental caries and oral candidiasis, and causing severe difficulty in mastication and deglutition. Modern Intensity-Modulated Radiotherapy (IMRT) is designed to spare the contralateral parotid gland below the 26 Gy threshold.\n\nOption Review:\n- Option A is correct because radiation causes apoptosis and irreversible fibrosis of parotid serous acini when threshold doses are exceeded.\n- Option B is incorrect because the primary damage is direct ionizing radiation toxicity, not an autoimmune disease.\n- Option C is incorrect because neural transection does not occur from radiation.\n- Option D is incorrect because radiation physically destroys parenchymal glands rather than pharmacologically blocking receptors.\n\nKey Takeaway: Parotid-sparing IMRT is utilized in head and neck cancers to keep mean parotid doses below 26 Gray to prevent permanent radiation-induced xerostomia.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q290",
        "subjectId": "radiotherapy",
        "subjectTitle": "Radiotherapy",
        "topic": "Radiotherapy Physics - Linear Accelerators & Beam Types",
        "prompt": "In modern radiotherapy departments, Linear Accelerators (LINACs) are used to generate both high-energy megavoltage photon beams (X-rays) and electron beams. In which clinical scenario are electron beams specifically preferred over high-energy photon beams?",
        "options": [
            "Treating superficial skin lesions while sparing deeper normal tissues",
            "Treating deep-seated pelvic malignancies such as prostate cancer",
            "Treating retroperitoneal sarcomas lying anterior to the spine",
            "Treating central non-small cell lung carcinomas"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe choice between photon and electron radiation beams depends on their physical depth-dose profiles: 1) Megavoltage Photon Beams (X-rays, 6 to 18 MV): Have a 'skin-sparing' effect (peak dose occurs 1.5 to 3.5 cm beneath the skin surface) and high tissue penetration, continuing through the body with an exit dose. Photons are used for deep-seated visceral tumors (prostate, lung, cervix, esophagus, brain); 2) Electron Beams (6 to 20 MeV): Charged particles that deliver a high surface dose and travel a finite, predictable depth in tissue (therapeutic range in cm is approximately equal to energy in MeV divided by 3), after which there is a rapid, steep dose fall-off with negligible exit dose to deeper structures. Consequently, electron beams are the ideal modality for superficial tumors (cutaneous squamous cell carcinoma, basal cell carcinoma, keloids, mycosis fungoides, chest wall boost following mastectomy) where underlying critical structures (heart, lung) must be spared.\n\nOption Review:\n- Option A is correct because electron beams deliver high surface doses with rapid fall-off, making them ideal for superficial skin cancers.\n- Option B is incorrect because deep prostate cancers require deeply penetrating high-energy photon beams.\n- Option C is incorrect because retroperitoneal tumors require photon beams.\n- Option D is incorrect because central lung tumors require penetrating photon therapy.\n\nKey Takeaway: Electron beams are preferred for treating superficial lesions because they have a finite range with rapid dose fall-off, sparing underlying deep organs.",
        "imageUrls": []
    },

    # ==========================================
    # OPHTHALMOLOGY (5 Questions: Q291 - Q295)
    # ==========================================
    {
        "id": "fmge-gt1-q291",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Pediatric Ophthalmology - Retinoblastoma",
        "prompt": "An 18-month-old male infant is brought to the eye clinic after his parents notice a yellowish-white pupillary reflex in his left eye on flash photography ('cat's eye reflex' / leukocoria). Fundoscopy reveals a calcified, cream-colored retinal mass. Histopathological examination demonstrates pathognomonic Flexner-Wintersteiner rosettes. Which tumor suppressor gene on chromosome 13q14 is mutated in this primary intraocular malignancy of childhood?",
        "options": [
            "RB1 gene",
            "WT1 gene",
            "NF1 gene",
            "VHL gene"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nRetinoblastoma is the most common primary intraocular malignancy of childhood, arising from neuroepithelial cells of the developing retina. It serves as Knudson's classic prototype for the 'two-hit' hypothesis of tumorigenesis, caused by biallelic loss-of-function mutations in the RB1 tumor suppressor gene located on chromosome 13q14. The RB protein normally binds and sequesters the E2F transcription factor, inhibiting cell cycle progression past the G1/S checkpoint. The cardinal presenting sign in >60% of cases is leukocoria (white pupillary reflex, 'cat's eye reflex'), followed by strabismus. Histopathology demonstrates Flexner-Wintersteiner rosettes: pathognomonic clusters of cuboidal or columnar tumor cells arranged around a central clear lumen containing cytoplasmic extensions, representing early photoreceptor differentiation. Enucleation or systemic chemotherapy with focal laser therapy is utilized.\n\nOption Review:\n- Option A is correct because biallelic inactivation of the RB1 gene on chromosome 13q14 causes retinoblastoma.\n- Option B is incorrect because WT1 gene mutations on 11p cause Wilms tumor.\n- Option C is incorrect because NF1 mutations on 17q cause neurofibromatosis type 1 (Lisch nodules).\n- Option D is incorrect because VHL mutations on 3p cause retinal hemangioblastomas in Von Hippel-Lindau disease.\n\nKey Takeaway: Retinoblastoma is caused by mutations in the RB1 tumor suppressor gene on chromosome 13q14, presenting with leukocoria and Flexner-Wintersteiner rosettes.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Retinoblastoma_leukocoria.jpg/640px-Retinoblastoma_leukocoria.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q292",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Uveitis - Sympathetic Ophthalmia",
        "prompt": "A 30-year-old construction worker suffers an accidental penetrating trauma to his right eye involving the ciliary body (the 'exciting eye'). Three weeks later, while the injured eye remains inflamed, he develops sudden pain, photophobia, ciliary injection, and reduced vision in his previously uninjured left eye (the 'sympathizing eye'). Fundoscopy of the sympathizing eye reveals multiple yellow-white Dalen-Fuchs nodules in the choroid. What is the immunological mechanism of sympathetic ophthalmia?",
        "options": [
            "Autoimmune T-cell-mediated granulomatous panuveitis triggered by sequestered uveal antigens",
            "Direct intraocular bacterial endophthalmitis spreading across the optic chiasm",
            "Type I IgE-mediated anaphylactic reaction against lens crystallins",
            "Circulating immune complex vasculitis deposited in retinal vessels"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nSympathetic ophthalmia is a rare, bilateral, non-necrotizing granulomatous panuveitis that develops following penetrating trauma (or less commonly intraocular surgery) involving uveal tissue (particularly the ciliary body) of one eye (the 'exciting' eye). In normal physiology, intraocular uveal and retinal antigens are sequestered behind the blood-ocular barrier and shielded by ocular immune privilege. Mechanical disruption of the uveal tract exposes sequestered uveal antigens (e.g., melanin-associated proteins, retinal S-antigen) to regional lymph nodes, breaking self-tolerance. Autoreactive CD4+ T-lymphocytes are primed and cross-react with identical antigens in the uninjured contralateral eye (the 'sympathizing' eye), typically 2 weeks to 3 months later. Histology reveals diffuse lymphocytic infiltration of the uveal tract with Dalen-Fuchs nodules (epithelioid histiocytes beneath the retinal pigment epithelium). Prompt enucleation of a blind, severely traumatized exciting eye within 2 weeks of injury prevents sympathetic ophthalmia in the fellow eye.\n\nOption Review:\n- Option A is correct because sympathetic ophthalmia is an autoimmune T-cell-mediated granulomatous uveitis triggered by exposed sequestered uveal antigens.\n- Option B is incorrect because sympathetic ophthalmia is sterile and does not represent bacterial spread.\n- Option C is incorrect because lens-induced endophthalmitis involves lens proteins, not sympathetic uveitis.\n- Option D is incorrect because immune complex deposition causes retinal vasculitis (Behcet disease, SLE), not Dalen-Fuchs panuveitis.\n\nKey Takeaway: Sympathetic ophthalmia is a bilateral granulomatous panuveitis triggered by autoimmune T-cell response to sequestered uveal antigens exposed by trauma to the ciliary body.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q293",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Retina - Central Retinal Vein Occlusion (CRVO)",
        "prompt": "A 68-year-old male with long-standing hypertension and primary open-angle glaucoma presents with sudden, painless, severe reduction in vision in his right eye. Visual acuity is 20/200. Dilated fundoscopic examination demonstrates marked engorgement and tortuosity of all retinal veins, extensive flame-shaped and blot retinal hemorrhages in all four quadrants, cotton-wool spots, and optic disc edema, producing a dramatic 'blood and thunder' fundus appearance. What is the diagnosis?",
        "options": [
            "Central retinal vein occlusion",
            "Central retinal artery occlusion",
            "Anterior ischemic optic neuropathy",
            "Proliferative vitreoretinopathy"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nCentral Retinal Vein Occlusion (CRVO) is a major retinal vascular disorder, typically precipitated by thrombotic occlusion of the central retinal vein at or behind the lamina cribrosa, commonly provoked by an atherosclerotic central retinal artery compressing the adjacent vein in a shared adventitial sheath. Risk factors include advanced age, hypertension, diabetes mellitus, and elevated intraocular pressure (glaucoma). Obstruction of venous outflow leads to massive capillary engorgement, increased venous hydrostatic pressure, and widespread extravasation of blood throughout the retina. The pathognomonic fundoscopic appearance is termed the 'blood and thunder' or 'splashed tomato' fundus: marked venous dilatation and tortuosity with dense, flame-shaped and blot hemorrhages scattered across all four quadrants of the retina, accompanied by optic disc swelling and macular edema. A major complication of ischemic CRVO is neovascular glaucoma developing approximately 90 days later ('100-day glaucoma').\n\nOption Review:\n- Option A is correct because the 'blood and thunder' fundus with four-quadrant retinal hemorrhages is diagnostic of central retinal vein occlusion (CRVO).\n- Option B is incorrect because central retinal artery occlusion (CRAO) displays a pale, milky-white retina with a cherry-red spot in the fovea.\n- Option C is incorrect because anterior ischemic optic neuropathy produces pale, swollen disc without widespread four-quadrant hemorrhages.\n- Option D is incorrect because proliferative vitreoretinopathy presents with tractional retinal folds following retinal detachment.\n\nKey Takeaway: Central retinal vein occlusion (CRVO) characteristically produces a 'blood and thunder' fundus featuring diffuse retinal hemorrhages across all four quadrants.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Central_retinal_vein_occlusion.jpg/640px-Central_retinal_vein_occlusion.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q294",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Neuro-Ophthalmology - Relative Afferent Pupillary Defect",
        "prompt": "A 28-year-old female presents with subacute painful vision loss in her right eye that worsens with eye movements, consistent with acute optic neuritis. During pupillary evaluation with the swinging flashlight test, when the light beam is moved from the normal left eye to the affected right eye, both pupils paradoxically dilate rather than constrict. What is this classic clinical sign of an incomplete optic nerve lesion called?",
        "options": [
            "Marcus Gunn pupil",
            "Argyll Robertson pupil",
            "Adie tonic pupil",
            "Horner pupil"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nA Relative Afferent Pupillary Defect (RAPD / Marcus Gunn pupil) is an objective physical sign of asymmetric afferent conduction pathway disease anterior to the optic chiasm, most commonly due to unilateral optic neuritis or severe retinal disease (ischemic CRAO/CRVO, extensive retinal detachment). In the swinging flashlight test: When light shines into the normal eye, intact afferents (CN II) send bilateral signals via the pretectal nuclei and Edinger-Westphal nuclei (CN III), causing brisk consensual and direct pupillary constriction in both eyes. When the light is rapidly swung to the diseased eye, the damaged optic nerve conducts a substantially weaker light stimulus than the normal eye just received. The brainstem interprets this as a reduction in overall light intensity, causing both pupils to paradoxically dilate. The direct light reflex in the affected eye is weaker than the consensual light reflex evoked by the normal eye.\n\nOption Review:\n- Option A is correct because paradoxical pupillary dilation during the swinging flashlight test confirms a Marcus Gunn pupil (RAPD).\n- Option B is incorrect because Argyll Robertson pupil features light-near dissociation (constricts to accommodation but fails to react to light, seen in neurosyphilis).\n- Option C is incorrect because Adie tonic pupil is an unreactive dilated pupil due to postganglionic parasympathetic ciliary ganglion denervation.\n- Option D is incorrect because Horner pupil is a small (miotic) pupil with ptosis due to sympathetic disruption.\n\nKey Takeaway: A Marcus Gunn pupil (Relative Afferent Pupillary Defect) is detected by the swinging flashlight test, demonstrating paradoxical dilation of both pupils when light shines on the affected eye.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q295",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Strabismus & Amblyopia - Amblyopia Management",
        "prompt": "A 4-year-old boy is brought to the ophthalmology clinic with an inward deviation of his left eye (esotropia). Cycloplegic refraction reveals normal vision (20/20) in the right eye, but best-corrected visual acuity in the left eye is reduced to 20/100, with no organic ocular pathology on dilated examination. Strabismic amblyopia ('lazy eye') is diagnosed. What is the gold-standard first-line treatment to stimulate visual cortex development in the amblyopic eye during this critical sensitive period?",
        "options": [
            "Occlusion therapy of the dominant sound right eye",
            "Immediate bilateral extraocular muscle resection surgery",
            "Topical atropine drops administered into the amblyopic left eye",
            "High-dose systemic corticosteroid therapy"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAmblyopia is a unilateral (or rarely bilateral) reduction of best-corrected visual acuity resulting from abnormal visual experience during the critical period of early visual cortical development (birth to 7-8 years of age), caused by strabismus, anisometropia (refractive difference), or visual deprivation (congenital cataract, ptosis). In strabismic amblyopia, the visual cortex actively suppresses the blurred or misaligned foveal image from the deviating eye to prevent diplopia and visual confusion, leading to permanent underdevelopment of ocular dominance columns in the striate cortex (area 17). The gold-standard treatment (initiated after correcting refractive errors) is Occlusion (patching) therapy of the sound (dominant, fellow) eye for prescribed hours per day (2 to 6 hours daily). Patching eliminates visual input from the sound eye, forcing the visual cortex to process visual stimuli from the amblyopic eye, thereby stimulating neural plasticity and restoring visual acuity.\n\nOption Review:\n- Option A is correct because patching (occlusion) of the sound, dominant eye forces use of the amblyopic eye and restores cortical vision.\n- Option B is incorrect because strabismus surgery realigns the ocular axes, but does not cure the cortical sensory amblyopia; patching must precede surgery.\n- Option C is incorrect because atropine penalization is instilled into the SOUND eye (to blur its near vision), not the amblyopic eye.\n- Option D is incorrect because corticosteroids have zero role in amblyopia.\n\nKey Takeaway: Occlusion (patching) of the sound dominant eye is the gold-standard treatment for amblyopia during early childhood.",
        "imageUrls": []
    },

    # ==========================================
    # ENT (EAR, NOSE, THROAT) (5 Questions: Q296 - Q300)
    # ==========================================
    {
        "id": "fmge-gt1-q296",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Otology - Vestibular Schwannoma (Acoustic Neuroma)",
        "prompt": "A 45-year-old male presents with slowly progressive, unilateral sensorineural hearing loss in his left ear for 2 years, accompanied by left-sided high-frequency tinnitus and poor speech discrimination out of proportion to pure-tone thresholds. Physical examination demonstrates an absent left corneal reflex. Brain MRI demonstrates an intensely enhancing mass centered at the left cerebellopontine angle with widening and 'trumpet-shaped' flaring of the internal acoustic meatus. From which nerve sheath does this benign tumor arise?",
        "options": [
            "Vestibular nerve",
            "Facial nerve",
            "Trigeminal nerve",
            "Glossopharyngeal nerve"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nVestibular schwannoma (commonly misnamed 'acoustic neuroma') is a benign, slow-growing, encapsulated neoplasm derived from Schwann cells of the sheath of the eighth cranial nerve (specifically the superior or inferior vestibular nerve at the glial-Schwannian junction within the internal auditory canal / meatus). Early symptoms include unilateral, progressive, high-frequency sensorineural hearing loss, tinnitus, and poor speech discrimination. As the tumor expands medially into the cerebellopontine (CP) angle, it compresses adjacent cranial nerves: 1) Trigeminal nerve (CN V): Earliest physical sign is depression or loss of the corneal reflex (sensory V1 limb) and facial hypoesthesia; 2) Facial nerve (CN VII): Hypoesthesia of the posterior external auditory canal wall (Hitselberger sign) and late facial paresis; 3) Cerebellum and brainstem: Ataxia and hydrocephalus. Contrast-enhanced MRI with thin cuts through the internal auditory canal is the diagnostic gold standard, revealing 'ice-cream cone' widening of the porus acusticus.\n\nOption Review:\n- Option A is correct because vestibular schwannomas originate from Schwann cells of the vestibular division of the vestibulocochlear nerve (CN VIII).\n- Option B is incorrect because facial neuromas are much rarer and present with early facial muscle paresis.\n- Option C is incorrect because trigeminal schwannomas arise from the middle cranial fossa / Meckel's cave.\n- Option D is incorrect because glossopharyngeal tumors arise at the jugular foramen.\n\nKey Takeaway: Vestibular schwannoma arises from the vestibular nerve sheath inside the internal auditory canal, presenting with unilateral sensorineural hearing loss and loss of the corneal reflex.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Vestibular_schwannoma_MRI.jpg/640px-Vestibular_schwannoma_MRI.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q297",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Otology - Malignant (Necrotizing) Otitis Externa",
        "prompt": "A 72-year-old poorly controlled diabetic male presents with severe, unrelenting, deep-seated otalgia in his right ear that radiates to the temporomandibular joint and worsens at night, accompanied by foul-smelling purulent otorrhea. Otoscopy reveals granulation tissue at the bone-cartilage junction of the external auditory canal floor. High-resolution CT shows skull base osteomyelitis. What bacterial pathogen is responsible for malignant (necrotizing) otitis externa in over 90% of cases?",
        "options": [
            "Pseudomonas aeruginosa",
            "Staphylococcus aureus",
            "Streptococcus pneumoniae",
            "Aspergillus fumigatus"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nMalignant (necrotizing) otitis externa is a life-threatening, aggressive, invasive infection of the external auditory canal that spreads to cause skull base osteomyelitis, occurring almost exclusively in elderly diabetic or immunocompromised individuals. Pseudomonas aeruginosa is the causative pathogen in >90% to 95% of cases. The infection originates in the external canal and spreads through the fissures of Santorini and the osseocartilaginous junction into the temporal bone, stylomastoid foramen, and jugular foramen, leading to cranial neuropathies (CN VII facial nerve palsy in ~30%, followed by CN IX, X, XI, and XII palsies). Diagnostic hallmark: Granulation tissue at the junction of the osseous and cartilaginous canal floor. Technetium-99m bone scanning confirms osteomyelitis, and Gallium-67 scan monitors therapeutic response. Treatment requires long-term parenteral antipseudomonal antibiotics (ciprofloxacin, ceftazidime, or piperacillin-tazobactam) for 6 to 12 weeks.\n\nOption Review:\n- Option A is correct because Pseudomonas aeruginosa is the overwhelming primary pathogen causing malignant otitis externa.\n- Option B is incorrect because S. aureus causes localized furuncles of the outer third of the canal, not invasive skull base osteomyelitis.\n- Option C is incorrect because S. pneumoniae causes acute otitis media of the middle ear.\n- Option D is incorrect because Aspergillus causes fungal otomycosis without skull base osteomyelitis.\n\nKey Takeaway: Malignant otitis externa is caused by Pseudomonas aeruginosa in elderly diabetics, characterized by granulation tissue at the bone-cartilage junction and skull base osteomyelitis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q298",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Rhinology - Nasal Polyps (Antrochoanal vs Ethmoidal)",
        "prompt": "A 16-year-old male presents with progressive unilateral right-sided nasal obstruction and snoring. Anterior and posterior rhinoscopy reveals a smooth, pale, glistening, insensitive, pedunculated mass originating from the maxillary antrum, passing through the accessory maxillary ostium into the nasal cavity, and hanging down into the nasopharynx through the posterior choana. What type of solitary nasal polyp is present?",
        "options": [
            "Antrochoanal polyp",
            "Ethmoidal polyp",
            "Inverted papilloma",
            "Rhinosporidiosis"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nNasal polyps are non-neoplastic, edematous prolapses of sinonasal mucosa, classified into: 1) Antrochoanal polyp (Killian polyp): Arises from the edematous mucosal lining of the maxillary sinus (antrum), emerges through an accessory (or natural) maxillary ostium into the middle meatus of the nasal cavity, and extends backwards into the posterior choana and nasopharynx. Key characteristics: Solitary, strictly unilateral, occurs in children and young adults (10 to 25 years), non-allergic in etiology, presents with unilateral nasal obstruction and posterior rhinoscopy mass; 2) Ethmoidal polyps: Arise from ethmoidal air cells and middle turbinate. Key characteristics: Multiple, strictly bilateral, occurs in adults, allergic/asthmatic etiology (associated with triad asthma / Samter triad), present with bilateral nasal obstruction and anosmia. Treatment for antrochoanal polyp is complete endoscopic surgical excision (FESS) with clearance of its antral attachment.\n\nOption Review:\n- Option A is correct because a solitary, unilateral polyp originating in the maxillary sinus and projecting into the choana is an antrochoanal polyp.\n- Option B is incorrect because ethmoidal polyps are multiple, bilateral, and occur in older allergic patients.\n- Option C is incorrect because inverted papilloma is a locally aggressive, firm, fleshy, vascular neoplasm with malignant potential.\n- Option D is incorrect because rhinosporidiosis forms friable, reddish, strawberry-like vascular polyps studded with white sporangia.\n\nKey Takeaway: Antrochoanal polyps are solitary, unilateral polyps originating from the maxillary antrum and extending into the choana, common in children and young adults.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q299",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Deep Neck Infections - Ludwig Angina",
        "prompt": "A 40-year-old male presents with severe pain, bilateral submandibular swelling, drooling of saliva, and high fever 4 days after an infected mandibular second molar tooth extraction. Physical examination reveals a woody-hard, brawny, non-fluctuant swelling involving the submental, submandibular, and sublingual spaces bilaterally. The floor of the mouth is markedly edematous, elevating and displacing the tongue superiorly and posteriorly, threatening the airway. What life-threatening infection of the floor of the mouth is diagnosed?",
        "options": [
            "Ludwig angina",
            "Vincent angina",
            "Quinsy",
            "Parapharyngeal abscess"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nLudwig angina is a rapidly spreading, potentially fatal, non-suppurative gangrenous cellulitis involving the submandibular, sublingual, and submental fascial spaces bilaterally. Approximately 80% to 90% of cases originate from odontogenic infections of the second or third mandibular molars, whose root apices extend below the insertion of the mylohyoid muscle, allowing infection direct access into the submandibular space. Clinical hallmarks: 1) Brawny, board-like, woody induration of the submandibular and submental regions ('bull neck'); 2) Marked elevation and posterior displacement of the tongue by swollen sublingual tissues, pushing the tongue against the palate and posterior pharynx; 3) Rapid airway compromise, stridor, and asphyxia; 4) Notably, there is absence of tissue fluctuance (pus is sparse in early cellulitic stages). Immediate management priority is securing the airway (awake fiberoptic intubation or emergency tracheostomy under local anesthesia), followed by intravenous broad-spectrum antibiotics and surgical decompression.\n\nOption Review:\n- Option A is correct because bilateral submandibular and sublingual cellulitis elevating the tongue defines Ludwig angina.\n- Option B is incorrect because Vincent angina (trench mouth) is acute necrotizing ulcerative gingivitis caused by spirochetes and fusobacteria.\n- Option C is incorrect because quinsy is a unilateral peritonsillar abscess displacing the uvula.\n- Option D is incorrect because parapharyngeal abscess produces medial displacement of the lateral pharyngeal wall and tonsil.\n\nKey Takeaway: Ludwig angina is a bilateral cellulitis of the sublingual and submandibular spaces, classically elevating the tongue and threatening catastrophic airway obstruction.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q300",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Otology - Complications of CSOM (Lateral Sinus Thrombophlebitis)",
        "prompt": "A 24-year-old male with chronic foul-smelling ear discharge (unsafe CSOM with cholesteatoma) presents with severe headache, high spiking 'picket-fence' fevers with chills and rigors, and vomiting. On examination, there is marked tenderness and pitting edema over the posterior part of the mastoid process overlying the mastoid emissary vein (Griesinger sign). Contrast-enhanced CT reveals a filling defect within the sigmoid sinus displaying an enhancing rim of dural wall ('empty delta sign'). What intracranial complication of chronic otitis media is diagnosed?",
        "options": [
            "Lateral sinus thrombophlebitis",
            "Extradural abscess",
            "Subdural empyema",
            "Otitic hydrocephalus"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nLateral (sigmoid) sinus thrombophlebitis is a severe intracranial vascular complication of chronic suppurative otitis media with cholesteatoma, occurring when bony erosion of the sinus plate allows infection to contact the lateral venous sinus. The clinical course demonstrates four distinct stages: 1) Perisinus abscess; 2) Endophlebitis; 3) Mural/obliterative septic thrombus; 4) Septic embolization. Key diagnostic features include: 1) 'Picket-fence' fever (hectic, irregular spikes of temperature with chills and drenching sweats coinciding with the periodic release of septic emboli into the circulation); 2) Griesinger sign: Pain, localized tenderness, and pitting edema over the posterior border of the mastoid process due to retrograde thrombosis of the mastoid emissary vein; 3) Contrast-enhanced CT or MR venography reveals the 'empty delta sign' (a central non-enhancing hypodense intraluminal thrombus surrounded by intense dural ring enhancement). Management involves urgent cortical/modified radical mastoidectomy with sinus exposure, needle aspiration/incision, and evacuation of the septic thrombus, along with high-dose intravenous antibiotics.\n\nOption Review:\n- Option A is correct because picket-fence fever, Griesinger sign, and sigmoid sinus thrombosis define lateral sinus thrombophlebitis.\n- Option B is incorrect because extradural abscess causes localized headache and fever, without Griesinger sign.\n- Option C is incorrect because subdural empyema causes rapid neurological deterioration with hemiparesis and seizures.\n- Option D is incorrect because otitic hydrocephalus causes raised intracranial pressure (papilledema, headache) with clear CSF.\n\nKey Takeaway: Lateral sinus thrombophlebitis is characterized by 'picket-fence' fever spikes, Griesinger sign (mastoid emissary vein edema), and the 'empty delta sign' on contrast CT.",
        "imageUrls": []
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(QUESTIONS)} questions in Part 2 Block 3.")
    for q in QUESTIONS:
        assert len(q["options"]) == 4, f"{q['id']} does not have 4 options"
        assert 0 <= q["answerIndex"] <= 3, f"{q['id']} invalid answerIndex"
        for opt in q["options"]:
            assert not opt.endswith(";"), f"{q['id']} option ends with semicolon: {opt}"
            assert "(" not in opt or any(c.isdigit() for c in opt), f"{q['id']} option has explanatory bracket: {opt}"
    print("All 50 questions passed structural assertions.")
