import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Genetics"
CHAPTER_ORDER = 4
SOURCE_PDF = "physiology 1.pdf"
SOURCE_PAGE_START = 40
SOURCE_PAGE_END = 54

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
        "genetic-substrate",
        "STRUCTURAL AND FUNCTIONAL CHARACTERISTICS OF SUBSTRATE FOR GENETICS",
        1,
        [
            q(
                "Who coined the term chromosome for thread-like nuclear structures seen during division?",
                ["Waldeyer", "Mendel", "Morgan", "Watson"],
                0,
                "The source states that Waldeyer coined the term chromosomes in 1888.",
            ),
            q(
                "How many chromosomes are present in all dividing human body cells except gametes?",
                ["46 chromosomes", "23 chromosomes", "64 chromosomes", "30,000 chromosomes"],
                0,
                "Human dividing cells contain 46 chromosomes, arranged as 23 pairs; gametes contain 23.",
            ),
            q(
                "A karyotype shows a chromosome whose centromere divides it into two equal arms. Which morphological type is this?",
                ["Metacentric", "Submetacentric", "Acrocentric", "Telocentric"],
                0,
                "Metacentric chromosomes have a centromere that divides the chromosome into two equal arms.",
                clinical=True,
            ),
            q(
                "Which statement correctly describes DNA according to the chapter?",
                ["DNA is the molecule of inheritance and reserve bank of genetic information", "DNA is usually single stranded and contains uracil", "DNA is present only in ribosomes", "DNA obeys no base-pairing relationship"],
                0,
                "The source calls DNA the molecule of inheritance and reserve bank of genetic information.",
            ),
            q(
                "Chargaff's rule for DNA states which relationship?",
                ["A = T and G = C", "A = G and T = C", "A = U and G = T", "Purines are absent in DNA"],
                0,
                "Each DNA molecule has equal adenine and thymine residues and equal guanine and cytosine residues.",
            ),
            q(
                "Which feature belongs to the Watson-Crick B-DNA model?",
                ["Right-handed double helix with antiparallel chains", "Single-stranded clover leaf molecule", "Protein-only chromosome core", "RNA polymer with uracil instead of thymine"],
                0,
                "The chapter describes B-DNA as a right-handed double helix of two antiparallel polynucleotide chains.",
            ),
            q(
                "A human cell contains about 2 m of DNA packed into chromosomes by association with which proteins?",
                ["Histones", "Connexins", "Caspases", "Integrins"],
                0,
                "Human DNA associates with positively charged histone proteins; nucleosomes and solenoid fibres help package DNA.",
            ),
            q(
                "Which RNA type delivers amino acids for protein synthesis and resembles a clover leaf?",
                ["Transfer RNA", "Messenger RNA", "Ribosomal RNA", "Viral DNA"],
                0,
                "tRNA has a clover-leaf-like structure and delivers amino acids for protein synthesis.",
            ),
            q(
                "DNA replication is called semiconservative because:",
                ["Each new double helix retains one strand of the original DNA", "Both original strands are destroyed", "Only RNA is copied", "Each chromosome loses a chromatid"],
                0,
                "In semiconservative replication each newly formed double helix conserves one original DNA strand.",
            ),
            q(
                "A retrovirus such as HIV forms DNA from RNA. Which enzyme is responsible?",
                ["Reverse transcriptase", "DNA helicase", "RNA polymerase II", "Aminoacyl tRNA synthetase"],
                0,
                "The chapter states that reverse transcriptase forms DNA from RNA in retroviruses, including HIV.",
                clinical=True,
            ),
        ],
    ),
    (
        "applied-genetics",
        "APPLIED GENETICS",
        2,
        [
            q(
                "What is genetic engineering or recombinant DNA technology?",
                ["Insertion of desired genes from another organism into DNA", "Measurement of membrane potential", "Movement of water through a semipermeable membrane", "Fusion of vesicles during secretion"],
                0,
                "The source describes genetic engineering as adding desired genes from another organism to produce new combinations.",
            ),
            q(
                "PCR is mainly used to do what?",
                ["Amplify a small amount of DNA to large amounts", "Detect only proteins", "Measure osmotic pressure", "Separate chromosomes by centromere position"],
                0,
                "Polymerase chain reaction is described as a technique for amplifying small amounts of DNA.",
            ),
            q(
                "Which blotting technique detects a specific DNA sequence?",
                ["Southern blotting", "Northern blotting", "Western blotting", "Tissue culture"],
                0,
                "Southern blotting is used for DNA; the chapter lists DNA fingerprinting and mutant-gene detection as applications.",
            ),
            q(
                "A confirmatory test for HIV detects a specific protein after positive ELISA. Which technique is classically used?",
                ["Western blotting", "Southern blotting", "Northern blotting", "Chorionic villus sampling"],
                0,
                "The source states that Western blot identifies specific proteins and is widely used as a confirmatory HIV test.",
                clinical=True,
            ),
            q(
                "Which process is programmed cell death under genetic control?",
                ["Apoptosis", "Necrosis only", "Transduction", "Biolistics"],
                0,
                "Apoptosis is described as programmed cell death under genetic control, also called cell suicide.",
            ),
            q(
                "During fetal development, removal of web tissue between fingers and toes occurs mainly by which process?",
                ["Apoptosis", "PCR", "Southern blotting", "Gene amplification"],
                0,
                "The chapter gives removal of web tissue between fetal digits as an example of apoptosis in development.",
                clinical=True,
            ),
            q(
                "What is the final common pathway leading to apoptosis?",
                ["Activation of caspases", "Activation of Na+-K+ ATPase", "Opening of connexins", "Formation of solenoid fibres"],
                0,
                "The source identifies activation of cysteine proteases called caspases as the final common pathway of apoptosis.",
            ),
            q(
                "A mutation in which one base pair of DNA is replaced by another is called:",
                ["Point mutation", "Frame shift mutation", "Aneuploidy", "Transcytosis"],
                0,
                "Point mutation is defined as replacement of one DNA base pair by another.",
            ),
            q(
                "Prenatal genetic diagnosis can be performed by which technique listed in the chapter?",
                ["Chorionic villus sampling", "Western blot only", "Tissue culture of cosmetics", "Na+-glucose co-transport"],
                0,
                "Techniques of prenatal diagnosis listed include chorionic villus sampling, amniocentesis and pre-implantation diagnosis.",
                clinical=True,
            ),
            q(
                "In somatic cell gene therapy for cystic fibrosis of the lung, epithelial cells are made to produce which normal protein?",
                ["CFTR", "Factor VIII", "Phenylalanine hydroxylase", "c-myc"],
                0,
                "The source describes cystic fibrosis gene therapy using adenovirus vectors or liposomes so airway epithelial cells make normal CFTR.",
                clinical=True,
                difficulty="high",
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
                "id": f"physiology-genetics-{slug}-{index:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "options": options,
                "answerIndex": options.index(answer),
                "answer": answer,
            })
    return questions


def validate(questions):
    if len(TOPICS) != 2 or len(questions) != 20:
        raise ValueError("Expected 2 topics and 20 questions")
    if len({question["id"] for question in questions}) != len(questions):
        raise ValueError("Duplicate question ids")
    for _, topic, _, _ in TOPICS:
        topic_questions = [question for question in questions if question["topic"] == topic]
        clinical_count = sum("clinical" in question.get("tags", []) for question in topic_questions)
        if len(topic_questions) != 10:
            raise ValueError(f"{topic} must contain exactly 10 questions")
        if clinical_count < 2:
            raise ValueError(f"{topic} must contain at least 2 clinical questions")
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
