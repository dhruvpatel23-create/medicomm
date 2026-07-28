import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Gastrointestinal (GI) Infections"
BASE = {"subjectId": "microbiology", "subjectTitle": "Microbiology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("gi-infective-syndromes", "Gastrointestinal Infective Syndromes", [
        q("A patient has profuse watery diarrhea without blood or fever after ingesting contaminated water. The dominant pathophysiology is most likely:", "Enterotoxin-mediated secretory diarrhea", ["Mucosal invasion with ulceration", "Autoimmune villous atrophy", "Pure constipation overflow"], "Watery diarrhea without inflammation suggests toxin-mediated secretion rather than invasive dysentery."),
        q("A patient with fever, tenesmus, and blood-mucus stool most likely has:", "Inflammatory dysentery from colonic invasion", ["Noninflammatory secretory diarrhea", "Pure gastric outlet obstruction", "Viral hepatitis"], "Blood, fever, cramps, and tenesmus point to invasive or cytotoxin-mediated colitis."),
        q("The most useful stool test in acute dysentery to support inflammatory diarrhea is:", "Fecal leukocytes or lactoferrin", ["Urine ketones", "Serum amylase only", "Sputum culture"], "Neutrophils in stool suggest mucosal inflammation/invasion."),
        q("Oral rehydration solution works in acute diarrhea because:", "Sodium-glucose cotransport remains functional in small intestine", ["It kills Vibrio directly", "It blocks all toxins", "It stops peristalsis completely"], "ORS exploits intact SGLT1-mediated absorption even in secretory diarrhea."),
        q("Empiric antibiotics in acute diarrhea are avoided routinely because:", "Many cases are self-limited and antibiotics can worsen some infections or resistance", ["All diarrheas are viral", "Antibiotics never reach gut", "ORS cannot be combined with antibiotics"], "Treatment depends on severity, host risk, travel, dysentery, and suspected pathogen."),
        q("A patient with severe dehydration from cholera needs first:", "Rapid fluid and electrolyte replacement", ["Immediate colonoscopy", "High-dose loperamide only", "Steroids"], "Mortality in cholera is from dehydration; rehydration is the lifesaving intervention."),
        q("Food poisoning with vomiting within 2 hours of eating cream pastry suggests:", "Preformed toxin ingestion", ["Invasive typhoid", "Hepatitis E", "Amebic liver abscess"], "Very short incubation with vomiting suggests preformed toxin such as S. aureus."),
        q("Persistent diarrhea in an AIDS patient should raise suspicion for:", "Opportunistic protozoa such as Cryptosporidium", ["Only pinworm", "Only botulism", "Only tetanus"], "Immunocompromised patients can have chronic diarrhea due to coccidian parasites and other opportunists."),
        q("A stool culture is most indicated in acute diarrhea when there is:", "Blood, fever, severe illness, outbreak concern, or immunocompromise", ["Mild watery diarrhea for 6 hours only", "Simple constipation", "No GI symptoms"], "Culture/testing is targeted to severe, inflammatory, persistent, or public health-relevant cases."),
        q("A common complication of severe diarrhea in infants is:", "Hypovolemic shock and metabolic acidosis", ["Pulmonary fibrosis", "Cataract", "Hyperthyroidism"], "Fluid and bicarbonate loss can rapidly cause shock and acidosis in children."),
    ]),
    ("food-poisoning", "Food Poisoning: S. aureus, Bacillus cereus, Clostridium botulinum and Others", [
        q("A student develops intense vomiting 2 hours after eating custard pastry. The most likely agent is:", "Staphylococcus aureus preformed enterotoxin", ["Clostridioides difficile", "Giardia lamblia", "Vibrio cholerae"], "S. aureus food poisoning has short incubation and vomiting from heat-stable preformed toxin."),
        q("Fried rice eaten at a buffet causes vomiting after 3 hours. The likely organism is:", "Bacillus cereus emetic toxin", ["Enterobius vermicularis", "Salmonella Typhi", "Rotavirus"], "B. cereus emetic syndrome is classically linked to reheated rice."),
        q("Watery diarrhea 12 hours after meat/gravy consumption suggests:", "Clostridium perfringens", ["S. aureus emetic toxin", "Botulinum toxin", "Hepatitis A"], "C. perfringens causes abdominal cramps and watery diarrhea after meat dishes, with longer incubation than preformed emetic toxins."),
        q("A patient has diplopia, dysphagia, descending weakness, and no fever after home-canned food. The toxin blocks:", "Acetylcholine release at neuromuscular junction", ["Dopamine release in basal ganglia", "GABA receptors in spinal cord", "Sodium-glucose cotransport"], "Botulinum toxin cleaves SNARE proteins and prevents acetylcholine release."),
        q("Infant botulism after honey exposure occurs because:", "Spores germinate in the infant gut and produce toxin", ["Preformed toxin is always in honey", "Honey causes cholera", "Honey contains Giardia cysts"], "Infants can ingest C. botulinum spores that colonize and produce toxin in the intestine."),
        q("Botulism treatment includes antitoxin because antitoxin:", "Neutralizes circulating unbound toxin", ["Reverses toxin already inside nerve terminals instantly", "Kills spores in gut", "Stimulates acetylcholine release"], "Antitoxin prevents progression by binding free toxin; supportive ventilation may be needed."),
        q("A key lab clue for C. perfringens food poisoning is:", "Large Gram-positive spore-forming anaerobic rods", ["Acid-fast bacilli", "Comma-shaped oxidase-positive rods", "Budding yeast"], "Clostridia are anaerobic spore-forming Gram-positive rods."),
        q("Scombroid fish poisoning resembles allergy because spoiled fish contains:", "Histamine", ["Botulinum toxin", "Cholera toxin", "Aflatoxin only"], "Histamine from improper fish storage causes flushing, headache, urticaria-like symptoms."),
        q("Mushroom poisoning with delayed hepatic failure is classically due to:", "Amanita phalloides amatoxins", ["Staphylococcal enterotoxin", "Bacillus cereus", "Norovirus"], "Amatoxins inhibit RNA polymerase II and can cause severe liver failure."),
        q("The most important prevention of bacterial food poisoning is:", "Safe cooking, rapid cooling, refrigeration, and avoiding temperature abuse", ["Adding antibiotics to all food", "Relying on smell alone", "Freezing after toxin has formed"], "Temperature control prevents bacterial growth and toxin production."),
    ]),
    ("enterobacteriaceae-gi", "Gastrointestinal Infections due to Enterobacteriaceae: Diarrheagenic Escherichia coli, Shigellosis, Nontyphoidal Salmonellosis and Yersiniosis", [
        q("A traveler develops watery diarrhea without blood after street food. The E. coli pathotype most likely is:", "ETEC", ["EHEC", "EIEC", "UPEC"], "Enterotoxigenic E. coli causes traveler's diarrhea via heat-labile/heat-stable toxins."),
        q("A child develops bloody diarrhea after undercooked beef and later hemolytic uremic syndrome. The likely organism is:", "EHEC/STEC", ["ETEC", "EAEC", "Salmonella Typhi"], "Shiga toxin-producing E. coli, especially O157:H7, causes hemorrhagic colitis and HUS."),
        q("Antibiotics are generally avoided in suspected EHEC because they may:", "Increase Shiga toxin release and HUS risk", ["Cause immediate cholera", "Prevent culture growth only", "Induce malaria relapse"], "Supportive care is preferred in suspected STEC infection."),
        q("Shigella causes dysentery with a very low infectious dose because it:", "Survives gastric acid and invades colonic mucosa", ["Requires mosquito transmission", "Forms spores", "Only produces preformed toxin in food"], "Shigella spreads person-to-person and invades the colon."),
        q("A stool isolate is nonmotile, non-lactose fermenting, and causes dysentery. This supports:", "Shigella", ["Proteus mirabilis", "Vibrio cholerae", "Campylobacter jejuni"], "Shigella is nonmotile and typically non-lactose fermenting."),
        q("Nontyphoidal Salmonella gastroenteritis is commonly acquired from:", "Eggs, poultry, reptiles, or contaminated food", ["Human-only chronic carriers always", "Mosquito bite", "Freshwater snail"], "Nontyphoidal Salmonella is zoonotic/food-borne."),
        q("Antibiotics for uncomplicated nontyphoidal Salmonella diarrhea in healthy adults are often avoided because:", "They may prolong fecal carriage and are usually unnecessary", ["They always cause HUS", "They cannot treat Gram-negative rods", "They cause botulism"], "Most cases are self-limited; treat severe disease or high-risk hosts."),
        q("Yersinia enterocolitica can mimic appendicitis because it causes:", "Mesenteric adenitis and terminal ileitis", ["Pyloric stenosis", "Pancreatitis", "Esophageal candidiasis"], "Yersinia infection may present with right lower quadrant pain."),
        q("Yersinia grows well at refrigerator temperature, explaining outbreaks linked to:", "Cold-stored contaminated food", ["Boiled water only", "Mosquito breeding", "Canned honey only"], "Yersinia can multiply at low temperatures."),
        q("EIEC resembles Shigella clinically because it:", "Invades colonic epithelial cells causing dysentery", ["Produces only preformed emetic toxin", "Forms spores", "Causes botulism"], "Enteroinvasive E. coli produces invasive colitis similar to shigellosis."),
    ]),
    ("cholera-vibrio-aeromonas", "Cholera, Halophilic Vibrio and Aeromonas Infections", [
        q("A patient has rice-water stools and severe dehydration. The virulence mechanism is:", "Cholera toxin ADP-ribosylates Gs, increasing cAMP", ["Shiga toxin inactivates 60S ribosomes", "Botulinum toxin blocks ACh release", "Exfoliative toxin cleaves desmoglein"], "Cholera toxin causes secretory diarrhea through cAMP-mediated chloride secretion."),
        q("The most important treatment for cholera is:", "Aggressive rehydration", ["Immediate colectomy", "High-dose steroids", "Antitoxin"], "Rehydration prevents death; antibiotics shorten duration but are secondary."),
        q("Vibrio cholerae on microscopy classically appears as:", "Comma-shaped motile Gram-negative rods", ["Gram-positive cocci in clusters", "Acid-fast rods", "Budding yeast"], "Vibrios are curved/comma-shaped motile Gram-negative bacilli."),
        q("TCBS agar is used for selective isolation of:", "Vibrio species", ["Shigella only", "Candida", "Mycobacterium"], "Thiosulfate citrate bile salts sucrose agar selects for Vibrio."),
        q("Vibrio cholerae O1 and O139 cause epidemics because they:", "Produce cholera toxin and spread efficiently through contaminated water", ["Form spores in rice", "Are airborne", "Require animal bites"], "Epidemic cholera is linked to toxigenic O1/O139 strains and water sanitation failure."),
        q("Seafood-associated gastroenteritis after eating raw oysters suggests:", "Vibrio parahaemolyticus", ["Vibrio cholerae O1 always", "Shigella dysenteriae", "Enterobius"], "Halophilic Vibrio species are associated with marine seafood."),
        q("Severe wound infection after seawater exposure in a cirrhotic patient suggests:", "Vibrio vulnificus", ["Clostridioides difficile", "H. pylori", "Giardia"], "V. vulnificus causes severe wound sepsis, especially in liver disease."),
        q("Vibrio vulnificus sepsis is especially severe in patients with:", "Chronic liver disease or iron overload", ["Atopic dermatitis only", "Myopia", "Hypothyroidism"], "Iron-rich states and liver disease increase risk of fulminant V. vulnificus infection."),
        q("Aeromonas diarrhea or wound infection is often linked to:", "Freshwater exposure", ["Dry soil only", "Dog bite only", "Airborne droplet nuclei"], "Aeromonas species are aquatic organisms found in freshwater."),
        q("ORS works in cholera because:", "Glucose-coupled sodium absorption remains intact", ["It blocks toxin binding", "It kills vibrios directly", "It stops chloride secretion completely"], "SGLT1-mediated sodium and water absorption persists despite cholera toxin."),
    ]),
    ("misc-bacterial-gi", "Miscellaneous Bacterial Infections of Gastrointestinal System: Helicobacter, Campylobacter and Clostridioides difficile Infections", [
        q("A patient with duodenal ulcer has urease-positive curved bacilli on gastric biopsy. The organism is:", "Helicobacter pylori", ["Campylobacter jejuni", "Vibrio cholerae", "Shigella sonnei"], "H. pylori is urease-positive and colonizes gastric mucosa."),
        q("H. pylori survives gastric acidity mainly by:", "Urease-mediated ammonia production", ["Spore formation", "Capsule swelling", "Shiga toxin"], "Urease generates ammonia, buffering the local gastric environment."),
        q("A noninvasive test confirming active H. pylori infection after therapy is:", "Urea breath test", ["Widal test", "Weil-Felix test", "ASO titer"], "Urea breath and stool antigen tests detect active infection."),
        q("Campylobacter jejuni gastroenteritis is commonly acquired from:", "Undercooked poultry", ["Home-canned vegetables", "Pigeon droppings", "Mosquito bite"], "Campylobacter is strongly associated with poultry exposure."),
        q("Campylobacter jejuni is linked to postinfectious:", "Guillain-Barre syndrome", ["Rheumatic fever", "Subacute sclerosing panencephalitis", "Hydatid disease"], "Molecular mimicry after C. jejuni can trigger GBS."),
        q("Campylobacter grows best under:", "Microaerophilic conditions", ["Strict anaerobic conditions only", "High salt alkaline water only", "No oxygen with spores"], "Campylobacter requires reduced oxygen tension."),
        q("A hospitalized patient develops watery diarrhea after clindamycin. The major toxins are:", "Toxin A and toxin B", ["Shiga toxin and LT toxin", "Botulinum toxin", "Cholera toxin"], "C. difficile toxins damage colonic epithelium and cause colitis."),
        q("Pseudomembranous colitis is most commonly associated with:", "Clostridioides difficile", ["H. pylori", "Vibrio parahaemolyticus", "Yersinia pestis"], "C. difficile causes antibiotic-associated pseudomembranous colitis."),
        q("Preferred therapy for initial C. difficile infection commonly includes:", "Oral vancomycin or fidaxomicin", ["IV acyclovir", "Albendazole", "Doxycycline for all cases"], "Oral vancomycin/fidaxomicin target colonic C. difficile."),
        q("Recurrent C. difficile improves after fecal microbiota transplantation because it:", "Restores colonization resistance", ["Directly neutralizes toxin with antibody only", "Kills spores by heat", "Blocks gastric urease"], "Restoring diverse gut microbiota can prevent recurrent overgrowth."),
    ]),
    ("viral-gastroenteritis", "Viral Gastroenteritis: Rotaviruses and Others", [
        q("Severe dehydrating diarrhea in an unvaccinated infant is classically caused by:", "Rotavirus", ["Norovirus only", "Adenovirus 40/41 only", "Astrovirus only"], "Rotavirus is a major cause of severe infantile gastroenteritis."),
        q("Rotavirus has a segmented dsRNA genome, making it prone to:", "Reassortment", ["Integration into host DNA", "Reverse transcription", "Spore formation"], "Segmented genomes can reassort during coinfection."),
        q("Rotavirus diarrhea occurs partly because NSP4 acts as:", "Enterotoxin", ["Neuraminidase", "Reverse transcriptase", "Hemolysin"], "Rotavirus NSP4 contributes to secretory diarrhea."),
        q("The best prevention of severe rotavirus diarrhea is:", "Vaccination in infancy", ["Antibiotic prophylaxis", "Boiling all milk only", "BCG vaccination"], "Rotavirus vaccines reduce severe disease and hospitalization."),
        q("A cruise ship has explosive vomiting and diarrhea affecting many passengers. The likely virus is:", "Norovirus", ["Rabies virus", "HSV-1", "Hepatitis B"], "Norovirus causes highly contagious outbreaks in closed settings."),
        q("Norovirus outbreaks are difficult to control because the virus has:", "Low infectious dose and environmental stability", ["Fragile envelope", "Need for mosquito vector", "No fecal shedding"], "Norovirus spreads easily by fecal-oral routes, fomites, and aerosols from vomitus."),
        q("Enteric adenovirus types most associated with pediatric gastroenteritis are:", "40 and 41", ["16 and 18", "6 and 11", "1 and 2 only"], "Adenovirus 40/41 cause diarrhea in children."),
        q("Viral gastroenteritis stool usually lacks:", "Many fecal leukocytes or gross blood", ["Watery consistency", "Vomiting", "Dehydration risk"], "Most viral gastroenteritis is noninflammatory."),
        q("Treatment of uncomplicated viral gastroenteritis is mainly:", "Oral/IV rehydration and electrolyte support", ["Routine antibiotics", "Steroids", "Antitoxin"], "Supportive rehydration is the mainstay."),
        q("Astrovirus gastroenteritis is most important in:", "Children, elderly, and immunocompromised patients", ["Only adult men with ulcers", "Only snakebite victims", "Only malaria patients"], "Astrovirus causes mild gastroenteritis but can matter in vulnerable groups."),
    ]),
    ("intestinal-protozoa", "Intestinal Protozoan Infections: Intestinal Amoebiasis, Giardiasis, Coccidian Parasitic Infections, Balantidiasis, Blastocystosis, and Others", [
        q("Trophozoites with ingested RBCs in dysenteric stool are diagnostic of:", "Entamoeba histolytica", ["Entamoeba coli", "Giardia lamblia", "Balantidium coli"], "E. histolytica trophozoites may contain ingested erythrocytes."),
        q("Amebic liver abscess classically produces:", "Anchovy sauce pus", ["Rice-water stool", "Pseudomembranes", "Rose spots"], "Amebic abscess material is classically described as anchovy sauce-like."),
        q("Treatment of invasive amoebiasis should include luminal therapy because:", "Metronidazole does not reliably eradicate intestinal cyst carriage", ["Luminal drugs treat liver only", "Cysts are viral", "Metronidazole causes giardiasis"], "A luminal agent such as paromomycin clears cysts and prevents relapse/transmission."),
        q("A camper has foul-smelling greasy diarrhea, bloating, and weight loss after stream water. The likely organism is:", "Giardia lamblia", ["E. histolytica", "Cryptosporidium parvum", "Balantidium coli"], "Giardia causes malabsorption/steatorrhea after cyst ingestion from contaminated water."),
        q("Giardia attaches to intestinal mucosa using:", "Ventral sucking disc", ["Hooklets", "Cilia", "Polar tube"], "The ventral disc mediates attachment and contributes to malabsorption."),
        q("Acid-fast oocysts in stool of an AIDS patient with chronic watery diarrhea suggest:", "Cryptosporidium", ["Giardia", "Entamoeba", "Trichomonas"], "Cryptosporidium, Cyclospora, and Cystoisospora oocysts are acid-fast to varying degrees."),
        q("Cryptosporidium is difficult in AIDS because infection may be:", "Chronic and severe with biliary involvement", ["Always asymptomatic", "Limited to blood", "Prevented by antibiotics alone"], "Cellular immunity is important for control; AIDS can cause persistent disease."),
        q("Balantidium coli is notable because it is:", "A ciliated intestinal protozoan", ["A flagellated blood parasite", "A cestode", "A fungus"], "Balantidium is the only ciliated protozoan infecting humans."),
        q("Cyclospora diarrhea is linked to:", "Contaminated fresh produce and acid-fast oocysts", ["Undercooked beef only", "Dog bite", "Mosquito bite"], "Cyclospora spreads through contaminated food/water and causes prolonged diarrhea."),
        q("Blastocystis interpretation in stool requires caution because:", "Pathogenic role can be variable and must be correlated clinically", ["It always causes fatal dysentery", "It is always a lab artifact", "It proves helminth infection"], "Blastocystis may be commensal or associated with symptoms depending on context."),
    ]),
    ("intestinal-helminths", "Intestinal Helminthic Infections", [
        q("A child with perianal itching at night is diagnosed by tape test. The parasite is:", "Enterobius vermicularis", ["Ascaris lumbricoides", "Taenia solium", "Strongyloides stercoralis"], "Pinworm females lay eggs around the anus at night."),
        q("Ascaris lumbricoides can cause intestinal obstruction because:", "Adult worms are large and may aggregate", ["Eggs invade RBCs", "Larvae form hydatid cysts", "Worms live only in liver"], "Heavy Ascaris burden can obstruct intestine or biliary tract."),
        q("Hookworm causes iron deficiency anemia because adult worms:", "Attach to intestinal mucosa and suck blood", ["Block vitamin B12 absorption only", "Destroy platelets", "Invade red cells"], "Ancylostoma/Necator cause chronic intestinal blood loss."),
        q("Strongyloides is dangerous in steroid-treated patients because it can:", "Cause autoinfection and hyperinfection", ["Transform into malaria", "Produce hydatid cysts", "Cause only perianal itching"], "Strongyloides can replicate within the host and disseminate during immunosuppression."),
        q("Whipworm infection is caused by:", "Trichuris trichiura", ["Enterobius", "Hymenolepis nana", "Diphyllobothrium latum"], "Trichuris has barrel-shaped eggs with bipolar plugs and can cause dysentery/rectal prolapse in heavy infection."),
        q("Diphyllobothrium latum infection may cause:", "Vitamin B12 deficiency", ["Iron overload", "Hyperthyroidism", "Hemolytic uremic syndrome"], "Fish tapeworm can compete for vitamin B12 and cause megaloblastic anemia."),
        q("Taenia solium is more dangerous than T. saginata because ingestion of eggs can cause:", "Cysticercosis", ["Hydatid cyst only", "Malaria", "Schistosomiasis"], "T. solium eggs release larvae that encyst in tissues including brain."),
        q("Hymenolepis nana is notable because it can:", "Complete its life cycle in humans with autoinfection", ["Require cattle as mandatory host", "Transmit by mosquito", "Cause liver flukes"], "Dwarf tapeworm can cause internal autoinfection."),
        q("Fasciolopsis buski is an intestinal:", "Trematode", ["Cestode", "Nematode", "Protozoan"], "F. buski is the giant intestinal fluke."),
        q("Schistosoma mansoni and S. japonicum intestinal disease is mainly due to:", "Granulomatous reaction to eggs in intestinal and portal tissues", ["Adult worms eating mucosa", "Preformed toxin", "Larval lung migration only"], "Egg deposition drives inflammation, fibrosis, and portal complications."),
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
            questions.append({**BASE, "id": f"micro-gi-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

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
