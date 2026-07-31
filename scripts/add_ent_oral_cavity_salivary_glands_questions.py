import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ent"
SUBJECT_TITLE = "ENT"
CHAPTER = "Diseases of Oral Cavity and Salivary Glands"
CHAPTER_ORDER = 3
SOURCE_PDF = "ent 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def punctuate(prompt):
    prompt = prompt.strip()
    if prompt[-1] in ".?!:":
        return prompt
    replacements = [
        (". The most likely diagnosis is", ". What is the most likely diagnosis?"),
        (". The likely diagnosis is", ". What is the likely diagnosis?"),
        (". The next step is", ". What is the next step?"),
        (". The best treatment is", ". What is the best treatment?"),
        (". This suggests", ". What does this suggest?"),
        (". This points toward", ". What does this point toward?"),
        (". The lesion is most likely", ". What is the lesion most likely?"),
    ]
    for old, new in replacements:
        if prompt.endswith(old):
            return f"{prompt[:-len(old)]}{new}"
    if prompt.lower().endswith(("what does this suggest", "what does this point toward", "what is the likely diagnosis", "what is the most likely diagnosis", "what is the next step", "what is the best treatment")):
        return f"{prompt}?"
    if prompt.startswith(("Which ", "What ", "Why ", "How ", "When ", "Where ")):
        return f"{prompt}?"
    return f"{prompt}:"


