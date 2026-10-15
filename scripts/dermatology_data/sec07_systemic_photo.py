from .common import q

CHAPTERS = [
    (26, "Collagen Vascular Disorders", "hard", [
        q(
            "Which anatomical landmark feature definitively distinguishes the classic acute Malar 'Butterfly' Rash of Systemic Lupus Erythematosus (SLE) from the facial eruptions of Rosacea and Seborrheic Dermatitis?",
            "Strict sparing of the nasolabial folds",
            ["Involvement of the upper eyelids with violaceous edema", "Presence of central comedones and purulent pustules", "Greasy, yellowish scales confined to the eyebrows"],
            "The classic acute cutaneous lupus erythematous rash is the malar ('butterfly') rash: an erythematous, edematous plaque distributed symmetrically across the bridge of the nose and both malar eminences. Its cardinal, pathognomonic diagnostic feature is the strict SPARING of the nasolabial folds (due to anatomical shadowing from UV light). In contrast, seborrheic dermatitis and rosacea characteristically involve the nasolabial folds.",
            clinical=False
        ),
        q(
            "A 36-year-old male presents with chronic, scarring, well-demarcated, coin-shaped erythematous plaques on his scalp and face with adherent hyperkeratotic scales. When the scale is peeled back, small horny keratotic plugs are seen projecting from the undersurface, corresponding to patent follicular orifices ('carpet-tack sign' / tin-tack sign). As lesions resolve, they produce permanent cicatricial alopecia and depigmentation. What is the diagnosis?",
            "Discoid lupus erythematosus (DLE)",
            ["Psoriasis vulgaris", "Lichen planus", "Seborrheic dermatitis"],
            "Discoid Lupus Erythematosus (DLE) is the most common form of chronic cutaneous lupus erythematosus. Triad of progression: 1. Inflammatory active erythema with adherent hyperkeratotic scale; 2. Follicular plugging (carpet-tack or tin-tack sign, where keratotic spicules project from the underside of peeled scale); 3. End-stage central atrophic scarring, telangiectasia, follicular obliteration (permanent cicatricial alopecia), and hyperpigmented margins with central depigmentation.",
            clinical=True
        ),
        q(
            "A 30-year-old female presents with a non-scarring, non-indurated, widespread annular and polycyclic erythematous eruption over her shoulders, upper back, and V-neck area triggered by sun exposure. Serological evaluation demonstrates high-titer anti-Ro/SSA antibodies. What variant of cutaneous lupus is this, and what fetal complication is associated if she becomes pregnant?",
            "Subacute cutaneous lupus erythematosus (SCLE); complete congenital fetal heart block",
            ["Systemic sclerosis; fetal limb reduction defects", "Discoid lupus erythematosus; fetal hydrocephalus", "Lupus profundus; neonatal polycystic kidney disease"],
            "Subacute Cutaneous Lupus Erythematosus (SCLE) presents with non-scarring annular/polycyclic or papulosquamous plaques on sun-exposed upper trunk and arms. It is extraordinarily linked to anti-Ro/SSA antibodies (>80%) and HLA-DR3. Transplacental crossing of maternal anti-Ro/SSA and anti-La/SSB IgG antibodies between weeks 16-24 of gestation can attack the fetal cardiac conduction system, producing irreversible congenital complete heart block (Neonatal Lupus Erythematosus).",
            clinical=True
        ),
        q(
            "What critical diagnostic and prognostic distinction is established by the 'Lupus Band Test' on Direct Immunofluorescence (DIF)?",
            "Granular band in normal sun-protected skin confirms systemic lupus",
            ["Band positivity in oral mucosa confirms Behçet disease", "Linear band of IgA along the basement membrane confirms Pemphigus", "Deposition of IgE along dermal papillae confirms Atopic dermatitis"],
            "The Lupus Band Test (LBT) is Direct Immunofluorescence demonstrating a continuous, granular band of immunoglobulins (IgG, IgM) and complement (C3) along the basement membrane zone: 1. Positive in LESIONAL skin: seen in >90% of Discoid Lupus (DLE) and SLE; 2. Positive in SUN-EXPOSED normal-appearing skin: suggests lupus; 3. Positive in NON-LESIONAL, SUN-PROTECTED skin (e.g., inner arm or buttocks): highly specific for active, severe Systemic Lupus Erythematosus (SLE) with high risk of lupus nephritis.",
            clinical=False
        ),
        q(
            "A 46-year-old female presents with symmetrical proximal muscle weakness, difficulty climbing stairs, and a violaceous, dusky-erythematous periorbital edema involving both upper eyelids ('heliotrope rash'). Physical examination of the hands reveals pathognomonic violaceous, flat-topped, lichenoid papules and plaques overlying the dorsal aspect of the metacarpophalangeal (MCP) and interphalangeal (IP) joints. What are these joint papules termed, and what is the diagnosis?",
            "Gottron papules; Dermatomyositis",
            ["Heberden nodes; Osteoarthritis", "Bouchard nodes; Rheumatoid arthritis", "Osler nodes; Infective endocarditis"],
            "Dermatomyositis is an idiopathic autoimmune inflammatory myopathy with distinct cutaneous features. Gottron papules are pathognomonic: violaceous, flat-topped lichenoid papules symmetrically overlying the dorsal MCP, PIP, and DIP joints (in contrast to SLE, which preferentially targets the interphalangeal spaces between joints, SPARING the knuckles). The Heliotrope rash (violaceous periorbital edema resembling the heliotrope flower) is also pathognomonic.",
            clinical=True
        ),
        q(
            "A 52-year-old female presents with clinically amyopathic dermatomyositis, rapidly progressive fatal interstitial lung disease (RP-ILD), and painful, refractory cutaneous vasculitic ulcers over the digital pulp and palmar creases. Which specific myositis-specific autoantibody is strongly linked to this lethal phenotype?",
            "Anti-MDA5 (Melanoma Differentiation-Associated Gene 5) antibody",
            ["Anti-Mi-2 antibody", "Anti-TIF1-gamma antibody", "Anti-Jo-1 antibody"],
            "Anti-MDA5 (melanoma differentiation-associated protein 5) autoantibodies define a clinically distinct and aggressive subgroup of dermatomyositis, characterized by: 1. Little or no muscle weakness (clinically amyopathic dermatomyositis - CADM); 2. Painful cutaneous ulcerations (digital pulp, knuckles, elbows); 3. Palmar violaceous papules; 4. High incidence of rapidly progressive, treatment-resistant interstitial lung disease (RP-ILD) with a catastrophic 6-month mortality rate.",
            clinical=True
        ),
        q(
            "A 45-year-old female presents with cold-induced triphasic color changes of her fingers (white to blue to red), sclerodactyly with skin bound down to underlying tissue, beaked facies with microstomia and radial furrowing around the lips, telangiectasias on her face, and subcutaneous calcific nodules over her elbows. Systemic workup confirms the CREST syndrome variant of Limited Systemic Sclerosis. Which circulating autoantibody is highly specific for this limited cutaneous form?",
            "Anti-Centromere antibodies (ACA)",
            ["Anti-Scl-70 (anti-topoisomerase I) antibodies", "Anti-RNA polymerase III antibodies", "Anti-dsDNA antibodies"],
            "CREST syndrome is the classic clinical manifestation of Limited Cutaneous Systemic Sclerosis (lcSSc): Calcinosis cutis, Raynaud's phenomenon, Esophageal dysmotility, Sclerodactyly, and Telangiectasia. Skin thickening is restricted to the face and distal extremities below the elbows and knees. Anti-Centromere Antibodies (ACA) are positive in >70-80% of patients with limited disease (predicting isolated pulmonary arterial hypertension), whereas Anti-Scl-70 associates with Diffuse cutaneous systemic sclerosis.",
            clinical=True
        ),
        q(
            "A 50-year-old male with Diffuse Cutaneous Systemic Sclerosis (dcSSc) positive for Anti-RNA Polymerase III antibodies is treated with high-dose systemic oral Prednisolone (40 mg/day) for severe inflammatory joint pain. Within 3 weeks, he develops acute malignant hypertension (BP 220/120 mmHg), encephalopathy, and oliguric acute renal failure with microangiopathic hemolytic anemia. What catastrophic iatrogenic complication has been triggered?",
            "Scleroderma Renal Crisis (SRC)",
            ["Lupus nephritis class IV", "Goodpasture syndrome", "Acute tubular necrosis"],
            "Scleroderma Renal Crisis (SRC) occurs in 10-15% of patients with diffuse systemic sclerosis, characterized by acute abrupt malignant hypertension, oliguric acute kidney injury, and microangiopathic hemolytic anemia. High-dose corticosteroids (>15 mg/day of prednisone) and anti-RNA polymerase III antibodies are the two strongest recognized risk factors precipitating SRC. ACE inhibitors (specifically captopril) are the life-saving treatment of choice.",
            clinical=True
        ),
        q(
            "A 9-year-old girl presents with a solitary, linear, indurated, ivory-white, scar-like sclerotic band extending vertically down her forehead and frontoparietal scalp, with underlying localized depression and permanent loss of hair along the band ('en coup de sabre'). What is the diagnosis?",
            "Linear morphea (en coup de sabre)",
            ["Plaque morphea", "Parry-Romberg syndrome alone", "Systemic sclerosis"],
            "Morphea (localized scleroderma) is characterized by sclerosis confined to the skin and subcutaneous tissue without internal organ involvement or Raynaud's phenomenon. Linear Morphea 'en coup de sabre' (resembling the blow of a sabre or sword) typically arises in children on the frontoparietal scalp and paramedian forehead, presenting as an indurated gutter-like groove with cicatricial alopecia, which may be associated with hemifacial atrophy (Parry-Romberg syndrome).",
            clinical=True
        ),
        q(
            "A 32-year-old female presents with severe Raynaud's phenomenon, swollen 'puffy' hands with tapering sausage digits, proximal muscle weakness, and polyarthritis, demonstrating overlapping features of SLE, systemic sclerosis, and polymyositis. Serum antinuclear antibody (ANA) shows a high-titer speckled pattern. Which specific autoantibody is pathognomonic for Mixed Connective Tissue Disease (MCTD)?",
            "High-titer anti-U1-ribonucleoprotein (anti-U1 RNP) antibodies",
            ["Anti-Smith (anti-Sm) antibodies", "Anti-Ro/SSA antibodies", "Anti-Jo-1 antibodies"],
            "Mixed Connective Tissue Disease (MCTD / Sharp syndrome) is an overlap connective tissue disorder combining clinical hallmarks of systemic lupus erythematosus, systemic sclerosis, and polymyositis/dermatomyositis. The hallmark serological requirement in all diagnostic criteria sets (Alarcón-Segovia, Kasukawa) is the presence of high-titer circulating antibodies directed against U1 small nuclear ribonucleoprotein (U1-RNP), usually in the absence of anti-dsDNA and anti-Sm antibodies.",
            clinical=True
        ),
    ]),
    (27, "Skin in Systemic Disease", "easy", [
        q(
            "A 24-year-old obese male presents with symmetrical, velvety, papillomatous, hyperpigmented, brown-black plaques on the posterior and lateral folds of his neck, axillae, and groins. Skin tags (acrochordons) are scattered throughout the plaques. What is the diagnosis and its primary endocrine pathophysiology?",
            "Acanthosis nigricans; hyperinsulinemia stimulating IGF-1 receptors on keratinocytes",
            ["Hemochromatosis; iron overload stimulating tyrosinase in epidermal basal cells", "Addison disease; ACTH stimulating melanocortin-1 receptors directly", "Cushing disease; excess cortisol inducing epidermal thinning and lipid synthesis"],
            "Acanthosis nigricans is characterized by hyperpigmented, velvety, verrucous plaques in intertriginous skin folds (posterior neck, axillae). In benign forms (associated with obesity, Type 2 diabetes mellitus, insulin resistance, and PCOS), severe hyperinsulinemia leads to supra-physiological insulin concentrations that cross-react with and activate Insulin-like Growth Factor-1 (IGF-1) receptors on epidermal keratinocytes and dermal fibroblasts, stimulating excessive proliferation.",
            clinical=True
        ),
        q(
            "A 38-year-old female with long-standing Type 1 Diabetes Mellitus presents with multiple, shiny, well-demarcated, atrophic, waxy yellowish-brown plaques with prominent surface telangiectasias and violaceous borders on the anterior pretibial shins. Skin biopsy reveals palisading granulomas surrounding degenerated collagen ('necrobiosis') arranged in horizontal parallel tiers throughout the full dermis ('sandwich pattern'). What is the diagnosis?",
            "Necrobiosis lipoidica (diabeticorum)",
            ["Granuloma annulare", "Pretibial myxedema", "Xanthoma disseminatum"],
            "Necrobiosis Lipoidica (NL / NLD) is a chronic granulomatous disorder occurring in 0.3-1.2% of diabetic patients, with a 3:1 female predominance. Hallmarks: yellow-brown, waxy, atrophic pretibial plaques where the epidermis thins to allow dermal blood vessels to shine through as prominent telangiectasias. Classic histopathology: alternating horizontal tiers of granulomatous inflammation and degenerated collagen necrosis (necrobiosis) extending from the superficial dermis into the subcutis.",
            clinical=True
        ),
        q(
            "A 42-year-old male with severe familial hypertriglyceridemia presents with the explosive, sudden eruption of crops of small (1 to 4 mm), dome-shaped, firm, yellowish-orange papules surrounded by an inflammatory erythematous halo over his buttocks, shoulders, and extensor surfaces of his arms. Serum triglycerides are measured at 2400 mg/dL. What type of xanthoma is this, and what acute medical complication is he at imminent risk of developing?",
            "Eruptive xanthomas; acute necrotizing pancreatitis",
            ["Tendon xanthomas; aortic dissection", "Tuberous xanthomas; acute stroke", "Plane xanthomas; hepatic failure"],
            "Eruptive xanthomas are cutaneous hallmarks of severe chylomicronemia and hypertriglyceridemia (serum triglycerides typically >1000 to 2000 mg/dL; Fredrickson Types I, IV, and V). They present as crops of tiny, tender, yellow-orange papules on an erythematous base on the buttocks, thighs, and extensor limbs. The presence of eruptive xanthomas signals an imminent, life-threatening risk of Acute Pancreatitis, mandating immediate dietary fat restriction and lipid-lowering therapy.",
            clinical=True
        ),
        q(
            "A 45-year-old female with severe Graves' ophthalmopathy presents with bilateral, non-pitting, indurated, shiny, purplish-brown plaques and nodules with prominent follicular orifices resembling an 'orange peel' (peau d'orange) on her anterior lower legs and dorsa of feet. What is the diagnosis, and what glycosaminoglycan is massively deposited within the reticular dermis?",
            "Pretibial myxedema (Thyroid dermopathy); Hyaluronic acid (and chondroitin sulfate)",
            ["Scleromyxedema; Amyloid light-chain protein", "Erythema nodosum; Fibrinogen", "Lipodermatosclerosis; Collagen Type III"],
            "Pretibial myxedema (thyroid dermopathy) occurs in 1-5% of patients with Graves' disease, almost always in the presence of severe exophthalmos and high-titer TSH-receptor autoantibodies (TRAb). Stimulated by TRAb, orbital and pretibial dermal fibroblasts proliferate and synthesize colossal amounts of hydrophilic glycosaminoglycans (predominantly hyaluronic acid). The mucin accumulates in the reticular dermis, producing woody, non-pitting, peau d'orange plaques on the pretibial shins.",
            clinical=True
        ),
        q(
            "A 7-year-old boy fulfills the National Institutes of Health (NIH) consensus diagnostic criteria for Neurofibromatosis Type 1 (NF1 / von Recklinghausen disease). Which specific constellation of cutaneous and ocular signs fulfills these criteria?",
            "≥6 café-au-lait macules, Crowe sign, neurofibromas, Lisch nodules",
            ["Three café-au-lait macules, facial angiofibromas, and shagreen patch", "Ash-leaf macules, periungual fibromas, optic glioma, and hypopigmented streaks", "Port-wine stain, facial asymmetry, glaucoma, and leptomeningeal angioma"],
            "NIH diagnostic criteria for NF1 require >=2 of the following 7 features: 1. >=6 Café-au-lait macules (>5 mm in prepubertal; >15 mm in postpubertal individuals); 2. >=2 Neurofibromas of any type or 1 plexiform neurofibroma; 3. Crowe sign: axillary or inguinal intertriginous freckling; 4. Optic pathway glioma; 5. >=2 Lisch nodules (melanocytic iris hamartomas on slit-lamp); 6. Distinctive osseous lesion (sphenoid dysplasia or anterolateral bowing/pseudarthrosis of tibia); 7. First-degree relative with NF1.",
            clinical=False
        ),
    ]),
    (28, "Genetic Disorders of Skin", "easy", [
        q(
            "A 14-year-old boy presents with dry, rough skin with fine, polygonal, light gray-to-brown adherent scales on his extensor extremities and back, which began during early infancy. Physical examination demonstrates striking, absolute SPARING of the flexural creases (antecubital and popliteal fossae), hyperlinear palms and soles, and keratosis pilaris on his arms. What is the diagnosis and its inheritance pattern?",
            "Ichthyosis vulgaris; Autosomal semidominant (Filaggrin gene mutation)",
            ["X-linked recessive ichthyosis; X-linked recessive (Steroid sulfatase deficiency)", "Lamellar ichthyosis; Autosomal recessive (TGM1 mutation)", "Epidermolytic hyperkeratosis; Autosomal dominant (K1/K10 mutation)"],
            "Ichthyosis vulgaris is the most common disorder of cornification (1 in 250 individuals), inherited in an autosomal semidominant pattern with incomplete penetrance, caused by loss-of-function mutations in the Filaggrin (FLG) gene on chromosome 1q21. Hallmark: fine, polygonal, white-to-gray scales with free edges on extensor surfaces with classic, strict SPARING of flexural creases (antecubital, popliteal, axillary vaults), associated with palmar hyperlinearity, keratosis pilaris, and atopy.",
            clinical=True
        ),
        q(
            "A 12-year-old boy presents with prominent, generalized, thick, dark brown, adherent, polygonal scales over his neck, trunk, and extensor limbs, giving a distinctive 'dirty neck' appearance. The flexural creases are involved, but palms and soles are normal. Corneal examination reveals asymptomatic deep comma-shaped stromal opacities. His mother had an obstetric history of failure of labor progression requiring cesarean delivery. What is the diagnosis and enzymatic deficiency?",
            "X-linked recessive ichthyosis; Steroid sulfatase (arylsulfatase C) deficiency",
            ["Ichthyosis vulgaris; Filaggrin deficiency", "Harlequin ichthyosis; ABCA12 deficiency", "Netherton syndrome; SPINK5 deficiency"],
            "X-linked Recessive Ichthyosis (XLI) affects 1 in 6000 males, caused by deletions or mutations in the STS gene encoding Steroid Sulfatase (arylsulfatase C). Deficiency leads to cholesterol sulfate accumulation in the stratum corneum, inhibiting desquamation. Hallmarks: prominent, dirty-brown, large adherent scales ('dirty neck' sign); asymptomatic deep comma-shaped stromal corneal opacities; cryptorchidism in 20%; and maternal failure of labor progression due to placental steroid sulfatase deficiency.",
            clinical=True
        ),
        q(
            "What is the precise ultrastructural cleavage level and molecular target in Recessive Dystrophic Epidermolysis Bullosa (Hallopeau-Siemens type), an agonizing mechanobullous genodermatosis characterized by severe mucosal strictures, pseudosyndactyly ('mitten-hand' deformities), and aggressive Squamous Cell Carcinoma?",
            "Sublamina densa split with absent type VII collagen fibrils",
            ["Intraepidermal basal cell cytolysis; Keratin 14 gene mutation", "Intra-lamina lucida split; Laminin-332 gene mutation", "Subcorneal granular cell split; Desmoglein 1 mutation"],
            "Recessive Dystrophic Epidermolysis Bullosa (RDEB, Hallopeau-Siemens) is caused by biallelic null mutations in the COL7A1 gene encoding Type VII collagen, the primary component of anchoring fibrils that secure the lamina densa to the papillary dermis. Complete loss of anchoring fibrils results in blister cleavage in the SUBLAMINA DENSA zone below the basement membrane. Blisters heal with relentless, mutilating dermal fibrosis, leading to fusion of digits ('mitten hands'), microstomia, esophageal webs, and fatal metastatic SCC.",
            clinical=False
        ),
        q(
            "A 3-year-old child presents with multiple ash-leaf-shaped hypopigmented macules on the trunk visualized under Wood's lamp, facial angiofibromas across the malar area, and infantile spasms with cortical tubers on brain MRI. What autosomal dominant neurocutaneous syndrome is this, and which tumor suppressor genes are mutated?",
            "Tuberous Sclerosis Complex (Bourneville disease); TSC1 and TSC2 genes",
            ["Neurofibromatosis type 1; NF1 gene", "Sturge-Weber syndrome; GNAQ gene", "Incontinentia pigmenti; NEMO gene"],
            "Tuberous Sclerosis Complex (TSC / epiloia) is an autosomal dominant hamartomatous multi-organ phakomatosis caused by mutations in TSC1 (chromosome 9q34, encoding Hamartin) or TSC2 (chromosome 16p13, encoding Tuberin), which form a complex that normally inhibits the mTOR pathway. Cutaneous hallmarks: 1. Ash-leaf hypomelanotic macules (earliest sign, present at birth); 2. Facial angiofibromas (adenoma sebaceum, appearing at 3-5 years); 3. Shagreen patch (connective tissue nevus); 4. Periungual fibromas (Koenen tumors).",
            clinical=True
        ),
        q(
            "An 8-year-old girl born to consanguineous parents presents with extreme solar sensitivity resulting in severe sunburns upon minimal UV exposure in infancy, widespread dense freckling, xerosis, poikiloderma on sun-exposed facial skin, and bilateral corneal clouding. By age 7, she has developed multiple primary Basal Cell Carcinomas and invasive Squamous Cell Carcinomas. What DNA repair mechanism is defective in Xeroderma Pigmentosum?",
            "Nucleotide excision repair defect failing to excise pyrimidine dimers",
            ["Mismatch repair (MMR) pathway, causing microsatellite instability", "Base excision repair (BER) pathway, causing 8-hydroxyguanine accumulation", "Homologous recombination repair, leading to chromosome fragility"],
            "Xeroderma Pigmentosum (XP, complementation groups XPA through XPG) is an autosomal recessive genodermatosis characterized by severe impairment of the Nucleotide Excision Repair (NER) multi-enzyme machinery. Cells are completely unable to recognize and excise bulky DNA photoproducts induced by ultraviolet light (such as cyclobutane pyrimidine dimers [CPDs] and 6-4 photoproducts). This produces a >1000-fold to 10,000-fold increase in the incidence of non-melanoma skin cancer and cutaneous melanoma before age 10.",
            clinical=True
        ),
    ]),
    (29, "Skin Disorders due to Light", "easy", [
        q(
            "A 24-year-old female presents every spring with an intensely itchy, symmetrical eruption of monomorphic erythematous papules, papulovesicles, and plaques on sun-exposed areas (V-neck of chest and dorsal forearms) developing 8 to 24 hours after her first significant seasonal sun exposure. As summer progresses, the eruption gradually decreases in severity despite continued sun exposure ('hardening phenomenon'). What is the diagnosis?",
            "Polymorphous light eruption (PMLE)",
            ["Solar urticaria", "Porphyria cutanea tarda", "Lupus erythematosus"],
            "Polymorphous Light Eruption (PMLE) is the most common acquired idiopathic photodermatosis worldwide (>10-20% of fair-skinned individuals). It represents a delayed-type hypersensitivity reaction to a photo-induced cutaneous neoantigen triggered by UVA (and UVB). Hallmarks: delayed onset (hours to days post-exposure), pruritic papules or papulovesicles on exposed skin (sparing the face due to habitual exposure), and the pathognomonic 'hardening' phenomenon (tolerance develops through repetitive sun exposure by late summer).",
            clinical=True
        ),
        q(
            "A 52-year-old male with chronic Hepatitis C infection and alcohol use presents with extreme skin fragility and tense bullae on the dorsa of his hands that rupture upon trivial friction, healing with milia, pigment changes, and atrophic scars. Examination reveals dark brown facial hyperpigmentation and prominent hypertrichosis on his temples and cheeks. Urine examined under Wood's light emits a brilliant coral-pink to red fluorescence. What is the diagnosis and the defective enzyme?",
            "Porphyria cutanea tarda (PCT); Uroporphyrinogen decarboxylase (UROD) deficiency",
            ["Acute intermittent porphyria; Porphobilinogen deaminase deficiency", "Variegate porphyria; Protoporphyrinogen oxidase deficiency", "Erythropoietic protoporphyria; Ferrochelatase deficiency"],
            "Porphyria Cutanea Tarda (PCT) is the most common porphyria, caused by acquired or hereditary deficiency of hepatic Uroporphyrinogen Decarboxylase (UROD). Uroporphyrins accumulate in the blood and deposit in skin, where absorption of Soret band light (400-410 nm) generates reactive oxygen species. Hallmarks: mechanobullous skin fragility on dorsal hands with milia, facial hypertrichosis, and dark tea-colored urine that fluoresces brilliant coral-pink under Wood's lamp (365 nm UVA). High association with Hepatitis C virus.",
            clinical=True
        ),
        q(
            "Which clinical and immunological characteristics distinguish a Phototoxic Drug Eruption from a Photoallergic Drug Eruption?",
            "Phototoxicity is dose-dependent non-immunologic sunburn; Photoallergy is type IV eczematous allergy",
            ["Phototoxicity requires 2 weeks sensitization; Photoallergy occurs on first exposure", "Phototoxicity is mediated by circulating IgE antibodies causing urticarial wheals", "Photoallergy is universal dose-dependent toxicity resolving within 2 hours"],
            "Phototoxicity: 1. Non-immunologic direct cellular damage by photoactivated drug radicals; 2. Dose-dependent (occurs in anyone given sufficient drug + UV dose); 3. Rapid onset (minutes to hours); 4. Morphologically resembles an exaggerated, severe sunburn (erythema, edema, bullae); 5. Strictly delimited to exposed skin (sharp cutoffs at clothing lines); common drugs: Doxycycline, amiodarone, thiazides. Photoallergy: Type IV delayed-type hypersensitivity; eczematous; spreads beyond exposed skin; requires prior sensitization.",
            clinical=False
        ),
        q(
            "A 28-year-old female develops intensely pruritic, erythematous, edematous wheals and flares across all uncovered skin within 5 to 10 minutes of direct sunlight exposure, which completely vanish within 1 to 2 hours after she steps into indoor shade. Phototesting with visible light and UVA reproduces identical hives. What is this physical photodermatosis termed?",
            "Solar urticaria",
            ["Polymorphous light eruption", "Chronic actinic dermatitis", "Erythropoietic protoporphyria"],
            "Solar urticaria is an uncommon, chronic physical inducible urticaria where direct exposure to sunlight (UVA, UVB, or visible light) triggers wheal-and-flare formation within 5 to 10 minutes. It is mediated by a Type I (immediate) IgE-dependent hypersensitivity reaction: a light-induced chromophore in the skin acts as a photoallergen that binds circulating IgE, triggering immediate mast cell degranulation. Wheals resolve rapidly (<1-2 hours) after UV exposure ceases.",
            clinical=True
        ),
        q(
            "A 24-year-old male bartender squeezed dozens of fresh limes for cocktails at an outdoor beach party on a sunny afternoon. Two days later, he develops painless, linear, streaked, bizarre-shaped erythematous macules and bullae on the dorsa of his hands, which heal leaving behind dense, dark brown hyperpigmentation that persists for months ('margarita photodermatitis'). What is the diagnosis and the responsible photochemical?",
            "Phytophotodermatitis; Furocoumarins (Psoralens like 5-methoxypsoralen) interacting with UVA light",
            ["Allergic contact dermatitis; Urushiol", "Chemical burn; Citric acid alone", "Fixed drug eruption; Alcohol ingestion"],
            "Phytophotodermatitis (Berloque dermatitis / lime-induced photodermatitis) is a non-immunologic phototoxic reaction caused by skin contact with plants containing phototoxic furocoumarins (psoralens, especially 5-MOP and 8-MOP in limes, celery, parsnips, figs) followed by exposure to solar Ultraviolet A (UVA, 320-400 nm). The activated psoralen intercalates into DNA and generates singlet oxygen, causing epidermal necrosis, bizarre linear/splattered blister patterns, and intense, long-lasting hyperpigmentation.",
            clinical=True
        ),
    ]),
]
