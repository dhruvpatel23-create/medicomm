from .common import q

CHAPTERS = [
    # Chapter 9: Fractures in Children (HARD - 10 questions)
    (9, "Fractures in Children", "hard", [
        q(
            "An 8-year-old girl falls from a swing onto her outstretched hand. Radiographs of the distal radius reveal a fracture line passing across the growth plate and traversing vertically through the epiphysis into the articular joint space. According to the Salter-Harris classification, this is classified as",
            "Salter-Harris Type III",
            ["Salter-Harris Type II", "Salter-Harris Type IV", "Salter-Harris Type I"],
            "Salter-Harris Type III is an intra-articular physeal injury where the fracture runs along the physis and exits through the epiphysis into the joint. Type I is a pure transverse separation through the physis. Type II passes through the physis and exits through the metaphysis (creating a triangular Thurston-Holland sign). Type IV crosses through the metaphysis, physis, and epiphysis in continuity.",
            clinical=True
        ),
        q(
            "Which Salter-Harris physeal injury pattern is statistically the most common, accounting for approximately 75% of all growth plate fractures?",
            "Salter-Harris Type II (physis fracture with metaphyseal Thurston-Holland fragment)",
            ["Salter-Harris Type I (pure cleavage separation through hypertrophic zone)", "Salter-Harris Type III (intra-articular fracture traversing physis and epiphysis)", "Salter-Harris Type V (crush injury of physeal germinal cells)"],
            "Salter-Harris Type II is by far the most frequent physeal fracture (~75%). The shear force cleaves the weak hypertrophic zone of the physis and directs obliquely into the metaphysis, producing a characteristic triangular metaphyseal fragment known as the Thurston-Holland sign. The periosteal hinge remains intact on the metaphyseal side, facilitating stable closed reduction.",
            clinical=False
        ),
        q(
            "A 9-year-old boy sustains a displaced Salter-Harris Type IV fracture of the distal femoral physis. What surgical principle is essential to prevent progressive angular deformity, bone bridging (physeal bar), and leg-length discrepancy?",
            "Anatomical open reduction and internal fixation with smooth wires placed parallel to the physis",
            ["Closed reduction and loose circular casting allowing minor displacement", "Prolonged skeletal traction for 8 weeks until bridging callus forms", "Immediate open resection of the entire growth plate with early arthrodesis"],
            "Salter-Harris Type IV is an intra-articular fracture crossing metaphysis, physis, and epiphysis. If reduced with any step-off or gap, endochondral ossification forms an osseous bridge across the physis (physeal bar), resulting in asymmetric tethering, severe angular deformity, and limb shortening. Anatomic reduction and stabilization using smooth K-wires (or screws placed strictly within the epiphysis and metaphysis without traversing the physis) are mandatory.",
            clinical=True
        ),
        q(
            "Why do incomplete greenstick fractures occur almost exclusively in growing children rather than in mature adult bone?",
            "Thick vascular periosteum combined with elastic, porous, compliant cortical bone",
            ["Higher concentration of insoluble crystalline hydroxyapatite in pediatric bone", "Continuous plastic deformation occurring under low torsional forces in adult bone", "Complete absence of Haversian canals in immature pediatric skeletons"],
            "Greenstick fractures reflect the unique biomechanical properties of immature pediatric bone: the bone has high water and collagen content, lower mineral density, and greater elasticity. Under bending forces, the bone behaves like a green twig—the cortex on the convex (tension) side breaks while the cortex on the concave (compression) side buckles without complete fracture, held securely by a thick, tough periosteal sleeve.",
            clinical=False
        ),
        q(
            "When evaluating the spontaneous remodeling potential of malunited pediatric long-bone fractures, which deformity has the LEAST capacity for spontaneous correction by skeletal growth?",
            "Rotational deformity (torsional malalignment)",
            ["Angular deformity in the plane of adjacent hinge joint movement", "Metaphyseal angular deformity near an active growth plate", "Appositional bayonet displacement with mild shortening in a child under 8 years"],
            "Pediatric bone remodels based on the Heuter-Volkmann law and Wolff's law. Remodeling is greatest for: 1. Younger children with significant remaining growth; 2. Fractures near an active growth plate (metaphyseal); 3. Angular deformities in the plane of joint motion (flexion-extension). In contrast, rotational (torsional) deformities do NOT correct spontaneously with growth and persist into adult life unless surgically realigned.",
            clinical=False
        ),
        q(
            "A 5-year-old girl sustains a closed midshaft femoral fracture. The surgeon deliberately accepts 1.0 to 1.5 cm of bayonet appositional shortening during closed reduction and spica casting. What physiological phenomenon justifies this decision?",
            "Post-traumatic hyperemic overgrowth of the fractured femur over the next 1 to 2 years",
            ["Spontaneous elastic recoil of the iliotibial band pulling bone fragments apart", "Rapid chondrolysis of the contralateral femoral physis equalizing limb length", "Permanent arrest of distal femoral physeal growth on the injured side"],
            "In children aged 2 to 10 years, femoral fractures stimulate increased regional vascularity and hyperemia during fracture healing, accelerating physeal growth plates. This causes 1 to 2 cm of longitudinal overgrowth of the injured femur over the next 18 to 24 months. Therefore, an initial 1 cm of bayonet apposition and shortening is desirable to prevent long-term limb length inequality (overlengthening).",
            clinical=True
        ),
        q(
            "A 7-month-old infant is brought to the emergency department with unexplained swelling and irritability. Skeletal survey reveals multiple fractures at varying stages of healing, including metaphyseal bucket-handle avulsions and posterior rib fractures near the costovertebral junctions. What condition must be suspected?",
            "Non-accidental injury (Battered baby syndrome / physical abuse)",
            ["Severe nutritional rickets", "Osteogenesis imperfecta Type I", "Congenital syphilis (Wimberger sign)"],
            "The radiological constellation of fractures of different healing ages, metaphyseal corner/bucket-handle fractures (caused by violent twisting or shaking), posterior rib fractures (caused by thoracic squeezing), and spinous process fractures is pathognomonic for non-accidental injury (battered baby syndrome / physical abuse). It demands immediate hospitalization, child protection notification, and a full multidisciplinary forensic evaluation.",
            clinical=True
        ),
        q(
            "What is the mechanical mechanism of a pediatric torus (buckle) fracture commonly seen in the distal radius?",
            "Axial compressive loading causing impaction and wrinkling of the porous metaphyseal cortex",
            ["High-velocity torsional stress causing longitudinal cleavage of the diaphysis", "Direct transverse shear force slicing through the epiphysis", "Avulsion of the periosteal cuff by sudden extensor tendon contraction"],
            "A torus or buckle fracture is a classic pediatric compressive injury. Axial load (e.g., fall on an outstretched hand) compresses the porous, compliant trabecular bone of the distal radial metaphysis, producing acute buckling or bulging of the cortex. There is no true cortical disruption, no displacement, and it heals reliably within 3 weeks in a simple splint or cast.",
            clinical=False
        ),
        q(
            "A 6-year-old boy presents with a malunited supracondylar fracture of the humerus resulting in a severe gunstock deformity (cubitus varus). What is the primary anatomical component of the malunion responsible for this deformity?",
            "Medial tilting (coronal collapse) and internal rotation of the distal fragment",
            ["Complete premature growth arrest of the lateral condylar physis", "Avascular necrosis of the trochlea and capitulum", "Lateral translocation of the olecranon process"],
            "Cubitus varus ('gunstock deformity') following supracondylar fractures is caused by mechanical malunion of the distal fragment, specifically medial tilt, medial translation, and internal rotation. Contrary to historical belief, it is NOT due to asymmetric physeal growth arrest. The distal humeral physis contributes only 15-20% to humerus growth and does not correct the coronal plane malunion.",
            clinical=True
        ),
        q(
            "In Slipped Capital Femoral Epiphysis (SCFE), through which specific histological zone of the proximal femoral physis does mechanical displacement characteristically occur?",
            "Zone of hypertrophy (maturation and provisional calcification)",
            ["Zone of resting germinal chondrocytes", "Zone of active chondrocyte proliferation", "Zone of primary bone deposition in the metaphysis"],
            "In SCFE, the mechanical shearing separation occurs precisely through the zone of hypertrophy (specifically the cell hypertrophy and provisional calcification layers) of the growth plate. This zone has the lowest matrix-to-cell ratio and lacks structural collagen cross-linking, making it vulnerable to shear stresses during the adolescent growth spurt under hormonal influences.",
            clinical=False
        ),
    ]),

    # Chapter 10: Peripheral Nerve Injuries (HARD - 10 questions)
    (10, "Peripheral Nerve Injuries", "hard", [
        q(
            "A 32-year-old man awakens after a deep sleep with his right upper arm draped over a hard chair. On examination, he has complete wrist drop and finger drop, loss of sensation over the first dorsal web space, but normal triceps strength and an intact triceps jerk. What is the diagnosis and site of compression?",
            "Saturday night palsy; compression of radial nerve in the spiral groove",
            ["Crutch palsy; compression of radial nerve high in the axilla", "Posterior interosseous nerve syndrome; entrapment at the Arcade of Frohse", "Pronator teres syndrome; median nerve compression in the forearm"],
            "Saturday night palsy is a compression injury of the radial nerve in the spiral (radial) groove of the mid-shaft humerus. Because the motor branches to the triceps and anconeus arise proximal to the spiral groove (in the axilla), triceps power and elbow extension are fully preserved, but all wrist and finger extensors innervated distally (BR, ECRL, ECRB, EDC, ECU, EPL, etc.) are paralyzed, accompanied by numbness over the first dorsal web space.",
            clinical=True
        ),
        q(
            "According to the nerve injury classifications of Seddon and Sunderland, which grade represents complete anatomical transection of the nerve trunk (axon, endoneurium, perineurium, and epineurium)?",
            "Neurotmesis (Sunderland Grade V)",
            ["Neuropraxia (Sunderland Grade I)", "Axonotmesis (Sunderland Grade II)", "Perineurial disruption (Sunderland Grade III)"],
            "Seddon's Neurotmesis corresponds to Sunderland Grade V: the nerve trunk is completely divided, with disruption of axons, endoneurial tubes, perineurium, and the external epineurium. Complete Wallerian degeneration occurs, and spontaneous recovery is impossible. Accurate surgical realignment and microscopic end-to-end neurorrhaphy (or nerve grafting) are obligatory.",
            clinical=False
        ),
        q(
            "A 28-year-old kitchen worker suffers a deep glass laceration on the volar wrist proximal to the flexor retinaculum. Examination reveals loss of finger abduction/adduction, a positive Froment's sign, and sensory loss over the hypothenar eminence and little finger. Which nerve is severed?",
            "Ulnar nerve (low ulnar nerve injury at the wrist)",
            ["High radial nerve in the spiral groove", "Median nerve at the pronator canal", "Anterior interosseous nerve at the fibrous arch of FDS"],
            "This presentation reflects low ulnar nerve palsy at the wrist: denervation of intrinsic hand muscles (interossei, medial two lumbricals, hypothenar muscles, and adductor pollicis). Loss of adductor pollicis causes a positive Froment's sign (patient flexes thumb IP joint via FPL, innervated by AIN, to hold paper). Sensation over the hypothenar area and little finger is lost.",
            clinical=True
        ),
        q(
            "What physiological phenomenon underlies Tinel's sign in a regenerating peripheral nerve, and at what approximate rate does axonal regeneration advance?",
            "Percussion over regenerating unmyelinated axonal sprouts elicits paresthesias; advances at ~1 mm/day",
            ["Electrical discharge from demyelinated Schwann cells; advances at 5 mm/day", "Microvascular spasms within the endoneurium; advances at 3 cm/week", "Retrograde motor unit firing; advances at 10 mm/day"],
            "Tinel's sign is elicited by gently tapping along the path of a damaged nerve from distal to proximal. When the percussion reaches the tips of regenerating, unmyelinated axonal sprouts (growth cones), tingling sensations (paresthesias) shoot into the cutaneous distribution of the nerve. A progressive distally advancing Tinel's sign indicates active axonal regeneration, which occurs at the rate of ~1 mm/day (or 1 mm per 24 hours, ~1 inch per month).",
            clinical=False
        ),
        q(
            "A patient sustains a high median nerve transection at the elbow. When asked to make a tight fist, the index and middle fingers remain extended while the ring and little fingers flex into the palm. What is this clinical posture termed?",
            "Benediction sign (Hand of Benediction)",
            ["Claw hand deformity", "Ape thumb deformity", "Volkmann's ischemic contracture"],
            "In high median nerve palsy, the patient cannot flex the thumb, index, or middle fingers when attempting to make a fist because of paralysis of the FPL, FDS, and the radial half of FDP (innervating digits 2 and 3). The ring and little fingers flex normally because the ulnar half of FDP is innervated by the intact ulnar nerve. This resulting posture resembles a priest giving a papal blessing ('Benediction sign' or 'pointing sign').",
            clinical=True
        ),
        q(
            "What is the anatomical basis for the Ulnar Paradox in peripheral nerve injuries?",
            "Clawing of ring and little fingers is more severe in low ulnar nerve palsy than in high ulnar nerve palsy",
            ["Sensory loss is greater in high lesions, but motor loss is restricted to low lesions", "The nerve regenerates twice as fast following high lesions compared to low lesions", "Intrinsic muscles are paralyzed in high lesions but completely spared in low lesions"],
            "The Ulnar Paradox states: 'the higher the lesion, the less severe the clawing.' In a low ulnar lesion (at the wrist), the intrinsic muscles (interossei, lumbricals 3 and 4) are paralyzed, but the extrinsic muscle Flexor Digitorum Profundus (FDP) to digits 4 and 5 is intact; active FDP flexion unopposed by lumbricals produces severe clawing. In a high ulnar lesion (above elbow), FDP to digits 4 and 5 is also paralyzed, removing the primary flexor force at the IP joints, resulting in markedly less conspicuous clawing.",
            clinical=False
        ),
        q(
            "A 25-year-old motorcyclist sustains a fracture of the neck of the fibula. On examination, he is unable to dorsiflex or evert his foot, walks with a steppage gait, and has numbness over the anterolateral leg and dorsum of the foot. Which nerve is injured?",
            "Common peroneal nerve (lateral popliteal nerve)",
            ["Tibial nerve in the popliteal fossa", "Saphenous nerve at the adductor canal", "Deep femoral nerve in the obturator groove"],
            "The common peroneal nerve winds tightly around the neck of the fibula in a subcutaneous, vulnerable position where it can be crushed by direct blows or fibular neck fractures. Division causes loss of both deep peroneal (foot and toe dorsiflexors) and superficial peroneal (peroneus longus and brevis evertors) branches, causing classic foot drop, loss of eversion, equinovarus attitude during swing phase (steppage gait), and sensory loss over the dorsum of the foot.",
            clinical=True
        ),
        q(
            "How does clinical examination reliably differentiate Pronator Teres Syndrome from Carpal Tunnel Syndrome?",
            "Sensation over the thenar eminence is preserved in Carpal Tunnel Syndrome but diminished in Pronator Teres Syndrome",
            ["Phalen's maneuver is positive in Pronator Teres Syndrome but negative in Carpal Tunnel Syndrome", "Abductor pollicis brevis power is completely normal in Carpal Tunnel Syndrome", "Nocturnal paresthesias are exclusively present in Pronator Teres Syndrome"],
            "The palmar cutaneous branch of the median nerve arises approximately 5 to 6 cm proximal to the wrist and travels superficial to the flexor retinaculum into the palm. Therefore, in Carpal Tunnel Syndrome (compression inside the carpal tunnel under the retinaculum), sensation over the base of the thenar eminence is characteristically spared. In contrast, in proximal median nerve entrapment (Pronator Teres Syndrome), the palmar cutaneous branch is compressed, resulting in sensory loss over the thenar eminence.",
            clinical=False
        ),
        q(
            "A patient with an open infected midshaft humeral fracture sustains an irreparable 8-cm gap in the radial nerve. One year later, with all extensor muscles completely denervated, what is the classic tendon transfer of choice to restore wrist extension?",
            "Transfer of Pronator Teres (PT) to Extensor Carpi Radialis Brevis (ECRB)",
            ["Transfer of Flexor Carpi Ulnaris (FCU) to Biceps brachii", "Transfer of Brachioradialis to Flexor Digitorum Profundus", "Transfer of Palmaris longus directly to Triceps tendon"],
            "For permanent, irreparable radial nerve palsy, standard tendon transfer (the Robert Jones or modified transfer) restores function: 1. Pronator Teres (PT) transferred to Extensor Carpi Radialis Brevis (ECRB) to restore wrist extension; 2. Flexor Carpi Radialis (FCR) or Flexor Carpi Ulnaris (FCU) transferred to Extensor Digitorum Communis (EDC) to restore finger extension; 3. Palmaris Longus (PL) transferred to Extensor Pollicis Longus (EPL) to restore thumb extension.",
            clinical=True
        ),
        q(
            "In electrodiagnostic testing following acute peripheral nerve transection, how many days after injury do denervation changes (fibrillations and positive sharp waves) first appear on needle EMG?",
            "14 to 21 days (2 to 3 weeks) post-injury",
            ["Within 2 to 4 hours post-injury", "At 48 to 72 hours post-injury", "Only after 6 to 9 months post-injury"],
            "Following complete nerve division, distal axons conduct normally for up to 48-72 hours. Wallerian degeneration then begins and takes 2 to 3 weeks (14-21 days) to complete down the entire length of the distal nerve segment. Spontaneous denervation potentials (fibrillations and positive sharp waves) indicating loss of neural control over muscle membrane potentials appear on EMG only after Wallerian degeneration reaches the motor endplate, usually at 2-3 weeks.",
            clinical=False
        ),
    ]),

    # Chapter 11: Deformities and Their Management (Easy - 5 questions)
    (11, "Deformities and Their Management", "easy", [
        q(
            "A 6-year-old child presents with knock-knees. On examination with medial femoral condyles in contact, the intermalleolar distance (IMD) measures 9 cm. Beyond what threshold is genu valgum considered pathological in a child older than 7 years?",
            "Intermalleolar distance greater than 8 cm",
            ["Intermalleolar distance greater than 2 cm", "Intercondylar distance greater than 5 cm", "Any degree of knee valgus at any age"],
            "Physiological genu valgum is normal between ages 3 and 6 years, with spontaneous resolution expected by age 7 (normal adult valgus is 5-7 degrees). An intermalleolar distance (IMD) exceeding 8 cm in a child older than 7 years, or unilateral/progressive valgus, is considered pathological and requires workup (rickets, trauma, skeletal dysplasia) and possible surgical correction.",
            clinical=True
        ),
        q(
            "A 10-year-old child with post-traumatic cubitus varus following a malunited supracondylar fracture is scheduled for corrective osteotomy. Which procedure is the classic standard technique described by French?",
            "Lateral closing-wedge osteotomy of the distal humerus",
            ["Medial opening-wedge distraction osteotomy with fibular graft", "Dome-shaped derotation osteotomy of the radial neck", "Resection of the lateral epicondyle with annular ligament release"],
            "The classic French osteotomy for cubitus varus is a lateral closing-wedge osteotomy of the supracondylar distal humerus. The medial cortical hinge is preserved, a predetermined triangular wedge of bone is excised from the lateral cortex, the osteotomy is closed to restore the carrying angle, and stability is maintained using crossed screws or K-wires.",
            clinical=False
        ),
        q(
            "What is the primary mechanical advantage of an opening-wedge osteotomy compared to a closing-wedge osteotomy?",
            "Opening-wedge preserves or gains bone length, whereas closing-wedge causes limb shortening",
            ["Opening-wedge eliminates any need for bone grafting or plate fixation", "Opening-wedge permits immediate full weight-bearing without hardware", "Opening-wedge never places tension on adjacent neurovascular structures"],
            "An opening-wedge osteotomy corrects angular deformity while increasing overall bone length (beneficial when the injured limb is already short), but creates a structural gap requiring autologous/allograft bone grafting and rigid plate fixation. In contrast, a closing-wedge osteotomy achieves direct bone-on-bone contact with faster union, but inherently shortens the limb.",
            clinical=False
        ),
        q(
            "What fundamental clinical feature distinguishes a structural deformity from a postural (functional) deformity?",
            "A structural deformity is fixed by permanent tissue contractures; a postural deformity is passively fully correctable",
            ["A structural deformity always involves a fracture; a postural deformity is confined to skin", "A structural deformity occurs only in geriatrics; a postural deformity occurs only in neonates", "A structural deformity has absent reflexes; a postural deformity has brisk reflexes"],
            "A postural (functional or dynamic) deformity is caused by habitual posture or muscle imbalance; there are no permanent contractures, and the deformity can be actively or passively corrected completely to neutral. A structural (fixed) deformity is associated with permanent morphological changes in bones, joints, ligaments, or contracted capsules, and cannot be corrected to neutral by passive manipulation.",
            clinical=False
        ),
        q(
            "A 12-year-old boy with severe idiopathic genu valgum of 18 degrees has open physes. What minimally invasive guided growth procedure is indicated to correct this deformity without performing an osteotomy?",
            "Temporary medial hemiepiphysiodesis using extra-periosteal tension-band plates (8-plates)",
            ["Complete bilateral open epiphyseodesis of both femoral and tibial physes", "High tibial closing-wedge osteotomy with a T-plate", "Immediate Ilizarov ring frame application with acute 20-degree valgus correction"],
            "Temporary hemiepiphysiodesis (guided growth) using extra-periosteal non-locking tension-band plates ('8-plates' and cannulated screws) straddling the medial aspect of the physis inhibits growth on the medial side while allowing continued growth on the lateral side. As the child grows, the valgus deformity progressively straightens. Once corrected, the implant is removed, allowing normal symmetrical physeal growth.",
            clinical=True
        ),
    ]),

    # Chapter 12: Treatment of Orthopaedic Disorders: A General Review (Easy - 5 questions)
    (2, "Treatment of Orthopaedic Disorders: A General Review", "easy", [
        q(
            "A 56-year-old patient with long-standing diabetic neuropathy presents with a painless, swollen, completely destroyed, and flail Charcot ankle joint. Which operative procedure is indicated to provide a stable, painless, weight-bearing extremity?",
            "Arthrodesis (surgical joint fusion)",
            ["Excision arthroplasty (Girdlestone procedure)", "High-flexion total ankle replacement", "Continuous passive motion and early weight-bearing"],
            "Charcot neuroarthropathy results in progressive joint destruction, ligamentous laxity, fragmentation, and instability due to loss of protective pain and proprioceptive sensation. Total joint replacement is contraindicated because lack of proprioception causes catastrophic early loosening. Arthrodesis (joint fusion) using rigid internal/external fixation is the surgical procedure of choice to establish a stable, plantigrade, non-ulcerating foot.",
            clinical=True
        ),
        q(
            "What is the optimal functional position for arthrodesis (fusion) of the hip joint in an adult manual laborer?",
            "20 to 25 degrees of flexion, 0 to 5 degrees of abduction, and neutral rotation",
            ["45 degrees of flexion, 15 degrees of adduction, and 15 degrees of internal rotation", "Complete neutral extension (0 degrees), 20 degrees of external rotation, and 10 degrees of adduction", "90 degrees of flexion and 30 degrees of abduction to allow comfortable sitting"],
            "The ideal position for arthrodesis of the hip joint is 20 to 25 degrees of flexion, neutral to 5 degrees of abduction (prevents pelvic tilt), and neutral rotation. This allows the patient to walk with an acceptable gait without excessive lordosis, sit comfortably without excessive pelvic tilt, and stand upright with minimum compensatory spinal strain.",
            clinical=False
        ),
        q(
            "What is the optimal functional position for arthrodesis of the adult wrist joint to preserve maximal grasp power?",
            "20 to 25 degrees of dorsiflexion (extension) with 5 degrees of ulnar deviation",
            ["30 degrees of palmar flexion with 15 degrees of radial deviation", "Complete neutral position (0 degrees flexion/extension) with maximal pronation", "45 degrees of dorsiflexion with 20 degrees of radial deviation"],
            "The optimal position for wrist arthrodesis is 20 to 25 degrees of dorsiflexion (extension) and slight ulnar deviation (5 degrees). This position mimics the natural posture of the wrist during powerful power-grip activities, optimizing length-tension relationships for the long digital flexor tendons.",
            clinical=False
        ),
        q(
            "What is the surgical definition of an excision arthroplasty (such as the Girdlestone procedure for the hip joint)?",
            "Resection of diseased articular bone ends, allowing fibrous tissue to form a mobile pseudoarthrosis",
            ["Interposition of a biological fascia lata graft without removing any bone ends", "Permanent metallic prosthetic replacement of the acetabulum and femoral head", "Rigid intra-articular screw compression to fuse opposing bone surfaces"],
            "Excision arthroplasty involves complete surgical removal of the articulating bone ends (e.g., Girdlestone resection arthroplasty of the hip involves excision of the femoral head and neck). The resulting dead space fills with fibrous scar tissue, creating a mobile pseudoarthrosis that eliminates pain (e.g., in refractory septic arthritis or failed total hip replacement) at the expense of limb shortening and instability.",
            clinical=False
        ),
        q(
            "Following arthroscopic lysis of knee adhesions or ACL reconstruction, what is the primary biological benefit of a Continuous Passive Motion (CPM) machine?",
            "Prevents intra-articular adhesions and enhances synovial fluid nutrition to cartilage",
            ["Accelerates primary direct cortical bone healing at graft fixation tunnels", "Stimulates systemic osteoblast differentiation via piezoelectric fields", "Eliminates the physiological requirement for postoperative analgesia"],
            "Continuous Passive Motion (CPM), introduced by Robert Salter, moves the joint passively through a controlled range of motion without active muscle contraction. This continuous movement promotes synovial fluid circulation, provides metabolic nutrition to healing articular cartilage, minimizes intra-articular adhesion and scar formation, and accelerates clearance of hemarthrosis and periarticular edema.",
            clinical=True
        ),
    ]),

    # Chapter 13: Injuries Around the Shoulder, Fracture Humerus (HARD - 10 questions)
    (13, "Injuries Around the Shoulder, Fracture Humerus", "hard", [
        q(
            "A 24-year-old rugby player falls onto his abducted, externally rotated right arm. On examination, the normal rounded contour of the right deltoid is flattened, the acromion is prominent with a subacromial hollow, the elbow is held in slight abduction, and the patient cannot touch his opposite shoulder with the affected hand (positive Dugas test). What is the diagnosis?",
            "Anterior dislocation of the shoulder joint (subcoracoid type)",
            ["Posterior dislocation of the shoulder joint", "Acromioclavicular joint disruption Grade III", "Fracture of the anatomical neck of the humerus"],
            "This is the classic presentation of an acute anterior dislocation of the shoulder (most commonly subcoracoid): flattening of the deltoid, prominent acromion, subacromial hollow, arm held in slight abduction and external rotation, and inability to adduct the arm to bring the hand to the opposite shoulder (Dugas test / Hamilton's ruler sign / Callaway's test).",
            clinical=True
        ),
        q(
            "What is the precise step-by-step sequence of maneuvers described by Kocher for closed reduction of an anterior shoulder dislocation?",
            "Traction -> External rotation -> Adduction -> Internal rotation",
            ["Adduction -> Internal rotation -> Direct pressure -> Traction", "Hyperabduction -> Elevation -> Downward traction -> Neutral rotation", "Internal rotation -> Traction -> Abduction -> Extension"],
            "Kocher's method consists of 4 distinct steps: 1. Traction in the line of the humerus with elbow flexed at 90 degrees; 2. External rotation of the arm slowly until resistance is felt (relaxes subscapularis and levers head out); 3. Adduction of the elbow across the front of the chest to the midline; 4. Internal rotation of the arm bringing the hand to the opposite shoulder (slides humeral head into glenoid fossa).",
            clinical=False
        ),
        q(
            "On an anteroposterior radiograph with internal rotation of the shoulder following recurrent anterior dislocations, a wedge-shaped compression fracture is visible on the posterolateral aspect of the humeral head. What is this lesion termed?",
            "Hill-Sachs lesion",
            ["Bankart lesion", "Bennett's lesion", "ALPSA lesion"],
            "A Hill-Sachs lesion is a compression/impact depression fracture on the posterolateral aspect of the humeral head. It is produced when the dislocated humeral head impacts against the hard, anterior-inferior rim of the glenoid. In contrast, a Bankart lesion affects the anterior-inferior glenoid labrum/rim.",
            clinical=False
        ),
        q(
            "A 45-year-old male is brought to the emergency department following a generalized tonic-clonic seizure with severe shoulder pain. The arm is locked in adduction and internal rotation, with complete loss of external rotation. AP radiograph shows a symmetrical, rounded humeral head resembling a 'light bulb'. What is the diagnosis?",
            "Posterior dislocation of the shoulder joint",
            ["Anterior subcoracoid shoulder dislocation", "Fracture of the greater tuberosity with subacromial impingement", "Rotator cuff tear arthropathy"],
            "Posterior shoulder dislocation is notoriously missed (in up to 50% of cases) and classically occurs after epileptic seizures, electric shocks, or electroconvulsive therapy due to violent contraction of the internal rotators (latissimus dorsi, pectoralis major, subscapularis) overpowering external rotators. Hallmark signs: arm locked in internal rotation and adduction; AP radiograph shows 'light-bulb sign'.",
            clinical=True
        ),
        q(
            "In Neer's classification of proximal humeral fractures, what criteria must a bone fragment meet to be classified as a displaced 'part'?",
            "Displacement greater than 1.0 cm or angulation greater than 45 degrees",
            ["Displacement greater than 2.0 cm or angulation greater than 90 degrees", "Any visible fracture line regardless of displacement", "Displacement greater than 5 mm with associated neurovascular deficit"],
            "Neer's classification is based on displacement of 4 anatomical segments: 1. Greater tuberosity; 2. Lesser tuberosity; 3. Humeral head (articular segment); 4. Humeral shaft. A fragment is considered a 'part' ONLY if it is displaced more than 1 cm (10 mm) or angulated more than 45 degrees from its anatomical position. An undisplaced fracture is a 'one-part' fracture even if all 4 lines are present.",
            clinical=False
        ),
        q(
            "A 28-year-old female sustains a distal third spiral fracture of the humerus (Holstein-Lewis fracture). On examination, she has wrist drop and sensory loss over the first dorsal web space. Which structure is at high risk of entrapment between fracture fragments?",
            "Radial nerve",
            ["Median nerve", "Ulnar nerve", "Musculocutaneous nerve"],
            "The Holstein-Lewis fracture is a spiral fracture of the distal third of the humeral shaft. At this level, the radial nerve pierces the lateral intermuscular septum to pass from the posterior to the anterior compartment, tethering it firmly to the bone. Distal third spiral fractures have a high incidence of radial nerve entrapment or laceration (up to 20-25%).",
            clinical=True
        ),
        q(
            "A 30-year-old male with a closed midshaft transverse humeral fracture presents with complete primary radial nerve palsy. What is the consensus first-line management strategy?",
            "Closed reduction and splinting (functional brace/U-slab) with observation for 3 to 4 months",
            ["Emergency open surgical exploration of the radial nerve within 6 hours", "Immediate resection of the fractured humerus with primary sural nerve grafting", "Emergency posterior arm compartment fasciotomy with immediate tendon transfers"],
            "Primary radial nerve palsy accompanying a closed humeral shaft fracture is almost always a neuropraxia or axonotmesis in continuity (>90% recover spontaneously within 3-4 months). Therefore, initial management is closed fracture reduction and splinting (U-slab/functional brace) and watchful waiting with serial clinical and EMG examinations. Exploration is reserved for open fractures, secondary palsy developing after manipulation, or failure of recovery after 3-4 months.",
            clinical=True
        ),
        q(
            "In a fracture of the middle third of the clavicle, what characteristic displacement forces are exerted by attached muscle groups on the proximal and distal fragments?",
            "Proximal fragment pulled upward by sternocleidomastoid; distal fragment pulled downward by arm weight and pectoralis major",
            ["Proximal fragment depressed by subclavius; distal fragment pulled upward by trapezius", "Proximal fragment pulled forward by deltoid; distal fragment displaced backward by latissimus dorsi", "Both fragments remain undisplaced due to rigid containment by costoclavicular ligament"],
            "In middle-third clavicular fractures, the sternocleidomastoid muscle pulls the medial (proximal) fragment superiorly and posteriorly. The lateral (distal) fragment is displaced inferiorly, anteriorly, and medially by the gravitational weight of the unsupported upper extremity and the strong adductor pull of the pectoralis major muscle.",
            clinical=False
        ),
        q(
            "In an active young adult, what threshold of superior displacement of a greater tuberosity fracture of the humerus mandates open reduction and internal fixation to prevent subacromial impingement?",
            "Displacement greater than 5 mm (or > 3 mm in overhead athletes)",
            ["Displacement greater than 15 mm exclusively", "Any displacement greater than 1 mm regardless of lifestyle", "Only complete detachment exceeding 30 mm"],
            "The greater tuberosity serves as the insertion site for the supraspinatus, infraspinatus, and teres minor tendons. Superior displacement of > 5 mm (or > 3 mm in high-demand overhead athletes) causes mechanical blockage and painful subacromial impingement against the acromion and coracoacromial arch during abduction, warranting surgical anatomical reduction and screw or suture-anchor fixation.",
            clinical=False
        ),
        q(
            "A 40-year-old male sustains an anterior shoulder dislocation. Clinical examination reveals deltoid weakness and sensory numbness over the lateral aspect of the upper arm ('regimental badge' area). Which nerve is injured?",
            "Axillary nerve",
            ["Radial nerve", "Suprascapular nerve", "Long thoracic nerve"],
            "The axillary nerve winds around the surgical neck of the humerus immediately inferior to the glenohumeral joint capsule. During anterior shoulder dislocation, the displaced humeral head stretches the nerve, causing neuropraxia in 10-15% of cases. Hallmark signs are paralysis/weakness of the deltoid muscle and sensory loss over the upper lateral aspect of the arm ('regimental badge' area).",
            clinical=True
        ),
    ]),

    # Chapter 14: Injuries Around the Elbow (HARD - 10 questions)
    (14, "Injuries Around the Elbow", "hard", [
        q(
            "A 7-year-old boy falls onto his outstretched hand with the elbow hyperextended. Examination shows a swollen, deformed elbow with S-shaped anterior skin puckering. Radiographs show distal humeral metaphysis disruption with posterior and superior displacement of the distal fragment. What is the diagnosis?",
            "Extension-type supracondylar fracture of the humerus (Gartland Type III)",
            ["Flexion-type supracondylar fracture of the humerus", "Posterior dislocation of the elbow joint", "Fracture of the olecranon process"],
            "Extension-type supracondylar fractures account for >95% of supracondylar fractures in children, classically caused by a fall onto an outstretched hand with hyperextended elbow. The distal fragment is displaced posteriorly and tilted into extension, while the sharp spike of the proximal fragment juts anteriorly into the brachialis muscle. Gartland Type III is completely displaced with disrupted cortices.",
            clinical=True
        ),
        q(
            "What crucial anatomical landmark relationship distinguishes a supracondylar fracture of the humerus from a posterior dislocation of the elbow joint?",
            "Three-point bony triangle is preserved in supracondylar fracture but disrupted in elbow dislocation",
            ["Active elbow flexion is preserved in dislocation but absent in fracture", "The radial head is palpable in supracondylar fracture but unpalpable in dislocation", "The carrying angle is increased in dislocation but reversed in fracture"],
            "The 'three-point bony relationship' consists of the tip of the olecranon and the two epicondyles: in 90 degrees of flexion they form an equilateral triangle; in full extension they lie in a straight horizontal line. In supracondylar fracture, the fracture line is entirely above the condyles, so the relationship among the epicondyles and olecranon remains normal. In elbow dislocation, the olecranon is displaced relative to the epicondyles, disrupting the triangle.",
            clinical=False
        ),
        q(
            "In a Gartland Type III supracondylar fracture of the humerus with posteromedial displacement of the distal fragment, which neurovascular structure is at greatest risk of injury from the proximal bone spike?",
            "Radial nerve",
            ["Median nerve and brachial artery", "Ulnar nerve", "Anterior interosseous nerve alone"],
            "The direction of distal fragment displacement dictates which neurovascular structures are endangered: When the distal fragment is displaced posteromedially, the sharp proximal fragment juts anterolaterally, endangering the radial nerve. Conversely, when the distal fragment is displaced posterolaterally, the proximal spike juts anteromedially, endangering the brachial artery and median nerve.",
            clinical=False
        ),
        q(
            "A 6-year-old child in an above-elbow slab for a supracondylar fracture develops severe forearm pain. The fingers are held in slight flexion. Attempting to passively extend the fingers produces excruciating volar forearm pain. What is the earliest pathognomonic sign of impending Volkmann's ischemia?",
            "Severe pain elicited by gentle passive extension of the fingers",
            ["Complete absence of the radial pulse at the wrist", "Development of a fixed claw hand with anesthesia", "Cold, pale, cyanotic hand with capillary refill > 5 seconds"],
            "Severe pain out of proportion to the injury, markedly exacerbated by passive extension of the fingers, is the earliest and most sensitive sign of impending Volkmann's ischemia (forearm compartment syndrome). The presence of a radial pulse does NOT exclude ischemia because capillary perfusion pressure is overwhelmed long before major arterial pulses cease. Pallor, pulselessness, and paralysis are late, irreversible signs.",
            clinical=True
        ),
        q(
            "Why is a displaced fracture of the lateral condyle of the humerus in a 6-year-old child termed a 'fracture of necessity' requiring anatomical open reduction and internal fixation?",
            "It is an intra-articular physeal fracture prone to non-union, cubitus valgus deformity, and late tardy ulnar nerve palsy",
            ["The fragment invariably undergoes complete septic chondrolysis within 48 hours", "The lateral condyle provides the sole blood supply to the olecranon process", "It triggers immediate ossification of the biceps tendon if treated in a cast"],
            "Lateral condyle fracture is a Salter-Harris Type IV intra-articular physeal fracture through the capitulum and trochlear groove. Because the extensor muscles attach to it, the fragment is rotated and tilted. Synovial fluid inhibits healing. Failure to achieve anatomical reduction leads to non-union, growth arrest, progressive cubitus valgus deformity, and tardy ulnar nerve palsy 10-20 years later. Hence, it is a 'fracture of necessity'.",
            clinical=True
        ),
        q(
            "A 3-year-old toddler is swung by the wrists by an adult. The child cries and refuses to use the arm, holding the elbow in slight flexion and pronation. Radiographs are normal. What is the diagnosis and reduction maneuver?",
            "Pulled elbow; reduced by forearm supination with thumb pressure over radial head, followed by elbow flexion",
            ["Supracondylar fracture Gartland I; reduced by hyperflexion and casting for 4 weeks", "Dislocation of distal radioulnar joint; reduced by forced pronation and splinting", "Radial neck fracture; treated by open surgical screw fixation"],
            "Pulled elbow occurs in children under 5 years when sudden longitudinal traction is applied to an extended, pronated arm. The immature, loose annular ligament slips over the rounded head of the radius into the radiocapitellar joint, where it becomes entrapped. Closed reduction is performed by supporting the elbow with thumb over radial head, rapidly supinating the forearm, and then fully flexing the elbow. A subtle 'click' is felt, and the child immediately resumes using the arm.",
            clinical=True
        ),
        q(
            "An adult falls onto an outstretched hand and sustains a Mason Type II radial head fracture (>30% articular surface, displaced >2 mm) without mechanical block. What is the treatment of choice?",
            "Open reduction and internal fixation (ORIF) with low-profile countersunk mini-screws",
            ["Radial head excision with prolonged immobilization in a sling", "Simple sling immobilization for 8 weeks without surgery", "Immediate total elbow replacement arthroplasty"],
            "According to the Mason classification of radial head fractures: Type I is undisplaced (conservative); Type II is a displaced partial articular fracture (>2 mm displacement, >30% articular surface); Type III is a severely comminuted fracture involving the entire radial head. For Mason Type II, ORIF with low-profile headless screws restoring articular congruity is the procedure of choice. Radial head excision in a young adult is avoided to prevent proximal radial migration.",
            clinical=True
        ),
        q(
            "Why is a displaced olecranon fracture treated with tension band wiring (TBW) rather than conservative casting?",
            "Tension band wiring dynamically converts the tensile distraction of the triceps into compressive forces across the joint",
            ["The olecranon has no endosteal blood supply and can only heal through titanium compression", "Plaster casts cause immediate ossification of the ulnar collateral ligament", "The ulnar nerve undergoes transection if an olecranon fracture is not wired"],
            "The olecranon forms the trochlear notch of the elbow joint. When fractured, the triceps muscle continually pulls the proximal fragment proximally, causing displacement and articular incongruity. A tension band construct (two parallel K-wires and a figure-of-eight stainless steel wire loop) harnesses the tensile pull of the triceps during elbow flexion and converts it into compressive force across the articular fracture surface, allowing early active movement.",
            clinical=False
        ),
        q(
            "A 28-year-old male sustains a severely displaced, comminuted intercondylar T- or Y-shaped distal humerus fracture. What is the gold-standard surgical approach and fixation construct?",
            "Olecranon osteotomy approach with anatomical condylar reduction and bicolumnar plate fixation",
            ["Anterior midline approach with a single lateral dynamic compression plate", "Closed reduction and multiple percutaneous pins placed across the elbow joint", "Immediate resection of both humeral condyles with a hinged splint"],
            "Intercondylar T- or Y-shaped fractures of the distal humerus involve complete intra-articular and metaphyseal dissociation. Surgical restoration requires direct exposure of the articular surface via a chevron olecranon osteotomy (or triceps-sparing approach), anatomical reduction and screw fixation of the articular condyles, and rigid stabilization of both medial and lateral columns using dual locking plates in a 90-90 (orthogonal) or parallel configuration.",
            clinical=True
        ),
        q(
            "Tardy ulnar nerve palsy is a classic late sequela developing 10 to 20 years following which pediatric elbow fracture?",
            "Malunited or non-united lateral condyle humerus fracture causing cubitus valgus deformity",
            ["Undisplaced supracondylar fracture resulting in mild cubitus varus", "Radial neck fracture treated with closed manipulation", "Medial epicondyle avulsion treated with early active motion"],
            "Tardy ulnar nerve palsy develops decades after an ununited or malunited fracture of the lateral condyle of the humerus. The arrest of lateral column growth combined with continued medial growth produces a progressive cubitus valgus deformity. With increasing valgus, the ulnar nerve is stretched around the medial epicondyle, leading to chronic friction neuritis, numbness in digits 4 and 5, and clawing. Treatment is anterior transposition of the ulnar nerve.",
            clinical=False
        ),
    ]),

    # Chapter 15: Injuries of the Forearm and Wrist (HARD - 10 questions)
    (15, "Injuries of the Forearm and Wrist", "hard", [
        q(
            "A 25-year-old male sustains an isolated fracture of the proximal third of the ulna associated with anterior dislocation of the radial head. What eponymic fracture-dislocation is this?",
            "Monteggia fracture-dislocation (Bado Type I)",
            ["Galeazzi fracture-dislocation", "Colles' fracture-dislocation", "Essex-Lopresti lesion"],
            "A Monteggia fracture-dislocation is a fracture of the shaft of the ulna associated with dislocation of the radio-capitellar joint (radial head). In Bado Type I (most common, ~60-70%), the ulnar fracture is angulated anteriorly, and the radial head is dislocated anteriorly. Bado Type II involves posterior dislocation; Type III involves lateral dislocation; Type IV involves fractures of both radius and ulna with radial head dislocation.",
            clinical=True
        ),
        q(
            "In a Monteggia fracture-dislocation, which peripheral nerve is at highest risk of stretch or entrapment by the dislocated radial head?",
            "Posterior Interosseous Nerve (PIN)",
            ["Anterior Interosseous Nerve (AIN)", "Ulnar nerve", "Superficial branch of radial nerve"],
            "The posterior interosseous nerve (PIN), the deep motor branch of the radial nerve, passes through the supinator muscle (Arcade of Frohse) immediately adjacent to the neck of the radius. When the radial head dislocates anteriorly or anterolaterally in a Monteggia fracture, the PIN is stretched across the dislocated radial head, resulting in PIN palsy (loss of MCP finger extension and thumb extension with preserved wrist extension due to ECRL innervation).",
            clinical=False
        ),
        q(
            "A 30-year-old motorcyclist falls onto a pronated forearm and sustains a fracture of the distal third radius shaft accompanied by disruption and dislocation of the Distal Radioulnar Joint (DRUJ). What is this injury termed?",
            "Galeazzi fracture-dislocation",
            ["Monteggia fracture-dislocation", "Barton's fracture", "Chauffeur's fracture"],
            "A Galeazzi fracture-dislocation consists of a fracture of the distal third of the radius shaft with disruption/dislocation of the distal radioulnar joint (DRUJ) and tearing of the triangular fibrocartilage complex (TFCC). It is also known as a 'fracture of necessity' because closed casting almost always fails due to the deforming forces of the pronator quadratus and brachioradialis; it requires rigid open reduction and plate fixation of the radius.",
            clinical=True
        ),
        q(
            "A 65-year-old postmenopausal woman sustains a Colles' fracture following a fall on an outstretched hand. What are the classical displacement components of the distal fragment?",
            "Dorsal displacement, dorsal tilt, radial displacement, radial tilt, supination, and impaction",
            ["Volar displacement, volar tilt, ulnar displacement, ulnar tilt, pronation, and distraction", "Dorsal displacement, volar tilt, radial displacement, pronation, distraction, and internal rotation", "Volar displacement, dorsal tilt, ulnar displacement, supination, impaction, and lengthening"],
            "In Colles' fracture (extra-articular fracture of the distal radius within 2.5 cm of the articular surface), the distal fragment undergoes 6 classical displacements: 1. Dorsal displacement (shifts backward); 2. Dorsal tilt (articular surface tilts dorsally); 3. Radial displacement (shifts outward); 4. Radial tilt (articular surface tilts radially); 5. Supination (rotates backward relative to proximal shaft); 6. Impaction (telescoping causing loss of radial length/radial height).",
            clinical=False
        ),
        q(
            "On standard radiographs of a normal adult wrist, what are the normal reference parameters for radial inclination and palmar (volar) tilt of the distal radius articular surface?",
            "Radial inclination of 21 to 23 degrees; Palmar tilt of 11 to 12 degrees",
            ["Radial inclination of 45 degrees; Palmar tilt of 0 degrees", "Radial inclination of 10 degrees; Dorsal tilt of 15 degrees", "Radial inclination of 30 degrees; Volar tilt of 25 degrees"],
            "On a standard posteroanterior (PA) radiograph, the distal radius articular surface angles towards the ulna with a normal radial inclination of 21 to 23 degrees (and a radial height of 11-12 mm). On a true lateral radiograph, the articular surface tilts forward with a normal palmar (volar) tilt of 11 to 12 degrees. In Colles' fracture, radial inclination is reduced and volar tilt is reversed into a dorsal tilt.",
            clinical=False
        ),
        q(
            "A 32-year-old male falls onto the back of his flexed wrist, presenting with a 'garden-spade' deformity. Radiographs show a distal radius metaphyseal fracture with volar displacement and volar tilt of the distal fragment. What is the diagnosis?",
            "Smith's fracture (Reverse Colles' fracture)",
            ["Colles' fracture", "Barton's fracture", "Rolando's fracture"],
            "Smith's fracture (reverse Colles' fracture) is caused by a fall onto a flexed wrist or a direct blow to the dorsum of the flexed wrist. The fracture line is extra-articular at the distal radius metaphysis, and the distal fragment is displaced anteriorly (volarly) and tilted volarly, producing the classic 'garden-spade' deformity. It is inherently unstable and usually requires buttress plate fixation.",
            clinical=True
        ),
        q(
            "How does a Barton's fracture anatomically differ from both Colles' and Smith's fractures?",
            "Barton's is an intra-articular fracture-subluxation of the radiocarpal joint involving the dorsal or volar rim",
            ["Barton's is an extra-articular diaphyseal greenstick fracture of the radius", "Barton's involves an isolated avulsion of the ulnar styloid process", "Barton's is an isolated dislocation of the scapholunate joint without fracture"],
            "While Colles' and Smith's fractures are extra-articular metaphyseal fractures, Barton's fracture is an intra-articular fracture-dislocation or subluxation of the radiocarpal joint. An oblique fracture line shears off either the dorsal lip (Dorsal Barton's) or the volar lip (Volar Barton's) of the distal radius articular surface, and the entire carpus displaces along with the articular bone fragment. Volar Barton's is treated with a volar buttress plate.",
            clinical=False
        ),
        q(
            "A 22-year-old male presents with anatomical snuffbox tenderness and pain on axial loading of the thumb following a fall on an outstretched hand. Initial plain radiographs of the wrist are normal. What is the mandatory management protocol?",
            "Immobilize in a scaphoid cast and repeat radiographs in 10 to 14 days, or obtain an early MRI",
            ["Reassure the patient of a simple sprain and discharge without splinting", "Apply an elastic crepe bandage and encourage immediate heavy manual loading", "Perform immediate open reduction and headless screw fixation without further imaging"],
            "A high index of suspicion for scaphoid fracture must be maintained whenever anatomical snuffbox tenderness is present following a fall on an outstretched hand. Undisplaced hairline fractures of the scaphoid waist are notoriously invisible on initial radiographs (false negative in up to 15-20%). The standard protocol mandates applying a scaphoid plaster cast and repeating radiographs after 10-14 days (when bone resorption along the fracture line makes it visible), or performing an early MRI/CT scan.",
            clinical=True
        ),
        q(
            "Why is a fracture traversing the proximal pole of the scaphoid at high risk of developing avascular necrosis (AVN)?",
            "Retrograde intraosseous blood supply enters through distal foramina, leaving proximal pole ischemic",
            ["The proximal pole is covered by periosteum that lacks osteoblasts", "Synovial fluid decomposes the proximal pole through proteolytic enzymes", "The scaphoid bone is composed entirely of cortical bone without cancellous marrow"],
            "The arterial blood supply to the scaphoid is retrograde: branches of the radial artery enter the bone through vascular foramina on the non-articular dorsal ridge and distal tubercle, flowing proximally within the bone to supply the waist and proximal pole. A fracture through the waist or proximal pole severs this intraosseous arterial network, rendering the proximal fragment completely ischemic and predisposing it to avascular necrosis (AVN) in nearly 100% of proximal pole fractures.",
            clinical=False
        ),
        q(
            "On a true lateral radiograph of the wrist following high-energy trauma, the lunate maintains its normal articulation with the distal radius, but the capitate is dislocated dorsally out of the lunate cup. What is the diagnosis?",
            "Perilunate dislocation of the wrist",
            ["Lunate dislocation (anterior dislocation of lunate)", "Scapholunate advanced collapse (SLAC)", "Isolated triquetral fracture-dislocation"],
            "In perilunate dislocation, the lunate remains in its normal anatomical position within the lunate fossa of the distal radius, but the rest of the carpus (headed by the capitate) is displaced dorsally. In contrast, in a true lunate dislocation, the capitate remains aligned with the radius, while the lunate is squeezed out of the carpal space and displaced volarly into the carpal tunnel, tilting like a 'spilled teacup'.",
            clinical=True
        ),
    ]),

    # Chapter 16: Hand Injuries (Easy - 5 questions)
    (16, "Hand Injuries", "easy", [
        q(
            "A 24-year-old boxer strikes a wall with a clenched fist, developing acute swelling at the thumb base. Radiographs reveal an intra-articular fracture through the base of the first metacarpal with shaft subluxation. What eponymic fracture is this?",
            "Bennett's fracture-dislocation",
            ["Rolando's fracture", "Boxer's fracture", "Gamekeeper's thumb"],
            "Bennett's fracture-dislocation is an intra-articular fracture-subluxation of the base of the first metacarpal. A triangular avulsion fragment of the volar-ulnar lip remains attached to the trapezium via the anterior oblique (beak) ligament, while the entire metacarpal shaft is displaced proximally, dorsally, and radially by the pull of the abductor pollicis longus (APL) muscle.",
            clinical=True
        ),
        q(
            "In Bennett's fracture-dislocation of the first metacarpal, which muscle tendon exerts the primary deforming force displacing the metacarpal shaft proximally, dorsally, and radially?",
            "Abductor Pollicis Longus (APL)",
            ["Adductor pollicis", "Flexor Pollicis Brevis (FPB)", "Extensor Pollicis Brevis (EPB)"],
            "The abductor pollicis longus (APL) inserts into the base of the first metacarpal. When the intra-articular volar lip fracture occurs, the stabilizing anterior oblique ligament remains attached only to the small volar-ulnar fragment. The unrestrained APL tendon pulls the main metacarpal shaft proximally, dorsally, and radially, while the adductor pollicis adducts the distal head, rendering closed conservative casting unstable.",
            clinical=False
        ),
        q(
            "How does a Rolando's fracture anatomically differ from a Bennett's fracture-dislocation?",
            "Rolando's fracture is a comminuted T- or Y-shaped intra-articular fracture of the first metacarpal base",
            ["Rolando's fracture involves the fifth metacarpal base exclusively", "Rolando's fracture is an extra-articular diaphyseal injury", "Rolando's fracture occurs exclusively through an open pediatric growth plate"],
            "While Bennett's fracture is an oblique, two-part intra-articular fracture of the base of the first metacarpal, Rolando's fracture is a three-part or comminuted T- or Y-shaped intra-articular fracture of the first metacarpal base. Because of extensive joint comminution, treatment is technically demanding, requiring external fixation, open reduction with mini-plates, or percutaneous pin fixation.",
            clinical=False
        ),
        q(
            "In Verdan's classification of flexor tendon injuries, why is Zone II (distal palmar crease to FDS insertion) traditionally called 'No Man's Land'?",
            "Both FDS and FDP tendons travel within a tight fibro-osseous sheath, prone to dense cicatricial adhesions",
            ["Zone II has zero microvascular supply, preventing biological tendon healing", "Digital nerve repair is strictly contraindicated due to vasospasm", "Any surgical intervention in Zone II causes ischemic necrosis of the distal phalanx"],
            "Zone II extends from the distal palmar crease to the middle of the middle phalanx (FDS insertion). Within this zone, both the FDS and FDP tendons are tightly contained inside the narrow, rigid fibro-osseous digital sheath with its annular pulleys. Historically, primary repair resulted in severe adhesions binding both tendons together and to the sheath ('No Man's Land'), leading Bunnell to recommend delayed tendon grafting. Modern microsurgical repair and early protected motion protocols have improved outcomes.",
            clinical=False
        ),
        q(
            "A basketball player sustains a forceful hyperflexion blow to the tip of an extended finger, resulting in inability to actively extend the DIP joint while passive extension is full. What is the diagnosis and initial management?",
            "Mallet finger; treated with continuous DIP extension splinting for 6 to 8 weeks",
            ["Trigger finger; treated with percutaneous release of the A1 pulley", "Swan-neck deformity; treated with immediate surgical central slip repair", "Boutonnière deformity; treated with acute PIP joint flexion casting"],
            "Mallet finger is caused by avulsion of the terminal extensor tendon from the base of the distal phalanx (with or without a small avulsion bone fragment) due to sudden forced flexion of an actively extended DIP joint. The patient cannot actively extend the DIP joint. Initial management for closed injuries is continuous immobilization of the DIP joint in slight hyperextension (using a Stack splint or mallet splint) for 6 to 8 weeks; PIP joint motion is kept free.",
            clinical=True
        ),
    ]),
]
