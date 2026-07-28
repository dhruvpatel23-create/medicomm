import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "General Metabolism"
BASE = {"subjectId": "biochemistry", "subjectTitle": "Biochemistry", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}

STD = [
    "Which option best completes this metabolism statement: {clue}?",
    "What is the most appropriate answer for: {clue}?",
    "Which concept is most directly associated with: {clue}?",
    "Why is this point important in general metabolism: {clue}?",
    "Which interpretation is best for this finding: {clue}?",
    "How should this be classified in an exam question: {clue}?",
    "Which choice is the best single association for: {clue}?",
    "What does this source-book detail most strongly indicate: {clue}?",
    "Which statement is correct regarding: {clue}?",
    "How is this clue best applied clinically: {clue}?",
]
UNQ = [
    "A metabolism viva gives only this hint: '{clue}'. Choose the expected answer.",
    "Match the metabolic clue with the correct term: {clue}.",
    "A pathway diagram has a blank beside '{clue}'. Which label fits?",
    "Assertion-reason style: the assertion depends on '{clue}'. Select the correct reason.",
    "A final-year MCQ uses this practical clue: '{clue}'. What is the best answer?",
]
ORDER = [("s",0),("s",1),("u",0),("s",2),("s",3),("s",4),("u",1),("s",5),("s",6),("u",2),("s",7),("s",8),("u",3),("s",9),("u",4)]

def q(clue, answer, wrong, explanation):
    return {"clue": clue, "answer": answer, "wrong": wrong, "explanation": explanation}

