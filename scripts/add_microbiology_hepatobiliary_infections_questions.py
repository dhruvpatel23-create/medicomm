import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Hepatobiliary System Infections"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("hepatobiliary-abdomen-syndromes", "Infective Syndromes of Hepatobiliary System and Abdomen", [
        q("A patient has fever, right upper quadrant pain, and jaundice. This Charcot triad most strongly suggests:", "Acute cholangitis", ["Acute viral gastroenteritis", "Uncomplicated cystitis", "Tetanus"], "Charcot triad indicates infected obstructed biliary tree and needs urgent antibiotics plus biliary drainage when severe."),
        q("A patient with cholangitis becomes hypotensive and confused. This expanded presentation is:", "Reynolds pentad", ["Murphy sign", "Courvoisier sign", "Kehr sign"], "Reynolds pentad is Charcot triad plus shock and altered mental status, suggesting severe suppurative cholangitis."),
        q("Acute cholecystitis is usually initiated by:", "Cystic duct obstruction by gallstone", ["Portal venous thrombosis only", "Hepatitis B replication", "Splenic rupture"], "Gallstone obstruction causes inflammation; secondary bacterial infection may complicate the process."),
        q("Common bacteria in ascending cholangitis are typically:", "Enteric Gram-negative rods and anaerobes", ["Dermatophytes", "Mycobacterium leprae", "Respiratory viruses only"], "Biliary infections often involve gut flora such as E. coli, Klebsiella, Enterococcus, and anaerobes."),
        q("A patient develops fever and diffuse abdominal pain after bowel perforation. The main microbiology concern is:", "Polymicrobial peritonitis with aerobic and anaerobic gut flora", ["Pure viral hepatitis", "Only pinworm", "Single dermatophyte infection"], "Secondary peritonitis from perforation is typically polymicrobial."),
        q("Spontaneous bacterial peritonitis in cirrhosis is diagnosed when ascitic fluid shows:", "Neutrophil count at or above 250 cells/µL", ["Only eosinophilia", "No cells but high glucose", "Acid-fast bacilli always"], "Ascitic PMN count >=250 cells/µL supports SBP and warrants empiric antibiotics."),
        q("The most common source of pyogenic liver abscess is:", "Biliary tract infection or portal spread from abdomen", ["Airborne droplet infection", "Skin dermatophyte spread", "Mosquito inoculation"], "Pyogenic abscesses often arise from biliary sepsis or intra-abdominal infection."),
        q("A liver abscess aspirate grows mixed E. coli and Bacteroides. This supports:", "Pyogenic liver abscess", ["Amebic liver abscess only", "Hydatid cyst", "Viral hepatitis"], "Polymicrobial enteric flora suggests pyogenic rather than amebic etiology."),
        q("Empiric treatment of severe intra-abdominal sepsis must cover:", "Gram-negative enteric bacilli and anaerobes", ["Only atypical pneumonia organisms", "Only viruses", "Only dermatophytes"], "Intra-abdominal infections need coverage for Enterobacteriaceae and anaerobes such as Bacteroides."),
        q("Source control in intra-abdominal infection means:", "Drainage, debridement, or correction of the infected focus", ["Giving antipyretic only", "Avoiding imaging", "Stopping all antibiotics immediately"], "Antibiotics alone may fail if pus, obstruction, perforation, or necrotic tissue remains."),
    ]),
    ("hepatitis-viruses-yellow-fever", "Viruses Causing Hepatitis: Hepatitis Viruses, Yellow Fever and Others", [
        q("A patient has acute hepatitis after contaminated water exposure. Which virus is classically fecal-orally transmitted and does not cause chronic infection?", "Hepatitis A virus", ["Hepatitis C virus", "Hepatitis D virus", "Hepatitis B virus"], "HAV spreads fecal-orally and causes acute self-limited hepatitis."),
        q("A pregnant woman in the third trimester develops fulminant hepatitis after waterborne outbreak. The virus of special concern is:", "Hepatitis E virus", ["Hepatitis A virus", "Epstein-Barr virus", "Cytomegalovirus"], "HEV can cause severe disease and high mortality in pregnancy."),
        q("HBsAg positive for more than 6 months indicates:", "Chronic hepatitis B infection", ["Resolved infection only", "Successful vaccination", "Window period only"], "Persistence of HBsAg beyond 6 months defines chronic HBV infection."),
        q("During the hepatitis B window period, the most useful serologic marker is:", "Anti-HBc IgM", ["Anti-HBs only", "HBeAg only", "HBsAg only"], "When HBsAg has disappeared and anti-HBs is not yet detectable, IgM anti-HBc indicates recent infection."),
        q("A person with anti-HBs only and no anti-HBc most likely has:", "Immunity due to vaccination", ["Chronic active HBV", "Window period", "Acute HAV"], "HBV vaccine contains HBsAg and induces anti-HBs without anti-HBc."),
        q("Hepatitis D virus can replicate only in the presence of:", "Hepatitis B surface antigen", ["Hepatitis A capsid", "HCV polymerase", "HEV ORF2"], "HDV is defective and requires HBV HBsAg for assembly."),
        q("Chronic hepatitis C is clinically important because it commonly leads to:", "Cirrhosis and hepatocellular carcinoma risk", ["Hydatid cyst", "Tetanus", "Cholera"], "HCV frequently becomes chronic and can progress to cirrhosis and HCC."),
        q("The best test to confirm active hepatitis C infection after a positive antibody screen is:", "HCV RNA", ["Widal test", "HBsAb titer", "ASO titer"], "Anti-HCV shows exposure; RNA confirms current viremia."),
        q("Yellow fever severe disease causes jaundice and hemorrhage. The vector is:", "Aedes mosquito", ["Anopheles mosquito", "Sandfly", "Tsetse fly"], "Yellow fever is a flavivirus transmitted by Aedes and other mosquitoes depending on cycle."),
        q("Councilman bodies in viral hepatitis represent:", "Apoptotic hepatocytes", ["Bacterial spores", "Fungal hyphae", "Malaria gametocytes"], "Councilman bodies are acidophilic apoptotic hepatocytes seen in viral hepatitis/yellow fever."),
    ]),
    ("parasitic-hepatobiliary", "Parasitic Infections of Hepatobiliary System: Amoebic Liver Abscess, Hydatid Disease, Trematode Infections and Others", [
        q("A patient with fever, right upper quadrant pain, and anchovy sauce aspirate from liver abscess most likely has:", "Entamoeba histolytica", ["Echinococcus granulosus", "Clonorchis sinensis", "Fasciola hepatica"], "Amebic liver abscess classically produces sterile chocolate/anchovy sauce-like material."),
        q("Amebic liver abscess usually reaches liver through:", "Portal venous spread from colonic infection", ["Airborne spread", "Mosquito inoculation", "Direct skin penetration"], "E. histolytica invades colon and travels via portal circulation."),
        q("Treatment of invasive amoebic liver abscess should be followed by luminal therapy because:", "Intestinal cyst carriage can persist after tissue therapy", ["Luminal drugs drain pus", "Metronidazole treats only bacteria", "Cysts live only in liver"], "Metronidazole treats tissue disease; luminal agents eradicate intestinal colonization."),
        q("Hydatid cyst disease is caused by larval stage of:", "Echinococcus granulosus", ["Taenia saginata", "Ascaris lumbricoides", "Enterobius vermicularis"], "Humans are accidental intermediate hosts for E. granulosus larvae."),
        q("Hydatid cyst surgery must avoid spillage because rupture can cause:", "Anaphylaxis and secondary dissemination", ["Cholera toxin release", "Tetanus spasms", "Typhoid relapse"], "Hydatid fluid is antigenic and protoscolices can seed daughter cysts."),
        q("The definitive host of Echinococcus granulosus is usually:", "Dog", ["Human", "Pig", "Snail"], "Dogs harbor adult worms; humans acquire eggs from dog fecal contamination."),
        q("Fasciola hepatica infection is commonly acquired by eating:", "Aquatic plants such as watercress", ["Undercooked beef", "Raw crab", "Contaminated rice only"], "Fasciola metacercariae encyst on aquatic vegetation."),
        q("Clonorchis sinensis infection is acquired from:", "Raw or undercooked freshwater fish", ["Dog bite", "Mosquito bite", "Unwashed berries"], "Clonorchis metacercariae are transmitted in freshwater fish."),
        q("Chronic Clonorchis/Opisthorchis infection increases risk of:", "Cholangiocarcinoma", ["Hepatoblastoma only", "Gastric volvulus", "Intussusception only"], "Chronic biliary fluke inflammation is linked to cholangiocarcinoma."),
        q("Eosinophilia with biliary colic after freshwater plant ingestion suggests:", "Fascioliasis", ["HAV infection", "HCV infection", "Pyogenic abscess only"], "Tissue-invasive helminths such as Fasciola often cause eosinophilia."),
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
            questions.append({**BASE, "id": f"micro-hepatobiliary-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "microbiology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 3 or len(questions) != 30:
        raise AssertionError(f"Expected 3 topics and 30 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 30:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
