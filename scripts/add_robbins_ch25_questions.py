import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Skin"
BASE = {"subjectId": "pathology", "subjectTitle": "Pathology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(difficulty, prompt, answer, distractors, explanation):
    if difficulty not in {"easy", "moderate", "high"}:
        raise ValueError(difficulty)
    options = [answer, *distractors]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {"difficulty": difficulty, "prompt": prompt, "options": options, "answerIndex": 0, "answer": answer, "explanation": explanation}


def jumble(question, desired_index):
    answer = question["answer"]
    distractors = [option for option in question["options"] if option != answer]
    options = distractors[:]
    options.insert(desired_index, answer)
    question["options"] = options
    question["answerIndex"] = desired_index
    return question


TOPICS = [
    ("reaction-patterns", "Skin Structure and Basic Reaction Patterns", [
        q("easy", "The outermost layer of skin is the:", "Epidermis", ["Dermis", "Hypodermis", "Fascia"], "The epidermis is the superficial keratinizing epithelium."),
        q("easy", "Spongiosis means intercellular edema in the:", "Epidermis", ["Subcutis", "Bone marrow", "Cartilage"], "Spongiosis is epidermal intercellular edema."),
        q("easy", "Acanthosis means thickening of the:", "Epidermis", ["Adrenal cortex", "Renal pelvis", "Bone cortex"], "Acanthosis is epidermal hyperplasia."),
        q("moderate", "Hyperkeratosis refers to thickening of the:", "Stratum corneum", ["Basal lamina only", "Dermal collagen only", "Subcutaneous fat"], "Hyperkeratosis is increased keratin layer."),
        q("moderate", "Parakeratosis means retained nuclei in:", "Stratum corneum", ["Dermal vessels", "Melanocytes", "Adipocytes"], "Parakeratosis reflects abnormal keratinization."),
        q("moderate", "Interface dermatitis primarily injures:", "Basal keratinocytes", ["Eccrine ducts only", "Adipocytes only", "Hair shafts"], "Interface dermatitis targets the dermoepidermal junction."),
        q("moderate", "Acantholysis means loss of cohesion between:", "Keratinocytes", ["Adipocytes", "Melanocytes and nerves", "Endothelial cells only"], "Acantholysis causes intraepidermal blistering."),
        q("high", "A skin biopsy from an itchy eczematous plaque shows widened spaces between epidermal keratinocytes with lymphocytes migrating into the epidermis. Which reaction pattern is present?", "Spongiotic dermatitis", ["Interface dermatitis", "Granulomatous dermatitis", "Panniculitis"], "Spongiosis is epidermal intercellular edema typical of eczema."),
        q("high", "A biopsy shows basal keratinocyte damage, apoptotic Civatte bodies, pigment incontinence, and lymphocytes hugging the dermoepidermal junction. Which broad inflammatory reaction pattern is described?", "Interface dermatitis", ["Spongiotic dermatitis", "Bullous pemphigoid", "Lobular panniculitis"], "Interface dermatitis involves injury along the dermoepidermal junction."),
        q("high", "An intraepidermal blister forms because keratinocytes lose desmosomal adhesion and round up into free-floating cells within the epidermis. Which microscopic process is this called?", "Acantholysis", ["Spongiosis", "Papillomatosis", "Elastosis"], "Acantholysis is loss of keratinocyte cohesion."),
    ]),
    ("eczema-psoriasis", "Eczematous Dermatitis, Psoriasis, and Lichenoid Disorders", [
        q("easy", "Atopic dermatitis is commonly associated with:", "IgE-mediated atopy", ["Low thyroid hormone", "Adrenal insufficiency", "Renal stones"], "Atopic dermatitis occurs in the atopic diathesis."),
        q("easy", "Psoriasis classically has sharply demarcated plaques with:", "Silvery scale", ["Black eschar", "Umbilicated vesicles", "Painless ulcers"], "Psoriasis produces erythematous plaques with silvery scale."),
        q("easy", "Lichen planus often presents with purple:", "Pruritic polygonal papules", ["Painless nodules", "Bullae only", "Comedones"], "The classic lesions are pruritic, purple, polygonal papules."),
        q("moderate", "Psoriasis histology shows neutrophils in stratum corneum called:", "Munro microabscesses", ["Pautrier microabscesses", "Aschoff bodies", "Call-Exner bodies"], "Munro microabscesses are neutrophils in parakeratotic scale."),
        q("moderate", "Psoriasis has regular acanthosis with:", "Elongated rete ridges", ["Loss of epidermis", "Dermal amyloid only", "Subcutaneous vasculitis"], "Psoriasis shows regular epidermal hyperplasia."),
        q("moderate", "Lichen planus shows a band-like infiltrate at the:", "Dermoepidermal junction", ["Deep subcutis", "Sweat gland lumen", "Hair shaft cortex"], "Lichenoid inflammation hugs the junction."),
        q("moderate", "Contact dermatitis is usually mediated by:", "Type IV hypersensitivity", ["Type I IgE only", "Complement deficiency", "Amyloid deposition"], "Allergic contact dermatitis is delayed hypersensitivity."),
        q("high", "A patient has itchy flexural dermatitis, asthma, and allergic rhinitis. Biopsy shows spongiosis with superficial perivascular lymphocytes and occasional eosinophils. Which disorder is most likely?", "Atopic dermatitis", ["Psoriasis", "Lichen planus", "Pemphigus vulgaris"], "Atopic dermatitis is an eczematous atopic disorder."),
        q("high", "A biopsy from an extensor plaque shows regular acanthosis, thinning over dermal papillae, parakeratosis, and neutrophils within the stratum corneum. Which disease is likely?", "Psoriasis", ["Atopic dermatitis", "Lichen planus", "Bullous pemphigoid"], "Psoriasis has regular acanthosis and Munro microabscesses."),
        q("high", "A patient has violaceous flat-topped itchy papules on wrists and oral white lace-like lesions. Biopsy shows sawtooth rete ridges and band-like lymphocytes. Which diagnosis fits?", "Lichen planus", ["Psoriasis", "Seborrheic keratosis", "Urticaria"], "Lichen planus has purple polygonal papules and lichenoid inflammation."),
    ]),
    ("blistering", "Blistering Disorders and Autoimmune Bullous Disease", [
        q("easy", "Pemphigus vulgaris targets:", "Desmoglein", ["Hemidesmosomes only", "Collagen VII only", "Keratin 17"], "Autoantibodies target desmogleins in desmosomes."),
        q("easy", "Bullous pemphigoid produces:", "Subepidermal blisters", ["Intraepidermal acantholysis", "Dermal sarcoma", "Melanocytic nests only"], "Hemidesmosomal injury separates epidermis from dermis."),
        q("easy", "Dermatitis herpetiformis is associated with:", "Celiac disease", ["Graves disease only", "Addison disease", "Renal stones"], "Dermatitis herpetiformis is gluten-sensitive."),
        q("moderate", "Pemphigus vulgaris has a positive:", "Nikolsky sign", ["Murphy sign", "Courvoisier sign", "Chvostek sign"], "Fragile epidermal adhesion causes Nikolsky sign."),
        q("moderate", "Bullous pemphigoid antibodies target:", "Hemidesmosomal proteins", ["Desmoglein 3", "Melan-A", "Elastin only"], "BP180 and BP230 are hemidesmosomal antigens."),
        q("moderate", "Dermatitis herpetiformis shows granular IgA in:", "Dermal papillae", ["Basal nuclei", "Sebaceous glands", "Subcutaneous fat"], "Granular IgA deposits occur at tips of dermal papillae."),
        q("moderate", "Pemphigus vulgaris blister is located:", "Suprabasal", ["Subepidermal", "Subcutaneous", "In blood vessels"], "Suprabasal acantholysis is classic."),
        q("high", "A patient has flaccid oral and skin bullae, positive Nikolsky sign, and biopsy showing suprabasal acantholysis with tombstone basal cells. Which disease is most likely?", "Pemphigus vulgaris", ["Bullous pemphigoid", "Dermatitis herpetiformis", "Epidermolysis bullosa"], "Pemphigus vulgaris causes suprabasal acantholytic blisters."),
        q("high", "An older patient has tense bullae on erythematous skin. Biopsy shows a subepidermal blister with eosinophils and linear IgG along basement membrane. Which diagnosis fits?", "Bullous pemphigoid", ["Pemphigus vulgaris", "Impetigo", "Lichen planus"], "Bullous pemphigoid targets hemidesmosomes and creates tense bullae."),
        q("high", "A patient with gluten sensitivity has intensely pruritic grouped vesicles on elbows and knees. Immunofluorescence shows granular IgA at dermal papillae. Which condition is present?", "Dermatitis herpetiformis", ["Pemphigus foliaceus", "Bullous pemphigoid", "Herpes zoster"], "Dermatitis herpetiformis is a celiac-associated IgA blistering disease."),
    ]),
    ("infections", "Cutaneous Infections and Infestations", [
        q("easy", "Impetigo is commonly caused by:", "Staphylococcus aureus or Streptococcus pyogenes", ["HPV only", "Candida only", "Molluscum contagiosum only"], "Impetigo is a superficial bacterial infection."),
        q("easy", "Molluscum contagiosum is caused by a:", "Poxvirus", ["Herpesvirus", "Papillomavirus", "Fungus"], "Molluscum contagiosum is a poxvirus infection."),
        q("easy", "Tinea corporis is caused by:", "Dermatophyte fungi", ["Mycobacteria", "Poxvirus", "Treponema"], "Dermatophytes infect keratinized tissue."),
        q("moderate", "Molluscum contagiosum lesions contain:", "Henderson-Patterson bodies", ["Cowdry A inclusions", "Auer rods", "Psammoma bodies"], "Large intracytoplasmic inclusions are characteristic."),
        q("moderate", "Herpes simplex infection shows:", "Multinucleated epithelial giant cells", ["Schiller-Duval bodies", "Keratin pearls only", "Amyloid stroma"], "HSV causes multinucleation and nuclear molding."),
        q("moderate", "Verruca vulgaris is caused by:", "HPV", ["EBV", "CMV", "Candida"], "Common warts are HPV-related."),
        q("moderate", "Scabies is caused by:", "Sarcoptes scabiei", ["Dermatophyte hyphae", "Poxvirus", "Treponema pallidum"], "Scabies mites burrow in stratum corneum."),
        q("high", "A child has honey-colored crusted erosions around the mouth. Culture grows gram-positive cocci, and the infection is limited to the superficial epidermis. Which diagnosis is most likely?", "Impetigo", ["Cellulitis", "Molluscum contagiosum", "Tinea corporis"], "Impetigo causes superficial crusted bacterial lesions."),
        q("high", "A patient has multiple umbilicated pearly papules. Biopsy shows lobulated epidermal hyperplasia with large eosinophilic intracytoplasmic viral inclusions in keratinocytes. Which infection is likely?", "Molluscum contagiosum", ["Verruca vulgaris", "Herpes simplex", "Tinea versicolor"], "Molluscum contagiosum produces Henderson-Patterson bodies."),
        q("high", "A painful grouped vesicular eruption recurs on the lip, and cytology shows multinucleated giant cells with nuclear molding and margination. Which viral infection is most likely?", "Herpes simplex virus", ["HPV", "Poxvirus", "Parvovirus B19"], "HSV causes grouped vesicles and multinucleated giant cells."),
    ]),
    ("pigment-nevi", "Pigmentary Disorders and Benign Melanocytic Nevi", [
        q("easy", "Vitiligo is loss of:", "Melanocytes", ["Keratinocytes", "Langerhans cells only", "Sebocytes"], "Vitiligo involves autoimmune melanocyte destruction."),
        q("easy", "Melanocytic nevi are benign proliferations of:", "Melanocytes", ["Keratinocytes", "Fibroblasts", "Adipocytes"], "Nevi are benign melanocytic lesions."),
        q("easy", "Freckles are also called:", "Ephelides", ["Lentigines only", "Nevi", "Melanomas"], "Ephelides are sun-induced freckles."),
        q("moderate", "Junctional nevi have nests at the:", "Dermoepidermal junction", ["Deep subcutis", "Eccrine ducts", "Hair bulb only"], "Junctional nests lie along the basal layer."),
        q("moderate", "Compound nevi have melanocytes in epidermis and:", "Dermis", ["Bone marrow", "Blood vessels only", "Adrenal cortex"], "Compound nevi bridge junctional and dermal components."),
        q("moderate", "Dysplastic nevi are clinically important because they:", "Increase melanoma risk", ["Are always melanoma", "Are infections", "Cause psoriasis"], "Dysplastic nevi are melanoma risk markers and precursors."),
        q("moderate", "Nevus maturation means melanocytes become smaller with:", "Depth", ["Sun exposure", "Keratinization", "Necrosis"], "Benign nevi mature as cells descend into dermis."),
        q("high", "A depigmented patch shows absence of melanocytes in the basal epidermis, and the patient has other autoimmune disease. Which pigmentary disorder is most likely?", "Vitiligo", ["Melasma", "Lentigo simplex", "Mongolian spot"], "Vitiligo is autoimmune melanocyte loss."),
        q("high", "A small symmetric pigmented papule shows nests of melanocytes at the dermoepidermal junction and in dermis, with progressive maturation at depth. Which lesion is likely?", "Compound melanocytic nevus", ["Superficial spreading melanoma", "Seborrheic keratosis", "Blue nevus"], "Benign compound nevi show junctional and dermal nests with maturation."),
        q("high", "A patient has multiple large irregular pigmented nevi with architectural disorder and cytologic atypia, plus family history of melanoma. Which diagnosis best describes these lesions?", "Dysplastic nevi", ["Common freckles", "Molluscum contagiosum", "Dermatofibromas"], "Dysplastic nevi are atypical melanocytic lesions associated with melanoma risk."),
    ]),
    ("melanoma", "Melanoma and Malignant Melanocytic Tumors", [
        q("easy", "The most important prognostic factor in melanoma is:", "Breslow thickness", ["Tumor color", "Patient sex only", "Itch severity"], "Depth of invasion strongly predicts prognosis."),
        q("easy", "Melanoma arises from malignant:", "Melanocytes", ["Keratinocytes", "Sebocytes", "Fibroblasts"], "Melanoma is a malignant melanocytic tumor."),
        q("easy", "ABCDE warning signs include asymmetry, border irregularity, color variation, diameter, and:", "Evolution", ["Edema only", "Eosinophilia", "Exophthalmos"], "Evolution is change in a lesion."),
        q("moderate", "Superficial spreading melanoma often has a prominent:", "Radial growth phase", ["Pure subcutaneous growth", "No epidermal component", "Only follicular growth"], "Radial growth is common in superficial spreading melanoma."),
        q("moderate", "Nodular melanoma is notable for early:", "Vertical growth", ["Viral inclusions", "Cyst formation", "Comedo necrosis"], "Nodular melanoma rapidly invades vertically."),
        q("moderate", "Acral lentiginous melanoma occurs on palms, soles, and:", "Subungual sites", ["Thyroid", "Breast ducts", "Adrenal medulla"], "Acral sites include nail beds."),
        q("moderate", "Sentinel lymph node biopsy in melanoma evaluates:", "Regional metastasis", ["Keratinization", "Sebum production", "Celiac disease"], "Sentinel nodes assess early lymphatic spread."),
        q("high", "A changing asymmetric pigmented lesion has irregular borders, multiple colors, and biopsy shows atypical melanocytes invading dermis with pagetoid spread in epidermis. Which tumor is most likely?", "Melanoma", ["Compound nevus", "Seborrheic keratosis", "Dermatofibroma"], "ABCDE changes and invasive atypical melanocytes indicate melanoma."),
        q("high", "A melanoma pathology report emphasizes tumor depth measured from the granular layer to the deepest malignant cell in the dermis. Which prognostic measurement is being reported?", "Breslow thickness", ["Clark color score", "Gleason score", "Ann Arbor stage"], "Breslow thickness is the key melanoma depth measurement."),
        q("high", "A dark rapidly enlarging dome-shaped nodule shows little radial growth but deep dermal invasion by atypical melanocytes and frequent mitoses. Which melanoma subtype is suggested?", "Nodular melanoma", ["Lentigo maligna melanoma", "Compound nevus", "Blue nevus"], "Nodular melanoma is dominated by vertical growth."),
    ]),
    ("epidermal-benign", "Benign Epidermal and Adnexal Tumors", [
        q("easy", "Seborrheic keratosis is a benign tumor of:", "Epidermal keratinocytes", ["Melanocytes only", "Adipocytes", "Endothelial cells"], "Seborrheic keratosis is a benign epidermal proliferation."),
        q("easy", "Epidermal inclusion cyst is lined by:", "Squamous epithelium", ["Respiratory epithelium", "Urothelium", "Endothelium"], "It is lined by stratified squamous epithelium with granular layer."),
        q("easy", "A lipoma is a benign tumor of:", "Adipose tissue", ["Sweat glands", "Melanocytes", "Keratinocytes"], "Lipoma is benign mature fat."),
        q("moderate", "Seborrheic keratoses often appear clinically as:", "Stuck-on plaques", ["Painful ulcers", "Blue nodules only", "Grouped vesicles"], "They have a waxy stuck-on appearance."),
        q("moderate", "Horn cysts are characteristic of:", "Seborrheic keratosis", ["Melanoma", "Basal cell carcinoma", "Kaposi sarcoma"], "Pseudohorn cysts are keratin-filled spaces."),
        q("moderate", "Pilomatricoma shows differentiation toward:", "Hair matrix", ["Sebaceous glands only", "Eccrine ducts only", "Melanocytes"], "Pilomatricoma is a hair matrix tumor."),
        q("moderate", "Syringoma is a benign tumor with:", "Eccrine duct differentiation", ["Neural crest only", "Melanocytic nests", "Adipose lobules"], "Syringomas are benign eccrine ductal tumors."),
        q("high", "An older adult has a waxy brown stuck-on plaque. Biopsy shows basaloid epidermal proliferation with keratin-filled horn cysts and no invasion. Which lesion is most likely?", "Seborrheic keratosis", ["Melanoma", "Squamous cell carcinoma", "Dermatofibroma"], "Seborrheic keratosis has a stuck-on appearance and horn cysts."),
        q("high", "A mobile subcutaneous nodule has a central punctum, and excision shows a cyst lined by stratified squamous epithelium containing laminated keratin. Which lesion is this?", "Epidermal inclusion cyst", ["Lipoma", "Pilomatricoma", "Basal cell carcinoma"], "Epidermal inclusion cysts contain keratin and squamous lining."),
        q("high", "A child has a firm calcified dermal nodule. Microscopy shows basaloid cells transitioning to shadow cells with calcification. Which hair follicle tumor is likely?", "Pilomatricoma", ["Syringoma", "Seborrheic keratosis", "Kaposi sarcoma"], "Pilomatricoma shows hair matrix differentiation with shadow cells."),
    ]),
    ("keratinocyte-cancers", "Actinic Keratosis, Squamous Cell Carcinoma, and Basal Cell Carcinoma", [
        q("easy", "Actinic keratosis is caused by chronic:", "UV exposure", ["HPV always", "Fungal infection", "Autoimmune IgA"], "UV light causes atypia in sun-damaged keratinocytes."),
        q("easy", "Basal cell carcinoma is the most common human:", "Cancer", ["Sarcoma", "Lymphoma", "Germ cell tumor"], "BCC is extremely common."),
        q("easy", "Squamous cell carcinoma shows malignant:", "Keratinocytes", ["Melanocytes", "Adipocytes", "Langerhans cells"], "Cutaneous SCC is a keratinocyte carcinoma."),
        q("moderate", "Basal cell carcinoma is associated with mutations in:", "PTCH pathway", ["HBB", "HFE", "CFTR"], "Hedgehog pathway alterations are common."),
        q("moderate", "Basal cell carcinoma histology shows:", "Peripheral palisading", ["Schiller-Duval bodies", "Call-Exner bodies", "Zellballen nests"], "Tumor nests have peripheral palisading and clefting."),
        q("moderate", "Squamous cell carcinoma may show:", "Keratin pearls", ["Horn cysts only", "Nevus maturation", "Dermal amyloid always"], "Keratin pearls indicate squamous differentiation."),
        q("moderate", "Actinic keratosis is a precursor to:", "Squamous cell carcinoma", ["Basal cell carcinoma only", "Melanoma only", "Lipoma"], "Some actinic keratoses progress to SCC."),
        q("high", "A fair-skinned older adult has rough scaly erythematous papules on sun-exposed skin. Biopsy shows atypical basal keratinocytes with parakeratosis. Which precursor lesion is likely?", "Actinic keratosis", ["Seborrheic keratosis", "Melanoma", "Dermatofibroma"], "Actinic keratosis is a UV-induced SCC precursor."),
        q("high", "A pearly papule with telangiectasias on the face shows nests of basaloid cells with peripheral palisading and stromal retraction clefts. Which tumor is most likely?", "Basal cell carcinoma", ["Squamous cell carcinoma", "Merkel cell carcinoma", "Keratoacanthoma"], "BCC has basaloid nests, palisading, and clefting."),
        q("high", "A sun-exposed ulcerated skin lesion shows invasive atypical squamous cells extending into dermis with intercellular bridges and keratin pearls on microscopy. Which carcinoma is present?", "Squamous cell carcinoma", ["Basal cell carcinoma", "Melanoma", "Sebaceous adenoma"], "SCC is invasive malignant keratinocyte tumor with keratinization."),
    ]),
    ("dermal-vascular", "Dermal, Vascular, and Subcutaneous Tumors", [
        q("easy", "Dermatofibroma is a benign fibrohistiocytic lesion of:", "Dermis", ["Epidermal surface only", "Bone", "Thyroid"], "Dermatofibroma is a dermal fibrohistiocytic proliferation."),
        q("easy", "Kaposi sarcoma is associated with:", "HHV-8", ["HPV 6", "EBV only", "Poxvirus"], "Human herpesvirus 8 drives Kaposi sarcoma."),
        q("easy", "A hemangioma is a benign tumor of:", "Blood vessels", ["Melanocytes", "Keratinocytes", "Adipocytes only"], "Hemangiomas are benign vascular proliferations."),
        q("moderate", "Dermatofibroma often shows epidermal:", "Hyperplasia overlying lesion", ["Complete necrosis", "Full-thickness dysplasia", "Subepidermal blister"], "Overlying epidermal hyperplasia is common."),
        q("moderate", "Dermatofibrosarcoma protuberans is locally aggressive and often has:", "Storiform pattern", ["Comedo necrosis", "Horn cysts", "Granular IgA"], "DFSP shows storiform spindle cell proliferation."),
        q("moderate", "Kaposi sarcoma forms vascular slits with:", "Spindle cells", ["Nevus cells", "Squamous pearls", "Shadow cells"], "Kaposi sarcoma is a spindle-cell vascular tumor."),
        q("moderate", "Erythema nodosum is a form of:", "Septal panniculitis", ["Epidermal carcinoma", "Acantholytic blister", "Melanocytic nevus"], "Erythema nodosum is septal panniculitis without vasculitis."),
        q("high", "A firm brown papule on the leg dimples when squeezed. Biopsy shows dermal spindle cells, collagen trapping, and overlying epidermal hyperplasia. Which lesion is most likely?", "Dermatofibroma", ["Dermatofibrosarcoma protuberans", "Melanoma", "Basal cell carcinoma"], "Dermatofibroma is a benign dermal fibrohistiocytic lesion."),
        q("high", "An AIDS patient has purple skin plaques. Biopsy shows spindle cells forming slit-like vascular spaces with extravasated red cells and HHV-8 positivity. Which tumor is likely?", "Kaposi sarcoma", ["Angiosarcoma", "Hemangioma", "Pyogenic granuloma"], "Kaposi sarcoma is an HHV-8-associated vascular tumor."),
        q("high", "A slowly enlarging plaque on the trunk shows a storiform CD34-positive spindle cell tumor infiltrating subcutaneous fat in a honeycomb pattern. Which diagnosis fits?", "Dermatofibrosarcoma protuberans", ["Dermatofibroma", "Kaposi sarcoma", "Lipoma"], "DFSP is locally aggressive and infiltrates fat."),
    ]),
    ("cutaneous-lymphoid", "Cutaneous Lymphoid, Histiocytic, and Systemic Skin Lesions", [
        q("easy", "Mycosis fungoides is a cutaneous:", "T-cell lymphoma", ["B-cell leukemia only", "Melanoma", "Sarcoma"], "Mycosis fungoides is a primary cutaneous T-cell lymphoma."),
        q("easy", "Pautrier microabscesses are seen in:", "Mycosis fungoides", ["Psoriasis", "Pemphigus", "Kaposi sarcoma"], "They are collections of atypical T cells in epidermis."),
        q("easy", "Urticaria is mediated largely by:", "Mast cell degranulation", ["Melanocyte loss", "Keratinocyte invasion", "Adipocyte necrosis"], "Histamine release causes wheals."),
        q("moderate", "Sezary syndrome includes malignant T cells in:", "Peripheral blood", ["Urine", "Bile", "Synovial fluid only"], "Sezary syndrome is leukemic CTCL."),
        q("moderate", "Langerhans cell histiocytosis cells are positive for:", "CD1a and langerin", ["PSA and HER2", "Calcitonin and TTF1", "Desmin and myogenin"], "Langerhans cells express CD1a and langerin."),
        q("moderate", "Erythema multiforme often shows:", "Targetoid lesions", ["Stuck-on plaques", "Pearly papules", "Blue dome cysts"], "Target lesions are classic."),
        q("moderate", "Drug eruptions commonly show:", "Interface or spongiotic dermatitis with eosinophils", ["Only horn cysts", "Only nevus maturation", "Only amyloid stroma"], "Eosinophils often suggest drug reaction."),
        q("high", "A patient has chronic scaly patches progressing to plaques and tumors. Biopsy shows epidermotropic atypical cerebriform T cells forming Pautrier microabscesses. Which diagnosis is most likely?", "Mycosis fungoides", ["Psoriasis", "Lichen planus", "Kaposi sarcoma"], "Mycosis fungoides is epidermotropic cutaneous T-cell lymphoma."),
        q("high", "A patient with diffuse erythroderma has circulating malignant T cells with cerebriform nuclei, pruritus, and generalized lymphadenopathy. Which leukemic cutaneous lymphoma variant is present?", "Sezary syndrome", ["Mycosis fungoides patch stage only", "Hodgkin lymphoma", "Merkel cell carcinoma"], "Sezary syndrome is leukemic CTCL with erythroderma."),
        q("high", "A child has lytic bone lesions and skin papules. Biopsy shows grooved histiocytes positive for CD1a and langerin with Birbeck granules. Which disease is likely?", "Langerhans cell histiocytosis", ["Dermatofibroma", "Urticaria", "Bullous pemphigoid"], "Langerhans cell histiocytosis has CD1a/langerin-positive cells."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch25-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 25 questions, got {len(chapter_questions)}")
    topic_counts = Counter(q["topic"] for q in chapter_questions)
    if len(topic_counts) != 10 or any(count != 10 for count in topic_counts.values()):
        raise ValueError(f"Bad topic distribution: {topic_counts}")
    expected = Counter({"easy": 3, "moderate": 4, "high": 3})
    for topic in topic_counts:
        counts = Counter(q["difficulty"] for q in chapter_questions if q["topic"] == topic)
        if counts != expected:
            raise ValueError(f"Bad difficulty distribution for {topic}: {counts}")
    for question in chapter_questions:
        options = question["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Bad options: {question['id']}")
        if question["answer"] != options[question["answerIndex"]]:
            raise ValueError(f"Bad answer: {question['id']}")
    short_high = [q["id"] for q in chapter_questions if q["difficulty"] == "high" and len(q["prompt"].split()) < 24]
    if short_high:
        raise ValueError(f"High-level prompts too short: {short_high[:5]}")
    if all_questions is not None:
        ids = [q.get("id") for q in all_questions]
        duplicates = [qid for qid, count in Counter(ids).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate ids: {duplicates[:10]}")


def main():
    chapter_questions = build_questions()
    validate(chapter_questions)
    total_removed = 0
    for data_path in DATA_PATHS:
        data = json.loads(data_path.read_text(encoding="utf-8-sig"))
        existing = data.get("questions", [])
        kept = [
            question for question in existing
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch25-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 25 questions")
    print(f"Removed {total_removed} existing Chapter 25 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 25 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
