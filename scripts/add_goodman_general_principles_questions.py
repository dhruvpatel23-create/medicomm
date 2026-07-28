import json
from collections import Counter
from pathlib import Path

DATA = Path('runtime-data/users.json')
CHAPTER = 'General Principles'
BASE = {'subjectId':'pharmacology','subjectTitle':'Pharmacology','chapterTitle':CHAPTER,'source':'ai','imageUrls':[]}

# The earlier bank asked bare definitions.  These clinical/research frames force the
# learner to interpret an observation before selecting the underlying principle.
FRAMES = {
    'drug-discovery': 'In an early drug-development meeting, investigators must decide how to interpret the following finding. ',
    'pharmacokinetics': 'After a dose change, serial plasma samples are reviewed for a patient receiving a drug with the stated property. ',
    'pharmacodynamics': 'In an isolated-tissue experiment, the response is compared before and after a second ligand is added. ',
    'transporters': 'A patient develops an unexpected interaction after starting a transporter inhibitor. ',
    'metabolism': 'A patient starts a second medicine and the concentration of a hepatically handled drug changes. ',
    'microbiome': 'Two patients receive the same oral regimen but have markedly different intestinal microbial exposure. ',
    'pharmacogenomics': 'Before prescribing, a clinician considers a patient\'s genetic result together with the intended drug. ',
    'drug-safety': 'A safety team reviews a suspected adverse event observed after a medicine reaches routine clinical use. ',
    'toxicology': 'In the emergency department, a patient is assessed after a suspected poisoning. ',
}

RATIONALes = {
    'drug-discovery': 'The finding is interpreted at the target/lead-development stage; the other choices describe a different pharmacologic role or a later, unrelated process.',
    'pharmacokinetics': 'This follows from the relationship between dose, concentration, distribution, clearance, and elimination; it is not determined simply by receptor action.',
    'pharmacodynamics': 'The response pattern identifies how the ligand changes agonist effect. Distinguish a shift in potency from a fall in maximal efficacy.',
    'transporters': 'Transporters can alter exposure by changing movement across gut, blood-tissue, hepatic, or renal barriers; the direction depends on whether uptake or efflux is affected.',
    'metabolism': 'Metabolic pathway changes alter parent-drug or metabolite exposure. The timing and direction depend on inhibition, induction, enzyme capacity, and whether the drug is a prodrug.',
    'microbiome': 'Gut organisms can activate, inactivate, deconjugate, or otherwise modify orally encountered drugs, producing clinically meaningful interpatient variation.',
    'pharmacogenomics': 'A genotype predicts a tendency, not a prescription in isolation: drug choice, dose, organ function, and interacting medicines still matter.',
    'drug-safety': 'Postmarketing evidence must be interpreted with the study design and alternative explanations in mind; a signal prompts evaluation rather than proving causality alone.',
    'toxicology': 'Poisoning management prioritizes physiology and the toxin\'s kinetic properties. A specific intervention is useful only when its mechanism fits the exposure.',
}

def clinical_prompt(slug, prompt):
    return FRAMES[slug] + prompt

