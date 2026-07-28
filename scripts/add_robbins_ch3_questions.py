import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path("runtime-data/users.json")

BASE = {
    "subjectId": "pathology",
    "subjectTitle": "Pathology",
    "chapterTitle": "Inflammation and Repair",
    "source": "ai",
    "imageUrls": [],
}


def item(difficulty, prompt, options, answer_index, explanation):
    return {
        "difficulty": difficulty,
        "prompt": prompt,
        "options": options,
        "answerIndex": answer_index,
        "answer": options[answer_index],
        "explanation": explanation,
    }


def jumble_answer_position(question, desired_index):
    answer = question["answer"]
    distractors = [option for option in question["options"] if option != answer]
    if len(distractors) != 3:
        raise ValueError(f"Cannot jumble options for {question.get('id', question['prompt'])}")
    options = distractors[:]
    options.insert(desired_index, answer)
    question["options"] = options
    question["answerIndex"] = desired_index
    return question


TOPICS = [
    (
        "overview",
        "Introduction, Causes, and Recognition of Inflammation",
        [
            item("easy", "Which pair of tissue components carries out the two major reactions of inflammation?", ["Peripheral nerves and skeletal muscle", "Blood vessels and leukocytes", "Fibroblasts and chondrocytes", "Erythrocytes and platelets only"], 1, "Inflammation depends chiefly on vascular reactions and leukocyte responses, which together deliver plasma proteins and effector cells to the site of injury."),
            item("easy", "Which set contains the classic local signs of acute inflammation described in pathology?", ["Pallor, anesthesia, rigidity, and cyanosis", "Rubor, calor, tumor, and dolor", "Jaundice, pruritus, edema, and petechiae", "Necrosis, fibrosis, calcification, and atrophy"], 1, "Redness, heat, swelling, and pain reflect vasodilation, vascular leakage, and mediator effects on nerves."),
            item("easy", "What is the main protective purpose of inflammation?", ["To wall off every wound permanently with collagen", "To eliminate the offending agent and initiate repair", "To prevent all leukocytes from entering tissue", "To replace the immune system with coagulation"], 1, "Inflammation removes microbes or damaged tissue and sets the stage for tissue repair."),
            item("moderate", "Which description best defines acute inflammation?", ["Slow mononuclear infiltrate with fibrosis as the initial event", "Rapid response with vascular leakage and predominantly neutrophilic infiltrate", "Pure lymphocyte proliferation without vascular changes", "Permanent scar formation without mediator release"], 1, "Acute inflammation begins quickly, is usually short-lived, and commonly features edema and neutrophils."),
            item("moderate", "Which description best defines chronic inflammation?", ["A brief neutrophil-rich response lasting minutes", "Prolonged inflammation with mononuclear cells, tissue destruction, and repair", "A response limited to histamine release from mast cells", "A nonvascular response without leukocyte recruitment"], 1, "Chronic inflammation combines continuing injury, macrophages/lymphocytes, tissue damage, and attempts at healing."),
            item("moderate", "A sterile focus of necrotic tissue releases ATP, uric acid, and DNA fragments. These molecules are best classified as:", ["Opsonins", "Damage-associated molecular patterns", "Anaphylatoxins", "Selectin ligands"], 1, "Endogenous products of injured or necrotic cells act as DAMPs that trigger inflammation even without infection."),
            item("moderate", "Toll-like receptors are especially important in inflammation because they:", ["Degrade collagen in scars", "Recognize conserved microbial products and activate inflammatory signaling", "Convert fibrinogen into fibrin", "Transport neutrophils across lymph nodes"], 1, "TLRs are pattern-recognition receptors that detect microbial PAMPs and stimulate cytokine and inflammatory responses."),
            item("very high", "Activation of the NLRP3 inflammasome most directly promotes inflammation by increasing production of:", ["Albumin", "Mature interleukin-1", "Type I collagen", "Histamine"], 1, "The inflammasome activates caspase-1, which converts pro-IL-1 beta into active IL-1, a potent inflammatory cytokine."),
            item("very high", "Which stimulus is a typical trigger for inflammation through recognition of microbial or damaged-cell products?", ["Completely intact basement membrane", "Bacterial lipopolysaccharide binding pattern-recognition receptors", "Normal plasma oncotic pressure", "Inactive fibroblast collagen synthesis"], 1, "Microbial products such as LPS are PAMPs recognized by innate immune receptors."),
            item("very high", "Why can inflammation itself become harmful?", ["It always prevents tissue repair", "Leukocyte products and mediators can injure normal host tissues", "It blocks all plasma proteins from leaving vessels", "It permanently prevents immunity against microbes"], 1, "The same enzymes, ROS, cytokines, and mediators that attack microbes can damage bystander tissues when excessive or misdirected."),
        ],
    ),
    (
        "vascular",
        "Vascular Reactions in Acute Inflammation",
        [
            item("easy", "Redness and warmth in acute inflammation are mainly caused by:", ["Vasodilation and increased blood flow", "Venous thrombosis without arterial flow", "Fibroblast contraction", "Loss of all plasma proteins"], 0, "Arteriolar vasodilation increases local blood flow, producing rubor and calor."),
            item("easy", "An exudate differs from a transudate because an exudate is:", ["Protein-rich and caused by increased vascular permeability", "Protein-poor and caused only by hydrostatic pressure", "Made only of red cells", "Always sterile urine"], 0, "Inflammatory endothelial leakage produces protein-rich fluid and often cells, whereas transudates are low-protein ultrafiltrates."),
            item("easy", "Edema means:", ["Excess fluid in interstitial tissue or serous cavities", "Only pus inside an abscess", "Only fibrin inside a thrombus", "Loss of tissue fluid from dehydration"], 0, "Edema is abnormal fluid accumulation in tissues or body cavities."),
            item("moderate", "The most common mechanism of vascular leakage in acute inflammation is:", ["Endothelial contraction in postcapillary venules", "Complete arterial rupture in every case", "Permanent loss of basement membrane", "Lymphocyte-mediated fibrosis"], 0, "Histamine, bradykinin, and leukotrienes commonly cause endothelial contraction and intercellular gaps in venules."),
            item("moderate", "Which mediator is classically linked to rapid, transient endothelial contraction and vascular leakage?", ["Histamine", "Hemoglobin", "Keratin", "Myosin"], 0, "Histamine from mast cells is a classic early mediator of venular leakage."),
            item("moderate", "Stasis in acute inflammation develops mainly because:", ["Fluid leaves vessels, concentrating red cells and slowing flow", "Arterioles permanently constrict", "Leukocytes disappear from blood", "Endothelium stops expressing all adhesion molecules"], 0, "Loss of plasma fluid increases blood viscosity, producing slower flow and leukocyte margination."),
            item("moderate", "What is the role of lymphatic vessels during acute inflammation?", ["Drain extravascular fluid, proteins, and leukocytes from the site", "Produce all neutrophils in the lesion", "Prevent any antigen from reaching lymph nodes", "Convert edema into collagen directly"], 0, "Lymphatics help clear edema and inflammatory cells; inflamed lymphatics or nodes may cause lymphangitis or lymphadenitis."),
            item("very high", "A severe burn directly damages endothelium, causing leakage that persists until repair occurs. This is best explained by:", ["Direct endothelial injury", "Only a transient histamine response", "Selective loss of oncotic pressure without injury", "Pure neurogenic vasospasm"], 0, "Endothelial necrosis or detachment causes sustained leakage because the vascular barrier is physically disrupted."),
            item("very high", "VEGF promotes inflammation-associated edema primarily by:", ["Increasing vascular permeability and endothelial responses", "Inhibiting endothelial gaps completely", "Destroying neutrophil granules", "Blocking angiogenesis"], 0, "VEGF is a potent inducer of vascular permeability and also supports new vessel growth during repair."),
            item("very high", "Which plasma protein entering an inflamed site can form a fibrinous mesh when vascular permeability is high?", ["Fibrinogen", "Albumin only", "Hemoglobin", "Keratin"], 0, "Leaked fibrinogen can be converted to fibrin, especially in severe vascular injury or leakage."),
        ],
    ),
    (
        "leukocytes",
        "Leukocyte Recruitment and Activation",
        [
            item("easy", "What is the correct sequence of leukocyte recruitment in acute inflammation?", ["Rolling, firm adhesion, transmigration, chemotaxis", "Chemotaxis, phagocytosis, rolling, vasoconstriction", "Transmigration, necrosis, rolling, fibrosis", "Scar formation, rolling, antigen presentation, apoptosis"], 0, "Leukocytes first roll, then adhere firmly, pass through endothelium, and migrate toward chemoattractants."),
            item("easy", "Leukocyte rolling on endothelium is mediated mainly by:", ["Selectins", "Collagenases", "Immunoglobulin light chains", "Mitochondrial ribosomes"], 0, "Selectins mediate weak, transient leukocyte-endothelial interactions that produce rolling."),
            item("easy", "Firm adhesion of leukocytes to endothelium depends mainly on leukocyte:", ["Integrins binding endothelial ICAM-1 and VCAM-1", "Hemoglobin binding oxygen", "Keratin binding desmosomes", "Elastin binding calcium"], 0, "Activated leukocyte integrins bind endothelial adhesion molecules to arrest rolling cells."),
            item("moderate", "TNF and IL-1 promote leukocyte recruitment chiefly by:", ["Increasing endothelial adhesion molecule expression", "Blocking chemokine production", "Destroying neutrophil nuclei", "Inhibiting all vascular leakage"], 0, "TNF and IL-1 activate endothelium, increasing molecules such as E-selectin, ICAM-1, and VCAM-1."),
            item("moderate", "Chemokines displayed on endothelial surfaces help leukocytes by:", ["Activating integrins to a high-affinity state", "Digesting bacterial cell walls directly", "Forming fibrin clots", "Suppressing all leukocyte movement"], 0, "Chemokines bind leukocyte receptors and convert integrins into strong adhesion molecules."),
            item("moderate", "Which molecule is especially associated with leukocyte transmigration through endothelial junctions?", ["PECAM-1/CD31", "Hemoglobin A", "Surfactant protein B only", "Type II collagen"], 0, "PECAM-1, also called CD31, participates in diapedesis across endothelial junctions."),
            item("moderate", "Which group contains important chemoattractants for neutrophils?", ["Bacterial products, C5a, LTB4, and IL-8", "Albumin, bilirubin, insulin, and thyroxine", "Keratin, melanin, elastin, and collagen", "Fibrinogen, prothrombin, factor X, and plasminogen only"], 0, "Microbial products, complement C5a, leukotriene B4, and chemokines such as IL-8 guide leukocyte migration."),
            item("very high", "Neutrophils usually predominate during the first 6 to 24 hours of acute inflammation because they:", ["Are more numerous in blood and respond rapidly to chemokines", "Are the only leukocytes with nuclei", "Cannot undergo apoptosis", "Are produced only inside lymph nodes"], 0, "Neutrophils are abundant and rapidly recruited; monocytes usually become more prominent later."),
            item("very high", "A child has recurrent bacterial infections and absent neutrophil accumulation at infection sites due to defective beta-2 integrins. Which step is most impaired?", ["Firm leukocyte adhesion", "Histamine storage in mast cells", "Complement protein synthesis", "Fibrin degradation"], 0, "Beta-2 integrins are needed for firm adhesion to endothelial ICAM molecules; defects cause leukocyte adhesion deficiency."),
            item("very high", "After crossing endothelium, leukocytes move through tissue toward the inflammatory focus by:", ["Actin-dependent migration along chemoattractant gradients", "Passive diffusion without receptors", "Red cell-mediated transport", "Fibroblast contraction only"], 0, "Chemoattractants activate leukocyte receptors, cytoskeletal rearrangement, and directional movement."),
        ],
    ),
    (
        "killing",
        "Phagocytosis, Microbial Killing, and Leukocyte-Mediated Injury",
        [
            item("easy", "What are the major steps of phagocytosis?", ["Recognition and attachment, engulfment, then killing/degradation", "Vasodilation, stasis, fibrosis, then calcification", "Rolling, fever, collagen synthesis, then scarring", "Apoptosis, metaplasia, dysplasia, then necrosis"], 0, "Phagocytosis proceeds from recognition of particles to phagosome formation and intracellular killing/degradation."),
            item("easy", "Which is an important opsonin that enhances phagocytosis?", ["IgG", "Albumin", "Creatinine", "Glucose"], 0, "IgG Fc regions bind phagocyte Fc receptors, promoting ingestion of coated microbes."),
            item("easy", "Fusion of a phagosome with lysosomal granules forms a:", ["Phagolysosome", "Desmosome", "Ribosome", "Nucleosome"], 0, "The phagolysosome brings ingested material together with antimicrobial enzymes and reactive molecules."),
            item("moderate", "The respiratory burst in neutrophils depends on activation of:", ["NADPH oxidase", "DNA polymerase", "Acetylcholinesterase", "Cyclin B"], 0, "NADPH oxidase generates superoxide, initiating reactive oxygen species production."),
            item("moderate", "Myeloperoxidase kills microbes by converting hydrogen peroxide and halide into:", ["Hypochlorous acid", "Nitric oxide synthase", "Leukotriene B4", "Type I collagen"], 0, "The MPO-halide system produces hypochlorous acid, a powerful antimicrobial oxidant."),
            item("moderate", "Chronic granulomatous disease most often reflects defective:", ["NADPH oxidase-dependent ROS generation", "Histamine storage in mast cells", "Prostaglandin synthesis in platelets", "Collagen cross-linking by vitamin C"], 0, "CGD impairs the oxidative burst, leading to recurrent infections with catalase-positive organisms."),
            item("moderate", "Nitric oxide participates in acute inflammation primarily by:", ["Killing microbes and modulating vascular tone", "Synthesizing collagen fibers", "Opsonizing bacteria as C3b", "Serving as the main neutrophil adhesion molecule"], 0, "NO made by endothelial cells and macrophages contributes to vasodilation and microbial killing."),
            item("very high", "Extracellular release of leukocyte lysosomal enzymes and ROS is clinically important because it:", ["Can injure host tissues during inflammation", "Always prevents tissue necrosis", "Stops all complement activation", "Converts neutrophils into fibroblasts"], 0, "Leukocyte products can spill into extracellular tissue and cause collateral damage."),
            item("very high", "Neutrophil extracellular traps are composed mainly of:", ["Chromatin studded with antimicrobial granule proteins", "Pure collagen and elastin", "Fibrinogen and platelets only", "Calcium phosphate crystals"], 0, "NETs are nuclear chromatin networks decorated with granule proteins that trap microbes but may also promote injury."),
            item("very high", "Myeloperoxidase deficiency is often less severe than CGD because neutrophils can still:", ["Kill microbes through MPO-independent mechanisms", "Avoid all phagocytosis", "Generate no reactive oxygen species", "Replace macrophages in granulomas permanently"], 0, "MPO deficiency reduces HOCl generation, but other ROS and lysosomal mechanisms often compensate."),
        ],
    ),
    (
        "mediators",
        "Chemical Mediators of Inflammation",
        [
            item("easy", "Chemical mediators of inflammation may be derived from:", ["Plasma proteins or cells", "Only red blood cells", "Only bone matrix", "Only dietary carbohydrates"], 0, "Mediators are produced by cells or generated from circulating plasma proteins."),
            item("easy", "Histamine released from mast cells causes:", ["Vasodilation and increased vascular permeability", "Collagen maturation only", "Permanent macrophage fusion", "Complement inhibition"], 0, "Histamine is a major early mediator of arteriolar dilation and venular leakage."),
            item("easy", "Prostaglandins are especially associated with:", ["Vasodilation, pain, and fever", "Neutrophil rolling by selectins", "Formation of granuloma giant cells", "Opsonization as C3b"], 0, "Several prostaglandins mediate vasodilation; PGE2 contributes to pain and fever."),
            item("moderate", "Which arachidonic acid metabolite is a powerful neutrophil chemoattractant?", ["Leukotriene B4", "Thromboxane A2", "Prostacyclin", "Lipoxin A4"], 0, "LTB4 promotes leukocyte adhesion, chemotaxis, and activation."),
            item("moderate", "LTC4, LTD4, and LTE4 mainly promote:", ["Vascular permeability and bronchospasm", "Macrophage epithelioid transformation only", "Collagen degradation by MMPs only", "Fever through hypothalamic PGE2 only"], 0, "The cysteinyl leukotrienes increase vascular leakage and cause bronchoconstriction."),
            item("moderate", "Lipoxins contribute to resolution of inflammation by:", ["Inhibiting neutrophil recruitment and adhesion", "Increasing neutrophil oxidative burst indefinitely", "Converting fibrin into pus", "Stimulating all macrophages to become M1 only"], 0, "Lipoxins are anti-inflammatory lipid mediators that limit further neutrophil recruitment."),
            item("moderate", "The major local actions of TNF and IL-1 include:", ["Endothelial activation and leukocyte recruitment", "Direct synthesis of hemoglobin", "Permanent inhibition of fever", "Conversion of plasma cells into neutrophils"], 0, "TNF and IL-1 activate endothelium and promote cytokine/chemokine cascades; systemically, they also contribute to fever."),
            item("very high", "Which complement fragment is both a potent chemoattractant and an anaphylatoxin?", ["C5a", "C3b", "C5b", "Factor H"], 0, "C5a recruits and activates leukocytes and also increases vascular permeability through mast cell activation."),
            item("very high", "Which complement component is the major opsonin generated during complement activation?", ["C3b", "C1 inhibitor", "C5b-9", "C4-binding protein"], 0, "C3b coats microbes and promotes phagocytosis through complement receptors."),
            item("very high", "Hereditary angioedema is caused by deficiency of:", ["C1 inhibitor", "Myeloperoxidase", "PECAM-1", "E-selectin"], 0, "C1 inhibitor normally restrains complement and kallikrein-kinin activation; deficiency causes episodic bradykinin-mediated edema."),
        ],
    ),
    (
        "patterns",
        "Morphologic Patterns and Outcomes of Acute Inflammation",
        [
            item("easy", "Serous inflammation is characterized by:", ["Thin, watery, protein-poor fluid", "Thick pus with liquefactive necrosis only", "Dense collagen scar without edema", "Caseating granulomas"], 0, "Serous inflammation produces watery effusions or blisters derived from plasma or mesothelial secretions."),
            item("easy", "Fibrinous inflammation most often indicates:", ["More severe vascular leakage with fibrinogen escape", "Only a noninflammatory transudate", "A purely viral lymphocytosis", "Normal wound contraction"], 0, "When vascular permeability is high, fibrinogen leaks out and is converted to fibrin."),
            item("easy", "Purulent or suppurative inflammation is characterized by:", ["Pus rich in neutrophils and liquefactive debris", "Only clear serous fluid", "Only collagen deposition", "Only noncaseating granulomas"], 0, "Suppurative inflammation contains neutrophils, necrotic debris, and edema fluid."),
            item("moderate", "An abscess is best described as:", ["A localized collection of pus in tissue", "A platelet-rich arterial thrombus", "A healed linear scar", "A sterile transudate in a serous cavity"], 0, "Abscesses are focal suppurative lesions with central liquefactive necrosis and many neutrophils."),
            item("moderate", "An ulcer is:", ["A local defect of an epithelial surface produced by shedding necrotic inflamed tissue", "A granuloma made entirely of macrophages", "A vascular dilation without tissue loss", "A normal lymph node reaction"], 0, "Ulcers occur on skin or mucosal surfaces when necrotic inflammatory tissue is lost."),
            item("moderate", "Complete resolution of acute inflammation is most likely when:", ["Injury is limited, short-lived, and tissue can regenerate", "There is extensive stromal destruction", "A persistent microbe remains", "Large amounts of fibrin cannot be cleared"], 0, "Resolution requires removal of mediators/debris and preservation of regenerative capacity and tissue framework."),
            item("moderate", "Organization and scarring are favored when:", ["There is substantial tissue destruction or abundant fibrinous exudate", "The injury is tiny and the matrix is intact", "All macrophages are absent", "The tissue has no vascular leakage"], 0, "If exudate or necrotic tissue cannot be cleared, granulation tissue grows into it and collagen scar forms."),
            item("very high", "Progression from acute to chronic inflammation is most likely when:", ["The injurious agent persists or normal healing is interfered with", "The exudate is immediately cleared", "Neutrophils undergo prompt apoptosis and macrophages clear debris", "The basement membrane is intact and injury is trivial"], 0, "Persistent infection, foreign material, autoimmune injury, or delayed clearance can convert acute inflammation into chronic inflammation."),
            item("very high", "A fibrinous pericarditis can either resolve or become organized. Organization means:", ["Ingrowth of fibroblasts and vessels followed by scar formation", "Immediate conversion of fibrin into normal mesothelium", "Loss of all inflammatory cells without repair", "Transformation of fibrin into red blood cells"], 0, "Organization is replacement of fibrinous exudate by granulation tissue and eventually fibrous scar."),
            item("very high", "The three core events in acute inflammation are best summarized as:", ["Vascular changes, leukocyte recruitment/activation, and mediator action", "Metaplasia, dysplasia, and carcinoma", "Atrophy, hypertrophy, and hyperplasia only", "Calcification, pigmentation, and aging"], 0, "Acute inflammation is driven by vascular responses, leukocyte movement and activation, and chemical mediators."),
        ],
    ),
    (
        "chronic",
        "Chronic Inflammation, Macrophages, and Granulomas",
        [
            item("easy", "Chronic inflammation is characterized by:", ["Mononuclear infiltrates, tissue destruction, and attempts at repair", "Only neutrophils for a few minutes", "Only edema without cells", "Only thrombosis without cytokines"], 0, "Macrophages, lymphocytes, plasma cells, tissue injury, angiogenesis, and fibrosis are typical of chronic inflammation."),
            item("easy", "Which is a common cause of chronic inflammation?", ["Persistent infection", "Brief histamine release after a mosquito bite only", "Normal epithelial turnover", "Physiologic vasodilation during exercise"], 0, "Persistent microbes, immune-mediated diseases, and prolonged toxic exposures commonly drive chronic inflammation."),
            item("easy", "The dominant effector cell in many chronic inflammatory lesions is the:", ["Macrophage", "Erythrocyte", "Platelet", "Adipocyte"], 0, "Macrophages ingest debris, secrete cytokines, damage tissue, and promote repair/fibrosis."),
            item("moderate", "Classically activated M1 macrophages are induced mainly by:", ["Microbial products and IFN-gamma", "IL-4 and IL-13 only", "Albumin and fibrinogen", "Estrogen and progesterone"], 0, "M1 activation is promoted by TLR ligands and IFN-gamma and supports microbicidal and pro-inflammatory functions."),
            item("moderate", "Alternatively activated M2 macrophages are most associated with:", ["Tissue repair and fibrosis", "Respiratory burst as their only function", "Immediate neutrophil rolling", "Complement membrane attack complex formation"], 0, "M2 macrophages, driven by IL-4/IL-13, dampen inflammation and promote repair, collagen deposition, and fibrosis."),
            item("moderate", "Th1 lymphocytes promote macrophage activation mainly by secreting:", ["IFN-gamma", "IL-4", "IL-5", "Eotaxin"], 0, "Th1-derived IFN-gamma is a major activator of classical macrophage functions."),
            item("moderate", "Th17 cells contribute to inflammation mainly by:", ["Recruiting neutrophils and monocytes through IL-17-driven mediators", "Making only IgE", "Forming collagen cross-links", "Producing hypochlorous acid"], 0, "IL-17 induces chemokines and other mediators that recruit neutrophils and monocytes."),
            item("very high", "A granuloma is best defined as:", ["An aggregate of activated macrophages, often with lymphocytes and giant cells", "A collection of serum without cells", "A platelet plug in a vessel", "A zone of pure collagen without inflammation"], 0, "Granulomas are collections of epithelioid macrophages formed in certain persistent inflammatory settings."),
            item("very high", "Caseating granulomas are classically associated with:", ["Tuberculosis", "Simple edema", "Uncomplicated serous blister", "Physiologic wound contraction"], 0, "Tuberculosis often produces granulomas with central caseous necrosis."),
            item("very high", "Foreign body granulomas form when:", ["Inert material too large to phagocytose persists in tissue", "Every acute inflammatory mediator is cleared immediately", "Only mast cell histamine acts on venules", "The liver regenerates after partial hepatectomy"], 0, "Sutures, talc, or other indigestible material can provoke macrophage fusion and foreign body giant cells."),
        ],
    ),
    (
        "systemic",
        "Systemic Effects of Inflammation",
        [
            item("easy", "The acute-phase response is driven mainly by which cytokines?", ["TNF, IL-1, and IL-6", "Insulin, glucagon, and thyroxine", "Histamine, serotonin, and dopamine only", "Erythropoietin and thrombopoietin only"], 0, "TNF, IL-1, and especially IL-6 mediate many systemic responses to inflammation."),
            item("easy", "Fever in inflammation occurs because cytokines induce hypothalamic production of:", ["Prostaglandin E2", "C3b", "Leukotriene B4", "Collagenase"], 0, "IL-1 and TNF stimulate prostaglandin production in the hypothalamus, raising the temperature set point."),
            item("easy", "Which set contains important acute-phase proteins?", ["C-reactive protein, fibrinogen, and serum amyloid A", "Keratin, elastin, and melanin", "Hemoglobin, myoglobin, and troponin", "Insulin, glucagon, and somatostatin"], 0, "The liver increases synthesis of CRP, fibrinogen, and SAA during systemic inflammation."),
            item("moderate", "In many bacterial infections, leukocytosis is dominated by:", ["Neutrophilia", "Eosinophilia only", "Basophilia only", "Reticulocytosis"], 0, "Bacterial infections commonly cause increased circulating neutrophils."),
            item("moderate", "A left shift in acute inflammation means increased circulating:", ["Immature neutrophils such as band forms", "Atypical epithelial cells", "Old erythrocytes", "Fibroblasts"], 0, "Accelerated marrow release during inflammation increases immature granulocyte forms in blood."),
            item("moderate", "Fibrinogen increases the erythrocyte sedimentation rate by promoting:", ["Rouleaux formation", "Red cell lysis", "Platelet degranulation", "Neutrophil apoptosis"], 0, "Fibrinogen coats red cells, making them stack and sediment faster."),
            item("moderate", "CRP and serum amyloid A can help host defense by:", ["Binding microbes and acting as opsonins or complement activators", "Making hypochlorous acid directly", "Synthesizing type I collagen", "Blocking all macrophage activity"], 0, "CRP and SAA bind microbial components and damaged cells, enhancing clearance."),
            item("very high", "High, sustained TNF production in chronic inflammation contributes to:", ["Cachexia", "Physiologic muscle hypertrophy", "Complete absence of fever", "Inhibition of all acute-phase proteins"], 0, "TNF suppresses appetite and alters metabolism, contributing to wasting/cachexia."),
            item("very high", "Septic shock reflects excessive systemic inflammatory mediator release causing:", ["Hypotension, disseminated coagulation, and metabolic abnormalities", "Only a small local blister", "Pure collagen scar without vascular effects", "Isolated eosinophilia without organ dysfunction"], 0, "Systemic cytokine excess in sepsis can cause vasodilation, vascular leakage, DIC, and multiorgan failure."),
            item("very high", "A leukemoid reaction is best described as:", ["Extreme reactive leukocytosis that can mimic leukemia", "A malignant plasma cell neoplasm", "Pure lymph node fibrosis", "Normal neutrophil count after inflammation"], 0, "Severe infections can produce very high leukocyte counts, sometimes 40,000 to 100,000 per microliter, mimicking leukemia."),
        ],
    ),
    (
        "repair",
        "Tissue Regeneration and Scar Formation",
        [
            item("easy", "Tissue repair occurs by which two broad processes?", ["Regeneration and connective tissue deposition", "Thrombosis and embolism only", "Metaplasia and dysplasia only", "Necrosis and calcification only"], 0, "Repair restores tissue by regenerating cells and/or forming scar through connective tissue deposition."),
            item("easy", "Labile cells are cells that:", ["Continuously divide throughout life", "Never divide after birth", "Only divide after partial hepatectomy", "Are permanently calcified"], 0, "Labile tissues, such as epithelia and hematopoietic cells, have continuous cell turnover."),
            item("easy", "Permanent cells are best exemplified by:", ["Neurons and cardiac myocytes", "Intestinal epithelium", "Bone marrow precursors", "Skin basal cells"], 0, "Permanent cells have little or no proliferative ability, so injury usually heals by scar."),
            item("moderate", "Why is an intact extracellular matrix important for regeneration?", ["It preserves the scaffold needed for orderly cell growth", "It blocks all growth factor signaling", "It converts all cells into fibroblasts", "It prevents angiogenesis entirely"], 0, "Regeneration needs an intact stromal framework; ECM destruction favors scarring."),
            item("moderate", "Liver regeneration after partial hepatectomy is mainly achieved by:", ["Proliferation of remaining hepatocytes and nonparenchymal cells", "Permanent replacement by bone", "Only neutrophil accumulation", "Complete absence of growth factors"], 0, "The liver can restore mass through cytokine priming and growth factor-driven proliferation of residual cells."),
            item("moderate", "Granulation tissue is composed mainly of:", ["New vessels, proliferating fibroblasts, and loose extracellular matrix", "Only mature dense collagen without vessels", "Only neutrophils in pus", "Only calcified debris"], 0, "Granulation tissue is a vascular, fibroblast-rich provisional repair tissue."),
            item("moderate", "Which growth factor is most important in angiogenesis during repair?", ["VEGF", "Erythropoietin", "Thyroxine", "Calcitonin"], 0, "VEGF stimulates endothelial migration, proliferation, and new vessel formation."),
            item("very high", "The most important fibrogenic cytokine in scar formation is:", ["TGF-beta", "IL-8", "C5a", "Histamine"], 0, "TGF-beta increases collagen synthesis, decreases collagen degradation, and promotes fibroblast activity."),
            item("very high", "Matrix metalloproteinases in healing wounds are important because they:", ["Remodel extracellular matrix and are balanced by TIMPs", "Serve as the main opsonins for bacteria", "Generate fever in the hypothalamus", "Cause leukocyte rolling"], 0, "MMPs degrade matrix components during remodeling, while tissue inhibitors of metalloproteinases limit their activity."),
            item("very high", "During scar maturation, early type III collagen is gradually replaced mainly by:", ["Type I collagen", "Type II collagen", "Type IV collagen only", "Elastin only"], 0, "Healing scars become stronger as type I collagen replaces the initially deposited type III collagen."),
        ],
    ),
    (
        "wound",
        "Cutaneous Wound Healing and Pathologic Repair",
        [
            item("easy", "Healing by first intention occurs in:", ["A clean, sutured surgical incision with minimal tissue loss", "A large infected ulcer with extensive tissue loss", "A burn wound healing entirely by contraction", "A chronic pressure sore"], 0, "Primary union is typical of clean incised wounds with closely apposed edges."),
            item("easy", "Healing by second intention is characterized by:", ["Larger tissue defects with more inflammation, granulation tissue, and contraction", "No granulation tissue formation", "No collagen deposition", "Instant restoration of normal tissue strength"], 0, "Secondary union occurs when wounds have substantial tissue loss or separated edges."),
            item("easy", "Wound contraction is mediated mainly by:", ["Myofibroblasts", "Erythrocytes", "Neurons", "Plasma proteins only"], 0, "Myofibroblasts have contractile features that pull wound edges together."),
            item("moderate", "The most important local cause of delayed wound healing is:", ["Infection", "Mild redness during normal healing", "Temporary scab formation", "Normal macrophage clearance"], 0, "Infection prolongs inflammation and increases local tissue injury, strongly delaying repair."),
            item("moderate", "Which systemic factor impairs wound healing?", ["Diabetes mellitus", "Normal vitamin C intake", "Adequate protein nutrition", "Good tissue perfusion"], 0, "Diabetes impairs perfusion, leukocyte function, and matrix production, delaying repair."),
            item("moderate", "Tensile strength of a skin wound after healing usually reaches:", ["About 70% to 80% of normal skin at maximum", "100% of normal skin within 24 hours", "More than 200% of normal skin", "Zero permanently"], 0, "Wound strength rises over months but generally plateaus below normal unwounded skin strength."),
            item("moderate", "A keloid differs from a hypertrophic scar because a keloid:", ["Extends beyond the boundaries of the original wound", "Contains no collagen", "Is always an abscess", "Occurs only inside arteries"], 0, "Keloids are exuberant scars that grow beyond the original wound margins; hypertrophic scars remain confined."),
            item("very high", "Wound dehiscence is especially likely after abdominal surgery when poor healing combines with:", ["Increased mechanical stress such as coughing or vomiting", "Immediate complete collagen maturation", "Absence of any wound tension", "Excess CRP alone"], 0, "Mechanical stress on a weak healing wound can cause the wound edges to separate."),
            item("very high", "Contractures are pathologic because they:", ["Cause deformity by excessive wound contraction", "Represent normal complete regeneration", "Are composed only of pus", "Always resolve without functional effect"], 0, "Excessive contraction can limit movement and deform tissues, especially after burns or wounds over joints."),
            item("very high", "Fibrosis in parenchymal organs most often follows:", ["Chronic inflammation with persistent injury and repair signaling", "A single trivial injury with intact matrix and rapid resolution", "Pure transudate formation", "Normal physiologic cell turnover only"], 0, "Persistent injury activates macrophages and fibroblasts, causing excessive extracellular matrix deposition and organ fibrosis."),
        ],
    ),
]


