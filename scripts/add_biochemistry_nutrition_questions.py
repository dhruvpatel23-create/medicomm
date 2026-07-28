import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Nutrition"
BASE = {"subjectId": "biochemistry", "subjectTitle": "Biochemistry", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}

STD = [
    "Which option best completes this nutrition statement: {clue}?",
    "What is the most appropriate answer for: {clue}?",
    "Which value, vitamin, mineral or concept is most directly associated with: {clue}?",
    "Why is this point important in nutrition: {clue}?",
    "Which interpretation is best for this finding: {clue}?",
    "How should this be classified in an exam question: {clue}?",
    "Which choice is the best single association for: {clue}?",
    "What does this source-book detail most strongly indicate: {clue}?",
    "Which statement is correct regarding: {clue}?",
    "How is this clue best applied clinically: {clue}?",
]
UNQ = [
    "A nutrition viva gives only this hint: '{clue}'. Choose the expected answer.",
    "Match the nutrition clue with the correct term: {clue}.",
    "A clinical nutrition chart has a blank beside '{clue}'. Which label fits?",
    "Assertion-reason style: the assertion depends on '{clue}'. Select the correct reason.",
    "A final-year MCQ uses this practical clue: '{clue}'. What is the best answer?",
]
ORDER = [("s",0),("s",1),("u",0),("s",2),("s",3),("s",4),("u",1),("s",5),("s",6),("u",2),("s",7),("s",8),("u",3),("s",9),("u",4)]

def q(clue, answer, wrong, explanation):
    return {"clue": clue, "answer": answer, "wrong": wrong, "explanation": explanation}

