import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
BASE = {"subjectId": "anatomy", "subjectTitle": "Anatomy", "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


CHAPTERS = {
    "Head and Neck": [
        ("scalp-face-parotid", "Scalp, Face and Parotid Region", [
            q("The layer of scalp containing vessels and nerves is the:", "Dense connective tissue layer", ["Skin only", "Loose areolar tissue", "Pericranium"], "The second scalp layer is dense connective tissue and holds vessels open."),
            q("The danger area of scalp is the:", "Loose areolar tissue layer", ["Skin", "Dense connective tissue", "Pericranium"], "Emissary veins in loose areolar tissue can spread infection intracranially."),
            q("Motor supply of muscles of facial expression is by:", "Facial nerve", ["Trigeminal nerve", "Glossopharyngeal nerve", "Hypoglossal nerve"], "Facial nerve supplies muscles derived from second pharyngeal arch."),
            q("Sensory supply of most face is by:", "Trigeminal nerve", ["Facial nerve", "Accessory nerve", "Vagus nerve"], "The trigeminal divisions carry general sensation from the face."),
            q("The parotid duct opens opposite the:", "Upper second molar tooth", ["Lower canine", "Upper central incisor", "Lower third molar"], "The duct pierces buccinator and opens into the vestibule opposite upper second molar."),
            q("The facial nerve divides within the parotid gland into:", "Terminal motor branches", ["Sensory divisions of trigeminal nerve", "Sympathetic ganglia", "Hypoglossal branches"], "The parotid plexus gives temporal, zygomatic, buccal, marginal mandibular and cervical branches."),
            q("The structure most superficial in the parotid gland is usually:", "Facial nerve", ["External carotid artery", "Retromandibular vein", "Glossopharyngeal nerve"], "From superficial to deep: facial nerve, retromandibular vein, external carotid artery."),
            q("The muscles of mastication are supplied by:", "Mandibular nerve", ["Maxillary nerve", "Facial nerve", "Hypoglossal nerve"], "Motor fibers to muscles of mastication travel with V3."),
            q("The facial artery crosses the mandible at the anterior border of:", "Masseter", ["Temporalis", "Sternocleidomastoid", "Mylohyoid"], "The pulse is palpable where it crosses the mandible at masseter's anterior border."),
            q("The great auricular nerve supplies skin over:", "Parotid region and auricle", ["Upper eyelid only", "Tongue tip", "Nasal septum"], "It is a cervical plexus branch crossing sternocleidomastoid to parotid/auricle."),
            q("A scalp wound bleeds profusely and the vessel ends do not retract. Which scalp layer explains this?", "Dense connective tissue layer", ["Loose areolar tissue", "Pericranium", "Temporalis fascia only"], "Dense connective tissue fixes vessels open, causing heavy bleeding."),
            q("A boil in the upper lip is squeezed and cavernous sinus thrombosis follows. Which venous route explains spread?", "Facial vein to ophthalmic veins", ["Facial artery to maxillary artery", "Parotid duct to pterygoid plexus", "External jugular vein to thoracic duct"], "The facial vein communicates with ophthalmic veins, providing a route to cavernous sinus."),
            q("After parotid surgery, the patient cannot close the eye tightly and has mouth deviation. Which nerve was injured?", "Facial nerve", ["Auriculotemporal nerve", "Glossopharyngeal nerve", "Hypoglossal nerve"], "Facial nerve branches traverse the parotid and supply facial expression muscles."),
            q("A parotid abscess is painful while chewing because the gland is enclosed by which tough fascia?", "Investing layer of deep cervical fascia", ["Buccopharyngeal fascia", "Pretracheal fascia", "Pharyngobasilar fascia"], "Parotid fascia is tough and limits swelling, producing pain."),
            q("A child with mumps has pain referred to the ear. Which sensory nerve carries parotid pain?", "Auriculotemporal nerve", ["Infraorbital nerve", "Hypoglossal nerve", "Recurrent laryngeal nerve"], "Auriculotemporal nerve carries sensory and secretomotor-related fibers for parotid region."),
        ]),
        ("temporal-infratemporal", "Temporal and Infratemporal Fossae", [
            q("The temporalis muscle inserts on the:", "Coronoid process of mandible", ["Condylar neck", "Angle of mandible", "Mastoid process"], "Temporalis passes deep to zygomatic arch to coronoid process."),
            q("The maxillary artery is a terminal branch of:", "External carotid artery", ["Internal carotid artery", "Facial artery", "Vertebral artery"], "External carotid ends as maxillary and superficial temporal arteries."),
            q("The middle meningeal artery enters skull through:", "Foramen spinosum", ["Foramen ovale", "Foramen rotundum", "Optic canal"], "Middle meningeal artery enters through foramen spinosum."),
            q("Mandibular nerve exits cranial cavity through:", "Foramen ovale", ["Foramen spinosum", "Superior orbital fissure", "Jugular foramen"], "V3 passes through foramen ovale to infratemporal fossa."),
            q("Chorda tympani joins the:", "Lingual nerve", ["Inferior alveolar nerve", "Buccal nerve", "Auriculotemporal nerve"], "It carries taste from anterior two-thirds tongue and parasympathetic fibers."),
            q("The otic ganglion is functionally related to:", "Parotid secretion", ["Lacrimal secretion", "Submandibular secretion", "Pupil constriction"], "Postganglionic fibers reach parotid through auriculotemporal nerve."),
            q("The inferior alveolar nerve enters the mandible through:", "Mandibular foramen", ["Mental foramen", "Infraorbital foramen", "Incisive foramen"], "It enters mandibular canal through mandibular foramen."),
            q("The pterygoid venous plexus communicates with:", "Cavernous sinus", ["Straight sinus only", "Great saphenous vein", "Portal vein"], "Connections through emissary veins can transmit infection."),
            q("Lateral pterygoid mainly helps in:", "Protrusion and opening of mandible", ["Retraction only", "Eye closure", "Tongue protrusion"], "Lateral pterygoid pulls condyle/disc forward and assists opening."),
            q("The buccal nerve supplies sensory fibers to:", "Cheek mucosa and skin", ["Buccinator motor supply", "Parotid gland secretion", "Tongue muscles"], "Buccal nerve of V3 is sensory; buccinator motor supply is facial nerve."),
            q("A blow to the pterion causes extradural hemorrhage. Which artery is torn?", "Middle meningeal artery", ["Anterior cerebral artery", "Facial artery", "Occipital artery"], "The anterior branch of middle meningeal artery runs deep to pterion."),
            q("A dental block near the mandibular foramen anesthetizes lower teeth. Which nerve is targeted?", "Inferior alveolar nerve", ["Lingual nerve only", "Mental nerve only", "Chorda tympani"], "Inferior alveolar nerve supplies mandibular teeth before giving mental branch."),
            q("After third molar extraction, the patient loses taste from anterior tongue. Which nerve was injured?", "Chorda tympani fibers in lingual nerve", ["Hypoglossal nerve", "Glossopharyngeal nerve", "Greater petrosal nerve"], "Chorda tympani travels with lingual nerve near the mandibular third molar."),
            q("An infratemporal infection spreads to cavernous sinus. Which venous plexus forms the route?", "Pterygoid venous plexus", ["Suboccipital plexus", "Internal vertebral plexus only", "Azygos plexus"], "Pterygoid plexus communicates with cavernous sinus via emissary veins."),
            q("A patient cannot protrude the mandible and deviates jaw to the weak side. Which muscle is weak?", "Lateral pterygoid", ["Masseter", "Posterior belly of digastric", "Orbicularis oris"], "Unilateral lateral pterygoid weakness causes jaw deviation toward the lesion."),
        ]),
        ("orbit-eye", "Orbit and Eye", [
            q("The optic nerve passes through the:", "Optic canal", ["Superior orbital fissure", "Inferior orbital fissure", "Foramen rotundum"], "CN II enters orbit through the optic canal with ophthalmic artery."),
            q("Most extraocular muscles arise from the:", "Common tendinous ring", ["Orbital septum", "Lacrimal sac", "Zygomatic arch"], "Recti and some muscles arise around the optic canal from the annular tendon."),
            q("Superior oblique is supplied by:", "Trochlear nerve", ["Oculomotor nerve", "Abducens nerve", "Optic nerve"], "CN IV supplies superior oblique."),
            q("Lateral rectus is supplied by:", "Abducens nerve", ["Trochlear nerve", "Facial nerve", "Maxillary nerve"], "CN VI abducts the eye through lateral rectus."),
            q("Parasympathetic fibers to sphincter pupillae relay in:", "Ciliary ganglion", ["Pterygopalatine ganglion", "Otic ganglion", "Submandibular ganglion"], "Preganglionic fibers from CN III synapse in ciliary ganglion."),
            q("The lacrimal gland receives secretomotor fibers from:", "Facial nerve pathway", ["Hypoglossal nerve", "Accessory nerve", "Abducens nerve"], "Parasympathetic fibers reach lacrimal gland via greater petrosal and pterygopalatine ganglion."),
            q("The ophthalmic artery is a branch of:", "Internal carotid artery", ["External carotid artery", "Maxillary artery", "Facial artery"], "It enters orbit through optic canal."),
            q("The infraorbital nerve is a branch of:", "Maxillary nerve", ["Ophthalmic nerve", "Mandibular nerve", "Facial nerve"], "V2 continues as infraorbital nerve."),
            q("The superior orbital fissure transmits CN III, IV, VI and:", "Ophthalmic division of trigeminal", ["Optic nerve", "Facial nerve", "Hypoglossal nerve"], "V1 branches enter orbit through the superior orbital fissure."),
            q("The nasolacrimal duct drains into the:", "Inferior meatus", ["Middle meatus", "Superior meatus", "Sphenoethmoidal recess"], "Tears drain to inferior meatus of nose."),
            q("A patient has ptosis, lateral squint and dilated pupil. Which nerve is compressed?", "Oculomotor nerve", ["Trochlear nerve", "Abducens nerve", "Optic nerve"], "CN III palsy affects levator, most extraocular muscles and parasympathetic pupillary fibers."),
            q("A fracture of orbital floor causes diplopia on upward gaze. Which muscle is trapped?", "Inferior rectus", ["Superior rectus", "Lateral rectus", "Superior oblique"], "Blowout fracture can entrap inferior rectus and restrict elevation."),
            q("A patient tilts head away from the affected side to reduce vertical diplopia. Which nerve palsy is typical?", "Trochlear nerve", ["Abducens nerve", "Facial nerve", "Optic nerve"], "Superior oblique palsy causes vertical diplopia improved by compensatory head tilt."),
            q("Cavernous sinus thrombosis causes ophthalmoplegia with sensory loss over forehead. Which trigeminal division is involved?", "Ophthalmic nerve", ["Mandibular nerve", "Maxillary nerve only", "Facial nerve"], "V1 runs in the lateral wall of cavernous sinus and supplies forehead/cornea."),
            q("Loss of corneal reflex afferent limb follows injury to which nerve?", "Nasociliary branch of ophthalmic nerve", ["Facial motor branch", "Infraorbital nerve", "Hypoglossal nerve"], "Corneal sensation is carried by nasociliary nerve of V1."),
        ]),
        ("nose-mouth-pharynx", "Nose, Oral Cavity and Pharynx", [
            q("The maxillary sinus opens into the:", "Middle meatus", ["Inferior meatus", "Superior meatus", "Sphenoethmoidal recess"], "Most paranasal sinuses drain into middle meatus."),
            q("Epistaxis commonly occurs at:", "Little area of nasal septum", ["Posterior tongue", "Tonsillar fossa", "Piriform fossa"], "Kiesselbach plexus is a common anterior bleeding site."),
            q("General sensation from anterior two-thirds tongue is by:", "Lingual nerve", ["Chorda tympani", "Glossopharyngeal nerve", "Hypoglossal nerve"], "Lingual nerve carries general sensation; chorda tympani carries taste."),
            q("Taste from posterior one-third tongue is by:", "Glossopharyngeal nerve", ["Facial nerve", "Hypoglossal nerve", "Vagus nerve"], "CN IX supplies taste and general sensation from posterior one-third tongue."),
            q("Motor supply of tongue muscles is mainly:", "Hypoglossal nerve", ["Glossopharyngeal nerve", "Vagus nerve", "Mandibular nerve"], "All intrinsic and most extrinsic tongue muscles are supplied by CN XII."),
            q("Palatine tonsil lies between palatoglossal and:", "Palatopharyngeal arches", ["Salpingopharyngeal folds", "Vocal folds", "Aryepiglottic folds"], "The tonsil occupies the tonsillar fossa."),
            q("The auditory tube opens into the:", "Nasopharynx", ["Oropharynx", "Laryngopharynx", "Oral vestibule"], "The pharyngotympanic tube opens on lateral wall of nasopharynx."),
            q("Most pharyngeal muscles are supplied by:", "Vagus nerve", ["Hypoglossal nerve", "Facial nerve", "Oculomotor nerve"], "Pharyngeal plexus with vagal fibers supplies most pharyngeal muscles."),
            q("Stylopharyngeus is supplied by:", "Glossopharyngeal nerve", ["Vagus nerve", "Facial nerve", "Accessory nerve"], "Stylopharyngeus is the main motor muscle of CN IX."),
            q("The gag reflex afferent limb is mainly:", "Glossopharyngeal nerve", ["Vagus nerve", "Hypoglossal nerve", "Facial nerve"], "CN IX carries sensation from oropharynx for gag reflex."),
            q("A maxillary sinus infection causes upper toothache. Which nerve pathway explains this?", "Superior alveolar branches of maxillary nerve", ["Inferior alveolar nerve", "Hypoglossal nerve", "Recurrent laryngeal nerve"], "Superior alveolar nerves supply maxillary teeth and sinus mucosa."),
            q("A tonsillectomy causes troublesome bleeding from the tonsillar bed. Which artery is classically involved?", "Tonsillar branch of facial artery", ["Middle meningeal artery", "Cystic artery", "Inferior thyroid artery"], "The tonsillar branch of facial artery is the main arterial supply to palatine tonsil."),
            q("A lesion of hypoglossal nerve causes protruded tongue to deviate to which side?", "Toward the lesion", ["Away from lesion", "Always upward", "No deviation"], "The intact genioglossus pushes the tongue toward the paralyzed side."),
            q("Food regurgitates into the nose after palatal paralysis. Which nerve is most likely affected?", "Vagus nerve", ["Hypoglossal nerve", "Optic nerve", "Abducens nerve"], "Vagus supplies most soft palate muscles except tensor veli palatini."),
            q("Middle ear infection spreads from nasopharynx in a child through which tube?", "Pharyngotympanic tube", ["Nasolacrimal duct", "Parotid duct", "Thyroglossal duct"], "The auditory tube connects nasopharynx to middle ear."),
        ]),
        ("larynx-neck", "Larynx and Neck", [
            q("The thyroid cartilage forms the:", "Laryngeal prominence", ["Cricoid arch", "Epiglottic vallecula", "Carina"], "The thyroid cartilage is the largest laryngeal cartilage."),
            q("The only complete ring of cartilage in airway is:", "Cricoid cartilage", ["Thyroid cartilage", "Epiglottis", "Arytenoid cartilage"], "Cricoid is a complete signet-ring cartilage."),
            q("The vocal folds attach posteriorly to:", "Arytenoid cartilages", ["Hyoid bone", "First tracheal ring", "Mandible"], "Arytenoids move the vocal ligaments."),
            q("All intrinsic laryngeal muscles except cricothyroid are supplied by:", "Recurrent laryngeal nerve", ["External laryngeal nerve", "Hypoglossal nerve", "Glossopharyngeal nerve"], "Recurrent laryngeal supplies most intrinsic laryngeal muscles."),
            q("Cricothyroid is supplied by:", "External laryngeal nerve", ["Internal laryngeal nerve", "Recurrent laryngeal nerve", "Ansa cervicalis"], "External branch of superior laryngeal nerve tenses vocal folds."),
            q("Sensation above vocal folds is by:", "Internal laryngeal nerve", ["External laryngeal nerve", "Hypoglossal nerve", "Ansa cervicalis"], "Internal laryngeal nerve pierces thyrohyoid membrane."),
            q("The carotid sheath contains common/internal carotid artery, internal jugular vein and:", "Vagus nerve", ["Phrenic nerve", "Hypoglossal nerve", "Accessory nerve"], "Vagus nerve lies within the carotid sheath."),
            q("The ansa cervicalis supplies:", "Infrahyoid muscles except thyrohyoid", ["Muscles of mastication", "Extraocular muscles", "Tongue intrinsic muscles"], "Ansa cervicalis innervates most strap muscles."),
            q("The phrenic nerve descends on:", "Anterior scalene", ["Middle scalene", "Masseter", "Mylohyoid"], "Phrenic nerve runs on anterior scalene deep to prevertebral fascia."),
            q("The thyroid gland is enclosed by:", "Pretracheal fascia", ["Parotid fascia", "Buccopharyngeal fascia", "Temporal fascia"], "Pretracheal fascia forms a false capsule around thyroid."),
            q("After thyroidectomy, the patient has hoarseness. Which nerve was injured?", "Recurrent laryngeal nerve", ["Internal laryngeal nerve only", "Hypoglossal nerve", "Facial nerve"], "Recurrent laryngeal nerve supplies vocal fold abductors/adductors."),
            q("A singer loses ability to hit high notes after surgery near superior thyroid vessels. Which nerve is injured?", "External laryngeal nerve", ["Internal laryngeal nerve", "Ansa cervicalis", "Marginal mandibular nerve"], "External laryngeal nerve supplies cricothyroid, which tenses vocal cords."),
            q("A foreign body lodges in the piriform fossa and causes loss of supraglottic sensation. Which nerve is at risk?", "Internal laryngeal nerve", ["External laryngeal nerve", "Hypoglossal nerve", "Facial nerve"], "Internal laryngeal nerve lies beneath mucosa of piriform fossa."),
            q("A deep neck infection spreads from pharynx to posterior mediastinum. Which space is the dangerous route?", "Retropharyngeal space", ["Carotid triangle", "Submental triangle", "Temporal fossa"], "The retropharyngeal/danger space can track infection into mediastinum."),
            q("During central venous catheterization, the target vein in the carotid sheath is:", "Internal jugular vein", ["External jugular vein", "Anterior jugular vein", "Vertebral vein"], "The internal jugular vein lies lateral to carotid artery in the sheath."),
        ]),
        ("vessels-lymph-development", "Vessels, Lymphatics and Development", [
            q("The common carotid artery bifurcates near the upper border of:", "Thyroid cartilage", ["Cricoid cartilage", "Hyoid lesser horn", "First rib"], "Bifurcation is around C4, upper border of thyroid cartilage."),
            q("The carotid sinus functions as a:", "Baroreceptor", ["Chemoreceptor", "Taste receptor", "Motor ganglion"], "Carotid sinus senses blood pressure."),
            q("The carotid body functions as a:", "Chemoreceptor", ["Baroreceptor", "Lymph node", "Salivary gland"], "Carotid body senses blood gases."),
            q("The external carotid artery gives the superior thyroid, lingual and:", "Facial arteries", ["Vertebral arteries", "Ophthalmic arteries", "Basilar artery"], "These are anterior branches of external carotid."),
            q("The internal jugular vein begins at the:", "Jugular foramen", ["Foramen ovale", "Optic canal", "Mental foramen"], "It continues from sigmoid sinus at the jugular foramen."),
            q("Deep cervical lymph nodes lie mainly along:", "Internal jugular vein", ["External carotid artery only", "Facial vein only", "Subclavian artery only"], "The internal jugular chain receives lymph from head and neck."),
            q("The thoracic duct usually ends at the:", "Left venous angle", ["Right venous angle", "Portal vein", "Azygos arch"], "It drains into the junction of left IJV and subclavian vein."),
            q("The right lymphatic duct drains into the:", "Right venous angle", ["Left venous angle", "Inferior vena cava", "Portal vein"], "It drains the right upper quadrant."),
            q("The thyroid descends from the foramen cecum through the:", "Thyroglossal duct", ["Pharyngotympanic tube", "Nasolacrimal duct", "Parotid duct"], "Persistent duct remnants can form cysts."),
            q("The first pharyngeal arch gives rise to:", "Muscles of mastication", ["Muscles of facial expression", "Stylopharyngeus", "Cricothyroid"], "First arch is supplied by trigeminal nerve and forms mastication muscles."),
            q("Pressure on carotid sinus causes fainting by stimulating which nerve?", "Glossopharyngeal nerve", ["Hypoglossal nerve", "Facial nerve", "Accessory nerve"], "Carotid sinus afferents travel via CN IX."),
            q("A lateral neck mass anterior to sternocleidomastoid is a branchial cyst. It most often relates to which arch anomaly?", "Second pharyngeal cleft", ["First pouch", "Fourth arch artery", "Thyroglossal duct"], "Second cleft cysts commonly present along anterior border of SCM."),
            q("A midline neck cyst moves on tongue protrusion. What embryological tract explains this?", "Thyroglossal duct", ["Second branchial cleft", "Carotid sheath", "Nasolacrimal duct"], "Thyroglossal cysts are attached to the tongue base tract and move with swallowing/tongue protrusion."),
            q("Virchow node enlargement suggests abdominal malignancy because it receives lymph through:", "Thoracic duct", ["Right lymphatic duct", "Facial vein", "External carotid artery"], "Left supraclavicular node is near thoracic duct termination."),
            q("A tumor at jugular foramen causes dysphagia, hoarseness and loss of gag reflex. Which cranial nerves are involved?", "IX, X and XI", ["III, IV and VI", "V1 and V2", "VII and VIII only"], "Glossopharyngeal, vagus and accessory nerves pass through jugular foramen."),
        ]),
    ],
    "Brain": [
        ("meninges-csf-ventricles", "Meninges, CSF and Ventricles", [
            q("The outer meningeal layer closely attached to skull is:", "Dura mater", ["Arachnoid mater", "Pia mater", "Ependyma"], "Cranial dura has periosteal and meningeal layers."),
            q("CSF is produced mainly by:", "Choroid plexus", ["Arachnoid granulations", "Falx cerebri", "Corpus callosum"], "Choroid plexuses produce CSF within ventricles."),
            q("CSF is absorbed mainly through:", "Arachnoid granulations", ["Choroid plexus", "Pineal gland", "Pituitary gland"], "Arachnoid villi/granulations drain CSF into venous sinuses."),
            q("The lateral ventricles communicate with third ventricle through:", "Interventricular foramina", ["Cerebral aqueduct", "Median aperture", "Central canal only"], "Foramina of Monro connect lateral to third ventricles."),
            q("The third ventricle communicates with fourth ventricle through:", "Cerebral aqueduct", ["Interventricular foramen", "Foramen magnum", "Superior sagittal sinus"], "The aqueduct passes through midbrain."),
            q("The fourth ventricle opens to subarachnoid space through median and:", "Lateral apertures", ["Intervertebral foramina", "Optic canals", "Jugular foramina"], "Foramina of Magendie and Luschka allow CSF exit."),
            q("Falx cerebri lies between:", "Cerebral hemispheres", ["Cerebellar hemispheres", "Temporal lobes and pons", "Thalami only"], "It is a dural fold in the longitudinal fissure."),
            q("Tentorium cerebelli separates cerebrum from:", "Cerebellum", ["Medulla", "Spinal cord", "Pituitary"], "It forms a dural roof over posterior cranial fossa."),
            q("The superior sagittal sinus runs in attached margin of:", "Falx cerebri", ["Tentorium free edge", "Falx cerebelli", "Diaphragma sellae"], "It lies along the superior margin of falx cerebri."),
            q("The cavernous sinus contains the internal carotid artery and:", "Abducens nerve", ["Optic nerve", "Olfactory tract", "Facial nerve"], "CN VI and ICA pass through the sinus; III, IV, V1, V2 in lateral wall."),
            q("A child has enlarged head and dilated ventricles from aqueduct stenosis. Which CSF pathway is blocked?", "Third to fourth ventricle", ["Lateral to third ventricle", "Subarachnoid to venous sinus", "Central canal to lumbar cistern"], "Aqueduct obstruction blocks CSF flow from third to fourth ventricle."),
            q("A head injury tears middle meningeal artery and causes a lucid interval. Which bleeding is likely?", "Extradural hemorrhage", ["Subarachnoid hemorrhage", "Subdural hemorrhage", "Intracerebral hemorrhage"], "Arterial bleeding between skull and dura causes extradural hematoma."),
            q("Elderly patient develops slowly progressive confusion after tearing bridging veins. Which hemorrhage is likely?", "Subdural hemorrhage", ["Extradural hemorrhage", "Intraventricular hemorrhage only", "Epidural spinal abscess"], "Bridging veins tear between dura and arachnoid."),
            q("Sudden worst headache with blood in CSF suggests rupture into which space?", "Subarachnoid space", ["Epidural space", "Subdural space", "Ventricular choroid plexus only"], "Subarachnoid hemorrhage mixes with CSF."),
            q("Cavernous sinus thrombosis causes lateral rectus palsy first. Which nerve is most exposed within the sinus?", "Abducens nerve", ["Optic nerve", "Facial nerve", "Hypoglossal nerve"], "CN VI runs through the cavernous sinus beside the internal carotid artery."),
        ]),
        ("cerebrum-cortex", "Cerebrum and Cerebral Cortex", [
            q("The primary motor cortex lies in the:", "Precentral gyrus", ["Postcentral gyrus", "Cuneus", "Superior temporal gyrus"], "Brodmann area 4 occupies the precentral gyrus."),
            q("The primary somatosensory cortex lies in the:", "Postcentral gyrus", ["Precentral gyrus", "Inferior frontal gyrus", "Uncus"], "Areas 3, 1 and 2 occupy the postcentral gyrus."),
            q("The primary visual cortex lies around the:", "Calcarine sulcus", ["Central sulcus", "Lateral sulcus", "Parieto-occipital sulcus only"], "Area 17 is on banks of calcarine sulcus."),
            q("The primary auditory cortex lies in:", "Transverse temporal gyri", ["Lingual gyrus", "Precentral gyrus", "Cingulate gyrus"], "Heschl gyri receive auditory input."),
            q("Broca area is usually in the:", "Inferior frontal gyrus", ["Superior temporal gyrus", "Postcentral gyrus", "Occipital pole"], "Dominant inferior frontal gyrus mediates motor speech."),
            q("Wernicke area is usually in the:", "Posterior superior temporal region", ["Precentral gyrus", "Anterior cingulate", "Paracentral lobule"], "It mediates language comprehension in dominant hemisphere."),
            q("The corpus callosum connects:", "Two cerebral hemispheres", ["Cerebrum to spinal cord", "Cerebellum to pons", "Thalamus to pituitary"], "It is the major commissural fiber bundle."),
            q("The internal capsule carries:", "Projection fibers", ["Only commissural fibers", "Only CSF", "Only venous blood"], "It contains corticospinal, corticobulbar and thalamocortical fibers."),
            q("Leg area of motor cortex lies mainly in:", "Paracentral lobule", ["Lateral precentral face area", "Insula", "Temporal pole"], "Lower-limb representation is medial."),
            q("Face area of motor cortex lies mainly on:", "Lateral precentral gyrus", ["Medial paracentral lobule", "Cuneus", "Precuneus only"], "Face and tongue motor areas are lateral."),
            q("A stroke affecting the left inferior frontal gyrus causes nonfluent speech with comprehension preserved. What area is involved?", "Broca area", ["Wernicke area", "Primary visual cortex", "Hippocampus"], "Broca aphasia is expressive/nonfluent."),
            q("A patient speaks fluently but nonsensically and cannot understand commands. Which dominant cortical region is damaged?", "Wernicke area", ["Broca area", "Precentral hand area", "Calcarine cortex"], "Wernicke aphasia affects comprehension with fluent output."),
            q("A lesion in right parietal association cortex causes neglect of the left side. Which function is impaired?", "Spatial attention", ["Motor speech", "Primary vision only", "Smell"], "Non-dominant parietal cortex is important for spatial awareness."),
            q("A small infarct in posterior limb of internal capsule causes dense contralateral weakness. Why?", "Compact corticospinal fibers are packed together", ["CSF is blocked", "Optic nerve is compressed", "Cerebellar cortex is destroyed"], "Internal capsule contains tightly packed descending motor fibers."),
            q("A parasagittal meningioma compresses medial motor cortex. Which body part is most affected?", "Contralateral leg", ["Contralateral face only", "Ipsilateral hand only", "Tongue taste"], "Lower limb area is medial on paracentral lobule."),
        ]),
        ("basal-ganglia-diencephalon", "Basal Ganglia and Diencephalon", [
            q("The corpus striatum includes caudate nucleus and:", "Lentiform nucleus", ["Amygdala only", "Hippocampus", "Red nucleus"], "Caudate plus lentiform nucleus form corpus striatum."),
            q("The lentiform nucleus includes putamen and:", "Globus pallidus", ["Caudate head", "Thalamus", "Subthalamic nucleus"], "Putamen and globus pallidus form lentiform nucleus."),
            q("The thalamus is the major relay for:", "Sensory pathways to cortex", ["CSF production only", "Facial expression muscles", "Pituitary hormones only"], "Most sensory pathways relay in thalamus before cortex."),
            q("The hypothalamus is important for:", "Autonomic and endocrine control", ["Voluntary finger movement only", "Hearing only", "Lens accommodation only"], "It regulates homeostasis, autonomic output and pituitary function."),
            q("The lateral geniculate body relays:", "Vision", ["Hearing", "Smell", "Taste"], "Visual fibers from optic tract relay in LGN."),
            q("The medial geniculate body relays:", "Hearing", ["Vision", "Pain", "Balance"], "Auditory pathway relays in MGN."),
            q("The subthalamic nucleus lesion classically causes:", "Hemiballismus", ["Aphasia", "Anosmia", "Internuclear ophthalmoplegia"], "Contralateral flinging movements follow subthalamic lesions."),
            q("Dopaminergic input to basal ganglia comes mainly from:", "Substantia nigra pars compacta", ["Red nucleus", "Dentate nucleus", "Inferior olive"], "Nigrostriatal dopamine modulates movement circuits."),
            q("The pineal gland is part of the:", "Epithalamus", ["Metathalamus only", "Subthalamus", "Hypophysis"], "Pineal lies in epithalamic region."),
            q("The mammillary bodies belong to:", "Hypothalamus", ["Thalamus", "Midbrain tectum", "Cerebellum"], "They are hypothalamic nuclei involved in memory circuits."),
            q("A patient has resting tremor, rigidity and bradykinesia. Loss of neurons in which structure explains this?", "Substantia nigra pars compacta", ["Lateral geniculate body", "Mammillary body", "Dentate nucleus"], "Parkinsonism follows degeneration of nigrostriatal dopaminergic neurons."),
            q("A lacunar stroke in thalamus causes contralateral sensory loss. Which role of thalamus explains this?", "Major sensory relay to cortex", ["Primary motor origin", "CSF absorption", "Facial muscle innervation"], "Thalamic nuclei relay somatosensory information to cortex."),
            q("A lesion of subthalamic nucleus causes violent flinging movements of opposite limbs. What is the movement disorder?", "Hemiballismus", ["Chorea from caudate only", "Ataxia", "Myoclonus of palate"], "Subthalamic nucleus lesions reduce indirect pathway control."),
            q("A pituitary tumor compresses hypothalamic region and optic chiasm. Which endocrine-control center is nearby?", "Hypothalamus", ["Caudate nucleus", "Red nucleus", "Inferior colliculus"], "The hypothalamus lies above pituitary and controls hypophyseal secretion."),
            q("Memory impairment with mammillary body damage is classically seen in which syndrome?", "Wernicke-Korsakoff syndrome", ["Brown-Sequard syndrome", "Weber syndrome", "Horner syndrome"], "Mammillary bodies are part of Papez circuit and affected in thiamine deficiency."),
        ]),
        ("brainstem-cranial-nuclei", "Brainstem and Cranial Nerve Nuclei", [
            q("The midbrain contains the:", "Cerebral aqueduct", ["Fourth ventricle floor only", "Lateral ventricle", "Central canal only"], "The aqueduct passes through midbrain."),
            q("The pons is related posteriorly to the:", "Fourth ventricle", ["Third ventricle", "Lateral ventricle", "Superior sagittal sinus"], "The dorsal pons forms part of the floor of the fourth ventricle."),
            q("The medulla contains pyramids formed by:", "Corticospinal tracts", ["Dorsal columns only", "Optic radiations", "Auditory radiations"], "Pyramids are descending motor tracts."),
            q("Most corticospinal fibers decussate in the:", "Caudal medulla", ["Midbrain tectum", "Pons only", "Thalamus"], "Pyramidal decussation occurs in caudal medulla."),
            q("The oculomotor nucleus is in the:", "Midbrain", ["Pons", "Medulla", "Thalamus"], "CN III nucleus lies in midbrain."),
            q("The facial motor nucleus is in the:", "Pons", ["Midbrain", "Medulla", "Cerebellar cortex"], "CN VII motor nucleus is in caudal pons."),
            q("The hypoglossal nucleus is in the:", "Medulla", ["Midbrain", "Thalamus", "Basal ganglia"], "CN XII nucleus lies in medulla near midline."),
            q("The nucleus ambiguus supplies motor fibers to:", "Pharynx and larynx", ["Extraocular muscles", "Facial expression", "Tongue intrinsic muscles"], "It contributes motor fibers to IX, X and cranial XI."),
            q("The solitary nucleus receives:", "Taste and visceral afferents", ["Corticospinal fibers", "Optic radiation", "Auditory ossicle vibration"], "Nucleus tractus solitarius processes taste and visceral sensory information."),
            q("The medial lemniscus carries:", "Fine touch, vibration and proprioception", ["Pain and temperature only", "Vision", "Smell"], "Dorsal column fibers decussate and ascend as medial lemniscus."),
            q("A medial medullary lesion causes contralateral hemiparesis and ipsilateral tongue weakness. Which artery is often involved?", "Anterior spinal artery", ["Posterior cerebral artery", "Middle meningeal artery", "Superior cerebellar artery"], "Medial medullary syndrome involves pyramid and hypoglossal fibers."),
            q("A lateral medullary infarct causes dysphagia, hoarseness and loss of gag. Which nucleus is involved?", "Nucleus ambiguus", ["Oculomotor nucleus", "Facial nucleus", "Edinger-Westphal nucleus"], "Nucleus ambiguus supplies pharyngeal/laryngeal muscles."),
            q("A pontine lesion damages abducens fascicles and corticospinal tract. What eye sign is expected?", "Ipsilateral lateral rectus palsy", ["Contralateral ptosis only", "Bilateral blindness", "Loss of smell"], "CN VI fibers in pons supply ipsilateral lateral rectus."),
            q("A midbrain lesion with CN III palsy and contralateral hemiparesis is called:", "Weber syndrome", ["Wallenberg syndrome", "Brown-Sequard syndrome", "Dejerine syndrome"], "Weber syndrome involves oculomotor fibers and cerebral peduncle."),
            q("Loss of pain and temperature from face with ipsilateral ataxia suggests lateral brainstem involvement of which tract/nucleus?", "Spinal trigeminal nucleus/tract", ["Optic tract", "Hypoglossal nucleus", "Dorsal column nucleus only"], "Spinal trigeminal system carries facial pain and temperature."),
        ]),
        ("cerebellum", "Cerebellum", [
            q("The cerebellum is located in the:", "Posterior cranial fossa", ["Anterior cranial fossa", "Middle cranial fossa", "Sella turcica"], "It lies behind pons and medulla under tentorium."),
            q("The vermis mainly coordinates:", "Axial posture and gait", ["Language comprehension", "Smell", "Pupillary reflex only"], "Midline cerebellum controls trunk and gait."),
            q("Cerebellar hemispheres mainly coordinate:", "Limb movements", ["Visceral pain", "Hearing", "CSF absorption"], "Lateral hemispheres refine skilled limb movement."),
            q("The flocculonodular lobe is related to:", "Vestibular function", ["Speech comprehension", "Endocrine control", "Smell"], "It connects with vestibular nuclei for balance and eye movement."),
            q("The dentate nucleus is a:", "Deep cerebellar nucleus", ["Basal ganglion", "Thalamic nucleus", "Midbrain nucleus"], "Dentate is the largest deep cerebellar nucleus."),
            q("The superior cerebellar peduncle mainly carries:", "Cerebellar output", ["Olfactory fibers", "Optic radiations", "CSF"], "Most output leaves through superior cerebellar peduncle."),
            q("The middle cerebellar peduncle carries fibers from:", "Pons", ["Medulla only", "Spinal cord only", "Thalamus only"], "Pontocerebellar fibers enter through middle peduncle."),
            q("The inferior cerebellar peduncle carries input from:", "Medulla and spinal cord", ["Frontal cortex directly", "Optic nerve", "Internal capsule only"], "It carries vestibular, spinocerebellar and olivocerebellar inputs."),
            q("Cerebellar lesions usually produce signs on the:", "Ipsilateral side", ["Contralateral side", "Both eyes only", "No side"], "Cerebellar output crosses twice, so deficits are ipsilateral."),
            q("The posterior inferior cerebellar artery arises from:", "Vertebral artery", ["Basilar artery", "Internal carotid artery", "Middle cerebral artery"], "PICA is a vertebral artery branch."),
            q("A patient has wide-based gait and truncal instability. Which cerebellar region is likely affected?", "Vermis", ["Lateral hemisphere only", "Dentate nucleus only", "Optic radiation"], "Vermian lesions disturb axial posture and gait."),
            q("A patient has intention tremor and dysmetria of the right arm. Which side of cerebellum is affected?", "Right cerebellar hemisphere", ["Left cerebellar hemisphere", "Left frontal cortex only", "Right occipital lobe"], "Cerebellar limb signs are ipsilateral."),
            q("A child with medulloblastoma obstructs fourth ventricle. Which CSF problem develops?", "Non-communicating hydrocephalus", ["Subdural hemorrhage", "Epidural hematoma", "Facial palsy only"], "Posterior fossa tumors can block CSF flow from fourth ventricle."),
            q("A lesion of flocculonodular lobe causes nystagmus and balance difficulty. Which functional system is involved?", "Vestibulocerebellum", ["Cerebrocerebellum only", "Limbic system", "Language cortex"], "Flocculonodular lobe coordinates vestibular reflexes and balance."),
            q("An infarct of PICA causes cerebellar ataxia plus lateral medullary signs. Which artery is involved?", "Posterior inferior cerebellar artery", ["Anterior cerebral artery", "Middle meningeal artery", "Anterior communicating artery"], "PICA supplies inferior cerebellum and lateral medulla territory."),
        ]),
        ("blood-supply-functional", "Blood Supply and Functional Pathways", [
            q("The internal carotid artery gives rise to anterior cerebral and:", "Middle cerebral arteries", ["Posterior cerebral arteries only", "Basilar artery", "Vertebral arteries"], "ICA terminal branches include ACA and MCA."),
            q("The vertebral arteries unite to form the:", "Basilar artery", ["Internal carotid artery", "Middle cerebral artery", "Anterior cerebral artery"], "Vertebral arteries join at pontomedullary junction."),
            q("Posterior cerebral artery is usually a terminal branch of:", "Basilar artery", ["Internal carotid artery", "External carotid artery", "Anterior communicating artery"], "The basilar bifurcates into PCAs."),
            q("Anterior communicating artery connects the:", "Anterior cerebral arteries", ["Middle cerebral arteries", "Posterior cerebral arteries", "Vertebral arteries"], "It completes the anterior part of circle of Willis."),
            q("Posterior communicating artery connects internal carotid to:", "Posterior cerebral artery", ["Anterior cerebral artery", "Basilar artery directly", "Vertebral artery"], "It forms the lateral connection in circle of Willis."),
            q("Middle cerebral artery supplies much of the:", "Lateral cerebral hemisphere", ["Medial leg cortex", "Cerebellar vermis", "Medulla only"], "MCA supplies lateral frontal, parietal and temporal cortex."),
            q("Anterior cerebral artery supplies mainly:", "Medial frontal and parietal cortex", ["Lateral temporal cortex", "Occipital pole only", "Cerebellum"], "ACA territory includes medial leg motor/sensory areas."),
            q("Posterior cerebral artery supplies:", "Occipital cortex", ["Lateral frontal cortex", "Broca area only", "Cerebellar tonsil only"], "PCA supplies visual cortex in occipital lobe."),
            q("Lenticulostriate arteries arise mainly from:", "Middle cerebral artery", ["Anterior spinal artery", "PICA", "External carotid artery"], "They supply internal capsule and basal ganglia."),
            q("The corticospinal tract crosses mainly at:", "Pyramidal decussation", ["Optic chiasm", "Corpus callosum", "Superior colliculus"], "Most fibers cross in caudal medulla."),
            q("A right MCA stroke causes left face-arm weakness and aphasia if dominant hemisphere is involved. Which territory is affected?", "Lateral cerebral cortex", ["Medial leg cortex", "Occipital pole only", "Cerebellar vermis"], "MCA supplies face/arm motor cortex and dominant language areas."),
            q("A left ACA stroke causes weakness mainly of the right leg. Which cortical area is ischemic?", "Medial motor cortex", ["Lateral face cortex", "Primary auditory cortex", "Cerebellar hemisphere"], "ACA supplies medial frontal/parietal cortex containing leg representation."),
            q("A PCA infarct causes contralateral homonymous hemianopia. Which cortex is involved?", "Primary visual cortex", ["Primary auditory cortex", "Broca area", "Postcentral hand area"], "PCA supplies occipital visual cortex."),
            q("Hypertensive hemorrhage in internal capsule causes dense contralateral paralysis. Which small arteries commonly rupture?", "Lenticulostriate arteries", ["Short gastric arteries", "Middle meningeal arteries", "Posterior auricular arteries"], "Lenticulostriate arteries are vulnerable penetrating branches."),
            q("An aneurysm of posterior communicating artery compresses CN III. What eye finding is expected?", "Ptosis with dilated pupil", ["Loss of smell only", "Tongue deviation", "Facial numbness only"], "CN III parasympathetic fibers are superficial and compressed by PCom aneurysm."),
        ]),
    ],
}


def main():
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    new_questions = []
    for chapter, topics in CHAPTERS.items():
        for topic_index, (slug, topic, rows) in enumerate(topics):
            if len(rows) != 15:
                raise ValueError(f"{chapter} / {topic} has {len(rows)} questions")
            for question_index, row in enumerate(rows, 1):
                options = list(row["wrong"])
                answer_index = (topic_index + question_index - 1) % 4
                options.insert(answer_index, row["answer"])
                new_questions.append({
                    **BASE,
                    "chapterTitle": chapter,
                    "id": f"anatomy-{chapter.lower().replace(' and ', '-').replace(' ', '-')}-{slug}-{question_index:02d}",
                    "topic": topic,
                    "difficulty": "moderate" if question_index <= 5 else "high" if question_index <= 10 else "very high",
                    "prompt": row["prompt"],
                    "options": options,
                    "answerIndex": answer_index,
                    "answer": row["answer"],
                    "explanation": row["explanation"],
                })

    target_chapters = set(CHAPTERS)
    data["questions"] = [
        x for x in data.get("questions", [])
        if not (x.get("subjectId") == "anatomy" and x.get("chapterTitle") in target_chapters)
    ] + new_questions

    expected = sum(len(topics) * 15 for topics in CHAPTERS.values())
    if len(new_questions) != expected:
        raise AssertionError(f"Expected {expected}, got {len(new_questions)}")
    if len({x["id"] for x in new_questions}) != len(new_questions):
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in new_questions):
        raise AssertionError("Bad answer index")
    data_questions = data.get("questions", [])
    for chapter, topics in CHAPTERS.items():
        chapter_questions = [x for x in data_questions if x.get("subjectId") == "anatomy" and x.get("chapterTitle") == chapter]
        if len(chapter_questions) != len(topics) * 15:
            raise AssertionError(f"{chapter} count mismatch: {len(chapter_questions)}")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(new_questions)} questions across {len(CHAPTERS)} chapters.")


if __name__ == "__main__":
    main()
