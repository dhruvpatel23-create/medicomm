import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
BASE = {
    "subjectId": "pharmacology",
    "subjectTitle": "Pharmacology",
    "chapterTitle": "Neuropharmacology",
    "source": "ai",
    "imageUrls": [],
}


def item(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    (
        "neurotransmission-autonomic-somatic",
        "Neurotransmission: The Autonomic and Somatic Motor Nervous Systems",
        [
            item("A patient stands suddenly and arterial pressure falls. The compensatory reflex tachycardia is best explained by increased firing of which efferent pathway?", "Sympathetic postganglionic norepinephrine release at beta-1 receptors", ["Parasympathetic acetylcholine release at M2 receptors", "Somatic motor acetylcholine release at nicotinic receptors", "Adrenal histamine release at H1 receptors"], "Baroreceptor unloading increases sympathetic outflow; norepinephrine stimulates cardiac beta-1 receptors to raise rate and contractility."),
            item("Botulinum toxin improves focal dystonia because it prevents which presynaptic event?", "SNARE-dependent fusion of acetylcholine vesicles", ["Choline transport into the nerve terminal", "Acetylcholine breakdown in the synaptic cleft", "Nicotinic receptor channel opening"], "Botulinum toxins cleave SNARE proteins, blocking acetylcholine vesicle fusion and causing local chemodenervation."),
            item("A drug that blocks neuronal choline uptake would most directly reduce which process?", "Acetylcholine synthesis in cholinergic nerve terminals", ["Norepinephrine storage in vesicles", "Dopamine receptor coupling to G proteins", "GABA reuptake by astrocytes"], "High-affinity choline uptake is rate limiting for acetylcholine synthesis in many cholinergic terminals."),
            item("After a spinal cord injury, a patient loses voluntary movement but the neuromuscular junction itself is intact. The transmitter at that junction is:", "Acetylcholine acting on nicotinic Nm receptors", ["Norepinephrine acting on alpha-1 receptors", "Dopamine acting on D2 receptors", "Serotonin acting on 5-HT3 receptors"], "Somatic motor neurons release acetylcholine onto muscle-type nicotinic receptors."),
            item("A patient has dry mouth, urinary retention, tachycardia, and blurred near vision after taking an over-the-counter sleep aid. Which receptor family is being blocked?", "Muscarinic acetylcholine receptors", ["Nicotinic Nm receptors", "Alpha-2 adrenergic receptors", "GABA-A receptors"], "The anticholinergic toxidrome is caused by muscarinic blockade at glands, bladder, eye, heart, and CNS."),
            item("Reserpine lowers blood pressure but can cause depression because it inhibits which target?", "Vesicular monoamine transporter", ["Acetylcholinesterase", "Muscarinic M3 receptor", "Voltage-gated sodium channel"], "VMAT inhibition depletes norepinephrine, dopamine, and serotonin from storage vesicles."),
            item("A patient receiving a ganglion blocker develops loss of both sympathetic and parasympathetic reflexes. Which receptor is blocked?", "Nicotinic Nn receptor", ["Muscarinic M2 receptor", "Beta-2 receptor", "Nicotinic Nm receptor"], "Autonomic ganglia use neuronal nicotinic receptors, distinct from muscle nicotinic receptors at the neuromuscular junction."),
            item("A drug causes mydriasis without cycloplegia by contracting the radial iris muscle. Which receptor mediates this?", "Alpha-1 adrenergic receptor", ["Muscarinic M3 receptor", "Beta-1 adrenergic receptor", "Nicotinic Nm receptor"], "Alpha-1 activation contracts radial dilator muscle; muscarinic blockade causes mydriasis with cycloplegia."),
            item("A patient with autonomic failure has severe orthostatic hypotension but preserved skeletal muscle strength. Which structure is most selectively impaired?", "Autonomic efferent control of vascular tone", ["Neuromuscular transmission to skeletal muscle", "Cortical motor neuron action potentials", "Muscle sarcoplasmic calcium release"], "Orthostatic hypotension reflects loss of sympathetic vasoconstrictor responses, not necessarily somatic motor failure."),
            item("An alpha-2 agonist reduces sympathetic outflow from the CNS. The immediate pharmacologic logic is:", "Presynaptic inhibition of norepinephrine release and reduced central sympathetic tone", ["Direct activation of adrenal epinephrine secretion", "Nicotinic blockade at the neuromuscular junction", "Irreversible inhibition of acetylcholinesterase"], "Alpha-2 receptors function as inhibitory autoreceptors and also reduce central sympathetic signaling."),
        ],
    ),
    (
        "muscarinic-agonists-antagonists",
        "Muscarinic Receptor Agonists and Antagonists",
        [
            item("A postoperative patient has urinary retention without mechanical obstruction. Which drug can increase detrusor contraction with minimal nicotinic action?", "Bethanechol", ["Atropine", "Ipratropium", "Pralidoxime"], "Bethanechol is a muscarinic agonist used for nonobstructive urinary retention and ileus."),
            item("A patient with Sjogren syndrome needs treatment for severe xerostomia but has uncontrolled asthma. Why is pilocarpine risky?", "M3 activation can increase bronchial secretions and bronchoconstriction", ["It blocks beta-2 receptors irreversibly", "It depletes vesicular norepinephrine", "It inhibits carbonic anhydrase"], "Muscarinic agonists stimulate exocrine secretion and can worsen bronchospasm in susceptible patients."),
            item("A child ingests jimsonweed and becomes febrile, flushed, delirious, tachycardic, and dry. The best mechanistic label is:", "Central and peripheral muscarinic receptor blockade", ["Excess acetylcholine at nicotinic receptors", "Mu-opioid receptor activation", "Beta-2 receptor activation"], "Antimuscarinic poisoning causes dry skin, hyperthermia, mydriasis, urinary retention, tachycardia, and delirium."),
            item("A patient receives atropine for symptomatic sinus bradycardia. The heart rate rises because atropine blocks:", "Vagal M2 effects on the SA node", ["Beta-1 receptors in the ventricle", "Alpha-1 receptors in the vasculature", "Nicotinic receptors in skeletal muscle"], "Muscarinic M2 blockade removes parasympathetic slowing of the sinus node."),
            item("A patient with narrow-angle glaucoma takes a strong antimuscarinic and develops painful red eye with halos. What caused the attack?", "Mydriasis narrowing the iridocorneal angle and obstructing aqueous outflow", ["Miosis closing the trabecular meshwork", "Beta-1 blockade reducing ciliary secretion", "Dopamine release in the retina"], "Antimuscarinic mydriasis can precipitate acute angle closure in anatomically susceptible eyes."),
            item("Why is ipratropium useful in COPD with fewer systemic anticholinergic effects than atropine?", "Its quaternary structure limits systemic absorption and CNS entry", ["It selectively activates nicotinic receptors", "It is an irreversible muscarinic antagonist", "It releases endogenous corticosteroid"], "Inhaled quaternary antimuscarinics act mainly in the airways and poorly cross membranes."),
            item("Scopolamine prevents motion sickness mainly because it:", "Blocks muscarinic signaling in vestibular pathways and the vomiting center", ["Stimulates dopamine receptors in the basal ganglia", "Blocks peripheral beta receptors", "Reactivates acetylcholinesterase"], "Scopolamine has prominent CNS antimuscarinic activity and is useful for motion sickness."),
            item("An older patient started oxybutynin and soon developed confusion and constipation. Which receptor effect links both adverse effects?", "Muscarinic blockade in CNS and gut", ["Alpha-1 blockade", "D2 blockade", "Nicotinic Nm activation"], "Antimuscarinics can impair cognition and reduce GI motility, especially in older patients."),
            item("A patient with organophosphate poisoning receives atropine. Which finding best tells you atropine dosing is becoming adequate?", "Bronchial secretions and wheeze improve", ["Plasma cholinesterase normalizes immediately", "Muscle fasciculations stop completely", "Pupils become maximally constricted"], "Atropine treats muscarinic effects; drying bronchial secretions is a key clinical endpoint."),
            item("A patient with BPH is given a drug that worsens urinary hesitancy and causes dry mouth. Which drug class most likely caused this?", "Antimuscarinic agent", ["Alpha-1 blocker", "Cholinesterase inhibitor", "Beta-2 agonist"], "Muscarinic blockade relaxes the detrusor and can precipitate urinary retention in bladder outlet obstruction."),
        ],
    ),
    (
        "anticholinesterase-inhibitors-reactivators",
        "Anticholinesterase Inhibitors and Reactivators",
        [
            item("A patient with myasthenia gravis improves after pyridostigmine. Which synaptic change explains the benefit?", "More acetylcholine persists at nicotinic Nm receptors", ["More dopamine reaches D2 receptors", "Less acetylcholine is released from motor neurons", "Beta-1 receptors become sensitized"], "Acetylcholinesterase inhibition increases acetylcholine at the neuromuscular junction."),
            item("A patient has antimuscarinic delirium from atropine overdose. Which acetylcholinesterase inhibitor can enter the CNS and reverse symptoms?", "Physostigmine", ["Neostigmine", "Edrophonium", "Pyridostigmine"], "Physostigmine is tertiary and crosses the blood-brain barrier; quaternary agents have poor CNS entry."),
            item("A farmer exposed to organophosphate has miosis, bronchorrhea, bradycardia, fasciculations, and weakness. Atropine is started. What should pralidoxime add?", "Reactivation of acetylcholinesterase at nicotinic and muscarinic synapses before aging", ["Direct beta-2 bronchodilation", "Permanent muscarinic receptor blockade", "Inhibition of acetylcholine synthesis"], "Pralidoxime can remove the phosphate from acetylcholinesterase if given before aging, improving nicotinic weakness as well as cholinergic excess."),
            item("After nerve-agent exposure, delayed pralidoxime is ineffective. The best explanation is:", "Aging makes the phosphorylated enzyme resistant to oxime reactivation", ["Atropine destroys pralidoxime", "Nicotinic receptors are genetically absent", "Acetylcholine synthesis stops permanently"], "Aged organophosphate-enzyme complexes cannot be reactivated by oximes."),
            item("A myasthenic patient becomes weak with diarrhea, sweating, salivation, and miosis after increasing medication. The most likely problem is:", "Cholinergic crisis from excessive acetylcholinesterase inhibition", ["Myasthenic crisis from too little drug", "Serotonin syndrome", "Neuroleptic malignant syndrome"], "Weakness plus muscarinic excess favors cholinergic crisis over undertreated myasthenia."),
            item("Neostigmine is paired with glycopyrrolate after surgery. What is the purpose of the antimuscarinic co-drug?", "Prevent bradycardia and secretions while neostigmine reverses nondepolarizing blockade", ["Increase acetylcholine breakdown", "Block skeletal muscle nicotinic receptors", "Induce hepatic metabolism"], "Neostigmine increases acetylcholine at muscarinic and nicotinic sites; glycopyrrolate limits unwanted muscarinic effects."),
            item("A patient with Alzheimer disease receives donepezil. The intended symptomatic effect depends on:", "Increasing central cholinergic transmission", ["Depleting central dopamine", "Blocking NMDA receptors irreversibly", "Activating peripheral alpha-1 receptors"], "Donepezil inhibits acetylcholinesterase in the CNS and can modestly improve cognition or function."),
            item("Which adverse effect is most expected from rivastigmine therapy?", "Nausea, vomiting, and bradycardia from cholinergic excess", ["Severe mydriasis and urinary retention", "Profound bronchodilation", "Opioid withdrawal"], "Cholinesterase inhibitors commonly cause GI and cardiac muscarinic adverse effects."),
            item("A child ingests a carbamate insecticide and has cholinergic toxicity. Compared with many organophosphates, carbamate inhibition is often:", "Reversible and shorter acting", ["Always irreversible after aging", "Selective only for beta receptors", "Unable to affect nicotinic sites"], "Carbamates inhibit acetylcholinesterase reversibly, though severe poisoning still requires urgent supportive and antidotal care."),
            item("A patient receiving neostigmine for ileus develops bronchospasm. The mechanism is:", "Muscarinic stimulation of airway smooth muscle and secretory glands", ["Direct histamine receptor blockade", "Dopamine D2 antagonism", "Voltage-gated sodium channel block"], "Acetylcholinesterase inhibition increases acetylcholine at airway muscarinic receptors, which can worsen asthma or COPD."),
        ],
    ),
    (
        "neuromuscular-ganglia-nicotine-relaxants-spasmolytics",
        "Neuromuscular Junction and Autonomic Ganglia; Nicotine, Muscle Relaxants, and Spasmolytics",
        [
            item("A patient with pseudocholinesterase deficiency has prolonged apnea after intubation. Which drug most likely caused it?", "Succinylcholine", ["Rocuronium", "Cisatracurium", "Baclofen"], "Succinylcholine is metabolized by plasma cholinesterase; deficiency prolongs depolarizing paralysis."),
            item("After succinylcholine, a patient develops rigidity, hyperthermia, acidosis, and hyperkalemia. Which treatment directly reduces skeletal muscle calcium release?", "Dantrolene", ["Neostigmine", "Flumazenil", "Naloxone"], "Dantrolene inhibits ryanodine receptor-mediated calcium release and treats malignant hyperthermia."),
            item("A nondepolarizing neuromuscular blocker is reversed with neostigmine. Why can this restore strength?", "More acetylcholine competes with the blocker at Nm receptors", ["The blocker is chemically destroyed in plasma", "Muscle calcium channels are opened directly", "GABA-A receptors are activated"], "Nondepolarizing blockers are competitive nicotinic antagonists, so acetylcholinesterase inhibition can overcome blockade."),
            item("A trauma patient with extensive burns develops severe hyperkalemia after succinylcholine. The best explanation is:", "Upregulated extrajunctional nicotinic receptors release excess potassium when depolarized", ["Acetylcholinesterase is irreversibly inhibited", "Renal potassium secretion abruptly increases", "D2 receptors are blocked"], "Burns, denervation, and prolonged immobilization increase nicotinic receptors and make succinylcholine-associated potassium release dangerous."),
            item("Which neuromuscular blocker undergoes Hofmann elimination and is useful when organ failure limits drug clearance?", "Cisatracurium", ["Pancuronium", "Succinylcholine", "Vecuronium"], "Cisatracurium undergoes organ-independent spontaneous degradation."),
            item("A patient trying to stop smoking uses varenicline. Its benefit comes from:", "Partial agonism at alpha4beta2 nicotinic receptors", ["Irreversible muscarinic blockade", "Full mu-opioid agonism", "Direct MAO-A inhibition"], "Varenicline partially stimulates and blocks key nicotinic receptors, reducing craving and reward from cigarettes."),
            item("Baclofen helps painful flexor spasms after spinal cord injury mainly by activating:", "GABA-B receptors in the spinal cord", ["Nicotinic Nm receptors", "Muscarinic M3 receptors", "NMDA receptors"], "Baclofen is a GABA-B agonist that reduces excitatory neurotransmitter release and spinal reflex activity."),
            item("Tizanidine reduces spasticity but causes hypotension and sedation. Which mechanism explains both?", "Alpha-2 agonism decreasing excitatory motor neuron activity and sympathetic outflow", ["Beta-1 antagonism only", "Acetylcholinesterase inhibition", "COMT inhibition"], "Tizanidine is a central alpha-2 agonist; reduced sympathetic tone can lower blood pressure."),
            item("Botulinum toxin for blepharospasm causes local weakness because it:", "Prevents acetylcholine release from motor nerve terminals", ["Blocks postsynaptic acetylcholine receptors competitively", "Inhibits skeletal muscle myosin ATPase", "Stimulates spinal GABA-B receptors"], "Botulinum toxin blocks cholinergic vesicle release at the injected site."),
            item("A patient with myasthenia gravis is unusually sensitive to rocuronium. Why?", "Fewer functional nicotinic receptors reduce the safety margin for transmission", ["Excess acetylcholinesterase destroys rocuronium", "Rocuronium activates muscarinic receptors", "Dopamine depletion worsens paralysis"], "Myasthenia reduces available Nm receptors, so competitive blockade produces greater weakness."),
        ],
    ),
    (
        "adrenergic-agonists-antagonists",
        "Adrenergic Agonists and Antagonists",
        [
            item("A patient has anaphylaxis with hypotension, bronchospasm, and urticaria. Which single drug addresses the key physiology fastest?", "Intramuscular epinephrine", ["Phenylephrine", "Metoprolol", "Atropine"], "Epinephrine provides alpha-1 vasoconstriction, beta-1 cardiac support, and beta-2 bronchodilation."),
            item("A patient with pheochromocytoma is prepared for surgery. Why should alpha blockade precede beta blockade?", "Unopposed alpha stimulation can worsen hypertension if beta blockade is started first", ["Beta blockade prevents phenoxybenzamine absorption", "Alpha blockade causes fatal bronchospasm", "Beta receptors must be stimulated before surgery"], "Blocking beta receptors first can leave alpha-mediated vasoconstriction unchecked."),
            item("A man takes prazosin and faints after the first dose. The mechanism is:", "Alpha-1 blockade causing venous and arteriolar dilation", ["Beta-2 blockade causing bronchospasm", "M2 stimulation slowing the SA node", "Nicotinic blockade at ganglia"], "Alpha-1 blockers can produce a first-dose orthostatic hypotensive episode."),
            item("A patient abruptly stops clonidine and develops severe rebound hypertension. The cause is:", "Loss of central alpha-2-mediated sympathetic inhibition", ["Permanent alpha-1 receptor blockade", "Acetylcholinesterase aging", "Mu-opioid receptor withdrawal"], "Clonidine reduces central sympathetic outflow; sudden withdrawal allows a surge in adrenergic tone."),
            item("A patient with asthma and hypertension wheezes after propranolol. Which receptor blockade explains this?", "Beta-2 blockade in bronchial smooth muscle", ["Alpha-2 blockade in the CNS", "M3 blockade in bronchi", "D1 blockade in kidney"], "Nonselective beta blockers can provoke bronchospasm by blocking beta-2-mediated bronchodilation."),
            item("Dobutamine is chosen for acute decompensated heart failure with low output because it primarily:", "Stimulates beta-1 receptors to increase contractility", ["Blocks alpha-1 receptors to reduce secretions", "Activates M2 receptors to slow conduction", "Inhibits acetylcholinesterase"], "Dobutamine is a beta-1-predominant agonist used for short-term inotropic support."),
            item("Phenylephrine relieves nasal congestion but can raise blood pressure because it:", "Activates alpha-1 receptors causing vasoconstriction", ["Blocks beta-2 receptors", "Inhibits dopamine reuptake", "Stimulates muscarinic M3 receptors"], "Alpha-1 vasoconstriction shrinks nasal mucosa and increases peripheral vascular resistance."),
            item("A patient on tamsulosin has improved urinary flow with less blood pressure effect than prazosin. The reason is relative selectivity for:", "Alpha-1A receptors in prostate and bladder neck", ["Beta-1 receptors in heart", "Alpha-2 receptors in brainstem", "D2 receptors in pituitary"], "Alpha-1A selectivity targets lower urinary tract smooth muscle more than vascular alpha-1B receptors."),
            item("A beta blocker beneficial after myocardial infarction works largely by:", "Reducing cardiac oxygen demand and arrhythmogenic sympathetic effects", ["Increasing renin release", "Stimulating AV nodal conduction", "Opening skeletal muscle sodium channels"], "Beta-1 blockade lowers heart rate, contractility, renin, and arrhythmia risk."),
            item("Cocaine plus epinephrine during nasal surgery can cause severe hypertension because cocaine:", "Blocks catecholamine reuptake and amplifies adrenergic signaling", ["Destroys alpha receptors", "Inhibits acetylcholine release", "Activates GABA-A receptors"], "Cocaine inhibits norepinephrine reuptake, increasing synaptic catecholamines and pressor responses."),
        ],
    ),
    (
        "serotonin-dopamine",
        "5-Hydroxytryptamine (Serotonin) and Dopamine",
        [
            item("A migraine patient takes sumatriptan early in an attack. Its useful vascular and trigeminal effects are mainly through:", "5-HT1B/1D receptor agonism", ["5-HT3 antagonism", "D2 receptor blockade", "Alpha-1 antagonism"], "Triptans activate 5-HT1B/1D receptors, reducing cranial vasodilation and trigeminal neuropeptide release."),
            item("A chemotherapy patient receives ondansetron. The antiemetic mechanism is:", "5-HT3 receptor blockade in vagal afferents and the chemoreceptor trigger zone", ["D2 receptor activation", "M1 receptor stimulation", "Mu receptor antagonism"], "5-HT3 antagonists are effective for chemotherapy-induced nausea and vomiting."),
            item("A patient on an SSRI develops clonus, hyperreflexia, agitation, diarrhea, and fever after starting linezolid. The toxidrome reflects excess:", "Serotonin", ["Dopamine deficiency", "Acetylcholine blockade", "GABA inhibition"], "Serotonin syndrome is characterized by neuromuscular hyperactivity, autonomic instability, and altered mental status."),
            item("A man with carcinoid syndrome has flushing and diarrhea. Which mediator is central to many symptoms?", "Serotonin released from tumor cells", ["Acetylcholine from motor neurons", "Glycine from spinal interneurons", "Histamine from parietal cells only"], "Carcinoid tumors can produce serotonin and related mediators causing diarrhea and flushing."),
            item("A patient with hyperprolactinemia improves with cabergoline. The pharmacologic action is:", "D2 receptor agonism inhibiting prolactin release", ["5-HT3 receptor blockade", "Alpha-1 receptor activation", "Nicotinic receptor antagonism"], "Dopamine acting at D2 receptors suppresses prolactin secretion from lactotrophs."),
            item("Metoclopramide improves gastric emptying but causes acute dystonia. The adverse effect is due to:", "Central D2 receptor blockade", ["Peripheral beta-2 activation", "Muscarinic receptor stimulation only", "NMDA receptor antagonism"], "D2 blockade in basal ganglia pathways can cause extrapyramidal symptoms."),
            item("A patient with Parkinson disease worsens after taking a dopamine antagonist antiemetic. Which antiemetic would avoid D2 blockade?", "Ondansetron", ["Prochlorperazine", "Metoclopramide", "Haloperidol"], "Ondansetron blocks 5-HT3 receptors and does not antagonize dopamine receptors."),
            item("A patient taking ergotamine for migraine develops painful cold fingers. The toxicity is best explained by:", "Persistent vasoconstriction from serotonergic and adrenergic receptor activity", ["Pure beta-2 bronchodilation", "Muscarinic paralysis", "GABA-A activation"], "Ergot alkaloids can cause severe peripheral vasospasm."),
            item("Buspirone reduces anxiety without benzodiazepine-like sedation mainly by acting as a:", "5-HT1A partial agonist", ["GABA-A channel opener", "D2 irreversible antagonist", "Alpha-1 agonist"], "Buspirone is a 5-HT1A partial agonist with delayed anxiolytic effect and little dependence liability."),
            item("A patient on levodopa develops hallucinations and impulse-control symptoms after adding a dopamine agonist. The problem is:", "Excess dopaminergic stimulation in CNS pathways", ["Serotonin depletion in platelets", "Muscarinic blockade in the bladder", "Peripheral acetylcholine excess"], "Dopamine agonists can overstimulate mesolimbic pathways and cause hallucinations or impulse-control disorders."),
        ],
    ),
    (
        "central-neurotransmission",
        "Neurotransmission in the Central Nervous System",
        [
            item("Benzodiazepines reduce anxiety by enhancing which inhibitory synaptic current?", "GABA-A chloride channel activity", ["NMDA calcium influx", "AMPA sodium influx", "D1 cAMP signaling"], "Benzodiazepines increase the frequency of GABA-A channel opening in the presence of GABA."),
            item("Memantine is useful in Alzheimer disease because it reduces pathologic signaling through:", "NMDA glutamate receptors", ["Muscarinic M2 receptors", "Nicotinic Nm receptors", "Alpha-1 adrenergic receptors"], "Memantine is an NMDA receptor antagonist that can dampen excitotoxic glutamatergic activity."),
            item("A spinal inhibitory interneuron releases glycine. Strychnine poisoning would most likely cause:", "Convulsions from loss of inhibitory glycine receptor signaling", ["Flaccid paralysis from Nm blockade", "Miosis from M3 stimulation", "Sedation from GABA-A activation"], "Strychnine blocks glycine receptors, producing unchecked motor neuron activity and convulsions."),
            item("Caffeine increases alertness partly by antagonizing which CNS receptor?", "Adenosine receptor", ["Mu-opioid receptor", "Nicotinic Nm receptor", "Glycine receptor"], "Adenosine normally promotes sleepiness; caffeine blocks adenosine receptors."),
            item("A drug that blocks GABA reuptake can be antiseizure because it:", "Increases inhibitory GABA signaling in synapses", ["Increases glutamate release", "Blocks chloride influx", "Activates skeletal muscle nicotinic receptors"], "Enhancing GABAergic inhibition can raise seizure threshold."),
            item("Excitotoxic neuronal injury after ischemia is closely linked to excessive:", "Glutamate receptor activation and calcium influx", ["Histamine H2 blockade", "Muscarinic receptor absence", "Beta-2 receptor desensitization"], "Excess glutamate, especially through NMDA receptors, increases intracellular calcium and neuronal injury."),
            item("A patient has analgesia and euphoria after morphine. Which neuronal mechanism contributes to reduced transmitter release?", "Mu receptor Gi signaling decreases calcium influx and increases potassium conductance", ["GABA-A receptors open sodium channels", "D1 receptors block adenylyl cyclase", "NMDA receptors close chloride channels"], "Mu receptors are Gi-coupled and inhibit neurotransmitter release while hyperpolarizing neurons."),
            item("A drug enhancing AMPA receptor activity would most directly increase:", "Fast excitatory glutamatergic transmission", ["Slow muscarinic cardiac inhibition", "Peripheral neuromuscular blockade", "Opioid receptor desensitization"], "AMPA receptors mediate fast excitatory postsynaptic currents in many CNS synapses."),
            item("A patient with Huntington disease has loss of striatal neurons. The transmitter most associated with these medium spiny projection neurons is:", "GABA", ["Acetylcholine at Nm receptors", "Epinephrine", "Substance P only"], "Striatal medium spiny neurons are GABAergic, with peptide cotransmitters in some pathways."),
            item("Tolerance to many CNS depressants develops partly because neurons:", "Adapt receptor number or signaling to repeated drug exposure", ["Stop producing ATP permanently", "Lose all synaptic vesicles", "Convert GABA receptors into dopamine receptors"], "Neuroadaptation in receptor expression and downstream signaling contributes to tolerance and dependence."),
        ],
    ),
    (
        "blood-brain-barrier",
        "The Blood-Brain Barrier and Its Influence on Drug Transport to the Brain",
        [
            item("Levodopa enters the brain more effectively than dopamine because levodopa:", "Uses the large neutral amino acid transporter at the BBB", ["Is more water soluble than dopamine", "Blocks P-glycoprotein", "Opens endothelial tight junctions"], "Dopamine is too polar for useful BBB entry; levodopa uses amino acid transport."),
            item("Carbidopa improves levodopa therapy because it:", "Inhibits peripheral dopa decarboxylase without entering the brain significantly", ["Blocks central D2 receptors", "Increases dopamine renal clearance", "Opens the BBB"], "Carbidopa limits peripheral conversion, reducing nausea and increasing levodopa available for CNS transport."),
            item("A brain tumor drug fails despite potent in vitro activity. One plausible BBB explanation is:", "Efflux by P-glycoprotein at brain capillary endothelium", ["Absence of plasma albumin", "Rapid gastric emptying", "Excess renal filtration into CSF"], "Efflux transporters such as P-glycoprotein limit CNS penetration of many xenobiotics."),
            item("During meningitis, some beta-lactam antibiotic concentrations in CSF rise because inflammation:", "Disrupts barrier integrity and increases permeability", ["Eliminates renal clearance", "Blocks hepatic metabolism", "Destroys albumin binding"], "Inflammation can loosen BBB restrictions, increasing entry of selected drugs."),
            item("Intrathecal chemotherapy is used for some CNS disease because it:", "Bypasses the blood-brain barrier by delivering drug into CSF", ["Increases first-pass metabolism", "Prevents all neurotoxicity", "Requires P-glycoprotein efflux"], "Direct CSF administration can achieve CNS exposure when systemic delivery is inadequate."),
            item("A highly ionized quaternary ammonium drug has little CNS effect because it:", "Crosses lipid membranes and the BBB poorly", ["Is always destroyed in the stomach", "Must bind NMDA receptors first", "Is converted to dopamine"], "Ionized, polar molecules generally penetrate the BBB poorly unless transported."),
            item("Why do many monoclonal antibodies have limited treatment effects inside the brain parenchyma?", "Large size and polarity restrict BBB passage", ["They are all rapidly filtered into neurons", "They irreversibly bind hemoglobin", "They activate muscarinic receptors"], "Large biologics generally have poor BBB penetration without specialized delivery mechanisms."),
            item("A lipophilic anesthetic induces unconsciousness quickly after IV bolus. The key distribution principle is:", "Rapid entry into highly perfused brain tissue", ["Slow entry through renal tubules", "Irreversible binding to plasma albumin only", "Failure to cross endothelial membranes"], "Lipophilicity and high brain blood flow allow rapid CNS onset for many anesthetics."),
            item("A patient drinks a high-protein meal with levodopa and notices reduced benefit. The likely reason is competition for:", "Large neutral amino acid transport into gut and brain", ["Renal organic acid secretion", "Pulmonary gas exchange", "Muscarinic receptor binding"], "Dietary amino acids can compete with levodopa transport across the gut and BBB."),
            item("A CNS drug is designed as a prodrug that becomes active after crossing the BBB. The advantage is:", "Improved brain entry while preserving active pharmacology after conversion", ["Guaranteed absence of toxicity", "Permanent BBB opening", "Elimination of metabolism"], "Prodrug strategies can tune polarity or transporter recognition to improve CNS delivery."),
        ],
    ),
    (
        "depression-anxiety",
        "Drug Therapy of Depression and Anxiety Disorders",
        [
            item("A patient on sertraline starts linezolid and develops agitation, fever, clonus, and diarrhea. The diagnosis is:", "Serotonin syndrome", ["Neuroleptic malignant syndrome", "Cholinergic crisis", "Malignant hyperthermia"], "Linezolid has MAO-inhibiting activity; combined serotonergic drugs can produce serotonin toxicity with clonus and hyperreflexia."),
            item("A depressed patient also has diabetic neuropathic pain. Which antidepressant class is especially logical?", "Serotonin-norepinephrine reuptake inhibitor", ["Selective alpha-1 blocker", "Pure dopamine antagonist", "Peripheral muscarinic agonist"], "SNRIs such as duloxetine treat depression and neuropathic pain via descending monoaminergic pathways."),
            item("A patient overdoses on amitriptyline and has seizures, hypotension, and wide QRS tachycardia. The targeted treatment is:", "Sodium bicarbonate", ["Flumazenil", "Pralidoxime", "Methadone"], "TCAs block cardiac sodium channels; bicarbonate therapy narrows QRS and treats severe cardiotoxicity."),
            item("A patient taking phenelzine eats aged cheese and develops severe hypertension. The mechanism is:", "Tyramine-triggered norepinephrine release when MAO is inhibited", ["Direct histamine release from cheese", "Loss of acetylcholine at ganglia", "Beta-2 receptor destruction"], "MAO normally metabolizes tyramine; MAO inhibition allows tyramine to release norepinephrine."),
            item("A patient with depression wants to avoid sexual dysfunction and weight gain and also wants help quitting smoking. Which drug is most suitable?", "Bupropion", ["Paroxetine", "Mirtazapine", "Amitriptyline"], "Bupropion inhibits norepinephrine and dopamine reuptake and is also used for smoking cessation."),
            item("A depressed patient with severe insomnia and poor appetite is started on mirtazapine. Which adverse effect is most expected?", "Weight gain and sedation", ["Hypertensive crisis with tyramine", "Severe sodium-channel cardiotoxicity at usual doses", "Irreversible parkinsonism"], "Mirtazapine is often sedating and appetite-stimulating, partly through H1 and 5-HT2/5-HT3 blockade."),
            item("Buspirone is chosen for generalized anxiety in a patient with substance use history because it:", "Has little abuse liability and lacks benzodiazepine-like respiratory depression", ["Works immediately like IV diazepam", "Blocks opioid receptors", "Causes general anesthesia"], "Buspirone is a 5-HT1A partial agonist with delayed onset but minimal dependence risk."),
            item("An older patient becomes hyponatremic after starting an SSRI. The likely adverse effect is:", "SIADH", ["Diabetes insipidus", "Organophosphate poisoning", "Pheochromocytoma"], "SSRIs can cause SIADH and hyponatremia, particularly in older adults."),
            item("A panic-disorder patient receives a short benzodiazepine bridge while an SSRI is initiated. The rationale is:", "SSRIs take weeks, while benzodiazepines provide rapid symptom relief", ["SSRIs are inactive unless benzodiazepines induce CYP enzymes", "Benzodiazepines prevent serotonin syndrome", "Benzodiazepines cure depression permanently"], "Benzodiazepines act quickly; antidepressant anxiolytic effects usually require weeks."),
            item("A patient has abrupt venlafaxine cessation with dizziness, irritability, and electric-shock sensations. This is:", "Antidepressant discontinuation syndrome", ["Opioid withdrawal", "Neuroleptic malignant syndrome", "Cholinergic crisis"], "Short half-life serotonergic antidepressants can cause discontinuation symptoms if stopped suddenly."),
        ],
    ),
    (
        "psychosis-mania",
        "Pharmacotherapy of Psychosis and Mania",
        [
            item("A patient on haloperidol develops fever, lead-pipe rigidity, confusion, autonomic instability, and high CK. The diagnosis is:", "Neuroleptic malignant syndrome", ["Serotonin syndrome", "Opioid overdose", "Cholinergic crisis"], "D2 blockade can trigger NMS; treatment includes stopping the drug, supportive care, and sometimes dantrolene or bromocriptine."),
            item("Clozapine is considered for treatment-resistant schizophrenia. Which monitoring is mandatory?", "Absolute neutrophil count", ["Serum amylase after every dose", "Daily pulmonary function testing", "Urine glucose every hour"], "Clozapine can cause severe neutropenia/agranulocytosis and requires ANC monitoring."),
            item("A patient on risperidone develops amenorrhea and galactorrhea. The pathway involved is:", "Tuberoinfundibular D2 blockade increasing prolactin", ["Nigrostriatal D1 activation", "Mesolimbic 5-HT3 blockade", "Peripheral alpha-1 activation"], "Dopamine tonically inhibits prolactin release; D2 blockade removes that inhibition."),
            item("A patient with schizophrenia and Parkinson disease needs an antipsychotic least likely to worsen motor symptoms. Which is commonly preferred?", "Quetiapine", ["Haloperidol", "Fluphenazine", "Metoclopramide"], "Quetiapine has relatively lower D2 occupancy and is often used when extrapyramidal worsening is a concern."),
            item("Olanzapine improves psychosis but causes weight gain and new diabetes. This is most consistent with:", "Metabolic toxicity of second-generation antipsychotics", ["Irreversible acetylcholinesterase inhibition", "Pure beta-1 blockade", "Mu-opioid withdrawal"], "Several atypical antipsychotics, especially clozapine and olanzapine, increase metabolic risk."),
            item("A patient on lithium develops tremor, ataxia, vomiting, confusion, and worsening kidney function after starting an NSAID. The reason is:", "Reduced renal lithium clearance causing toxicity", ["Increased hepatic lithium metabolism", "D2 receptor supersensitivity", "Irreversible lithium binding to albumin"], "Lithium is renally cleared; NSAIDs, ACE inhibitors, and thiazides can increase lithium levels."),
            item("A bipolar patient taking lithium develops polyuria and polydipsia. The mechanism is:", "Nephrogenic diabetes insipidus", ["SIADH", "Alpha-1 blockade", "Acetylcholine excess"], "Lithium can impair renal concentrating ability, causing nephrogenic diabetes insipidus."),
            item("Valproate is useful for acute mania but is avoided when possible in pregnancy because it:", "Has high teratogenic risk including neural tube defects", ["Causes irreversible deafness in all adults", "Blocks opioid receptors", "Cannot enter the CNS"], "Valproate is effective for mania but is strongly teratogenic."),
            item("A patient on haloperidol develops acute painful neck twisting hours after treatment. Best immediate treatment is:", "Benztropine or diphenhydramine", ["Pralidoxime", "Naltrexone", "Acamprosate"], "Acute dystonia from D2 blockade responds to antimuscarinic or antihistaminic anticholinergic therapy."),
            item("A patient with poor adherence receives monthly paliperidone injection. The main reason is:", "Long-acting depot delivery improves adherence coverage", ["Depot drugs have no adverse effects", "Paliperidone cannot be taken orally", "It permanently cures psychosis after one dose"], "Long-acting injectable antipsychotics maintain exposure and reduce relapse from missed oral doses."),
        ],
    ),
    (
        "epilepsies",
        "Pharmacotherapy of the Epilepsies",
        [
            item("A child has brief staring spells with 3-Hz spike-and-wave discharges. Which drug targets the relevant thalamic current?", "Ethosuximide", ["Phenytoin", "Gabapentin", "Phenobarbital"], "Ethosuximide blocks T-type calcium channels and is classic for absence seizures."),
            item("A patient on phenytoin has nystagmus, ataxia, and confusion after a small dose increase. Why can this happen?", "Saturable metabolism causes disproportionate level increases", ["Renal secretion becomes infinite", "It has no protein binding", "It is destroyed by gastric acid"], "Phenytoin has capacity-limited metabolism near therapeutic levels."),
            item("A woman of childbearing potential with generalized epilepsy is counseled to avoid valproate if alternatives work because of:", "Neural tube defect and neurodevelopmental risk", ["Permanent infertility in all users", "No antiseizure efficacy", "Severe bronchospasm"], "Valproate is broad-spectrum but highly teratogenic."),
            item("Carbamazepine is started for focal seizures. Which adverse effect needs blood count attention?", "Agranulocytosis or aplastic anemia", ["Irreversible miosis", "Acute opioid overdose", "Pulmonary fibrosis after one dose"], "Carbamazepine can cause serious blood dyscrasias and also hyponatremia."),
            item("A patient develops fever and mucosal blistering rash after lamotrigine titration. The concern is:", "Stevens-Johnson syndrome", ["Cholinergic crisis", "Pheochromocytoma", "Serotonin withdrawal"], "Lamotrigine can cause life-threatening rash, especially with rapid titration or valproate coadministration."),
            item("Status epilepticus is treated first with lorazepam because it:", "Rapidly enhances GABA-A inhibition", ["Irreversibly blocks sodium channels", "Reactivates acetylcholinesterase", "Blocks opioid receptors"], "Benzodiazepines are first-line acute therapy because they rapidly increase inhibitory GABAergic signaling."),
            item("Levetiracetam is added for focal seizures. Its distinctive target is:", "SV2A synaptic vesicle protein", ["T-type calcium channel only", "Muscarinic M3 receptor", "Alpha-1 receptor"], "Levetiracetam binds SV2A and modulates synaptic neurotransmitter release."),
            item("Topiramate helps seizures and migraine but a patient develops kidney stones and word-finding difficulty. Which property contributes?", "Carbonic anhydrase inhibition", ["Pure beta blockade", "Mu-opioid agonism", "D2 antagonism"], "Topiramate can inhibit carbonic anhydrase, causing stones and metabolic acidosis; cognitive slowing is also common."),
            item("A patient on vigabatrin needs visual field monitoring because it can cause:", "Irreversible retinal toxicity", ["Agranulocytosis only", "Malignant hyperthermia", "Hypertensive crisis with tyramine"], "Vigabatrin can cause permanent visual field defects."),
            item("Gabapentin reduces neuropathic pain and seizures by binding:", "The alpha2delta subunit of voltage-gated calcium channels", ["GABA-A benzodiazepine sites", "NMDA glycine sites", "Nicotinic Nm receptors"], "Gabapentin and pregabalin bind alpha2delta calcium channel subunits, reducing excitatory transmitter release."),
        ],
    ),
    (
        "cns-degenerative-disorders",
        "Treatment of Central Nervous System Degenerative Disorders",
        [
            item("A Parkinson patient gets nausea and orthostasis when levodopa is started. Which adjunct reduces peripheral dopamine formation?", "Carbidopa", ["Haloperidol", "Donepezil", "Naloxone"], "Carbidopa inhibits peripheral aromatic L-amino acid decarboxylase and does not significantly enter the brain."),
            item("Entacapone is added for wearing-off episodes. Its role is to:", "Inhibit peripheral COMT and prolong levodopa effect", ["Block central D2 receptors", "Stimulate muscarinic receptors", "Inhibit acetylcholinesterase in muscle"], "COMT inhibitors reduce peripheral levodopa metabolism and extend levodopa availability."),
            item("A Parkinson patient with impulse-control disorder and sleep attacks is likely affected by:", "Dopamine agonist adverse effects", ["Acetylcholinesterase inhibitor toxicity", "NMDA antagonist withdrawal", "Alpha-1 blockade only"], "Pramipexole and ropinirole can cause sleep attacks, hallucinations, and impulse-control disorders."),
            item("Benztropine is most useful in Parkinson disease when the dominant symptom is:", "Tremor in a younger patient", ["Dementia with urinary retention", "Levodopa-induced psychosis", "Severe orthostatic hypotension"], "Antimuscarinics can reduce tremor but are poorly tolerated in older or cognitively impaired patients."),
            item("Selegiline can worsen serotonin toxicity risk when combined with meperidine because it:", "Inhibits monoamine oxidase signaling pathways", ["Blocks all dopamine receptors", "Activates NMDA receptors", "Inhibits renal lithium clearance"], "MAO-B inhibitors can interact dangerously with serotonergic drugs."),
            item("Donepezil provides modest Alzheimer symptomatic benefit by:", "Increasing synaptic acetylcholine in the CNS", ["Blocking dopamine receptors", "Opening the BBB", "Stimulating beta-1 receptors"], "Central acetylcholinesterase inhibition can improve cognition or function modestly."),
            item("Memantine is added in moderate Alzheimer disease to:", "Antagonize NMDA receptors and reduce pathologic glutamate signaling", ["Destroy amyloid plaques immediately", "Activate nicotinic Nm receptors", "Increase peripheral dopamine"], "Memantine is an NMDA antagonist used for moderate to severe Alzheimer disease."),
            item("Riluzole modestly extends survival in ALS mainly by:", "Reducing glutamatergic neurotransmission", ["Blocking muscarinic receptors", "Activating mu receptors", "Inhibiting COMT"], "Riluzole decreases glutamate release/signaling and can modestly prolong survival in ALS."),
            item("Tetrabenazine improves Huntington chorea but can worsen depression because it:", "Depletes monoamines by inhibiting VMAT2", ["Inhibits acetylcholinesterase", "Stimulates CB1 receptors", "Blocks sodium channels"], "VMAT2 inhibition reduces dopamine signaling and chorea but may worsen depression or parkinsonism."),
            item("Amantadine may reduce levodopa-induced dyskinesia partly through:", "NMDA receptor antagonism", ["Irreversible MAO-A inhibition", "Alpha-1 blockade", "Acetylcholine vesicle fusion blockade"], "Amantadine has dopaminergic effects and NMDA antagonist activity useful for dyskinesia in some patients."),
        ],
    ),
    (
        "hypnotics-sedatives",
        "Hypnotics and Sedatives",
        [
            item("Compared with phenobarbital, diazepam is safer in isolated overdose because benzodiazepines:", "Require GABA and have a ceiling effect on channel opening", ["Directly open chloride channels at all doses", "Block sodium channels in the heart", "Are irreversible receptor antagonists"], "Benzodiazepines increase GABA-A opening frequency in the presence of GABA, giving a wider safety margin than barbiturates."),
            item("Flumazenil reverses procedural midazolam but can cause seizures in which patient?", "A chronic benzodiazepine user or mixed TCA overdose patient", ["A patient with isolated caffeine use", "A patient receiving atropine eye drops", "A patient on oral iron"], "Flumazenil can precipitate withdrawal seizures and is risky in mixed proconvulsant overdoses."),
            item("A patient taking zolpidem reports sleep-driving with amnesia. The adverse effect is:", "Complex sleep behavior from a Z-drug", ["Opioid withdrawal", "Cholinergic crisis", "Alpha-1 agonism"], "Nonbenzodiazepine hypnotics can cause amnesia and complex sleep behaviors."),
            item("Ramelteon is chosen for sleep-onset insomnia because it:", "Activates melatonin MT1/MT2 receptors", ["Blocks D2 receptors", "Opens NMDA channels", "Inhibits acetylcholinesterase"], "Ramelteon targets melatonin receptors and has little abuse liability."),
            item("Suvorexant promotes sleep by:", "Antagonizing orexin receptors", ["Stimulating beta-1 receptors", "Blocking mu receptors", "Activating nicotinic receptors"], "Orexin signaling promotes wakefulness; antagonism helps sleep initiation and maintenance."),
            item("A patient on phenobarbital has reduced warfarin effect after weeks. The explanation is:", "CYP enzyme induction", ["Renal tubular blockade", "P-glycoprotein destruction", "Albumin synthesis arrest"], "Barbiturates induce hepatic drug-metabolizing enzymes, increasing clearance of many drugs."),
            item("An older patient receives a long-acting benzodiazepine and falls repeatedly. The likely drug-related problem is:", "Sedation, psychomotor impairment, and accumulation", ["Permanent neuromuscular paralysis", "Acute hypertensive crisis", "Bronchorrhea"], "Older adults are sensitive to benzodiazepine sedation and falls, especially with long-acting agents."),
            item("A patient with severe alcohol withdrawal is treated with diazepam. The mechanistic reason is:", "Cross-tolerant enhancement of GABA-A signaling", ["Irreversible blockade of NMDA receptors only", "Dopamine receptor activation", "Muscarinic receptor stimulation"], "Benzodiazepines replace deficient inhibitory tone and prevent seizures in alcohol withdrawal."),
            item("A hypnotic that directly prolongs GABA-A chloride channel opening and can cause fatal respiratory depression is most likely:", "A barbiturate", ["An SSRI", "A 5-HT3 antagonist", "A COMT inhibitor"], "Barbiturates prolong GABA-A channel opening and at high doses can directly gate the channel."),
            item("A patient with liver disease needs a benzodiazepine less dependent on oxidative hepatic metabolism. Which is preferred?", "Lorazepam", ["Diazepam", "Chlordiazepoxide", "Clonazepam"], "Lorazepam, oxazepam, and temazepam rely mainly on glucuronidation and lack long-lived active metabolites."),
        ],
    ),
    (
        "opioid-analgesics",
        "Opioid Analgesics",
        [
            item("A patient with pinpoint pupils and respiratory depression wakes after naloxone, then becomes sedated again. Why repeat dosing may be required?", "Naloxone can wear off before the opioid", ["Naloxone is a long-acting opioid agonist", "Naloxone induces CYP enzymes instantly", "Naloxone blocks acetylcholinesterase"], "Naloxone is a competitive antagonist with shorter duration than many opioids."),
            item("A patient on chronic morphine has constipation despite stable analgesia. Which option treats gut effects while sparing central analgesia best?", "Methylnaltrexone", ["High-dose naloxone infusion", "Diazepam", "Atropine"], "Peripherally acting mu antagonists treat opioid-induced constipation with limited CNS penetration."),
            item("Buprenorphine precipitates withdrawal in a heroin-dependent patient who used recently because it:", "Partially activates mu receptors while displacing full agonist", ["Irreversibly blocks NMDA receptors", "Inhibits serotonin reuptake only", "Activates nicotinic receptors"], "High-affinity partial agonism can lower net mu signaling in the presence of full agonist dependence."),
            item("Methadone is useful for opioid use disorder but needs ECG caution because it can:", "Prolong the QT interval", ["Cause irreversible deafness in all patients", "Block acetylcholinesterase", "Induce malignant hyperthermia"], "Methadone is long acting and can prolong QT, especially at higher doses or with interacting drugs."),
            item("A patient with renal failure becomes confused and oversedated on morphine. The concern is accumulation of:", "Active glucuronide metabolites", ["Unchanged drug in alveoli only", "Inactive sulfate salts", "Dopamine metabolites"], "Morphine metabolites are renally cleared and can accumulate in kidney failure."),
            item("Tramadol causes seizure and serotonin syndrome risk because it:", "Has monoamine reuptake inhibition in addition to weak mu agonism", ["Is a pure peripheral antagonist", "Blocks muscarinic receptors only", "Reactivates acetylcholinesterase"], "Tramadol combines opioid activity with serotonergic/noradrenergic effects."),
            item("Codeine gives poor analgesia in a CYP2D6 poor metabolizer because:", "Less codeine is converted to morphine", ["More naloxone is produced", "The BBB becomes impermeable to all opioids", "Mu receptors disappear"], "Codeine is a prodrug partly bioactivated by CYP2D6."),
            item("A patient with opioid overdose has severe pulmonary edema after reversal. The immediate priority remains:", "Ventilation and airway support with careful naloxone titration", ["Giving more opioid to restore miosis", "Avoiding oxygen", "Starting pralidoxime"], "Opioid overdose management centers on ventilation; naloxone is titrated to restore breathing, not necessarily full arousal."),
            item("Fentanyl patches cause overdose after a patient applies heat over the patch. The mechanism is:", "Increased transdermal absorption", ["Patch conversion into naloxone", "Loss of mu receptor binding", "Renal activation"], "Heat can increase fentanyl delivery from transdermal systems and cause respiratory depression."),
            item("Miosis in opioid overdose is mediated mainly by:", "Mu receptor effects on parasympathetic pupillary pathways", ["Alpha-1 activation of radial muscle", "M3 blockade of sphincter muscle", "Beta-2 activation"], "Opioids increase parasympathetic tone to the pupil, producing pinpoint pupils."),
        ],
    ),
    (
        "general-anesthetics-therapeutic-gases",
        "General Anesthetics and Therapeutic Gases",
        [
            item("An inhaled anesthetic has a low blood-gas partition coefficient. Its clinical implication is:", "Rapid induction and recovery", ["Very slow alveolar equilibration", "No brain penetration", "Irreversible metabolism"], "Low blood solubility allows alveolar and brain partial pressures to rise and fall quickly."),
            item("MAC is lower in an older patient. This means the patient:", "Needs a lower alveolar anesthetic concentration to prevent movement", ["Needs more anesthetic because age raises MAC", "Cannot receive inhaled anesthetics", "Has no response to opioids"], "MAC is the alveolar concentration preventing movement in 50% of patients; it decreases with age."),
            item("A child under halothane develops hyperthermia, rigidity, acidosis, and hyperkalemia. Which treatment is specific?", "Dantrolene", ["Flumazenil", "Pralidoxime", "Physostigmine"], "Malignant hyperthermia is treated with dantrolene and supportive cooling."),
            item("Propofol is favored for induction but causes hypotension primarily because it:", "Decreases systemic vascular resistance and myocardial contractility", ["Activates alpha-1 receptors", "Blocks all GABA signaling", "Releases acetylcholine at ganglia"], "Propofol enhances GABA-A signaling and commonly produces vasodilation and myocardial depression."),
            item("Ketamine is useful in trauma anesthesia because it often:", "Maintains airway reflexes and supports blood pressure via sympathetic stimulation", ["Causes profound histamine-mediated hypotension in all patients", "Has no analgesic effect", "Blocks opioid receptors"], "Ketamine is an NMDA antagonist with dissociative anesthesia, analgesia, and sympathetic stimulation."),
            item("Etomidate is chosen for unstable induction but prolonged infusion is avoided because it:", "Suppresses adrenal steroid synthesis", ["Causes irreversible renal failure after one dose", "Triggers opioid withdrawal", "Blocks acetylcholinesterase"], "Etomidate inhibits adrenal 11-beta-hydroxylase and can suppress cortisol production."),
            item("Nitrous oxide can expand a pneumothorax because it:", "Diffuses into closed gas spaces faster than nitrogen leaves", ["Is highly soluble in blood", "Irreversibly binds hemoglobin", "Blocks beta-2 receptors"], "Nitrous oxide enters air-filled spaces rapidly and can enlarge them."),
            item("A patient develops postoperative nausea after volatile anesthesia. Which class is commonly used prophylactically?", "5-HT3 antagonist such as ondansetron", ["COMT inhibitor", "Acetylcholinesterase reactivator", "Alpha-1 agonist only"], "Ondansetron is commonly used for postoperative nausea and vomiting."),
            item("Sevoflurane is commonly used for inhalational induction in children because it is:", "Nonpungent with rapid onset", ["The most airway-irritating agent", "Unable to cross the BBB", "A pure opioid agonist"], "Sevoflurane is pleasant/nonirritating and has relatively rapid kinetics."),
            item("Carbon monoxide poisoning is treated with oxygen because oxygen:", "Shortens carboxyhemoglobin half-life by competing for hemoglobin binding", ["Converts CO into dopamine", "Blocks muscarinic receptors", "Inhibits alcohol dehydrogenase"], "High-flow oxygen, and sometimes hyperbaric oxygen, accelerates CO dissociation from hemoglobin."),
        ],
    ),
    (
        "local-anesthetics",
        "Local Anesthetics",
        [
            item("Lidocaine works poorly in an abscess because acidic tissue:", "Increases ionized drug fraction outside the nerve, reducing membrane penetration", ["Destroys all sodium channels", "Makes the drug an irreversible agonist", "Prevents hepatic metabolism"], "Local anesthetics are weak bases; the uncharged form crosses nerve membranes."),
            item("A patient has tinnitus, circumoral numbness, seizures, and arrhythmia after bupivacaine. The core toxicity is:", "Systemic voltage-gated sodium channel blockade", ["Muscarinic receptor stimulation", "D2 receptor blockade", "Acetylcholinesterase aging"], "High systemic local anesthetic levels affect CNS and cardiac sodium channels; bupivacaine is notably cardiotoxic."),
            item("Lipid emulsion is given for severe bupivacaine cardiotoxicity because it:", "Sequesters lipophilic anesthetic and supports resuscitation", ["Reactivates acetylcholinesterase", "Blocks opioid receptors", "Induces immediate renal excretion"], "IV lipid emulsion is used for severe local anesthetic systemic toxicity."),
            item("Epinephrine prolongs lidocaine anesthesia mainly by:", "Local alpha-1 vasoconstriction reducing systemic absorption", ["Opening sodium channels", "Increasing tissue acidity", "Blocking GABA-A receptors"], "Vasoconstriction keeps anesthetic near the nerve and lowers peak plasma concentration."),
            item("Which local anesthetic can cause methemoglobinemia?", "Prilocaine", ["Ropivacaine", "Bupivacaine", "Mepivacaine"], "Prilocaine and benzocaine are classic causes of methemoglobinemia."),
            item("A patient allergic to procaine may tolerate lidocaine because lidocaine is:", "An amide local anesthetic rather than an ester", ["A muscarinic agonist", "A dopamine precursor", "A barbiturate"], "Ester anesthetics are more associated with PABA-related allergy; amides are structurally different."),
            item("Local anesthetics preferentially block pain before motor function partly because:", "Small, rapidly firing fibers are more susceptible to use-dependent blockade", ["Motor fibers lack sodium channels", "Pain fibers have opioid receptors only", "Large fibers are outside nerves"], "Frequency-dependent sodium channel blockade affects active, smaller fibers earlier."),
            item("Cocaine differs from most local anesthetics because it also:", "Blocks norepinephrine reuptake causing vasoconstriction", ["Reactivates acetylcholinesterase", "Stimulates GABA-A receptors", "Blocks mu receptors"], "Cocaine has sympathomimetic effects through catecholamine reuptake inhibition."),
            item("Spinal anesthesia causing hypotension is mainly due to:", "Sympathetic blockade with vasodilation", ["Direct renal failure", "Pure beta-1 stimulation", "Increased skeletal muscle tone"], "Neuraxial local anesthetic can block sympathetic outflow, reducing venous return and vascular tone."),
            item("Repeated dosing into inflamed tissue increases systemic toxicity risk because:", "Greater absorption and need for larger doses can raise plasma levels", ["Inflammation prevents all vascular uptake", "Sodium channels become absent", "The drug becomes naloxone"], "Inflamed tissues can require more drug and may absorb it quickly, increasing toxicity risk."),
        ],
    ),
    (
        "cannabinoids",
        "Cannabinoids",
        [
            item("THC produces euphoria, impaired short-term memory, and appetite stimulation mainly through:", "CB1 receptor activation in the CNS", ["CB2 receptor blockade in bone marrow", "Nicotinic Nm activation", "Alpha-1 blockade"], "CB1 receptors are abundant in the CNS and mediate most psychoactive cannabinoid effects."),
            item("A patient with chemotherapy-induced nausea refractory to standard therapy receives dronabinol. It is:", "A synthetic THC agonist", ["A 5-HT3 antagonist", "A dopamine precursor", "An opioid antagonist"], "Dronabinol is synthetic delta-9-THC used for selected nausea and appetite indications."),
            item("Cannabidiol is useful in some severe childhood epilepsies and is notable because it:", "Has antiseizure activity without THC-like intoxication", ["Is a strong CB1 intoxicant", "Irreversibly blocks GABA-A receptors", "Causes acetylcholinesterase aging"], "CBD has distinct pharmacology from THC and is approved for certain seizure syndromes."),
            item("A chronic cannabis user has cyclic vomiting relieved by hot showers. The diagnosis is:", "Cannabinoid hyperemesis syndrome", ["Serotonin syndrome", "Opioid withdrawal only", "Cholinergic crisis"], "Chronic heavy cannabis use can paradoxically cause recurrent vomiting."),
            item("A teen develops paranoia and panic after a high-potency edible. The most likely drug effect is:", "Excess CB1-mediated psychoactive stimulation", ["Peripheral acetylcholine excess", "Pure beta-2 blockade", "Irreversible NMDA blockade"], "High THC exposure can cause anxiety, paranoia, perceptual changes, and psychosis-like symptoms."),
            item("Synthetic cannabinoid products can be more dangerous than cannabis because many are:", "Full CB1 agonists with unpredictable potency and contaminants", ["Pure caffeine tablets", "Selective CB2 antagonists only", "Unable to enter the brain"], "Some synthetic cannabinoids have high potency/full agonism and unpredictable toxicity."),
            item("A cannabis user has tachycardia and conjunctival injection. These are:", "Common acute autonomic and vascular effects", ["Signs of acetylcholinesterase inhibition", "Proof of opioid overdose", "Evidence of beta-blocker toxicity"], "Cannabis commonly causes tachycardia and red eyes."),
            item("Stopping heavy daily cannabis use may cause:", "Irritability, insomnia, reduced appetite, and craving", ["Life-threatening delirium tremens in most patients", "Irreversible muscle paralysis", "Cholinergic crisis"], "Cannabis withdrawal is usually not medically dangerous but can be clinically significant."),
            item("THC can impair driving because it:", "Slows reaction time and impairs attention and coordination", ["Improves divided attention", "Prevents all sedation", "Blocks visual processing permanently"], "Cannabinoids impair psychomotor performance and judgment."),
            item("Cannabinoid anti-inflammatory effects in immune cells are more associated with:", "CB2 receptor signaling", ["Nicotinic Nm receptors", "Beta-1 receptors", "M3 receptors"], "CB2 receptors are prominent in immune tissues and contribute to immunomodulatory effects."),
        ],
    ),
    (
        "ethanol-drug-use-disorders-addiction",
        "Ethanol, Drug Use Disorders, and Addiction",
        [
            item("A patient with chronic alcohol use presents confused, ataxic, and ophthalmoplegic. What should be given before glucose?", "Thiamine", ["Naloxone", "Flumazenil", "Disulfiram"], "Thiamine prevents worsening Wernicke encephalopathy when carbohydrate metabolism increases."),
            item("A patient 24 hours after stopping alcohol has tremor, tachycardia, hypertension, and hallucinations. First-line drug therapy is:", "Benzodiazepine", ["Disulfiram", "Varenicline", "Physostigmine"], "Benzodiazepines treat alcohol withdrawal by restoring GABAergic inhibition and preventing seizures."),
            item("Disulfiram causes flushing, hypotension, and nausea after alcohol because it inhibits:", "Aldehyde dehydrogenase", ["Alcohol dehydrogenase", "Monoamine oxidase", "COMT"], "Acetaldehyde accumulates when aldehyde dehydrogenase is inhibited."),
            item("Naltrexone helps alcohol use disorder primarily by:", "Blocking opioid-mediated reward and reducing relapse/craving", ["Inducing vomiting with alcohol", "Replacing GABA during withdrawal", "Activating nicotinic receptors"], "Opioid receptor antagonism can reduce rewarding effects of alcohol and heavy-drinking relapse."),
            item("Acamprosate is most useful after abstinence is achieved because it:", "Modulates glutamate/GABA balance to support maintenance of abstinence", ["Produces acetaldehyde accumulation", "Blocks alcohol absorption", "Stimulates dopamine release"], "Acamprosate helps maintain abstinence and is renally cleared."),
            item("Methanol poisoning is treated with fomepizole because it:", "Inhibits alcohol dehydrogenase formation of toxic metabolites", ["Activates aldehyde dehydrogenase", "Blocks mu receptors", "Induces CYP2E1"], "Fomepizole prevents conversion of methanol or ethylene glycol to toxic acids."),
            item("A patient starting buprenorphine too soon after fentanyl develops withdrawal. The cause is:", "High-affinity partial agonist displacement of full agonist", ["Aldehyde dehydrogenase inhibition", "CB1 receptor activation", "GABA-A blockade"], "Buprenorphine can precipitate withdrawal if full agonist opioids are still strongly occupying receptors."),
            item("Varenicline helps tobacco cessation by:", "Partial agonism at alpha4beta2 nicotinic receptors", ["Full opioid agonism", "Irreversible MAO inhibition", "Aldehyde dehydrogenase inhibition"], "Varenicline reduces craving and blunts nicotine reward."),
            item("Cocaine use causes chest pain and hypertension because it:", "Blocks norepinephrine and dopamine reuptake", ["Stimulates GABA-A receptors", "Activates aldehyde dehydrogenase", "Blocks all calcium channels selectively"], "Cocaine increases catecholamine signaling and can cause vasospasm, arrhythmias, and hypertension."),
            item("Long-term addiction vulnerability is strongly linked to drug-induced plasticity in which circuit?", "Mesolimbic dopamine reward pathway", ["Neuromuscular junction only", "Renal juxtaglomerular apparatus", "Peripheral muscarinic synapse"], "Addictive drugs converge on reward learning and salience circuits involving ventral tegmental dopamine projections."),
        ],
    ),
]


