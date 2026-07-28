import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Pharmacotherapy of Neoplastic Disease"
BASE = {"subjectId": "pharmacology", "subjectTitle": "Pharmacology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("general-principles-cancer", "General Principles in the Pharmacotherapy of Cancer", [
        q("A tumor initially shrinks with chemotherapy but later regrows despite continued treatment. Which concept best explains selection of a resistant clone?", "Tumor heterogeneity with drug-sensitive cells eliminated first", ["Immediate drug allergy", "Loss of all cell division", "Universal cure of micrometastases"], "Cancer cell populations are genetically diverse; therapy can select resistant subclones."),
        q("Combination chemotherapy is often more effective than single-agent therapy because it:", "Targets different mechanisms and reduces probability of resistance", ["Always eliminates toxicity", "Allows subtherapeutic dosing of all drugs", "Prevents all myelosuppression"], "Non-cross-resistant combinations improve log-kill and reduce resistant escape when toxicities are manageable."),
        q("A patient receives adjuvant chemotherapy after complete surgical resection. The goal is to:", "Eradicate occult micrometastatic disease", ["Shrink an unresectable primary only", "Provide analgesia without antitumor effect", "Reverse tumor marker assays"], "Adjuvant therapy treats microscopic residual disease to reduce recurrence risk."),
        q("Neoadjuvant therapy before surgery is chosen partly to:", "Downstage tumor and test in vivo treatment response", ["Avoid tissue diagnosis", "Increase tumor vascular invasion", "Prevent any need for staging"], "Preoperative systemic therapy can improve resectability and reveal sensitivity."),
        q("A chemotherapy regimen is most likely curative when tumor cells have:", "High growth fraction and strong drug sensitivity", ["Complete absence of proliferation", "No drug penetration", "Universal efflux pumps"], "Rapidly dividing, chemosensitive tumors often respond best to cytotoxic therapy."),
        q("Dose intensity matters in curative chemotherapy because:", "Suboptimal exposure can permit regrowth of resistant disease", ["Lower doses always kill more cancer cells", "Toxicity proves cure", "Tumor cells cannot recover"], "Cancer therapy often follows log-kill kinetics, making adequate scheduled dosing important."),
        q("A patient with bulky lymphoma develops hyperkalemia, hyperphosphatemia, hypocalcemia, and renal injury after treatment. The diagnosis is:", "Tumor lysis syndrome", ["Serotonin syndrome", "SIADH from vincristine only", "Red man syndrome"], "Rapid tumor breakdown releases intracellular potassium, phosphate, and nucleic acids."),
        q("Rasburicase helps high-risk tumor lysis syndrome by:", "Converting uric acid to soluble allantoin", ["Blocking xanthine oxidase only", "Chelating phosphate", "Stimulating renal potassium secretion"], "Rasburicase rapidly degrades existing uric acid; allopurinol prevents new formation."),
        q("Cancer therapy response is best interpreted using both imaging and clinical context because:", "Tumor size, viability, symptoms, and biomarkers can diverge", ["Imaging is never useful", "Biomarkers always prove cure", "Symptoms always worsen with response"], "Modern oncology integrates radiographic, molecular, and patient-level outcomes."),
        q("A targeted drug works only in tumors with a specific mutation. The required step before treatment is:", "Predictive biomarker testing", ["Avoiding biopsy", "Giving the drug to all cancers", "Stopping pathology review"], "Precision therapy depends on identifying the actionable driver or target."),
    ]),
    ("cytotoxics-antimetabolites", "Cytotoxics and Antimetabolites", [
        q("Cyclophosphamide causes hemorrhagic cystitis. Which protective drug binds the toxic metabolite acrolein?", "Mesna", ["Leucovorin", "Dexrazoxane", "Folinic acid"], "Mesna detoxifies acrolein in urine and reduces ifosfamide/cyclophosphamide cystitis."),
        q("Cisplatin nephrotoxicity and ototoxicity occur because platinum drugs:", "Form DNA cross-links but also injure renal tubules and cochlear cells", ["Block microtubules only", "Inhibit aromatase", "Activate EGFR"], "Platinum compounds cross-link DNA; hydration and monitoring reduce toxicity."),
        q("Doxorubicin lifetime dosing is limited mainly by:", "Cumulative cardiomyopathy from free radical injury", ["Immediate cystitis", "Severe ototoxicity only", "Pulmonary fibrosis in every patient"], "Anthracyclines intercalate DNA/topoisomerase II and generate radicals causing dose-related cardiotoxicity."),
        q("Dexrazoxane can reduce anthracycline cardiotoxicity because it:", "Chelates iron and reduces free radical formation", ["Rescues folate pools", "Blocks HER2", "Activates topoisomerase II"], "Dexrazoxane is cardioprotective in selected anthracycline-treated patients."),
        q("Methotrexate toxicity is rescued with leucovorin because leucovorin:", "Bypasses dihydrofolate reductase blockade", ["Blocks thymidylate synthase", "Inhibits xanthine oxidase", "Chelates platinum"], "Leucovorin supplies reduced folate to normal cells after high-dose methotrexate."),
        q("5-Fluorouracil kills cancer cells mainly by inhibiting:", "Thymidylate synthase after conversion to FdUMP", ["BCR-ABL kinase", "Tubulin polymerization", "Proteasome beta subunit"], "5-FU metabolites impair thymidylate synthesis and RNA processing."),
        q("Capecitabine is clinically useful because it is:", "An oral prodrug converted to 5-FU preferentially in tumors", ["A platinum analog", "A taxane", "A monoclonal antibody"], "Capecitabine is an oral fluoropyrimidine prodrug."),
        q("Vincristine causes constipation and peripheral neuropathy because it:", "Inhibits microtubule polymerization in neurons and dividing cells", ["Stabilizes microtubules like paclitaxel", "Cross-links DNA", "Blocks VEGF"], "Vinca alkaloids prevent microtubule assembly and are neurotoxic."),
        q("Paclitaxel arrests mitosis by:", "Stabilizing microtubules and preventing depolymerization", ["Blocking folate reduction", "Inhibiting proteasomes", "Alkylating DNA"], "Taxanes freeze microtubule dynamics, disrupting mitosis."),
        q("Bleomycin pulmonary toxicity is dose-limiting because lung tissue has:", "Low bleomycin hydrolase activity and susceptibility to oxidative injury", ["High folate rescue", "No oxygen exposure", "No DNA"], "Bleomycin causes DNA breaks and can produce pneumonitis/fibrosis."),
    ]),
    ("kinase-pathway-small-molecules", "Protein Kinase Inhibitors and Pathway-Targeted Small Molecules", [
        q("Imatinib produces dramatic responses in CML because it inhibits:", "BCR-ABL tyrosine kinase", ["HER2 extracellular domain", "VEGF ligand", "PD-1 receptor"], "CML is driven by BCR-ABL, making kinase inhibition highly effective."),
        q("A CML patient with T315I mutation is resistant to many TKIs. Which drug was designed to retain activity?", "Ponatinib", ["Tamoxifen", "Trastuzumab", "Rituximab"], "Ponatinib can inhibit BCR-ABL with T315I but has vascular toxicity risk."),
        q("Erlotinib works best in non-small cell lung cancers with activating:", "EGFR mutations", ["BCR-ABL translocation", "CD20 expression", "ER positivity"], "EGFR TKIs require predictive mutation testing for best response."),
        q("EGFR inhibitors commonly cause acneiform rash because EGFR signaling is important in:", "Skin and hair follicle epithelial homeostasis", ["Platelet aggregation", "Renal erythropoietin synthesis", "Bile acid transport"], "Rash often correlates with EGFR pathway inhibition in skin."),
        q("Osimertinib is useful in EGFR-mutant lung cancer with T790M because it:", "Inhibits mutant EGFR including T790M with CNS activity", ["Blocks ALK only", "Binds VEGF ligand", "Activates PD-1"], "Osimertinib is a later-generation EGFR TKI active against key resistance mutations."),
        q("Crizotinib is chosen for lung cancer when testing shows:", "ALK rearrangement", ["ER positivity", "CD20 expression", "BRAF wild-type melanoma without mutation", "BCR-ABL in neutrophils"], "ALK inhibitors treat ALK-driven tumors."),
        q("Vemurafenib can worsen tumors without BRAF V600 mutation because:", "Paradoxical MAPK activation may occur in BRAF-wild-type cells", ["It activates estrogen receptors", "It blocks CD20", "It chelates platinum"], "BRAF inhibitors require mutation selection to avoid ineffective or harmful signaling effects."),
        q("Palbociclib treats hormone receptor-positive breast cancer by inhibiting:", "CDK4/6 cell-cycle progression", ["DNA gyrase", "PD-1", "Aromatase"], "CDK4/6 inhibitors block G1-S progression and commonly cause neutropenia."),
        q("Bortezomib is effective in multiple myeloma because it inhibits:", "Proteasome-mediated protein degradation", ["EGFR kinase", "Microtubule polymerization", "Estrogen synthesis"], "Proteasome inhibition causes toxic protein accumulation in plasma cells."),
        q("Venetoclax induces apoptosis in selected leukemias by inhibiting:", "BCL-2", ["BTK", "mTOR only", "Topoisomerase I"], "BCL-2 inhibition releases apoptotic signaling, especially in BCL-2-dependent malignancies."),
    ]),
    ("antibodies-car-t-proteins", "Antibodies, CAR T Cells, and Proteins to Treat Cancer", [
        q("Rituximab treats many B-cell malignancies by targeting:", "CD20", ["HER2", "EGFR", "PD-L1"], "CD20 is expressed on many B cells and B-cell lymphomas; rituximab mediates immune clearance."),
        q("Trastuzumab improves HER2-positive breast cancer outcomes but requires monitoring for:", "Cardiomyopathy", ["Hemorrhagic cystitis", "Ototoxicity", "Tumor lysis in every patient"], "HER2 blockade can impair cardiac signaling, especially with anthracyclines."),
        q("Bevacizumab can cause hypertension, bleeding, and impaired wound healing because it blocks:", "VEGF", ["CD20", "CTLA-4", "BCR-ABL"], "VEGF inhibition reduces angiogenesis and affects vascular repair and tone."),
        q("Cetuximab works in metastatic colorectal cancer only when downstream signaling is appropriate; lack of benefit is expected with:", "Activating RAS mutation", ["CD20 positivity", "HER2 amplification", "Low neutrophil count"], "RAS mutations activate downstream MAPK signaling independent of EGFR blockade."),
        q("Pembrolizumab restores antitumor immunity by blocking:", "PD-1 inhibitory checkpoint signaling", ["HER2 dimerization", "VEGF ligand", "CD20 on B cells"], "PD-1 inhibitors release exhausted T-cell responses against tumors."),
        q("A patient on nivolumab develops colitis and thyroiditis. The mechanism is:", "Immune checkpoint blockade causing autoimmune-like toxicity", ["Direct DNA cross-linking", "Microtubule stabilization", "Folate depletion"], "Checkpoint inhibitors can cause immune-related adverse events in multiple organs."),
        q("Ipilimumab differs from pembrolizumab because it targets:", "CTLA-4", ["PD-1", "CD19", "HER2"], "Ipilimumab blocks CTLA-4, enhancing early T-cell activation."),
        q("CAR T-cell therapy for B-ALL often targets:", "CD19", ["BCR-ABL only", "VEGF", "Aromatase"], "CD19-directed CAR T cells recognize B-lineage malignant cells."),
        q("Cytokine release syndrome after CAR T therapy is treated in many cases with:", "Tocilizumab", ["Mesna", "Leucovorin", "Allopurinol only"], "IL-6 receptor blockade with tocilizumab can control severe cytokine release syndrome."),
        q("Antibody-drug conjugates improve selectivity by:", "Delivering a cytotoxic payload to cells expressing a tumor-associated antigen", ["Removing all systemic exposure", "Activating bacterial immunity", "Replacing surgery"], "ADCs combine antibody targeting with potent cytotoxic drugs, though off-target toxicity can still occur."),
    ]),
    ("hormone-cancer-therapy", "Hormones, Hormone Receptor Antagonists, and Related Agents in the Therapy of Cancer", [
        q("Tamoxifen treats ER-positive breast cancer because it:", "Antagonizes estrogen receptors in breast tissue", ["Inhibits aromatase irreversibly in all tissues", "Blocks androgen synthesis", "Activates HER2"], "Tamoxifen is a SERM with breast antiestrogen effects."),
        q("Tamoxifen increases endometrial cancer risk because it:", "Has partial estrogen agonist activity in endometrium", ["Destroys ovarian follicles", "Blocks progesterone receptors completely", "Inhibits VEGF"], "Tissue-selective ER modulation explains benefit and risk."),
        q("Anastrozole is most effective in postmenopausal ER-positive breast cancer because it:", "Blocks peripheral aromatase-mediated estrogen synthesis", ["Blocks ovarian LH receptors directly", "Stimulates estrogen receptors", "Inhibits CD20"], "After menopause, peripheral aromatization is a key estrogen source."),
        q("A premenopausal patient needs ovarian suppression for breast cancer. A long-acting GnRH agonist works by:", "Downregulating pituitary GnRH receptors and lowering LH/FSH", ["Increasing ovulation", "Activating aromatase", "Blocking HER2"], "Continuous GnRH agonist exposure suppresses gonadotropins after initial flare."),
        q("Fulvestrant differs from tamoxifen because it:", "Degrades estrogen receptors", ["Partially agonizes endometrium", "Blocks CYP17", "Activates progesterone receptors"], "Fulvestrant is a selective estrogen receptor degrader."),
        q("Leuprolide for prostate cancer may initially worsen bone pain because:", "Transient LH/testosterone flare occurs before suppression", ["It directly stimulates tumor androgen receptors forever", "It blocks cortisol", "It activates aromatase"], "GnRH agonists cause a flare before pituitary downregulation."),
        q("Degarelix avoids testosterone flare because it is a:", "GnRH receptor antagonist", ["GnRH receptor agonist", "Androgen receptor agonist", "Aromatase inhibitor"], "GnRH antagonists suppress LH rapidly without initial stimulation."),
        q("Enzalutamide treats prostate cancer by:", "Blocking androgen receptor signaling", ["Inhibiting aromatase", "Activating estrogen receptors", "Blocking CD20"], "Androgen receptor pathway inhibition remains central in prostate cancer."),
        q("Abiraterone requires prednisone coadministration because CYP17 inhibition:", "Lowers cortisol and raises ACTH-driven mineralocorticoid excess", ["Raises cortisol dangerously", "Blocks aldosterone receptors", "Activates insulin"], "Glucocorticoid replacement suppresses ACTH and reduces hypertension/hypokalemia."),
        q("Megestrol can improve cancer-related anorexia but may increase risk of:", "Thromboembolism and adrenal suppression", ["Ototoxicity", "Tendon rupture", "Red man syndrome"], "Megestrol is a progestin with appetite effects and endocrine/thrombotic risks."),
    ]),
]


def main():
    questions = []
    for topic_index, (slug, topic, rows) in enumerate(TOPICS):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        for question_index, row in enumerate(rows, 1):
            options = list(row["wrong"])
            answer_index = (topic_index + question_index - 1) % 4
            options.insert(answer_index, row["answer"])
            questions.append({**BASE, "id": f"neoplastic-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "pharmacology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 5 or len(questions) != 50:
        raise AssertionError(f"Expected 5 topics and 50 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 50:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
