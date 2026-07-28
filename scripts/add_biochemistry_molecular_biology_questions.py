import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Molecular Biology"
BASE = {"subjectId": "biochemistry", "subjectTitle": "Biochemistry", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}

STD = [
    "Which option best completes this molecular biology statement: {clue}?",
    "What is the most appropriate answer for: {clue}?",
    "Which molecule, enzyme or concept is most directly associated with: {clue}?",
    "Why is this point important in molecular biology: {clue}?",
    "Which interpretation is best for this finding: {clue}?",
    "How should this be classified in an exam question: {clue}?",
    "Which choice is the best single association for: {clue}?",
    "What does this source-book detail most strongly indicate: {clue}?",
    "Which statement is correct regarding: {clue}?",
    "How is this clue best applied in genetics or biotechnology: {clue}?",
]
UNQ = [
    "A genetics viva gives only this hint: '{clue}'. Choose the expected answer.",
    "Match the molecular-biology clue with the correct term: {clue}.",
    "A DNA/RNA pathway diagram has a blank beside '{clue}'. Which label fits?",
    "Assertion-reason style: the assertion depends on '{clue}'. Select the correct reason.",
    "A final-year MCQ uses this practical clue: '{clue}'. What is the best answer?",
]
ORDER = [("s",0),("s",1),("u",0),("s",2),("s",3),("s",4),("u",1),("s",5),("s",6),("u",2),("s",7),("s",8),("u",3),("s",9),("u",4)]

def q(clue, answer, wrong, explanation):
    return {"clue": clue, "answer": answer, "wrong": wrong, "explanation": explanation}

