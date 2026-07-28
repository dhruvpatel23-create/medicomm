import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Gastrointestinal Pharmacology"
BASE = {"subjectId": "pharmacology", "subjectTitle": "Pharmacology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("gastric-acidity-ulcers-gerd", "Pharmacotherapy for Gastric Acidity, Peptic Ulcers, and Gastroesophageal Reflux Disease", [
        q("A patient with severe erosive esophagitis is started on omeprazole. The drug suppresses acid because it:", "Irreversibly inhibits the gastric parietal cell H/K-ATPase", ["Blocks H2 receptors competitively", "Neutralizes acid already in the lumen only", "Stimulates prostaglandin breakdown"], "PPIs are prodrugs that covalently inhibit the final common proton pump for gastric acid secretion."),
        q("A patient says omeprazole works poorly when taken at bedtime after dinner. The best instruction is:", "Take it before a meal so active pumps are inhibited", ["Take it only with antacid at bedtime", "Crush it with orange juice after meals", "Use it only when pain begins"], "PPIs work best before meals because food activates proton pumps that the drug can then inhibit."),
        q("A patient with peptic ulcer disease and chronic NSAID need is given misoprostol. It helps by:", "Replacing prostaglandin-mediated mucus and bicarbonate protection", ["Eradicating H. pylori directly", "Blocking histamine H1 receptors", "Inhibiting proton pumps irreversibly"], "Misoprostol is a PGE1 analog that protects gastric mucosa but can cause diarrhea and uterine contractions."),
        q("A pregnant patient with dyspepsia should avoid misoprostol because it can:", "Stimulate uterine contractions", ["Cause fetal thyroid ablation", "Block folate receptors", "Induce neonatal opioid withdrawal"], "Misoprostol is uterotonic and is contraindicated for routine ulcer prophylaxis in pregnancy."),
        q("A patient on clopidogrel needs acid suppression. Which concern is most relevant with omeprazole?", "CYP2C19 inhibition may reduce clopidogrel activation", ["Omeprazole directly activates platelets", "Clopidogrel neutralizes gastric acid", "Both drugs cause acetaldehyde accumulation"], "Clopidogrel is a prodrug activated partly by CYP2C19; some PPIs can interfere."),
        q("Famotidine reduces nocturnal acid symptoms by blocking:", "H2 receptors on parietal cells", ["M3 receptors on chief cells", "Proton pumps covalently", "Gastrin receptors on enterocytes"], "H2 blockers reduce histamine-driven parietal cell acid secretion, especially basal/nocturnal secretion."),
        q("A patient with H. pylori ulcer receives bismuth quadruple therapy. Bismuth contributes by:", "Coating ulcers and exerting local antimicrobial effects", ["Irreversibly inhibiting H/K-ATPase", "Blocking dopamine receptors", "Stimulating gastric acid"], "Bismuth has mucosal protective and anti-H. pylori activity and can darken stool/tongue."),
        q("Long-term high-dose PPI therapy is associated with which plausible adverse effect?", "Hypomagnesemia and increased enteric infection risk", ["Severe hyperthyroidism", "Irreversible beta-cell failure", "Acute opioid withdrawal"], "Profound acid suppression can alter mineral handling and gastric defense against pathogens."),
        q("An antacid containing aluminum hydroxide causes constipation. Which paired adverse effect is typical of magnesium hydroxide?", "Diarrhea", ["Agranulocytosis", "Pulmonary fibrosis", "Severe hypoglycemia"], "Aluminum salts tend to constipate; magnesium salts commonly cause diarrhea."),
        q("Sucralfate is most effective in acidic environments because it:", "Polymerizes into a protective barrier over ulcer bases", ["Blocks acid secretion systemically", "Kills H. pylori by DNA disruption", "Inhibits vagal acetylcholine release"], "Sucralfate forms a viscous protective coating and requires gastric acidity for activation."),
    ]),
    ("gi-motility-water-flux-emesis-biliary-pancreatic", "Gastrointestinal Motility and Water Flux, Emesis, and Biliary and Pancreatic Disease", [
        q("A patient with diabetic gastroparesis improves with metoclopramide but develops acute dystonia. The adverse effect is due to:", "Central dopamine D2 receptor blockade", ["Peripheral opioid receptor activation", "H2 receptor blockade", "Proton pump inhibition"], "Metoclopramide is a D2 antagonist and 5-HT4 agonist; central D2 blockade can cause extrapyramidal effects."),
        q("Ondansetron prevents chemotherapy-induced vomiting mainly by blocking:", "5-HT3 receptors on vagal afferents and in the chemoreceptor trigger zone", ["D2 receptors in basal ganglia only", "NK1 receptors only", "Muscarinic receptors in vestibular nuclei"], "5-HT3 antagonists are key antiemetics for chemotherapy and postoperative nausea."),
        q("A patient on ondansetron with other QT-prolonging drugs needs caution because ondansetron can:", "Prolong the QT interval", ["Cause irreversible hearing loss", "Trigger hypertensive crisis with tyramine", "Block vitamin K"], "5-HT3 antagonists can prolong QT, especially with risk factors or interacting drugs."),
        q("A patient with opioid-induced constipation and ongoing analgesia receives methylnaltrexone. The rationale is:", "Peripheral mu-opioid receptor blockade with limited CNS entry", ["Central mu agonism", "Proton pump inhibition", "D2 receptor activation"], "Peripherally acting mu antagonists reverse gut opioid effects while sparing central analgesia."),
        q("Loperamide helps noninvasive diarrhea because it:", "Activates peripheral mu receptors to slow intestinal transit", ["Blocks H. pylori urease", "Inhibits pancreatic lipase", "Stimulates chloride secretion"], "Loperamide has poor CNS penetration and reduces motility; avoid when invasive infection/toxic megacolon is a concern."),
        q("A traveler with watery diarrhea takes bismuth subsalicylate. Which patient should avoid it?", "A child with viral illness because of salicylate-related Reye risk", ["An adult with mild dyspepsia", "A patient with constipation only", "A patient needing stool darkening"], "Bismuth subsalicylate contains salicylate and is avoided in children with viral illness."),
        q("Lubiprostone treats chronic constipation by:", "Activating intestinal chloride channels to increase fluid secretion", ["Blocking chloride secretion", "Inhibiting serotonin receptors", "Activating opioid receptors"], "Chloride and water secretion soften stool and improve transit."),
        q("Linaclotide improves constipation-predominant IBS because it:", "Activates guanylate cyclase-C, increasing chloride and bicarbonate secretion", ["Blocks D2 receptors", "Inhibits H/K-ATPase", "Activates pancreatic enzymes"], "GC-C activation increases cGMP and intestinal fluid secretion; diarrhea is common."),
        q("Ursodeoxycholic acid can help selected cholesterol gallstones because it:", "Reduces biliary cholesterol saturation", ["Blocks gallbladder contraction completely", "Inhibits gastric acid secretion", "Directly lyses pigment stones instantly"], "Ursodiol makes bile less lithogenic and is useful only in selected patients."),
        q("Pancrelipase improves steatorrhea in chronic pancreatitis. It should be taken:", "With meals to replace digestive enzymes during nutrient exposure", ["Only at bedtime without food", "Only with antacids after all meals", "Once monthly"], "Pancreatic enzyme replacement must mix with food to improve fat and protein digestion."),
    ]),
    ("inflammatory-bowel-disease", "Pharmacotherapy of Inflammatory Bowel Disease", [
        q("Mesalamine is useful in mild ulcerative colitis because it delivers anti-inflammatory 5-ASA to:", "Intestinal mucosa", ["Adrenal cortex", "Gastric parietal cells", "Pancreatic beta cells"], "5-ASA preparations act locally in the intestinal lumen/mucosa to reduce inflammation."),
        q("Sulfasalazine causes more systemic adverse effects than mesalamine partly because gut bacteria split it into 5-ASA plus:", "Sulfapyridine", ["Methotrexate", "Infliximab", "Budesonide"], "The sulfa carrier contributes to adverse effects such as headache, nausea, rash, and reversible infertility."),
        q("Budesonide is used for some ileocecal Crohn disease because it:", "Has high first-pass metabolism and relatively lower systemic steroid exposure", ["Cannot act locally in gut", "Blocks TNF directly", "Depletes B cells"], "Budesonide provides topical glucocorticoid effect with less systemic exposure than prednisone."),
        q("A patient with severe UC flare receives systemic corticosteroids. Why are they not ideal maintenance therapy?", "Long-term toxicity is high despite short-term anti-inflammatory benefit", ["They never suppress inflammation", "They permanently cure UC", "They increase 5-ASA delivery"], "Steroids induce remission but chronic use causes major metabolic, bone, infection, and adrenal toxicities."),
        q("Azathioprine maintenance therapy requires awareness that benefit is delayed because it:", "Gradually suppresses lymphocyte proliferation through thiopurine metabolites", ["Neutralizes TNF within minutes", "Blocks acid secretion immediately", "Works only as an antacid"], "Thiopurines are steroid-sparing immunomodulators with slow onset and myelosuppression risk."),
        q("Before starting infliximab for Crohn disease, screening is needed for:", "Latent tuberculosis and hepatitis B", ["Hypothyroidism only", "Iron overload only", "Acute pancreatitis only"], "TNF blockade can reactivate latent TB and HBV; screening reduces preventable harm."),
        q("A patient on infliximab loses response after months. One mechanism is:", "Anti-drug antibody formation increasing clearance or neutralization", ["Permanent cure of inflammation", "Conversion to mesalamine", "Activation of H2 receptors"], "Biologic immunogenicity can reduce drug levels and clinical response."),
        q("Vedolizumab may have less systemic immunosuppression than some biologics because it blocks:", "Alpha4beta7 integrin gut-homing lymphocyte trafficking", ["All leukocyte DNA synthesis", "CD20 on every B cell", "Calcineurin in all T cells"], "Vedolizumab is gut-selective by targeting lymphocyte trafficking to intestinal mucosa."),
        q("Ustekinumab helps Crohn disease by targeting:", "The p40 subunit shared by IL-12 and IL-23", ["TNF receptor only", "H2 receptors", "Proton pumps"], "Blocking IL-12/23 signaling reduces Th1/Th17 inflammatory pathways."),
        q("Tofacitinib for ulcerative colitis increases zoster risk because it:", "Inhibits JAK-dependent cytokine signaling", ["Blocks gastric acid", "Activates leukotriene receptors", "Stimulates platelet COX"], "JAK inhibition affects antiviral immune signaling and can increase herpes zoster risk."),
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
            questions.append({**BASE, "id": f"gi-pharm-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "pharmacology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 3 or len(questions) != 30:
        raise AssertionError(f"Expected 3 topics and 30 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 30:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
