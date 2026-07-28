import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Cardiovascular System"
CHAPTER_ORDER = 7
SOURCE_PDF = "physiology 1.pdf"
SOURCE_PAGE_START = 185
SOURCE_PAGE_END = 302

BASE = {
    "subjectId": "physiology", "subjectTitle": "Physiology", "chapterTitle": CHAPTER,
    "source": "ai", "sourcePdf": SOURCE_PDF, "sourcePdfPageStart": SOURCE_PAGE_START,
    "sourcePdfPageEnd": SOURCE_PAGE_END, "chapterOrder": CHAPTER_ORDER, "imageUrls": [],
}

def q(prompt, answer, wrong, explanation, clinical=False):
    return {"prompt": prompt, "options": [answer, *wrong], "answerIndex": 0, "answer": answer,
            "explanation": explanation, "difficulty": "moderate", "tags": ["clinical"] if clinical else []}

TOPICS = [
("functional-anatomy-cardiac-muscle","Functional Anatomy of Heart and Physiology of Cardiac Muscle",1,[
q("Which layer forms the muscular wall of the heart?", "Myocardium", ["Endocardium","Pericardium","Epicardial fat"], "Myocardium is the cardiac muscle layer responsible for contraction."),
q("Which valves lie between atria and ventricles?", "Atrioventricular valves", ["Semilunar valves","Thebesian valves","Venous valves"], "Mitral and tricuspid valves are atrioventricular valves."),
q("A patient develops backflow from left ventricle to left atrium during systole. Which valve is incompetent?", "Mitral valve", ["Aortic valve","Pulmonary valve","Tricuspid valve"], "The mitral valve guards the left atrioventricular orifice.", True),
q("Cardiac muscle fibres are functionally connected mainly through:", "Intercalated discs", ["Nodes of Ranvier","Motor end plates","Dense bodies"], "Intercalated discs provide mechanical and electrical coupling."),
q("The resting membrane potential of ventricular cardiac muscle is about:", "-90 mV", ["-55 mV","+30 mV","0 mV"], "Ventricular cardiac muscle has a stable resting potential around -90 mV."),
q("The plateau phase of cardiac action potential is mainly important because it:", "Prolongs refractory period", ["Abolishes calcium entry","Causes tetanus","Prevents contraction"], "The plateau prolongs action potential and refractory period."),
q("A long refractory period in myocardium prevents:", "Tetanus", ["Autorhythmicity","Conduction","Excitation"], "Long refractory period prevents fused sustained contraction.", True),
q("Cardiac excitation-contraction coupling depends partly on:", "Extracellular calcium", ["Only intracellular sodium","Only chloride","DNA synthesis"], "Calcium entry triggers calcium-induced calcium release."),
q("All-or-none law in cardiac muscle applies to:", "Whole heart muscle", ["Each motor unit","Each RBC","Only SA node"], "Functional syncytium behavior makes the whole cardiac muscle respond as a unit."),
q("Increased venous return stretches cardiac fibres and increases force. This illustrates:", "Frank-Starling/length-tension relation", ["Re-entry","Fick principle","Korotkoff sounds"], "Preload increases fibre length and force within limits.", True),
]),
("impulse-ecg","Origin and Spread of Cardiac Impulse and Electrocardiography",2,[
q("Normal cardiac pacemaker is:", "SA node", ["AV node","Bundle of His","Purkinje fibre"], "SA node has the highest rhythmicity and initiates normal impulse."),
q("Impulse normally passes from atria to ventricles through:", "AV node", ["Aortic valve","Coronary sinus","Pericardium"], "AV node is the normal atrioventricular conduction pathway."),
q("A patient has complete AV block. Which structure's conduction is most relevant?", "AV node/His pathway", ["Mitral valve","Albumin","Coronary vein"], "Complete block interrupts atrioventricular impulse conduction.", True),
q("P wave of ECG represents:", "Atrial depolarization", ["Ventricular depolarization","Ventricular repolarization","Atrial repolarization only"], "P wave records atrial depolarization."),
q("QRS complex represents:", "Ventricular depolarization", ["Atrial depolarization","Ventricular filling","SA nodal delay"], "QRS is ventricular depolarization."),
q("T wave represents:", "Ventricular repolarization", ["Atrial contraction","Ventricular depolarization","Valve closure"], "T wave is ventricular repolarization."),
q("PR interval mainly reflects:", "Atrioventricular conduction time", ["Ventricular ejection","Pulse pressure","Stroke volume"], "PR interval includes AV nodal delay and atrioventricular conduction."),
q("ST elevation in a patient with chest pain suggests:", "Acute myocardial injury/infarction", ["Normal venous return","Physiological sinus arrhythmia","Low ESR"], "ST segment changes are clinically important in myocardial infarction.", True),
q("Sinus tachycardia means:", "Fast rhythm originating from SA node", ["AV dissociation","No P waves ever","Ventricular fibrillation"], "Sinus tachycardia is increased SA nodal rhythm."),
q("Hyperkalaemia changes cardiac electrical activity mainly by affecting:", "Membrane potential and excitability", ["Plasma oncotic pressure","RBC count","Lymph flow"], "Potassium level strongly influences cardiac membrane potential.", True),
]),
("pump-cycle-output","Heart as a Pump: Cardiac Cycle, Cardiac Output and Venous Return",3,[
q("First heart sound is mainly due to closure of:", "Atrioventricular valves", ["Semilunar valves","Coronary ostia","Venous valves"], "S1 occurs with closure of mitral and tricuspid valves."),
q("Second heart sound is mainly due to closure of:", "Semilunar valves", ["AV valves","Foramen ovale","Chordae only"], "S2 occurs with aortic and pulmonary valve closure."),
q("During isovolumic contraction, ventricular volume:", "Remains constant", ["Rapidly increases","Rapidly decreases","Becomes zero"], "All valves are closed, so pressure rises without volume change."),
q("Aortic valve opens when:", "Left ventricular pressure exceeds aortic pressure", ["Atrial pressure rises","Venous pressure falls","AV valves open"], "Ejection starts when ventricular pressure exceeds arterial pressure."),
q("Cardiac output equals:", "Heart rate × stroke volume", ["BP × ESR","TPR ÷ HR","EDV − HR"], "CO is HR multiplied by stroke volume."),
q("A patient with haemorrhage has low venous return and low stroke volume. Which mechanism is directly affected?", "Frank-Starling mechanism", ["ABO grouping","Hering-Breuer reflex","Rouleaux formation"], "Reduced venous return lowers EDV and stroke volume.", True),
q("Fick principle measures cardiac output using oxygen uptake and:", "Arteriovenous oxygen difference", ["ESR","ABO titre","Platelet count"], "Fick method uses uptake divided by A-V concentration difference."),
q("Third heart sound is associated with:", "Rapid ventricular filling", ["AV valve closure","Semilunar closure","Atrial depolarization"], "S3 occurs during rapid filling phase."),
q("Tachycardia reduces diastolic duration most, thereby reducing:", "Ventricular filling time", ["QRS amplitude only","RBC lifespan","Plasma protein synthesis"], "Diastole shortens disproportionately at high heart rates.", True),
q("In heart failure, raised venous pressure and reduced output reflect impaired:", "Pumping function of heart", ["ABO inheritance","Neutrophil chemotaxis","Lymphocyte activation"], "Heart failure is inadequate pump function.", True),
]),
("circulation-dynamics","Dynamics of Circulation: Pressure and Flow of Blood and Lymph",4,[
q("Blood flow is directly proportional to:", "Pressure gradient", ["Vessel length","Viscosity","Resistance"], "Flow rises with pressure difference."),
q("Blood flow is inversely proportional to:", "Resistance", ["Pressure gradient","Radius to fourth power","Cardiac output"], "Flow = pressure gradient/resistance."),
q("Poiseuille's law states flow varies with vessel radius to the:", "Fourth power", ["Second power","First power","Eighth power"], "Radius is the most powerful determinant of resistance."),
q("Small decrease in arteriolar radius causes large fall in flow because:", "Resistance rises sharply", ["Blood becomes plasma","Valves close","Lymph stops"], "Resistance varies inversely with radius to fourth power.", True),
q("Arterioles are called resistance vessels because they:", "Control peripheral resistance", ["Store all blood","Have no smooth muscle","Contain valves"], "Arterioles are major regulators of TPR and organ flow."),
q("Capillary exchange of water is governed mainly by:", "Starling forces", ["ECG vectors","SA node rate","ABO antibodies"], "Filtration and reabsorption depend on hydrostatic and oncotic pressures."),
q("Edema after lymphatic obstruction occurs because lymph normally:", "Returns excess interstitial fluid and proteins", ["Makes RBCs","Conducts impulses","Clots blood"], "Lymph drains filtered fluid/proteins from tissues.", True),
q("Mean arterial pressure is approximated by:", "Diastolic BP + one-third pulse pressure", ["Systolic BP only","Pulse pressure × HR","Venous pressure"], "MAP is DBP plus one-third pulse pressure at normal rates."),
q("Korotkoff sounds are used in measuring:", "Arterial blood pressure", ["Cardiac output by Fick","ESR","ECG axis"], "Indirect sphygmomanometry uses Korotkoff sounds."),
q("A patient with severe dehydration has hypotension mainly due to reduced:", "Blood volume and venous return", ["ABO antigens","T wave","Fibrinogen only"], "Volume depletion lowers venous return and arterial pressure.", True),
]),
("cardiovascular-regulation","Cardiovascular Regulation",5,[
q("Rapid regulation of arterial pressure is mainly by:", "Baroreceptor reflex", ["Erythropoiesis","Gene therapy","Osmotic fragility"], "Baroreceptor reflex provides rapid neural BP control."),
q("Carotid sinus baroreceptors respond chiefly to:", "Stretch from arterial pressure", ["Blood glucose","Plasma bilirubin","RBC shape"], "Baroreceptors are stretch receptors in arterial walls."),
q("Standing suddenly may cause transient fall in BP; baroreflex responds by:", "Increasing sympathetic activity", ["Stopping SA node permanently","Reducing venous tone","Destroying RBCs"], "Baroreflex increases sympathetic outflow and reduces vagal tone.", True),
q("Medullary vasomotor centre controls:", "Vascular tone and blood pressure", ["ABO grouping","Platelet formation","DNA replication"], "Vasomotor centre regulates sympathetic vasoconstrictor activity."),
q("Chemoreceptor reflex is stimulated by hypoxia, hypercapnia and:", "Acidosis", ["Alkaline tide only","High albumin","Low ESR"], "Chemoreceptors respond to low O2, high CO2 and H+." ),
q("Renin-angiotensin system raises BP mainly through angiotensin II causing:", "Vasoconstriction and aldosterone release", ["Vasodilation only","Haemolysis","Reduced sodium reabsorption"], "Angiotensin II constricts vessels and promotes salt-water retention."),
q("A patient with renal artery stenosis develops hypertension due to activation of:", "Renin-angiotensin system", ["ABO system","Fibrinolysis","ECG axis"], "Reduced renal perfusion increases renin release.", True),
q("Atrial natriuretic peptide generally promotes:", "Natriuresis and vasodilation", ["Sodium retention","Power stroke","Coagulation"], "ANP opposes volume overload by promoting sodium excretion."),
q("Local metabolic control of blood flow increases flow when tissue metabolism:", "Increases", ["Stops","Has no oxygen demand","Clots"], "Metabolites dilate local vessels to match blood flow to demand."),
q("During exercise, skeletal muscle blood flow rises mainly due to:", "Local metabolites and sympathetic adjustments", ["ABO antibodies","Bilirubin","Nissl bodies"], "Exercise hyperaemia depends on local metabolic vasodilation with cardiovascular regulation.", True),
]),
("regional-circulation","Regional Circulation",6,[
q("Coronary blood flow to left ventricle is least during:", "Systole", ["Diastole","Atrial filling","Sleep only"], "Left ventricular contraction compresses coronary vessels during systole."),
q("Coronary flow is regulated mainly by:", "Local metabolic factors", ["ABO antibodies","ESR","Platelet count"], "Myocardial metabolism tightly controls coronary flow."),
q("Angina pectoris occurs when:", "Myocardial oxygen demand exceeds coronary supply", ["RBCs swell in hypotonic fluid","Albumin rises","AV valves open"], "Angina reflects transient myocardial ischemia.", True),
q("Cerebral blood flow is strongly influenced by arterial:", "CO2 and H+ concentration", ["ABO group","Platelet count","Fibrinogen only"], "CO2/H+ are potent cerebral vasodilator stimuli."),
q("Raised intracranial pressure can reduce:", "Cerebral blood flow", ["ABO agglutination","RBC lifespan","Plasma viscosity only"], "High ICP opposes cerebral perfusion."),
q("Cutaneous circulation is important for:", "Temperature regulation", ["Bile formation","ECG recording","Haemoglobin synthesis"], "Skin blood flow helps heat loss/conservation."),
q("Blushing and pallor reflect changes in:", "Cutaneous blood flow", ["Coronary sinus flow","Renal filtration only","ABO antigens"], "Skin vessel tone changes produce visible color changes.", True),
q("Skeletal muscle blood flow increases during exercise mainly from:", "Metabolic vasodilation", ["Fibrin formation","Low lymph flow","High bilirubin"], "Active muscle metabolites dilate resistance vessels."),
q("Hepatic circulation is distinctive because liver receives blood from hepatic artery and:", "Portal vein", ["Pulmonary vein","Coronary sinus","Aorta only"], "Liver has dual inflow: portal vein and hepatic artery."),
q("Myocardial infarction results from severe reduction of:", "Coronary blood supply", ["Cutaneous flow","Lymph flow","Portal flow"], "MI is necrosis due to inadequate coronary perfusion.", True),
]),
("homeostasis-health-disease","Cardiovascular Homeostasis in Health and Disease",7,[
q("On standing, venous pooling initially reduces:", "Venous return", ["ABO antibodies","RBC lifespan","T wave only"], "Standing shifts blood to dependent veins and reduces venous return."),
q("Postural hypotension is failure to maintain BP during:", "Standing", ["Deep sleep","Blood grouping","Digestion only"], "Postural hypotension is BP fall on standing."),
q("An elderly patient feels dizzy after standing suddenly. The immediate problem is reduced:", "Cerebral blood flow", ["Plasma protein synthesis","Platelet adhesion","Rh antigen"], "Postural BP fall can transiently reduce cerebral perfusion.", True),
q("Valsalva manoeuvre involves forced expiration against:", "Closed glottis", ["Open mouth only","Contracted pupil","Relaxed diaphragm only"], "Valsalva raises intrathoracic pressure by straining against closed glottis."),
q("During muscular exercise, cardiac output:", "Increases", ["Falls to zero","Does not change","Becomes venous pressure"], "Exercise increases venous return, heart rate and contractility."),
q("Hypovolaemic shock is commonly due to:", "Loss of blood or fluid volume", ["Excess albumin","ABO inheritance","High platelet count"], "Hypovolaemic shock results from reduced circulating volume.", True),
q("Cardiogenic shock is due to failure of:", "Pump function of heart", ["Lymph nodes","RBC membrane","ABO antibodies"], "Cardiogenic shock results from inadequate cardiac pumping."),
q("In early non-progressive shock, rapid compensation is mainly:", "Neural sympathetic response", ["Gene amplification","Haemolysis","Osmosis only"], "Early shock triggers baroreflex/sympathetic compensation."),
q("Progressive shock worsens because of:", "Positive feedback cycles", ["Stable negative feedback","High albumin","Improved perfusion"], "Progressive shock involves self-worsening cycles of tissue ischemia."),
q("Treatment of shock with fluids primarily aims to restore:", "Circulating volume and venous return", ["ABO type","ECG paper speed","RBC shape"], "Volume replacement improves venous return and cardiac output in hypovolaemia.", True),
]),
]

def build_questions():
    qs=[]
    for slug, topic, order, rows in TOPICS:
        for i,row in enumerate(rows,1):
            shift=(order+i)%4; opts=row["options"][shift:]+row["options"][:shift]; ans=row["answer"]
            qs.append({**BASE, **row, "id":f"physiology-cardiovascular-{slug}-{i:02d}",
                       "topic":topic, "topicTitle":topic, "topicOrder":order,
                       "options":opts, "answerIndex":opts.index(ans), "answer":ans})
    return qs

def validate(qs):
    if len(qs)!=70: raise ValueError("Expected 70")
    if len({q["id"] for q in qs})!=70: raise ValueError("Duplicate ids")
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
    qs=build_questions(); validate(qs)
    for p in DATA_PATHS:
        update(p,qs); print(f"Added {len(qs)} physiology questions to {p}.")
    for _,topic,_,_ in TOPICS: print(f"- {topic}: 10 questions")

if __name__=="__main__": main()
