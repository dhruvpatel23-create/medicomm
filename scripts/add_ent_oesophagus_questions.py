import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ent"
SUBJECT_TITLE = "ENT"
CHAPTER = "Diseases of Oesophagus"
CHAPTER_ORDER = 7
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


TOPIC_NAMES = [
    "Oesophageal Anatomy, Physiology and Evaluation",
    "Dysphagia, Odynophagia and Globus",
    "Foreign Bodies and Food Bolus Impaction",
    "Caustic Injury and Oesophageal Strictures",
    "Gastro-Oesophageal Reflux and Barrett Oesophagus",
    "Motility Disorders and Diverticula",
    "Oesophageal Perforation and Fistulae",
    "Benign Oesophageal Lesions, Webs and Rings",
    "Oesophageal Carcinoma and Premalignant Disease",
    "Paediatric Oesophageal Disorders",
]


ROWS = {
    "Oesophageal Anatomy, Physiology and Evaluation": [
        q("The upper oesophageal sphincter is formed mainly by the", "Cricopharyngeus", ["Posterior cricoarytenoid", "Palatoglossus", "Inferior turbinate"], "Cricopharyngeus forms the major functional component of the upper oesophageal sphincter."),
        q("The oesophagus begins at the lower border of", "Cricoid cartilage", ["Hyoid bone", "Thyroid notch", "Soft palate"], "The cervical oesophagus begins around C6 at the cricoid level."),
        q("A patient has dysphagia with pooling of saliva in pyriform fossae on endoscopy. What does this suggest", "Pharyngoesophageal obstruction", ["Nasal allergy", "Otosclerosis", "Mumps"], "Pooling indicates impaired bolus passage at the hypopharynx or upper oesophagus.", True),
        q("The oesophagus lacks", "Serosa", ["Mucosa", "Submucosa", "Muscular layer"], "Absence of serosa contributes to easy spread of infection or tumor."),
        q("Barium swallow is especially useful for evaluating", "Structural narrowing and diverticula", ["Sensorineural deafness", "Parotid cytology", "Nasal cycle"], "Contrast swallow outlines strictures, rings, webs and diverticula."),
        q("A patient with progressive dysphagia has a shouldered narrowing on barium swallow. What is the concern", "Oesophageal malignancy", ["Simple globus", "Viral croup", "Benign nasal polyp"], "Irregular shouldered narrowing is suspicious for cancer.", True),
        q("Flexible upper GI endoscopy is useful because it permits visualization and", "Biopsy", ["Audiometry", "Epley maneuver", "Tonsil grading only"], "Endoscopy can diagnose mucosal disease and obtain tissue."),
        q("Manometry is the key test for", "Oesophageal motility disorders", ["Tonsillitis", "Epistaxis", "Otitis externa"], "Pressure measurements diagnose achalasia and spasm patterns."),
        q("A patient has normal endoscopy but suspected achalasia. What investigation best confirms motility abnormality", "Oesophageal manometry", ["Pure tone audiometry", "Sialography", "Nasal endoscopy only"], "Manometry defines LES relaxation and peristalsis abnormalities.", True),
        q("The lower oesophageal sphincter prevents", "Gastro-oesophageal reflux", ["Middle ear infection", "Parotid stone", "Nasal polyps"], "LES tone limits reflux of gastric contents into the oesophagus.", True),
    ],
    "Dysphagia, Odynophagia and Globus": [
        q("Dysphagia means", "Difficulty swallowing", ["Painful hearing", "Loss of smell", "Nasal bleeding"], "Dysphagia is impaired passage of solids or liquids during swallowing."),
        q("Odynophagia means", "Painful swallowing", ["Painless regurgitation", "Voice fatigue", "Dry mouth"], "Pain with swallowing suggests mucosal inflammation, ulceration or injury."),
        q("Progressive dysphagia first to solids and later to liquids suggests", "Mechanical obstruction", ["Pure functional globus", "Acute rhinitis", "BPPV"], "A narrowing lumen blocks solids first, then liquids as obstruction worsens."),
        q("A smoker develops progressive solid-food dysphagia, weight loss and hoarseness. What is the most likely diagnosis", "Oesophageal carcinoma", ["Globus pharyngeus", "Aphthous ulcer", "Mumps"], "Progressive dysphagia with weight loss is cancer until excluded.", True),
        q("Dysphagia to both solids and liquids from onset suggests", "Motility disorder", ["Early mechanical ring only", "Wax impaction", "Adenoid hypertrophy"], "Motility disorders impair transport of both solids and liquids early."),
        q("A patient has intermittent dysphagia to solids and liquids with regurgitation of undigested food. What does this suggest", "Achalasia", ["Simple viral pharyngitis", "Oral candidiasis", "Allergic rhinitis"], "Achalasia causes impaired LES relaxation and aperistalsis.", True),
        q("Globus pharyngeus is classically a sensation of lump in throat that improves with", "Eating", ["Lying flat after meals", "Whispering", "Neck trauma"], "Globus is often noticed between meals and may improve during swallowing."),
        q("Alarm features in dysphagia include weight loss, bleeding, aspiration and", "Progressive worsening", ["Brief mild globus only", "Normal appetite", "Itchy eyes"], "Progressive symptoms need urgent evaluation."),
        q("A patient has lump sensation in throat but swallows meals normally and has normal endoscopy. What is likely", "Globus pharyngeus", ["Oesophageal cancer", "Foreign body impaction", "Retropharyngeal abscess"], "Normal swallowing and examination support globus after red flags are excluded.", True),
        q("Oropharyngeal dysphagia is suggested by coughing, choking and", "Nasal regurgitation", ["Meal-time parotid swelling", "Pulsatile tinnitus", "Posterior epistaxis"], "Transfer-phase dysfunction causes aspiration and nasal regurgitation.", True),
    ],
    "Foreign Bodies and Food Bolus Impaction": [
        q("The commonest site for oesophageal foreign body impaction is near the", "Cricopharyngeus", ["Ileocecal valve", "Pylorus", "External auditory canal"], "The upper oesophageal sphincter is a natural narrowing."),
        q("Button battery in the oesophagus requires", "Emergency removal", ["Observation for 48 hours", "Oral antibiotics only", "Barium swallow first in every case"], "Battery injury can cause rapid liquefaction necrosis and perforation."),
        q("A toddler has drooling after suspected coin ingestion; X-ray shows a round object at thoracic inlet. What is the next step", "Endoscopic removal", ["Wait for spontaneous passage", "Nasal cautery", "Tonsillectomy"], "Symptomatic oesophageal coin at upper narrowing requires removal.", True),
        q("A coin in the oesophagus on AP X-ray usually appears", "En face as a round disc", ["Sagittal like a thin line", "Always invisible", "As air only"], "Oesophageal coins usually lie in coronal plane."),
        q("Food bolus impaction in adults is often associated with underlying", "Oesophageal stricture or eosinophilic oesophagitis", ["Adenoid hypertrophy", "Otosclerosis", "Mumps"], "Food impaction should prompt evaluation for structural or inflammatory disease."),
        q("A man cannot swallow saliva after meat impaction at dinner. What is the management", "Urgent endoscopic clearance", ["Force more food down", "Observe for weeks", "Voice therapy"], "Complete obstruction with saliva intolerance needs urgent endoscopy.", True),
        q("Sharp foreign bodies are dangerous because they may cause", "Perforation", ["Benign nasal cycle", "Stapes fixation", "Ranula"], "Sharp objects can pierce the oesophageal wall."),
        q("Plain radiographs may miss foreign bodies made of", "Fish bone or plastic", ["Metal coin", "Button battery", "Dental plate with wire"], "Radiolucent objects may require CT or endoscopic assessment when suspected."),
        q("A patient has persistent throat pain after fish bone ingestion despite normal oral exam. What is the next step", "Flexible endoscopy or imaging based on suspicion", ["Blind finger sweep", "Ignore all symptoms", "Epley maneuver"], "Hidden bones may lodge in hypopharynx or oesophagus.", True),
        q("Multiple magnets swallowed by a child are dangerous because they can", "Trap bowel walls and perforate", ["Cause otosclerosis", "Dissolve harmlessly", "Prevent dysphagia"], "Magnets can attract across bowel loops and cause pressure necrosis.", True),
    ],
    "Caustic Injury and Oesophageal Strictures": [
        q("Alkali ingestion causes", "Liquefactive necrosis", ["Coagulative necrosis only", "No deep injury", "Stapes fixation"], "Alkali penetrates deeply and causes liquefactive tissue injury."),
        q("Acid ingestion classically causes", "Coagulative necrosis", ["Liquefactive necrosis only", "No gastric injury", "Benign nasal edema"], "Acids tend to coagulate proteins, though severe injury can still occur."),
        q("A child drinks drain cleaner and presents with drooling and stridor. What is the next step", "Airway assessment and stabilization", ["Induce vomiting", "Neutralize with acid", "Blind NG tube"], "Airway compromise comes first in caustic ingestion.", True),
        q("Vomiting after caustic ingestion is avoided because it", "Re-exposes mucosa and risks aspiration", ["Always neutralizes caustic", "Prevents strictures", "Improves visualization"], "Emesis can worsen injury and aspiration."),
        q("Endoscopy after caustic ingestion is used to grade", "Mucosal injury", ["Hearing loss", "Tonsil size", "Nasal polyp stage"], "Endoscopy helps determine severity when performed safely."),
        q("A patient develops progressive dysphagia weeks after caustic ingestion. What is likely", "Oesophageal stricture", ["Acute viral laryngitis", "Mumps", "Globus only"], "Fibrotic healing after burns can narrow the lumen.", True),
        q("Late complication of caustic oesophageal injury includes increased risk of", "Squamous cell carcinoma", ["Meniere disease", "Warthin tumor", "Otosclerosis"], "Long-term scarred oesophagus has malignant risk."),
        q("Benign oesophageal strictures are commonly treated by", "Endoscopic dilatation", ["Tonsillectomy", "Parotidectomy", "Nasal cautery"], "Dilatation relieves luminal narrowing when appropriate."),
        q("During dilatation of a tight stricture, sudden severe chest pain and surgical emphysema suggest", "Oesophageal perforation", ["Simple reflux", "Vocal nodule", "Aphthous ulcer"], "Pain and emphysema after instrumentation indicate perforation until proven otherwise.", True),
        q("Corrosive stricture prevention and care require nutrition support, surveillance and", "Planned staged dilatation when safe", ["Repeated forced vomiting", "No follow-up", "Antihistamines only"], "Management is careful and staged to reduce perforation and malnutrition.", True),
    ],
    "Gastro-Oesophageal Reflux and Barrett Oesophagus": [
        q("Gastro-oesophageal reflux disease is caused by reflux of gastric contents due to", "Failure of anti-reflux barrier", ["Excess ear wax", "Tonsillar crypts", "Parotid stone"], "LES dysfunction, hiatus hernia and impaired clearance contribute to GERD."),
        q("Typical GERD symptoms are heartburn and", "Regurgitation", ["Epistaxis", "Vertigo", "Hearing loss"], "Heartburn and acid regurgitation are classic symptoms."),
        q("A patient has heartburn after meals, sour regurgitation and nocturnal cough. What is the most likely diagnosis", "Gastro-oesophageal reflux disease", ["Achalasia", "Oesophageal cancer", "Mumps"], "Meal-related heartburn and regurgitation support GERD.", True),
        q("Barrett oesophagus means replacement of squamous mucosa by", "Intestinal-type columnar metaplasia", ["Keratinized skin", "Thyroid follicular cells", "Respiratory cartilage"], "Chronic reflux can cause intestinal metaplasia in distal oesophagus."),
        q("Barrett oesophagus increases risk of", "Adenocarcinoma", ["Medullary thyroid carcinoma", "Otosclerosis", "Aphthous ulcer"], "Barrett metaplasia is a precursor for oesophageal adenocarcinoma."),
        q("A chronic reflux patient has endoscopic salmon-colored mucosa above the gastro-oesophageal junction. What does biopsy look for", "Intestinal metaplasia", ["Sulfur granules", "Amyloid only", "Curschmann spirals"], "Goblet-cell intestinal metaplasia confirms Barrett oesophagus.", True),
        q("First-line medical therapy for frequent GERD symptoms is", "Proton pump inhibitor", ["Aminoglycoside", "Radioiodine", "Epley maneuver"], "PPIs suppress acid and heal erosive oesophagitis."),
        q("Alarm symptoms in reflux include dysphagia, weight loss and", "Gastrointestinal bleeding", ["Sneezing", "Watery eyes", "Ear itching"], "Alarm features require endoscopic evaluation."),
        q("A reflux patient develops progressive dysphagia and weight loss. What is the next step", "Upper GI endoscopy", ["Increase lozenges only", "Ignore as simple reflux", "Audiometry"], "Dysphagia and weight loss are alarm features.", True),
        q("Laryngopharyngeal reflux can cause throat clearing, globus and", "Hoarseness", ["Pinna swelling", "Posterior epistaxis", "Meal-time parotid pain"], "Refluxate can irritate the larynx and pharynx.", True),
    ],
    "Motility Disorders and Diverticula": [
        q("Achalasia is characterized by failed lower oesophageal sphincter relaxation and", "Aperistalsis", ["Excess peristalsis only", "Normal manometry", "Subglottic stenosis"], "Loss of inhibitory myenteric neurons causes aperistalsis and LES nonrelaxation."),
        q("Barium swallow in achalasia classically shows", "Bird-beak narrowing", ["Corkscrew only", "Thumb sign", "Steeple sign"], "Tapered distal narrowing gives the bird-beak appearance."),
        q("A patient has dysphagia to solids and liquids, regurgitation and bird-beak narrowing. What is the diagnosis", "Achalasia", ["GERD only", "Zenker diverticulum", "Plummer-Vinson syndrome"], "Both solids and liquids with bird-beak tapering is classic.", True),
        q("Definitive treatment options for achalasia include pneumatic dilatation, Heller myotomy or", "POEM", ["Tonsillectomy", "Radioiodine", "Adenoidectomy"], "Peroral endoscopic myotomy is a modern option for achalasia."),
        q("Diffuse oesophageal spasm may show barium swallow appearance called", "Corkscrew oesophagus", ["Bird beak only", "Rat-tail stenosis", "Shouldered apple core"], "Uncoordinated contractions can produce corkscrew pattern."),
        q("A patient has intermittent chest pain and dysphagia with corkscrew oesophagus. What is likely", "Diffuse oesophageal spasm", ["Caustic stricture", "Foreign body", "Mumps"], "Intermittent dysphagia and corkscrew barium pattern fit spasm.", True),
        q("Zenker diverticulum arises through", "Killian dehiscence", ["Foramen cecum", "Little area", "Wharton duct"], "It is a posterior hypopharyngeal pulsion diverticulum."),
        q("Zenker diverticulum commonly causes", "Regurgitation of undigested food and halitosis", ["Posterior epistaxis", "Meal-time parotid swelling", "Vertigo"], "Food retention leads to delayed regurgitation and bad breath."),
        q("An elderly man regurgitates undigested food hours after eating and has aspiration episodes. What is likely", "Zenker diverticulum", ["Achalasia only", "GERD only", "Aphthous ulcer"], "Delayed regurgitation with aspiration is classic Zenker presentation.", True),
        q("Traction diverticula are usually associated with", "Mediastinal inflammation pulling the oesophageal wall", ["Cricopharyngeal failure", "Barrett metaplasia", "Vocal cord nodules"], "Traction diverticula are true diverticula caused by external scarring traction.", True),
    ],
    "Oesophageal Perforation and Fistulae": [
        q("Boerhaave syndrome is", "Spontaneous transmural oesophageal rupture after vomiting", ["Benign globus", "Congenital web", "Vocal cord polyp"], "Forceful vomiting can rupture the oesophageal wall."),
        q("Mackler triad includes vomiting, chest pain and", "Subcutaneous emphysema", ["Sneezing", "Parotid swelling", "Tinnitus"], "The classic triad suggests spontaneous oesophageal rupture."),
        q("After heavy vomiting, a patient develops severe chest pain, fever and neck crepitus. What is likely", "Boerhaave syndrome", ["GERD only", "Vocal nodule", "Mumps"], "Post-emetic chest pain with emphysema suggests rupture.", True),
        q("Oesophageal perforation can rapidly cause", "Mediastinitis", ["Otosclerosis", "Atrophic rhinitis", "Ranula"], "Contamination of mediastinum causes severe infection."),
        q("Initial management of suspected oesophageal perforation includes nil per oral, broad antibiotics and", "Urgent surgical or endoscopic evaluation", ["Oral feeding", "Blind dilatation", "Reassurance"], "Perforation needs urgent source control and supportive care."),
        q("A patient develops fever, tachycardia and mediastinal air after endoscopy. What is the next step", "Treat as oesophageal perforation urgently", ["Discharge with lozenges", "Do Epley maneuver", "Start nasal steroid"], "Mediastinal air after instrumentation is perforation until proven otherwise.", True),
        q("Tracheoesophageal fistula in adults may present with", "Coughing after swallowing", ["Only anosmia", "Meal-time submandibular swelling", "Pulsatile tinnitus"], "Swallowed liquids entering airway cause cough and aspiration."),
        q("Malignant tracheoesophageal fistula is commonly due to advanced", "Oesophageal carcinoma", ["Aphthous ulcer", "Mumps", "Benign mucocele"], "Tumor invasion can connect oesophagus and airway."),
        q("A patient with oesophageal cancer coughs immediately on drinking and has recurrent pneumonia. What does this suggest", "Tracheoesophageal fistula", ["Simple reflux only", "Zenker without aspiration", "Tonsillitis"], "Oesophago-airway communication causes aspiration with swallowing.", True),
        q("Water-soluble contrast is preferred initially in suspected perforation because barium leakage can worsen", "Mediastinal inflammation", ["Hearing loss", "Nasal obstruction", "Salivary stones"], "Water-soluble contrast is safer if extravasation occurs.", True),
    ],
    "Benign Oesophageal Lesions, Webs and Rings": [
        q("Plummer-Vinson syndrome includes iron deficiency anemia, dysphagia and", "Upper oesophageal web", ["Lower oesophageal cancer only", "Mumps", "Vocal nodule"], "Postcricoid/upper oesophageal web causes dysphagia."),
        q("Plummer-Vinson syndrome increases risk of", "Squamous cell carcinoma", ["Medullary thyroid cancer", "Otosclerosis", "Meniere disease"], "It is a premalignant condition for upper aerodigestive SCC."),
        q("A woman has iron deficiency anemia, dysphagia and a postcricoid web. What is the diagnosis", "Plummer-Vinson syndrome", ["Achalasia", "GERD", "Boerhaave syndrome"], "The triad defines Plummer-Vinson syndrome.", True),
        q("Schatzki ring is typically located at the", "Gastro-oesophageal junction", ["Cricopharyngeus only", "Pyriform fossa", "Nasopharynx"], "A lower mucosal ring near the GE junction causes intermittent solid dysphagia."),
        q("Intermittent solid-food dysphagia with meat impaction suggests", "Schatzki ring", ["Diffuse spasm only", "Mumps", "Adenoid hypertrophy"], "A ring intermittently traps solid boluses."),
        q("A patient has episodic steakhouse dysphagia with a thin lower oesophageal ring. What is likely", "Schatzki ring", ["Zenker diverticulum", "Caustic stricture", "Oesophageal cancer"], "Lower oesophageal ring causes intermittent solid food impaction.", True),
        q("Eosinophilic oesophagitis is associated with atopy and", "Food bolus impaction", ["Posterior epistaxis", "Parotid colic", "Pinna swelling"], "EoE commonly presents with dysphagia and food impaction in young men."),
        q("Endoscopic rings and furrows suggest", "Eosinophilic oesophagitis", ["Mumps", "Achalasia only", "Simple reflux only"], "Trachealization, rings, furrows and exudates are common EoE findings."),
        q("A young atopic man has recurrent food impactions and endoscopic rings. What is the likely diagnosis", "Eosinophilic oesophagitis", ["Schatzki ring only", "Viral croup", "Ranula"], "Atopy plus recurrent impaction strongly suggests EoE.", True),
        q("Biopsy in eosinophilic oesophagitis shows increased", "Eosinophils in oesophageal mucosa", ["Amyloid only", "Sulfur granules", "Psammoma bodies"], "Dense eosinophilic infiltration supports EoE.", True),
    ],
    "Oesophageal Carcinoma and Premalignant Disease": [
        q("The two main histologic types of oesophageal carcinoma are adenocarcinoma and", "Squamous cell carcinoma", ["Medullary carcinoma", "Pleomorphic adenoma", "Warthin tumor"], "SCC and adenocarcinoma are the major types."),
        q("Squamous cell carcinoma of oesophagus is strongly associated with tobacco, alcohol and", "Caustic stricture or achalasia in selected patients", ["Otosclerosis", "Mumps", "Nasal allergy"], "Chronic irritation and stasis increase SCC risk."),
        q("A man has progressive dysphagia, weight loss and an irregular shouldered stricture. What is the diagnosis", "Oesophageal carcinoma", ["Simple globus", "Viral pharyngitis", "Schatzki ring"], "Progressive dysphagia and malignant stricture pattern are red flags.", True),
        q("Adenocarcinoma of oesophagus is associated with", "Barrett oesophagus", ["Plummer-Vinson syndrome", "Mumps", "Zenker alone"], "Barrett metaplasia predisposes to adenocarcinoma."),
        q("Progressive dysphagia in oesophageal cancer usually begins with", "Solids", ["Liquids only from start", "No swallowing symptoms", "Only saliva"], "Mechanical obstruction first affects solids."),
        q("A patient with Barrett oesophagus develops nodularity and dysphagia. What is the next step", "Endoscopic biopsy and staging evaluation", ["Ignore as reflux", "Only antacid forever", "Epley maneuver"], "New alarm symptoms in Barrett require endoscopy and tissue diagnosis.", True),
        q("Staging of oesophageal cancer commonly uses CT, endoscopic ultrasound and", "PET-CT when indicated", ["Audiogram", "Nasal smear", "Tonsil culture only"], "Local depth, nodes and metastases guide management."),
        q("Hoarseness in oesophageal cancer suggests possible involvement of the", "Recurrent laryngeal nerve", ["Facial nerve", "Lingual nerve", "Optic nerve"], "Advanced disease may invade or compress RLN."),
        q("A patient with oesophageal cancer develops new hoarseness and aspiration. What does this suggest", "Recurrent laryngeal nerve involvement", ["Benign reflux only", "Aphthous ulcer", "Mumps"], "RLN palsy causes hoarseness and aspiration risk.", True),
        q("Treatment of oesophageal cancer depends on stage and may include surgery, chemotherapy and", "Radiotherapy", ["Sialendoscopy", "Myringoplasty", "Adenoidectomy"], "Management is multimodal and stage-specific.", True),
    ],
    "Paediatric Oesophageal Disorders": [
        q("The commonest type of tracheoesophageal fistula has oesophageal atresia with", "Distal tracheoesophageal fistula", ["Proximal fistula only", "No fistula always", "Double oesophagus"], "The common form has blind upper pouch and distal fistula."),
        q("Oesophageal atresia in a newborn presents with frothing, choking and", "Inability to pass nasogastric tube", ["Posterior epistaxis", "Parotid pain", "Hoarse adult voice"], "A tube coiling in the upper pouch is a key clue."),
        q("A newborn has excessive salivation, coughing with feeds and NG tube coiled in the upper pouch. What is the diagnosis", "Oesophageal atresia with tracheoesophageal fistula", ["Pyloric stenosis", "Mumps", "Adenoid hypertrophy"], "Classic neonatal presentation suggests oesophageal atresia/TEF.", True),
        q("Oesophageal atresia is associated with", "VACTERL anomalies", ["MEN2 only", "CHARGE only", "Kartagener only"], "Associated vertebral, anorectal, cardiac, TE, renal and limb anomalies are sought."),
        q("Initial management of suspected oesophageal atresia includes keeping nil oral and", "Suctioning the upper pouch", ["Force feeding", "Blind dilatation", "Oral contrast bolus"], "Aspiration prevention and stabilization precede surgery."),
        q("A newborn with oesophageal atresia develops respiratory distress from aspiration. What is the priority", "Airway protection and upper pouch suction", ["Immediate oral feeds", "Nasal cautery", "Tonsillectomy"], "Secretions pool in the pouch and can enter the airway.", True),
        q("Congenital oesophageal stenosis causes", "Progressive feeding difficulty when solids are introduced", ["Posterior epistaxis", "Pinna swelling", "Vertigo"], "Narrowing becomes more obvious with thicker feeds or solids."),
        q("A child has dysphagia after button battery ingestion months ago. The likely late complication is", "Oesophageal stricture", ["Mumps", "Otosclerosis", "Ranula"], "Deep caustic injury from battery can heal with stenosis."),
        q("A child with repaired tracheoesophageal fistula has recurrent cough during meals. What does this suggest", "Recurrent fistula or aspiration", ["Simple nasal allergy", "Warthin tumor", "Vocal nodule only"], "Post-repair coughing with feeds needs evaluation for fistula or swallow dysfunction.", True),
        q("Peptic stricture in children with severe reflux results from", "Chronic acid injury and fibrosis", ["Ear wax", "Adenoid involution", "Parotid tumor"], "Long-standing reflux oesophagitis can scar and narrow the lumen.", True),
    ],
}


def build_questions():
    questions = []
    for topic_order, topic in enumerate(TOPIC_NAMES, 1):
        rows = ROWS[topic]
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        clinical_count = sum(1 for row in rows if "clinical" in row.get("tags", []))
        if clinical_count != 4:
            raise ValueError(f"{topic} has {clinical_count} clinical questions, expected 4")
        topic_slug = slugify(topic)
        for question_order, row in enumerate(rows, 1):
            questions.append({
                "id": f"ent-oesophagus-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ENT oesophagus question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ENT oesophagus questions.")


if __name__ == "__main__":
    main()
