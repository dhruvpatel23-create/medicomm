import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ophthalmology"
SUBJECT_TITLE = "Ophthalmology"
SOURCE_PDF = "opthalmology 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def punctuate(prompt):
    prompt = prompt.strip()
    if prompt[-1] in ".?!:":
        return prompt
    final_clause = re.split(r"[.:]", prompt)[-1].strip()
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


CHAPTERS = [
    ("Systemic and Community Ophthalmology", 5, [
        ("Systemic Ophthalmology", [
            q("Diabetes mellitus most commonly affects the eye by causing", "Diabetic retinopathy", ["Congenital cataract only", "Trachoma", "Ectropion"], "Chronic hyperglycaemia damages retinal microvasculature and produces diabetic retinopathy."),
            q("A diabetic patient has microaneurysms, dot haemorrhages and hard exudates without new vessels. The stage is", "Non-proliferative diabetic retinopathy", ["Proliferative diabetic retinopathy", "Retinoblastoma", "Optic neuritis"], "Microaneurysms, haemorrhages and exudates without neovascularization indicate NPDR.", True),
            q("New vessels on the disc in diabetic retinopathy indicate", "Proliferative diabetic retinopathy", ["Background retinopathy only", "Hypertensive choroidopathy", "Simple cataract"], "Neovascularization defines proliferative diabetic retinopathy."),
            q("A diabetic patient presents with sudden floaters and severe visual loss from vitreous haemorrhage. The likely underlying lesion is", "Retinal neovascularization", ["Posterior subcapsular cataract alone", "Conjunctival follicles", "Acute dacryocystitis"], "Fragile new vessels in PDR bleed into the vitreous.", True),
            q("Hypertension produces retinal arteriolar changes such as", "Arteriolar narrowing and AV nicking", ["Dendritic ulcer", "Munson sign", "Kayser-Fleischer ring"], "Chronic hypertension causes arteriolar narrowing, sclerosis and arteriovenous crossing changes."),
            q("A patient with severe hypertension has disc oedema, flame haemorrhages and cotton wool spots. This suggests", "Malignant hypertensive retinopathy", ["Simple refractive error", "Trachoma", "Vernal conjunctivitis"], "Papilloedema with retinopathy is a severe hypertensive emergency sign.", True),
            q("Cotton wool spots represent", "Retinal nerve fibre layer microinfarcts", ["Lipid-filled chalazia", "Lens opacities", "Corneal scars"], "They are fluffy white lesions caused by focal retinal ischemia."),
            q("Sickle cell disease can cause retinal", "Peripheral neovascularization", ["Nasolacrimal duct obstruction only", "Pterygium always", "Congenital ptosis"], "Retinal ischemia in sickle cell disease can produce sea-fan neovascularization."),
            q("A young patient with sickle cell disease has sea-fan peripheral new vessels. The ocular diagnosis is", "Proliferative sickle retinopathy", ["Vernal keratoconjunctivitis", "Senile cataract", "Acute angle closure"], "Sea-fan neovascularization is classic for proliferative sickle retinopathy.", True),
            q("Leukaemia may involve the fundus with", "Retinal haemorrhages and infiltrates", ["Only corneal arcus", "Only chalazion", "Only trichiasis"], "Anaemia, thrombocytopenia and leukemic infiltration can affect retina."),
            q("Rheumatoid arthritis is classically associated with", "Scleritis and keratoconjunctivitis sicca", ["Retinoblastoma", "Congenital glaucoma", "Pterygium only"], "Autoimmune ocular disease in RA includes dry eye, episcleritis and scleritis."),
            q("A patient with rheumatoid arthritis has deep boring eye pain and violaceous redness. The likely diagnosis is", "Scleritis", ["Simple conjunctivitis", "Chalazion", "Presbyopia"], "Scleritis causes severe deep pain and is linked to systemic autoimmune disease.", True),
            q("Ankylosing spondylitis commonly causes recurrent", "Acute anterior uveitis", ["Orbital blow-out fracture", "Trachoma", "Aphakia"], "HLA-B27 spondyloarthropathy is a classic cause of recurrent acute anterior uveitis."),
            q("A young man with back stiffness develops painful photophobic red eye with cells in anterior chamber. Which systemic association fits best", "HLA-B27 spondyloarthropathy", ["Scurvy", "Phenylketonuria", "Marfan lens opacity only"], "Acute anterior uveitis is strongly associated with HLA-B27 disease.", True),
            q("Sarcoidosis can cause ocular", "Granulomatous uveitis", ["Only external hordeolum", "Only refractive error", "Only pinguecula"], "Sarcoidosis commonly presents with granulomatous anterior or posterior uveitis."),
            q("Behcet disease classically causes recurrent oral ulcers with", "Uveitis and retinal vasculitis", ["Congenital cataract", "Simple blepharitis", "Dacryocystitis only"], "Behcet disease causes relapsing occlusive retinal vasculitis and uveitis."),
            q("A patient with recurrent oral and genital ulcers has hypopyon uveitis. The likely systemic disease is", "Behcet disease", ["Diabetes mellitus only", "Albinism", "Myasthenia gravis"], "Hypopyon uveitis with mucosal ulcers is a high-yield Behcet presentation.", True),
            q("Marfan syndrome is associated with lens subluxation typically", "Superotemporal", ["Inferonasal", "Directly posterior always", "Into anterior chamber always"], "Ectopia lentis in Marfan syndrome is classically upward and outward."),
            q("Wilson disease produces", "Kayser-Fleischer ring", ["Arlt line", "Munson sign", "Cherry-red spot always"], "Copper deposition in Descemet membrane forms the Kayser-Fleischer ring."),
            q("A child with developmental delay has bilateral inferonasal lens subluxation. Which metabolic disorder is likely", "Homocystinuria", ["Wilson disease", "Alport syndrome", "Diabetic retinopathy"], "Homocystinuria usually causes downward and inward lens subluxation.", True),
        ]),
        ("Community Opthalmology", [
            q("The leading cause of avoidable blindness in many Indian community surveys is", "Cataract", ["Optic neuritis", "Colour blindness", "Simple conjunctivitis"], "Age-related cataract remains a major avoidable cause of blindness."),
            q("In a village eye camp, an elderly patient has painless white lens opacity and poor vision. The priority intervention is", "Cataract surgery referral", ["Long-term antibiotic drops", "Eye exercises only", "No action"], "Cataract blindness is reversible by surgery and should be identified in screening camps.", True),
            q("Visual acuity screening in school children mainly detects", "Refractive errors", ["Retinoblastoma in adults", "Orbital cellulitis only", "Endophthalmitis only"], "Uncorrected refractive error is common and easily detected by acuity testing."),
            q("A 10-year-old school child improves from 6/18 to 6/6 with pinhole. The likely community eye problem is", "Uncorrected refractive error", ["Optic atrophy", "Retinal detachment", "Corneal perforation"], "Pinhole improvement suggests correctable refractive blur.", True),
            q("Vitamin A prophylaxis prevents nutritional blindness mainly by preventing", "Xerophthalmia", ["Trachoma scarring only", "Glaucoma", "Diabetic macular edema"], "Vitamin A deficiency causes night blindness, xerosis and keratomalacia."),
            q("A malnourished child has night blindness and Bitot spots. The community diagnosis is", "Vitamin A deficiency", ["Congenital cataract", "Retinopathy of prematurity", "Acute angle closure"], "Night blindness and Bitot spots are classic xerophthalmia findings.", True),
            q("Bitot spots are seen on the", "Conjunctiva", ["Lens nucleus", "Optic disc", "Vitreous"], "Bitot spots are foamy keratinized conjunctival patches."),
            q("SAFE strategy is used for control of", "Trachoma", ["Diabetic retinopathy", "Retinoblastoma", "Chemical injury"], "SAFE stands for surgery, antibiotics, facial cleanliness and environmental improvement."),
            q("A community has endemic trachoma with trichiasis. The surgical component of SAFE is aimed at preventing", "Corneal blindness from inturned lashes", ["Lens opacity", "Macular edema", "Optic neuritis"], "Correcting trichiasis prevents lashes from abrading and scarring the cornea.", True),
            q("Trachoma is transmitted mainly by contact with infected ocular or nasal secretions and", "Flies and fomites", ["Mosquito bite only", "Dog bite", "Waterborne helminths only"], "Poor hygiene, crowding, flies and contaminated fomites spread trachoma."),
            q("NPCBVI in India focuses on prevention and control of", "Blindness and visual impairment", ["Only tuberculosis", "Only maternal mortality", "Only dental caries"], "The national programme targets avoidable blindness and visual impairment."),
            q("A district programme plans cataract outreach. The best indicator of service output is", "Cataract surgical rate", ["Birth rate", "Infant mortality rate only", "Body mass index"], "Cataract surgical rate measures cataract operations performed per million population per year.", True),
            q("Blindness for programme purposes is commonly defined using best corrected visual acuity in the better eye below", "3/60", ["6/6", "6/9", "6/18 only"], "Operational blindness definitions use severe reduction of vision in the better eye."),
            q("Low vision refers to visual impairment that", "Persists despite treatment or standard refractive correction", ["Always improves to 6/6 with pinhole", "Means no perception of light only", "Is only night blindness"], "Low vision services help patients with residual usable vision."),
            q("A patient cannot be improved surgically but can read large print with magnifiers. The appropriate service is", "Low vision rehabilitation", ["Emergency evisceration", "Only topical steroid", "No visual aid"], "Low vision care maximizes remaining vision with optical and non-optical aids.", True),
            q("Vision 2020 emphasized elimination of", "Avoidable blindness", ["All refractive errors permanently", "All genetic diseases", "All ocular trauma"], "VISION 2020 was a global initiative against avoidable blindness."),
            q("Retinopathy of prematurity screening is targeted at", "Preterm and low birth weight infants", ["All elderly cataract patients", "Only hypertensive adults", "All school teachers"], "ROP occurs in premature infants with immature retinal vasculature."),
            q("A premature infant discharged from NICU is referred for timely fundus screening. The condition being prevented is", "Retinopathy of prematurity blindness", ["Trachoma", "Senile cataract", "Presbyopia"], "Early screening detects treatable ROP before retinal detachment.", True),
            q("Primary eye care includes early recognition and referral of", "Vision-threatening red eye", ["Only cosmetic lid wrinkles", "Only normal presbyopia", "Only spectacle frame choice"], "Primary care must identify emergencies such as keratitis, acute glaucoma and trauma."),
            q("An eye camp finds many adults with undiagnosed glaucoma risk. Community screening should include referral for", "IOP, optic disc and visual field evaluation", ["Only ear examination", "Only dental scaling", "Only colour of spectacles"], "Glaucoma screening requires assessment beyond simple visual acuity when risk is suspected.", True),
        ]),
    ]),
    ("Practical Ophthalmology", 6, [
        ("Practical Ophthalmology", [
            q("Distant visual acuity is usually tested with", "Snellen chart", ["Ishihara chart", "Amsler grid only", "Schiotz tonometer"], "Snellen chart records distance acuity as a fraction."),
            q("A patient reads the 6/24 line at 6 metres. The visual acuity is recorded as", "6/24", ["24/6", "6/6", "Counting fingers only"], "The numerator is testing distance and the denominator is the smallest line read.", True),
            q("Pinhole testing improves vision mainly in", "Refractive error", ["Dense optic atrophy always", "Endophthalmitis", "Retinal artery occlusion"], "Pinhole reduces blur circles and suggests optical focusing error."),
            q("A patient improves from 6/18 to 6/6 with pinhole. The next practical step is", "Refraction", ["Evisceration", "Urgent vitrectomy", "No correction possible"], "Pinhole improvement indicates that refraction may restore acuity.", True),
            q("Near vision is commonly tested with", "Jaeger chart", ["Maddox rod", "Schiotz tonometer", "Placido disc only"], "Jaeger or near vision charts assess reading vision at near distance."),
            q("Ishihara plates are used to test", "Colour vision", ["Intraocular pressure", "Lacrimal drainage", "Corneal sensation"], "Ishihara pseudoisochromatic plates screen red-green colour defects."),
            q("A young man cannot read numbers on Ishihara plates but visual acuity is normal. The likely defect is", "Red-green colour vision deficiency", ["Acute glaucoma", "Cataract", "Dacryocystitis"], "Congenital red-green defects are often detected by Ishihara testing.", True),
            q("Confrontation test is a bedside method for assessing", "Visual fields", ["Lens power", "Tear breakup time", "Corneal thickness only"], "Confrontation compares the patient's field with the examiner's field."),
            q("A patient with pituitary tumour has loss of temporal fields. Which practical test can detect this at bedside", "Confrontation visual field testing", ["Syringing", "Fluorescein staining only", "Schirmer test"], "Confrontation can pick up gross bitemporal field loss.", True),
            q("Amsler grid is used mainly to assess", "Macular function", ["Peripheral retina only", "Nasolacrimal duct patency", "Ocular motility only"], "Distortion or missing grid lines suggest macular disease."),
            q("Direct ophthalmoscopy gives a magnified view of the", "Fundus", ["Nasolacrimal sac", "Corneal endothelium only", "Eyelid margin only"], "Direct ophthalmoscope is used for optic disc, vessels, macula and retina."),
            q("A diabetic patient needs retinal screening. The most relevant practical examination is", "Fundus examination", ["Schirmer test only", "Lid eversion only", "Maddox rod only"], "Diabetic retinopathy is diagnosed by examining the retina.", True),
            q("The normal optic disc cup-disc ratio is roughly less than", "0.3 to 0.4", ["0.9 always", "1.0 always", "No cup ever"], "A large or asymmetric cup-disc ratio raises suspicion for glaucoma."),
            q("Slit-lamp biomicroscopy is used to examine", "Anterior segment in detail", ["Only visual fields", "Only systemic blood pressure", "Only hearing"], "The slit lamp evaluates lids, conjunctiva, cornea, anterior chamber, iris and lens."),
            q("Cells and flare in anterior chamber are best seen using", "Slit-lamp examination", ["Snellen chart", "Ishihara plates", "Amsler grid"], "A narrow slit beam demonstrates inflammatory cells and protein flare."),
            q("A patient with painful photophobic red eye needs confirmation of anterior uveitis. Which examination is best", "Slit-lamp examination", ["Jaeger chart only", "Colour vision chart", "Syringing"], "Slit lamp shows ciliary congestion, keratic precipitates, cells and flare.", True),
            q("Fluorescein staining helps identify", "Corneal epithelial defect", ["Lens opacity only", "Optic disc pallor only", "Extraocular muscle palsy only"], "Fluorescein highlights abrasions, ulcers and epithelial defects."),
            q("A contact lens wearer has severe pain and fluorescein-positive corneal defect. The urgent diagnosis to consider is", "Microbial keratitis", ["Presbyopia", "Simple cataract", "Ectropion only"], "Contact lens-associated epithelial defect with pain can represent infectious keratitis.", True),
            q("Seidel test detects", "Aqueous leakage from corneal wound", ["Colour blindness", "Retinal detachment", "Dry eye only"], "Dilution of fluorescein by leaking aqueous indicates a full-thickness wound."),
            q("A trauma patient has streaming of fluorescein from a corneal laceration. The test is", "Positive Seidel test", ["Positive Schirmer test", "Positive Amsler grid", "Positive Hirschberg test"], "A positive Seidel test indicates open globe leakage and needs urgent protection/referral.", True),
            q("Tonometry measures", "Intraocular pressure", ["Axial length only", "Colour vision", "Retinal thickness only"], "Tonometry estimates IOP for glaucoma diagnosis and monitoring."),
            q("Goldmann applanation tonometry is based on flattening a fixed area of", "Cornea", ["Lens", "Retina", "Sclera behind equator only"], "Applanation tonometry estimates pressure from the force needed to flatten the cornea."),
            q("A patient has severe ocular pain, halos and cloudy cornea. Which practical measurement is urgent", "Intraocular pressure", ["Near vision only", "Colour plates only", "Lacrimal syringing"], "Acute angle closure is confirmed by raised IOP and needs urgent treatment.", True),
            q("Schiotz tonometer is an indentation tonometer affected by", "Scleral rigidity", ["Colour contrast", "Tear lysozyme only", "Lens pigmentation"], "Indentation tonometry readings vary with ocular rigidity."),
            q("Gonioscopy is used to evaluate", "Anterior chamber angle", ["Posterior capsule opacity only", "Colour vision", "Lacrimal sac"], "Gonioscopy distinguishes open from narrow or closed angles."),
            q("A glaucoma suspect has shallow anterior chamber. Which test confirms angle status", "Gonioscopy", ["Schirmer test", "Amsler grid", "Ishihara plates"], "Gonioscopy directly visualizes the drainage angle.", True),
            q("Syringing of lacrimal passages assesses", "Nasolacrimal drainage patency", ["Retinal circulation", "Optic nerve conduction", "Lens opacity"], "Fluid passage into nose indicates patency; reflux suggests obstruction site."),
            q("A patient has watering with regurgitation from opposite punctum during syringing. This suggests", "Nasolacrimal duct obstruction", ["Optic neuritis", "Keratoconus", "Macular hole"], "Regurgitation through the other punctum indicates distal lacrimal drainage obstruction.", True),
            q("Schirmer test measures", "Tear secretion", ["Aqueous outflow", "Retinal acuity", "Lens thickness"], "Filter paper wetting quantifies basal and reflex tear production."),
            q("A patient has burning eyes and normal Schirmer wetting but tear film breaks up rapidly after blinking. The test evaluates", "Tear film stability", ["Colour vision", "Visual field", "Cup-disc ratio only"], "Short TBUT suggests evaporative dry eye or unstable tear film.", True),
            q("Keratometry measures", "Corneal curvature", ["Retinal thickness", "Pupil reaction only", "Lacrimal patency"], "Keratometry is used for astigmatism assessment and IOL calculation."),
            q("A cataract patient needs IOL power calculation. Which measurements are essential", "Keratometry and axial length", ["Ishihara plates and syringing", "Schirmer test only", "Visual field only"], "Biometry combines corneal power and axial length to calculate IOL power.", True),
            q("A-scan ultrasonography measures", "Axial length of eyeball", ["Colour vision", "Tear production", "Anterior chamber cells only"], "A-scan is used in ocular biometry."),
            q("B-scan ultrasonography is especially useful when", "Fundus view is obscured by opaque media", ["Cornea is perfectly clear always", "Only refraction is needed", "Tear secretion is low"], "B-scan evaluates posterior segment behind cataract, vitreous haemorrhage or corneal opacity."),
            q("A patient has dense vitreous haemorrhage and no fundus view. Which investigation assesses retinal detachment", "B-scan ultrasonography", ["Ishihara chart", "Schirmer strip", "Syringing"], "B-scan can detect retinal detachment when media opacity blocks ophthalmoscopy.", True),
            q("Retinoscopy is an objective method for estimating", "Refractive error", ["Lacrimal drainage", "Retinal vessels only", "IOP only"], "Retinoscopy observes reflex movement to determine refractive status."),
            q("Against movement on retinoscopy generally indicates", "Myopia greater than working distance correction", ["Hypermetropia always", "Normal emmetropia always", "Colour blindness"], "Retinoscopic reflex direction helps identify and neutralize refractive error."),
            q("A child with suspected latent hypermetropia is examined after cycloplegic drops. This is done to", "Eliminate accommodation during refraction", ["Increase retinal bleeding", "Cause permanent miosis", "Measure tear secretion"], "Cycloplegia reveals true refractive error by relaxing accommodation.", True),
            q("During subjective refraction, a patient with residual meridional blur is tested with a Jackson cross-cylinder. It is used for refining", "Astigmatic correction", ["Lacrimal obstruction", "Colour blindness", "IOP"], "JCC refines cylinder power and axis during subjective refraction.", True),
            q("Trial frame and trial lenses are used during", "Subjective refraction", ["Cryotherapy", "Syringing", "Tonography only"], "Trial lenses help determine the correction giving best visual acuity."),
            q("Cover-uncover test detects", "Tropia", ["Phoria only", "Dry eye", "Corneal ulcer"], "Movement of the uncovered eye indicates manifest deviation."),
            q("Alternate cover test reveals", "Total ocular deviation including phoria", ["Only cataract grade", "Only colour defect", "Only IOP"], "Alternating occlusion dissociates fusion and shows total deviation."),
            q("A child has corneal light reflex displaced temporally in one eye. Hirschberg test suggests", "Esotropia", ["Exotropia", "Hypertropia only", "Normal alignment"], "Temporal corneal reflex means the visual axis is turned inward."),
            q("A patient with intermittent diplopia is evaluated with a Maddox rod. The test assesses", "Ocular deviation and diplopia", ["Tear secretion", "Corneal ulcer depth", "Retinal cholesterol"], "Maddox rod dissociates images to measure phorias and tropias.", True),
            q("Worth four-dot test evaluates", "Binocular single vision and suppression", ["Intraocular pressure", "Axial length", "Lacrimal patency"], "Worth four-dot assesses fusion, diplopia and suppression."),
            q("A squinting child suppresses one eye on Worth four-dot test. This indicates risk of", "Amblyopia", ["Acute glaucoma", "Endophthalmitis", "Dacryocystitis"], "Persistent suppression during visual development can produce amblyopia.", True),
            q("Hess charting is used mainly for", "Paralytic squint assessment", ["Cataract grading only", "Tear film testing", "Fundus photography only"], "Hess chart maps underaction and overaction in ocular muscle palsies."),
            q("A patient with diplopia after head injury has suspected sixth nerve palsy. Which practical chart helps document it", "Hess chart", ["Jaeger chart", "Schirmer chart", "Amsler chart only"], "Hess charting helps identify and follow extraocular muscle palsy.", True),
            q("Exophthalmometry measures", "Proptosis", ["Corneal staining", "Colour vision", "Visual acuity only"], "Hertel exophthalmometry quantifies anterior displacement of the globe."),
            q("A thyroid eye disease patient needs objective follow-up of eye prominence. Which tool is used", "Hertel exophthalmometer", ["Schiotz tonometer", "Maddox rod only", "Amsler grid"], "Exophthalmometry documents proptosis in orbital disease.", True),
        ]),
    ]),
]


