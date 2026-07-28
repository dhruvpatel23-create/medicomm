import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Lung"
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
    ("acute-injury", "Atelectasis, Pulmonary Edema, and Acute Lung Injury", [
        q("easy", "Atelectasis means:", "Incomplete expansion or collapse of lung tissue", ["Permanent airway dilation", "Pulmonary arterial thrombosis", "Pleural malignant tumor"], "Atelectasis is loss of alveolar air with reduced lung volume."),
        q("easy", "Cardiogenic pulmonary edema most often results from:", "Left-sided heart failure", ["Thymoma", "Platelet adhesion defect", "Alpha-globin deletion"], "Left heart failure raises pulmonary venous pressure and causes transudative edema."),
        q("easy", "Diffuse alveolar damage is the histologic pattern of:", "Acute respiratory distress syndrome", ["Asthma", "Silicosis", "Pulmonary hamartoma"], "ARDS is characterized by diffuse alveolar damage."),
        q("moderate", "Resorption atelectasis commonly occurs when:", "An airway obstruction prevents air entry distal to the blockage", ["Pulmonary arteries dilate", "Surfactant is excessive", "Pleural plaques calcify"], "Trapped distal air is absorbed, and the affected lung segment collapses."),
        q("moderate", "Compression atelectasis can be caused by:", "Pleural effusion or pneumothorax", ["Beta-globin mutation", "Intrinsic factor loss", "Bronchial cartilage overgrowth"], "External pressure from air or fluid in the pleural cavity collapses adjacent lung."),
        q("moderate", "ARDS hyaline membranes are composed mainly of:", "Fibrin-rich edema fluid and necrotic epithelial debris", ["Keratin pearls", "Amyloid fibrils", "Elastic cartilage"], "Alveolar-capillary injury allows protein-rich fluid to line damaged alveoli."),
        q("moderate", "Noncardiogenic pulmonary edema in ARDS is caused by:", "Increased alveolar-capillary membrane permeability", ["Low oncotic pressure only", "Mitral stenosis only", "Obstructed lymph nodes only"], "ARDS is a permeability edema rather than purely hydrostatic edema."),
        q("high", "A septic patient develops severe hypoxemia refractory to oxygen, bilateral pulmonary infiltrates, and no evidence of left-sided heart failure. Autopsy shows hyaline membranes lining alveoli. Which process is present?", "Acute respiratory distress syndrome", ["Cardiogenic pulmonary edema", "Chronic bronchitis", "Usual interstitial pneumonia"], "Sepsis is a common trigger of ARDS with diffuse alveolar damage."),
        q("high", "After abdominal surgery, a patient has fever, reduced breath sounds at the lung base, and a small area of lower-lobe collapse that improves with deep breathing and mobilization. Which type of atelectasis is most likely?", "Postoperative resorption atelectasis", ["Compression atelectasis from pleural tumor", "Contraction atelectasis from fibrosis", "Neonatal respiratory distress syndrome"], "Mucus plugging after surgery can obstruct bronchi and cause resorption atelectasis."),
        q("high", "A patient with acute myocardial infarction develops dyspnea and pink frothy sputum. Lungs are heavy and wet, and alveoli contain transudate with heart failure cells. Which mechanism caused the edema?", "Increased pulmonary venous hydrostatic pressure", ["Direct alveolar epithelial necrosis from sepsis", "Loss of surfactant in prematurity", "Granulomatous destruction of bronchi"], "Left ventricular failure increases pulmonary venous pressure and causes cardiogenic edema."),
    ]),
    ("obstructive", "Obstructive Lung Disease: Emphysema, Chronic Bronchitis, Asthma, Bronchiectasis", [
        q("easy", "Obstructive lung disease is characterized by difficulty with:", "Airflow during expiration", ["Pulmonary venous drainage", "Pleural fluid absorption", "Red cell production"], "Airflow obstruction is most evident during expiration."),
        q("easy", "Emphysema is defined by:", "Permanent enlargement of airspaces with wall destruction", ["Mucus gland hyperplasia alone", "Interstitial fibrosis only", "Pleural plaque formation"], "Emphysema destroys alveolar septa without prominent fibrosis."),
        q("easy", "Chronic bronchitis is clinically defined by persistent productive cough for:", "At least 3 months in 2 consecutive years", ["1 week only", "Every winter once", "Only during exercise"], "The definition is based on chronic productive cough after excluding other causes."),
        q("moderate", "Centriacinar emphysema is most strongly associated with:", "Cigarette smoking", ["Alpha-1 antitrypsin deficiency only", "Sarcoidosis", "Asbestos exposure"], "Smoking commonly causes centriacinar emphysema, especially in upper lobes."),
        q("moderate", "Panacinar emphysema is classically associated with:", "Alpha-1 antitrypsin deficiency", ["Coal worker pneumoconiosis", "Hypersensitivity pneumonitis", "Lobar pneumonia"], "Alpha-1 antitrypsin deficiency causes diffuse acinar destruction, often lower lobe predominant."),
        q("moderate", "Asthma is driven by:", "Reversible bronchoconstriction with airway inflammation", ["Irreversible alveolar wall destruction only", "Pulmonary artery emboli", "Pleural mesothelial tumors"], "Asthma features episodic reversible airflow obstruction and inflammation."),
        q("moderate", "Bronchiectasis is best defined as:", "Permanent dilation of bronchi due to chronic necrotizing infection or obstruction", ["Transient bronchospasm only", "Alveolar proteinosis", "Pulmonary arterial hypertension"], "Repeated infection and inflammation destroy bronchial walls."),
        q("high", "A long-term smoker has dyspnea, barrel chest, weight loss, decreased breath sounds, and enlarged airspaces with destruction of alveolar septa but little fibrosis. Which diagnosis is most likely?", "Emphysema", ["Chronic bronchitis", "Bronchiectasis", "Idiopathic pulmonary fibrosis"], "Emphysema causes airspace enlargement from alveolar wall destruction."),
        q("high", "A patient has chronic productive cough, cyanosis, recurrent infections, and histology showing enlarged bronchial mucus glands with an increased Reid index. Which obstructive disease is present?", "Chronic bronchitis", ["Emphysema", "Asthma", "Sarcoidosis"], "Chronic bronchitis is associated with mucus gland hyperplasia and productive cough."),
        q("high", "A patient with cystic fibrosis has chronic cough, copious foul sputum, recurrent Pseudomonas infections, and dilated bronchi extending nearly to the pleural surface. Which complication has developed?", "Bronchiectasis", ["Centriacinar emphysema", "Pulmonary embolism", "Hyaline membrane disease"], "Persistent infection and obstruction in CF predispose to bronchiectasis."),
    ]),
    ("asthma-cf", "Asthma, Cystic Fibrosis, and Small Airway Disease", [
        q("easy", "Curschmann spirals in asthma are composed of:", "Shed airway epithelial cells and mucus", ["Fibrin thrombi", "Calcium oxalate", "Amyloid"], "Curschmann spirals are mucus plugs containing sloughed epithelium."),
        q("easy", "Charcot-Leyden crystals are derived from:", "Eosinophil granule proteins", ["Neutrophil nuclei", "Red cell membranes", "Platelet granules"], "They are formed from eosinophil breakdown products."),
        q("easy", "Cystic fibrosis is caused by mutations in:", "CFTR chloride channel", ["Surfactant protein B only", "Alpha-1 antitrypsin only", "Factor VIII"], "CFTR mutations impair chloride transport and produce thick secretions."),
        q("moderate", "The classic inflammatory cell in allergic asthma is:", "Eosinophil", ["Plasma cell only", "Megakaryocyte", "Osteoclast"], "Type 2 inflammation recruits eosinophils in allergic asthma."),
        q("moderate", "Airway remodeling in asthma includes:", "Smooth muscle hypertrophy and basement membrane thickening", ["Alveolar septal destruction only", "Pleural calcified plaques", "Pulmonary arterial atherosclerosis"], "Chronic asthma causes structural thickening of airway walls."),
        q("moderate", "The most common lethal pulmonary complication of cystic fibrosis is:", "Chronic bronchopulmonary infection", ["Lobar emphysema only", "Pleural mesothelioma", "Pulmonary hamartoma"], "Thick secretions promote persistent infection and bronchiectasis."),
        q("moderate", "Bronchiolitis obliterans refers to:", "Fibrotic narrowing or obliteration of small airways", ["Acute pulmonary edema", "Pleural air leakage only", "Cancer of bronchial glands"], "Small airway injury can heal by luminal fibrosis and obstruction."),
        q("high", "A child has episodic wheezing, cough, and dyspnea after allergen exposure. Sputum contains Curschmann spirals and Charcot-Leyden crystals, and biopsy shows eosinophilic inflammation. Which disease is most likely?", "Atopic asthma", ["Chronic bronchitis", "Bronchiectasis", "Idiopathic pulmonary fibrosis"], "Asthma causes reversible bronchospasm with eosinophilic mucus plugging."),
        q("high", "A teenager has recurrent sinusitis, pancreatic insufficiency, male infertility risk, and chronic Pseudomonas lung infection with thick tenacious mucus. Which molecular defect explains the disease?", "Defective CFTR-mediated chloride transport", ["Defective spectrin anchoring", "Excess alpha-1 antitrypsin", "Factor IX deficiency"], "CFTR mutations cause dehydrated secretions and multisystem cystic fibrosis."),
        q("high", "After lung transplantation, a patient develops progressive airflow obstruction. Biopsy from small airways shows submucosal fibrosis narrowing bronchioles rather than alveolar septal fibrosis. Which lesion is present?", "Bronchiolitis obliterans", ["Diffuse alveolar damage", "Pulmonary alveolar proteinosis", "Asbestosis"], "Bronchiolitis obliterans is an obstructive small-airway fibrosing lesion."),
    ]),
    ("interstitial", "Restrictive and Interstitial Lung Diseases", [
        q("easy", "Restrictive lung disease is characterized by reduced:", "Total lung capacity", ["Platelet count", "Serum ferritin only", "Airway mucus glands only"], "Restriction reduces lung expansion and lung volumes."),
        q("easy", "Idiopathic pulmonary fibrosis shows the histologic pattern called:", "Usual interstitial pneumonia", ["Diffuse alveolar damage only", "Lobar pneumonia", "Bronchiectasis"], "UIP is the pattern underlying most idiopathic pulmonary fibrosis."),
        q("easy", "Sarcoidosis is characterized by:", "Noncaseating granulomas", ["Caseating granulomas only", "Auer rods", "Hyaline membranes"], "Sarcoidosis forms noncaseating granulomas in lung and lymph nodes."),
        q("moderate", "Honeycomb lung refers to:", "Cystic fibrotic end-stage remodeling of lung", ["Acute alveolar edema", "Dilated pulmonary arteries only", "Pleural cholesterol plaques"], "Advanced interstitial fibrosis creates cystic airspaces lined by bronchiolar epithelium."),
        q("moderate", "Temporal heterogeneity is a feature of:", "Usual interstitial pneumonia", ["Lobar pneumonia", "Acute bronchitis", "Pulmonary embolism"], "UIP has patchy fibrosis of different ages."),
        q("moderate", "Hypersensitivity pneumonitis is caused by:", "Immune reaction to inhaled organic antigens", ["Alpha-1 antitrypsin loss", "CFTR mutation", "Platelet autoantibodies"], "Repeated exposure to organic dusts can produce immune-mediated interstitial disease."),
        q("moderate", "Goodpasture syndrome involves antibodies against:", "Basement membrane collagen in lung and kidney", ["Surfactant protein", "Bronchial cartilage", "Pleural mesothelium"], "Anti-GBM antibodies cause pulmonary hemorrhage and glomerulonephritis."),
        q("high", "An older adult has progressive dyspnea, dry cough, bibasilar crackles, clubbing, and CT showing subpleural lower-lobe fibrosis with honeycombing. Biopsy shows patchy fibroblastic foci. Which diagnosis is most likely?", "Idiopathic pulmonary fibrosis", ["Sarcoidosis", "Asthma", "Pulmonary edema"], "IPF shows UIP with patchy subpleural fibrosis and fibroblastic foci."),
        q("high", "A young adult has bilateral hilar lymphadenopathy, skin nodules, uveitis, and lung biopsy with tight noncaseating granulomas but no organisms. Which systemic disease best fits?", "Sarcoidosis", ["Tuberculosis", "Histoplasmosis", "Hypersensitivity pneumonitis"], "Sarcoidosis commonly involves lung, hilar nodes, skin, and eyes."),
        q("high", "A farmer develops dyspnea, cough, and fever hours after handling moldy hay. Biopsy shows interstitial pneumonitis with poorly formed granulomas after repeated antigen exposure. Which disorder is likely?", "Hypersensitivity pneumonitis", ["Usual interstitial pneumonia", "Silicosis", "Chronic bronchitis"], "Organic antigen exposure can cause hypersensitivity pneumonitis."),
    ]),
    ("vascular", "Pulmonary Vascular Disease and Pulmonary Hypertension", [
        q("easy", "Most pulmonary emboli arise from thrombi in:", "Deep leg veins", ["Pulmonary capillaries", "Bronchial arteries", "Pleural lymphatics"], "Deep venous thrombosis is the usual source of pulmonary embolism."),
        q("easy", "Pulmonary hypertension causes hypertrophy of the:", "Right ventricle", ["Left atrium only", "Thymus", "Spleen"], "High pulmonary vascular resistance causes right ventricular pressure overload."),
        q("easy", "Cor pulmonale means right heart disease due to:", "Pulmonary hypertension from lung or pulmonary vascular disease", ["Systemic hypertension", "Mitral stenosis only", "Aortic dissection"], "Cor pulmonale excludes primary left heart disease as the cause."),
        q("moderate", "A saddle embolus lodges at the:", "Bifurcation of the main pulmonary artery", ["Carina of the trachea", "Left atrial appendage", "Aortic valve"], "A large embolus can straddle the pulmonary artery bifurcation."),
        q("moderate", "Pulmonary infarcts are usually:", "Hemorrhagic and wedge-shaped", ["Pale and round", "Cavitary in every case", "Nonhemorrhagic because lungs lack blood"], "Dual blood supply and loose tissue make pulmonary infarcts hemorrhagic."),
        q("moderate", "Plexiform lesions are associated with:", "Severe pulmonary arterial hypertension", ["Mild asthma", "Acute bronchitis", "Lobar pneumonia only"], "Plexiform vascular proliferations occur in advanced pulmonary hypertension."),
        q("moderate", "Fat embolism syndrome often follows:", "Long bone fracture", ["Vitamin B12 deficiency", "H. pylori gastritis", "CFTR mutation"], "Marrow fat can enter circulation after fractures."),
        q("high", "A postoperative patient suddenly develops dyspnea, pleuritic chest pain, hemoptysis, and a wedge-shaped hemorrhagic infarct at the lung periphery. Which event most likely caused it?", "Pulmonary thromboembolism", ["Bronchopneumonia", "Asthma attack", "Sarcoidosis"], "Pulmonary emboli can obstruct peripheral vessels and produce hemorrhagic infarcts."),
        q("high", "A patient with long-standing COPD develops pulmonary hypertension, right ventricular hypertrophy, peripheral edema, and hepatic congestion. The left ventricle is not primarily diseased. Which diagnosis fits?", "Cor pulmonale", ["Left-sided heart failure", "Aortic stenosis", "Restrictive cardiomyopathy"], "Chronic lung disease can cause pulmonary vascular resistance and right heart failure."),
        q("high", "A patient with idiopathic pulmonary arterial hypertension has small muscular pulmonary arteries showing medial hypertrophy, intimal fibrosis, and complex plexiform lesions. Which hemodynamic abnormality drives these changes?", "Sustained elevation of pulmonary arterial pressure", ["Low pulmonary venous pressure", "Acute airway mucus plugging", "Pleural cavity obstruction"], "Severe pulmonary hypertension remodels pulmonary arteries."),
    ]),
    ("pneumonia", "Pneumonia and Acute Pulmonary Infections", [
        q("easy", "Lobar pneumonia typically involves:", "Most or all of one lobe", ["Only terminal bronchioles", "Only pleura", "Only pulmonary arteries"], "Lobar pneumonia produces confluent consolidation of a lobe."),
        q("easy", "Bronchopneumonia is characterized by:", "Patchy suppurative consolidation centered on bronchioles", ["Diffuse alveolar wall fibrosis", "Noncaseating granulomas", "Pleural plaques only"], "Bronchopneumonia is a patchy acute bacterial infection."),
        q("easy", "Atypical pneumonia primarily involves:", "Interstitial inflammation", ["Large airway cartilage", "Pleural mesothelium only", "Pulmonary arteries only"], "Viral and mycoplasmal pneumonias often inflame alveolar septa."),
        q("moderate", "The classic stages of lobar pneumonia include:", "Congestion, red hepatization, gray hepatization, and resolution", ["Necrosis, granuloma, fibrosis, calcification only", "Edema, asthma, emphysema, abscess", "Thrombosis, infarction, embolization, scar"], "Lobar pneumonia has a traditional sequence of gross changes."),
        q("moderate", "Streptococcus pneumoniae classically causes:", "Lobar pneumonia", ["Primary atypical pneumonia only", "Asbestosis", "Mesothelioma"], "Pneumococcus is a common cause of community-acquired lobar pneumonia."),
        q("moderate", "Klebsiella pneumonia is associated with:", "Currant jelly sputum", ["Rust-colored urine", "Charcot-Leyden crystals only", "Howell-Jolly bodies"], "Klebsiella can cause thick bloody mucoid sputum."),
        q("moderate", "Viral pneumonia often shows:", "Mononuclear interstitial infiltrates", ["Massive neutrophilic alveolar exudate only", "Pleural plaques", "Silicotic nodules"], "Viral infections mainly affect alveolar septa and interstitium."),
        q("high", "An alcoholic patient develops severe lobar pneumonia with thick currant jelly sputum, necrosis, and a bulging fissure on imaging. Which organism is classically implicated?", "Klebsiella pneumoniae", ["Mycoplasma pneumoniae", "Pneumocystis jirovecii", "Mycobacterium tuberculosis"], "Klebsiella causes necrotizing pneumonia in debilitated or alcoholic patients."),
        q("high", "A young adult has fever, dry cough, and patchy bilateral infiltrates, but the alveoli contain little exudate. Histology shows mononuclear inflammation in alveolar septa. Which pattern is present?", "Atypical pneumonia", ["Lobar pneumonia", "Bronchiectasis", "Pulmonary abscess"], "Atypical pneumonia is an interstitial pneumonitis, often from viruses or Mycoplasma."),
        q("high", "An elderly hospitalized patient develops patchy lower-lobe consolidations around bronchioles. Microscopy shows neutrophil-rich exudate filling bronchi, bronchioles, and adjacent alveoli. Which pattern is this?", "Bronchopneumonia", ["Lobar pneumonia", "Interstitial fibrosis", "Pulmonary embolism"], "Bronchopneumonia is patchy, bronchiolocentric, and suppurative."),
    ]),
    ("tb-abscess", "Tuberculosis, Lung Abscess, and Opportunistic Infections", [
        q("easy", "Primary tuberculosis usually produces:", "Ghon focus with hilar lymph node involvement", ["Diffuse alveolar damage only", "Pleural mesothelioma", "Pulmonary embolus"], "The Ghon complex includes parenchymal focus and draining nodes."),
        q("easy", "Reactivation tuberculosis classically favors the:", "Lung apices", ["Costophrenic angle only", "Right middle lobe only", "Pleural surface only"], "High oxygen tension favors apical reactivation."),
        q("easy", "Lung abscess means:", "Localized suppurative necrosis of lung parenchyma", ["Noncaseating granuloma", "Alveolar wall thickening only", "Pleural fibrosis only"], "A lung abscess is a cavity caused by tissue destruction and pus."),
        q("moderate", "Caseating granulomas are typical of:", "Tuberculosis", ["Asthma", "Emphysema", "Pulmonary edema"], "TB commonly causes granulomas with central caseous necrosis."),
        q("moderate", "Miliary tuberculosis results from:", "Hematogenous dissemination of mycobacteria", ["Pure bronchial mucus plugging", "Pleural air leak", "Pulmonary venous congestion"], "Bloodstream spread produces innumerable small lesions."),
        q("moderate", "Aspiration is a major cause of lung abscess in:", "Patients with impaired consciousness", ["Patients with isolated iron deficiency", "Patients with hypertension only", "Patients with hemophilia A"], "Aspiration of oropharyngeal material introduces anaerobic bacteria."),
        q("moderate", "Pneumocystis jirovecii pneumonia is especially seen in:", "Immunocompromised patients with low CD4 counts", ["Healthy marathon runners only", "Patients with polycythemia vera only", "Patients with kidney stones"], "PJP is an opportunistic infection in AIDS and other immunodeficiencies."),
        q("high", "A patient from a TB-endemic area has chronic cough, weight loss, night sweats, hemoptysis, and cavitary apical lesions. Biopsy shows caseating granulomas with acid-fast bacilli. Which diagnosis is most likely?", "Reactivation tuberculosis", ["Primary atypical pneumonia", "Sarcoidosis", "Pulmonary hamartoma"], "Reactivation TB commonly affects apices and cavitates."),
        q("high", "An unconscious patient aspirates gastric and oropharyngeal contents, then develops fever and foul-smelling sputum. Imaging shows a cavitary lesion with an air-fluid level in a dependent lung segment. Which complication occurred?", "Lung abscess", ["Pulmonary infarct", "Bronchial carcinoid", "ARDS"], "Aspiration pneumonia can progress to anaerobic lung abscess."),
        q("high", "An AIDS patient with very low CD4 count develops fever, dry cough, dyspnea, diffuse bilateral infiltrates, and foamy intra-alveolar exudate containing cyst forms on silver stain. Which infection is likely?", "Pneumocystis jirovecii pneumonia", ["Klebsiella pneumonia", "Reactivation tuberculosis", "Aspergilloma only"], "PJP causes diffuse interstitial pneumonia with foamy alveolar exudate in immunocompromised patients."),
    ]),
    ("tumors", "Lung Tumors and Carcinogenesis", [
        q("easy", "The strongest risk factor for lung carcinoma is:", "Cigarette smoking", ["Vitamin C deficiency", "Alpha-thalassemia", "Hemophilia"], "Smoking is the major cause of lung cancer."),
        q("easy", "Adenocarcinoma is the lung cancer type most common in:", "Nonsmokers", ["Only asbestos workers", "Only children", "Only patients with TB"], "Adenocarcinoma is the most common lung cancer in nonsmokers and women."),
        q("easy", "Small cell carcinoma is a:", "High-grade neuroendocrine carcinoma", ["Benign cartilage tumor", "Low-grade mesothelial tumor", "Reactive granuloma"], "Small cell carcinoma is an aggressive neuroendocrine tumor."),
        q("moderate", "Squamous cell carcinoma of lung is classically associated with:", "Keratinization and intercellular bridges", ["Mucin-producing glands only", "Neuroendocrine granules only", "Cartilage and fat"], "Squamous differentiation includes keratin pearls and intercellular bridges."),
        q("moderate", "Pancoast tumor can cause:", "Horner syndrome from sympathetic chain involvement", ["Nephrotic syndrome in every case", "Macrocytic anemia", "DIC only"], "Apical tumors may invade brachial plexus and sympathetic chain."),
        q("moderate", "Small cell carcinoma is strongly associated with:", "Paraneoplastic ACTH or ADH production", ["AFP secretion", "Intrinsic factor secretion", "ADAMTS13 excess"], "Small cell carcinoma can cause Cushing syndrome or SIADH."),
        q("moderate", "Carcinoid tumor of lung is derived from:", "Neuroendocrine cells", ["Pleural mesothelium only", "Alveolar macrophages", "Bronchial cartilage"], "Carcinoids are low-grade neuroendocrine tumors."),
        q("high", "A peripheral lung mass in a nonsmoking woman forms glandular structures and produces mucin. Molecular testing reveals an EGFR mutation. Which lung carcinoma type is most likely?", "Adenocarcinoma", ["Squamous cell carcinoma", "Small cell carcinoma", "Typical carcinoid"], "Adenocarcinoma is often peripheral, mucin-producing, and may have targetable mutations."),
        q("high", "A central hilar lung tumor in a smoker is composed of cells with scant cytoplasm, finely granular chromatin, nuclear molding, and extensive necrosis. The patient has hyponatremia from SIADH. Which tumor is likely?", "Small cell carcinoma", ["Adenocarcinoma", "Squamous papilloma", "Pulmonary hamartoma"], "Small cell carcinoma is a central aggressive neuroendocrine tumor with paraneoplastic syndromes."),
        q("high", "A smoker has a central cavitary lung mass. Biopsy shows malignant cells forming keratin pearls with intercellular bridges, and serum calcium is elevated due to PTH-related peptide. Which cancer fits?", "Squamous cell carcinoma", ["Adenocarcinoma", "Large cell neuroendocrine carcinoma", "Mesothelioma"], "Squamous cell carcinoma is smoking-associated, central, and can produce PTHrP."),
    ]),
    ("pleura", "Pleural Disease, Pneumothorax, and Mesothelioma", [
        q("easy", "Pleural effusion means accumulation of fluid in the:", "Pleural cavity", ["Alveolar septa", "Bronchial lumen", "Pulmonary arteries"], "Fluid can collect between visceral and parietal pleura."),
        q("easy", "Pneumothorax means air in the:", "Pleural space", ["Alveolar capillary membrane", "Pulmonary vein", "Bronchial cartilage"], "Air in the pleural cavity can collapse the lung."),
        q("easy", "Malignant mesothelioma is strongly associated with:", "Asbestos exposure", ["Silica alone", "Radon only", "Coal dust only"], "Asbestos exposure greatly increases mesothelioma risk."),
        q("moderate", "A transudative pleural effusion is commonly caused by:", "Congestive heart failure", ["Bacterial pneumonia only", "Mesothelioma only", "Pulmonary infarct only"], "Hydrostatic pressure elevation produces transudates."),
        q("moderate", "An exudative pleural effusion suggests:", "Inflammation, infection, or malignancy", ["Pure hydrostatic pressure only", "Low protein in every case", "No pleural disease"], "Exudates are protein-rich and occur with increased vascular permeability."),
        q("moderate", "Tension pneumothorax is dangerous because it:", "Shifts mediastinum and impairs venous return", ["Improves oxygenation", "Prevents lung collapse", "Only affects red cells"], "Pressure builds in the pleural cavity and compromises circulation."),
        q("moderate", "Pleural plaques from asbestos exposure most often involve:", "Parietal pleura", ["Bronchial mucosa", "Alveolar macrophages only", "Pulmonary veins"], "Asbestos-related plaques are fibrous lesions of parietal pleura."),
        q("high", "A tall young man develops sudden pleuritic chest pain and dyspnea. Imaging shows air in the pleural space with collapse of the ipsilateral lung but no mediastinal shift. Which condition is present?", "Spontaneous pneumothorax", ["Pleural effusion", "Pulmonary edema", "Bronchiectasis"], "Rupture of apical blebs can cause spontaneous pneumothorax."),
        q("high", "A ventilated trauma patient suddenly becomes hypotensive with tracheal deviation, distended neck veins, and absent breath sounds on one side. Air is trapped under pressure in the pleural space. What is the diagnosis?", "Tension pneumothorax", ["Simple pleural effusion", "Lobar pneumonia", "Pulmonary embolism"], "Tension pneumothorax compresses mediastinal structures and impairs venous return."),
        q("high", "A retired shipyard worker develops diffuse pleural thickening encasing the lung. Biopsy shows malignant mesothelial cells, and he has a remote history of asbestos exposure. Which tumor is most likely?", "Malignant mesothelioma", ["Adenocarcinoma of lung", "Pulmonary hamartoma", "Bronchial carcinoid"], "Mesothelioma is a malignant tumor of mesothelial cells linked to asbestos."),
    ]),
    ("pediatric-occupational", "Neonatal, Pediatric, Occupational, and Environmental Lung Disease", [
        q("easy", "Neonatal respiratory distress syndrome is caused by deficiency of:", "Surfactant", ["Hemoglobin", "Intrinsic factor", "Platelets"], "Premature type II pneumocytes may produce insufficient surfactant."),
        q("easy", "Surfactant is produced by:", "Type II pneumocytes", ["Type I pneumocytes", "Alveolar macrophages only", "Endothelial cells only"], "Type II pneumocytes synthesize and secrete surfactant."),
        q("easy", "Coal worker pneumoconiosis results from inhalation of:", "Coal dust", ["Asbestos fibers", "Beryllium", "Organic mold"], "Coal dust inhalation causes coal macules and progressive massive fibrosis in severe cases."),
        q("moderate", "Hyaline membrane disease occurs because surfactant deficiency causes:", "Alveolar collapse and epithelial injury", ["Pleural plaque formation", "Pulmonary emboli", "Granulomatous lymphadenitis"], "High surface tension causes atelectasis and damage, forming hyaline membranes."),
        q("moderate", "Asbestosis classically begins in the:", "Lower lung lobes and subpleural regions", ["Upper lobes around bronchioles only", "Pleural cavity only", "Trachea only"], "Asbestos-related interstitial fibrosis often starts subpleurally in lower lobes."),
        q("moderate", "Silicosis classically affects:", "Upper lung lobes", ["Lower lobes only", "Pleural space only", "Pulmonary veins"], "Silicosis causes upper-lobe silicotic nodules."),
        q("moderate", "Asbestos exposure increases risk of:", "Bronchogenic carcinoma and mesothelioma", ["Only asthma", "Only TB", "Only pulmonary embolism"], "Asbestos increases carcinoma risk especially with smoking and causes mesothelioma."),
        q("high", "A premature infant develops tachypnea, grunting, hypoxemia, and diffuse atelectasis shortly after birth. Autopsy would show collapsed alveoli lined by protein-rich hyaline membranes. Which mechanism is central?", "Surfactant deficiency", ["CFTR mutation", "Pulmonary thromboembolism", "Asbestos exposure"], "Surfactant deficiency increases alveolar surface tension and causes neonatal RDS."),
        q("high", "A sandblaster develops progressive dyspnea. Imaging shows upper-lobe nodules with eggshell calcification of hilar lymph nodes, and polarized microscopy reveals birefringent particles. Which pneumoconiosis is most likely?", "Silicosis", ["Asbestosis", "Coal worker pneumoconiosis", "Berylliosis"], "Silica exposure causes upper-lobe fibrotic nodules and eggshell nodal calcification."),
        q("high", "A construction worker with many years of asbestos exposure develops progressive dyspnea, lower-lobe interstitial fibrosis, ferruginous bodies, and calcified pleural plaques on imaging. Which occupational lung disease is present?", "Asbestosis", ["Silicosis", "Byssinosis", "Hypersensitivity pneumonitis"], "Asbestos causes lower-lobe fibrosis with asbestos bodies and pleural plaques."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch15-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 15 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch15-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 15 questions")
    print(f"Removed {total_removed} existing Chapter 15 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 15 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
