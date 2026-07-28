import json
from collections import Counter
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Bones, Joints, and Soft Tissue Tumors"
BASE = {"subjectId": "pathology", "subjectTitle": "Pathology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(difficulty, prompt, answer, distractors, explanation):
    if difficulty not in {"easy", "moderate", "high"}:
        raise ValueError(difficulty)
    options = [answer, *distractors]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(prompt)
    return {"difficulty": difficulty, "prompt": prompt, "options": options, "answerIndex": 0, "answer": answer, "explanation": explanation}


def jumble(question, desired_index):
    answer = question["answer"]
    distractors = [option for option in question["options"] if option != answer]
    options = distractors[:]
    options.insert(desired_index, answer)
    question["options"] = options
    question["answerIndex"] = desired_index
    return question


TOPICS = [
    ("bone-formation-remodeling", "Bone Formation, Remodeling, and Metabolic Bone Disease", [
        q("easy", "Osteoblasts are responsible for:", "Bone formation", ["Bone resorption", "Cartilage digestion", "Synovial fluid production"], "Osteoblasts synthesize osteoid and mineralize bone."),
        q("easy", "Osteoclasts are responsible for:", "Bone resorption", ["Osteoid production", "Collagen synthesis only", "Cartilage formation"], "Osteoclasts resorb mineralized bone."),
        q("easy", "Osteoporosis is characterized by:", "Reduced bone mass with normal mineralization", ["Excess osteoid", "Defective collagen I only", "Infected marrow"], "Osteoporosis has quantitatively reduced but normally mineralized bone."),
        q("moderate", "Osteomalacia in adults results from defective:", "Mineralization of osteoid", ["Osteoclast absence", "PTH receptor activation", "Cartilage tumor formation"], "Osteomalacia is failure to mineralize newly formed osteoid."),
        q("moderate", "Rickets affects children at the:", "Growth plate", ["Articular cartilage only", "Synovial membrane", "Tendon insertion only"], "Rickets disturbs mineralization at growth plates."),
        q("moderate", "Paget disease of bone has an early phase of excessive:", "Osteoclastic bone resorption", ["Marrow aplasia", "Cartilage necrosis", "Synovial pannus"], "Paget disease begins with increased osteoclast activity."),
        q("moderate", "Mosaic lamellar bone is characteristic of:", "Paget disease of bone", ["Osteoporosis", "Osteomalacia", "Achondroplasia"], "Paget disease produces a jigsaw mosaic cement-line pattern."),
        q("high", "An elderly woman develops vertebral compression fractures after menopause. Biopsy would show thin trabeculae with normal mineral-to-matrix ratio rather than excess unmineralized osteoid. Which disorder is present?", "Osteoporosis", ["Osteomalacia", "Paget disease", "Osteopetrosis"], "Osteoporosis is low bone mass with normal mineralization."),
        q("high", "An adult with vitamin D deficiency has bone pain and fractures. Biopsy shows abundant unmineralized osteoid lining trabeculae because osteoid mineralization is defective. Which diagnosis fits?", "Osteomalacia", ["Osteoporosis", "Osteosarcoma", "Osteopetrosis"], "Osteomalacia is defective mineralization in adults."),
        q("high", "An older man has enlarged skull, hearing loss, elevated alkaline phosphatase, and bone biopsy showing thick disorganized trabeculae with mosaic cement lines. Which disease is most likely?", "Paget disease of bone", ["Rickets", "Osteoporosis", "Fibrous dysplasia"], "Paget disease causes disordered remodeling and mosaic lamellar bone."),
    ]),
    ("genetic-developmental", "Genetic and Developmental Bone Disorders", [
        q("easy", "Achondroplasia is caused by activating mutation in:", "FGFR3", ["COL1A1", "RB1", "EXT1"], "FGFR3 activation inhibits chondrocyte proliferation."),
        q("easy", "Osteogenesis imperfecta involves defective:", "Type I collagen", ["Type IV collagen", "Elastin", "Fibrillin"], "OI is caused by defects in type I collagen."),
        q("easy", "Osteopetrosis is caused by defective:", "Osteoclast bone resorption", ["Osteoblast formation", "Vitamin D absorption only", "Cartilage proliferation"], "Failure of osteoclast resorption produces dense brittle bones."),
        q("moderate", "Achondroplasia causes short limbs because it impairs:", "Endochondral ossification", ["Intramembranous ossification only", "Osteoid mineralization only", "Marrow hematopoiesis only"], "Long bone growth depends on endochondral ossification."),
        q("moderate", "Osteogenesis imperfecta commonly causes:", "Blue sclerae and brittle bones", ["Exophthalmos", "Skin warts", "Hypercalcemia always"], "Type I collagen defects affect bone and sclera."),
        q("moderate", "Osteopetrosis may cause anemia because dense bone narrows:", "Marrow cavities", ["Synovial spaces", "Growth plates", "Articular cartilage"], "Marrow space obliteration impairs hematopoiesis."),
        q("moderate", "Hereditary multiple exostoses are associated with mutations in:", "EXT genes", ["RET", "VHL", "HFE"], "EXT mutations cause multiple osteochondromas."),
        q("high", "A child has rhizomelic limb shortening, large head, frontal bossing, and normal trunk length. The mutation increases signaling that suppresses growth plate chondrocyte proliferation. Which disorder is likely?", "Achondroplasia", ["Osteogenesis imperfecta", "Osteopetrosis", "Marfan syndrome"], "Achondroplasia is due to activating FGFR3 mutation."),
        q("high", "A child has recurrent fractures, blue sclerae, hearing loss, and abnormal dentin due to defective synthesis of a major bone matrix collagen. Which disease is most likely?", "Osteogenesis imperfecta", ["Achondroplasia", "Rickets", "Osteopetrosis"], "OI is caused by type I collagen defects."),
        q("high", "An infant has diffusely dense brittle bones, cranial nerve compression, anemia, and hepatosplenomegaly due to failure of bone resorption. Which cell type is defective?", "Osteoclast", ["Osteoblast", "Chondrocyte", "Synoviocyte"], "Osteopetrosis results from impaired osteoclast function."),
    ]),
    ("fracture-necrosis-infection", "Fracture Healing, Osteonecrosis, and Osteomyelitis", [
        q("easy", "Osteomyelitis means infection of:", "Bone", ["Synovium only", "Cartilage only", "Tendon"], "Osteomyelitis is infection of bone and marrow."),
        q("easy", "The most common cause of acute hematogenous osteomyelitis is:", "Staphylococcus aureus", ["HPV", "Candida in all cases", "Giardia"], "S. aureus is the classic organism."),
        q("easy", "Avascular necrosis is bone death due to loss of:", "Blood supply", ["Vitamin C", "Synovial fluid", "Collagen only"], "Ischemia causes osteonecrosis."),
        q("moderate", "Sequestrum refers to:", "Dead bone separated by infection", ["New periosteal bone only", "Cartilage cap", "Synovial pannus"], "A sequestrum is necrotic bone in osteomyelitis."),
        q("moderate", "Involucrum means:", "New reactive bone around sequestrum", ["Unmineralized osteoid", "Tumor osteoid", "Chondrocyte proliferation"], "Involucrum is reactive bone surrounding infected necrotic bone."),
        q("moderate", "Fracture healing initially forms a:", "Hematoma and soft callus", ["Sarcoma", "Tophus", "Pannus"], "Hemorrhage and inflammation precede callus formation."),
        q("moderate", "Sickle cell disease predisposes to osteomyelitis by:", "Bone infarction", ["FGFR3 activation", "Type I collagen defect", "Vitamin D excess"], "Infarcted bone is vulnerable to infection."),
        q("high", "A child has fever, bone pain, and metaphyseal infection. Cultures grow Staphylococcus aureus, and imaging later shows necrotic bone separated from viable tissue. What is the necrotic fragment called?", "Sequestrum", ["Involucrum", "Osteoid seam", "Osteophyte"], "Sequestrum is dead infected bone."),
        q("high", "A patient with femoral neck fracture develops collapse of the femoral head months later because the epiphyseal blood supply was disrupted. Which process caused the collapse?", "Avascular necrosis", ["Osteomalacia", "Osteopetrosis", "Synovial chondromatosis"], "Femoral head ischemia causes osteonecrosis and collapse."),
        q("high", "A fracture site first forms hematoma, then fibrocartilaginous soft callus, followed by woven bone and later lamellar remodeling. Which repair process is being described?", "Secondary fracture healing", ["Primary intention skin healing", "Tumor ossification", "Pannus formation"], "Most fractures heal through callus formation and remodeling."),
    ]),
    ("bone-forming-tumors", "Bone-Forming Tumors: Osteoma, Osteoid Osteoma, and Osteosarcoma", [
        q("easy", "Osteosarcoma is a malignant tumor producing:", "Osteoid", ["Mucin", "Keratin", "Amyloid"], "Malignant osteoid production defines osteosarcoma."),
        q("easy", "Osteoid osteoma pain is classically relieved by:", "Aspirin or NSAIDs", ["Insulin", "Antibiotics always", "Thyroxine"], "Prostaglandin-mediated pain responds to NSAIDs."),
        q("easy", "Osteosarcoma most often arises near the:", "Knee", ["Skull base only", "Small hand bones only", "Ribs only"], "Distal femur and proximal tibia are common sites."),
        q("moderate", "Osteoid osteoma is usually less than:", "2 cm", ["10 cm", "20 cm", "30 cm"], "Osteoid osteoma has a small nidus."),
        q("moderate", "Osteosarcoma is associated with mutation in:", "RB and TP53 pathways", ["HBB only", "CFTR only", "RET only"], "Tumor suppressor pathway defects increase risk."),
        q("moderate", "Codman triangle may be seen in:", "Osteosarcoma", ["Osteoid osteoma only", "Osteochondroma", "Gout"], "Aggressive periosteal elevation can create Codman triangle."),
        q("moderate", "Parosteal osteosarcoma arises on the:", "Bone surface", ["Synovial membrane", "Marrow only", "Articular cartilage only"], "Parosteal tumors are surface osteosarcomas."),
        q("high", "A teenager has painful metaphyseal mass around the knee. Imaging shows sunburst periosteal reaction, and biopsy shows malignant cells producing lace-like osteoid. Which tumor is most likely?", "Osteosarcoma", ["Ewing sarcoma", "Chondrosarcoma", "Osteochondroma"], "Osteosarcoma is malignant osteoid-forming tumor."),
        q("high", "A young adult has nocturnal bone pain relieved by aspirin. Imaging shows a small radiolucent nidus surrounded by reactive sclerosis. Which benign bone tumor is most likely?", "Osteoid osteoma", ["Osteoblastoma", "Osteosarcoma", "Giant cell tumor"], "Osteoid osteoma is small and NSAID-responsive."),
        q("high", "A child with hereditary retinoblastoma later develops an aggressive metaphyseal bone tumor producing malignant osteoid around the knee. Which tumor risk is increased by RB mutation?", "Osteosarcoma", ["Chondroma", "Fibrous dysplasia", "Osteochondroma"], "RB mutation predisposes to osteosarcoma."),
    ]),
    ("cartilage-giant-ewing", "Cartilage Tumors, Giant Cell Tumor, and Ewing Sarcoma", [
        q("easy", "Osteochondroma is a benign bone tumor with a cartilage:", "Cap", ["Core of pus", "Amyloid center", "Keratin plug"], "Osteochondroma is cartilage-capped bony outgrowth."),
        q("easy", "Chondrosarcoma is malignant tumor producing:", "Cartilage", ["Osteoid only", "Mucin only", "Keratin"], "Chondrosarcoma produces malignant cartilage."),
        q("easy", "Ewing sarcoma is a small round blue cell tumor of:", "Bone", ["Thyroid", "Skin epidermis", "Parathyroid"], "Ewing sarcoma commonly arises in bone."),
        q("moderate", "Ewing sarcoma is associated with translocation:", "t(11;22)", ["t(9;22)", "t(14;18)", "t(15;17)"], "EWSR1-FLI1 commonly results from t(11;22)."),
        q("moderate", "Giant cell tumor of bone commonly arises in:", "Epiphysis", ["Metaphysis only", "Diaphysis only", "Skull sutures"], "Giant cell tumor usually involves epiphysis of long bones."),
        q("moderate", "Osteochondroma points away from the:", "Joint", ["Medullary cavity", "Periosteum", "Epiphysis always"], "Osteochondromas grow away from the nearest joint."),
        q("moderate", "Chondrosarcoma usually affects:", "Adults", ["Infants only", "Toddlers only", "Only teenagers"], "Chondrosarcoma is more common in adults."),
        q("high", "A child has a painful diaphyseal bone mass. Biopsy shows sheets of small round blue cells with glycogen, and genetic testing shows EWSR1-FLI1 fusion. Which tumor is most likely?", "Ewing sarcoma", ["Osteosarcoma", "Chondrosarcoma", "Giant cell tumor"], "Ewing sarcoma is linked to t(11;22)."),
        q("high", "A skeletally mature young adult has an expansile lytic epiphyseal lesion around the knee. Biopsy shows mononuclear stromal cells and numerous osteoclast-like giant cells. Which tumor fits?", "Giant cell tumor of bone", ["Osteochondroma", "Osteoid osteoma", "Enchondroma"], "Giant cell tumor is epiphyseal with osteoclast-like giant cells."),
        q("high", "An adult has a destructive pelvic bone tumor composed of malignant chondrocytes in lacunae producing abundant cartilaginous matrix with permeative growth. Which diagnosis is most likely?", "Chondrosarcoma", ["Osteosarcoma", "Ewing sarcoma", "Fibrous dysplasia"], "Chondrosarcoma is malignant cartilage-forming tumor."),
    ]),
    ("arthritis-degenerative", "Osteoarthritis and Degenerative Joint Disease", [
        q("easy", "Osteoarthritis primarily involves degeneration of:", "Articular cartilage", ["Synovial lymphocytes", "Bone marrow only", "Tendon sheaths"], "OA begins with cartilage degeneration."),
        q("easy", "Osteophytes are bony:", "Outgrowths at joint margins", ["Necrotic fragments", "Crystal deposits", "Synovial tumors"], "Osteophytes are marginal bony spurs."),
        q("easy", "Osteoarthritis is commonly associated with:", "Aging and mechanical stress", ["Anti-CCP antibodies", "Urate crystals only", "HLA-B27 only"], "OA is degenerative and mechanical."),
        q("moderate", "Eburnation means polished exposed:", "Subchondral bone", ["Synovium", "Cartilage cap", "Tendon"], "Loss of cartilage exposes polished bone."),
        q("moderate", "Heberden nodes involve the:", "Distal interphalangeal joints", ["Elbows only", "Sacroiliac joints", "Temporomandibular joint only"], "DIP osteophytes form Heberden nodes."),
        q("moderate", "Osteoarthritis inflammation is usually:", "Mild compared with rheumatoid arthritis", ["Always granulomatous", "Always purulent", "Absent from all joints"], "OA is primarily degenerative with secondary inflammation."),
        q("moderate", "Subchondral cysts in osteoarthritis are also called:", "Geodes", ["Tophi", "Pannus", "Sequestra"], "Geodes are subchondral cystic spaces."),
        q("high", "An elderly patient has chronic knee pain worse with use. X-ray shows joint space narrowing, osteophytes, subchondral sclerosis, and cysts. Which disease is most likely?", "Osteoarthritis", ["Rheumatoid arthritis", "Gout", "Septic arthritis"], "OA causes degenerative cartilage loss and osteophytes."),
        q("high", "A joint surface in advanced osteoarthritis has complete cartilage loss with smooth ivory-like polishing of the exposed subchondral bone. Which gross change is described?", "Eburnation", ["Pannus", "Tophus", "Ankylosis"], "Eburnation is polished exposed bone in OA."),
        q("high", "A patient has bony enlargement of distal interphalangeal joints from marginal osteophyte formation in chronic degenerative joint disease of the hands. What are these nodules called?", "Heberden nodes", ["Bouchard rheumatoid nodules", "Tophi", "Rice bodies"], "Heberden nodes are DIP osteophytes in OA."),
    ]),
    ("inflammatory-arthritis", "Rheumatoid Arthritis, Spondyloarthritis, and Septic Arthritis", [
        q("easy", "Rheumatoid arthritis is an autoimmune disease primarily affecting:", "Synovial joints", ["Hair follicles", "Thyroid follicles", "Renal tubules"], "RA is chronic inflammatory synovitis."),
        q("easy", "Pannus is proliferative inflamed:", "Synovium", ["Cartilage cap", "Necrotic bone", "Adipose tissue"], "Pannus invades cartilage and bone."),
        q("easy", "Septic arthritis is infection of a:", "Joint", ["Bone only", "Tendon only", "Skin only"], "Septic arthritis is microbial infection of joint space."),
        q("moderate", "Rheumatoid arthritis is associated with antibodies to:", "Citrullinated peptides", ["Desmoglein", "TSH receptor", "GBM"], "Anti-CCP antibodies are characteristic."),
        q("moderate", "Rheumatoid nodules have central:", "Fibrinoid necrosis", ["Keratin pearls", "Amyloid only", "Cartilage cap"], "Rheumatoid nodules show necrotizing granulomatous inflammation."),
        q("moderate", "Ankylosing spondylitis is associated with:", "HLA-B27", ["HLA-B8 only", "RET", "RB1"], "HLA-B27 is strongly associated."),
        q("moderate", "Septic arthritis most commonly involves:", "Neutrophilic joint inflammation", ["Pannus only", "Urate tophi only", "Osteophytes only"], "Bacterial infection causes purulent inflammation."),
        q("high", "A woman has symmetric small-joint arthritis, prolonged morning stiffness, anti-CCP antibodies, rheumatoid factor, and synovial pannus eroding cartilage and bone. Which disease is most likely?", "Rheumatoid arthritis", ["Osteoarthritis", "Gout", "Osteomyelitis"], "RA is autoimmune pannus-forming synovitis."),
        q("high", "A subcutaneous nodule from a patient with rheumatoid arthritis shows central fibrinoid necrosis surrounded by palisading macrophages and chronic inflammation. Which lesion is present?", "Rheumatoid nodule", ["Tophus", "Granuloma annulare only", "Osteophyte"], "Rheumatoid nodules have necrobiotic centers and palisading histiocytes."),
        q("high", "A young man has inflammatory back pain, bilateral sacroiliitis, reduced spinal mobility, enthesitis, uveitis, and eventual radiographic bamboo spine. Which HLA-associated disease is likely?", "Ankylosing spondylitis", ["Rheumatoid arthritis", "Osteoarthritis", "Septic arthritis"], "Ankylosing spondylitis is an HLA-B27 spondyloarthritis."),
    ]),
    ("crystal-synovial", "Crystal Arthropathies and Synovial Lesions", [
        q("easy", "Gout is caused by deposition of:", "Monosodium urate crystals", ["Calcium pyrophosphate only", "Cholesterol", "Cystine"], "Urate crystals cause gout."),
        q("easy", "Pseudogout is caused by:", "Calcium pyrophosphate crystals", ["Monosodium urate", "Hydroxyapatite only", "Keratin"], "CPPD causes pseudogout."),
        q("easy", "A tophus is a deposit of:", "Urate crystals with inflammation", ["Bacterial pus", "Cartilage cap", "Tumor osteoid"], "Tophi are gouty urate deposits."),
        q("moderate", "Gout crystals are:", "Needle-shaped and negatively birefringent", ["Rhomboid and positively birefringent", "Cubic and nonbirefringent", "Round fat droplets"], "Urate crystals are needle-shaped and negatively birefringent."),
        q("moderate", "Pseudogout crystals are:", "Rhomboid and positively birefringent", ["Needle-shaped and negative", "Branching hyphae", "Hexagonal cystine"], "CPPD crystals are rhomboid and weakly positive."),
        q("moderate", "Chondrocalcinosis is associated with:", "CPPD deposition", ["Rheumatoid pannus", "Osteosarcoma", "Ewing sarcoma"], "CPPD often calcifies cartilage."),
        q("moderate", "Tenosynovial giant cell tumor often contains:", "Hemosiderin-laden macrophages", ["Keratin pearls", "Psammoma bodies", "Schiller-Duval bodies"], "Pigmented villonodular synovitis has hemosiderin."),
        q("high", "A man has sudden severe pain in the first metatarsophalangeal joint. Synovial fluid contains needle-shaped crystals with strong negative birefringence. Which disease is most likely?", "Gout", ["Pseudogout", "Septic arthritis", "Osteoarthritis"], "Podagra with negatively birefringent urate crystals indicates gout."),
        q("high", "An older patient has acute knee arthritis and x-ray chondrocalcinosis. Synovial fluid contains rhomboid crystals with weak positive birefringence. Which crystal disease is present?", "Pseudogout", ["Gout", "Rheumatoid arthritis", "Ankylosing spondylitis"], "CPPD causes pseudogout and chondrocalcinosis."),
        q("high", "A synovial mass shows villous and nodular proliferation with foamy macrophages, multinucleated giant cells, stromal cells, and abundant hemosiderin. Which lesion is most likely?", "Tenosynovial giant cell tumor", ["Rheumatoid pannus", "Synovial sarcoma", "Gouty tophus"], "Tenosynovial giant cell tumor includes pigmented villonodular synovitis."),
    ]),
    ("soft-tissue-benign", "Benign Soft Tissue Tumors and Tumor-Like Lesions", [
        q("easy", "Lipoma is a benign tumor of:", "Adipose tissue", ["Smooth muscle", "Skeletal muscle", "Peripheral nerve"], "Lipomas are benign mature fat tumors."),
        q("easy", "Hemangioma is a benign tumor of:", "Blood vessels", ["Fat", "Cartilage", "Bone"], "Hemangiomas are benign vascular tumors."),
        q("easy", "Leiomyoma is a benign tumor of:", "Smooth muscle", ["Skeletal muscle", "Adipose tissue", "Synovium"], "Leiomyomas show smooth muscle differentiation."),
        q("moderate", "Nodular fasciitis is notable for:", "Rapid growth but benign behavior", ["High metastatic rate", "Cartilage matrix", "Urate crystals"], "Nodular fasciitis is a self-limited reactive proliferation."),
        q("moderate", "Desmoid-type fibromatosis is:", "Locally aggressive but nonmetastasizing", ["Always benign with no recurrence", "Highly metastatic", "A vascular malformation"], "Desmoid tumors infiltrate locally but do not metastasize."),
        q("moderate", "Schwannoma is often associated with:", "Antoni A and Antoni B areas", ["Osteoid seams", "Tophi", "Comedo necrosis"], "Schwannoma has alternating cellular and loose regions."),
        q("moderate", "Neurofibroma is associated with:", "NF1", ["RB1 only", "RET only", "HFE"], "Neurofibromas are common in neurofibromatosis type 1."),
        q("high", "A soft, mobile subcutaneous mass is composed of mature adipocytes without atypia and is well circumscribed. Which benign soft tissue tumor is most likely?", "Lipoma", ["Liposarcoma", "Desmoid tumor", "Leiomyosarcoma"], "Lipoma is a benign mature adipose tumor."),
        q("high", "A rapidly growing forearm nodule in a young adult shows plump myofibroblasts in a tissue-culture-like pattern but lacks atypical mitoses. Which lesion is likely?", "Nodular fasciitis", ["Fibrosarcoma", "Synovial sarcoma", "Malignant peripheral nerve sheath tumor"], "Nodular fasciitis grows quickly but is benign."),
        q("high", "A deep abdominal wall mass in a patient with familial adenomatous polyposis infiltrates muscle and recurs locally but does not metastasize. Which tumor is most likely?", "Desmoid-type fibromatosis", ["Lipoma", "Hemangioma", "Rhabdomyoma"], "Desmoid tumors are locally aggressive fibromatoses."),
    ]),
    ("soft-tissue-malignant", "Malignant Soft Tissue Tumors", [
        q("easy", "Liposarcoma is a malignant tumor of:", "Adipocytic differentiation", ["Bone-forming cells", "Cartilage only", "Synovium only"], "Liposarcomas show adipocytic differentiation."),
        q("easy", "Rhabdomyosarcoma shows skeletal muscle differentiation and is common in:", "Children", ["Elderly only", "Only postmenopausal women", "Only newborn girls"], "Rhabdomyosarcoma is a common pediatric soft tissue sarcoma."),
        q("easy", "Leiomyosarcoma is malignant tumor of:", "Smooth muscle", ["Fat", "Cartilage", "Bone"], "Leiomyosarcoma shows smooth muscle differentiation."),
        q("moderate", "Well-differentiated liposarcoma commonly shows amplification of:", "MDM2", ["RET", "HBB", "CFTR"], "MDM2 amplification supports atypical lipomatous tumor/liposarcoma."),
        q("moderate", "Embryonal rhabdomyosarcoma may show:", "Rhabdomyoblasts", ["Chondrocytes in lacunae", "Urate crystals", "Osteophytes"], "Rhabdomyoblasts indicate skeletal muscle differentiation."),
        q("moderate", "Synovial sarcoma is associated with translocation involving:", "SS18-SSX", ["BCR-ABL", "EWSR1-FLI1", "PML-RARA"], "Synovial sarcoma often has t(X;18) SS18-SSX fusion."),
        q("moderate", "Undifferentiated pleomorphic sarcoma was formerly called:", "Malignant fibrous histiocytoma", ["Ewing sarcoma", "Chondrosarcoma", "Osteoid osteoma"], "Many MFH tumors are now classified as UPS."),
        q("high", "A deep thigh mass in an older adult shows pleomorphic lipoblasts with scalloped nuclei and adipocytic differentiation. Which malignant soft tissue tumor is most likely?", "Liposarcoma", ["Lipoma", "Rhabdomyoma", "Synovial chondromatosis"], "Lipoblasts support liposarcoma."),
        q("high", "A child has a soft tissue tumor near the orbit composed of primitive cells with strap-shaped rhabdomyoblasts and skeletal muscle markers. Which sarcoma is likely?", "Rhabdomyosarcoma", ["Leiomyosarcoma", "Liposarcoma", "Desmoid tumor"], "Rhabdomyosarcoma is a pediatric skeletal muscle sarcoma."),
        q("high", "A young adult has a deep periarticular mass near the knee. Tumor shows epithelial and spindle components with t(X;18) SS18-SSX fusion. Which sarcoma is most likely?", "Synovial sarcoma", ["Ewing sarcoma", "Chondrosarcoma", "Giant cell tumor"], "Synovial sarcoma is defined by SS18-SSX fusion and often arises near joints."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch26-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 26 questions, got {len(chapter_questions)}")
    topic_counts = Counter(q["topic"] for q in chapter_questions)
    if len(topic_counts) != 10 or any(count != 10 for count in topic_counts.values()):
        raise ValueError(f"Bad topic distribution: {topic_counts}")
    expected = Counter({"easy": 3, "moderate": 4, "high": 3})
    for topic in topic_counts:
        counts = Counter(q["difficulty"] for q in chapter_questions if q["topic"] == topic)
        if counts != expected:
            raise ValueError(f"Bad difficulty distribution for {topic}: {counts}")
    for question in chapter_questions:
        options = question["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Bad options: {question['id']}")
        if question["answer"] != options[question["answerIndex"]]:
            raise ValueError(f"Bad answer: {question['id']}")
    short_high = [q["id"] for q in chapter_questions if q["difficulty"] == "high" and len(q["prompt"].split()) < 24]
    if short_high:
        raise ValueError(f"High-level prompts too short: {short_high[:5]}")
    if all_questions is not None:
        ids = [q.get("id") for q in all_questions]
        duplicates = [qid for qid, count in Counter(ids).items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate ids: {duplicates[:10]}")


def main():
    chapter_questions = build_questions()
    validate(chapter_questions)
    total_removed = 0
    for data_path in DATA_PATHS:
        data = json.loads(data_path.read_text(encoding="utf-8-sig"))
        existing = data.get("questions", [])
        kept = [
            question for question in existing
            if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch26-"))
        ]
        data["questions"] = kept + chapter_questions
        validate(chapter_questions, data["questions"])
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        removed = len(existing) - len(kept)
        total_removed += removed
        print(f"Updated {data_path}: removed {removed} existing Chapter 26 questions")
    print(f"Removed {total_removed} existing Chapter 26 questions across {len(DATA_PATHS)} databases")
    print(f"Added {len(chapter_questions)} Robbins Chapter 26 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
