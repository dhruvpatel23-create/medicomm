import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Urogenital Tract Infections"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("urinary-tract-syndromes", "Infective Syndromes of Urinary Tract", [
        q("A young woman has dysuria, urinary frequency, suprapubic pain, and no fever or flank tenderness. The most likely syndrome is:", "Acute uncomplicated cystitis", ["Acute pyelonephritis", "Urethral chancre", "Bacterial vaginosis"], "Lower UTI presents with irritative voiding symptoms without systemic features or renal angle tenderness."),
        q("Fever, chills, flank pain, costovertebral angle tenderness, and pyuria in a woman with bacteriuria suggest:", "Acute pyelonephritis", ["Simple cystitis only", "Vulvovaginal candidiasis", "Primary syphilis"], "Systemic symptoms with flank tenderness indicate upper urinary tract involvement."),
        q("The most common cause of community-acquired uncomplicated UTI is:", "Uropathogenic Escherichia coli", ["Neisseria gonorrhoeae", "Treponema pallidum", "Candida albicans only"], "Uropathogenic E. coli is the leading cause of uncomplicated cystitis and pyelonephritis."),
        q("A nitrite-positive urine dipstick supports infection by:", "Enterobacteriaceae that reduce nitrate to nitrite", ["Enterococcus alone", "Candida alone", "Schistosoma eggs"], "Many Gram-negative uropathogens such as E. coli convert nitrate to nitrite; Enterococcus often does not."),
        q("A catheterized ICU patient develops fever, pyuria, and urine culture with Pseudomonas aeruginosa. The major risk factor is:", "Indwelling urinary catheter with biofilm formation", ["Unprotected sexual exposure only", "Mosquito bite", "Eating undercooked pork"], "Catheters bypass host defenses and permit biofilm-associated nosocomial UTI."),
        q("Recurrent UTI in a sexually active young woman is commonly related to:", "Ascending periurethral colonization after intercourse", ["Hematogenous spread from lung", "Dog bite inoculation", "Transplacental spread"], "Most UTIs are ascending infections from periurethral flora; intercourse is a common trigger."),
        q("Enterococcus faecalis UTI is important clinically because it is characteristically:", "Intrinsically resistant to cephalosporins", ["Always nitrite-positive", "Acid-fast", "A strict intracellular parasite"], "Enterococci are common healthcare-associated uropathogens and are intrinsically cephalosporin resistant."),
        q("Terminal hematuria with urinary schistosomiasis is caused by eggs of:", "Schistosoma haematobium", ["Schistosoma mansoni", "Taenia solium", "Enterobius vermicularis"], "S. haematobium adults inhabit vesical venous plexus and eggs damage the urinary bladder."),
        q("A renal transplant recipient with ureteric stenosis, hemorrhagic cystitis, and decoy cells in urine should be evaluated for:", "BK polyomavirus infection", ["Rabies", "Poliovirus", "Dengue"], "BK virus reactivation in immunosuppressed renal transplant patients can cause nephropathy and urinary tract disease."),
        q("The best specimen for routine diagnosis of uncomplicated bacterial UTI in an adult woman is:", "Clean-catch midstream urine before antibiotics", ["Saliva", "Vaginal swab only", "Stool microscopy"], "Midstream urine minimizes contamination and should be collected before antimicrobial therapy when culture is needed."),
    ]),
    ("genital-tract-sti-syndromes", "Infective Syndromes of Genital Tract and Sexually-transmitted Infections", [
        q("A painless indurated genital ulcer with non-tender regional lymphadenopathy most strongly suggests:", "Primary syphilis", ["Chancroid", "Genital herpes", "Trichomoniasis"], "Primary syphilis classically causes a painless hard chancre with regional lymphadenopathy."),
        q("Painful genital ulcers with tender suppurative inguinal lymphadenitis are typical of:", "Chancroid due to Haemophilus ducreyi", ["Primary syphilis", "Donovanosis", "Bacterial vaginosis"], "Chancroid produces soft painful ulcers and painful buboes."),
        q("A beefy-red painless genital ulcer that bleeds easily and shows Donovan bodies on tissue smear is:", "Granuloma inguinale", ["Lymphogranuloma venereum", "Gonorrhea", "Vaginal candidiasis"], "Granuloma inguinale due to Klebsiella granulomatis shows intracellular Donovan bodies."),
        q("A transient genital ulcer followed by painful inguinal lymphadenopathy and proctocolitis is most consistent with:", "Lymphogranuloma venereum caused by Chlamydia trachomatis L1-L3", ["HSV-1 reactivation only", "Candida vaginitis", "Schistosomiasis"], "LGV begins with a small lesion and progresses to invasive lymphatic disease."),
        q("Clusters of painful recurrent vesicles and shallow ulcers on the genitalia are most often due to:", "Herpes simplex virus", ["Treponema pallidum", "Haemophilus ducreyi", "Gardnerella vaginalis"], "Genital herpes causes painful vesicles/ulcers and recurrence due to latency."),
        q("A man has purulent urethral discharge; Gram stain shows intracellular kidney-shaped Gram-negative diplococci. The organism is:", "Neisseria gonorrhoeae", ["Chlamydia trachomatis", "Treponema pallidum", "Candida albicans"], "Gonococci are Gram-negative diplococci classically seen inside neutrophils in male urethral discharge."),
        q("Non-gonococcal urethritis with scant mucoid discharge is most commonly caused by:", "Chlamydia trachomatis", ["Clostridium tetani", "Schistosoma haematobium", "BK virus"], "C. trachomatis is the leading cause of non-gonococcal urethritis."),
        q("Frothy yellow-green vaginal discharge with strawberry cervix points to:", "Trichomonas vaginalis", ["Candida albicans", "Gardnerella vaginalis", "Treponema pallidum"], "Trichomoniasis causes frothy discharge, pruritus, and punctate cervical hemorrhages."),
        q("Thin homogeneous fishy-smelling vaginal discharge with clue cells is diagnostic of:", "Bacterial vaginosis", ["Vulvovaginal candidiasis", "Gonococcal urethritis", "Chancroid"], "Bacterial vaginosis is associated with clue cells, elevated pH, and amine odor."),
        q("Thick curdy vaginal discharge with intense pruritus and budding yeast/pseudohyphae on microscopy suggests:", "Vulvovaginal candidiasis", ["Trichomoniasis", "Primary syphilis", "Lymphogranuloma venereum"], "Candida vaginitis causes pruritus and curdy discharge; microscopy may show budding yeast and pseudohyphae."),
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
            questions.append({**BASE, "id": f"micro-urogenital-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "microbiology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 2 or len(questions) != 20:
        raise AssertionError(f"Expected 2 topics and 20 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 20:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
