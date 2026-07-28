import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Heart"
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
    ("failure-adaptation", "Cardiac Adaptation, Hypertrophy, and Heart Failure", [
        q("easy", "The main compensatory morphologic response of myocardium to chronic pressure overload is:", "Concentric hypertrophy", ["Eccentric hypertrophy", "Fatty infiltration", "Caseous necrosis"], "Pressure overload adds sarcomeres in parallel, producing thick ventricular walls."),
        q("easy", "Volume overload most often produces:", "Eccentric hypertrophy with chamber dilation", ["Pure concentric hypertrophy only", "Endocardial granulomas", "Valve commissural fusion"], "Volume overload adds sarcomeres in series and dilates the chamber."),
        q("easy", "Left-sided heart failure most commonly causes congestion in the:", "Lungs", ["Spleen", "Skin", "Thyroid"], "Pulmonary venous congestion is the classic consequence of left heart failure."),
        q("moderate", "Brown induration of the lung in chronic left heart failure is due to:", "Hemosiderin-laden macrophages and fibrosis", ["Acute neutrophilic abscesses", "Amyloid in alveolar walls", "Keratin debris in bronchi"], "Repeated pulmonary congestion causes microhemorrhage, heart failure cells, and septal fibrosis."),
        q("moderate", "Right-sided heart failure classically produces:", "Systemic venous congestion with hepatomegaly and peripheral edema", ["Pulmonary edema only", "Left atrial myxoma", "Cerebral berry aneurysm"], "Right heart failure backs blood into systemic venous beds."),
        q("moderate", "The nutmeg appearance of the liver in chronic passive congestion reflects:", "Centrilobular congestion alternating with paler periportal zones", ["Diffuse fatty liver only", "Portal granulomas", "Bile duct hamartomas"], "High venous pressure congests centrilobular regions around terminal hepatic venules."),
        q("moderate", "Cor pulmonale is right ventricular hypertrophy or dilation caused by:", "Pulmonary hypertension from lung or pulmonary vascular disease", ["Systemic hypertension", "Aortic valve stenosis only", "Mitral valve prolapse only"], "Cor pulmonale excludes right-sided failure caused by left heart disease."),
        q("high", "A patient with long-standing systemic hypertension has a thick left ventricular wall, reduced chamber size, and myocytes with enlarged boxcar nuclei. Which hemodynamic load produced this pattern?", "Chronic pressure overload", ["Chronic volume overload", "Pulmonary embolic obstruction", "Primary amyloid infiltration"], "Hypertension creates pressure overload and concentric left ventricular hypertrophy."),
        q("high", "A patient with severe chronic aortic regurgitation develops a massively dilated left ventricle with increased mass. The chamber enlarged because each beat handled excess diastolic volume. Which adaptation is expected?", "Eccentric hypertrophy from volume overload", ["Concentric hypertrophy from pressure overload", "Restrictive cardiomyopathy from amyloid", "Endocardial fibroelastosis"], "Regurgitant flow causes volume overload and eccentric hypertrophy."),
        q("high", "A person with COPD and pulmonary hypertension develops ankle edema, ascites, hepatic congestion, and isolated right ventricular enlargement. The left ventricle is not the primary problem. Which diagnosis fits best?", "Cor pulmonale", ["Left-sided hypertensive heart disease", "Acute rheumatic pancarditis", "Dilated cardiomyopathy"], "Chronic lung disease can cause pulmonary hypertension and secondary right heart enlargement."),
    ]),
    ("ischemia-angina", "Ischemic Heart Disease and Angina", [
        q("easy", "The usual underlying cause of ischemic heart disease is:", "Coronary atherosclerosis", ["Pulmonary arteriolar sclerosis", "Mitral annular calcification", "Amyloid in endocardium"], "Most IHD results from atherosclerotic narrowing or acute plaque change in coronary arteries."),
        q("easy", "Stable angina is usually caused by:", "Fixed coronary stenosis limiting flow during increased demand", ["Complete valve rupture", "Acute myocarditis", "Right atrial tumor emboli"], "Stable angina is predictable exertional pain from chronic critical stenosis."),
        q("easy", "Prinzmetal angina is caused primarily by:", "Coronary artery vasospasm", ["Venous valve failure", "Pulmonary infarction", "Myocardial abscess"], "Variant angina reflects episodic coronary spasm, often at rest."),
        q("moderate", "Unstable angina is best explained by:", "Acute plaque disruption with nonocclusive thrombosis", ["Chronic passive congestion only", "Pure myocardial hypertrophy", "Calcific aortic stenosis without coronary disease"], "Unstable angina is part of acute coronary syndrome and often follows plaque rupture."),
        q("moderate", "Critical fixed coronary stenosis is usually defined as about:", "70% luminal narrowing", ["10% luminal narrowing", "25% luminal narrowing", "100% narrowing in every case"], "A fixed narrowing of roughly 70% can limit flow during exertion."),
        q("moderate", "Silent myocardial ischemia is especially common in patients with:", "Diabetes mellitus", ["Albinism", "Achondroplasia", "Acute appendicitis"], "Autonomic neuropathy in diabetes can blunt ischemic pain."),
        q("moderate", "Subendocardium is most vulnerable to ischemia because it:", "Has the highest wall stress and poorest perfusion reserve", ["Has no mitochondria", "Is supplied only by veins", "Cannot hypertrophy"], "The inner myocardium is farthest from epicardial vessels and compressed during systole."),
        q("high", "A patient has exertional chest pressure relieved by rest. Coronary angiography shows a stable proximal LAD plaque causing 75% narrowing, without thrombus or plaque rupture. Which syndrome is most likely?", "Stable angina", ["Unstable angina", "Prinzmetal angina", "Acute myocarditis"], "Predictable demand-related pain reflects fixed critical coronary stenosis."),
        q("high", "A patient has recurrent chest pain at rest with transient ST elevation that improves with nitrates. Angiography between episodes shows no critical fixed stenosis. Which mechanism best explains the symptoms?", "Episodic coronary vasospasm", ["Chronic right heart failure", "Aortic dissection into the media", "Mitral valve commissural fusion"], "Prinzmetal angina is episodic vasospasm and may occur without severe atherosclerosis."),
        q("high", "A patient has increasing frequency of chest pain with minimal exertion. Troponin remains negative, but a disrupted coronary plaque has a platelet-rich thrombus that does not fully occlude the artery. Which diagnosis fits?", "Unstable angina", ["Stable angina", "Transmural myocardial infarction", "Restrictive cardiomyopathy"], "Unstable angina has acute plaque change and ischemia without detectable myocyte necrosis."),
    ]),
    ("myocardial-infarction", "Myocardial Infarction: Pathogenesis, Morphology, and Markers", [
        q("easy", "Most transmural myocardial infarctions are caused by:", "Acute coronary plaque rupture with thrombosis", ["Primary bacterial myocarditis", "Mitral stenosis", "Cardiac myxoma"], "Plaque disruption exposes thrombogenic material and can occlude a coronary artery."),
        q("easy", "The earliest highly sensitive serum marker of myocardial necrosis is:", "Cardiac troponin", ["Alkaline phosphatase", "Amylase", "D-dimer"], "Troponins rise after myocyte injury and remain elevated for days."),
        q("easy", "Coagulative necrosis is the typical necrosis pattern in:", "Myocardial infarction", ["Brain infarction", "Tuberculous myocarditis", "Fat necrosis only"], "Ischemic death of myocardium produces coagulative necrosis."),
        q("moderate", "A myocardial infarct usually becomes grossly apparent after about:", "12 to 24 hours", ["5 minutes", "1 hour", "6 months"], "Early infarcts may be grossly invisible before pallor and mottling develop."),
        q("moderate", "Neutrophilic infiltration is most prominent in myocardial infarction during:", "1 to 3 days", ["First 10 minutes", "2 to 8 weeks", "Several years only"], "Acute inflammation with neutrophils dominates during the first few days."),
        q("moderate", "Macrophage removal of necrotic myocardium is most prominent around:", "3 to 7 days", ["Immediately at occlusion", "30 minutes", "10 years"], "Macrophages clear dead tissue and leave the wall mechanically weak."),
        q("moderate", "A healed myocardial infarct is characterized by:", "Dense collagenous scar", ["Regeneration of normal myocytes", "Caseating granuloma", "Cavernous vascular channels"], "Myocytes have limited regenerative capacity, so healing occurs by fibrosis."),
        q("high", "A patient dies 2 days after sudden occlusion of the left anterior descending artery. Histology from the anterior wall shows wavy fibers, coagulative necrosis, and a dense neutrophilic infiltrate. Which time window best fits?", "1 to 3 days after infarction", ["Less than 30 minutes", "10 to 14 days", "Several months"], "Neutrophils dominate the early acute phase of myocardial infarction."),
        q("high", "A patient develops a myocardial infarct from a brief severe drop in blood pressure superimposed on diffuse coronary atherosclerosis. Necrosis is limited to the inner third to half of the ventricular wall and involves multiple territories. Which pattern is this?", "Subendocardial infarction", ["Transmural infarction", "Constrictive pericarditis", "Dilated cardiomyopathy"], "Global hypoperfusion commonly injures the vulnerable subendocardium."),
        q("high", "A patient presents 5 days after an untreated myocardial infarction and suddenly collapses with tamponade. The infarcted wall was softened by macrophage digestion before scar formation. Which complication occurred?", "Free wall rupture", ["Papillary muscle fibrosis", "Chronic aneurysm calcification", "Fibrinous pericarditis only"], "Rupture risk is highest when necrotic myocardium has been digested but not yet replaced by scar."),
    ]),
    ("mi-complications", "Complications of Myocardial Infarction and Chronic IHD", [
        q("easy", "The most common cause of sudden death after acute myocardial infarction is:", "Arrhythmia", ["Cardiac rupture in every case", "Atrial myxoma", "Mitral stenosis"], "Electrical instability after ischemia commonly causes lethal arrhythmias."),
        q("easy", "Papillary muscle rupture after MI most often causes acute:", "Mitral regurgitation", ["Aortic stenosis", "Tricuspid stenosis", "Pulmonary stenosis"], "Papillary muscle rupture prevents mitral valve closure."),
        q("easy", "A true ventricular aneurysm after MI consists of:", "Bulging scarred ventricular wall", ["Contained free wall rupture only", "Vegetation on a valve", "Dilated coronary sinus"], "A true aneurysm is formed by thinned scarred myocardium."),
        q("moderate", "Ventricular septal rupture after MI produces:", "Acute left-to-right shunt", ["Right-to-left shunt from birth", "Pure pulmonary stenosis", "Left atrial tumor"], "Septal rupture allows high-pressure LV blood to enter the RV."),
        q("moderate", "Mural thrombus after MI forms because of:", "Endocardial injury and abnormal ventricular contraction", ["Excess lymphatic drainage", "Complete valve sterilization", "Low platelet count only"], "Damaged endocardium and stasis favor thrombosis."),
        q("moderate", "Dressler syndrome is:", "Autoimmune fibrinous pericarditis weeks after MI", ["Immediate septic endocarditis", "Congenital valve malformation", "Primary myocardial amyloidosis"], "Dressler syndrome is a delayed immune-mediated postinfarction pericarditis."),
        q("moderate", "Chronic ischemic heart disease often presents as:", "Progressive heart failure due to ischemic myocardial damage", ["Diffuse purulent myocarditis", "Benign atrial lipoma only", "Pulmonary valve agenesis"], "Repeated ischemic injury and scarring can cause chronic pump failure."),
        q("high", "A patient 4 days after an inferior wall MI develops sudden pulmonary edema and a new loud systolic murmur. The posteromedial papillary muscle has a single blood supply and has ruptured. Which valve lesion results?", "Acute severe mitral regurgitation", ["Acute aortic stenosis", "Tricuspid atresia", "Pulmonary regurgitation from carcinoid"], "Papillary muscle rupture causes abrupt failure of mitral valve competence."),
        q("high", "A patient who survived a large transmural MI later has a thin dyskinetic bulge of the left ventricular wall. The lesion contains dense scar and is a focus for mural thrombus and arrhythmia, but it rarely ruptures. What is it?", "True ventricular aneurysm", ["Pseudoaneurysm", "Acute free wall rupture", "Valvular vegetation"], "A healed infarct can form a true aneurysm made of scarred ventricular wall."),
        q("high", "Weeks after MI, a patient develops fever, pleuritic chest pain, and pericardial friction rub. The coronary artery is patent and there is no new infarct. Which mechanism best explains the pericarditis?", "Autoimmune response to myocardial antigens", ["Direct bacterial infection of valves", "Amyloid deposition", "Congenital septal defect"], "Dressler syndrome is delayed immune-mediated pericarditis after myocardial injury."),
    ]),
    ("hypertensive-valvular", "Hypertensive, Valvular, and Calcific Heart Disease", [
        q("easy", "Systemic hypertension most commonly causes:", "Left ventricular hypertrophy", ["Right atrial myxoma", "Pulmonary valve atresia", "Mitral valve vegetations only"], "The left ventricle adapts to systemic pressure overload."),
        q("easy", "Calcific aortic stenosis is most common in:", "Older adults", ["Newborns only", "Adolescents only", "Pregnant patients only"], "Degenerative calcific aortic stenosis increases with age."),
        q("easy", "Mitral annular calcification most often involves:", "Fibrous ring of the mitral valve", ["Pulmonary valve leaflets only", "SA node only", "Aortic vasa vasorum"], "Calcium deposits can form in the mitral annulus, especially in older adults."),
        q("moderate", "Bicuspid aortic valve predisposes to:", "Earlier calcific aortic stenosis", ["Mitral valve prolapse in every case", "Pulmonary embolism only", "Right ventricular myxoma"], "Two cusps undergo accelerated wear and calcification."),
        q("moderate", "Calcific aortic stenosis produces which hemodynamic load?", "Left ventricular pressure overload", ["Left ventricular volume overload", "Right atrial volume overload", "Pulmonary venous volume depletion"], "The LV must generate higher pressure to eject across a narrowed valve."),
        q("moderate", "Mitral valve prolapse classically shows:", "Myxomatous degeneration of valve leaflets", ["Caseating granulomas", "Fish-mouth commissural fusion", "Vegetations along the line of closure"], "MVP has redundant, gelatinous leaflets due to myxomatous change."),
        q("moderate", "Aortic regurgitation causes:", "Left ventricular volume overload", ["Left ventricular pressure overload only", "Right ventricular pressure overload only", "No chamber remodeling"], "Regurgitant aortic flow returns to the LV during diastole."),
        q("high", "An elderly patient has exertional syncope and angina. The aortic valve is heavily calcified with immobile cusps but no commissural fusion. The left ventricle is concentrically hypertrophied. Which lesion is most likely?", "Degenerative calcific aortic stenosis", ["Rheumatic mitral stenosis", "Carcinoid tricuspid disease", "Libman-Sacks endocarditis"], "Age-related calcific aortic stenosis causes LV pressure overload without rheumatic commissural fusion."),
        q("high", "A 48-year-old with a congenital bicuspid aortic valve develops progressive calcification and stenosis decades earlier than typical degenerative disease. Which factor explains the early presentation?", "Abnormal cusp number causing accelerated mechanical stress", ["Autoimmune Aschoff bodies", "Fungal valve invasion", "Metastatic calcification of normal cusps only"], "Bicuspid valves are mechanically stressed and calcify earlier."),
        q("high", "A tall young patient has midsystolic click and late systolic murmur. The mitral leaflets are enlarged and balloon into the left atrium, with proteoglycan-rich myxomatous stroma. Which diagnosis fits?", "Mitral valve prolapse", ["Calcific aortic stenosis", "Acute rheumatic valvulitis", "Infective endocarditis"], "MVP is characterized by myxomatous degeneration and systolic billowing."),
    ]),
    ("rheumatic-endocarditis", "Rheumatic Fever and Rheumatic Heart Disease", [
        q("easy", "Acute rheumatic fever follows infection with:", "Group A beta-hemolytic streptococci", ["Staphylococcus aureus", "Candida albicans", "Coxsackievirus B"], "Rheumatic fever is an immune reaction after streptococcal pharyngitis."),
        q("easy", "The most commonly involved valve in chronic rheumatic heart disease is:", "Mitral valve", ["Pulmonary valve", "Tricuspid valve only", "Aortic valve only in every case"], "The mitral valve is affected most often, alone or with the aortic valve."),
        q("easy", "Aschoff bodies are characteristic of:", "Rheumatic carditis", ["Calcific aortic stenosis", "Carcinoid heart disease", "Cardiac amyloidosis"], "Aschoff bodies are granuloma-like inflammatory lesions of acute rheumatic fever."),
        q("moderate", "Anitschkow cells have:", "Caterpillar-like chromatin", ["Reed-Sternberg nucleoli", "Auer rods", "Owl-eye inclusions"], "Activated macrophages in Aschoff bodies show wavy caterpillar chromatin."),
        q("moderate", "Acute rheumatic heart disease can cause:", "Pancarditis", ["Isolated coronary vasospasm", "Pure pericardial tumor", "Only right atrial dilation"], "Rheumatic fever may involve endocardium, myocardium, and pericardium."),
        q("moderate", "Chronic rheumatic mitral stenosis shows:", "Commissural fusion and chordal thickening", ["Myxomatous ballooning only", "Sterile verrucae on both sides of leaflets", "Friable bulky vegetations"], "Chronic rheumatic disease scars valves and fuses commissures."),
        q("moderate", "The classic gross appearance of severe rheumatic mitral stenosis is:", "Fish-mouth or buttonhole stenosis", ["Water-bottle heart", "Boot-shaped heart", "Shaggy bread-and-butter surface only"], "Commissural fusion creates a narrowed fish-mouth orifice."),
        q("high", "A child develops migratory polyarthritis, fever, and carditis weeks after untreated streptococcal pharyngitis. Myocardial lesions contain activated macrophages with caterpillar chromatin. Which immune disease is present?", "Acute rheumatic fever", ["Infective endocarditis", "Viral myocarditis", "Kawasaki disease"], "Acute rheumatic fever is a post-streptococcal immune disease with Aschoff bodies."),
        q("high", "An adult from an endemic region has exertional dyspnea, left atrial dilation, atrial fibrillation, and a stenotic mitral valve with fused commissures and thickened chordae. Which prior condition caused it?", "Chronic rheumatic heart disease", ["Mitral valve prolapse", "Degenerative annular calcification", "Carcinoid syndrome"], "Chronic rheumatic scarring commonly causes mitral stenosis and left atrial enlargement."),
        q("high", "A patient with acute rheumatic fever has small vegetations along the lines of valve closure, myocarditis with Aschoff bodies, and fibrinous pericarditis. What term best describes this distribution?", "Pancarditis", ["Endocardial fibroelastosis", "Constrictive pericarditis", "Restrictive cardiomyopathy"], "Acute rheumatic fever can involve all three layers of the heart."),
    ]),
    ("infective-nbte-lse", "Infective and Noninfective Endocarditis", [
        q("easy", "Infective endocarditis is infection of the:", "Endocardial surface, usually valves", ["Epicardial fat only", "Coronary veins only", "Pericardial sac only"], "Microbes colonize thrombotic deposits on valves or mural endocardium."),
        q("easy", "The most common cause of acute destructive native-valve endocarditis is:", "Staphylococcus aureus", ["Streptococcus pyogenes", "Mycoplasma pneumoniae", "Aspergillus only"], "S. aureus can infect normal or abnormal valves and causes aggressive disease."),
        q("easy", "Subacute infective endocarditis on abnormal valves is commonly caused by:", "Viridans streptococci", ["Rotavirus", "Treponema pallidum", "Enterobius vermicularis"], "Viridans streptococci often cause indolent endocarditis after transient bacteremia."),
        q("moderate", "Vegetations in infective endocarditis are typically:", "Bulky, friable, and destructive", ["Tiny sterile platelet deposits only", "Pure calcium nodules", "Tumor-like myxoid nodules"], "Infected vegetations contain fibrin, inflammatory cells, and organisms."),
        q("moderate", "IV drug use endocarditis most often involves the:", "Tricuspid valve", ["Mitral annulus only", "Aortic root only", "Pulmonary veins"], "Injected organisms reach the right heart first."),
        q("moderate", "Nonbacterial thrombotic endocarditis is associated with:", "Hypercoagulable states and malignancy", ["Group A strep pharyngitis", "Congenital rubella", "COPD alone"], "NBTE forms sterile platelet-fibrin vegetations in wasting or hypercoagulable states."),
        q("moderate", "Libman-Sacks endocarditis is associated with:", "Systemic lupus erythematosus", ["Marfan syndrome", "Cystic fibrosis", "Phenylketonuria"], "SLE can produce sterile vegetations on either side of valve leaflets."),
        q("high", "A febrile IV drug user has septic pulmonary emboli and blood cultures grow Staphylococcus aureus. Echocardiography shows a large friable vegetation on the valve first reached by venous blood. Which valve is most likely involved?", "Tricuspid valve", ["Mitral valve", "Aortic valve", "Pulmonary vein valve"], "Right-sided S. aureus endocarditis in IV drug use commonly affects the tricuspid valve."),
        q("high", "A patient with pancreatic adenocarcinoma develops multiple small sterile vegetations along valve closure lines. There is no valve destruction or organism growth, but systemic emboli occur. Which diagnosis is most likely?", "Nonbacterial thrombotic endocarditis", ["Acute infective endocarditis", "Rheumatic verrucous endocarditis", "Carcinoid heart disease"], "Malignancy-associated hypercoagulability can cause sterile platelet-fibrin vegetations."),
        q("high", "A young woman with SLE has sterile vegetations on both surfaces of the mitral valve leaflets and immune complex-mediated inflammation. Which form of endocarditis is this?", "Libman-Sacks endocarditis", ["Subacute bacterial endocarditis", "Nonbacterial thrombotic endocarditis", "Rheumatic endocarditis"], "Libman-Sacks lesions in SLE may occur on either side of valve leaflets."),
    ]),
    ("cardiomyopathy-myocarditis", "Cardiomyopathies and Myocarditis", [
        q("easy", "Dilated cardiomyopathy is characterized by:", "Ventricular dilation with systolic dysfunction", ["Massive concentric hypertrophy only", "Pericardial calcification", "Valve commissural fusion"], "DCM has impaired contractility and dilated chambers."),
        q("easy", "Hypertrophic cardiomyopathy commonly involves mutation in genes encoding:", "Sarcomere proteins", ["Lysosomal enzymes only", "Collagen type IV only", "Hemoglobin chains"], "HCM is often caused by mutations in contractile apparatus proteins."),
        q("easy", "Restrictive cardiomyopathy primarily causes:", "Impaired ventricular filling", ["Pure outflow infection", "Valve rupture", "Coronary thrombosis only"], "Stiff ventricles restrict diastolic filling."),
        q("moderate", "The classic histology of hypertrophic cardiomyopathy is:", "Myocyte hypertrophy with myofiber disarray", ["Caseating granulomas", "Suppurative abscesses", "Aschoff bodies only"], "Myofiber disarray is a characteristic microscopic feature of HCM."),
        q("moderate", "A common infiltrative cause of restrictive cardiomyopathy is:", "Amyloidosis", ["Influenza rhinitis", "Aortic atherosclerosis", "Mitral annular calcification"], "Amyloid deposition stiffens the ventricular walls."),
        q("moderate", "Viral myocarditis is most commonly associated with:", "Lymphocytic infiltrates and myocyte injury", ["Neutrophils without myocyte injury", "Sterile platelet thrombi only", "Valve calcification"], "Viral myocarditis shows lymphocytes with myocyte necrosis."),
        q("moderate", "Chagas myocarditis is caused by:", "Trypanosoma cruzi", ["Toxoplasma gondii", "Candida albicans", "Schistosoma haematobium"], "T. cruzi can cause chronic myocarditis and dilated cardiomyopathy."),
        q("high", "A young athlete dies suddenly during exertion. The heart has asymmetric septal hypertrophy, small LV cavity, and histologic myofiber disarray. Which disease is most likely?", "Hypertrophic cardiomyopathy", ["Dilated cardiomyopathy", "Restrictive amyloidosis", "Rheumatic myocarditis"], "HCM causes asymmetric hypertrophy and is an important cause of sudden death in young athletes."),
        q("high", "A patient with alcohol use disorder develops four-chamber dilation, mural thrombi, and reduced ejection fraction. Histology shows nonspecific myocyte hypertrophy and interstitial fibrosis. Which cardiomyopathy pattern is present?", "Dilated cardiomyopathy", ["Hypertrophic cardiomyopathy", "Restrictive cardiomyopathy", "Constrictive pericarditis"], "Toxic injury such as alcohol can produce DCM with systolic failure."),
        q("high", "A patient with plasma cell dyscrasia develops heart failure with normal-sized ventricles, biatrial enlargement, thick stiff walls, and Congo red-positive deposits. Which mechanism best explains the physiology?", "Amyloid restrictive cardiomyopathy", ["Sarcomeric myofiber disarray", "Acute plaque rupture", "Rheumatic commissural fusion"], "Amyloid deposition causes a stiff, poorly filling restrictive heart."),
    ]),
    ("pericardial", "Pericardial Disease", [
        q("easy", "Acute pericarditis often presents with:", "Pleuritic chest pain and friction rub", ["Painless jaundice", "Hemoptysis only", "Renal colic"], "Inflamed pericardial surfaces can cause sharp pain and an audible rub."),
        q("easy", "Cardiac tamponade is caused by:", "Compression of the heart by pericardial fluid", ["Mitral valve prolapse", "Aortic atherosclerosis", "Pulmonary emphysema only"], "Fluid under pressure impairs cardiac filling."),
        q("easy", "Serous pericarditis can occur with:", "Viral infection", ["Only bacterial abscess", "Only metastatic carcinoma", "Only valve calcification"], "Viral and immune causes often produce serous inflammation."),
        q("moderate", "Uremic pericarditis is typically:", "Fibrinous or serofibrinous", ["Caseating only", "Purely fatty", "Always purulent"], "Uremia can cause a fibrinous pericarditis with a friction rub."),
        q("moderate", "Purulent pericarditis most often indicates:", "Bacterial infection of the pericardial space", ["Benign age-related calcification", "Sarcomere mutation", "Chronic hypertension"], "Pus in the pericardium reflects microbial infection."),
        q("moderate", "Constrictive pericarditis causes heart failure by:", "Restricting diastolic filling with a dense fibrotic pericardium", ["Destroying coronary intima", "Rupturing papillary muscle", "Dilating all valves"], "A rigid pericardium limits expansion of the heart."),
        q("moderate", "Hemopericardium can result from:", "Free wall rupture after myocardial infarction", ["Uncomplicated stable angina", "Simple fatty streak", "Primary Raynaud phenomenon"], "Blood entering the pericardial sac can rapidly cause tamponade."),
        q("high", "A patient with renal failure develops sharp chest pain and a rough pericardial friction rub. At autopsy, the pericardial surfaces are shaggy with fibrin strands but no pus. Which type of pericarditis is present?", "Fibrinous pericarditis", ["Purulent pericarditis", "Hemorrhagic pericarditis", "Constrictive pericarditis"], "Uremia commonly causes fibrinous pericarditis."),
        q("high", "After a stab wound to the chest, a patient has hypotension, elevated jugular venous pressure, and muffled heart sounds. The pericardial sac contains blood under pressure. Which acute syndrome is this?", "Cardiac tamponade", ["Constrictive pericarditis", "Stable angina", "Hypertrophic cardiomyopathy"], "Rapid pericardial fluid accumulation impairs filling and causes tamponade."),
        q("high", "A patient years after tuberculous pericarditis has a calcified, fibrotic pericardium encasing the heart. Diastolic filling is limited despite preserved myocardial contractility. Which diagnosis fits?", "Constrictive pericarditis", ["Dilated cardiomyopathy", "Acute serous pericarditis", "Aortic stenosis"], "Chronic fibrous pericardial scarring can mechanically constrain the heart."),
    ]),
    ("congenital", "Congenital Heart Disease", [
        q("easy", "The most common congenital cardiac anomaly is:", "Ventricular septal defect", ["Tetralogy of Fallot", "Tricuspid atresia", "Transposition of great arteries"], "VSD is the most common congenital heart defect."),
        q("easy", "Left-to-right shunts initially cause:", "Increased pulmonary blood flow", ["Immediate cyanosis in every case", "Systemic venous thrombosis", "Aortic dissection"], "Oxygenated blood recirculates through the lungs."),
        q("easy", "Tetralogy of Fallot includes:", "VSD, pulmonary stenosis, overriding aorta, and right ventricular hypertrophy", ["ASD, PDA, mitral stenosis, LVH", "Coarctation, bicuspid valve, PDA, LV dilation", "Ebstein anomaly, ASD, MR, LA dilation"], "These four features define tetralogy of Fallot."),
        q("moderate", "Eisenmenger syndrome means:", "Reversal of a left-to-right shunt due to pulmonary hypertension", ["Closure of all shunts at birth", "Acute rheumatic fever", "Congenital absence of myocardium"], "Long-standing increased pulmonary flow can cause irreversible pulmonary vascular disease and cyanosis."),
        q("moderate", "Patent ductus arteriosus connects the:", "Pulmonary artery to the aorta", ["Left atrium to right atrium", "Left ventricle to right ventricle", "Aorta to coronary sinus"], "The ductus arteriosus normally links pulmonary artery and aorta in fetal life."),
        q("moderate", "Coarctation of the aorta in adults is classically associated with:", "Upper extremity hypertension and weak femoral pulses", ["Cyanosis from birth in every case", "Mitral vegetations", "Right atrial tumor"], "Postductal coarctation causes high arm pressure and low leg pressure."),
        q("moderate", "Transposition of the great arteries requires survival through:", "A mixing lesion such as VSD, ASD, or PDA", ["Complete absence of any shunt", "Mitral commissural fusion", "Aortic valve calcification"], "Parallel circuits are incompatible with life unless blood mixes."),
        q("high", "An infant with unrepaired VSD develops progressive pulmonary vascular remodeling, pulmonary hypertension, cyanosis, and clubbing. The original left-to-right shunt has reversed direction. Which complication occurred?", "Eisenmenger syndrome", ["Tetralogy of Fallot repair", "Acute rheumatic fever", "Cardiac tamponade"], "Pulmonary vascular disease can reverse shunts and produce late cyanosis."),
        q("high", "A cyanotic child squats during exertion. The heart shows a large VSD, obstruction of the right ventricular outflow tract, overriding aorta, and right ventricular hypertrophy. Which congenital disease is present?", "Tetralogy of Fallot", ["Atrial septal defect", "Patent ductus arteriosus", "Coarctation of the aorta"], "Tetralogy of Fallot is the classic cyanotic defect improved by squatting."),
        q("high", "A neonate has severe cyanosis soon after birth. The aorta arises from the right ventricle and pulmonary artery from the left ventricle, creating two parallel circulations. Which additional feature is necessary for survival?", "A communication allowing mixing of blood", ["Complete closure of the ductus arteriosus", "Calcific aortic stenosis", "Left atrial myxoma"], "Transposition requires a shunt such as ASD, VSD, or PDA to permit mixing."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch12-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 12 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch12-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 12 questions")
    print(f"Removed {total_removed} existing Chapter 12 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 12 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