def q(prompt, answer, wrong, explanation, clinical=False, difficulty=None):
    options = [answer, *wrong]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {
        "prompt": punctuate(prompt),
        "options": options,
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty or ("high" if clinical else "moderate"),
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("Oral Cavity Anatomy, Examination and Common Symptoms", [
        q("The anterior two-thirds of the tongue drains mainly to", "Submental, submandibular and deep cervical nodes", ["Preauricular nodes only", "Posterior mediastinal nodes", "Axillary nodes"], "Tongue lymphatics drain variably to submental, submandibular and deep cervical groups."),
        q("Which nerve carries general sensation from the anterior two-thirds of tongue", "Lingual nerve", ["Glossopharyngeal nerve", "Hypoglossal nerve", "Greater palatine nerve"], "The lingual nerve supplies general sensation; chorda tympani carries taste."),
        q("A patient develops numbness of the anterior tongue after third molar extraction. The injured nerve is most likely", "Lingual nerve", ["Hypoglossal nerve", "Vagus nerve", "Lesser palatine nerve"], "The lingual nerve runs close to the mandibular third molar region.", True),
        q("Taste from the anterior two-thirds of tongue is carried by", "Chorda tympani", ["Auriculotemporal nerve", "Inferior alveolar nerve", "Recurrent laryngeal nerve"], "Chorda tympani joins the lingual nerve to carry taste fibers."),
        q("The main motor nerve of the tongue is", "Hypoglossal nerve", ["Facial nerve", "Trigeminal nerve", "Accessory nerve"], "CN XII supplies intrinsic and extrinsic tongue muscles except palatoglossus."),
        q("A protruded tongue deviates to the right. This usually indicates weakness of", "Right hypoglossal nerve", ["Left facial nerve", "Right glossopharyngeal nerve", "Left mandibular nerve"], "The tongue deviates toward the side of lower motor neuron hypoglossal weakness.", True),
        q("The hard palate is supplied posteriorly by branches passing through the", "Greater palatine foramen", ["Foramen ovale", "Stylomastoid foramen", "Jugular foramen"], "Greater palatine vessels and nerves emerge onto the hard palate."),
        q("Trismus in oral cavity infection is important because it may indicate spread to", "Masticator space", ["Middle ear only", "Frontal sinus", "Nasolacrimal sac"], "Involvement of muscles of mastication causes restricted mouth opening."),
        q("A patient with dental infection develops fever and inability to open the mouth fully. What does this suggest", "Deep fascial space involvement", ["Simple aphthous ulcer", "Otosclerosis", "Allergic rhinitis"], "Trismus with infection suggests deeper spread and needs urgent assessment.", True),
        q("Floor of mouth swelling can endanger life primarily by", "Airway obstruction", ["Stapes fixation", "Retinal detachment", "External canal stenosis"], "Rapid floor of mouth edema can push the tongue upward and obstruct the airway.", True),
    ]),
    ("Ulcers, Stomatitis and Oral Mucosal Lesions", [
        q("Recurrent aphthous ulcers are typically", "Painful shallow ulcers on nonkeratinized mucosa", ["Painless bony swellings", "Black necrotic eschars only", "Vascular pulsatile masses"], "Minor aphthae usually affect labial, buccal or ventral tongue mucosa."),
        q("Which oral lesion is a potentially malignant white patch that cannot be scraped off", "Leukoplakia", ["Thrush", "Mucocele", "Ranula"], "Leukoplakia is a clinical diagnosis after excluding other white lesions."),
        q("A smoker has a persistent non-scrapable white patch on the lateral tongue. The lesion is most likely", "Leukoplakia", ["Pseudomembranous candidiasis", "Herpangina", "Mucous retention cyst"], "A persistent white patch in a smoker needs biopsy to assess dysplasia.", True),
        q("Erythroplakia is clinically important because it has", "High risk of severe dysplasia or carcinoma", ["No malignant potential", "Only viral inclusion bodies", "Only salivary duct obstruction"], "Velvety red patches often harbor dysplasia or invasive carcinoma."),
        q("Oral candidiasis in an adult should prompt assessment for", "Diabetes, immunosuppression or steroid use", ["Otosclerosis", "Choanal atresia", "Nasal valve collapse"], "Thrush may reflect local steroid exposure or systemic immune/metabolic disease."),
        q("A patient using inhaled steroids develops removable white oral plaques with burning. What is the likely diagnosis", "Pseudomembranous candidiasis", ["Leukoplakia", "Pemphigus vulgaris", "Oral submucous fibrosis"], "Scrapable plaques after steroid inhaler use are typical of thrush.", True),
        q("Oral lichen planus commonly shows", "Reticular white striae", ["Pulsatile red mass", "Blue cyst under tongue", "Hard salivary calculus"], "Wickham striae are a classic reticular pattern."),
        q("Oral submucous fibrosis is strongly associated with", "Areca nut chewing", ["Cold water exposure", "Aspirin sensitivity", "Noise trauma"], "Areca nut causes progressive fibrosis, trismus and malignant risk."),
        q("A man who chews gutka has burning mouth, blanching mucosa and progressive trismus. What does this point toward", "Oral submucous fibrosis", ["Acute tonsillitis", "Meniere disease", "Choanal atresia"], "Areca-related fibrosis causes stiffness and reduced mouth opening.", True),
        q("A chronic ulcer with indurated margins on the lateral tongue should be managed by", "Biopsy to exclude carcinoma", ["Repeated topical anesthetic only", "Wax removal", "Posterior nasal packing"], "Induration and persistence are warning signs for oral squamous carcinoma.", True),
    ]),
    ("Oral Infections and Deep Neck Spread from Oral Sepsis", [
        q("Ludwig angina is cellulitis of the submandibular space, usually arising from", "Mandibular molar infection", ["Frontal sinusitis", "External otitis", "Sphenoid mucocele"], "Lower molar roots communicate with submandibular and sublingual spaces."),
        q("A patient with dental sepsis has brawny floor-of-mouth swelling, drooling and muffled voice. The priority is", "Airway assessment and securing if threatened", ["Delayed elective biopsy", "Pure tone audiometry", "Epley maneuver"], "Ludwig angina can rapidly obstruct the airway.", True),
        q("Cancrum oris is also known as", "Noma", ["Ranula", "Sialolithiasis", "Geographic tongue"], "Noma is destructive gangrenous stomatitis, often in malnourished children."),
        q("Angular cheilitis commonly affects the", "Corners of mouth", ["Hard palate midline", "Parotid tail", "Tonsillar fossa only"], "Fissuring and inflammation occur at oral commissures."),
        q("Herpetic gingivostomatitis commonly presents with painful oral ulcers and", "Fever with gingival inflammation", ["Painless red tongue only", "Unilateral parotid tumor", "Stone in Wharton duct"], "Primary HSV infection causes fever, gingivitis and vesiculo-ulcers."),
        q("A child has fever, drooling, painful gingivitis and multiple oral vesicles. What is the likely diagnosis", "Primary herpetic gingivostomatitis", ["Leukoplakia", "Pleomorphic adenoma", "Oral submucous fibrosis"], "The acute febrile vesiculo-ulcerative picture fits primary HSV.", True),
        q("Hand-foot-mouth disease is commonly caused by", "Coxsackie virus", ["Mumps virus", "Epstein-Barr virus only", "Candida albicans"], "Coxsackie A viruses commonly cause oral ulcers with hand and foot lesions."),
        q("Dental abscess may spread to the parapharyngeal space and present with", "Fever, neck swelling and trismus", ["Only sneezing", "Pulsatile tinnitus", "Watery rhinorrhea"], "Deep space infection produces systemic toxicity, neck signs and trismus."),
        q("After molar pain, a patient develops fever, medial tonsillar bulge and trismus. What does this suggest", "Parapharyngeal space abscess", ["Simple aphthous ulcer", "Atrophic rhinitis", "Otosclerosis"], "Medial pharyngeal bulge and trismus suggest deep neck space infection.", True),
        q("Actinomycosis classically produces chronic cervicofacial infection with", "Sulfur granules", ["Keratin pearls only", "Sporangia dots", "Cholesterol crystals"], "Actinomycosis causes indurated sinuses with yellow sulfur granules.", True),
    ]),
    ("Benign Oral Cavity Lesions and Cysts", [
        q("A mucocele most commonly results from", "Minor salivary gland mucus extravasation", ["Stapes fixation", "Fungal invasion", "Nasolacrimal obstruction"], "Trauma to minor salivary ducts leads to mucus pooling."),
        q("The commonest site for oral mucocele is the", "Lower lip", ["Hard palate only", "Parotid tail", "Posterior choana"], "Lower lip biting commonly injures minor salivary ducts."),
        q("A teenager has a bluish fluctuant swelling on the lower lip after repeated lip biting. What is the likely diagnosis", "Mucocele", ["Leukoplakia", "Pleomorphic adenoma", "Sialolithiasis"], "A blue lower-lip cyst after trauma is classic for mucocele.", True),
        q("Ranula arises from the", "Sublingual gland", ["Parotid gland", "Tonsil", "Thyroid gland"], "Ranula is a mucus extravasation cyst related to the sublingual gland."),
        q("A plunging ranula extends through or around the", "Mylohyoid muscle", ["Masseter tendon", "Stapedius tendon", "Cricothyroid membrane"], "Cervical extension occurs through a mylohyoid defect or around its posterior margin."),
        q("A child has a bluish cystic floor-of-mouth swelling that elevates the tongue. What is it most likely", "Ranula", ["Dermoid of nose", "Leukoplakia", "Epulis fissuratum"], "A ranula appears as a translucent bluish swelling in the floor of mouth.", True),
        q("Epulis refers to a localized swelling arising from the", "Gingiva", ["Olfactory cleft", "Middle ear", "Nasopharynx"], "Epulis is a clinical term for a gingival mass."),
        q("Geographic tongue is also called", "Benign migratory glossitis", ["Median rhomboid glossitis", "Black hairy tongue", "Ankyloglossia"], "Migratory depapillated patches create map-like changes."),
        q("A patient has changing map-like red patches on the tongue with white borders and mild burning. What does this suggest", "Geographic tongue", ["Tongue carcinoma", "Ranula", "Oral pemphigus"], "Migratory erythematous patches with white margins are typical and benign.", True),
        q("A dermoid cyst in the floor of mouth is usually", "Midline and doughy", ["Pulsatile and vascular", "Black and necrotic", "Scrapable white plaque"], "Dermoids are often midline, slow-growing, doughy floor-of-mouth masses.", True),
    ]),
    ("Premalignant Disease and Oral Cavity Carcinoma", [
        q("The commonest malignancy of the oral cavity is", "Squamous cell carcinoma", ["Adenoid cystic carcinoma", "Pleomorphic adenoma", "Lymphangioma"], "Most oral cavity cancers are squamous carcinomas."),
        q("Important risk factors for oral squamous carcinoma include tobacco, alcohol and", "Areca nut chewing", ["Cold water swimming", "Aspirin sensitivity", "Stapes fixation"], "Tobacco, alcohol and areca nut are major oral cancer risks."),
        q("A chronic non-healing lateral tongue ulcer has induration and contact bleeding. What is the most likely diagnosis", "Oral squamous cell carcinoma", ["Aphthous ulcer", "Mucocele", "Geographic tongue"], "Indurated persistent ulcer with bleeding is malignant until proved otherwise.", True),
        q("The most common site for carcinoma of the oral tongue is", "Lateral border", ["Dorsal midline only", "Tip only", "Ventral frenulum"], "The lateral border is a high-risk site for tongue carcinoma."),
        q("Early nodal spread from oral tongue cancer commonly involves", "Level I and II cervical nodes", ["Axillary nodes", "Inguinal nodes", "Popliteal nodes"], "Submandibular and upper deep cervical nodes are common first stations."),
        q("A patient with tongue carcinoma has a firm ipsilateral upper cervical node. This represents", "Regional nodal metastasis", ["Benign nasal polyp", "Mumps parotitis", "Thyroglossal cyst"], "A firm draining cervical node in oral cancer suggests metastasis.", True),
        q("Biopsy of a suspicious oral ulcer should be taken from", "Edge including abnormal and adjacent tissue", ["Only central necrotic slough", "Normal opposite cheek", "Dental calculus"], "The advancing edge best shows diagnostic epithelium and invasion."),
        q("T staging in oral cavity carcinoma is based mainly on tumor size and", "Depth of invasion", ["Audiogram threshold", "Nasal airflow", "Taste testing only"], "Depth of invasion is important for staging and nodal risk."),
        q("A small tongue cancer with deep invasion has higher neck risk because depth of invasion predicts", "Cervical nodal metastasis", ["Otosclerosis", "BPPV", "Atrophic rhinitis"], "Greater invasion depth correlates with occult nodal disease.", True),
        q("Treatment of resectable oral cavity carcinoma usually centers on", "Surgical excision with appropriate neck management", ["Antihistamines alone", "Repeated cautery only", "Grommet insertion"], "Surgery is the mainstay, with neck dissection and adjuvant therapy as indicated.", True),
    ]),
    ("Salivary Gland Anatomy, Physiology and Investigation", [
        q("Stensen duct drains the", "Parotid gland", ["Submandibular gland", "Sublingual gland", "Minor palatal glands"], "The parotid duct opens opposite the upper second molar."),
        q("Wharton duct drains the", "Submandibular gland", ["Parotid gland", "Lacrimal gland", "Thyroid gland"], "The submandibular duct opens at the sublingual papilla."),
        q("A stone is visible at the sublingual papilla with painful meal-time swelling of the submandibular region. The involved duct is", "Wharton duct", ["Stensen duct", "Nasolacrimal duct", "Thyroglossal tract"], "Submandibular stones commonly lodge in Wharton duct.", True),
        q("The facial nerve passes through the", "Parotid gland", ["Submandibular gland", "Sublingual gland", "Thyroid isthmus"], "The facial nerve divides the parotid into superficial and deep surgical lobes."),
        q("The retromandibular vein is an important landmark within the", "Parotid gland", ["Floor of mouth", "Tonsillar crypt", "Nasal vestibule"], "It lies in the parotid and helps orientation with facial nerve anatomy."),
        q("A painless parotid mass is being evaluated before surgery. Facial nerve function should be documented because", "Weakness suggests malignant or invasive disease", ["It confirms mumps", "It rules out all stones", "It treats xerostomia"], "Preoperative facial weakness is a red flag in parotid tumors.", True),
        q("Ultrasound-guided FNAC is commonly used for salivary swellings to assess", "Cytology and guide management", ["Hearing threshold", "Nasal airflow", "Eustachian tube function"], "FNAC helps distinguish inflammatory, benign and malignant lesions."),
        q("Sialography is generally avoided during", "Acute infection", ["Chronic dry mouth only", "Resolved swelling", "Routine tumor follow-up"], "Injecting contrast into an acutely infected duct can worsen pain and infection."),
        q("A patient with suspected acute parotitis is in severe pain and febrile. Sialography is avoided because", "Acute infection may be worsened", ["It fixes the stapes", "It causes choanal atresia", "It closes Wharton duct permanently"], "Acute infection is a contraindication to sialography.", True),
        q("Minor salivary glands are distributed widely, especially in the", "Palate, lips and buccal mucosa", ["Middle ear", "Frontal sinus only", "External auditory canal"], "Minor glands are numerous in oral mucosa and can develop tumors.", True),
    ]),
    ("Sialolithiasis and Obstructive Salivary Disease", [
        q("Sialolithiasis most commonly affects the", "Submandibular gland", ["Parotid gland", "Sublingual gland", "Lacrimal gland"], "Submandibular saliva is more mucous and alkaline, favoring stone formation."),
        q("The classic symptom of salivary stone is", "Painful swelling during meals", ["Painless anosmia", "Vertigo on rolling", "Itchy sneezing only"], "Meal stimulation increases salivary flow against an obstruction."),
        q("A patient gets recurrent painful swelling below the mandible whenever eating. What is the most likely diagnosis", "Submandibular sialolithiasis", ["Pleomorphic adenoma", "Mumps", "Oral candidiasis"], "Meal-time colic and swelling are typical of duct obstruction.", True),
        q("Submandibular stones are common because Wharton duct is long, uphill and saliva is", "Mucin-rich and alkaline", ["Purely serous and acidic", "Absent during meals", "Produced by thyroid"], "Viscous alkaline saliva promotes calculus formation."),
        q("Small distal duct stones may be managed by", "Transoral duct stone removal", ["Parotidectomy", "Radiotherapy first", "Tonsillectomy"], "Palpable distal Wharton duct stones can often be removed intraorally."),
        q("A palpable stone near the opening of Wharton duct causes recurrent swelling. What is the best treatment", "Transoral sialolithotomy", ["Superficial parotidectomy", "Cochlear implantation", "Nasal cautery"], "Distal duct stones are suitable for intraoral removal.", True),
        q("Sialendoscopy is useful because it can", "Visualize and treat ductal obstruction minimally invasively", ["Grade hearing loss", "Remove nasal polyps", "Measure olfaction"], "Endoscopic duct techniques can retrieve stones or dilate strictures."),
        q("Chronic obstructive sialadenitis may lead to", "Recurrent infection and gland fibrosis", ["Otosclerosis", "Septal perforation only", "BPPV"], "Repeated obstruction and infection damage the gland."),
        q("A long-standing stone with repeated painful infections leaves a firm poorly functioning submandibular gland. The definitive option may be", "Submandibular gland excision", ["Silver nitrate cautery", "Epley maneuver", "Grommet insertion"], "Chronically damaged glands with recurrent disease may require excision.", True),
        q("Radiolucent salivary stones can still be detected by", "Ultrasound or noncontrast CT", ["Rinne test", "Dix-Hallpike test", "Pure nasal endoscopy only"], "Imaging can detect stones not seen on plain radiographs.", True),
    ]),
    ("Inflammatory, Viral and Autoimmune Salivary Disease", [
        q("Acute bacterial parotitis is commonly promoted by", "Dehydration and poor oral hygiene", ["Cold water exposure", "Aspirin sensitivity", "Noise trauma"], "Reduced salivary flow allows ascending duct infection."),
        q("Pus expressed from Stensen duct in a febrile patient with painful parotid swelling suggests", "Acute suppurative parotitis", ["Pleomorphic adenoma", "Ranula", "Leukoplakia"], "Purulent duct discharge confirms bacterial sialadenitis.", True),
        q("Mumps typically causes painful swelling of the", "Parotid glands", ["Thyroid gland", "Minor palatal glands only", "Sublingual caruncle"], "Mumps virus classically affects parotid glands."),
        q("A child has bilateral parotid swelling, fever and orchitis. What is the likely diagnosis", "Mumps", ["Sialolithiasis", "Adenoid cystic carcinoma", "Oral submucous fibrosis"], "Parotitis with orchitis is a classic mumps complication.", True),
        q("Sjögren syndrome is characterized by xerostomia, keratoconjunctivitis sicca and", "Autoimmune salivary gland destruction", ["Stapes fixation", "Nasal valve collapse", "Cholesteatoma"], "Lymphocytic autoimmune damage reduces lacrimal and salivary secretion."),
        q("A woman has dry eyes, dry mouth, dental caries and parotid enlargement. What does this suggest", "Sjögren syndrome", ["Acute otitis media", "Choanal atresia", "Meniere disease"], "Sicca symptoms with parotid enlargement point to Sjögren syndrome.", True),
        q("Sjögren syndrome increases risk of", "Non-Hodgkin lymphoma", ["Otosclerosis", "Nasal dermoid", "BPPV"], "Chronic lymphoid stimulation can lead to lymphoma."),
        q("Recurrent parotitis of childhood usually presents with", "Repeated painful parotid swelling episodes", ["Persistent tongue ulcer only", "Posterior epistaxis", "Conductive deafness"], "Children may have recurrent inflammatory parotid episodes, often improving with age."),
        q("Treatment of acute suppurative parotitis includes hydration, sialogogues, gland massage and", "Antistaphylococcal antibiotics", ["Stapedotomy", "Nasal polypectomy", "Radiotherapy"], "Supportive salivary flow measures plus antibiotics treat ascending bacterial infection."),
        q("A postoperative dehydrated elderly patient develops tender parotid swelling and fever. The first-line management includes", "Hydration and appropriate antibiotics", ["Immediate parotidectomy in every case", "Intranasal steroid only", "Epley maneuver"], "Postoperative parotitis is treated with fluids, oral hygiene, massage and antibiotics.", True),
    ]),
    ("Benign Salivary Gland Tumors", [
        q("The commonest benign salivary gland tumor is", "Pleomorphic adenoma", ["Warthin tumor", "Mucoepidermoid carcinoma", "Adenoid cystic carcinoma"], "Pleomorphic adenoma is the most common benign salivary tumor."),
        q("Pleomorphic adenoma most commonly arises in the", "Parotid gland", ["Sublingual gland", "Thyroid gland", "Tonsil"], "Most salivary tumors arise in parotid; most parotid tumors are benign."),
        q("A slow-growing painless mobile parotid tail mass in a young adult is most likely", "Pleomorphic adenoma", ["Acute parotitis", "Adenoid cystic carcinoma", "Sialolithiasis"], "A painless slow parotid mass is classic for pleomorphic adenoma.", True),
        q("Pleomorphic adenoma should not be shelled out because of risk of", "Recurrence from pseudopodia or capsule breach", ["Immediate mumps", "Stone migration", "Nasal obstruction"], "Incomplete enucleation can leave microscopic tumor extensions."),
        q("Standard treatment for superficial-lobe parotid pleomorphic adenoma is", "Superficial parotidectomy with facial nerve preservation", ["Simple incision drainage", "Long-term antibiotics only", "Tonsillectomy"], "Formal parotidectomy removes tumor safely while identifying the facial nerve."),
        q("A pleomorphic adenoma recurs after simple enucleation. The recurrence is explained by", "Capsule violation and residual tumor extensions", ["Viral reinfection", "Wharton duct stone", "Allergic edema"], "Pseudopodia and spillage increase recurrence risk.", True),
        q("Warthin tumor is strongly associated with", "Smoking", ["Areca nut only", "Cold water exposure", "Aspirin sensitivity"], "Warthin tumor has a notable smoking association."),
        q("An older male smoker has a painless swelling near the angle of mandible in the parotid tail. The tumor site favors", "Warthin tumor", ["Ranula", "Oral leukoplakia", "Submandibular duct stone"], "Warthin tumor often arises in parotid lymphoid tissue near the tail.", True),
        q("An older male smoker has a cystic parotid tail mass that is hot on technetium scan. What is likely", "Warthin tumor", ["Ranula", "Oral candidiasis", "Sialolithiasis"], "Warthin tumor classically affects older male smokers and may be bilateral."),
        q("Facial nerve weakness with a presumed benign parotid tumor should raise concern for", "Malignancy rather than simple benign tumor", ["Normal Warthin tumor behavior", "Uncomplicated mucocele", "Geographic tongue"], "Benign tumors usually do not cause facial palsy.", True),
    ]),
    ("Malignant Salivary Gland Tumors and Management", [
        q("The commonest malignant salivary gland tumor is", "Mucoepidermoid carcinoma", ["Pleomorphic adenoma", "Warthin tumor", "Lipoma"], "Mucoepidermoid carcinoma is the most common salivary malignancy."),
        q("Adenoid cystic carcinoma is known for", "Perineural invasion", ["Always benign behavior", "Meal-time colic only", "Scrapable plaques"], "Perineural spread causes pain, numbness and late recurrence."),
        q("A patient has a small hard palate salivary tumor with severe pain and numbness. What does this suggest", "Adenoid cystic carcinoma with perineural spread", ["Mucocele", "Geographic tongue", "Mumps"], "Minor salivary adenoid cystic carcinoma often spreads along nerves.", True),
        q("Facial nerve palsy in a parotid mass is a red flag for", "Malignant parotid tumor", ["Simple Warthin tumor", "Submandibular stone", "Ranula"], "Invasion of the facial nerve suggests malignancy."),
        q("The likelihood of malignancy is highest in tumors of the", "Sublingual gland", ["Parotid gland", "Minor labial glands only", "Normal Stensen duct"], "Smaller salivary glands have a higher proportion of malignant tumors."),
        q("A rapidly enlarging painful parotid mass with facial weakness is most concerning for", "Parotid carcinoma", ["Pleomorphic adenoma", "Acute aphthous ulcer", "Rhinitis medicamentosa"], "Rapid growth, pain and facial palsy are malignant features.", True),
        q("Management of high-grade parotid carcinoma usually includes surgery and", "Postoperative radiotherapy when indicated", ["Observation only", "Intranasal antihistamine", "Epley maneuver"], "Adjuvant radiotherapy is often used for high-risk malignant salivary tumors."),
        q("Neck dissection in salivary gland cancer is considered when there are", "Clinically positive nodes or high-risk disease", ["Simple dry mouth only", "Small uncomplicated mucocele", "Mild aphthous ulcers"], "Nodal disease and high-grade tumors may need neck management."),
        q("A parotid malignancy encases the facial nerve with preoperative complete palsy. Surgical planning may require", "Facial nerve sacrifice with reconstruction planning", ["Ignoring the nerve", "Only duct dilation", "No oncologic margins"], "A nonfunctioning invaded nerve may need resection for clearance.", True),
        q("Long-term follow-up is especially important in adenoid cystic carcinoma because of", "Late local recurrence and distant metastasis", ["Immediate spontaneous cure", "No perineural spread", "Only childhood presentation"], "Adenoid cystic carcinoma may recur or metastasize years later.", True),
    ]),
]


