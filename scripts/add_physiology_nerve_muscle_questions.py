import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Nerve Muscle Physiology"
CHAPTER_ORDER = 5
SOURCE_PDF = "physiology 1.pdf"
SOURCE_PAGE_START = 55
SOURCE_PAGE_END = 104

BASE = {
    "subjectId": "physiology",
    "subjectTitle": "Physiology",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "sourcePdf": SOURCE_PDF,
    "sourcePdfPageStart": SOURCE_PAGE_START,
    "sourcePdfPageEnd": SOURCE_PAGE_END,
    "chapterOrder": CHAPTER_ORDER,
    "imageUrls": [],
}


def q(prompt, options, answer_index, explanation, clinical=False, difficulty="moderate"):
    return {
        "prompt": prompt,
        "options": options,
        "answerIndex": answer_index,
        "answer": options[answer_index],
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("nerve", "The Nerve", 1, [
        q("What is the structural and functional unit of the nervous system?", ["Neuron", "Schwann cell", "Endoneurium", "Epineurium"], 0, "The source defines the neuron or nerve cell as the structural and functional unit of the nervous system."),
        q("Absence of which structure explains why destroyed neurons are not replaced by cell division?", ["Centrosome", "Nissl body", "Axolemma", "Node of Ranvier"], 0, "The neuronal cell body lacks a centrosome, indicating loss of ability for division."),
        q("Which neuronal component is composed of rough endoplasmic reticulum and indicates high protein synthesis?", ["Nissl bodies", "Myelin sheath", "Terminal buttons", "Perineurium"], 0, "Nissl granules are basophilic rough ER and indicate high protein synthesis in neurons."),
        q("Chromatolysis of Nissl bodies may occur after which event?", ["Sectioning of the axon", "Opening of gap junctions", "Formation of sarcomeres", "Calcium binding to troponin"], 0, "The source notes that Nissl bodies disintegrate in fatigue, poisoning and after sectioning of the axon.", clinical=True),
        q("Which part of a neuron conducts impulses away from the cell body?", ["Axon", "Dendrite", "Nucleolus", "Microglia"], 0, "Axons perform the specialized function of conducting impulses away from the cell body."),
        q("What are nodes of Ranvier?", ["Periodic gaps between myelinated Schwann cell segments", "Terminal synaptic vesicles", "Neuron cell bodies", "Layers of epineurium"], 0, "Nodes of Ranvier are short periodic gaps at junctions between myelin segments."),
        q("Retrograde axoplasmic flow may carry which agents to neuronal cell bodies in the CNS?", ["Tetanus toxin and neurotropic viruses", "Troponin and tropomyosin", "Albumin and fibrinogen", "Glucose and amino acids only"], 0, "The source mentions tetanus toxin and viruses such as polio, herpes simplex and rabies can travel by retrograde flow.", clinical=True),
        q("Which connective tissue sheath covers each fasciculus of a peripheral nerve?", ["Perineurium", "Endoneurium", "Epineurium", "Sarcolemma"], 0, "Each nerve fasciculus is covered by perineurium, whose cells act as a barrier."),
        q("What is the resting membrane potential recorded inside a nerve fibre in the source example?", ["-70 mV", "+35 mV", "-55 mV", "-90 mV"], 0, "With one microelectrode inside the axon, a steady potential difference of about -70 mV is recorded."),
        q("A subthreshold stimulus depolarizes a nerve by about 7 mV but does not propagate. Propagation begins only when depolarization reaches about:", ["-55 mV", "-90 mV", "+130 mV", "0 mV exactly"], 0, "The source gives firing level as about -55 mV, after which abrupt propagated action potential occurs.", clinical=True),
    ]),
    ("neuromuscular-junction", "Neuromuscular Junction", 2, [
        q("What is the neuromuscular junction?", ["Synapse between a motor nerve terminal and skeletal muscle fibre", "Gap junction between smooth muscle cells", "Node between two Schwann cells", "A mitochondrial calcium pump"], 0, "The chapter describes NMJ as the junction where a motor nerve terminal communicates with skeletal muscle."),
        q("Which neurotransmitter mediates transmission at the skeletal neuromuscular junction?", ["Acetylcholine", "Norepinephrine", "Dopamine", "Histamine"], 0, "Neuromuscular transmission at skeletal muscle uses acetylcholine released from nerve terminals."),
        q("Where is acetylcholine stored before release at the NMJ?", ["Synaptic vesicles", "T-tubules", "Dense bodies", "Z discs"], 0, "The source describes acetylcholine synthesis and storage in vesicles at the nerve terminal."),
        q("Entry of which ion into the nerve terminal triggers acetylcholine release?", ["Ca2+", "K+", "Cl-", "HCO3-"], 0, "Calcium entry into the nerve terminal triggers release of acetylcholine vesicles."),
        q("Acetylcholine acts on the postsynaptic membrane to produce which local potential?", ["End plate potential", "Plateau potential", "After-hyperpolarization only", "Oncotic pressure"], 0, "Acetylcholine opens channels at the motor end plate and develops the end plate potential."),
        q("Which enzyme removes acetylcholine from the neuromuscular junction?", ["Acetylcholinesterase", "Myosin ATPase", "Na+-K+ ATPase", "DNA helicase"], 0, "Acetylcholine is removed mainly by acetylcholinesterase at the junction."),
        q("Myasthenia gravis primarily impairs which site/process?", ["Postsynaptic neuromuscular transmission", "DNA replication", "Osmosis", "Renal glucose reabsorption"], 0, "Myasthenia gravis is discussed with neuromuscular disorders and classically affects postsynaptic transmission.", clinical=True),
        q("A toxin prevents acetylcholine release from motor nerve terminals. Which immediate effect is expected?", ["Failure of skeletal muscle activation", "Excessive RBC swelling", "Increased chromosome number", "Apoptosis of web tissue"], 0, "Without acetylcholine release, the end plate potential cannot adequately activate the muscle fibre.", clinical=True),
        q("The motor end plate belongs to which muscle type in this source contrast?", ["Skeletal muscle", "Single-unit smooth muscle", "Cardiac muscle only", "Uterine smooth muscle only"], 0, "The source contrasts skeletal muscle motor end plates with smooth muscle varicosities that do not form direct motor end plates."),
        q("A drug that inhibits acetylcholinesterase at the NMJ would most directly prolong:", ["Acetylcholine action at the end plate", "DNA transcription", "Osmotic pressure", "Myelin formation"], 0, "Inhibiting acetylcholinesterase delays acetylcholine removal and prolongs its junctional action.", clinical=True),
    ]),
    ("skeletal-muscle", "Skeletal Muscle", 3, [
        q("Skeletal muscle fibres are described as which structural type?", ["Striated cylindrical fibres", "Spindle-shaped nonstriated cells", "Ribbon-like branched cells", "Neuron fasciculi"], 0, "The comparison table describes skeletal fibres as cylindrical and striated."),
        q("Which regulatory protein complex is present in skeletal muscle thin filaments?", ["Troponin-tropomyosin", "Calmodulin only", "Connexin", "CFTR"], 0, "Skeletal muscle contraction is regulated by troponin-tropomyosin on thin filaments."),
        q("The T-tubule system of skeletal muscle is part of which function?", ["Excitation-contraction coupling", "DNA replication", "Endocytosis", "Axoplasmic transport"], 0, "The sarcotubular system, including T-tubules, carries excitation inward for excitation-contraction coupling."),
        q("During skeletal muscle contraction, thin filaments slide over thick filaments due to:", ["Cross-bridge cycling", "Chromatolysis", "Gibbs-Donnan equilibrium", "Pinocytosis"], 0, "The source explains contraction by molecular cross-bridge cycling and sliding of thin over thick filaments."),
        q("Which ion binds to troponin to initiate skeletal muscle contraction?", ["Ca2+", "Na+", "Cl-", "I-"], 0, "Calcium binds to troponin, allowing actin-myosin interaction in skeletal muscle."),
        q("What is a motor unit?", ["One motor neuron and the muscle fibres it supplies", "One actin and one myosin molecule", "One Schwann cell and one node", "One chromosome pair"], 0, "The motor unit is the functional group of a motor neuron and its innervated muscle fibres."),
        q("Holding a heavy object without changing muscle length is which type of contraction?", ["Isometric", "Isotonic", "Apoptotic", "Osmotic"], 0, "In isometric contraction, tension develops without change in muscle length.", clinical=True),
        q("Lifting a load with muscle shortening is which type of contraction?", ["Isotonic", "Isometric", "Tetanus only", "Fibrillation"], 0, "In isotonic contraction, muscle length changes while moving a load.", clinical=True),
        q("Electromyography is used to record electrical activity of which tissue?", ["Skeletal muscle", "Plasma proteins", "Chromosomes", "Renal filtrate"], 0, "The chapter discusses electromyography and electromyogram for skeletal muscle electrical activity.", clinical=True),
        q("Muscular dystrophy, myotonia and myasthenia gravis are listed under:", ["Disorders of skeletal muscles", "Genetic screening only", "Vesicular transport", "Body fluid tonicity"], 0, "These are listed under common disorders of skeletal muscles in the chapter.", clinical=True),
    ]),
    ("smooth-muscle", "Smooth Muscle", 4, [
        q("Smooth muscle fibres are typically:", ["Spindle-shaped cells with central nuclei", "Long cylindrical fibres with peripheral nuclei", "Branched ribbon-like fibres", "Myelinated axons"], 0, "Smooth muscle fibres are long spindle-shaped myocytes with a central nucleus."),
        q("Which junction allows adjacent single-unit smooth muscle cells to communicate?", ["Gap junction", "Tight junction only", "Node of Ranvier", "Motor end plate"], 0, "Adjacent smooth muscle cells communicate through gap junctions, especially in single-unit smooth muscle."),
        q("Compared with skeletal muscle, smooth muscle lacks which regulatory protein?", ["Troponin", "Actin", "Myosin", "ATP"], 0, "Smooth muscle thin filaments lack troponin; calcium acts through calmodulin."),
        q("In smooth muscle, calcium binds to which protein to activate contraction?", ["Calmodulin", "Troponin C", "Connexin", "Nissl protein"], 0, "Calcium-calmodulin activates myosin light chain kinase in smooth muscle."),
        q("Which enzyme phosphorylates the myosin regulatory light chain in smooth muscle?", ["Myosin light chain kinase", "Acetylcholinesterase", "DNA polymerase", "Reverse transcriptase"], 0, "MLCK uses ATP to phosphorylate the myosin regulatory chain, enabling cross-bridge formation."),
        q("Depolarization in smooth muscle action potentials is mainly due to entry of:", ["Ca2+", "Na+ only", "Cl- only", "Proteins"], 0, "The source states smooth muscle depolarization occurs due to calcium entry rather than sodium entry."),
        q("A gut smooth muscle strip shows rhythmic slow waves and rhythmic contractions. These slow waves are due to:", ["Pacemaker potentials", "Nissl bodies", "Chromosome replication", "Myelin gaps"], 0, "Slow wave or pacemaker potentials underlie rhythmic contractions in many visceral smooth muscles.", clinical=True),
        q("The latch phenomenon in smooth muscle helps maintain contraction with:", ["Low energy use", "Rapid fatigue", "No calcium involvement", "Loss of myosin"], 0, "The chapter lists latch phenomenon as a characteristic allowing sustained smooth muscle contraction efficiently.", clinical=True),
        q("Autonomic nerve fibres supplying smooth muscle release transmitter mainly from:", ["Varicosities", "Motor end plates", "Nodes of Ranvier", "Nucleoli"], 0, "Smooth muscle autonomic fibres have beaded varicosities that release neurotransmitter into interstitial fluid."),
        q("Multiunit smooth muscles such as iris and piloerector muscles usually respond mainly to:", ["Nerve stimuli", "Stretch only", "Voluntary somatic commands only", "RBC tonicity"], 0, "The source says multiunit smooth muscles, including iris and piloerector muscles, usually respond to nerve stimuli.", clinical=True),
    ]),
    ("cardiac-muscle", "Cardiac Muscle", 5, [
        q("Cardiac muscle fibres are best described as:", ["Striated, branched and functionally connected", "Non-striated spindle-shaped isolated cells", "Unmyelinated axons", "Only epithelial sheets"], 0, "The comparison table describes cardiac muscle as striated with branching and functional connections forming a syncytium."),
        q("Cardiac muscle is controlled by which nervous system?", ["Autonomic nervous system", "Somatic voluntary nerves", "Only sensory afferents", "No nerves at all"], 0, "The table lists cardiac muscle as involuntary and supplied by autonomic nerves."),
        q("The resting membrane potential of cardiac muscle in the comparison table is approximately:", ["-90 mV", "-55 mV", "-25 mV", "+60 mV"], 0, "The comparison table lists cardiac resting membrane potential as about -90 mV."),
        q("What action potential shape is typical of cardiac muscle in the comparison table?", ["Plateau potential of 100-300 ms", "Spike potential of 5 ms only", "No action potential", "Pacemaker wave only in all fibres"], 0, "Cardiac muscle has a plateau action potential lasting about 100-300 ms."),
        q("Why is tetanus not possible in cardiac muscle?", ["Long refractory period", "Absence of actin", "No calcium use", "No mitochondria"], 0, "The table states tetanus is not possible due to the long refractory period.", clinical=True),
        q("Cardiac muscle has many mitochondria mainly reflecting:", ["High oxygen consumption and continuous work", "No ATP use", "Absence of blood supply", "Lack of contractility"], 0, "The comparison table notes many mitochondria and high oxygen consumption in cardiac muscle."),
        q("A patient develops reduced myocardial contractility when extracellular calcium availability falls. This reflects that cardiac excitation-contraction coupling is partly dependent on:", ["Extracellular calcium", "Only intracellular proteins", "Only chloride channels", "Chromosome number"], 0, "The comparison table states cardiac contraction is partly dependent on extracellular calcium concentration.", clinical=True),
        q("Which property is listed for cardiac muscle but not skeletal muscle in the comparison table?", ["Autorhythmicity", "Voluntary control", "Multiple fibre summation", "Tetanus"], 0, "Cardiac muscle has autorhythmicity, while skeletal muscle does not."),
        q("Cardiac muscle obeys all-or-none law at the level of:", ["Whole muscle", "Single sarcomere only", "Single Schwann cell", "Each RBC"], 0, "The table states cardiac muscle obeys all-or-none law as a whole muscle because it behaves as a functional syncytium."),
        q("A myocardium with a very long refractory period is protected against sustained fused contraction. Which clinical principle does this explain?", ["Cardiac tetanus is prevented", "Cardiac muscle becomes voluntary", "Cardiac muscle lacks action potentials", "Cardiac muscle cannot conduct"], 0, "The long refractory period prevents tetanus, allowing rhythmic contraction-relaxation cycles essential for pumping.", clinical=True),
    ]),
]


