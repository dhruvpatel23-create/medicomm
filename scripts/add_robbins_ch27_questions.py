import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Peripheral Nerves and Skeletal Muscles"
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
    ("nerve-injury", "Peripheral Nerve Structure, Injury, and Regeneration", [
        q("easy", "Schwann cells normally form myelin in the:", "Peripheral nervous system", ["Central nervous system", "Bone marrow", "Skeletal muscle sarcomere"], "Schwann cells myelinate peripheral axons."),
        q("easy", "Wallerian degeneration occurs distal to:", "Axonal transection", ["Muscle hypertrophy", "Myelin excess", "Neuromuscular blockade"], "The distal axon degenerates after axonal injury."),
        q("easy", "A traumatic neuroma is a reactive proliferation after:", "Nerve injury", ["Bone infection", "Muscle tumor", "Joint degeneration"], "Disorganized regenerating nerve forms a traumatic neuroma."),
        q("moderate", "Axonal regeneration in peripheral nerve depends on:", "Intact Schwann cell tubes", ["Astrocyte scars only", "Osteoclast activity", "Synovial pannus"], "Schwann cell basal lamina guides regenerating axons."),
        q("moderate", "Endoneurium surrounds individual:", "Nerve fibers", ["Muscle fascicles", "Bone trabeculae", "Tendon bundles"], "Endoneurium is connective tissue around single nerve fibers."),
        q("moderate", "A conduction block without axonal loss suggests:", "Demyelination", ["Complete infarction", "Tumor necrosis", "Muscle dystrophy"], "Loss of myelin impairs conduction while axons may remain intact."),
        q("moderate", "Peripheral nerve ischemia commonly injures:", "Axons", ["Hair follicles", "Chondrocytes", "Osteoblasts"], "Ischemic neuropathy often causes axonal degeneration."),
        q("high", "After a deep laceration, the distal segment of a severed peripheral nerve undergoes axonal and myelin breakdown with macrophage cleanup. Which process is occurring?", "Wallerian degeneration", ["Segmental remyelination", "Myopathic atrophy", "Pannus formation"], "Wallerian degeneration affects the distal axon after transection."),
        q("high", "A painful nodule develops at an amputation stump. Microscopy shows a tangled proliferation of axons, Schwann cells, and fibrosis rather than a true neoplasm. Which lesion is present?", "Traumatic neuroma", ["Schwannoma", "Neurofibroma", "Rhabdomyoma"], "Traumatic neuroma is disorganized regenerative nerve growth."),
        q("high", "A peripheral nerve biopsy after compression injury shows preserved axons but focal myelin loss and slowed conduction across the lesion. Which primary injury pattern is most likely?", "Segmental demyelination", ["Complete axonal transection", "Myonecrosis", "Dystrophic calcification"], "Demyelination causes conduction slowing or block with relative axon preservation."),
    ]),
    ("inherited-neuropathies", "Inherited and Metabolic Peripheral Neuropathies", [
        q("easy", "Charcot-Marie-Tooth disease is an inherited:", "Peripheral neuropathy", ["Muscular dystrophy only", "Bone tumor", "Joint infection"], "CMT is a group of inherited motor-sensory neuropathies."),
        q("easy", "Diabetic neuropathy commonly affects:", "Distal symmetric nerves", ["Only cranial nerve I", "Only spinal cord", "Only smooth muscle"], "Diabetes often causes distal symmetric polyneuropathy."),
        q("easy", "Amyloid neuropathy involves deposition of:", "Amyloid", ["Urate crystals", "Keratin", "Osteoid"], "Amyloid may deposit in peripheral nerves."),
        q("moderate", "CMT1 is typically a:", "Demyelinating neuropathy", ["Primary myopathy", "Bone dysplasia", "Synovial disorder"], "CMT1 causes segmental demyelination and remyelination."),
        q("moderate", "Onion bulb formations in nerve biopsy reflect repeated:", "Demyelination and remyelination", ["Muscle necrosis", "Cartilage repair", "Urate deposition"], "Concentric Schwann cell processes form onion bulbs."),
        q("moderate", "Diabetic neuropathy is promoted by microvascular injury and:", "Metabolic axonal damage", ["Desmosomal antibodies", "FGFR3 activation", "Synovial pannus"], "Hyperglycemia damages nerves through vascular and metabolic mechanisms."),
        q("moderate", "Hereditary neuropathy with liability to pressure palsies often involves:", "PMP22 deletion", ["RET mutation", "DMD duplication only", "HFE mutation"], "PMP22 deletion causes pressure palsy susceptibility."),
        q("high", "A patient has slowly progressive distal leg weakness, pes cavus, sensory loss, and nerve biopsy showing onion bulbs from repeated demyelination and remyelination. Which disease is likely?", "Charcot-Marie-Tooth disease type 1", ["Diabetic amyotrophy", "Myasthenia gravis", "Duchenne muscular dystrophy"], "CMT1 is a demyelinating inherited neuropathy with onion bulbs."),
        q("high", "A patient with long-standing diabetes has burning feet, loss of vibration sense, autonomic symptoms, and distal symmetric axonal degeneration. Which neuropathy pattern is most likely?", "Diabetic polyneuropathy", ["Guillain-Barre syndrome", "Neurofibromatosis type 2", "Lambert-Eaton syndrome"], "Diabetes causes distal symmetric sensorimotor polyneuropathy."),
        q("high", "A patient has recurrent focal palsies after minor compression at entrapment sites, and genetic testing shows loss of one PMP22 copy. Which inherited neuropathy is suggested?", "Hereditary neuropathy with liability to pressure palsies", ["CMT2A", "Familial ALS", "Duchenne muscular dystrophy"], "PMP22 deletion predisposes to recurrent pressure palsies."),
    ]),
    ("acquired-neuropathies", "Acquired Inflammatory and Toxic Neuropathies", [
        q("easy", "Guillain-Barre syndrome is an acute inflammatory:", "Polyradiculoneuropathy", ["Myopathy", "Bone infection", "Synovitis only"], "GBS affects peripheral nerves and roots."),
        q("easy", "Leprosy commonly damages:", "Peripheral nerves", ["Cardiac valves only", "Renal glomeruli only", "Bone marrow"], "Mycobacterium leprae infects Schwann cells."),
        q("easy", "Toxic neuropathy may be caused by:", "Chemotherapy drugs", ["Vitamin D only", "Calcitonin", "PTH"], "Several chemotherapies injure peripheral nerves."),
        q("moderate", "Guillain-Barre syndrome often follows:", "Infection", ["Bone fracture only", "Breast carcinoma only", "Thyroidectomy"], "GBS may follow Campylobacter or viral infection."),
        q("moderate", "GBS classically causes:", "Ascending weakness and areflexia", ["Pure sensory rash", "Bone pain", "Hyperthyroidism"], "Ascending paralysis with areflexia is classic."),
        q("moderate", "Chronic inflammatory demyelinating polyneuropathy is a chronic counterpart of:", "GBS-like demyelinating neuropathy", ["Osteosarcoma", "Dermatomyositis only", "Gout"], "CIDP is chronic immune-mediated demyelinating neuropathy."),
        q("moderate", "Vasculitic neuropathy often presents as:", "Mononeuritis multiplex", ["Diffuse myotonia", "Osteophytes", "Pseudogout"], "Ischemic injury of separate nerves causes mononeuritis multiplex."),
        q("high", "A patient develops rapidly progressive ascending weakness, areflexia, facial weakness, and albuminocytologic dissociation in CSF after diarrheal illness. Which peripheral nerve disorder is most likely?", "Guillain-Barre syndrome", ["Diabetic neuropathy", "Duchenne muscular dystrophy", "Myasthenia gravis"], "GBS is acute immune polyradiculoneuropathy."),
        q("high", "A patient has asymmetric painful wrist drop and foot drop from necrotizing inflammation of small arteries supplying individual nerves. Which neuropathy pattern is most likely?", "Vasculitic mononeuritis multiplex", ["CMT1", "Lambert-Eaton syndrome", "Myotonic dystrophy"], "Vasculitis causes ischemic injury to multiple named nerves."),
        q("high", "A patient with lepromatous leprosy develops numb skin lesions, sensory loss, and thickened peripheral nerves because organisms invade Schwann cells. Which pathogen is responsible?", "Mycobacterium leprae", ["Mycobacterium tuberculosis", "Treponema pallidum", "Borrelia burgdorferi"], "M. leprae infects Schwann cells and peripheral nerves."),
    ]),
    ("nerve-tumors", "Peripheral Nerve Sheath Tumors", [
        q("easy", "Schwannoma is a benign tumor of:", "Schwann cells", ["Skeletal muscle", "Bone matrix", "Synovium"], "Schwannomas arise from Schwann cells."),
        q("easy", "Neurofibromas are associated with:", "NF1", ["MEN2", "HFE", "BRCA1 only"], "Neurofibromas are characteristic of neurofibromatosis type 1."),
        q("easy", "Bilateral vestibular schwannomas suggest:", "NF2", ["NF1", "MEN1", "Tuberous sclerosis only"], "NF2 classically causes bilateral vestibular schwannomas."),
        q("moderate", "Schwannoma histology shows:", "Antoni A and Antoni B areas", ["Schiller-Duval bodies", "Keratin pearls", "Osteoid seams"], "Schwannomas have alternating compact and loose areas."),
        q("moderate", "Verocay bodies are associated with:", "Schwannoma", ["Neurofibroma", "Rhabdomyosarcoma", "Osteosarcoma"], "Verocay bodies are palisaded nuclear arrangements."),
        q("moderate", "Plexiform neurofibroma is strongly associated with:", "NF1", ["NF2 only", "MEN2B", "Duchenne dystrophy"], "Plexiform neurofibroma is virtually diagnostic of NF1."),
        q("moderate", "Malignant peripheral nerve sheath tumor often arises from:", "Plexiform neurofibroma", ["Osteochondroma", "Fibroadenoma", "Thyroid adenoma"], "MPNST may arise in NF1-associated plexiform neurofibroma."),
        q("high", "A well-circumscribed nerve sheath tumor is eccentric to a nerve and shows alternating Antoni A and Antoni B areas with Verocay bodies. Which tumor is most likely?", "Schwannoma", ["Neurofibroma", "MPNST", "Ganglion cyst"], "Schwannoma is encapsulated and has Antoni patterns."),
        q("high", "A child with cafe-au-lait macules has a large rope-like nerve lesion expanding multiple fascicles. This lesion carries risk for malignant peripheral nerve sheath tumor. Which lesion is it?", "Plexiform neurofibroma", ["Schwannoma", "Traumatic neuroma", "Perineurioma"], "Plexiform neurofibroma is an NF1 lesion with malignant potential."),
        q("high", "A patient with NF2 develops hearing loss and tinnitus, and imaging reveals bilateral tumors of cranial nerve VIII. Which tumor type explains this classic presentation?", "Vestibular schwannoma", ["Plexiform neurofibroma", "Rhabdomyosarcoma", "Malignant melanoma"], "Bilateral vestibular schwannomas are diagnostic of NF2."),
    ]),
    ("nmj", "Neuromuscular Junction Disorders", [
        q("easy", "Myasthenia gravis targets the:", "Acetylcholine receptor", ["Dystrophin", "Myelin basic protein", "Type I collagen"], "Most MG is caused by anti-ACh receptor antibodies."),
        q("easy", "Lambert-Eaton syndrome is associated with:", "Small cell lung carcinoma", ["Colon adenoma", "Papillary thyroid carcinoma", "Osteosarcoma"], "LEMS is often paraneoplastic with small cell carcinoma."),
        q("easy", "Botulism blocks release of:", "Acetylcholine", ["Dystrophin", "PTH", "Myoglobin"], "Botulinum toxin prevents acetylcholine release."),
        q("moderate", "Myasthenia gravis weakness typically worsens with:", "Repeated use", ["Rest", "Cold exposure only", "Vitamin D"], "Neuromuscular transmission fails with activity."),
        q("moderate", "Myasthenia gravis is associated with thymic:", "Hyperplasia or thymoma", ["Amyloid only", "Osteoid", "Melanoma"], "Thymic abnormalities are common in MG."),
        q("moderate", "Lambert-Eaton syndrome involves antibodies against:", "Presynaptic calcium channels", ["Postsynaptic desmoglein", "Dystrophin", "Collagen VI"], "LEMS targets voltage-gated calcium channels."),
        q("moderate", "Lambert-Eaton weakness often improves with:", "Repeated activity", ["Sleep only", "Insulin", "Calcium restriction"], "Facilitation occurs with repeated use."),
        q("high", "A woman has fluctuating ptosis, diplopia, and fatigable weakness that worsens with use. Testing shows antibodies to postsynaptic acetylcholine receptors. Which disease is present?", "Myasthenia gravis", ["Lambert-Eaton syndrome", "Botulism", "Duchenne dystrophy"], "MG causes fatigable weakness from anti-ACh receptor antibodies."),
        q("high", "A smoker has proximal weakness, autonomic symptoms, reduced reflexes, and strength that improves after repeated contraction. Antibodies target presynaptic calcium channels. Which syndrome is likely?", "Lambert-Eaton myasthenic syndrome", ["Myasthenia gravis", "Guillain-Barre syndrome", "Myotonic dystrophy"], "LEMS is often paraneoplastic and presynaptic."),
        q("high", "After eating improperly canned food, a patient develops descending paralysis, dilated pupils, and dry mouth from impaired acetylcholine release. Which toxin-mediated disorder is likely?", "Botulism", ["Tetanus", "Myasthenia gravis", "Polymyositis"], "Botulinum toxin blocks acetylcholine release at neuromuscular junctions."),
    ]),
    ("muscle-injury-patterns", "Skeletal Muscle Structure and Patterns of Injury", [
        q("easy", "Skeletal muscle fibers are multinucleated:", "Myofibers", ["Neurons", "Chondrocytes", "Osteoclasts"], "Skeletal muscle is composed of multinucleated fibers."),
        q("easy", "Rhabdomyolysis releases:", "Myoglobin", ["Bile", "Calcitonin", "Urate only"], "Myoglobin from damaged muscle can injure kidneys."),
        q("easy", "Denervation atrophy affects groups of:", "Muscle fibers", ["Hepatocytes", "Keratinocytes", "Osteoblasts"], "Loss of nerve input causes grouped muscle fiber atrophy."),
        q("moderate", "Neurogenic atrophy produces:", "Angulated atrophic fibers", ["Necrotic keratinocytes", "Osteophytes", "Chondrocyte nests"], "Denervated fibers become small and angulated."),
        q("moderate", "Myopathic injury often shows:", "Fiber size variation with necrosis and regeneration", ["Only demyelination", "Only onion bulbs", "Only pannus"], "Myopathies damage muscle fibers directly."),
        q("moderate", "Myoglobinuria can cause acute injury to:", "Renal tubules", ["Thyroid follicles", "Synovium", "Epidermis"], "Myoglobin is nephrotoxic."),
        q("moderate", "Target fibers are commonly associated with:", "Neurogenic disease", ["Actinic keratosis", "Osteomalacia", "Mucinous carcinoma"], "Target fibers suggest denervation and reinnervation."),
        q("high", "A patient after prolonged immobilization has severe muscle pain, high creatine kinase, dark urine, and acute kidney injury from pigment toxicity. Which muscle injury syndrome is present?", "Rhabdomyolysis", ["Myasthenia gravis", "Dermatomyositis", "Neurofibromatosis"], "Rhabdomyolysis releases myoglobin and CK."),
        q("high", "A muscle biopsy from a patient with motor neuron loss shows small angular fibers in groups and fiber-type grouping after reinnervation. Which injury pattern is present?", "Neurogenic atrophy", ["Primary myopathic necrosis", "Mitochondrial myopathy", "Dystrophic calcification"], "Denervation produces grouped angular atrophy."),
        q("high", "A muscle biopsy shows necrotic and regenerating fibers, internal nuclei, fiber splitting, and endomysial fibrosis without primary nerve loss. Which broad process is suggested?", "Primary myopathic injury", ["Peripheral nerve demyelination", "Synovial pannus", "Bone remodeling"], "Myopathies primarily injure muscle fibers."),
    ]),
    ("muscular-dystrophies", "Muscular Dystrophies and Inherited Myopathies", [
        q("easy", "Duchenne muscular dystrophy is caused by absence of:", "Dystrophin", ["Collagen I", "Myelin", "Acetylcholine receptor"], "Duchenne dystrophy has absent dystrophin."),
        q("easy", "Becker muscular dystrophy has abnormal but partially functional:", "Dystrophin", ["PTH", "RET", "Myoglobin"], "Becker dystrophy is milder because dystrophin is reduced or abnormal."),
        q("easy", "Myotonic dystrophy is characterized by delayed:", "Muscle relaxation", ["Bone mineralization", "Nerve myelination", "Synovial lubrication"], "Myotonia is delayed relaxation after contraction."),
        q("moderate", "Duchenne muscular dystrophy inheritance is:", "X-linked recessive", ["Autosomal dominant only", "Mitochondrial only", "Y-linked"], "DMD gene is on the X chromosome."),
        q("moderate", "Duchenne dystrophy often causes calf enlargement due to:", "Pseudohypertrophy", ["True tumor", "Synovitis", "Edema only"], "Fat and fibrosis enlarge calves."),
        q("moderate", "Gowers sign reflects weakness of:", "Proximal muscles", ["Extraocular muscles only", "Facial nerve", "Distal sensory nerves"], "Children use hands to rise due to proximal weakness."),
        q("moderate", "Myotonic dystrophy is caused by:", "Trinucleotide repeat expansion", ["Dystrophin deletion only", "PMP22 deletion", "RET activation"], "Myotonic dystrophy is a repeat expansion disorder."),
        q("high", "A boy develops delayed walking, proximal weakness, calf pseudohypertrophy, very high CK, and absent dystrophin staining on muscle biopsy. Which disorder is most likely?", "Duchenne muscular dystrophy", ["Becker muscular dystrophy", "Myotonic dystrophy", "Myasthenia gravis"], "Duchenne dystrophy is severe dystrophin deficiency."),
        q("high", "A young man has a milder X-linked dystrophy with later onset, abnormal internally deleted dystrophin, and slow progression compared with Duchenne disease. Which diagnosis fits?", "Becker muscular dystrophy", ["Duchenne muscular dystrophy", "Limb-girdle myasthenia", "Polymyositis"], "Becker dystrophy has partially functional dystrophin."),
        q("high", "An adult has distal muscle weakness, myotonia, cataracts, frontal balding, and testicular atrophy caused by a trinucleotide repeat expansion. Which disorder is most likely?", "Myotonic dystrophy", ["Duchenne dystrophy", "Dermatomyositis", "Lambert-Eaton syndrome"], "Myotonic dystrophy is multisystemic with myotonia and cataracts."),
    ]),
    ("inflammatory-myopathies", "Inflammatory Myopathies", [
        q("easy", "Dermatomyositis has characteristic skin:", "Rash", ["Ulcer from gout", "Neurofibroma", "Keratin cyst"], "Dermatomyositis combines myositis and rash."),
        q("easy", "Polymyositis primarily affects:", "Skeletal muscle", ["Peripheral myelin only", "Bone cartilage", "Synovium only"], "Polymyositis is inflammatory myopathy."),
        q("easy", "Inclusion body myositis commonly affects:", "Older adults", ["Newborns only", "Toddlers only", "Only adolescents"], "Inclusion body myositis is common in older adults."),
        q("moderate", "Dermatomyositis shows inflammation mainly around:", "Perimysial vessels", ["Neuromuscular junction only", "Bone cortex", "Synovial cartilage"], "Dermatomyositis has complement-mediated microangiopathy."),
        q("moderate", "Polymyositis has endomysial inflammation with:", "CD8 T cells", ["IgA deposits", "Urate crystals", "Amyloid only"], "CD8 T cells attack muscle fibers."),
        q("moderate", "Inclusion body myositis shows rimmed:", "Vacuoles", ["Keratin pearls", "Osteophytes", "Horn cysts"], "Rimmed vacuoles are characteristic."),
        q("moderate", "Dermatomyositis can be associated with:", "Underlying malignancy", ["Achondroplasia", "Osteopetrosis", "CMT1 only"], "Adult dermatomyositis can be paraneoplastic."),
        q("high", "A woman has proximal muscle weakness, heliotrope rash, Gottron papules, elevated creatine kinase, and biopsy showing perifascicular atrophy with perivascular inflammation. Which myopathy is most likely?", "Dermatomyositis", ["Polymyositis", "Inclusion body myositis", "Duchenne dystrophy"], "Dermatomyositis has rash, perifascicular atrophy, and vascular injury."),
        q("high", "A patient has symmetric proximal muscle weakness without rash. Biopsy shows endomysial CD8 T cells invading non-necrotic muscle fibers. Which inflammatory myopathy is likely?", "Polymyositis", ["Dermatomyositis", "Myasthenia gravis", "Neurogenic atrophy"], "Polymyositis is CD8-mediated endomysial myositis."),
        q("high", "An older man has slowly progressive weakness of quadriceps and finger flexors, poor response to immunosuppression, and muscle biopsy with rimmed vacuoles. Which diagnosis fits?", "Inclusion body myositis", ["Polymyositis", "Duchenne dystrophy", "Lambert-Eaton syndrome"], "Inclusion body myositis affects older adults and has rimmed vacuoles."),
    ]),
    ("metabolic-toxic-myopathies", "Metabolic, Mitochondrial, and Toxic Myopathies", [
        q("easy", "McArdle disease is a defect of muscle:", "Glycogen phosphorylase", ["Dystrophin", "Acetylcholine receptor", "PMP22"], "McArdle disease is myophosphorylase deficiency."),
        q("easy", "Mitochondrial myopathy may show ragged:", "Red fibers", ["Blue nevi", "White thrombi", "Yellow cartilage"], "Ragged red fibers reflect abnormal mitochondria."),
        q("easy", "Steroid myopathy causes:", "Proximal weakness", ["Myotonia only", "Paresthesia only", "Bone tumor"], "Glucocorticoids can cause proximal muscle weakness."),
        q("moderate", "McArdle disease causes exercise intolerance and:", "Myoglobinuria", ["Hyperthyroidism", "Synovitis", "Cataracts always"], "Exercise can trigger cramps and rhabdomyolysis."),
        q("moderate", "Mitochondrial diseases often show maternal inheritance because mitochondria are:", "Maternally transmitted", ["X-linked only", "Autosomal recessive only", "Y-linked"], "Mitochondrial DNA is inherited from the mother."),
        q("moderate", "Lipid storage myopathy can be due to defects in:", "Fatty acid oxidation", ["Keratinization", "Bone resorption", "Synovial proliferation"], "Impaired fatty acid use causes lipid accumulation."),
        q("moderate", "Statin-associated myopathy may show elevated:", "Creatine kinase", ["Calcitonin", "PTH", "TSH receptor antibody"], "Muscle injury raises CK."),
        q("high", "A teenager develops muscle cramps and dark urine during intense exercise, with failure of lactate to rise during forearm exercise testing. Which metabolic myopathy is likely?", "McArdle disease", ["Pompe disease", "Duchenne dystrophy", "Myasthenia gravis"], "McArdle disease impairs muscle glycogen breakdown."),
        q("high", "A patient has exercise intolerance, lactic acidosis, neurologic symptoms, maternal inheritance pattern, and muscle biopsy showing ragged red fibers from subsarcolemmal mitochondrial accumulation. Which category fits?", "Mitochondrial myopathy", ["Neurogenic atrophy", "Dermatomyositis", "Becker dystrophy"], "Ragged red fibers indicate mitochondrial proliferation."),
        q("high", "A patient on high-dose glucocorticoids develops painless proximal weakness with selective type II fiber atrophy and minimal inflammation. Which toxic myopathy is most likely?", "Steroid myopathy", ["Polymyositis", "McArdle disease", "Inclusion body myositis"], "Steroid myopathy causes type II fiber atrophy."),
    ]),
    ("muscle-tumors", "Skeletal Muscle Tumors and Soft Tissue Mimics", [
        q("easy", "Rhabdomyosarcoma shows differentiation toward:", "Skeletal muscle", ["Peripheral nerve", "Cartilage", "Synovium"], "Rhabdomyosarcoma is a malignant skeletal muscle tumor."),
        q("easy", "Rhabdomyosarcoma is common in:", "Children", ["Elderly adults only", "Only infants with NF2", "Only postmenopausal women"], "It is one of the common pediatric soft tissue sarcomas."),
        q("easy", "Rhabdomyoma is a benign tumor of:", "Skeletal muscle", ["Smooth muscle", "Adipose tissue", "Bone"], "Rhabdomyoma is benign skeletal muscle tumor."),
        q("moderate", "Embryonal rhabdomyosarcoma may form a botryoid mass in:", "Hollow mucosal organs", ["Bone cortex", "Thyroid follicles", "Synovial cartilage"], "Botryoid variant occurs beneath mucosal surfaces."),
        q("moderate", "Alveolar rhabdomyosarcoma is associated with:", "PAX3-FOXO1 fusion", ["EWSR1-FLI1", "SS18-SSX", "BCR-ABL"], "Alveolar RMS often has PAX3/7-FOXO1 fusion."),
        q("moderate", "Rhabdomyoblasts may appear as:", "Strap cells", ["Reed-Sternberg cells", "Koilocytes", "Osteoclasts only"], "Strap cells suggest skeletal muscle differentiation."),
        q("moderate", "Myogenin and MyoD1 are markers of:", "Skeletal muscle differentiation", ["Neural sheath differentiation", "Adipocytic differentiation", "Bone formation"], "These nuclear markers support rhabdomyosarcoma."),
        q("high", "A child has a soft tissue tumor near the orbit composed of primitive cells and strap-shaped rhabdomyoblasts positive for desmin and myogenin. Which tumor is most likely?", "Rhabdomyosarcoma", ["Schwannoma", "Liposarcoma", "Neurofibroma"], "Rhabdomyosarcoma is a pediatric skeletal muscle sarcoma."),
        q("high", "A grape-like polypoid mass protrudes from the vagina of a young child and shows cambium layer of malignant rhabdomyoblasts beneath mucosa. Which variant is likely?", "Embryonal rhabdomyosarcoma, botryoid type", ["Alveolar rhabdomyosarcoma", "Leiomyoma", "Schwannoma"], "Botryoid RMS forms mucosal grape-like masses."),
        q("high", "An adolescent has an aggressive deep soft tissue tumor with alveolar architecture, skeletal muscle differentiation, and PAX3-FOXO1 fusion, showing myogenin positivity. Which diagnosis is favored?", "Alveolar rhabdomyosarcoma", ["Embryonal rhabdomyosarcoma", "Rhabdomyoma", "Nodular fasciitis"], "Alveolar RMS is associated with PAX-FOXO1 fusions."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch27-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 27 questions, got {len(chapter_questions)}")
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
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch27-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 27 questions")
    print(f"Removed {total_removed} existing Chapter 27 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 27 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
