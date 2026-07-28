import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Gastrointestinal System"
CHAPTER_ORDER = 10
BASE = {
    "subjectId": "physiology",
    "subjectTitle": "Physiology",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "sourcePdf": "physiology 1.pdf",
    "sourcePdfPageStart": 460,
    "sourcePdfPageEnd": 540,
    "chapterOrder": CHAPTER_ORDER,
    "imageUrls": [],
}


def q(prompt, answer, wrong, explanation, clinical=False):
    return {
        "prompt": prompt,
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "moderate",
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("functional-anatomy-general-principles", "Functional Anatomy and General Principles of Functions of Gastrointestinal System", 1, [
        q("Which layer of the gastrointestinal wall contains Auerbach's myenteric plexus?", "Muscularis externa", ["Mucosa", "Submucosa", "Serosa only"], "The myenteric plexus lies between circular and longitudinal muscle and controls motility."),
        q("Meissner's plexus is chiefly involved in regulating which gastrointestinal function?", "Secretion and local mucosal activity", ["Skeletal muscle contraction", "Bile pigment formation", "Portal venous pressure"], "The submucosal plexus regulates secretion, blood flow and mucosal movement."),
        q("Which nervous system can coordinate many gut reflexes even without direct CNS input?", "Enteric nervous system", ["Somatic nervous system", "Optic pathway", "Vestibular system"], "The enteric nervous system contains intrinsic circuits for motility and secretion."),
        q("After abdominal surgery, a patient develops paralytic ileus with absent bowel sounds. Which function is most directly depressed?", "Gastrointestinal motility", ["Pancreatic endocrine secretion only", "Vitamin B12 absorption only", "Bile salt synthesis"], "Postoperative ileus reflects impaired gut smooth muscle and enteric reflex activity.", True),
        q("Parasympathetic stimulation generally has what effect on gastrointestinal activity?", "Increases motility and secretion", ["Stops all secretion", "Constricts all sphincters permanently", "Abolishes peristalsis"], "Parasympathetic activity facilitates digestive motility and glandular secretion."),
        q("Sympathetic stimulation usually affects the gut by causing which response?", "Decreased motility with sphincter contraction", ["Marked salivary watery secretion", "Relaxation of all sphincters", "Increased villus formation"], "Sympathetic input inhibits motility and secretion and tends to contract sphincters."),
        q("Segmentation movements in the intestine mainly serve which purpose?", "Mixing of intestinal contents", ["Rapid propulsion only", "Vomiting reflex", "Defecation only"], "Segmentation mixes chyme with secretions and exposes it to mucosa."),
        q("A patient with diabetic autonomic neuropathy develops gastroparesis. Which control system is impaired?", "Autonomic and enteric control of gut motility", ["ABO blood group control", "Pulmonary stretch reflex", "Renal counter-current exchange"], "Autonomic neuropathy can disturb enteric motor patterns and gastric emptying.", True),
        q("Gastrointestinal hormones are released mainly from which cells?", "Enteroendocrine cells", ["Chief cells only", "Kupffer cells", "Parietal neurons"], "Enteroendocrine cells secrete hormones such as gastrin, CCK and secretin."),
        q("A patient taking opioids develops constipation because opioids mainly reduce which gut function?", "Propulsive motility", ["Intrinsic factor binding", "Bile formation", "Salivary amylase activation"], "Opioids slow intestinal transit by inhibiting enteric neural activity.", True),
    ]),
    ("mouth-pharynx-oesophagus", "Physiological Activities in Mouth, Pharynx and Oesophagus", 2, [
        q("Salivary amylase begins digestion of which nutrient?", "Starch", ["Triglycerides", "Nucleic acids", "Cellulose"], "Ptyalin starts starch digestion in the mouth."),
        q("Which salivary component lubricates food and helps bolus formation?", "Mucin", ["Pepsin", "Trypsin", "Bile salt"], "Mucin makes saliva viscous and lubricates the bolus."),
        q("The first phase of swallowing is mainly under which type of control?", "Voluntary control", ["Purely spinal reflex", "Renal reflex control", "Cardiac pacemaker control"], "The oral phase is voluntary before the reflex pharyngeal phase begins."),
        q("A child with mumps has painful swelling of the parotid gland. Which secretion may be reduced?", "Saliva", ["Bile", "Gastric acid", "Pancreatic insulin"], "Parotid inflammation can reduce salivary flow and oral lubrication.", True),
        q("During swallowing, closure of the laryngeal inlet primarily prevents what?", "Aspiration into the airway", ["Gastric acid secretion", "Bile reflux", "Defecation reflex"], "Airway protection is a key part of the pharyngeal phase."),
        q("Primary peristalsis in the oesophagus is initiated by which act?", "Swallowing", ["Defecation", "Micturition", "Sneezing"], "Primary peristalsis follows a swallow and propels the bolus."),
        q("Lower oesophageal sphincter tone is important for preventing which condition?", "Gastro-oesophageal reflux", ["Achlorhydria", "Steatorrhoea", "Jaundice"], "The LES prevents reflux of gastric contents into the oesophagus."),
        q("A patient with heartburn that worsens after meals most likely has failure of which barrier?", "Lower oesophageal sphincter", ["Pyloric pump", "Ileocecal valve", "Anal sphincter"], "Reduced LES competence permits acid reflux.", True),
        q("Which cranial nerve provides major parasympathetic supply for swallowing and oesophageal motility?", "Vagus nerve", ["Optic nerve", "Hypoglossal nerve only", "Accessory nerve only"], "The vagus is central to oesophageal motor control."),
        q("A patient with achalasia has dysphagia due to failure of which event?", "Relaxation of lower oesophageal sphincter", ["Opening of ileocecal valve", "Secretion of bile salts", "Absorption of iron"], "Achalasia involves impaired LES relaxation and disordered peristalsis.", True),
    ]),
    ("stomach", "Physiological Activities in Stomach", 3, [
        q("Which gastric cells secrete hydrochloric acid?", "Parietal cells", ["Chief cells", "Goblet cells", "Kupffer cells"], "Parietal cells secrete HCl and intrinsic factor."),
        q("Pepsinogen is secreted mainly by which gastric cells?", "Chief cells", ["Parietal cells", "G cells", "D cells only"], "Chief cells release pepsinogen, which is activated to pepsin."),
        q("Gastrin is released mainly from which cells?", "G cells", ["Chief cells", "Goblet cells", "Enterocytes"], "G cells of the antrum secrete gastrin."),
        q("A patient with pernicious anaemia has impaired vitamin B12 absorption due to loss of which gastric secretion?", "Intrinsic factor", ["Pepsin", "Mucin only", "Gastric lipase"], "Intrinsic factor from parietal cells is required for ileal B12 absorption.", True),
        q("Which hormone strongly stimulates gastric acid secretion?", "Gastrin", ["Secretin", "Insulin", "Aldosterone"], "Gastrin stimulates parietal cell acid secretion directly and via histamine."),
        q("Secretin inhibits gastric acid secretion mainly when chyme entering duodenum is what?", "Acidic", ["Highly alkaline", "Protein-free", "Air-filled"], "Duodenal acid releases secretin, which reduces gastric acid output."),
        q("The pyloric pump mainly helps with which gastric function?", "Grinding and controlled emptying", ["Bile concentration", "Colon haustration", "Salivary secretion"], "Antral contractions grind food and regulate delivery to duodenum."),
        q("A patient with Zollinger-Ellison syndrome develops recurrent ulcers because of excess secretion of which hormone?", "Gastrin", ["CCK", "Secretin", "Motilin"], "Gastrinoma causes very high acid output and peptic ulceration.", True),
        q("The gastric mucosal barrier is protected importantly by mucus and which ion?", "Bicarbonate", ["Potassium only", "Iron", "Calcium oxalate"], "Mucus-bicarbonate protects epithelium from acid and pepsin."),
        q("NSAID use predisposes to gastric ulcer mainly by reducing which protective factor?", "Prostaglandin-mediated mucus and bicarbonate secretion", ["Gastrin release", "Pepsinogen activation", "Oesophageal peristalsis"], "Prostaglandins support mucosal blood flow, mucus and bicarbonate.", True),
    ]),
    ("pancreas-liver-gall-bladder", "Pancreas, Liver and Gall Bladder", 4, [
        q("Pancreatic acinar cells primarily secrete which type of substance?", "Digestive enzymes", ["Bile salts", "Intrinsic factor", "Hydrochloric acid"], "Acinar cells release enzymes for digestion of proteins, fats and carbohydrates."),
        q("Pancreatic duct cells secrete fluid rich in which ion?", "Bicarbonate", ["Hydrogen ion", "Ferric ion", "Ammonium only"], "Duct cells secrete bicarbonate-rich alkaline fluid."),
        q("Secretin mainly stimulates which pancreatic secretion?", "Bicarbonate-rich fluid", ["Pepsinogen", "Intrinsic factor", "Bile pigment only"], "Secretin promotes ductal bicarbonate secretion."),
        q("A patient with chronic pancreatitis passes bulky foul-smelling stools. Which defect explains this best?", "Pancreatic enzyme deficiency causing fat maldigestion", ["Excess salivary amylase", "Increased gastric acid only", "Loss of colonic haustra"], "Pancreatic lipase deficiency causes steatorrhoea.", True),
        q("CCK is released from the small intestine mainly in response to which nutrients?", "Fat and amino acids", ["Water only", "Bile pigments", "Cellulose only"], "Fatty acids and amino acids stimulate CCK release."),
        q("Bile salts are most important for which digestive process?", "Emulsification and micelle formation for fat absorption", ["Protein denaturation", "Starch hydrolysis", "Vitamin B12 binding"], "Bile salts aid fat digestion and absorption."),
        q("The gall bladder primarily performs which function?", "Stores and concentrates bile", ["Produces insulin", "Secretes pepsin", "Absorbs vitamin B12"], "The gall bladder concentrates hepatic bile between meals."),
        q("A gallstone obstructing the common bile duct most directly impairs absorption of which vitamins?", "Fat-soluble vitamins", ["Vitamin C only", "Vitamin B12 only", "Folate only"], "Loss of bile delivery impairs absorption of vitamins A, D, E and K.", True),
        q("Enterohepatic circulation mainly recycles which substances?", "Bile salts", ["Pepsin", "Intrinsic factor", "Gastric acid"], "Most bile salts are reabsorbed in ileum and returned to liver."),
        q("After ileal resection, a patient develops bile salt wasting and steatorrhoea. Which process is lost?", "Enterohepatic recycling of bile salts", ["Gastric receptive relaxation", "Salivary starch digestion", "Colonic defecation reflex"], "The terminal ileum is the main site for bile salt reabsorption.", True),
    ]),
    ("small-intestine", "Physiological Activities in Small Intestine", 5, [
        q("The small intestine is the major site for which gastrointestinal function?", "Digestion and absorption", ["Faecal storage only", "Bile synthesis", "Hydrochloric acid secretion"], "Most nutrient digestion and absorption occur in the small intestine."),
        q("Brush border enzymes are located on which cells?", "Enterocytes", ["Parietal cells", "Kupffer cells", "Chief cells"], "Enterocyte microvilli contain brush border enzymes."),
        q("Segmentation contractions in the small intestine mainly promote what?", "Mixing of chyme", ["Vomiting", "Micturition", "Rapid defecation"], "Segmentation mixes chyme with digestive juices."),
        q("A patient with lactase deficiency develops bloating and diarrhoea after milk. Which carbohydrate is malabsorbed?", "Lactose", ["Starch only", "Glycogen", "Cellulose"], "Lactase deficiency prevents normal lactose digestion.", True),
        q("The migrating motor complex is most active during which state?", "Fasting", ["Immediately after every meal", "During defecation only", "During sleep only"], "MMC clears residual contents during fasting."),
        q("Secretin released from duodenum is stimulated most strongly by what?", "Acid in duodenal chyme", ["Alkaline saliva", "Colonic bacteria", "Oesophageal distension"], "Duodenal acid triggers secretin release."),
        q("CCK slows gastric emptying while stimulating which action?", "Pancreatic enzyme secretion", ["Intrinsic factor secretion only", "Renin release", "Platelet aggregation"], "CCK coordinates fat/protein digestion by stimulating pancreatic enzymes."),
        q("A patient with coeliac disease has villous atrophy. Which function is most directly reduced?", "Intestinal absorptive surface area", ["Gastric acid formation", "Bile synthesis", "Oesophageal sphincter tone"], "Villi greatly increase absorptive area.", True),
        q("Iron absorption occurs mainly in which part of the gut?", "Duodenum", ["Sigmoid colon", "Stomach fundus", "Oesophagus"], "Iron is absorbed mainly in the duodenum and proximal jejunum."),
        q("Loss of terminal ileum most directly impairs absorption of vitamin B12 and which other substance?", "Bile salts", ["Hydrochloric acid", "Pepsinogen", "Salivary mucin"], "The terminal ileum absorbs B12-intrinsic factor complex and bile salts.", True),
    ]),
    ("large-intestine", "Physiological Activities in Large Intestine", 6, [
        q("The large intestine is especially important for absorption of what?", "Water and electrolytes", ["Most amino acids", "Vitamin B12-intrinsic factor", "Gastric acid"], "Colon absorbs water and electrolytes and forms faeces."),
        q("Haustral contractions of colon mainly serve which function?", "Mixing and slow propulsion", ["Gastric emptying", "Swallowing", "Bile concentration"], "Haustrations mix colonic contents and aid absorption."),
        q("Mass movements in colon are important for which process?", "Propulsion of faeces toward rectum", ["Salivary secretion", "Pancreatic enzyme activation", "Oesophageal reflux"], "Mass movements move faecal material over long colonic segments."),
        q("A patient with cholera has profuse watery diarrhoea because intestinal secretion of which ion increases?", "Chloride", ["Iron", "Calcium", "Bile pigment"], "Cholera toxin increases cAMP-mediated chloride and water secretion.", True),
        q("Normal colonic bacteria contribute to synthesis of which vitamin?", "Vitamin K", ["Vitamin D from sunlight", "Vitamin B12-intrinsic factor", "Vitamin A from bile"], "Gut flora contribute to vitamin K production."),
        q("The internal anal sphincter is composed mainly of which muscle type?", "Smooth muscle", ["Skeletal muscle", "Cardiac muscle", "Ciliated epithelium"], "The internal anal sphincter is involuntary smooth muscle."),
        q("The external anal sphincter is important because it provides what?", "Voluntary control of defecation", ["Gastric acid secretion", "Bile salt recycling", "Pancreatic bicarbonate"], "The external anal sphincter is skeletal muscle under voluntary control."),
        q("After spinal cord injury, loss of voluntary defecation control most directly involves which sphincter?", "External anal sphincter", ["Pyloric sphincter", "Lower oesophageal sphincter", "Ileocecal valve"], "Voluntary continence depends on somatic control of the external sphincter.", True),
        q("Short-chain fatty acids in colon are produced mainly by what?", "Bacterial fermentation", ["Gastric acid secretion", "Pancreatic proteases", "Salivary amylase"], "Colonic bacteria ferment undigested carbohydrate to short-chain fatty acids."),
        q("A patient with Hirschsprung disease has severe constipation due to absence of which neural elements?", "Enteric ganglion cells", ["Parietal cells", "Chief cells", "Kupffer cells"], "Aganglionosis prevents normal relaxation and peristalsis in affected bowel.", True),
    ]),
    ("digestion-absorption", "Digestion and Absorption", 7, [
        q("Final carbohydrate digestion at the intestinal surface is performed mainly by which enzymes?", "Brush border disaccharidases", ["Pepsin", "Bile salts", "Gastric lipase only"], "Disaccharidases split sugars at the brush border."),
        q("Glucose absorption across intestinal epithelium depends mainly on which transporter?", "Sodium-glucose cotransport", ["Chloride-bicarbonate exchanger only", "Aquaporin only", "Intrinsic factor receptor"], "SGLT transports glucose with sodium at the apical membrane."),
        q("Protein digestion produces absorbable amino acids and which smaller products?", "Dipeptides and tripeptides", ["Bile acids", "Chylomicrons only", "Free fatty acid soaps only"], "Small peptides and amino acids are absorbed by enterocytes."),
        q("A patient with pancreatic lipase deficiency will have the greatest problem absorbing which nutrient?", "Fat", ["Glucose", "Sodium", "Water"], "Pancreatic lipase is essential for triglyceride digestion.", True),
        q("Long-chain fatty acids are absorbed from enterocytes mainly through which route?", "Lymphatics as chylomicrons", ["Portal blood as free glucose", "Direct renal tubules", "Pulmonary veins"], "Long-chain fats are packaged into chylomicrons and enter lacteals."),
        q("Vitamin B12 absorption requires intrinsic factor and occurs mainly in which site?", "Terminal ileum", ["Stomach fundus", "Oesophagus", "Rectum"], "B12-intrinsic factor complex is absorbed in the terminal ileum."),
        q("Calcium absorption is promoted by which vitamin?", "Vitamin D", ["Vitamin K", "Vitamin C", "Vitamin B1"], "Vitamin D increases intestinal calcium absorption."),
        q("A patient after gastrectomy develops macrocytic anaemia years later. Which deficiency is most likely?", "Vitamin B12 deficiency", ["Vitamin C excess", "Sodium deficiency", "Bile salt excess"], "Loss of intrinsic factor reduces B12 absorption and can cause megaloblastic anaemia.", True),
        q("Bile salts help fat absorption mainly by forming what?", "Micelles", ["Haemoglobin", "Pepsinogen", "Mucus plugs"], "Micelles carry lipid digestion products to the enterocyte surface."),
        q("A patient with obstructive jaundice develops pale stools and steatorrhoea because delivery of which substance to intestine is reduced?", "Bile", ["Saliva", "Gastric mucus", "Intrinsic factor"], "Reduced bile entry impairs fat emulsification and absorption.", True),
    ]),
]


