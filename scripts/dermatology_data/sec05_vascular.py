from .common import q

CHAPTERS = [
    (20, "Disorders of Blood Vessels and Lymphatics", "easy", [
        q(
            "Which combination of clinical features definitively differentiates a Venous Stasis Ulcer from an Ischemic Arterial Ulcer on the lower extremity?",
            "Medial malleolus location, shallow irregular margins, heavy exudate",
            ["Distal toe location, punched-out borders, absent peripheral pulses", "Severe nocturnal rest pain relieved by leg dependency", "Cold, pale, hairless skin with thickened dystrophic toenails"],
            "Venous stasis ulcers (70-80% of all leg ulcers) arise from ambulatory venous hypertension: located classically in the 'gaiter zone' above the medial malleolus, shallow, irregular borders, moist beefy-red granulation base with copious serous exudate, surrounded by stasis dermatitis and hemosiderin staining, and pain is relieved by leg elevation. In contrast, arterial ulcers occur at pressure points/toes, are deep, punched-out, dry, necrotic, and have rest pain aggravated by elevation.",
            clinical=False
        ),
        q(
            "A 62-year-old female with long-standing bilateral varicose veins presents with progressive induration, brawny woody hardness, and circumferential fibrotic constriction of the lower third of both calves, producing a distinctive 'inverted champagne bottle' or 'bowling pin' contour of the legs. What is this sclerosing panniculitis termed?",
            "Lipodermatosclerosis (sclerosing panniculitis)",
            ["Elephantiasis nostras verrucosa", "Erythema nodosum", "Pretibial myxedema"],
            "Lipodermatosclerosis is a chronic, fibrosing panniculitis resulting from advanced venous hypertension. Chronic capillary leakage of fibrinogen forms pericapillary fibrin cuffs that impede tissue oxygenation, inciting severe subcutaneous fat necrosis and dense septal/lobular fibrosis. The lower calf becomes woody and bound down circumferentially; combined with proximal edema, the leg assumes the characteristic appearance of an inverted champagne bottle or bowling pin.",
            clinical=True
        ),
        q(
            "What critical biological, clinical, and immunohistochemical marker differentiates an Infantile Hemangioma from a Congenital Vascular Malformation?",
            "GLUT-1 positive, post-natal proliferation phase, spontaneous gradual involution",
            ["GLUT-1 negative, present at birth, persists without involution", "High-flow arteriovenous fistulas requiring urgent endovascular embolization", "Regular association with Kasabach-Merritt consumptive coagulopathy"],
            "Infantile hemangiomas are true benign vascular neoplasms of endothelial cells: 1. Absent or a faint telangiectatic macule at birth; 2. Undergo rapid proliferation during infancy (months 1-9); 3. Undergo slow, spontaneous involution over years (50% resolve by age 5, 90% by age 9); 4. Express Glucose Transporter-1 (GLUT-1) in all stages. Conversely, vascular malformations are structural developmental errors (capillary, venous, arteriovenous, lymphatic), GLUT-1 negative, present at birth, grow proportionately with the child, and never involute.",
            clinical=False
        ),
        q(
            "A 24-year-old pregnant female presents with a rapidly growing, solitary, bright red, sessile, fleshy vascular papule with a delicate surrounding collarette of scale on her index finger, which bleeds profusely upon minimal accidental trauma. What is the diagnosis?",
            "Pyogenic granuloma (Lobular capillary hemangioma)",
            ["Amelanotic melanoma", "Bacillary angiomatosis", "Kaposi sarcoma"],
            "Pyogenic granuloma (lobular capillary hemangioma) is a benign, acquired vascular proliferation of capillaries that typically arises on fingers, lips, or gingiva (where it is termed 'granuloma gravidarum' or pregnancy epulis). Despite its historical misnomer, it is neither infectious (pyogenic) nor a true granuloma, but a lobular capillary proliferation in an edematous stroma with a characteristic epithelial collarette, notoriously prone to brisk, recurrent hemorrhage upon trivial contact.",
            clinical=True
        ),
        q(
            "In evaluating a patient with severe, chronic brawny swelling of the lower leg to differentiate true Lymphedema from chronic venous edema, what physical examination sign is considered pathognomonic when positive?",
            "Positive Stemmer sign at base of second toe",
            ["Positive Trendelenburg test with rapid venous refilling", "Ankle-Brachial Index reduced below 0.5", "Positive Buerger test with pallor on elevation"],
            "Stemmer's sign is pathognomonic for lymphedema: The examiner attempts to pinch and lift a fold of skin at the dorsal base of the second toe. In lymphedema, chronic subcutaneous lymphatic fluid accumulation and secondary interstitial fibrosis thicken the dermis and tether it to underlying subcutaneous tissue, making it impossible to pinch or lift the skin fold (positive Stemmer sign). In pure venous edema or lipedema, the skin fold can still be easily pinched and lifted (negative sign).",
            clinical=True
        ),
    ]),
    (21, "Vasculitis and Neutrophilic Disorders", "hard", [
        q(
            "A 28-year-old female presents with multiple, symmetrical, non-blanching, purpuric papules distributed predominantly on the dependent lower extremities and ankles (palpable purpura) 10 days after starting a cephalosporin. Skin biopsy demonstrates post-capillary venular wall fibrinoid necrosis, extravasated erythrocytes, and a dense perivascular infiltrate of neutrophils with fragmented, pyknotic nuclear debris. What is this histological process termed?",
            "Leukocytoclasia (karyorrhexis / nuclear dust) in Leukocytoclastic Vasculitis",
            ["Acantholysis in Pemphigus", "Granulomatous vasculitis in Giant cell arteritis", "Liquefactive necrosis in Lichen planus"],
            "Leukocytoclastic Vasculitis (LCV / hypersensitivity vasculitis / cutaneous small vessel vasculitis) is an immune complex-mediated (Type III) inflammation of post-capillary venules. The primary clinical sign is palpable purpura (non-blanching red-to-purple papules). Histological tetrad: 1. Fibrinoid necrosis of the venular wall; 2. Dense neutrophilic infiltrate; 3. Leukocytoclasia (fragmentation and disintegration of neutrophil nuclei into 'nuclear dust' or karyorrhexis); 4. Extravasation of red blood cells into the dermis.",
            clinical=True
        ),
        q(
            "An 8-year-old boy presents with a dramatic symmetrical eruption of palpable purpura over his buttocks and lower legs, severe colicky abdominal pain with hematochezia, bilateral knee arthralgias, and microscopic hematuria, 2 weeks after an upper respiratory tract infection. What is the diagnosis and its pathognomonic Direct Immunofluorescence (DIF) finding?",
            "IgA vasculitis; granular IgA and C3 in post-capillary venules",
            ["Granulomatosis with polyangiitis; c-ANCA targeting proteinase-3", "Microscopic polyangiitis; p-ANCA targeting myeloperoxidase", "Cryoglobulinemic vasculitis; cold-precipitable IgM rheumatoid factor"],
            "Henoch-Schönlein Purpura (HSP / IgA Vasculitis) is the most common systemic vasculitis of childhood. Classic clinical tetrad: 1. Palpable purpura on dependent areas (buttocks, extensor legs); 2. Arthralgia/arthritis; 3. Gastrointestinal colic / gastrointestinal bleeding (risk of ileocecal intussusception); 4. Glomerulonephritis (IgA nephropathy). Direct immunofluorescence of an early purpuric lesion (<24 hours old) demonstrates pathognomonic granular vascular deposition of IgA and C3.",
            clinical=True
        ),
        q(
            "A 40-year-old female with active Ulcerative Colitis develops a tender, pustular nodule on her pretibial shin. Within 5 days, the pustule rapidly ulcerates, expanding into an agonizingly painful, necrotic ulcer with a distinctive, undermined, ragged, violaceous or gunmetal-blue border and a cribriform purulent base. What is the diagnosis?",
            "Pyoderma gangrenosum",
            ["Ecthyma gangrenosum", "Necrotizing fasciitis", "Venous stasis ulcer"],
            "Pyoderma Gangrenosum (PG) is an uncommon, non-infectious, destructive, inflammatory neutrophilic dermatosis strongly associated with underlying systemic diseases: Inflammatory Bowel Disease (Ulcerative Colitis > Crohn's in 30-50%), seropositive Rheumatoid Arthritis, and monoclonal gammopathies/AML. Hallmark: an initial tender sterile papulopustule that rapidly breaks down into an exquisitely painful ulcer with a characteristic undermined, overhang, violaceous-blue border.",
            clinical=True
        ),
        q(
            "A patient with active Pyoderma Gangrenosum was mistakenly diagnosed with an ordinary bacterial abscess, and the surgeon performed aggressive mechanical surgical debridement of the wound edges. Over the next 48 hours, the ulcer exploded in size, tripling in diameter with catastrophic tissue necrosis. What is this phenomenon termed, and why is surgical debridement strictly contraindicated?",
            "Pathergy phenomenon; surgical debridement triggers rapid ulcer expansion",
            ["Koebner phenomenon; isomorphic plaque induction along incision lines", "Nikolsky sign; mechanical shear dislodging the upper epidermis", "Auspitz sign; pinpoint capillary bleeding upon scale removal"],
            "Pathergy is the development of a sterile pustule or profound exacerbation of ulceration at sites of minimal skin trauma (needle pricks, surgical incisions, mechanical debridement). In Pyoderma Gangrenosum, pathergy occurs in up to 30% of patients. Surgical debridement is strictly contraindicated during the active inflammatory phase because mechanical wounding acts as a potent neutrophilic stimulus, causing rapid, catastrophic enlargement of the ulcer. First-line therapy is medical (high-dose systemic corticosteroids or cyclosporine).",
            clinical=True
        ),
        q(
            "A 48-year-old female presents with acute high fever, malaise, marked peripheral leukocytosis with neutrophilia (WBC 22,000/mcL, 85% neutrophils), elevated ESR/CRP, and the sudden emergence of multiple tender, juicy, mammillated, bright red-to-violaceous plaques with an edematous pseudovesicular surface on her face, neck, and upper limbs. Skin biopsy reveals a massive, dense, band-like infiltrate of mature neutrophils in the upper dermis with severe papillary dermal edema, but ZERO true leukocytoclastic vasculitis. What is the diagnosis?",
            "Sweet syndrome (Acute febrile neutrophilic dermatosis)",
            ["Leukocytoclastic vasculitis", "Erythema multiforme major", "Cellulitis"],
            "Sweet syndrome (Acute Febrile Neutrophilic Dermatosis) is characterized by: 1. Abrupt onset of high fever and leukocytosis with prominent neutrophilia; 2. Tender, edematous, erythematous plaques or nodules with a translucent, 'pseudovesicular' or juicy surface produced by massive papillary dermal edema; 3. Histology: diffuse, dense dermal infiltrate composed predominantly of mature neutrophils with leukocytoclasia, but without fibrinoid necrosis of blood vessels (non-vasculitic).",
            clinical=True
        ),
        q(
            "Which underlying hematological malignancy is most frequently associated with the Malignancy-Associated (Paraneoplastic) variant of Sweet Syndrome, which often presents with atypical bullous or ulcerated cutaneous lesions?",
            "Acute Myeloid Leukemia (AML) and Myelodysplastic Syndromes (MDS)",
            ["Chronic Lymphocytic Leukemia (CLL)", "Hodgkin Lymphoma", "Multiple Myeloma alone"],
            "Up to 15-20% of Sweet syndrome cases are paraneoplastic, of which >85% are linked to hematological disorders, overwhelmingly Acute Myeloid Leukemia (AML, especially M4 and M5 FAB subtypes) and Myelodysplastic Syndromes (MDS). Malignancy-associated Sweet syndrome frequently manifests with atypical, severe bullous, ulcerated, or pyoderma gangrenosum-like lesions on the dorsal hands and face.",
            clinical=False
        ),
        q(
            "A 30-year-old male from the Mediterranean region presents with recurrent, painful, punched-out oral aphthous ulcers occurring at least 4 times per year, recurrent painful genital scrotal ulcers that heal with scars, and bilateral hypopyon uveitis causing blurred vision. When his forearm is pricked with a sterile 20-gauge needle, a sterile pustule surrounded by an erythematous halo develops at the puncture site within 48 hours. What is the diagnosis and the primary HLA association?",
            "Behçet disease; HLA-B*51",
            ["Reactive arthritis; HLA-B*27", "Systemic lupus erythematosus; HLA-DR3", "Ankylosing spondylitis; HLA-B*27"],
            "Behçet disease is a chronic, relapsing, multi-system inflammatory vasculitis. Diagnostic criteria require recurrent oral aphthosis (at least 3 episodes in 12 months) PLUS two of the following: 1. Recurrent genital aphthae (heal with scarring); 2. Eye lesions (anterior hypopyon uveitis, retinal vasculitis); 3. Skin lesions (erythema nodosum, pseudofolliculitis); 4. Positive Pathergy test (sterile erythematous pustule developing 24-48 hours after sterile needle puncture). It is strongly linked to the HLA-B*51 allele (Silk Route distribution).",
            clinical=True
        ),
        q(
            "A 50-year-old male with a history of chronic active Hepatitis B presents with painful subcutaneous nodules along the course of superficial arteries on his legs, livedo reticularis, peripheral foot drop (mononeuritis multiplex), and severe hypertension, without glomerulonephritis or pulmonary involvement. Angiography reveals multiple microaneurysms at the bifurcations of visceral arteries. What is the diagnosis?",
            "Polyarteritis nodosa (PAN)",
            ["Granulomatosis with polyangiitis (GPA)", "Henoch-Schönlein purpura", "Microscopic polyangiitis"],
            "Classic Polyarteritis Nodosa (PAN) is a systemic necrotizing vasculitis targeting medium-sized and small muscular arteries. Hallmarks: subcutaneous nodules along arterial tracks, livedo reticularis, digital gangrene, mononeuritis multiplex (e.g., foot drop), renal renovascular hypertension (due to renal artery involvement), with characteristic SPARING of the lungs and glomerular capillaries. Up to 30% of cases are etiologically associated with Hepatitis B virus (HBV) antigen-antibody immune complexes.",
            clinical=True
        ),
        q(
            "A 46-year-old male presents with recurrent epistaxis, chronic sinusitis, purulent nasal discharge with saddle-nose deformity, hemoptysis, multiple bilateral cavitary pulmonary nodules, and rapidly progressive glomerulonephritis. Cutaneous examination reveals palpable purpura and ulcerative pyoderma gangrenosum-like plaques. What serological antibody marker has extraordinarily high sensitivity and specificity for this condition?",
            "Cytoplasmic anti-neutrophil cytoplasmic antibodies (c-ANCA) targeting Proteinase 3 (PR3)",
            ["Perinuclear anti-neutrophil cytoplasmic antibodies (p-ANCA) targeting Myeloperoxidase (MPO)", "Anti-nuclear antibodies (ANA) targeting double-stranded DNA", "Anti-glomerular basement membrane (anti-GBM) antibodies"],
            "Granulomatosis with Polyangiitis (GPA / historically Wegener's granulomatosis) is a necrotizing granulomatous vasculitis characterized by the classic clinical triad of: 1. Upper respiratory tract involvement (chronic sinusitis, nasal septal perforation, saddle-nose deformity); 2. Lower respiratory tract involvement (cough, cavitary pulmonary nodules); 3. Renal disease (necrotizing crescentic glomerulonephritis). Serum c-ANCA (PR3-ANCA) is positive in >90% of active systemic cases and tracks disease activity.",
            clinical=True
        ),
        q(
            "A 38-year-old male with chronic severe allergic asthma and allergic rhinitis presents with palpable purpura, tender subcutaneous nodules on his elbows, and mononeuritis multiplex. Laboratory testing reveals striking peripheral blood eosinophilia (eosinophils 35% of total WBC; absolute eosinophil count 4500/mcL). Perinuclear ANCA (p-ANCA) directed against Myeloperoxidase (MPO) is positive in 70% of cases. What is the diagnosis?",
            "Eosinophilic Granulomatosis with Polyangiitis (EGPA / Churg-Strauss syndrome)",
            ["Granulomatosis with polyangiitis", "Microscopic polyangiitis", "Hypereosinophilic syndrome alone"],
            "Eosinophilic Granulomatosis with Polyangiitis (EGPA / Churg-Strauss syndrome) is a necrotizing systemic small-to-medium vessel vasculitis defined by three sequential phases: 1. Prodromal allergic phase (severe adult-onset asthma and allergic rhinitis); 2. Eosinophilic tissue-invasive phase (striking peripheral blood eosinophilia >1500/mcL, eosinophilic pneumonia, and gastroenteritis); 3. Vasculitic phase (systemic necrotizing vasculitis with extravascular necrotizing granulomas, palpable purpura, mononeuritis multiplex, and p-ANCA / MPO-ANCA positivity in ~50-70%).",
            clinical=True
        ),
    ]),
]
