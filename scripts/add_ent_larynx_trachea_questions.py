import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ent"
SUBJECT_TITLE = "ENT"
CHAPTER = "Diseases of Larynx and Trachea"
CHAPTER_ORDER = 5
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
    ("Laryngeal Anatomy, Physiology and Examination", [
        q("The true vocal cords are covered mainly by", "Stratified squamous epithelium", ["Ciliated respiratory epithelium only", "Transitional epithelium", "Keratinized skin"], "The vibrating edge of the true cord is adapted to friction."),
        q("The only abductor of the vocal cord is", "Posterior cricoarytenoid", ["Lateral cricoarytenoid", "Interarytenoid", "Cricothyroid"], "Posterior cricoarytenoid opens the glottis."),
        q("A thyroidectomy patient develops a breathy voice and aspiration on drinking. What does this suggest", "Recurrent laryngeal nerve palsy", ["Posterior epistaxis", "Otosclerosis", "Ranula"], "RLN injury impairs vocal fold closure and airway protection.", True),
        q("The cricothyroid muscle is supplied by", "External branch of superior laryngeal nerve", ["Internal laryngeal nerve", "Hypoglossal nerve", "Glossopharyngeal nerve"], "The external superior laryngeal nerve tenses the vocal fold via cricothyroid."),
        q("Flexible laryngoscopy is useful because it assesses", "Vocal cord mobility and laryngeal mucosa", ["Stapes fixation", "Retinal fields", "Wharton duct stones"], "Awake flexible examination shows structure and movement."),
        q("A singer cannot reach high notes after thyroid surgery but has mobile vocal cords. The injured nerve is likely", "External superior laryngeal nerve", ["Recurrent laryngeal nerve", "Facial nerve", "Lingual nerve"], "Cricothyroid weakness affects pitch control.", True),
        q("The narrowest part of the adult upper airway is generally the", "Glottis", ["Nasopharynx", "Oral vestibule", "Tracheal carina"], "The adult laryngeal airway is narrowest at the glottic level."),
        q("The pediatric airway is relatively narrow at the", "Subglottis/cricoid region", ["Piriform fossa", "Hard palate", "External nose"], "The cricoid/subglottis is a key pediatric airway narrowing."),
        q("A child has mild subglottic swelling but marked stridor. This happens because airway resistance rises sharply as radius falls, according to", "Poiseuille law", ["Weber law", "Boyle law only", "Rinne principle"], "Small decreases in radius greatly increase resistance.", True),
        q("The laryngeal inlet is protected during swallowing mainly by coordinated closure of the glottis and", "Epiglottic movement with laryngeal elevation", ["Stapes reflex", "Nasal cycle", "Parotid contraction"], "Airway protection depends on multiple coordinated laryngeal movements.", True),
    ]),
    ("Stridor and Acute Upper Airway Obstruction", [
        q("Inspiratory stridor usually indicates obstruction at or above the", "Extrathoracic upper airway", ["Alveoli", "Lower bronchioles only", "Pleural cavity"], "Extrathoracic narrowing produces inspiratory noise."),
        q("Biphasic stridor suggests fixed obstruction around the", "Glottis or subglottis", ["Nasal vestibule only", "Terminal bronchiole", "Esophagus"], "Fixed central upper-airway obstruction affects both inspiration and expiration."),
        q("A child has sudden choking, cough and unilateral reduced air entry after playing with peanuts. What is the most likely diagnosis", "Airway foreign body aspiration", ["Viral croup", "Epiglottitis", "Vocal nodule"], "Abrupt symptoms during play or eating suggest foreign body.", True),
        q("The first priority in severe stridor is", "Airway assessment and oxygenation", ["Detailed audiogram", "Elective voice therapy", "Routine nasal cautery"], "Airway safety comes before definitive diagnosis."),
        q("Drooling, tripod posture and toxic appearance in a child with stridor suggest", "Supraglottitis", ["Simple allergic rhinitis", "Otosclerosis", "Geographic tongue"], "Epiglottitis/supraglottitis can rapidly obstruct the airway."),
        q("A toxic febrile child sits forward, drools and has muffled voice. What is the next step", "Secure airway in a controlled setting", ["Force tongue depressor examination", "Send home with lozenges", "Do Epley maneuver"], "Agitating the child can precipitate obstruction; airway control is urgent.", True),
        q("Nebulized adrenaline is useful in croup because it", "Reduces subglottic mucosal edema", ["Kills all viruses", "Paralyzes vocal cords", "Removes foreign body"], "Alpha-adrenergic vasoconstriction temporarily reduces airway edema."),
        q("Steroids in croup are used to", "Reduce airway inflammation and relapse", ["Open Wharton duct", "Treat otosclerosis", "Stop all aspiration"], "Dexamethasone reduces severity and need for further care."),
        q("A child with barking cough, hoarseness and inspiratory stridor worsens at night. The likely diagnosis is", "Viral croup", ["Diphtheria", "Laryngeal cancer", "Zenker diverticulum"], "Barking cough and subglottic inflammation point to croup.", True),
        q("Complete airway obstruction with inability to cough or speak requires", "Immediate choking rescue maneuvers", ["Observation", "Oral antibiotics first", "Voice rest only"], "Ineffective cough and silent obstruction require emergency intervention.", True),
    ]),
    ("Acute and Chronic Laryngitis", [
        q("Acute laryngitis most commonly follows", "Viral upper respiratory infection", ["Stapes surgery", "Submandibular stone", "Adenoidectomy only"], "Viral inflammation causes acute hoarseness."),
        q("The main symptom of laryngitis is", "Hoarseness", ["Posterior epistaxis", "Meal-time swelling", "Conductive deafness"], "Inflammation alters vocal fold vibration."),
        q("A teacher develops hoarseness after a cold, with mild cough and no airway distress. What is the most likely diagnosis", "Acute viral laryngitis", ["Vocal cord carcinoma", "Bilateral abductor palsy", "Epiglottitis"], "Self-limited hoarseness after URI is typical.", True),
        q("Routine antibiotics are not needed in most acute laryngitis because it is usually", "Viral", ["Malignant", "Fungal invasive", "Traumatic fracture"], "Most cases improve with supportive care and voice rest."),
        q("Chronic laryngitis is strongly associated with smoking, reflux and", "Voice misuse", ["Cerumen", "Nasal dermoid", "Sialolithiasis"], "Persistent irritants and phonotrauma inflame the larynx."),
        q("A smoker has hoarseness lasting more than three weeks. What is the next step", "Laryngeal examination", ["Repeated cough syrup only", "Ignore until pain appears", "Wax syringing"], "Persistent hoarseness, especially in smokers, needs visualization to exclude cancer.", True),
        q("Laryngopharyngeal reflux may cause hoarseness with", "Throat clearing and globus", ["Pulsatile tinnitus", "Blue lip cyst", "Meal-time parotid pain"], "Reflux irritation can present without classic heartburn."),
        q("Voice rest in acute laryngitis means avoiding shouting and", "Whispering excessively", ["Drinking water", "Steam inhalation", "Normal quiet speech only"], "Whispering can strain the larynx; relative voice rest is preferred."),
        q("A professional voice user has chronic throat clearing, posterior laryngeal edema and worse morning voice. What does this suggest", "Laryngopharyngeal reflux", ["Mumps", "Acute otitis media", "Ranula"], "Posterior laryngeal irritation and globus are common reflux clues.", True),
        q("Chronic hyperkeratotic laryngitis in a smoker is important because it may hide", "Dysplasia or carcinoma", ["Simple croup only", "Otosclerosis", "Wharton duct stone"], "Persistent leukoplakic or keratotic lesions require evaluation and often biopsy.", True),
    ]),
    ("Benign Vocal Fold Lesions and Voice Disorders", [
        q("Vocal nodules are usually", "Bilateral symmetric lesions at the junction of anterior and middle thirds", ["Unilateral parotid masses", "Posterior choanal webs", "Subglottic cancers"], "Nodules occur at the maximal vibratory impact point."),
        q("Vocal polyps are often", "Unilateral phonotraumatic lesions", ["Always bilateral malignant tumors", "Congenital choanal blocks", "Salivary stones"], "Polyps are commonly unilateral and related to acute or chronic phonotrauma."),
        q("A school teacher has chronic hoarseness with bilateral small nodules on the free edge of both cords. What is the likely diagnosis", "Vocal nodules", ["Vocal cord carcinoma", "Papillomatosis", "Epiglottitis"], "Bilateral symmetric lesions in a voice user are nodules.", True),
        q("Initial treatment of vocal nodules usually includes", "Voice therapy and vocal hygiene", ["Total laryngectomy", "Tracheostomy for all cases", "Radiotherapy"], "Behavioral therapy treats the phonotraumatic cause."),
        q("Reinke edema is strongly associated with", "Smoking and voice abuse", ["Mumps", "Choanal atresia", "Sialolithiasis"], "Chronic irritation causes gelatinous swelling of superficial lamina propria."),
        q("A middle-aged smoker has a deep husky voice and bilateral floppy swollen vocal folds. What is the likely diagnosis", "Reinke edema", ["Acute croup", "Bilateral abductor palsy", "Laryngeal web"], "The classic voice is low-pitched and rough with bilateral cord edema.", True),
        q("Contact ulcer or granuloma commonly occurs over the", "Vocal process of arytenoid", ["Epiglottic tip only", "Submandibular duct", "Hard palate"], "Posterior glottic trauma or reflux affects the vocal process."),
        q("Functional dysphonia means voice disorder without", "Structural or neurologic lesion explaining symptoms", ["Any symptom", "Any laryngeal movement", "Any need for therapy"], "Functional voice disorders have abnormal use patterns without matching structural disease."),
        q("A patient has severe hoarseness, normal vocal cord anatomy and inconsistent voice during laughter. What does this suggest", "Functional dysphonia", ["Laryngeal cancer", "Epiglottitis", "Tracheal stenosis"], "Inconsistent normal automatic voice supports functional dysphonia.", True),
        q("Recurrent respiratory papillomatosis is caused by", "Human papillomavirus types 6 and 11", ["EBV only", "Mumps virus", "Candida"], "Low-risk HPV types cause recurrent laryngeal papillomas.", True),
    ]),
    ("Vocal Cord Paralysis and Neurogenic Laryngeal Disease", [
        q("Unilateral recurrent laryngeal nerve palsy commonly causes", "Hoarseness and weak cough", ["Posterior epistaxis", "Meal-time swelling", "Vertigo"], "Glottic insufficiency causes breathy voice and aspiration risk."),
        q("Bilateral abductor palsy classically presents with", "Stridor with relatively preserved voice", ["Silent aphonia without breathing issue", "Nasal obstruction only", "Parotid pain"], "Both cords lie near midline, narrowing airway while allowing voice."),
        q("After thyroid surgery, a patient has inspiratory stridor but can phonate fairly well. What is the likely diagnosis", "Bilateral abductor vocal cord palsy", ["Acute tonsillitis", "Mumps", "Vocal nodule"], "Bilateral cords in paramedian position cause airway obstruction.", True),
        q("Left recurrent laryngeal nerve palsy may be caused by lesions in the chest because the nerve loops around the", "Aortic arch", ["Right subclavian artery", "Carotid bifurcation", "Mandible"], "The left RLN has a long intrathoracic course."),
        q("A new left vocal cord palsy without surgical history should prompt evaluation of", "Neck and chest along the recurrent laryngeal nerve", ["Only external ear", "Only lower lip", "Only nasal vestibule"], "Malignancy or mediastinal disease must be excluded."),
        q("A smoker has hoarseness and left vocal cord paralysis. Chest imaging reveals an apical lung mass. What caused the palsy", "Left recurrent laryngeal nerve involvement", ["Facial nerve neuritis", "Lingual nerve injury", "Cricothyroid spasm"], "Thoracic tumors can involve the left RLN.", True),
        q("Superior laryngeal nerve palsy mainly affects", "Pitch control", ["Nasal airflow", "Salivary secretion", "Tongue protrusion"], "Cricothyroid weakness limits high-pitch phonation."),
        q("Medialization thyroplasty is used to improve voice in selected", "Unilateral vocal fold paralysis", ["Acute croup", "Mumps", "Nasal polyposis"], "Medializing a paralyzed fold improves glottic closure."),
        q("A patient aspirates liquids and has a breathy voice after vagal skull base surgery. What is the problem", "Glottic insufficiency from vocal fold paralysis", ["Choanal atresia", "Sialolithiasis", "Atrophic rhinitis"], "Poor cord closure causes aspiration and weak breathy phonation.", True),
        q("Laryngeal electromyography can help distinguish paralysis from", "Cricoarytenoid joint fixation", ["Posterior epistaxis", "Ranula", "Aphthous ulcer"], "EMG assesses denervation when cord immobility has uncertain cause.", True),
    ]),
    ("Laryngeal Trauma, Burns and Airway Stenosis", [
        q("Blunt laryngeal trauma is dangerous because it can cause", "Airway edema and framework fracture", ["Salivary stone", "Otitis media", "Nasal allergy"], "Swelling, hematoma or cartilage disruption can obstruct the airway."),
        q("Red flags after neck trauma include hoarseness, stridor, hemoptysis and", "Subcutaneous emphysema", ["Itchy eyes", "Meal-time pain", "Watery rhinorrhea"], "Air leak suggests airway mucosal disruption."),
        q("After a road accident, a patient has hoarseness, stridor and neck crepitus. What is the next step", "Secure airway with urgent specialist assessment", ["Send home on voice rest", "Blind nasogastric tube", "Routine antihistamine"], "Airway control and laryngeal evaluation are urgent.", True),
        q("Laryngeal web most often involves the", "Anterior glottis", ["Posterior choana", "Parotid duct", "Pyriform apex only"], "Congenital webs commonly affect the anterior commissure."),
        q("Subglottic stenosis after intubation is related to pressure injury at the", "Cuffed tube contact area", ["Tongue tip", "Palatine tonsil", "Nasal vestibule"], "Mucosal ischemia and scarring narrow the subglottis/trachea."),
        q("A patient develops exertional biphasic stridor weeks after prolonged ICU intubation. What is the likely diagnosis", "Post-intubation laryngotracheal stenosis", ["Vocal nodule", "Mumps", "Allergic rhinitis"], "Delayed fixed airway symptoms after intubation suggest stenosis.", True),
        q("Cotton-Myer grading is used for", "Subglottic stenosis severity", ["Tonsil size only", "Nasal polyp stage", "Parotid tumor cytology"], "It grades percentage airway obstruction."),
        q("Thermal inhalational injury may worsen after presentation because of progressive", "Laryngeal edema", ["Stapes fixation", "Sialolithiasis", "Tongue tie"], "Edema can evolve and threaten the airway."),
        q("A burn patient has facial burns, soot in mouth and hoarseness. What does this suggest", "Inhalational airway injury", ["Simple aphthous ulcer", "Benign vocal nodule", "Wharton duct stone"], "Soot and hoarseness after burns demand airway vigilance.", True),
        q("Definitive management of mature severe laryngotracheal stenosis may require", "Endoscopic dilation or open airway reconstruction", ["Only cough syrup", "Epley maneuver", "Tonsillectomy alone"], "Treatment depends on site, length, grade and cartilage framework.", True),
    ]),
    ("Tracheostomy, Intubation and Airway Procedures", [
        q("Tracheostomy is usually created between the", "Second and fourth tracheal rings", ["Cricoid and first ring always", "Hyoid and thyroid cartilage", "Carina and main bronchus"], "A standard tracheostomy avoids cricoid and low vascular structures."),
        q("Emergency cricothyrotomy enters through the", "Cricothyroid membrane", ["Thyrohyoid membrane", "Wharton duct", "Pyriform sinus"], "The cricothyroid membrane is a rapid emergency airway route."),
        q("A patient with upper airway obstruction cannot be intubated or ventilated. What is the emergency airway", "Cricothyrotomy", ["Tonsillectomy", "Sialendoscopy", "Myringotomy"], "Cannot-intubate-cannot-oxygenate requires front-of-neck access.", True),
        q("Early tracheostomy complications include bleeding, tube blockage and", "Surgical emphysema", ["Otosclerosis", "Mumps", "Leukoplakia"], "Air leak, bleeding, displacement and blockage are early risks."),
        q("Late tracheostomy complications include tracheal stenosis and", "Tracheoesophageal fistula", ["Geographic tongue", "Nasal dermoid", "BPPV"], "Pressure necrosis can injure trachea or posterior wall."),
        q("A tracheostomy patient suddenly becomes distressed with no airflow through the tube. What is the first concern", "Blocked or displaced tracheostomy tube", ["Vocal nodule", "Simple rhinitis", "Parotid tumor"], "Tube obstruction/displacement is a life-threatening emergency.", True),
        q("Humidification is important after tracheostomy because the tube bypasses", "Nasal warming and humidifying function", ["Cochlear function", "Salivary digestion", "Taste buds"], "Dry secretions can crust and block the tube."),
        q("A cuffed tracheostomy tube helps", "Reduce aspiration and allow positive-pressure ventilation", ["Improve smell", "Close the pharynx", "Treat tonsillitis"], "Cuffs seal the trachea for ventilation and reduce gross aspiration."),
        q("A ventilated patient develops air leak and gastric distension after prolonged tracheostomy cuff overinflation. What is suspected", "Tracheoesophageal fistula", ["Ranula", "Meniere disease", "Aphthous ulcer"], "Posterior tracheal wall pressure necrosis can create a fistula.", True),
        q("Accidental decannulation is most dangerous in a fresh tracheostomy because", "The tract may not be mature", ["The vocal cords disappear", "The parotid duct opens", "The tonsil bleeds"], "A fresh tract can close or form a false passage during reinsertion.", True),
    ]),
    ("Laryngeal Cancer and Premalignant Laryngeal Lesions", [
        q("The commonest malignancy of the larynx is", "Squamous cell carcinoma", ["Pleomorphic adenoma", "Lymphangioma", "Osteoma"], "Most laryngeal cancers are squamous carcinomas."),
        q("The most important risk factor for laryngeal carcinoma is", "Tobacco smoking", ["Cold water exposure", "Mumps", "Cerumen"], "Smoking is the major modifiable laryngeal cancer risk."),
        q("A smoker has painless hoarseness for six weeks. What is the next step", "Flexible laryngoscopy", ["Repeated antibiotics without examination", "Wax syringing", "Epley maneuver"], "Persistent hoarseness in a smoker needs laryngeal visualization.", True),
        q("Glottic carcinoma presents early because it causes", "Hoarseness", ["Posterior epistaxis", "Meal-time swelling", "Watery rhinorrhea"], "Small cord lesions alter voice early."),
        q("Supraglottic carcinoma tends to metastasize earlier because of", "Rich lymphatic drainage", ["Absent mucosa", "No blood supply", "Fixed stapes"], "Supraglottis has abundant lymphatics compared with true cords."),
        q("A patient has dysphagia, referred otalgia, neck node and supraglottic mass. What is likely", "Supraglottic carcinoma", ["Vocal nodule", "Croup", "Mumps"], "Supraglottic tumors often present with throat symptoms and nodal disease.", True),
        q("Laryngeal leukoplakia requires evaluation because it may represent", "Keratosis, dysplasia or carcinoma", ["Always harmless mucus", "Only viral croup", "Only salivary stone"], "White laryngeal plaques need risk assessment and often biopsy."),
        q("Staging of laryngeal cancer considers tumor extent, nodal disease and", "Distant metastasis", ["Audiogram only", "Nasal cycle", "Salivary flow"], "TNM staging guides treatment."),
        q("A small mobile true cord carcinoma without nodal disease may be treated with", "Radiotherapy or transoral laser surgery", ["Total laryngectomy in every case", "Only antihistamines", "Tracheostomy alone"], "Early glottic cancers can often be treated with organ preservation.", True),
        q("Advanced laryngeal cancer with cartilage invasion or nonfunctional larynx may require", "Total laryngectomy with adjuvant therapy as indicated", ["Voice rest only", "Sialendoscopy", "Nasal cautery"], "Advanced disease may need definitive surgery and multidisciplinary care.", True),
    ]),
    ("Pediatric Laryngeal and Tracheal Disorders", [
        q("The commonest congenital laryngeal anomaly causing stridor is", "Laryngomalacia", ["Laryngeal carcinoma", "Vocal nodule", "Reinke edema"], "Laryngomalacia is the most common cause of infant stridor."),
        q("Laryngomalacia stridor usually worsens when the infant is supine or", "Feeding and crying", ["Sleeping quietly only", "Underwater", "After wax removal"], "Dynamic supraglottic collapse increases with inspiratory effort."),
        q("An infant has inspiratory stridor worse during feeding but is thriving. What is the likely diagnosis", "Mild laryngomalacia", ["Epiglottic cancer", "Bilateral vocal nodules", "Tracheal stenosis"], "Typical mild laryngomalacia can be observed if feeding and growth are safe.", True),
        q("Severe laryngomalacia with failure to thrive may require", "Supraglottoplasty", ["Tonsillectomy only", "Sialolithotomy", "Nasal cautery"], "Surgery trims obstructing supraglottic tissue in severe cases."),
        q("Recurrent respiratory papillomatosis in children presents mainly with", "Progressive hoarseness and airway symptoms", ["Posterior epistaxis", "Meal-time parotid swelling", "Watery rhinorrhea"], "Papillomas affect voice and may obstruct the airway."),
        q("A child has progressive hoarseness and multiple wart-like lesions on the vocal cords. What is the likely cause", "HPV types 6 and 11", ["EBV", "Mumps", "Candida"], "Juvenile papillomatosis is linked to low-risk HPV.", True),
        q("Congenital subglottic stenosis is diagnosed when narrowing exists without prior", "Intubation trauma", ["Breastfeeding", "Vaccination", "Voice use"], "Congenital stenosis is present independent of acquired airway injury."),
        q("A child with recurrent barking cough and poor response to standard croup treatment should be assessed for", "Underlying airway lesion", ["Simple cerumen", "Parotid tumor", "Geographic tongue"], "Recurrent or atypical croup suggests structural airway disease."),
        q("A toddler has repeated croup-like episodes and persistent biphasic stridor between infections. What does this suggest", "Subglottic stenosis or fixed airway lesion", ["Allergic rhinitis only", "Mumps", "Aphthous ulcer"], "Persistent biphasic stridor is not typical of simple viral croup.", True),
        q("Tracheomalacia causes noisy breathing because of", "Dynamic collapse of weak tracheal walls", ["Stone in Wharton duct", "Vocal cord leukoplakia", "Tonsillar crypt debris"], "Weak cartilage allows expiratory or biphasic airway collapse.", True),
    ]),
    ("Tracheal Disease, Aspiration and Lower Airway Interface", [
        q("Tracheal stenosis commonly presents with exertional dyspnea, wheeze-like noise and", "Biphasic stridor", ["Posterior epistaxis", "Anosmia", "Meal-time swelling"], "Fixed central airway narrowing can mimic asthma but causes stridor."),
        q("A tracheal foreign body may produce", "Biphasic stridor or cough", ["Only tongue numbness", "Only parotid colic", "Only nasal itching"], "Central airway foreign bodies affect both phases and provoke cough."),
        q("A child has persistent cough and recurrent pneumonia after choking on a small toy. What is the likely problem", "Retained airway foreign body", ["Adenoid hypertrophy only", "Oral leukoplakia", "Mumps"], "Delayed foreign body diagnosis can present as recurrent infection.", True),
        q("Bronchoscopy for suspected airway foreign body is both diagnostic and", "Therapeutic", ["A hearing test", "A salivary flow test", "A nasal allergy test"], "Rigid bronchoscopy allows visualization and removal."),
        q("Tracheomalacia after prolonged intubation may result from", "Cartilage damage and airway wall weakness", ["Increased smell", "Tonsillar hypertrophy", "Adenoid involution"], "Pressure and inflammation can weaken tracheal support."),
        q("A patient has expiratory collapse of the trachea on dynamic bronchoscopy after prolonged ventilation. What is this", "Acquired tracheomalacia", ["Vocal nodule", "Epiglottitis", "Ranula"], "Dynamic collapse confirms tracheomalacia.", True),
        q("Aspiration risk rises when laryngeal sensation and vocal fold closure are impaired by", "Vagal or recurrent laryngeal nerve dysfunction", ["Nasal cycle", "Cerumen", "Sialolithiasis"], "Airway protection depends on sensation and glottic closure."),
        q("A patient coughs immediately after swallowing liquids following skull base surgery. This suggests", "Aspiration from impaired laryngeal protection", ["Otosclerosis", "Antrochoanal polyp", "Oral candidiasis"], "Neurogenic laryngeal dysfunction can impair swallowing safety.", True),
        q("Tracheitis after viral croup is suspected when the child becomes toxic with", "Thick purulent secretions and worsening airway obstruction", ["Itchy eyes", "Meal-time swelling", "Painless hoarseness only"], "Bacterial tracheitis causes toxic illness and obstructing secretions."),
        q("A child with croup-like illness has high fever, toxicity and poor response to nebulized adrenaline. What is the concern", "Bacterial tracheitis", ["Simple viral croup", "Vocal nodules", "Warthin tumor"], "Toxic appearance and poor response suggest bacterial tracheitis needing airway-ready care.", True),
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
                "id": f"ent-larynx-trachea-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ENT larynx/trachea question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ENT larynx and trachea questions.")


if __name__ == "__main__":
    main()