# Each topic corresponds to one chapter in Goodman & Gilman's 14th edition, Section I.
T = [
('drug-discovery','Drug Discovery: From Medicinal Plants to Computer-Aided Drug Design',[
('A ligand that binds a receptor and produces the maximal system response is a:', 'Full agonist',['Competitive antagonist','Partial agonist','Inverse agonist']),
('The pharmacophore of a drug is best defined as its:', 'Essential three-dimensional features required for target recognition',['Entire chemical formulation','Route of administration','Elimination half-life']),
('High-throughput screening is primarily used to:', 'Identify active lead compounds from large libraries',['Establish phase IV safety','Determine renal clearance','Replace clinical trials']),
('A lead compound is optimized chiefly to improve:', 'Potency, selectivity, and drug-like properties',['Only tablet color','Only protein binding','Only placebo response']),
('Structure–activity relationship studies relate changes in:', 'Chemical structure to biological activity',['Dose interval to adherence','Age to placebo response','pH to tablet shape']),
('An allosteric modulator binds:', 'A site distinct from the endogenous ligand-binding site',['Only covalently to DNA','Only to plasma albumin','The active site of every enzyme']),
('Fragment-based drug discovery begins with:', 'Small low-affinity chemical fragments',['Large randomized clinical trials','Herbal extracts only','Postmarketing reports']),
('A major advantage of computer-aided docking is prediction of:', 'How a ligand may fit a target binding pocket',['A drug’s retail price','Patient adherence','Manufacturing sterility']),
('A prodrug is designed so that conversion in the body produces:', 'The active therapeutic moiety',['An inactive toxic metabolite only','A placebo response','An antibody against the drug']),
('Repurposing a drug means finding:', 'A new therapeutic use for an existing agent',['A new trade name only','A new route for insulin only','A new placebo control']),]),
('pharmacokinetics','Pharmacokinetics: Absorption, Distribution, Metabolism, and Elimination',[
('Bioavailability is the fraction of an administered dose that:', 'Reaches systemic circulation unchanged',['Binds plasma proteins','Enters the kidney','Produces toxicity']),
('For a drug given intravenously, bioavailability is generally:', '100%',['0%','Less than oral dosing by definition','Independent of dose delivered']),
('First-pass metabolism most directly reduces bioavailability after:', 'Oral administration',['Intravenous administration','Transdermal delivery','Inhalation of a gas']),
('Volume of distribution is calculated as:', 'Amount of drug in body divided by plasma concentration',['Dose divided by clearance','Clearance divided by half-life','Urinary concentration divided by dose']),
('A large apparent volume of distribution usually suggests:', 'Extensive distribution into tissues',['Confinement to plasma','Complete renal filtration','No protein binding']),
('At steady state during constant infusion, rate of infusion equals:', 'Rate of elimination',['Volume of distribution','Bioavailability','Protein binding']),
('For first-order elimination, a constant:', 'Fraction of drug is eliminated per unit time',['Amount is eliminated per unit time','Plasma concentration is maintained without dosing','Dose is absorbed each minute']),
('The loading dose is most dependent on:', 'Volume of distribution and target concentration',['Clearance alone','Half-life alone','Hepatic blood flow alone']),
('Maintenance dose rate is most dependent on:', 'Clearance and target concentration',['Volume of distribution alone','Drug color','Receptor density alone']),
('A drug with linear kinetics reaches near steady state after approximately:', 'Four to five half-lives',['One half-life','One distribution volume','Ten minutes for all drugs']),]),
('pharmacodynamics','Pharmacodynamics: Molecular Mechanisms of Drug Action',[
('Potency refers to the:', 'Concentration or dose needed for a specified effect',['Maximum effect attainable','Duration of action','Frequency of adverse effects']),
('Efficacy refers to the:', 'Maximum effect a drug can produce',['Dose needed for EC50','Extent of protein binding','Rate of renal elimination']),
('A partial agonist in the presence of a full agonist may behave as a:', 'Competitive antagonist',['Irreversible agonist','Chemical antagonist','Enzyme inducer']),
('A reversible competitive antagonist typically causes a:', 'Parallel rightward shift of the agonist dose-response curve',['Decrease in maximal efficacy','Leftward shift with higher efficacy','Nonparallel curve with no potency change']),
('A noncompetitive antagonist generally:', 'Reduces the maximal response to an agonist',['Raises maximal response','Has no effect at high agonist dose','Always increases potency']),
('The EC50 is the concentration producing:', '50% of maximal effect',['50% receptor occupancy in every system','50% toxicity','Complete receptor blockade']),
('Therapeutic index is commonly expressed as:', 'TD50 divided by ED50',['ED50 divided by TD50','Clearance divided by Vd','Ka divided by Ke']),
('Spare receptors are present when:', 'Maximal response occurs without occupancy of all receptors',['All receptors are irreversibly blocked','No agonist is bound','Affinity is zero']),
('Desensitization after persistent agonist exposure may result from:', 'Receptor phosphorylation and internalization',['Increased receptor synthesis only','Irreversible DNA binding','Reduced drug absorption']),
('An inverse agonist produces:', 'An effect opposite to constitutive receptor activity',['The same maximal effect as an agonist','No receptor binding','Only competitive inhibition of enzymes']),]),
('transporters','Membrane Transporters and Drug Response',[
('Passive diffusion across membranes is driven primarily by:', 'A concentration gradient',['ATP hydrolysis','Sodium-potassium ATPase only','Vesicular transport']),
('A weak acid is more lipid soluble in its:', 'Protonated, uncharged form',['Ionized anionic form','Protein-bound form','Conjugated form']),
('P-glycoprotein is best described as an:', 'ATP-dependent efflux transporter',['Plasma esterase','Ligand-gated ion channel','Phase II enzyme']),
('P-glycoprotein at the blood-brain barrier tends to:', 'Limit entry of its substrates into the brain',['Increase passive diffusion','Activate prodrugs','Increase glomerular filtration']),
('Organic anion transporters in the proximal tubule contribute to:', 'Active renal secretion of many drugs',['Passive pulmonary elimination','Platelet aggregation','Biliary synthesis']),
('SLC transporters generally mediate:', 'Facilitated or secondary active transport',['Only ATP-driven efflux','DNA transcription','Receptor internalization']),
('ABC transporters are characterized by use of:', 'ATP binding and hydrolysis',['Only sodium gradients','Only passive diffusion','G-protein signaling']),
('A transporter inhibitor can increase exposure to a substrate by:', 'Reducing its efflux or secretion',['Increasing its metabolism','Decreasing its absorption in every case','Blocking receptor binding']),
('Saturable carrier-mediated transport differs from diffusion because it:', 'Has a transport maximum',['Never shows competition','Does not require a gradient','Cannot be inhibited']),
('A clinically important transporter-mediated interaction may alter:', 'Absorption, distribution, or elimination',['Only tablet disintegration','Only receptor gene sequence','Only placebo effect']),]),
('metabolism','Drug Metabolism',[
('Phase I metabolism commonly includes:', 'Oxidation, reduction, or hydrolysis',['Glucuronidation only','Renal filtration only','Protein synthesis']),
('Phase II metabolism usually involves:', 'Conjugation with an endogenous substrate',['Only CYP-mediated oxidation','Only tubular secretion','Only receptor binding']),
('Cytochrome P450 enzymes are located mainly in the:', 'Smooth endoplasmic reticulum of hepatocytes',['Mitochondrial matrix only','Nuclear membrane only','Glomerular basement membrane']),
('Enzyme induction usually causes a substrate drug concentration to:', 'Decrease',['Increase immediately after one dose','Remain unchanged in all cases','Become independent of dose']),
('Enzyme inhibition usually causes a substrate drug concentration to:', 'Increase',['Decrease by increasing clearance','Become zero','Lose all protein binding']),
('A genetic CYP polymorphism may create a poor metabolizer with:', 'Reduced clearance of an active substrate',['Universal enzyme induction','Increased renal filtration only','No variability in response']),
('A reactive metabolite is clinically important because it may:', 'Cause tissue toxicity when detoxification is inadequate',['Always improve efficacy','Prevent all drug interactions','Eliminate first-pass metabolism']),
('Glutathione is important in detoxification because it:', 'Conjugates reactive electrophilic metabolites',['Induces CYP3A4','Blocks renal secretion','Activates receptors']),
('Enterohepatic recycling can prolong drug action when a drug is:', 'Excreted in bile and reabsorbed from intestine',['Filtered unchanged in glomerulus only','Given intravenously only','Irreversibly receptor-bound']),
('The first-pass effect reflects metabolism in the:', 'Gut wall and liver before systemic circulation',['Kidney after filtration','Lung after inhalation','Brain before receptor binding']),]),
('microbiome','The Gastrointestinal Microbiome and Drug Response',[
('The intestinal microbiome can alter drug response by:', 'Metabolizing drugs and modifying host enzymes',['Replacing hepatic blood flow','Eliminating all adverse effects','Preventing oral absorption of every drug']),
('Bacterial beta-glucuronidase can promote:', 'Deconjugation and intestinal reabsorption of drug metabolites',['Irreversible renal filtration','CYP gene deletion','Receptor downregulation']),
('Antibiotics may alter response to some drugs because they:', 'Change microbial metabolic capacity',['Always induce CYP enzymes','Always increase albumin','Prevent hepatic metabolism']),
('Microbial conversion of a prodrug may:', 'Generate its active metabolite',['Eliminate all parent drug absorption','Only reduce receptor affinity','Make IV administration impossible']),
('Interindividual microbiome variation can contribute to:', 'Variable efficacy and toxicity',['Identical pharmacokinetics in all patients','Fixed receptor number','Elimination of pharmacogenetics']),
('A drug–microbiome interaction can be bidirectional because drugs may:', 'Also change microbial composition or function',['Never affect microbes','Only bind human DNA','Only affect renal clearance']),
('Microbial metabolites may influence host drug metabolism by:', 'Modulating host enzymes and signaling pathways',['Directly changing tablet dose','Replacing glomerular filtration','Destroying all CYP proteins']),
('Loss of bacteria that inactivate a drug can lead to:', 'Higher active drug exposure',['Guaranteed treatment failure','No change in exposure','Zero oral bioavailability']),
('A useful strategy to study microbiome-related drug metabolism is:', 'Compare germ-free or antibiotic-treated models with controls',['Measure blood pressure only','Use placebo without sampling','Avoid metabolite measurement']),
('Microbiome-related variability is particularly relevant to oral drugs because of:', 'Direct contact with intestinal microbes',['Absence of hepatic metabolism','Lack of systemic circulation','Universal complete absorption']),]),
('pharmacogenomics','Pharmacogenetics and Pharmacogenomics',[
('Pharmacogenetics examines how inherited variation affects:', 'Response to individual drugs',['Only drug manufacturing','Only tablet dissolution','All infectious transmission']),
('Pharmacogenomics differs by considering:', 'Genome-wide influences on drug response',['Only one receptor in every patient','Only renal physiology','Only drug cost']),
('A poor metabolizer receiving a standard dose of an active drug is at risk of:', 'Excess drug exposure and toxicity',['Subtherapeutic exposure from rapid clearance','No effect on concentration','Universal enzyme induction']),
('A prodrug activated by a polymorphic enzyme may fail in a poor metabolizer because of:', 'Reduced formation of active metabolite',['Increased protein binding only','Enhanced renal secretion only','Excess receptor expression']),
('HLA variants are especially useful in predicting:', 'Immune-mediated severe adverse drug reactions',['Renal clearance','Tablet absorption','First-order kinetics']),
('Genotype-guided dosing is most valuable when a variant has a:', 'Large, actionable effect on efficacy or toxicity',['Trivial association only','No reproducibility','No clinical consequence']),
('Phenoconversion refers to change in apparent metabolic phenotype caused by:', 'Nongenetic factors such as inhibitors or disease',['Permanent DNA mutation after one dose','A placebo response only','Drug crystallization']),
('A pharmacogenetic test should not be interpreted without considering:', 'Clinical factors and concomitant medicines',['Only eye color','Only drug packaging','Only placebo response']),
('An ultrarapid metabolizer of an active drug may experience:', 'Reduced exposure and treatment failure',['Excess exposure from slow clearance','Guaranteed toxicity','No effect of dose']),
('The central clinical goal of pharmacogenomics is to:', 'Improve benefit while reducing preventable harm',['Replace all clinical judgment','Avoid therapeutic monitoring','Eliminate all adverse reactions']),]),
('drug-safety','Postmarketing Drug Safety',[
('Pharmacovigilance is the science of:', 'Detecting, assessing, understanding, and preventing adverse effects',['Discovering receptors only','Manufacturing generic drugs only','Measuring renal clearance only']),
('A limitation of premarketing trials is that they often cannot detect:', 'Rare adverse events',['Any intended pharmacologic effect','Drug absorption','Placebo responses']),
('A spontaneous adverse-event report is most useful for:', 'Generating a safety signal',['Proving causality by itself','Determining exact incidence','Replacing controlled studies']),
('An adverse drug reaction is more likely causal when it:', 'Recurs on rechallenge and follows a plausible time course',['Occurs before exposure','Has no biological plausibility','Persists unchanged after withdrawal']),
('A boxed warning is used to communicate:', 'A serious, potentially life-threatening risk',['A minor packaging issue','A generic substitution rule','A drug’s mechanism only']),
('Risk Evaluation and Mitigation Strategies are intended to:', 'Ensure benefits outweigh serious risks',['Guarantee zero adverse events','Replace labeling','Prohibit all monitoring']),
('Confounding by indication is a challenge because:', 'The illness prompting treatment may itself cause the outcome',['All observational data are randomized','Case reports estimate incidence precisely','Randomization increases bias']),
('Disproportionality analysis in safety databases looks for:', 'Reports occurring more often than expected for a drug-event pair',['Individual proof of causality','Exact patient adherence','Drug receptor occupancy']),
('A medication error differs from an adverse drug reaction because it:', 'Is a preventable failure in the medication-use process',['Is always immune mediated','Never causes harm','Requires a genetic variant']),
('Postmarketing surveillance is essential because real-world use includes:', 'Broader and more diverse patients than trials',['Only healthy volunteers','No concomitant medicines','No off-label use']),]),
('toxicology','Principles of Clinical Toxicology',[
('The initial priority in a severely poisoned patient is:', 'Airway, breathing, and circulation stabilization',['Immediate antidote before assessment','Routine gastric lavage','Waiting for toxicology confirmation']),
('The dose-response principle of toxicology means:', 'Toxicity generally depends on exposure magnitude',['All exposures are harmless','Only route matters','Time has no role']),
('Activated charcoal is most useful when given:', 'Early after ingestion of an adsorbable toxin',['For corrosive ingestion','For all alcohols equally','After bowel perforation']),
('Activated charcoal should generally be avoided with:', 'An unprotected airway or caustic ingestion',['Most alert patients after selected ingestions','Many organic compounds','Early adsorbable overdoses']),
('Enhanced elimination by urinary alkalinization is useful for:', 'Weak acids such as salicylate',['Weak bases such as amphetamine','Highly protein-bound drugs only','Inhaled anesthetics']),
('Hemodialysis is most effective for toxins with:', 'Low volume of distribution and low protein binding',['Very high tissue binding','Large volume of distribution only','Rapid hepatic activation only']),
('An antidote is most valuable when it:', 'Targets a specific toxic mechanism',['Replaces supportive care in every overdose','Has no adverse effects','Is given without diagnosis']),
('Toxidrome recognition is useful because it:', 'Links characteristic findings to likely toxin classes',['Proves exact dose ingested','Replaces glucose testing','Eliminates need for examination']),
('A high anion-gap metabolic acidosis in poisoning suggests:', 'Accumulation of unmeasured acids or toxic metabolites',['Isolated respiratory alkalosis','Normal acid-base status','Only hypoventilation']),
('Serial clinical assessment in poisoning is essential because:', 'Toxic effects may be delayed or evolve over time',['One normal examination excludes all toxicity','Drug levels always predict severity','All toxins act immediately']),]),
]