TOPICS = [
("nucleotides", "Nucleotides: Chemistry and Metabolism", [
q("nucleotide contains nitrogenous base, pentose sugar and phosphate", "three-component structure of nucleotide", ["base and amino acid only", "fatty acid and glycerol", "protein and heme"], "Nucleotides consist of base, sugar and phosphate."),
q("base plus pentose sugar without phosphate is called", "nucleoside", ["nucleotide", "nucleic acid", "nucleosome"], "A nucleoside is base plus sugar."),
q("nucleoside esterified with phosphate is called", "nucleotide", ["nucleoside", "nucleoprotein", "nucleosome"], "Adding phosphate converts a nucleoside to nucleotide."),
q("adenine and guanine are", "purines", ["pyrimidines", "pentoses", "nucleosides only"], "Adenine and guanine are purine bases."),
q("cytosine, thymine and uracil are", "pyrimidines", ["purines", "nucleotides only", "pentoses"], "C, T and U are pyrimidines."),
q("ATP functions as this in metabolism", "universal energy currency", ["DNA repair enzyme", "ribosomal structural protein", "restriction enzyme"], "ATP is a nucleotide derivative and energy carrier."),
q("NAD+ and FAD contain nucleotide components", "coenzyme role of nucleotides", ["fiber role", "lipoprotein role", "albumin role"], "Nucleotides are components of important coenzymes."),
q("cAMP and cGMP act mainly as", "metabolic regulators", ["storage polysaccharides", "essential fatty acids", "structural collagen"], "Cyclic nucleotides are signaling molecules."),
q("de novo purine synthesis builds purine ring on this sugar phosphate", "PRPP", ["free thymine", "cholesterol", "glycogen"], "Purine ring is assembled on PRPP."),
q("final degradation product of purines in humans", "uric acid", ["urea", "creatinine", "bilirubin"], "Purine degradation ends as uric acid in humans."),
q("hyperuricemia with urate crystal deposition causes", "gout", ["phenylketonuria", "galactosemia", "scurvy"], "Gout is due to urate crystal deposition."),
q("allopurinol inhibits this enzyme in purine degradation", "xanthine oxidase", ["DNA ligase", "RNA polymerase", "aminoacyl synthetase"], "Allopurinol lowers uric acid by inhibiting xanthine oxidase."),
q("pyrimidine ring is synthesized before attachment to ribose phosphate", "de novo pyrimidine synthesis", ["de novo purine synthesis", "DNA replication", "translation"], "Pyrimidine synthesis makes the ring first."),
q("orotic aciduria is related to disordered synthesis of", "pyrimidines", ["purines", "fatty acids", "bile acids"], "Orotic aciduria is a pyrimidine synthesis disorder."),
q("nucleotides are precursors of DNA and RNA", "nucleic acid synthesis", ["lipid storage", "protein digestion", "bile salt formation"], "DNA and RNA are nucleotide polymers."),
]),
("dna", "DNA Structure and Replication", [
q("Avery demonstrated the genetic material in 1944", "DNA", ["protein", "RNA primer", "ribosomal RNA"], "Avery's experiment established DNA as genetic material."),
q("Watson and Crick proposed this DNA structure", "double helix", ["triple helix", "beta sheet", "single random coil"], "Watson and Crick described the double helix."),
q("Chargaff rule states adenine pairs with", "thymine", ["guanine", "cytosine", "uracil"], "A pairs with T in DNA."),
q("Chargaff rule states guanine pairs with", "cytosine", ["thymine", "uracil", "adenine"], "G pairs with C."),
q("DNA strands run in this orientation", "antiparallel", ["parallel", "nonpolar", "branched"], "DNA strands run opposite directions."),
q("DNA backbone is linked by", "3'-5' phosphodiester bonds", ["peptide bonds", "disulfide bonds", "hydrogen bonds only"], "Phosphodiester bonds form the backbone."),
q("DNA replication is called this because each daughter duplex retains one parental strand", "semiconservative", ["conservative", "dispersive only", "random"], "Replication is semiconservative."),
q("enzyme that unwinds DNA at replication fork", "helicase", ["ligase", "primase", "RNA polymerase"], "Helicase separates DNA strands."),
q("enzyme relieving supercoils ahead of fork", "topoisomerase", ["DNA ligase", "peptidyl transferase", "restriction enzyme"], "Topoisomerase relieves torsional stress."),
q("short RNA segment needed to initiate DNA synthesis", "RNA primer", ["poly-A tail", "promoter", "anticodon"], "DNA polymerase requires a primer."),
q("new DNA is synthesized in this direction", "5' to 3'", ["3' to 5'", "N to C", "C to N"], "DNA polymerase synthesizes 5' to 3'."),
q("short discontinuous fragments on lagging strand", "Okazaki fragments", ["introns", "exons", "codons"], "Lagging strand forms Okazaki fragments."),
q("enzyme joining Okazaki fragments", "DNA ligase", ["helicase", "primase", "telomerase"], "Ligase seals DNA nicks."),
q("UV light commonly causes this DNA lesion", "thymine dimers", ["uracil dimers", "peptide breaks", "glycogen branches"], "UV forms pyrimidine dimers."),
q("defect in nucleotide excision repair causes", "xeroderma pigmentosum", ["sickle cell anemia", "phenylketonuria", "gout"], "XP is due to defective UV-damage repair."),
]),
("transcription-translation", "Transcription and Translation", [
q("RNA contains this sugar", "ribose", ["deoxyribose", "glucose", "galactose"], "RNA contains ribose."),
q("RNA uses this base instead of thymine", "uracil", ["adenine", "guanine", "cytosine"], "RNA contains uracil."),
q("RNA type carrying genetic message from DNA", "mRNA", ["rRNA", "tRNA", "snRNA"], "mRNA carries coding message."),
q("most abundant RNA in cell", "rRNA", ["mRNA", "tRNA", "hnRNA"], "rRNA is the major RNA fraction."),
q("RNA carrying amino acids to ribosome", "tRNA", ["mRNA", "rRNA", "miRNA"], "tRNA brings amino acids."),
q("DNA-directed RNA synthesis is called", "transcription", ["translation", "replication", "splicing"], "Transcription makes RNA."),
q("enzyme responsible for RNA synthesis", "RNA polymerase", ["DNA ligase", "helicase", "aminoacyl synthetase"], "RNA polymerase synthesizes RNA."),
q("5' end modification of eukaryotic mRNA", "7-methylguanosine cap", ["poly-A removal", "anticodon addition", "Okazaki fragment"], "mRNA receives a 5' cap."),
q("removal of introns from hnRNA", "splicing", ["translation", "replication", "translocation"], "Splicing removes introns."),
q("enzyme that synthesizes DNA from RNA template", "reverse transcriptase", ["DNA ligase", "RNA polymerase I", "peptidyl transferase"], "Reverse transcriptase makes DNA from RNA."),
q("genetic code is read as groups of", "triplet codons", ["doublet codons", "single bases", "quadruplets"], "Codons are triplets."),
q("AUG codes for this amino acid and start signal", "methionine", ["tryptophan", "lysine", "glycine"], "AUG initiates translation and codes methionine."),
q("UAA, UAG and UGA are", "stop codons", ["start codons", "anticodons", "introns"], "These terminate translation."),
q("protein synthesis from mRNA is called", "translation", ["transcription", "replication", "reverse transcription"], "Translation synthesizes protein."),
q("tetracycline blocks bacterial translation by preventing", "aminoacyl tRNA binding to ribosome", ["DNA ligation", "mRNA capping", "telomere extension"], "Tetracycline inhibits aminoacyl-tRNA entry."),
]),
("inheritance-gene-expression", "Inheritance, Mutations and Control of Gene Expression", [
q("Mendel described these", "principles of heredity", ["restriction enzymes", "PCR cycles", "RNA caps"], "Mendel described inheritance laws."),
q("trait expressed in heterozygote", "dominant", ["recessive", "silent", "linked only"], "Dominant traits show with one allele."),
q("trait expressed only when both alleles are affected", "recessive", ["dominant", "codominant only", "polygenic"], "Recessive traits require two affected alleles."),
q("phenylketonuria is classically", "autosomal recessive", ["autosomal dominant", "mitochondrial", "Y-linked"], "PKU is autosomal recessive."),
q("mutation changing one amino acid codon to another", "missense mutation", ["nonsense mutation", "silent mutation", "frameshift"], "Missense changes amino acid."),
q("mutation creating a stop codon", "nonsense mutation", ["missense mutation", "silent mutation", "splice mutation"], "Nonsense creates termination codon."),
q("insertion or deletion not in multiples of three", "frameshift mutation", ["silent mutation", "transition only", "transversion only"], "Frameshift disrupts reading frame."),
q("single-base beta-globin mutation causes", "sickle cell anemia", ["gout", "Down syndrome", "Turner syndrome"], "Sickle cell anemia is due to beta-globin missense mutation."),
q("trisomy 21 causes", "Down syndrome", ["Turner syndrome", "Klinefelter syndrome", "PKU"], "Down syndrome is trisomy 21."),
q("45,X karyotype causes", "Turner syndrome", ["Down syndrome", "Klinefelter syndrome", "Marfan syndrome"], "Turner syndrome is monosomy X."),
q("lac operon controls metabolism of", "lactose", ["tryptophan", "glucose only", "heme"], "Lac operon regulates lactose utilization."),
q("lac repressor binds this region", "operator", ["poly-A tail", "anticodon", "telomere"], "Repressor binds operator."),
q("removal of repression is called", "derepression", ["repression", "translation", "replication"], "Inducer causes derepression."),
q("tryptophan acts as this in trp operon", "corepressor", ["inducer", "primer", "enhancer"], "Tryptophan activates its repressor."),
q("newborn screening detects treatable inherited disorders early", "secondary prevention of genetic disease", ["DNA ligation", "translation elongation", "BMR measurement"], "Early screening prevents complications."),
]),
("recombinant", "Recombinant DNA Technology and Gene Therapy", [
q("artificial transfer of gene between organisms is called", "recombinant DNA technology", ["translation", "glycosylation", "transamination"], "Genetic engineering transfers genes artificially."),
q("enzymes cutting DNA at specific sequences", "restriction endonucleases", ["DNA ligases", "helicases", "aminoacyl synthetases"], "Restriction enzymes cut DNA."),
q("restriction enzymes often recognize", "palindromic sequences", ["poly-A tails", "anticodon loops", "peptide signals"], "Many restriction sites are palindromes."),
q("enzyme joining DNA fragments", "DNA ligase", ["helicase", "primase", "peptidyl transferase"], "Ligase seals DNA fragments."),
q("small circular bacterial DNA used as vector", "plasmid", ["ribosome", "nucleosome", "lysosome"], "Plasmids are common vectors."),
q("viral DNA vehicle for cloning", "phage vector", ["mRNA cap", "histone", "tRNA"], "Phages can serve as vectors."),
q("marker helping identify transformed cells", "antibiotic resistance gene", ["stop codon", "intron", "poly-A tail"], "Selectable markers identify transformants."),
q("making many identical DNA copies in host cells", "molecular cloning", ["protein folding", "splicing", "translation termination"], "Cloning amplifies DNA."),
q("common host for cloning experiments", "E. coli", ["RBC", "platelet", "myocyte"], "E. coli is a standard cloning host."),
q("DNA made from processed mRNA lacks", "introns", ["exons", "codons", "open reading frame"], "cDNA lacks introns."),
q("PCR amplifies DNA using", "thermostable DNA polymerase", ["DNA ligase only", "RNA polymerase I", "peptidyl transferase"], "PCR uses heat-stable polymerase."),
q("PCR requires two short sequences flanking target", "primers", ["histones", "ribosomes", "operators only"], "Primers define target region."),
q("large-scale human insulin production is an application of", "genetic engineering", ["bomb calorimetry", "BMR measurement", "protein electrophoresis only"], "Recombinant technology produces insulin."),
q("insertion of normal gene to correct genetic defect", "gene therapy", ["gene knockout only", "Southern blot", "translation"], "Gene therapy introduces functional genes."),
q("viral vectors are useful because they can", "deliver genes into cells", ["measure BMR", "digest proteins", "lower glycemic index"], "Viruses efficiently deliver genetic material."),
]),
]

