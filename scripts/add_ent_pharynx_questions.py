import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ent"
SUBJECT_TITLE = "ENT"
CHAPTER = "Diseases of Pharynx"
CHAPTER_ORDER = 4
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
        (". The diagnosis is", ". What is the diagnosis?"),
        (". The next step is", ". What is the next step?"),
        (". The best treatment is", ". What is the best treatment?"),
        (". This suggests", ". What does this suggest?"),
        (". This points toward", ". What does this point toward?"),
    ]
    for old, new in replacements:
        if prompt.endswith(old):
            return f"{prompt[:-len(old)]}{new}"
    if prompt.lower().endswith(("what does this suggest", "what is the most likely diagnosis", "what is the next step", "what is the best treatment")):
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
    ("Pharyngeal Anatomy, Waldeyer Ring and Examination", [
        q("Waldeyer ring includes palatine tonsils, adenoids, tubal tonsils and", "Lingual tonsils", ["Parotid glands", "Inferior turbinates", "Vocal folds"], "Waldeyer ring is lymphoid tissue around the naso-oropharyngeal inlet."),
        q("The palatine tonsil lies between palatoglossal and", "Palatopharyngeal arches", ["Salpingopharyngeal folds", "Aryepiglottic folds", "Plica semilunaris"], "The tonsillar fossa is bounded by anterior and posterior pillars."),
        q("A child has mouth breathing, hyponasal voice and a dull tympanic membrane. What does this suggest", "Adenoid hypertrophy with eustachian tube dysfunction", ["Otosclerosis", "Meniere disease", "Vocal cord palsy"], "Adenoids can obstruct the choanae and eustachian tube opening.", True),
        q("The tonsillar bed is formed mainly by the", "Superior constrictor muscle", ["Masseter", "Stylopharyngeus only", "Mylohyoid"], "The tonsil lies on the superior constrictor, separated by capsule and loose areolar tissue."),
        q("The main arterial supply at risk in tonsillectomy comes from branches including the", "Tonsillar branch of facial artery", ["Middle meningeal artery", "Internal carotid terminal bifurcation", "Ophthalmic artery"], "The tonsillar branch of facial artery is an important contributor."),
        q("A patient bleeds from the tonsillar fossa after tonsillectomy. The vessel most classically implicated is", "Tonsillar branch of facial artery", ["Anterior ethmoidal artery", "Superficial temporal artery", "Inferior thyroid artery"], "Post-tonsillectomy bleeding often arises from tonsillar bed vessels.", True),
        q("Flexible nasopharyngoscopy helps evaluate the pharynx because it can assess", "Nasopharynx, oropharynx, hypopharynx and laryngeal inlet", ["Cochlear hair cells", "Middle ear ossicles only", "Retina"], "Flexible scope allows dynamic upper aerodigestive tract assessment."),
        q("The vallecula lies between the tongue base and", "Epiglottis", ["Soft palate", "Posterior choana", "Cricoid cartilage"], "Valleculae are paired depressions anterior to the epiglottis."),
        q("A fish bone is suspected but oral examination is normal. Flexible endoscopy is useful to inspect the", "Tongue base, vallecula and pyriform fossae", ["External auditory canal", "Nasal valve only", "Lacrimal sac"], "Foreign bodies commonly lodge in hidden hypopharyngeal recesses.", True),
        q("The pyriform fossa is clinically important because it may lodge foreign bodies and lies beside the", "Laryngeal inlet", ["Nasal septum", "Middle ear", "Parotid duct"], "Sharp objects in the pyriform fossa can injure nearby mucosa and laryngeal structures.", True),
    ]),
    ("Acute Pharyngitis, Tonsillitis and Membranous Infections", [
        q("The commonest cause of acute pharyngitis is", "Viral infection", ["Tuberculosis", "Otosclerosis", "Salivary calculus"], "Most sore throats are viral and self-limited."),
        q("Group A streptococcal tonsillitis is important because it may lead to", "Rheumatic fever and glomerulonephritis", ["Meniere disease", "Septal perforation", "Otosclerosis"], "Streptococcal infection can trigger immune-mediated complications."),
        q("A child has fever, sore throat, tonsillar exudate and tender anterior cervical nodes without cough. The likely diagnosis is", "Streptococcal tonsillitis", ["Allergic rhinitis", "Atrophic rhinitis", "BPPV"], "Centor features increase likelihood of group A streptococcal infection.", True),
        q("Infectious mononucleosis is commonly caused by", "Epstein-Barr virus", ["Mumps virus", "Rhinovirus only", "Candida albicans"], "EBV causes fever, tonsillitis, lymphadenopathy and atypical lymphocytosis."),
        q("Ampicillin rash after treatment of exudative tonsillitis suggests underlying", "Infectious mononucleosis", ["Diphtheria always", "Oral cancer", "Peritonsillar abscess only"], "Aminopenicillin rash is classic in EBV infection."),
        q("A teenager has fever, massive tonsils, generalized lymphadenopathy and splenomegaly. What is the most likely diagnosis", "Infectious mononucleosis", ["Acute epiglottitis", "Nasopharyngeal carcinoma", "Sialolithiasis"], "Systemic lymphadenopathy and splenomegaly point to EBV.", True),
        q("Diphtheria classically produces a pharyngeal membrane that", "Bleeds on attempted removal", ["Is always painless and removable", "Contains only food debris", "Appears only on the tongue tip"], "The pseudomembrane is adherent and removal can cause bleeding."),
        q("Treatment of suspected diphtheria requires antitoxin plus", "Erythromycin or penicillin", ["Only saline gargle", "Stapedotomy", "Antihistamine alone"], "Antitoxin neutralizes toxin; antibiotics eradicate organisms."),
        q("A child with sore throat has a gray adherent membrane and toxic appearance. What is the next step", "Give diphtheria antitoxin without waiting for culture", ["Scrape the membrane repeatedly", "Observe without isolation", "Do Epley maneuver"], "Clinical suspicion warrants urgent antitoxin and isolation.", True),
        q("Vincent angina is associated with fusospirochetal infection and causes", "Ulceromembranous tonsillitis with foul breath", ["Meal-time parotid swelling", "Posterior epistaxis", "Vertigo"], "Fusobacteria and spirochetes can cause necrotic ulcerative tonsillitis.", True),
    ]),
    ("Chronic Tonsillitis and Indications for Tonsillectomy", [
        q("Chronic tonsillitis commonly produces", "Recurrent sore throat with tonsillar crypt debris", ["Pulsatile tinnitus", "Watery rhinorrhea", "Facial nerve palsy"], "Cryptic infected tonsils may cause recurrent attacks and halitosis."),
        q("Tonsilloliths form due to accumulation of debris in", "Tonsillar crypts", ["Pyriform sinus apex", "Nasolacrimal duct", "Stensen duct"], "Keratin, bacteria and food debris can calcify in crypts."),
        q("A student has repeated tonsillitis episodes, halitosis and cheesy material from tonsillar crypts. What does this suggest", "Chronic tonsillitis", ["Juvenile angiofibroma", "Atrophic rhinitis", "Meniere disease"], "Recurrent infection with crypt debris fits chronic tonsillitis.", True),
        q("One accepted indication for tonsillectomy is", "Recurrent documented acute tonsillitis meeting frequency criteria", ["One mild viral cold", "Simple nasal allergy", "Asymptomatic small tonsils"], "Frequent disabling documented attacks may justify surgery."),
        q("Tonsillectomy is also considered for tonsillar asymmetry when there is concern for", "Malignancy", ["Otosclerosis", "BPPV", "Cerumen"], "Unexplained asymmetric tonsil, especially with risk factors or nodes, needs evaluation."),
        q("An adult smoker has unilateral tonsillar enlargement and a firm neck node. The priority is", "Evaluation for malignancy", ["Routine antihistamine only", "Wax syringing", "Epley maneuver"], "Asymmetry plus cervical node is a cancer red flag.", True),
        q("Primary post-tonsillectomy hemorrhage occurs within", "24 hours", ["7 to 10 days only", "6 months", "2 years"], "Primary hemorrhage is immediate or within the first day."),
        q("Secondary post-tonsillectomy hemorrhage commonly occurs around", "5 to 10 days", ["First 5 minutes only", "One year", "Before surgery"], "Slough separation and infection can cause delayed bleeding."),
        q("A child bleeds from the mouth 7 days after tonsillectomy. What is the likely type of hemorrhage", "Secondary post-tonsillectomy hemorrhage", ["Primary hemorrhage", "Physiologic healing only", "Posterior epistaxis always"], "Bleeding about a week later is secondary hemorrhage until controlled.", True),
        q("A dangerous complication of tonsillectomy anesthesia induction in obstructive sleep apnea is", "Airway obstruction", ["Stapes fixation", "Sialolithiasis", "Atrophic rhinitis"], "Large tonsils and OSA increase perioperative airway risk.", True),
    ]),
    ("Adenoid Disease and Adenoidectomy", [
        q("Adenoids are located in the", "Nasopharynx", ["Pyriform sinus", "Vallecula", "Floor of mouth"], "The pharyngeal tonsil lies in the roof and posterior wall of nasopharynx."),
        q("Adenoid hypertrophy commonly causes mouth breathing, snoring and", "Hyponasal speech", ["Conductive aphonia", "Pulsatile tinnitus only", "Tongue deviation"], "Nasopharyngeal obstruction reduces nasal resonance."),
        q("A child has chronic mouth breathing, snoring, open-mouth facies and recurrent otitis media with effusion. What is the likely diagnosis", "Adenoid hypertrophy", ["Peritonsillar abscess", "Hypopharyngeal cancer", "Oral candidiasis"], "Adenoids can obstruct nasal airway and eustachian tube function.", True),
        q("Adenoid facies is associated with long-standing", "Nasal obstruction in childhood", ["Acute otitis externa", "Meniere attacks", "Septal perforation only"], "Chronic mouth breathing can alter facial growth pattern."),
        q("Adenoidectomy may improve otitis media with effusion by", "Relieving eustachian tube obstruction and reservoir infection", ["Fixing the stapes", "Removing tongue base tumors", "Treating BPPV"], "Adenoids obstruct and harbor infection near the eustachian tube opening."),
        q("A child with persistent glue ear and large adenoids needs surgery. The procedure added to grommet insertion may be", "Adenoidectomy", ["Stapedotomy", "Parotidectomy", "Septal cautery"], "Adenoidectomy can reduce recurrence in selected children.", True),
        q("Adenoidectomy is avoided or planned carefully in patients with", "Submucous cleft palate", ["Cerumen impaction", "Mild allergic rhinitis", "Geographic tongue"], "Removing adenoids can worsen velopharyngeal insufficiency in palatal defects."),
        q("Velopharyngeal insufficiency after adenoidectomy presents with", "Hypernasal speech and nasal regurgitation", ["Hyponasal speech only", "Vertigo", "Posterior epistaxis"], "Poor palatal closure allows air and fluids into the nose."),
        q("After adenoidectomy, a child develops hypernasal speech and nasal regurgitation. What does this suggest", "Velopharyngeal insufficiency", ["Mumps", "Peritonsillar abscess", "Sialolithiasis"], "Adenoids may have helped compensate for poor palatal closure.", True),
        q("Endoscopic assessment of adenoids is useful because it shows", "Size and relation to choanae and eustachian tube cushions", ["Cochlear function", "Stapes mobility", "Tongue taste only"], "Endoscopy directly grades nasopharyngeal obstruction.", True),
    ]),
    ("Peritonsillar, Parapharyngeal and Retropharyngeal Abscess", [
        q("Peritonsillar abscess is also called", "Quinsy", ["Noma", "Ranula", "Pott puffy tumor"], "Quinsy is pus between tonsillar capsule and superior constrictor."),
        q("Classic peritonsillar abscess causes unilateral sore throat, muffled voice and", "Uvula deviation away from the affected side", ["Bilateral nasal polyps", "Facial palsy", "Watery rhinorrhea"], "The swollen peritonsillar area pushes the uvula medially and away."),
        q("A young adult has severe unilateral throat pain, trismus, hot-potato voice and uvula displaced to the left. The abscess is likely on the", "Right peritonsillar region", ["Left nasal cavity", "Right parotid tail", "Left pyriform sinus"], "The uvula deviates away from the affected peritonsillar swelling.", True),
        q("Treatment of peritonsillar abscess includes antibiotics and", "Needle aspiration or incision and drainage", ["Cochlear implant", "Long-term nasal decongestant", "Watchful waiting only"], "Pus must usually be drained in addition to antimicrobial therapy."),
        q("Retropharyngeal abscess is especially common in young children because of", "Prominent retropharyngeal lymph nodes", ["Large stapes footplate", "Adult dentition", "Absent tonsils"], "These nodes involute with age but can suppurate in children."),
        q("A toddler has fever, neck stiffness, drooling and posterior pharyngeal wall bulge. What is the most likely diagnosis", "Retropharyngeal abscess", ["Aphthous ulcer", "Allergic rhinitis", "Otosclerosis"], "Posterior wall bulge with toxicity and neck stiffness is typical.", True),
        q("Danger space infection is feared because it can spread to the", "Mediastinum", ["Middle ear only", "Orbit only", "Parotid duct"], "The danger space extends from skull base to posterior mediastinum."),
        q("Parapharyngeal abscess may present with medial bulge of tonsil and", "Trismus with neck swelling", ["Pure watery rhinorrhea", "Bilateral itchy eyes", "Painless lip cyst"], "Deep lateral pharyngeal infection affects masticator region and neck."),
        q("A dental infection is followed by fever, neck swelling, trismus and medial pharyngeal wall bulge. What does this suggest", "Parapharyngeal space abscess", ["Simple chronic tonsillitis", "Viral coryza", "Ranula"], "Dental sepsis can spread to the parapharyngeal space.", True),
        q("Airway assessment is urgent in deep neck abscess because swelling can cause", "Sudden airway compromise", ["Stapes fixation", "Sensorineural presbycusis", "Benign nasal cycle"], "Pharyngeal edema and mass effect can obstruct the upper airway.", True),
    ]),
    ("Nasopharyngeal Disorders and Nasopharyngeal Carcinoma", [
        q("The fossa of Rosenmüller is an important site for", "Nasopharyngeal carcinoma", ["Ranula", "Peritonsillar abscess", "Warthin tumor"], "NPC commonly arises in the lateral nasopharyngeal recess."),
        q("Nasopharyngeal carcinoma is strongly associated with", "Epstein-Barr virus", ["Coxsackie virus only", "Mumps vaccine", "Candida albicans"], "EBV association is important in endemic NPC."),
        q("An adult has unilateral otitis media with effusion and a neck node. What is the most important diagnosis to exclude", "Nasopharyngeal carcinoma", ["Allergic rhinitis only", "BPPV", "Cerumen impaction"], "Adult unilateral OME can result from eustachian tube obstruction by NPC.", True),
        q("The most common presenting feature of nasopharyngeal carcinoma may be", "Cervical lymph node metastasis", ["Meal-time salivary colic", "Lower lip mucocele", "Pinna perichondritis"], "NPC often spreads early to upper cervical nodes."),
        q("Endoscopic biopsy for suspected nasopharyngeal carcinoma should target the", "Nasopharyngeal mass or fossa of Rosenmüller", ["Normal inferior turbinate only", "External canal", "Tonsillar crypt stone"], "Tissue diagnosis comes from the suspicious nasopharyngeal lesion."),
        q("A patient has nasal obstruction, blood-stained postnasal drip, serous otitis media and level II neck nodes. The likely diagnosis is", "Nasopharyngeal carcinoma", ["Acute tonsillitis", "Adenoid hypertrophy only", "Sialolithiasis"], "Nasal, ear and nodal symptoms together are classic NPC clues.", True),
        q("Primary treatment of nasopharyngeal carcinoma is usually", "Radiotherapy with chemotherapy for appropriate stages", ["Simple adenoidectomy", "Tonsillectomy alone", "Sialendoscopy"], "NPC is radiosensitive and often managed non-surgically."),
        q("Skull base involvement in nasopharyngeal carcinoma may cause", "Cranial nerve palsies", ["Lower lip cyst", "Watery eyes only", "Wax impaction"], "Superior spread can involve skull base foramina and cranial nerves."),
        q("A patient with known NPC develops diplopia from abducens palsy. What does this suggest", "Skull base involvement", ["Simple viral pharyngitis", "Ranula", "Aphthous ulcer"], "CN VI palsy can occur with skull base or cavernous sinus extension.", True),
        q("Adenoids are unusual as a new obstructive mass in adults; persistent adult nasopharyngeal mass needs", "Endoscopic evaluation and biopsy when suspicious", ["Blind cautery only", "No follow-up", "Epley maneuver"], "Adult nasopharyngeal masses require exclusion of malignancy.", True),
    ]),
    ("Hypopharyngeal Disorders, Dysphagia and Foreign Bodies", [
        q("The hypopharynx includes pyriform sinuses, posterior pharyngeal wall and", "Postcricoid region", ["Inferior meatus", "Middle ear", "Hard palate"], "These are the major subsites of hypopharynx."),
        q("Plummer-Vinson syndrome includes dysphagia, iron deficiency anemia and", "Postcricoid web", ["Adenoid hypertrophy", "Wharton duct stone", "Cholesteatoma"], "It is associated with upper esophageal/postcricoid web and cancer risk."),
        q("A middle-aged woman has dysphagia, iron deficiency anemia and a postcricoid web. What is the diagnosis", "Plummer-Vinson syndrome", ["Ludwig angina", "Mumps", "Quinsy"], "The triad is classic and has malignant potential.", True),
        q("Zenker diverticulum is a pulsion diverticulum through", "Killian dehiscence", ["Foramen ovale", "Little area", "Wharton duct"], "It herniates through a weak area above the cricopharyngeus."),
        q("Zenker diverticulum commonly presents with dysphagia, regurgitation and", "Halitosis", ["Epistaxis", "Vertigo", "Parotid colic"], "Food retention leads to regurgitation, cough and bad breath."),
        q("An elderly patient regurgitates undigested food hours after meals and has gurgling in the neck. The likely diagnosis is", "Zenker diverticulum", ["Peritonsillar abscess", "Aphthous ulcer", "Allergic rhinitis"], "Delayed regurgitation of undigested food is typical.", True),
        q("A sharp fish bone most commonly lodges in the tonsil, tongue base or", "Pyriform fossa", ["Stensen duct", "Middle meatus", "External canal"], "The pyriform fossa is a common hidden site for fish bones."),
        q("Persistent foreign body sensation after fish bone ingestion with normal oral exam should be evaluated by", "Flexible endoscopy", ["Only reassurance in every case", "Audiometry", "Nasal cautery"], "Endoscopy can inspect tongue base, vallecula and hypopharynx."),
        q("A patient has odynophagia after fish meal and pooling of saliva in one pyriform fossa. What is the next step", "Urgent endoscopic assessment and removal if seen", ["Forceful blind finger sweep", "Long-term antihistamine", "Stapedotomy"], "Pooling and symptoms suggest retained foreign body or injury.", True),
        q("Button battery impaction in the pharynx or esophagus requires", "Emergency removal", ["Observation for spontaneous dissolution", "Delayed removal after a week", "Nasal steroid only"], "Button batteries cause rapid caustic injury and perforation risk.", True),
    ]),
    ("Sleep-Disordered Breathing and Pharyngeal Obstruction", [
        q("Obstructive sleep apnea is caused by repeated collapse of the", "Upper airway during sleep", ["External auditory canal", "Lacrimal duct", "Middle ear"], "Pharyngeal soft tissue collapse produces apneas and hypopneas."),
        q("Common symptoms of obstructive sleep apnea include loud snoring, witnessed apneas and", "Excessive daytime sleepiness", ["Pulsatile tinnitus", "Meal-time salivary swelling", "Watery rhinorrhea"], "Sleep fragmentation produces daytime somnolence."),
        q("An obese man snores loudly, has witnessed apneas and morning headaches. The investigation of choice is", "Polysomnography", ["Pure tone audiometry", "Sialography", "Dix-Hallpike test"], "Sleep study confirms OSA severity.", True),
        q("The apnea-hypopnea index measures", "Number of apneas and hypopneas per hour of sleep", ["Tonsil size only", "Nasal bone angle", "Salivary flow"], "AHI quantifies OSA severity."),
        q("First-line treatment for moderate to severe adult OSA is commonly", "CPAP", ["Tonsillectomy for every adult", "Antibiotics alone", "Epley maneuver"], "CPAP splints the upper airway open during sleep."),
        q("A patient with severe OSA is started on a machine that maintains positive airway pressure overnight. What is this treatment", "CPAP therapy", ["Sialendoscopy", "Septal cautery", "Myringoplasty"], "Continuous positive airway pressure prevents pharyngeal collapse.", True),
        q("Large tonsils in a child with OSA are commonly treated with", "Adenotonsillectomy", ["Stapedotomy", "Parotidectomy", "Nasal packing"], "Adenotonsillar hypertrophy is a common pediatric OSA cause."),
        q("A child has snoring, witnessed apneas, poor school performance and large tonsils. The likely treatment is", "Adenotonsillectomy after appropriate assessment", ["Long-term decongestant abuse", "Cochlear implant", "Observation despite severe symptoms"], "Symptomatic pediatric OSA with adenotonsillar hypertrophy often needs surgery.", True),
        q("Drug-induced sedation can worsen OSA by", "Reducing pharyngeal muscle tone", ["Increasing stapes movement", "Opening Wharton duct", "Removing adenoids"], "Sedatives reduce airway tone and arousal responses."),
        q("Untreated OSA may contribute to systemic hypertension because of", "Intermittent hypoxia and sympathetic activation", ["Pure tongue taste loss", "Cerumen impaction", "Benign nasal cycle"], "Repeated hypoxia and arousals increase cardiovascular stress.", True),
    ]),
    ("Pharyngeal Trauma, Burns and Caustic Injuries", [
        q("Thermal injury to the pharynx is dangerous because edema may cause", "Airway obstruction", ["Stapes fixation", "Submandibular stone", "BPPV"], "Upper airway burns can swell rapidly after injury."),
        q("Caustic alkali ingestion tends to cause", "Liquefactive necrosis", ["Only superficial dryness", "Stapes ankylosis", "Benign aphthae"], "Alkalis penetrate deeply through liquefactive necrosis."),
        q("A child drinks drain cleaner and has drooling, oral burns and stridor. What is the next step", "Urgent airway assessment", ["Induce vomiting", "Blind nasogastric tube insertion", "Give only lozenges"], "Airway compromise must be assessed before GI evaluation.", True),
        q("Vomiting should be avoided after caustic ingestion because it may", "Re-expose tissues and worsen injury", ["Neutralize all alkali", "Prevent strictures", "Cure perforation"], "Emesis can repeat caustic contact and risk aspiration."),
        q("Rigid endoscopy after caustic ingestion is performed selectively to assess", "Extent and severity of mucosal injury", ["Hearing thresholds", "Nasal cycle", "Salivary stone size only"], "Endoscopy grades injury when safe and indicated."),
        q("A patient develops progressive dysphagia weeks after caustic ingestion. This suggests", "Pharyngoesophageal stricture", ["Acute viral pharyngitis", "Mumps", "Adenoid hypertrophy"], "Healing by fibrosis can narrow the pharynx or esophagus.", True),
        q("Penetrating pharyngeal trauma raises concern for", "Deep neck infection and vascular injury", ["Simple allergic rhinitis", "Otosclerosis", "Geographic tongue"], "The pharynx lies near major vessels and deep spaces."),
        q("Surgical emphysema after pharyngeal injury suggests", "Aerodigestive tract perforation", ["Benign tonsillolith", "Oral candidiasis", "Meniere disease"], "Air leaking into soft tissues indicates mucosal breach."),
        q("After endoscopy, a patient develops neck pain, fever and crepitus. What does this suggest", "Pharyngeal or esophageal perforation", ["Aphthous ulcer", "Warthin tumor", "Allergic rhinitis"], "Crepitus with systemic signs after instrumentation is perforation until excluded.", True),
        q("Initial management of suspected pharyngeal perforation includes nil per oral, antibiotics and", "Urgent specialist evaluation with imaging/endoscopy as indicated", ["Immediate oral feeding", "Forceful blind probing", "Nasal steroid only"], "Early control of contamination prevents deep neck sepsis.", True),
    ]),
    ("Oropharyngeal and Hypopharyngeal Tumors", [
        q("The commonest malignancy of the oropharynx is", "Squamous cell carcinoma", ["Pleomorphic adenoma", "Warthin tumor", "Osteoma"], "Most pharyngeal mucosal cancers are squamous carcinomas."),
        q("HPV-positive oropharyngeal carcinoma commonly arises in the", "Tonsil and base of tongue", ["Inferior turbinate", "Parotid tail", "Middle ear"], "HPV-related tumors often originate in lymphoid crypt epithelium."),
        q("A middle-aged nonsmoker has a cystic neck node and small tonsillar primary. What does this suggest", "HPV-associated oropharyngeal carcinoma", ["Mumps", "Peritonsillar abscess", "Ranula"], "HPV-positive cancers can present with cystic nodal metastasis.", True),
        q("Tobacco and alcohol are major risks for", "HPV-negative pharyngeal squamous carcinoma", ["Adenoid hypertrophy", "Simple tonsillolith", "Zenker diverticulum"], "Classic upper aerodigestive SCC risk is tobacco plus alcohol."),
        q("Hypopharyngeal carcinoma often presents late because early symptoms are", "Vague or minimal", ["Always dramatic airway obstruction", "Always painless visible lip mass", "Always bilateral epistaxis"], "The hypopharynx is hidden, so tumors may present with advanced disease."),
        q("An older smoker has progressive dysphagia, referred otalgia and weight loss. The likely diagnosis is", "Hypopharyngeal carcinoma", ["Aphthous ulcer", "Adenoid hypertrophy", "Mumps"], "Dysphagia with referred ear pain and weight loss is a malignancy warning pattern.", True),
        q("Referred otalgia in oropharyngeal carcinoma occurs through", "Glossopharyngeal nerve pathways", ["Optic nerve", "Hypoglossal nerve only", "Phrenic nerve"], "CN IX supplies tonsillar/oropharyngeal sensation and refers pain to the ear."),
        q("A suspicious tonsillar ulcer with neck node should be evaluated with", "Endoscopy, biopsy and staging imaging", ["Only repeated antibiotics", "No follow-up", "Dix-Hallpike test"], "Cancer workup needs tissue diagnosis and staging."),
        q("A patient has unilateral tonsillar ulcer, trismus and firm level II node. What is the next step", "Biopsy with complete head-neck evaluation", ["Reassurance only", "Immediate adenoidectomy", "Sialolithotomy"], "Persistent ulcer with node and trismus needs malignancy evaluation.", True),
        q("Treatment selection for pharyngeal cancer depends on site, stage, function and usually involves", "Surgery, radiotherapy, chemotherapy or combinations", ["Antihistamines only", "Grommet insertion", "Epley maneuver"], "Management is multidisciplinary and stage-specific.", True),
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
                "id": f"ent-pharynx-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ENT pharynx question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ENT pharynx questions.")


if __name__ == "__main__":
    main()
