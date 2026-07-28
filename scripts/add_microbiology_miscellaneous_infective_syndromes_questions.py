import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Miscellaneous Infective Syndromes"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("ocular-ear-infections", "Ocular and Ear Infections", [
        q("A contact lens user develops painful keratitis with a ring infiltrate after exposure to contaminated lens solution. The most likely agent is:", "Acanthamoeba", ["Treponema pallidum", "Bordetella pertussis", "Clostridium tetani"], "Acanthamoeba keratitis is classically linked to contact lens use and contaminated water or lens solutions."),
        q("A neonate develops purulent conjunctivitis 2 days after birth. Gram-negative intracellular diplococci are seen. The likely cause is:", "Neisseria gonorrhoeae", ["Chlamydia trachomatis", "HSV-1", "Adenovirus"], "Gonococcal ophthalmia neonatorum presents early with severe purulent discharge and can threaten the cornea."),
        q("Neonatal conjunctivitis appearing 5-14 days after birth with intracellular inclusions is most suggestive of:", "Chlamydia trachomatis", ["Neisseria gonorrhoeae", "Pseudomonas aeruginosa", "Moraxella catarrhalis"], "Chlamydial ophthalmia neonatorum usually appears later than gonococcal disease and may accompany afebrile pneumonia."),
        q("Follicular conjunctivitis with preauricular lymphadenopathy during an outbreak in a hostel is most commonly caused by:", "Adenovirus", ["Candida albicans", "Mycobacterium leprae", "Plasmodium falciparum"], "Adenovirus causes epidemic keratoconjunctivitis and pharyngoconjunctival fever."),
        q("Dendritic corneal ulcer on fluorescein staining is characteristic of:", "Herpes simplex keratitis", ["Trachoma", "Toxoplasmosis", "Mucormycosis"], "HSV keratitis classically produces branching dendritic ulcers and may recur."),
        q("Chronic follicular conjunctivitis progressing to entropion, trichiasis, and corneal opacity is due to:", "Chlamydia trachomatis serovars A-C", ["Chlamydia trachomatis L1-L3", "Neisseria gonorrhoeae", "Aspergillus fumigatus"], "Trachoma is caused by ocular C. trachomatis A-C and can lead to scarring blindness."),
        q("Acute otitis media in a child after viral upper respiratory infection is most commonly caused by:", "Streptococcus pneumoniae", ["Vibrio cholerae", "Treponema pallidum", "Leishmania donovani"], "S. pneumoniae, H. influenzae, and Moraxella are major bacterial causes of acute otitis media."),
        q("Malignant otitis externa in an elderly diabetic patient is classically caused by:", "Pseudomonas aeruginosa", ["Staphylococcus saprophyticus", "Corynebacterium diphtheriae", "Cryptococcus neoformans"], "Pseudomonas can invade skull base tissues in diabetic or immunocompromised patients."),
        q("Otomycosis with black fungal debris in the external auditory canal most strongly suggests:", "Aspergillus niger", ["Candida auris only", "Histoplasma capsulatum", "Pneumocystis jirovecii"], "Aspergillus, especially A. niger, is a common cause of fungal otitis externa."),
        q("Post-traumatic endophthalmitis with rapidly progressive eye pain and loss of vision is often caused by:", "Bacillus cereus", ["Bacillus anthracis", "Mycoplasma pneumoniae", "Echinococcus granulosus"], "B. cereus is a virulent cause of post-traumatic endophthalmitis and requires urgent management."),
    ]),
    ("congenital-infections", "Congenital Infections", [
        q("A newborn has cataract, patent ductus arteriosus, and sensorineural deafness. The congenital infection is most likely:", "Congenital rubella", ["Congenital toxoplasmosis", "Neonatal tetanus", "Congenital varicella"], "The classic rubella triad is cataract, cardiac defect such as PDA, and deafness."),
        q("Periventricular calcifications, microcephaly, and sensorineural hearing loss in a neonate point to:", "Congenital cytomegalovirus infection", ["Congenital toxoplasmosis", "Congenital syphilis", "Zika virus only"], "CMV is the most common congenital viral infection and classically causes periventricular calcifications."),
        q("Hydrocephalus, chorioretinitis, and diffuse intracranial calcifications in a neonate suggest:", "Congenital toxoplasmosis", ["Congenital CMV", "Congenital rubella", "Neonatal gonorrhea"], "Congenital toxoplasmosis classically causes the triad of chorioretinitis, hydrocephalus, and intracranial calcification."),
        q("A neonate develops vesicular skin lesions, seizures, and hepatitis after maternal genital lesions around delivery. The likely agent is:", "Herpes simplex virus", ["Parvovirus B19", "Rubella virus", "Treponema pallidum"], "Neonatal HSV is usually acquired intrapartum and can cause skin-eye-mouth, CNS, or disseminated disease."),
        q("Limb hypoplasia, cicatricial skin scarring, and eye defects after maternal chickenpox early in pregnancy suggest:", "Congenital varicella syndrome", ["Congenital CMV", "Congenital syphilis", "Neonatal listeriosis"], "Maternal varicella in early pregnancy can cause fetal limb, skin, neurologic, and ocular defects."),
        q("Snuffles, hepatosplenomegaly, rash involving palms and soles, and later Hutchinson teeth are features of:", "Congenital syphilis", ["Congenital rubella", "Congenital toxoplasmosis", "Congenital candidiasis"], "Congenital syphilis has early systemic features and late dental, skeletal, and neurologic signs."),
        q("Severe fetal microcephaly and arthrogryposis during an outbreak transmitted by Aedes mosquitoes suggests:", "Congenital Zika virus infection", ["Congenital dengue", "Congenital rabies", "Congenital measles"], "Zika virus is associated with congenital microcephaly and neurologic malformations."),
        q("The best prevention of congenital rubella is:", "Immunizing susceptible women with rubella-containing vaccine before pregnancy", ["Giving live rubella vaccine during pregnancy", "Treating newborn with penicillin", "Avoiding all vaccines in adolescence"], "Rubella vaccination prevents congenital rubella, but live vaccine is contraindicated during pregnancy."),
        q("Parvovirus B19 infection in pregnancy can cause fetal hydrops mainly by infecting:", "Erythroid precursor cells", ["Neural crest cells", "Renal tubular cells", "Hepatocytes only"], "Parvovirus B19 targets erythroid precursors, causing severe fetal anemia and hydrops."),
        q("Screening pregnant women with non-treponemal tests helps prevent congenital disease due to:", "Treponema pallidum", ["Toxoplasma gondii", "Varicella-zoster virus", "Cytomegalovirus"], "Maternal syphilis is treatable, and antenatal screening plus penicillin prevents congenital syphilis."),
    ]),
    ("oncogenic-organisms", "Organisms with Oncogenic Potential", [
        q("Cervical carcinoma is most strongly associated with persistent infection by:", "High-risk human papillomavirus types 16 and 18", ["HPV types 6 and 11 only", "HSV-2", "Adenovirus 40"], "High-risk HPV, especially 16 and 18, drives cervical and other anogenital cancers."),
        q("HPV E6 oncoprotein promotes carcinogenesis primarily by inactivating:", "p53", ["Rb only", "BRCA1", "APC"], "HPV E6 promotes degradation of p53, impairing DNA damage response and apoptosis."),
        q("HPV E7 oncoprotein promotes cell-cycle progression by inactivating:", "Retinoblastoma protein", ["p53 only", "Beta-catenin", "BCR-ABL"], "E7 binds Rb, releasing E2F and pushing infected cells into S phase."),
        q("Kaposi sarcoma in an HIV-positive patient is caused by:", "Human herpesvirus 8", ["Human herpesvirus 6", "Epstein-Barr virus", "JC virus"], "HHV-8 is the etiologic agent of Kaposi sarcoma and some lymphoproliferative disorders."),
        q("Endemic Burkitt lymphoma with jaw mass is strongly linked to:", "Epstein-Barr virus", ["Hepatitis C virus", "HTLV-1", "BK virus"], "EBV is associated with Burkitt lymphoma, nasopharyngeal carcinoma, and some Hodgkin lymphomas."),
        q("Adult T-cell leukemia/lymphoma is associated with:", "HTLV-1", ["HTLV-2", "Hepatitis A virus", "Parvovirus B19"], "HTLV-1 is a retrovirus associated with adult T-cell leukemia/lymphoma and tropical spastic paraparesis."),
        q("Hepatocellular carcinoma is associated with chronic infection by:", "Hepatitis B and hepatitis C viruses", ["Rotavirus and norovirus", "Influenza and RSV", "Rhinovirus and adenovirus"], "Chronic HBV/HCV infection causes ongoing inflammation, cirrhosis, and malignant transformation."),
        q("Nasopharyngeal carcinoma is characteristically associated with:", "Epstein-Barr virus", ["Rabies virus", "Measles virus", "Enterovirus 71"], "EBV is strongly linked to nasopharyngeal carcinoma, especially in endemic regions."),
        q("Gastric MALT lymphoma can regress after eradication of:", "Helicobacter pylori", ["Mycoplasma pneumoniae", "Vibrio cholerae", "Bacillus cereus"], "Chronic H. pylori antigenic stimulation can drive MALT lymphoma, which may respond to eradication therapy."),
        q("The most effective primary prevention for HPV-associated cervical cancer is:", "Prophylactic HPV vaccination before exposure", ["Acyclovir after every sexual contact", "BCG at birth", "Ribavirin after Pap smear"], "HPV vaccination prevents infection with oncogenic HPV types and reduces cervical cancer risk."),
    ]),
    ("zoonotic-infections", "Zoonotic Infections: Plague, Tularemia and Bite Wound Infections", [
        q("Bubonic plague with painful lymphadenitis after flea exposure is caused by:", "Yersinia pestis", ["Francisella tularensis", "Pasteurella multocida", "Bartonella henselae"], "Y. pestis is transmitted from rodents by fleas and causes buboes, septicemia, or pneumonia."),
        q("Yersinia pestis classically shows which staining pattern?", "Bipolar safety-pin appearance", ["Acid-fast branching filaments", "Terminal drumstick spores", "India ink capsule"], "Y. pestis can show bipolar staining, producing a safety-pin appearance."),
        q("Pneumonic plague is especially dangerous because it:", "Can spread person-to-person by respiratory droplets", ["Requires snail intermediate host", "Never causes sepsis", "Only infects skin"], "Pneumonic plague is highly contagious and rapidly fatal without prompt treatment."),
        q("Ulceroglandular disease after handling rabbits or tick exposure suggests:", "Tularemia", ["Brucellosis", "Leptospirosis", "Q fever"], "Francisella tularensis causes tularemia, classically ulceroglandular illness after rabbit/tick exposure."),
        q("Francisella tularensis is notable because it is:", "Highly infectious and requires biosafety caution in the laboratory", ["A common gut commensal", "An obligate helminth", "A nonpathogenic yeast"], "Tularemia has a very low infectious dose and poses laboratory-acquired infection risk."),
        q("A rapidly developing cellulitis after a cat bite is most commonly due to:", "Pasteurella multocida", ["Clostridioides difficile", "Vibrio cholerae", "Mycobacterium tuberculosis"], "Pasteurella from cat/dog oral flora causes rapidly progressive bite wound infection."),
        q("Painless papule followed by regional lymphadenopathy after a kitten scratch suggests:", "Bartonella henselae", ["Yersinia pestis", "Bacillus anthracis", "Corynebacterium ulcerans"], "Cat-scratch disease is caused by Bartonella henselae and presents with regional lymphadenitis."),
        q("Human bite wounds are especially concerning for infection by:", "Eikenella corrodens with mixed anaerobes", ["Schistosoma haematobium", "Naegleria fowleri", "Enterobius vermicularis"], "Human oral flora includes Eikenella and anaerobes; clenched-fist injuries are high risk."),
        q("A dog bite patient with fever, hypotension, and disseminated intravascular coagulation after splenectomy should raise suspicion for:", "Capnocytophaga canimorsus", ["Coxiella burnetii", "Rickettsia prowazekii", "Toxocara canis"], "Capnocytophaga canimorsus can cause fulminant sepsis after dog bites, especially in asplenic patients."),
        q("Rabies prophylaxis after a high-risk animal bite is urgent because:", "Once symptomatic rabies develops, it is almost always fatal", ["Rabies causes only mild fever", "Vaccine works only after symptoms appear", "The virus remains only in skin"], "Post-exposure prophylaxis with wound care, vaccine, and immunoglobulin when indicated prevents fatal CNS disease."),
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
            questions.append({**BASE, "id": f"micro-misc-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "microbiology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 4 or len(questions) != 40:
        raise AssertionError(f"Expected 4 topics and 40 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 40:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