TOPICS = [
("fat-soluble", "Fat Soluble Vitamins (A, D, E, K)", [
q("night blindness and xerophthalmia are caused by deficiency of", "vitamin A", ["vitamin D", "vitamin E", "vitamin K"], "Vitamin A is required for vision and epithelial health."),
q("retinal combines with opsin in Wald visual cycle to form", "rhodopsin", ["calcitriol", "tocopherol", "prothrombin"], "Rhodopsin is the visual pigment of rods."),
q("Bitot spots are classically associated with deficiency of", "vitamin A", ["vitamin K", "vitamin E", "vitamin D"], "Bitot spots occur in vitamin A deficiency."),
q("active vitamin D hormone is", "calcitriol", ["retinol", "tocopherol", "phylloquinone"], "Calcitriol is 1,25-dihydroxy vitamin D."),
q("vitamin D increases intestinal absorption of", "calcium and phosphate", ["iron and copper", "sodium and chloride", "iodine and selenium"], "Vitamin D supports calcium-phosphate homeostasis."),
q("rickets is due to deficiency of", "vitamin D", ["retinol deficiency", "tocopherol deficiency", "vitamin K dependent clotting defect"], "Vitamin D deficiency causes rickets in children."),
q("osteomalacia is adult deficiency manifestation of", "vitamin D", ["night blindness", "hemolysis in premature infants", "prolonged prothrombin time"], "Vitamin D deficiency causes defective mineralization."),
q("major antioxidant vitamin protecting membranes", "vitamin E", ["retinal in visual cycle", "calcitriol for calcium absorption", "phylloquinone for coagulation"], "Vitamin E is a lipid-phase antioxidant."),
q("hemolysis in premature infants may occur with deficiency of", "vitamin E", ["xerophthalmia", "rickets", "warfarin-like bleeding"], "Vitamin E deficiency can cause RBC membrane injury."),
q("gamma-carboxylation of clotting factors requires", "vitamin K", ["tocopherol antioxidant action", "retinoic acid epithelial action", "calcitriol endocrine action"], "Vitamin K is needed for clotting factor activation."),
q("prothrombin time is prolonged in deficiency of", "vitamin K", ["night blindness vitamin", "bone mineralization vitamin", "membrane antioxidant vitamin"], "Vitamin K deficiency impairs coagulation."),
q("warfarin antagonizes", "vitamin K", ["vitamin A", "vitamin D", "vitamin E"], "Warfarin blocks vitamin K recycling."),
q("bile obstruction can cause deficiency of fat-soluble vitamins because it impairs", "fat absorption", ["protein synthesis only", "glucose transport", "renal excretion"], "Fat-soluble vitamins need bile-mediated fat absorption."),
q("hypervitaminosis A may cause raised intracranial pressure and", "skin and liver toxicity", ["rickets", "hemolytic anemia only", "bleeding tendency only"], "Excess vitamin A is toxic."),
q("vitamin K is produced partly by", "intestinal bacteria", ["pancreatic beta cells", "thyroid gland", "RBCs"], "Gut bacteria contribute vitamin K."),
]),
("water-soluble", "Water Soluble Vitamins", [
q("thiamine deficiency causes", "beriberi", ["scurvy", "pellagra", "rickets"], "Vitamin B1 deficiency causes beriberi."),
q("thiamine pyrophosphate is needed for oxidative decarboxylation of", "alpha-keto acids", ["fatty acids only", "cholesterol", "heme"], "TPP is a coenzyme for pyruvate and alpha-ketoglutarate dehydrogenases."),
q("riboflavin forms these coenzymes", "FMN and FAD", ["NAD and NADP", "TPP and PLP", "THF and B12"], "Vitamin B2 forms flavin coenzymes."),
q("niacin forms these coenzymes", "NAD and NADP", ["FMN and FAD", "TPP and PLP", "biotin and THF"], "Niacin is precursor of NAD/NADP."),
q("pellagra is classically dermatitis, diarrhea and", "dementia", ["night blindness", "rickets", "bleeding"], "Niacin deficiency causes the three Ds."),
q("pyridoxal phosphate is the active form of", "vitamin B6", ["vitamin B1", "vitamin B2", "vitamin B12"], "PLP is active B6."),
q("transamination reactions require", "pyridoxal phosphate", ["ascorbate", "biotin", "cobalamin"], "PLP is coenzyme for aminotransferases."),
q("biotin is required for", "carboxylation reactions", ["decarboxylation by TPP", "hydroxylation of collagen only", "gamma carboxylation of clotting factors"], "Biotin carries CO2 in carboxylases."),
q("folic acid carries", "one-carbon units", ["oxygen", "fatty acids", "calcium"], "THF transfers one-carbon groups."),
q("folate deficiency causes", "megaloblastic anemia", ["microcytic anemia", "hemolytic anemia", "aplastic anemia only"], "Folate is needed for DNA synthesis."),
q("vitamin B12 deficiency causes megaloblastic anemia with", "neurological features", ["night blindness", "rickets", "bleeding gums only"], "B12 deficiency can affect myelin."),
q("folate trap occurs in deficiency of", "vitamin B12", ["vitamin C", "niacin", "riboflavin"], "B12 deficiency traps folate as methyl-THF."),
q("vitamin C is required for hydroxylation of proline and lysine in", "collagen", ["glycogen", "DNA", "cholesterol"], "Ascorbate supports collagen synthesis."),
q("scurvy is due to deficiency of", "vitamin C", ["vitamin B12", "vitamin B6", "niacin"], "Scurvy causes bleeding gums and poor wound healing."),
q("pantothenic acid is a component of", "coenzyme A", ["NAD", "FAD", "THF"], "Pantothenate forms CoA."),
]),
("minerals", "Mineral Metabolism and Abnormalities", [
q("major mineral of bone hydroxyapatite", "calcium", ["iodine", "selenium", "chromium"], "Calcium is the main bone mineral cation."),
q("parathyroid hormone increases serum", "calcium", ["iodine", "iron", "chloride"], "PTH raises serum calcium."),
q("calcitonin tends to lower serum", "calcium", ["iron", "copper", "iodine"], "Calcitonin opposes bone resorption."),
q("phosphate is abundant in bone and in", "ATP and nucleic acids", ["thyroxine only", "hemoglobin only", "ceruloplasmin only"], "Phosphate has structural and energy roles."),
q("magnesium is important as a cofactor for enzymes using", "ATP", ["bilirubin", "cholesterol only", "albumin"], "ATP often acts as Mg-ATP complex."),
q("iron deficiency causes", "microcytic hypochromic anemia", ["megaloblastic anemia", "rickets", "scurvy"], "Iron deficiency impairs hemoglobin synthesis."),
q("major storage protein for iron", "ferritin", ["transferrin", "ceruloplasmin", "albumin"], "Ferritin stores iron."),
q("plasma transport protein for iron", "transferrin", ["ferritin", "hemosiderin", "metallothionein"], "Transferrin transports iron."),
q("copper transport protein in plasma", "ceruloplasmin", ["transferrin", "ferritin", "albumin only"], "Ceruloplasmin carries copper."),
q("Wilson disease is due to disordered metabolism of", "copper", ["iron", "iodine", "selenium"], "Wilson disease causes copper accumulation."),
q("iodine deficiency causes", "goiter and hypothyroidism", ["hemolysis", "scurvy", "rickets only"], "Iodine is needed for thyroid hormone synthesis."),
q("zinc is important for wound healing and many", "metalloenzymes", ["bile salts", "fat-soluble vitamins only", "ketone bodies"], "Zinc functions in multiple enzymes."),
q("fluoride deficiency increases risk of", "dental caries", ["goiter", "Wilson disease", "hemolysis"], "Fluoride protects enamel."),
q("selenium is part of", "glutathione peroxidase", ["hemoglobin", "transferrin", "calcitonin"], "Selenium supports antioxidant defense."),
q("chromium is linked with action of", "insulin", ["thyroxine", "PTH", "calcitonin"], "Chromium is associated with glucose tolerance."),
]),
("energy-nutrition", "Energy Metabolism and Nutrition", [
q("one kilocalorie equals", "1000 calories", ["100 calories", "4 calories", "9 calories"], "Food energy is expressed in kcal."),
q("carbohydrate yields", "4 kcal/g", ["9 kcal/g", "7 kcal/g", "0 kcal/g"], "Carbohydrate provides 4 kcal/g."),
q("fat yields", "9 kcal/g", ["4 kcal/g", "7 kcal/g", "1 kcal/g"], "Fat is energy dense."),
q("protein yields about", "4 kcal/g", ["9 kcal/g", "7 kcal/g", "0 kcal/g"], "Protein is counted near 4 kcal/g in diet calculations."),
q("RQ of carbohydrate is", "1.0", ["0.7", "0.8", "0.66"], "Carbohydrate RQ is 1."),
q("RQ of fat is about", "0.7", ["1.0", "0.8", "1.2"], "Fat RQ is about 0.7."),
q("BMR is energy required at complete rest in awake state", "basal metabolic rate", ["glycemic index", "nitrogen balance", "food exchange"], "BMR is basal energy expenditure."),
q("fever increases BMR by about this per degree Celsius", "12 percent", ["1 percent", "50 percent", "0 percent"], "Fever raises BMR."),
q("protein has SDA of about", "30 percent", ["5 percent", "15 percent", "0 percent"], "Protein has high thermogenic effect."),
q("mixed diet needs extra calories for SDA of about", "10 percent", ["30 percent", "50 percent", "0 percent"], "Mixed diet SDA is about 10%."),
q("fiber requirement is about", "30 g/day", ["3 g/day", "100 g/day", "1 g/day"], "The chapter states fiber requirement around 30 g/day."),
q("safe adult protein intake is about", "0.75-0.8 g/kg/day", ["2.5 g/kg/day", "10 g/kg/day", "30 g/day"], "Adult safe protein allowance is around 0.8 g/kg/day."),
q("kwashiorkor is mainly deficiency of", "protein", ["calorie only", "vitamin D", "iodine"], "Kwashiorkor is protein-energy malnutrition with protein deficiency."),
q("marasmus is mainly deficiency of", "calories", ["vitamin K", "copper", "iodine"], "Marasmus is severe calorie deficiency."),
q("glycemic index compares response to a test meal with", "50 g glucose", ["50 g fat", "50 g protein", "BMR"], "GI uses glucose reference."),
]),
("detoxification", "Detoxification and Biotransformation of Xenobiotics", [
q("biotransformation converts xenobiotics into more", "polar metabolites", ["nonpolar gases", "storage fats", "DNA polymers"], "Polar metabolites are more readily excreted."),
q("major organ for biotransformation", "liver", ["brain", "bone", "RBC"], "Liver is the main detoxifying organ."),
q("phase I reactions include oxidation, reduction and", "hydrolysis", ["conjugation only", "translation", "glycogenesis"], "Phase I functionalizes compounds."),
q("cytochrome P450 enzymes are mainly involved in", "phase I oxidation", ["phase II methylation only", "DNA replication", "protein folding"], "CYP enzymes oxidize xenobiotics."),
q("phase II reactions are mainly", "conjugation reactions", ["only oxidation", "only reduction", "only hydrolysis"], "Phase II adds polar groups."),
q("glucuronic acid conjugation uses", "UDP-glucuronic acid", ["ATP only", "NADH only", "FAD only"], "UDPGA donates glucuronic acid."),
q("sulfate conjugation uses", "PAPS", ["PRPP", "SAM only", "CoA only"], "PAPS is active sulfate donor."),
q("methylation reactions commonly use", "S-adenosyl methionine", ["UDP-glucose", "NADPH only", "biotin"], "SAM donates methyl groups."),
q("acetylation requires", "acetyl CoA", ["FAD", "THF only", "heme"], "Acetyl CoA donates acetyl group."),
q("glutathione conjugation protects against", "electrophilic toxic metabolites", ["vitamin deficiency only", "mineral absorption", "fiber loss"], "GSH detoxifies reactive intermediates."),
q("phase III reactions involve", "transport and excretion", ["DNA transcription", "protein synthesis", "BMR measurement"], "Transporters help remove metabolites."),
q("some drugs are activated rather than inactivated by metabolism", "prodrug activation", ["vitamin storage", "glycemic index", "nitrogen balance"], "Some metabolites are therapeutic."),
q("enzyme induction can increase drug metabolism by increasing", "detoxifying enzyme levels", ["body water only", "serum albumin only", "bone calcium only"], "Induction increases metabolizing enzymes."),
q("enzyme inhibition can cause", "drug toxicity", ["immediate vitamin synthesis", "zero drug levels", "no interaction"], "Inhibition raises active drug levels."),
q("biotransformation protects body by enhancing", "excretion of xenobiotics", ["storage in fat always", "DNA mutation", "protein-energy malnutrition"], "Detoxication favors elimination."),
]),
("pollution-poisons", "Environmental Pollution and Heavy Metal Poisons", [
q("organophosphorus compounds inhibit", "acetylcholinesterase", ["xanthine oxidase", "DNA ligase", "lactase"], "Organophosphates cause cholinergic toxicity."),
q("lead poisoning inhibits heme synthesis and causes", "anemia", ["rickets", "scurvy", "goiter"], "Lead interferes with heme synthesis."),
q("lead poisoning may show basophilic stippling in", "RBCs", ["platelets", "neutrophils only", "osteoclasts"], "Basophilic stippling is a classic lead finding."),
q("mercury toxicity primarily affects nervous system and", "kidney", ["thyroid only", "pancreas only", "adipose only"], "Mercury damages CNS and kidney."),
q("arsenic poisoning can affect skin, GI tract and", "nervous system", ["lens only", "cartilage only", "hair pigment only"], "Arsenic is multisystem toxic."),
q("aluminium toxicity is important in patients with", "renal failure", ["hyperthyroidism", "scurvy", "night blindness"], "Aluminium may accumulate when renal excretion is poor."),
q("corrosive poisons produce damage mainly by", "local tissue destruction", ["DNA replication", "glycemic response", "vitamin storage"], "Corrosives injure tissues directly."),
q("sulfur dioxide is an example of", "air pollutant", ["fat-soluble vitamin", "trace element", "coenzyme"], "SO2 is listed among air pollutants."),
q("industrial hazards may expose workers to", "toxic chemicals and metals", ["only carbohydrates", "only vitamins", "only amino acids"], "Occupational exposure is a pollution risk."),
q("pesticides and insecticides are important environmental", "toxicants", ["coenzymes", "dietary fibers", "essential amino acids"], "They can poison humans and ecosystems."),
q("lathyrism is linked with toxic substance in", "foodstuffs", ["air only", "water only", "blood plasma"], "Lathyrism is a food toxin-related disease."),
q("heavy metals often bind to sulfhydryl groups of", "enzymes", ["DNA codons only", "triglycerides", "cellulose"], "Metal toxicity often inhibits enzymes."),
q("chelation therapy works by", "binding metals for excretion", ["raising glycemic index", "increasing BMR", "synthesizing vitamins"], "Chelators help remove metals."),
q("environmental toxicology is clinically important because exposure may be", "chronic and cumulative", ["always harmless", "only genetic", "always nutritional"], "Many toxins accumulate over time."),
q("prevention of poisoning depends strongly on", "exposure control", ["increasing dose", "ignoring workplace safety", "removing all vitamins"], "Reducing exposure is key."),
]),
]

def prompt(i, clue):
    kind, n = ORDER[i-1]
    return (STD if kind == "s" else UNQ)[n].format(clue=clue)

def rotate(items, offset):
    if not items: return []
    offset %= len(items)
    return items[offset:] + items[:offset]

def options(answer, wrong, topic_answers, chapter_answers, offset):
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
            opts = options(row["answer"], row["wrong"], topic_answers, chapter_answers, ti + qi)
            questions.append({**BASE, "id": f"biochemistry-nutrition-{slug}-{qi:02d}", "topic": topic, "topicTitle": topic, "difficulty": "moderate" if qi <= 6 else "high" if qi <= 12 else "very high", "prompt": prompt(qi, row["clue"]), "options": opts, "answerIndex": opts.index(row["answer"]), "answer": row["answer"], "explanation": row["explanation"]})
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "biochemistry" and x.get("chapterTitle") == CHAPTER)] + questions
    if len(TOPICS) != 6 or len(questions) != 90:
        raise ValueError("Expected 6 topics and 90 questions")
    if len({q["id"] for q in questions}) != 90 or len({q["prompt"] for q in questions}) != 90:
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
