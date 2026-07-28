import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path("runtime-data/users.json")
CHAPTER = "Genetic Disorders"

BASE = {
    "subjectId": "pathology",
    "subjectTitle": "Pathology",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "imageUrls": [],
}


def q(difficulty, prompt, answer, distractors, explanation):
    options = [answer, *distractors]
    if difficulty not in {"easy", "moderate", "high"}:
        raise ValueError(f"Unexpected difficulty: {difficulty}")
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(f"Bad options for prompt: {prompt}")
    return {
        "difficulty": difficulty,
        "prompt": prompt,
        "options": options,
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
    }


def jumble_answer_position(question, desired_index):
    answer = question["answer"]
    distractors = [option for option in question["options"] if option != answer]
    if len(distractors) != 3:
        raise ValueError(f"Cannot jumble options for {question.get('id', question['prompt'])}")
    options = distractors[:]
    options.insert(desired_index, answer)
    question["options"] = options
    question["answerIndex"] = desired_index
    return question


TOPICS = [
    (
        "genes-mutations",
        "Genes, Human Disease, and Mutations",
        [
            q("easy", "A missense mutation is best defined as:", "A base substitution that changes one amino acid to another", ["A mutation that creates a premature stop codon", "A deletion of an entire chromosome", "A repeat expansion that always silences a gene"], "Missense mutations alter the meaning of a codon and substitute one amino acid in the protein."),
            q("easy", "A nonsense mutation produces disease by:", "Changing an amino acid codon into a stop codon", ["Replacing one amino acid with a similar amino acid", "Duplicating an entire autosome", "Increasing mitochondrial DNA copy number"], "Nonsense mutations create premature termination codons, often yielding truncated unstable proteins."),
            q("easy", "A frameshift mutation usually results from:", "Insertion or deletion of bases not in multiples of three", ["A single synonymous codon change", "Balanced translocation without gene disruption", "Normal X chromosome inactivation"], "Because codons are read in triplets, non-triplet insertions or deletions alter the downstream reading frame."),
            q("moderate", "A mutation in a promoter or enhancer may cause disease mainly by:", "Reducing or abolishing gene transcription", ["Changing the number of chromosomes in every cell", "Increasing fibrinolysis", "Producing only mitochondrial inheritance"], "Regulatory sequence mutations can impair transcription factor binding and reduce mRNA production."),
            q("moderate", "A point mutation in an intron can be pathogenic when it:", "Disrupts normal RNA splicing", ["Always produces a visible trisomy", "Prevents all DNA replication", "Creates a red infarct"], "Intronic splice-site mutations can prevent proper processing of the primary RNA transcript."),
            q("moderate", "A conservative missense mutation is usually less harmful because:", "The substituted amino acid has similar biochemical properties", ["It deletes the entire gene", "It always restores the normal codon", "It creates a full chromosomal monosomy"], "A chemically similar substitution may preserve enough protein structure and function."),
            q("moderate", "The sickle cell mutation is a classic example of:", "A nonconservative missense mutation", ["A balanced Robertsonian translocation", "A mitochondrial deletion", "A pure promoter deletion"], "Sickle hemoglobin results from substitution of valine for glutamic acid in beta-globin, changing protein properties."),
            q("high", "A three-base-pair deletion within a coding exon is less likely to cause a frameshift because:", "The reading frame remains aligned after loss of one codon", ["All deletions are corrected by mismatch repair", "Translation stops before the deletion", "Introns are never translated"], "In-frame deletions remove amino acid(s) but preserve codon grouping downstream."),
            q("high", "Pleiotropism means:", "One mutant gene produces multiple phenotypic effects", ["Several genes produce the same phenotype", "Only males express the phenotype", "A trait skips every generation"], "Sickle cell disease is pleiotropic because one beta-globin mutation causes anemia, vaso-occlusion, organ infarcts, and more."),
            q("high", "Genetic heterogeneity means:", "Mutations at different loci can produce a similar clinical phenotype", ["One mutation always produces many unrelated effects", "Every mutation is inherited maternally", "A gene is expressed only from the paternal allele"], "Clinically similar disorders such as childhood deafness may arise from mutations in many different genes."),
        ],
    ),
    (
        "mendelian",
        "Transmission Patterns of Single-Gene Disorders",
        [
            q("easy", "Autosomal dominant disorders are typically expressed in:", "Heterozygotes", ["Only homozygotes", "Only hemizygous males", "Only mitochondrial DNA carriers"], "A single mutant autosomal allele is sufficient to produce many dominant phenotypes."),
            q("easy", "If an affected heterozygous parent has an autosomal dominant disorder and the other parent is unaffected, each child has what risk?", "50%", ["0%", "25%", "100%"], "Each child has a one-in-two chance of inheriting the mutant allele."),
            q("easy", "Autosomal recessive disorders usually require:", "Mutant alleles on both homologous chromosomes", ["A mutant allele only on the Y chromosome", "One dominant allele in every affected person", "Loss of all mitochondria"], "Most autosomal recessive diseases manifest in homozygotes or compound heterozygotes."),
            q("moderate", "A key reason autosomal recessive disorders are more common in consanguineous families is:", "Relatives are more likely to carry the same rare mutant allele", ["Females cannot transmit autosomal genes", "All recessive disorders are mitochondrial", "X inactivation becomes impossible"], "Shared ancestry increases the chance both parents carry the same pathogenic recessive variant."),
            q("moderate", "Incomplete penetrance means:", "Some individuals with the disease genotype do not express the phenotype", ["The phenotype is always identical in all carriers", "Only males inherit the allele", "The gene is located only in mitochondria"], "Penetrance describes the proportion of genotype-positive individuals who show the trait."),
            q("moderate", "Variable expressivity means:", "The same genotype produces different severity or features among affected individuals", ["Only half of carriers have any phenotype", "All daughters of affected fathers are unaffected", "The mutation is always silent"], "Expressivity refers to the range of manifestations in people who express the disease."),
            q("moderate", "X-linked recessive disorders are usually expressed more severely in males because males are:", "Hemizygous for most X-linked genes", ["Homozygous for all autosomes", "Protected by two Y chromosomes", "Unable to inherit X chromosomes"], "Males have one X chromosome, so a mutant X-linked allele lacks a normal counterpart."),
            q("high", "An affected male with an X-linked recessive disorder and an unaffected noncarrier female will transmit the mutant allele to:", "All daughters and no sons", ["All sons and no daughters", "Half of sons and half of daughters", "No children"], "Fathers pass their X chromosome to daughters and Y chromosome to sons."),
            q("high", "A heterozygous female carrier of an X-linked disorder may show symptoms because of:", "Random X chromosome inactivation", ["Loss of both Y chromosomes", "Paternal mitochondrial inheritance", "Balanced translocation in every cell"], "Lyonization can leave a substantial fraction of cells expressing the mutant X chromosome."),
            q("high", "A new mutation is especially common in severe autosomal dominant disorders because:", "Affected individuals often have reduced reproductive fitness", ["Dominant mutations cannot be transmitted", "Autosomal genes mutate only after birth", "Recessive carriers are never healthy"], "When disease limits reproduction, many cases arise from new germline mutations rather than inheritance."),
        ],
    ),
    (
        "single-gene-mechanisms",
        "Biochemical and Molecular Basis of Single-Gene Disorders",
        [
            q("easy", "Most inborn errors of metabolism are caused by defects in:", "Enzymes", ["Platelet receptors", "Histone proteins only", "Centromeres"], "Many metabolic diseases are autosomal recessive enzyme deficiencies."),
            q("easy", "A receptor or transport-system defect classically causes:", "Impaired uptake or movement of a molecule", ["A balanced karyotype in every cell", "Only increased mitochondrial inheritance", "Universal frameshift mutation"], "Mutations in transporters or receptors block normal cellular handling of specific molecules."),
            q("easy", "Pharmacogenetics studies:", "Inherited differences in drug responses", ["Only chromosomal trisomies", "Only postmortem clots", "Only bacterial resistance genes"], "Genetic variants in drug-metabolizing enzymes, transporters, or receptors can influence toxicity and efficacy."),
            q("moderate", "Loss of enzyme activity may cause disease by:", "Accumulation of substrate or deficiency of product", ["Always increasing chromosome number", "Preventing X-linked inheritance", "Blocking all protein translation"], "Enzyme defects often cause toxic substrate buildup or inadequate production of downstream metabolites."),
            q("moderate", "Why are many enzyme deficiencies autosomal recessive?", "Half-normal enzyme activity is often sufficient", ["Enzymes are encoded only on mitochondrial DNA", "Dominant disorders never affect metabolism", "Heterozygotes always lack all enzyme activity"], "Carriers often remain healthy because one normal allele provides enough enzyme function."),
            q("moderate", "A dominant-negative mutation causes disease because the mutant protein:", "Interferes with function of the normal protein", ["Is always completely absent", "Corrects the wild-type protein", "Only affects mitochondrial genes"], "Structural proteins made of multimers are vulnerable to dominant-negative mutant subunits."),
            q("moderate", "Haploinsufficiency refers to disease caused when:", "One normal allele does not produce enough functional protein", ["Both alleles are always overexpressed", "The gene product is never needed", "Only introns are duplicated"], "Some genes require two working copies to provide adequate protein dosage."),
            q("high", "G6PD deficiency is often clinically silent until oxidant drug exposure because:", "The enzyme defect becomes important under oxidative stress", ["It is caused by trisomy 21", "It increases LDL receptors", "It prevents all hemoglobin synthesis"], "G6PD helps maintain red cell glutathione; oxidant stress can trigger hemolysis in deficient cells."),
            q("high", "A mutation affecting a collagen chain can produce dominant disease because:", "Mutant chains can disrupt assembly of normal collagen triple helices", ["Collagen is never multimeric", "Half-normal collagen is always excessive", "Collagen is encoded only by mitochondrial DNA"], "Abnormal structural subunits can poison the function of multimeric protein complexes."),
            q("high", "Patient-tailored therapy based on drug-metabolizing gene variants is an example of:", "Personalized medicine", ["Genomic imprinting", "Robertsonian translocation", "Gonadal mosaicism"], "Pharmacogenetic information can guide drug selection or dose for an individual patient."),
        ],
    ),
    (
        "structural-proteins",
        "Structural Protein Disorders: Marfan Syndrome and Ehlers-Danlos Syndromes",
        [
            q("easy", "Marfan syndrome is caused by mutations affecting:", "Fibrillin-1", ["LDL receptor", "Hexosaminidase A", "CFTR"], "Marfan syndrome usually results from FBN1 mutations encoding fibrillin-1."),
            q("easy", "The major organ systems affected in Marfan syndrome are:", "Skeleton, eyes, and cardiovascular system", ["Liver, pancreas, and spleen only", "Kidney glomeruli only", "Bone marrow only"], "Marfan syndrome prominently affects connective tissues rich in microfibrils."),
            q("easy", "Ehlers-Danlos syndromes are primarily disorders of:", "Collagen synthesis or structure", ["LDL uptake", "Mitochondrial oxidative phosphorylation only", "Imprinting at chromosome 15"], "EDS variants involve defective collagen or collagen-processing proteins."),
            q("moderate", "A dangerous cardiovascular complication of Marfan syndrome is:", "Aortic aneurysm and dissection", ["Pulmonary fat embolism", "Thrombocytopenia", "Acute appendicitis"], "Weakness of the aortic media predisposes to dilation, regurgitation, and dissection."),
            q("moderate", "Lens dislocation in Marfan syndrome reflects weakness of:", "Ciliary zonules", ["Corneal endothelium", "Retinal photoreceptors only", "Optic nerve myelin"], "Fibrillin-rich zonular fibers help suspend the lens."),
            q("moderate", "Excess TGF-beta signaling contributes to Marfan syndrome because fibrillin normally:", "Helps sequester latent TGF-beta in extracellular matrix", ["Degrades LDL particles", "Activates lysosomal hydrolases", "Silences imprinted genes"], "Fibrillin defects increase TGF-beta bioavailability, contributing to tissue abnormalities."),
            q("moderate", "Classic EDS commonly presents with:", "Hyperextensible skin and hypermobile joints", ["Severe hypercholesterolemia and xanthomas", "Obesity with hyperphagia", "Male hypogonadism with 47,XXY"], "Defective collagen weakens skin, ligaments, and other connective tissues."),
            q("high", "The vascular type of EDS is especially associated with defects in:", "Type III collagen", ["Type II pneumocytes", "LDL receptor recycling only", "Hexosaminidase A"], "Type III collagen is abundant in vessels and hollow organs, explaining rupture risk."),
            q("high", "Autosomal dominant inheritance in some EDS variants is explained by:", "Dominant-negative effects of abnormal collagen chains", ["Complete absence of mitochondria", "Only promoter methylation", "Loss of paternal chromosome 15"], "A mutant collagen chain can disrupt the collagen molecule even when a normal allele is present."),
            q("high", "The dermatosparaxis type of EDS is autosomal recessive because it involves:", "Deficiency of a procollagen-processing enzyme", ["A dominant structural collagen chain defect", "Trisomy of chromosome 21", "Expansion of CGG repeats"], "Enzyme deficiencies often require both alleles to be defective before disease appears."),
        ],
    ),
    (
        "fh",
        "Receptor and Transport Protein Disorders: Familial Hypercholesterolemia",
        [
            q("easy", "Familial hypercholesterolemia most commonly involves defective:", "LDL receptor-mediated clearance", ["Hemoglobin oxygen binding", "Mitochondrial DNA replication", "Collagen hydroxylation"], "Reduced LDL receptor function decreases hepatic LDL uptake."),
            q("easy", "The major plasma lipid abnormality in familial hypercholesterolemia is:", "Increased LDL cholesterol", ["Decreased ammonia", "Increased glycogen only", "Reduced chylomicron formation only"], "LDL accumulates in plasma when receptor-mediated clearance is impaired."),
            q("easy", "A clinical finding associated with familial hypercholesterolemia is:", "Tendon xanthomas", ["Café-au-lait spots only", "Macroorchidism only", "Webbed neck only"], "Cholesterol-rich deposits in tendons and skin can form xanthomas."),
            q("moderate", "The most serious consequence of familial hypercholesterolemia is:", "Premature atherosclerosis and coronary artery disease", ["Hemarthrosis", "Pulmonary edema from hypoalbuminemia", "Septic shock"], "High LDL accelerates atheroma formation and vascular disease."),
            q("moderate", "LDL receptors are normally clustered in membrane regions called:", "Coated pits", ["Nuclear pores", "Desmosomes", "Ciliary zonules"], "LDL binds receptors in coated pits, which are internalized by endocytosis."),
            q("moderate", "After LDL receptor-mediated endocytosis, LDL is degraded mainly in:", "Lysosomes", ["Peroxisomes", "Ribosomes", "Golgi cisternae only"], "The LDL particle dissociates from its receptor and is degraded in lysosomes."),
            q("moderate", "PCSK9 promotes hypercholesterolemia by:", "Increasing degradation of LDL receptors", ["Increasing LDL receptor recycling", "Converting LDL into HDL", "Activating hexosaminidase A"], "PCSK9 binds LDL receptors and targets them for degradation after endocytosis."),
            q("high", "A homozygous LDL receptor defect is more severe than heterozygous disease because:", "LDL receptor activity is nearly absent rather than partially reduced", ["Only homozygotes make HDL", "Heterozygotes cannot develop atherosclerosis", "LDL is cleared by red cells only"], "Gene dosage strongly affects LDL clearance and age of cardiovascular disease onset."),
            q("high", "Intracellular cholesterol normally suppresses cholesterol synthesis by inhibiting:", "HMG-CoA reductase", ["DNA polymerase", "Hexosaminidase A", "Thrombomodulin"], "Free cholesterol downregulates HMG-CoA reductase, the rate-limiting enzyme in cholesterol synthesis."),
            q("high", "Statins are useful in many patients with familial hypercholesterolemia because they:", "Increase hepatic LDL receptor expression by lowering intracellular cholesterol synthesis", ["Repair the LDL receptor gene directly", "Convert LDL to fibrin", "Block all cholesterol absorption in lysosomes"], "By inhibiting HMG-CoA reductase, statins increase LDL receptor expression when receptor function remains."),
        ],
    ),
    (
        "enzyme-storage",
        "Enzyme Defects and Storage Diseases",
        [
            q("easy", "Lysosomal storage diseases usually result from:", "Inherited deficiency of a lysosomal enzyme or related protein", ["Excess platelet activation", "Loss of all chromosomes", "Aspirin toxicity"], "Failure of lysosomal degradation causes accumulation of undegraded substrates."),
            q("easy", "Tay-Sachs disease is caused by deficiency of:", "Hexosaminidase A", ["Glucocerebrosidase", "Alpha-1,4-glucosidase", "LDL receptor"], "Tay-Sachs disease results from HEXA mutations and GM2 ganglioside accumulation."),
            q("easy", "Gaucher disease is caused by deficiency of:", "Glucocerebrosidase", ["Fibrillin-1", "Type III collagen", "Factor VIII"], "Gaucher disease is a lysosomal storage disorder involving glucocerebroside accumulation."),
            q("moderate", "A cherry-red spot may be seen in:", "Tay-Sachs disease", ["Familial hypercholesterolemia", "Turner syndrome", "Marfan syndrome"], "Ganglioside accumulation in retinal ganglion cells can leave the fovea appearing cherry red."),
            q("moderate", "Gaucher cells have a characteristic cytoplasm described as:", "Wrinkled tissue paper", ["Sea-blue histiocytes only", "Foamy vacuoles with no fibrils", "Auer rods"], "Lipid-laden macrophages in Gaucher disease have fibrillary, wrinkled cytoplasm."),
            q("moderate", "Niemann-Pick disease types A and B involve deficiency of:", "Sphingomyelinase", ["Hexosaminidase A", "LDL receptor", "Fibrillin-1"], "Types A and B Niemann-Pick disease are caused by sphingomyelinase deficiency."),
            q("moderate", "Niemann-Pick disease type C is primarily a defect in:", "Intracellular cholesterol trafficking", ["Collagen triple helix formation", "Beta-globin synthesis", "X chromosome pairing"], "NPC1/NPC2 defects impair cholesterol movement out of lysosomes."),
            q("high", "I-cell disease occurs because lysosomal enzymes:", "Fail to receive mannose-6-phosphate targeting markers", ["Are overtargeted to mitochondria", "Have excessive LDL receptor activity", "Are encoded only by the Y chromosome"], "Without mannose-6-phosphate, lysosomal enzymes are secreted rather than delivered to lysosomes."),
            q("high", "Pompe disease is a glycogen storage disease caused by deficiency of:", "Lysosomal acid alpha-glucosidase", ["Branching enzyme", "Glucose-6-phosphatase", "Fibrillin-1"], "Pompe disease is glycogen storage disease type II and affects lysosomal glycogen degradation."),
            q("high", "Lysosomal storage disorders often show organomegaly because:", "Storage material accumulates in mononuclear phagocytes and parenchymal cells", ["All organs develop trisomy", "There is universal thrombosis", "Albumin leaks into all tissues"], "Progressive substrate accumulation expands affected cells and organs."),
        ],
    ),
    (
        "complex-cytogenetics",
        "Complex Multigenic Disorders and Cytogenetic Principles",
        [
            q("easy", "Complex multigenic disorders result from:", "Interactions of multiple genes and environmental factors", ["A single mutation with classic Mendelian inheritance only", "Only mitochondrial DNA mutations", "Only balanced translocations"], "Common diseases often reflect multiple susceptibility genes plus environmental influences."),
            q("easy", "A normal human somatic karyotype contains:", "46 chromosomes", ["23 chromosomes", "47 chromosomes", "69 chromosomes"], "Human somatic cells normally have 22 pairs of autosomes and two sex chromosomes."),
            q("easy", "Aneuploidy means:", "Chromosome number is not an exact multiple of the haploid number", ["A perfectly balanced genome", "A point mutation in one codon", "A mitochondrial-only mutation"], "Monosomy and trisomy are forms of aneuploidy."),
            q("moderate", "Nondisjunction is:", "Failure of homologous chromosomes or sister chromatids to separate", ["Exchange of equal chromosomal segments only", "Silencing of a paternal allele", "A lysosomal targeting defect"], "Nondisjunction during meiosis is a major cause of aneuploidy."),
            q("moderate", "Mosaicism means:", "Two or more genetically distinct cell lines in one individual", ["Every cell has the same mutation inherited from both parents", "Only mitochondrial DNA is present", "All chromosomes are triploid"], "Postzygotic errors can create genetically different cell populations."),
            q("moderate", "A balanced reciprocal translocation is often clinically silent because:", "No essential genetic material is gained or lost", ["It always deletes one chromosome", "It prevents gamete formation entirely", "It only affects mitochondrial DNA"], "Balanced rearrangements may preserve gene dosage, although they can disrupt genes or affect offspring."),
            q("moderate", "A Robertsonian translocation involves fusion of:", "Long arms of two acrocentric chromosomes", ["Two mitochondrial genomes", "Two sister chromatids at every centromere", "Only X and Y chromosomes"], "Robertsonian translocations join acrocentric long arms and can underlie familial Down syndrome."),
            q("high", "A ring chromosome forms after:", "Breaks at both chromosome ends with fusion of the broken ends", ["Triplet-repeat expansion", "LDL receptor recycling", "Mannose-6-phosphate tagging"], "Loss of terminal segments and end-to-end fusion creates a ring chromosome."),
            q("high", "An inversion is pericentric when it:", "Includes the centromere", ["Excludes the centromere", "Duplicates the entire chromosome", "Deletes all telomeres without rearrangement"], "Pericentric inversions involve breaks on both sides of the centromere."),
            q("high", "Genetic linkage analysis uses polymorphic markers because:", "Marker alleles can track inheritance of nearby disease loci in families", ["They directly cure the mutation", "They replace karyotyping for all aneuploidies", "They silence all imprinted genes"], "Markers such as microsatellites can identify inheritance patterns near a disease gene."),
        ],
    ),
    (
        "autosomal-chromosomal",
        "Autosomal Chromosomal Disorders",
        [
            q("easy", "Down syndrome is most commonly caused by:", "Trisomy 21 from meiotic nondisjunction", ["Monosomy X", "47,XXY", "Deletion of paternal 15q11-q13"], "Most cases of Down syndrome result from an extra chromosome 21 due to nondisjunction."),
            q("easy", "A major risk factor for trisomy 21 is:", "Advanced maternal age", ["Low dietary cholesterol", "Paternal mitochondrial inheritance", "Aspirin exposure"], "Maternal age strongly increases risk of meiotic nondisjunction."),
            q("easy", "Children with Down syndrome have increased risk of:", "Acute leukemia", ["Familial hypercholesterolemia", "Marfan lens dislocation only", "Hemophilia A only"], "Down syndrome is associated with increased risk of ALL and AML, especially megakaryoblastic leukemia."),
            q("moderate", "A congenital heart defect classically associated with Down syndrome is:", "Atrioventricular septal defect", ["Tetralogy caused by 22q11.2 only", "Hypertrophic pyloric stenosis", "Coarctation in Turner syndrome only"], "Endocardial cushion defects, including AV septal defects, are common in Down syndrome."),
            q("moderate", "A Robertsonian translocation involving chromosome 21 can cause:", "Familial Down syndrome", ["Turner syndrome", "Fragile X syndrome", "Leber hereditary optic neuropathy"], "A parent carrying a balanced Robertsonian translocation can have children with extra 21q material."),
            q("moderate", "Edwards syndrome is:", "Trisomy 18", ["Trisomy 13", "Monosomy X", "Triploidy"], "Trisomy 18 is Edwards syndrome."),
            q("moderate", "Patau syndrome is:", "Trisomy 13", ["Trisomy 18", "Trisomy 21", "47,XXY"], "Trisomy 13 is Patau syndrome."),
            q("high", "Chromosome 22q11.2 deletion syndrome is strongly associated with abnormal development of:", "Third and fourth pharyngeal pouches", ["Ciliary zonules", "Lysosomal mannose-6-phosphate receptors", "LDL coated pits"], "22q11.2 deletion affects pharyngeal pouch development, causing thymic/parathyroid and cardiac defects."),
            q("high", "A child with thymic hypoplasia, hypocalcemia, and conotruncal cardiac defects most likely has:", "22q11.2 deletion syndrome", ["Tay-Sachs disease", "Klinefelter syndrome", "Familial hypercholesterolemia"], "DiGeorge/22q11.2 deletion syndrome causes T-cell deficiency, hypocalcemia, and conotruncal anomalies."),
            q("high", "Mosaic Down syndrome is usually milder because:", "Only a proportion of cells carry trisomy 21", ["All cells carry four copies of chromosome 21", "The extra chromosome is mitochondrial", "It is caused by LDL receptor mutation"], "Phenotype depends partly on the fraction and distribution of trisomic cells."),
        ],
    ),
    (
        "sex-chromosomes",
        "Sex Chromosome Disorders and Disorders of Sex Development",
        [
            q("easy", "Klinefelter syndrome most commonly has which karyotype?", "47,XXY", ["45,X", "47,XYY", "46,XX"], "The classic Klinefelter karyotype is 47,XXY."),
            q("easy", "Turner syndrome most commonly involves:", "Monosomy X", ["Trisomy 21", "47,XXY", "Trisomy 18"], "Turner syndrome is usually 45,X or mosaic variants involving X chromosome loss."),
            q("easy", "A common clinical feature of Turner syndrome is:", "Short stature", ["Tall stature with small testes", "Hyperphagia and obesity from paternal 15q deletion", "Cherry-red macula"], "Short stature and gonadal dysgenesis are classic Turner features."),
            q("moderate", "Klinefelter syndrome classically presents with:", "Testicular atrophy and infertility", ["Webbed neck and coarctation only", "Hyperextensible skin", "Lens dislocation"], "Seminiferous tubule dysgenesis causes small firm testes, infertility, and hypogonadism."),
            q("moderate", "Barr body number is generally equal to:", "Number of X chromosomes minus one", ["Number of Y chromosomes plus one", "Number of autosomes minus 22", "Number of mitochondria"], "All but one X chromosome are inactivated in somatic cells."),
            q("moderate", "A classic cardiovascular association of Turner syndrome is:", "Coarctation of the aorta", ["Aortic root dilation from fibrillin defect", "Pulmonary embolism", "Coronary xanthomas"], "Turner syndrome is associated with congenital cardiovascular defects, including coarctation."),
            q("moderate", "Why are sex chromosome aneuploidies often better tolerated than autosomal aneuploidies?", "X inactivation and limited Y chromosome gene content reduce gene dosage imbalance", ["Sex chromosomes contain no genes", "Autosomes are always inactive", "Mitochondria compensate for all genes"], "Dosage compensation blunts the effect of extra X chromosomes, and the Y has relatively few genes."),
            q("high", "In Klinefelter syndrome, increased gonadotropins occur because:", "Primary testicular failure reduces sex steroid and inhibin feedback", ["The pituitary is absent", "There is excess LDL receptor activity", "Both adrenal glands are deleted"], "Gonadal failure leads to hypergonadotropic hypogonadism."),
            q("high", "A phenotypic female with streak ovaries, webbed neck, and lymphedema most likely has:", "Turner syndrome", ["Fragile X syndrome", "Marfan syndrome", "Gaucher disease"], "These findings are classic for Turner syndrome."),
            q("high", "True hermaphroditism is defined by the presence of:", "Both ovarian and testicular tissue", ["Only testes with female external genitalia", "Only ovaries with male external genitalia", "One extra X chromosome in all males"], "Ovotesticular disorder of sex development contains both ovarian and testicular gonadal tissue."),
        ],
    ),
    (
        "nonclassic-diagnosis",
        "Nonclassic Inheritance and Molecular Genetic Diagnosis",
        [
            q("easy", "Fragile X syndrome is caused by expansion of:", "CGG repeats in FMR1", ["CAG repeats in beta-globin", "CTG repeats in LDL receptor", "GAA repeats in collagen III"], "Fragile X syndrome results from CGG repeat expansion in the FMR1 gene."),
            q("easy", "Mitochondrial DNA disorders are usually inherited from:", "The mother", ["The father", "Both parents equally through autosomes", "Only affected brothers"], "Oocytes contribute most mitochondria to the embryo, so mtDNA is maternally inherited."),
            q("easy", "Genomic imprinting means:", "Gene expression depends on whether the allele is inherited from the mother or father", ["All genes are expressed equally from both parents", "Only mitochondrial genes are expressed", "Genes are altered without inheritance"], "Imprinting is parent-of-origin-specific gene expression due to epigenetic marking."),
            q("moderate", "Anticipation in trinucleotide-repeat disorders refers to:", "Earlier onset or increased severity in successive generations", ["Stable phenotype in every generation", "Equal expression of maternal and paternal alleles", "Loss of all repeat sequences"], "Repeat expansions can enlarge during transmission, worsening disease in descendants."),
            q("moderate", "Full Fragile X mutations usually cause disease by:", "Methylation and silencing of FMR1", ["Overexpression of LDL receptor", "Loss of collagen III secretion", "Failure of platelet aggregation"], "Large CGG expansions promote methylation and transcriptional silencing of FMR1."),
            q("moderate", "Prader-Willi syndrome usually results from loss of genes on:", "Paternal chromosome 15q11-q13", ["Maternal chromosome 21q", "Both X chromosomes", "Mitochondrial DNA only"], "Paternal 15q11-q13 deletion or maternal uniparental disomy can cause Prader-Willi syndrome."),
            q("moderate", "Angelman syndrome usually results from loss of function of genes on:", "Maternal chromosome 15q11-q13", ["Paternal chromosome 22q11.2", "Both chromosome 18 copies", "Y chromosome AZF region"], "Angelman syndrome reflects loss of the maternally active allele in the same imprinted region."),
            q("high", "Heteroplasmy in mitochondrial disease means:", "A cell contains a mixture of normal and mutant mitochondrial DNA", ["All mitochondria are inherited from the father", "Every cell has identical mutant autosomes", "Only one X chromosome is active"], "Variable proportions of mutant mtDNA help explain variable severity and threshold effects."),
            q("high", "FISH is especially useful for detecting:", "Specific chromosomal deletions or rearrangements using fluorescent probes", ["Single-base substitutions across the entire genome only", "Protein folding defects directly", "Serum LDL concentration"], "FISH uses labeled DNA probes to localize particular genomic regions in cells."),
            q("high", "Next-generation sequencing is powerful because it can:", "Sequence many genomic regions in parallel", ["Always detect every balanced translocation without other tests", "Replace clinical interpretation", "Measure platelet aggregation directly"], "NGS massively parallelizes DNA sequencing, enabling panels, exomes, and tumor profiling."),
        ],
    ),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch5-{slug}-{index}", "topic": topic, **data}
            jumble_answer_position(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 5 questions, got {len(chapter_questions)}")
    topic_counts = Counter(q["topic"] for q in chapter_questions)
    if len(topic_counts) != 10 or any(count != 10 for count in topic_counts.values()):
        raise ValueError(f"Bad topic distribution: {topic_counts}")
    expected = Counter({"easy": 3, "moderate": 4, "high": 3})
    for topic in topic_counts:
        counts = Counter(q["difficulty"] for q in chapter_questions if q["topic"] == topic)
        if counts != expected:
            raise ValueError(f"Bad difficulty distribution for {topic}: {counts}")
    for question in chapter_questions:
        options = question["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Bad options: {question['id']}")
        if question["answer"] != options[question["answerIndex"]]:
            raise ValueError(f"Bad answer: {question['id']}")
    if all_questions is not None:
        ids = [q.get("id") for q in all_questions]
        duplicates = [qid for qid, count in Counter(ids).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate ids: {duplicates[:10]}")


def main():
    chapter_questions = build_questions()
    validate(chapter_questions)

    data = json.loads(DATA_PATH.read_text(encoding="utf-8-sig"))
    existing = data.get("questions", [])
    kept = [
        question
        for question in existing
        if not (
            question.get("chapterTitle") == CHAPTER
            or str(question.get("id", "")).startswith("robbins-ch5-")
        )
    ]
    data["questions"] = kept + chapter_questions
    validate(chapter_questions, data["questions"])
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Removed {len(existing) - len(kept)} existing Chapter 5 questions")
    print(f"Added {len(chapter_questions)} Robbins Chapter 5 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
