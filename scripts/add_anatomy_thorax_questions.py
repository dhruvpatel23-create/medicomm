import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Thorax"
BASE = {"subjectId": "anatomy", "subjectTitle": "Anatomy", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("introduction", "Introduction", [
        q("The thorax is primarily concerned with:", "Respiration and protection of heart and lungs", ["Digestion only", "Urine storage", "Fine manipulation"], "The thoracic cage protects vital cardiopulmonary organs and participates in breathing."),
        q("The superior thoracic aperture is bounded anteriorly by:", "Superior border of manubrium", ["Xiphoid process", "T12 vertebra", "Costal margin"], "The inlet is bounded by T1, first ribs/costal cartilages, and superior manubrium."),
        q("The inferior thoracic aperture is closed by:", "Diaphragm", ["Pleura", "Pericardium", "Serratus anterior"], "The diaphragm separates thoracic and abdominal cavities."),
        q("The thoracic cavity is divided into pleural cavities and:", "Mediastinum", ["Peritoneal cavity", "Vertebral canal", "Axilla"], "The mediastinum lies centrally between pleural cavities."),
        q("The sternum lies in the:", "Anterior median thoracic wall", ["Posterior wall", "Lateral wall only", "Thoracic inlet posteriorly"], "The sternum forms the anterior midline support."),
        q("The thoracic cage is formed by vertebrae, ribs, costal cartilages and:", "Sternum", ["Scapula", "Clavicle", "Humerus"], "Thoracic cage includes sternum anteriorly and thoracic vertebrae posteriorly."),
        q("Pump-handle movement increases mainly the:", "Anteroposterior diameter", ["Vertical diameter only", "Transverse diameter only", "Pelvic diameter"], "Upper rib movement raises sternum and increases AP diameter."),
        q("Bucket-handle movement increases mainly the:", "Transverse diameter", ["AP diameter only", "Cranial diameter", "Spinal canal diameter"], "Middle/lower ribs swing upward and outward, increasing transverse diameter."),
        q("The thoracic inlet transmits structures between:", "Neck and thorax", ["Thorax and pelvis", "Axilla and hand", "Abdomen and thigh"], "Trachea, esophagus, vessels, nerves and lymphatics pass through the superior aperture."),
        q("The costal margin is formed mainly by cartilages of ribs:", "7 to 10", ["1 to 3", "11 and 12 only", "2 to 5"], "The false rib cartilages form the costal margin."),
        q("A stab wound just above the clavicle may injure the lung apex because:", "Cervical pleura and apex project into root of neck", ["Lungs end at second rib", "Pleura is absent near neck", "Diaphragm reaches clavicle"], "The cupula of pleura and lung apex extend above the first rib into the neck."),
        q("During quiet inspiration, expansion of thoracic cavity mainly requires:", "Diaphragm contraction with external intercostal assistance", ["Internal intercostals only", "Abdominal wall contraction only", "Passive collapse"], "Diaphragm is the chief muscle of inspiration; external intercostals elevate ribs."),
        q("In severe respiratory distress, sternocleidomastoid and scalenes help by:", "Elevating upper ribs and sternum", ["Depressing ribs", "Closing glottis", "Compressing lungs directly"], "Accessory inspiratory muscles elevate the thoracic cage."),
        q("A tumor at the thoracic inlet causing hand muscle wasting and Horner syndrome suggests involvement of:", "Lower brachial plexus and sympathetic chain", ["Femoral nerve", "Facial nerve", "Phrenic nerve only"], "Apical/Pancoast lesions can affect T1 fibers and cervical sympathetic pathway."),
        q("A patient with flail chest ventilates poorly mainly because:", "Paradoxical movement reduces effective thoracic expansion", ["Pleura becomes thicker", "Heart stops rotating", "Ribs become more elastic"], "Segmental rib fractures create paradoxical movement and impair ventilation."),
    ]),
    ("bones-joints-thorax", "Bones and Joints of Thorax", [
        q("A typical rib has a head, neck, tubercle, shaft and:", "Angle", ["Olecranon", "Coracoid", "Radial styloid"], "Typical ribs include head, neck, tubercle, angle, and costal groove."),
        q("The head of a typical rib articulates with:", "Bodies of two adjacent thoracic vertebrae", ["Sternum directly", "Transverse process only", "Costal cartilage only"], "Typical rib heads articulate with demifacets of adjacent vertebral bodies."),
        q("The tubercle of a typical rib articulates with:", "Transverse process of corresponding vertebra", ["Body of sternum", "Xiphoid", "Intervertebral disc only"], "Costotransverse joint is between rib tubercle and transverse process."),
        q("The costal groove contains:", "Intercostal vein, artery and nerve", ["Thoracic duct only", "Azygos vein only", "Phrenic nerve"], "The VAN bundle runs in the costal groove along inferior rib border."),
        q("True ribs are ribs:", "1 to 7", ["8 to 10", "11 to 12", "2 to 8"], "True ribs attach directly to sternum via their own costal cartilages."),
        q("Floating ribs are:", "11 and 12", ["1 and 2", "7 and 8", "3 and 4"], "Ribs 11 and 12 have no anterior attachment."),
        q("The sternal angle is at the level of:", "Second costal cartilage", ["First lumbar vertebra", "Xiphoid tip", "T12 only"], "The second costal cartilage articulates at the manubriosternal joint."),
        q("The manubriosternal joint is usually a:", "Secondary cartilaginous joint", ["Plane synovial joint", "Fibrous suture", "Ball-and-socket joint"], "It is a symphysis and forms the sternal angle."),
        q("First rib is atypical because it has:", "Single facet on head and scalene tubercle", ["No head", "No groove", "Three tubercles"], "First rib has one facet and grooves for subclavian vessels separated by scalene tubercle."),
        q("The thoracic vertebrae are identified by:", "Costal facets", ["Transverse foramina", "Bifid spinous processes", "Massive kidney-shaped body only"], "Thoracic vertebrae articulate with ribs via costal facets."),
        q("A needle placed too close to the inferior border of a rib risks injuring:", "Intercostal neurovascular bundle", ["Internal thoracic artery only", "Phrenic nerve", "Thoracic duct"], "VAN bundle lies in the costal groove on the inferior border."),
        q("Counting ribs clinically often begins at the sternal angle because it marks:", "Second rib/costal cartilage", ["First floating rib", "Xiphoid", "T12 rib"], "The second costal cartilage is palpable at the sternal angle."),
        q("A first rib fracture is clinically serious because of nearby:", "Subclavian vessels and brachial plexus", ["Femoral vessels", "Median nerve in carpal tunnel", "Sciatic nerve"], "The first rib is protected; fracture implies high force and may injure subclavian vessels/plexus."),
        q("Thoracic kyphosis is accentuated in elderly osteoporosis mainly due to:", "Compression fractures of vertebral bodies", ["Dislocation of all ribs", "Sternal fracture only", "Pleural thickening"], "Osteoporotic wedge compression fractures increase kyphosis."),
        q("Pain from rib fracture worsens during breathing because:", "Ribs move at costovertebral and costotransverse joints", ["Ribs are fixed immobile", "Pleura has no sensation", "Diaphragm is paralyzed always"], "Rib movements during respiration stress fracture sites."),
    ]),
    ("wall-thorax", "Wall of Thorax", [
        q("The main muscles occupying intercostal spaces are:", "External, internal and innermost intercostals", ["Pectoralis major only", "Diaphragm only", "Serratus anterior only"], "Three intercostal muscle layers form thoracic wall proper."),
        q("External intercostals primarily assist in:", "Inspiration", ["Forced expiration only", "Swallowing", "Phonation only"], "External intercostals elevate ribs during inspiration."),
        q("Internal intercostals are most active during:", "Forced expiration", ["Quiet inspiration only", "Micturition", "Eye movement"], "Interosseous internal intercostals depress ribs in forced expiration."),
        q("Typical intercostal nerve is the anterior ramus of:", "Thoracic spinal nerve", ["Cervical plexus", "Lumbar plexus", "Vagus nerve"], "Intercostal nerves are thoracic anterior rami."),
        q("The intercostal neurovascular order in costal groove is:", "Vein, artery, nerve", ["Nerve, artery, vein", "Artery, vein, nerve", "Vein, nerve, artery"], "VAN from superior to inferior in costal groove."),
        q("Internal thoracic artery arises from:", "Subclavian artery", ["Axillary artery", "Aorta directly", "Brachiocephalic vein"], "It descends near sternum and gives anterior intercostals."),
        q("Posterior intercostal arteries mostly arise from:", "Thoracic aorta", ["Internal thoracic artery", "Pulmonary trunk", "Axillary artery"], "Most posterior intercostals arise from descending thoracic aorta."),
        q("Azygos vein drains into:", "Superior vena cava", ["Inferior vena cava", "Portal vein", "Left atrium"], "Azygos arches over right lung root to enter SVC."),
        q("Thoracic sympathetic trunk lies near:", "Heads of ribs", ["Sternum anteriorly", "Carpal tunnel", "Pleural cavity lumen"], "The thoracic sympathetic trunk descends on rib heads/vertebral bodies."),
        q("Anterior intercostal arteries in upper spaces arise from:", "Internal thoracic artery", ["Azygos vein", "Pulmonary artery", "Coronary arteries"], "Internal thoracic gives anterior intercostal branches."),
        q("Chest tube insertion is safest just above the upper border of rib because:", "Main intercostal bundle lies below the rib above", ["Pleura is absent there", "Lung has no apex", "Diaphragm blocks the site"], "Avoid the neurovascular bundle in the costal groove by entering above the rib."),
        q("Intercostal nerve block must target the nerve near:", "Inferior border of rib", ["Superior border of rib below", "Sternum only", "Spinous process only"], "The nerve runs along the costal groove near inferior rib border."),
        q("Internal thoracic artery is commonly used for coronary bypass because:", "It has good long-term patency and accessible course", ["It drains lymph", "It is a vein", "It supplies only skin"], "Internal thoracic/mammary artery grafts are durable for CABG."),
        q("Herpes zoster in a band-like thoracic distribution follows:", "Intercostal nerve dermatome", ["Pulmonary artery", "Azygos vein", "Thoracic duct only"], "Shingles reactivates in dorsal root ganglion and follows a dermatome."),
        q("Collateral circulation in coarctation of aorta may enlarge:", "Intercostal arteries causing rib notching", ["Pulmonary veins", "Coronary sinus", "Thoracic duct"], "Enlarged posterior intercostals erode inferior rib margins."),
    ]),
    ("thoracic-cavity-pleurae", "Thoracic Cavity and Pleurae", [
        q("Pleura covering lung surface is:", "Visceral pleura", ["Parietal pleura", "Fibrous pericardium", "Endothoracic fascia"], "Visceral pleura adheres to lung surface and fissures."),
        q("Pleura lining thoracic wall is:", "Parietal pleura", ["Visceral pleura", "Epicardium", "Endocardium"], "Parietal pleura lines ribs, diaphragm and mediastinum."),
        q("Costodiaphragmatic recess lies between:", "Costal and diaphragmatic pleura", ["Lung lobes", "Atria", "Pericardial layers"], "It is the lowest pleural recess where fluid collects."),
        q("Pleural cavity normally contains:", "Thin film of serous fluid", ["Air", "Blood clot", "CSF"], "A small fluid film reduces friction during respiration."),
        q("Cervical pleura is reinforced by:", "Suprapleural membrane", ["Falx cerebri", "Pericardium", "Pleural ligament only"], "Sibson fascia reinforces the pleural cupula."),
        q("Parietal pleura pain is carried by:", "Intercostal and phrenic nerves", ["Vagus only", "Pulmonary plexus only", "Thoracic duct"], "Costal pleura by intercostals; mediastinal/central diaphragmatic by phrenic."),
        q("Visceral pleura is insensitive to:", "Pain", ["Stretch only", "Autonomic fibers", "Surface contact"], "Visceral pleura has autonomic supply and is insensitive to pain."),
        q("The pleural reflection around lung root forms:", "Pulmonary ligament", ["Falciform ligament", "Ligamentum arteriosum", "Annular ligament"], "Pleural sleeve below root hangs as pulmonary ligament."),
        q("Right pleural cavity is separated from left by:", "Mediastinum", ["Diaphragm only", "Azygos vein only", "Sternum only"], "The mediastinum lies between pleural sacs."),
        q("Pleural recesses allow:", "Lung expansion during inspiration", ["Heart valve closure", "Esophageal peristalsis", "Rib ossification"], "Recesses are reserve spaces for lung expansion."),
        q("A basal pleural effusion is best aspirated from:", "Costodiaphragmatic recess", ["Lung apex", "Pericardial cavity", "Middle mediastinum"], "Fluid collects in dependent pleural recesses."),
        q("Referred shoulder pain in diaphragmatic pleurisy occurs via:", "Phrenic nerve C3-C5", ["Intercostobrachial nerve", "Vagus recurrent branch", "Long thoracic nerve"], "Central diaphragmatic pleura is phrenic; C3-C5 refer to shoulder."),
        q("Open pneumothorax causes lung collapse because:", "Negative intrapleural pressure is lost", ["Bronchi close permanently", "Pleura secretes bone", "Pulmonary veins thrombose always"], "Air entering pleural cavity abolishes pressure gradient keeping lung expanded."),
        q("A needle inserted below the 9th rib in midaxillary line may injure:", "Diaphragm or abdominal viscera", ["Carpal tunnel", "Brachial plexus", "Cervical pleura only"], "Pleural and lung borders vary; too low risks diaphragm/liver/spleen."),
        q("Pain from costal pleura is localized because:", "Intercostal nerves are somatic", ["Vagus carries sharp pain", "Visceral pleura is somatic", "Lungs have dermatomes"], "Somatic intercostal innervation gives well-localized pain."),
    ]),
    ("lungs", "Lungs", [
        q("Right lung has how many lobes?", "Three", ["Two", "Four", "One"], "Right lung has superior, middle and inferior lobes."),
        q("Left lung has how many lobes?", "Two", ["Three", "Four", "One"], "Left lung has superior and inferior lobes."),
        q("Horizontal fissure is present in:", "Right lung", ["Left lung only", "Both lungs", "Neither lung"], "Right lung has oblique and horizontal fissures."),
        q("Lingula belongs to:", "Left superior lobe", ["Right middle lobe", "Left inferior lobe", "Right upper lobe"], "Lingula is tongue-like part of left upper lobe."),
        q("At the root of right lung, the eparterial bronchus lies:", "Above pulmonary artery", ["Below pulmonary vein", "Inside pericardium", "Behind esophagus"], "Right superior lobar bronchus is eparterial."),
        q("Pulmonary veins are usually:", "Anterior and inferior in lung root", ["Only posterior", "Above bronchus", "Absent at hilum"], "Veins lie anterior/inferior relative to bronchi and arteries."),
        q("Bronchopulmonary segment is supplied by:", "Segmental bronchus and artery", ["Pulmonary vein only", "Thoracic duct", "Internal thoracic artery"], "Each segment has its own segmental bronchus and pulmonary artery branch."),
        q("Pulmonary veins run mainly in:", "Intersegmental planes", ["Inside segmental bronchi", "Pleural cavity free", "Pericardial sinuses only"], "Intersegmental veins form surgical planes."),
        q("Left lung has a cardiac notch due to:", "Heart impression", ["Liver", "Azygos vein", "SVC"], "The heart indents the left lung anterior border."),
        q("Bronchial arteries supply:", "Conducting bronchi and lung connective tissue", ["Oxygenating alveolar blood", "Only pleura", "Only pericardium"], "Bronchial circulation nourishes bronchial walls and supporting tissues."),
        q("Aspiration in an upright adult most often enters:", "Right lower lobe bronchus", ["Left upper lobe always", "Lingula only", "Right middle ear"], "Right main bronchus is wider, shorter and more vertical."),
        q("A lung abscess after aspiration is more common on the right because:", "Right main bronchus is wider and more vertical", ["Left lung has three lobes", "Right lung lacks bronchus", "Left bronchus is vertical"], "Airway anatomy favors aspiration into right bronchial tree."),
        q("Segmentectomy is possible because bronchopulmonary segments are:", "Anatomically and functionally discrete units", ["Supplied by one common bronchus only", "Without vessels", "Not separated by veins"], "Segments have segmental bronchi/arteries and intersegmental veins."),
        q("Cancer at lung apex causing Horner syndrome likely involves:", "Cervical sympathetic pathway", ["Median nerve in wrist", "Femoral nerve", "Optic chiasma only"], "Pancoast tumors may invade sympathetic chain/stellate ganglion."),
        q("Pulmonary emboli lodge according to:", "Pulmonary arterial branching", ["Bronchial veins only", "Pleural recesses", "Coronary sinuses"], "Emboli travel through pulmonary arteries to segmental/subsegmental branches."),
    ]),
    ("mediastinum", "Mediastinum", [
        q("Mediastinum is the region between:", "Two pleural cavities", ["Two lungs only within pleura", "Ribs and skin", "Diaphragm and pelvis"], "It is the central thoracic compartment between pleural sacs."),
        q("Superior mediastinum lies above the plane from sternal angle to:", "T4/T5 intervertebral disc", ["T12/L1 disc", "Xiphoid tip", "C7/T1 disc"], "Transverse thoracic plane separates superior and inferior mediastina."),
        q("Inferior mediastinum is subdivided into:", "Anterior, middle and posterior", ["Right and left only", "Upper and lower only", "Costal and cervical"], "Inferior mediastinum has anterior, middle and posterior parts."),
        q("Middle mediastinum contains:", "Heart and pericardium", ["Thymus only", "Descending aorta only", "Esophagus only"], "The heart/pericardium occupy middle mediastinum."),
        q("Posterior mediastinum contains:", "Esophagus and descending thoracic aorta", ["Heart only", "Thymus only", "Sternum"], "Posterior mediastinum lies behind pericardium."),
        q("Thymus is mainly in:", "Superior and anterior mediastinum", ["Posterior mediastinum only", "Pleural cavity", "Pericardial cavity"], "Thymus extends from superior into anterior mediastinum."),
        q("Arch of aorta is located in:", "Superior mediastinum", ["Anterior mediastinum", "Pleural cavity", "Middle mediastinum only"], "Aortic arch is a key superior mediastinal structure."),
        q("Trachea bifurcates at approximately:", "Sternal angle/T4-T5 plane", ["Xiphoid", "T12", "C1"], "Carina lies near the transverse thoracic plane."),
        q("Phrenic nerves pass anterior to:", "Roots of lungs", ["Esophagus only posteriorly", "Azygos vein only", "Thoracic duct"], "Phrenic nerves descend anterior to lung roots with pericardiacophrenic vessels."),
        q("Vagus nerves pass posterior to:", "Roots of lungs", ["Sternum", "Costal cartilages", "Internal thoracic artery"], "Vagi pass posterior to lung roots and form esophageal plexus."),
        q("A posterior mediastinal mass causing dysphagia likely compresses:", "Esophagus", ["Trachea only anteriorly", "Internal thoracic artery", "Thymus"], "Esophagus is in posterior mediastinum."),
        q("Enlarged left atrium causing dysphagia does so because it lies anterior to:", "Esophagus", ["Trachea only", "Sternum", "Thoracic duct only"], "Esophagus passes posterior to left atrium."),
        q("A mediastinal shift after tension pneumothorax occurs because:", "Rising pleural pressure pushes mediastinum opposite side", ["Heart becomes smaller", "Ribs dissolve", "Diaphragm ossifies"], "Tension pneumothorax displaces mediastinum and impairs venous return."),
        q("In mediastinal surgery, phrenic nerve injury results in:", "Diaphragmatic paralysis", ["Vocal cord paralysis", "Wrist drop", "Loss of taste"], "Phrenic nerve supplies motor fibers to diaphragm."),
        q("Left recurrent laryngeal nerve is vulnerable near:", "Arch of aorta and ligamentum arteriosum", ["Carpal tunnel", "Femoral triangle", "Right atrium only"], "It loops under aortic arch near ligamentum arteriosum."),
    ]),
    ("pericardium-heart", "Pericardium and Heart", [
        q("Fibrous pericardium is attached inferiorly to:", "Central tendon of diaphragm", ["Liver", "Pleura only", "Sternocleidomastoid"], "Fibrous pericardium blends with central tendon."),
        q("Serous pericardium has parietal layer and:", "Visceral layer/epicardium", ["Endocardium", "Myocardium only", "Pleura"], "Visceral serous pericardium is epicardium."),
        q("Transverse pericardial sinus lies between:", "Arterial and venous ends of heart", ["Two ventricles", "Pleura and lung", "Ribs and sternum"], "It is posterior to ascending aorta/pulmonary trunk and anterior to SVC."),
        q("Oblique pericardial sinus lies behind:", "Left atrium", ["Right ventricle anteriorly", "Sternum", "Aortic arch"], "It is a blind recess posterior to left atrium."),
        q("Base of heart is formed mainly by:", "Left atrium", ["Right ventricle", "Apex", "Pulmonary trunk"], "Left atrium forms most of base/posterior surface."),
        q("Apex of heart is formed by:", "Left ventricle", ["Right atrium", "Right ventricle", "SVC"], "Apex is left ventricular."),
        q("Right coronary artery usually gives:", "Posterior interventricular artery", ["Anterior interventricular artery", "Circumflex artery only", "Internal thoracic artery"], "In right dominance, RCA gives posterior interventricular branch."),
        q("Anterior interventricular artery is a branch of:", "Left coronary artery", ["Right coronary artery", "Pulmonary trunk", "Internal thoracic"], "LAD/anterior interventricular descends in anterior interventricular groove."),
        q("SA node is usually supplied by:", "Right coronary artery", ["Pulmonary artery", "Left marginal artery always", "Azygos vein"], "Most often SA nodal artery arises from RCA."),
        q("Coronary sinus opens into:", "Right atrium", ["Left atrium", "Right ventricle", "SVC"], "Coronary sinus drains most cardiac veins into right atrium."),
        q("Pericardial tamponade reduces cardiac output mainly by:", "Restricting ventricular filling", ["Blocking airway", "Increasing lung compliance", "Closing coronary sinus only"], "Fluid under pressure in pericardial sac impairs diastolic filling."),
        q("Pain from pericarditis may refer to shoulder because of:", "Phrenic nerve sensory supply to fibrous/parietal pericardium", ["Median nerve", "Intercostobrachial nerve", "Radial nerve"], "Phrenic nerve C3-C5 carries pain and refers to shoulder."),
        q("A stab wound left of sternum injuring the anterior heart most likely damages:", "Right ventricle", ["Left atrium", "SVC", "Pulmonary veins"], "Right ventricle forms most sternocostal surface."),
        q("Occlusion of anterior interventricular artery endangers:", "Anterior two-thirds of interventricular septum", ["SA node always only", "Posterior left atrium only", "Azygos vein"], "LAD supplies anterior septum and anterior ventricular walls."),
        q("Fetal foramen ovale functionally directs blood from:", "Right atrium to left atrium", ["Left atrium to right ventricle", "Aorta to pulmonary trunk", "SVC to IVC"], "Foramen ovale bypasses fetal lungs by RA-to-LA flow."),
    ]),
    ("great-vessels", "Superior Vena Cava, Aorta and Pulmonary Trunk", [
        q("Superior vena cava is formed by union of:", "Right and left brachiocephalic veins", ["Azygos and hemiazygos", "Pulmonary veins", "Internal thoracic veins"], "The brachiocephalic veins unite to form SVC."),
        q("SVC drains into:", "Right atrium", ["Left atrium", "Right ventricle", "Coronary sinus"], "SVC returns venous blood from upper body to right atrium."),
        q("Azygos vein drains into:", "Superior vena cava", ["Inferior vena cava", "Pulmonary trunk", "Left atrium"], "Azygos arches over right lung root to SVC."),
        q("Ascending aorta begins at:", "Left ventricle", ["Right ventricle", "Right atrium", "Pulmonary veins"], "It arises from left ventricle at aortic orifice."),
        q("Branches of arch of aorta classically are:", "Brachiocephalic trunk, left common carotid, left subclavian", ["Right coronary, left coronary, azygos", "Internal thoracic, intercostal, bronchial", "Pulmonary arteries"], "These are the three usual arch branches."),
        q("Descending thoracic aorta lies in:", "Posterior mediastinum", ["Anterior mediastinum", "Right atrium", "Pleural cavity only"], "It descends left of vertebral bodies in posterior mediastinum."),
        q("Pulmonary trunk arises from:", "Right ventricle", ["Left ventricle", "Left atrium", "SVC"], "It carries deoxygenated blood to lungs."),
        q("Ligamentum arteriosum connects:", "Pulmonary trunk/left pulmonary artery to arch of aorta", ["SVC to IVC", "Azygos to hemiazygos", "Right atrium to left atrium"], "It is remnant of ductus arteriosus."),
        q("Left recurrent laryngeal nerve loops under:", "Arch of aorta", ["Right subclavian artery", "SVC", "Internal thoracic artery"], "Left RLN hooks below aortic arch near ligamentum arteriosum."),
        q("Coarctation of aorta commonly occurs near:", "Ductus arteriosus/ligamentum arteriosum", ["Aortic valve only", "Coronary sinus", "SVC opening"], "Juxtaductal coarctation is classic."),
        q("SVC obstruction produces:", "Facial and upper limb venous congestion", ["Leg-only edema", "Portal hypertension only", "Urinary retention"], "SVC drains head, neck, upper limbs and upper thorax."),
        q("Aortic arch aneurysm causing hoarseness compresses:", "Left recurrent laryngeal nerve", ["Right phrenic nerve", "Median nerve", "Long thoracic nerve"], "Left RLN loops around aortic arch."),
        q("Patent ductus arteriosus causes abnormal communication between:", "Aorta and pulmonary trunk", ["Atria only", "Ventricles only", "SVC and IVC"], "Ductus arteriosus connects pulmonary trunk/left pulmonary artery to aorta in fetus."),
        q("Rib notching in coarctation occurs due to enlarged:", "Posterior intercostal arteries", ["Pulmonary veins", "Internal jugular veins", "Coronary arteries"], "Collateral flow through intercostals erodes inferior rib margins."),
        q("Pulmonary embolus from leg veins reaches lungs through:", "Right heart and pulmonary trunk", ["Left heart first", "Aorta", "Coronary sinus directly"], "Venous emboli pass IVC/RA/RV to pulmonary arteries."),
    ]),
    ("trachea-oesophagus-thoracic-duct", "Trachea, Oesophagus and Thoracic Duct", [
        q("Trachea begins at lower border of:", "Cricoid cartilage", ["Thyroid cartilage upper border", "Sternal angle", "T12"], "Trachea starts at C6 below cricoid."),
        q("Trachea bifurcates at:", "Sternal angle", ["Xiphoid", "Jugular notch", "T12"], "Carina lies near T4/T5 plane at sternal angle."),
        q("Right main bronchus is:", "Shorter, wider and more vertical", ["Longer and narrower", "Absent", "Horizontal"], "This explains right-sided aspiration."),
        q("Esophagus begins at:", "C6", ["T4", "T10", "L1"], "It begins as continuation of pharynx at lower border of cricoid."),
        q("Esophagus passes through diaphragm at:", "T10", ["T8", "T12", "C6"], "Esophageal hiatus is at T10."),
        q("Thoracic duct begins from:", "Cisterna chyli", ["Right atrium", "Azygos arch", "Left ventricle"], "It ascends from cisterna chyli through aortic hiatus."),
        q("Thoracic duct drains into:", "Left venous angle", ["Right venous angle", "Portal vein", "Azygos vein"], "It opens at junction of left internal jugular and subclavian veins."),
        q("Thoracic duct drains lymph from:", "Most of body except right upper quadrant", ["Right upper quadrant only", "Only lungs", "Only heart"], "Right lymphatic duct drains right upper quadrant."),
        q("Esophageal plexus is formed mainly by:", "Vagus nerves", ["Phrenic nerves", "Intercostal nerves", "Sympathetic trunks only"], "Vagi form esophageal plexus and anterior/posterior vagal trunks."),
        q("Tracheal cartilages are incomplete posteriorly because of:", "Esophagus expansion during swallowing", ["Aortic pulsation only", "Lung inflation", "Pleural recess"], "Posterior membranous wall allows esophagus to bulge anteriorly."),
        q("A foreign body is more likely to enter right bronchus because it is:", "Wider, shorter and more vertical", ["Narrower and longer", "Blocked by carina", "Outside mediastinum"], "Right bronchial anatomy favors aspiration."),
        q("Esophageal cancer commonly causes dysphagia because:", "Esophageal lumen is narrowed", ["Trachea is absent", "Thoracic duct expands", "Pleura ossifies"], "Progressive obstruction produces difficulty swallowing."),
        q("Milky pleural effusion after thoracic surgery suggests injury to:", "Thoracic duct", ["Azygos vein", "Phrenic nerve", "Internal thoracic artery"], "Thoracic duct injury causes chylothorax."),
        q("Carinal irritation during bronchoscopy may cause cough because carina is:", "Highly sensitive", ["Insensate", "Part of pericardium", "In abdomen"], "Carina is very sensitive and triggers cough reflex."),
        q("Left atrial enlargement may compress:", "Esophagus", ["Trachea at neck only", "Thoracic duct only", "Sternum"], "Esophagus lies posterior to left atrium."),
    ]),
    ("surface-radiological-thorax", "Surface Marking and Radiological Anatomy of Thorax", [
        q("Apex beat is usually felt in:", "Left 5th intercostal space midclavicular line", ["Right 2nd space", "Epigastrium only", "Left 10th space"], "The cardiac apex projects to left 5th ICS near midclavicular line."),
        q("Sternal angle marks the level of:", "Second costal cartilage", ["Xiphoid tip", "T12", "First lumbar vertebra"], "Useful landmark for rib counting."),
        q("Tracheal bifurcation projects near:", "Sternal angle", ["Xiphoid", "Umbilicus", "C2"], "Carina lies at T4/T5 transverse thoracic plane."),
        q("Right border of heart is formed mainly by:", "Right atrium", ["Left ventricle", "Pulmonary trunk", "Left atrium"], "Right atrium forms right cardiac border."),
        q("Left border of heart is formed mainly by:", "Left ventricle", ["Right atrium", "SVC", "IVC"], "Left ventricle contributes most of left border and apex."),
        q("Lower border of lung in midclavicular line is at rib:", "6", ["8", "10", "12"], "Lung border: 6 MCL, 8 midaxillary, 10 paravertebral."),
        q("Pleural reflection in midclavicular line reaches rib:", "8", ["6", "10", "12"], "Pleura descends two ribs below lung: 8 MCL, 10 MAL, 12 posterior."),
        q("On PA chest X-ray, right heart border is formed by:", "Right atrium", ["Left atrium", "Left ventricle", "Aortic arch"], "Right atrium forms right lower cardiac border."),
        q("Aortic knuckle on chest X-ray represents:", "Arch of aorta", ["Pulmonary trunk", "SVC", "Azygos vein"], "The aortic arch forms the aortic knuckle."),
        q("Costophrenic angle blunting on X-ray suggests:", "Pleural effusion", ["Carpal tunnel syndrome", "Scaphoid fracture", "Mitral valve only"], "Fluid collects in costodiaphragmatic recess and blunts the angle."),
        q("Needle decompression for tension pneumothorax is aimed at pleural cavity to:", "Release trapped air under pressure", ["Enter pericardium", "Drain CSF", "Inject coronary artery"], "Tension pneumothorax requires urgent decompression of pleural air."),
        q("In chest drain insertion, the neurovascular bundle is avoided by passing:", "Just above upper border of rib", ["Just below lower border", "Through sternum", "Through costal cartilage only"], "The main VAN bundle lies under the rib above."),
        q("Apex beat displaced laterally and inferiorly suggests:", "Cardiomegaly/left ventricular enlargement", ["Scaphoid fracture", "Pneumothorax always only", "Carpal tunnel"], "LV enlargement shifts apex beat down and out."),
        q("Loss of left heart border on X-ray classically localizes disease to:", "Lingula", ["Right lower lobe", "Azygos vein", "Esophagus"], "Silhouette sign localizes opacity adjacent to the obscured border."),
        q("A widened mediastinum on trauma X-ray raises concern for:", "Aortic injury", ["Median nerve lesion", "Appendicitis", "Scaphoid fracture"], "Mediastinal widening after blunt trauma may indicate great vessel injury."),
    ]),
]


def main():
    questions = []
    for topic_index, (slug, topic, rows) in enumerate(TOPICS):
        if len(rows) != 15:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 15")
        for question_index, row in enumerate(rows, 1):
            options = list(row["wrong"])
            answer_index = (topic_index + question_index - 1) % 4
            options.insert(answer_index, row["answer"])
            questions.append({
                **BASE,
                "id": f"anatomy-thorax-{slug}-{question_index:02d}",
                "topic": topic,
                "difficulty": "moderate" if question_index <= 5 else "high" if question_index <= 10 else "very high",
                "prompt": row["prompt"],
                "options": options,
                "answerIndex": answer_index,
                "answer": row["answer"],
                "explanation": row["explanation"],
            })
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "anatomy" and x.get("chapterTitle") == CHAPTER)] + questions
    if len(TOPICS) != 10 or len(questions) != 150:
        raise AssertionError(f"Expected 10 topics and 150 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 150:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