def build():
    out = []
    for slug, topic, order, rows in TOPICS:
        for index, row in enumerate(rows, 1):
            shift = (order + index) % 4
            options = row["options"][shift:] + row["options"][:shift]
            answer = row["answer"]
            out.append({
                **BASE,
                **row,
                "id": f"physiology-gastrointestinal-{slug}-{index:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": order,
                "options": options,
                "answerIndex": options.index(answer),
                "answer": answer,
            })
    return out


def validate(questions):
    if len(questions) != 70:
        raise ValueError(f"Expected 70 questions, got {len(questions)}")
    if len({question["id"] for question in questions}) != 70:
        raise ValueError("Duplicate question IDs")
    for _, topic, _, _ in TOPICS:
        topic_questions = [question for question in questions if question["topic"] == topic]
        clinical_count = sum("clinical" in question.get("tags", []) for question in topic_questions)
        if len(topic_questions) != 10 or clinical_count < 3:
            raise ValueError(f"{topic}: {len(topic_questions)} questions, {clinical_count} clinical")
    for question in questions:
        if question["answer"] != question["options"][question["answerIndex"]]:
            raise ValueError(question["id"])


def update(path, questions):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    ids = {question["id"] for question in questions}
    data["questions"] = [question for question in data.get("questions", []) if question.get("id") not in ids] + questions
    data["questions"].sort(key=lambda question: question.get("id", ""))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    questions = build()
    validate(questions)
    for path in DATA_PATHS:
        update(path, questions)
        print(f"Added {len(questions)} physiology questions to {path}.")
    for _, topic, _, _ in TOPICS:
        print(f"- {topic}: 10 questions")


if __name__ == "__main__":
    main()
