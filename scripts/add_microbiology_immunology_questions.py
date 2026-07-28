import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Immunology"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("immunity-innate-acquired", "Immunity (Innate and Acquired)", [
        q("A child develops fever and neutrophil influx within hours of a skin wound before antibodies appear. This early defense is mainly:", "Innate immunity", ["Humoral memory", "Delayed-type hypersensitivity", "Active artificial immunity"], "Innate immunity is rapid, nonspecific, and uses barriers, phagocytes, complement, and inflammatory mediators."),
        q("A vaccinated person mounts a faster antibody response after exposure to the same virus. This is due to:", "Immunological memory", ["Toll-like receptor deletion", "Complement exhaustion", "Neutrophil chemotaxis"], "Adaptive immunity generates memory B and T cells that respond faster on re-exposure."),
        q("Natural killer cells kill virus-infected cells that have low MHC class I because they:", "Detect missing self", ["Recognize soluble antibody only", "Need antigen presentation on MHC II", "Produce immunoglobulin"], "NK cells are inhibited by normal MHC I; reduced MHC I removes inhibition."),
        q("A macrophage recognizes bacterial lipopolysaccharide through pattern recognition. The receptor family involved is:", "Toll-like receptors", ["T-cell receptors only", "B-cell receptors only", "Fc epsilon receptors"], "TLRs recognize conserved pathogen-associated molecular patterns."),
        q("A newborn receives maternal IgG through placenta. This protection is:", "Natural passive immunity", ["Natural active immunity", "Artificial active immunity", "Innate immunity only"], "Passive immunity transfers ready-made antibody without the infant generating memory."),
        q("A patient receives tetanus toxoid vaccine and later produces antitoxin. This is:", "Artificial active immunity", ["Artificial passive immunity", "Natural passive immunity", "Complement-mediated immunity"], "Vaccines induce the host's own adaptive response and memory."),
        q("A splenectomized patient is prone to pneumococcal sepsis because the spleen is important for:", "Clearing opsonized encapsulated bacteria", ["Producing all complement proteins", "Making neutrophils", "Destroying T cells"], "Splenic macrophages remove antibody/complement-opsonized encapsulated organisms."),
        q("The first immunoglobulin produced in a primary immune response is usually:", "IgM", ["IgE", "IgA", "IgG4"], "Naive B-cell responses begin with IgM before class switching."),
        q("A mucosal vaccine aims to increase protection at the intestinal surface. The antibody class most relevant is:", "Secretory IgA", ["IgD", "IgE", "IgM pentamer in serum"], "Secretory IgA protects mucosal surfaces by neutralization without major inflammation."),
        q("A patient with defective neutrophil oxidative burst has recurrent catalase-positive infections. The missing innate function is:", "Intracellular killing by reactive oxygen species", ["Antibody class switching", "MHC restriction", "Thymic selection"], "Respiratory burst defects impair phagocyte killing, as in chronic granulomatous disease."),
    ]),
    ("antigen", "Antigen", [
        q("A small drug molecule causes allergy only after binding host protein. The drug is acting as a:", "Hapten", ["Complete antigen", "Superantigen", "Adjuvant only"], "Haptens are too small to be immunogenic alone but become immunogenic when linked to carrier proteins."),
        q("A vaccine protein has many distinct sites recognized by different antibodies. Each recognized site is an:", "Epitope", ["Idiotype", "Isotype", "Allotype"], "An epitope is the specific antigenic determinant bound by antibody or T-cell receptor."),
        q("A toxin activates many T cells by bridging MHC II and TCR outside the peptide groove. This is a:", "Superantigen", ["Hapten", "Adjuvant", "T-independent antigen"], "Superantigens cause polyclonal T-cell activation and massive cytokine release."),
        q("Polysaccharide capsules in young children often produce weak memory because they are:", "T-independent antigens", ["T-dependent protein antigens", "Superantigens", "Autoantigens only"], "Pure polysaccharides activate B cells without strong T-cell help, producing poor memory in infants."),
        q("Conjugate vaccines work better in infants because polysaccharide antigen is linked to:", "Protein carrier that recruits T-cell help", ["Endotoxin lipid A", "Human albumin only", "Antibody Fc fragment"], "Protein conjugation converts a T-independent response into a T-dependent response with class switching and memory."),
        q("An antigen that induces tolerance rather than immunity when encountered in a specific context may be called:", "Tolerogen", ["Mitogen", "Opsonin", "Allotype"], "Antigen outcome depends on context, dose, route, and costimulation."),
        q("A B-cell epitope is commonly:", "Conformational or linear surface structure", ["Only peptide in MHC I groove", "Only intracellular processed peptide", "Only lipid A"], "B cells can recognize native surface shapes, while T cells recognize processed peptide-MHC."),
        q("T cells recognize antigen mainly as:", "Processed peptide presented by MHC molecules", ["Free soluble native antigen only", "Whole bacterium without APC", "Unprocessed carbohydrate only"], "TCRs recognize peptide-MHC complexes."),
        q("An adjuvant in a vaccine is added mainly to:", "Enhance innate activation and improve adaptive response", ["Destroy antigen immediately", "Prevent all inflammation", "Act as passive antibody"], "Adjuvants improve immunogenicity by stimulating innate signals and antigen presentation."),
        q("A cross-reactive antigen shared between microbe and host can contribute to:", "Autoimmune tissue injury by molecular mimicry", ["Immediate sterilization", "Loss of all antibody", "Complement absence"], "Molecular mimicry can trigger immune responses that also attack host tissues."),
    ]),
    ("antibody", "Antibody", [
        q("A patient with recurrent Giardia and respiratory infections has absent secretory antibody at mucosa. The deficient class is:", "IgA", ["IgE", "IgD", "IgG3"], "IgA is the major mucosal immunoglobulin and protects respiratory/GI surfaces."),
        q("The immunoglobulin best at crossing placenta is:", "IgG", ["IgM", "IgA", "IgE"], "IgG crosses placenta via FcRn and provides neonatal passive immunity."),
        q("A high IgM with low IgG, IgA, and IgE suggests a defect in:", "Class switching", ["V(D)J recombination only", "Complement C9", "Neutrophil chemotaxis"], "Class switch recombination changes heavy-chain constant region from IgM to other isotypes."),
        q("IgE mediates allergy by binding high-affinity receptors on:", "Mast cells and basophils", ["Red blood cells", "Platelets only", "Hepatocytes"], "IgE bound to Fc epsilon RI triggers degranulation after allergen cross-linking."),
        q("The antigen-binding site of an antibody is formed by:", "Variable regions of heavy and light chains", ["Fc constant region only", "J chain only", "Hinge carbohydrate only"], "Fab variable domains determine antigen specificity."),
        q("The Fc region is most important for:", "Effector functions such as complement activation and Fc receptor binding", ["Antigen specificity only", "DNA replication", "Somatic recombination only"], "Fc determines isotype-dependent effector functions."),
        q("IgM is efficient at complement activation because it:", "Forms a pentamer that binds C1q effectively", ["Crosses placenta best", "Is secreted as a dimer in saliva", "Binds mast cells"], "Pentameric IgM is a powerful classical pathway activator."),
        q("A monoclonal antibody preparation contains antibodies of:", "Single specificity from one B-cell clone", ["All possible specificities", "Only IgM from serum", "No Fc region ever"], "Monoclonal antibodies are clone-derived and target one antigenic specificity."),
        q("Affinity maturation occurs in germinal centers through:", "Somatic hypermutation and selection of higher-affinity B cells", ["Random neutrophil migration", "Complement lysis", "Thymic negative selection of B cells"], "Germinal center reactions improve antibody affinity."),
        q("Opsonization by IgG helps phagocytes because:", "Fc receptors bind antibody-coated microbes", ["IgG dissolves cell walls alone", "IgG blocks neutrophil adhesion", "IgG prevents complement"], "IgG Fc binds Fc gamma receptors on phagocytes to promote ingestion."),
    ]),
    ("antigen-antibody-reaction", "Antigen-antibody Reaction", [
        q("A Widal tube test showing visible clumping is based on:", "Agglutination", ["Precipitation", "Complement fixation only", "Neutralization only"], "Agglutination occurs when antibodies cross-link particulate antigens."),
        q("A ring precipitin test detects soluble antigen-antibody lattice formation. The principle is:", "Precipitation", ["Agglutination", "Opsonization", "Chemotaxis"], "Soluble antigen plus antibody forms visible precipitate at equivalence."),
        q("A false-negative precipitation test occurs with antibody excess. This is called:", "Prozone phenomenon", ["Postzone from antigen excess", "Hookworm effect", "Herd effect"], "Prozone is antibody excess preventing lattice formation."),
        q("A false-negative test due to antigen excess is called:", "Postzone phenomenon", ["Prozone phenomenon", "Opsonization", "Seroconversion"], "Postzone occurs when excess antigen prevents cross-linking."),
        q("ELISA detection of patient IgM against dengue most directly indicates:", "Recent or current infection", ["Remote infection only", "Absence of immune response", "Culture positivity"], "Pathogen-specific IgM usually suggests recent infection, though timing and cross-reactivity matter."),
        q("Western blot is useful because it:", "Detects antibodies against separated specific proteins", ["Measures bacterial motility", "Counts colonies", "Tests antibiotic MIC directly"], "Western blot separates antigens by size then detects specific antibody binding."),
        q("A neutralization test demonstrates antibody that:", "Blocks biological activity or infectivity of toxin/virus", ["Only clumps red cells", "Only fixes complement", "Only stains capsules"], "Neutralizing antibodies prevent toxin or virus from binding/entering cells."),
        q("Immunofluorescence on tissue biopsy helps detect:", "Antigen or antibody localization using fluorescent labels", ["Bacterial growth rate", "Sugar fermentation", "Minimum bactericidal concentration"], "Fluorescent-tagged antibodies visualize immune targets in cells/tissues."),
        q("Latex agglutination for cryptococcal antigen detects:", "Soluble capsular antigen attached to latex particle reaction", ["Fungal culture only", "Antibiotic susceptibility", "T-cell memory"], "Latex particles coated with antibody agglutinate in presence of antigen."),
        q("Paired sera showing a fourfold rise in antibody titer indicates:", "Recent infection or significant immune response", ["No exposure", "Lab contamination always", "Only passive immunity"], "A fourfold rise between acute and convalescent samples supports recent infection."),
    ]),
    ("complement", "Complement", [
        q("A patient with recurrent Neisseria meningitidis infections most likely has deficiency of:", "C5-C9 terminal complement components", ["C1 inhibitor", "Factor H only", "MBL only"], "Terminal complement forms MAC, critical for Neisseria killing."),
        q("Hereditary angioedema is due to deficiency of:", "C1 esterase inhibitor", ["C3", "C5", "Properdin"], "C1 inhibitor deficiency causes excess bradykinin-mediated swelling."),
        q("The most important opsonin generated by complement is:", "C3b", ["C5a", "C3a", "C9"], "C3b coats microbes and promotes phagocytosis."),
        q("The strongest complement-derived neutrophil chemoattractant is:", "C5a", ["C9", "C1q", "Factor B"], "C5a is a potent chemoattractant and anaphylatoxin."),
        q("Classical complement activation is initiated by:", "Antigen-antibody complexes binding C1q", ["Microbial surfaces binding factor B first", "Mannose-binding lectin only", "C5 convertase alone"], "The classical pathway is triggered mainly by IgG or IgM immune complexes."),
        q("The lectin pathway begins when:", "Mannose-binding lectin binds microbial carbohydrates", ["IgE binds mast cells", "C9 polymerizes spontaneously", "Factor H binds host cells"], "MBL recognizes mannose-rich microbial surfaces and activates MASPs."),
        q("Alternative pathway activation is amplified on microbial surfaces because:", "C3b is not rapidly inactivated without host regulatory proteins", ["IgM is required", "C1q binds endotoxin", "C1 inhibitor is absent only in microbes"], "Host cells express complement regulators; microbial surfaces favor amplification."),
        q("Paroxysmal nocturnal hemoglobinuria involves complement-mediated RBC lysis due to deficiency of:", "GPI-anchored CD55 and CD59", ["IgA", "C5a receptor", "C1q"], "Loss of CD55/CD59 permits complement attack on blood cells."),
        q("Eculizumab increases susceptibility to meningococcal infection because it blocks:", "C5 cleavage and MAC formation", ["C3 synthesis", "C1 inhibitor", "IgG class switching"], "C5 inhibition prevents terminal complement activity; meningococcal vaccination is needed."),
        q("C3 deficiency is severe because C3 is central to:", "All complement pathways and opsonization", ["Only IgE allergy", "Only T-cell selection", "Only NK-cell inhibition"], "C3 is the convergence point for classical, lectin, and alternative pathways."),
    ]),
    ("immune-system-components", "Components of Immune System: Organs, Cells and Products", [
        q("T cells mature and undergo selection in the:", "Thymus", ["Spleen", "Bone marrow after antigen only", "Lymph node germinal center"], "The thymus is the primary lymphoid organ for T-cell maturation."),
        q("B cells in humans primarily mature in:", "Bone marrow", ["Thymus", "Spleen red pulp", "Appendix only"], "Bone marrow is the primary lymphoid organ for B-cell development."),
        q("A lymph node filters:", "Lymph draining from tissues", ["Arterial blood", "Bile", "CSF only"], "Lymph nodes sample tissue lymph for antigen and immune activation."),
        q("The spleen is especially important for filtering:", "Blood-borne antigens and encapsulated bacteria", ["Airway mucus", "Urine", "Skin keratin"], "Splenic macrophages and marginal zone B cells respond to blood-borne microbes."),
        q("Professional antigen-presenting cells include:", "Dendritic cells, macrophages, and B cells", ["Red blood cells only", "Platelets only", "Neurons"], "Professional APCs express MHC II and costimulatory molecules."),
        q("Naive T cells require antigen presentation plus costimulation; the classic costimulatory pair is:", "B7 on APC binding CD28 on T cell", ["CD40L binding IgE", "C5a binding C9", "MHC I binding antibody"], "Without costimulation, T cells may become anergic."),
        q("IL-2 is important after T-cell activation because it:", "Drives T-cell proliferation", ["Kills bacteria directly", "Forms MAC", "Neutralizes toxins"], "IL-2 is a key autocrine growth factor for activated T cells."),
        q("Plasma cells are differentiated B cells specialized for:", "Antibody secretion", ["Antigen phagocytosis only", "Complement synthesis only", "Histamine release"], "Plasma cells produce large amounts of immunoglobulin."),
        q("Mast cells contribute to immediate allergy by releasing:", "Histamine and other granule mediators", ["IgG only", "C3b only", "Thymosin"], "IgE cross-linking triggers mast cell degranulation."),
        q("Dendritic cells are particularly important because they:", "Prime naive T cells in lymphoid organs", ["Produce all antibodies", "Carry oxygen", "Lyse RBCs"], "Dendritic cells bridge innate sensing and adaptive T-cell activation."),
    ]),
    ("immune-responses", "Immune Responses: Cell-mediated and Antibody-mediated", [
        q("A patient with intracellular viral infection needs cytotoxic killing of infected cells. The key effector cell is:", "CD8-positive T cell", ["Plasma cell", "Eosinophil only", "Basophil"], "CD8 T cells recognize peptide-MHC I and kill infected cells."),
        q("Exogenous bacterial antigen taken up by a macrophage is usually presented to CD4 T cells on:", "MHC class II", ["MHC class I only", "CD1 only", "Fc receptor"], "MHC II presents extracellularly derived peptides to CD4 T cells."),
        q("Endogenous viral peptides in nucleated cells are presented on:", "MHC class I", ["MHC class II only", "IgE", "C3b"], "MHC I presents intracellular peptides to CD8 T cells."),
        q("Th1 responses are especially important for:", "Macrophage activation against intracellular pathogens", ["IgE-mediated helminth allergy only", "Mast cell degranulation only", "Mucus secretion only"], "Th1 cells produce IFN-gamma and support cell-mediated immunity."),
        q("Th2 responses promote defense against helminths and allergy through:", "IL-4, IL-5, and IgE/eosinophil responses", ["IL-2 only cytotoxicity", "C3b deposition only", "NK missing-self only"], "Th2 cytokines drive IgE class switching and eosinophil activation."),
        q("Th17 cells are important for mucocutaneous defense by recruiting:", "Neutrophils", ["Red cells", "Platelets", "B cells only"], "Th17 cytokines recruit neutrophils and support barrier immunity."),
        q("Regulatory T cells maintain tolerance partly through:", "IL-10, TGF-beta, and suppression of autoreactive responses", ["Histamine release", "C5b-9 formation", "IgE cross-linking"], "Tregs reduce excessive and self-reactive immune activation."),
        q("A secondary antibody response differs from primary response by:", "Faster, higher-affinity, class-switched antibody production", ["Only IgM and no memory", "No plasma cells", "Absent antigen specificity"], "Memory B cells generate rapid, high-affinity class-switched responses."),
        q("Germinal centers are sites of:", "Class switching and affinity maturation", ["T-cell thymic selection", "Complement MAC assembly", "Neutrophil killing"], "B-cell maturation occurs in germinal centers with T-cell help."),
        q("Anergy occurs when a lymphocyte recognizes antigen without:", "Appropriate costimulation", ["Oxygen", "Hemoglobin", "Complement C9"], "Lack of costimulation can functionally silence lymphocytes and maintain tolerance."),
    ]),
    ("hypersensitivity", "Hypersensitivity", [
        q("A patient develops urticaria, wheeze, and hypotension minutes after penicillin. This is:", "Type I hypersensitivity", ["Type II hypersensitivity", "Type III hypersensitivity", "Type IV hypersensitivity"], "Immediate hypersensitivity is IgE-mediated mast cell degranulation."),
        q("Hemolytic disease of newborn due to anti-Rh IgG is:", "Type II hypersensitivity", ["Type I", "Type III", "Type IV"], "Type II reactions involve antibodies against cell surface antigens causing cell injury."),
        q("Serum sickness after antiserum presents with fever, rash, arthralgia, and proteinuria. The mechanism is:", "Immune complex deposition", ["IgE mast cell degranulation", "T-cell granuloma only", "Direct toxin effect"], "Type III hypersensitivity is mediated by circulating immune complexes."),
        q("A tuberculin skin test becomes indurated after 48 hours. This is:", "Type IV delayed hypersensitivity", ["Type I immediate", "Type II cytotoxic", "Type III Arthus"], "Type IV reactions are T-cell mediated and delayed."),
        q("An Arthus reaction after intradermal antigen in an immune person is:", "Localized type III hypersensitivity", ["Systemic type I", "Type II receptor blockade", "T-cell anergy"], "Local immune complex formation activates complement and inflammation."),
        q("Contact dermatitis from nickel jewelry is mediated mainly by:", "T cells", ["IgE", "IgM against RBCs", "C5-C9 only"], "Contact dermatitis is a type IV T-cell-mediated reaction."),
        q("Graves disease is a type II hypersensitivity variant because antibody:", "Stimulates TSH receptors", ["Deposits immune complexes in glomeruli", "Activates mast cell IgE", "Kills by CD8 only"], "Antireceptor antibodies can stimulate or block receptor function."),
        q("Myasthenia gravis is caused by antibodies that:", "Block or destroy acetylcholine receptors", ["Stimulate TSH receptors", "Deposit in alveoli", "Activate IgE on mast cells"], "Type II antireceptor antibodies impair neuromuscular transmission."),
        q("Anaphylaxis is treated first with epinephrine because it:", "Reverses bronchospasm, edema, and hypotension through adrenergic effects", ["Neutralizes antigen directly", "Destroys IgE permanently", "Blocks complement C3"], "Epinephrine is lifesaving in anaphylaxis."),
        q("Atopy means:", "Genetic tendency to produce IgE responses to common environmental allergens", ["Complete absence of complement", "Only immune complex disease", "Failure of T-cell maturation"], "Atopy predisposes to allergic rhinitis, asthma, and eczema."),
    ]),
    ("autoimmunity", "Autoimmunity", [
        q("A patient develops rheumatic fever after streptococcal pharyngitis. The autoimmune mechanism is:", "Molecular mimicry", ["Hapten-carrier allergy only", "Complement deficiency", "Superantigen tolerance"], "Cross-reactive antibodies/T cells against streptococcal and host antigens cause injury."),
        q("Failure to delete strongly self-reactive T cells in thymus is failure of:", "Central tolerance", ["Opsonization", "Class switching", "Alternative complement pathway"], "Central tolerance removes many autoreactive lymphocytes during development."),
        q("Regulatory T-cell dysfunction can promote autoimmunity because Tregs:", "Suppress self-reactive immune responses", ["Produce all antibodies", "Lyse bacteria by MAC", "Carry antigen in RBCs"], "Tregs maintain peripheral tolerance."),
        q("SLE is characterized by immune complexes and autoantibodies against:", "Nuclear antigens", ["Acetylcholine receptors only", "TSH receptors only", "Basement membrane collagen only"], "ANA and anti-dsDNA/anti-Sm antibodies are classic in SLE."),
        q("Anti-dsDNA titers in SLE are clinically useful because they correlate with:", "Disease activity and lupus nephritis risk", ["IgE allergy only", "TB exposure", "HIV viral load"], "Anti-dsDNA is relatively specific and often tracks renal disease activity."),
        q("Type 1 diabetes mellitus results from autoimmune destruction of:", "Pancreatic beta cells", ["Adrenal medulla", "Thyroid parafollicular cells", "Gastric chief cells"], "T-cell-mediated beta-cell destruction causes insulin deficiency."),
        q("Hashimoto thyroiditis commonly involves antibodies against:", "Thyroid peroxidase", ["TSH receptor stimulating only", "Intrinsic factor only", "Desmoglein"], "Anti-TPO and anti-thyroglobulin antibodies support autoimmune thyroiditis."),
        q("Pemphigus vulgaris is caused by autoantibodies against:", "Desmogleins", ["Hemidesmosomes", "Acetylcholine receptor", "Mitochondrial DNA"], "Anti-desmoglein antibodies disrupt keratinocyte adhesion causing flaccid blisters."),
        q("Goodpasture syndrome involves antibodies against:", "Glomerular and alveolar basement membrane", ["Nuclear ribonucleoprotein", "Platelet factor 4", "IgE Fc receptor"], "Anti-GBM antibodies cause pulmonary hemorrhage and glomerulonephritis."),
        q("Epitope spreading in chronic autoimmunity means:", "Immune response expands from initial antigenic targets to additional self epitopes", ["Antibody becomes less specific only", "Antigens disappear", "Complement stops"], "Tissue injury can expose new self-antigens and broaden autoimmune responses."),
    ]),
    ("immunodeficiency-disorders", "Immunodeficiency Disorders", [
        q("A boy has recurrent bacterial infections and absent tonsils with very low immunoglobulins. The likely disorder is:", "X-linked agammaglobulinemia", ["DiGeorge syndrome", "Chronic granulomatous disease", "Chediak-Higashi syndrome"], "BTK defect blocks B-cell maturation, causing absent mature B cells and antibodies."),
        q("A child with thymic aplasia, hypocalcemia, and recurrent viral/fungal infections has:", "DiGeorge syndrome", ["Bruton agammaglobulinemia", "Selective IgA deficiency", "Leukocyte adhesion deficiency"], "DiGeorge syndrome impairs T-cell development due to thymic hypoplasia/aplasia."),
        q("Recurrent mucosal infections with Giardia and anaphylaxis to blood products suggest:", "Selective IgA deficiency", ["C5 deficiency", "SCID only", "Hyper-IgE syndrome"], "IgA deficiency affects mucosal immunity and can cause anti-IgA transfusion reactions."),
        q("Delayed separation of umbilical cord and absent pus formation suggests:", "Leukocyte adhesion deficiency", ["Chediak-Higashi", "XLA", "C1 inhibitor deficiency"], "LAD impairs neutrophil adhesion and migration into tissues."),
        q("Recurrent catalase-positive infections with granuloma formation suggest:", "Chronic granulomatous disease", ["C5-C9 deficiency", "Selective IgA deficiency", "AIDS only"], "CGD is due to defective NADPH oxidase respiratory burst."),
        q("Partial albinism, neuropathy, and giant granules in leukocytes suggest:", "Chediak-Higashi syndrome", ["DiGeorge syndrome", "SCID", "Hyper-IgM due to CD40L"], "Chediak-Higashi involves lysosomal trafficking defects."),
        q("A child with eczema, recurrent staphylococcal abscesses, and very high IgE has:", "Hyper-IgE syndrome", ["XLA", "C3 deficiency", "DiGeorge syndrome"], "STAT3-related hyper-IgE causes eczema, cold abscesses, and high IgE."),
        q("Severe combined immunodeficiency causes:", "Defective cellular and humoral immunity", ["Only complement terminal pathway loss", "Only IgA deficiency", "Only neutrophil chemotaxis"], "SCID affects T-cell function and secondarily B-cell responses."),
        q("HIV predisposes to opportunistic infections mainly by depleting:", "CD4 T cells", ["Platelets", "Red cells", "Eosinophils only"], "CD4 T-cell loss impairs cellular immunity and macrophage/B-cell help."),
        q("C3 deficiency causes severe recurrent bacterial infections because C3 is required for:", "Opsonization and complement pathway convergence", ["IgE class switching only", "T-cell thymic selection", "NK-cell missing-self"], "C3b opsonization is central to bacterial clearance."),
    ]),
    ("transplant-cancer-immunology", "Transplant and Cancer Immunology", [
        q("Hyperacute graft rejection within minutes is caused by:", "Preformed anti-donor antibodies", ["New T-cell priming over months", "Tumor immune escape", "IgE allergy"], "Preexisting antibodies activate complement and thrombose graft vessels."),
        q("Acute cellular transplant rejection is mediated mainly by:", "T cells recognizing donor alloantigens", ["IgE on mast cells", "C5-C9 deficiency", "Eosinophils against helminths"], "T cells attack graft tissue through direct/indirect allorecognition."),
        q("Chronic graft rejection usually presents as:", "Progressive vascular narrowing and fibrosis", ["Immediate anaphylaxis", "Only urticaria", "Transient fever with no organ injury"], "Chronic rejection involves vascular and fibrotic remodeling over time."),
        q("HLA matching is most important because HLA molecules:", "Present antigen and are major targets of allorecognition", ["Are antibiotics", "Make red cells", "Neutralize toxins"], "HLA differences drive transplant immune responses."),
        q("Graft-versus-host disease occurs when donor immune cells:", "Attack recipient tissues", ["Are destroyed by recipient antibodies only", "Fail to engraft platelets", "Make insulin"], "GVHD is classically after hematopoietic stem cell transplantation."),
        q("A tumor downregulates MHC class I to escape CD8 T cells. Which immune cell may recognize this missing self?", "Natural killer cell", ["Plasma cell only", "Basophil", "Red blood cell"], "NK cells detect reduced MHC I expression."),
        q("PD-1 checkpoint inhibitors improve cancer immunity by:", "Releasing inhibitory brakes on T cells", ["Directly alkylating DNA", "Blocking folate", "Destroying all B cells"], "Checkpoint blockade enhances antitumor T-cell activity."),
        q("Immune-related colitis after checkpoint inhibitor therapy results from:", "Loss of peripheral immune tolerance", ["Bacterial endotoxin contamination only", "Complement C9 deficiency", "IgA absence"], "Checkpoint blockade can cause autoimmune-like inflammation."),
        q("Tumor antigens generated by mutated cancer genes are called:", "Neoantigens", ["Allotypes", "Haptens only", "Adjuvants"], "Neoantigens arise from tumor-specific mutations and can be immunogenic."),
        q("CAR T cells are engineered to:", "Recognize tumor antigens through synthetic receptors", ["Secrete only antibiotics", "Replace complement", "Prevent all cytokine release"], "CAR T therapy gives T cells antibody-like antigen recognition plus activation domains."),
    ]),
    ("immunoprophylaxis", "Immunoprophylaxis", [
        q("BCG is an example of which vaccine type?", "Live attenuated vaccine", ["Killed whole-cell vaccine", "Toxoid", "Subunit polysaccharide only"], "BCG is live attenuated Mycobacterium bovis."),
        q("Tetanus vaccine protects by inducing antibodies against:", "Toxoid", ["Capsule", "Endotoxin lipid A", "Flagella only"], "Tetanus toxoid is inactivated toxin that induces neutralizing antitoxin."),
        q("Hepatitis B vaccine is a:", "Recombinant subunit vaccine", ["Live attenuated vaccine", "Toxoid", "Killed bacterial vaccine"], "HBV vaccine contains recombinant HBsAg."),
        q("A conjugate pneumococcal vaccine is preferred in infants because it:", "Induces T-dependent memory to polysaccharide antigen", ["Avoids antibody production", "Contains live pneumococci", "Works only by passive immunity"], "Protein conjugation improves infant responses to polysaccharide capsules."),
        q("Rabies post-exposure prophylaxis in an unimmunized person includes vaccine plus immunoglobulin because:", "Passive antibody gives immediate protection while vaccine induces active immunity", ["Vaccine acts instantly as antibody", "Immunoglobulin creates memory", "Both are antibiotics"], "PEP combines immediate neutralization with long-term active response."),
        q("Cold chain failure can make vaccines ineffective because many vaccines:", "Lose potency with improper temperature exposure", ["Become antibiotics", "Turn into live pathogens always", "Lose all labels only"], "Vaccine potency depends on proper storage and transport."),
        q("Herd immunity from vaccination protects a community by:", "Reducing transmission chains", ["Making pathogens extinct in every animal", "Treating active disease", "Increasing susceptibility"], "High population immunity protects vulnerable individuals by limiting spread."),
        q("Adverse event following immunization should be investigated because:", "Temporal association does not always prove causation", ["All events are vaccine caused", "No event can be coincidental", "Vaccines have no monitoring"], "AEFI surveillance distinguishes coincidental, programmatic, anxiety-related, and vaccine-related events."),
        q("Live vaccines are generally contraindicated in:", "Severe immunosuppression", ["Healthy adults", "Mild local eczema only", "Past antibiotic use"], "Live attenuated organisms may cause disease in severely immunocompromised hosts."),
        q("Booster doses are given to:", "Restore or enhance waning immune memory and antibody levels", ["Erase memory cells", "Prevent antigen presentation", "Replace innate immunity"], "Boosters re-stimulate immune memory and improve protection."),
    ]),
]


def main():
    questions = []
    for topic_index, (slug, topic, rows) in enumerate(TOPICS):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        for question_index, row in enumerate(rows, 1):
            options = list(row["wrong"])
            answer_index = (topic_index + question_index - 1) % 4
            options.insert(answer_index, row["answer"])
            questions.append({**BASE, "id": f"micro-immunology-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "microbiology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 12 or len(questions) != 120:
        raise AssertionError(f"Expected 12 topics and 120 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 120:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
