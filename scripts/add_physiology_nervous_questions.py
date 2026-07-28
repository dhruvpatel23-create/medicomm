import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Nervous System"
CHAPTER_ORDER = 13
BASE = {"subjectId":"physiology","subjectTitle":"Physiology","chapterTitle":CHAPTER,"source":"ai","sourcePdf":"physiology 1.pdf","sourcePdfPageStart":721,"sourcePdfPageEnd":900,"chapterOrder":CHAPTER_ORDER,"imageUrls":[]}

def q(prompt, answer, wrong, explanation, clinical=False):
    return {"prompt":prompt,"options":[answer,*wrong],"answerIndex":0,"answer":answer,"explanation":explanation,"difficulty":"moderate","tags":["clinical"] if clinical else []}

TOPICS = [
("spinal-cord","Physiological Anatomy, Functions and Lesions of Spinal Cord",1,[
q("Which tract carries fine touch, vibration and conscious proprioception?", "Dorsal column-medial lemniscus", ["Lateral spinothalamic tract","Anterior corticospinal tract","Vestibulospinal tract"], "Posterior columns carry discriminative touch, vibration and proprioception."),
q("Pain and temperature from the body ascend mainly through which tract?", "Lateral spinothalamic tract", ["Fasciculus gracilis only","Corticobulbar tract","Rubrospinal tract"], "The lateral spinothalamic tract carries pain and temperature."),
q("The anterior horn of spinal cord contains mainly which neurons?", "Lower motor neurons", ["Preganglionic parasympathetic neurons only","Second-order visual neurons","Pyramidal cells"], "Anterior horn cells are somatic lower motor neurons."),
q("A hemisection of spinal cord causes ipsilateral loss of proprioception and contralateral pain loss. Which syndrome is this?", "Brown-Sequard syndrome", ["Weber syndrome","Wallenberg syndrome","Horner syndrome only"], "Cord hemisection produces ipsilateral dorsal column/corticospinal and contralateral spinothalamic deficits.", True),
q("A muscle stretch reflex is initiated by stimulation of which receptor?", "Muscle spindle", ["Golgi tendon organ only","Pacinian corpuscle","Free nerve ending"], "Muscle spindles detect stretch and mediate stretch reflexes."),
q("Golgi tendon organs mainly respond to which stimulus?", "Muscle tension", ["Light touch","Sound","Blood glucose"], "Golgi tendon organs sense tension and mediate inverse stretch reflexes."),
q("Upper motor neuron lesions typically produce which sign?", "Spasticity with exaggerated reflexes", ["Flaccidity with absent reflexes only","Loss of all sensation","Pure autonomic failure"], "Loss of descending inhibition causes hyperreflexia and spasticity."),
q("A patient with poliomyelitis has flaccid paralysis and fasciculations. Which neurons are damaged?", "Anterior horn cells", ["Posterior column neurons","Cerebellar Purkinje cells","Thalamic relay cells"], "Polio damages lower motor neurons in anterior horn.", True),
q("Sacral spinal segments are important for which reflex?", "Micturition reflex", ["Pupillary light reflex","Corneal reflex","Vestibulo-ocular reflex"], "Sacral cord circuits coordinate bladder emptying."),
q("A complete spinal cord transection initially causes loss of reflexes below the lesion. This phase is called what?", "Spinal shock", ["Decerebrate rigidity","Clonus only","Akathisia"], "Spinal shock is transient areflexia after acute cord injury.", True),
]),
("cerebellum-basal-ganglia","Physiological Anatomy, Functions and Lesions of Cerebellum and Basal Ganglia",2,[
q("The cerebellum is especially important for which function?", "Coordination of movement", ["Initiation of menstruation","Formation of CSF only","Conscious pain perception"], "The cerebellum coordinates timing, force and accuracy of movements."),
q("Which cerebellar lobe is most related to balance and eye movements?", "Flocculonodular lobe", ["Occipital lobe","Insula","Temporal pole"], "The vestibulocerebellum includes flocculonodular lobe."),
q("Basal ganglia participate mainly in regulation of what?", "Motor planning and movement selection", ["Urine concentration","Gas exchange","Bile storage"], "Basal ganglia modulate initiation and scaling of movements."),
q("A patient with intention tremor and dysmetria most likely has lesion of which structure?", "Cerebellum", ["Anterior pituitary","Adrenal cortex","Dorsal root ganglion only"], "Cerebellar disease causes ataxia, intention tremor and past-pointing.", True),
q("Parkinsonism is classically due to dopamine deficiency in which pathway?", "Nigrostriatal pathway", ["Optic pathway","Spinothalamic tract","HPA axis"], "Loss of substantia nigra dopamine affects striatal circuits."),
q("Which basal ganglia disorder is associated with choreiform movements?", "Huntington disease", ["Myasthenia gravis","Cushing syndrome","Diabetes insipidus"], "Huntington disease causes chorea from striatal degeneration."),
q("Cerebellar lesions usually affect which side of body?", "Ipsilateral side", ["Contralateral side only","Both eyes only","No motor side"], "Cerebellar output crosses twice, so deficits are ipsilateral."),
q("A patient walks with broad-based staggering gait and cannot perform heel-shin test. Which deficit is present?", "Cerebellar ataxia", ["Sensory aphasia","Lower motor neuron paralysis","Pure autonomic failure"], "Limb and gait ataxia indicate cerebellar dysfunction.", True),
q("The direct basal ganglia pathway generally facilitates what?", "Movement", ["Sleep only","Acid secretion","Auditory transduction"], "Direct pathway promotes thalamocortical motor activity."),
q("Resting tremor, rigidity and bradykinesia point toward which condition?", "Parkinson disease", ["Cerebellar tumour only","Tabes dorsalis","Brown-Sequard syndrome"], "These are classic parkinsonian motor features.", True),
]),
("thalamus-hypothalamus","Physiological Anatomy, Functions and Lesions of Thalamus and Hypothalamus",3,[
q("The thalamus acts mainly as a relay station for which information?", "Sensory signals to cerebral cortex", ["Renal filtrate","Bile salts","Anterior pituitary blood only"], "Most sensory pathways relay in thalamus before cortex."),
q("Which sensory modality reaches cortex without obligatory thalamic relay first?", "Olfaction", ["Pain","Touch","Vision"], "Olfaction is the major exception to initial thalamic relay."),
q("The hypothalamus is a major centre for regulation of which function?", "Autonomic and endocrine homeostasis", ["Voluntary hand grip only","Lens accommodation only","Platelet formation"], "Hypothalamus links autonomic, endocrine and behavioural responses."),
q("A lesion of lateral hypothalamus causes which feeding abnormality?", "Aphagia", ["Hyperphagia","Vomiting only","Polyphagia with obesity"], "Lateral hypothalamus is a feeding centre."),
q("The supraoptic and paraventricular nuclei synthesize which hormones?", "ADH and oxytocin", ["TSH and ACTH","Insulin and glucagon","Gastrin and secretin"], "These hypothalamic nuclei produce posterior pituitary hormones."),
q("A patient with central diabetes insipidus has damage to which functional system?", "Hypothalamo-neurohypophyseal ADH system", ["Basal ganglia direct pathway","Cerebellar vermis","Auditory cortex"], "Loss of ADH secretion causes water diuresis.", True),
q("The hypothalamus regulates body temperature using input from which receptors?", "Thermoreceptors", ["Photoreceptors only","Baroreceptors only","Osmotic receptors only"], "Hypothalamic centres integrate thermal signals."),
q("Damage to ventromedial hypothalamus may cause which clinical feature?", "Hyperphagia and obesity", ["Aphagia only","Blindness","Flaccid paralysis"], "Ventromedial hypothalamus is a satiety centre.", True),
q("Thalamic pain syndrome may follow vascular lesion involving which structure?", "Thalamus", ["Cerebellar cortex","Anterior horn","Neuromuscular junction"], "Thalamic lesions can cause severe contralateral pain."),
q("A patient has contralateral sensory loss after a small stroke in a relay nucleus. Which structure is implicated?", "Thalamus", ["Pons respiratory centre","Pituitary posterior lobe","Adrenal medulla"], "Thalamic relay lesions impair cortical sensory input.", True),
]),
("cerebral-cortex-white-matter","Physiological Anatomy and Functions of Cerebral Cortex and White Matter of Cerebrum",4,[
q("The primary motor cortex is located mainly in which gyrus?", "Precentral gyrus", ["Postcentral gyrus","Superior temporal gyrus","Cingulate gyrus"], "Area 4 in precentral gyrus is primary motor cortex."),
q("The primary somatosensory cortex is located mainly in which gyrus?", "Postcentral gyrus", ["Precentral gyrus","Inferior frontal gyrus","Uncus"], "Areas 3, 1 and 2 lie in postcentral gyrus."),
q("Broca area is important for which function?", "Motor speech production", ["Auditory transduction","Smell identification only","Balance"], "Broca area programs expressive speech."),
q("A right-handed patient understands speech but speaks nonfluently after left inferior frontal lesion. Which aphasia is likely?", "Broca aphasia", ["Wernicke aphasia","Conduction aphasia only","Global sensory loss"], "Broca aphasia causes nonfluent speech with relatively preserved comprehension.", True),
q("Wernicke area is mainly involved in which function?", "Language comprehension", ["Voluntary micturition only","Milk ejection","Visual accommodation"], "Wernicke area supports comprehension of language."),
q("Association cortex is important for what?", "Integration and interpretation of information", ["Simple spinal reflex only","Hormone filtration","Bile concentration"], "Association areas combine inputs for higher processing."),
q("The corpus callosum mainly connects what?", "Right and left cerebral hemispheres", ["Cerebellum and spinal cord only","Pituitary and thyroid","Kidney and adrenal"], "Corpus callosum is the major commissural fibre tract."),
q("A patient with fluent but meaningless speech and poor comprehension has lesion of which area?", "Wernicke area", ["Primary motor cortex leg area","Cerebellar flocculus","Hypothalamic supraoptic nucleus"], "Wernicke aphasia causes fluent aphasia with impaired comprehension.", True),
q("Internal capsule lesions commonly produce dense contralateral weakness because they affect which fibres?", "Corticospinal fibres", ["Olfactory fila only","Optic rods","Postganglionic sympathetic fibres"], "Motor fibres are compact in the internal capsule."),
q("Sudden lacunar infarct in internal capsule causing pure motor hemiparesis damages which pathway?", "Descending corticospinal pathway", ["Dorsal column in medulla","Vestibular apparatus","Enteric plexus"], "Internal capsule stroke can interrupt corticospinal fibres.", True),
]),
("autonomic-nervous-system","Autonomic Nervous System",5,[
q("Preganglionic sympathetic neurons arise mainly from which spinal segments?", "Thoracolumbar segments", ["Craniosacral segments","Cervical cord only","Sacral cord only"], "Sympathetic outflow is thoracolumbar."),
q("Parasympathetic outflow is described as what?", "Craniosacral", ["Thoracolumbar","Purely lumbar","Purely cervical"], "Parasympathetic fibres arise from brainstem nuclei and sacral cord."),
q("The neurotransmitter at all autonomic ganglia is what?", "Acetylcholine", ["Noradrenaline","Dopamine only","GABA"], "Preganglionic autonomic neurons release acetylcholine onto nicotinic receptors."),
q("A patient with Horner syndrome has ptosis, miosis and anhidrosis due to interruption of which pathway?", "Sympathetic supply to head", ["Parasympathetic supply to bladder","Somatic motor supply to face","Auditory pathway"], "Horner syndrome follows sympathetic pathway damage.", True),
q("Most postganglionic sympathetic neurons release which neurotransmitter?", "Noradrenaline", ["Acetylcholine only","Glutamate only","Serotonin"], "Most sympathetic postganglionic fibres are adrenergic."),
q("Sweat glands are an exception because their sympathetic postganglionic fibres release what?", "Acetylcholine", ["Dopamine","Glycine","Histamine"], "Eccrine sweat glands receive cholinergic sympathetic fibres."),
q("Parasympathetic stimulation of heart primarily causes what?", "Decreased heart rate", ["Marked bronchodilation","Pupil dilation","Sweating"], "Vagal activity slows SA node firing."),
q("A patient with autonomic neuropathy develops postural dizziness. Which reflex is impaired?", "Baroreceptor-mediated sympathetic response", ["Stretch reflex only","Pupillary accommodation only","Swallowing oral phase"], "Autonomic failure impairs vasoconstriction on standing.", True),
q("Alpha-1 receptor stimulation usually causes which vascular response?", "Vasoconstriction", ["Vasodilation always","No effect","Capillary rupture"], "Alpha-1 activation contracts vascular smooth muscle."),
q("Organophosphate poisoning causes salivation, lacrimation and bronchospasm by increasing which neurotransmitter?", "Acetylcholine", ["Noradrenaline","Dopamine","Histamine only"], "Acetylcholinesterase inhibition increases acetylcholine at muscarinic synapses.", True),
]),
("meninges-csf-bbb-cbf","Meninges, Cerebrospinal Fluid, Blood-Brain Barrier and Cerebral Blood Flow",6,[
q("Cerebrospinal fluid is produced mainly by which structure?", "Choroid plexus", ["Pineal gland","Basal ganglia","Dorsal root ganglion"], "Choroid plexus forms most CSF."),
q("CSF is absorbed mainly through which structures?", "Arachnoid villi", ["Choroid plexus only","Pia mater","Ependymal cilia only"], "Arachnoid villi/granulations drain CSF into venous sinuses."),
q("The blood-brain barrier is formed importantly by tight junctions between which cells?", "Brain capillary endothelial cells", ["RBCs","Schwann cells","Platelets"], "BBB depends on tight junctions of CNS capillary endothelium."),
q("A patient with communicating hydrocephalus has impaired CSF absorption. Which site is most likely affected?", "Arachnoid granulations", ["Neuromuscular junction","Semicircular canals","Adrenal cortex"], "Communicating hydrocephalus often reflects defective CSF absorption.", True),
q("Cerebral blood flow is strongly increased by rise in arterial level of which gas?", "Carbon dioxide", ["Oxygen in hyperoxia","Nitrogen","Helium"], "CO2 is a potent cerebral vasodilator."),
q("The dura mater is the outer meningeal layer and contains which venous structures?", "Dural venous sinuses", ["Portal veins","Pulmonary veins","Renal veins"], "Dural folds enclose venous sinuses."),
q("Lumbar puncture samples CSF from which space?", "Subarachnoid space", ["Epidural fat only","Subdural potential space","Central canal only"], "CSF circulates in the subarachnoid space."),
q("A head injury tears bridging veins causing crescent-shaped bleed. Which haemorrhage is likely?", "Subdural haemorrhage", ["Epidural haemorrhage","Intracerebral calcification","Subarachnoid only"], "Bridging vein rupture causes subdural bleeding.", True),
q("BBB permeability is relatively limited for which type of substance?", "Large polar molecules", ["Lipid-soluble gases","Oxygen","Carbon dioxide"], "Large hydrophilic molecules cross BBB poorly."),
q("Severe hypercapnia increases intracranial pressure mainly by causing which change?", "Cerebral vasodilation", ["Cerebral vasoconstriction","CSF absence","Dural calcification"], "CO2-induced vasodilation increases cerebral blood volume.", True),
]),
("synaptic-transmission","Synaptic Transmission",7,[
q("Chemical synaptic transmission begins with opening of which presynaptic channels?", "Voltage-gated calcium channels", ["Voltage-gated chloride channels only","Aquaporin channels","Nuclear pores"], "Calcium influx triggers vesicle fusion."),
q("Neurotransmitter vesicle fusion releases transmitter by which process?", "Exocytosis", ["Endocytosis","Osmosis","Filtration"], "Synaptic vesicles release contents by exocytosis."),
q("An excitatory postsynaptic potential usually brings membrane potential closer to what?", "Threshold", ["Potassium equilibrium only","Absolute zero","Resting chloride potential only"], "EPSPs depolarize postsynaptic membrane toward threshold."),
q("Botulinum toxin causes paralysis by blocking release of which neurotransmitter?", "Acetylcholine", ["Dopamine","GABA","Substance P"], "Botulinum toxin prevents acetylcholine release at neuromuscular junctions.", True),
q("Inhibitory postsynaptic potentials commonly involve entry of chloride or exit of which ion?", "Potassium", ["Calcium only","Sodium only","Iron"], "IPSPs hyperpolarize by chloride influx or potassium efflux."),
q("Temporal summation occurs when inputs arrive close together in what dimension?", "Time", ["Space only","Blood flow","Hormone axis"], "Repeated inputs at one synapse can summate over time."),
q("Spatial summation refers to addition of inputs from what?", "Multiple synapses", ["One receptor over time only","One axon alone","One hormone gland"], "Inputs at several synapses combine spatially."),
q("A patient with myasthenia gravis has fatigable weakness due to antibodies against which receptor?", "Nicotinic acetylcholine receptor", ["GABA-A receptor","Dopamine D2 receptor","Adrenergic beta receptor"], "Myasthenia reduces functional postsynaptic nicotinic receptors.", True),
q("Synaptic delay is mainly due to which event?", "Neurotransmitter release and receptor activation", ["Saltatory conduction only","Axonal myelination","Blood flow"], "Chemical transmission requires vesicle release, diffusion and receptor binding."),
q("Organophosphates prolong synaptic acetylcholine action by inhibiting which enzyme?", "Acetylcholinesterase", ["Monoamine oxidase only","Carbonic anhydrase","Tyrosinase"], "AChE inhibition prevents acetylcholine breakdown.", True),
]),
("somatosensory-system","Somatosensory System",8,[
q("First-order somatosensory neuron cell bodies are located mainly in which structure?", "Dorsal root ganglia", ["Anterior horn","Thalamus","Cerebellar cortex"], "Primary sensory neuron cell bodies lie in dorsal root ganglia."),
q("Two-point discrimination is best developed in which body region?", "Fingertips", ["Back","Thigh","Calf"], "High receptor density and cortical representation improve discrimination."),
q("Pain receptors are usually which type of receptors?", "Free nerve endings", ["Muscle spindles","Rods","Hair cells"], "Nociceptors are free nerve endings."),
q("A patient with tabes dorsalis has loss of vibration and position sense. Which pathway is damaged?", "Dorsal columns", ["Spinothalamic tract only","Corticospinal tract only","Vestibulospinal tract"], "Posterior column damage impairs proprioception and vibration.", True),
q("Fast pain is carried mainly by which fibres?", "A-delta fibres", ["C fibres only","A-alpha motor fibres","B autonomic fibres"], "A-delta fibres carry sharp, fast pain."),
q("Slow dull pain is carried mainly by which fibres?", "C fibres", ["A-beta fibres only","A-alpha fibres","Preganglionic B fibres only"], "Unmyelinated C fibres carry slow pain."),
q("Referred pain occurs because visceral and somatic afferents converge where?", "Same spinal segments", ["Same adrenal gland","Same muscle spindle","Same vestibular nucleus"], "Convergence in spinal cord produces mislocalization."),
q("A myocardial infarction causing pain in left arm is an example of what?", "Referred pain", ["Phantom limb only","Neuropathic itch","Cerebellar ataxia"], "Cardiac visceral afferents converge with somatic segments.", True),
q("Adaptation of sensory receptors means reduced response during what?", "Sustained stimulus", ["Absent stimulus","Only sleep","Only exercise"], "Many receptors reduce firing during continuous stimulation."),
q("Burning pain after nerve injury with allodynia suggests which pain type?", "Neuropathic pain", ["Pure physiological itch","Normal proprioception","Receptor adaptation only"], "Nerve injury can cause abnormal pain processing.", True),
]),
("somatic-motor-system","Somatic Motor System",9,[
q("The corticospinal tract is most important for which type of movement?", "Skilled voluntary movement", ["Sweating","Pupillary constriction only","Gut peristalsis"], "Pyramidal tract controls fine voluntary movement."),
q("Lower motor neuron lesion produces which sign?", "Flaccid paralysis", ["Spasticity with clonus only","Hyperreflexia only","Babinski sign only"], "LMN lesions cause weakness, atrophy, fasciculations and reduced reflexes."),
q("Babinski sign usually indicates lesion of which system?", "Corticospinal tract", ["Posterior column only","Cerebellar cortex","Peripheral sensory receptor"], "Extensor plantar response indicates upper motor neuron dysfunction."),
q("A stroke involving motor cortex causes weakness on which side?", "Contralateral side", ["Ipsilateral side only","No side preference","Only face ipsilaterally"], "Corticospinal fibres decussate, producing contralateral weakness above decussation.", True),
q("Gamma motor neurons regulate sensitivity of which receptor?", "Muscle spindle", ["Golgi tendon organ only","Pacinian corpuscle","Rod cell"], "Gamma efferents adjust intrafusal fibre tension."),
q("Motor unit means one motor neuron and what?", "All muscle fibres it innervates", ["One sarcomere only","One tendon","One fascial sheath"], "A motor unit includes a motor neuron and its muscle fibres."),
q("Decerebrate rigidity is associated with increased activity of which extensor facilitatory pathway?", "Vestibulospinal pathway", ["Optic pathway","Dorsal column","Olfactory pathway"], "Brainstem imbalance can increase extensor tone."),
q("A patient with acute anterior horn cell injury shows fasciculations because of damage to which component?", "Lower motor neuron", ["Upper motor neuron only","Thalamic neuron","Cerebellar basket cell"], "Fasciculations arise from diseased LMNs.", True),
q("The final common pathway for somatic motor output is which neuron?", "Alpha motor neuron", ["Purkinje cell","Pyramidal neuron only","Thalamic relay neuron"], "Alpha motor neurons directly innervate extrafusal muscle."),
q("Clasp-knife rigidity is typically associated with which lesion type?", "Upper motor neuron lesion", ["Lower motor neuron lesion","Myopathy only","Peripheral sensory receptor loss"], "UMN lesions can cause spasticity with clasp-knife response.", True),
]),
("limbic-system","Limbic System and Physiology of Emotional, Behavioural and Motivational Mechanisms",10,[
q("The limbic system is especially involved in which functions?", "Emotion, motivation and memory", ["Renal filtration","Pulmonary diffusion","Bile secretion"], "Limbic circuits regulate emotional behaviour and memory."),
q("The hippocampus is particularly important for which process?", "Formation of new declarative memories", ["Primary motor output","Pupil constriction only","CSF absorption"], "Hippocampus is essential for memory consolidation."),
q("The amygdala is strongly associated with which emotional response?", "Fear and threat processing", ["Urine concentration","Visual acuity only","Milk production"], "Amygdala participates in fear and emotional salience."),
q("Bilateral hippocampal damage causes prominent inability to form new memories. What is this called?", "Anterograde amnesia", ["Broca aphasia","Ataxia","Hyperalgesia"], "Hippocampal damage impairs new memory formation.", True),
q("Reward pathways of brain prominently use which neurotransmitter?", "Dopamine", ["Acetylcholine at NMJ only","Bile salts","Calcitonin"], "Mesolimbic dopamine pathways participate in reward."),
q("Papez circuit is classically related to which function?", "Emotion", ["Glomerular filtration","Hearing only","Gastric emptying"], "Papez circuit is a limbic circuit linked with emotion."),
q("Septal area stimulation is associated with which behavioural state?", "Pleasure/reward", ["Complete paralysis","Blindness","Tetany"], "Septal and related limbic areas participate in reward."),
q("A patient with bilateral amygdala damage shows reduced fear responses. Which structure is affected?", "Amygdala", ["Pons","Anterior horn","Thyroid gland"], "Amygdala lesions blunt fear and threat responses.", True),
q("Hypothalamus links limbic activity to which outputs?", "Autonomic and endocrine responses", ["Only skeletal reflexes","Only visual reflexes","Only renal filtration"], "Hypothalamus expresses emotional states through autonomic/endocrine changes."),
q("Sudden rage with autonomic activation after hypothalamic-limbic disturbance reflects altered control of what?", "Emotional behaviour", ["CSF production only","Oxygen diffusion","Bile storage"], "Limbic-hypothalamic circuits regulate affective behaviour.", True),
]),
("reticular-sleep","Reticular Formation, Electrical Activity of the Brain, and Alert Behaviour and Sleep",11,[
q("The ascending reticular activating system is important for maintaining what?", "Wakefulness and alertness", ["Renal blood flow","Bile secretion","Bone mineralization"], "ARAS supports cortical arousal."),
q("Alpha rhythm on EEG is most associated with which state?", "Relaxed wakefulness with eyes closed", ["Deep coma only","REM sleep only","Generalized seizure only"], "Alpha waves are prominent in relaxed awake adults with eyes closed."),
q("Delta waves are most prominent during which state?", "Deep non-REM sleep", ["Alert calculation","Exercise","Pain perception only"], "Slow delta activity occurs in deep NREM sleep."),
q("A comatose patient after brainstem injury likely has damage to which arousal system?", "Reticular activating system", ["Enteric plexus","Adrenal cortex","Posterior column only"], "Brainstem reticular formation is essential for consciousness.", True),
q("REM sleep is characterized by rapid eye movements and what muscle tone pattern?", "Marked skeletal muscle atonia", ["Generalized rigidity","Sustained clonus","Normal voluntary movement"], "REM sleep has vivid dreaming and muscle atonia."),
q("Sleep spindles are characteristic of which non-REM sleep stage?", "Stage N2", ["Stage N1 only","Stage N3 only","REM only"], "N2 sleep includes spindles and K complexes."),
q("The suprachiasmatic nucleus is important for regulation of what?", "Circadian rhythm", ["Spinal reflex arc","CSF absorption","Spermatogenesis only"], "SCN is the master circadian clock."),
q("A patient with narcolepsy has sudden sleep attacks and cataplexy related to deficiency of which peptide?", "Orexin/hypocretin", ["Insulin","PTH","Gastrin"], "Narcolepsy is linked to orexin neuron loss.", True),
q("Generalized tonic-clonic seizure shows abnormal hypersynchronous activity in which tissue?", "Cerebral cortex", ["Renal cortex","Adrenal medulla","Gastric mucosa"], "Seizures reflect abnormal cortical electrical discharges."),
q("Obstructive sleep apnoea causes daytime sleepiness mainly by repeated sleep fragmentation and what?", "Intermittent hypoxia", ["Hypercalcaemia","Low bile salts","High intrinsic factor"], "Apnoeic episodes fragment sleep and reduce oxygenation.", True),
]),
("higher-functions","Some Higher Functions of Nervous System",12,[
q("Learning is best described as acquisition of new information that produces what?", "Relatively lasting behavioural change", ["Immediate reflex only","Urine formation","Bile release"], "Learning changes behaviour or capability through experience."),
q("Memory consolidation depends strongly on which temporal lobe structure?", "Hippocampus", ["Primary visual cortex only","Anterior horn","Cochlea"], "Hippocampus is central to consolidation of declarative memory."),
q("Dominant hemisphere language areas are most often located in which hemisphere?", "Left hemisphere", ["Right hemisphere in all persons","Cerebellum","Both occipital poles only"], "Language dominance is usually left-sided, especially in right-handed people."),
q("A patient cannot repeat phrases despite fluent speech and fair comprehension. Which aphasia is suggested?", "Conduction aphasia", ["Broca aphasia only","Pure motor paralysis","Global amnesia"], "Conduction aphasia classically impairs repetition.", True),
q("Prefrontal cortex is important for which higher function?", "Planning and executive control", ["CSF secretion","Primary smell receptor activity","Spinal stretch reflex"], "Prefrontal areas support judgement, planning and working memory."),
q("Procedural memory for skills depends importantly on basal ganglia and which structure?", "Cerebellum", ["Adrenal gland","Thyroid gland","Kidney"], "Motor skill learning involves basal ganglia and cerebellum."),
q("Apraxia means impaired skilled movement despite preserved what?", "Basic motor power", ["All sensation absent","Vision absent","Consciousness absent"], "Apraxia is failure of learned motor acts not explained by weakness."),
q("A patient neglects the left side after right parietal stroke. Which deficit is present?", "Hemispatial neglect", ["Broca aphasia","Narcolepsy","Spinal shock"], "Non-dominant parietal lesions can cause contralateral neglect.", True),
q("Agnosia means inability to recognize stimuli despite intact what?", "Primary sensation", ["All memory","All language","All movement"], "Agnosia is impaired recognition with basic sensory function preserved."),
q("A patient recognizes objects by touch only when looking at them, despite normal primary sensation. Which cortical function is impaired?", "Stereognosis", ["Pupillary reflex","Stretch reflex","Osmoregulation"], "Astereognosis reflects parietal association cortex dysfunction.", True),
]),
]

def build():
    out=[]
    for slug,topic,order,rows in TOPICS:
        for i,row in enumerate(rows,1):
            shift=(order+i)%4
            opts=row["options"][shift:]+row["options"][:shift]
            ans=row["answer"]
            out.append({**BASE,**row,"id":f"physiology-nervous-{slug}-{i:02d}","topic":topic,"topicTitle":topic,"topicOrder":order,"options":opts,"answerIndex":opts.index(ans),"answer":ans})
    return out

def validate(qs):
    if len(qs)!=120: raise ValueError(f"Expected 120, got {len(qs)}")
    if len({q["id"] for q in qs})!=120: raise ValueError("Duplicate IDs")
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
