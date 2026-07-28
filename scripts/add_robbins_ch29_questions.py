import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Eye"
BASE = {"subjectId": "pathology", "subjectTitle": "Pathology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(difficulty, prompt, answer, distractors, explanation):
    if difficulty not in {"easy", "moderate", "high"}:
        raise ValueError(difficulty)
    options = [answer, *distractors]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {"difficulty": difficulty, "prompt": prompt, "options": options, "answerIndex": 0, "answer": answer, "explanation": explanation}


def jumble(question, desired_index):
    answer = question["answer"]
    distractors = [option for option in question["options"] if option != answer]
    options = distractors[:]
    options.insert(desired_index, answer)
    question["options"] = options
    question["answerIndex"] = desired_index
    return question


TOPICS = [
    ("eyelid-conjunctiva", "Eyelid, Conjunctiva, and Ocular Surface Lesions", [
        q("easy", "A chalazion is a chronic inflammation of a:", "Meibomian gland", ["Lacrimal nerve", "Retinal vessel", "Optic disc"], "Chalazion is lipogranulomatous inflammation of meibomian glands."),
        q("easy", "A hordeolum is commonly called a:", "Stye", ["Pterygium", "Cataract", "Glaucoma"], "Hordeolum is an acute suppurative eyelid gland infection."),
        q("easy", "Pterygium is a fibrovascular growth onto the:", "Cornea", ["Retina", "Optic nerve", "Lens nucleus"], "Pterygium extends from conjunctiva onto cornea."),
        q("moderate", "Basal cell carcinoma of eyelid most often affects the:", "Lower eyelid", ["Retina", "Lens", "Choroid only"], "Lower eyelid is a common site for periocular BCC."),
        q("moderate", "Sebaceous carcinoma of eyelid may mimic:", "Chalazion", ["Retinoblastoma", "Cataract", "Papilledema"], "Sebaceous carcinoma can present like recurrent chalazion."),
        q("moderate", "Conjunctival squamous dysplasia is strongly related to:", "UV exposure", ["Hypercalcemia", "Myelin loss", "Urate crystals"], "UV light contributes to ocular surface squamous neoplasia."),
        q("moderate", "Pinguecula is an elastotic degeneration of:", "Conjunctival stroma", ["Retinal ganglion cells", "Lens fibers", "Optic nerve myelin"], "Pinguecula is a yellow conjunctival elastotic lesion."),
        q("high", "An older patient has a recurrent eyelid lesion treated as chalazion, but biopsy shows malignant cells with sebaceous differentiation and pagetoid spread. Which tumor is most likely?", "Sebaceous carcinoma", ["Basal cell carcinoma", "Squamous papilloma", "Conjunctival nevus"], "Sebaceous carcinoma can masquerade as chalazion."),
        q("high", "A sun-exposed worker has a triangular fibrovascular conjunctival lesion crossing the limbus and encroaching on the cornea, causing irritation and astigmatism. Which lesion is present?", "Pterygium", ["Pinguecula only", "Chalazion", "Retinoblastoma"], "Pterygium grows from conjunctiva onto cornea."),
        q("high", "A pearly ulcerated nodule on the lower eyelid shows nests of basaloid cells with peripheral palisading and stromal retraction. Which eyelid malignancy is likely?", "Basal cell carcinoma", ["Sebaceous carcinoma", "Melanoma", "Lymphoma"], "Basal cell carcinoma is common on eyelid and shows palisading."),
    ]),
    ("cornea-sclera", "Cornea, Sclera, and Anterior Segment Inflammation", [
        q("easy", "Keratitis means inflammation of the:", "Cornea", ["Retina", "Lens", "Optic nerve"], "Keratitis is corneal inflammation."),
        q("easy", "Scleritis is inflammation of the:", "Sclera", ["Choroid only", "Lens capsule", "Vitreous"], "Scleritis involves the scleral coat."),
        q("easy", "Corneal ulcer can threaten vision by causing:", "Scarring", ["Bone formation", "Retinal detachment always", "Cataract only"], "Corneal scarring can impair transparency."),
        q("moderate", "Herpes simplex keratitis often forms:", "Dendritic ulcers", ["Drusen", "Cotton wool spots", "Keratic precipitates only"], "HSV keratitis produces branching dendritic epithelial ulcers."),
        q("moderate", "Acanthamoeba keratitis is associated with:", "Contact lens use", ["Hypertension only", "Diabetes always", "Retinoblastoma"], "Contact lens exposure is a major risk."),
        q("moderate", "Fuchs endothelial dystrophy primarily affects corneal:", "Endothelium", ["Epithelium only", "Sclera", "Retina"], "Endothelial failure causes corneal edema."),
        q("moderate", "Keratoconus causes cone-shaped thinning of the:", "Cornea", ["Lens", "Optic disc", "Macula"], "Keratoconus is ectatic corneal thinning."),
        q("high", "A patient with painful red eye and contact lens use has severe keratitis with ring infiltrate, and organisms show cyst and trophozoite forms. Which infection is likely?", "Acanthamoeba keratitis", ["HSV keratitis", "Bacterial conjunctivitis", "CMV retinitis"], "Acanthamoeba keratitis is linked to contact lenses."),
        q("high", "A patient has recurrent painful keratitis with branching epithelial defects that stain with fluorescein and contain viral cytopathic changes. Which pathogen is most likely?", "Herpes simplex virus", ["Acanthamoeba", "Candida", "Toxoplasma gondii"], "HSV causes dendritic corneal ulcers."),
        q("high", "An older woman develops progressive corneal edema and blurred vision because endothelial cells fail and Descemet membrane shows guttae. Which corneal dystrophy is most likely?", "Fuchs endothelial dystrophy", ["Keratoconus", "Band keratopathy", "HSV keratitis"], "Fuchs dystrophy causes endothelial loss and corneal edema."),
    ]),
    ("uvea-inflammation", "Uveitis, Choroid, and Intraocular Inflammation", [
        q("easy", "Uveitis is inflammation of the:", "Uveal tract", ["Lens fibers", "Optic nerve only", "Eyelid glands"], "The uvea includes iris, ciliary body, and choroid."),
        q("easy", "The uveal tract includes the iris, ciliary body, and:", "Choroid", ["Cornea", "Lens", "Conjunctiva"], "Choroid is part of uveal tract."),
        q("easy", "Endophthalmitis is infection involving:", "Intraocular cavities", ["Eyelid skin only", "Optic canal only", "Lacrimal sac only"], "Endophthalmitis is severe intraocular inflammation."),
        q("moderate", "Anterior uveitis is associated with:", "HLA-B27 disease", ["Osteopetrosis", "Duchenne dystrophy", "Cystic fibrosis"], "Spondyloarthropathies can cause anterior uveitis."),
        q("moderate", "Sympathetic ophthalmia follows penetrating trauma to one eye and affects:", "Both eyes", ["Only eyelid skin", "Only lacrimal gland", "Only retina vessels"], "Autoimmune response can inflame both eyes."),
        q("moderate", "Sarcoidosis can cause granulomatous:", "Uveitis", ["Cataract only", "Retinoblastoma", "Glaucoma only"], "Sarcoidosis is a systemic granulomatous cause of uveitis."),
        q("moderate", "Endophthalmitis after surgery is often:", "Bacterial", ["Prion-related", "Purely degenerative", "Metabolic only"], "Postoperative endophthalmitis is often bacterial."),
        q("high", "A young man with ankylosing spondylitis develops painful photophobic red eye. Slit lamp shows anterior chamber cells and flare. Which ocular inflammatory disorder is most likely?", "Anterior uveitis", ["Fuchs dystrophy", "Retinal detachment", "Chalazion"], "HLA-B27 spondyloarthritis is linked to anterior uveitis."),
        q("high", "After penetrating injury to one eye, a patient develops bilateral granulomatous uveitis with T-cell response against normally sequestered ocular antigens. Which diagnosis is most likely?", "Sympathetic ophthalmia", ["Endophthalmitis", "Retinoblastoma", "Keratoconus"], "Sympathetic ophthalmia is bilateral autoimmune uveitis after trauma."),
        q("high", "A postoperative patient develops severe eye pain, hypopyon, decreased vision, and vitreous inflammation from bacterial infection within the eye after surgery. Which complication is present?", "Endophthalmitis", ["Pinguecula", "Open-angle glaucoma", "Senile cataract"], "Endophthalmitis is severe intraocular infection."),
    ]),
    ("lens-cataract", "Lens Disease and Cataract", [
        q("easy", "Cataract is opacity of the:", "Lens", ["Retina", "Cornea only", "Optic nerve"], "Cataract is lens opacity."),
        q("easy", "The most common cataract is related to:", "Aging", ["Retinoblastoma", "Uveitis always", "Optic neuritis"], "Age-related cataract is common."),
        q("easy", "Diabetes predisposes to:", "Cataract", ["Retinoblastoma only", "Pterygium only", "Optic glioma only"], "Diabetes accelerates lens opacification."),
        q("moderate", "Diabetic cataract formation is related to accumulation of:", "Sorbitol", ["Amyloid beta", "Urate", "Calcitonin"], "Aldose reductase converts glucose to sorbitol in lens."),
        q("moderate", "Posterior subcapsular cataracts are associated with:", "Corticosteroid use", ["PMP22 deletion", "RB1 deletion only", "HLA-B27 only"], "Steroids can cause posterior subcapsular cataracts."),
        q("moderate", "Congenital cataracts can be caused by:", "Rubella infection", ["HSV keratitis only", "Hypertension", "Gout"], "Congenital rubella may cause cataracts."),
        q("moderate", "Lens proteins lose transparency partly due to:", "Oxidative damage", ["Demyelination", "Bone resorption", "Synovial pannus"], "Protein damage and aggregation opacify the lens."),
        q("high", "An older adult has slowly progressive painless blurred vision and lens opacity from protein aggregation and oxidative damage over many years. Which diagnosis is most likely?", "Age-related cataract", ["Acute glaucoma", "Retinal detachment", "Uveitis"], "Senile cataract causes painless progressive lens opacity."),
        q("high", "A patient with poorly controlled diabetes develops lens swelling and opacity because excess glucose is converted by aldose reductase to an osmotically active alcohol. Which molecule accumulates?", "Sorbitol", ["Lactate", "Urate", "Dopamine"], "Sorbitol accumulation contributes to diabetic cataract."),
        q("high", "A newborn has cataracts, cardiac defects, hearing impairment, and growth restriction after maternal viral infection during early pregnancy. Which congenital infection classically causes this triad?", "Rubella", ["Toxoplasma", "Cytomegalovirus only", "Varicella zoster"], "Congenital rubella syndrome includes cataracts, deafness, and heart disease."),
    ]),
    ("glaucoma", "Glaucoma and Optic Nerve Cupping", [
        q("easy", "Glaucoma damages the:", "Optic nerve", ["Lens capsule", "Eyelid gland", "Extraocular muscle"], "Glaucoma causes optic neuropathy."),
        q("easy", "Open-angle glaucoma usually has an open:", "Anterior chamber angle", ["Lacrimal duct", "Optic canal", "Retinal tear"], "The angle remains anatomically open."),
        q("easy", "Angle-closure glaucoma is often:", "Painful and acute", ["Always painless", "A congenital tumor", "A corneal dystrophy"], "Acute angle closure causes painful high pressure."),
        q("moderate", "Glaucoma produces increased cup-to-disc ratio due to loss of:", "Retinal ganglion cell axons", ["Lens fibers", "Corneal endothelium", "Melanocytes"], "Optic nerve axon loss causes cupping."),
        q("moderate", "Primary open-angle glaucoma is associated with impaired:", "Aqueous humor outflow", ["Vitreous production", "Tear secretion", "Lens metabolism"], "Trabecular outflow resistance increases pressure."),
        q("moderate", "Acute angle closure is precipitated by blockage at the:", "Trabecular meshwork angle", ["Macula", "Optic disc", "Choroid only"], "Closure prevents aqueous drainage."),
        q("moderate", "Congenital glaucoma may result from abnormal development of:", "Anterior chamber angle", ["Retinal rods only", "Lens nucleus only", "Eyelid skin"], "Angle dysgenesis impairs aqueous outflow."),
        q("high", "An older patient has slowly progressive peripheral visual field loss, elevated intraocular pressure, open angles, and optic disc cupping. Which diagnosis is most likely?", "Primary open-angle glaucoma", ["Acute angle-closure glaucoma", "Cataract", "Retinal detachment"], "Open-angle glaucoma causes chronic optic neuropathy."),
        q("high", "A patient develops sudden painful red eye, halos around lights, mid-dilated pupil, cloudy cornea, nausea, and markedly elevated intraocular pressure. Which disorder is present?", "Acute angle-closure glaucoma", ["Open-angle glaucoma", "Optic neuritis", "Chalazion"], "Angle closure is an acute painful glaucoma emergency."),
        q("high", "A glaucomatous optic disc shows enlarged excavation because retinal ganglion cell axons are lost at the optic nerve head. Which morphologic change is described?", "Optic nerve cupping", ["Papilledema", "Drusen", "Retinal tear"], "Cupping reflects glaucomatous optic nerve damage."),
    ]),
    ("retina-detachment-degeneration", "Retinal Degeneration, Detachment, and Macular Disease", [
        q("easy", "Retinal detachment separates neurosensory retina from:", "Retinal pigment epithelium", ["Lens capsule", "Corneal stroma", "Optic nerve sheath"], "Detachment separates neurosensory retina from RPE."),
        q("easy", "Age-related macular degeneration affects central:", "Vision", ["Hearing", "Peripheral nerve conduction", "Bone growth"], "Macular disease impairs central vision."),
        q("easy", "Retinitis pigmentosa causes progressive loss of:", "Photoreceptors", ["Lens fibers", "Corneal endothelium", "Aqueous humor"], "Inherited photoreceptor degeneration causes RP."),
        q("moderate", "Drusen are deposits between RPE and:", "Bruch membrane", ["Lens capsule", "Optic nerve myelin", "Corneal epithelium"], "Drusen are extracellular deposits beneath RPE."),
        q("moderate", "Wet macular degeneration involves:", "Choroidal neovascularization", ["Lens opacification", "Trabecular scarring only", "Ciliary spasm"], "Neovascular membranes leak and bleed."),
        q("moderate", "Rhegmatogenous retinal detachment requires a retinal:", "Tear", ["Tumor only", "Infection only", "Cataract"], "Fluid enters through a retinal break."),
        q("moderate", "Retinitis pigmentosa often presents first with:", "Night blindness", ["Eye pain only", "Acute halos", "Purulent discharge"], "Rod dysfunction causes nyctalopia."),
        q("high", "An older patient has central vision loss, drusen, geographic atrophy, and degeneration of retinal pigment epithelium in the macula. Which disease is most likely?", "Dry age-related macular degeneration", ["Wet AMD", "Retinal detachment", "CMV retinitis"], "Dry AMD features drusen and RPE atrophy."),
        q("high", "An older patient has sudden distorted central vision due to abnormal choroidal vessels growing through Bruch membrane with leakage and hemorrhage. Which macular disease is present?", "Wet age-related macular degeneration", ["Dry AMD only", "Retinitis pigmentosa", "Open-angle glaucoma"], "Wet AMD is choroidal neovascularization."),
        q("high", "A patient sees flashes and floaters followed by a curtain over vision. Exam shows fluid separating neurosensory retina from RPE through a retinal tear. Which detachment type is this?", "Rhegmatogenous retinal detachment", ["Tractional detachment", "Exudative detachment", "Macular drusen"], "Rhegmatogenous detachment is due to a retinal break."),
    ]),
    ("vascular-retinopathy", "Vascular Retinopathies and Retinal Ischemia", [
        q("easy", "Diabetic retinopathy is a complication of:", "Diabetes mellitus", ["Glaucoma only", "Chalazion", "Pterygium"], "Hyperglycemia damages retinal microvasculature."),
        q("easy", "Hypertensive retinopathy is due to chronic:", "High blood pressure", ["Low glucose", "Lens opacity", "Viral keratitis"], "Hypertension injures retinal vessels."),
        q("easy", "Retinal artery occlusion causes sudden:", "Vision loss", ["Cataract", "Eyelid swelling only", "Tearing"], "Arterial occlusion acutely ischemic retina."),
        q("moderate", "Proliferative diabetic retinopathy is defined by:", "Neovascularization", ["Drusen only", "Lens opacity", "Open angle"], "Ischemia drives VEGF-mediated new vessels."),
        q("moderate", "Cotton wool spots represent:", "Nerve fiber layer infarcts", ["Lens protein aggregates", "Corneal ulcers", "Uveal granulomas"], "They are retinal microinfarcts."),
        q("moderate", "Central retinal artery occlusion classically shows:", "Cherry-red spot", ["Kayser-Fleischer ring", "Bitot spot", "Hypopyon"], "Pale retina contrasts with foveal choroidal circulation."),
        q("moderate", "Retinopathy of prematurity is driven by abnormal retinal:", "Neovascularization", ["Lens calcification", "Corneal scarring", "Uveal melanoma"], "Oxygen-related vascular disruption causes neovascularization."),
        q("high", "A patient with long-standing diabetes has microaneurysms, hemorrhages, hard exudates, and later fragile new vessels growing on retina and disc. Which complication is present?", "Proliferative diabetic retinopathy", ["Dry AMD", "Open-angle glaucoma", "Retinitis pigmentosa"], "Neovascularization defines proliferative diabetic retinopathy."),
        q("high", "A patient with severe hypertension has arteriolar narrowing, flame hemorrhages, cotton wool spots, hard exudates, and papilledema. Which ocular manifestation of systemic disease is present?", "Hypertensive retinopathy", ["CMV retinitis", "Retinal detachment", "Choroidal melanoma"], "Hypertension causes retinal vascular damage."),
        q("high", "A patient has sudden painless monocular blindness. Fundus shows pale retina with a cherry-red foveal spot after embolic arterial obstruction. Which vessel is occluded?", "Central retinal artery", ["Central retinal vein", "Posterior ciliary vein", "Lacrimal artery"], "Central retinal artery occlusion causes acute retinal ischemia."),
    ]),
    ("ocular-infections", "Ocular Infections and Opportunistic Retinitis", [
        q("easy", "CMV retinitis occurs mainly in:", "Immunocompromised patients", ["Healthy newborn adults only", "Patients with cataract only", "Hypertensive patients only"], "CMV retinitis is common in severe immunosuppression."),
        q("easy", "Toxoplasmosis commonly affects the:", "Retina and choroid", ["Lens only", "Eyelid gland", "Trabecular meshwork"], "Toxoplasma causes retinochoroiditis."),
        q("easy", "Trachoma is caused by:", "Chlamydia trachomatis", ["Acanthamoeba", "CMV", "HSV-1 only"], "Chlamydia trachomatis causes trachoma."),
        q("moderate", "CMV retinitis has necrosis with:", "Hemorrhage", ["Drusen", "Lens opacity only", "Palisading basaloid nests"], "CMV retinitis causes necrotizing hemorrhagic lesions."),
        q("moderate", "Congenital toxoplasmosis can cause:", "Chorioretinitis", ["Glaucoma only", "Chalazion", "Pterygium"], "Chorioretinitis is a classic congenital toxoplasmosis finding."),
        q("moderate", "Trachoma can cause blindness by:", "Conjunctival scarring and corneal opacity", ["Retinoblastoma", "Lens dislocation", "Macular drusen"], "Scarring distorts lashes and scars cornea."),
        q("moderate", "HSV eye infection commonly causes:", "Keratitis", ["Retinoblastoma", "Open-angle glaucoma", "Dry AMD"], "HSV commonly causes epithelial keratitis."),
        q("high", "An AIDS patient has painless progressive vision loss with retinal hemorrhage and necrosis in a perivascular distribution. Enlarged cells show viral inclusions. Which infection is most likely?", "Cytomegalovirus retinitis", ["Toxoplasma retinochoroiditis", "HSV keratitis", "Trachoma"], "CMV causes hemorrhagic necrotizing retinitis in AIDS."),
        q("high", "A child with congenital infection has hydrocephalus, intracranial calcifications, seizures, developmental delay, and recurrent necrotizing retinochoroiditis involving the posterior pole. Which organism is most likely?", "Toxoplasma gondii", ["Chlamydia trachomatis", "Acanthamoeba", "CMV only"], "Congenital toxoplasmosis causes chorioretinitis, hydrocephalus, and calcifications."),
        q("high", "A patient from an endemic area develops chronic follicular conjunctivitis, eyelid scarring, trichiasis, and corneal opacity with progressive blindness. Which organism causes this blinding disease?", "Chlamydia trachomatis", ["HSV-1", "CMV", "Toxoplasma gondii"], "Trachoma from C. trachomatis causes scarring blindness."),
    ]),
    ("optic-nerve", "Optic Nerve, Papilledema, and Inherited Optic Disorders", [
        q("easy", "Papilledema is swelling of the:", "Optic disc", ["Lens", "Cornea", "Eyelid"], "Papilledema is optic disc edema."),
        q("easy", "Optic neuritis is inflammation of the:", "Optic nerve", ["Lens", "Sclera", "Meibomian gland"], "Optic neuritis causes painful vision loss."),
        q("easy", "Optic neuritis is associated with:", "Multiple sclerosis", ["Osteoarthritis", "Chalazion", "Cataract only"], "Optic neuritis can be an MS manifestation."),
        q("moderate", "Papilledema is often caused by raised:", "Intracranial pressure", ["Intraocular lens opacity", "Blood glucose only", "Tear osmolarity"], "Raised ICP transmits pressure to optic nerve sheath."),
        q("moderate", "Leber hereditary optic neuropathy is due to:", "Mitochondrial DNA mutation", ["RB1 mutation", "PMP22 deletion", "FGFR3 activation"], "LHON is maternally inherited mitochondrial disease."),
        q("moderate", "Glaucoma causes optic nerve damage with increased:", "Cup-to-disc ratio", ["Lens thickness", "Macular drusen", "Corneal ulcer depth"], "Glaucomatous axon loss enlarges the cup."),
        q("moderate", "Ischemic optic neuropathy involves infarction of the:", "Optic nerve head", ["Lens nucleus", "Eyelid skin", "Choroidal melanoma"], "Vascular insufficiency damages optic nerve head."),
        q("high", "A patient with increased intracranial pressure has bilateral blurred disc margins, venous congestion, and optic disc swelling from pressure transmitted along the optic nerve sheath. Which finding is present?", "Papilledema", ["Optic atrophy only", "Retinal detachment", "Chalazion"], "Papilledema is optic disc edema from raised ICP."),
        q("high", "A young woman has painful monocular vision loss, impaired color vision, afferent pupillary defect, and later develops periventricular demyelinating plaques. Which optic nerve disorder is likely?", "Optic neuritis", ["Papilledema", "Retinoblastoma", "Open-angle glaucoma"], "Optic neuritis is associated with multiple sclerosis."),
        q("high", "A young man develops subacute central vision loss, and family history shows maternal transmission. Testing reveals mitochondrial DNA mutation. Which optic neuropathy is likely?", "Leber hereditary optic neuropathy", ["Diabetic retinopathy", "CMV retinitis", "Uveal melanoma"], "LHON is maternally inherited mitochondrial optic neuropathy."),
    ]),
    ("ocular-tumors", "Ocular Tumors: Retinoblastoma, Uveal Melanoma, and Metastases", [
        q("easy", "Retinoblastoma is caused by mutation in:", "RB1", ["RET", "VHL", "HFE"], "RB1 loss drives retinoblastoma."),
        q("easy", "The most common primary intraocular malignancy in adults is:", "Uveal melanoma", ["Retinoblastoma", "Chalazion", "Cataract"], "Uveal melanoma is the common adult primary intraocular cancer."),
        q("easy", "Retinoblastoma often presents with white pupillary reflex called:", "Leukocoria", ["Hypopyon", "Papilledema", "Pterygium"], "Leukocoria is a classic sign."),
        q("moderate", "Retinoblastoma may form:", "Flexner-Wintersteiner rosettes", ["Verocay bodies", "Call-Exner bodies", "Negri bodies"], "These rosettes support retinal differentiation."),
        q("moderate", "Uveal melanoma most often metastasizes to:", "Liver", ["Spleen only", "Kidney cortex only", "Parathyroid"], "Uveal melanoma commonly spreads hematogenously to liver."),
        q("moderate", "Retinoblastoma hereditary cases are often:", "Bilateral", ["Always unilateral", "Only in adults", "Never familial"], "Germline RB1 mutation predisposes to bilateral tumors."),
        q("moderate", "Ocular metastases commonly involve the:", "Choroid", ["Lens", "Cornea only", "Eyelid margin only"], "Choroid is vascular and common for metastases."),
        q("high", "A child has leukocoria and a retinal mass. Histology shows small blue cells forming Flexner-Wintersteiner rosettes after loss of both RB1 alleles. Which tumor is most likely?", "Retinoblastoma", ["Uveal melanoma", "Medulloepithelioma", "Choroidal metastasis"], "Retinoblastoma is an RB1-driven pediatric retinal tumor."),
        q("high", "An adult has a pigmented choroidal mass with spindle and epithelioid melanoma cells, and later develops liver metastases. Which primary ocular tumor is most likely?", "Uveal melanoma", ["Retinoblastoma", "Conjunctival papilloma", "Basal cell carcinoma"], "Uveal melanoma is the common adult intraocular primary malignancy."),
        q("high", "A patient with known lung carcinoma develops visual symptoms, and exam reveals a yellow-white vascular lesion in the posterior uveal tract. Which diagnosis is most likely?", "Choroidal metastasis", ["Retinoblastoma", "Chalazion", "Fuchs dystrophy"], "The choroid is a common site for ocular metastases."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch29-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 29 questions, got {len(chapter_questions)}")
    topic_counts = Counter(q["topic"] for q in chapter_questions)
    if len(topic_counts) != 10 or any(count != 10 for count in topic_counts.values()):
        raise ValueError(f"Bad topic distribution: {topic_counts}")
    expected = Counter({"easy": 3, "moderate": 4, "high": 3})
    for topic in topic_counts:
        counts = Counter(q["difficulty"] for q in chapter_questions if q["topic"] == topic)
        if counts != expected:
            raise ValueError(f"Bad difficulty distribution for {topic}: {counts}")
    for question in chapter_questions:
        options = question["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Bad options: {question['id']}")
        if question["answer"] != options[question["answerIndex"]]:
            raise ValueError(f"Bad answer: {question['id']}")
    short_high = [q["id"] for q in chapter_questions if q["difficulty"] == "high" and len(q["prompt"].split()) < 24]
    if short_high:
        raise ValueError(f"High-level prompts too short: {short_high[:5]}")
    if all_questions is not None:
        ids = [q.get("id") for q in all_questions]
        duplicates = [qid for qid, count in Counter(ids).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate ids: {duplicates[:10]}")


def main():
    chapter_questions = build_questions()
    validate(chapter_questions)
    total_removed = 0
    for data_path in DATA_PATHS:
        data = json.loads(data_path.read_text(encoding="utf-8-sig"))
        existing = data.get("questions", [])
        kept = [
            question for question in existing
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch29-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 29 questions")
    print(f"Removed {total_removed} existing Chapter 29 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 29 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
