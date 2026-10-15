from .common import q

CHAPTERS = [
    # Chapter 1: Orthopaedic Trauma: Introduction (Easy - 5 questions)
    (1, "Orthopaedic Trauma: Introduction", "easy", [
        q(
            "A 32-year-old construction worker is brought to the casualty following a high-velocity motor vehicle crash. Examination reveals an open tibial fracture with an 11-cm laceration, extensive soft-tissue stripping, and exposed cortical bone. Periosteal coverage is preserved, and local soft-tissue coverage of the bone is achievable without a free flap. Distal neurovascular status is intact. According to the Gustilo-Anderson classification, this fracture is categorized as",
            "Type IIIA",
            ["Type IIIB", "Type IIIC", "Type II"],
            "Gustilo-Anderson Type IIIA fractures involve high-energy trauma with an open wound > 10 cm and extensive soft-tissue laceration or flaps, but adequate soft-tissue coverage of bone is present. Type IIIB involves extensive periosteal stripping and bone exposure requiring reconstructive flap coverage. Type IIIC includes an open fracture associated with an arterial injury requiring repair.",
            clinical=True
        ),
        q(
            "A 58-year-old postmenopausal woman with known metastatic adenocarcinoma presents with sudden severe right thigh pain while walking, without antecedent trauma. Radiographs reveal an osteolytic lesion with a transverse cortical break in the subtrochanteric region of the right femur. Which pathogenetic mechanism defines this fracture?",
            "Failure through bone weakened by pre-existing focal pathology",
            ["Cyclic fatigue failure of normal bone under repetitive strain", "Microtrabecular insufficiency failure from acute periosteal avulsion", "Stress concentration at the insertion of normal tendon"],
            "A pathological fracture occurs through bone weakened by pre-existing disease (such as metastases, multiple myeloma, bone cysts, or osteomyelitis) under normal physiological stress. In contrast, stress/fatigue fractures result from cyclic, repetitive subthreshold loading on structurally normal bone.",
            clinical=True
        ),
        q(
            "In an acute trauma patient who fell from a height, radiographs show a fracture where two bony fragments are firmly driven into each other without abnormal mobility at the fracture site. What is the clinical hallmark of this impacted fracture?",
            "Absence of abnormal mobility and crepitus despite localized bony tenderness",
            ["Presence of a visible flail segment with false joint motion", "Audible crepitus upon gentle limb rotation", "Immediate distal sensory loss from nerve tethering"],
            "In impacted fractures, the fractured bone fragments are driven into each other, providing intrinsic temporary stability. Consequently, the classical signs of fracture like abnormal mobility and bone crepitus are absent, making diagnosis dependent on localized tenderness, loss of function, and radiographic demonstration.",
            clinical=True
        ),
        q(
            "A 42-year-old mechanic sustains an isolated, displaced intra-articular fracture of the radial styloid process following a rotational blow to the dorsoradial wrist. What is the eponym for this injury?",
            "Chauffeur's fracture",
            ["Barton's fracture", "Smith's fracture", "Galeazzi's fracture"],
            "Chauffeur's (Hutchinson's) fracture is an intra-articular fracture of the radial styloid process, historically caused by the backfire of an automobile starting crank handle hitting the dorsum of the wrist. Barton's is an intra-articular fracture-subluxation of the radiocarpal joint, Smith's is a reverse Colles' fracture, and Galeazzi's is a distal radius fracture with distal radioulnar joint dislocation.",
            clinical=False
        ),
        q(
            "A collegiate athlete suffers a severe inversion injury of the ankle. Clinical examination reveals marked diffuse swelling, severe ecchymosis, complete loss of ligamentous restraint with wide joint opening on stress testing, and an inability to bear weight. This ligament injury is classified as",
            "Grade III sprain (complete tear)",
            ["Grade I sprain (mild stretch)", "Grade II sprain (partial tear)", "Grade IV sprain (articular subluxation)"],
            "Ligament injuries are graded based on tissue disruption: Grade I is a mild stretch with microscopic fiber tearing, no joint laxity, and minimal swelling; Grade II is a partial or incomplete tear with moderate laxity and preserved endpoint; Grade III is a complete ligament rupture with gross joint instability, wide joint opening, and severe loss of function.",
            clinical=True
        ),
    ]),

    # Chapter 2: Anatomy of Bone and Fracture Healing (Easy - 5 questions)
    (2, "Anatomy of Bone and Fracture Healing", "easy", [
        q(
            "During physiological secondary fracture healing in a tubular long bone, what is the correct chronological sequence of reparative stages?",
            "Hematoma -> Granulation tissue -> Callus formation -> Consolidation -> Remodeling",
            ["Hematoma -> Callus formation -> Granulation tissue -> Remodeling -> Consolidation", "Granulation tissue -> Hematoma -> Consolidation -> Callus formation -> Remodeling", "Hematoma -> Primary osteon bridging -> Fibrous sleeve -> Medullary remodeling"],
            "Secondary (indirect) bone healing occurs in 5 classical stages: 1. Stage of hematoma (hours to days); 2. Stage of granulation tissue (soft tissue procallus, ~2 weeks); 3. Stage of callus (cartilaginous soft callus transforming to hard woven bone callus by endochondral ossification, ~4-12 weeks); 4. Stage of consolidation (woven bone replaced by mature lamellar bone); 5. Stage of remodeling (restoration of original cortical architecture).",
            clinical=False
        ),
        q(
            "A 28-year-old athlete undergoes anatomical reduction and absolute rigid internal fixation of a transverse radial shaft fracture using a compression plate with zero interfragmentary strain. Postoperative radiographs show progressive disappearance of the fracture line without any visible external callus. What type of bone healing has occurred?",
            "Primary (direct) cortical bone healing",
            ["Secondary bone healing with delayed union", "Endochondral ossification within the medullary canal", "Fibrous union without osteogenesis"],
            "Primary (direct) bone healing occurs when a fracture is anatomically reduced with absolute rigidity and interfragmentary compression (strain < 2%). Under these biomechanical conditions, no external callus forms; instead, osteoclasts create longitudinal cutting cones across the fracture interface, immediately followed by osteoblasts depositing secondary osteons directly bridging the fracture gap.",
            clinical=True
        ),
        q(
            "Under normal physiological conditions in the adult skeleton, what is the anatomical distribution of arterial blood supply to the diaphysis of a long bone?",
            "Nutrient artery supplies inner two-thirds; periosteal vessels supply outer one-third",
            ["Periosteal vessels supply inner two-thirds; nutrient artery supplies outer one-third", "Nutrient artery supplies the entire cortex under centripetal flow", "Metaphyseal anastomoses supply 80% of the mid-diaphyseal cortex"],
            "The diaphysis of a tubular long bone receives a centrifugal arterial supply: the nutrient artery enters the nutrient canal, divides into ascending and descending medullary branches, and supplies the bone marrow and inner two-thirds of the cortex under high hydrostatic pressure. The periosteal capillary network provides the outer one-third of the cortex under lower pressure.",
            clinical=False
        ),
        q(
            "Why does a fracture of cancellous bone (such as the calcaneum or vertebral body) heal substantially faster than a fracture through cortical bone?",
            "Abundant osteogenic trabecular surface area with direct internal callus union",
            ["Absence of endosteal capillary networks allowing rapid fibrous bridging", "Higher hydroxyapatite density resisting local shear strain", "Greater dependence on external periosteal cartilaginous sleeve formation"],
            "Cancellous bone has a broad contact area, highly vascular marrow, and abundant trabecular surfaces lined by active osteoblasts. Fracture healing in cancellous bone occurs by direct internal callus and trabecular bridging without the intermediate large external periosteal cartilaginous callus phase required in cortical bone.",
            clinical=False
        ),
        q(
            "A 40-year-old chronic heavy smoker on long-term systemic corticosteroids sustains a closed distal tibial shaft fracture. At 6 months, he exhibits persistent mobility and absence of bridging callus. Which combination of mechanisms is primarily responsible for impaired union in this patient?",
            "Microvascular vasoconstriction and suppressed osteoblast differentiation",
            ["Elevated calcitonin levels and excessive bone resorption", "Accelerated osteoid matrix synthesis with fibrous capping", "Increased vascular endothelial growth factor with premature remodeling"],
            "Smoking causes peripheral vasoconstriction, tissue hypoxia, and downregulates osteoblast function through nicotine and carbon monoxide toxicity. Systemic corticosteroids inhibit osteoblast differentiation, downregulate type I collagen synthesis, and impair local angiogenesis, dramatically predisposing the fracture to delayed union or non-union.",
            clinical=True
        ),
    ]),

    # Chapter 3: Treatment of Fractures: General Principles (Easy - 5 questions)
    (3, "Treatment of Fractures: General Principles", "easy", [
        q(
            "A 24-year-old motorcyclist arrives in the emergency department with a contaminated Gustilo Type IIIB open tibial fracture 2 hours after a crash. Following ABCDE resuscitation, what is the mandatory immediate local management step?",
            "Sterile dressing, intravenous antibiotics, splinting, and urgent operative debridement",
            ["Immediate primary wound closure in the emergency room under local anesthesia", "Vigorous mechanical scrub with povidone-iodine and definitive plate fixation", "Wound packing with topical antibiotic powder and delayed cast immobilization"],
            "Management of open fractures prioritizes prevention of sepsis: after initial ATLS stabilization, the wound is photographed, covered with a sterile saline-soaked dressing (no probing in the ER), IV antibiotics and tetanus prophylaxis are administered immediately, the limb is splinted, and the patient is taken to the operating room for formal debridement, copious saline irrigation, and skeletal stabilization.",
            clinical=True
        ),
        q(
            "What chemical reaction occurs during the setting of Plaster of Paris (POP) bandages used for orthopaedic cast immobilization?",
            "Exothermic conversion of calcium sulfate hemihydrate to calcium sulfate dihydrate",
            ["Endothermic polymerization of anhydrous calcium phosphate into hydroxyapatite", "Non-thermal evaporation of ethyl silicate leaving a rigid silica matrix", "Oxidation of hydrated calcium carbonate catalyzed by ambient oxygen"],
            "Plaster of Paris consists of gypsum (calcium sulfate dihydrate) that has been heated to drive off part of its water of crystallization, forming calcium sulfate hemihydrate: (CaSO4)2.H2O. When mixed with water, it rehydrates to form calcium sulfate dihydrate [CaSO4.2H2O] in an exothermic reaction that generates palpable heat during setting.",
            clinical=False
        ),
        q(
            "Why is anatomical reduction with rigid internal fixation mandatory in intra-articular fractures, whereas minor axial displacement can be accepted in extra-articular diaphyseal fractures?",
            "Articular step-off alters contact stresses and leads to rapid post-traumatic osteoarthritis",
            ["Intra-articular fractures heal exclusively through extensive periosteal bridging callus", "Synovial fluid degrades any metal implant that lacks interfragmentary compression", "Articular cartilage contains abundant blood supply that triggers heterotopic ossification"],
            "Articular cartilage has virtually no regenerative capacity. Any residual intra-articular step-off or gap greater than 1-2 mm causes concentrated contact stresses across opposing cartilage surfaces during joint motion, producing accelerated cartilage wear and debilitating post-traumatic osteoarthritis.",
            clinical=False
        ),
        q(
            "When immobilizing a fractured long bone in a plaster cast, what is the standard joint immobilization rule to achieve rotational and angular stability?",
            "Immobilize the joint immediately proximal and the joint immediately distal to the fracture",
            ["Encompass all joints of the entire affected extremity up to the trunk", "Immobilize only the fracture zone, leaving both adjacent joints completely mobile", "Immobilize the proximal joint only, while keeping the distal joint free"],
            "To prevent angular displacement and especially rotational shearing forces exerted by muscles traversing the fracture site, a rigid cast must immobilize the joint immediately above and the joint immediately below the fractured long bone (e.g., above-knee cast for tibia fracture, above-elbow cast for forearm bones fracture).",
            clinical=False
        ),
        q(
            "A 35-year-old male with an isolated closed midshaft transverse femoral fracture is hemodynamically stable. What is the definitive treatment of choice?",
            "Closed reamed locked intramedullary interlocking nailing",
            ["Open reduction and broad dynamic compression plate (DCP) fixation", "Skeletal traction on a Bohler-Braun frame for 12 weeks", "External ring fixator with tensioned transfixion wires"],
            "Closed reamed locked intramedullary interlocking nailing is the gold standard for diaphyseal femoral fractures: it provides load-sharing biomechanical stability, preserves the fracture hematoma and periosteal biology, allows early mobilization and weight-bearing, and achieves union rates exceeding 95-98%.",
            clinical=True
        ),
    ]),

    # Chapter 4: Splints and Tractions (Easy - 5 questions)
    (4, "Splints and Tractions", "easy", [
        q(
            "A 26-year-old male sustains an isolated closed midshaft femur fracture in a rural area. Which emergency splint should be applied to provide immediate pain relief, align fragments, and minimize bleeding during ambulance transport?",
            "Thomas splint with fixed traction",
            ["Bohler-Braun splint with hanging weights", "Cramer wire splint bent at 90 degrees", "Denis Browne splint with bilateral footplates"],
            "The Thomas splint is the standard emergency splint for femur shaft fractures. It utilizes the padded ring seated against the ischial tuberosity as a counter-traction point while fixed traction is applied to the foot/ankle, aligning the bone, reducing muscle spasm, minimizing bleeding, and preventing bone ends from piercing the femoral neurovascular bundle.",
            clinical=True
        ),
        q(
            "When setting up skeletal traction on a Bohler-Braun frame for a femoral fracture, how many pulleys are present on the frame and what is the primary role of the middle pulley?",
            "Three pulleys; the middle pulley maintains traction in the longitudinal axis of the femur",
            ["Two pulleys; the middle pulley suspends the foot to prevent foot drop", "Four pulleys; the middle pulley controls lateral tilt of the patella", "One pulley; it redirects both counter-traction and limb elevation"],
            "The Bohler-Braun frame has three pulleys: the distal/inferior pulley prevents foot drop by suspending the foot, the middle pulley carries the primary traction cord aligned with the axis of the femur, and the proximal/superior pulley is used for supracondylar or vertical traction when needed.",
            clinical=False
        ),
        q(
            "A surgeon plans to insert a Steinmann pin through the proximal tibia for skeletal traction in a distal femoral fracture. To avoid iatrogenic injury to the common peroneal nerve, what is the safe anatomical entry site and direction of pin insertion?",
            "2 cm posterior and 2 cm inferior to the tibial tuberosity, driven from lateral to medial",
            ["1 cm anterior to the fibular head, driven from lateral to medial", "3 cm directly distal to the medial joint line, driven from medial to lateral", "Directly through the tibial tuberosity crest, driven from anterior to posterior"],
            "The safe entry point for proximal tibial skeletal traction is 2 cm posterior and 2 cm inferior to the tibial tuberosity. It must be inserted from the lateral side to the medial side because inserting from lateral to medial pushes the pin away from the common peroneal nerve winding around the fibular neck.",
            clinical=True
        ),
        q(
            "What is the maximum safe weight permissible when applying skin traction to an adult lower limb?",
            "4 to 5 kg (or roughly 10% of body weight)",
            ["8 to 10 kg", "12 to 15 kg", "1 to 2 kg"],
            "Skin traction relies on adhesive strapping applied to the skin and subcutaneous tissues. The maximum safe weight that can be applied is 4 to 5 kg (approximately 10% of body weight). Exceeding this limit leads to shearing forces that tear epidermis from the dermis, causing severe friction blisters, skin sloughing, and ulceration.",
            clinical=False
        ),
        q(
            "One week after insertion of a distal femoral skeletal traction pin, a patient develops high fever, severe knee pain, and a tense knee effusion. Arthrocentesis confirms septic arthritis. What technical error during pin insertion caused this complication?",
            "Pin inserted too distal, violating the suprapatellar synovial pouch",
            ["Pin inserted through the adductor tubercle, injuring the saphenous nerve", "Pin driven from medial to lateral, piercing the femoral artery", "Pin placed through the popliteus tendon groove on the lateral condyle"],
            "The suprapatellar pouch of the knee joint extends up to 5 cm proximal to the superior pole of the patella beneath the quadriceps tendon. If a distal femoral traction pin is placed too distal (within 2-3 cm of the joint line), it penetrates the synovial pouch; pin track infection can then track directly into the joint space, producing septic arthritis.",
            clinical=True
        ),
    ]),

    # Chapter 5: Recent Advances in the Treatment of Fractures (Easy - 5 questions)
    (5, "Recent Advances in the Treatment of Fractures", "easy", [
        q(
            "In elderly patients with severe osteoporotic comminuted metaphyseal fractures, how does a Locking Compression Plate (LCP) achieve mechanical stability compared to a conventional Dynamic Compression Plate (DCP)?",
            "Threaded screw heads lock into the plate, forming a fixed-angle internal fixator independent of bone friction",
            ["Screws compress the plate tightly against periosteum to maximize frictional grip", "The plate undergoes thermal memory contraction to compress fracture fragments", "The plate delivers piezoelectric micro-currents to stimulate periosteal osteogenesis"],
            "In conventional DCP, stability depends on friction generated by pressing the plate tightly against the bone surface, which requires strong bone screw purchase and strips periosteal blood supply. In an LCP, threaded screw heads lock rigidly into the plate, forming a fixed-angle 'internal fixator' construct where stability depends on the screw-plate interface rather than bone-plate friction, protecting periosteal vascularity.",
            clinical=False
        ),
        q(
            "Which fundamental biological principle forms the basis of distraction osteogenesis in the Ilizarov method?",
            "Law of tension-stress: gradual controlled mechanical distraction stimulates active tissue regeneration",
            ["Wolff's law of bone remodeling under compressive piezoelectric polarity", "Pauwels' law of shear-force suppression in intra-articular fractures", "Heuter-Volkmann law of epiphyseal growth retardation under compression"],
            "Ilizarov's Law of Tension-Stress states that gradual, continuous mechanical traction applied to living tissues creates a state of active metabolic stimulation that induces tissue regeneration and histogenesis of bone, vessels, nerves, skin, and muscle. In cortical bone, distraction at a rate of 1 mm per day in 4 divided increments produces robust new bone.",
            clinical=False
        ),
        q(
            "A 36-year-old male sustains a comminuted distal tibial fracture with significant soft-tissue contusion. The surgeon chooses Minimally Invasive Percutaneous Plate Osteosynthesis (MIPPO). What is the main biological advantage of this technique?",
            "Submuscular extra-periosteal plate tunneling preserves fracture hematoma and periosteal blood supply",
            ["Direct anatomical reduction and rigid compression of every small comminuted fragment", "Elimination of intraoperative fluoroscopy and radiation exposure", "Production of absolute rigid stability with primary direct bone healing"],
            "MIPPO is a biological fixation method: rather than opening the fracture site (which evacuates osteogenic fracture hematoma and strips periosteal blood vessels), a plate is inserted percutaneously through small proximal and distal incisions and bridged across the comminuted zone. This preserves the biological osteogenic envelope and promotes rapid secondary healing via robust bridging callus.",
            clinical=True
        ),
        q(
            "How has the modern philosophy of AO fracture fixation evolved regarding the treatment of comminuted diaphyseal fractures?",
            "Shifted from anatomical rigidity and direct healing to biological flexible fixation and secondary callus union",
            ["Shifted from closed intramedullary nailing to routine open anatomical plating of all fragments", "Shifted from functional mobilization to prolonged cast immobilization after plate fixation", "Shifted to exclusive conservative management with skeletal traction for 12 weeks"],
            "The original AO concept emphasized anatomical reduction, absolute rigid fixation, interfragmentary compression, and primary direct bone healing without callus. Over time, extensive periosteal stripping caused high rates of non-union and infection in comminuted fractures. The modern AO philosophy emphasizes 'biological fixation'—preserving vascularity and soft tissues, achieving functional alignment, and encouraging secondary healing with robust bridging callus.",
            clinical=False
        ),
        q(
            "What is the mechanical mechanism by which a Sarmiento functional brace stabilizes a midshaft humeral or tibial fracture during limb movement?",
            "Compression of surrounding musculature creates hydrostatic fluid pressure that maintains axial alignment",
            ["Rigid metallic hinge locks eliminate all adjacent joint rotation and motion", "Absolute suppression of interfragmentary micro-motion allowing direct primary union", "Continuous transcutaneous electrical stimulation of deep compartment flexors"],
            "Sarmiento functional bracing utilizes hydrostatic pressure: rigid or semi-rigid shells conform tightly to the thigh, leg, or arm, compressing the fluid-filled muscular envelope. When the muscles contract during active joint motion, the enclosed fluid/soft tissues act as an incompressible hydraulic cylinder that resists angular and shortening displacement while allowing beneficial axial micro-motion.",
            clinical=False
        ),
    ]),

    # Chapter 6: Approach to a Patient with Limb Injury (Easy - 5 questions)
    (6, "Approach to a Patient with Limb Injury", "easy", [
        q(
            "A 29-year-old driver involved in a high-speed roll-over crash arrives with a deformed right thigh and hypotension (BP 85/55 mmHg). In accordance with ATLS primary survey resuscitation protocols, what three screening radiographs are routinely obtained in the trauma bay?",
            "Cervical spine lateral (or CT), Chest AP, and Pelvis AP",
            ["Skull AP/Lateral, Femur AP/Lateral, and Abdomen erect", "Pelvis AP, Bilateral knees AP, and Thoracolumbar spine AP", "Chest PA erect, Right femur AP/Lateral, and Forearm AP"],
            "During the ATLS primary survey resuscitation phase, after managing Airway, Breathing, and Circulation, the three standard screening radiographs for an unconscious or severely injured polytrauma patient are: 1. Cervical spine lateral (or rapid pan-scan CT); 2. Chest anteroposterior (AP); and 3. Pelvis AP (to rapidly identify life-threatening hemorrhage from pelvic ring disruption). Individual extremity radiographs are performed during the secondary survey.",
            clinical=True
        ),
        q(
            "In standard orthopaedic radiography, what are the components of the clinical 'Rule of Twos'?",
            "Two views (AP/Lateral), Two joints (above/below), Two limbs (in children), and Two occasions (pre/post-reduction)",
            ["Two surgeons, Two assistants, Two tourniquets, and Two hours maximum operating time", "Two radiographs per hour, Two splints per limb, Two weeks traction, and Two months casting", "Two skin incisions, Two cortical screws, Two locking plates, and Two suction drains"],
            "The 'Rule of Twos' in orthopaedic radiology consists of: 1. Two views: Anteroposterior (AP) and lateral, as a fracture visible in one projection may be completely concealed in the other; 2. Two joints: Must include the joint above and joint below the fractured bone; 3. Two limbs: In pediatric patients with open growth plates, compare with the uninjured opposite limb; 4. Two occasions: Repeat radiograph immediately after reduction, and after 1-2 weeks if an undisplaced or stress fracture is suspected.",
            clinical=False
        ),
        q(
            "A 6-year-old child presents with elbow pain and swelling following a fall from monkey bars. Why is a comparative radiograph of the contralateral uninjured elbow essential before ruling out a fracture?",
            "Multiple unossified cartilaginous centers and normal physes can simulate or conceal fractures",
            ["Pediatric elbow injuries are obligatorily bilateral due to symmetrical force transmission", "Contralateral comparison is required to determine systemic osteoid mineralization status", "Physeal closure occurs prematurely within 24 hours of contralateral injury"],
            "The pediatric elbow has six secondary ossification centers that appear and fuse at predictable ages (CRITOE: Capitulum 1y, Radial head 3y, Internal/medial epicondyle 5y, Trochlea 7y, Olecranon 9y, External/lateral epicondyle 11y). Non-ossified cartilage is radiolucent, and normal physeal lines can be misdiagnosed as fractures, or displaced avulsion fragments misdiagnosed as normal centers. A comparative film of the normal elbow prevents catastrophic errors.",
            clinical=True
        ),
        q(
            "In orthopaedic clinical practice, after what time interval is an untreated or neglected fracture formally classified as an 'old fracture'?",
            "More than 3 weeks after injury",
            ["More than 48 hours after injury", "More than 7 days after injury", "More than 6 months after injury"],
            "According to standard orthopaedic definitions, an untreated fracture presenting more than 3 weeks after trauma is categorized as an 'old fracture'. By 3 weeks, early soft callus and fibrous tissue have organized between the fragments, making simple closed reduction impossible without formal open mobilization, osteoclasis, or osteotomy.",
            clinical=False
        ),
        q(
            "A 34-year-old male with an open distal femoral fracture presents with an expanding pulsatile hematoma in the popliteal fossa, absent distal pedal pulses, and a cold, pale foot. What is the immediate management requirement?",
            "Immediate emergency surgical exploration in the operating room without delaying for CT angiography",
            ["Urgent non-contrast CT scan of the brain followed by CT angiography of the lower limb", "Application of an elastic compression bandage and observation for 6 hours", "Immediate reduction of the fracture in the emergency room under local hematoma block"],
            "'Hard signs' of arterial injury include: 1. Active, pulsatile arterial bleeding; 2. Expanding or pulsatile hematoma; 3. Palpable thrill or audible bruit; 4. Absent distal pulses; 5. Obvious signs of distal limb ischemia (pale, cold, mottled, pulseless extremity). The presence of hard signs mandates immediate emergency surgical exploration and vascular repair without wasting precious warm ischemia time on non-invasive imaging.",
            clinical=True
        ),
    ]),

    # Chapter 7: Complications of Fractures (HARD - 10 questions)
    (7, "Complications of Fractures", "hard", [
        q(
            "A 24-year-old male with a closed midshaft tibial fracture in an above-knee cast develops excruciating leg pain 8 hours post-injury. The pain is refractory to IV morphine and is exacerbated by passive extension of the toes. The anterolateral compartment is tense and woody. Distal pedal pulses are palpable. What is the immediate management step?",
            "Bivalve the cast and split all padding to the skin, and prepare for urgent four-compartment fasciotomy",
            ["Administer intravenous mannitol and elevate the leg 45 degrees above the heart", "Apply an ice pack, increase the analgesic dose, and re-examine in 4 hours", "Perform an immediate closed reduction under regional block to relieve bony pressure"],
            "Pain out of proportion to injury and pain elicited by passive stretching of compartment muscles are the earliest and most reliable signs of acute compartment syndrome. The presence of palpable peripheral pulses does NOT rule out compartment syndrome (pulses disappear only in late/terminal stages). The immediate intervention is to remove all constricting dressings (split cast and padding down to skin) and prepare for emergent surgical fasciotomy.",
            clinical=True
        ),
        q(
            "When assessing compartment syndrome using needle manometry, what delta-P threshold (diastolic blood pressure minus intracompartmental pressure) mandates emergency surgical fasciotomy?",
            "Delta P of 30 mmHg or less",
            ["Delta P of 50 mmHg or less", "Delta P of 70 mmHg or less", "Delta P of 15 mmHg or less"],
            "Tissue perfusion is determined by the pressure gradient between microvascular perfusion pressure and tissue pressure. An absolute compartment pressure > 30-40 mmHg or, more accurately, a delta-P (diastolic blood pressure minus compartment pressure) of 30 mmHg or less indicates critical tissue ischemia and mandates emergency decompression by fasciotomy.",
            clinical=False
        ),
        q(
            "A 22-year-old male sustains closed bilateral femoral fractures. Thirty-six hours after admission, he develops acute confusion, tachypnea (respiratory rate 34/min), PaO2 of 54 mmHg on room air, and petechial hemorrhages across the anterior chest and conjunctivae. What is the diagnosis?",
            "Fat Embolism Syndrome (FES)",
            ["Pulmonary thromboembolism", "Traumatic hypovolemic shock", "Tension pneumothorax"],
            "Fat Embolism Syndrome typically presents 24 to 72 hours following closed long-bone (especially femur) or pelvic fractures. Gurd's diagnostic criteria require at least one major sign and four minor signs, or two major signs. Major signs include: 1. Respiratory insufficiency (tachypnea, PaO2 < 60 mmHg); 2. Neurological depression/confusion; 3. Subconjunctival and axillary/chest petechial rash (pathognomonic, caused by fat emboli occluding dermal capillaries).",
            clinical=True
        ),
        q(
            "What is the fundamental biological distinction between delayed union and non-union of a fracture?",
            "In delayed union, reparative osteogenesis remains active; in non-union, reparative processes have ceased completely",
            ["Delayed union requires immediate bone grafting; non-union heals with simple splinting", "Delayed union is declared at 6 weeks; non-union is strictly defined at 12 weeks for all bones", "Delayed union is always infected; non-union is always aseptic"],
            "Delayed union means the fracture is taking longer than the expected average time to unite for that specific bone, but the fracture gap remains open, vascularity is preserved, and union can still be achieved with continued immobilization. Non-union implies that all reparative processes have ceased, the bone ends have become rounded and sclerotic (or atrophic/tapered), the medullary canal is sealed by bone, and a false joint (pseudoarthrosis) has formed.",
            clinical=False
        ),
        q(
            "A 40-year-old male with an isolated midshaft tibial fracture presents 8 months post-injury with persistent pain on weight-bearing and demonstrable mobility. Radiographs show a persistent radiolucent gap flanked by flared, dense, sclerotic bone ends resembling an 'elephant's foot'. What is the diagnosis and surgical treatment principle?",
            "Hypertrophic non-union; requires rigid mechanical stabilization without mandatory bone grafting",
            ["Atrophic non-union; requires massive autologous cancellous bone grafting with cast immobilization", "Infected non-union; requires radical bone resection and long-term antibiotic beads", "Oligotrophic non-union; requires low-intensity pulsed ultrasound without internal fixation"],
            "Hypertrophic non-union (vascular/elephant-foot) occurs when biological healing potential and blood supply are excellent, but mechanical stability is inadequate (excessive interfragmentary motion). Abundant fibrocartilage forms, producing flared sclerotic ends. Treatment focuses strictly on restoring rigid mechanical stability (e.g., reamed interlocking intramedullary nailing); bone grafting is generally unnecessary.",
            clinical=True
        ),
        q(
            "A 35-year-old female presents 9 months after an open, severely stripped forearm fracture with painless abnormal mobility. Radiographs show pencil-thin, tapered, osteopenic bone ends separated by a wide radiolucent gap with no visible callus. What is the fundamental surgical requirement for this atrophic non-union?",
            "Excision of intervening fibrous tissue, opening sclerosed canals, autologous cancellous bone grafting, and rigid plate fixation",
            ["Application of a tight plaster cast for an additional 6 months to allow osteonal bridging", "Percutaneous injection of bone marrow aspirate without opening the non-union site", "External immobilization and high-frequency ultrasound therapy alone"],
            "Atrophic non-union is characterized by a complete failure of biological osteogenesis and poor vascularity. The bone ends are tapered, rounded, and avascular ('pencil-in-cup' or 'horse's foot'). Treatment requires both biological stimulation (freshening bone ends, opening sclerosed medullary canals, decortication, and autologous cancellous bone grafting) and mechanical stability with rigid plate fixation.",
            clinical=True
        ),
        q(
            "A 48-year-old woman sustains a distal radius fracture treated in a tight cast for 6 weeks. Two weeks after cast removal, she presents with severe burning pain in the hand out of proportion to the original trauma, diffuse hand edema, hyperesthesia, warmth, and finger stiffness. Radiographs show patchy, spotty osteopenia ('ground-glass' osteoporosis). What is the diagnosis?",
            "Complex Regional Pain Syndrome Type I (Sudeck's atrophy)",
            ["Volkmann's Ischaemic Contracture", "Acute suppurative flexor tenosynovitis", "De Quervain's tenosynovitis"],
            "Complex Regional Pain Syndrome Type I (CRPS I), historically known as Sudeck's atrophy or reflex sympathetic dystrophy, is an exaggerated neurovascular and autonomic response to trauma (often minor or following tight cast immobilization). It presents with burning pain, allodynia, hyperpathia, autonomic dysregulation (edema, color and temperature changes), and progressive joint stiffness. Radiographs classically reveal spotty, patchy juxta-articular osteoporosis.",
            clinical=True
        ),
        q(
            "A 14-year-old boy sustains an elbow dislocation that is successfully reduced. His parents take him for vigorous daily massage and forced passive extension exercises. Three weeks later, the elbow is tender and stiff, and radiographs reveal a cloudy mass of new bone forming within the brachialis muscle anterior to the elbow joint. What is the diagnosis and immediate management?",
            "Myositis ossificans traumatica; stop all massage and passive stretching, splint the elbow, and allow the bone mass to mature",
            ["Osteosarcoma of the distal humerus; proceed with emergency wide-margin limb-salvage resection", "Chronic septic arthritis; perform emergency arthrotomy and open synovectomy", "Early Volkmann's contracture; perform emergency forearm flexor fasciotomy"],
            "Myositis ossificans traumatica is heterotopic bone formation within muscle or periarticular soft tissues following trauma, classically occurring in the brachialis muscle after elbow injuries subjected to vigorous massage or forceful passive manipulation. Management requires immediate cessation of massage/passive stretching, resting the joint in a splint until the acute inflammatory phase subsides, followed by active gentle mobilization. Premature excision causes severe recurrence; excision is considered only after the mass has fully matured on radiograph (6-12 months).",
            clinical=True
        ),
        q(
            "What is the earliest and most sensitive imaging modality for detecting avascular necrosis (AVN) of the femoral head following an intracapsular fracture, before plain radiographs show any changes?",
            "Magnetic Resonance Imaging (MRI) demonstrating a low-signal T1 band and 'double-line sign' on T2",
            ["High-resolution CT scan showing subchondral trabecular condensation", "Contrast-enhanced ultrasound showing joint capsule thickening", "Standing pelvic radiograph measuring the acetabular roof index"],
            "MRI is the gold standard and most sensitive diagnostic tool for detecting early avascular necrosis (Ficat-Arlet Stage 0/I), detecting microvascular ischemia weeks to months before plain radiographs show osteopenia, sclerosis, or the 'crescent sign' of subchondral collapse. Classically, MRI demonstrates a serpentine band of low signal intensity on T1-weighted images and the pathognomonic 'double-line sign' on T2-weighted images.",
            clinical=False
        ),
        q(
            "In established Volkmann's Ischaemic Contracture (VIC) of the forearm, what is the classic deformity of the wrist and fingers, and which muscle group is primarily fibrosed?",
            "Wrist flexion, MCP hyperextension, and IP flexion; caused by fibrosis of the deep volar flexors (FDP and FPL)",
            ["Wrist extension, MCP flexion, and IP extension; caused by fibrosis of the extensor digitorum communis", "Radial deviation with thumb adduction contracture; caused by fibrosis of abductor pollicis longus", "Isolated intrinsic hand muscle clawing with completely normal wrist motion"],
            "Volkmann's Ischaemic Contracture is the end-stage cicatricial sequela of untreated compartment syndrome of the forearm. The deep flexor compartment—chiefly Flexor Digitorum Profundus (FDP) and Flexor Pollicis Longus (FPL)—suffers ischemic infarction and turns into inelastic fibrous scar tissue. This produces the classic deformity: wrist flexion, MCP hyperextension, and severe IP flexion. A key sign is that finger extension can be increased only by simultaneously flexing the wrist (Volkmann's sign).",
            clinical=True
        ),
    ]),

    # Chapter 8: Injury to Joints: Dislocation and Subluxation (Easy - 5 questions)
    (8, "Injury to Joints: Dislocation and Subluxation", "easy", [
        q(
            "What is the anatomical distinction between a joint dislocation and a subluxation?",
            "Dislocation is complete loss of articular contact; subluxation is partial loss of contact with some articular apposition remaining",
            ["Dislocation involves an associated bone avulsion; subluxation involves ligamentous sprain only", "Dislocation occurs only in ball-and-socket joints; subluxation occurs only in hinge joints", "Dislocation is congenital in origin; subluxation is exclusively acquired from trauma"],
            "According to standard orthopaedic definitions, a dislocation (luxation) represents complete, total disruption of joint congruity such that the articulating bone surfaces lose all anatomical contact with each other. In a subluxation, there is partial displacement and incongruity, but a portion of the opposing articular cartilages remains in contact.",
            clinical=False
        ),
        q(
            "Why is an acute dislocation of a major joint (such as the hip or knee) an orthopaedic emergency requiring immediate reduction?",
            "Displaced articular ends compress, stretch, or kink adjacent vessels, risking irreversible avascular necrosis or limb ischemia",
            ["Synovial fluid decomposes within 4 hours, causing irreversible chemical chondrolysis", "Periarticular ligaments undergo acute ossification if displaced for more than 6 hours", "The joint capsule closes permanently by primary intention within 12 hours"],
            "Acute joint dislocation is an emergency because the displaced skeletal ends exert direct tension, compression, or kinking on vital periarticular neurovascular structures. For example, in hip dislocation, the retinacular vessels supplying the femoral head are stretched, risking avascular necrosis (the risk escalates dramatically if reduction is delayed > 6 hours); in knee dislocation, popliteal artery occlusion risks limb amputation.",
            clinical=False
        ),
        q(
            "A 20-year-old collegiate gymnast sustains an acute posterolateral elbow dislocation. Following prompt, uncomplicated closed reduction under procedural sedation, what is the mandatory immediate clinical step?",
            "Perform a neurovascular assessment of brachial artery and median/ulnar/radial nerves, followed by post-reduction radiographs",
            ["Apply a circular plaster cast from shoulder to palm for 8 weeks without checking pulses", "Schedule the patient for immediate open capsular reconstruction and ligament repair", "Place the patient in continuous skeletal traction via an olecranon pin for 3 weeks"],
            "Immediately after reducing any dislocation, the surgeon must: 1. Re-evaluate and document neurovascular integrity (e.g., in elbow dislocation, assess radial pulse, capillary refill, and motor/sensory function of median, radial, and ulnar nerves); 2. Obtain orthogonal post-reduction radiographs to confirm concentric reduction and exclude previously obscured fractures; 3. Gently assess range of motion and joint stability to determine the safe arc of movement.",
            clinical=True
        ),
        q(
            "In recurrent anterior dislocation of the shoulder, what pathological lesion consists of an avulsion of the anteroinferior glenoid labrum with the attached inferior glenohumeral ligament?",
            "Bankart lesion",
            ["Hill-Sachs lesion", "SLAP lesion", "Kim's lesion"],
            "A Bankart lesion is the primary essential lesion predisposing to recurrent anterior shoulder instability: it is an avulsion of the anteroinferior glenoid labrum from the glenoid rim, typically accompanied by disruption of the anterior band of the inferior glenohumeral ligament complex (IGHLC). A Hill-Sachs lesion is a compression fracture of the posterolateral humeral head caused by impaction against the hard anterior glenoid rim.",
            clinical=False
        ),
        q(
            "What clinical feature distinguishes recurrent dislocation of the patella from habitual dislocation of the patella in adolescents?",
            "Recurrent dislocation is episodic following trauma or laxity; habitual dislocation occurs obligatorily every time the knee flexes due to vastus lateralis contracture",
            ["Recurrent dislocation dislocates medially; habitual dislocation dislocates laterally", "Recurrent dislocation affects males only; habitual dislocation affects females after skeletal maturity", "Recurrent dislocation is managed by quadriceps release; habitual dislocation requires patellectomy"],
            "Recurrent patellar dislocation is episodic, often starting after an initial traumatic subluxation and recurring during pivoting or twisting movements in patients with underlying predisposing factors (e.g., high Q angle, patella alta, trochlear dysplasia). Habitual patellar dislocation occurs obligatorily and painlessly every time the knee flexes, almost always caused by an abnormal fibrous band or tight contracture of the vastus lateralis / iliotibial band tethering the patella laterally during flexion.",
            clinical=True
        ),
    ]),
]
