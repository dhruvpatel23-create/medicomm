import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Lower Limb"
BASE = {"subjectId": "anatomy", "subjectTitle": "Anatomy", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("introduction", "Introduction and Comparison", [
        q("The lower limb is chiefly specialized for:", "Weight bearing and locomotion", ["Fine prehension", "Respiration", "Protection of thoracic organs"], "The lower limb is adapted for support, balance and movement of the body."),
        q("The anatomical root of the lower limb is attached to the axial skeleton through the:", "Pelvic girdle", ["Pectoral girdle", "Thoracic cage", "Hyoid bone"], "The hip bones transmit body weight from axial skeleton to lower limbs."),
        q("Compared with upper limb, lower limb joints generally favor:", "Stability over mobility", ["Mobility over stability", "No weight transfer", "Only rotation"], "Lower limb joints are shaped and reinforced for support and gait."),
        q("The preaxial border of lower limb corresponds mainly to the:", "Tibial/great-toe side", ["Fibular/little-toe side", "Posterior thigh only", "Gluteal fold"], "Developmentally the preaxial side maps to the tibial and great-toe side."),
        q("The postaxial border of lower limb corresponds mainly to the:", "Fibular/little-toe side", ["Tibial/great-toe side", "Anterior midline", "Inguinal ligament"], "The fibular and little-toe side is postaxial."),
        q("Most lower-limb motor supply comes from branches of:", "Lumbar and sacral plexuses", ["Brachial plexus", "Cervical plexus only", "Intercostal nerves only"], "Lumbosacral plexus branches supply the lower limb."),
        q("The femur is developmentally homologous with the:", "Humerus", ["Radius", "Ulna", "Clavicle"], "Femur and humerus are proximal long bones of lower and upper limbs."),
        q("The tibia corresponds developmentally to the:", "Radius", ["Ulna", "Scapula", "Metacarpal"], "Tibia is the preaxial bone, corresponding to radius."),
        q("The fibula corresponds developmentally to the:", "Ulna", ["Radius", "Humerus", "Sternum"], "Fibula is the postaxial bone, corresponding to ulna."),
        q("Lower-limb dermatomes are clinically used to localize:", "Spinal nerve root lesions", ["Only arterial occlusion", "Only bone age", "Only lymph node disease"], "Dermatomal sensory loss helps identify involved lumbosacral roots."),
        q("A patient with L5 disc prolapse has pain radiating down the lateral leg to dorsum of foot. Which anatomical logic localizes the root?", "Dermatomal pattern of L5", ["Femoral arterial pulse", "Obturator canal anatomy", "Superficial inguinal lymph drainage"], "Radicular pain follows dermatomes; L5 commonly involves lateral leg and dorsum of foot."),
        q("A hip joint is less commonly dislocated than shoulder. Which design principle explains this difference?", "Deep acetabulum and strong ligaments provide stability", ["Femoral head is absent", "Hip has no capsule", "Lower limb is designed mainly for grasping"], "The hip sacrifices some mobility for strong weight-bearing stability."),
        q("During gait, the body weight passes from pelvis to femur and then to tibia. Which feature of lower limb makes this possible?", "Aligned weight-bearing skeleton with strong joints", ["Free-floating pelvic girdle", "Only fibular weight transmission", "Absence of arches"], "Lower-limb bones and joints form a stable column for transmitting body weight."),
        q("A sensory deficit over the great toe is interpreted using limb-axis development. Which side is being tested?", "Preaxial tibial side", ["Postaxial fibular side", "Posterior gluteal side", "Perineal side"], "Great toe and tibial side are preaxial, commonly useful in root localization."),
        q("Why does lower-limb anatomy emphasize surface pulses and compartments in trauma?", "Neurovascular compromise threatens gait and limb viability", ["Lower limb has no collateral vessels", "Muscles are superficial only", "Bones cannot fracture"], "Compartment pressure and vascular injury can rapidly impair function and survival of tissues."),
    ]),
    ("bones-lower-limb", "Bones of Lower Limb", [
        q("The acetabulum is formed by fusion of ilium, ischium and:", "Pubis", ["Sacrum", "Femur", "Coccyx"], "All three hip bones contribute to the acetabulum."),
        q("The head of femur articulates with the:", "Acetabulum", ["Obturator foramen", "Tibial plateau", "Patella"], "Hip joint is formed between femoral head and acetabulum."),
        q("The neck of femur is clinically important because fractures may endanger:", "Retinacular blood supply to femoral head", ["Sciatic nerve in popliteal fossa", "Anterior tibial artery", "Plantar aponeurosis"], "Intracapsular neck fractures can disrupt vessels to the femoral head."),
        q("The greater trochanter belongs to the:", "Femur", ["Tibia", "Fibula", "Talus"], "Greater trochanter is the lateral proximal projection of femur."),
        q("The tibia transmits most body weight because it is:", "The medial large bone of leg", ["A small lateral bone", "Only a sesamoid", "Non-articular proximally"], "Tibia is the main weight-bearing bone of the leg."),
        q("The fibula mainly provides:", "Muscle attachment and ankle stability", ["Primary body-weight transfer", "Hip socket formation", "Patellar articulation"], "Fibula bears little weight but stabilizes lateral ankle and gives attachments."),
        q("The patella is a:", "Sesamoid bone in quadriceps tendon", ["Flat skull bone", "Tarsal bone", "Fibular epiphysis"], "Patella develops within quadriceps tendon and improves leverage."),
        q("The sustentaculum tali is part of the:", "Calcaneus", ["Talus", "Navicular", "Cuboid"], "It supports the head of talus medially."),
        q("The talus transmits body weight from tibia to:", "Calcaneus and forefoot", ["Patella", "Fibular head", "Pubic symphysis"], "Talus is central in weight transmission at ankle and foot."),
        q("The fifth metatarsal tuberosity gives attachment to:", "Fibularis brevis", ["Tibialis anterior", "Adductor longus", "Quadriceps"], "Fibularis brevis inserts at the base of fifth metatarsal."),
        q("An elderly woman falls and cannot bear weight; the affected limb is shortened and laterally rotated. Which fracture is most likely?", "Neck of femur fracture", ["Patella fracture only", "Fibular shaft fracture", "Fifth metatarsal fracture"], "Femoral neck fracture classically produces shortening and lateral rotation due to muscle pull."),
        q("After intracapsular femoral neck fracture, later hip pain is due to avascular necrosis. Which vessel group was compromised?", "Retinacular branches of medial circumflex femoral artery", ["Anterior tibial recurrent arteries", "Inferior gluteal veins", "Dorsalis pedis artery"], "Retinacular vessels, mainly from medial circumflex femoral artery, supply the femoral head."),
        q("A blow to the lateral knee fractures the fibular neck and the patient develops foot drop. Which nerve was injured?", "Common fibular nerve", ["Tibial nerve", "Femoral nerve", "Obturator nerve"], "Common fibular nerve winds around the neck of fibula and is vulnerable there."),
        q("A runner has tenderness over the navicular region and flattening of the medial longitudinal arch. Which bony support has likely failed?", "Talus-navicular-calcaneal alignment", ["Patella-femur alignment", "Fibular head articulation", "Ischial tuberosity"], "The medial arch depends on talus, calcaneus, navicular and supporting ligaments/tendons."),
        q("A twisting injury avulses the base of the fifth metatarsal. Which muscle pull explains the fragment?", "Fibularis brevis insertion", ["Tibialis posterior insertion", "Sartorius insertion", "Adductor magnus insertion"], "Fibularis brevis inserts on the tuberosity of fifth metatarsal and can avulse it."),
    ]),
    ("front-medial-thigh", "Front and Medial Side of Thigh", [
        q("The anterior thigh compartment is supplied mainly by:", "Femoral nerve", ["Obturator nerve", "Tibial nerve", "Common fibular nerve"], "Femoral nerve supplies quadriceps and most anterior thigh muscles."),
        q("Quadriceps femoris inserts through the patellar ligament into:", "Tibial tuberosity", ["Fibular head", "Lesser trochanter", "Ischial tuberosity"], "Quadriceps tendon continues as patellar ligament to tibial tuberosity."),
        q("Sartorius is supplied by:", "Femoral nerve", ["Obturator nerve", "Superior gluteal nerve", "Tibial nerve"], "Sartorius is an anterior compartment muscle."),
        q("Iliopsoas is the chief flexor of:", "Hip joint", ["Knee joint", "Ankle joint", "Subtalar joint"], "Iliopsoas flexes thigh at hip."),
        q("The femoral triangle roof is formed by:", "Fascia lata and superficial fascia", ["Pectineus only", "Adductor magnus", "Hip capsule"], "The roof includes skin, superficial fascia and fascia lata."),
        q("Femoral triangle contents from lateral to medial include:", "Femoral nerve, artery, vein, canal", ["Vein, artery, nerve, canal", "Canal, nerve, artery, vein", "Artery, nerve, vein, canal"], "NAVC is the classic lateral-to-medial order."),
        q("The femoral artery is continuation of:", "External iliac artery", ["Internal iliac artery", "Popliteal artery", "Obturator artery"], "External iliac becomes femoral below inguinal ligament."),
        q("The adductor canal transmits femoral artery, femoral vein and:", "Saphenous nerve", ["Sciatic nerve", "Deep fibular nerve", "Pudendal nerve"], "Saphenous nerve passes through the canal but does not enter popliteal fossa."),
        q("The medial thigh compartment is supplied mainly by:", "Obturator nerve", ["Femoral nerve", "Inferior gluteal nerve", "Common fibular nerve"], "Obturator nerve supplies most adductor muscles."),
        q("Adductor magnus has an adductor part and:", "Hamstring part", ["Quadriceps part", "Thenar part", "Deltoid part"], "Its hamstring part is supplied by tibial division of sciatic nerve."),
        q("A stab wound just below the inguinal ligament causes severe bleeding medial to the femoral nerve. Which vessel is injured?", "Femoral artery", ["Femoral canal", "Great saphenous vein only", "Obturator artery"], "Femoral artery lies between femoral nerve laterally and femoral vein medially in the triangle."),
        q("After pelvic surgery, a patient cannot adduct the thigh and has sensory loss on medial thigh. Which nerve is injured?", "Obturator nerve", ["Femoral nerve", "Sciatic nerve", "Superior gluteal nerve"], "Obturator nerve supplies adductors and medial thigh skin."),
        q("A femoral hernia passes through the femoral canal. Why can it strangulate easily?", "Rigid boundaries of femoral ring", ["Absence of peritoneum", "Wide muscular canal", "Direct opening into hip joint"], "Femoral ring has firm boundaries, so swelling can compromise bowel."),
        q("A patient loses knee jerk after an anterior thigh injury. Which nerve and muscle group are tested?", "Femoral nerve and quadriceps", ["Obturator nerve and adductors", "Tibial nerve and hamstrings", "Deep fibular nerve and dorsiflexors"], "Patellar reflex tests L3-L4 via femoral nerve to quadriceps."),
        q("During adductor canal block, analgesia spreads to medial leg but quadriceps power is mostly preserved. Which nerve is targeted?", "Saphenous nerve", ["Sciatic nerve", "Inferior gluteal nerve", "Common fibular nerve"], "Saphenous nerve is sensory and travels in the adductor canal."),
    ]),
    ("gluteal-region", "Gluteal Region", [
        q("Gluteus maximus is supplied by:", "Inferior gluteal nerve", ["Superior gluteal nerve", "Femoral nerve", "Obturator nerve"], "Inferior gluteal nerve supplies gluteus maximus."),
        q("Gluteus medius and minimus are supplied by:", "Superior gluteal nerve", ["Inferior gluteal nerve", "Tibial nerve", "Pudendal nerve"], "Superior gluteal nerve supplies gluteus medius, minimus and tensor fasciae latae."),
        q("The safest quadrant for intramuscular gluteal injection is:", "Upper outer quadrant", ["Lower inner quadrant", "Lower outer quadrant", "Upper inner quadrant"], "Upper outer quadrant avoids sciatic nerve and major vessels."),
        q("The sciatic nerve usually leaves pelvis through:", "Greater sciatic foramen below piriformis", ["Obturator canal", "Femoral ring", "Lesser sciatic foramen above coccygeus"], "Sciatic nerve exits below piriformis into gluteal region."),
        q("Trendelenburg sign indicates weakness of:", "Gluteus medius and minimus", ["Gluteus maximus only", "Adductor longus", "Hamstrings"], "Hip abductors stabilize pelvis during single-leg stance."),
        q("Gluteus maximus is most active in:", "Rising from sitting and climbing", ["Quiet standing only", "Toe extension", "Knee locking by quadriceps"], "Gluteus maximus powerfully extends hip against resistance."),
        q("Piriformis is a landmark for:", "Gluteal nerves and vessels", ["Femoral triangle contents", "Tarsal tunnel", "Adductor canal"], "Structures leave pelvis above and below piriformis."),
        q("The superior gluteal nerve emerges:", "Above piriformis", ["Below piriformis", "Through femoral canal", "Behind adductor magnus"], "Superior gluteal nerve and vessels pass superior to piriformis."),
        q("The pudendal nerve leaves pelvis below piriformis and enters perineum through:", "Lesser sciatic foramen", ["Femoral ring", "Obturator canal", "Adductor hiatus"], "It hooks around sacrospinous ligament and enters perineum via lesser sciatic foramen."),
        q("Tensor fasciae latae inserts into:", "Iliotibial tract", ["Patellar ligament", "Calcaneal tendon", "Adductor tubercle"], "TFL tightens iliotibial tract and assists hip abduction."),
        q("After a wrongly placed gluteal injection, a patient has radiating posterior thigh pain and foot weakness. Which nerve is likely injured?", "Sciatic nerve", ["Femoral nerve", "Obturator nerve", "Saphenous nerve"], "Inferomedial gluteal injections risk sciatic nerve injury."),
        q("A patient lurches trunk over the affected hip while walking. What is the compensation trying to reduce?", "Abductor moment needed from weak gluteus medius", ["Hamstring tension", "Ankle dorsiflexion", "Patellar tracking"], "Lurching shifts the center of gravity over the stance limb to reduce abductor demand."),
        q("After superior gluteal nerve injury, the pelvis drops on the opposite side during single-leg stance. Why?", "Hip abductors cannot stabilize pelvis", ["Gluteus maximus cannot extend knee", "Adductors are overactive only", "Sciatic nerve loses sensation"], "Gluteus medius/minimus keep the pelvis level when the opposite foot is off the ground."),
        q("A posterior hip dislocation can injure a large nerve behind the joint. Which clinical deficit would you check?", "Sciatic nerve motor and sensory function", ["Median nerve opposition", "Phrenic nerve breathing", "Facial nerve taste"], "Sciatic nerve lies posterior to hip and may be injured in posterior dislocation."),
        q("A patient cannot rise from a chair without pushing on the thighs after pelvic trauma. Which muscle is weak?", "Gluteus maximus", ["Gluteus minimus only", "Pectineus", "Sartorius"], "Gluteus maximus is essential for powerful hip extension from flexed posture."),
    ]),
    ("back-thigh-popliteal", "Back of Thigh and Popliteal Fossa", [
        q("Most hamstrings arise from the:", "Ischial tuberosity", ["Anterior superior iliac spine", "Pubic tubercle", "Lesser trochanter"], "Semitendinosus, semimembranosus and long head of biceps arise from ischial tuberosity."),
        q("Hamstrings are supplied mainly by:", "Tibial division of sciatic nerve", ["Femoral nerve", "Obturator nerve", "Deep fibular nerve"], "Most hamstrings receive tibial division fibers."),
        q("Short head of biceps femoris is supplied by:", "Common fibular division of sciatic nerve", ["Femoral nerve", "Obturator nerve", "Inferior gluteal nerve"], "Short head is the exception among hamstrings."),
        q("Hamstrings extend hip and:", "Flex knee", ["Extend ankle", "Flex toes only", "Abduct shoulder"], "They cross hip and knee except short head of biceps."),
        q("The sciatic nerve usually divides into tibial and common fibular nerves near:", "Superior angle of popliteal fossa", ["Femoral triangle", "Adductor canal", "Tarsal tunnel"], "Division often occurs near the upper popliteal fossa."),
        q("The popliteal fossa is posterior to the:", "Knee joint", ["Hip joint", "Ankle joint", "Subtalar joint"], "It is the diamond-shaped region behind the knee."),
        q("Popliteal artery is continuation of femoral artery after it passes through:", "Adductor hiatus", ["Femoral ring", "Obturator canal", "Greater sciatic foramen"], "Femoral artery enters popliteal fossa through adductor hiatus."),
        q("The deepest important structure in popliteal fossa is:", "Popliteal artery", ["Small saphenous vein", "Tibial nerve", "Skin"], "From superficial to deep: nerve, vein, artery."),
        q("Small saphenous vein usually drains into:", "Popliteal vein", ["Femoral vein at saphenous opening", "Great saphenous vein only", "External iliac vein"], "Small saphenous pierces deep fascia to join popliteal vein."),
        q("Popliteal lymph nodes receive lymph from:", "Lateral foot and deep leg structures", ["Anterior abdominal wall only", "Breast", "Scalp"], "They drain parts of foot/leg and deep lymphatics."),
        q("A posterior thigh stab wound damages the tibial part of sciatic nerve. Which movement is most weakened?", "Knee flexion by most hamstrings", ["Hip adduction only", "Knee extension", "Ankle eversion only"], "Most hamstrings are tibial-division supplied and flex the knee."),
        q("A popliteal aneurysm compresses the tibial nerve. What symptom pattern is expected?", "Pain or weakness in posterior leg and sole", ["Thenar wasting", "Deltoid paralysis", "Loss of shoulder abduction"], "Tibial nerve continues to posterior leg and plantar foot."),
        q("The popliteal pulse is hard to feel in a normal patient. Why?", "Artery lies deep against the femur and capsule", ["It is absent in adults", "It lies in skin", "It is covered by clavicle"], "Popliteal artery is the deepest major fossa content."),
        q("A Baker cyst expands in the popliteal fossa and causes calf swelling. Which joint relation explains it?", "Synovial outpouching from knee region", ["Hip capsule rupture", "Ankle mortise widening", "Femoral canal hernia"], "Popliteal cysts communicate with or arise near the knee joint synovial region."),
        q("During posterior knee dislocation, distal pulses disappear. Which vessel is at greatest risk?", "Popliteal artery", ["Dorsalis pedis artery at foot", "Internal iliac artery", "Great saphenous vein only"], "Popliteal artery is tethered around the knee and vulnerable in dislocation."),
    ]),
    ("leg-dorsum-foot", "Leg and Dorsum of Foot", [
        q("Anterior compartment of leg is supplied by:", "Deep fibular nerve", ["Tibial nerve", "Superficial fibular nerve", "Saphenous nerve"], "Deep fibular nerve supplies dorsiflexors."),
        q("The main action of tibialis anterior is:", "Dorsiflexion and inversion", ["Plantarflexion and eversion", "Knee extension", "Hip flexion"], "Tibialis anterior dorsiflexes ankle and inverts foot."),
        q("Lateral compartment of leg is supplied by:", "Superficial fibular nerve", ["Deep fibular nerve", "Tibial nerve", "Femoral nerve"], "Superficial fibular nerve supplies fibularis longus and brevis."),
        q("Fibularis longus supports mainly the:", "Transverse and lateral arch", ["Thoracic inlet", "Palmar arch", "Pelvic diaphragm"], "Its tendon crosses sole and helps maintain foot arches."),
        q("Posterior compartment of leg is supplied by:", "Tibial nerve", ["Deep fibular nerve", "Obturator nerve", "Femoral nerve"], "Tibial nerve supplies plantarflexors and deep posterior muscles."),
        q("Gastrocnemius and soleus insert through the:", "Calcaneal tendon", ["Patellar ligament", "Iliotibial tract", "Plantar plate"], "The tendo calcaneus inserts on calcaneus."),
        q("The dorsalis pedis artery is continuation of:", "Anterior tibial artery", ["Posterior tibial artery", "Fibular artery", "Femoral artery"], "Anterior tibial becomes dorsalis pedis on dorsum of foot."),
        q("The pulse of dorsalis pedis is palpated lateral to:", "Extensor hallucis longus tendon", ["Achilles tendon", "Patellar tendon", "Flexor digitorum longus tendon"], "Dorsalis pedis lies just lateral to EHL tendon."),
        q("The great saphenous vein begins from the:", "Medial end of dorsal venous arch", ["Lateral end of dorsal venous arch", "Popliteal vein", "Femoral artery"], "Great saphenous ascends anterior to medial malleolus from medial arch."),
        q("The small saphenous vein begins from the:", "Lateral end of dorsal venous arch", ["Medial end of dorsal venous arch", "Femoral vein", "Deep plantar arch"], "Small saphenous passes behind lateral malleolus and up posterior leg."),
        q("A fibular neck fracture causes foot drop and sensory loss over dorsum of foot. Which nerve lesion explains both?", "Common fibular nerve", ["Tibial nerve", "Femoral nerve", "Obturator nerve"], "Common fibular nerve divides into deep and superficial fibular branches for anterior/lateral compartments and dorsum sensation."),
        q("After anterior compartment syndrome, a patient cannot dorsiflex the ankle. Which nerve and muscle group failed?", "Deep fibular nerve to anterior compartment", ["Tibial nerve to calf", "Femoral nerve to quadriceps", "Obturator nerve to adductors"], "Anterior compartment ischemia damages dorsiflexors and deep fibular nerve function."),
        q("A patient catches the toes while walking and lifts the knee high to clear the foot. What gait problem is this?", "Foot drop from dorsiflexor paralysis", ["Trendelenburg gait", "Scissor gait from adductors only", "Locked knee from quadriceps"], "Loss of dorsiflexion produces steppage gait."),
        q("Pain and swelling behind the medial malleolus with numb sole suggests compression in which tunnel?", "Tarsal tunnel", ["Femoral canal", "Adductor canal", "Carpal tunnel"], "Tibial nerve and posterior tibial vessels pass behind medial malleolus beneath flexor retinaculum."),
        q("A weak dorsalis pedis pulse after ankle trauma suggests compromise of which arterial continuation?", "Anterior tibial artery", ["Posterior tibial artery only", "Obturator artery", "Inferior gluteal artery"], "Dorsalis pedis is the distal continuation of anterior tibial artery."),
    ]),
    ("sole-foot", "Sole of Foot", [
        q("The sole is mainly supplied by branches of:", "Tibial nerve", ["Deep fibular nerve", "Femoral nerve", "Obturator nerve"], "Tibial nerve divides into medial and lateral plantar nerves."),
        q("Medial plantar nerve is comparable to the:", "Median nerve in hand", ["Radial nerve", "Axillary nerve", "Intercostal nerve"], "It supplies a similar functional group to median nerve in the hand."),
        q("Lateral plantar nerve is comparable to the:", "Ulnar nerve in hand", ["Median nerve", "Femoral nerve", "Phrenic nerve"], "It supplies most intrinsic muscles of sole like ulnar nerve in hand."),
        q("The plantar aponeurosis supports the:", "Longitudinal arches", ["Shoulder joint", "Thoracic cage", "Elbow joint"], "It acts as a tie-beam for the arches."),
        q("The first muscular layer of sole includes abductor hallucis, flexor digitorum brevis and:", "Abductor digiti minimi", ["Adductor longus", "Tibialis anterior", "Extensor hallucis longus"], "These three form the superficial muscular layer of sole."),
        q("Flexor hallucis longus tendon passes to the:", "Great toe", ["Little toe", "Patella", "Fibular head"], "FHL flexes the great toe."),
        q("Flexor digitorum longus tendons supply:", "Lateral four toes", ["Great toe only", "Heel skin only", "Dorsum of foot"], "FDL flexes toes 2 to 5."),
        q("The lateral plantar artery contributes to:", "Deep plantar arch", ["Femoral triangle", "Popliteal fossa", "Dorsal venous arch only"], "Lateral plantar artery forms most of the deep plantar arch."),
        q("Medial longitudinal arch is supported dynamically by:", "Tibialis posterior and flexor hallucis longus", ["Deltoid only", "Biceps femoris", "Pectoralis major"], "Tendons crossing the sole support the arch during gait."),
        q("The spring ligament supports the:", "Head of talus", ["Neck of femur", "Patella", "Fibular neck"], "Plantar calcaneonavicular ligament supports talar head."),
        q("A patient has burning pain in the sole after compression behind the medial malleolus. Which nerve is compressed?", "Tibial nerve", ["Common fibular nerve", "Femoral nerve", "Saphenous nerve"], "Tibial nerve passes through tarsal tunnel and supplies the sole."),
        q("Plantar fasciitis causes sharp heel pain on first steps in the morning. Which structure is inflamed?", "Plantar aponeurosis near calcaneal attachment", ["Dorsal venous arch", "Patellar ligament", "Iliotibial tract"], "The plantar fascia attaches to calcaneal tuberosity and supports the arch."),
        q("A diabetic ulcer under the first metatarsal head threatens which functional support area?", "Medial forefoot weight-bearing point", ["Non-weight-bearing dorsum", "Patellar surface", "Fibular neck"], "Weight passes through heel and metatarsal heads, especially medial forefoot during push-off."),
        q("A collapse of the medial arch stretches the spring ligament. Which bone loses its sling-like support?", "Talus", ["Patella", "Femur", "Fibula"], "The spring ligament forms a support for the head of talus."),
        q("Injury to lateral plantar nerve causes weak interossei and loss of toe adduction/abduction. Why is the deficit broad?", "It supplies most intrinsic sole muscles", ["It supplies only skin", "It is a branch of femoral nerve", "It controls quadriceps"], "Lateral plantar nerve is the major motor nerve of intrinsic foot muscles."),
    ]),
    ("joints-lower-limb", "Joints of Lower Limb", [
        q("The hip joint is a:", "Ball-and-socket synovial joint", ["Hinge joint", "Pivot joint", "Fibrous joint"], "Hip is multiaxial but strongly stabilized."),
        q("The strongest ligament of hip joint is:", "Iliofemoral ligament", ["Annular ligament", "Coracoacromial ligament", "Transverse humeral ligament"], "Iliofemoral ligament resists hyperextension and supports standing."),
        q("The knee joint is primarily a:", "Modified hinge synovial joint", ["Saddle joint", "Pivot joint only", "Suture"], "Knee permits flexion-extension with rotation when flexed."),
        q("The medial meniscus is more commonly injured because it is attached to:", "Tibial collateral ligament", ["Fibular collateral ligament", "Patellar ligament only", "Anterior cruciate only"], "Medial meniscus is less mobile due to attachment to MCL."),
        q("Anterior cruciate ligament prevents:", "Anterior translation of tibia on femur", ["Posterior translation only", "Hip abduction", "Ankle eversion"], "ACL checks anterior displacement of tibia and hyperextension."),
        q("Posterior cruciate ligament prevents:", "Posterior translation of tibia on femur", ["Anterior translation only", "Patellar tracking", "Subtalar inversion"], "PCL is the main restraint to posterior tibial displacement."),
        q("The locking of knee in terminal extension is produced mainly by:", "Medial rotation of femur on tibia in weight bearing", ["Lateral rotation of patella", "Dorsiflexion of ankle", "Toe flexion"], "Screw-home mechanism locks the extended knee."),
        q("Unlocking of knee is initiated by:", "Popliteus", ["Soleus", "Adductor longus", "Gluteus maximus"], "Popliteus laterally rotates femur or medially rotates tibia to unlock knee."),
        q("The ankle joint is a:", "Hinge synovial joint", ["Ball-and-socket joint", "Saddle joint", "Plane fibrous joint"], "Ankle permits dorsiflexion and plantarflexion."),
        q("Inversion and eversion occur mainly at:", "Subtalar and transverse tarsal joints", ["Hip joint only", "Knee hinge only", "Tibiofibular syndesmosis only"], "Intertarsal joints permit foot inversion and eversion."),
        q("A footballer twists a flexed knee and tears ACL with medial meniscus injury. Which test becomes positive?", "Anterior drawer/Lachman test", ["Posterior drawer only", "Trendelenburg test", "Tinel sign at wrist"], "ACL rupture allows excessive anterior translation of tibia."),
        q("A dashboard injury drives the tibia posteriorly. Which ligament is most likely torn?", "Posterior cruciate ligament", ["Anterior cruciate ligament", "Iliofemoral ligament", "Deltoid ligament"], "PCL resists posterior displacement of tibia and is injured in dashboard trauma."),
        q("A swollen knee after lateral blow shows medial joint-line pain and valgus instability. Which structures are at risk?", "Tibial collateral ligament and medial meniscus", ["Fibular collateral ligament only", "Achilles tendon", "Plantar fascia"], "Valgus stress injures MCL, and attached medial meniscus may tear."),
        q("An ankle sprain after forced inversion most often injures which ligament first?", "Anterior talofibular ligament", ["Deltoid ligament", "Posterior cruciate ligament", "Iliofemoral ligament"], "Lateral ligament, especially ATFL, is commonly injured in inversion sprains."),
        q("A patient with knee locked in extension cannot start flexion. Which small posterior muscle is failing?", "Popliteus", ["Sartorius", "Tibialis anterior", "Fibularis longus"], "Popliteus unlocks the knee by initiating rotation before flexion."),
    ]),
    ("arteries-veins-lymph", "Arteries, Veins and Lymphatics", [
        q("The femoral artery enters the thigh behind the:", "Inguinal ligament", ["Piriformis", "Adductor hiatus", "Medial malleolus"], "External iliac artery becomes femoral behind inguinal ligament."),
        q("The profunda femoris artery is the chief artery of:", "Thigh", ["Sole only", "Anterior abdominal wall", "Pelvic diaphragm only"], "Deep artery of thigh supplies most thigh musculature."),
        q("Medial circumflex femoral artery is important for supply to:", "Femoral head and neck", ["Dorsum of foot only", "Patella only", "Skin of sole only"], "It gives retinacular branches to femoral head."),
        q("Femoral artery becomes popliteal artery after passing through:", "Adductor hiatus", ["Femoral canal", "Obturator canal", "Tarsal tunnel"], "The vessel changes name at the adductor hiatus."),
        q("Popliteal artery divides into:", "Anterior and posterior tibial arteries", ["Radial and ulnar arteries", "Medial and lateral plantar nerves", "Femoral and obturator arteries"], "Terminal branches supply leg and foot."),
        q("Posterior tibial artery divides into:", "Medial and lateral plantar arteries", ["Dorsalis pedis and arcuate", "Femoral and popliteal", "Obturator and gluteal"], "It enters sole and divides into plantar arteries."),
        q("Great saphenous vein drains into:", "Femoral vein", ["Popliteal vein", "External iliac artery", "Portal vein"], "It pierces cribriform fascia at saphenous opening."),
        q("Small saphenous vein drains into:", "Popliteal vein", ["Femoral vein directly", "Internal iliac vein", "Deep plantar arch"], "It ascends posterior leg to the popliteal vein."),
        q("Superficial inguinal nodes drain most superficial lymph from:", "Lower limb below umbilicus region", ["Deep thorax", "Brain", "Lungs only"], "They receive superficial lymph from lower limb and lower anterior abdominal wall."),
        q("Deep inguinal nodes include the node of:", "Cloquet", ["Virchow", "Rotter", "Delphian"], "Cloquet node lies in femoral canal."),
        q("A femoral pulse is compressed midway between ASIS and pubic symphysis. Which vessel is being controlled?", "Femoral artery", ["Popliteal artery", "Posterior tibial artery", "Dorsalis pedis artery"], "Femoral artery is palpable in femoral triangle below inguinal ligament."),
        q("A patient with femoral neck fracture later develops avascular necrosis. Which artery is most relevant?", "Medial circumflex femoral artery", ["Dorsalis pedis artery", "Anterior tibial artery", "Small saphenous vein"], "Retinacular branches of medial circumflex femoral artery are critical."),
        q("Varicose veins along the medial leg involve the long superficial vein. Where does it terminate?", "Femoral vein at saphenous opening", ["Popliteal vein", "Posterior tibial artery", "Obturator vein"], "Great saphenous vein ascends medially and joins femoral vein."),
        q("A malignant lesion on the lateral heel first enlarges nodes in the popliteal fossa. Which lymph route explains it?", "Small saphenous territory to popliteal nodes", ["Great saphenous territory to axillary nodes", "Thoracic duct directly", "Deep cervical route"], "Lateral foot and heel lymph may follow small saphenous vein to popliteal nodes."),
        q("Absent dorsalis pedis pulse with preserved posterior tibial pulse suggests disease in which artery?", "Anterior tibial artery", ["Posterior tibial artery only", "Femoral vein", "Obturator artery"], "Dorsalis pedis is the continuation of anterior tibial artery."),
    ]),
    ("surface-radiological", "Surface Marking and Radiological Anatomy", [
        q("The midpoint of inguinal ligament lies between ASIS and:", "Pubic tubercle", ["Ischial spine", "Coccyx", "Medial malleolus"], "The inguinal ligament runs from ASIS to pubic tubercle."),
        q("The mid-inguinal point lies between ASIS and:", "Pubic symphysis", ["Pubic tubercle", "Ischial tuberosity", "Greater trochanter"], "Femoral artery is marked at the mid-inguinal point."),
        q("Femoral artery pulse is felt at:", "Mid-inguinal point", ["Behind lateral malleolus", "Over fibular neck", "At xiphisternum"], "It lies just below inguinal ligament in femoral triangle."),
        q("Popliteal pulse is best felt with knee:", "Flexed to relax fascia", ["Fully locked in extension", "Hyperextended forcefully", "Abducted at shoulder"], "Flexion relaxes popliteal fascia and hamstrings."),
        q("Posterior tibial pulse is palpated:", "Behind medial malleolus", ["In femoral triangle", "Over patella", "Behind lateral epicondyle of humerus"], "Posterior tibial artery passes behind medial malleolus."),
        q("Dorsalis pedis pulse is palpated on:", "Dorsum of foot lateral to EHL tendon", ["Sole medial to heel", "Popliteal fossa", "Femoral canal"], "Dorsalis pedis lies lateral to extensor hallucis longus."),
        q("The sciatic nerve surface line runs from gluteal region toward:", "Midpoint of posterior thigh", ["Femoral triangle", "Dorsum of great toe", "Anterior abdominal wall"], "It descends deep in posterior thigh."),
        q("The head of fibula is palpated:", "Inferolateral to knee", ["Medial to pubic tubercle", "Behind medial malleolus", "At femoral head"], "Fibular head is a lateral knee landmark."),
        q("On AP pelvis X-ray, Shenton line assesses alignment between:", "Inferior femoral neck and superior pubic ramus", ["Patella and tibia", "Talus and calcaneus", "Fibula and fifth metatarsal"], "Broken Shenton line suggests hip fracture/dislocation."),
        q("On knee X-ray, patella is best profiled on:", "Lateral view", ["AP chest view", "Oblique wrist view", "Skull base view"], "Lateral knee view shows patellar position and effusion signs."),
        q("A trauma X-ray shows broken Shenton line and shortened externally rotated limb. Which diagnosis is most likely?", "Fracture neck of femur", ["Anterior shoulder dislocation", "Scaphoid fracture", "Rib fracture"], "Broken Shenton line with classic limb posture suggests femoral neck fracture."),
        q("A clinician checks posterior tibial pulse after ankle fracture. Which compartment's distal blood flow is being assessed?", "Posterior compartment/plantar foot supply", ["Anterior chest wall", "Upper limb", "Femoral head only"], "Posterior tibial artery supplies posterior leg and sole through plantar arteries."),
        q("A patient with common fibular nerve palsy is tapped near the fibular neck. Why this surface point?", "The nerve winds superficially around fibular neck", ["The femoral nerve exits there", "The tibial nerve becomes subcutaneous there", "The obturator nerve crosses there"], "Common fibular nerve is palpable/vulnerable at fibular neck."),
        q("A compartment syndrome check focuses on pain with passive toe stretch. Which anatomical fact makes this urgent?", "Tight fascial compartments can compress nerves and arteries", ["Leg compartments are open spaces", "Only skin is involved", "Bone marrow drains pressure"], "Deep fascia creates closed compartments where swelling can cut off perfusion."),
        q("On foot examination, loss of medial arch is assessed from the side during standing. Which structure is central to the arch summit?", "Talus", ["Patella", "Fibular head", "Greater trochanter"], "Talus sits at the summit of the medial longitudinal arch."),
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
                "id": f"anatomy-lower-limb-{slug}-{question_index:02d}",
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
    if any(len(q["prompt"].split()) < 10 for q in questions if q["difficulty"] == "very high"):
        raise AssertionError("Clinical prompts should be vignette-style")
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
