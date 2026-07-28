import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Liver and Gallbladder"
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
    ("injury-jaundice", "Liver Injury Patterns, Jaundice, and Cholestasis", [
        q("easy", "The main parenchymal cell of the liver is the:", "Hepatocyte", ["Kupffer platelet", "Pneumocyte", "Osteoclast"], "Hepatocytes perform most liver metabolic and synthetic functions."),
        q("easy", "Jaundice means visible tissue accumulation of:", "Bilirubin", ["Urea", "Amylase", "Ferritin"], "Yellow discoloration is caused by increased bilirubin."),
        q("easy", "Cholestasis refers to impaired flow of:", "Bile", ["Lymph", "Cerebrospinal fluid", "Synovial fluid"], "Cholestasis is reduced bile formation or flow."),
        q("moderate", "Canalicular bile plugs are most typical of:", "Cholestatic liver injury", ["Pure steatosis only", "Amyloidosis", "Hemangioma"], "Bile plugs reflect retention of bile within canaliculi."),
        q("moderate", "Councilman bodies in acute viral hepatitis represent:", "Apoptotic hepatocytes", ["Fibrotic septa", "Bile duct hamartomas", "Mallory bodies"], "Scattered apoptotic hepatocytes are acidophil bodies."),
        q("moderate", "Bridging necrosis connects portal tracts or central veins and indicates:", "Severe hepatic injury", ["Normal regeneration", "Simple congestion only", "Gallstone ileus"], "Confluent necrosis spanning vascular structures is serious."),
        q("moderate", "Conjugated hyperbilirubinemia with pale stools and dark urine suggests:", "Obstructive cholestasis", ["Gilbert syndrome only", "Hemolysis only", "Iron deficiency"], "Conjugated bilirubin enters urine while bile pigment fails to reach stool."),
        q("high", "A patient has pruritus, dark urine, pale stools, and elevated alkaline phosphatase out of proportion to aminotransferases. Which broad pattern of liver injury best explains these findings?", "Cholestatic injury", ["Pure hepatocellular necrosis", "Hemolytic anemia only", "Portal vein thrombosis only"], "Disproportionate alkaline phosphatase elevation with retained conjugated bilirubin suggests cholestasis."),
        q("high", "A liver biopsy from acute hepatitis shows lobular disarray, lymphocytes, ballooning degeneration, and scattered round intensely eosinophilic hepatocytes. What are these shrunken eosinophilic cells?", "Apoptotic acidophil bodies", ["Regenerative nodules", "Bile duct adenomas", "Kupffer cell granulomas"], "Acidophil bodies are apoptotic hepatocytes in acute hepatitis."),
        q("high", "A patient develops rapidly progressive hepatic dysfunction after massive hepatic necrosis. Histology shows collapse of reticulin framework with loss of hepatocytes across broad zones. Which injury pattern is present?", "Massive hepatic necrosis", ["Simple fatty change", "Focal nodular hyperplasia", "Biliary hamartoma"], "Massive hepatic necrosis can cause fulminant hepatic failure."),
    ]),
    ("viral-hepatitis", "Viral Hepatitis: Acute, Chronic, and Fulminant", [
        q("easy", "Hepatitis A virus is transmitted mainly by:", "Fecal-oral route", ["Blood transfusion only", "Mosquito bite", "Respiratory droplets"], "HAV spreads through contaminated food or water."),
        q("easy", "Hepatitis B virus is a:", "DNA virus", ["RNA prion", "Fungus", "Helminth"], "HBV is an enveloped partially double-stranded DNA virus."),
        q("easy", "Hepatitis C virus commonly causes:", "Chronic hepatitis", ["Acute appendicitis", "Celiac disease", "Pneumoconiosis"], "HCV has a high rate of chronic infection."),
        q("moderate", "HDV infection requires coinfection with:", "HBV", ["HAV", "HEV", "EBV only"], "Delta virus needs hepatitis B surface antigen."),
        q("moderate", "HEV is especially dangerous in:", "Pregnant women", ["Infants with pyloric stenosis", "Patients with asthma only", "People with achalasia"], "HEV can cause severe disease in pregnancy."),
        q("moderate", "Ground-glass hepatocytes are classically associated with:", "Chronic hepatitis B", ["Hepatitis A", "Gilbert syndrome", "Hemochromatosis only"], "HBsAg accumulation gives hepatocytes a ground-glass appearance."),
        q("moderate", "Interface hepatitis means inflammation at the:", "Portal-parenchymal interface", ["Gallbladder fundus only", "Central nervous system", "Splenic red pulp"], "Chronic hepatitis often damages limiting plate hepatocytes."),
        q("high", "A patient develops jaundice after eating contaminated shellfish and recovers completely without chronic carriage. Serology shows IgM antibody to the responsible virus. Which hepatitis virus is most likely?", "Hepatitis A virus", ["Hepatitis B virus", "Hepatitis C virus", "Hepatitis D virus"], "HAV causes acute self-limited fecal-oral hepatitis."),
        q("high", "A person with chronic hepatitis B has superimposed infection by a defective RNA virus using hepatitis B surface antigen for its envelope. Which agent has caused the superinfection?", "Hepatitis D virus", ["Hepatitis A virus", "Hepatitis E virus", "Epstein-Barr virus"], "HDV depends on HBV for HBsAg."),
        q("high", "A patient with a remote history of injection drug use has chronic hepatitis, fluctuating aminotransferases, and increased risk of cirrhosis and hepatocellular carcinoma. Which virus is most likely?", "Hepatitis C virus", ["Hepatitis A virus", "Rotavirus", "Norovirus"], "HCV commonly becomes chronic after parenteral exposure."),
    ]),
    ("fatty-liver", "Alcoholic and Metabolic Fatty Liver Disease", [
        q("easy", "Fatty change in hepatocytes is called:", "Steatosis", ["Cholangiocarcinoma", "Amyloidosis", "Hemangioma"], "Steatosis is abnormal triglyceride accumulation in hepatocytes."),
        q("easy", "Mallory-Denk bodies are associated with:", "Alcoholic hepatitis", ["Wilson disease only", "HAV infection only", "Portal vein thrombosis"], "Mallory-Denk bodies are damaged keratin aggregates in ballooned hepatocytes."),
        q("easy", "Nonalcoholic fatty liver disease is linked to:", "Metabolic syndrome", ["Factor VIII deficiency", "Asthma", "Achalasia"], "Obesity and insulin resistance are major associations."),
        q("moderate", "Alcoholic hepatitis classically shows:", "Ballooned hepatocytes, neutrophils, and Mallory-Denk bodies", ["Caseating granulomas only", "Reed-Sternberg cells", "Auer rods"], "Alcoholic steatohepatitis has ballooning injury and neutrophils."),
        q("moderate", "The earliest reversible lesion in alcoholic liver disease is:", "Hepatic steatosis", ["Macronodular cirrhosis always", "Cholangiocarcinoma", "Budd-Chiari syndrome"], "Fatty liver can regress with abstinence."),
        q("moderate", "Steatohepatitis differs from bland steatosis by presence of:", "Hepatocyte injury and inflammation", ["Normal histology", "Only gallstones", "Only splenic congestion"], "Steatohepatitis includes ballooning degeneration and inflammatory injury."),
        q("moderate", "Pericellular chicken-wire fibrosis is typical of:", "Steatohepatitis", ["Acute appendicitis", "Celiac disease", "Barrett esophagus"], "Sinusoidal fibrosis around hepatocytes is characteristic."),
        q("high", "An obese patient with diabetes has elevated aminotransferases. Liver biopsy shows macrovesicular steatosis, ballooned hepatocytes, lobular inflammation, and pericellular fibrosis despite no alcohol use. Which diagnosis fits?", "Nonalcoholic steatohepatitis", ["Autoimmune hepatitis", "Primary biliary cholangitis", "Acute hepatitis A"], "NASH is metabolic steatohepatitis with hepatocyte injury."),
        q("high", "A patient with heavy alcohol use develops fever, jaundice, tender hepatomegaly, neutrophilic lobular inflammation, and eosinophilic cytoplasmic inclusions in ballooned hepatocytes. What are these inclusions?", "Mallory-Denk bodies", ["Councilman bodies", "Ground-glass inclusions", "Psammoma bodies"], "Mallory-Denk bodies are keratin aggregates in alcoholic hepatitis."),
        q("high", "After years of recurrent steatohepatitis, a patient develops portal hypertension and a nodular fibrotic liver. Which pathway best explains the progression from fatty injury to this end stage?", "Activation of stellate cells with collagen deposition", ["Loss of intrinsic factor", "Auer rod formation", "Goblet cell metaplasia"], "Chronic hepatocyte injury activates stellate cells and fibrosis."),
    ]),
    ("cirrhosis-failure", "Cirrhosis, Portal Hypertension, and Hepatic Failure", [
        q("easy", "Cirrhosis is defined by fibrosis plus:", "Regenerative nodules", ["Only steatosis", "Only jaundice", "Only gallstones"], "Cirrhosis requires diffuse fibrosis and nodular regeneration."),
        q("easy", "Portal hypertension commonly causes:", "Esophageal varices", ["Pyloric stenosis", "Achalasia", "Pneumothorax"], "High portal pressure drives portosystemic collateral veins."),
        q("easy", "Ascites is accumulation of fluid in the:", "Peritoneal cavity", ["Pleural alveoli", "Bone marrow", "Renal pelvis"], "Ascites is free peritoneal fluid."),
        q("moderate", "Hepatic encephalopathy is associated with increased:", "Ammonia", ["Hemoglobin A", "Factor VIII only", "Gastric acid"], "Reduced detoxification allows neurotoxic ammonia accumulation."),
        q("moderate", "Caput medusae results from dilation of:", "Paraumbilical collateral veins", ["Pulmonary veins", "Coronary arteries", "Cystic duct"], "Portal hypertension opens paraumbilical venous collaterals."),
        q("moderate", "Splenomegaly in cirrhosis is due to:", "Congestive portal hypertension", ["Sickle cell autosplenectomy", "Acute cholecystitis", "Celiac sprue"], "Portal venous congestion enlarges the spleen."),
        q("moderate", "Spider angiomas in chronic liver disease reflect:", "Hyperestrogenemia", ["Vitamin C excess", "Low insulin only", "Iron deficiency"], "Impaired estrogen metabolism contributes to vascular changes."),
        q("high", "A patient with long-standing cirrhosis develops hematemesis from dilated veins at the distal esophagus after portal pressure rises markedly. Which vascular adaptation created the bleeding vessels?", "Portosystemic collateral formation", ["Arterial aneurysm rupture", "Ductus arteriosus reopening", "Pulmonary venous shunting"], "Portal hypertension enlarges collateral veins at the gastroesophageal junction."),
        q("high", "A patient with end-stage liver disease becomes confused and asterixis is noted. Laboratory studies show impaired hepatic detoxification and elevated nitrogenous metabolites. Which complication is most likely?", "Hepatic encephalopathy", ["Wernicke encephalopathy only", "Subarachnoid hemorrhage", "Myasthenic crisis"], "Hepatic failure can cause encephalopathy from ammonia and related toxins."),
        q("high", "A cirrhotic liver contains diffuse fibrous septa surrounding nodules of regenerating hepatocytes, distorting vascular flow between portal tracts and central veins. Which diagnosis is established?", "Cirrhosis", ["Acute passive congestion", "Hepatic adenoma", "Simple steatosis"], "Cirrhosis is diffuse nodular regeneration with bridging fibrosis."),
    ]),
    ("autoimmune-cholestatic", "Autoimmune and Cholestatic Liver Diseases", [
        q("easy", "Autoimmune hepatitis often has antibodies against:", "Smooth muscle", ["Factor VIII", "Gliadin only", "Acetylcholine receptor only"], "Anti-smooth muscle antibodies are a common marker."),
        q("easy", "Primary biliary cholangitis mainly destroys:", "Small intrahepatic bile ducts", ["Large bronchi", "Renal glomeruli", "Splenic follicles"], "PBC is chronic nonsuppurative destruction of small ducts."),
        q("easy", "Primary sclerosing cholangitis is strongly associated with:", "Ulcerative colitis", ["Asthma", "Achalasia", "Hemophilia A"], "PSC commonly occurs in patients with ulcerative colitis."),
        q("moderate", "Antimitochondrial antibodies are characteristic of:", "Primary biliary cholangitis", ["Autoimmune gastritis", "Wilson disease", "Alcoholic hepatitis"], "AMA is the classic serologic marker of PBC."),
        q("moderate", "PSC produces a cholangiographic pattern described as:", "Beading of bile ducts", ["Bird-beak esophagus", "Soap-bubble bone", "Apple-core stomach"], "Alternating strictures and dilation create beading."),
        q("moderate", "Autoimmune hepatitis histology often shows:", "Interface hepatitis rich in plasma cells", ["Pure sinusoidal congestion", "Only cholesterol stones", "Auer rods"], "Plasma cell-rich interface hepatitis supports autoimmune hepatitis."),
        q("moderate", "A late complication of chronic cholestatic disease is:", "Biliary-type cirrhosis", ["Pyloric stenosis", "Teratoma", "Pneumoconiosis"], "Persistent bile duct injury can progress to cirrhosis."),
        q("high", "A middle-aged woman has pruritus, fatigue, elevated alkaline phosphatase, antimitochondrial antibodies, and biopsy showing florid duct lesions of small intrahepatic bile ducts. Which diagnosis is most likely?", "Primary biliary cholangitis", ["Primary sclerosing cholangitis", "Autoimmune hepatitis", "Acute hepatitis A"], "PBC causes autoimmune destruction of small intrahepatic bile ducts."),
        q("high", "A man with ulcerative colitis has cholestatic enzymes and imaging showing multifocal strictures alternating with dilated segments of intrahepatic and extrahepatic bile ducts. Which disease is present?", "Primary sclerosing cholangitis", ["Primary biliary cholangitis", "Hemochromatosis", "Gilbert syndrome"], "PSC is associated with UC and beaded bile ducts."),
        q("high", "A young woman has hypergammaglobulinemia, anti-smooth muscle antibodies, and liver biopsy showing plasma cell-rich inflammation crossing the limiting plate. Which treatment-responsive disorder is suggested?", "Autoimmune hepatitis", ["Alcoholic fatty liver", "Budd-Chiari syndrome", "Cholelithiasis"], "Autoimmune hepatitis has immune-mediated interface activity and responds to immunosuppression."),
    ]),
    ("genetic-metabolic", "Genetic and Metabolic Liver Diseases", [
        q("easy", "Hemochromatosis is excessive accumulation of:", "Iron", ["Copper only", "Bilirubin only", "Glycogen only"], "Hereditary hemochromatosis causes iron overload."),
        q("easy", "Wilson disease involves accumulation of:", "Copper", ["Calcium", "Lead only", "Cholesterol stones"], "ATP7B mutation impairs copper excretion."),
        q("easy", "Alpha-1 antitrypsin deficiency can cause:", "Liver disease and emphysema", ["Only colon cancer", "Hemophilia", "Celiac sprue"], "Misfolded AAT injures liver; deficiency injures lung."),
        q("moderate", "Hereditary hemochromatosis is most often due to mutation in:", "HFE", ["HBB", "APC", "KIT"], "HFE mutation increases intestinal iron absorption."),
        q("moderate", "Prussian blue stain highlights:", "Iron deposits", ["Copper deposits", "Bile canaliculi", "Amyloid only"], "Iron stores are demonstrated by Prussian blue."),
        q("moderate", "Wilson disease typically has low serum:", "Ceruloplasmin", ["Ferritin always", "Albumin only", "Alkaline phosphatase only"], "Ceruloplasmin is often reduced in Wilson disease."),
        q("moderate", "Alpha-1 antitrypsin deficiency shows PAS-positive globules in:", "Hepatocytes", ["Neutrophils only", "Thyroid follicles", "Colon crypts"], "Misfolded AAT accumulates in hepatocyte endoplasmic reticulum."),
        q("high", "A young patient has chronic liver disease, neuropsychiatric symptoms, Kayser-Fleischer rings on eye examination, and low ceruloplasmin. Which inherited defect best explains these findings?", "ATP7B mutation causing impaired copper excretion", ["HFE mutation causing iron absorption", "APC mutation causing adenomas", "CFTR mutation causing thick mucus"], "Wilson disease is due to defective biliary copper excretion."),
        q("high", "An adult has cirrhosis, diabetes, skin hyperpigmentation, cardiomyopathy, arthropathy, and markedly increased transferrin saturation with high serum ferritin. Which storage disorder is most likely?", "Hereditary hemochromatosis", ["Wilson disease", "Alpha-1 antitrypsin deficiency", "Gaucher disease"], "Iron overload damages liver, pancreas, skin, and heart."),
        q("high", "A patient with early emphysema develops liver biopsy findings of round eosinophilic PAS-positive diastase-resistant globules within hepatocytes. Which protein is retained in the liver?", "Misfolded alpha-1 antitrypsin", ["Albumin", "Hemoglobin S", "Factor VIII"], "Mutant AAT accumulates in hepatocytes and reduces antiprotease activity in lung."),
    ]),
    ("drug-toxic", "Drug-Induced and Toxic Liver Injury", [
        q("easy", "Acetaminophen overdose causes severe:", "Centrilobular hepatic necrosis", ["Pancreatic islet hyperplasia", "Splenic infarction only", "Appendicitis"], "Toxic metabolites injure zone 3 hepatocytes."),
        q("easy", "The antidote for acetaminophen toxicity is:", "N-acetylcysteine", ["Warfarin", "Imatinib", "Omeprazole"], "N-acetylcysteine restores glutathione stores."),
        q("easy", "Aflatoxin exposure increases risk of:", "Hepatocellular carcinoma", ["Follicular lymphoma", "Melanoma only", "Osteosarcoma"], "Aflatoxin is a potent hepatocarcinogen."),
        q("moderate", "Carbon tetrachloride injury mainly begins in zone:", "3 near central veins", ["1 near portal tracts only", "Bile ducts only", "Gallbladder mucosa"], "Zone 3 has abundant CYP activity and lower oxygen."),
        q("moderate", "Acetaminophen toxicity is worsened by depleted:", "Glutathione", ["Intrinsic factor", "Factor VIII", "Secretin"], "Glutathione detoxifies NAPQI."),
        q("moderate", "Halothane-type injury is best categorized as:", "Idiosyncratic drug reaction", ["Congenital malformation", "Pure ischemia", "Gallstone obstruction"], "Some drug injuries are unpredictable immune-mediated reactions."),
        q("moderate", "Reye syndrome is associated with aspirin use during:", "Viral illness in children", ["Pregnancy only", "Cirrhosis only", "Iron overload"], "Reye syndrome causes microvesicular fatty change and encephalopathy."),
        q("high", "A patient presents after ingesting a large amount of acetaminophen. Liver biopsy shows massive centrilobular necrosis from a reactive metabolite normally detoxified by glutathione. Which metabolite is responsible?", "NAPQI", ["Bilirubin diglucuronide", "Ceruloplasmin", "Urobilinogen"], "NAPQI accumulation causes acetaminophen hepatotoxicity."),
        q("high", "A child recovering from influenza receives aspirin and develops vomiting, hypoglycemia, encephalopathy, and diffuse microvesicular fatty change in the liver biopsy. Which syndrome is most likely?", "Reye syndrome", ["Wilson disease", "Gilbert syndrome", "Primary biliary cholangitis"], "Reye syndrome is linked to aspirin use during viral illness."),
        q("high", "A population exposed to mold-contaminated grains has increased hepatocellular carcinoma, especially with chronic hepatitis B, and tumors show characteristic p53 mutation patterns. Which toxin is the best-known contributor?", "Aflatoxin B1", ["Carbon monoxide", "Silica", "Vinyl chloride only"], "Aflatoxin B1 synergizes with HBV and mutates p53."),
    ]),
    ("vascular", "Vascular Disorders of the Liver", [
        q("easy", "Budd-Chiari syndrome is obstruction of:", "Hepatic veins", ["Cystic duct", "Common bile duct", "Pancreatic duct"], "Hepatic venous outflow obstruction defines Budd-Chiari syndrome."),
        q("easy", "Chronic right-sided heart failure causes:", "Congestive hepatopathy", ["Celiac disease", "Autoimmune gastritis", "Pyloric stenosis"], "Elevated venous pressure congests liver sinusoids."),
        q("easy", "Nutmeg liver is associated with:", "Chronic passive congestion", ["Acute viral hepatitis only", "Gallstones", "Hemochromatosis only"], "Alternating congested and pale zones create nutmeg appearance."),
        q("moderate", "Sinusoidal obstruction syndrome can follow:", "Bone marrow transplantation", ["Appendectomy only", "Gluten exposure", "H. pylori infection"], "Endothelial injury can obstruct small hepatic veins and sinusoids."),
        q("moderate", "Hepatic infarcts are uncommon because the liver has:", "Dual blood supply", ["No arterial blood", "No portal veins", "No sinusoids"], "Portal vein and hepatic artery provide redundant inflow."),
        q("moderate", "Peliosis hepatis consists of:", "Blood-filled cystic spaces in liver", ["Bile duct stones", "Granulomatous portal tracts", "Fat-filled hepatocytes only"], "Peliosis is sinusoidal dilatation with blood-filled cavities."),
        q("moderate", "Centrilobular congestion and necrosis are prominent in:", "Passive hepatic congestion", ["Focal nodular hyperplasia only", "Gilbert syndrome", "Cholecystitis"], "Zone 3 is most vulnerable to hypoxia and venous congestion."),
        q("high", "A patient with a hypercoagulable state develops painful hepatomegaly, ascites, weight gain, and imaging evidence of hepatic venous outflow obstruction. Which vascular liver disorder best explains the presentation?", "Budd-Chiari syndrome", ["Portal vein cavernoma only", "Primary biliary cholangitis", "Gilbert syndrome"], "Budd-Chiari syndrome obstructs hepatic veins and causes congestive enlargement."),
        q("high", "An autopsy liver from a patient with chronic right heart failure shows red-brown depressed centrilobular regions alternating with tan periportal areas. What gross description matches this pattern?", "Nutmeg liver", ["Linitis plastica", "Strawberry gallbladder", "Pseudomyxoma peritonei"], "Chronic passive congestion produces nutmeg liver."),
        q("high", "After high-dose chemotherapy and marrow transplantation, a patient develops painful hepatomegaly, ascites, and weight gain from endothelial injury of small hepatic venules. Which disorder is likely?", "Sinusoidal obstruction syndrome", ["Autoimmune hepatitis", "Wilson disease", "Cholelithiasis"], "Sinusoidal obstruction syndrome follows toxic endothelial damage."),
    ]),
    ("liver-tumors", "Liver Tumors and Nodules", [
        q("easy", "The most common primary malignant liver tumor is:", "Hepatocellular carcinoma", ["Hemangioma", "Focal nodular hyperplasia", "Cholesterol polyp"], "HCC is the common primary liver malignancy."),
        q("easy", "The most common benign liver tumor is:", "Cavernous hemangioma", ["Hepatoblastoma", "Cholangiocarcinoma", "Angiosarcoma"], "Hemangiomas are common benign vascular lesions."),
        q("easy", "Focal nodular hyperplasia contains a central:", "Stellate scar", ["Auer rod", "Reed-Sternberg cell", "Gallstone"], "FNH often has a central fibrous scar."),
        q("moderate", "Hepatocellular carcinoma commonly arises in:", "Cirrhotic liver", ["Normal appendix", "Bronchial mucosa", "Splenic red pulp"], "Cirrhosis from many causes increases HCC risk."),
        q("moderate", "Cholangiocarcinoma arises from:", "Bile duct epithelium", ["Kupffer cells", "Platelets", "Adrenal cortex"], "Cholangiocarcinoma is an adenocarcinoma of biliary epithelium."),
        q("moderate", "Hepatocellular adenoma is associated with:", "Oral contraceptive or anabolic steroid exposure", ["H. pylori", "Asbestos", "Celiac disease"], "Hormone exposure is a classic association."),
        q("moderate", "Angiosarcoma of liver has been linked to:", "Vinyl chloride exposure", ["Gluten exposure", "EBV only", "Measles virus"], "Vinyl chloride is a known risk for hepatic angiosarcoma."),
        q("high", "A cirrhotic patient has a liver mass with elevated alpha-fetoprotein. Histology shows malignant hepatocytes forming thick trabeculae and vascular invasion. Which tumor is most likely?", "Hepatocellular carcinoma", ["Cavernous hemangioma", "Focal nodular hyperplasia", "Hepatic adenoma"], "HCC often arises in cirrhosis and may produce AFP."),
        q("high", "A young woman taking oral contraceptives has a solitary liver mass composed of benign hepatocytes without normal portal tracts and with risk of hemorrhage. Which lesion is likely?", "Hepatocellular adenoma", ["Focal nodular hyperplasia", "Cholangiocarcinoma", "Hemangiosarcoma"], "Hepatic adenoma is hormone-associated and may bleed."),
        q("high", "A patient with primary sclerosing cholangitis develops a firm biliary tract tumor composed of malignant glands in dense desmoplastic stroma. Which primary liver tumor is most likely?", "Cholangiocarcinoma", ["Hepatocellular carcinoma", "Cavernous hemangioma", "Focal nodular hyperplasia"], "PSC increases risk of cholangiocarcinoma."),
    ]),
    ("gallbladder-biliary", "Gallbladder and Biliary Tract Disease", [
        q("easy", "Most gallstones are composed mainly of:", "Cholesterol", ["Urate", "Calcium oxalate", "Cystine"], "Cholesterol stones are the most common type in many populations."),
        q("easy", "Acute cholecystitis is usually caused by:", "Cystic duct obstruction by gallstone", ["Portal vein thrombosis", "Hepatitis A", "Wilson disease"], "Most acute cholecystitis follows gallstone obstruction."),
        q("easy", "Charcot triad suggests:", "Acute ascending cholangitis", ["Gilbert syndrome", "Alcoholic fatty liver", "Hemochromatosis"], "Fever, jaundice, and right upper quadrant pain suggest cholangitis."),
        q("moderate", "Porcelain gallbladder is associated with increased risk of:", "Gallbladder carcinoma", ["Hepatoblastoma", "Gastric lymphoma", "Appendicitis"], "Chronic calcification is linked to carcinoma risk."),
        q("moderate", "Brown pigment stones are associated with:", "Infection of bile ducts", ["Pure cholesterol supersaturation only", "Achalasia", "Celiac disease"], "Bacterial enzymes promote brown pigment stone formation."),
        q("moderate", "Black pigment stones are associated with:", "Chronic hemolysis", ["H. pylori infection", "Barrett esophagus", "Asthma"], "Unconjugated bilirubin from hemolysis promotes black pigment stones."),
        q("moderate", "Chronic cholecystitis most often follows:", "Repeated gallstone irritation", ["Acute viral myocarditis", "Iron deficiency", "Celiac villous atrophy"], "Chronic inflammation is usually linked to cholelithiasis."),
        q("high", "A patient has fever, jaundice, right upper quadrant pain, hypotension, and confusion from infected obstructed bile ducts under pressure. Which biliary emergency is most likely?", "Acute ascending cholangitis", ["Biliary atresia", "Gilbert syndrome", "Hepatic adenoma"], "Ascending cholangitis occurs when obstruction allows infected bile under pressure."),
        q("high", "A woman has episodic postprandial right upper quadrant pain, and ultrasound shows radiolucent stones formed from supersaturated bile with cholesterol nucleation. Which stone type is most likely?", "Cholesterol gallstones", ["Black pigment stones", "Brown pigment stones", "Urate stones"], "Cholesterol stones form when bile is supersaturated with cholesterol."),
        q("high", "A gallbladder removed after years of recurrent biliary colic shows Rokitansky-Aschoff sinuses, wall thickening, fibrosis, and stones. Which condition best explains these histologic changes?", "Chronic cholecystitis", ["Acute viral hepatitis", "Primary biliary cholangitis", "Budd-Chiari syndrome"], "Chronic cholecystitis has mucosal outpouchings and fibrosis from repeated injury."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch18-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 18 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch18-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 18 questions")
    print(f"Removed {total_removed} existing Chapter 18 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 18 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
