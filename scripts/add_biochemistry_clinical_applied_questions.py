import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Clinical and Applied Biochemistry"
BASE = {
    "subjectId": "biochemistry",
    "subjectTitle": "Biochemistry",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "imageUrls": [],
}

STANDARD = [
    "Which option best completes the clinical biochemistry statement: {clue}?",
    "What is the most appropriate answer for this finding: {clue}?",
    "Which investigation or marker is most directly associated with: {clue}?",
    "Why is this biochemical point clinically useful: {clue}?",
    "Which option best explains the laboratory interpretation: {clue}?",
    "How should this result be interpreted in an exam setting: {clue}?",
    "Which choice is the best single association for: {clue}?",
    "What does this source-book detail most strongly indicate: {clue}?",
    "Which statement is correct regarding: {clue}?",
    "How is this clue best classified in clinical biochemistry: {clue}?",
]

UNIQUE = [
    "A case vignette gives only this clue: '{clue}'. Choose the most likely answer.",
    "Match the laboratory clue with the correct clinical-biochemistry term: {clue}.",
    "A report comment is missing after '{clue}'. Which comment fits best?",
    "Assertion-reason style: the assertion depends on '{clue}'. Select the correct reason.",
    "A viva examiner asks for the high-yield association of '{clue}'. What should be answered?",
]

ORDER = [
    ("standard", 0), ("standard", 1), ("unique", 0), ("standard", 2), ("standard", 3),
    ("standard", 4), ("unique", 1), ("standard", 5), ("standard", 6), ("unique", 2),
    ("standard", 7), ("standard", 8), ("unique", 3), ("standard", 9), ("unique", 4),
]


