from .common import q

CHAPTERS = [
    # Section I: Introduction to Skin Disorders (10 questions)
    # Topic 1: Structure and Function of Skin (Non-important - 5 questions)
    (1, "Structure and Function of Skin", "easy", [
        q(
            "Which pair of keratins is specifically synthesized by dividing basal keratinocytes in the stratum basale, and mutations in which are directly implicated in Epidermolysis Bullosa Simplex?",
            "Keratin 5 and Keratin 14",
            ["Keratin 1 and Keratin 10", "Keratin 2e and Keratin 9", "Keratin 6 and Keratin 16"],
            "Basal keratinocytes synthesize the basic/acidic keratin pair K5 and K14. As keratinocytes exit the basal layer and differentiate into the spinous and granular layers, they downregulate K5/K14 and upregulate Keratin 1 and Keratin 10. Missense mutations in K5 or K14 lead to structural fragility of the basal layer, manifesting as intraepidermal friction blistering in Epidermolysis Bullosa Simplex.",
            clinical=False
        ),
        q(
            "A neonate presents with severe widespread blistering and extensive mucosal erosions at friction-prone sites within hours of delivery. Transmission electron microscopy reveals tissue separation occurring precisely within the lamina lucida of the basement membrane zone. Which adhesion molecule is defective in this junctional variant of epidermolysis bullosa?",
            "Laminin-332 (Laminin 5)",
            ["Collagen Type VII", "Desmoglein 1", "Keratin 14"],
            "Junctional Epidermolysis Bullosa (JEB, including Herlitz type) is characterized by plane of cleavage through the lamina lucida of the basement membrane zone (BMZ). It is caused by genetic mutations in laminin-332 (formerly laminin 5), alpha-6 beta-4 integrin, or collagen XVII (BP180). In contrast, cleavages in EBS occur in the basal cell cytoplasm (K5/K14), while dystrophic EB involves collagen VII anchoring fibrils in the sublamina densa.",
            clinical=True
        ),
        q(
            "What is the primary epidermal distribution and desmosomal target of autoantibodies in Pemphigus Foliaceus versus mucosal-dominant Pemphigus Vulgaris according to the desmoglein compensation hypothesis?",
            "Pemphigus foliaceus targets desmoglein 1; mucosal pemphigus vulgaris targets desmoglein 3",
            ["Pemphigus foliaceus targets desmoglein 3; mucosal pemphigus vulgaris targets desmoglein 1", "Pemphigus foliaceus targets BP180; mucosal pemphigus vulgaris targets desmocollin 2", "Pemphigus foliaceus targets envoplakin; mucosal pemphigus vulgaris targets periplakin"],
            "Desmoglein 1 (Dsg1) is expressed predominantly in the superficial layers of the epidermis and minimally in mucous membranes. Desmoglein 3 (Dsg3) is heavily expressed throughout the mucosal epithelium and basal/parabasal epidermis. In pemphigus foliaceus, anti-Dsg1 autoantibodies produce subcorneal intraepidermal blistering without mucosal involvement. In mucosal-dominant pemphigus vulgaris, anti-Dsg3 antibodies cause mucosal blistering while skin is spared because cutaneous Dsg1 compensates.",
            clinical=False
        ),
        q(
            "A 24-year-old male presents with severe skin hyperextensibility, velvety skin texture, generalized joint hypermobility, and prominent atrophic 'cigarette-paper' (papyraceous) scars over bony prominences. Genetic analysis reveals an autosomal dominant mutation affecting the COL5A1 gene. Which component of the extracellular matrix is structurally impaired?",
            "Type V collagen",
            ["Type I collagen", "Type III collagen", "Fibrillin-1"],
            "Classical Ehlers-Danlos Syndrome (EDS types I and II) is an autosomal dominant connective tissue disorder caused by mutations in the COL5A1 and COL5A2 genes encoding Type V collagen. Type V collagen regulates the fibril diameter and assembly of Type I collagen. Impairment results in mechanical fragility, hyperextensible skin, poor wound healing with widening papyraceous scars, and articular hypermobility.",
            clinical=True
        ),
        q(
            "What biochemical precursor protein located within keratohyalin granules of the stratum granulosum is enzymatically processed into natural moisturizing factor (NMF) and urocanic acid to preserve epidermal barrier hydration and UV protection?",
            "Profilaggrin",
            ["Involucrin", "Loricrin", "Transglutaminase-1"],
            "Profilaggrin is a giant, phosphorylated histidine-rich precursor packed within keratohyalin granules in the stratum granulosum. During cornification, it is dephosphorylated and cleaved into filaggrin monomers that aggregate keratin filaments into dense macrofibrils. Filaggrin is subsequently degraded into hygroscopic amino acids forming the Natural Moisturizing Factor (NMF) and trans-urocanic acid, which provides endogenous photoprotection.",
            clinical=False
        ),
    ]),

    # Topic 2: Diagnosis of Skin Disorders (Non-important - 5 questions)
    (2, "Diagnosis of Skin Disorders", "easy", [
        q(
            "A 46-year-old male presents with widespread flaccid, easily ruptured blisters on normal-appearing skin and painful oral erosions. When gentle tangential pressure with a finger is applied to normal-appearing perilesional skin, the epidermis slides and shears off easily from the dermis. What is this clinical sign, and what underlying mechanism produces it?",
            "Positive Nikolsky sign; caused by loss of intraepidermal cell-cell adhesion (acantholysis)",
            ["Positive Asboe-Hansen sign; caused by hydrostatic pressure dissecting subepidermal fluid", "Positive Darier sign; caused by localized mast cell degranulation", "Positive Auspitz sign; caused by elongation of dermal papillae"],
            "Nikolsky sign is elicited by applying firm, sliding tangential pressure to normal-appearing skin adjacent to a blister. A positive result (epidermal sloughing) indicates acantholysis—loss of cohesion between keratinocytes due to autoantibodies against desmogleins (Pemphigus vulgaris) or exfoliative toxins cleaving Dsg1 (SSSS, Ritter disease). It is negative in subepidermal blistering disorders like bullous pemphigoid.",
            clinical=True
        ),
        q(
            "An 8-month-old infant is brought with multiple brownish, hyperpigmented macules on the trunk. When the examiner firmly rubs one of the lesions with the blunt end of a pen, the macule promptly becomes red, edematous, and develops a palpable, pruritic wheal within minutes. What is this pathognomonic diagnostic sign?",
            "Darier sign",
            ["Nikolsky sign", "Auspitz sign", "Crowe sign"],
            "Darier's sign is pathognomonic of cutaneous mastocytosis (urticaria pigmentosa). Stroking, rubbing, or scratching a lesion induces physical trauma that triggers immediate degranulation of clustered mast cells in the dermis, releasing histamine and leukotrienes that cause localized wheal-and-flare formation with intense erythema and pruritus.",
            clinical=True
        ),
        q(
            "A 32-year-old male presents with sharply demarcated erythematous plaques covered by thick, silvery-white micaceous scales over both elbows and knees. Grasping and scratching away the scales layer by layer reveals a shiny glistening membrane, removal of which immediately produces multiple pinpoint bleeding droplets. What is this clinical phenomenon?",
            "Auspitz sign",
            ["Brocq sign", "Koebner phenomenon", "Wickham striae"],
            "Auspitz sign is elicited in psoriasis vulgaris by scraping off the silvery scales: 1. Candle grease sign (scales peel off in layers like candle wax); 2. Membrane of Bulkeley (peeling reveals a transparent, thin moist membrane); 3. Auspitz sign: Peeling this membrane exposes elongated, tortuous dermal capillaries inside thinned suprapapillary dermal plates, producing pinpoint punctate bleeding droplets.",
            clinical=True
        ),
        q(
            "Which constellation of dermoscopic features strongly favors a diagnosis of pigmented Basal Cell Carcinoma (BCC) over Cutaneous Malignant Melanoma?",
            "Arborizing telangiectasias, blue-gray ovoid nests, and maple-leaf-like areas",
            ["Atypical pigment network, pseudopods, and blue-white veil", "Uniform cobblestone pattern with comma vessels", "Central white scar-like patch with hairpin vessels and hyperkeratotic halos"],
            "Dermoscopy of pigmented BCC is characterized by the absence of a melanocytic pigment network and the presence of specific vascular and pigmentary criteria: 1. Arborizing (tree-like branching) telangiectasias; 2. Large blue-gray ovoid nests; 3. Multiple blue-gray globules; 4. Leaf-like (maple-leaf) pigmented structures; 5. Spoke-wheel areas and ulceration. In contrast, atypical pigment network, irregular dots/globules, and blue-white veils signify melanoma.",
            clinical=False
        ),
        q(
            "A 28-year-old male with active cutaneous lichen planus accidentally scratches his left forearm on a thorny plant. Seven days later, a linear crop of shiny, violaceous, polygonal, pruritic papules erupts precisely along the scratch mark. What is this dermatological phenomenon?",
            "Koebner isomorphic response",
            ["Reverse Koebner phenomenon", "Wolf isotopic response", "Pathergy phenomenon"],
            "The Koebner phenomenon (isomorphic response) is the appearance of typical new lesions of a pre-existing dermatosis at sites of uninvolved skin following non-specific physical trauma (linear scratches, abrasions, surgical incisions). It is characteristically positive in Lichen Planus, Psoriasis vulgaris, and Vitiligo. Pathergy (sterile pustule following a needle prick) is seen in Behcet disease and Pyoderma gangrenosum.",
            clinical=True
        ),
    ]),
]
