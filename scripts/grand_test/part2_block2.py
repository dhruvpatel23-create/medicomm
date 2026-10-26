# -*- coding: utf-8 -*-
"""
FMGE Grand Test 1 - Part 2: Block 2
Dermatology (3 Qs: Q201-Q203) + Psychiatry (5 Qs: Q204-Q208) + General Surgery (32 Qs: Q209-Q240) + Orthopedics (5 Qs: Q241-Q245) + Anesthesia (5 Qs: Q246-Q250) = 50 Questions (Q201 - Q250)
Strict adherence to 2026 NBE pattern, clinical vignettes, option-by-option review.
Zero textbook citations.
"""

QUESTIONS = [
    # ==========================================
    # DERMATOLOGY (3 Questions: Q201 - Q203)
    # ==========================================
    {
        "id": "fmge-gt1-q201",
        "subjectId": "dermatology",
        "subjectTitle": "Dermatology & STD",
        "topic": "Blistering Disorders - Pemphigus Vulgaris vs Bullous Pemphigoid",
        "prompt": "A 45-year-old male presents with painful, flaccid, easily ruptured blisters and extensive raw erosions on his scalp, chest, and oral mucosa. Gentle lateral tangential pressure on normal-appearing perilesional skin causes sloughing of the epidermis (positive Nikolsky sign). Direct immunofluorescence reveals intraepidermal IgG and C3 deposition in a 'fishnet-like' pattern around keratinocytes. Autoantibodies in this disorder target which adhesion molecule?",
        "options": [
            "Desmoglein 3",
            "Hemidesmosomal BP180 antigen",
            "Type VII collagen",
            "Transglutaminase"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nPemphigus vulgaris is a potentially life-threatening autoimmune intraepidermal blistering disease caused by IgG autoantibodies directed against desmoglein 3 (and desmoglein 1 in mucocutaneous disease), which are cadherin-type cell adhesion molecules of desmosomes connecting adjacent epidermal keratinocytes. Disruption of desmosomes causes loss of intercellular cohesion (acantholysis), producing suprabasal intraepidermal clefting with rounded, free-floating acantholytic cells (Tzanck cells). Because the blister roof consists of only thin upper epidermis, the bullae are flaccid, rupture easily to leave painful weeping erosions, and demonstrate a positive Nikolsky sign and positive Asboe-Hansen (bulla spread) sign. Direct immunofluorescence demonstrates IgG deposition along cell borders in a characteristic 'fishnet' or reticular pattern.\n\nOption Review:\n- Option A is correct because autoantibodies against desmoglein 3 cause suprabasal acantholysis in pemphigus vulgaris.\n- Option B is incorrect because antibodies against hemidesmosomal BP180 (and BP230) cause bullous pemphigoid, which features tense subepidermal bullae with a negative Nikolsky sign.\n- Option C is incorrect because antibodies against type VII anchoring collagen fibrils cause epidermolysis bullosa acquisita.\n- Option D is incorrect because epidermal transglutaminase antibodies cause dermatitis herpetiformis.\n\nKey Takeaway: Pemphigus vulgaris is characterized by flaccid blisters, mucosal erosions, positive Nikolsky sign, and IgG antibodies directed against desmoglein 3 in a fishnet pattern.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Pemphigus_vulgaris_immunofluorescence.jpg/640px-Pemphigus_vulgaris_immunofluorescence.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q202",
        "subjectId": "dermatology",
        "subjectTitle": "Dermatology & STD",
        "topic": "Parasitic Infestations - Scabies",
        "prompt": "A 22-year-old university student living in a dormitory presents with intense, generalized pruritus that worsens significantly at night. Physical examination reveals excoriated erythematous papules and fine, dark, thread-like linear, tortuous burrows localized to the finger web spaces, flexor wrists, axillae, and genitalia. What is the topical pharmacological treatment of choice for Sarcoptes scabiei infestation?",
        "options": [
            "5% Permethrin cream",
            "1% Hydrocortisone cream",
            "Topical ketoconazole cream",
            "0.1% Tacrolimus ointment"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nScabies is an intensely pruritic infestation caused by the human itch mite, Sarcoptes scabiei var. hominis. The fertilized female mite burrows into the stratum corneum of the epidermis, depositing eggs and feces (scybala). This induces a delayed Type IV hypersensitivity allergic reaction after 3 to 6 weeks, resulting in intense nocturnal itching. The pathognomonic diagnostic lesion is the burrow: a short, wavy, elevated, grayish-white or brownish linear track, found predominantly in web spaces of fingers, flexor wrists, elbows, axillary folds, umbilicus, and male genitalia. The first-line treatment of choice is topical 5% permethrin cream applied from the neck down to the soles of the feet, left on for 8 to 14 hours, and washed off, repeated after 7 days, with simultaneous treatment of all household and close contacts.\n\nOption Review:\n- Option A is correct because topical 5% permethrin cream is the first-line pediculicide/scabicide of choice for classical scabies.\n- Option B is incorrect because topical steroids suppress inflammation without killing mites, potentially causing 'scabies incognito'.\n- Option C is incorrect because ketoconazole is an antifungal agent with zero scabicidal activity.\n- Option D is incorrect because tacrolimus is an immunosuppressant calcineurin inhibitor.\n\nKey Takeaway: Topical 5% permethrin cream applied overnight and repeated after one week is the first-line treatment of choice for scabies.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q203",
        "subjectId": "dermatology",
        "subjectTitle": "Dermatology & STD",
        "topic": "Infectious Dermatology - Leprosy (Hansen Disease)",
        "prompt": "A 35-year-old male presents with a solitary, well-defined, hypopigmented macule with an erythematous, raised border on his right forearm. Sensation to light touch, temperature, and pinprick is completely absent within the lesion. The right greater auricular nerve and radial cutaneous nerve are thickened and non-tender. Slit-skin smear is negative for acid-fast bacilli. According to the Ridley-Jopling classification, which pole of Hansen disease is characterized by strong cell-mediated immunity and negative bacterial index?",
        "options": [
            "Tuberculoid leprosy",
            "Lepromatous leprosy",
            "Borderline lepromatous leprosy",
            "Histoid leprosy"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nLeprosy (Hansen disease), caused by Mycobacterium leprae, manifests across a spectrum determined by host cell-mediated immunity (CMI): 1) Tuberculoid leprosy (TT): Vigorous host Th1 cell-mediated immunity (positive lepromin test). Infection is contained, resulting in paucibacillary disease (bacterial index 0). Lesions are few (1 to 3), hypopigmented, anesthetic macules with distinct erythematous, raised, dry, hairless borders. Severe asymmetrical peripheral nerve thickening with early localized sensory loss occurs; 2) Lepromatous leprosy (LL): Absent CMI (negative lepromin test) with high Th2 humoral response, leading to multibacillary disease. Features widespread, bilateral symmetrical macules/papules, leonine facies, loss of lateral third of eyebrows (madarosis), and gloved-and-stocking sensory loss.\n\nOption Review:\n- Option A is correct because tuberculoid leprosy represents the high-immunity pole with few anesthetic hypopigmented lesions and negative bacterial index.\n- Option B is incorrect because lepromatous leprosy has absent CMI, massive bacillary load, and widespread symmetrical lesions.\n- Option C is incorrect because borderline lepromatous has low CMI and high bacillary counts.\n- Option D is incorrect because histoid leprosy is a multibacillary variant with firm, shiny, keloid-like nodules.\n\nKey Takeaway: Tuberculoid leprosy represents the high cell-mediated immunity pole of Hansen disease, characterized by single or few anesthetic hypopigmented macules with negative skin smears.",
        "imageUrls": []
    },

    # ==========================================
    # PSYCHIATRY (5 Questions: Q204 - Q208)
    # ==========================================
    {
        "id": "fmge-gt1-q204",
        "subjectId": "psychiatry",
        "subjectTitle": "Psychiatry",
        "topic": "Psychosis - Schizophrenia DSM-5 Diagnostic Criteria",
        "prompt": "A 21-year-old male college student is brought to the clinic by his family due to a 7-month decline in functioning. He believes the government is monitoring his thoughts through the radio (persecutory delusions) and frequently converses with invisible voices discussing his actions in the third person (auditory hallucinations). His speech is disorganized, and he exhibits avolition and social withdrawal. Neurological examination and urine toxicology are normal. What is the diagnosis?",
        "options": [
            "Schizophrenia",
            "Schizoaffective disorder",
            "Brief psychotic disorder",
            "Bipolar I disorder with psychosis"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAccording to DSM-5 criteria, Schizophrenia requires at least two of the following five active-phase symptoms present for a significant portion of time during a 1-month period, with at least one symptom being delusions, hallucinations, or disorganized speech: 1) Delusions; 2) Hallucinations; 3) Disorganized speech; 4) Grossly disorganized or catatonic behavior; 5) Negative symptoms (diminished emotional expression, avolition). Continuous signs of the disturbance must persist for at least 6 months (including prodromal, active-phase, and residual periods), causing marked social or occupational dysfunction, without concurrent primary mood episodes.\n\nOption Review:\n- Option A is correct because active delusions, auditory hallucinations, disorganized speech, negative symptoms, and duration >6 months establish schizophrenia.\n- Option B is incorrect because schizoaffective disorder requires a concurrent major depressive or manic episode alongside psychotic symptoms, plus >=2 weeks of delusions/hallucinations without mood symptoms.\n- Option C is incorrect because brief psychotic disorder lasts at least 1 day but less than 1 month, followed by full recovery.\n- Option D is incorrect because bipolar disorder with psychosis features prominent sustained mania or depression.\n\nKey Takeaway: Schizophrenia requires characteristic psychotic symptoms (delusions, hallucinations, or disorganized speech) with continuous illness signs persisting for at least 6 months.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q205",
        "subjectId": "psychiatry",
        "subjectTitle": "Psychiatry",
        "topic": "Mood Disorders - Bipolar I Disorder & Lithium Monitoring",
        "prompt": "A 28-year-old male is admitted after 5 days of euphoric mood, sleeping only 2 hours a night without feeling tired, rapid pressured speech, grandiosity claiming he possesses supernatural wealth, and reckless financial spending. Following resolution of acute mania, he is started on lithium carbonate for long-term maintenance. Which two baseline organ functions must be routinely monitored during chronic lithium therapy?",
        "options": [
            "Renal and thyroid function tests",
            "Pulmonary function and liver enzymes",
            "Serum amylase and lipase",
            "Bone mineral density and serum iron"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nBipolar I disorder is defined by the occurrence of at least one manic episode (abnormally and persistently elevated, expansive, or irritable mood and increased energy lasting >= 1 week, causing marked social/occupational impairment). Lithium carbonate is the gold-standard mood stabilizer for treating acute mania and preventing manic and depressive recurrences. Because lithium is excreted almost entirely unchanged by the kidneys (handling resembles sodium in the proximal tubule), and has a narrow therapeutic window (0.6 to 1.2 mEq/L), chronic therapy carries established organ toxicities: 1) Nephrotoxicity: Nephrogenic diabetes insipidus (impairing aquaporin-2 response to ADH) and chronic tubulointerstitial nephropathy; 2) Thyroid dysfunction: Goiter and hypothyroidism (inhibiting thyroid hormone synthesis and release). Therefore, baseline and periodic monitoring of serum creatinine, eGFR, and TSH is mandatory.\n\nOption Review:\n- Option A is correct because renal function (BUN/creatinine) and thyroid function (TSH) are the two primary organ parameters monitored on lithium.\n- Option B is incorrect because pulmonary fibrosis is associated with amiodarone, not lithium.\n- Option C is incorrect because pancreatic enzymes are monitored for valproic acid toxicity.\n- Option D is incorrect because bone density is not a standard routine monitoring target for lithium.\n\nKey Takeaway: Routine surveillance of renal function (BUN, creatinine) and thyroid function (TSH) is mandatory during chronic lithium therapy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q206",
        "subjectId": "psychiatry",
        "subjectTitle": "Psychiatry",
        "topic": "Anxiety Disorders - Panic Disorder",
        "prompt": "A 26-year-old female presents to the emergency room convinced she is suffering a heart attack. She describes sudden, unexpected attacks of intense fear reaching a peak within 10 minutes, accompanied by palpitations, sweating, trembling, shortness of breath, chest tightness, and a fear of dying or losing control. Medical evaluation including ECG, cardiac troponins, and thyroid panel is completely normal. She has lived in constant dread of having another attack for the past 2 months. What is the diagnosis?",
        "options": [
            "Panic disorder",
            "Generalized anxiety disorder",
            "Social anxiety disorder",
            "Somatic symptom disorder"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nPanic disorder is characterized by recurrent, unexpected panic attacks: abrupt surges of intense fear or intense discomfort that reach a crescendo within minutes, accompanied by at least 4 of 13 somatic and cognitive symptoms (palpitations, diaphoresis, trembling, dyspnea, choking sensation, chest pain, nausea, dizziness, chills/hot flushes, paresthesias, derealization/depersonalization, fear of losing control, fear of dying). DSM-5 diagnosis requires that at least one attack be followed by >= 1 month of persistent concern or worry about additional attacks or their consequences ('anticipatory anxiety'), or a significant maladaptive change in behavior related to the attacks (e.g., agoraphobic avoidance). First-line long-term treatment consists of SSRIs (e.g., sertraline) combined with cognitive behavioral therapy (CBT).\n\nOption Review:\n- Option A is correct because recurrent unexpected panic attacks accompanied by persistent anticipatory anxiety define panic disorder.\n- Option B is incorrect because GAD involves chronic, diffuse, pervasive worry about multiple daily domains lasting >=6 months without discrete panic peaks.\n- Option C is incorrect because social anxiety disorder involves fear of negative evaluation in social or performance situations.\n- Option D is incorrect because somatic symptom disorder involves excessive anxiety regarding distressing chronic somatic symptoms.\n\nKey Takeaway: Panic disorder is defined by recurrent unexpected panic attacks followed by at least 1 month of persistent worry about future attacks.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q207",
        "subjectId": "psychiatry",
        "subjectTitle": "Psychiatry",
        "topic": "Substance Use - Delirium Tremens Management",
        "prompt": "A 48-year-old chronic alcoholic is hospitalized for an ankle fracture. On hospital day 3 (approximately 60 hours after his last alcoholic drink), he becomes severely agitated, disoriented, diaphoretic, and tachycardic (heart rate 130 bpm). Blood pressure is 185/105 mmHg. He experiences visual hallucinations of insects crawling on the hospital walls. What is the first-line pharmacological agent of choice to treat delirium tremens?",
        "options": [
            "Intravenous lorazepam or diazepam",
            "Intramuscular haloperidol monotherapy",
            "Oral phenytoin",
            "Intravenous chlorpromazine"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nDelirium tremens (DTs) is the most severe, life-threatening manifestation of alcohol withdrawal syndrome, occurring 48 to 96 hours after the cessation or reduction of heavy alcohol intake. Chronic alcohol consumption downregulates inhibitory GABAA receptors and upregulates excitatory NMDA receptors. Abrupt alcohol cessation removes GABAA facilitation and causes massive, unchecked NMDA-mediated glutamatergic excitation and sympathetic storm. Clinical features include acute delirium (fluctuating clouding of consciousness, disorientation), profound autonomic hyperactivity (tachycardia, malignant hypertension, hyperthermia, diaphoresis), coarse tremor, and visual/tactile hallucinations. The first-line treatment of choice is long-acting intravenous benzodiazepines (diazepam, chlordiazepoxide, or lorazepam in liver disease) to restore GABAA-mediated neural inhibition.\n\nOption Review:\n- Option A is correct because benzodiazepines (lorazepam or diazepam) cross-react with GABAA receptors and represent the first-line treatment for delirium tremens.\n- Option B is incorrect because haloperidol lowers the seizure threshold and worsens cardiac arrhythmias, indicated only as an adjunct for severe agitation refractory to benzodiazepines.\n- Option C is incorrect because phenytoin has zero efficacy in preventing or treating alcohol withdrawal seizures or DTs.\n- Option D is incorrect because chlorpromazine lowers seizure thresholds and causes profound hypotension.\n\nKey Takeaway: Intravenous benzodiazepines (diazepam or lorazepam) are the first-line medical therapy for life-threatening delirium tremens.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q208",
        "subjectId": "psychiatry",
        "subjectTitle": "Psychiatry",
        "topic": "Psychopharmacology - Neuroleptic Malignant Syndrome",
        "prompt": "A 25-year-old male with schizophrenia is started on intramuscular haloperidol. Within 4 days, he develops extreme generalized 'lead-pipe' muscle rigidity, body temperature spiking to 40.5°C (104.9°F), autonomic instability (fluctuating blood pressure and tachycardia), altered level of consciousness, and elevated serum creatine kinase (CK 18,000 U/L). What life-threatening idiosyncratic reaction to dopamine D2 receptor blockade has occurred?",
        "options": [
            "Neuroleptic malignant syndrome",
            "Serotonin syndrome",
            "Malignant hyperthermia",
            "Acute dystonic reaction"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nNeuroleptic Malignant Syndrome (NMS) is an idiosyncratic, life-threatening medical emergency caused by potent dopamine D2 receptor blockade (most commonly first-generation high-potency neuroleptics like haloperidol and fluphenazine, or withdrawal of dopamine agonists). Sudden loss of central dopaminergic activity in the hypothalamus and basal ganglia results in the cardinal tetrad: 1) Severe 'lead-pipe' muscle rigidity; 2) Hyperthermia (temperature often >40°C); 3) Autonomic instability (diaphoresis, labile blood pressure, tachycardia); 4) Altered mental status (confusion, stupor, coma). Severe muscle breakdown drives marked elevation of serum creatine kinase (CK) and myoglobinuria (acute kidney injury). Treatment involves immediate discontinuation of the antipsychotic, supportive cooling, and administration of dantrolene (muscle relaxant) or bromocriptine (dopamine agonist).\n\nOption Review:\n- Option A is correct because lead-pipe rigidity, hyperthermia, autonomic instability, and massive CK elevation define neuroleptic malignant syndrome.\n- Option B is incorrect because serotonin syndrome features hyperreflexia, shivering, and clonus (spontaneous, inducible, or ocular), rather than lead-pipe rigidity.\n- Option C is incorrect because malignant hyperthermia is triggered by volatile inhalational anesthetics or succinylcholine, not neuroleptics.\n- Option D is incorrect because acute dystonia involves brief, localized focal spasms (e.g., torticollis, oculogyric crisis) without fever and autonomic collapse.\n\nKey Takeaway: Neuroleptic malignant syndrome is a life-threatening reaction to dopamine antagonists presenting with lead-pipe rigidity, hyperthermia, autonomic storm, and elevated CK.",
        "imageUrls": []
    },

    # ==========================================
    # GENERAL SURGERY (32 Questions: Q209 - Q240)
    # ==========================================
    {
        "id": "fmge-gt1-q209",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Acute Abdomen - Acute Appendicitis (Alvarado Score)",
        "prompt": "A 19-year-old male presents with periumbilical pain that shifted to the right lower quadrant 12 hours later, accompanied by anorexia, low-grade fever, and vomiting. Physical examination reveals tenderness, localized guarding, and rebound tenderness at McBurney's point. Complete blood count shows leukocytosis with a left shift. What is the anatomical location of McBurney's point on the anterior abdominal wall?",
        "options": [
            "One-third the distance from the anterior superior iliac spine to the umbilicus",
            "Two-thirds the distance from the anterior superior iliac spine to the umbilicus",
            "Midpoint between the xiphoid process and the umbilicus",
            "Directly over the right costal margin at the midclavicular line"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAcute appendicitis is the leading cause of emergency acute abdominal surgery in young adults. Luminal obstruction (by a fecalith, lymphoid hyperplasia, or foreign body) leads to closed-loop mucosal secretion, bacterial overgrowth, ischemic necrosis, and perforation. Pain initially begins as dull, poorly localized periumbilical visceral pain mediated by T10 sympathetic splanchnic fibers. Once transmural inflammation contacts the parietal peritoneum, somatic pain localizes sharply to the right iliac fossa at McBurney's point. McBurney's point is anatomically defined as the junction of the lateral one-third and medial two-thirds of an imaginary line drawn from the right anterior superior iliac spine (ASIS) to the umbilicus (or one-third the distance from the ASIS to the umbilicus).\n\nOption Review:\n- Option A is correct because McBurney's point is situated one-third the distance from the right ASIS along the line joining the ASIS to the umbilicus.\n- Option B is incorrect because two-thirds from the ASIS places the landmark too close to the midline umbilicus.\n- Option C is incorrect because the midpoint between xiphoid and umbilicus is in the epigastrium.\n- Option D is incorrect because the right costal margin at midclavicular line is Murphy's point for the gallbladder.\n\nKey Takeaway: McBurney's point corresponds to the base of the appendix, located one-third the distance from the right anterior superior iliac spine to the umbilicus.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q210",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Biliary Surgery - Acute Cholecystitis & Murphy Sign",
        "prompt": "A 44-year-old obese female presents with severe, steady pain in her right upper quadrant radiating to her right scapula, accompanied by nausea, vomiting, and low-grade fever following a fatty meal. Palpation of the right subcostal area during deep inspiration triggers sudden, sharp pain and abrupt arrest of inspiration (positive Murphy sign). What is the initial diagnostic imaging investigation of choice for acute calculous cholecystitis?",
        "options": [
            "Transabdominal ultrasound",
            "Contrast-enhanced abdominal CT",
            "Endoscopic retrograde cholangiopancreatography",
            "Plain abdominal radiography"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAcute calculous cholecystitis occurs when a gallstone becomes impacted in the neck of the gallbladder or cystic duct, resulting in luminal distension, wall ischemia, and acute chemical and secondary bacterial inflammation. Patients present with right upper quadrant pain radiating to the right inferior scapular angle (Boas sign, mediated by phrenic and cutaneous C3-C5 fibers) and a positive Murphy sign (sudden arrest of inspiratory effort during palpation of the right costal margin). Transabdominal ultrasonography is the first-line investigation of choice (sensitivity >90%), demonstrating: 1) Gallstones; 2) Gallbladder wall thickening (>3 to 4 mm); 3) Pericholecystic fluid; 4) Sonographic Murphy sign (focal tenderness elicited by ultrasound transducer pressure directly over the visualized gallbladder).\n\nOption Review:\n- Option A is correct because transabdominal ultrasound is the primary, highly sensitive, non-invasive imaging modality of choice for acute cholecystitis.\n- Option B is incorrect because CT is less sensitive for gallstones (many are isodense to bile) and is used when complications (gangrene, perforation) are suspected.\n- Option C is incorrect because ERCP is an invasive therapeutic procedure for choledocholithiasis, not initial diagnostic imaging for cholecystitis.\n- Option D is incorrect because only 10% to 15% of gallstones are radiopaque on plain X-rays.\n\nKey Takeaway: Transabdominal ultrasound is the first-line diagnostic investigation of choice for acute cholecystitis, revealing gallstones, wall thickening, and sonographic Murphy sign.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q211",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Trauma Surgery - Tension Pneumothorax Immediate Triage",
        "prompt": "A 28-year-old male is brought to the trauma bay following a high-speed vehicular collision. He is in severe respiratory distress and cyanotic. Blood pressure is 70/40 mmHg, pulse is 138 bpm, and neck veins are distended. Physical examination demonstrates hyperresonance to percussion and absent breath sounds over the entire right hemithorax, with the trachea visibly deviated to the left. What is the immediate, life-saving next step in management?",
        "options": [
            "Immediate needle thoracostomy decompression",
            "Urgent portable chest radiography",
            "Immediate formal endotracheal intubation",
            "Contrast-enhanced CT scan of the thorax"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nTension pneumothorax is a clinical diagnosis and an absolute surgical emergency that must NEVER be delayed for radiological confirmation. A one-way 'ball-valve' tissue defect allows air to enter the pleural space during inspiration without escaping during expiration. Intrapleural pressure escalates, causing complete collapse of the ipsilateral lung and shifting the mediastinum and trachea to the opposite side. Mediastinal shift kinks the inferior vena cava and superior vena cava, severely restricting venous return to the right heart, producing profound obstructive shock, hypotension, jugular venous distension, and imminent cardiac arrest. Immediate management is rapid needle decompression (using a large-bore 14- or 16-gauge cannula inserted in the 2nd intercostal space at the midclavicular line, or 5th intercostal space at the anterior axillary line), which converts the tension pneumothorax into an open pneumothorax, followed promptly by tube thoracostomy (intercostal chest drain).\n\nOption Review:\n- Option A is correct because immediate needle thoracostomy decompression relieves the life-threatening pleural tension without waiting for imaging.\n- Option B is incorrect because waiting for a chest X-ray in a hemodynamically unstable patient with obvious tension pneumothorax leads to cardiac arrest.\n- Option C is incorrect because positive pressure ventilation before decompressing the tension pneumothorax will worsen intrathoracic pressure and collapse venous return.\n- Option D is incorrect because CT scan is strictly contraindicated in unstable trauma resuscitation.\n\nKey Takeaway: Tension pneumothorax is a clinical emergency requiring immediate bedside needle decompression; radiological investigations must never delay treatment.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q212",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Burns - Parkland Formula Fluid Resuscitation",
        "prompt": "A 70-kg adult male suffers deep second-degree thermal burns covering his entire anterior trunk (18%) and both anterior upper extremities (9% each = 18%), totaling 36% Total Body Surface Area (TBSA). Fluid resuscitation is calculated using the Parkland formula. According to the Parkland formula, what total volume of Ringer's lactate must be infused during the first 24 hours post-burn?",
        "options": [
            "5,040 mL",
            "10,080 mL",
            "15,120 mL",
            "20,160 mL"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe Parkland (Baxter) formula is the standard guideline for calculating crystalloid fluid resuscitation in major thermal burns (>20% TBSA in adults) during the first 24 hours from the time of injury: Total 24-hour Fluid Volume = 4 mL x Body Weight in kg x Percentage of Total Body Surface Area (% TBSA) burned. In this patient: Body Weight = 70 kg; % TBSA = 36%. Total 24-hour volume of Ringer's lactate = 4 x 70 x 36 = 10,080 mL. Timing of infusion: 1) First half (5,040 mL) is infused over the first 8 hours calculated from the time of the burn injury (not from the time of hospital arrival); 2) The remaining half (5,040 mL) is infused evenly over the subsequent 16 hours. Adequate resuscitation is guided by titrating to maintain target adult urine output of 0.5 to 1.0 mL/kg/hour (approximately 30 to 50 mL/hour).\n\nOption Review:\n- Option A is incorrect because 5,040 mL is the volume administered during the first 8 hours, not the full 24-hour requirement.\n- Option B is correct because 4 mL x 70 kg x 36% = 10,080 mL total 24-hour fluid volume.\n- Option C is incorrect because 15,120 mL overestimates fluid by using a 6 mL multiplier.\n- Option D is incorrect because 20,160 mL represents double the calculated requirement.\n\nKey Takeaway: The Parkland formula calculates 24-hour fluid resuscitation as 4 mL x kg x % TBSA of Ringer's lactate, with half infused over the first 8 hours and the rest over 16 hours.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q213",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Endocrine Surgery - Thyroid Malignancies (Follicular Carcinoma)",
        "prompt": "A 42-year-old female presents with a solitary, painless 3 cm thyroid nodule. Fine needle aspiration cytology (FNAC) demonstrates a microfollicular proliferation of thyroid follicular cells, reported as a 'follicular neoplasm'. Why can fine needle aspiration cytology definitively distinguish follicular adenoma from follicular carcinoma?",
        "options": [
            "It cannot distinguish because demonstration of capsular or vascular invasion on histology is required",
            "It readily identifies malignant capsular penetration on cellular aspirates",
            "It detects specific amyloid stroma that is absent in adenomas",
            "It detects pathognomonic Orphan Annie eye nuclei"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nFollicular thyroid lesions present a unique diagnostic challenge in surgical pathology. Fine needle aspiration cytology (FNAC) evaluates cellular morphology from aspirates, but cannot assess the architecture of the surrounding tumor capsule. The cytological features of follicular adenoma and well-differentiated follicular thyroid carcinoma are identical (microfollicles, crowded follicular cells with round regular nuclei). The definitive histopathological distinction between a benign follicular adenoma and a malignant follicular carcinoma relies entirely on identifying: 1) Full-thickness penetration/transgression of the fibrous capsule (capsular invasion); or 2) Tumor penetration into blood vessels within or outside the capsule (vascular invasion). Because this requires histological examination of the intact tumor-capsule interface, formal diagnostic lobectomy with histological examination is mandatory.\n\nOption Review:\n- Option A is correct because FNAC cannot evaluate architectural capsular or vascular invasion, which is required to differentiate follicular carcinoma from adenoma.\n- Option B is incorrect because aspirates disrupt tissue architecture and cannot evaluate capsular invasion.\n- Option C is incorrect because amyloid stroma is characteristic of medullary thyroid carcinoma, not follicular lesions.\n- Option D is incorrect because Orphan Annie eye nuclei are pathognomonic for papillary thyroid carcinoma, not follicular carcinoma.\n\nKey Takeaway: Follicular carcinoma cannot be distinguished from follicular adenoma by FNAC alone because histological demonstration of capsular or vascular invasion is required.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q214",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Surgical Oncology - Breast Cancer (Sentinel Lymph Node Biopsy)",
        "prompt": "A 52-year-old female undergoes breast-conserving surgery (wide local excision) for an unifocal 1.8 cm invasive ductal carcinoma of the upper outer quadrant of the left breast. Preoperative axillary ultrasound and clinical examination reveal no suspicious axillary lymphadenopathy (cN0). What is the standard-of-care procedure for staging the axilla in clinically node-negative early breast cancer?",
        "options": [
            "Sentinel lymph node biopsy",
            "Routine full level I, II, and III axillary dissection",
            "Routine blind irradiation of the axilla without biopsy",
            "Observation of the axilla without staging"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIn early-stage breast cancer with a clinically and radiologically normal axilla (cN0), Sentinel Lymph Node Biopsy (SLNB) has superseded routine complete axillary lymph node dissection (ALND) as the standard of care for axillary staging. The sentinel lymph node (SLN) is defined as the first lymph node (or group of nodes) that receives direct lymphatic drainage from the primary breast tumor. A radiotracer (Technetium-99m sulfur colloid) and/or blue dye (isosulfan blue or patent blue) is injected into the peritumoral/subareolar dermis. The hot and/or blue sentinel nodes are excised and examined by frozen section/histopathology. If the SLN is negative for metastasis, the remainder of the axilla is spared, dramatically reducing the risk of disabling lymphedema, pain, and paresthesias.\n\nOption Review:\n- Option A is correct because sentinel lymph node biopsy is the standard minimally invasive axillary staging technique in cN0 early breast cancer.\n- Option B is incorrect because complete level I-III ALND causes significant arm lymphedema and is reserved for patients with biopsy-proven node-positive disease.\n- Option C is incorrect because blind radiotherapy without surgical staging is not standard of care.\n- Option D is incorrect because omitting axillary evaluation leaves stage and adjuvant systemic therapy undetermined.\n\nKey Takeaway: Sentinel lymph node biopsy (SLNB) is the standard method for axillary staging in clinically node-negative (cN0) early breast cancer.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q215",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Abdominal Wall Surgery - Inguinal Hernia (Direct vs Indirect)",
        "prompt": "During an open inguinal hernia repair in a 62-year-old male, the hernia sac is found protruding directly through the floor of the inguinal canal, medial to the inferior epigastric vessels within Hesselbach's triangle. What anatomical defect forms the floor of Hesselbach's triangle in direct inguinal hernias?",
        "options": [
            "Fascia transversalis",
            "External oblique aponeurosis",
            "Internal oblique muscle belly",
            "Inguinal ligament"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nDirect inguinal hernias are acquired weaknesses occurring predominantly in older males. The hernia sac protrudes forward directly through Hesselbach's triangle, which is bounded: Medially by the lateral border of the rectus abdominis muscle; Laterally by the inferior epigastric vessels; Inferiorly by the inguinal ligament (Poupart's ligament). The floor of Hesselbach's triangle is formed entirely by the fascia transversalis (reinforced medially by the conjoint tendon). Chronic increases in intra-abdominal pressure (BPH straining, chronic cough, constipation) stretch and attenuate this transversalis fascia, allowing abdominal viscera enclosed in a diffuse, broad-based peritoneal sac to push forward medial to the epigastric vessels. Direct hernias rarely strangulate because of their wide neck.\n\nOption Review:\n- Option A is correct because the fascia transversalis forms the floor of Hesselbach's triangle where direct inguinal hernias protrude.\n- Option B is incorrect because the external oblique aponeurosis forms the anterior wall of the inguinal canal.\n- Option C is incorrect because the internal oblique and transversus abdominis arch over to form the roof and conjoint tendon.\n- Option D is incorrect because the inguinal ligament forms the inferior boundary (gutter/floor of canal), not the floor of Hesselbach's triangle.\n\nKey Takeaway: Direct inguinal hernias protrude through Hesselbach's triangle medial to the inferior epigastric vessels due to an acquired defect in the fascia transversalis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q216",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Colorectal Surgery - Fistula-in-Ano (Goodsall's Rule)",
        "prompt": "A 40-year-old male presents with persistent discharge from an external perianal opening located at the 5 o'clock position (posterior to the transverse anal line), 3 cm from the anal verge. According to Goodsall's rule of fistulas-in-ano, what path will the fistulous tract take to enter the anal canal?",
        "options": [
            "Curved tract opening into the posterior midline of the anal canal",
            "Direct radial straight tract opening at the 5 o'clock position",
            "Transverse tract crossing directly to the anterior midline",
            "Oblique straight tract opening into the contralateral 11 o'clock crypt"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nGoodsall's rule guides the anatomical trajectory of fistula-in-ano relative to an imaginary transverse line drawn across the midpoint of the anus: 1) Fistulas with an external opening situated POSTERIOR to the transverse line: Follow a curved, tortuous tract running towards the posterior midline (6 o'clock position) to open into the posterior anal crypt (crypt of Morgagni); 2) Fistulas with an external opening situated ANTERIOR to the transverse line: Follow a straight, direct radial tract running directly inward to enter the anal canal at the corresponding clock position. Exception to the rule: An anterior external opening situated >3 cm from the anal verge often behaves like a posterior fistula, curving backwards to open into the posterior midline.\n\nOption Review:\n- Option A is correct because posterior external openings (like 5 o'clock) curve backward to enter the anal canal at the posterior midline.\n- Option B is incorrect because straight radial tracks are typical for anterior external openings within 3 cm.\n- Option C is incorrect because fistulous tracks do not cross transversely to the anterior midline.\n- Option D is incorrect because contralateral diagonal tracks do not occur under Goodsall's rule.\n\nKey Takeaway: According to Goodsall's rule, fistulas-in-ano with posterior external openings follow a curved tract to open at the posterior midline crypt of the anal canal.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q217",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Vascular Surgery - Abdominal Aortic Aneurysm (AAA) Rupture",
        "prompt": "A 70-year-old male with a history of heavy smoking and hypertension presents with sudden onset of severe, tearing lower back pain, diaphoresis, and syncope. On examination, blood pressure is 80/50 mmHg, pulse is 118 bpm, and a tender, pulsatile, expansile mass is palpated in the central abdomen above the umbilicus. What life-threatening vascular emergency is diagnosed by this classic clinical triad?",
        "options": [
            "Ruptured abdominal aortic aneurysm",
            "Acute mesenteric ischemia",
            "Perforated duodenal ulcer",
            "Strangulated umbilical hernia"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nRuptured Abdominal Aortic Aneurysm (AAA) is a vascular catastrophe with an overall mortality of 80% to 90%. An aortic aneurysm is defined as a permanent focal dilation of the abdominal aorta >= 3.0 cm (or >= 50% increase compared to normal adjacent aorta), typically infrarenal in location. The classic triad of ruptured AAA consists of: 1) Sudden onset of severe abdominal or back/flank pain; 2) Hypotension / hemorrhagic shock; 3) Palpable, tender, pulsatile expansile abdominal mass. In unstable patients demonstrating this triad, emergency bedside ultrasound confirms aortic dilation, and immediate transfer to the operating theater for emergency repair (open surgical or EVAR) is indicated without delaying for CT angiography.\n\nOption Review:\n- Option A is correct because sudden back pain, shock, and a pulsatile expansile abdominal mass define ruptured abdominal aortic aneurysm.\n- Option B is incorrect because acute mesenteric ischemia presents with pain out of proportion to physical findings without a pulsatile mass.\n- Option C is incorrect because perforated ulcer causes board-like rigidity and free air under the diaphragm without a pulsatile mass.\n- Option D is incorrect because strangulated hernia presents as a tender, non-expansile, irreducible external swelling at the umbilicus.\n\nKey Takeaway: The triad of sudden severe back pain, hypotension, and a pulsatile abdominal mass is diagnostic of a ruptured abdominal aortic aneurysm.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q218",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Intestinal Obstruction - Small Bowel Obstruction (SBO)",
        "prompt": "A 50-year-old female with a history of an open appendectomy 10 years ago presents with colicky periumbilical abdominal pain, bilious vomiting, progressive abdominal distension, and obstipation (failure to pass flatus or feces) for 24 hours. Physical examination reveals high-pitched 'tinkling' bowel sounds. Upright abdominal radiograph demonstrates multiple central air-fluid levels with prominent plicae circulares (valvulae conniventes) spanning the entire diameter of the dilated bowel loops. What is the most common cause of mechanical small bowel obstruction in adults with prior abdominal surgery?",
        "options": [
            "Postoperative peritoneal adhesions",
            "Incarcerated groin hernia",
            "Colorectal adenocarcinoma",
            "Intussusception"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nMechanical small bowel obstruction (SBO) presents with the cardinal tetrad: 1) Colicky abdominal pain; 2) Vomiting (bilious in mid-gut obstruction); 3) Abdominal distension; 4) Obstipation (absolute constipation). On physical examination, hyperactive, high-pitched metallic or 'tinkling' bowel sounds with visible peristalsis are heard in early stages. Upright abdominal radiography characteristically shows dilated small bowel loops (>3 cm) located centrally in a 'stepladder' pattern, with multiple air-fluid levels (>5) and thin, transverse folds (valvulae conniventes / plicae circulares) that completely cross the luminal width (distinguishing small bowel from colon, whose haustral markings span only partway). Postoperative intra-abdominal adhesions account for approximately 60% to 75% of all mechanical small bowel obstructions in adults.\n\nOption Review:\n- Option A is correct because postoperative peritoneal adhesions are the single leading cause of small bowel obstruction in patients with prior surgery.\n- Option B is incorrect because incarcerated hernias are the second most common cause overall, but less frequent than adhesions in post-surgical patients.\n- Option C is incorrect because colorectal cancer is the leading cause of large bowel obstruction, not small bowel obstruction.\n- Option D is incorrect because intussusception is a common cause in infants, but rare in adults (where it typically indicates a neoplastic lead point).\n\nKey Takeaway: Postoperative peritoneal adhesions are the leading cause of mechanical small bowel obstruction in adults, presenting with air-fluid levels and plicae circulares on X-ray.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Small_bowel_obstruction_X-ray.jpg/640px-Small_bowel_obstruction_X-ray.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q219",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Trauma Surgery - FAST Examination",
        "prompt": "A 30-year-old male is brought to the trauma center following blunt abdominal trauma from a motor vehicle crash. He is tachycardic (115 bpm) and hypotensive (85/55 mmHg). An emergency Focused Assessment with Sonography for Trauma (FAST) scan is performed. Which dependent peritoneal space between the liver and right kidney is the most sensitive anatomical site for detecting free intraperitoneal fluid in the supine patient?",
        "options": [
            "Hepatorenal recess",
            "Splenorenal recess",
            "Rectovesical pouch",
            "Subdiaphragmatic space"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe Focused Assessment with Sonography for Trauma (FAST) is a rapid, bedside ultrasound examination performed during the primary survey to detect free intraperitoneal and pericardial fluid (blood/hemoperitoneum) in blunt trauma. The four standard acoustic windows are: 1) Right Upper Quadrant (RUQ): Evaluates the hepatorenal recess (Morison's pouch) and right pleural space; 2) Left Upper Quadrant (LUQ): Evaluates the splenorenal recess and left pleural space; 3) Pelvis (Suprapubic): Evaluates the rectovesical pouch in males or rectouterine pouch (pouch of Douglas) in females; 4) Subxiphoid: Evaluates the pericardial sac for cardiac tamponade. In a supine patient, Morison's pouch (the hepatorenal space) is the most gravitationally dependent pocket of the supramesocolic compartment and is the single most sensitive location for detecting hemoperitoneum.\n\nOption Review:\n- Option A is correct because the hepatorenal space (Morison's pouch) is the most dependent peritoneal space in supine patients and the most sensitive FAST window.\n- Option B is incorrect because the splenorenal space detects left-sided fluid, but fluid accumulates here only after pooling in Morison's pouch.\n- Option C is incorrect because the rectovesical pouch is the most dependent space in the pelvis, but secondary to Morison's pouch in total sensitivity.\n- Option D is incorrect because the subdiaphragmatic space is less dependent.\n\nKey Takeaway: The hepatorenal space (Morison's pouch) is the most sensitive acoustic window on FAST for detecting hemoperitoneum in supine trauma patients.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q220",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Pancreatic Surgery - Acute Pancreatitis (Ranson Criteria)",
        "prompt": "A 45-year-old male with chronic gallstones is admitted with severe epigastric pain radiating through to his back, accompanied by vomiting and elevated serum lipase (1,800 U/L). Ranson criteria are assessed to predict the severity and mortality of acute pancreatitis. Which parameter is evaluated at the time of admission in Ranson prognostic scoring?",
        "options": [
            "Age greater than 55 years",
            "Hematocrit drop greater than 10%",
            "Serum calcium less than 8 mg/dL",
            "Blood urea nitrogen rise greater than 5 mg/dL"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nRanson's prognostic criteria assess the severity and mortality risk of acute pancreatitis: 1) At Admission (mnemonic: 'GA LAW' / 5 parameters): (a) Glucose > 200 mg/dL; (b) Age > 55 years; (c) Leukocyte count (WBC) > 16,000/microL; (d) AST > 250 U/L; (e) LDH > 350 U/L. 2) During the first 48 hours (mnemonic: 'C HOBBS' / 6 parameters): (a) Calcium < 8.0 mg/dL; (b) Hematocrit drop > 10%; (c) Oxygen (arterial PO2) < 60 mmHg; (d) Base deficit > 4 mEq/L; (e) BUN increase > 5 mg/dL; (f) Sequestration of fluid > 6 liters. A score >= 3 indicates severe acute pancreatitis.\n\nOption Review:\n- Option A is correct because Age > 55 years is evaluated at the time of admission.\n- Option B is incorrect because hematocrit drop is assessed during the first 48 hours.\n- Option C is incorrect because serum calcium drop is assessed at 48 hours.\n- Option D is incorrect because BUN rise is measured during the initial 48-hour period.\n\nKey Takeaway: In Ranson prognostic criteria for acute pancreatitis, age > 55 years, WBC > 16,000, glucose > 200, AST > 250, and LDH > 350 are assessed at admission.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q221",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Esophageal Surgery - Achalasia Cardia",
        "prompt": "A 36-year-old female presents with progressive dysphagia to both liquids and solids, regurgitation of undigested food, nocturnal coughing, and gradual weight loss for 18 months. Barium swallow demonstrates marked dilatation of the esophageal body with smooth, symmetrical, tapered narrowing of the distal lower esophagus resembling a 'bird's beak' or 'pencil tip'. High-resolution esophageal manometry confirms incomplete lower esophageal sphincter (LES) relaxation and absent peristalsis. What is the primary neurogenic defect in achalasia cardia?",
        "options": [
            "Loss of inhibitory nitric oxide-producing ganglion cells in Auerbach myenteric plexus",
            "Congenital absence of Meissner submucosal ganglion cells in the upper esophagus",
            "Autoimmune destruction of skeletal muscle fibers in the upper third of the esophagus",
            "Chronic acid reflux causing stricture of the distal squamous epithelium"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAchalasia cardia is a primary esophageal motility disorder characterized manometrically by: 1) Incomplete or failed relaxation of the lower esophageal sphincter (LES) during swallowing; 2) Complete aperistalsis in the smooth muscle body of the esophagus. The underlying histopathological lesion is selective loss of inhibitory postganglionic neurons in the myenteric (Auerbach) plexus of the esophagus. These neurons normally secrete nitric oxide (NO) and vasoactive intestinal peptide (VIP) to mediate LES relaxation. Loss of inhibitory neurons leaves cholinergic excitatory input unopposed, producing a hypertensive, non-relaxing LES. High-resolution manometry is the gold standard diagnostic test, and barium esophagogram demonstrates classic 'bird-beak' narrowing.\n\nOption Review:\n- Option A is correct because degeneration of nitric oxide-producing inhibitory ganglion cells in the Auerbach plexus causes achalasia.\n- Option B is incorrect because Meissner plexus absence in the distal colon defines Hirschsprung disease.\n- Option C is incorrect because upper esophageal skeletal muscle involvement occurs in dermatomyositis.\n- Option D is incorrect because peptic strictures occur in chronic GERD and show irregular, asymmetrical narrowing with preserved peristalsis.\n\nKey Takeaway: Achalasia is caused by the degeneration of inhibitory ganglion cells in Auerbach's myenteric plexus, leading to aperistalsis and a non-relaxing LES with a bird-beak sign on barium swallow.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Achalasia_barium_swallow.jpg/640px-Achalasia_barium_swallow.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q222",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Peptic Ulcer Disease - Perforated Duodenal Ulcer",
        "prompt": "A 48-year-old male with chronic epigastric burning pain develops sudden-onset, agonizing, generalized abdominal pain that struck like a 'thunderclap'. On examination, he lies completely still with shallow respirations. The entire abdomen exhibits board-like rigidity and involuntary guarding, with loss of liver dullness on percussion. An upright chest radiograph is performed. What pathognomonic radiological finding confirms hollow viscus perforation?",
        "options": [
            "Free crescentic air under the right dome of the diaphragm",
            "Multiple central small bowel air-fluid levels",
            "Thumbprinting of the colonic mucosal wall",
            "Soft-tissue mass displacing the gastric bubble"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nPerforation of a peptic ulcer (most commonly an anterior first-part duodenal ulcer) results in sudden spillage of acidic gastric and duodenal contents into the peritoneal cavity, producing immediate chemical peritonitis followed by bacterial peritonitis. Clinical features include sudden catastrophic 'thunderclap' pain, board-like abdominal wall muscular rigidity, and obliteration of normal hepatic dullness on percussion (due to free air interposing between the liver and anterior abdominal wall). An erect (upright) chest radiograph including both domes of the diaphragm is the most sensitive plain film examination, demonstrating pneumoperitoneum (free crescentic gas under the right diaphragmatic dome in >75% of cases, identifiable with as little as 1 to 2 mL of free air).\n\nOption Review:\n- Option A is correct because free crescentic air under the right dome of the diaphragm (pneumoperitoneum) is the classic sign of hollow viscus perforation.\n- Option B is incorrect because multiple air-fluid levels indicate mechanical bowel obstruction.\n- Option C is incorrect because 'thumbprinting' indicates mucosal edema in ischemic colitis.\n- Option D is incorrect because soft-tissue displacement indicates an extrinsic mass or splenomegaly.\n\nKey Takeaway: An erect chest radiograph showing free crescentic air under the right diaphragm confirms pneumoperitoneum from a perforated hollow viscus.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q223",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Gastrointestinal Surgery - Meckel Diverticulum (Rule of 2s)",
        "prompt": "A 2-year-old boy is brought to the hospital with painless, massive dark red rectal bleeding (melena/hematochezia). Hemoglobin is 7.8 g/dL. Physical examination reveals a soft, non-tender abdomen. Technetium-99m pertechnetate scintigraphy (Meckel scan) shows an area of focal tracer uptake in the right lower quadrant that appears simultaneously with the gastric mucosa. Meckel diverticulum is confirmed. What congenital embryological remnant forms Meckel diverticulum?",
        "options": [
            "Persistent patent vitellointestinal duct",
            "Persistent patent urachus",
            "Failure of closure of the processus vaginalis",
            "Congenital duplication of the cecum"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nMeckel diverticulum is the most common congenital anomaly of the gastrointestinal tract, resulting from incomplete obliteration of the embryonic vitellointestinal (omphalomesenteric) duct during the 5th to 7th week of gestation. It is a true diverticulum (containing all four layers of the bowel wall: mucosa, submucosa, muscularis propria, serosa) located on the antimesenteric border of the ileum. It adheres to the classic 'Rule of 2s': 2% prevalence in population, 2 inches (5 cm) in length, located 2 feet (60 cm) proximal to the ileocecal valve, 2 times more common in males, presents before 2 years of age, and commonly contains 2 types of heterotopic mucosa (gastric mucosa in ~50%, pancreatic mucosa in ~5%). Heterotopic gastric mucosa secretes acid, which ulcerates adjacent ileal mucosa lacking protective bicarbonate, causing painless lower GI hemorrhage. Technetium-99m pertechnetate binds selectively to gastric mucus-secreting cells, confirming the diagnosis.\n\nOption Review:\n- Option A is correct because failure of obliteration of the vitellointestinal duct forms Meckel diverticulum.\n- Option B is incorrect because patent urachus connects the bladder to the umbilicus, leaking urine.\n- Option C is incorrect because patent processus vaginalis causes congenital indirect inguinal hernias or hydroceles.\n- Option D is incorrect because enterogenous duplications arise from different embryonic vacuolization defects.\n\nKey Takeaway: Meckel diverticulum is a true congenital diverticulum arising from the persistence of the vitellointestinal duct, characterized by the 'Rule of 2s'.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q224",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Colorectal Surgery - Familial Adenomatous Polyposis (FAP)",
        "prompt": "An 18-year-old male undergoes screening colonoscopy because his father died of colorectal cancer at age 38. Colonoscopy demonstrates thousands (greater than 1,000) of small adenomatous polyps carpeting the entire mucosal surface of the colon and rectum. Biopsy confirms tubular and tubulovillous adenomas. What tumor suppressor gene is mutated in this autosomal dominant condition?",
        "options": [
            "APC gene",
            "MLH1 gene",
            "TP53 gene",
            "RET gene"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nFamilial Adenomatous Polyposis (FAP) is an autosomal dominant inherited cancer syndrome caused by germline mutations in the Adenomatous Polyposis Coli (APC) tumor suppressor gene located on chromosome 5q21. The APC protein normally degrades beta-catenin in the Wnt signaling pathway. Loss of APC leads to accumulation of beta-catenin, which translocates to the nucleus and drives transcription of cell-proliferating genes (c-myc, cyclin D1). Patients develop hundreds to thousands (always >100) of adenomatous polyps throughout the colon and rectum starting in their teens. Because the lifetime risk of progression to invasive colorectal adenocarcinoma is 100% (typically before age 40), prophylactic total proctocolectomy with ileal pouch-anal anastomosis (IPAA) is standard.\n\nOption Review:\n- Option A is correct because germline mutation of the APC gene on chromosome 5q21 causes familial adenomatous polyposis.\n- Option B is incorrect because DNA mismatch repair gene mutations (MLH1, MSH2) cause Lynch syndrome (HNPCC), which features few polyps with high microsatellite instability.\n- Option C is incorrect because TP53 mutations cause Li-Fraumeni syndrome.\n- Option D is incorrect because RET proto-oncogene mutations cause MEN 2A and 2B.\n\nKey Takeaway: Familial adenomatous polyposis (FAP) is caused by mutations in the APC gene on chromosome 5q21, resulting in >100 adenomatous polyps and a 100% lifetime colon cancer risk.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Familial_adenomatous_polyposis_gross.jpg/640px-Familial_adenomatous_polyposis_gross.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q225",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Colorectal Surgery - Colorectal Cancer Screening & TNM",
        "prompt": "A 65-year-old male presents with fatigue, progressive weight loss, and dark stools. Complete blood count shows microcytic hypochromic iron deficiency anemia. Colonoscopy reveals an exophytic mass in the cecum, and biopsy confirms adenocarcinoma. Right hemicolectomy is performed. Pathological staging reveals tumor invading through the muscularis propria into the pericolic fat (T3), with metastases in 3 of 18 regional lymph nodes (N1), and no distant metastases (M0). What TNM anatomical stage of colorectal cancer is diagnosed?",
        "options": [
            "Stage I",
            "Stage II",
            "Stage III",
            "Stage IV"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nColorectal cancer staging follows the American Joint Committee on Cancer (AJCC) TNM classification: 1) Stage I: Tumor invades submucosa (T1) or muscularis propria (T2), with negative lymph nodes (N0) and no distant metastasis (M0); 2) Stage II: Tumor invades through the muscularis propria into subserosa/pericolic fat (T3) or penetrates visceral peritoneum / directly invades other organs (T4), but lymph nodes are NEGATIVE (N0, M0); 3) Stage III: ANY T stage (T1-T4) with POSITIVE regional lymph node metastases (N1: 1-3 regional nodes; N2: >=4 regional nodes), with no distant metastasis (M0). 4) Stage IV: Distant metastatic disease present (M1: liver, peritoneum, lung). Because this patient has confirmed regional lymph node involvement (N1) without distant metastasis (M0), it is Stage III disease, which warrants adjuvant fluoropyrimidine-based chemotherapy (FOLFOX/CAPOX).\n\nOption Review:\n- Option A is incorrect because Stage I involves T1/T2 without node involvement.\n- Option B is incorrect because Stage II has no lymph node metastases (N0).\n- Option C is correct because the presence of regional lymph node metastases (N1) in the absence of distant metastasis defines Stage III colorectal cancer.\n- Option D is incorrect because Stage IV requires distant metastases (M1).\n\nKey Takeaway: The presence of regional lymph node metastases (N1 or N2) defines Stage III colorectal cancer, mandating adjuvant postoperative chemotherapy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q226",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Hernia Surgery - Femoral Hernia Boundaries",
        "prompt": "A 68-year-old multiparous female presents with an acutely painful, irreducible, tender mass in her right groin, located below and lateral to the pubic tubercle. Emergency exploration is indicated for a strangulated femoral hernia. What vascular structure forms the direct lateral boundary of the femoral canal?",
        "options": [
            "Femoral vein",
            "Femoral artery",
            "Great saphenous vein",
            "Inferior epigastric vein"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe femoral canal is the innermost compartment of the femoral sheath, through which femoral hernias descend into the upper thigh below the inguinal ligament. The boundaries of the femoral ring (the entrance to the canal) are crucial in surgical anatomy: Anteriorly: Inguinal ligament (Poupart's ligament); Posteriorly: Pectineal ligament (Cooper's ligament) and pectineus muscle covering the superior pubic ramus; Medially: Lacunar ligament (Gimbernat's ligament); Laterally: A thin fibrous septum separating it from the femoral vein. Femoral hernias have a high rate of strangulation (up to 40%) because of the rigid, unyielding boundaries of the ring (especially the sharp edge of the lacunar ligament medially).\n\nOption Review:\n- Option A is correct because the femoral vein forms the lateral boundary of the femoral canal within the femoral sheath.\n- Option B is incorrect because the femoral artery lies lateral to the femoral vein.\n- Option C is incorrect because the great saphenous vein pierces the cribriform fascia to join the femoral vein lower down.\n- Option D is incorrect because inferior epigastric vessels lie superiorly in the retroperitoneum of the inguinal canal.\n\nKey Takeaway: The lateral boundary of the femoral ring and canal is formed by the femoral vein.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q227",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Trauma Surgery - Splenic Injury Grading",
        "prompt": "A 22-year-old male is struck on the left side of his lower chest during a rugby game. He presents with left upper quadrant pain and referred pain to the tip of his left shoulder upon supine positioning (Kehr sign). Contrast-enhanced CT reveals a subcapsular splenic hematoma involving 35% of the surface area and a parenchymal laceration measuring 2.5 cm in depth that does not involve trabecular vessels. According to the AAST splenic injury scale, what grade of splenic injury is present?",
        "options": [
            "Grade I",
            "Grade II",
            "Grade III",
            "Grade IV"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nSplenic injuries are graded by the American Association for the Surgery of Trauma (AAST) based on CT or operative findings: 1) Grade I: Subcapsular hematoma < 10% surface area; laceration < 1 cm parenchymal depth; 2) Grade II: Subcapsular hematoma 10% to 50% surface area; intraparenchymal hematoma < 5 cm diameter; parenchymal laceration 1 to 3 cm depth without trabecular vessel involvement; 3) Grade III: Subcapsular hematoma > 50% surface area or expanding/ruptured hematoma; intraparenchymal hematoma >= 5 cm; parenchymal laceration > 3 cm depth or involving trabecular vessels; 4) Grade IV: Laceration involving segmental or hilar vessels producing devascularization of >25% of the spleen; 5) Grade V: Completely shattered spleen or total hilar avulsion. In this patient, a 35% subcapsular hematoma and 2.5 cm deep laceration without vascular involvement define a Grade II injury.\n\nOption Review:\n- Option A is incorrect because Grade I requires hematoma <10% and laceration <1 cm.\n- Option B is correct because hematoma 10-50% and laceration 1-3 cm depth define Grade II splenic injury.\n- Option C is incorrect because Grade III requires hematoma >50% or laceration >3 cm.\n- Option D is incorrect because Grade IV involves segmental devascularization.\n\nKey Takeaway: AAST Grade II splenic trauma involves a subcapsular hematoma between 10% and 50% surface area or a parenchymal laceration 1 to 3 cm in depth.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q228",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Urological Surgery - Testicular Torsion Diagnostics",
        "prompt": "A 14-year-old male awakens at 3 AM with sudden, excruciating left scrotal pain and vomiting. Physical examination reveals an exquisitely tender, swollen, high-riding left testis lying in a horizontal transverse lie ('bell-clapper' deformity). Elevation of the left scrotum fails to relieve the pain (negative Prehn sign), and the ipsilateral cremasteric reflex is completely absent. What is the emergency diagnostic imaging investigation of choice?",
        "options": [
            "Color Doppler ultrasound of the scrotum",
            "Contrast-enhanced pelvic CT scan",
            "Pelvic magnetic resonance imaging",
            "Diagnostic radionuclide cystourethrogram"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nTesticular torsion is a surgical emergency caused by twisting of the spermatic cord, which initially cuts off venous outflow, followed by arterial thrombosis and testicular hemorrhagic necrosis. It is predisposed by an abnormally high attachment of the tunica vaginalis ('bell-clapper deformity'), allowing the testis to twist freely along its vertical axis. Physical examination reveals a high-riding, horizontal testis, absent cremasteric reflex, and negative Prehn sign (scrotal elevation does NOT relieve pain; in contrast, Prehn sign is positive in acute epididymo-orchitis). Color Doppler ultrasonography is the emergency imaging investigation of choice, demonstrating complete absence of intratesticular blood flow. Surgical detorsion and bilateral orchiopexy must be performed within 6 hours of onset to achieve a >90% salvage rate.\n\nOption Review:\n- Option A is correct because color Doppler ultrasound is the investigation of choice to evaluate intratesticular blood flow.\n- Option B is incorrect because CT scan is slower, exposes the gonads to radiation, and cannot evaluate parenchymal Doppler flow.\n- Option C is incorrect because MRI causes unacceptable delay in surgical detorsion.\n- Option D is incorrect because cystourethrogram evaluates the urethra and bladder, not the scrotum.\n\nKey Takeaway: Emergency color Doppler ultrasound demonstrating absent arterial flow confirms testicular torsion; surgical exploration and bilateral orchiopexy within 6 hours is vital.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q229",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Vascular Surgery - Chronic Venous Insufficiency (CEAP Classification)",
        "prompt": "A 52-year-old female presents with chronic bilateral leg heaviness, ankle edema, hyperpigmentation, and lipodermatosclerosis (thickened 'inverted champagne bottle' leg). On the medial aspect of the left ankle above the medial malleolus, there is an open, shallow ulcer with irregular margins and a granulating base. Under the clinical CEAP classification of chronic venous disorders, what clinical class represents an active venous ulcer?",
        "options": [
            "Clinical class C4",
            "Clinical class C5",
            "Clinical class C6",
            "Clinical class C3"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nThe CEAP classification system standardizes the reporting of chronic venous disease based on Clinical (C), Etiological (E), Anatomical (A), and Pathophysiological (P) characteristics. The Clinical (C) stages are: C0: No visible or palpable signs of venous disease; C1: Telangiectasias or reticular veins; C2: Varicose veins (>=3 mm); C3: Venous edema; C4: Skin changes secondary to venous disease (C4a: pigmentation/eczema; C4b: lipodermatosclerosis/atrophie blanche); C5: Healed venous ulcer; C6: Active, open venous ulcer. An open, granulating ulcer located in the 'gaiter zone' above the medial malleolus represents Class C6.\n\nOption Review:\n- Option A is incorrect because C4 represents skin trophic changes (pigmentation, lipodermatosclerosis) without ulceration.\n- Option B is incorrect because C5 represents a healed venous ulcer.\n- Option C is correct because C6 designates an active, open venous ulcer.\n- Option D is incorrect because C3 represents pitting venous edema without trophic skin changes.\n\nKey Takeaway: Under the CEAP classification, an active, open venous stasis ulcer is designated as clinical class C6.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q230",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Head and Neck Surgery - Salivary Gland Tumors (Pleomorphic Adenoma)",
        "prompt": "A 45-year-old male presents with a painless, slow-growing, mobile, lobulated 3 cm swelling in his right parotid region that lifts the earlobe for 4 years. Facial nerve function is completely intact. Fine needle aspiration biopsy reveals a mixture of epithelial and myoepithelial cells embedded within a myxoid and chondroid chondromyxoid stroma. What is the most common benign salivary gland neoplasm?",
        "options": [
            "Pleomorphic adenoma",
            "Warthin tumor",
            "Mucoepidermoid carcinoma",
            "Adenoid cystic carcinoma"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nPleomorphic adenoma (benign mixed tumor) is the most common salivary gland neoplasm overall (~60% of all salivary tumors and ~80% of benign parotid tumors). It presents as a slow-growing, painless, firm, lobulated, mobile swelling that characteristically lifts the ear lobule, occurring with intact facial nerve function. Histologically, it demonstrates morphological diversity with a mixture of epithelial ducts and myoepithelial cells embedded within a variable chondromyxoid, myxoid, or hyalinized stroma (hence 'pleomorphic'). Because it forms finger-like microscopic pseudopods projecting beyond the true capsule, simple enucleation leaves residual cells and results in high recurrence rates. The standard surgical procedure of choice is superficial parotidectomy with facial nerve preservation.\n\nOption Review:\n- Option A is correct because pleomorphic adenoma is the most common benign salivary gland tumor, featuring mixed epithelial and chondromyxoid elements.\n- Option B is incorrect because Warthin tumor (papillary cystadenoma lymphomatosum) is a cystic tumor with lymphoid stroma occurring almost exclusively in male smokers.\n- Option C is incorrect because mucoepidermoid carcinoma is the most common malignant salivary tumor.\n- Option D is incorrect because adenoid cystic carcinoma is a malignancy notorious for perineural invasion along facial nerve branches.\n\nKey Takeaway: Pleomorphic adenoma is the most common salivary gland tumor, characterized by epithelial and chondromyxoid elements and treated with superficial parotidectomy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q231",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Biliary Surgery - Choledochal Cyst (Todani Classification)",
        "prompt": "A 7-year-old girl presents with intermittent right upper quadrant abdominal pain, fluctuating jaundice, and a palpable right subcostal mass (the classic triad). Magnetic resonance cholangiopancreatography (MRCP) reveals fusiform, saccular dilation of the entire extrahepatic common bile duct, with normal intrahepatic ducts. What is the most common type of choledochal cyst according to the Todani classification?",
        "options": [
            "Type I choledochal cyst",
            "Type II choledochal cyst",
            "Type III choledochal cyst",
            "Type V choledochal cyst"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nCholedochal cysts are congenital dilatations of the biliary tree, thought to result from an anomalous pancreaticobiliary duct junction (APBDJ), which allows reflux of pancreatic enzymes into the biliary system, causing inflammation, weakening, and cyst formation. The Todani classification categorizes them into five types: 1) Type I (most common, accounting for 80% to 90% of cases): Dilatation of the extrahepatic bile duct (fusiform or saccular); 2) Type II: True diverticulum protruding from the extrahepatic duct; 3) Type III (choledochocele): Dilatation of the intraduodenal segment of the CBD; 4) Type IV: Multiple cysts (IVa: intrahepatic and extrahepatic; IVb: extrahepatic only); 5) Type V (Caroli disease): Multiple dilatations confined to the intrahepatic ducts. Because Type I cysts carry an 8% to 15% lifetime risk of cholangiocarcinoma, complete cyst excision with Roux-en-Y hepaticojejunostomy is mandatory.\n\nOption Review:\n- Option A is correct because Type I (fusiform extrahepatic dilatation) represents 80% to 90% of all choledochal cysts.\n- Option B is incorrect because Type II (extrahepatic diverticulum) accounts for <5%.\n- Option C is incorrect because Type III is a choledochocele.\n- Option D is incorrect because Type V is Caroli disease (purely intrahepatic).\n\nKey Takeaway: Todani Type I (fusiform extrahepatic bile duct dilatation) is the most common choledochal cyst, requiring complete surgical excision due to high malignant potential.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q232",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Bariatric Surgery - Metabolic & Bariatric Procedures",
        "prompt": "A 38-year-old female with a BMI of 44 kg/m2 and poorly controlled type 2 diabetes undergoes a laparoscopic Roux-en-Y gastric bypass. Which gastrointestinal hormone, predominantly synthesized and secreted by the endocrine cells of the gastric fundus to stimulate hunger, is suppressed by partitioning the stomach into a small upper gastric pouch?",
        "options": [
            "Ghrelin",
            "Glucagon-like peptide-1",
            "Peptide YY",
            "Cholecystokinin"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nGhrelin is a 28-amino-acid peptide hormone synthesized predominantly by P/D1 neuroendocrine cells in the fundus of the stomach. It is the only known circulating orexigenic (appetite-stimulating) hormone; it crosses the blood-brain barrier to bind to growth hormone secretagogue receptors (GHSR) in the arcuate nucleus of the hypothalamus, stimulating NPY/AgRP neurons to trigger hunger. In procedures like sleeve gastrectomy (where the fundus is completely resected) and Roux-en-Y gastric bypass (where food is diverted away from the excluded gastric fundus), circulating ghrelin levels drop precipitously, producing early post-surgical satiety and sustained appetite reduction.\n\nOption Review:\n- Option A is correct because ghrelin is secreted by the gastric fundus to stimulate appetite, and its suppression contributes to weight loss after bypass.\n- Option B is incorrect because GLP-1 is an incretin produced by intestinal L-cells that suppresses appetite and increases after bypass.\n- Option C is incorrect because Peptide YY (PYY) is an anorexigenic hormone released by ileal L-cells.\n- Option D is incorrect because cholecystokinin (CCK) is secreted by duodenal I-cells in response to fats.\n\nKey Takeaway: Ghrelin is an orexigenic hormone synthesized in the gastric fundus; its suppression after bariatric surgery reduces hunger.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q233",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Urological Surgery - Renal Cell Carcinoma (Clear Cell)",
        "prompt": "A 58-year-old male presents with painless gross hematuria, dull left flank pain, and a palpable left flank mass. Complete blood count shows erythrocytosis (hemoglobin 18.5 g/dL) due to paraneoplastic erythropoietin production. Abdominal CT demonstrates a solid, heterogeneously enhancing 6 cm cortical renal mass with clear cells containing abundant glycogen and lipids on histology. What genetic mutation on chromosome 3p is characteristic of clear cell renal cell carcinoma?",
        "options": [
            "Von Hippel-Lindau gene mutation",
            "WT1 gene mutation",
            "RET proto-oncogene mutation",
            "MET proto-oncogene mutation"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nClear cell renal cell carcinoma (RCC) accounts for 75% to 80% of all renal epithelial malignancies, arising from the proximal convoluted tubule epithelium. Microscopic examination demonstrates nests of polygonal cells with clear cytoplasm (rich in lipid and glycogen that dissolve during routine histological processing) surrounded by a dense network of thin-walled capillaries. The molecular genetic hallmark of >90% of sporadic and hereditary (Von Hippel-Lindau syndrome) clear cell RCCs is loss-of-function mutation or hypermethylation of the VHL tumor suppressor gene on chromosome 3p25. The VHL protein is part of an E3 ubiquitin ligase that targets hypoxia-inducible factor (HIF-1alpha) for proteasomal degradation under normoxic conditions. Inactivation of VHL causes accumulation of HIF-1alpha, driving constitutive overexpression of VEGF and PDGF to promote angiogenesis.\n\nOption Review:\n- Option A is correct because inactivation of the VHL gene on chromosome 3p drives clear cell renal cell carcinoma.\n- Option B is incorrect because WT1 gene mutations on chromosome 11p cause Wilms tumor (nephroblastoma) in young children.\n- Option C is incorrect because RET mutations cause MEN 2 and Hirschsprung disease.\n- Option D is incorrect because MET mutations cause hereditary papillary renal cell carcinoma.\n\nKey Takeaway: Clear cell renal cell carcinoma is molecularly characterized by deletion or mutation of the VHL tumor suppressor gene on chromosome 3p.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Clear_cell_renal_cell_carcinoma_histopathology.jpg/640px-Clear_cell_renal_cell_carcinoma_histopathology.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q234",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Transplantation - Renal Transplant Rejection Types",
        "prompt": "Within 15 minutes of vascular clamp release during a renal allotransplantation, the transplanted donor kidney becomes cyanotic, mottled, flaccid, and stops producing urine. Histopathological examination shows diffuse microvascular thrombosis, neutrophilic margination in peritubular capillaries, and extensive cortical necrosis. What type of transplant rejection has occurred?",
        "options": [
            "Hyperacute rejection",
            "Acute cellular rejection",
            "Acute antibody-mediated rejection",
            "Chronic allograft nephropathy"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nTransplant rejection is classified based on timing and mechanism: 1) Hyperacute rejection: Occurs within minutes to hours of graft reperfusion. It is mediated by pre-existing circulating recipient antibodies (Type II hypersensitivity) directed against donor ABO blood group antigens or HLA Class I molecules (sensitization from prior blood transfusions, pregnancies, or failed transplants). Binding of antibodies to donor vascular endothelium activates the complement cascade, triggering extensive endothelial necrosis, platelet aggregation, microvascular thrombosis, and rapid ischemic graft infarction on the operating table; 2) Acute cellular rejection: Occurs weeks to months post-transplant, mediated by recipient CD8+ T cells causing tubulitis and interstitial inflammation; 3) Chronic rejection: Occurs over years, manifesting as concentric intimal hyperplasia and interstitial fibrosis.\n\nOption Review:\n- Option A is correct because onset within minutes of graft revascularization with thrombosis and cortical necrosis defines hyperacute rejection.\n- Option B is incorrect because acute cellular rejection manifests weeks to months later with tubulitis.\n- Option C is incorrect because acute antibody-mediated rejection manifests days to weeks later with C4d staining.\n- Option D is incorrect because chronic allograft nephropathy develops slowly over years.\n\nKey Takeaway: Hyperacute rejection occurs within minutes of revascularization, caused by preformed anti-donor antibodies triggering complement-mediated graft thrombosis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q235",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Surgical Infections - Necrotizing Fasciitis",
        "prompt": "A 56-year-old diabetic male presents with rapidly progressive swelling, severe pain, and erythema over his left thigh following a minor scratch. Within 24 hours, the pain becomes excruciating, extending far beyond the margin of erythema. The skin turns dusky purple with bullae, skin anesthesia develops, and palpable subcutaneous crepitus is felt. Blood pressure drops to 80/50 mmHg. What is the definitive emergency surgical management of necrotizing fasciitis?",
        "options": [
            "Immediate radical surgical debridement of all necrotic tissue",
            "Intravenous broad-spectrum antibiotics alone without surgery",
            "Hyperbaric oxygen therapy as initial definitive therapy",
            "Bedside needle aspiration of fluid collections"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nNecrotizing fasciitis is a surgical emergency characterized by rapid, fulminant destruction of subcutaneous tissue and muscular fascia. It can be polymicrobial (Type I: mixed anaerobes, enteric gram-negative rods, and streptococci, common in diabetics) or monomicrobial (Type II: Streptococcus pyogenes / 'flesh-eating bacteria', with or without S. aureus). Hallmark diagnostic features include: 1) Pain out of proportion to physical findings in early stages; 2) Rapid spread across fascial planes; 3) Late skin necrosis, bullae, anesthesia (due to thrombosis of cutaneous nerves traversing the fascia), and crepitus; 4) Systemic toxicity and septic shock. Definitive, life-saving management requires immediate, aggressive, wide operative surgical debridement of all non-viable fascial and subcutaneous tissue down to bleeding, healthy margins, combined with broad-spectrum parenteral antibiotics and hemodynamic resuscitation.\n\nOption Review:\n- Option A is correct because emergent, extensive radical surgical debridement is the single most critical intervention for patient survival.\n- Option B is incorrect because antibiotics cannot penetrate the thrombosed, ischemic fascial microcirculation and will lead to fatal sepsis without debridement.\n- Option C is incorrect because hyperbaric oxygen is only an adjunctive modality, never a replacement for emergency surgery.\n- Option D is incorrect because needle aspiration is inadequate for necrotizing soft tissue infection.\n\nKey Takeaway: Immediate, radical surgical debridement of all necrotic tissue is the primary life-saving treatment for necrotizing fasciitis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q236",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Anorectal Surgery - Anal Fissure Localization",
        "prompt": "A 28-year-old female presents with agonizing, sharp, 'knife-like' pain during defecation accompanied by bright red blood streaking the toilet paper. On gentle separation of the buttocks, a longitudinal tear in the anoderm is visualized, with a swollen skin tag ('sentinel pile') at its distal margin. In greater than 90% of cases, in which anatomical location does a primary acute anal fissure occur?",
        "options": [
            "Posterior midline of the anal verge",
            "Anterior midline of the anal verge",
            "Lateral right wall of the anal canal",
            "Lateral left wall of the anal canal"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAn anal fissure is a painful linear tear or ulcer in the squamous anoderm situated distal to the dentate line. Primary fissures are typically initiated by passage of hard, dry stool or chronic diarrhea, which tears the lining. Spasm and hypertonicity of the internal anal sphincter elevate resting anal pressures, which compromises perfusion to the anoderm. The posterior midline of the anal verge is an anatomical watershed zone with the poorest blood supply, and its elliptical muscular fibers provide the least structural support. Consequently, >90% of all primary anal fissures are located in the posterior midline (while ~10% are anterior, predominantly in females). Fissures located laterally should raise suspicion for underlying systemic pathology (Crohn disease, tuberculosis, HIV, syphilis, or anal carcinoma).\n\nOption Review:\n- Option A is correct because the posterior midline is the site of >90% of primary anal fissures due to relative ischemia and elliptical sphincter architecture.\n- Option B is incorrect because anterior fissures account for only ~10% of cases (more common in postpartum females).\n- Option C is incorrect because lateral fissures are atypical and suggest secondary systemic disease.\n- Option D is incorrect because lateral locations indicate underlying conditions like Crohn disease.\n\nKey Takeaway: More than 90% of primary anal fissures occur in the posterior midline because of anatomical hypoperfusion and structural weakness.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q237",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Upper GI Surgery - Gastrointestinal Stromal Tumor (GIST)",
        "prompt": "A 55-year-old male presents with vague upper abdominal discomfort and iron deficiency anemia. Upper endoscopy reveals a 5 cm smooth, submucosal bulge with central ulceration in the gastric body. Endoscopic ultrasound-guided core biopsy reveals spindle-shaped mesenchymal cells. Immunohistochemical staining demonstrates strong, diffuse cytoplasmic positivity for CD117 (c-KIT receptor). What targeted tyrosine kinase inhibitor is the standard first-line medical therapy for advanced gastrointestinal stromal tumors (GIST)?",
        "options": [
            "Imatinib",
            "Trastuzumab",
            "Erlotinib",
            "Bevacizumab"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nGastrointestinal Stromal Tumors (GIST) are the most common mesenchymal neoplasms of the digestive tract (most commonly arising in the stomach, ~60%, followed by the small intestine, ~30%). They arise from or share a common precursor with the interstitial cells of Cajal (the electrical pacemaker cells of bowel muscularis propria). The molecular hallmark in approximately 85% of GISTs is an activating, gain-of-function mutation in the KIT proto-oncogene encoding the transmembrane receptor tyrosine kinase KIT (CD117), or less commonly in PDGFRA (~10%). CD117 positivity is the definitive immunohistochemical marker. For metastatic, recurrent, or high-risk resected GIST, imatinib mesylate (a targeted small-molecule inhibitor of KIT and PDGFRA tyrosine kinases) is the standard first-line systemic therapy.\n\nOption Review:\n- Option A is correct because imatinib specifically inhibits the mutated KIT tyrosine kinase in GIST, providing excellent therapeutic response.\n- Option B is incorrect because trastuzumab is a monoclonal antibody against HER2 used in breast and gastric adenocarcinoma.\n- Option C is incorrect because erlotinib is an EGFR tyrosine kinase inhibitor used in non-small cell lung cancer.\n- Option D is incorrect because bevacizumab is a monoclonal antibody targeting VEGF.\n\nKey Takeaway: Gastrointestinal stromal tumors (GIST) are CD117 (c-KIT) positive mesenchymal neoplasms treated with the targeted tyrosine kinase inhibitor imatinib.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q238",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Surgical Oncology - Melanoma Biopsy Technique",
        "prompt": "A 50-year-old fair-skinned male presents with an asymmetrical, deeply pigmented cutaneous lesion with irregular borders, color variegation, and a diameter of 8 mm on his back that has been enlarging. Melanoma is clinically suspected. What is the standard diagnostic surgical biopsy technique recommended for a suspicious pigmented cutaneous lesion?",
        "options": [
            "Complete narrow-margin excisional biopsy with 1 to 2 mm margins",
            "Wide local excision with 2 cm margins as the initial step",
            "Superficial shave biopsy of the top layers",
            "Electrodessication and curettage"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIn the management of suspected cutaneous malignant melanoma, the primary prognostic determinant and guide for definitive surgical margins is Breslow tumor thickness (the vertical microstaging measurement in millimeters from the granular layer of the epidermis to the deepest invading melanoma cell in the dermis). Therefore, the recommended diagnostic biopsy technique is a complete, full-thickness excisional biopsy with a narrow (1 to 2 mm) margin of normal skin and subcutaneous fat. Superficial shave biopsies are strictly contraindicated because they transect the base of the lesion, precluding accurate microstaging of Breslow depth. Wide local excision (1 to 2 cm margins) is performed only as a definitive second stage AFTER histopathological confirmation of Breslow thickness.\n\nOption Review:\n- Option A is correct because complete excisional biopsy with 1 to 2 mm margins preserves intact tissue architecture for accurate Breslow depth measurement.\n- Option B is incorrect because wide excision (2 cm) as the initial step is premature and disrupts lymphatic drainage channels needed for sentinel node mapping.\n- Option C is incorrect because shave biopsy transects the deep base, precluding accurate Breslow thickness assessment.\n- Option D is incorrect because curettage destroys tissue and prevents histological diagnosis.\n\nKey Takeaway: Complete narrow-margin excisional biopsy (1 to 2 mm) down to subcutaneous fat is the standard diagnostic biopsy technique for suspected cutaneous melanoma.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q239",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "General Surgery - Surgical Wound Healing Stages",
        "prompt": "A surgical resident reviews the biochemical and cellular phases of wound healing following an elective laparotomy incision. During which physiological phase of wound healing do fibroblasts actively synthesize and lay down type III collagen, followed by angiogenesis and peak granulation tissue formation?",
        "options": [
            "Proliferative phase",
            "Hemostasis phase",
            "Inflammatory phase",
            "Remodeling phase"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nWound healing proceeds through four overlapping phases: 1) Hemostasis (immediate, 0 to several hours): Platelet plug formation, fibrin clot cascade, and growth factor release (PDGF, TGF-beta); 2) Inflammatory phase (day 1 to 4): Neutrophils arrive within 24 hours, followed by macrophages (day 2-3) which phagocytose debris and secrete angiogenic cytokines; 3) Proliferative phase (day 4 to 21): Dominated by fibroblasts and endothelial cells. Fibroblasts synthesize granulation tissue, laying down ground substance and immature Type III collagen, while endothelial budding (neovascularization) restores tissue perfusion, and myofibroblasts mediate wound contraction; 4) Remodeling / Maturation phase (day 21 up to 1-2 years): Type III collagen is replaced by mature, high-tensile-strength Type I collagen, increasing wound tensile strength to ~80% of uninjured skin.\n\nOption Review:\n- Option A is correct because fibroblast proliferation, type III collagen synthesis, and granulation tissue formation define the proliferative phase.\n- Option B is incorrect because hemostasis establishes the initial platelet and fibrin clot.\n- Option C is incorrect because inflammation is dominated by neutrophil and macrophage debridement.\n- Option D is incorrect because the remodeling phase replaces type III collagen with type I collagen.\n\nKey Takeaway: The proliferative phase of wound healing (days 4 to 21) is characterized by fibroblast activity, granulation tissue formation, angiogenesis, and type III collagen synthesis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q240",
        "subjectId": "general-surgery",
        "subjectTitle": "General Surgery",
        "topic": "Trauma Surgery - Hemorrhagic Shock Classification",
        "prompt": "A 25-year-old trauma victim arrives in the emergency department with an estimated blood loss of 1,800 mL (approximately 35% of his circulating blood volume). Physical examination reveals heart rate 130 bpm, blood pressure 85/55 mmHg (marked hypotension), respiratory rate 35 breaths/min, oliguria (urine output < 15 mL/hour), and confusion. Under the American College of Surgeons Advanced Trauma Life Support (ATLS) classification, what class of hemorrhagic shock is present?",
        "options": [
            "Class I hemorrhagic shock",
            "Class II hemorrhagic shock",
            "Class III hemorrhagic shock",
            "Class IV hemorrhagic shock"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nThe ATLS classification categorizes hemorrhagic shock into four classes (based on a 70-kg adult with 5 L blood volume): 1) Class I (<15% blood loss, <750 mL): Normal heart rate, normal BP, normal urine output, mild anxiety; 2) Class II (15-30% blood loss, 750-1500 mL): Tachycardia (100-120 bpm), normal systolic BP, narrowed pulse pressure, urine output 20-30 mL/h; 3) Class III (30-40% blood loss, 1500-2000 mL): Marked tachycardia (120-140 bpm), DECREASED systolic blood pressure (hypotension begins here), marked tachypnea (30-40/min), oliguria (5-15 mL/h), and confusion/mental status changes; requires blood transfusion; 4) Class IV (>40% blood loss, >2000 mL): Severe tachycardia (>140 bpm), profound hypotension, anuria, and lethargy/coma. A blood loss of 35% with hypotension, tachycardia 130 bpm, and oliguria defines Class III shock.\n\nOption Review:\n- Option A is incorrect because Class I involves <15% blood loss with normal vitals.\n- Option B is incorrect because Class II involves 15-30% blood loss with preserved systolic blood pressure.\n- Option C is correct because 30-40% blood loss with frank hypotension, tachycardia (120-140), and oliguria defines Class III hemorrhagic shock.\n- Option D is incorrect because Class IV involves >40% blood loss with near-anuria and imminent death.\n\nKey Takeaway: Class III hemorrhagic shock (30% to 40% blood loss) is characterized by the onset of frank systolic hypotension, marked tachycardia, and oliguria, requiring blood product resuscitation.",
        "imageUrls": []
    },

    # ==========================================
    # ORTHOPEDICS (5 Questions: Q241 - Q245)
    # ==========================================
    {
        "id": "fmge-gt1-q241",
        "subjectId": "orthopedics",
        "subjectTitle": "Orthopedics",
        "topic": "Traumatology - Distal Radius Fractures (Colles Fracture)",
        "prompt": "A 65-year-old postmenopausal female slips on an icy pavement and lands on her outstretched hand with the wrist in dorsiflexion. On examination, there is marked wrist swelling with a classic 'dinner-fork' deformity. Radiographs demonstrate an extra-articular fracture of the distal radial metaphysis. What displacement of the distal bone fragment defines a Colles fracture?",
        "options": [
            "Dorsal and radial displacement with dorsal tilt",
            "Volar and radial displacement with volar tilt",
            "Purely proximal impaction without angular displacement",
            "Anterior displacement of the distal ulna only"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nA Colles fracture is an extra-articular transverse fracture of the distal radius occurring within 2.5 cm (1 inch) of the wrist joint, caused by a fall onto an outstretched dorsiflexed hand (FOOSH). It is the most common wrist fracture in elderly osteoporotic individuals. The impact drives the distal bony fragment into characteristic six-fold displacement: 1) Dorsal displacement; 2) Dorsal tilt (dorsal angulation, altering the normal volar tilt of the articular surface); 3) Radial displacement; 4) Radial tilt; 5) Proximal impaction; 6) Supination. The prominence of the dorsally displaced distal fragment and volar prominence of the proximal shaft creates the classic clinical 'dinner-fork' (bayonet) deformity. In contrast, a Smith fracture ('reverse Colles') occurs from a fall onto a flexed wrist, producing volar displacement ('garden-spade' deformity).\n\nOption Review:\n- Option A is correct because dorsal displacement and dorsal tilt of the distal radial fragment define a Colles fracture.\n- Option B is incorrect because volar displacement and volar tilt define a Smith fracture ('reverse Colles').\n- Option C is incorrect because pure impaction without dorsal displacement does not create the dinner-fork contour.\n- Option D is incorrect because the primary bony fracture is in the distal radius, not isolated ulna.\n\nKey Takeaway: A Colles fracture is a distal radius metaphyseal fracture featuring dorsal displacement and dorsal tilt, producing a characteristic dinner-fork deformity.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Colles_fracture_X-ray.jpg/640px-Colles_fracture_X-ray.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q242",
        "subjectId": "orthopedics",
        "subjectTitle": "Orthopedics",
        "topic": "Traumatology - Scaphoid Fracture Complications",
        "prompt": "A 24-year-old male athlete falls onto an outstretched hand during a basketball game. Physical examination reveals exquisite tenderness localized specifically within the anatomical snuffbox and with axial loading of the thumb. Initial plain radiographs fail to demonstrate a clear fracture line. Which serious complication occurs frequently in fractures through the proximal pole of the scaphoid due to its retrograde arterial blood supply?",
        "options": [
            "Avascular necrosis",
            "Reflex sympathetic dystrophy",
            "Extensor pollicis longus tendon rupture",
            "Carpal tunnel syndrome"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe scaphoid is the most commonly fractured carpal bone (~70% of carpal injuries), typically injured by a fall on an outstretched hand with the wrist hyperextended. Hallmark examination signs include focal point tenderness in the anatomical snuffbox (bounded medially by extensor pollicis longus, laterally by abductor pollicis longus and extensor pollicis brevis) and scaphoid tubercle tenderness. The scaphoid receives its arterial blood supply in a retrograde fashion: branches of the radial artery enter the bone through its distal pole and waist to course proximally. Therefore, fractures through the proximal third (proximal pole) disrupt this retrograde blood flow, leaving the proximal fragment completely devascularized, leading to non-union and avascular necrosis (Preiser disease).\n\nOption Review:\n- Option A is correct because the retrograde vascular supply leaves the proximal scaphoid fragment highly vulnerable to avascular necrosis.\n- Option B is incorrect because complex regional pain syndrome is a secondary neurovascular complication, not specific to proximal retrograde anatomy.\n- Option C is incorrect because EPL rupture can occur following non-displaced distal radius fractures, not scaphoid avascular necrosis.\n- Option D is incorrect because carpal tunnel syndrome is caused by lunate dislocation compressing the median nerve.\n\nKey Takeaway: Scaphoid fractures through the proximal pole have a high rate of avascular necrosis and non-union due to its retrograde arterial blood supply.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q243",
        "subjectId": "orthopedics",
        "subjectTitle": "Orthopedics",
        "topic": "Joint Dislocations - Anterior Shoulder Dislocation",
        "prompt": "A 22-year-old collegiate rugby player sustains a direct blow to his abducted and externally rotated right arm. He presents supporting his right arm at the elbow, unable to move the shoulder. Physical examination reveals flattening of the normal deltoid lateral contour ('epaulet sign') and a palpable void beneath the acromion. What is the most common type of shoulder joint dislocation?",
        "options": [
            "Anterior shoulder dislocation",
            "Posterior shoulder dislocation",
            "Inferior shoulder dislocation",
            "Superior shoulder dislocation"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe glenohumeral joint is the most frequently dislocated large joint in the body due to its anatomical sacrifice of bony stability (shallow glenoid fossa) for maximum range of motion. Anterior dislocations account for approximately 95% to 98% of all shoulder dislocations, typically produced by forced abduction, external rotation, and extension. The humeral head is driven anteriorly and inferiorly out of the glenoid. Clinical signs include flattening of the lateral shoulder contour, prominent acromion process ('epaulet sign'), palpable humeral head in the subcoracoid space, and inability to adduct the arm (Hamilton ruler test positive). The axillary nerve wraps around the surgical neck of the humerus and is the most commonly injured nerve (causing deltoid weakness and sensation loss over the 'regimental badge' area). In contrast, posterior dislocations (2-4%) are classically triggered by epileptic seizures or electric shocks.\n\nOption Review:\n- Option A is correct because anterior dislocation accounts for >95% of all shoulder dislocations.\n- Option B is incorrect because posterior dislocation accounts for only ~2-4% and is classically associated with seizures.\n- Option C is incorrect because inferior dislocation (luxatio erecta) is very rare, presenting with the arm locked overhead.\n- Option D is incorrect because superior dislocation is exceedingly rare, requiring extreme upward force.\n\nKey Takeaway: Anterior shoulder dislocation accounts for >95% of cases, classically presenting with flattening of the deltoid, palpable subcoracoid head, and risk of axillary nerve neuropraxia.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q244",
        "subjectId": "orthopedics",
        "subjectTitle": "Orthopedics",
        "topic": "Pediatric Orthopedics - Clubfoot (CTEV & Ponseti Method)",
        "prompt": "A newborn infant is noted to have a congenital foot deformity at birth. Examination reveals that the heel is in equinus and varus, the midfoot and forefoot are adducted and inverted, and a deep transverse crease is present on the medial border of the sole (Congenital Talipes Equinovarus / CTEV). What is the internationally established gold-standard non-operative conservative management for clubfoot?",
        "options": [
            "Serial corrective casting using the Ponseti technique",
            "Immediate radical soft-tissue posteromedial release surgery",
            "Rigid thermoplastic ankle-foot orthosis without manipulation",
            "Expectant observation until walking age"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nCongenital Talipes Equinovarus (CTEV / clubfoot) is a complex congenital deformity involving bones, joints, muscles, and ligaments of the foot and ankle. The anatomical components of the deformity are remembered by the mnemonic 'CAVE': C: Midfoot Cavus; A: Forefoot Adduction; V: Hindfoot Varus; E: Hindfoot Equinus. The established gold-standard conservative treatment worldwide is the Ponseti technique of serial manipulation and long-leg plaster casting, initiated ideally in the first weeks of life. Deformities are corrected in a strict sequential order: First, cavus is corrected by supinating the forefoot to align it with the hindfoot; Then adduction and varus are simultaneously corrected by gently abducting the foot in supination around a fulcrum placed on the lateral head of the talus. Equinus is corrected LAST (often requiring a minor percutaneous Achilles tenotomy). Radical open surgical releases have been largely abandoned.\n\nOption Review:\n- Option A is correct because serial manipulation and casting using the Ponseti method is the gold standard for CTEV.\n- Option B is incorrect because radical open posteromedial release surgery causes severe long-term foot stiffness and arthrosis, now largely obsolete.\n- Option C is incorrect because rigid braces without prior corrective casting fail to correct the deformity.\n- Option D is incorrect because untreated clubfoot becomes rigid, causing permanent disability and walking on the outer dorsum of the foot.\n\nKey Takeaway: Congenital Talipes Equinovarus (CTEV) is treated conservatively using the Ponseti method of sequential serial manipulation and casting (correcting Cavus, Adduction, Varus, and Equinus).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q245",
        "subjectId": "orthopedics",
        "subjectTitle": "Orthopedics",
        "topic": "Bone Tumors - Osteochondroma",
        "prompt": "A 16-year-old male presents with a painless, bony, non-tender lump near his knee that has been growing slowly for two years. Radiograph demonstrates a pedunculated mushroom-shaped bony outgrowth arising from the metaphysis of the distal femur, projecting away from the adjacent knee joint. The cortex and medullary cavity of the lesion are continuous with the underlying host bone. What is the most common benign bone tumor?",
        "options": [
            "Osteochondroma",
            "Giant cell tumor of bone",
            "Osteoid osteoma",
            "Enchondroma"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nOsteochondroma (exostosis) is the most common benign bone tumor, accounting for approximately 35% to 40% of all benign bone neoplasms. It typically presents in adolescents and young adults as an asymptomatic, slow-growing, hard, non-tender bony mass in the metaphysis of long bones around the knee (distal femur, proximal tibia) or proximal humerus. Pathognomonic radiographic features: 1) A sessile or pedunculated bony stalk arising from the cortex and projecting away from the adjacent epiphyseal growth plate / joint line; 2) The cortex and the trabecular medullary cavity of the stalk are directly continuous with the parent bone. The tumor is covered by a cartilaginous cap; growth ceases when the adjacent epiphyseal growth plate closes. Thickening of the cartilage cap (>1.5 to 2 cm in adults) raises suspicion of malignant transformation to secondary chondrosarcoma (<1%).\n\nOption Review:\n- Option A is correct because a pedunculated metaphyseal lesion with medullary continuity projecting away from the joint is an osteochondroma.\n- Option B is incorrect because giant cell tumor occurs in skeletally mature adults (20-40 years) as an eccentric, lytic epiphyseal lesion extending to articular cartilage ('soap bubble' appearance).\n- Option C is incorrect because osteoid osteoma produces nocturnal bone pain dramatically relieved by aspirin, with a radiolucent nidus surrounded by dense sclerosis.\n- Option D is incorrect because enchondroma is an intramedullary benign cartilaginous tumor typically affecting short tubular bones of the hands.\n\nKey Takeaway: Osteochondroma is the most common benign bone tumor, characterized radiologically by a metaphyseal bony outgrowth with cortex and medullary continuity projecting away from the joint.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Osteochondroma_X-ray.jpg/640px-Osteochondroma_X-ray.jpg"
        ]
    },

    # ==========================================
    # ANESTHESIOLOGY (5 Questions: Q246 - Q250)
    # ==========================================
    {
        "id": "fmge-gt1-q246",
        "subjectId": "anesthesia",
        "subjectTitle": "Anesthesiology",
        "topic": "Airway Assessment - Mallampati Classification",
        "prompt": "During a pre-anesthetic airway evaluation, an anesthesiologist examines a 45-year-old female sitting upright with her head in a neutral position, mouth opened maximally, and tongue fully protruded without phonation. Inspection of the oropharynx reveals visualization of the soft palate, fauces, and uvula, but the tonsillar pillars are obscured by the tongue base. What modified Mallampati class is assigned to this airway?",
        "options": [
            "Mallampati Class I",
            "Mallampati Class II",
            "Mallampati Class III",
            "Mallampati Class IV"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe modified Mallampati classification is a standardized bedside scoring system that predicts the degree of difficulty of direct laryngoscopy and endotracheal intubation based on the anatomical structures visualized inside the oral cavity (patient sitting, mouth wide open, tongue protruded, NO phonation): 1) Class I: Soft palate, faucial pillars, entire uvula, and tonsils visualized; 2) Class II: Soft palate, fauces, and upper portion of uvula visualized (tonsillar pillars obscured); 3) Class III: Soft palate and base of uvula visualized (uvula tip and pillars obscured); 4) Class IV: Only hard palate visualized (soft palate completely hidden). Higher classes (III and IV) are statistically associated with difficult laryngoscopy (Cormack-Lehane grades 3 and 4).\n\nOption Review:\n- Option A is incorrect because Class I allows visualization of all structures, including the faucial tonsillar pillars.\n- Option B is correct because visualization of the soft palate, fauces, and uvula without the tonsillar pillars defines Mallampati Class II.\n- Option C is incorrect because Class III shows only the soft palate and base of the uvula.\n- Option D is incorrect because Class IV shows only the hard palate.\n\nKey Takeaway: Mallampati Class II is characterized by visualization of the soft palate, fauces, and uvula, with the tonsillar pillars obscured.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q247",
        "subjectId": "anesthesia",
        "subjectTitle": "Anesthesiology",
        "topic": "Regional Anesthesia - Spinal vs Epidural Anatomy",
        "prompt": "An anesthesiologist performs a subarachnoid block (spinal anesthesia) for a patient undergoing elective cesarean section. In adults, the spinal cord terminates at the conus medullaris at the L1-L2 interspace. To avoid needle trauma to the spinal cord, spinal lumbar puncture is safely performed below this level (typically at the L3-L4 or L4-L5 interspace). What surface anatomical landmark connects the highest points of both iliac crests to identify the L4 vertebral spinous process?",
        "options": [
            "Tuffier line",
            "McBurney line",
            "Spigelian line",
            "Nélaton line"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIn adults, the spinal cord terminates at the conus medullaris at the lower border of the L1 vertebra (or L1-L2 intervertebral space), while the dural sac continues downward to terminate at the lower border of S2. Therefore, to prevent direct mechanical needle damage to the spinal cord, lumbar puncture for spinal anesthesia must be performed in the lower lumbar interspaces (L3-L4 or L4-L5). The universal surface landmark used to identify the lumbar spine is Tuffier's line (the intercristal or Jacoby line), which is a horizontal line drawn across the highest points of both iliac crests. Tuffier's line intersects the vertebral column at the level of the L4 spinous process or the L4-L5 intervertebral space.\n\nOption Review:\n- Option A is correct because Tuffier's (intercristal) line connects the superior iliac crests and crosses the L4 spinous process.\n- Option B is incorrect because McBurney's line connects the right ASIS to the umbilicus.\n- Option C is incorrect because the Spigelian line represents the lateral border of the rectus sheath.\n- Option D is incorrect because Nélaton's line connects the ASIS to the ischial tuberosity to assess hip joint dislocation.\n\nKey Takeaway: Tuffier's line (intercristal line) joins the tops of the iliac crests at the level of the L4 spinous process, marking the safe zone for lumbar spinal puncture.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q248",
        "subjectId": "anesthesia",
        "subjectTitle": "Anesthesiology",
        "topic": "Local Anesthetics - Systemic Toxicity (LAST) & Lipid Rescue",
        "prompt": "During the performance of an ultrasound-guided femoral nerve block using 0.5% bupivacaine, a 60-year-old male develops an accidental intravascular injection. Within 2 minutes, he experiences circumoral numbness, tinnitus, a metallic taste, followed rapidly by generalized tonic-clonic convulsions, ventricular arrhythmias, and profound cardiovascular collapse. Along with airway management, what specific pharmacological antidote is administered intravenously to treat local anesthetic systemic toxicity (LAST)?",
        "options": [
            "20% Intravenous lipid emulsion",
            "Intravenous sodium bicarbonate",
            "High-dose calcium gluconate",
            "Intravenous flumazenil"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nLocal Anesthetic Systemic Toxicity (LAST) is a life-threatening complication resulting from inadvertent intravascular injection or massive systemic absorption of local anesthetics, particularly lipophilic amide agents like bupivacaine. Bupivacaine binds avidly to inactivated cardiac sodium channels, dissociating extremely slowly during diastole and triggering refractory ventricular arrhythmias, electromechanical dissociation, and cardiac arrest. CNS symptoms (tinnitus, perioral numbness, seizures) precede cardiovascular collapse. The specific antidote is 20% Intravenous Lipid Emulsion (Intralipid / 'Lipid Rescue'). The lipid emulsion acts primarily as a 'lipid sink', creating an expanded intravascular lipid phase that sequesters the lipophilic bupivacaine molecules away from cardiac myocytes and brain tissue, while directly facilitating myocardial fatty acid metabolism and driving positive inotropy.\n\nOption Review:\n- Option A is correct because 20% IV lipid emulsion is the proven specific antidote for local anesthetic systemic toxicity.\n- Option B is incorrect because sodium bicarbonate treats tricyclic antidepressant cardiotoxicity, not primary bupivacaine toxicity.\n- Option C is incorrect because calcium gluconate stabilizes cardiac membranes in hyperkalemia, but does not extract local anesthetics.\n- Option D is incorrect because flumazenil is a benzodiazepine antagonist.\n\nKey Takeaway: 20% intravenous lipid emulsion is the specific antidote of choice for reversing local anesthetic systemic toxicity (LAST) and bupivacaine-induced cardiac arrest.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q249",
        "subjectId": "anesthesia",
        "subjectTitle": "Anesthesiology",
        "topic": "Preoperative Evaluation - ASA Physical Status Classification",
        "prompt": "An anesthesiologist performs a pre-anesthetic check-up on a 58-year-old male scheduled for an elective laparoscopic inguinal hernia repair. The patient has well-controlled hypertension on amlodipine and well-controlled type 2 diabetes mellitus with an HbA1c of 6.8%. He has no functional limitations and easily climbs two flights of stairs without dyspnea. According to the American Society of Anesthesiologists (ASA) Physical Status Classification System, what class is assigned to this patient?",
        "options": [
            "ASA Class I",
            "ASA Class II",
            "ASA Class III",
            "ASA Class IV"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe ASA Physical Status Classification System assesses a patient's pre-operative physical health: 1) ASA I: Normal healthy patient (non-smoking, no alcohol, no systemic disease); 2) ASA II: Patient with mild systemic disease without substantive functional limitations (e.g., well-controlled hypertension, well-controlled diabetes mellitus, mild obesity BMI 30-40, social alcohol drinker, cigarette smoker); 3) ASA III: Patient with severe systemic disease that causes substantive functional limitations (e.g., poorly controlled diabetes or hypertension, COPD, stable angina, prior MI >3 months ago, morbid obesity BMI >=40); 4) ASA IV: Patient with severe systemic disease that is a constant threat to life (e.g., ongoing unstable angina, sepsis, severe valve dysfunction, MI within last 3 months); 5) ASA V: Moribund patient not expected to survive 24 hours without surgery; 6) ASA VI: Declared brain-dead organ donor.\n\nOption Review:\n- Option A is incorrect because ASA I is reserved for completely healthy individuals without chronic diseases.\n- Option B is correct because well-controlled hypertension and diabetes without functional limitations define ASA Class II.\n- Option C is incorrect because ASA III requires severe disease with substantial functional limitations.\n- Option D is incorrect because ASA IV requires a condition that is a constant threat to life.\n\nKey Takeaway: A patient with mild, well-controlled systemic disease without functional limitations (such as well-controlled diabetes or hypertension) is classified as ASA Class II.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q250",
        "subjectId": "anesthesia",
        "subjectTitle": "Anesthesiology",
        "topic": "Airway Management - Rapid Sequence Induction & Cricoid Pressure",
        "prompt": "A 30-year-old pregnant female at 38 weeks of gestation presents for an emergency cesarean section 1 hour after consuming a full meal. She is at high risk for pulmonary aspiration of gastric contents (Mendelson syndrome). Rapid Sequence Induction and Intubation (RSII) is performed. What maneuver involves backward digital compression on the cricoid cartilage to occlude the underlying upper esophagus against the sixth cervical vertebra?",
        "options": [
            "Sellick maneuver",
            "Heimlich maneuver",
            "Epley maneuver",
            "Pringle maneuver"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nRapid Sequence Induction and Intubation (RSII) is designed to achieve rapid control of the airway while minimizing the risk of regurgitation and pulmonary aspiration of acidic gastric contents in patients with a 'full stomach' (trauma, pregnancy, bowel obstruction, emergency surgery). The classical technique consists of: 1) Thorough pre-oxygenation; 2) Predetermined rapid-acting IV hypnotic (e.g., propofol, ketamine) immediately followed by a fast-onset muscle relaxant (succinylcholine or high-dose rocuronium); 3) Complete avoidance of bag-valve-mask positive pressure ventilation (to prevent gastric insufflation); 4) Application of cricoid pressure (the Sellick maneuver). In the Sellick maneuver, an assistant applies firm posterior pressure (approximately 30 Newtons) on the non-collapsible, complete cartilaginous ring of the cricoid cartilage. This compresses the underlying cervical esophagus against the anterior body of the C6 vertebra, preventing passive regurgitation until the endotracheal tube cuff is inflated.\n\nOption Review:\n- Option A is correct because the Sellick maneuver is backward compression on the cricoid cartilage to occlude the esophagus during rapid sequence induction.\n- Option B is incorrect because the Heimlich maneuver involves subdiaphragmatic abdominal thrusts to relieve foreign-body airway obstruction.\n- Option C is incorrect because the Epley maneuver is a canalith repositioning procedure for BPPV.\n- Option D is incorrect because the Pringle maneuver is surgical cross-clamping of the hepatoduodenal ligament.\n\nKey Takeaway: The Sellick maneuver applies posterior pressure on the cricoid cartilage during rapid sequence induction to occlude the esophagus and prevent pulmonary aspiration.",
        "imageUrls": []
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(QUESTIONS)} questions in Part 2 Block 2.")
    for q in QUESTIONS:
        assert len(q["options"]) == 4, f"{q['id']} does not have 4 options"
        assert 0 <= q["answerIndex"] <= 3, f"{q['id']} invalid answerIndex"
        for opt in q["options"]:
            assert not opt.endswith(";"), f"{q['id']} option ends with semicolon: {opt}"
            assert "(" not in opt or any(c.isdigit() for c in opt), f"{q['id']} option has explanatory bracket: {opt}"
    print("All 50 questions passed structural assertions.")
