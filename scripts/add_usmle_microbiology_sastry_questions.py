import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = ROOT / "runtime-data" / "users.json"
SOURCE_PDF = "Essentials of Medical Microbiology, 4th ed., Apurba S. Sastry (provided PDF)"
ID_PREFIX = "usmle-microbiology-sastry-"


def question(
    number,
    chapter_title,
    chapter_order,
    topic,
    topic_order,
    page_start,
    prompt,
    options,
    answer_index,
    explanation,
    difficulty="moderate",
    tags=None,
    lead_in=None,
    laboratory_findings=None,
    item_family="mechanism",
    image_urls=None,
    page_end=None,
):
    return {
        "id": f"{ID_PREFIX}{number:02d}",
        "examId": "usmle-step-1",
        "examTitle": "USMLE Step 1-Style Practice",
        "subjectId": "microbiology",
        "subjectTitle": "Microbiology",
        "chapterTitle": chapter_title,
        "chapterOrder": chapter_order,
        "topic": topic,
        "topicTitle": topic,
        "topicOrder": topic_order,
        "source": "usmle",
        "sourcePdf": SOURCE_PDF,
        "sourcePdfPageStart": page_start,
        "sourcePdfPageEnd": page_end or page_start,
        "difficulty": difficulty,
        "prompt": prompt,
        "leadIn": lead_in,
        "laboratoryFindings": laboratory_findings or [],
        "itemFamily": item_family,
        "options": options,
        "answerIndex": answer_index,
        "answer": options[answer_index],
        "explanation": explanation,
        "imageUrls": image_urls or [],
        "tags": ["usmle-step-1", "sastry-microbiology-4e", *(tags or [])],
    }