def q(clue, answer, wrong, explanation):
    return {"clue": clue, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    (
        "clinical-enzymology-biomarkers",
        "Clinical Enzymology and Biomarkers",
        [
            q("non-functional plasma enzymes rise markedly after tissue necrosis", "cell damage releases intracellular enzymes", ["coagulation enzymes are actively secreted", "albumin binds bromocresol green", "kidney excretes hydrogen ions"], "Intracellular enzymes appear in plasma when cells are injured or necrotic."),
            q("no single cardiac marker reliably excludes acute MI within the first 6 hours", "serial cardiac marker testing is needed", ["single LDH estimation is definitive", "urine bilirubin confirms infarction", "serum albumin rises early"], "Early MI diagnosis uses serial testing with markers such as troponin and CK-MB."),
            q("CK-MB starts rising 3-6 hours after myocardial infarction", "early marker of myocardial infarction", ["late marker persisting for months", "specific marker of pancreatitis", "marker of renal tubular function"], "CK-MB is useful early, especially when ECG changes are equivocal."),
            q("CK-MB peaks at 18-24 hours and returns by 36-72 hours", "detection of reinfarction is possible", ["it remains elevated for 8-14 days", "it is unaffected by myocardial necrosis", "it is the best marker of cholestasis"], "Its short duration makes a second rise suggest recurrent ischemia."),
            q("cardiac troponin I is not raised in ordinary skeletal muscle injury", "high cardiac specificity", ["high pancreatic specificity", "low myocardial specificity", "marker of bile obstruction"], "Cardiac troponin isoforms are more specific for myocardial injury than total CK."),
            q("troponins remain elevated for several days after infarction", "late diagnostic window for MI", ["immediate normalization after 6 hours", "false positivity from mild hemolysis", "exclusive marker of liver disease"], "Troponins are useful when the patient presents late after chest pain."),
            q("myoglobin rises within 1-4 hours but is non-specific", "sensitive early but non-specific marker", ["specific marker of hepatocellular jaundice", "late marker of MI only", "marker of prostatic carcinoma"], "Myoglobin appears early but also rises in skeletal muscle damage."),
            q("LDH is about 100 times higher inside RBCs than plasma", "hemolysis can falsely increase LDH", ["LDH is absent from red cells", "LDH is specific for MI", "LDH confirms renal glycosuria"], "Even minor hemolysis can cause a false LDH elevation."),
            q("LDH and AST were previously used for MI but are no longer preferred", "older cardiac markers with lower specificity", ["current first-line markers for early MI", "specific markers of nephrotic syndrome", "tests of gastric acid secretion"], "Troponins and CK-MB replaced LDH/AST for routine MI diagnosis."),
            q("ALP and gamma-glutamyl transferase rise in obstructive liver disease", "cholestatic enzyme pattern", ["myocardial necrosis pattern", "renal tubular acidosis pattern", "hemolytic anemia pattern"], "Canalicular enzymes are classically elevated in cholestasis."),
            q("ALT is more liver-specific than AST", "hepatocellular injury marker", ["marker of ventricular failure", "marker of pancreatic lipase activity", "marker of prostate cancer"], "ALT is concentrated in liver and rises with hepatocellular injury."),
            q("acid phosphatase was historically linked with carcinoma prostate", "prostatic disease marker", ["acute pancreatitis marker", "renal clearance marker", "diabetic control marker"], "Acid phosphatase is a classic older marker for prostate disease."),
            q("prostate-specific antigen is used in prostate disease evaluation", "PSA", ["CK-MB", "troponin T", "serum amylase"], "PSA is clinically used in screening/monitoring prostate pathology."),
            q("serum amylase and lipase rise in acute pancreatitis", "pancreatic enzyme markers", ["cardiac necrosis markers", "cholestatic markers", "glomerular markers"], "Both enzymes support diagnosis of acute pancreatitis, with lipase more pancreas-specific."),
            q("streptokinase and asparaginase are examples of enzymes used in treatment", "therapeutic enzymes", ["immobilized analytical enzymes", "serum electrophoresis bands", "urine preservatives"], "Some enzymes are used therapeutically, not just diagnostically."),
        ],
    ),
    (
        "blood-glucose-diabetes",
        "Blood Glucose, Insulin and Diabetes Mellitus",
        [
            q("brain, RBC and renal medulla require a continuous glucose supply", "importance of blood glucose homeostasis", ["need for bile salt synthesis", "need for albumin electrophoresis", "need for creatinine clearance"], "These tissues depend heavily on glucose availability."),
            q("post-prandial rise in glucose stimulates beta cells", "insulin secretion", ["glucagon secretion", "ketone body excretion", "renin release"], "Insulin is secreted by pancreatic beta cells after a meal."),
            q("insulin promotes glucose storage as glycogen and conversion to fat", "hypoglycemic and storage hormone action", ["hyperglycemic hormone action", "renal clearance effect", "gastric acid secretion"], "Insulin lowers blood glucose and favors storage pathways."),
            q("glucagon, steroids and glycogenolysis increase plasma glucose", "factors causing glucose entry into blood", ["factors depleting blood glucose", "urine preservatives", "cholestatic markers"], "Glucagon and glycogen breakdown raise blood glucose."),
            q("tissue utilization, glycogen synthesis and lipogenesis lower plasma glucose", "factors depleting blood glucose", ["glucose entry mechanisms", "cardiac markers", "renal tubular tests"], "Glucose leaves blood through utilization and storage."),
            q("fasting plasma glucose is used to screen diabetes", "fasting glucose estimation", ["serum amylase", "acid phosphatase", "urine chloride"], "Fasting glucose is a basic diagnostic investigation in diabetes."),
            q("oral glucose tolerance test assesses response after glucose load", "OGTT", ["creatinine clearance", "serum electrophoresis", "gastric juice analysis"], "OGTT tests the body's ability to handle an oral glucose load."),
            q("impaired glucose tolerance is diagnosed from abnormal post-load glucose", "prediabetic OGTT pattern", ["obstructive jaundice", "nephrotic syndrome", "respiratory alkalosis"], "IGT is a category between normal glucose tolerance and diabetes."),
            q("glucose in urine may occur when blood glucose exceeds renal threshold", "glycosuria", ["ketonuria only", "albuminuria", "bilirubinuria"], "Hyperglycemia can produce urinary glucose."),
            q("Benedict test detects reducing substances in urine", "urinary reducing sugar test", ["specific HbA1c assay", "specific troponin assay", "bilirubin conjugation test"], "Benedict test is a classical non-specific reducing substance test."),
            q("diabetic ketoacidosis occurs due to insulin deficiency with lipolysis and ketogenesis", "acute metabolic complication of diabetes", ["chronic cholestasis", "respiratory alkalosis", "albumin-globulin reversal"], "Insulin deficiency promotes ketone-body production and acidosis."),
            q("hyperosmolar nonketotic coma is classically severe hyperglycemia with dehydration", "hyperosmolar diabetic emergency", ["pancreatic enzyme leak", "prostatic marker rise", "bile duct obstruction"], "Marked hyperglycemia causes osmotic diuresis and dehydration."),
            q("glycated hemoglobin reflects glucose exposure over previous weeks", "HbA1c", ["OGTT only", "Benedict test", "serum fructose"], "HbA1c is used for long-term glycemic monitoring."),
            q("insulin is synthesized as preproinsulin and processed to insulin", "insulin biosynthesis", ["glucagon conversion to insulin", "albumin cleavage", "CK-MB dimerization"], "Insulin synthesis involves precursor processing."),
            q("microvascular complications involve retina, kidney and nerves", "chronic diabetic complications", ["acute pancreatitis", "prostate cancer", "milk protein allergy"], "Diabetes damages small vessels, causing retinopathy, nephropathy and neuropathy."),
        ],
    ),
    (
        "cardiovascular-hyperlipidemias",
        "Cardiovascular Diseases and Hyperlipidemias",
        [
            q("LDL is called bad cholesterol", "cholesterol delivery to peripheral tissues", ["reverse cholesterol transport", "TAG transport from gut", "albumin oncotic pressure"], "LDL carries cholesterol from liver to tissues and is atherogenic."),
            q("HDL is called good cholesterol", "reverse cholesterol transport", ["cholesterol delivery to tissues", "exogenous TAG transport", "bile pigment excretion"], "HDL returns cholesterol from tissues to liver."),
            q("chylomicrons mainly transport dietary triacylglycerol", "TAG from gut to muscle and adipose tissue", ["cholesterol from tissues to liver", "albumin-bound bilirubin", "ketone bodies to brain"], "Chylomicrons are the major exogenous TAG carriers."),
            q("VLDL transports triacylglycerol synthesized in liver", "endogenous TAG transport", ["reverse cholesterol transport", "oxygen transport", "urinary nitrogen transport"], "VLDL moves hepatic TAG to peripheral tissues."),
            q("LDL has beta electrophoretic mobility", "beta-lipoprotein", ["pre-beta VLDL fraction", "alpha HDL fraction", "origin chylomicron band"], "LDL migrates in the beta region."),
            q("HDL has alpha electrophoretic mobility", "alpha-lipoprotein", ["beta LDL fraction", "pre-beta VLDL fraction", "chylomicron origin band"], "HDL migrates in the alpha region."),
            q("Apo B-100 is the major apoprotein of LDL", "LDL receptor recognition ligand", ["Apo B-48 of chylomicrons", "Apo A-I of HDL", "albumin ligand"], "Apo B-100 is important for LDL receptor binding."),
            q("foam cells form when macrophages take up oxidized LDL", "early atherosclerotic lesion", ["renal tubular cast", "gastric parietal cell", "pancreatic acinar cell"], "Oxidized LDL uptake creates lipid-laden foam cells."),
            q("coronary arteries and cerebral vessels are common atherosclerosis sites", "clinically important arterial involvement", ["venous valve calcification", "glomerular basement membrane only", "gastric mucosa only"], "Atherosclerosis commonly affects large and medium arteries."),
            q("high LDL and low HDL increase coronary risk", "atherogenic lipid profile", ["protective lipid profile", "normal renal profile", "obstructive jaundice profile"], "LDL is atherogenic while HDL is protective."),
            q("hsCRP is used as an inflammatory risk marker", "cardiovascular risk prediction", ["pancreatitis confirmation", "GFR calculation", "gastric acid estimation"], "High-sensitivity CRP reflects inflammatory risk in CAD."),
            q("Lp(a) is an independent atherogenic lipoprotein risk factor", "cardiovascular risk marker", ["milk protein fraction", "renal tubular enzyme", "gastric secretion marker"], "Lp(a) is linked with increased atherosclerotic risk."),
            q("familial hypercholesterolemia commonly involves LDL receptor defect", "type IIa hyperlipoproteinemia pattern", ["chylomicron lipase excess", "HDL overproduction", "albumin deficiency"], "LDL receptor defects cause marked LDL cholesterol elevation."),
            q("lipoprotein lipase deficiency causes chylomicronemia", "type I hyperlipoproteinemia pattern", ["isolated LDL rise", "isolated HDL rise", "bile acid deficiency"], "LPL deficiency prevents chylomicron TAG clearance."),
            q("diet, exercise, smoking cessation and lipid-lowering therapy reduce CAD risk", "prevention of atherosclerosis", ["increasing trans fat intake", "withholding BP control", "raising LDL deliberately"], "Risk reduction targets lipids and other modifiable factors."),
        ],
    ),
    (
        "liver-gastric-function-tests",
        "Liver and Gastric Function Tests",
        [
            q("normal LFT values do not exclude disease because liver has large reserve", "interpret LFT with clinical picture", ["LFT alone proves normal liver", "bilirubin alone diagnoses MI", "albumin rises in cirrhosis"], "Liver reserve can mask early disease."),
            q("ALT and AST rise prominently in hepatocellular injury", "markers of hepatocyte damage", ["markers of cholestasis only", "markers of GFR", "markers of gastric acid"], "Transaminases indicate hepatocellular damage."),
            q("ALP and GGT rise prominently in obstruction", "cholestatic pattern", ["hemolytic pattern", "diabetic pattern", "renal tubular pattern"], "Canalicular enzymes rise in cholestasis."),
            q("serum bilirubin and urine bilirubin help evaluate jaundice", "bile pigment excretion tests", ["synthetic function tests only", "gastric acid tests", "cardiac markers"], "Bilirubin tests classify and monitor jaundice."),
            q("albumin and prothrombin time assess hepatic synthesis", "synthetic function of liver", ["hepatocellular leakage only", "tubular secretion only", "gastric HCl output"], "Liver synthesizes albumin and clotting factors."),
            q("prolonged prothrombin time may reflect impaired clotting factor synthesis", "defective hepatic synthetic function", ["increased GFR", "high insulin action", "pancreatic lipase excess"], "PT is sensitive to reduced hepatic synthesis or vitamin K problems."),
            q("low albumin in chronic liver disease can cause edema", "reduced oncotic pressure", ["high GFR", "respiratory alkalosis", "increased gastric HCl"], "Albumin maintains plasma oncotic pressure."),
            q("unconjugated bilirubin predominates in hemolytic jaundice", "prehepatic jaundice pattern", ["obstructive jaundice pattern", "renal failure pattern", "diabetic ketoacidosis"], "Excess heme breakdown increases unconjugated bilirubin."),
            q("conjugated bilirubin and alkaline phosphatase rise in obstruction", "posthepatic cholestatic jaundice", ["hemolytic anemia", "nephrotic syndrome", "respiratory acidosis"], "Biliary obstruction causes conjugated hyperbilirubinemia and cholestatic enzymes."),
            q("hepatocellular jaundice can show mixed bilirubin and high transaminases", "liver-cell injury pattern", ["isolated renal tubular pattern", "pure gastric acid pattern", "pure cardiac marker pattern"], "Hepatocyte injury impairs uptake/conjugation/excretion and leaks enzymes."),
            q("detoxification of ammonia into urea is a liver function", "metabolic detoxification function", ["renal filtration only", "gastric digestion only", "HDL transport"], "The liver detoxifies ammonia by urea synthesis."),
            q("bile acids help absorb fat and fat-soluble vitamins", "digestive function of bile", ["albumin electrophoresis", "creatinine clearance", "troponin release"], "Bile acids emulsify lipids and aid absorption."),
            q("gastric juice analysis evaluates acid secretion", "gastric function testing", ["renal concentration test", "serum protein electrophoresis", "cardiac marker test"], "Gastric analysis measures HCl secretion patterns."),
            q("achlorhydria means absence of free HCl in gastric juice", "loss of gastric acid secretion", ["excess HCl secretion", "renal bicarbonate wasting", "bile duct obstruction"], "Achlorhydria indicates absent gastric acid."),
            q("pentagastrin or histamine stimulation assesses parietal cell acid output", "stimulated gastric acid secretion test", ["glomerular clearance test", "lipoprotein electrophoresis", "troponin assay"], "Stimulation tests evaluate gastric secretory reserve."),
        ],
    ),
    (
        "kidney-function-tests",
        "Kidney Function Tests",
        [
            q("the nephron is the functional unit of kidney", "glomerulus and tubules together perform renal function", ["hepatocyte", "pancreatic acinus", "cardiac myofibril"], "Renal tests assess nephron function."),
            q("earliest glomerular abnormality may be albumin in urine", "proteinuria from increased glomerular permeability", ["glycosuria from insulin excess", "bilirubinuria from hemolysis", "ketonuria from alkalosis"], "Albumin appears when glomerular selectivity is impaired."),
            q("GFR falls when blood pressure is below about 80 mm Hg", "reduced glomerular filtration", ["increased tubular secretion", "increased gastric acid", "increased HDL"], "Low perfusion pressure reduces filtration."),
            q("inulin clearance is a reference method for GFR", "ideal filtration marker", ["tubular secretion marker", "liver synthesis marker", "cardiac necrosis marker"], "Inulin is filtered and not reabsorbed or secreted."),
            q("creatinine clearance is commonly used to estimate GFR", "practical renal function test", ["specific liver enzyme test", "gastric secretion test", "pancreatic marker"], "Creatinine clearance approximates GFR in practice."),
            q("plasma creatinine rises when GFR falls", "renal function impairment", ["improved filtration", "isolated cholestasis", "hyperinsulinemia"], "Creatinine accumulates as filtration decreases."),
            q("urea is affected by diet and protein catabolism", "less specific renal marker than creatinine", ["perfect GFR marker", "specific cardiac marker", "specific pancreatic marker"], "Blood urea is influenced by nonrenal factors."),
            q("complete urine analysis screens kidney disease", "routine renal screening test", ["definitive liver synthetic test", "specific MI marker", "OGTT"], "Urinalysis detects protein, cells, casts and abnormal constituents."),
            q("plasma electrolytes are part of renal assessment", "water and electrolyte regulation by kidney", ["cardiac troponin monitoring", "gastric acid output", "LDL receptor testing"], "Kidneys regulate sodium, potassium and acid-base balance."),
            q("concentration and dilution tests assess tubules", "renal tubular function", ["glomerular permeability only", "liver excretory function", "pancreatic function"], "Tubules regulate urine concentration and dilution."),
            q("renal acidification tests assess hydrogen ion excretion", "tubular acid-base function", ["lipoprotein clearance", "gastric HCl secretion", "cardiac ATP turnover"], "Kidneys maintain pH by acid excretion and bicarbonate handling."),
            q("microalbuminuria is important in diabetes", "early diabetic nephropathy marker", ["late MI marker", "pancreatic enzyme marker", "gastric malignancy marker"], "Small albumin loss can signal early kidney damage in diabetes."),
            q("renal excretion of potassium affects heart function", "kidney role in potassium balance", ["liver role in albumin synthesis", "pancreatic role in lipase release", "brain role in ketone use"], "Potassium disturbances can cause cardiac arrhythmias."),
            q("kidney activates vitamin D", "calcitriol production", ["bilirubin conjugation", "insulin synthesis", "albumin synthesis"], "Renal 1-alpha hydroxylation produces active vitamin D."),
            q("kidney produces erythropoietin", "renal endocrine function", ["hepatic detoxification", "gastric digestion", "lipoprotein transport"], "Erythropoietin from kidney supports erythropoiesis."),
        ],
    ),
    (
        "plasma-proteins",
        "Plasma Proteins",
        [
            q("serum is defibrinated plasma", "serum lacks fibrinogen and clotting factors", ["serum contains more fibrinogen than plasma", "serum is whole blood", "serum is urine supernatant"], "Clotting removes fibrinogen and some clotting factors."),
            q("normal total plasma protein is about 6-8 g/dL", "total plasma protein concentration", ["serum sodium level", "urine protein cutoff", "blood glucose level"], "This is the usual total plasma protein range."),
            q("albumin concentration is about 3.5-5 g/dL", "major plasma protein fraction", ["minor clotting factor", "main immunoglobulin fraction", "urinary pigment"], "Albumin is the most abundant plasma protein."),
            q("albumin:globulin ratio is about 1.2:1 to 1.5:1", "normal A:G ratio", ["normal anion gap", "normal pH", "normal cholesterol ratio"], "A:G ratio helps interpret plasma protein disorders."),
            q("almost all plasma proteins except immunoglobulins are synthesized in liver", "hepatic synthesis of plasma proteins", ["renal synthesis of albumin", "gastric synthesis of globulins", "cardiac synthesis of fibrinogen"], "The liver is the major source of plasma proteins."),
            q("Biuret method estimates total protein", "serum total protein assay", ["albumin dye-binding only", "troponin immunoassay", "creatinine clearance"], "Biuret reaction is used for total proteins."),
            q("bromocresol green preferentially binds albumin", "albumin estimation method", ["urea estimation method", "bilirubin conjugation method", "LDL precipitation method"], "BCG dye-binding is a common albumin assay."),
            q("agar gel electrophoresis separates serum into five bands", "albumin, alpha1, alpha2, beta and gamma fractions", ["only albumin and fibrinogen", "only LDL and HDL", "only urea and creatinine"], "Serum protein electrophoresis classically shows five bands."),
            q("albumin maintains plasma oncotic pressure", "fluid distribution function", ["oxygen carriage", "renal filtration", "gastric acid secretion"], "Albumin prevents excessive movement of fluid into tissues."),
            q("albumin transports bilirubin, fatty acids and many drugs", "transport function of albumin", ["clotting factor activation only", "urea synthesis", "acid secretion"], "Albumin is an important carrier protein."),
            q("hypoalbuminemia causes edema", "low oncotic pressure", ["high troponin", "high GFR", "alkaline urine"], "Low albumin reduces plasma oncotic pressure."),
            q("nephrotic syndrome can cause hypoalbuminemia", "urinary albumin loss", ["increased albumin synthesis only", "gastric HCl loss", "cardiac necrosis"], "Proteinuria can lower serum albumin."),
            q("gamma region contains immunoglobulins", "antibody fraction", ["albumin fraction", "fibrinogen fraction in serum", "pre-beta fraction"], "Immunoglobulins migrate mainly in gamma region."),
            q("acute phase proteins rise in inflammation", "positive acute-phase response", ["decrease in all globulins", "specific MI-only marker", "renal clearance estimate"], "Inflammation changes plasma protein pattern."),
            q("alpha-1 antitrypsin deficiency affects lung and liver", "protease inhibitor deficiency", ["albumin dye defect", "creatinine assay error", "bilirubin transport excess"], "Alpha-1 antitrypsin is an important antiprotease."),
        ],
    ),
    (
        "acid-base-balance",
        "Acid-Base Balance and pH",
        [
            q("Bronsted acids donate protons", "acid", ["base", "buffer only", "zwitterion only"], "Acids are proton donors."),
            q("Bronsted bases accept protons", "base", ["acid", "strong electrolyte only", "non-electrolyte"], "Bases are proton acceptors."),
            q("pH is negative logarithm of hydrogen ion concentration", "-log[H+]", ["log[OH-]", "[H+] x [OH-]", "pCO2/HCO3"], "pH expresses hydrogen ion concentration logarithmically."),
            q("blood pH is maintained by buffers, lungs and kidney", "acid-base homeostasis", ["albumin electrophoresis", "lipoprotein transport", "enzyme leakage"], "Body pH depends on chemical buffers plus respiratory and renal regulation."),
            q("bicarbonate buffer system is the major extracellular buffer", "HCO3-/H2CO3 buffer", ["phosphate-only buffer", "hemoglobin-only buffer", "albumin-only buffer"], "The bicarbonate system is central in plasma."),
            q("lungs regulate pH by changing CO2 elimination", "respiratory regulation", ["renal glucose filtration", "hepatic albumin synthesis", "gastric HCl secretion"], "Ventilation changes carbonic acid through CO2."),
            q("kidney regulates pH by hydrogen ion excretion and bicarbonate handling", "renal regulation", ["troponin release", "insulin secretion", "LDL uptake"], "Kidneys provide slower but powerful acid-base regulation."),
            q("fall in pH with rise in pCO2", "respiratory acidosis", ["metabolic acidosis due to bicarbonate loss", "respiratory alkalosis due to hyperventilation", "metabolic alkalosis due to acid loss"], "CO2 retention causes respiratory acidosis."),
            q("rise in pH with fall in pCO2", "respiratory alkalosis", ["CO2 retention pattern", "fixed acid accumulation pattern", "primary bicarbonate excess pattern"], "Hyperventilation lowers CO2 and raises pH."),
            q("fall in pH with primary fall in bicarbonate", "metabolic acidosis", ["primary carbon dioxide retention", "primary carbon dioxide washout", "primary bicarbonate excess"], "Loss of bicarbonate or gain of fixed acid causes metabolic acidosis."),
            q("rise in pH with primary rise in bicarbonate", "metabolic alkalosis", ["ventilatory CO2 retention", "hyperventilation with low pCO2", "ketoacid accumulation"], "Excess bicarbonate or acid loss causes metabolic alkalosis."),
            q("diabetic ketoacidosis is an example", "metabolic acidosis", ["vomiting-induced alkalosis", "hyperventilation-induced alkalosis", "CO2-retention acidosis"], "Ketone bodies add fixed acid."),
            q("persistent vomiting can cause acid loss", "metabolic alkalosis", ["metabolic acidosis", "respiratory acidosis", "renal glycosuria"], "Loss of gastric HCl favors metabolic alkalosis."),
            q("hyperventilation is compensation for metabolic acidosis", "respiratory compensation", ["renal compensation only", "albumin buffering failure", "lipoprotein clearance"], "Blowing off CO2 helps raise pH."),
            q("pH changes affect protein charge and configuration", "hydrogen ion effect on proteins", ["LDL receptor mutation", "fibrinogen removal", "creatinine secretion"], "Protein structure and function are pH-sensitive."),
        ],
    ),
    (
        "electrolyte-water-balance",
        "Electrolyte and Water Balance",
        [
            q("total body water is about 60 percent of body weight", "body water compartment estimate", ["plasma protein range", "GFR", "OGTT cutoff"], "Adult total body water is roughly 60%."),
            q("intracellular fluid is about 40 percent of body weight", "ICF compartment", ["ECF compartment", "plasma compartment", "fecal water output"], "Most body water is intracellular."),
            q("extracellular fluid is about 20 percent of body weight", "ECF compartment", ["ICF compartment", "gastric juice", "RBC volume only"], "ECF includes plasma and interstitial fluid."),
            q("intravascular fluid is about 4 percent of body weight", "plasma water compartment", ["intracellular compartment", "interstitial compartment", "transcellular fluid only"], "Plasma is the intravascular part of ECF."),
            q("oxidation of fat yields more water per gram than carbohydrate or protein", "metabolic water from fat", ["urinary water only", "water from albumin", "water from sodium"], "Fat oxidation produces relatively more metabolic water."),
            q("thirst center is stimulated by increased blood osmolality", "water intake regulation", ["low LDL", "high albumin", "low troponin"], "Hyperosmolality stimulates thirst."),
            q("kidney is the major controller of water output", "renal regulation of water balance", ["liver only", "gastric mucosa only", "skeletal muscle only"], "Urine output is the main regulated water loss."),
            q("skin water loss increases during fever", "increased insensible/perspiratory loss", ["renal concentration only", "LDL oxidation", "albumin synthesis"], "Water loss through skin rises with temperature."),
            q("sodium is the major extracellular cation", "ECF sodium dominance", ["ICF potassium dominance", "plasma protein dominance", "intracellular chloride dominance"], "Na+ is high in extracellular fluid."),
            q("potassium is the major intracellular cation", "ICF potassium dominance", ["ECF sodium dominance", "plasma calcium dominance", "extracellular phosphate dominance"], "K+ is high inside cells."),
            q("aldosterone promotes sodium retention and potassium excretion", "mineralocorticoid action", ["insulin action", "glucagon action", "troponin action"], "Aldosterone controls Na+/K+ handling."),
            q("renin-angiotensin system helps maintain sodium and water balance", "RAAS", ["OGTT", "CK-MB", "SPEP"], "RAAS regulates vascular tone, aldosterone and volume."),
            q("hyponatremia means low plasma sodium", "sodium deficit/dilution state", ["high potassium", "high chloride", "low albumin"], "Hyponatremia is reduced serum sodium."),
            q("hyperkalemia can cause cardiac arrhythmias", "dangerous potassium excess", ["low LDL risk", "low bilirubin risk", "high albumin risk"], "Potassium disturbances affect cardiac excitability."),
            q("chloride generally follows sodium in extracellular fluid", "major extracellular anion", ["major intracellular cation", "main plasma protein", "cardiac marker"], "Cl- is a major ECF anion."),
        ],
    ),
    (
        "body-fluids",
        "Body Fluids: Milk, CSF and Amniotic Fluid",
        [
            q("milk lacks relatively important amounts of iron, copper and vitamin C", "nutrients low in milk", ["high lactose and casein", "high sodium and chloride", "high urea and creatinine"], "Milk is nearly complete but poor in iron, copper and vitamin C."),
            q("lactose synthase contains galactosyl transferase and alpha-lactalbumin", "enzyme system for lactose synthesis", ["lactase and amylase", "albumin and fibrinogen", "renin and angiotensin"], "Alpha-lactalbumin modifies galactosyl transferase to synthesize lactose."),
            q("prolactin increases alpha-lactalbumin after parturition", "initiation of lactose synthesis", ["insulin degradation", "bilirubin conjugation", "LDL oxidation"], "Prolactin controls the modifier subunit needed for lactose synthase."),
            q("human milk has higher carbohydrate and lower protein than cow milk", "difference between human and cow milk", ["cow milk has no protein", "human milk lacks lactose", "both are identical"], "Human milk is relatively carbohydrate-rich and protein-poor."),
            q("to humanize cow milk, dilute protein and add sugar", "modify cow milk composition for infants", ["add more protein only", "remove all lactose", "add bile salts"], "Dilution plus carbohydrate addition makes cow milk closer to human milk."),
            q("white color of milk is due to emulsified fat and calcium caseinate", "physical appearance of milk", ["bilirubin", "hemoglobin", "LDL cholesterol"], "Milk opacity comes from fat globules and caseinate."),
            q("medium-chain fatty acids in milk are easily digested and absorbed", "digestibility of milk fat", ["need chylomicrons exclusively", "cannot be absorbed", "cause renal failure"], "MCFA are handled more readily than long-chain fats."),
            q("colostrum is rich in immunoglobulins", "early passive immunity", ["high creatinine", "high CK-MB", "high bilirubin"], "Colostrum provides antibodies to the newborn."),
            q("CSF is normally clear and has low protein", "normal cerebrospinal fluid feature", ["high fibrinogen like plasma", "high RBC count normally", "milky lipid-rich fluid"], "CSF normally has low protein and few cells."),
            q("CSF glucose is lower than plasma but depends on blood glucose", "CSF glucose interpretation", ["unrelated to plasma glucose", "always zero", "always higher than plasma"], "CSF glucose must be interpreted with plasma glucose."),
            q("in bacterial meningitis, CSF glucose falls and proteins rise", "infective CSF pattern", ["normal CSF pattern", "milk intolerance pattern", "nephrotic pattern"], "Bacterial infection consumes glucose and increases permeability."),
            q("amniotic fluid analysis can assess fetal maturity", "prenatal biochemical assessment", ["cardiac enzyme diagnosis", "adult renal clearance", "lipoprotein electrophoresis"], "Amniotic fluid provides fetal diagnostic information."),
            q("lecithin:sphingomyelin ratio assesses fetal lung maturity", "L/S ratio", ["A:G ratio", "LDL:HDL ratio", "anion gap"], "L/S ratio reflects surfactant maturity."),
            q("amniocentesis samples amniotic fluid", "prenatal diagnostic sampling", ["renal biopsy", "gastric aspiration", "serum electrophoresis"], "Amniocentesis obtains fluid for fetal testing."),
            q("lactase deficiency in infants can cause diarrhea after milk feeding", "lactose intolerance", ["diabetic ketoacidosis", "cholestasis", "respiratory alkalosis"], "Undigested lactose causes osmotic symptoms and fermentation."),
        ],
    ),
    (
        "lab-screening-quality-control",
        "Clinical Laboratory Screening and Quality Control",
        [
            q("three-generation family history helps prenatal genetic evaluation", "pedigree analysis", ["OGTT", "creatinine clearance", "gastric analysis"], "Pedigree analysis identifies inherited risk."),
            q("amniocytes can be cultured for enzyme assay in inborn errors", "prenatal diagnosis by amniocentesis", ["cardiac marker testing", "urine glucose screening", "gastric acid analysis"], "Cultured amniocytes allow enzyme-based diagnosis."),
            q("chorionic villus sampling allows earlier prenatal diagnosis", "CVS", ["OGTT", "SPEP", "LFT"], "CVS samples placental tissue genetically similar to fetus."),
            q("FISH detects common aneuploidies involving chromosomes 13, 18, 21, X and Y", "molecular cytogenetic screening", ["enzyme immobilization", "albumin dye binding", "urine preservation"], "FISH probes target common chromosomal abnormalities."),
            q("biochemical screening is cheap and quick but not definitive", "screening test limitation", ["diagnostic certainty", "therapeutic enzyme use", "renal clearance"], "Screening identifies risk, while diagnostic tests confirm."),
            q("newborn screening detects treatable metabolic disorders early", "preventive metabolic screening", ["late MI diagnosis", "gastric acidity", "lipoprotein density"], "Early detection can prevent irreversible damage."),
            q("phenylketonuria is a classic newborn screening target", "inborn error screening", ["cholestatic jaundice marker", "cardiac failure marker", "renal sodium test"], "PKU is screened early because treatment prevents neurologic injury."),
            q("sample collection timing, diet and posture can affect results", "pre-analytical variables", ["external quality assurance", "analytical specificity only", "therapeutic enzyme effect"], "Pre-analytical factors can change laboratory results."),
            q("EDTA is an anticoagulant for many hematology samples", "prevention of clotting by calcium chelation", ["glucose preservation by fluoride", "protein precipitation by sulfate", "bilirubin conjugation"], "EDTA chelates calcium and prevents coagulation."),
            q("fluoride is used to preserve blood glucose", "inhibition of glycolysis", ["activation of amylase", "release of troponin", "increase of bilirubin"], "Fluoride inhibits glycolysis in collected blood."),
            q("accuracy means closeness to true value", "analytical accuracy", ["reproducibility", "detection of disease only", "absence of interference only"], "Accuracy describes agreement with the true value."),
            q("precision means reproducibility of repeated measurements", "analytical precision", ["truth of result", "clinical sensitivity", "screening prevalence"], "Precision describes repeatability."),
            q("sensitivity is ability to detect disease when disease is present", "true-positive rate", ["true-negative rate", "reproducibility", "closeness to true value"], "Sensitivity reduces false negatives."),
            q("specificity is ability to exclude disease when disease is absent", "true-negative rate", ["true-positive rate", "precision", "accuracy"], "Specificity reduces false positives."),
            q("Levey-Jennings charts are used in laboratory quality control", "quality control chart", ["OGTT plot", "lipoprotein profile", "cardiac marker curve"], "Control charts monitor analytical performance over time."),
        ],
    ),
]


