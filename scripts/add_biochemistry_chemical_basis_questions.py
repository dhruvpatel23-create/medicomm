import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Chemical Basis of Life"
BASE = {"subjectId": "biochemistry", "subjectTitle": "Biochemistry", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}

STD = [
    "Which option best completes this biochemical statement: {clue}?",
    "What is the most appropriate answer for: {clue}?",
    "Which concept is most directly associated with: {clue}?",
    "Why is this point important in the chemical basis of life: {clue}?",
    "Which interpretation is best for this finding: {clue}?",
    "How should this be classified in an exam question: {clue}?",
    "Which choice is the best single association for: {clue}?",
    "What does this source-book detail most strongly indicate: {clue}?",
    "Which statement is correct regarding: {clue}?",
    "How is this clue best applied in biochemistry: {clue}?",
]
UNQ = [
    "A viva examiner gives only this hint: '{clue}'. Choose the expected answer.",
    "Match the biochemical clue with the correct term: {clue}.",
    "A concept map has a blank beside '{clue}'. Which label fits?",
    "Assertion-reason style: the assertion depends on '{clue}'. Select the correct reason.",
    "A final-year MCQ uses this practical clue: '{clue}'. What is the best answer?",
]
ORDER = [("s",0),("s",1),("u",0),("s",2),("s",3),("s",4),("u",1),("s",5),("s",6),("u",2),("s",7),("s",8),("u",3),("s",9),("u",4)]

def q(clue, answer, wrong, explanation):
    return {"clue": clue, "answer": answer, "wrong": wrong, "explanation": explanation}

