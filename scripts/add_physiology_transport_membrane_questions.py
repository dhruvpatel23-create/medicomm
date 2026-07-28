import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Transport Through Cell Membrane"
CHAPTER_ORDER = 2
SOURCE_PDF = "physiology 1.pdf"
SOURCE_PAGE_START = 27
SOURCE_PAGE_END = 36

BASE = {
    "subjectId": "physiology",
    "subjectTitle": "Physiology",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "sourcePdf": SOURCE_PDF,
    "sourcePdfPageStart": SOURCE_PAGE_START,
    "sourcePdfPageEnd": SOURCE_PAGE_END,
    "chapterOrder": CHAPTER_ORDER,
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


TOPICS = [
    (
        "passive-transport",
        "PASSIVE TRANSPORT",
        1,
        [
            q(
                "Which statement best defines passive transport across the cell membrane?",
                ["Movement along a gradient without energy expenditure", "Movement against a gradient using ATP directly", "Vesicular movement of macromolecules", "Protein synthesis on rough endoplasmic reticulum"],
                0,
                "The source defines passive transport as movement along concentration, electrical or pressure gradients without expenditure of energy.",
            ),
            q(
                "According to Fick's law, the rate of simple diffusion is directly proportional to which factor?",
                ["Concentration gradient and membrane area", "Membrane thickness only", "Molecular size only", "ATPase activity"],
                0,
                "Fick's law states that diffusion is directly proportional to concentration difference and area, and inversely proportional to membrane thickness.",
            ),
            q(
                "Which substance would diffuse rapidly through the lipid bilayer by simple diffusion?",
                ["Oxygen", "Glucose", "Sodium ion", "Plasma protein"],
                0,
                "Lipid soluble substances such as oxygen, nitrogen, carbon dioxide, alcohol and steroid hormones diffuse rapidly through the lipid bilayer.",
            ),
            q(
                "A nerve membrane loses its strong inside-negative charge and sodium gates open, causing sodium influx. Which channel behavior is being described?",
                ["Voltage-gated sodium channel opening", "Ligand-gated potassium channel closing", "Mechanical-gated chloride channel opening", "Carrier-mediated glucose uniport"],
                0,
                "Voltage-gated sodium channels open when the inside of the membrane loses its negative charge, producing marked sodium inflow.",
                clinical=True,
            ),
            q(
                "Acetylcholine opens a channel during transmission from a nerve cell to a muscle cell. What type of gating is this?",
                ["Ligand-gated channel", "Voltage-gated channel", "Pressure-gated pump", "Osmotic gate"],
                0,
                "The source gives acetylcholine channels as an important example of ligand or chemical gating.",
                clinical=True,
            ),
            q(
                "Glucose crosses many membranes by binding to a carrier protein that changes conformation. Which process is this?",
                ["Facilitated diffusion", "Simple diffusion through lipid bilayer", "Primary active transport", "Phagocytosis"],
                0,
                "Large water-soluble molecules such as glucose use carrier proteins and cross by facilitated diffusion.",
            ),
            q(
                "Which feature distinguishes facilitated diffusion from simple diffusion?",
                ["It shows saturation when carrier binding sites are fully occupied", "It has no specificity", "It always requires ATP hydrolysis", "It is independent of carrier proteins"],
                0,
                "Facilitated diffusion is carrier-mediated, specific, competitive and reaches a saturation point when carrier binding sites are occupied.",
            ),
            q(
                "Water moves through a semipermeable membrane from pure water into sodium chloride solution. What is this process called?",
                ["Osmosis", "Exocytosis", "Counter-transport", "Primary active transport"],
                0,
                "Osmosis is diffusion of water or solvent through a semipermeable membrane toward the solution with higher solute concentration.",
            ),
            q(
                "An RBC neither shrinks nor swells in 0.9% NaCl. How is this fluid classified with respect to plasma?",
                ["Isotonic", "Hypertonic", "Hypotonic", "Colloidal only"],
                0,
                "The source states that 0.9% NaCl is isotonic with plasma, so RBCs neither shrink nor swell.",
                clinical=True,
            ),
            q(
                "A patient with severe diabetes develops hyperosmolality and altered consciousness because water leaves brain cells. Which applied concept is this?",
                ["Hyperosmolar coma", "Hypotonic hemolysis", "Oncotic edema only", "Receptor-mediated endocytosis"],
                0,
                "The applied aspects note that increased glucose raises plasma osmolality and hyperosmolality can cause coma by drawing water out of brain cells.",
                clinical=True,
                difficulty="high",
            ),
        ],
    ),
    (
        "active-transport",
        "ACTIVE TRANSPORT",
        2,
        [
            q(
                "Which statement best defines active transport?",
                ["Movement against chemical or electrical gradient using energy", "Movement down a gradient without energy", "Vesicle fusion with the plasma membrane only", "Random thermal collision of lipid-soluble molecules"],
                0,
                "Active transport moves substances against chemical and/or electrical gradients and uses energy from high-energy compounds such as ATP.",
            ),
            q(
                "Which substances are listed as examples of actively transported ionic substances?",
                ["Na+, K+, Ca2+, Cl- and I-", "Oxygen and carbon dioxide only", "Steroid hormones only", "Albumin and fibrinogen"],
                0,
                "The source lists Na+, K+, Ca2+, Cl- and I- among ionic substances transported actively.",
            ),
            q(
                "In primary active transport, energy is derived directly from which source?",
                ["Breakdown of ATP or another high-energy phosphate compound", "Existing sodium concentration gradient only", "Osmotic pressure of plasma proteins", "Membrane lipid solubility"],
                0,
                "Primary active transport uses energy directly from ATP or other high-energy phosphate compounds.",
            ),
            q(
                "The Na+-K+ pump moves which ions in which direction during each cycle described in the source?",
                ["3 Na+ out and 2 K+ in", "2 Na+ out and 3 K+ in", "3 K+ out and 2 Na+ in", "1 Ca2+ in and 1 H+ out"],
                0,
                "Na+-K+ ATPase actively transports three sodium ions outward and two potassium ions inward.",
            ),
            q(
                "Why is the Na+-K+ pump described as electrogenic?",
                ["It produces net movement of positive charge out of the cell", "It moves equal positive charges in both directions", "It transports only neutral glucose", "It abolishes all membrane potential"],
                0,
                "Because it moves 3 Na+ out for 2 K+ in, the Na+-K+ pump causes a net positive charge movement outward and contributes to membrane potential.",
            ),
            q(
                "If the Na+-K+ pump fails, what major cellular consequence is expected according to the source?",
                ["Cells swell and may burst", "Cells immediately shrink in all fluids", "Ribosomes stop containing RNA", "Gap junctions become tight junctions"],
                0,
                "A key function of the Na+-K+ pump is control of cell volume; without it, most cells swell until they burst.",
                clinical=True,
            ),
            q(
                "The calcium pump maintains intracellular calcium at approximately what relation to extracellular calcium?",
                ["About 10,000 times lower than ECF", "Equal to ECF", "About 10,000 times higher than ECF", "Independent of ATPase activity"],
                0,
                "The calcium pump helps maintain intracellular calcium concentration about 10,000 times less than extracellular fluid.",
            ),
            q(
                "A drug inhibiting gastric parietal cell K+-H+ ATPase would directly target which transport process?",
                ["Primary active hydrogen ion transport", "Simple oxygen diffusion", "Glucose facilitated diffusion", "Receptor-mediated endocytosis"],
                0,
                "K+-H+ ATPase is a primary active transport system for hydrogen ions and is present in gastric parietal cells and renal tubules.",
                clinical=True,
            ),
            q(
                "In secondary active glucose transport, what must bind to the carrier before conformational change occurs?",
                ["Both sodium and glucose", "Only glucose", "Only potassium", "Only ATP on the inner surface"],
                0,
                "For sodium co-transport of glucose, the carrier changes conformation only when both sodium and glucose are attached.",
            ),
            q(
                "Renal tubular glucose reabsorption and intestinal glucose absorption use which mechanism described in this chapter?",
                ["Sodium co-transport", "Sodium-calcium counter-transport", "Phagocytosis", "Ligand-gated channel diffusion"],
                0,
                "The source states that glucose co-transport occurs during intestinal absorption and renal tubular reabsorption of glucose.",
                clinical=True,
            ),
        ],
    ),
    (
        "vesicular-transport",
        "VESICULAR TRANSPORT",
        3,
        [
            q(
                "Vesicular transport is mainly needed for which type of substance?",
                ["Macromolecules such as large protein molecules", "Only oxygen and carbon dioxide", "Only sodium and potassium ions", "Only steroid hormones"],
                0,
                "The source states that vesicular transport handles macromolecules, such as large proteins, that cannot cross by diffusion or active transport.",
            ),
            q(
                "Which processes are included under vesicular transport?",
                ["Endocytosis, exocytosis and transcytosis", "Simple diffusion, osmosis and filtration", "Uniport, symport and antiport only", "Voltage, ligand and mechanical gating only"],
                0,
                "Vesicular transport mechanisms include endocytosis, exocytosis and transcytosis.",
            ),
            q(
                "What is endocytosis?",
                ["Transport into the cell by infolding of the cell membrane around a substance", "Expulsion from the cell by vesicle fusion", "Movement of water down an osmotic gradient", "Exchange of sodium for calcium"],
                0,
                "Endocytosis transports substances into the cell by infolding the cell membrane around the substance and internalising it.",
            ),
            q(
                "Renal tubular epithelial cells engulf liquid substances during reabsorption. Which type of endocytosis is this?",
                ["Pinocytosis", "Phagocytosis", "Exocytosis", "Transcytosis"],
                0,
                "Pinocytosis, or cell drinking, refers to engulfing liquid substances and is exemplified by renal tubular epithelial reabsorption.",
                clinical=True,
            ),
            q(
                "A neutrophil engulfs bacteria and dead tissue. Which vesicular process is being used?",
                ["Phagocytosis", "Pinocytosis", "Transcytosis", "Facilitated diffusion"],
                0,
                "Phagocytosis, or cell eating, engulfs solid particles such as bacteria, dead tissue and foreign particles.",
                clinical=True,
            ),
            q(
                "Which sequence of steps is described for phagocytosis?",
                ["Attachment, engulfment, killing or degradation", "Binding, phosphorylation, dephosphorylation", "Vesicle formation, transportation, docking", "Osmosis, oncotic pressure, tonicity"],
                0,
                "The source describes phagocytosis in three steps: attachment, engulfment and killing or degradation.",
            ),
            q(
                "Iron and cholesterol enter cells by binding special surface receptors before internalisation. Which process is this?",
                ["Receptor-mediated endocytosis", "Simple diffusion through lipid", "Mechanical-gated diffusion", "Sodium counter-transport"],
                0,
                "The source lists iron and cholesterol transport into cells as examples of receptor-mediated endocytosis.",
                clinical=True,
            ),
            q(
                "What is exocytosis?",
                ["Expulsion of substances from the cell by vesicle fusion without passing through the membrane", "Engulfment of liquid by membrane infolding", "Water movement through a semipermeable membrane", "Carrier saturation during glucose diffusion"],
                0,
                "Exocytosis is the reverse of endocytosis: vesicle membranes fuse with the cell membrane and release contents outside while leaving the membrane intact.",
            ),
            q(
                "Release of hormones and enzymes by secretory cells occurs by which mechanism?",
                ["Exocytosis", "Simple diffusion", "Osmosis", "Sodium-hydrogen counter-transport"],
                0,
                "The chapter states that release of hormones and enzymes by secretory cells occurs by exocytosis.",
                clinical=True,
            ),
            q(
                "Which requirement is specifically mentioned for exocytosis?",
                ["Ca2+, energy and docking proteins", "Only osmotic pressure", "Only sodium gradient", "Only lipid solubility"],
                0,
                "The process of exocytosis requires calcium, energy and docking proteins.",
            ),
        ],
    ),
]


def build_questions():
    questions = []
    for slug, topic, topic_order, rows in TOPICS:
        for index, row in enumerate(rows, 1):
            option_shift = (topic_order + index) % 4
            options = row["options"][option_shift:] + row["options"][:option_shift]
            answer = row["answer"]
            questions.append({
                **BASE,
                **row,
                "id": f"physiology-transport-membrane-{slug}-{index:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "options": options,
                "answerIndex": options.index(answer),
                "answer": answer,
            })
    return questions


def validate(questions):
    if len(TOPICS) != 3 or len(questions) != 30:
        raise ValueError("Expected 3 topics and 30 questions")
    if len({question["id"] for question in questions}) != len(questions):
        raise ValueError("Duplicate question ids")
    for _, topic, _, _ in TOPICS:
        topic_questions = [question for question in questions if question["topic"] == topic]
        clinical_count = sum("clinical" in question.get("tags", []) for question in topic_questions)
        if len(topic_questions) != 10:
            raise ValueError(f"{topic} must contain exactly 10 questions")
        if clinical_count < 3:
            raise ValueError(f"{topic} must contain at least 3 clinical questions")
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
    for _, topic, _, _ in TOPICS:
        print(f"- {topic}: 10 questions")


if __name__ == "__main__":
    main()
