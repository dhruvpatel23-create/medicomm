import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ophthalmology"
SUBJECT_TITLE = "Ophthalmology"
CHAPTER = "Diseases of Eye and Ocular Adnexa"
CHAPTER_ORDER = 3
SOURCE_PDF = "opthalmology 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def punctuate(prompt):
    prompt = prompt.strip()
    if prompt[-1] in ".?!:":
        return prompt
    final_clause = re.split(r"[.:]", prompt)[-1].strip()
    starts = ("Which ", "What ", "Why ", "How ", "When ", "Where ")
    if prompt.startswith(starts) or final_clause.startswith(starts):
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
    ("Diseases of Eyelids and Lacrimal Apparatus", [
        q("The commonest organism causing external hordeolum is", "Staphylococcus aureus", ["Pseudomonas aeruginosa", "Adenovirus", "Candida albicans"], "External hordeolum is acute staphylococcal infection of glands of Zeis or Moll."),
        q("A tender red swelling at the lid margin around an eyelash is most likely", "External hordeolum", ["Chalazion", "Xanthelasma", "Dermoid cyst"], "Painful acute lid-margin swelling points to a stye.", True),
        q("Chalazion is a chronic granulomatous inflammation of", "Meibomian gland", ["Lacrimal gland", "Gland of Moll", "Goblet cell"], "Blocked meibomian secretion produces lipogranulomatous inflammation."),
        q("A painless firm nodule in the upper lid persists for weeks without acute redness. What is the likely diagnosis", "Chalazion", ["Acute dacryocystitis", "Preseptal cellulitis", "Herpes zoster ophthalmicus"], "Chalazion is chronic, firm and usually painless.", True),
        q("Recurrent chalazion in an elderly patient should raise suspicion of", "Sebaceous gland carcinoma", ["Retinoblastoma", "Optic neuritis", "Vernal keratoconjunctivitis"], "Sebaceous carcinoma can masquerade as recurrent chalazion."),
        q("Trichiasis means", "Misdirected eyelashes rubbing the globe", ["Drooping upper lid", "Outward lid turning", "Loss of eyelashes"], "Misdirected lashes irritate cornea and conjunctiva."),
        q("An elderly patient has watering and lower lid turned outward. What is the diagnosis", "Ectropion", ["Entropion", "Ptosis", "Lagophthalmos"], "Ectropion causes punctal malposition and epiphora.", True),
        q("Entropion damages cornea mainly due to", "Lash and lid margin rubbing", ["Raised IOP", "Lens opacity", "Vitreous traction"], "Inturned lid causes mechanical keratopathy."),
        q("Congenital nasolacrimal duct obstruction commonly presents with", "Persistent watering since infancy", ["Sudden painful proptosis", "Night blindness", "Coloboma"], "Delayed canalization causes epiphora and discharge in infants."),
        q("A febrile patient has painful swelling below medial canthus with regurgitation of pus on pressure. What is the diagnosis", "Acute dacryocystitis", ["Chalazion", "Pterygium", "Blepharospasm"], "Infected lacrimal sac produces medial canthal swelling and reflux.", True),
    ]),
    ("Conjunctival Disorders", [
        q("Acute bacterial conjunctivitis typically causes", "Mucopurulent discharge", ["Halos with high IOP", "Central scotoma", "Leukocoria"], "Bacterial conjunctivitis commonly presents with sticky mucopurulent discharge."),
        q("A child wakes with both eyelids stuck together and conjunctival congestion. What is likely", "Bacterial conjunctivitis", ["Optic neuritis", "Acute glaucoma", "Retinal detachment"], "Sticky discharge with red eye is typical of bacterial conjunctivitis.", True),
        q("Viral conjunctivitis most often has", "Watery discharge with preauricular lymphadenopathy", ["Severe purulent discharge always", "Painless white pupil", "Raised corneal opacity only"], "Adenoviral disease causes watery red eye and tender preauricular node."),
        q("Follicles on palpebral conjunctiva are classically seen in", "Viral or chlamydial conjunctivitis", ["Acute angle closure", "Cataract", "Retinal vein occlusion"], "Follicular response suggests viral, chlamydial or toxic causes."),
        q("A sexually active adult has chronic follicular conjunctivitis not responding to routine drops. Which infection is likely", "Chlamydial conjunctivitis", ["Fungal endophthalmitis", "Acanthamoeba keratitis", "Trachoma only in childhood"], "Adult inclusion conjunctivitis is caused by Chlamydia trachomatis.", True),
        q("Trachoma is caused by", "Chlamydia trachomatis", ["Neisseria gonorrhoeae", "Moraxella catarrhalis", "HSV-2 only"], "Trachoma is chronic keratoconjunctivitis due to C. trachomatis."),
        q("Arlt line in trachoma refers to", "Linear conjunctival scarring", ["Corneal ring abscess", "Lens opacity", "Optic disc pallor"], "Arlt line is a horizontal scar in upper tarsal conjunctiva."),
        q("A patient from an endemic area has upper tarsal follicles, Herbert pits and pannus. What is the diagnosis", "Trachoma", ["Vernal conjunctivitis", "Episcleritis", "Scleritis"], "Follicles, pannus and limbal pits are classic trachoma findings.", True),
        q("Pterygium is a triangular fibrovascular growth encroaching onto the", "Cornea", ["Lens", "Retina", "Optic disc"], "Pterygium arises from bulbar conjunctiva and grows across the limbus."),
        q("A farmer has a nasal triangular conjunctival growth crossing the limbus. What is it", "Pterygium", ["Pinguecula", "Phlycten", "Chalazion"], "UV exposure is associated with nasal pterygium.", True),
    ]),
    ("Corneal Diseases", [
        q("Corneal ulcer with pain, photophobia and circumcorneal congestion is called", "Keratitis", ["Blepharitis", "Retinitis", "Dacryoadenitis"], "Keratitis involves corneal inflammation and may ulcerate."),
        q("A contact lens wearer develops severe painful red eye with corneal infiltrate. Which organism is important", "Pseudomonas aeruginosa", ["Treponema pallidum", "Mumps virus", "Toxoplasma only"], "Contact lens keratitis is strongly associated with Pseudomonas."),
        q("Dendritic corneal ulcer is typical of", "Herpes simplex keratitis", ["Fungal keratitis", "Trachoma", "Phlyctenular disease"], "HSV epithelial keratitis causes branching dendritic ulcers."),
        q("A patient has recurrent painful red eye with a branching fluorescein-staining epithelial ulcer. What is the diagnosis", "Herpes simplex keratitis", ["Bacterial conjunctivitis", "Scleritis", "Cataract"], "Dendritic ulcer on fluorescein staining is classic HSV keratitis.", True),
        q("Feathery margin corneal ulcer with satellite lesions suggests", "Fungal keratitis", ["Adenoviral conjunctivitis", "Acute glaucoma", "Retinal tear"], "Fungal ulcers often have dry raised slough, feathery edge and satellites."),
        q("A farmer gets vegetative trauma and develops a dry corneal ulcer with feathery margins. What is likely", "Fungal corneal ulcer", ["Vernal catarrh", "Optic neuritis", "Chalazion"], "Vegetative trauma is a classic risk for fungal keratitis.", True),
        q("Keratoconus causes progressive", "Irregular astigmatism", ["Absolute hypermetropia", "Acute uveitis", "Retinal vascular occlusion"], "Corneal ectasia produces irregular myopic astigmatism."),
        q("Munson sign is seen in", "Keratoconus", ["Trachoma", "Endophthalmitis", "Choroiditis"], "Advanced keratoconus indents the lower lid on downgaze."),
        q("A teenager has progressive irregular astigmatism and scissoring reflex on retinoscopy. What is likely", "Keratoconus", ["Presbyopia", "Acute conjunctivitis", "Papilloedema"], "Scissoring retinoscopic reflex suggests keratoconus.", True),
        q("Corneal oedema after endothelial failure produces", "Loss of transparency", ["Improved vision", "Optic disc cupping", "Macular hole"], "Endothelial pump failure hydrates stroma and clouds the cornea.", True),
    ]),
    ("Sclera, Episclera and Uveal Tract", [
        q("Episcleritis is usually", "Benign and self-limiting", ["Always vision-threatening", "A lens opacity", "A retinal detachment"], "Episcleritis is superficial inflammation and often mild."),
        q("Scleritis is important because it is painful and associated with", "Systemic autoimmune disease", ["Simple refractive error only", "Congenital cataract only", "Meibomian cyst only"], "Scleritis is deeper, painful and may threaten vision."),
        q("A patient has boring ocular pain worse at night with violaceous scleral congestion. What is likely", "Scleritis", ["Episcleritis", "Pinguecula", "Chalazion"], "Deep severe pain and violaceous hue suggest scleritis.", True),
        q("Anterior uveitis classically causes", "Pain, photophobia and ciliary congestion", ["Painless leukocoria", "Sticky lid margins only", "Sudden lid swelling only"], "Iritis causes photophobia, pain and circumcorneal congestion."),
        q("Keratic precipitates are inflammatory deposits on the", "Corneal endothelium", ["Lens nucleus", "Optic disc", "Eyelid skin"], "Cells adhere to the posterior corneal surface in uveitis."),
        q("A patient has painful red eye, small irregular pupil and cells in anterior chamber. What is the diagnosis", "Anterior uveitis", ["Bacterial conjunctivitis", "Retinal detachment", "Ptosis"], "Cells, flare and miosis are typical of iridocyclitis.", True),
        q("Posterior synechiae means adhesion between iris and", "Anterior lens capsule", ["Corneal epithelium", "Retina", "Optic nerve"], "Inflamed iris may stick to the lens surface."),
        q("Cycloplegics in anterior uveitis are used to relieve pain and prevent", "Posterior synechiae", ["Lens subluxation", "Retinal tears", "Lid ectropion"], "Cycloplegics rest ciliary muscle and keep pupil mobile."),
        q("A uveitis patient develops a fixed irregular pupil after delayed treatment. What caused it", "Posterior synechiae", ["Ectropion", "Corneal abrasion", "Vitreous detachment"], "Iris-lens adhesions distort the pupil.", True),
        q("Hypopyon is accumulation of inflammatory cells in the", "Anterior chamber", ["Vitreous base only", "Subretinal space", "Lacrimal sac"], "Layered leukocytes in anterior chamber form hypopyon.", True),
    ]),
    ("Lens and Cataract", [
        q("Cataract is opacity of the", "Crystalline lens", ["Corneal epithelium", "Retina", "Optic nerve"], "Any opacity of the lens or its capsule is cataract."),
        q("The commonest type of senile cataract is", "Cortical or nuclear age-related cataract", ["Congenital coloboma", "Traumatic iridodialysis", "Optic neuritis"], "Age-related cataract commonly affects nucleus and cortex."),
        q("A 65-year-old has painless progressive diminution of vision with normal IOP and lens opacity. What is likely", "Senile cataract", ["Acute glaucoma", "Keratitis", "Endophthalmitis"], "Painless gradual visual loss with lens opacity is cataract.", True),
        q("Posterior subcapsular cataract commonly causes difficulty in", "Bright light and near work", ["Only night driving improvement", "Ear pain", "Lid swelling"], "PSC lies near the nodal point and affects glare and near vision."),
        q("Steroid use is associated with", "Posterior subcapsular cataract", ["Blue dot cataract only", "Keratoconus only", "Trachoma"], "Long-term corticosteroids predispose to PSC."),
        q("A young patient on long-term systemic steroids develops glare and near visual difficulty. Which cataract is likely", "Posterior subcapsular cataract", ["Nuclear sclerosis", "Morgagnian cataract", "Lamellar cataract only"], "Steroid-related PSC produces disproportionate glare.", True),
        q("Phacoemulsification removes cataract using", "Ultrasound energy", ["Laser photocoagulation only", "Cryotherapy only", "Radiotherapy"], "Phaco fragments the lens nucleus ultrasonically."),
        q("Pseudophakia means", "Intraocular lens implanted eye", ["Lens absent eye", "Corneal grafted eye", "Retina detached eye"], "After cataract extraction with IOL, the eye is pseudophakic."),
        q("Sudden painful loss of vision after cataract surgery with hypopyon suggests", "Endophthalmitis", ["Normal postoperative reaction", "Presbyopia", "Pinguecula"], "Postoperative endophthalmitis is an ocular emergency.", True),
        q("Congenital cataract must be treated early to prevent", "Deprivation amblyopia", ["Presbyopia", "Ectropion", "Pterygium"], "Clear retinal image is needed during visual development.", True),
    ]),
    ("Glaucoma", [
        q("Glaucoma is characterized by optic neuropathy with", "Progressive visual field loss", ["Only conjunctival discharge", "Only lens opacity", "Only lid swelling"], "Glaucoma damages optic nerve and visual field."),
        q("Primary open-angle glaucoma is usually", "Chronic and initially asymptomatic", ["Always painful acutely", "Always congenital", "Only infectious"], "Open-angle glaucoma often remains silent until field loss occurs."),
        q("A 58-year-old has raised IOP, open angles and optic disc cupping. What is likely", "Primary open-angle glaucoma", ["Acute conjunctivitis", "Senile cataract only", "Keratoconus"], "Open angle with cupping and raised IOP suggests POAG.", True),
        q("The earliest visual field defect in glaucoma may be", "Paracentral scotoma", ["Complete hemianopia always", "Central red-green loss only", "Normal blind spot loss only"], "Early glaucomatous defects include paracentral and nasal step changes."),
        q("Acute angle-closure glaucoma presents with", "Painful red eye with halos and vomiting", ["Painless gradual opacity only", "Sticky discharge only", "Itching only"], "Sudden angle closure causes high IOP and systemic symptoms."),
        q("A hypermetropic elderly woman has severe ocular pain, mid-dilated fixed pupil and cloudy cornea. What is the diagnosis", "Acute angle-closure glaucoma", ["Viral conjunctivitis", "Optic neuritis", "Chalazion"], "This is the classic acute angle-closure presentation.", True),
        q("Definitive prevention of recurrent primary angle closure is", "Laser peripheral iridotomy", ["Myringotomy", "Tarsorrhaphy", "Dacryocystectomy"], "Iridotomy bypasses pupillary block."),
        q("Cup-disc ratio is assessed to evaluate", "Glaucomatous optic nerve damage", ["Corneal ulcer depth", "Lens thickness", "Tear film"], "Progressive cupping reflects optic nerve fibre loss."),
        q("A glaucoma patient has beta-blocker eye drops and develops bronchospasm. Which drug class caused it", "Topical beta blocker", ["Prostaglandin analogue", "Carbonic anhydrase inhibitor", "Cycloplegic"], "Timolol can be systemically absorbed and worsen asthma.", True),
        q("Congenital glaucoma commonly causes", "Buphthalmos and epiphora", ["Small painless eye", "Mature cataract only", "Ptosis only"], "High IOP stretches the infant eye, causing enlarged cornea and watering.", True),
    ]),
    ("Retinal and Vitreous Disorders", [
        q("Diabetic retinopathy is primarily a disease of retinal", "Microvasculature", ["Lens capsule", "Lacrimal gland", "Extraocular muscles"], "Chronic hyperglycaemia damages retinal capillaries."),
        q("Hard exudates in diabetic retinopathy are due to", "Lipid leakage", ["Melanin loss", "Lens protein denaturation", "Vitreous liquefaction only"], "Leaky microaneurysms allow lipid-rich exudation."),
        q("A diabetic patient has new vessels on disc and vitreous haemorrhage. What stage is this", "Proliferative diabetic retinopathy", ["Mild cataract", "Dry eye", "Simple conjunctivitis"], "Neovascularization defines proliferative disease.", True),
        q("Hypertensive retinopathy may show", "Arteriolar narrowing and AV crossing changes", ["Dendritic ulcer", "Posterior synechiae", "Chalazion"], "Long-standing hypertension alters retinal arterioles."),
        q("Central retinal artery occlusion classically shows", "Cherry-red spot", ["Arlt line", "Munson sign", "Kayser-Fleischer ring only"], "Retinal whitening with foveal choroidal show produces a cherry-red spot."),
        q("A patient has sudden painless monocular vision loss with pale retina and cherry-red spot. What is likely", "Central retinal artery occlusion", ["Acute conjunctivitis", "Chalazion", "Presbyopia"], "CRAO causes acute retinal ischemia and severe visual loss.", True),
        q("Central retinal vein occlusion has fundus appearance described as", "Blood and thunder", ["Ground glass", "Salt and pepper only", "Fish egg"], "Diffuse retinal haemorrhages and venous engorgement give this appearance."),
        q("Retinal detachment presents classically with flashes, floaters and", "Curtain-like field defect", ["Itching", "Mucopurulent discharge", "Lid crusting only"], "Detached retina causes progressive field loss."),
        q("A high myope reports flashes and a shadow descending over vision. What is the concern", "Rhegmatogenous retinal detachment", ["Vernal conjunctivitis", "Blepharitis", "Presbyopia"], "High myopia predisposes to retinal breaks and detachment.", True),
        q("Age-related macular degeneration primarily affects", "Central vision", ["Peripheral vestibular function", "Tear drainage", "Eye movements only"], "Macular disease impairs reading and central visual tasks.", True),
    ]),
    ("Optic Nerve and Neuro-Ophthalmic Disorders", [
        q("Optic neuritis commonly causes painful eye movements and", "Subacute visual loss", ["Sticky discharge", "Lens opacity", "Lid abscess"], "Inflammatory optic neuropathy causes visual loss and pain on eye movement."),
        q("A young adult has painful monocular visual loss and reduced colour vision. What is likely", "Optic neuritis", ["Chalazion", "Acute dacryocystitis", "Pterygium"], "Painful vision loss with dyschromatopsia suggests optic neuritis.", True),
        q("Papilloedema is optic disc swelling due to", "Raised intracranial pressure", ["Lens hydration", "Corneal abrasion", "Meibomian blockage"], "Raised ICP causes bilateral disc oedema through axoplasmic flow stasis."),
        q("Papilloedema usually preserves early", "Visual acuity", ["Consciousness always", "Corneal sensation only", "Pupil size only"], "Early papilloedema may have enlarged blind spot with preserved central acuity."),
        q("A patient with headache and vomiting has bilateral blurred disc margins but normal central vision. What is likely", "Papilloedema", ["Optic atrophy", "Corneal ulcer", "Retinitis pigmentosa"], "Raised ICP commonly presents with bilateral disc oedema.", True),
        q("Relative afferent pupillary defect indicates damage to", "Optic nerve or severe retinal pathway", ["Facial nerve", "Ciliary muscle only", "Orbicularis oculi"], "RAPD reflects asymmetric afferent visual pathway dysfunction."),
        q("Bitemporal hemianopia is classically caused by lesion at the", "Optic chiasm", ["Optic disc", "Occipital pole only", "Ciliary ganglion"], "Chiasmal compression affects crossing nasal retinal fibres."),
        q("A pituitary tumour patient loses temporal fields in both eyes. Which site is compressed", "Optic chiasm", ["Lateral geniculate body only", "Facial nerve", "Corneal endothelium"], "Pituitary masses commonly compress the chiasm from below.", True),
        q("Optic atrophy appears as", "Pale optic disc", ["Red conjunctiva", "Lens opacity", "Corneal vascularization only"], "Loss of optic nerve fibres produces disc pallor."),
        q("Third nerve palsy with pupil involvement raises concern for", "Posterior communicating artery aneurysm", ["Simple dry eye", "Chalazion", "Vernal conjunctivitis"], "A painful pupil-involving third nerve palsy may indicate aneurysmal compression.", True),
    ]),
    ("Orbital Disorders and Ocular Trauma", [
        q("Orbital cellulitis differs from preseptal cellulitis by presence of", "Painful eye movements or proptosis", ["Lid redness only", "Mild itching only", "Watering only"], "Postseptal infection affects orbit and may restrict movements."),
        q("A child with sinusitis has fever, proptosis and painful restricted eye movements. What is the diagnosis", "Orbital cellulitis", ["Preseptal cellulitis", "Chalazion", "Pinguecula"], "Sinus-related orbital cellulitis can threaten vision and brain.", True),
        q("Blow-out fracture commonly traps the", "Inferior rectus muscle", ["Superior oblique tendon", "Levator palpebrae", "Orbicularis oculi"], "Orbital floor fracture may entrap inferior rectus."),
        q("Diplopia on upgaze after blunt orbital trauma suggests", "Inferior rectus entrapment", ["Optic neuritis", "Acute conjunctivitis", "Dacryocystitis"], "Entrapment limits elevation and causes diplopia.", True),
        q("Chemical eye injury should first be treated by", "Immediate copious irrigation", ["Steroid drops before washing", "Eye patching only", "Delayed referral without washing"], "Irrigation is the first and most time-critical step."),
        q("A worker splashes alkali into the eye. What is the immediate management", "Copious irrigation", ["Wait for pH report", "Apply pressure patch only", "Use miotic first"], "Alkali penetrates rapidly, so irrigation begins immediately.", True),
        q("Open globe injury should be protected with", "Rigid eye shield", ["Pressure pad", "Massage", "Warm compress"], "Pressure can extrude intraocular contents; rigid shield protects the globe."),
        q("A patient has peaked pupil after penetrating injury. What does this suggest", "Open globe injury", ["Simple conjunctivitis", "Presbyopia", "Chalazion"], "Peaked pupil points toward iris prolapse through a wound.", True),
        q("Retrobulbar haemorrhage can cause acute proptosis with", "Raised orbital pressure and vision threat", ["Improved vision", "Lens subluxation only", "Pterygium"], "Orbital compartment syndrome can rapidly damage optic nerve."),
        q("Sympathetic ophthalmia follows penetrating trauma and is", "Bilateral granulomatous uveitis", ["Unilateral chalazion", "Corneal abrasion only", "Acute conjunctivitis"], "Autoimmune reaction after trauma may affect the fellow eye."),
    ]),
    ("Ocular Infections, Inflammation and Emergencies", [
        q("Endophthalmitis is inflammation involving", "Intraocular cavities", ["Only eyelid skin", "Only lacrimal sac", "Only conjunctival sac"], "Endophthalmitis is severe intraocular infection or inflammation."),
        q("Painful severe visual loss with hypopyon after intraocular surgery suggests", "Postoperative endophthalmitis", ["Normal healing", "Presbyopia", "Pinguecula"], "Postoperative endophthalmitis is an emergency.", True),
        q("Panophthalmitis involves inflammation of", "All coats of eyeball and surrounding tissues", ["Only lens nucleus", "Only optic disc", "Only eyelid margin"], "Panophthalmitis is more extensive than endophthalmitis."),
        q("Herpes zoster ophthalmicus involves the", "Ophthalmic division of trigeminal nerve", ["Facial motor nerve", "Abducens nerve", "Mandibular division only"], "V1 involvement causes forehead, lid and ocular disease."),
        q("A patient has vesicles on forehead and tip of nose with red eye. What sign predicts ocular involvement", "Hutchinson sign", ["Munson sign", "Arlt line", "Berlin oedema"], "Nasociliary involvement causes vesicles on nose tip and higher ocular risk.", True),
        q("Phlyctenular keratoconjunctivitis is a hypersensitivity reaction commonly associated with", "Tuberculosis or staphylococcal antigen", ["Aphakia", "Retinal detachment", "Presbyopia"], "It is an immune response to microbial proteins."),
        q("Ophthalmia neonatorum refers to conjunctivitis occurring in", "First month of life", ["Adolescence only", "After cataract surgery only", "Old age only"], "Neonatal conjunctivitis occurs within 28 days of birth."),
        q("A neonate develops severe purulent conjunctivitis 2 days after birth. Which organism is feared", "Neisseria gonorrhoeae", ["Adenovirus only", "Toxoplasma gondii", "Aspergillus"], "Gonococcal conjunctivitis appears early and can rapidly damage cornea.", True),
        q("Red eye with severe pain, reduced vision and corneal haze should not be treated as simple", "Conjunctivitis", ["Glaucoma emergency", "Keratitis", "Uveitis"], "Pain and reduced vision are warning signs needing urgent evaluation."),
        q("A contact lens user with red eye and reduced vision should be evaluated urgently for", "Microbial keratitis", ["Simple presbyopia", "Physiological blind spot", "Benign pinguecula only"], "Contact lens wear increases risk of sight-threatening keratitis.", True),
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
                "id": f"ophth-eye-adnexa-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ophthalmology eye adnexa question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 ophthalmology eye and ocular adnexa questions.")


if __name__ == "__main__":
    main()