def build_questions():
    questions = []
    for chapter, chapter_order, topics in CHAPTERS:
        for topic_order, (topic, rows) in enumerate(topics, 1):
            if len(rows) % 10 != 0:
                raise ValueError(f"{topic} has {len(rows)} questions, expected blocks of 10")
            for block_start in range(0, len(rows), 10):
                clinical_count = sum(1 for row in rows[block_start:block_start + 10] if "clinical" in row.get("tags", []))
                if clinical_count != 4:
                    raise ValueError(f"{topic} block {block_start // 10 + 1} has {clinical_count} clinical questions, expected 4")
            topic_slug = slugify(topic)
            chapter_slug = slugify(chapter)
            for question_order, row in enumerate(rows, 1):
                questions.append({
                    "id": f"ophth-{chapter_slug}-{topic_slug}-{question_order:02d}",
                    "subjectId": SUBJECT_ID,
                    "subjectTitle": SUBJECT_TITLE,
                    "chapterTitle": chapter,
                    "chapterOrder": chapter_order,
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
    chapter_names = {chapter for chapter, _, _ in CHAPTERS}
    chapter_names.add("Practical Opthalmology")
    data["questions"] = [
        item for item in data.get("questions", [])
        if not (item.get("subjectId") == SUBJECT_ID and item.get("chapterTitle") in chapter_names)
    ] + questions
    if len(questions) != 90:
        raise AssertionError(f"Expected 90 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 90:
        raise AssertionError("Duplicate ophthalmology question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 90 ophthalmology systemic/community/practical questions.")


if __name__ == "__main__":
    main()
