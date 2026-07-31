import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ophthalmology"
SUBJECT_TITLE = "Ophthalmology"
CHAPTER = "Anatomy and Physiology of Eye"
CHAPTER_ORDER = 1
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
    ("Anatomy and Development of Eye", [
        q("The outer fibrous coat of the eyeball consists of sclera and", "Cornea", ["Choroid", "Retina", "Ciliary body"], "The fibrous coat is formed by opaque sclera posteriorly and transparent cornea anteriorly."),
        q("The vascular coat of the eye includes choroid, ciliary body and", "Iris", ["Cornea", "Lens capsule", "Vitreous cortex"], "The uveal tract is the vascular middle coat: iris, ciliary body and choroid."),
        q("A newborn has a white pupillary reflex. Which ocular structure must be examined urgently", "Lens and retina", ["Lacrimal punctum only", "Eyelashes only", "Caruncle only"], "Leukocoria may arise from congenital cataract or retinoblastoma and needs urgent evaluation.", True),
        q("The transparent anterior one-sixth of the outer coat is the", "Cornea", ["Sclera", "Choroid", "Ora serrata"], "The cornea forms the clear anterior part of the fibrous coat."),
        q("Bowman's layer lies in the", "Cornea", ["Retina", "Lens", "Optic nerve"], "Bowman's layer is an acellular anterior stromal layer of the cornea."),
        q("A patient has a full-thickness corneal wound. Which corneal layer has poor regenerative capacity and scars", "Stroma", ["Endothelium only", "Tear film", "Epithelium only"], "Stromal collagen disruption heals by scarring and affects transparency.", True),
        q("Descemet membrane is the basement membrane of", "Corneal endothelium", ["Corneal epithelium", "Retinal pigment epithelium", "Lens epithelium"], "Descemet membrane supports the posterior corneal endothelium."),
        q("On gonioscopy, the main filtering structure seen in the anterior chamber angle is", "Trabecular meshwork", ["Macula", "Zonule", "Canal of Schlemm only without trabeculum"], "Aqueous humour drains through trabecular meshwork into Schlemm canal.", True),
        q("A shallow anterior chamber after blunt trauma raises concern for angle damage and future", "Secondary glaucoma", ["Presbyopia only", "Night blindness only", "Ptosis only"], "Angle recession or synechial closure can impair aqueous drainage.", True),
        q("The lens is held in position by", "Zonular fibres", ["Tenon's capsule", "Medial rectus", "Canal of Schlemm"], "Zonules suspend the lens from the ciliary body."),
        q("The strongest refracting surface of the eye is", "Anterior corneal surface", ["Posterior lens surface", "Retina", "Vitreous"], "The air-tear-cornea interface contributes the greatest refractive power."),
        q("The macula is responsible for", "Fine central vision", ["Aqueous formation", "Tear secretion", "Extraocular movement"], "The macula, especially fovea, mediates high-acuity central vision."),
        q("A patient with a tiny central retinal lesion has severe reading difficulty but preserved peripheral field. Which area is affected", "Macula", ["Ora serrata", "Ciliary body", "Inferior rectus"], "Macular disease selectively affects fine central vision.", True),
        q("During visual field testing, the normal blind spot corresponds anatomically to the", "Optic disc", ["Fovea", "Ora serrata", "Ciliary body"], "The optic nerve head lacks rods and cones and produces the physiological blind spot.", True),
        q("The ora serrata marks the anterior limit of the", "Retina", ["Cornea", "Lens", "Sclera"], "The sensory retina ends anteriorly at the ora serrata."),
        q("The extraocular muscle supplied by trochlear nerve is", "Superior oblique", ["Lateral rectus", "Medial rectus", "Inferior oblique"], "CN IV supplies superior oblique."),
        q("A patient has vertical diplopia worse while going downstairs. Which muscle is classically involved", "Superior oblique", ["Medial rectus", "Levator palpebrae superioris", "Orbicularis oculi"], "Superior oblique palsy causes vertical diplopia, worse on downgaze and adduction.", True),
        q("The lateral rectus muscle is supplied by", "Abducens nerve", ["Oculomotor nerve", "Trochlear nerve", "Facial nerve"], "CN VI innervates lateral rectus."),
        q("The embryological origin of retina is", "Neuroectoderm", ["Surface ectoderm", "Mesoderm", "Endoderm"], "The neural retina develops from the optic cup, a neuroectodermal derivative."),
        q("Congenital coloboma is due to failure of closure of the", "Embryonic fissure", ["Anterior fontanelle", "Hyaloid canal only", "Nasolacrimal duct"], "Failure of fetal fissure closure causes typical inferonasal coloboma.", True),
    ]),
    ("Physiology of Eye and Vision", [
        q("Aqueous humour is produced mainly by the", "Ciliary processes", ["Lens cortex", "Corneal epithelium", "Lacrimal gland"], "The ciliary epithelium secretes aqueous humour into the posterior chamber."),
        q("Normal aqueous humour flows from posterior chamber through pupil into", "Anterior chamber", ["Vitreous cavity", "Subretinal space", "Optic nerve sheath"], "Aqueous passes through the pupil before trabecular outflow."),
        q("A patient has acute painful red eye, mid-dilated pupil and high intraocular pressure. What mechanism is likely", "Pupillary block angle closure", ["Macular degeneration", "Simple myopia", "Optic neuritis"], "Blocked aqueous flow through the pupil can close the angle and raise IOP acutely.", True),
        q("In a glaucoma clinic, conventional aqueous outflow is assessed at the trabecular meshwork draining into", "Canal of Schlemm", ["Central retinal vein", "Nasolacrimal duct", "Vortex veins"], "Trabecular outflow reaches Schlemm canal and episcleral veins.", True),
        q("Accommodation for near vision requires ciliary muscle contraction and", "Increased lens convexity", ["Flattening of lens", "Pupil dilation only", "Retinal detachment"], "Ciliary contraction relaxes zonules, allowing the lens to become more convex."),
        q("A 48-year-old holds books farther away to read. What physiological change explains this", "Reduced lens elasticity", ["Increased corneal endothelium", "Retinal rod excess", "Superior oblique palsy"], "Presbyopia results from age-related loss of accommodative ability.", True),
        q("The photoreceptors responsible for scotopic vision are", "Rods", ["Cones", "Ganglion cells", "Bipolar cells only"], "Rods function in dim light and peripheral vision."),
        q("Colour vision and highest visual acuity depend mainly on", "Cones", ["Rods", "Amacrine cells only", "Schlemm canal"], "Cones are concentrated at the fovea and mediate colour and acuity."),
        q("A patient with vitamin A deficiency first complains of poor vision in dim light. Which cells are affected early", "Rods", ["Corneal endothelium", "Lens fibres", "Trabecular cells"], "Rhodopsin-dependent rod function is impaired early in vitamin A deficiency.", True),
        q("The visual cycle depends on regeneration of", "Rhodopsin", ["Melanin only", "Aqueous humour", "Myosin"], "Rhodopsin regeneration is necessary for rod phototransduction."),
        q("The fovea has maximum visual acuity because it contains densely packed", "Cones", ["Rods", "Mast cells", "Goblet cells"], "Cone density and one-to-one neural connections are highest at the fovea."),
        q("A patient has absent direct light reflex in the right eye when light is shone into that eye, but constriction occurs when light is shone into the left eye. The right-sided defect is in the", "Optic nerve", ["Facial nerve", "Trochlear nerve", "Abducens nerve"], "Light input travels through CN II to pretectal pathways.", True),
        q("A swinging flashlight test shows paradoxical dilation in one eye. What does this indicate", "Relative afferent pupillary defect", ["Facial nerve palsy", "Adie's tonic pupil always", "Complete third nerve palsy only"], "RAPD reflects asymmetric optic nerve or severe retinal dysfunction.", True),
        q("The efferent limb of pupillary constriction runs through", "Oculomotor nerve", ["Optic nerve", "Abducens nerve", "Trigeminal motor root"], "Parasympathetic fibres travel with CN III to ciliary ganglion and sphincter pupillae."),
        q("Corneal transparency is maintained mainly by regular collagen arrangement and endothelial", "Pump function", ["Melanin secretion", "Rod activity", "Tear drainage only"], "Endothelial dehydration of stroma is essential for clarity."),
        q("After intraocular surgery, corneal oedema occurs due to endothelial damage. What function is impaired", "Stromal deturgescence", ["Aqueous production", "Rod dark adaptation", "Eyelid closure"], "The corneal endothelium pumps fluid out of stroma to keep it dehydrated.", True),
        q("The tear film lipid layer is secreted mainly by", "Meibomian glands", ["Goblet cells", "Main lacrimal gland", "Zeis glands only"], "Meibomian secretion reduces evaporation of the tear film."),
        q("Goblet cells of conjunctiva contribute to the tear film by secreting", "Mucin", ["Aqueous", "Lipid", "Melanin"], "Mucin helps spread tears over the ocular surface."),
        q("A patient has dry eye with rapid tear break-up time. Which tear film layer is commonly deficient", "Lipid layer", ["Vitreous layer", "Retinal layer", "Lens capsule"], "Meibomian gland dysfunction causes evaporative dry eye and reduced TBUT.", True),
        q("Intraocular pressure is determined by the balance between aqueous production and", "Aqueous outflow", ["Rod density", "Lens colour", "Blink rate only"], "IOP reflects aqueous formation, outflow resistance and episcleral venous pressure."),
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
                "id": f"ophth-anat-phys-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ophthalmology anatomy physiology question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 40 ophthalmology anatomy and physiology questions.")


if __name__ == "__main__":
    main()
