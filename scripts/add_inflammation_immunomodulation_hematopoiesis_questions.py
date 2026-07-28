import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Inflammation, Immunomodulation, and Hematopoiesis"
BASE = {"subjectId": "pharmacology", "subjectTitle": "Pharmacology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("immunity-inflammation", "Introduction to Immunity and Inflammation", [
        q("A patient has an acute bacterial skin infection with redness, warmth, swelling, and pain. Which mediator best explains vasodilation and increased vascular permeability early in the response?", "Histamine released from mast cells", ["Erythropoietin from kidney", "Thrombin inhibition", "LDL receptor recycling"], "Histamine rapidly increases blood flow and vascular permeability in acute inflammation."),
        q("A child with recurrent Neisseria infections has a terminal complement defect. Which immune function is most impaired?", "Membrane attack complex formation", ["IgE class switching only", "T-cell thymic selection", "Eosinophil degranulation"], "C5-C9 form the membrane attack complex, important for defense against Neisseria."),
        q("A patient taking high-dose glucocorticoids has poor wound healing. Which anti-inflammatory mechanism contributes?", "Reduced cytokine transcription and leukocyte recruitment", ["Direct activation of neutrophil oxidative burst", "Increased prostaglandin synthesis", "Permanent B-cell immortalization"], "Glucocorticoids broadly suppress inflammatory gene expression and cell trafficking."),
        q("A patient develops fever during infection. The final hypothalamic mediator raising the temperature set point is:", "Prostaglandin E2", ["Bradykinin B2", "Leukotriene B4", "Thromboxane A2"], "IL-1, IL-6, and TNF increase hypothalamic PGE2, causing fever."),
        q("An NSAID lowers fever because it:", "Inhibits cyclooxygenase-dependent prostaglandin synthesis", ["Blocks histamine H1 receptors", "Neutralizes TNF directly", "Activates complement C5"], "COX inhibition reduces PGE2 generation in the hypothalamus."),
        q("A drug blocks leukocyte adhesion to endothelium. Which phase of inflammation is most directly impaired?", "Leukocyte extravasation into tissue", ["Antibody VDJ recombination", "Platelet fibrin cross-linking", "Erythrocyte oxygen delivery"], "Rolling, adhesion, and diapedesis are required for leukocytes to leave blood and enter inflamed tissue."),
        q("A patient with septic shock has profound vasodilation after bacterial endotoxin exposure. Which cytokine is a major early driver?", "TNF-alpha", ["Erythropoietin", "ApoB-100", "Factor IX"], "Macrophage cytokines such as TNF and IL-1 drive systemic inflammatory responses."),
        q("A patient with hereditary angioedema has recurrent swelling without urticaria. The key excess mediator is:", "Bradykinin", ["Dopamine", "Thromboxane", "Erythropoietin"], "C1 esterase inhibitor deficiency increases bradykinin-mediated vascular permeability."),
        q("A patient receives a monoclonal antibody that neutralizes IL-6 receptor signaling. Which inflammatory output should fall?", "Hepatic acute-phase reactant production", ["Vitamin K recycling", "Platelet COX-1 acetylation", "Renal bicarbonate excretion"], "IL-6 strongly stimulates hepatic acute-phase proteins such as CRP."),
        q("A neutrophil reaches an abscess by following an IL-8 gradient. This is an example of:", "Chemotaxis", ["Clonal deletion", "Opsonin-independent erythropoiesis", "Antigenic drift"], "Chemokines guide leukocyte movement toward inflammatory sites."),
    ]),
    ("immunosuppressants-immunomodulation-tolerance", "Immunosuppressants, Immunomodulation, and Tolerance", [
        q("A kidney transplant patient receives tacrolimus. Which signaling step is inhibited?", "Calcineurin-dependent IL-2 transcription", ["mTOR-dependent protein degradation", "TNF receptor binding", "B-cell CD20 expression"], "Tacrolimus-FKBP inhibits calcineurin, reducing IL-2 and T-cell activation."),
        q("Cyclosporine causes hypertension and rising creatinine after transplant. The major dose-limiting toxicity is:", "Nephrotoxicity from renal vasoconstriction", ["Irreversible pulmonary fibrosis", "Severe hypoglycemia", "Hemolysis from G6PD inhibition"], "Calcineurin inhibitors commonly cause nephrotoxicity and hypertension."),
        q("Sirolimus is useful in transplant regimens because it:", "Inhibits mTOR and blocks T-cell proliferation response to IL-2", ["Blocks calcineurin directly", "Depletes CD20 B cells only", "Activates complement"], "Sirolimus binds FKBP but inhibits mTOR rather than calcineurin."),
        q("A patient on mycophenolate has leukopenia and diarrhea. The drug selectively affects lymphocytes because it:", "Inhibits inosine monophosphate dehydrogenase and de novo guanine synthesis", ["Blocks folate absorption in gut only", "Activates adenosine receptors", "Inhibits platelet COX-1"], "Lymphocytes depend heavily on de novo purine synthesis."),
        q("Azathioprine toxicity is severe in a patient with low TPMT activity because:", "Active thiopurine metabolites accumulate", ["Calcineurin becomes overactive", "CD20 is deleted", "IL-6 receptor is stimulated"], "TPMT helps metabolize thiopurines; deficiency increases myelosuppression risk."),
        q("A patient with rheumatoid arthritis improves on methotrexate. At low weekly doses, a key anti-inflammatory effect is:", "Increased extracellular adenosine signaling", ["Complete complement depletion", "Irreversible JAK activation", "Direct histamine release"], "Low-dose methotrexate has anti-inflammatory effects including increased adenosine."),
        q("A patient starting infliximab needs tuberculosis screening because TNF blockade:", "Can reactivate latent granulomatous infection", ["Always causes immediate hypokalemia", "Blocks vitamin K recycling", "Prevents all antibody formation permanently"], "TNF is critical for granuloma maintenance, so latent TB can reactivate."),
        q("A patient with multiple sclerosis is treated with natalizumab and later develops progressive neurologic deficits from PML. The drug blocks:", "Alpha-4 integrin-mediated leukocyte trafficking", ["CD20 on B cells", "IL-1 receptor signaling", "Calcineurin in T cells"], "Natalizumab blocks leukocyte migration into CNS and gut but increases PML risk."),
        q("Rituximab helps some autoimmune diseases by depleting:", "CD20-positive B cells", ["Neutrophils through CXCR2", "Platelets through COX-1", "T cells through CD3 only"], "Rituximab targets CD20 on B cells, reducing antibody-producing lineage precursors."),
        q("A JAK inhibitor improves inflammatory arthritis but increases zoster risk because it:", "Blocks cytokine receptor signaling important for antiviral immunity", ["Activates TNF-alpha", "Stimulates calcineurin", "Inhibits thrombin directly"], "JAK-STAT pathways mediate many cytokine signals; inhibition can raise infection risk."),
    ]),
    ("immune-globulins-vaccines", "Immune Globulins and Vaccines", [
        q("A newborn exposed to hepatitis B receives vaccine plus HBIG. HBIG provides:", "Immediate passive antibody protection", ["Long-term memory T-cell priming only", "Direct antiviral polymerase inhibition", "Complement C9 replacement"], "Immune globulin provides passive antibodies while vaccine induces active immunity."),
        q("A patient bitten by a rabid animal receives rabies immune globulin plus vaccine because:", "Passive antibody bridges the delay before active immunity develops", ["The vaccine is purely analgesic", "Immune globulin activates opioid receptors", "Rabies virus is treated by vitamin K"], "Postexposure prophylaxis combines immediate passive neutralization with active immune priming."),
        q("Live attenuated vaccines are generally avoided in severe immunosuppression because they:", "Can replicate and cause disease", ["Never induce cellular immunity", "Contain only purified toxoid", "Are immediately destroyed by antibodies"], "Live vaccines mimic infection and can be dangerous when immune control is impaired."),
        q("A toxoid vaccine prevents tetanus by inducing antibodies against:", "Inactivated toxin", ["Bacterial ribosomes", "Host acetylcholine receptors", "Viral polymerase"], "Toxoids are inactivated toxins that induce neutralizing antitoxin antibodies."),
        q("Conjugating a polysaccharide antigen to a protein improves infant vaccine response by:", "Recruiting T-cell help for B-cell memory and class switching", ["Blocking all IgG formation", "Eliminating antigen presentation", "Activating platelets"], "Protein conjugation converts a weak T-independent response into a T-dependent response."),
        q("Aluminum salts are used in some vaccines primarily as:", "Adjuvants that enhance immune response", ["Antivirals that block DNA polymerase", "Anticoagulants", "Direct fever suppressants"], "Adjuvants improve antigen immunogenicity and immune activation."),
        q("A patient with primary antibody deficiency receives IVIG. The goal is:", "Replace broad IgG opsonizing and neutralizing activity", ["Stimulate erythropoietin release", "Block factor Xa", "Inhibit histamine H1 receptors"], "IVIG provides pooled IgG to reduce infections in antibody deficiency."),
        q("IVIG can help immune thrombocytopenia rapidly because it:", "Saturates Fc receptors and reduces antibody-coated platelet clearance", ["Inhibits platelet COX permanently", "Activates thrombin", "Blocks vitamin K"], "High-dose IVIG modulates Fc receptor-mediated phagocytosis and immune signaling."),
        q("A vaccine booster works because it:", "Re-expands memory lymphocytes and raises antibody titers", ["Erases primary immune memory", "Depletes complement permanently", "Blocks cytokine receptors"], "Boosters leverage immunologic memory for faster, stronger responses."),
        q("A patient with egg allergy is worried about vaccines. The best pharmacologic principle is:", "Vaccine excipients and production systems matter for specific contraindications", ["All vaccines contain identical allergen amounts", "Passive immunoglobulin is always contraindicated", "Adjuvants are opioid agonists"], "Safety depends on the exact vaccine formulation, allergy severity, and current guidance."),
    ]),
    ("eicosanoids-paf", "Lipid-Derived Autacoids: Eicosanoids and Platelet-Activating Factor", [
        q("Aspirin-exacerbated respiratory disease occurs partly because COX inhibition shifts arachidonic acid metabolism toward:", "Cysteinyl leukotrienes", ["Erythropoietin", "Bradykinin breakdown", "Factor Xa"], "Blocking prostaglandin synthesis can increase leukotriene-mediated bronchoconstriction."),
        q("Montelukast improves asthma symptoms by blocking:", "CysLT1 receptors", ["COX-1", "Thromboxane synthase", "Histamine H2 receptors"], "Montelukast blocks cysteinyl leukotriene receptors, reducing bronchoconstriction and inflammation."),
        q("Zileuton requires liver enzyme monitoring because it inhibits:", "5-lipoxygenase", ["Cyclooxygenase irreversibly", "P2Y12 receptors", "Factor IIa"], "Zileuton blocks leukotriene synthesis via 5-LOX and can cause hepatotoxicity."),
        q("Low-dose aspirin prevents thrombosis mainly by reducing platelet:", "Thromboxane A2", ["Prostacyclin receptor density", "Leukotriene B4", "Histamine"], "Platelet COX-1 inhibition lowers TXA2-mediated aggregation and vasoconstriction."),
        q("Prostacyclin analogs help pulmonary arterial hypertension because prostacyclin:", "Raises cAMP causing vasodilation and platelet inhibition", ["Activates thromboxane receptors", "Blocks beta-2 receptors", "Stimulates aldosterone"], "PGI2 signaling dilates vascular smooth muscle and inhibits platelet activation."),
        q("Misoprostol protects the stomach in NSAID users because it is a:", "PGE1 analog increasing mucus and bicarbonate", ["TXA2 receptor blocker", "Leukotriene receptor agonist", "PAF antagonist"], "Prostaglandins support gastric mucosal defense; misoprostol replaces that effect."),
        q("Dinoprostone is used clinically because PGE2 can:", "Ripen the cervix and stimulate uterine contractions", ["Reverse heparin", "Block H1 receptors", "Lower LDL"], "PGE2 preparations are used for cervical ripening and labor induction in selected settings."),
        q("A patient with allergic inflammation has leukocyte chemotaxis driven strongly by:", "Leukotriene B4", ["Prostacyclin", "Erythropoietin", "Albumin"], "LTB4 is a potent neutrophil chemoattractant and activator."),
        q("Platelet-activating factor contributes to inflammation by:", "Promoting platelet aggregation, bronchoconstriction, and vascular permeability", ["Inhibiting all leukocyte adhesion", "Replacing vitamin K", "Blocking IL-2 transcription"], "PAF is a phospholipid mediator with platelet and inflammatory vascular effects."),
        q("Celecoxib has less gastric toxicity than nonselective NSAIDs because it preferentially spares:", "COX-1-derived gastric protective prostaglandins", ["5-lipoxygenase-derived leukotrienes", "Thrombin generation", "Histamine metabolism"], "COX-2 selectivity reduces but does not eliminate GI risk by sparing COX-1 at usual doses."),
    ]),
    ("inflammation-fever-pain-gout", "Pharmacotherapy of Inflammation, Fever, Pain, and Gout", [
        q("A patient with acute gout and CKD cannot use NSAIDs. Colchicine helps because it:", "Inhibits microtubule-dependent neutrophil migration and activation", ["Blocks uric acid synthesis directly", "Dissolves urate crystals instantly", "Inhibits xanthine oxidase irreversibly"], "Colchicine reduces neutrophil-driven inflammation in gout flares."),
        q("Allopurinol prevents gout flares long term by inhibiting:", "Xanthine oxidase", ["URAT1", "Cyclooxygenase-2", "IL-1 receptor"], "Xanthine oxidase inhibition lowers uric acid production."),
        q("Starting allopurinol during uncontrolled gout without flare prophylaxis can:", "Precipitate or worsen an acute flare", ["Cause immediate urate stone dissolution only", "Prevent all future pain within minutes", "Block platelet aggregation"], "Changing urate levels can mobilize crystals; prophylaxis is often used at initiation."),
        q("Probenecid lowers urate by:", "Inhibiting renal tubular urate reabsorption", ["Inhibiting xanthine oxidase", "Blocking IL-1 beta", "Activating COX-1"], "Uricosurics increase urate excretion but require adequate renal function and hydration."),
        q("A patient with peptic ulcer disease worsens after ibuprofen because nonselective NSAIDs:", "Reduce gastric protective prostaglandins", ["Increase mucus and bicarbonate", "Block histamine H1 receptors", "Neutralize acid directly"], "COX-1-derived prostaglandins help maintain gastric mucosal protection."),
        q("Acetaminophen overdose is treated with N-acetylcysteine because it:", "Replenishes glutathione to detoxify NAPQI", ["Blocks opioid receptors", "Inhibits COX irreversibly in platelets", "Chelates iron"], "NAC restores glutathione and is most effective when given early."),
        q("Aspirin is avoided in children with viral illness because of risk of:", "Reye syndrome", ["Serotonin syndrome", "Gray baby syndrome", "Torsades"], "Aspirin use in children with viral infections is associated with Reye syndrome."),
        q("Indomethacin closes a patent ductus arteriosus because it:", "Inhibits prostaglandin synthesis", ["Activates PGE receptors", "Blocks thrombin", "Stimulates nitric oxide"], "Prostaglandins keep the ductus open; NSAIDs promote closure."),
        q("Celecoxib should be used cautiously in high cardiovascular-risk patients because COX-2 inhibition can:", "Tilt balance toward thrombosis by sparing platelet thromboxane", ["Cause universal bronchospasm", "Reverse warfarin", "Block urate production"], "Reduced endothelial prostacyclin with preserved platelet TXA2 may increase thrombotic risk."),
        q("Anakinra can help refractory gout flares by blocking:", "IL-1 receptor signaling", ["TNF-alpha converting enzyme only", "Histamine H2 receptors", "Vitamin K recycling"], "Urate crystals activate inflammasome IL-1 beta pathways; IL-1 blockade can reduce inflammation."),
    ]),
    ("histamine-bradykinin-antagonists", "Histamine, Bradykinin, and Their Antagonists", [
        q("A patient with allergic rhinitis improves with cetirizine. The drug blocks:", "H1 receptors", ["H2 receptors", "B2 bradykinin receptors", "CysLT1 receptors"], "Second-generation H1 antihistamines reduce sneezing, itching, and rhinorrhea with less sedation."),
        q("Diphenhydramine causes sedation and urinary retention because it:", "Crosses the BBB and has antimuscarinic activity", ["Activates beta-2 receptors", "Blocks factor Xa", "Stimulates H2 receptors"], "First-generation H1 blockers are sedating and often anticholinergic."),
        q("Famotidine reduces gastric acid secretion by blocking:", "H2 receptors on parietal cells", ["H1 receptors on mast cells", "Bradykinin B2 receptors", "Leukotriene receptors"], "Histamine stimulates parietal cell acid secretion via H2 receptors."),
        q("A patient with ACE-inhibitor angioedema has swelling without hives. The key mediator is:", "Bradykinin", ["Histamine", "Thromboxane", "Dopamine"], "ACE inhibition reduces bradykinin breakdown, causing nonurticarial angioedema."),
        q("Icatibant treats hereditary angioedema by blocking:", "Bradykinin B2 receptors", ["H1 receptors", "IL-6 receptors", "P2Y12 receptors"], "Icatibant is a B2 receptor antagonist for bradykinin-mediated angioedema."),
        q("C1 esterase inhibitor concentrate helps hereditary angioedema because it:", "Restores regulation of kallikrein-bradykinin generation", ["Blocks mast cell histamine release only", "Inhibits thromboxane synthase", "Activates complement C5"], "C1-INH deficiency causes excess kallikrein activity and bradykinin formation."),
        q("A patient taking a first-generation antihistamine before driving is at risk because these drugs:", "Impair alertness and psychomotor performance", ["Cause immediate platelet lysis", "Induce severe hyperthyroidism", "Activate NMDA receptors"], "Sedating antihistamines can impair driving and cognition."),
        q("Omalizumab reduces allergic asthma exacerbations by binding:", "IgE", ["Histamine H1 receptor", "Bradykinin", "COX-2"], "Anti-IgE therapy reduces free IgE and downstream mast cell/basophil activation."),
        q("Epinephrine is first-line for anaphylaxis because it:", "Reverses airway edema, bronchospasm, and hypotension through adrenergic effects", ["Only blocks H1 receptors", "Only reduces itching", "Slowly inhibits IL-5"], "Epinephrine provides alpha vasoconstriction and beta bronchodilator/cardiac support."),
        q("A patient with chronic spontaneous urticaria not controlled with standard dosing may benefit from:", "Up-dosed second-generation H1 antihistamine or anti-IgE therapy", ["Warfarin", "Allopurinol", "Digoxin"], "Guidelines often escalate non-sedating H1 blockers and consider omalizumab in refractory disease."),
    ]),
    ("pulmonary-pharmacology", "Pulmonary Pharmacology", [
        q("Albuterol relieves acute bronchospasm by:", "Stimulating beta-2 receptors to increase airway smooth muscle cAMP", ["Blocking muscarinic M2 receptors only", "Inhibiting IL-5", "Activating thromboxane receptors"], "Short-acting beta-2 agonists rapidly relax airway smooth muscle."),
        q("A patient overuses albuterol and develops tremor and tachycardia. These effects reflect:", "Beta receptor stimulation outside the airway", ["Factor Xa inhibition", "H1 blockade", "Xanthine oxidase inhibition"], "Beta-2 agonists can cause tremor, tachycardia, and hypokalemia."),
        q("Ipratropium helps COPD because it:", "Blocks muscarinic bronchoconstriction with limited systemic absorption", ["Stimulates beta-1 receptors", "Blocks IL-4 receptors", "Inhibits COX irreversibly"], "Inhaled quaternary antimuscarinics reduce vagal bronchoconstriction."),
        q("Inhaled corticosteroids reduce asthma exacerbations mainly by:", "Suppressing airway inflammatory gene expression", ["Directly relaxing smooth muscle within seconds", "Blocking acetylcholine at Nm receptors", "Opening potassium channels in heart"], "ICS are controller drugs that reduce airway inflammation and hyperresponsiveness."),
        q("A patient using inhaled fluticasone develops oral candidiasis. Prevention is best with:", "Mouth rinsing after inhalation", ["Taking extra aspirin", "Avoiding spacer devices", "Adding warfarin"], "Rinsing and spacer use reduce local steroid deposition and thrush risk."),
        q("Salmeterol should not be used alone in asthma because LABA monotherapy:", "Can increase severe asthma risk without anti-inflammatory control", ["Cannot bronchodilate", "Always causes renal failure", "Blocks corticosteroid receptors"], "LABAs in asthma should be paired with inhaled corticosteroid therapy."),
        q("Montelukast is especially useful in aspirin-sensitive asthma because it:", "Blocks cysteinyl leukotriene signaling", ["Inhibits HMG-CoA reductase", "Blocks factor Xa", "Activates beta-1 receptors"], "Leukotrienes are important in aspirin-exacerbated respiratory disease."),
        q("Omalizumab is considered for allergic asthma with high IgE because it:", "Binds free IgE and reduces Fc-epsilon receptor activation", ["Blocks IL-5 receptor directly", "Stimulates beta-2 receptors", "Inhibits PDE4"], "Anti-IgE therapy reduces allergic inflammatory signaling."),
        q("Mepolizumab benefits eosinophilic asthma by targeting:", "IL-5", ["TNF-alpha", "Bradykinin B2", "Thromboxane A2"], "IL-5 promotes eosinophil growth, activation, and survival."),
        q("Roflumilast can reduce COPD exacerbations but commonly causes:", "Weight loss and gastrointestinal adverse effects", ["Gingival hyperplasia", "Ototoxicity", "Hypouricemia"], "Roflumilast is a PDE4 inhibitor with anti-inflammatory effects and GI/weight-loss toxicity."),
    ]),
    ("hematopoietic-agents", "Hematopoietic Agents: Growth Factors, Minerals, and Vitamins", [
        q("A CKD patient with anemia receives epoetin alfa. The intended response requires adequate:", "Iron stores", ["Platelet P2Y12 blockade", "Vitamin K antagonism", "Histamine release"], "Erythropoiesis-stimulating agents need iron substrate to produce hemoglobin."),
        q("Epoetin therapy targeting too high a hemoglobin increases risk of:", "Thrombosis and hypertension", ["Severe hypocalcemia only", "Bronchospasm from leukotrienes", "Opioid withdrawal"], "Overcorrection with ESAs increases cardiovascular and thrombotic risk."),
        q("Filgrastim after chemotherapy reduces infection risk by stimulating:", "Neutrophil production through G-CSF receptors", ["Platelet aggregation through TXA2", "Red cell destruction", "B-cell CD20 expression"], "G-CSF promotes neutrophil proliferation and maturation."),
        q("Sargramostim differs from filgrastim because it is:", "GM-CSF and stimulates broader myeloid lineages", ["A direct thrombin inhibitor", "A vitamin B12 analog", "An H1 blocker"], "GM-CSF affects granulocyte and macrophage lineages more broadly than G-CSF."),
        q("Romiplostim helps immune thrombocytopenia by activating:", "Thrombopoietin receptors", ["Erythropoietin receptors", "H1 receptors", "CysLT1 receptors"], "TPO receptor agonists increase platelet production."),
        q("Iron deficiency anemia with poor oral tolerance is treated with IV iron. A key safety concern is:", "Infusion reactions and iron overload if misused", ["Immediate vitamin K reversal", "Torsades in all patients", "ACE-inhibitor cough"], "IV iron bypasses absorption limits but requires monitoring for reactions and excess iron."),
        q("A vegan patient with macrocytic anemia and neuropathy most likely needs:", "Vitamin B12", ["Vitamin K", "Copper only", "Erythropoietin alone"], "B12 deficiency causes megaloblastic anemia and neurologic dysfunction."),
        q("Folate corrects anemia in B12 deficiency but is dangerous alone because it:", "May allow neurologic injury to progress", ["Causes immediate hemolysis", "Blocks neutrophil production", "Induces angioedema"], "Folate can improve megaloblastosis while masking ongoing B12-related neurologic damage."),
        q("Hydroxocobalamin is useful in cyanide poisoning because it:", "Binds cyanide to form cyanocobalamin", ["Blocks COX-2", "Activates thrombin", "Inhibits xanthine oxidase"], "Hydroxocobalamin scavenges cyanide and is also a B12 form."),
        q("Vitamin K is given to reverse warfarin because it restores:", "Gamma-carboxylation of clotting factors II, VII, IX, and X", ["Platelet COX-1 activity", "Fibrin breakdown", "Erythropoietin receptor signaling"], "Vitamin K is required for hepatic activation of vitamin K-dependent clotting factors."),
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
            questions.append({**BASE, "id": f"inflamm-immuno-heme-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "pharmacology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 8 or len(questions) != 80:
        raise AssertionError(f"Expected 8 topics and 80 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 80:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