TOPICS = [
("six-levels", "Study on Six Levels of Organizations", [
q("feeding animals diets lacking one ingredient reveals essential nutrients", "intact organism study", ["organ perfusion", "purified enzyme assay", "homogenate fractionation"], "Whole-animal studies reveal integrated nutrient requirements."),
q("Wohler showed injected benzoic acid is excreted as hippuric acid", "early intact-animal metabolic study", ["Warburg apparatus", "cell culture", "DNA sequencing"], "This was an early animal metabolic study."),
q("isolated organ is cannulated and perfused with Ringer solution", "organ perfusion", ["intact organism feeding", "purified enzyme assay", "genomics"], "Organ perfusion studies input-output metabolism."),
q("50 micrometer liver slice preserving organelles is used", "organ slice experiment", ["whole animal trial", "single enzyme assay", "polymerase chain reaction"], "Organ slices preserve architecture."),
q("Warburg apparatus studied tissue respiration using", "organ slices", ["DNA probes", "serum electrophoresis", "food exchange"], "Warburg studied respiration in tissue slices."),
q("defined medium keeps cells alive for metabolic studies", "tissue culture", ["organ perfusion", "bomb calorimetry", "nitrogen balance"], "Cell culture permits controlled studies."),
q("labelled glucose incorporation into glycogen in cultured cells indicates", "tracer study in cell culture", ["enzyme denaturation", "simple diffusion only", "protein sequencing"], "Labels reveal metabolic fate."),
q("hybridoma culture supernatant can yield", "monoclonal antibodies", ["ketone bodies", "glycogen", "bile acids"], "Hybridoma cultures produce monoclonal antibodies."),
q("tissue is broken in isotonic medium and organelles separated", "homogenate fractionation", ["intact organism study", "prenatal screening", "gastric analysis"], "Homogenates allow subcellular studies."),
q("isolated mitochondria demonstrate enzymes of this pathway", "electron transport chain", ["brush-border digestion", "glycogen storage", "protein absorption"], "Mitochondria contain ETC enzymes."),
q("single enzyme preparation tests cofactors and regulation", "purified enzyme study", ["organ perfusion", "whole animal feeding", "tissue culture only"], "Purified enzymes isolate individual reactions."),
q("phenylketonuria traced to phenylalanine hydroxylase mutation is studied at", "DNA or genomics level", ["organ-slice level", "perfusion level", "BMR level"], "Gene defects explain enzyme disease."),
q("genomics, transcriptomics and proteomics examine", "genes, expression and products", ["only organ weight", "only dietary calories", "only body water"], "Modern studies operate at molecular levels."),
q("59Fe incorporation into marrow estimates", "RBC formation and heme turnover", ["gastric acid output", "LDL oxidation", "albumin electrophoresis"], "Radioiron traces erythropoiesis."),
q("15N glycine appearing in heme, nucleic acids and creatinine shows", "precursor-product relationship", ["Donnan equilibrium", "glycemic index", "SDA"], "Isotope tracing proves metabolic relationships."),
]),
("pathways-control", "Metabolic Pathways and Control Mechanisms", [
q("organized cellular chemical reactions together are called", "metabolism", ["homeostasis only", "digestion only", "genomics only"], "Metabolism is the sum of organized cell reactions."),
q("degradation of energy-rich nutrients provides", "chemical energy", ["only genetic information", "only water", "only minerals"], "Catabolism provides energy."),
q("food materials are converted into building blocks of macromolecules", "precursor formation", ["oxygen transport", "bile excretion", "urine concentration"], "Metabolism supplies biosynthetic precursors."),
q("sequential enzyme systems form", "metabolic pathways", ["random reactions", "organ slices only", "genetic codes only"], "Pathways are ordered enzyme sequences."),
q("effector molecules alter activity of regulatory enzymes", "allosteric regulation", ["DNA-level regulation", "organ perfusion", "isotope tracing"], "Allosteric control changes enzyme activity rapidly."),
q("hormones coordinate pathway flux between organs", "hormonal regulation", ["enzyme purification", "Donnan effect", "Warburg apparatus"], "Hormones regulate metabolism systemically."),
q("enzyme amount changes because synthesis changes", "DNA-level regulation", ["allosteric regulation only", "organ perfusion", "primary digestion"], "Gene expression affects enzyme concentration."),
q("metabolic blocks help determine pathway steps", "perturbation analysis", ["steady-state anatomy", "food exchange", "albumin assay"], "Blocks reveal sequence/control."),
q("organisms with metabolic defects help reveal", "normal metabolic processes", ["body surface area", "gastric acid", "milk protein"], "Inborn errors clarify normal pathways."),
q("gene knockout is an example of", "genetic manipulation", ["organ perfusion", "nitrogen balance", "glycemic index"], "Knockouts test gene function."),
q("identifying order of intermediates studies", "sequence of reactions", ["calorie intake", "body weight", "CSF pressure"], "Pathway sequence is a core study aspect."),
q("following labelled precursor into product studies", "precursor-product relationship", ["enzyme surface area", "blood pressure", "exercise category"], "Tracer studies reveal product relationships."),
q("chemical steps of conversion are called", "mechanism of reaction", ["energy reserve", "organ profile", "diet prescription"], "Mechanism asks how reactions occur."),
q("feedback by ATP, citrate or AMP reflects", "control mechanisms", ["structural anatomy", "random flux", "protein malnutrition"], "Effectors control pathway flux."),
q("early fasting mainly changes activity of existing enzymes", "short-term fine control", ["long-term organ growth", "DNA deletion", "food exchange"], "Early control is rapid enzyme activity change."),
]),
("glucose-homeostasis", "Importance of Blood Glucose Homeostasis", [
q("blood glucose is maintained within narrow limits mainly for this organ", "brain", ["adipose tissue", "skin", "bone"], "Brain requires continuous glucose."),
q("brain has this type of glucose requirement", "obligatory requirement", ["optional requirement only", "no requirement", "cholesterol requirement"], "Brain needs glucose even when using ketones partly."),
q("RBCs depend on glucose because they lack", "mitochondria", ["hemoglobin", "membrane", "enzymes"], "RBCs rely on glycolysis."),
q("renal medulla also depends heavily on", "glucose", ["fatty acids", "ketone bodies only", "cholesterol"], "Renal medulla uses glucose under low oxygen conditions."),
q("after a meal insulin promotes", "glucose uptake and storage", ["protein breakdown", "ketogenesis", "glycogenolysis"], "Insulin stores glucose as glycogen/fat."),
q("during fasting liver maintains glucose first by", "glycogenolysis", ["ketolysis", "lipogenesis", "protein synthesis"], "Hepatic glycogen maintains early fasting glucose."),
q("later fasting maintains glucose mainly by", "gluconeogenesis", ["glycogenesis", "cholesterol synthesis", "DNA replication"], "Gluconeogenesis replaces glycogenolysis."),
q("glucagon promotes this in fasting", "hepatic glucose output", ["muscle glucose storage", "fat synthesis", "DNA splicing"], "Glucagon raises glucose."),
q("low blood glucose below about 30 mg/dL may be", "fatal", ["always harmless", "required for brain", "normal post-meal value"], "Severe hypoglycemia threatens brain function."),
q("muscle shifts to fatty acids in fasting to spare", "glucose for brain", ["cholesterol for liver", "albumin for kidney", "bile salts"], "Muscle reduces glucose use during fasting."),
q("reciprocal regulation of glycolysis and gluconeogenesis controls", "metabolic flux", ["chromosome segregation", "organ perfusion", "body height"], "Flux depends on reciprocal control."),
q("fed state is associated with high", "insulin", ["glucagon", "ketone bodies", "free fatty acids only"], "Insulin rises after meals."),
q("fasting state is associated with high", "glucagon-insulin ratio", ["insulin-only ratio", "albumin-globulin ratio", "LDL-HDL ratio"], "Fasting raises glucagon relative to insulin."),
q("maintenance of glucose across fed and fasting states is", "caloric homeostasis", ["DNA repair", "protein sequencing", "milk synthesis"], "Fuel regulation maintains energy supply."),
q("diabetes disrupts glucose homeostasis through impaired", "insulin action or secretion", ["albumin synthesis only", "bile acid recycling", "gastric secretion"], "Diabetes involves insulin deficiency/resistance."),
]),
("organ-profile", "Metabolic Profile of Organs", [
q("brain normally prefers this fuel", "glucose", ["fatty acids", "urea", "cholesterol"], "Brain normally uses glucose."),
q("brain cannot use fatty acids well because albumin-bound fatty acids cannot cross", "blood-brain barrier", ["glomerulus", "gastric mucosa", "bile canaliculus"], "Fatty acids do not cross BBB readily."),
q("during prolonged starvation brain uses", "ketone bodies", ["bilirubin", "LDL", "urea"], "Ketones support brain in starvation."),
q("resting skeletal muscle uses mainly", "fatty acids", ["glucose only", "ammonia", "bilirubin"], "Resting muscle prefers fatty acids."),
q("short active spurts in muscle use", "glycogen to lactate", ["fat to bile", "protein to DNA", "ketone to urea"], "Anaerobic bursts use glycogen."),
q("lactate from muscle returns to liver in", "Cori cycle", ["urea cycle", "Donnan cycle", "Krebs cycle only"], "Cori cycle recycles lactate."),
q("prolonged fasting muscle releases this amino acid to liver", "alanine", ["tyrosine", "histidine", "tryptophan"], "Alanine carries carbon and nitrogen."),
q("adipose tissue stores energy as", "triacylglycerol", ["glycogen", "albumin", "DNA"], "Adipose stores TAG."),
q("adipose lipoprotein lipase is activated by", "insulin", ["glucagon", "thyroxine only", "cortisol only"], "Insulin favors fat storage."),
q("fasting activates this adipose enzyme", "hormone-sensitive lipase", ["glucokinase", "DNA ligase", "lactase"], "HSL releases fatty acids."),
q("liver provides glucose in starvation by glycogenolysis and", "gluconeogenesis", ["ketolysis", "albumin degradation only", "glycosylation"], "Liver maintains blood glucose."),
q("liver produces but cannot use", "ketone bodies", ["glucose", "albumin", "urea"], "Liver lacks ketolysis enzyme."),
q("heart mainly uses oxidative metabolism of", "fatty acids", ["lactose", "bilirubin", "DNA"], "Heart relies heavily on fatty acids."),
q("heart energy buffer uses", "creatine kinase shuttle", ["Donnan equilibrium", "Cori cycle", "glycemic index"], "Creatine kinase transfers high-energy phosphate."),
q("hypertrophied heart shifts fuel use toward", "glucose", ["bilirubin", "urea", "cholesterol"], "Hypertrophied heart uses more glucose."),
]),
("starvation", "Metabolic Adaptations During Starvation", [
q("first stage of fasting maintains blood glucose by", "glycogenolysis", ["ketolysis", "lipogenesis", "glycogenesis"], "Early fasting uses liver glycogen."),
q("hepatic glycogen stores last about", "18 hours", ["3 days", "10 days", "60 days"], "Glycogen reserves are limited."),
q("gluconeogenesis accelerates even before", "glycogen depletion", ["DNA replication", "albumin synthesis", "bile obstruction"], "Gluconeogenesis begins early."),
q("major gluconeogenic substrate from muscle is", "amino acids", ["cholesterol", "bile salts", "fat-soluble vitamins"], "Muscle protein provides amino acids."),
q("amino nitrogen reaches liver mainly as", "alanine", ["bilirubin", "creatine", "lactose"], "Alanine safely transports nitrogen."),
q("branched-chain amino acids are used by", "skeletal muscle", ["RBCs", "adipose only", "brain only"], "Muscle oxidizes BCAA."),
q("plasma branched-chain amino acids peak around this starvation day", "5th day", ["1st hour", "10th minute", "60th day"], "The chapter notes peak around day 5."),
q("high glucagon-insulin ratio stimulates", "lipolysis", ["glycogenesis", "protein synthesis", "fat storage"], "Fasting activates fat breakdown."),
q("hormone-sensitive lipase releases", "free fatty acids", ["DNA primers", "bile acids", "albumin"], "HSL hydrolyzes TAG."),
q("muscle, heart and kidney reduce glucose use and depend on", "fatty acids", ["glucose only", "bilirubin", "lactose"], "FFA become major fasting fuels."),
q("pyruvate dehydrogenase is inactivated by", "phosphorylation", ["glycosylation", "splicing", "translation"], "PDH inhibition spares glucose."),
q("liver converts acetyl CoA to", "ketone bodies", ["glycogen", "albumin", "DNA"], "Ketogenesis increases in fasting."),
q("brain starts using ketone bodies from about", "3rd day of starvation", ["first minute", "after 18 hours only", "after 60 days"], "Brain adapts to ketones after several days."),
q("by 10th day, about this brain energy comes from ketones", "60 percent", ["5 percent", "100 percent", "0 percent"], "Ketones supply major brain energy by day 10."),
q("excess ketone bodies can cause", "metabolic acidosis", ["respiratory alkalosis only", "albuminuria", "hyperlipidemia only"], "Ketosis may progress to acidosis."),
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
            questions.append({**BASE, "id": f"biochemistry-general-metabolism-{slug}-{qi:02d}", "topic": topic, "topicTitle": topic, "difficulty": "moderate" if qi <= 6 else "high" if qi <= 12 else "very high", "prompt": make_prompt(qi, row["clue"]), "options": opts, "answerIndex": opts.index(row["answer"]), "answer": row["answer"], "explanation": row["explanation"]})
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

if __name__ == "__main__":
    main()
