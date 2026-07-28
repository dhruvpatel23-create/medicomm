import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "General Microbiology"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("introduction-history", "Introduction and History", [
        q("A surgeon in the 1860s reduces postoperative wound sepsis by using carbolic acid spray. This contribution is classically linked to:", "Joseph Lister", ["Robert Koch", "Louis Pasteur", "Edward Jenner"], "Lister applied antisepsis principles to surgery using phenol, reducing wound infections."),
        q("A milk-borne outbreak is prevented by controlled heating that kills pathogens without sterilizing the product. This method is named after:", "Louis Pasteur", ["Alexander Fleming", "Hans Christian Gram", "Paul Ehrlich"], "Pasteurization reduces microbial load and pathogens while preserving food quality."),
        q("A microbiologist proves a specific bacillus causes anthrax using organism isolation, culture, animal inoculation, and reisolation. This demonstrates:", "Koch's postulates", ["Pasteur effect", "Lancefield grouping", "Quellung reaction"], "Koch's postulates link a specific microorganism to a specific disease."),
        q("Smallpox prevention by cowpox inoculation is historically attributed to:", "Edward Jenner", ["Robert Koch", "Joseph Lister", "Dmitri Ivanovsky"], "Jenner's vaccination work established a foundation for immunization."),
        q("A patient asks why antibiotics do not work for influenza. The core microbiology reason is:", "Viruses lack bacterial targets such as cell wall and ribosomes", ["Viruses are larger than bacteria", "Viruses grow on ordinary agar", "Viruses are killed only by Gram stain"], "Most antibacterial drugs target bacterial-specific structures or pathways absent in viruses."),
        q("A student says spontaneous generation explains maggots in meat. The experiment that disproved this idea by swan-neck flasks was by:", "Louis Pasteur", ["Robert Hooke", "Edward Jenner", "Alexander Fleming"], "Pasteur showed microbes arise from preexisting microbes, not spontaneous generation."),
        q("The discovery of penicillin after observing mold inhibiting staphylococci is credited to:", "Alexander Fleming", ["Paul Ehrlich", "Louis Pasteur", "Joseph Lister"], "Fleming observed Penicillium inhibiting bacterial growth, leading to penicillin development."),
        q("A physician uses the term 'normal flora' but wants modern wording recognizing ecological function. The better term is:", "Normal microbiota", ["Pure culture", "Sterile flora", "Pathognomonic flora"], "Microbiota better describes the community of microbes living in and on the host."),
        q("The germ theory of disease changed medicine because it proposed that:", "Specific microorganisms can cause specific diseases", ["All fevers are due to toxins only", "Miasma is the only source of infection", "Human cells transform into bacteria"], "Germ theory replaced vague miasma concepts with microbial causation and prevention strategies."),
        q("A new MBBS student asks why microbiology matters clinically. The best answer is:", "It links syndrome, specimen, diagnosis, antimicrobial choice, and infection control", ["It only names organisms", "It replaces clinical examination", "It studies only dead microbes"], "Clinical microbiology integrates pathogen biology with diagnosis, treatment, and prevention."),
    ]),
    ("microscopy", "Microscopy", [
        q("A CSF sample is examined for Cryptococcus. Which microscopy test rapidly demonstrates the capsule?", "India ink preparation", ["Albert stain", "Ziehl-Neelsen stain", "Hanging drop", "Lactophenol cotton blue only"], "India ink gives negative staining around the cryptococcal capsule."),
        q("A sputum sample from suspected tuberculosis is stained by Ziehl-Neelsen method. Acid fastness is mainly due to:", "Mycolic acids in the cell wall", ["Capsular polysaccharide", "Teichoic acid", "Endotoxin"], "Mycobacterial mycolic acids retain carbol fuchsin after acid-alcohol decolorization."),
        q("A motility test is needed for Vibrio cholerae from rice-water stool. The best rapid wet mount method is:", "Hanging drop preparation", ["Gram stain only", "Albert stain", "Negative capsule stain"], "Hanging drop can show darting motility of Vibrio in fresh specimens."),
        q("A throat swab from suspected diphtheria shows metachromatic granules. Which stain is classically used?", "Albert stain", ["India ink", "Giemsa only", "Silver stain"], "Albert stain demonstrates volutin/metachromatic granules in Corynebacterium diphtheriae."),
        q("A Gram stain shows purple cocci in clusters. The purple color means the bacteria:", "Retained crystal violet-iodine complex", ["Lost safranin", "Contain acid-fast mycolic acid", "Have no peptidoglycan"], "Gram-positive bacteria retain crystal violet because of thick peptidoglycan."),
        q("A clinician wants direct detection of spirochetes from a chancre exudate. Which microscopy is most suitable?", "Dark-field microscopy", ["Bright-field unstained microscopy", "Electron microscopy only", "Phase contrast for eggs"], "Treponema pallidum is thin and best visualized by dark-field microscopy in lesion fluid."),
        q("Fluorescent auramine-rhodamine staining for AFB is useful because it:", "Allows faster screening of smears at lower magnification", ["Confirms drug susceptibility", "Differentiates all mycobacterial species", "Kills viable bacilli"], "Fluorescent AFB stains improve screening efficiency but positives may need confirmation."),
        q("Lactophenol cotton blue is used mainly to examine:", "Fungal morphology", ["Viral inclusion bodies in blood", "Bacterial capsules in CSF", "Protozoal motility in stool"], "LPCB mounts preserve and stain fungal hyphae, spores, and conidia."),
        q("A stool wet mount must be examined quickly for trophozoites because delay causes:", "Loss of motility and morphological distortion", ["Instant acid-fastness", "Conversion to bacterial spores", "Permanent Gram positivity"], "Fresh examination preserves motility of trophozoites such as Entamoeba and Giardia."),
        q("Electron microscopy is rarely routine for diagnosis today because:", "It is expensive, technically demanding, and often replaced by antigen or molecular tests", ["It cannot see viruses", "It works only for Gram-positive bacteria", "It requires live patients in scanner"], "EM can visualize viruses but is impractical for most routine clinical diagnosis."),
    ]),
    ("general-bacteriology", "General Bacteriology", [
        q("A Gram-negative septic patient develops shock. The major outer membrane component triggering cytokine release is:", "Lipid A of lipopolysaccharide", ["Peptidoglycan pentaglycine bridge", "Teichoic acid", "Capsular hyaluronic acid"], "Lipid A is the endotoxin component of LPS and drives fever, shock, and DIC."),
        q("A patient with recurrent pneumococcal infection after splenectomy lacks effective clearance mainly because pneumococcus has:", "Antiphagocytic capsule", ["Endospore", "Flagellar sheath", "Mycolic acid"], "Encapsulated bacteria require opsonization and splenic macrophage clearance."),
        q("An autoclave is preferred for surgical instruments because it kills spores by:", "Moist heat protein denaturation under pressure", ["Dry heat oxidation only", "Filtration", "Freezing"], "Autoclaving uses saturated steam under pressure and is reliable for spores."),
        q("Clostridium tetani survives adverse conditions in soil because it forms:", "Endospores", ["Elementary bodies", "Cysts", "Conidia"], "Bacterial endospores resist heat, drying, and chemicals."),
        q("A culture plate has tiny colonies only around Staphylococcus aureus streak because the organism needs V factor. This is:", "Satellitism of Haemophilus influenzae", ["Swarming of Proteus", "String test of Vibrio", "Optochin sensitivity"], "S. aureus supplies NAD/V factor, allowing H. influenzae satellite growth."),
        q("A bacterium acquires a plasmid carrying ESBL resistance through direct pilus-mediated transfer. This genetic process is:", "Conjugation", ["Transduction", "Transformation", "Transposition only"], "Conjugation transfers plasmid DNA through cell-to-cell contact."),
        q("A pneumococcus takes up naked DNA from its environment and changes capsule type. This is:", "Transformation", ["Conjugation", "Specialized transduction", "Binary fission"], "Transformation is uptake and expression of naked extracellular DNA."),
        q("A toxin gene is transferred between bacteria by a bacteriophage. This is:", "Transduction", ["Transformation", "Conjugation", "Mutation only"], "Bacteriophages can transfer bacterial genes, including toxin genes."),
        q("Kirby-Bauer testing reports zones around antibiotic discs. The result is interpreted using:", "Standardized zone diameters linked to susceptibility breakpoints", ["Colony color alone", "Smell of agar", "Microscope motility"], "Disc diffusion requires standardized inoculum, medium, and interpretive criteria."),
        q("Biofilm-associated device infection is difficult to eradicate because biofilms:", "Limit antibiotic penetration and contain slow-growing protected cells", ["Increase drug diffusion", "Prevent adhesion", "Make bacteria unable to communicate"], "Biofilms on catheters/prostheses promote persistence and often require device removal."),
    ]),
    ("general-virology", "General Virology and Overview of Viral Infections", [
        q("A DNA virus replicates in cytoplasm rather than nucleus. Which virus family is the classic exception?", "Poxvirus", ["Herpesvirus", "Adenovirus", "Papillomavirus"], "Poxviruses carry enzymes for cytoplasmic DNA replication."),
        q("A positive-sense RNA virus enters a cell. Its genome can immediately function as:", "mRNA", ["DNA template", "Reverse transcriptase", "Capsid protein"], "Positive-sense RNA genomes are directly translated by host ribosomes."),
        q("Influenza undergoes antigenic shift because:", "Segmented genomes reassort when two strains infect the same cell", ["Point mutations stop completely", "DNA integrates into host genome", "Capsids become spores"], "Reassortment of segmented RNA can create pandemic strains."),
        q("Acyclovir selectively inhibits HSV because it requires activation by:", "Viral thymidine kinase", ["Host peptidoglycan", "Viral neuraminidase", "Bacterial beta-lactamase"], "HSV thymidine kinase phosphorylates acyclovir, enabling selective action."),
        q("A nonenveloped virus usually has which environmental property?", "Greater resistance to drying, acid, and detergents", ["Extreme fragility outside host", "Mandatory ether sensitivity", "No capsid"], "Nonenveloped capsids are generally more environmentally stable."),
        q("A patient with measles spreads infection before rash appears. This highlights that viral control often requires:", "Vaccination and isolation based on incubation/transmission biology", ["Treating only after rash", "Gram stain screening", "Antifungal prophylaxis"], "Viral infectivity may precede symptoms, making prevention crucial."),
        q("Cytopathic effect in cell culture means:", "Virus-induced morphological damage to host cells", ["Bacterial capsule swelling", "Fungal hyphae production", "Antibiotic inhibition zone"], "CPE includes rounding, syncytia, inclusion bodies, or cell lysis."),
        q("Reverse transcriptase is essential in:", "Retroviruses", ["Poxviruses", "Adenoviruses", "Reoviruses"], "Retroviruses copy RNA into DNA before integration."),
        q("A latent viral infection with later reactivation is classically seen with:", "Herpesviruses", ["Rhinoviruses only", "Noroviruses only", "Rotaviruses only"], "Herpesviruses establish latency and can reactivate under stress or immunosuppression."),
        q("Interferon-alpha/beta helps antiviral defense by:", "Inducing an antiviral state in neighboring cells", ["Digesting bacterial walls", "Neutralizing endotoxin", "Chelating iron"], "Type I interferons upregulate antiviral proteins that inhibit viral replication."),
    ]),
    ("general-parasitology", "General Parasitology and Overview of Parasitic Infections", [
        q("A stool sample shows motile trophozoites with ingested RBCs. This finding strongly suggests:", "Entamoeba histolytica", ["Giardia lamblia", "Balantidium coli", "Cryptosporidium parvum"], "Ingested RBCs in trophozoites are characteristic of invasive E. histolytica."),
        q("Peripheral eosinophilia is most associated with:", "Tissue-invasive helminth infections", ["Uncomplicated viral URI", "Pure bacterial UTI", "Latent TB"], "Helminth tissue migration often drives Th2/eosinophil responses."),
        q("The infective form of malaria transmitted by Anopheles mosquito is:", "Sporozoite", ["Merozoite", "Trophozoite", "Hypnozoite"], "Anopheles injects sporozoites, which travel to liver cells."),
        q("A patient has recurrent P. vivax malaria months after treatment. Relapse occurs due to:", "Dormant liver hypnozoites", ["Persistent intestinal cysts", "Bacterial spores", "Adult worms in colon"], "P. vivax and P. ovale can form dormant hepatic hypnozoites."),
        q("Autoinfection with potentially fatal hyperinfection is classically seen with:", "Strongyloides stercoralis", ["Enterobius vermicularis", "Taenia saginata", "Ascaris lumbricoides"], "Strongyloides can complete its life cycle within the host and disseminate with immunosuppression."),
        q("A perianal tape test is used to diagnose:", "Enterobius vermicularis", ["Echinococcus granulosus", "Plasmodium falciparum", "Leishmania donovani"], "Pinworm eggs are deposited around the anus and detected by tape test."),
        q("Hydatid cyst surgery must avoid spillage because rupture can cause:", "Anaphylaxis and secondary seeding", ["Tetanus", "Neonatal sepsis", "Meningococcemia"], "Echinococcus cyst fluid is antigenic and viable protoscolices can seed new cysts."),
        q("A parasite requiring two hosts to complete development has:", "Indirect life cycle", ["Direct life cycle", "Binary fission only", "Saprophytic cycle"], "Indirect cycles involve intermediate and definitive hosts."),
        q("Kala-azar diagnosis is supported by amastigotes in macrophages from marrow/splenic aspirate. The organism is:", "Leishmania donovani", ["Trypanosoma cruzi", "Toxoplasma gondii", "Naegleria fowleri"], "Leishmania amastigotes multiply within macrophages."),
        q("Cyst ingestion followed by excystation in the intestine is common in:", "Protozoal intestinal infections", ["All viral infections", "Only Gram-positive sepsis", "Dermatophyte infections"], "Many intestinal protozoa transmit as cysts that survive outside the host."),
    ]),
    ("general-mycology", "General Mycology and Overview of Fungal Infections", [
        q("A diabetic patient with ketoacidosis develops black nasal eschar and broad aseptate hyphae. The likely infection is:", "Mucormycosis", ["Aspergillosis", "Candidiasis", "Cryptococcosis"], "Mucorales cause rhinocerebral disease with broad ribbon-like aseptate hyphae, especially in DKA."),
        q("A fungal cell wall target absent in human cells is:", "Beta-glucan", ["Cholesterol", "Mitochondrial DNA", "Ribosomal RNA"], "Echinocandins target beta-1,3-glucan synthesis in fungal cell walls."),
        q("Amphotericin B works by binding:", "Ergosterol", ["Peptidoglycan", "Lipid A", "Mycolic acid"], "Amphotericin binds ergosterol and forms membrane pores."),
        q("India ink showing encapsulated budding yeast in CSF suggests:", "Cryptococcus neoformans", ["Candida albicans", "Aspergillus fumigatus", "Mucor species"], "Cryptococcus has a prominent polysaccharide capsule."),
        q("Germ tube test is used for presumptive identification of:", "Candida albicans", ["Cryptococcus gattii", "Aspergillus flavus", "Rhizopus"], "C. albicans forms germ tubes in serum."),
        q("Septate hyphae with acute-angle branching in an immunocompromised patient suggest:", "Aspergillus", ["Mucor", "Candida yeast only", "Pneumocystis trophozoite"], "Aspergillus shows septate hyphae with acute-angle branching."),
        q("A dimorphic fungus is best described as:", "Mold in environment and yeast or spherule-like form in tissue depending on species", ["Only yeast at all temperatures", "Only bacteria-like rods", "Virus with capsule"], "Thermally dimorphic fungi change morphology with temperature/host environment."),
        q("Dermatophytes infect skin, hair, and nails because they:", "Utilize keratin", ["Invade red blood cells", "Require anaerobic intestine", "Grow only in CSF"], "Dermatophytes are keratinophilic fungi causing superficial mycoses."),
        q("Pneumocystis jirovecii pneumonia is strongly associated with:", "Impaired cellular immunity such as advanced HIV", ["High neutrophil count", "Iron deficiency alone", "Asplenia only"], "Pneumocystis causes pneumonia in T-cell immunodeficiency."),
        q("Sabouraud dextrose agar favors fungal growth because it:", "Has acidic pH and high dextrose that inhibit many bacteria", ["Contains blood for hemolysis", "Is alkaline for Vibrio", "Contains bile salts for enterics"], "SDA is a routine fungal medium that suppresses many bacterial contaminants."),
    ]),
    ("normal-human-microbiota", "Normal Human Microbiota", [
        q("A patient develops C. difficile colitis after clindamycin. The key predisposing event is:", "Disruption of normal gut microbiota colonization resistance", ["Increased gastric acid only", "Improved anaerobic competition", "Permanent loss of spores"], "Antibiotics disrupt microbiota, allowing C. difficile overgrowth and toxin production."),
        q("The anterior nares are an important colonization site for:", "Staphylococcus aureus", ["Vibrio cholerae", "Clostridium tetani spores only", "Plasmodium falciparum"], "Nasal carriage of S. aureus is common and clinically relevant."),
        q("Normal vaginal Lactobacillus helps prevent infection mainly by:", "Maintaining acidic pH through lactic acid production", ["Producing endotoxin", "Destroying epithelial glycogen", "Increasing vaginal pH"], "Lactobacilli lower pH and inhibit pathogens."),
        q("A newborn's microbiota is shaped early by delivery mode, feeding, and environment. This matters because microbiota:", "Influences immune development and colonization resistance", ["Is always sterile until puberty", "Cannot affect pathogens", "Only lives in blood"], "Early microbiota affects metabolism, immunity, and pathogen resistance."),
        q("Skin sites differ in microbiota because microbial growth depends on:", "Moisture, sebum, oxygen, pH, and local environment", ["Blood group only", "Hair color only", "Bone marrow output only"], "Dry, moist, and sebaceous skin niches support different communities."),
        q("Bacterial vaginosis is best viewed as:", "Dysbiosis with reduced lactobacilli and increased anaerobes", ["Pure Candida invasion", "Sterile inflammation", "Normal puberty finding always"], "BV is a microbiota imbalance, not simply one invasive pathogen."),
        q("A urinary catheter increases UTI risk partly because it:", "Bypasses host barriers and provides a surface for biofilm", ["Sterilizes periurethral flora", "Prevents bacterial adhesion", "Produces antibiotics"], "Devices disrupt defenses and allow biofilm-associated infection."),
        q("Oral streptococci contribute to dental caries by:", "Producing acid from carbohydrates that demineralizes enamel", ["Making alkaline urine", "Invading red cells", "Blocking saliva permanently"], "Cariogenic bacteria ferment sugars to acids, damaging enamel."),
        q("Fecal microbiota transplantation can treat recurrent C. difficile by:", "Restoring diverse colonization resistance", ["Directly neutralizing tetanus toxin", "Killing all spores with heat", "Replacing vancomycin in fulminant shock always"], "FMT re-establishes a protective gut microbial ecosystem."),
        q("The bloodstream is normally:", "Sterile", ["Dense with anaerobes", "Colonized by dermatophytes", "Filled with cysts"], "Blood should not contain resident microbiota; positive cultures require interpretation for true bacteremia vs contamination."),
    ]),
    ("epidemiology-infectious-diseases", "Epidemiology of Infectious Diseases", [
        q("An outbreak investigation shows all cases ate from the same contaminated food item. This is a:", "Common source outbreak", ["Propagated outbreak only", "Sporadic case", "Endemic carrier state"], "Common source outbreaks arise from exposure to the same source."),
        q("A disease constantly present at expected frequency in a region is:", "Endemic", ["Pandemic", "Sporadic", "Eradicated"], "Endemic disease persists at baseline levels in a population."),
        q("The basic reproduction number R0 represents:", "Average secondary cases caused by one case in a fully susceptible population", ["Case fatality rate", "Incubation period", "Culture positivity rate"], "R0 reflects transmissibility under fully susceptible conditions."),
        q("Herd immunity protects susceptible individuals when:", "Enough people are immune to interrupt transmission", ["Everyone is infected", "No one is vaccinated", "Pathogens become larger"], "Population immunity reduces effective spread."),
        q("A diagnostic test with very high sensitivity is most useful to:", "Rule out disease when negative", ["Confirm disease when positive always", "Measure mortality", "Replace clinical judgment"], "Sensitive tests have few false negatives; SnNout is the classic principle."),
        q("A test with very high specificity is most useful to:", "Rule in disease when positive", ["Exclude disease when negative always", "Estimate incubation", "Prevent infection directly"], "Specific tests have few false positives; SpPin is the classic principle."),
        q("A carrier who transmits Salmonella Typhi despite no symptoms is an example of:", "Asymptomatic carrier state", ["Vector-only transmission", "Dead-end host", "Sterile colonization"], "Carriers can maintain and transmit pathogens without active disease."),
        q("Infection acquired in a hospital after admission is called:", "Healthcare-associated infection", ["Zoonosis only", "Congenital infection", "Iatrogenic immunity"], "Healthcare-associated infections occur in care settings and relate to procedures, devices, or exposure."),
        q("Quarantine differs from isolation because quarantine applies to:", "Exposed but not yet ill individuals", ["Confirmed infectious cases only", "Sterile instruments", "Vaccinated healthcare workers only"], "Quarantine separates exposed persons during incubation; isolation separates infectious cases."),
        q("A mosquito transmitting malaria from one host to another is a:", "Biological vector", ["Fomite", "Vehicle only", "Reservoir-free agent"], "Anopheles mosquitoes are biological vectors because the parasite develops within them."),
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
            questions.append({**BASE, "id": f"micro-general-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "microbiology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 8 or len(questions) != 80:
        raise AssertionError(f"Expected 8 topics and 80 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 80:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
