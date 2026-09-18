"""Build USMLE Step 1 integrated practice items for Module 2.

These items are authored from core medical knowledge and intentionally avoid
page-level textbook extraction. Each stem is written so the final lead-in
depends on interpreting the vignette first.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_ID = "usmle-module-02"


def lab(test, value, reference):
    return {"test": test, "value": value, "reference": reference}


def q(number, disciplines, system, topic, prompt, lead_in, choices, answer_index,
      explanation, objective, reasoning, family="mechanism", labs=None):
    return {
        "id": f"{MODULE_ID}-q{number:03d}",
        "moduleId": MODULE_ID,
        "questionNumber": number,
        "subjectId": MODULE_ID,
        "subjectTitle": "Module 2",
        "examId": "usmle-step-1",
        "examTitle": "USMLE Step 1 - Integrated Practice",
        "source": "usmle",
        "topic": topic,
        "organSystem": system,
        "disciplines": disciplines,
        "itemFamily": family,
        "difficulty": "integrated",
        "prompt": prompt,
        "leadIn": lead_in,
        "options": [choice[0] for choice in choices],
        "answerIndex": answer_index,
        "answer": choices[answer_index][0],
        "optionExplanations": [choice[1] for choice in choices],
        "explanation": explanation,
        "educationalObjective": objective,
        "reasoningChain": reasoning,
        "references": [],
        "laboratoryFindings": labs or [],
        "imageUrls": [],
        "tags": ["usmle-step-1", "integrated", "module-2", *[d.lower().replace(" ", "-") for d in disciplines]],
    }


QUESTIONS = [
    q(1, ["Immunology", "Pathology", "Behavioral science"], "Hematologic",
      "Antiphospholipid syndrome",
      "A 31-year-old woman is evaluated after a painful swollen calf is diagnosed as a deep venous thrombosis. She has had three spontaneous pregnancy losses at 11 to 14 weeks' gestation. She has no history of heavy bleeding. Platelet count is mildly decreased, and screening for syphilis has been falsely positive twice. Coagulation studies show a prolonged activated partial thromboplastin time that does not correct after mixing with normal plasma.",
      "The antibodies responsible for this patient's disorder most directly bind which of the following targets?",
      [
          ("Phospholipid-binding plasma proteins", "Correct. Antiphospholipid antibodies commonly bind beta2-glycoprotein I or prothrombin on phospholipid surfaces, causing thrombosis and pregnancy morbidity despite a prolonged in vitro clotting test."),
          ("Platelet glycoprotein IIb/IIIa", "Antibodies against platelet glycoprotein IIb/IIIa cause immune thrombocytopenia with mucocutaneous bleeding rather than recurrent thrombosis and fetal loss."),
          ("Double-stranded DNA", "Anti-dsDNA antibodies support systemic lupus erythematosus and immune complex nephritis, but they do not explain this thrombotic laboratory pattern."),
          ("Factor VIII", "A factor VIII inhibitor causes bleeding and a prolonged aPTT that fails to correct, but it does not produce recurrent venous thrombosis and pregnancy loss."),
          ("Von Willebrand factor", "Defective von Willebrand factor function causes platelet-type mucosal bleeding and may prolong aPTT through factor VIII effects; thrombosis is not typical."),
      ],
      0,
      "Recurrent fetal loss, venous thrombosis, false-positive syphilis testing, thrombocytopenia, and a prolonged aPTT without clinical bleeding point to antiphospholipid syndrome. The paradox is that these antibodies prolong phospholipid-dependent clotting assays in vitro but promote thrombosis in vivo.",
      "Recognize antiphospholipid syndrome from thrombotic events plus misleading coagulation tests.",
      "Pregnancy loss + DVT + false-positive syphilis + prolonged aPTT without bleeding -> antiphospholipid syndrome -> antibodies to phospholipid-binding proteins.",
      labs=[lab("Platelets", "118,000/mm3", "150,000-400,000/mm3"), lab("aPTT", "58 sec", "25-35 sec")]),

    q(2, ["Immunology", "Microbiology", "Genetics"], "Immune system",
      "X-linked agammaglobulinemia",
      "A 9-month-old boy has had three episodes of otitis media and one episode of pneumonia since he stopped breastfeeding. He appears well between infections. Physical examination shows absent tonsillar tissue and no palpable cervical lymph nodes. Flow cytometry shows very few circulating CD19+ cells; T-cell number and function are normal. His maternal uncle died in childhood of recurrent bacterial infections.",
      "The mutated protein in this patient normally functions at which step of lymphocyte development?",
      [
          ("Signal transduction from the pre-B-cell receptor", "Correct. Bruton's tyrosine kinase transduces signals required for maturation past the pre-B-cell stage. Failure causes absent mature B cells and markedly decreased immunoglobulins."),
          ("Somatic hypermutation in germinal centers", "Activation-induced cytidine deaminase defects impair class switching and affinity maturation but do not eliminate circulating B cells or tonsils."),
          ("V(D)J recombination in early T and B cells", "RAG defects cause severe combined immunodeficiency with both T-cell and B-cell dysfunction, not isolated absent mature B cells."),
          ("Respiratory burst in neutrophil phagosomes", "NADPH oxidase defects cause chronic granulomatous disease with catalase-positive infections; lymphoid tissue is not absent from failed B-cell maturation."),
          ("Complement C3 cleavage on microbial surfaces", "C3 deficiency causes severe recurrent pyogenic infections but does not explain absent B cells and X-linked family history."),
      ],
      0,
      "Infections beginning after maternal IgG wanes, absent tonsils, absent B-cell markers, and normal T-cell function indicate X-linked agammaglobulinemia. The defective gene encodes Bruton's tyrosine kinase, a pre-B-cell receptor signaling protein.",
      "Use infection timing and lymphoid tissue findings to identify failed B-cell maturation.",
      "Male infant + infections after 6 months + absent tonsils/B cells + normal T cells -> BTK deficiency -> impaired pre-B-cell receptor signaling."),

    q(3, ["Endocrinology", "Biochemistry", "Pathology"], "Endocrine",
      "Congenital adrenal hyperplasia",
      "A 5-day-old infant is brought to the emergency department because of poor feeding, vomiting, and lethargy. The infant is dehydrated and hypotensive. External genitalia are virilized despite a 46,XX karyotype. Serum sodium is low, potassium is high, glucose is low, and plasma ACTH is markedly increased.",
      "Which steroid precursor is most likely to be markedly increased in this patient?",
      [
          ("17-hydroxyprogesterone", "Correct. 21-hydroxylase deficiency blocks cortisol and aldosterone synthesis, increasing ACTH and shunting precursors toward androgens. 17-hydroxyprogesterone accumulates."),
          ("11-deoxycorticosterone", "11-beta-hydroxylase deficiency increases 11-deoxycorticosterone, causing hypertension rather than salt wasting and hyperkalemia."),
          ("Corticosterone", "Corticosterone is downstream of mineralocorticoid synthesis and would not accumulate when 21-hydroxylase is deficient."),
          ("Estriol", "Estriol is a placental estrogen and does not explain neonatal salt wasting with virilization."),
          ("Dihydrotestosterone", "DHT mediates external male genital development. It may be increased indirectly, but it is not the diagnostic accumulated adrenal precursor."),
      ],
      0,
      "The combination of neonatal salt wasting, hypotension, hyperkalemia, hypoglycemia, virilization in a genetic female, and high ACTH is classic for 21-hydroxylase deficiency. Low cortisol and aldosterone production removes feedback inhibition and drives adrenal androgen excess.",
      "Connect salt-wasting congenital adrenal hyperplasia to the accumulated precursor 17-hydroxyprogesterone.",
      "Newborn shock + hyperkalemia + 46,XX virilization + high ACTH -> 21-hydroxylase deficiency -> high 17-hydroxyprogesterone.",
      labs=[lab("Sodium", "125 mEq/L", "135-145 mEq/L"), lab("Potassium", "6.5 mEq/L", "3.5-5.0 mEq/L"), lab("Glucose", "42 mg/dL", "70-100 mg/dL")]),

    q(4, ["Biochemistry", "Renal", "Genetics"], "Renal",
      "Cystinuria",
      "An 8-year-old boy has recurrent flank pain and hematuria. His father had kidney stones as a teenager. Urinalysis shows hexagon-shaped crystals, and stone analysis identifies a poorly soluble amino acid. A cyanide-nitroprusside screening test is positive.",
      "A defect in the same proximal tubular transporter would also impair reabsorption of which amino acid?",
      [
          ("Lysine", "Correct. Cystinuria impairs renal and intestinal transport of cystine and the dibasic amino acids ornithine, lysine, and arginine."),
          ("Phenylalanine", "Phenylalanine is not transported by the cystine/dibasic amino acid transporter. Phenylketonuria involves phenylalanine hydroxylase or tetrahydrobiopterin pathways."),
          ("Tryptophan", "Neutral amino acid transport defects can cause Hartnup disease, which presents with pellagra-like findings rather than hexagonal cystine stones."),
          ("Glutamate", "Glutamate is acidic, not dibasic, and is not part of the COLA group lost in cystinuria."),
          ("Methionine", "Methionine is neutral and sulfur-containing, but it is not the poorly soluble amino acid forming hexagonal stones in cystinuria."),
      ],
      0,
      "Hexagonal urinary crystals identify cystine stones. The mnemonic COLA describes the amino acids with impaired transport in cystinuria: cystine, ornithine, lysine, and arginine. Cystine is least soluble and precipitates in urine.",
      "Infer cystinuria from stone morphology and link it to dibasic amino acid transport.",
      "Childhood recurrent stones + hexagonal crystals + positive cyanide-nitroprusside -> cystinuria -> impaired cystine, ornithine, lysine, arginine transport."),

    q(5, ["Biochemistry", "Genetics", "Neurology"], "Musculoskeletal/Neurologic",
      "Purine salvage",
      "A 4-year-old boy is evaluated for developmental delay, involuntary writhing movements, and repeated biting of his lips and fingers. His parents report orange sand-like material in his diapers during infancy. Serum uric acid is elevated.",
      "Loss of the deficient enzyme most directly increases de novo purine synthesis through accumulation of which substrate?",
      [
          ("5-phosphoribosyl-1-pyrophosphate", "Correct. HGPRT deficiency prevents salvage of hypoxanthine and guanine. PRPP accumulates and drives de novo purine synthesis, increasing uric acid production."),
          ("Inosine monophosphate", "IMP is a purine nucleotide product that normally helps inhibit de novo synthesis; it is not the accumulated driver in this disorder."),
          ("Uridine monophosphate", "UMP is a pyrimidine nucleotide and is not the signal that drives excess purine synthesis in HGPRT deficiency."),
          ("Carbamoyl phosphate", "Carbamoyl phosphate accumulation is relevant to ornithine transcarbamylase deficiency and orotic aciduria, not self-injury with hyperuricemia."),
          ("S-adenosylmethionine", "S-adenosylmethionine is a methyl donor and does not explain purine overproduction in Lesch-Nyhan syndrome."),
      ],
      0,
      "Self-injurious behavior, dystonia, developmental delay, and hyperuricemia indicate Lesch-Nyhan syndrome due to HGPRT deficiency. Failed purine salvage leaves PRPP unused and stimulates de novo purine synthesis.",
      "Recognize HGPRT deficiency and the biochemical reason for increased uric acid.",
      "Self-mutilation + movement disorder + orange urate crystals -> HGPRT deficiency -> PRPP accumulation -> increased de novo purines."),

    q(6, ["Biochemistry", "Pathology", "Genetics"], "Hepatobiliary",
      "Wilson disease",
      "A 17-year-old boy is brought by his parents because of declining school performance, new irritability, and a coarse tremor. Examination shows brown-green rings at the corneal margins. Aminotransferase levels are increased, serum ceruloplasmin is low, and he has Coombs-negative hemolytic anemia.",
      "The defective protein in this patient normally has which function?",
      [
          ("Copper incorporation into ceruloplasmin and biliary copper excretion", "Correct. Wilson disease is due to ATP7B dysfunction in hepatocytes, impairing copper loading onto ceruloplasmin and copper excretion into bile."),
          ("Copper export from intestinal enterocytes into portal blood", "This describes ATP7A, which is defective in Menkes disease and causes kinky hair, neurodegeneration, and copper deficiency."),
          ("Iron export from enterocytes and macrophages", "Ferroportin exports iron. Defects in iron handling cause hemochromatosis or iron-restricted anemia patterns, not Kayser-Fleischer rings."),
          ("Lysosomal degradation of sphingomyelin", "Sphingomyelinase deficiency causes Niemann-Pick disease with neurodegeneration and hepatosplenomegaly, not low ceruloplasmin."),
          ("Peroxisomal beta-oxidation of very-long-chain fatty acids", "Peroxisomal disorders can cause neurologic and hepatic disease, but the corneal rings and copper studies identify Wilson disease."),
      ],
      0,
      "Neuropsychiatric changes, liver injury, Kayser-Fleischer rings, low ceruloplasmin, and Coombs-negative hemolysis identify Wilson disease. ATP7B normally loads copper onto ceruloplasmin and excretes excess copper into bile.",
      "Use neurologic, hepatic, ocular, and hematologic clues to identify ATP7B dysfunction.",
      "Teenager + behavior/tremor + Kayser-Fleischer rings + low ceruloplasmin + hemolysis -> Wilson disease -> ATP7B copper transport defect."),

    q(7, ["Pharmacology", "Physiology", "Toxicology"], "Neuromuscular",
      "Organophosphate poisoning",
      "A 42-year-old farm worker is found confused beside an open container of insecticide. He is sweating and salivating profusely. Pulse is 48/min, pupils are pinpoint, lungs have diffuse wheezes, and fasciculations are present in both calves. He receives atropine and an additional medication before the enzyme-inhibitor complex ages.",
      "The second medication improves weakness by restoring which molecular function?",
      [
          ("Hydrolysis of acetylcholine in the synaptic cleft", "Correct. Pralidoxime reactivates phosphorylated acetylcholinesterase before aging, allowing acetylcholine breakdown at muscarinic and nicotinic synapses."),
          ("Competitive blockade of muscarinic acetylcholine receptors", "Atropine provides this effect and improves secretions and bronchospasm, but it does not reverse nicotinic weakness."),
          ("Inhibition of acetylcholine release from presynaptic terminals", "Botulinum toxin inhibits acetylcholine release; this would worsen weakness rather than treat organophosphate toxicity."),
          ("Increased metabolism of acetylcholine by plasma pseudocholinesterase", "Pseudocholinesterase metabolizes some ester drugs but is not the synaptic enzyme reactivated by pralidoxime."),
          ("Opening of postsynaptic chloride channels", "Opening chloride channels is the action of agents such as benzodiazepines or glycine, not treatment for cholinergic crisis."),
      ],
      0,
      "Miosis, bronchorrhea, bradycardia, diarrhea/sweating, and fasciculations after insecticide exposure indicate organophosphate poisoning. Atropine blocks muscarinic effects; pralidoxime reactivates acetylcholinesterase before irreversible aging and helps nicotinic weakness.",
      "Differentiate atropine's receptor blockade from pralidoxime's enzyme reactivation.",
      "Insecticide exposure + muscarinic signs + fasciculations -> organophosphate poisoning -> pralidoxime restores acetylcholinesterase activity."),

    q(8, ["Pharmacology", "Physiology", "Genetics"], "Musculoskeletal",
      "Malignant hyperthermia",
      "A healthy 19-year-old man undergoes emergency appendectomy. Shortly after induction with sevoflurane and succinylcholine, he develops generalized muscle rigidity, rapidly rising end-tidal CO2, hyperkalemia, and a temperature of 40.3 C. His father once had a severe fever during surgery.",
      "The drug used to treat this episode directly decreases which process?",
      [
          ("Calcium release from the sarcoplasmic reticulum", "Correct. Dantrolene inhibits ryanodine receptor-mediated calcium release from skeletal muscle sarcoplasmic reticulum."),
          ("Calcium entry through L-type channels in vascular smooth muscle", "Dihydropyridine calcium channel blockers act here, but malignant hyperthermia is due to skeletal muscle calcium release."),
          ("Acetylcholine binding at the neuromuscular junction", "Nondepolarizing neuromuscular blockers reduce nicotinic receptor activation but do not treat the intracellular calcium release crisis."),
          ("Myosin light-chain kinase activity", "This affects smooth muscle contraction and is not the mechanism of dantrolene in skeletal muscle."),
          ("Cyclooxygenase-mediated prostaglandin synthesis", "Antipyretics do not correct the hypermetabolic skeletal muscle process driving malignant hyperthermia."),
      ],
      0,
      "Volatile anesthetic plus succinylcholine exposure followed by rigidity, hypercapnia, hyperkalemia, fever, and family history identifies malignant hyperthermia, usually due to ryanodine receptor susceptibility. Dantrolene limits calcium release from skeletal muscle sarcoplasmic reticulum.",
      "Recognize malignant hyperthermia and connect dantrolene to skeletal muscle calcium handling.",
      "Anesthesia trigger + rigidity + rising CO2 + fever + hyperkalemia -> malignant hyperthermia -> dantrolene inhibits SR calcium release."),

    q(9, ["Microbiology", "Cell biology", "Pathology"], "Gastrointestinal",
      "Clostridioides difficile toxin",
      "A 71-year-old woman develops fever, crampy abdominal pain, and profuse watery diarrhea 6 days after receiving clindamycin for a dental infection. Colonoscopy shows yellow-white plaques over inflamed mucosa. A stool toxin assay is positive.",
      "The toxin causing this patient's disease most directly disrupts which host-cell process?",
      [
          ("Actin cytoskeleton regulation by Rho-family GTPases", "Correct. C difficile toxins A and B glucosylate Rho-family GTPases, disrupting actin organization, tight junctions, and epithelial integrity."),
          ("ADP-ribosylation of elongation factor 2", "Diphtheria toxin and Pseudomonas exotoxin A inhibit EF-2 and protein synthesis; they do not cause antibiotic-associated pseudomembranous colitis."),
          ("Cleavage of SNARE proteins in motor neurons", "Tetanus and botulinum toxins cleave SNARE proteins. The presentation here is colonic mucosal injury after antibiotics."),
          ("Ribosomal 28S rRNA depurination", "Shiga toxin inactivates the 60S ribosomal subunit and is associated with hemorrhagic colitis and hemolytic uremic syndrome."),
          ("Increased cyclic GMP secretion in small intestine", "Heat-stable enterotoxin of enterotoxigenic E coli increases cGMP and causes watery traveler's diarrhea without pseudomembranes."),
      ],
      0,
      "Antibiotic exposure followed by watery diarrhea, fever, abdominal pain, and pseudomembranes indicates C difficile colitis. Its toxins glucosylate Rho GTPases, causing actin disorganization and mucosal injury.",
      "Infer the toxin mechanism from antibiotic-associated pseudomembranous colitis.",
      "Clindamycin exposure + pseudomembranes + positive toxin -> C difficile -> Rho GTPase glucosylation disrupts actin."),

    q(10, ["Immunology", "Microbiology", "Pathology"], "Immune system",
      "Asplenia and encapsulated bacteria",
      "A 28-year-old man underwent splenectomy after a motor vehicle collision 2 years ago and did not complete recommended vaccinations. He now presents with fever, confusion, hypotension, and a petechial rash. Blood cultures grow lancet-shaped gram-positive diplococci.",
      "Loss of which splenic function most directly increased this patient's risk of overwhelming infection?",
      [
          ("Clearance of opsonized encapsulated organisms from the blood", "Correct. Splenic macrophages and marginal zone B cells help clear encapsulated bacteria such as Streptococcus pneumoniae from blood."),
          ("Negative selection of autoreactive T cells", "Central T-cell tolerance occurs in the thymus, not spleen; loss would cause autoimmunity rather than pneumococcal sepsis."),
          ("Class switching from IgM to IgE in mucosal lymphoid tissue", "IgE class switching is not the key defense against encapsulated bloodstream pathogens."),
          ("Generation of oxidative burst in neutrophils", "Neutrophil oxidative burst defects cause catalase-positive infections, not the specific risk after splenectomy."),
          ("Presentation of lipid antigens by cortical epithelial cells", "Cortical epithelial cells are thymic, and lipid antigen presentation is not the core defect in asplenic sepsis."),
      ],
      0,
      "Asplenia predisposes to severe infection with encapsulated organisms, especially S pneumoniae, H influenzae, and N meningitidis. The spleen filters blood and supports IgM-mediated opsonization and macrophage clearance of these organisms.",
      "Identify why splenectomy predisposes to rapidly progressive sepsis from encapsulated bacteria.",
      "Splenectomy + pneumococcal sepsis -> impaired splenic filtration/opsonized encapsulated organism clearance."),

    q(11, ["Immunology", "Hematology", "Pathology"], "Hematologic",
      "Acute hemolytic transfusion reaction",
      "A 64-year-old man undergoing surgery receives packed red blood cells. Within minutes, he develops fever, chills, hypotension, flank pain, and red-brown urine in the catheter bag. Oozing is noted from venipuncture sites.",
      "The antibody class most responsible for this reaction has which property?",
      [
          ("Efficient activation of the classical complement pathway as a pentamer", "Correct. ABO incompatibility is mediated mainly by preformed IgM, which forms pentamers and strongly activates complement, causing intravascular hemolysis."),
          ("Crossing the placenta as a monomer", "IgG crosses the placenta and mediates delayed hemolytic transfusion reactions and hemolytic disease of the newborn, not the classic immediate ABO reaction."),
          ("Binding mast cells through a high-affinity Fc receptor", "IgE binds mast cells and mediates immediate allergy and anaphylaxis, not intravascular hemolysis from ABO mismatch."),
          ("Dimeric secretion across mucosal surfaces", "IgA is important in mucosal immunity and is not the main antibody causing immediate complement-mediated transfusion hemolysis."),
          ("Antigen receptor expression on naive mature B cells only", "Naive B cells express IgM and IgD as surface receptors, but the damaging circulating antibody in ABO mismatch is secreted IgM with complement activity."),
      ],
      0,
      "Immediate fever, hypotension, flank pain, hemoglobinuria, and DIC during transfusion indicate acute hemolytic transfusion reaction from ABO mismatch. Preformed IgM antibodies activate complement and lyse transfused erythrocytes intravascularly.",
      "Recognize acute ABO transfusion reaction and connect it to IgM complement activation.",
      "Minutes after transfusion + hemoglobinuria + shock + DIC -> acute ABO reaction -> IgM pentamer activates classical complement."),

    q(12, ["Anatomy", "Neurology", "Physiology"], "Nervous system",
      "Medial pontine syndrome",
      "A 67-year-old man with long-standing hypertension suddenly develops double vision and left-sided weakness. The right eye cannot abduct when he looks to the right, but the left eye adducts normally when he looks left. Facial sensation is intact. Strength is 2/5 in the left arm and leg.",
      "Occlusion of which vessel most likely caused this patient's findings?",
      [
          ("Paramedian branches of the basilar artery", "Correct. Ipsilateral abducens palsy with contralateral corticospinal tract weakness localizes to the medial pons, supplied by paramedian basilar branches."),
          ("Posterior inferior cerebellar artery", "PICA lesions cause lateral medullary syndrome with dysphagia, hoarseness, vertigo, and crossed pain-temperature deficits, not abducens palsy with hemiparesis."),
          ("Anterior cerebral artery", "ACA stroke causes contralateral leg-predominant cortical deficits and behavioral changes, not an isolated pontine cranial nerve finding."),
          ("Superior cerebellar artery", "SCA infarcts cause ipsilateral limb ataxia and cerebellar signs, not corticospinal weakness with abducens palsy."),
          ("Middle cerebral artery superior division", "MCA superior division stroke can cause face/arm weakness and aphasia or neglect, but it does not produce an ipsilateral abducens nerve palsy."),
      ],
      0,
      "The combination of ipsilateral abducens nerve palsy and contralateral limb weakness localizes to the medial pons, where corticospinal fibers and abducens fascicles are near each other. The medial pons is supplied by paramedian branches of the basilar artery.",
      "Localize a brainstem stroke from crossed motor and cranial nerve findings.",
      "Right abduction failure + left hemiparesis + intact lateral medullary signs -> right medial pons -> paramedian basilar branches."),

    q(13, ["Physiology", "Biochemistry", "Endocrinology"], "Endocrine",
      "Catecholamine synthesis",
      "A 36-year-old woman has episodic headaches, sweating, palpitations, and severe hypertension. Plasma free metanephrines are elevated. CT shows a right adrenal medullary mass. Her mother had medullary thyroid carcinoma.",
      "High local concentrations of which hormone normally induce the enzyme that converts norepinephrine to epinephrine in this tissue?",
      [
          ("Cortisol", "Correct. Cortisol from the adrenal cortex reaches the medulla through the portal circulation and induces phenylethanolamine N-methyltransferase, which converts norepinephrine to epinephrine."),
          ("Aldosterone", "Aldosterone regulates sodium and potassium handling in the kidney and does not induce catecholamine methylation in the adrenal medulla."),
          ("Insulin", "Insulin affects glucose and lipid metabolism, not norepinephrine methylation in chromaffin cells."),
          ("Thyroid hormone", "Thyroid hormone increases beta-adrenergic responsiveness but does not induce PNMT in the adrenal medulla."),
          ("Parathyroid hormone", "PTH regulates calcium and phosphate homeostasis and is unrelated to adrenal catecholamine synthesis."),
      ],
      0,
      "Paroxysmal headache, sweating, palpitations, hypertension, elevated metanephrines, and an adrenal medullary mass indicate pheochromocytoma. In adrenal chromaffin cells, cortisol induces PNMT, enabling conversion of norepinephrine to epinephrine.",
      "Connect pheochromocytoma to adrenal medullary catecholamine synthesis.",
      "Paroxysmal sympathetic symptoms + high metanephrines + adrenal medullary mass -> pheochromocytoma -> cortisol induces PNMT."),

    q(14, ["Behavioral science", "Biostatistics", "Epidemiology"], "Biostatistics",
      "Positive predictive value",
      "A screening program is piloted for a treatable metabolic disorder in 10,000 asymptomatic newborns. The disorder is present in 100 newborns. The screening test is positive in 95 affected newborns and in 495 unaffected newborns.",
      "What is the probability that a newborn with a positive screening test truly has the disorder?",
      [
          ("16%", "Correct. Positive predictive value equals true positives divided by all positive tests: 95/(95+495) = 95/590 = 16%."),
          ("50%", "This would require true positives to equal false positives. Here, false positives are much more common because the disorder is uncommon."),
          ("84%", "This is close to the probability that a positive test is false, not true: 495/590 = 84%."),
          ("95%", "This is the sensitivity: true positives divided by all affected newborns, 95/100."),
          ("99%", "This approximates the proportion of the whole screened population without disease, not the probability of disease after a positive test."),
      ],
      0,
      "The stem provides actual counts, so no extra formula rearrangement is needed. Among positive tests, 95 are true positives and 495 are false positives. The positive predictive value is 95 divided by 590, which is about 16%.",
      "Calculate positive predictive value from a screening table embedded in a clinical scenario.",
      "Positive test group = true positives + false positives = 95 + 495; probability truly affected = 95/590 = 16%.",
      family="biostatistics"),

    q(15, ["Behavioral science", "Ethics", "Pediatrics"], "Behavioral science",
      "Shared decision-making",
      "A healthy term newborn is ready to receive intramuscular vitamin K. The parents say they read online that the injection contains harmful chemicals and ask the physician to skip it. The baby is feeding well and has no signs of bleeding. The hospital does not require a court order for refusal in this situation.",
      "Which response is most appropriate?",
      [
          ("Ask what concerns they have heard, acknowledge the worry, and explain the reason vitamin K is recommended", "Correct. The best initial response explores the parents' concerns respectfully, validates the emotion, and provides clear medical information to support shared decision-making."),
          ("Tell the parents that refusal proves they are not acting in the infant's best interest", "This is unnecessarily adversarial and may close communication before understanding their concern."),
          ("Administer vitamin K without telling the parents because the infant cannot consent", "A nonemergent preventive intervention generally requires parental permission; deception damages trust."),
          ("Discharge the infant immediately because the parents have refused standard care", "Ending care abruptly is inappropriate. The physician should counsel, document, and continue caring for the newborn."),
          ("Request a court order before discussing the issue further", "Court involvement is reserved for imminent serious harm or lifesaving treatment refusal. The prompt says this hospital does not require that step here."),
      ],
      0,
      "For vaccine or prophylaxis hesitancy, the first step is to explore the specific concern, show respect, and explain the medical rationale in plain language. This approach preserves trust and often resolves misinformation.",
      "Choose a patient-centered response to parental refusal of routine newborn prophylaxis.",
      "Nonemergent refusal + misinformation concern + healthy newborn -> explore concern, acknowledge, explain recommendation.",
      family="communication"),
]


def main():
    bank_path = ROOT / "data" / "usmle-module-bank.json"
    bank = json.loads(bank_path.read_text(encoding="utf-8"))
    for module in bank["modules"]:
        if module["id"] == MODULE_ID:
            module["questions"] = QUESTIONS
            break
    else:
        raise SystemExit(f"Missing module {MODULE_ID}")
    bank_path.write_text(json.dumps(bank, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(QUESTIONS)} questions to {MODULE_ID}")


if __name__ == "__main__":
    main()
