import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Infectious Diseases"
CHAPTER_ORDER = 5
SOURCE_PDF = "medicine 1"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def q(prompt, answer, wrong, explanation, clinical=False):
    return {
        "prompt": prompt.strip(),
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "high" if clinical else "moderate",
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("Approach to Fever and Sepsis", [
        q("Sepsis is best defined as", "Life-threatening organ dysfunction caused by a dysregulated host response to infection", ["Fever with leukocytosis only", "Any positive blood culture", "Localized infection without systemic effects"], "Modern sepsis definitions emphasize organ dysfunction from dysregulated response, not fever alone."),
        q("A hypotensive febrile patient has lactate 5 mmol/L despite fluids. What is the syndrome?", "Septic shock", ["Simple viral fever", "Heat exhaustion", "Drug fever only"], "Septic shock involves vasopressor-requiring hypotension or severe hypoperfusion with elevated lactate.", True),
        q("Which action should not be delayed in suspected septic shock?", "Early broad-spectrum antimicrobials after appropriate cultures if feasible", ["Waiting for all cultures to finalize", "Steroids before antibiotics in every patient", "Discharge if fever transiently falls"], "Delays in effective antimicrobial therapy increase mortality in septic shock."),
        q("Blood cultures are most useful when obtained", "Before antibiotics, without delaying urgent therapy", ["Only after 7 days of antibiotics", "From a single bottle only", "Only after fever resolves"], "Cultures improve pathogen identification but should not postpone lifesaving treatment."),
        q("A patient with fever, confusion, hypotension, thrombocytopenia and rising creatinine most likely has", "Sepsis with organ dysfunction", ["Uncomplicated rhinitis", "Stable chronic anemia", "Migraine"], "Altered mentation, shock, thrombocytopenia and kidney injury are organ dysfunction clues.", True),
        q("Procalcitonin is best used as", "An adjunct to clinical judgment, especially for antibiotic de-escalation in selected settings", ["A perfect test for all infections", "A replacement for cultures", "Proof that viral disease is impossible"], "Biomarkers can support but not replace clinical assessment."),
        q("Source control in infection means", "Drainage, removal or correction of the infected focus when needed", ["Only prescribing antipyretics", "Avoiding imaging", "Stopping all antibiotics"], "Abscess drainage, device removal and debridement are examples of source control."),
        q("A diabetic patient has fever and a fluctuant thigh abscess. Best management includes", "Incision and drainage plus appropriate antibiotics if systemic illness is present", ["Antibiotics alone in every abscess", "Steroid injection into the abscess", "No treatment until culture returns"], "Abscess cure usually requires drainage; antibiotics are added for systemic or high-risk cases.", True),
        q("Persistent fever after 72 hours of antibiotics should prompt", "Reassessment for wrong diagnosis, resistant organism, inadequate source control or drug fever", ["Automatic doubling of every dose", "Stopping all evaluation", "Assuming malingering"], "Nonresponse requires a structured reassessment rather than blind escalation."),
        q("Which clinical clue suggests infection in an elderly patient even without fever?", "New delirium or functional decline", ["Improved appetite", "Stable baseline mobility", "Lower creatinine"], "Older adults may present with delirium, falls or decline rather than classic fever.", True),
    ]),
    ("Antimicrobial Principles and Stewardship", [
        q("Empiric antibiotic choice should be guided by", "Likely site, pathogens, severity, host factors and local resistance", ["Drug color", "Newest available brand", "Patient preference alone"], "Rational empiric therapy balances coverage with resistance and toxicity risk."),
        q("De-escalation means", "Narrowing therapy based on culture data and clinical response", ["Adding more antibiotics daily", "Stopping therapy before diagnosis", "Avoiding cultures"], "Stewardship reduces unnecessary broad-spectrum exposure."),
        q("A patient with E. coli bacteremia susceptible to ceftriaxone improves after meropenem. Best stewardship step?", "Switch to a narrower active agent such as ceftriaxone", ["Continue meropenem indefinitely", "Add vancomycin", "Stop all therapy immediately"], "Culture-directed narrowing preserves efficacy and reduces resistance pressure.", True),
        q("Time-dependent antibiotics are optimized mainly by", "Maintaining drug concentration above MIC for sufficient time", ["Maximizing only peak level", "Avoiding repeated dosing", "Binding red cells"], "Beta-lactams are classic time-dependent antimicrobials."),
        q("Concentration-dependent killing is characteristic of", "Aminoglycosides", ["Penicillin V", "Vancomycin only", "Fluconazole only"], "Aminoglycosides have peak-dependent killing and post-antibiotic effect."),
        q("A patient on gentamicin develops rising creatinine and vestibular symptoms. The toxicity is", "Nephrotoxicity and ototoxicity", ["Aplastic crisis", "Serotonin syndrome", "Hyperthyroidism"], "Aminoglycosides can injure kidney and inner ear.", True),
        q("Antibiotic duration should generally be", "The shortest effective course for the syndrome and source control achieved", ["Always 6 weeks", "Until all fatigue disappears", "One dose for all infections"], "Shorter validated courses reduce adverse events and resistance."),
        q("Colonization differs from infection because colonization means", "Organism presence without tissue invasion or host injury", ["Mandatory fever", "Positive culture requiring antibiotics always", "Bloodstream spread"], "Treating colonization often causes harm without benefit."),
        q("An asymptomatic catheterized patient has bacteriuria but no fever, dysuria or instability. Best approach is usually", "Do not treat unless a specific indication exists", ["Give broad-spectrum antibiotics", "Treat until urine is sterile forever", "Start antifungals"], "Asymptomatic bacteriuria is usually not treated except in selected groups such as pregnancy or urologic procedures.", True),
        q("Clostridioides difficile risk rises most after", "Broad-spectrum antibiotic exposure disrupting gut flora", ["Vaccination", "Iron deficiency", "Short fasting"], "Antibiotics can disrupt normal flora and allow C. difficile overgrowth.", True),
    ]),
    ("HIV and Opportunistic Infections", [
        q("The most useful marker of HIV immune status is", "CD4 T-cell count", ["Serum sodium", "Platelet volume", "Urine pH"], "CD4 count estimates cellular immune depletion and opportunistic infection risk."),
        q("HIV viral load is most useful for", "Monitoring antiretroviral treatment response", ["Diagnosing iron deficiency", "Grading proteinuria", "Measuring clotting factors"], "Falling viral load indicates effective ART and adherence."),
        q("A patient with HIV has CD4 count 80 and subacute dyspnea with diffuse interstitial infiltrates. Likely infection?", "Pneumocystis jirovecii pneumonia", ["Rhinovirus cold", "Tetanus", "Uncomplicated cystitis"], "PCP classically occurs with CD4 below 200 and causes hypoxemic pneumonia.", True),
        q("PCP prophylaxis is generally indicated when CD4 count is below", "200 cells/microliter", ["800 cells/microliter", "600 cells/microliter", "500 cells/microliter only"], "TMP-SMX prophylaxis is used below CD4 200 or equivalent risk settings."),
        q("Which infection suggests advanced AIDS when CD4 is below 50?", "Disseminated Mycobacterium avium complex", ["Impetigo only", "Acute otitis externa", "Simple dermatophyte infection"], "MAC risk rises markedly with profound CD4 depletion."),
        q("A patient with AIDS has ring-enhancing brain lesions and positive toxoplasma IgG. Initial treatment should target", "Toxoplasma gondii", ["Prion disease", "Rabies", "Tetanus"], "Multiple ring-enhancing lesions in advanced HIV commonly represent toxoplasmosis.", True),
        q("When should ART usually be started in HIV care?", "As soon as possible after diagnosis, with timing adjusted for certain opportunistic infections", ["Only after CD4 reaches zero", "Never during chronic disease", "Only after symptoms resolve for years"], "Early ART improves outcomes, though selected OIs require careful timing."),
        q("Immune reconstitution inflammatory syndrome occurs after ART because", "Recovering immunity mounts inflammation against existing antigens or infections", ["ART directly destroys neutrophils", "HIV viral load rises intentionally", "Antibiotics stop working"], "IRIS is paradoxical inflammatory worsening after immune recovery."),
        q("An HIV patient starts ART and soon develops worsening lymphadenitis while viral load falls. What is likely?", "Immune reconstitution inflammatory syndrome", ["ART failure", "Drug-induced aplastic anemia only", "New diabetes"], "Clinical worsening with virologic response after ART can be IRIS.", True),
        q("Which counseling point is essential for ART?", "Excellent adherence prevents resistance and maintains viral suppression", ["Skipping doses improves tolerance long term", "ART can be stopped once symptoms improve", "Resistance cannot develop"], "Suboptimal adherence permits viral replication under drug pressure and resistance.", True),
    ]),
    ("Tuberculosis and Mycobacterial Disease", [
        q("Pulmonary tuberculosis classically spreads by", "Airborne droplet nuclei", ["Fecal-oral transmission", "Mosquito bite", "Direct blood transfusion only"], "TB is transmitted through inhaled aerosolized droplet nuclei."),
        q("Latent TB infection means", "Immune containment without clinical or radiographic active disease", ["No exposure ever occurred", "Always contagious", "Mandatory cavitary disease"], "Latent infection has viable organisms contained by immunity without active symptoms."),
        q("A man has chronic cough, fever, night sweats, weight loss and upper-lobe cavitation. Most likely diagnosis?", "Pulmonary tuberculosis", ["Acute viral bronchitis", "Stable asthma", "Pulmonary edema"], "Constitutional symptoms plus apical cavitary lung disease strongly suggest TB.", True),
        q("Which test confirms rifampicin resistance rapidly in suspected TB?", "Nucleic acid amplification test with resistance detection", ["ESR alone", "Mantoux size alone", "Chest x-ray alone"], "Molecular tests can detect M. tuberculosis and rifampicin resistance quickly."),
        q("Standard first-line intensive TB therapy includes isoniazid, rifampicin, pyrazinamide and", "Ethambutol", ["Acyclovir", "Amphotericin B", "Oseltamivir"], "RIPE therapy is the classic initial regimen for drug-susceptible TB."),
        q("A TB patient on ethambutol reports reduced visual acuity and red-green color difficulty. The drug toxicity is", "Optic neuritis", ["Ototoxicity", "Pancreatitis", "Aplastic anemia"], "Ethambutol can cause optic neuritis and color vision defects.", True),
        q("Isoniazid neuropathy is prevented by giving", "Pyridoxine", ["Folic acid only", "Vitamin C only", "Calcium carbonate"], "Vitamin B6 reduces INH-associated peripheral neuropathy risk."),
        q("Tuberculous meningitis treatment usually requires", "Prompt multidrug anti-TB therapy plus adjunctive corticosteroids", ["Observation only", "Single-dose azithromycin", "No treatment until culture finalizes"], "TB meningitis is severe and steroids reduce inflammatory complications."),
        q("A patient with HIV and TB begins treatment. Why is rifampicin interaction important?", "It induces hepatic enzymes and can lower levels of many antiretrovirals", ["It blocks all renal excretion", "It permanently raises CD4 count", "It has no interactions"], "Rifampicin is a potent inducer affecting many ART regimens.", True),
        q("Miliary TB is best described as", "Disseminated hematogenous TB with numerous tiny lesions", ["Localized skin wart", "Single lobar pneumonia only", "Noninfectious granuloma"], "Hematogenous spread produces millet-seed lesions across organs.", True),
    ]),
    ("Respiratory and CNS Infections", [
        q("Community-acquired pneumonia severity assessment helps decide", "Outpatient treatment versus admission or ICU care", ["Cancer stage", "Need for dialysis in all patients", "Blood group"], "Severity scoring and clinical judgment guide site of care."),
        q("Typical bacterial pneumonia often presents with", "Fever, productive cough, pleuritic pain and focal consolidation", ["Painless jaundice", "Polyuria only", "Migratory arthritis only"], "Lobar findings and purulent sputum are classic for typical bacterial pneumonia."),
        q("A confused elderly patient has fever, cough, hypoxia and right lower lobe crackles. Initial management includes", "Antibiotics targeting community-acquired pneumonia and oxygen/supportive care", ["No treatment because cough is absent in elderly", "Anticoagulation only", "High-dose steroids alone"], "Older adults may present atypically but hypoxic pneumonia requires prompt therapy.", True),
        q("Atypical pneumonia pathogens include", "Mycoplasma pneumoniae", ["Plasmodium vivax", "Candida albicans in all cases", "Taenia solium"], "Mycoplasma, Chlamydophila and Legionella are classic atypical causes."),
        q("Bacterial meningitis classically causes", "Fever, headache, neck stiffness and altered mental status", ["Painless hematuria", "Isolated ankle edema", "Chronic pruritus only"], "The classic meningitis syndrome reflects meningeal inflammation."),
        q("A febrile patient has headache, neck stiffness and purpuric rash. Which pathogen is a major concern?", "Neisseria meningitidis", ["Rhinovirus", "Enterobius vermicularis", "Dermatophyte"], "Meningococcemia can cause meningitis, petechiae/purpura and shock.", True),
        q("Empiric bacterial meningitis therapy should be started", "Immediately after blood cultures and lumbar puncture if LP will not delay treatment", ["Only after culture finalizes", "After one week of observation", "Only when rash appears"], "Meningitis is time-critical; antibiotics should not be delayed."),
        q("When is brain imaging needed before lumbar puncture?", "Focal neurologic deficit, papilledema, seizure, immunocompromise or impaired consciousness", ["Every mild sore throat", "Normal neurologic exam always", "Before any blood culture"], "Imaging reduces herniation risk in selected high-risk patients."),
        q("A patient with temporal lobe seizures, fever and altered behavior has CSF lymphocytosis. Best empiric antiviral?", "Acyclovir", ["Oseltamivir", "Fluconazole", "Praziquantel"], "HSV encephalitis affects temporal lobes and requires urgent IV acyclovir.", True),
        q("Brain abscess management usually requires", "Antibiotics plus neurosurgical drainage for selected size, mass effect or diagnosis", ["Antipyretics only", "No imaging", "Oral vitamins"], "Abscess care combines pathogen coverage with drainage when indicated.", True),
    ]),
    ("Gastrointestinal and Hepatobiliary Infections", [
        q("Acute watery diarrhea is most often caused by", "Viral or toxin-mediated enteric infection", ["Multiple myeloma", "Aortic stenosis", "Nephrotic syndrome"], "Most acute watery diarrhea is infectious and self-limited, often viral."),
        q("Dysentery means diarrhea with", "Blood and inflammatory features", ["Only pale stools", "No abdominal symptoms", "Constipation"], "Dysentery suggests invasive or inflammatory colitis."),
        q("A traveler develops high-volume rice-water stools and dehydration after unsafe water exposure. Likely organism?", "Vibrio cholerae", ["Clostridioides tetani", "Mycobacterium leprae", "Aspergillus fumigatus"], "Cholera causes profuse watery diarrhea and rapid dehydration.", True),
        q("The most important treatment for most acute infectious diarrhea is", "Rehydration and electrolyte replacement", ["Immediate colon surgery", "Long steroids", "Chemotherapy"], "Fluid replacement prevents morbidity and mortality."),
        q("Antibiotics should be avoided in suspected STEC infection because they may increase risk of", "Hemolytic uremic syndrome", ["Migraine", "Asthma", "Hyperthyroidism"], "Antibiotics may increase Shiga toxin release and HUS risk."),
        q("A child has bloody diarrhea followed by anemia, thrombocytopenia and renal failure. Diagnosis?", "Hemolytic uremic syndrome", ["Guillain-Barre syndrome", "Acute pancreatitis", "Typhoid fever"], "Post-diarrheal HUS follows Shiga toxin-producing infection.", True),
        q("Typhoid fever is transmitted mainly by", "Fecal-oral route through contaminated food or water", ["Airborne spores", "Tick bite only", "Sexual contact only"], "Salmonella Typhi spreads by ingestion of contaminated food or water."),
        q("Acute viral hepatitis with very high aminotransferases is most consistent with", "Hepatocellular injury", ["Pure cholestasis only", "Nephritic syndrome", "Myocarditis only"], "Marked AST/ALT elevation reflects hepatocyte injury."),
        q("A patient has fever, right upper quadrant pain and jaundice. What triad is this?", "Charcot triad of acute cholangitis", ["Beck triad", "Cushing triad", "Virchow triad"], "Cholangitis presents with fever, jaundice and RUQ pain and may progress to sepsis.", True),
        q("Liver abscess due to Entamoeba histolytica classically produces", "Anchovy sauce-like aspirate", ["Caseous sputum", "Rice-water stool only", "Blue-green pus"], "Amoebic liver abscess aspirate is classically brown, thick and acellular.", True),
    ]),
    ("Urinary, Skin and Soft Tissue Infections", [
        q("Uncomplicated cystitis typically presents with", "Dysuria, frequency and urgency without systemic illness", ["Hemoptysis", "Neck stiffness", "Painless jaundice"], "Lower UTI causes irritative voiding symptoms."),
        q("Pyelonephritis is suggested by", "Fever, flank pain and costovertebral angle tenderness", ["Isolated pruritus", "Painless edema", "Vertigo"], "Upper UTI involves renal parenchyma and systemic symptoms."),
        q("A young woman has dysuria, frequency and positive nitrites but no fever or flank pain. Likely diagnosis?", "Acute uncomplicated cystitis", ["Acute pyelonephritis", "Meningitis", "Cellulitis"], "Localized lower urinary symptoms without systemic signs fit cystitis.", True),
        q("The most common cause of uncomplicated UTI is", "Escherichia coli", ["Neisseria meningitidis", "Plasmodium falciparum", "Influenza A"], "Uropathogenic E. coli is the dominant cause."),
        q("Cellulitis usually involves", "Dermis and subcutaneous tissue", ["Only epidermal stratum corneum", "Bone marrow exclusively", "Synovial fluid only"], "Cellulitis is a spreading infection of deeper skin and subcutaneous tissue."),
        q("A patient has rapidly progressive painful leg infection, bullae, crepitus and shock. Diagnosis to suspect?", "Necrotizing fasciitis", ["Simple tinea pedis", "Contact dermatitis", "Lipoma"], "Pain, systemic toxicity, bullae or gas suggest necrotizing soft tissue infection.", True),
        q("Necrotizing fasciitis management requires", "Urgent surgical debridement plus broad-spectrum antibiotics", ["Topical antifungal only", "Delayed outpatient review", "Compression stockings only"], "Surgery is lifesaving and should not wait for complete imaging."),
        q("Purulent skin abscess is primarily treated by", "Incision and drainage", ["Long-term steroids", "Radiotherapy", "No drainage ever"], "Drainage is the key treatment for a drainable abscess."),
        q("A diabetic patient has foot ulcer probing to bone with fever. Which complication is likely?", "Osteomyelitis", ["Migraine", "Viral rhinitis", "Gastritis"], "Probe-to-bone and systemic signs in diabetic foot ulcer suggest bone infection.", True),
        q("Erysipelas differs from cellulitis by having", "Raised sharply demarcated superficial inflammation", ["No erythema", "Only nerve involvement", "Mandatory abscess cavity"], "Erysipelas is a superficial dermal lymphatic infection with well-defined margins.", True),
    ]),
    ("Vector-Borne and Zoonotic Infections", [
        q("Malaria is transmitted by", "Female Anopheles mosquitoes", ["Aedes mosquitoes only", "Sandflies", "Ticks"], "Anopheles mosquitoes transmit Plasmodium species."),
        q("Severe falciparum malaria may cause", "Cerebral malaria, severe anemia, acidosis and renal failure", ["Only mild rhinitis", "Chronic warts", "Isolated otitis externa"], "P. falciparum can cause microvascular sequestration and multiorgan disease."),
        q("A traveler from a malaria-endemic area has fever, confusion, anemia and parasitemia. What is the emergency?", "Severe falciparum malaria", ["Uncomplicated influenza", "Tension headache", "Stable cystitis"], "CNS dysfunction with malaria is severe disease requiring urgent parenteral therapy.", True),
        q("Dengue classically presents with", "High fever, severe myalgia, headache and thrombocytopenia", ["Chronic cough for months", "Painless jaundice only", "Hemarthrosis from factor VIII deficiency"], "Dengue often causes fever, retro-orbital pain, myalgia, rash and low platelets."),
        q("Which finding warns of severe dengue?", "Abdominal pain, mucosal bleeding, lethargy or plasma leakage", ["Improving appetite only", "Normal hematocrit with no symptoms", "Isolated sneezing"], "Warning signs identify risk for shock and hemorrhage."),
        q("A dengue patient on day 5 has falling platelets, rising hematocrit and abdominal pain. Best interpretation?", "Plasma leakage with risk of severe dengue", ["Recovery without monitoring", "Bacterial meningitis", "Iron deficiency only"], "Rising hematocrit during defervescence suggests capillary leak.", True),
        q("Leptospirosis exposure is classically associated with", "Water contaminated by animal urine", ["Raw eggs only", "Airborne droplet nuclei", "Cat scratch only"], "Leptospira spreads through urine-contaminated water entering skin or mucosa."),
        q("Weil disease refers to severe leptospirosis with", "Jaundice, renal failure and hemorrhage", ["Only rash", "Only arthritis", "Only sore throat"], "Severe leptospirosis can cause hepatic, renal and bleeding complications."),
        q("A farmer has fever, calf tenderness, conjunctival suffusion, jaundice and renal injury after floodwater exposure. Diagnosis?", "Leptospirosis", ["Dengue only", "Typhoid only", "Rabies"], "Floodwater exposure plus conjunctival suffusion, myalgia, jaundice and AKI suggests leptospirosis.", True),
        q("Rabies post-exposure prophylaxis after a high-risk bite includes", "Wound washing, vaccine and rabies immunoglobulin when indicated", ["Antipyretics only", "Delayed vaccine after symptoms", "Oral antibiotics alone"], "Rabies is almost universally fatal after symptoms, so PEP is urgent.", True),
    ]),
    ("Healthcare-Associated and Device-Related Infections", [
        q("Healthcare-associated infections are important because they", "Increase morbidity, mortality, length of stay and antimicrobial resistance", ["Only affect outpatients", "Never involve devices", "Do not require prevention"], "HAIs are major preventable causes of harm."),
        q("Central line-associated bloodstream infection prevention includes", "Maximal barrier precautions and chlorhexidine skin antisepsis during insertion", ["Touching the site repeatedly", "Skipping hand hygiene", "Using nonsterile gloves"], "Insertion bundles reduce catheter-related bloodstream infections."),
        q("A patient with a central venous catheter develops fever and blood cultures grow Staphylococcus aureus. Best next step includes", "Evaluate for catheter-related bloodstream infection and remove catheter when indicated", ["Ignore culture as contamination always", "Treat with oral vitamins", "No repeat cultures"], "S. aureus bacteremia with a line requires serious evaluation and often line removal.", True),
        q("Catheter-associated UTI prevention is best achieved by", "Avoiding unnecessary catheterization and removing catheters early", ["Routine antibiotics for every catheter", "Changing catheters hourly", "Ignoring closed drainage"], "Reducing catheter exposure is the most effective prevention."),
        q("Ventilator-associated pneumonia risk is reduced by", "Ventilator care bundles including head elevation and oral care", ["Supine positioning always", "Stopping suction forever", "Routine antifungals"], "Bundles reduce aspiration and colonization risks."),
        q("A ventilated ICU patient develops new infiltrate, purulent secretions and worsening oxygenation after 6 days. Likely infection?", "Ventilator-associated pneumonia", ["Community-acquired cystitis", "Simple rhinitis", "Tinea corporis"], "Pneumonia after more than 48 hours of ventilation suggests VAP.", True),
        q("Surgical site infection prevention includes", "Appropriate perioperative antibiotic prophylaxis timed before incision", ["Antibiotics started one week after surgery only", "No sterile technique", "Routine prolonged antibiotics for all clean wounds"], "Correct prophylaxis timing and sterile technique reduce SSI."),
        q("Multidrug-resistant organisms spread in hospitals mainly through", "Selection pressure and lapses in infection prevention practices", ["Sunlight exposure", "Normal saline infusion", "Blood group mismatch"], "Antibiotic pressure plus transmission drives MDRO problems."),
        q("A patient develops watery diarrhea after clindamycin with positive toxin test. Diagnosis?", "Clostridioides difficile infection", ["Cholera from seawater only", "Celiac disease proven", "Amoebic liver abscess"], "Antibiotic exposure followed by toxin-positive diarrhea suggests C. difficile.", True),
        q("Contact precautions are especially important for", "Patients with transmissible organisms such as C. difficile or certain MDROs", ["All healed fractures", "Migraine without infection", "Isolated hypertension"], "Contact precautions reduce spread by hands, surfaces and equipment.", True),
    ]),
    ("Emerging, Viral and Travel-Related Infections", [
        q("A travel history in fever should include destination, dates, exposures and", "Vaccines, prophylaxis, food-water intake and animal or insect contacts", ["Only hotel rating", "Only airline name", "Only passport number"], "Incubation periods and exposures narrow the differential."),
        q("Influenza is treated most effectively with antivirals when", "Started early in high-risk or severely ill patients", ["Started after one month in all patients", "Used only after bacterial culture", "Never used in severe disease"], "Neuraminidase inhibitors work best early and are useful in severe/high-risk cases."),
        q("A pregnant patient during influenza season has fever, myalgia and cough. Best management includes", "Prompt antiviral therapy if influenza is suspected", ["Avoid treatment because pregnancy excludes antivirals", "Wait for pneumonia", "Give antibiotics only"], "Pregnancy is high risk for influenza complications and warrants early treatment.", True),
        q("COVID-19 severe disease is associated with", "Viral pneumonia, hypoxemia, thrombosis and inflammatory complications", ["Only urinary symptoms", "Mandatory bacterial meningitis", "No lung involvement"], "SARS-CoV-2 can cause respiratory failure and systemic complications."),
        q("Post-exposure prophylaxis is most time-critical for", "Rabies and certain bloodborne or sexual exposures", ["Old healed scar", "Remote childhood measles", "Stable hypertension"], "Some infections can be prevented if prophylaxis is given promptly after exposure."),
        q("A healthcare worker has needlestick injury from an HIV-positive source. Best immediate action?", "Wash the site, report exposure and start HIV PEP promptly if indicated", ["Wait 6 months for symptoms", "Ignore if wound is small", "Use only topical antibiotic"], "HIV PEP is most effective when started quickly after significant exposure.", True),
        q("Which vaccine is live attenuated?", "Measles-mumps-rubella vaccine", ["Inactivated influenza injection", "Tetanus toxoid", "Hepatitis B recombinant vaccine"], "MMR is a live attenuated vaccine and has contraindications in severe immunosuppression and pregnancy."),
        q("Fever after return from tropics should always consider", "Malaria until excluded when exposure is plausible", ["Only allergic rhinitis", "Only migraine", "Only vitamin deficiency"], "Malaria can be rapidly fatal and must be ruled out in compatible travel fever."),
        q("A traveler returns from sub-Saharan Africa with fever 10 days later. Which test is urgent?", "Thick and thin blood smear or rapid malaria test", ["Colonoscopy first", "Skin biopsy only", "Audiometry"], "Malaria testing is urgent in febrile travelers from endemic regions.", True),
        q("Emerging infections become difficult to control when they combine", "Efficient transmission, susceptible populations and delayed recognition", ["No human contact", "No incubation period", "Perfect lifelong immunity"], "Outbreak potential depends on transmission, susceptibility and detection/control capacity.", True),
    ]),
]


