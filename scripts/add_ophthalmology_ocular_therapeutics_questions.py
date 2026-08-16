import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ophthalmology"
SUBJECT_TITLE = "Ophthalmology"
CHAPTER = "Ocular Therapeutics"
CHAPTER_ORDER = 4
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
    ("Ocular Pharmacology", [
        q("The commonest route for treating anterior segment eye disease is", "Topical instillation", ["Intrathecal injection", "Oral depot therapy only", "Subconjunctival implant always"], "Drops deliver high drug concentration to conjunctiva, cornea and anterior chamber with less systemic exposure."),
        q("A patient using antiglaucoma drops develops bradycardia and bronchospasm. Which drug is most likely responsible", "Timolol", ["Latanoprost", "Pilocarpine", "Dorzolamide"], "Topical beta blockers can be absorbed systemically and may worsen asthma, COPD or bradyarrhythmia.", True),
        q("A preservative commonly present in multidose ophthalmic preparations is", "Benzalkonium chloride", ["Mannitol", "Fluorescein sodium", "Hyaluronidase"], "Benzalkonium chloride is a quaternary ammonium preservative but can irritate the ocular surface."),
        q("A patient with exposure keratopathy is advised lubricating ointment at bedtime rather than drops. The advantage is", "Greater contact time", ["Lower viscosity than tears", "No drug content", "Only systemic absorption"], "Ointments prolong contact with the ocular surface but commonly blur vision, so bedtime use is practical.", True),
        q("Topical atropine produces mydriasis by blocking", "Muscarinic receptors", ["Beta-1 receptors", "Alpha-2 receptors", "Carbonic anhydrase",], "Atropine is an antimuscarinic cycloplegic that blocks sphincter pupillae and ciliary muscle action."),
        q("A child undergoes cycloplegic refraction and remains photophobic with near blur for many days. Which drug was likely used", "Atropine", ["Tropicamide", "Phenylephrine", "Fluorescein"], "Atropine is long acting and can cause prolonged cycloplegia and mydriasis.", True),
        q("The shortest acting commonly used mydriatic-cycloplegic is", "Tropicamide", ["Atropine", "Homatropine", "Pilocarpine"], "Tropicamide has a rapid onset and short duration, making it useful for routine fundus examination."),
        q("Phenylephrine dilates the pupil by stimulating", "Alpha-1 receptors of dilator pupillae", ["Muscarinic receptors of sphincter pupillae", "Beta receptors of ciliary epithelium", "Histamine receptors in conjunctiva"], "Phenylephrine is a sympathomimetic mydriatic with little cycloplegic effect."),
        q("A patient with acute anterior uveitis is prescribed homatropine. The main purpose is to", "Relieve ciliary spasm and prevent posterior synechiae", ["Increase corneal ulcer depth", "Constrict pupil permanently", "Increase aqueous production"], "Cycloplegics rest the inflamed ciliary body and keep the pupil mobile.", True),
        q("Pilocarpine lowers intraocular pressure chiefly by", "Increasing trabecular outflow", ["Suppressing aqueous production", "Paralyzing accommodation", "Blocking prostaglandin receptors"], "Pilocarpine contracts ciliary muscle, opens the trabecular meshwork and increases conventional outflow."),
        q("Latanoprost lowers intraocular pressure mainly by increasing", "Uveoscleral outflow", ["Aqueous protein concentration", "Lens transparency", "Pupillary block"], "Prostaglandin analogues increase uveoscleral aqueous drainage."),
        q("A glaucoma patient develops iris darkening and eyelash growth after starting a once-nightly drop. Which class is likely", "Prostaglandin analogue", ["Topical steroid", "Mydriatic anticholinergic", "Antiviral"], "Prostaglandin analogues such as latanoprost can cause hypertrichosis and increased iris pigmentation.", True),
        q("Dorzolamide reduces intraocular pressure by inhibiting", "Carbonic anhydrase in ciliary epithelium", ["Cyclooxygenase in retina", "Acetylcholinesterase at neuromuscular junction", "DNA gyrase in cornea"], "Carbonic anhydrase inhibitors reduce bicarbonate-dependent aqueous humour formation."),
        q("Brimonidine is an antiglaucoma drug that acts as an", "Alpha-2 adrenergic agonist", ["Alpha-1 blocker", "Muscarinic antagonist", "Prostaglandin antagonist"], "Alpha-2 agonists lower aqueous production and can also increase uveoscleral outflow."),
        q("Topical corticosteroids are avoided in untreated herpes simplex epithelial keratitis because they may", "Worsen viral replication and corneal ulceration", ["Immediately cure dendritic ulcers", "Prevent cataract always", "Lower risk of fungal infection"], "Steroids can aggravate epithelial HSV disease unless antiviral cover and indication are appropriate."),
        q("A patient self-medicates steroid drops for a red eye and develops raised IOP. Which complication is this", "Steroid-induced glaucoma", ["Aphakia", "Pinguecula", "Myopia reversal"], "Corticosteroids can increase trabecular outflow resistance and raise IOP in responders.", True),
        q("Fluorescein staining is used clinically to detect", "Corneal epithelial defects", ["Optic nerve pallor", "Lens nuclear hardness", "Retinal arterial emboli only"], "Fluorescein pools in areas where corneal epithelium is absent or disrupted."),
        q("Rose bengal and lissamine green stain mainly", "Devitalized ocular surface cells and mucus", ["Intact lens fibres", "Normal retinal vessels", "Vitreous collagen only"], "These dyes help evaluate ocular surface disease and dry eye."),
        q("A contact lens wearer has a corneal ulcer. Which topical antibiotic coverage is especially important", "Antipseudomonal coverage", ["Antitubercular monotherapy", "Only antiviral ointment", "Only oral antifungal"], "Contact lens keratitis has strong association with Pseudomonas and needs appropriate broad topical coverage.", True),
        q("Intravitreal drug delivery is preferred when high drug levels are needed in the", "Vitreous and retina", ["Eyelid skin only", "Nasolacrimal sac only", "Spectacle lens"], "Intravitreal injection bypasses ocular barriers and delivers therapeutic levels to the posterior segment.", True),
    ]),
    ("Lasers and Cryotherapy in Ophthalmology", [
        q("Laser light is characterized by being monochromatic, coherent and", "Collimated", ["Incoherent", "Polychromatic only", "Sound based"], "Ophthalmic lasers produce focused, predictable energy because the beam is collimated and coherent."),
        q("Argon laser energy is absorbed mainly by", "Melanin and haemoglobin", ["Water only", "Bone calcium", "Air in anterior chamber"], "Blue-green argon wavelengths are useful for retinal photocoagulation because pigment and blood absorb them."),
        q("A patient with proliferative diabetic retinopathy undergoes panretinal photocoagulation. The treatment aims to reduce", "Retinal ischemic drive for neovascularization", ["Corneal thickness", "Lens capsule fibrosis", "Aqueous humour pH only"], "PRP ablates ischemic peripheral retina, lowering angiogenic stimulus and neovascular complications.", True),
        q("The laser commonly used for posterior capsulotomy after cataract surgery is", "Nd:YAG laser", ["Excimer laser", "Diode indirect laser", "Argon laser trabeculoplasty only"], "Nd:YAG produces photodisruption and is used to open an opacified posterior capsule."),
        q("A pseudophakic patient develops painless gradual blur from posterior capsular opacification. Best laser procedure is", "Nd:YAG posterior capsulotomy", ["Panretinal photocoagulation", "Laser peripheral iridotomy only", "Transscleral cyclophotocoagulation"], "Posterior capsular opacification is treated by creating a central opening with Nd:YAG laser.", True),
        q("Laser peripheral iridotomy is most useful in", "Pupillary block angle closure", ["Open globe injury", "Bacterial conjunctivitis", "Mature cataract without glaucoma"], "Iridotomy creates an alternate aqueous pathway from posterior to anterior chamber."),
        q("In acute angle closure, laser iridotomy is performed after initial medical therapy mainly to", "Prevent recurrence of pupillary block", ["Remove the crystalline lens nucleus immediately", "Seal a corneal ulcer", "Treat optic neuritis"], "Once cornea clears and IOP is controlled, iridotomy addresses the underlying pupillary block mechanism.", True),
        q("Selective laser trabeculoplasty lowers IOP by targeting", "Trabecular meshwork", ["Macular photoreceptors", "Posterior capsule", "Lacrimal gland"], "SLT improves aqueous outflow through the trabecular meshwork in open-angle glaucoma."),
        q("Retinal photocoagulation treats retinal tears by creating", "Chorioretinal adhesion", ["Posterior synechiae", "Corneal epithelial defect", "Lens zonular relaxation"], "Laser burns around a tear scar the retina to underlying tissue and reduce detachment risk."),
        q("A high myope has a symptomatic horseshoe retinal tear without detachment. Which procedure is appropriate", "Barricade laser photocoagulation", ["Nd:YAG capsulotomy", "Laser iridotomy", "Cycloplegic refraction only"], "Laser retinopexy surrounds the break with adhesive scars before fluid enters the subretinal space.", True),
        q("Focal or grid macular laser has historically been used for", "Diabetic macular edema", ["Trachoma scarring", "Congenital ptosis", "Acute dacryocystitis"], "Macular laser can reduce leakage in selected diabetic macular edema, though anti-VEGF therapy is now central."),
        q("Excimer laser reshapes the cornea using", "Photoablation", ["Photocoagulation", "Cryoadhesion", "Photodynamic thrombosis only"], "Excimer laser removes microscopic stromal tissue with minimal thermal damage."),
        q("LASIK corrects refractive error by applying excimer laser to the", "Corneal stroma under a flap", ["Retina", "Lens nucleus", "Trabecular meshwork"], "LASIK creates a corneal flap, then photoablates stromal tissue to alter corneal curvature."),
        q("A patient seeking refractive surgery has unstable keratoconus. Why is LASIK contraindicated", "It can worsen corneal ectasia", ["It always causes cataract", "It blocks nasolacrimal drainage", "It permanently closes the angle"], "Removing stromal tissue from an ectatic cornea may destabilize it further.", True),
        q("Diode laser cyclophotocoagulation lowers IOP by damaging", "Ciliary body epithelium", ["Posterior capsule", "Corneal epithelium", "Optic disc cup"], "Cyclodestructive procedures reduce aqueous production by treating ciliary processes."),
        q("Cryotherapy treats peripheral retinal breaks by producing", "Chorioretinal scar formation", ["Pupil dilation only", "Lens accommodation", "Corneal endothelial regeneration"], "Freezing causes controlled inflammation and adhesion around the break."),
        q("Cryotherapy in retinoblastoma is most suitable for", "Small anterior peripheral retinal tumors", ["Large optic nerve invading tumors", "Diffuse orbital extension", "Dense mature cataract"], "Cryotherapy is a focal treatment for selected small peripheral retinoblastoma lesions."),
        q("An infant with retinoblastoma has a small peripheral tumor anterior to the equator. Which focal therapy is useful", "Cryotherapy", ["Nd:YAG capsulotomy", "LASIK", "Trabeculoplasty"], "Anterior peripheral retinoblastoma lesions can be treated with freeze-thaw cryotherapy.", True),
        q("A patient with an anterior retinal break has media haze that makes laser delivery difficult. Cryotherapy is useful because", "Media haze or anterior location limits laser delivery", ["The retina is perfectly visible and central macula is involved", "Only posterior capsule is opacified", "The problem is presbyopia"], "Cryotherapy can be applied transsclerally when direct laser visualization is difficult.", True),
        q("A patient develops marked lid swelling and conjunctival chemosis after retinal cryopexy. This is due to", "Inflammatory reaction from freezing", ["Posterior capsular opacity", "Cycloplegic paralysis only", "Aqueous overproduction by laser"], "Cryotherapy causes more postoperative inflammation than laser photocoagulation.", True),
    ]),
]


def build_questions():
    questions = []
    for topic_order, (topic, rows) in enumerate(TOPICS, 1):
        if len(rows) != 20:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 20")
        clinical_count = sum(1 for row in rows if "clinical" in row.get("tags", []))
        if clinical_count != 8:
            raise ValueError(f"{topic} has {clinical_count} clinical questions, expected 8")
        topic_slug = slugify(topic)
        for question_order, row in enumerate(rows, 1):
            questions.append({
                "id": f"ophth-ocular-therapeutics-{topic_slug}-{question_order:02d}",
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
    if len(questions) != 40:
        raise AssertionError(f"Expected 40 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 40:
        raise AssertionError("Duplicate ophthalmology ocular therapeutics question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 40 ophthalmology ocular therapeutics questions.")


if __name__ == "__main__":
    main()
