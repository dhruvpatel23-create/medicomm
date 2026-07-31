import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ent"
SUBJECT_TITLE = "ENT"
CHAPTER = "Operative Surgery"
CHAPTER_ORDER = 9
SOURCE_PDF = "ent 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def punctuate(prompt):
    prompt = prompt.strip()
    if prompt[-1] in ".?!:":
        return prompt
    final_clause = re.split(r"[.:]", prompt)[-1].strip()
    question_starts = ("Which ", "What ", "Why ", "How ", "When ", "Where ")
    if prompt.startswith(question_starts) or final_clause.startswith(question_starts):
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
    ("Principles, Consent and Anaesthesia in ENT Surgery", [
        q("The most important preoperative airway assessment in obstructing laryngeal disease is", "Degree and site of airway compromise", ["Serum calcium alone", "Mastoid pneumatization", "Tonsil culture only"], "Airway risk decides urgency, anaesthesia plan and need for tracheostomy."),
        q("Local anaesthesia with adrenaline is avoided in uncontrolled severe hypertension because it can cause", "Dangerous cardiovascular stimulation", ["Immediate ototoxicity", "Septal cartilage growth", "Hypocalcaemia"], "Adrenaline may worsen tachycardia and hypertension."),
        q("A patient with stridor from a supraglottic mass is posted for biopsy. What should be planned first", "Secure airway strategy", ["Routine nasal packing", "Caloric test", "Parotid massage"], "Airway planning precedes diagnostic manipulation in obstructing upper airway lesions.", True),
        q("Informed consent for ENT surgery must include specific risk of", "Bleeding, airway compromise and nerve injury when relevant", ["Only cosmetic scar", "Only drug allergy", "Only discharge timing"], "ENT procedures may involve airway, cranial nerves and major vessels."),
        q("The safest position for most microscopic ear surgery is", "Supine with head turned", ["Prone", "Knee-elbow", "Standing"], "Supine head-turn positioning gives stable microscope access."),
        q("A diabetic patient scheduled for elective FESS has uncontrolled blood sugar and acute infection. What is the best decision", "Control infection and diabetes before elective surgery", ["Proceed without optimization", "Give no antibiotics ever", "Operate only under topical anaesthesia"], "Elective surgery should wait until modifiable infection and metabolic risks are optimized.", True),
        q("Throat pack during oral or nasal surgery is used mainly to prevent", "Blood aspiration and swallowed blood", ["Facial nerve palsy", "Stapes fixation", "Thyroid storm"], "A throat pack protects the airway and stomach from blood and debris."),
        q("The World Health Organization surgical checklist reduces", "Wrong site surgery and preventable perioperative errors", ["Otosclerosis incidence", "Viral load", "Eustachian tube length"], "Checklist use improves team communication and safety checks."),
        q("After adenotonsillectomy, a child becomes restless with repeated swallowing. What should be suspected", "Postoperative bleeding", ["Benign hunger", "External otitis", "Wax impaction"], "Restlessness and swallowing may be early signs of concealed throat bleeding.", True),
        q("The commonest reason to keep suction ready during ENT procedures is", "Shared airway contamination by blood or secretions", ["Need for audiogram", "Measuring nasal patency", "Testing taste"], "ENT surgery frequently shares the airway with anaesthesia.", True),
    ]),
    ("Otologic Surgery and Mastoid Procedures", [
        q("Myringotomy incision is classically made in the", "Anteroinferior quadrant", ["Posterosuperior quadrant", "Pars flaccida", "Attic"], "The anteroinferior quadrant avoids ossicles and chorda tympani."),
        q("The main indication for cortical mastoidectomy is", "Coalescent mastoiditis or mastoid disease needing drainage", ["Simple wax", "Allergic rhinitis", "Vocal nodule"], "Cortical mastoidectomy exenterates mastoid air cells while preserving canal wall."),
        q("A child with acute otitis media develops postaural swelling, fever and pinna pushed forward. What operation may be needed", "Cortical mastoidectomy", ["Stapedotomy", "Tonsillectomy", "Septoplasty"], "This is acute mastoiditis with subperiosteal abscess.", True),
        q("Canal wall down mastoidectomy creates", "An open mastoid cavity communicating with ear canal", ["Closed nasal cavity", "New parotid duct", "Laryngeal web"], "The posterior canal wall is removed to exteriorize disease."),
        q("The structure at risk near the second genu in mastoid surgery is", "Facial nerve", ["Optic nerve", "Hypoglossal nerve", "Recurrent laryngeal nerve"], "The facial nerve runs through the fallopian canal in the temporal bone."),
        q("During mastoidectomy, sudden twitching of facial muscles suggests", "Facial nerve irritation", ["Glossopharyngeal block", "Superior laryngeal palsy", "Maxillary sinus breach"], "Facial movement during drilling warns of nerve proximity.", True),
        q("Stapedotomy is performed for conductive hearing loss due to", "Otosclerosis", ["Meniere disease", "Presbycusis", "Vestibular neuritis"], "Fixation of stapes footplate is treated with stapes surgery in selected patients."),
        q("A postoperative stapedotomy patient has severe vertigo and sensorineural hearing loss. What complication is feared", "Perilymph leak or inner ear injury", ["Tonsillar remnant", "Septal haematoma", "Parotid fistula"], "Severe vestibulocochlear symptoms after stapes surgery need urgent assessment.", True),
        q("Tympanoplasty primarily aims to reconstruct", "Tympanic membrane and hearing mechanism", ["Nasal valve", "Vocal cord cover", "Thyroid capsule"], "Tympanoplasty repairs perforation and may reconstruct ossicles."),
        q("A patient with dry central tympanic membrane perforation is planned for repair using temporalis fascia. What operation is this", "Myringoplasty", ["Adenoidectomy", "Cricothyrotomy", "Sialendoscopy"], "Temporalis fascia is accessible and reliable for tympanic membrane repair.", True),
    ]),
    ("Nasal Septal, Turbinate and Epistaxis Surgery", [
        q("Septoplasty is preferred over submucous resection because it is", "More conservative", ["More destructive", "Only cosmetic", "Contraindicated in adults"], "Septoplasty preserves support while correcting deviation."),
        q("Killian incision is associated with", "Submucous resection of septum", ["Tonsillectomy", "Myringotomy", "Hemithyroidectomy"], "Classic SMR uses a Killian incision with bilateral flap elevation."),
        q("A patient develops septal swelling and pain after nasal trauma. What is the immediate treatment", "Incision and drainage of septal haematoma", ["Observation for 2 weeks", "Mastoid dressing", "Radiotherapy"], "Septal haematoma can cause cartilage necrosis and saddle nose.", True),
        q("Inferior turbinate reduction is used for", "Persistent nasal obstruction due to turbinate hypertrophy", ["Glottic cancer", "Otitis media", "Achalasia"], "Hypertrophied inferior turbinates may need reduction after medical therapy fails."),
        q("The artery most commonly ligated endoscopically for refractory posterior epistaxis is", "Sphenopalatine artery", ["Anterior cerebral artery", "Lingual artery", "Inferior thyroid artery"], "Sphenopalatine artery is the terminal maxillary artery branch supplying posterior nasal cavity."),
        q("An elderly hypertensive patient has persistent posterior epistaxis despite packing. What is the definitive endoscopic option", "Sphenopalatine artery ligation", ["Myringoplasty", "Adenoid curettage", "Parotidectomy"], "Endoscopic SPA ligation controls many refractory posterior bleeds.", True),
        q("A major complication of aggressive septal cartilage removal is", "Saddle nose deformity", ["Carhart notch", "Ranula", "Zenker diverticulum"], "Loss of dorsal and caudal support can collapse the nasal dorsum."),
        q("Septal perforation after surgery commonly presents with crusting and", "Whistling or epistaxis", ["Facial paralysis", "Hypocalcaemia", "Dysphonia only"], "Airflow turbulence causes whistling, crusts and bleeding."),
        q("After septoplasty, a patient has fever, hypotension and diffuse rash. What complication is suspected", "Toxic shock syndrome", ["Benign nasal cycle", "Otosclerosis", "Vocal polyp"], "Nasal packing rarely predisposes to toxic shock syndrome.", True),
        q("Anterior nasal packing should be accompanied by monitoring for", "Airway risk and hypoxia in vulnerable patients", ["Stapes fixation", "Achalasia", "Thyroid nodule malignancy"], "Packing can worsen breathing, especially in elderly or cardiopulmonary disease.", True),
    ]),
    ("Endoscopic Sinus and Skull Base Surgery", [
        q("Functional endoscopic sinus surgery primarily restores", "Sinus ventilation and mucociliary drainage", ["Ossicular continuity", "Vocal pitch", "Parotid saliva"], "FESS opens natural drainage pathways while preserving mucosa."),
        q("The uncinate process is an important landmark in", "Middle meatal antrostomy", ["Stapedotomy", "Tonsillectomy", "Tracheostomy"], "Uncinectomy exposes the natural maxillary ostium region."),
        q("A FESS patient develops clear watery nasal discharge that increases on bending forward. What is suspected", "CSF leak", ["Allergic sneezing", "Parotid fistula", "Otitis externa"], "Clear positional rhinorrhoea after sinus surgery suggests skull base breach.", True),
        q("The lamina papyracea separates ethmoid sinus from the", "Orbit", ["Middle ear", "Parotid gland", "Hypopharynx"], "It is a thin medial orbital wall at risk in ethmoid surgery."),
        q("The most feared vascular injury in sphenoid sinus surgery is injury to the", "Internal carotid artery", ["Facial artery", "Greater palatine artery", "Superior thyroid artery"], "The carotid artery may be closely related to the sphenoid sinus."),
        q("During ethmoidectomy, sudden orbital fat prolapse is seen. What should the surgeon do", "Stop further dissection in that area and protect orbit", ["Continue blindly", "Insert grommet", "Excise thyroid lobe"], "Orbital fat indicates lamina breach and risk to orbital contents.", True),
        q("Image-guided navigation is especially useful in FESS when", "Anatomy is distorted or disease is extensive", ["Wax is impacted", "Tonsils are enlarged", "Tongue tie is present"], "Navigation improves orientation in revision or skull-base-adjacent disease."),
        q("A patient with chronic epiphora from nasolacrimal duct obstruction undergoes endoscopic DCR. The sac is opened into the", "Nasal cavity", ["Middle ear", "Oesophagus", "Parotid duct"], "DCR bypasses distal nasolacrimal obstruction into the nose.", True),
        q("After endoscopic sinus surgery, sudden visual loss suggests", "Orbital or optic nerve complication", ["Expected crusting only", "Aphthous ulcer", "Meniere disease"], "Visual symptoms after FESS are an emergency.", True),
        q("The ostiomeatal complex is important because it drains the frontal, maxillary and", "Anterior ethmoid sinuses", ["Mastoid cells", "Piriform sinus", "Parotid gland"], "Anterior group sinuses drain around the middle meatus."),
    ]),
    ("Oral Cavity, Salivary and Pharyngeal Operations", [
        q("Tonsillectomy dissection is performed in the plane between tonsil capsule and", "Superior constrictor muscle", ["Buccinator", "Masseter", "Posterior cricoarytenoid"], "The peritonsillar space lies lateral to the tonsillar capsule."),
        q("The most important early complication after tonsillectomy is", "Haemorrhage", ["Otosclerosis", "Septal perforation", "Thyroid storm"], "Primary bleeding can threaten airway and circulation."),
        q("A child vomits fresh blood 4 hours after tonsillectomy. What is the next priority", "Airway assessment and control of bleeding", ["Routine discharge", "Ear syringing", "Barium swallow"], "Post-tonsillectomy bleeding needs urgent airway-conscious management.", True),
        q("Adenoidectomy is performed through the", "Nasopharynx", ["Middle ear", "Laryngeal ventricle", "Thyroid bed"], "Adenoids occupy the roof and posterior wall of nasopharynx."),
        q("Tongue tie release is called", "Frenotomy or frenuloplasty", ["Stapedectomy", "Caldwell-Luc operation", "Hemiglossectomy"], "Ankyloglossia is treated by dividing or reconstructing the lingual frenulum."),
        q("After submandibular gland excision, weakness of lower lip depression suggests injury to", "Marginal mandibular nerve", ["Optic nerve", "Chorda tympani in middle ear", "External branch of superior laryngeal nerve"], "The marginal mandibular branch runs close to the submandibular region.", True),
        q("Superficial parotidectomy requires identification of the", "Facial nerve", ["Sciatic nerve", "Recurrent laryngeal nerve", "Phrenic nerve"], "Facial nerve preservation is central to parotid surgery."),
        q("A patient develops salivary leakage from wound after parotidectomy. What complication is this", "Salivary fistula", ["CSF rhinorrhoea", "Chyle leak", "Tracheal stenosis"], "Parotid duct or gland remnant leak can form a salivary fistula.", True),
        q("Marsupialization is a treatment option for", "Ranula", ["Glomus jugulare", "Choanal atresia", "Otosclerosis"], "Ranula is a mucous extravasation cyst from floor of mouth."),
        q("Uvulopalatopharyngoplasty is used in selected patients with", "Obstructive sleep apnoea", ["Acute mastoiditis", "Mucormycosis", "Vocal cord palsy"], "UPPP enlarges the retropalatal airway in selected OSA cases.", True),
    ]),
    ("Laryngeal Microlaryngoscopy and Laser Surgery", [
        q("Direct laryngoscopy gives best exposure of the", "Larynx and hypopharynx", ["Middle ear", "Ethmoid roof", "Thyroid isthmus"], "Rigid laryngoscopy allows inspection, biopsy and operative work."),
        q("Suspension microlaryngoscopy is commonly used for", "Vocal fold lesions", ["Septal haematoma", "Mastoid abscess", "Submandibular stones"], "Microlaryngoscopy enables precise surgery on vocal folds."),
        q("A teacher has a small unilateral vocal fold polyp with persistent hoarseness despite voice therapy. What procedure is considered", "Microlaryngeal excision", ["Cortical mastoidectomy", "Septoplasty", "Sistrunk operation"], "Persistent benign vocal fold lesions may need phonomicrosurgery.", True),
        q("The key principle in phonosurgery is preservation of", "Vocal fold mucosa and layered microstructure", ["Inferior turbinate bone only", "Tonsillar capsule only", "Mastoid cortex only"], "Over-resection scars the vibratory cover and worsens voice."),
        q("CO2 laser in laryngeal surgery requires special care to prevent", "Airway fire", ["Hypocalcaemia", "CSF leak", "Perilymph fistula"], "Laser, oxygen and airway tube create fire risk."),
        q("During laser excision of a laryngeal lesion, smoke and sudden flame are seen. What is the immediate action", "Stop laser, disconnect gases and flood airway with saline", ["Increase oxygen flow", "Continue excision", "Pack nose"], "Airway fire management starts by stopping fuel and oxidizer, then extinguishing.", True),
        q("Early glottic carcinoma may be treated surgically by", "Transoral laser microsurgery in selected cases", ["Myringotomy", "Adenoidectomy", "Caldwell-Luc operation"], "Selected early glottic cancers can be excised endoscopically."),
        q("A suspicious ulceroproliferative laryngeal lesion is biopsied. Tissue should be taken from the", "Representative tumor edge", ["Normal contralateral tonsil", "Nasal vestibule", "Ear canal"], "Representative tissue is required for diagnosis without excessive necrotic sampling.", True),
        q("After laryngeal biopsy, a patient develops increasing stridor. What is the concern", "Laryngeal oedema or bleeding", ["Expected voice rest only", "Parotid swelling", "Wax migration"], "Airway compromise after laryngeal procedure is urgent.", True),
        q("Voice rest after vocal fold surgery reduces", "Mechanical trauma to healing mucosa", ["Nasal bleeding", "Middle ear effusion", "Thyroid hormone release"], "Controlled voice use protects the surgical site."),
    ]),
    ("Tracheostomy and Airway Procedures", [
        q("Elective tracheostomy is usually performed between the", "Second to fourth tracheal rings", ["Cricoid and first ring through cricoid", "Hyoid and epiglottis", "Thyroid laminae"], "A standard tracheal window avoids high cricoid injury and low vascular risk."),
        q("Bjork flap in tracheostomy is an", "Inferiorly based tracheal flap", ["Nasal mucosal flap", "Tympanic membrane graft", "Parotid duct flap"], "The flap can help create a stable tracheal opening."),
        q("A tracheostomy patient suddenly becomes cyanosed and ventilation is difficult. What is the first concern", "Tube blockage or displacement", ["Tonsillar regrowth", "Otosclerosis", "Nasal polyp"], "Acute deterioration after tracheostomy is obstruction or displacement until proven otherwise.", True),
        q("Emergency cricothyrotomy is performed through the", "Cricothyroid membrane", ["Thyrohyoid membrane", "First tracheal ring routinely", "Vallecula"], "The cricothyroid membrane provides rapid emergency airway access."),
        q("The most dangerous early complication of low tracheostomy is injury to", "Innominate artery", ["Chorda tympani", "Optic nerve", "Lingual nerve"], "Low dissection risks major vessels in the thoracic inlet."),
        q("A tracheostomy tube has been in place for weeks and the patient bleeds briskly from the stoma. What is feared", "Tracheo-innominate fistula", ["Benign granulation only", "Ranula", "Septal haematoma"], "Sentinel or major bleed from stoma may indicate a fatal vascular fistula.", True),
        q("Humidification after tracheostomy is required because bypassing the nose causes", "Dry thick secretions", ["Improved mucociliary clearance automatically", "Immediate vocal cord paralysis", "Hypothyroidism"], "Inspired air is no longer warmed and humidified by nasal passages."),
        q("A tracheostomy patient is considered for decannulation. Besides airway patency and cough, what is required", "Ability to manage secretions", ["Persistent obstruction", "Uncontrolled aspiration", "Need for high oxygen always"], "Safe decannulation requires airway patency and secretion control.", True),
        q("A child pulls out a fresh tracheostomy tube 12 hours after surgery. What is the safest response", "Call expert help and maintain oxygenation without blind reinsertion", ["Blindly force the tube in", "Ignore if crying", "Give oral water"], "Fresh tracts are immature and blind reinsertion can create a false passage.", True),
        q("Subcutaneous emphysema after tracheostomy usually suggests", "Air leak around tracheal opening", ["Stapes fixation", "Parotid abscess", "Thyroid carcinoma"], "Air tracking into soft tissues follows leak or tight closure."),
    ]),
    ("Neck Dissection and Head-Neck Oncosurgery", [
        q("Radical neck dissection classically removes lymph nodes with SCM, IJV and", "Spinal accessory nerve", ["Facial artery only", "Thyroid cartilage", "Parotid duct"], "Classical radical dissection sacrifices these three non-lymphatic structures."),
        q("Modified radical neck dissection preserves one or more of", "Spinal accessory nerve, internal jugular vein or sternocleidomastoid", ["All cervical lymph nodes only", "Mandible always", "Larynx always"], "MRND removes nodal levels while preserving selected non-lymphatic structures."),
        q("After neck dissection, a patient cannot abduct the shoulder above horizontal. Which nerve is injured", "Spinal accessory nerve", ["Hypoglossal nerve", "Vagus nerve", "Marginal mandibular nerve"], "Accessory nerve injury weakens trapezius and shoulder elevation.", True),
        q("Selective neck dissection removes", "Only nodal levels at risk", ["All neck contents from skull base to clavicle", "Only thyroid lobe", "Only submandibular duct"], "It is tailored to lymphatic risk pattern."),
        q("Chyle leak after left lower neck dissection results from injury to the", "Thoracic duct", ["Parotid duct", "Nasolacrimal duct", "Eustachian tube"], "The thoracic duct enters venous system in the left lower neck."),
        q("A milky drain output increases after feeding following left neck dissection. What is the diagnosis", "Chyle leak", ["Salivary calculus", "CSF otorrhoea", "Tracheomalacia"], "Milky postoperative drainage suggests lymphatic chyle leak.", True),
        q("Mandibulotomy in oral cancer surgery is used to improve", "Surgical access", ["Hearing threshold", "Nasal airflow", "Thyroid hormone level"], "Splitting the mandible may expose posterior oral cavity and oropharynx tumors."),
        q("Free flap reconstruction depends most critically on", "Microvascular anastomosis patency", ["Tonsil size", "Audiogram notch", "Nasal cycle"], "Flap survival requires arterial inflow and venous drainage."),
        q("A free flap becomes dusky and swollen within hours of surgery. What is the likely problem", "Venous congestion", ["Normal healing", "Otosclerosis", "Allergic rhinitis"], "Early dusky swelling strongly suggests venous outflow obstruction.", True),
        q("Frozen section during cancer surgery is used mainly to assess", "Margin status", ["Serum calcium", "Hearing level", "Nasal allergy"], "Intraoperative pathology helps decide adequacy of excision margins.", True),
    ]),
    ("Thyroid and Parathyroid Surgery", [
        q("The recurrent laryngeal nerve is at risk during", "Thyroidectomy", ["Myringoplasty", "Septoplasty", "Adenoidectomy"], "The nerve runs near the tracheoesophageal groove and Berry ligament."),
        q("External branch of superior laryngeal nerve injury causes difficulty with", "High-pitched voice", ["Nasal breathing", "Bone conduction", "Salivation"], "It supplies cricothyroid, important for pitch control."),
        q("After thyroidectomy, a singer cannot reach high notes but vocal cords move normally. Which nerve is likely injured", "External branch of superior laryngeal nerve", ["Facial nerve", "Glossopharyngeal nerve", "Chorda tympani"], "Cricothyroid weakness affects pitch without obvious cord immobility.", True),
        q("Post-thyroidectomy tingling and carpopedal spasm suggest", "Hypocalcaemia", ["Hypernatraemia", "Otosclerosis", "Achalasia"], "Parathyroid injury or devascularization can cause hypocalcaemia."),
        q("A tense neck swelling with respiratory distress soon after thyroidectomy requires", "Immediate wound opening and airway management", ["Routine oral calcium only", "Delayed ultrasound", "Ear suction"], "Neck haematoma can rapidly obstruct the airway.", True),
        q("The middle thyroid vein is encountered during thyroidectomy and drains into the", "Internal jugular vein", ["External jugular vein", "Facial vein", "Subclavian artery"], "It is divided carefully during lateral mobilization of the lobe."),
        q("Subtotal thyroidectomy leaves thyroid tissue to reduce risk of", "Hypoparathyroidism and recurrent laryngeal nerve injury", ["Otitis media", "Epistaxis", "Parotid fistula"], "Older operations left remnants to reduce complications, though recurrence risk remains."),
        q("In Graves disease, preoperative preparation includes achieving", "Euthyroid state", ["Deliberate thyrotoxicosis", "Permanent hypocalcaemia", "Nasal decongestion only"], "Euthyroid preparation reduces thyroid storm risk."),
        q("A Graves patient develops fever, tachycardia and delirium after surgery. What complication is suspected", "Thyroid storm", ["Meniere disease", "Septal perforation", "Ranula"], "Thyroid storm is acute severe thyrotoxicosis precipitated by stress or surgery.", True),
        q("During thyroidectomy, a parathyroid gland appears devascularized. What should be considered", "Parathyroid autotransplantation", ["Discarding all glands", "Myringoplasty", "Nasal packing"], "Devascularized parathyroid tissue may be implanted into muscle.", True),
    ]),
    ("Oesophagoscopy, Bronchoscopy and Foreign Body Surgery", [
        q("Rigid oesophagoscopy is useful for removal of", "Impacted oesophageal foreign body", ["Inferior turbinate", "Stapes footplate", "Thyroid nodule"], "Rigid endoscopy allows controlled extraction under vision."),
        q("Coins in the oesophagus on AP radiograph usually appear", "En face", ["Edge-on always", "Invisible always", "Inside trachea only"], "Oesophageal coins often show the flat face on AP view."),
        q("A child has drooling and dysphagia after swallowing a button battery. What is the management", "Emergency endoscopic removal", ["Observe for passage", "Give emetics", "Delay for barium swallow"], "Button batteries can cause rapid caustic injury and perforation.", True),
        q("Rigid bronchoscopy is the procedure of choice for", "Airway foreign body removal", ["Septal deviation", "Vocal cord polyp always", "Parotid tumor"], "Rigid bronchoscopy secures ventilation and permits extraction."),
        q("A toddler has sudden cough, unilateral wheeze and air trapping. What should be suspected", "Bronchial foreign body", ["Otosclerosis", "Thyroiditis", "Aphthous ulcer"], "Acute choking followed by unilateral signs suggests airway foreign body.", True),
        q("Peanut aspiration is dangerous because it can cause", "Chemical bronchitis and obstruction", ["Hypocalcaemia", "Septal perforation", "Parotid fistula"], "Vegetable foreign bodies swell and inflame airway mucosa."),
        q("The most common site of oesophageal foreign body impaction is", "Cricopharyngeal narrowing", ["Middle meatus", "Oval window", "Piriform aperture only"], "The upper oesophageal sphincter is the narrowest physiological region."),
        q("After oesophagoscopy, fever, chest pain and surgical emphysema suggest", "Oesophageal perforation", ["Expected recovery", "Myringitis", "Allergic rhinitis"], "Perforation causes mediastinal contamination and emphysema.", True),
        q("Ventilating bronchoscope is designed to allow", "Airway ventilation during endoscopy", ["Thyroid hormone measurement", "Audiometry", "Nasal packing"], "Rigid bronchoscopy shares the airway and must maintain oxygenation."),
        q("Sharp foreign bodies in the hypopharynx require careful removal because of risk of", "Mucosal perforation and deep neck infection", ["Otosclerosis", "Benign nasal cycle", "Ranula only"], "Sharp objects can penetrate pharyngeal wall and seed deep spaces.", True),
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
                "id": f"ent-operative-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ENT operative surgery question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ENT operative surgery questions.")


if __name__ == "__main__":
    main()
