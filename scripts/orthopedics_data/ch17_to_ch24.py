from .common import q

CHAPTERS = [
    # Chapter 17: Pelvic Fractures (HARD - 10 questions)
    (17, "Pelvic Fractures", "hard", [
        q(
            "A 36-year-old male is brought to the emergency department after a vehicular collision with hypotension (BP 80/50 mmHg). AP pelvic radiograph shows 3.5 cm separation of the pubic symphysis ('open-book' pelvis) with disruption of anterior sacroiliac ligaments, but posterior sacroiliac ligaments are intact. According to the Young-Burgess classification, this is",
            "Anteroposterior Compression Type II (APC-II)",
            ["Anteroposterior Compression Type I (APC-I)", "Lateral Compression Type I (LC-I)", "Vertical Shear (VS)"],
            "The Young-Burgess classification categorizes pelvic ring injuries based on force vector: Anteroposterior Compression (APC), Lateral Compression (LC), and Vertical Shear (VS). In APC-I, pubic diastasis is < 2.5 cm with intact SI ligaments. In APC-II, diastasis is > 2.5 cm with disruption of anterior SI, sacrotuberous, and sacrospinous ligaments (rotationally unstable, vertically stable). In APC-III, there is complete disruption of anterior and posterior SI ligaments with total hemipelvis dissociation.",
            clinical=True
        ),
        q(
            "In Tile's classification of pelvic ring fractures, what fundamental biomechanical difference distinguishes a Type B injury from a Type C injury?",
            "Type B is rotationally unstable but vertically stable; Type C is both rotationally and vertically unstable",
            ["Type B involves isolated acetabular fractures; Type C involves iliac wing fractures", "Type B fractures are open; Type C fractures are strictly closed", "Type B involves visceral injury; Type C has no visceral involvement"],
            "Tile's classification is based on pelvic ring integrity: Tile A is stable (isolated avulsions or non-displaced ring breaks); Tile B is rotationally unstable but vertically stable because the strong posterior sacroiliac tension band complex is partially preserved (includes open-book and lateral compression injuries); Tile C is completely unstable—both rotationally and vertically—due to total disruption of the posterior sacroiliac ligamentous complex and pelvic floor.",
            clinical=False
        ),
        q(
            "A 28-year-old male with an unstable pelvic fracture has blood at the urethral meatus, a distended bladder, and a high-riding prostate on rectal examination. What diagnostic test must be performed before any transurethral catheterization?",
            "Retrograde urethrography (RUG)",
            ["Diagnostic peritoneal lavage", "Intravenous pyelography", "Immediate 18-Fr Foley catheter insertion"],
            "The triad of blood at the urethral meatus, high-riding prostate on DRE, and inability to void strongly indicates an acute traumatic posterior urethral rupture (membranous urethra disruption above the urogenital diaphragm). Blind catheterization is strictly contraindicated as it can convert a partial tear into a complete transection or introduce infection into a pelvic hematoma. A retrograde urethrogram (RUG) must be performed first.",
            clinical=True
        ),
        q(
            "What is the source of life-threatening hemorrhage in approximately 85% to 90% of hemodynamically unstable pelvic ring fractures?",
            "Presacral venous plexus, perivesical veins, and bleeding from cancellous fracture surfaces",
            ["Transection of the common iliac artery", "Rupture of the inferior mesenteric artery", "Laceration of the external iliac vein"],
            "In 85% to 90% of pelvic fractures with severe hemorrhagic shock, the primary source of bleeding is the extensive low-pressure presacral, perivesical, and internal iliac venous plexuses, combined with copious bleeding from raw cancellous fracture surfaces. Major arterial lacerations (most commonly superior gluteal, internal pudendal, or obturator arteries) account for only 10-15% of life-threatening pelvic bleeding.",
            clinical=False
        ),
        q(
            "Following high-energy pelvic crush trauma, a patient develops a large, fluctuant, non-pulsatile closed fluid collection over the greater trochanter and flank where hypodermis has sheared off deep fascia. What is this lesion termed?",
            "Morel-Lavallée lesion",
            ["Destot's hematoma", "Earle's collection", "Guttering of the iliacus"],
            "A Morel-Lavallée lesion is a severe closed traumatic degloving injury where high-energy tangential shearing forces tear the skin and subcutaneous tissue from the underlying deep muscle fascia. The resulting potential space fills with blood, lymph, and liquefied necrotic subcutaneous fat. Because of ischemia and avascularity, it has an extraordinarily high infection rate (up to 30-50%) and requires aspiration, percutaneous debridement, or open drainage with compression.",
            clinical=True
        ),
        q(
            "In a patient with suspected pelvic trauma, what does the clinical finding termed 'Destot's sign' represent?",
            "Superficial hematoma above the inguinal ligament or in the scrotum/perineum",
            ["Loss of anal sphincter tone associated with coccygeal injury", "Asymmetric elevation of the iliac crest on the injured side", "Audible bone crepitus on manual pelvic compression"],
            "Destot's sign is the appearance of a hematoma or ecchymosis superficial to the inguinal ligament, over the scrotum or labia majora, or in the upper thigh. It occurs when retroperitoneal blood from a disrupted pelvic ring or fracture of the pubic rami tracks along fascial planes through the inguinal canal or femoral sheath into the superficial perineal tissues.",
            clinical=False
        ),
        q(
            "A patient involved in a fall from a height of 30 feet sustains a Vertical Shear (Tile C) pelvic fracture. What is the clinical hallmark of this injury on physical examination?",
            "Limb shortening with vertical displacement and gross instability to axial load",
            ["Inward collapse of anterior pelvic ring with bilateral acetabular protrusion", "Isolated pubic symphysis widening with completely stable posterior ring", "Isolated avulsion of the anterior superior iliac spine"],
            "Vertical shear fractures result from extreme axial loading (e.g., fall landing on an extended leg). All anterior (pubic rami or symphysis) and posterior (sacroiliac joint, sacrum, or ilium) structural restraints are completely torn. The hemipelvis displaces cranially and vertically, producing marked true and apparent limb shortening, pelvic asymmetry, gross rotational and vertical instability, and massive retroperitoneal bleeding.",
            clinical=True
        ),
        q(
            "What is the immediate, life-saving bedside stabilization for a hemodynamically unstable open-book pelvic fracture in the resuscitation bay?",
            "Application of a pelvic circumferential binder centered over the greater trochanters",
            ["Immediate emergency laparotomy to pack the retroperitoneal space", "Distal femoral skeletal traction with 15 kg weights", "Emergency open symphysis plating in the trauma bay"],
            "The immediate priority in open-book pelvic fractures is 'closing the pelvic volume' to promote retroperitoneal tamponade and control venous hemorrhage. A commercial pelvic binder (or bedsheet) must be applied immediately around the pelvis, centered specifically over the greater trochanters (NOT over the iliac crests). This compresses the disrupted pelvis, closes the diastasis, and reduces internal pelvic volume.",
            clinical=True
        ),
        q(
            "When assessing an acetabular fracture with 45-degree Judet oblique views, what structures are profiled on the Obturator Oblique view versus the Iliac Oblique view?",
            "Obturator Oblique profiles anterior column and posterior wall; Iliac Oblique profiles posterior column and anterior wall",
            ["Obturator Oblique profiles posterior column; Iliac Oblique profiles posterior wall only", "Obturator Oblique profiles iliac crest; Iliac Oblique profiles ischial tuberosity", "Both views visualize only the femoral head articular surface"],
            "The Judet views are 45-degree oblique pelvic radiographs: 1. Obturator Oblique view (injured side rolled 45 degrees up) profiles the obturator foramen, clearly demonstrating the Anterior Column and the Posterior Wall of the acetabulum; 2. Iliac Oblique view (injured side rolled 45 degrees down) profiles the iliac wing, clearly demonstrating the Posterior Column and the Anterior Wall of the acetabulum.",
            clinical=False
        ),
        q(
            "What clinical finding constitutes 'Earle's sign' on rectal examination in pelvic trauma?",
            "Palpable bony step-off or tender hematoma along the lateral pelvic sidewall",
            ["Absence of the bulbocavernosus reflex", "Bright red blood coating the glove from an anal fissure", "Empty acetabular socket due to anterior hip dislocation"],
            "Earle's sign is elicited on digital rectal examination in pelvic trauma: the examining finger palpates a sharp bony spike, displaced fracture fragment, or a large, tender, tense hematoma along the lateral wall of the pelvis or ischial spine, providing clinical confirmation of pelvic ring or acetabular column disruption.",
            clinical=False
        ),
    ]),

    # Chapter 18: Injuries Around the Hip (HARD - 10 questions)
    (18, "Injuries Around the Hip", "hard", [
        q(
            "A 76-year-old woman presents after a slip and fall. The injured right limb is shortened by 2 cm and held in 30 to 40 degrees of external rotation. Radiographs reveal a completely displaced transcervical femoral neck fracture with disrupted trabeculae. According to Garden's classification, this is",
            "Garden Type III",
            ["Garden Type I", "Garden Type II", "Garden Type IV"],
            "Garden's classification is based on displacement of femoral neck trabeculae: Type I is an incomplete or impacted valgus fracture; Type II is a complete but non-displaced fracture (trabecular lines aligned); Type III is a complete fracture with partial displacement (trabeculae of femoral head are mismatched with acetabular trabeculae, tilting into varus); Type IV is a completely displaced fracture where head trabeculae align normally with acetabular trabeculae because head has regained anatomical orientation in the socket.",
            clinical=True
        ),
        q(
            "A 26-year-old male motorcyclist sustains a displaced femoral neck fracture. Why is emergency anatomical reduction and rigid internal fixation indicated within 24 hours?",
            "To relieve capsular tamponade, restore retinacular blood flow, and prevent avascular necrosis",
            ["To prevent malignant transformation of metaphyseal marrow", "To eliminate the need for postoperative non-weight-bearing", "Because femoral neck fractures in young adults cannot unite after 24 hours"],
            "In young active patients (<60 years), preserving the native femoral head is paramount. The retinacular vessels (branches of the medial femoral circumflex artery) supplying the head are severely compromised by displacement, torsion, and intracapsular hematoma tamponade. Urgent anatomical reduction (closed or open) and rigid internal fixation with cannulated cancellous screws within 6-24 hours restores perfusion and reduces the risk of AVN and non-union.",
            clinical=True
        ),
        q(
            "Pauwels' classification of femoral neck fractures is based on the angle of the fracture line relative to the horizontal. Why does a Pauwels Type III fracture (>50 degrees) have the highest non-union rate?",
            "High vertical angle converts axial loading into powerful shear forces that displace fragments",
            ["The fracture line lies entirely outside the joint capsule away from synovial nutrition", "The fracture damages the sciatic nerve within the greater sciatic notch", "The steep angle prevents any penetration by metallic cannulated screws"],
            "Pauwels classified femoral neck fractures by the angle of the fracture line with the horizontal: Type I is <30 degrees; Type II is 30 to 50 degrees; Type III is >50 degrees. In Type I, axial weight-bearing produces compressive forces that favor union. In Type III, the near-vertical orientation subjects the fracture to powerful shear forces during weight-bearing that tend to slide the fragments apart, leading to non-union and screw cutout.",
            clinical=False
        ),
        q(
            "How does the clinical attitude of the lower limb in an intertrochanteric fracture characteristically differ from that in an intracapsular femoral neck fracture?",
            "Intertrochanteric fractures display marked external rotation (up to 90 degrees); neck fractures display moderate external rotation (30-40 degrees)",
            ["Intertrochanteric fractures are locked in internal rotation; neck fractures are externally rotated", "Intertrochanteric fractures show limb lengthening; neck fractures show shortening", "Both fractures present with identical degrees of rotation and shortening"],
            "In intracapsular femoral neck fractures, external rotation is limited to 30-40 degrees because the strong, unruptured iliofemoral ligament (ligament of Bigelow) and intact joint capsule restrain excessive rotation. In intertrochanteric fractures, the fracture is extracapsular, entirely outside the joint capsule; with no capsular restraint, the distal limb falls into complete external rotation of nearly 90 degrees, with the lateral border of the foot resting flat against the bed.",
            clinical=True
        ),
        q(
            "What biological factor explains why intertrochanteric fractures unite readily, whereas intracapsular femoral neck fractures have high rates of non-union and avascular necrosis?",
            "Intertrochanteric fractures involve vascular cancellous bone with intact periosteum; neck fractures lack periosteum and rely on fragile retinacular vessels",
            ["Intertrochanteric fractures are nourished directly by the ligamentum teres artery", "Femoral neck fractures undergo immediate osteoclastic resorption within 48 hours", "Intertrochanteric bone is entirely composed of compact cortical bone"],
            "The trochanteric region is extracapsular, consisting of wide porous cancellous bone with an abundant blood supply from surrounding muscular attachments (glutei, vastus lateralis); it forms abundant external periosteal and internal callus and unites reliably. The femoral neck is intracapsular, lacks a periosteal cambium layer (heals solely by internal endosteal union), is dependent on the retinacular vessels easily torn by trauma, and is bathed in synovial fluid containing collagenases that dissolve the fracture hematoma.",
            clinical=False
        ),
        q(
            "A 28-year-old front-seat passenger in a car crash hits his flexed knee against the dashboard. On presentation, the affected limb is held in flexion, adduction, and internal rotation, with shortening. What is the diagnosis?",
            "Posterior dislocation of the hip joint",
            ["Anterior dislocation of the hip joint (obturator type)", "Anterior dislocation of the hip joint (pubic type)", "Displaced transcervical femoral neck fracture"],
            "Posterior hip dislocation accounts for 85-90% of all hip dislocations, classically occurring in 'dashboard injuries' where direct axial force strikes the flexed knee, driving the femoral head backward out of the acetabulum. The clinical hallmark is pathognomonic: the limb is held in flexion, adduction, internal rotation, and shortening. The femoral head is palpable in the gluteal region.",
            clinical=True
        ),
        q(
            "In posterior dislocation of the hip, which nerve is at greatest risk of stretch, contusion, or laceration?",
            "Sciatic nerve (especially peroneal division)",
            ["Femoral nerve", "Obturator nerve", "Superior gluteal nerve"],
            "The sciatic nerve emerges from the greater sciatic foramen and courses immediately behind the posterior wall of the acetabulum and posterior capsule. During posterior hip dislocation, the displaced femoral head stretches or compresses the nerve in 10-15% of cases. The peroneal division of the sciatic nerve is most vulnerable due to its lateral, superficial location and relative fixation at the fibular neck, manifesting as foot drop and numbness over the dorsum of the foot.",
            clinical=False
        ),
        q(
            "A patient presents following an extreme abduction and external rotation injury of the hip. The lower limb is held in flexion, abduction, and external rotation, with a prominent bulge palpable in the groin. What is the diagnosis?",
            "Anterior dislocation of the hip (obturator type)",
            ["Posterior dislocation of the hip", "Central dislocation of the hip", "Fracture of the greater trochanter"],
            "Anterior dislocation of the hip accounts for ~10-15% of hip dislocations and occurs when the hip is forced into violent abduction, external rotation, and extension/flexion. The clinical posture is the exact opposite of posterior dislocation: the limb is abducted, externally rotated, slightly flexed, and appears lengthened. In the obturator type, the head is displaced anteroinferiorly near the obturator foramen.",
            clinical=True
        ),
        q(
            "What is the pathoanatomy defining a central dislocation (central fracture-dislocation) of the hip?",
            "Fracture of the medial acetabular wall and quadrilateral plate with intrapelvic protrusion of the femoral head",
            ["Dislocation of the femoral head anterior to the pubic ramus with intact acetabulum", "Complete avulsion of the ligamentum teres without bony fracture", "Extrusion of the femoral head through the greater sciatic notch"],
            "Central dislocation of the hip is always a fracture-dislocation caused by a direct blow to the lateral aspect of the greater trochanter (or axial load along an abducted femur). The force drives the femoral head medially, fracturing the quadrilateral plate and thin medial wall of the acetabulum and intruding the femoral head directly into the pelvic cavity.",
            clinical=False
        ),
        q(
            "What is the maneuver described by Allis for closed reduction of a posterior hip dislocation?",
            "Patient supine, pelvis stabilized, upward longitudinal traction applied in line of deformity with hip/knee flexed at 90 degrees",
            ["Patient prone with leg dangling and 20 kg traction applied to the ankle", "Forced hyperabduction and external rotation followed by adduction across the midline", "Straight-leg axial traction while pushing the femoral head laterally through the groin"],
            "The Allis technique for reducing posterior hip dislocation: 1. Patient supine on the floor/firm stretcher; 2. An assistant stabilizes the pelvis with downward pressure on both anterior superior iliac spines; 3. The surgeon flexes the hip and knee to 90 degrees and applies firm, steady upward vertical traction in the axis of the femur; 4. Gentle adduction and internal/external rotation are applied until a palpable 'clunk' confirms concentric reduction.",
            clinical=False
        ),
    ]),

    # Chapter 19: Fracture Shaft of Femur (Easy - 5 questions)
    (19, "Fracture Shaft of Femur", "easy", [
        q(
            "In a subtrochanteric fracture of the femur, what characteristic displacement forces act on the proximal fragment?",
            "Flexion by iliopsoas, abduction by gluteus medius, and external rotation by short rotators",
            ["Extension by gluteus maximus and adduction by pectineus", "Internal rotation by tensor fasciae latae and adduction by gracilis", "Neutral alignment due to balanced sleeve of vastus intermedius"],
            "In proximal femoral shaft/subtrochanteric fractures: 1. The proximal fragment is pulled into flexion by the iliopsoas, abduction by the gluteus medius and minimus, and external rotation by the piriformis and obturators; 2. The distal fragment is drawn medially (adducted) by the adductor magnus and pulled proximally (shortened) by the long hamstrings and rectus femoris.",
            clinical=True
        ),
        q(
            "In the Winquist-Hansen classification of femoral shaft fractures, what defines a Type III comminuted fracture?",
            "Comminution involving more than 50% of the cortical circumference with loss of cortical contact",
            ["Comminution involving less than 25% of cortical width", "Comminution between 25% and 50% with intact cortical contact remaining", "Complete segmental bone loss with an open gap"],
            "The Winquist-Hansen classification grades comminution: Type I: minimal or no comminution (small butterfly <25%); Type II: butterfly fragment involving up to 50% of bone circumference, with >50% cortical contact between main fragments; Type III: comminution >50% of circumference with loss of cortical contact between main fragments; Type IV: complete segmental comminution with zero cortical contact.",
            clinical=False
        ),
        q(
            "What is the typical estimated internal blood loss associated with a closed, displaced femoral shaft fracture in an adult?",
            "1000 to 1500 mL",
            ["100 to 250 mL", "300 to 500 mL", "3000 to 4000 mL"],
            "A closed fracture of the femoral shaft can easily cause occult internal hemorrhage of 1000 to 1500 mL (1 to 1.5 L) into the surrounding thigh compartments without external blood loss. In bilateral femur fractures, occult bleeding can exceed 2.5 to 3 liters, leading to profound hypovolemic shock if not recognized and resuscitated promptly.",
            clinical=False
        ),
        q(
            "In a supracondylar fracture of the distal femur, which muscle pulls the distal fragment into posterior angulation, endangering the popliteal artery?",
            "Gastrocnemius",
            ["Quadriceps femoris", "Biceps femoris", "Sartorius"],
            "In distal femoral/supracondylar fractures, the gastrocnemius muscle originates from the posterior surface of the medial and lateral femoral condyles. Its powerful contraction tilts the distal condylar fragment into sharp posterior angulation (hyperextension of the fragment), which can directly impinge against, compress, or lacerate the popliteal artery within the tight popliteal fossa.",
            clinical=False
        ),
        q(
            "A 32-year-old male with a closed midshaft femoral fracture is hemodynamically stable. What is the surgical gold standard treatment?",
            "Closed reamed locked intramedullary interlocking nailing",
            ["Open reduction and broad dynamic compression plate (DCP) fixation", "Skeletal traction via a proximal tibial pin for 12 weeks", "Spanning external ring fixator across hip and knee"],
            "Closed reamed locked intramedullary interlocking nailing is the gold-standard treatment for femoral shaft fractures. Operating without opening the fracture site preserves osteogenic fracture hematoma and periosteal vascularity, provides load-sharing biomechanical support, resists bending and rotational stresses, and achieves union rates > 98% with low infection rates.",
            clinical=True
        ),
    ]),

    # Chapter 20: Injuries Around the Knee (HARD - 10 questions)
    (20, "Injuries Around the Knee", "hard", [
        q(
            "A 21-year-old football player hears an audible 'pop' during a sudden deceleration and twisting motion, developing rapid tense knee hemarthrosis within 2 hours. Lachman testing demonstrates increased anterior translation with a soft endpoint. What is the diagnosis?",
            "Anterior Cruciate Ligament (ACL) tear",
            ["Posterior Cruciate Ligament (PCL) tear", "Isolated Medial Collateral Ligament (MCL) rupture", "Patellar tendon rupture"],
            "The history of a non-contact pivoting/deceleration injury accompanied by an audible 'pop', followed by rapid onset of hemarthrosis within 2-4 hours, is pathognomonic for an acute ACL tear (responsible for >70% of acute traumatic knee hemarthroses). The Lachman test (performed at 20-30 degrees of flexion) is the most sensitive physical examination test for ACL rupture.",
            clinical=True
        ),
        q(
            "Why is the Lachman test clinically superior to the 90-degree Anterior Drawer test for detecting an acute ACL rupture?",
            "Hamstring protective spasm is minimized and the posterior meniscal horn does not wedge against the femoral condyle",
            ["The Lachman test evaluates the patellar tendon rather than cruciate fibers", "At 90 degrees flexion, the normal ACL is completely slack and non-functional", "The Lachman test can only be performed under general anesthesia"],
            "The Anterior Drawer test is performed at 90 degrees of knee flexion, where acute pain triggers protective hamstring muscle spasm that holds the tibia posteriorly, producing a false-negative result; additionally, the posterior horn of the medial meniscus can wedge against the medial femoral condyle, blocking anterior translation. In the Lachman test (at 20-30 degrees flexion), hamstring spasm is minimal, secondary stabilizers are relaxed, and anterior translation can be accurately evaluated.",
            clinical=False
        ),
        q(
            "On an anteroposterior radiograph of the knee following an acute twisting injury, a small vertical avulsion fracture is seen at the lateral margin of the lateral tibial plateau. What is this lesion termed?",
            "Segond fracture (associated with ACL tear)",
            ["Stieda-Pellegrini lesion", "Hoffa fracture", "Gerdy's tubercle fracture"],
            "A Segond fracture is an avulsion fracture of the lateral tibial plateau immediately adjacent to the articular surface, produced by avulsion of the anterolateral ligament / mid-third lateral capsular ligament during excessive internal rotation and varus stress. It is virtually pathognomonic (in 75-100% of cases) of an underlying rupture of the Anterior Cruciate Ligament (ACL).",
            clinical=True
        ),
        q(
            "In classic orthopaedic descriptions, what three structures are injured in O'Donoghue's Unhappy Triad?",
            "Anterior Cruciate Ligament (ACL), Medial Collateral Ligament (MCL), and Medial Meniscus",
            ["Posterior Cruciate Ligament (PCL), Lateral Collateral Ligament (LCL), and Lateral Meniscus", "ACL, Patellar tendon, and Vastus medialis", "PCL, Popliteus tendon, and Arcuate ligament"],
            "O'Donoghue's Unhappy Triad was originally described as the simultaneous disruption of three structures following a severe lateral blow to the knee: 1. Anterior Cruciate Ligament (ACL); 2. Medial Collateral Ligament (MCL); and 3. Medial Meniscus (though modern MRI studies demonstrate that acute lateral meniscus tears are actually more common with acute ACL/MCL tears, O'Donoghue's classical triad remains the standard textbook description).",
            clinical=False
        ),
        q(
            "A 28-year-old male sustains a dashboard impact to the proximal tibia with the knee flexed at 90 degrees. Examination at 90 degrees reveals loss of the normal 1-cm anterior tibial step-off and posterior tibial sagging. What is the diagnosis?",
            "Posterior Cruciate Ligament (PCL) tear",
            ["Anterior Cruciate Ligament (ACL) tear", "Bucket-handle medial meniscal tear", "Quadriceps tendon rupture"],
            "In a normal knee flexed at 90 degrees, the medial tibial plateau rests approximately 1 cm anterior to the medial femoral condyle. In a Posterior Cruciate Ligament (PCL) rupture, gravitational pull causes the tibia to drop posteriorly, creating a visible and palpable depression termed the 'posterior sag sign' or 'Godfrey's test'. The Posterior Drawer test is strongly positive.",
            clinical=True
        ),
        q(
            "During McMurray's test, what combination of movements specifically stresses the posterior horn of the MEDIAL meniscus?",
            "External rotation of the foot with valgus stress while extending the knee from full flexion",
            ["Internal rotation of the foot with varus stress while extending the knee", "Axial compression on the fully extended knee without rotation", "Hyperflexion of the knee with the foot in neutral rotation"],
            "McMurray's test traps the posterior horn of the meniscus between the femoral condyle and tibial plateau: To test the MEDIAL meniscus, the knee is fully flexed, the tibia is EXTERNALLY rotated, a valgus force is applied, and the knee is slowly extended; a palpable/audible 'click' or pain signifies a tear. To test the LATERAL meniscus, the tibia is INTERNALLY rotated with a varus force during extension.",
            clinical=False
        ),
        q(
            "A 42-year-old male sustains a displaced transverse patellar fracture with a 2-cm gap and complete loss of active straight leg raise. What is the treatment of choice?",
            "Open reduction and Modified Tension Band Wiring (TBW)",
            ["Cylindrical plaster cast in 30 degrees knee flexion for 8 weeks", "Total patellectomy with primary tendon-to-tendon repair", "Percutaneous screw fixation with immediate full weight-bearing"],
            "A displaced transverse fracture of the patella with disruption of the extensor retinaculum and inability to straight-leg raise mandates operative restoration. The gold-standard treatment is open reduction and Modified Tension Band Wiring (TBW) using two longitudinal parallel Kirschner wires and an anterior figure-of-eight stainless steel wire loop. This dynamically converts the tensile pull of the quadriceps into compressive forces across the articular surface, allowing early knee mobilization.",
            clinical=True
        ),
        q(
            "In the Schatzker classification of tibial plateau fractures, which type corresponds to a split-depression fracture of the lateral tibial plateau?",
            "Schatzker Type II",
            ["Schatzker Type I", "Schatzker Type III", "Schatzker Type IV"],
            "Schatzker classification: Type I: Pure split/cleavage fracture of the lateral plateau (young patients, dense bone); Type II: Split AND depression fracture of the lateral plateau (most common, combined cleavage and articular impaction); Type III: Pure central depression of lateral plateau without split; Type IV: Medial tibial plateau fracture (high energy, associated with cruciate/collateral tears); Type V: Bicondylar plateau fracture; Type VI: Plateau fracture with metaphyseal-diaphyseal dissociation.",
            clinical=False
        ),
        q(
            "A 17-year-old female dancer sustains an acute lateral patellar dislocation while pivoting. Which primary passive stabilizing structure is torn?",
            "Medial Patellofemoral Ligament (MPFL)",
            ["Lateral patellar retinaculum", "Patellar tendon", "Iliotibial band"],
            "The Medial Patellofemoral Ligament (MPFL) provides 50-60% of the primary passive restraining force against lateral patellar displacement between 0 and 30 degrees of knee flexion. During acute lateral patellar dislocation, the MPFL is avulsed or torn (either at the femoral origin near the adductor tubercle or at the medial patellar margin). Point tenderness at the femoral insertion is termed Bassett's sign.",
            clinical=True
        ),
        q(
            "What clinical hallmark definitively differentiates a displaced bucket-handle meniscal tear from an acute knee ligament sprain?",
            "True mechanical locking with a springy block preventing terminal extension",
            ["Complete absence of any joint effusion or localized tenderness", "Development of sudden, painless hyperextension of the knee joint", "Inability to flex the knee past 10 degrees with normal extension"],
            "A bucket-handle tear is a longitudinal vertical tear where the inner fragment displaces centrally into the intercondylar notch. The displaced fragment becomes mechanically wedged between the femur and tibia, causing true mechanical locking: the patient cannot achieve terminal extension (typically lacking the last 10-30 degrees of extension with a characteristic springy/elastic block), while flexion is relatively well preserved.",
            clinical=False
        ),
    ]),

    # Chapter 21: Injuries to the Leg, Ankle and Foot (HARD - 10 questions)
    (21, "Injuries to the Leg, Ankle and Foot", "hard", [
        q(
            "Why is the tibial diaphysis the most frequent long bone to sustain an open fracture and delayed union?",
            "Subcutaneous anteromedial border and single nutrient artery entering high with precarious distal supply",
            ["Absence of an internal medullary canal preventing endosteal callus", "Lack of parathyroid hormone receptors on tibial osteocytes", "The fibula absorbing 90% of axial weight-bearing stresses"],
            "The tibia is uniquely vulnerable because: 1. Its entire anteromedial border and surface lie immediately beneath the skin without muscular coverage, making fractures readily penetrate the skin (open fractures) and stripping periosteum; 2. The nutrient artery enters high in the upper third, and branches descending to the distal third are often severed by displaced fractures, leaving the distal fragment dependent on sparse periosteal supply.",
            clinical=False
        ),
        q(
            "According to the Danis-Weber classification of ankle fractures, how is a Weber Type B fracture defined anatomically?",
            "Fibula fracture at the level of the syndesmosis, extending obliquely proximally",
            ["Fibula fracture strictly below the joint line with intact syndesmosis", "Fibula fracture high above the syndesmosis with total syndesmotic rupture", "Isolated avulsion of the medial malleolus with intact fibula"],
            "Danis-Weber classification is based on the level of the fibular fracture relative to the syndesmosis: Type A: Infrasyndesmotic (below joint line, transverse avulsion, intact syndesmosis); Type B: Trans-syndesmotic (oblique or spiral fracture at the level of the syndesmosis, extending upward; syndesmosis partially torn, joint may be stable or unstable); Type C: Suprasyndesmotic (above the syndesmosis; complete rupture of the syndesmosis and interosseous membrane, highly unstable).",
            clinical=False
        ),
        q(
            "A 24-year-old athlete sustains an ankle injury with widening of the medial clear space and syndesmosis, but no distal fibular fracture. What mandatory examination prevents missing a Maisonneuve fracture?",
            "Palpate and radiograph the proximal third and neck of the fibula",
            ["Perform an emergency diagnostic arthroscopy of the subtalar joint", "Measure compartment pressures of the superficial posterior compartment", "Evaluate the contralateral knee for collateral ligament laxity"],
            "A Maisonneuve fracture is an unstable ankle injury produced by pronation-external rotation: the force ruptures the deltoid ligament (or fractures the medial malleolus), tears through the anterior inferior tibiofibular ligament and the entire interosseous membrane all the way up the leg, and finally exits as an oblique or spiral fracture through the proximal third or neck of the fibula. If the proximal fibula is not palpated and imaged, the complete syndesmotic disruption is missed.",
            clinical=True
        ),
        q(
            "A 40-year-old painter falls from a ladder landing on his heels. Radiographs show a depressed intra-articular calcaneal fracture. What angle is measured on the lateral view, and what is its normal value?",
            "Böhler's angle; normally 20 to 40 degrees",
            ["Kite's angle; normally 10 to 15 degrees", "Baumann's angle; normally 70 to 80 degrees", "Cobb's angle; normally 0 degrees"],
            "Böhler's angle (the tuber-joint angle) is formed on the lateral radiograph of the foot by the intersection of two lines: one from the highest point of the posterior articular facet to the highest point of the anterior process, and the second from the posterior facet to the superior margin of the calcaneal tuberosity. The normal angle is 20 to 40 degrees. In depressed intra-articular fractures, the posterior facet collapses, reducing or reversing Böhler's angle (often <0 to 10 degrees).",
            clinical=True
        ),
        q(
            "According to the Hawkins classification of talar neck fractures, which type involves dislocation of BOTH the subtalar and tibiotalar joints, carrying an AVN risk of 85% to 100%?",
            "Hawkins Type III",
            ["Hawkins Type I", "Hawkins Type II", "Hawkins Type IV"],
            "Hawkins classification of talus neck fractures: Type I: Undisplaced fracture (AVN risk <10%); Type II: Displaced neck fracture with dislocation of the subtalar joint, ankle joint normal (AVN risk 30-45%); Type III: Displaced neck fracture with dislocation of BOTH the subtalar and tibiotalar (ankle) joints (body extruded posteriorly; AVN risk 85-100%); Type IV: Displaced neck fracture with subtalar, tibiotalar, AND talonavicular subluxation/dislocation.",
            clinical=False
        ),
        q(
            "On follow-up radiographs 6 to 8 weeks after a talar neck fracture, what does the presence of Hawkins sign (subchondral radiolucent band in the talar dome) indicate?",
            "Intact vascularity with disuse osteopenia, ruling out avascular necrosis",
            ["Early subchondral bone collapse confirming complete avascular necrosis", "Acute septic arthritis of the ankle joint requiring debridement", "Failure of bony union between head and body of the talus"],
            "Hawkins sign is a patchy subchondral band of radiolucency (demineralization) seen in the dome of the talus on an AP/mortise radiograph 6 to 8 weeks post-injury. Bone resorption requires an intact blood supply; therefore, visible subchondral osteopenia proves that the body of the talus is vascularized and has NOT undergone avascular necrosis. If the bone has lost its blood supply, it cannot undergo resorption and appears abnormally dense (sclerotic) relative to surrounding osteopenic bones.",
            clinical=False
        ),
        q(
            "A horseback rider sustains a midfoot injury with plantar ecchymosis and widening between the first and second metatarsal bases with a small avulsion 'fleck sign'. What is the diagnosis?",
            "Lisfranc fracture-dislocation (tarsometatarsal injury)",
            ["Chopart fracture-dislocation", "Jones fracture", "Freiberg's infraction"],
            "A Lisfranc injury is a dislocation or subluxation of the tarsometatarsal joint complex. The base of the second metatarsal is mortised between the medial and lateral cuneiforms, acting as the keystone. The Lisfranc ligament connects the medial cuneiform to the base of the second metatarsal. Rupture creates a gap between metatarsal 1 and 2, often with a small avulsion flake of bone from the 2nd metatarsal base ('fleck sign') and pathognomonic plantar ecchymosis.",
            clinical=True
        ),
        q(
            "A military recruit complains of forefoot pain after long-distance marching. Initial radiographs are negative, but 3 weeks later radiographs reveal a hairline crack with fusiform periosteal callus on the 2nd metatarsal shaft. What is this fracture termed?",
            "March fracture (fatigue/stress fracture)",
            ["Jones fracture", "Freiberg's infraction", "Kohler's disease"],
            "A March fracture is a classic fatigue/stress fracture occurring in normal bone subjected to unaccustomed, repetitive cyclic loading (classically in military recruits or marathon runners). It most commonly involves the neck or shaft of the second or third metatarsal (which are rigidly fixed and absorb high propulsion forces). Initial radiographs are often normal; bone scan or MRI shows early marrow edema, and follow-up radiographs after 2-3 weeks show fusiform healing callus.",
            clinical=True
        ),
        q(
            "What anatomical feature differentiates a true Jones fracture of the fifth metatarsal from a pseudo-Jones tuberosity avulsion fracture?",
            "Jones fracture occurs at the metaphyseal-diaphyseal junction in a watershed zone prone to non-union; pseudo-Jones is an avulsion of the tuberosity that heals readily",
            ["Jones fracture occurs at the metatarsal head; pseudo-Jones occurs at the midshaft", "Jones fracture is an open fracture; pseudo-Jones is always closed", "Jones fracture requires amputation; pseudo-Jones requires tension-band wiring"],
            "The fifth metatarsal base has 3 zones: Zone 1 is the tuberosity (pseudo-Jones / dancer's fracture), an avulsion by the peroneus brevis or lateral band of plantar aponeurosis that heals uneventfully. Zone 2 is the true Jones fracture at the metaphyseal-diaphyseal junction (within 1.5 cm distal to the tuberosity), which involves the articulation with the 4th metatarsal. Zone 2 lies in an arterial watershed zone and is prone to non-union (up to 30-50%), often requiring non-weight-bearing cast or screw fixation.",
            clinical=False
        ),
        q(
            "In open fracture debridement of a contaminated tibial fracture, what is the surgical principle regarding management of bone fragments?",
            "Retain fragments with soft-tissue attachment; discard small loose avascular fragments; clean and preserve large articular pieces",
            ["Excise all cortical fragments regardless of periosteal attachment to prevent osteomyelitis", "Retain all loose bone fragments and secure them tightly with cerclage wires", "Boil all contaminated bone fragments in an autoclave and reimplant them"],
            "During surgical debridement of open long-bone fractures: Any bone fragment possessing a viable soft tissue or periosteal attachment must be preserved because it retains osteogenic potential. Small, loose, avascular cortical fragments stripped of all soft tissues must be excised because they act as dead sequestra and niduses for infection. However, large articular fragments essential for joint reconstruction should be thoroughly irrigated, decontaminated, and preserved.",
            clinical=False
        ),
    ]),

    # Chapter 22: Infections of Bones and Joints (HARD - 10 questions)
    (22, "Infections of Bones and Joints", "hard", [
        q(
            "An 8-year-old boy presents with high fever, throbbing distal thigh pain, refusal to bear weight, and exquisite localized tenderness over the distal femoral metaphysis, while gentle knee motion over 30 degrees is tolerated. What is the most likely diagnosis and pathogen?",
            "Acute hematogenous osteomyelitis; Staphylococcus aureus",
            ["Septic arthritis of the knee; Streptococcus pyogenes", "Ewing sarcoma; Kingella kingae", "Acute rheumatic fever; Group A Streptococcus"],
            "Acute hematogenous osteomyelitis typically affects rapidly growing metaphyses of long bones in children. Staphylococcus aureus is the causative organism in >80% of cases. Hallmark signs are high fever, severe constant pain, and exquisite well-localized metaphyseal point tenderness. Because the infection is primarily metaphyseal (not intra-articular), gentle passive joint movement over a small range is relatively painless, which differentiates it from septic arthritis.",
            clinical=True
        ),
        q(
            "Why does acute hematogenous osteomyelitis preferentially originate within the metaphysis of growing long bones in children?",
            "Hairpin loops of nutrient capillaries have sluggish flow and lack competent phagocytic reticuloendothelial cells",
            ["The metaphysis consists of dense compact cortex that traps circulating bacteria", "Metaphyseal marrow has an acidic pH that accelerates bacterial proliferation", "The periosteum over the metaphysis is absent, allowing direct bacterial entry"],
            "In growing children, the nutrient artery terminates in the metaphysis as non-anastomosing hairpin capillary loops immediately beneath the growth plate. Blood flow slows down dramatically in these wide loops, creating sluggish hemodynamics. Furthermore, these capillary loops lack a competent reticuloendothelial lining and phagocytic cells, allowing transiently circulating bacteria (bacteremia) to settle, multiply, and initiate acute osteomyelitis.",
            clinical=False
        ),
        q(
            "In chronic osteomyelitis with a draining sinus, what terms denote the dead devitalized bone, surrounding new bone sheath, and the cortical defect through which pus discharges?",
            "Sequestrum, Involucrum, and Cloaca",
            ["Involucrum, Sequestrum, and Sinus", "Callus, Osteon, and Volkmann's canal", "Brodie's abscess, Osteoid, and Fistula"],
            "In chronic osteomyelitis: 1. Sequestrum is a piece of dead, devitalized bone that has separated from the viable parent bone (appears abnormally dense on X-ray because it has lost its blood supply and cannot participate in disuse osteopenia); 2. Involucrum is a thick, irregular sheath of new subperiosteal bone formed around the dead bone by the elevated, hyperemic periosteum; 3. Cloaca is an opening or hole in the involucrum through which pus, debris, and small sequestra escape to the skin.",
            clinical=True
        ),
        q(
            "A 20-year-old male presents with dull aching tibial pain worse at night. Radiograph reveals a solitary 2-cm radiolucent cavity surrounded by a dense sclerotic halo in the proximal tibial metaphysis. What is the diagnosis?",
            "Brodie's abscess",
            ["Osteoid osteoma", "Ewing sarcoma", "Aneurysmal bone cyst"],
            "Brodie's abscess is a localized form of subacute or chronic pyogenic osteomyelitis characterized by an indolent clinical course. The host defenses wall off the infection within the cancellous metaphysis (most commonly proximal or distal tibia). Radiographically, it appears as a well-defined oval or circular radiolucency (>1 cm) surrounded by a dense, smooth rim of reactive sclerotic bone. Staphylococcus aureus is the most common organism.",
            clinical=True
        ),
        q(
            "A 10-year-old child with sickle cell disease presents with multifocal diaphyseal osteomyelitis. What atypical bacterial pathogen is classically associated with this condition?",
            "Salmonella species",
            ["Pseudomonas aeruginosa", "Brucella abortus", "Mycobacterium avium-intracellulare"],
            "While Staphylococcus aureus remains common, patients with sickle cell disease have an extraordinarily high susceptibility to osteomyelitis caused by Salmonella species. Repeated microvascular sickling and thrombosis in the mesenteric vessels cause bowel mucosal ischemic infarction, allowing Salmonella to enter the bloodstream; sluggish flow in infarcted, ischemic bone marrow provides an ideal culture medium for Salmonella osteomyelitis (often multifocal and diaphyseal).",
            clinical=True
        ),
        q(
            "What is the pathognomonic radiological feature of Garré's sclerosing non-suppurative osteomyelitis?",
            "Diffuse cortical thickening and dense bone sclerosis without sequestrum or abscess formation",
            ["Extensive geographic osteolysis with pathological fracture and soft-tissue mass", "Rapid destruction of the adjacent articular joint space within 48 hours", "Multiple subchondral cysts with calcified intra-articular loose bodies"],
            "Garré's osteomyelitis is an uncommon, chronic, non-suppurative form of osteomyelitis typically affecting adolescents and young adults. It is characterized by an indolent, low-grade infection that stimulates massive, dense subperiosteal and endosteal bone formation, producing spindle-shaped cortical thickening and marked sclerosis of the diaphysis (classically mandible or tibia). There is no soft tissue abscess, no pus formation, and no sequestrum.",
            clinical=False
        ),
        q(
            "A 2-year-old child with high fever holds the hip flexed, abducted, and externally rotated, screaming upon attempted motion. Arthrocentesis yields turbid fluid with 85,000 WBC/mm3 (90% neutrophils). What is the mandatory immediate treatment?",
            "Emergency arthrotomy, decompression, irrigation, and intravenous antibiotics",
            ["Oral amoxicillin and watchful waiting in the outpatient clinic for 48 hours", "Skin traction with 3 kg weight and application of local heat packs", "Intra-articular steroid injection to suppress acute synovitis"],
            "Septic arthritis of the hip in infants is a surgical emergency. The hip capsule is tight; purulent exudate under high intra-articular pressure rapidly tamponades the retinacular blood vessels supplying the cartilaginous femoral head, while bacterial proteases and neutrophil elastases digest articular cartilage within 24-48 hours. Urgent open surgical arthrotomy and debridement (or emergency arthroscopic washout) is mandatory to decompress the joint and prevent irreversible femoral head destruction and dislocation (Tom Smith arthritis).",
            clinical=True
        ),
        q(
            "What are the four components of the Kocher criteria used to identify septic arthritis in an irritable pediatric hip?",
            "Non-weight-bearing, ESR > 40 mm/hr, Fever > 38.5 C, and WBC > 12,000 cells/mm3",
            ["Morning stiffness > 1 hour, HLA-B27 positivity, Knee swelling, and Intermalleolar distance > 5 cm", "Age > 10 years, Normal ESR, CRP < 5 mg/L, and Positive Trendelenburg sign", "Bilateral hip pain, Thrombocytosis, Low ferritin, and Subnormal temperature"],
            "The Kocher criteria predict the probability of septic arthritis in a child with an irritable hip: 1. History of fever > 38.5 C; 2. Inability to bear weight; 3. ESR > 40 mm/hr; 4. Serum WBC > 12,000/mm3. The presence of 1 criterion gives a 3% probability; 2 criteria = 40%; 3 criteria = 93%; and all 4 criteria = 99% probability of septic arthritis, mandating diagnostic joint aspiration.",
            clinical=False
        ),
        q(
            "A 23-year-old sexually active woman presents with fever, migratory tenosynovitis, pustular skin lesions, and acute purulent monoarthritis of the wrist. What is the causative pathogen?",
            "Neisseria gonorrhoeae",
            ["Staphylococcus epidermidis", "Treponema pallidum", "Brucella melitensis"],
            "Disseminated Gonococcal Infection (DGI) caused by Neisseria gonorrhoeae is the most common cause of acute septic arthritis in young, healthy, sexually active adults. It characteristically presents in two stages: an initial bacteremic phase with migratory tenosynovitis, fever, and classic pustular/maculopapular dermatitis on the extremities, followed by localization into an acute purulent monoarthritis or oligoarthritis (most commonly knee, wrist, or ankle).",
            clinical=True
        ),
        q(
            "In a patient with a 25-year history of chronic osteomyelitis and a persistent discharging sinus, the sinus mouth develops an everted, fungating, bleeding ulcer. Biopsy confirms malignancy. What is this lesion termed?",
            "Marjolin's ulcer (Squamous cell carcinoma)",
            ["Secondary Osteosarcoma", "Periosteal fibrosarcoma", "Malignant fibrous histiocytoma"],
            "A Marjolin's ulcer is a squamous cell carcinoma (SCC) developing in long-standing, chronic, non-healing sinus tracts or scars (classically chronic osteomyelitis draining sinuses or old burn scars). Constant cellular turnover, chronic inflammation, and tissue irritation over decades lead to malignant metaplasia and dedifferentiation into an aggressive squamous cell carcinoma. Hallmark signs: foul-smelling bleeding, exophytic fungating mass, everted margins, and local bone invasion.",
            clinical=True
        ),
    ]),

    # Chapter 23: Tuberculosis of Bones and Joints (HARD - 10 questions)
    (23, "Tuberculosis of Bones and Joints", "hard", [
        q(
            "A 35-year-old male presents with chronic backache, evening low-grade fever, localized kyphotic gibbus at T9-T10, and disc space narrowing with adjacent endplate erosions on radiograph. What is the diagnosis?",
            "Tuberculosis of the spine (Pott's disease)",
            ["Metastatic adenocarcinoma to vertebral bodies", "Multiple myeloma involving thoracic spine", "Ankylosing spondylitis"],
            "Tuberculosis of the spine (Pott's spine) is the most common site of skeletal TB (~50%). It classically begins in the subchondral paradiscal region of adjacent vertebrae. The disc space narrows early (in contrast to metastases, which destroy pedicles and spare discs), bone destruction of adjacent endplates occurs, and the anterior vertebral bodies collapse, producing an acute localized angular kyphosis known as a 'gibbus' or 'knuckle'.",
            clinical=True
        ),
        q(
            "What is the most common anatomical variety of spinal tuberculosis, and what vascular feature accounts for its predilection?",
            "Paradiscal type; contiguous vertebral subchondral bone shares anastomosing spinal arterial branches",
            ["Central type; retrograde venous flow through Batson's plexus into spinous process", "Posterior type; exclusive arterial seeding of facet joints via intercostal arteries", "Synovial type; direct hematogenous inoculation into the ligamentum flavum"],
            "The paradiscal type is by far the most frequent variety of Pott's spine (>80%). It affects the adjacent subchondral margins of two contiguous vertebrae and the intervening disc. In adults and children, adjacent vertebral bodies receive arterial supply from branches of the same spinal artery; bacterial emboli lodge in these contiguous subchondral capillary beds, causing paradoxical kissing lesions with early disc space narrowing.",
            clinical=False
        ),
        q(
            "A patient with active thoracic Pott's disease develops spastic paraparesis, sustained clonus, and extensor plantars, but sensation is intact. What is the primary underlying cause of this early-onset Pott's paraplegia?",
            "Mechanical compression by inflammatory cold abscess, granulation tissue, and edema",
            ["Permanent bony ridge impingement from malunited healed kyphosis", "Direct transverse myelitis caused by viral co-infection", "Hyperextension ligamentous buckling of the posterior arch"],
            "Pott's paraplegia in active disease (early-onset paraplegia) develops during the active phase of tuberculous infection. It is primarily caused by extrinsic mechanical compression of the anterior spinal cord by inflammatory soft-tissue elements: cold abscess, soft caseous debris, tuberculous granulation tissue, or inflammatory edema. Because it is largely inflammatory, it carries an excellent prognosis (over 90% recovery) when treated with multidrug anti-tubercular therapy (ATT) and rest.",
            clinical=True
        ),
        q(
            "What clinical presentation in thoracic spinal tuberculosis represents an absolute indication for emergency surgical decompression?",
            "Rapid onset of paraplegia, progressive neurological deficit, or failure to improve after 3 to 4 weeks of medical therapy",
            ["Presence of mild back pain with normal motor power (Grade 5/5)", "Narrowing of a single disc space without any neurological signs", "Elevated ESR with localized spinal tenderness"],
            "Indications for surgical decompression in Pott's spine include: 1. Paraplegia of sudden onset or rapid deterioration; 2. Paraplegia failing to improve or deteriorating despite 3-4 weeks of adequate conservative therapy (ATT + immobilization); 3. Severe bony compression (retropulsed sequestrum or pathological dislocation); 4. Posterior spinal disease; 5. Severe crippling kyphosis; 6. Recurrence of paraplegia.",
            clinical=False
        ),
        q(
            "An 8-year-old child presents with a limp, groin pain radiating to the knee, and a hip held in flexion, abduction, and external rotation with apparent lengthening. Joint space is preserved on radiograph. What stage of TB hip is this?",
            "Stage 1: Stage of Synovitis",
            ["Stage 2: Stage of Early Arthritis", "Stage 3: Stage of Advanced Arthritis (Joint Destruction)", "Stage 4: Healed Fibrous Ankylosis"],
            "TB of the hip progresses through three classic clinical stages: Stage 1 (Stage of Synovitis): Joint effusion causes the hip to assume the position of maximum capsular capacity—Flexion, Abduction, and External Rotation (FABER), producing apparent lengthening of the limb; joint space is preserved or widened on X-ray. Stage 2 (Early Arthritis): Spasm of stronger muscles takes over—Flexion, Adduction, Internal Rotation (FADIR) with apparent shortening. Stage 3 (Destruction): Bone erosion, 'wandering acetabulum', dislocation, true shortening.",
            clinical=True
        ),
        q(
            "In Stage 2 (Early Arthritis) of tuberculous hip disease, what change in limb attitude occurs compared to Stage 1?",
            "Limb shifts into flexion, adduction, and internal rotation, with apparent shortening",
            ["Limb shifts into hyperextension, abduction, and external rotation with true lengthening", "Limb remains in neutral extension with complete flaccid paralysis", "Limb assumes extreme 90-degree external rotation with true shortening"],
            "In Stage 1 (Synovitis), the joint capsule is distended with effusion, so the limb adopts the position of maximum intra-articular capacity: Flexion, Abduction, External Rotation (apparent lengthening). In Stage 2 (Early Arthritis), articular cartilage is eroded; intense muscle spasm of the powerful adductors and internal rotators overcomes the weaker abductors, forcing the limb into: Flexion, Adduction, Internal Rotation (FADIR), resulting in apparent shortening.",
            clinical=False
        ),
        q(
            "A 4-year-old child presents with a painless, spindle-shaped swelling of the ring finger proximal phalanx. Radiographs show medullary destruction with subperiosteal expansion producing a ballooned shell ('spina ventosa'). What is the diagnosis?",
            "Tuberculous dactylitis",
            ["Enchondroma of the phalanx", "Pyogenic acute osteomyelitis", "Sickle cell dactylitis"],
            "Tuberculous dactylitis ('spina ventosa') is tuberculosis of the short tubular bones (metacarpals, metatarsals, phalanges) seen primarily in children under 5 years. Granulomatous infection expands the medullary canal, eroding the cortex from within while the active periosteum lays down a shell of new subperiosteal bone, giving the appearance of a bone expanded with air/gas ('spina ventosa' = spina wind/blown with wind).",
            clinical=True
        ),
        q(
            "In lumbar spinal tuberculosis (L1-L4), through which anatomical pathway does a cold abscess typically track to present as a swelling in the groin?",
            "Within the psoas muscle sheath, entering the femoral triangle lateral to the femoral vessels",
            ["Through the obturator canal into the medial adductor compartment", "Along the sciatic nerve into the popliteal fossa", "Through the greater sciatic notch into the ischiorectal fossa"],
            "The psoas major originates from the transverse processes and bodies of T12 to L5 vertebrae. Caseous purulent exudate from lumbar spinal TB tracks downward within the tight psoas fascial sheath ('psoas abscess'). It passes over the pelvic brim, behind the inguinal ligament, and enters the upper thigh to point in the femoral triangle lateral to the femoral artery (or may track into Petit's lumbar triangle or the gluteal region).",
            clinical=False
        ),
        q(
            "What three cardinal radiographic signs comprise Phemister's Triad in tuberculous arthritis of the knee?",
            "Juxta-articular osteoporosis, peripheral subchondral erosions, and gradual joint space narrowing",
            ["Rapid bone destruction within 48 hours, massive involucrum, and dense sequestrum", "Complete joint dislocation, sunburst periosteal reaction, and Codman's triangle", "Dense subchondral sclerosis, multiple osteophytes, and asymmetric joint space loss"],
            "Phemister's triad characterizes tuberculous arthritis on plain radiography: 1. Marked juxta-articular osteopenia (secondary to chronic hyperemia); 2. Peripheral osseous erosions (tuberculous pannus attacks peripheral non-contact margins of cartilage first, unlike pyogenic enzymes that digest weight-bearing cartilage early); 3. Slow, gradual joint space narrowing (because Mycobacterium tuberculosis lacks the chondrolytic enzymes present in Staphylococcus aureus).",
            clinical=False
        ),
        q(
            "Why is a tuberculous abscess clinically designated as a 'cold abscess'?",
            "It lacks classical acute signs of inflammation: no heat, erythema, or acute throbbing tenderness",
            ["The internal purulent fluid freezes at physiological body temperature", "It develops exclusively during winter months in cold climates", "It is caused by psychrophilic organisms that replicate only at low temperatures"],
            "A 'cold abscess' is a collection of liquefied caseous tuberculous pus, necrotic debris, and inflammatory exudate that forms slowly over months. Because Mycobacterium tuberculosis infection is an indolent chronic granulomatous process, the abscess lacks the classical signs of acute acute pyogenic inflammation (calor, rubor, dolor)—the overlying skin is normal in color, cool to touch, and non-tender, giving it the clinical name 'cold abscess'.",
            clinical=False
        ),
    ]),

    # Chapter 24: Infections of the Hand (Easy - 5 questions)
    (24, "Infections of the Hand", "easy", [
        q(
            "A carpenter presents with severe throbbing pain in the distal index pulp 3 days after a splinter puncture. The pulp is tense, red, and swollen. What is the diagnosis and risk of delayed drainage?",
            "Felon; risk of ischemic necrosis and osteomyelitis of the distal phalanx",
            ["Paronychia; risk of Dupuytren's contracture", "Thenar space abscess; risk of carpal tunnel syndrome", "Herpetic whitlow; risk of digital amputation"],
            "A felon is an acute pyogenic infection (usually Staph aureus) of the closed terminal pulp space of the finger. The pulp is divided into multiple closed fascial compartments by tough vertical fibrous septa running from the periosteum of the distal phalanx to the skin. Rapidly rising pressure within these tight chambers compresses the digital nutrient arterioles, leading to ischemic necrosis and osteomyelitis of the distal two-thirds of the phalanx.",
            clinical=True
        ),
        q(
            "What are Kanavel's four cardinal signs of acute flexor tenosynovitis in a digit?",
            "Uniform sausage swelling, flexed finger posture, tenderness along flexor sheath, and severe pain on passive extension",
            ["Palmar flattening, loss of radial pulse, clawing of all digits, and thenar anesthesia", "Fixed extension posture, cold pale fingertip, palpable step-off, and subungual discharge", "Wrist dorsiflexion pain, A1 pulley nodule, thenar atrophy, and positive Phalen test"],
            "Kanavel's four cardinal signs of acute flexor tenosynovitis: 1. Symmetrical, uniform sausage-like swelling along the entire digit; 2. The affected finger is held in slight flexion at rest; 3. Exquisite tenderness strictly localized along the entire anatomical course of the flexor tendon sheath; 4. Excruciating pain elicited upon passive extension of the finger (the most sensitive and reliable early sign).",
            clinical=False
        ),
        q(
            "Suppurative flexor tenosynovitis originating in the little finger flexor sheath has a direct anatomical pathway to rapidly spread into which deep synovial space?",
            "Ulnar bursa (with potential tracking to radial bursa forming a horseshoe abscess)",
            ["Thenar space", "Midpalmar space exclusively", "Subaponeurotic space on dorsum of hand"],
            "In the vast majority of human hands, the digital flexor tendon sheath of the little finger is directly continuous with the common flexor sheath (Ulnar bursa) in the palm and carpal tunnel. (In contrast, index, middle, and ring digital sheaths end blindly at the level of the metacarpal heads). Furthermore, the ulnar bursa communicates with the radial bursa (FPL sheath) in over 50% of individuals, allowing infection to track across into a life-threatening 'horseshoe abscess'.",
            clinical=True
        ),
        q(
            "A seamstress presents with acute throbbing pain and redness at the lateral nail fold with pus extending beneath the proximal nail plate. What is the diagnosis and definitive management?",
            "Paronychia with subungual abscess; drainage with partial/total excision of proximal nail plate",
            ["Felon; treated with a fish-mouth incision across the distal fingertip", "Herpetic whitlow; treated with radical surgical excision of the nail bed", "Glomus tumor; treated with en-bloc amputation of the distal phalanx"],
            "Paronychia is a superficial pyogenic infection of the paronychium (skin fold surrounding the nail plate). When pus tracks beneath the proximal nail bed (subungual abscess), antibiotic therapy alone fails. The proximal portion of the nail plate floating over the pus acts as a foreign body; definitive treatment requires lifting the eponychial fold and excising the proximal one-third of the nail plate to allow unhindered drainage.",
            clinical=True
        ),
        q(
            "What clinical feature differentiates an infection of the Thenar Space from that of the Midpalmar Space?",
            "Thenar space infection balloons the first web space with thumb abduction; midpalmar space infection obliterates palmar concavity with dorsal swelling",
            ["Thenar space infection causes clawing of digits 4 and 5; midpalmar causes wrist drop", "Thenar space infection involves ulnar bursa; midpalmar involves radial bursa", "Thenar space infection causes isolated pulp necrosis; midpalmar causes paronychia"],
            "The midpalmar space lies between the middle palmar septum and hypothenar septum, deep to the flexor tendons; infection obliterates the normal concave palmar hollow, making it convex/bulging, and pus tracks along lumbrical canals producing marked edema on the loose dorsum of the hand. The thenar space lies between the hypothenar septum and the adductor pollicis; infection balloons the first interdigital web space, holding the thumb abducted and flexed.",
            clinical=False
        ),
    ]),
]
