import json
from pathlib import Path

DATA_PATHS=[Path("runtime-data/users.json"),Path("data/users.json")]
CHAPTER="Excretory System"; CHAPTER_ORDER=9
BASE={"subjectId":"physiology","subjectTitle":"Physiology","chapterTitle":CHAPTER,"source":"ai","sourcePdf":"physiology 1.pdf","sourcePdfPageStart":387,"sourcePdfPageEnd":459,"chapterOrder":CHAPTER_ORDER,"imageUrls":[]}
def q(p,a,w,e,c=False): return {"prompt":p,"options":[a,*w],"answerIndex":0,"answer":a,"explanation":e,"difficulty":"moderate","tags":["clinical"] if c else []}
TOPICS=[
("kidneys-anatomy-blood-flow","Kidneys: Functional Anatomy and Blood Flow",1,[
q("The structural and functional unit of kidney is the:","Nephron",["Glomerulus only","Collecting duct only","Renal pelvis"],"Nephron is the kidney's functional unit."),
q("Renal corpuscle consists of glomerulus and:","Bowman's capsule",["Loop of Henle","Ureter","Macula densa only"],"Renal corpuscle contains glomerular tuft within Bowman's capsule."),
q("Juxtaglomerular apparatus is important for:","Renin release and tubular feedback",["Bile secretion","ECG recording","Platelet aggregation"],"JGA participates in renin secretion and tubuloglomerular feedback."),
q("A patient with renal artery stenosis activates renin release mainly from cells in the:","Juxtaglomerular apparatus",["Renal pelvis","Urethra","Glomerular filtrate"],"Reduced perfusion stimulates JG cells to release renin.",True),
q("Most nephrons are:","Cortical nephrons",["Juxtamedullary nephrons","Atonic nephrons","Portal nephrons"],"Cortical nephrons form the majority."),
q("Long loops of Henle are characteristic of:","Juxtamedullary nephrons",["Only cortical nephrons","Renal pelvis","Ureter"],"Juxtamedullary nephrons help concentration by long loops."),
q("Renal blood flow is high relative to kidney weight mainly for:","Filtration and homeostatic function",["Heat production only","Bile storage","Respiration"],"High RBF supports filtration and regulation."),
q("A fall in renal perfusion pressure within normal range may not reduce flow much because of:","Autoregulation",["ABO grouping","Myelin conduction","Tetanus"],"Renal autoregulation stabilizes flow/GFR.",True),
q("Afferent arteriole supplies blood to:","Glomerulus",["Ureter","Bladder","Collecting pelvis only"],"Afferent arteriole enters glomerular capillaries."),
q("Efferent arteriolar constriction initially tends to maintain glomerular pressure. This affects:","GFR",["ESR","Tidal volume","Blood group"],"Efferent tone influences glomerular capillary pressure and filtration.",True),
]),
("urine-formation","Mechanism of Urine Formation: Glomerular Filtration and Tubular Transport",2,[
q("Glomerular filtrate is normally almost free of:","Proteins and blood cells",["Glucose","Sodium","Water"],"Filtration barrier restricts cells and most proteins."),
q("Normal GFR is approximately:","125 mL/min",["5 mL/min","1 L/min","500 mL/min"],"Adult GFR is about 125 mL/min."),
q("Filtration fraction is ratio of GFR to:","Renal plasma flow",["Renal blood pressure","Urine volume","Plasma protein"],"FF = GFR/RPF."),
q("Inulin clearance measures:","GFR",["RPF","Tubular secretion only","Urine pH"],"Inulin is freely filtered and neither reabsorbed nor secreted."),
q("Creatinine clearance is used clinically as an estimate of:","GFR",["RBC mass","Lung diffusion","Cardiac axis"],"Creatinine clearance approximates GFR.",True),
q("Most filtered sodium and water are reabsorbed in:","Proximal tubule",["Urethra","Bladder","Bowman's space only"],"Proximal tubule reabsorbs bulk filtrate."),
q("Glucose reabsorption normally occurs mainly by:","Na+-glucose co-transport",["Simple lipid diffusion","Phagocytosis","Fibrinolysis"],"Glucose uses sodium-linked transport."),
q("Glycosuria in uncontrolled diabetes occurs when filtered glucose exceeds:","Tubular transport maximum",["ABO threshold","Surfactant level","Platelet count"],"Excess filtered glucose exceeds reabsorptive Tm.",True),
q("PAH clearance is used to estimate:","Renal plasma flow",["GFR exactly","Urine osmolality only","Bladder capacity"],"PAH is used for effective RPF."),
q("Proteinuria suggests damage to:","Glomerular filtration barrier",["SA node","Pleura","Motor end plate"],"Increased protein filtration suggests barrier dysfunction.",True),
]),
("concentration-dilution-acidification","Concentration, Dilution and Acidification of Urine",3,[
q("Counter-current multiplier is located mainly in:","Loop of Henle",["Urethra","Bladder","Glomerular capsule"],"Loop of Henle creates medullary gradient."),
q("Vasa recta function as counter-current:","Exchangers",["Multipliers","Pacemakers","Valves"],"Vasa recta preserve medullary gradient."),
q("ADH increases water reabsorption mainly in:","Collecting ducts",["Bowman's capsule","Urethra","Proximal glomerulus"],"ADH increases collecting duct water permeability."),
q("Water deprivation causes urine to become:","Concentrated",["Maximally dilute","Protein-rich always","Isotonic always"],"ADH rises and conserves water.",True),
q("Excess water intake normally causes:","Water diuresis",["Osmotic diuresis","Haematuria","Anuria"],"Low ADH permits dilute urine excretion."),
q("Osmotic diuresis may occur in diabetes mellitus due to filtered:","Glucose",["Albumin only","Haemoglobin","Platelets"],"Unreabsorbed glucose holds water in tubule.",True),
q("Urine acidification depends importantly on secretion of:","H+ ions",["O2","Albumin","Fibrin"],"Tubules secrete H+ to acidify urine."),
q("Filtered bicarbonate is normally mostly:","Reabsorbed",["Excreted unchanged","Converted to RBCs","Stored in bladder"],"Kidneys reclaim filtered HCO3-."),
q("New bicarbonate generation is linked to excretion of H+ as ammonium and:","Titratable acid",["Oxyhaemoglobin","Surfactant","Agglutinin"],"New HCO3- is added when H+ is excreted with buffers."),
q("A patient with impaired distal H+ secretion develops metabolic acidosis because kidney cannot adequately:","Acidify urine",["Make bile","Conduct ECG","Clot blood"],"Defective acidification impairs acid excretion.",True),
]),
("body-fluid-regulation","Regulation of Body Fluid Osmolality, Composition and Volume",4,[
q("Major extracellular cation is:","Sodium",["Potassium","Magnesium","Protein"],"Na+ dominates ECF osmolality."),
q("Major intracellular cation is:","Potassium",["Sodium","Calcium","Chloride"],"K+ is the major ICF cation."),
q("Body fluid osmolality is regulated mainly by water balance and:","ADH/thirst mechanisms",["ABO antibodies","ECG axis","Platelets"],"ADH and thirst control water."),
q("Rise in plasma osmolality stimulates:","Thirst and ADH release",["Diuresis without ADH","RBC destruction","Bronchodilation"],"Osmoreceptors trigger thirst/ADH.",True),
q("Effective circulating volume is sensed by volume receptors and affects renal:","Sodium excretion",["Vision","Hearing","Blood group"],"Volume sensors regulate NaCl/water excretion."),
q("Aldosterone primarily increases reabsorption of:","Sodium",["Urea only","Albumin","Bilirubin"],"Aldosterone promotes Na+ reabsorption in distal nephron."),
q("A patient with dehydration has increased ADH, causing increased:","Water reabsorption",["Water excretion","Proteinuria","Glycosuria"],"ADH conserves water.",True),
q("ANP generally promotes:","Natriuresis",["Sodium retention","Renin release","Urine acidification only"],"ANP promotes sodium excretion."),
q("Water intoxication results from excess water causing low plasma:","Osmolality",["RBC count","Platelet count","Renal blood flow only"],"Excess water dilutes ECF."),
q("SIADH causes hyponatraemia mainly by excess:","Water retention",["Sodium loss only","Protein loss","RBC destruction"],"Excess ADH retains free water.",True),
]),
("acid-base-balance","Physiology of Acid-Base Balance",5,[
q("Normal arterial blood pH is about:","7.4",["6.4","8.4","5.0"],"Blood pH is tightly maintained near 7.4."),
q("Primary immediate defence against pH change is:","Buffer system",["Renal biopsy","Micturition","Blood grouping"],"Buffers act first."),
q("Major extracellular buffer is:","Bicarbonate buffer",["Melanin","Fibrin","Surfactant"],"Bicarbonate is the principal ECF buffer."),
q("Respiratory regulation of pH works by changing:","CO2 excretion",["ABO antigens","Creatinine production","Platelet plug"],"Ventilation alters PaCO2 and pH."),
q("Renal regulation of pH includes H+ secretion and:","Bicarbonate handling",["ECG intervals","Myelin formation","Lymphocyte typing"],"Kidneys reclaim/generate bicarbonate and excrete acid."),
q("Diarrhoea can cause metabolic acidosis due to loss of:","Bicarbonate",["Oxygen","Platelets","Albumin only"],"GI HCO3- loss causes metabolic acidosis.",True),
q("Vomiting can cause metabolic alkalosis due to loss of:","Gastric acid",["Bicarbonate from stool","RBCs","Surfactant"],"Loss of HCl favors alkalosis.",True),
q("Respiratory acidosis is caused by:","Hypoventilation",["Hyperventilation","Excess renal acid loss","High altitude only"],"CO2 retention lowers pH."),
q("Respiratory alkalosis is caused by:","Hyperventilation",["Hypoventilation","Renal failure","Diarrhoea"],"CO2 washout raises pH."),
q("A COPD patient retaining CO2 develops which primary disorder?", "Respiratory acidosis", ["Metabolic alkalosis","Respiratory alkalosis","Normal pH always"], "CO2 retention from hypoventilation causes respiratory acidosis.", True),
]),
("applied-renal","Applied Renal Physiology Including Renal Function Tests",6,[
q("Oliguria means urine output is:","Decreased",["Increased","Bloody only","Foamy only"],"Oliguria is low urine output."),
q("Polyuria means urine output is:","Increased",["Absent","Painful","Protein-free"],"Polyuria is increased urine volume."),
q("Nephrotic syndrome is characterized by heavy:","Proteinuria",["Glycosuria only","Haematuria only","Ketonuria only"],"Protein loss is central in nephrotic syndrome.",True),
q("Acute renal failure develops over:", "Short period", ["Years only","Embryonic life","Only after transfusion"], "ARF is rapid decline in renal function."),
q("Chronic renal failure is usually:", "Progressive long-term renal dysfunction", ["Instant and reversible always","Normal GFR","Only bladder disease"], "CRF is gradual irreversible decline."),
q("Creatinine clearance is commonly used to assess:", "GFR", ["RPF only","Urine pH only","Bladder reflex"], "Creatinine clearance estimates filtration."),
q("PAH clearance is used to assess:", "Renal plasma flow", ["GFR exactly","Acid-base nomogram","Blood group"], "PAH clearance estimates effective RPF."),
q("A patient with renal failure develops high urea and creatinine because kidneys fail to:", "Excrete nitrogenous waste", ["Make haemoglobin","Ventilate alveoli","Close valves"], "Renal failure impairs waste excretion.", True),
q("Haemodialysis works as an artificial kidney mainly by:", "Diffusion across semipermeable membrane", ["ECG recording","Pulmonary diffusion","Platelet aggregation"], "Dialysis removes solutes across a membrane."),
q("Loop diuretics act mainly on thick ascending limb and can cause increased:", "Salt and water excretion", ["Bile flow","RBC production","Surfactant"], "Blocking NaCl reabsorption increases diuresis.", True),
]),
("micturition","Physiology of Micturition",7,[
q("Micturition means:", "Emptying of urinary bladder", ["Urine formation only","GFR measurement","Renin release"], "Micturition is bladder emptying."),
q("Detrusor muscle is present in:", "Urinary bladder wall", ["Ureter only","Renal cortex","Glomerulus"], "Detrusor is bladder smooth muscle."),
q("Internal urethral sphincter is mainly:", "Smooth muscle", ["Skeletal muscle","Cardiac muscle","Cartilage"], "Internal sphincter is involuntary smooth muscle."),
q("External urethral sphincter is mainly:", "Skeletal muscle", ["Smooth muscle","Cardiac muscle","Endothelium"], "External sphincter allows voluntary control."),
q("Parasympathetic activity during micturition causes detrusor:", "Contraction", ["Relaxation always","Paralysis","No effect"], "Parasympathetic nerves contract detrusor."),
q("A spinal cord lesion initially causes urinary retention due to:", "Atonic bladder/spinal shock", ["High GFR","Proteinuria","Glycosuria"], "Loss of reflex activity can cause atonic bladder.", True),
q("Stretch receptors in bladder wall signal:", "Bladder filling", ["Blood oxygen","Renal plasma flow","Acid-base status"], "Bladder filling activates stretch receptors."),
q("Voluntary control of micturition mainly acts through:", "External urethral sphincter", ["Glomerulus","Loop of Henle","Macula densa"], "External sphincter is under voluntary somatic control."),
q("A patient with loss of bladder sensation develops overdistension and overflow. This suggests:", "Deafferentation/atonic bladder", ["Hyperactive SA node","Nephrotic syndrome","Respiratory acidosis"], "Loss of sensory afferents impairs micturition reflex.", True),
q("Supraspinal centres normally help coordinate:", "Micturition reflex and voluntary control", ["ABO typing","GFR filtration barrier","Bilirubin transport"], "Higher centres regulate timing and coordination of voiding.", True),
]),
]
def build():
 out=[]
 for slug,topic,order,rows in TOPICS:
  for i,row in enumerate(rows,1):
   shift=(order+i)%4; opts=row["options"][shift:]+row["options"][:shift]; ans=row["answer"]
   out.append({**BASE,**row,"id":f"physiology-excretory-{slug}-{i:02d}","topic":topic,"topicTitle":topic,"topicOrder":order,"options":opts,"answerIndex":opts.index(ans),"answer":ans})
 return out
def validate(qs):
 if len(qs)!=70: raise ValueError("Expected 70")
 if len({q["id"] for q in qs})!=70: raise ValueError("Dupes")
 for _,topic,_,_ in TOPICS:
  t=[q for q in qs if q["topic"]==topic]
  if len(t)!=10 or sum("clinical" in q.get("tags",[]) for q in t)<3: raise ValueError(topic)
 for q in qs:
  if q["answer"]!=q["options"][q["answerIndex"]]: raise ValueError(q["id"])
def update(path,qs):
 data=json.loads(path.read_text(encoding="utf-8-sig")); ids={q["id"] for q in qs}
 data["questions"]=[q for q in data.get("questions",[]) if q.get("id") not in ids]+qs
 data["questions"].sort(key=lambda x:x.get("id",""))
 path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def main():
 qs=build(); validate(qs)
 for p in DATA_PATHS:
  update(p,qs); print(f"Added {len(qs)} physiology questions to {p}.")
 for _,topic,_,_ in TOPICS: print(f"- {topic}: 10 questions")
if __name__=="__main__": main()
