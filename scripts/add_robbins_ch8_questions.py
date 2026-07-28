import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path("runtime-data/users.json")
CHAPTER = "Infectious Diseases"
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
    ("pathogenesis", "General Principles, Routes of Entry, and Transmission", [
        q("easy", "Most enteric pathogens are transmitted by the:", "Fecal-oral route", ["Paravertebral venous plexus", "IgE-mediated route", "Transplacental-only route"], "Food and water contaminated by stool spread many gastrointestinal pathogens."),
        q("easy", "The intact keratinized epidermis protects against infection mainly as a:", "Mechanical and chemical barrier", ["Source of IgE memory", "Site of V(D)J recombination", "Portal venous filter"], "Skin blocks entry, has low pH, and produces antimicrobial fatty acids and defensins."),
        q("easy", "A zoonotic infection is transmitted from:", "Animals to humans", ["Tumor to tumor", "Mother allele to paternal allele", "Only lymph node to spleen"], "Zoonoses are acquired from animals directly, through animal products, or via vectors."),
        q("moderate", "Neutralization of gastric acid increases susceptibility to some gastrointestinal infections because acid:", "Kills many ingested organisms", ["Promotes viral integration", "Blocks all neutrophils", "Activates IgE"], "Gastric acidity is an important local defense against ingested microbes."),
        q("moderate", "Mucus in the gastrointestinal tract helps prevent infection by:", "Limiting access of pathogens to surface epithelium", ["Killing all intracellular bacteria", "Producing complement C5a", "Causing granulomas"], "The mucus layer physically separates luminal organisms from epithelial surfaces."),
        q("moderate", "Respiratory pathogens such as tuberculosis spread efficiently because they:", "Can be carried in small airborne particles", ["Require direct blood transfusion", "Only survive in stool", "Need intact skin penetration"], "Small droplet nuclei can remain suspended and travel longer distances."),
        q("moderate", "Blood-borne dissemination is dangerous because it:", "Allows microbes to reach many organs", ["Prevents systemic spread", "Always produces only local abscess", "Blocks endothelial adhesion"], "The bloodstream is the most efficient route for widespread microbial dissemination."),
        q("high", "A traveler drinks contaminated water and develops profuse diarrhea. Several family members become ill after sharing the same water source, but no insect vector or sexual contact is involved. Which transmission route best explains the outbreak?", "Fecal-oral transmission", ["Respiratory droplet transmission", "Transplacental transmission", "Percutaneous inoculation by tick"], "Stool-contaminated food or water is classic for enteric outbreaks."),
        q("high", "A burn patient develops sepsis with organisms normally present on skin and mucosal surfaces. The organisms are not highly virulent in healthy hosts, but the barrier breach and immunologic stress allow invasion. Which concept best explains this infection?", "Commensal microbiota causing opportunistic disease after host defenses fail", ["Obligate intracellular parasitism", "Pure toxin-mediated food poisoning", "Prion transmission"], "Commensals can become pathogens when barriers or immunity are compromised."),
        q("high", "Rabies virus enters through an animal bite and later causes encephalitis. Instead of spreading first by massive bacteremia, the virus travels from peripheral tissue toward the central nervous system along nerves. Which dissemination route is highlighted?", "Axonal spread through peripheral nerves", ["Portal venous spread", "Lymphatic spread to sentinel nodes only", "Peritoneal seeding"], "Rabies and some other viruses can spread by neural transport."),
    ]),
    ("host-pathogen", "Host-Pathogen Interactions, Immune Evasion, and Microbial Damage", [
        q("easy", "Microbial virulence refers to:", "Ability of a microbe to cause disease", ["Amount of edema fluid", "Host HLA type only", "Tumor grade"], "Virulence is the pathogenic capacity of an organism."),
        q("easy", "Endotoxin is a component of:", "Gram-negative bacterial outer membrane", ["Fungal capsule only", "Viral envelope only", "Helminth eggs only"], "Lipopolysaccharide is the classic gram-negative endotoxin."),
        q("easy", "Exotoxins are usually:", "Secreted bacterial proteins", ["Host antibodies", "Amyloid fibrils", "Cholesterol crystals"], "Many bacteria secrete protein toxins that injure host cells."),
        q("moderate", "Antigenic variation helps microbes by:", "Avoiding existing immune responses", ["Increasing host antibody affinity", "Blocking all mutation", "Preventing transmission"], "Changing surface antigens permits escape from antibodies or T cells."),
        q("moderate", "Capsules promote bacterial virulence mainly by:", "Inhibiting phagocytosis", ["Increasing telomerase", "Activating collagen synthesis", "Blocking toxin production"], "Capsules protect organisms from ingestion by phagocytes."),
        q("moderate", "Biofilms are clinically important because they:", "Protect microbes from antibiotics and host defenses", ["Always prevent chronic infection", "Only occur in viruses", "Are made of amyloid"], "Biofilms on prostheses or catheters can sustain persistent infection."),
        q("moderate", "Host immune responses can injure tissue during infection by:", "Producing inflammation, necrosis, or fibrosis", ["Eliminating all pathogens without damage", "Preventing cytokine release", "Blocking granuloma formation"], "Some tissue damage is immunopathologic rather than directly microbial."),
        q("high", "A child with recurrent infections by encapsulated bacteria has poor opsonization. The organisms resist direct ingestion by neutrophils unless coated by antibody or complement. Which microbial virulence factor is most responsible?", "Polysaccharide capsule", ["Endospore formation", "Viral latency", "Axonal transport"], "Capsules are antiphagocytic and are especially problematic when humoral immunity is weak."),
        q("high", "A patient with sepsis from gram-negative rods develops fever, hypotension, disseminated intravascular coagulation, and multiorgan failure. The responsible microbial product activates innate immune cells through TLR signaling. Which product is central?", "Lipopolysaccharide endotoxin", ["Botulinum neurotoxin", "Fungal ergosterol", "Prion protein"], "LPS triggers cytokine release and septic shock physiology."),
        q("high", "A prosthetic joint infection persists despite antibiotics. Microscopy shows bacteria embedded in an extracellular matrix attached to the implant surface, with intermittent shedding into surrounding tissue. Which microbial strategy explains chronicity?", "Biofilm formation", ["Antigen receptor recombination", "Carcinoma in situ", "Mitochondrial heteroplasmy"], "Biofilms protect microbes and make device infections difficult to eradicate."),
    ]),
    ("patterns", "Patterns of Tissue Response to Infection", [
        q("easy", "Suppurative inflammation is characterized by abundant:", "Neutrophils and pus", ["Eosinophils only", "Amyloid deposits", "Mature adipocytes"], "Pyogenic bacteria commonly produce neutrophil-rich pus."),
        q("easy", "Granulomatous inflammation is strongly associated with:", "Persistent intracellular organisms", ["Pure toxin ingestion only", "Acute IgE allergy", "Simple transudate"], "Tuberculosis, fungi, and some parasites can provoke granulomas."),
        q("easy", "Viral cytopathic effect means:", "Cell injury with characteristic viral-induced morphologic changes", ["Fibrin clot formation", "Collagen scar only", "Platelet plug formation"], "Viruses may produce inclusions, syncytia, or other cytopathic changes."),
        q("moderate", "Abscesses are most typical of infections by:", "Pyogenic bacteria", ["Prions", "Dermatophytes only", "Latent herpesvirus only"], "Staphylococci and other pyogenic bacteria often produce localized abscesses."),
        q("moderate", "Caseating granulomas are classically seen in:", "Tuberculosis", ["Acute staphylococcal impetigo", "Cholera", "Botulism"], "TB often produces granulomas with central caseous necrosis."),
        q("moderate", "Viral inclusion bodies are useful because they:", "May suggest a specific viral infection", ["Always prove bacterial sepsis", "Are amyloid deposits", "Represent normal mitoses"], "Inclusions such as CMV owl-eye inclusions can be diagnostic clues."),
        q("moderate", "Chronic inflammation and scarring during infection may lead to:", "Strictures or organ dysfunction", ["Immediate complete regeneration in all tissues", "Absence of fibrosis", "Only transient edema"], "Persistent infection can destroy tissue and heal by fibrosis."),
        q("high", "A lung biopsy from a patient with chronic cough shows epithelioid macrophages, Langhans giant cells, and central caseous necrosis. Acid-fast bacilli are rare but present. Which tissue reaction pattern is most characteristic?", "Granulomatous inflammation with caseation", ["Suppurative inflammation only", "Cytopathic-cytoproliferative reaction", "Serous transudate"], "TB induces a Th1 macrophage response forming caseating granulomas."),
        q("high", "A skin lesion caused by Staphylococcus aureus contains liquefactive necrosis, many viable and degenerated neutrophils, and a surrounding rim of congested vessels. Which inflammatory pattern best describes the lesion?", "Suppurative abscess formation", ["Noncaseating granuloma", "Amyloid deposition", "Viral syncytial cytopathic effect"], "Pyogenic bacteria often create pus-filled abscesses."),
        q("high", "A liver fluke infection persists for years and causes ongoing epithelial injury, duct inflammation, and periductal fibrosis. The major clinical problem eventually reflects scarring rather than acute microbial lysis. Which pattern is emphasized?", "Chronic inflammation with fibrosis", ["Immediate type I hypersensitivity", "Pure endotoxin shock", "Benign tumor growth"], "Long-standing infections may cause fibrosis and structural organ damage."),
    ]),
    ("viral", "Viral Infections", [
        q("easy", "Herpesviruses are notable for their ability to establish:", "Latent infection", ["Obligate abscess formation", "Endospore formation", "Prion conversion"], "HSV, VZV, CMV, and EBV can persist latently and reactivate."),
        q("easy", "Measles virus classically produces:", "Koplik spots", ["Chancre", "Caseating granuloma", "Apple-green birefringence"], "Koplik spots are oral lesions seen in measles."),
        q("easy", "Cytomegalovirus inclusions are often described as:", "Owl-eye inclusions", ["Councilman bodies", "Negri bodies", "Aschoff bodies"], "CMV produces large cells with basophilic intranuclear inclusions."),
        q("moderate", "HSV infection often shows multinucleated cells with:", "Nuclear molding and ground-glass nuclei", ["Caseous necrosis only", "Birbeck granules", "Auer rods"], "Herpes cytopathic effect includes multinucleation, molding, and margination."),
        q("moderate", "Varicella-zoster virus causes chickenpox and can later reactivate as:", "Shingles", ["Mumps", "Dengue", "Poliomyelitis"], "VZV remains latent in dorsal root ganglia and reactivates as zoster."),
        q("moderate", "EBV infects B cells mainly through:", "CD21 complement receptor", ["CD4 receptor", "LDL receptor", "GpIb"], "EBV uses CD21 on B cells and is linked to mononucleosis and tumors."),
        q("moderate", "Dengue hemorrhagic fever is associated with:", "Antibody-dependent enhancement", ["Mannose-6-phosphate deficiency", "IgE receptor mutation", "Prion conversion"], "Nonneutralizing antibodies can enhance infection during secondary dengue."),
        q("high", "A transplant recipient develops fever and pneumonitis. Lung biopsy shows enlarged cells with prominent basophilic intranuclear inclusions surrounded by a clear halo. Which virus best matches this cytopathic pattern?", "Cytomegalovirus", ["Measles virus", "Parvovirus B19", "Hepatitis A virus"], "CMV causes enlarged cells with owl-eye nuclear inclusions, especially in immunosuppressed hosts."),
        q("high", "A young adult develops fever, pharyngitis, lymphadenopathy, atypical lymphocytosis, and splenomegaly. The virus infects B cells using CD21, while the atypical circulating lymphocytes are reactive CD8+ T cells. Which infection is most likely?", "Epstein-Barr virus infectious mononucleosis", ["Varicella-zoster primary infection", "Dengue fever", "Poliomyelitis"], "EBV mononucleosis features infected B cells and reactive cytotoxic T cells."),
        q("high", "A patient has a second dengue infection with a different serotype and develops plasma leakage, thrombocytopenia, and hemorrhage. Preexisting antibodies fail to neutralize the virus and instead promote Fc receptor-mediated uptake. What mechanism is responsible?", "Antibody-dependent enhancement", ["Latency in dorsal root ganglia", "Defective nucleotide excision repair", "Endotoxin-mediated shock"], "Dengue severity can result from antibody-enhanced infection of Fc receptor-bearing cells."),
    ]),
    ("bacterial", "Gram-Positive and Gram-Negative Bacterial Infections", [
        q("easy", "Staphylococcus aureus commonly causes:", "Abscesses", ["Caseating granulomas only", "Malaria", "Hydatid cysts"], "S. aureus is a classic pyogenic abscess-forming bacterium."),
        q("easy", "Streptococcus pyogenes is a:", "Group A beta-hemolytic streptococcus", ["Gram-negative diplococcus", "Acid-fast bacillus", "Yeast"], "S. pyogenes is group A beta-hemolytic streptococcus."),
        q("easy", "Neisseria gonorrhoeae is a:", "Gram-negative diplococcus", ["Gram-positive rod", "Acid-fast bacillus", "Helminth"], "Gonococcus is a gram-negative diplococcus."),
        q("moderate", "Diphtheria toxin inhibits:", "Protein synthesis by ADP-ribosylating EF-2", ["DNA mismatch repair", "LDL uptake", "Collagen cross-linking"], "Corynebacterium diphtheriae toxin blocks elongation factor-2."),
        q("moderate", "Listeria monocytogenes is especially dangerous in:", "Pregnant and immunocompromised patients", ["Only healthy adult athletes", "Only patients with LDL receptor mutation", "Only patients with xeroderma pigmentosum"], "Listeria causes severe disease in neonates, pregnant persons, elderly, and immunosuppressed."),
        q("moderate", "Pertussis is caused by:", "Bordetella pertussis", ["Yersinia pestis", "Haemophilus ducreyi", "Klebsiella rhinoscleromatis"], "B. pertussis causes whooping cough."),
        q("moderate", "Pseudomonas aeruginosa is strongly associated with infections in:", "Burn wounds and cystic fibrosis lungs", ["Normal gastric mucosa only", "Latent dorsal root ganglia", "Hydatid cysts only"], "Pseudomonas thrives in moist environments and affects burns, devices, and CF airways."),
        q("high", "A burn patient develops a green-blue wound infection with sepsis. The organism is oxidase-positive, produces pigments, and often infects moist hospital environments and damaged tissue. Which bacterium is most likely?", "Pseudomonas aeruginosa", ["Listeria monocytogenes", "Treponema pallidum", "Streptococcus pneumoniae"], "Pseudomonas causes burn wound infections with characteristic pigments and severe sepsis."),
        q("high", "A child with fever and sore throat develops a thick gray pharyngeal pseudomembrane that bleeds when scraped. The major systemic danger is myocarditis and neuropathy caused by toxin-mediated protein synthesis inhibition. Which pathogen is responsible?", "Corynebacterium diphtheriae", ["Neisseria meningitidis", "Staphylococcus epidermidis", "Clostridium perfringens"], "Diphtheria produces a pseudomembrane and toxin that inhibits EF-2."),
        q("high", "A sexually active patient has purulent urethral discharge with intracellular gram-negative diplococci in neutrophils. The organism can vary pili and outer membrane proteins to evade immunity and reinfect hosts. Which organism is most likely?", "Neisseria gonorrhoeae", ["Chlamydia trachomatis", "Treponema pallidum", "Haemophilus ducreyi"], "Gonorrhea shows gram-negative diplococci and antigenic variation."),
    ]),
    ("myco-spiro", "Mycobacteria, Spirochetes, Anaerobes, and Intracellular Bacteria", [
        q("easy", "Mycobacterium tuberculosis is identified by:", "Acid-fast staining", ["Gram-positive cocci in clusters", "Silver stain only", "Congo red staining"], "Mycobacteria have mycolic acids and are acid-fast."),
        q("easy", "The primary lesion of syphilis is a:", "Chancre", ["Gumma only", "Abscess", "Hydatid cyst"], "Primary syphilis produces a painless chancre."),
        q("easy", "Clostridia are:", "Anaerobic spore-forming gram-positive rods", ["Acid-fast bacilli", "Gram-negative diplococci", "Obligate intracellular viruses"], "Clostridia are anaerobic spore-forming rods."),
        q("moderate", "Tuberculosis immunity depends strongly on:", "Th1-mediated macrophage activation", ["IgE-mediated mast cell degranulation", "Complement alone", "Platelet aggregation"], "IFN-gamma from Th1 cells activates macrophages to contain TB."),
        q("moderate", "Leprosy is caused by:", "Mycobacterium leprae", ["Mycobacterium avium", "Treponema pallidum", "Borrelia burgdorferi"], "M. leprae infects skin and peripheral nerves."),
        q("moderate", "Lyme disease is transmitted by:", "Ixodes ticks", ["Sandflies", "Tsetse flies", "Mosquitoes only"], "Borrelia burgdorferi is spread by Ixodes ticks."),
        q("moderate", "Chlamydia trachomatis is an:", "Obligate intracellular bacterium", ["Encapsulated yeast", "Acid-fast helminth", "Free-living protozoan"], "Chlamydiae require intracellular replication."),
        q("high", "A patient with cough, fever, weight loss, and apical cavitary lung lesions has sputum positive for acid-fast bacilli. Granulomas show caseous necrosis. Which immune response is most responsible for containing but also damaging tissue?", "Th1-mediated delayed-type hypersensitivity and macrophage activation", ["IgE-mediated mast cell activation", "Type II receptor blockade", "Complement C1 inhibitor deficiency"], "TB control and pathology depend on Th1 IFN-gamma macrophage responses."),
        q("high", "A patient has a painless genital ulcer, followed weeks later by diffuse rash involving palms and soles. Years later, untreated infection can cause gummas and aortitis. Which organism explains this staged disease?", "Treponema pallidum", ["Haemophilus ducreyi", "Neisseria gonorrhoeae", "Chlamydia psittaci"], "Syphilis progresses through primary, secondary, and tertiary stages."),
        q("high", "After a deep contaminated wound, a patient develops crepitus, severe pain, myonecrosis, and systemic toxicity. Gram-positive anaerobic rods produce toxins that destroy tissue and generate gas. Which infection is most likely?", "Clostridial myonecrosis", ["Tuberculoid leprosy", "Lyme arthritis", "Primary syphilis"], "Clostridium perfringens can cause gas gangrene with myonecrosis."),
    ]),
    ("fungal", "Fungal Infections", [
        q("easy", "Candida albicans commonly causes:", "Thrush and vaginitis", ["Malaria", "Hydatid disease", "Chancre"], "Candida causes mucocutaneous infections and invasive disease in susceptible hosts."),
        q("easy", "Cryptococcus neoformans has a prominent:", "Polysaccharide capsule", ["Acid-fast wall", "Segmented larval body", "Gram-negative outer membrane"], "Cryptococcus is an encapsulated yeast."),
        q("easy", "Aspergillus typically shows:", "Septate hyphae with acute-angle branching", ["Broad nonseptate hyphae", "Intracellular amastigotes", "Acid-fast rods"], "Aspergillus has narrow septate hyphae branching at acute angles."),
        q("moderate", "Mucormycosis is characterized by:", "Broad ribbon-like nonseptate hyphae", ["Narrow acute-angle septate hyphae", "Encapsulated budding yeast only", "Spherules with endospores"], "Mucorales show broad pauciseptate hyphae with wide-angle branching."),
        q("moderate", "Pneumocystis jirovecii pneumonia is most common in:", "Patients with impaired T-cell immunity", ["Patients with isolated platelet deficiency", "Healthy hosts only", "Patients with familial hypercholesterolemia"], "Pneumocystis affects AIDS and other T-cell immunodeficient patients."),
        q("moderate", "Invasive aspergillosis is strongly associated with:", "Neutropenia", ["High LDL cholesterol", "IgE allergy alone", "Scurvy"], "Neutrophils are important against molds; neutropenia predisposes to invasive Aspergillus."),
        q("moderate", "Mucormycosis has a predilection for patients with:", "Diabetic ketoacidosis", ["Turner syndrome", "Marfan syndrome", "Sickle trait only"], "Rhinocerebral mucormycosis is classically associated with DKA."),
        q("high", "A neutropenic leukemia patient develops pleuritic chest pain and hemoptysis. Lung biopsy shows angioinvasive septate hyphae branching at acute angles with hemorrhagic infarction. Which fungus is most likely?", "Aspergillus species", ["Candida albicans", "Cryptococcus neoformans", "Mucor species"], "Aspergillus is angioinvasive and causes infarcts in neutropenic patients."),
        q("high", "A patient with diabetic ketoacidosis develops facial pain, black nasal eschar, orbital swelling, and broad nonseptate hyphae invading blood vessels. Which fungal infection best explains this rapidly progressive disease?", "Mucormycosis", ["Pneumocystis pneumonia", "Cryptococcal meningitis", "Dermatophyte infection"], "Mucorales invade vessels in DKA, causing rhinocerebral necrosis."),
        q("high", "An AIDS patient with very low CD4 count develops meningitis. India ink highlights round yeasts with thick capsules in cerebrospinal fluid. Which virulence feature is most important for this organism?", "Polysaccharide capsule", ["Acute-angle hyphae", "Endotoxin", "Egg shell calcification"], "Cryptococcus neoformans is an encapsulated yeast causing meningitis in immunosuppressed hosts."),
    ]),
    ("protozoa", "Protozoal Infections", [
        q("easy", "Malaria is caused by:", "Plasmodium species", ["Schistosoma species", "Candida species", "Clostridium species"], "Plasmodium protozoa cause malaria."),
        q("easy", "Malaria is transmitted by:", "Anopheles mosquitoes", ["Ixodes ticks", "Tsetse flies", "Sandflies only"], "Female Anopheles mosquitoes transmit Plasmodium."),
        q("easy", "Toxoplasma gondii is especially dangerous in:", "Fetuses and immunocompromised patients", ["Only patients with high LDL", "Only burn wounds", "Only patients with cystic fibrosis"], "Toxoplasma causes congenital infection and reactivation encephalitis."),
        q("moderate", "Leishmaniasis is transmitted by:", "Sandflies", ["Anopheles mosquitoes", "Fleas", "Lice only"], "Leishmania is spread by sandflies."),
        q("moderate", "Chagas disease is caused by:", "Trypanosoma cruzi", ["Trypanosoma brucei", "Plasmodium vivax", "Babesia microti"], "T. cruzi causes American trypanosomiasis."),
        q("moderate", "Babesiosis infects primarily:", "Red blood cells", ["Hepatocytes only", "Neurons only", "Salivary glands"], "Babesia parasites infect erythrocytes and can mimic malaria."),
        q("moderate", "Cerebral malaria is most associated with:", "Plasmodium falciparum", ["Plasmodium malariae", "Toxoplasma gondii", "Leishmania donovani"], "P. falciparum causes severe disease through sequestration of infected RBCs."),
        q("high", "A traveler from sub-Saharan Africa develops cyclic fever, anemia, splenomegaly, and coma. Blood smear shows heavy parasitemia with delicate ring forms, and infected RBCs adhere to endothelium in small vessels. Which organism is most likely?", "Plasmodium falciparum", ["Babesia microti", "Trypanosoma cruzi", "Leishmania donovani"], "P. falciparum causes severe malaria by RBC sequestration and microvascular obstruction."),
        q("high", "An immunosuppressed patient has multiple ring-enhancing brain lesions. Biopsy shows necrotizing abscesses with tachyzoites, and history reveals latent cysts reactivated after CD4 depletion. Which protozoan is responsible?", "Toxoplasma gondii", ["Entamoeba histolytica", "Plasmodium vivax", "Giardia lamblia"], "Toxoplasma reactivation causes encephalitis in AIDS and other immunodeficiencies."),
        q("high", "A patient from rural South America develops dilated cardiomyopathy and megacolon years after an insect-borne infection. The parasite forms intracellular amastigotes in muscle cells. Which disease is most likely?", "Chagas disease", ["African sleeping sickness", "Visceral leishmaniasis", "Babesiosis"], "Trypanosoma cruzi causes chronic Chagas cardiomyopathy and GI dilation."),
    ]),
    ("metazoal-sti", "Metazoal, Sexually Transmitted, and Emerging Infections", [
        q("easy", "Schistosoma species infect humans when cercariae:", "Penetrate skin in contaminated water", ["Are inhaled as spores", "Are transmitted by respiratory droplets", "Integrate into host DNA"], "Schistosome larvae penetrate intact skin during water exposure."),
        q("easy", "Hydatid disease is caused by:", "Echinococcus granulosus", ["Taenia solium larvae in brain", "Strongyloides stercoralis", "Onchocerca volvulus"], "Echinococcus forms hydatid cysts, often in liver."),
        q("easy", "Chancroid is caused by:", "Haemophilus ducreyi", ["Treponema pallidum", "Klebsiella granulomatis", "HSV-1 only"], "H. ducreyi causes painful chancroid ulcers."),
        q("moderate", "Cysticercosis results from ingestion of:", "Taenia solium eggs", ["Echinococcus adult worms", "Schistosoma cercariae", "Candida yeast"], "Ingested T. solium eggs produce larval cysts in tissues, including brain."),
        q("moderate", "Strongyloides can cause hyperinfection in:", "Immunosuppressed patients", ["Patients with isolated hypercholesterolemia", "Healthy vaccinated hosts only", "Patients with Turner syndrome"], "Autoinfection can become disseminated with impaired immunity, especially steroids."),
        q("moderate", "Onchocerciasis is associated with:", "River blindness", ["Hydatid cysts", "Genital chancre", "Gas gangrene"], "Onchocerca volvulus can cause dermatitis and blindness."),
        q("moderate", "Emerging infections may arise from:", "Zoonotic spillover and ecological change", ["Only decreased microbial mutation", "Elimination of travel", "Absence of vectors"], "New infections often reflect animal reservoirs, environmental disruption, travel, and microbial evolution."),
        q("high", "A patient with seizures has multiple calcified brain cysts. The infection followed ingestion of eggs from a pork tapeworm, not undercooked pork muscle containing cysticerci. Which diagnosis best fits?", "Neurocysticercosis", ["Hydatid disease", "Schistosomiasis", "Trichinosis"], "Ingesting T. solium eggs causes cysticercosis; larvae can lodge in brain."),
        q("high", "A farmer develops a large liver cyst with daughter cysts after exposure to dog feces containing tapeworm eggs. Rupture could cause anaphylaxis and spread of protoscolices. Which parasite is responsible?", "Echinococcus granulosus", ["Taenia solium", "Strongyloides stercoralis", "Schistosoma mansoni"], "Echinococcus causes hydatid cysts with daughter cysts, often in liver."),
        q("high", "A patient on corticosteroids develops severe enterocolitis, pneumonia, and gram-negative sepsis from disseminated larvae. The parasite can autoinfect the host, allowing decades of persistence before hyperinfection. Which helminth is most likely?", "Strongyloides stercoralis", ["Onchocerca volvulus", "Trichinella spiralis", "Wuchereria bancrofti"], "Strongyloides autoinfection can become fatal hyperinfection with immunosuppression."),
    ]),
    ("diagnosis", "Special Techniques and Diagnostic Approach to Infection", [
        q("easy", "Acid-fast stains are used mainly to detect:", "Mycobacteria", ["Encapsulated yeasts only", "Amyloid", "Gram-negative diplococci"], "Mycobacteria retain acid-fast stains because of mycolic acids."),
        q("easy", "Silver stains are often useful for detecting:", "Fungi", ["LDL receptors", "Collagen fibrils only", "Platelet granules"], "GMS and other silver stains highlight many fungi."),
        q("easy", "Culture is useful because it can:", "Identify organisms and guide antimicrobial susceptibility testing", ["Always detect every virus instantly", "Replace all histology", "Determine tumor grade"], "Culture can grow organisms and support susceptibility testing."),
        q("moderate", "PCR-based tests detect infection by identifying:", "Microbial nucleic acid", ["Only host antibodies", "Only pus formation", "Only tissue fibrosis"], "PCR amplifies specific DNA or RNA sequences of pathogens."),
        q("moderate", "Serology is most useful when it detects:", "Host antibody response to a pathogen", ["Only bacterial capsules", "Only tissue necrosis", "Only telomerase"], "Serologic tests infer infection through antigen-specific antibodies."),
        q("moderate", "In situ hybridization helps localize:", "Microbial nucleic acid within tissue sections", ["Serum antibodies in plasma only", "Culture colonies on agar only", "Drug levels"], "ISH can show pathogen genomes in their histologic context."),
        q("moderate", "Histologic diagnosis of infection is valuable because it:", "Shows tissue reaction and organism location", ["Always gives antibiotic susceptibility", "Eliminates need for clinical correlation", "Detects only viruses"], "Microscopy can link organisms to injury patterns."),
        q("high", "A lung biopsy from an immunosuppressed patient shows necrotizing pneumonia, but routine H&E does not clearly reveal organisms. GMS stain highlights septate branching hyphae invading vessels. Why was the special stain important?", "It increased visualization of fungal organisms in tissue", ["It measured serum antibody titer", "It cultured bacteria for susceptibility", "It detected tumor stage"], "Special stains such as GMS highlight fungi that may be subtle on H&E."),
        q("high", "A patient has suspected tuberculosis, but organisms are sparse in granulomas. Acid-fast stain is negative on one section, while PCR on tissue detects mycobacterial DNA. Which advantage does molecular testing provide here?", "Sensitive detection of pathogen nucleic acid despite low organism burden", ["Proof of antibiotic susceptibility in every case", "Measurement of host IgE only", "Replacement of all morphology"], "PCR can detect small amounts of microbial DNA when stains are insensitive."),
        q("high", "A transplant recipient has colitis with large cells suspicious for CMV. Immunohistochemistry stains viral antigen within enlarged endothelial and stromal cells, confirming that the virus is present at sites of injury. What is the key diagnostic value?", "Localizing pathogen antigen directly in diseased tissue", ["Showing only past exposure", "Determining host HLA type", "Measuring complement consumption"], "IHC confirms specific organisms in the lesional tissue context."),
    ]),
]


def build_questions():
    questions = []
    for topic_index, (slug, topic, items) in enumerate(TOPICS):
        if len(items) != 10:
            raise ValueError(f"{topic} has {len(items)} questions")
        for index, data in enumerate(items, start=1):
            question = {**BASE, "id": f"robbins-ch8-{slug}-{index}", "topic": topic, **data}
            jumble(question, (topic_index + index - 1) % 4)
            questions.append(question)
    return questions


def validate(chapter_questions, all_questions=None):
    if len(chapter_questions) != 100:
        raise ValueError(f"Expected 100 Chapter 8 questions, got {len(chapter_questions)}")
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
    kept = [question for question in existing if not (question.get("chapterTitle") == CHAPTER or str(question.get("id", "")).startswith("robbins-ch8-"))]
    data["questions"] = kept + chapter_questions
    validate(chapter_questions, data["questions"])
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Removed {len(existing) - len(kept)} existing Chapter 8 questions")
    print(f"Added {len(chapter_questions)} Robbins Chapter 8 questions")
    for topic, count in Counter(q["topic"] for q in chapter_questions).items():
        print(f"{count:2d}  {topic}")


if __name__ == "__main__":
    main()