def main():
    questions = []
    for topic_index, (slug, topic, rows) in enumerate(TOPICS):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        for question_index, row in enumerate(rows, 1):
            options = list(row["wrong"])
            answer_index = (topic_index + question_index - 1) % 4
            options.insert(answer_index, row["answer"])
            questions.append(
                {
                    **BASE,
                    "id": f"neuropharm-{slug}-{question_index:02d}",
                    "topic": topic,
                    "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high",
                    "prompt": row["prompt"],
                    "options": options,
                    "answerIndex": answer_index,
                    "answer": row["answer"],
                    "explanation": row["explanation"],
                }
            )

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    old_questions = data.get("questions", [])
    data["questions"] = [
        question
        for question in old_questions
        if not (
            question.get("subjectId") == "pharmacology"
            and question.get("chapterTitle") == "Neuropharmacology"
        )
    ] + questions

    if len(TOPICS) != 18:
        raise AssertionError(f"Expected 18 topics, got {len(TOPICS)}")
    if len(questions) != 180:
        raise AssertionError(f"Expected 180 questions, got {len(questions)}")
    if len({question["id"] for question in questions}) != 180:
        raise AssertionError("Question IDs are not unique")
    if any(question["answer"] != question["options"][question["answerIndex"]] for question in questions):
        raise AssertionError("At least one answerIndex does not point to the answer")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} Neuropharmacology questions across {len(TOPICS)} topics.")


if __name__ == "__main__":
    main()
