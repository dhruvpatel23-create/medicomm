"""Build USMLE Step 1 integrated practice items for Module 3.

These items use longer NBME-style clinical stems with purposeful history,
physical findings, and laboratory data. No textbook/PDF extraction is used.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_ID = "usmle-module-03"


def lab(test, value, reference):
    return {"test": test, "value": value, "reference": reference}


def q(number, disciplines, system, topic, prompt, lead_in, choices, answer_index,
      explanation, objective, reasoning, family="mechanism", labs=None):
    return {
        "id": f"{MODULE_ID}-q{number:03d}",
        "moduleId": MODULE_ID,
        "questionNumber": number,
        "subjectId": MODULE_ID,
        "subjectTitle": "Module 3",
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
        "tags": ["usmle-step-1", "integrated", "module-3", *[d.lower().replace(" ", "-") for d in disciplines]],
    }


QUESTIONS = [
    q(1, ["Pulmonary", "Physiology", "Pharmacology"], "Respiratory",
      "Reversible obstructive airway disease",
      "A 24-year-old woman comes to urgent care in late spring because of a 3-month history of intermittent cough, chest tightness, and shortness of breath. The symptoms are worse when she cleans houses and when she jogs outdoors. She has awakened twice this month because of coughing. She has no fever, weight loss, or sputum production. Temperature is 36.8 C, pulse is 96/min, respirations are 20/min, and oxygen saturation is 97% on room air. Expiration is prolonged, and scattered end-expiratory wheezes are heard bilaterally. Spirometry before and after an inhaled medication is shown below. Ten minutes after the medication, she says that breathing feels easier but notices a fine hand tremor.",
      "The medication responsible for the change in pulmonary function most directly increases which signaling pathway in airway smooth muscle?",
      [
          ("Gs protein -> adenylyl cyclase -> protein kinase A", "Correct. Rapid reversibility plus tremor indicates a short-acting beta2 agonist, which increases cAMP through Gs and relaxes airway smooth muscle."),
          ("Gq protein -> phospholipase C -> inositol trisphosphate", "Gq signaling raises intracellular calcium and promotes smooth muscle contraction; this would worsen bronchoconstriction."),
          ("Gi protein -> decreased adenylyl cyclase -> decreased cAMP", "Lower cAMP favors airway smooth muscle contraction rather than rapid bronchodilation."),
          ("Soluble guanylyl cyclase -> cyclic GMP -> protein kinase G", "Nitric oxide signaling through cGMP is important in vascular smooth muscle; it is not the main mechanism of rescue inhalers."),
          ("JAK2 -> STAT phosphorylation -> altered transcription", "JAK-STAT signaling is slower transcriptional signaling and does not explain bronchodilation within minutes."),
      ], 0,
      "The episodic symptoms, wheezing, obstructive spirometry, and bronchodilator response indicate asthma. Short-acting beta2 agonists cause rapid smooth-muscle relaxation by increasing cAMP and PKA activity. Tremor supports beta-adrenergic stimulation.",
      "Infer beta2-agonist signaling from reversible obstructive physiology and drug effect.",
      "Episodic wheeze + low FEV1/FVC + rapid FEV1 improvement + tremor -> beta2 agonist -> Gs/cAMP/PKA.",
      labs=[lab("FEV1 before bronchodilator", "2.0 L", "Predicted 3.1 L"), lab("FVC before bronchodilator", "3.6 L", "Predicted 3.8 L"), lab("FEV1 after bronchodilator", "2.5 L", "Increase >=12% supports reversibility")]),

    q(2, ["Neurology", "Immunology", "Physiology"], "Neuromuscular",
      "Fatigable weakness",
      "A 35-year-old woman comes to the office because of intermittent double vision and difficulty speaking clearly. She first noticed drooping of her eyelids while driving home from work 2 months ago. During dinner, chewing becomes difficult and her voice becomes nasal, but her strength is much better the next morning. She has no numbness, bowel symptoms, dry mouth, or recent gastrointestinal illness. Pupils are equal and reactive. Extraocular movements are full at the beginning of the examination, but sustained upward gaze produces bilateral ptosis. Repetitive arm abduction causes progressive weakness. Serum creatine kinase is normal.",
      "Which structural change is most likely present at the site responsible for this patient's symptoms?",
      [
          ("Flattening of postsynaptic folds with decreased nicotinic acetylcholine receptors", "Correct. Fluctuating ocular and bulbar weakness with normal pupils and normal CK indicates myasthenia gravis, a postsynaptic receptor disorder."),
          ("Loss of presynaptic P/Q-type calcium channel function", "This causes Lambert-Eaton syndrome, which often has autonomic symptoms and strength that improves with repeated effort."),
          ("Immune demyelination of peripheral motor nerves", "Peripheral demyelination causes slowed conduction, reflex loss, and sensory symptoms rather than isolated fatigable ocular-bulbar weakness."),
          ("Degeneration of anterior horn cells with grouped atrophy", "Anterior horn cell disease causes progressive weakness and denervation, not marked fluctuation over the day."),
          ("Absence of dystrophin from the sarcolemma", "Dystrophinopathy causes chronic proximal weakness with high CK rather than normal CK and fatigable ptosis."),
      ], 0,
      "This is myasthenia gravis. Autoantibodies reduce functional postsynaptic acetylcholine receptors and simplify junctional folds, producing fatigable weakness. Normal pupils help distinguish it from botulism, and normal CK argues against primary muscle injury.",
      "Use fluctuation, ocular-bulbar symptoms, and normal pupils to localize weakness to the postsynaptic neuromuscular junction.",
      "Evening ptosis/dysarthria + fatigability + normal pupils/CK -> myasthenia gravis -> decreased postsynaptic nicotinic receptors.",
      labs=[lab("Creatine kinase", "92 U/L", "40-150 U/L"), lab("TSH", "2.1 uU/mL", "0.4-4.0 uU/mL")]),

    q(3, ["Renal", "Physiology", "Biochemistry"], "Renal",
      "Generalized proximal tubular dysfunction",
      "A 7-year-old boy is brought to the clinic because of poor growth, frequent urination, and leg pain. He was adopted, and family history is unknown. His height and weight are below the 5th percentile. Blood pressure is 94/60 mm Hg. There is bowing of both legs and tenderness over the tibias. Urinalysis shows no blood and no protein, but glucose is present despite a normal fasting serum glucose concentration. The urine pH is 6.8 shortly after an intravenous bicarbonate load. Additional serum studies are shown below.",
      "Which additional urinary finding is most likely in this patient?",
      [
          ("Increased uric acid excretion", "Correct. Fanconi syndrome causes generalized proximal tubular wasting of bicarbonate, glucose, phosphate, amino acids, and uric acid."),
          ("Decreased urinary ammonium excretion despite systemic acidosis", "Distal renal tubular acidosis has impaired acid secretion and low ammonium generation, but it does not cause glycosuria and phosphaturia."),
          ("Isolated cystine crystals with otherwise normal solute handling", "Cystinuria causes selective cystine and dibasic amino acid transport defects, not broad proximal solute wasting."),
          ("Oval fat bodies from severe albuminuria", "Oval fat bodies indicate nephrotic syndrome due to glomerular protein leak; this urinalysis lacks proteinuria."),
          ("Low urinary calcium excretion despite hypercalcemia", "Familial hypocalciuric hypercalcemia involves calcium-sensing receptor physiology, not proximal tubular bicarbonate and phosphate wasting."),
      ], 0,
      "Growth failure, rickets, normoglycemic glycosuria, low phosphate, and proximal bicarbonate wasting indicate Fanconi syndrome. Because the proximal tubule reabsorbs many filtered solutes, generalized dysfunction also causes uricosuria and aminoaciduria.",
      "Recognize Fanconi syndrome from multiple proximal tubular transport failures.",
      "Poor growth + rickets + normal-glucose glycosuria + phosphate/bicarbonate wasting -> proximal tubule failure -> uricosuria.",
      labs=[lab("Serum glucose", "86 mg/dL", "70-100 mg/dL"), lab("Bicarbonate", "15 mEq/L", "22-28 mEq/L"), lab("Phosphate", "2.0 mg/dL", "3.0-4.5 mg/dL"), lab("Anion gap", "10 mEq/L", "8-12 mEq/L")]),

    q(4, ["Microbiology", "Pharmacology", "Genetics"], "Infectious disease",
      "Atypical pneumonia treatment failure",
      "A 19-year-old college student comes to student health because of 8 days of low-grade fever, malaise, sore throat, and a dry cough. Several students in his dormitory have similar symptoms. Temperature is 38.1 C, pulse is 92/min, respirations are 18/min, and oxygen saturation is 96% on room air. Chest examination shows scattered crackles. Chest x-ray shows patchy interstitial infiltrates that appear more extensive than the physical findings suggest. He is treated with azithromycin. Four days later, symptoms persist, and PCR testing identifies a wall-less organism. Sequencing of the organism shows methylation of a nucleotide in 23S rRNA.",
      "This genetic change most directly prevents the prescribed drug from binding to which target?",
      [
          ("50S ribosomal subunit near the peptide exit tunnel", "Correct. Macrolides bind 23S rRNA in the 50S subunit; methylation of this site causes resistance."),
          ("30S ribosomal subunit at the aminoacyl-tRNA acceptor site", "Tetracyclines act at this 30S site and may treat atypical pneumonia, but this explains doxycycline action rather than macrolide failure."),
          ("30S ribosomal subunit causing misreading of mRNA", "Aminoglycosides act here and are not used for this atypical pneumonia pattern."),
          ("DNA-dependent RNA polymerase beta subunit", "Rifamycins inhibit RNA polymerase; the resistance mechanism described involves rRNA methylation."),
          ("D-alanyl-D-alanine terminus of peptidoglycan precursors", "Vancomycin targets cell wall synthesis; the organism in the stem lacks a cell wall."),
      ], 0,
      "The prolonged dry cough, dormitory outbreak, interstitial infiltrates, and wall-less organism suggest Mycoplasma pneumoniae. Macrolides bind the 50S ribosomal subunit at 23S rRNA; methylation of the binding site reduces drug binding.",
      "Infer a macrolide resistance mechanism from atypical pneumonia plus rRNA methylation.",
      "Dormitory atypical pneumonia + wall-less organism + azithromycin failure + 23S rRNA methylation -> decreased macrolide binding to 50S.",
      labs=[lab("Leukocyte count", "8,900/mm3", "4,500-11,000/mm3"), lab("Cold agglutinin titer", "Positive", "Negative")]),

    q(5, ["Cardiology", "Pathology", "Pharmacology"], "Cardiovascular",
      "Acute coronary thrombosis",
      "A 59-year-old man is brought to the emergency department 45 minutes after the onset of crushing substernal chest pressure radiating to the left arm. He has type 2 diabetes mellitus and smokes one pack of cigarettes daily. Temperature is 37.0 C, pulse is 106/min, respirations are 22/min, and blood pressure is 154/92 mm Hg. ECG shows ST-segment elevations in leads II, III, and aVF. Emergent angiography shows an occlusive thrombus at the site of a disrupted lipid-rich plaque in the right coronary artery. He is given chewable aspirin while preparations for percutaneous coronary intervention are made.",
      "The immediate antithrombotic effect of this medication is best explained by decreased synthesis of which platelet product?",
      [
          ("Thromboxane A2", "Correct. Aspirin irreversibly inhibits platelet cyclooxygenase, decreasing thromboxane A2-mediated platelet activation and aggregation."),
          ("Adenosine diphosphate", "ADP receptor signaling is blocked by P2Y12 inhibitors such as clopidogrel; aspirin does not primarily reduce ADP production."),
          ("Prostacyclin", "Prostacyclin from endothelium inhibits platelet aggregation. Its reduction is not the desired antiplatelet effect."),
          ("Tissue factor", "Tissue factor initiates the extrinsic coagulation pathway after plaque rupture, but aspirin acts on platelet eicosanoid synthesis."),
          ("von Willebrand factor", "vWF mediates platelet adhesion to exposed subendothelium; aspirin does not directly block vWF production."),
      ], 0,
      "ST elevation in inferior leads with an occlusive thrombus after plaque rupture indicates acute myocardial infarction. Aspirin irreversibly inhibits platelet COX-1 and decreases thromboxane A2, reducing platelet aggregation.",
      "Connect plaque rupture therapy to platelet cyclooxygenase biology.",
      "Inferior STEMI + plaque rupture thrombus + aspirin -> irreversible platelet COX inhibition -> low thromboxane A2.",
      labs=[lab("Troponin I", "0.08 ng/mL", "<0.04 ng/mL early; rises over hours"), lab("Creatinine", "1.0 mg/dL", "0.6-1.2 mg/dL")]),

    q(6, ["Endocrinology", "Pathology", "Physiology"], "Endocrine",
      "PTH-mediated hypercalcemia",
      "A 53-year-old woman comes to the office because of 6 months of fatigue, constipation, and intermittent flank pain. She has passed two kidney stones during the past year and says she has been drinking more water because she is often thirsty. She does not take calcium, vitamin D, lithium, or thiazide diuretics. Her mother had osteoporosis. Blood pressure is 138/82 mm Hg. There is mild tenderness over the left costovertebral angle. Serum testing shows hypercalcemia with low phosphate. Parathyroid hormone concentration is elevated. A 24-hour urine collection shows increased calcium excretion.",
      "If this disease remains untreated, which skeletal finding is most likely to develop?",
      [
          ("Subperiosteal bone resorption along the radial aspects of phalanges", "Correct. Primary hyperparathyroidism increases osteoblast RANKL expression, indirectly increasing osteoclast activity and subperiosteal resorption."),
          ("Diffuse osteosclerosis due to failure of osteoclast acidification", "Osteopetrosis causes dense brittle bones from impaired resorption, the opposite of PTH-driven bone loss."),
          ("Poorly mineralized osteoid with low calcium and low phosphate", "Vitamin D deficiency osteomalacia usually has low or normal calcium, low phosphate, and secondary hyperparathyroidism, not high urine calcium from primary PTH excess."),
          ("Lytic punched-out lesions from monoclonal plasma cells", "Multiple myeloma can cause bone pain and hypercalcemia, but PTH would be suppressed rather than elevated."),
          ("Mosaic lamellar bone with elevated alkaline phosphatase and normal calcium", "Paget disease produces disorganized remodeling and usually normal serum calcium and phosphate."),
      ], 0,
      "High calcium, low phosphate, elevated PTH, kidney stones, and high urinary calcium identify primary hyperparathyroidism. PTH stimulates osteoblasts to express RANKL, which activates osteoclasts and causes subperiosteal bone resorption.",
      "Discriminate primary hyperparathyroidism from other hypercalcemic disorders using urine calcium and phosphate.",
      "Stones + high Ca/PTH + low phosphate + high urine Ca -> primary hyperparathyroidism -> RANKL-mediated subperiosteal resorption.",
      labs=[lab("Calcium", "11.8 mg/dL", "8.5-10.5 mg/dL"), lab("Phosphate", "2.1 mg/dL", "2.5-4.5 mg/dL"), lab("PTH", "132 pg/mL", "10-65 pg/mL"), lab("24-hour urine calcium", "380 mg/day", "100-300 mg/day")]),

    q(7, ["Microbiology", "Immunology", "Pathology"], "Renal",
      "Postinfectious glomerular injury",
      "A 9-year-old boy is brought to the clinic because of facial puffiness and dark urine for 2 days. Three weeks ago, he had a sore throat and fever that improved without medical care. He has no dysuria or flank pain. Temperature is 37.2 C, pulse is 88/min, respirations are 16/min, and blood pressure is 132/86 mm Hg. Examination shows periorbital edema. Urinalysis shows dysmorphic erythrocytes and red blood cell casts. Serum C3 is decreased, and antistreptolysin O titer is elevated.",
      "Which immune process best explains the renal findings?",
      [
          ("Deposition of circulating immune complexes with complement activation", "Correct. Poststreptococcal glomerulonephritis is a type III hypersensitivity reaction with immune complex deposition and low C3."),
          ("Linear IgG binding to the glomerular basement membrane", "Anti-GBM disease produces linear staining and may cause pulmonary hemorrhage; the delayed postpharyngitis timing and low C3 favor immune complexes."),
          ("Mesangial IgA deposition within days of mucosal infection", "IgA nephropathy often occurs during or immediately after an upper respiratory infection, not weeks later with low complement."),
          ("T-cell mediated granulomatous interstitial inflammation", "Interstitial nephritis typically causes pyuria, eosinophiluria, and drug exposure rather than nephritic casts after pharyngitis."),
          ("Direct bacterial invasion of glomerular capillaries", "The kidney injury is immune mediated; streptococci do not directly invade glomeruli in this disease."),
      ], 0,
      "Nephritic syndrome several weeks after pharyngitis with low C3 and elevated ASO titer is poststreptococcal glomerulonephritis. Immune complexes activate complement and inflame glomeruli.",
      "Use timing after infection, urine sediment, and complement level to identify type III glomerular injury.",
      "Pharyngitis weeks ago + edema/hypertension + RBC casts + low C3 + high ASO -> poststreptococcal GN -> immune complex deposition.",
      labs=[lab("Creatinine", "1.1 mg/dL", "0.5-1.0 mg/dL in children"), lab("C3", "Low", "Normal"), lab("ASO titer", "Elevated", "Negative/low")]),

    q(8, ["Biochemistry", "Nutrition", "Neurology"], "Nervous system",
      "Thiamine-dependent metabolism",
      "A 48-year-old man is brought to the emergency department by a neighbor because of confusion. He has had little food intake for several days and drinks a pint of liquor daily. Temperature is 36.7 C, pulse is 104/min, respirations are 18/min, and blood pressure is 112/68 mm Hg. He is disoriented to date and place. Horizontal nystagmus is present, and his gait is broad-based. Serum glucose is 58 mg/dL. Intravenous dextrose is ordered, but the physician gives a vitamin first.",
      "Deficiency of this vitamin would most directly decrease activity of which enzyme complex in vulnerable neurons?",
      [
          ("Alpha-ketoglutarate dehydrogenase", "Correct. Thiamine pyrophosphate is required by alpha-ketoglutarate dehydrogenase, pyruvate dehydrogenase, branched-chain alpha-ketoacid dehydrogenase, and transketolase."),
          ("Succinate dehydrogenase", "Succinate dehydrogenase uses FAD and functions as complex II; it is not thiamine dependent."),
          ("Isocitrate dehydrogenase", "Isocitrate dehydrogenase uses NAD+ or NADP+ and is not the classic thiamine-dependent step."),
          ("Glutamate dehydrogenase", "Glutamate dehydrogenase uses NAD+ or NADP+; it does not explain worsening Wernicke encephalopathy after glucose."),
          ("Malate dehydrogenase", "Malate dehydrogenase uses NAD+ and is not dependent on thiamine pyrophosphate."),
      ], 0,
      "Confusion, nystagmus, and ataxia in a malnourished patient with alcohol use disorder indicate Wernicke encephalopathy. Thiamine should be given before glucose because carbohydrate metabolism increases demand for thiamine-dependent enzymes.",
      "Connect Wernicke encephalopathy prevention to thiamine-dependent energy metabolism.",
      "Alcohol use + malnutrition + confusion/nystagmus/ataxia + dextrose planned -> thiamine first -> alpha-ketoglutarate dehydrogenase needs TPP.",
      labs=[lab("Serum glucose", "58 mg/dL", "70-100 mg/dL"), lab("AST", "88 U/L", "10-40 U/L"), lab("ALT", "42 U/L", "7-56 U/L"), lab("MCV", "104 fL", "80-100 fL")]),

    q(9, ["Pharmacology", "Renal", "Physiology"], "Renal/Cardiovascular",
      "Loop diuretic electrolyte pattern",
      "A 70-year-old man with ischemic cardiomyopathy is admitted because of worsening shortness of breath and orthopnea. He has been sleeping in a recliner for 3 nights and has gained 3 kg during the past week. He has bibasilar crackles, jugular venous distention, and 2+ pitting edema of both legs. Chest x-ray shows pulmonary edema. He receives an intravenous medication and produces 2.8 L of urine over the next 6 hours. The following morning, dyspnea is improved, but laboratory studies show metabolic alkalosis, hypokalemia, and increased urinary calcium excretion.",
      "The transporter inhibited by this medication normally performs which function?",
      [
          ("Reabsorption of sodium, potassium, and chloride in the thick ascending limb", "Correct. Loop diuretics inhibit NKCC2 in the thick ascending limb, causing brisk diuresis, hypokalemic metabolic alkalosis, and increased calcium excretion."),
          ("Reabsorption of sodium and chloride in the distal convoluted tubule", "Thiazides inhibit this transporter and decrease urinary calcium excretion."),
          ("Sodium entry through epithelial channels in principal cells", "ENaC inhibitors are potassium sparing and do not cause increased urinary calcium."),
          ("Bicarbonate reabsorption through carbonic anhydrase in the proximal tubule", "Carbonic anhydrase inhibitors cause metabolic acidosis from bicarbonaturia, not alkalosis."),
          ("Antagonism of aldosterone receptors in collecting duct cells", "Aldosterone antagonists are potassium sparing and have slower onset than the potent IV diuresis described."),
      ], 0,
      "Acute pulmonary edema treated with potent IV diuresis and followed by hypokalemic metabolic alkalosis plus calciuria indicates a loop diuretic. Loop diuretics inhibit the Na-K-2Cl cotransporter in the thick ascending limb.",
      "Use therapeutic context and electrolyte changes to identify the nephron transporter affected by a diuretic.",
      "Pulmonary edema + brisk IV diuresis + alkalosis/hypokalemia + high urine calcium -> loop diuretic -> NKCC2 blockade.",
      labs=[lab("Potassium", "3.0 mEq/L", "3.5-5.0 mEq/L"), lab("Bicarbonate", "33 mEq/L", "22-28 mEq/L"), lab("Urinary calcium", "Increased", "Variable by diuretic class")]),

    q(10, ["Pathology", "Genetics", "Gastrointestinal"], "Oncology",
      "Microsatellite instability",
      "A 39-year-old man undergoes colonoscopy because of 4 months of fatigue, intermittent right-sided abdominal discomfort, and a positive fecal occult blood test. He has not had changes in stool caliber. A friable mass is found in the ascending colon, and biopsy shows adenocarcinoma. His father died of colon cancer at age 44, and a paternal aunt had endometrial cancer at age 47. Colonoscopy shows two small adenomas but not hundreds of polyps. Tumor testing shows loss of MSH2 protein expression and numerous insertion-deletion mutations in short repetitive DNA sequences.",
      "The inherited defect in this family most directly impairs which cellular process?",
      [
          ("Repair of base-pair mismatches after DNA replication", "Correct. Lynch syndrome is due to mismatch repair defects, causing microsatellite instability and early colon/endometrial cancers without polyposis."),
          ("Excision of ultraviolet-induced pyrimidine dimers", "Nucleotide excision repair defects cause xeroderma pigmentosum with skin cancer susceptibility."),
          ("Homologous recombination repair of double-strand DNA breaks", "BRCA pathway defects increase breast, ovarian, prostate, and pancreatic cancer risk but do not produce microsatellite instability."),
          ("APC-mediated degradation of beta-catenin", "APC defects cause familial adenomatous polyposis with hundreds to thousands of adenomas."),
          ("Telomerase-independent alternative lengthening of telomeres", "Telomere maintenance contributes to cancer cell survival, but it is not the inherited defect shown by MSH2 loss and microsatellite instability."),
      ], 0,
      "Early right-sided colon cancer, endometrial cancer in relatives, few polyps, MSH2 loss, and microsatellite instability indicate Lynch syndrome. The underlying problem is impaired DNA mismatch repair.",
      "Use family history, polyp burden, and tumor testing to identify mismatch repair deficiency.",
      "Early colon/endometrial cancers + few polyps + MSH2 loss + microsatellite instability -> Lynch syndrome -> mismatch repair defect.",
      labs=[lab("Hemoglobin", "10.4 g/dL", "13.5-17.5 g/dL"), lab("MCV", "72 fL", "80-100 fL"), lab("Ferritin", "8 ng/mL", "20-250 ng/mL")]),

    q(11, ["Immunology", "Microbiology", "Pediatrics"], "Immune system",
      "Terminal complement deficiency",
      "A 16-year-old boy is hospitalized for fever, headache, photophobia, and confusion that began 1 day ago. Cerebrospinal fluid culture grows gram-negative diplococci. He had a similar episode at age 12 after returning from summer camp. He has normal growth, no chronic diarrhea, no history of severe viral or fungal infections, and normal wound healing after minor injuries. His parents are healthy. After recovery, immune testing is performed. Quantitative immunoglobulins and neutrophil oxidative burst are normal. C3 level is normal, but total hemolytic complement activity is undetectable.",
      "Which host defense function is most specifically impaired in this patient?",
      [
          ("Formation of membrane attack complexes on bacterial surfaces", "Correct. Recurrent Neisseria infections with absent CH50 and normal C3 indicate terminal complement deficiency, impairing C5b-9 MAC formation."),
          ("Opsonization of bacteria by C3b", "C3 deficiency would lower C3 and cause recurrent pyogenic infections and immune complex disease."),
          ("Oxidative killing of catalase-positive organisms", "Chronic granulomatous disease has abnormal oxidative burst testing and recurrent catalase-positive infections."),
          ("Class switching to secretory IgA at mucosal surfaces", "Selective IgA deficiency causes mucosal infections and possible transfusion reactions, not absent CH50 with recurrent meningococcal disease."),
          ("Cytotoxic killing of virus-infected cells by CD8+ lymphocytes", "T-cell cytotoxic defects cause viral and opportunistic infections; this patient's pattern is specific for Neisseria."),
      ], 0,
      "Recurrent meningococcal meningitis with absent CH50 and normal C3 points to terminal complement deficiency. C5 through C9 form the membrane attack complex, which is especially important against Neisseria.",
      "Infer terminal complement deficiency from infection pattern and complement testing.",
      "Recurrent meningococcal meningitis + normal immunoglobulins/oxidative burst + normal C3 + absent CH50 -> C5-C9 defect -> impaired MAC.",
      labs=[lab("C3", "Normal", "Normal"), lab("CH50", "Undetectable", "Detectable"), lab("Neutrophil oxidative burst", "Normal", "Normal")]),

    q(12, ["Reproductive", "Pharmacology", "Physiology"], "Reproductive",
      "Emergency contraception near ovulation",
      "A 22-year-old woman comes to clinic 18 hours after unprotected intercourse. Her menstrual periods occur every 28 days and last 5 days. Her last menstrual period began 12 days ago. She has no history of thromboembolism, liver disease, or migraine with aura. Temperature is 36.9 C, pulse is 78/min, and blood pressure is 112/68 mm Hg. Pelvic examination is normal. Urine pregnancy test is negative. She wants an oral medication and says she is not ready for a copper intrauterine device today.",
      "The most appropriate oral medication primarily prevents pregnancy by modulating which receptor?",
      [
          ("Progesterone receptor", "Correct. Ulipristal is a selective progesterone receptor modulator that delays ovulation and is effective close to the LH surge."),
          ("Estrogen receptor", "SERMs do not provide standard oral emergency contraception in this setting."),
          ("GnRH receptor", "GnRH analogs require more sustained effects on the hypothalamic-pituitary-gonadal axis and are not used for immediate oral emergency contraception."),
          ("Androgen receptor", "Androgen receptor antagonists are used for prostate cancer and some hyperandrogenic states, not emergency contraception."),
          ("Prostaglandin E1 receptor", "Misoprostol acts on prostaglandin receptors and is used in other reproductive contexts, not to delay ovulation before implantation."),
      ], 0,
      "At cycle day 12 in a regular 28-day cycle, ovulation is near. Ulipristal, a selective progesterone receptor modulator, is an effective oral emergency contraceptive close to ovulation because it delays follicular rupture.",
      "Choose an emergency contraceptive mechanism from timing in the menstrual cycle.",
      "Unprotected intercourse + cycle day 12 + wants oral option + pregnancy test negative -> ulipristal -> progesterone receptor modulation.",
      family="therapeutics",
      labs=[lab("Urine hCG", "Negative", "Negative"), lab("Last menstrual period", "12 days ago", "Cycle timing matters")]),

    q(13, ["Hematology", "Biochemistry", "Pathology"], "Hematologic",
      "Sickle hemoglobin polymerization",
      "A 25-year-old man comes to the emergency department because of severe pain in his lower back and both thighs. He returned yesterday from a hiking trip at high altitude. He has had similar episodes since childhood and was hospitalized twice for pneumonia. He is not taking any medications. Temperature is 37.8 C, pulse is 112/min, respirations are 22/min, and blood pressure is 128/76 mm Hg. Scleral icterus is present. The spleen is not palpable. Peripheral smear shows target cells, Howell-Jolly bodies, and crescent-shaped erythrocytes.",
      "Which change would most directly reduce the molecular event responsible for this patient's acute pain?",
      [
          ("Increased fetal hemoglobin concentration", "Correct. HbF interferes with HbS polymer formation and reduces vaso-occlusive crises."),
          ("Increased 2,3-bisphosphoglycerate concentration", "2,3-BPG stabilizes deoxygenated hemoglobin and would promote HbS polymerization."),
          ("Decreased arterial oxygen tension", "Hypoxemia favors deoxygenated HbS polymerization and triggered this crisis."),
          ("Increased erythrocyte dehydration", "Dehydration increases intracellular HbS concentration and worsens polymerization."),
          ("Decreased unconjugated bilirubin production", "Less hemolysis would lower bilirubin, but bilirubin itself is not the direct driver of HbS polymerization."),
      ], 0,
      "Vaso-occlusive pain after hypoxic stress, chronic hemolysis, autosplenectomy, Howell-Jolly bodies, and sickled cells indicate sickle cell disease. HbS polymerizes when deoxygenated; fetal hemoglobin decreases polymerization.",
      "Connect clinical triggers of sickle crisis to hemoglobin polymerization and HbF protection.",
      "High altitude + pain crisis + hemolysis + autosplenectomy/sickled cells -> deoxygenated HbS polymers -> HbF reduces polymerization.",
      labs=[lab("Hemoglobin", "8.9 g/dL", "13.5-17.5 g/dL"), lab("Reticulocytes", "9%", "0.5-2.5%"), lab("Indirect bilirubin", "3.4 mg/dL", "0.2-0.8 mg/dL"), lab("Oxygen saturation", "93% on room air", "95-100%")]),

    q(14, ["Gastrointestinal", "Pathology", "Physiology"], "Gastrointestinal",
      "Acid hypersecretion and diarrhea",
      "A 46-year-old man comes to the office because of 8 months of burning epigastric pain and watery diarrhea. The pain improves briefly after meals but returns despite daily proton pump inhibitor use. He has lost 4 kg during this period and says greasy foods worsen the diarrhea. He has no history of gastric surgery or inflammatory bowel disease. Upper endoscopy shows multiple ulcers, including one in the proximal jejunum. Fasting serum gastrin is markedly increased. Gastric aspirate has a pH of 1.1. Secretin infusion causes a further rise in serum gastrin.",
      "Which process most likely contributes to this patient's diarrhea?",
      [
          ("Inactivation of pancreatic lipase by excess gastric acid entering the small intestine", "Correct. Gastrinoma causes acid hypersecretion; acid inactivates pancreatic enzymes and damages mucosa, causing malabsorption and diarrhea."),
          ("Autoimmune destruction of gastric parietal cells with achlorhydria", "Autoimmune gastritis causes high gastrin with high gastric pH, not very acidic gastric fluid."),
          ("Failure of chloride-bicarbonate exchange in pancreatic ducts", "Cystic fibrosis can cause pancreatic insufficiency but does not cause refractory jejunal ulcers and a paradoxical secretin response."),
          ("Loss of lactase activity after viral gastroenteritis", "Lactase deficiency causes dairy-associated osmotic diarrhea, not acid hypersecretion with distal ulcers."),
          ("Bile acid malabsorption after terminal ileal disease", "Ileal disease causes bile acid diarrhea and B12 deficiency but does not explain high gastrin with low gastric pH."),
      ], 0,
      "Refractory ulcers distal to the duodenal bulb, high gastrin, low gastric pH, and increased gastrin after secretin indicate Zollinger-Ellison syndrome. Excess acid inactivates pancreatic enzymes and injures small intestinal mucosa, causing diarrhea.",
      "Distinguish gastrinoma from achlorhydria and connect acid excess to diarrhea.",
      "Refractory distal ulcers + high gastrin + low pH + secretin response -> gastrinoma -> acid-mediated pancreatic enzyme inactivation.",
      labs=[lab("Fasting gastrin", "1,240 pg/mL", "<100 pg/mL"), lab("Gastric pH", "1.1", "Acidic"), lab("Secretin stimulation", "Gastrin rises", "Normally decreases or little change")]),

    q(15, ["Behavioral science", "Biostatistics", "Ethics"], "Behavioral science",
      "Interim trial safety monitoring",
      "A multicenter randomized trial compares a new oral anticoagulant with standard prophylaxis after hip replacement. The protocol includes interim analyses by an independent data and safety monitoring board using prespecified stopping boundaries. After 40% of planned enrollment is complete, efficacy for prevention of venous thromboembolism is similar in both groups. However, the monitoring board finds a statistically significant increase in fatal intracranial hemorrhage in the new-drug group. Several enrolled participants have not yet completed follow-up, and investigators remain blinded to individual treatment assignments. The sponsor asks whether enrollment can continue until the planned sample size is reached.",
      "Which action is most appropriate?",
      [
          ("Stop or modify the trial according to the prespecified safety monitoring plan", "Correct. A clear excess of serious harm at interim analysis requires action under the DSMB plan to protect participants."),
          ("Continue enrollment until the original sample size is reached", "Continuing unchanged would expose participants to a treatment with an identified serious harm signal."),
          ("Unblind all participants and allow each to choose a treatment group", "Unblinding everyone is not the standard response and can compromise trial integrity without addressing the monitoring plan."),
          ("Exclude fatal hemorrhage from analysis because the efficacy endpoint is unchanged", "Removing serious adverse outcomes after seeing the data is unethical and invalid."),
          ("Publish only the efficacy finding and wait for final analysis to report harms", "Serious harms found during interim monitoring must guide trial conduct and be reported appropriately."),
      ], 0,
      "Clinical trials require ongoing safety monitoring. When interim analysis shows a statistically significant excess of fatal harm, investigators should stop or modify the trial according to the prespecified plan rather than continue enrollment unchanged.",
      "Apply research ethics to interim detection of serious treatment harm.",
      "Randomized trial + DSMB interim review + similar benefit but excess fatal harm -> stop/modify per safety plan.",
      family="ethics",
      labs=[lab("Planned enrollment completed", "40%", "Interim analysis"), lab("Efficacy outcome", "Similar between groups", "No clear benefit advantage"), lab("Fatal intracranial hemorrhage", "Increased in new-drug group", "Serious harm signal")]),
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
