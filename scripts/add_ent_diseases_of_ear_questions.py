import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ent"
SUBJECT_TITLE = "ENT"
CHAPTER = "Diseases of Ear"
CHAPTER_ORDER = 1
SOURCE_PDF = "ent 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def q(prompt, answer, wrong, explanation, clinical=False, difficulty=None):
    prompt = prompt.strip()
    if prompt and prompt[-1] not in ".?!":
        prompt = f"{prompt}:"
    options = [answer, *wrong]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {
        "prompt": prompt,
        "options": options,
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty or ("high" if clinical else "moderate"),
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("Anatomy, Physiology and Examination of Ear", [
        q("The pars flaccida of the tympanic membrane is clinically important because acquired cholesteatoma commonly begins in the", "Attic retraction pocket", ["Anteroinferior pars tensa", "Promontory mucosa", "Round window niche"], "Poor ventilation of the epitympanum can create a pars flaccida retraction pocket that accumulates keratin."),
        q("Which ossicle is attached to the tympanic membrane by its handle?", "Malleus", ["Incus", "Stapes", "Lenticular process"], "The manubrium of malleus is embedded in the tympanic membrane."),
        q("The cone of light on otoscopy is normally seen in which quadrant of the right tympanic membrane?", "Anteroinferior quadrant", ["Posterosuperior quadrant", "Posteroinferior quadrant", "Anterosuperior quadrant"], "The light reflex runs downward and forward from the umbo in a normal right ear."),
        q("A child with earache has a red, bulging tympanic membrane with loss of landmarks. The most likely diagnosis is", "Acute otitis media", ["Otitis externa", "Tympanosclerosis", "Serous labyrinthitis"], "Bulging of the drum with acute pain and fever points to middle ear pus under pressure.", True),
        q("Rinne test is positive when", "Air conduction is better than bone conduction", ["Bone conduction is better than air conduction", "Both air and bone conduction are absent", "Weber lateralizes to the diseased ear"], "A positive Rinne is normal or sensorineural; a negative Rinne suggests conductive loss."),
        q("Weber test lateralizes to the affected ear in", "Conductive hearing loss", ["Symmetric normal hearing", "Unilateral cochlear loss", "Bilateral equal sensorineural loss"], "Conductive loss reduces environmental masking, so bone-conducted sound is perceived louder in the affected ear."),
        q("A patient hears Weber louder in the left ear and has negative Rinne on the left. The pattern is", "Left conductive hearing loss", ["Left sensorineural hearing loss", "Right conductive hearing loss", "Nonorganic hearing loss"], "Weber lateralization to the left plus left BC greater than AC is a conductive pattern.", True),
        q("The eustachian tube mainly helps the middle ear by", "Equalizing pressure and draining secretions", ["Producing endolymph", "Moving the stapes footplate", "Suppressing mastoid pneumatization"], "Ventilation and mucociliary clearance through the tube maintain middle ear function."),
        q("A postoperative patient develops altered taste over the anterior two-thirds of tongue after middle ear surgery. The nerve most likely stretched is", "Chorda tympani", ["Jacobson nerve", "Auriculotemporal nerve", "Greater petrosal nerve"], "Chorda tympani crosses the middle ear and carries taste fibers from the anterior tongue.", True),
        q("A fistula test is used primarily to detect abnormal communication involving the", "Lateral semicircular canal", ["Cochlear aqueduct", "Mastoid emissary vein", "Internal auditory canal"], "Pressure-induced vertigo or nystagmus suggests a labyrinthine fistula, commonly lateral canal erosion.", True),
    ]),
    ("External Ear Disorders and Otitis Externa", [
        q("The organism classically associated with malignant otitis externa is", "Pseudomonas aeruginosa", ["Streptococcus pyogenes", "Moraxella catarrhalis", "Candida albicans"], "Necrotizing external otitis is typically due to invasive Pseudomonas infection."),
        q("Furunculosis of the external auditory canal arises from infection of hair follicles in the", "Cartilaginous canal", ["Bony canal", "Middle ear cleft", "Mastoid antrum"], "Hair follicles are present in the lateral cartilaginous canal."),
        q("A diabetic elderly man has severe otalgia, granulation tissue at the canal floor and facial weakness. The best diagnosis is", "Malignant otitis externa", ["Keratosis obturans", "Bullous myringitis", "Serous otitis media"], "Severe otalgia with granulation at the bony-cartilaginous junction in a diabetic is typical.", True),
        q("Otomycosis most often presents with", "Itching, blocked ear and fungal debris", ["Painless pulsatile otorrhea", "Sudden facial palsy only", "Profound congenital deafness"], "Fungal otitis externa commonly causes pruritus and characteristic wet or black-white debris."),
        q("Exostoses of the external canal are strongly associated with", "Repeated cold water exposure", ["Adenoid hypertrophy", "Otosclerosis", "Meniere disease"], "Surfer's ear reflects benign bony narrowing after chronic cold-water irritation."),
        q("A swimmer develops tragal tenderness and edematous external canal after repeated pool exposure. The likely condition is", "Diffuse otitis externa", ["Acute mastoiditis", "Cholesteatoma", "Otosclerosis"], "Pain on tragal pressure with canal edema after water exposure favors otitis externa.", True),
        q("The first step for an impacted hard cerumen plug causing conductive loss is usually", "Wax softening followed by careful removal", ["Immediate mastoidectomy", "Systemic aminoglycoside therapy", "Stapedotomy"], "Cerumen is treated by softening, syringing if safe, suction or instrumentation."),
        q("Perichondritis of pinna characteristically spares the", "Lobule", ["Helix", "Concha", "Antihelix"], "The lobule lacks cartilage, so cartilage perichondritis usually spares it."),
        q("A painful swollen pinna after piercing involves the upper cartilage and spares the lobule. The likely diagnosis is", "Pinna perichondritis", ["Mastoid abscess", "Preauricular sinus", "Otitis media with effusion"], "Cartilage infection after trauma or piercing causes tender pinna swelling with lobular sparing.", True),
        q("A teenager has severe bilateral otalgia and a large circumferential keratin plug widening the bony canal. This favors", "Keratosis obturans", ["External canal cholesteatoma", "Otosclerosis", "Meniere disease"], "Keratosis obturans causes painful plug-like keratin accumulation with generalized canal expansion.", True),
    ]),
    ("Acute Otitis Media and Otitis Media with Effusion", [
        q("The most common route by which infection reaches the middle ear in acute otitis media is through the", "Eustachian tube", ["External auditory canal", "Internal auditory canal", "Cochlear aqueduct"], "Upper respiratory infection spreads to the middle ear chiefly through the eustachian tube."),
        q("The commonest bacteria in acute otitis media include Streptococcus pneumoniae, Haemophilus influenzae and", "Moraxella catarrhalis", ["Pseudomonas aeruginosa", "Treponema pallidum", "Mycobacterium leprae"], "These three organisms dominate uncomplicated bacterial AOM in children."),
        q("A crying toddler has fever, otalgia and a tense yellow tympanic membrane. The best immediate diagnosis is", "Suppurative acute otitis media", ["Otosclerosis", "Meniere disease", "Presbycusis"], "Pain, fever and a bulging drum indicate acute purulent middle ear infection.", True),
        q("Otitis media with effusion produces hearing loss mainly because", "Fluid dampens tympanic membrane and ossicular movement", ["Outer hair cells are destroyed", "Endolymph pressure ruptures the saccule", "The auditory nerve demyelinates"], "Middle ear fluid creates a conductive hearing loss."),
        q("A type B flat tympanogram most strongly suggests", "Middle ear effusion", ["Normal middle ear pressure", "Ossicular discontinuity only", "Retrocochlear lesion"], "A flat tympanogram is typical when fluid reduces tympanic membrane mobility."),
        q("A school child has inattentiveness, mild conductive hearing loss and dull retracted drums after repeated colds. The likely diagnosis is", "Otitis media with effusion", ["Acute mastoiditis", "Noise-induced hearing loss", "Vestibular neuritis"], "Glue ear often presents with hearing and school problems rather than pain.", True),
        q("Adenoid hypertrophy promotes otitis media with effusion chiefly by", "Blocking eustachian tube function", ["Fixing the stapes footplate", "Eroding the lateral canal", "Producing cholesteatoma matrix directly"], "Adenoids obstruct the nasopharyngeal opening and harbor infection."),
        q("Myringotomy with grommet insertion is used in persistent effusion to", "Ventilate the middle ear", ["Ablate the cochlea", "Remove the stapes", "Close the eustachian tube"], "Ventilation tubes bypass poor eustachian tube function and improve conductive loss."),
        q("An adult has unilateral persistent middle ear effusion without infection. The important site to examine is the", "Nasopharynx", ["Thyroid gland", "Parotid duct", "Frontal sinus"], "Adult unilateral OME can signal nasopharyngeal obstruction, including malignancy.", True),
        q("A febrile child with acute otitis media suddenly develops mucopurulent otorrhea and pain relief. This indicates", "Suppuration with perforation", ["Tubal occlusion only", "Resolution before pus forms", "Adhesive otitis"], "Pain may decrease once the tense drum perforates and pus drains.", True),
    ]),
    ("Chronic Otitis Media and Cholesteatoma", [
        q("The unsafe type of chronic otitis media is dangerous mainly because of", "Cholesteatoma with bone erosion", ["Wax impaction", "Isolated myringosclerosis", "Simple otitis externa"], "Squamous disease can erode ossicles, facial canal, labyrinth and tegmen."),
        q("A central perforation with intermittent mucopurulent discharge is typical of", "Tubotympanic chronic otitis media", ["Atticoantral disease", "Otosclerosis", "Vestibular schwannoma"], "Mucosal disease usually causes a central pars tensa perforation."),
        q("A patient has foul-smelling scanty ear discharge, attic perforation and granulation. The likely diagnosis is", "Atticoantral chronic otitis media with cholesteatoma", ["Otitis media with effusion", "Diffuse otitis externa", "Presbycusis"], "Attic disease with foul discharge is cholesteatoma until proved otherwise.", True),
        q("The hallmark tissue in cholesteatoma is", "Keratinizing squamous epithelium in the middle ear", ["Goblet cell metaplasia only", "Normal respiratory mucosa", "Otosclerotic vascular bone"], "Cholesteatoma is a squamous epithelial sac accumulating keratin."),
        q("The commonest ossicle eroded by cholesteatoma is the", "Long process of incus", ["Stapes footplate", "Handle of malleus", "Head of malleus"], "The long process of incus is delicate and poorly vascularized."),
        q("A man with chronic foul ear discharge develops vertigo on tragal pressure. This suggests", "Lateral semicircular canal fistula", ["Simple wax impaction", "Presbycusis", "Serous otitis media"], "Pressure-induced vertigo in cholesteatoma suggests labyrinthine fistula.", True),
        q("The definitive treatment for unsafe chronic otitis media is usually", "Mastoid surgery to eradicate disease", ["Repeated wax syringing only", "Long-term vestibular sedatives", "Stapedotomy"], "Cholesteatoma requires surgical clearance because medicines cannot remove matrix."),
        q("Tympanoplasty primarily aims to", "Repair tympanic membrane and improve hearing", ["Destroy the cochlea", "Paralyze tensor tympani", "Open the endolymphatic sac"], "Tympanoplasty reconstructs the drum and may address ossicular chain problems."),
        q("A dry subtotal central perforation with conductive hearing loss but no cholesteatoma is best managed electively by", "Myringoplasty", ["Labyrinthectomy", "Radical mastoidectomy in every case", "Cochlear nerve section"], "A dry mucosal perforation can be repaired with tympanic membrane grafting.", True),
        q("An attic retraction pocket with trapped keratin that cannot be cleaned in clinic is unsafe because it may", "Progress to cholesteatoma", ["Restore normal ossicular movement", "Prevent all infections", "Close the eustachian tube permanently"], "A non-self-cleansing pocket can evolve into cholesteatoma.", True),
    ]),
    ("Complications of Otitis Media and Mastoiditis", [
        q("The commonest extracranial complication of acute otitis media in children is", "Acute mastoiditis", ["Otosclerosis", "Meniere disease", "Acoustic neuroma"], "Infection can spread from the middle ear to mastoid air cells."),
        q("A postaural swelling pushing the pinna forward and downward after acute otitis media suggests", "Subperiosteal mastoid abscess", ["Preauricular sinus", "Pinna hematoma", "Parotid tumor"], "Mastoid cortex erosion can form a subperiosteal abscess with pinna displacement.", True),
        q("Bezold abscess occurs when mastoid infection tracks through the", "Tip of mastoid into sternocleidomastoid region", ["Zygomatic root", "Petrous apex", "Jugular foramen only"], "Pus can escape through the medial mastoid tip into the neck."),
        q("Gradenigo syndrome consists of otitis media with abducens palsy and", "Deep facial pain from trigeminal involvement", ["Hypoglossal palsy", "Anosmia", "Hemianopia"], "Petrous apicitis may involve CN VI and trigeminal ganglion."),
        q("A child with chronic ear disease develops fever, headache, neck stiffness and photophobia. The feared complication is", "Otogenic meningitis", ["Otosclerosis", "Glue ear", "Cerumen impaction"], "Meningeal signs in ear infection require urgent evaluation for intracranial spread.", True),
        q("Lateral sinus thrombosis from otitis media classically produces", "Picket-fence fever with septicemia", ["Painless bilateral deafness only", "Itching of canal", "Immediate otosclerosis"], "Septic thrombosis can cause swinging pyrexia and systemic toxicity."),
        q("The most common intracranial abscess associated with otitis media is usually in the", "Temporal lobe or cerebellum", ["Pituitary gland", "Frontal lobe only", "Spinal cord"], "Otogenic infection spreads to adjacent temporal lobe and cerebellum."),
        q("A patient with chronic squamosal otitis media develops severe headache, vomiting and papilledema. The concern is", "Intracranial complication with raised intracranial pressure", ["Simple otitis externa", "Presbycusis", "Benign wax plug"], "Raised ICP symptoms in cholesteatoma indicate possible abscess or venous sinus complication.", True),
        q("A patient with chronic foul ear discharge develops new lower motor neuron facial palsy. This is urgent because it may indicate", "Facial canal erosion by cholesteatoma", ["Normal chorda tympani function", "Simple grommet blockage", "Physiologic stapes reflex"], "Squamous disease can expose or inflame the facial nerve.", True),
        q("Luc abscess is a subperiosteal abscess associated with otitis media but without", "Mastoiditis", ["Otorrhea", "Ear pain", "Conductive hearing loss"], "Luc abscess is classically related to spread via deep meatal lymphatics rather than mastoid cortex erosion."),
    ]),
    ("Hearing Loss, Audiology and Rehabilitation", [
        q("Conductive hearing loss is suggested by", "Air-bone gap on pure tone audiometry", ["Equal fall of air and bone thresholds", "Absent caloric response only", "Normal tympanometry in every case"], "An air-bone gap indicates impaired sound conduction with preserved cochlear reserve."),
        q("A flat sensorineural audiogram in an elderly patient with poor speech discrimination suggests", "Presbycusis", ["Wax impaction", "Acute otitis externa", "Central perforation"], "Age-related cochlear degeneration causes bilateral sensorineural loss and speech difficulty."),
        q("A factory worker has bilateral high-frequency sensorineural loss with a 4 kHz notch. The likely cause is", "Noise-induced hearing loss", ["Otosclerosis", "Otitis media with effusion", "Keratosis obturans"], "Chronic noise exposure classically produces a 4 kHz dip.", True),
        q("Otoacoustic emissions test primarily assesses", "Outer hair cell function", ["Stapes tendon reflex only", "Facial nerve taste fibers", "Eustachian tube patency"], "OAEs are generated by active outer hair cell motility."),
        q("Auditory brainstem response is useful for evaluating", "Neural conduction along auditory pathway", ["Wax color", "Pinna cartilage infection", "Nasal airflow"], "ABR measures wave latencies from cochlear nerve to brainstem."),
        q("A newborn fails OAE screening repeatedly but has normal otoscopy. The next useful objective test is", "Auditory brainstem response", ["Fistula test", "Cold caloric test", "Schwabach test only"], "ABR helps confirm and quantify congenital hearing loss objectively.", True),
        q("The main indication for cochlear implantation is", "Severe to profound sensorineural hearing loss with limited hearing-aid benefit", ["Simple wax impaction", "Small dry central perforation", "Acute furuncle"], "Cochlear implants bypass damaged hair cells and stimulate the auditory nerve."),
        q("A patient has mild pure-tone loss but markedly poor speech discrimination in one ear. This pattern suggests", "Retrocochlear pathology", ["Pure conductive loss", "Wax without infection", "Simple tympanosclerosis"], "Neural lesions often impair clarity more than expected from pure tone thresholds.", True),
        q("A patient has unilateral sensorineural loss, tinnitus and absent corneal reflex on the same side. The suspected lesion is", "Vestibular schwannoma", ["Otitis externa", "Myringosclerosis", "Ossicular fixation only"], "CPA tumors can affect CN VIII and adjacent trigeminal fibers.", True),
        q("Masking in audiometry is used to", "Prevent the non-test ear from detecting the test signal", ["Increase wax removal", "Treat tinnitus", "Open the eustachian tube"], "Masking avoids cross-hearing when interaural attenuation is exceeded."),
    ]),
    ("Otosclerosis and Ossicular Disorders", [
        q("Otosclerosis most commonly fixes the", "Stapes footplate", ["Malleus handle", "Incus body", "Tympanic annulus"], "Fenestral otosclerosis typically involves the oval window and stapes footplate."),
        q("The classic audiometric feature of stapedial otosclerosis is", "Conductive loss with Carhart notch near 2 kHz", ["Low-frequency sensorineural loss only", "Flat type B tympanogram always", "No air-bone gap"], "Carhart notch is a depression in bone conduction around 2 kHz."),
        q("A young woman has progressive bilateral conductive hearing loss, normal tympanic membranes and family history. The likely diagnosis is", "Otosclerosis", ["Otitis externa", "Acute mastoiditis", "Meniere disease"], "Progressive conductive loss with a normal drum in a young adult suggests stapes fixation.", True),
        q("Paracusis Willisii means the patient hears better", "In noisy surroundings", ["During sleep", "Only underwater", "After wax syringing"], "Patients with otosclerosis may perceive speech better in noise because others speak louder."),
        q("Schwartze sign is", "Flamingo-pink hue over promontory", ["Blue tympanic membrane", "White attic crust", "Black fungal spores"], "Active otospongiotic focus may be visible as promontory vascular blush."),
        q("A patient develops vertigo and sensorineural drop after stapes surgery. One feared complication is", "Perilymph fistula", ["Cerumen recurrence", "Adenoid hypertrophy", "Diffuse otitis externa"], "Inner ear symptoms after stapes surgery can indicate oval-window leak.", True),
        q("The usual hearing-restoring operation in otosclerosis is", "Stapedotomy with prosthesis", ["Canal wall down mastoidectomy", "Myringotomy alone", "Labyrinthectomy"], "A small fenestra in the stapes footplate with prosthesis improves ossicular transmission."),
        q("Ossicular discontinuity typically shows tympanometry with", "High compliance", ["Absent ear canal volume", "Flat curve in every case", "Negative pressure only"], "A flaccid ossicular chain can produce an Ad-type hypercompliant tracing."),
        q("After head trauma, a patient has persistent conductive hearing loss with intact tympanic membrane and hypercompliant tympanogram. The likely cause is", "Ossicular chain disruption", ["Presbycusis", "Vestibular neuritis", "Serous labyrinthitis"], "Trauma can dislocate the incudostapedial joint while the drum remains intact.", True),
        q("A patient with known otosclerosis later develops a sensorineural component in addition to conductive loss. This is explained by", "Involving the otic capsule and inner ear", ["Filling the external canal with wax", "Producing adenoid obstruction", "Infecting pinna cartilage"], "Retrofenestral disease can add sensorineural loss.", True),
    ]),
    ("Inner Ear Disorders, Vertigo and Tinnitus", [
        q("Meniere disease is pathologically associated with", "Endolymphatic hydrops", ["Stapes footplate fixation", "External canal furuncle", "Attic keratin cyst only"], "Excess endolymph pressure distends the membranous labyrinth."),
        q("The classic triad of Meniere disease is episodic vertigo, tinnitus and", "Fluctuating sensorineural hearing loss", ["Painless otorrhea", "Facial anesthesia", "Central perforation"], "Aural fullness is also common."),
        q("A patient has recurrent hours-long vertigo with roaring tinnitus, aural fullness and fluctuating low-frequency hearing loss. The likely diagnosis is", "Meniere disease", ["BPPV", "Otosclerosis", "Otitis externa"], "The duration and auditory symptoms favor Meniere disease over positional vertigo.", True),
        q("Benign paroxysmal positional vertigo most often involves the", "Posterior semicircular canal", ["Cochlear duct", "Saccule only", "External auditory canal"], "Canaliths most commonly enter the posterior canal."),
        q("The bedside maneuver used to diagnose posterior canal BPPV is", "Dix-Hallpike test", ["Rinne test", "Fistula test only", "Valsalva audiometry"], "Dix-Hallpike provokes positional nystagmus in posterior canal BPPV."),
        q("A woman develops brief spinning vertigo when turning in bed; Dix-Hallpike triggers fatigable torsional nystagmus. Treatment is", "Epley canalith repositioning maneuver", ["Stapedotomy", "Radical mastoidectomy", "Long-term antibiotics"], "Posterior canal BPPV responds to repositioning maneuvers.", True),
        q("Vestibular neuritis differs from labyrinthitis because vestibular neuritis usually has", "Vertigo without hearing loss", ["Profuse otorrhea", "Conductive loss with perforation", "Facial palsy in every case"], "Labyrinthitis affects cochlear and vestibular function; neuritis is predominantly vestibular."),
        q("A patient describes tinnitus exactly synchronous with the pulse. This should raise suspicion of", "Vascular lesion or glomus tumor", ["Simple presbycusis only", "Wax in every case", "BPPV"], "Pulse-synchronous tinnitus is often vascular until evaluated.", True),
        q("A patient with chronic otitis media suddenly develops vertigo, sensorineural loss and spontaneous nystagmus. The complication is", "Labyrinthitis", ["Otosclerosis", "Glue ear", "Pinna perichondritis"], "Inner ear invasion or inflammation from middle ear disease causes labyrinthitis.", True),
        q("Vestibular suppressants are best used in acute vertigo for", "Short-term symptom control", ["Permanent cure of BPPV", "Closing tympanic perforations", "Reversing otosclerosis"], "Prolonged use may delay central compensation."),
    ]),
    ("Facial Nerve, Trauma and Temporal Bone", [
        q("The narrowest segment of the facial canal is the", "Labyrinthine segment", ["Mastoid segment", "Tympanic annulus", "External canal"], "The labyrinthine segment is vulnerable to edema-related compression."),
        q("Bell palsy is classically", "Acute idiopathic lower motor neuron facial paralysis", ["Upper motor neuron forehead-sparing palsy", "Conductive deafness from stapes fixation", "Painless wax impaction"], "Bell palsy affects the peripheral facial nerve and involves the forehead."),
        q("A patient has acute complete left facial weakness including forehead, hyperacusis and loss of taste. The lesion is proximal to the", "Chorda tympani and nerve to stapedius", ["Optic chiasm", "Hypoglossal canal", "Posterior cricoarytenoid"], "Taste loss and hyperacusis localize above chorda tympani and stapedius branches.", True),
        q("Ramsay Hunt syndrome is due to reactivation of", "Varicella-zoster virus in geniculate ganglion", ["Epstein-Barr virus in adenoids", "Candida in external canal", "Staphylococcus in hair follicle"], "Herpes zoster oticus causes painful vesicles with facial palsy."),
        q("Longitudinal temporal bone fracture most commonly causes", "Conductive hearing loss", ["Immediate bilateral blindness", "Isolated anosmia", "Pure aphonia"], "Longitudinal fractures often disrupt the canal or ossicles."),
        q("After road traffic injury, a patient has hemotympanum, conductive loss and otorrhea of clear fluid. The clear fluid suggests", "CSF leak", ["Otomycosis", "Meniere disease", "Exostosis"], "Temporal bone fracture can tear dura and produce CSF otorrhea.", True),
        q("Transverse temporal bone fracture more often causes", "Sensorineural hearing loss and facial nerve injury", ["Only wax impaction", "Adenoid hypertrophy", "Simple otitis externa"], "Transverse fractures cross the otic capsule more often."),
        q("House-Brackmann grading is used for", "Facial nerve function", ["Tympanic membrane perforation size", "Vertigo duration", "Mastoid pneumatization"], "It grades severity of facial paralysis."),
        q("A vesicular eruption in the concha with severe otalgia and ipsilateral facial palsy indicates", "Herpes zoster oticus", ["Furunculosis only", "Serous otitis media", "Otosclerosis"], "Painful ear vesicles plus LMN facial palsy is Ramsay Hunt syndrome.", True),
        q("Immediately after temporal bone trauma, a patient has complete facial paralysis. Compared with delayed palsy, this more strongly suggests", "Nerve transection or severe compression", ["Simple viral edema only", "Wax swelling", "BPPV"], "Immediate complete palsy has higher risk of structural nerve injury.", True),
    ]),
    ("Tumors, Cysts and Miscellaneous Ear Conditions", [
        q("The commonest benign tumor of the cerebellopontine angle is", "Vestibular schwannoma", ["Glomus jugulare", "Squamous cell carcinoma", "Osteoma of canal"], "Vestibular schwannoma commonly arises from the vestibular division of CN VIII."),
        q("The earliest symptom of vestibular schwannoma is commonly", "Unilateral sensorineural hearing loss", ["Purulent otorrhea", "Postaural abscess", "Pinna perichondritis"], "Progressive asymmetric SNHL is typical."),
        q("A patient has asymmetric sensorineural hearing loss, unilateral tinnitus and poor speech discrimination. The investigation of choice is", "MRI internal auditory canals with contrast", ["Plain wax syringing", "Schirmer test", "Barium swallow"], "MRI best detects vestibular schwannoma and other CPA lesions.", True),
        q("Glomus tympanicum often appears otoscopically as", "Reddish pulsatile mass behind tympanic membrane", ["Central dry perforation", "Black fungal debris", "White stapes footplate"], "Paraganglioma is vascular and may cause pulsatile tinnitus."),
        q("Brown sign in glomus tumor refers to", "Blanching of the mass on pneumatic otoscopy", ["Blue scleral band", "Facial spasm after chewing", "Nystagmus on cold water"], "Positive pressure can blanch a vascular middle ear mass."),
        q("A woman has pulsatile tinnitus and a red retrotympanic mass that blanches on pressure. The likely diagnosis is", "Glomus tympanicum", ["Otosclerosis", "Keratosis obturans", "Diffuse otitis externa"], "Pulse-synchronous tinnitus with a red blanching middle ear mass is classic.", True),
        q("Preauricular sinus is usually located near the", "Ascending limb of helix", ["Mastoid tip", "Lobule center", "Posterior canal wall"], "Congenital preauricular pits commonly occur anterior to the helix."),
        q("A repeatedly infected preauricular sinus is treated definitively by", "Complete surgical excision after infection settles", ["Stapedotomy", "Labyrinthectomy", "Grommet insertion"], "Recurrent infection requires removal of the entire tract."),
        q("An elderly man has persistent bleeding ulcer in the external auditory canal with severe pain and granulation. The concern is", "External auditory canal carcinoma", ["Simple wax", "BPPV", "Myringosclerosis"], "Persistent painful bleeding canal lesion needs biopsy to exclude malignancy.", True),
        q("A child has recurrent discharge from a tract near the external ear planned for excision. The surgeon must carefully protect the", "Facial nerve", ["Optic nerve", "Recurrent laryngeal nerve", "Phrenic nerve"], "First cleft tracts can pass close to or through the parotid-facial nerve region.", True),
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
                "id": f"ent-ear-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ENT ear question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ENT Diseases of Ear questions.")


if __name__ == "__main__":
    main()