def make_prompt(i, clue):
    kind, n = ORDER[i - 1]
    return (STD if kind == "s" else UNQ)[n].format(clue=clue)

def rotate(items, offset):
    if not items:
        return []
    offset %= len(items)
    return items[offset:] + items[:offset]

def make_options(answer, wrong, topic_answers, chapter_answers, offset):
    out = []
    for item in rotate(wrong, offset) + rotate([a for a in topic_answers if a != answer], offset) + rotate([a for a in chapter_answers if a != answer], offset):
        if item != answer and item not in out:
            out.append(item)
        if len(out) == 3:
            break
    if len(out) < 3:
        raise ValueError(answer)
    out.insert(offset % 4, answer)
    return out

def main():
    chapter_answers = []
    for _, _, rows in TOPICS:
        for row in rows:
            if row["answer"] not in chapter_answers:
                chapter_answers.append(row["answer"])
    questions = []
    for ti, (slug, topic, rows) in enumerate(TOPICS):
        topic_answers = []
        for row in rows:
            if row["answer"] not in topic_answers:
                topic_answers.append(row["answer"])
        for qi, row in enumerate(rows, 1):
            opts = make_options(row["answer"], row["wrong"], topic_answers, chapter_answers, ti + qi)
            questions.append({**BASE, "id": f"biochemistry-molecular-biology-{slug}-{qi:02d}", "topic": topic, "topicTitle": topic, "difficulty": "moderate" if qi <= 6 else "high" if qi <= 12 else "very high", "prompt": make_prompt(qi, row["clue"]), "options": opts, "answerIndex": opts.index(row["answer"]), "answer": row["answer"], "explanation": row["explanation"]})
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "biochemistry" and x.get("chapterTitle") == CHAPTER)] + questions
    if len(TOPICS) != 5 or len(questions) != 75:
        raise ValueError("Expected 5 topics and 75 questions")
    if len({q["id"] for q in questions}) != 75 or len({q["prompt"] for q in questions}) != 75:
        raise ValueError("Duplicate ids/prompts")
    if any(q["answer"] != q["options"][q["answerIndex"]] for q in questions):
        raise ValueError("Bad answer mapping")
    data["questions"].sort(key=lambda item: item.get("id", ""))
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")
    for _, topic, _ in TOPICS:
        print(f"- {topic}")

if __name__ == "__main__":
    main()
