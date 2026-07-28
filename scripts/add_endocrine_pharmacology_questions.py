import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Endocrine Pharmacology"
BASE = {"subjectId": "pharmacology", "subjectTitle": "Pharmacology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("hypothalamic-pituitary-axis", "Introduction to Endocrinology: The Hypothalamic-Pituitary Axis", [
        q("A woman with infertility receives pulsatile GnRH and ovulates. Why must GnRH be pulsatile for this effect?", "Continuous GnRH downregulates pituitary receptors, while pulses stimulate LH and FSH", ["Continuous GnRH increases prolactin only", "Pulses block ovarian steroid synthesis", "GnRH directly ruptures the follicle"], "Physiologic pulsatile GnRH drives gonadotropin release; continuous exposure suppresses the axis."),
        q("Leuprolide is used for prostate cancer after an initial flare. The long-term effect is:", "Pituitary GnRH receptor downregulation with reduced LH and testosterone", ["Direct androgen receptor activation", "Increased adrenal cortisol synthesis", "Permanent aromatase activation"], "Continuous GnRH agonists first stimulate then suppress gonadotropins."),
        q("A patient starting leuprolide for metastatic prostate cancer is briefly given an antiandrogen because:", "Initial LH surge can transiently worsen androgen-sensitive disease", ["Leuprolide causes immediate adrenal crisis", "Antiandrogens prevent pituitary apoptosis", "GnRH agonists cannot affect testes"], "GnRH agonist flare can be clinically important; androgen blockade can blunt it."),
        q("A patient with acromegaly after pituitary surgery receives octreotide. It lowers GH because it is a:", "Somatostatin receptor agonist", ["Dopamine D2 antagonist", "GnRH receptor blocker", "ACTH analog"], "Somatostatin analogs suppress GH secretion and can help acromegaly."),
        q("A patient with hyperprolactinemia and galactorrhea is treated with cabergoline. The mechanism is:", "D2 receptor agonism suppressing prolactin release", ["D2 receptor blockade", "Oxytocin receptor antagonism", "TRH receptor activation"], "Dopamine tonically inhibits prolactin secretion through D2 receptors."),
        q("Desmopressin improves central diabetes insipidus because it:", "Activates V2 receptors to increase collecting duct water reabsorption", ["Blocks aldosterone receptors", "Inhibits aquaporin insertion", "Stimulates glucose excretion"], "Desmopressin is a vasopressin analog with strong V2 activity."),
        q("A patient on desmopressin develops headache, confusion, and seizures. The likely toxicity is:", "Water retention causing hyponatremia", ["Severe hypernatremia", "Thyroid storm", "Androgen excess"], "Excess V2 activity can retain free water and cause hyponatremia."),
        q("Tolvaptan helps SIADH by:", "Blocking V2 receptors and promoting free water excretion", ["Activating V2 receptors", "Increasing ADH release", "Blocking mineralocorticoid receptors only"], "Vaptans are vasopressin receptor antagonists that cause aquaresis."),
        q("Oxytocin used for labor induction can cause fetal distress mainly through:", "Excess uterine contractions reducing uteroplacental perfusion", ["Complete progesterone blockade", "Direct fetal beta-blockade", "Maternal thyroid suppression"], "Overstimulation of the uterus can compromise fetal oxygenation."),
        q("A patient with Cushing disease receives pasireotide. Its rationale is broader activation of:", "Somatostatin receptor subtypes on pituitary tumor cells", ["Insulin receptors in liver", "V2 receptors in kidney", "Mineralocorticoid receptors"], "Pasireotide is a somatostatin analog used in selected pituitary hormone excess states."),
    ]),
    ("thyroid-antithyroid", "Thyroid and Antithyroid Drugs", [
        q("A patient with hypothyroidism starts levothyroxine. Why is TSH checked weeks later rather than the next day?", "Thyroxine has a long half-life and pituitary TSH equilibrates slowly", ["Levothyroxine is inactive for months", "TSH cannot respond to T4", "T3 is stored only in bone"], "Levothyroxine has slow pharmacokinetics; dose assessment needs steady state."),
        q("A patient taking levothyroxine with iron has persistent high TSH. The likely issue is:", "Reduced GI absorption from chelation/binding", ["Increased thyroid receptor affinity", "Blocked renal TSH clearance", "Pituitary destruction by iron"], "Iron, calcium, and some foods/drugs reduce levothyroxine absorption."),
        q("Methimazole treats Graves disease by inhibiting:", "Thyroid peroxidase-mediated iodination and coupling", ["Peripheral beta receptors", "TSH receptor binding directly", "Iodide uptake only"], "Thionamides block thyroid hormone synthesis through thyroid peroxidase inhibition."),
        q("Propylthiouracil is preferred in thyroid storm partly because it also:", "Inhibits peripheral T4 to T3 conversion", ["Activates TSH release", "Blocks beta receptors irreversibly", "Destroys stored thyroglobulin instantly"], "PTU inhibits hormone synthesis and high-dose PTU reduces peripheral conversion."),
        q("A patient on methimazole develops fever and sore throat. The urgent concern is:", "Agranulocytosis", ["Ototoxicity", "Pulmonary fibrosis", "Hyperkalemia"], "Thionamides can rarely cause severe neutropenia; symptoms require prompt CBC evaluation."),
        q("Iodide is given before thyroid surgery in Graves disease because it:", "Acutely reduces hormone release and thyroid vascularity", ["Stimulates lifelong hormone synthesis", "Destroys thyroid tissue by radiation", "Blocks adrenergic receptors"], "High-dose iodide transiently suppresses organification/release and decreases vascularity."),
        q("Radioactive iodine is avoided in pregnancy because it:", "Can ablate the fetal thyroid", ["Causes fetal opioid withdrawal", "Induces maternal hypoglycemia only", "Blocks folate absorption"], "I-131 crosses to the fetus and can damage fetal thyroid tissue."),
        q("Propranolol improves tremor and tachycardia in thyrotoxicosis because it:", "Blocks beta-adrenergic manifestations and at high doses reduces T4 to T3 conversion", ["Inhibits thyroid peroxidase directly", "Blocks TSH receptors", "Chelates iodine"], "Beta blockers control adrenergic symptoms; propranolol has some conversion effect."),
        q("Amiodarone can cause hypo- or hyperthyroidism because it:", "Contains iodine and affects thyroid hormone metabolism", ["Activates pituitary GnRH", "Blocks insulin receptors", "Destroys adrenal cortex"], "Amiodarone is iodine-rich and alters thyroid physiology."),
        q("Cholestyramine can help severe thyrotoxicosis as adjunct therapy by:", "Interrupting enterohepatic circulation of thyroid hormone", ["Stimulating TSH release", "Activating deiodinase", "Blocking thyroid hormone receptors"], "Bile acid resins can increase fecal thyroid hormone loss."),
    ]),
    ("estrogens-progestins-female-reproductive", "Estrogens, Progestins, and the Female Reproductive Tract", [
        q("Combined oral contraceptives prevent pregnancy mainly by:", "Suppressing LH surge and ovulation", ["Increasing FSH surge", "Activating sperm motility", "Stimulating implantation"], "Estrogen plus progestin suppresses gonadotropins; progestin thickens cervical mucus."),
        q("A patient taking combined contraception has migraine with aura. Why is this concerning?", "Higher ischemic stroke risk with estrogen-containing contraception", ["Guaranteed ovarian failure", "Loss of contraceptive efficacy", "Immediate ectopic pregnancy"], "Estrogen-containing methods are avoided in migraine with aura due to vascular risk."),
        q("A progestin-only pill is useful during breastfeeding because it:", "Avoids estrogen-related reduction in milk supply and thrombotic risk", ["Has no need for adherence", "Always suppresses lactation", "Contains GnRH"], "Progestin-only contraception is often chosen postpartum/lactation settings."),
        q("Levonorgestrel emergency contraception works primarily by:", "Delaying or inhibiting ovulation", ["Disrupting an implanted pregnancy", "Blocking progesterone receptors for months", "Activating uterine contractions"], "Emergency levonorgestrel is most effective before ovulation and does not terminate established pregnancy."),
        q("Ulipristal is effective for emergency contraception because it is a:", "Selective progesterone receptor modulator", ["Estrogen receptor pure agonist", "Aromatase enzyme", "GnRH antagonist"], "Ulipristal modulates progesterone receptors and delays ovulation."),
        q("Mifepristone with misoprostol terminates early pregnancy because mifepristone:", "Blocks progesterone receptors and sensitizes uterus to prostaglandin", ["Activates estrogen receptors", "Inhibits prolactin", "Blocks oxytocin receptors"], "Progesterone withdrawal plus prostaglandin-induced contractions causes medical abortion."),
        q("Clomiphene induces ovulation in anovulatory infertility by:", "Blocking estrogen feedback at hypothalamus/pituitary to increase FSH and LH", ["Activating ovarian estrogen receptors only", "Suppressing GnRH pulses", "Destroying corpus luteum"], "Clomiphene is a SERM that increases gonadotropin drive."),
        q("Letrozole can induce ovulation in PCOS because it:", "Inhibits aromatase and reduces estrogen negative feedback", ["Blocks progesterone receptors", "Activates prolactin release", "Stimulates androgen receptors"], "Aromatase inhibition increases gonadotropin secretion and follicular development."),
        q("Tamoxifen helps ER-positive breast cancer but increases endometrial cancer risk because it:", "Antagonizes breast ER while partially agonizing endometrial ER", ["Blocks all estrogen receptors equally in every tissue", "Inhibits aromatase irreversibly", "Activates HER2"], "SERMs have tissue-selective agonist/antagonist actions."),
        q("Aromatase inhibitors are most useful for ER-positive breast cancer in postmenopausal women because:", "Peripheral aromatization is the main estrogen source after menopause", ["Ovaries make all estrogen after menopause", "They activate progesterone receptors", "They increase prolactin"], "Anastrozole/letrozole/exemestane lower peripheral estrogen synthesis."),
    ]),
    ("androgens-male-reproductive", "Androgens and the Male Reproductive Tract", [
        q("Testosterone replacement suppresses fertility because exogenous androgen:", "Reduces GnRH, LH, and FSH, lowering intratesticular testosterone and spermatogenesis", ["Directly increases FSH", "Activates spermatogonial meiosis", "Blocks aromatase only"], "Negative feedback suppresses the hypothalamic-pituitary-gonadal axis."),
        q("A patient on testosterone develops high hematocrit. The mechanism is increased:", "Erythropoiesis", ["Platelet destruction", "Vitamin K blockade", "Renal calcium wasting"], "Androgens can stimulate erythropoiesis, causing polycythemia."),
        q("Finasteride improves BPH symptoms by inhibiting:", "5-alpha-reductase conversion of testosterone to dihydrotestosterone", ["Aromatase conversion to estradiol", "Androgen receptor binding directly", "GnRH release"], "DHT drives prostate growth; 5-alpha-reductase inhibitors shrink prostate over months."),
        q("A patient taking finasteride has reduced PSA. The clinical implication is:", "PSA interpretation must account for drug-related lowering", ["PSA becomes useless forever", "Prostate cancer risk is eliminated", "PSA must double immediately"], "5-alpha-reductase inhibitors lower PSA, so screening interpretation is adjusted."),
        q("Flutamide treats prostate cancer by:", "Blocking androgen receptors", ["Inhibiting CYP17", "Activating GnRH receptors continuously", "Increasing LH action"], "Nonsteroidal antiandrogens antagonize androgen receptor signaling."),
        q("Abiraterone is paired with glucocorticoid because CYP17 inhibition can cause:", "Mineralocorticoid excess from upstream steroid precursors", ["Complete aldosterone deficiency only", "Severe insulin excess", "Histamine release"], "CYP17 blockade lowers cortisol/androgens and raises ACTH-driven mineralocorticoid precursors; steroids suppress ACTH."),
        q("Enzalutamide differs from older antiandrogens by strongly inhibiting:", "Androgen receptor signaling including nuclear translocation", ["Aromatase in adipose tissue", "5-alpha-reductase only", "Pituitary prolactin release"], "Enzalutamide is a potent androgen receptor pathway inhibitor."),
        q("Sildenafil treats erectile dysfunction by:", "Inhibiting PDE5 and preserving cGMP in corpus cavernosum", ["Increasing nitric oxide synthesis directly in all vessels", "Blocking alpha-1 receptors only", "Stimulating testosterone synthesis"], "PDE5 inhibitors enhance NO-cGMP-mediated smooth muscle relaxation."),
        q("Nitrates are contraindicated with sildenafil because:", "Excess cGMP can cause profound hypotension", ["Sildenafil blocks nitrate metabolism into cyanide", "Both stimulate aldosterone", "Both cause severe hyperkalemia"], "Nitrates increase cGMP and PDE5 inhibitors reduce its breakdown."),
        q("Anabolic steroid misuse can cause testicular atrophy because:", "Pituitary LH and FSH are suppressed by negative feedback", ["Testosterone cannot enter cells", "DHT synthesis rises only in testes", "Prolactin is eliminated"], "Suppressed gonadotropins reduce testicular stimulation and sperm production."),
    ]),
    ("acth-adrenal-steroids-cortex", "Adrenocorticotropic Hormone, Adrenal Steroids, and the Adrenal Cortex", [
        q("A patient on chronic prednisone stops abruptly and develops hypotension and weakness. The cause is:", "Suppressed HPA axis with adrenal insufficiency", ["Acute aldosterone excess", "Thyroid storm", "Insulin overdose"], "Long-term glucocorticoids suppress CRH/ACTH and adrenal cortisol production."),
        q("Glucocorticoids reduce inflammation partly by inducing lipocortin, which inhibits:", "Phospholipase A2", ["HMG-CoA reductase", "Factor Xa", "Thyroid peroxidase"], "Reduced arachidonic acid release decreases prostaglandin and leukotriene synthesis."),
        q("A patient on prednisone develops hyperglycemia, proximal weakness, and osteoporosis. These reflect:", "Catabolic and metabolic glucocorticoid effects", ["Selective mineralocorticoid blockade", "Pure androgen receptor activation", "Insulin receptor agonism"], "Glucocorticoids increase gluconeogenesis and protein/bone catabolism."),
        q("Dexamethasone is preferred when mineralocorticoid activity must be minimized because it has:", "High glucocorticoid potency with little sodium-retaining effect", ["No glucocorticoid activity", "Strong aldosterone receptor activation", "Only topical action"], "Dexamethasone has minimal mineralocorticoid activity."),
        q("Fludrocortisone treats primary adrenal insufficiency because it:", "Replaces mineralocorticoid activity", ["Blocks aldosterone receptors", "Inhibits cortisol synthesis", "Suppresses sodium retention"], "Fludrocortisone is a potent mineralocorticoid used for aldosterone replacement."),
        q("Spironolactone improves primary aldosteronism hypertension by:", "Antagonizing mineralocorticoid receptors", ["Inhibiting ACTH release", "Stimulating cortisol synthesis", "Blocking thyroid hormone receptors"], "MR blockade reduces sodium retention and potassium wasting."),
        q("Ketoconazole can reduce cortisol synthesis in Cushing syndrome because it:", "Inhibits adrenal steroidogenic CYP enzymes", ["Activates ACTH receptors", "Blocks glucocorticoid receptors only", "Stimulates cholesterol transport"], "At higher doses ketoconazole inhibits steroid synthesis."),
        q("Metyrapone is used diagnostically because it blocks:", "11-beta-hydroxylase", ["21-hydroxylase", "Aromatase", "5-alpha-reductase"], "Metyrapone reduces cortisol synthesis, testing pituitary ACTH reserve."),
        q("Mifepristone can treat hyperglycemia in Cushing syndrome by:", "Blocking glucocorticoid receptors", ["Destroying adrenal cortex", "Activating mineralocorticoid receptors", "Inhibiting insulin release"], "Mifepristone antagonizes glucocorticoid receptors, improving cortisol effects without lowering cortisol levels."),
        q("Primary adrenal crisis requires hydrocortisone because it provides:", "Rapid glucocorticoid effect with some mineralocorticoid activity", ["Only androgen blockade", "Only antithyroid action", "Only insulin secretion"], "Hydrocortisone is used acutely with fluids; it supplies cortisol-like activity."),
    ]),
    ("diabetes-hypoglycemia", "Endocrine Pancreas and Pharmacotherapy of Diabetes Mellitus and Hypoglycemia", [
        q("Metformin is first-line in type 2 diabetes partly because it:", "Reduces hepatic gluconeogenesis without causing weight gain", ["Closes beta-cell potassium channels", "Activates glucagon release", "Blocks insulin receptors"], "Metformin improves insulin sensitivity and hepatic glucose output and is weight neutral or modestly weight reducing."),
        q("Metformin is held during severe renal dysfunction because of risk of:", "Lactic acidosis", ["Thyroid storm", "Torsades from QT shortening", "Agranulocytosis"], "Reduced clearance and hypoxic states increase metformin-associated lactic acidosis risk."),
        q("Sulfonylureas lower glucose by:", "Closing beta-cell KATP channels to trigger insulin release", ["Blocking SGLT2 in kidney", "Activating GLP-1 receptors directly", "Inhibiting alpha-glucosidase only"], "Sulfonylureas stimulate insulin secretion and can cause hypoglycemia/weight gain."),
        q("A patient on glyburide has confusion and diaphoresis after skipping meals. The toxicity is:", "Hypoglycemia from insulin secretagogue action", ["DKA from SGLT2 inhibition", "Lactic acidosis from biguanide", "Pancreatitis from lipase inhibition"], "Sulfonylureas can produce prolonged hypoglycemia, especially with missed meals or renal impairment."),
        q("SGLT2 inhibitors lower glucose by:", "Increasing urinary glucose excretion in the proximal tubule", ["Increasing insulin secretion directly", "Blocking intestinal carbohydrate absorption only", "Replacing insulin receptors"], "SGLT2 blockade causes glucosuria and osmotic natriuresis."),
        q("A patient on empagliflozin develops abdominal pain, ketones, and only mildly elevated glucose. The concern is:", "Euglycemic diabetic ketoacidosis", ["Cholinergic crisis", "Thyroid storm", "Addison crisis from aldosterone blockade"], "SGLT2 inhibitors can rarely cause euglycemic DKA."),
        q("GLP-1 receptor agonists help diabetes and weight by:", "Increasing glucose-dependent insulin, reducing glucagon, slowing gastric emptying, and increasing satiety", ["Opening beta-cell KATP channels", "Blocking insulin receptors", "Increasing hepatic glucose output"], "GLP-1 agonists have incretin and appetite effects and low intrinsic hypoglycemia risk."),
        q("DPP-4 inhibitors increase incretin action by:", "Preventing GLP-1 and GIP degradation", ["Activating PPAR-gamma", "Blocking SGLT2", "Stimulating glucagon release"], "DPP-4 inhibition prolongs endogenous incretin hormones."),
        q("Pioglitazone improves insulin resistance through:", "PPAR-gamma activation", ["KATP channel closure", "GLP-1 receptor agonism", "Alpha-glucosidase inhibition"], "Thiazolidinediones activate PPAR-gamma, improving insulin sensitivity but may cause edema/weight gain."),
        q("Acarbose mainly reduces postprandial hyperglycemia by:", "Inhibiting intestinal alpha-glucosidases", ["Increasing renal glucose loss", "Stimulating basal insulin release", "Activating amylin receptors"], "Alpha-glucosidase inhibitors delay carbohydrate digestion and absorption."),
    ]),
    ("mineral-ion-bone", "Agents Affecting Mineral Ion Homeostasis and Bone Turnover", [
        q("Alendronate reduces vertebral fracture risk by:", "Inhibiting osteoclast-mediated bone resorption", ["Stimulating osteoclast proton pumps", "Blocking vitamin D receptors", "Increasing PTH continuously"], "Bisphosphonates bind bone mineral and impair osteoclast function."),
        q("A patient taking alendronate is told to remain upright after dosing to prevent:", "Esophagitis", ["Nephrogenic diabetes insipidus", "Thyroid storm", "Severe hypoglycemia"], "Oral bisphosphonates can irritate the esophagus; upright posture and water reduce risk."),
        q("Denosumab treats osteoporosis by blocking:", "RANKL", ["Calcitonin receptors", "PTH receptors", "Vitamin D activation"], "RANKL inhibition reduces osteoclast formation and activity."),
        q("Teriparatide builds bone when given intermittently because it:", "Stimulates osteoblast activity more than osteoclast activity", ["Continuously suppresses osteoblasts", "Blocks RANKL permanently", "Chelates calcium in gut"], "Intermittent PTH analog exposure is anabolic to bone."),
        q("Cinacalcet lowers PTH in secondary hyperparathyroidism by:", "Activating calcium-sensing receptors on parathyroid cells", ["Blocking vitamin D receptors", "Stimulating osteoclasts directly", "Inhibiting renal phosphate absorption only"], "Calcimimetics make parathyroid cells sense higher calcium, suppressing PTH release."),
        q("Calcitriol is useful in CKD mineral bone disease because it:", "Replaces active vitamin D to increase calcium absorption and suppress PTH", ["Blocks intestinal calcium absorption", "Inhibits PTH receptors", "Chelates phosphate only"], "Kidney disease reduces 1-alpha hydroxylation; active vitamin D can be needed."),
        q("Sevelamer lowers serum phosphate by:", "Binding phosphate in the gut", ["Increasing renal phosphate filtration", "Activating PTH receptors", "Inhibiting osteoclasts"], "Non-calcium phosphate binders reduce intestinal phosphate absorption."),
        q("Calcitonin can rapidly lower calcium partly by:", "Inhibiting osteoclast activity", ["Activating osteoclast RANK", "Increasing PTH secretion", "Increasing renal calcium reabsorption strongly"], "Calcitonin has a fast but modest antiresorptive effect."),
        q("Loop diuretics can help hypercalcemia after hydration because they:", "Increase renal calcium excretion", ["Increase distal calcium reabsorption", "Activate vitamin D", "Block PTH"], "Loop diuretics inhibit paracellular calcium reabsorption in thick ascending limb; use only after volume repletion."),
        q("Thiazides can worsen hypercalcemia because they:", "Increase distal tubular calcium reabsorption", ["Block calcium-sensing receptors", "Inhibit vitamin D receptors", "Destroy osteoclasts"], "Thiazides reduce urinary calcium and can raise serum calcium."),
    ]),
]


def main():
    questions = []
    for topic_index, (slug, topic, rows) in enumerate(TOPICS):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        for question_index, row in enumerate(rows, 1):
            options = list(row["wrong"])
            answer_index = (topic_index + question_index - 1) % 4
            options.insert(answer_index, row["answer"])
            questions.append({**BASE, "id": f"endocrine-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "pharmacology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 7 or len(questions) != 70:
        raise AssertionError(f"Expected 7 topics and 70 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 70:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
