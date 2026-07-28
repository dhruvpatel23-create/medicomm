import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Head and Neck"
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
    ("oral-reactive", "Oral Cavity: Reactive, Inflammatory, and Premalignant Lesions", [
        q("easy", "Leukoplakia is best defined as:", "A white oral plaque that cannot be scraped off or otherwise diagnosed", ["A red vascular tumor", "A cyst of salivary origin", "A congenital thyroid remnant"], "Leukoplakia is a clinical term for a persistent white patch with malignant potential."),
        q("easy", "Erythroplakia has a higher risk of:", "Severe dysplasia or carcinoma", ["Fibrous ankylosis", "Benign lipoma", "Odontoma only"], "Red velvety oral patches are more likely than leukoplakia to show severe dysplasia."),
        q("easy", "Aphthous ulcers are commonly:", "Painful shallow recurrent oral ulcers", ["Keratin-filled jaw cysts", "Malignant salivary tumors", "Vocal cord nodules"], "Aphthous ulcers are recurrent painful mucosal ulcerations."),
        q("moderate", "Oral squamous dysplasia is graded based on:", "Extent and severity of epithelial atypia", ["Depth of salivary duct dilation", "Number of tooth roots", "Middle ear ossicle erosion"], "Dysplasia reflects disordered epithelial maturation and cytologic atypia."),
        q("moderate", "The strongest traditional risk factors for oral squamous cell carcinoma are:", "Tobacco and alcohol", ["Low salt intake and exercise", "Iron supplementation", "Vaccination alone"], "Tobacco and alcohol synergistically increase oral cancer risk."),
        q("moderate", "Oral hairy leukoplakia is associated with:", "Epstein-Barr virus in immunosuppressed patients", ["HPV-16 in every patient", "Candida invasion of bone", "Asbestos exposure"], "EBV causes corrugated white tongue plaques in immunocompromised patients."),
        q("moderate", "Candidiasis in the oral cavity commonly produces:", "White plaques that can be scraped off", ["A midline neck cyst", "A blue submucosal vascular tumor", "An ossifying jaw mass only"], "Thrush forms removable white pseudomembranes."),
        q("high", "A smoker has a persistent white plaque on the lateral tongue that cannot be scraped off. Biopsy shows epithelial dysplasia but no invasion through the basement membrane. Which clinical lesion is this?", "Leukoplakia", ["Candidiasis", "Mucocele", "Ranula"], "Leukoplakia is a persistent white plaque and may harbor dysplasia."),
        q("high", "A patient has a red, velvety oral patch on the floor of mouth. Biopsy shows severe epithelial dysplasia approaching carcinoma in situ. Which clinical lesion has the highest malignant potential?", "Erythroplakia", ["Fibroma", "Oral hairy leukoplakia", "Aphthous ulcer"], "Erythroplakia is uncommon but frequently dysplastic or malignant."),
        q("high", "An HIV-positive patient develops corrugated white plaques along the lateral tongue. The plaques do not scrape off, and epithelial cells contain EBV-related changes without invasive carcinoma. Which diagnosis fits?", "Oral hairy leukoplakia", ["Thrush", "Erythroplakia", "Pleomorphic adenoma"], "Oral hairy leukoplakia is EBV-associated and seen in immunosuppression."),
    ]),
    ("oral-cancer", "Oral Cavity and Oropharyngeal Squamous Cell Carcinoma", [
        q("easy", "The most common malignancy of the oral cavity is:", "Squamous cell carcinoma", ["Adenoid cystic carcinoma", "Pleomorphic adenoma", "Ameloblastoma"], "Most oral cancers are squamous cell carcinomas."),
        q("easy", "HPV-associated oropharyngeal carcinoma is most strongly linked to:", "HPV-16", ["EBV only", "HHV-8", "HSV-1 only"], "High-risk HPV-16 drives many tonsillar and base-of-tongue cancers."),
        q("easy", "Keratin pearls suggest:", "Squamous differentiation", ["Mucinous glandular differentiation", "Neuroendocrine differentiation", "Lymphoid hyperplasia"], "Keratin pearl formation is a feature of well-differentiated squamous carcinoma."),
        q("moderate", "HPV-positive oropharyngeal carcinoma commonly overexpresses:", "p16", ["BCL2 from t(14;18)", "Cyclin D1 from t(11;14)", "PML-RARA"], "p16 is used as a surrogate marker of transcriptionally active high-risk HPV."),
        q("moderate", "The common sites for HPV-positive oropharyngeal carcinoma include:", "Tonsil and base of tongue", ["Middle ear and mastoid", "Parotid tail only", "Thyroglossal duct"], "HPV-related tumors often arise in lymphoid-rich oropharyngeal sites."),
        q("moderate", "Tobacco-associated oral squamous cell carcinoma often shows:", "TP53 mutation and field cancerization", ["CFTR mutation", "PIGA mutation", "JAK2 mutation"], "Carcinogen exposure creates widespread genetically altered mucosa."),
        q("moderate", "Cervical lymph node metastasis in oral cancer indicates:", "More advanced disease and worse prognosis", ["Benign reactive disease only", "Cure without treatment", "Absence of invasion"], "Nodal spread is a major prognostic factor in head and neck SCC."),
        q("high", "A heavy smoker and drinker has a nonhealing ulcer on the floor of mouth. Biopsy shows invasive nests of atypical squamous cells with keratin pearls extending into stroma. Which diagnosis is most likely?", "Oral squamous cell carcinoma", ["Leukoplakia without invasion", "Pleomorphic adenoma", "Aphthous ulcer"], "Invasive keratinizing squamous carcinoma is strongly associated with tobacco and alcohol."),
        q("high", "A younger nonsmoking patient has a tonsillar mass and cystic cervical node metastasis. Tumor cells are p16-positive, and HPV-16 DNA is detected. Compared with tobacco-related tumors, which category fits?", "HPV-associated oropharyngeal squamous cell carcinoma", ["EBV-associated nasopharyngeal carcinoma", "Mucoepidermoid carcinoma", "Laryngeal papilloma"], "HPV-positive oropharyngeal SCC often presents with nodal disease and has distinct biology."),
        q("high", "A patient treated for oral squamous carcinoma later develops a second independent tumor in nearby mucosa. Multiple epithelial areas were genetically damaged by tobacco carcinogens. Which concept explains this?", "Field cancerization", ["Tumor lysis syndrome", "Contiguous granulomatous spread", "Metastasis to salivary duct"], "Field cancerization means broad mucosal exposure creates multiple premalignant clones."),
    ]),
    ("odontogenic", "Odontogenic Cysts and Tumors", [
        q("easy", "A dentigerous cyst is associated with:", "Crown of an unerupted tooth", ["Root apex of a nonvital tooth", "Parotid duct", "Thyroglossal tract"], "Dentigerous cysts surround the crown of an unerupted tooth."),
        q("easy", "A radicular cyst is usually related to:", "Inflammation at the apex of a nonvital tooth", ["HPV infection", "Salivary gland duct obstruction", "Middle ear cholesteatoma"], "Radicular cysts arise from periapical inflammation."),
        q("easy", "Ameloblastoma is an odontogenic tumor that is:", "Locally aggressive", ["Always metastatic", "A benign salivary gland tumor", "A laryngeal lesion"], "Ameloblastoma is benign but infiltrative and recurrent if incompletely excised."),
        q("moderate", "Odontogenic keratocyst is notable for:", "High recurrence and association with PTCH pathway defects", ["EBV infection", "Asbestos exposure", "Factor VIII deficiency"], "Odontogenic keratocysts can recur and occur in nevoid basal cell carcinoma syndrome."),
        q("moderate", "The lining of odontogenic keratocyst often shows:", "Parakeratinized stratified squamous epithelium", ["Respiratory epithelium with cilia", "Oncocytic epithelium", "Mesothelium"], "A corrugated parakeratinized lining is characteristic."),
        q("moderate", "Ameloblastoma most often arises in the:", "Mandible", ["Parotid gland", "Nasopharynx", "Larynx"], "The posterior mandible is a common location."),
        q("moderate", "Compound odontoma is composed of:", "Multiple tooth-like structures", ["Sheets of plasma cells", "Keratin pearls only", "Malignant glandular cells"], "Compound odontomas contain miniature tooth-like structures."),
        q("high", "A young adult has a multilocular radiolucent mandibular lesion described as soap-bubble on imaging. Histology shows odontogenic epithelium resembling enamel organ. The lesion is benign but locally invasive. Which tumor is likely?", "Ameloblastoma", ["Radicular cyst", "Pleomorphic adenoma", "Nasopharyngeal carcinoma"], "Ameloblastoma is a locally aggressive odontogenic epithelial tumor."),
        q("high", "A patient has multiple jaw cysts, basal cell carcinomas, and skeletal anomalies. A jaw lesion shows parakeratinized odontogenic epithelium and tends to recur after removal. Which cyst is most likely?", "Odontogenic keratocyst", ["Dentigerous cyst", "Mucocele", "Branchial cleft cyst"], "Multiple odontogenic keratocysts suggest PTCH-related nevoid basal cell carcinoma syndrome."),
        q("high", "A child has a radiopaque jaw lesion made of numerous small tooth-like structures that interfere with eruption of a permanent tooth. Which odontogenic lesion best fits?", "Compound odontoma", ["Ameloblastoma", "Adenoid cystic carcinoma", "Warthin tumor"], "Compound odontomas are hamartomatous odontogenic lesions with tooth-like elements."),
    ]),
    ("salivary-benign", "Salivary Glands: Inflammation and Benign Tumors", [
        q("easy", "The most common salivary gland tumor is:", "Pleomorphic adenoma", ["Warthin tumor", "Mucoepidermoid carcinoma", "Adenoid cystic carcinoma"], "Pleomorphic adenoma is the most common salivary gland neoplasm."),
        q("easy", "Pleomorphic adenoma most commonly involves the:", "Parotid gland", ["Sublingual gland", "Minor glands only", "Thyroid gland"], "Most pleomorphic adenomas arise in the parotid."),
        q("easy", "A mucocele is caused by:", "Extravasation or retention of salivary mucus", ["HPV infection", "Tooth root inflammation", "EBV infection"], "Mucoceles commonly follow trauma to minor salivary ducts."),
        q("moderate", "Pleomorphic adenoma contains:", "Epithelial and myoepithelial elements in chondromyxoid stroma", ["Only keratinizing squamous nests", "Only lymphoid follicles", "Only necrotizing granulomas"], "Mixed epithelial and stromal-like components give pleomorphic appearance."),
        q("moderate", "Warthin tumor is strongly associated with:", "Smoking", ["Alcohol alone", "HPV-16", "Parvovirus B19"], "Warthin tumor is a smoking-associated benign parotid tumor."),
        q("moderate", "Warthin tumor histology shows:", "Papillary cystic oncocytic epithelium with lymphoid stroma", ["Cribriform glands with perineural invasion", "Sheets of small blue cells", "Keratin pearls invading muscle"], "Warthin tumor has oncocytic epithelium and lymphoid stroma."),
        q("moderate", "Sialolithiasis most commonly affects the:", "Submandibular gland", ["Lacrimal gland", "Thyroid gland", "Thymus"], "Submandibular ducts are long and mucin-rich, favoring stones."),
        q("high", "A slow-growing painless parotid mass is excised. Histology shows ductal epithelial and myoepithelial cells embedded in a chondromyxoid matrix. Incomplete excision risks recurrence. Which tumor is most likely?", "Pleomorphic adenoma", ["Warthin tumor", "Mucoepidermoid carcinoma", "Adenoid cystic carcinoma"], "Pleomorphic adenoma is a benign mixed tumor with chondromyxoid stroma."),
        q("high", "An older male smoker has a cystic parotid mass. Biopsy shows papillary oncocytic epithelium lining cystic spaces with dense lymphoid stroma and germinal centers. Which diagnosis fits?", "Warthin tumor", ["Pleomorphic adenoma", "Mucoepidermoid carcinoma", "Sialadenitis only"], "Warthin tumor is a benign smoking-associated parotid tumor."),
        q("high", "A patient has painful swelling under the jaw that worsens at mealtime. Imaging shows a calcified stone obstructing Wharton duct with secondary inflammation. Which process is present?", "Submandibular sialolithiasis", ["Ranula from sublingual gland", "Parotid pleomorphic adenoma", "Branchial cleft cyst"], "Salivary stones commonly obstruct submandibular ducts and cause meal-related pain."),
    ]),
    ("salivary-malignant", "Malignant Salivary Gland Tumors", [
        q("easy", "The most common malignant salivary gland tumor is:", "Mucoepidermoid carcinoma", ["Pleomorphic adenoma", "Warthin tumor", "Lipoma"], "Mucoepidermoid carcinoma is the most common salivary gland malignancy."),
        q("easy", "Adenoid cystic carcinoma is known for:", "Perineural invasion", ["Benign lymphoid stroma", "Tooth-like structures", "Reversible bronchospasm"], "Adenoid cystic carcinoma often tracks along nerves and causes pain."),
        q("easy", "Acinic cell carcinoma shows differentiation toward:", "Serous acinar cells", ["Squamous keratinocytes only", "Melanocytes", "Thyroid follicular cells"], "Acinic cell carcinoma resembles serous acinar differentiation."),
        q("moderate", "Mucoepidermoid carcinoma contains:", "Mucous, squamous, and intermediate cells", ["Only oncocytes", "Only chondromyxoid stroma", "Only lymphocytes"], "This tumor has mixed mucous and squamous elements."),
        q("moderate", "High-grade mucoepidermoid carcinoma is more likely to show:", "Solid growth, atypia, and aggressive behavior", ["Pure cystic benign behavior", "No invasion", "Only lymphoid stroma"], "High-grade tumors have more epidermoid cells and worse prognosis."),
        q("moderate", "Adenoid cystic carcinoma often has a:", "Cribriform pattern", ["Starry-sky pattern", "Fish-mouth stenosis", "Honeycomb lung pattern"], "Cribriform architecture creates pseudocystic spaces."),
        q("moderate", "Carcinoma ex pleomorphic adenoma arises from:", "Malignant transformation in a pleomorphic adenoma", ["A radicular cyst", "A Warthin tumor always", "A laryngeal papilloma"], "Long-standing pleomorphic adenoma can undergo malignant transformation."),
        q("high", "A parotid mass is composed of mucin-producing cells, squamoid cells, and intermediate cells. Low-grade areas are cystic, while high-grade areas are solid and invasive. Which salivary malignancy is this?", "Mucoepidermoid carcinoma", ["Adenoid cystic carcinoma", "Pleomorphic adenoma", "Warthin tumor"], "Mucoepidermoid carcinoma has mucous and squamous components."),
        q("high", "A patient has a painful minor salivary gland tumor of the palate. Histology shows cribriform nests of basaloid cells, and tumor tracks along nerves beyond the main mass. Which diagnosis is most likely?", "Adenoid cystic carcinoma", ["Acinic cell carcinoma", "Warthin tumor", "Mucocele"], "Adenoid cystic carcinoma is painful due to perineural invasion and has cribriform architecture."),
        q("high", "A long-standing parotid pleomorphic adenoma suddenly enlarges and becomes painful. Histology shows residual benign mixed tumor next to invasive high-grade carcinoma. Which diagnosis fits?", "Carcinoma ex pleomorphic adenoma", ["Warthin tumor", "Odontogenic keratocyst", "Acinic cell carcinoma only"], "Malignant transformation can occur in a long-standing pleomorphic adenoma."),
    ]),
    ("nasopharynx", "Nasal Cavity, Paranasal Sinuses, and Nasopharynx", [
        q("easy", "Nasopharyngeal carcinoma is strongly associated with:", "Epstein-Barr virus", ["HPV-6 only", "H. pylori", "Hepatitis B"], "EBV is strongly linked to nonkeratinizing nasopharyngeal carcinoma."),
        q("easy", "Sinonasal papilloma associated with local recurrence is:", "Inverted papilloma", ["Squamous papilloma of larynx", "Pleomorphic adenoma", "Odontoma"], "Inverted papilloma grows inward and can recur."),
        q("easy", "Nasal polyps are usually:", "Inflammatory edematous mucosal protrusions", ["Malignant epithelial tumors", "Odontogenic cysts", "Salivary stones"], "Nasal polyps are non-neoplastic inflammatory lesions."),
        q("moderate", "Nasopharyngeal carcinoma commonly presents with:", "Cervical lymph node metastasis", ["Meal-related submandibular pain", "Jaw cysts", "Pleural effusion"], "Nodal metastasis may be the first manifestation."),
        q("moderate", "Undifferentiated nasopharyngeal carcinoma often has:", "Syncytial tumor cells with lymphoid infiltrate", ["Chondromyxoid stroma", "Oncocytic papillae", "Tooth-like structures"], "The tumor has a lymphoepithelioma-like appearance."),
        q("moderate", "Allergic nasal polyps commonly contain:", "Eosinophils", ["Auer rods", "Reed-Sternberg cells", "Asbestos bodies"], "Allergic inflammation recruits eosinophils."),
        q("moderate", "Juvenile nasopharyngeal angiofibroma is a:", "Vascular tumor in adolescent males", ["Salivary gland carcinoma", "Odontogenic cyst", "Middle ear cholesteatoma"], "It is a benign but locally aggressive vascular tumor."),
        q("high", "A patient from southern China has a neck mass. Biopsy of nasopharynx shows nonkeratinizing carcinoma with dense lymphoid infiltrate, and EBV markers are positive. Which cancer is most likely?", "Nasopharyngeal carcinoma", ["HPV-positive tonsillar carcinoma", "Inverted papilloma", "Pleomorphic adenoma"], "EBV-associated nasopharyngeal carcinoma often presents with nodal metastasis."),
        q("high", "A teenage boy has recurrent severe epistaxis and nasal obstruction. Imaging shows a highly vascular nasopharyngeal mass. Biopsy is avoided because of bleeding risk. Which lesion is likely?", "Juvenile nasopharyngeal angiofibroma", ["Nasal polyp", "Nasopharyngeal carcinoma", "Warthin tumor"], "Juvenile nasopharyngeal angiofibroma is a vascular tumor of adolescent males."),
        q("high", "An adult has unilateral nasal obstruction. Pathology shows endophytic growth of squamous epithelium into underlying stroma, and the lesion has recurrence risk plus possible carcinoma association. Which lesion is this?", "Inverted papilloma", ["Inflammatory nasal polyp", "Aphthous ulcer", "Radicular cyst"], "Inverted papilloma is locally aggressive and grows inward."),
    ]),
    ("larynx", "Larynx and Upper Airway Lesions", [
        q("easy", "Vocal cord nodules are commonly associated with:", "Voice overuse", ["EBV infection", "Asbestos exposure", "Salivary stones"], "Singer nodules arise from chronic irritation or voice abuse."),
        q("easy", "Laryngeal papillomas are commonly caused by:", "HPV types 6 and 11", ["EBV", "CMV", "H. pylori"], "Low-risk HPV causes squamous papillomas of the larynx."),
        q("easy", "Most laryngeal cancers are:", "Squamous cell carcinomas", ["Adenocarcinomas", "Melanomas", "Sarcomas"], "The larynx is lined largely by squamous mucosa at key sites."),
        q("moderate", "The major risk factors for laryngeal squamous carcinoma are:", "Tobacco and alcohol", ["Low calcium intake", "Sialolithiasis", "Parvovirus infection"], "Smoking and alcohol are classic risk factors."),
        q("moderate", "True vocal cord tumors often present early because they cause:", "Hoarseness", ["Painless jaundice", "Hematuria", "Jaw expansion"], "Glottic lesions affect phonation early."),
        q("moderate", "Recurrent respiratory papillomatosis may cause:", "Airway obstruction from multiple papillomas", ["Pulmonary emboli", "Pleural plaques", "Sialadenitis"], "Multiple HPV-related papillomas can compromise the airway."),
        q("moderate", "Squamous dysplasia of the larynx can progress to:", "Invasive squamous cell carcinoma", ["Pleomorphic adenoma", "Odontoma", "Warthin tumor"], "Persistent dysplasia may acquire invasive behavior."),
        q("high", "A teacher develops bilateral small nodules on the true vocal cords after years of voice strain. Histology shows reactive fibrous nodules without malignancy. Which lesion is most likely?", "Vocal cord nodules", ["Laryngeal papillomatosis", "Squamous cell carcinoma", "Adenoid cystic carcinoma"], "Vocal cord nodules are reactive lesions from chronic voice abuse."),
        q("high", "A child has recurrent hoarseness and airway symptoms. Laryngoscopy shows multiple exophytic squamous papillomas caused by low-risk HPV, requiring repeated removal. Which condition is present?", "Recurrent respiratory papillomatosis", ["Glottic carcinoma", "Nasopharyngeal carcinoma", "Vocal cord polyp"], "HPV 6/11 can cause recurrent laryngeal papillomatosis in children."),
        q("high", "A smoker has progressive hoarseness. Biopsy of a true vocal cord lesion shows invasive keratinizing squamous cell carcinoma. Why did symptoms appear relatively early?", "Glottic tumors impair vocal cord vibration", ["They always metastasize first", "They obstruct Wharton duct", "They produce EBV viremia"], "Glottic cancers often present with hoarseness before extensive spread."),
    ]),
    ("ear", "Ear and Temporal Bone Disorders", [
        q("easy", "Acute otitis media most often involves infection of the:", "Middle ear", ["External auditory canal only", "Cochlear nerve only", "Parotid gland"], "Otitis media is inflammation and infection of the middle ear space."),
        q("easy", "Cholesteatoma is composed of:", "Keratinizing squamous epithelium and keratin debris", ["Mucinous salivary cells", "Odontogenic epithelium", "Thyroid follicles"], "Despite the name, cholesteatoma is not a cholesterol tumor."),
        q("easy", "Otosclerosis commonly causes:", "Conductive hearing loss", ["Bleeding gums", "Oral leukoplakia", "Jaw cysts"], "Fixation of the stapes impairs sound conduction."),
        q("moderate", "Cholesteatoma can erode bone because of:", "Expanding keratin debris and chronic inflammation", ["Factor VIII deficiency", "CFTR mutation", "Hepcidin excess"], "Cholesteatomas can erode ossicles and temporal bone."),
        q("moderate", "Chronic otitis media can be complicated by:", "Mastoiditis", ["Pleomorphic adenoma", "Sialolithiasis", "Nasopharyngeal angiofibroma"], "Infection can extend into mastoid air cells."),
        q("moderate", "Otosclerosis often involves abnormal remodeling of:", "Otic capsule around stapes footplate", ["Mandibular alveolus", "Parotid duct", "Nasal septum"], "Stapes fixation produces conductive hearing loss."),
        q("moderate", "External otitis is commonly called:", "Swimmer's ear", ["Glue ear", "Cauliflower ear", "Saddle nose"], "Moisture and trauma predispose to external canal infection."),
        q("high", "A patient with chronic ear discharge and hearing loss has a middle ear mass made of keratinizing squamous epithelium with abundant keratin debris. It erodes ossicles. Which diagnosis is most likely?", "Cholesteatoma", ["Acute otitis externa", "Otosclerosis", "Ceruminous adenoma"], "Cholesteatoma is destructive keratinizing squamous epithelium in the middle ear."),
        q("high", "A young adult develops progressive conductive hearing loss. Surgery shows fixation of the stapes footplate due to abnormal bone remodeling of the otic capsule. Which diagnosis fits?", "Otosclerosis", ["Cholesteatoma", "Acute otitis media", "Vestibular schwannoma"], "Otosclerosis fixes the stapes and causes conductive hearing loss."),
        q("high", "A child develops fever and ear pain after an upper respiratory infection. The tympanic membrane is bulging, and bacterial infection fills the middle ear with suppurative exudate. Which disorder is present?", "Acute otitis media", ["Otitis externa", "Cholesteatoma", "Otosclerosis"], "Acute otitis media commonly follows URI and affects the middle ear."),
    ]),
    ("neck-cysts", "Neck Cysts and Developmental Lesions", [
        q("easy", "A thyroglossal duct cyst is usually located in the:", "Midline neck", ["Parotid tail", "Posterior mandible", "External auditory canal"], "Thyroglossal duct remnants lie along the midline thyroid descent path."),
        q("easy", "A branchial cleft cyst is usually located in the:", "Lateral neck", ["Midline tongue base", "Floor of mouth only", "Middle ear"], "Branchial cleft cysts commonly present along the anterior border of the sternocleidomastoid."),
        q("easy", "A ranula is a mucocele of the:", "Floor of mouth", ["Middle ear", "Tonsil", "Nasopharynx"], "Ranula arises from sublingual or minor salivary mucus extravasation."),
        q("moderate", "Thyroglossal duct cysts move with swallowing or tongue protrusion because they are attached to:", "The tract of thyroid descent near the hyoid", ["Parotid duct", "External auditory canal", "Dental follicle"], "They are connected to the tongue base/hyoid region."),
        q("moderate", "Branchial cleft cyst lining may include:", "Squamous or respiratory epithelium with lymphoid tissue", ["Only thyroid follicles", "Only odontogenic epithelium", "Only oncocytes"], "Branchial cleft cysts often have lymphoid tissue in the wall."),
        q("moderate", "The most important adult mimic of a lateral neck cyst is:", "Cystic metastatic squamous cell carcinoma", ["Simple aphthous ulcer", "Sialolithiasis", "Otosclerosis"], "In adults, cystic neck masses must be evaluated for metastatic carcinoma."),
        q("moderate", "Ectopic thyroid tissue can occur at the:", "Base of tongue", ["Middle ear ossicle", "Parotid duct only", "Dental pulp"], "Lingual thyroid results from abnormal thyroid descent."),
        q("high", "A child has a painless midline neck mass that moves upward when the tongue is protruded. Histology shows a cyst lined by respiratory epithelium with thyroid follicles in the wall. Which lesion is most likely?", "Thyroglossal duct cyst", ["Branchial cleft cyst", "Ranula", "Lymphangioma"], "Thyroglossal duct cysts are midline and may contain thyroid tissue."),
        q("high", "A young adult has a fluctuant lateral neck mass near the anterior border of the sternocleidomastoid. The cyst wall has squamous epithelium and prominent lymphoid tissue. Which diagnosis fits?", "Branchial cleft cyst", ["Thyroglossal duct cyst", "Odontogenic keratocyst", "Mucoepidermoid carcinoma"], "Branchial cleft cysts are lateral neck developmental cysts."),
        q("high", "An older adult presents with a new cystic lateral neck mass. Although it resembles a branchial cleft cyst, biopsy reveals p16-positive squamous carcinoma from the oropharynx. What diagnostic pitfall is illustrated?", "Cystic metastatic squamous cell carcinoma can mimic a branchial cleft cyst", ["All lateral cysts are benign", "Thyroglossal duct cysts metastasize routinely", "Ranulas arise from lymph nodes"], "Adult cystic neck masses require exclusion of metastatic HPV-related carcinoma."),
    ]),
    ("tonsil-pharynx", "Tonsils, Pharynx, and Lymphoid Lesions", [
        q("easy", "Tonsillitis is most often caused by:", "Infection of tonsillar lymphoid tissue", ["Salivary stone", "Odontogenic cyst", "Pleural fibrosis"], "Tonsils are lymphoid tissue exposed to oral pathogens."),
        q("easy", "Peritonsillar abscess is also called:", "Quinsy", ["Ranula", "Mucocele", "Cholesteatoma"], "Quinsy is suppurative infection around the tonsil."),
        q("easy", "Waldeyer ring is composed of:", "Pharyngeal lymphoid tissue", ["Salivary ducts", "Jaw cysts", "Middle ear bones"], "Waldeyer ring includes tonsillar lymphoid tissue."),
        q("moderate", "Tonsillar hypertrophy in children often reflects:", "Reactive lymphoid hyperplasia", ["Invasive carcinoma in every case", "Pleomorphic adenoma", "Otosclerosis"], "Children commonly have reactive tonsillar enlargement."),
        q("moderate", "A peritonsillar abscess may cause:", "Uvular deviation and trismus", ["Conductive hearing from stapes fixation", "Meal-related salivary pain", "Cystic jaw expansion"], "Abscess near tonsil can push the uvula and irritate muscles."),
        q("moderate", "Extranodal NK/T-cell lymphoma of nasal type is associated with:", "EBV", ["HPV-6", "H. pylori", "Parvovirus"], "This destructive midline lymphoma is strongly EBV-associated."),
        q("moderate", "Diffuse large B-cell lymphoma can arise in:", "Waldeyer ring", ["Only tooth enamel", "Only parotid ducts", "Only vocal cord lamina propria"], "Waldeyer ring is an extranodal lymphoid site for lymphoma."),
        q("high", "A child with fever, sore throat, muffled voice, trismus, and uvular deviation has a fluctuant swelling adjacent to the tonsil. Which complication of tonsillitis is present?", "Peritonsillar abscess", ["Branchial cleft cyst", "Ranula", "Otosclerosis"], "Peritonsillar abscess produces quinsy with trismus and uvular deviation."),
        q("high", "A patient has a destructive midline nasal lesion. Biopsy shows angioinvasive atypical lymphoid cells with necrosis, and EBV testing is positive. Which lymphoma is most likely?", "Extranodal NK/T-cell lymphoma, nasal type", ["Follicular lymphoma", "Classical Hodgkin lymphoma", "Mantle cell lymphoma"], "Nasal NK/T-cell lymphoma is EBV-associated and angioinvasive."),
        q("high", "An adult has asymmetric tonsillar enlargement. Biopsy shows sheets of large CD20-positive lymphoid cells effacing the normal architecture of Waldeyer ring. Which diagnosis is most likely?", "Diffuse large B-cell lymphoma", ["Reactive tonsillar hyperplasia", "Peritonsillar abscess", "Laryngeal papilloma"], "Waldeyer ring can be involved by aggressive B-cell lymphoma."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch16-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 16 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch16-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 16 questions")
    print(f"Removed {total_removed} existing Chapter 16 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 16 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
