import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "The Central Nervous System"
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
    ("edema-herniation", "Cerebral Edema, Raised ICP, and Herniation", [
        q("easy", "Cerebral edema means increased water content in:", "Brain tissue", ["Bone marrow", "Synovium", "Skin epidermis"], "Cerebral edema is excess fluid within brain parenchyma."),
        q("easy", "Uncal herniation can compress cranial nerve:", "III", ["I", "VII only", "XII only"], "The oculomotor nerve is vulnerable in uncal herniation."),
        q("easy", "Hydrocephalus means dilation of:", "Cerebral ventricles", ["Renal pelvis", "Bile ducts", "Bronchi"], "Hydrocephalus is excess CSF with ventricular enlargement."),
        q("moderate", "Vasogenic edema is caused by disruption of the:", "Blood-brain barrier", ["Neuromuscular junction", "Myelin gene", "Basement membrane of kidney"], "BBB disruption allows extracellular fluid accumulation."),
        q("moderate", "Cytotoxic edema reflects swelling of:", "Neurons and glia", ["Only skull bone", "Only meninges", "Only choroid plexus"], "Cellular energy failure causes intracellular swelling."),
        q("moderate", "Duret hemorrhages occur in the:", "Midbrain and pons", ["Cerebellar cortex only", "Spinal roots", "Basal ganglia only"], "Downward herniation stretches and tears brainstem vessels."),
        q("moderate", "Communicating hydrocephalus results from impaired:", "CSF resorption", ["CSF production always", "Aqueduct obstruction always", "Skull ossification"], "CSF pathways are open but resorption is defective."),
        q("high", "A brain tumor disrupts the blood-brain barrier, causing extracellular fluid accumulation predominantly in white matter around the lesion. Which type of cerebral edema is present?", "Vasogenic edema", ["Cytotoxic edema", "Interstitial edema only", "Hydrostatic pulmonary edema"], "Vasogenic edema follows BBB disruption and is often prominent in white matter."),
        q("high", "A patient with a large temporal lobe mass develops ipsilateral fixed dilated pupil and contralateral weakness. Compression of which structure explains the pupillary finding?", "Oculomotor nerve", ["Optic chiasm", "Facial nerve nucleus", "Abducens nerve only"], "Uncal herniation compresses cranial nerve III."),
        q("high", "After severe diffuse cerebral swelling, autopsy shows linear hemorrhages in the midbrain and pons from downward displacement and vascular tearing. What are these hemorrhages called?", "Duret hemorrhages", ["Charcot-Bouchard aneurysms", "Berry aneurysms", "Virchow-Robin spaces"], "Duret hemorrhages occur in brainstem with herniation."),
    ]),
    ("vascular-cns", "Cerebrovascular Disease and Intracranial Hemorrhage", [
        q("easy", "Ischemic stroke is commonly caused by:", "Thrombotic or embolic arterial occlusion", ["Prion deposition", "Demyelination only", "Pituitary adenoma"], "Reduced blood flow from occlusion causes infarction."),
        q("easy", "Hypertension predisposes to hemorrhage in:", "Basal ganglia", ["Cerebellar tonsils only", "Optic nerve", "Pituitary stalk"], "Hypertensive hemorrhage commonly affects basal ganglia."),
        q("easy", "Subarachnoid hemorrhage commonly results from rupture of:", "Berry aneurysm", ["Meningioma", "Neurofibroma", "Pituitary adenoma"], "Saccular aneurysm rupture causes subarachnoid bleeding."),
        q("moderate", "Lacunar infarcts are associated with:", "Hypertensive small vessel disease", ["Multiple sclerosis", "Medulloblastoma", "Prion disease"], "Lipohyalinosis of small penetrating arteries causes lacunes."),
        q("moderate", "Charcot-Bouchard microaneurysms are associated with:", "Chronic hypertension", ["Celiac disease", "Duchenne dystrophy", "HSV encephalitis"], "Hypertension weakens small penetrating arteries."),
        q("moderate", "Cerebral amyloid angiopathy causes lobar hemorrhage in:", "Older adults", ["Newborns only", "Teenagers only", "Infants with rickets"], "Amyloid weakens cortical and leptomeningeal vessels."),
        q("moderate", "Watershed infarcts occur at:", "Border zones between arterial territories", ["Only choroid plexus", "Only basal ganglia", "Only spinal roots"], "Global hypoperfusion injures arterial boundary zones."),
        q("high", "An elderly patient with Alzheimer disease develops recurrent lobar hemorrhages. Vessel walls contain beta-amyloid in cortical and leptomeningeal arteries on microscopy. Which vasculopathy is likely?", "Cerebral amyloid angiopathy", ["Charcot-Bouchard disease", "Moyamoya disease", "Fibromuscular dysplasia"], "CAA causes lobar hemorrhages in older adults."),
        q("high", "A patient with long-standing hypertension suddenly develops coma. Autopsy shows a large hemorrhage in the putamen from rupture of small penetrating arteries. Which lesion predisposed to this?", "Charcot-Bouchard microaneurysm", ["Berry aneurysm", "Arteriovenous malformation only", "Cavernous hemangioma"], "Hypertension causes small vessel microaneurysms in basal ganglia."),
        q("high", "A patient has thunderclap headache and blood in the subarachnoid space. Angiography finds a saccular aneurysm at an arterial branch point in the circle of Willis. What ruptured?", "Berry aneurysm", ["Lacunar infarct", "Duret hemorrhage", "Subdural bridge vein"], "Berry aneurysm rupture causes classic subarachnoid hemorrhage."),
    ]),
    ("trauma", "CNS Trauma and Traumatic Hemorrhage", [
        q("easy", "Epidural hematoma usually involves rupture of the:", "Middle meningeal artery", ["Bridging veins", "Anterior spinal artery", "Circle of Willis"], "Temporal bone fracture can tear the middle meningeal artery."),
        q("easy", "Subdural hematoma usually involves rupture of:", "Bridging veins", ["Middle meningeal artery", "Charcot-Bouchard aneurysm", "Lenticulostriate artery"], "Bridging veins tear between brain and dural sinuses."),
        q("easy", "Concussion is transient neurologic dysfunction after:", "Head trauma", ["Prion infection", "Demyelination", "Brain tumor only"], "Concussion produces reversible functional disturbance."),
        q("moderate", "Epidural hematoma classically has a:", "Lucid interval", ["Long prodrome of dementia", "Relapsing-remitting course", "Fever first"], "Patients may briefly recover before deterioration."),
        q("moderate", "Subdural hematoma risk is increased by:", "Brain atrophy in elderly patients", ["Thick skull only", "High bone mass", "Acute otitis alone"], "Atrophy stretches bridging veins."),
        q("moderate", "Diffuse axonal injury is caused by:", "Rotational acceleration-deceleration", ["Fungal invasion", "Vitamin deficiency only", "CSF overproduction"], "Shearing forces damage axons."),
        q("moderate", "Coup-contrecoup injuries are brain:", "Contusions", ["Abscesses", "Demyelinating plaques", "Tumors"], "Impact causes cortical contusions at and opposite the blow."),
        q("high", "A young adult has head trauma, brief loss of consciousness, lucid interval, then rapid deterioration. CT shows a biconvex extra-axial bleed. Which vessel is usually torn?", "Middle meningeal artery", ["Bridging vein", "Anterior cerebral artery", "Superior sagittal sinus"], "Epidural hematoma is arterial and lens-shaped."),
        q("high", "An elderly patient with cerebral atrophy develops progressive confusion weeks after minor trauma. CT shows crescent-shaped extra-axial blood crossing suture lines. What is the source?", "Torn bridging veins", ["Middle meningeal artery", "Berry aneurysm", "Choroid plexus"], "Subdural hematoma arises from bridging veins and is crescent-shaped."),
        q("high", "After high-speed motor vehicle crash, a comatose patient has widespread axonal swellings in white matter, corpus callosum, and brainstem. Which traumatic injury is present?", "Diffuse axonal injury", ["Epidural hematoma", "Meningitis", "Watershed infarct"], "Rotational shearing causes diffuse axonal injury."),
    ]),
    ("infections", "Meningitis, Encephalitis, and Brain Abscess", [
        q("easy", "Bacterial meningitis involves inflammation of:", "Leptomeninges", ["Peripheral nerve", "Skeletal muscle", "Bone cortex"], "Meningitis is inflammation of pia-arachnoid and CSF."),
        q("easy", "HSV encephalitis commonly involves the:", "Temporal lobes", ["Cerebellar tonsils only", "Pituitary", "Spinal roots only"], "HSV-1 encephalitis targets temporal lobes."),
        q("easy", "Brain abscess is a focal collection of:", "Pus", ["Amyloid", "Myelin", "Tumor osteoid"], "Abscess is suppurative necrotic infection."),
        q("moderate", "Acute bacterial meningitis CSF usually has:", "Neutrophils", ["Only eosinophils", "No cells", "Malignant glial cells"], "Bacterial meningitis causes neutrophilic CSF pleocytosis."),
        q("moderate", "Cryptococcal meningitis is common in:", "Immunocompromised patients", ["Healthy athletes only", "Newborns only", "Patients with gout"], "Cryptococcus causes opportunistic meningitis."),
        q("moderate", "JC virus causes:", "Progressive multifocal leukoencephalopathy", ["Rabies", "HSV encephalitis", "Poliomyelitis"], "JC virus infects oligodendrocytes and demyelinates CNS."),
        q("moderate", "Rabies infection shows cytoplasmic inclusions called:", "Negri bodies", ["Cowdry bodies", "Lewy bodies", "Pick bodies"], "Negri bodies are rabies inclusions."),
        q("high", "A patient has fever, headache, neck stiffness, cloudy CSF, low glucose, high protein, and many neutrophils on lumbar puncture. Which CNS infection pattern is most likely?", "Acute bacterial meningitis", ["Viral meningitis", "Prion disease", "Progressive multifocal leukoencephalopathy"], "Bacterial meningitis produces neutrophilic low-glucose CSF."),
        q("high", "A patient develops fever, seizures, personality change, aphasia, and hemorrhagic necrosis of temporal lobes with intranuclear viral inclusions on biopsy. Which pathogen is most likely?", "Herpes simplex virus type 1", ["JC virus", "Rabies virus", "Cryptococcus neoformans"], "HSV-1 causes necrotizing temporal lobe encephalitis."),
        q("high", "An AIDS patient develops multifocal demyelinating white matter lesions without mass effect. Oligodendrocytes contain viral inclusions from polyomavirus infection on biopsy. Which disease is present?", "Progressive multifocal leukoencephalopathy", ["Toxoplasmosis", "Bacterial abscess", "Multiple sclerosis"], "JC virus causes PML in immunosuppressed patients."),
    ]),
    ("demyelinating", "Demyelinating and Dysmyelinating Diseases", [
        q("easy", "Multiple sclerosis is a demyelinating disease of the:", "Central nervous system", ["Peripheral nerve only", "Skeletal muscle", "Bone"], "MS targets CNS myelin."),
        q("easy", "Multiple sclerosis plaques often occur around:", "Ventricles", ["Joints", "Adrenal glands", "Peripheral nerves only"], "Periventricular plaques are common."),
        q("easy", "Oligodendrocytes form myelin in the:", "CNS", ["PNS", "Bone marrow", "Skeletal muscle"], "Oligodendrocytes myelinate CNS axons."),
        q("moderate", "MS plaques show relative preservation of:", "Axons early", ["Myelin always", "Neurons only", "Blood vessels only"], "Demyelination initially spares many axons."),
        q("moderate", "CSF in multiple sclerosis may show:", "Oligoclonal IgG bands", ["Very low protein always", "No immune markers", "Only neutrophils"], "Oligoclonal bands support MS."),
        q("moderate", "Acute disseminated encephalomyelitis often follows:", "Infection or vaccination", ["Bone fracture only", "Hypertension", "Pituitary adenoma"], "ADEM is postinfectious immune demyelination."),
        q("moderate", "Neuromyelitis optica is associated with antibodies to:", "Aquaporin-4", ["Desmoglein 3", "Dystrophin", "Acetylcholine receptor"], "NMO often targets aquaporin-4."),
        q("high", "A young woman has episodes of optic neuritis, sensory deficits, and weakness separated in time and space. MRI shows periventricular plaques. Which disease is most likely?", "Multiple sclerosis", ["PML", "ALS", "Alzheimer disease"], "MS produces relapsing CNS demyelinating lesions."),
        q("high", "A demyelinating plaque shows macrophages filled with myelin debris, lymphocytes, and relative axonal preservation in a periventricular white matter lesion. Which process is present?", "Multiple sclerosis plaque", ["Lacunar infarct", "Glioblastoma", "Brain abscess"], "MS plaques are inflammatory demyelinating CNS lesions."),
        q("high", "A patient has severe optic neuritis, intractable vomiting, and longitudinally extensive transverse myelitis with serum aquaporin-4 IgG antibodies. Which demyelinating disease is most likely?", "Neuromyelitis optica spectrum disorder", ["Multiple sclerosis only", "ADEM", "Central pontine myelinolysis"], "NMO targets aquaporin-4 and affects optic nerves and spinal cord."),
    ]),
    ("neurodegenerative", "Neurodegenerative Diseases and Dementia", [
        q("easy", "Alzheimer disease is associated with beta-amyloid plaques and:", "Neurofibrillary tangles", ["Negri bodies", "Lewy bodies only", "Rosenthal fibers"], "Tau tangles and amyloid plaques are key lesions."),
        q("easy", "Parkinson disease involves loss of dopaminergic neurons in:", "Substantia nigra", ["Hippocampus only", "Cerebellar cortex", "Anterior horn only"], "Nigral neuron loss causes parkinsonism."),
        q("easy", "Huntington disease is caused by CAG repeat expansion in:", "HTT", ["APP", "SNCA", "DMD"], "Huntington disease is due to HTT CAG expansion."),
        q("moderate", "Lewy bodies contain:", "Alpha-synuclein", ["Beta-amyloid only", "PrP only", "Huntingtin only"], "Lewy bodies are alpha-synuclein inclusions."),
        q("moderate", "Alzheimer neurofibrillary tangles contain:", "Hyperphosphorylated tau", ["Dystrophin", "GFAP only", "Myelin basic protein"], "Tau aggregates form tangles."),
        q("moderate", "Pick disease is a form of:", "Frontotemporal lobar degeneration", ["Prion disease", "Demyelinating disease", "Bacterial meningitis"], "Pick disease causes frontotemporal dementia."),
        q("moderate", "Huntington disease primarily affects the:", "Caudate nucleus", ["Substantia nigra only", "Cerebellar vermis", "Optic nerve"], "Caudate atrophy is characteristic."),
        q("high", "An elderly patient has progressive memory loss. Brain shows cortical atrophy, neuritic plaques with beta-amyloid cores, and neurofibrillary tangles made of tau. Which disease is most likely?", "Alzheimer disease", ["Parkinson disease", "Huntington disease", "ALS"], "Alzheimer disease has amyloid plaques and tau tangles."),
        q("high", "A patient has resting tremor, rigidity, bradykinesia, shuffling gait, postural instability, and depigmentation of the substantia nigra with intracytoplasmic alpha-synuclein inclusions. Which diagnosis fits?", "Parkinson disease", ["Alzheimer disease", "Huntington disease", "Multiple sclerosis"], "Parkinson disease has Lewy bodies and nigral neuron loss."),
        q("high", "An adult develops chorea, psychiatric changes, progressive dementia, and caudate atrophy with enlarged lateral ventricles due to expanded CAG repeats. Which disorder is present?", "Huntington disease", ["Parkinson disease", "Pick disease", "Creutzfeldt-Jakob disease"], "Huntington disease causes caudate degeneration and chorea."),
    ]),
    ("motor-neuron-prion", "Motor Neuron Disease, Prion Disease, and Ataxias", [
        q("easy", "Amyotrophic lateral sclerosis affects motor neurons in brain and:", "Spinal cord", ["Peripheral myelin only", "Pituitary", "Meninges only"], "ALS damages upper and lower motor neurons."),
        q("easy", "Prion diseases are caused by abnormal:", "PrP protein", ["DNA virus", "Bacterium", "Autoantibody only"], "Misfolded prion protein propagates disease."),
        q("easy", "Creutzfeldt-Jakob disease causes rapidly progressive:", "Dementia", ["Bone pain", "Hyperthyroidism", "Arthritis"], "CJD is a rapidly progressive prion dementia."),
        q("moderate", "ALS commonly shows degeneration of:", "Corticospinal tracts and anterior horn cells", ["Only cerebellar Purkinje cells", "Only optic nerves", "Only hippocampus"], "ALS affects upper and lower motor neuron systems."),
        q("moderate", "Prion disease histology shows:", "Spongiform change", ["Suppurative abscess", "Demyelinating plaque only", "Comedo necrosis"], "Prion disease produces vacuolated neuropil."),
        q("moderate", "Friedreich ataxia is caused by repeat expansion in:", "Frataxin gene", ["HTT", "APP", "SNCA"], "GAA expansion in FXN causes Friedreich ataxia."),
        q("moderate", "ALS usually spares:", "Sensation", ["Motor function", "Respiratory muscles always", "Anterior horn cells"], "Sensory systems are usually spared."),
        q("high", "A patient has progressive weakness, fasciculations, hyperreflexia, spasticity, and muscle atrophy, with degeneration of corticospinal tracts and anterior horn cells. Which disease is likely?", "Amyotrophic lateral sclerosis", ["Guillain-Barre syndrome", "Multiple sclerosis", "Myasthenia gravis"], "ALS combines upper and lower motor neuron signs."),
        q("high", "A patient develops rapidly progressive dementia, myoclonus, and periodic EEG changes. Brain biopsy shows spongiform vacuolation without inflammation. Which disease category is most likely?", "Prion disease", ["Viral encephalitis", "Alzheimer disease", "Bacterial meningitis"], "CJD is a prion disease with spongiform change."),
        q("high", "A teenager has progressive ataxia, loss of position sense, pes cavus, cardiomyopathy, scoliosis, and GAA repeat expansion reducing frataxin. Which disorder is most likely?", "Friedreich ataxia", ["Huntington disease", "ALS", "Parkinson disease"], "Friedreich ataxia is due to frataxin deficiency."),
    ]),
    ("metabolic-toxic", "Metabolic, Toxic, and Nutritional CNS Disorders", [
        q("easy", "Wernicke encephalopathy is due to deficiency of:", "Thiamine", ["Vitamin C", "Vitamin D", "Iron"], "Thiamine deficiency causes Wernicke encephalopathy."),
        q("easy", "Central pontine myelinolysis follows rapid correction of:", "Hyponatremia", ["Hypercalcemia", "Hyperthyroidism", "Iron deficiency"], "Rapid sodium correction can cause osmotic demyelination."),
        q("easy", "Hepatic encephalopathy is associated with elevated:", "Ammonia", ["Calcitonin", "Urate", "Troponin"], "Liver failure impairs ammonia detoxification."),
        q("moderate", "Wernicke encephalopathy lesions involve:", "Mammillary bodies", ["Substantia nigra only", "Caudate only", "Peripheral nerves only"], "Mammillary bodies are classic sites."),
        q("moderate", "Korsakoff syndrome causes:", "Memory impairment and confabulation", ["Chorea", "Exophthalmos", "Myotonia"], "Korsakoff syndrome is chronic thiamine-related amnesia."),
        q("moderate", "Carbon monoxide poisoning injures:", "Globus pallidus", ["Hippocampus only", "Optic chiasm", "Pituitary posterior lobe"], "CO poisoning classically damages globus pallidus."),
        q("moderate", "Hepatic encephalopathy shows Alzheimer type II astrocytes in:", "Cerebral cortex and basal ganglia", ["Peripheral nerve", "Muscle", "Bone"], "Ammonia toxicity alters astrocytes."),
        q("high", "A patient with alcoholism has confusion, ophthalmoplegia, ataxia, and memory difficulty. Autopsy shows hemorrhagic lesions in mammillary bodies and periaqueductal gray. Which deficiency caused this?", "Thiamine deficiency", ["Vitamin C deficiency", "Vitamin D deficiency", "Copper excess"], "Wernicke encephalopathy is due to thiamine deficiency."),
        q("high", "A severely hyponatremic patient is corrected rapidly and develops quadriplegia, dysarthria, and locked-in syndrome. Pathology shows demyelination centered in the pons. Which disorder occurred?", "Central pontine myelinolysis", ["Multiple sclerosis", "PML", "Wernicke encephalopathy"], "Rapid correction of hyponatremia can cause osmotic demyelination."),
        q("high", "A patient with cirrhosis develops confusion and asterixis. Brain shows swollen pale astrocytes with enlarged nuclei in cortex and basal ganglia. Which metabolic encephalopathy is present?", "Hepatic encephalopathy", ["Hypoglycemic encephalopathy", "CO poisoning", "CJD"], "Hepatic encephalopathy causes Alzheimer type II astrocytes."),
    ]),
    ("glial-tumors", "Gliomas and Other Primary Brain Tumors", [
        q("easy", "Glioblastoma is a malignant tumor of:", "Astrocytic lineage", ["Meningothelial cells", "Schwann cells", "Choroid plexus only"], "Glioblastoma is a high-grade diffuse astrocytic glioma."),
        q("easy", "Meningioma arises from:", "Arachnoid cap cells", ["Oligodendrocytes", "Ependymal cells", "Neurons"], "Meningiomas are meningothelial tumors."),
        q("easy", "Medulloblastoma occurs mainly in:", "Children", ["Elderly only", "Only adults with cirrhosis", "Only neonates"], "Medulloblastoma is a pediatric embryonal tumor."),
        q("moderate", "Glioblastoma histology shows necrosis with:", "Pseudopalisading tumor cells", ["Keratin pearls", "Schiller-Duval bodies", "Call-Exner bodies"], "Pseudopalisading necrosis is a hallmark."),
        q("moderate", "Oligodendroglioma often has:", "1p/19q codeletion", ["RET activation", "HFE mutation", "DMD deletion"], "IDH-mutant oligodendroglioma has 1p/19q codeletion."),
        q("moderate", "Ependymoma can show:", "Perivascular pseudorosettes", ["Psammoma bodies only", "Lewy bodies", "Negri bodies"], "Ependymomas form perivascular pseudorosettes."),
        q("moderate", "Pilocytic astrocytoma often contains:", "Rosenthal fibers", ["Auer rods", "Osteoid", "Tophi"], "Pilocytic astrocytoma has Rosenthal fibers and eosinophilic granular bodies."),
        q("high", "An adult has an infiltrative cerebral hemisphere tumor with necrosis, microvascular proliferation, marked nuclear atypia, and pseudopalisading tumor cells. Which glioma is most likely?", "Glioblastoma", ["Pilocytic astrocytoma", "Meningioma", "Ependymoma"], "Glioblastoma is high-grade with necrosis and vascular proliferation."),
        q("high", "A frontal lobe tumor in an adult has uniform cells with perinuclear halos, delicate branching capillaries, calcification, IDH mutation, and 1p/19q codeletion. Which tumor is likely?", "Oligodendroglioma", ["Glioblastoma", "Medulloblastoma", "Schwannoma"], "Oligodendroglioma has fried-egg cells and 1p/19q codeletion."),
        q("high", "A cerebellar tumor in a child is composed of small blue cells and can disseminate through CSF, causing drop metastases along the neuraxis. Which tumor is most likely?", "Medulloblastoma", ["Meningioma", "Oligodendroglioma", "Pituitary adenoma"], "Medulloblastoma is a malignant pediatric cerebellar embryonal tumor."),
    ]),
    ("meningeal-metastatic", "Meningeal, Sellar, and Metastatic CNS Tumors", [
        q("easy", "The most common intracranial tumors in adults are:", "Metastases", ["Medulloblastomas", "Ependymomas", "Neuroblastomas"], "Metastatic tumors are common in adult brain."),
        q("easy", "Meningioma is usually:", "Benign and extra-axial", ["Always intramedullary", "Always metastatic", "A demyelinating plaque"], "Most meningiomas are benign extra-axial tumors."),
        q("easy", "Primary CNS lymphoma is associated with:", "Immunosuppression", ["Achondroplasia", "Gout", "Osteoporosis"], "Immunosuppressed patients have increased CNS lymphoma risk."),
        q("moderate", "Meningioma can show:", "Whorls and psammoma bodies", ["Pseudopalisading necrosis", "Fried-egg cells", "Negri bodies"], "Whorled meningothelial cells and psammoma bodies are classic."),
        q("moderate", "Brain metastases often localize at the:", "Gray-white junction", ["Pituitary posterior lobe only", "Cerebellar tonsil only", "Optic nerve only"], "Embolic tumor cells lodge at vascular border zones."),
        q("moderate", "Primary CNS lymphoma is most often:", "Diffuse large B-cell lymphoma", ["Hodgkin lymphoma", "T-cell ALL always", "Plasma cell myeloma"], "DLBCL is the common primary CNS lymphoma."),
        q("moderate", "Hemangioblastoma is associated with:", "Von Hippel-Lindau disease", ["NF1 only", "MEN2", "BRCA1"], "VHL predisposes to hemangioblastomas."),
        q("high", "An extra-axial dural-based mass compresses the brain and shows meningothelial whorls with psammoma bodies on histologic sections after resection. Which tumor is most likely?", "Meningioma", ["Glioblastoma", "Oligodendroglioma", "Medulloblastoma"], "Meningioma is a dural-based tumor of arachnoid cap cells."),
        q("high", "A patient with lung carcinoma develops multiple well-circumscribed brain masses at the gray-white junction surrounded by vasogenic edema. Which CNS tumor category is most likely?", "Metastatic carcinoma", ["Primary glioblastoma only", "Meningioma", "Ependymoma"], "Metastases commonly form multiple lesions at gray-white junction."),
        q("high", "An AIDS patient develops a deep periventricular brain mass with rapid neurologic decline. Biopsy shows angiocentric sheets of EBV-positive large B cells. Which tumor is most likely?", "Primary CNS lymphoma", ["Medulloblastoma", "Schwannoma", "Meningioma"], "Primary CNS lymphoma is often EBV-positive DLBCL in immunosuppressed patients."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch28-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 28 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch28-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 28 questions")
    print(f"Removed {total_removed} existing Chapter 28 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 28 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
