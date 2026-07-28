import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path("runtime-data/users.json")
CHAPTER = "Neoplasia"

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
    ("nomenclature", "Nomenclature and Tumor Components", [
        q("easy", "A neoplasm is best defined as:", "A clonal genetic disorder of cell growth with autonomous proliferation", ["A physiologic enlargement due only to increased workload", "A reversible replacement of one mature cell type by another", "A collection of neutrophils and necrotic debris"], "Modern pathology defines neoplasia as abnormal clonal growth driven by genetic or epigenetic alterations."),
        q("easy", "The tumor parenchyma is composed of:", "Neoplastic cells", ["Reactive stroma only", "Edema fluid", "Fibrin thrombi"], "Parenchyma refers to the transformed cells that determine tumor behavior and nomenclature."),
        q("easy", "The supportive non-neoplastic tissue of a tumor is called:", "Stroma", ["Anaplasia", "Metastasis", "Dysplasia"], "Stroma includes connective tissue, blood vessels, and inflammatory cells that support tumor growth."),
        q("moderate", "A benign tumor of fibrous tissue is called a:", "Fibroma", ["Fibrosarcoma", "Adenocarcinoma", "Melanoma"], "Benign mesenchymal tumors often add -oma to the cell of origin."),
        q("moderate", "A malignant tumor arising from gland-forming epithelium is called:", "Adenocarcinoma", ["Adenoma", "Chondrosarcoma", "Leiomyoma"], "Malignant epithelial tumors are carcinomas; glandular differentiation makes them adenocarcinomas."),
        q("moderate", "A malignant tumor of mesenchymal origin is generally called a:", "Sarcoma", ["Papilloma", "Carcinoma in situ", "Hamartoma"], "Sarcomas arise from mesenchymal tissues such as muscle, bone, fat, and fibrous tissue."),
        q("moderate", "A teratoma contains:", "Mature or immature tissues derived from more than one germ layer", ["Only reactive scar tissue", "Only metastatic carcinoma in lymphatics", "Only misplaced normal tissue without neoplastic growth"], "Teratomas arise from totipotent germ cells and may show multiple tissue types."),
        q("high", "An ovarian mass contains hair, sebaceous material, cartilage, and neural tissue arranged in a haphazard but mature fashion. The pathologist explains that the tumor arose from a totipotent germ cell. Which term best fits this lesion?", "Mature teratoma", ["Papilloma", "Hamartoma", "Choristoma"], "Mature teratomas contain differentiated tissues from multiple germ layers, often in ovary."),
        q("high", "A lung nodule is made of disorganized but mature cartilage, bronchial epithelium, and connective tissue normally found in lung. Cytogenetic studies show a clonal abnormality, but the components are not foreign to the site. What is the best designation?", "Hamartoma", ["Choristoma", "Metastatic sarcoma", "Carcinoma in situ"], "Hamartomas are disorganized overgrowths of tissue native to the site and are often clonal benign lesions."),
        q("high", "A small, well-organized nodule of pancreatic tissue is found in the gastric submucosa during endoscopy. It is composed of normal pancreatic acini and ducts but is located in the wrong organ. Which term is most accurate?", "Choristoma", ["Hamartoma", "Adenocarcinoma", "Mixed tumor"], "A choristoma is a heterotopic rest of normal tissue in an abnormal location."),
    ]),
    ("benign-malignant", "Characteristics of Benign and Malignant Neoplasms", [
        q("easy", "The most reliable feature proving malignancy in a solid tumor is:", "Metastasis", ["Slow growth", "Encapsulation", "Well differentiation"], "Metastasis is unequivocal evidence of malignancy in solid tumors."),
        q("easy", "Differentiation refers to:", "Resemblance of tumor cells to normal cells of origin", ["Ability to enter lymphatics only", "Tumor blood supply", "Amount of necrosis only"], "Differentiation measures morphologic and functional similarity to normal tissue."),
        q("easy", "Anaplasia means:", "Lack of differentiation", ["Benign encapsulation", "Formation of glands", "Replacement by scar"], "Anaplasia is a hallmark of many malignant tumors."),
        q("moderate", "Carcinoma in situ means malignant epithelial cells:", "Involve full epithelial thickness without basement membrane invasion", ["Have metastasized to lymph nodes", "Are benign and encapsulated", "Have invaded blood vessels only"], "In situ carcinoma shows cytologic malignancy but remains above the basement membrane."),
        q("moderate", "Dysplasia is most often recognized by:", "Disordered epithelial growth with pleomorphism and architectural loss", ["Orderly maturation with tiny uniform nuclei", "Pure stromal edema", "Only increased collagen"], "Dysplasia is premalignant epithelial disordered growth."),
        q("moderate", "Benign tumors usually grow by:", "Expansion with a well-demarcated border", ["Diffuse infiltration of all adjacent structures", "Early hematogenous spread", "Obligate lymphatic invasion"], "Benign tumors often push aside adjacent tissue rather than invade it."),
        q("moderate", "Which feature favors malignancy over benignity?", "Tumor giant cells with abnormal mitoses", ["Uniform mature cells", "Thin capsule", "Slow expansile growth"], "Marked pleomorphism and atypical mitoses suggest anaplasia and malignancy."),
        q("high", "A cervical biopsy shows full-thickness epithelial atypia, loss of maturation, hyperchromatic nuclei, and mitoses above the basal layer. The basement membrane is intact, and no stromal invasion is identified. Which diagnosis best matches these findings?", "Carcinoma in situ", ["Invasive squamous cell carcinoma", "Squamous metaplasia", "Benign papilloma"], "Full-thickness dysplasia without basement membrane invasion is carcinoma in situ."),
        q("high", "A smoker’s bronchial biopsy shows replacement of ciliated columnar epithelium by squamous epithelium. A later biopsy shows pleomorphic basal-like cells and abnormal mitoses, but no invasion. Which sequence best describes the progression?", "Metaplasia to dysplasia to carcinoma in situ", ["Anaplasia to hamartoma to choristoma", "Necrosis to granuloma to sarcoma", "Hyperemia to edema to infarction"], "Chronic injury can cause metaplasia, then dysplasia, then preinvasive carcinoma."),
        q("high", "A large uterine smooth muscle tumor has infiltrative edges, hemorrhage, necrosis, numerous atypical mitoses, and pleomorphic cells. A small well-circumscribed smooth muscle mass elsewhere in the uterus lacks these findings. Which feature most supports leiomyosarcoma?", "Invasion with cytologic atypia and abnormal mitotic activity", ["Presence of smooth muscle differentiation", "Location in myometrium", "Estrogen responsiveness"], "Malignant smooth muscle tumors show infiltrative growth, atypia, necrosis, and mitoses."),
    ]),
    ("epidemiology", "Epidemiology and Predisposing Conditions", [
        q("easy", "The strongest environmental cause of cancer deaths worldwide is:", "Tobacco use", ["Low dietary salt", "Exercise", "Vaccination"], "Tobacco is linked to cancers of lung, upper aerodigestive tract, pancreas, bladder, and others."),
        q("easy", "Most carcinomas occur in adults older than:", "55 years", ["5 years", "15 years", "25 years"], "Cancer incidence generally rises with age due to accumulated mutations."),
        q("easy", "Obesity increases risk of several cancers partly through:", "Metabolic and hormonal effects", ["Complete prevention of inflammation", "Loss of all estrogen", "Universal DNA repair enhancement"], "Obesity is associated with increased mortality from several cancers."),
        q("moderate", "Alcohol and tobacco together increase risk of cancer of the:", "Oropharynx and esophagus", ["Thyroid medulla only", "Retina only", "Bone marrow only"], "Alcohol synergizes with tobacco for upper aerodigestive tract cancers."),
        q("moderate", "Unopposed estrogen exposure increases risk of:", "Endometrial carcinoma", ["Osteosarcoma", "Basal cell carcinoma", "Glioblastoma"], "Prolonged estrogen stimulation promotes endometrial proliferation and cancer risk."),
        q("moderate", "Chronic inflammation predisposes to cancer partly by:", "Increasing regenerative proliferation and DNA damage", ["Suppressing all cytokines", "Eliminating reactive oxygen species", "Stopping cell division"], "Chronic injury and repair create a mutation-promoting environment."),
        q("moderate", "Ultraviolet radiation is most strongly linked to cancers of the:", "Skin", ["Colon", "Liver only", "Prostate only"], "UV light causes DNA damage in epidermal cells, contributing to skin cancers."),
        q("high", "A patient with long-standing ulcerative colitis develops multifocal epithelial dysplasia and later colon carcinoma. The cancer arises in a background of chronic mucosal injury, regeneration, and inflammatory mediator production. Which acquired predisposing condition is most relevant?", "Chronic inflammation", ["Benign encapsulation", "Balanced translocation", "Pure hormonal withdrawal"], "Chronic inflammatory disorders increase cancer risk by promoting cycles of damage and repair."),
        q("high", "Two populations have markedly different rates of colon, prostate, and breast cancer, but migrants gradually acquire the risk profile of the host country. This observation most strongly supports which influence on cancer incidence?", "Environmental and lifestyle factors", ["Fixed species-wide mutation rates only", "Only inherited germline mutations", "Only random mitotic nondisjunction"], "Geographic and migration patterns show major environmental contributions to common cancers."),
        q("high", "A 70-year-old develops carcinoma after decades of tobacco exposure. Sequencing shows many unrelated passenger mutations in addition to driver mutations. Which age-related concept best explains the increased cancer risk?", "Accumulation of somatic mutations over time", ["Immediate congenital aneuploidy", "Complete loss of immune responses at birth", "Maternal imprinting alone"], "Cancer risk rises with age as cells accumulate genetic and epigenetic alterations."),
    ]),
    ("hallmarks", "Molecular Basis and Hallmarks of Cancer", [
        q("easy", "Cancer is fundamentally caused by:", "Genetic and epigenetic alterations in a cell clone", ["Only acute inflammation", "Only edema", "Only physiologic hyperplasia"], "Neoplasms arise from heritable changes that confer growth and survival advantages."),
        q("easy", "Driver mutations are mutations that:", "Contribute directly to cancer development", ["Never affect cell behavior", "Only occur after death", "Always repair DNA"], "Drivers provide selective growth, survival, or invasion advantages."),
        q("easy", "Passenger mutations are:", "Incidental mutations not directly contributing to tumor behavior", ["Mutations required for metastasis", "Germline-only changes", "Normal antigen receptor rearrangements"], "Passenger mutations accumulate but do not drive cancer phenotype."),
        q("moderate", "A core hallmark of cancer is:", "Self-sufficiency in growth signals", ["Permanent dependence on normal growth control", "Inability to invade", "Obligate apoptosis"], "Cancer cells acquire autonomous growth signaling."),
        q("moderate", "Cancer cells evade growth suppression by altering:", "Tumor suppressor pathways", ["Only albumin synthesis", "Only complement activation", "Only platelet granules"], "Loss of RB, TP53, and related pathways removes brakes on proliferation."),
        q("moderate", "Cancer cells acquire limitless replicative potential largely through:", "Telomerase activation or telomere maintenance", ["Fibrin deposition", "Histamine release", "C3b opsonization"], "Telomere maintenance prevents senescence during repeated division."),
        q("moderate", "Angiogenesis helps tumors by:", "Supplying nutrients and oxygen for expanding tumor mass", ["Blocking all metastasis", "Inducing permanent dormancy", "Eliminating stroma"], "Tumors require new vessels beyond small diffusion-limited sizes."),
        q("high", "A tumor biopsy shows many mutations, but only a small subset repeatedly appears in independent samples and activates pathways controlling growth, survival, and invasion. The remaining mutations vary randomly between regions. Which term applies to the recurrent selected mutations?", "Driver mutations", ["Passenger mutations", "Silent polymorphisms", "Germline mosaicism"], "Driver mutations are selected because they contribute to malignant behavior."),
        q("high", "A cancer cell grows without exogenous growth factors, ignores antigrowth signals, resists apoptosis after DNA damage, induces blood vessels, and invades basement membrane. Which framework best integrates these diverse acquired properties?", "Hallmarks of cancer", ["Virchow triad", "Four signs of inflammation", "Mendelian inheritance"], "The hallmarks summarize acquired capabilities needed for malignant growth and spread."),
        q("high", "A small carcinoma remains clinically dormant until a clone emerges that secretes VEGF, degrades basement membrane, and survives in blood. The new clone expands because it has a selective advantage within the tumor. What process best explains this evolution?", "Clonal selection during tumor progression", ["Complete reversibility of dysplasia", "Physiologic hypertrophy", "Normal wound healing"], "Tumors evolve by selection of subclones with advantageous mutations."),
    ]),
    ("oncogenes", "Oncogenes and Growth-Promoting Pathways", [
        q("easy", "Proto-oncogenes normally promote:", "Cell growth and survival", ["DNA repair only", "Cell-cell adhesion only", "Complement activation"], "Proto-oncogenes encode regulated proteins involved in growth signaling."),
        q("easy", "An activated oncogene generally acts in a:", "Dominant gain-of-function manner", ["Recessive loss-of-function manner", "Mitochondrial inheritance pattern", "Purely epigenetic imprinting pattern"], "One activated allele can drive growth."),
        q("easy", "RAS is a:", "GTP-binding signal transduction protein", ["DNA mismatch repair enzyme", "Cell-cycle inhibitor", "Basement membrane collagen"], "RAS transmits growth signals downstream of receptor tyrosine kinases."),
        q("moderate", "A common mechanism of MYC activation in Burkitt lymphoma is:", "t(8;14) translocation near immunoglobulin heavy-chain locus", ["Deletion of both RB alleles", "Loss of E-cadherin", "Microsatellite instability"], "Burkitt lymphoma often places MYC under Ig heavy-chain enhancer control."),
        q("moderate", "BCR-ABL in chronic myeloid leukemia encodes:", "A constitutively active tyrosine kinase", ["A defective collagen chain", "An inactive complement protein", "A secreted IgE antibody"], "The Philadelphia chromosome creates a fusion tyrosine kinase."),
        q("moderate", "HER2 amplification in breast cancer leads to:", "Excess receptor tyrosine kinase signaling", ["Loss of mismatch repair", "Telomere shortening only", "E-cadherin restoration"], "HER2 amplification drives growth signaling and is targetable."),
        q("moderate", "Cyclin D overexpression promotes cancer by:", "Driving G1-to-S cell-cycle progression", ["Increasing basement membrane integrity", "Blocking all angiogenesis", "Inhibiting telomerase"], "Cyclin D activates CDK4/6, phosphorylating RB and promoting S phase entry."),
        q("high", "A lung adenocarcinoma carries an EGFR kinase-domain mutation. The receptor signals without normal ligand regulation, activating downstream RAS and PI3K pathways. Which therapeutic principle follows from this molecular abnormality?", "Use of targeted tyrosine kinase inhibition", ["Use of C1 inhibitor replacement", "Avoidance of all molecular testing", "Treatment with antihistamines only"], "Activated receptor tyrosine kinases may be blocked by specific kinase inhibitors."),
        q("high", "A leukemia cell contains t(9;22), producing a fusion protein that constitutively phosphorylates substrates and drives myeloid proliferation. The disease responds dramatically to imatinib. Which oncogenic mechanism is present?", "BCR-ABL fusion tyrosine kinase activation", ["RB pathway loss alone", "p53-mediated apoptosis", "APC germline deletion"], "CML is driven by the BCR-ABL fusion kinase, targetable by imatinib."),
        q("high", "A colon carcinoma has a KRAS mutation that locks RAS in its active GTP-bound state. Even if upstream EGFR is blocked, downstream signaling persists. Which concept explains resistance to anti-EGFR therapy?", "Constitutive downstream oncogene activation", ["Restored contact inhibition", "MHC class I loss", "Antibody-mediated anaphylaxis"], "Activating KRAS mutations bypass upstream receptor blockade."),
    ]),
    ("suppressors", "Tumor Suppressor Genes and Cell-Cycle Control", [
        q("easy", "Tumor suppressor genes usually require:", "Loss of both alleles for full inactivation", ["Activation of one allele only", "IgE class switching", "Mitochondrial inheritance"], "Most tumor suppressors follow the two-hit model."),
        q("easy", "RB normally controls transition from:", "G1 to S phase", ["M phase to cytokinesis only", "G2 to M through telomerase", "Apoptosis to necrosis"], "RB restrains E2F and prevents S phase entry when hypophosphorylated."),
        q("easy", "TP53 is often called the:", "Guardian of the genome", ["Master of IgE switching", "Warburg enzyme", "Basement membrane receptor"], "p53 responds to DNA damage by inducing arrest, repair, senescence, or apoptosis."),
        q("moderate", "The two-hit hypothesis was first illustrated by:", "Retinoblastoma", ["Burkitt lymphoma", "Hodgkin lymphoma", "Kaposi sarcoma"], "RB loss in hereditary and sporadic retinoblastoma illustrates two hits."),
        q("moderate", "APC mutation promotes colorectal carcinoma by activating:", "WNT/beta-catenin signaling", ["JAK/STAT only", "Complement cascade", "IgE receptor signaling"], "APC normally promotes beta-catenin degradation."),
        q("moderate", "Loss of E-cadherin is especially linked to:", "Diffuse gastric carcinoma and lobular breast carcinoma", ["CML", "Tay-Sachs disease", "Teratoma"], "CDH1 loss reduces epithelial adhesion and promotes diffuse infiltrative growth."),
        q("moderate", "TGF-beta signaling normally acts as:", "A growth-inhibitory pathway in many epithelial cells", ["A universal oncogenic kinase", "A platelet aggregation receptor", "An amyloid precursor"], "Loss of TGF-beta pathway components removes growth suppression."),
        q("high", "A child inherits one mutant RB allele and develops bilateral retinoblastomas after somatic loss of the remaining normal allele in retinal cells. Years later, osteosarcoma risk is also increased. Which model explains this pattern?", "Two-hit inactivation of a tumor suppressor gene", ["Dominant activation of a proto-oncogene", "Maternal mitochondrial inheritance", "IgE-mediated hypersensitivity"], "Inherited first hit plus somatic second hit produces early multiple tumors."),
        q("high", "A colon adenoma has APC loss, allowing beta-catenin to accumulate and enter the nucleus. The cell then transcribes growth-promoting genes despite absent WNT ligand. Which tumor suppressor pathway is disrupted?", "APC/beta-catenin pathway", ["BCR-ABL pathway", "PD-1 checkpoint pathway", "NADPH oxidase pathway"], "APC restrains WNT signaling by degrading beta-catenin."),
        q("high", "A tumor cell exposed to ionizing radiation fails to arrest the cell cycle, repair DNA, or undergo apoptosis. Sequencing shows biallelic TP53 loss. Which consequence best explains why this mutation accelerates cancer progression?", "Survival and replication of genetically damaged cells", ["Improved immune recognition", "Restored senescence", "Reduced mutation accumulation"], "Loss of p53 permits damaged cells to survive and accumulate additional mutations."),
    ]),
    ("genomic-instability", "DNA Repair Defects and Genomic Instability", [
        q("easy", "Defective DNA repair predisposes to cancer by causing:", "Genomic instability", ["Immediate tumor encapsulation", "Permanent apoptosis of all cells", "Loss of all mutations"], "Failure to repair DNA damage increases mutation rates."),
        q("easy", "Mismatch repair defects are associated with:", "Microsatellite instability", ["Apple-green birefringence", "IgE degranulation", "Telomerase absence only"], "Mismatch repair loss causes length changes in microsatellite repeats."),
        q("easy", "BRCA1 and BRCA2 participate in repair of:", "Double-strand DNA breaks by homologous recombination", ["IgE receptor signaling", "LDL uptake", "Collagen secretion"], "BRCA proteins help high-fidelity double-strand break repair."),
        q("moderate", "Lynch syndrome is caused by germline defects in:", "DNA mismatch repair genes", ["RB only", "FBN1", "LDLR"], "Inherited mismatch repair defects predispose to colon and endometrial cancers."),
        q("moderate", "Xeroderma pigmentosum results from defective:", "Nucleotide excision repair", ["Mismatch repair", "Base excision repair only", "Homologous recombination only"], "XP impairs repair of UV-induced pyrimidine dimers."),
        q("moderate", "Microsatellite instability is most useful as a marker of:", "Mismatch repair deficiency", ["RAS GTPase activity", "E-cadherin expression", "Angiogenesis"], "MSI reflects insertion/deletion errors at short repeats due to MMR loss."),
        q("moderate", "Cancers with high mutation burdens may be more responsive to immune checkpoint blockade because they:", "Generate more neoantigens", ["Have no antigens", "Cannot express MHC", "Never mutate p53"], "More mutations can create tumor-specific peptides recognized by T cells."),
        q("high", "A young patient develops colon cancer, and tumor testing shows loss of MLH1/MSH2 function with length variation in multiple microsatellite markers. The tumor has numerous frameshift mutations in growth-regulatory genes. Which inherited syndrome is most likely?", "Lynch syndrome", ["Familial adenomatous polyposis", "Li-Fraumeni syndrome", "Multiple endocrine neoplasia type 2"], "Lynch syndrome is caused by germline mismatch repair defects and MSI."),
        q("high", "A child develops multiple skin cancers on sun-exposed areas, severe photosensitivity, and inability to repair UV-induced pyrimidine dimers. The underlying defect lies in excising bulky helix-distorting lesions. Which repair pathway is abnormal?", "Nucleotide excision repair", ["Mismatch repair", "Homologous recombination", "Nonhomologous end joining only"], "Xeroderma pigmentosum involves nucleotide excision repair defects."),
        q("high", "A woman with inherited BRCA1 mutation develops high-grade serous carcinoma. The tumor is defective in homologous recombination repair, making it vulnerable to PARP inhibition through synthetic lethality. Which lesion is normally repaired by BRCA pathways?", "DNA double-strand breaks", ["Ig heavy-chain class switching only", "LDL receptor mutations", "Amyloid fibrils"], "BRCA1/2 are essential for homologous recombination repair of double-strand DNA breaks."),
    ]),
    ("metabolism-angiogenesis", "Tumor Metabolism, Evasion of Death, Immortality, and Angiogenesis", [
        q("easy", "The Warburg effect refers to tumor cells using:", "Aerobic glycolysis", ["Anaerobic metabolism only when oxygen is absent", "Fatty acid storage only", "Oxidative phosphorylation exclusively"], "Many cancers prefer glycolysis even in the presence of oxygen."),
        q("easy", "A major anti-apoptotic protein overexpressed in some lymphomas is:", "BCL2", ["RB", "APC", "E-cadherin"], "BCL2 blocks apoptosis and is activated in follicular lymphoma."),
        q("easy", "VEGF primarily promotes:", "Angiogenesis", ["Apoptosis", "DNA repair", "Contact inhibition"], "VEGF stimulates new vessel formation."),
        q("moderate", "Telomerase activation helps cancer cells by:", "Maintaining telomeres during repeated division", ["Degrading basement membrane", "Blocking glucose uptake", "Increasing E-cadherin"], "Telomerase prevents telomere crisis and supports replicative immortality."),
        q("moderate", "Hypoxia increases angiogenesis mainly by stabilizing:", "HIF-1 alpha", ["RB", "Caspase-3", "E-cadherin"], "HIF-1 alpha induces VEGF and metabolic adaptation under hypoxia."),
        q("moderate", "Follicular lymphoma commonly activates BCL2 through:", "t(14;18)", ["t(9;22)", "t(8;14)", "del(13q14) only"], "The Ig heavy-chain enhancer drives BCL2 expression in t(14;18)."),
        q("moderate", "Tumor angiogenesis often produces vessels that are:", "Leaky and irregular", ["Perfectly mature and nonpermeable", "Absent from all tumors", "Made only of lymphatics"], "Tumor vessels are abnormal, tortuous, and permeable."),
        q("high", "A PET scan detects intense uptake of fluorodeoxyglucose in a lung cancer even though oxygen is available. The tumor diverts glycolytic intermediates into nucleotide, amino acid, and lipid synthesis. Which metabolic adaptation is being exploited?", "Warburg effect", ["Pasteur effect only", "Oxidative burst", "Beta-pleated sheet formation"], "Aerobic glycolysis supports biosynthesis and is imaged by FDG-PET."),
        q("high", "A lymphoma cell survives despite signals that should trigger mitochondrial apoptosis. Cytogenetics shows t(14;18), placing BCL2 under immunoglobulin enhancer control. Which cancer hallmark is most directly promoted?", "Evasion of cell death", ["Self-sufficiency by RAS activation", "Loss of DNA mismatch repair", "Invasion through basement membrane"], "BCL2 overexpression prevents apoptosis."),
        q("high", "A tumor expands beyond 1 to 2 mm and develops central hypoxia. HIF-1 alpha induces VEGF, leading to new but abnormal blood vessels that support further tumor growth and provide access to the circulation. Which process is central?", "Tumor angiogenesis", ["Contact inhibition", "Carcinoma in situ", "Nucleotide excision repair"], "Angiogenesis is required for growth beyond diffusion limits and aids dissemination."),
    ]),
    ("invasion-metastasis", "Invasion and Metastasis", [
        q("easy", "Metastasis means:", "Spread of malignant tumor to distant sites", ["Benign encapsulation", "Full-thickness dysplasia without invasion", "Replacement of one epithelium by another"], "Metastasis is discontinuous spread of cancer."),
        q("easy", "Carcinomas most commonly spread initially by:", "Lymphatics", ["Synovial fluid only", "Nerve axons only", "Bile ducts only"], "Lymphatic spread is typical of carcinomas."),
        q("easy", "Sarcomas more often spread by:", "Bloodstream", ["Epidermal desquamation", "Sweat ducts", "Mucus only"], "Hematogenous spread is common in sarcomas."),
        q("moderate", "Loss of E-cadherin promotes invasion by reducing:", "Tumor cell adhesion to neighboring epithelial cells", ["Telomerase activity", "VEGF production", "DNA mutation rate"], "Reduced adhesion permits dissociation and invasion."),
        q("moderate", "Matrix metalloproteinases help metastasis by:", "Degrading extracellular matrix and basement membrane", ["Increasing RB activity", "Repairing UV damage", "Producing IgE"], "MMPs facilitate invasion through tissue barriers."),
        q("moderate", "Ovarian carcinoma commonly spreads by:", "Seeding of peritoneal surfaces", ["Paravertebral venous plexus only", "CSF in every case", "Direct spread through airways only"], "Ovarian cancers often exfoliate cells into the peritoneal cavity."),
        q("moderate", "Portal venous drainage helps explain why colon carcinoma often metastasizes first to:", "Liver", ["Brain", "Bone marrow only", "Skin"], "Blood from colon drains through portal circulation to liver."),
        q("high", "A breast carcinoma loses E-cadherin expression, degrades basement membrane with proteases, migrates through stroma, enters lymphatics, and forms deposits in axillary nodes. Which step sequence best describes this event?", "Local invasion followed by lymphatic metastasis", ["Carcinoma in situ without invasion", "Benign expansile growth", "Pure hematogenous sarcoma spread"], "Carcinoma metastasis requires invasion, intravasation, survival, extravasation, and colonization."),
        q("high", "A prostate carcinoma metastasizes to vertebral bodies despite other organs being closer in arterial flow. The spread follows valveless venous connections around the spine. Which pathway best explains this pattern?", "Paravertebral venous plexus spread", ["Peritoneal seeding", "Thoracic duct-only spread", "Direct implantation by biopsy"], "Pelvic tumors can spread to vertebrae through Batson paravertebral venous plexus."),
        q("high", "A renal cell carcinoma grows as a long tumor thrombus up the renal vein into the inferior vena cava, yet widespread metastases are initially absent. What concept from Robbins does this illustrate?", "Intravascular extension can occur without immediate widespread metastasis", ["All venous invasion proves systemic spread", "Benign tumors routinely invade veins", "Carcinoma in situ invades vessels"], "Some tumors, especially renal cell carcinoma, show striking venous growth without parallel dissemination."),
    ]),
    ("immunity-carcinogens", "Tumor Immunity and Carcinogenic Agents", [
        q("easy", "Tumor neoantigens are often generated by:", "Mutated proteins", ["Normal albumin only", "Unchanged collagen only", "Fibrinogen"], "Cancer mutations can create new peptides recognized by T cells."),
        q("easy", "The main antitumor effector lymphocyte is:", "CD8+ cytotoxic T cell", ["Naive erythrocyte", "Platelet", "Fibroblast"], "CTLs recognize tumor peptides on MHC I and kill tumor cells."),
        q("easy", "Immune checkpoint blockade commonly targets:", "PD-1/PD-L1 or CTLA-4 pathways", ["LDL receptors", "C1 inhibitor", "Fibrillin"], "Checkpoint inhibitors release brakes on antitumor T-cell responses."),
        q("moderate", "Tumors evade immunity by downregulating:", "MHC class I expression", ["Glucose uptake", "All oncogenes", "All VEGF"], "Loss of MHC I impairs CD8 T-cell recognition."),
        q("moderate", "Chemical carcinogenesis typically includes:", "Initiation and promotion", ["Only reversible edema", "Only immune complex deposition", "Only platelet adhesion"], "Initiation causes mutation; promotion drives clonal expansion."),
        q("moderate", "Direct-acting carcinogens require:", "No metabolic activation", ["Always viral infection", "Conversion by liver enzymes", "UV radiation only"], "Direct-acting agents are intrinsically carcinogenic."),
        q("moderate", "Indirect-acting chemical carcinogens are often activated by:", "Cytochrome P450 enzymes", ["Antibodies", "Caspases", "Telomerase"], "Procarcinogens require metabolic conversion to ultimate carcinogens."),
        q("high", "A melanoma responds to anti-PD-1 therapy after biopsy shows many mutation-derived neoantigens and T cells at the tumor edge. The treatment does not kill tumor cells directly but restores exhausted T-cell activity. Which mechanism is being targeted?", "Immune checkpoint-mediated T-cell inhibition", ["Tumor angiogenesis by VEGF", "RAS GTP hydrolysis", "Mismatch repair correction"], "PD-1 blockade reinvigorates antitumor T-cell responses."),
        q("high", "A chemical produces no tumor by itself after a single exposure, but later application of a nonmutagenic irritant causes clonal expansion of initiated cells and papilloma formation. Which stage does the irritant represent?", "Tumor promotion", ["Tumor initiation", "Metastatic colonization", "Immune editing"], "Promoters are nonmutagenic stimuli that expand initiated mutant clones."),
        q("high", "Aflatoxin B1 exposure in food leads to a characteristic TP53 mutation and greatly increases hepatocellular carcinoma risk, especially with hepatitis B infection. Which broad carcinogenic mechanism is most relevant?", "Chemical carcinogenesis with mutational DNA damage", ["IgE-mediated allergy", "Benign hamartomatous growth", "Chromosomal imprinting"], "Aflatoxin is an indirect chemical carcinogen producing DNA adducts and TP53 mutations."),
    ]),
    ("clinical", "Clinical Features, Grading, Staging, and Laboratory Diagnosis", [
        q("easy", "Tumor grade is based mainly on:", "Degree of differentiation and mitotic activity", ["Anatomic extent only", "Patient age only", "Tumor color"], "Grade estimates biologic aggressiveness from histology."),
        q("easy", "Tumor stage is based mainly on:", "Size/local extent, nodal spread, and distant metastasis", ["Microscopic differentiation only", "Amount of keratin only", "Cytoplasmic color"], "Stage describes anatomic spread, often by TNM."),
        q("easy", "For most solid tumors, prognosis correlates better with:", "Stage", ["Suffix of tumor name only", "Patient blood group", "Presence of edema"], "Anatomic extent is usually more prognostically important than grade."),
        q("moderate", "Cachexia in cancer is driven partly by:", "Inflammatory cytokines and altered metabolism", ["Pure starvation only", "Excess insulin alone", "Complete absence of tumor cytokines"], "Cancer cachexia involves systemic inflammation and metabolic wasting."),
        q("moderate", "Paraneoplastic syndromes are symptoms caused by:", "Hormone-like or immune effects not explained by local tumor spread", ["Only direct compression by tumor mass", "Only metastasis to lymph nodes", "Only chemotherapy toxicity"], "Paraneoplastic syndromes are remote effects of cancer."),
        q("moderate", "A classic paraneoplastic endocrine syndrome in small cell lung carcinoma is:", "Ectopic ACTH or ADH production", ["Insulin from colon carcinoma", "PTH from melanoma always", "Aldosterone from lymphoma"], "Small cell carcinoma may secrete ACTH or ADH."),
        q("moderate", "A definitive cancer diagnosis most often requires:", "Histologic or cytologic examination", ["Serum marker alone", "Fever pattern alone", "ESR alone"], "Tissue diagnosis remains central to tumor classification."),
        q("high", "A colon cancer invades through muscularis propria and has metastases in regional lymph nodes but no distant metastasis. Another colon cancer is poorly differentiated but confined to mucosa. Which parameter usually has greater prognostic weight?", "Stage based on anatomic spread", ["Grade alone", "Tumor pigment", "Presence of a capsule in all cancers"], "Stage generally predicts outcome better than grade in most solid tumors."),
        q("high", "A patient with lung cancer develops hypercalcemia, but imaging shows no bone metastases. Laboratory testing reveals tumor production of a parathyroid hormone-related peptide. Which clinical category best explains this finding?", "Paraneoplastic syndrome", ["Local invasion", "Tumor grading", "Carcinoma in situ"], "PTHrP-mediated hypercalcemia is a paraneoplastic endocrine syndrome."),
        q("high", "A man with pancreatic carcinoma loses marked weight despite adequate caloric intake and no mechanical obstruction. He has muscle wasting, anorexia, and elevated inflammatory mediators. Which mechanism best explains this systemic effect?", "Cancer cachexia mediated by cytokines and metabolic changes", ["Simple starvation alone", "Anaphylaxis", "Tumor embolism"], "Cachexia is a cytokine-driven wasting syndrome not fully reversed by nutrition."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if slug == "epidemiology":
            continue
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch7-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 7 questions, got {len(chapter_questions)}")
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
    data = json.loads(DATA_PATH.read_text(encoding="utf-8-sig"))
    existing = data.get("questions", [])
    kept = [question for question in existing if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch7-"))]
    data["questions"] = kept + chapter_questions
    validate(chapter_questions, data["questions"])
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Removed {len(existing) - len(kept)} existing Chapter 7 questions")
    print(f"Added {len(chapter_questions)} Robbins Chapter 7 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