def build_questions():
    questions = []
    seen_ids = set()
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions, expected 10")
        for number, data in enumerate(items, start=1):
            qid = f"robbins-ch3-{slug}-{number}"
            if qid in seen_ids:
                raise ValueError(f"Duplicate generated id: {qid}")
            seen_ids.add(qid)
            q = {
                **BASE,
                "id": qid,
                "topic": topic,
                **data,
            }
            jumble_answer_position(q, (topic_index + number - 1) % 4)
            questions.append(q)
    return questions


def validate(questions, all_questions=None):
    if len(questions) != 100:
        raise ValueError(f"Expected 100 Chapter 3 questions, got {len(questions)}")
    topic_counts = Counter(q["topic"] for q in questions)
    if set(topic_counts.values()) != {10} or len(topic_counts) != 10:
        raise ValueError(f"Bad topic distribution: {topic_counts}")
    for topic in topic_counts:
        difficulty_counts = Counter(q["difficulty"] for q in questions if q["topic"] == topic)
        expected = Counter({"easy": 3, "moderate": 4, "very high": 3})
        if difficulty_counts != expected:
            raise ValueError(f"Bad difficulty distribution for {topic}: {difficulty_counts}")
    for q in questions:
        options = q["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"Bad options for {q['id']}")
        if not 0 <= q["answerIndex"] < 4:
            raise ValueError(f"Bad answer index for {q['id']}")
        if q["answer"] != options[q["answerIndex"]]:
            raise ValueError(f"Answer mismatch for {q['id']}")
    if all_questions is not None:
        ids = [q.get("id") for q in all_questions]
        dupes = [qid for qid, count in Counter(ids).items() if count > 1]
        if dupes:
            raise ValueError(f"Duplicate ids in full question bank: {dupes[:10]}")


def main():
    questions = build_questions()
    validate(questions)

    data = json.loads(DATA_PATH.read_text(encoding="utf-8-sig"))
    existing = data.get("questions", [])
    kept = [
        q
        for q in existing
        if not (
            q.get("chapterTitle") == BASE["chapterTitle"]
            or str(q.get("id", "")).startswith("robbins-ch3-")
        )
    ]
    data["questions"] = kept + questions
    validate(questions, data["questions"])
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Removed {len(existing) - len(kept)} existing Chapter 3 questions")
    print(f"Added {len(questions)} Robbins Chapter 3 questions")
    for topic, count in Counter(q["topic"] for q in questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
