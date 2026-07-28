import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Membrane Potential"
CHAPTER_ORDER = 3
TOPIC = "Membrane Potential genesis and recording"
TOPIC_ORDER = 1
SOURCE_PDF = "physiology 1.pdf"
SOURCE_PAGE_START = 37
SOURCE_PAGE_END = 39

BASE = {
    "subjectId": "physiology",
    "subjectTitle": "Physiology",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "sourcePdf": SOURCE_PDF,
    "sourcePdfPageStart": SOURCE_PAGE_START,
    "sourcePdfPageEnd": SOURCE_PAGE_END,
    "chapterOrder": CHAPTER_ORDER,
    "topic": TOPIC,
    "topicTitle": TOPIC,
    "topicOrder": TOPIC_ORDER,
    "imageUrls": [],
}


def q(prompt, options, answer_index, explanation, clinical=False, difficulty="moderate"):
    return {
        "prompt": prompt,
        "options": options,
        "answerIndex": answer_index,
        "answer": options[answer_index],
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": ["clinical"] if clinical else [],
    }


QUESTIONS = [
    q(
        "What is meant by membrane potential in a living cell?",
        ["Potential difference across the cell membrane with inside usually negative", "Equal distribution of all ions across the membrane", "Absence of electrical charge in resting cells", "Only the ATP content of the plasma membrane"],
        0,
        "The source defines membrane potential as the potential difference across living cell membranes, with the inside negative in relation to outside.",
    ),
    q(
        "A resting nerve cell has a membrane potential of about -70 mV. What happens during excitation according to the source example?",
        ["It may become about +30 mV inside positive", "It remains exactly -70 mV", "It becomes 0 mV permanently", "It becomes -130 mV because calcium exits"],
        0,
        "The chapter gives nerve cell resting potential as about -70 mV and excited/action potential as about +30 mV.",
        clinical=True,
    ),
    q(
        "The term resting membrane potential means the cell is not undergoing which change?",
        ["Electrical change", "Metabolic activity", "Protein synthesis", "Ion distribution"],
        0,
        "The source clarifies that rest does not mean metabolic quiescence; it means the cell is not undergoing electrical change.",
    ),
    q(
        "The membrane potential measured during the excited state of a cell is called what?",
        ["Action potential", "Oncotic pressure", "Gibbs-Donnan ratio", "Osmolarity"],
        0,
        "The membrane potential during the excited state is called the action potential.",
    ),
    q(
        "Which is the basic reason for genesis of membrane potential?",
        ["Unequal distribution of ions across the cell membrane", "Equal movement of all proteins across the membrane", "Complete impermeability to sodium and potassium", "Absence of intracellular organic phosphate"],
        0,
        "Membrane potential is basically due to unequal ion distribution across the membrane, produced by combined forces acting on ions.",
    ),
    q(
        "Which set contains the factors listed for genesis of membrane potential?",
        ["Selective permeability, Gibbs-Donnan equilibrium, Nernst equation, GHK equation and Na+-K+ ATPase", "Only osmosis, pinocytosis and exocytosis", "Only ribosomes, lysosomes and Golgi apparatus", "Only oncotic pressure and plasma protein concentration"],
        0,
        "The chapter lists selective permeability, Gibbs-Donnan equilibrium, Nernst equation, constant field Goldmann equation and Na+-K+ ATPase pump.",
    ),
    q(
        "Which ions are described as diffusible ions in the selective permeability section?",
        ["Na+, K+, Cl- and HCO3-", "Only intracellular proteins", "Only organic phosphate", "Only ATP and ADP"],
        0,
        "Na+, K+, Cl- and HCO3- are listed as diffusible ions in this section.",
    ),
    q(
        "In resting membrane permeability, the membrane is freely permeable to which ions according to the source?",
        ["K+ and Cl-", "Na+ and Ca2+ only", "Intracellular proteins and phosphate", "Only glucose and urea"],
        0,
        "The source states the membrane is freely permeable to K+ and Cl- and moderately permeable to Na+.",
    ),
    q(
        "Why are intracellular proteins and organic phosphate important for membrane potential?",
        ["They are non-diffusible negatively charged ions", "They diffuse freely through sodium channels", "They are pumped out by Na+-K+ ATPase", "They directly open acetylcholine channels"],
        0,
        "The membrane is practically impermeable to intracellular proteins and organic phosphate, which are negatively charged non-diffusible ions.",
    ),
    q(
        "According to Gibbs-Donnan equilibrium, what must be true for each solution separated by a semipermeable membrane at equilibrium?",
        ["Each solution is electrically neutral", "One solution must carry only positive charge", "All ions become non-diffusible", "Only calcium determines equilibrium"],
        0,
        "Gibbs-Donnan equilibrium requires each solution to remain electrically neutral, with total cation charge equal to total anion charge.",
    ),
    q(
        "If non-diffusible anions are present on one side of a semipermeable membrane, what ion distribution is expected by Gibbs-Donnan equilibrium?",
        ["Asymmetrical distribution of diffusible ions", "Perfectly equal Na+ and Cl- on both sides", "No effect on diffusible ions", "Only chloride becomes non-diffusible"],
        0,
        "With non-diffusible anions on one side, Gibbs-Donnan equilibrium produces asymmetrical distribution of diffusible ions.",
    ),
    q(
        "The Nernst equation is used to calculate which value?",
        ["Equilibrium potential for an individual ion", "Total body water", "Osmotic pressure of plasma proteins", "Rate of exocytosis"],
        0,
        "The source states that the magnitude of equilibrium potential for an ion can be determined by the Nernst equation.",
    ),
    q(
        "For a mammalian spinal motor neuron in the table, what is the equilibrium potential for sodium?",
        ["+60 mV", "-90 mV", "-70 mV", "+130 mV"],
        0,
        "Table 1.4-1 lists sodium equilibrium potential as +60 mV.",
    ),
    q(
        "For a mammalian spinal motor neuron in the table, what is the equilibrium potential for potassium?",
        ["-90 mV", "+60 mV", "-70 mV", "+130 mV"],
        0,
        "Table 1.4-1 lists potassium equilibrium potential as -90 mV.",
    ),
    q(
        "For a mammalian spinal motor neuron in the table, which ion has an equilibrium potential of about +130 mV?",
        ["Ca2+", "K+", "Cl-", "Na+"],
        0,
        "Table 1.4-1 lists calcium equilibrium potential as +130 mV.",
    ),
    q(
        "Why is the Goldmann-Hodgkin-Katz equation needed in addition to the Nernst equation?",
        ["It accounts for Na+, K+ and Cl- distributions and their permeabilities together", "It calculates osmolarity from glucose alone", "It records membrane potential with electrodes", "It describes only vesicular transport"],
        0,
        "Nernst calculates one ion individually; GHK integrates Na+, K+ and Cl- distributions with their membrane permeabilities.",
    ),
    q(
        "In nerve and muscle fibres, which ions are most important for development of membrane potentials according to the GHK inference?",
        ["Sodium, potassium and chloride", "Calcium, magnesium and phosphate only", "Glucose, urea and protein", "Bicarbonate only"],
        0,
        "The GHK inferences state that Na+, K+ and Cl- are the most important ions for membrane potentials in nerve and muscle fibres.",
    ),
    q(
        "Signal transmission in nerves is primarily due to rapid changes in permeability of which ions?",
        ["Sodium and potassium", "Chloride and bicarbonate only", "Calcium and phosphate only", "Proteins and organic phosphate"],
        0,
        "The source states nerve signal transmission is primarily due to changes in sodium and potassium permeability during impulse conduction.",
        clinical=True,
    ),
    q(
        "What is the main role of Na+-K+ ATPase in membrane potential genesis according to this chapter?",
        ["Building and maintaining sodium and potassium concentration gradients", "Producing the entire membrane potential by itself", "Making the membrane impermeable to chloride", "Recording action potentials on an oscilloscope"],
        0,
        "Na+-K+ ATPase mainly builds concentration gradients by pumping back Na+ that diffuses in and K+ that diffuses out.",
    ),
    q(
        "A physiology practical asks for essential instruments used to record activity of excitable tissue. Which set is correct?",
        ["Microelectrodes, electronic amplifiers and cathode ray oscilloscope", "Stethoscope, sphygmomanometer and spirometer", "Spectrophotometer, centrifuge and pH meter", "ECG limb leads, tuning fork and ophthalmoscope"],
        0,
        "The chapter lists microelectrodes, electronic amplifiers and cathode ray oscilloscope as essential recording instruments.",
        clinical=True,
    ),
]


