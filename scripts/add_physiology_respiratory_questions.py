import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Respiratory System"
CHAPTER_ORDER = 8
BASE = {"subjectId":"physiology","subjectTitle":"Physiology","chapterTitle":CHAPTER,"source":"ai","sourcePdf":"physiology 1.pdf","sourcePdfPageStart":303,"sourcePdfPageEnd":386,"chapterOrder":CHAPTER_ORDER,"imageUrls":[]}

def q(prompt, answer, wrong, explanation, clinical=False):
    return {"prompt":prompt,"options":[answer,*wrong],"answerIndex":0,"answer":answer,"explanation":explanation,"difficulty":"moderate","tags":["clinical"] if clinical else []}

TOPICS=[
("tract-structure","Respiratory Tract: Structure and Functions",1,[
q("The respiratory tract conducts air from atmosphere to:", "Alveoli", ["Pleural cavity","Pulmonary veins","Pericardium"], "Respiratory passages conduct air to respiratory parenchyma."),
q("The functional gas exchanging unit of lung is centered on:", "Alveolus", ["Trachea","Primary bronchus","Pleura"], "Alveoli form the main site of gas exchange."),
q("A premature baby develops respiratory distress due to poor alveolar stability. Which structure/function is most relevant?", "Alveolar surfactant system", ["Nasal hairs","Pleural fluid only","Bronchial cartilage"], "Surfactant stabilizes alveoli and reduces surface tension.", True),
q("Pleural cavity normally contains:", "Thin film of pleural fluid", ["Air at atmospheric pressure","Blood","Lymph nodes"], "Pleural fluid lubricates pleural surfaces."),
q("Non-respiratory functions of lung include:", "Defence and metabolic functions", ["Erythropoiesis only","Bile secretion","Urine concentration"], "Lungs have defense and metabolic roles beyond gas exchange."),
q("Cilia and mucus in conducting airways primarily help:", "Remove inhaled particles", ["Produce haemoglobin","Secrete bile","Form lymph"], "Mucociliary clearance protects lower airways."),
q("A smoker with impaired mucociliary clearance is prone to infection because loss of which defence is important?", "Mucus-ciliary removal of particles", ["ABO agglutination","Cardiac output","Renal filtration"], "Airway defense depends heavily on mucus and ciliary movement.", True),
q("Pulmonary blood supply participates mainly in:", "Gas exchange", ["Protein digestion","ECG recording","Bile storage"], "Pulmonary circulation brings venous blood for oxygenation."),
q("Alveolar macrophages are important in:", "Lung defence", ["Valve closure","RBC formation","Gastric acid secretion"], "Alveolar macrophages help remove particles and microbes."),
q("A patient aspirates foreign material into bronchi. Which respiratory tract function first limits distal contamination?", "Conducting airway defence mechanisms", ["Oxygen-haemoglobin curve","Renin secretion","Platelet plug"], "Airway reflexes and mucociliary defense protect respiratory parenchyma.", True),
]),
("pulmonary-ventilation","Pulmonary Ventilation",2,[
q("Quiet inspiration is mainly an:", "Active process", ["Passive process","Coagulation process","Diffusion-only process"], "Inspiration requires contraction of inspiratory muscles."),
q("Quiet expiration is usually:", "Passive", ["Always active","Impossible without diaphragm contraction","Due to platelet action"], "Quiet expiration is mainly elastic recoil."),
q("The diaphragm contraction causes thoracic volume to:", "Increase", ["Decrease","Remain zero","Become pleural"], "Diaphragm contraction enlarges thoracic cavity."),
q("Intrapleural pressure during quiet breathing is normally:", "Negative", ["Positive","Zero always","Equal to arterial pressure"], "Pleural pressure remains subatmospheric."),
q("Tidal volume is the volume of air:", "Inspired or expired in quiet breath", ["Left after maximal expiration","In dead space only","In blood"], "TV is air moved with normal quiet breathing."),
q("A patient with restrictive lung disease has reduced lung compliance. What happens to work of breathing?", "It increases", ["It becomes zero","It affects only ECG","It improves ventilation"], "Low compliance makes lungs harder to inflate.", True),
q("Surfactant decreases:", "Alveolar surface tension", ["Airway diameter","Haemoglobin","Pleural fluid"], "Surfactant reduces surface tension and work of breathing."),
q("A premature neonate lacking surfactant has alveolar collapse because surface tension is:", "Increased", ["Decreased","Absent","Converted to oncotic pressure"], "Surfactant deficiency increases surface tension and atelectasis risk.", True),
q("FEV1/FVC is useful clinically for assessing:", "Airflow obstruction", ["ABO grouping","RBC fragility","Platelet count"], "Timed vital capacity helps detect obstructive defects.", True),
q("Minute ventilation equals:", "Tidal volume × respiratory rate", ["Vital capacity × BP","Dead space ÷ rate","Residual volume × Hb"], "Minute ventilation is total air breathed per minute."),
]),
("pulmonary-circulation","Pulmonary Circulation",3,[
q("Pulmonary circulation is characterized by:", "Low pressure and low resistance", ["High pressure like systemic","No blood volume","Only lymph"], "Pulmonary vessels normally operate at low pressure/resistance."),
q("Pulmonary artery carries:", "Deoxygenated blood", ["Oxygenated blood","Lymph","Air"], "Pulmonary artery carries venous blood to lungs."),
q("Pulmonary veins carry:", "Oxygenated blood", ["Deoxygenated blood","Air","Pleural fluid"], "Pulmonary veins return oxygenated blood to left atrium."),
q("Bronchial circulation mainly supplies:", "Conducting airways and lung tissues", ["Only alveolar air","Only RBCs","Only pleura"], "Bronchial vessels nourish lung tissue."),
q("Regional pulmonary blood flow is affected strongly by:", "Gravity", ["ABO group","ESR","Skin color"], "Gravity creates regional perfusion differences."),
q("In an upright person, perfusion is greatest at lung:", "Base", ["Apex","Trachea","Pleura only"], "Hydrostatic pressure makes basal perfusion greater.", True),
q("Pulmonary edema occurs when fluid accumulates in:", "Lung interstitium/alveoli", ["Pericardium only","Bone marrow","Liver sinusoids"], "Pulmonary edema impairs gas exchange by fluid accumulation.", True),
q("Pulmonary circulation can act as a blood:", "Reservoir", ["Coagulator","Pacemaker","Hormone gland only"], "Pulmonary blood volume contributes to blood reservoir function."),
q("Hypoxia in pulmonary vessels tends to cause:", "Vasoconstriction", ["Vasodilation always","No vascular effect","Platelet lysis"], "Alveolar hypoxia constricts pulmonary vessels, redistributing flow."),
q("A patient with localized alveolar hypoxia redirects blood away from poorly ventilated alveoli through:", "Hypoxic pulmonary vasoconstriction", ["Baroreceptor reflex","ABO reaction","Fibrinolysis"], "Pulmonary arterioles constrict in hypoxic regions to improve matching.", True),
]),
("pulmonary-diffusion","Pulmonary Diffusion",4,[
q("Gas diffusion across respiratory membrane follows:", "Partial pressure gradient", ["Blood group gradient","Platelet gradient","DNA gradient"], "Gases diffuse from higher to lower partial pressure."),
q("Alveolar ventilation is fresh air reaching:", "Alveoli", ["Dead space only","Pleural cavity","Pulmonary artery"], "Alveolar ventilation excludes dead-space ventilation."),
q("Anatomical dead space is air in:", "Conducting passages", ["Alveoli participating in exchange","Blood","Lymph"], "Conducting airways contain air not used for exchange."),
q("VA/Q ratio means:", "Ventilation-perfusion ratio", ["Vital-air quotient","Venous-aortic quotient","Volume-albumin quotient"], "VA/Q expresses alveolar ventilation relative to perfusion."),
q("Low VA/Q units cause:", "Impaired oxygenation", ["Improved oxygenation always","ABO reaction","High ESR"], "Poor ventilation relative to perfusion lowers oxygen uptake."),
q("A pulmonary embolus creates alveoli that are ventilated but not perfused, increasing:", "Physiological dead space", ["RBC count","Albumin","Tidal volume always"], "Embolism creates wasted ventilation.", True),
q("Diffusion capacity of lung is measured commonly using:", "Carbon monoxide", ["Nitrogen only","Helium only","Oxygen toxicity"], "CO uptake is used because it is diffusion-limited."),
q("Thickening of respiratory membrane in pulmonary fibrosis reduces:", "Diffusion capacity", ["ABO antigens","Heart sounds","Platelets"], "Increased thickness impairs gas diffusion.", True),
q("Oxygen diffuses from alveoli into blood because alveolar PO2 is:", "Higher than venous blood PO2", ["Lower than venous PO2","Zero","Equal always"], "O2 moves down its partial pressure gradient."),
q("At high altitude, reduced inspired PO2 primarily lowers:", "Alveolar PO2", ["ABO titre","Fibrinogen","Platelet adhesiveness"], "Lower barometric pressure lowers alveolar oxygen tension.", True),
]),
("transport-gases","Transport of Gases",5,[
q("Most oxygen in blood is transported:", "Combined with haemoglobin", ["Dissolved in plasma only","As bicarbonate","As carbamino compound"], "O2 is transported mainly as oxyhaemoglobin."),
q("Oxygen carrying capacity depends mainly on:", "Haemoglobin concentration", ["Platelet count","Albumin only","Blood group"], "Hb amount determines O2 carrying capacity."),
q("Right shift of O2-Hb curve promotes:", "Oxygen unloading in tissues", ["Oxygen loading only","CO2 abolition","No tissue effect"], "Right shift lowers affinity and aids unloading."),
q("Exercise shifts O2-Hb curve right due to increased CO2, H+ and:", "Temperature", ["Albumin","Platelets","ABO antibodies"], "Exercise raises temperature/CO2/H+, promoting unloading.", True),
q("Carbon monoxide poisoning reduces O2 transport by binding:", "Haemoglobin", ["Albumin","Fibrinogen","Surfactant"], "CO binds Hb with high affinity, reducing oxygen carriage.", True),
q("Most CO2 is transported as:", "Bicarbonate", ["Dissolved oxygen","Oxyhaemoglobin","Nitrogen"], "CO2 is carried mainly as bicarbonate in plasma."),
q("Carbonic anhydrase in RBCs facilitates formation of:", "Carbonic acid/bicarbonate", ["Fibrin","Surfactant","Oxyhaemoglobin only"], "Carbonic anhydrase speeds CO2 hydration."),
q("Chloride shift occurs during:", "CO2 transport", ["ABO grouping","Platelet adhesion","ECG recording"], "Chloride enters RBCs as bicarbonate leaves."),
q("A patient with severe anaemia has reduced oxygen content despite normal PO2 because of low:", "Haemoglobin", ["Plasma sodium","CO2","Dead space"], "Oxygen content depends strongly on Hb.", True),
q("Respiratory quotient is ratio of:", "CO2 produced to O2 consumed", ["O2 consumed to Hb","Tidal volume to dead space","BP to flow"], "RQ = CO2 output/O2 uptake."),
]),
("regulation-respiration","Regulation of Respiration",6,[
q("Basic respiratory rhythm is generated mainly in:", "Medulla", ["Cerebellum","Kidney","Spleen"], "Medullary respiratory centres generate automatic rhythm."),
q("Dorsal respiratory group is mainly associated with:", "Inspiration", ["Expiration only","Blood grouping","Coagulation"], "DRG neurons are primarily inspiratory."),
q("Pneumotaxic centre is located in:", "Pons", ["Spinal cord","Liver","Atria"], "Pontine centres modulate respiration."),
q("Hering-Breuer reflex is mediated by:", "Pulmonary stretch receptors", ["Carotid chemoreceptors","RBCs","Platelets"], "Stretch receptors limit inspiration when lungs inflate."),
q("Most powerful chemical regulator of ventilation is usually:", "CO2/H+ via central chemoreceptors", ["Oxygen at all levels","Albumin","Glucose"], "CO2 alters CSF H+ and strongly drives breathing."),
q("Peripheral chemoreceptors are located in carotid and:", "Aortic bodies", ["SA node","Spleen","Alveoli only"], "Peripheral chemoreceptors are in carotid and aortic bodies."),
q("A COPD patient retaining CO2 depends more on hypoxic drive. Excess oxygen may reduce:", "Ventilatory drive", ["ABO antigen","RBC lifespan","Pleural fluid"], "Chronic CO2 retainers may rely more on hypoxic stimulation.", True),
q("Hyperventilation acutely lowers arterial:", "CO2", ["O2 carrying capacity","Haemoglobin","Blood group"], "Hyperventilation blows off CO2."),
q("Anxiety-induced hyperventilation can cause dizziness due to hypocapnia and:", "Cerebral vasoconstriction", ["Cerebral vasodilation","Haemolysis","Pulmonary edema only"], "Low CO2 constricts cerebral vessels.", True),
q("Severe metabolic acidosis stimulates ventilation mainly through:", "Increased H+ effect on chemoreceptors", ["ABO reaction","Surfactant release only","Platelet plug"], "Acidosis increases respiratory drive.", True),
]),
("respiration-applied","Respiration: Applied Aspects",7,[
q("Dyspnoea means:", "Difficult or laboured breathing", ["No breathing","Normal quiet breathing","High Hb"], "Dyspnoea is subjective breathing difficulty."),
q("Apnoea means:", "Cessation of breathing", ["Rapid breathing","Deep breathing","Cough"], "Apnoea is absence of breathing."),
q("Cheyne-Stokes respiration is:", "Periodic waxing and waning breathing with apnoea", ["Always normal exercise breathing","Single cough","Pleural rub"], "It is periodic breathing with cycles of apnea."),
q("Hypoxia means deficiency of:", "Oxygen at tissue level", ["CO2 only","Nitrogen","Albumin"], "Hypoxia is inadequate tissue oxygen."),
q("Cyanosis is bluish discoloration due to increased:", "Deoxygenated haemoglobin", ["Albumin","Platelets","Fibrin"], "Cyanosis occurs when reduced Hb is increased.", True),
q("Carbon monoxide poisoning causes tissue hypoxia because CO:", "Binds haemoglobin strongly", ["Destroys surfactant only","Increases VA/Q","Raises O2 capacity"], "CO forms carboxyhaemoglobin and impairs O2 transport.", True),
q("High-altitude hypoxia is mainly due to reduced:", "Barometric pressure and inspired PO2", ["Haemoglobin affinity only","Blood group","Platelets"], "At altitude, low barometric pressure lowers inspired/alveolar PO2."),
q("Decompression sickness is due to bubbles of:", "Nitrogen", ["Oxygen","Carbon dioxide","Helium always"], "Rapid ascent releases dissolved nitrogen bubbles."),
q("CPR is used during:", "Cardiorespiratory arrest", ["Normal sleep","Mild fever","ABO typing"], "CPR supports circulation and ventilation in arrest.", True),
q("Spirometry is used to assess:", "Pulmonary function", ["Blood group","ECG axis","Platelet count"], "Spirometry measures lung volumes/capacities and ventilatory function."),
]),
("exercise-physiology","Physiology of Exercise",8,[
q("During exercise, oxygen consumption:", "Increases", ["Falls to zero","Does not change","Becomes BP"], "Exercise raises metabolic O2 demand."),
q("Oxygen debt is related to:", "Recovery oxygen consumption after exercise", ["ABO antibodies","Lung dead space only","Pleural pressure"], "Extra O2 is consumed post-exercise to restore stores."),
q("During exercise, cardiac output:", "Increases", ["Falls","Stops","Equals ESR"], "Exercise increases HR and stroke volume."),
q("Skeletal muscle blood flow during exercise:", "Increases greatly", ["Falls to zero","Is unchanged","Becomes lymph"], "Active muscle receives increased flow."),
q("Blood flow is redistributed during exercise toward:", "Active skeletal muscle", ["Resting gut only","Skin only always","Bone marrow only"], "Exercise redistributes CO to active muscle."),
q("A trained athlete has lower resting heart rate due to increased:", "Stroke volume and vagal tone", ["ABO antibodies","RBC fragility","Platelet plug"], "Training improves stroke volume and autonomic balance.", True),
q("Pulmonary ventilation during exercise:", "Increases", ["Ceases","Does not change","Equals residual volume"], "Ventilation rises to match metabolic demand."),
q("At onset of exercise, oxygen deficit occurs because:", "O2 demand rises before uptake fully matches it", ["O2 demand falls","Hb disappears","CO2 transport stops"], "There is lag before aerobic systems meet demand.", True),
q("Training increases maximal oxygen consumption mainly by improving:", "Cardiorespiratory capacity", ["Blood group","Coagulation time","Bilirubin"], "Training improves cardiovascular and respiratory performance."),
q("During dynamic exercise, systolic BP usually rises because:", "Cardiac output increases", ["ABO agglutination","ESR increases","Surfactant falls"], "Higher CO raises systolic pressure during exercise.", True),
]),
]

def build():
    out=[]
    for slug,topic,order,rows in TOPICS:
        for i,row in enumerate(rows,1):
            shift=(order+i)%4; opts=row["options"][shift:]+row["options"][:shift]; ans=row["answer"]
            out.append({**BASE,**row,"id":f"physiology-respiratory-{slug}-{i:02d}","topic":topic,"topicTitle":topic,"topicOrder":order,"options":opts,"answerIndex":opts.index(ans),"answer":ans})
    return out

def validate(qs):
    if len(qs)!=80: raise ValueError("Expected 80")
    if len({q["id"] for q in qs})!=80: raise ValueError("Duplicate ids")
    for _,topic,_,_ in TOPICS:
        t=[q for q in qs if q["topic"]==topic]
        if len(t)!=10 or sum("clinical" in q.get("tags",[]) for q in t)<3: raise ValueError(topic)
    for q in qs:
        if q["answer"] != q["options"][q["answerIndex"]]: raise ValueError(q["id"])

def update(path, qs):
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
