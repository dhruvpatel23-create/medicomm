from .common import q

CHAPTERS = [
    (10, "Psoriasis", "hard", [
        q(
            "A 34-year-old male presents with sharply demarcated, salmon-pink erythematous plaques covered by thick, layered, silvery-white micaceous scales over both extensor elbows, knees, and presacral region. Skin biopsy demonstrates regular epidermal acanthosis with uniform clubbed elongation of rete ridges, absence of the stratum granulosum, confluent parakeratosis, and focal intracorneal collections of neutrophils. What are these diagnostic neutrophil aggregates termed?",
            "Munro microabscesses",
            ["Pautrier microabscesses", "Kogoj pustules in spinous layer", "Civatte bodies"],
            "Munro microabscesses are collections of degenerated neutrophils migrating through the epidermis and trapped within parakeratotic stratum corneum, representing a cardinal histological hallmark of psoriasis vulgaris. Neutrophil collections within the spinous layer with surrounding spongiosis are termed spongiform pustules of Kogoj. Pautrier microabscesses contain atypical CD4+ T-lymphocytes in Mycosis Fungoides.",
            clinical=True
        ),
        q(
            "What precise microvascular and epidermal architecture explains the elicitation of Auspitz sign (pinpoint bleeding droplets upon peeling the membrane of Bulkeley) in plaque psoriasis?",
            "Thinning of suprapapillary plates over dilated capillaries",
            ["Necrosis and rupture of large subcutaneous arterioles", "Diffuse intraepidermal microaneurysms", "Acantholytic loss of perivascular desmosomes"],
            "In psoriasis, the suprapapillary epidermal plate (the epidermis overlying dermal papillae) is dramatically thinned to just a few cell layers. The dermal papillae are elongated and house dilated, tortuous, hyperpermeable capillary loops. When the overlying silvery scales and the glistening basement layer (membrane of Bulkeley) are removed, the roof of these superficial papillary capillary loops is torn, producing punctate pinpoint bleeding (Auspitz sign).",
            clinical=False
        ),
        q(
            "A 16-year-old high school student suddenly develops an acute, widespread eruption of hundreds of small, drop-like (2 to 8 mm), scaly, salmon-colored papules and plaques across his trunk and proximal extremities, 2 weeks after recovering from severe exudative pharyngitis. Serum antistreptolysin O (ASO) titer is markedly elevated. What is the diagnosis?",
            "Guttate psoriasis",
            ["Pityriasis rosea", "Secondary syphilis", "Lichen planus"],
            "Guttate psoriasis characteristically erupts in children and adolescents 1 to 3 weeks following an acute Group A beta-hemolytic streptococcal pharyngitis or perianal streptococcal infection. It manifests as a sudden 'rain shower' eruption of small, droplet-like (gutta = drop) erythematous scaly papules on the trunk and limbs, strongly linked to HLA-Cw*0602.",
            clinical=True
        ),
        q(
            "A 42-year-old female with long-standing plaque psoriasis was inappropriately treated with a 2-week course of high-dose systemic oral prednisolone. Three days after abruptly stopping the steroids, she develops high spiking fever, rigors, leukocytosis, and an acute eruption of sheets of hundreds of pinpoint sterile yellow pustules coalescing into 'lakes of pus' on a generalized fiery erythroderma. What life-threatening condition is this?",
            "Generalized pustular psoriasis of von Zumbusch",
            ["Acute generalized exanthematous pustulosis", "Subcorneal pustular dermatosis", "Toxic epidermal necrolysis"],
            "Generalized Pustular Psoriasis of von Zumbusch is an acute, life-threatening form of psoriasis that is classically triggered by the abrupt withdrawal of systemic corticosteroids. Patients experience profound systemic toxicity, high fever, circulatory instability, and rapid eruption of waves of sterile, superficial pustules that coalesce into extensive 'lakes of pus' on fiery erythematous skin.",
            clinical=True
        ),
        q(
            "Which combination of nail changes is considered the most specific and characteristic for Psoriatic Nail Disease?",
            "Deep irregular pits, 'oil drop' (salmon patch) discoloration, and subungual hyperkeratosis",
            ["Longitudinal melanonychia and trachyonychia", "Koilonychia and Beau lines", "Splinter hemorrhages alone with pterygium inversum"],
            "Psoriatic nail dystrophy occurs in up to 50% of psoriasis patients and 80% of psoriatic arthritis patients. Hallmarks: 1. Nail matrix psoriasis: deep, irregular, randomly distributed punctate pits (due to focal parakeratosis of the proximal matrix), leukonychia, and red spots in the lunula; 2. Nail bed psoriasis: pathognomonic 'oil-drop' or 'salmon patch' (translucent yellowish-red discoloration from bed parakeratosis), subungual hyperkeratosis, and distal onycholysis.",
            clinical=False
        ),
        q(
            "A 55-year-old male presents with generalized erythema and scaling involving over 92% of his total body surface area, accompanied by severe peripheral edema, shivering from impaired thermoregulation, and high-output cardiac decompensation. What percentage of cutaneous involvement defines Erythroderma?",
            "Greater than 90% body surface area involvement",
            ["Greater than 50% body surface area involvement", "Greater than 30% body surface area involvement", "Greater than 75% body surface area involvement"],
            "Erythroderma (exfoliative dermatitis) is defined as generalized, confluent erythema and scaling affecting at least 90% of the total body surface area. It represents a dermatological emergency causing profound metabolic and hemodynamic complications: hypothermia (from cutaneous vasodilation), high-output cardiac failure, massive protein loss from exfoliated scale, dehydration, and electrolyte disturbances. Pre-existing psoriasis is the single most common cause.",
            clinical=True
        ),
        q(
            "What is the specific immunological molecular target of Ustekinumab, a human monoclonal antibody approved for the treatment of moderate-to-severe plaque psoriasis and psoriatic arthritis?",
            "Shared p40 subunit of interleukin-12 (IL-12) and interleukin-23 (IL-23)",
            ["Soluble tumor necrosis factor-alpha (TNF-alpha)", "Interleukin-17A receptor (IL-17RA)", "p19 subunit of interleukin-23 alone"],
            "Ustekinumab is a fully human IgG1kappa monoclonal antibody that binds with high affinity to the common shared p40 protein subunit of both interleukin-12 (IL-12) and interleukin-23 (IL-23). By preventing p40 from interacting with the IL-12Rbeta1 receptor, it blocks both the Th1 (IL-12 driven) and Th17 (IL-23 driven) inflammatory cascades. In contrast, Guselkumab and Risankizumab selectively target the p19 subunit of IL-23 alone.",
            clinical=False
        ),
        q(
            "A 48-year-old male with severe recalcitrant psoriasis is treated with oral Methotrexate (15 mg/week). What serious chronic parenchymal organ toxicity requires serial non-invasive screening (such as transient elastography / FibroScan or serum procollagen III amino-terminal peptide [P3NP]) after cumulative doses exceed 1.5 grams?",
            "Hepatic fibrosis and cirrhosis",
            ["Pulmonary alveolar proteinosis", "Chronic renal tubular acidosis", "Dilated cardiomyopathy"],
            "Methotrexate is a dihydrofolate reductase inhibitor widely used in severe psoriasis. Long-term cumulative use (>1.5 to 3.0 grams) carries a significant risk of cumulative hepatic steatosis, progressive fibrosis, and cirrhosis. Current guidelines recommend non-invasive monitoring using serum Procollagen III N-terminal peptide (P3NP) assays or hepatic transient elastography (FibroScan) to minimize the need for routine surveillance liver biopsies.",
            clinical=True
        ),
        q(
            "Why must a 28-year-old female patient treated with oral Acitretin for severe plaque psoriasis strictly maintain effective contraception during therapy and for a full three years AFTER completing the course?",
            "Transesterification into etretinate with prolonged 120-day half-life",
            ["Accelerated hepatic clearance causing therapeutic failure", "Synergistic induction of acute hemorrhagic pancreatitis", "Competitive inhibition of intestinal retinoid absorption"],
            "Acitretin (an oral second-generation aromatic retinoid) has an elimination half-life of ~50 hours. However, in the presence of even minuscule amounts of dietary ethanol/alcohol, acitretin undergoes reverse metabolic transesterification into its parent compound, Etretinate. Etretinate is lipophilic, stored in adipose tissue, has an extremely prolonged elimination half-life (120 days), and is notoriously teratogenic (craniofacial, cardiac, and CNS malformations), necessitating strict contraception for 3 years post-therapy.",
            clinical=False
        ),
        q(
            "What histopathological pattern of the dermo-epidermal junction and epidermal rete pegs is classically described in fully established, mature Psoriasis vulgaris?",
            "Regular, uniform elongation and clubbing of rete ridges ('test-tubes in a rack')",
            ["Saw-toothed irregular rete pegs with basal liquefaction", "Complete atrophy and flattening of all rete pegs", "Pseudoepitheliomatous hyperplasia with horn pearls"],
            "The histopathology of mature psoriasis vulgaris is characterized by: 1. Regular, uniform elongation of rete ridges with club-shaped thickened lower portions, famously likened to 'test-tubes in a rack'; 2. Marked thinning of suprapapillary plates; 3. Dilated, tortuous capillaries in edematous dermal papillae; 4. Confluent parakeratosis with absent stratum granulosum; 5. Munro microabscesses and Kogoj pustules.",
            clinical=False
        ),
    ]),
    (11, "Lichenoid Skin Disorders", "hard", [
        q(
            "A 36-year-old female presents with an intensely itchy eruption on the flexor surfaces of both wrists, forearms, and medial ankles. Examination reveals shiny, flat-topped, polygonal, violaceous papules crossed by a delicate, fine, lacy network of whitish lines on their surface. What are these diagnostic white surface lines termed, and what is the underlying condition?",
            "Wickham striae; Lichen planus",
            ["Civatte striae; Psoriasis", "Koebner lines; Vitiligo", "Auspitz streaks; Eczema"],
            "Lichen planus is a chronic T-cell-mediated autoimmune mucocutaneous disorder summarized by the '6 Ps': Pruritic, Polygonal, Planar (flat-topped), Purple (violaceous), Papules and Plaques. The characteristic fine, white, reticular, lacy lines on the surface of papules and oral mucosal lesions are known as Wickham's striae, produced histologically by focal, localized thickening of the stratum granulosum (focal hypergranulosis).",
            clinical=True
        ),
        q(
            "Which constellation of histopathological findings on a punch biopsy of an active cutaneous lesion is pathognomonic for Lichen Planus?",
            "Band-like interface infiltrate, basal liquefaction, and saw-toothed rete",
            ["Elongated rete ridges with Munro microabscesses", "Subepidermal blister with papillary microabscesses", "Spongiotic intraepidermal microvesicles"],
            "The classic histopathological tetrad of Lichen Planus: 1. Compact orthokeratosis without parakeratosis; 2. Wedge-shaped hypergranulosis; 3. Irregular 'saw-toothed' acanthosis of rete ridges; 4. Basal layer liquefactive degeneration (hydropic vacuolization); 5. Band-like (lichenoid) lymphocytic infiltrate hugging the dermo-epidermal junction; 6. Civatte bodies (colloid/cytoid bodies—apoptotic basal keratinocytes).",
            clinical=False
        ),
        q(
            "What are 'Max Joseph spaces' observed on histopathological examination of Lichen Planus?",
            "Subepidermal clefts due to extensive basal cell liquefaction",
            ["Intraepidermal microabscesses with neutrophils", "Subcorneal collections of acantholytic cells", "Neutrophilic abscesses at papillary tips"],
            "In lichen planus, severe, widespread liquefactive hydropic degeneration of basal keratinocytes destroys the mechanical continuity of the dermo-epidermal junction. During histological tissue processing, this weakened junction separates focally, forming small, artifactual clefts between the basal epidermis and papillary dermis termed 'Max Joseph spaces'. When this separation becomes extensive clinically, it produces the rare variant 'Bullous Lichen Planus'.",
            clinical=False
        ),
        q(
            "A 45-year-old male presents with persistent, painful, ulcerated, and eroded lesions on the bilateral buccal mucosa that have failed to respond to topical antiseptics for 18 months. Biopsy confirms erosive (ulcerative) oral lichen planus. Why is long-term clinical surveillance mandatory in this specific patient?",
            "Squamous cell carcinoma transformation risk in erosive oral variant",
            ["Adenocarcinoma transformation risk in reticular variant", "Systemic B-cell lymphoma risk in hypertrophic variant", "Basal cell carcinoma transformation risk in bullous variant"],
            "While reticular oral lichen planus (characterized by asymptomatic bilateral lacy Wickham striae) is typically benign, the chronic erosive (ulcerative) and atrophic subtypes of oral lichen planus are officially classified as oral potentially malignant disorders (OPMDs). They carry an estimated 1% to 2% lifetime risk of malignant transformation into oral Squamous Cell Carcinoma (SCC), mandating regular long-term follow-up and biopsy of suspicious non-healing ulcers.",
            clinical=True
        ),
        q(
            "A 40-year-old female presents with progressive, patchy hair loss on the crown and vertex of her scalp. Examination reveals perifollicular erythema, violaceous scaling around emerging hair shafts ('perifollicular collarettes'), and scarring loss of follicular ostia. Biopsy reveals a dense lymphocytic infiltrate destroying the follicular infundibulum and isthmus with permanent scarring. What is the diagnosis?",
            "Lichen planopilaris (follicular lichen planus)",
            ["Alopecia areata", "Telogen effluvium", "Dissecting cellulitis of scalp"],
            "Lichen planopilaris (LPP) is the follicular variant of lichen planus, representing a primary cicatricial (scarring) alopecia. It preferentially targets the stem-cell-rich bulge region of hair follicles (infundibulum and isthmus). Hallmarks: active violaceous follicular papules and scaling at the advancing perimeter of smooth, shiny, atrophic bald patches where follicular openings are permanently obliterated.",
            clinical=True
        ),
        q(
            "What classic clinical triad defines the Graham-Little-Piccardi-Lassueur syndrome?",
            "Cicatricial scalp alopecia, non-scarring axillary alopecia, and spinous papules",
            ["Patchy alopecia areata, leukonychia, and vitiligo", "Scarring eyebrow loss, keratoderma, and ichthyosis", "Total scalp atrichia, anhidrosis, and conical incisors"],
            "Graham-Little-Piccardi-Lassueur syndrome is an uncommon variant of lichen planus characterized by the pathognomonic triad of: 1. Multifocal primary cicatricial (scarring) alopecia of the scalp; 2. Non-cicatricial hair loss involving the axillae and pubic hair; 3. Disseminated follicular hyperkeratotic, spinous papules on the trunk and limbs resembling lichen spinulosus.",
            clinical=False
        ),
        q(
            "A 52-year-old postmenopausal female presents with severe vulvar pruritus, dyspareunia, and burning. Physical examination reveals porcelain-white, ivory-colored, atrophic plaques with a wrinkled 'cigarette-paper' texture surrounding the vulva and perianal region in a classic 'figure-of-eight' or 'hourglass' configuration, with resorption and fusion of the labia minora. What is the diagnosis?",
            "Lichen sclerosus (et atrophicus)",
            ["Lichen planus", "Extramammary Paget disease", "Genital candidiasis"],
            "Lichen sclerosus (historically kraurosis vulvae) is a chronic inflammatory dermatosis with a predilection for the anogenital region in postmenopausal women. Classic appearance: porcelain-white, shiny, polygonal papules and atrophic plaques with follicular plugging, wrinkling ('cigarette-paper skin'), and fusion of the labia minora ('architectural obliteration') in an anogenital 'figure-of-eight' distribution. Patients have an increased risk (4-5%) of vulvar squamous cell carcinoma.",
            clinical=True
        ),
        q(
            "A 50-year-old male presents with thick, hyperkeratotic, verrucous, brownish-violaceous plaques covered by fine adherent scales on the anterior aspect of both shins. Pruritus is extraordinarily intense and intractable. Biopsy confirms Hypertrophic Lichen Planus. What malignant transformation can rarely complicate long-standing neglected lesions on the shins?",
            "Squamous cell carcinoma (Marjolin-like malignant transformation)",
            ["Basal cell carcinoma", "Cutaneous angiosarcoma", "Malignant blue nevus"],
            "Hypertrophic (verrucous) lichen planus is the most pruritic variant of lichen planus, characteristically targeting the pretibial surfaces (shins) and dorsal feet as symmetric, thick, purplish, warty plaques with follicular plugging. Chronic, neglected, long-standing hypertrophic LP carries an elevated risk of malignant transformation into invasive well-differentiated Squamous Cell Carcinoma.",
            clinical=True
        ),
        q(
            "Which clinical and histopathological feature most reliably distinguishes a Lichenoid Drug Eruption from idiopathic Lichen Planus?",
            "Parakeratosis, tissue eosinophils, and absence of Wickham striae",
            ["Absent basal liquefaction and absent pruritus", "Suprabasal acantholysis with mucosal erosions", "Neutrophilic papillary microabscesses on biopsy"],
            "Lichenoid drug eruptions (triggered by beta-blockers, ACE inhibitors, thiazides, antimalarials, and gold) clinically mimic idiopathic LP but have distinguishing features: lesions are often more eczematous, psoriasiform, or photo-distributed, and Wickham striae are usually absent. On biopsy, the presence of focal parakeratosis, apoptotic Civatte bodies in the upper spinous/granular layers, and dermal infiltrate containing eosinophils and plasma cells distinguishes it from idiopathic LP.",
            clinical=False
        ),
        q(
            "What is the classical diagnostic phenomenon termed when cutaneous lichen planus papules erupt within linear surgical scars, scratch marks, or areas of friction?",
            "Koebner isomorphic phenomenon",
            ["Pathergy reaction", "Auspitz sign", "Nikolsky sign"],
            "The Koebner phenomenon (isomorphic response) is characteristically positive in active Lichen Planus (along with psoriasis and vitiligo). Traumatizing normal-appearing skin via scratches, surgical incisions, or constant friction stimulates keratinocyte release of cytokines (IFN-gamma, TNF-alpha) that recruit autoreactive cytotoxic T cells, precipitating identical violaceous polygonal flat-topped papules along the linear path of injury within 7 to 14 days.",
            clinical=False
        ),
    ]),
    (12, "Miscellaneous Papulosquamous Disorders and Erythroderma", "easy", [
        q(
            "A 42-year-old male presents with an orange-red erythroderma that characteristically spares sharp, well-demarcated 'islands of normal skin' within the diffuse erythema. The dorsa of his fingers show follicular hyperkeratotic papules resembling a 'nutmeg grater', and his palms and soles display a thick, waxy, yellow-orange keratoderma ('PRP sandals'). What is the diagnosis?",
            "Pityriasis rubra pilaris (PRP)",
            ["Psoriatic erythroderma", "Sezary syndrome", "Atopic erythroderma"],
            "Pityriasis Rubra Pilaris (PRP, particularly classical adult Type I) is characterized by: 1. Rapidly spreading orange-red (salmon-colored) plaques with pathognomonic, sharply defined 'islands of normal skin' (nappes claires); 2. Follicular hyperkeratotic plug-like papules on the dorsal proximal phalanges ('nutmeg-grater sign'); 3. Waxy, yellow-orange, thickened palmoplantar keratoderma resembling a sandal ('PRP sandal'); 4. Alternating orthokeratosis and parakeratosis ('checkerboard pattern') on histology.",
            clinical=True
        ),
        q(
            "What clinical triad characterizes Sézary Syndrome, the leukemic and erythrodermic variant of Cutaneous T-Cell Lymphoma (Mycosis Fungoides)?",
            "Erythroderma, generalized lymphadenopathy, and circulating cerebriform Sézary cells",
            ["Erythroderma, hepatomegaly, and peripheral Reed-Sternberg cells", "Exfoliative dermatitis, nephrotic proteinuria, and smudge cells", "Ichthyosiform erythroderma, sensorineural deafness, and keratitis"],
            "Sézary syndrome is the leukemic, aggressive form of Cutaneous T-cell Lymphoma (CTCL). Diagnostic triad: 1. Pruritic, generalized, exfoliative erythroderma; 2. Generalized lymphadenopathy; 3. Demonstration of circulating clonally expanded CD4+ T-helper cells with grooved, folded, hyperconvoluted 'cerebriform' nuclei (Sézary cells) exceeding 1,000/mcL in peripheral blood or a CD4/CD8 ratio >10.",
            clinical=False
        ),
        q(
            "What are the four most frequent underlying dermatological dermatoses that account for over 75% of all cases of secondary adult Erythroderma?",
            "Psoriasis, Eczema (atopic/contact), Adverse drug reactions, and Cutaneous T-Cell Lymphoma",
            ["Lichen planus, Pemphigus vulgaris, Vitiligo, and Alopecia areata", "Basal cell carcinoma, Melanoma, Histiocytosis, and Leprosy", "Impetigo, Scabies, Tinea corporis, and Molluscum contagiosum"],
            "The leading etiologies of erythroderma (exfoliative dermatitis) in adults: 1. Preexisting dermatoses (Psoriasis is #1, followed by Atopic, Seborrheic, and Allergic Contact Eczemas); 2. Adverse drug eruptions (anticonvulsants, allopurinol, sulfonamides); 3. Cutaneous T-cell lymphoma (Sézary syndrome / Mycosis fungoides); 4. Idiopathic ('red man syndrome').",
            clinical=False
        ),
        q(
            "A 52-year-old male presents with multiple, large (>5 cm), irregularly shaped, atrophic, dusky-red patches exhibiting cigarette-paper wrinkling, telangiectasias, and reticulate pigmentation (poikiloderma) distributed across his 'bathing-trunk' area. Biopsy reveals atypical lymphoid cells along the dermo-epidermal junction. What condition is this, and what malignancy does it portend?",
            "Large-plaque parapsoriasis; high propensity to progress into Mycosis Fungoides",
            ["Guttate parapsoriasis; progression into B-cell lymphoma", "Pityriasis rosea; progression into systemic lupus erythematosus", "Eczema craquelé; progression into basal cell carcinoma"],
            "Large-plaque parapsoriasis is a chronic clonal T-cell dermatosis presenting with large (>5 cm), yellowish-fawn to dusky-erythematous patches characteristically distributed in 'bathing-trunk' or sun-shielded areas, often demonstrating poikiloderma (mottled atrophy, telangiectasia, pigmentation). It represents a form of pre-Mycosis Fungoides or patch-stage Mycosis Fungoides with a high rate of malignant progression (up to 30-40% over decades).",
            clinical=True
        ),
        q(
            "A 14-year-old boy presents with an acute, self-limiting eruption of recurrent crops of erythematous macules and papules that rapidly evolve into hemorrhagic vesicles, central crusts, and varioliform (pockmark-like) scars, accompanied by low-grade fever. What is the diagnosis?",
            "Pityriasis lichenoides et varioliformis acuta (PLEVA / Mucha-Habermann disease)",
            ["Pityriasis lichenoides chronica (PLC)", "Varicella (Chickenpox)", "Guttate psoriasis"],
            "Pityriasis Lichenoides et Varioliformis Acuta (PLEVA, also known as Mucha-Habermann disease) is an acute clonal T-cell-mediated reactive papulosquamous disorder. It presents in children and young adults with recurrent crops of inflammatory papules that develop central purpura, blister formation, ulceration, and necrosis, characteristically healing with depressed, varioliform (pockmark-like) scars.",
            clinical=True
        ),
    ]),
    (13, "Eczematous Disorders", "hard", [
        q(
            "According to the classic Hanifin and Rajka diagnostic criteria for Atopic Dermatitis, a patient must fulfill at least three of four Major Criteria. What are these four Major Criteria?",
            "Pruritus, typical flexural/facial morphology, chronicity, and atopic history",
            ["Xerosis, palmar hyperlinearity, pityriasis alba, and elevated IgE", "Dennie-Morgan fold, keratosis pilaris, and cataracts", "Recurrent skin infections, cheilitis, and nipple eczema"],
            "The 4 Major Hanifin-Rajka Criteria for Atopic Dermatitis: 1. Pruritus (cardinal symptom); 2. Typical morphology and distribution: facial/extensor involvement in infants; flexural lichenification and linearity in adults; 3. Chronic or chronically-relapsing course; 4. Personal or family history of atopic diathesis (asthma, allergic rhinitis, atopic dermatitis). Minor criteria include xerosis, ichthyosis, Dennie-Morgan infraorbital fold, hyperlinear palms, and elevated serum IgE.",
            clinical=False
        ),
        q(
            "What epidermal structural protein gene undergoes loss-of-function mutations in up to 50% of patients with moderate-to-severe Atopic Dermatitis, predisposing to defective stratum corneum hydration and transepidermal allergen penetration?",
            "Filaggrin (FLG) gene",
            ["Collagen Type VII (COL7A1) gene", "Loricrin (LOR) gene", "Involucrin (IVL) gene"],
            "Loss-of-function mutations in the Filaggrin (FLG) gene (located on chromosome 1q21 in the Epidermal Differentiation Complex) represent the strongest known genetic risk factor for Atopic Dermatitis (and Ichthyosis Vulgaris). Filaggrin deficiency disrupts keratohyalin packing, impairs natural moisturizing factor (NMF) generation, raises stratum corneum pH, and leads to defective barrier function, allowing percutaneous allergen penetration and triggering Th2 immune cascades.",
            clinical=False
        ),
        q(
            "What is the precise molecular target and mechanism of action of Dupilumab, a breakthrough fully human monoclonal antibody approved for moderate-to-severe atopic dermatitis?",
            "IL-4 receptor alpha subunit, inhibiting IL-4 and IL-13",
            ["IL-17A ligand, preventing neutrophil recruitment", "TNF-alpha soluble ligand, inhibiting receptor binding", "IL-23 p19 subunit, blocking Th17 differentiation"],
            "Dupilumab is a recombinant human IgG4 monoclonal antibody directed against the shared alpha subunit of the interleukin-4 receptor complex (IL-4R-alpha). Because IL-4R-alpha is a component of both the Type I receptor (IL-4 specific) and Type II receptor (utilized by both IL-4 and IL-13), Dupilumab potently blocks the dual downstream signaling of IL-4 and IL-13, the two master Th2 cytokines driving atopic dermatitis.",
            clinical=False
        ),
        q(
            "A 25-year-old female develops a pruritic, vesicular, weeping erythematous eruption exactly underlying the metal buckle of her belt and metal studs of her jeans. Which metal is the single most common contact allergen worldwide, and what immunologic mechanism mediates this reaction?",
            "Nickel sulfate; Type IV (delayed-type) cell-mediated hypersensitivity",
            ["Cobalt chloride; Type I IgE-mediated immediate hypersensitivity", "Chromium; Type II antibody-dependent cytotoxicity", "Gold sodium thiomalate; Type III immune complex deposition"],
            "Allergic Contact Dermatitis (ACD) to Nickel is the most frequent contact allergy in the world (>15% of women). It is a classic Type IV (delayed-type) cell-mediated hypersensitivity reaction: Nickel acts as a hapten, binding to epidermal self-proteins, processed by epidermal Langerhans cells, and presented to CD4+ T-helper 1 (Th1) memory cells. Re-exposure triggers cytokine release (IFN-gamma, IL-2), producing spongiotic dermatitis 48 to 72 hours later. Patch testing with 5% nickel sulfate confirms the diagnosis.",
            clinical=True
        ),
        q(
            "Which key pathophysiological and clinical features distinguish Irritant Contact Dermatitis (ICD) from Allergic Contact Dermatitis (ACD)?",
            "Non-immunologic direct cytotoxicity, burning sensation, and sharp borders",
            ["Type IV hypersensitivity requiring sensitization and spreading beyond borders", "IgE-mediated immediate hypersensitivity causing evanescent wheals", "Clonal T-cell memory proliferation with positive patch test"],
            "Irritant Contact Dermatitis (accounting for 80% of all contact dermatitis, commonly seen in wet-workers / dishwashers): 1. Non-immunologic: direct chemical or physical injury to keratinocyte cell membranes and skin barrier; 2. No sensitization phase required: occurs on first exposure if concentration is high enough; 3. Burning and pain dominate over itching; 4. Strictly limited to the anatomical area of contact; 5. Negative patch test.",
            clinical=False
        ),
        q(
            "A 32-year-old male presents with greasy, yellowish, greasy scales overlying poorly defined erythematous patches on his scalp, eyebrows, glabella, nasolabial folds, and presternal region. What commensal lipid-dependent fungal organism plays a central pathogenic role in triggering this inflammation?",
            "Malassezia species (M. restricta and M. globosa)",
            ["Candida albicans", "Trichophyton mentagrophytes", "Epidermophyton floccosum"],
            "Seborrheic dermatitis is a chronic inflammatory disorder localized to sebum-rich anatomical regions (scalp, face, chest, retroauricular folds). Lipophilic Malassezia yeasts (especially M. restricta and M. globosa) metabolize sebum triglycerides using fungal lipases, releasing irritant free fatty acids (oleic acid, arachidonic acid) that breach the epidermal barrier and incite secondary inflammation in susceptible hosts. Topical ketoconazole and zinc pyrithione are first-line treatments.",
            clinical=True
        ),
        q(
            "A 45-year-old male with dry skin presents with multiple discrete, coin-shaped (nummular), intensely pruritic, erythematous plaques studded with tiny vesicles, oozing, and crusts on the extensor aspects of his lower legs and forearms. What is the diagnosis?",
            "Nummular (discoid) eczema",
            ["Psoriasis vulgaris", "Tinea corporis", "Lichen planus"],
            "Nummular eczema (discoid dermatitis) is characterized by strikingly discrete, coin-shaped (nummular = coin-like), round or oval plaques ranging from 1 to 5 cm in diameter. Lesions classically develop on the lower legs and arms of middle-aged and elderly individuals with underlying xerosis, presenting with clustered papules, microvesicles, confluent serous weeping, and honey-colored crusting.",
            clinical=True
        ),
        q(
            "A 26-year-old female complains of recurrent, intensely pruritic crops of deep-seated, tense, clear, non-erythematous vesicles located symmetrically along the lateral borders of her fingers and on her palms, resembling 'tapioca pudding'. What is the diagnosis?",
            "Dyshidrotic eczema (Pompholyx)",
            ["Herpes simplex (herpetic whitlow)", "Scabies", "Bullous pemphigoid"],
            "Pompholyx (dyshidrotic eczema / vesicular palmoplantar dermatitis) is an acute or recurrent episodic eruption characterized by deep-seated, tense, pruritic vesicles likened to 'tapioca pudding grains' on the lateral margins of the fingers, palms, and soles. Despite its historical name 'dyshidrosis', it has no relationship to eccrine sweat gland dysfunction, but represents an intense spongiotic reaction triggered by contact allergens, sweating, or atopy.",
            clinical=True
        ),
        q(
            "A 60-year-old female with chronic varicose veins presents with pitting edema, brawny brownish-orange pigmentation, and itchy eczematous scaling over the medial aspect of both lower legs. What microvascular pathology and biochemical breakdown product cause this characteristic discoloration?",
            "Chronic venous hypertension causing extravasation of erythrocytes and dermal hemosiderin deposition",
            ["Arterial occlusion causing melanin hypersecretion", "Lymphatic hypoplasia causing amyloid accumulation", "Capillary thrombosis causing foreign-body keratinization"],
            "Stasis dermatitis is a direct consequence of chronic venous insufficiency and ambulatory venous hypertension: incompetent valves in the saphenous and perforator veins transmit elevated hydrostatic pressures to dermal capillary beds. Capillaries distend, become permeable, and extravasate erythrocytes into the dermis. Macrophages phagocytose the red cells, degrading hemoglobin into hemosiderin pigment, which produces the characteristic indelible golden-brown or brawny staining.",
            clinical=True
        ),
        q(
            "An 80-year-old male residing in a heated nursing facility during winter presents with dry, itchy, polygonal plates of skin separated by superficial red fissures on his anterior shins, giving the appearance of 'cracked porcelain' or 'dry riverbed'. What is this entity termed?",
            "Asteatotic eczema (Eczema craquelé)",
            ["Nummular eczema", "Stasis dermatitis", "Ichthyosis vulgaris"],
            "Asteatotic eczema (eczema craquelé) is caused by severe cutaneous dehydration, lipid depletion, and loss of epidermal barrier integrity in elderly individuals, aggravated by low humidity, dry indoor heating, and frequent hot soapy baths. It characteristically affects the pretibial shins as a network of fine red fissures crisscrossing polygonal keratin plates, resembling cracked china, dried mud, or crazy paving.",
            clinical=True
        ),
    ]),
    (14, "Urticaria and Reactive Erythemas", "easy", [
        q(
            "What clinical duration threshold strictly differentiates Acute Urticaria from Chronic Urticaria, and how long does an individual wheal characteristically persist at a single anatomical spot?",
            "6 weeks duration; individual wheals resolve within 24 hours",
            ["2 weeks duration; individual wheals persist over 48 hours", "12 weeks duration; individual lesions persist over several days", "4 weeks duration; individual lesions persist over 72 hours"],
            "Urticaria is categorized chronologically into Acute (<6 weeks duration, frequently triggered by infections, foods, or medications) and Chronic (spontaneous or inducible wheals occurring almost daily for >=6 weeks). Cardinal diagnostic feature: an individual urticarial wheal (edematous, pruritic plaque with surrounding erythema) is evanescent, developing rapidly and completely resolving within 2 to 24 hours without leaving any residual ecchymosis, purpura, or pigmentation.",
            clinical=False
        ),
        q(
            "A 32-year-old female presents with persistent urticarial wheals that burn and sting rather than itch. Unlike classic hives, each individual lesion remains fixed at the exact same site for 48 to 72 hours and resolves leaving behind localized purpura and faint brown post-inflammatory staining. Biopsy demonstrates leukocytoclastic vasculitis. What is the diagnosis?",
            "Urticarial vasculitis",
            ["Chronic spontaneous urticaria", "Angioedema", "Erythema annulare centrifugum"],
            "Urticarial vasculitis is a Type III immune complex-mediated small vessel vasculitis that clinically mimics urticaria. Critical distinguishing features: 1. Lesions persist for >24 hours at the exact same anatomical location (classic urticaria resolves <24 hours); 2. Burning, tender, or painful rather than purely pruritic; 3. Resolves with palpable purpura or post-inflammatory hemosiderin hyperpigmentation; 4. Biopsy confirms true leukocytoclastic vasculitis (fibrinoid necrosis, nuclear dust).",
            clinical=True
        ),
        q(
            "A 20-year-old collegiate athlete develops intense itching and an eruption of tiny (1 to 3 mm), punctate, highly pruritic wheals surrounded by large, intense erythematous flares across his trunk and neck within 10 minutes of beginning a vigorous run, taking a hot shower, or eating spicy soup. What type of physical urticaria is this?",
            "Cholinergic urticaria",
            ["Cold urticaria", "Solar urticaria", "Delayed pressure urticaria"],
            "Cholinergic urticaria is a distinctive physical inducible urticaria triggered by any factor that raises core body temperature by >=0.5 to 1.0 C (vigorous physical exertion, hot baths, emotional stress, spicy food). Sympathetic postganglionic cholinergic nerve fibers stimulate sweat glands and mast cells, producing classic monomorphic, tiny (1-3 mm) follicular wheals surrounded by widespread, axon-reflex flare erythema.",
            clinical=True
        ),
        q(
            "A 24-year-old male presents with recurrent episodes of non-pruritic, painless swelling of his lips, eyelids, laryngeal airway, and severe crampy abdominal pain without any cutaneous hives or wheals. Laboratory workup reveals severely reduced serum C4 levels and a quantitative deficiency of C1 esterase inhibitor (C1-INH). What is the primary mediator driving this angioedema?",
            "Bradykinin",
            ["Histamine", "Leukotriene B4", "Platelet-activating factor"],
            "Hereditary Angioedema (HAE Types I and II) is an autosomal dominant disorder caused by mutations in the SERPING1 gene, leading to deficiency (Type I, 85%) or functional dysfunction (Type II, 15%) of C1 esterase inhibitor (C1-INH). Unchecked activation of the plasma kallikrein-kinin system results in excessive production of Bradykinin, a potent non-histaminergic vasodilator that increases vascular permeability, causing swelling of the face, bowel wall (colic), and fatal laryngeal asphyxiation.",
            clinical=True
        ),
        q(
            "A 22-year-old male presents with an acute, symmetrical eruption of asymptomatic, concentric, three-zoned 'target' or 'iris' lesions on the dorsa of his hands, palms, and extensor forearms, 8 days after an episode of recurrent herpes labialis. What is the diagnosis, and what defines a true classic target lesion?",
            "Erythema multiforme minor; concentric target lesions with dusky center",
            ["Fixed drug eruption; solitary bullous hyperpigmented plaque", "Granuloma annulare; annular erythematous beaded plaque", "Urticarial vasculitis; fixed wheals persisting over 48 hours"],
            "Erythema Multiforme (EM) is an acute, immune-mediated mucocutaneous reactive condition triggered primarily by Herpes Simplex Virus (HSV-1 and HSV-2 in >70-80% of recurrent cases). The pathognomonic lesion is the 'classic target' (iris lesion), which has THREE concentric zones: 1. A central dusky, dark, purpuric or blistering zone; 2. An intermediate pale, edematous, raised ring; 3. A sharply defined, outer bright erythematous border.",
            clinical=True
        ),
    ]),
    (15, "Panniculitis and Erythema Nodosum", "easy", [
        q(
            "A 24-year-old female presents with multiple exquisitely tender, warm, painful, non-ulcerating, bright red subcutaneous nodules on the anterior surfaces of both shins, accompanied by ankle arthralgia and malaise, 10 days after a streptococcal sore throat. Over 3 weeks, the nodules evolve from red to purplish and yellowish-green, resembling resolving bruises ('erythema contusiformis'). What is the diagnosis and its primary histological classification?",
            "Erythema nodosum; septal panniculitis without vasculitis",
            ["Erythema induratum; lobular panniculitis with vasculitis", "Polyarteritis nodosa; necrotizing arteritis", "Subcutaneous panniculitis-like T-cell lymphoma"],
            "Erythema nodosum (EN) is the most common form of panniculitis. It is a delayed-type hypersensitivity reaction to various systemic antigenic triggers (Streptococcal pharyngitis, sarcoidosis, primary tuberculosis, IBD, drugs like sulfonamides and OCPs). Hallmarks: tender subcutaneous nodules on anterior shins that never ulcerate and resolve like a bruise (erythema contusiformis). Histologically, it is the prototype of Septal Panniculitis WITHOUT Vasculitis.",
            clinical=True
        ),
        q(
            "What pathognomonic microscopic histopathological structure located within the thickened subcutaneous interlobular septa confirms the diagnosis of early Erythema Nodosum?",
            "Miescher radial granulomas",
            ["Civatte bodies", "Asteroid bodies", "Schaumann bodies"],
            "Miescher's radial granulomas are the pathognomonic histopathological hallmark of early erythema nodosum. They are small, well-defined nodular aggregates of histiocytes and multinucleated giant cells arranged radially around a tiny central star-shaped or cleft-like central space within the thickened interlobular septa of the subcutaneous fat.",
            clinical=False
        ),
        q(
            "A 28-year-old female presents with bilateral hilar lymphadenopathy on chest radiography, acute bilateral ankle arthritis, and painful erythema nodosum on both shins. What is this clinical triad termed, and what is its prognosis in Sarcoidosis?",
            "Löfgren syndrome; acute benign sarcoidosis with high spontaneous remission",
            ["Heerfordt syndrome; progressive sarcoidosis with facial palsy", "Mikulicz syndrome; chronic dacryosialoadenitis requiring immunosuppression", "Sweet syndrome; acute neutrophilic dermatosis with leukemia"],
            "Löfgren syndrome is an acute, self-limiting clinical phenotype of Sarcoidosis characterized by the classic triad of: 1. Erythema nodosum; 2. Bilateral hilar lymphadenopathy (BHL) on chest X-ray; 3. Migratory polyarthritis/periarthritis (predominantly involving the ankles). It has an extraordinarily favorable prognosis, with spontaneous complete resolution in >80-90% of patients within 1 to 2 years, requiring only symptomatic treatment with NSAIDs.",
            clinical=True
        ),
        q(
            "A 56-year-old chronic alcoholic male presents with acute severe epigastric pain radiating to his back, accompanied by multiple tender, erythematous, subcutaneous nodules on his lower legs. Biopsy reveals enzymatic fat necrosis with pathognomonic 'ghost adipocytes' (anucleated adipocytes with thick, shadowy basophilic walls and calcium saponification). What is the diagnosis?",
            "Pancreatic panniculitis",
            ["Erythema nodosum", "Lupus panniculitis", "Alpha-1 antitrypsin deficiency panniculitis"],
            "Pancreatic panniculitis (pancreatitis-associated subcutaneous fat necrosis) occurs in 2-3% of patients with acute/chronic pancreatitis or acinar cell carcinoma of the pancreas. Massive release of pancreatic enzymes (lipase and amylase) into the systemic circulation causes distant enzymatic digestion of peri-articular and subcutaneous fat. Histology shows pathognomonic 'ghost cells' (necrotic adipocytes lacking nuclei with shadowy basophilic borders) and calcium deposition (saponification).",
            clinical=True
        ),
        q(
            "A 34-year-old female with systemic lupus erythematosus presents with deep, firm, non-tender subcutaneous nodules and plaques on her cheeks, upper arms, and buttocks. As the lesions slowly regress over several months, they leave behind disfiguring, deep, punched-out, saucer-like lipoatrophic depressions. What is this variant termed?",
            "Lupus panniculitis (Lupus erythematosus profundus)",
            ["Erythema nodosum", "Morphea profunda", "Lipodermatosclerosis"],
            "Lupus erythematosus profundus (lupus panniculitis) is a chronic inflammatory disorder of subcutaneous fat occurring in 2-3% of patients with SLE or discoid lupus. It characteristically affects fatty areas (cheeks, shoulders, upper arms, breasts, buttocks) as deep indurated plaques that heal with marked subcutaneous atrophy, producing permanent, unsightly cup-shaped or saucer-like depressions. Biopsy shows lobular panniculitis with hyaline fat necrosis and lymphoid follicles.",
            clinical=True
        ),
    ]),
    (16, "Adverse Drug Reactions", "hard", [
        q(
            "A 28-year-old male takes an oral tablet of Cotrimoxazole for a urinary tract infection. Twelve hours later, a solitary, well-demarcated, rounded, dusky-violaceous, burning plaque with an edematous border erupts on the glans penis. The lesion heals over 2 weeks with dense slate-gray hyperpigmentation. Six months later, he takes the same drug and the plaque flares up at the EXACT SAME anatomical site. What is the diagnosis and its immunopathogenesis?",
            "Fixed drug eruption; mediated by intraepidermal resident CD8+ T-cells",
            ["Erythema multiforme; dermal perivascular immune complex deposition", "Drug-induced urticaria; IgE-mediated mast cell degranulation", "Stevens-Johnson syndrome; systemic granulysin-mediated apoptosis"],
            "Fixed Drug Eruption (FDE) is characterized by well-demarcated, solitary or few, dusky-erythematous or violaceous round plaques that recur precisely at the same anatomical site upon re-exposure to the culprit drug (common drugs: trimethoprim-sulfamethoxazole, NSAIDs, paracetamol, tetracyclines). Pathogenesis involves quiescent intraepidermal CD8+ effector memory T cells permanently stationed in the basal epidermis at the site; upon drug re-challenge, they rapidly reactivate and release IFN-gamma and granzyme B, inducing localized basal cell apoptosis.",
            clinical=True
        ),
        q(
            "According to the Bastuji-Garin consensus classification, what threshold percentage of detached Body Surface Area (BSA) differentiates Stevens-Johnson Syndrome (SJS), SJS/TEN Overlap, and Toxic Epidermal Necrolysis (TEN)?",
            "SJS: <10% BSA; Overlap: 10-30% BSA; TEN: >30% BSA",
            ["SJS: <20% BSA; Overlap: 20-50% BSA; TEN: >50% BSA", "SJS: mucosal only; Overlap: trunk only; TEN: generalized", "SJS: <5% BSA; Overlap: 5-15% BSA; TEN: >15% BSA"],
            "SJS and TEN represent points on a clinical severity spectrum of drug-induced epidermal necrolysis characterized by full-thickness epidermal necrosis and extensive mucosal detachments: 1. Stevens-Johnson Syndrome (SJS): <10% of total body surface area (BSA) epidermal detachment; 2. SJS/TEN Overlap: 10% to 30% BSA epidermal detachment; 3. Toxic Epidermal Necrolysis (TEN / Lyell syndrome): >30% BSA epidermal detachment. Nikolsky sign is positive on erythematous areas.",
            clinical=False
        ),
        q(
            "What seven clinical and biochemical prognostic parameters assessed within the first 24 hours of hospital admission constitute the validated SCORTEN score for predicting mortality in Stevens-Johnson Syndrome and Toxic Epidermal Necrolysis?",
            "Age ≥40, heart rate ≥120, malignancy, BSA ≥10%, urea, glucose, bicarbonate",
            ["Fever, leukocytosis, elevated CRP, hypotension, thrombocytopenia, hyperbilirubinemia, hypoalbuminemia", "Male sex, obesity, previous allergy, anemia, elevated ESR, hyponatremia, hyperkalemia", "Hypothermia, neutropenia, procalcitonin, acute renal failure, hypokalemia, hyperkalemia"],
            "The SCORTEN prognostic score assigns 1 point for each of 7 independent risk factors measured within 24 hours of admission: 1. Age >= 40 years; 2. Heart rate >= 120 beats/min; 3. Presence of underlying malignancy/cancer; 4. Body surface area detached >= 10%; 5. Serum urea (BUN) > 28 mg/dL (10 mmol/L); 6. Serum glucose > 252 mg/dL (14 mmol/L); 7. Serum bicarbonate < 20 mEq/L (20 mmol/L). A score of 0-1 predicts 3% mortality, whereas a score >= 5 predicts >90% mortality.",
            clinical=False
        ),
        q(
            "Which human leukocyte antigen (HLA) allele is strongly associated with Carbamazepine-induced Stevens-Johnson Syndrome / Toxic Epidermal Necrolysis in Han Chinese and Southeast Asian populations, making pre-treatment genetic screening mandatory?",
            "HLA-B*15:02",
            ["HLA-B*58:01", "HLA-B*57:01", "HLA-B*27"],
            "Carbamazepine-induced SJS/TEN is extraordinarily linked to the HLA-B*15:02 allele in Southeast Asian populations (odds ratio >1000 in Han Chinese, Thai, and Malaysian patients). The FDA and international guidelines mandate genetic screening for HLA-B*15:02 prior to initiating carbamazepine in these ethnic groups. In comparison, HLA-B*58:01 is associated with Allopurinol-induced SJS/TEN, and HLA-B*57:01 with Abacavir hypersensitivity.",
            clinical=False
        ),
        q(
            "A 38-year-old male develops high remittent fever, facial edema, diffuse morbilliform exanthem, tender generalized lymphadenopathy, marked peripheral eosinophilia (absolute eosinophil count 2800/mcL), and marked hepatic transaminitis (ALT 650 IU/L), 4 weeks after initiating Carbamazepine for seizures. Serology demonstrates reactivation of Human Herpesvirus 6 (HHV-6). What is the diagnosis?",
            "DRESS syndrome (Drug Reaction with Eosinophilia and Systemic Symptoms)",
            ["Stevens-Johnson syndrome", "Acute generalized exanthematous pustulosis", "Infectious mononucleosis"],
            "DRESS (Drug Reaction with Eosinophilia and Systemic Symptoms / Drug-Induced Hypersensitivity Syndrome - DIHS) is a severe, life-threatening idiosyncratic reaction. Hallmark features: prolonged latency (2 to 8 weeks after starting the drug; high-risk drugs: aromatic anticonvulsants, allopurinol, sulfasalazine, dapsone), severe facial edema, diffuse maculopapular exanthem, atypical lymphocytosis, prominent eosinophilia, visceral organ damage (hepatitis in >70%, nephritis, pneumonitis), and frequent reactivation of latent HHV-6 and EBV.",
            clinical=True
        ),
        q(
            "A 45-year-old female presents with acute high fever, leukocytosis with marked neutrophilia, and the sudden eruption of hundreds of small (<5 mm), non-follicular, sterile pustules arising on a widespread edematous, fiery erythematous background, 36 hours after initiating oral Amoxicillin. Skin biopsy demonstrates subcorneal spongiform pustules packed with neutrophils and dermal edema. What is the diagnosis?",
            "Acute generalized exanthematous pustulosis (AGEP)",
            ["Pustular psoriasis of von Zumbusch", "Subcorneal pustular dermatosis (Sneddon-Wilkinson)", "DRESS syndrome"],
            "Acute Generalized Exanthematous Pustulosis (AGEP) is a severe cutaneous adverse reaction typically triggered by antibiotics (beta-lactams, macrolides, quinolones) in >80% of cases. Distinctive features: very short latency period (less than 24 to 48 hours post-ingestion), sudden onset of high fever, marked peripheral blood neutrophilia (>7000/mcL), and hundreds of tiny, discrete, non-follicular sterile pustules coalescing over flexural and intertriginous folds, rapidly resolving with desquamation within 10-14 days.",
            clinical=True
        ),
        q(
            "A 24-year-old patient taking long-term oral Minocycline for cystic acne develops a distinct blue-gray to bluish-black pigmentation localized to the anterior shins and ankles, sclerae, and mucosal alveolar ridges of the mouth. What is the mechanism of this drug-induced hyperpigmentation?",
            "Dermal accumulation of insoluble complexes of minocycline metabolites and iron/hemosiderin within macrophages",
            ["Stimulation of epidermal melanogenesis via MSH receptor upregulation", "Permanent covalent binding of minocycline to keratinocyte nuclei", "Direct extravasation of bile pigments into the stratum basale"],
            "Minocycline causes three types of cutaneous pigmentation: Type I (blue-black pigment in scars/acne lesions); Type II (blue-gray pigmentation of the anterior shins, ankles, and forearms); Type III (diffuse muddy-brown pigmentation in sun-exposed areas). Type II pigmentation is caused by dermal deposition of minocycline-iron chelates and hemosiderin-like pigment complexes engulfed by dermal macrophages and perivascular histiocytes.",
            clinical=True
        ),
        q(
            "A 62-year-old male with atrial fibrillation on long-term Amiodarone therapy complains that his skin has turned a striking slate-gray to bluish-violaceous hue on sun-exposed areas of his face and hands ('smurf skin'). What is the underlying pathology of this amiodarone-induced pigmentation?",
            "Lipofuscin and drug metabolites within lysosomal inclusion bodies",
            ["Melanin hyperproduction stimulated by alpha-MSH in basal layer", "Hemosiderin extravasation surrounding subcutaneous eccrine coils", "Silver nanoparticle precipitation along elastic fibers"],
            "Amiodarone (which contains iodine) causes two distinct dermatological side effects: acute phototoxicity (erythema, burning) in up to 50% of patients, and distinctive slate-gray to bluish-violaceous pigmentation of photo-exposed facial skin in 1-2% of patients taking high doses (>400 mg/day for >1-2 years). Histology and electron microscopy reveal yellow-brown lipofuscin granules and membrane-bound electron-dense lysosomal inclusions (myeloid bodies) within dermal macrophages.",
            clinical=True
        ),
        q(
            "A 45-year-old male receiving Phenytoin for post-traumatic epilepsy develops DRESS syndrome. Why must aromatic anticonvulsants (Phenytoin, Carbamazepine, and Phenobarbital) ALL be permanently avoided in this patient?",
            "High cross-reactivity (70-80%) due to shared arene oxide metabolites",
            ["Zero cross-reactivity due to completely unrelated aromatic ring structures", "IgE-mediated cross-reactivity directed against shared carboxamide chains", "Low cross-reactivity (<5%) confined strictly to HLA-B*1502 carriers"],
            "The aromatic anticonvulsants (phenytoin, carbamazepine, and phenobarbital) undergo hepatic cytochrome P450 oxidation to form reactive arene oxide intermediates. Normally, these toxic metabolites are rapidly detoxified by the enzyme epoxide hydrolase. Patients who develop anticonvulsant hypersensitivity syndrome harbor genetic deficiencies in epoxide hydrolase, accumulating toxic metabolites that bind cellular proteins and trigger immune attacks. Cross-reactivity between these three aromatic agents exceeds 75-80%.",
            clinical=False
        ),
        q(
            "A 58-year-old obese female receives a loading dose of oral Warfarin for deep vein thrombosis without heparin bridging. On day 4, she suddenly develops excruciatingly painful, sharply demarcated, dusky purpuric plaques with bullae that progress rapidly into full-thickness ischemic skin necrosis and gangrene over her breasts, thighs, and buttocks. What is the underlying molecular mechanism?",
            "Transient hypercoagulability from rapid initial decline of protein C",
            ["Direct endothelial necrosis caused by toxic warfarin metabolites", "Autoimmune thrombocytopenia with consumption of factor VIII", "Severe anaphylactoid vasospasm of subcutaneous dermal arterioles"],
            "Warfarin inhibits vitamin K epoxide reductase, blocking gamma-carboxylation of clotting factors II, VII, IX, X and natural anticoagulant proteins C and S. Protein C has a very short biological half-life (6 hours) compared to Factor II (prothrombin, 60-72 hours) and Factor X (40 hours). Consequently, in the first 48-72 hours of unbridged warfarin therapy, protein C activity plummets rapidly while procoagulant factors remain high, precipitating microvascular thrombosis, dermal infarction, and skin necrosis.",
            clinical=True
        ),
    ]),
    (17, "Vesiculobullous Disorders", "hard", [
        q(
            "A 42-year-old female presents with persistent, painful, non-healing erosions in her oral cavity for 4 months, followed by the eruption of flaccid, easily ruptured bullae on normal-appearing skin over the scalp, chest, and back. Lateral pressure on perilesional skin readily induces epidermal shearing (positive Nikolsky sign). What is the diagnosis and its primary autoantigen?",
            "Pemphigus vulgaris; autoantibodies targeting Desmoglein 3 (and Desmoglein 1)",
            ["Bullous pemphigoid; autoantibodies targeting BP180 and BP230", "Pemphigus foliaceus; autoantibodies targeting Desmocollin 1", "Dermatitis herpetiformis; autoantibodies targeting epidermal transglutaminase"],
            "Pemphigus vulgaris (PV) is an intraepidermal autoimmune blistering disease targeting desmosomal cadherins. Oral mucosal erosions precede cutaneous blistering in >70% of patients. Flaccid blisters rupture easily, leaving painful, weeping, raw erosions with a tendency to extend peripherally. Pathophysiology is driven by pathogenic IgG autoantibodies directed against Desmoglein 3 (mucosal-dominant PV) or both Desmoglein 3 and Desmoglein 1 (mucocutaneous PV).",
            clinical=True
        ),
        q(
            "Which histopathological hallmark confirms the diagnosis of Pemphigus Vulgaris on a punch biopsy of an intact early cutaneous vesicle?",
            "Suprabasal acantholysis with 'row of tombstones' basal cells",
            ["Subcorneal acantholytic cleavage beneath stratum corneum", "Subepidermal non-acantholytic split with intact epidermal roof", "Ballooning intraepidermal degeneration with multinucleated giant cells"],
            "In pemphigus vulgaris, autoantibodies against desmoglein 3 disrupt desmosomal bridges immediately above the basal cell layer, producing Suprabasal Acantholysis (intraepidermal blister). While spinous cells lose intercellular cohesion and round up into free-floating acantholytic Tzanck cells, basal keratinocytes remain attached to the basement membrane via intact hemidesmosomes, creating the classic 'tombstone' appearance along the blister floor.",
            clinical=False
        ),
        q(
            "What classic pattern of immunoreactivity is observed on Direct Immunofluorescence (DIF) of perilesional skin in Pemphigus Vulgaris?",
            "Intercellular epidermal IgG and C3 in fish-net pattern",
            ["Linear IgG and C3 along basement membrane zone", "Granular IgA deposition within dermal papillary tips", "Perivascular IgM and fibrinogen deposits in papillary dermis"],
            "Direct Immunofluorescence (DIF) of perilesional skin in pemphigus vulgaris shows cell-surface (intercellular substance) deposition of IgG (predominantly IgG4 subclass) and complement C3 in a characteristic reticular, honeycomb, 'fishnet' or 'chicken-wire' pattern outlining the individual keratinocyte plasma membranes throughout the entire epidermis.",
            clinical=False
        ),
        q(
            "A 50-year-old male presents with widespread superficial scaly, crusted, erythematous erosions on the face, scalp, and upper trunk resembling 'cornflakes', but has completely spared oral and genital mucous membranes. Nikolsky sign is positive. Histology shows subcorneal acantholysis. What is the diagnosis and antigenic target?",
            "Pemphigus foliaceus; anti-Desmoglein 1 autoantibodies",
            ["Pemphigus vulgaris; anti-Desmoglein 3 autoantibodies", "Bullous pemphigoid; anti-BP180 autoantibodies", "Paraneoplastic pemphigus; anti-Envoplakin autoantibodies"],
            "Pemphigus foliaceus is a superficial autoimmune blistering disease mediated by IgG autoantibodies targeting Desmoglein 1 (Dsg1) alone. Because Dsg1 is concentrated in the superficial epidermis and is minimally present in oral mucosa (where Dsg3 is abundant and compensates), mucous membranes are strictly SPARED. Blisters form subcorneally in the granular layer and rupture immediately, presenting as greasy, crusted, cornflake-like erosions.",
            clinical=True
        ),
        q(
            "A 60-year-old male with a history of Castleman disease presents with excruciating, intractable, polymorphic stomatitis with severe tongue ulceration, pseudomembranous conjunctivitis, and widespread lichenoid and bullous cutaneous lesions. Indirect immunofluorescence demonstrates autoantibodies binding to rat bladder transitional epithelium. What is the diagnosis?",
            "Paraneoplastic pemphigus (PNP)",
            ["Pemphigus vulgaris", "Stevens-Johnson syndrome", "Mucous membrane pemphigoid"],
            "Paraneoplastic Pemphigus (PNP) is a life-threatening autoimmune multi-organ syndrome associated with occult or diagnosed neoplasms (most commonly non-Hodgkin lymphoma, chronic lymphocytic leukemia, Castleman disease, and thymoma). Diagnostic hallmarks: severe, unyielding, hemorrhagic stomatitis/cheilitis, bronchiolitis obliterans, autoantibodies against the plakin family (envoplakin, periplakin) and desmogleins, and positive indirect immunofluorescence on murine bladder transitional epithelium.",
            clinical=True
        ),
        q(
            "A 76-year-old male presents with a 2-month history of intense generalized pruritus followed by the eruption of large, tense, firm blisters arising on erythematous, urticarial plaques and normal skin across his limbs and lower abdomen. Nikolsky sign is negative, and oral mucosa is uninvolved. What is the diagnosis and the primary molecular targets?",
            "Bullous pemphigoid; autoantibodies targeting BP180 (type XVII collagen) and BP230",
            ["Pemphigus vulgaris; autoantibodies targeting Desmoglein 3", "Epidermolysis bullosa acquisita; autoantibodies targeting Type VII collagen", "Dermatitis herpetiformis; autoantibodies targeting transglutaminase 3"],
            "Bullous pemphigoid (BP) is the most common autoimmune subepidermal blistering disease, classically affecting elderly patients (>70 years). Hallmarks: large, tense bullae that resist rupture (negative Nikolsky sign), often preceded by a pruritic urticarial prodrome. Pathogenesis involves autoantibodies against hemidesmosomal plaque components: BP180 (type XVII collagen, NC16A domain) and BP230 (dystonin), inciting complement activation, eosinophil recruitment, and subepidermal cleavage.",
            clinical=True
        ),
        q(
            "What direct immunofluorescence (DIF) pattern and salt-split skin localization definitively characterize Bullous Pemphigoid?",
            "Linear basement membrane IgG binding the epidermal roof side",
            ["Granular basement membrane IgA binding dermal floor", "Linear basement membrane IgG binding dermal floor", "Intercellular epidermal IgG binding both roof and floor"],
            "DIF of perilesional skin in Bullous Pemphigoid demonstrates smooth, continuous, linear deposition of IgG and C3 along the dermo-epidermal junction (BMZ). When serum is incubated on 1M NaCl-split normal human skin (which separates the skin within the lamina lucida), BP autoantibodies bind to the EPIDERMAL ROOF of the split (where the NC16A domain of BP180 resides), distinguishing BP from Epidermolysis Bullosa Acquisita (which binds to the DERMAL FLOOR).",
            clinical=False
        ),
        q(
            "A 32-year-old male with chronic diarrhea and weight loss presents with severe, burning, intensely pruritic, grouped (herpetiform) vesicles and excoriations symmetrically distributed over both elbows, knees, buttocks, and upper back. Biopsy of an early lesion reveals subepidermal clefting with neutrophilic microabscesses at the tips of dermal papillae. What is the diagnosis?",
            "Dermatitis herpetiformis (Duhring disease)",
            ["Bullous pemphigoid", "Linear IgA bullous dermatosis", "Scabies"],
            "Dermatitis herpetiformis (Duhring disease) is an intensely pruritic cutaneous manifestation of celiac disease (gluten-sensitive enteropathy). Hallmarks: bilateral, symmetrical, grouped polymorphic vesicles, papules, and urticarial wheals over extensor surfaces (elbows, knees, buttocks, scalp). Intractable burning pruritus leads to rapid excoriation. Biopsy reveals neutrophilic microabscesses filling dermal papillae tips.",
            clinical=True
        ),
        q(
            "What pathognomonic Direct Immunofluorescence (DIF) finding confirms Dermatitis Herpetiformis, and what is the definitive first-line pharmacological treatment of choice combined with a strict gluten-free diet?",
            "Granular deposition of IgA clustered at the tips of dermal papillae; Dapsone",
            ["Linear IgG along the basement membrane zone; Oral Prednisolone", "Intercellular IgG throughout the epidermis; Azathioprine", "Linear IgA along the basement membrane; Mycophenolate mofetil"],
            "DIF of perilesional normal-appearing skin in Dermatitis Herpetiformis shows pathognomonic granular deposits of IgA (targeting epidermal transglutaminase - eTG) clustered within the apices of dermal papillae. Dapsone is the drug of choice, dramatically relieving the excruciating pruritus and aborting new vesicle formation within 24 to 48 hours. A strict, life-long gluten-free diet is essential to heal the intestinal enteropathy and eventually allow tapering off dapsone.",
            clinical=False
        ),
        q(
            "A 40-year-old female presents with recurrent, tense subepidermal blisters over trauma-prone extensor surfaces (dorsa of hands, knuckles, elbows, knees) that heal with prominent atrophic scarring and milia formation. Direct immunofluorescence demonstrates linear IgG along the basement membrane, which localizes exclusively to the DERMAL (floor) side of salt-split skin. What is the diagnosis and antigenic target?",
            "Epidermolysis bullosa acquisita (EBA); autoantibodies targeting Type VII collagen (anchoring fibrils)",
            ["Bullous pemphigoid; autoantibodies targeting BP180", "Pemphigus vulgaris; autoantibodies targeting Desmoglein 3", "Mucous membrane pemphigoid; autoantibodies targeting Laminin 332"],
            "Epidermolysis Bullosa Acquisita (EBA) is an acquired mechanobullous disease characterized by extreme skin fragility and tense blisters at friction sites that heal with scarring and milia, mimicking dystrophic epidermolysis bullosa. Autoantibodies target Type VII collagen, the primary constituent of anchoring fibrils in the sublamina densa. On salt-split skin, EBA autoantibodies map to the DERMAL FLOOR of the split, whereas BP autoantibodies map to the epidermal roof.",
            clinical=True
        ),
    ]),
]