# Case-based replacements.  Each item asks the learner to infer a consequence,
# rather than recognise an isolated definition.
T = [
('drug-discovery','Drug Discovery: From Medicinal Plants to Computer-Aided Drug Design',[
('A candidate produces the same maximal response as the reference agonist but needs one tenth of its concentration. What is the best conclusion?', 'It is more potent but has equal efficacy',['It is more efficacious','It is a competitive antagonist','It must have a longer half-life']),
('A lead compound works in vitro but has poor oral exposure because it is rapidly converted to an inactive product. Which modification is most rational?', 'Design a prodrug that improves delivery before conversion to the active moiety',['Increase receptor density','Use a placebo run-in','Eliminate phase IV monitoring']),
('Two analogues bind the same target. Analogue B retains activity after a small structural change that abolishes A activity. This comparison is most useful for defining the:', 'Structure-activity relationship',['Therapeutic index','Renal clearance','Placebo effect']),
('A docking program predicts that a fragment occupies a previously unrecognized pocket away from the active site. Optimizing it could yield a:', 'Allosteric modulator',['Irreversible renal toxin','Phase II metabolite','Spontaneous safety report']),
('A drug approved for one disease is found to inhibit a pathway driving a rare cancer. Developing it for the cancer is:', 'Drug repurposing',['Lead optimization','High-throughput screening','A bioequivalence study'])]),
('pharmacokinetics','Pharmacokinetics: Absorption, Distribution, Metabolism, and Elimination',[
('An oral dose of 100 mg gives an AUC half that produced by 100 mg IV. Assuming linear kinetics, its bioavailability is:', '50%',['25%','100%','200%']),
('A 70-kg patient has 500 mg of drug in the body and a plasma concentration of 10 mg/L. The apparent volume of distribution is:', '50 L',['5 L','10 L','500 L']),
('A drug has Vd 40 L. To promptly achieve 5 mg/L, assuming complete bioavailability, the loading dose should be:', '200 mg',['8 mg','40 mg','800 mg']),
('During constant infusion, clearance suddenly falls by half while the infusion rate is unchanged. At the new steady state, concentration will be:', 'Approximately doubled',['Approximately halved','Unchanged','Zero']),
('A drug with first-order elimination has a half-life of 8 hours. Near steady state after a fixed regimen is expected in:', 'About 32-40 hours',['8 hours','16 hours','80 hours'])]),
('pharmacodynamics','Pharmacodynamics: Molecular Mechanisms of Drug Action',[
('Adding antagonist X shifts an agonist curve rightward in parallel without lowering Emax. X is most consistent with a:', 'Reversible competitive antagonist',['Noncompetitive antagonist','Partial agonist','Inverse agonist']),
('Antagonist Y lowers agonist Emax even when agonist concentration is greatly increased. Y is most consistent with a:', 'Noncompetitive antagonist',['Reversible competitive antagonist','Full agonist','Spare receptor']),
('Drug A reaches 100% response; drug B plateaus at 60% despite full receptor occupancy. B is a:', 'Partial agonist',['Full agonist','Neutral antagonist','Chemical antagonist']),
('A tissue produces maximal contraction when only 30% of receptors are occupied. The remaining receptors demonstrate:', 'Spare receptors',['Irreversible antagonism','Zero affinity','First-pass metabolism']),
('A receptor has constitutive signaling; a ligand reduces activity below its basal level. The ligand is an:', 'Inverse agonist',['Partial agonist','Neutral antagonist','Enzyme inducer'])]),
('transporters','Membrane Transporters and Drug Response',[
('A P-glycoprotein inhibitor is added to a P-glycoprotein substrate. Which change is most likely?', 'Increased substrate exposure due to reduced efflux',['Reduced absorption in every tissue','Increased CYP synthesis','Reduced receptor affinity']),
('A weak acid is trapped in alkaline urine after bicarbonate therapy. The immediate reason is that it becomes:', 'More ionized and less able to diffuse back across tubules',['More lipid soluble','More protein bound','A strong base']),
('Two medicines compete for the same proximal-tubule organic anion transporter. The substrate drug is most likely to show:', 'Reduced renal secretion and higher plasma concentration',['Faster glomerular filtration','Lower oral absorption','Greater receptor efficacy']),
('A transport process reaches a maximum rate and is inhibited by a structurally related drug. This process is:', 'Carrier-mediated transport',['Simple passive diffusion','Glomerular filtration','Osmosis']),
('A substrate has low CNS penetration despite high plasma concentration; blocking an ATP-dependent BBB efflux pump increases its brain level. The pump belongs to the:', 'ABC transporter family',['SLC family only','Cytochrome P450 family','G-protein family'])]),
('metabolism','Drug Metabolism',[
('A stable patient on warfarin begins a potent CYP inhibitor and later develops an elevated INR. The most likely explanation is:', 'Reduced warfarin metabolism causing higher exposure',['Increased renal filtration','Reduced receptor affinity','Faster enzyme induction']),
('A patient taking rifampicin has inadequate response to an active CYP substrate after two weeks. The likely mechanism is:', 'Enzyme induction increasing clearance',['Competitive receptor blockade','Reduced glomerular filtration','Immediate enzyme inhibition']),
('A prodrug requires CYP activation. In a genetic poor metabolizer, the expected result is:', 'Reduced active-metabolite formation and reduced benefit',['Higher active-metabolite formation','Universal toxicity','No effect on response']),
('After acetaminophen overdose, depletion of glutathione increases hepatic injury because glutathione normally:', 'Detoxifies the reactive electrophilic metabolite',['Induces CYP enzymes','Increases absorption','Blocks renal filtration']),
('A conjugated drug metabolite enters bile, is deconjugated in the intestine, and is reabsorbed. This process can:', 'Prolong drug exposure through enterohepatic recycling',['Eliminate first-pass metabolism','Make clearance zero','Prevent all interactions'])]),
('microbiome','The Gastrointestinal Microbiome and Drug Response',[
('An antibiotic removes bacteria that normally inactivate an orally administered drug. Without changing the dose, active drug exposure will most likely:', 'Increase',['Decrease to zero','Remain fixed in every patient','Become independent of absorption']),
('A glucuronidated metabolite is deconjugated by bacterial beta-glucuronidase and reabsorbed. This is most likely to:', 'Increase systemic drug exposure',['Prevent biliary excretion','Increase glomerular filtration','Block hepatic conjugation']),
('Two patients with the same genotype have different responses to an oral prodrug because one lacks organisms that form its active metabolite. The key source of variation is:', 'Microbial drug metabolism',['Receptor downregulation','IV bioavailability','Plasma albumin alone']),
('A new oral drug alters intestinal bacterial composition, which then changes the metabolism of a second drug. This illustrates that drug-microbiome interactions are:', 'Bidirectional',['Limited to hepatic CYP enzymes','Always beneficial','Independent of oral administration']),
('Why is microbiome-mediated variation generally more important for an oral medicine than an IV medicine?', 'The oral drug has direct contact with intestinal organisms',['IV drugs cannot be metabolized','Oral drugs bypass the liver','Only IV drugs enter plasma'])]),
('pharmacogenomics','Pharmacogenetics and Pharmacogenomics',[
('A patient with an HLA allele strongly associated with a severe immune drug reaction is being considered for that drug. The most appropriate use of the result is to:', 'Choose an alternative when an effective safer option exists',['Ignore it because genotype never matters','Double the dose','Assume renal failure']),
('A standard dose of an active drug causes repeated toxicity in a known poor metabolizer. The most likely pharmacokinetic change is:', 'Reduced clearance with higher exposure',['Faster clearance','Reduced absorption only','Higher receptor number']),
('An ultrarapid metabolizer receives a standard dose of an active drug and has no response. The most likely explanation is:', 'Increased metabolism causing low exposure',['Irreversible receptor blockade','Higher bioavailability','Reduced renal secretion']),
('A genotype predicts normal CYP function, but severe liver disease and a potent inhibitor are present. The observed phenotype may still be slow because of:', 'Phenoconversion',['Mendelian segregation','Placebo effect','Bioequivalence']),
('Which situation most strongly supports pre-treatment pharmacogenetic testing?', 'A validated variant has a large actionable effect on serious toxicity',['The variant has no clinical consequence','The drug has no exposure-response relation','The test result cannot alter management'])]),
('drug-safety','Postmarketing Drug Safety',[
('Five similar cases of a rare liver injury are reported soon after a new drug is marketed. The reports should initially be treated as:', 'A safety signal requiring further evaluation',['Proof of causality and incidence','A randomized trial','Evidence of no risk']),
('In an observational study, people receiving a drug have more thrombosis, but the drug was prescribed for a disease that itself causes thrombosis. This bias is:', 'Confounding by indication',['Lead-time bias','Recall bias only','Randomization']),
('A rash resolves after stopping a drug and recurs promptly on inadvertent rechallenge. This finding:', 'Strengthens evidence for causality',['Excludes causality','Proves exact incidence','Shows a medication error']),
('Why can a rare serious adverse effect be missed before approval?', 'Premarketing trials are often too small and selective to detect rare events',['Trials never record adverse events','Phase I includes all patients','Postmarketing data are randomized']),
('A nurse administers ten times the intended dose because of a decimal error. This is best classified as a:', 'Medication error',['Idiosyncratic adverse reaction','Pharmacogenetic result','Safety signal alone'])]),
('toxicology','Principles of Clinical Toxicology',[
('An obtunded patient arrives after an unknown ingestion with shallow breathing. The first priority is:', 'Airway, breathing, and circulation stabilization',['Immediate gastric lavage','Waiting for a drug level','Giving every antidote']),
('A toxin has low protein binding, a small volume of distribution, and causes severe persistent acidosis. The most useful enhanced-elimination method is likely:', 'Hemodialysis',['Forced diuresis alone','Increasing tissue binding','Observation only']),
('A conscious patient presents one hour after a large ingestion of an adsorbable drug and has a protected airway. The most appropriate decontamination option is:', 'Activated charcoal',['Charcoal after caustic ingestion','Routine induced emesis','No assessment']),
('In salicylate poisoning, bicarbonate increases renal elimination primarily by:', 'Ionizing the weak acid in urine and reducing reabsorption',['Making it more lipid soluble','Increasing protein binding','Blocking glomerular filtration']),
('A poisoned patient develops findings of miosis, bronchorrhea, bradycardia, and sweating. Recognizing this pattern is useful because it identifies a:', 'Cholinergic toxidrome',['Sympathomimetic toxidrome','Sedative withdrawal syndrome','Metabolic alkalosis'])]),
]

