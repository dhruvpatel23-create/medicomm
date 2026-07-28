import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Pancreas"
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
    ("normal-congenital", "Normal Pancreas, Developmental Anomalies, and Cystic Fibrosis", [
        q("easy", "The exocrine pancreas mainly secretes:", "Digestive enzymes", ["Thyroid hormone", "Bile salts", "Erythropoietin"], "Acinar cells produce digestive enzymes that drain through ducts."),
        q("easy", "Islets of Langerhans are the endocrine component of the:", "Pancreas", ["Spleen", "Gallbladder", "Appendix"], "Pancreatic islets contain hormone-secreting endocrine cells."),
        q("easy", "Cystic fibrosis injures the pancreas mainly by causing:", "Duct obstruction by thick secretions", ["Autoimmune beta-cell destruction", "Portal hypertension", "Iron overload"], "Thick secretions obstruct ducts and damage exocrine tissue."),
        q("moderate", "Annular pancreas can cause:", "Duodenal obstruction", ["Esophageal varices", "Ulcerative colitis", "Hemarthrosis"], "A ring of pancreatic tissue may encircle and narrow the duodenum."),
        q("moderate", "Pancreas divisum results from failure of fusion of:", "Dorsal and ventral pancreatic ducts", ["Portal and hepatic veins", "Cystic and common hepatic ducts", "Ileum and cecum"], "Separate duct drainage may predispose to pancreatitis."),
        q("moderate", "Ectopic pancreas is pancreatic tissue located:", "Outside the normal pancreas", ["Only within islets", "Inside gallstones", "Within bone marrow"], "Heterotopic pancreatic tissue can occur in stomach or duodenum."),
        q("moderate", "In cystic fibrosis, pancreatic malabsorption is due to loss of:", "Exocrine acinar function", ["Kupffer cells", "Parietal cells", "Megakaryocytes"], "Duct obstruction causes acinar atrophy and enzyme deficiency."),
        q("high", "An infant has meconium ileus and later develops bulky foul-smelling stools. The pancreas shows dilated ducts plugged by inspissated secretions with acinar atrophy and fibrosis. Which inherited disease explains this?", "Cystic fibrosis", ["Hirschsprung disease", "Wilson disease", "Hereditary hemochromatosis"], "CFTR dysfunction causes thick secretions and exocrine pancreatic failure."),
        q("high", "A newborn develops vomiting from duodenal narrowing, and imaging suggests pancreatic tissue encircling the second part of the duodenum. Which developmental anomaly best explains the obstruction?", "Annular pancreas", ["Pancreas divisum", "Ectopic spleen", "Meckel diverticulum"], "Annular pancreas can wrap around the duodenum and obstruct it."),
        q("high", "A patient with recurrent pancreatitis has most pancreatic drainage passing through the minor papilla because the embryologic duct systems failed to join. Which anomaly is present?", "Pancreas divisum", ["Annular pancreas", "Biliary atresia", "Choledochal cyst"], "Pancreas divisum is failure of dorsal and ventral duct fusion."),
    ]),
    ("acute-pancreatitis", "Acute Pancreatitis: Causes, Morphology, and Complications", [
        q("easy", "The two most common causes of acute pancreatitis are:", "Gallstones and alcohol", ["Gluten and aspirin", "Smoking and asbestos", "Iron and copper"], "Biliary tract disease and alcohol are the major causes."),
        q("easy", "Acute pancreatitis involves autodigestion by activated:", "Pancreatic enzymes", ["Gastric parietal cells", "Red blood cells", "Bile pigments"], "Premature enzyme activation injures pancreatic tissue."),
        q("easy", "Fat necrosis in pancreatitis produces deposits of:", "Calcium soaps", ["Urate crystals", "Amyloid", "Melanin"], "Lipase releases fatty acids that bind calcium."),
        q("moderate", "Serum lipase is useful in acute pancreatitis because it:", "Remains elevated longer than amylase", ["Measures insulin secretion", "Detects gallbladder cancer", "Counts neutrophils"], "Lipase is relatively specific and persists longer."),
        q("moderate", "Hemorrhagic pancreatitis may show blue discoloration around the umbilicus called:", "Cullen sign", ["Kayser-Fleischer ring", "Virchow node", "Trousseau sign"], "Periumbilical ecchymosis can occur with severe hemorrhagic pancreatitis."),
        q("moderate", "The key initiating event in acute pancreatitis is:", "Inappropriate intrapancreatic trypsin activation", ["Loss of intrinsic factor", "APC mutation", "Portal-systemic shunting"], "Trypsin activation triggers activation of other enzymes."),
        q("moderate", "A pancreatic pseudocyst lacks:", "Epithelial lining", ["Fibrous wall", "Enzymatic debris", "Fluid content"], "Pseudocysts are walled-off collections without true epithelium."),
        q("high", "A patient with gallstones develops severe epigastric pain radiating to the back, elevated lipase, and chalky white fat necrosis in peripancreatic tissue. Which mechanism produced the chalky deposits?", "Lipase-mediated fat necrosis with calcium saponification", ["Amyloid deposition", "Bilirubin precipitation", "Urate crystal formation"], "Released fatty acids bind calcium to form chalky soaps."),
        q("high", "A patient with acute pancreatitis later has a persistent cystic peripancreatic collection rich in enzymes and necrotic debris. The wall is granulation and fibrous tissue without epithelium. What is it?", "Pancreatic pseudocyst", ["Mucinous cystic neoplasm", "Serous cystadenoma", "Choledochal cyst"], "Pseudocysts are post-pancreatitis collections lacking epithelial lining."),
        q("high", "A heavy alcohol user develops shock, hypocalcemia, respiratory distress, and extensive pancreatic hemorrhage after premature activation of pancreatic proenzymes. Which complication pattern is most likely?", "Severe acute necrotizing pancreatitis", ["Chronic autoimmune pancreatitis", "Pancreatic adenoma", "Insulinoma"], "Severe acute pancreatitis can cause necrosis, hemorrhage, and systemic inflammatory complications."),
    ]),
    ("chronic-pancreatitis", "Chronic Pancreatitis and Exocrine Pancreatic Insufficiency", [
        q("easy", "Chronic pancreatitis is characterized by irreversible:", "Fibrosis and loss of acini", ["Pure edema only", "Only islet hyperplasia", "Gallbladder dysplasia"], "Repeated injury causes fibrosis and exocrine loss."),
        q("easy", "A common cause of chronic pancreatitis in adults is:", "Long-term alcohol use", ["Acute appendicitis", "Celiac sprue", "Asthma"], "Alcohol is a major cause in many settings."),
        q("easy", "Exocrine pancreatic insufficiency commonly causes:", "Steatorrhea", ["Hematemesis", "Hematuria", "Hemarthrosis"], "Poor lipase delivery causes fat malabsorption."),
        q("moderate", "Pancreatic calcifications on imaging favor:", "Chronic pancreatitis", ["Acute hepatitis", "Ulcerative colitis", "Barrett esophagus"], "Ductal stones and calcification are typical of chronic pancreatitis."),
        q("moderate", "Pain in chronic pancreatitis often radiates to the:", "Back", ["Left arm only", "Groin only", "Jaw only"], "Retroperitoneal pancreatic inflammation commonly causes back pain."),
        q("moderate", "Hereditary pancreatitis can involve gain-of-function mutation in:", "PRSS1", ["HBB", "APC", "PIGA"], "PRSS1 mutations promote trypsin activity."),
        q("moderate", "Late chronic pancreatitis can cause diabetes by destruction of:", "Islets", ["Goblet cells", "Parietal cells", "Kupffer cells"], "Progressive fibrosis may involve endocrine tissue."),
        q("high", "A patient with years of alcohol use has recurrent epigastric pain, pancreatic calcifications, steatorrhea, and biopsy showing fibrosis with acinar loss and chronic inflammation. Which diagnosis is most likely?", "Chronic pancreatitis", ["Acute edematous pancreatitis", "Serous cystadenoma", "Autoimmune hepatitis"], "Chronic pancreatitis causes irreversible fibrosis and exocrine insufficiency."),
        q("high", "A child from a family with recurrent pancreatitis has attacks due to a mutation that makes trypsin resistant to inactivation. Which gene is classically implicated?", "PRSS1", ["BRCA2", "VHL", "SMAD4"], "PRSS1 mutations cause hereditary pancreatitis by increasing trypsin activity."),
        q("high", "A patient with chronic pancreatic fibrosis develops bulky greasy stools and weight loss because digestive enzymes no longer reach the duodenum. Which enzyme deficiency most directly causes fat malabsorption?", "Pancreatic lipase deficiency", ["Lactase excess", "Pepsin excess", "Salivary amylase excess"], "Loss of pancreatic lipase causes steatorrhea."),
    ]),
    ("autoimmune-hereditary", "Autoimmune, Hereditary, and Systemic Pancreatic Disorders", [
        q("easy", "Autoimmune pancreatitis is often associated with elevated:", "IgG4", ["IgE only", "Factor VIII", "Troponin"], "Many cases belong to IgG4-related disease."),
        q("easy", "Autoimmune pancreatitis can mimic:", "Pancreatic carcinoma", ["Acute appendicitis only", "Asthma", "Hemophilia"], "A mass-like pancreatic lesion may resemble cancer."),
        q("easy", "Hereditary pancreatitis increases risk of:", "Pancreatic carcinoma", ["Thyroiditis only", "Sickle crisis", "Celiac disease"], "Long-standing hereditary pancreatitis raises cancer risk."),
        q("moderate", "IgG4-related pancreatitis often shows:", "Storiform fibrosis and lymphoplasmacytic inflammation", ["Caseating granulomas only", "Reed-Sternberg cells", "Auer rods"], "IgG4 disease causes lymphoplasmacytic inflammation and fibrosis."),
        q("moderate", "Autoimmune pancreatitis typically responds to:", "Glucocorticoids", ["Anticoagulation only", "Appendectomy", "Iron chelation"], "Steroids often improve IgG4-related pancreatic disease."),
        q("moderate", "CFTR mutations can predispose to pancreatitis by causing:", "Abnormal ductal secretion", ["Excess bile salts", "Loss of platelets", "Portal vein dilation"], "Viscous secretions and duct dysfunction promote pancreatic injury."),
        q("moderate", "SPINK1 mutations predispose to pancreatitis by affecting:", "Trypsin inhibition", ["Insulin receptor signaling", "Bile acid synthesis", "Hemoglobin oxygen affinity"], "SPINK1 normally inhibits prematurely activated trypsin."),
        q("high", "A patient has painless jaundice and a pancreatic head mass, but biopsy shows IgG4-positive plasma cells, storiform fibrosis, and obliterative phlebitis. Which diagnosis should be considered?", "Autoimmune pancreatitis", ["Ductal adenocarcinoma only", "Serous cystadenoma", "Acute hemorrhagic pancreatitis"], "Autoimmune pancreatitis can mimic a mass and is IgG4-related."),
        q("high", "A patient with recurrent pancreatitis has a germline defect in a pancreatic secretory trypsin inhibitor, allowing prematurely activated trypsin to persist. Which gene is involved?", "SPINK1", ["RB1", "HFE", "MLH1"], "SPINK1 encodes a trypsin inhibitor that limits enzyme activation."),
        q("high", "A patient with suspected autoimmune pancreatitis improves rapidly after steroids, and imaging shows reduction of a diffuse sausage-shaped pancreas. Which immune-mediated disease category is most likely?", "IgG4-related disease", ["Type I hypersensitivity only", "Immune thrombocytopenia", "Celiac sprue"], "Autoimmune pancreatitis is a manifestation of IgG4-related disease."),
    ]),
    ("ductal-adenocarcinoma", "Pancreatic Ductal Adenocarcinoma: Risks and Morphology", [
        q("easy", "The most common malignant tumor of the pancreas is:", "Ductal adenocarcinoma", ["Insulinoma", "Serous cystadenoma", "Solid pseudopapillary tumor"], "Most pancreatic cancers are invasive ductal adenocarcinomas."),
        q("easy", "Pancreatic cancer most often arises in the:", "Head of pancreas", ["Tail only", "Spleen", "Gallbladder fundus"], "Many pancreatic ductal adenocarcinomas arise in the head."),
        q("easy", "A major risk factor for pancreatic carcinoma is:", "Cigarette smoking", ["Gluten avoidance", "Low altitude", "Vitamin C intake"], "Smoking is an important modifiable risk factor."),
        q("moderate", "Pancreatic head carcinoma commonly causes:", "Painless obstructive jaundice", ["Hemarthrosis", "Pneumothorax", "Nephrotic syndrome"], "Tumors in the head can obstruct the common bile duct."),
        q("moderate", "The most frequent early driver mutation in pancreatic ductal adenocarcinoma is:", "KRAS", ["HBB", "PIGA", "RET only"], "KRAS activation is common and early."),
        q("moderate", "PanIN means:", "Pancreatic intraepithelial neoplasia", ["Pancreatic infectious necrosis", "Portal inflammation node", "Parietal intestinal neoplasm"], "PanIN lesions are ductal precursor lesions."),
        q("moderate", "Pancreatic ductal adenocarcinoma typically produces a:", "Desmoplastic stroma", ["Pure cyst without stroma", "Lymphoid follicle", "Hemangioma"], "Dense desmoplasia is a classic histologic feature."),
        q("high", "An older smoker develops painless jaundice, weight loss, and a hard irregular pancreatic head mass that encases nearby vessels. Histology shows infiltrating glands in dense desmoplastic stroma. Which tumor is most likely?", "Pancreatic ductal adenocarcinoma", ["Serous cystadenoma", "Insulinoma", "Solid pseudopapillary neoplasm"], "Ductal adenocarcinoma commonly presents as an infiltrative desmoplastic mass."),
        q("high", "A pancreatic cancer progresses through microscopic ductal precursor lesions with increasing dysplasia, KRAS activation, and later loss of tumor suppressor pathways. What precursor lesion is described?", "PanIN", ["IPMN only", "MCN only", "Pseudocyst"], "PanIN is a noninvasive ductal precursor of ductal adenocarcinoma."),
        q("high", "A patient with pancreatic body carcinoma develops recurrent migratory thrombophlebitis in superficial veins before the abdominal mass is clinically obvious. Which paraneoplastic phenomenon is this?", "Trousseau syndrome", ["Cullen sign", "Courvoisier sign", "Zollinger-Ellison syndrome"], "Pancreatic adenocarcinoma can cause migratory thrombophlebitis."),
    ]),
    ("clinical-spread", "Pancreatic Cancer Clinical Features, Spread, and Prognosis", [
        q("easy", "Courvoisier sign is a palpable gallbladder with:", "Painless jaundice", ["Hemolysis only", "Acute appendicitis", "Pneumonia"], "Malignant distal bile duct obstruction can distend the gallbladder."),
        q("easy", "Pancreatic adenocarcinoma has a generally:", "Poor prognosis", ["Uniformly benign course", "No metastatic potential", "Spontaneous cure rate"], "It is often detected late and behaves aggressively."),
        q("easy", "Pancreatic cancer commonly spreads by:", "Perineural invasion", ["Only hematoma formation", "Airway aspiration", "Bone marrow suppression"], "Perineural invasion contributes to pain and spread."),
        q("moderate", "Carcinoma in the pancreatic tail often presents late because it:", "Does not obstruct the bile duct early", ["Always secretes insulin", "Causes early hematuria", "Cannot metastasize"], "Tail tumors may grow silently before symptoms."),
        q("moderate", "Elevated CA 19-9 in pancreatic cancer is mainly useful for:", "Monitoring disease course", ["Population screening", "Confirming all benign cysts", "Replacing biopsy"], "CA 19-9 is not adequate as a general screening test."),
        q("moderate", "Pancreatic cancer commonly metastasizes to the:", "Liver", ["Thymus only", "Appendix only", "Skin epidermis only"], "Portal drainage facilitates liver metastasis."),
        q("moderate", "Pain from pancreatic carcinoma often radiates to the back due to:", "Retroperitoneal invasion", ["Pleural effusion only", "Esophageal spasm", "Renal stones"], "Pancreatic tumors can invade retroperitoneal nerves."),
        q("high", "A patient has painless progressive jaundice, weight loss, a palpable nontender gallbladder, and imaging showing obstruction near the ampulla by a pancreatic head mass. What sign is present?", "Courvoisier sign", ["Cullen sign", "Grey Turner sign", "Murphy sign"], "A distended gallbladder with painless jaundice suggests malignant obstruction."),
        q("high", "A pancreatic tail carcinoma grows silently until the patient develops weight loss, deep epigastric pain radiating to the back, and liver metastases. Why was jaundice absent initially?", "The common bile duct was not obstructed early", ["The tumor secreted glucagon", "Bile production stopped completely", "The gallbladder was absent congenitally"], "Tail lesions are distant from the distal common bile duct."),
        q("high", "A patient with pancreatic adenocarcinoma develops severe back pain, and histology shows malignant glands tracking along nerves within dense desmoplastic tissue. Which route of local spread is emphasized?", "Perineural invasion", ["Transcoelomic spread only", "Airborne spread", "Lymphocytic emperipolesis"], "Perineural invasion is common in pancreatic ductal carcinoma."),
    ]),
    ("cystic-neoplasms", "Cystic Neoplasms of the Pancreas", [
        q("easy", "A pancreatic pseudocyst differs from cystic neoplasm because it lacks:", "Epithelial lining", ["Fluid", "Fibrous tissue", "Inflammation"], "Pseudocysts are not true epithelial cysts."),
        q("easy", "Serous cystadenoma of pancreas is usually:", "Benign", ["Highly metastatic", "A type of lymphoma", "Always endocrine"], "Serous cystadenomas are generally benign."),
        q("easy", "Mucinous cystic neoplasm occurs most often in:", "Women", ["Newborn boys only", "Elderly men only", "All patients with CF"], "MCNs are classically seen in women."),
        q("moderate", "Serous cystadenoma is associated with mutation or syndrome involving:", "VHL", ["HBB", "PIGA", "BCR-ABL"], "VHL alterations are linked to serous cystadenoma."),
        q("moderate", "Mucinous cystic neoplasm characteristically has:", "Ovarian-type stroma", ["Neutrophils in muscularis", "Reed-Sternberg cells", "Auer rods"], "Ovarian-type stroma helps define MCN."),
        q("moderate", "Intraductal papillary mucinous neoplasm arises in:", "Pancreatic ducts", ["Islet beta cells", "Peripancreatic fat only", "Splenic capsule"], "IPMN is an intraductal mucin-producing neoplasm."),
        q("moderate", "IPMN often causes duct dilation due to production of:", "Mucin", ["Insulin", "Bile salts", "Amyloid"], "Mucin secretion can distend pancreatic ducts."),
        q("high", "A woman has a solitary cystic lesion in the pancreatic tail with mucin-producing epithelium and dense ovarian-type stroma, without communication with the duct system. Which neoplasm is most likely?", "Mucinous cystic neoplasm", ["Serous cystadenoma", "Pseudocyst", "Pancreatic neuroendocrine tumor"], "MCN typically occurs in women and has ovarian-type stroma."),
        q("high", "An older patient has a cystic pancreatic head lesion communicating with the main pancreatic duct, with papillary mucinous epithelium and abundant mucin causing duct dilation. Which lesion is this?", "Intraductal papillary mucinous neoplasm", ["Mucinous cystic neoplasm", "Serous cystadenoma", "Lymphangioma"], "IPMN is an intraductal mucin-producing precursor."),
        q("high", "A microcystic pancreatic lesion has glycogen-rich clear cuboidal epithelium and a central scar. It is linked to VHL alterations and is usually benign. Which tumor is likely?", "Serous cystadenoma", ["Ductal adenocarcinoma", "Mucinous cystic neoplasm", "Pseudocyst"], "Serous cystadenoma is a benign microcystic VHL-associated tumor."),
    ]),
    ("neuroendocrine", "Pancreatic Neuroendocrine Tumors", [
        q("easy", "Pancreatic neuroendocrine tumors arise from:", "Islet endocrine cells", ["Acinar digestive cells only", "Bile duct epithelium", "Kupffer cells"], "PanNETs show endocrine differentiation."),
        q("easy", "An insulinoma commonly causes:", "Hypoglycemia", ["Hypercalcemia only", "Jaundice always", "Hematuria"], "Insulin secretion lowers blood glucose."),
        q("easy", "Gastrinoma causes increased:", "Gastric acid secretion", ["Bile salt synthesis", "Red cell mass", "Platelet count"], "Gastrin stimulates acid production."),
        q("moderate", "Pancreatic neuroendocrine tumors may be associated with:", "MEN1", ["Down syndrome only", "Turner syndrome only", "Marfan syndrome only"], "MEN1 predisposes to pancreatic endocrine tumors."),
        q("moderate", "Glucagonoma is associated with:", "Necrolytic migratory erythema", ["Cherry-red spot", "Kayser-Fleischer rings", "Cullen sign"], "Glucagonoma causes diabetes, anemia, and a characteristic rash."),
        q("moderate", "VIPoma classically causes:", "Watery diarrhea, hypokalemia, and achlorhydria", ["Constipation and miosis", "Hemarthrosis", "Pancytopenia"], "VIP excess causes WDHA syndrome."),
        q("moderate", "Neuroendocrine tumors often stain for:", "Chromogranin and synaptophysin", ["Desmin only", "GFAP only", "Myeloperoxidase only"], "These markers support neuroendocrine differentiation."),
        q("high", "A patient has fasting confusion, sweating, low plasma glucose, high insulin, and symptoms relieved by glucose. A small pancreatic neuroendocrine tumor is found. Which tumor is most likely?", "Insulinoma", ["Gastrinoma", "Glucagonoma", "VIPoma"], "Insulinoma causes Whipple triad from inappropriate insulin secretion."),
        q("high", "A patient has recurrent severe peptic ulcers, diarrhea, and markedly increased gastric acid secretion from a pancreatic or duodenal neuroendocrine tumor. Which syndrome is present?", "Zollinger-Ellison syndrome", ["Carcinoid syndrome", "MEN2B", "Verner-Morrison syndrome"], "Gastrinoma causes Zollinger-Ellison syndrome."),
        q("high", "A patient has diabetes, weight loss, anemia, and a blistering erythematous rash that migrates around the groin and lower abdomen. Which pancreatic endocrine tumor is suggested?", "Glucagonoma", ["Insulinoma", "Somatostatinoma", "Serous cystadenoma"], "Glucagonoma causes necrolytic migratory erythema and diabetes."),
    ]),
    ("acinar-pancreatoblastoma", "Acinar Cell Carcinoma, Pancreatoblastoma, and Rare Tumors", [
        q("easy", "Acinar cell carcinoma shows differentiation toward:", "Enzyme-producing acinar cells", ["Beta cells only", "Bile duct epithelium", "Squamous epithelium"], "Acinar tumors produce digestive enzyme-related proteins."),
        q("easy", "Pancreatoblastoma is primarily a tumor of:", "Children", ["Elderly smokers only", "Pregnant women only", "Patients with cirrhosis"], "Pancreatoblastoma is a childhood pancreatic malignancy."),
        q("easy", "Solid pseudopapillary neoplasm most often affects:", "Young women", ["Newborn boys", "Elderly men with COPD", "Patients with hemophilia"], "It classically occurs in young women."),
        q("moderate", "Acinar cell carcinoma may produce excessive:", "Lipase", ["Intrinsic factor", "Ceruloplasmin", "Calcitonin"], "Some acinar tumors cause lipase hypersecretion syndrome."),
        q("moderate", "Lipase hypersecretion syndrome may cause:", "Subcutaneous fat necrosis", ["Megaloblastic anemia", "Hemarthrosis", "Pulmonary embolus only"], "Circulating lipase can injure fat tissue."),
        q("moderate", "Solid pseudopapillary neoplasm commonly has mutation in:", "Beta-catenin pathway", ["BCR-ABL", "HFE", "CFTR only"], "CTNNB1 mutations activate beta-catenin signaling."),
        q("moderate", "Pancreatoblastoma may show:", "Squamoid nests", ["Auer rods", "Reed-Sternberg cells", "Psammoma bodies only"], "Squamoid corpuscles are characteristic."),
        q("high", "A child has a malignant pancreatic mass with acinar differentiation and squamoid nests on microscopy. The tumor marker alpha-fetoprotein may be elevated. Which tumor is most likely?", "Pancreatoblastoma", ["Ductal adenocarcinoma", "Serous cystadenoma", "Insulinoma"], "Pancreatoblastoma is a pediatric pancreatic tumor with squamoid nests."),
        q("high", "A patient with pancreatic acinar cell carcinoma develops painful subcutaneous nodules, fever, and polyarthralgia from circulating digestive enzymes. Which paraneoplastic mechanism explains these findings?", "Lipase-mediated fat necrosis", ["Insulin-mediated hypoglycemia", "Gastrin-mediated ulceration", "VIP-mediated achlorhydria"], "Excess lipase can cause fat necrosis and joint symptoms."),
        q("high", "A young woman has a large well-circumscribed pancreatic mass with solid and pseudopapillary areas, hemorrhage, and nuclear beta-catenin staining. Which neoplasm is most likely?", "Solid pseudopapillary neoplasm", ["Pancreatic ductal adenocarcinoma", "Mucinous cystic neoplasm", "Pancreatic pseudocyst"], "Solid pseudopapillary neoplasm affects young women and activates beta-catenin."),
    ]),
    ("diabetes-islets", "Diabetes Mellitus and Islet Pathology", [
        q("easy", "Type 1 diabetes mellitus is caused by destruction of:", "Beta cells", ["Acinar cells", "Kupffer cells", "Parietal cells"], "Autoimmune beta-cell loss causes absolute insulin deficiency."),
        q("easy", "Type 2 diabetes is strongly associated with:", "Insulin resistance", ["CFTR mutation only", "HBV infection", "Portal hypertension"], "Peripheral insulin resistance is central to type 2 diabetes."),
        q("easy", "Diabetic ketoacidosis is most typical of:", "Type 1 diabetes", ["Serous cystadenoma", "VIPoma", "Chronic cholecystitis"], "Absolute insulin deficiency promotes ketoacidosis."),
        q("moderate", "Islet amyloid in type 2 diabetes is derived from:", "Amylin", ["Insulin receptor", "Glucagon only", "Trypsin"], "Amylin is co-secreted with insulin by beta cells."),
        q("moderate", "Insulitis is most characteristic of:", "Type 1 diabetes", ["Type 2 diabetes only", "Pancreatic pseudocyst", "Serous cystadenoma"], "Autoimmune inflammation targets islets in type 1 diabetes."),
        q("moderate", "Long-standing diabetes causes microvascular disease through:", "Advanced glycation end products", ["Bile duct obstruction", "Trypsin inhibition", "Goblet cell metaplasia"], "AGEs injure vessels and basement membranes."),
        q("moderate", "A major chronic complication of diabetes is:", "Diabetic nephropathy", ["Achalasia", "Appendicitis", "Hemophilia"], "Kidney disease is a common microvascular complication."),
        q("high", "A child develops polyuria, weight loss, ketoacidosis, and pancreatic islets infiltrated by lymphocytes with marked beta-cell depletion on microscopy. Which disease mechanism is most likely?", "Autoimmune T-cell-mediated beta-cell destruction", ["Insulin receptor mutation in all tissues", "Ductal mucin obstruction", "Gastrin hypersecretion"], "Type 1 diabetes is autoimmune beta-cell destruction."),
        q("high", "An obese adult with hyperglycemia has enlarged islets early, followed later by beta-cell dysfunction and extracellular eosinophilic islet deposits derived from amylin. Which diabetes type is favored?", "Type 2 diabetes mellitus", ["Type 1 diabetes mellitus", "MODY from glucokinase only", "Cystic fibrosis pancreatitis"], "Type 2 diabetes involves insulin resistance and islet amyloid."),
        q("high", "A patient with long-standing diabetes develops nodular glomerulosclerosis, retinal microaneurysms, peripheral neuropathy, and accelerated atherosclerosis. Which biochemical process contributes broadly to these chronic complications?", "Nonenzymatic glycation of proteins", ["Trypsinogen activation", "Bilirubin deconjugation", "Copper retention"], "AGE formation drives diabetic vascular and matrix injury."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch19-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 19 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch19-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 19 questions")
    print(f"Removed {total_removed} existing Chapter 19 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 19 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