def make_prompt(index, clue):
    kind, template_index = ORDER[index - 1]
    source = STANDARD if kind == "standard" else UNIQUE
    return source[template_index].format(clue=clue)


def rotate(items, offset):
    if not items:
        return []
    offset %= len(items)
    return items[offset:] + items[:offset]


def make_options(answer, wrong, topic_answers, chapter_answers, offset):
    options = []
    candidates = rotate(wrong, offset) + rotate([a for a in topic_answers if a != answer], offset) + rotate([a for a in chapter_answers if a != answer], offset)
    for candidate in candidates:
        if candidate != answer and candidate not in options:
            options.append(candidate)
        if len(options) == 3:
            break
    if len(options) < 3:
        raise ValueError(f"Not enough distractors for {answer}")
    options.insert(offset % 4, answer)
    return options


def main():
    chapter_answers = []
    for _, _, rows in TOPICS:
        for row in rows:
            if row["answer"] not in chapter_answers:
                chapter_answers.append(row["answer"])

    questions = []
    for ti, (slug, topic, rows) in enumerate(TOPICS):
        if len(rows) != 15:
            raise ValueError(f"{topic} has {len(rows)} rows")
        topic_answers = []
        for row in rows:
            if row["answer"] not in topic_answers:
                topic_answers.append(row["answer"])
        for qi, row in enumerate(rows, 1):
            options = make_options(row["answer"], row["wrong"], topic_answers, chapter_answers, ti + qi)
            questions.append(
                {
                    **BASE,
                    "id": f"biochemistry-clinical-applied-{slug}-{qi:02d}",
                    "topic": topic,
                    "topicTitle": topic,
                    "difficulty": "moderate" if qi <= 6 else "high" if qi <= 12 else "very high",
                    "prompt": make_prompt(qi, row["clue"]),
                    "options": options,
                    "answerIndex": options.index(row["answer"]),
                    "answer": row["answer"],
                    "explanation": row["explanation"],
                }
            )

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [
        question
        for question in data.get("questions", [])
        if not (question.get("subjectId") == "biochemistry" and question.get("chapterTitle") == CHAPTER)
    ] + questions

    if len(TOPICS) != 10 or len(questions) != 150:
        raise ValueError("Expected 10 topics and 150 questions")
    if len({q["id"] for q in questions}) != len(questions):
        raise ValueError("Duplicate IDs")
    if len({q["prompt"] for q in questions}) != len(questions):
        raise ValueError("Duplicate prompts")
    if any(q["answer"] != q["options"][q["answerIndex"]] for q in questions):
        raise ValueError("Answer mapping failed")

    data["questions"].sort(key=lambda item: item.get("id", ""))
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")
    for _, topic, _ in TOPICS:
        print(f"- {topic}")


if __name__ == "__main__":
    main()