def main():
    qs=[]
    for ti,(slug,topic,items) in enumerate(T):
        if len(items)!=5: raise ValueError(topic)
        for i,(prompt,answer,wrong) in enumerate(items,1):
            opts=wrong[:]; pos=(ti+i-1)%4; opts.insert(pos,answer)
            qs.append({**BASE,'id':f'goodman-general-{slug}-{i}','topic':topic,'difficulty':('moderate' if i<=2 else 'high' if i<=4 else 'very high'),'prompt':prompt,'options':opts,'answerIndex':pos,'answer':answer,'explanation':f'{answer} is the best answer. {RATIONALes[slug]}'})
    d=json.loads(DATA.read_text(encoding='utf-8-sig')); old=d.get('questions',[])
    d['questions']=[x for x in old if not(str(x.get('id','')).startswith('goodman-general-') or (x.get('subjectId')=='pharmacology' and x.get('chapterTitle')==CHAPTER))]+qs
    ids=[x['id'] for x in d['questions']]
    if len(qs)!=45 or len(ids)!=len(set(ids)) or any(x['answer']!=x['options'][x['answerIndex']] for x in qs): raise ValueError('validation failed')
    DATA.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Added {len(qs)} Goodman & Gilman General Principles questions across {len(T)} topics.')
if __name__=='__main__': main()
