import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Respiratory Tract Infections"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("respiratory-syndromes", "Infective Syndromes of Respiratory Tract", [
        q("A patient has cough, fever, pleuritic chest pain, bronchial breath sounds, and lobar consolidation on X-ray. The syndrome is:", "Pneumonia", ["Rhinitis", "Epiglottitis only", "Otitis externa"], "Parenchymal lung infection with consolidation, fever, and respiratory symptoms defines pneumonia."),
        q("A child has inspiratory stridor, barking cough, and subglottic narrowing. The syndrome is:", "Croup", ["Bronchiolitis", "Lobar pneumonia", "Sinusitis"], "Croup is laryngotracheobronchitis, commonly viral, causing barking cough and stridor."),
        q("An infant has wheeze, tachypnea, and hyperinflation during winter. The syndrome is most consistent with:", "Bronchiolitis", ["Diphtheria", "Tuberculosis meningitis", "Lobar pneumonia only"], "Bronchiolitis affects small airways in infants, often due to RSV."),
        q("A patient with severe sore throat, drooling, tripod posture, and muffled voice needs urgent airway assessment for:", "Epiglottitis", ["Common cold", "Otitis media", "Atypical pneumonia"], "Epiglottitis can rapidly obstruct the airway."),
        q("Ventilator-associated pneumonia is usually defined as pneumonia occurring:", "More than 48 hours after endotracheal intubation", ["Before hospital admission", "Only after discharge", "Only in neonates"], "VAP develops after mechanical ventilation exposure and has device-associated risk factors."),
        q("Aspiration pneumonia classically involves:", "Dependent lung segments and anaerobic/oral flora risk", ["Only upper lobes in all patients", "No bacteria", "Only viruses"], "Aspiration introduces oropharyngeal/gastric contents into dependent lung areas."),
        q("A chronic cough for weeks with weight loss, night sweats, and hemoptysis should prompt testing for:", "Pulmonary tuberculosis", ["Acute rhinovirus only", "Food poisoning", "Tetanus"], "Chronic constitutional symptoms with hemoptysis are classic for TB evaluation."),
        q("Sinusitis following viral URI is likely bacterial when symptoms:", "Persist beyond expected course, worsen after improvement, or are severe", ["Last 12 hours only", "Include sneezing alone", "Resolve completely"], "Persistent, severe, or double-worsening symptoms support bacterial sinusitis."),
        q("Community-acquired pneumonia severity assessment helps decide:", "Outpatient versus inpatient/ICU management", ["Whether lungs are sterile", "Vaccine type only", "Whether Gram stain is illegal"], "Severity scores and clinical judgment guide site of care and empiric therapy."),
        q("In pneumonia, sputum Gram stain is most useful when the specimen has:", "Many neutrophils and few squamous epithelial cells", ["Many squamous epithelial cells", "Only saliva", "No cells at all"], "A good lower respiratory specimen has inflammatory cells and minimal oral contamination."),
    ]),
    ("bacterial-pharyngitis", "Bacterial Pharyngitis: Streptococcus pyogenes Pharyngitis, Diphtheria and Others", [
        q("A school child has fever, tonsillar exudates, tender anterior cervical nodes, and no cough. The key bacterial cause is:", "Streptococcus pyogenes", ["Mycoplasma pneumoniae", "Klebsiella pneumoniae", "Pseudomonas aeruginosa"], "Group A streptococcus causes exudative pharyngitis and can lead to rheumatic fever."),
        q("Treating confirmed streptococcal pharyngitis prevents:", "Acute rheumatic fever", ["Post-streptococcal glomerulonephritis reliably", "Diphtheria", "Measles"], "Timely penicillin therapy prevents rheumatic fever but not consistently PSGN."),
        q("A gray adherent pharyngeal pseudomembrane that bleeds on removal suggests:", "Diphtheria", ["Scarlet fever", "Infectious mononucleosis", "Pertussis"], "Corynebacterium diphtheriae produces a tough pseudomembrane and systemic toxin effects."),
        q("Diphtheria toxin inhibits protein synthesis by:", "ADP-ribosylating elongation factor-2", ["Blocking 30S ribosome", "Cleaving SNARE proteins", "Increasing cAMP"], "Diphtheria toxin inactivates EF-2, stopping host protein synthesis."),
        q("The most urgent specific therapy in suspected respiratory diphtheria is:", "Diphtheria antitoxin plus antibiotics", ["Antibiotics alone after culture", "Steroids only", "No treatment until PCR"], "Antitoxin neutralizes unbound toxin and must not wait for lab confirmation."),
        q("Albert stain in diphtheria demonstrates:", "Metachromatic granules", ["Acid-fast bacilli", "Capsule swelling", "Germ tubes"], "C. diphtheriae contains volutin/metachromatic granules."),
        q("Toxigenicity of C. diphtheriae depends on:", "Lysogenic beta-phage carrying tox gene", ["Plasmid mecA", "Vi antigen", "M protein"], "Only strains lysogenized with tox-bearing phage produce diphtheria toxin."),
        q("Scarlet fever rash in streptococcal pharyngitis is mediated by:", "Erythrogenic pyrogenic exotoxin", ["Pneumolysin", "Diphtheria toxin", "Pertussis toxin"], "Streptococcal pyrogenic exotoxins act as superantigens causing rash."),
        q("A throat carrier of C. diphtheriae matters epidemiologically because:", "Transmission can occur even without severe disease", ["Carriers never transmit", "Only blood spreads diphtheria", "Vaccination treats carriers"], "Carriers can maintain spread; contacts need evaluation and prophylaxis."),
        q("A positive rapid antigen test for group A strep detects:", "Streptococcal antigen from throat swab", ["ASO antibody only", "Diphtheria toxin", "Viral RNA"], "RADT identifies GAS antigen and supports targeted treatment."),
    ]),
    ("lobar-pneumonia", "Bacterial Lobar Pneumonia: Pneumococcal Pneumonia, Haemophilus influenzae Pneumonia and Others", [
        q("Rusty sputum, lobar consolidation, and lancet-shaped Gram-positive diplococci suggest:", "Streptococcus pneumoniae", ["Haemophilus influenzae", "Mycoplasma pneumoniae", "Legionella pneumophila"], "Pneumococcus is the classic cause of lobar pneumonia with rusty sputum."),
        q("The major virulence factor of Streptococcus pneumoniae is:", "Polysaccharide capsule", ["M protein", "Exotoxin A", "Vi antigen"], "Capsule prevents phagocytosis and defines serotypes."),
        q("Optochin sensitivity and bile solubility help identify:", "Streptococcus pneumoniae", ["Viridans streptococci", "S. pyogenes", "Enterococcus"], "Pneumococcus is optochin sensitive and bile soluble."),
        q("Pneumococcal vaccine is especially important in asplenic patients because they have impaired clearance of:", "Encapsulated bacteria", ["Dermatophytes", "Nonenveloped viruses", "Helminths only"], "The spleen clears opsonized encapsulated organisms."),
        q("Haemophilus influenzae requires which growth factors?", "X and V factors", ["Only factor VIII", "Coagulase", "Bile salts"], "H. influenzae requires hemin (X) and NAD (V)."),
        q("Satellitism of H. influenzae around S. aureus occurs because S. aureus supplies:", "V factor (NAD)", ["Mycolic acid", "Pneumolysin", "Capsular antigen"], "S. aureus provides NAD, supporting H. influenzae growth on blood agar."),
        q("Hib vaccine protects against invasive disease by targeting:", "Polyribosylribitol phosphate capsule", ["Lipid A", "Pili only", "M protein"], "Type b capsule PRP is the vaccine antigen, conjugated to protein."),
        q("Klebsiella pneumoniae classically causes pneumonia with:", "Thick currant jelly sputum", ["Rice-water sputum", "Whooping cough", "Pseudomembrane"], "Klebsiella is encapsulated and can cause necrotizing pneumonia with bloody mucoid sputum."),
        q("Staphylococcus aureus pneumonia after influenza is important because it can cause:", "Necrotizing pneumonia and abscesses", ["Atypical interstitial pneumonia only", "No cavitation", "Diphtheria"], "Post-influenza S. aureus pneumonia may be severe and necrotizing."),
        q("A good empiric pneumonia regimen is chosen based on:", "Likely pathogen, severity, comorbidity, and local resistance", ["Sputum color only", "Patient zodiac", "Only Gram stain morphology in all cases"], "CAP therapy depends on clinical setting and resistance epidemiology."),
    ]),
    ("atypical-pneumonia", "Bacterial Atypical (Interstitial) Pneumonia: Mycoplasma, Chlamydia, Legionella and Others", [
        q("A young adult has dry cough, low-grade fever, and interstitial infiltrates; cold agglutinins are positive. The likely agent is:", "Mycoplasma pneumoniae", ["S. pneumoniae", "Klebsiella pneumoniae", "H. influenzae"], "Mycoplasma causes walking pneumonia and can induce cold agglutinins."),
        q("Mycoplasma pneumoniae lacks:", "Cell wall", ["Cell membrane", "Ribosomes", "DNA"], "Absence of cell wall explains beta-lactam resistance and pleomorphism."),
        q("Beta-lactams fail in Mycoplasma pneumonia because:", "There is no peptidoglycan target", ["It produces capsule only", "It is a virus", "It lives only extracellularly in stool"], "Beta-lactams require bacterial cell wall synthesis targets."),
        q("Legionella pneumonia with diarrhea, hyponatremia, and hotel water exposure is diagnosed rapidly by:", "Urinary antigen test for L. pneumophila serogroup 1", ["Widal test", "ASO titer", "India ink"], "Urinary antigen is a common rapid test but mainly detects serogroup 1."),
        q("Legionella grows on:", "Buffered charcoal yeast extract agar", ["MacConkey agar only", "Loeffler serum slope", "Lowenstein-Jensen only"], "BCYE agar with cysteine and iron supports Legionella."),
        q("Legionella survives in the environment within:", "Amoebae and biofilms in water systems", ["Mosquito salivary glands", "Human RBCs", "Soil spores only"], "Water systems and amoebae are important reservoirs."),
        q("Chlamydia pneumoniae is an obligate intracellular bacterium because it:", "Depends on host cell ATP/metabolism", ["Forms spores", "Has no DNA", "Is a fungus"], "Chlamydiae replicate intracellularly with elementary and reticulate bodies."),
        q("Psittacosis after bird exposure is caused by:", "Chlamydia psittaci", ["Chlamydia trachomatis D-K", "Coxiella burnetii", "Bordetella pertussis"], "C. psittaci causes atypical pneumonia linked to birds."),
        q("Macrolides or doxycycline cover atypical pneumonia because they:", "Act on intracellular or cell-wall-deficient pathogens", ["Only treat encapsulated pneumococci", "Block beta-lactamase", "Sterilize water systems"], "Atypicals require agents active intracellularly and not dependent on cell wall targets."),
        q("Q fever pneumonia after livestock exposure is due to:", "Coxiella burnetii", ["Legionella pneumophila", "Mycoplasma hominis", "Bacillus anthracis"], "Coxiella causes atypical pneumonia/hepatitis and is linked to farm animals/birth products."),
    ]),
    ("tuberculosis-ntm", "Tuberculosis and Nontuberculous Mycobacteria Infections", [
        q("A patient has chronic cough, fever, night sweats, weight loss, and upper-lobe cavitation. The likely diagnosis is:", "Pulmonary tuberculosis", ["Acute bronchiolitis", "Diphtheria", "Pertussis"], "Reactivation TB favors upper lobes and causes chronic constitutional symptoms."),
        q("Acid-fastness of Mycobacterium tuberculosis is due to:", "Mycolic acid-rich cell wall", ["Polysaccharide capsule", "M protein", "Lipid A"], "Mycolic acids retain carbol fuchsin after acid-alcohol decolorization."),
        q("The standard culture medium for M. tuberculosis is:", "Lowenstein-Jensen medium", ["TCBS agar", "Sabouraud dextrose agar", "Chocolate agar only"], "LJ medium is egg-based and supports mycobacterial culture."),
        q("CBNAAT/GeneXpert is useful because it detects:", "M. tuberculosis DNA and rifampicin resistance", ["Only IgM antibody", "Only culture growth", "Only tuberculin reaction"], "Molecular testing rapidly identifies MTB complex and rpoB-associated rifampicin resistance."),
        q("A positive tuberculin skin test indicates:", "Cell-mediated immune sensitization to mycobacterial antigens", ["Active TB disease always", "No prior exposure", "Protective antibody"], "TST shows delayed-type hypersensitivity and cannot alone distinguish active from latent infection."),
        q("Granuloma formation in TB depends heavily on:", "Th1 immunity and IFN-gamma macrophage activation", ["IgE mast cells", "C5-C9 only", "Eosinophils only"], "Cell-mediated immunity contains mycobacteria in granulomas."),
        q("Miliary tuberculosis results from:", "Hematogenous dissemination", ["Only bronchial allergy", "Toxin-mediated diarrhea", "Direct skin contact only"], "Miliary TB produces widespread tiny lesions via bloodstream spread."),
        q("BCG vaccine primarily protects young children against:", "Severe forms such as TB meningitis and miliary TB", ["All adult pulmonary TB completely", "Leprosy only", "Diphtheria"], "BCG is most valuable for preventing severe pediatric TB."),
        q("Mycobacterium avium complex disease in AIDS is associated with very low:", "CD4 T-cell count", ["Platelet count only", "IgE level only", "Neutrophil count always"], "Disseminated MAC occurs in advanced cellular immunodeficiency."),
        q("Multidrug-resistant TB means resistance at least to:", "Isoniazid and rifampicin", ["Ethambutol alone", "Pyrazinamide alone", "Streptomycin alone"], "MDR-TB is defined by resistance to INH and rifampicin."),
    ]),
    ("pertussis", "Pertussis (Bordetella pertussis)", [
        q("A child has paroxysmal cough with inspiratory whoop and post-tussive vomiting. The likely organism is:", "Bordetella pertussis", ["Corynebacterium diphtheriae", "Mycoplasma pneumoniae", "RSV"], "Pertussis causes prolonged paroxysmal cough and whoop, especially in children."),
        q("Pertussis toxin increases cAMP because it:", "ADP-ribosylates Gi protein", ["Blocks EF-2", "Cleaves SNARE proteins", "Inactivates 60S ribosomes"], "Pertussis toxin prevents Gi inhibition of adenylate cyclase."),
        q("Marked lymphocytosis in pertussis is due to:", "Impaired lymphocyte migration from bloodstream", ["Bone marrow leukemia always", "Hemolysis", "Complement deficiency"], "Pertussis toxin causes lymphocytosis by affecting chemokine receptor signaling."),
        q("The catarrhal stage of pertussis is most important for control because:", "Patients are most contagious and antibiotics work best early", ["Cough has already stopped", "Culture is impossible", "Vaccination treats disease"], "Early disease resembles URI but has highest transmission."),
        q("Best specimen for pertussis PCR/culture is:", "Nasopharyngeal swab or aspirate", ["Stool", "Urine", "Blood only"], "Bordetella colonizes the nasopharynx; proper NP sampling is needed."),
        q("Bordet-Gengou medium is used for:", "Bordetella pertussis culture", ["M. tuberculosis", "Vibrio cholerae", "Candida"], "Bordet-Gengou and Regan-Lowe media support Bordetella isolation."),
        q("Macrolides in pertussis mainly:", "Reduce transmission when given early", ["Immediately repair ciliary damage", "Neutralize toxin already bound", "Replace vaccination"], "Antibiotics are most useful early and for public health control."),
        q("Pertussis vaccination uses:", "Acellular pertussis antigens in many current schedules", ["Live Bordetella", "Only toxoid tetanus", "Killed measles"], "DTaP/Tdap contain acellular pertussis components."),
        q("Infants are at high risk in pertussis because they may develop:", "Apnea and severe complications", ["Hydatid cyst", "Tetanus spasms", "Cholera shock"], "Young infants can have severe pertussis without classic whoop."),
        q("Cocooning strategy means:", "Vaccinating close contacts to protect infants", ["Isolating only mosquitoes", "Using bed nets", "Avoiding all vaccines"], "Immunizing caregivers reduces transmission to vulnerable infants."),
    ]),
    ("non-fermenting-gnb", "Infections due to Non-fermenting Gram-negative Bacilli: Pseudomonas, Acinetobacter, Burkholderia and Others", [
        q("A burn patient develops blue-green pus with fruity odor. The likely organism is:", "Pseudomonas aeruginosa", ["Klebsiella pneumoniae", "S. pyogenes", "Bordetella pertussis"], "Pseudomonas produces pigments and characteristic odor and infects burns."),
        q("Pseudomonas virulence factor that inhibits protein synthesis like diphtheria toxin is:", "Exotoxin A", ["TSST-1", "Cholera toxin", "Tetanospasmin"], "Exotoxin A ADP-ribosylates EF-2."),
        q("Pseudomonas is oxidase:", "Positive", ["Negative", "Variable only in anaerobes", "Not testable"], "Pseudomonas aeruginosa is a non-fermenting oxidase-positive Gram-negative rod."),
        q("A ventilated ICU patient grows multidrug-resistant Acinetobacter baumannii. A key epidemiologic feature is:", "Persistence on dry hospital surfaces", ["Only waterborne survival", "Inability to colonize skin", "Strict community-only spread"], "Acinetobacter survives desiccation and causes healthcare outbreaks."),
        q("Burkholderia cepacia complex is especially important in patients with:", "Cystic fibrosis", ["Sickle cell trait only", "Measles", "Rheumatic fever"], "B. cepacia causes difficult infections in CF and chronic granulomatous disease."),
        q("Melioidosis is caused by:", "Burkholderia pseudomallei", ["Burkholderia cepacia", "Pseudomonas fluorescens", "Acinetobacter lwoffii"], "B. pseudomallei is a soil/water organism causing melioidosis."),
        q("Melioidosis risk is increased in:", "Diabetes mellitus with soil/water exposure in endemic areas", ["Atopy only", "Myopia", "Iron deficiency alone"], "Diabetes is a major risk factor for melioidosis."),
        q("Non-fermenters are difficult to treat because they often have:", "Intrinsic resistance, efflux pumps, and biofilm formation", ["No cell wall", "No DNA", "Extreme penicillin susceptibility always"], "Non-fermenting GNB frequently have multiple resistance mechanisms."),
        q("Pseudomonas pneumonia in hospital settings is associated with:", "Ventilation, structural lung disease, and prior antibiotics", ["Healthy school outbreaks only", "Tick bites", "Unpasteurized milk"], "Pseudomonas is an important nosocomial and structural-lung pathogen."),
        q("Ecthyma gangrenosum in neutropenia is classically associated with:", "Pseudomonas aeruginosa bacteremia", ["Mycoplasma", "Parainfluenza", "Mumps"], "Ecthyma gangrenosum is a necrotic vascular skin lesion linked to Pseudomonas sepsis."),
    ]),
    ("myxovirus-respiratory", "Myxovirus Infections of Respiratory Tract: Influenza, Parainfluenza, Mumps, Respiratory Syncytial Virus and Others", [
        q("Influenza antigenic shift occurs due to:", "Reassortment of segmented RNA genome", ["Point mutation only", "DNA integration", "Capsid spore formation"], "Segmented influenza genomes can reassort, causing major antigenic changes."),
        q("Influenza antigenic drift is due to:", "Accumulation of point mutations in HA/NA genes", ["Whole segment reassortment only", "Bacterial conjugation", "Latent integration"], "Drift causes seasonal variation and vaccine updates."),
        q("Oseltamivir acts by inhibiting:", "Neuraminidase", ["Hemagglutinin binding", "M2 only", "RNA polymerase cap snatching"], "Neuraminidase inhibitors reduce release of influenza virions."),
        q("Parainfluenza virus is a classic cause of:", "Croup", ["Whooping cough", "Diphtheria", "Lobar pneumonia"], "Parainfluenza causes laryngotracheobronchitis with barking cough."),
        q("RSV is the most important cause of:", "Bronchiolitis in infants", ["Rheumatic fever", "Typhoid", "Hydatid cyst"], "RSV causes bronchiolitis and pneumonia in young children."),
        q("RSV pathogenesis includes formation of:", "Syncytia", ["Negri bodies", "Maltese crosses", "Sulfur granules"], "The fusion protein causes multinucleated giant cells/syncytia."),
        q("Palivizumab is used for selected high-risk infants to prevent severe:", "RSV disease", ["Influenza", "Mumps", "Parainfluenza"], "Palivizumab is monoclonal antibody against RSV F protein."),
        q("Mumps classically causes:", "Parotitis and orchitis", ["Pseudomembrane", "Rusty sputum", "Rice-water stool"], "Mumps virus infects salivary glands and can involve testes, pancreas, CNS."),
        q("Mumps prevention is through:", "Live attenuated MMR vaccine", ["Acellular pertussis vaccine", "BCG", "Killed oral cholera vaccine"], "MMR protects against measles, mumps, and rubella."),
        q("Influenza vaccination must be updated because:", "Circulating strains change antigenically", ["The virus becomes bacterial", "Antibodies cannot form", "Vaccines cause influenza infection"], "Drift and changing strains require periodic vaccine reformulation."),
    ]),
    ("coronavirus-covid", "Coronavirus Infections Including COVID-19", [
        q("SARS-CoV-2 enters human cells primarily by spike binding to:", "ACE2 receptor", ["CD4 receptor", "Duffy antigen", "ICAM-1"], "Spike protein binds ACE2, with protease priming facilitating entry."),
        q("The genome of SARS-CoV-2 is:", "Positive-sense single-stranded RNA", ["Double-stranded DNA", "Negative-sense segmented RNA", "Circular DNA"], "Coronaviruses are enveloped positive-sense RNA viruses."),
        q("RT-PCR for COVID-19 detects:", "Viral RNA", ["Host antibody only", "Bacterial culture", "Complement C3"], "NAAT/RT-PCR identifies SARS-CoV-2 RNA in respiratory specimens."),
        q("A rapid antigen test for SARS-CoV-2 is most reliable when:", "Viral load is high early in symptomatic infection", ["Three months after recovery", "Before exposure", "For bacterial pneumonia"], "Antigen tests are faster but less sensitive than NAAT, especially at low viral loads."),
        q("Severe COVID-19 lung disease is often driven by:", "Viral pneumonia with dysregulated host inflammation and thrombosis", ["Botulinum toxin", "Only IgE allergy", "Spore germination"], "Severe disease combines viral injury, inflammation, endothelial dysfunction, and coagulopathy."),
        q("Loss of smell in COVID-19 is called:", "Anosmia", ["Ageusia only", "Dysphonia", "Diplopia"], "Anosmia is loss of smell; ageusia is loss of taste."),
        q("COVID-19 transmission is reduced most directly by:", "Masking, ventilation, vaccination, isolation when infectious, and hand hygiene", ["Antibiotics for all contacts", "Avoiding cooked food", "Mosquito control only"], "Respiratory transmission control uses source control, airflow, immunity, and isolation."),
        q("Dexamethasone benefits selected severe COVID-19 patients mainly when they:", "Require oxygen or ventilatory support", ["Have asymptomatic infection", "Have only bacterial UTI", "Are exposed but PCR negative"], "Steroids reduce mortality in hypoxic severe disease but are not for mild early infection."),
        q("Nirmatrelvir-ritonavir works because nirmatrelvir inhibits:", "SARS-CoV-2 main protease", ["Neuraminidase", "Reverse transcriptase", "Hemagglutinin"], "Nirmatrelvir blocks viral protease processing; ritonavir boosts drug levels."),
        q("Emergence of variants is promoted by:", "Viral replication with mutation and selection pressure", ["Absence of RNA genome", "Bacterial conjugation", "Spore formation"], "RNA virus replication generates mutations; transmissibility/immune escape can be selected."),
    ]),
    ("misc-respiratory-viruses", "Miscellaneous Viral Infections of Respiratory Tract: Rhinovirus, Adenovirus and Infectious Mononucleosis (Epstein-Barr Virus)", [
        q("The common cold is most commonly caused by:", "Rhinovirus", ["Rabies virus", "HBV", "Rotavirus"], "Rhinoviruses are the leading cause of common cold."),
        q("Rhinovirus binds commonly to:", "ICAM-1", ["CD4", "ACE2 only", "Duffy antigen"], "Many rhinoviruses use ICAM-1 as receptor."),
        q("Rhinovirus replicates best at:", "Cooler nasal temperatures", ["Boiling temperature", "Deep lung only at 42 C", "Anaerobic intestine"], "Rhinoviruses prefer upper airway temperatures."),
        q("Adenovirus can cause pharyngoconjunctival fever after:", "Swimming pool exposure", ["Dog bite", "Tick bite", "Undercooked pork"], "Adenovirus spreads through respiratory/ocular secretions and water outbreaks."),
        q("Adenovirus is:", "Nonenveloped double-stranded DNA virus", ["Enveloped negative RNA virus", "Segmented RNA virus", "Retrovirus"], "Adenoviruses are hardy nonenveloped dsDNA viruses."),
        q("A military recruit outbreak of febrile respiratory illness with conjunctivitis suggests:", "Adenovirus", ["Mumps", "Hantavirus", "Ebola"], "Adenovirus causes outbreaks in crowded settings."),
        q("Infectious mononucleosis is classically caused by:", "Epstein-Barr virus", ["Rhinovirus", "Adenovirus 40", "RSV"], "EBV causes fever, pharyngitis, lymphadenopathy, and atypical lymphocytosis."),
        q("EBV infects B cells by binding:", "CD21 receptor", ["CD4", "ACE2", "CCR5"], "CD21/complement receptor 2 mediates EBV B-cell entry."),
        q("Atypical lymphocytes in infectious mononucleosis are mainly:", "Reactive CD8 T cells", ["Malignant B cells always", "Neutrophils", "Eosinophils only"], "CD8 cells expand in response to EBV-infected B cells."),
        q("Aminopenicillin rash after amoxicillin in EBV pharyngitis is:", "A common immune-mediated drug eruption, not proof of true penicillin allergy", ["Diagnostic of diphtheria", "Always anaphylaxis", "Due to pneumococcal capsule"], "Ampicillin/amoxicillin rash is classic in EBV infection."),
    ]),
    ("parasitic-fungal-respiratory", "Parasitic and Fungal Infections of Respiratory Tract", [
        q("A patient coughs rusty-brown sputum and has lung fluke eggs in sputum after eating raw crab. The diagnosis is:", "Paragonimiasis", ["Aspergillosis", "Pneumocystosis", "Mucormycosis"], "Paragonimus lung flukes are acquired from raw/undercooked crab or crayfish."),
        q("Paragonimus infection can mimic tuberculosis because it causes:", "Chronic cough, hemoptysis, and cavitary lung lesions", ["Whooping cough", "Croup", "Pseudomembrane"], "Pulmonary paragonimiasis may resemble TB radiologically and clinically."),
        q("Invasive aspergillosis in neutropenia shows hyphae that are:", "Septate with acute-angle branching", ["Broad aseptate right-angle branching", "Yeast with capsule", "Spaghetti and meatballs"], "Aspergillus is septate and acute-angle branching."),
        q("Allergic bronchopulmonary aspergillosis is associated with:", "Asthma or cystic fibrosis with hypersensitivity to Aspergillus", ["AIDS CD4 <50 only", "Dog bite", "Raw fish"], "ABPA is an allergic reaction to airway Aspergillus colonization."),
        q("Aspergilloma typically develops in:", "Pre-existing lung cavity", ["Normal gallbladder", "Intestinal lumen only", "Peripheral nerves"], "Fungus ball forms in old cavities such as TB cavities."),
        q("Mucormycosis hyphae are classically:", "Broad, ribbon-like, aseptate with right-angle branching", ["Septate acute-angle", "Budding yeast with capsule", "Ciliated trophozoites"], "Mucorales show broad pauciseptate hyphae and angioinvasion."),
        q("Rhinocerebral mucormycosis is strongly linked to:", "Diabetic ketoacidosis", ["Simple allergic rhinitis", "Measles vaccination", "Iron deficiency only"], "DKA and immunosuppression predispose to mucormycosis."),
        q("Pneumocystis jirovecii pneumonia is suggested by hypoxia, diffuse interstitial infiltrates, and elevated LDH in:", "Advanced HIV or T-cell immunodeficiency", ["Healthy athlete after cold exposure", "Typhoid carrier", "Pinworm infection"], "PJP occurs with impaired cellular immunity."),
        q("Pneumocystis is diagnosed by demonstrating organisms in respiratory sample using:", "Silver stain or immunofluorescence/PCR", ["Widal test", "India ink for capsule only", "Hanging drop"], "PJP organisms can be detected by special stains or molecular tests."),
        q("First-line treatment of Pneumocystis pneumonia is:", "Trimethoprim-sulfamethoxazole", ["Acyclovir", "Albendazole only", "Oseltamivir"], "TMP-SMX is preferred for treatment and prophylaxis of PJP."),
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
            questions.append({**BASE, "id": f"micro-respiratory-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "microbiology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 11 or len(questions) != 110:
        raise AssertionError(f"Expected 11 topics and 110 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 110:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
