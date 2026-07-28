import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Endocrinal System"
CHAPTER_ORDER = 11
BASE = {"subjectId":"physiology","subjectTitle":"Physiology","chapterTitle":CHAPTER,"source":"ai","sourcePdf":"physiology 1.pdf","sourcePdfPageStart":541,"sourcePdfPageEnd":640,"chapterOrder":CHAPTER_ORDER,"imageUrls":[]}

def q(prompt, answer, wrong, explanation, clinical=False):
    return {"prompt":prompt,"options":[answer,*wrong],"answerIndex":0,"answer":answer,"explanation":explanation,"difficulty":"moderate","tags":["clinical"] if clinical else []}

TOPICS=[
("general-principles","General Principles of Endocrinal System",1,[
q("Which feature best defines an endocrine hormone?", "Chemical messenger released into blood to act on target cells", ["Enzyme acting only inside the same cell","Neurotransmitter released only at motor end plate","Digestive juice secreted into a duct"], "Endocrine hormones enter blood and act on cells with appropriate receptors."),
q("Peptide hormones usually act through which receptor location?", "Cell membrane receptors", ["Nuclear DNA only","Mitochondrial ribosomes","Red cell membrane antigens"], "Peptides are water-soluble and generally signal through membrane receptors."),
q("Steroid hormones usually produce effects by binding receptors in which location?", "Cytoplasm or nucleus", ["Synaptic cleft only","Lysosomal lumen","Bile canaliculus"], "Steroids are lipid-soluble and regulate gene transcription through intracellular receptors."),
q("A patient with a receptor mutation has high hormone levels but poor tissue response. Which mechanism explains this?", "Target-cell hormone resistance", ["Excess hormone clearance only","Improved feedback inhibition","Increased renal filtration"], "Hormone resistance can cause high circulating hormone with reduced biological effect.", True),
q("Negative feedback in endocrine systems primarily helps maintain what?", "Hormone levels within a physiological range", ["Permanent maximal secretion","Blood clotting only","Alveolar ventilation"], "Negative feedback stabilizes hormone secretion."),
q("Second messengers such as cAMP are commonly used by which hormone group?", "Peptide and catecholamine hormones", ["Most steroid hormones","Thyroid hormones only","Bile salts"], "Many membrane receptor hormones act through second messengers."),
q("Permissive action of a hormone means it does what?", "Allows another hormone to exert full effect", ["Destroys all receptors","Acts only in urine","Blocks gene transcription always"], "Some hormones prepare tissues for responses to other hormones."),
q("A patient on long-term steroid therapy develops adrenal suppression. Which feedback pathway is responsible?", "Suppression of ACTH by glucocorticoid negative feedback", ["Increased TSH release","Increased insulin release","Loss of ADH action"], "Exogenous glucocorticoids suppress CRH-ACTH drive.", True),
q("Hormones secreted in pulses are best assessed clinically by considering what?", "Timing and dynamic testing", ["Only a single random value always","Blood group","Pulse pressure"], "Pulsatile secretion may require timed or stimulation/suppression tests."),
q("A pituitary stimulation test is useful when basal hormone level is unclear because it assesses what?", "Reserve capacity of an endocrine axis", ["Lung compliance","Renal plasma flow","Platelet function"], "Dynamic tests evaluate the ability of glands to respond.", True),
]),
("hypothalamus-pituitary","Endocrinal Functions of Hypothalamus and Pituitary Gland",2,[
q("Which hypothalamic hormone stimulates TSH release?", "TRH", ["GnRH","Dopamine","Somatostatin"], "TRH stimulates thyrotrophs to secrete TSH."),
q("Dopamine from hypothalamus mainly inhibits which anterior pituitary hormone?", "Prolactin", ["ACTH","LH","TSH only"], "Dopamine is prolactin-inhibiting hormone."),
q("Growth hormone acts directly and through which mediator?", "IGF-1", ["Calcitonin","Aldosterone","Secretin"], "GH stimulates hepatic and tissue IGF-1 production."),
q("A child with pituitary GH deficiency presents with short stature. Which hormone axis is primarily affected?", "Growth hormone-IGF-1 axis", ["Renin-angiotensin axis","ADH-aquaporin axis only","Gastrin-acid axis"], "GH deficiency reduces IGF-1 and linear growth.", True),
q("ACTH primarily stimulates which endocrine gland?", "Adrenal cortex", ["Adrenal medulla only","Thyroid C cells","Pancreatic alpha cells"], "ACTH maintains cortisol secretion from adrenal cortex."),
q("Posterior pituitary releases ADH and which other hormone?", "Oxytocin", ["TSH","Gastrin","PTH"], "ADH and oxytocin are synthesized in hypothalamus and released from posterior pituitary."),
q("ADH mainly increases water reabsorption in which renal segment?", "Collecting duct", ["Glomerulus","Proximal convoluted tubule only","Urethra"], "ADH inserts aquaporins in collecting duct principal cells."),
q("A patient with polyuria and polydipsia improves after desmopressin. Which disorder is most likely?", "Central diabetes insipidus", ["SIADH","Primary hyperaldosteronism","Cushing syndrome"], "Response to ADH analog suggests deficient ADH secretion.", True),
q("Oxytocin is important for milk ejection by acting on which cells?", "Myoepithelial cells of breast", ["Chief cells of stomach","Thyroid follicular cells","Adrenal zona glomerulosa"], "Oxytocin contracts mammary myoepithelial cells."),
q("A pituitary adenoma causing bitemporal hemianopia compresses which nearby structure?", "Optic chiasma", ["Medulla oblongata","Cerebellar vermis","Spinal cord"], "Pituitary masses can compress the optic chiasma.", True),
]),
("thyroid-gland","Thyroid Gland",3,[
q("Thyroid hormones are synthesized from iodine and which amino acid?", "Tyrosine", ["Tryptophan","Glycine","Histidine"], "Iodinated tyrosyl residues form T3 and T4."),
q("TSH mainly stimulates which thyroid cell?", "Follicular cell", ["Parafollicular C cell","Adrenal chromaffin cell","Pancreatic beta cell"], "TSH acts on follicular cells to increase thyroid hormone synthesis and release."),
q("Most circulating thyroid hormone is secreted as which form?", "T4", ["T3 only","Reverse T3 only","Calcitonin"], "The thyroid secretes more T4, which is converted peripherally to T3."),
q("A patient with weight loss, tremor and heat intolerance most likely has excess of which hormones?", "T3 and T4", ["PTH and calcitonin","Insulin only","Aldosterone only"], "Thyrotoxicosis increases metabolic rate and adrenergic sensitivity.", True),
q("Thyroid hormone increases basal metabolic rate mainly by affecting what?", "Cellular oxidative metabolism", ["RBC agglutination","Bile storage","Urine acidification only"], "Thyroid hormone increases oxygen consumption and heat production."),
q("Iodide trapping in thyroid follicular cells is mediated by which transporter?", "Sodium-iodide symporter", ["SGLT1","Aquaporin-2","CFTR"], "NIS transports iodide into follicular cells with sodium."),
q("Calcitonin is secreted by which thyroid cells?", "Parafollicular C cells", ["Follicular cells","Chief cells","G cells"], "C cells secrete calcitonin."),
q("A patient with primary hypothyroidism typically shows which TSH pattern?", "High TSH", ["Low TSH always","Absent TSH with high T4","No change in TSH"], "Loss of thyroid feedback raises pituitary TSH secretion.", True),
q("Graves disease causes hyperthyroidism through antibodies that stimulate which receptor?", "TSH receptor", ["Insulin receptor","ACTH receptor","PTH receptor"], "TSH receptor-stimulating antibodies drive thyroid hormone production."),
q("Neonatal hypothyroidism must be treated early to prevent which complication?", "Impaired brain development", ["Renal stones","Pulmonary edema","Peptic ulcer"], "Thyroid hormone is essential for normal CNS development.", True),
]),
("calcium-bone","Endocrinal Control of Calcium Metabolism and Bone Physiology",4,[
q("Parathyroid hormone is secreted in response to low plasma level of which ion?", "Calcium", ["Sodium","Chloride","Iron"], "Low ionized calcium stimulates PTH secretion."),
q("PTH increases plasma calcium partly by increasing which renal process?", "Calcium reabsorption", ["Glucose filtration","Protein excretion","Bile salt recycling"], "PTH increases distal tubular calcium reabsorption."),
q("Vitamin D increases intestinal absorption of calcium and which ion?", "Phosphate", ["Chloride only","Hydrogen ion","Bilirubin"], "Calcitriol promotes absorption of calcium and phosphate."),
q("A patient with chronic kidney disease develops hypocalcaemia and high PTH. Which disorder is this?", "Secondary hyperparathyroidism", ["Central diabetes insipidus","Primary hyperthyroidism","Conn syndrome"], "Renal failure reduces calcitriol and phosphate excretion, stimulating PTH.", True),
q("Calcitonin generally lowers plasma calcium mainly by inhibiting which cells?", "Osteoclasts", ["Beta cells","Chief cells","Follicular cells"], "Calcitonin inhibits bone resorption by osteoclasts."),
q("Bone remodeling depends on coordinated action of osteoblasts and which cells?", "Osteoclasts", ["Enterocytes","Parietal cells","Chromaffin cells"], "Osteoblasts form bone and osteoclasts resorb bone."),
q("Active vitamin D is formed finally in which organ?", "Kidney", ["Stomach","Spleen","Colon"], "The kidney converts 25-hydroxyvitamin D to calcitriol."),
q("A child with vitamin D deficiency develops bowed legs. Which condition is this?", "Rickets", ["Tetany from hypercalcaemia","Cretinism","Acromegaly"], "Vitamin D deficiency in children causes defective mineralization and rickets.", True),
q("PTH decreases renal reabsorption of which ion?", "Phosphate", ["Calcium","Magnesium always","Sodium always"], "PTH promotes phosphaturia."),
q("Post-thyroidectomy tingling and carpopedal spasm most likely result from low levels of which hormone?", "PTH", ["Insulin","ADH","Gastrin"], "Accidental parathyroid removal causes hypocalcaemic tetany.", True),
]),
("adrenal-glands","Adrenal Glands",5,[
q("Aldosterone is secreted from which adrenal cortical zone?", "Zona glomerulosa", ["Zona fasciculata","Zona reticularis","Adrenal medulla"], "Zona glomerulosa produces mineralocorticoids."),
q("Cortisol is secreted mainly from which zone?", "Zona fasciculata", ["Zona glomerulosa","Adrenal medulla","Pancreatic islets"], "Zona fasciculata produces glucocorticoids."),
q("Adrenal medulla secretes mainly which hormones?", "Catecholamines", ["Thyroid hormones","Bile salts","PTH"], "Chromaffin cells secrete adrenaline and noradrenaline."),
q("A patient with hyperpigmentation, hypotension and hyponatraemia has primary adrenal failure. Which hormone is high?", "ACTH", ["TSH only","Insulin","Calcitonin"], "Loss of cortisol feedback increases ACTH in Addison disease.", True),
q("Aldosterone increases sodium reabsorption mainly in which renal cells?", "Principal cells of distal nephron", ["Parietal cells","Chief cells","Kupffer cells"], "Aldosterone acts on principal cells to retain sodium and excrete potassium."),
q("Cortisol supports blood pressure partly by increasing vascular responsiveness to which agents?", "Catecholamines", ["Bile salts","Insulin only","Secretin"], "Glucocorticoids permit normal vascular response to catecholamines."),
q("ACTH secretion is regulated by which hypothalamic hormone?", "CRH", ["TRH","GnRH","GHRH only"], "CRH stimulates corticotroph ACTH release."),
q("A patient with Cushing syndrome has muscle wasting and hyperglycaemia due to excess of which hormone?", "Cortisol", ["Aldosterone only","Calcitonin","Oxytocin"], "Cortisol excess causes protein catabolism and insulin antagonism.", True),
q("Primary hyperaldosteronism commonly causes hypertension with which electrolyte change?", "Hypokalaemia", ["Hyperkalaemia","Hypocalcaemia","Hyponatraemia only"], "Aldosterone excess promotes potassium loss."),
q("A pheochromocytoma causes episodic headache, sweating and palpitations by excess secretion of what?", "Catecholamines", ["PTH","ADH","Gastrin"], "Catecholamine surges produce paroxysmal adrenergic symptoms.", True),
]),
("pancreatic-gi-hormones","Pancreatic and Gastrointestinal Hormones",6,[
q("Insulin is secreted by which pancreatic islet cells?", "Beta cells", ["Alpha cells","Delta cells","PP cells"], "Beta cells secrete insulin."),
q("Glucagon is secreted by which islet cells?", "Alpha cells", ["Beta cells","Delta cells","Enterochromaffin-like cells"], "Alpha cells secrete glucagon."),
q("Insulin lowers blood glucose mainly by promoting what?", "Glucose uptake and storage", ["Glycogen breakdown only","Ketone formation only","Protein catabolism"], "Insulin promotes glucose uptake, glycogenesis and lipogenesis."),
q("A patient with type 1 diabetes develops ketoacidosis because of deficiency of which hormone?", "Insulin", ["Gastrin","Secretin","Calcitonin"], "Absolute insulin deficiency increases lipolysis and ketogenesis.", True),
q("Glucagon increases blood glucose by stimulating hepatic glycogenolysis and what?", "Gluconeogenesis", ["Glycolysis in RBCs only","Bile secretion","Calcium reabsorption"], "Glucagon promotes hepatic glucose output."),
q("Somatostatin from pancreatic delta cells generally has what endocrine effect?", "Inhibits insulin and glucagon secretion", ["Stimulates only insulin","Destroys beta cells","Acts as bile salt"], "Somatostatin inhibits several endocrine and GI secretions."),
q("Gastrin mainly stimulates secretion of which gastric product?", "Hydrochloric acid", ["Bile salts","Insulin","ADH"], "Gastrin increases acid secretion by parietal cells."),
q("A patient with fasting hypoglycaemia, sweating and confusion may have excess secretion from which tumor?", "Insulinoma", ["Gastrinoma","Pheochromocytoma","Prolactinoma"], "Insulinoma causes inappropriate insulin release and hypoglycaemia.", True),
q("Secretin is released in response to duodenal acid and stimulates which secretion?", "Pancreatic bicarbonate", ["Gastric pepsin only","Aldosterone","Thyroxine"], "Secretin neutralizes duodenal acid by stimulating bicarbonate."),
q("A gastrinoma causes recurrent peptic ulcers through excess secretion of which hormone?", "Gastrin", ["CCK","Insulin","Somatostatin"], "Excess gastrin causes marked acid hypersecretion.", True),
]),
("other-organs-local-hormones","Endocrinal Functions of Other Organs and Local Hormones",7,[
q("Erythropoietin is secreted mainly by which organ?", "Kidney", ["Stomach","Thyroid","Adrenal medulla"], "Renal peritubular cells produce erythropoietin in response to hypoxia."),
q("Atrial natriuretic peptide is released mainly from which chamber tissue?", "Atrial myocardium", ["Gastric mucosa","Adrenal cortex","Pancreatic duct"], "Atrial stretch stimulates ANP release."),
q("Leptin is secreted primarily by which tissue?", "Adipose tissue", ["Bone marrow only","Thyroid follicle","Gastric parietal cell"], "Adipocytes secrete leptin to signal energy stores."),
q("A patient with chronic kidney disease develops anaemia partly because of reduced secretion of which hormone?", "Erythropoietin", ["Gastrin","Oxytocin","Calcitonin"], "Low renal EPO reduces marrow RBC production.", True),
q("Renin is released by juxtaglomerular cells and begins formation of which hormone system?", "Angiotensin-aldosterone system", ["Thyroid hormone system","Insulin-glucagon system","Gastrin-secretin system"], "Renin starts RAAS activation."),
q("Prostaglandins are examples of which type of signalling molecule?", "Local hormones", ["Classical pituitary tropins only","Plasma proteins","Digestive enzymes"], "Prostaglandins usually act near their site of production."),
q("Placenta produces which hormone to maintain corpus luteum early in pregnancy?", "Human chorionic gonadotropin", ["TSH only","ACTH only","Calcitonin"], "hCG supports corpus luteum progesterone secretion early in pregnancy."),
q("A patient taking NSAIDs may develop gastric irritation because prostaglandin synthesis is reduced. Which protective action is lost?", "Mucus and bicarbonate support", ["TSH stimulation","Insulin secretion","EPO release"], "Gastric prostaglandins maintain mucosal protection.", True),
q("Calcitriol can be considered an endocrine product of which organ?", "Kidney", ["Colon","Spleen","Oesophagus"], "Kidney produces active vitamin D, which acts hormonally."),
q("Excess ANP would be expected to promote which renal response?", "Natriuresis", ["Sodium retention","Potassium retention always","Water deprivation"], "ANP promotes sodium excretion and opposes volume expansion.", True),
]),
]

