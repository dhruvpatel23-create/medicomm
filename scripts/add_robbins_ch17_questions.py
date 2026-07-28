import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Gastrointestinal Tract"
BASE = {"subjectId": "pathology", "subjectTitle": "Pathology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(difficulty, prompt, answer, distractors, explanation):
    if difficulty not in {"easy", "moderate", "high"}:
        raise ValueError(difficulty)
    options = [answer, *distractors]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {"difficulty": difficulty, "prompt": prompt, "options": options, "answerIndex": 0, "answer": answer, "explanation": explanation}


def jumble(question, desired_index):
    answer = question["answer"]
    distractors = [option for option in question["options"] if option != answer]
    options = distractors[:]
    options.insert(desired_index, answer)
    question["options"] = options
    question["answerIndex"] = desired_index
    return question


TOPICS = [
    ("esophagus", "Esophagus: Reflux, Barrett Esophagus, and Tumors", [
        q("easy", "Barrett esophagus is:", "Intestinal metaplasia of distal esophageal squamous mucosa", ["Squamous carcinoma of stomach", "Congenital pyloric narrowing", "Colonic diverticulosis"], "Barrett esophagus is replacement of squamous epithelium by intestinal-type columnar mucosa."),
        q("easy", "The major risk factor for Barrett esophagus is:", "Chronic gastroesophageal reflux", ["Acute appendicitis", "Celiac disease", "Portal hypertension only"], "Long-standing reflux injures distal esophageal mucosa and promotes metaplasia."),
        q("easy", "Esophageal varices are caused by:", "Portal hypertension", ["Achalasia only", "Celiac disease", "Meckel diverticulum"], "Portal hypertension dilates submucosal collateral veins in the distal esophagus."),
        q("moderate", "Barrett esophagus increases risk of:", "Esophageal adenocarcinoma", ["Esophageal leiomyoma only", "Gastric lymphoma only", "Appendiceal carcinoid"], "Intestinal metaplasia can progress through dysplasia to adenocarcinoma."),
        q("moderate", "Achalasia is caused by:", "Loss of inhibitory myenteric neurons", ["Excess acid production", "Portal vein thrombosis", "CFTR mutation"], "Failure of LES relaxation follows loss of inhibitory ganglion cells."),
        q("moderate", "Squamous cell carcinoma of esophagus is associated with:", "Alcohol and tobacco use", ["Helicobacter pylori only", "Low-fiber diet only", "Lynch syndrome only"], "Tobacco and alcohol are classic risks for esophageal SCC."),
        q("moderate", "Mallory-Weiss tears are:", "Longitudinal mucosal lacerations at the gastroesophageal junction", ["Transmural rupture of esophagus", "Submucosal venous collaterals", "Congenital duplications"], "Forceful vomiting can tear mucosa near the GE junction."),
        q("high", "A patient with long-standing reflux has salmon-colored distal esophageal mucosa. Biopsy shows goblet cells replacing normal squamous epithelium, without invasion. Which diagnosis is most likely?", "Barrett esophagus", ["Reflux esophagitis only", "Esophageal varices", "Achalasia"], "Goblet cells in distal esophagus define intestinal metaplasia of Barrett esophagus."),
        q("high", "A patient with cirrhosis vomits large amounts of blood. Endoscopy shows tortuous dilated submucosal veins in the distal esophagus. Which hemodynamic abnormality caused the bleeding?", "Portal hypertension", ["Pyloric stenosis", "Superior mesenteric artery occlusion", "Celiac sprue"], "Portal hypertension drives portosystemic collaterals and varices."),
        q("high", "A man has progressive dysphagia to solids and liquids. Barium swallow shows a bird-beak narrowing at the lower esophageal sphincter with proximal dilation. Which mechanism is responsible?", "Failure of LES relaxation from myenteric plexus degeneration", ["Goblet cell metaplasia", "Mucosal tear after vomiting", "Portal-systemic shunting"], "Achalasia causes impaired peristalsis and incomplete LES relaxation."),
    ]),
    ("stomach-gastritis", "Stomach: Gastritis, Gastropathy, and Peptic Ulcer Disease", [
        q("easy", "The most common cause of chronic gastritis is:", "Helicobacter pylori infection", ["CMV in all patients", "Celiac disease", "Crohn disease"], "H. pylori is the leading cause of chronic gastritis worldwide."),
        q("easy", "Peptic ulcers most commonly occur in the:", "Duodenum and stomach", ["Appendix only", "Colon only", "Ileum only"], "Peptic ulcers arise where acid-peptic injury overwhelms mucosal defenses."),
        q("easy", "Autoimmune gastritis primarily affects the:", "Body and fundus", ["Appendix", "Rectum", "Esophagus only"], "Autoimmune injury targets parietal cells in oxyntic mucosa."),
        q("moderate", "Autoimmune gastritis can cause:", "Pernicious anemia", ["Hemophilia", "Sickle cell disease", "ITP"], "Parietal cell loss reduces intrinsic factor and causes vitamin B12 deficiency."),
        q("moderate", "H. pylori promotes duodenal ulceration partly by:", "Increasing acid load to duodenal mucosa", ["Destroying factor VIII", "Blocking bile ducts", "Causing volvulus"], "Antral gastritis can increase gastrin and acid secretion."),
        q("moderate", "NSAID gastropathy occurs because NSAIDs:", "Reduce prostaglandin-mediated mucosal protection", ["Increase intrinsic factor", "Stimulate goblet cells", "Cause granulomas"], "Prostaglandins support mucus, bicarbonate, and mucosal blood flow."),
        q("moderate", "Curling ulcers are associated with:", "Severe burns", ["Head trauma", "Portal hypertension", "Celiac disease"], "Burn stress can cause acute gastric/duodenal ulcers."),
        q("high", "A patient has epigastric pain and an antral biopsy showing curved organisms along the mucus layer with chronic active inflammation. Which organism is most likely involved?", "Helicobacter pylori", ["Campylobacter jejuni", "Vibrio cholerae", "Entamoeba histolytica"], "H. pylori colonizes gastric mucus and causes chronic active gastritis."),
        q("high", "A patient with autoimmune gastritis has body-fundus mucosal atrophy, achlorhydria, hypergastrinemia, and antibodies to parietal cells with loss of intrinsic factor. Which hematologic complication may develop?", "Vitamin B12 deficiency megaloblastic anemia", ["Iron overload", "G6PD hemolysis", "Thalassemia major"], "Intrinsic factor loss causes pernicious anemia."),
        q("high", "A patient using high-dose NSAIDs develops acute gastric erosions and bleeding. The injury occurs because protective mucus and bicarbonate secretion are reduced. Which mediator was suppressed?", "Prostaglandins", ["Gastrin only", "Secretin", "Intrinsic factor"], "NSAIDs inhibit cyclooxygenase and reduce protective prostaglandins."),
    ]),
    ("stomach-tumors", "Gastric Polyps and Gastric Tumors", [
        q("easy", "The most common gastric malignancy is:", "Adenocarcinoma", ["GIST", "MALT lymphoma", "Carcinoid tumor"], "Most malignant gastric tumors are adenocarcinomas."),
        q("easy", "Diffuse gastric carcinoma often contains:", "Signet-ring cells", ["Reed-Sternberg cells", "Auer rods", "Asbestos bodies"], "Diffuse-type carcinoma is poorly cohesive and often has signet-ring cells."),
        q("easy", "GIST is commonly driven by mutation in:", "KIT", ["APC", "CFTR", "PIGA"], "Gastrointestinal stromal tumors frequently have KIT or PDGFRA mutations."),
        q("moderate", "Intestinal-type gastric adenocarcinoma is associated with:", "Chronic atrophic gastritis and intestinal metaplasia", ["Achalasia only", "Ulcerative colitis only", "Appendicitis"], "The intestinal type follows a metaplasia-dysplasia-carcinoma sequence."),
        q("moderate", "Diffuse gastric carcinoma is linked to mutations in:", "CDH1 encoding E-cadherin", ["BCR-ABL", "PML-RARA", "HBB"], "Loss of E-cadherin causes poorly cohesive infiltrative growth."),
        q("moderate", "Linitis plastica means:", "Diffuse rigid thickening of stomach wall", ["Pyloric smooth muscle hypertrophy", "Duodenal diverticulum", "Appendiceal mucin"], "Diffuse carcinoma can create a leather-bottle stomach."),
        q("moderate", "Gastric MALT lymphoma may regress after:", "H. pylori eradication", ["Appendectomy", "Gluten withdrawal only", "Splenectomy"], "Early gastric MALT lymphoma can depend on H. pylori-driven inflammation."),
        q("high", "A patient has weight loss and early satiety. Endoscopy shows a diffusely thickened rigid stomach, and biopsy shows infiltrating signet-ring cells lacking cohesion. Which tumor is most likely?", "Diffuse gastric adenocarcinoma", ["Intestinal-type gastric adenocarcinoma", "GIST", "Hyperplastic polyp"], "Diffuse gastric cancer infiltrates the wall and can cause linitis plastica."),
        q("high", "A gastric mass is composed of spindle cells arising from the muscularis propria. Immunostaining is positive for KIT, and targeted therapy with imatinib is considered. Which tumor is this?", "Gastrointestinal stromal tumor", ["Leiomyoma", "MALT lymphoma", "Carcinoid tumor"], "GISTs are KIT-positive mesenchymal tumors."),
        q("high", "A patient with chronic H. pylori gastritis develops a low-grade gastric B-cell lymphoma. After antibiotic treatment, the tumor regresses. Which lymphoma category explains this behavior?", "Extranodal marginal zone lymphoma of MALT", ["Diffuse large B-cell lymphoma", "Burkitt lymphoma", "Mantle cell lymphoma"], "Antigen-dependent gastric MALT lymphoma may regress after H. pylori eradication."),
    ]),
    ("congenital-obstruction", "Congenital and Mechanical Intestinal Obstruction", [
        q("easy", "Hirschsprung disease is caused by absence of:", "Enteric ganglion cells", ["Paneth cells", "Goblet cells", "Hepatocytes"], "Aganglionosis prevents relaxation and causes functional obstruction."),
        q("easy", "Meckel diverticulum is a remnant of the:", "Vitelline duct", ["Urachus", "Neural tube", "Thyroglossal duct"], "Meckel diverticulum arises from incomplete involution of the omphalomesenteric duct."),
        q("easy", "Intussusception means:", "Telescoping of one bowel segment into another", ["Twisting around mesentery", "Outpouching of mucosa only", "Ganglion cell absence"], "Intussusception drags mesentery and may obstruct blood supply."),
        q("moderate", "Hirschsprung disease most commonly affects the:", "Rectosigmoid colon", ["Duodenum only", "Stomach body", "Appendix tip"], "Aganglionosis begins distally and extends proximally."),
        q("moderate", "A Meckel diverticulum may bleed because it contains:", "Ectopic gastric mucosa", ["Pancreatic cancer", "Cirrhotic varices", "Celiac villi"], "Acid secretion from gastric mucosa can ulcerate adjacent ileal mucosa."),
        q("moderate", "Volvulus is:", "Twisting of bowel around its mesenteric attachment", ["Mucosal metaplasia", "Autoimmune gastritis", "Portal venous dilation"], "Twisting can obstruct lumen and blood supply."),
        q("moderate", "Adhesions are a common cause of:", "Small bowel obstruction", ["Barrett esophagus", "Gastric MALT lymphoma", "Celiac disease"], "Postoperative fibrous bands can trap bowel."),
        q("high", "A neonate fails to pass meconium and has abdominal distention. Rectal biopsy lacks ganglion cells in submucosal and myenteric plexuses, and proximal colon is dilated. Which disease is present?", "Hirschsprung disease", ["Meckel diverticulum", "Pyloric stenosis", "Intussusception"], "Aganglionic distal bowel causes functional obstruction and megacolon."),
        q("high", "A toddler has episodic abdominal pain, vomiting, and currant jelly stools. Imaging shows telescoping of ileum into colon with a lead point. Which mechanical process is this?", "Intussusception", ["Volvulus", "Adhesive obstruction", "Hirschsprung disease"], "Intussusception causes intermittent obstruction and mucosal ischemia."),
        q("high", "A child has painless lower GI bleeding. A scan detects ectopic gastric mucosa in an ileal outpouching located on the antimesenteric border. Which congenital anomaly is most likely?", "Meckel diverticulum", ["Omphalocele", "Hirschsprung disease", "Anal atresia"], "Meckel diverticulum can contain acid-secreting gastric mucosa and bleed."),
    ]),
    ("malabsorption", "Malabsorption, Celiac Disease, and Tropical Sprue", [
        q("easy", "Celiac disease is triggered by:", "Gluten", ["Lactose only", "H. pylori", "Shiga toxin"], "Gluten peptides trigger immune injury in genetically susceptible patients."),
        q("easy", "Celiac disease primarily affects the:", "Small intestine", ["Appendix", "Esophagus", "Rectal veins"], "Proximal small intestine is commonly involved."),
        q("easy", "Lactase deficiency causes intolerance to:", "Milk sugar", ["Gluten", "Bile salts", "Fructose only"], "Lactase deficiency impairs lactose digestion."),
        q("moderate", "Celiac disease is associated with:", "HLA-DQ2 or HLA-DQ8", ["HLA-B27 only", "BCR-ABL", "PIGA mutation"], "Most patients carry HLA-DQ2 or DQ8."),
        q("moderate", "Small bowel biopsy in celiac disease shows:", "Villous atrophy, crypt hyperplasia, and increased intraepithelial lymphocytes", ["Caseating granulomas only", "Signet-ring cells", "Pseudomembranes"], "The classic triad reflects immune-mediated mucosal injury."),
        q("moderate", "Dermatitis herpetiformis is associated with:", "Celiac disease", ["Crohn disease only", "Ulcerative colitis only", "Hirschsprung disease"], "IgA deposits in dermal papillae are linked to gluten sensitivity."),
        q("moderate", "Tropical sprue is treated with:", "Antibiotics and folate", ["Colectomy only", "H. pylori eradication only", "Anti-TNF only"], "Tropical sprue causes malabsorption and often responds to antibiotics and folate."),
        q("high", "A patient has chronic diarrhea, weight loss, iron deficiency anemia, and a pruritic blistering rash. Duodenal biopsy shows villous atrophy with increased intraepithelial lymphocytes, and anti-tTG IgA is positive. Which diagnosis fits?", "Celiac disease", ["Tropical sprue", "Whipple disease", "Lactase deficiency"], "Celiac disease causes immune-mediated villous injury and dermatitis herpetiformis."),
        q("high", "A traveler living in a tropical region develops chronic diarrhea, weight loss, macrocytic anemia, and small intestinal villous blunting. Symptoms improve with antibiotics and folate. Which disorder is likely?", "Tropical sprue", ["Celiac disease", "Crohn disease", "Ulcerative colitis"], "Tropical sprue is an acquired malabsorption syndrome in tropical regions."),
        q("high", "A child develops bloating and watery diarrhea after dairy intake, but intestinal biopsy is otherwise normal and symptoms improve with lactose avoidance. Which enzyme deficiency explains this?", "Lactase deficiency", ["Pancreatic lipase deficiency", "Sucrase excess", "Brush border peptidase excess"], "Lactase deficiency causes osmotic diarrhea after lactose ingestion."),
    ]),
    ("enterocolitis", "Infectious Enterocolitis and Pseudomembranous Colitis", [
        q("easy", "Cholera causes diarrhea by increasing:", "Chloride and water secretion", ["Colonic fibrosis", "Goblet cell metaplasia", "Portal pressure"], "Cholera toxin increases cAMP-mediated chloride secretion."),
        q("easy", "Pseudomembranous colitis is most commonly caused by:", "Clostridioides difficile", ["Vibrio cholerae", "H. pylori", "EBV"], "C. difficile overgrowth after antibiotics produces toxins."),
        q("easy", "Shigella commonly causes:", "Dysentery with bloody diarrhea", ["Achalasia", "Barrett esophagus", "Gastric MALT lymphoma"], "Shigella invades colonic mucosa and causes inflammatory diarrhea."),
        q("moderate", "C. difficile toxins injure colon by:", "Inactivating Rho GTPases and damaging cytoskeleton", ["Activating KIT", "Deleting APC", "Blocking gluten digestion"], "Toxins A and B disrupt epithelial cytoskeleton and barrier function."),
        q("moderate", "Pseudomembranes are composed of:", "Fibrin, mucus, neutrophils, and necrotic epithelial debris", ["Amyloid only", "Keratin pearls", "Goblet cells only"], "Volcano-like exudates form plaques on injured mucosa."),
        q("moderate", "Enterohemorrhagic E. coli can cause:", "Hemolytic uremic syndrome", ["Pernicious anemia", "Linitis plastica", "Achalasia"], "Shiga-like toxin can injure endothelium and cause HUS."),
        q("moderate", "Giardia lamblia causes malabsorption mainly in the:", "Small intestine", ["Esophagus", "Appendix", "Anal canal"], "Giardia adheres to duodenal mucosa and impairs absorption."),
        q("high", "A hospitalized patient develops watery diarrhea after broad-spectrum antibiotics. Colonoscopy shows yellow-white plaques, and biopsy shows volcano-like mucopurulent exudates erupting from damaged crypts. Which organism is responsible?", "Clostridioides difficile", ["Salmonella typhi", "Vibrio cholerae", "Giardia lamblia"], "Antibiotic-associated pseudomembranous colitis is caused by C. difficile toxins."),
        q("high", "A child develops bloody diarrhea after eating undercooked beef, followed by thrombocytopenia, renal failure, and schistocytes from endothelial injury. Which pathogen category is most likely?", "Enterohemorrhagic E. coli", ["Vibrio cholerae", "Giardia lamblia", "H. pylori"], "EHEC produces Shiga-like toxin and can cause HUS."),
        q("high", "A camper develops foul-smelling diarrhea, bloating, flatulence, and weight loss after drinking stream water. Stool contains pear-shaped trophozoites with two nuclei. Which organism is likely?", "Giardia lamblia", ["Entamoeba histolytica", "Shigella sonnei", "Clostridioides difficile"], "Giardia causes malabsorptive diarrhea after contaminated water exposure."),
    ]),
    ("ibd", "Inflammatory Bowel Disease", [
        q("easy", "Crohn disease can affect:", "Any part of the gastrointestinal tract", ["Colon only", "Stomach only", "Appendix only"], "Crohn disease may involve mouth to anus."),
        q("easy", "Ulcerative colitis begins in the:", "Rectum", ["Terminal ileum", "Esophagus", "Duodenum"], "UC starts in the rectum and extends proximally in continuous fashion."),
        q("easy", "Noncaseating granulomas favor:", "Crohn disease", ["Ulcerative colitis", "Celiac disease", "Ischemic colitis"], "Granulomas are a classic but not universal feature of Crohn disease."),
        q("moderate", "Crohn disease classically shows:", "Skip lesions and transmural inflammation", ["Continuous mucosal disease only", "Pseudomembranes", "Goblet cell metaplasia of esophagus"], "Crohn disease is patchy and transmural."),
        q("moderate", "Ulcerative colitis inflammation is usually limited to:", "Mucosa and submucosa", ["Muscularis propria in every case", "Serosa only", "Mesentery only"], "UC is primarily a mucosal disease except in severe toxic megacolon."),
        q("moderate", "Creeping fat is associated with:", "Crohn disease", ["Ulcerative colitis", "Pseudomembranous colitis", "Celiac disease"], "Mesenteric fat wraps around inflamed bowel in Crohn disease."),
        q("moderate", "Primary sclerosing cholangitis is associated with:", "Ulcerative colitis", ["Achalasia", "Meckel diverticulum", "Pyloric stenosis"], "PSC is an important extraintestinal association of UC."),
        q("high", "A young adult has chronic diarrhea, crampy pain, perianal fistulas, and segmental terminal ileal disease. Biopsy shows transmural inflammation with noncaseating granulomas. Which diagnosis is most likely?", "Crohn disease", ["Ulcerative colitis", "Celiac disease", "Ischemic colitis"], "Transmural skip lesions and fistulas favor Crohn disease."),
        q("high", "A patient has bloody diarrhea and continuous colitis extending proximally from the rectum. Biopsy shows mucosal inflammation with crypt abscesses but no skip lesions. Which diagnosis fits best?", "Ulcerative colitis", ["Crohn disease", "Giardiasis", "Angiodysplasia"], "UC is continuous, starts at rectum, and remains mucosal."),
        q("high", "A patient with long-standing pancolitis from ulcerative colitis develops worsening dysplasia on surveillance biopsies after many years of symptoms. The increased cancer risk is most closely related to which factor?", "Duration and extent of chronic colonic inflammation", ["Presence of appendectomy scar", "Amount of gastric acid", "Number of Meckel diverticula"], "Colitis-associated carcinoma risk rises with long duration and extensive disease."),
    ]),
    ("polyps", "Intestinal Polyps and Polyposis Syndromes", [
        q("easy", "Adenomatous polyps are:", "Neoplastic epithelial polyps with dysplasia", ["Non-neoplastic lymphoid follicles", "Vascular malformations", "Congenital diverticula"], "Adenomas are dysplastic precursor lesions."),
        q("easy", "Hyperplastic polyps are most often:", "Non-neoplastic serrated mucosal proliferations", ["Invasive cancers", "Granulomas", "Lymphomas"], "Small distal hyperplastic polyps usually have little malignant potential."),
        q("easy", "Familial adenomatous polyposis is caused by mutation in:", "APC", ["MLH1", "KIT", "CFTR"], "FAP is due to germline APC mutation."),
        q("moderate", "A villous adenoma has higher cancer risk because it:", "Is often larger and has villous architecture", ["Is always infectious", "Contains gastric mucosa", "Is made of smooth muscle"], "Large size, villous architecture, and high-grade dysplasia increase risk."),
        q("moderate", "Peutz-Jeghers syndrome features:", "Hamartomatous polyps and mucocutaneous pigmentation", ["Hundreds of adenomas only", "H. pylori gastritis", "Appendiceal rupture"], "STK11 mutation causes Peutz-Jeghers syndrome."),
        q("moderate", "Juvenile polyps are usually:", "Hamartomatous polyps with cystically dilated glands", ["Always malignant", "Pure lymphomas", "Vascular ectasias"], "Sporadic juvenile polyps are hamartomatous and often present with bleeding."),
        q("moderate", "Serrated sessile lesions commonly arise in the:", "Right colon", ["Esophagus only", "Pylorus only", "Appendix only"], "Sessile serrated lesions are important right-sided precursors."),
        q("high", "A teenager has hundreds of colonic adenomatous polyps and a germline APC mutation. Without colectomy, colorectal carcinoma is nearly inevitable. Which syndrome is present?", "Familial adenomatous polyposis", ["Lynch syndrome", "Peutz-Jeghers syndrome", "Juvenile polyp"], "FAP causes numerous adenomas and near-certain cancer risk."),
        q("high", "A patient has mucocutaneous pigmentation around the lips and multiple hamartomatous small intestinal polyps with arborizing smooth muscle cores. Which syndrome is most likely?", "Peutz-Jeghers syndrome", ["FAP", "Lynch syndrome", "Serrated polyposis only"], "Peutz-Jeghers polyps have arborizing smooth muscle and pigmentation."),
        q("high", "A large sessile right-sided serrated lesion shows abnormal crypt architecture and is associated with CpG island methylation. Which colorectal cancer pathway can it enter?", "Serrated neoplasia pathway", ["Classic APC-beta-catenin pathway only", "BCR-ABL pathway", "PML-RARA pathway"], "Sessile serrated lesions can progress through methylator phenotype and mismatch repair silencing."),
    ]),
    ("colorectal-cancer", "Colorectal Carcinoma and Molecular Pathways", [
        q("easy", "Most colorectal carcinomas are:", "Adenocarcinomas", ["Squamous carcinomas", "GISTs", "Melanomas"], "Colorectal epithelium gives rise to adenocarcinoma."),
        q("easy", "The classic adenoma-carcinoma sequence begins with loss of:", "APC", ["KIT", "PIGA", "HBB"], "APC loss activates WNT signaling early."),
        q("easy", "Lynch syndrome is caused by defects in:", "DNA mismatch repair genes", ["APC only", "CFTR", "Factor VIII"], "Lynch syndrome involves germline mismatch repair mutation."),
        q("moderate", "Right-sided colon cancers often present with:", "Iron deficiency anemia", ["Obstruction first in every case", "Dysphagia", "Hematemesis"], "Right-sided tumors can bleed occultly and become large before obstruction."),
        q("moderate", "Left-sided colon cancers often present with:", "Change in bowel habits and obstruction", ["Painless jaundice", "Achalasia", "Steatorrhea only"], "Left-sided annular tumors narrow the lumen."),
        q("moderate", "Microsatellite instability results from:", "Mismatch repair deficiency", ["Excess gastrin", "APC protein overexpression", "Portal hypertension"], "Mismatch repair failure creates unstable repetitive DNA sequences."),
        q("moderate", "KRAS mutation in colorectal carcinoma is important because it:", "Predicts poor response to anti-EGFR therapy", ["Guarantees response to cetuximab", "Causes celiac disease", "Eradicates adenomas"], "Activating KRAS bypasses EGFR signaling blockade."),
        q("high", "An older patient has occult blood loss and iron deficiency anemia. Colonoscopy shows a large exophytic cecal mass. Biopsy reveals invasive glands with desmoplastic stroma. Which diagnosis is most likely?", "Right-sided colorectal adenocarcinoma", ["Ulcerative colitis", "Hyperplastic polyp", "Appendicitis"], "Right-sided colon cancer often presents with occult bleeding and anemia."),
        q("high", "A patient has several relatives with early colon and endometrial cancers. Tumor testing shows microsatellite instability and loss of MLH1 staining. Which inherited syndrome is most likely?", "Lynch syndrome", ["Familial adenomatous polyposis", "Peutz-Jeghers syndrome", "Juvenile polyposis"], "Lynch syndrome is hereditary nonpolyposis colorectal cancer due to mismatch repair defects."),
        q("high", "A left-sided colon cancer forms an annular napkin-ring lesion that narrows the lumen and causes constipation alternating with pencil-thin stools. Which gross growth pattern explains symptoms?", "Circumferential constricting tumor", ["Exophytic nonobstructing cecal mass", "Diffuse linitis plastica", "Villous adenoma only"], "Left-sided cancers commonly encircle and constrict the bowel."),
    ]),
    ("appendix-peritoneum", "Appendix, Peritoneum, and GI Neuroendocrine Tumors", [
        q("easy", "Acute appendicitis is usually caused by:", "Luminal obstruction", ["Barrett metaplasia", "Gluten sensitivity", "Portal hypertension"], "Obstruction permits bacterial overgrowth and inflammation."),
        q("easy", "The diagnostic histologic feature of acute appendicitis is:", "Neutrophils in muscularis propria", ["Goblet cells in esophagus", "Villous atrophy", "Signet-ring cells"], "Transmural neutrophilic inflammation confirms acute appendicitis."),
        q("easy", "Carcinoid tumors are now called:", "Neuroendocrine tumors", ["GISTs", "Adenomas", "Hamartomas"], "Carcinoids are well-differentiated neuroendocrine tumors."),
        q("moderate", "Appendiceal obstruction commonly results from:", "Fecalith, lymphoid hyperplasia, or tumor", ["Low acid secretion", "Celiac antibodies", "Achalasia"], "Several processes can obstruct the appendiceal lumen."),
        q("moderate", "Pseudomyxoma peritonei is associated with:", "Mucinous appendiceal neoplasm", ["H. pylori gastritis", "Celiac sprue", "Achalasia"], "Mucin-producing appendiceal tumors can seed peritoneum with mucin."),
        q("moderate", "Carcinoid syndrome usually requires:", "Liver metastases from GI neuroendocrine tumor", ["Tumor limited to appendix tip", "H. pylori infection", "APC mutation only"], "Liver metastases allow serotonin to bypass hepatic metabolism."),
        q("moderate", "Appendiceal neuroendocrine tumors most often arise at the:", "Tip of the appendix", ["Esophagogastric junction", "Rectosigmoid junction", "Pylorus"], "Small appendiceal neuroendocrine tumors commonly occur at the tip."),
        q("high", "A patient has right lower quadrant pain, fever, and rebound tenderness. Appendectomy shows luminal obstruction and neutrophils extending into the muscularis propria. Which diagnosis is present?", "Acute appendicitis", ["Crohn disease", "Ulcerative colitis", "Meckel diverticulum"], "Neutrophils in the muscularis propria establish acute appendicitis."),
        q("high", "A patient has gelatinous ascites filling the peritoneal cavity. Pathology shows abundant mucin with mucinous epithelial cells from an appendiceal tumor. Which condition is this?", "Pseudomyxoma peritonei", ["Peritoneal tuberculosis", "Mesothelioma", "Ischemic colitis"], "Appendiceal mucinous neoplasms can cause pseudomyxoma peritonei."),
        q("high", "A patient with metastatic ileal neuroendocrine tumor to the liver develops episodic flushing, diarrhea, bronchospasm, and right-sided valvular fibrosis. Which secreted mediator is most implicated?", "Serotonin", ["Gastrin", "Insulin", "Intrinsic factor"], "Carcinoid syndrome is mediated largely by serotonin and related vasoactive products."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch17-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 17 questions, got {len(chapter_questions)}")
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
    short_high = [q["id"] for q in chapter_questions if q["difficulty"] == "high" and len(q["prompt"].split()) < 24]
    if short_high:
        raise ValueError(f"High-level prompts too short: {short_high[:5]}")
    if all_questions is not None:
        ids = [q.get("id") for q in all_questions]
        duplicates = [qid for qid, count in Counter(ids).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate ids: {duplicates[:10]}")


def main():
    chapter_questions = build_questions()
    validate(chapter_questions)
    total_removed = 0
    for data_path in DATA_PATHS:
        data = json.loads(data_path.read_text(encoding="utf-8-sig"))
        existing = data.get("questions", [])
        kept = [
            question for question in existing
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch17-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 17 questions")
    print(f"Removed {total_removed} existing Chapter 17 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 17 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
