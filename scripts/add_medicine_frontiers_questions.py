import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Frontiers"
CHAPTER_ORDER = 20
SOURCE_PDF = "medicine 1"
TOPIC = "Frontiers"


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
    q("Behavioral economics broadens policy thinking by introducing costs individuals impose on themselves, termed", "Internalities", ["Externalities only", "Telomeropathies", "Epigenomes"], "Chapter 468 contrasts externalities with internalities, which are costs people impose on themselves through behavior.", page=3453),
    q("Loss aversion studies cited in Medicine 1 show ratios commonly in the range of", "1.5 to 2.5", ["0.1 to 0.2", "10 to 20", "50 to 100"], "Chapter 468 states that people often have a loss aversion ratio around 1.5-2.5.", page=3455),
    q("A hospital designs a quality program using penalties rather than equal-sized rewards because losses motivate more strongly than gains. This uses", "Loss aversion", ["Chromatin bivalency", "Horizontal gene transfer", "Circadian entrainment"], "Medicine 1 explains that penalties can be more motivating than equal rewards because of loss aversion.", True, page=3455),
    q("Medicine 1 cautions that health education alone often fails because knowledge rarely translates directly into", "Health-enhancing behavior", ["Genomic sequencing", "Telomere elongation", "Antibiotic susceptibility"], "Chapter 468 notes that better knowledge often does not translate into healthier behavior.", page=3458),
    q("The most widespread practitioner-based complementary health practice in the United States is", "Chiropractic care", ["Acupuncture only", "Ayurveda only", "Homeopathy only"], "Chapter 469 describes chiropractic as the most widespread practitioner-based complementary health practice in the United States.", page=3464),
    q("A patient asks where to find science-based information on herbs and supplements. Medicine 1 lists MedlinePlus and the NIH National Center for", "Complementary and Integrative Health", ["Network Medicine", "Viral Genomics", "Cardiac Surgery"], "Table 469-3 lists NCCIH as an NIH source for complementary health product and practice information.", True, page=3466),
    q("Dyskeratosis congenita has a mucocutaneous triad including reticular skin pigmentation, oral leukoplakia and", "Nail dystrophy", ["Blue sclera", "Cataracts", "Clubbing only"], "Chapter 470 figure 470-2 identifies the triad of reticular pigmentation, oral leukoplakia and nail dystrophy.", page=3468),
    q("Clinical presentation of telomere disease is highly variable in affected tissues, severity and", "Patterns within families", ["Only blood glucose", "Only snakebite site", "Only altitude reached"], "Medicine 1 states that telomere disease varies by tissue involvement, organ dysfunction severity and family patterns.", page=3468),
    q("Epigenetics describes mechanisms by which gene expression and phenotype are influenced independent of changes in the underlying", "DNA sequence", ["Blood pressure", "Protein intake", "Oxygen saturation"], "Chapter 471 defines epigenetics as phenotype and gene-expression changes independent of DNA sequence changes.", page=3471),
    q("Genes in embryonic stem cells may be bivalent, marked by activating H3K4me3 and repressive", "H3K27me3", ["HLA-B27", "AQP4-IgG", "BRCA1"], "Medicine 1 describes bivalent genes in embryonic stem cells as carrying H3K4me3 and H3K27me3 marks.", page=3473),
    q("A tumor of unknown origin is profiled. Medicine 1 notes chromatin landscape profiling may identify tissue of origin better than sequencing mutations alone. This uses", "Epigenome profiling", ["Activated charcoal", "Spirometry", "Gastric lavage"], "Chapter 471 states epigenome profiling of tumor chromatin can provide a strong index of tissue of origin.", True, page=3473),
    q("Corticosteroids in asthma treatment can recruit HDAC2 to promoters of NF-kappaB-stimulated inflammatory genes to prevent", "Activation", ["Methylation only", "Replication only", "Translation only"], "Chapter 471 describes corticosteroid recruitment of HDAC2 to repress NF-kappaB-stimulated inflammatory gene activation.", page=3476),
    q("Mitochondrial DNA replicates independently of cellular replication, so mtDNA copy number is not directly coordinated with the", "Cell cycle", ["Sleep cycle", "Menstrual cycle", "Urea cycle"], "Chapter 472 states mtDNA replication is independent and copy number is not directly coordinated with the cell cycle.", page=3478),
    q("A patient with common mitochondrial 12S rRNA m.A1555G mutation develops rapid hearing loss after normal-dose aminoglycoside exposure. This is an example of an", "Ecogenetic mutation", ["Externality", "Bivalent promoter", "Disease module"], "Medicine 1 describes m.A1555G as silent until aminoglycoside exposure, a classic ecogenetic example.", True, page=3478),
    q("In stem cell clinical applications, only which cells are adequately characterized by surface markers for unambiguous identification?", "Hematopoietic stem cells", ["Neurons", "Hepatocytes", "Pancreatic beta cells"], "Chapter 473 states only HSCs have been adequately characterized by surface markers for reliable clinical applications.", page=3491),
    q("A proposed stem cell therapy fails because transplanted cells cannot be tracked after infusion. Medicine 1 notes there is currently no way to image stem cells in vivo after transplantation into", "Humans", ["Cell culture only", "Bacteria", "Viruses"], "Chapter 473 lists lack of in vivo stem-cell imaging in humans as an obstacle.", True, page=3491),
    q("Molecular diagnostics can accelerate antimicrobial decisions by detecting genotypes that confer", "Resistance", ["Altitude tolerance", "Loss aversion", "Sleep hygiene"], "Chapter 474 states resistance-conferring genotypes can be targeted for molecular detection to guide therapy.", page=3497),
    q("Loss of bacterial CRISPR elements may facilitate genome invasion by foreign genetic material and adaptation as", "Nosocomial pathogens", ["Stem cells", "Telomeres", "Circadian clocks"], "Medicine 1 links CRISPR loss and mobile genetic material in Enterococcus to adaptation as nosocomial pathogens.", page=3500),
    q("Circadian rhythm sleep disorders share a mismatch between behavioral/physiologic rhythm and the external", "Light-dark cycle", ["DNA sequence", "Antibiotic target", "Tumor scaffold"], "Chapter 475 describes CRSDs as body-clock mismatch with environmental light-dark or social activity-rest cycles.", page=3508),
    q("A depressed patient is classified into an rsFC-defined biotype that predicts response to transcranial magnetic stimulation. This frontier technology uses resting-state", "Functional connectivity", ["Bone densitometry", "Pulmonary angiography", "Activated charcoal"], "Chapter 477 describes rsFC biomarkers for depression biotypes that may predict TMS response.", True, page=3525),
]


def build_questions():
    if len(QUESTIONS) != 20:
        raise AssertionError(f"Expected 20 questions, got {len(QUESTIONS)}")
    if sum(1 for row in QUESTIONS if "clinical" in row.get("tags", [])) < 6:
        raise AssertionError("Expected at least 6 clinical questions")
    topic_slug = slugify(TOPIC)
    questions = []
    for question_order, row in enumerate(QUESTIONS, 1):
        questions.append({
            "id": f"medicine-frontiers-{topic_slug}-{question_order:02d}",
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
    if len({item["id"] for item in questions}) != 20:
        raise AssertionError("Duplicate frontiers question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 20 book-based Frontiers questions.")


if __name__ == "__main__":
    main()
