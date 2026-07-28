import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Kidney"
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
    ("renal-response", "Renal Anatomy, Injury Responses, and Clinical Syndromes", [
        q("easy", "The basic filtering unit of the kidney is the:", "Glomerulus", ["Alveolus", "Hepatic lobule", "Splenic follicle"], "The glomerulus filters plasma into Bowman space."),
        q("easy", "Nephrotic syndrome is defined by heavy:", "Proteinuria", ["Hematuria only", "Bacteriuria only", "Glycosuria only"], "Massive proteinuria is the central feature of nephrotic syndrome."),
        q("easy", "Nephritic syndrome is classically associated with:", "Hematuria", ["Pure steatorrhea", "Hemarthrosis", "Achlorhydria"], "Glomerular inflammation causes hematuria and red cell casts."),
        q("moderate", "Red blood cell casts indicate bleeding from:", "Glomeruli", ["Ureter stones only", "Bladder mucosa only", "Prostate only"], "RBC casts form in tubules after glomerular bleeding."),
        q("moderate", "Podocyte foot process injury primarily causes:", "Proteinuria", ["Bile obstruction", "Hypochlorhydria", "Hypercalcemia only"], "Podocytes maintain the filtration barrier to protein."),
        q("moderate", "Azotemia means elevated blood levels of:", "Urea nitrogen and creatinine", ["Bilirubin and bile salts", "Amylase and lipase", "Insulin and glucagon"], "Reduced kidney filtration raises nitrogenous wastes."),
        q("moderate", "Rapidly progressive glomerulonephritis is characterized histologically by:", "Crescents", ["Kimmelstiel-Wilson nodules only", "Psammoma bodies", "Mallory bodies"], "Crescents reflect severe glomerular injury."),
        q("high", "A patient has generalized edema, hypoalbuminemia, hyperlipidemia, lipiduria, and sustained urine protein excretion above 3.5 grams per day. Which renal clinical syndrome is present?", "Nephrotic syndrome", ["Nephritic syndrome", "Acute pyelonephritis", "Renal colic"], "Heavy proteinuria with hypoalbuminemia and edema defines nephrotic syndrome."),
        q("high", "A patient develops cola-colored urine, hypertension, oliguria, and red blood cell casts after an inflammatory glomerular injury. Which renal syndrome best explains these findings?", "Nephritic syndrome", ["Fanconi syndrome", "Renal tubular acidosis only", "Diabetes insipidus"], "Nephritic syndrome results from glomerular inflammation and hematuria."),
        q("high", "A renal biopsy shows epithelial proliferation within Bowman space compressing glomerular tufts after fibrin leaks through damaged capillary walls. Which lesion is being described?", "Crescent formation", ["Wire-loop deposit only", "Papillary necrosis", "Foam cell cluster"], "Crescents are proliferating parietal epithelial cells and macrophages."),
    ]),
    ("nephrotic", "Nephrotic Syndrome: Minimal Change, FSGS, and Membranous Nephropathy", [
        q("easy", "Minimal change disease is the most common nephrotic syndrome in:", "Children", ["Elderly smokers only", "Pregnant women only", "Cirrhotic adults only"], "Minimal change disease commonly causes childhood nephrotic syndrome."),
        q("easy", "Minimal change disease shows effacement of:", "Podocyte foot processes", ["Collecting duct cilia", "Ureteric smooth muscle", "Renal papillae"], "Electron microscopy shows diffuse foot process effacement."),
        q("easy", "Membranous nephropathy primarily affects:", "Adults", ["Only neonates", "Only toddlers", "Only fetuses"], "Membranous nephropathy is a common adult nephrotic syndrome."),
        q("moderate", "Focal segmental glomerulosclerosis means sclerosis involving:", "Some glomeruli and parts of tufts", ["All glomeruli entirely", "Only renal pelvis", "Only collecting ducts"], "FSGS is focal and segmental."),
        q("moderate", "Membranous nephropathy has immune deposits located:", "Subepithelial", ["Subendothelial only", "Mesangial only", "Intratubular only"], "Subepithelial immune complexes thicken capillary walls."),
        q("moderate", "Primary membranous nephropathy is often associated with antibodies to:", "PLA2 receptor", ["GBM collagen IV alpha-3 only", "AQP2", "Factor VIII"], "Anti-PLA2R antibodies are common in primary membranous nephropathy."),
        q("moderate", "HIV and heroin use are associated with:", "FSGS", ["Minimal change disease only", "IgA nephropathy only", "Alport syndrome"], "Secondary FSGS may occur with HIV or heroin exposure."),
        q("high", "A child develops abrupt edema and heavy selective albuminuria after a respiratory infection. Light microscopy is nearly normal, but electron microscopy shows diffuse foot process effacement. Which disease is most likely?", "Minimal change disease", ["Membranous nephropathy", "IgA nephropathy", "Diabetic nephropathy"], "Minimal change disease causes nephrotic syndrome with normal light microscopy."),
        q("high", "An adult has nephrotic syndrome and renal biopsy shows diffuse capillary wall thickening with granular IgG and C3. Silver stain shows spikes between subepithelial deposits. Which disease fits?", "Membranous nephropathy", ["Minimal change disease", "Postinfectious GN", "Alport syndrome"], "Membranous nephropathy has subepithelial deposits and spike formation."),
        q("high", "A patient with HIV develops nephrotic syndrome. Biopsy shows sclerosis and hyalinosis involving only segments of some glomerular tufts. Which glomerular disease is most likely?", "Focal segmental glomerulosclerosis", ["Minimal change disease", "Membranoproliferative GN", "Thin basement membrane disease"], "FSGS is segmental scarring and is linked to HIV."),
    ]),
    ("nephritic", "Nephritic Glomerulonephritis and Rapidly Progressive GN", [
        q("easy", "Poststreptococcal glomerulonephritis follows infection by:", "Group A beta-hemolytic streptococci", ["Helicobacter pylori", "Clostridioides difficile", "Giardia"], "Certain nephritogenic streptococcal strains trigger immune complex GN."),
        q("easy", "IgA nephropathy commonly presents with:", "Hematuria after mucosal infection", ["Massive steatorrhea", "Painless jaundice", "Hemarthrosis"], "IgA nephropathy often follows respiratory or GI infection."),
        q("easy", "Goodpasture syndrome involves antibodies against:", "Glomerular basement membrane", ["Podocyte PLA2 receptor only", "Intrinsic factor", "Desmoglein"], "Anti-GBM antibodies bind kidney and lung basement membranes."),
        q("moderate", "Postinfectious GN classically shows electron-dense:", "Subepithelial humps", ["Basket-weave splitting", "Amyloid fibrils", "Zebra bodies"], "Subepithelial hump deposits are classic."),
        q("moderate", "IgA nephropathy has immune deposits mainly in the:", "Mesangium", ["Renal pelvis", "Proximal tubule brush border", "Adrenal cortex"], "IgA immune complexes deposit in mesangium."),
        q("moderate", "Linear immunofluorescence of IgG along GBM suggests:", "Anti-GBM disease", ["Postinfectious GN", "Membranous nephropathy", "Minimal change disease"], "Anti-GBM antibodies create smooth linear staining."),
        q("moderate", "Granular immunofluorescence usually indicates:", "Immune complex deposition", ["Direct anti-GBM antibody only", "Pure ischemia", "Tubular obstruction only"], "Immune complexes create lumpy granular staining."),
        q("high", "A child develops periorbital edema, cola-colored urine, hypertension, low complement, and red cell casts several weeks after impetigo. Biopsy shows subepithelial humps. Which diagnosis is most likely?", "Poststreptococcal glomerulonephritis", ["IgA nephropathy", "Minimal change disease", "Alport syndrome"], "Poststreptococcal GN follows skin or throat infection and causes nephritic syndrome."),
        q("high", "A young adult has recurrent gross hematuria within days of upper respiratory infections. Renal biopsy shows mesangial proliferation with IgA deposits. Which glomerulopathy is most likely?", "IgA nephropathy", ["Poststreptococcal GN", "Membranous nephropathy", "Diabetic nephropathy"], "Synpharyngitic hematuria and mesangial IgA deposits define IgA nephropathy."),
        q("high", "A patient has hemoptysis, rapidly progressive renal failure, crescents, and linear IgG staining along glomerular and alveolar basement membranes. Which disease is most likely?", "Goodpasture syndrome", ["Granulomatosis with polyangiitis only", "Lupus nephritis", "Minimal change disease"], "Goodpasture syndrome is anti-GBM disease affecting lung and kidney."),
    ]),
    ("mpgn-lupus-hereditary", "MPGN, Lupus Nephritis, and Hereditary Glomerular Disease", [
        q("easy", "Alport syndrome is a hereditary defect of:", "Type IV collagen", ["Type I collagen only", "Elastin", "Fibrillin"], "Alport syndrome affects collagen IV in basement membranes."),
        q("easy", "Lupus nephritis occurs in:", "Systemic lupus erythematosus", ["Celiac disease", "Achalasia", "Hemophilia A"], "SLE commonly involves immune complex nephritis."),
        q("easy", "Thin basement membrane disease usually causes:", "Benign hematuria", ["Nephrotic syndrome in every case", "Renal stones only", "Pyelonephritis only"], "Thin GBM disease often presents with persistent microscopic hematuria."),
        q("moderate", "Membranoproliferative GN often shows:", "Tram-track capillary walls", ["Spike and dome only", "Normal light microscopy", "Papillary necrosis"], "GBM duplication creates tram-track appearance."),
        q("moderate", "Dense deposit disease is linked to dysregulation of:", "Alternative complement pathway", ["Coagulation factor VIII", "Bile salt transport", "Insulin secretion"], "C3 glomerulopathy reflects complement dysregulation."),
        q("moderate", "Diffuse proliferative lupus nephritis often shows:", "Wire-loop lesions", ["Kimmelstiel-Wilson nodules only", "Hyaline casts only", "Papillary adenoma"], "Subendothelial immune deposits create wire-loop capillaries."),
        q("moderate", "Alport syndrome commonly includes kidney disease with:", "Hearing and ocular abnormalities", ["Asthma and eczema", "Cirrhosis and diabetes", "Hemarthrosis"], "Basement membrane defects affect kidney, ear, and eye."),
        q("high", "A patient with SLE develops hematuria, proteinuria, hypertension, and renal biopsy showing diffuse proliferative glomerulonephritis with wire-loop capillary wall deposits. Which lupus class is most severe/common?", "Class IV diffuse lupus nephritis", ["Class I minimal mesangial disease", "Class VI advanced sclerosing only", "Class V without immune deposits"], "Class IV lupus nephritis is diffuse proliferative and clinically serious."),
        q("high", "A boy has hematuria, progressive renal failure, sensorineural hearing loss, and ocular abnormalities. Electron microscopy shows irregular splitting and lamellation of the GBM. Which disorder is likely?", "Alport syndrome", ["Thin basement membrane disease", "Postinfectious GN", "Minimal change disease"], "Alport syndrome causes basket-weave GBM splitting from collagen IV defects."),
        q("high", "A patient has nephritic-nephrotic features, persistent low complement, and biopsy showing mesangial interposition with duplicated basement membranes forming tram tracks. Which pattern is described?", "Membranoproliferative glomerulonephritis", ["Focal segmental glomerulosclerosis", "Amyloidosis", "Anti-GBM nephritis"], "MPGN has GBM duplication and mesangial interposition."),
    ]),
    ("tubules-aki", "Tubular Injury, Acute Kidney Injury, and Chronic Kidney Disease", [
        q("easy", "Acute tubular injury is a common cause of:", "Acute kidney injury", ["Nephrotic syndrome only", "Renal cell carcinoma", "Hydronephrosis only"], "Tubular epithelial injury frequently causes AKI."),
        q("easy", "Ischemic acute tubular injury commonly affects:", "Proximal tubules and thick ascending limbs", ["Only glomerular mesangium", "Only renal pelvis", "Only ureter"], "These segments have high metabolic demand."),
        q("easy", "Uremia refers to clinical symptoms from:", "Renal failure", ["Liver failure only", "Pancreatic insufficiency", "Pulmonary edema only"], "Uremia is the symptomatic syndrome of severe renal failure."),
        q("moderate", "Muddy brown granular casts suggest:", "Acute tubular injury", ["Minimal change disease", "Goodpasture syndrome only", "Bladder carcinoma"], "Necrotic tubular cells form granular casts."),
        q("moderate", "Myoglobinuria can cause acute tubular injury after:", "Rhabdomyolysis", ["Celiac disease", "Barrett esophagus", "Gallstones"], "Myoglobin is directly toxic to tubules."),
        q("moderate", "Chronic kidney disease often causes secondary:", "Hyperparathyroidism", ["Hypoglycemia", "Achlorhydria", "Pulmonary emphysema"], "Phosphate retention and low vitamin D stimulate PTH."),
        q("moderate", "End-stage kidneys are typically:", "Small and granular", ["Large and spongy only", "Normal in size always", "Filled with gallstones"], "Chronic scarring produces contracted granular kidneys."),
        q("high", "A patient develops oliguria after severe hypotension. Urine contains muddy brown casts, and biopsy shows patchy tubular epithelial necrosis with regeneration. Which lesion is most likely?", "Ischemic acute tubular injury", ["Minimal change disease", "Membranous nephropathy", "Renal oncocytoma"], "Ischemia causes acute tubular injury with granular casts."),
        q("high", "A crush injury patient develops dark urine, high creatine kinase, and acute kidney injury from pigment-induced tubular toxicity and obstruction. Which molecule is most responsible?", "Myoglobin", ["Albumin", "Ceruloplasmin", "Bilirubin"], "Rhabdomyolysis releases myoglobin, which damages tubules."),
        q("high", "A patient with long-standing chronic kidney disease has anemia, bone pain, pruritus, pericarditis, neurologic symptoms, and small granular kidneys. Which systemic syndrome explains these findings?", "Uremia", ["Nephritic syndrome alone", "Renal colic", "Fanconi anemia"], "Severe renal failure produces uremic multisystem manifestations."),
    ]),
    ("tubulointerstitial", "Tubulointerstitial Nephritis, Pyelonephritis, and Papillary Necrosis", [
        q("easy", "Acute pyelonephritis is usually caused by:", "Bacterial infection", ["Immune complex deposition only", "Podocyte mutation", "Amyloid"], "Ascending bacterial infection commonly causes pyelonephritis."),
        q("easy", "The most common cause of urinary tract infection is:", "Escherichia coli", ["Mycobacterium leprae", "Hepatitis B virus", "Giardia"], "Uropathogenic E. coli causes most UTIs."),
        q("easy", "Drug-induced interstitial nephritis often features:", "Eosinophils", ["Auer rods", "Reed-Sternberg cells", "Signet-ring cells"], "Hypersensitivity interstitial nephritis commonly includes eosinophils."),
        q("moderate", "Acute pyelonephritis shows neutrophils in:", "Tubules and interstitium", ["Only glomerular capillary loops", "Only renal artery", "Only ureter muscle"], "Suppurative inflammation involves tubules and interstitium."),
        q("moderate", "Chronic pyelonephritis often produces:", "Coarse corticomedullary scars", ["Diffuse wire-loop lesions", "Subepithelial spikes", "Normal kidneys"], "Recurrent infection or reflux causes irregular scarring."),
        q("moderate", "Analgesic nephropathy is associated with:", "Papillary necrosis", ["Minimal change disease", "Alport syndrome", "Serous cystadenoma"], "Chronic analgesic use can necrose renal papillae."),
        q("moderate", "Vesicoureteral reflux predisposes to:", "Chronic pyelonephritis", ["Membranous nephropathy only", "Renal oncocytoma", "Amyloidosis only"], "Reflux allows infected urine to reach renal parenchyma."),
        q("high", "A woman has fever, flank pain, dysuria, and urine cultures growing E. coli. Kidney biopsy shows neutrophils filling tubules and interstitium with small abscesses. Which diagnosis is most likely?", "Acute pyelonephritis", ["Acute tubular injury", "IgA nephropathy", "Membranous nephropathy"], "Acute pyelonephritis is suppurative bacterial tubulointerstitial infection."),
        q("high", "A patient with recurrent childhood urinary infections from vesicoureteral reflux develops asymmetric kidneys with coarse scars overlying blunted calyces. Which chronic renal disease is present?", "Chronic pyelonephritis", ["Minimal change disease", "Goodpasture syndrome", "Renal amyloidosis"], "Reflux nephropathy causes chronic pyelonephritic scarring and calyceal deformity."),
        q("high", "A patient taking antibiotics develops fever, rash, eosinophilia, sterile pyuria, and acute kidney injury. Biopsy shows interstitial edema with lymphocytes and eosinophils. Which process is likely?", "Drug-induced acute interstitial nephritis", ["Poststreptococcal GN", "Renal cell carcinoma", "Autosomal dominant polycystic kidney disease"], "Drug hypersensitivity can cause eosinophil-rich interstitial nephritis."),
    ]),
    ("vascular-hypertension", "Renal Vascular Disease and Hypertension", [
        q("easy", "Benign nephrosclerosis is associated with:", "Long-standing hypertension", ["Cystic fibrosis", "Viral hepatitis", "Barrett esophagus"], "Chronic hypertension causes arteriolar hyalinosis and scarring."),
        q("easy", "Malignant hypertension can cause:", "Hyperplastic arteriolosclerosis", ["Minimal change disease", "Cystitis only", "Wilms tumor"], "Severe hypertension produces onion-skin arteriolar thickening."),
        q("easy", "Renal artery stenosis activates the:", "Renin-angiotensin system", ["Complement membrane attack complex only", "Intrinsic factor pathway", "Bile acid cycle"], "Reduced renal perfusion stimulates renin release."),
        q("moderate", "Hyaline arteriolosclerosis is seen in hypertension and:", "Diabetes mellitus", ["Hemophilia A", "Asthma only", "Achalasia"], "Diabetes and hypertension damage arterioles."),
        q("moderate", "Malignant nephrosclerosis may show arteriolar:", "Fibrinoid necrosis", ["Amyloid only", "Fat necrosis", "Squamous metaplasia"], "Severe pressure injury causes necrotizing arteriolitis."),
        q("moderate", "Thrombotic microangiopathy injures kidneys by causing:", "Small-vessel thrombosis", ["Podocyte foot process effacement only", "Bacterial abscesses", "Ureter obstruction"], "Microvascular platelet thrombi damage glomeruli and arterioles."),
        q("moderate", "Atheroembolic renal disease may show cholesterol clefts in:", "Renal arteries and arterioles", ["Bowman space only", "Collecting duct nuclei", "Ureter epithelium"], "Cholesterol emboli lodge in small renal vessels."),
        q("high", "A patient with long-standing mild hypertension has small symmetrically granular kidneys and arterioles with homogeneous pink hyaline wall thickening. Which vascular lesion is present?", "Benign nephrosclerosis", ["Malignant nephrosclerosis", "Polyarteritis nodosa", "Renal infarct only"], "Benign nephrosclerosis causes hyaline arteriolosclerosis and granular kidneys."),
        q("high", "A patient presents with very high blood pressure, retinal hemorrhages, acute renal failure, and arterioles showing concentric onion-skin proliferation with fibrinoid necrosis. Which diagnosis is most likely?", "Malignant nephrosclerosis", ["Minimal change disease", "Chronic pyelonephritis", "Renal oncocytoma"], "Malignant hypertension causes hyperplastic arteriolosclerosis and necrotizing injury."),
        q("high", "After vascular catheterization for coronary disease, a patient develops renal dysfunction, livedo reticularis, eosinophilia, and biopsy showing needle-shaped clefts in small arteries. Which process occurred?", "Cholesterol atheroembolism", ["Goodpasture syndrome", "Acute pyelonephritis", "Alport syndrome"], "Atheroemboli release cholesterol crystals into renal vessels."),
    ]),
    ("cysts-stones-obstruction", "Cystic Kidney Disease, Stones, and Obstruction", [
        q("easy", "Autosomal dominant polycystic kidney disease is usually due to mutation in:", "PKD1 or PKD2", ["HBB", "CFTR only", "APC"], "ADPKD involves polycystin genes."),
        q("easy", "Renal stones are also called:", "Nephrolithiasis", ["Hydrocephalus", "Cholestasis", "Bronchiectasis"], "Nephrolithiasis means kidney stone disease."),
        q("easy", "Hydronephrosis is dilation due to:", "Urinary tract obstruction", ["Immune complex deposition", "Podocyte injury", "Iron overload"], "Obstruction dilates renal pelvis and calyces."),
        q("moderate", "ADPKD is associated with berry aneurysms in the:", "Circle of Willis", ["Pulmonary artery only", "Portal vein", "Cystic duct"], "Intracranial aneurysms are an important ADPKD association."),
        q("moderate", "Autosomal recessive polycystic kidney disease is linked to mutation in:", "PKHD1", ["VHL", "RET", "HFE"], "ARPKD involves fibrocystin/polyductin."),
        q("moderate", "The most common kidney stones are composed of:", "Calcium oxalate or calcium phosphate", ["Pure cholesterol", "Bilirubin pigment", "Cystine in every case"], "Most renal calculi are calcium-containing."),
        q("moderate", "Staghorn calculi are often composed of:", "Struvite", ["Cholesterol", "Urate only", "Silica"], "Urease-positive infections can form magnesium ammonium phosphate stones."),
        q("high", "An adult has enlarged kidneys filled with numerous cysts, hypertension, hematuria, liver cysts, and family history of intracranial hemorrhage. Which disease is most likely?", "Autosomal dominant polycystic kidney disease", ["Autosomal recessive polycystic kidney disease", "Medullary sponge kidney", "Simple renal cyst"], "ADPKD causes adult bilateral cystic kidney enlargement and extrarenal cysts."),
        q("high", "A child has bilaterally enlarged smooth kidneys, fusiform dilatation of collecting ducts, and congenital hepatic fibrosis from a fibrocystin defect. Which cystic kidney disease is present?", "Autosomal recessive polycystic kidney disease", ["ADPKD", "Acquired cystic disease", "Multicystic dysplastic kidney"], "ARPKD affects collecting ducts and is associated with hepatic fibrosis."),
        q("high", "A patient with recurrent Proteus urinary infections develops a large branching stone filling the renal pelvis and calyces. Which stone composition is most likely?", "Magnesium ammonium phosphate", ["Calcium bilirubinate", "Cholesterol monohydrate", "Xanthine only"], "Urease-positive organisms alkalinize urine and form struvite staghorn stones."),
    ]),
    ("renal-tumors", "Renal Tumors", [
        q("easy", "The most common malignant kidney tumor in adults is:", "Renal cell carcinoma", ["Wilms tumor", "Oncocytoma", "Angiomyolipoma"], "Renal cell carcinoma is the major adult renal malignancy."),
        q("easy", "Wilms tumor is primarily a tumor of:", "Children", ["Elderly smokers only", "Cirrhotic adults", "Patients with asthma"], "Wilms tumor is the classic pediatric renal malignancy."),
        q("easy", "Clear cell renal cell carcinoma is associated with loss of:", "VHL", ["HBB", "PIGA", "CFTR"], "VHL loss drives clear cell RCC."),
        q("moderate", "Renal cell carcinoma often arises from:", "Renal tubular epithelium", ["Urothelial mucosa only", "Glomerular mesangium", "Adrenal cortex"], "RCCs are epithelial tumors of renal tubules."),
        q("moderate", "RCC can invade the renal vein and extend into the:", "Inferior vena cava", ["Cystic duct", "Bronchus", "Portal triad"], "Renal vein invasion is a characteristic spread pattern."),
        q("moderate", "Angiomyolipoma is associated with:", "Tuberous sclerosis", ["MEN1 only", "Down syndrome only", "Celiac disease"], "Renal angiomyolipomas can occur in tuberous sclerosis."),
        q("moderate", "Papillary renal cell carcinoma is associated with alterations in:", "MET", ["RET only", "BCR-ABL", "HBB"], "Papillary RCC can involve MET pathway activation."),
        q("high", "An older adult has hematuria, flank pain, weight loss, and a golden-yellow renal cortical mass composed of clear cells with delicate vasculature. Which tumor is most likely?", "Clear cell renal cell carcinoma", ["Wilms tumor", "Renal oncocytoma", "Angiomyolipoma"], "Clear cell RCC has lipid-rich clear cells and VHL pathway loss."),
        q("high", "A child has an abdominal mass, hematuria, hypertension, and a renal tumor with blastemal, epithelial, and stromal components. Which pediatric tumor is most likely?", "Wilms tumor", ["Clear cell RCC", "Oncocytoma", "Urothelial carcinoma"], "Wilms tumor is a triphasic pediatric nephroblastoma."),
        q("high", "A patient with tuberous sclerosis has a renal mass composed microscopically of thick-walled vessels, smooth muscle, and adipose tissue. Which benign tumor is described?", "Angiomyolipoma", ["Papillary RCC", "Collecting duct carcinoma", "Wilms tumor"], "Angiomyolipoma contains vessels, muscle, and fat."),
    ]),
    ("lower-urinary-tract", "Lower Urinary Tract, Urothelial Tumors, and Obstructive Uropathy", [
        q("easy", "The most common bladder cancer type is:", "Urothelial carcinoma", ["Squamous carcinoma always", "Adenocarcinoma always", "Nephroblastoma"], "Most bladder cancers are urothelial carcinomas."),
        q("easy", "Cystitis means inflammation of the:", "Urinary bladder", ["Renal glomerulus", "Pancreatic duct", "Gallbladder"], "Cystitis is bladder inflammation."),
        q("easy", "Benign prostatic hyperplasia can cause:", "Urinary obstruction", ["Nephrotic syndrome directly", "Pulmonary embolism only", "Cirrhosis"], "BPH obstructs the prostatic urethra."),
        q("moderate", "Schistosoma haematobium is associated with bladder:", "Squamous cell carcinoma", ["Clear cell RCC", "Wilms tumor", "Oncocytoma"], "Chronic schistosomiasis predisposes to squamous bladder cancer."),
        q("moderate", "Cyclophosphamide exposure can cause hemorrhagic cystitis due to:", "Acrolein", ["Ammonia", "Aflatoxin", "Ceruloplasmin"], "Acrolein is a toxic cyclophosphamide metabolite."),
        q("moderate", "Urothelial carcinoma risk is increased by:", "Cigarette smoking", ["Vitamin C only", "Gluten exposure", "Low altitude"], "Smoking is a major bladder cancer risk factor."),
        q("moderate", "Long-standing obstruction can lead to:", "Hydroureter and hydronephrosis", ["Membranous nephropathy", "Minimal change disease", "IgA nephropathy only"], "Obstruction dilates ureter, pelvis, and calyces."),
        q("high", "An older smoker has painless hematuria, irritative urinary symptoms, and cystoscopy showing a papillary bladder lesion lined by atypical transitional epithelium. Which malignancy is most likely?", "Urothelial carcinoma", ["Renal cell carcinoma", "Wilms tumor", "Prostatic adenocarcinoma"], "Painless hematuria in a smoker suggests urothelial carcinoma."),
        q("high", "A patient from an endemic region has chronic hematuria from Schistosoma haematobium infection and later develops a keratinizing bladder tumor. Which histologic type is favored?", "Squamous cell carcinoma", ["Clear cell carcinoma", "Nephroblastoma", "Papillary RCC"], "Chronic schistosomal cystitis predisposes to squamous carcinoma."),
        q("high", "An older man with severe benign prostatic hyperplasia develops bladder trabeculation, bilateral hydroureter, hydronephrosis, and declining renal function. Which mechanism caused the kidney damage?", "Chronic urinary outflow obstruction", ["Anti-GBM antibody injury", "Podocyte cytokine injury", "Immune complex deposition"], "Lower tract obstruction can back up pressure and damage kidneys."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch20-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 20 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch20-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 20 questions")
    print(f"Removed {total_removed} existing Chapter 20 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 20 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
