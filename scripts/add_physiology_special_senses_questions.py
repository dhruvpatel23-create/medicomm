import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Special Senses"
CHAPTER_ORDER = 14
BASE = {"subjectId":"physiology","subjectTitle":"Physiology","chapterTitle":CHAPTER,"source":"ai","sourcePdf":"physiology 1.pdf","sourcePdfPageStart":901,"sourcePdfPageEnd":960,"chapterOrder":CHAPTER_ORDER,"imageUrls":[]}

def q(prompt, answer, wrong, explanation, clinical=False):
    return {"prompt":prompt,"options":[answer,*wrong],"answerIndex":0,"answer":answer,"explanation":explanation,"difficulty":"moderate","tags":["clinical"] if clinical else []}

TOPICS=[
("vision","Sense of Vision",1,[
q("Which part of the eye provides the greatest refractive power?", "Cornea", ["Lens","Vitreous body","Retina"], "The cornea produces most refraction because of the air-cornea interface."),
q("Accommodation for near vision mainly requires contraction of which muscle?", "Ciliary muscle", ["Superior rectus","Orbicularis oculi","Dilator pupillae"], "Ciliary contraction relaxes zonules and makes the lens more convex."),
q("Rods are most important for which type of vision?", "Dim-light vision", ["Colour discrimination","High-acuity foveal vision only","Near reflex only"], "Rods are highly sensitive and function in scotopic vision."),
q("A patient with night blindness most likely has impaired function of which photoreceptor system?", "Rods", ["Cones only","Bipolar cells only","Ganglion cells only"], "Rod dysfunction or vitamin A deficiency can cause night blindness.", True),
q("Cones are concentrated maximally in which retinal region?", "Fovea centralis", ["Optic disc","Ora serrata","Peripheral retina only"], "The fovea has dense cones and gives highest visual acuity."),
q("The optic disc is blind because it lacks which cells?", "Photoreceptors", ["Ganglion cells","Astrocytes","Blood vessels"], "No rods or cones are present at the optic nerve head."),
q("Phototransduction in rods begins with light-induced change in which pigment?", "Rhodopsin", ["Melanin","Haemoglobin","Myosin"], "Rhodopsin absorbs light and initiates the rod response."),
q("A lesion of the optic chiasma classically causes which visual field defect?", "Bitemporal hemianopia", ["Left monocular blindness","Right homonymous hemianopia","Central scotoma only"], "Chiasmal lesions affect crossing nasal retinal fibres.", True),
q("The pupillary light reflex uses which cranial nerves?", "Optic and oculomotor nerves", ["Facial and trigeminal nerves","Vagus and glossopharyngeal nerves","Accessory and hypoglossal nerves"], "CN II is afferent and CN III parasympathetic fibres are efferent."),
q("Raised intraocular pressure damages retinal ganglion cell axons in which condition?", "Glaucoma", ["Cataract","Myopia","Presbyopia"], "Glaucoma causes optic neuropathy from pressure-related ganglion cell damage.", True),
]),
("hearing","Sense of Hearing",2,[
q("Sound waves are transmitted from tympanic membrane to inner ear by which bones?", "Auditory ossicles", ["Semicircular canals","Cochlear hair cells","Eustachian tube"], "Malleus, incus and stapes conduct vibrations to the oval window."),
q("The organ of Corti is located in which structure?", "Cochlea", ["Utricle","Saccule","Middle ear cavity"], "The organ of Corti sits on the basilar membrane in the cochlea."),
q("Inner hair cells primarily perform which role?", "Sensory transduction for hearing", ["Endolymph secretion only","Pressure equalization","Sound reflection"], "Inner hair cells provide most auditory afferent signalling."),
q("A patient with wax blocking the external auditory canal has which type of hearing loss?", "Conductive hearing loss", ["Sensorineural hearing loss","Central aphasia","Vestibular ataxia"], "External or middle ear obstruction impairs sound conduction.", True),
q("High-frequency sounds maximally stimulate which part of basilar membrane?", "Base of cochlea", ["Apex of cochlea","Utricle","Round window only"], "The stiff narrow base responds best to high frequencies."),
q("Low-frequency sounds maximally stimulate which part of cochlea?", "Apex", ["Base","Oval window only","Tympanic membrane"], "The wider flexible apex responds to low frequencies."),
q("The auditory pathway reaches primary auditory cortex in which lobe?", "Temporal lobe", ["Occipital lobe","Frontal lobe only","Parietal lobe only"], "Primary auditory cortex lies in the superior temporal region."),
q("A patient with aminoglycoside ototoxicity develops hearing loss due to injury of which cells?", "Cochlear hair cells", ["Retinal rods","Olfactory bulb neurons","Taste bud basal cells"], "Aminoglycosides can damage inner ear hair cells.", True),
q("The Eustachian tube mainly equalizes pressure between middle ear and what?", "Nasopharynx", ["Cochlea","Cerebellum","External auditory canal only"], "The auditory tube connects middle ear to nasopharynx."),
q("Rinne test showing bone conduction greater than air conduction suggests which problem?", "Conductive hearing loss", ["Normal hearing","Pure cortical deafness","Optic nerve lesion"], "In conductive loss, air conduction is reduced relative to bone conduction.", True),
]),
("smell-taste","Chemical Senses: Smell and Taste",3,[
q("Olfactory receptor neurons are located mainly in which region?", "Olfactory epithelium", ["Cochlea","Retina","Tongue papillae only"], "Olfactory receptors lie in specialized nasal epithelium."),
q("Olfactory signals first synapse in which structure?", "Olfactory bulb", ["Thalamus only","Cochlear nucleus","Geniculate ganglion"], "Olfactory receptor axons synapse in glomeruli of the olfactory bulb."),
q("Taste buds detect chemicals dissolved in what?", "Saliva", ["Endolymph","CSF","Aqueous humour"], "Taste substances must dissolve in saliva to stimulate taste receptors."),
q("A patient loses smell after head trauma with cribriform plate injury. Which nerve is damaged?", "Olfactory nerve", ["Optic nerve","Facial nerve only","Vagus nerve"], "Olfactory filaments pass through the cribriform plate and can be sheared.", True),
q("Sweet taste is commonly associated with which class of substances?", "Sugars", ["Strong acids","Alkaloids","Sodium salts only"], "Sugars stimulate sweet taste receptors."),
q("Sour taste is mainly produced by which ion?", "Hydrogen ion", ["Calcium ion","Ferric ion","Bicarbonate ion"], "Acids produce sour taste through hydrogen ions."),
q("Bitter taste is important physiologically because it may signal what?", "Potential toxins", ["Oxygen level","Sound intensity","Lens curvature"], "Many toxic plant alkaloids taste bitter."),
q("A patient with facial nerve injury proximal to chorda tympani loses taste from which area?", "Anterior two-thirds of tongue", ["Posterior one-third only","Epiglottis only","Soft palate only"], "Chorda tympani carries taste from anterior two-thirds of tongue.", True),
q("Taste from posterior one-third of tongue is carried mainly by which nerve?", "Glossopharyngeal nerve", ["Facial nerve","Hypoglossal nerve","Optic nerve"], "CN IX carries taste from posterior third of tongue."),
q("Loss of smell reduces flavour perception because flavour depends heavily on which input?", "Olfactory input", ["Vestibular input","Renal input","Motor cortex output"], "Retronasal olfaction strongly contributes to perceived flavour.", True),
]),
]

def build():
    out=[]
    for slug,topic,order,rows in TOPICS:
        for i,row in enumerate(rows,1):
            shift=(order+i)%4
            opts=row["options"][shift:]+row["options"][:shift]
            ans=row["answer"]
            out.append({**BASE,**row,"id":f"physiology-special-senses-{slug}-{i:02d}","topic":topic,"topicTitle":topic,"topicOrder":order,"options":opts,"answerIndex":opts.index(ans),"answer":ans})
    return out

def validate(qs):
    if len(qs)!=30: raise ValueError(f"Expected 30, got {len(qs)}")
    if len({q["id"] for q in qs})!=30: raise ValueError("Duplicate IDs")
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
