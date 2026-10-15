from .common import q

CHAPTERS = [
    # Chapter 25: Congenital Talipes Equino Varus (CTEV) (HARD - 10 questions)
    (25, "Congenital Talipes Equino Varus (CTEV)", "hard", [
        q(
            "A male newborn is found to have bilateral clubfoot deformity that cannot be passively corrected to neutral. What are the four structural components of the CAVE deformity in Congenital Talipes Equinovarus (CTEV)?",
            "Cavus of midfoot, Adductus of forefoot, Varus of hindfoot, and Equinus of ankle",
            ["Calcaneus of hindfoot, Abduction of forefoot, Valgus of ankle, and Eversion of midfoot", "Cavus of hindfoot, Abductus of midfoot, Valgus of subtalar joint, and Extension of toes", "Claw toes, Adductus of metatarsals, Valgus of heel, and Equinus of hindfoot"],
            "The classic acronym CAVE describes the 4 structural deformities of CTEV: 1. Cavus of the midfoot (exaggerated medial longitudinal arch caused by plantarflexion of 1st metatarsal relative to hindfoot); 2. Adductus of the forefoot (medial deviation of metatarsals at Lisfranc/Chopart joints); 3. Varus of the hindfoot (inversion/tilting of calcaneus under the talus); 4. Equinus of the ankle (plantarflexion at the tibiotalar joint caused by contracted Achilles tendon).",
            clinical=True
        ),
        q(
            "In the Ponseti method of serial casting for CTEV, what is the mandatory sequence of deformity correction and the pivotal anatomical fulcrum?",
            "Correct Cavus first; then correct Adductus and Varus simultaneously around lateral talar head; lastly correct Equinus",
            ["Correct Equinus first by forceful dorsiflexion; then pronate forefoot around cuboid", "Correct Adductus and Equinus simultaneously by forceful eversion and pronation", "Perform immediate posteromedial soft-tissue release followed by a circular cast"],
            "Ponseti's method follows strict kinematic principles: 1. Correct Cavus first by elevating the first metatarsal (supinating forefoot) to align the forefoot with the inverted hindfoot; 2. Correct Adductus and Varus together: stabilize the head of the talus with the thumb on its lateral aspect (fulcrum) and gently abduct the supinated foot beneath it (the calcaneus abducts and everts freely under the talus); 3. Never pronate the foot (which causes a rocker-bottom foot); 4. Correct Equinus last by dorsiflexing the ankle once full abduction (60 degrees) is achieved.",
            clinical=False
        ),
        q(
            "A 6-week-old infant with CTEV has undergone five Ponseti casts. The foot is abducted 60 degrees with neutral varus, but ankle dorsiflexion remains limited to -10 degrees. What is the next step?",
            "Percutaneous Achilles tenotomy under local anesthesia followed by casting in dorsiflexion for 3 weeks",
            ["Forceful closed manipulation under general anesthesia to stretch the heel cord", "Open extensive posteromedial soft-tissue release (Turco procedure)", "Application of a Dennis Browne bar without tenotomy and observation for 6 months"],
            "In over 85% to 90% of CTEV cases managed by the Ponseti method, the tight, collagen-rich calcaneal tendon (Achilles tendon) cannot be fully stretched by casting alone. Once cavus, adductus, and varus are fully corrected and the foot achieves 60 degrees of abduction, a percutaneous Achilles tenotomy (complete transection 1.5 cm above insertion) is performed to relieve the equinus. A post-tenotomy cast is worn for 3 weeks, during which the tendon regenerates at the lengthened length.",
            clinical=True
        ),
        q(
            "What are the two major sub-scores evaluated in the Pirani scoring system for monitoring CTEV?",
            "Midfoot Contracture Score and Hindfoot Contracture Score",
            ["Forefoot score and Ankle score", "Tarsal score and Soft tissue score", "Motor score and Sensory score"],
            "The Pirani score (0 to 6 total) evaluates 6 clinical signs, each scored 0 (normal), 0.5 (moderate), or 1 (severe): Midfoot Contracture Score (0-3): 1. Curvature of the lateral border of foot; 2. Medial creasing; 3. Uncoverage of the lateral head of the talus. Hindfoot Contracture Score (0-3): 4. Posterior creasing; 5. Rigidity of equinus; 6. Empty heel sign (absence of calcaneus in heel pad). A score > 4 predicts the need for tenotomy.",
            clinical=False
        ),
        q(
            "On AP and lateral stress radiographs of a foot with untreated CTEV, what alteration is seen in the relationship between the longitudinal axes of the talus and calcaneus (Kite's angle)?",
            "Kite's angle is markedly decreased, with talus and calcaneus appearing parallel on both views",
            ["Kite's angle is widened to greater than 60 degrees on both views", "The talus and calcaneus cross each other at a right angle (90 degrees)", "The calcaneal axis points directly superiorly into the tibial shaft"],
            "In a normal infant foot, the longitudinal axis of the talus and the axis of the calcaneus diverge, forming Kite's angle (normally 25 to 45 degrees on AP view and 25 to 50 degrees on lateral view). In CTEV, the calcaneus is inverted, adducted, and rotated under the talus, causing the longitudinal axes of the talus and calcaneus to lie parallel to each other (Kite's angle < 15-20 degrees or approaching 0).",
            clinical=False
        ),
        q(
            "What iatrogenic deformity is created if a clinician attempts to correct equinus in a clubfoot by forceful dorsiflexion BEFORE heel varus is corrected?",
            "Rocker-bottom foot (midfoot break through midtarsal joints)",
            ["Pes cavus deformity with vertical talus", "Hallux rigidus with metatarsal overgrowth", "Tarsal coalition of the subtalar joint"],
            "If dorsiflexion is forcefully applied to a foot that is still in varus with an unyielding Achilles tendon, the calcaneus cannot dorsiflex in the mortise. The upward force instead fractures or dorsally subluxates the midtarsal joints (Chopart's or naviculocuneiform joints), crushing the plantar cortex and creating an iatrogenic 'rocker-bottom foot' (convex sole with persistent heel equinus).",
            clinical=False
        ),
        q(
            "Following successful Ponseti casting and Achilles tenotomy, what is the mandatory maintenance brace protocol to prevent relapse?",
            "Foot abduction orthosis (Denis Browne bar) in 60-70 degrees external rotation: 23 hrs/day for 3 months, then night/naps until 4-5 years",
            ["Short-leg walking cast worn for 6 weeks followed by ordinary sports shoes", "Custom ankle-foot orthosis holding foot neutral for 6 months only", "Nightly elastic band wrapping without rigid cross-bars until walking age"],
            "Non-compliance with the post-correction foot abduction orthosis (FAO / Denis Browne or Steenbeek bar) is the single most common cause of CTEV recurrence (relapse rate > 80% with poor compliance vs < 5% with strict compliance). The brace holds the affected foot in 60-70 degrees external rotation (40 degrees for unaffected side) and 10-15 degrees dorsiflexion: worn 23 hours/day for the first 3 months, then 12-14 hours at night/naps until 4-5 years of age.",
            clinical=True
        ),
        q(
            "What are the primary pathological morphological abnormalities of the TALUS bone in CTEV?",
            "Talus is small, its neck deviated medially and plantarly, and its anterior body extruded from the mortise",
            ["Talus is massively hypertrophied with a duplicated head", "Talus is rotated laterally by 90 degrees with dorsal dislocation into the tibia", "Talus undergoes complete cartilaginous necrosis at birth"],
            "In CTEV, the talus is the primary bone affected: 1. It is abnormally small; 2. Its neck is foreshortened and deflected medially and plantarly (up to 30-50 degrees relative to the body); 3. The body of the talus is plantarly flexed, extruded anteriorly from the ankle mortise, and only its posterior articular surface articulates with the tibia; 4. The navicular articulates with the medial aspect of the talar head rather than anteriorly.",
            clinical=False
        ),
        q(
            "A 4-year-old child who underwent Ponseti treatment as an infant presents with dynamic supination of the forefoot during the swing phase of gait. What tendon transfer is indicated?",
            "Split Anterior Tibialis Tendon Transfer (SPLATT) or full transfer of tibialis anterior to the lateral cuneiform",
            ["Transfer of the Achilles tendon to the dorsum of the navicular", "Transfer of the Peroneus longus to the medial malleolus", "Complete release of the plantar fascia and abductor hallucis"],
            "Dynamic supination during gait occurs when the tibialis anterior muscle overpowers the weaker evertors (peronei) during the swing phase, causing the foot to invert as it swings forward. Transferring the tibialis anterior tendon (either completely or as a split transfer—SPLATT) to the lateral (third) cuneiform neutralizes this supination force, transforming the muscle into a pure, balanced ankle dorsiflexor without disturbing passive hindfoot motion.",
            clinical=True
        ),
        q(
            "Why is extensive open posteromedial release (Turco procedure) now reserved only as a salvage procedure for clubfoot rather than primary management?",
            "Extensive open release causes severe deep fibrosis, joint stiffness, and late painful arthrosis",
            ["Open surgery requires bilateral above-knee amputations", "The Achilles tendon cannot heal following surgical z-lengthening", "PMR cannot be performed before skeletal maturity at age 18"],
            "Long-term follow-up studies of extensive open posteromedial releases (Turco, McKay, Carroll) revealed high rates of complications: severe intra-articular scarring, stiffness, weak calf musculature, overcorrection (calcaneovalgus), undercorrection, and early degenerative osteoarthritis. The biological, minimally invasive Ponseti technique achieves superior functional, supple, and pain-free feet, relegating open surgery to rare, rigid, neglected, or syndromic cases.",
            clinical=False
        ),
    ]),

    # Chapter 26: Congenital Dislocation of the Hip and Other Malformations (HARD - 10 questions)
    (26, "Congenital Dislocation of the Hip and Other Malformations", "hard", [
        q(
            "During neonatal examination of an infant born in breech presentation, flexing hips to 90 degrees and gently abducting thighs produces a palpable 'clunk' as the femoral head relocates into the acetabulum. What physical examination test is this?",
            "Ortolani test",
            ["Barlow test", "Galeazzi test", "Trendelenburg test"],
            "The Ortolani test is a test of REDUCTION for a dislocated hip: with the infant supine, the examiner flexes the hips to 90 degrees, places fingers over the greater trochanters and thumbs along the inner thighs, and gently abducts the thighs while applying forward pressure behind the trochanter. If the hip is dislocated, the femoral head slips over the posterior acetabular rim into the socket with a palpable 'clunk' (relocation).",
            clinical=True
        ),
        q(
            "What is the diagnostic maneuver and objective of the Barlow provocative test in infant hip assessment?",
            "Adducting the flexed hip while applying gentle posterior pressure to determine if an unstable hip can be dislocated",
            ["Abducting the hip to feel a reduction clunk as the head enters the socket", "Measuring leg length discrepancy with hips and knees flexed at 90 degrees", "Testing gluteus medius power during single-leg weight-bearing stance"],
            "The Barlow test is a provocative test to identify an unstable, dislocatable hip (a hip that is located at rest but can be displaced). The examiner flexes the hip to 90 degrees, adducts the thigh slightly past the midline, and applies gentle backward (posterior) pressure along the line of the femur. If the hip is unstable, the femoral head slips out of the acetabulum over the posterior fibrocartilaginous labrum.",
            clinical=False
        ),
        q(
            "A 6-month-old infant is examined for asymmetric thigh folds. With the infant supine, hips and knees flexed to 90 degrees, and feet flat on the table, the knee on the affected side sits lower than the normal side. What is this sign termed?",
            "Galeazzi sign (Allis sign)",
            ["Trendelenburg sign", "Telescoping sign", "Thomas sign"],
            "The Galeazzi (Allis) sign is a classic clinical indicator of unilateral hip dislocation in infants older than 3 to 6 months. With the infant supine, hips and knees flexed to 90 degrees, and heels resting together on a firm flat surface, the dislocated femoral head rests posterior and superior to the acetabulum, causing apparent shortening of the femur and resulting in the knee on the affected side appearing lower than the normal side.",
            clinical=True
        ),
        q(
            "On an anteroposterior pelvic radiograph of an infant with suspected DDH, where should the capital femoral ossification center normally lie relative to Hilgenreiner and Perkins lines?",
            "Inferomedial quadrant",
            ["Superolateral quadrant", "Superomedial quadrant", "Inferolateral quadrant"],
            "Hilgenreiner's line is a horizontal line drawn through the triradiate cartilages of both acetabula. Perkins' line is a vertical line drawn perpendicular to Hilgenreiner's line from the outermost bony edge of the acetabular roof. In a normal hip, the capital femoral ossification center (which appears at 4-6 months) lies within the INFEROMEDIAL quadrant. In DDH, the dislocated head is displaced into the SUPEROLATERAL quadrant.",
            clinical=False
        ),
        q(
            "What does an abnormal disruption (break) in Shenton's line on an anteroposterior radiograph of the pelvis signify?",
            "Subluxation or dislocation of the femoral head, or a displaced femoral neck fracture",
            ["Congenital absence of the obturator membrane", "Hypertrophy of the iliofemoral ligament", "Premature fusion of the triradiate cartilage"],
            "Shenton's line is a smooth, continuous radiological arch formed by the inferior margin of the superior pubic ramus and the adjacent inferior/medial margin of the femoral neck. Any cranial or lateral displacement of the femoral head (as in DDH, subluxation, Perthes disease, or fractured femoral neck) disrupts the continuity of this smooth curve, producing a broken Shenton's line.",
            clinical=False
        ),
        q(
            "What is the mechanism of the Pavlik harness in managing DDH under 6 months, and what is the 'safe zone' of positioning?",
            "Flexion at 90-100 degrees and abduction at 45-60 degrees; avoiding hyperflexion and extreme abduction",
            ["Rigid extension at 180 degrees and internal rotation at 90 degrees", "Axial traction distracting the head 2 cm away from the joint", "Circumferential pelvic compression clamping both trochanters"],
            "The Pavlik harness is the gold standard for reducible DDH under 6 months: it maintains the hips in 90-100 degrees flexion and 45-60 degrees abduction ('safe zone' of Ramsay). Within this zone, the femoral head is centered directly into the acetabulum, stimulating normal acetabular development while allowing kicking. Hyperflexion (>110-120 deg) compresses the femoral nerve causing transient quadriceps palsy; hyperabduction (>60-70 deg) compresses the circumflex vessels against the pubic bone, risking AVN.",
            clinical=True
        ),
        q(
            "In late-diagnosed DDH (18 months of age), which anatomical structures act as physical obstacles preventing closed reduction of the hip?",
            "Inverted labrum (limbus), hourglass capsular constriction, hypertrophied ligamentum teres, and pulvinar fat",
            ["Patellar tendon, quadriceps expansion, and medial collateral ligament", "Gluteus maximus tendon, sacrotuberous ligament, and piriformis", "Femoral artery, femoral vein, and saphenous nerve"],
            "Obstacles to closed reduction in late DDH include: 1. Inverted fibrocartilaginous labrum (limbus); 2. Hourglass constriction of the joint capsule by the tight iliopsoas tendon; 3. Hypertrophied, elongated ligamentum teres; 4. Pulvinar (hypertrophic fibrofatty tissue filling the empty acetabulum); 5. Contracted transverse acetabular ligament; 6. Contracted adductor and iliopsoas musculature.",
            clinical=False
        ),
        q(
            "How does a Salter innominate osteotomy correct acetabular dysplasia in a 2-year-old child with DDH?",
            "Rotates the entire acetabular roof anteriorly and laterally around the symphysis pubis fulcrum",
            ["Bends the outer iliac cortex downward without altering the triradiate cartilage", "Excises the superior acetabular rim followed by autologous bone grafting", "Fuses the femoral head to the ilium to construct a functional shelf"],
            "Salter's innominate osteotomy is a redirectional pelvic osteotomy indicated between 18 months and 6-8 years. A transverse cut is made through the ilium from the greater sciatic notch to the anterior inferior iliac spine. The entire lower fragment (including the intact acetabulum) is rotated as a unit anterolaterally around the pivot of the symphysis pubis and held with a triangular bone graft and pins, improving anterior and superior femoral head coverage.",
            clinical=False
        ),
        q(
            "What clinical information is obtained by assessing Klisic's line in a child suspected of having a dislocated hip?",
            "A line from the greater trochanter to ASIS normally points to or above umbilicus; in dislocation, it passes below umbilicus",
            ["It measures the carrying angle of the knee in full extension", "It detects rotational torsion of the tibial diaphysis", "It identifies congenital fusion of the cervical vertebrae"],
            "Klisic's line is a quick clinical screening tool for hip dislocation: with the child supine, the examiner places an index finger on the anterior superior iliac spine (ASIS) and the thumb on the tip of the greater trochanter. An imaginary line connecting these points is projected toward the midline. In a normal hip, this line points to or above the umbilicus. In a dislocated hip, the proximal migration of the greater trochanter causes the line to project significantly below the umbilicus.",
            clinical=False
        ),
        q(
            "A 3-year-old child with untreated bilateral DDH walks with a waddling gait and bilateral Trendelenburg sign. What anatomical defect causes this gait?",
            "Proximal migration of greater trochanters shortens abductor lever arm, causing gluteal insufficiency",
            ["Direct transection of superior gluteal nerve during intrauterine development", "Fibrotic contracture of tensor fasciae latae preventing adduction", "Congenital absence of the capital femoral ossification center"],
            "The Trendelenburg gait in DDH is due to abductor insufficiency. Because the femoral head is dislocated superiorly and posteriorly on the iliac wing, the distance between the origin (iliac crest) and insertion (greater trochanter) of the gluteus medius and minimus is drastically shortened. This loses muscle tension and mechanical leverage. When the child stands on the affected leg, the abductors cannot stabilize the pelvis, causing the opposite side of the pelvis to drop.",
            clinical=True
        ),
    ]),

    # Chapter 27: Poliomyelitis and Other Neuromuscular Disorders (Easy - 5 questions)
    (27, "Poliomyelitis and Other Neuromuscular Disorders", "easy", [
        q(
            "A 12-year-old boy with residual poliomyelitis walks by pushing his hand firmly against the anterior thigh during stance phase. What muscle paralysis is this 'hand-to-knee' gait compensating for?",
            "Paralysis of the Quadriceps femoris muscle",
            ["Paralysis of the Gluteus maximus muscle", "Paralysis of the Gastrocnemius and Soleus", "Paralysis of the Tibialis anterior"],
            "The 'hand-to-knee' gait is the classic compensatory mechanism for severe quadriceps paralysis (power Grade 0-2/5) in polio. Normally, the quadriceps contracts during early stance to stabilize the knee against flexion. In quadriceps paralysis, the knee tends to buckle forward under body weight; the patient uses their hand to push the anterior thigh backward, locking the knee into passive hyperextension (recurvatum) to achieve stability.",
            clinical=True
        ),
        q(
            "What three tarsal joints are formally fused in a Triple Arthrodesis for an unstable post-polio flail foot, and what is the minimum recommended age?",
            "Subtalar, Calcaneocuboid, and Talonavicular joints; recommended after age 10 to 12 years",
            ["Tibiotalar, Subtalar, and First metatarsophalangeal joints; recommended at age 3 years", "Talonavicular, Cuneonavicular, and Tarso-metatarsal joints; recommended at age 6 years", "Tibioperoneal, Calcaneocuboid, and Naviculocuneiform joints; recommended at age 18 years"],
            "Triple arthrodesis fuses three joints: 1. Subtalar (talocalcaneal) joint; 2. Calcaneocuboid joint; 3. Talonavicular joint. It permanently eliminates subtalar inversion and eversion, stabilizing a deformed, flail foot into a solid, plantigrade, weight-bearing platform while preserving ankle dorsiflexion/plantarflexion. It is delayed until age 10-12 years because fusing immature cartilaginous tarsal bones stunts foot growth and leads to pseudarthrosis.",
            clinical=False
        ),
        q(
            "A 14-year-old post-polio patient has complete paralysis of the quadriceps (Grade 0/5) with intact Grade 5/5 hamstring strength. What tendon transfer restores active knee extension?",
            "Hamstring transfer (transfer of biceps femoris and/or semitendinosus into the patella)",
            ["Transfer of Achilles tendon directly to the tibial tuberosity", "Transfer of tibialis posterior to the anterior distal femur", "Transfer of tensor fasciae latae to the calcaneus"],
            "When the quadriceps is paralyzed but the flexors (hamstrings) are fully intact and functional (Grade 4 or 5), anterior transfer of one or both hamstrings (most commonly the biceps femoris laterally and/or semitendinosus medially) through the subcutaneous tissue to insert into the superior pole of the patella or patellar tendon converts knee flexors into active knee extensors, eliminating the need for a long-leg brace (KAFO).",
            clinical=True
        ),
        q(
            "What are the three clinical stages of acute anterior poliomyelitis in chronological sequence?",
            "Acute stage (1-4 weeks) -> Convalescent stage (up to 2 years) -> Stage of residual paralysis (after 2 years)",
            ["Stage of spasticity -> Stage of rigidity -> Stage of contracture", "Prodromal stage (1 year) -> Paralytic stage (5 years) -> Recovery stage (10 years)", "Stage of hypertrophy -> Stage of pseudohypertrophy -> Stage of necrosis"],
            "Polio progresses in 3 distinct clinical phases: 1. Acute stage (1-4 weeks): acute systemic enteroviral illness, meningism, intense muscle spasm/tenderness, and asymmetrical flaccid paralysis; 2. Convalescent stage (weeks up to 2 years): acute inflammation subsides, and damaged anterior horn cells recover; maximal muscle recovery occurs in the first 6 months and plateauing by 2 years; 3. Stage of residual paralysis (after 2 years): neurological deficit is permanent; treatment focuses on managing deformities, braces, tendon transfers, and osteotomies/arthrodesis.",
            clinical=False
        ),
        q(
            "A 5-year-old child with spastic diplegic cerebral palsy walks with hips adducted and internally rotated, flexed knees, and equinus feet, causing thighs to cross during ambulation. What is this gait termed?",
            "Scissoring gait",
            ["Trendelenburg gait", "Steppage gait", "Stamping sensory ataxia gait"],
            "A 'scissoring gait' is characteristic of spastic diplegia or quadriplegia in cerebral palsy. Chronic spasticity of the hip adductor muscles (adductor longus, brevis, magnus, and gracilis) pulls the thighs together and causes them to cross in front of each other like the blades of a pair of scissors during the swing phase of walking, accompanied by knee flexion (tight hamstrings) and equinus (tight heel cords).",
            clinical=True
        ),
    ]),

    # Chapter 28: Bone Tumours (HARD - 10 questions)
    (28, "Bone Tumours", "hard", [
        q(
            "A 16-year-old adolescent boy presents with deep, boring pain in his distal thigh and a warm swelling over the distal femur. Plain radiograph shows a mixed osteolytic/sclerotic lesion in the metaphysis, a 'sunburst' periosteal reaction, and Codman's triangle. What is the diagnosis?",
            "Osteosarcoma",
            ["Ewing sarcoma", "Giant cell tumour", "Osteochondroma"],
            "Osteosarcoma is the most common primary malignant bone tumor in children and adolescents (peak incidence 10-20 years, mostly in the metaphyseal regions of the distal femur and proximal tibia). Hallmarks include: mixed lytic/sclerotic bone destruction, malignant osteoid formation, cortical breach, Codman's triangle (triangular cuff of subperiosteal reactive bone at the periphery of cortical breakthrough), and the 'sunburst' appearance (radiating spicules of periosteal new bone).",
            clinical=True
        ),
        q(
            "What pathognomonic chromosomal translocation and immunohistochemical marker characterize Ewing sarcoma?",
            "t(11;22)(q24;q12) translocation generating EWSR1-FLI1 fusion; strong membranous CD99 positivity",
            ["t(9;22)(q34;q11) translocation; positivity for BCR-ABL tyrosine kinase", "t(14;18)(q32;q21) translocation; positivity for BCL2", "t(8;14)(q24;q32) translocation; positivity for c-MYC"],
            "Ewing sarcoma is a malignant small round blue cell tumor of bone. In over 85% to 90% of cases, it is characterized by the reciprocal chromosomal translocation t(11;22)(q24;q12), which fuses the EWSR1 gene on chromosome 22 with the FLI1 gene on chromosome 11, encoding an aberrant chimeric transcription factor. On immunohistochemistry, the malignant cells exhibit diffuse, strong, membranous staining for CD99 (O13 / MIC2).",
            clinical=False
        ),
        q(
            "A 28-year-old female presents with dull knee pain. Radiographs reveal an eccentric, purely osteolytic, 'soap-bubble' lesion in the distal femur epiphysis extending directly to the articular subchondral plate, with no sclerotic rim. What is the diagnosis?",
            "Giant Cell Tumour (GCT / Osteoclastoma)",
            ["Aneurysmal bone cyst", "Chondrosarcoma", "Osteoid osteoma"],
            "Giant Cell Tumour (GCT) occurs characteristically in skeletally mature young adults (20-40 years, slight female predominance) and is strictly located at the EPIPHYSIS of long bones, abutting the articular cartilage (most commonly distal femur, proximal tibia, distal radius). Hallmarks: purely lytic, eccentric, 'soap-bubble' trabeculated appearance, expands and balloons the cortex into an eggshell, and has NO sclerotic rim (differentiating it from chondroblastoma or benign cysts).",
            clinical=True
        ),
        q(
            "A 22-year-old male presents with severe localized femoral shaft pain, worse at night and dramatically relieved by aspirin. CT reveals a 1-cm radiolucent nidus surrounded by intense cortical sclerosis. What is the diagnosis and definitive minimally invasive treatment?",
            "Osteoid osteoma; treated by CT-guided Radiofrequency Ablation (RFA)",
            ["Ewing sarcoma; treated by high-dose multi-agent chemotherapy", "Osteosarcoma; treated by wide-margin limb-salvage resection", "Stress fracture; treated by non-weight-bearing cast for 12 weeks"],
            "Osteoid osteoma is a benign osteoblastic tumor classically presenting in young males with severe nocturnal pain dramatically relieved by salicylates/NSAIDs (which block the extraordinarily high local concentrations of prostaglandins PGE2 and PGI2 produced inside the tumor nidus). Diagnostic hallmark is a small radiolucent nidus (<1.5 cm) surrounded by thick reactive cortical hyperostosis. Percutaneous CT-guided radiofrequency ablation (RFA) is the treatment of choice, achieving >95% cure.",
            clinical=True
        ),
        q(
            "A 14-year-old boy presents with a painless, pedunculated bony outgrowth on the medial distal femur whose cortex and medullary canal are continuous with host bone. What MRI finding raises suspicion of malignant transformation to chondrosarcoma?",
            "Cartilaginous cap thickness exceeding 1.5 to 2.0 cm in a mature skeleton",
            ["Enlargement of the bony pedicle stalk exceeding 5 cm", "Complete calcification of the stalk without soft-tissue edema", "Appearance of endosteal scalloping within the femoral diaphysis"],
            "Osteochondroma is the most common benign bone tumor. It is a developmental exostosis where a growth plate fragment herniates subperiosteally: it is characterized by direct continuity of both the cortex and the medullary cancellous cavity with the parent bone, pointing away from the nearest joint. It is capped by hyaline cartilage. Malignant transformation into secondary chondrosarcoma is heralded by sudden rapid growth or pain in adults; a cartilage cap thickness > 1.5-2 cm on MRI is highly suspicious.",
            clinical=True
        ),
        q(
            "A 16-year-old girl presents with a rapidly enlarging painful proximal tibial swelling. Radiographs show an eccentric osteolytic 'blow-out' lesion. T2-weighted MRI demonstrates internal septations with multiple fluid-fluid levels. What is the diagnosis?",
            "Aneurysmal Bone Cyst (ABC)",
            ["Unicameral (simple) bone cyst", "Giant cell tumour", "Osteoblastoma"],
            "An Aneurysmal Bone Cyst (ABC) is an expansile, osteolytic, vascular lesion containing cavernous blood-filled spaces separated by fibrous septa containing giant cells. It typically affects children and adolescents in the metaphyses of long bones and posterior elements of the spine. Hallmarks: cortical 'blow-out' ballooning and multiple fluid-fluid levels on T2-weighted MRI (caused by settling of cellular blood components beneath unclotted serum/plasma).",
            clinical=True
        ),
        q(
            "A 65-year-old male presents with back pain and anemia. Plain radiographs of the skull demonstrate multiple round, 'punched-out' lytic lesions without reactive sclerosis. Serum electrophoresis shows a monoclonal M-spike. What is the diagnosis?",
            "Multiple myeloma",
            ["Osteoblastic metastatic prostate carcinoma", "Polyostotic fibrous dysplasia", "Hyperparathyroidism with brown tumors"],
            "Multiple myeloma is a malignant neoplasm of plasma cells and is the most common primary malignant bone neoplasm in adults (>50 years). Hallmark features: bone pain, fatigue (anemia), hypercalcemia, renal failure, and elevated ESR. Radiographically, extensive osteoclast-activating factor (OAF/RANKL) secretion causes multiple, sharply circumscribed, 'punched-out' lytic lesions without reactive osteoblastic sclerosis (classically visible in the skull, spine, ribs, and pelvis).",
            clinical=True
        ),
        q(
            "What primary malignancy is most frequently responsible for producing purely osteoblastic (dense, sclerotic) bone metastases in adult males?",
            "Carcinoma of the Prostate",
            ["Renal cell carcinoma", "Thyroid carcinoma", "Bronchogenic squamous cell carcinoma"],
            "Skeletal metastases are either osteolytic, osteoblastic (sclerotic), or mixed. Carcinoma of the prostate is the classic and most common primary tumor that produces purely or predominantly osteoblastic (dense, sclerotic, radiodense) bone metastases in men due to tumor-derived endothelin-1 and bone morphogenetic proteins stimulating osteoblasts. In contrast, renal and thyroid carcinomas produce purely lytic, highly vascular expansile metastases.",
            clinical=False
        ),
        q(
            "A 12-year-old boy presents with fever, leukocytosis, and diaphyseal tibial pain. Radiographs reveal permeative bone destruction with multi-layered 'onion-skin' periosteal reaction. Biopsy reveals uniform small round blue cells with PAS-positive glycogen. What is the diagnosis?",
            "Ewing sarcoma",
            ["Acute pyogenic osteomyelitis", "Eosinophilic granuloma", "Chondromyxoid fibroma"],
            "Ewing sarcoma is a malignant primitive neuroectodermal tumor classically arising in the diaphysis or metadiaphysis of long bones (and pelvis) in children and adolescents (10-15 years). Because it grows rapidly and mimics osteomyelitis (fever, leukocytosis, high ESR), it is frequently misdiagnosed. Radiographically, it causes permeative destruction with multi-layered, concentric subperiosteal bone deposition ('onion-skin' or 'onion-peel' pattern).",
            clinical=True
        ),
        q(
            "A 20-year-old female presents with a pathological fracture of the proximal femur. Radiographs reveal a uniform 'ground-glass' matrix surrounded by a sclerotic rind, with varus remodeling producing a 'shepherd's crook' deformity. What is the diagnosis?",
            "Fibrous dysplasia",
            ["Osteosarcoma", "Paget's disease of bone", "Achondroplasia"],
            "Fibrous dysplasia is a developmental anomaly caused by somatic activating mutations in the GNAS gene, where normal lamellar bone is replaced by cellular fibrous tissue containing immature, curvilinear trabeculae of woven bone ('Chinese character' pattern on histology). Radiographically, it exhibits a classic 'ground-glass' or 'milky haze' appearance, endosteal scalloping, and severe mechanical bowing of the proximal femur into a 'shepherd's crook' deformity.",
            clinical=True
        ),
    ]),

    # Chapter 29: Prolapsed Intervertebral Disc (HARD - 10 questions)
    (29, "Prolapsed Intervertebral Disc", "hard", [
        q(
            "A 42-year-old manual laborer presents with acute low back pain radiating down the posterolateral thigh, lateral calf, and dorsum of the foot to the great toe. Examination reveals weak extensor hallucis longus (EHL) and numbness over the 1st web space, but knee and ankle reflexes are normal. Which disc and nerve root are involved?",
            "L4-L5 disc prolapse compressing the traversing L5 nerve root",
            ["L3-L4 disc prolapse compressing the L4 nerve root", "L5-S1 disc prolapse compressing the S1 nerve root", "L2-L3 disc prolapse compressing the L2 nerve root"],
            "In the lumbar spine, nerve roots exit through the neural foramina beneath the corresponding pedicle (e.g., L4 root exits at L4-L5). A typical posterolateral disc herniation compresses the TRAVERSING nerve root that is crossing down to exit at the next lower level. Therefore, an L4-L5 posterolateral herniation compresses the L5 nerve root: motor deficit is weakness of ankle/great toe dorsiflexion (EHL, EDL, tibialis anterior); sensory loss is over the lateral calf, dorsum of foot, and 1st web space; reflexes are normal (L4 mediates knee jerk, S1 mediates ankle jerk).",
            clinical=True
        ),
        q(
            "In lumbar disc herniation, what anatomical rule governs the nerve root compressed by a posterolateral versus a far-lateral herniation at L5-S1?",
            "Posterolateral herniation compresses traversing S1 root; far-lateral herniation compresses exiting L5 root",
            ["Posterolateral herniation compresses exiting L5 root; far-lateral compresses traversing S1 root", "All lumbar disc herniations compress the exiting root regardless of location", "Far-lateral herniation compresses the traversing L4 root exclusively"],
            "The lumbar canal anatomy dictates root vulnerability: At the L5-S1 interspace, the L5 root has already exited through the foramen beneath the L5 pedicle, while the S1 root is traversing through the lateral recess to exit at S1. A typical posterolateral herniation compresses the traversing S1 root. However, a far-lateral / extra-foraminal herniation (lateral to the pedicle) compresses the EXITING root (L5 root at L5-S1).",
            clinical=False
        ),
        q(
            "A 45-year-old male with sciatica develops sudden urinary retention, overflow incontinence, saddle anesthesia, and lax anal sphincter tone. What emergency condition is this, and what is the definitive management window?",
            "Cauda Equina Syndrome; emergency surgical decompression within 24 to 48 hours",
            ["Meralgia paraesthetica; managed with oral NSAIDs and physical therapy", "Conus medullaris infarction; managed with high-dose intravenous heparin", "Piriformis syndrome; treated with local anesthetic injection into the buttock"],
            "Cauda Equina Syndrome is a true surgical emergency caused by massive central disc herniation or tumor compressing the multi-radicular cauda equina nerve roots below the conus medullaris (L1-L2). Hallmarks: bilateral radicular pain/weakness, saddle anesthesia (S3-S5 dermatomes), urinary retention with overflow incontinence, loss of anal sphincter tone, and fecal incontinence. Urgent decompression within 24-48 hours is mandatory to avoid irreversible bladder/bowel paralysis and sexual dysfunction.",
            clinical=True
        ),
        q(
            "During the Straight Leg Raising Test (SLRT / Lasegue's sign), what angular elevation range is mechanically specific for stretching the L5 and S1 nerve roots against a herniated disc?",
            "Pain radiating below the knee between 30 and 70 degrees of elevation",
            ["Pain felt only between 0 and 15 degrees", "Pain elicited strictly between 85 and 90 degrees", "Pain appearing only when the leg is lowered back to the bed"],
            "In the Straight Leg Raise Test (SLRT): Between 0 and 30 degrees, the nerve roots are completely slack; between 30 and 70 degrees, the L5 and S1 roots and sciatic nerve undergo maximal tension and excursion over the ventral disc margins; pain radiating below the knee into the dermatome between 30 and 70 degrees is a positive test. Pain beyond 70 degrees is typically non-specific hamstring tightness.",
            clinical=False
        ),
        q(
            "What clinical significance is attributed to a positive Crossed Straight Leg Raising Test (Fajersztajn's sign) in lumbar sciatica?",
            "Elevating the unaffected leg reproduces sciatica in the symptomatic leg; highly specific for a large disc herniation",
            ["It proves the presence of malingering and non-organic pain magnification", "It indicates an isolated piriformis muscle spasm", "It indicates an intra-articular tear of the contralateral hip acetabular labrum"],
            "The Crossed SLRT (Fajersztajn's test) is performed by elevating the patient's normal, unaffected lower extremity. When elevating the healthy leg produces typical radicular shooting pain down the symptomatic opposite leg, the test is positive. This occurs because traction on the contralateral roots pulls the entire dural sac and the axilla of the compressed nerve root against the herniated disc fragment. It is highly specific (over 90%) for a significant disc herniation.",
            clinical=False
        ),
        q(
            "What morphological feature differentiates an extruded intervertebral disc from a sequestrated disc?",
            "Extruded nuclear material remains attached to the parent disc; sequestrated fragment is completely detached and free",
            ["Extruded disc has an intact annulus; sequestrated disc has a calcified nucleus", "Extruded disc maintains intact posterior ligament; sequestrated disc is strictly intradural", "Extruded disc lies anteriorly; sequestrated disc lies inside the vertebral marrow"],
            "Disc herniation pathology progresses through 4 stages: 1. Bulge (diffuse annular extension); 2. Protrusion (focal herniation, annulus stretched but intact); 3. Extrusion (nucleus pulposus breaks through the annulus fibrosus and posterior longitudinal ligament into the canal, but maintains continuous connection with the central disc space); 4. Sequestration (the extruded nuclear fragment breaks free, losing all continuity with the parent disc, and can migrate cranially or caudally in the epidural space).",
            clinical=False
        ),
        q(
            "A 38-year-old female presents with pain shooting down the posterior calf to the heel and lateral foot. She is unable to walk on tiptoes, has weak gastrocnemius-soleus power, numbness along the lateral foot, and an absent Achilles jerk. Which disc and root are affected?",
            "L5-S1 disc prolapse compressing the S1 nerve root",
            ["L4-L5 disc prolapse compressing the L5 nerve root", "L3-L4 disc prolapse compressing the L4 nerve root", "L2-L3 disc prolapse compressing the L3 nerve root"],
            "S1 radiculopathy is classically caused by an L5-S1 posterolateral disc prolapse: 1. Motor: Weakness of ankle plantarflexion (gastrocnemius-soleus), making the patient unable to walk on tiptoes or perform single-leg heel raises; 2. Sensory: Numbness over the posterolateral calf, lateral malleolus, lateral border of foot, and little toe; 3. Reflex: Depressed or absent Achilles tendon jerk (S1 deep tendon reflex).",
            clinical=True
        ),
        q(
            "A 46-year-old male presents with neck pain radiating down the lateral arm to the thumb and index finger, with weakness of the biceps and diminished biceps reflex. Which cervical disc and root are compressed?",
            "C5-C6 cervical disc herniation compressing the C6 nerve root",
            ["C4-C5 cervical disc herniation compressing the C5 nerve root", "C6-C7 cervical disc herniation compressing the C7 nerve root", "C7-T1 cervical disc herniation compressing the C8 nerve root"],
            "In the cervical spine, nerve roots exit ABOVE the pedicle of the same-numbered vertebra (e.g., C6 root exits between C5 and C6). A C5-C6 disc prolapse compresses the exiting C6 nerve root. Clinical syndrome of C6 radiculopathy: 1. Motor: Weakness of elbow flexion and wrist extension (biceps, brachioradialis, extensor carpi radialis); 2. Sensory: Numbness over the radial forearm, thumb, and index finger; 3. Reflex: Diminished or absent biceps and brachioradialis tendon reflexes.",
            clinical=True
        ),
        q(
            "What clinical feature reliably differentiates neurogenic claudication (lumbar stenosis) from vascular claudication?",
            "Neurogenic claudication is relieved by lumbar flexion (leaning forward on a cart); vascular claudication is relieved simply by standing still",
            ["Neurogenic claudication is associated with completely absent pedal pulses", "Neurogenic claudication pain begins in the toes and never ascends to buttocks", "Vascular claudication causes a straight leg raise limited to 20 degrees"],
            "Neurogenic claudication (pseudoclaudication) is posture-dependent: lumbar extension narrows the spinal canal and neural foramina, exacerbating root ischemia; lumbar flexion widens the canal by 15-20%, relieving symptoms. Patients find walking downhill painful (extension) and walking uphill or pushing a cart comfortable ('shopping cart sign'). In vascular claudication, muscle ischemia depends strictly on workload; pain stops immediately upon resting in any posture, and pedal pulses are diminished or absent.",
            clinical=False
        ),
        q(
            "What imaging modality represents the definitive investigation of choice for confirming the level, morphology, and neural compression of a lumbar disc herniation?",
            "Magnetic Resonance Imaging (MRI) of the lumbosacral spine",
            ["Standing plain radiographs of the lumbar spine", "CT myelography following lumbar puncture", "Dynamic lateral flexion-extension radiographs"],
            "MRI is the gold standard and investigation of choice for prolapsed intervertebral disc. It provides non-invasive, high-contrast visualization of the nucleus pulposus, annulus fibrosus, posterior longitudinal ligament, epidural space, thecal sac, and exiting/traversing nerve roots in both sagittal and axial planes, accurately identifying the degree of stenosis, disc hydration (T2 darkening), and distinguishing disc extrusion from sequestration or tumors.",
            clinical=False
        ),
    ]),

    # Chapter 30: Approach to a Patient with Back Pain (Easy - 5 questions)
    (30, "Approach to a Patient with Back Pain", "easy", [
        q(
            "Which clinical features represent 'red flags' in acute low back pain that mandate immediate laboratory and radiological investigation?",
            "Age < 20 or > 50, nocturnal pain unrelieved by rest, weight loss, fever, and progressive neurological deficit",
            ["Pain aggravated by forward bending and relieved by lying supine", "Morning stiffness lasting 10 minutes that improves with walking", "Localized paraspinal soreness after unaccustomed physical activity"],
            "'Red flag' features in back pain warrant immediate urgent investigation (MRI, ESR/CRP, radiographs) to exclude systemic infection (TB, epidural abscess), neoplasm (metastases, myeloma), or cauda equina syndrome. Red flags include: 1. Age < 20 or > 50 years; 2. History of cancer; 3. Unexplained weight loss; 4. Fever/chills; 5. Pain that is constant, progressive, severe at night, and NOT relieved by rest; 6. Neurological deficit or sphincter disturbance.",
            clinical=True
        ),
        q(
            "What do Waddell's non-organic signs evaluate in a patient with chronic low back pain?",
            "Psychological distress and non-organic behavioral symptom magnification",
            ["The exact depth of disc extrusion on plain radiographs", "The presence of occult sacroiliac joint infections", "The degree of true structural rotational scoliosis"],
            "Waddell's signs identify patients whose back pain is influenced by non-organic, psychological, or behavioral factors. The 5 categories are: 1. Tenderness (superficial skin pinch or non-anatomical tenderness); 2. Simulation (axial loading of skull or simulated pelvis rotation produces back pain); 3. Distraction (formal SLRT is markedly restricted, but sitting distracted knee extension is normal); 4. Regional disturbances (stocking-glove sensory loss or cogwheel weakness); 5. Overreaction. >= 3 positive signs indicate non-organic behavior.",
            clinical=False
        ),
        q(
            "What pain pattern distinguishes inflammatory back pain (e.g., Ankylosing Spondylitis) from mechanical back pain?",
            "Onset before age 40, morning stiffness > 30 minutes, worsening with rest, and improvement with activity",
            ["Sudden onset after lifting, worsening with exercise, and complete relief with bed rest", "Severe nocturnal pain awakening the patient only when turning on their side", "Unilateral pain radiating below the knee with normal ESR and CRP"],
            "Mechanical back pain is exacerbated by physical activity, lifting, and prolonged standing, and is relieved by rest and lying flat; morning stiffness is absent or brief (<15-20 min). Inflammatory back pain (spondyloarthritis) begins insidiously before age 40, causes severe prolonged morning stiffness (>30-60 min), worsens with rest and inactivity, awakens the patient in the second half of the night, and dramatically improves with physical exercise.",
            clinical=False
        ),
        q(
            "In the FABER (Patrick's) test, how is the hip positioned, and where is pain elicited if the sacroiliac joint is diseased?",
            "Flexion, ABduction, and External Rotation; pressing down on the knee elicits pain posteriorly in the sacroiliac joint",
            ["Extension, ADduction, and Internal Rotation; elicits pain in the anterior groin", "Flexion and Internal Rotation; elicits pain in the greater sciatic notch", "Hyperextension with knee flexed; elicits pain along the femoral nerve"],
            "The FABER test (Flexion, ABduction, External Rotation) or Patrick's test evaluates the sacroiliac joint and hip joint. The patient lies supine; the foot of the tested side is placed on the opposite knee (forming a 'figure 4'). The examiner stabilizes the opposite ASIS and presses downward on the flexed knee. Pain elicited in the groin indicates hip pathology; pain elicited posteriorly in the sacroiliac region indicates sacroiliac joint disease/sacroiliitis.",
            clinical=True
        ),
        q(
            "In Schober's test for measuring lumbar spine flexion in suspected ankylosing spondylitis, what is the normal expected increase in distance between marks during forward bending?",
            "An increase of at least 5 cm (e.g., 10 cm expands to >= 15 cm)",
            ["An increase of at least 15 cm", "An increase of exactly 1 cm only", "Zero expansion occurs in normal human spines"],
            "Schober's test measures lumbar flexion: With the patient standing erect, a mark is made at the lumbosacral junction (level of dimples of Venus / S2) and a second mark 10 cm directly above it in the midline (modified Schober also adds a mark 5 cm below, total distance 15 cm). The patient flexes forward fully with knees straight. In a normal spine, the 10 cm distance increases by at least 5 cm (to >= 15 cm). An expansion of < 5 cm indicates pathologically restricted lumbar excursion (classic in ankylosing spondylitis).",
            clinical=False
        ),
    ]),

    # Chapter 31: Spinal Injuries (HARD - 10 questions)
    (31, "Spinal Injuries", "hard", [
        q(
            "According to the Denis three-column classification of spinal stability, which structures constitute the Middle Column?",
            "Posterior longitudinal ligament, posterior half of vertebral body, and posterior annulus fibrosus",
            ["Anterior longitudinal ligament, anterior half of vertebral body, and anterior annulus", "Supraspinous ligament, interspinous ligament, ligamentum flavum, and spinous processes", "Facet joints, pedicles, and transverse processes"],
            "Denis divided the spine into three biomechanical columns: 1. Anterior Column: Anterior longitudinal ligament (ALL), anterior half of vertebral body, and anterior annulus fibrosus; 2. Middle Column: Posterior longitudinal ligament (PLL), posterior half of vertebral body, and posterior annulus fibrosus; 3. Posterior Column: Bony neural arch (pedicles, laminae, facet joints, spinous processes) and the posterior ligamentous complex (ligamentum flavum, interspinous, and supraspinous ligaments).",
            clinical=False
        ),
        q(
            "In Denis's model of thoracolumbar trauma, what criterion defines an acute injury as mechanically unstable?",
            "Disruption of at least two columns, or any structural failure involving the middle column",
            ["Isolated fracture of a single transverse process", "Mild anterior compression of 10% of vertebral body with intact middle column", "Isolated stretching of the supraspinous ligament"],
            "The Middle Column is the key stabilizer of the spine. Under Denis's model, a spinal fracture is deemed unstable if two or more columns have failed, or whenever the middle column is disrupted (in tension or compression). For example, a simple wedge compression fracture involves only the anterior column (stable); a burst fracture disrupts both the anterior and middle columns (unstable).",
            clinical=False
        ),
        q(
            "A 24-year-old wearing a lap-only seatbelt sustains a flexion-distraction injury across L2. Radiographs show horizontal splitting of the posterior arch and middle column. What is this fracture termed, and what associated injury must be ruled out?",
            "Chance fracture; high incidence of intra-abdominal hollow viscus perforation",
            ["Jefferson fracture; high incidence of vertebral artery transection", "Hangman's fracture; high incidence of esophageal rupture", "Clay-shoveler's fracture; high incidence of apical lung puncture"],
            "A Chance fracture is a flexion-distraction injury classically caused by a lap seatbelt: the axis of flexion rotates around an anterior fulcrum (the seatbelt over the anterior abdominal wall). Tensile distraction forces rip horizontally through the posterior bony arch/ligaments and middle column, with compression/splitting of the anterior vertebral body. Up to 50% of patients have associated intra-abdominal injuries (bowel perforation, mesenteric tears, pancreatic/splenic lacerations).",
            clinical=True
        ),
        q(
            "What is the key pathological difference between a burst fracture and a simple wedge compression fracture?",
            "Burst fractures disrupt both anterior and middle columns with retropulsion; compression fractures involve only the anterior column",
            ["Burst fractures occur only in cervical spine; compression fractures occur only in sacrum", "Burst fractures never cause neurological deficit; compression fractures cause total paraplegia", "Burst fractures are purely ligamentous injuries without bony fracture"],
            "Both injuries result from axial loading. In a simple wedge compression fracture, failure is restricted to the anterior column (anterior cortex collapses into a wedge), while the middle column remains intact and acts as a hinge, preventing posterior retropulsion and preserving the spinal canal. In a burst fracture, the axial force crushes the middle column as well as the anterior column, retropulsing posterosuperior bone fragments into the spinal canal, risking neurological injury.",
            clinical=False
        ),
        q(
            "A male dives into shallow water and strikes his head. CT reveals a four-part burst fracture involving bilateral fractures of both the anterior and posterior arches of C1. What eponymic injury is this?",
            "Jefferson fracture of the atlas (C1)",
            ["Hangman's fracture of the axis (C2)", "Clay-shoveler's fracture of C7", "Teardrop fracture of C5"],
            "A Jefferson fracture is an axial-loading compressive burst fracture of the atlas (C1). The axial force drives the wedge-shaped occipital condyles downward into the lateral masses of C1, bursting the ring outward into bilateral fractures of the anterior and posterior arches (producing 4 distinct fractures). On an open-mouth odontoid radiograph, lateral displacement (overhang) of both C1 lateral masses relative to C2 exceeding a combined total of 7 mm indicates rupture of the transverse atlantal ligament.",
            clinical=True
        ),
        q(
            "What anatomical lesion defines a Hangman's fracture of the cervical spine?",
            "Bilateral fractures through the pars interarticularis (neural arch) of C2",
            ["Fracture through the waist of the dens with anterior atlantoaxial subluxation", "Complete avulsion of the transverse atlantal ligament without bony fracture", "Compression burst fracture of the body of C3 with retropulsion"],
            "A Hangman's fracture (traumatic spondylolisthesis of C2) is caused by hyperextension and distraction (historically seen in judicial hanging; today seen in motor vehicle crashes when the forehead strikes the windshield). The bilateral pars interarticularis (isthmus) of C2 fractures, dissociating the anterior body of C2 from its posterior neural arch. Because the neural canal expands at this level, cord compression is surprisingly infrequent unless severe displacement occurs.",
            clinical=False
        ),
        q(
            "In the Anderson and D'Alonzo classification of odontoid fractures, which type traverses the waist (base) of the dens and has the highest non-union rate?",
            "Type II odontoid fracture",
            ["Type I odontoid fracture", "Type III odontoid fracture", "Type IV odontoid fracture"],
            "Anderson and D'Alonzo classified odontoid fractures into 3 types: Type I: Avulsion fracture of the apex/tip of the dens (stable); Type II: Fracture through the base/waist of the dens where it joins the body of C2 (most common, highly unstable, and prone to non-union due to poor blood supply and high shear); Type III: Fracture extending down into the vascular cancellous body of C2 (unites readily with halo-vest or cervical collar).",
            clinical=False
        ),
        q(
            "A road worker feels sudden sharp interscapular pain while vigorously shoveling gravel. Radiographs show an isolated avulsion fracture of the C7 spinous process. What is this fracture termed?",
            "Clay-shoveler's fracture",
            ["Hangman's fracture", "Chance fracture", "Teardrop fracture"],
            "A Clay-shoveler's fracture is an isolated avulsion fracture of the spinous process of a lower cervical or upper thoracic vertebra (most commonly C7, followed by C6 and T1). It is caused by violent, sudden contraction of the trapezius, rhomboid, and serratus posterior superior muscles pulling against the supraspinous ligament during heavy lifting or shoveling. It is a stable injury managed conservatively with analgesia and a soft collar.",
            clinical=True
        ),
        q(
            "According to the ASIA Impairment Scale, how is an ASIA Grade B injury defined?",
            "Sensory but no motor function preserved below the neurological level, including sacral segments S4-S5",
            ["Complete absence of all motor and sensory function in sacral segments S4-S5", "Motor function preserved with more than half of key muscles having grade >= 3/5", "Normal motor and sensory function throughout all dermatomes and myotomes"],
            "ASIA Impairment Scale grades spinal cord injury: Grade A (Complete): No motor or sensory function preserved in sacral segments S4-S5; Grade B (Sensory Incomplete): Sensory but NO motor function preserved below the neurological level, including sacral segments S4-S5; Grade C (Motor Incomplete): Motor function preserved below level, with more than half of key muscles having a muscle grade < 3/5; Grade D (Motor Incomplete): At least half of key muscles have a grade >= 3/5; Grade E: Normal.",
            clinical=False
        ),
        q(
            "According to the NEXUS criteria, what five findings allow safe clinical clearance of the cervical spine without imaging?",
            "No midline cervical tenderness, no focal neurological deficit, normal alertness, no intoxication, and no distracting injury",
            ["Normal blood pressure, absence of skull fracture, reactive pupils, age under 40, and negative toxicology", "Patient able to walk, no facial laceration, heart rate < 100, normal hemoglobin, and normal chest X-ray", "Cervical flexion to 90 degrees, negative Hoffman sign, intact gag reflex, normal gait, and no ear bleeding"],
            "The NEXUS low-risk criteria allow safe clinical clearance of the cervical spine without imaging if the patient meets ALL 5 criteria: 1. No posterior midline cervical spine tenderness; 2. No focal neurological deficits; 3. Normal alertness (GCS 15); 4. No evidence of alcohol or drug intoxication; 5. No painful distracting injuries (e.g., long bone fractures, large burns, visceral injuries) that could mask neck pain. If any criterion is failed, imaging is mandatory.",
            clinical=False
        ),
    ]),

    # Chapter 32: Traumatic Paraplegia (HARD - 10 questions)
    (32, "Traumatic Paraplegia", "hard", [
        q(
            "A trauma patient with a T6 cord injury has complete flaccid motor paralysis, total anesthesia below T6, absent deep tendon reflexes, and an absent bulbocavernosus reflex. What physiological state is this?",
            "Spinal shock",
            ["Neurogenic shock", "Established spastic paraplegia", "Autonomic dysreflexia"],
            "Spinal shock is the immediate, transient physiological cessation of all spinal cord reflex activity below the level of a severe acute cord transection or contusion. Hallmarks: complete flaccid paralysis, total anesthesia, loss of autonomic tone, absent deep tendon reflexes, and loss of visceral reflexes (areflexic neurogenic bladder, loss of bulbocavernosus reflex and anal wink). It typically lasts from 24 to 48 hours up to several weeks.",
            clinical=True
        ),
        q(
            "What physiological event and reflex recovery officially marks the termination of spinal shock?",
            "Return of the Bulbocavernosus reflex",
            ["Spontaneous recovery of voluntary great toe extension", "Return of the patellar tendon jerk alone", "Cessation of all orthostatic hypotension"],
            "The termination of spinal shock is officially defined by the return of the bulbocavernosus reflex (elicited by squeezing the glans penis or tugging on the Foley catheter while feeling for reflex contraction of the external anal sphincter via digital rectal examination). Once the bulbocavernosus reflex returns, any persistent absence of motor and sensory function indicates a true, permanent 'complete' spinal cord injury (ASIA A).",
            clinical=False
        ),
        q(
            "A patient with acute C5 cervical trauma presents with hypotension (BP 75/45 mmHg), bradycardia (HR 46 bpm), and warm, dry skin. What is the diagnosis and mechanism?",
            "Neurogenic shock; disruption of descending sympathetic pathways causing unopposed vagal tone and vasodilation",
            ["Spinal shock; direct traumatic loss of reflex arc motor neurons", "Hypovolemic shock; occult internal hemorrhage into the retroperitoneum", "Cardiogenic shock; direct blunt traumatic myocardial contusion"],
            "Neurogenic shock (a form of distributive shock) occurs in acute spinal cord injuries at or above T6. Interruption of the descending sympathetic pathways from the brainstem leaves parasympathetic (vagal) innervation to the heart unopposed, producing the classic combination of profound hypotension (arteriolar and venous vasodilation with peripheral blood pooling) AND bradycardia. Unlike hypovolemic shock (cold, clammy, tachycardic), the skin in neurogenic shock is warm, dry, and flushed.",
            clinical=True
        ),
        q(
            "A 68-year-old male with cervical spondylosis falls forward striking his forehead (hyperextension injury). He has severe motor weakness in both arms and hands (Grade 1/5) but preserved leg strength (Grade 4/5). What syndrome is this?",
            "Central Cord Syndrome",
            ["Anterior Spinal Cord Syndrome", "Brown-Séquard Syndrome", "Posterior Cord Syndrome"],
            "Central Cord Syndrome is the most common incomplete cervical cord injury. It classically occurs in elderly individuals with pre-existing cervical spondylosis following a hyperextension injury: the cord is pinched anteriorly by osteophytes and posteriorly by the buckled ligamentum flavum. Because the cervical somatotopic fibers of the lateral corticospinal tracts lie centrally while sacral and lumbar fibers lie peripherally, the upper extremities (especially the hands) suffer severe motor deficit while lower extremity motor function is largely spared.",
            clinical=True
        ),
        q(
            "A patient sustains a penetrating stab wound causing hemisection of the right thoracic spinal cord (T8). What pattern of deficits defines Brown-Séquard syndrome below the lesion?",
            "Ipsilateral motor paralysis and proprioception loss, with contralateral loss of pain and temperature",
            ["Bilateral total motor paralysis with complete preservation of pain and temperature", "Contralateral motor paralysis with ipsilateral loss of pain and temperature", "Bilateral loss of all sensory modalities with preserved voluntary motor power"],
            "Brown-Séquard syndrome (spinal cord hemisection): 1. Ipsilateral to lesion: Loss of voluntary motor function below lesion (corticospinal tract crosses at medulla); loss of proprioception, vibration, and fine touch (dorsal columns ascend uncrossed to medulla); 2. Contralateral to lesion: Loss of pain and temperature sensation beginning 1-2 segments below the lesion (spinothalamic tract fibers cross the midline 1-2 segments above their entry).",
            clinical=True
        ),
        q(
            "In Anterior Spinal Artery Syndrome resulting from retropulsion of a burst fracture, which sensory modalities are classically PRESERVED below the lesion?",
            "Proprioception, vibration sensation, and deep light touch (posterior columns)",
            ["Pain and temperature sensation exclusively", "Crude touch and thermal discrimination", "No sensory modalities are preserved"],
            "The anterior spinal artery supplies the anterior two-thirds of the spinal cord (anterior horns, corticospinal tracts, and spinothalamic tracts). Occlusion or compression produces complete bilateral motor paralysis below the lesion and total loss of pain and temperature sensation. However, the posterior one-third of the cord (dorsal columns: fasciculus gracilis and cuneatus) is supplied by the paired posterior spinal arteries, completely preserving proprioception, vibration, and deep light touch.",
            clinical=False
        ),
        q(
            "A patient with chronic T4 paraplegia develops pounding headache, facial sweating/flushing, severe hypertension (BP 210/110 mmHg), and bradycardia (HR 48 bpm). What is this condition and its most common trigger?",
            "Autonomic dysreflexia; most commonly triggered by acute bladder distension or fecal impaction",
            ["Addisonian adrenal crisis; triggered by corticosteroid withdrawal", "Pheochromocytoma crisis; triggered by abdominal palpation", "Acute pulmonary embolism; triggered by deep vein thrombosis"],
            "Autonomic dysreflexia occurs in patients with spinal cord lesions at or above T6. Noxious visceral stimuli below the lesion (overwhelmingly a distended, blocked urinary bladder in >80%, or fecal impaction) trigger massive, uninhibited sympathetic discharge from isolated thoracolumbar splanchnic nerves, causing severe vasoconstriction and life-threatening hypertension. Baroreceptors in the carotid sinus detect the hypertension and stimulate vagal bradycardia, but the descending inhibitory impulses cannot cross the cord lesion.",
            clinical=True
        ),
        q(
            "What has historically been the most common cause of long-term mortality in chronic traumatic paraplegia?",
            "Renal failure and urosepsis secondary to chronic neurogenic bladder dysfunction",
            ["Acute traumatic aortic aneurysm rupture", "Secondary osteosarcoma at the fracture site", "Congestive heart failure from lower limb disuse"],
            "Chronic neurogenic bladder (spastic reflexic or flaccid) leads to high intravesical pressures, vesicoureteral reflux, staghorn calculi, chronic pyelonephritis, renal amyloidosis, and lethal urosepsis. The introduction of clean intermittent catheterization (CIC), urodynamic monitoring, anticholinergics, and strict urinary surveillance revolutionized paraplegic life expectancy, shifting mortality towards respiratory and cardiovascular causes.",
            clinical=False
        ),
        q(
            "During the acute spinal shock stage, what is the standard method for managing the neurogenic bladder to prevent detrusor overstretching?",
            "Clean Intermittent Catheterization (CIC) maintaining bladder volume below 400 to 500 mL",
            ["Suprapubic cystostomy without monitoring bladder filling volumes", "Credé manual compression of the lower abdomen every 2 hours", "Continuous irrigation with normal saline through a three-way catheter at 500 mL/hr"],
            "During spinal shock, the bladder is completely flaccid and acontractile; failure to decompress results in painless overdistension, stretching the detrusor muscle beyond its elastic limit, causing permanent myogenic damage and bladder rupture. Clean Intermittent Catheterization (CIC) every 4-6 hours (maintaining bladder volumes < 400-500 mL) is the standard method, minimizing infection rates compared to long-term indwelling catheters.",
            clinical=False
        ),
        q(
            "What clinical finding constitutes 'Sacral Sparing' in acute spinal cord trauma, and why is it of major prognostic importance?",
            "Preservation of perianal sensation, voluntary anal contraction, or toe flexion; proves incomplete injury with higher recovery potential",
            ["Presence of normal deep tendon knee reflexes with absent sensation", "Return of the cremasteric reflex within 1 hour of trauma", "Intact motor power in the upper extremities only"],
            "Sacral sparing is the hallmark of an incomplete spinal cord injury. Because sacral motor and sensory tracts (corticospinal and spinothalamic) run in the most peripheral, superficial rim of the spinal cord, they are the last to be damaged by central or expanding lesions. The presence of any sacral sparing (perianal sensation, voluntary anal sphincter contraction, deep anal sensation) proves axonal continuity across the injury site and predicts a favorable prognosis for walking recovery.",
            clinical=False
        ),
    ]),
]
