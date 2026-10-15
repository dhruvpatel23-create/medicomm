from .common import q

CHAPTERS = [
    # Chapter 33: Scoliosis and Other Spinal Deformities (Easy - 5 questions)
    (33, "Scoliosis and Other Spinal Deformities", "easy", [
        q(
            "A 13-year-old girl is noted by her mother to have uneven shoulder levels and a prominent right scapula. During the clinical examination, the patient is asked to bend forward at the waist with knees straight and arms hanging freely (Adam's forward bend test). A prominent rotational rib hump is immediately accentuated on the right thoracic region. What is the diagnostic significance of this test?",
            "Differentiates structural from postural scoliosis",
            ["Quantifies lumbar spondylolisthesis", "Detects active spinal tuberculosis", "Evaluates tethered cord syndrome"],
            "Adam's forward bend test is the cardinal clinical screening test for structural scoliosis. In a postural (functional) scoliosis, the spinal curvature straightens out on forward bending. In a structural scoliosis, the vertebral bodies are fixed in rotation (spinous processes rotated toward the concavity, vertebral bodies and ribs pushed toward the convexity), producing an asymmetric rib prominence or 'rib hump' on the convex side that accentuates during forward flexion.",
            clinical=True
        ),
        q(
            "How is the Cobb angle formally measured on a standing whole-spine anteroposterior radiograph to quantify the severity of a scoliotic curve?",
            "Angle between perpendiculars of upper and lower endplate lines of end-vertebrae",
            ["Distance between C7 plumb line and gluteal cleft", "Angle connecting transverse process tips on convexity", "Angle between L1 superior endplate and sacral promontory"],
            "To measure Cobb's angle: 1. Identify the 'end-vertebrae' (the most tilted vertebrae at the upper and lower limits of the curve, whose endplates tilt most severely toward the concavity of the curve); 2. Draw a line along the superior endplate of the upper end-vertebra; 3. Draw a line along the inferior endplate of the lower end-vertebra; 4. The angle formed at the intersection of these lines (or perpendiculars drawn from them) is the Cobb angle.",
            clinical=False
        ),
        q(
            "What skeletal maturity parameter is assessed by the Risser sign on a standing pelvic radiograph, and why is a Risser Grade 0 or 1 associated with high clinical concern in adolescent idiopathic scoliosis?",
            "Iliac crest apophysis ossification; indicates significant remaining spinal growth",
            ["Ischial tuberosity fusion; marks completion of all spinal growth", "Triradiate cartilage closure; marks cessation of curve progression", "Greater trochanter ossification; marks need for halo traction"],
            "The Risser sign grades the progressive ossification of the iliac apophysis across 4 quadrants from anterolateral to posteromedial: Grade 0 (no ossification); Grade 1 (first 25% ossified); Grade 2 (50%); Grade 3 (75%); Grade 4 (100% excursion across iliac crest); Grade 5 (complete bony fusion to the ilium). A Risser grade of 0 or 1 during the adolescent growth spurt indicates substantial remaining spinal growth and a very high risk of rapid curve progression.",
            clinical=True
        ),
        q(
            "According to standard orthopaedic guidelines, what is the management threshold for an adolescent idiopathic scoliosis (AIS) curve based on Cobb angle in a skeletally immature patient (Risser 0-2)?",
            "Observation for <20 degrees; bracing for 20-40 degrees; surgery for >45-50 degrees",
            ["Surgery for <20 degrees; observation for >40 degrees", "Bed rest for <30 degrees; plaster cast for >40 degrees", "Electrical stimulation alone for all curve magnitudes"],
            "Management of AIS depends on Cobb angle and skeletal maturity: 1. Curves < 20 degrees: Observation with serial radiographs every 4-6 months; 2. Curves 20 to 40 degrees in a growing child (Risser 0-2): Rigid spinal orthosis/bracing (e.g., Boston thoracolumbosacral orthosis or Milwaukee brace worn 18-23 hours/day) to prevent further progression; 3. Curves exceeding 45-50 degrees: Surgical correction with posterior spinal instrumentation and fusion.",
            clinical=False
        ),
        q(
            "In Meyerding's classification of spondylolisthesis (forward slip of one vertebra over the one below), what percentage of anterior displacement of the L5 vertebral body on the S1 sacral base defines a 'Grade II' slip?",
            "26% to 50% displacement",
            ["0% to 25% displacement", "51% to 75% displacement", "76% to 100% displacement"],
            "Meyerding classified spondylolisthesis by dividing the superior sacral plateau into 4 quarters: Grade I: 0% to 25% forward slip of the superior vertebra; Grade II: 26% to 50% forward slip; Grade III: 51% to 75% forward slip; Grade IV: 76% to 100% forward slip; Grade V (Spondyloptosis): Complete displacement (>100%), where the L5 vertebra slips completely off the sacral promontory into the pelvic cavity.",
            clinical=False
        ),
    ]),

    # Chapter 34: Arthritis and Related Diseases (HARD - 10 questions)
    (34, "Arthritis and Related Diseases", "hard", [
        q(
            "A 36-year-old female presents with persistent, symmetrical pain and swelling in both hands, wrists, and knees for 4 months. She suffers from profound morning stiffness lasting over 90 minutes. Examination reveals tender, spongy synovitis involving the Metacarpophalangeal (MCP) and Proximal Interphalangeal (PIP) joints, but the Distal Interphalangeal (DIP) joints are completely spared. Laboratory testing reveals high-titer anti-cyclic citrullinated peptide (anti-CCP) antibodies. What is the diagnosis?",
            "Rheumatoid arthritis",
            ["Primary osteoarthritis", "Systemic lupus erythematosus", "Acute gouty arthritis"],
            "Rheumatoid arthritis is a chronic, systemic autoimmune inflammatory polyarthritis characterized by bilateral, symmetrical synovitis classically targeting the small joints of the hands and feet (MCP, PIP, MTP joints and wrists) while characteristically SPARING the DIP joints (unlike osteoarthritis and psoriatic arthritis). Prolonged morning stiffness (>1 hour) is a hallmark. Anti-CCP antibodies possess >95% specificity for RA.",
            clinical=True
        ),
        q(
            "What is the underlying pathomechanics differentiating a 'Swan-neck deformity' from a 'Boutonnière deformity' of the fingers in chronic rheumatoid arthritis?",
            "Swan-neck: PIP hyperextension with DIP flexion; Boutonnière: PIP flexion with DIP hyperextension",
            ["Swan-neck: DIP hyperextension with PIP flexion; Boutonnière: MCP dislocation", "Swan-neck: FDP tendon rupture; Boutonnière: Lumbrical contracture", "Swan-neck: FDS tendon avulsion; Boutonnière: Extensor hood avulsion"],
            "In RA hand deformities: 1. Swan-neck deformity: Laxity or rupture of the volar plate at the PIP joint allows the lateral bands to subluxate dorsally, producing PIP hyperextension; the tight FDP then pulls the DIP into secondary flexion; 2. Boutonnière deformity: Synovitis distends the PIP joint, causing rupture or stretching of the central slip of the extensor tendon; the lateral bands slip volarly below the axis of the PIP joint, acting as flexors of the PIP joint while hyperextending the DIP joint.",
            clinical=False
        ),
        q(
            "A 24-year-old man presents with chronic, insidious low back pain and morning stiffness for 8 months that improves with exercise and worsens with rest. He has alternating buttock pain and reduced chest expansion measuring only 1.8 cm. Radiographs reveal bilateral symmetrical sacroiliitis and squaring of the lumbar vertebral bodies. HLA-B27 is strongly positive. What is the diagnosis?",
            "Ankylosing spondylitis",
            ["Degenerative lumbar canal stenosis", "Scheuermann disease", "Diffuse idiopathic skeletal hyperostosis"],
            "Ankylosing spondylitis is a chronic inflammatory seronegative spondyloarthropathy strongly associated with HLA-B27 (>90%). It characteristically affects young adult males (peak 20-30 years). Cardinal features: bilateral symmetrical sacroiliitis (earliest and mandatory diagnostic feature), inflammatory back pain, diminished chest expansion (<2.5 cm at the 4th intercostal space due to costovertebral joint ankylosis), vertebral squaring, and ascending spinal fusion.",
            clinical=True
        ),
        q(
            "What classic radiological features characterize advanced, 'end-stage' Ankylosing Spondylitis on anteroposterior and lateral radiographs of the spine?",
            "Bamboo spine, dagger sign, and trolley-track sign",
            ["Diffuse punched-out lytic lesions with vertebral collapse", "Flowing anterior hyperostosis preserving disc heights", "Multiple Schmorl nodes with anterior wedging"],
            "In advanced ankylosing spondylitis: 1. Marginal syndesmophytes (calcification/ossification of the outer fibers of the annulus fibrosus) bridge vertebral margins vertically, creating the classic smooth undulating 'bamboo spine'; 2. Ossification of the central supraspinous and interspinous ligaments appears as a single dense central radiodense line on AP view ('dagger sign'); 3. Combined ossification of the central ligaments and bilateral apophyseal joint capsules forms three parallel longitudinal dense lines ('trolley-track sign').",
            clinical=False
        ),
        q(
            "Why is pre-operative cervical spine radiography (specifically dynamic flexion-extension lateral views) mandatory in all rheumatoid arthritis patients scheduled for elective orthopaedic or general surgery under endotracheal intubation?",
            "Detects atlantoaxial subluxation risking fatal spinal cord compression",
            ["Assesses spontaneous laryngeal cartilage fusion", "Evaluates carotid artery calcification", "Precludes endotracheal tube placement in all cases"],
            "Rheumatoid synovial pannus frequently invades and destroys the synovial bursa between the anterior arch of C1, the odontoid process (dens), and the transverse atlantal ligament. The resulting atlantoaxial subluxation (AAS) is present in up to 30-50% of RA patients (anterior atlantodens interval > 3 mm in adults on flexion view). Neck manipulation during laryngoscopy and endotracheal intubation can produce catastrophic, fatal displacement of C1 on C2 with acute cervicomedullary cord compression.",
            clinical=True
        ),
        q(
            "What clinical triad defines Felty's syndrome, an uncommon extra-articular manifestation of severe, long-standing seropositive rheumatoid arthritis?",
            "Rheumatoid arthritis, splenomegaly, and neutropenia",
            ["Rheumatoid arthritis, keratoconjunctivitis sicca, and xerostomia", "Rheumatoid arthritis, glomerulonephritis, and alveolar hemorrhage", "Rheumatoid arthritis, aortic regurgitation, and complete heart block"],
            "Felty's syndrome is a serious systemic manifestation of rheumatoid arthritis characterized by the triad of: 1. Long-standing, destructive, seropositive Rheumatoid Arthritis; 2. Splenomegaly; 3. Neutropenia (absolute neutrophil count < 1500/mm3). Patients have an extraordinarily high risk of recurrent, life-threatening bacterial infections (especially skin and pulmonary infections) and chronic lower extremity ulcers.",
            clinical=False
        ),
        q(
            "A 42-year-old male with plaque psoriasis presents with severe, asymmetrical pain and swelling in the DIP joints of both hands, diffuse sausage-like swelling of the entire right middle finger (dactylitis), and pitted, dystrophic fingernails. Radiographs of the DIP joints show erosion of the distal phalanx base and sharpening of the middle phalanx head, producing a classic 'pencil-in-cup' deformity. What is the diagnosis?",
            "Psoriatic arthritis",
            ["Rheumatoid arthritis", "Primary osteoarthritis", "Pseudogout"],
            "Psoriatic arthritis is a seronegative spondyloarthropathy affecting 10-30% of patients with psoriasis. Hallmarks: asymmetric oligoarthritis or DIP-predominant polyarthritis, dactylitis ('sausage digit' caused by simultaneous tenosynovitis and arthritis), nail pitting and onycholysis, and destructive osteolysis leading to arthritis mutilans and the classic 'pencil-in-cup' appearance (tapered proximal phalanx head fitting into an expanded, cup-shaped distal phalanx base).",
            clinical=True
        ),
        q(
            "What is the classical clinical triad that characterizes Reactive Arthritis (historically known as Reiter's syndrome), and what are the most common triggering antecedent infections?",
            "Urethritis, conjunctivitis, and oligoarthritis following Chlamydia or enteric infection",
            ["Jaundice, ascites, and encephalopathy following Hepatitis B", "Hematuria, flank pain, and palpable mass following E. coli", "Dysphagia, glossitis, and anemia following H. pylori"],
            "Reactive arthritis is an autoimmune, seronegative spondyloarthropathy occurring 1-4 weeks following a mucosal infection. The classic aphorism 'can't see, can't pee, can't climb a tree' summarizes the triad: 1. Aseptic urethritis/cervicitis; 2. Conjunctivitis or uveitis; 3. Asymmetric, additive oligoarthritis (predominantly lower extremity joints, enthesitis of Achilles tendon/plantar fascia). Common triggers: Chlamydia trachomatis (venereal) or Shigella/Salmonella/Campylobacter (dysenteric).",
            clinical=False
        ),
        q(
            "A 52-year-old male awakens at 2 AM with excruciating, sudden-onset pain, violent erythema, warmth, and marked swelling of his right first metatarsophalangeal (MTP) joint (podagra). Synovial fluid aspiration examined under compensated polarized light microscopy reveals needle-shaped, intracellular crystals displaying strongly NEGATIVE birefringence (yellow when parallel to the slow axis). What is the diagnosis?",
            "Acute gouty arthritis (monosodium urate crystals)",
            ["Pseudogout (calcium pyrophosphate crystals)", "Septic arthritis (Staphylococcus aureus)", "Hydroxyapatite deposition disease"],
            "Acute gout is an inflammatory arthritis caused by precipitation of monosodium urate (MSU) crystals in synovial fluid when serum urate exceeds solubility. The 1st MTP joint is the site of first presentation in >50-70% of patients (podagra). Polarized light microscopy of joint aspirate is diagnostic: MSU crystals are needle-shaped and show strong NEGATIVE birefringence (appear bright yellow when aligned parallel to the compensator axis and blue when perpendicular).",
            clinical=True
        ),
        q(
            "How do the synovial fluid crystals and radiographic findings in Pseudogout (Calcium Pyrophosphate Dihydrate - CPPD deposition disease) differ from those in true Gout?",
            "Rhomboid crystals with weak positive birefringence and chondrocalcinosis",
            ["Needle-shaped crystals with strong negative birefringence and tophi", "Spherical crystals with zero birefringence and osteolytic lesions", "Envelope-shaped crystals with negative birefringence and osteopenia"],
            "In Calcium Pyrophosphate Dihydrate (CPPD) crystal deposition disease (pseudogout): 1. Crystals: Rhomboid or rod-shaped with weak POSITIVE birefringence (appear blue when aligned parallel to the compensator axis); 2. Radiographs: Show pathognomonic chondrocalcinosis—delicate, punctate, or linear radio-opacities within fibrocartilage (menisci of knee, triangular fibrocartilage of wrist) and hyaline articular cartilage.",
            clinical=False
        ),
    ]),

    # Chapter 35: Degenerative Disorders (Easy - 5 questions)
    (35, "Degenerative Disorders", "easy", [
        q(
            "A 64-year-old overweight woman presents with bilateral knee pain for 3 years, worse after prolonged walking, standing, and descending stairs. She reports morning stiffness that lasts only 10 to 15 minutes. On physical examination, there is coarse joint crepitus on passive flexion, mild medial joint-line tenderness, and a varus deformity. What is the diagnosis?",
            "Primary osteoarthritis of the knees",
            ["Rheumatoid arthritis", "Ankylosing spondylitis", "Gouty arthritis"],
            "Primary osteoarthritis is a degenerative 'wear and tear' joint disorder characterized by progressive loss of articular cartilage, subchondral sclerosis, and osteophyte formation. Hallmarks: age > 50 years, mechanical pain (worse with weight-bearing, walking down stairs, relieved by rest), brief morning stiffness (<30 minutes, unlike RA), joint crepitus, and gradual varus deformity due to preferential wear of the medial compartment.",
            clinical=True
        ),
        q(
            "According to the classic Kellgren-Lawrence radiographic grading system for Osteoarthritis, what specific features define 'Grade 3' severity?",
            "Moderate osteophytes with definite joint space narrowing and sclerosis",
            ["Doubtful joint space narrowing with minute osteophytic specks", "Definite osteophytes with completely preserved joint space", "Severe joint space obliteration with marked bone contour deformity"],
            "The Kellgren-Lawrence radiographic classification of OA: Grade 0: Normal; Grade 1 (Doubtful): Doubtful narrowing of joint space and possible osteophytic lipping; Grade 2 (Minimal): Definite osteophytes and possible joint space narrowing; Grade 3 (Moderate): Moderate multiple osteophytes, definite joint space narrowing, some sclerosis, and possible deformity of bone ends; Grade 4 (Severe): Large osteophytes, marked joint space narrowing, severe sclerosis, and definite bone contour deformity.",
            clinical=False
        ),
        q(
            "In nodal primary generalized osteoarthritis of the hands, what anatomical interphalangeal joints do Heberden's nodes and Bouchard's nodes specifically involve?",
            "Heberden nodes at DIP joints; Bouchard nodes at PIP joints",
            ["Heberden nodes at MCP joints; Bouchard nodes at wrist joints", "Heberden nodes at PIP joints; Bouchard nodes at DIP joints", "Heberden nodes at thumb CMC joint; Bouchard nodes at DIP joints"],
            "Heberden's and Bouchard's nodes are prominent, firm, knobby osteophytic enlargements characteristic of primary nodal osteoarthritis of the hands: 1. Heberden's nodes occur at the Distal Interphalangeal (DIP) joints (far more common, strong familial female predilection); 2. Bouchard's nodes occur at the Proximal Interphalangeal (PIP) joints.",
            clinical=False
        ),
        q(
            "What are the four cardinal radiographic hallmarks of primary Osteoarthritis on plain orthogonal radiographs?",
            "Asymmetric joint space narrowing, subchondral sclerosis, osteophytes, and subchondral cysts",
            ["Symmetric joint space narrowing, periarticular osteopenia, erosions, and ankylosis", "Punched-out lytic lesions, sunburst reaction, sequestrum, and involucrum", "Widened joint space, loose bodies, cortical destruction, and Codman triangle"],
            "The four pathognomonic radiological signs of osteoarthritis: 1. Non-uniform, asymmetrical joint space narrowing (reflecting focal mechanical cartilage loss in weight-bearing zones); 2. Subchondral bone sclerosis/eburnation (thickening of subchondral bone in response to concentrated stress); 3. Marginal osteophytes (bony spurs formed by endochondral ossification at joint margins); 4. Subchondral radiolucent cysts (geodes, formed by synovial fluid micro-intrusion through trabecular microfractures).",
            clinical=False
        ),
        q(
            "A 60-year-old male presents with clumsy, numb hands, difficulty buttoning his shirt, and a broad-based, unsteady, stiff gait. Neurological examination reveals brisk hyperreflexia in both lower extremities, sustained ankle clonus, bilateral positive Babinski signs, and a positive Hoffman's sign. What degenerative spinal condition is this?",
            "Cervical spondylotic myelopathy",
            ["Lumbar spinal canal stenosis", "Carpal tunnel syndrome", "Diabetic sensory polyneuropathy"],
            "Cervical Spondylotic Myelopathy (CSM) is the most common cause of spinal cord dysfunction in older adults (>55 years). Degenerative cervical disc bulging, facet hypertrophy, osteophytes, and buckling of the ligamentum flavum compress the cervical spinal cord. Symptoms: insidious loss of fine motor dexterity in the hands ('numb clumsy hands') combined with an upper motor neuron (UMN) spastic gait, hyperreflexia, clonus, extensor plantars, and positive Hoffman's sign.",
            clinical=True
        ),
    ]),

    # Chapter 36: Affections of the Soft Tissues (HARD - 10 questions)
    (36, "Affections of the Soft Tissues", "hard", [
        q(
            "A 32-year-old nursing mother presents with severe pain over the radial aspect of her right wrist that worsens when lifting her baby. On examination, there is localized tenderness and swelling over the radial styloid process. When the patient tucks her thumb into her palm, curls her fingers over it, and the examiner gently deviates the wrist ulnarly, sharp excruciating pain is reproduced over the radial styloid. What is the diagnosis, and which specific tendon sheaths are inflamed?",
            "De Quervain tenosynovitis (APL and EPB tendons)",
            ["Intersection syndrome (ECRL and ECRB tendons)", "Carpal tunnel syndrome (median nerve)", "Trigger thumb (FPL tendon at A1 pulley)"],
            "De Quervain's tenosynovitis is a stenosing tenovaginitis of the first dorsal extensor compartment of the wrist, which contains the Abductor Pollicis Longus (APL) and Extensor Pollicis Brevis (EPB) tendons. It is classically seen in mothers lifting infants ('baby wrist') or repetitive thumb abduction/wrist deviation. The physical maneuver described is Finkelstein's test (Eichhoff's maneuver), which stretches the inflamed tendons within the tight osteofibrous canal, reproducing sharp localized pain.",
            clinical=True
        ),
        q(
            "What precise anatomical structures form the boundaries of the Carpal Tunnel, and what ten structures pass through it beneath the flexor retinaculum?",
            "Carpal arch and flexor retinaculum; transmits 9 flexor tendons and median nerve",
            ["Radius and ulna; transmits radial nerve, ulnar nerve, and 8 extensor tendons", "Palmar fascia; transmits ulnar artery, ulnar nerve, and 4 lumbrical tendons", "Thenar fascia; transmits radial artery, median nerve, and abductor pollicis"],
            "The carpal tunnel is an inelastic fibro-osseous conduit: its floor and lateral walls are formed by the concavity of the carpal bones (scaphoid, trapezium laterally; pisiform, hook of hamate medially), and its roof is the dense transverse carpal ligament (flexor retinaculum). Exactly 10 structures pass through: the Median Nerve, 4 tendons of Flexor Digitorum Superficialis, 4 tendons of Flexor Digitorum Profundus, and 1 tendon of Flexor Pollicis Longus.",
            clinical=False
        ),
        q(
            "A 48-year-old female computer programmer presents with nocturnal tingling, burning numbness, and pain in the thumb, index, and middle fingers of her right hand that awakens her from sleep, relieved by shaking her hand ('flick sign'). On examination, there is thenar muscle atrophy and weakness of thumb abduction (Abductor Pollicis Brevis). Phalen's test reproduces numbness within 45 seconds. What is the diagnosis?",
            "Severe carpal tunnel syndrome",
            ["C8-T1 cervical radiculopathy", "Cubital tunnel syndrome", "Thoracic outlet syndrome"],
            "Carpal Tunnel Syndrome is the most common entrapment neuropathy, caused by compression of the median nerve in the carpal tunnel. Classic presentation: nocturnal paresthesias in the median nerve distribution (thumb, index, middle, and radial half of ring finger), positive Phalen's wrist-flexion test, positive Tinel's percussion sign, and relief on shaking the hand ('flick sign'). Motor weakness and atrophy of the Abductor Pollicis Brevis (thenar wasting) indicate severe, advanced nerve compression.",
            clinical=True
        ),
        q(
            "In lateral epicondylitis of the humerus (Tennis Elbow), which specific tendon origin is primarily degenerate and micro-torn at the lateral humeral epicondyle?",
            "Extensor carpi radialis brevis (ECRB)",
            ["Extensor digitorum communis (EDC)", "Extensor carpi ulnaris (ECU)", "Brachioradialis"],
            "Tennis elbow (lateral epicondylitis / lateral epicondylalgia) is NOT an acute inflammatory condition; rather, it is an angiofibroblastic tendinosis (repetitive micro-tearing, failed biological healing response, and fibrovascular hyperplasia) originating primarily at the origin of the Extensor Carpi Radialis Brevis (ECRB) tendon from the lateral epicondyle (with or without EDC involvement). Pain is aggravated by resisted active wrist extension with the elbow in extension (Cozen's test).",
            clinical=False
        ),
        q(
            "A 56-year-old male with a history of alcohol use presents with nodular, cord-like thickening of the palmar fascia of both hands. Over 2 years, he has developed progressive, irreversible flexion contractures of the metacarpophalangeal (MCP) and proximal interphalangeal (PIP) joints of his ring and little fingers, preventing him from placing his hand flat on a tabletop (positive Hueston tabletop test). What is the diagnosis?",
            "Dupuytren contracture (palmar fibromatosis)",
            ["Stenosing tenosynovitis of FDS", "Claw hand secondary to ulnar nerve palsy", "Volkmann ischemic contracture"],
            "Dupuytren's contracture is a benign, proliferative fibroplastic disorder of the palmar aponeurosis. Myofibroblasts proliferate within the pretendinous bands, forming nodules that mature into dense, collagen-rich, inelastic cords that contract longitudinally, drawing the MCP and PIP joints into fixed flexion deformities (ring and little fingers most commonly involved). The inability to place the palm flat on a table is Hueston's tabletop test, an indication for surgical fasciotomy or fasciectomy.",
            clinical=True
        ),
        q(
            "In stenosing tenosynovitis producing a 'Trigger Finger' or 'Trigger Thumb', at which specific anatomical pulley does the primary mechanical discrepancy and nodular tendon entrapment occur?",
            "A1 (first annular) pulley at the metacarpal head",
            ["A2 pulley on the proximal phalanx", "A3 pulley at the PIP joint", "A4 pulley on the middle phalanx"],
            "Trigger finger (stenosing tenovaginitis) is caused by repetitive friction and mismatch between the flexor tendon (which develops a reactive intratendinous nodule) and the tight first annular (A1) pulley at the level of the metacarpal head (distal palmar crease). As the digit flexes, the nodule is pulled into the sheath; on attempted extension, the nodule becomes mechanically trapped beneath the proximal edge of the A1 pulley, producing painful snapping, clicking, or locking in flexion.",
            clinical=False
        ),
        q(
            "A 52-year-old diabetic woman presents with gradual-onset, severe shoulder pain followed by progressive, global restriction of both active AND passive movements of the glenohumeral joint in all planes, with external rotation being the earliest and most severely restricted motion. Radiographs are normal. What condition is this, and what is its primary pathology?",
            "Adhesive capsulitis (capsular fibrosis and contracture)",
            ["Full-thickness rotator cuff tear (supraspinatus detachment)", "Subacromial impingement syndrome", "Humeral head avascular necrosis"],
            "Frozen shoulder (Adhesive Capsulitis) is characterized by insidious painful stiffening of the shoulder with profound global restriction of BOTH active and passive glenohumeral motion (external rotation restricted first and most severely, followed by abduction and internal rotation). Pathology shows progressive inflammatory capsular fibrosis, dense contracture of the coracohumeral ligament, obliteration of the inferior axillary fold, and loss of intra-articular volume (reduced from 15-20 mL to <5 mL).",
            clinical=True
        ),
        q(
            "A 42-year-old nurse complains of severe, sharp, stabbing heel pain on the plantar aspect of her foot that is excruciating during the first few steps after getting out of bed in the morning, gradually easing with walking, but recurring after prolonged rest. On examination, exquisite tenderness is elicited by pressing directly over the medial calcaneal tuberosity. What is the diagnosis?",
            "Plantar fasciitis",
            ["Tarsal tunnel syndrome", "Calcaneal stress fracture", "Achilles tendinopathy"],
            "Plantar fasciitis is a traction-overload enthesopathy/degenerative tear of the origin of the thick plantar aponeurosis at the medial tubercle of the calcaneus. Hallmark symptom: 'start-up' heel pain—severe pain upon taking the first few steps in the morning (the fascia contracts overnight in plantarflexion; taking weight suddenly stretches the tight, inflamed enthesis). Tenderness is precisely localized to the anteromedial border of the plantar calcaneal tuberosity.",
            clinical=True
        ),
        q(
            "A 45-year-old obese male who wears a tight police duty belt presents with persistent burning dysesthesia, tingling, and numbness localized to the anterolateral aspect of his right thigh. Motor power, knee reflexes, and straight leg raising are completely normal. What is the diagnosis, and which nerve is compressed?",
            "Meralgia paresthetica (lateral femoral cutaneous nerve compression)",
            ["L2-L3 lumbar radiculopathy", "Femoral neuropathy", "Obturator nerve entrapment"],
            "Meralgia paraesthetica (Bernhardt-Roth syndrome) is an isolated sensory entrapment neuropathy of the Lateral Femoral Cutaneous Nerve (LFCN) of the thigh (derived from L2-L3). The nerve is compressed where it pierces or passes beneath the lateral attachment of the inguinal ligament just medial to the Anterior Superior Iliac Spine (ASIS). Because the LFCN is a PURELY SENSORY nerve, there is burning pain, numbness, and hyperesthesia over the anterolateral thigh with completely normal motor power and reflexes.",
            clinical=True
        ),
        q(
            "What is the most common anatomical site of origin and internal composition of a simple Ganglion Cyst of the wrist?",
            "Dorsal scapholunate ligament; viscous mucinous fluid rich in hyaluronic acid",
            ["Volar radial artery sheath; serosanguinous synovial fluid", "Flexor tendon sheath; purulent bacterial exudate", "First dorsal compartment; calcified osteoid tissue"],
            "A ganglion cyst is the most common benign soft-tissue tumor-like swelling of the hand and wrist (>60-70%). Approximately 70% arise on the dorsal aspect of the wrist, pedicled to the underlying scapholunate ligament or capsule. It is a true cystic degeneration of periarticular fibrous tissue (not lined by true synoviocytes, but by flattened cells) filled with thick, clear, viscous, mucin-rich fluid containing high concentrations of hyaluronic acid and glucosamine.",
            clinical=False
        ),
    ]),

    # Chapter 37: Metabolic Bone Diseases (HARD - 10 questions)
    (37, "Metabolic Bone Diseases", "hard", [
        q(
            "A 20-month-old toddler presents with delayed walking, frontal bossing, craniotabes, pigeon-chest deformity (pectus carinatum), symmetrical bead-like enlargements along the costochondral junctions ('rachitic rosary'), and marked widening of the wrists. Anteroposterior radiograph of the wrists shows widening, cupping, splaying, and ragged fraying of the distal radial and ulnar metaphyses with widening of the radiolucent physeal gap. What is the diagnosis?",
            "Nutritional rickets",
            ["Infantile scurvy", "Achondroplasia", "Congenital syphilis"],
            "Rickets is a disease of growing children caused by deficiency of vitamin D (or calcium/phosphate metabolism) leading to failure of mineralization of newly formed osteoid matrix and growth plate cartilaginous matrix. Hallmarks: frontal bossing, craniotabes, rachitic rosary, Harrison's sulcus, widening of epiphyses (wrists/ankles), and bowlegs/knock-knees. Radiographs show cupping (concave metaphysis), fraying (ragged margins), splaying (flared metaphysis), and widened growth plates.",
            clinical=True
        ),
        q(
            "What is the fundamental histological and biochemical distinction between Osteoporosis and Osteomalacia?",
            "Osteoporosis: decreased bone mass with normal mineralisation; Osteomalacia: defective mineralisation of osteoid matrix",
            ["Osteoporosis: hypermineralisation; Osteomalacia: complete loss of matrix", "Osteoporosis: occurs exclusively in men; Osteomalacia: occurs only in children", "Osteoporosis: elevated alkaline phosphatase; Osteomalacia: normal alkaline phosphatase"],
            "Osteoporosis is a quantitative defect: there is decreased bone volume and mass, but whatever bone is present is normally mineralized (normal ratio of mineral to collagen matrix; normal calcium, phosphate, and alkaline phosphatase). Osteomalacia is a qualitative defect occurring in the mature adult skeleton: organic osteoid matrix is deposited at normal or elevated rates by osteoblasts, but mineralization fails, leading to unmineralized wide osteoid seams, bone softening, low/normal calcium, low phosphate, and markedly elevated alkaline phosphatase.",
            clinical=False
        ),
        q(
            "A 45-year-old multiparous woman with poor nutritional intake and chronic lack of sunlight exposure presents with generalized bone pain, severe proximal muscle weakness (difficulty rising from a chair, waddling gait), and bone tenderness. Plain radiographs reveal symmetrical, transverse, radiolucent bands perpendicular to the cortex on the medial femoral neck, superior pubic rami, and axillary borders of the scapulae. What are these pathognomonic radiological lesions termed?",
            "Looser zones (Milkman pseudofractures)",
            ["Harris growth arrest lines", "Codman triangles", "Brodie abscesses"],
            "Looser's zones (pseudofractures, Milkman's lines, or Umbauzonen) are the radiological hallmark of osteomalacia. They are narrow, ribbon-like radiolucent bands traversing the cortex (usually perpendicular to the long axis, with sclerotic margins) representing cortical microstress fractures repaired with unmineralized fibrous osteoid tissue. They are classically bilateral, symmetrical, and found in the axillary border of the scapula, femoral neck, pubic rami, ribs, and proximal ulna.",
            clinical=True
        ),
        q(
            "According to the World Health Organization (WHO) diagnostic criteria based on Dual-Energy X-ray Absorptiometry (DEXA) measurement of the lumbar spine or femoral neck, what T-score threshold defines 'Osteoporosis'?",
            "T-score <= -2.5 standard deviations",
            ["T-score between 0 and -1.0 standard deviations", "T-score between -1.0 and -2.5 standard deviations", "T-score greater than +1.0 standard deviations"],
            "WHO DEXA scan criteria (comparing patient's bone mineral density to a young adult sex-matched reference population): 1. Normal: T-score >= -1.0 SD; 2. Osteopenia: T-score between -1.0 and -2.5 SD; 3. Osteoporosis: T-score <= -2.5 SD; 4. Severe (established) Osteoporosis: T-score <= -2.5 SD in the presence of one or more documented fragility fractures.",
            clinical=False
        ),
        q(
            "A 54-year-old female presents with recurrent calcium nephrolithiasis, generalized lethargy, abdominal constipation, and diffuse bone aches. Radiographs show generalized osteopenia, subperiosteal cortical resorption on the radial aspect of the middle phalanges of the fingers, 'salt-and-pepper' skull degranulation, and multiple cystic expansile osteolytic lesions in the mandible and clavicle. Serum calcium is 11.8 mg/dL, phosphate is 2.1 mg/dL, and parathyroid hormone (PTH) is markedly elevated. What is the diagnosis?",
            "Primary hyperparathyroidism with osteitis fibrosa cystica",
            ["Osteomalacia", "Multiple myeloma", "Polyostotic fibrous dysplasia"],
            "Primary hyperparathyroidism (most commonly due to a solitary parathyroid adenoma) produces excess PTH, stimulating osteoclastic bone resorption. Skeletal manifestations (Osteitis Fibrosa Cystica / von Recklinghausen's disease of bone): 1. Subperiosteal cortical bone resorption (most specific sign, seen on radial borders of middle phalanges); 2. Salt-and-pepper demineralization of skull; 3. Loss of lamina dura around teeth; 4. Brown tumors (cystic fibrous accumulations filled with osteoclasts, macrophages, and hemosiderin).",
            clinical=True
        ),
        q(
            "What histological architectural hallmark characterizes the sclerotic, 'burned-out' phase of Paget's disease of bone (Osteitis Deformans) under light microscopy?",
            "Disorganized mosaic pattern with thick, irregular cement lines",
            ["Uniform Haversian canals with concentric lamellae", "Continuous unmineralized osteoid seams lining trabeculae", "Sheets of small round blue cells with glycogen granules"],
            "Paget's disease progresses through 3 phases: 1. Osteolytic (resorptive) phase; 2. Mixed osteolytic-osteoblastic phase; 3. Sclerotic (quiescent / burned-out) phase. In the sclerotic phase, rapid, chaotic, disorganized bone formation and resorption produce an abnormal 'mosaic' or 'jigsaw puzzle' architectural pattern: irregularly shaped fragments of lamellar bone are joined by prominent, thick, wavy, dark blue cement lines, resulting in bone that is structurally enlarged, weak, and brittle.",
            clinical=False
        ),
        q(
            "A 68-year-old elderly man complains that his hat size has progressively increased over the past 5 years and that he has developed progressive bilateral sensorineural hearing loss and deep, dull aching pain in his bowed left tibia. Plain radiographs reveal cortical thickening, coarsened trabeculae, expansion of the skull bones ('cotton-wool' appearance), and bowing of the tibia. Serum alkaline phosphatase is markedly elevated at 850 IU/L, but serum calcium and phosphate are normal. What is the diagnosis?",
            "Paget disease of bone (osteitis deformans)",
            ["Primary hyperparathyroidism", "Osteomalacia", "Metastatic prostate carcinoma"],
            "Paget's disease typically affects elderly patients (>60 years). Hallmarks: progressive enlargement of the cranium ('increasing hat size'), cranial nerve impingement (sensorineural deafness due to eighth nerve compression in the auditory canal), bone expansion, and anterolateral bowing of the femur/tibia with microfractures ('banana fractures'). Laboratory profile: isolated, massive elevation of serum Alkaline Phosphatase (reflecting exuberant osteoblastic activity) with completely normal serum calcium and phosphate.",
            clinical=True
        ),
        q(
            "In an elderly patient with long-standing, multi-focal Paget's disease of bone, what rare (<1%) but catastrophic complication must be suspected if the patient presents with a sudden onset of severe, localized, unrelenting bone pain, a rapidly enlarging warm soft-tissue mass, and an aggressive osteolytic cortical breakthrough on radiograph?",
            "Secondary osteosarcoma (Pagetic sarcoma)",
            ["Avascular necrosis of femoral head", "Garré sclerosing osteomyelitis", "Eosinophilic granuloma"],
            "The most dreaded complication of Paget's disease is malignant degeneration into secondary osteosarcoma (Pagetic sarcoma), occurring in <1% of patients. It typically arises in long-standing polyostotic disease in individuals over 60 years. Hallmark: sudden onset of severe localized bone pain, rapid enlargement of a mass, pathological fracture, and permeative osteolytic cortical destruction. Pagetic osteosarcoma is highly aggressive with a dismal 5-year survival (<10%).",
            clinical=True
        ),
        q(
            "A 40-year-old male living in an endemic rural region with high well-water fluoride concentrations presents with joint stiffness, neck pain, and inability to bend his spine. Plain radiographs show marked, uniform osteosclerosis of the axial skeleton (vertebrae resembling 'chalk'), ossification of the sacrotuberous and sacrospinous ligaments, and dense periosteal outgrowths. Teeth show dark brown mottling of the enamel. What is the diagnosis?",
            "Skeletal fluorosis",
            ["Ankylosing spondylitis", "Osteopetrosis", "Paget disease"],
            "Endemic skeletal fluorosis occurs from chronic ingestion of high-fluoride drinking water (>3-5 ppm). Fluoride incorporates into hydroxyapatite forming fluoroapatite crystals, stimulating chaotic osteoblastic bone formation. Hallmarks: mottled dental enamel (fluorosis), progressive joint stiffness, diffuse chalky osteosclerosis of the axial spine and pelvis, calcification/ossification of ligaments (sacrotuberous, sacrospinous, interosseous membrane, ligamentum flavum), and dense periosteal hyperostosis.",
            clinical=True
        ),
        q(
            "What is the first-line pharmacological class of antiresorptive agents of choice for treating postmenopausal osteoporosis to reduce the risk of vertebral and hip fragility fractures, and what is their cellular mechanism of action?",
            "Bisphosphonates; inhibit osteoclastic farnesyl pyrophosphate (FPP) synthase",
            ["Selective serotonin reuptake inhibitors; stimulate calcitonin secretion", "Calcium channel blockers; promote direct osteoid crystallization", "Loop diuretics; inhibit renal calcium excretion"],
            "Nitrogen-containing bisphosphonates (oral Alendronate, Risedronate, or annual IV Zoledronic acid) are the first-line antiresorptive therapy for osteoporosis. They bind with high affinity to hydroxyapatite crystals in bone; when internalized by resorbing osteoclasts, they inhibit farnesyl pyrophosphate (FPP) synthase in the mevalonate pathway, preventing prenylation of small GTP-binding proteins (Rho, Rac), leading to osteoclast inactivation and apoptosis, increasing bone mineral density and reducing fractures by 40-70%.",
            clinical=False
        ),
    ]),

    # Chapter 38: Miscellaneous Affections of the Bone (HARD - 10 questions)
    (38, "Miscellaneous Affections of the Bone", "hard", [
        q(
            "A 6-year-old boy presents with a 4-month history of a painless limp and vague, dull aching pain in the right groin referred to the anteromedial knee. On physical examination, internal rotation and abduction of the right hip in flexion are markedly restricted. Plain radiograph reveals increased radiodensity (sclerosis), widening of the joint space, and slight flattening of the capital femoral epiphysis. What is the diagnosis?",
            "Legg-Calvé-Perthes disease",
            ["Slipped capital femoral epiphysis", "Tuberculous arthritis of hip", "Transient synovitis of hip"],
            "Perthes disease is idiopathic avascular necrosis (osteochondritis) of the femoral head epiphysis affecting growing children (peak 4-8 years, 4:1 male predominance). Symptoms begin insidiously with an antalgic limp and mild groin/knee pain (referred via obturator nerve). Physical hallmark: early, preferential loss of internal rotation and abduction in flexion. Radiographs demonstrate the classic avascular changes (increased density, subchondral lucency, flattening, fragmentation).",
            clinical=True
        ),
        q(
            "According to Waldenström's classic chronological staging of Perthes disease on serial plain radiographs, what are the four sequential stages in order of progression?",
            "Initial/condensation -> Fragmentation -> Reossification -> Healed/remodeling",
            ["Fibrous -> Cartilaginous -> Bony -> Ankylosis", "Hyperemic -> Necrotic -> Sclerotic -> Dislocation", "Pre-radiographic -> Synovial -> Chondral -> Osteotomy"],
            "Waldenström's radiographic stages of Perthes disease: 1. Initial/Condensation stage (6-12 months): Epiphysis stops growing, appears smaller and homogeneously radiodense; subchondral fracture ('crescent sign') appears; 2. Fragmentation stage (1-2 years): Necrotic bone is resorbed by vascular granulation tissue; epiphysis breaks into fragments; 3. Reossification stage (healing, 2-3 years): New bone is deposited from periphery; 4. Residual stage: Final mature femoral head contour remains (spherical, oval, or flat/coxa plana).",
            clinical=False
        ),
        q(
            "In Herring's lateral pillar classification of Perthes disease assessed on the anteroposterior pelvic radiograph during the fragmentation stage, what defines 'Herring Group B' severity?",
            "Lateral pillar maintains >50% of its normal height",
            ["Lateral pillar maintains 100% height with no radiolucency", "Lateral pillar collapses to <50% of normal height", "Complete resorption of all three pillars with dislocation"],
            "Herring's lateral pillar classification evaluates the height of the lateral 15-30% of the femoral head (the lateral pillar, which bears the brunt of acetabular contact stresses): Group A: No loss of height in the lateral pillar (normal height, excellent prognosis); Group B: Lateral pillar maintains >50% of its normal height (moderate prognosis; surgical containment beneficial if age > 8 years); Group C: Lateral pillar collapses to <50% of normal height (poor prognosis, head deforms severely).",
            clinical=False
        ),
        q(
            "What clinical and radiological indicators comprise Catterall's classic 'Head-at-Risk' signs in Perthes disease, warning of impending severe femoral head deformity and extrusion?",
            "Gage sign, lateral calcification, lateral subluxation, and horizontal physis",
            ["Absence of knee pain with normal internal rotation", "Normal abduction of 60 degrees with symmetric skin folds", "Preserved lateral pillar height with negative Trendelenburg"],
            "Catterall's 'Head-at-Risk' signs indicate a high risk of permanent femoral head deformity and uncontainment: 1. Gage's sign (small radiolucent V-shaped defect at the lateral margin of the epiphysis/adjacent metaphysis); 2. Calcification lateral to the epiphysis; 3. Lateral subluxation/extrusion of the femoral head from the acetabulum; 4. Horizontalization of the physis; 5. Diffuse metaphyseal radiolucent cysts/reactions.",
            clinical=False
        ),
        q(
            "An 18-year-old male athlete presents with intermittent aching knee pain, joint swelling, and a sensation of sudden knee 'giving way' and locking. Plain radiographs demonstrate a well-demarcated, crescentic subchondral radiolucent line separating a partially detached oval bone fragment on the lateral, non-weight-bearing aspect of the MEDIAL femoral condyle. What is the diagnosis?",
            "Osteochondritis dissecans of the knee",
            ["Giant cell tumour of distal femur", "Osgood-Schlatter disease", "Hoffa fracture of lateral condyle"],
            "Osteochondritis Dissecans (OCD) is an idiopathic focal avascular necrosis of subchondral bone leading to demarcation and potential detachment of an articular cartilage and bone fragment into the joint space. It classically affects the lateral aspect of the MEDIAL femoral condyle (>75% of cases; area of lateral intercondylar notch impingement by the tibial spine). As the fragment loosens, it causes effusion, aching pain, and true mechanical locking when it drops into the joint as a loose body ('joint mouse').",
            clinical=True
        ),
        q(
            "According to the Ficat and Arlet classification of Avascular Necrosis (AVN) of the femoral head, what pathognomonic radiological finding on the lateral or frog-leg radiograph marks the transition from Stage II to Stage III?",
            "Subchondral radiolucent fracture line (crescent sign)",
            ["Diffuse trabecular demineralization without fracture", "Complete obliteration of acetabular joint space", "Normal plain radiograph with marrow edema on MRI"],
            "Ficat-Arlet staging of femoral head AVN: Stage 0: Pre-clinical, pre-radiographic (normal X-ray and MRI); Stage 1: Normal plain radiograph, diagnostic changes on MRI (marrow edema, band); Stage 2: Diffuse sclerosis, osteopenia, and cystic changes on X-ray, but normal spherical contour with NO collapse; Stage 3: Subchondral collapse manifested as the pathognomonic 'crescent sign' (subchondral radiolucent fracture line) and flattening; Stage 4: Joint space narrowing and secondary osteoarthritis.",
            clinical=False
        ),
        q(
            "A 14-year-old adolescent athlete presents with localized pain, tenderness, and a prominent, firm swelling over the tibial tuberosity that is exacerbated by running, jumping, and direct kneeling. Radiographs reveal fragmentation and irregular soft-tissue swelling at the tibial tuberosity apophysis. What is the diagnosis, and what is the underlying pathoetiology?",
            "Osgood-Schlatter disease (patellar tendon traction apophysitis)",
            ["Acute osteomyelitis of proximal tibia", "Osteosarcoma of tibial tuberosity", "Brodie abscess of proximal tibial metaphysis"],
            "Osgood-Schlatter disease is a traction apophysitis of the tibial tuberosity occurring in active adolescents (10-15 years, especially running/jumping sports). Repetitive tensile pull of the quadriceps muscle through the patellar tendon on the secondary ossification center (apophysis) of the tibial tubercle causes micro-avulsions, inflammation, fragmentation, and reactive heterotopic bone formation. It is benign, self-limiting upon physeal fusion, and treated with rest, ice, and activity modification.",
            clinical=True
        ),
        q(
            "A 10-year-old soccer player presents with bilateral, burning posterior heel pain aggravated by running. On examination, there is exquisite tenderness when compressing the medial and lateral aspects of the posterior calcaneus simultaneously ('calcaneal squeeze test'). Radiographs show patchy sclerotic condensation and fragmentation of the posterior calcaneal apophysis. What is the diagnosis?",
            "Sever disease (calcaneal apophysitis)",
            ["Plantar fasciitis", "Achilles tendon rupture", "Kohler disease"],
            "Sever's disease (calcaneal apophysitis) is a common, self-limiting traction apophysitis at the insertion of the Achilles tendon into the secondary ossification center of the calcaneal tuberosity in active children aged 8-12 years. Repetitive microtrauma from the tight gastrosoleus complex during the growth spurt creates pain. The clinical pathognomonic test is the 'squeeze test' (mediolateral compression of the posterior calcaneus elicits sharp pain).",
            clinical=True
        ),
        q(
            "What specific tarsal and metatarsal bones are affected in Köhler's disease versus Freiberg's infraction in pediatric osteochondrosis?",
            "Köhler: Tarsal navicular; Freiberg: Second metatarsal head",
            ["Köhler: Calcaneus; Freiberg: Talus", "Köhler: First metatarsal head; Freiberg: Cuboid", "Köhler: Medial cuneiform; Freiberg: Fifth metatarsal base"],
            "In juvenile osteochondroses: 1. Köhler's disease is avascular necrosis/osteochondritis of the tarsal navicular bone, typically presenting in boys aged 3-7 years with a painful limp and navicular tenderness (X-ray shows wafer-thin, sclerotic, fragmented navicular; self-limiting with complete reconstitution); 2. Freiberg's disease (infraction) is avascular necrosis of the head of the second (or third) metatarsal, classically affecting adolescent girls, producing collapse and flattening of the metatarsal head.",
            clinical=False
        ),
        q(
            "In the core decompression procedure for early (Ficat Stage I or II) avascular necrosis of the femoral head, what is the fundamental biological and mechanical goal of drilling into the necrotic zone?",
            "Relieves intraosseous venous hypertension and promotes vascular ingrowth",
            ["Arthrodeses femoral head to acetabular socket", "Replaces necrotic trabeculae with polymethylmethacrylate", "Excises articular cartilage to stimulate fibrous scarring"],
            "In early avascular necrosis, microvascular ischemia leads to intraosseous venous stasis, marrow edema, and extremely high intraosseous compartment pressures (>30 mmHg, normal <10 mmHg), which perpetuate ischemia. Core decompression (drilling a 3-8 mm track from the lateral cortex through the femoral neck into the center of the necrotic head lesion) relieves this intraosseous hypertension, provides immediate pain relief, and creates a vascular conduit for creeping substitution and neovascularization.",
            clinical=False
        ),
    ]),

    # Chapter 39: Miscellaneous Regional Diseases (HARD - 10 questions)
    (39, "Miscellaneous Regional Diseases", "hard", [
        q(
            "A 6-week-old female infant is brought to the clinic because her head is constantly tilted toward the right shoulder with the chin rotated pointing toward the left. On palpation, a firm, non-tender, olive-shaped, mobile mass is felt within the lower third of the right sternocleidomastoid (SCM) muscle. What is the diagnosis and its classic histological basis?",
            "Congenital muscular torticollis (fibrous contracture of sternocleidomastoid)",
            ["Atlantoaxial rotary subluxation", "Klippel-Feil syndrome", "Cervical lymphadenitis with abscess"],
            "Congenital muscular torticollis (fibromatosis colli / sternomastoid tumor) typically presents in infants aged 2-8 weeks (often following breech extraction or birth trauma). Muscle ischemia or intrauterine compression results in fibrous replacement and contracture of the SCM: the tight muscle pulls the mastoid toward the clavicle (lateral head tilt to the IPSILATERAL side) and rotates the chin toward the CONTRALATERAL shoulder. >90% resolve with early passive stretching exercises.",
            clinical=True
        ),
        q(
            "A 28-year-old female presents with pain, numbness, and tingling along the medial border of her forearm and hypothenar hand (C8-T1 distribution) and coldness of her hand, exacerbated by carrying heavy grocery bags. Adson's maneuver reproduces paresthesias and obliterates the radial pulse. What anatomical anomaly is the underlying cause, and which structures are compressed?",
            "Cervical rib compressing C8-T1 lower trunk and subclavian artery",
            ["Carpal tunnel syndrome compressing median nerve", "Pancoast tumor compressing sympathetic chain", "Cubital tunnel syndrome compressing ulnar nerve"],
            "A cervical rib is a congenital supernumerary rib arising from the C7 vertebra. As it curves downward and forward toward the first thoracic rib, it (or its fibrous band) elevates and compresses the lower trunk of the brachial plexus (C8-T1 fibers -> tingling in ulnar digits, weakness of intrinsics) and the subclavian artery (ischemia, pallor, weak pulse, post-stenotic aneurysm). In Adson's test, neck extension, head rotation toward affected side, and deep inspiration obliterate the radial pulse.",
            clinical=True
        ),
        q(
            "A 5-year-old boy presents with an acute limp and hip pain 10 days following a mild viral upper respiratory infection. He is afebrile (temperature 37.1 C), comfortable at rest, but resists extreme internal rotation. Serum WBC, ESR, and CRP are within normal limits. Ultrasound reveals a small, transient, clear hip effusion. Following 5 days of bed rest and oral ibuprofen, the child is completely asymptomatic with full normal motion. What is the diagnosis?",
            "Transient synovitis of hip (observation hip)",
            ["Acute septic arthritis of hip", "Legg-Calvé-Perthes disease", "Pauciarticular juvenile idiopathic arthritis"],
            "Transient synovitis ('observation hip') is the most common cause of acute painful limp in young children (aged 3-8 years). It is a benign, self-limiting, non-specific reactive synovitis that classically develops 1-2 weeks after a viral upper respiratory illness. Unlike septic arthritis (high fever, severe pain, inability to bear weight, ESR > 40, Kocher criteria positive), transient synovitis patients are afebrile or low-grade, have normal/mild inflammatory markers, and recover fully within 7-10 days with simple rest and NSAIDs.",
            clinical=True
        ),
        q(
            "What is the quantitative anatomical definition of 'Coxa Vara' of the hip, and what is the normal adult femoral neck-shaft (CCD) angle?",
            "Neck-shaft angle <120 degrees; normal adult angle is 125-135 degrees",
            ["Neck-shaft angle >145 degrees; normal adult angle is 110 degrees", "Acetabular anteversion <5 degrees; normal adult angle is 45 degrees", "Femoral head extrusion index exceeding 80%"],
            "The collodiaphyseal angle (neck-shaft angle) is formed by the axis of the femoral neck and the axis of the femoral shaft: Normal in infants is 140-150 degrees; in normal adults it is 125 to 135 degrees. Coxa vara is defined as a pathological reduction of the neck-shaft angle to < 120 degrees (congenital, developmental, or acquired secondary to rickets, fibrous dysplasia, or malunited trochanteric fracture). In contrast, coxa valga is an angle > 135-140 degrees.",
            clinical=False
        ),
        q(
            "An overweight, rapidly growing 13-year-old boy presents with dull pain in his left knee and an antalgic limp for 6 weeks. On examination, when the examiner passively flexes the left hip, the thigh obligatorily rotates into external rotation and abduction (positive Drehmann sign). Anteroposterior pelvic radiograph shows that a line drawn along the superior cortex of the femoral neck (Klein's line) fails to intersect the lateral capital femoral epiphysis (Trethowan's sign). What is the diagnosis?",
            "Slipped capital femoral epiphysis (SCFE)",
            ["Legg-Calvé-Perthes disease", "Osgood-Schlatter disease", "Avulsion fracture of anterior inferior iliac spine"],
            "SCFE is the most common adolescent hip disorder, characteristically affecting obese adolescent boys (11-15 years). The capital femoral epiphysis slips posteriorly and inferiorly through the hypertrophic physeal zone. Hallmark: Drehmann sign (obligatory external rotation during hip flexion). On AP radiograph, Klein's line normally cuts through the lateral third of the epiphysis; in SCFE, it passes completely outside the head (Trethowan's sign). Immediate in-situ single cannulated screw fixation is mandatory.",
            clinical=True
        ),
        q(
            "A 45-year-old male presents with a painless, smooth, fluctuant, oval swelling in the popliteal fossa that becomes tense and prominent when the knee is fully extended, and soft and less prominent when the knee is flexed to 45 degrees (Foucher's sign). What is the diagnosis, and between which two muscle tendons does this synovial cyst characteristically arise?",
            "Baker cyst (between semimembranosus and medial gastrocnemius)",
            ["Meniscal cyst (between biceps femoris and popliteus)", "Bursal hygroma (between sartorius and gracilis)", "Popliteal artery aneurysm (within plantaris muscle)"],
            "A Baker's cyst (popliteal synovial cyst) is a chronic distension of the gastrocnemio-semimembranosus bursa located in the posteromedial popliteal fossa. It communicates with the knee joint via a slit-like opening. In adults, it is almost always secondary to underlying intra-articular pathology (meniscal tear, osteoarthritis, rheumatoid arthritis) causing chronic effusion. Foucher's sign (cyst hard/prominent in extension, soft in flexion) is pathognomonic.",
            clinical=True
        ),
        q(
            "What are the four most common etiologies responsible for producing intra-articular 'loose bodies' ('joint mice') in the knee joint?",
            "Osteochondritis dissecans, synovial chondromatosis, osteochondral fractures, and osteophytes",
            ["Gouty tophi, tuberculous sequestra, calcaneal spurs, and Brodie abscesses", "Cruciate ligament tears, fabella subluxation, prepatellar bursitis, and xanthomas", "Spondylolisthesis, ganglion cysts, fibrous dysplasia, and myositis ossificans"],
            "Intra-articular loose bodies ('joint mice') are small, unattached fragments of bone, cartilage, or fibrous tissue floating freely within a synovial cavity: 1. Osteochondritis dissecans (detached osteochondral flake, most common in young patients); 2. Synovial chondromatosis (synovial metaplasia forming hundreds of cartilaginous nodules); 3. Osteoarthritis (detached marginal osteophytes or fragmented fibrillated cartilage); 4. Traumatic osteochondral shear fractures.",
            clinical=False
        ),
        q(
            "In evaluating a patient with Flatfoot (Pes Planus), what simple clinical examination maneuver (Jack's toe-raise test) definitively differentiates a flexible flatfoot from a rigid flatfoot?",
            "Passive great toe hyperextension reconstitutes arch in flexible flatfoot",
            ["Active ankle dorsiflexion reconstitutes arch in rigid flatfoot", "Mediolateral calcaneal compression reconstitutes arch in flexible flatfoot", "Measuring intermalleolar distance differentiates flexibility"],
            "Jack's test (Great Toe Extension test) utilizes the Windlass mechanism: When the great toe is passively dorsiflexed, the plantar fascia is pulled taut around the first metatarsal head, which naturally elevates the medial longitudinal arch and inverts the calcaneus. If the arch reconstitutes, it is a normal/supple flexible flatfoot. If the arch remains completely flat, rigid, and locked, it indicates a rigid flatfoot (most commonly due to tarsal coalition or congenital vertical talus).",
            clinical=True
        ),
        q(
            "A 15-year-old adolescent presents with a rigid, severely painful, non-correctable flatfoot and recurrent ankle sprains. Peroneal muscle spasm is demonstrable on forced inversion. Plain oblique radiographs of the foot demonstrate an abnormal fibro-osseous bridge between the calcaneus and the navicular bone ('anteater nose' sign). What is the diagnosis?",
            "Tarsal coalition (calcaneonavicular coalition)",
            ["Congenital vertical talus", "Rocker-bottom foot secondary to CTEV", "Freiberg infraction"],
            "Tarsal coalition is an abnormal congenital failure of segmentation producing a fibrous, cartilaginous, or bony connection between two or more tarsal bones. The two most common varieties are Calcaneonavicular coalition (~50%) and Talocalcaneal (subtalar) coalition (~45%). Symptoms manifest in adolescence (12-16 years) as the coalition ossifies, producing rigid flatfoot, loss of subtalar motion, and peroneal spasticity. The elongated anterior process of calcaneus on oblique view resembles an 'anteater nose'.",
            clinical=True
        ),
        q(
            "In foot deformities, what are the precise anatomical alignment definitions of 'Hallux Valgus', and what radiographic cutoff angles define a moderate-to-severe deformity requiring surgical correction?",
            "Hallux valgus angle >15-20 degrees and intermetatarsal angle >9-10 degrees",
            ["Hallux valgus angle <5 degrees and intermetatarsal angle <5 degrees", "Fixed plantarflexion with intermetatarsal angle >45 degrees", "Dorsal toe subluxation with Bohler angle <10 degrees"],
            "Hallux valgus is a complex deformity characterized by lateral deviation of the hallux (great toe) and medial deviation of the first metatarsal, resulting in a prominent, painful bunion over the medial first metatarsal head. Normal radiographic angles: Hallux Valgus Angle (HVA, angle between first metatarsal and proximal phalanx) is < 15 degrees; Intermetatarsal Angle (IMA, angle between first and second metatarsals) is < 9 degrees. Angles exceeding these cutoffs indicate hallux valgus.",
            clinical=False
        ),
    ]),

    # Chapter 40: Amputations, Prosthetics and Orthotics (Easy - 5 questions)
    (40, "Amputations, Prosthetics and Orthotics", "easy", [
        q(
            "In a 62-year-old diabetic patient with non-reconstructable peripheral arterial dry gangrene involving all five toes, what is the ideal anatomical level for an elective Transtibial (Below-Knee) Amputation to provide the most optimal stump for prosthetic fitting?",
            "12 to 15 cm below knee joint line with posterior flap (Burgess)",
            ["Through mid-patellar tendon at the joint line", "2 cm above medial malleolus to preserve maximal length", "Immediately distal to tibial tuberosity within 3 cm"],
            "The ideal below-knee (transtibial) amputation stump is 12 to 15 cm below the knee joint line (or at the junction of the upper and middle thirds of the leg). Stumps shorter than 7-8 cm lack adequate lever arm to control a prosthesis, while stumps longer than 15-18 cm have poor distal blood supply and inadequate clearance for modern dynamic prosthetic foot components. The Burgess technique utilizes a well-vascularized long posterior flap rich in sural artery supply.",
            clinical=True
        ),
        q(
            "What is the precise anatomical level of bone transection in a classic 'Syme's Amputation' of the foot, and what unique weight-bearing feature does it offer?",
            "Ankle disarticulation with malleolar shaving; provides end-bearing heel pad",
            ["Midshaft metatarsal transection; non-weight-bearing stump", "Chopart midtarsal disarticulation; non-end-bearing stump", "Calcaneal excision with talar preservation; requires crutches"],
            "Syme's amputation is an ankle disarticulation where the distal articular surfaces of the tibia and fibula (including both malleoli) are shaved off flush with the joint line. The specialized, thick, fibrofatty heel pad (which has durable shock-absorbing fibrous septa) is preserved and anchored over the flat cut end of the tibia, providing a true end-bearing stump that allows the patient to walk short distances even without a prosthesis.",
            clinical=False
        ),
        q(
            "A 45-year-old male who underwent an above-knee amputation 3 weeks ago complains of intense, burning, and crushing pain perceived as originating from the absent toes and foot of the amputated limb. The surgical stump is completely healed with no signs of infection or neuroma. What is this neuropathic phenomenon termed, and what is the first-line medical therapy?",
            "Phantom limb pain (treated with gabapentinoids and mirror therapy)",
            ["Phantom limb sensation (managed with immediate revision surgery)", "Terminal osteomyelitis (treated with intravenous vancomycin)", "Complex regional pain syndrome Type II (treated with sympathectomy)"],
            "Phantom limb pain is severe, painful neuropathic dysesthesia perceived in the missing, amputated portion of the limb (present in up to 60-80% of amputees). It must be distinguished from benign 'phantom limb sensation' (painless awareness of the missing limb, which is universal and harmless). Phantom pain is central/neuropathic in origin; first-line management involves neuropathic pain medications (gabapentin, pregabalin, duloxetine) combined with psychological mirror-box therapy.",
            clinical=True
        ),
        q(
            "What critical physiological feature distinguishes lower-extremity amputations in growing children from adult amputations, and how does it influence surgical technique?",
            "Appositional terminal bone spike overgrowth; disarticulation is preferred",
            ["Complete failure of stump wound healing; transfixion is avoided", "Inability to fit prostheses before age 18; amputation is delayed", "Immediate premature closure of all proximal physes within 24 hours"],
            "In children, transecting a long bone diaphysis triggers vigorous, continuous appositional bone overgrowth from the periosteum and cut medullary canal, producing a sharp, conical bone spike that pushes through the distal skin flap. This is NOT due to physeal growth, but appositional osteogenesis. Consequently, in pediatric orthopaedics, joint disarticulations (e.g., knee or ankle disarticulation) that preserve intact epiphyseal cartilaginous caps are strongly preferred over diaphyseal amputations.",
            clinical=False
        ),
        q(
            "What is the structural design and kinematic function of a SACH (Solid Ankle Cushion Heel) prosthetic foot in lower-limb prosthetics?",
            "Solid keel with compressible rubber heel simulating plantarflexion",
            ["Microprocessor-controlled motorized powered dorsiflexion unit", "Multiaxial hydraulic ankle allowing 40 degrees of inversion", "Rigid uncushioned titanium blade designed solely for sprinting"],
            "The SACH (Solid Ankle Cushion Heel) foot is the most widely used basic, non-articulated prosthetic foot: It has a rigid internal keel covered with molded polyurethane foam, with no moving mechanical joints. At heel strike, the soft, compressible rubber wedge in the heel compresses under body weight, simulating normal ankle plantarflexion (bringing the forefoot rapidly into contact with the ground) and absorbing shock during early stance phase.",
            clinical=False
        ),
    ]),

    # Chapter 41: Arthroscopic Surgery (Easy - 5 questions)
    (41, "Arthroscopic Surgery", "easy", [
        q(
            "What fundamental optical and surgical principle governs the technique of 'triangulation' in diagnostic and operative arthroscopic surgery?",
            "Arthroscope and instrument portals converge at target pathology",
            ["Three surgeons operating simultaneously across three monitors", "Joint divided into three geometric zones by percutaneous sutures", "Irrigation delivered through three high-pressure inflow cannulas"],
            "Triangulation is the cornerstone technique of all arthroscopic surgery: The telescope (arthroscope) is inserted through one portal (e.g., anterolateral) and the working instrument (probe, shaver, punch) is inserted through a second portal (e.g., anteromedial). The surgeon visualizes the field on the monitor and directs both instruments so their trajectories meet precisely at the target intra-articular lesion, creating a triangle whose apex is the operative site.",
            clinical=False
        ),
        q(
            "In standard diagnostic arthroscopy of the knee joint, what are the two primary anterior portals established and their precise anatomical locations relative to the patellar tendon?",
            "Anterolateral (viewing) and anteromedial (working) portals 1 cm adjacent to patellar tendon",
            ["Superior patellar and trans-patellar tendon splitting portals", "Posteromedial and central popliteal fossa portals", "Anterior tibial tubercle and fibular head portals"],
            "The standard anterior portals for knee arthroscopy: 1. Anterolateral portal: Established 1 cm above the lateral joint line and 1 cm lateral to the lateral border of the patellar tendon (primary viewing portal, providing optimal visualization of the intercondylar notch, medial and lateral compartments); 2. Anteromedial portal: Established 1 cm above the medial joint line and 1 cm medial to the patellar tendon (primary working portal for probes, shavers, and suture passers).",
            clinical=False
        ),
        q(
            "What is considered an absolute contraindication to performing an elective arthroscopic procedure on a knee or shoulder joint?",
            "Active superficial skin infection or cellulitis over portal sites",
            ["History of a closed diaphyseal fracture united 5 years ago", "Presence of a traumatic bucket-handle meniscal tear", "Age over 60 years with mild degenerative joint disease"],
            "Absolute contraindications to arthroscopy include: 1. Active superficial skin infection, cellulitis, or furunculosis overlying the portal entry sites (high risk of seeding the joint with bacteria and causing devastating septic arthritis); 2. Severe joint ankylosis or dense arthrofibrosis that mechanically prevents joint distension and safe telescope insertion. Relative contraindications include severe capsular disruption with extensive extravasation into soft tissues.",
            clinical=True
        ),
        q(
            "What is the standard, physiological irrigation fluid utilized for joint distension during diagnostic and therapeutic arthroscopic procedures, and why are non-electrolyte solutions like distilled water strictly avoided?",
            "Normal saline or Ringer's lactate; hypotonic water causes chondrocyte lysis",
            ["10% Dextrose; provides metabolic glucose to articular chondrocytes", "Distilled water; provides superior optical refraction index", "Pure glycine 1.5%; mandatory for all orthopaedic joint procedures"],
            "Isotonic electrolyte solutions such as Normal Saline (0.9% NaCl) or Ringer's Lactate are the standard distension and irrigation media in orthopaedics. Hypotonic solutions like sterile water cause acute osmotic swelling and irreversible chondrocyte lysis. While non-conductive solutions like glycine or sorbitol are required for monopolar electrocautery in urology, in orthopaedics, bipolar radiofrequency devices operate safely in normal saline.",
            clinical=False
        ),
        q(
            "Which clinical condition represents a primary, high-yield therapeutic indication for knee arthroscopy?",
            "Partial meniscectomy or meniscal repair for symptomatic meniscal tear",
            ["End-stage tricompartmental osteoarthritis with fixed 30-degree varus", "Acute hematogenous osteomyelitis of the mid-femoral diaphysis", "Infantile developmental hip dislocation"],
            "The primary therapeutic indications for knee arthroscopy include: 1. Meniscal tears (partial meniscectomy or meniscal repair/suturing); 2. Anterior or Posterior Cruciate Ligament (ACL/PCL) reconstruction; 3. Removal of symptomatic intra-articular loose bodies; 4. Synovectomy in rheumatoid arthritis or pigmented villonodular synovitis; 5. Microfracture or chondroplasty for isolated focal articular cartilage defects.",
            clinical=False
        ),
    ]),

    # Chapter 42: Joint Replacement Surgery (Easy - 5 questions)
    (42, "Joint Replacement Surgery", "easy", [
        q(
            "An 80-year-old sedentary female sustains a displaced intracapsular transcervical fracture of the femoral neck (Garden Type IV). Pre-injury, she walked only indoors with a stick, and pelvic radiographs demonstrate healthy, well-preserved acetabular articular cartilage. Which surgical procedure is the treatment of choice?",
            "Unipolar or bipolar hemiarthroplasty of the hip",
            ["Total hip arthroplasty with cemented acetabular cup", "Closed reduction with percutaneous cancellous screw fixation", "Girdlestone excision arthroplasty"],
            "In elderly, low-demand, sedentary patients (>75-80 years) with displaced femoral neck fractures and a normal, healthy acetabulum, Hemiarthroplasty (Austin-Moore, Thompson, or modern modular bipolar hemiarthroplasty) is the gold standard: it replaces only the damaged femoral head and neck while preserving the native acetabular cartilage. It is technically simpler, has shorter operating time, lower dislocation rates, and allows immediate full weight-bearing.",
            clinical=True
        ),
        q(
            "What fundamental anatomical and prosthetic distinction differentiates a 'Total Hip Arthroplasty' (THA) from a 'Hemiarthroplasty' of the hip?",
            "THA resurfaces both femoral head and acetabulum; hemiarthroplasty replaces only femoral head",
            ["THA replaces femoral stem only; hemiarthroplasty replaces knee as well", "THA is always uncemented; hemiarthroplasty always requires ceramic cement", "THA preserves femoral neck; hemiarthroplasty excises entire proximal femur"],
            "The fundamental difference is acetabular resurfacing: Hemiarthroplasty ('half joint replacement') replaces only the femoral side of the hip joint with a prosthetic stem and metallic head that articulates directly against the patient's native cartilaginous acetabulum. Total Hip Arthroplasty (THA) replaces both sides: a prosthetic cup (polyethylene, ceramic, or metal) is implanted into the reamed acetabular bone, and a prosthetic femoral stem with a modular head articulates inside this artificial socket.",
            clinical=False
        ),
        q(
            "A 62-year-old active male presents with end-stage tricompartmental osteoarthritis of the right knee with severe rest pain, night pain, and progressive limitation of walking distance to less than 100 meters, refractory to all medical management. What is the definitive surgical procedure of choice?",
            "Total knee arthroplasty (TKA)",
            ["Unicompartmental (partial) knee replacement", "High tibial closing-wedge osteotomy", "Knee joint arthrodesis"],
            "Total Knee Arthroplasty (TKA / Total Knee Replacement) is the definitive surgical gold standard for advanced, end-stage tricompartmental osteoarthritis that has failed comprehensive conservative management. TKA resurfaces the distal femoral condyles, the proximal tibial plateau (with a metal baseplate and ultra-high-molecular-weight polyethylene insert), and patella if needed, restoring anatomical alignment, stability, and relieving pain in >90-95% of patients.",
            clinical=True
        ),
        q(
            "What is the chemical composition of orthopaedic 'bone cement' used for implant fixation in cemented arthroplasty, and what is its biomechanical mechanism of action?",
            "Polymethylmethacrylate (PMMA); acts as a mechanical grout without adhesive properties",
            ["Calcium hydroxyapatite paste; forms covalent peptide bonds to collagen", "Polyurethane resin; expands elastically to create vacuum seal", "Cyanoacrylate glue; adheres titanium directly to cortical periosteum"],
            "Orthopaedic bone cement is Polymethylmethacrylate (PMMA), formed by an exothermic polymerization reaction mixing liquid methylmethacrylate monomer with powdered PMMA polymer. Crucially, bone cement is NOT a glue: it possesses no adhesive properties. Rather, it functions as a mechanical 'grout' that interlocks into the porous cancellous bone trabeculae and conforms tightly to the prosthesis, distributing axial and torsional loads uniformly across a large surface area.",
            clinical=False
        ),
        q(
            "What is the most devastating late complication of total joint arthroplasty that typically necessitates a two-stage revision procedure (implant removal, antibiotic-loaded cement spacer, followed by delayed reimplantation)?",
            "Periprosthetic joint infection (PJI) with biofilm formation",
            ["Superficial wound ecchymosis", "Heterotopic ossification Brooker Grade I", "Transient peroneal neuropraxia resolving in 2 weeks"],
            "Periprosthetic Joint Infection (PJI) is the most challenging and dreaded complication of joint replacement (affecting 1-2% of primary arthroplasties). Bacteria (most commonly Staphylococcus aureus and coagulase-negative staphylococci) adhere to the metallic and polyethylene surfaces, secreting a protective polysaccharide extracellular slime matrix (biofilm) that shields them from systemic antibiotics and host immune cells. Eradication almost always requires complete removal of all implants, extensive debridement, and a staged revision.",
            clinical=True
        ),
    ]),
]
