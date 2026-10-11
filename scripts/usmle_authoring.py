"""Shared schema helpers for source-audited integrated USMLE teaching blocks."""
from copy import deepcopy
import random


BOOKS = {
    "robbins": ("Robbins & Cotran Pathologic Basis of Disease", "10th ed."),
    "bio": ("Vasudevan, Sreekumari & Vaidyanathan: Textbook of Biochemistry for Medical Students", "6th ed."),
    "goodman": ("Goodman & Gilman's The Pharmacological Basis of Therapeutics", "14th ed."),
    "micro": ("Sastry & Bhat: Essentials of Medical Microbiology", "4th ed."),
    "head": ("B. D. Chaurasia's Human Anatomy, Volume 3", "6th ed."),
    "limb": ("B. D. Chaurasia's Human Anatomy, Volume 2", "6th ed."),
}


def ref(book, chapter, pdf_pages):
    title, edition = BOOKS[book]
    return {"book": title, "edition": edition, "chapter": chapter, "pdfPages": pdf_pages}


def web_ref(book, edition, chapter, url):
    return {"book": book, "edition": edition, "chapter": chapter, "url": url}


def lab(test, value, reference):
    return {"test": test, "value": value, "reference": reference}


def item(number, disciplines, system, topic, proposition, prompt, lead_in,
         choices, explanation, objective, reasoning, references,
         family="mechanism", labs=None):
    """Draft choices as (key first, then distractors); shuffle paired notes at finalization."""
    assert len(choices) == 5 and references
    return {
        "questionNumber": number, "disciplines": disciplines, "organSystem": system,
        "topic": topic, "sourceProposition": proposition, "prompt": prompt,
        "leadIn": lead_in, "options": [c[0] for c in choices],
        "optionExplanations": [c[1] for c in choices], "answerIndex": 0,
        "answer": choices[0][0], "explanation": explanation,
        "educationalObjective": objective, "reasoningChain": reasoning,
        "references": references, "itemFamily": family, "difficulty": "integrated",
        "laboratoryFindings": labs or [], "imageUrls": [],
        "reviewStatus": "Author source audit completed; independent physician review pending",
    }


def finalize(module_number, drafts, revision=None):
    assert len(drafts) == 15
    questions = deepcopy(drafts)
    rng = random.Random(20261009 + module_number)
    # Balanced, reproducible key positions, shuffled only after the drafts are complete.
    positions = list(range(5)) * 3
    rng.shuffle(positions)
    for number, (q, key_position) in enumerate(zip(questions, positions), 1):
        assert q["questionNumber"] == number
        pairs = list(zip(q["options"], q["optionExplanations"]))
        key = pairs.pop(0)
        rng.shuffle(pairs)
        pairs.insert(key_position, key)
        module_id = f"usmle-module-{module_number:02d}"
        q.update({
            "id": f"{module_id}{f'-v{revision}' if revision else ''}-q{number:03d}", "moduleId": module_id,
            "subjectId": module_id, "subjectTitle": f"Module {module_number}",
            "examId": "usmle-step-1", "examTitle": "USMLE Step 1 - Integrated Practice",
            "source": "usmle", "answerIndex": key_position,
            "options": [p[0] for p in pairs], "optionExplanations": [p[1] for p in pairs],
            "tags": ["usmle-step-1", "integrated", f"module-{module_number}",
                     *[d.lower().replace(" ", "-") for d in q["disciplines"]]],
        })
    return questions
