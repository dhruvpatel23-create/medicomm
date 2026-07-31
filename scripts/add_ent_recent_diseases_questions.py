import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ent"
SUBJECT_TITLE = "ENT"
CHAPTER = "Recent Diseases"
CHAPTER_ORDER = 8
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
    ]
    for old, new in replacements:
        if prompt.endswith(old):
            return f"{prompt[:-len(old)]}{new}"
    final_clause = re.split(r"[.:]", prompt)[-1].strip()
    if prompt.lower().endswith(("what does this suggest", "what is the most likely diagnosis", "what is the next step", "what is the best treatment")):
        return f"{prompt}?"
    if prompt.startswith(("Which ", "What ", "Why ", "How ", "When ", "Where ")) or final_clause.startswith(("Which ", "What ", "Why ", "How ", "When ", "Where ")):
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
    ("COVID-19 and Post-Viral ENT Manifestations", [
        q("The most characteristic early ENT symptom of COVID-19 is", "Sudden smell loss", ["Pulsatile tinnitus", "Meal-time parotid swelling", "Blue ranula"], "COVID-related olfactory dysfunction may occur with little nasal obstruction."),
        q("COVID-related anosmia is thought to involve injury to", "Olfactory supporting cells and local neuroepithelium", ["Stapes footplate", "Parotid acini only", "Tonsillar crypt stones"], "Sustentacular and olfactory cleft inflammation contribute to smell loss."),
        q("A young adult has sudden anosmia after fever and sore throat, with normal nasal endoscopy. What is the likely diagnosis", "Post-viral olfactory dysfunction", ["Antrochoanal polyp", "Otosclerosis", "Peritonsillar abscess"], "Sudden smell loss after viral illness with clear nasal cavity fits post-viral olfactory loss.", True),
        q("Olfactory training usually uses repeated exposure to", "Distinct odors over weeks to months", ["Pure tones", "Cold water", "Salivary stimulants"], "Regular odor exposure can aid recovery after post-viral smell loss."),
        q("Parosmia after viral infection means", "Distorted perception of odors", ["Complete inability to swallow", "Painful parotid swelling", "Ear discharge"], "Patients perceive familiar smells as unpleasant or altered."),
        q("After COVID infection, coffee smells rotten to a patient who can still detect odors. What does this suggest", "Parosmia", ["Phantosmia only", "Ageusia only", "Conductive anosmia"], "Distorted odor quality is parosmia.", True),
        q("Persistent dysphonia after prolonged COVID ventilation may result from", "Post-intubation laryngeal injury", ["Adenoid hypertrophy", "Mumps", "Septal spur"], "Intubation can cause granuloma, stenosis or vocal fold immobility."),
        q("Tracheostomy in contagious respiratory infection requires particular attention to", "Aerosol precautions", ["Smell testing only", "Dental charting", "Caloric testing"], "Airway procedures generate aerosols and need protection."),
        q("A patient extubated after prolonged ICU care has biphasic stridor. What is the concern", "Post-intubation laryngotracheal stenosis", ["Simple reflux", "Vocal nodules", "Aphthous ulcer"], "Delayed stridor after intubation suggests airway narrowing.", True),
        q("Taste disturbance after viral illness is called", "Dysgeusia", ["Dysphonia", "Dysphagia", "Diplacusis"], "Dysgeusia means altered taste perception.", True),
    ]),
    ("Rhino-Orbito-Cerebral Mucormycosis", [
        q("Rhino-orbito-cerebral mucormycosis is most strongly associated with diabetes, especially", "Ketoacidosis", ["Hypocalcemia", "Otosclerosis", "Iron deficiency alone"], "Acidosis and impaired immunity favor mucor invasion."),
        q("The hallmark pathology of mucormycosis is", "Angioinvasion with tissue necrosis", ["Benign lymphoid hyperplasia", "Capsular invasion only", "Keratin cyst formation"], "Fungal invasion of vessels causes thrombosis and black necrosis."),
        q("A diabetic patient after steroid-treated COVID has facial pain, black turbinate eschar and orbital swelling. What is the most likely diagnosis", "Rhino-orbito-cerebral mucormycosis", ["Allergic fungal sinusitis", "Simple bacterial sinusitis", "Nasal polyp"], "Black eschar and orbital signs in uncontrolled diabetes are classic.", True),
        q("First-line antifungal therapy for mucormycosis is", "Liposomal amphotericin B", ["Fluconazole", "Acyclovir", "Azithromycin"], "Mucor requires amphotericin-based therapy; fluconazole is ineffective."),
        q("Surgical treatment in mucormycosis focuses on", "Urgent debridement of necrotic tissue", ["Simple polypectomy only", "Silver nitrate cautery", "Adenoidectomy"], "Dead tissue has poor drug penetration and must be removed."),
        q("A patient with mucormycosis loses vision and has ophthalmoplegia. What does this suggest", "Orbital apex or cavernous sinus involvement", ["Benign rhinitis", "Mild otitis externa", "Ranula"], "Orbital apex disease threatens optic nerve and ocular motor nerves.", True),
        q("Correcting the underlying risk factor in mucormycosis includes control of hyperglycemia and", "Reversal of ketoacidosis", ["Increasing steroids", "Stopping all insulin", "Avoiding debridement"], "Metabolic correction is essential with antifungal and surgery."),
        q("On microscopy, mucor shows broad aseptate hyphae with", "Right-angle branching", ["Narrow septate acute-angle branching", "Budding yeast capsules", "Acid-fast bacilli"], "Mucorales show broad ribbon-like aseptate hyphae."),
        q("A necrotic palatal ulcer appears in uncontrolled diabetes with maxillary sinus disease. What is the likely mechanism", "Vascular invasion causing ischemic necrosis", ["Simple pressure ulcer", "IgE allergy", "Salivary obstruction"], "Angioinvasion causes thrombosis and palatal necrosis.", True),
        q("Delay in treating invasive fungal sinusitis is dangerous because spread can reach the orbit and", "Brain", ["Middle ear ossicles only", "Parotid duct", "Lower lip"], "Rhino-orbital disease may extend intracranially.", True),
    ]),
    ("Allergic Fungal Rhinosinusitis and Eosinophilic Disease", [
        q("Allergic fungal rhinosinusitis is a", "Noninvasive hypersensitivity reaction to fungi", ["Angioinvasive emergency in every case", "Salivary gland tumor", "Vocal fold palsy"], "AFRS has allergic mucin and fungi without tissue invasion."),
        q("Allergic mucin usually contains eosinophils and", "Charcot-Leyden crystals", ["Amyloid stroma", "Psammoma bodies", "Sulfur granules"], "Eosinophil breakdown can form Charcot-Leyden crystals."),
        q("An atopic teenager has nasal polyps, expanded sinuses and thick allergic mucin. What is the diagnosis", "Allergic fungal rhinosinusitis", ["Mucormycosis", "Rhinitis medicamentosa", "Choanal atresia"], "Polyps, atopy, sinus expansion and allergic mucin fit AFRS.", True),
        q("CT in allergic fungal rhinosinusitis may show heterogeneous opacities due to", "Dense allergic mucin", ["Pure air only", "Parotid calculus", "Stapes fixation"], "Proteinaceous allergic mucin gives hyperdense areas."),
        q("Treatment of allergic fungal rhinosinusitis usually includes surgery and", "Topical or systemic corticosteroid control", ["Fluconazole alone", "Radioiodine", "Voice therapy only"], "Disease control needs clearance and anti-inflammatory therapy."),
        q("A patient with AFRS has recurrent polyposis after surgery. What long-term measure is important", "Regular topical steroid therapy and surveillance", ["No follow-up", "Repeated blind avulsion", "Epley maneuver"], "Recurrence is common and needs endoscopic follow-up.", True),
        q("Eosinophilic chronic rhinosinusitis is commonly associated with", "Asthma and smell loss", ["Otosclerosis", "Mumps", "Branchial cyst"], "Type 2 inflammation often overlaps with asthma and anosmia."),
        q("Aspirin-exacerbated respiratory disease includes asthma, nasal polyps and", "NSAID sensitivity", ["Mucor infection", "Thyroid storm", "Submandibular stone"], "AERD causes severe recurrent polyposis and reactions to COX-1 inhibitors."),
        q("An asthmatic patient with recurrent nasal polyps develops bronchospasm after aspirin. What does this suggest", "Aspirin-exacerbated respiratory disease", ["Simple viral rhinitis", "Atrophic rhinitis", "Meniere disease"], "Asthma, polyps and aspirin sensitivity form the classic triad.", True),
        q("Biologic therapy in severe nasal polyposis targets type 2 inflammation such as", "IL-4, IL-5 or IgE pathways", ["Thyroglobulin", "Dopamine", "Calcitonin"], "Selected severe CRSwNP can respond to biologics targeting type 2 pathways.", True),
    ]),
    ("HPV-Related Head and Neck Disease", [
        q("HPV-related oropharyngeal carcinoma most often arises in", "Tonsil and base of tongue", ["Inferior turbinate", "External ear", "Submandibular duct"], "HPV-associated SCC commonly begins in oropharyngeal lymphoid crypts."),
        q("The high-risk HPV type most linked with oropharyngeal carcinoma is", "HPV 16", ["HPV 6", "HPV 11", "HPV 2"], "HPV 16 is the major high-risk type in oropharyngeal SCC."),
        q("A nonsmoker presents with cystic level II neck node and small tonsil primary. What is likely", "HPV-positive oropharyngeal carcinoma", ["Mumps", "Peritonsillar abscess", "Warthin tumor"], "HPV-positive tumors may present with cystic nodal metastasis.", True),
        q("p16 immunohistochemistry is commonly used as a surrogate marker for", "HPV-associated oropharyngeal carcinoma", ["Mucormycosis", "Otosclerosis", "Sialolithiasis"], "p16 overexpression correlates with transcriptionally active HPV in the right context."),
        q("HPV vaccination helps prevent infection with oncogenic HPV types and reduces risk of", "HPV-related cancers", ["Thyroid storm", "Oesophageal achalasia", "Meniere disease"], "Vaccination prevents infection with high-risk HPV types."),
        q("A young adult asks why HPV vaccine matters for ENT. The best reason is prevention of", "Oropharyngeal cancer linked to high-risk HPV", ["Cerumen", "Submandibular stones", "BPPV"], "High-risk HPV is a major cause of oropharyngeal carcinoma.", True),
        q("Recurrent respiratory papillomatosis is usually caused by", "HPV 6 and 11", ["HPV 16 only", "EBV", "CMV"], "Low-risk HPV types cause benign but recurrent papillomas."),
        q("Juvenile laryngeal papillomatosis presents mainly with", "Progressive hoarseness and stridor", ["Posterior epistaxis", "Meal-time swelling", "Blue ranula"], "Papillomas affect the voice and can obstruct the airway."),
        q("A child has multiple wart-like vocal cord lesions recurring after debulking. What is the diagnosis", "Recurrent respiratory papillomatosis", ["Laryngeal carcinoma", "Acute croup", "Vocal nodule only"], "Recurrent papillomas are typical of HPV-related disease.", True),
        q("Compared with tobacco-related tumors, HPV-positive oropharyngeal carcinoma generally has", "Better treatment response", ["No nodal spread ever", "No need for diagnosis", "Only fungal cause"], "HPV-positive disease often has a more favorable prognosis.", True),
    ]),
    ("HIV, Immunosuppression and ENT Infections", [
        q("Oral candidiasis in an adult may be a clue to", "Immunosuppression", ["Otosclerosis", "Benign nasal cycle", "Sialolithiasis"], "Thrush can occur with HIV, diabetes, steroids or other immune defects."),
        q("Hairy leukoplakia is associated with", "Epstein-Barr virus in immunosuppression", ["Mumps virus", "HPV 6 only", "Mucor"], "Oral hairy leukoplakia is EBV-related and classically seen in HIV."),
        q("An HIV-positive patient has non-scrapable white corrugated plaques on lateral tongue. What is likely", "Oral hairy leukoplakia", ["Thrush", "Aphthous minor ulcer", "Mucocele"], "Lateral tongue corrugated white plaques suggest EBV hairy leukoplakia.", True),
        q("Kaposi sarcoma in the oral cavity is associated with", "HHV-8", ["HSV-1 only", "HPV 11", "Mumps"], "Kaposi sarcoma is driven by human herpesvirus 8."),
        q("Deep fungal infections in immunocompromised ENT patients are dangerous because they may become", "Invasive and angioinvasive", ["Always self-limited", "Purely allergic only", "Only cosmetic"], "Impaired immunity permits tissue and vascular invasion."),
        q("A neutropenic patient has facial pain, fever and necrotic nasal crusting. What is the concern", "Acute invasive fungal rhinosinusitis", ["Simple allergic rhinitis", "Nasal cycle", "Benign polyp"], "Necrosis in immunosuppression is invasive fungal disease until excluded.", True),
        q("Necrotizing ulcerative gingivitis is associated with pain, bleeding and", "Interdental papilla necrosis", ["Stapes fixation", "Parotid stone", "Pulsatile tinnitus"], "Papillary necrosis and fetor occur in immunosuppression or poor nutrition."),
        q("Persistent generalized lymphadenopathy in HIV commonly involves", "Cervical nodes", ["Popliteal nodes only", "Middle ear", "Inferior turbinate"], "Cervical lymph nodes are commonly enlarged."),
        q("An HIV patient develops rapidly enlarging unilateral tonsil with B symptoms. What must be excluded", "Lymphoma", ["Simple tonsillolith", "Globus", "Atrophic rhinitis"], "Immunosuppression increases lymphoma risk.", True),
        q("Recurrent severe aphthous-like ulcers in HIV may require evaluation for", "Advanced immune suppression", ["Normal nasal cycle", "Otosclerosis", "Meniere disease"], "Large persistent ulcers can occur with low CD4 counts.", True),
    ]),
    ("Antimicrobial Resistance and Recurrent ENT Infection", [
        q("Antibiotic stewardship means using antibiotics only when indicated, with correct drug, dose and", "Duration", ["Color", "Taste", "Brand only"], "Appropriate duration reduces resistance and adverse effects."),
        q("Most uncomplicated viral upper respiratory infections require", "Supportive care rather than antibiotics", ["Immediate broad-spectrum antibiotics", "Radiotherapy", "Thyroidectomy"], "Viral illness does not benefit from antibiotics."),
        q("A child has mild sore throat, cough, rhinorrhea and no fever. What is the best approach", "Supportive care and no routine antibiotic", ["Immediate cephalosporin", "Tonsillectomy next day", "Amphotericin"], "Cough and coryza suggest viral pharyngitis.", True),
        q("Recurrent acute otitis media is commonly promoted by daycare exposure, smoke exposure and", "Eustachian tube dysfunction", ["Stapes fixation", "Lingual thyroid", "Ranula"], "Risk factors increase infections and middle ear ventilation problems."),
        q("Culture-directed therapy is especially useful in", "Recurrent or nonresponding infection", ["Every common cold", "Benign nasal cycle", "Simple globus"], "Cultures help when usual empirical treatment fails."),
        q("A patient with chronic otorrhea fails repeated empirical drops. What is the next useful step", "Aural toilet and culture-directed treatment", ["Keep changing random antibiotics", "Ignore discharge", "Voice therapy"], "Cleaning and microbiology guide targeted therapy.", True),
        q("MRSA ENT infections require antibiotics active against", "Methicillin-resistant Staphylococcus aureus", ["Mumps virus", "Candida only", "Mucor only"], "MRSA is resistant to usual beta-lactam antistaphylococcal drugs."),
        q("Biofilms contribute to chronic ENT infection by", "Protecting bacteria from host defenses and antibiotics", ["Increasing smell", "Fixing stapes", "Preventing all recurrence"], "Biofilms support persistence on mucosa or devices."),
        q("A child with recurrent tonsillitis has symptoms only during viral colds and normal growth. What should be avoided", "Unnecessary antibiotic courses", ["Hydration", "Fever control", "Clinical follow-up"], "Antibiotics should not be used for clear viral illness.", True),
        q("Vaccination reduces ENT infections by preventing pathogens such as pneumococcus and", "Influenza virus", ["Mucor", "All allergens", "Every salivary stone"], "Vaccines reduce respiratory infections and complications.", True),
    ]),
    ("Air Pollution, Allergy and Occupational ENT Disease", [
        q("Air pollution can worsen rhinitis by causing", "Mucosal inflammation and hyperreactivity", ["Stapes fixation", "Parotid stones", "Thyroid storm"], "Irritants inflame nasal mucosa and worsen symptoms."),
        q("Occupational rhinitis is suggested when symptoms improve", "Away from work", ["Only during sleep", "After tonsillectomy", "With loud noise"], "Work-related timing is the key clue."),
        q("A bakery worker has sneezing and nasal blockage at work that improves on weekends. What is likely", "Occupational allergic rhinitis", ["Atrophic rhinitis", "Mucormycosis", "Otosclerosis"], "Flour exposure can cause occupational allergy.", True),
        q("Wood dust exposure is linked to sinonasal", "Adenocarcinoma", ["Warthin tumor", "Mumps", "Ranula"], "Wood dust is a classic occupational risk for ethmoid adenocarcinoma."),
        q("Laryngopharyngeal irritation from smoke exposure may cause", "Chronic laryngitis", ["Sialolithiasis", "BPPV", "Adenoid cyst"], "Smoke irritates the laryngeal mucosa and worsens hoarseness."),
        q("A furniture worker develops unilateral nasal obstruction and epistaxis with ethmoid mass. What is the concern", "Sinonasal adenocarcinoma", ["Simple cold", "Vocal nodule", "Mumps"], "Wood dust plus unilateral mass is a malignancy red flag.", True),
        q("Personal protective equipment in dusty work reduces exposure of nasal mucosa to", "Inhaled irritants and allergens", ["Thyroid hormone", "Endolymph", "Salivary stones"], "Reducing exposure is central to occupational disease prevention."),
        q("Nonallergic irritant rhinitis often causes congestion and rhinorrhea without", "IgE-mediated itching and sneezing pattern", ["Any nasal symptom", "Any trigger", "Any treatment"], "Irritant rhinitis is not primarily allergic."),
        q("A traffic policeman has chronic congestion worsened by fumes without itching or positive allergy tests. What does this suggest", "Irritant nonallergic rhinitis", ["Aspirin-exacerbated disease", "Antrochoanal polyp", "Acute invasive fungus"], "Fume-triggered symptoms without allergy fit irritant rhinitis.", True),
        q("Indoor biomass smoke exposure can worsen ENT disease by increasing", "Chronic mucosal irritation", ["Ossicular fixation", "Parathyroid secretion", "Tongue deviation"], "Chronic irritant exposure damages upper airway mucosa.", True),
    ]),
    ("Autoimmune and Systemic ENT Disorders", [
        q("Granulomatosis with polyangiitis can cause nasal crusting, septal perforation and", "Saddle nose deformity", ["Stapes fixation", "Ranula", "Mumps"], "Vasculitis can destroy cartilage and mucosa."),
        q("Relapsing polychondritis affects cartilage and may involve the pinna, nose and", "Laryngotracheal airway", ["Salivary ducts only", "Retina only", "Thyroid follicles only"], "Airway cartilage involvement can be life-threatening."),
        q("A patient has painful red ear cartilage sparing lobule, saddle nose and hoarseness. What is likely", "Relapsing polychondritis", ["Mumps", "Vocal nodule", "Simple otitis externa"], "Multisite cartilage inflammation suggests relapsing polychondritis.", True),
        q("Sarcoidosis in ENT may present with nasal crusting, parotid enlargement and", "Facial nerve palsy", ["Posterior epistaxis only", "Sialolithiasis always", "BPPV"], "Heerfordt syndrome includes parotid swelling and facial palsy."),
        q("Sjögren syndrome causes dry mouth due to", "Autoimmune salivary gland destruction", ["Wharton duct trauma only", "Stapes fixation", "Nasal valve collapse"], "Lymphocytic gland damage reduces saliva."),
        q("A woman has dry eyes, dry mouth, recurrent dental caries and parotid enlargement. What does this suggest", "Sjögren syndrome", ["Atrophic rhinitis only", "Mucormycosis", "Otosclerosis"], "Sicca symptoms with parotid involvement suggest Sjögren disease.", True),
        q("IgG4-related disease may cause salivary gland enlargement and", "Fibroinflammatory mass-like lesions", ["Acute viral croup only", "Foreign body aspiration", "Benign nasal cycle"], "IgG4 disease can mimic tumors in salivary and lacrimal glands."),
        q("Behçet disease is associated with recurrent oral ulcers and", "Genital ulcers with uveitis", ["Stapes fixation", "Mumps orchitis only", "Thyroid storm"], "Recurrent oral-genital ulceration and eye disease suggest Behçet disease."),
        q("A patient has recurrent painful oral ulcers, genital ulcers and eye inflammation. What is the diagnosis", "Behçet disease", ["Oral candidiasis", "Leukoplakia", "Ranula"], "The recurrent oral-genital-ocular pattern is classic.", True),
        q("Autoimmune inner ear disease is suspected when sensorineural hearing loss is rapidly progressive and", "Steroid responsive", ["Always conductive", "Only due to wax", "Present only at birth"], "Immune-mediated hearing loss may respond to steroids if treated early.", True),
    ]),
    ("ENT Manifestations of Emerging and Zoonotic Infections", [
        q("Tuberculous cervical lymphadenitis commonly presents as", "Chronic matted neck nodes", ["Acute watery rhinorrhea", "Blue ranula", "Meal-time parotid colic"], "TB nodes are chronic and may mat or form sinuses."),
        q("Laryngeal tuberculosis typically causes hoarseness with", "Painful ulcerative laryngeal lesions", ["Painless parotid stone", "Nasal polyps only", "BPPV"], "Laryngeal TB can mimic malignancy and is infectious."),
        q("A patient with pulmonary TB develops hoarseness and painful swallowing. What should be suspected", "Laryngeal tuberculosis", ["Vocal nodule only", "Mumps", "Otosclerosis"], "TB can involve the larynx and cause ulcerative lesions.", True),
        q("Diphtheria remains important because the pseudomembrane can cause airway obstruction and toxin can cause", "Myocarditis", ["Otosclerosis", "Sialolithiasis", "Barrett oesophagus"], "Diphtheria toxin can damage heart and nerves."),
        q("Fungal otitis externa is more common with humidity, ear instrumentation and", "Antibiotic drop overuse", ["Low iodine", "HPV vaccine", "Voice therapy"], "Moisture and altered flora promote otomycosis."),
        q("A patient has intense ear itching with black fungal debris after repeated antibiotic ear drops. What is likely", "Otomycosis", ["Mumps", "BPPV", "Cholesteatoma always"], "Pruritus and black/white fungal debris suggest otomycosis.", True),
        q("Mpox can produce ENT complaints including fever, lymphadenopathy and", "Oropharyngeal lesions", ["Stapes fixation", "Thyroid storm", "Sialolithiasis"], "Mucosal lesions may involve the mouth and throat."),
        q("Dengue can present to ENT with epistaxis because of", "Thrombocytopenia and capillary fragility", ["Vocal cord palsy", "Mucor invasion", "Wharton duct obstruction"], "Platelet drop and vascular leak increase bleeding tendency."),
        q("A febrile patient during dengue season has gum bleeding, epistaxis and low platelets. What is the ENT relevance", "Bleeding risk during nasal/oral procedures", ["Need for tonsillectomy", "Diagnosis of otosclerosis", "Immediate radioiodine"], "Thrombocytopenia changes procedural risk and epistaxis management.", True),
        q("Recent infection-control practice in ENT emphasizes screening, PPE and ventilation because many procedures generate", "Aerosols", ["Thyroid hormones", "Endolymph", "Salivary stones"], "Endoscopy, suction and airway procedures can aerosolize secretions.", True),
    ]),
    ("Newer Diagnostics, Biologics and Technology in ENT", [
        q("Nasal endoscopy has improved ENT diagnosis by allowing direct visualization of", "Hidden sinonasal and nasopharyngeal disease", ["Serum TSH", "Cochlear potentials only", "Bone marrow"], "Endoscopy shows areas missed by simple anterior rhinoscopy."),
        q("Cone-beam CT is increasingly useful in selected ENT/dental overlap for", "Bony sinonasal and odontogenic assessment", ["Taste testing", "Pure voice therapy", "Sleep scoring only"], "It can define dental roots, maxillary sinus floor and bony anatomy."),
        q("A patient has unilateral maxillary sinusitis after dental implant. Which imaging helps define odontogenic relation", "CT or cone-beam CT", ["Audiogram", "Rinne test", "Sialography only"], "Cross-sectional bony imaging shows dental-sinus communication.", True),
        q("Biologics for severe nasal polyposis are considered when disease remains uncontrolled despite surgery and", "Appropriate topical medical therapy", ["No diagnosis", "Only mild cold", "Simple septal spur"], "They are reserved for selected severe type 2 inflammatory disease."),
        q("Dupilumab targets signaling involving", "IL-4 and IL-13", ["Calcitonin", "Dopamine", "Thyroglobulin"], "Dupilumab blocks IL-4 receptor alpha, affecting IL-4/IL-13 pathways."),
        q("An asthmatic patient has recurrent severe nasal polyposis despite surgery and steroids. What newer option may help", "Biologic therapy for type 2 inflammation", ["Repeated blind avulsion", "Radioiodine", "Myringoplasty"], "Selected CRSwNP patients benefit from biologics.", True),
        q("High-resolution imaging before endoscopic sinus surgery helps identify", "Skull base and orbital risk anatomy", ["Stapes reflex only", "Tongue taste", "Parotid saliva pH"], "CT road-mapping reduces surgical risk."),
        q("Navigation-guided sinus surgery is most useful in revision, extensive disease or", "Distorted anatomy near skull base/orbit", ["Simple anterior epistaxis", "Routine wax removal", "Minor aphthae"], "Navigation supports orientation in high-risk anatomy."),
        q("A revision FESS patient has absent landmarks and disease near skull base. What technology may improve orientation", "Image-guided navigation", ["Pure tone audiometry", "Epley maneuver", "Sistrunk operation"], "Navigation is helpful when anatomy is distorted.", True),
        q("Point-of-care ultrasound in salivary disease can quickly detect", "Ductal stones or abscess", ["HPV genotype always", "Olfactory threshold", "Vocal pitch"], "Ultrasound is useful for accessible salivary gland swelling.", True),
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
                "id": f"ent-recent-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ENT recent diseases question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ENT recent diseases questions.")


if __name__ == "__main__":
    main()
