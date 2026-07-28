import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Skin, Soft Tissue and Musculoskeletal System Infections"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("sst-msk-syndromes", "Infective Syndromes of Skin, Soft Tissue and Musculoskeletal Systems", [
        q("A patient has diffuse erythema, warmth, edema, and pain of the lower leg without a sharp raised border. The syndrome is:", "Cellulitis", ["Impetigo", "Erysipelas", "Mycetoma"], "Cellulitis involves deeper dermis/subcutaneous tissue and has less sharply demarcated margins than erysipelas."),
        q("A child has honey-colored crusted lesions around the mouth. The syndrome is:", "Impetigo", ["Necrotizing fasciitis", "Septic arthritis", "Tinea corporis"], "Impetigo is a superficial bacterial infection, commonly due to S. aureus or S. pyogenes."),
        q("Severe pain out of proportion, bullae, crepitus, and systemic toxicity after minor trauma suggest:", "Necrotizing fasciitis", ["Simple folliculitis", "Molluscum contagiosum", "Scabies"], "Necrotizing soft tissue infection is a surgical emergency."),
        q("A diabetic patient has a chronic foot ulcer probing to bone. The infection to suspect is:", "Osteomyelitis", ["Erysipelas only", "Viral exanthem", "Tinea versicolor"], "Contiguous spread from chronic ulcers can involve bone."),
        q("Acute hot swollen knee with fever should be aspirated urgently because:", "Septic arthritis can rapidly destroy cartilage", ["All cases are gout", "Blood culture is never useful", "Joint aspiration sterilizes the joint"], "Septic arthritis requires prompt diagnosis and drainage/antibiotics."),
        q("A child has fever and metaphyseal bone pain after bacteremia. The likely syndrome is:", "Acute hematogenous osteomyelitis", ["Cellulitis", "Mycetoma", "Molluscum"], "Children commonly develop hematogenous osteomyelitis in metaphyses."),
        q("A bite wound on the hand is high risk because:", "Deep inoculation into tendon sheaths and joints can cause polymicrobial infection", ["Human saliva is sterile", "Bites never need irrigation", "Skin flora cannot infect hands"], "Bite wounds need irrigation, assessment, and targeted prophylaxis/treatment when indicated."),
        q("A painless chronic draining sinus with grains from foot swelling after thorn injury suggests:", "Mycetoma", ["Erysipelas", "Herpes zoster", "Scalded skin syndrome"], "Mycetoma causes tumefaction, draining sinuses, and grains, due to actinomycetes or fungi."),
        q("The most important initial management in suspected necrotizing fasciitis is:", "Urgent surgical exploration/debridement plus broad antibiotics", ["Topical antibiotic only", "Wait for culture final report", "Steroid monotherapy"], "Source control is lifesaving; antibiotics alone are insufficient."),
        q("A purulent abscess is best managed primarily by:", "Incision and drainage", ["Only oral antihistamine", "No drainage to avoid spread", "Antiviral therapy"], "Drainage is key for abscess source control; antibiotics depend on severity/risk."),
    ]),
    ("staphylococcal-infections", "Staphylococcal Infections", [
        q("A Gram-positive coccus in clusters is catalase and coagulase positive. The organism is:", "Staphylococcus aureus", ["Streptococcus pyogenes", "Enterococcus faecalis", "Staphylococcus epidermidis"], "Coagulase positivity distinguishes S. aureus from most coagulase-negative staphylococci."),
        q("A child develops bullous impetigo with fragile blisters. The toxin targets:", "Desmoglein-1", ["Elastin", "Collagen IV", "Myelin"], "S. aureus exfoliative toxins cleave desmoglein-1."),
        q("Scalded skin syndrome differs from bullous impetigo because it:", "Is toxin-mediated at distant sites and bullae are sterile", ["Always has organisms in every blister", "Is caused by S. pyogenes", "Only affects adults"], "Circulating exfoliative toxin causes widespread epidermal splitting."),
        q("A tampon user has fever, hypotension, diffuse rash, and later desquamation. The toxin is:", "TSST-1 superantigen", ["Alpha toxin", "Botulinum toxin", "Diphtheria toxin"], "Toxic shock syndrome toxin is a superantigen causing cytokine storm."),
        q("MRSA resistance is mediated by:", "Altered penicillin-binding protein PBP2a encoded by mecA", ["Beta-lactamase only", "Loss of peptidoglycan", "VanA D-Ala-D-Lac"], "mecA confers methicillin resistance via low-affinity PBP2a."),
        q("A furuncle is infection of:", "Hair follicle extending into surrounding tissue", ["Nail plate only", "Lymphatic vessel", "Bone cortex"], "Furuncles are deep follicular abscesses commonly caused by S. aureus."),
        q("Panton-Valentine leukocidin is associated with:", "Necrotic skin abscesses and severe community MRSA disease", ["Cholera", "Leprosy anesthesia", "Tinea versicolor"], "PVL damages leukocytes and is linked to recurrent abscesses/necrotizing pneumonia."),
        q("S. epidermidis is important in prosthetic joint infection because it:", "Forms biofilm on foreign material", ["Produces exfoliative toxin", "Is coagulase positive", "Forms spores"], "Coagulase-negative staphylococci adhere to devices and form biofilms."),
        q("S. saprophyticus is best known for:", "Urinary tract infection in young women", ["Gas gangrene", "Scarlet fever", "Kala-azar"], "S. saprophyticus is a novobiocin-resistant cause of uncomplicated UTI."),
        q("Food poisoning due to S. aureus has rapid vomiting because:", "Preformed heat-stable enterotoxin is ingested", ["Bacteria invade colon", "Spores germinate in muscle", "Toxin blocks acetylcholine release"], "Short incubation vomiting follows ingestion of preformed enterotoxin."),
    ]),
    ("beta-hemolytic-streptococci", "Beta-hemolytic Streptococcal Infections", [
        q("A child has pharyngitis followed by fever and migratory polyarthritis weeks later. The original agent was:", "Streptococcus pyogenes", ["Staphylococcus aureus", "Enterococcus faecalis", "Corynebacterium jeikeium"], "Group A streptococcal pharyngitis can trigger rheumatic fever."),
        q("S. pyogenes is identified as group A by:", "Lancefield carbohydrate antigen", ["Coagulase", "Optochin sensitivity", "Acid-fast stain"], "Lancefield grouping classifies beta-hemolytic streptococci by cell wall carbohydrate."),
        q("Bacitracin sensitivity and PYR positivity support identification of:", "Group A Streptococcus", ["Group B Streptococcus", "Streptococcus pneumoniae", "Viridans streptococci"], "GAS is classically bacitracin sensitive and PYR positive."),
        q("A neonate develops sepsis and meningitis. Beta-hemolytic streptococcus with CAMP positivity suggests:", "Streptococcus agalactiae", ["Streptococcus pyogenes", "Enterococcus faecium", "Staphylococcus aureus"], "Group B strep is CAMP positive and causes neonatal sepsis/meningitis."),
        q("Scarlet fever rash occurs due to:", "Streptococcal pyrogenic exotoxin", ["M protein alone", "Hyaluronidase only", "C5a peptidase only"], "Erythrogenic toxins are superantigens responsible for scarlet fever rash."),
        q("Necrotizing fasciitis due to S. pyogenes is dangerous because:", "Rapid toxin-mediated tissue destruction and systemic toxicity occur", ["It never invades fascia", "It is always painless", "It needs no surgery"], "GAS necrotizing fasciitis requires urgent surgery and antibiotics."),
        q("Post-streptococcal glomerulonephritis follows skin or throat infection due to:", "Immune complex deposition", ["Direct kidney invasion", "IgE degranulation", "Toxin blocking ACh"], "PSGN is immune-mediated and can follow nephritogenic GAS strains."),
        q("Penicillin remains drug of choice for susceptible S. pyogenes because:", "Resistance to penicillin has not become a clinical problem", ["It blocks toxins only", "It is antiviral", "It prevents all immune sequelae after late treatment"], "GAS remains penicillin susceptible; early treatment prevents rheumatic fever."),
        q("Erysipelas is classically:", "Raised sharply demarcated superficial cellulitis", ["Deep bone infection", "Fungal nail infection", "Painless viral papule"], "Erysipelas involves upper dermis/lymphatics and often has a raised border."),
        q("M protein helps S. pyogenes evade immunity by:", "Inhibiting phagocytosis", ["Producing spores", "Binding ergosterol", "Cleaving IgA only"], "M protein is antiphagocytic and a major virulence factor."),
    ]),
    ("gas-gangrene-anaerobes", "Gas Gangrene (Clostridium perfringens) and Infections due to Non-sporing Anaerobes", [
        q("A trauma wound has severe pain, crepitus, foul discharge, and muscle necrosis. The likely agent is:", "Clostridium perfringens", ["Mycobacterium leprae", "Candida albicans", "Parvovirus B19"], "C. perfringens causes clostridial myonecrosis/gas gangrene."),
        q("The major toxin in gas gangrene is:", "Alpha toxin lecithinase", ["Tetanospasmin", "Botulinum toxin", "Shiga toxin"], "C. perfringens alpha toxin is a phospholipase causing myonecrosis and hemolysis."),
        q("Nagler reaction is used to demonstrate:", "Lecithinase activity of Clostridium perfringens", ["Urease of H. pylori", "Coagulase of S. aureus", "Oxidase of Vibrio"], "Nagler reaction shows opalescence on egg yolk agar inhibited by antitoxin."),
        q("Gas in soft tissue infection is produced because clostridia:", "Ferment tissue carbohydrates under anaerobic conditions", ["Release oxygen", "Form viral particles", "Calcify muscle"], "Anaerobic fermentation produces gas in necrotic tissue."),
        q("Management of gas gangrene requires:", "Urgent surgical debridement plus high-dose antibiotics", ["Topical cream only", "Waiting for serology", "No oxygen exposure"], "Surgery and antibiotics are essential; delay is fatal."),
        q("Non-sporing anaerobic infections are often polymicrobial because they arise from:", "Endogenous mucosal flora", ["Mosquito vectors", "Freshwater snails", "Airborne spores only"], "Anaerobes like Bacteroides originate from oral, gut, or genital mucosa."),
        q("Bacteroides fragilis virulence is aided by:", "Polysaccharide capsule and beta-lactamase production", ["Acid-fast cell wall", "Exotoxin A", "Motile swarming"], "B. fragilis is encapsulated and often beta-lactamase producing."),
        q("A foul-smelling abscess after bowel perforation suggests:", "Anaerobic infection", ["Pure viral infection", "Dermatophyte infection", "Malaria"], "Anaerobic metabolism produces foul-smelling volatile fatty acids."),
        q("Actinomycosis differs from typical anaerobic abscess by forming:", "Draining sinuses with sulfur granules", ["Rice-water stool", "Rose spots", "Vesicular rash"], "Actinomyces causes chronic suppurative lesions with sulfur granules."),
        q("Metronidazole is useful for many anaerobic infections because:", "Anaerobes reduce it to DNA-damaging radicals", ["It blocks beta-lactamase", "It inhibits fungal ergosterol", "It neutralizes alpha toxin"], "Metronidazole is activated in anaerobic conditions."),
    ]),
    ("leprosy", "Leprosy (Mycobacterium leprae)", [
        q("A patient has hypopigmented anesthetic skin patches and thickened peripheral nerves. The diagnosis is:", "Leprosy", ["Vitiligo only", "Tinea versicolor", "Scabies"], "Loss of sensation in skin lesions with nerve thickening is classic for Hansen disease."),
        q("Mycobacterium leprae primarily infects:", "Peripheral nerves and skin macrophages/Schwann cells", ["Red cells", "Intestinal villi", "Hepatocytes only"], "M. leprae has tropism for cooler skin and peripheral nerves."),
        q("Tuberculoid leprosy shows:", "Strong cell-mediated immunity with few bacilli", ["Absent T-cell response with many bacilli", "Only humoral immunity", "No granulomas"], "Tuberculoid disease is paucibacillary with robust Th1 response."),
        q("Lepromatous leprosy shows:", "Poor cell-mediated immunity and numerous bacilli", ["Strong granulomas with no bacilli", "Acute toxin disease", "Only joint infection"], "Lepromatous leprosy is multibacillary due to weak CMI."),
        q("Lepromin test is usually positive in:", "Tuberculoid leprosy", ["Lepromatous leprosy", "All viral exanthems", "Gas gangrene"], "Lepromin reflects cell-mediated immunity rather than active infection diagnosis."),
        q("M. leprae cannot be grown on artificial media; classic animal model is:", "Mouse footpad", ["Guinea pig peritoneum only", "Embryonated egg only", "Blood agar"], "M. leprae is uncultivable in routine media and grows in mouse footpad/armadillo models."),
        q("Type 1 lepra reaction is:", "Reversal reaction due to increased cellular immunity", ["Immune complex erythema nodosum leprosum", "Botulinum toxicity", "Serum sickness after antitoxin"], "Type 1 reactions involve delayed-type hypersensitivity and nerve inflammation."),
        q("Type 2 lepra reaction is also called:", "Erythema nodosum leprosum", ["Lucio phenomenon only", "Arthus reaction", "Koplik reaction"], "ENL is immune complex-mediated and occurs in multibacillary leprosy."),
        q("Multidrug therapy for leprosy is used to:", "Prevent resistance and treat persisting bacilli", ["Avoid all immune reactions", "Cure with one dose", "Replace diagnosis"], "Combination therapy with rifampicin, dapsone, and clofazimine is standard for multibacillary disease."),
        q("Disability prevention in leprosy depends heavily on:", "Early nerve involvement detection and reaction management", ["Ignoring numb patches", "Avoiding footwear", "Steroid avoidance in all reactions"], "Nerve damage causes deformity; early treatment and protection prevent disability."),
    ]),
    ("misc-bacterial-skin", "Miscellaneous Bacterial Infections of Skin and Soft Tissues: Anthrax, Actinomycosis, Nocardiosis, Nonvenereal Treponematoses and Others", [
        q("A painless black eschar with massive edema after handling animal hide suggests:", "Cutaneous anthrax", ["Impetigo", "Leprosy", "Molluscum"], "Bacillus anthracis causes painless ulcer with black eschar and edema."),
        q("Bacillus anthracis virulence depends on capsule made of:", "Poly-D-glutamate", ["Hyaluronic acid", "Polysialic acid", "Alginate"], "Anthrax capsule is polypeptide poly-D-glutamate and antiphagocytic."),
        q("Anthrax toxin edema factor functions as:", "Adenylate cyclase increasing cAMP", ["SNARE protease", "Superantigen", "DNA gyrase inhibitor"], "Edema factor raises cAMP; lethal factor is a protease."),
        q("Actinomycosis after dental procedure causes jaw swelling with draining sinuses and:", "Sulfur granules", ["Rice-water stool", "Negri bodies", "Maltese cross"], "Actinomyces israelii causes chronic cervicofacial disease with sulfur granules."),
        q("Actinomyces is best described as:", "Anaerobic branching Gram-positive filamentous bacterium", ["Acid-fast aerobic branching bacterium", "Encapsulated yeast", "Spirochete"], "Actinomyces are anaerobic, non-acid-fast branching Gram-positive rods."),
        q("Nocardia differs from Actinomyces because Nocardia is:", "Weakly acid-fast aerobic branching filamentous bacterium", ["Strict anaerobe non-acid-fast", "Gram-negative coccus", "Helminth"], "Nocardia is aerobic and partially acid-fast due to mycolic acids."),
        q("Nocardiosis is especially seen in:", "Cell-mediated immunodeficiency", ["Healthy neonates only", "All vaccinated persons", "Only iron deficiency"], "Nocardia causes pulmonary, CNS, and cutaneous disease in immunocompromised hosts."),
        q("Yaws is a nonvenereal treponematosis caused by:", "Treponema pallidum pertenue", ["Borrelia recurrentis", "Leptospira interrogans", "Rickettsia prowazekii"], "Yaws is a nonsexual treponemal infection affecting skin and bone."),
        q("Pinta primarily affects:", "Skin", ["Heart valves", "Liver only", "RBCs"], "Pinta is a nonvenereal treponemal disease causing skin lesions."),
        q("Erysipeloid in fish/meat handlers is caused by:", "Erysipelothrix rhusiopathiae", ["Erysipelothrix diphtheriae", "S. pyogenes only", "Vibrio cholerae"], "Erysipelothrix causes localized violaceous skin infection after animal/fish exposure."),
    ]),
    ("cutaneous-viral-infections", "Viral Exanthems and Other Cutaneous Viral Infections", [
        q("Grouped painful vesicles on an erythematous base at the lip are most consistent with:", "Herpes simplex virus", ["Molluscum contagiosum", "Parvovirus B19", "Measles"], "HSV causes recurrent grouped vesicles at mucocutaneous sites."),
        q("Dermatomal painful vesicular rash in an elderly patient suggests:", "Herpes zoster", ["Rubella", "Molluscum", "Hand-foot-mouth disease"], "Varicella-zoster reactivation causes shingles in a dermatomal distribution."),
        q("Tzanck smear from herpetic lesion shows:", "Multinucleated giant cells", ["Acid-fast bacilli", "Maltese cross", "Sulfur granules"], "HSV/VZV can show multinucleated giant cells on Tzanck smear."),
        q("Measles rash is preceded by:", "Koplik spots", ["Forchheimer spots only", "Eschar", "Black eschar"], "Koplik spots on buccal mucosa precede measles exanthem."),
        q("Rubella in early pregnancy is feared because it can cause:", "Congenital rubella syndrome", ["Neonatal tetanus", "Hydatid cyst", "Gas gangrene"], "Rubella can cause cataract, deafness, cardiac defects, and other fetal injury."),
        q("Slapped cheek rash in a child is classically due to:", "Parvovirus B19", ["HHV-6", "HSV-2", "Variola"], "Parvovirus B19 causes erythema infectiosum."),
        q("Roseola infantum presents with high fever followed by rash after defervescence due to:", "HHV-6 or HHV-7", ["HSV-1", "Measles virus", "Smallpox"], "Roseola is caused mainly by HHV-6."),
        q("Molluscum contagiosum lesions are:", "Umbilicated pearly papules", ["Dermatomal vesicles", "Honey crusts", "Black eschars"], "Molluscum poxvirus causes dome-shaped umbilicated papules."),
        q("Hand-foot-mouth disease is most often caused by:", "Coxsackievirus A", ["Variola major", "HHV-8", "Parvovirus B19 only"], "Enteroviruses, especially Coxsackie A, cause oral ulcers and hand/foot lesions."),
        q("Smallpox differs from chickenpox because smallpox lesions are classically:", "Synchronous and more centrifugal", ["Always at different stages", "Only on trunk", "Noninfectious"], "Smallpox lesions tend to be at the same stage and involve face/extremities prominently."),
    ]),
    ("parasitic-skin-msk", "Parasitic Infections of Skin, Soft Tissue and Musculoskeletal System", [
        q("A chronic painless ulcer with raised indurated margin after sandfly bite suggests:", "Cutaneous leishmaniasis", ["Scabies", "Tinea corporis", "Impetigo"], "Cutaneous leishmaniasis causes chronic skin ulcers at bite sites."),
        q("Cutaneous leishmaniasis is transmitted by:", "Sandfly", ["Aedes mosquito", "Tsetse fly", "Body louse"], "Phlebotomine sandflies transmit Leishmania."),
        q("Subcutaneous nodules and seizures from larval Taenia solium indicate:", "Cysticercosis", ["Hydatid disease only", "Filariasis", "Amoebiasis"], "Cysticerci can lodge in subcutaneous tissue, muscle, eye, and brain."),
        q("Guinea worm disease is caused by:", "Dracunculus medinensis", ["Wuchereria bancrofti", "Trichinella spiralis", "Loa loa"], "Dracunculus emerges through skin after ingestion of infected Cyclops in water."),
        q("Dracunculus transmission is prevented mainly by:", "Safe drinking water filtration and preventing infected persons entering water sources", ["Mosquito nets only", "Dog vaccination only", "BCG"], "Water safety interrupts Cyclops-borne transmission."),
        q("Myalgia, periorbital edema, and eosinophilia after undercooked pork suggest:", "Trichinellosis", ["Leprosy", "Scabies", "Onchocerciasis"], "Trichinella larvae encyst in muscle after ingestion of infected meat."),
        q("Creeping eruption on foot after walking barefoot on contaminated sand suggests:", "Cutaneous larva migrans", ["Tinea versicolor", "Molluscum", "Yaws"], "Dog/cat hookworm larvae migrate in skin causing serpiginous tracks."),
        q("Loa loa is known for:", "Calabar swellings and eyeworm", ["Hydatid cyst", "Black eschar", "Rose spots"], "Loa loa causes transient angioedema and subconjunctival migration."),
        q("Onchocerciasis skin disease with nodules and eye involvement is transmitted by:", "Blackfly", ["Sandfly", "Mosquito", "Flea"], "Simulium blackflies transmit Onchocerca volvulus."),
        q("Eosinophilia in parasitic skin/muscle disease most strongly suggests:", "Tissue-invasive helminth infection", ["Superficial viral exanthem", "Pure bacterial impetigo", "Dermatophyte colonization only"], "Helminth tissue migration commonly drives eosinophilia."),
    ]),
    ("fungal-skin-msk", "Fungal Infections of Skin, Soft Tissue and Musculoskeletal System", [
        q("A ring-shaped scaly itchy lesion with central clearing is:", "Tinea corporis", ["Herpes zoster", "Impetigo", "Molluscum"], "Dermatophyte infection of body skin produces annular scaly plaques."),
        q("Dermatophytes infect skin, hair, and nails because they:", "Utilize keratin", ["Invade RBCs", "Require anaerobic colon", "Grow only in blood"], "Dermatophytes are keratinophilic fungi."),
        q("KOH mount in dermatophytosis shows:", "Septate branching hyphae", ["Acid-fast bacilli", "Trophozoites with RBCs", "Multinucleated giant cells"], "KOH clears keratin and reveals fungal hyphae."),
        q("Wood lamp coral-red fluorescence in erythrasma is due to:", "Corynebacterium minutissimum", ["Microsporum only", "Candida", "Sporothrix"], "Erythrasma is bacterial but mimics fungal intertrigo; it fluoresces coral-red."),
        q("Pityriasis versicolor is caused by:", "Malassezia species", ["Trichophyton rubrum", "Sporothrix schenckii", "Candida auris"], "Malassezia causes hypo/hyperpigmented scaly macules."),
        q("Spaghetti and meatballs appearance on KOH suggests:", "Malassezia furfur", ["Candida albicans", "Aspergillus", "Mucor"], "Short hyphae and yeasts create the classic appearance."),
        q("Sporotrichosis after rose thorn injury spreads along lymphatics and is caused by:", "Sporothrix schenckii", ["Candida albicans", "Malassezia", "Trichophyton"], "Sporothrix causes nodular lymphangitis after traumatic inoculation."),
        q("Chromoblastomycosis shows which tissue form?", "Sclerotic Medlar bodies", ["Germ tubes", "Maltese cross", "LD bodies"], "Copper penny/sclerotic bodies are diagnostic of chromoblastomycosis."),
        q("Madura foot with draining sinuses and grains can be due to:", "Eumycetoma or actinomycetoma", ["Only HSV", "Only parvovirus", "Only measles"], "Mycetoma may be fungal or actinomycotic; grains help identify etiology."),
        q("Oral thrush in an immunocompromised patient is commonly due to:", "Candida albicans", ["Malassezia", "Microsporum", "Sporothrix"], "Candida causes mucocutaneous candidiasis with pseudohyphae and budding yeast."),
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
            questions.append({**BASE, "id": f"micro-skin-msk-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "microbiology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 9 or len(questions) != 90:
        raise AssertionError(f"Expected 9 topics and 90 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 90:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
