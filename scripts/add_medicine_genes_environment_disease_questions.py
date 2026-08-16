import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Genes, the Environment, and Disease"
CHAPTER_ORDER = 16
SOURCE_PDF = "medicine 1"
TOPIC = "Genes, the Environment, and Disease"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def q(prompt, answer, wrong, explanation, clinical=False, page=None):
    return {
        "prompt": prompt.strip(),
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "high" if clinical else "moderate",
        "tags": ["clinical"] if clinical else [],
        "sourcePdfPageStart": page,
        "sourcePdfPageEnd": page,
    }


QUESTIONS = [
    q("Human genetics refers to the study of individual genes, their role in disease and their", "Mode of inheritance", ["Oxygen saturation only", "Dietary sodium content", "Radiographic density"], "Chapter 456 defines human genetics as the study of individual genes, their role and function in disease, and their inheritance.", page=3347),
    q("Genomics refers to an organism's entire genetic information and interaction of DNA with environmental or", "Nongenetic factors", ["Only serum enzymes", "Only infectious vectors", "Only radiographic contrast"], "Medicine 1 defines genomics as the genome plus DNA function and interaction with environmental or nongenetic factors such as lifestyle.", page=3347),
    q("Precision medicine aims at customizing medical decisions to", "An individual patient", ["A hospital budget", "A national average only", "A single chromosome only"], "Chapter 456 states that precision medicine aims to customize medical decisions to an individual patient.", page=3347),
    q("A patient's genotype is used to optimize drug dosing and predict adverse events. This application is called", "Pharmacogenomics", ["Cytogenetic drift", "Metagenesis", "Osmoregulation"], "Medicine 1 describes pharmacogenomics as using genetic characteristics to optimize drug therapy and predict efficacy, adverse events and dosing.", True, page=3347),
    q("Genetic abnormalities of DNA mismatch/repair include xeroderma pigmentosum, Bloom syndrome, ataxia telangiectasia and", "Hereditary nonpolyposis colon cancer", ["Acute mountain sickness", "Scombroid poisoning", "Myasthenia gravis"], "Chapter 456 lists HNPCC among DNA mismatch/repair abnormalities that predispose to neoplasia.", page=3350),
    q("Meiosis differs from mitosis by reducing chromosome number to the haploid state and generating diversity through", "Recombination", ["Pulmonary vasoconstriction", "Antibody neutralization", "Bone resorption"], "Medicine 1 notes that meiosis involves two divisions and active recombination that generates genetic diversity.", page=3350),
    q("Genomic imprinting silences methylated regions while unmethylated regions are", "Actively expressed", ["Always deleted", "Converted to RNA viruses", "Unable to replicate"], "Figure 456-8 describes unmethylated imprinted regions as active and methylated regions as silenced.", page=3355),
    q("A family pedigree shows affected individuals in successive generations, and one mutated allele is sufficient for disease. This pattern is", "Autosomal dominant inheritance", ["Autosomal recessive inheritance", "Mitochondrial depletion only", "Polygenic neutral variation"], "Chapter 456 states autosomal dominant disorders require mutation in a single allele and often affect successive generations.", True, page=3360),
    q("About what proportion of human monogenic disorders are autosomal dominant in Medicine 1?", "65%", ["5%", "25%", "100%"], "The Mendelian inheritance section states about 65% are autosomal dominant, 25% autosomal recessive and 5% X-linked.", page=3360),
    q("Genome-wide association studies of complex disorders are complicated by gene-gene and", "Gene-environment interactions", ["Airway intubation", "Snakebite identification", "Core rewarming"], "Chapter 456 notes that complex disorder analysis is complicated by locus heterogeneity, allele heterogeneity, gene-gene and gene-environment interactions, and phenocopies.", page=3365),
    q("A direct-to-consumer genetic test is offered without counseling. Medicine 1 raises concerns about validity, oversight, accuracy, confidentiality and", "Handling of results", ["Oxygen delivery only", "Activated charcoal dose", "Frostbite thawing temperature"], "Chapter 457 warns about direct-to-consumer genetic testing concerns including counseling and handling of results.", True, page=3369),
    q("A negative BRCA1/2 result from older testing must be qualified because comprehensive large genomic rearrangement testing was not commercially available until", "2006", ["1950", "1980", "2020"], "Medicine 1 uses BRCA1/2 testing to illustrate that older negative results may miss changes because comprehensive rearrangement testing became commercially available only in 2006.", page=3372),
    q("Identification of familial long QT syndrome allows early ECG testing and prophylactic antiarrhythmic therapy, pacemakers or", "Defibrillators", ["Chelation", "Fecal transplant", "Antivenom"], "Chapter 457 describes preventive interventions after identifying familial long QT syndrome, including defibrillators.", True, page=3375),
    q("ADA-SCID gene therapy improved after protocols used hematopoietic stem cells, stopped PEG-ADA at infusion and used mild", "Conditioning", ["Hypothermia", "Iodine loading", "Gastric lavage"], "Chapter 458 describes modifications that led to successful ADA-SCID gene therapy, including mild conditioning to aid engraftment.", True, page=3377),
    q("Fecal microbiota transplantation for recurrent Clostridium difficile infection has clinical cure rates of approximately", "85-90%", ["5-10%", "20-25%", "100% in all cases"], "Chapter 459 states that FMT is effective for recurrent CDI with clinical cure in 85-90% of patients.", page=3388),
]


def build_questions():
    if len(QUESTIONS) != 15:
        raise AssertionError(f"Expected 15 questions, got {len(QUESTIONS)}")
    if sum(1 for row in QUESTIONS if "clinical" in row.get("tags", [])) < 5:
        raise AssertionError("Expected at least 5 clinical questions")
    topic_slug = slugify(TOPIC)
    questions = []
    for question_order, row in enumerate(QUESTIONS, 1):
        questions.append({
            "id": f"medicine-genes-environment-disease-{topic_slug}-{question_order:02d}",
            "subjectId": SUBJECT_ID,
            "subjectTitle": SUBJECT_TITLE,
            "chapterTitle": CHAPTER,
            "chapterOrder": CHAPTER_ORDER,
            "topic": TOPIC,
            "topicTitle": TOPIC,
            "topicOrder": 1,
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
    if len({item["id"] for item in questions}) != 15:
        raise AssertionError("Duplicate genes/environment/disease question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 15 book-based Genes, the Environment, and Disease questions.")


if __name__ == "__main__":
    main()