QUESTIONS = [
    question(
        1,
        "Bacterial Lobar Pneumonia",
        61,
        "Pneumococcal Virulence",
        1,
        1370,
        "A 69-year-old man who underwent splenectomy after trauma develops fever, pleuritic chest pain, and cough productive of rust-colored sputum. Chest radiography shows right lower-lobe consolidation. A Gram-stained sputum specimen is shown. Which of the following microbial structures is the principal virulence factor of the causative organism?",
        [
            "Immunoglobulin A protease",
            "Lipopolysaccharide O antigen",
            "Polysaccharide capsule",
            "Protein A",
            "Type III secretion apparatus",
        ],
        2,
        "The image shows lancet-shaped gram-positive diplococci consistent with Streptococcus pneumoniae. Its polysaccharide capsule is the major virulence factor because it impairs phagocytosis; splenic macrophages are especially important for clearing encapsulated organisms.",
        tags=["streptococcus-pneumoniae", "capsule", "asplenia", "gram-stain"],
        image_urls=["/uploads/usmle-microbiology-sastry-q01-pneumococcus-gram-stain.png"],
        page_end=1373,
    ),
    question(
        2,
        "Antimicrobial Agents and Antimicrobial Resistance",
        3,
        "Methicillin Resistance in Staphylococcus aureus",
        1,
        192,
        "Blood cultures from a hospitalized patient with a catheter-associated infection grow Staphylococcus aureus that is resistant to oxacillin. Addition of a beta-lactamase inhibitor does not restore susceptibility. Which of the following alterations most likely accounts for this resistance?",
        [
            "Acquisition of a plasmid encoding an extended-spectrum beta-lactamase",
            "Decreased expression of outer-membrane porins",
            "Enzymatic replacement of D-alanine with D-lactate",
            "Increased production of a drug-efflux pump",
            "Production of a low-affinity penicillin-binding protein encoded by mecA",
        ],
        4,
        "Methicillin-resistant S aureus carries mecA, which encodes the altered penicillin-binding protein PBP2a. PBP2a has low affinity for most beta-lactams, so inhibiting beta-lactamase does not restore activity.",
        tags=["mrsa", "meca", "pbp2a", "antimicrobial-resistance"],
    ),
    question(
        3,
        "Complement",
        13,
        "Terminal Complement Deficiency",
        1,
        433,
        "A 17-year-old boy has his third episode of meningococcemia. He has otherwise had normal growth and no history of recurrent viral or fungal infections. Immunoglobulin concentrations are normal.",
        [
            "Formation of transmembrane pores in susceptible bacteria",
            "Generation of hydrogen peroxide within neutrophil phagolysosomes",
            "Opsonization of bacteria by immunoglobulin A",
            "Recognition of mannose residues by macrophage Toll-like receptors",
            "Transport of secretory immunoglobulin across mucosal epithelium",
        ],
        0,
        "Loss of terminal complement components C5-C9 prevents assembly of the membrane attack complex, which normally forms pores in target membranes. Terminal complement deficiency strongly predisposes to recurrent or disseminated Neisseria infection.",
        tags=["complement", "membrane-attack-complex", "neisseria"],
        lead_in="The patient's disorder most directly impairs which of the following immune functions?",
        laboratory_findings=[
            {"test": "CH50", "value": "Undetectable", "reference": "Normal hemolytic activity"},
            {"test": "AH50", "value": "Undetectable", "reference": "Normal hemolytic activity"},
            {"test": "Serum C3", "value": "112 mg/dL", "reference": "80-160 mg/dL"},
            {"test": "Serum C4", "value": "24 mg/dL", "reference": "10-40 mg/dL"},
        ],
        item_family="mechanism",
    ),
    question(
        4,
        "Hypersensitivity",
        16,
        "Tuberculin Delayed-Type Hypersensitivity",
        1,
        512,
        "A healthcare worker with prior latent Mycobacterium tuberculosis infection undergoes a tuberculin skin test. Forty-eight hours later, the injection site has a 17-mm area of firm induration. Biopsy of the site shows a predominantly mononuclear inflammatory infiltrate. Which of the following mechanisms most directly produces this reaction?",
        [
            "Deposition of circulating antigen-antibody complexes in dermal vessels",
            "IgE-mediated mast-cell degranulation after antigen cross-linking",
            "IgG-mediated activation of complement on antigen-bearing cells",
            "Release of interferon-gamma by antigen-specific T cells with macrophage activation",
            "Release of preformed histamine from sensitized basophils",
        ],
        3,
        "The tuberculin reaction is type IV delayed hypersensitivity. Previously sensitized T cells, predominantly TH1-derived cells, release interferon-gamma and other cytokines that recruit and activate macrophages over 48-72 hours.",
        tags=["tuberculin-test", "type-iv-hypersensitivity", "th1", "interferon-gamma"],
    ),
    question(
        5,
        "Cardiovascular System Infections",
        28,
        "Streptococcus gallolyticus Endocarditis",
        1,
        704,
        "A 66-year-old man has 6 weeks of fatigue, low-grade fever, and weight loss. Examination shows a new holosystolic murmur and splinter hemorrhages. Echocardiography demonstrates a mitral-valve vegetation, and three blood-culture sets grow Streptococcus gallolyticus. In addition to treating the endocarditis, which of the following is the most appropriate next step?",
        [
            "Bone-marrow biopsy",
            "Colonoscopy",
            "CT scan of the paranasal sinuses",
            "Serum protein electrophoresis",
            "Upper gastrointestinal endoscopy",
        ],
        1,
        "S gallolyticus, formerly S bovis, bacteremia or endocarditis is associated with colorectal carcinoma and adenomatous polyps. The patient should undergo evaluation of the colon even when gastrointestinal symptoms are absent.",
        tags=["streptococcus-gallolyticus", "endocarditis", "colorectal-cancer"],
        laboratory_findings=[
            {"test": "Hemoglobin", "value": "9.7 g/dL", "reference": "13.5-17.5 g/dL"},
            {"test": "Leukocyte count", "value": "13,200/mm3", "reference": "4,500-11,000/mm3"},
            {"test": "Blood cultures", "value": "3 of 3 sets positive", "reference": "No growth"},
        ],
        item_family="treatment",
    ),
    question(
        6,
        "Malaria and Babesiosis",
        35,
        "Falciparum Malaria and Sequestration",
        1,
        833,
        "A 32-year-old man develops fever, confusion, and a generalized seizure 2 weeks after returning from Nigeria. A Giemsa-stained peripheral blood smear is shown. MRI shows diffuse cerebral edema without a focal lesion. Which of the following parasite-host interactions most directly contributes to this severe neurologic complication?",
        [
            "Binding of Duffy antigen by merozoites restricted to reticulocytes",
            "Deposition of circulating immune complexes in cerebral arterioles",
            "Invasion of endothelial cells by sporozoites",
            "Lysis of erythrocytes containing Maltese-cross tetrads",
            "PfEMP1-mediated adherence of infected erythrocytes to vascular endothelium",
        ],
        4,
        "The crescent gametocyte and multiple delicate ring forms identify P falciparum. PfEMP1 on infected erythrocytes mediates cytoadherence and sequestration in small vessels of deep organs, including the brain, causing microvascular obstruction, hypoxia, and cerebral malaria.",
        difficulty="hard",
        tags=["plasmodium-falciparum", "cerebral-malaria", "pfemp1", "blood-smear"],
        laboratory_findings=[
            {"test": "Hemoglobin", "value": "8.9 g/dL", "reference": "13.5-17.5 g/dL"},
            {"test": "Platelet count", "value": "64,000/mm3", "reference": "150,000-400,000/mm3"},
            {"test": "Serum glucose", "value": "51 mg/dL", "reference": "70-100 mg/dL"},
            {"test": "Parasitemia", "value": "8%", "reference": "0%"},
        ],
        image_urls=["/uploads/usmle-microbiology-sastry-q06-falciparum-smear.png"],
        page_end=841,
    ),
    question(
        7,
        "Cholera and Halophilic Vibrio Infections",
        42,
        "Cholera Toxin Signaling",
        1,
        953,
        "A 28-year-old woman develops abrupt, profuse, painless watery diarrhea after drinking untreated water. She is severely dehydrated, and stool microscopy shows motile curved gram-negative rods without fecal leukocytes. The responsible toxin binds GM1 ganglioside on intestinal epithelial cells. Which of the following intracellular events is caused by its active subunit?",
        [
            "Cleavage of synaptobrevin in cholinergic nerve terminals",
            "Dephosphorylation of elongation factor 2",
            "ADP-ribosylation of a G protein with persistent adenylate cyclase activation",
            "Glycosylation of Rho-family GTP-binding proteins",
            "Irreversible inhibition of the 60S ribosomal subunit",
        ],
        2,
        "The A subunit of cholera toxin ADP-ribosylates the stimulatory G protein, persistently activating adenylate cyclase. Increased cAMP promotes chloride secretion and inhibits sodium absorption, producing isotonic watery diarrhea.",
        tags=["vibrio-cholerae", "cholera-toxin", "camp", "gm1"],
    ),
    question(
        8,
        "Clostridioides difficile Infection",
        43,
        "Toxin-Mediated Pseudomembranous Colitis",
        1,
        982,
        "A 74-year-old woman develops fever, abdominal cramping, and frequent watery stools after receiving clindamycin. Colonoscopy shows raised yellow-white plaques over erythematous mucosa. The bacterial products responsible for this disease most directly injure enterocytes by which of the following mechanisms?",
        [
            "Glycosylation and inactivation of Rho-family GTP-binding proteins",
            "Inhibition of acetylcholine release from enteric neurons",
            "Irreversible activation of adenylate cyclase by a G protein",
            "Proteolytic cleavage of E-cadherin at epithelial junctions",
            "Stimulation of guanylate cyclase through a heat-stable peptide",
        ],
        0,
        "C difficile toxins A and B glycosylate regulatory GTP-binding proteins involved in the actin cytoskeleton. Loss of cytoskeletal integrity and epithelial barrier function produces diarrhea, inflammation, and pseudomembrane formation.",
        tags=["clostridioides-difficile", "toxin-a", "toxin-b", "rho-gtpase"],
    ),
    question(
        9,
        "Staphylococcal Infections",
        51,
        "Toxic Shock Syndrome Toxin",
        1,
        1163,
        "A 24-year-old woman presents with high fever, vomiting, diffuse erythema, hypotension, and acute kidney injury during menstruation. Blood cultures are negative. A vaginal culture grows Staphylococcus aureus. Which of the following mechanisms best explains the systemic manifestations?",
        [
            "Antibody-mediated destruction of endothelial cells",
            "Binding of Fc immunoglobulin through bacterial protein A",
            "Endotoxin-mediated activation of Toll-like receptor 4",
            "Cross-linking of MHC class II and T-cell receptors outside the antigen-binding groove",
            "Formation of pores in phagocyte membranes by leukocidin",
        ],
        3,
        "Toxic shock syndrome toxin 1 acts as a superantigen. It cross-links MHC class II on antigen-presenting cells to T-cell receptors outside the normal peptide-binding site, activating many T cells and causing massive cytokine release, fever, rash, and shock.",
        tags=["staphylococcus-aureus", "toxic-shock-syndrome", "superantigen"],
    ),
    question(
        10,
        "Beta-Hemolytic Streptococcal Infections",
        52,
        "Acute Rheumatic Fever",
        1,
        1190,
        "An 11-year-old boy develops migratory pain and swelling of the knees and ankles 3 weeks after an untreated episode of exudative pharyngitis. Examination shows a new apical holosystolic murmur. Which of the following immunologic mechanisms most likely caused this complication?",
        [
            "Deposition of streptococcal antigen-antibody complexes in cardiac valves",
            "Cross-reactivity between antibodies to streptococcal antigens and host cardiac tissue",
            "Direct invasion of the myocardium by viable streptococci",
            "Polyclonal T-cell activation by a streptococcal superantigen",
            "Toxin-mediated inhibition of cardiomyocyte protein synthesis",
        ],
        1,
        "Acute rheumatic fever follows group A streptococcal pharyngitis. Molecular mimicry causes antibodies and immune cells directed against streptococcal antigens to cross-react with host tissues, particularly the heart, joints, skin, and central nervous system.",
        tags=["streptococcus-pyogenes", "rheumatic-fever", "molecular-mimicry"],
    ),
    question(
        11,
        "Tuberculosis and Nontuberculous Mycobacteria",
        63,
        "Mycobacterial Acid Fastness",
        1,
        1412,
        "A 46-year-old man has 3 months of cough, night sweats, fever, and weight loss. Chest radiography shows cavitary lesions in both upper lobes. A stained sputum specimen is shown. The staining property of the organisms is primarily attributable to a high concentration of which of the following cell-wall components?",
        [
            "Mycolic acids",
            "N-acetylneuraminic acid",
            "Peptidoglycan teichoic acids",
            "Porin proteins",
            "Wax-free lipopolysaccharide",
        ],
        0,
        "The image shows red acid-fast bacilli. The long-chain mycolic acids of the mycobacterial cell wall confer resistance to acid-alcohol decolorization, reduce cell-wall permeability, and contribute to intrinsic resistance to many antimicrobial drugs.",
        tags=["mycobacterium-tuberculosis", "acid-fast", "mycolic-acid", "ziehl-neelsen"],
        image_urls=["/uploads/usmle-microbiology-sastry-q11-acid-fast-bacilli.png"],
    ),
    question(
        12,
        "Bacterial Atypical Pneumonia",
        62,
        "Laboratory Diagnosis of Legionella",
        1,
        1408,
        "A 61-year-old man develops high fever, nonproductive cough, diarrhea, and confusion after attending a convention at a hotel. Chest radiography shows patchy bilateral infiltrates. Sputum contains many neutrophils, but routine Gram stain shows few organisms. Which of the following culture media is most appropriate for isolating the pathogen?",
        [
            "Bile-esculin agar with sodium azide",
            "Chocolate agar containing factors V and X",
            "Lowenstein-Jensen medium",
            "Thayer-Martin medium",
            "Buffered charcoal yeast-extract agar",
        ],
        4,
        "Legionella pneumophila causes severe atypical pneumonia with gastrointestinal and neurologic symptoms and often hyponatremia. It stains poorly with Gram stain and is cultured on buffered charcoal yeast-extract agar, which supports this fastidious organism.",
        tags=["legionella", "atypical-pneumonia", "bcye-agar"],
        laboratory_findings=[
            {"test": "Serum sodium", "value": "126 mEq/L", "reference": "136-145 mEq/L"},
            {"test": "AST", "value": "82 U/L", "reference": "10-40 U/L"},
            {"test": "Creatine kinase", "value": "620 U/L", "reference": "30-200 U/L"},
        ],
        item_family="laboratory-diagnosis",
    ),
    question(
        13,
        "Myxovirus Infections of the Respiratory Tract",
        66,
        "Influenza Antigenic Shift",
        1,
        1479,
        "A swine farm worker is simultaneously infected with an avian influenza A strain and a human influenza A strain. Viral progeny isolated from respiratory secretions contain a novel combination of hemagglutinin and neuraminidase genes and spread efficiently between humans. Which of the following processes produced this change?",
        [
            "Complementation between two defective viral genomes",
            "Reassortment of segmented viral RNA genomes",
            "Recombination of proviral DNA integrated into host chromosomes",
            "Stepwise accumulation of point mutations during seasonal transmission",
            "Transduction of envelope genes by a bacteriophage",
        ],
        1,
        "Influenza A has a segmented RNA genome. Coinfection of one cell by distinct strains can exchange entire genome segments, producing an abrupt major antigenic change called antigenic shift and creating the potential for a pandemic.",
        tags=["influenza-a", "antigenic-shift", "reassortment"],
    ),
    question(
        14,
        "Miscellaneous Viral Respiratory Infections",
        68,
        "Epstein-Barr Virus Infection",
        1,
        1523,
        "A 19-year-old college student has fever, exudative pharyngitis, posterior cervical lymphadenopathy, and splenomegaly. A peripheral blood smear shows atypical lymphocytes, and a heterophile-antibody test is positive. The causative virus initially infects B lymphocytes by binding which of the following surface molecules?",
        [
            "CCR5",
            "CD4",
            "CD8",
            "CD21",
            "ICAM-1",
        ],
        3,
        "Epstein-Barr virus binds CD21, also called complement receptor 2, on B lymphocytes and pharyngeal epithelial cells. The atypical cells in blood are activated CD8 T lymphocytes responding to infected B cells.",
        tags=["epstein-barr-virus", "infectious-mononucleosis", "cd21"],
    ),
    question(
        15,
        "Viral Encephalitis and Encephalopathy",
        74,
        "Rabies Postexposure Prophylaxis",
        1,
        1639,
        "A previously unvaccinated 34-year-old wildlife biologist is bitten deeply on the hand by a bat that escapes. He presents 2 hours later. The wound is bleeding, and he has no neurologic symptoms. Which of the following is the most appropriate management?",
        [
            "Observe without treatment unless symptoms develop",
            "Rabies vaccine alone after primary closure of the wound",
            "Immediate wound cleansing, rabies vaccine, and infiltration of rabies immunoglobulin around the wound",
            "Rabies immunoglobulin alone because it acts immediately",
            "Surgical excision of the wound followed by oral antiviral therapy",
        ],
        2,
        "A transdermal bite from a bat is a high-risk exposure. Postexposure prophylaxis for a previously unvaccinated person includes thorough local wound care, active immunization with rabies vaccine, and passive immunization with rabies immunoglobulin infiltrated into and around the wound when feasible.",
        tags=["rabies", "postexposure-prophylaxis", "rabies-immunoglobulin", "vaccine"],
        item_family="treatment",
    ),
    question(
        16,
        "Parasitic and Fungal Infections of the Respiratory Tract",
        69,
        "Rhino-Orbital-Cerebral Mucormycosis",
        1,
        1542,
        "A 53-year-old man with poorly controlled diabetes mellitus is admitted for diabetic ketoacidosis. Two days later, he develops severe facial pain, periorbital swelling, ophthalmoplegia, and a black necrotic lesion on the nasal turbinate. Histologic examination of debrided tissue is shown. Which of the following is the most likely diagnosis?",
        [
            "Invasive aspergillosis",
            "Mucormycosis",
            "Nocardiosis",
            "Pseudomonas ecthyma gangrenosum",
            "Rhinosporidiosis",
        ],
        1,
        "The image shows broad, ribbon-like, pauciseptate hyphae with wide-angle branching and angioinvasion, characteristic of mucormycosis. Diabetic ketoacidosis is a major risk factor for rapidly progressive rhino-orbital-cerebral disease.",
        tags=["mucormycosis", "diabetic-ketoacidosis", "broad-aseptate-hyphae"],
        image_urls=["/uploads/usmle-microbiology-sastry-q16-mucormycosis-hyphae.png"],
        item_family="diagnosis",
    ),
    question(
        17,
        "Congenital Infections",
        79,
        "Congenital Cytomegalovirus Infection",
        1,
        1786,
        "A newborn is small for gestational age and has jaundice, hepatosplenomegaly, petechiae, microcephaly, and sensorineural hearing loss. Cranial ultrasonography shows periventricular calcifications. Which of the following histopathologic findings is most likely?",
        [
            "Crescent-shaped intracellular organisms within macrophages",
            "Granulomas containing spherules filled with endospores",
            "Multinucleated giant cells with molded nuclei and margination of chromatin",
            "Neurons containing eosinophilic cytoplasmic inclusions",
            "Enlarged cells containing intranuclear owl-eye inclusions",
        ],
        4,
        "The findings indicate congenital cytomegalovirus infection. CMV produces cytomegalic cells with characteristic large intranuclear owl-eye inclusions. Periventricular calcifications and sensorineural hearing loss help distinguish CMV from congenital toxoplasmosis.",
        tags=["congenital-cmv", "owl-eye-inclusion", "periventricular-calcifications"],
        laboratory_findings=[
            {"test": "Platelet count", "value": "58,000/mm3", "reference": "150,000-400,000/mm3"},
            {"test": "Direct bilirubin", "value": "4.1 mg/dL", "reference": "<0.3 mg/dL"},
            {"test": "Urine CMV PCR", "value": "Positive", "reference": "Negative"},
        ],
        item_family="predicted-finding",
        page_end=1790,
    ),
    question(
        18,
        "HIV/AIDS",
        33,
        "Detection During the HIV Window Period",
        1,
        794,
        "A 27-year-old man has fever, sore throat, diffuse lymphadenopathy, and a maculopapular rash 18 days after unprotected sexual exposure. A third-generation antibody-only HIV assay is negative. Which of the following tests is most likely to detect infection at this time?",
        [
            "Plasma HIV RNA by reverse-transcription PCR",
            "HIV proviral DNA in a hair-follicle specimen",
            "IgG antibody to Epstein-Barr nuclear antigen",
            "Western blot for HIV envelope antibodies alone",
            "Repeat antibody-only assay in 24 hours",
        ],
        0,
        "Acute retroviral syndrome can occur before antibodies become detectable. Plasma HIV RNA is detectable earliest, often within about 10-14 days after exposure; fourth-generation assays shorten the window by also detecting p24 antigen.",
        tags=["acute-hiv", "window-period", "hiv-rna", "rt-pcr"],
        laboratory_findings=[
            {"test": "Leukocyte count", "value": "3,400/mm3", "reference": "4,500-11,000/mm3"},
            {"test": "Platelet count", "value": "118,000/mm3", "reference": "150,000-400,000/mm3"},
            {"test": "Antibody-only HIV assay", "value": "Negative", "reference": "Negative"},
        ],
        difficulty="hard",
        item_family="laboratory-diagnosis",
        page_end=799,
    ),
    question(
        19,
        "Laboratory Diagnosis of Bacterial Infections",
        3,
        "Diagnostic-Test Sensitivity",
        2,
        151,
        "Investigators compare a new multiplex PCR assay with culture, the reference standard, for detecting a bacterial bloodstream infection. Among 100 patients with positive cultures, the PCR result is positive in 90 and negative in 10. Among 900 patients with negative cultures, the PCR result is positive in 45 and negative in 855. What is the sensitivity of the PCR assay?",
        [
            "10%",
            "67%",
            "90%",
            "95%",
            "99%",
        ],
        2,
        "Sensitivity is the proportion of patients with the infection who test positive: true positives divided by true positives plus false negatives. Here, sensitivity is 90 / (90 + 10) = 90%.",
        tags=["diagnostic-testing", "sensitivity", "multiplex-pcr"],
        item_family="experimental-design",
    ),
    question(
        20,
        "AETCOM in Microbiology",
        9,
        "Confidentiality of an HIV Test Result",
        1,
        1878,
        "A 29-year-old woman is informed that confirmatory testing for HIV is positive. She begins to cry and says, \"Please do not tell my husband yet. I need time to understand this first.\" Which of the following is the most appropriate initial response by the physician?",
        [
            "I must call your husband immediately because he may have been exposed",
            "I will document that you refused disclosure and end today's visit",
            "You should not worry because current treatment makes HIV harmless",
            "I can see this is overwhelming; let's discuss your concerns, confidentiality, and how we can safely involve your partner",
            "Your husband can only be tested after you provide written permission",
        ],
        3,
        "The initial response should acknowledge emotion, preserve trust, and invite discussion. HIV results are confidential, while partner safety and applicable disclosure requirements must be addressed through counseling and a plan rather than immediate coercive disclosure or false reassurance.",
        tags=["hiv", "confidentiality", "patient-communication"],
        item_family="communication-ethics",
    ),
]


