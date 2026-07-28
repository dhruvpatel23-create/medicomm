import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Bloodstream and Cardiovascular System Infections"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("cardiovascular-infections", "Cardiovascular System Infections: Infective Endocarditis and Acute Rheumatic Fever", [
        q("A patient with prosthetic valve fever has multiple positive blood cultures with coagulase-negative staphylococci. The most likely pathogen is:", "Staphylococcus epidermidis", ["Streptococcus pyogenes", "Corynebacterium diphtheriae", "Vibrio cholerae"], "Coagulase-negative staphylococci form biofilms on prosthetic valves and devices."),
        q("An IV drug user has fever, septic pulmonary emboli, and a new murmur. Which valve is most often involved?", "Tricuspid valve", ["Mitral valve", "Aortic valve", "Pulmonary valve only"], "Right-sided endocarditis, especially tricuspid, is classic in injection drug use."),
        q("A dental-procedure-associated subacute endocarditis in a patient with damaged valve is most classically due to:", "Viridans streptococci", ["Neisseria meningitidis", "Clostridium tetani", "Shigella dysenteriae"], "Viridans streptococci from oral flora adhere to abnormal valves."),
        q("Duke criteria for infective endocarditis rely heavily on:", "Positive blood cultures and echocardiographic evidence", ["Urine culture only", "Stool ova test", "Widal titer alone"], "Major Duke criteria include typical blood cultures and endocardial involvement."),
        q("Culture-negative endocarditis after prior antibiotics should raise suspicion for:", "Fastidious organisms or partially treated infection", ["Absence of infection always", "Only viral myocarditis", "Sterile thrombus only"], "Prior antibiotics and fastidious agents can make blood cultures negative."),
        q("Acute rheumatic fever follows pharyngitis due to:", "Group A Streptococcus", ["Enterococcus faecalis", "Staphylococcus epidermidis", "Candida albicans"], "Rheumatic fever is an immune sequela of S. pyogenes pharyngitis."),
        q("The pathogenesis of acute rheumatic fever is best explained by:", "Molecular mimicry between streptococcal and host antigens", ["Direct bacterial invasion of valves", "Toxin-mediated diarrhea", "Fungal biofilm"], "Cross-reactive immune responses damage heart, joints, skin, and CNS."),
        q("Aschoff bodies are characteristic lesions of:", "Rheumatic carditis", ["Bacterial myocarditis due to diphtheria", "Viral hemorrhagic fever", "Malaria"], "Aschoff bodies are granulomatous lesions seen in rheumatic heart disease."),
        q("Janeway lesions in endocarditis are:", "Painless vascular lesions on palms and soles", ["Painful fingertip nodules", "Retinal hemorrhages only", "Oral Koplik spots"], "Janeway lesions are painless embolic/vascular phenomena."),
        q("Long-term penicillin prophylaxis after rheumatic fever aims to:", "Prevent recurrent streptococcal pharyngitis and valve damage", ["Treat existing valve calcification", "Sterilize blood forever", "Prevent malaria"], "Recurrent GAS infections worsen rheumatic heart disease risk."),
    ]),
    ("bloodstream-infections", "Bloodstream Infections (Including Infections Causing Anemia)", [
        q("A patient has fever, hypotension, high lactate, and positive blood culture. The syndrome is:", "Sepsis due to bloodstream infection", ["Simple colonization", "Sterile pyuria", "Latent infection"], "Sepsis is life-threatening organ dysfunction from dysregulated response to infection."),
        q("Two blood culture sets are recommended before antibiotics because they:", "Increase yield and help distinguish contamination from true bacteremia", ["Guarantee antibiotic susceptibility", "Replace clinical assessment", "Prevent fever"], "Multiple sets improve interpretation of bloodstream isolates."),
        q("Coagulase-negative staphylococcus in one of four blood culture bottles most often suggests:", "Possible contamination requiring clinical correlation", ["Always fatal sepsis", "Malaria", "Enteric fever"], "Skin commensals may contaminate blood cultures unless repeatedly isolated or device-associated."),
        q("A septic patient should receive empiric antibiotics after cultures because delay:", "Increases mortality in severe sepsis and shock", ["Improves culture yield indefinitely", "Prevents resistance", "Sterilizes devices"], "Early appropriate antimicrobial therapy is critical in sepsis."),
        q("A patient with hemolytic anemia after Mycoplasma pneumoniae infection has cold agglutinins targeting:", "I antigen on red cells", ["D antigen", "Kell antigen", "Duffy antigen"], "Mycoplasma can induce IgM cold agglutinins causing hemolysis."),
        q("Parvovirus B19 causes severe aplastic crisis in sickle cell disease by infecting:", "Erythroid precursors", ["Neutrophils", "Platelets only", "Endothelial cells only"], "B19 targets erythroid progenitors via P antigen."),
        q("Blackwater fever is severe hemolysis classically associated with:", "Falciparum malaria", ["Enterobiasis", "Diphtheria", "Cholera"], "Massive intravascular hemolysis can complicate severe P. falciparum malaria."),
        q("A febrile neutropenic patient with suspected bacteremia needs:", "Immediate broad-spectrum antipseudomonal coverage", ["Wait for culture finalization", "Only oral rehydration", "No antibiotics if no focus"], "Neutropenic sepsis can deteriorate quickly and needs urgent empiric therapy."),
        q("Catheter-related bloodstream infection is best prevented by:", "Aseptic insertion, hub care, chlorhexidine skin antisepsis, and early removal", ["Routine antibiotics for all lines", "Using femoral lines always", "No hand hygiene if gloves used"], "CLABSI prevention depends on insertion and maintenance bundles."),
        q("Persistent Staphylococcus aureus bacteremia should prompt evaluation for:", "Endocarditis or deep metastatic focus", ["Simple contamination only", "Giardiasis", "Food poisoning only"], "S. aureus bacteremia often seeds valves, bones, and devices."),
    ]),
    ("enteric-fever", "Enteric Fever (Salmonella Typhi and Salmonella Paratyphi)", [
        q("A traveler has step-ladder fever, abdominal symptoms, relative bradycardia, and rose spots. The likely diagnosis is:", "Enteric fever", ["Cholera", "Tetanus", "Gas gangrene"], "Typhoid/paratyphoid fever causes systemic febrile illness after intestinal invasion."),
        q("The best diagnostic test in the first week of typhoid fever is:", "Blood culture", ["Widal test alone", "Stool culture only after cure", "Urine microscopy"], "Blood culture yield is highest early before antibodies rise."),
        q("Widal test is difficult to interpret because:", "Baseline antibodies, vaccination, and cross-reactions can cause false results", ["It cultures Salmonella directly", "It detects only malaria", "It is positive before infection always"], "Widal needs paired titers/local baseline and clinical correlation."),
        q("Salmonella Typhi survives in macrophages partly because it:", "Resists intracellular killing", ["Forms spores", "Has no cell wall", "Is an obligate virus"], "Typhi is a facultative intracellular pathogen."),
        q("A chronic carrier of Salmonella Typhi commonly harbors organisms in:", "Gallbladder", ["Lung apex", "Skin only", "Prostate only"], "Chronic biliary carriage is associated with gallbladder colonization/gallstones."),
        q("Typhoid intestinal perforation usually involves:", "Peyer's patches in ileum", ["Gastric fundus", "Appendix only", "Rectal valves"], "Necrosis of ileal Peyer's patches can cause bleeding/perforation."),
        q("Vi antigen in Salmonella Typhi is a:", "Capsular virulence antigen", ["Flagellar H antigen", "Somatic O antigen", "Exotoxin"], "Vi capsular antigen helps resist phagocytosis and is used in vaccines."),
        q("Empiric therapy for enteric fever should consider:", "Local resistance patterns", ["Only Gram stain shape", "Patient blood group", "Widal single titer only"], "Fluoroquinolone, ceftriaxone, and azithromycin choices depend on resistance."),
        q("Relapse of typhoid after treatment occurs because:", "Organisms may persist intracellularly or in biliary sites", ["Antibodies destroy antibiotics", "It becomes viral", "Spores germinate"], "Relapse reflects incomplete eradication in some patients."),
        q("Public health prevention of typhoid focuses on:", "Safe water, sanitation, food hygiene, and vaccination for risk groups", ["Mosquito nets only", "Dog vaccination", "Avoiding all milk"], "Typhoid spreads fecal-orally through contaminated food/water."),
    ]),
    ("rickettsial-infections", "Rickettsial Infections", [
        q("A patient has fever, severe headache, rash, and history of tick exposure. Rickettsial infection is suspected. First-line treatment is:", "Doxycycline", ["Acyclovir", "Amphotericin B", "Penicillin V only"], "Doxycycline is treatment of choice for most rickettsial infections, including children when severe."),
        q("Rickettsiae primarily infect:", "Vascular endothelial cells", ["Red cells only", "Neurons only", "Intestinal villi only"], "Endothelial infection causes vasculitis, rash, edema, and organ injury."),
        q("An eschar at the bite site with fever suggests:", "Scrub typhus or spotted fever group rickettsiosis", ["Cholera", "Tetanus", "Enterobiasis"], "Eschar is a necrotic inoculation lesion seen in several rickettsioses."),
        q("Weil-Felix test is based on cross-reactivity between rickettsiae and:", "Proteus antigens", ["Salmonella O antigen", "Vibrio O1 antigen", "Candida mannan"], "Weil-Felix is an older, nonspecific agglutination test using Proteus strains."),
        q("Scrub typhus is transmitted by:", "Chigger mite larvae", ["Anopheles mosquito", "Sandfly", "Tsetse fly"], "Orientia tsutsugamushi is transmitted by trombiculid mite larvae."),
        q("Epidemic typhus is transmitted by:", "Body louse", ["Hard tick only", "Flea from rats only", "Mosquito"], "Rickettsia prowazekii spreads via body louse feces."),
        q("Murine typhus is classically associated with:", "Rat fleas", ["Dog bite", "Freshwater snails", "Undercooked pork"], "Rickettsia typhi is flea-borne, often rodent-associated."),
        q("A negative early serology does not exclude rickettsial disease because:", "Antibodies may appear only after the first week", ["Rickettsiae never induce antibodies", "Doxycycline prevents testing forever", "Serology detects only bacteria in stool"], "Treatment should not wait for seroconversion when clinical suspicion is high."),
        q("Severe rickettsial disease can cause multiorgan dysfunction through:", "Widespread vasculitis and capillary leak", ["Botulinum toxin", "Urease production", "Mucosal invasion only"], "Endothelial injury drives vascular leakage and organ ischemia."),
        q("Rickettsial infections are often missed clinically because they:", "Present as nonspecific acute febrile illness", ["Always have pathognomonic rash", "Never cause fever", "Only infect neonates"], "High suspicion is needed in endemic areas and exposure history."),
    ]),
    ("misc-bacterial-bsi", "Miscellaneous Bacterial Bloodstream Infections: Brucellosis, Leptospirosis and Borreliosis", [
        q("A veterinarian has undulating fever, sweats, arthralgia, and hepatosplenomegaly. The likely diagnosis is:", "Brucellosis", ["Cholera", "Diphtheria", "Pertussis"], "Brucella causes zoonotic systemic infection with undulant fever."),
        q("Brucella infection is commonly acquired from:", "Unpasteurized dairy or animal exposure", ["Mosquito bite", "Contaminated needles only", "Air conditioning water"], "Brucellosis is linked to livestock exposure and unpasteurized milk products."),
        q("Brucella is difficult to eradicate because it:", "Survives intracellularly in macrophages", ["Forms endospores", "Is an obligate virus", "Has no genome"], "Intracellular survival requires combination therapy and prolonged treatment."),
        q("A farmer has fever, conjunctival suffusion, calf tenderness, jaundice, and renal failure after floodwater exposure. The likely infection is:", "Leptospirosis", ["Relapsing fever", "Typhoid", "Scrub typhus"], "Leptospira spreads via animal urine-contaminated water and can cause Weil disease."),
        q("The severe icteric form of leptospirosis is called:", "Weil disease", ["Brill-Zinsser disease", "Carrion disease", "Pontiac fever"], "Weil disease includes jaundice, renal failure, hemorrhage, and shock."),
        q("Leptospira is best described morphologically as:", "Thin spirochete with hooked ends", ["Gram-positive cocci in chains", "Acid-fast bacillus", "Budding yeast"], "Leptospira are tightly coiled spirochetes with hooked ends."),
        q("Relapsing fever due to Borrelia shows recurrent fever spikes because of:", "Antigenic variation", ["Spore germination", "Lactose fermentation", "Toxin neutralization"], "Borrelia changes surface antigens, causing relapsing febrile episodes."),
        q("Lyme disease early localized infection classically presents with:", "Erythema migrans", ["Rose spots", "Eschar only", "Pseudomembrane"], "Borrelia burgdorferi causes expanding erythema migrans after Ixodes tick bite."),
        q("Jarisch-Herxheimer reaction after treating spirochetal infection is:", "Acute inflammatory worsening from organism lysis", ["IgE anaphylaxis to penicillin only", "Chronic carrier state", "Drug resistance"], "Rapid spirochete killing can trigger fever, rigors, hypotension, and symptom worsening."),
        q("Prevention of leptospirosis after floods focuses on:", "Avoiding contaminated water and rodent control", ["Typhoid vaccination only", "Mosquito nets only", "Avoiding pasteurized milk"], "Leptospira is maintained in animal reservoirs, especially rodents."),
    ]),
    ("hiv-aids", "HIV/AIDS", [
        q("HIV primarily infects CD4 cells by binding CD4 plus:", "CCR5 or CXCR4 coreceptors", ["CD20", "TLR4", "Duffy antigen"], "HIV entry requires CD4 and a chemokine coreceptor."),
        q("The enzyme targeted by integrase inhibitors is needed for:", "Insertion of viral DNA into host genome", ["Viral attachment only", "Capsid uncoating only", "gp120 shedding"], "Integrase inserts reverse-transcribed HIV DNA into host chromosomes."),
        q("A patient with suspected acute HIV has negative antibody test but high viral RNA. This occurs because:", "Viremia precedes seroconversion", ["HIV never induces antibodies", "RNA tests detect bacteria", "Antibody tests are always useless"], "Acute HIV may be antibody-negative during the window period."),
        q("Pneumocystis pneumonia prophylaxis is recommended when CD4 count falls below:", "200 cells/µL", ["500 cells/µL", "1000 cells/µL", "800 cells/µL"], "CD4 <200 is a major threshold for PCP prophylaxis."),
        q("Toxoplasma encephalitis risk rises especially when CD4 count is below:", "100 cells/µL", ["700 cells/µL", "450 cells/µL", "300 cells/µL"], "Toxoplasma prophylaxis is considered at CD4 <100 with IgG positivity."),
        q("Disseminated MAC prophylaxis historically applies at CD4 count below:", "50 cells/µL", ["600 cells/µL", "350 cells/µL", "200 cells/µL"], "MAC risk increases with profound immunosuppression."),
        q("The best marker for monitoring immediate ART response is:", "Plasma HIV viral load", ["ESR", "Widal titer", "ASO titer"], "Viral load falls with effective ART and detects failure earlier than CD4 alone."),
        q("Opportunistic infections in AIDS mainly reflect loss of:", "Cell-mediated immunity", ["Complement terminal components only", "IgE only", "Platelets"], "CD4 T-cell depletion impairs cellular immune defense."),
        q("HIV post-exposure prophylaxis should be started:", "As soon as possible after significant exposure", ["After seroconversion", "Only after 6 months", "Only if symptoms appear"], "PEP efficacy is time-sensitive and should begin promptly."),
        q("Prevention of mother-to-child HIV transmission depends strongly on:", "Maternal ART and viral load suppression", ["Avoiding all vaccines", "Giving antibiotics only at birth", "No antenatal testing"], "ART during pregnancy and delivery greatly reduces vertical transmission."),
    ]),
    ("viral-hemorrhagic-fever", "Viral Hemorrhagic Fever (VHF) Arboviral VHF, Filoviral VHF, Hantaviral and Other Agents of VHF", [
        q("Dengue severe disease is characterized by:", "Plasma leakage, thrombocytopenia, and hemorrhagic manifestations", ["Pseudomembrane", "Spastic paralysis", "Rose spots only"], "Severe dengue involves vascular leakage and bleeding risk."),
        q("A dengue patient with falling fever, abdominal pain, vomiting, and rising hematocrit is entering:", "Critical phase with plasma leakage", ["Convalescent phase only", "Latent phase", "Carrier phase"], "Defervescence can mark the critical leakage phase in dengue."),
        q("Aedes mosquito control is central for dengue because Aedes breeds commonly in:", "Clean stagnant water containers", ["Fast-flowing rivers only", "Dry dust", "Deep seawater"], "Aedes aegypti breeds in domestic water collections."),
        q("Chikungunya differs clinically from dengue by prominent:", "Severe persistent arthralgia", ["Pseudomembrane", "Hydrophobia", "Tetanus spasms"], "Chikungunya often causes severe joint pain that may persist."),
        q("Ebola virus disease requires strict isolation because transmission occurs through:", "Contact with blood and body fluids", ["Routine airborne spread over long distances only", "Mosquito bites", "Food toxin ingestion"], "Filoviruses spread through infected body fluids and require PPE/barrier nursing."),
        q("Hantavirus pulmonary syndrome is linked to exposure to:", "Rodent excreta aerosols", ["Cat scratches", "Tick saliva only", "Undercooked fish"], "Hantaviruses are transmitted from rodent urine/feces/saliva aerosols."),
        q("Ribavirin is useful for some hemorrhagic fevers, especially:", "Lassa fever", ["Dengue", "Chikungunya", "Ebola in all cases"], "Ribavirin has benefit in Lassa fever when given early."),
        q("In suspected VHF sample handling, the key laboratory principle is:", "High biosafety precautions and notification", ["Routine open bench processing", "No labeling", "Centrifuge without containment"], "VHF specimens require strict biosafety to protect lab staff."),
        q("Dengue secondary infection can be more severe due to:", "Antibody-dependent enhancement", ["Complete viral latency", "Bacterial toxin conversion", "Spore formation"], "Non-neutralizing antibodies can enhance Fc-mediated viral entry."),
        q("The most important initial management of dengue shock is:", "Careful isotonic fluid resuscitation guided by leakage status", ["Immediate aspirin", "High-dose anticoagulation", "No monitoring"], "Dengue shock is managed with judicious fluids and avoidance of NSAIDs."),
    ]),
    ("malaria-babesiosis", "Malaria and Babesiosis", [
        q("A patient returning from Africa has fever, altered sensorium, and high parasitemia. The most likely species is:", "Plasmodium falciparum", ["P. malariae", "P. ovale", "Babesia microti"], "P. falciparum causes severe malaria including cerebral malaria."),
        q("Fever periodicity in malaria results from:", "Synchronous rupture of infected red cells", ["Mosquito bite timing", "Liver capsule rupture", "Antibody class switching"], "RBC schizont rupture releases merozoites and inflammatory mediators."),
        q("Banana-shaped gametocytes on smear suggest:", "Plasmodium falciparum", ["P. vivax", "P. malariae", "Babesia"], "Crescent/banana gametocytes are characteristic of P. falciparum."),
        q("Schuffner dots are classically seen in RBCs infected with:", "P. vivax", ["P. falciparum mature trophozoites", "Babesia", "Trypanosoma"], "P. vivax enlarges RBCs and shows Schuffner stippling."),
        q("Primaquine is needed in P. vivax infection to eliminate:", "Hypnozoites in liver", ["Adult worms", "Bacterial spores", "RBC merozoites only"], "Radical cure requires hypnozoite eradication."),
        q("G6PD testing before primaquine is important because primaquine can cause:", "Hemolysis", ["Ototoxicity", "Tendon rupture", "Kernicterus in adults"], "Oxidant drugs can trigger hemolysis in G6PD deficiency."),
        q("Severe falciparum malaria is treated with:", "Intravenous artesunate", ["Oral acyclovir", "Single-dose albendazole", "Topical amphotericin"], "IV artesunate rapidly reduces parasite burden in severe malaria."),
        q("Babesiosis smear may show:", "Maltese cross tetrads", ["Banana gametocytes", "Negri bodies", "Safety-pin bacilli"], "Babesia can form tetrads in RBCs and causes malaria-like illness."),
        q("Babesiosis is especially severe in patients with:", "Asplenia", ["Appendectomy", "Atopy", "Myopia"], "The spleen clears infected RBCs; asplenia increases severity."),
        q("Malaria control includes insecticide-treated nets because transmission is by:", "Female Anopheles mosquito", ["Aedes mosquito", "Sandfly", "Tsetse fly"], "Anopheles mosquitoes transmit Plasmodium sporozoites."),
    ]),
    ("leishmaniasis-trypanosomiasis", "Visceral Leishmaniasis and Trypanosomiasis", [
        q("A patient with prolonged fever, weight loss, massive splenomegaly, and pancytopenia in Bihar has:", "Visceral leishmaniasis", ["Cholera", "Tetanus", "Enterobiasis"], "Kala-azar due to Leishmania donovani causes fever, cachexia, hepatosplenomegaly, and cytopenias."),
        q("Leishmania is transmitted by:", "Sandfly", ["Anopheles mosquito", "Tsetse fly for kala-azar", "Body louse"], "Phlebotomine sandflies transmit Leishmania."),
        q("The diagnostic tissue form of Leishmania in macrophages is:", "Amastigote", ["Promastigote", "Sporozoite", "Trophozoite with RBCs"], "Amastigotes are intracellular LD bodies in macrophages."),
        q("rk39 rapid test is used for diagnosis of:", "Visceral leishmaniasis", ["Malaria", "Typhoid", "Filariasis"], "rk39 detects antibodies useful in kala-azar diagnosis in appropriate settings."),
        q("Post-kala-azar dermal leishmaniasis is epidemiologically important because:", "It can act as a reservoir for transmission", ["It always means cure", "It is caused by bacteria", "It prevents relapse"], "PKDL patients may maintain parasites in the community."),
        q("African sleeping sickness is transmitted by:", "Tsetse fly", ["Sandfly", "Aedes mosquito", "Rat flea"], "Trypanosoma brucei is transmitted by Glossina flies."),
        q("Winterbottom sign in African trypanosomiasis refers to:", "Posterior cervical lymphadenopathy", ["Splenic rupture", "Perianal itching", "Conjunctival suffusion"], "Posterior cervical lymph node enlargement is a classic sign."),
        q("Chagas disease is transmitted by:", "Triatomine bug feces contaminating bite or mucosa", ["Tsetse fly saliva", "Sandfly bite", "Snail penetration"], "T. cruzi spreads when infected bug feces contaminate breaks/mucosa."),
        q("Romana sign in Chagas disease is:", "Unilateral periorbital swelling", ["Eschar", "Rose spot", "Bull neck"], "Conjunctival inoculation of T. cruzi can cause Romana sign."),
        q("Chronic Chagas disease classically causes:", "Dilated cardiomyopathy and megacolon/megaesophagus", ["Hydatid cysts", "Cerebral malaria", "Filariasis hydrocele"], "T. cruzi damages cardiac and enteric nervous systems chronically."),
    ]),
    ("lymphatic-filariasis", "Lymphatic Filariasis", [
        q("Lymphatic filariasis in India is most commonly caused by:", "Wuchereria bancrofti", ["Onchocerca volvulus", "Loa loa", "Trichinella spiralis"], "W. bancrofti is the major cause of lymphatic filariasis in India."),
        q("The vector for Wuchereria bancrofti in many Indian urban settings is:", "Culex mosquito", ["Sandfly", "Tsetse fly", "Hard tick"], "Culex quinquefasciatus is an important vector."),
        q("Night blood sample is collected for filariasis because microfilariae show:", "Nocturnal periodicity", ["Acid-fastness", "Daytime spore formation", "Thermal dimorphism"], "W. bancrofti microfilariae circulate more at night in many regions."),
        q("Hydrocele and elephantiasis result mainly from:", "Chronic lymphatic obstruction and inflammation", ["RBC invasion", "Hepatic hypnozoites", "Intestinal toxin"], "Adult worms in lymphatics cause lymphangitis and chronic lymphedema."),
        q("A rapid card test detecting circulating filarial antigen is useful because it:", "Can diagnose active W. bancrofti infection without relying on night smear", ["Identifies malaria species", "Measures eosinophil count", "Detects adult worm motility directly"], "Antigen tests improve detection of bancroftian filariasis."),
        q("Diethylcarbamazine acts against filarial parasites and can cause reactions due to:", "Inflammation after microfilarial killing", ["Viral lysis", "Endotoxin from Gram-negative rods", "Fungal ergosterol release"], "Killing microfilariae can provoke fever, rash, and local reactions."),
        q("Mass drug administration for filariasis aims to:", "Reduce community microfilaria reservoir and interrupt transmission", ["Treat only symptomatic elephantiasis", "Kill mosquitoes directly", "Diagnose all hydroceles"], "MDA reduces human parasite reservoir for mosquito transmission."),
        q("Tropical pulmonary eosinophilia is an immune response associated with:", "Filarial infection", ["Typhoid", "Dengue", "Cholera"], "TPE is hypersensitivity to filarial antigens with cough, wheeze, and eosinophilia."),
        q("Microfilaria of W. bancrofti is:", "Sheathed with nuclei not extending to tail tip", ["Unsheathed with nuclei to tail tip", "Acid-fast rod", "Cyst with four nuclei"], "Tail nuclei pattern helps distinguish filarial species."),
        q("Morbidity management in chronic filariasis includes:", "Limb hygiene, skin care, exercise, and treatment of secondary bacterial infection", ["Only antimalarial therapy", "No local care", "Immediate amputation for all"], "Chronic lymphedema care reduces acute attacks and disability."),
    ]),
    ("systemic-candidiasis-mycoses", "Systemic Candidiasis and Systemic Mycoses", [
        q("A neutropenic ICU patient with central line and persistent fever grows Candida in blood. The diagnosis is:", "Candidemia", ["Oral thrush only", "Dermatophytosis", "Colonization always"], "Candida in blood is clinically significant and needs treatment/source control."),
        q("A key risk factor for invasive candidiasis is:", "Central venous catheter and broad-spectrum antibiotics", ["Brief handwashing", "Normal neutrophil count only", "BCG vaccination"], "Devices, antibiotics, TPN, surgery, and immunosuppression predispose to candidemia."),
        q("Initial therapy for many critically ill candidemia patients is:", "Echinocandin", ["Oseltamivir", "Albendazole", "Doxycycline only"], "Echinocandins are preferred initial therapy in many invasive candidiasis settings."),
        q("Candida albicans forms germ tubes due to:", "Yeast-to-hypha transition", ["Capsule swelling", "Acid-fastness", "Spore staining"], "Germ tube formation helps identify C. albicans/dubliniensis."),
        q("Persistent candidemia requires evaluation for:", "Endophthalmitis, endocarditis, and infected catheters", ["Only pinworm", "Typhoid carrier state", "Dengue shock"], "Candida can seed eyes, valves, and devices; source control is essential."),
        q("Histoplasma infection is acquired by inhaling:", "Microconidia from soil enriched with bird/bat droppings", ["Mosquito sporozoites", "Sandfly promastigotes", "Cysts in water"], "Histoplasma grows in soil with bird/bat droppings and infects lungs."),
        q("Cryptococcus neoformans meningitis is associated with:", "Pigeon droppings and impaired cellular immunity", ["Tick bite", "Freshwater snails", "Undercooked pork"], "Cryptococcus is encapsulated yeast causing meningitis, especially in AIDS."),
        q("Mucormycosis is strongly associated with:", "Diabetic ketoacidosis", ["Hypocalcemia only", "Atopic rhinitis", "Iron deficiency alone"], "Mucorales thrive in DKA/high iron states and invade vessels."),
        q("Aspergillus invades blood vessels causing:", "Thrombosis, infarction, and hemoptysis", ["Watery diarrhea only", "Hydrocele", "Rose spots"], "Angioinvasion is characteristic in invasive aspergillosis."),
        q("Dimorphic systemic fungi generally exist as:", "Mold in environment and yeast/spherule-like tissue form depending on species", ["Only bacteria", "Only viruses", "Only protozoal cysts"], "Thermal dimorphism helps systemic fungi adapt to host and environment."),
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
            questions.append({**BASE, "id": f"micro-blood-cv-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

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