def build_questions():
    questions = []
    for topic_order, (topic, rows) in enumerate(TOPICS, 1):
        if len(rows) != 10:
            raise ValueError(f"{topic} has {len(rows)} questions, expected 10")
        clinical_count = sum(1 for row in rows if "clinical" in row.get("tags", []))
        if clinical_count != 4:
            raise ValueError(f"{topic} has {clinical_count} clinical questions, expected 4")
        topic_slug = slugify(topic)
        for question_order, row in enumerate(rows, 1):
            questions.append({
                "id": f"medicine-infectious-diseases-{topic_slug}-{question_order:02d}",
                "subjectId": SUBJECT_ID,
                "subjectTitle": SUBJECT_TITLE,
                "chapterTitle": CHAPTER,
                "chapterOrder": CHAPTER_ORDER,
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": topic_order,
                "source": "ai",
                "sourcePdf": SOURCE_PDF,
                "imageUrls": [],
                **row,
            })
    return questions


def update(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    questions = build_questions()
    data["questions"] = [
        item for item in data.get("questions", [])
        if not (item.get("subjectId") == SUBJECT_ID and item.get("chapterTitle") == CHAPTER)
    ] + questions
    if len(questions) != 100:
        raise AssertionError(f"Expected 100 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 100:
        raise AssertionError("Duplicate infectious diseases question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 100 Infectious Diseases questions.")


if __name__ == "__main__":
    main()