TOPICS = [
("history", "History of Biochemistry", [
q("the term biochemistry was coined in 1903 by this scientist", "Carl Neuberg", ["Hans Krebs", "Watson and Crick", "Justus von Liebig"], "The chapter attributes the term biochemistry to Carl Neuberg."),
q("Wohler's synthesis of urea weakened this old idea", "vital force theory", ["central dogma", "Donnan equilibrium", "chemiosmotic theory"], "Urea synthesis showed organic compounds could be made outside living systems."),
q("Buchner's cell-free yeast extract supported this concept", "enzymatic reactions can occur outside intact cells", ["genes are made of protein", "DNA lacks bases", "water is nonpolar"], "Cell-free fermentation helped establish enzymes as biochemical catalysts."),
q("Avery, MacLeod and McCarty identified this as genetic material", "DNA", ["protein", "lipid", "glycogen"], "Their transformation experiments pointed to DNA."),
q("Watson and Crick explained genetic storage through this model", "DNA double helix", ["urea cycle", "Krebs cycle", "Donnan equilibrium"], "The double helix explained base pairing and replication."),
q("Hans Krebs is associated with this metabolic pathway", "citric acid cycle", ["glycogen synthesis", "DNA replication", "protein sequencing"], "Krebs described the TCA cycle."),
q("Sanger's insulin work showed proteins have this", "defined amino acid sequence", ["random base composition", "no peptide bonds", "only carbohydrate structure"], "Sequencing insulin established defined protein sequence."),
q("clinical biochemistry became central because disease alters these", "measurable body molecules", ["bone names only", "organ shapes only", "skin color only"], "Disease produces measurable molecular changes."),
q("biochemistry explains life processes mainly at this level", "molecular level", ["gross anatomical level", "population level only", "radiographic level only"], "The chapter frames biochemistry as molecular biology of life."),
q("recombinant DNA technology allowed production of this therapeutic molecule", "human insulin", ["bile salts", "collagen fibers", "gastric acid"], "Recombinant technology made therapeutic proteins available."),
q("molecular biology grew from applying biochemistry to this", "inheritance and information transfer", ["bone mechanics", "surgical anatomy", "auscultation"], "Biochemistry connects molecules with heredity."),
q("PCR is useful because it can amplify this", "specific DNA sequences", ["whole organs", "fat droplets", "calcium crystals"], "PCR amplifies nucleic acid sequences."),
q("biochemistry links symptoms to this", "disturbed molecular pathways", ["only external appearance", "only organ weight", "only height"], "Clinical interpretation depends on pathways."),
q("enzymes became central to biochemistry because they are", "specific biological catalysts", ["inert storage molecules", "always structural minerals", "only genetic bases"], "Enzymes catalyze biological reactions."),
q("modern medical biochemistry includes genomics, proteomics and this broad aim", "molecular diagnosis and therapy", ["only gross dissection", "only taxonomy", "only radiography"], "Modern biochemistry supports diagnosis and targeted therapy."),
]),
("biomolecules-metabolism", "Biomolecules and Metabolism", [
q("proteins are polymers of these building blocks", "amino acids", ["nucleotides", "fatty acids", "monosaccharides"], "Proteins are built from amino acids."),
q("nucleic acids are polymers of these", "nucleotides", ["amino acids", "triacylglycerols", "minerals"], "DNA and RNA are nucleotide polymers."),
q("glycogen is a storage polymer of this", "glucose", ["ribose", "alanine", "cholesterol"], "Glycogen stores glucose."),
q("macromolecules associate into complexes mainly through this", "noncovalent interactions", ["nuclear fission", "random heat", "metallic bonding only"], "Supramolecular assemblies use weak interactions."),
q("ribosomes are examples of this level of organization", "supramolecular complexes", ["single atoms", "monosaccharides", "trace elements"], "Ribosomes contain RNA and protein."),
q("catabolism primarily does this", "breaks molecules and releases energy", ["builds complex molecules only", "stores genetic code only", "prevents enzyme action"], "Catabolism degrades fuels."),
q("anabolism primarily does this", "synthesizes complex molecules using energy", ["breaks all macromolecules", "oxidizes NADH only", "digests food in lumen only"], "Anabolism builds biomolecules."),
q("amphibolic pathways serve both catabolic and anabolic roles", "crossroads of metabolism", ["only digestion", "only excretion", "only DNA repair"], "Amphibolic pathways link breakdown and synthesis."),
q("primary metabolism in the chapter refers to this", "digestion to absorbable units", ["electron transport only", "gene expression", "ketone excretion"], "Primary metabolism is digestion."),
q("secondary or intermediary metabolism generates this", "NADH and FADH2", ["only bile salts", "only albumin", "only antibodies"], "Intermediary metabolism produces reduced coenzymes."),
q("tertiary metabolism occurs through this", "electron transport chain", ["brush border digestion", "DNA splicing", "protein folding only"], "ETC captures energy from reduced coenzymes."),
q("carbohydrate metabolism is centered mainly around", "glucose", ["cholesterol", "leucine", "heme"], "Glucose is central to carbohydrate metabolism."),
q("lipid metabolism is centered mainly around", "fatty acids", ["glycine", "ribose", "calcium"], "Fatty acids are central lipid fuels."),
q("amino acids are mainly used for this purpose", "body building", ["exclusive energy storage", "oxygen transport only", "water buffering only"], "Amino acids primarily build body proteins."),
q("ATP links catabolism and anabolism by acting as", "energy currency", ["genetic template", "structural fiber", "bile pigment"], "ATP couples energy release to energy use."),
]),
("ionic-bonds", "Ionic Bonds", [
q("ionic bond is due to attraction between", "oppositely charged groups", ["two nonpolar groups", "shared electron pair only", "peptide chains only"], "Ionic interactions occur between opposite charges."),
q("electron transfer commonly creates these charged species", "ions", ["ribosomes", "peptides", "micelles"], "Ions arise by gain/loss of electrons."),
q("positively charged ion is called", "cation", ["anion", "zwitterion only", "dipole"], "Cations carry positive charge."),
q("negatively charged ion is called", "anion", ["cation", "proton donor only", "hydrophobe"], "Anions carry negative charge."),
q("NaCl is a classic example of this bond", "ionic bond", ["hydrogen bond", "hydrophobic interaction", "van der Waals force"], "NaCl is held by ionic attraction."),
q("lysine side chain contributes this in proteins", "positive charge", ["negative charge", "nonpolar ring", "phosphate ester"], "Lysine is basic and positively charged."),
q("arginine guanidinium group usually carries this charge", "positive charge", ["negative charge", "neutral hydrophobic charge", "no charge always"], "Arginine is basic."),
q("histidine imidazole can participate in ionic interactions because", "it can accept or donate protons near physiological pH", ["it lacks nitrogen", "it is always fatty", "it is a sugar"], "Histidine is proton-sensitive near physiologic pH."),
q("aspartate side chain contributes this in proteins", "negative charge", ["positive charge", "aromatic ring only", "sulfhydryl only"], "Aspartate has a carboxylate."),
q("glutamate side chain contributes this in proteins", "negative charge", ["positive charge", "neutral sugar", "heme group"], "Glutamate has a carboxylate."),
q("salt bridges in proteins are mainly this type of interaction", "ionic interaction", ["peptide bond", "glycosidic bond", "hydrophobic bond"], "Salt bridges are charge-charge interactions."),
q("ionic interactions are weakened when pH changes because", "ionization state changes", ["atoms disappear", "peptide bonds vanish", "water becomes nonpolar"], "pH affects charge of groups."),
q("ionic bonds are stronger in nonpolar interior than in water because water", "screens charges", ["destroys covalent bonds", "has no dipole", "cannot dissolve ions"], "Water competes with charge interactions."),
q("protein tertiary structure may be stabilized by", "oppositely charged side chains", ["only glucose residues", "only cholesterol", "only oxygen gas"], "Charged side chains can form ionic interactions."),
q("ionic bonds differ from covalent bonds because they involve", "electrostatic attraction rather than electron sharing", ["electron sharing only", "peptide synthesis", "phosphate transfer only"], "Ionic bonds are charge attractions."),
]),
("hydrogen-bonding", "Hydrogen Bonding", [
q("hydrogen bond commonly involves hydrogen attached to", "oxygen or nitrogen", ["carbon only", "sodium only", "calcium only"], "Biological H bonds usually involve O or N."),
q("hydrogen bond donor provides this atom", "hydrogen", ["sodium", "phosphate", "carbonyl carbon"], "Donors provide hydrogen."),
q("hydrogen bond acceptor commonly has", "lone pair of electrons", ["no electrons", "only peptide chain", "only methyl groups"], "Acceptors use lone pairs."),
q("water molecules associate through this interaction", "hydrogen bonding", ["ionic bonding only", "peptide bonding", "disulfide bonding"], "Water forms H-bonded networks."),
q("DNA base pairing uses this interaction", "hydrogen bonds", ["covalent bonds between bases", "metallic bonds", "ester bonds"], "Complementary bases pair by H bonds."),
q("A-T base pair has this number of hydrogen bonds", "two", ["three", "one", "four"], "A-T has two H bonds."),
q("G-C base pair has this number of hydrogen bonds", "three", ["two", "one", "five"], "G-C has three H bonds."),
q("alpha helix is stabilized mainly by", "backbone hydrogen bonds", ["glycosidic bonds", "ionic sodium bonds", "fatty acid ester bonds"], "Protein secondary structure uses backbone H bonds."),
q("beta sheet is stabilized mainly by", "backbone hydrogen bonds", ["phosphodiester bonds", "disulfide bonds only", "cholesterol ester"], "Beta sheets use H bonds."),
q("hydrogen bonds are individually weaker than", "covalent bonds", ["van der Waals attractions only", "thermal motion only", "water dipoles"], "H bonds are weak compared with covalent bonds."),
q("many hydrogen bonds together provide", "structural stability and specificity", ["random breakdown", "no biological effect", "only heat loss"], "Collective H bonds stabilize biomolecules."),
q("hydrogen bonding contributes to enzyme-substrate recognition by", "specific orientation of groups", ["destroying active site", "making all substrates identical", "removing charges"], "H bonds help specificity."),
q("peptide carbonyl oxygen often acts as", "hydrogen bond acceptor", ["hydrogen bond donor only", "cation", "hydrophobic group"], "Carbonyl oxygen accepts H bonds."),
q("peptide N-H often acts as", "hydrogen bond donor", ["anion", "nonpolar lipid", "phosphate donor only"], "Peptide N-H donates H bonds."),
q("hydrogen bonding differs from hydrophobic interaction because it depends on", "polar donor-acceptor groups", ["nonpolar clustering only", "fat storage", "electron transfer"], "H bonding is directional and polar."),
]),
("hydrophobic", "Hydrophobic Interactions", [
q("hydrophobic interaction occurs when nonpolar groups cluster in", "water", ["benzene only", "vacuum", "solid salt"], "Hydrophobic groups aggregate in aqueous solution."),
q("nonpolar side chains avoid water because they cannot form", "favorable hydrogen bonds with water", ["peptide bonds", "DNA codons", "glycosidic linkages"], "Hydrophobic groups disrupt water H bonding."),
q("hydrophobic interactions help stabilize this protein feature", "folded interior", ["urine glucose", "serum sodium", "DNA phosphate charge"], "Nonpolar residues are buried in protein cores."),
q("cell membranes are stabilized partly by hydrophobic interaction among", "lipid tails", ["phosphate heads only", "ribose sugars", "amino groups"], "Lipid tails cluster away from water."),
q("micelle formation is driven mainly by", "hydrophobic effect", ["DNA replication", "ionic calcium binding", "peptide synthesis"], "Amphipathic molecules form micelles due to hydrophobic effect."),
q("hydrophobic interactions are not true bonds but arise from", "water ordering around nonpolar surfaces", ["electron transfer", "proton donation", "phosphate esterification"], "Hydrophobic effect is solvent-driven."),
q("valine, leucine and isoleucine side chains are mostly", "hydrophobic", ["strongly acidic", "strongly basic", "phosphorylated"], "Branched-chain residues are nonpolar."),
q("phenylalanine side chain contributes this interaction", "hydrophobic and aromatic packing", ["only ionic attraction", "only phosphate transfer", "only glycosidic bond"], "Phenylalanine is nonpolar aromatic."),
q("exposure of hydrophobic core to water tends to", "destabilize protein folding", ["always stabilize protein", "create DNA", "increase pH directly"], "Exposed hydrophobic cores are unfavorable."),
q("hydrophobic interactions are important in ligand binding because they", "exclude water from nonpolar contact surfaces", ["require covalent reaction always", "destroy active sites", "replace all H bonds"], "Water exclusion can strengthen binding."),
q("detergents disrupt membranes by interfering with", "hydrophobic lipid interactions", ["DNA base sequence", "protein synthesis code", "Donnan equilibrium only"], "Detergents solubilize lipids."),
q("hydrophobic molecules are generally", "poorly soluble in water", ["highly ionized in water", "always charged", "only nucleotides"], "Nonpolar compounds have low water solubility."),
q("hydrophobic effect increases when nonpolar surface area exposed to water", "decreases", ["increases forever", "becomes ionic", "turns into ribose"], "Burial of nonpolar surfaces is favorable."),
q("protein folding often places hydrophilic residues", "on the surface", ["only in core", "only in DNA", "outside the cell always"], "Polar residues interact with water."),
q("hydrophobic interactions differ from ionic bonds because they involve", "nonpolar association rather than charge attraction", ["opposite charges only", "electron transfer", "proton donation"], "Hydrophobic effect is not charge-charge attraction."),
]),
("thermodynamics", "Principles of Thermodynamics", [
q("first law of thermodynamics states conservation of", "energy", ["entropy only", "mass of DNA only", "pH only"], "Energy is neither created nor destroyed."),
q("second law states spontaneous processes increase this in universe", "entropy", ["enthalpy only", "protein content", "glucose content"], "Entropy of universe increases in spontaneous processes."),
q("Gibbs free energy predicts this", "spontaneity of a reaction", ["chromosome number", "enzyme name only", "amino acid sequence directly"], "Delta G indicates reaction direction."),
q("negative delta G means reaction is", "exergonic", ["endergonic", "at equilibrium", "impossible"], "Negative delta G is favorable."),
q("positive delta G means reaction is", "endergonic", ["exergonic", "complete", "diffusion-only"], "Positive delta G needs energy input."),
q("delta G equal to zero indicates", "equilibrium", ["irreversible reaction", "protein denaturation", "DNA mutation"], "At equilibrium, no net change occurs."),
q("ATP hydrolysis can drive unfavorable reactions by", "coupling", ["Donnan trapping", "base pairing", "hydrophobic burial only"], "Coupling links exergonic and endergonic reactions."),
q("standard biochemical free energy uses this pH convention", "pH 7", ["pH 0", "pH 14", "undefined pH"], "Biochemical standard state uses pH 7."),
q("enthalpy represents this component", "heat content", ["disorder only", "charge only", "gene number"], "Enthalpy relates to heat."),
q("entropy represents this tendency", "disorder or randomness", ["heat content only", "amino acid charge only", "DNA length only"], "Entropy reflects disorder."),
q("biological systems maintain order by", "using energy", ["violating thermodynamics", "stopping entropy globally", "removing water"], "Cells require energy to maintain order."),
q("oxidation of nutrients provides this to cells", "usable free energy", ["chromosomes only", "structural water only", "bile pigments"], "Fuel oxidation releases energy."),
q("high-energy phosphate bonds are important because hydrolysis has", "large negative free energy change", ["no free energy change", "positive-only energy", "no biological use"], "ATP hydrolysis is strongly exergonic."),
q("catabolic reactions generally supply energy for", "anabolic reactions", ["only mineral storage", "only water balance", "only blood pressure"], "Catabolism powers biosynthesis."),
q("thermodynamic feasibility does not prove rate because rate depends on", "enzyme kinetics", ["chromosome count", "gross anatomy", "dietary fiber"], "Delta G and rate are different concepts."),
]),
("donnan", "Donnan Membrane Equilibrium", [
q("Donnan equilibrium involves a membrane permeable to small ions but not to", "one charged macromolecule", ["water", "sodium only", "chloride only"], "A nondiffusible charged particle causes Donnan distribution."),
q("plasma proteins act as nondiffusible anions contributing to", "Donnan effect", ["PCR", "translation", "glycolysis"], "Proteins can create Donnan effects."),
q("side with nondiffusible anion attracts more", "cations", ["anions", "neutral lipids", "ribosomes"], "Fixed negative charge attracts cations."),
q("side with nondiffusible anion has relatively fewer diffusible", "anions", ["cations", "water molecules only", "proteins"], "Diffusible anions are relatively excluded."),
q("Donnan equilibrium still maintains this in each compartment", "electroneutrality", ["protein synthesis", "DNA replication", "complete equality of all ions"], "Each side remains electrically neutral."),
q("product of diffusible ion concentrations tends to be equal across membrane", "Donnan product rule", ["Michaelis constant", "Chargaff rule", "Bohr effect"], "Ion products equal at equilibrium."),
q("Donnan effect contributes to this plasma property", "oncotic pressure", ["genetic code", "protein folding only", "enzyme active site"], "Plasma proteins influence water distribution."),
q("cell membranes with trapped intracellular proteins show", "unequal ion distribution", ["no ion distribution", "complete protein diffusion", "loss of charge"], "Fixed proteins affect ion distribution."),
q("Donnan equilibrium is important because it links ion distribution with", "osmotic water movement", ["DNA sequencing", "protein translation", "lipid digestion"], "Ion imbalance affects water movement."),
q("chloride shift in red cells relates to membrane ion exchange and", "Donnan-type principles", ["protein sequencing", "glycogen storage", "fatty acid synthesis"], "RBC ion distribution reflects membrane equilibria."),
q("nondiffusible proteins cannot cross membrane because of", "size and charge restrictions", ["lack of atoms", "no peptide bonds", "being gases"], "Proteins are retained by membranes."),
q("if a protein anion is trapped inside a compartment, sodium tends to be", "higher on protein side", ["lower on protein side always", "absent", "converted to chloride"], "Cations accumulate near fixed anions."),
q("Donnan equilibrium differs from simple diffusion because of", "nondiffusible charged species", ["temperature only", "enzyme turnover", "ATP synthesis"], "Fixed charges prevent equal distribution."),
q("Donnan effect can influence pH distribution across membranes because", "hydrogen ions are diffusible cations", ["hydrogen is a protein", "pH is not ionic", "chloride is a sugar"], "H+ distribution may be affected by fixed charges."),
q("clinical relevance of Donnan equilibrium is strongest in", "fluid and electrolyte distribution", ["DNA cloning only", "ribosomal decoding only", "glycogen digestion"], "Donnan forces affect body fluid compartments."),
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
            questions.append({**BASE, "id": f"biochemistry-chemical-basis-{slug}-{qi:02d}", "topic": topic, "topicTitle": topic, "difficulty": "moderate" if qi <= 6 else "high" if qi <= 12 else "very high", "prompt": make_prompt(qi, row["clue"]), "options": opts, "answerIndex": opts.index(row["answer"]), "answer": row["answer"], "explanation": row["explanation"]})
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "biochemistry" and x.get("chapterTitle") == CHAPTER)] + questions
    if len(TOPICS) != 7 or len(questions) != 105:
        raise ValueError("Expected 7 topics and 105 questions")
    if len({q["id"] for q in questions}) != 105 or len({q["prompt"] for q in questions}) != 105:
        raise ValueError("Duplicate ids/prompts")
    if any(q["answer"] != q["options"][q["answerIndex"]] for q in questions):
        raise ValueError("Bad answer mapping")
    data["questions"].sort(key=lambda item: item.get("id", ""))
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")

if __name__ == "__main__":
    main()