def build_questions():
    questions = []
    for topic_order, (topic, rows) in enumerate(TOPICS, 1):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        clinical_count = sum(1 for row in rows if "clinical" in row.get("tags", []))
        if clinical_count != 4:
            raise ValueError(f"{topic} has {clinical_count} clinical questions, expected 4")
        topic_slug = slugify(topic)
        for question_order, row in enumerate(rows, 1):
            questions.append({
                "id": f"ent-oral-salivary-{topic_slug}-{question_order:02d}",
                "subjectId": SUBJECT_ID,
                "subjectTitle": SUBJECT_TITLE,
                "chapterTitle": CHAPTER,
                "chapterOrder": CHAPTER_ORDER,
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "source": "ai",
                "sourcePdf": SOURCE_PDF,
                "imageUrls": [],
                **row,
            })
    return questions


def update(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    questions = build_questions()
    data["questions"] = [
        item for item in data.get("questions", [])
        if not (item.get("subjectId") == SUBJECT_ID and item.get("chapterTitle") == CHAPTER)
    ] + questions
    if len(questions) != 100:
        raise AssertionError(f"Expected 100 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 100:
        raise AssertionError("Duplicate ENT oral/salivary question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ENT oral cavity and salivary gland questions.")


if __name__ == "__main__":
    main()