def build_questions():
    questions = []
    for index, row in enumerate(QUESTIONS, 1):
        option_shift = (TOPIC_ORDER + index) % 4
        options = row["options"][option_shift:] + row["options"][:option_shift]
        answer = row["answer"]
        questions.append({
            **BASE,
            **row,
            "id": f"physiology-membrane-potential-genesis-recording-{index:02d}",
            "options": options,
            "answerIndex": options.index(answer),
            "answer": answer,
        })
    return questions


def validate(questions):
    if len(questions) != 20:
        raise ValueError("Expected 20 questions")
    if len({question["id"] for question in questions}) != len(questions):
        raise ValueError("Duplicate question ids")
    if sum("clinical" in question.get("tags", []) for question in questions) < 3:
        raise ValueError("Expected at least 3 clinical questions")
    for question in questions:
        if len(question["options"]) != 4:
            raise ValueError(f"{question['id']} must contain 4 options")
        if question["answer"] != question["options"][question["answerIndex"]]:
            raise ValueError(f"{question['id']} has a bad answer mapping")
        if not question["explanation"] or len(question["explanation"]) < 30:
            raise ValueError(f"{question['id']} needs a stronger explanation")


def update_file(path, questions):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    new_ids = {question["id"] for question in questions}
    data["questions"] = [
        question
        for question in data.get("questions", [])
        if question.get("id") not in new_ids
    ] + questions
    data["questions"].sort(key=lambda item: item.get("id", ""))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    questions = build_questions()
    validate(questions)
    for path in DATA_PATHS:
        update_file(path, questions)
        print(f"Added {len(questions)} physiology questions to {path}.")
    print(f"- {TOPIC}: 20 questions")


if __name__ == "__main__":
    main()
