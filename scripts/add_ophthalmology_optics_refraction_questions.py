import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "ophthalmology"
SUBJECT_TITLE = "Ophthalmology"
CHAPTER = "Optics and Refraction"
CHAPTER_ORDER = 2
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
    ("Elementary and Physiological Optics", [
        q("The unit of refractive power of a lens is", "Dioptre", ["Candela", "Lux", "Prism dioptre only"], "Dioptre is the reciprocal of focal length in metres."),
        q("A convex lens is also called a", "Plus lens", ["Minus lens", "Plano lens", "Cylindrical axis"], "Convex lenses converge light and have positive power."),
        q("A patient is prescribed a +2.00 D lens. What is its focal length", "50 cm", ["25 cm", "100 cm", "2 cm"], "Focal length in metres is 1 divided by dioptric power; 1/2 = 0.5 m.", True),
        q("A concave lens causes incident parallel rays to", "Diverge", ["Converge", "Remain focused on retina always", "Become polarized only"], "Minus lenses diverge light rays."),
        q("The principal focus of a convex lens is the point where parallel rays", "Converge after refraction", ["Appear to diverge before refraction", "Reflect from lens surface", "Enter optic nerve"], "A convex lens brings parallel rays to a real focus."),
        q("A child uses a strong convex magnifier to read small print. Which optical action is being used", "Convergence of rays", ["Divergence of rays", "Absorption of all blue light", "Rotation of image only"], "Convex lenses magnify by converging light and forming an enlarged image.", True),
        q("Prism power is measured in", "Prism dioptres", ["Spherical dioptres", "Candela", "Millimetres of mercury"], "A prism dioptre displaces an image by 1 cm at 1 m."),
        q("The apex of a prism deviates light toward its", "Base", ["Apex", "Optical centre", "Nodal point only"], "Light passing through a prism bends toward the base."),
        q("A patient with diplopia is given a prism. The image is displaced toward the", "Apex of the prism", ["Base of the prism", "Retina only", "Corneal limbus"], "Prisms bend rays toward base, so the perceived image shifts toward apex.", True),
        q("The optical centre of a spherical lens is the point through which a ray passes", "Undeviated", ["With maximum deviation", "With total reflection", "Only after accommodation"], "A ray through the optical centre does not deviate significantly."),
        q("Chromatic aberration occurs because different wavelengths have different", "Refractive indices", ["Retinal blood supply", "Accommodation amplitudes", "Tear secretion rates"], "Shorter and longer wavelengths refract differently."),
        q("A patient notices blur from peripheral rays through a large pupil. This optical defect occurs because peripheral rays focus differently from", "Paraxial rays", ["Sound waves", "Tear film lipid", "Eyelid margin"], "Peripheral and central rays do not share the same focus in spherical aberration.", True),
        q("After dilated retinal examination, a patient complains of glare and blurred near vision. Which physiological function was blocked", "Accommodation and pupillary constriction", ["Rod regeneration only", "Tear secretion only", "Corneal endothelial pump only"], "Cycloplegic mydriatics relax accommodation and dilate the pupil.", True),
        q("The reduced eye is a simplified optical model in which ocular refracting surfaces are treated as", "One equivalent refracting surface", ["Four separate retinas", "No refracting surface", "Only the eyelid"], "Reduced-eye models simplify calculations of image formation."),
        q("The approximate total refractive power of the emmetropic eye is", "60 dioptres", ["6 dioptres", "120 dioptres", "1 dioptre"], "The eye has about 60 D of total refractive power, mainly from the cornea."),
        q("A small pupil improves image clarity by reducing", "Spherical aberration", ["Aqueous production", "Retinal circulation", "Lens nutrition"], "A smaller aperture blocks peripheral rays and increases depth of focus.", True),
        q("Visual acuity depends most on image formation at the", "Fovea", ["Optic disc", "Ora serrata", "Ciliary body"], "Foveal cone packing and precise optics give best acuity."),
        q("A patient reads more letters on the chart through a pinhole. The pinhole improves vision by", "Reducing blur circles", ["Increasing cataract opacity", "Paralyzing accommodation", "Stimulating rods only"], "A pinhole admits central rays and reduces retinal blur.", True),
        q("A patient with blurred distance vision improves markedly with pinhole. What does this suggest", "Refractive error", ["Dense optic atrophy always", "Complete retinal detachment", "Endophthalmitis"], "Pinhole improvement points to an optical focusing problem.", True),
        q("The far point of an emmetropic eye is at", "Infinity", ["25 cm", "1 m", "Behind the lens only"], "An emmetropic relaxed eye focuses parallel rays from infinity on the retina."),
    ]),
    ("Errors of Refraction and Accommodation", [
        q("In myopia, parallel rays focus", "In front of the retina", ["Behind the retina", "On the optic disc only", "At the corneal epithelium"], "Myopia is caused by excessive refractive power or long axial length."),
        q("Myopia is corrected with", "Concave lenses", ["Convex lenses", "Plano prisms", "Cylindrical lenses only"], "Minus lenses diverge rays so the focus moves backward onto the retina."),
        q("A 14-year-old sees near objects clearly but cannot read the classroom board. Which refractive error is likely", "Myopia", ["Hypermetropia", "Presbyopia", "Aphakia"], "Myopes have poor distance vision and relatively good near vision.", True),
        q("In hypermetropia, parallel rays focus", "Behind the retina", ["In front of the retina", "At the vitreous base", "On the iris"], "Hypermetropia reflects insufficient power or short axial length."),
        q("Hypermetropia is corrected with", "Convex lenses", ["Concave lenses", "Prisms only", "Occluders"], "Plus lenses converge rays and bring focus forward onto the retina."),
        q("A young hypermetrope may maintain clear distance vision by using", "Accommodation", ["Divergence excess", "Loss of lens elasticity", "Retinal detachment"], "Accommodation can compensate latent hypermetropia in children and young adults.", True),
        q("Astigmatism occurs when refractive power differs in different", "Meridians", ["Retinal vessels", "Eyelashes", "Optic nerve fibres only"], "Unequal curvature in different meridians produces line foci."),
        q("Regular astigmatism is corrected with", "Cylindrical lenses", ["Spherical lenses only", "Opaque lenses", "No optical correction possible"], "A cylinder lens neutralizes power in a specific meridian."),
        q("A patient sees vertical lines clearer than horizontal lines on fan chart. What refractive error is being assessed", "Astigmatism", ["Presbyopia only", "Night blindness", "Colour blindness"], "Fan charts help detect meridional blur in astigmatism.", True),
        q("A child has markedly different spectacle powers in the two eyes. This refractive condition is called", "Anisometropia", ["Isometropia", "Presbyopia", "Aphakia"], "A significant interocular refractive difference can cause aniseikonia and amblyopia.", True),
        q("Amblyopia can develop in childhood due to uncorrected high", "Anisometropia", ["Presbyopia", "Physiological astigmatism in adults only", "Pseudomyopia only"], "Unequal blur during visual development can suppress one eye."),
        q("A 5-year-old has one eye with high hypermetropia and poor vision despite normal fundus. What is the likely cause", "Anisometropic amblyopia", ["Presbyopia", "Retinal detachment", "Acute glaucoma"], "Unilateral high refractive error can produce amblyopia if not corrected early.", True),
        q("Presbyopia is caused by age-related reduction in", "Accommodation", ["Corneal transparency only", "Aqueous outflow only", "Rod count only"], "Loss of lens elasticity reduces accommodative amplitude."),
        q("Presbyopia is corrected using", "Plus lenses for near", ["Minus lenses for near", "Prisms for all patients", "No lens ever"], "Near add lenses compensate for reduced accommodation."),
        q("A 45-year-old with previously normal vision develops difficulty reading fine print at near. What is the likely diagnosis", "Presbyopia", ["Myopia", "Colour blindness", "Keratoconus"], "Age-related loss of accommodation produces near blur.", True),
        q("Aphakia causes marked", "Hypermetropia", ["Myopia", "Emmetropia always", "Astigmatism only"], "Removal of the crystalline lens greatly reduces ocular refractive power."),
        q("Pseudophakia means the eye has", "Intraocular lens implant", ["No lens", "Only contact lens", "Retinal prosthesis"], "Pseudophakia refers to an artificial intraocular lens after cataract surgery."),
        q("After cataract surgery without IOL implantation, a patient needs thick plus glasses. What refractive state is present", "Aphakia", ["Myopia", "Astigmatic fan error", "Cycloplegia only"], "Aphakia produces high hypermetropia requiring strong plus correction.", True),
        q("A child suspected of hidden hypermetropia is examined after cycloplegic drops. Cycloplegic refraction reveals", "Latent hypermetropia", ["Retinal tear", "Optic disc oedema", "Vitreous haemorrhage"], "Cycloplegia relaxes accommodation and uncovers hidden hypermetropia.", True),
        q("Spasm of accommodation can produce", "Pseudomyopia", ["Aphakia", "Absolute hypermetropia only", "Presbyopia in infancy"], "Excess accommodation temporarily shifts focus anteriorly and mimics myopia."),
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
                "id": f"ophth-optics-refraction-{topic_slug}-{question_order:02d}",
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
        raise AssertionError("Duplicate ophthalmology optics refraction question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    if any(item["prompt"][-1] not in ".?!:" for item in questions):
        raise AssertionError("Prompt without terminal punctuation found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 40 ophthalmology optics and refraction questions.")


if __name__ == "__main__":
    main()
