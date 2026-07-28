import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Special Systems Pharmacology"
BASE = {"subjectId": "pharmacology", "subjectTitle": "Pharmacology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("ocular-pharmacology", "Ocular Pharmacology", [
        q("A patient with open-angle glaucoma is started on latanoprost at night. The main pressure-lowering mechanism is:", "Increased uveoscleral outflow", ["Reduced aqueous production by beta blockade", "Miosis from cholinesterase inhibition", "Osmotic dehydration of vitreous only"], "Prostaglandin analogs increase uveoscleral outflow and are common first-line glaucoma therapy."),
        q("A patient using latanoprost notices darker irides and longer eyelashes. This adverse effect is due to:", "Prostaglandin receptor effects on melanocytes and hair follicles", ["Beta-1 blockade", "Carbonic anhydrase inhibition", "Alpha-2 antagonism"], "Prostaglandin analogs can cause iris pigmentation, eyelash growth, and periocular changes."),
        q("Timolol eye drops lower intraocular pressure by:", "Reducing aqueous humor production", ["Increasing lens accommodation", "Blocking prostaglandin receptors", "Increasing trabecular pigment release"], "Topical beta blockers reduce ciliary body aqueous humor production."),
        q("A patient with asthma becomes short of breath after timolol eye drops. The reason is:", "Systemic absorption causing beta-2 blockade", ["Local corneal anesthesia", "Alpha-1 stimulation", "Muscarinic agonism"], "Even topical ophthalmic beta blockers can be systemically absorbed and provoke bronchospasm."),
        q("Dorzolamide helps glaucoma because it inhibits:", "Carbonic anhydrase in the ciliary body", ["Cyclooxygenase in conjunctiva", "H1 receptors in iris", "Na/K-ATPase in retina"], "Carbonic anhydrase inhibitors reduce bicarbonate-dependent aqueous humor secretion."),
        q("Acetazolamide is used acutely for high intraocular pressure but can cause:", "Metabolic acidosis and paresthesias", ["Ototoxicity from hair cell uptake", "Tendon rupture", "Agranulocytosis as the classic toxicity"], "Systemic carbonic anhydrase inhibition causes bicarbonaturia, acidosis, and electrolyte effects."),
        q("Pilocarpine can open the trabecular meshwork in angle-closure glaucoma by:", "Contracting ciliary muscle and producing miosis", ["Relaxing the iris sphincter", "Blocking M3 receptors", "Increasing aqueous secretion"], "Muscarinic agonists constrict the pupil and contract ciliary muscle, improving trabecular outflow."),
        q("Apraclonidine lowers intraocular pressure after laser procedures mainly through:", "Alpha-2 agonism reducing aqueous production", ["Beta-2 agonism increasing outflow", "H1 blockade", "Direct osmotic vitreous shrinkage"], "Topical alpha-2 agonists reduce aqueous humor production and may increase outflow."),
        q("Intravitreal anti-VEGF therapy for wet macular degeneration works by:", "Reducing pathologic choroidal neovascularization and leakage", ["Increasing lens transparency", "Blocking retinal dopamine", "Stimulating aqueous humor production"], "VEGF drives abnormal vessel growth and leakage in neovascular AMD."),
        q("Topical tropicamide is used for fundus examination because it:", "Blocks muscarinic receptors causing mydriasis and cycloplegia", ["Activates alpha-2 receptors", "Blocks beta receptors", "Inhibits carbonic anhydrase"], "Antimuscarinics dilate the pupil and paralyze accommodation."),
    ]),
    ("dermatological-pharmacology", "Dermatological Pharmacology", [
        q("A patient with plaque psoriasis improves with topical calcipotriene. The mechanism is:", "Vitamin D receptor activation normalizing keratinocyte proliferation and differentiation", ["Beta-lactamase inhibition", "Histamine H2 blockade", "Opioid receptor antagonism"], "Vitamin D analogs regulate epidermal growth and immune activity in psoriasis."),
        q("High-potency topical corticosteroids improve eczema because they:", "Suppress local inflammatory gene expression", ["Directly kill dermatophytes", "Block bacterial ribosomes", "Stimulate keratinocyte overgrowth"], "Topical glucocorticoids reduce cytokines, vasodilation, and immune cell activity."),
        q("A patient using clobetasol on the face develops skin thinning and telangiectasias. This is due to:", "Local corticosteroid-induced dermal atrophy", ["Retinoid-induced collagen excess", "Antifungal toxicity", "Beta-blocker absorption"], "Potent topical steroids can cause atrophy, striae, telangiectasias, and perioral dermatitis."),
        q("Tacrolimus ointment is useful for atopic dermatitis on thin skin because it:", "Inhibits calcineurin without causing steroid atrophy", ["Inhibits fungal ergosterol synthesis", "Blocks histamine H1 receptors", "Activates vitamin D receptors"], "Topical calcineurin inhibitors reduce T-cell cytokine signaling and avoid steroid skin thinning."),
        q("Topical benzoyl peroxide helps acne partly by:", "Generating free radicals toxic to Cutibacterium acnes", ["Blocking androgen receptors systemically", "Inhibiting calcineurin", "Activating opioid receptors"], "Benzoyl peroxide is antibacterial and comedolytic and does not cause bacterial resistance alone."),
        q("Isotretinoin is highly effective for severe nodulocystic acne because it:", "Shrinks sebaceous glands and reduces sebum production", ["Only blocks H1 receptors", "Stimulates bacterial folate synthesis", "Activates estrogen receptors"], "Systemic retinoids target sebaceous gland activity, comedogenesis, and inflammation."),
        q("A woman starting isotretinoin must use strict pregnancy prevention because it is:", "Highly teratogenic", ["A strong opioid agonist", "A live vaccine", "A beta-lactam"], "Isotretinoin can cause severe birth defects and requires pregnancy prevention programs."),
        q("Terbinafine treats tinea corporis by inhibiting:", "Fungal squalene epoxidase", ["Bacterial DNA gyrase", "Human cyclooxygenase", "Viral neuraminidase"], "Terbinafine blocks ergosterol synthesis and accumulates in keratinized tissue."),
        q("Permethrin treats scabies because it:", "Disrupts arthropod sodium channel function", ["Blocks fungal beta-glucan", "Inhibits human histamine release", "Chelates iron"], "Permethrin is a pyrethroid neurotoxin for mites and lice with low mammalian toxicity when used properly."),
        q("Topical minoxidil promotes hair growth most plausibly by:", "Shortening telogen and prolonging anagen through follicular vascular/signaling effects", ["Blocking 5-alpha-reductase in serum only", "Activating glucocorticoid receptors", "Killing dermatophytes"], "Minoxidil promotes hair growth through follicular effects; irritation and unwanted hair growth can occur."),
    ]),
    ("environmental-toxicology", "Environmental Toxicology", [
        q("A child with abdominal pain, anemia, and developmental delay has elevated lead level. Chelation with succimer is useful because it:", "Binds lead and increases urinary excretion", ["Activates heme synthesis", "Blocks opioid receptors", "Inhibits acetylcholinesterase"], "Succimer is an oral chelator used for lead poisoning in appropriate cases."),
        q("Lead poisoning causes microcytic anemia partly by inhibiting:", "ALA dehydratase and ferrochelatase", ["Vitamin K epoxide reductase", "Na/K-ATPase only", "HMG-CoA reductase"], "Lead disrupts heme synthesis enzymes, producing anemia and basophilic stippling."),
        q("A patient with severe arsenic or mercury poisoning may be treated with dimercaprol because it:", "Provides sulfhydryl groups that bind heavy metals", ["Oxidizes metals into gas", "Blocks NMDA receptors", "Activates CYP enzymes"], "Dimercaprol chelates certain heavy metals through thiol binding."),
        q("Iron overdose with vomiting, metabolic acidosis, and shock is treated with:", "Deferoxamine", ["Naloxone", "Atropine", "Protamine"], "Deferoxamine chelates iron and is used in severe iron poisoning."),
        q("A patient exposed to carbon monoxide has normal PaO2 but low oxygen content. Hyperbaric oxygen helps by:", "Accelerating dissociation of CO from hemoglobin and improving tissue oxygen delivery", ["Blocking CO production in mitochondria", "Chelating hemoglobin", "Activating beta receptors"], "CO binds hemoglobin with high affinity and impairs oxygen delivery; oxygen shortens carboxyhemoglobin half-life."),
        q("Cyanide poisoning after smoke inhalation causes lactic acidosis because cyanide:", "Inhibits mitochondrial cytochrome oxidase", ["Blocks hemoglobin iron only", "Activates oxidative phosphorylation", "Inhibits acetylcholinesterase"], "Cyanide prevents cellular oxygen utilization, causing histotoxic hypoxia and lactic acidosis."),
        q("Hydroxocobalamin treats cyanide poisoning by:", "Binding cyanide to form cyanocobalamin", ["Blocking opioid receptors", "Reactivating cytochrome oxidase directly", "Chelating lead"], "Hydroxocobalamin scavenges cyanide and is commonly used in smoke-inhalation cyanide toxicity."),
        q("Organophosphate poisoning with salivation, bronchorrhea, fasciculations, and miosis requires atropine plus pralidoxime because:", "Atropine blocks muscarinic effects while pralidoxime can reactivate acetylcholinesterase before aging", ["Both drugs block opioid receptors", "Atropine reactivates AChE and pralidoxime dries secretions", "Both inhibit acetylcholine release"], "Organophosphates inhibit acetylcholinesterase; treatment addresses muscarinic crisis and enzyme reactivation."),
        q("Nitrate-contaminated well water can cause infant cyanosis because nitrates produce:", "Methemoglobinemia", ["Carboxyhemoglobinemia", "Lead encephalopathy", "Cyanide binding to cobalt"], "Nitrates oxidize hemoglobin iron, impairing oxygen delivery; infants are vulnerable."),
        q("Methylene blue treats significant methemoglobinemia by:", "Reducing ferric iron in hemoglobin back to ferrous iron", ["Chelating lead", "Binding cyanide", "Blocking muscarinic receptors"], "Methylene blue accelerates reduction of methemoglobin via NADPH-dependent pathways; caution is needed in G6PD deficiency."),
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
            questions.append({**BASE, "id": f"special-systems-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "pharmacology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 3 or len(questions) != 30:
        raise AssertionError(f"Expected 3 topics and 30 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 30:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
