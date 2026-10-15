from .common import q

CHAPTERS = [
    (30, "HIV, Skin Manifestations and Management", "easy", [
        q(
            "A 36-year-old HIV-infected male presents with an intensely pruritic, symmetrical eruption of numerous discrete, 2 to 5 mm, firm, hyperpigmented, urticarial papules distributed across the extensor surfaces of his extremities and trunk, without excoriated burrows or web space lesions. What is this dermatosis termed, and of what CD4 threshold is it a recognized clinical marker?",
            "Pruritic Papular Eruption (PPE) of HIV; CD4 count <200 cells/mcL",
            ["Scabies infestation; CD4 count >500 cells/mcL", "Papular urticaria; CD4 count >1000 cells/mcL", "Guttate psoriasis; CD4 count normal"],
            "Pruritic Papular Eruption (PPE) of HIV is one of the most common and characteristic cutaneous manifestations of advanced HIV disease in tropical regions. It presents as intensely pruritic, chronic, symmetric, monomorphic papules on the extensor limbs and trunk. Histology reveals perivascular and perifollicular lymphocytic and eosinophilic infiltrates. PPE serves as an established clinical surrogate marker for severe immunosuppression (CD4 count <200 cells/mcL).",
            clinical=True
        ),
        q(
            "An HIV-seropositive male with a CD4 count of 150 cells/mcL presents with asymptomatic, corrugated, vertically folded, white, plaque-like lesions along the lateral borders of his tongue that CANNOT be scraped or wiped off with a wooden tongue depressor. What is the diagnosis and its viral etiology?",
            "Oral Hairy Leukoplakia (OHL); Epstein-Barr Virus (EBV)",
            ["Oral pseudomembranous candidiasis; Candida albicans", "Oral lichen planus; Hepatitis C virus", "Condyloma acuminatum; HPV type 16"],
            "Oral Hairy Leukoplakia (OHL) is an opportunistic intraepithelial mucocutaneous manifestation of severe HIV immunosuppression (and other immunocompromised states). It is caused by productive, opportunistic replication of the Epstein-Barr Virus (EBV / HHV-4) within lingual epithelial cells. Hallmark: vertically corrugated, white, adherent, non-scrapable plaques strictly localized to the lateral borders of the tongue, differentiating it from oral candidal thrush.",
            clinical=True
        ),
        q(
            "A 40-year-old male with AIDS (CD4 count 45 cells/mcL) presents with fever, night sweats, and multiple rapidly growing, vascular, red-to-violaceous, friable, dome-shaped papules and subcutaneous nodules resembling pyogenic granulomas on his face and limbs. Warthin-Starry silver stain of biopsy tissue demonstrates clusters of tangled, granular, dark silver-staining bacilli in an edematous vascular stroma. What is the diagnosis and organism?",
            "Bacillary angiomatosis; Bartonella henselae (or Bartonella quintana)",
            ["Kaposi sarcoma; Human herpesvirus 8", "Erysipeloid; Erysipelothrix rhusiopathiae", "Pyogenic granuloma; Staphylococcus aureus"],
            "Bacillary angiomatosis is a vascular proliferative zoonosis occurring almost exclusively in severely immunocompromised individuals (CD4 <100 cells/mcL). It is caused by Gram-negative fastidious bacilli: Bartonella henselae (transmitted by domestic cat scratches or cat fleas) or Bartonella quintana (transmitted by the human body louse). Warthin-Starry silver stain or Steiner stain reveals clumps of purple-black bacilli. Oral Erythromycin or Doxycycline is the definitive treatment.",
            clinical=True
        ),
        q(
            "A 32-year-old HIV-infected male presents with an intensely pruritic, recurring eruption of sterile, dome-shaped, follicular papules and pustules across the face, neck, and upper chest, with prominent absolute peripheral eosinophilia. Biopsy demonstrates a dense eosinophilic infiltrate centered on the sebaceous gland and follicular infundibulum. What is the diagnosis?",
            "Eosinophilic pustular folliculitis (HIV-associated Ofuji disease)",
            ["Bacterial folliculitis", "Pityrosporum folliculitis", "Demodex folliculitis"],
            "HIV-associated Eosinophilic Pustular Folliculitis (EPF / Ofuji-like disease) is an intensely pruritic dermatosis occurring typically when CD4 counts fall below 250-300 cells/mcL. Hallmarks: urticarial follicular papules and sterile pustules favoring the face, neck, and upper trunk, accompanied by prominent blood and tissue eosinophilia. Treatment involves initiation of Antiretroviral Therapy (ART), high-potency topical corticosteroids, oral indomethacin, or phototherapy (UVB).",
            clinical=True
        ),
        q(
            "A 38-year-old HIV-infected male with a baseline CD4 count of 35 cells/mcL begins combination Antiretroviral Therapy (ART). Four weeks later, while his viral load plummets and his CD4 count surges to 220 cells/mcL, he suddenly develops an explosive, severe, necrotic, multi-dermatomal eruption of Herpes Zoster and severe worsening of previously stable Kaposi Sarcoma lesions. What immunological phenomenon explains this paradoxical deterioration?",
            "Immune Reconstitution Inflammatory Syndrome (IRIS)",
            ["Antiretroviral drug hypersensitivity syndrome (DRESS)", "Secondary treatment failure due to viral resistance", "Acute retroviral seroconversion syndrome"],
            "Immune Reconstitution Inflammatory Syndrome (IRIS) is an exuberant, dysregulated inflammatory reaction occurring in 10-25% of HIV patients initiating effective ART. Rapid quantitative recovery of CD4+ T-lymphocytes and antigen-specific memory immunity restores the host's capacity to mount intense inflammatory attacks against preexisting, subclinical, or occult infectious pathogens (such as VZV, mycobacteria, CMV, Cryptococcus, or HHV-8). ART should be continued while managing the infection.",
            clinical=True
        ),
    ]),
    (31, "Sexually Transmitted Infections", "hard", [
        q(
            "A 26-year-old male presents with a solitary, painless, indurated ulcer on the coronal sulcus of his penis that developed 3 weeks after unprotected intercourse. On examination, the ulcer has clean, sharply defined, elevated margins, a red serous base, cartilage-like indurated margins, and is accompanied by bilateral, painless, rubbery, discrete, non-matted inguinal lymphadenopathy. Darkfield microscopy of ulcer exudate demonstrates motile, slender, corkscrew-shaped spirochetes. What is the diagnosis?",
            "Primary syphilis (Hard chancre / Hunterian chancre)",
            ["Chancroid (soft sore)", "Herpes genitalis", "Donovanosis"],
            "The hard chancre (Hunterian chancre) of Primary Syphilis is caused by Treponema pallidum subsp. pallidum (incubation period 9-90 days, average 21 days). Cardinal hallmarks: 1. Usually solitary; 2. Exquisitely PAINLESS; 3. Pronounced cartilage-like ('button-like') induration at the base and margins; 4. Clean, beefy-red base discharging clear serous fluid; 5. Accompanied by bilateral, painless, discrete, firm, non-suppurative inguinal lymphadenopathy ('shotty nodes').",
            clinical=True
        ),
        q(
            "A 28-year-old male presents with a non-pruritic, generalized, symmetrical eruption of copper-colored, ham-colored macules and scaly papules prominently involving the palms and soles, each surrounded by a delicate collarette of scale (Biett's collarette). Examination of the perianal area reveals flat, moist, broad-based, highly infectious hypertrophic plaques. What is the diagnosis, and what are the perianal plaques termed?",
            "Secondary syphilis; Condylomata lata",
            ["Condylomata acuminata; HPV infection", "Plaque psoriasis; Inverse psoriasis", "Lichen planus; Wickham striae"],
            "Secondary Syphilis develops 4 to 10 weeks after the primary chancre, caused by systemic treponemal bacteremia. Cutaneous hallmarks: 1. Non-pruritic, ham-colored or coppery papulosquamous eruption typically involving the PALMS and SOLES, with a pathognomonic peripheral fringe of scale (Biett's sign); 2. Condylomata lata: soft, flat-topped, moist, velvety, grayish-white hypertrophic papules in warm intertriginous folds (anogenital region) that teem with infectious spirochetes; 3. 'Moth-eaten' non-scarring alopecia.",
            clinical=True
        ),
        q(
            "A 50-year-old male with untreated syphilis for 15 years presents with a solitary, painless, deep-seated subcutaneous nodule on his upper leg that slowly broke down to form a chronic, punched-out ulcer with vertical borders and a central, adherent, yellowish-gray necrotic slough resembling 'wash-leather'. Biopsy demonstrates endarteritis obliterans and granulomas. What is this tertiary syphilitic lesion termed?",
            "Syphilitic gumma (Gummatous syphilis)",
            ["Hard chancre", "Condyloma latum", "Charcot joint"],
            "A gumma is the hallmark lesion of Tertiary (Late Benign) Syphilis. It begins in the dermis, subcutaneous tissue, or bone as a painless, rubbery granulomatous nodule that undergoes ischemic central necrosis, ulcerating into a characteristic 'punched-out' ulcer with punched-out vertical margins and a pathognomonic, tough, adherent, yellowish necrotic base likened to 'wash-leather'. Gummas contain very few spirochetes, representing a delayed-type hypersensitivity reaction.",
            clinical=True
        ),
        q(
            "What is the first-line, gold-standard antimicrobial regimen of choice for an adult diagnosed with early syphilis (primary, secondary, or early latent of less than one year duration)?",
            "Benzathine Penicillin G 2.4 million units IM single dose",
            ["Procaine Penicillin 1.2 million units IM daily for 30 days", "Oral Doxycycline 100 mg twice daily for 3 days", "Oral Azithromycin 500 mg single dose"],
            "Benzathine Penicillin G (2.4 million units IM administered as a single dose, often divided into two 1.2 million unit injections in each buttock) is the definitive, globally established treatment of choice for primary, secondary, and early latent syphilis (<1 year duration). Penicillin maintains treponemicidal serum levels (>0.03 mcg/mL) for over 2 to 3 weeks, eradicating the slowly dividing spirochetes.",
            clinical=False
        ),
        q(
            "A patient receiving his first intramuscular injection of Benzathine Penicillin G for secondary syphilis suddenly develops shaking rigors, high fever (39.5 C), headache, tachycardia, flushing, and transient accentuation of his cutaneous rash 4 hours after the injection. What is this acute reaction, and what is its appropriate management?",
            "Jarisch-Herxheimer reaction; manage supportively without stopping penicillin",
            ["Type I anaphylactic IgE reaction; administer immediate intramuscular epinephrine", "Serum sickness; administer high-dose systemic steroids", "Toxic epidermal necrolysis; discontinue penicillin permanently"],
            "The Jarisch-Herxheimer Reaction is an acute, benign, self-limiting systemic reaction occurring in up to 50-75% of patients with early syphilis within 2 to 12 hours of initiating antimicrobial therapy (most commonly penicillin). Massive lysis of treponemes releases massive quantities of lipoproteins, endotoxins, and inflammatory cytokines (TNF-alpha, IL-6, IL-8). It is NOT an allergic drug reaction: management consists of reassurance, bed rest, and antipyretics (paracetamol), and penicillin must NEVER be discontinued.",
            clinical=True
        ),
        q(
            "A 24-year-old male presents with four excruciatingly painful, soft, non-indurated, deep ulcers on his prepuce with ragged, undermined, irregular borders and a necrotic, purulent, foul-smelling yellow-gray base. Two days later, a painful, fluctuant, inflammatory unilateral inguinal lymph node (bubo) develops, threatening to rupture spontaneously through a single sinus. Gram stain of the ulcer exudate reveals Gram-negative coccobacilli arranged in parallel chains resembling a 'school of fish' or 'railroad tracks'. What is the diagnosis?",
            "Chancroid (Soft sore); Haemophilus ducreyi",
            ["Primary syphilis; Treponema pallidum", "Lymphogranuloma venereum; Chlamydia trachomatis", "Donovanosis; Klebsiella granulomatis"],
            "Chancroid is an acute, sexually transmitted ulcerative infection caused by Haemophilus ducreyi (a fastidious Gram-negative coccobacillus). Cardinal distinguishing features from primary syphilis: 1. Multiple, soft, NON-INDURATED ulcers ('soft sore'); 2. Exquisitely PAINFUL; 3. Ragged, undermined margins with foul-smelling purulent base; 4. Unilateral, painful, suppurative bubo that characteristically uniloculates and ruptures through a SINGLE sinus; 5. Gram stain shows 'school-of-fish' or 'railroad-track' morphology.",
            clinical=True
        ),
        q(
            "A 30-year-old male presents with massive, painful, matted inguinal and femoral lymphadenopathy in his right groin that is visibly divided into upper and lower groups by Poupart's inguinal ligament, producing the pathognomonic 'Groove sign of Greenblatt'. The buboes become multilocular and discharge purulent fluid through multiple sinus tracts. History reveals an evanescent, painless herpetiform papule on his coronal sulcus that healed spontaneously 3 weeks ago. What is the diagnosis and organism?",
            "Lymphogranuloma Venereum (LGV); Chlamydia trachomatis serovars L1, L2, and L3",
            ["Chancroid; Haemophilus ducreyi", "Primary syphilis; Treponema pallidum", "Donovanosis; Klebsiella granulomatis"],
            "Lymphogranuloma Venereum (LGV) is an invasive systemic STI caused by the lymphotropic serovars L1, L2, and L3 of Chlamydia trachomatis. Stages: Primary stage: a small, painless, transient, non-indurated papule/erosion that heals rapidly; Secondary stage (2-6 weeks later): acute suppurative lymphadenitis (buboes) of inguinal and femoral nodes separated by the inguinal ligament, producing the pathognomonic 'Groove sign of Greenblatt', discharging through MULTIPLE fistulous sinus tracts ('watering-can groin').",
            clinical=True
        ),
        q(
            "A 32-year-old male presents with a slowly spreading, painless, beefy-red, velvety, exuberant, granulomatous, friable ulcer with elevated, rolled, everted margins on his penile shaft and scrotum that bleeds copiously upon touch. There is total ABSENCE of true regional lymphadenopathy, though fluctuant subcutaneous granulomas ('pseudobuboes') are palpable in the groin. Giemsa stain of a tissue crush preparation reveals large mononuclear histiocytes stuffed with diagnostic, closed safety-pin-shaped, bipolar-staining intracellular bacilli. What is the diagnosis?",
            "Donovanosis (Granuloma Inguinale); Klebsiella granulomatis (Donovan bodies)",
            ["Primary syphilis; Treponema pallidum", "Chancroid; Haemophilus ducreyi", "Squamous cell carcinoma of penis"],
            "Donovanosis (Granuloma Inguinale) is a chronic, progressively destructive STI caused by the intracellular Gram-negative bacillus Klebsiella granulomatis. Cardinal hallmarks: 1. PAINLESS, beefy-red, friable, velvety, exuberant granulomatous ulcer that bleeds readily; 2. Complete absence of true inguinal lymphadenopathy (true buboes do not occur; instead, subcutaneous granulomas in the groin form 'pseudobuboes'); 3. Diagnostic Giemsa/Wright stain demonstration of 'Donovan bodies' (safety-pin-shaped bacilli in large histiocytes).",
            clinical=True
        ),
        q(
            "A 22-year-old sexually active female presents with sudden onset of severe vulvar pain, burning upon micturition, fever, and bilateral tender inguinal lymphadenopathy. Examination reveals crops of tiny, clustered, thin-walled vesicles on an erythematous base across both labia majora that rapidly rupture into exquisitely tender, shallow, polycyclic, punched-out erosions. Tzanck smear demonstrates multinucleated giant cells with nuclear molding. What is the diagnosis?",
            "Primary genital herpes; herpes simplex virus type 2",
            ["Primary syphilis", "Chancroid", "Behçet disease"],
            "Genital herpes is the most common cause of genital ulcer disease worldwide, caused predominantly by HSV-2 (and increasingly HSV-1). Primary genital herpes presents 2-14 days post-exposure with severe pain, dysuria, systemic fever, and crops of grouped vesicles on an erythematous base that erode into painful, scalloped, shallow ulcers with crusting and tender bilateral adenopathy. Episodes recur due to viral latency within sacral dorsal root ganglia.",
            clinical=True
        ),
        q(
            "Which clinical diagnostic summary correctly differentiates the five classical causes of Genital Ulcer Disease (GUD)?",
            "Syphilis: indurated/painless; Chancroid: purulent/painful; Donovanosis: beefy-red; LGV: groove sign",
            ["Syphilis: painful multiple pustules; Chancroid: painless indurated; Donovanosis: purulent; LGV: vesicles", "Syphilis: beefy-red pseudobuboes; Chancroid: painless erosion; Donovanosis: vesicles; LGV: soft chancre", "Syphilis: groove sign; Chancroid: shotty painless nodes; Donovanosis: single bubo; LGV: gumma"],
            "Key diagnostic algorithm for Genital Ulcer Disease (GUD): 1. Primary Syphilis: Solitary, PAINLESS, hard indurated ulcer with clean base + non-tender rubbery nodes; 2. Chancroid: Multiple, PAINFUL, soft non-indurated ulcers with purulent base + painful unilocular bubo; 3. Donovanosis: PAINLESS, beefy-red, velvety, exuberant granulating ulcer + pseudobuboes (no true lymphadenopathy); 4. LGV: Small painless transient erosion + painful multilocular matted nodes with Groove sign; 5. Genital Herpes: Multiple PAINFUL grouped vesicles/erosions on red base.",
            clinical=False
        ),
    ]),
]
