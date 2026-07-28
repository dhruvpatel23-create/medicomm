import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path("runtime-data/users.json")
CHAPTER = "Environmental and Nutritional Diseases"
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
    ("climate", "Climate Change and Environmental Disease Principles", [
        q("easy", "Climate change can increase infectious disease burden by altering:", "Vector distribution", ["MHC restriction", "Platelet adhesion", "Tumor grading"], "Temperature and rainfall changes alter mosquito and other vector habitats."),
        q("easy", "Heat waves most directly increase risk of:", "Heat-related illness and death", ["Scurvy", "Lead line", "Rickets"], "Extreme heat causes dehydration, heat exhaustion, and heat stroke."),
        q("easy", "Flooding increases risk of:", "Waterborne infections", ["Vitamin A toxicity only", "Familial obesity", "Carbon monoxide poisoning only"], "Floods disrupt clean water and sewage systems, promoting diarrheal disease."),
        q("moderate", "A major greenhouse gas released by burning fossil fuels is:", "Carbon dioxide", ["Radon", "Lead", "Benzene"], "CO2 traps heat and contributes to the greenhouse effect."),
        q("moderate", "Climate-related crop failure most directly contributes to:", "Malnutrition", ["Hypertension from sodium retention only", "Lead neuropathy", "Alcoholic hepatitis"], "Reduced agricultural productivity can cause food insecurity and malnutrition."),
        q("moderate", "Environmental disease burden is often greatest in poorer populations because of:", "Higher exposure and fewer protective resources", ["Complete absence of infections", "Universal vitamin excess", "No occupational risk"], "Vulnerability depends on exposure, infrastructure, nutrition, and access to care."),
        q("moderate", "Sea-level rise threatens health partly by:", "Displacing populations and contaminating water supplies", ["Increasing vitamin D synthesis", "Preventing vector breeding", "Reducing storms"], "Coastal flooding can force migration and compromise sanitation."),
        q("high", "After unusually heavy rains, a low-income region loses sewage treatment capacity and develops outbreaks of cholera and gastroenteritis. The same season brings expanded mosquito breeding and more dengue. Which climate-related mechanism best links these events?", "Extreme weather disrupting sanitation and expanding vector habitats", ["Inherited enzyme deficiency", "Direct ionizing radiation injury", "Cigarette carcinogen activation"], "Climate change can increase waterborne and vector-borne disease through floods, heat, and altered ecosystems."),
        q("high", "A tropical farming community experiences repeated crop failures after rising average temperatures and drought. Children present with wasting, infections, and micronutrient deficiencies. Which major health effect of climate change is most directly illustrated?", "Food insecurity leading to malnutrition", ["Carbon monoxide asphyxiation", "Acute ethanol intoxication", "Radon-induced lung cancer"], "Climate-driven agricultural disruption can produce protein-energy and micronutrient malnutrition."),
        q("high", "A coastal population is displaced by storm surge and rising sea level; crowding, poor sanitation, and loss of clean water follow. The immediate disease pattern includes diarrhea and respiratory infection rather than a single toxin exposure. What broad determinant is central?", "Environmental disaster compromising public health infrastructure", ["Leptin resistance", "Vitamin C hydroxylase activation", "Benzo[a]pyrene detoxification"], "Environmental disasters cause disease by disrupting shelter, water, sanitation, and access to care."),
    ]),
    ("xenobiotics", "Xenobiotic Metabolism and Toxic Injury", [
        q("easy", "A xenobiotic is:", "A foreign chemical substance in the body", ["A normal mitochondrial enzyme", "A vitamin receptor", "A lymphocyte clone"], "Xenobiotics include drugs, pollutants, and industrial chemicals."),
        q("easy", "The major phase I xenobiotic enzyme system is:", "Cytochrome P-450", ["Complement C3", "RAG recombinase", "Telomerase"], "CYP enzymes catalyze oxidation, reduction, and hydrolysis reactions."),
        q("easy", "Phase II metabolism generally makes compounds:", "More water soluble", ["More chromosomal", "Less excretable", "More antigenic only"], "Conjugation reactions increase excretion in urine or bile."),
        q("moderate", "Phase I reactions include:", "Oxidation, reduction, and hydrolysis", ["Glucuronidation only", "Antibody class switching", "Granuloma formation"], "Phase I modifies chemicals through oxidation/reduction/hydrolysis."),
        q("moderate", "Phase II reactions include:", "Glucuronidation, sulfation, methylation, and glutathione conjugation", ["Only DNA replication", "Only phagocytosis", "Only angiogenesis"], "Phase II conjugates metabolites to increase water solubility."),
        q("moderate", "Xenobiotic metabolism can increase toxicity when it:", "Generates reactive metabolites", ["Always detoxifies completely", "Prevents ROS formation", "Blocks DNA adducts"], "Some CYP products are electrophilic or free radical intermediates that injure cells."),
        q("moderate", "Genetic polymorphisms in CYP enzymes can alter:", "Drug toxicity and effectiveness", ["Karyotype number", "Amyloid birefringence", "MHC inheritance only"], "CYP variation changes metabolism rates and toxic metabolite production."),
        q("high", "A chemical is harmless until hepatic CYP enzymes convert it to a reactive intermediate that binds DNA and creates mutations. Phase II conjugation is overwhelmed, and long-term cancer risk rises. Which principle is illustrated?", "Metabolic activation of a xenobiotic", ["Direct vitamin deficiency", "Leptin resistance", "Mechanical trauma"], "Some xenobiotics become toxic only after phase I activation."),
        q("high", "A patient taking multiple drugs develops toxicity after a second medication induces CYP activity. The same dose now generates more reactive metabolite and oxidative stress. Which feature explains the altered response?", "Inducible and variable cytochrome P-450 metabolism", ["Fixed Mendelian penetrance", "Absence of phase I reactions", "Loss of all renal excretion"], "CYP activity varies with genetics and exposure to inducers or inhibitors."),
        q("high", "Carbon tetrachloride causes hepatic injury after conversion to a trichloromethyl free radical in the endoplasmic reticulum. Lipid peroxidation then damages membranes. Which cellular injury mechanism is central?", "Free radical generation during xenobiotic metabolism", ["IgE cross-linking", "Amyloid deposition", "Granulomatous inflammation"], "CYP-mediated metabolism can generate free radicals that injure membranes."),
    ]),
    ("air-co", "Air Pollution, Indoor Pollutants, and Carbon Monoxide", [
        q("easy", "Carbon monoxide is dangerous because it binds:", "Hemoglobin with high affinity", ["Vitamin D receptor", "LDL receptor", "Collagen"], "CO forms carboxyhemoglobin and impairs oxygen delivery."),
        q("easy", "Radon exposure increases risk of:", "Lung cancer", ["Scurvy", "Rickets", "Lead anemia"], "Radon is a radioactive gas linked to lung cancer."),
        q("easy", "Formaldehyde exposure can trigger:", "Airway irritation and asthma attacks", ["Hydatid cysts", "Night blindness", "Basophilic stippling"], "Formaldehyde irritates eyes, throat, and airways."),
        q("moderate", "Carbon monoxide poisoning often produces tissue injury by:", "Systemic hypoxia without cyanosis", ["Excess calcium absorption", "Immune complex deposition", "Osteoid overmineralization"], "CO reduces oxygen carrying capacity and shifts the dissociation curve."),
        q("moderate", "Indoor biomass smoke exposure is associated with:", "Respiratory infections and chronic lung disease", ["Only goiter", "Only beriberi", "Only mercury tremor"], "Smoke particulates and irritants injure airways and predispose to infection."),
        q("moderate", "Bioaerosols in indoor environments may cause:", "Allergic rhinitis and asthma", ["Lead line", "Alcoholic cirrhosis", "Obesity"], "Dust mites, molds, and pet dander can provoke allergic disease."),
        q("moderate", "Particulate air pollution contributes to disease by:", "Inducing pulmonary and systemic inflammation", ["Increasing collagen hydroxylation", "Preventing atherosclerosis", "Curing asthma"], "Fine particles reach airways and can trigger inflammation and cardiopulmonary disease."),
        q("high", "A family using a faulty heater is found confused and somnolent, but their skin is not cyanotic. Pulse oximetry is misleadingly normal, while carboxyhemoglobin is high. Which environmental toxin explains the presentation?", "Carbon monoxide", ["Radon", "Formaldehyde", "Ozone"], "CO is colorless, odorless, and causes hypoxic injury by binding hemoglobin."),
        q("high", "A nonsmoker living in a poorly ventilated basement has chronic low-level exposure to a radioactive gas from soil uranium decay. The agent is the second leading cause of lung cancer overall and particularly important in nonsmokers. Which pollutant is it?", "Radon", ["Carbon monoxide", "Mercury vapor", "Benzene"], "Radon is an indoor radioactive gas and lung carcinogen."),
        q("high", "A poorly ventilated home uses wood and dung for cooking. Children develop recurrent respiratory symptoms and infections, while adults have chronic bronchitic complaints. Which exposure best accounts for this pattern?", "Indoor biomass smoke and particulates", ["Excess vitamin A", "Dietary nitrosamines only", "Lead-contaminated paint chips only"], "Indoor combustion of organic material produces irritants and particulates."),
    ]),
    ("metals", "Heavy Metal Toxicity", [
        q("easy", "Lead poisoning classically causes:", "Microcytic anemia with basophilic stippling", ["Macrocytosis with hypersegmented neutrophils", "Nephrotic syndrome only", "Hypercalcemia"], "Lead interferes with heme synthesis and causes basophilic stippling."),
        q("easy", "Children with lead poisoning are especially prone to:", "Encephalopathy and cognitive defects", ["Peripheral wrist drop only", "Hydatid disease", "Scurvy"], "Developing brains are highly vulnerable to lead."),
        q("easy", "Mercury toxicity primarily injures:", "Central nervous system and kidney", ["Only skin collagen", "Only adipose tissue", "Only thyroid follicles"], "Mercury binds sulfhydryl groups and damages CNS and kidney."),
        q("moderate", "Lead inhibits heme synthesis by affecting:", "Ferrochelatase and ALA dehydratase", ["Telomerase and RB", "Lactase and sucrase", "Lipase and amylase"], "Lead blocks enzymes in heme synthesis."),
        q("moderate", "A classic adult neurologic manifestation of lead poisoning is:", "Peripheral motor neuropathy with wrist drop", ["Cerebellar tonsillar herniation", "Optic glioma", "Myasthenic crisis"], "Adults often develop demyelinating peripheral neuropathy."),
        q("moderate", "Methylmercury exposure is most commonly from:", "Contaminated fish", ["Old paint chips", "Radon gas", "Excess vitamin C"], "Methylmercury bioaccumulates in aquatic food chains."),
        q("moderate", "Chronic arsenic exposure is linked to:", "Skin lesions and cancers", ["Basophilic stippling only", "Wrist drop only", "Rickets only"], "Arsenic causes skin changes, neuropathy, and cancers."),
        q("high", "A toddler in an old house eats paint flakes and develops abdominal pain, irritability, developmental regression, microcytic anemia, and basophilic stippling. Wrist radiographs show dense metaphyseal lines. Which toxin is responsible?", "Lead", ["Mercury", "Cadmium", "Arsenic"], "Lead exposure from old paint causes anemia, neurotoxicity, abdominal pain, and dense epiphyseal deposits."),
        q("high", "A pregnant patient eats contaminated fish with high methylmercury. The fetus later shows severe neurologic impairment with cerebral palsy, deafness, and blindness. Which disease pattern does Robbins associate with this exposure?", "Minamata disease", ["Keshan disease", "Beriberi", "Pellagra"], "Fetal mercury exposure can cause Minamata disease with severe CNS injury."),
        q("high", "A worker chronically exposed to arsenic develops hyperpigmentation, hyperkeratosis, peripheral neuropathy, and later skin and lung cancers. The toxin also interferes with mitochondrial oxidative phosphorylation. Which exposure best fits?", "Arsenic", ["Lead", "Carbon monoxide", "Fluoride"], "Arsenic causes skin changes, neuropathy, mitochondrial toxicity, and cancer risk."),
    ]),
    ("occupation-tobacco", "Occupational Exposures and Tobacco", [
        q("easy", "Asbestos exposure is strongly associated with:", "Mesothelioma", ["Rickets", "Kwashiorkor", "Beriberi"], "Asbestos causes pulmonary fibrosis, lung carcinoma, and mesothelioma."),
        q("easy", "Benzene exposure increases risk of:", "Leukemia", ["Osteomalacia", "Night blindness", "Scurvy"], "Benzene metabolites injure marrow and increase leukemia risk."),
        q("easy", "Nicotine is important in smoking because it is:", "Addictive", ["A vitamin", "A heavy metal", "A fungal toxin"], "Nicotine stimulates nicotinic acetylcholine receptors and reinforces dependence."),
        q("moderate", "Smoking promotes emphysema partly by:", "Recruiting leukocytes and increasing elastase-mediated lung injury", ["Increasing collagen hydroxylation", "Blocking all ROS", "Increasing surfactant only"], "Smoke induces inflammation and protease-antiprotease imbalance."),
        q("moderate", "Tobacco carcinogens include:", "Polycyclic hydrocarbons and nitrosamines", ["Leptin and ghrelin", "Calcium and phosphate", "Vitamin C and E"], "These compounds form DNA adducts after metabolic activation."),
        q("moderate", "Smoking and asbestos together increase lung cancer risk because:", "Their carcinogenic effects are synergistic", ["Asbestos prevents smoke inhalation", "Nicotine chelates asbestos", "Both cause only benign tumors"], "Smoking greatly magnifies asbestos-related lung cancer risk."),
        q("moderate", "Occupational organic solvents can cause acute high-dose:", "CNS depression", ["Rickets", "Night blindness", "Goiter only"], "Solvents such as chloroform and carbon tetrachloride can depress CNS and injure liver/kidney."),
        q("high", "A shipyard worker with decades of asbestos exposure develops progressive dyspnea, pleural plaques, and later malignant pleural mesothelioma. He also smokes heavily, increasing lung carcinoma risk. Which occupational agent is central?", "Asbestos", ["Benzene", "Mercury", "Formaldehyde"], "Asbestos causes plaques, asbestosis, lung carcinoma, and mesothelioma."),
        q("high", "A smoker’s lung cancer genome contains thousands of mutations with signatures typical of tobacco carcinogens. CYP metabolism generated electrophilic intermediates that formed DNA adducts repaired by error-prone pathways. Which exposure is most responsible?", "Cigarette smoke polycyclic hydrocarbons and nitrosamines", ["Excess dietary fiber", "Vitamin D deficiency", "Leptin resistance"], "Tobacco carcinogens produce DNA adducts and characteristic mutational signatures."),
        q("high", "A rubber industry worker chronically exposed to benzene develops marrow failure and later acute myeloid leukemia. The chemical is metabolized by hepatic CYP2E1 into toxic intermediates affecting progenitor cells. Which toxin is implicated?", "Benzene", ["Radon", "Carbon monoxide", "Cadmium in rice"], "Benzene exposure is a classic occupational risk for leukemia."),
    ]),
    ("alcohol-drugs", "Alcohol, Therapeutic Drugs, and Drugs of Abuse", [
        q("easy", "Most ethanol is metabolized in the:", "Liver", ["Skin", "Bone", "Thyroid"], "The liver metabolizes ethanol through alcohol dehydrogenase, MEOS, and catalase pathways."),
        q("easy", "Ethanol is first converted mainly to:", "Acetaldehyde", ["Acetone", "Lactate", "Urea"], "Alcohol dehydrogenase converts ethanol to acetaldehyde."),
        q("easy", "Acetaminophen overdose causes severe injury mainly to:", "Liver", ["Bone", "Lens", "Cartilage"], "Toxic NAPQI metabolite causes hepatic necrosis when glutathione is depleted."),
        q("moderate", "Chronic alcohol use induces:", "CYP2E1", ["RAG1", "LDLR", "AIRE"], "MEOS/CYP2E1 induction increases ethanol metabolism and drug toxicity risks."),
        q("moderate", "Alcoholic liver disease progresses through:", "Fatty liver, hepatitis, and cirrhosis", ["Rickets, scurvy, beriberi", "Metaplasia, dysplasia, carcinoma in situ", "Edema, thrombosis, infarction"], "Alcohol causes steatosis, steatohepatitis, fibrosis, and cirrhosis."),
        q("moderate", "Methanol poisoning can cause blindness because it is metabolized to:", "Formic acid", ["Acetaldehyde", "Benzo[a]pyrene", "Leptin"], "Formic acid causes retinal and optic nerve toxicity."),
        q("moderate", "Cocaine can cause sudden death by:", "Arrhythmia or myocardial ischemia", ["Vitamin C deficiency", "Lead line formation", "Night blindness"], "Cocaine increases catecholamines, vasoconstriction, and arrhythmias."),
        q("high", "A chronic drinker takes therapeutic acetaminophen doses and develops severe hepatic necrosis. Alcohol has induced CYP2E1 and depleted glutathione, increasing formation and reducing detoxification of NAPQI. Which interaction explains the injury?", "Enhanced toxic metabolite formation with impaired detoxification", ["IgE-mediated drug allergy", "Lead inhibition of ferrochelatase", "Leptin receptor mutation"], "CYP induction and low GSH increase acetaminophen hepatotoxicity."),
        q("high", "A patient drinks windshield washer fluid and later develops metabolic acidosis with visual disturbances. Toxicity results after alcohol dehydrogenase converts the parent alcohol to formic acid. Which substance was ingested?", "Methanol", ["Ethanol", "Isopropanol", "Ethylene glycol"], "Methanol metabolism causes formic acid accumulation and ocular toxicity."),
        q("high", "A long-term heavy drinker develops macrovesicular steatosis, Mallory-Denk bodies, neutrophilic hepatitis, pericellular fibrosis, and eventually portal hypertension. Which disease sequence best describes this injury?", "Alcoholic fatty liver progressing to alcoholic hepatitis and cirrhosis", ["Kwashiorkor progressing to marasmus", "Rickets progressing to osteomalacia", "Lead poisoning progressing to Minamata disease"], "Alcoholic liver disease evolves from steatosis to hepatitis and cirrhosis."),
    ]),
    ("pem", "Protein-Energy Malnutrition and Eating Disorders", [
        q("easy", "Marasmus is primarily due to deficiency of:", "Calories and protein", ["Vitamin C only", "Iodine only", "Iron only"], "Marasmus is overall calorie deprivation with wasting."),
        q("easy", "Kwashiorkor is primarily associated with:", "Protein deficiency with edema", ["Excess vitamin D", "Lead poisoning", "High BMI"], "Kwashiorkor features hypoalbuminemia and edema."),
        q("easy", "Anorexia nervosa is characterized by:", "Self-induced starvation and distorted body image", ["High leptin sensitivity only", "Lead ingestion", "Mercury accumulation"], "Anorexia involves psychiatric restriction of intake and severe undernutrition."),
        q("moderate", "Edema in kwashiorkor is mainly due to:", "Hypoalbuminemia", ["Carbon monoxide", "Hypervitaminosis A", "Mercury"], "Low plasma oncotic pressure from protein deficiency causes edema."),
        q("moderate", "Marasmus typically shows:", "Severe muscle wasting without prominent edema", ["Moon face and fatty liver only", "Basophilic stippling", "Radiodense epiphyses"], "Marasmus is cachectic wasting with relative preservation of serum protein until late."),
        q("moderate", "Fatty liver in kwashiorkor is caused partly by:", "Reduced apoprotein synthesis", ["Excess LDL receptor activity", "High vitamin C intake", "Carbon monoxide hypoxia"], "Protein deficiency impairs lipoprotein export from liver."),
        q("moderate", "Bulimia nervosa commonly causes:", "Dental enamel erosion and electrolyte abnormalities", ["Cerebral malaria", "Mesothelioma", "Hydatid cyst"], "Vomiting exposes teeth to acid and can cause hypokalemic alkalosis."),
        q("high", "A severely malnourished child has marked wasting, loss of subcutaneous fat, growth retardation, and no significant edema. Serum albumin is relatively preserved compared with a child who has flaky paint dermatosis and fatty liver. Which condition is present?", "Marasmus", ["Kwashiorkor", "Scurvy", "Pellagra"], "Marasmus is total calorie deprivation with severe wasting but less edema than kwashiorkor."),
        q("high", "A child weaned onto a carbohydrate-rich but protein-poor diet develops edema, distended abdomen, flaky skin lesions, hair color changes, and fatty liver. The edema reflects low plasma oncotic pressure. Which diagnosis fits?", "Kwashiorkor", ["Marasmus", "Beriberi", "Rickets"], "Kwashiorkor is protein malnutrition with hypoalbuminemia, edema, dermatosis, and fatty liver."),
        q("high", "A young woman with binge eating and self-induced vomiting develops parotid enlargement, enamel erosion, hypokalemic metabolic alkalosis, and normal-to-low body weight. Which nutritional/behavioral disorder best explains these findings?", "Bulimia nervosa", ["Anorexia nervosa restrictive type", "Kwashiorkor", "Marasmus"], "Bulimia involves binge-purge behavior with characteristic dental and electrolyte effects."),
    ]),
    ("vitamins", "Vitamin Deficiencies and Toxicities", [
        q("easy", "Vitamin A deficiency causes:", "Night blindness", ["Beriberi", "Scurvy", "Pellagra"], "Vitamin A is required for vision and epithelial maintenance."),
        q("easy", "Vitamin D deficiency in children causes:", "Rickets", ["Scurvy", "Pellagra", "Wernicke encephalopathy"], "Defective mineralization of growing bone causes rickets."),
        q("easy", "Vitamin C deficiency causes:", "Scurvy", ["Osteopetrosis", "Minamata disease", "Lead colic"], "Vitamin C deficiency impairs collagen hydroxylation."),
        q("moderate", "Thiamine deficiency causes:", "Beriberi and Wernicke-Korsakoff syndrome", ["Night blindness", "Rickets", "Kwashiorkor"], "Vitamin B1 deficiency injures heart and nervous system."),
        q("moderate", "Niacin deficiency causes:", "Dermatitis, diarrhea, and dementia", ["Bleeding gums only", "Tetany only", "Wrist drop"], "Pellagra is the three Ds, and may progress to death."),
        q("moderate", "Vitamin K deficiency causes:", "Bleeding due to impaired gamma-carboxylation", ["Night blindness", "Rickets", "Goiter"], "Vitamin K is needed for factors II, VII, IX, and X."),
        q("moderate", "Vitamin A toxicity may cause:", "Liver injury and increased intracranial pressure", ["Hypochromic anemia", "Pellagra", "Kwashiorkor"], "Hypervitaminosis A can be hepatotoxic and teratogenic."),
        q("high", "A child with limited sunlight exposure develops bowed legs and widened growth plates. Serum calcium is maintained by elevated PTH, but phosphate remains low, impairing mineralization of osteoid and epiphyseal cartilage. Which deficiency is responsible?", "Vitamin D deficiency", ["Vitamin C deficiency", "Vitamin A excess", "Niacin deficiency"], "Vitamin D deficiency causes rickets through defective mineralization."),
        q("high", "A sailor on a long voyage develops swollen bleeding gums, perifollicular hemorrhages, poor wound healing, and fragile blood vessels. The molecular defect is impaired hydroxylation of proline and lysine in procollagen. Which vitamin is deficient?", "Vitamin C", ["Vitamin D", "Vitamin B12", "Vitamin A"], "Scurvy reflects defective collagen synthesis from vitamin C deficiency."),
        q("high", "A malnourished alcoholic develops confusion, ataxia, and ophthalmoplegia, then memory loss and confabulation. The disorder reflects impaired carbohydrate metabolism in vulnerable brain regions. Which vitamin deficiency is most likely?", "Thiamine deficiency", ["Vitamin K deficiency", "Vitamin E deficiency", "Riboflavin deficiency"], "Wernicke-Korsakoff syndrome is due to thiamine deficiency."),
    ]),
    ("obesity", "Obesity, Leptin, and Metabolic Syndrome", [
        q("easy", "Obesity is defined in adults by BMI greater than:", "30 kg/m²", ["18.5 kg/m²", "20 kg/m²", "25 kg/m²"], "BMI over 30 kg/m² is classified as obesity."),
        q("easy", "Central obesity carries high risk because fat accumulates in:", "Visceral abdominal depots", ["Only scalp", "Only bone marrow", "Only fingernails"], "Visceral adiposity is metabolically harmful."),
        q("easy", "Leptin is produced mainly by:", "Adipocytes", ["Osteoblasts", "Neurons only", "Platelets"], "Adipose tissue secretes leptin in proportion to fat stores."),
        q("moderate", "Leptin normally acts to:", "Reduce appetite and increase energy expenditure", ["Increase appetite only", "Cause lead anemia", "Block insulin secretion completely"], "Leptin signals adequate fat stores to hypothalamic pathways."),
        q("moderate", "Common obesity often shows:", "Leptin resistance", ["Complete leptin absence", "Universal MC4R deletion", "No inflammation"], "Obese individuals often have high leptin but reduced response."),
        q("moderate", "Metabolic syndrome includes obesity with:", "Insulin resistance, dyslipidemia, hypertension, and inflammation", ["Scurvy and rickets", "Lead and mercury toxicity", "Only osteoporosis"], "Central obesity is linked to insulin resistance and proinflammatory metabolic disease."),
        q("moderate", "MC4R mutations are associated with:", "Severe monogenic obesity", ["Lead neuropathy", "Vitamin C deficiency", "Alcoholic cirrhosis"], "MC4R variants are among the more common monogenic obesity causes."),
        q("high", "A patient has central obesity, hypertension, hypertriglyceridemia, insulin resistance, and elevated CRP. Adipose tissue cytokines and lipid-induced inflammasome activation contribute to systemic inflammation. Which syndrome is best described?", "Metabolic syndrome", ["Kwashiorkor", "Scurvy", "Minamata disease"], "Metabolic syndrome links visceral obesity with insulin resistance, dyslipidemia, hypertension, and inflammation."),
        q("high", "An obese patient has high circulating leptin but persistent hyperphagia and low response to exogenous leptin. The problem is not absence of fat stores but impaired hypothalamic response to the signal. Which mechanism explains this?", "Leptin resistance", ["Lead inhibition of ferrochelatase", "Vitamin D receptor excess", "Alcohol dehydrogenase deficiency"], "Most common obesity involves resistance to leptin signaling rather than leptin deficiency."),
        q("high", "A child with massive early-onset obesity has a mutation disabling the melanocortin-4 receptor pathway downstream of leptin-responsive hypothalamic neurons. Which regulatory system is primarily disrupted?", "Appetite and energy homeostasis signaling", ["Collagen hydroxylation", "Heme synthesis", "Phase II glucuronidation"], "MC4R participates in hypothalamic control of food intake and energy expenditure."),
    ]),
    ("diet-trace", "Diet, Cancer Risk, and Trace Elements", [
        q("easy", "Iron deficiency causes:", "Microcytic hypochromic anemia", ["Night blindness", "Rickets", "Beriberi"], "Iron is required for hemoglobin synthesis."),
        q("easy", "Iodine deficiency causes:", "Goiter and hypothyroidism", ["Scurvy", "Wrist drop", "Mesothelioma"], "Iodine is needed for thyroid hormone synthesis."),
        q("easy", "Zinc deficiency can cause:", "Acrodermatitis enteropathica-like rash and poor wound healing", ["Lead line", "Hydatid cyst", "Pulmonary edema"], "Zinc is needed for enzymes, immunity, wound healing, and skin integrity."),
        q("moderate", "Selenium deficiency is associated with:", "Cardiomyopathy", ["Night blindness", "Rickets", "Mesothelioma"], "Keshan disease is selenium deficiency cardiomyopathy."),
        q("moderate", "Copper deficiency can impair:", "Collagen cross-linking", ["IgE binding", "LDL receptor uptake", "Vitamin D absorption only"], "Copper is needed for lysyl oxidase and collagen cross-linking."),
        q("moderate", "Aflatoxin exposure is linked to:", "Hepatocellular carcinoma", ["Colon diverticulosis", "Scurvy", "Lead encephalopathy"], "Aflatoxin synergizes with HBV and causes TP53 mutations."),
        q("moderate", "High animal fat and low fiber intake has been implicated in:", "Colon cancer risk", ["Rickets", "Mercury poisoning", "Carbon monoxide death"], "Dietary fat and fiber may influence colon carcinogenesis through bile acids and transit time."),
        q("high", "A population consuming mold-contaminated grains has high hepatocellular carcinoma rates, especially where hepatitis B is endemic. Tumors often contain a characteristic TP53 codon 249 mutation. Which dietary carcinogen is implicated?", "Aflatoxin", ["Nitrite-free fiber", "Vitamin C", "Fluoride"], "Aflatoxin B1 is a dietary hepatocarcinogen with a molecular TP53 signature."),
        q("high", "A child on a restricted artificial diet develops periorificial rash, diarrhea, alopecia, poor wound healing, depressed immunity, and impaired growth. The deficiency affects many enzymes, especially oxidases. Which trace element is lacking?", "Zinc", ["Iodine", "Fluoride", "Selenium"], "Zinc deficiency causes acrodermatitis enteropathica-like lesions and immune/wound defects."),
        q("high", "A region with low soil selenium has patients with dilated cardiomyopathy, while glutathione peroxidase antioxidant function is impaired. Which trace element deficiency best explains this endemic heart disease?", "Selenium", ["Copper", "Iron", "Iodine"], "Selenium is part of glutathione peroxidase; deficiency can cause Keshan cardiomyopathy."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch9-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 9 questions, got {len(chapter_questions)}")
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
    data = json.loads(DATA_PATH.read_text(encoding="utf-8-sig"))
    existing = data.get("questions", [])
    kept = [question for question in existing if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch9-"))]
    data["questions"] = kept + chapter_questions
    validate(chapter_questions, data["questions"])
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Removed {len(existing) - len(kept)} existing Chapter 9 questions")
    print(f"Added {len(chapter_questions)} Robbins Chapter 9 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
