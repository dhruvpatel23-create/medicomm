from .common import q

CHAPTERS = [
    # Topic 3: Bacterial Infections (Important - 10 questions)
    (3, "Bacterial Infections", "hard", [
        q(
            "An 8-year-old boy presents with multiple discrete facial lesions around the mouth and nares that initially began as thin-walled vesicles, rapidly rupturing to leave behind thick, golden-yellow, adherent 'honey-colored' crusts. Regional submandibular lymph nodes are enlarged. What is the diagnosis and the most common causative organism?",
            "Non-bullous impetigo; Staphylococcus aureus",
            ["Bullous impetigo; Pseudomonas aeruginosa", "Ecthyma; Corynebacterium diphtheriae", "Herpes labialis; Cytomegalovirus"],
            "Non-bullous impetigo (impetigo contagiosa) is the most common superficial bacterial skin infection in children. It is primarily caused by Staphylococcus aureus (alone or co-infecting with Group A Streptococcus pyogenes). It begins as thin-walled intraepidermal vesicles/pustules that rupture easily, releasing seropurulent exudate that dries to form pathognomonic golden-yellow 'honey-colored' crusts over an erythematous base.",
            clinical=True
        ),
        q(
            "A 3-year-old child presents with large, flaccid, transparent blisters on the trunk and intertriginous folds that contain clear-to-turbid fluid without surrounding erythema. The blister roof easily ruptures leaving a glistening, red, moist erosion with a thin collarette of scale. What bacterial virulence factor is responsible for this bullous presentation?",
            "Staphylococcal exfoliative toxin A cleaving desmoglein 1",
            ["Streptococcal pyrogenic exotoxin A", "Pseudomonas exotoxin A inhibiting protein synthesis", "Panton-Valentine leukocidin destroying neutrophils"],
            "Bullous impetigo is caused exclusively by phage group II (types 71 and 55) Staphylococcus aureus. These strains produce Exfoliative Toxins A and B (ETA and ETB), which are serine proteases that specifically bind to and cleave Desmoglein 1 (Dsg1) in the stratum granulosum, producing localized subcorneal blister cleavage and flaccid bullae.",
            clinical=True
        ),
        q(
            "A 14-month-old infant develops high fever, marked irritability, diffuse tender erythema beginning around the mouth and eyes, followed by widespread flaccid blistering and epidermal sheet-like desquamation on light shearing force. The oral mucosa, tongue, and conjunctivae are completely normal and unaffected. What is the diagnosis?",
            "Staphylococcal scalded skin syndrome",
            ["Toxic epidermal necrolysis", "Stevens-Johnson syndrome", "Kawasaki disease"],
            "Staphylococcal Scalded Skin Syndrome (SSSS / Ritter disease) is caused by systemic hematogenous dissemination of exfoliative toxins A and B from a localized distant staphylococcal focus (e.g., nasopharynx, umbilicus). Hallmarks: tender erythroderma, periorificial radial fissuring/crusting, positive Nikolsky sign, and intraepidermal subcorneal split. Critically, mucous membranes are completely SPARED because mucosal epithelial cohesion is maintained by desmoglein 3, which is unaffected by exfoliative toxin.",
            clinical=True
        ),
        q(
            "Which clinical feature definitively differentiates facial Erysipelas from facial Cellulitis?",
            "Sharply demarcated, raised, elevated margin involving the superficial dermis",
            ["Indistinct diffuse border involving the deep subcutis", "Painless anesthesia over the erythematous zone", "Spontaneous ulceration with central black eschar"],
            "Erysipelas is a superficial dermal infection with prominent lymphatic involvement, almost invariably caused by Streptococcus pyogenes. Its diagnostic hallmark is a bright red, edematous, brawny plaque with a sharply demarcated, distinctly elevated, palpable advancing border. In contrast, cellulitis extends deeper into the deep dermis and subcutaneous fat, presenting with an ill-defined, diffuse, non-elevated border.",
            clinical=False
        ),
        q(
            "A 12-year-old malnourished child living in poor hygienic conditions presents with several painful, ulcerative lesions on the lower legs. Each lesion consists of a deep, 'punched-out' circular ulcer with violaceous indurated borders covered by a thick, adherent, hard, dark brown crust. What is the diagnosis?",
            "Ecthyma",
            ["Impetigo contagiosa", "Erythema induratum", "Pyoderma gangrenosum"],
            "Ecthyma is an ulcerative pyoderma that represents a deep, tissue-destructive form of impetigo caused by Streptococcus pyogenes (often superinfected with S. aureus). Unlike impetigo which is intraepidermal, ecthyma penetrates through the full epidermis into the deep dermis, producing a punched-out ulcer covered by a thick, hard, firmly adherent crust that heals with permanent scarring.",
            clinical=True
        ),
        q(
            "A 42-year-old obese male presents with sharply defined, asymptomatic, reddish-brown macular patches in both axillae and groins that have a fine wrinkled surface. Examination of the intertriginous patches under Wood's light demonstrates intense, brilliant coral-red fluorescence. What is the diagnosis and etiology?",
            "Erythrasma; Corynebacterium minutissimum",
            ["Tinea cruris; Trichophyton rubrum", "Intertrigo; Candida albicans", "Pityriasis versicolor; Malassezia furfur"],
            "Erythrasma is a superficial bacterial infection of intertriginous skin caused by Corynebacterium minutissimum (a Gram-positive rod). Under Wood's lamp (365 nm UVA), the lesions emit a brilliant, pathognomonic coral-red fluorescence due to excessive porphyrin synthesis (predominantly coproporphyrin III) by the proliferating bacteria.",
            clinical=True
        ),
        q(
            "A 26-year-old soldier who wears occlusive combat boots presents with offensive, malodorous feet and a burning sensation while walking. Examination of the weight-bearing plantar surfaces of both feet reveals multiple shallow, punched-out, crater-like pits (1 to 3 mm in diameter) coalescing into erosive sulci on a macerated white background. What is the diagnosis?",
            "Pitted keratolysis",
            ["Tinea pedis", "Plantar warts", "Juvenile plantar dermatosis"],
            "Pitted keratolysis is a superficial bacterial infection of the stratum corneum of the soles, caused by Kytococcus sedentarius, Corynebacterium species, and Dermatophilus congolensis. These bacteria produce serine proteases that digest the stratum corneum keratin, creating characteristic crateriform pits. Production of volatile sulfur-containing organic compounds (thiol esters) accounts for the pungent, foul foot odor.",
            clinical=True
        ),
        q(
            "A 50-year-old diabetic male presents with rapidly progressive, severe pain in his perineum and scrotum that is disproportionate to mild initial erythema. Within 24 hours, the scrotum becomes dusky violaceous with bullae, cutaneous crepitus, and foul-smelling 'dishwater' fluid discharge. What life-threatening surgical emergency is this?",
            "Fournier gangrene (necrotizing fasciitis)",
            ["Cellulitis of the scrotum", "Erysipelas of the perineum", "Lymphangitis"],
            "Fournier gangrene is a fulminant polymicrobial necrotizing fasciitis of the perineal, perianal, and genital regions. Disproportionate excruciating pain, systemic toxicity, subcutaneous crepitus (gas-forming anaerobes), and grayish 'dishwater pus' indicate extensive fascial necrosis. Immediate broad-spectrum intravenous antibiotics and urgent aggressive surgical debridement are lifesaving.",
            clinical=True
        ),
        q(
            "A goat farmer presents with an initially painless, pruritic red papule on his right forearm that rapidly evolved into a vesicle surrounded by non-pitting gelatinous edema. Within 4 days, the vesicle ruptured to form a diagnostic, painless, depressed coal-black necrotic eschar surrounded by a ring of small satellite vesicles. What is the organism?",
            "Bacillus anthracis",
            ["Francisella tularensis", "Erysipelothrix rhusiopathiae", "Pasteurella multocida"],
            "Cutaneous anthrax (malignant pustule) accounts for >95% of natural human anthrax cases, acquired through direct skin contact with infected animal carcasses or wool/hides. Hallmarks: painless pruritic papule developing into a ring of hemorrhagic vesicles, culminating in a depressed, coal-black, leathery necrotic eschar surrounded by extensive brawny non-pitting edema.",
            clinical=True
        ),
        q(
            "A 38-year-old fish handler develops a sharply circumscribed, violaceous-red, non-suppurative, tender plaque with a smooth center and an elevated purplish advancing border on the dorsum of his hand 3 days after puncturing his finger on a fish spine. Regional lymph nodes are not enlarged. What is the diagnosis?",
            "Erysipeloid of Rosenbach",
            ["Erysipelas", "Cutaneous leishmaniasis", "Lupus vulgaris"],
            "Erysipeloid is an acute cutaneous occupational zoonosis caused by Erysipelothrix rhusiopathiae (Gram-positive bacillus), contracted via skin abrasions during handling of meat, poultry, fish, or crustaceans. It produces a well-demarcated, violaceous or purplish cellulitic plaque without suppuration or pitting edema, typically centered on the fingers or hands.",
            clinical=True
        ),
    ]),

    # Topic 4: Viral Infections (Important - 10 questions)
    (4, "Viral Infections", "hard", [
        q(
            "A 26-year-old female presents with recurrent, painful, grouped vesicles on an erythematous base on her right vermilion border. A Tzanck smear prepared from the scraping of a freshly unroofed vesicle base and stained with Giemsa demonstrates multinucleated epidermal giant cells and intra-nuclear eosinophilic inclusions. What are these diagnostic inclusions termed?",
            "Cowdry A inclusion bodies",
            ["Henderson-Paterson bodies", "Guarnieri bodies", "Negri bodies"],
            "A positive Tzanck smear for Herpes Simplex Virus (HSV) or Varicella-Zoster Virus (VZV) shows characteristic multinucleated acantholytic giant cells (formed by syncytial fusion of infected keratinocytes), nuclear molding, ballooning degeneration, and Cowdry A inclusion bodies (eosinophilic intranuclear inclusion bodies). Henderson-Paterson bodies are seen in Molluscum; Guarnieri bodies in Poxvirus; Negri bodies in Rabies.",
            clinical=True
        ),
        q(
            "A 68-year-old male presents with severe lancinating pain across his forehead and scalp, accompanied by a unilateral vesicular eruption extending along the ophthalmic division of the trigeminal nerve (V1). The examining physician notes vesicles clustered on the tip and side of the patient's nose. What is this clinical sign, and what complication does it herald?",
            "Hutchinson sign (predicts herpes zoster ophthalmicus)",
            ["Crowe sign (predicts optic glioma)", "Nikolsky sign (predicts toxic necrolysis)", "Auspitz sign (predicts ocular psoriasis)"],
            "Hutchinson's sign in Herpes Zoster refers to the appearance of herpetic vesicles on the tip, side, or root of the nose. This indicates involvement of the external nasal branch of the nasociliary nerve (a branch of the ophthalmic division V1). Because the nasociliary nerve also innervates the cornea and uvea, a positive Hutchinson sign predicts a 75% risk of severe ocular complications (keratitis, corneal ulceration, anterior uveitis, permanent visual loss).",
            clinical=True
        ),
        q(
            "A 4-year-old child presents with multiple painless, discrete, dome-shaped, pearly-white papules on the lower abdomen and thighs. Many lesions exhibit a central, tiny dell or punctum ('umbilication') from which a cheesy curd-like material can be expressed. What histological structure is pathognomonic on skin biopsy?",
            "Henderson-Paterson molluscum bodies",
            ["Civatte colloid bodies", "Kamino bodies", "Michaelis-Gutmann bodies"],
            "Molluscum Contagiosum is caused by a double-stranded DNA Molluscipoxvirus. Histopathology reveals downward proliferating lobules of hyperplastic epidermis with pathognomonic Henderson-Paterson bodies (large, intracytoplasmic, eosinophilic-to-basophilic inclusion bodies) that displace the keratinocyte nucleus to the periphery and contain millions of viral virions.",
            clinical=True
        ),
        q(
            "Which Human Papillomavirus (HPV) genotypes are etiologically linked to Condylomata Acuminata (anogenital warts) in contrast to the high-risk oncogenic types causing Bowenoid papulosis and cervical intraepithelial neoplasia?",
            "HPV 6 and 11 (benign); HPV 16 and 18 (oncogenic)",
            ["HPV 1 and 2 (benign); HPV 3 and 10 (oncogenic)", "HPV 5 and 8 (benign); HPV 6 and 11 (oncogenic)", "HPV 7 and 13 (benign); HPV 31 and 33 (oncogenic)"],
            "Condylomata acuminata (benign anogenital cauliflower-like warts) are caused by 'low-risk' non-oncogenic HPV types 6 and 11 in >90% of cases. Conversely, 'high-risk' oncogenic types HPV 16, 18, 31, and 33 are causative in high-grade squamous intraepithelial lesions, bowenoid papulosis, cervical carcinoma, and anal carcinoma.",
            clinical=False
        ),
        q(
            "A 32-year-old HIV-infected male with a CD4 count of 80 cells/mcL presents with multiple purple-to-violaceous, non-tender macules, plaques, and nodules on the lower extremities and oral mucosa. Biopsy demonstrates intersecting fascicles of spindle cells, vascular slit-like channels containing extravasated erythrocytes, and intracellular hemosiderin. Which infectious agent drives this neoplasm?",
            "Human herpesvirus 8 (HHV-8)",
            ["Epstein-Barr virus (EBV)", "Human T-cell lymphotropic virus-1 (HTLV-1)", "Cytomegalovirus (CMV)"],
            "Kaposi Sarcoma is an endothelial neoplasm driven by Human Herpesvirus 8 (HHV-8 / KSHV). In epidemic (AIDS-associated) KS, lesions manifest as violaceous, rust-colored or purplish macules, plaques, and nodules commonly involving the palate, gingiva, face, lower limbs, and gastrointestinal tract. Histopathology shows spindle cell proliferation forming slit-like vascular spaces with extravasated RBCs.",
            clinical=True
        ),
        q(
            "A 2-year-old child presents with low-grade fever, sore mouth, and refusal to eat. Examination reveals small, painful aphthoid ulcers on the buccal mucosa and tongue, along with non-pruritic, oval, grayish-white vesicles surrounded by an erythematous halo oriented parallel to skin creases on the palms and soles. What is the most common viral etiology?",
            "Coxsackievirus A16",
            ["Herpes simplex virus type 1", "Parvovirus B19", "Human herpesvirus 6"],
            "Hand, Foot, and Mouth Disease (HFMD) is an acute viral exanthem caused primarily by enteroviruses of the family Picornaviridae, most frequently Coxsackievirus A16 and Enterovirus 71 (the latter can cause severe neurological complications). Hallmark: painful oral vesicles/erosions combined with elliptical, football-shaped gray vesicles on an erythematous base on the palms, soles, and buttocks.",
            clinical=True
        ),
        q(
            "A 22-year-old college student presents with a single, salmon-colored, 4-cm oval plaque with a peripheral collarette of thin cigarette-paper scales on her chest. Two weeks later, a secondary eruption of smaller, identical oval macules and papules erupts across her trunk and back, oriented along skin cleavage lines ('Christmas tree pattern'). What is the diagnosis?",
            "Pityriasis rosea",
            ["Secondary syphilis", "Guttate psoriasis", "Tinea corporis"],
            "Pityriasis rosea is a self-limiting exanthem associated with reactivation of HHV-6 and HHV-7. It classically initiates with a solitary primary 'herald patch' (2-5 cm oval plaque with a peripheral collarette of inward-facing scale), followed 1-2 weeks later by an eruption of smaller oval lesions aligned along the Langer cleavage lines, producing the characteristic 'fir-tree' or 'Christmas tree' pattern on the back.",
            clinical=True
        ),
        q(
            "A 6-year-old girl develops bright, confluent erythema with marked sparing of the circumoral area on both cheeks, giving a dramatic 'slapped-cheek' appearance. Three days later, a reticular, erythematous, lacy eruption appears on her arms and thighs, which waxes and wanes with heat and sunlight. What is the causative virus?",
            "Parvovirus B19",
            ["Rubella virus", "Measles virus (Morbillivirus)", "Roseolovirus (HHV-6)"],
            "Erythema infectiosum (Fifth disease) is caused by Parvovirus B19 (a single-stranded DNA virus that targets erythroid progenitor cells). Clinical stages: 1. Intense erythematous facial erythema with circumoral pallor ('slapped cheek' appearance); 2. Reticular, lace-like, maculopapular eruption on trunk and extremities; 3. Evanescent waxing and waning over several weeks triggered by exercise, sun exposure, or temperature changes.",
            clinical=True
        ),
        q(
            "A 3-year-old boy presents with a sudden, symmetric eruption of non-pruritic, flat-topped, copper-red, lichenoid papules localized exclusively to his cheeks, buttocks, and the extensor surfaces of his forearms and legs, with total sparing of the trunk. What is this syndrome, and with which viral infection was it classically first described?",
            "Gianotti-Crosti syndrome (papular acrodermatitis of childhood); Hepatitis B virus",
            ["Kawasaki disease; Adenovirus", "Sweet syndrome; Hepatitis C virus", "Erythema multiforme; HSV"],
            "Gianotti-Crosti syndrome (papular acrodermatitis of childhood) is a reactive exanthem occurring in young children (aged 1-6 years). It is characterized by dense, monomorphic, flat-topped, lichenoid, non-coalescing papules symmetrically distributed over the face, buttocks, and extensor extremities while strictly sparing the trunk. Classically described with Hepatitis B virus, it is now more commonly triggered by Epstein-Barr Virus (EBV).",
            clinical=True
        ),
        q(
            "A 3-year-old toddler with severe active atopic dermatitis suddenly develops high spiking fever, irritability, and a widespread eruption of painful, umbilicated, punched-out vesicles and crusts rapidly erupting over preexisting eczematous skin on the face, neck, and chest. What is this dermatological emergency, and what immediate therapy is required?",
            "Eczema herpeticum (Kaposi varicelliform eruption); immediate intravenous acyclovir",
            ["Staphylococcal scalded skin syndrome; intravenous flucloxacillin", "Severe varicella; oral antihistamines", "Generalized bullous impetigo; topical mupirocin"],
            "Eczema herpeticum (Kaposi varicelliform eruption) is a potentially life-threatening disseminated viral infection (almost always HSV-1, occasionally coxsackievirus) superimposed on preexisting defective skin barrier disease (most commonly atopic dermatitis). Characteristic dome-shaped, grouped, punched-out umbilicated vesicles rapidly progress to hemorrhagic crusts. Immediate prompt systemic antiviral therapy (IV or high-dose oral acyclovir) is imperative to prevent fatal viremia.",
            clinical=True
        ),
    ]),

    # Topic 5: Fungal Infections (Important - 10 questions)
    (5, "Fungal Infections", "hard", [
        q(
            "A 7-year-old boy presents with a severely inflamed, tender, boggy, fluctuating, purulent mass studded with pustules and loose, easily epilated hairs on his scalp. Regional posterior cervical and suboccipital lymphadenopathy is present. What is this inflammatory presentation of tinea capitis, and what is its standard systemic therapy?",
            "Kerion celsi; systemic oral griseofulvin or terbinafine",
            ["Favus; topical ketoconazole shampoo alone", "Trichotillomania; behavioral therapy", "Dissecting cellulitis of scalp; oral isotretinoin"],
            "A Kerion is a severe, cell-mediated hypersensitivity reaction to zoophilic dermatophytes (most commonly Trichophyton verrucosum or Trichophyton mentagrophytes), manifesting as a boggy, elevated, suppurative inflammatory tumefaction studded with follicular pustules. Topical antifungals are ineffective; standard treatment requires oral antifungal therapy (Griseofulvin is the gold standard for tinea capitis in children, or Terbinafine) often combined with a short course of oral corticosteroids to prevent permanent cicatricial alopecia.",
            clinical=True
        ),
        q(
            "Which dermatophyte is the primary causative agent of Endothrix Tinea Capitis ('black dot' ringworm), where fungal arthroconidia are packed entirely WITHIN the hair shaft without destroying the cuticle?",
            "Trichophyton tonsurans",
            ["Microsporum canis", "Microsporum audouinii", "Epidermophyton floccosum"],
            "In Endothrix tinea capitis (caused predominantly by anthropophilic Trichophyton tonsurans and T. violaceum), arthroconidia proliferate entirely within the interior of the hair shaft. Because the cuticle remains intact, hairs become brittle and snap off flush at the level of the follicular orifice, appearing as tiny black dots ('black dot tinea capitis'). Endothrix infections do NOT fluoresce under Wood's light. In contrast, Ectothrix infections (M. canis) show external cuticle destruction and bright green Wood's fluorescence.",
            clinical=False
        ),
        q(
            "A 24-year-old male presents with mildly pruritic, finely scaly, hypopigmented macules over his upper chest and back that fail to tan after sun exposure. Scratching a lesion with a fingernail easily accentuates the fine, furfuraceous scale (Besnier's scratch sign). Microscopic examination of the scale in 10% potassium hydroxide (KOH) reveals short, stubby curved hyphae interspersed with clusters of spherical yeast cells ('spaghetti and meatballs' appearance). What is the diagnosis?",
            "Pityriasis versicolor",
            ["Vitiligo", "Leprosy (tuberculoid)", "Pityriasis alba"],
            "Pityriasis (Tinea) versicolor is a chronic, superficial fungal infection caused by dimorphic lipophilic Malassezia yeasts (M. globosa, M. furfur). Pathognomonic microscopic finding on 10% KOH mount is the 'spaghetti and meatballs' pattern (short septate hyphae and round yeast cells). Hypopigmentation results from dicarboxylic acids (such as azelaic acid) synthesized by the fungus that competitively inhibit tyrosinase in melanocytes.",
            clinical=True
        ),
        q(
            "A 35-year-old female presents with an extensive, poorly demarcated, erythematous, non-scaly plaque with scattered pustules on her face. History reveals she mistakenly applied a high-potency fluorinated topical corticosteroid cream for 2 months to a pre-existing ringworm infection. What is this modified presentation termed?",
            "Tinea incognito",
            ["Tinea faciei", "Rosacea", "Discoid lupus erythematosus"],
            "Tinea incognito is a dermatophyte infection whose classic morphology (annular shape, raised scaly advancing border, central clearing) has been completely masked and altered by the inappropriate application of topical or systemic corticosteroids or calcineurin inhibitors. Steroids suppress the local cell-mediated immune response, reducing scaling and inflammation while allowing unrestricted fungal proliferation, producing atypical, diffuse, pustular, or plaque-like lesions.",
            clinical=True
        ),
        q(
            "A rose gardener pricks his right index finger on a rose thorn. Three weeks later, a painless, ulcerating subcutaneous nodule develops at the puncture site, followed sequentially by a linear chain of painless, firm, subcutaneous nodules ascending along the lymphatic drainage of his forearm. Biopsy shows suppurative granulomas and rare 'asteroid bodies'. What is the diagnosis and drug of choice?",
            "Lymphocutaneous sporotrichosis; oral itraconazole",
            ["Cutaneous anthrax; oral ciprofloxacin", "Mycobacterium marinum infection; oral clarithromycin", "Nocardiosis; trimethoprim-sulfamethoxazole"],
            "Sporotrichosis is a subacute or chronic dimorphic fungal infection caused by Sporothrix schenckii (found in soil, sphagnum moss, and rose thorns). In the classic lymphocutaneous form, a primary chancriform nodule ulcerates, followed by secondary nodules developing in a linear chain along ascending lymphatic channels ('sporotrichoid spread'). Oral Itraconazole is the definitive first-line therapeutic agent.",
            clinical=True
        ),
        q(
            "A 48-year-old agricultural laborer presents with chronic, painless swelling of his left foot with numerous discharging sinuses exuding black granules. Radiographs reveal extensive osteolytic bone destruction. What type of mycetoma is this, and what is its most frequent fungal etiology?",
            "Eumycetoma; Madurella mycetomatis",
            ["Actinomycetoma; Actinomadura madurae", "Actinomycetoma; Streptomyces somaliensis", "Eumycetoma; Nocardia brasiliensis"],
            "Mycetoma (Madura foot) is a chronic granulomatous subcutaneous infection characterized by the diagnostic triad of: 1. Indurated subcutaneous tumefaction; 2. Multiple draining sinuses; 3. Macroscopic granule/grain discharge. Eumycetoma (caused by true fungi, most commonly Madurella mycetomatis) classically discharges black (melanin-containing) or pale grains, whereas Actinomycetoma (caused by filamentous aerobic bacteria) discharges white, yellow, or red grains.",
            clinical=True
        ),
        q(
            "A 52-year-old agricultural worker presents with a solitary, slowly progressive, verrucous, crusted, cauliflower-like plaque on his lower leg. Scraping the surface revealing tiny black dots ('cayenne pepper spots') and examining the crust in 10% KOH demonstrates thick-walled, chestnut-brown, round cells divided by internal cross-septation ('copper penny' or muriform Medlar bodies). What is the diagnosis?",
            "Chromoblastomycosis",
            ["Blastomycosis", "Lobomycosis", "Tuberculosis verrucosa cutis"],
            "Chromoblastomycosis (chromomycosis) is a chronic fungal infection of skin and subcutaneous tissue caused by dematiaceous (pigmented) fungi (Fonsecaea pedrosoi, Cladophialophora carrionii). Hallmark: verrucous, hyperkeratotic, warty plaques with black surface dots representing transepidermal elimination of fungal elements. Pathognomonic microscopic hallmark: sclerotic Medlar bodies ('copper pennies' or muriform cells)—thick-walled, golden-brown cells dividing by internal cleavage rather than budding.",
            clinical=True
        ),
        q(
            "A 58-year-old diabetic woman presents with fiery red, macerated plaques in her submammary folds and groin. The margins demonstrate characteristic small, discrete, peripheral pinpoint pustules and papules detached from the main plaque ('satellite lesions'). What is the diagnosis?",
            "Candidal intertrigo",
            ["Tinea cruris", "Seborrheic dermatitis", "Inverse psoriasis"],
            "Intertrigo caused by Candida albicans typically occurs in warm, moist, occluded anatomical skin folds (inframammary, axillary, inguinal, perianal). Diagnostic hallmark: bright red, glistening, macerated plaques surrounded by tiny, discrete pustules and papules with collarettes of scale situated outside the primary border, known as 'satellite lesions'.",
            clinical=True
        ),
        q(
            "A 30-year-old male from a rural river basin presents with a painless, friable, raspberry-like polypoid mass in his left nasal cavity that bleeds readily upon touching. Examination under light microscopy reveals giant, thick-walled sporangia measuring 100 to 350 microns packed with thousands of round endospores. What is the diagnosis?",
            "Rhinosporidiosis",
            ["Nasal polyp", "Paracoccidioidomycosis", "Coccidioidomycosis"],
            "Rhinosporidiosis is a chronic granulomatous infection of mucosal surfaces (predominantly the nasal mucosa and conjunctiva) caused by Rhinosporidium seeberi (a mesomycetozoean fish parasite). It presents as a bright red, soft, vascular, sessile or pedunculated 'strawberry' or 'raspberry' polypoid mass studded with tiny white dots (mature sporangia visible through the mucosal surface).",
            clinical=True
        ),
        q(
            "A 28-year-old female who regularly shaves her legs develops multiple deep, firm, inflammatory perifollicular nodules and pustules on both lower legs. Biopsy reveals dermatophytic hyphae and fungal spores invading down into the deep dermis and subcutaneous tissue surrounding ruptured hair follicles. What is this condition termed?",
            "Majocchi granuloma",
            ["Bacterial folliculitis", "Erythema nodosum", "Hidradenitis suppurativa"],
            "Majocchi granuloma (dermatophytic granuloma) is a deep fungal infection occurring when dermatophytes (most commonly Trichophyton rubrum) penetrate into the dermis and subcutaneous tissue. It is typically triggered by physical trauma (such as shaving legs) or the use of topical steroids, which disrupt the follicular infundibulum and allow dermatophytes to breach the dermis, inciting a suppurative granulomatous inflammatory reaction.",
            clinical=True
        ),
    ]),

    # Topic 6: Mycobacterial Infections: Tuberculosis (Non-important - 5 questions)
    (6, "Mycobacterial Infections: Tuberculosis", "easy", [
        q(
            "A 34-year-old female presents with a solitary, slowly spreading, brownish-red plaque on her cheek for 2 years. When a glass slide is firmly pressed against the lesion (diascopy), the background erythema blanches completely, revealing underlying translucent, yellowish-brown 'apple-jelly' nodules. What is the diagnosis?",
            "Lupus vulgaris",
            ["Scrofuloderma", "Sarcoidosis", "Discoid lupus erythematosus"],
            "Lupus vulgaris is the most common form of reinfection cutaneous tuberculosis, developing in individuals with high immunity and tuberculin hypersensitivity. Classic diagnostic test is diascopy (glass slide pressure), which empties congested capillaries to expose discrete, yellowish-brown, semi-translucent gelatinous granulomas known as 'apple-jelly nodules'. Untreated lesions cause severe destructive scarring of cartilage and carry a risk of squamous cell carcinoma.",
            clinical=True
        ),
        q(
            "A 14-year-old boy presents with painless enlargement of cervical lymph nodes that break down and ulcerate through the overlying skin. Examination reveals linear ulcers with undermined, ragged, bluish margins, discharging thin watery pus, interspersed with bridging keloidal scars. What is the diagnosis?",
            "Scrofuloderma",
            ["Lupus vulgaris", "Tuberculosis verrucosa cutis", "Cat-scratch disease"],
            "Scrofuloderma (tuberculosis colliquativa cutis) occurs by direct continuous extension of Mycobacterium tuberculosis from an underlying tuberculous focus (most frequently a cervical or axillary lymph node, bone, or joint) into the overlying skin. The cold abscess breaks down to form sinus tracts, sinuses, and linear ulcers with characteristic undermined, thinned, ragged, bluish-purple borders, healing with dense puckered, corded scars.",
            clinical=True
        ),
        q(
            "A pathologist who performs autopsies presents with an asymptomatic, firm, warty, hyperkeratotic plaque with a violaceous inflammatory halo on his right knuckle. Squeezing the indurated lesion expresses small droplets of pus from crevices between the warty papillae. What is this form of exogenous cutaneous tuberculosis termed?",
            "Tuberculosis verrucosa cutis (prosector's wart)",
            ["Lupus vulgaris", "Tuberculous chancre", "Verruca vulgaris"],
            "Tuberculosis verrucosa cutis (anatomist's wart / prosector's wart / butcher's wart) is an exogenous inoculation of M. tuberculosis into the skin of a previously sensitized host with high degrees of cell-mediated immunity. It typically occurs on hands, fingers, or soles as an indurated, warty, hyperkeratotic verrucous plaque with an erythematous border, exuding purulent exudate upon lateral compression.",
            clinical=True
        ),
        q(
            "A 28-year-old female presents with recurrent crops of painful, indurated, bluish-red subcutaneous nodules on the posterior lower calves that ulcerate, discharge necrotic slough, and heal with hyperpigmentation and depressed atrophic scars. Mantoux test is strongly positive (22 mm induration), and biopsy reveals lobular panniculitis with vasculitis and caseous necrosis. What is the diagnosis?",
            "Erythema induratum of Bazin",
            ["Erythema nodosum", "Polyarteritis nodosa", "Nodular vasculitis"],
            "Erythema induratum of Bazin is a classic tuberculid (a hypersensitivity reaction to hematogenously disseminated M. tuberculosis antigens in a patient with high tuberculin sensitivity). It characteristically presents on the calves (posterior lower legs) of young women as tender, violaceous nodules that frequently ulcerate (unlike erythema nodosum, which occurs on the anterior shins and never ulcerates). Biopsy demonstrates tuberculoid lobular panniculitis with necrotizing vasculitis.",
            clinical=True
        ),
        q(
            "What clinical entity represents the cutaneous equivalent of the primary Ghon complex, occurring in an unsensitized, non-immune individual (tuberculin negative) following primary exogenous inoculation of Mycobacterium tuberculosis into the skin?",
            "Tuberculous chancre (primary inoculation tuberculosis)",
            ["Lupus vulgaris", "Scrofuloderma", "Papulonecrotic tuberculid"],
            "Tuberculous chancre (primary cutaneous inoculation tuberculosis) arises when M. tuberculosis penetrates the skin of an unsensitized individual (usually an infant or child with negative tuberculin reactivity). A firm brownish-red papule develops at the inoculation site and ulcerates (the chancre), followed 3-8 weeks later by massive regional lymphadenopathy. Together, the skin chancre and regional lymph node constitute the primary cutaneous tuberculous complex.",
            clinical=False
        ),
    ]),

    # Topic 7: Leprosy (Important - 10 questions)
    (7, "Leprosy", "hard", [
        q(
            "According to the Ridley-Jopling classification of leprosy, what immunological parameter dictates the histological position, number of lesions, bacterial index (BI), and lepromin reactivity across the five-group spectrum?",
            "Host cell-mediated immunity (CMI) against Mycobacterium leprae",
            ["Humoral anti-phenolic glycolipid-1 antibody titer", "Serum complement C3 and C4 consumption levels", "Total circulating peripheral neutrophil count"],
            "The Ridley-Jopling classification organizes leprosy along a spectrum based strictly on the host's Cell-Mediated Immunity (CMI) against M. leprae: High CMI corresponds to Tuberculoid (TT) leprosy (single lesion, zero bacilli, strongly positive lepromin test). As CMI progressively falls through Borderline Tuberculoid (BT), Mid-borderline (BB), and Borderline Lepromatous (BL), to Lepromatous (LL) leprosy, bacterial load explodes (BI 5-6+), lesions become generalized, and lepromin test becomes completely negative.",
            clinical=False
        ),
        q(
            "A 32-year-old male presents with a single, large, hypopigmented, well-demarcated dry patch on his left forearm with elevated erythematous borders. Physical examination reveals complete loss of pain, temperature, and touch sensations within the patch, marked loss of sweating (anhidrosis), and an enlarged, non-tender left radial cutaneous nerve. Lepromin skin test is strongly positive (3+). What is the diagnosis?",
            "Tuberculoid leprosy (TT)",
            ["Lepromatous leprosy (LL)", "Borderline lepromatous leprosy (BL)", "Histoid leprosy"],
            "Tuberculoid (TT) leprosy represents the high-immunity pole of the spectrum. Cardinal features: 1. Single or few (<3) well-defined hypopigmented or erythematous dry patches with raised, beaded, spreading edges; 2. Complete cutaneous anesthesia (temperature lost first, then pain and light touch); 3. Complete anhidrosis and hair loss; 4. Thickened local dermal nerve; 5. High CMI with strongly positive lepromin test and undetectable acid-fast bacilli on slit-skin smear (BI = 0).",
            clinical=True
        ),
        q(
            "A 45-year-old male presents with diffuse infiltration of the facial skin, marked deepening of facial skin creases, thickening of earlobes, complete loss of the lateral two-thirds of the eyebrows (madarosis), saddle-nose deformity, and bilateral symmetrical glove-and-stocking sensory impairment. Slit-skin smear shows a Bacteriological Index of 6+ with abundant clumps of acid-fast bacilli ('globi'). What is this facial appearance termed?",
            "Leonine facies of lepromatous leprosy",
            ["Lupus pernio", "Scleroderma mask face", "Myxedema facies"],
            "Leonine facies ('lion-like face') is the pathognomonic late presentation of polar Lepromatous Leprosy (LL). Extensive dermal infiltration of the forehead, nose, cheeks, and earlobes by histiocytes packed with M. leprae leads to furrowed, thickened skin, madarosis (loss of eyebrow hairs starting laterally), collapse of nasal cartilage (saddle nose), and pendulous earlobes.",
            clinical=True
        ),
        q(
            "A patient with treated multibacillary leprosy presents with multiple firm, smooth, succulent, shiny, coppery-red nodules erupting on normal-appearing skin over the back and buttocks. Biopsy demonstrates spindle-shaped histiocytes arranged in a whorled or storiform pattern, packed with extraordinarily high numbers of uniform acid-fast bacilli aligned in parallel arrays. What variant of leprosy is this?",
            "Histoid leprosy",
            ["Indeterminate leprosy", "Lucio leprosy", "Borderline tuberculoid leprosy"],
            "Histoid leprosy is a distinctive, hyper-bacillary clinicopathological variant of lepromatous leprosy (originally described by Wade in patients relapsing after dapsone monotherapy or arising de novo). Hallmarks: dome-shaped, succulent, shiny nodules arising on normal-looking skin, containing spindle-shaped histiocytes in a storiform pattern densely stuffed with intensely acid-fast bacilli (longer than ordinary lepra bacilli) arranged in parallel 'cigar-like' packets.",
            clinical=True
        ),
        q(
            "A 28-year-old male with borderline tuberculoid (BT) leprosy undergoing Multi-Drug Therapy suddenly develops acute erythema, edema, and warmth within his preexisting skin patches, accompanied by acute pain and tenderness along the right ulnar nerve with impending claw hand. What is this immunological complication, and what is the definitive immediate management?",
            "Type 1 lepra reaction (reversal reaction); oral corticosteroids",
            ["Type 2 lepra reaction; oral thalidomide", "Jarisch-Herxheimer reaction; intravenous penicillin", "Dapsone hypersensitivity syndrome; stop all antibiotics"],
            "Type 1 lepra reaction (reversal reaction) is a delayed-type (Type IV) hypersensitivity reaction occurring in borderline forms of leprosy (BT, BB, BL) due to an abrupt surge in cell-mediated immunity against mycobacterial antigens. Hallmark: preexisting lesions become acutely inflamed, erythematous, and swollen, frequently associated with acute severe neuritis. Systemic corticosteroids (oral prednisolone starting at 40 mg/day) are the absolute treatment of choice to prevent irreversible permanent nerve damage.",
            clinical=True
        ),
        q(
            "A 36-year-old male with lepromatous leprosy presents with high remittent fever, malaise, and sudden eruption of crops of exquisitely tender, evanescent, bright pink subcutaneous nodules on his face and extensor extremities, accompanied by acute bilateral anterior uveitis and orchitis. What is this reaction termed, and what is its immunopathogenesis?",
            "Type 2 lepra reaction (erythema nodosum leprosum); immune complex-mediated (Type III) hypersensitivity",
            ["Type 1 lepra reaction; delayed-type (Type IV) hypersensitivity", "Lucio phenomenon; necrotizing panvasculitis", "Polyarteritis nodosa; ANCA-associated vasculitis"],
            "Type 2 lepra reaction (Erythema Nodosum Leprosum - ENL) is an immune complex-mediated (Type III) hypersensitivity reaction occurring in multibacillary patients (BL and LL) with heavy antigenic loads. Deposition of antigen-antibody-complement complexes in vascular walls incites an acute neutrophilic vasculitis, presenting as recurrent crops of tender, evanescent subcutaneous nodules, high fever, iridocyclitis, orchitis, and dactylitis. Thalidomide is the most potent and rapid drug of choice.",
            clinical=True
        ),
        q(
            "What is the standard World Health Organization (WHO) Multi-Drug Therapy (MDT) regimen and duration for an adult diagnosed with Paucibacillary (PB) Leprosy (1 to 5 skin lesions)?",
            "Monthly Rifampicin 600 mg + Daily Dapsone 100 mg for 6 months",
            ["Monthly Rifampicin + Monthly Clofazimine for 12 months", "Daily Dapsone 100 mg monotherapy for 24 months", "Daily Ofloxacin + Daily Minocycline for 3 months"],
            "WHO MDT regimen for adult Paucibacillary (PB) leprosy (1 to 5 lesions, single nerve trunk involvement, skin smear negative at all sites): 1. Rifampicin: 600 mg once a month, administered under direct supervision; 2. Dapsone: 100 mg daily, self-administered. Total duration is 6 months (to be completed within 9 months).",
            clinical=False
        ),
        q(
            "What is the standard adult WHO Multi-Drug Therapy (MDT) regimen and duration for Multibacillary (MB) Leprosy (more than 5 lesions, or any slit-skin smear positivity)?",
            "Monthly Rifampicin/Clofazimine + Daily Clofazimine/Dapsone for 12 months",
            ["Daily Rifampicin + Daily Dapsone for 6 months", "Daily Clofazimine + Daily Dapsone for 24 months", "Weekly Rifampicin + Daily Isoniazid for 18 months"],
            "WHO MDT for adult Multibacillary (MB) leprosy (more than 5 lesions, or multi-nerve involvement, or any positive slit-skin smear): 1. Rifampicin: 600 mg once a month, supervised; 2. Clofazimine: 300 mg once a month (supervised) PLUS 50 mg daily (self-administered); 3. Dapsone: 100 mg daily, self-administered. Total duration is 12 months (to be completed within a maximum of 18 months).",
            clinical=False
        ),
        q(
            "Which peripheral nerve is most commonly thickened and involved in Leprosy, and what characteristic motor claw hand deformity results from its irreversible motor branch paralysis?",
            "Ulnar nerve (causing medial two lumbricals claw hand)",
            ["Radial nerve (causing wrist drop)", "Median nerve (causing ape thumb)", "Common peroneal nerve (causing foot drop)"],
            "The Ulnar nerve (at the ulnar groove behind the medial epicondyle) is the most commonly involved and enlarged nerve trunk in leprosy. Paralysis of ulnar-innervated intrinsic hand muscles (hypothenar, all interossei, medial two lumbricals, adductor pollicis) leads to clawing of the little and ring fingers (hyperextension at MCP joints and flexion at IP joints) and severe hypothenar wasting.",
            clinical=False
        ),
        q(
            "What is the distinct histopathological hallmark of the 'Lucio phenomenon' (erythema necroticans) seen exclusively in diffuse non-nodular lepromatous leprosy of Lucio and Latapi?",
            "Endothelial bacterial invasion causing occlusive thrombosis and infarction",
            ["Neutrophilic microabscesses within stratum corneum", "Non-caseating epithelioid granulomas around cutaneous nerves", "Acantholytic split at suprabasal epidermis"],
            "Lucio's phenomenon is a severe, necrotizing vasculitic reaction seen almost exclusively in patients with pure diffuse lepromatous leprosy of Lucio and Latapi (endemic to Mexico and Central America). Histology reveals massive direct invasion of capillary endothelial cells by M. leprae, causing endothelial proliferation, occlusive thrombosis, ischemic dermal infarction, and jagged, geographic purpuric ulcers.",
            clinical=False
        ),
    ]),

    # Topic 8: Miscellaneous Parasitic Disorders (Non-important - 5 questions)
    (8, "Miscellaneous Parasitic Disorders", "easy", [
        q(
            "A 28-year-old male who recently traveled to an endemic Middle Eastern region presents with a painless, indurated erythematous papule on his exposed forearm that slowly enlarged and ulcerated over 3 months into a shallow, crateriform ulcer with an elevated, violaceous border covered by a thick crust ('oriental sore'). Giemsa-stained smear of dermal scrapings demonstrates Leishman-Donovan (LD) bodies. What is the vector transmitting this infection?",
            "Sandfly (Phlebotomus species)",
            ["Tsetse fly (Glossina species)", "Blackfly (Simulium species)", "Deerfly (Chrysops species)"],
            "Cutaneous leishmaniasis (Oriental sore / Delhi boil / Aleppo evil) is caused by Leishmania tropica, Leishmania major, or Leishmania aethiopica, transmitted by the bite of the female phlebotomine sandfly (Phlebotomus species in the Old World; Lutzomyia in the New World). The promastigotes enter dermal macrophages and transform into round-to-oval amastigotes (LD bodies).",
            clinical=True
        ),
        q(
            "A 35-year-old male from Bihar presents with multiple asymptomatic, hypopigmented macules across the trunk and progressive, erythematous, non-ulcerating nodules distributed symmetrically across the face in a butterfly distribution, 4 years after being successfully treated for Visceral Leishmaniasis (Kala-azar). What is the diagnosis?",
            "Post-kala-azar dermal leishmaniasis (PKDL)",
            ["Lepromatous leprosy", "Secondary syphilis", "Lupus vulgaris"],
            "Post-Kala-Azar Dermal Leishmaniasis (PKDL) is a dermatological sequel to visceral leishmaniasis caused by Leishmania donovani (occurring in up to 10% of cases in India, usually 2-7 years post-kala-azar). Clinical spectrum: hypopigmented macules, erythematous butterfly patches on face, and succulent non-ulcerating nodular lesions. Patients act as the primary human reservoir for leishmaniasis transmission in non-epidemic periods.",
            clinical=True
        ),
        q(
            "A 24-year-old tourist returns from walking barefoot on a Caribbean beach with an intensely pruritic, erythematous, winding, thread-like serpiginous track on the sole and lateral border of his right foot that advances by 1 to 2 cm each day. What is the diagnosis and etiology?",
            "Cutaneous larva migrans; animal hookworm larvae (Ancylostoma braziliense)",
            ["Cutaneous larva currens; Strongyloides stercoralis", "Dracunculiasis; Dracunculus medinensis", "Scabies; Sarcoptes scabiei"],
            "Cutaneous larva migrans (creeping eruption) is caused by percutaneous penetration of third-stage filariform larvae of animal hookworms (most commonly Ancylostoma braziliense or Ancylostoma caninum from dogs/cats). Because humans are accidental hosts, the larvae lack collagenases to breach the basement membrane and wander aimlessly within the epidermis, producing an intensely pruritic, creeping, serpiginous inflammatory track. Treatment is oral albendazole or ivermectin.",
            clinical=True
        ),
        q(
            "A traveler returning from rural sub-Saharan Africa presents with a painful, swollen, white papule with a central dark punctum on the periungual border of her great toe. Dermoscopy reveals a central black opening surrounded by a whitish halo (the posterior abdomen of an embedded gravid flea). What is this infestation termed?",
            "Tungiasis (Tunga penetrans)",
            ["Cutaneous myiasis", "Scabies burrow", "Verruca vulgaris"],
            "Tungiasis is an ectoparasitosis caused by the burrowing flea Tunga penetrans (jigger / chigoe flea). The fertilized female flea burrows into the periungual epidermis of the toes or soles, swelling to the size of a pea as its abdomen distends with eggs. It presents as a white papulonodule with a central black dot (the flea's respiratory spiracles and anus) through which eggs are expelled.",
            clinical=True
        ),
        q(
            "A 32-year-old field biologist presents with two tender, furuncle-like erythematous nodules on his scalp. He reports a bizarre sensation of localized crawling and squirming beneath the skin. On close examination, each nodule exhibits a central pore with serosanguinous discharge through which a respiratory spiracle occasionally protrudes. What is the diagnosis?",
            "Furuncular myiasis (Dermatobia hominis)",
            ["Furunculosis", "Ruptured epidermoid cyst", "Hidradenitis suppurativa"],
            "Furuncular cutaneous myiasis is an infestation of viable human skin by dipterous fly larvae (maggots), most commonly Dermatobia hominis (human botfly, Central/South America) or Cordylobia anthropophaga (tumbu fly, Africa). The larva develops inside a tender, boil-like subcutaneous cavity with a central respiratory spiracle hole that discharges serous fluid.",
            clinical=True
        ),
    ]),

    # Topic 9: Common Infestations (Important - 10 questions)
    (9, "Common Infestations", "hard", [
        q(
            "A 22-year-old male complains of intense, unrelenting itching that is excruciatingly worse at night in bed. Physical examination reveals erythematous excoriated papules in the finger web spaces, flexor wrists, axillae, anterior axillary folds, periumbilical area, and buttocks, with prominent pruritic nodules on the shaft of the penis and scrotum. What is this classic anatomical distribution termed?",
            "Circle of Hebra in Scabies",
            ["Langer lines in Pityriasis rosea", "Blaschko lines in Mosaicism", "Crowe distribution in Neurofibromatosis"],
            "The classic anatomical distribution of scabies lesions is known as the 'Circle of Hebra': it spares the head, neck, and upper back in immunocompetent adults, preferentially targeting thin stratum corneum regions: interdigital web spaces of fingers, flexor aspects of wrists, elbows, axillary folds, umbilicus, belt-line, genitalia (penis/scrotum in men, areolae in women), and buttocks.",
            clinical=True
        ),
        q(
            "A 64-year-old bedridden patient with advanced Parkinson's disease residing in a nursing facility presents with generalized, thick, psoriasiform, yellow-gray, fissured, hyperkeratotic crusts over the hands, palms, soles, and scalp with minimal pruritus. Skin scraping under light microscopy reveals thousands of live mites and ova per high-power field. What is this condition termed?",
            "Crusted (Norwegian) scabies",
            ["Psoriatic erythroderma", "Severe seborrheic dermatitis", "Darier disease"],
            "Crusted (Norwegian) scabies is a rare, hyper-infestation occurring in immunocompromised, neurologically impaired, or institutionalized patients who cannot mount a normal cell-mediated hypersensitivity response or cannot scratch. The skin is colonized by millions of Sarcoptes scabiei mites, producing thick, warty, asbestos-like, malodorous hyperkeratotic crusts. Because itching is absent or minimal, diagnosis is frequently delayed, triggering devastating institutional epidemics.",
            clinical=True
        ),
        q(
            "What microscopic structures identified on a mineral oil preparation from an unroofed skin burrow definitively establish the microbiological diagnosis of Scabies?",
            "Sarcoptes scabiei female mite, oval eggs, and scybala",
            ["Flagellated trophozoites and undulating membranes", "Non-septate broad hyphae and sporangiospores", "Leishman-Donovan amastigotes inside histiocytes"],
            "Definitive microscopic confirmation of scabies is made by placing a drop of mineral oil over a fresh, intact burrow, scraping the lesion vigorously with a sterile scalpel blade down to the stratum basale, and examining under low power (10x-40x) light microscopy. Visualizing the eight-legged adult female mite (with anterior suckers and dorsal spines), oval translucent eggs, or characteristic brownish fecal pellets (scybala) confirms the diagnosis.",
            clinical=False
        ),
        q(
            "What is the first-line topical drug of choice for the treatment of classic Scabies in adults, and what is the proper application protocol?",
            "5% Permethrin cream applied overnight, repeated in 7-14 days",
            ["1% Lindane lotion applied daily for 14 days", "10% Benzyl benzoate applied for 30 minutes", "0.5% Malathion shampoo washed after 5 minutes"],
            "Permethrin 5% cream is the topical gold standard for scabies. It acts by disrupting sodium channel conductance, causing neurotoxic paralysis and death of the mite. Protocol: applied thoroughly to all skin surfaces from the chin/jawline down to the toes (including under fingernails, umbilicus, and genitalia), left on overnight for 8-14 hours before washing off, and repeated after 7 to 14 days to eliminate newly hatched nymphs. All close household contacts must be treated simultaneously.",
            clinical=False
        ),
        q(
            "What is the recommended oral dosage and scheduling of Ivermectin for the management of Scabies, and in which patient populations is its use strictly contraindicated?",
            "Oral Ivermectin 200 mcg/kg repeated at 14 days; avoid in pregnancy/<15 kg",
            ["Oral Ivermectin 50 mcg/kg daily for 7 days; avoid in renal failure", "Oral Ivermectin 12 mg single dose without repetition; avoid in elderly", "Oral Ivermectin 400 mcg/kg monthly; avoid in hypertension"],
            "Oral Ivermectin is dosed at 200 micrograms/kg taken with a fatty meal, and a second dose MUST be repeated 10-14 days later because ivermectin is not ovicidal (it does not kill mite eggs; the second dose catches newly hatched larvae before they reach sexual maturity). It is contraindicated during pregnancy, lactation, and in young children weighing less than 15 kg due to the risk of crossing the immature blood-brain barrier.",
            clinical=False
        ),
        q(
            "A 19-year-old male was successfully treated for scabies with two courses of 5% permethrin cream 6 weeks ago. Repeated skin scrapings are negative for mites. However, he presents with intensely pruritic, firm, persistent, reddish-brown nodules on the shaft of his penis and scrotum. What is the diagnosis?",
            "Post-scabetic nodular scabies",
            ["Active persistent scabies infection", "Primary syphilitic chancre", "Lichen planus"],
            "Post-scabetic nodules (nodular scabies) develop in 7-10% of patients and can persist for months after the active scabies infestation has been completely eradicated. They represent a sterile, localized, cell-mediated hypersensitivity reaction to retained, dead mite parts and antigens in the dermis. They are not contagious and are best managed with potent topical or intralesional corticosteroids.",
            clinical=True
        ),
        q(
            "An 8-year-old schoolgirl presents with intense occipital scalp itching and localized cervical lymphadenopathy. Examination reveals oval, white, gleaming operculated nits firmly cemented to the hair shafts near the scalp that cannot be detached by sliding with fingers. What is the diagnosis and organism?",
            "Pediculosis capitis; Pediculus humanus capitis",
            ["Pediculosis corporis; Pediculus humanus corporis", "White piedra; Trichosporon asahii", "Pseudonits (hair casts); keratin scales"],
            "Pediculosis capitis (head lice infestation) is caused by Pediculus humanus capitis. Nits (eggs) are glued firmly to hair shafts by a chitinous cement secreted by the female louse, distinguishing them from dandruff or hair casts which slide easily along the shaft. Nits located within 6 mm of the scalp indicate active, viable infestation. Standard treatment is 1% permethrin lotion or 0.5% malathion lotion.",
            clinical=True
        ),
        q(
            "A homeless male presents with diffuse excoriations, post-inflammatory hyperpigmentation, and lichenification on his trunk and shoulders ('vagabond disease'). Lice and nits are found clustered within the seams of his clothing rather than on his skin. Which three major systemic infectious diseases are vector-borne transmitted by this parasite?",
            "Epidemic typhus, trench fever, and relapsing fever",
            ["Scrub typhus, Q fever, and Lyme disease", "Rocky Mountain spotted fever, tularemia, and ehrlichiosis", "Plague, murine typhus, and Chagas disease"],
            "Pediculus humanus corporis (the body louse) lives in the seams of clothing and visits the human skin only to feed. Chronic infestation causes the dry, thickened, hyperpigmented 'vagabond's skin'. The body louse is a medically dangerous vector transmitting three life-threatening epidemic diseases: 1. Epidemic typhus (Rickettsia prowazekii); 2. Trench fever (Bartonella quintana); 3. Louse-borne relapsing fever (Borrelia recurrentis).",
            clinical=True
        ),
        q(
            "A 24-year-old sexually active male presents with intense pubic pruritus. Examination reveals rust-colored specks on his underwear and multiple asymptomatic, discrete, non-blanching, slate-gray or bluish macules (3 to 10 mm) scattered across the lower abdomen and thighs. What are these characteristic macules termed, and what produces them?",
            "Maculae caeruleae; caused by louse saliva enzymes altering host hemoglobin to biliverdin",
            ["Koplik spots; caused by viral endothelial necrosis", "Janeway lesions; caused by septic micro-emboli", "Osler nodes; caused by immune complex vasculitis"],
            "Maculae caeruleae (taches bleues) are pathognomonic, slate-gray, bluish, non-tender, non-blanching macules seen in Phthiriasis (Pediculosis pubis / crab louse infestation). They are produced by the action of an anticoagulant salivary enzyme secreted by Phthirus pubis during feeding, which enzymatically degrades host heme/bilirubin into biliverdin in the subcutaneous fat.",
            clinical=True
        ),
        q(
            "A hotel guest awakens with rows of intensely pruritic, erythematous, edematous papules arranged in linear groups of three along her exposed arm and neck ('breakfast, lunch, and dinner' sign). What arthropod is responsible for this distinct biting pattern?",
            "Cimex lectularius (Bedbug)",
            ["Pulex irritans (Flea)", "Culicoides (Biting midge)", "Ixodes scapularis (Deer tick)"],
            "Cimex lectularius (the human bedbug) feeds nocturnally on exposed skin surfaces while the host sleeps. The bites classically present in a linear, consecutive grouping of three or four lesions, historically termed the 'breakfast, lunch, and dinner' sign, corresponding to sequential test bites along a capillary bed by a feeding bug.",
            clinical=True
        ),
    ]),
]
