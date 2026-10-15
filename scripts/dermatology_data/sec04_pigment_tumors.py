from .common import q

CHAPTERS = [
    (18, "Disorders of Skin Pigmentation", "hard", [
        q(
            "A 28-year-old female presents with completely depigmented, chalky-white, asymptomatic macules and patches with sharply defined, scalloped margins around her mouth, eyes, dorsal hands, and elbows. Skin biopsy of the chalky-white macule stained with Fontana-Masson and DOPA reaction demonstrates total absence of epidermal melanocytes. What is the diagnosis, and which systemic disease is most frequently associated?",
            "Vitiligo; Autoimmune thyroid disease (Hashimoto thyroiditis / Graves disease)",
            ["Pityriasis alba; Type 1 diabetes mellitus", "Albinism; Celiac disease", "Post-inflammatory hypopigmentation; Rheumatoid arthritis"],
            "Vitiligo is an acquired, autoimmune destruction of functional epidermal and follicular melanocytes resulting in well-demarcated amelanotic (chalky-white) macules. Biopsy shows complete absence of melanocytes and melanin in the basal layer. Over 20-30% of vitiligo patients harbor coexisting autoimmune conditions, with autoimmune thyroiditis (Hashimoto's or Graves' disease) being by far the most prevalent, warranting routine screening of TSH and anti-TPO antibodies.",
            clinical=True
        ),
        q(
            "Which clinical characteristic definitively distinguishes Segmental Vitiligo from Non-Segmental (Generalized) Vitiligo?",
            "Unilateral dermatomal distribution, childhood onset, early stabilization, surgical graft responsiveness",
            ["Symmetrical bilateral distribution, adult onset, and rapid corticosteroid response", "Mucosal-only distribution, frequent spontaneous repigmentation, and malignancy risk", "Generalized symmetric distribution, Hashimoto association, and phototherapy response"],
            "Segmental vitiligo (accounting for 5-16% of vitiligo): 1. Unilateral, quasi-dermatomal band-like distribution that does not cross the midline; 2. Early onset (typically in children); 3. Rapid progression over 6-24 months followed by lifelong arrest and stability; 4. Poliosis (hair whitening) is early and common; 5. Associated with minimal systemic autoimmunity; 6. Highly resistant to medical therapy/phototherapy, but the ideal candidate for autologous non-cultured epidermal cell suspension grafting.",
            clinical=False
        ),
        q(
            "A 34-year-old woman in her third trimester of pregnancy presents with symmetrical, reticulated, light-to-dark brown macules and patches with irregular borders over her forehead, malar eminences, upper lip, and chin (centrofacial pattern). Examination under Wood's light shows no enhancement of the pigment contrast, indicating deep dermal melanin deposition. What is the diagnosis and the standard first-line 'triple combination' topical regimen?",
            "Melasma; modified Kligman triple combination topical formula",
            ["Post-inflammatory hyperpigmentation; clobetasol propionate monotherapy", "Lichen planus pigmentosus; high-dose oral dapsone monotherapy", "Acanthosis nigricans; topical salicylic acid keratolytic ointment"],
            "Melasma (chloasma / mask of pregnancy) is an acquired symmetric hyperpigmentation of sun-exposed areas of the face, exacerbated by UV radiation, genetic factors, estrogen, and progesterone. The gold-standard topical therapy is the modified Kligman triple combination cream: Hydroquinone 4% (tyrosinase inhibitor), Tretinoin 0.05% (enhances penetration and epidermal turnover), and Fluocinolone acetonide 0.01% (reduces irritation and cellular melanogenesis).",
            clinical=True
        ),
        q(
            "What enzymatic defect is responsible for Oculocutaneous Albinism Type 1 (OCA1), an autosomal recessive disorder characterized by complete lifelong absence of melanin in the skin, hair, and eyes, severe photophobia, nystagmus, and high susceptibility to Squamous Cell Carcinoma?",
            "Complete deficiency of Tyrosinase (encoded by the TYR gene on chromosome 11q14)",
            ["Deficiency of P-protein (OCA2 gene)", "Deficiency of Tyrosinase-related protein-1 (TYRP1 gene)", "Deficiency of SLC45A2 (MATP gene)"],
            "Oculocutaneous Albinism Type 1 (OCA1) is caused by autosomal recessive loss-of-function mutations in the TYR gene on chromosome 11q14, which encodes the copper-containing enzyme tyrosinase. Tyrosinase catalyzes the initial, rate-limiting steps of melanogenesis: conversion of L-tyrosine to L-DOPA and dopaquinone. In OCA1A (tyrosinase-negative albinism), complete absence of tyrosinase activity results in snow-white hair, pink-white skin, translucent blue irides, and severe photophobia.",
            clinical=False
        ),
        q(
            "A patient with resolved severe lichen planus presents with persistent, slate-gray to bluish-brown macules on his ankles that have failed to fade over 12 months. Biopsy demonstrates 'pigmentary incontinence'. What cellular and architectural process produces this histological finding?",
            "Basal liquefaction causing melanin incontinence into papillary dermal melanophages",
            ["Increased melanosome transfer from hyperactive melanocytes to spinous keratinocytes", "Aberrant migration of neural crest melanocytes into reticular dermis", "Erythrocyte extravasation with progressive breakdown and dermal hemosiderin deposition"],
            "Pigmentary incontinence (pigment drop-out) is a classic histological sequel of interface dermatitis (seen in lichen planus, lupus erythematosus, fixed drug eruption). Immunological attack on the basal cell layer destroys basal keratinocytes; their stored melanin granules escape and spill downward into the papillary dermis. Dermal histiocytes phagocytose the free pigment, transforming into 'melanophages'. Dermal melanin scatters blue light (Tyndall effect), producing an indelible slate-gray discoloration that responds poorly to bleaching agents.",
            clinical=True
        ),
        q(
            "A female neonate is born with crops of linear, inflammatory vesicles and pustules distributed along the lines of Blaschko on her limbs, accompanied by marked peripheral blood eosinophilia. Over the next 18 months, the rash evolves through a verrucous hyperkeratotic stage, culminating in bizarre, swirled, marbled, reticulated hyperpigmentation ('fountain-pen splash' pattern) on the trunk. What is this X-linked dominant condition, and which gene is mutated?",
            "Incontinentia pigmenti (Bloch-Sulzberger syndrome); IKBKG (NEMO) gene mutation",
            ["Hypomelanosis of Ito; MTOR gene mutation", "Neurofibromatosis type 1; NF1 gene mutation", "Tuberous sclerosis; TSC1 gene mutation"],
            "Incontinentia Pigmenti (IP / Bloch-Sulzberger syndrome) is an X-linked dominant genodermatosis that is lethal in males in utero, caused by mutations in the IKBKG (NEMO) gene encoding the NF-kappa-B essential modulator. The cutaneous phenotype progresses through 4 classic chronological stages following Blaschko's lines: Stage 1 (vesiculobullous with eosinophilia); Stage 2 (verrucous hyperkeratotic); Stage 3 (swirled, marbled hyperpigmentation); Stage 4 (pale, hairless, hypopigmented atrophic streaks).",
            clinical=True
        ),
        q(
            "An 8-year-old atopic boy presents with multiple poorly demarcated, round, hypopigmented macules with fine, powdery, branny scales on both cheeks that become strikingly more noticeable after summer outdoor activities. What is the diagnosis?",
            "Pityriasis alba",
            ["Tinea versicolor", "Vitiligo", "Indeterminate leprosy"],
            "Pityriasis alba is a mild, low-grade, superficial eczematous dermatosis occurring predominantly in atopic children on the face (especially cheeks). Hallmarks: round or oval, ill-defined, hypopigmented macules covered by fine, furfuraceous, powdery scales. Lesions become more noticeable in summer because the hypopigmented areas (which have reduced melanin synthesis and impaired melanosome transfer secondary to chronic micro-inflammation) fail to tan compared to surrounding healthy skin.",
            clinical=True
        ),
        q(
            "A 22-year-old female presents with congenital, asymptomatic, unilateral, mottled, slate-gray or blue-black coalescent macules involving the left temple, forehead, periorbital skin, and the ipsilateral sclera of her left eye. What is this dermal melanocytosis termed, and along which cranial nerve distribution does it lie?",
            "Nevus of Ota; trigeminal nerve V1 and V2 divisions",
            ["Nevus of Ito; supraclavicular and lateral brachial nerves", "Mongolian spot; lumbosacral nerve roots L2 to S2", "Blue nevus; terminal digital sensory branches of radial nerve"],
            "Nevus of Ota (nevus fuscocaeruleus ophthalmomaxillaris) is an aberrant dermal melanocytosis characterized by persistent, non-regressing, blue-gray or slate-colored pigmentation. It involves the skin and mucous membranes innervated by the first (V1) and second (V2) divisions of the trigeminal nerve, characteristically including the ipsilateral sclera (in two-thirds of cases), conjunctiva, cornea, and tympanic membrane.",
            clinical=True
        ),
        q(
            "A 42-year-old female with systemic sclerosis presents with a distinctive 'salt-and-pepper' pigmentary pattern on her forehead, upper chest, and neck. What precise anatomical preservation of pigment produces this appearance?",
            "Confetti leukoderma with selective perifollicular pigment preservation",
            ["Uniform chalky-white depigmentation with universal poliosis", "Reticular slate-gray macular hyperpigmentation sparing flexures", "Annular depigmented plaques with elevated erythematous borders"],
            "The 'salt-and-pepper' sign (diffuse cutaneous depigmentation with perifollicular pigment retention) is a classic cutaneous hallmark of Systemic Sclerosis (Scleroderma). Autoimmune destruction causes generalized vitiligo-like depigmentation of interfollicular skin, but the melanocytes located in the deep hair follicle bulb and outer root sheath are protected and survive, retaining their pigment and producing discrete dots of brown pigment on a white background.",
            clinical=True
        ),
        q(
            "What physiological and optical physical phenomenon explains why deep dermal melanin collections (such as in Mongolian spots, blue nevi, and Nevus of Ota) appear distinctly bluish-gray to the human eye, despite melanin being a brown-black polymer?",
            "Tyndall effect; preferential dermal backscattering of shorter blue wavelengths",
            ["Rayleigh scattering by atmospheric gases reflecting off skin", "Raman scattering induced by intracellular melanosome vibrations", "Fluorescence emission triggered by endogenous cutaneous porphyrins"],
            "The blue-gray color of dermal melanocytic lesions (Mongolian spots, Blue nevi, Nevus of Ota) is an optical illusion governed by the Tyndall effect: When white light enters human skin, longer wavelengths (red, yellow) penetrate into the deep dermis and are absorbed by the deeply situated melanin. In contrast, shorter wavelengths (blue light) are scattered sideways and reflected backward to the observer's eye by collagen bundles, causing dark brown melanin to appear distinctly slate-blue.",
            clinical=False
        ),
    ]),
    (19, "Benign and Malignant Tumors", "hard", [
        q(
            "A 65-year-old fair-skinned male presents with a solitary, slowly enlarging, pearly, translucent papule with prominent arborizing telangiectasias and rolled, beaded borders on his left temple. Over the past 6 months, the center has ulcerated, forming a crusted 'rodent ulcer'. What is the diagnosis and the most characteristic histopathological feature on biopsy?",
            "Basal cell carcinoma; basaloid lobules with peripheral palisading",
            ["Squamous cell carcinoma; atypical keratinocytes forming keratin pearls", "Malignant melanoma; atypical melanocytes in upward pagetoid scatter", "Seborrheic keratosis; benign acanthosis with intraepidermal horn pseudocysts"],
            "Basal Cell Carcinoma (BCC) is the most common cutaneous malignancy, derived from non-keratinizing cells in the basal layer of the interfollicular epidermis or hair follicle outer root sheath. Cardinal histopathology: nests/islands of uniform, basophilic basaloid cells with hyperchromatic nuclei, prominent peripheral palisading (nuclei aligned like fence pickets at the margin of nests), and artifactual retraction clefting (stromal-epithelial separation) from specialized mucinous stroma.",
            clinical=True
        ),
        q(
            "A 70-year-old farmer presents with a firm, non-healing, indurated, hyperkeratotic, ulcerated nodule with everted borders on the vermilion border of his lower lip that bleeds upon minor trauma. Biopsy reveals invasive atypical squamous keratinocytes invading deeply into the dermis, intercellular bridges (desmosomes), and concentric laminated whorls of eosinophilic keratin. What are these diagnostic laminated structures termed?",
            "Keratin pearls (horn pearls)",
            ["Munro microabscesses", "Henderson-Paterson bodies", "Russell bodies"],
            "Keratin pearls (epithelial pearls / horn pearls) are pathognomonic histopathological features of well-differentiated Cutaneous Squamous Cell Carcinoma (SCC). They represent concentric, onion-skin-like laminated nests of keratinizing atypical squamous cells with dyskeratosis, intercellular bridges, and central densely packed eosinophilic keratin flakes invading into the dermis.",
            clinical=True
        ),
        q(
            "In the clinical evaluation of pigmented cutaneous lesions for suspected Cutaneous Malignant Melanoma, what clinical criteria constitute the validated 'ABCDE' rule?",
            "Asymmetry, Border irregularity, Color variegation, Diameter >6mm, Evolving",
            ["Acanthosis, Blistering, Crust formation, Depth >1cm, Exudation", "Annular configuration, Brown pigmentation, Central clearing, Desquamation, Erythema", "Age over 50, Basaloid proliferation, Capillary loops, Dimpling, Elevation"],
            "The ABCDE mnemonic is the cardinal clinical screening criteria for Cutaneous Melanoma: A: Asymmetry (one half does not match the other half); B: Border irregularity (notched, scalloped, ragged, or blurred borders); C: Color variegation (shades of tan, brown, black, with red, white, or blue); D: Diameter (>6 mm, the size of a pencil eraser); E: Evolving (any dynamic change in size, shape, color, surface texture, bleeding, or itching over time).",
            clinical=False
        ),
        q(
            "According to the American Joint Committee on Cancer (AJCC) staging manual for primary Cutaneous Malignant Melanoma, what is the single most important histological prognostic factor that dictates surgical excision margins and sentinel lymph node biopsy indications?",
            "Breslow tumor thickness in millimeters from stratum granulosum",
            ["Clark anatomical level of cutaneous invasion", "Presence or absence of macroscopic ulceration", "Mitotic rate per square millimeter in dermis"],
            "Breslow thickness is the absolute gold-standard, most critical independent prognostic indicator in primary cutaneous melanoma. It is measured objectively in millimeters from the top of the granular layer of the epidermis (or base of ulcer if ulcerated) to the deepest point of tumor penetration into the dermis/subcutis. It directly determines surgical safety margins (e.g., 1 cm margin for depth <=1.0 mm; 2 cm margin for depth >2.0 mm) and triggers sentinel lymph node biopsy (indicated when depth >=0.8 mm or ulcerated).",
            clinical=False
        ),
        q(
            "A 68-year-old male presents with dozens of asymptomatic, well-circumscribed, brownish-black, greasy, warty plaques with a characteristic 'stuck-on' appearance scattered across his back and chest. Dermoscopy reveals horn pseudocysts and crypt-like openings. What is the diagnosis?",
            "Seborrheic keratosis",
            ["Malignant melanoma", "Pigmented basal cell carcinoma", "Actinic keratosis"],
            "Seborrheic keratosis (verruca seborrhoica / senile wart) is the most common benign cutaneous neoplasm of older adults. Lesions look as if they have been 'stuck onto' or 'pasted onto' the skin surface. Hallmark histology: hyperkeratosis, acanthosis, papillomatosis, and pathognomonic intraepidermal horn pseudocysts (invaginations of stratum corneum filled with concentric laminated keratin).",
            clinical=True
        ),
        q(
            "An 80-year-old male with sudden weight loss develops a sudden, explosive eruption of hundreds of intensely pruritic, eruptive Seborrheic Keratoses across his back and trunk within a 6-week period. What is this clinical phenomenon termed, and of which internal malignancy is it a classic cutaneous paraneoplastic sign?",
            "Sign of Leser-Trélat; Gastric adenocarcinoma",
            ["Crowe sign; Pheochromocytoma", "Trousseau sign; Glioblastoma", "Sister Mary Joseph sign; Ovarian cancer alone"],
            "The Sign of Leser-Trélat is a rare, cutaneous paraneoplastic syndrome characterized by the sudden, rapid outbreak of multiple, pruritic seborrheic keratoses on the trunk, often associated with acanthosis nigricans. It is triggered by tumor secretion of epidermal growth factor (EGF) or transforming growth factor-alpha (TGF-alpha). In over 60-70% of cases, it signals an underlying occult, aggressive internal visceral adenocarcinoma (most frequently Gastric Adenocarcinoma).",
            clinical=True
        ),
        q(
            "A 62-year-old male presents with a rapidly growing, solitary, firm, dome-shaped, flesh-colored nodule with a central, crater-like crater filled with a thick, hard keratin plug on his sun-exposed forearm, which grew from a tiny papule to 2.5 cm over just 4 weeks. What is the diagnosis?",
            "Keratoacanthoma",
            ["Basal cell carcinoma", "Dermatofibroma", "Nodular melanoma"],
            "Keratoacanthoma (KA) is a low-grade cutaneous neoplasm closely related to Squamous Cell Carcinoma that characteristically arises on sun-damaged skin of elderly individuals. Cardinal feature: explosive rapid growth over 4 to 8 weeks into a symmetric, volcanic dome-shaped nodule with a central crateriform core filled with a dense, friable keratin plug, followed in many cases by spontaneous slow regression over months leaving a depressed scar.",
            clinical=True
        ),
        q(
            "A 54-year-old male presents with chronic, itchy, scaly erythematous patches and indurated plaques in a non-sun-exposed 'bathing-trunk' distribution that have progressed over 10 years. Skin biopsy demonstrates epidermotropism of atypical lymphoid cells with hyperconvoluted, grooved nuclei that cluster together within the epidermis without spongiosis. What are these intraepidermal T-cell clusters termed?",
            "Pautrier microabscesses in Mycosis Fungoides",
            ["Munro microabscesses in Psoriasis", "Civatte bodies in Lichen Planus", "Schaumann bodies in Sarcoidosis"],
            "Mycosis Fungoides (MF) is the most common Cutaneous T-Cell Lymphoma (CTCL), classically progressing through patch, plaque, and tumor stages. Cardinal histopathological features: 1. Epidermotropism (malignant CD4+ T-lymphocytes migrating into the epidermis with a characteristic clear perinuclear halo, despite minimal or absent epidermal spongiosis); 2. Pautrier microabscesses (small, diagnostic intraepidermal clusters of atypical T-cells with cerebriform nuclei); 3. Band-like papillary dermal infiltrate.",
            clinical=True
        ),
        q(
            "A 32-year-old female presents with a firm, solitary, asymptomatic, brownish-tan, button-like dermal nodule on her right pretibial shin. When the examiner pinches the skin on either side of the lesion between thumb and index finger, the nodule retracts downward, producing a central depression ('positive dimple sign'). What is the diagnosis?",
            "Dermatofibroma (Benign fibrous histiocytoma)",
            ["Nodular melanoma", "Dermatofibrosarcoma protuberans", "Keloid"],
            "Dermatofibroma (benign fibrous histiocytoma) is a common, benign fibrohistiocytic proliferation in the dermis, typically presenting on the lower extremities of young adult females (often following an insect bite or minor folliculitis). The 'dimple sign' (lateral pinch sign) is characteristic: lateral compression of the lesion between the thumb and forefinger causes the tethered overlying epidermis to puck downwards, producing a central depression.",
            clinical=True
        ),
        q(
            "A 72-year-old fair-skinned male presents with a rapidly growing, painless, firm, violaceous-red, non-ulcerating solitary nodule on his sun-damaged cheek. Biopsy reveals small, round blue cells with neuroendocrine features that stain positive for Cytokeratin 20 (CK20) in a pathognomonic perinuclear dot-like pattern, while negative for Thyroid Transcription Factor-1 (TTF-1). What is the diagnosis?",
            "Merkel cell carcinoma",
            ["Basal cell carcinoma", "Cutaneous Ewing sarcoma", "Melanoma"],
            "Merkel Cell Carcinoma (MCC) is an extraordinarily aggressive primary cutaneous neuroendocrine carcinoma driven by the Merkel Cell Polyomavirus (MCPyV) in >80% of cases. Clinical features are summarized by the AEIOU acronym: Asymptomatic, Expanding rapidly, Immune suppressed, Older (>50 years), UV-exposed site. Pathognomonic immunohistochemical hallmark: punctate, perinuclear dot-like cytoplasmic staining for Cytokeratin 20 (CK20), with negativity for TTF-1 (excluding metastatic small-cell lung cancer).",
            clinical=True
        ),
    ]),
]
