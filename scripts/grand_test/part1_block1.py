# -*- coding: utf-8 -*-
"""
FMGE Grand Test 1 - Part 1: Block 1
Anatomy (17 Qs) + Physiology (17 Qs) + Biochemistry (17 Qs) = 51 Questions
Strict adherence to 2026 NBE pattern, clinical vignettes, option-by-option review.
Zero textbook citations.
"""

QUESTIONS = [
    # ==========================================
    # ANATOMY (17 Questions: Q001 - Q017)
    # ==========================================
    {
        "id": "fmge-gt1-q001",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Upper Limb - Radial Nerve Injury",
        "prompt": "A 28-year-old construction worker falls from a scaffolding and sustains a closed fracture of the midshaft humerus. On physical examination, he is unable to extend his wrist and fingers. He also exhibits loss of sensation over the dorsal aspect of the first web space. Which nerve was directly damaged in the spiral groove?",
        "options": [
            "Axillary nerve",
            "Median nerve",
            "Radial nerve",
            "Musculocutaneous nerve"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nThe midshaft of the humerus is closely related to the radial groove (spiral groove), where the radial nerve and the profunda brachii artery run. Fractures of the humeral midshaft commonly cause direct neuropraxia or laceration of the radial nerve. The radial nerve innervates all extensors of the forearm, wrist, and digits; damage results in classic wrist drop (inability to extend the wrist and fingers) and loss of cutaneous sensation over the dorsum of the first web space.\n\nOption Review:\n- Option A is incorrect because the axillary nerve winds around the surgical neck of the humerus and innervates the deltoid and teres minor, producing loss of shoulder abduction and sensory deficit over the regimental badge area.\n- Option B is incorrect because the median nerve runs anteriorly in the arm and cubital fossa; injury at the elbow leads to loss of forearm pronation, loss of thumb opposition, and sensory loss over the palmar aspect of the lateral three and a half digits.\n- Option C is correct because the radial nerve travels in the spiral groove of the midshaft humerus, supplying wrist and finger extensors.\n- Option D is incorrect because the musculocutaneous nerve pierces the coracobrachialis to supply the anterior arm flexors (biceps brachii, brachialis) and terminates as the lateral cutaneous nerve of the forearm.\n\nKey Takeaway: Midshaft humerus fractures classically damage the radial nerve in the spiral groove, producing wrist drop and sensory deficit over the dorsal first web space.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Gray817.png/640px-Gray817.png"
        ]
    },
    {
        "id": "fmge-gt1-q002",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Upper Limb - Brachial Plexus Injury",
        "prompt": "A newborn delivered via difficult breech extraction presents with an adducted, internally rotated shoulder, an extended elbow, and a pronated forearm. The grasp reflex is intact, but the biceps and Moro reflexes are absent on the affected side. Which roots of the brachial plexus are injured?",
        "options": [
            "C5 and C6 roots",
            "C7 and C8 roots",
            "C8 and T1 roots",
            "C6 and C7 roots"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe presentation described is classic Erb-Duchenne palsy ('waiter's tip' posture), caused by excessive traction on the neck during difficult delivery that damages the upper trunk of the brachial plexus (C5 and C6 nerve roots). Muscles paralyzed include the deltoid and supraspinatus (loss of abduction), infraspinatus (loss of external rotation), biceps brachii and brachialis (loss of elbow flexion and supination). The limb hangs by the side in adduction and internal rotation, with elbow extended and forearm pronated. The grasp reflex depends on lower roots (C8-T1) and remains preserved.\n\nOption Review:\n- Option A is correct because injury to the C5-C6 roots (Erb's point) paralyzes abductors, external rotators, and flexors of the upper extremity.\n- Option B is incorrect because isolated C7-C8 lesions do not produce the classic waiter's tip deformity; C7 lesions primarily affect triceps extension.\n- Option C is incorrect because damage to C8-T1 roots causes Klumpke's palsy, characterized by intrinsic hand muscle paralysis leading to a claw hand and Horner syndrome, with an absent grasp reflex.\n- Option D is incorrect because the primary upper trunk composition is C5-C6.\n\nKey Takeaway: Erb palsy results from traction on C5-C6 roots, resulting in the characteristic 'waiter's tip' posture with preserved grasp reflex.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q003",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Head and Neck - Cavernous Sinus Anatomy",
        "prompt": "A 34-year-old male presents with high-grade fever, severe periorbital edema, proptosis, and ophthalmoplegia following a severe furuncle on his upper lip. Sensation over the forehead and cheek is diminished. Infection has spread retrograde through the facial venous system into which dural venous sinus?",
        "options": [
            "Superior sagittal sinus",
            "Cavernous sinus",
            "Transverse sinus",
            "Sigmoid sinus"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe 'danger area of the face' includes the upper lip, columella, and bridge of the nose. Venous blood from this region drains via the facial and angular veins, which communicate with the ophthalmic veins and the pterygoid venous plexus. Because facial veins lack valves, infections can travel retrograde through superior and inferior ophthalmic veins into the cavernous sinus, resulting in septic cavernous sinus thrombosis. Structures traversing the cavernous sinus include CN III, IV, V1, V2 in the lateral wall, and CN VI along with the internal carotid artery centrally.\n\nOption Review:\n- Option A is incorrect because the superior sagittal sinus runs in the superior border of the falx cerebri, draining cortical cerebral veins.\n- Option B is correct because the cavernous sinus receives venous drainage directly from the ophthalmic veins communicating with the danger area of the face.\n- Option C is incorrect because the transverse sinus courses horizontally along the internal surface of the occipital bone and drains into the sigmoid sinus.\n- Option D is incorrect because the sigmoid sinus is a continuation of the transverse sinus, draining mastoid air cell infections rather than facial infections.\n\nKey Takeaway: Retrograde spread of infection from the danger area of the face travels via the ophthalmic veins into the cavernous sinus.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Gray570.png/640px-Gray570.png"
        ]
    },
    {
        "id": "fmge-gt1-q004",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Lower Limb - Femoral Triangle Boundaries",
        "prompt": "During a femoral artery catheterization, a resident identifies the anatomical landmarks of the femoral triangle. The needle must be introduced just medial to the femoral nerve and lateral to the femoral vein within the femoral sheath. Which structure forms the lateral border of the femoral triangle?",
        "options": [
            "Medial border of adductor longus",
            "Medial border of sartorius",
            "Lateral border of rectus femoris",
            "Inguinal ligament"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe femoral triangle (Scarpa's triangle) is bounded superiorly by the inguinal ligament (base), medially by the medial border of the adductor longus, and laterally by the medial border of the sartorius muscle. The floor is formed from lateral to medial by the iliopsoas, pectineus, and adductor longus. The contents from lateral to medial are the femoral nerve (outside the sheath), femoral artery, femoral vein, and femoral canal containing deep inguinal lymph nodes (Cloquet's node).\n\nOption Review:\n- Option A is incorrect because the medial border of the adductor longus muscle forms the medial boundary of the femoral triangle.\n- Option B is correct because the medial border of the sartorius muscle defines the lateral boundary of the femoral triangle.\n- Option C is incorrect because the rectus femoris lies deep and lateral to the sartorius and does not form a boundary of the femoral triangle.\n- Option D is incorrect because the inguinal ligament forms the superior boundary (base) of the triangle.\n\nKey Takeaway: The femoral triangle is bounded laterally by the medial border of the sartorius and medially by the medial border of the adductor longus.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q005",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Thorax - Coronary Artery Dominance",
        "prompt": "An angiogram reveals an occlusion in the artery that supplies the diaphragmatic surface of both ventricles and the posterior third of the interventricular septum. In approximately 85% of individuals, which coronary vessel gives rise to the posterior interventricular artery?",
        "options": [
            "Left anterior descending artery",
            "Left circumflex artery",
            "Right coronary artery",
            "Left main coronary artery"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nCoronary artery dominance is determined by which vessel gives origin to the posterior descending artery (posterior interventricular artery), which runs in the posterior interventricular groove and supplies the diaphragmatic ventricular myocardium and the posterior third of the interventricular septum. In right-dominant circulation (~85% of individuals), the posterior descending artery arises from the right coronary artery. In left-dominant circulation (~10%), it arises from the left circumflex artery; in codominant circulation (~5%), branches arise from both vessels.\n\nOption Review:\n- Option A is incorrect because the left anterior descending artery supplies the anterior two-thirds of the interventricular septum and anterior wall of the left ventricle.\n- Option B is incorrect because the left circumflex gives rise to the posterior descending artery only in the 10% of individuals with left-dominant anatomy.\n- Option C is correct because the right coronary artery gives rise to the posterior descending artery in approximately 85% of individuals.\n- Option D is incorrect because the left main coronary artery bifurcates into the left anterior descending and circumflex arteries and does not directly give off the posterior descending vessel.\n\nKey Takeaway: Right coronary dominance occurs in 85% of individuals, where the posterior descending artery branches off the right coronary artery.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q006",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Abdomen - Epiploic Foramen (Foramen of Winslow)",
        "prompt": "During an emergency exploratory laparotomy for severe hepatic trauma, the surgeon applies digital compression across the hepatoduodenal ligament to achieve temporary hemostasis (Pringle maneuver). Which major vascular structure lies immediately posterior to the epiploic foramen?",
        "options": [
            "Abdominal aorta",
            "Inferior vena cava",
            "Portal vein",
            "Superior mesenteric vein"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe epiploic foramen (foramen of Winslow) connects the greater peritoneal sac with the lesser sac (omental bursa). Its boundaries are critically tested in surgical anatomy: Anteriorly lies the hepatoduodenal ligament containing the portal triad (proper hepatic artery, common bile duct, and portal vein); Posteriorly lies the inferior vena cava and right crus of the diaphragm; Superiorly lies the caudate lobe of the liver; Inferiorly lies the first part of the duodenum and horizontal hepatic artery.\n\nOption Review:\n- Option A is incorrect because the abdominal aorta lies further posteriorly and to the left of the midline, behind the retroperitoneum.\n- Option B is correct because the inferior vena cava forms the direct posterior boundary of the epiploic foramen.\n- Option C is incorrect because the portal vein lies anteriorly within the hepatoduodenal ligament as part of the portal triad.\n- Option D is incorrect because the superior mesenteric vein lies inferiorly in the root of the mesentery, passing posterior to the neck of the pancreas to join the splenic vein.\n\nKey Takeaway: The posterior boundary of the epiploic foramen of Winslow is formed by the inferior vena cava.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q007",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Pelvis & Perineum - Ischioanal Fossa & Pudendal Canal",
        "prompt": "A 42-year-old male develops a deep ischioanal abscess requiring surgical drainage. The surgeon takes great care while making the incision in the lateral wall of the ischioanal fossa to avoid injury to the neurovascular bundle coursing within the pudendal canal. Which muscle fascia forms the lateral wall of this canal?",
        "options": [
            "Obturator internus",
            "Levator ani",
            "Piriformis",
            "Gluteus maximus"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe ischioanal (ischiorectal) fossa is a wedge-shaped space on each side of the anal canal. The lateral wall is vertical and formed by the obturator internus muscle covered by obturator fascia. Within a duplication of this obturator fascia lies Alcock's canal (pudendal canal), through which the internal pudendal vessels and pudendal nerve travel. The medial wall slopes downward and is formed by the levator ani and external anal sphincter.\n\nOption Review:\n- Option A is correct because the fascia covering the obturator internus forms the lateral wall of the ischioanal fossa and splits to form the pudendal canal.\n- Option B is incorrect because the levator ani forms the medial and superior boundary (roof) of the ischioanal fossa.\n- Option C is incorrect because the piriformis forms the posterolateral wall of the true pelvis above the pelvic diaphragm.\n- Option D is incorrect because the gluteus maximus forms part of the posterior boundary.\n\nKey Takeaway: The pudendal (Alcock) canal is located in the lateral wall of the ischioanal fossa within the fascia of the obturator internus muscle.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q008",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Neuroanatomy - Circle of Willis & Aneurysms",
        "prompt": "A 50-year-old female presents with sudden onset of diplopia and ptosis. Physical examination reveals a dilated, unreactive right pupil, with the right eye deviated downward and laterally ('down-and-out'). CT angiography demonstrates a berry aneurysm compressing the oculomotor nerve. At which arterial junction is this aneurysm most likely situated?",
        "options": [
            "Anterior communicating and anterior cerebral arteries",
            "Posterior communicating and internal carotid arteries",
            "Basilar artery and posterior cerebral artery",
            "Middle cerebral artery bifurcation"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe oculomotor nerve (CN III) emerges from the midbrain between the posterior cerebral artery and the superior cerebellar artery and passes forward just lateral to the posterior communicating artery (PCoA). An aneurysm arising at the junction of the internal carotid artery (ICA) and the posterior communicating artery characteristically compresses the outer parasympathetic pupilloconstrictor fibers of CN III first (producing early mydriasis and loss of pupillary light reflex), followed by somatic motor fibers causing ptosis and a 'down-and-out' globe position.\n\nOption Review:\n- Option A is incorrect because anterior communicating artery aneurysms typically compress the optic chiasm, causing bitemporal hemianopsia rather than third nerve palsy.\n- Option B is correct because an ICA-PCoA junction aneurysm directly compresses the adjacent third cranial nerve.\n- Option C is incorrect because basilar tip aneurysms can affect both oculomotor nerves or midbrain centers, but unilateral isolated pupil-involving palsy is classic for PCoA aneurysms.\n- Option D is incorrect because MCA bifurcation aneurysms present with rupture causing contralateral hemiparesis and aphasia rather than cranial nerve palsies.\n\nKey Takeaway: A pupil-involving third nerve palsy is a medical emergency indicating compression by an expanding posterior communicating artery aneurysm.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q009",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Embryology - Pharyngeal Arches",
        "prompt": "A male infant is born with micrognathia, cleft palate, and hypoplasia of the zygomatic bones. Genetic testing confirms Treacher Collins syndrome, a disorder of first pharyngeal arch development. Which of the following muscles is derived from the muscular component of the first pharyngeal arch?",
        "options": [
            "Stapedius",
            "Tensor veli palatini",
            "Stylopharyngeus",
            "Cricothyroid"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe first pharyngeal (mandibular) arch is innervated by the mandibular division of the trigeminal nerve (CN V3). Its muscular derivatives include the four muscles of mastication (masseter, temporalis, medial pterygoid, lateral pterygoid), mylohyoid, anterior belly of the digastric, tensor tympani, and tensor veli palatini.\n\nOption Review:\n- Option A is incorrect because the stapedius is derived from the second pharyngeal arch and innervated by the facial nerve (CN VII).\n- Option B is correct because the tensor veli palatini originates from the first pharyngeal arch and is innervated by CN V3 (nerve to medial pterygoid).\n- Option C is incorrect because the stylopharyngeus is derived from the third pharyngeal arch and innervated by the glossopharyngeal nerve (CN IX).\n- Option D is incorrect because the cricothyroid is derived from the fourth pharyngeal arch and innervated by the superior laryngeal nerve of the vagus (CN X).\n\nKey Takeaway: The first pharyngeal arch gives rise to the muscles of mastication, mylohyoid, anterior digastric, tensor tympani, and tensor veli palatini.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q010",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Lower Limb - Common Peroneal Nerve",
        "prompt": "A 22-year-old soccer player sustains a direct blow to the lateral aspect of his right knee. He is unable to dorsiflex or evert his right foot, resulting in a high-stepping gait. There is numbness over the anterolateral leg and dorsum of the foot. Which structure was injured as it wound around the fibular neck?",
        "options": [
            "Tibial nerve",
            "Common peroneal nerve",
            "Saphenous nerve",
            "Deep peroneal nerve"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe common peroneal (fibular) nerve diverges from the sciatic nerve at the apex of the popliteal fossa and winds around the lateral aspect of the neck of the fibula, where it is superficial and vulnerable to trauma, tight casts, or fibular fractures. It bifurcates into the deep peroneal nerve (supplying anterior compartment muscles for dorsiflexion and sensation to the first web space) and the superficial peroneal nerve (supplying lateral compartment muscles for eversion and sensation to the foot dorsum). Injury at the fibular neck compromises both, causing classic foot drop and loss of eversion with dorsomedial sensory deficit.\n\nOption Review:\n- Option A is incorrect because the tibial nerve courses straight through the popliteal fossa to supply posterior compartment plantarflexors; injury causes inability to stand on tiptoes.\n- Option B is correct because the common peroneal nerve wraps around the neck of the fibula before dividing into deep and superficial branches.\n- Option C is incorrect because the saphenous nerve is a purely sensory branch of the femoral nerve supplying the medial side of the leg and foot.\n- Option D is incorrect because the deep peroneal nerve is one of the terminal divisions formed after the common peroneal winds around the neck of the fibula.\n\nKey Takeaway: Direct trauma to the neck of the fibula classically injures the common peroneal nerve, causing foot drop and loss of foot eversion.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q011",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Head and Neck - Cranial Foramina",
        "prompt": "A 60-year-old patient with suspected nasopharyngeal carcinoma presents with loss of sensation over the lower jaw, chin, and anterior two-thirds of the tongue, along with weakness of jaw clenching. MRI demonstrates tumor extension through a base-of-skull foramen located in the greater wing of the sphenoid. Through which foramen does the involved nerve exit?",
        "options": [
            "Foramen rotundum",
            "Foramen ovale",
            "Superior orbital fissure",
            "Jugular foramen"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe mandibular division of the trigeminal nerve (CN V3) carries sensory fibers from the lower third of the face, lower teeth, anterior two-thirds of the tongue (general sensation), and motor fibers to the muscles of mastication. CN V3 exits the middle cranial fossa through the foramen ovale in the greater wing of the sphenoid bone. Mnemonic: Standing Room Only (V1 - Superior orbital fissure, V2 - Foramen Rotundum, V3 - Foramen Ovale).\n\nOption Review:\n- Option A is incorrect because the foramen rotundum transmits the maxillary nerve (CN V2).\n- Option B is correct because the foramen ovale transmits the mandibular nerve (CN V3), along with the accessory meningeal artery, lesser petrosal nerve, and emissary vein (OVALE).\n- Option C is incorrect because the superior orbital fissure transmits CN III, IV, V1, VI, and superior ophthalmic vein.\n- Option D is incorrect because the jugular foramen transmits CN IX, X, XI, and the internal jugular vein.\n\nKey Takeaway: The mandibular nerve (CN V3) exits the skull through the foramen ovale in the greater wing of the sphenoid.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q012",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Thorax - Thoracic Duct Anatomy",
        "prompt": "During an esophageal resection for midthoracic esophageal carcinoma, a chylothorax occurs secondary to inadvertent injury to the thoracic duct. At which vertebral level does the thoracic duct normally penetrate the diaphragm to enter the posterior mediastinum?",
        "options": [
            "T8",
            "T10",
            "T12",
            "L1"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nThe thoracic duct begins in the abdomen as the cisterna chyli (at L1-L2) and ascends into the posterior mediastinum through the aortic hiatus of the diaphragm at the level of T12, accompanied by the abdominal aorta and the azygos vein. It ascends on the right side of the vertebral column between T12 and T5, crosses to the left at T5, and empties into the junction of the left internal jugular and left subclavian veins.\n\nOption Review:\n- Option A is incorrect because the caval opening in the central tendon of the diaphragm is at the T8 level, transmitting the inferior vena cava and branches of the right phrenic nerve.\n- Option B is incorrect because the esophageal hiatus is at the T10 level, transmitting the esophagus, anterior/posterior vagal trunks, and esophageal branches of the left gastric vessels.\n- Option C is correct because the aortic hiatus is at the T12 level, transmitting the aorta, thoracic duct, and azygos vein.\n- Option D is incorrect because L1 is the level of origin of the cisterna chyli below the diaphragm.\n\nKey Takeaway: The thoracic duct enters the thorax through the aortic aperture of the diaphragm at the level of T12.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q013",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Upper Limb - Long Thoracic Nerve & Winged Scapula",
        "prompt": "A 45-year-old female undergoes a modified radical mastectomy with level II axillary lymph node clearance for breast carcinoma. Postoperatively, she notices difficulty raising her arm above the horizontal plane, and pushing against a wall causes her medial scapular border to project prominently backwards. Which nerve was injured during axillary dissection?",
        "options": [
            "Thoracodorsal nerve",
            "Long thoracic nerve",
            "Dorsal scapular nerve",
            "Suprascapular nerve"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nWinged scapula occurs due to paralysis of the serratus anterior muscle, which holds the scapula against the thoracic cage and rotates the glenoid cavity upward to permit overhead arm abduction beyond 90 degrees. The serratus anterior is innervated by the long thoracic nerve of Bell (roots C5, C6, C7), which descends vertically along the lateral surface of the thoracic wall in the midaxillary line, making it susceptible to injury during axillary lymph node dissection.\n\nOption Review:\n- Option A is incorrect because the thoracodorsal nerve innervates the latissimus dorsi; injury impairs shoulder extension, adduction, and internal rotation, but does not cause winging of the scapula.\n- Option B is correct because the long thoracic nerve supplies the serratus anterior; injury leads to prominent winging of the medial border of the scapula.\n- Option C is incorrect because the dorsal scapular nerve innervates the rhomboids and levator scapulae.\n- Option D is incorrect because the suprascapular nerve innervates the supraspinatus and infraspinatus muscles.\n\nKey Takeaway: The long thoracic nerve of Bell innervates the serratus anterior; its injury during axillary surgery causes winging of the scapula.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q014",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Abdomen - Inguinal Canal Anatomy",
        "prompt": "During repair of an indirect inguinal hernia in a 30-year-old male, the surgeon identifies the deep inguinal ring. In relation to the inferior epigastric vessels, where is the deep inguinal ring anatomically situated?",
        "options": [
            "Medial to the inferior epigastric artery",
            "Lateral to the inferior epigastric artery",
            "Directly posterior to the inferior epigastric artery",
            "Directly inferior to the pubic tubercle"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe deep (internal) inguinal ring is an outpouching of the transversalis fascia located approximately 1.25 cm above the midinguinal point. It lies immediately lateral to the inferior epigastric artery. Indirect inguinal hernias enter the deep ring lateral to the inferior epigastric vessels and pass through the inguinal canal, whereas direct inguinal hernias protrude through Hesselbach's triangle medial to the inferior epigastric vessels.\n\nOption Review:\n- Option A is incorrect because structures medial to the inferior epigastric artery define the floor of Hesselbach's triangle, where direct hernias emerge.\n- Option B is correct because the deep inguinal ring is located lateral to the inferior epigastric artery.\n- Option C is incorrect because the vessels course vertically in the posterior wall of the canal medial to the ring, not directly anterior.\n- Option D is incorrect because the superficial ring lies superolateral to the pubic crest/tubercle, not the deep ring.\n\nKey Takeaway: The deep inguinal ring lies lateral to the inferior epigastric vessels, which serves as the landmark differentiating indirect from direct inguinal hernias.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q015",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Pelvis - Ureter Relations in Female Pelvis",
        "prompt": "A 48-year-old woman undergoes total abdominal hysterectomy for uterine leiomyomas. During ligation of the uterine artery within the cardinal (Mackenrodt) ligament, the gynecologist must exercise caution because which critical structure passes immediately inferior to the artery?",
        "options": [
            "Obturator nerve",
            "Ureter",
            "External iliac vein",
            "Pudendal nerve"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe surgical dictum 'water under the bridge' describes the anatomic relationship between the ureter and the uterine artery. As the ureter enters the pelvis and approaches the bladder base, it courses forward in the cardinal ligament approximately 1.5 to 2 cm lateral to the cervix, where the uterine artery crosses directly superior to it. Inadvertent ligation or transection of the ureter during clamping of the uterine vessels is a recognized complication of hysterectomy.\n\nOption Review:\n- Option A is incorrect because the obturator nerve runs on the lateral pelvic wall along the obturator internus, far lateral to the uterine vessels.\n- Option B is correct because the ureter passes directly inferior to the uterine artery near the cervix within the cardinal ligament.\n- Option C is incorrect because the external iliac vein courses along the pelvic brim.\n- Option D is incorrect because the pudendal nerve leaves the pelvis through the greater sciatic foramen and courses in the perineum.\n\nKey Takeaway: The ureter courses immediately inferior to the uterine artery ('water under the bridge') near the lateral fornix of the vagina.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q016",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Head and Neck - Laryngeal Nerve Anatomy",
        "prompt": "Following a total thyroidectomy for papillary thyroid carcinoma, a patient notices that her voice fatigues easily and she cannot hit high-pitched vocal notes, though normal conversational speech is mostly unaffected. Laryngoscopy reveals a slack vocal cord that fails to tense. Which nerve was injured during ligation of the superior thyroid artery?",
        "options": [
            "Recurrent laryngeal nerve",
            "Internal branch of superior laryngeal nerve",
            "External branch of superior laryngeal nerve",
            "Glossopharyngeal nerve"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nThe superior thyroid artery is closely associated with the external branch of the superior laryngeal nerve near the superior pole of the thyroid gland. The external laryngeal nerve is purely motor and innervates the cricothyroid muscle, which acts to tense and elongate the vocal cords. Injury to this nerve leads to loss of tension in the vocal cord, resulting in a weak, monotone voice and inability to produce high-frequency sounds. The recurrent laryngeal nerve courses near the inferior thyroid artery and innervates all other intrinsic laryngeal muscles.\n\nOption Review:\n- Option A is incorrect because recurrent laryngeal nerve damage produces frank hoarseness, vocal cord paralysis in the paramedian position, or bilateral stridor.\n- Option B is incorrect because the internal branch of the superior laryngeal nerve is purely sensory to the larynx above the vocal cords; its injury impairs the cough reflex.\n- Option C is correct because the external branch of the superior laryngeal nerve supplies the cricothyroid muscle and is vulnerable during superior thyroid artery ligation.\n- Option D is incorrect because the glossopharyngeal nerve supplies the stylopharyngeus and does not innervate laryngeal muscles.\n\nKey Takeaway: The external branch of the superior laryngeal nerve innervates the cricothyroid muscle; injury produces vocal fatigue and loss of high-pitched phonation.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q017",
        "subjectId": "anatomy",
        "subjectTitle": "Anatomy",
        "topic": "Neuroanatomy - Corticospinal Tract Decussation",
        "prompt": "An MRI of the brain in a 55-year-old stroke patient with acute left-sided hemiparesis shows an ischemic infarction involving the right internal capsule. The corticospinal axons descending from the primary motor cortex travel through the posterior limb of the internal capsule. At which level do approximately 85% to 90% of these fibers decussate?",
        "options": [
            "Cerebral peduncles of the midbrain",
            "Basis pontis",
            "Lower open medulla",
            "Lower closed medulla at the spinomedullary junction"
        ],
        "answerIndex": 3,
        "explanation": "Clinical Reasoning:\nThe primary lateral corticospinal tract arises from pyramidal cells in motor cortex areas 4 and 6, descends through the posterior limb of the internal capsule, middle three-fifths of the crus cerebri in the midbrain, and basal pons to form the medullary pyramids. At the lower, closed part of the medulla oblongata (spinomedullary junction), approximately 85% to 90% of the fibers cross the midline in the decussation of the pyramids to form the lateral corticospinal tract in the lateral funiculus of the spinal cord.\n\nOption Review:\n- Option A is incorrect because the midbrain crus cerebri carries uncrossed corticospinal fibers.\n- Option B is incorrect because the fibers travel through the pons as fascicles without decussating.\n- Option C is incorrect because the upper open medulla contains the prominent pyramids where fibers are still strictly ipsilateral.\n- Option D is correct because pyramidal decussation occurs at the lower closed medulla just above the first cervical spinal cord segment.\n\nKey Takeaway: The corticospinal tract decussates in the lower closed medulla at the junction with the spinal cord, explaining why cortical lesions produce contralateral motor deficits.",
        "imageUrls": []
    },

    # ==========================================
    # PHYSIOLOGY (17 Questions: Q018 - Q034)
    # ==========================================
    {
        "id": "fmge-gt1-q018",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Renal - Nephron Osmolality Under ADH",
        "prompt": "A healthy volunteer is subjected to 24 hours of water deprivation, causing maximal secretion of antidiuretic hormone (ADH/vasopressin). Under these physiological conditions, which segment of the nephron fluid displays the lowest osmolality?",
        "options": [
            "Proximal convoluted tubule",
            "Tip of the loop of Henle",
            "Early distal convoluted tubule",
            "Medullary collecting duct"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nThe thick ascending limb of Henle's loop is the 'diluting segment' of the nephron; it actively reabsorbs Na+, K+, and 2Cl- via the NKCC2 symporter but is completely impermeable to water. Consequently, tubular fluid leaving the thick ascending limb and entering the early distal convoluted tubule (cortical diluting segment) is profoundly hypotonic (approximately 70 to 100 mOsm/kg H2O), which represents the lowest osmolality found anywhere along the nephron, regardless of ADH presence. Even with maximal ADH, water permeability only increases from the late distal tubule onwards.\n\nOption Review:\n- Option A is incorrect because fluid in the proximal convoluted tubule is isosmotic to plasma (~300 mOsm/kg) due to obligate water reabsorption.\n- Option B is incorrect because the hairpin tip of the loop of Henle reaches peak hyperosmolality (~1200 mOsm/kg in antidiuresis).\n- Option C is correct because the thick ascending limb removes solutes without water, rendering early distal tubular fluid hypoosmotic (~100 mOsm/kg).\n- Option D is incorrect because the medullary collecting duct equilibrates with the hypertonic medullary interstitium in the presence of ADH, producing concentrated urine (~1200 mOsm/kg).\n\nKey Takeaway: The early distal convoluted tubule always contains the lowest osmolality fluid in the nephron (~100 mOsm/kg) because the preceding thick ascending limb removes solutes without water.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q019",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Cardiovascular - Ventricular Action Potential Phases",
        "prompt": "A cardiac electrophysiologist records intracellular electrical potentials from a ventricular myocyte. During Phase 2 of the ventricular action potential, the membrane potential is maintained near a plateau of 0 mV for approximately 200 milliseconds. Which balanced ionic currents are responsible for this plateau?",
        "options": [
            "Inward Na+ current balanced by outward K+ current",
            "Inward L-type Ca2+ current balanced by outward delayed rectifier K+ current",
            "Inward T-type Ca2+ current balanced by inward Cl- current",
            "Outward transient K+ current balanced by inward Na+ current"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe ventricular action potential consists of 5 phases: Phase 0 (rapid depolarization via voltage-gated fast Na+ channels), Phase 1 (brief initial repolarization via transient outward K+ channels, Ito), Phase 2 (plateau phase), Phase 3 (rapid repolarization via delayed rectifier K+ channels, IKr and IKs), and Phase 4 (resting membrane potential via inward rectifier K+ channels, IK1). Phase 2 is maintained by a sustained balance between inward influx of Ca2+ through L-type (dihydropyridine) channels and outward efflux of K+ through delayed rectifier channels.\n\nOption Review:\n- Option A is incorrect because fast Na+ channels are inactivated during Phase 2.\n- Option B is correct because the Phase 2 plateau is produced by calcium entry through L-type calcium channels balanced by potassium exit through delayed rectifier channels.\n- Option C is incorrect because T-type calcium channels function mainly in pacemaker cells, not the ventricular plateau.\n- Option D is incorrect because the transient outward K+ current is active in Phase 1, not during the Phase 2 plateau.\n\nKey Takeaway: The plateau of the cardiac ventricular action potential (Phase 2) is mediated by inward L-type Ca2+ currents counterbalanced by outward K+ currents.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q020",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Respiratory - Oxyhemoglobin Dissociation Curve",
        "prompt": "A 30-year-old marathon runner is running at mile 20. In his active skeletal muscles, temperature is 39.5°C, tissue pH is 7.20, and local PCO2 is elevated. Which change occurs in the oxyhemoglobin dissociation curve in these active tissues?",
        "options": [
            "Shift to the left with increased oxygen affinity",
            "Shift to the right with enhanced oxygen unloading",
            "Shift to the left with decreased P50",
            "No change in curve position but decreased oxygen capacity"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe Bohr effect describes how elevated carbon dioxide, acidosis (decreased pH), elevated temperature, and increased 2,3-bisphosphoglycerate (2,3-BPG) in metabolically active tissues decrease hemoglobin's affinity for oxygen. This shifts the oxyhemoglobin dissociation curve to the right, which increases the P50 (the PO2 required to achieve 50% saturation) and facilitates oxygen unloading to hard-working tissues.\n\nOption Review:\n- Option A is incorrect because a left shift reflects increased oxygen affinity, seen with hypothermia, alkalosis, decreased PCO2, and fetal hemoglobin (HbF).\n- Option B is correct because acidosis, hypercapnia, and elevated temperature shift the curve to the right, promoting oxygen delivery to tissues.\n- Option C is incorrect because a right shift increases P50 (more oxygen partial pressure needed to saturate 50%), whereas a left shift decreases P50.\n- Option D is incorrect because the curve distinctly shifts to the right without altering total oxygen-binding capacity.\n\nKey Takeaway: Increased temperature, PCO2, [H+], and 2,3-BPG shift the oxyhemoglobin curve to the right, increasing P50 and enhancing oxygen unloading.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q021",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Endocrine - Calcium Homeostasis",
        "prompt": "A patient with accidental parathyroid gland removal during thyroidectomy develops hypocalcemic tetany. Parathyroid hormone (PTH) normally increases serum calcium through multiple direct and indirect actions. Which direct biochemical action does PTH exert on the renal tubules?",
        "options": [
            "Stimulates calcium reabsorption in the proximal convoluted tubule",
            "Inhibits phosphate reabsorption in the proximal convoluted tubule",
            "Inhibits 1-alpha-hydroxylase in the distal tubule",
            "Stimulates phosphate reabsorption in the thick ascending limb"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nParathyroid hormone acts directly on the kidney to produce two major effects: 1) It stimulates Ca2+ reabsorption in the distal convoluted tubule and connecting tubule; 2) It inhibits Na+-phosphate cotransport (Npt2a) in the proximal convoluted tubule, causing phosphaturia (preventing insoluble calcium-phosphate precipitation). Additionally, PTH stimulates renal 1-alpha-hydroxylase in the proximal tubule to activate 25-hydroxyvitamin D into 1,25-dihydroxyvitamin D3 (calcitriol).\n\nOption Review:\n- Option A is incorrect because PTH does not directly regulate calcium reabsorption in the proximal tubule; its direct stimulatory effect is in the distal tubule.\n- Option B is correct because PTH inhibits the apical sodium-phosphate cotransporter in the proximal tubule, promoting phosphate excretion.\n- Option C is incorrect because PTH stimulates (rather than inhibits) 1-alpha-hydroxylase in the proximal tubule.\n- Option D is incorrect because PTH promotes phosphate loss rather than reabsorption.\n\nKey Takeaway: PTH directly inhibits phosphate reabsorption in the proximal convoluted tubule and stimulates calcium reabsorption in the distal convoluted tubule.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q022",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Gastrointestinal - Gastric Acid Secretion",
        "prompt": "During the cephalic phase of digestion, sham feeding stimulates gastric acid production via vagal efferent fibers. The vagus nerve releases acetylcholine onto parietal cells and stimulates histamine release from enterochromaffin-like (ECL) cells. Which intracellular second messenger mediates histamine-induced H+ secretion by parietal cells?",
        "options": [
            "Cyclic adenosine monophosphate",
            "Inositol 1,4,5-trisphosphate and calcium",
            "Cyclic guanosine monophosphate",
            "Diacylglycerol and protein kinase C"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nGastric parietal cell acid secretion via the apical H+/K+-ATPase pump is regulated by three secretagogues acting through distinct intracellular pathways: 1) Histamine binds to H2 receptors, activating adenylyl cyclase via Gs to increase intracellular cyclic adenosine monophosphate (cAMP), which activates protein kinase A; 2) Acetylcholine binds to M3 muscarinic receptors (coupled to Gq), increasing IP3 and intracellular Ca2+; 3) Gastrin binds to CCK-B receptors (coupled to Gq), also increasing IP3 and Ca2+. Somatostatin and prostaglandins bind Gi-coupled receptors, decreasing cAMP and inhibiting acid secretion.\n\nOption Review:\n- Option A is correct because histamine acts via H2 receptors coupled to Gs, increasing intracellular cAMP.\n- Option B is incorrect because the IP3/Ca2+ pathway mediates the actions of acetylcholine (M3) and gastrin (CCK-B), not histamine.\n- Option C is incorrect because cGMP is involved in nitric oxide and ANP signaling, not parietal cell stimulation.\n- Option D is incorrect because the DAG/PKC branch belongs to the Gq pathway activated by acetylcholine and gastrin.\n\nKey Takeaway: Histamine stimulates gastric parietal acid secretion through H2 receptors via the cAMP second messenger pathway.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q023",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Neurophysiology - Muscle Spindle & Stretch Reflex",
        "prompt": "A neurologist taps the patellar tendon of a 40-year-old male with a reflex hammer, producing a brisk knee-jerk reflex. Which sensory afferent fiber type conducts the primary dynamic stretch signal from the muscle spindle to the spinal cord in this monosynaptic reflex arc?",
        "options": [
            "Group Ia sensory afferent fibers",
            "Group Ib sensory afferent fibers",
            "Group II sensory afferent fibers",
            "Group C unmyelinated fibers"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nThe stretch reflex (myotatic reflex) is a monosynaptic reflex initiated when rapid stretching of the muscle (e.g., patellar tendon tap) deforms the primary sensory endings (annulospiral endings) of the intrafusal muscle spindle fibers. These signals are conducted via heavily myelinated, rapid Group Ia afferent nerve fibers. Ia fibers enter the posterior horn of the spinal cord and synapse directly on alpha motor neurons innervating the stretched extrafusal muscle, producing contraction.\n\nOption Review:\n- Option A is correct because Group Ia afferents wrap around nuclear bag and chain fibers and convey dynamic rate-of-stretch information.\n- Option B is incorrect because Group Ib fibers originate from Golgi tendon organs and mediate the inverse stretch (autogenic inhibition) reflex.\n- Option C is incorrect because Group II fibers innervate static nuclear chain fibers and secondary flower-spray endings, conveying static length rather than dynamic tendon-tap reflexes.\n- Option D is incorrect because Group C fibers are unmyelinated slow fibers conducting dull pain, warmth, and postganglionic autonomic signals.\n\nKey Takeaway: Group Ia afferent fibers from muscle spindles mediate the monosynaptic stretch reflex (deep tendon reflex).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q024",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Respiratory - Lung Volumes & Capacities",
        "prompt": "A 52-year-old smoker undergoes pulmonary function testing for progressive dyspnea. Routine spirometry can directly measure several lung volumes, but certain parameters require plethysmography or helium dilution. Which of the following parameters CANNOT be measured by standard spirometry alone?",
        "options": [
            "Inspiratory capacity",
            "Vital capacity",
            "Functional residual capacity",
            "Expiratory reserve volume"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nStandard spirometry records air volumes displaced during inhalation and exhalation. It cannot measure any volume that remains inside the thoracic cavity after maximal forced exhalation. Therefore, Residual Volume (RV) cannot be measured by spirometry. Any composite lung capacity that incorporates the residual volume also cannot be measured by spirometry alone, which includes Functional Residual Capacity (FRC = ERV + RV) and Total Lung Capacity (TLC = VC + RV).\n\nOption Review:\n- Option A is incorrect because Inspiratory Capacity (IC = TV + IRV) is measured by inhaling maximally from tidal end-expiration.\n- Option B is incorrect because Vital Capacity (VC = TV + IRV + ERV) is directly measured from maximal inspiration to maximal expiration.\n- Option C is correct because Functional Residual Capacity contains the Residual Volume, requiring helium dilution, nitrogen washout, or body plethysmography.\n- Option D is incorrect because Expiratory Reserve Volume (ERV) is directly expired and measured by spirometry.\n\nKey Takeaway: Spirometry cannot measure Residual Volume (RV), Functional Residual Capacity (FRC), or Total Lung Capacity (TLC).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q025",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Renal - Glomerular Filtration Rate Regulation",
        "prompt": "In response to a decrease in mean arterial pressure to 75 mmHg, the macula densa senses reduced sodium chloride delivery in the tubular fluid. This triggers a localized tubuloglomerular feedback response and renin secretion. Which hemodynamic change occurs in the renal microcirculation to maintain glomerular filtration rate?",
        "options": [
            "Constriction of afferent arterioles and dilation of efferent arterioles",
            "Dilation of afferent arterioles and angiotensin II-mediated constriction of efferent arterioles",
            "Constriction of both afferent and efferent arterioles equally",
            "Dilation of both afferent and efferent arterioles equally"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nTo maintain glomerular filtration rate (GFR) during states of decreased renal perfusion pressure (autoregulatory range: 80 to 180 mmHg), the kidney uses dual mechanisms: 1) Prostaglandins (PGE2, PGI2) and nitric oxide dilate the afferent arteriole, decreasing resistance to incoming blood; 2) Renin from juxtaglomerular cells produces angiotensin II, which preferentially constricts the narrower efferent arteriole. Constriction of the outflow tract elevates glomerular capillary hydrostatic pressure (PGC), preserving GFR despite reduced systemic pressure.\n\nOption Review:\n- Option A is incorrect because afferent constriction and efferent dilation would drop intraglomerular pressure and precipitate renal failure.\n- Option B is correct because afferent dilation combined with efferent constriction preserves glomerular capillary hydrostatic pressure.\n- Option C is incorrect because equal constriction reduces renal blood flow and drops filtration rate.\n- Option D is incorrect because generalized dilation reduces filtration fraction without raising intraglomerular pressure.\n\nKey Takeaway: Autoregulation of GFR during hypoperfusion relies on afferent arteriolar dilation (prostaglandin-mediated) and efferent arteriolar constriction (angiotensin II-mediated).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q026",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Cardiovascular - Jugular Venous Pulse Waves",
        "prompt": "An internal medicine resident examines the jugular venous pulse (JVP) of a 65-year-old male with chronic palpitations and dizziness. The radial pulse is irregularly irregular. On inspection of the neck veins, the 'a' wave is absent. Which cardiac event normally produces the 'a' wave in the JVP?",
        "options": [
            "Passive atrial filling during ventricular systole",
            "Right atrial active contraction",
            "Bulging of the tricuspid valve during isovolumetric contraction",
            "Rapid ventricular filling following tricuspid valve opening"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe waves of the jugular venous pulse reflect pressure changes in the right atrium: 'a' wave represents right atrial contraction (presystolic); 'c' wave represents tricuspid valve bulging into the right atrium during right ventricular isovolumetric contraction; 'v' wave represents passive right atrial filling against a closed tricuspid valve during ventricular systole; 'x' descent reflects atrial relaxation and downward displacement of the tricuspid floor; 'y' descent represents rapid emptying of the right atrium into the right ventricle after the tricuspid valve opens. In atrial fibrillation, synchronized atrial contraction is lost, resulting in the complete absence of the 'a' wave.\n\nOption Review:\n- Option A is incorrect because passive atrial filling generates the 'v' wave.\n- Option B is correct because the 'a' wave is produced by active atrial contraction.\n- Option C is incorrect because tricuspid bulging during isovolumetric ventricular contraction generates the 'c' wave.\n- Option D is incorrect because rapid ventricular filling following tricuspid opening corresponds to the 'y' descent.\n\nKey Takeaway: The 'a' wave in the jugular venous pulse corresponds to right atrial contraction and is absent in atrial fibrillation.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q027",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Endocrine - Thyroid Hormone Feedback & Mechanism",
        "prompt": "A 32-year-old woman with heat intolerance, tremor, and weight loss has an elevated free thyroxine (T4) level and suppressed TSH. At the cellular level, triiodothyronine (T3) exerts its metabolic effects by binding to specific intracellular receptors. Which type of receptor mediates the primary genomic action of thyroid hormones?",
        "options": [
            "G-protein-coupled cell membrane receptor",
            "Receptor tyrosine kinase",
            "Nuclear transcription factor receptor",
            "Ligand-gated ion channel"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nThyroid hormones (T3 and T4) are lipophilic and enter target cells via specific monocarboxylate transporters (MCT8/10). Within the cytoplasm, T4 is converted to active T3 by 5'-deiodinases. T3 enters the nucleus and binds to thyroid hormone receptors (TR-alpha, TR-beta), which belong to the nuclear receptor superfamily. These receptors form heterodimers with retinoid X receptors (RXR) and bind to thyroid response elements (TRE) on target DNA, modulating the transcription of genes such as the Na+/K+-ATPase and uncoupling protein-1 (thermogenin).\n\nOption Review:\n- Option A is incorrect because G-protein-coupled membrane receptors mediate TSH and catecholamine actions, not thyroid hormone genomic actions.\n- Option B is incorrect because receptor tyrosine kinases mediate insulin and growth factor signaling.\n- Option C is correct because thyroid hormone receptors reside within the cell nucleus and function as ligand-activated transcription factors.\n- Option D is incorrect because ligand-gated ion channels mediate rapid neurotransmission (e.g., nicotinic ACh receptors).\n\nKey Takeaway: Thyroid hormones bind to nuclear receptors that dimerize with RXR to act as transcription factors regulating gene expression.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q028",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Neurophysiology - Cerebellar Functional Zones",
        "prompt": "A 58-year-old chronic alcoholic is brought to the neurology clinic with severe unsteadiness while walking. On examination, he has broad-based, reeling ataxia with marked trunk titubation, but finger-to-nose testing in the supine position shows minimal limb dysmetria. Which region of the cerebellum is selectively degenerated?",
        "options": [
            "Lateral cerebellar hemispheres",
            "Anterior vermis and spinocerebellum",
            "Flocculonodular lobe",
            "Dentate nucleus"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nAlcoholic cerebellar degeneration selectively affects the Purkinje cells of the anterior vermis and adjacent spinocerebellum. Because the vermis controls midline axial musculature, stance, and gait, its degeneration produces prominent truncal ataxia, broad-based staggering gait, and titubation. In contrast, the lateral cerebellar hemispheres (cerebrocerebellum), which coordinate fine distal limb movements via the dentate nucleus, are relatively spared, explaining why finger-to-nose and heel-to-shin testing are preserved when the patient is lying supported.\n\nOption Review:\n- Option A is incorrect because lateral hemisphere lesions produce ipsilateral limb dysmetria, intention tremor, and dysdiadochokinesia.\n- Option B is correct because chronic alcohol toxicity selectively damages the anterior vermis, causing isolated truncal and gait ataxia.\n- Option C is incorrect because flocculonodular (vestibulocerebellar) lesions characteristically cause nystagmus, vertigo, and loss of balance with head tilt.\n- Option D is incorrect because the dentate nucleus mediates lateral hemisphere output to the motor cortex.\n\nKey Takeaway: Alcoholic cerebellar degeneration selectively damages the anterior vermis, manifesting as profound truncal and gait ataxia with preserved distal limb coordination.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q029",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Hematology - Hemostasis & Platelet Activation",
        "prompt": "Following a vascular laceration, circulating platelets adhere to exposed subendothelial collagen. Under conditions of high shear stress in arterial blood vessels, which plasma glycoprotein bridges subendothelial collagen to the platelet surface receptor GPIb?",
        "options": [
            "Fibrinogen",
            "Von Willebrand factor",
            "Fibronectin",
            "Tissue factor"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nPrimary hemostasis begins with platelet adhesion to damaged vascular endothelium. Endothelial injury exposes subendothelial collagen. In high-shear environments (arterioles and capillaries), von Willebrand factor (vWF), synthesized by endothelial Weibel-Palade bodies and megakaryocytes, binds to the exposed collagen and undergoes a conformational change that allows it to bind to the platelet glycoprotein Ib (GPIb) receptor complex. This tethers platelets to the site of injury.\n\nOption Review:\n- Option A is incorrect because fibrinogen bridges platelets to each other by binding the activated GPIIb/IIIa complex during platelet aggregation.\n- Option B is correct because von Willebrand factor forms the essential bridge between subendothelial collagen and the platelet GPIb receptor.\n- Option C is incorrect because fibronectin contributes to extracellular matrix stability and secondary adhesion but is not the primary mediator at high shear.\n- Option D is incorrect because tissue factor (thromboplastin) activates factor VII to initiate the extrinsic coagulation cascade.\n\nKey Takeaway: Von Willebrand factor mediates initial platelet adhesion by binding subendothelial collagen to the platelet GPIb receptor under high shear stress.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q030",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Physiology - Baroreceptor Reflex",
        "prompt": "When a healthy individual stands up rapidly from a supine posture, approximately 500 mL of blood pools in the lower extremities due to gravity, temporarily lowering venous return and cardiac output. Within seconds, which compensatory baroreflex response restores mean arterial pressure?",
        "options": [
            "Increased firing of carotid sinus nerve and increased vagal outflow",
            "Decreased firing of carotid sinus nerve and increased sympathetic outflow",
            "Decreased firing of aortic arch nerve and decreased circulating catecholamines",
            "Increased firing of glossopharyngeal nerve and systemic vasodilation"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nArterial baroreceptors in the carotid sinus (innervated by the glossopharyngeal nerve via Hering's nerve) and aortic arch (innervated by the vagus nerve) are stretch receptors that fire tonically in proportion to arterial pressure. Upon standing, venous pooling drops arterial pressure and decreases wall stretch, leading to decreased afferent firing to the nucleus tractus solitarius (NTS) in the medulla. Reduced NTS stimulation disinhibits the rostral ventrolateral medulla (RVLM) and reduces parasympathetic vagal tone, triggering reflex tachycardia, enhanced cardiac contractility, and arteriolar vasoconstriction.\n\nOption Review:\n- Option A is incorrect because increased baroreceptor firing occurs during hypertension, stimulating vagal tone and causing bradycardia.\n- Option B is correct because hypotensive pooling decreases afferent baroreceptor discharge, triggering reflex sympathetic outflow and vagal withdrawal.\n- Option C is incorrect because sympathetic outflow and circulating catecholamines increase upon standing.\n- Option D is incorrect because decreased (not increased) glossopharyngeal firing occurs, promoting vasoconstriction instead of vasodilation.\n\nKey Takeaway: Orthostatic pooling reduces stretch on carotid sinus baroreceptors, decreasing afferent firing to trigger reflex sympathetic vasoconstriction and tachycardia.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q031",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Gastrointestinal - Bilirubin Processing & Secretion",
        "prompt": "In the hepatocyte, unconjugated bilirubin is conjugated with glucuronic acid to form water-soluble bilirubin diglucuronide. Which transport mechanism represents the rate-limiting step in hepatic bilirubin metabolism under physiological conditions?",
        "options": [
            "Uptake of unconjugated bilirubin across the sinusoidal membrane",
            "Intracellular binding of bilirubin to ligandin",
            "Conjugation of bilirubin by UDP-glucuronosyltransferase",
            "Active secretion of conjugated bilirubin into the bile canaliculus"
        ],
        "answerIndex": 3,
        "explanation": "Clinical Reasoning:\nHepatic processing of bilirubin involves four sequential phases: 1) Sinusoidal uptake of unconjugated bilirubin from albumin via OATP1B1/1B3; 2) Cytoplasmic binding to ligandin (glutathione S-transferase); 3) Endoplasmic reticulum conjugation with glucuronic acid by UGT1A1; 4) ATP-dependent canalicular excretion mediated by the multidrug resistance-associated protein 2 (MRP2/ABCC2). Canalicular secretion against a steep concentration gradient is the slowest and rate-limiting step of the entire pathway, making it the most vulnerable to impairment during hepatocellular injury or cholestasis (and congenitally mutated in Dubin-Johnson syndrome).\n\nOption Review:\n- Option A is incorrect because sinusoidal uptake is rapid and high-capacity.\n- Option B is incorrect because intracellular ligandin binding is non-rate-limiting.\n- Option C is incorrect because UGT1A1 conjugation occurs in excess capacity under physiological conditions.\n- Option D is correct because active ATP-dependent canalicular transport across the canalicular membrane via MRP2 is the rate-limiting step.\n\nKey Takeaway: The rate-limiting step in hepatic bilirubin processing is the active secretion of conjugated bilirubin into the bile canaliculi via MRP2.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q032",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Physiology - Skeletal Muscle Contraction",
        "prompt": "During skeletal muscle excitation-contraction coupling, depolarization of the T-tubule membrane triggers conformational change in which voltage-sensing receptor that physically interacts with the ryanodine receptor (RyR1) on the sarcoplasmic reticulum?",
        "options": [
            "Dihydropyridine receptor",
            "Nicotinic acetylcholine receptor",
            "Sarcoendoplasmic reticulum calcium ATPase",
            "Calsequestrin receptor"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIn skeletal muscle, action potentials travel deep into the myocyte along the invaginations of the sarcolemma (transverse tubules or T-tubules). The T-tubule membrane contains voltage-gated L-type calcium channels called dihydropyridine receptors (DHPR). Upon depolarization, DHPR undergoes a conformational change that mechanically pulls open the adjacent ryanodine receptors (RyR1) on the terminal cisternae of the sarcoplasmic reticulum, releasing stored Ca2+ into the sarcoplasm without requiring extracellular calcium entry (in contrast to cardiac muscle, which requires calcium-induced calcium release).\n\nOption Review:\n- Option A is correct because the dihydropyridine receptor acts as the T-tubule voltage sensor physically coupled to RyR1 in skeletal muscle.\n- Option B is incorrect because nicotinic receptors are ligand-gated channels located at the neuromuscular junction motor endplate.\n- Option C is incorrect because SERCA pumps calcium back into the sarcoplasmic reticulum during relaxation.\n- Option D is incorrect because calsequestrin is a low-affinity, high-capacity calcium-binding protein inside the SR lumen.\n\nKey Takeaway: Skeletal muscle contraction relies on mechanical coupling between the T-tubule dihydropyridine receptor (DHPR) and the sarcoplasmic ryanodine receptor (RyR1).",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q033",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Renal - Countercurrent Multiplier System",
        "prompt": "The medullary osmotic gradient is essential for the concentration of urine under the influence of ADH. The primary driving force that establishes this hypertonic medullary gradient is the active transport of ions occurring in which segment of the nephron?",
        "options": [
            "Thin descending limb of Henle's loop",
            "Thick ascending limb of Henle's loop",
            "Cortical collecting duct",
            "Proximal straight tubule"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe countercurrent multiplier in juxtamedullary nephrons generates the corticomedullary osmotic gradient (increasing from 300 mOsm/kg at the cortex to ~1200 mOsm/kg in the inner medulla). The single driving engine of this system is the thick ascending limb of Henle's loop (TAL), which actively reabsorbs sodium, potassium, and chloride via the apical NKCC2 transporter. Because the TAL is strictly impermeable to water, this solute transport continuously deposits salt into the medullary interstitium, concentrating fluid in the adjacent descending limbs and establishing the gradient.\n\nOption Review:\n- Option A is incorrect because the thin descending limb is permeable to water but does not actively transport solutes.\n- Option B is correct because the thick ascending limb actively pumps solutes via NKCC2 while remaining impermeable to water, powering countercurrent multiplication.\n- Option C is incorrect because the cortical collecting duct regulates final water reabsorption under ADH, but does not drive medullary hyperosmolality.\n- Option D is incorrect because the proximal straight tubule reabsorbs fluid isosmotically.\n\nKey Takeaway: The thick ascending limb of the loop of Henle serves as the active engine of the countercurrent multiplier by transporting solutes without water via NKCC2.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q034",
        "subjectId": "physiology",
        "subjectTitle": "Physiology",
        "topic": "Endocrine - Adrenal Cortex Regulation",
        "prompt": "A 28-year-old male with severe dehydration exhibits high circulating levels of angiotensin II. Angiotensin II acts on the zona glomerulosa of the adrenal cortex to stimulate the synthesis and secretion of aldosterone. Which key mitochondrial enzyme in the aldosterone pathway is specifically stimulated by angiotensin II?",
        "options": [
            "21-hydroxylase",
            "17-alpha-hydroxylase",
            "Aldosterone synthase",
            "11-beta-hydroxylase"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nIn the zona glomerulosa of the adrenal cortex, cholesterol is converted to pregnenolone, which undergoes sequential reactions via 3-beta-hydroxysteroid dehydrogenase, 21-hydroxylase, and 11-beta-hydroxylase to produce corticosterone. Angiotensin II and hyperkalemia directly stimulate aldosterone synthase (CYP11B2), a mitochondrial cytochrome P450 enzyme uniquely expressed in the zona glomerulosa, which catalyzes the final three steps: 11-beta-hydroxylation, 18-hydroxylation, and 18-oxidation of corticosterone into aldosterone.\n\nOption Review:\n- Option A is incorrect because 21-hydroxylase is present in both the zona glomerulosa and fasciculata, mediating early steps in cortisol and aldosterone synthesis.\n- Option B is incorrect because 17-alpha-hydroxylase is absent in the zona glomerulosa, which prevents this layer from synthesizing cortisol and androgens.\n- Option C is correct because aldosterone synthase (CYP11B2) is uniquely present in the zona glomerulosa and directly up-regulated by angiotensin II.\n- Option D is incorrect because 11-beta-hydroxylase converts 11-deoxycortisol to cortisol and 11-deoxycorticosterone to corticosterone, but does not complete aldosterone synthesis.\n\nKey Takeaway: Aldosterone synthase (CYP11B2) is uniquely expressed in the zona glomerulosa and catalyzed by angiotensin II to produce aldosterone.",
        "imageUrls": []
    },

    # ==========================================
    # BIOCHEMISTRY (17 Questions: Q035 - Q051)
    # ==========================================
    {
        "id": "fmge-gt1-q035",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Carbohydrate Metabolism - Glycolysis Regulation",
        "prompt": "During vigorous sprinting, rapid ATP generation is achieved through anaerobic glycolysis in skeletal muscle. Phosphofructokinase-1 (PFK-1) serves as the primary rate-limiting enzyme of this pathway. In the liver, which allosteric molecule is the most potent physiological activator of PFK-1?",
        "options": [
            "Adenosine triphosphate",
            "Fructose 2,6-bisphosphate",
            "Citrate",
            "Glucose 6-phosphate"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nPhosphofructokinase-1 (PFK-1) catalyzes the committed, rate-limiting step of glycolysis: phosphorylation of fructose 6-phosphate to fructose 1,6-bisphosphate. PFK-1 is allosterically inhibited by high levels of ATP and citrate (signals of high cellular energy). Its most potent physiological allosteric activator is fructose 2,6-bisphosphate (F-2,6-BP), synthesized by the bifunctional enzyme PFK-2/FBPase-2 under insulin stimulation. F-2,6-BP overcomes ATP inhibition and powerfully stimulates glycolysis.\n\nOption Review:\n- Option A is incorrect because ATP acts as an allosteric inhibitor of PFK-1.\n- Option B is correct because fructose 2,6-bisphosphate is the most potent allosteric stimulator of PFK-1.\n- Option C is incorrect because citrate is an allosteric inhibitor of PFK-1.\n- Option D is incorrect because glucose 6-phosphate inhibits hexokinase, not PFK-1.\n\nKey Takeaway: Fructose 2,6-bisphosphate is the most potent allosteric activator of phosphofructokinase-1, overcoming ATP-mediated feedback inhibition.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q036",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Inborn Errors of Metabolism - Phenylketonuria",
        "prompt": "A 4-month-old infant is brought to the pediatric clinic due to developmental delay, microcephaly, and a musty (mousy) body odor. Physical examination reveals fair skin, blonde hair, blue eyes, and eczema. What enzyme is deficient in this classic inborn error of metabolism?",
        "options": [
            "Homogentisate oxidase",
            "Phenylalanine hydroxylase",
            "Branched-chain alpha-keto acid dehydrogenase",
            "Tyrosinase"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nClassic phenylketonuria (PKU) is an autosomal recessive metabolic disorder caused by deficiency of phenylalanine hydroxylase (PAH), which converts phenylalanine to tyrosine using tetrahydrobiopterin (BH4) as a cofactor. Toxic accumulation of phenylalanine and its alternative transamination products (phenylacetate, phenylpyruvate, and phenyllactate) causes severe cognitive impairment, seizures, and the characteristic 'mousy/musty' odor. Tyrosine becomes an essential amino acid, and reduced melanin synthesis results in fair skin, blonde hair, and light eyes.\n\nOption Review:\n- Option A is incorrect because homogentisate oxidase deficiency causes alkaptonuria, characterized by dark urine on standing, ochronosis, and arthropathy.\n- Option B is correct because phenylalanine hydroxylase deficiency causes classic phenylketonuria.\n- Option C is incorrect because branched-chain alpha-keto acid dehydrogenase deficiency causes maple syrup urine disease (MSUD).\n- Option D is incorrect because tyrosinase deficiency results in oculocutaneous albinism without systemic neurologic deterioration or musty odor.\n\nKey Takeaway: Classic PKU is caused by phenylalanine hydroxylase deficiency, leading to intellectual disability, hypopigmentation, and a mousy body odor.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q037",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Glycogen Storage Diseases - Von Gierke Disease",
        "prompt": "A 6-month-old male infant presents with abdominal distension and failure to thrive. On physical examination, he has a rounded 'doll-like' face, thin extremities, and massive hepatomegaly, but normal spleen size. Laboratory tests reveal profound fasting hypoglycemia, lactic acidosis, hyperuricemia, and hyperlipidemia. Which enzyme is deficient?",
        "options": [
            "Glucose-6-phosphatase",
            "Lysosomal acid alpha-glucosidase",
            "Debranching enzyme",
            "Muscle glycogen phosphorylase"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nVon Gierke disease (Glycogen Storage Disease Type I) is caused by deficiency of glucose-6-phosphatase, the enzyme responsible for dephosphorylating glucose-6-phosphate to free glucose in the final step of both glycogenolysis and gluconeogenesis. In its absence, free glucose cannot be released into the blood, leading to severe fasting hypoglycemia. Trapped glucose-6-phosphate is shunted into glycolysis (producing severe lactic acidosis), the hexose monophosphate shunt/PRPP pathway (producing hyperuricemia/gout), and lipogenesis (producing marked hypertriglyceridemia and doll-like fat distribution).\n\nOption Review:\n- Option A is correct because glucose-6-phosphatase deficiency leads to Type I GSD (Von Gierke disease).\n- Option B is incorrect because lysosomal alpha-glucosidase (acid maltase) deficiency causes Pompe disease (Type II GSD), marked by fatal hypertrophic cardiomyopathy and hypotonia without severe hypoglycemia.\n- Option C is incorrect because debranching enzyme deficiency causes Cori disease (Type III GSD), which presents with milder hypoglycemia and accumulation of limit dextrins.\n- Option D is incorrect because muscle glycogen phosphorylase deficiency causes McArdle disease (Type V GSD), presenting in young adults with exercise-induced cramps and myoglobinuria.\n\nKey Takeaway: Von Gierke disease (GSD Type I) is due to glucose-6-phosphatase deficiency, presenting with doll-like facies, massive hepatomegaly, severe fasting hypoglycemia, and lactic acidosis.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q038",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Lipid Metabolism - Familial Hypercholesterolemia",
        "prompt": "A 16-year-old boy presents with yellowish, nodular deposits over his Achilles tendons and extensor tendons of the hands. His father died of a myocardial infarction at age 38. Fasting lipid panel reveals total cholesterol of 620 mg/dL and LDL cholesterol of 530 mg/dL, with normal triglycerides. Which receptor protein is mutated in this autosomal dominant condition?",
        "options": [
            "Low-density lipoprotein receptor",
            "Apolipoprotein E receptor",
            "Scavenger receptor B1",
            "Very-low-density lipoprotein receptor"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nFamilial hypercholesterolemia (Type IIa hyperlipidemia) is an autosomal dominant disorder caused by mutations in the low-density lipoprotein (LDL) receptor gene (or less commonly in APOB or PCSK9). Defective or absent LDL receptors prevent hepatic clearance of circulating LDL particles, resulting in severely elevated plasma LDL cholesterol. Excess LDL is phagocytosed by macrophages and deposited in tissues, producing characteristic tendon xanthomas (especially Achilles tendons), xanthelasmas, and accelerated atherosclerotic coronary artery disease presenting at a young age.\n\nOption Review:\n- Option A is correct because mutations in the LDL receptor cause classic familial hypercholesterolemia.\n- Option B is incorrect because apolipoprotein E deficiency causes Type III hyperlipoproteinemia (dysbetalipoproteinemia), characterized by elevated chylomicron remnants/IDL and palmar xanthomas.\n- Option C is incorrect because scavenger receptor B1 mediates HDL cholesterol uptake.\n- Option D is incorrect because VLDL receptor defects do not cause classic tendon xanthomas and isolated severe LDL elevation.\n\nKey Takeaway: Familial hypercholesterolemia is an autosomal dominant condition caused by LDL receptor deficiency, characterized by tendon xanthomas and premature coronary atherosclerosis.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Xanthoma_tendon.jpg/640px-Xanthoma_tendon.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q039",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "HMP Shunt - G6PD Deficiency",
        "prompt": "A 26-year-old male with malaria is prescribed primaquine. Three days later, he presents with sudden jaundice, dark brown urine, and fatigue. Blood smear reveals red blood cells containing Heinz bodies and 'bite cells'. Which biochemical product of the hexose monophosphate shunt is deficient in maintaining reduced glutathione in this patient's erythrocytes?",
        "options": [
            "Nicotinamide adenine dinucleotide",
            "Nicotinamide adenine dinucleotide phosphate",
            "Adenosine triphosphate",
            "Flavin adenine dinucleotide"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nGlucose-6-phosphate dehydrogenase (G6PD) catalyzes the first, rate-limiting step of the hexose monophosphate (HMP) shunt: the oxidation of glucose-6-phosphate to 6-phosphoglucono-delta-lactone. This reaction reduces NADP+ to NADPH. In erythrocytes, which lack mitochondria, the HMP shunt is the sole source of NADPH. NADPH is required by glutathione reductase to regenerate reduced glutathione (GSH), which neutralizes reactive oxygen species. In G6PD deficiency, oxidative drugs (primaquine, dapsone, sulfonamides) deplete GSH, allowing oxidants to denature hemoglobin into Heinz bodies. Splenic macrophages remove these inclusions, forming 'bite cells' and precipitating acute intravascular hemolysis.\n\nOption Review:\n- Option A is incorrect because NADH is generated by glycolysis and the TCA cycle, not the primary antioxidant shield of RBCs.\n- Option B is correct because NADPH generated by the HMP shunt is required to maintain glutathione in its reduced, protective state.\n- Option C is incorrect because ATP is produced by glycolysis; its deficiency occurs in pyruvate kinase deficiency.\n- Option D is incorrect because FAD is a cofactor for complex II and flavoproteins, not the antioxidant electron donor.\n\nKey Takeaway: G6PD deficiency impairs NADPH production in erythrocytes, preventing glutathione reduction and precipitating oxidative hemolysis after exposure to drugs like primaquine.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q040",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Vitamins - Vitamin B1 (Thiamine) Deficiency",
        "prompt": "A 54-year-old homeless male with chronic alcohol use disorder is brought to the emergency department confused, disoriented, and unable to walk independently. Physical examination reveals bilateral lateral rectus palsy and horizontal nystagmus. Intravenous thiamine is administered immediately. Which enzyme requires thiamine pyrophosphate as a cofactor in carbohydrate metabolism?",
        "options": [
            "Lactate dehydrogenase",
            "Pyruvate dehydrogenase complex",
            "Malate dehydrogenase",
            "Succinate dehydrogenase"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nThe clinical triad of acute confusion, ophthalmoplegia (CN VI palsy/nystagmus), and ataxia defines Wernicke encephalopathy, caused by severe thiamine (vitamin B1) deficiency in chronic alcoholism. Thiamine pyrophosphate (TPP) serves as an essential cofactor for four key multienzyme complexes: 1) Pyruvate dehydrogenase (links glycolysis to TCA cycle); 2) Alpha-ketoglutarate dehydrogenase (TCA cycle); 3) Transketolase (HMP shunt); 4) Branched-chain alpha-keto acid dehydrogenase (amino acid catabolism). Administration of glucose before thiamine precipitates severe lactic acidosis and fatal encephalopathy because pyruvate cannot enter the TCA cycle.\n\nOption Review:\n- Option A is incorrect because lactate dehydrogenase requires NAD+/NADH, not thiamine.\n- Option B is correct because the pyruvate dehydrogenase complex requires thiamine pyrophosphate (TPP) as its E1 prosthetic group.\n- Option C is incorrect because malate dehydrogenase uses NAD+ as a cofactor.\n- Option D is incorrect because succinate dehydrogenase uses FAD as its electron acceptor.\n\nKey Takeaway: Thiamine pyrophosphate (TPP) is an indispensable cofactor for pyruvate dehydrogenase, alpha-ketoglutarate dehydrogenase, and transketolase.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q041",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Purine Metabolism - Lesch-Nyhan Syndrome",
        "prompt": "A 14-month-old male infant presents with severe motor delay, choreoathetosis, spasticity, and compulsive self-mutilation (biting his lips and fingertips). Orange, sand-like crystals are noted in his diapers. Serum uric acid is markedly elevated. Which purine salvage pathway enzyme is deficient in this X-linked recessive disorder?",
        "options": [
            "Adenosine deaminase",
            "Hypoxanthine-guanine phosphoribosyltransferase",
            "Xanthine oxidase",
            "Phosphoribosylpyrophosphate synthetase"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nLesch-Nyhan syndrome is an X-linked recessive disorder caused by deficiency of hypoxanthine-guanine phosphoribosyltransferase (HGPRT). HGPRT salvages hypoxanthine to IMP and guanine to GMP using PRPP. When HGPRT is absent, purine bases cannot be salvaged and are degraded to uric acid by xanthine oxidase, leading to severe hyperuricemia, nephrolithiasis, and gouty arthritis ('orange sand' in diapers). Lack of salvage also drives de novo purine synthesis by elevating PRPP levels, resulting in severe basal ganglia dysfunction, choreoathetosis, cognitive impairment, and compulsive self-injurious behavior.\n\nOption Review:\n- Option A is incorrect because adenosine deaminase (ADA) deficiency causes severe combined immunodeficiency (SCID) due to toxic dATP accumulation in lymphocytes.\n- Option B is correct because HGPRT deficiency causes classic Lesch-Nyhan syndrome.\n- Option C is incorrect because xanthine oxidase converts hypoxanthine to xanthine and uric acid; it is inhibited by allopurinol.\n- Option D is incorrect because PRPP synthetase superactivity can cause hyperuricemia, but does not produce the characteristic self-mutilation of Lesch-Nyhan syndrome.\n\nKey Takeaway: Lesch-Nyhan syndrome is caused by HGPRT deficiency, leading to severe hyperuricemia, gout, spastic choreoathetosis, and compulsive self-mutilation.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q042",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Urea Cycle Disorders - Ornithine Transcarbamylase Deficiency",
        "prompt": "A 3-day-old male newborn becomes lethargic, feeds poorly, and develops hyperventilation and seizures. Serum ammonia is 650 micromol/L (profoundly elevated). Plasma amino acid analysis reveals markedly increased glutamine and undetectable citrulline. Urine organic acid analysis reveals markedly elevated orotic acid. What is the most common urea cycle enzyme deficiency responsible for these findings?",
        "options": [
            "Carbamoyl phosphate synthetase I",
            "Ornithine transcarbamylase",
            "Argininosuccinate synthetase",
            "Arginase"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nOrnithine transcarbamylase (OTC) deficiency is the most common urea cycle disorder and the only one inherited in an X-linked recessive pattern (the others are autosomal recessive). In the mitochondrial matrix, OTC combines carbamoyl phosphate with ornithine to produce citrulline. When OTC is deficient, carbamoyl phosphate accumulates in the mitochondria and overflows into the cytoplasm, where it enters the pyrimidine synthesis pathway, leading to massive synthesis and urinary excretion of orotic acid. The block in the urea cycle produces severe hyperammonemia without citrulline.\n\nOption Review:\n- Option A is incorrect because Carbamoyl Phosphate Synthetase I (CPS I) deficiency also causes hyperammonemia, but carbamoyl phosphate is not synthesized, so urine orotic acid is low or normal.\n- Option B is correct because OTC deficiency leads to accumulated carbamoyl phosphate shunted into pyrimidine synthesis, producing orotic aciduria with hyperammonemia.\n- Option C is incorrect because argininosuccinate synthetase deficiency causes classic citrullinemia with massively elevated plasma citrulline.\n- Option D is incorrect because arginase deficiency presents late in childhood with progressive spastic diplegia and only mild hyperammonemia.\n\nKey Takeaway: OTC deficiency is an X-linked urea cycle disorder distinguished from CPS I deficiency by the presence of massive urinary orotic acid excretion.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q043",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Porphyria - Acute Intermittent Porphyria",
        "prompt": "A 27-year-old woman is admitted with severe colicky abdominal pain, vomiting, and confusion following a fast. Physical examination reveals tachycardia and peripheral motor neuropathy, with no rash. Her urine turns port-wine colored after exposure to sunlight. What enzyme is deficient in this autosomal dominant hepatic porphyria?",
        "options": [
            "Porphobilinogen deaminase",
            "Uroporphyrinogen decarboxylase",
            "ALA dehydratase",
            "Ferrochelatase"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAcute intermittent porphyria (AIP) is an autosomal dominant disorder caused by deficiency of porphobilinogen deaminase (also known as hydroxymethylbilane synthase). Attacks are precipitated by cytochrome P450 inducers (antiepileptics, barbiturates), fasting, or infection, which induce hepatic ALA synthase-1. The metabolic block leads to accumulation of neurotoxic porphyrin precursors: delta-aminolevulinic acid (ALA) and porphobilinogen (PBG). Clinical features include the classic 5 P's: Painful abdomen, Port-wine urine, Polyneuropathy, Psychological disturbances, and Precipitated by drugs. Notably, cutaneous photosensitivity is ABSENT because porphyrin rings have not yet formed.\n\nOption Review:\n- Option A is correct because porphobilinogen deaminase deficiency causes acute intermittent porphyria.\n- Option B is incorrect because uroporphyrinogen decarboxylase deficiency causes porphyria cutanea tarda (PCT), characterized by prominent blistering skin photosensitivity and hypertrichosis.\n- Option C is incorrect because ALA dehydratase deficiency is exceedingly rare and mimics lead poisoning.\n- Option D is incorrect because ferrochelatase deficiency causes erythropoietic protoporphyria, presenting with immediate painful solar burning.\n\nKey Takeaway: Acute intermittent porphyria is caused by porphobilinogen deaminase deficiency; it presents with abdominal pain, neurovisceral symptoms, and dark urine without cutaneous blisters.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q044",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Vitamins - Vitamin B12 vs Folate Deficiency",
        "prompt": "A 62-year-old female with autoimmune gastritis presents with progressive paresthesias in both feet, difficulty walking, and memory loss. Complete blood count shows macrocytic anemia (MCV 112 fL) with hypersegmented neutrophils. Serum methylmalonic acid and homocysteine are both elevated. Which coenzyme-dependent enzyme deficiency accounts for the accumulation of methylmalonic acid?",
        "options": [
            "Methionine synthase",
            "Methylmalonyl-CoA mutase",
            "Cystathionine beta-synthase",
            "Thymidylate synthase"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nVitamin B12 (cobalamin) serves as an essential cofactor for only two enzymes in humans: 1) Methionine synthase (converts homocysteine to methionine using methylcobalamin); 2) Methylmalonyl-CoA mutase (converts methylmalonyl-CoA to succinyl-CoA using adenosylcobalamin). In B12 deficiency, both homocysteine and methylmalonic acid (MMA) accumulate in plasma. In contrast, folate deficiency elevates homocysteine but leaves MMA levels entirely normal. Accumulation of abnormal methylmalonic acid contributes to myelin sheath breakdown in the posterior and lateral columns of the spinal cord (subacute combined degeneration).\n\nOption Review:\n- Option A is incorrect because methionine synthase deficiency elevates homocysteine, but not methylmalonic acid.\n- Option B is correct because methylmalonyl-CoA mutase requires adenosylcobalamin; its impairment leads to accumulation of methylmalonic acid.\n- Option C is incorrect because cystathionine beta-synthase requires vitamin B6 (pyridoxine) to convert homocysteine to cystathionine.\n- Option D is incorrect because thymidylate synthase requires N5,N10-methylene-THF, which is blocked in folate deficiency.\n\nKey Takeaway: Elevated methylmalonic acid (MMA) is specific for vitamin B12 deficiency (due to methylmalonyl-CoA mutase impairment) and differentiates it from folate deficiency.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q045",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Amino Acid Metabolism - Alkaptonuria",
        "prompt": "A 38-year-old male presents with severe bilateral lower back and knee pain. Physical examination reveals slate-blue pigmentation of the sclerae and ear cartilage (ochronosis). He notes that since childhood, his urine turns dark brown or black upon standing. What enzyme deficiency causes the accumulation of homogentisic acid in this condition?",
        "options": [
            "Homogentisate 1,2-dioxygenase",
            "Fumarylacetoacetate hydrolase",
            "Tyrosine aminotransferase",
            "Branched-chain amino acid transaminase"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nAlkaptonuria is a benign-appearing in childhood, autosomal recessive disorder of tyrosine degradation caused by deficiency of homogentisate 1,2-dioxygenase (homogentisic acid oxidase). Homogentisic acid accumulates and is excreted in urine, where oxidation by atmospheric oxygen polymerizes it into a dark-pigmented substance (urine turning black upon standing). In adulthood, circulating homogentisate polymer binds to collagen in cartilage and connective tissues (ochronosis), leading to slate-gray pigmentation of the ear cartilage and sclerae, and severe degenerative ochronotic arthropathy.\n\nOption Review:\n- Option A is correct because deficiency of homogentisate 1,2-dioxygenase causes alkaptonuria.\n- Option B is incorrect because fumarylacetoacetate hydrolase deficiency causes Tyrosinemia Type I, presenting with severe infant liver failure, renal Fanconi syndrome, and cabbage-like odor.\n- Option C is incorrect because tyrosine aminotransferase deficiency causes Tyrosinemia Type II, characterized by painful palmoplantar hyperkeratosis and corneal ulcers.\n- Option D is incorrect because branched-chain aminotransferase initiates catabolism of leucine, isoleucine, and valine.\n\nKey Takeaway: Alkaptonuria is caused by homogentisate oxidase deficiency, presenting with urine turning black on standing, ochronosis of cartilage, and severe arthropathy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q046",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Lipid Storage Diseases - Tay-Sachs Disease",
        "prompt": "A 6-month-old infant of Ashkenazi Jewish ancestry is brought to the clinic due to loss of developmental milestones, progressive muscle weakness, and hyperacusis (startle response to loud sounds). Fundoscopic examination reveals a prominent cherry-red spot in the macula. Hepatomegaly and splenomegaly are absent. Which lysosomal enzyme is deficient?",
        "options": [
            "Sphingomyelinase",
            "Beta-hexosaminidase A",
            "Glucocerebrosidase",
            "Alpha-L-iduronidase"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nTay-Sachs disease is an autosomal recessive lysosomal storage disease caused by deficiency of beta-hexosaminidase A, resulting in toxic accumulation of GM2 ganglioside in the central nervous system. Infants develop progressive neurodegeneration, developmental regression, hyperacusis, seizures, and blindness. The classic macular 'cherry-red spot' occurs because lipid-laden retinal ganglion cells swell and become pale, accentuating the normal red vascularity of the underlying choroid at the fovea. Unlike Niemann-Pick disease (sphingomyelinase deficiency), hepatosplenomegaly is conspicuously ABSENT in Tay-Sachs disease.\n\nOption Review:\n- Option A is incorrect because sphingomyelinase deficiency causes Niemann-Pick disease, which presents with a cherry-red spot PLUS prominent hepatosplenomegaly and foam cells on bone marrow biopsy.\n- Option B is correct because beta-hexosaminidase A deficiency causes Tay-Sachs disease (cherry-red spot without hepatosplenomegaly).\n- Option C is incorrect because glucocerebrosidase deficiency causes Gaucher disease, presenting with massive splenomegaly, pancytopenia, and aseptic necrosis of the femoral head, without a cherry-red spot.\n- Option D is incorrect because alpha-L-iduronidase deficiency causes Hurler syndrome (MPS I), characterized by coarse facial features and corneal clouding.\n\nKey Takeaway: Tay-Sachs disease is caused by beta-hexosaminidase A deficiency, characterized by neurodegeneration and a macular cherry-red spot WITHOUT hepatosplenomegaly.",
        "imageUrls": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Cherry_red_spot.jpg/640px-Cherry_red_spot.jpg"
        ]
    },
    {
        "id": "fmge-gt1-q047",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Vitamins - Vitamin C Deficiency (Scurvy)",
        "prompt": "An elderly widower living alone on a diet consisting solely of canned soup and white bread presents with lethargy, bleeding gums around loose teeth, corkscrew hairs, and extensive perifollicular petechiae over both lower legs. Ascorbic acid (vitamin C) deficiency impairs which post-translational modification of procollagen alpha chains?",
        "options": [
            "Glycosylation of hydroxylysine residues",
            "Hydroxylation of proline and lysine residues",
            "Cleavage of procollagen C- and N-terminal propeptides",
            "Oxidative deamination of lysine residues by lysyl oxidase"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nScurvy results from nutritional deficiency of vitamin C (ascorbic acid). Ascorbic acid acts as an essential reducing agent to keep iron in its active ferrous (Fe2+) state for the enzymes prolyl hydroxylase and lysyl hydroxylase in the rough endoplasmic reticulum. These enzymes hydroxylate specific proline and lysine residues on nascent procollagen chains. Hydroxyproline is required for stable triple-helix hydrogen bonding; without it, defective collagen denatures at body temperature. Capillary fragility leads to perifollicular hemorrhages, subperiosteal hematomas, corkscrew hairs, and bleeding spongy gums.\n\nOption Review:\n- Option A is incorrect because glycosylation occurs following hydroxylation, but is not directly vitamin C-dependent.\n- Option B is correct because vitamin C is an obligatory cofactor for prolyl and lysyl hydroxylase.\n- Option C is incorrect because cleavage of terminal propeptides occurs extracellularly by procollagen peptidases.\n- Option D is incorrect because lysyl oxidase cross-linking is an extracellular process that requires copper, not vitamin C.\n\nKey Takeaway: Vitamin C is required for the post-translational hydroxylation of proline and lysine residues during collagen biosynthesis; deficiency results in scurvy.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q048",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Molecular Biology - DNA Repair Mechanisms",
        "prompt": "A 9-year-old child presents with severe sun sensitivity, marked freckling, and skin xerosis on minimal sun exposure. By age 8, he has developed multiple cutaneous squamous cell carcinomas and basal cell carcinomas. Cultured skin fibroblasts fail to repair ultraviolet-induced cyclobutane pyrimidine dimers. Which DNA repair pathway is defective in xeroderma pigmentosum?",
        "options": [
            "Mismatch repair",
            "Base excision repair",
            "Nucleotide excision repair",
            "Homologous end-joining"
        ],
        "answerIndex": 2,
        "explanation": "Clinical Reasoning:\nXeroderma pigmentosum (XP) is an autosomal recessive disorder caused by mutations in nucleotide excision repair (NER) genes (XPA through XPG). Ultraviolet radiation induces covalent cross-links between adjacent pyrimidine bases (thymine-thymine dimers), distorting the DNA double helix. In healthy cells, the NER pathway recognizes the bulky distortion, an endonuclease excises an oligonucleotide fragment containing the lesion, and DNA polymerase and ligase fill and seal the gap. When NER is defective, unrepaired pyrimidine dimers lead to translesion mutations and a 2000-fold increase in skin cancer risk.\n\nOption Review:\n- Option A is incorrect because mismatch repair corrects single-base errors and microsatellite slips during replication; mutations cause Lynch syndrome (HNPCC).\n- Option B is incorrect because base excision repair (BER) uses DNA glycosylases to remove single damaged bases (e.g., deaminated cytosine or 8-oxoguanine).\n- Option C is correct because nucleotide excision repair is responsible for removing UV-induced pyrimidine dimers.\n- Option D is incorrect because homologous recombination repairs double-strand DNA breaks and is defective in BRCA mutations.\n\nKey Takeaway: Xeroderma pigmentosum is caused by a defect in nucleotide excision repair (NER), resulting in the inability to remove UV-induced pyrimidine dimers.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q049",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Lipid Metabolism - Carnitine Shuttle Deficiency",
        "prompt": "A 4-year-old girl is admitted to the pediatric ICU with lethargy, vomiting, and stupor following a 24-hour gastrointestinal illness with poor oral intake. Blood glucose is 28 mg/dL (severe hypoglycemia). Urinalysis shows completely absent ketones. Serum free carnitine levels are profoundly reduced, and acylcarnitine is elevated. What physiological process is impaired by carnitine deficiency?",
        "options": [
            "Transport of long-chain fatty acids into mitochondria for beta-oxidation",
            "Cytoplasmic synthesis of palmitate by fatty acid synthase",
            "Mitochondrial synthesis of acetoacetate from acetyl-CoA",
            "Peroxisomal alpha-oxidation of branched-chain phytanic acid"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nDuring prolonged fasting, skeletal muscle and hepatocytes rely on beta-oxidation of long-chain fatty acids (LCFA) to generate ATP, NADH, and acetyl-CoA (which drives gluconeogenesis and ketogenesis). While short- and medium-chain fatty acids freely diffuse into mitochondria, long-chain fatty acyl-CoA molecules cannot penetrate the inner mitochondrial membrane. They must be conjugated to carnitine by Carnitine Palmitoyltransferase-1 (CPT-1), transported across via carnitine-acylcarnitine translocase, and converted back by CPT-2. Carnitine deficiency blocks mitochondrial entry of LCFAs, causing non-ketotic (hypoketotic) hypoglycemia, hepatic steatosis, and cardiomyopathy.\n\nOption Review:\n- Option A is correct because the carnitine shuttle is required to transport long-chain fatty acids across the inner mitochondrial membrane for beta-oxidation.\n- Option B is incorrect because fatty acid synthesis occurs in the cytoplasm and requires citrate and ACP.\n- Option C is incorrect because ketogenesis is downstream of beta-oxidation and fails secondarily due to lack of acetyl-CoA.\n- Option D is incorrect because peroxisomal alpha-oxidation breaks down phytanic acid; its defect causes Refsum disease.\n\nKey Takeaway: Carnitine deficiency impairs the transport of long-chain fatty acids into the mitochondrial matrix, producing severe hypoketotic hypoglycemia during fasting.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q050",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Heme Synthesis - Acute Lead Poisoning",
        "prompt": "A 3-year-old child living in a pre-1970 urban home presents with lethargy, irritability, abdominal colic, and poor attention. Complete blood count shows microcytic hypochromic anemia, and peripheral smear reveals basophilic stippling of erythrocytes. Lead inhibits two critical enzymes in the heme biosynthetic pathway: ferrochelatase and which other early cytoplasmic enzyme?",
        "options": [
            "Porphobilinogen deaminase",
            "Delta-aminolevulinic acid dehydratase",
            "Uroporphyrinogen decarboxylase",
            "Coprophyrinogen oxidase"
        ],
        "answerIndex": 1,
        "explanation": "Clinical Reasoning:\nLead toxicity inactivates zinc-dependent sulfhydryl-containing enzymes throughout the body. In the heme biosynthesis pathway, lead directly inhibits two enzymes: 1) Delta-aminolevulinic acid dehydratase (ALA dehydratase / porphobilinogen synthase), which converts ALA to porphobilinogen in the cytoplasm; 2) Ferrochelatase, which inserts ferrous iron (Fe2+) into protoporphyrin IX in the mitochondria. Inhibition of ALA dehydratase causes elevated blood levels of delta-ALA, while inhibition of ferrochelatase results in accumulation of zinc protoporphyrin in erythrocytes. Basophilic stippling occurs due to lead inhibition of pyrimidine 5'-nucleotidase, causing ribosomal RNA aggregation.\n\nOption Review:\n- Option A is incorrect because porphobilinogen deaminase is deficient in acute intermittent porphyria.\n- Option B is correct because delta-aminolevulinic acid dehydratase (ALA dehydratase) is directly inhibited by lead, alongside ferrochelatase.\n- Option C is incorrect because uroporphyrinogen decarboxylase is deficient in porphyria cutanea tarda.\n- Option D is incorrect because coproporphyrinogen oxidase is deficient in hereditary coproporphyria.\n\nKey Takeaway: Lead poisoning inhibits delta-aminolevulinic acid (ALA) dehydratase and ferrochelatase, resulting in elevated blood ALA and zinc protoporphyrin with basophilic stippling.",
        "imageUrls": []
    },
    {
        "id": "fmge-gt1-q051",
        "subjectId": "biochemistry",
        "subjectTitle": "Biochemistry",
        "topic": "Enzyme Kinetics - Competitive vs Non-competitive Inhibition",
        "prompt": "An investigator studies the inhibition of a metabolic enzyme in the presence of a new pharmacological agent. Analysis of Lineweaver-Burk (double reciprocal) plots demonstrates that the inhibitor increases the apparent Michaelis constant (Km) without changing the maximum reaction velocity (Vmax). What type of enzyme inhibition does this agent exhibit?",
        "options": [
            "Competitive inhibition",
            "Non-competitive inhibition",
            "Uncompetitive inhibition",
            "Irreversible inhibition"
        ],
        "answerIndex": 0,
        "explanation": "Clinical Reasoning:\nIn enzyme kinetics: 1) A competitive inhibitor reversibly binds to the active site of the free enzyme, competing directly with the substrate. High concentrations of substrate can displace the inhibitor, meaning maximum velocity (Vmax) is unchanged. However, more substrate is needed to achieve half-maximal velocity, so the apparent Michaelis constant (Km) increases (x-intercept on Lineweaver-Burk plot moves closer to zero). 2) A non-competitive inhibitor binds to an allosteric site on both free enzyme and enzyme-substrate complex, reducing Vmax while leaving Km unchanged. 3) An uncompetitive inhibitor binds only to the ES complex, reducing both Vmax and Km proportionally.\n\nOption Review:\n- Option A is correct because competitive inhibitors increase apparent Km while leaving Vmax unchanged.\n- Option B is incorrect because non-competitive inhibitors decrease Vmax while keeping Km unchanged.\n- Option C is incorrect because uncompetitive inhibitors decrease both Km and Vmax in parallel.\n- Option D is incorrect because irreversible inhibitors permanently decrease the pool of active enzyme, lowering Vmax.\n\nKey Takeaway: Competitive inhibitors increase the apparent Km without altering Vmax because excess substrate can overcome the active site competition.",
        "imageUrls": []
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(QUESTIONS)} questions in Part 1 Block 1.")
    for q in QUESTIONS:
        assert len(q["options"]) == 4, f"{q['id']} does not have 4 options"
        assert 0 <= q["answerIndex"] <= 3, f"{q['id']} invalid answerIndex"
        for opt in q["options"]:
            assert not opt.endswith(";"), f"{q['id']} option ends with semicolon: {opt}"
            assert "(" not in opt or any(c.isdigit() for c in opt), f"{q['id']} option has explanatory bracket: {opt}"
    print("All 51 questions passed structural assertions.")
