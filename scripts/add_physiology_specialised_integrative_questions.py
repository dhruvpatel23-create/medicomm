import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Specialised Integrative Physiology"
CHAPTER_ORDER = 15
BASE = {"subjectId":"physiology","subjectTitle":"Physiology","chapterTitle":CHAPTER,"source":"ai","sourcePdf":"physiology 1.pdf","sourcePdfPageStart":961,"sourcePdfPageEnd":1020,"chapterOrder":CHAPTER_ORDER,"imageUrls":[]}

def q(prompt, answer, wrong, explanation, clinical=False):
    return {"prompt":prompt,"options":[answer,*wrong],"answerIndex":0,"answer":answer,"explanation":explanation,"difficulty":"moderate","tags":["clinical"] if clinical else []}

TOPICS=[
("body-temperature-regulation","Physiology of Body Temperature Regulation",1,[
q("The main integrating centre for body temperature regulation is located in which structure?", "Hypothalamus", ["Cerebellum","Medulla respiratory centre","Basal ganglia"], "Hypothalamic thermoregulatory centres integrate core and skin temperature inputs."),
q("Heat loss from skin occurs mainly through radiation, conduction, convection and what?", "Evaporation", ["Glycogenolysis","Filtration","Osmosis only"], "Evaporation of sweat is a major heat-loss mechanism, especially in heat."),
q("Shivering increases body temperature mainly by increasing what?", "Skeletal muscle heat production", ["Renal filtration","Bile flow","CSF absorption"], "Involuntary skeletal muscle contractions produce heat."),
q("A marathon runner collapses with hot dry skin and confusion. Which condition is most likely?", "Heat stroke", ["Simple faint without hyperthermia","Hypothyroidism","Addison disease"], "Heat stroke is severe hyperthermia with CNS dysfunction and failed heat dissipation.", True),
q("Sweating promotes heat loss most effectively when sweat can do what?", "Evaporate from skin", ["Remain pooled on skin","Enter blood directly","Turn into sebum"], "Evaporation removes latent heat from the body surface."),
q("Cutaneous vasodilation during heat exposure helps by increasing what?", "Heat transfer to skin", ["Bone formation","Gastric acid secretion","Urine acidification"], "Skin vasodilation increases heat delivery to body surface."),
q("Fever differs from hyperthermia because fever involves what?", "Raised hypothalamic set point", ["Loss of all hypothalamic function","Absent cytokines","Low prostaglandins always"], "Pyrogens raise the hypothalamic set point, producing fever."),
q("A child with fever improves after paracetamol because it reduces synthesis of which mediator?", "Prostaglandin E2", ["Aldosterone","Insulin","Bile salts"], "Antipyretics reduce PGE2-mediated hypothalamic set-point elevation.", True),
q("Cold exposure causes piloerection and skin vasoconstriction mainly through which system?", "Sympathetic nervous system", ["Parasympathetic sacral outflow only","Somatic sensory system only","Enteric nervous system"], "Sympathetic responses conserve heat and produce piloerection."),
q("An elderly person in winter develops confusion with low core temperature. Which thermoregulatory failure is present?", "Hypothermia", ["Fever","Heat cramps","Thyrotoxicosis only"], "Hypothermia causes CNS depression and can occur with impaired heat production/conservation.", True),
]),
("growth-behavioural-development","Physiology of Growth and Behavioural Development",2,[
q("Linear growth in children depends strongly on growth hormone and which mediator?", "IGF-1", ["Calcitonin","Secretin","ADH"], "GH stimulates IGF-1, which promotes epiphyseal growth."),
q("Thyroid hormone is essential in childhood for normal development of which system?", "Central nervous system", ["Bile duct system only","Adult dentition only","Platelet plug"], "Thyroid hormone is crucial for brain maturation and growth."),
q("Pubertal growth spurt is influenced importantly by growth hormone and which hormone group?", "Sex steroids", ["Bile salts","Gastrin only","Erythropoietin only"], "Sex steroids contribute to pubertal growth and epiphyseal maturation."),
q("A child with untreated congenital hypothyroidism is at risk of impaired growth and which major deficit?", "Intellectual disability", ["Polycythaemia only","Pulmonary fibrosis","Nephrotic syndrome"], "Early thyroid deficiency can cause irreversible neurodevelopmental impairment.", True),
q("Growth velocity is usually fastest during which postnatal period?", "Infancy", ["Late adulthood","Middle age","After epiphyseal closure"], "Postnatal growth rate is greatest in infancy and again rises at puberty."),
q("Epiphyseal plate closure is promoted mainly by which hormones?", "Oestrogens", ["ADH","Calcitonin only","Gastrin"], "Oestrogen mediates epiphyseal closure in both sexes."),
q("Behavioural development depends on maturation of nervous system and what?", "Environmental stimulation and learning", ["Only renal growth","Only bile secretion","Only blood group"], "Development reflects biological maturation plus experience."),
q("A teenager with delayed puberty and eunuchoid proportions likely has delayed closure of which structure?", "Epiphyseal plates", ["Fontanelles only","Cranial sutures only","Neuromuscular junction"], "Low sex steroids delay epiphyseal closure and prolong limb growth.", True),
q("Protein-energy malnutrition impairs growth mainly by limiting what?", "Substrate for tissue synthesis", ["Visual refraction","CSF pressure","Auditory transduction"], "Growth requires adequate calories, protein and micronutrients."),
q("A child with chronic glucocorticoid excess has poor linear growth because cortisol antagonizes which process?", "Protein synthesis and growth hormone action", ["Sweat evaporation","Pupillary reflex","Taste sensation"], "Excess glucocorticoids inhibit growth and protein accretion.", True),
]),
("fetus-neonate-childhood","Physiology of Fetus, Neonate and Childhood",3,[
q("Fetal oxygenation occurs through which organ?", "Placenta", ["Fetal lungs","Fetal kidney","Fetal liver only"], "The placenta mediates fetal gas exchange."),
q("Fetal haemoglobin has higher affinity for oxygen than adult haemoglobin because it binds 2,3-BPG how?", "Less avidly", ["More avidly","Irreversibly","Not at all with oxygen"], "Reduced 2,3-BPG binding shifts fetal Hb oxygen curve left."),
q("At birth, the first breaths help reduce which vascular resistance?", "Pulmonary vascular resistance", ["Systemic vascular resistance to zero","Portal resistance only","Renal tubular resistance"], "Lung expansion and oxygenation lower pulmonary resistance."),
q("A preterm neonate develops respiratory distress due to deficiency of which substance?", "Surfactant", ["Intrinsic factor","Bile salt","Aldosterone"], "Immature type II pneumocytes may produce insufficient surfactant.", True),
q("Closure of ductus arteriosus after birth is promoted by increased oxygen and reduced what?", "Prostaglandins", ["Calcium","Thyroxine","Insulin"], "Falling prostaglandins and rising oxygen favor ductal closure."),
q("Newborns are prone to heat loss partly because they have a high ratio of what?", "Surface area to body weight", ["Haemoglobin to oxygen","Bone to muscle only","Bile to plasma"], "Large surface area relative to mass increases heat loss."),
q("Brown adipose tissue helps neonates produce heat by which mechanism?", "Non-shivering thermogenesis", ["Sweat evaporation","Voluntary exercise","CSF circulation"], "Brown fat generates heat via uncoupled oxidative metabolism."),
q("A newborn with central cyanosis that improves with oxygen likely has a problem involving which system?", "Cardiopulmonary transition", ["Taste buds","Micturition reflex only","Lens accommodation"], "Persistent cyanosis suggests impaired neonatal oxygenation or circulatory transition.", True),
q("Breast milk provides passive immunity mainly through which immunoglobulin?", "Secretory IgA", ["IgE only","IgD only","IgM only"], "Secretory IgA protects mucosal surfaces in infants."),
q("A neonate has jaundice in the first week because bilirubin conjugating capacity is immature. Which enzyme system is limited?", "UDP-glucuronyl transferase", ["Acetylcholinesterase","Carbonic anhydrase only","5-alpha reductase"], "Immature hepatic conjugation contributes to physiological neonatal jaundice.", True),
]),
("geriatric-physiology","Geriatric Physiology",4,[
q("Ageing is generally associated with a decline in maximal capacity of which system?", "Multiple organ systems", ["Only hair follicles","Only taste buds","Only bile ducts"], "Physiological reserve declines across many systems with age."),
q("Total body water tends to do what with ageing?", "Decrease", ["Increase markedly","Remain identical in all persons","Become zero"], "Older adults generally have lower lean mass and total body water."),
q("Basal metabolic rate in older adults usually changes in which direction?", "Decreases", ["Increases sharply","Becomes identical to infancy","Is unrelated to lean mass"], "Loss of lean mass contributes to lower basal metabolic rate."),
q("An elderly patient becomes confused during dehydration more easily because ageing reduces which reserve?", "Homeostatic reserve for fluid balance", ["Visual pigment only","Taste receptor count only","Hair growth"], "Reduced thirst, renal concentrating ability and reserve increase dehydration risk.", True),
q("Renal ageing commonly reduces which functional measure?", "Glomerular filtration rate", ["ABO antigen expression","Auditory ossicle number","Gastric pH to zero"], "GFR tends to decline with age."),
q("Baroreceptor sensitivity with ageing generally does what?", "Decreases", ["Increases to infinity","Remains perfect","Stops heart sounds"], "Reduced baroreflex sensitivity predisposes to orthostatic hypotension."),
q("Bone loss in ageing is influenced strongly by reduced sex steroids and reduced what?", "Bone formation relative to resorption", ["CSF production","Taste bud turnover only","Air conduction"], "Ageing shifts bone remodeling toward net loss."),
q("An older person feels dizzy on standing after antihypertensive therapy. Which age-related change contributes?", "Reduced baroreflex compensation", ["Increased retinal cones","Increased renal reserve","Increased surfactant"], "Impaired baroreflexes make orthostatic hypotension more likely.", True),
q("Presbyopia occurs due to age-related reduction in what?", "Lens elasticity", ["Corneal blood supply","Retinal rods only","Pupil pigment"], "Lens stiffening reduces accommodation for near vision."),
q("An elderly patient with high-frequency hearing loss most likely has which age-related condition?", "Presbycusis", ["Achalasia","Cretinism","Tetany"], "Presbycusis is age-related sensorineural hearing loss, often high-frequency.", True),
]),
]

def build():
    out=[]
    for slug,topic,order,rows in TOPICS:
        for i,row in enumerate(rows,1):
            shift=(order+i)%4
            opts=row["options"][shift:]+row["options"][:shift]
            ans=row["answer"]
            out.append({**BASE,**row,"id":f"physiology-specialised-integrative-{slug}-{i:02d}","topic":topic,"topicTitle":topic,"topicOrder":order,"options":opts,"answerIndex":opts.index(ans),"answer":ans})
    return out

def validate(qs):
    if len(qs)!=40: raise ValueError(f"Expected 40, got {len(qs)}")
    if len({q["id"] for q in qs})!=40: raise ValueError("Duplicate IDs")
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
