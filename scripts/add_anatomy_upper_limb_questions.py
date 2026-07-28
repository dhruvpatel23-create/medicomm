import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Upper Limb"
BASE = {"subjectId": "anatomy", "subjectTitle": "Anatomy", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("introduction", "Introduction", [
        q("The upper limb is chiefly specialized for:", "Mobility and skilled prehension", ["Weight transmission only", "Respiration", "Pelvic support"], "The upper limb evolved for mobility, manipulation, and fine skilled movements."),
        q("The anatomical root of the upper limb is attached to the axial skeleton mainly through the:", "Pectoral girdle", ["Pelvic girdle", "Thoracic cage only", "Vertebral arches"], "The clavicle and scapula form the pectoral girdle attaching the limb to the trunk."),
        q("The only bony articulation between upper limb and axial skeleton is the:", "Sternoclavicular joint", ["Acromioclavicular joint", "Glenohumeral joint", "Costovertebral joint"], "The clavicle articulates with the sternum at the sternoclavicular joint."),
        q("In anatomical position, the thumb lies on the:", "Lateral side of the hand", ["Medial side of the hand", "Posterior midline", "Proximal border"], "With palms facing anteriorly, the thumb is lateral."),
        q("Pronation of forearm occurs mainly at:", "Radioulnar joints", ["Elbow hinge only", "Wrist joint only", "Intercarpal joints"], "Pronation-supination happens at proximal and distal radioulnar joints."),
        q("The preaxial border of the upper limb corresponds to the:", "Thumb/radial side", ["Little finger/ulnar side", "Posterior arm only", "Axillary apex"], "Preaxial side is radial/thumb side; postaxial side is ulnar/little finger side."),
        q("Upper limb dermatomes are clinically used to localize:", "Spinal nerve root lesions", ["Arterial aneurysms only", "Bone age only", "Lymph node metastasis only"], "Dermatomal sensory loss helps identify involved roots."),
        q("The functional value of clavicle is that it:", "Holds the limb away from trunk", ["Eliminates all shoulder movement", "Forms the arm bone", "Protects the pelvic inlet"], "The clavicle acts as a strut allowing free upper limb movement."),
        q("Most upper limb muscles receive motor supply from:", "Brachial plexus", ["Cervical plexus only", "Lumbar plexus", "Sacral plexus"], "The brachial plexus supplies most muscles of the upper limb."),
        q("A structure described as distal in the upper limb is:", "Farther from the shoulder root", ["Nearer the median plane", "Nearer the skin", "Toward the head"], "Distal means farther from the limb attachment."),
        q("Opposition of thumb is important because it permits:", "Precision grip", ["Knee locking", "Forced expiration", "Scapular depression only"], "Thumb opposition is central to human precision handling."),
        q("The limb bud preaxial/postaxial pattern explains why the:", "Radius is on thumb side and ulna on little-finger side", ["Femur is in upper limb", "Scapula is a carpal bone", "Clavicle is absent"], "Developmental axes correspond to adult radial and ulnar sides."),
        q("Compared with lower limb, upper limb joints generally favor:", "Mobility over stability", ["Stability over mobility", "Weight bearing only", "No rotation"], "Upper limb sacrifices stability for range and dexterity."),
        q("A clinical examination of upper limb begins best with:", "Inspection, palpation, movements and neurovascular assessment", ["Only auscultation", "Only abdominal reflex", "Only skull measurement"], "Upper limb anatomy is tested by systematic surface and functional assessment."),
        q("The most important evolutionary adaptation of human upper limb is:", "Freeing the hand for manipulation", ["Permanent fixation to trunk", "Loss of thumb", "Reduction of shoulder mobility"], "Bipedal posture allowed upper limb specialization for manipulation."),
    ]),
    ("bones-upper-limb", "Bones of Upper Limb", [
        q("The clavicle commonly fractures at the junction of:", "Medial two-thirds and lateral one-third", ["Medial end only", "Acromial facet only", "Conoid tubercle only"], "The junction of medial 2/3 and lateral 1/3 is the weakest point."),
        q("The subclavian vessels and brachial plexus pass posterior to the:", "Clavicle", ["Scaphoid", "Olecranon", "Capitate"], "Clavicular fractures may endanger underlying neurovascular structures."),
        q("The glenoid cavity belongs to the:", "Scapula", ["Clavicle", "Humerus", "Radius"], "The scapular glenoid cavity articulates with the humeral head."),
        q("The surgical neck of humerus is closely related to:", "Axillary nerve", ["Median nerve", "Ulnar nerve", "Musculocutaneous nerve"], "Axillary nerve and posterior circumflex humeral vessels wind around the surgical neck."),
        q("Radial nerve injury is classically associated with fracture of:", "Shaft of humerus", ["Surgical neck of humerus", "Medial epicondyle", "Scaphoid waist"], "Radial nerve runs in the spiral groove on posterior humeral shaft."),
        q("Ulnar nerve is vulnerable behind the:", "Medial epicondyle of humerus", ["Lateral epicondyle", "Radial tuberosity", "Supraglenoid tubercle"], "The ulnar nerve passes posterior to medial epicondyle."),
        q("The head of radius is located:", "Proximally", ["Distally", "In the carpus", "At the scapula"], "Radius has head proximally and styloid process distally."),
        q("The olecranon is part of the:", "Ulna", ["Radius", "Humerus", "Scapula"], "Olecranon forms the prominence of elbow and fits in olecranon fossa."),
        q("The carpal bone most commonly fractured after fall on outstretched hand is:", "Scaphoid", ["Pisiform", "Hamate", "Trapezium"], "Scaphoid fracture may endanger its retrograde blood supply."),
        q("Avascular necrosis after scaphoid fracture commonly affects the:", "Proximal fragment", ["Distal fragment", "Pisiform", "Hook of hamate"], "Scaphoid blood supply enters distally and runs proximally."),
        q("Carpal tunnel floor is formed mainly by:", "Carpal bones", ["Flexor retinaculum", "Palmar aponeurosis", "Extensor retinaculum"], "Carpal tunnel is an osseofibrous tunnel with carpal bones as floor/walls."),
        q("The first metacarpal is specialized for:", "Thumb opposition", ["Elbow extension", "Shoulder abduction", "Pronation only"], "First carpometacarpal joint permits opposition and precision grip."),
        q("Epiphyseal line crossing a joint capsule may allow infection to spread to:", "Joint cavity", ["Epidermis only", "Nail bed only", "Thoracic duct"], "Capsular attachments and epiphyseal relationships influence spread of osteomyelitis."),
        q("The hook of hamate gives attachment to:", "Flexor retinaculum", ["Triceps", "Deltoid", "Coracoclavicular ligament"], "Flexor retinaculum attaches to pisiform/hook of hamate medially."),
        q("The capitulum of humerus articulates with:", "Head of radius", ["Trochlear notch of ulna", "Scaphoid", "Glenoid"], "Capitulum is the lateral articular part for radius."),
    ]),
    ("pectoral-region", "Pectoral Region", [
        q("The breast lies mainly in the superficial fascia over:", "Pectoralis major", ["Serratus posterior", "Trapezius", "Infraspinatus"], "The mammary gland is in superficial fascia of pectoral region."),
        q("Most lymph from breast drains first to:", "Axillary lymph nodes", ["Inguinal nodes", "Popliteal nodes", "Preaortic nodes"], "Axillary nodes receive the majority of breast lymph."),
        q("Retraction of nipple in breast carcinoma is due to involvement of:", "Lactiferous ducts/fibrous stroma", ["Pleura", "Humerus", "Brachial plexus roots"], "Tumor fibrosis shortens ducts and suspensory tissues."),
        q("Peau d'orange appearance is due to obstruction of:", "Cutaneous lymphatics", ["Axillary artery", "Cephalic vein only", "Intercostal nerves only"], "Lymphatic obstruction causes skin edema tethered by hair follicles."),
        q("Pectoralis major is primarily supplied by:", "Medial and lateral pectoral nerves", ["Long thoracic nerve", "Thoracodorsal nerve", "Axillary nerve"], "Both pectoral nerves contribute to pectoralis major innervation."),
        q("Pectoralis minor inserts on:", "Coracoid process", ["Acromion", "Lesser tubercle", "Olecranon"], "Pectoralis minor runs from ribs 3-5 to coracoid process."),
        q("Clavipectoral fascia encloses:", "Subclavius and pectoralis minor", ["Deltoid only", "Latissimus dorsi", "Triceps"], "Clavipectoral fascia invests subclavius and pectoralis minor."),
        q("The cephalic vein pierces:", "Clavipectoral fascia", ["Flexor retinaculum", "Interosseous membrane", "Palmar aponeurosis"], "Cephalic vein pierces clavipectoral fascia to drain into axillary vein."),
        q("Serratus anterior is supplied by:", "Long thoracic nerve", ["Thoracodorsal nerve", "Dorsal scapular nerve", "Accessory nerve"], "Long thoracic nerve injury causes winging of scapula."),
        q("Winging of scapula during pushing against wall suggests paralysis of:", "Serratus anterior", ["Pectoralis major", "Biceps", "Supinator"], "Serratus anterior protracts and holds scapula against thoracic wall."),
        q("The mammary gland is a modified:", "Sweat gland", ["Sebaceous gland", "Lymph node", "Endocrine gland"], "Breast is a modified apocrine sweat gland."),
        q("A breast abscess incision is best made:", "Radially", ["Circumferentially across ducts", "Vertically through nipple", "Random zigzag"], "Radial incisions avoid cutting multiple lactiferous ducts."),
        q("The tail of Spence extends toward the:", "Axilla", ["Umbilicus", "Groin", "Neck posterior triangle"], "Axillary tail is clinically important in breast examination."),
        q("The main action of pectoralis major is:", "Adduction and medial rotation of arm", ["Extension of elbow", "Supination", "Wrist flexion only"], "Pectoralis major adducts and medially rotates humerus."),
        q("Interpectoral nodes lie between:", "Pectoralis major and minor", ["Biceps and brachialis", "Radius and ulna", "Trapezius and deltoid"], "Rotter nodes are between the two pectoral muscles."),
    ]),
    ("axilla", "Axilla", [
        q("The apex of axilla communicates with the neck through:", "Cervicoaxillary canal", ["Carpal tunnel", "Cubital tunnel", "Adductor canal"], "The cervicoaxillary canal transmits axillary vessels and brachial plexus."),
        q("The anterior wall of axilla is formed chiefly by:", "Pectoral muscles", ["Scapula only", "Latissimus dorsi only", "Humerus only"], "Pectoralis major/minor and clavipectoral fascia form anterior wall."),
        q("The posterior wall of axilla includes:", "Subscapularis, teres major and latissimus dorsi", ["Pectoralis major only", "Biceps and brachialis", "Flexor retinaculum"], "These muscles form the posterior axillary fold/wall."),
        q("Axillary artery begins as continuation of:", "Subclavian artery", ["Brachial artery", "Radial artery", "Thoracic aorta"], "Subclavian becomes axillary at lateral border of first rib."),
        q("Axillary artery becomes brachial artery at:", "Lower border of teres major", ["Medial epicondyle", "Lateral border of first rib", "Coracoid process"], "At lower border of teres major axillary continues as brachial."),
        q("Axillary artery is divided into three parts by:", "Pectoralis minor", ["Pectoralis major", "Serratus anterior", "Deltoid"], "Pectoralis minor crosses anterior to axillary artery."),
        q("The cords of brachial plexus are named around the:", "Second part of axillary artery", ["Clavicle", "First rib", "Brachial artery in cubital fossa"], "Lateral, medial and posterior cords relate to second part of axillary artery."),
        q("Posterior cord gives rise to:", "Axillary and radial nerves", ["Median nerve only", "Ulnar nerve only", "Long thoracic nerve"], "Terminal branches of posterior cord include axillary and radial nerves."),
        q("Medial cord contributes to:", "Median nerve and ulnar nerve", ["Axillary nerve", "Radial nerve only", "Suprascapular nerve"], "Medial cord gives ulnar nerve and medial root of median nerve."),
        q("Axillary lymph nodes draining upper limb are mainly:", "Lateral group", ["Preaortic group", "Popliteal group", "Deep inguinal group"], "Lateral/humeral nodes drain most of upper limb."),
        q("Central axillary nodes drain into:", "Apical nodes", ["Popliteal nodes", "Para-aortic nodes", "Submental nodes"], "Central nodes pass lymph to apical axillary nodes."),
        q("In axillary dissection, long thoracic nerve injury causes:", "Winging of scapula", ["Wrist drop", "Claw hand", "Ape thumb"], "Long thoracic nerve supplies serratus anterior."),
        q("Thoracodorsal nerve supplies:", "Latissimus dorsi", ["Pectoralis minor", "Deltoid", "Brachialis"], "Thoracodorsal nerve is a posterior cord branch to latissimus dorsi."),
        q("The axillary vein lies generally:", "Medial/anterior to axillary artery", ["Posterior to scapula", "Inside humerus", "In carpal tunnel"], "Axillary vein is medial to artery in axilla."),
        q("The quadrangular space transmits:", "Axillary nerve and posterior circumflex humeral artery", ["Radial nerve and profunda brachii", "Median nerve and brachial artery", "Ulnar nerve"], "These structures pass through quadrangular space to surgical neck area."),
    ]),
    ("back", "Back", [
        q("Trapezius is supplied by:", "Spinal accessory nerve", ["Long thoracic nerve", "Axillary nerve", "Median nerve"], "Motor supply is accessory nerve; proprioception from cervical nerves."),
        q("Trapezius paralysis causes difficulty in:", "Shrugging shoulder", ["Flexing fingers", "Supinating forearm", "Opposing thumb"], "Upper fibers elevate scapula and shoulder."),
        q("Latissimus dorsi is supplied by:", "Thoracodorsal nerve", ["Dorsal scapular nerve", "Axillary nerve", "Ulnar nerve"], "Thoracodorsal nerve supplies latissimus dorsi."),
        q("Latissimus dorsi acts on humerus to:", "Extend, adduct and medially rotate", ["Abduct only", "Laterally rotate only", "Flex elbow"], "It is a powerful extensor/adductor/medial rotator."),
        q("The triangle of auscultation is bounded partly by:", "Trapezius and latissimus dorsi", ["Biceps and triceps", "Pectoralis major only", "Pronator teres"], "It is an area with thin musculature on back for lung auscultation."),
        q("Dorsal scapular nerve supplies:", "Rhomboids", ["Serratus anterior", "Deltoid", "Pectoralis major"], "Rhomboids retract scapula and are supplied by dorsal scapular nerve."),
        q("Levator scapulae elevates the:", "Scapula", ["Radius", "Mandible", "Sternum"], "Levator scapulae runs from cervical transverse processes to superior medial scapula."),
        q("The superficial back muscles connecting upper limb to vertebral column are:", "Extrinsic back muscles", ["Intrinsic hand muscles", "Rotator cuff only", "Intercostals"], "Trapezius, latissimus, rhomboids and levator scapulae are extrinsic."),
        q("Rhomboids attach to the:", "Medial border of scapula", ["Lateral epicondyle", "Olecranon", "Carpal tunnel"], "Rhomboids insert along medial border of scapula."),
        q("Weakness of scapular retraction indicates lesion of:", "Dorsal scapular nerve", ["Median nerve", "Radial nerve", "Ulnar nerve"], "Dorsal scapular nerve innervates rhomboids."),
        q("Latissimus dorsi is important in:", "Climbing and crutch walking", ["Blinking", "Chewing", "Knee locking"], "It pulls trunk up toward fixed upper limb."),
        q("The accessory nerve is vulnerable in surgery of:", "Posterior triangle of neck", ["Carpal tunnel", "Cubital fossa", "Palm"], "Accessory nerve crosses posterior triangle superficially."),
        q("The tendon of latissimus dorsi inserts into:", "Floor of intertubercular sulcus", ["Greater tubercle upper facet", "Olecranon", "Coracoid tip"], "Latissimus inserts into floor of bicipital groove."),
        q("Trapezius helps rotate scapula during:", "Overhead abduction", ["Finger flexion", "Pronation", "Wrist adduction"], "Upper and lower trapezius with serratus anterior upwardly rotate scapula."),
        q("Rhomboids rotate scapula so the glenoid cavity faces:", "Downward", ["Upward", "Anteriorly only", "Laterally only"], "Rhomboids retract and downwardly rotate scapula."),
    ]),
    ("scapular-region", "Scapular Region", [
        q("Deltoid is supplied by:", "Axillary nerve", ["Radial nerve", "Median nerve", "Long thoracic nerve"], "Axillary nerve supplies deltoid and teres minor."),
        q("Deltoid initiates arm abduction mainly from:", "15 to 90 degrees", ["0 to 15 degrees", "Above 150 degrees only", "Finger flexion"], "Supraspinatus initiates first 15 degrees; deltoid is chief abductor thereafter."),
        q("Supraspinatus is supplied by:", "Suprascapular nerve", ["Axillary nerve", "Thoracodorsal nerve", "Median nerve"], "Suprascapular nerve supplies supraspinatus and infraspinatus."),
        q("The rotator cuff muscles include all except:", "Teres major", ["Supraspinatus", "Infraspinatus", "Subscapularis"], "Rotator cuff is SITS: supraspinatus, infraspinatus, teres minor, subscapularis."),
        q("Most commonly torn rotator cuff tendon is:", "Supraspinatus", ["Teres major", "Deltoid", "Coracobrachialis"], "Supraspinatus tendon is vulnerable beneath acromion."),
        q("Infraspinatus primarily causes:", "Lateral rotation of arm", ["Medial rotation", "Elbow flexion", "Wrist extension"], "Infraspinatus and teres minor laterally rotate humerus."),
        q("Subscapularis inserts on:", "Lesser tubercle of humerus", ["Greater tubercle", "Olecranon", "Radial tuberosity"], "Subscapularis medially rotates arm and inserts on lesser tubercle."),
        q("Quadrangular space is bounded laterally by:", "Surgical neck of humerus", ["Clavicle", "Radius", "Ulna"], "Surgical neck forms lateral boundary; axillary nerve passes through."),
        q("Triangular interval transmits:", "Radial nerve and profunda brachii artery", ["Axillary nerve", "Median nerve", "Ulnar nerve"], "Radial nerve enters posterior arm through triangular interval."),
        q("Anastomosis around scapula is clinically important in occlusion of:", "Axillary artery", ["Radial artery at wrist", "Femoral artery", "Internal carotid"], "Scapular anastomoses provide collateral circulation."),
        q("Teres minor is supplied by:", "Axillary nerve", ["Lower subscapular nerve", "Dorsal scapular nerve", "Ulnar nerve"], "Axillary nerve supplies deltoid and teres minor."),
        q("Teres major is supplied by:", "Lower subscapular nerve", ["Axillary nerve", "Suprascapular nerve", "Median nerve"], "Teres major is not cuff and is supplied by lower subscapular nerve."),
        q("Deltoid injection is safest in the:", "Middle bulky part away from axillary nerve", ["Quadrangular space directly", "Medial arm", "Cubital fossa"], "Axillary nerve winds around surgical neck deep to deltoid."),
        q("Subacromial bursitis causes painful:", "Abduction arc", ["Finger extension only", "Elbow flexion only", "Forearm pronation only"], "Inflamed subacromial bursa is compressed during abduction."),
        q("Rotator cuff mainly stabilizes:", "Shoulder joint", ["Elbow joint", "Wrist joint", "Interphalangeal joints"], "Cuff muscles hold humeral head in glenoid cavity."),
    ]),
    ("cutaneous-veins-lymph", "Cutaneous Nerves, Superficial Veins and Lymphatic Drainage", [
        q("Lateral cutaneous nerve of forearm is continuation of:", "Musculocutaneous nerve", ["Median nerve", "Ulnar nerve", "Radial nerve"], "Musculocutaneous nerve continues as lateral cutaneous nerve of forearm."),
        q("Medial cutaneous nerve of forearm arises from:", "Medial cord", ["Posterior cord", "Lateral cord", "Dorsal scapular nerve"], "It is a medial cord branch of brachial plexus."),
        q("Cephalic vein ascends on the:", "Lateral side of upper limb", ["Medial side only", "Deep palmar arch", "Axillary floor"], "Cephalic vein runs along lateral forearm/arm and deltopectoral groove."),
        q("Basilic vein ascends on the:", "Medial side of upper limb", ["Lateral side", "Posterior midline only", "Carpal tunnel"], "Basilic vein is medial and joins brachial veins to form axillary vein."),
        q("Median cubital vein is commonly used for:", "Venepuncture", ["Arterial bypass", "Nerve grafting", "Tendon repair"], "It connects cephalic and basilic veins in cubital fossa."),
        q("The median cubital vein is separated from brachial artery by:", "Bicipital aponeurosis", ["Flexor retinaculum", "Palmar aponeurosis", "Interosseous membrane"], "Bicipital aponeurosis protects brachial artery and median nerve."),
        q("Lymph from most upper limb drains first to:", "Lateral axillary nodes", ["Parasternal nodes", "Preaortic nodes", "Inguinal nodes"], "Lateral axillary nodes receive upper limb lymphatics."),
        q("Lymph from medial hand may follow basilic vein to:", "Supratrochlear nodes", ["Popliteal nodes", "Submental nodes", "Bronchopulmonary nodes"], "Some medial superficial lymphatics pass to supratrochlear nodes."),
        q("Dermatome over thumb is mainly:", "C6", ["T1", "T4", "S1"], "Thumb is a classic C6 dermatome area."),
        q("Dermatome over middle finger is mainly:", "C7", ["C5", "T2", "L5"], "Middle finger represents C7."),
        q("Dermatome over little finger is mainly:", "C8", ["C5", "C6", "T6"], "Little finger/medial hand corresponds to C8."),
        q("Loss of sensation over regimental badge area suggests injury to:", "Axillary nerve", ["Median nerve", "Ulnar nerve", "Musculocutaneous nerve"], "Superior lateral cutaneous nerve of arm from axillary nerve supplies badge area."),
        q("Superficial veins of upper limb lie in:", "Superficial fascia", ["Bone marrow", "Synovial cavity", "Deep fascia only"], "Cephalic and basilic veins are in superficial fascia."),
        q("Intercostobrachial nerve supplies skin of:", "Medial upper arm/axilla", ["Thumb pulp", "Dorsum of foot", "Scalp"], "It is lateral cutaneous branch of second intercostal nerve."),
        q("During axillary node clearance, numbness over medial arm may follow injury to:", "Intercostobrachial nerve", ["Radial nerve", "Deep branch of ulnar nerve", "Posterior interosseous nerve"], "Intercostobrachial nerve is vulnerable in axillary surgery."),
    ]),
    ("arm", "Arm", [
        q("Anterior compartment of arm is supplied mainly by:", "Musculocutaneous nerve", ["Radial nerve", "Ulnar nerve", "Axillary nerve"], "Musculocutaneous nerve supplies biceps, brachialis, coracobrachialis."),
        q("Biceps brachii inserts on:", "Radial tuberosity", ["Ulnar tuberosity", "Olecranon", "Medial epicondyle"], "Biceps tendon attaches to radial tuberosity and gives bicipital aponeurosis."),
        q("Biceps is a powerful:", "Supinator of flexed forearm", ["Pronator", "Wrist extensor", "Finger abductor"], "Biceps supinates especially when elbow is flexed."),
        q("Brachialis is supplied by musculocutaneous nerve and often also by:", "Radial nerve", ["Median nerve", "Ulnar nerve", "Axillary nerve"], "Lateral part may receive radial nerve contribution."),
        q("Brachial artery is continuation of:", "Axillary artery", ["Radial artery", "Ulnar artery", "Subclavian vein"], "Axillary artery becomes brachial at lower border of teres major."),
        q("Brachial artery bifurcates into radial and ulnar arteries in:", "Cubital fossa", ["Axilla", "Carpal tunnel", "Quadrangular space"], "It usually divides near neck of radius in cubital fossa."),
        q("Median nerve in arm is related to:", "Brachial artery", ["Profunda brachii only", "Cephalic vein only", "Axillary nerve"], "Median nerve crosses anterior to brachial artery from lateral to medial."),
        q("Ulnar nerve pierces medial intermuscular septum to enter:", "Posterior compartment", ["Carpal tunnel", "Deltopectoral groove", "Axilla apex"], "It passes posteriorly in mid-arm and behind medial epicondyle."),
        q("Posterior compartment of arm is supplied by:", "Radial nerve", ["Median nerve", "Ulnar nerve", "Musculocutaneous nerve"], "Radial nerve supplies triceps and posterior arm."),
        q("Triceps brachii inserts on:", "Olecranon", ["Radial tuberosity", "Coracoid process", "Lesser tubercle"], "Triceps extends elbow and inserts on olecranon."),
        q("Radial nerve runs with profunda brachii artery in:", "Spiral groove", ["Carpal tunnel", "Guyon's canal", "Cubital tunnel"], "Radial nerve and profunda brachii occupy radial groove."),
        q("Wrist drop after midshaft humerus fracture is due to injury of:", "Radial nerve", ["Median nerve", "Ulnar nerve", "Axillary nerve"], "Radial nerve supplies wrist/finger extensors."),
        q("Cubital fossa lateral boundary is:", "Brachioradialis", ["Pronator teres", "Biceps tendon", "Triceps"], "Cubital fossa boundaries: brachioradialis lateral, pronator teres medial."),
        q("Cubital fossa medial boundary is:", "Pronator teres", ["Brachioradialis", "Deltoid", "Supinator"], "Pronator teres forms medial boundary."),
        q("Contents of cubital fossa from lateral to medial include:", "Tendon, artery, nerve", ["Nerve, tendon, artery", "Artery, nerve, tendon", "Vein, bone, lymph"], "Mnemonic TAN: biceps tendon, brachial artery, median nerve."),
    ]),
    ("forearm-and-hand", "Forearm and Hand", [
        q("Most flexor muscles of forearm are supplied by:", "Median nerve", ["Radial nerve", "Axillary nerve", "Musculocutaneous nerve"], "Median nerve supplies most anterior forearm muscles."),
        q("Flexor carpi ulnaris is supplied by:", "Ulnar nerve", ["Median nerve", "Radial nerve", "Axillary nerve"], "FCU and medial half FDP are ulnar nerve supplied."),
        q("Anterior interosseous nerve is a branch of:", "Median nerve", ["Ulnar nerve", "Radial nerve", "Musculocutaneous nerve"], "AIN supplies deep anterior forearm muscles except medial FDP."),
        q("Posterior interosseous nerve is continuation of deep branch of:", "Radial nerve", ["Median nerve", "Ulnar nerve", "Axillary nerve"], "PIN supplies most extensor compartment muscles."),
        q("Carpal tunnel transmits:", "Median nerve and flexor tendons", ["Ulnar nerve and artery", "Radial artery only", "Extensor tendons"], "Median nerve with FDS, FDP, FPL tendons pass through carpal tunnel."),
        q("Guyon's canal transmits:", "Ulnar nerve and artery", ["Median nerve", "Radial nerve", "Brachial artery"], "Ulnar neurovascular bundle enters hand superficial to flexor retinaculum."),
        q("Thenar muscles are supplied mainly by:", "Recurrent branch of median nerve", ["Deep ulnar nerve", "Radial nerve", "Axillary nerve"], "LOAF muscles are median supplied."),
        q("Adductor pollicis is supplied by:", "Deep branch of ulnar nerve", ["Median recurrent branch", "Radial nerve", "AIN"], "Adductor pollicis is ulnar nerve supplied."),
        q("Lumbricals 1 and 2 are supplied by:", "Median nerve", ["Ulnar nerve", "Radial nerve", "Musculocutaneous nerve"], "Lateral two lumbricals are median; medial two are ulnar."),
        q("Lumbricals 3 and 4 are supplied by:", "Ulnar nerve", ["Median nerve", "Radial nerve", "AIN"], "Medial lumbricals are deep ulnar nerve supplied."),
        q("Superficial palmar arch is formed mainly by:", "Ulnar artery", ["Radial artery", "Brachial artery", "Anterior interosseous artery"], "Ulnar artery predominates in superficial palmar arch."),
        q("Deep palmar arch is formed mainly by:", "Radial artery", ["Ulnar artery", "Median artery", "Cephalic vein"], "Radial artery predominates in deep palmar arch."),
        q("Anatomical snuffbox floor includes:", "Scaphoid and trapezium", ["Pisiform and hamate", "Capitate only", "Olecranon"], "Scaphoid tenderness in snuffbox suggests fracture."),
        q("Ulnar nerve lesion at wrist causes:", "Clawing of ring and little fingers", ["Wrist drop", "Ape thumb only", "Deltoid paralysis"], "Ulnar intrinsic hand paralysis causes claw hand."),
        q("Median nerve lesion in carpal tunnel causes weakness of:", "Thumb opposition", ["Elbow extension", "Shoulder abduction", "Forearm supination only"], "Recurrent median branch supplies opponens pollicis."),
    ]),
    ("joints-upper-limb", "Joints of Upper Limb", [
        q("Shoulder joint is a:", "Ball-and-socket synovial joint", ["Hinge joint", "Pivot joint", "Fibrous joint"], "Glenohumeral joint permits multiaxial movement."),
        q("The shoulder joint is most commonly dislocated:", "Inferiorly/anteriorly", ["Superiorly", "Posteriorly only", "Medially into thorax"], "Weak inferior capsule predisposes anterior-inferior dislocation."),
        q("Nerve endangered in shoulder dislocation is:", "Axillary nerve", ["Median nerve", "Ulnar nerve", "Long thoracic nerve"], "Axillary nerve winds around surgical neck below shoulder joint."),
        q("The glenoid labrum functions to:", "Deepen glenoid cavity", ["Form synovial fluid only", "Close axillary artery", "Attach biceps to radius"], "Labrum increases stability of shallow glenoid."),
        q("Elbow joint is primarily a:", "Hinge joint", ["Ball-and-socket joint", "Saddle joint", "Plane joint only"], "Elbow permits flexion-extension."),
        q("Carrying angle is normally more prominent in:", "Females", ["Males only", "Newborns only", "No one"], "Carrying angle is usually greater in females."),
        q("Pulled elbow in children involves subluxation of:", "Head of radius from annular ligament", ["Ulna from trochlea", "Scaphoid", "Clavicle"], "Traction can pull radial head partly out of annular ligament."),
        q("Proximal radioulnar joint is a:", "Pivot joint", ["Hinge joint", "Saddle joint", "Symphysis"], "It permits rotation of radial head within annular ligament."),
        q("Wrist joint is formed proximally by:", "Distal radius and articular disc", ["Distal ulna directly", "Metacarpals", "All carpal bones"], "Ulna is separated from wrist joint by articular disc."),
        q("The first carpometacarpal joint is:", "Saddle joint", ["Hinge joint", "Pivot joint", "Suture"], "Thumb CMC saddle joint permits opposition."),
        q("Sternoclavicular joint is functionally important because it:", "Allows movements of pectoral girdle", ["Locks shoulder permanently", "Forms elbow", "Prevents scapular rotation"], "It is the only bony link of upper limb with axial skeleton."),
        q("Acromioclavicular joint injuries commonly affect:", "Coracoclavicular ligament support", ["Median nerve", "Carpal tunnel", "Annular ligament only"], "CC ligaments provide major vertical stability."),
        q("The rotator cuff blends with capsule of:", "Shoulder joint", ["Elbow joint", "Wrist joint", "Sternoclavicular joint"], "Cuff tendons reinforce glenohumeral capsule."),
        q("Elbow aspiration is safest posterolaterally because it avoids:", "Median nerve and brachial artery anteriorly", ["Scapular spine", "Cephalic vein in hand", "Thoracic duct"], "Anterior cubital contents should be avoided."),
        q("Colles fracture classically produces:", "Dinner-fork deformity", ["Winging scapula", "Ape hand", "Claw toes"], "Distal radius fracture with dorsal displacement causes dinner-fork deformity."),
    ]),
    ("surface-radiological-comparison", "Surface Marking, Radiological Anatomy and Comparison of Upper and Lower Limbs", [
        q("Brachial artery pulse is palpated medial to:", "Biceps tendon in cubital fossa", ["Triceps tendon", "Ulnar styloid", "Acromion"], "Brachial artery lies medial to biceps tendon in cubital fossa."),
        q("Radial pulse is palpated lateral to:", "Flexor carpi radialis tendon", ["Flexor carpi ulnaris", "Palmaris longus", "Biceps tendon"], "Radial artery lies lateral to FCR tendon at wrist."),
        q("Ulnar artery at wrist lies lateral to:", "Flexor carpi ulnaris tendon", ["Extensor pollicis longus", "Brachioradialis", "Biceps tendon"], "Ulnar artery is just lateral to FCU with ulnar nerve medial."),
        q("Median nerve surface marking at wrist is between:", "Palmaris longus and flexor carpi radialis", ["FCU and pisiform", "EPL and EPB", "Biceps and triceps"], "Median nerve enters carpal tunnel deep to flexor retinaculum."),
        q("Ulnar nerve at wrist lies:", "Lateral to pisiform", ["Inside anatomical snuffbox", "Behind lateral epicondyle", "At deltoid insertion"], "Ulnar nerve enters Guyon's canal lateral to pisiform."),
        q("Cephalic vein is visible in:", "Deltopectoral groove", ["Cubital tunnel only", "Carpal tunnel", "Axillary posterior wall"], "Cephalic vein ascends in deltopectoral groove."),
        q("On AP shoulder X-ray, dislocation assessment focuses on relation of humeral head to:", "Glenoid cavity", ["Olecranon fossa", "Carpal tunnel", "Radial styloid"], "Shoulder radiology requires humeral head-glenoid alignment."),
        q("Scaphoid fracture is suspected radiologically after tenderness in:", "Anatomical snuffbox", ["Cubital fossa", "Axilla", "Deltoid tuberosity"], "Snuffbox tenderness prompts scaphoid views."),
        q("Compared with lower limb, upper limb has:", "Greater mobility and less weight-bearing function", ["Less mobility and more weight-bearing", "No homologous bones", "No plexus"], "Upper limb is designed for manipulation, lower for support/locomotion."),
        q("Humerus corresponds developmentally to:", "Femur", ["Tibia", "Fibula", "Talus"], "Arm bone humerus is homologous to thigh bone femur."),
        q("Radius corresponds to:", "Tibia", ["Fibula", "Femur", "Calcaneus"], "Preaxial bone radius corresponds to tibia."),
        q("Ulna corresponds to:", "Fibula", ["Tibia", "Femur", "Patella"], "Postaxial ulna corresponds to fibula."),
        q("Flexor retinaculum surface marking is relevant to:", "Carpal tunnel syndrome", ["Shoulder dislocation", "Breast abscess", "Thoracic outlet only"], "Median nerve compression occurs beneath flexor retinaculum."),
        q("The axillary nerve is surface-related to:", "Surgical neck of humerus", ["Medial epicondyle", "Radial styloid", "Pisiform"], "Axillary nerve winds posteriorly around surgical neck."),
        q("Radiological anatomy of upper limb is essential first to identify:", "Side, view and normal alignment", ["Only patient name", "Only film color", "Only skin thickness"], "Correct X-ray interpretation starts with orientation and joint alignment."),
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
                "id": f"anatomy-upper-limb-{slug}-{question_index:02d}",
                "topic": topic,
                "difficulty": "moderate" if question_index <= 5 else "high" if question_index <= 12 else "very high",
                "prompt": row["prompt"],
                "options": options,
                "answerIndex": answer_index,
                "answer": row["answer"],
                "explanation": row["explanation"],
            })
    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "anatomy" and x.get("chapterTitle") == CHAPTER)] + questions
    if len(TOPICS) != 11 or len(questions) != 165:
        raise AssertionError(f"Expected 11 topics and 165 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 165:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
