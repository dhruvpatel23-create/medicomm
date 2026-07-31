import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ent"
SUBJECT_TITLE = "ENT"
CHAPTER = "Diseases of Nose and Paranasal Sinuses"
CHAPTER_ORDER = 2
SOURCE_PDF = "ent 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def punctuate(prompt):
    prompt = prompt.strip()
    if not prompt:
        return prompt
    if prompt[-1] in ".?!:":
        return prompt
    replacements = [
        (". The bleeding point is most likely in", ". Where is the bleeding point most likely located?"),
        (". The diagnosis is most likely", ". What is the most likely diagnosis?"),
        (". The most likely diagnosis is", ". What is the most likely diagnosis?"),
        (". The likely diagnosis is", ". What is the likely diagnosis?"),
        (". The likely lesion is", ". What is the likely lesion?"),
        (". The likely source is", ". What is the likely source?"),
        (". The likely mechanism is", ". What is the likely mechanism?"),
        (". The likely condition is", ". What is the likely condition?"),
        (". The next step is", ". What is the next step?"),
        (". The next useful step is", ". What is the next useful step?"),
        (". Treatment is", ". What is the treatment?"),
        (". The diagnosis is", ". What is the diagnosis?"),
        (". This suggests", ". What does this suggest?"),
        (". This points toward", ". What does this point toward?"),
        (". This is typical of", ". What is this typical of?"),
        (". This favors", ". What does this favor?"),
    ]
    for old, new in replacements:
        if prompt.endswith(old):
            return f"{prompt[:-len(old)]}{new}"
    if prompt.lower().endswith((" in", " by", " due to", " from", " with", " of the", " around the", " because", " mainly", " called")):
        return f"{prompt}:"
    question_starters = ("Which ", "What ", "Why ", "How ", "When ", "Where ")
    if prompt.startswith(question_starters):
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
    ("Nasal Anatomy, Physiology and Examination", [
        q("The main arterial supply to the anteroinferior nasal septum comes from Kiesselbach plexus, also called", "Little area", ["Woodruff plexus", "Agger nasi", "Sphenoethmoidal recess"], "Little area is a vascular watershed and the common site of anterior epistaxis."),
        q("Which structure forms the main support of the external nasal dorsum", "Nasal bones and upper lateral cartilages", ["Inferior turbinates only", "Soft palate", "Nasopharyngeal tonsil"], "The nasal bones and upper lateral cartilages form the upper framework of the external nose."),
        q("A patient has recurrent anterior epistaxis from a visible vessel on the anteroinferior septum. The bleeding point is most likely in", "Little area", ["Posterior choana", "Frontal recess", "Inferior meatus"], "Most anterior nosebleeds arise from Kiesselbach plexus on the anterior septum.", True),
        q("The inferior meatus receives the opening of the", "Nasolacrimal duct", ["Frontal sinus", "Sphenoid sinus", "Posterior ethmoid cells"], "The nasolacrimal duct drains beneath the inferior turbinate."),
        q("What is the main function of turbinates in nasal physiology", "Humidification, warming and filtration of inspired air", ["Production of endolymph", "Closure of vocal cords", "Movement of ossicles"], "Turbinates increase mucosal surface area and condition inspired air."),
        q("A patient develops clear watery rhinorrhea while eating spicy food, without itching or sneezing. This points toward", "Gustatory nonallergic rhinitis", ["Acute bacterial sinusitis", "Nasal myiasis", "Septal abscess"], "Gustatory rhinitis is a nonallergic autonomic rhinorrhea triggered by food.", True),
        q("The olfactory cleft is located high in the nasal cavity around the", "Superior turbinate and upper septum", ["Inferior meatus", "Vestibule only", "Nasolacrimal duct opening"], "Olfactory mucosa lies in the roof, superior turbinate region and adjacent septum."),
        q("Diagnostic nasal endoscopy is especially useful because it allows direct visualization of the", "Middle meatus and sphenoethmoidal recess", ["Cochlear promontory", "Laryngeal ventricle only", "External auditory canal"], "Endoscopy shows drainage pathways and hidden lesions not seen on anterior rhinoscopy."),
        q("A patient with unilateral nasal obstruction has a smooth mass seen behind the inferior turbinate on endoscopy. The next useful step is", "Endoscopic assessment with imaging if needed", ["Blind avulsion in clinic", "Stapedotomy", "Tonsillectomy first"], "Unilateral obstruction needs proper endoscopic localization and often imaging before treatment.", True),
        q("The nasal cycle refers to alternating congestion and decongestion of the nasal mucosa due to", "Autonomic regulation of venous sinusoids", ["Ossicular reflexes", "Ciliary muscle contraction", "Permanent septal cartilage growth"], "Autonomic tone shifts vascular engorgement between the two nasal cavities.", True),
    ]),
    ("Congenital and Developmental Nasal Conditions", [
        q("Bilateral choanal atresia in a newborn is dangerous because neonates are mainly", "Obligate nasal breathers", ["Obligate mouth breathers", "Unable to swallow", "Unable to produce mucus"], "Newborns depend heavily on nasal breathing, so bilateral obstruction causes respiratory distress."),
        q("A newborn has cyclical cyanosis relieved by crying and inability to pass a catheter through either nostril. The diagnosis is most likely", "Bilateral choanal atresia", ["Nasal polyp", "Allergic rhinitis", "Septal perforation"], "Cyanosis relieved by crying is classic for bilateral posterior nasal obstruction.", True),
        q("Choanal atresia most commonly involves", "Bony or mixed bony-membranous obstruction", ["Only pure cartilage", "Only turbinate hypertrophy", "Only fungal debris"], "Most choanal atresia is bony or mixed rather than purely membranous."),
        q("A congenital midline nasal swelling that enlarges on crying should raise concern for", "Encephalocele", ["Furuncle", "Allergic polyp", "Rhinosporidiosis"], "A compressible mass with intracranial connection must not be biopsied blindly.", True),
        q("Which congenital nasal lesion may have hair protruding from a small midline pit", "Nasal dermoid sinus", ["Antrochoanal polyp", "Septal hematoma", "Inferior turbinate hypertrophy"], "Nasal dermoids may present as midline pits with hair and can extend intracranially."),
        q("Before excising a suspected nasal dermoid, the important investigation is", "CT or MRI to assess intracranial extension", ["Pure tone audiometry", "Barium swallow", "Caloric test"], "Imaging defines bony defects and intracranial tract before surgery."),
        q("A child has a firm midline nasal mass with a hair-bearing pit and recurrent discharge. The most likely lesion is", "Nasal dermoid", ["Juvenile nasopharyngeal angiofibroma", "Fungal ball", "Septal spur"], "A midline pit with discharge strongly suggests nasal dermoid sinus.", True),
        q("CHARGE association is classically linked with choanal atresia and", "Coloboma and cardiac defects", ["Cholesteatoma and otosclerosis", "Cleft lip only", "Chronic laryngitis"], "CHARGE includes coloboma, heart defects, choanal atresia, growth retardation, genital and ear anomalies."),
        q("Unilateral choanal atresia may present later with", "Persistent unilateral nasal discharge and obstruction", ["Bilateral aphonia", "Pulsatile tinnitus", "Conductive deafness only"], "Unilateral cases may be missed until chronic one-sided obstruction or discharge appears."),
        q("A six-year-old has persistent right-sided obstruction and foul discharge since infancy. A catheter cannot pass into the nasopharynx on that side. This suggests", "Unilateral choanal atresia", ["Bilateral nasal allergy", "Otosclerosis", "Acute tonsillitis"], "Longstanding unilateral obstruction with failed catheter passage supports choanal atresia.", True),
    ]),
    ("Nasal Trauma, Septum and Structural Obstruction", [
        q("The most urgent septal complication after nasal trauma is", "Septal hematoma", ["Septal spur", "Allergic crease", "Inferior turbinate hypertrophy"], "A septal hematoma can cause cartilage necrosis and saddle-nose deformity if not drained."),
        q("A boy is hit on the nose and develops bilateral soft septal swelling with nasal obstruction. The next step is", "Urgent incision and drainage", ["Observation for six months", "Intranasal steroid alone", "Stapedotomy"], "Septal hematoma requires urgent drainage and antibiotics.", True),
        q("Septal abscess can lead to saddle nose because it damages the", "Septal cartilage blood supply", ["Nasolacrimal duct", "Inferior turbinate bone", "Soft palate muscle"], "Cartilage depends on perichondrial nutrition; pus or hematoma separates it from supply."),
        q("A deviated nasal septum most commonly causes", "Nasal obstruction", ["Sensorineural deafness", "True vertigo", "Hemoptysis"], "Mechanical narrowing and turbinate compensation commonly produce obstruction."),
        q("Cottle test improves nasal airflow when obstruction is due to", "Nasal valve collapse", ["Sphenoid sinusitis", "Septal perforation only", "Choanal atresia"], "Lateral traction opens the nasal valve area."),
        q("A patient has obstruction that improves when the cheek is pulled laterally. This suggests", "Internal nasal valve narrowing", ["Posterior epistaxis", "Atrophic rhinitis", "Fungal sinusitis"], "Improvement with lateral traction supports nasal valve compromise.", True),
        q("Septoplasty is mainly performed to correct", "Symptomatic deviated nasal septum", ["Acute otitis media", "Vocal cord palsy", "Meniere disease"], "Septoplasty reshapes obstructing septal cartilage or bone while preserving support."),
        q("A septal perforation may cause whistling because airflow passes through", "A hole between the two nasal cavities", ["Blocked nasolacrimal duct", "Closed choana", "Frontal sinus osteoma"], "Small anterior perforations can create turbulent airflow and whistling."),
        q("A cocaine user has crusting, whistling and an anterior septal perforation. The likely mechanism is", "Ischemic mucosal and cartilage injury", ["Excessive endolymph", "Stapes fixation", "Adenoid hypertrophy"], "Cocaine causes vasoconstriction and mucosal necrosis, leading to perforation.", True),
        q("A depressed nasal bridge after untreated septal abscess is called", "Saddle nose deformity", ["Binder syndrome", "Pott puffy tumor", "Killian polyp"], "Loss of septal cartilage support produces saddle deformity.", True),
    ]),
    ("Epistaxis and Nasal Vascular Disorders", [
        q("The commonest site of epistaxis is", "Little area on anterior nasal septum", ["Sphenoid rostrum", "Posterior ethmoid roof", "Inferior meatus"], "Most nosebleeds are anterior and arise from Kiesselbach plexus."),
        q("Woodruff plexus is associated mainly with", "Posterior epistaxis", ["Anterior septal bleeding", "Nasal valve collapse", "Frontal sinus mucocele"], "Posterior epistaxis commonly arises from posterior lateral nasal wall venous plexus."),
        q("An elderly hypertensive patient has heavy bleeding running into the throat with no anterior point seen. This is most likely", "Posterior epistaxis", ["Allergic rhinitis", "Nasal dermoid", "Vestibulitis"], "Brisk bleeding into the pharynx with no anterior source suggests posterior epistaxis.", True),
        q("Initial management of uncomplicated anterior epistaxis includes sitting forward and", "Pinching the soft part of the nose", ["Lying flat with head extended", "Immediate tracheostomy", "Blind posterior packing first"], "Firm pressure over the soft nose compresses anterior septal vessels."),
        q("Chemical cautery for anterior epistaxis should usually avoid cauterizing", "Both sides of septum at the same level", ["Only one visible bleeding point", "The side with local anesthesia", "The vestibule skin"], "Opposing septal cautery increases risk of septal perforation."),
        q("A child has recurrent small-volume anterior nosebleeds from a visible septal vessel. Best office treatment after topical preparation is", "Silver nitrate cautery to the bleeding point", ["Cochlear implantation", "Radical mastoidectomy", "Endolymphatic sac surgery"], "A discrete anterior bleeding point can be treated with chemical cautery.", True),
        q("Hereditary hemorrhagic telangiectasia causes epistaxis due to", "Fragile mucocutaneous telangiectasias", ["Stapes fixation", "Fungal concretions", "Choanal membrane"], "Telangiectatic vessels bleed easily, often recurrently."),
        q("A teenager with recurrent epistaxis and telangiectasias on lips and tongue may have", "Hereditary hemorrhagic telangiectasia", ["Wegener granulomatosis only", "Antrochoanal polyp", "Rhinitis medicamentosa"], "Mucocutaneous telangiectasias with recurrent epistaxis suggest HHT.", True),
        q("Failure of anterior and posterior packing in severe epistaxis may require", "Endoscopic sphenopalatine artery ligation", ["Tonsillectomy", "Stapedectomy", "Myringoplasty"], "The sphenopalatine artery is a key terminal vessel in severe posterior epistaxis."),
        q("In epistaxis, resuscitation and airway assessment come before local control when the patient has", "Hemodynamic instability or compromised airway", ["Mild itching only", "Watery rhinorrhea", "Stable dry crusts"], "Heavy bleeding can threaten circulation and airway, so ABCs come first.", True),
    ]),
    ("Allergic, Vasomotor and Other Rhinitis", [
        q("Allergic rhinitis is mediated primarily by", "IgE-mediated mast cell activation", ["Type II cytotoxic reaction", "Endolymphatic hydrops", "Stapes fixation"], "Allergen-specific IgE on mast cells drives sneezing, itching and watery discharge."),
        q("The classic symptom combination in allergic rhinitis is sneezing, itching, watery rhinorrhea and", "Nasal obstruction", ["Purulent otorrhea", "Hemoptysis", "Facial nerve palsy"], "Allergic rhinitis commonly combines itch, sneeze, rhinorrhea and blockage."),
        q("A student gets sneezing bouts, itchy eyes and watery rhinorrhea every spring. The most likely diagnosis is", "Seasonal allergic rhinitis", ["Atrophic rhinitis", "Invasive fungal sinusitis", "Septal hematoma"], "Seasonal allergen exposure with ocular itching is typical.", True),
        q("First-line long-term treatment for moderate persistent allergic rhinitis is usually", "Intranasal corticosteroid", ["Oral aminoglycoside", "Emergency septoplasty", "Posterior nasal packing"], "Intranasal steroids best control nasal inflammation and obstruction."),
        q("Rhinitis medicamentosa is caused by overuse of", "Topical nasal decongestant drops", ["Saline spray", "Intranasal steroid", "Antihistamine eye drops"], "Prolonged topical alpha-agonist use causes rebound congestion."),
        q("A patient has severe congestion after using oxymetazoline several times daily for weeks. The diagnosis is", "Rhinitis medicamentosa", ["CSF rhinorrhea", "Nasal myiasis", "Choanal atresia"], "Rebound obstruction after decongestant abuse is rhinitis medicamentosa.", True),
        q("Nonallergic vasomotor rhinitis is best described as", "Autonomic nasal hyperreactivity without IgE allergy", ["Bacterial invasion of maxillary sinus", "Congenital posterior choanal block", "Granulomatous cartilage necrosis"], "Triggers such as temperature, odors or irritants can cause rhinorrhea and blockage."),
        q("Atrophic rhinitis is associated with roomy nasal cavities, crusting and", "Foul smell", ["Pulsatile tinnitus", "Bilateral facial palsy", "White attic debris"], "Crusting and secondary infection produce fetor, sometimes with paradoxical obstruction."),
        q("A patient has wide nasal cavities packed with foul crusts but complains of blockage. This is typical of", "Atrophic rhinitis", ["Acute vestibulitis", "Juvenile angiofibroma", "Silent sinus syndrome"], "Atrophic rhinitis can produce paradoxical nasal obstruction despite roomy cavities.", True),
        q("Allergen immunotherapy is most appropriate when symptoms are significant and", "Specific allergen sensitivity is demonstrated", ["There is septal abscess", "The patient has posterior packing", "A tumor is suspected"], "Immunotherapy targets proven clinically relevant allergens.", True),
    ]),
    ("Acute and Chronic Rhinosinusitis", [
        q("Acute bacterial rhinosinusitis is more likely when symptoms persist beyond 10 days, worsen after initial improvement, or are", "Severe with high fever and purulent discharge", ["Limited to one sneeze", "Only triggered by spicy food", "Present since birth"], "Persistence, double worsening and severe onset support bacterial sinusitis."),
        q("The osteomeatal complex is important because it drains the frontal, maxillary and", "Anterior ethmoid sinuses", ["Sphenoid sinus only", "Nasolacrimal sac", "Middle ear"], "The OMC is the common drainage pathway for anterior group sinuses."),
        q("A patient has purulent nasal discharge, facial pressure and fever for 12 days after a viral cold. The diagnosis is most likely", "Acute bacterial rhinosinusitis", ["Allergic rhinitis alone", "Septal perforation", "Vestibular schwannoma"], "Persistent purulent symptoms after URI suggest bacterial rhinosinusitis.", True),
        q("Chronic rhinosinusitis is diagnosed when sinonasal inflammation lasts at least", "12 weeks", ["24 hours", "3 days", "2 weeks"], "CRS requires at least 12 weeks of symptoms plus objective evidence."),
        q("Objective evidence in chronic rhinosinusitis can be provided by nasal endoscopy or", "CT scan of paranasal sinuses", ["Pure tone audiogram", "Chest ECG", "Barium swallow"], "Endoscopy and CT demonstrate mucosal disease, polyps or drainage obstruction."),
        q("A man has 5 months of nasal blockage, hyposmia and mucopurulent drainage. CT shows mucosal thickening in multiple sinuses. This is", "Chronic rhinosinusitis", ["Acute vestibulitis", "Choanal atresia", "Otosclerosis"], "Symptoms beyond 12 weeks with objective CT changes meet CRS criteria.", True),
        q("Functional endoscopic sinus surgery mainly aims to", "Restore sinus ventilation and drainage pathways", ["Remove the stapes", "Close the eustachian tube", "Destroy olfactory bulb"], "FESS opens obstructed drainage routes while preserving mucosa when possible."),
        q("Odontogenic maxillary sinusitis should be suspected with unilateral maxillary disease and", "Dental infection or recent dental procedure", ["Bilateral itchy eyes only", "Congenital deafness", "Pulsatile tinnitus"], "Upper dental roots are close to the maxillary sinus floor."),
        q("After dental extraction, a patient develops unilateral foul nasal discharge and maxillary pain. The likely source is", "Odontogenic maxillary sinusitis", ["Seasonal allergy", "Nasal dermoid", "BPPV"], "Dental manipulation can seed or communicate with the maxillary sinus.", True),
        q("In uncomplicated viral rhinosinusitis, routine antibiotics are avoided because the illness is usually", "Self-limited", ["Always fungal", "Always malignant", "Caused by stapes fixation"], "Most acute viral sinus symptoms resolve with supportive care.", True),
    ]),
    ("Nasal Polyps and Polypoid Disorders", [
        q("Nasal polyps are usually", "Pale, edematous and insensitive masses", ["Red painful vascular tumors", "Hard bony septal spurs", "Black necrotic crusts only"], "Inflammatory polyps are soft, pale and often insensitive."),
        q("Bilateral ethmoidal polyps are commonly associated with", "Chronic rhinosinusitis and allergy/asthma", ["Otosclerosis", "Septal hematoma", "Acute mastoiditis"], "Diffuse inflammatory disease often produces bilateral polyposis."),
        q("A patient with asthma has bilateral pale nasal masses, anosmia and recurrent sinusitis. The likely diagnosis is", "Chronic rhinosinusitis with nasal polyps", ["Juvenile nasopharyngeal angiofibroma", "Septal abscess", "Choanal atresia"], "Asthma, smell loss and bilateral pale polyps fit CRSwNP.", True),
        q("Antrochoanal polyp usually arises from the", "Maxillary sinus", ["Sphenoid sinus", "Frontal sinus only", "Nasal vestibule skin"], "It originates in the maxillary sinus and extends through the choana."),
        q("A unilateral smooth polyp extending backward into the choana in a child is most suggestive of", "Antrochoanal polyp", ["Ethmoidal polyposis", "Atrophic rhinitis", "Septal perforation"], "Antrochoanal polyps are classically unilateral and choanal."),
        q("A teenager has unilateral nasal obstruction and a pale mass passing into the nasopharynx from the maxillary sinus. Treatment is", "Endoscopic removal including antral component", ["Silver nitrate cautery only", "Posterior nasal packing forever", "Cochlear implant"], "Complete removal must address the maxillary antral origin to reduce recurrence.", True),
        q("Aspirin-exacerbated respiratory disease includes asthma, nasal polyps and sensitivity to", "Aspirin or other COX-1 inhibitors", ["Penicillin only", "Topical saline", "Local anesthetic"], "AERD is the triad of asthma, CRSwNP and NSAID sensitivity."),
        q("Cystic fibrosis should be considered in a child with recurrent nasal polyps and", "Chronic chest infections or failure to thrive", ["Facial palsy", "Conductive hearing only", "Vertigo on turning"], "Pediatric nasal polyposis warrants evaluation for systemic disease such as cystic fibrosis."),
        q("A child with bilateral nasal polyps, chronic cough and poor growth should be evaluated for", "Cystic fibrosis", ["Meniere disease", "Otosclerosis", "Bell palsy"], "Nasal polyps in children are uncommon and cystic fibrosis is an important association.", True),
        q("Topical intranasal steroids help nasal polyps mainly by", "Reducing mucosal inflammation and polyp size", ["Fixing the stapes", "Closing septal perforations", "Killing all fungi"], "Steroids reduce inflammatory edema and recurrence tendency.", True),
    ]),
    ("Fungal, Granulomatous and Destructive Nasal Disease", [
        q("Allergic fungal rhinosinusitis typically contains thick allergic mucin with", "Fungal hyphae without tissue invasion", ["Stapes prosthesis", "Caseating bone only", "Endolymph crystals"], "AFRS is a hypersensitivity process with eosinophilic mucin and noninvasive fungi."),
        q("A young atopic patient has nasal polyps, expanded sinuses and thick peanut-butter-like allergic mucin. The diagnosis is", "Allergic fungal rhinosinusitis", ["Acute invasive fungal sinusitis", "Septal hematoma", "Choanal atresia"], "Polyps with allergic mucin and sinus expansion suggest AFRS.", True),
        q("Acute invasive fungal sinusitis is most feared in patients with", "Diabetes ketoacidosis or immunosuppression", ["Simple allergic rhinitis only", "Wax impaction", "Otosclerosis"], "Mucor and Aspergillus can invade vessels in immunocompromised or acidotic patients."),
        q("Black eschar on the turbinate in a diabetic patient with facial pain suggests", "Acute invasive fungal rhinosinusitis", ["Vasomotor rhinitis", "Antrochoanal polyp", "Rhinitis medicamentosa"], "Necrotic black tissue reflects angioinvasive fungal disease and is an emergency.", True),
        q("Rhinosporidiosis classically appears as a strawberry-like mass due to", "White sporangia dots on a vascular polypoid lesion", ["Septal cartilage collapse only", "Keratin pearls", "Nasal valve collapse"], "The lesion is vascular and dotted with sporangia."),
        q("Treatment of rhinosporidiosis is mainly", "Surgical excision with cauterization of base", ["Antihistamine alone", "Stapedotomy", "Grommet insertion"], "Complete excision and cautery reduce recurrence and bleeding."),
        q("A patient has a friable red nasal mass with white dots and recurrent bleeding after pond-water exposure. This suggests", "Rhinosporidiosis", ["Otosclerosis", "BPPV", "Septal hematoma"], "Strawberry mass with white dots is a classic exam clue.", True),
        q("Granulomatosis with polyangiitis may cause nasal disease with crusting, septal perforation and", "Saddle nose deformity", ["Stapes fixation", "Antrochoanal polyp only", "Inferior meatal cyst"], "Vasculitic cartilage destruction can collapse the nasal bridge."),
        q("Midline destructive nasal lesions require biopsy because important causes include lymphoma, vasculitis and", "Invasive fungal disease", ["Simple nasal cycle", "Physiologic turbinate swelling", "Benign wax"], "Destructive lesions have serious malignant, vasculitic and infective differentials."),
        q("A patient with chronic crusting, hematuria and saddle nose is most likely to have", "Granulomatosis with polyangiitis", ["Seasonal allergic rhinitis", "Choanal atresia", "Septal spur only"], "Upper airway destruction plus renal involvement supports GPA.", True),
    ]),
    ("Complications of Sinusitis and Mucoceles", [
        q("The most common orbital complication of sinusitis is", "Preseptal cellulitis", ["Optic glioma", "Otosclerosis", "Meniere disease"], "Inflammation may spread anterior to the orbital septum before deeper orbital disease develops."),
        q("A child with sinusitis has eyelid edema but normal eye movements and vision. This suggests", "Preseptal cellulitis", ["Orbital abscess", "Cavernous sinus thrombosis", "Optic neuritis"], "Normal vision and motility favor preseptal rather than orbital cellulitis.", True),
        q("Painful restricted eye movements and proptosis in sinusitis indicate", "Postseptal orbital involvement", ["Simple allergic rhinitis", "Septal perforation", "Nasal valve collapse"], "Orbital cellulitis or abscess threatens vision and requires urgent management."),
        q("The sinus most commonly associated with orbital complications is the", "Ethmoid sinus", ["Sphenoid sinus only", "Maxillary sinus floor only", "Frontal sinus exclusively"], "The lamina papyracea separates ethmoid cells from orbit."),
        q("Pott puffy tumor is", "Frontal bone osteomyelitis with subperiosteal abscess", ["Benign turbinate edema", "Nasal dermoid", "Maxillary retention cyst"], "Frontal sinusitis can spread to frontal bone causing forehead swelling."),
        q("A teenager with frontal sinusitis develops tender forehead swelling and fever. The diagnosis is", "Pott puffy tumor", ["Antrochoanal polyp", "Rhinitis medicamentosa", "Nasal vestibulitis"], "Forehead subperiosteal abscess after frontal sinusitis is Pott puffy tumor.", True),
        q("Cavernous sinus thrombosis can present with fever, chemosis and palsy of cranial nerves III, IV, V1, V2 and", "VI", ["VII only", "IX", "XII"], "The abducens nerve and ocular motor nerves are vulnerable in cavernous sinus thrombosis."),
        q("A sinus mucocele expands because of", "Obstructed sinus drainage with mucus retention", ["Acute septal hematoma", "Stapes fixation", "Allergen IgE alone"], "Blocked drainage traps mucus and slowly expands the sinus."),
        q("A patient has painless progressive proptosis from an expansile frontal sinus lesion on CT. The likely diagnosis is", "Frontal sinus mucocele", ["Acute vestibulitis", "Atrophic rhinitis", "Choanal atresia"], "Mucoceles expand and can displace the orbit.", True),
        q("Visual decline in sphenoid sinusitis is dangerous because inflammation is close to the", "Optic nerve", ["Facial recess", "Chorda tympani", "Tonsillar crypt"], "The optic nerve and cavernous sinus lie close to sphenoid disease.", True),
    ]),
    ("Benign and Malignant Sinonasal Tumors", [
        q("Unilateral nasal obstruction with blood-stained discharge should raise suspicion for", "Sinonasal tumor", ["Simple bilateral allergy", "Physiologic nasal cycle", "Otitis externa"], "Unilateral persistent symptoms, especially bleeding, need tumor exclusion."),
        q("Juvenile nasopharyngeal angiofibroma classically occurs in", "Adolescent males", ["Elderly females only", "Newborn girls", "Postmenopausal women"], "JNA is a vascular tumor of adolescent boys."),
        q("An adolescent boy has recurrent profuse epistaxis and a nasopharyngeal mass. Biopsy should be avoided because of risk of", "Severe bleeding", ["Instant deafness", "Septal perforation only", "CSF leak in every case"], "JNA is highly vascular; diagnosis is by imaging and angiography rather than routine biopsy.", True),
        q("The site of origin of juvenile nasopharyngeal angiofibroma is near the", "Sphenopalatine foramen", ["Inferior meatus", "Frontal sinus floor", "Nasal vestibule"], "JNA arises around the posterolateral nasal wall near the sphenopalatine foramen."),
        q("Inverted papilloma is important because it is locally aggressive and associated with", "Squamous cell carcinoma", ["Otosclerosis", "Meniere disease", "Bell palsy"], "Inverted papilloma can recur and undergo malignant transformation."),
        q("A middle-aged man has unilateral nasal obstruction and a cerebriform mass from the lateral nasal wall. The likely lesion is", "Inverted papilloma", ["Bilateral ethmoidal polyps", "Atrophic rhinitis", "Septal hematoma"], "Unilateral papillomatous lateral wall mass suggests inverted papilloma.", True),
        q("The commonest malignancy of the sinonasal tract is", "Squamous cell carcinoma", ["Osteoma", "Hemangioma", "Schwannoma"], "Squamous carcinoma is the most common sinonasal cancer."),
        q("Occupational wood dust exposure is associated with adenocarcinoma of the", "Ethmoid sinus", ["External ear canal", "Tonsil only", "Laryngeal ventricle"], "Wood dust exposure is a classic risk factor for ethmoid adenocarcinoma."),
        q("A carpenter develops unilateral nasal obstruction, epistaxis and an ethmoid mass. The occupational association points toward", "Sinonasal adenocarcinoma", ["Antrochoanal polyp", "Rhinitis medicamentosa", "Fungal ball only"], "Wood dust exposure increases risk of sinonasal adenocarcinoma.", True),
        q("Red flags in a unilateral nasal mass include epistaxis, facial numbness, orbital symptoms and", "Loosening of teeth or palatal swelling", ["Seasonal sneezing alone", "Clear bilateral rhinorrhea", "Itchy eyes only"], "Dental, palatal, orbital or neurologic signs suggest invasive sinonasal malignancy.", True),
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
                "id": f"ent-nose-pns-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ENT nose/PNS question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ENT nose and paranasal sinuses questions.")


if __name__ == "__main__":
    main()
