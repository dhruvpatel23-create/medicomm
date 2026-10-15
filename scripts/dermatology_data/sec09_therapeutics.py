from .common import q

CHAPTERS = [
    (32, "Medical Therapy and Common Surgical Procedures", "easy", [
        q(
            "According to the standardized Stoughton-Cornell 7-class potency ranking of Topical Corticosteroids, which agent belongs to Class I (Superpotent), and why is its continuous application to the face, intertriginous folds, and in pediatric patients strictly contraindicated?",
            "Clobetasol propionate 0.05%; causes cutaneous atrophy and striae",
            ["Hydrocortisone 1%; causes acute contact dermatitis", "Triamcinolone acetonide 0.1%; causes localized vitiligo", "Desonide 0.05%; causes immediate osteomalacia"],
            "Class I (superpotent) topical corticosteroids (Clobetasol propionate 0.05%, Halobetasol propionate 0.05%) are up to 1000 times more potent than hydrocortisone. Their use is strictly restricted to thick, hyperkeratotic, recalcitrant lesions on palms, soles, or extensor plaques for a maximum of 2 to 3 consecutive weeks (<50 grams/week). Application to high-absorption, thin-skinned areas (face, axillae, groin) rapidly causes severe dermal atrophy, capillary telangiectasias, irreversible striae, perioral dermatitis, and systemic HPA-axis suppression.",
            clinical=False
        ),
        q(
            "In prescribing topical dermatological formulations, what is the quantitative clinical definition of a 'Fingertip Unit' (FTU), and how much total anatomical body surface area does one FTU cover?",
            "Ointment from distal crease to fingertip (~0.5g); covers 2 adult palms",
            ["Amount filling 10-ml spoon (~5g); covers lower extremity", "A pea-sized droplet (~0.1g); covers anterior chest", "Amount squeezed onto palm (~2.0g); covers scalp"],
            "A Fingertip Unit (FTU) is the standardized clinical metric for measuring topical medications: it is the amount of cream or ointment expressed from a tube with a standard 5-mm diameter nozzle onto the palmar aspect of an adult index finger from the distal interphalangeal crease to the fingertip. One FTU weighs approximately 0.5 grams and provides adequate coverage for a skin surface area equal to two adult handprints (both palms and all five fingers flat, representing ~2% of total body surface area).",
            clinical=False
        ),
        q(
            "What is the cellular molecular mechanism of action of Topical Calcineurin Inhibitors (Tacrolimus ointment and Pimecrolimus cream), and what critical clinical advantage do they offer over topical corticosteroids for facial atopic dermatitis?",
            "FKBP-12/calcineurin inhibition sparing collagen synthesis with zero cutaneous atrophy",
            ["Directly cross-link DNA in dividing basal keratinocytes to arrest mitosis", "Inhibit cyclooxygenase-2 (COX-2) to block prostaglandin E2 synthesis", "Bind nuclear glucocorticoid receptors to stimulate lipocortin-1 secretion"],
            "Topical calcineurin inhibitors (TCIs) bind to the intracellular immunophilin macrophilin-12 (FKBP-12). This complex blocks the protein phosphatase calcineurin, preventing dephosphorylation and nuclear translocation of Nuclear Factor of Activated T cells (NFAT), thereby blocking transcription of interleukin-2 (IL-2), IL-4, and IFN-gamma. Because TCIs have zero effect on endothelial cells, dermal fibroblasts, or collagen synthesis, they completely lack atrophogenic side effects and can be safely applied to delicate facial, eyelid, and intertriginous skin.",
            clinical=False
        ),
        q(
            "What is the precise peak monochromatic wavelength of Narrowband Ultraviolet B (NB-UVB) phototherapy, and why has it largely superseded both Broadband UVB and oral PUVA in the first-line treatment of moderate-to-severe Psoriasis and Vitiligo?",
            "Peak emission at 311-313 nm with minimal erythema and no oral psoralen",
            ["Peak emission at 254 nm; provides instantaneous bactericidal sterilization", "Peak emission at 365 nm; requires oral methoxsalen photosensitization", "Peak emission at 420 nm; penetrates into the deep subcutaneous adipose tissue"],
            "Narrowband UVB (NB-UVB) phototherapy utilizes fluorescent tubes that emit a narrow, concentrated spectrum centered precisely at 311 to 313 nm. This specific wavelength corresponds to the peak therapeutic action spectrum for clearing psoriasis plaques and stimulating follicular melanocyte migration in vitiligo, while avoiding shorter erythema-inducing wavelengths (290-305 nm). Unlike PUVA, NB-UVB does not require oral psoralen ingestion, avoids nausea, does not require 24-hour post-treatment eye protection, and carries a far lower long-term risk of cutaneous squamous cell carcinoma.",
            clinical=False
        ),
        q(
            "In cutaneous cryosurgery utilizing liquid nitrogen (-196 °C / 77 K) for benign and pre-malignant lesions (such as verrucae and actinic keratoses), which resident epidermal cell type is the most cold-sensitive and vulnerable to irreversible freezing injury (-5 °C), frequently resulting in post-procedure hypopigmentation?",
            "Epidermal Melanocytes (destroyed at -5 °C)",
            ["Keratinocytes (destroyed at -20 °C to -30 °C)", "Dermal Fibroblasts (destroyed at -35 °C to -40 °C)", "Subcutaneous Adipocytes (destroyed at -50 °C)"],
            "In cutaneous cryosurgery with liquid nitrogen (boiling point -196 °C), different skin cells exhibit markedly disparate thermal lethal thresholds: Melanocytes are extraordinarily cold-sensitive, undergoing lethal intracellular crystallization and cell death at just -5 °C. In contrast, epidermal keratinocytes require -20 °C to -30 °C for destruction, and malignant cells require -50 °C. Consequently, even brief, superficial cryotherapy frequently results in permanent, chalky-white post-inflammatory hypopigmentation, especially in darker skin types.",
            clinical=False
        ),
    ]),
]