def build():
    out=[]
    for slug,topic,order,rows in TOPICS:
        for i,row in enumerate(rows,1):
            shift=(order+i)%4
            opts=row["options"][shift:]+row["options"][:shift]
            ans=row["answer"]
            out.append({**BASE,**row,"id":f"physiology-endocrinal-{slug}-{i:02d}","topic":topic,"topicTitle":topic,"topicOrder":order,"options":opts,"answerIndex":opts.index(ans),"answer":ans})
    return out

def validate(qs):
    if len(qs)!=70: raise ValueError(f"Expected 70, got {len(qs)}")
    if len({q["id"] for q in qs})!=70: raise ValueError("Duplicate IDs")
    for _,topic,_,_ in TOPICS:
        t=[q for q in qs if q["topic"]==topic]
        if len(t)!=10 or sum("clinical" in q.get("tags",[]) for q in t)<3: raise ValueError(topic)
    for qn in qs:
        if qn["answer"]!=qn["options"][qn["answerIndex"]]: raise ValueError(qn["id"])

def update(path,qs):
    data=json.loads(path.read_text(encoding="utf-8-sig"))
    ids={q["id"] for q in qs}
    data["questions"]=[q for q in data.get("questions",[]) if q.get("id") not in ids]+qs
    data["questions"].sort(key=lambda q:q.get("id",""))
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def main():
    qs=build(); validate(qs)
    for p in DATA_PATHS:
        update(p,qs); print(f"Added {len(qs)} physiology questions to {p}.")
    for _,topic,_,_ in TOPICS: print(f"- {topic}: 10 questions")

if __name__=="__main__":
    main()
