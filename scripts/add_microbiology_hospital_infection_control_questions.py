import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Hospital Infection Control"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("healthcare-associated-infections", "Healthcare-associated Infections", [
        q("A patient develops pneumonia 72 hours after admission, with no respiratory symptoms at entry. This is best classified as:", "Healthcare-associated infection", ["Community-acquired infection", "Congenital infection", "Latent colonization only"], "HAIs are infections acquired during healthcare exposure, typically not present or incubating at admission."),
        q("A central line patient develops fever and blood cultures grow coagulase-negative staphylococci from line and peripheral samples. The most likely pathogenesis is:", "Biofilm formation on catheter surface", ["Airborne spread from ward dust", "Food-borne intoxication", "Vector-borne transmission"], "Intravascular devices allow skin organisms to adhere and form biofilms."),
        q("The single most important routine measure to prevent cross-transmission in hospital is:", "Hand hygiene", ["Daily fumigation", "Universal antibiotic prophylaxis", "Routine blood cultures"], "Hand hygiene interrupts transmission from patient-to-patient and environment-to-patient."),
        q("Alcohol hand rub is less reliable when hands are visibly soiled because:", "Organic material reduces effectiveness and mechanical washing is needed", ["Alcohol cannot kill any enveloped virus", "Soap sterilizes hands", "Gloves replace washing forever"], "Visible dirt or body fluids require soap-and-water cleaning."),
        q("A patient colonized with MRSA is placed under contact precautions. The key added practice is:", "Gloves and gown for patient/environment contact", ["N95 respirator for every entry only", "No hand hygiene if gloves used", "Negative pressure room mandatory"], "Contact precautions reduce spread via hands, clothes, and contaminated surfaces."),
        q("A patient with measles in the emergency room requires:", "Airborne precautions with negative-pressure isolation if available", ["Only standard precautions", "Droplet precautions without respirator", "No isolation after rash"], "Measles spreads by airborne droplet nuclei and needs airborne precautions."),
        q("A patient with influenza should be managed mainly with:", "Droplet precautions plus standard precautions", ["Airborne precautions for all routine care only", "Contact precautions alone", "No mask for close contact"], "Influenza spreads primarily by respiratory droplets during close contact."),
        q("A ventilated ICU patient develops pneumonia. Which preventive bundle element is most relevant?", "Head-end elevation and daily sedation/ventilation assessment", ["Routine broad-spectrum antibiotics for all ventilated patients", "Avoid oral care", "Keep patient supine"], "VAP bundles reduce aspiration and device duration."),
        q("A postoperative wound infection cluster is traced to poor instrument reprocessing. This represents failure in:", "Break in asepsis/sterilization chain", ["Natural flora only", "Endogenous immunity", "Vaccine cold chain"], "HAIs can arise from breaches in sterile technique and equipment processing."),
        q("Surveillance of HAIs is useful because it:", "Detects trends, outbreaks, and targets prevention measures", ["Replaces clinical diagnosis", "Eliminates need for hand hygiene", "Proves all fever is HAI"], "Systematic surveillance guides infection control action and audit."),
    ]),
    ("major-hai-types", "Major Healthcare-associated Infection Types", [
        q("A catheterized patient develops fever, suprapubic tenderness, pyuria, and urine culture growth. The major modifiable risk factor is:", "Duration of urinary catheterization", ["Patient hair color", "Room lighting", "Use of sterile gloves after removal"], "CAUTI risk rises with catheter duration; remove catheters early."),
        q("Best prevention of catheter-associated UTI is:", "Avoid unnecessary catheterization and remove early", ["Daily antibiotic irrigation", "Routine catheter change every hour", "Keeping bag above bladder"], "Appropriate indication, aseptic insertion, closed drainage, and early removal prevent CAUTI."),
        q("A central line bloodstream infection prevention bundle includes:", "Maximal sterile barrier precautions and chlorhexidine skin antisepsis", ["No hand hygiene if sterile gloves used", "Femoral site preference in adults", "Routine line access without scrubbing hub"], "CLABSI prevention requires sterile insertion, skin prep, hub care, and line necessity review."),
        q("A ventilator-associated pneumonia prevention step that reduces aspiration risk is:", "Elevating head of bed", ["Keeping cuff deflated", "Routine saline instillation", "Avoiding oral hygiene"], "Head elevation lowers aspiration of contaminated secretions."),
        q("A surgical site infection develops after colon surgery. Correct prophylaxis principle is:", "Give appropriate antibiotic within recommended time before incision", ["Start antibiotics 3 days after surgery", "Continue prophylaxis for weeks in all cases", "Use vancomycin for every patient"], "Surgical prophylaxis must achieve tissue levels at incision and is usually short."),
        q("A neonate in ICU develops sepsis after multiple line manipulations. The most likely source is:", "Device-associated bloodstream infection", ["Vector-borne infection", "Congenital rubella", "Food poisoning"], "Central venous access is a major neonatal HAI risk."),
        q("A burn patient develops Pseudomonas wound infection. A key reason burns are high risk is:", "Loss of skin barrier and moist nutrient-rich wound surface", ["Excess antibody production", "Absence of hospital exposure", "Sterile wound colonization"], "Burns remove mechanical barriers and support colonization/invasion."),
        q("A patient on broad-spectrum antibiotics develops watery diarrhea and pseudomembranes. The HAI type is:", "Clostridioides difficile infection", ["Ventilator pneumonia", "Catheter bacteriuria", "Surgical site cellulitis only"], "Antibiotic disruption of gut microbiota permits toxigenic C. difficile overgrowth."),
        q("A hospital wants to reduce SSI after orthopedic implants. Which measure is most direct?", "Strict asepsis, appropriate prophylaxis, and operating room discipline", ["Routine postoperative antibiotics until suture removal", "No skin preparation", "Reuse unsterilized implants"], "Implant SSIs are hard to eradicate; prevention is crucial."),
        q("Device-associated infections are difficult to cure without removal because microbes often:", "Form biofilms with reduced antimicrobial susceptibility", ["Become viruses", "Lose all adhesins", "Stop producing matrix"], "Biofilms protect organisms from antibiotics and host immunity."),
    ]),
    ("sterilization-disinfection", "Sterilization and Disinfection", [
        q("Surgical instruments that enter sterile tissue are Spaulding critical items and require:", "Sterilization", ["Low-level disinfection", "Cleaning only", "Air drying only"], "Critical items must be free of all microbial life including spores."),
        q("Autoclaving kills spores by:", "Saturated steam under pressure causing protein denaturation", ["Dry heat oxidation only", "Freezing water", "Ultraviolet shadowing"], "Steam sterilization is reliable for heat-stable instruments."),
        q("Hot air oven sterilizes glassware mainly by:", "Dry heat oxidation", ["Moist heat coagulation", "Filtration", "Ionizing radiation only"], "Dry heat requires higher temperatures/longer times than autoclaving."),
        q("Heat-labile serum is sterilized best by:", "Membrane filtration", ["Autoclaving", "Incineration", "Boiling for 5 minutes"], "Filtration removes microorganisms from heat-sensitive fluids without heat exposure."),
        q("Endoscopes are semicritical devices and usually require:", "High-level disinfection", ["Low-level disinfection only", "No reprocessing", "Dry sweeping"], "Semicritical items contact mucosa and require high-level disinfection if sterilization is impractical."),
        q("Glutaraldehyde is used for high-level disinfection because it:", "Alkylates microbial proteins and nucleic acids", ["Works only as detergent", "Requires visible dirt", "Cannot kill mycobacteria"], "Glutaraldehyde can disinfect heat-sensitive equipment but needs proper contact time and ventilation."),
        q("A chemical indicator tape on an autoclave pack changes color. This proves:", "The pack was exposed to process conditions, not necessarily sterility", ["All spores are killed inside", "Biological monitoring is unnecessary", "The load was dry"], "Chemical indicators show exposure; biological indicators best verify sterilization efficacy."),
        q("Biological monitoring of steam sterilization commonly uses spores of:", "Geobacillus stearothermophilus", ["Clostridium tetani", "Bacillus anthracis clinical strain", "Staphylococcus aureus"], "Resistant spores are used to validate autoclave performance."),
        q("Alcohol is not ideal for sterilizing surgical instruments because it:", "Does not reliably kill bacterial spores", ["Cannot kill enveloped viruses", "Has no protein denaturing action", "Works only at 5%"], "Alcohols are intermediate-level disinfectants but not sterilants."),
        q("Cleaning before disinfection is essential because organic matter can:", "Shield microbes and inactivate disinfectants", ["Improve disinfectant penetration always", "Sterilize instruments", "Replace contact time"], "Physical cleaning removes bioburden and improves disinfection/sterilization efficacy."),
    ]),
    ("biomedical-waste-management", "Biomedical Waste Management", [
        q("Used blood-soaked gauze from a procedure should be handled as:", "Biomedical waste requiring segregation at source", ["General office waste", "Food waste", "Recyclable clean paper"], "Infectious contaminated waste must be segregated immediately in the correct stream."),
        q("The most important first step in biomedical waste management is:", "Segregation at point of generation", ["Transport before segregation", "Mixing all waste", "Storing waste indefinitely"], "Correct source segregation prevents injury, infection, and costly downstream errors."),
        q("Used needles should be discarded immediately into:", "Puncture-proof sharps container", ["Open plastic bag", "Patient bedside tray", "Paper envelope"], "Sharps containers prevent needle-stick injury and allow safe disposal."),
        q("Recapping needles after injection is discouraged because it:", "Increases needle-stick injury risk", ["Sterilizes the needle", "Prevents all blood exposure", "Is required before disposal"], "Avoid recapping; dispose directly into sharps container."),
        q("An overfilled sharps container is unsafe because:", "Sharps may protrude and injure handlers", ["It becomes sterile", "It reduces infection risk", "It neutralizes blood"], "Sharps containers should be closed/replaced before overfilling."),
        q("Liquid infectious waste such as blood/body fluid requires:", "Appropriate chemical disinfection before safe disposal as per protocol", ["Direct disposal into public area", "Storage on ward for weeks", "Mixing with food waste"], "Liquid biomedical waste is disinfected according to local BMW rules before discharge."),
        q("Microbiology culture plates with pathogens should be:", "Autoclaved or treated before final disposal", ["Thrown untreated in general waste", "Washed in hand basin", "Stored indefinitely"], "Cultures have high bioburden and require sterilization/disinfection before disposal."),
        q("Color coding in biomedical waste management is used to:", "Link waste category with correct treatment and disposal route", ["Make bins decorative", "Replace staff training", "Avoid segregation"], "Color-coded segregation standardizes safe handling and treatment."),
        q("A healthcare worker mixes infectious waste with municipal waste. The consequence is:", "Expanded exposure risk and failure of safe waste treatment chain", ["Lower treatment cost safely", "Automatic sterilization", "Improved recycling"], "Mixing infectious waste contaminates the entire stream."),
        q("Biomedical waste records and barcoding are useful because they:", "Enable tracking, accountability, and regulatory compliance", ["Prove waste is sterile", "Replace disinfection", "Prevent all injuries alone"], "Documentation supports safe disposal and audit trails."),
    ]),
    ("needle-stick-injury", "Needle Stick Injury", [
        q("Immediately after a needle-stick injury, the correct first aid is:", "Wash the site with soap and water without squeezing aggressively", ["Apply bleach into wound", "Ignore if no bleeding", "Suture immediately", "Suck the wound"], "First aid reduces contamination; harsh chemicals and squeezing are not recommended."),
        q("After a needle-stick injury from an HIV-positive source, PEP is most effective when:", "Started as soon as possible, ideally within hours", ["Delayed until symptoms appear", "Started after 6 months", "Given only if fever develops"], "HIV PEP should be initiated urgently after risk assessment."),
        q("The usual duration of HIV post-exposure prophylaxis is:", "28 days", ["1 day", "7 days", "6 months"], "A 28-day antiretroviral PEP course is standard when indicated."),
        q("A vaccinated healthcare worker has anti-HBs 120 mIU/mL after exposure to HBsAg-positive blood. The best interpretation is:", "Protective immunity is present", ["No protection", "Immediate HBIG always required", "Vaccine failure"], "Anti-HBs at or above 10 mIU/mL is generally considered protective."),
        q("If an exposed worker is unvaccinated and source is HBsAg positive, management includes:", "HBIG plus hepatitis B vaccination", ["Only tetanus toxoid", "No action", "Hepatitis A vaccine only"], "HBV exposure prophylaxis depends on vaccination/antibody status and source status."),
        q("HCV exposure after needle-stick is managed primarily by:", "Baseline and follow-up testing because no proven PEP exists", ["Immediate HCV vaccine", "HBIG", "Oseltamivir"], "There is no established HCV PEP; early detection and referral are important."),
        q("Risk of HIV transmission after percutaneous exposure is increased by:", "Deep injury with hollow-bore needle visibly contaminated with blood", ["Superficial scratch from unused needle", "Contact with intact skin", "Exposure to sterile saline"], "Large inoculum, deep injury, and hollow-bore blood-filled needles increase risk."),
        q("Needle-stick reporting is important because it:", "Triggers risk assessment, PEP, testing, and prevention review", ["Punishes the worker", "Replaces first aid", "Prevents seroconversion without PEP"], "Prompt reporting protects the worker and improves safety systems."),
        q("A major preventive engineering control for needle-stick injury is:", "Safety-engineered needle devices", ["Recapping two-handed", "Manual needle bending", "Leaving sharps on tray"], "Safety devices reduce percutaneous injuries when used properly."),
        q("Post-exposure counseling should include:", "Drug adherence, side effects, follow-up testing, and precautions to prevent secondary transmission", ["Avoid all testing", "Stop work forever", "Donate blood to check status"], "Counseling supports safe completion of PEP and appropriate follow-up."),
    ]),
    ("antimicrobial-stewardship", "Antimicrobial Stewardship", [
        q("A patient with viral upper respiratory infection demands antibiotics. Stewardship recommends:", "No antibiotic and clear counseling on viral illness", ["Broad-spectrum carbapenem", "Dual antibiotics", "Long prophylaxis"], "Avoiding unnecessary antibiotics reduces resistance and adverse effects."),
        q("The core goal of antimicrobial stewardship is:", "Optimize clinical outcome while minimizing resistance, toxicity, and cost", ["Stop all antibiotics", "Use newest antibiotic always", "Avoid cultures"], "Stewardship improves appropriate drug, dose, route, and duration."),
        q("De-escalation after culture results means:", "Narrowing therapy to the most appropriate targeted agent", ["Adding more antibiotics despite susceptibility", "Stopping source control", "Ignoring cultures"], "Culture-guided narrowing reduces collateral damage."),
        q("An antibiotic time-out at 48-72 hours is used to:", "Reassess diagnosis, cultures, route, dose, and duration", ["Automatically continue all antibiotics", "Avoid documentation", "Delay therapy in sepsis"], "Time-outs are structured reviews of ongoing antimicrobial need."),
        q("Using a hospital antibiogram helps clinicians choose:", "Empiric therapy based on local susceptibility patterns", ["A universal drug for all infections", "Only antifungals", "No treatment"], "Local resistance patterns guide empiric antibiotic selection."),
        q("A positive urine culture in an asymptomatic catheterized patient should not automatically be treated because:", "Asymptomatic bacteriuria often represents colonization and treatment selects resistance", ["Urine cultures are always false", "Catheters prevent infection", "Antibiotics have no adverse effects"], "Treatment is reserved for specific groups and symptomatic infection."),
        q("Surgical prophylaxis should usually be:", "Appropriate agent timed before incision and discontinued promptly", ["Started after wound infection appears", "Continued for weeks in all clean surgeries", "Broadest possible drug for everyone"], "Correct timing and short duration prevent SSI while limiting harm."),
        q("Reserve antibiotics are protected because overuse can:", "Select multidrug-resistant organisms and remove last-line options", ["Improve sensitivity forever", "Prevent all C. difficile", "Sterilize microbiota safely"], "Restricting last-line agents preserves effectiveness."),
        q("Dose optimization in stewardship includes renal adjustment because:", "Underdosing risks failure and overdosing risks toxicity", ["Renal function never matters", "All antibiotics have same dose", "Dose does not affect resistance"], "PK/PD and patient factors are central to stewardship."),
        q("A stewardship audit finds prolonged double anaerobic coverage. The correct action is:", "Stop redundant therapy when not clinically justified", ["Continue because duplication is always better", "Add antifungal", "Avoid reviewing charts"], "Duplicate coverage increases toxicity and microbiome disruption without benefit."),
    ]),
    ("environmental-surveillance", "Environmental Surveillance (Bacteriology of Water, Air and Surface)", [
        q("Routine microbiological surveillance of operation theatre air is mainly used to:", "Assess environmental contamination trends and infection control breaches", ["Diagnose each patient's infection", "Replace hand hygiene", "Prove sterility of all staff"], "Environmental surveillance supports quality assurance and outbreak investigation."),
        q("Settle plate method for air sampling measures:", "Viable particles settling by gravity", ["All airborne viruses quantitatively", "Endotoxin only", "Chemical disinfectant level"], "Settle plates are passive and semi-quantitative, affected by airflow and time."),
        q("Active air sampling is better than settle plates when:", "A measured volume of air must be sampled", ["No equipment is available", "Only surface contamination matters", "Water potability is tested"], "Active samplers pull known air volumes, enabling quantitative counts."),
        q("A hospital water sample is tested for coliforms because coliforms indicate:", "Fecal contamination or failure of water safety", ["Sterility", "High chlorine always", "Absence of pathogens always"], "Coliforms are indicator organisms for water quality."),
        q("Residual chlorine in water is monitored because it indicates:", "Continuing disinfectant activity", ["Bacterial species identity", "Viral load", "Endotoxin concentration"], "Residual chlorine helps ensure ongoing protection against microbial contamination."),
        q("Surface swabbing in ICU is most useful when:", "Investigating contamination of high-touch surfaces or outbreak sources", ["Replacing patient cultures", "Diagnosing malaria", "Measuring hemoglobin"], "Surface surveillance targets cleaning efficacy and outbreak reservoirs."),
        q("A high-touch surface repeatedly grows Acinetobacter during an ICU outbreak. The control implication is:", "Improve cleaning/disinfection and hand/environmental practices", ["Ignore because environment never transmits", "Stop all patient cultures", "Use only air sampling"], "Environmental reservoirs can sustain healthcare-associated transmission."),
        q("Water outlets in high-risk units are monitored for Pseudomonas because it:", "Thrives in moist environments and can infect vulnerable patients", ["Requires dry dust only", "Cannot form biofilm", "Is killed by all tap water"], "Pseudomonas survives in wet reservoirs and biofilms."),
        q("Air sampling immediately after fumigation that shows no growth does not alone prove long-term safety because:", "Environmental contamination can recur with use and traffic", ["No organism can grow later", "Fumigation replaces cleaning forever", "Patients cannot introduce microbes"], "Surveillance results are time-bound and must be interpreted with practices and traffic."),
        q("Environmental surveillance data are most useful when combined with:", "Epidemiologic linkage to cases and infection control audit", ["Astrology", "Patient blood group only", "Antibiotic color"], "Environmental cultures need clinical correlation to guide action."),
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
            questions.append({**BASE, "id": f"micro-hic-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "microbiology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 7 or len(questions) != 70:
        raise AssertionError(f"Expected 7 topics and 70 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 70:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
