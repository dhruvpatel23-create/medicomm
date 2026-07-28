import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path("runtime-data/users.json")
CHAPTER = "Diseases of the Immune System"

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
    ("innate", "Innate Immunity", [
        q("easy", "The first line of defense that is ready before antigen exposure is called:", "Innate immunity", ["Adaptive immunity", "Humoral memory", "Clonal selection"], "Innate immunity is constitutively present and responds rapidly to microbes and damaged cells."),
        q("easy", "Which cells are the principal rapid phagocytes recruited from blood during innate immune responses?", "Neutrophils and monocytes", ["Plasma cells and eosinophils", "Megakaryocytes and erythroblasts", "Fibroblasts and chondrocytes"], "Neutrophils and monocytes/macrophages are central innate phagocytes."),
        q("easy", "Epithelia contribute to innate immunity mainly by:", "Providing barriers and producing antimicrobial molecules", ["Making antigen-specific IgG memory", "Undergoing V(D)J recombination", "Presenting antigen only on MHC class II"], "Skin and mucosal epithelia block entry and secrete defensins and other antimicrobial products."),
        q("moderate", "Toll-like receptors are important because they:", "Recognize conserved microbial products and activate inflammatory genes", ["Generate antibody diversity", "Kill targets by perforin only", "Bind peptide-MHC complexes on T cells"], "TLRs are pattern-recognition receptors for microbial PAMPs and damage signals."),
        q("moderate", "The inflammasome promotes inflammation chiefly by increasing production of:", "Active IL-1", ["IgE", "C3b only", "Fibrillin-1"], "Inflammasomes activate caspase-1, which processes pro-IL-1 beta into active IL-1."),
        q("moderate", "Natural killer cells kill abnormal cells when:", "Activating signals exceed inhibitory MHC class I signals", ["B-cell receptors bind soluble antigen", "CD4 cells secrete IL-4 only", "Complement fixes to immune complexes"], "NK cells integrate activating stress ligands and inhibitory recognition of self MHC I."),
        q("moderate", "Antibody-dependent cellular cytotoxicity by NK cells depends on:", "CD16 binding IgG Fc tails", ["CD28 binding B7", "TCR binding MHC II", "C1 inhibitor binding bradykinin"], "NK-cell CD16 recognizes IgG-coated targets and triggers killing."),
        q("high", "A virus-infected cell downregulates MHC class I and expresses stress-induced ligands on its surface. A nearby lymphocyte lacks a TCR but contains cytotoxic granules and secretes IFN-gamma. Which cell is best suited to eliminate this target?", "Natural killer cell", ["Naive B cell", "Follicular dendritic cell", "Th17 lymphocyte"], "Loss of MHC I removes NK inhibition, while stress ligands activate NK-cell cytotoxicity."),
        q("high", "A patient has recurrent fever attacks from excessive inflammasome activity but no autoantibodies or antigen-specific T-cell response. Symptoms improve dramatically with IL-1 blockade. This pattern is best classified as:", "Autoinflammatory disease", ["Classic antibody-mediated autoimmunity", "Type I hypersensitivity", "Transplant rejection"], "Autoinflammatory syndromes arise from dysregulated innate immunity, often IL-1 driven."),
        q("high", "Bacterial peptides containing N-formylmethionine are detected by leukocyte G-protein-coupled receptors. Neutrophils then migrate up the concentration gradient toward the infected tissue. Which innate immune function is being illustrated?", "Chemotaxis toward microbial products", ["Somatic hypermutation", "Class switching to IgE", "Central T-cell tolerance"], "N-formylated bacterial peptides act as chemoattractants for innate leukocytes."),
    ]),
    ("adaptive", "Adaptive Immunity and Antigen Presentation", [
        q("easy", "Adaptive immunity is mediated mainly by:", "T and B lymphocytes", ["Neutrophils only", "Endothelial cells only", "Platelets only"], "T and B cells provide antigen-specific immunity and memory."),
        q("easy", "The enzyme complex required for antigen receptor gene recombination is encoded by:", "RAG-1 and RAG-2", ["FBN1 and FBN2", "BRCA1 and BRCA2", "NPC1 and NPC2"], "RAG proteins mediate V(D)J recombination in developing lymphocytes."),
        q("easy", "Class I MHC molecules present peptides mainly to:", "CD8+ T cells", ["CD4+ T cells", "B cells only", "Mast cells"], "CD8 T cells recognize cytosolic peptides displayed by MHC class I."),
        q("moderate", "Class II MHC molecules present peptides mainly to:", "CD4+ T cells", ["CD8+ T cells", "NK cells only", "Erythrocytes"], "CD4 T cells recognize extracellularly derived peptides on MHC class II."),
        q("moderate", "Which cells are the most efficient antigen-presenting cells for activating naive T lymphocytes?", "Dendritic cells", ["Red blood cells", "Platelets", "Fibroblasts"], "Dendritic cells capture antigens in tissues and present them in T-cell zones of lymphoid organs."),
        q("moderate", "The principal costimulatory signal for naive T-cell activation is:", "B7 on APCs binding CD28 on T cells", ["CD16 binding IgG", "IgE binding Fc epsilon receptor", "C3b binding CR1 only"], "Signal 2 is provided by B7/CD28, ensuring T cells respond to danger-associated antigens."),
        q("moderate", "Follicular dendritic cells mainly help B-cell responses by:", "Displaying antibody- or complement-coated antigen in germinal centers", ["Phagocytosing bacteria in abscesses", "Killing MHC I-negative tumor cells", "Producing all serum IgG"], "FDCs retain immune complexes for selection of high-affinity B cells."),
        q("high", "A lymph node biopsy shows many lymphocytes with different immunoglobulin gene rearrangements after infection. Another node shows one dominant rearrangement pattern in nearly all B cells. What is the key diagnostic use of antigen receptor gene rearrangement testing here?", "Distinguishing polyclonal reactive proliferation from monoclonal lymphoma", ["Identifying edema fluid as exudate", "Measuring serum complement activity", "Diagnosing platelet aggregation defects"], "Each lymphocyte clone has a unique rearrangement; monoclonality suggests neoplasia."),
        q("high", "A vaccine protein is injected with an adjuvant. The antigen is recognized by T cells, but robust T-cell activation occurs only because the adjuvant stimulates dendritic cells to express B7 and cytokines. What principle explains this?", "Naive T cells require antigen plus costimulation", ["Antibodies require no T-cell help", "NK cells require somatic recombination", "MHC molecules bind only lipids"], "Signal 1 alone may induce tolerance; costimulation links adaptive responses to innate danger signals."),
        q("high", "A virus produces proteins in the cytosol of an infected epithelial cell. Peptides are generated in proteasomes, transported into the ER, and displayed to lymphocytes that kill the infected cell. Which MHC pathway is being used?", "Class I MHC presentation to CD8+ cytotoxic T cells", ["Class II MHC presentation to CD4+ cells", "FDC presentation to B cells", "IgE presentation to mast cells"], "Cytosolic antigens are presented on MHC I to CD8 CTLs."),
    ]),
    ("lymphocyte-effector", "T-Cell and B-Cell Effector Responses", [
        q("easy", "IL-2 produced by activated T cells primarily functions as:", "A T-cell growth factor", ["An opsonin", "A collagenase", "A complement inhibitor"], "IL-2 drives clonal expansion of antigen-stimulated T cells."),
        q("easy", "Th1 cells characteristically secrete:", "IFN-gamma", ["IL-4 only", "IgE", "Histamine"], "Th1 cells activate macrophages through IFN-gamma."),
        q("easy", "Th2 cells are especially important in defense against:", "Helminths", ["Intracellular viruses only", "Prions only", "Sterile infarcts"], "Th2 cytokines promote IgE, eosinophils, mast cells, and anti-helminth responses."),
        q("moderate", "Th17 cells promote inflammation mainly by:", "Recruiting neutrophils and monocytes", ["Killing targets with perforin", "Producing all antibody", "Suppressing all immune responses"], "Th17 cytokines induce chemokines and recruit inflammatory leukocytes."),
        q("moderate", "CD40 ligand on helper T cells is important because it:", "Activates macrophages and helps B-cell class switching", ["Binds MHC I on infected cells", "Serves as an antibody Fc receptor", "Blocks all cytokine secretion"], "CD40L-CD40 interactions are central to T-cell help for macrophages and B cells."),
        q("moderate", "Cytotoxic T lymphocytes kill infected cells mainly using:", "Perforin and granzymes", ["IgE and histamine", "C3a and C5a", "Fibrin and thrombin"], "CTL granules induce apoptosis in antigen-bearing target cells."),
        q("moderate", "Affinity maturation of antibodies occurs in:", "Germinal centers", ["Thymic cortex only", "Bone marrow sinusoids only", "Red pulp cords only"], "Somatic hypermutation and selection in germinal centers increase antibody affinity."),
        q("high", "A patient with a CD40L mutation has recurrent pyogenic and opportunistic infections with very high IgM but little IgG, IgA, or IgE. Germinal centers are poorly developed. Which failed process best explains this syndrome?", "T-cell-dependent B-cell class switching", ["MHC class I peptide transport", "NK-cell recognition of missing self", "C1 inhibitor regulation"], "CD40L deficiency causes hyper-IgM syndrome by blocking class switching and germinal center reactions."),
        q("high", "A macrophage contains viable intracellular mycobacteria. A nearby CD4+ T cell recognizes microbial peptide on MHC II, expresses CD40L, and secretes IFN-gamma. What is the main intended result?", "Classical macrophage activation with enhanced microbicidal killing", ["Immediate IgE-mediated mast cell degranulation", "Complement-mediated RBC lysis", "B-cell receptor editing"], "Th1 CD40L and IFN-gamma activate macrophages to kill ingested microbes."),
        q("high", "A child has recurrent mucocutaneous fungal infections due to impaired IL-17 signaling. Neutrophil numbers are normal, but epithelial chemokine responses are weak. Which helper T-cell subset function is most impaired?", "Th17-mediated recruitment of neutrophils and barrier defense", ["Th2-mediated eosinophil activation", "Treg-mediated tolerance", "CTL-mediated perforin release"], "Th17 cells are crucial for neutrophil-rich responses at mucosal barriers, especially against fungi."),
    ]),
    ("hypersensitivity-1-2", "Type I and Type II Hypersensitivity", [
        q("easy", "Type I hypersensitivity is mediated primarily by:", "IgE and mast cells", ["IgG immune complexes", "CD8 T cells only", "Amyloid fibrils"], "Immediate hypersensitivity is driven by IgE-sensitized mast cell degranulation."),
        q("easy", "The main vasoactive amine released from mast cell granules is:", "Histamine", ["IL-2", "C3b", "TGF-beta"], "Histamine causes vasodilation, vascular leakage, and bronchoconstriction."),
        q("easy", "Type II hypersensitivity is caused by antibodies directed against:", "Cell-surface or extracellular matrix antigens", ["Soluble circulating antigen only", "Inhaled pollen only", "Misfolded light chains only"], "Type II reactions involve IgG or IgM binding fixed antigens on cells or matrix."),
        q("moderate", "Anaphylaxis is an example of:", "Systemic type I hypersensitivity", ["Type IV delayed hypersensitivity", "Immune complex vasculitis", "Granulomatous inflammation only"], "Widespread IgE-mediated mast cell activation causes systemic vascular leakage and bronchospasm."),
        q("moderate", "Autoimmune hemolytic anemia is an example of:", "Antibody-mediated cell destruction", ["IgE-mediated allergy", "T-cell-mediated granuloma", "AL amyloidosis"], "IgG or complement on RBCs leads to phagocytosis or lysis."),
        q("moderate", "Goodpasture syndrome involves antibodies against:", "Basement membrane antigens", ["Acetylcholine receptor", "TSH receptor", "FMR1 protein"], "Anti-basement membrane antibodies injure glomeruli and alveoli."),
        q("moderate", "Myasthenia gravis is type II hypersensitivity because antibodies:", "Block acetylcholine receptors", ["Stimulate thyroid cells", "Form soluble immune complexes", "Activate mast cells through IgE"], "Antibodies alter receptor function without necessarily destroying cells."),
        q("high", "Minutes after a bee sting, a sensitized patient develops bronchospasm, hypotension, urticaria, and laryngeal edema. Serum tryptase is elevated, and symptoms improve with epinephrine. Which mechanism produced the acute event?", "IgE cross-linking on mast cells with mediator release", ["IgG against basement membrane", "Th1 macrophage activation", "Cytotoxic T-cell killing"], "Systemic immediate hypersensitivity reflects mast cell degranulation after IgE cross-linking."),
        q("high", "A woman develops weakness that worsens with repeated use of muscles. Autoantibodies bind the acetylcholine receptor and reduce neuromuscular transmission, but the receptor is not a soluble antigen. Which hypersensitivity mechanism is most accurate?", "Type II antibody-mediated receptor blockade", ["Type I IgE-mediated degranulation", "Type III immune complex deposition", "Type IV granulomatous inflammation"], "Myasthenia gravis is a functional type II antibody-mediated disease."),
        q("high", "A patient has hemoptysis, renal failure, linear IgG staining along glomerular basement membranes, and antibodies against a noncollagenous domain of type IV collagen. Which type II pattern best fits this disease?", "Antibody-mediated tissue injury against fixed basement membrane antigen", ["Antibody stimulation of endocrine receptors", "IgE-mediated late-phase inflammation", "Delayed-type hypersensitivity to tuberculin"], "Goodpasture syndrome is caused by antibodies binding fixed BM antigens, activating complement and leukocytes."),
    ]),
    ("hypersensitivity-3-4", "Type III and Type IV Hypersensitivity", [
        q("easy", "Type III hypersensitivity is mediated by:", "Immune complex deposition", ["IgE on mast cells", "Direct receptor blockade only", "Mitochondrial mutation"], "Soluble antigen-antibody complexes deposit and trigger complement and inflammation."),
        q("easy", "Type IV hypersensitivity is mediated by:", "T lymphocytes", ["IgE only", "Circulating immune complexes only", "LDL receptors"], "Delayed-type and cytotoxic T-cell reactions are type IV hypersensitivity."),
        q("easy", "The tuberculin skin test is a classic example of:", "Delayed-type hypersensitivity", ["Immediate anaphylaxis", "Antibody-mediated hemolysis", "Serum sickness"], "Prior sensitization leads to Th1-mediated macrophage inflammation after 24 to 72 hours."),
        q("moderate", "Serum sickness is caused by:", "Systemic immune complex deposition", ["IgE against pollen", "Autoantibodies blocking acetylcholine receptors", "T-cell killing of tumor cells only"], "Circulating immune complexes deposit in vessels, joints, and kidneys."),
        q("moderate", "An Arthus reaction is:", "Localized immune complex-mediated vasculitis", ["Systemic anaphylaxis", "Autoimmune receptor stimulation", "Central T-cell deletion"], "Preexisting IgG reacts with injected antigen and forms local immune complexes."),
        q("moderate", "Complement activation in type III hypersensitivity recruits:", "Neutrophils", ["Only eosinophils", "Only plasma cells", "Only fibroblasts"], "C5a attracts neutrophils, which release enzymes and cause tissue injury."),
        q("moderate", "Contact dermatitis from poison ivy is mediated mainly by:", "T-cell responses to hapten-modified proteins", ["IgE-coated mast cells", "Circulating DNA-anti-DNA complexes", "Anti-GBM antibodies"], "Small chemicals act as haptens and elicit type IV T-cell inflammation."),
        q("high", "A child receives heterologous antiserum and 8 days later develops fever, urticaria, arthralgias, proteinuria, and low complement. Biopsy shows granular immune deposits in small vessels. Which mechanism explains the disease?", "Systemic type III hypersensitivity from circulating immune complexes", ["Type I IgE-mediated anaphylaxis", "Type II receptor stimulation", "Primary T-cell immunodeficiency"], "Serum sickness occurs when soluble immune complexes form and deposit after antibody appears."),
        q("high", "A purified protein derivative skin test is read at 48 hours and shows induration, not just erythema. The lesion contains T cells and activated macrophages rather than immune-complex neutrophilic vasculitis. Which cytokine is central?", "IFN-gamma", ["Histamine", "C1 inhibitor", "Erythropoietin"], "Th1 cells secrete IFN-gamma, activating macrophages in delayed-type hypersensitivity."),
        q("high", "A renal biopsy shows granular immune deposits in glomeruli after infection, with complement consumption and neutrophilic inflammation. The target antigen is not fixed in the basement membrane before antibody binding. Which pattern distinguishes this from Goodpasture syndrome?", "Immune complex deposition with granular staining", ["Linear antibody binding to fixed antigen", "IgE-mediated mast cell degranulation", "T-cell receptor gene recombination"], "Type III lesions show granular immune complex deposits; anti-GBM disease shows linear staining."),
    ]),
    ("systemic-autoimmune", "Systemic Autoimmune Diseases", [
        q("easy", "Systemic lupus erythematosus is classically associated with antibodies against:", "Nuclear antigens", ["Basement membrane collagen only", "LDL receptor", "Acetylcholine receptor only"], "ANA and anti-dsDNA/anti-Sm antibodies are characteristic of SLE."),
        q("easy", "The most specific antibody for SLE among common tests is:", "Anti-Sm", ["Antimitochondrial antibody", "Anti-centromere only", "IgE to pollen"], "Anti-Sm is highly specific, though not very sensitive, for SLE."),
        q("easy", "Sjögren syndrome primarily affects:", "Lacrimal and salivary glands", ["Adrenal cortex only", "Aortic media only", "Pulmonary arteries only"], "Autoimmune destruction of exocrine glands causes dry eyes and dry mouth."),
        q("moderate", "Anti-dsDNA antibodies in SLE correlate especially with:", "Lupus nephritis", ["Allergic rhinitis", "Keloid formation", "Familial hypercholesterolemia"], "Anti-dsDNA immune complexes are associated with renal involvement."),
        q("moderate", "Libman-Sacks endocarditis in SLE is characterized by:", "Sterile vegetations on either side of valve leaflets", ["Bacterial colonies on valves", "Calcified rheumatic commissures only", "Atherosclerotic plaques"], "SLE can cause sterile verrucous endocarditis."),
        q("moderate", "Sjögren syndrome increases risk of:", "Extranodal marginal zone B-cell lymphoma", ["Hodgkin lymphoma only", "Osteosarcoma", "Melanoma only"], "Chronic B-cell stimulation in Sjögren syndrome predisposes to MALT-type lymphoma."),
        q("moderate", "Systemic sclerosis is characterized by:", "Autoimmunity, vasculopathy, and excessive fibrosis", ["Pure IgE mast cell disease", "Only immune complex nephritis", "Only T-cell immunodeficiency"], "Scleroderma combines vascular injury, immune activation, and collagen deposition."),
        q("high", "A woman has photosensitive malar rash, arthritis, low complement, and proteinuria. Renal biopsy shows granular deposits of IgG and complement in glomeruli. Which mechanism best explains the nephritis?", "Type III immune complex disease due to anti-nuclear antibodies", ["Linear anti-GBM antibody disease", "IgE-mediated mast cell degranulation", "Dominant-negative collagen mutation"], "SLE nephritis is largely immune complex-mediated, producing granular deposits."),
        q("high", "A patient has dry eyes, dry mouth, parotid enlargement, anti-SSA antibodies, and a monoclonal B-cell proliferation in salivary tissue. Which long-term complication is most directly linked to the chronic autoimmune process?", "MALT lymphoma", ["Aortic dissection", "Pulmonary thromboembolism", "Fragile X syndrome"], "Sjögren syndrome may evolve into extranodal marginal zone lymphoma from chronic B-cell activation."),
        q("high", "A patient develops tight skin of the fingers, Raynaud phenomenon, dysphagia from esophageal fibrosis, and pulmonary hypertension. The disease involves endothelial injury and fibroblast activation rather than immune complex deposition alone. Which disease fits best?", "Systemic sclerosis", ["SLE", "Goodpasture syndrome", "Wiskott-Aldrich syndrome"], "Systemic sclerosis is marked by vasculopathy and progressive fibrosis of skin and organs."),
    ]),
    ("transplant", "Transplantation Immunology", [
        q("easy", "The major barrier to organ transplantation is mismatch in:", "HLA molecules", ["Albumin levels", "LDL receptors", "Mitochondrial DNA only"], "HLA polymorphism is the main determinant of graft recognition."),
        q("easy", "Hyperacute rejection is usually mediated by:", "Preformed anti-donor antibodies", ["New Th17 cells only", "IgE to pollen", "Amyloid deposition"], "Preexisting antibodies cause immediate endothelial injury and thrombosis."),
        q("easy", "Graft-versus-host disease occurs when:", "Donor T cells attack recipient tissues", ["Recipient antibodies attack donor RBCs only", "Amyloid deposits in graft vessels", "Mast cells release histamine"], "Immunocompetent donor T cells react against host antigens."),
        q("moderate", "Acute cellular rejection is mediated mainly by:", "T lymphocytes", ["IgE", "LDL", "C1 inhibitor"], "Recipient T cells attack graft parenchyma and vessels."),
        q("moderate", "Acute antibody-mediated rejection primarily targets:", "Graft endothelium", ["Recipient thymus only", "Donor neutrophil granules", "Host salivary ducts"], "Antibodies to donor antigens injure graft vessels through complement and inflammation."),
        q("moderate", "Chronic rejection is characterized by:", "Progressive vascular narrowing and interstitial fibrosis", ["Immediate widespread thrombosis at reperfusion", "Pure mast cell degranulation", "Only reversible edema"], "Chronic rejection causes graft ischemia and fibrosis over months to years."),
        q("moderate", "Direct allorecognition means recipient T cells recognize:", "Intact donor MHC molecules on donor APCs", ["Only donor peptides on recipient MHC", "Soluble IgE", "Amyloid fibrils"], "Direct recognition is a strong T-cell response to foreign MHC itself."),
        q("high", "Minutes after kidney transplantation, the graft becomes cyanotic and fails to perfuse. Histology shows neutrophils, fibrin thrombi, and endothelial injury. The recipient had circulating antibodies against donor blood group/HLA antigens. What is the rejection pattern?", "Hyperacute rejection", ["Chronic rejection", "Graft-versus-host disease", "Delayed-type hypersensitivity to tuberculin"], "Preformed antibodies cause immediate complement-mediated vascular thrombosis."),
        q("high", "Months after transplant, a patient develops gradual renal graft dysfunction. Biopsy shows intimal smooth muscle proliferation, luminal narrowing, tubular atrophy, and interstitial fibrosis. There is no sudden thrombosed graft. Which process is most likely?", "Chronic rejection", ["Hyperacute rejection", "Anaphylaxis", "Serum sickness"], "Chronic rejection is dominated by vascular occlusion and fibrosis."),
        q("high", "After bone marrow transplantation, a recipient develops rash, jaundice, diarrhea, and mucosal ulceration. The graft contains mature donor T cells, and the recipient is immunosuppressed. Which immunologic event is central?", "Donor T cells reacting against recipient antigens", ["Recipient IgE against donor mast cells", "Preformed recipient antibodies to kidney endothelium", "Immune complexes against basement membrane"], "GVHD occurs when donor T cells recognize host alloantigens."),
    ]),
    ("immunodeficiency", "Primary and Secondary Immunodeficiency Diseases", [
        q("easy", "Primary immunodeficiencies are most often caused by:", "Inherited defects in immune development or function", ["Only malnutrition", "Only HIV infection", "Only chemotherapy"], "Primary immunodeficiencies are genetic disorders of immune components."),
        q("easy", "Severe combined immunodeficiency involves defective:", "T-cell and B-cell immunity", ["Only complement C3", "Only neutrophil chemotaxis", "Only IgE responses"], "SCID severely impairs cellular and humoral immunity."),
        q("easy", "X-linked agammaglobulinemia is caused by mutation in:", "BTK", ["AIRE", "FBN1", "LDLR"], "BTK is required for B-cell maturation."),
        q("moderate", "DiGeorge syndrome causes T-cell deficiency because of:", "Thymic hypoplasia", ["BTK mutation", "C3 deficiency", "IgE overproduction"], "22q11.2 deletion impairs thymic development and T-cell maturation."),
        q("moderate", "Wiskott-Aldrich syndrome classically includes:", "Eczema, thrombocytopenia, and immunodeficiency", ["Aortic aneurysm, lens dislocation, and tall stature", "Dry eyes, dry mouth, and lymphoma only", "Hematuria and pulmonary hemorrhage"], "WAS affects cytoskeletal responses in hematopoietic cells."),
        q("moderate", "Chediak-Higashi syndrome is associated with:", "Defective lysosomal trafficking and giant granules", ["Absence of MHC class I", "LDL receptor deficiency", "IgE-mediated anaphylaxis"], "LYST mutation causes abnormal granule fusion and impaired microbial killing."),
        q("moderate", "C3 deficiency predisposes especially to:", "Recurrent pyogenic infections", ["Only viral warts", "Only amyloidosis", "Only autoimmune thyroiditis"], "C3 is central to opsonization and complement activation."),
        q("high", "An infant develops recurrent bacterial infections after maternal IgG wanes. Tonsils and lymph nodes are very small, mature B cells are absent, and serum immunoglobulins of all classes are markedly reduced. T-cell numbers are preserved. Which defect is most likely?", "X-linked agammaglobulinemia due to BTK mutation", ["DiGeorge syndrome", "Chronic granulomatous disease", "C1 inhibitor deficiency"], "BTK deficiency blocks pre-B-cell maturation, causing absent mature B cells and antibodies."),
        q("high", "A newborn has chronic diarrhea, thrush, Pneumocystis pneumonia, and failure to thrive. Both cellular immunity and antibody responses are poor, and lymphocyte numbers are very low. Which category best describes the disease?", "Severe combined immunodeficiency", ["Isolated IgA deficiency", "Type I hypersensitivity", "Secondary amyloidosis"], "SCID causes profound T-cell deficiency with secondary impairment of B-cell immunity."),
        q("high", "A child has recurrent staphylococcal abscesses and granulomas. Neutrophils ingest bacteria but cannot generate an oxidative burst on testing. Which immune defect is responsible?", "NADPH oxidase defect in chronic granulomatous disease", ["BTK deficiency", "AIRE mutation", "C3 nephritic factor"], "CGD impairs respiratory burst-dependent microbial killing."),
    ]),
    ("hiv", "HIV Infection and AIDS", [
        q("easy", "HIV primarily infects cells expressing:", "CD4 with chemokine coreceptors", ["CD8 only", "IgE receptor only", "LDL receptor only"], "HIV uses CD4 and CCR5 or CXCR4 to enter cells."),
        q("easy", "The defining immune defect in AIDS is loss of:", "CD4+ T cells", ["Platelets only", "Erythrocytes only", "Fibroblasts"], "Progressive CD4 T-cell depletion causes opportunistic infections and tumors."),
        q("easy", "HIV is a:", "Retrovirus", ["Prion", "DNA adenovirus", "Fungus"], "HIV is an RNA retrovirus that uses reverse transcriptase."),
        q("moderate", "CCR5-tropic HIV strains usually infect:", "Macrophages and memory T cells", ["Only red blood cells", "Only neutrophils", "Only platelets"], "CCR5 is used by many transmitted macrophage-tropic strains."),
        q("moderate", "Reverse transcriptase allows HIV to:", "Make DNA from viral RNA", ["Make antibody from DNA", "Digest complement", "Cross-link IgE"], "Reverse transcriptase converts RNA genome into DNA for integration."),
        q("moderate", "AIDS is diagnosed clinically by opportunistic infections or tumors, often when CD4 count falls below:", "200 cells/µL", ["2000 cells/µL", "20,000 cells/µL", "2 cells/µL only"], "CD4 counts below 200/µL are associated with AIDS-defining opportunistic disease."),
        q("moderate", "Pneumocystis jirovecii pneumonia in HIV reflects defective:", "Cell-mediated immunity", ["Platelet aggregation", "IgE-mediated allergy", "LDL uptake"], "T-cell depletion predisposes to opportunistic fungal pneumonia."),
        q("high", "Soon after HIV exposure, a patient has fever, rash, lymphadenopathy, high viremia, and a transient drop in CD4 cells. Symptoms improve, but virus persists in lymphoid tissues with ongoing replication. Which phase is this?", "Acute retroviral syndrome followed by clinical latency", ["Hyperacute graft rejection", "Type III serum sickness", "Primary amyloidosis"], "Primary HIV infection causes high viremia; latency is clinically silent but virologically active."),
        q("high", "An untreated HIV patient develops progressive weight loss, chronic diarrhea, oral candidiasis, and Kaposi sarcoma. CD4 count is 80/µL. Which mechanism best explains the broad susceptibility to infections and tumors?", "Severe depletion and dysfunction of CD4+ helper T cells", ["Excess IgE-mediated mast cell activation", "Isolated neutrophil oxidative burst defect", "Only complement C1 inhibitor deficiency"], "CD4 T cells coordinate macrophage, B-cell, and CTL responses; their loss cripples immunity."),
        q("high", "A person homozygous for a loss-of-function CCR5 mutation is highly resistant to infection by common transmitted HIV strains. Which step in the viral life cycle is impaired?", "Coreceptor-mediated viral entry", ["Reverse transcription after entry", "Integration after nuclear transport", "Viral budding from macrophages"], "CCR5 is a required entry coreceptor for many HIV strains."),
    ]),
    ("amyloid", "Amyloidosis", [
        q("easy", "Amyloid is composed of misfolded proteins arranged as:", "Beta-pleated sheets", ["Alpha-helical collagen", "DNA triplet repeats", "Lipid bilayers"], "Amyloid fibrils share beta-pleated sheet structure."),
        q("easy", "Congo red-stained amyloid shows what under polarized light?", "Apple-green birefringence", ["Blue-black granules", "Linear IgG fluorescence", "Acid-fast bacilli"], "Congo red produces apple-green birefringence with amyloid."),
        q("easy", "AL amyloid is derived from:", "Immunoglobulin light chains", ["Serum amyloid A", "Transthyretin only", "Beta-2 microglobulin only"], "AL amyloidosis is associated with plasma cell dyscrasias producing light chains."),
        q("moderate", "AA amyloid is derived from:", "Serum amyloid A", ["Ig light chain", "Calcitonin", "Atrial natriuretic factor"], "AA amyloidosis follows chronic inflammation with increased SAA production."),
        q("moderate", "A common cause of systemic reactive AA amyloidosis is:", "Chronic inflammatory disease", ["IgE-mediated urticaria", "Turner syndrome", "Acute anaphylaxis only"], "Persistent inflammation elevates SAA, predisposing to AA amyloid."),
        q("moderate", "The kidney in amyloidosis commonly presents with:", "Proteinuria or nephrotic syndrome", ["Pure hemarthrosis", "Lens dislocation", "Bronchospasm only"], "Amyloid deposition in glomeruli causes protein leakage."),
        q("moderate", "Dialysis-associated amyloidosis is related to accumulation of:", "Beta-2 microglobulin", ["IgE", "C3a", "Fibrillin-1"], "Beta-2 microglobulin can accumulate in long-term dialysis patients."),
        q("high", "A patient with multiple myeloma develops nephrotic-range proteinuria and restrictive cardiomyopathy. Tissue biopsy shows Congo red-positive deposits with apple-green birefringence composed of monoclonal light-chain fragments. Which amyloid type is present?", "AL amyloid", ["AA amyloid", "A beta amyloid", "ATTR amyloid"], "Plasma cell dyscrasias produce monoclonal light chains that form AL amyloid."),
        q("high", "A patient with long-standing rheumatoid arthritis develops enlarged waxy kidneys and heavy proteinuria. The amyloid fibrils are derived from an acute-phase reactant made by the liver during chronic inflammation. Which precursor protein is involved?", "Serum amyloid A", ["Immunoglobulin kappa light chain", "Transthyretin", "Beta-2 microglobulin"], "Chronic inflammation causes AA amyloidosis from SAA."),
        q("high", "An elderly patient develops restrictive cardiomyopathy from transthyretin deposition, without a plasma cell neoplasm or chronic inflammatory disorder. The fibrils still share beta-pleated sheet structure and Congo red positivity. Which category best fits?", "ATTR amyloidosis", ["AL amyloidosis", "AA amyloidosis", "Type III hypersensitivity"], "Transthyretin can form senile systemic or hereditary amyloid deposits, especially in heart."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if slug == "autoimmunity":
            continue
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch6-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 6 questions, got {len(chapter_questions)}")
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
    high_prompts = [q["prompt"] for q in chapter_questions if q["difficulty"] == "high"]
    if any(len(prompt.split()) < 24 for prompt in high_prompts):
        raise ValueError("High-level prompts should be longer, integrated questions")
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
    kept = [question for question in existing if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch6-"))]
    data["questions"] = kept + chapter_questions
    validate(chapter_questions, data["questions"])
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Removed {len(existing) - len(kept)} existing Chapter 6 questions")
    print(f"Added {len(chapter_questions)} Robbins Chapter 6 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
