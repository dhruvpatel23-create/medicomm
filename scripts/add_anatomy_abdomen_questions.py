import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Abdomen"
BASE = {"subjectId": "anatomy", "subjectTitle": "Anatomy", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("introduction-abdominal-wall", "Introduction and Anterior Abdominal Wall", [
        q("The abdomen extends superiorly into the thoracic cage up to the:", "Diaphragm", ["Pelvic diaphragm", "Inguinal ligament", "Perineal membrane"], "The diaphragm forms the superior boundary and domes upward into the thorax."),
        q("The main anterolateral abdominal wall muscles include external oblique, internal oblique and:", "Transversus abdominis", ["Serratus anterior", "Psoas minor", "Piriformis"], "These three flat muscles form the layered abdominal wall."),
        q("Rectus abdominis lies within the:", "Rectus sheath", ["Femoral sheath", "Carotid sheath", "Axillary sheath"], "The aponeuroses of flat muscles form the rectus sheath."),
        q("The linea alba is formed by:", "Interlacing aponeuroses in the midline", ["Fusion of ribs", "Umbilical vein only", "Deep fascia of thigh"], "It is the midline tendinous raphe between rectus muscles."),
        q("The umbilicus is commonly at the level of:", "L3-L4 disc", ["T4-T5 disc", "C6 vertebra", "S2 vertebra"], "The umbilicus is a useful surface landmark near L3-L4."),
        q("The inguinal ligament extends from ASIS to:", "Pubic tubercle", ["Pubic symphysis", "Ischial spine", "Greater trochanter"], "It is the rolled lower border of external oblique aponeurosis."),
        q("The superficial inguinal ring is an opening in:", "External oblique aponeurosis", ["Transversalis fascia", "Internal oblique muscle", "Peritoneum"], "The spermatic cord exits through the superficial ring."),
        q("The deep inguinal ring is an opening in:", "Transversalis fascia", ["Skin", "External oblique aponeurosis", "Rectus abdominis"], "It is the entrance to the inguinal canal."),
        q("The roof of inguinal canal is formed mainly by:", "Arching fibers of internal oblique and transversus abdominis", ["Inguinal ligament only", "Lacunar ligament only", "Femoral vein"], "These fibers arch over the canal."),
        q("The posterior wall of inguinal canal is formed mainly by:", "Transversalis fascia", ["External oblique aponeurosis", "Skin", "Camper fascia only"], "It is reinforced medially by the conjoint tendon."),
        q("A swelling appears above and medial to the pubic tubercle and increases on coughing. Which canal is involved?", "Inguinal canal", ["Femoral canal", "Obturator canal", "Adductor canal"], "Inguinal hernias present above and medial to the pubic tubercle."),
        q("A hernia passes through the deep inguinal ring, traverses the canal and may enter the scrotum. What type is it?", "Indirect inguinal hernia", ["Direct inguinal hernia", "Femoral hernia", "Umbilical hernia only"], "Indirect hernia follows the path of the processus vaginalis through the deep ring."),
        q("A hernia pushes through Hesselbach triangle without entering the deep ring. Which type is it?", "Direct inguinal hernia", ["Indirect inguinal hernia", "Obturator hernia", "Epigastric hernia"], "Direct hernia protrudes through the posterior wall of the canal in Hesselbach triangle."),
        q("During abdominal incision, the surgeon chooses the linea alba. Why does this reduce bleeding?", "It is a relatively avascular tendinous raphe", ["It contains the inferior epigastric artery", "It is full of muscle belly", "It opens the femoral canal"], "The linea alba has fewer vessels and avoids cutting muscle fibers."),
        q("A lower abdominal incision injures iliohypogastric and ilioinguinal nerves. What postoperative problem may follow?", "Weak abdominal wall and sensory loss in groin", ["Wrist drop", "Foot drop only", "Loss of diaphragm movement"], "These L1 nerves supply lower abdominal wall motor and sensory territories."),
    ]),
    ("peritoneum-mesentery", "Peritoneum, Mesentery and Peritoneal Cavity", [
        q("The peritoneum lining the abdominal wall is:", "Parietal peritoneum", ["Visceral peritoneum", "Endothelium", "Pleura"], "Parietal peritoneum lines the body wall."),
        q("The peritoneum covering abdominal organs is:", "Visceral peritoneum", ["Parietal peritoneum", "Fibrous capsule only", "Mucosa"], "Visceral peritoneum invests organs."),
        q("The greater sac communicates with lesser sac through the:", "Epiploic foramen", ["Deep inguinal ring", "Aortic hiatus", "Femoral ring"], "The foramen of Winslow connects the two peritoneal sacs."),
        q("The anterior boundary of epiploic foramen contains the:", "Portal triad", ["Inferior vena cava only", "Ureter", "Inferior mesenteric artery"], "The hepatoduodenal ligament contains portal vein, hepatic artery and bile duct."),
        q("The greater omentum hangs from the greater curvature of stomach and:", "Proximal duodenum", ["Appendix", "Kidney", "Urinary bladder"], "It descends from stomach/proximal duodenum and attaches to transverse colon."),
        q("The lesser omentum extends from liver to lesser curvature of stomach and:", "First part of duodenum", ["Jejunum", "Spleen", "Sigmoid colon"], "It includes hepatogastric and hepatoduodenal ligaments."),
        q("Mesentery transmits vessels, nerves and lymphatics to:", "Jejunum and ileum", ["Bare area of liver only", "Kidney", "Pancreatic head only"], "The mesentery suspends small intestine from posterior abdominal wall."),
        q("A retroperitoneal organ is:", "Duodenum second part", ["Jejunum", "Appendix always", "Transverse colon"], "Most of duodenum is secondarily retroperitoneal."),
        q("An intraperitoneal organ is:", "Spleen", ["Kidney", "Pancreas except tail", "Ascending colon usually"], "Spleen is invested by peritoneum and suspended by ligaments."),
        q("Paracolic gutters allow spread of fluid between abdomen and:", "Pelvis/subphrenic spaces", ["Carpal tunnel", "Mediastinum only", "Femoral sheath only"], "These channels guide intraperitoneal fluid spread."),
        q("A posterior gastric ulcer erodes through the stomach wall and causes severe bleeding. Which artery behind the stomach is at risk?", "Splenic artery", ["Inferior epigastric artery", "Femoral artery", "Middle colic vein only"], "The splenic artery runs tortuously along the superior border of pancreas behind the stomach."),
        q("During surgery, the hepatoduodenal ligament is compressed to control hepatic bleeding. Which maneuver is this?", "Pringle maneuver", ["Trendelenburg test", "Allen test", "Lachman test"], "Compression of portal triad in hepatoduodenal ligament reduces inflow to liver."),
        q("A perforated anterior duodenal ulcer spills contents into the greater sac. Why is generalized peritonitis likely?", "Free intraperitoneal contamination spreads rapidly", ["Duodenum has no lumen", "Peritoneum is insensitive", "Omentum always seals all leaks instantly"], "Intraperitoneal leakage irritates peritoneum and can spread widely."),
        q("A patient with appendicitis first has vague periumbilical pain, then right iliac fossa pain. What changed?", "Visceral pain became parietal peritoneal irritation", ["Somatic pain became cardiac pain", "Kidney capsule ruptured", "Pleura became inflamed"], "Early visceral afferents refer to umbilicus; local parietal peritoneum gives sharp localized pain."),
        q("A pelvic abscess is drained through the posterior fornix of vagina. Which peritoneal pouch is accessed?", "Rectouterine pouch", ["Hepatorenal pouch", "Lesser sac", "Left paracolic gutter"], "The pouch of Douglas is the lowest peritoneal recess in females when upright."),
    ]),
    ("stomach-duodenum", "Stomach and Duodenum", [
        q("The stomach begins at the:", "Cardiac orifice", ["Pyloric orifice", "Ileocecal junction", "Duodenojejunal flexure"], "The esophagus enters the stomach at the cardiac orifice."),
        q("The pylorus continues as the:", "Duodenum", ["Jejunum", "Ileum", "Cecum"], "The pyloric canal opens into the first part of duodenum."),
        q("The lesser curvature gives attachment to:", "Lesser omentum", ["Greater omentum", "Mesentery proper", "Falciform ligament only"], "The hepatogastric ligament attaches along the lesser curvature."),
        q("The greater curvature gives attachment to:", "Greater omentum", ["Lesser omentum", "Coronary ligament", "Root of mesentery"], "Greater omentum descends from the greater curvature."),
        q("The arterial supply of stomach along lesser curvature includes left gastric and:", "Right gastric arteries", ["Middle colic arteries", "Inferior epigastric arteries", "Renal arteries"], "Right and left gastric arteries anastomose along lesser curvature."),
        q("The gastroduodenal artery lies posterior to:", "First part of duodenum", ["Cecum", "Left colic flexure", "Appendix"], "Posterior duodenal ulcer may erode it."),
        q("The duodenum is mostly:", "Secondarily retroperitoneal", ["Entirely intraperitoneal", "Inside spleen", "Subcutaneous"], "Parts 2-4 are fixed retroperitoneally."),
        q("The major duodenal papilla opens into the:", "Second part of duodenum", ["First part", "Third part", "Fourth part"], "Bile and main pancreatic ducts open here."),
        q("The duodenojejunal flexure is supported by:", "Suspensory muscle of duodenum", ["Falciform ligament", "Round ligament of liver", "Phrenicocolic ligament"], "The ligament of Treitz supports the flexure."),
        q("The stomach bed includes pancreas, spleen, left kidney and:", "Transverse mesocolon", ["Femoral canal", "Urinary bladder", "Prostate"], "These posterior relations form the stomach bed."),
        q("A posterior duodenal ulcer causes sudden hematemesis and shock. Which vessel was most likely eroded?", "Gastroduodenal artery", ["Inferior mesenteric artery", "Left renal vein", "Dorsalis pedis artery"], "Gastroduodenal artery runs behind the first part of duodenum."),
        q("A gastric ulcer near the lesser curvature may bleed from which arterial arcade?", "Right and left gastric arteries", ["Right and left gastroepiploic only", "Ileocolic and right colic", "Cystic artery"], "The gastric arteries run along lesser curvature."),
        q("Vomiting after annular pancreas is due to compression of which duodenal part?", "Second part of duodenum", ["First part only", "Fourth part only", "Jejunum"], "Annular pancreas encircles the descending duodenum."),
        q("A tumor at the major duodenal papilla causes obstructive jaundice. Why?", "Bile duct opens there with pancreatic duct", ["Portal vein opens there", "Spleen drains there", "Ureter passes there"], "Obstruction at papilla blocks bile flow into duodenum."),
        q("Pain from a foregut organ such as stomach is commonly referred to which region?", "Epigastrium", ["Hypogastrium", "Left leg", "Perineum"], "Foregut visceral pain commonly refers to the epigastric region."),
    ]),
    ("small-large-intestine", "Small Intestine, Large Intestine and Appendix", [
        q("Jejunum and ileum are suspended by:", "Mesentery proper", ["Lesser omentum", "Coronary ligament", "Broad ligament"], "The mesentery carries vessels and nerves to small intestine."),
        q("Jejunum has more prominent:", "Plicae circulares", ["Appendices epiploicae", "Taeniae coli", "Haustra only"], "Jejunum has thicker wall and more mucosal folds."),
        q("Ileum has more prominent:", "Peyer's patches", ["Gastric rugae", "Villi absent", "Taeniae coli"], "Aggregated lymphoid follicles are characteristic of ileum."),
        q("The cecum lies mainly in the:", "Right iliac fossa", ["Left hypochondrium", "Epigastrium", "Left lumbar region"], "The cecum is the blind beginning of large intestine."),
        q("The appendix arises from the:", "Posteromedial wall of cecum", ["Fundus of stomach", "Left colic flexure", "Second part of duodenum"], "The appendicular base is where taeniae converge on the cecum."),
        q("The most common position of appendix is:", "Retrocecal", ["Subhepatic", "Preileal only", "Pelvic only"], "Retrocecal appendix is common."),
        q("Large intestine is recognized by taeniae coli, haustra and:", "Appendices epiploicae", ["Plicae circulares", "Rugae", "Villi"], "These fat tags are typical of colon."),
        q("The transverse colon is supplied mainly by:", "Middle colic artery", ["Cystic artery", "Renal artery", "Inferior epigastric artery"], "Middle colic is a superior mesenteric branch."),
        q("The sigmoid colon is supplied by:", "Sigmoid branches of inferior mesenteric artery", ["Celiac trunk", "Renal artery", "Inferior phrenic artery"], "IMA supplies hindgut including sigmoid colon."),
        q("The rectosigmoid junction is around vertebral level:", "S3", ["T4", "L1", "C7"], "Sigmoid colon becomes rectum at S3."),
        q("A patient with appendicitis has pain at McBurney point. What does this surface point represent?", "Base of appendix", ["Fundus of gallbladder", "Pylorus", "Spleen hilum"], "McBurney point overlies the appendicular base."),
        q("A Meckel diverticulum is found on antimesenteric border of ileum. What embryological remnant explains it?", "Vitellointestinal duct", ["Urachus", "Ductus venosus", "Allantoic artery"], "Persistent vitelline duct forms Meckel diverticulum."),
        q("A carcinoma at splenic flexure may compromise a watershed area. Which arterial territories meet here?", "Superior and inferior mesenteric arteries", ["Celiac and renal arteries", "Internal and external iliac arteries", "Right and left gastric arteries"], "The splenic flexure is near the marginal watershed between SMA and IMA."),
        q("A volvulus commonly involves sigmoid colon because it has which feature?", "Long mesentery and mobility", ["No lumen", "Fixed retroperitoneal position", "Absence of blood supply"], "A mobile sigmoid loop can twist around its mesentery."),
        q("Early appendicitis causes periumbilical pain because visceral afferents enter at which spinal level?", "T10", ["C5", "S4", "L1 only"], "Midgut pain from appendix refers to T10 dermatome around umbilicus."),
    ]),
    ("liver-gallbladder-biliary", "Liver, Gallbladder and Biliary Apparatus", [
        q("The liver lies mainly in right hypochondrium and:", "Epigastrium", ["Left iliac fossa", "Perineum", "Popliteal fossa"], "The liver occupies right upper abdomen and extends into epigastrium."),
        q("The bare area of liver is related to:", "Diaphragm", ["Urinary bladder", "Femoral canal", "Appendix"], "The bare area lacks peritoneal covering and contacts diaphragm."),
        q("The porta hepatis transmits portal vein, hepatic artery and:", "Hepatic ducts", ["Ureter", "Femoral nerve", "Thoracic duct"], "These structures form the portal triad."),
        q("The portal vein is formed behind the neck of pancreas by union of splenic vein and:", "Superior mesenteric vein", ["Inferior vena cava", "Left gastric artery", "Renal vein"], "SMV and splenic vein unite to form portal vein."),
        q("The gallbladder lies on the visceral surface of liver between right lobe and:", "Quadrate lobe", ["Caudate lobe only", "Left kidney", "Spleen"], "The gallbladder fossa separates right and quadrate lobes."),
        q("The cystic duct joins common hepatic duct to form:", "Common bile duct", ["Pancreatic duct", "Portal vein", "Hepatic artery"], "CBD carries bile to the duodenum."),
        q("The cystic artery usually arises from:", "Right hepatic artery", ["Left gastric artery", "Splenic artery", "Inferior mesenteric artery"], "It is classically found in Calot triangle."),
        q("Calot triangle is bounded by cystic duct, common hepatic duct and:", "Inferior surface of liver", ["Inguinal ligament", "Spleen", "Left gastric artery"], "Modern hepatocystic triangle includes liver inferiorly."),
        q("Bile duct opens into the second part of duodenum at:", "Major duodenal papilla", ["Minor papilla", "Ileocecal valve", "Cardiac orifice"], "CBD joins main pancreatic duct and opens at major papilla."),
        q("Portal-systemic anastomosis at lower esophagus involves left gastric vein and:", "Esophageal veins", ["Great saphenous vein", "Dorsalis pedis vein", "Renal vein only"], "This site can form esophageal varices."),
        q("A patient with gallstones has pain referred to the right shoulder tip. Which nerve pathway explains this?", "Phrenic nerve irritation via diaphragm", ["Median nerve", "Common fibular nerve", "Obturator nerve"], "Inflammation near diaphragm can refer pain through C3-C5 phrenic pathways."),
        q("During cholecystectomy, the surgeon identifies Calot triangle mainly to find which artery?", "Cystic artery", ["Gastroduodenal artery", "Inferior epigastric artery", "Middle colic artery"], "Cystic artery is controlled during gallbladder removal."),
        q("A stone impacted at the ampulla causes jaundice and pancreatitis. Why are both systems affected?", "Common bile duct and pancreatic duct join near the ampulla", ["Portal vein joins the ureter", "Gallbladder drains into spleen", "Liver drains into colon"], "The hepatopancreatic ampulla receives bile and pancreatic ducts."),
        q("Caput medusae around umbilicus occurs in portal hypertension due to reopening of which vein?", "Paraumbilical veins", ["Femoral vein", "Short saphenous vein", "Azygos vein only"], "Paraumbilical veins connect portal system to superficial abdominal wall veins."),
        q("A liver abscess ruptures superiorly through bare area. Which cavity is most directly threatened?", "Pleural/subphrenic region near diaphragm", ["Knee joint", "Carpal tunnel", "Femoral sheath"], "Bare area is against diaphragm, so infection may track subphrenically or toward thorax."),
    ]),
    ("pancreas-spleen", "Pancreas and Spleen", [
        q("The pancreas is mainly:", "Secondarily retroperitoneal", ["Entirely intraperitoneal", "Subcutaneous", "Inside liver"], "Except tail, pancreas is retroperitoneal."),
        q("The head of pancreas lies within the curve of:", "Duodenum", ["Spleen", "Sigmoid colon", "Cecum"], "The duodenum embraces the pancreatic head."),
        q("The tail of pancreas reaches the:", "Hilum of spleen", ["Right kidney", "Appendix", "Femoral ring"], "The tail passes in the splenorenal ligament to splenic hilum."),
        q("The main pancreatic duct usually joins:", "Common bile duct", ["Portal vein", "Inferior vena cava", "Ureter"], "It joins CBD near the hepatopancreatic ampulla."),
        q("The splenic artery runs along the superior border of:", "Pancreas", ["Kidney", "Cecum", "Rectum"], "It is tortuous and closely related to pancreas."),
        q("The spleen lies mainly in the:", "Left hypochondrium", ["Right iliac fossa", "Hypogastrium", "Right lumbar region"], "Spleen is protected by left lower ribs."),
        q("The spleen is related to ribs:", "9 to 11", ["1 to 3", "4 to 6", "12 only"], "Its long axis follows the 10th rib."),
        q("The splenorenal ligament contains splenic vessels and:", "Tail of pancreas", ["Appendix", "Gallbladder", "Ureteric orifice"], "The pancreatic tail reaches splenic hilum through this ligament."),
        q("Accessory spleens are commonly found near:", "Splenic hilum", ["Femoral canal", "Inguinal ring", "Umbilicus only"], "Splenunculi often occur near hilum or splenic ligaments."),
        q("The spleen develops in:", "Dorsal mesogastrium", ["Ventral mesentery", "Septum transversum only", "Urogenital ridge"], "Spleen is a mesodermal derivative in dorsal mesogastrium."),
        q("A carcinoma in the head of pancreas causes painless progressive jaundice. Which structure is compressed?", "Common bile duct", ["Inferior mesenteric artery", "Left ureter", "Appendicular artery"], "CBD passes through/behind pancreatic head."),
        q("A posterior gastric ulcer erodes into the pancreas. Why can pain radiate to the back?", "Pancreas lies posterior to stomach", ["Pancreas is in femoral triangle", "Spleen has no capsule", "Appendix lies behind stomach"], "The stomach bed includes pancreas; posterior ulcers can involve it."),
        q("A child with left lower rib fracture develops shock and left upper quadrant tenderness. Which organ is most at risk?", "Spleen", ["Appendix", "Gallbladder", "Urinary bladder"], "Spleen is protected by ribs 9-11 and may rupture with rib trauma."),
        q("During splenectomy, injury to the pancreatic tail may cause leakage of which secretion?", "Pancreatic enzymes", ["Bile from cystic duct", "Urine", "Synovial fluid"], "The tail of pancreas lies close to the splenic hilum."),
        q("A splenic rupture irritates the diaphragm and causes left shoulder pain. What is this referred pain called?", "Kehr sign", ["Murphy sign", "Rovsing sign", "Tinel sign"], "Blood under the diaphragm irritates phrenic nerve, referring pain to shoulder."),
    ]),
    ("kidneys-suprarenals-ureters", "Kidneys, Suprarenal Glands and Ureters", [
        q("The kidneys are primarily:", "Retroperitoneal", ["Intraperitoneal", "Intrapleural", "Subcutaneous"], "Kidneys lie on posterior abdominal wall behind peritoneum."),
        q("The right kidney lies lower than the left because of the:", "Liver", ["Spleen", "Heart", "Bladder"], "The large right lobe of liver depresses the right kidney."),
        q("The renal hilum transmits vein, artery and pelvis arranged anterior to posterior as:", "Vein, artery, pelvis", ["Artery, vein, pelvis", "Pelvis, vein, artery", "Vein, pelvis, artery"], "Mnemonic VAP from anterior to posterior."),
        q("The left renal vein crosses anterior to the:", "Aorta", ["Inferior vena cava only", "Ureter", "Duodenum fourth part"], "It passes between SMA and aorta to reach IVC."),
        q("The suprarenal glands lie on the:", "Superior poles of kidneys", ["Inferior poles", "Iliac crests", "Gallbladder"], "They cap the kidneys."),
        q("The right suprarenal vein drains into:", "Inferior vena cava", ["Left renal vein", "Portal vein", "Splenic vein"], "Right suprarenal vein is short and drains directly to IVC."),
        q("The left suprarenal vein drains into:", "Left renal vein", ["Inferior vena cava directly", "Portal vein", "Azygos vein"], "It commonly joins the left renal vein."),
        q("The ureter crosses the pelvic brim near bifurcation of:", "Common iliac artery", ["Celiac trunk", "Renal artery", "Femoral artery"], "This is one common site of ureteric narrowing."),
        q("Ureteric constrictions occur at pelviureteric junction, pelvic brim and:", "Ureterovesical junction", ["Hepatic hilum", "Duodenal papilla", "Splenic hilum"], "Stones lodge at the three anatomical narrowings."),
        q("Renal pain may radiate from loin to groin because afferents follow:", "T11-L2 segments", ["C3-C5", "S2-S4 only", "C8-T1"], "Ureteric pain follows sympathetic afferents to lower thoracic/upper lumbar segments."),
        q("A stone at the ureterovesical junction causes pain radiating to scrotum or labium. Why?", "Shared segmental innervation with genitofemoral/ilioinguinal areas", ["Direct skin continuity", "Femoral nerve compression", "Portal hypertension"], "Lower ureter pain may refer to groin and external genital region."),
        q("A left renal vein is compressed between SMA and aorta. Which condition does this describe?", "Nutcracker syndrome", ["Pringle maneuver", "Volkmann contracture", "Trendelenburg sign"], "The left renal vein passes through the aortomesenteric angle."),
        q("A posterior abdominal stab near the 12th rib injures the upper pole of kidney. Which pleural relation matters?", "Diaphragm and costodiaphragmatic recess lie nearby", ["Pleura never descends", "Kidney is anterior to sternum", "Lung root covers kidney"], "Upper kidney is related to diaphragm and pleura, especially near 12th rib."),
        q("During hysterectomy, the ureter is at risk near the uterine artery. What relation is remembered?", "Ureter passes under uterine artery", ["Ureter passes through femoral canal", "Ureter lies inside ovary", "Uterine artery passes through kidney"], "Water under the bridge: ureter under uterine artery."),
        q("A renal hilum mass compresses the most anterior structure first. Which structure is affected?", "Renal vein", ["Renal pelvis", "Renal artery", "Ureter behind psoas"], "At the hilum, renal vein is most anterior."),
    ]),
    ("posterior-wall-vessels-nerves", "Posterior Abdominal Wall, Vessels and Nerves", [
        q("The abdominal aorta begins at the aortic hiatus at level:", "T12", ["T4", "L4", "S3"], "It enters abdomen through the diaphragm at T12."),
        q("The abdominal aorta bifurcates at level:", "L4", ["C6", "T8", "S5"], "It divides into common iliac arteries near L4."),
        q("The inferior vena cava is formed by union of common iliac veins at:", "L5", ["T12", "C7", "S3"], "The IVC begins around L5 on the right side."),
        q("The celiac trunk supplies:", "Foregut", ["Midgut", "Hindgut", "Lower limb only"], "Celiac trunk supplies abdominal foregut derivatives."),
        q("Superior mesenteric artery supplies:", "Midgut", ["Foregut only", "Hindgut only", "Kidney"], "SMA supplies midgut from distal duodenum to proximal two-thirds transverse colon."),
        q("Inferior mesenteric artery supplies:", "Hindgut", ["Foregut", "Midgut", "Liver only"], "IMA supplies distal one-third transverse colon to upper anal canal."),
        q("Psoas major flexes the:", "Hip joint", ["Elbow", "Wrist", "Shoulder"], "Psoas major with iliacus forms iliopsoas."),
        q("Quadratus lumborum is supplied by:", "Subcostal and lumbar nerves", ["Phrenic nerve only", "Vagus nerve", "Facial nerve"], "It is innervated by T12 and lumbar ventral rami."),
        q("The lumbar plexus forms within:", "Psoas major", ["Rectus sheath", "Spleen", "Liver"], "Lumbar plexus branches emerge around psoas."),
        q("The femoral nerve emerges from the:", "Lateral border of psoas major", ["Medial border", "Anterior surface as obturator", "Aortic hiatus"], "Femoral nerve descends between psoas and iliacus."),
        q("A midline aneurysm above umbilicus compresses structures behind stomach. Which major vessel is dilated?", "Abdominal aorta", ["Femoral artery", "Portal vein only", "Dorsalis pedis"], "Aortic aneurysm is often pulsatile and midline."),
        q("An aortic aneurysm at L4 threatens bifurcation into which arteries?", "Common iliac arteries", ["Renal arteries", "Gonadal arteries", "Inferior epigastric arteries"], "The abdominal aorta bifurcates into right and left common iliac arteries."),
        q("A tumor invading psoas causes difficulty flexing the hip and pain on hip extension. Which muscle is involved?", "Psoas major", ["Gluteus medius", "Rectus abdominis", "Soleus"], "Psoas major is a strong hip flexor and lies on posterior abdominal wall."),
        q("A lesion at the lateral border of psoas weakens knee extension. Which nerve is affected?", "Femoral nerve", ["Obturator nerve", "Tibial nerve", "Vagus nerve"], "Femoral nerve supplies quadriceps after emerging lateral to psoas."),
        q("A midgut volvulus twists around a major arterial root. Which artery is central to the twist?", "Superior mesenteric artery", ["Celiac trunk", "Inferior mesenteric artery", "Renal artery"], "Midgut mesentery is organized around the SMA axis."),
    ]),
    ("diaphragm-surface-clinical", "Diaphragm, Surface Marking and Clinical Anatomy", [
        q("The caval opening of diaphragm is at vertebral level:", "T8", ["T10", "T12", "L4"], "IVC passes through the central tendon at T8."),
        q("The esophageal hiatus is at vertebral level:", "T10", ["T8", "T12", "L5"], "Esophagus and vagal trunks pass at T10."),
        q("The aortic hiatus is at vertebral level:", "T12", ["T8", "T10", "C6"], "Aorta, thoracic duct and azygos structures pass at T12."),
        q("The motor supply of diaphragm is:", "Phrenic nerve", ["Vagus nerve", "Intercostal nerve T12 only", "Femoral nerve"], "Phrenic nerve C3-C5 supplies motor fibers."),
        q("The central tendon of diaphragm is pierced by:", "Inferior vena cava", ["Aorta", "Esophagus", "Ureter"], "IVC passes through central tendon."),
        q("The transpyloric plane lies at approximately:", "L1", ["T4", "L5", "S3"], "It is a classic surface plane at L1."),
        q("The gallbladder fundus is marked where right midclavicular line meets:", "Costal margin", ["Inguinal ligament", "Left iliac crest", "Umbilicus"], "This is the surface point for gallbladder fundus."),
        q("McBurney point lies between ASIS and:", "Umbilicus", ["Xiphoid", "Pubic symphysis", "Ischial tuberosity"], "It is about one-third from ASIS to umbilicus."),
        q("The subcostal plane passes through:", "L3", ["C6", "T4", "S2"], "It is a surface plane through the lowest costal margin, around L3."),
        q("The transtubercular plane passes through:", "L5", ["T1", "T8", "S5"], "It passes through iliac tubercles and L5."),
        q("A patient with diaphragmatic irritation has shoulder-tip pain. Which spinal roots explain referral?", "C3-C5", ["T10 only", "L4-L5", "S2-S4"], "Phrenic nerve shares C3-C5 segments with shoulder skin."),
        q("A stab wound through the left 8th intercostal space in midaxillary line may injure abdominal viscera. Why?", "Diaphragm rises high under ribs", ["Abdomen starts below iliac crest", "Pleura is absent above ribs", "Spleen is in pelvis"], "Upper abdominal organs lie protected under lower ribs due to diaphragm dome."),
        q("A surgeon marks the pylorus on the transpyloric plane. Which level is being used?", "L1 vertebral level", ["T12 sacral level", "L5 vertebral level", "S3 level"], "The transpyloric plane passes through L1 and many upper abdominal landmarks."),
        q("A patient has maximal tenderness at the gallbladder fundus point and inspiratory arrest on palpation. Which sign is this?", "Murphy sign", ["Rovsing sign", "Kehr sign", "Trendelenburg sign"], "Murphy sign suggests acute cholecystitis."),
        q("Rebound tenderness in right iliac fossa suggests appendicitis because which layer is inflamed?", "Parietal peritoneum", ["Visceral peritoneum only", "Renal cortex", "Pleura"], "Localized sharp pain and rebound occur when parietal peritoneum is irritated."),
    ]),
]


def main():
    questions = []
    for topic_index, (slug, topic, rows) in enumerate(TOPICS):
        if len(rows) != 15:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 15")
        for question_index, row in enumerate(rows, 1):
            options = list(row["wrong"])
            answer_index = (topic_index + question_index - 1) % 4
            options.insert(answer_index, row["answer"])
            questions.append({
                **BASE,
                "id": f"anatomy-abdomen-{slug}-{question_index:02d}",
                "topic": topic,
                "difficulty": "moderate" if question_index <= 5 else "high" if question_index <= 10 else "very high",
                "prompt": row["prompt"],
                "options": options,
                "answerIndex": answer_index,
                "answer": row["answer"],
                "explanation": row["explanation"],
            })
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "anatomy" and x.get("chapterTitle") == CHAPTER)] + questions
    if len(TOPICS) != 9 or len(questions) != 135:
        raise AssertionError(f"Expected 9 topics and 135 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != len(questions):
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
