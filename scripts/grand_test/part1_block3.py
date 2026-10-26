# -*- coding: utf-8 -*-
"""
FMGE Grand Test 1 - Part 1: Block 3
Community Medicine (30 Qs) + Ophthalmology (10 Qs) + ENT (10 Qs) = 50 Questions (Q101 - Q150)
Strict adherence to 2026 NBE pattern, clinical vignettes, option-by-option review.
Zero textbook citations.
"""

QUESTIONS = [
    # ==========================================
    # COMMUNITY MEDICINE / PSM (30 Questions: Q101 - Q130)
    # ==========================================
    {
        "id": "fmge-gt1-q101",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Epidemiology - Sensitivity & Specificity",
        "prompt": "An epidemiological team evaluates a new rapid antigen screening test for dengue fever among 1,000 febrile patients in an endemic district. The gold standard RT-PCR confirms dengue in 200 individuals. The rapid antigen test is positive in 180 of these confirmed cases and negative in 720 of the 800 non-dengue individuals. What is the sensitivity of this rapid test?",
        "options": [
            "75%",
            "80%",
            "90%",
            "95%"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nSensitivity is defined as the proportion of truly diseased individuals who are correctly identified as positive by the screening test (True Positive Rate). The formula is: Sensitivity = [True Positives (TP) / (True Positives (TP) + False Negatives (FN))] x 100. In this cohort: Total confirmed cases = 200. True Positives (test positive among diseased) = 180. False Negatives (diseased patients missed by test) = 200 - 180 = 20. Therefore, Sensitivity = (180 / 200) x 100 = 90%.\n\nOption Review:\n- Option A is incorrect because 75% underestimates the true positive detection rate.\n- Option B is incorrect because 80% represents an inaccurate calculation.\n- Option C is correct because Sensitivity = 180 / 200 = 90%.\n- Option D is incorrect because 95% is higher than the calculated true positive fraction.\n\nKey Takeaway: Sensitivity measures the ability of a test to correctly identify individuals who truly have the disease: TP / (TP + FN).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q102",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Epidemiology - Positive Predictive Value & Prevalence",
        "prompt": "A community health officer conducts screening for gestational diabetes mellitus using a standardized test with 90% sensitivity and 90% specificity. If the test is deployed in a high-prevalence population compared to a low-prevalence population, which statistical diagnostic parameter will increase?",
        "options": [
            "Sensitivity",
            "Specificity",
            "Positive predictive value",
            "Negative predictive value"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nSensitivity and specificity are intrinsic operating characteristics of a diagnostic test that remain relatively constant regardless of disease prevalence. In contrast, predictive values are heavily dependent on disease prevalence: As the prevalence of a disease increases in a population, the Positive Predictive Value (PPV) increases (because more positive tests reflect true disease rather than false positives), while the Negative Predictive Value (NPV) decreases.\n\nOption Review:\n- Option A is incorrect because sensitivity is an intrinsic test characteristic unaffected by disease prevalence.\n- Option B is incorrect because specificity is an intrinsic property of the test independent of prevalence.\n- Option C is correct because positive predictive value (PPV) directly increases with higher disease prevalence.\n- Option D is incorrect because negative predictive value (NPV) decreases as disease prevalence rises.\n\nKey Takeaway: While sensitivity and specificity are intrinsic test properties, positive predictive value (PPV) rises as disease prevalence increases.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q103",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Biomedical Waste Management - Bag Color Coding",
        "prompt": "During a major surgical procedure in the operating room, an uninfected amputated lower extremity and anatomical tissue fragments are excised. Under the current Biomedical Waste Management Rules, into which color-coded container or bag must these human anatomical waste specimens be segregated?",
        "options": [
            "Yellow bag",
            "Red bag",
            "Blue cardboard box",
            "White translucent puncture-proof container"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nUnder the Biomedical Waste Management (Amendment) Rules: 1) Yellow bags: For incinerable waste, including human and animal anatomical waste, soiled waste (cotton, bandages, linen contaminated with body fluids), discarded/expired cytotoxic drugs, and microbiological cultures; 2) Red bags: For recyclable contaminated plastics (IV tubing, catheters, urine bags, disposable syringes without needles); 3) Blue boxes: For contaminated glassware (medicine vials, ampoules) and metallic body implants; 4) White translucent puncture-proof containers: For sharps (needles, scalpels, blades, fixed-needle syringes).\n\nOption Review:\n- Option A is correct because human anatomical waste is segregated into non-chlorinated yellow plastic bags for incineration or deep burial.\n- Option B is incorrect because red bags are strictly reserved for recyclable contaminated plastics.\n- Option C is incorrect because blue containers are used for glassware and metallic implants.\n- Option D is incorrect because white puncture-proof containers are reserved for sharps.\n\nKey Takeaway: Human anatomical waste is segregated into yellow bags for high-temperature incineration or plasma pyrolysis under BMW rules.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q104",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Immunization - National Immunization Schedule at Birth",
        "prompt": "A healthy term male infant is delivered by normal vaginal delivery in a primary health center. Under the National Immunization Schedule (NIS) in India, which three vaccines should be routinely administered to this newborn before discharge within the first 24 hours of life?",
        "options": [
            "BCG, OPV zero dose, and Hepatitis B birth dose",
            "BCG, DPT first dose, and Hepatitis B birth dose",
            "Pentavalent first dose, OPV first dose, and Rotavirus",
            "BCG, Inactivated Polio Vaccine, and Vitamin A"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nUnder the Universal Immunization Programme (UIP) / National Immunization Schedule (NIS) in India, three vaccines are scheduled at birth (as early as possible within 24 hours): 1) BCG (Bacille Calmette-Guérin): 0.05 mL intradermally on the left upper arm to protect against severe disseminated childhood tuberculosis (tubercular meningitis and miliary TB); 2) Oral Polio Vaccine (OPV zero dose): 2 drops orally; 3) Hepatitis B birth dose: 0.5 mL intramuscularly on the anterolateral aspect of the mid-thigh to prevent vertical mother-to-child transmission.\n\nOption Review:\n- Option A is correct because BCG, OPV zero dose, and Hepatitis B birth dose form the standard at-birth vaccine triad.\n- Option B is incorrect because DPT is not given at birth (administered as Pentavalent starting at 6 weeks).\n- Option C is incorrect because Pentavalent, OPV-1, and Rotavirus are administered at 6 weeks of age.\n- Option D is incorrect because IPV is administered at 6 and 14 weeks (fractional intradermal), and Vitamin A starts at 9 months.\n\nKey Takeaway: At birth, newborns receive BCG (intradermal), OPV zero dose (oral), and Hepatitis B birth dose (intramuscular) within 24 hours.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q105",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Levels of Prevention - Primordial vs Primary",
        "prompt": "A state public health department passes a statewide ban on the sale of sugary sodas and energy drinks in all school cafeterias, accompanied by mandatory physical exercise curricula to prevent the emergence of childhood obesity risk factors. Which level of prevention is exemplified by eliminating the emergence of risk factors in a population?",
        "options": [
            "Primordial prevention",
            "Primary prevention",
            "Secondary prevention",
            "Tertiary prevention"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe levels of prevention are classified according to the natural history of disease: 1) Primordial prevention: Prevention of the emergence or development of risk factors in a population where they have not yet appeared (e.g., national nutrition policies, banning junk foods in schools, anti-smoking education directed at children to discourage tobacco initiation); 2) Primary prevention: Action taken prior to the onset of disease that removes the possibility that a disease will ever occur in individuals who already have risk factors (e.g., immunization, condoms, smoking cessation); 3) Secondary prevention: Early disease detection (screening, Pap smears) and prompt intervention to halt progression; 4) Tertiary prevention: Measures to reduce disability and facilitate rehabilitation (e.g., physiotherapy after stroke).\n\nOption Review:\n- Option A is correct because preventing the emergence of risk factors through lifestyle and policy interventions constitutes primordial prevention.\n- Option B is incorrect because primary prevention intervenes on established risk factors or provides specific protection.\n- Option C is incorrect because secondary prevention involves early diagnosis and treatment.\n- Option D is incorrect because tertiary prevention focuses on disability limitation and rehabilitation.\n\nKey Takeaway: Primordial prevention aims to prevent the initial development and emergence of environmental, economic, and behavioral risk factors in entire populations.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q106",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Demography - Infant Mortality Rate",
        "prompt": "In a district with a mid-year population of 500,000, official vital registration records 12,000 live births in a calendar year. During the same year, 480 infants die before celebrating their first birthday. What is the Infant Mortality Rate (IMR) per 1,000 live births in this district?",
        "options": [
            "24 per 1,000 live births",
            "40 per 1,000 live births",
            "48 per 1,000 live births",
            "96 per 1,000 live births"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe Infant Mortality Rate (IMR) is universally defined as the number of deaths of infants under one year of age during a given calendar year, per 1,000 live births in that same year. Formula: IMR = [Number of infant deaths under 1 year in a year / Total number of live births in that same year] x 1,000. Calculation: IMR = (480 / 12,000) x 1,000 = 40 per 1,000 live births. Crucially, the denominator is total live births, NOT the total mid-year population.\n\nOption Review:\n- Option A is incorrect because 24 per 1,000 represents a mathematical error.\n- Option B is correct because (480 / 12,000) x 1,000 = 40 per 1,000 live births.\n- Option C is incorrect because 48 would occur if calculated with an incorrect multiplier or denominator.\n- Option D is incorrect because 96 is double the true rate.\n\nKey Takeaway: Infant Mortality Rate is calculated as deaths under 1 year of age per 1,000 live births in the same year.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q107",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Demography - Maternal Mortality Ratio",
        "prompt": "In a state monitoring maternal health indicators, 200 maternal deaths related to pregnancy and childbirth are recorded during a year in which 100,000 live births occur. What is the Maternal Mortality Ratio (MMR) for this state?",
        "options": [
            "20 per 100,000 live births",
            "100 per 100,000 live births",
            "200 per 100,000 live births",
            "400 per 100,000 live births"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nMaternal Mortality Ratio (MMR) is expressed as the number of maternal deaths during pregnancy, delivery, or within 42 days of termination of pregnancy from pregnancy-related causes, per 100,000 live births. Formula: MMR = [Total maternal deaths in a year / Total live births in that same year] x 100,000. Note the multiplier is 100,000 (unlike IMR, which uses 1,000). Calculation: MMR = (200 / 100,000) x 100,000 = 200 per 100,000 live births. (In contrast, Maternal Mortality Rate uses the mid-year population of women of reproductive age 15-49 as denominator).\n\nOption Review:\n- Option A is incorrect because 20 is one-tenth of the actual ratio.\n- Option B is incorrect because 100 is half of the actual ratio.\n- Option C is correct because (200 / 100,000) x 100,000 = 200 per 100,000 live births.\n- Option D is incorrect because 400 overestimates the ratio.\n\nKey Takeaway: Maternal Mortality Ratio (MMR) is calculated per 100,000 live births, serving as a primary indicator of reproductive health care quality.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q108",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Epidemiology - Study Designs (Odds Ratio vs Relative Risk)",
        "prompt": "An epidemiological investigator undertakes a study to determine if occupational benzene exposure is associated with acute myeloid leukemia (AML). Because AML is a rare malignancy, the investigator identifies 100 patients with confirmed AML and 200 age- and sex-matched hospital controls without AML, then determines their prior history of benzene exposure. Which measure of association is calculated from this case-control study design?",
        "options": [
            "Relative risk",
            "Odds ratio",
            "Attributable risk",
            "Incidence rate ratio"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nA case-control study begins with the outcome (cases who have the disease vs controls who do not) and looks backward in time to determine antecedent exposure. Because the investigator selects the fixed number of cases and controls, the true incidence of disease in the population cannot be measured. Therefore, Relative Risk (RR) cannot be directly calculated. The key measure of association in a case-control study is the Odds Ratio (OR = ad/bc, the odds of exposure among cases divided by the odds of exposure among controls). When the disease is rare, the odds ratio closely approximates the relative risk.\n\nOption Review:\n- Option A is incorrect because relative risk requires direct calculation of incidence rates, which can only be obtained in cohort studies.\n- Option B is correct because the odds ratio is the primary measure of association in case-control studies.\n- Option C is incorrect because attributable risk requires background incidence figures from cohort studies.\n- Option D is incorrect because incidence rate ratios are derived from prospective longitudinal cohorts.\n\nKey Takeaway: Case-control studies measure association using the Odds Ratio (OR), whereas cohort studies measure Relative Risk (RR).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q109",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Epidemiology - Relative Risk Calculation",
        "prompt": "In a 10-year prospective cohort study of 2,000 middle-aged men, 1,000 are heavy smokers and 1,000 are non-smokers. During the follow-up period, 100 smokers and 10 non-smokers develop coronary artery disease. What is the Relative Risk (RR) of developing coronary artery disease among smokers compared to non-smokers?",
        "options": [
            "5",
            "10",
            "20",
            "50"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nIn a prospective cohort study, subjects are classified by exposure status and followed forward in time to observe disease incidence. Formula: Relative Risk (Risk Ratio, RR) = [Incidence of disease among exposed (Ie)] / [Incidence of disease among unexposed (Io)]. Incidence in exposed smokers (Ie) = 100 / 1,000 = 0.10 (10%). Incidence in unexposed non-smokers (Io) = 10 / 1,000 = 0.01 (1%). Therefore, Relative Risk = 0.10 / 0.01 = 10. This indicates that heavy smokers have 10 times the risk of developing coronary disease compared to non-smokers.\n\nOption Review:\n- Option A is incorrect because 5 is half the true relative risk.\n- Option B is correct because (100/1000) / (10/1000) = 0.10 / 0.01 = 10.\n- Option C is incorrect because 20 is double the true risk.\n- Option D is incorrect because 50 is an overestimation.\n\nKey Takeaway: Relative risk is the ratio of incidence in the exposed group to incidence in the unexposed group: Ie / Io.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q110",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Biostatistics - Measures of Central Tendency in Skewed Data",
        "prompt": "A clinical trial measures the hospital length of stay in days for 150 patients admitted with acute pancreatitis. Because a small subset of patients developed severe complications requiring prolonged intensive care stays of several months, the resulting data distribution is heavily positively (right) skewed. Which measure of central tendency is least affected by these extreme outliers and best represents the typical hospital stay?",
        "options": [
            "Arithmetic mean",
            "Median",
            "Mode",
            "Geometric mean"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nIn a symmetrical, bell-shaped normal distribution, the Mean, Median, and Mode are identical. However, when data are skewed (asymmetrical with extreme outliers), the arithmetic mean is pulled heavily toward the elongated tail (in a positively skewed distribution, Mean > Median > Mode). The Median (the 50th percentile value separating the higher half from the lower half of data) is based on rank order rather than numerical values, making it resistant (robust) to extreme outliers. Therefore, the Median is the preferred measure of central tendency for skewed distributions.\n\nOption Review:\n- Option A is incorrect because the arithmetic mean is highly sensitive to extreme outliers and will be falsely elevated in right-skewed data.\n- Option B is correct because the median is unaffected by outliers and best represents central tendency in skewed data.\n- Option C is incorrect because the mode merely reflects the most frequent single value, which may not represent the overall distribution.\n- Option D is incorrect because the geometric mean is used for logarithmic/exponential data like bacterial titers, but is less intuitive than the median for skewed clinical stays.\n\nKey Takeaway: For skewed numerical data with extreme outliers, the median is the preferred measure of central tendency because it is non-parametric and resistant to distortion.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q111",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Biostatistics - Normal Distribution Properties",
        "prompt": "The birth weights of 10,000 full-term singleton neonates born in a tertiary care hospital follow a normal (Gaussian) distribution with a mean of 3,000 grams and a standard deviation (SD) of 400 grams. According to the empirical rule of normal distributions, approximately what percentage of neonates will have birth weights falling between 2,200 grams and 3,800 grams?",
        "options": [
            "68%",
            "95%",
            "99.7%",
            "50%"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nIn a Gaussian (normal) distribution curve: 1) Mean ± 1 SD encompasses approximately 68.2% of the population; 2) Mean ± 2 SD encompasses approximately 95.4% of the population; 3) Mean ± 3 SD encompasses approximately 99.7% of the population. In this scenario: Mean = 3,000 g, SD = 400 g. The range from 2,200 g to 3,800 g corresponds to: [3,000 - 2(400)] to [3,000 + 2(400)] = Mean ± 2 SD. Therefore, approximately 95% of the infants have birth weights in this interval.\n\nOption Review:\n- Option A is incorrect because 68% corresponds to Mean ± 1 SD (2,600 g to 3,400 g).\n- Option B is correct because Mean ± 2 SD encompasses approximately 95% of all values in a normal distribution.\n- Option C is incorrect because 99.7% corresponds to Mean ± 3 SD (1,800 g to 4,200 g).\n- Option D is incorrect because 50% represents the area on one side of the mean.\n\nKey Takeaway: In a normal distribution, Mean ± 1 SD encompasses 68%, Mean ± 2 SD encompasses 95%, and Mean ± 3 SD encompasses 99.7% of the observations.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q112",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Water Purification - Chlorine Demand & Breakpoint Chlorination",
        "prompt": "During public water supply treatment, chlorine is added to filtered water to destroy pathogenic microorganisms. Chlorine first oxidizes organic impurities and iron, then reacts with ammonia to form chloramines, after which residual free chlorine begins to appear in direct proportion to added chlorine. What is the point on the chlorination curve at which all ammonia is oxidized and residual free chlorine starts to accumulate called?",
        "options": [
            "Contact point",
            "Breakpoint chlorination",
            "Saturation threshold",
            "Residual plateau"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nBreakpoint chlorination is a critical concept in water disinfection. When chlorine is progressively added to raw water, the chlorine curve displays four phases: 1) Immediate destruction of readily oxidizable compounds; 2) Reaction with ammonia and nitrogenous compounds to form chloramines (combined available chlorine); 3) Oxidation and destruction of these chloramines, during which total residual chlorine paradoxically drops despite adding more chlorine; 4) The 'breakpoint'—the nadir where all chloramines and ammonia are completely destroyed. Any chlorine added beyond the breakpoint appears as free residual chlorine (hypochlorous acid and hypochlorite ion), which provides active, rapid bactericidal action and protects against post-treatment contamination.\n\nOption Review:\n- Option A is incorrect because contact point is an arbitrary term, whereas contact time is the 1-hour duration needed for action.\n- Option B is correct because breakpoint chlorination is the point beyond which added chlorine appears as free available residual chlorine.\n- Option C is incorrect because saturation threshold is not the recognized chemical engineering term for water disinfection.\n- Option D is incorrect because residual plateau is not the designated term.\n\nKey Takeaway: Breakpoint chlorination represents the stage where all organic and ammonia compounds are oxidized, and added chlorine produces free residual chlorine.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q113",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Nutrition - Mid-Upper Arm Circumference (MUAC)",
        "prompt": "During community nutritional screening in an anganwadi center, a health worker measures the mid-upper arm circumference (MUAC) of a 3-year-old child using a Shakir tape. The measurement reads 11.2 cm, and bilateral pitting pedal edema is absent. According to World Health Organization criteria, which nutritional status is indicated by a MUAC of less than 11.5 cm in children aged 6 to 59 months?",
        "options": [
            "Normal nutritional status",
            "Moderate acute malnutrition",
            "Severe acute malnutrition",
            "Mild chronic stunting"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nMid-Upper Arm Circumference (MUAC) is a rapid, age-independent screening tool for acute malnutrition in children aged 6 to 59 months because muscle and fat mass in the arm remain relatively constant during this age span. The WHO cutoff values using standard color-coded Shakir tape are: 1) MUAC > 12.5 cm (Green): Normal nutritional status; 2) MUAC 11.5 to 12.5 cm (Yellow): Moderate Acute Malnutrition (MAM); 3) MUAC < 11.5 cm (Red): Severe Acute Malnutrition (SAM). The presence of bilateral nutritional pitting edema independently defines SAM regardless of MUAC measurement.\n\nOption Review:\n- Option A is incorrect because normal MUAC is > 12.5 cm.\n- Option B is incorrect because moderate acute malnutrition is defined by MUAC between 11.5 cm and 12.4 cm.\n- Option C is correct because MUAC < 11.5 cm is the diagnostic criterion for Severe Acute Malnutrition (SAM).\n- Option D is incorrect because stunting is defined by height-for-age z-score, not MUAC.\n\nKey Takeaway: A mid-upper arm circumference (MUAC) < 11.5 cm in children aged 6 to 59 months diagnoses Severe Acute Malnutrition (SAM).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q114",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Vaccinology - Cold Chain Equipment",
        "prompt": "A medical officer inspects the cold chain equipment at a Community Health Center (CHC). Oral Poliovirus Vaccine (OPV) and measles/MR vaccines must be stored at sub-zero temperatures (-15°C to -25°C), while sensitive liquid vaccines like DPT, TT, and Hepatitis B must be stored strictly at +2°C to +8°C and never allowed to freeze. Which cold chain equipment is kept at the district headquarters and PHC to store vaccines at +2°C to +8°C?",
        "options": [
            "Deep freezer",
            "Ice-lined refrigerator",
            "Cold box",
            "Vaccine carrier"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe cold chain is a system of transporting and storing vaccines at recommended temperatures from the manufacturer to the point of administration. The two primary electrical refrigeration units in the UIP are: 1) Ice-Lined Refrigerator (ILR): Top-opening refrigerator whose inner walls are lined with ice packs/water tubes. It maintains an internal temperature strictly between +2°C and +8°C, and can keep this temperature for up to 24 to 72 hours during power outages. It is used to store all routine vaccines at the PHC/CHC level (T-series, Pentavalent, Rotavirus, BCG, PCV); 2) Deep Freezer: Operates at -15°C to -25°C, used mainly to freeze ice packs and store OPV/measles at district levels.\n\nOption Review:\n- Option A is incorrect because deep freezers maintain -15°C to -25°C to freeze ice packs, and will destroy freezing-sensitive vaccines.\n- Option B is correct because the ice-lined refrigerator (ILR) reliably maintains temperatures between +2°C and +8°C.\n- Option C is incorrect because cold boxes are large portable, non-electrical insulated containers used for transit during breakdowns.\n- Option D is incorrect because vaccine carriers are small portable containers carried by ASHAs/ANMs for session-day outreach.\n\nKey Takeaway: Ice-lined refrigerators (ILRs) are top-opening units that maintain +2°C to +8°C for routine vaccine storage at PHC and CHC levels.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q115",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "National Health Programs - NTEP Tuberculosis Regimen",
        "prompt": "A 36-year-old male with new sputum smear-positive pulmonary tuberculosis without rifampicin resistance is initiated on first-line anti-tubercular therapy under the National Tuberculosis Elimination Program (NTEP). Daily fixed-dose combinations (FDCs) are prescribed based on weight bands. What is the standard duration and drug composition of the continuation phase for drug-sensitive tuberculosis?",
        "options": [
            "2 months of Isoniazid, Rifampicin, Pyrazinamide, and Ethambutol",
            "4 months of Isoniazid, Rifampicin, and Ethambutol",
            "6 months of Isoniazid and Rifampicin only",
            "4 months of Isoniazid and Pyrazinamide"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nUnder the National Tuberculosis Elimination Program (NTEP) in India, the standard daily regimen for new drug-sensitive pulmonary tuberculosis consists of two phases: 1) Intensive Phase (IP): 2 months duration with four drugs: Isoniazid (H), Rifampicin (R), Pyrazinamide (Z), and Ethambutol (E) [2 HRZE], administered as daily fixed-dose combinations (4-FDC); 2) Continuation Phase (CP): 4 months duration with three drugs: Isoniazid, Rifampicin, and Ethambutol [4 HRE], administered as daily 3-FDC. Pyrazinamide is omitted during the continuation phase.\n\nOption Review:\n- Option A is incorrect because 2 HRZE is the Intensive Phase, not the Continuation Phase.\n- Option B is correct because the standard Continuation Phase under NTEP is 4 months of HRE (Isoniazid, Rifampicin, Ethambutol).\n- Option C is incorrect because under modern daily NTEP guidelines, Ethambutol is included in the CP (making it 4 HRE, not 2-drug HR).\n- Option D is incorrect because Pyrazinamide is not given in the continuation phase.\n\nKey Takeaway: The standard continuation phase for drug-sensitive tuberculosis under NTEP consists of 4 months of daily Isoniazid, Rifampicin, and Ethambutol (4 HRE).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q116",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Occupational Health - Pneumoconiosis (Silicosis)",
        "prompt": "A 48-year-old stonemason presents with progressive exertional breathlessness and dry cough. Chest radiography reveals multiple small, rounded opacities predominantly in the upper lobes, along with thin, peripheral calcification of the hilar and mediastinal lymph nodes producing an 'eggshell calcification' appearance. Which occupational dust exposure causes these characteristic radiological findings?",
        "options": [
            "Asbestos fibers",
            "Free crystalline silica",
            "Coal dust",
            "Beryllium particles"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nSilicosis is a fibrotic pneumoconiosis caused by chronic inhalation of respirable crystalline silicon dioxide (quartz, silica) dust in quarry workers, stonecutters, sandblasters, and miners. Alveolar macrophages phagocytose silica crystals, which destabilize lysosomal membranes, triggering the release of inflammatory cytokines (IL-1, TNF-alpha) and extensive collagen deposition. Chest X-ray reveals multiple small, nodular opacities predominantly in the upper lung zones. Peripheral curvilinear calcification of the rim of hilar lymph nodes produces the pathognomonic 'eggshell calcification'. Silicosis markedly impairs macrophage function, conferring a 30-fold increased risk of developing active tuberculosis (silicotuberculosis).\n\nOption Review:\n- Option A is incorrect because asbestosis causes lower lobe interstitial fibrosis, pleural plaques, and ferruginous bodies, without eggshell calcification.\n- Option B is correct because chronic crystalline silica exposure characteristically produces upper zone nodules and eggshell calcification of hilar lymph nodes.\n- Option C is incorrect because coal workers' pneumoconiosis causes coal macules and progressive massive fibrosis without eggshell calcification.\n- Option D is incorrect because berylliosis causes non-caseating granulomas resembling sarcoidosis.\n\nKey Takeaway: Silicosis is caused by crystalline silica dust, manifesting as upper-lobe nodular opacities and characteristic 'eggshell calcification' of hilar lymph nodes.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q117",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Epidemiology - Epidemic Curves",
        "prompt": "Following a community wedding feast, 65 guests develop acute vomiting, abdominal cramps, and diarrhea within 18 to 36 hours. An epidemic curve plotted by the district surveillance officer reveals a steep upward slope, a sharp single peak, and a gradual downward slope, with all cases clustering tightly within the incubation period of Salmonella enteritidis. What type of epidemic curve is illustrated?",
        "options": [
            "Point-source common vehicle epidemic",
            "Continuous common source epidemic",
            "Propagated person-to-person epidemic",
            "Cyclical cyclical epidemic"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nA point-source (single-exposure) common vehicle epidemic occurs when a susceptible population is exposed to an infectious agent or toxic substance simultaneously or over a very brief period from a single source (e.g., contaminated food at a banquet). Key features of a point-source epidemic curve: 1) Rapid, steep upward rise as cases develop within the minimum incubation period; 2) A sharp, well-defined single peak; 3) A gradual tailing off; 4) All cases cluster within the span of one single incubation period of the disease. There is no secondary wave because person-to-person transmission does not occur.\n\nOption Review:\n- Option A is correct because a sharp single peak with all cases falling within one incubation period following a single shared exposure defines a point-source epidemic.\n- Option B is incorrect because continuous common source epidemics exhibit a prolonged plateau without a sharp peak (e.g., contaminated municipal well).\n- Option C is incorrect because propagated epidemics (e.g., measles, cholera) show successive, progressively taller waves spaced one incubation period apart.\n- Option D is incorrect because cyclical epidemics reflect multi-year variations influenced by herd immunity.\n\nKey Takeaway: A point-source epidemic curve features a rapid onset, a sharp single peak, and all cases occurring within a single incubation period without secondary transmission.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q118",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Vectors & Control - Mosquito Genera Identification",
        "prompt": "A medical entomologist collects adult mosquitoes resting on the walls of cattle sheds during a malaria vector survey. The adult mosquitoes rest at an angle of 45 degrees to the surface, their proboscis and abdomen form a straight line, their wings feature dark spotted markings, and the females have palpi that are equal in length to the proboscis. Which mosquito genus is identified?",
        "options": [
            "Anopheles",
            "Culex",
            "Aedes",
            "Mansonia"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nMosquito genera are differentiated by distinct morphological and resting characteristics: 1) Anopheles (malaria vector): Rests at an inclined angle (45 degrees) to the surface; proboscis and body lie in a continuous straight line; spotted wings; female palpi are long and equal in length to the proboscis; larvae rest parallel to the water surface because they lack a breathing siphon; 2) Culex (filariasis, Japanese encephalitis): Rests parallel or 'humpbacked' to the surface; unspotted wings; female palpi are very short; larvae hang at an angle from the water surface with a long breathing siphon; 3) Aedes (dengue, chikungunya, Zika): Day-biting mosquito with distinctive white lyre-shaped markings on the thorax and white stripes on legs ('tiger mosquito').\n\nOption Review:\n- Option A is correct because resting at a 45-degree angle, straight proboscis-abdomen alignment, spotted wings, and long female palpi characterize Anopheles.\n- Option B is incorrect because Culex rests parallel/hunchbacked and has plain wings and short female palpi.\n- Option C is incorrect because Aedes has black and white striped body and legs and breeds in clean artificial containers.\n- Option D is incorrect because Mansonia breeds in association with aquatic plants (Pistia).\n\nKey Takeaway: Anopheles mosquitoes rest at a 45-degree angle with a straight body-proboscis axis, spotted wings, and long female palpi.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q119",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Nutrition - Iodine Deficiency Disorders",
        "prompt": "In an endemic sub-Himalayan belt, the district health team surveys school-age children (6 to 12 years) for Iodine Deficiency Disorders (IDD). Under national guidelines, what is the primary biochemical laboratory indicator used to assess current population iodine nutrition status?",
        "options": [
            "Median urinary iodine concentration",
            "Serum thyroid-stimulating hormone",
            "Serum free thyroxine",
            "Serum thyroglobulin"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIodine absorbed from the diet is rapidly cleared by the thyroid gland and the kidneys, with >90% of ingested iodine excreted in urine within 24 to 48 hours. Therefore, Median Urinary Iodine Concentration (UIC) measured in spot urine samples among school-age children (6-12 years) is the internationally recommended primary epidemiological indicator of current population iodine nutrition. Normal optimal iodine intake is defined by a median UIC of 100 to 199 microg/L. While total goiter rate reflects long-term chronic historical deficiency, UIC reflects immediate dietary intake.\n\nOption Review:\n- Option A is correct because median urinary iodine concentration (UIC) in spot urine samples is the gold-standard indicator for population iodine status.\n- Option B is incorrect because neonatal TSH screening is used to detect congenital hypothyroidism, not routine community iodine status.\n- Option C is incorrect because serum free T4 is homeostatically preserved until severe end-stage deficiency occurs.\n- Option D is incorrect because serum thyroglobulin reflects thyroid enlargement over months, but is secondary to UIC.\n\nKey Takeaway: Median urinary iodine concentration (UIC) of 100 to 199 microg/L in school-age children is the primary indicator of adequate population iodine nutrition.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q120",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Social Sciences - Health Care Delivery System (Population Norms)",
        "prompt": "According to the established Indian Public Health Standards (IPHS) for rural health infrastructure, what is the population norm for establishing a Primary Health Centre (PHC) in plain areas versus hilly, tribal, or difficult terrain?",
        "options": [
            "30,000 in plains and 20,000 in hilly/tribal areas",
            "50,000 in plains and 30,000 in hilly/tribal areas",
            "20,000 in plains and 10,000 in hilly/tribal areas",
            "120,000 in plains and 80,000 in hilly/tribal areas"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nUnder the 3-tier rural healthcare infrastructure in India, the population coverage norms are strictly defined: 1) Sub-Centre (Health and Wellness Centre): 5,000 in plain areas; 3,000 in hilly/tribal/difficult areas; 2) Primary Health Centre (PHC): 30,000 in plain areas; 20,000 in hilly/tribal/difficult areas (acts as a referral center for 6 Sub-Centres, staffed by a Medical Officer); 3) Community Health Centre (CHC): 120,000 in plain areas; 80,000 in hilly/tribal/difficult areas (acts as a 30-bedded First Referral Unit with 4 specialists: surgeon, physician, obstetrician/gynecologist, and pediatrician).\n\nOption Review:\n- Option A is correct because the population norm for a PHC is 30,000 in plains and 20,000 in hilly/tribal areas.\n- Option B is incorrect because these are non-standard intermediate figures.\n- Option C is incorrect because 20,000/10,000 are not standard administrative tiers.\n- Option D is incorrect because 120,000 in plains and 80,000 in hilly/tribal areas represents the norm for a Community Health Centre (CHC).\n\nKey Takeaway: The population norm for a Primary Health Centre (PHC) in India is 30,000 in plain areas and 20,000 in hilly/tribal/desert areas.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q121",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Disinfection - Horrocks Apparatus",
        "prompt": "During a cholera outbreak in a rural camp, a public health inspector uses Horrocks apparatus to disinfect well water. What is the specific purpose of the Horrocks apparatus test in field water treatment?",
        "options": [
            "To measure the turbidity of raw water",
            "To estimate the dose of bleaching powder required to disinfect water",
            "To detect the presence of coliform organisms in water",
            "To measure dissolved oxygen in river water"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nHorrocks apparatus is a portable field test kit used in rural public health to estimate the exact quantity of bleaching powder (chlorinated lime) needed to disinfect a given volume (e.g., 455 liters or 100 gallons) of well or tank water. The kit contains 6 white cups, 1 black cup with a red mark, a metal spoon (holding 2 grams of bleaching powder), pipettes, and starch-iodide indicator solution. A calculated amount of bleaching powder is titrated across the cups until a faint blue color appears upon adding starch iodide, indicating the exact breakpoint chlorine demand of the water.\n\nOption Review:\n- Option A is incorrect because turbidity is measured using a turbidimeter or Jackson's candle.\n- Option B is correct because Horrocks apparatus determines the precise dose of bleaching powder required to disinfect a well.\n- Option C is incorrect because coliform detection requires membrane filtration, multiple tube fermentation, or MacConkey broth incubation.\n- Option D is incorrect because dissolved oxygen is measured by the Winkler titration method.\n\nKey Takeaway: Horrocks apparatus is used in field public health to determine the exact quantity of bleaching powder required to chlorinate well water.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q122",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Demography - Total Fertility Rate",
        "prompt": "A state demographer analyzes recent reproductive health data showing that the Total Fertility Rate (TFR) has dropped to 2.1 children per woman. At this demographic level, population stability will eventually be achieved. What does a Total Fertility Rate of 2.1 signify in demography?",
        "options": [
            "Maximum biological fecundity",
            "Replacement level fertility",
            "Zero population growth rate immediately",
            "Net reproduction rate of two"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe Total Fertility Rate (TFR) is the average number of children that would be born to a woman if she were to live to the end of her childbearing years and bear children in accordance with prevailing age-specific fertility rates. A TFR of 2.1 is defined as 'replacement level fertility'. The '0.1' extra child compensates for infant and child mortality before reaching reproductive age. At replacement level fertility, each generation of women replaces themselves and their partners, yielding a Net Reproduction Rate (NRR) of 1.0. Zero population growth is achieved several decades later due to population momentum.\n\nOption Review:\n- Option A is incorrect because biological fecundity represents maximum potential reproductive capacity (~15 children per woman).\n- Option B is correct because a TFR of 2.1 represents replacement level fertility.\n- Option C is incorrect because population momentum ensures the population continues growing for a few decades even after reaching TFR 2.1.\n- Option D is incorrect because replacement level fertility corresponds to an NRR of 1.0, not 2.0.\n\nKey Takeaway: A Total Fertility Rate of 2.1 represents replacement-level fertility, corresponding to a Net Reproduction Rate (NRR) of 1.0.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q123",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Environmental Health - Air Quality Index Indicators",
        "prompt": "During winter months in northern India, severe air pollution leads to high Air Quality Index (AQI) values. Particulate matter with an aerodynamic diameter of less than 2.5 micrometers (PM2.5) poses the greatest health risk to human lungs. Why is PM2.5 significantly more hazardous than larger particulate matter (PM10)?",
        "options": [
            "It is completely filtered by nasal hairs and causes rhinitis only",
            "It penetrates deep into terminal bronchioles and alveoli, entering systemic circulation",
            "It cannot be inhaled past the laryngeal vocal cords",
            "It is rapidly cleared within seconds by the tracheobronchial mucociliary escalator"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nParticulate matter is classified based on aerodynamic diameter: 1) PM10 (coarse particles between 2.5 and 10 micrometers): Trapped in the upper respiratory tract, nasal cavity, and large conducting airways, where they are cleared by the mucociliary escalator; 2) PM2.5 (fine particles < 2.5 micrometers): Small enough to bypass the upper respiratory defenses and penetrate deep into the terminal bronchioles and alveoli. In the alveoli, PM2.5 triggers local inflammation, impairs gas exchange, and can cross the thin alveolar-capillary barrier into systemic circulation, inducing systemic endothelial dysfunction, atherosclerosis, stroke, and ischemic heart disease.\n\nOption Review:\n- Option A is incorrect because PM2.5 easily bypasses nasal hairs.\n- Option B is correct because PM2.5 penetrates deep into the alveoli and can cross into the systemic circulation.\n- Option C is incorrect because PM2.5 readily passes the larynx into peripheral lung units.\n- Option D is incorrect because alveolar spaces lack cilia; clearance relies on slow macrophage phagocytosis rather than rapid mucociliary action.\n\nKey Takeaway: PM2.5 particles are hazardous because they penetrate beyond terminal bronchioles into the alveoli, crossing into systemic circulation to cause cardiovascular and pulmonary disease.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q124",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Communicable Diseases - Polio Eradication & VVM",
        "prompt": "Before administering oral poliovirus vaccine (OPV) during a pulse polio immunization campaign, the vaccinator checks the Vaccine Vial Monitor (VVM). The central square is white and significantly lighter than the dark surrounding circle. What action should the vaccinator take regarding this vaccine vial?",
        "options": [
            "Discard the vial immediately",
            "Use the vaccine vial",
            "Send the vial to the manufacturer for re-testing",
            "Boil the vial before administration"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe Vaccine Vial Monitor (VVM) is a heat-sensitive chemical label placed on vaccine vials (especially heat-labile OPV) that registers cumulative heat exposure over time. Interpretation: 1) Stage 1: Inner square is lighter than outer circle (square is white) -> USE THE VACCINE; 2) Stage 2: Inner square is still lighter than outer circle, but slightly gray -> USE THE VACCINE (use first if other vials available); 3) Stage 3 (Discard point): Inner square matches the color of the outer circle -> DO NOT USE, DISCARD; 4) Stage 4: Inner square is darker than the outer circle -> DO NOT USE, DISCARD.\n\nOption Review:\n- Option A is incorrect because discarding is indicated only at Stage 3 or Stage 4 when the inner square matches or is darker than the outer circle.\n- Option B is correct because when the central square is lighter than the surrounding circle, the vaccine has not suffered cumulative heat damage and should be used.\n- Option C is incorrect because re-testing is unnecessary for a valid VVM.\n- Option D is incorrect because boiling destroys live attenuated viral vaccines.\n\nKey Takeaway: A vaccine vial whose VVM inner square is lighter than the outer circle is potent and should be used; discard when the square matches or exceeds the darkness of the circle.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q125",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Screening - Lead Time Bias",
        "prompt": "A new screening biomarker detects prostate cancer an average of 4 years earlier than traditional clinical symptoms. In a 5-year follow-up study, patients whose cancer was detected by screening appear to survive significantly longer after diagnosis than unscreened patients, even though the actual age at death is identical in both groups. What epidemiological bias produces this false appearance of increased survival time?",
        "options": [
            "Lead time bias",
            "Length time bias",
            "Berkson bias",
            "Hawthorne effect"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nLead time is the period between the early detection of a disease by screening and the time when it would have normally presented with clinical symptoms. Lead time bias occurs when screening detects a disease earlier in its course without altering the actual biological progression or life expectancy. Because survival is calculated from the date of diagnosis to the date of death, diagnosing the disease earlier creates the statistical illusion of prolonged survival, even when the patient dies at the exact same age. To eliminate lead time bias, screening efficacy must be measured by mortality rates in the population, not survival time from diagnosis.\n\nOption Review:\n- Option A is correct because the false appearance of increased survival caused by earlier detection is lead time bias.\n- Option B is incorrect because length time bias occurs because screening selectively detects slow-growing, indolent cases that have a better intrinsic prognosis.\n- Option C is incorrect because Berkson bias is selection bias resulting from using hospitalized patients as controls.\n- Option D is incorrect because the Hawthorne effect occurs when study subjects alter their behavior because they know they are being observed.\n\nKey Takeaway: Lead time bias creates a false impression of improved survival because early screening shifts the date of diagnosis forward without altering the date of death.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q126",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Non-Communicable Diseases - Metabolic Syndrome Criteria",
        "prompt": "A 48-year-old male undergoes a health check-up. According to the National Cholesterol Education Program Adult Treatment Panel III (NCEP ATP III) guidelines, metabolic syndrome is diagnosed when at least 3 of 5 clinical criteria are met. Which of the following parameters meets the diagnostic threshold for metabolic syndrome?",
        "options": [
            "Fasting plasma glucose 90 mg/dL",
            "Serum triglycerides 180 mg/dL",
            "Blood pressure 120/75 mmHg",
            "HDL cholesterol 55 mg/dL in a male"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nUnder NCEP ATP III guidelines, Metabolic Syndrome is diagnosed when 3 or more of the following 5 criteria are present: 1) Elevated waist circumference: >102 cm (40 inches) in men, >88 cm (35 inches) in women (for South Asians: >90 cm in men, >80 cm in women); 2) Elevated triglycerides: >= 150 mg/dL (or drug treatment for hypertriglyceridemia); 3) Reduced HDL cholesterol: < 40 mg/dL in men, < 50 mg/dL in women; 4) Elevated blood pressure: >= 130 mmHg systolic or >= 85 mmHg diastolic (or antihypertensive therapy); 5) Elevated fasting glucose: >= 100 mg/dL (or drug therapy for elevated glucose).\n\nOption Review:\n- Option A is incorrect because normal fasting glucose is <100 mg/dL; cutoff is >=100 mg/dL.\n- Option B is correct because fasting triglycerides >= 150 mg/dL meets the ATP III diagnostic criteria (180 mg/dL is elevated).\n- Option C is incorrect because the blood pressure threshold is >= 130/85 mmHg.\n- Option D is incorrect because an HDL of 55 mg/dL is protective; the criterion is reduced HDL (<40 mg/dL in men).\n\nKey Takeaway: Fasting triglycerides >= 150 mg/dL constitutes one of the five diagnostic criteria for metabolic syndrome under NCEP ATP III.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q127",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "School Health - Mid-Day Meal Scheme Norms",
        "prompt": "Under the PM POSHAN Scheme (formerly National Programme of Nutritional Support to Primary Education / Mid-Day Meal Scheme) in India, what are the minimum statutory nutritional norms mandated for upper primary school children (classes VI to VIII) per school day?",
        "options": [
            "450 calories and 12 grams of protein",
            "700 calories and 20 grams of protein",
            "1,000 calories and 30 grams of protein",
            "300 calories and 8 grams of protein"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe Mid-Day Meal Scheme (now PM POSHAN) specifies standardized nutritional norms to combat classroom hunger and child malnutrition: 1) Primary stage (Classes I to V): Mandates a minimum of 450 calories and 12 grams of protein per child per school day (from 100 grams of food grains); 2) Upper Primary stage (Classes VI to VIII): Mandates a minimum of 700 calories and 20 grams of protein per child per school day (from 150 grams of food grains), along with adequate micronutrients (iron, folic acid, vitamin A).\n\nOption Review:\n- Option A is incorrect because 450 calories and 12 grams of protein is the norm for primary school children (Classes I to V).\n- Option B is correct because 700 calories and 20 grams of protein is the statutory requirement for upper primary children (Classes VI to VIII).\n- Option C is incorrect because 1,000 calories exceeds the single mid-day meal allowance.\n- Option D is incorrect because 300 calories is below the mandated standard.\n\nKey Takeaway: The PM POSHAN (Mid-Day Meal) norm for upper primary children is 700 calories and 20 grams of protein per child per school day.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q128",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Biostatistics - Hypothesis Testing & Types of Error",
        "prompt": "A phase III clinical trial compares a new antihypertensive drug against placebo. In reality, the drug has zero therapeutic benefit (null hypothesis is true). However, due to random sampling variation, the statistical test yields a p-value of 0.03, leading researchers to incorrectly reject the null hypothesis and claim the drug is effective. What type of statistical error has been committed?",
        "options": [
            "Type I error",
            "Type II error",
            "Sampling bias",
            "Measurement error"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIn statistical hypothesis testing: 1) Type I error (alpha error, false positive): Occurs when the researcher rejects the null hypothesis (H0) when the null hypothesis is actually true in reality (concluding there is a significant effect or difference when none actually exists). The probability of committing a Type I error is set by the significance level (alpha, typically 0.05); 2) Type II error (beta error, false negative): Occurs when the researcher fails to reject the null hypothesis when the null hypothesis is actually false (failing to detect a real difference). Statistical Power = 1 - beta.\n\nOption Review:\n- Option A is correct because rejecting a true null hypothesis (finding a false positive difference) is a Type I error.\n- Option B is incorrect because a Type II error involves failing to detect a true difference (false negative).\n- Option C is incorrect because sampling bias is a non-random systematic error in subject selection.\n- Option D is incorrect because measurement error is inaccuracy in instrument recording.\n\nKey Takeaway: A Type I error (alpha error) occurs when researchers reject a true null hypothesis, finding a false-positive treatment effect.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q129",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Nutrition - Vitamin A Prophylaxis Program",
        "prompt": "Under the National Prophylaxis Programme against Nutritional Blindness in India, periodic massive-dose vitamin A supplementation is administered to prevent xerophthalmia. What is the standard dose of oral vitamin A administered to an infant at 9 months of age alongside the measles-rubella vaccine?",
        "options": [
            "50,000 International Units",
            "100,000 International Units",
            "200,000 International Units",
            "500,000 International Units"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe National Vitamin A Prophylaxis Program schedules 9 total mega-doses of oral vitamin A syrup to children between 9 and 59 months: 1) First dose: Administered at 9 months of age (along with MR-1 / Measles vaccine) as 100,000 International Units (1 mL of oil-based solution containing 100,000 IU/mL); 2) Subsequent doses (Doses 2 to 9): Administered every 6 months up to the age of 5 years as 200,000 International Units (2 mL) per dose. The total cumulative dose received over 5 years is 1,700,000 IU.\n\nOption Review:\n- Option A is incorrect because 50,000 IU is given to infants under 6 months during acute treatment of measles, not routine prophylaxis.\n- Option B is correct because 100,000 IU (1 mL) is the standard first prophylactic dose at 9 months of age.\n- Option C is incorrect because 200,000 IU is the dose administered for subsequent rounds (doses 2 through 9 starting at 16 to 18 months).\n- Option D is incorrect because 500,000 IU is a toxic megadose.\n\nKey Takeaway: The first dose of Vitamin A at 9 months of age is 100,000 IU (1 mL); all subsequent 8 doses up to 5 years are 200,000 IU (2 mL) every 6 months.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q130",
        "subjectId": "community-medicine",
        "subjectTitle": "Community Medicine (PSM)",
        "topic": "Maternal & Child Health - ASHA Worker Profile",
        "prompt": "An Accredited Social Health Activist (ASHA) is an honorary community health volunteer under the National Health Mission (NHM). According to national guidelines, what is the standard general population coverage norm for one ASHA worker in rural areas?",
        "options": [
            "1 ASHA per 500 population",
            "1 ASHA per 1,000 population",
            "1 ASHA per 2,500 population",
            "1 ASHA per 5,000 population"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nUnder the National Rural Health Mission (NRHM / NHM), an Accredited Social Health Activist (ASHA) is an honorary female resident volunteer who acts as the primary interface between the community and the public healthcare system. The selection criteria specify: 1) Coverage norm: One ASHA per 1,000 population in rural areas (or 1 per habitation/village in hilly, tribal, or low-density areas); 2) Profile: Resident woman of the village, married/widowed/divorced, aged 25 to 45 years, with formal education up to at least the 10th standard (relaxed only if no suitable literate candidate is available); 3) Compensation: Performance-based incentive (honorary, not salaried).\n\nOption Review:\n- Option A is incorrect because 1 per 500 is used for Anganwadi workers in small hamlets or tribal areas.\n- Option B is correct because 1 ASHA per 1,000 rural population is the national standard norm.\n- Option C is incorrect because 2,500 is not a designated ASHA norm.\n- Option D is incorrect because 1 per 5,000 is the norm for a rural Sub-Centre, not a single ASHA.\n\nKey Takeaway: In rural India, one ASHA worker is appointed per 1,000 population to serve as a community health educator and facilitator.",
        "imageUrls": []
    },

    # ==========================================
    # OPHTHALMOLOGY (10 Questions: Q131 - Q140)
    # ==========================================
    {
        "id": "fmge-gt1-q131",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Glaucoma - Acute Angle-Closure Glaucoma",
        "prompt": "A 58-year-old hyperopic female presents with sudden, agonizing pain in her right eye, accompanied by blurred vision, colored halos around lights, nausea, and vomiting. On examination, the right eye shows ciliary injection, a hazy edematous cornea, a shallow anterior chamber, and a vertically oval, mid-dilated, fixed pupil. Intraocular pressure in the right eye is 62 mmHg. What is the definitive surgical treatment to prevent future attacks?",
        "options": [
            "Laser peripheral iridotomy",
            "Trabeculectomy with mitomycin C",
            "Cyclocryotherapy",
            "Pars plana vitrectomy"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAcute angle-closure glaucoma is an ophthalmic emergency that occurs in eyes with shallow anterior chambers (anatomically predisposed in hyperopes, elderly with growing lens). Pupillary block prevents aqueous humor from passing from the posterior to the anterior chamber, causing relative pupillary block. Pressure accumulates in the posterior chamber, ballooning the peripheral iris forward (iris bombé) to occlude the trabecular meshwork, causing IOP to spike (>50-60 mmHg). While medical therapy (IV mannitol, topical timolol, apraclonidine, pilocarpine, oral acetazolamide) is used to break the acute attack, the definitive curative treatment is Nd:YAG Laser Peripheral Iridotomy (LPI) in both the affected eye and prophylactically in the contralateral fellow eye to bypass the pupillary block.\n\nOption Review:\n- Option A is correct because laser peripheral iridotomy creates a patent bypass channel between posterior and anterior chambers, curing pupillary block.\n- Option B is incorrect because trabeculectomy is reserved for chronic open-angle glaucoma or cases where iridotomy fails due to extensive peripheral anterior synechiae.\n- Option C is incorrect because cyclocryotherapy is a destructive ciliary body procedure used for refractory absolute blind painful eyes.\n- Option D is incorrect because vitrectomy treats vitreoretinal diseases, not anterior pupillary block.\n\nKey Takeaway: Bilateral Nd:YAG laser peripheral iridotomy is the definitive treatment for acute angle-closure glaucoma following initial medical pressure reduction.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q132",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Retina - Central Retinal Artery Occlusion",
        "prompt": "A 70-year-old male with atrial fibrillation experiences sudden, catastrophic, painless loss of vision in his left eye. Visual acuity is reduced to hand motions. Fundoscopic examination reveals marked diffuse pallor and retinal whitening throughout the posterior pole with a prominent 'cherry-red spot' visible in the fovea. What is the underlying vascular diagnosis?",
        "options": [
            "Central retinal vein occlusion",
            "Central retinal artery occlusion",
            "Rhegmatogenous retinal detachment",
            "Non-arteritic anterior ischemic optic neuropathy"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nCentral Retinal Artery Occlusion (CRAO) is an ocular emergency caused by embolic (atherosclerotic, cardiac) or thrombotic occlusion of the central retinal artery. The inner two-thirds of the retina supplied by the CRA undergoes acute ischemic infarction, producing cloudy, opaque, milky-white retinal edema. Because the fovea centralis lacks inner retinal layers and is nourished independently by underlying choroidal vessels (via the short posterior ciliary arteries), the vascular choroid shines brightly through the thin foveolar depression, creating the classic 'cherry-red spot'. Immediate interventions (ocular massage, anterior chamber paracentesis, sublingual isosorbide dinitrate) must be attempted within 90 to 100 minutes to prevent irreversible retinal ganglion cell necrosis.\n\nOption Review:\n- Option A is incorrect because central retinal vein occlusion (CRVO) produces extensive retinal hemorrhages in all four quadrants ('blood and thunder' fundus) and tortuous dilated veins.\n- Option B is correct because sudden painless vision loss with diffuse retinal pallor and a foveal cherry-red spot is diagnostic of CRAO.\n- Option C is incorrect because retinal detachment displays an elevated, undulating, corrugated gray retinal fold with a tear.\n- Option D is incorrect because ischemic optic neuropathy shows pale optic disc edema without a cherry-red spot.\n\nKey Takeaway: Sudden, painless visual loss with a milky-white retina and foveal 'cherry-red spot' is diagnostic of Central Retinal Artery Occlusion (CRAO).",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Cherry_red_spot.jpg/640px-Cherry_red_spot.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q133",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Retina - Diabetic Retinopathy Proliferative vs NPDR",
        "prompt": "A 56-year-old female with a 15-year history of poorly controlled type 2 diabetes presents for an annual eye check-up. Dilated fundoscopic examination demonstrates extensive retinal microaneurysms, blot hemorrhages, hard exudates, and cotton-wool spots. In addition, prominent neovascularization of the optic disc (NVD) is identified. Which stage of diabetic retinopathy is confirmed by the presence of neovascularization?",
        "options": [
            "Mild non-proliferative diabetic retinopathy",
            "Moderate non-proliferative diabetic retinopathy",
            "Severe non-proliferative diabetic retinopathy",
            "Proliferative diabetic retinopathy"
        ],
        "answerIndex": 3,
        "explanation": "Clinical Reasoning:\nDiabetic retinopathy is broadly categorized into Non-Proliferative (NPDR) and Proliferative (PDR). The defining hallmark that separates PDR from NPDR is the development of neovascularization (new, fragile blood vessels growing on the retinal surface or optic disc) stimulated by retinal hypoxia and vascular endothelial growth factor (VEGF). Features of PDR include: 1) Neovascularization of the disc (NVD); 2) Neovascularization elsewhere (NVE); 3) Preretinal or vitreous hemorrhage; 4) Fibrovascular proliferation leading to tractional retinal detachment. High-risk PDR warrants urgent Pan-Retinal Photocoagulation (PRP) or intravitreal anti-VEGF injections.\n\nOption Review:\n- Option A is incorrect because mild NPDR shows microaneurysms only.\n- Option B is incorrect because moderate NPDR includes microaneurysms, hemorrhages, and hard exudates without neovascularization.\n- Option C is incorrect because severe NPDR meets the 4:2:1 rule (hemorrhages in 4 quadrants, venous beading in 2, IRMA in 1) but lacks true neovascularization.\n- Option D is correct because the presence of neovascularization (NVD or NVE) is the absolute diagnostic criterion for Proliferative Diabetic Retinopathy (PDR).\n\nKey Takeaway: Proliferative diabetic retinopathy (PDR) is distinguished from non-proliferative disease by the growth of abnormal new blood vessels (neovascularization of the disc or retina).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q134",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Cornea - Herpes Simplex Keratitis",
        "prompt": "A 35-year-old male presents with unilateral eye redness, foreign-body sensation, photophobia, and decreased vision. Corneal sensation is markedly diminished on cotton-wisp testing. Slit-lamp examination after instillation of 1% sodium fluorescein dye reveals a classic branching, linear arborizing epithelial ulcer with terminal rounded bulbs. Which pathogen causes this characteristic dendritic keratitis?",
        "options": [
            "Herpes simplex virus",
            "Adenovirus",
            "Pseudomonas aeruginosa",
            "Acanthamoeba"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nHerpes simplex virus (HSV-1) is the leading infectious cause of corneal blindness in developed nations. Following primary orofacial infection, HSV remains latent within the trigeminal ganglion. Reactivation down the ophthalmic branch (V1) results in recurrent epithelial keratitis. Pathognomonic clinical features include: 1) Reduced corneal sensation (corneal hypoesthesia due to neurotrophic sensory nerve damage); 2) Dendritic ulcer: A true branching linear ulcer with terminal buds/bulbs; 3) Fluorescein staining: Stains the central ulcerated epithelial bed bright green, while Rose Bengal stains devitalized epithelial cells at the ulcer margins. Topical corticosteroids are strictly CONTRAINDICATED in epithelial dendritic keratitis as they cause amoeboid/geographic ulceration.\n\nOption Review:\n- Option A is correct because Herpes simplex virus causes the pathognomonic branching dendritic corneal ulcer.\n- Option B is incorrect because Adenovirus causes epidemic keratoconjunctivitis with subepithelial nummular infiltrates.\n- Option C is incorrect because Pseudomonas aeruginosa causes rapidly progressive, suppurative keratitis with greenish-yellow exudate and corneal melting.\n- Option D is incorrect because Acanthamoeba causes radial keratoneuritis and ring-shaped stromal infiltrates in contact lens wearers.\n\nKey Takeaway: Herpes simplex virus causes corneal hypoesthesia and a classic dendritic branching epithelial ulcer with terminal bulbs on fluorescein staining.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Dendritic_corneal_ulcer_due_to_HSV.jpg/640px-Dendritic_corneal_ulcer_due_to_HSV.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q135",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Retina - Rhegmatogenous Retinal Detachment",
        "prompt": "A 52-year-old high myope presents with a 2-day history of flashes of light (photopsia) and multiple new floaters in his right eye, followed by a dark curtain-like shadow advancing from the superior periphery toward the visual center. Dilated fundoscopy reveals an elevated, undulating, mobile, translucent gray retinal fold with a horseshoe-shaped full-thickness break. What is the pathophysiological mechanism of this retinal detachment?",
        "options": [
            "Fluid accumulation in the subretinal space through a full-thickness retinal tear",
            "Fibrovascular tissue contracting and mechanically pulling the retina",
            "Exudation of serous fluid secondary to severe choroidal inflammation",
            "Subretinal neovascular membrane bleeding"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nRetinal detachments are classified into three types: 1) Rhegmatogenous (most common): Arises from a full-thickness break or tear (rhegma) in the sensory retina (commonly preceded by posterior vitreous detachment and traction in myopes). Liquefied vitreous humor passes through the tear into the potential subretinal space, peeling the neurosensory retina away from the underlying retinal pigment epithelium (RPE); 2) Tractional: Fibrovascular membranes contract and physically pull the retina off the RPE without a tear (seen in proliferative diabetic retinopathy); 3) Exudative/Serous: Fluid accumulates in the subretinal space due to breakdown of the blood-retinal barrier without a tear or traction (seen in choroidal tumors, Vogt-Koyanagi-Harada disease, malignant hypertension).\n\nOption Review:\n- Option A is correct because rhegmatogenous retinal detachment is caused by liquefied vitreous tracking through a full-thickness retinal tear.\n- Option B is incorrect because mechanical traction from fibrovascular membranes defines tractional retinal detachment.\n- Option C is incorrect because inflammatory fluid accumulation defines exudative (serous) retinal detachment.\n- Option D is incorrect because subretinal neovascular bleeding causes wet age-related macular degeneration.\n\nKey Takeaway: Rhegmatogenous retinal detachment is caused by liquefied vitreous humor dissecting through a full-thickness retinal break, separating the neurosensory retina from the RPE.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q136",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Neuro-Ophthalmology - Horner Syndrome",
        "prompt": "A 45-year-old male smoker with a pancoast tumor at the apex of the right lung presents with right-sided partial ptosis, pupillary miosis, and anhidrosis over the right side of his face. The right pupil is smaller in dim light and dilates poorly compared to the left. Instillation of apraclonidine drops reverses the anisocoria (dilates the Horner pupil). What neural pathway is interrupted in Horner syndrome?",
        "options": [
            "Parasympathetic fibers originating from the Edinger-Westphal nucleus",
            "Oculosympathetic pathway originating in the posterolateral hypothalamus",
            "Somatic motor fibers of the oculomotor nerve",
            "Trigeminal sensory afferents"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nHorner syndrome results from a lesion anywhere along the three-neuron oculosympathetic pathway: 1) First-order (central) neuron: Originates in the posterolateral hypothalamus, descends through the brainstem to the ciliospinal center of Budge (C8-T2); 2) Second-order (preganglionic) neuron: Exits C8-T2, traverses the sympathetic chain over the lung apex, and ascends to the superior cervical ganglion (frequently invaded by apical Pancoast lung carcinomas); 3) Third-order (postganglionic) neuron: Ascends along the internal carotid artery to supply the pupillary dilator muscle and superior tarsal (Muller's) muscle. Interruption produces the classic triad: Ptosis (Muller's muscle paralysis), Miosis (unopposed parasympathetic sphincter), and Anhidrosis (loss of facial sweat innervation).\n\nOption Review:\n- Option A is incorrect because interruption of parasympathetic fibers from the Edinger-Westphal nucleus causes mydriasis and loss of accommodation (third nerve palsy).\n- Option B is correct because Horner syndrome is caused by disruption of the oculosympathetic pathway.\n- Option C is incorrect because somatic motor lesions cause complete ptosis (levator palpebrae) and 'down-and-out' globe displacement.\n- Option D is incorrect because trigeminal sensory lesions cause facial numbness, not miosis and ptosis.\n\nKey Takeaway: Horner syndrome presents with the classic triad of ptosis, miosis, and anhidrosis caused by interruption of the three-neuron oculosympathetic pathway.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q137",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Optic Nerve - Papilledema vs Papillitis",
        "prompt": "A 32-year-old obese female presents with generalized headache, pulsatile tinnitus, transient visual obscurations lasting seconds, and horizontal diplopia on lateral gaze. Bilateral fundoscopy reveals elevated optic nerve heads with blurred disc margins, obscuration of retinal vessels at the disc border, absent spontaneous venous pulsations, and flame-shaped peripapillary hemorrhages. Visual acuity is 20/20 in both eyes. What is this non-inflammatory optic disc edema caused by elevated intracranial pressure called?",
        "options": [
            "Papillitis",
            "Papilledema",
            "Retrobulbar neuritis",
            "Anterior ischemic optic neuropathy"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nPapilledema is strictly defined as bilateral passive edema of the optic nerve head secondary to elevated intracranial pressure (ICP). The subarachnoid space surrounding the brain is continuous with the optic nerve sheath. Elevated CSF pressure transmits forward, compressing the optic nerve and axoplasmic flow in the unmyelinated axons at the lamina cribrosa. Hallmark fundoscopic features include: blurring of disc margins, cup obliteration, elevation of the optic nerve head, venous engorgement with loss of spontaneous venous pulsation, and peripapillary flame hemorrhages. In early stages, visual acuity is characteristically PRESERVED (20/20), with only enlarged blind spots on visual fields. This stands in sharp contrast to optic neuritis (papillitis), which causes early, profound central visual loss and an afferent pupillary defect.\n\nOption Review:\n- Option A is incorrect because papillitis is an inflammatory optic neuritis causing severe visual loss, pain on eye movement, and relative afferent pupillary defect.\n- Option B is correct because bilateral disc swelling caused by raised intracranial pressure with preserved early visual acuity is papilledema.\n- Option C is incorrect because retrobulbar neuritis presents with normal-appearing optic discs ('neither the doctor nor the patient sees anything').\n- Option D is incorrect because AION presents with sudden, painless, altitudinal visual field defect in older vasculopaths.\n\nKey Takeaway: Papilledema represents bilateral optic disc edema caused by raised intracranial pressure, presenting with preserved visual acuity in early stages.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q138",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Lens - Age-Related Cataract Types",
        "prompt": "A 68-year-old male complains of gradual, painless progressive decline in distance vision over the past two years. Interestingly, he notes that he is now able to read fine print without using his reading glasses ('second sight'). Slit-lamp examination reveals a yellowish-brown opacity and marked compaction localized to the center of the crystalline lens. What specific morphological type of age-related cataract causes this index myopia?",
        "options": [
            "Cortical cataract",
            "Nuclear sclerotic cataract",
            "Posterior subcapsular cataract",
            "Anterior polar cataract"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nAge-related cataracts are classified by anatomical location: 1) Nuclear sclerotic cataract: Progressive compaction and yellowing/browning of the central lens nucleus due to insoluble protein aggregation. Sclerosis increases the refractive index of the lens nucleus, producing index myopia (a shift toward nearsightedness). This temporary improvement in near vision allows elderly presbyopic patients to read without glasses, a phenomenon termed 'second sight'; 2) Cortical cataract: Involves the lens cortex; presents with radial, wedge-shaped opacities ('cuneiform spoke-like opacities') and causes prominent glare/halos; 3) Posterior subcapsular cataract: Located beneath the posterior capsule in the visual axis; causes early, disabling reduction in near vision and severe daytime glare; commonly induced by systemic corticosteroids.\n\nOption Review:\n- Option A is incorrect because cortical cataracts produce spoke-like cortical opacities and glare, without 'second sight'.\n- Option B is correct because nuclear sclerotic cataract increases the refractive index of the nucleus, producing index myopia ('second sight').\n- Option C is incorrect because posterior subcapsular cataracts impair near vision early and are associated with steroid therapy.\n- Option D is incorrect because anterior polar cataracts are congenital or developmental opacities at the anterior pole.\n\nKey Takeaway: Nuclear sclerotic cataracts cause index myopia, temporarily restoring near vision in presbyopic elderly individuals ('second sight').",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q139",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Conjunctiva - Trachoma Stages & WHO Classification",
        "prompt": "In an arid rural community, a public health survey examines school children for ocular infections. Several children exhibit chronic follicular conjunctivitis with follicles on the upper tarsal conjunctiva, progressive scarring, vascular pannus extending onto the superior cornea, and Herbert's pits at the limbus. Untreated, cicatricial entropion and trichiasis lead to corneal opacification and blindness. Which serovars of Chlamydia trachomatis cause endemic blinding trachoma?",
        "options": [
            "Serovars A, B, Ba, and C",
            "Serovars D through K",
            "Serovars L1, L2, and L3",
            "Serovars E and F only"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nTrachoma is the world's leading infectious cause of preventable blindness, caused by ocular infection with Chlamydia trachomatis: 1) Serovars A, B, Ba, and C: Cause chronic endemic blinding trachoma (mnemonic: A, B, C = Blindness in Africa/Children); 2) Serovars D through K: Cause inclusion conjunctivitis in adults, neonatal inclusion blennorrhea, and sexually transmitted urogenital chlamydial infections (urethritis, cervicitis, PID); 3) Serovars L1, L2, and L3: Cause lymphogranuloma venereum (LGV), presenting with transient genital ulcers and suppurative inguinal lymphadenitis. Trachoma transmission is managed by the WHO 'SAFE' strategy: Surgery, Antibiotics (azithromycin), Facial cleanliness, Environmental improvement.\n\nOption Review:\n- Option A is correct because Chlamydia trachomatis serovars A, B, Ba, and C cause endemic blinding trachoma.\n- Option B is incorrect because serovars D-K cause sexually transmitted urogenital infections and inclusion conjunctivitis.\n- Option C is incorrect because serovars L1-L3 cause lymphogranuloma venereum.\n- Option D is incorrect because E and F are included in the genital D-K serogroup.\n\nKey Takeaway: Endemic blinding trachoma is caused by Chlamydia trachomatis serovars A, B, Ba, and C, managed via the WHO SAFE strategy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q140",
        "subjectId": "ophthalmology",
        "subjectTitle": "Ophthalmology",
        "topic": "Neuro-Ophthalmology - Visual Field Pathway Lesions",
        "prompt": "A 50-year-old male presents with visual difficulties while driving. Automated perimetry testing reveals an incongruous, complete homonymous hemianopia affecting the right visual field of both eyes (loss of temporal field in right eye and nasal field in left eye). Pupillary light reflexes are diminished when light is shone from the hemianopic field (Wernicke hemianopic pupil). An occlusion in which anatomical structure causes contralateral homonymous hemianopia with Wernicke pupil?",
        "options": [
            "Optic chiasm",
            "Left optic tract",
            "Left visual cortex in occipital pole",
            "Right optic radiation in parietal lobe"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nIn the visual pathway: 1) Optic tract: Carries decussated nasal retinal fibers from the contralateral eye and uncrossed temporal retinal fibers from the ipsilateral eye. A lesion of the left optic tract causes right homonymous hemianopia. Because pupillary light reflex afferent fibers travel in the optic tract before peeling off to the pretectal nucleus in the midbrain, an optic tract lesion disrupts the reflex arc when light shines on the denervated hemi-retinae, producing Wernicke's hemianopic pupillary response; 2) Optic chiasm lesion: Compresses crossing nasal fibers, causing bitemporal hemianopia; 3) Occipital cortex lesion: Causes homonymous hemianopia with macular sparing (dual blood supply from PCA and MCA), but the pupillary light reflex is completely normal because pupillary fibers exit anteriorly.\n\nOption Review:\n- Option A is incorrect because optic chiasm lesions produce bitemporal hemianopia, typically seen in pituitary adenomas.\n- Option B is correct because a left optic tract lesion causes contralateral (right) homonymous hemianopia accompanied by Wernicke's pupillary sign.\n- Option C is incorrect because occipital pole lesions produce homonymous hemianopia with macular sparing and intact pupillary reflexes.\n- Option D is incorrect because right parietal radiation lesions cause left inferior quadrantanopia ('pie on the floor').\n\nKey Takeaway: A lesion of the optic tract causes contralateral homonymous hemianopia associated with Wernicke's hemianopic pupillary response.",
        "imageUrls": []
    },

    # ==========================================
    # ENT (EAR, NOSE, THROAT) (10 Questions: Q141 - Q150)
    # ==========================================
    {
        "id": "fmge-gt1-q141",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Audiology - Tuning Fork Tests (Rinne & Weber)",
        "prompt": "A 32-year-old female presents with progressive hearing loss in her right ear. Tuning fork evaluation (512 Hz) reveals: Rinne test in the right ear demonstrates bone conduction is heard louder and longer than air conduction (negative Rinne); Rinne test in the left ear is positive (air conduction > bone conduction). On Weber testing, the tone lateralizes clearly to the right ear. What type and location of hearing impairment is diagnosed?",
        "options": [
            "Conductive hearing loss in the right ear",
            "Sensorineural hearing loss in the right ear",
            "Conductive hearing loss in the left ear",
            "Sensorineural hearing loss in the left ear"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nTuning fork tests (using a 512 Hz fork) distinguish conductive from sensorineural hearing loss: 1) Rinne test: In healthy ears and sensorineural loss, air conduction is greater than bone conduction (AC > BC = Positive Rinne). In conductive hearing loss, bone conduction exceeds air conduction (BC > AC = Negative Rinne); 2) Weber test: Sound vibrates the skull equally. In conductive hearing loss, the sound lateralizes to the POORER/AFFECTED ear (because environmental background masking noise is blocked in the diseased ear). In sensorineural hearing loss, sound lateralizes to the BETTER/UNAFFECTED ear. A negative Rinne in the right ear (BC > AC) combined with Weber lateralizing to the right confirms right-sided conductive hearing loss (e.g., otosclerosis, wax, otitis media).\n\nOption Review:\n- Option A is correct because negative Rinne in the right ear with Weber lateralization to the right indicates right conductive hearing loss.\n- Option B is incorrect because right sensorineural loss would produce a positive Rinne in both ears and Weber lateralizing to the left ear.\n- Option C is incorrect because the left ear demonstrated a normal positive Rinne.\n- Option D is incorrect because a left sensorineural loss would cause Weber to lateralize to the right, but both Rinne tests would remain positive.\n\nKey Takeaway: A negative Rinne test (BC > AC) combined with Weber lateralization to the same affected ear confirms conductive hearing loss.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q142",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Otology - Cholesteatoma & Atticoantral CSOM",
        "prompt": "A 28-year-old male presents with persistent, scanty, foul-smelling discharge from his left ear for 6 months. Otoscopic examination reveals an attic retraction pocket with white, cheesy flakes of keratin debris and erosion of the posterosuperior canal wall. What benign destructive lesion composed of keratinizing stratified squamous epithelium is present?",
        "options": [
            "Cholesteatoma",
            "Glomus tympanicum",
            "Otosclerosis",
            "Vestibular schwannoma"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nChronic Suppurative Otitis Media (CSOM) is classified into: 1) Tubotympanic ('safe' type): Central perforation of the pars tensa, profuse mucoid non-foul discharge, no bone erosion; 2) Atticoantral ('unsafe' type): Attico-marginal perforation or retraction pocket containing a cholesteatoma. A cholesteatoma is a three-dimensional non-neoplastic mass of keratinizing stratified squamous epithelium in the middle ear cleft that continuously sheds keratin debris. It secretes osteolytic enzymes (collagenases, acid phosphatases) that erode adjacent ossicles and the bony tegmen tympani, carrying high risk of intracranial complications (meningitis, brain abscess) and facial nerve palsy. Surgical management (canal-wall-down or up mastoidectomy) is mandatory.\n\nOption Review:\n- Option A is correct because an attic perforation with keratin debris and bone erosion is the diagnostic hallmark of a cholesteatoma.\n- Option B is incorrect because glomus tympanicum is a vascular paraganglioma presenting as a pulsating reddish-blue mass behind an intact drum with pulsatile tinnitus.\n- Option C is incorrect because otosclerosis affects the stapes footplate, presenting with conductive hearing loss and an intact, normal tympanic membrane.\n- Option D is incorrect because vestibular schwannoma (acoustic neuroma) arises from the internal auditory canal, causing unilateral sensorineural loss and tinnitus.\n\nKey Takeaway: Cholesteatomas are destructive keratinizing squamous epithelial collections in the attic/posterosuperior tympanic membrane that erode middle ear bone and require mastoidectomy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q143",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Otology - Meniere Disease vs BPPV",
        "prompt": "A 42-year-old male presents with episodic, disabling true vertigo lasting 2 to 4 hours, accompanied by fluctuating low-frequency sensorineural hearing loss, roaring tinnitus, and a sensation of fullness in his left ear. Audiometry confirms low-frequency sensorineural deficit. What pathological fluid abnormality in the membranous labyrinth underlies Meniere disease?",
        "options": [
            "Endolymphatic hydrops",
            "Canalithiasis of the posterior semicircular canal",
            "Perilymphatic fistula at the oval window",
            "Autoimmune destruction of the tectorial membrane"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nMeniere disease (idiopathic endolymphatic hydrops) is a disorder of the inner ear characterized by a classic tetrad: 1) Recurrent episodes of spontaneous vertigo lasting minutes to hours (typically 20 min to 12 hours); 2) Fluctuating, progressive sensorineural hearing loss (characteristically affecting low frequencies initially); 3) Roaring or oceanic tinnitus; 4) Aural fullness. Histopathologically, impaired resorption of endolymph by the endolymphatic sac leads to distension and episodic ruptures of the membranous labyrinth (endolymphatic hydrops). Management includes dietary salt restriction, diuretics (hydrochlorothiazide), betahistine, and intratympanic dexamethasone or gentamicin.\n\nOption Review:\n- Option A is correct because endolymphatic hydrops (distension of the endolymphatic system) is the proven pathological basis of Meniere disease.\n- Option B is incorrect because canalithiasis (calcium carbonate otoconia floating in the posterior semicircular canal) causes Benign Paroxysmal Positional Vertigo (BPPV), which produces brief vertigo lasting seconds triggered by head turns without hearing loss.\n- Option C is incorrect because perilymph fistula presents with vertigo and hearing loss precipitated by pressure changes (sneezing, straining, Hennebert sign).\n- Option D is incorrect because autoimmune destruction of the tectorial membrane is not the mechanism.\n\nKey Takeaway: Meniere disease is caused by endolymphatic hydrops, presenting with the tetrad of episodic vertigo, fluctuating low-frequency hearing loss, tinnitus, and aural fullness.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q144",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Otology - Otosclerosis & Carhart Notch",
        "prompt": "A 26-year-old female presents with bilateral progressive hearing loss that worsened significantly during her recent pregnancy. She notes that she hears better in noisy environments (paracusis willisii). Otoscopy shows normal, mobile tympanic membranes with a faint pinkish vascular hue over the promontory (Schwartze sign). Pure-tone audiometry shows conductive hearing loss with an apparent dip in bone conduction thresholds at 2,000 Hz. What is this classic audiometric dip called?",
        "options": [
            "Carhart notch",
            "Boilermaker notch",
            "Acoustic notch at 4,000 Hz",
            "Guye notch"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nOtosclerosis is an autosomal dominant condition characterized by abnormal bone remodeling of the otic capsule, where vascular spongy bone (spongiosis) replaces mature lamellar bone, most commonly at the fissula ante fenestram. This progressively fixes the stapes footplate in the oval window, causing bilateral conductive hearing loss. Key clinical features: 1) Onset in young adulthood, accelerated by pregnancy/estrogen; 2) Paracusis willisii (paradoxically hearing better in noisy environments because background speakers raise their voices); 3) Schwartze sign (flamingo pink vascular glow on the promontory); 4) Carhart notch: A pseudo-sensorineural dip in bone conduction thresholds centered at 2,000 Hz (2 kHz), caused by mechanical disruption of stapes inertial bone conduction. It resolves following stapedotomy.\n\nOption Review:\n- Option A is correct because the Carhart notch is an artifactual dip in bone conduction thresholds at 2,000 Hz diagnostic of stapedial otosclerosis.\n- Option B is incorrect because boilermaker notch is a lay term for noise-induced hearing loss.\n- Option C is incorrect because a sensory acoustic notch at 4,000 Hz is characteristic of noise-induced hearing loss.\n- Option D is incorrect because Guye notch is a fictitious distractor.\n\nKey Takeaway: Otosclerosis fixes the stapes footplate, producing conductive hearing loss, Schwartze sign, paracusis willisii, and a classic Carhart notch at 2,000 Hz on bone conduction.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q145",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Rhinology - Juvenile Nasopharyngeal Angiofibroma",
        "prompt": "A 15-year-old adolescent male presents with recurrent, profuse, spontaneous unilateral epistaxis and progressive left-sided nasal obstruction for 5 months. Rhinoscopy reveals a smooth, lobulated, purplish-red mass occupying the posterior nasal cavity and nasopharynx. Contrast-enhanced CT reveals an intensely enhancing soft-tissue lesion originating near the sphenopalatine foramen with anterior bowing of the posterior wall of the maxillary antrum (Holman-Miller sign). Why is a biopsy strictly contraindicated in the outpatient setting?",
        "options": [
            "Extreme risk of catastrophic, uncontrollable hemorrhage",
            "High propensity for immediate intracranial malignant seeding",
            "Immediate complete permanent paralysis of the facial nerve",
            "Severe risk of acute infectious cavernous sinus thrombosis"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nJuvenile Nasopharyngeal Angiofibroma (JNA) is a histologically benign but locally aggressive, non-encapsulated vascular tumor seen almost exclusively in adolescent males (testosterone-dependent). It originates at the posterolateral wall of the nasal cavity near the superior border of the sphenopalatine foramen. On CT/MRI, it displays pathognomonic anterior bowing of the posterior wall of the maxillary sinus (Holman-Miller / antral sign). The tumor consists of an irregular network of thin-walled blood vessels completely lacking an internal elastic lamina and smooth muscle coat, embedded in fibrous stroma. Because these vessels cannot contract, attempting an outpatient biopsy triggers massive, life-threatening, uncontrollable arterial hemorrhage. Preoperative transarterial embolization followed by surgical resection is the standard of care.\n\nOption Review:\n- Option A is correct because JNA vessels lack smooth muscle, creating an extreme risk of fatal, uncontrollable hemorrhage upon incisional biopsy.\n- Option B is incorrect because JNA is a benign vascular tumor that does not undergo malignant metastasis.\n- Option C is incorrect because biopsy does not cause immediate facial nerve paralysis.\n- Option D is incorrect because infectious cavernous sinus thrombosis is not the primary direct risk of tissue biopsy.\n\nKey Takeaway: Biopsy of suspected Juvenile Nasopharyngeal Angiofibroma is strictly contraindicated due to the severe risk of catastrophic, uncontrollable hemorrhage.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q146",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Rhinology - Epistaxis & Kiesselbach's Plexus",
        "prompt": "An 8-year-old boy presents to the emergency room with acute anterior epistaxis from his right nostril following habitual digital trauma (nose-picking). Anterior rhinoscopy reveals active bleeding from an arterial vascular network located in the anteroinferior part of the nasal septum. Which vascular confluence (Little's area / Kiesselbach's plexus) is the source of approximately 90% of anterior nosebleeds?",
        "options": [
            "Anastomosis of anterior ethmoidal, sphenopalatine, greater palatine, and superior labial arteries",
            "Anastomosis of posterior ethmoidal, maxillary, and ascending pharyngeal arteries",
            "Anastomosis of facial artery and internal carotid artery only",
            "Anastomosis of ophthalmic artery and transverse facial artery only"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nApproximately 90% of all episodes of epistaxis occur anteriorly from Little's area on the anteroinferior portion of the cartilaginous nasal septum. This area contains Kiesselbach's plexus, an extensive anastomotic network formed by terminal branches of both the external and internal carotid arterial systems: 1) Anterior ethmoidal artery (from ophthalmic artery, internal carotid system); 2) Sphenopalatine artery (terminal branch of maxillary artery, external carotid system); 3) Greater palatine artery (from maxillary artery, external carotid system); 4) Superior labial artery (septal branch of facial artery, external carotid system). Mnemonic: 'LEGS' (Labial, Ethmoidal, Greater palatine, Sphenopalatine).\n\nOption Review:\n- Option A is correct because Kiesselbach's plexus is formed by the anterior ethmoidal, sphenopalatine, greater palatine, and superior labial arteries.\n- Option B is incorrect because the posterior ethmoidal artery does not participate in Kiesselbach's plexus (Woodruff's plexus is posterior).\n- Option C is incorrect because multiple external carotid branches are involved, not simply the facial artery.\n- Option D is incorrect because the transverse facial artery supplies the parotid region and does not enter the nasal septum.\n\nKey Takeaway: Little's area on the anteroinferior septum is the site of Kiesselbach's plexus, formed by the anterior ethmoidal, sphenopalatine, greater palatine, and superior labial arteries.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q147",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Laryngology - Croup vs Acute Epiglottitis",
        "prompt": "A 3-year-old unimmunized child is brought to the emergency department leaning forward with his neck extended, drooling saliva, and in acute inspiratory distress with high fever (39.8°C). He is toxic-appearing and prefers to sit in a 'tripod position', refusing to lie down. Stridor is soft and muffled. Why is direct examination of the pharynx using a tongue depressor strictly contraindicated in the emergency ward?",
        "options": [
            "It may trigger immediate fatal complete laryngospasm and airway obstruction",
            "It invariably precipitates severe posterior epistaxis",
            "It ruptures a retropharyngeal abscess into the mediastinum",
            "It induces immediate bilateral vocal cord adductor paralysis"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAcute epiglottitis (supraglottitis), classically caused by Haemophilus influenzae type b (Hib), is a medical emergency. Children present toxic, febrile, drooling saliva (due to severe odynophagia), sitting upright in a 'tripod' posture with a muffled 'hot potato' voice and soft stridor. The epiglottis and aryepiglottic folds are severely swollen, cherry-red, and edematous. Attempting to visualize the throat with a tongue depressor or swab in a non-intubation setting can induce sudden, fatal, complete reflex laryngospasm and total airway occlusion. The child must be kept calm, transported directly to the operating room, and examined only with personnel and equipment ready for emergency endotracheal intubation or tracheostomy.\n\nOption Review:\n- Option A is correct because instrumentation with a tongue depressor can trigger fatal reflex laryngospasm and total acute airway obstruction.\n- Option B is incorrect because epistaxis is not the mechanism of sudden death in epiglottitis.\n- Option C is incorrect because retropharyngeal abscess is an anatomical space infection in the posterior pharyngeal wall, not supraglottitis.\n- Option D is incorrect because neural vocal cord paralysis does not occur acutely from mucosal contact.\n\nKey Takeaway: In suspected acute epiglottitis, direct oral examination with a tongue depressor is strictly contraindicated because it can trigger fatal complete laryngospasm.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q148",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Pharynx - Quinsy (Peritonsillar Abscess)",
        "prompt": "A 22-year-old male presents with severe unilateral left-sided throat pain, high fever, marked trismus (inability to open his mouth), and a muffled 'hot potato' voice. Examination reveals extensive erythema and medial displacement of the left tonsil, with the uvula pushed across the midline to the contralateral right side. What is the definitive emergency management for this peritonsillar abscess (quinsy)?",
        "options": [
            "Immediate incision and drainage followed by intravenous antibiotics",
            "Oral amoxicillin-clavulanate alone for 14 days",
            "Urgent bilateral tonsillectomy under local anesthesia",
            "Radiation therapy to the pharyngeal tonsils"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nPeritonsillar abscess (quinsy) is a collection of pus between the fibrous capsule of the palatine tonsil and the superior pharyngeal constrictor muscle, typically arising as a complication of acute bacterial tonsillitis. Key diagnostic signs include: severe unilateral odynophagia, trismus (due to irritation and spasm of the adjacent medial pterygoid muscle), muffled 'hot potato' voice, fullness of the soft palate, medial displacement of the tonsil, and uvular deviation to the opposite side. Management requires prompt emergency needle aspiration or incision and drainage (I&D) at the point of maximum fluctuance (or supra-tonsillar fossa), along with parenteral broad-spectrum antibiotics, followed by elective 'interval tonsillectomy' 6 weeks later.\n\nOption Review:\n- Option A is correct because immediate incision and drainage (or needle aspiration) with intravenous antibiotics is the definitive treatment for quinsy.\n- Option B is incorrect because oral antibiotics alone are inadequate to treat a mature peritonsillar abscess.\n- Option C is incorrect because tonsillectomy in the presence of acute severe peritonsillar phlegmon ('hot tonsillectomy') under local anesthesia carries extreme bleeding and airway risks.\n- Option D is incorrect because radiation therapy is used for malignant tumors, not infectious abscesses.\n\nKey Takeaway: Peritonsillar abscess (quinsy) presents with trismus, medial tonsillar displacement, and contralateral uvular deviation, requiring emergency incision and drainage.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q149",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Laryngology - Vocal Cord Paralysis Mechanics",
        "prompt": "A 45-year-old female undergoes a subtotal thyroidectomy. Immediately following extubation, she develops severe inspiratory stridor, tachypnea, and cyanosis, necessitating immediate reintubation. Fiberoptic laryngoscopy reveals that both true vocal cords are fixed in the paramedian position (1.5 to 2 mm from the midline), obstructing the glottic aperture during inspiration. Bilateral injury to which nerve produces this life-threatening airway emergency?",
        "options": [
            "Recurrent laryngeal nerve",
            "External branch of superior laryngeal nerve",
            "Internal branch of superior laryngeal nerve",
            "Glossopharyngeal nerve"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe recurrent laryngeal nerve (RLN) innervates all intrinsic muscles of the larynx EXCEPT the cricothyroid muscle (which is supplied by the external branch of the superior laryngeal nerve). The posterior cricoarytenoid (PCA) is the sole abductor of the vocal cords. When bilateral recurrent laryngeal nerves are transected or severely damaged (as during bilateral thyroid lobectomy), the abductor function is completely lost. The intact cricothyroid muscles (supplied by preserved superior laryngeal nerves) act unopposed to adduct and tense the vocal cords, pulling both cords into the paramedian position. Because both cords cannot abduct during inspiration, severe glottic obstruction and fatal stridor occur, requiring immediate endotracheal intubation or emergency tracheostomy.\n\nOption Review:\n- Option A is correct because bilateral recurrent laryngeal nerve injury paralyzes the posterior cricoarytenoids, fixing the cords in the paramedian position and causing acute stridor.\n- Option B is incorrect because bilateral external laryngeal nerve injury paralyzes the cricothyroids, producing a weak, monotone voice without airway obstruction.\n- Option C is incorrect because internal laryngeal nerve injury causes loss of laryngeal supraglottic sensation, leading to aspiration.\n- Option D is incorrect because the glossopharyngeal nerve does not innervate the vocal cords.\n\nKey Takeaway: Bilateral recurrent laryngeal nerve injury paralyzes vocal cord abductors, causing cords to assume a paramedian position and producing life-threatening respiratory stridor.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q150",
        "subjectId": "ent",
        "subjectTitle": "ENT",
        "topic": "Vestibular Disorders - BPPV & Dix-Hallpike Test",
        "prompt": "A 55-year-old female presents with brief, intense episodes of true vertigo lasting 15 to 30 seconds, triggered whenever she turns her head to the right in bed or looks upward to reach a shelf. The episodes are not accompanied by hearing loss or tinnitus. Dix-Hallpike maneuver to the right triggers torsional, upbeating nystagmus toward the right ear with a 5-second latency. What is the initial, highly effective particle-repositioning maneuver used to treat posterior canal benign paroxysmal positional vertigo?",
        "options": [
            "Epley maneuver",
            "Valsalva maneuver",
            "Pringle maneuver",
            "Jaw-thrust maneuver"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nBenign Paroxysmal Positional Vertigo (BPPV) is the most common cause of peripheral vestibular vertigo. It is caused by canalithiasis: dislodged calcium carbonate crystals (otoconia) from the utricle migrate into one of the semicircular canals, most commonly the posterior semicircular canal (~85-90% of cases) due to gravity. Rapid head movement causes free-floating otoconia to move within the endolymph, deflecting the cupula and triggering acute vertigo lasting <1 minute without auditory symptoms. The diagnostic test of choice is the Dix-Hallpike test (producing latency, geotropic/torsional nystagmus, and fatigability). The definitive bedside treatment is the Epley maneuver (canalith repositioning procedure), which systematically rotates the head through sequential positions to guide otoconia out of the posterior canal back into the utricle.\n\nOption Review:\n- Option A is correct because the Epley maneuver is the definitive canalith repositioning procedure for posterior semicircular canal BPPV.\n- Option B is incorrect because the Valsalva maneuver increases intrathoracic pressure to test middle ear Eustachian tube patency.\n- Option C is incorrect because the Pringle maneuver is surgical clamping of the hepatoduodenal ligament for liver hemorrhage.\n- Option D is incorrect because the jaw-thrust maneuver is an emergency airway opening technique in trauma.\n\nKey Takeaway: Benign Paroxysmal Positional Vertigo (BPPV) of the posterior semicircular canal is diagnosed by the Dix-Hallpike test and treated with the Epley canalith repositioning maneuver.",
        "imageUrls": []
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(QUESTIONS)} questions in Part 1 Block 3.")
    for q in QUESTIONS:
        assert len(q["options"]) == 4, f"{q['id']} does not have 4 options"
        assert 0 <= q["answerIndex"] <= 3, f"{q['id']} invalid answerIndex"
        for opt in q["options"]:
            assert not opt.endswith(";"), f"{q['id']} option ends with semicolon: {opt}"
            assert "(" not in opt or any(c.isdigit() for c in opt), f"{q['id']} option has explanatory bracket: {opt}"
    print("All 50 questions passed structural assertions.")
