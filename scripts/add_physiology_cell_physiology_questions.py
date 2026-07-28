import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Cell Physiology"
CHAPTER_ORDER = 1
SOURCE_PDF = "physiology 1.pdf"
SOURCE_PAGE_START = 21
SOURCE_PAGE_END = 26

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
        "cell-structure",
        "CELL STRUCTURE",
        1,
        [
            q(
                "A typical cell seen by light microscopy is described as having three basic components. Which set is correct?",
                ["Cell membrane, cytoplasm and nucleus", "Cell wall, capsule and nucleoid", "Mitochondria, lysosomes and ribosomes only", "Cytoskeleton, glycocalyx and basal lamina"],
                0,
                "The source describes the typical cell as consisting of cell membrane, cytoplasm and nucleus.",
            ),
            q(
                "Which statement best defines the cell membrane in cell physiology?",
                ["It is a protective sheath that separates cell contents from the external environment", "It is the site of ribosomal RNA synthesis", "It is a temporary cytoplasmic inclusion", "It is the contractile protein of skeletal muscle"],
                0,
                "The plasma membrane envelops the cell body, separates intracellular from extracellular fluid and controls exchange.",
            ),
            q(
                "A skeletal muscle fibre requires rapid release and sequestration of calcium during contraction. Which organelle is modified for this function?",
                ["Smooth endoplasmic reticulum", "Golgi apparatus", "Primary lysosome", "Nucleolus"],
                0,
                "In skeletal and cardiac muscle, smooth ER is modified into sarcoplasmic reticulum for calcium release and sequestration.",
                clinical=True,
            ),
            q(
                "Which organelle is especially numerous in metabolically active cells because it is a major site of aerobic respiration?",
                ["Mitochondrion", "Centrosome", "Nucleolus", "Melanin granule"],
                0,
                "Mitochondria are major sites of aerobic respiration and are more numerous in metabolically active cells.",
            ),
            q(
                "A plasma cell has abundant Russell bodies and a pancreatic acinar cell actively synthesizes proteins. Which structure is expected to be well developed?",
                ["Rough endoplasmic reticulum", "Smooth endoplasmic reticulum", "Peroxisome", "Centrosome"],
                0,
                "Rough ER bears ribosomes and is well developed in cells active in protein synthesis, including plasma cells and pancreatic acinar cells.",
                clinical=True,
            ),
            q(
                "Which function is most directly associated with the Golgi apparatus?",
                ["Packaging proteins synthesized in rough ER into vesicles", "Oxidizing fatty acids in peroxisomes", "Moving chromosomes during cell division", "Forming actin and myosin microfilaments"],
                0,
                "The Golgi apparatus packages rough ER proteins into vesicles and also participates in secretion, glycosylation and lysosomal enzyme formation.",
            ),
            q(
                "A macrophage is engaged in phagocytosis and digestion of engulfed material. Which organelle is particularly abundant and functionally important?",
                ["Lysosome", "Centrosome", "Nucleolus", "Glycogen inclusion"],
                0,
                "Lysosomes contain hydrolytic enzymes and are abundant in phagocytic cells such as neutrophils and macrophages.",
                clinical=True,
            ),
            q(
                "Which cytoplasmic organelle contains oxidases and catalases and is prominent in hepatocytes and tubular epithelial cells?",
                ["Peroxisome", "Ribosome", "Centrosome", "Secretory granule"],
                0,
                "Peroxisomes contain oxidases and catalases and are described as predominant in hepatocytes and tubular epithelial cells.",
            ),
            q(
                "Which cytoskeletal element is composed of alpha- and beta-tubulin and forms a transport system for organelles and proteins?",
                ["Microtubule", "Intermediate filament", "Microfilament", "Glycocalyx"],
                0,
                "Microtubules are hollow structures made of alpha- and beta-tubulin and act as a cellular transport system.",
            ),
            q(
                "A patient has fragile skin with blistering due to abnormal mechanical integration of cell organelles. Which cytoskeletal structure is most consistent with this defect?",
                ["Intermediate filaments", "Mitochondrial cristae", "Nucleoli", "Peroxisomal oxidases"],
                0,
                "The source notes that abnormal intermediate filaments in humans are associated with skin blistering because cells rupture more easily.",
                clinical=True,
                difficulty="high",
            ),
        ],
    ),
    (
        "cell-membrane",
        "THE CELL MEMBRANE",
        2,
        [
            q(
                "Electron microscopy shows the plasma membrane as a trilayer unit membrane. What is its approximate total thickness?",
                ["7-10 nm", "15-20 nm", "25 nm", "40,270 nm"],
                0,
                "The source describes the cell membrane as a trilayer unit membrane with total thickness of 7-10 nm.",
            ),
            q(
                "What is the approximate biochemical composition of the cell membrane stated in the source?",
                ["Lipids 40%, proteins 55%, carbohydrates 5%", "Lipids 5%, proteins 40%, carbohydrates 55%", "Lipids 55%, proteins 5%, carbohydrates 40%", "Lipids 33%, proteins 33%, carbohydrates 33%"],
                0,
                "The membrane is described as a mixture of lipids 40%, proteins 55% and carbohydrates 5%.",
            ),
            q(
                "Which model of membrane structure was proposed by Singer and Nicholson in 1972?",
                ["Fluid mosaic model", "Unit crystal model", "Double helix model", "Sliding filament model"],
                0,
                "Singer and Nicholson proposed the fluid mosaic model of membrane structure.",
            ),
            q(
                "According to the fluid mosaic model, why can the plasma membrane tolerate considerable changes in cell shape?",
                ["Phospholipids are present in fluid form within a bilayer", "The membrane is made of rigid cellulose", "All membrane proteins are fixed permanently", "The glycocalyx replaces the lipid bilayer"],
                0,
                "Fluidity of the phospholipid bilayer makes the membrane flexible and helps preserve structural integrity during shape change.",
            ),
            q(
                "A lipid-soluble anesthetic rapidly crosses a cell membrane, while electrolytes cross poorly without channels. Which membrane feature explains this?",
                ["Hydrophobic lipid bilayer forms a major barrier to water-soluble molecules", "Nucleolus blocks fat-soluble substances", "Centrosomes pump electrolytes out", "Intermediate filaments form aqueous pores"],
                0,
                "The lipid bilayer is semipermeable: it restricts water-soluble molecules but allows fat-soluble substances like oxygen, fatty acids and alcohol to pass more easily.",
                clinical=True,
            ),
            q(
                "In the phospholipid bilayer, how are lipid molecules oriented?",
                ["Hydrophilic heads face extracellular and intracellular fluid, hydrophobic tails face the membrane centre", "Hydrophobic tails face water on both sides, hydrophilic heads face the centre", "All heads face only the cytoplasm", "All tails are exposed to extracellular fluid"],
                0,
                "Polar hydrophilic heads face the aqueous extracellular and intracellular phases; nonpolar hydrophobic tails point toward the centre.",
            ),
            q(
                "A hormone binds to a cell surface molecule and initiates intracellular physiologic change. Which membrane protein function is being used?",
                ["Receptor protein", "Channel protein", "Peripheral enzyme only", "Cytoskeletal anchor only"],
                0,
                "Some membrane proteins act as receptors for hormones and neurotransmitters, initiating intracellular changes.",
                clinical=True,
            ),
            q(
                "Which membrane proteins form active transport systems such as Na+-K+ ATPase, K+-H+ ATPase and Ca2+ pump?",
                ["Pump proteins", "Surface antigens", "Glycocalyx carbohydrates", "Cholesterol molecules"],
                0,
                "The source lists pumps as membrane proteins that form active transport systems, including Na+-K+ ATPase and Ca2+ pump.",
            ),
            q(
                "Which statement about peripheral extrinsic proteins is correct?",
                ["They are on the outer surface and can dissociate readily from the membrane", "They always cross the entire lipid bilayer", "They are the fatty acid tails of phospholipids", "They are found only inside mitochondria"],
                0,
                "Extrinsic or surface proteins are located on the outer surface and are not tightly associated with the membrane.",
            ),
            q(
                "A membrane carbohydrate defect reduces close fixation between adjacent epithelial cells. Which structure/function is most directly affected?",
                ["Glycocalyx-mediated cell fixation", "Mitochondrial ATP synthesis", "Nucleolar ribosomal RNA synthesis", "Centrosomal chromosome movement"],
                0,
                "Carbohydrates form the glycocalyx, which helps in tight fixation of cells with one another.",
                clinical=True,
                difficulty="high",
            ),
        ],
    ),
    (
        "intercellular-junctions",
        "INTERCELLULAR JUNCTIONS",
        3,
        [
            q(
                "Which are the three main types of intercellular junctions described in this chapter?",
                ["Tight junction, adherens junction and gap junction", "Synapse, neuromuscular junction and motor end plate", "Nucleolus, chromatin and chromosome", "Microtubule, microfilament and centrosome"],
                0,
                "The chapter classifies intercellular junctions into tight, adherens and gap junctions.",
            ),
            q(
                "A junction obliterates the space between neighbouring cells by fusion of outer layers of the cell membranes. What is it called?",
                ["Tight junction", "Gap junction", "Hemidesmosome", "Connexin channel"],
                0,
                "In tight junctions, the outer layers of neighbouring cell membranes fuse, obliterating the intercellular space.",
            ),
            q(
                "What is the main barrier function of tight junctions?",
                ["They block movement of ions and solutes from one cell to another", "They synthesize ribosomal RNA", "They generate ATP through Krebs cycle", "They move chromosomes during division"],
                0,
                "Tight junctions form a barrier to movement of ions and other solutes from one cell to another.",
            ),
            q(
                "A leaky epithelial barrier allows excessive paracellular movement of ions and solutes. Which junction is most likely functionally compromised?",
                ["Tight junction", "Nucleolus", "Peroxisome", "Centrosome"],
                0,
                "Because tight junctions normally restrict ion and solute movement between cells, their impairment can make an epithelial barrier leaky.",
                clinical=True,
            ),
            q(
                "In an adherens junction, what is the usual width of the space separating adjacent cell membranes?",
                ["15-20 nm", "2-3 nm", "7-10 nm", "1000 nm"],
                0,
                "The source describes adherens junctions as having adjacent membranes separated by a 15-20 nm space.",
            ),
            q(
                "Which adherens junction has thickened focal areas on both apposing cell membranes?",
                ["Desmosome", "Hemidesmosome", "Zona occludens", "Nexus"],
                0,
                "Desmosomes are adherens junctions with thickened focal areas on both apposing membranes.",
            ),
            q(
                "A blistering disorder involves failure of strong focal attachment between epidermal cells. Which junctional structure best matches this attachment mechanism?",
                ["Desmosome", "Gap junction", "Nuclear pore", "Glycocalyx only"],
                0,
                "Adherens junctions, including desmosomes, are described in epidermal cells and hold adjacent cells at focal places.",
                clinical=True,
            ),
            q(
                "What protein subunits surround each half-channel of a gap junction?",
                ["Six connexins", "Two tubulins", "Four spectrins", "Three cadherins"],
                0,
                "Each half of the gap junction channel is surrounded by six protein subunits called connexins.",
            ),
            q(
                "Gap junctions reduce the intercellular space to approximately what distance?",
                ["2-3 nm", "15-20 nm", "25 nm", "70-100 nm"],
                0,
                "At gap junctions, the intercellular space is reduced from the usual 15-20 nm to 2-3 nm.",
            ),
            q(
                "Rapid propagation of electrical potential changes from one cardiac muscle cell to another depends mainly on which junction?",
                ["Gap junction", "Tight junction", "Hemidesmosome", "Nuclear membrane"],
                0,
                "Gap junctions permit rapid propagation of electrical potential changes, as seen in cardiac muscle and smooth muscle.",
                clinical=True,
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
            item = {
                **BASE,
                **row,
                "id": f"physiology-cell-physiology-{slug}-{index:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "options": options,
                "answerIndex": options.index(answer),
                "answer": answer,
            }
            questions.append(item)
    return questions


def validate(questions):
    if len(TOPICS) != 3 or len(questions) != 30:
        raise ValueError("Expected 3 topics and 30 questions")
    if len({question["id"] for question in questions}) != len(questions):
        raise ValueError("Duplicate question ids")
    for slug, topic, _, _ in TOPICS:
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