def validate_questions():
    assert len(QUESTIONS) == 20
    assert len({item["id"] for item in QUESTIONS}) == 20
    for item in QUESTIONS:
        assert item["source"] == "usmle"
        assert item["subjectId"] == "microbiology"
        assert len(item["options"]) == 5
        assert len(set(item["options"])) == 5
        assert 0 <= item["answerIndex"] < len(item["options"])
        assert item["answer"] == item["options"][item["answerIndex"]]
        assert (item["leadIn"] or item["prompt"]).strip().endswith("?")
        assert item["explanation"].strip()
        assert item["sourcePdfPageStart"] <= item["sourcePdfPageEnd"]
        assert len(item["imageUrls"]) <= 1
        for finding in item["laboratoryFindings"]:
            assert set(finding) == {"test", "value", "reference"}
            assert all(str(value).strip() for value in finding.values())

    item_families = [item["itemFamily"] for item in QUESTIONS]
    assert item_families.count("diagnosis") == 1
    assert item_families.count("communication-ethics") == 1
    assert item_families.count("experimental-design") == 1
    assert sum(bool(item["laboratoryFindings"]) for item in QUESTIONS) == 6
    assert sum(bool(item["imageUrls"]) for item in QUESTIONS) == 4
    assert sorted(item["answerIndex"] for item in QUESTIONS) == [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]

    for item in QUESTIONS:
        for image_url in item["imageUrls"]:
            assert image_url.startswith("/uploads/")
            assert (ROOT / "public" / image_url.removeprefix("/")).is_file()


def main():
    validate_questions()
    database = json.loads(DATABASE_PATH.read_text(encoding="utf-8-sig"))
    existing = database.get("questions", [])
    retained = [item for item in existing if not str(item.get("id", "")).startswith(ID_PREFIX)]
    database["questions"] = [*retained, *QUESTIONS]
    DATABASE_PATH.write_text(json.dumps(database, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Stored {len(QUESTIONS)} USMLE Step 1-style microbiology questions.")
    print(f"Database question count: {len(existing)} -> {len(database['questions'])}")


if __name__ == "__main__":
    main()