def build_questions():
    questions = []
    for slug, topic, topic_order, rows in TOPICS:
        for index, row in enumerate(rows, 1):
            option_shift = (topic_order + index) % 4
            options = row["options"][option_shift:] + row["options"][:option_shift]
            answer = row["answer"]
            questions.append({
                **BASE,
                **row,
                "id": f"physiology-nerve-muscle-{slug}-{index:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "options": options,
                "answerIndex": options.index(answer),
                "answer": answer,
            })
    return questions


def validate(questions):
    if len(TOPICS) != 5 or len(questions) != 50:
        raise ValueError("Expected 5 topics and 50 questions")
    if len({question["id"] for question in questions}) != len(questions):
        raise ValueError("Duplicate question ids")
    for _, topic, _, _ in TOPICS:
        topic_questions = [question for question in questions if question["topic"] == topic]
        clinical_count = sum("clinical" in question.get("tags", []) for question in topic_questions)
        if len(topic_questions) != 10:
            raise ValueError(f"{topic} must contain exactly 10 questions")
        if clinical_count < 3:
            raise ValueError(f"{topic} must contain at least 3 clinical questions")
    for question in questions:
        if len(question["options"]) != 4:
            raise ValueError(f"{question['id']} must contain 4 options")
        if question["answer"] != question["options"][question["answerIndex"]]:
            raise ValueError(f"{question['id']} has a bad answer mapping")


def update_file(path, questions):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    new_ids = {question["id"] for question in questions}
    data["questions"] = [question for question in data.get("questions", []) if question.get("id") not in new_ids] + questions
    data["questions"].sort(key=lambda item: item.get("id", ""))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    questions = build_questions()
    validate(questions)
    for path in DATA_PATHS:
        update_file(path, questions)
        print(f"Added {len(questions)} physiology questions to {path}.")
    for _, topic, _, _ in TOPICS:
        print(f"- {topic}: 10 questions")


if __name__ == "__main__":
    main()
