import json
from pathlib import Path

DATA = Path("runtime-data/users.json")
CHAPTER = "Chemotherapy of Infectious Diseases"
BASE = {"subjectId": "pharmacology", "subjectTitle": "Pharmacology", "chapterTitle": CHAPTER, "source": "ai", "imageUrls": []}


def q(prompt, answer, wrong, explanation):
    return {"prompt": prompt, "answer": answer, "wrong": wrong, "explanation": explanation}


TOPICS = [
    ("general-antimicrobial-therapy", "General Principles of Antimicrobial Therapy", [
        q("A septic patient is started on broad empiric antibiotics after blood cultures. Why should therapy later be narrowed?", "To reduce toxicity, resistance selection, and microbiome disruption", ["To make therapy less active", "To avoid source control", "To prevent all drug penetration"], "De-escalation keeps adequate coverage while reducing collateral damage."),
        q("A beta-lactam works best when free drug levels remain above the MIC. This is an example of:", "Time-dependent killing", ["Concentration-dependent killing", "Postantibiotic antagonism", "Biofilm immunity"], "Beta-lactams depend mainly on time above MIC rather than high peaks."),
        q("Aminoglycosides are often dosed once daily because they show:", "Concentration-dependent killing and postantibiotic effect", ["Pure time-dependent killing", "No renal toxicity", "No need for monitoring"], "High peak/MIC ratios improve aminoglycoside killing; postantibiotic effect supports extended-interval dosing."),
        q("A patient with an abscess fails antibiotics until drainage is done. The best explanation is:", "Source control is required when drug penetration and host clearance are inadequate", ["All antibiotics are bacteriostatic", "Abscess pH activates every antibiotic", "Drainage prevents resistance in blood only"], "Antimicrobials often cannot sterilize undrained pus or necrotic tissue."),
        q("A bacteriostatic drug may still cure infection because:", "Host immunity can clear growth-arrested organisms", ["It always lyses bacteria immediately", "It blocks all human ribosomes", "It is never affected by resistance"], "Static agents inhibit growth, allowing immune clearance when host defenses are adequate."),
        q("Endocarditis is commonly treated with prolonged bactericidal therapy because vegetations have:", "High bacterial burden and limited immune penetration", ["No bacteria", "Excess drug penetration", "Only viral replication"], "Deep-seated infections with dense organisms require sustained bactericidal exposure."),
        q("A patient on warfarin receives TMP-SMX and develops high INR. The principle is:", "Antimicrobials can cause clinically important drug interactions", ["Antibiotics cannot affect anticoagulants", "Warfarin blocks bacterial ribosomes", "TMP-SMX reverses vitamin K instantly"], "Antibiotics may alter CYP metabolism, gut flora, or protein binding."),
        q("A patient with renal failure needs antibiotic adjustment mainly to avoid:", "Drug accumulation and toxicity", ["Lowering MIC", "Increasing bacterial mutation rate", "Reducing all hepatic metabolism"], "Many antimicrobials are renally cleared and require dose adjustment."),
        q("A hospital antibiogram is most useful for:", "Choosing empiric therapy based on local susceptibility patterns", ["Replacing cultures in every case", "Measuring patient creatinine", "Diagnosing viral infections"], "Empiric choices should reflect local resistance data."),
        q("Combination therapy is most justified when:", "It broadens empiric coverage, prevents resistance in select infections, or creates synergy", ["It always halves toxicity", "It is required for every sore throat", "It eliminates need for diagnosis"], "Combinations are useful in selected settings such as severe sepsis, TB, HIV, and some enterococcal infections."),
    ]),
    ("dna-disruptors", "DNA Disruptors: Sulfonamides, Quinolones, and Nitroimidazoles", [
        q("TMP-SMX treats Pneumocystis pneumonia by sequentially blocking:", "Folate synthesis", ["Cell wall cross-linking", "Ergosterol synthesis", "DNA gyrase only"], "Sulfamethoxazole blocks dihydropteroate synthase; trimethoprim blocks dihydrofolate reductase."),
        q("A patient on TMP-SMX develops hyperkalemia. Which component acts like a potassium-sparing diuretic?", "Trimethoprim", ["Sulfamethoxazole", "PABA", "Folinic acid"], "Trimethoprim can inhibit ENaC-like sodium channels in the collecting duct."),
        q("Sulfonamides are avoided late in pregnancy because they can:", "Displace bilirubin and increase kernicterus risk", ["Cause fetal thyroid ablation", "Block fetal opioid receptors", "Induce tooth discoloration only"], "Sulfonamides can displace bilirubin from albumin in neonates."),
        q("Ciprofloxacin is effective for many gram-negative infections because it inhibits:", "DNA gyrase and topoisomerase IV", ["Dihydrofolate reductase", "Peptidyl transferase", "Beta-lactamase"], "Fluoroquinolones block bacterial topoisomerases required for DNA replication."),
        q("A patient taking levofloxacin develops Achilles pain. The key adverse effect is:", "Tendinopathy and tendon rupture", ["Ototoxicity from hair cell uptake", "Gray baby syndrome", "Red man syndrome"], "Fluoroquinolones can damage tendons, especially in older patients and steroid users."),
        q("Fluoroquinolones should be separated from iron or calcium because cations:", "Chelate the drug and reduce absorption", ["Activate bacterial efflux pumps directly", "Cause folate rescue", "Prevent renal excretion"], "Divalent/trivalent cations markedly reduce oral quinolone absorption."),
        q("Metronidazole is especially useful for anaerobic infections because anaerobes:", "Reduce the drug to DNA-damaging radicals", ["Lack ribosomes", "Have ergosterol membranes", "Cannot make folate"], "Metronidazole is activated in low-redox anaerobic organisms and protozoa."),
        q("A patient taking metronidazole drinks alcohol and becomes flushed and nauseated. This resembles:", "Disulfiram-like reaction", ["Serotonin syndrome", "Cholinergic crisis", "Opioid withdrawal"], "Metronidazole can cause an alcohol intolerance reaction in some patients."),
        q("Nitrofurantoin is useful for uncomplicated cystitis but not pyelonephritis because it:", "Concentrates in urine but has poor renal tissue levels", ["Cannot enter bladder urine", "Only treats viruses", "Is inactivated by urine"], "Nitrofurantoin is a lower-tract urinary antiseptic."),
        q("A G6PD-deficient patient on sulfonamides develops hemolysis. The mechanism is:", "Oxidative stress exceeding red cell antioxidant capacity", ["Direct platelet activation", "Beta-lactam allergy", "Calcium chelation"], "Sulfonamides and other oxidant drugs can trigger hemolysis in G6PD deficiency."),
    ]),
    ("cell-envelope-disruptors", "Cell Envelope Disruptors: β-Lactam, Glycopeptide, and Lipopeptide Antibacterials", [
        q("Penicillin kills susceptible bacteria by:", "Inhibiting transpeptidation during peptidoglycan cross-linking", ["Blocking 30S initiation", "Disrupting ergosterol", "Inhibiting folate synthesis"], "Beta-lactams bind PBPs and prevent cell wall cross-linking."),
        q("Adding clavulanate to amoxicillin helps when resistance is due to:", "Beta-lactamase hydrolysis", ["Altered ribosomal methylation", "Loss of ergosterol", "VanA D-Ala-D-Lac substitution"], "Clavulanate inhibits many beta-lactamases, protecting amoxicillin."),
        q("Piperacillin-tazobactam is selected for suspected Pseudomonas sepsis because piperacillin has:", "Antipseudomonal beta-lactam activity", ["Only anaerobic gram-positive activity", "No cell wall activity", "Direct endotoxin binding"], "Extended-spectrum ureidopenicillins cover Pseudomonas when susceptible."),
        q("Ceftriaxone is convenient for gonorrhea partly because it:", "Has broad gram-negative activity and long half-life", ["Is only oral", "Cannot enter tissues", "Is a glycopeptide"], "Ceftriaxone is a third-generation cephalosporin with useful tissue penetration and dosing."),
        q("Cefepime is often chosen for neutropenic fever because it covers:", "Pseudomonas aeruginosa", ["MRSA reliably as monotherapy", "Candida", "Atypical viruses"], "Cefepime is a fourth-generation cephalosporin with antipseudomonal activity."),
        q("Aztreonam may be useful in severe IgE-mediated penicillin allergy because it:", "Is a monobactam with minimal cross-reactivity except with ceftazidime side chain concern", ["Covers only gram-positive cocci", "Blocks folate synthesis", "Treats anaerobes well"], "Aztreonam covers aerobic gram-negative rods and has low beta-lactam cross-allergy."),
        q("Vancomycin treats MRSA by binding:", "D-Ala-D-Ala termini of cell wall precursors", ["PBPs at active site", "50S ribosome", "DNA gyrase"], "Glycopeptides block cell wall precursor incorporation."),
        q("Vancomycin infusion causes flushing and hypotension. The prevention is:", "Slow infusion and antihistamine if needed", ["Give alcohol", "Add folinic acid", "Avoid renal monitoring"], "Vancomycin infusion reaction is histamine-mediated and rate-related."),
        q("Daptomycin cannot treat pneumonia effectively because it is:", "Inactivated by pulmonary surfactant", ["Destroyed by stomach acid only", "Unable to bind membranes", "A beta-lactamase substrate"], "Surfactant binds/inactivates daptomycin in alveoli."),
        q("A VRE isolate with D-Ala-D-Lac resistance reduces vancomycin binding by:", "Removing a critical hydrogen bond target", ["Increasing ergosterol", "Methylating 23S rRNA", "Producing PABA"], "D-Ala-D-Lac substitution markedly lowers glycopeptide affinity."),
    ]),
    ("misc-antibacterials", "Miscellaneous Antibacterials: Aminoglycosides, Polymyxins, Urinary Antiseptics, Bacteriophages", [
        q("Gentamicin plus ampicillin for enterococcal endocarditis is synergistic because:", "Cell wall inhibition improves aminoglycoside entry", ["Gentamicin blocks beta-lactamase", "Ampicillin inhibits 30S", "Both block folate"], "Beta-lactam cell wall damage facilitates aminoglycoside penetration."),
        q("Aminoglycosides require oxygen-dependent uptake, so they have poor activity against:", "Anaerobes", ["Aerobic gram-negative rods", "Mycobacteria", "Some staphylococci"], "Anaerobic conditions impair aminoglycoside transport into bacteria."),
        q("A patient on gentamicin develops rising creatinine and vertigo. The key toxicities are:", "Nephrotoxicity and ototoxicity", ["Hepatitis and pancreatitis", "Tendon rupture and QT prolongation", "Hemolysis and kernicterus"], "Aminoglycosides can injure renal proximal tubules and inner ear hair cells."),
        q("Amikacin can retain activity against some gentamicin-resistant organisms because it:", "Resists many aminoglycoside-modifying enzymes", ["Is a beta-lactam", "Blocks ergosterol", "Inhibits HIV protease"], "Amikacin is less susceptible to several modifying enzymes."),
        q("Colistin is reserved for multidrug-resistant gram-negative infections because it:", "Disrupts bacterial outer membranes but is nephrotoxic/neurotoxic", ["Has no toxicity", "Only treats gram positives", "Blocks 50S ribosome"], "Polymyxins bind LPS/phospholipids and are limited by toxicity."),
        q("Fosfomycin treats uncomplicated cystitis by inhibiting:", "MurA in early peptidoglycan synthesis", ["DNA gyrase", "50S peptidyl transferase", "Ergosterol synthesis"], "Fosfomycin blocks an early cell wall precursor step and concentrates in urine."),
        q("Methenamine works as a urinary antiseptic when acidic urine converts it to:", "Formaldehyde", ["Nitric oxide", "D-Ala-D-Ala", "Folinic acid"], "Methenamine releases formaldehyde in acidic urine, suppressing bacterial growth."),
        q("Bacteriophage therapy is conceptually attractive for resistant infection because phages:", "Can specifically infect and lyse target bacteria", ["Kill human cells selectively", "Replace all antibiotics for sepsis", "Block fungal ergosterol"], "Phages can be highly bacteria-specific, though clinical use is specialized."),
        q("Spectinomycin historically treated gonorrhea by:", "Inhibiting bacterial protein synthesis", ["Blocking folate", "Disrupting fungal membranes", "Inhibiting neuraminidase"], "Spectinomycin interferes with ribosomal translocation but is rarely used in many settings."),
        q("Aminoglycoside peak levels are monitored mainly to ensure:", "Adequate concentration-dependent killing without excessive toxicity", ["Time above MIC only", "No renal excretion", "Serotonin safety"], "Peak/trough monitoring balances efficacy and toxicity."),
    ]),
    ("protein-synthesis-inhibitors", "Protein Synthesis Inhibitors", [
        q("Doxycycline treats atypical pneumonia because it inhibits:", "30S ribosomal aminoacyl-tRNA binding", ["Cell wall transpeptidation", "DNA gyrase", "Fungal beta-glucan"], "Tetracyclines bind 30S and block tRNA entry."),
        q("Tetracyclines are avoided in young children because they:", "Discolor teeth and affect bone growth", ["Cause gray baby syndrome", "Cause kernicterus only", "Destroy cartilage tendons"], "Tetracyclines chelate calcium and deposit in teeth/bone."),
        q("Doxycycline absorption falls when taken with antacids because:", "Cations chelate the drug", ["Acid destroys all drug", "Antacids induce CYP3A4", "Calcium activates efflux"], "Divalent/trivalent cations reduce tetracycline absorption."),
        q("Azithromycin inhibits protein synthesis by binding:", "50S ribosomal subunit and blocking translocation", ["30S initiation complex", "PBPs", "Dihydrofolate reductase"], "Macrolides bind 50S rRNA and block translocation."),
        q("Erythromycin can cause QT prolongation and drug interactions because it:", "Can inhibit CYP3A4 and affect cardiac repolarization", ["Chelates calcium only", "Blocks renal ENaC", "Inhibits xanthine oxidase"], "Macrolides vary in CYP inhibition; erythromycin/clarithromycin are stronger inhibitors."),
        q("Clindamycin is useful for anaerobic infections but strongly associated with:", "C. difficile colitis", ["Ototoxicity", "Tendon rupture", "Kernicterus"], "Clindamycin disrupts gut flora and is a classic C. difficile risk."),
        q("Linezolid treats MRSA and VRE by:", "Blocking formation of the 70S initiation complex", ["Inhibiting cell wall D-Ala-D-Ala", "Activating beta-lactamase", "Blocking DNA gyrase"], "Oxazolidinones bind 50S and prevent initiation."),
        q("A patient on linezolid and sertraline develops clonus and fever. The concern is:", "Serotonin syndrome", ["Cholinergic crisis", "Thyroid storm", "Vancomycin infusion reaction"], "Linezolid has MAO-inhibiting activity and can interact with serotonergic drugs."),
        q("Chloramphenicol causes gray baby syndrome because neonates have:", "Poor glucuronidation and drug accumulation", ["Excess renal clearance", "No ribosomes", "High beta-lactamase"], "Immature hepatic metabolism in neonates increases chloramphenicol toxicity."),
        q("Quinupristin-dalfopristin can treat some VRE but not Enterococcus faecalis reliably because:", "Species susceptibility differs despite same genus", ["It only treats viruses", "It is a beta-lactam", "It cannot reach blood"], "Streptogramin activity is species-dependent, with E. faecium more susceptible than E. faecalis."),
    ]),
    ("antifungal-agents", "Antifungal Agents", [
        q("Amphotericin B treats severe systemic mycoses by binding:", "Ergosterol and forming membrane pores", ["Beta-glucan synthase", "Human tubulin only", "Viral neuraminidase"], "Amphotericin binds fungal ergosterol, disrupting membrane integrity."),
        q("A patient on amphotericin B develops fever, chills, renal dysfunction, and hypokalemia. These are:", "Expected infusion and nephrotoxic adverse effects", ["Proof of viral resistance", "Selective marrow aplasia only", "Disulfiram reaction"], "Amphotericin is limited by infusion reactions and nephrotoxicity."),
        q("Fluconazole is useful for cryptococcal suppression because it:", "Inhibits fungal 14-alpha-demethylase and penetrates CSF well", ["Blocks beta-glucan synthase only", "Binds bacterial PBPs", "Inhibits neuraminidase"], "Azoles inhibit ergosterol synthesis; fluconazole has good CNS penetration."),
        q("Voriconazole is often preferred for invasive aspergillosis but can cause:", "Visual disturbances and hepatotoxicity", ["Ototoxicity only", "Kernicterus", "Tendon rupture"], "Voriconazole has characteristic visual effects and hepatic/CYP interactions."),
        q("Echinocandins such as caspofungin act by inhibiting:", "Beta-1,3-glucan synthesis in fungal cell walls", ["Ergosterol binding", "DNA gyrase", "Folate synthesis"], "Echinocandins weaken fungal cell walls by blocking glucan synthase."),
        q("Terbinafine treats dermatophyte infection by inhibiting:", "Squalene epoxidase", ["14-alpha-demethylase", "Beta-glucan synthase", "Topoisomerase IV"], "Terbinafine blocks ergosterol synthesis earlier than azoles and accumulates in keratin."),
        q("Flucytosine is paired with amphotericin for cryptococcal meningitis because it:", "Is converted to 5-FU in fungi and improves fungicidal activity", ["Prevents amphotericin kidney injury completely", "Blocks ergosterol directly", "Treats bacteria only"], "Flucytosine inhibits fungal DNA/RNA synthesis; resistance emerges quickly alone."),
        q("Nystatin is used topically for Candida because it:", "Is too toxic for systemic use but binds ergosterol locally", ["Has excellent IV safety", "Blocks human cholesterol only", "Treats dermatophytes systemically"], "Nystatin is a polyene used for mucocutaneous candidiasis."),
        q("Griseofulvin treats dermatophytes by:", "Disrupting fungal microtubules and depositing in keratin", ["Binding ergosterol pores", "Inhibiting viral polymerase", "Blocking bacterial PBPs"], "Griseofulvin concentrates in keratinized tissue and inhibits fungal mitosis."),
        q("Azole resistance in Candida can occur through:", "Altered target enzyme, efflux pumps, or ergosterol pathway changes", ["Loss of bacterial cell wall only", "Increased human CYP activity only", "Viral latency"], "Fungal resistance often involves target alteration or drug efflux."),
    ]),
    ("antiviral-nonretroviral", "Antiviral Agents (Nonretroviral)", [
        q("Acyclovir selectively treats HSV because viral thymidine kinase:", "Phosphorylates acyclovir, trapping activation in infected cells", ["Destroys host DNA", "Blocks neuraminidase", "Activates protease"], "Acyclovir requires viral TK activation and inhibits viral DNA polymerase."),
        q("Acyclovir resistance in HSV commonly results from:", "Thymidine kinase deficiency or alteration", ["Neuraminidase mutation", "Loss of bacterial PBPs", "Ergosterol replacement"], "TK-negative mutants do not activate acyclovir effectively."),
        q("Ganciclovir treats CMV but causes dose-limiting:", "Myelosuppression", ["Tendon rupture", "Ototoxicity", "Kernicterus"], "Ganciclovir/valganciclovir commonly suppress bone marrow."),
        q("Foscarnet can treat acyclovir-resistant HSV because it:", "Directly inhibits viral DNA polymerase without phosphorylation", ["Requires viral TK", "Blocks neuraminidase only", "Activates interferon receptors"], "Foscarnet is a pyrophosphate analog that does not need viral kinase activation."),
        q("Oseltamivir shortens influenza symptoms by inhibiting:", "Neuraminidase-mediated virion release", ["Viral uncoating M2 in all strains", "Viral DNA polymerase", "Host ribosomes"], "Neuraminidase inhibitors reduce release and spread of influenza virions."),
        q("Baloxavir acts against influenza by inhibiting:", "Cap-dependent endonuclease", ["Neuraminidase", "M2 proton channel", "Reverse transcriptase"], "Baloxavir blocks influenza mRNA cap-snatching."),
        q("Remdesivir targets SARS-CoV-2 by:", "Inhibiting viral RNA-dependent RNA polymerase after nucleotide analog incorporation", ["Blocking ACE synthesis", "Inhibiting neuraminidase", "Binding ergosterol"], "Remdesivir is an adenosine nucleotide analog affecting viral RNA polymerase."),
        q("Nirmatrelvir is boosted with ritonavir because ritonavir:", "Inhibits CYP3A to increase nirmatrelvir levels", ["Blocks viral neuraminidase", "Prevents renal filtration only", "Activates host interferon"], "Ritonavir pharmacokinetic boosting raises protease inhibitor exposure."),
        q("Palivizumab prevents severe RSV in high-risk infants by:", "Providing monoclonal antibody against RSV fusion protein", ["Stimulating active vaccine memory", "Inhibiting viral DNA polymerase", "Blocking neuraminidase"], "Palivizumab gives passive protection against RSV F protein."),
        q("Interferon-alpha adverse effects commonly include:", "Flu-like symptoms and depression", ["Tendon rupture", "Kernicterus", "Red man syndrome"], "Interferons activate immune pathways and can cause systemic and neuropsychiatric toxicity."),
    ]),
    ("viral-hepatitis", "Treatment of Viral Hepatitis (HBV/HCV)", [
        q("Tenofovir suppresses HBV by inhibiting:", "Viral reverse transcriptase/DNA polymerase", ["NS5A", "Neuraminidase", "Beta-glucan synthase"], "HBV replicates through reverse transcription; nucleotide analogs inhibit polymerase."),
        q("Stopping HBV nucleos(t)ide therapy abruptly can cause:", "Severe hepatitis flare from viral rebound", ["Immediate bacterial sepsis", "Opioid withdrawal", "Torsades from QT shortening"], "HBV suppression withdrawal can lead to rebound replication and hepatic injury."),
        q("Entecavir is avoided as functional monotherapy in unrecognized HIV because it:", "Can select HIV resistance mutations", ["Activates HIV entry", "Blocks all CD4 cells", "Causes instant cure"], "HBV agents with anti-HIV activity can drive HIV resistance if ART is incomplete."),
        q("Pegylated interferon for hepatitis can be limited by:", "Depression, cytopenias, and flu-like symptoms", ["Tendon rupture", "Ototoxicity", "Kernicterus"], "Interferon has substantial systemic and psychiatric toxicity."),
        q("Sofosbuvir treats HCV by inhibiting:", "NS5B RNA-dependent RNA polymerase", ["NS3/4A only", "NS5A only", "HBV reverse transcriptase only"], "Sofosbuvir is a nucleotide analog polymerase inhibitor."),
        q("Ledipasvir and velpatasvir inhibit HCV:", "NS5A replication complex function", ["Neuraminidase", "Viral M2 channel", "Human HMG-CoA reductase"], "NS5A inhibitors are core components of modern HCV regimens."),
        q("Glecaprevir inhibits HCV:", "NS3/4A protease", ["NS5A", "HBV polymerase", "HIV integrase"], "HCV protease inhibitors block viral polyprotein processing."),
        q("HCV direct-acting antiviral regimens use combinations mainly to:", "Prevent resistance and cover viral replication steps", ["Increase bacterial killing", "Avoid all hepatic metabolism", "Replace vaccines"], "HCV therapy combines targets to achieve high cure rates and prevent escape."),
        q("Before starting HCV direct-acting antivirals, checking HBV status matters because:", "HBV reactivation can occur during HCV treatment", ["HCV drugs always cure HBV", "HBV prevents drug absorption", "HBV makes HCV a bacterium"], "HBV reactivation is a recognized risk when HCV is rapidly suppressed."),
        q("Ribavirin toxicity includes:", "Hemolytic anemia and teratogenicity", ["Ototoxicity", "Tendon rupture", "Red man syndrome"], "Ribavirin is now less commonly used but causes hemolysis and is highly teratogenic."),
    ]),
    ("antiretroviral-hiv", "Antiretroviral Agents and Treatment of HIV Infection", [
        q("Dolutegravir prevents HIV replication by inhibiting:", "Integrase strand transfer", ["Reverse transcriptase nucleotide binding only", "Viral budding only", "CCR5 binding"], "INSTIs block integration of viral DNA into host genome."),
        q("Tenofovir and emtricitabine are backbone NRTIs because they:", "Cause chain termination after phosphorylation", ["Block HIV protease", "Bind gp41", "Activate CD4"], "NRTIs are nucleos(t)ide analogs incorporated by reverse transcriptase."),
        q("Abacavir requires HLA testing because HLA-B*57:01 predicts:", "Severe hypersensitivity reaction", ["Renal Fanconi syndrome", "Tendon rupture", "Cyanide toxicity"], "HLA-B*57:01 screening prevents abacavir hypersensitivity."),
        q("Efavirenz is limited by:", "Neuropsychiatric adverse effects", ["Ototoxicity", "Kernicterus", "Nephrogenic diabetes insipidus"], "NNRTIs such as efavirenz can cause vivid dreams, dizziness, and mood effects."),
        q("Protease inhibitors are often boosted with ritonavir or cobicistat to:", "Inhibit CYP3A and increase drug exposure", ["Activate reverse transcriptase", "Prevent all resistance", "Improve renal filtration"], "Pharmacokinetic boosters raise protease inhibitor levels but increase interaction risk."),
        q("Maraviroc works only when HIV uses:", "CCR5 coreceptor", ["CXCR4 only", "Integrase only", "HBV polymerase", "Neuraminidase"], "CCR5 antagonists require tropism testing."),
        q("Enfuvirtide blocks HIV entry by targeting:", "gp41-mediated membrane fusion", ["gp120-CD4 binding only", "Integrase", "Protease"], "Enfuvirtide is a fusion inhibitor binding gp41."),
        q("Tenofovir disoproxil fumarate can cause:", "Renal proximal tubule toxicity and reduced bone density", ["Agranulocytosis only", "Red man syndrome", "Tendon rupture"], "TDF exposure can injure proximal tubules and affect bone mineral density."),
        q("ART failure with rising viral load most often requires:", "Adherence assessment and resistance testing before changing regimen", ["Stopping all drugs permanently", "Adding one active drug alone", "Using antibiotics"], "Incomplete adherence and resistance guide regimen selection."),
        q("HIV PrEP with tenofovir/emtricitabine works by:", "Maintaining intracellular NRTI levels that block early reverse transcription after exposure", ["Killing HIV in blood by antibodies", "Stimulating CD4 proliferation only", "Blocking bacterial folate"], "PrEP prevents establishment of infection when adequate drug levels are present."),
    ]),
    ("tuberculosis-mycobacteria-leprosy", "Chemotherapy of Tuberculosis and Nontuberculous Mycobacteria, Including Leprosy", [
        q("Initial active TB therapy uses multiple drugs mainly to:", "Prevent emergence of resistant mutants", ["Reduce pill count", "Avoid culture testing", "Treat only viruses"], "M. tuberculosis has high resistance potential; combination therapy protects against selection."),
        q("Isoniazid inhibits mycobacterial cell wall synthesis by blocking:", "Mycolic acid synthesis after KatG activation", ["Arabinogalactan only", "DNA gyrase", "Ergosterol"], "INH is activated by KatG and inhibits enzymes required for mycolic acids."),
        q("Pyridoxine is given with isoniazid to prevent:", "Peripheral neuropathy", ["Optic neuritis", "Red-orange secretions", "Tendon rupture"], "INH can cause vitamin B6 deficiency-related neuropathy."),
        q("Rifampin causes many drug interactions because it:", "Induces hepatic drug-metabolizing enzymes", ["Blocks CYP3A", "Chelates calcium", "Inhibits aldehyde dehydrogenase"], "Rifamycins are potent enzyme inducers."),
        q("Rifampin commonly causes:", "Orange discoloration of body fluids", ["Blue urine", "Gray baby syndrome", "Permanent anosmia"], "Rifampin can turn urine, sweat, and tears orange-red."),
        q("Ethambutol toxicity classically affects:", "Optic nerve causing decreased visual acuity and red-green color problems", ["Auditory hair cells", "Achilles tendon", "Bone marrow only"], "Ethambutol can cause optic neuritis."),
        q("Pyrazinamide is useful early in TB therapy because it:", "Has activity in acidic intracellular environments", ["Only treats extracellular staphylococci", "Blocks folate", "Binds ergosterol"], "PZA helps sterilize acidic lesions/macrophage environments."),
        q("Drug-resistant TB treatment with bedaquiline requires ECG monitoring because it can:", "Prolong QT interval", ["Cause kernicterus", "Block vitamin K", "Induce serotonin syndrome"], "Bedaquiline inhibits mycobacterial ATP synthase and may prolong QT."),
        q("Dapsone for leprosy can cause hemolysis especially in:", "G6PD deficiency", ["HLA-B*57:01 only", "Renal artery stenosis", "Achlorhydria"], "Dapsone is an oxidant sulfone and can cause hemolysis/methemoglobinemia."),
        q("Clofazimine in leprosy commonly causes:", "Skin discoloration", ["Ototoxicity", "Tendon rupture", "Kernicterus"], "Clofazimine can cause red-brown skin discoloration and GI effects."),
    ]),
    ("malaria", "Chemotherapy of Malaria", [
        q("Artemisinin-based combinations are preferred for many falciparum infections because artemisinins:", "Rapidly reduce parasite biomass", ["Only kill hypnozoites", "Prevent mosquito bites only", "Block human folate"], "Artemisinins are fast-acting blood schizonticides and are paired to reduce resistance."),
        q("Primaquine is needed to eradicate dormant liver forms of P. vivax/ovale because it kills:", "Hypnozoites", ["Only gametocytes of all species", "Only red cell rings", "Mosquito larvae"], "Primaquine/tafenoquine target latent hepatic hypnozoites."),
        q("Before primaquine, testing is needed for:", "G6PD deficiency", ["HLA-B*57:01", "CYP2C19", "Renin level"], "8-aminoquinolines can cause severe hemolysis in G6PD deficiency."),
        q("Chloroquine resistance in malaria commonly involves:", "Altered parasite food vacuole drug transport", ["Loss of human hemoglobin", "Bacterial beta-lactamase", "Viral neuraminidase"], "Transporter mutations reduce chloroquine accumulation in the parasite food vacuole."),
        q("Atovaquone-proguanil works in malaria by targeting:", "Parasite mitochondrial electron transport and folate metabolism", ["Human ribosomes", "Fungal ergosterol", "Bacterial PBPs"], "The combination attacks parasite mitochondrial function and DHFR."),
        q("Mefloquine prophylaxis is avoided in a patient with severe depression because it can cause:", "Neuropsychiatric adverse effects", ["Agranulocytosis only", "Pulmonary fibrosis", "Kernicterus"], "Mefloquine may cause vivid dreams, anxiety, depression, or psychosis."),
        q("Quinine toxicity includes cinchonism, characterized by:", "Tinnitus, headache, nausea, and visual disturbances", ["Red man syndrome", "Gray baby syndrome", "Tendon rupture"], "Cinchonism is a classic quinine/quinidine toxicity pattern."),
        q("Doxycycline malaria prophylaxis also requires counseling about:", "Photosensitivity and esophagitis prevention", ["Kernicterus in adults", "Cyanide toxicity", "Opioid withdrawal"], "Doxycycline can cause sun sensitivity and pill esophagitis."),
        q("Severe falciparum malaria is treated urgently with:", "IV artesunate", ["Oral acyclovir", "Topical nystatin", "Single-dose azithromycin only"], "Parenteral artesunate rapidly treats severe malaria."),
        q("Sulfadoxine-pyrimethamine targets parasite:", "Folate synthesis", ["Heme polymerase only", "Ergosterol", "Integrase"], "Antifolate combinations inhibit sequential folate pathway steps."),
    ]),
    ("protozoal-infections", "Chemotherapy of Protozoal Infections: Amebiasis, Giardiasis, Trichomoniasis, Trypanosomiasis, Leishmaniasis, and Other Protozoal Infections", [
        q("A patient with invasive amebic liver abscess receives metronidazole. Why add paromomycin afterward?", "To eradicate luminal intestinal cysts", ["To treat HSV coinfection", "To reverse metronidazole toxicity", "To prevent malaria hypnozoites"], "Tissue amebicides do not reliably clear luminal colonization."),
        q("Giardiasis after backpacking is treated with tinidazole or metronidazole because these drugs:", "Generate DNA-damaging radicals in anaerobic protozoa", ["Block ergosterol", "Inhibit neuraminidase", "Bind PBPs"], "Nitroimidazoles are activated in low-redox organisms such as Giardia."),
        q("Trichomoniasis treatment should include partner treatment because:", "Reinfection is common if sexual partners remain untreated", ["The drug only works in men", "It is always viral", "Partners need antimalarials"], "Sex partners require treatment to prevent ping-pong reinfection."),
        q("Toxoplasma encephalitis in AIDS is commonly treated with pyrimethamine plus sulfadiazine and leucovorin because:", "Sequential folate blockade treats parasite while leucovorin limits host toxicity", ["Leucovorin activates parasite folate", "The regimen blocks ergosterol", "It treats only bacteria"], "Leucovorin rescues host cells from antifolate marrow toxicity."),
        q("Pentamidine for Pneumocystis or trypanosomiasis can cause:", "Hypoglycemia or hyperglycemia from pancreatic toxicity", ["Tendon rupture", "Orange secretions", "Kernicterus"], "Pentamidine has notable pancreatic, renal, and cardiac toxicity."),
        q("Benznidazole treats Chagas disease by:", "Generating reactive metabolites toxic to Trypanosoma cruzi", ["Blocking viral polymerase", "Inhibiting human ACE", "Binding ergosterol only"], "Nitroheterocyclic drugs are used for T. cruzi infection."),
        q("Suramin for early African trypanosomiasis is not used for CNS disease because it:", "Penetrates the CNS poorly", ["Cannot kill bloodstream parasites", "Is only topical", "Requires viral thymidine kinase"], "Late-stage disease needs drugs with CNS activity."),
        q("Melarsoprol can treat CNS African trypanosomiasis but is feared because it:", "Can cause fatal reactive encephalopathy", ["Always causes tooth staining", "Causes red man syndrome only", "Induces kernicterus"], "Arsenical toxicity makes melarsoprol dangerous but sometimes necessary."),
        q("Miltefosine for leishmaniasis is limited by:", "Teratogenicity and gastrointestinal toxicity", ["No oral absorption", "Universal resistance", "Inability to enter macrophages"], "Miltefosine is oral but teratogenic and causes GI adverse effects."),
        q("Nitazoxanide can treat Cryptosporidium diarrhea in immunocompetent hosts by:", "Interfering with anaerobic energy metabolism", ["Blocking beta-lactamase", "Inhibiting HIV integrase", "Activating H1 receptors"], "Nitazoxanide has activity against several protozoa through pyruvate:ferredoxin oxidoreductase-linked pathways."),
    ]),
    ("helminth-infections", "Chemotherapy of Helminth Infections", [
        q("Albendazole treats many nematodes by:", "Inhibiting microtubule polymerization through beta-tubulin binding", ["Blocking acetylcholinesterase", "Opening chloride channels only", "Inhibiting neuraminidase"], "Benzimidazoles impair parasite microtubules and glucose uptake."),
        q("Ivermectin treats strongyloidiasis and onchocerciasis by:", "Activating glutamate-gated chloride channels causing paralysis", ["Blocking parasite tubulin", "Inhibiting folate", "Binding ergosterol"], "Ivermectin increases chloride influx in susceptible parasites."),
        q("Praziquantel treats schistosomiasis because it:", "Increases parasite calcium permeability causing contraction and tegument damage", ["Blocks glucose uptake only", "Inhibits viral polymerase", "Activates human beta receptors"], "Praziquantel is active against schistosomes and many cestodes."),
        q("Diethylcarbamazine is avoided in heavy onchocerciasis because rapid microfilarial killing can:", "Trigger severe inflammatory eye and skin reactions", ["Cause thyroid ablation", "Block vitamin K", "Induce tendon rupture"], "Killing microfilariae can provoke intense host inflammation."),
        q("Pyrantel pamoate treats pinworm by:", "Causing depolarizing neuromuscular paralysis of worms", ["Inhibiting DNA gyrase", "Blocking ergosterol", "Neutralizing stomach acid"], "Pyrantel is a nicotinic agonist that paralyzes intestinal nematodes."),
        q("Niclosamide historically treats tapeworms by:", "Inhibiting parasite oxidative phosphorylation locally in the gut", ["Treating tissue cysticercosis reliably", "Blocking human folate", "Opening chloride channels"], "Niclosamide is a luminal cestocide with poor absorption."),
        q("Neurocysticercosis therapy with albendazole often includes corticosteroids because:", "Parasite killing can provoke CNS inflammation and edema", ["Steroids kill cysticerci directly", "Albendazole causes adrenal crisis", "Steroids prevent all seizures alone"], "Antihelminthic treatment can worsen inflammatory edema around dying larvae."),
        q("Strongyloides hyperinfection risk rises before steroids in undiagnosed infection, so treatment uses:", "Ivermectin", ["Praziquantel only", "Oseltamivir", "Fluconazole"], "Ivermectin is first-line for strongyloidiasis and critical in hyperinfection."),
        q("Mebendazole is effective for enterobiasis, but household reinfection is prevented by:", "Treating close contacts and hygiene measures", ["Avoiding all carbohydrates", "Adding antivirals", "Using antacids"], "Pinworm spreads easily; repeat dosing and household hygiene reduce recurrence."),
        q("Triclabendazole is preferred for fascioliasis because it has activity against:", "Liver flukes", ["Pinworm only", "Malaria hypnozoites", "Candida"], "Triclabendazole is the key drug for Fasciola hepatica infection."),
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
            questions.append({**BASE, "id": f"infectious-chemo-{slug}-{question_index:02d}", "topic": topic, "difficulty": "moderate" if question_index <= 3 else "high" if question_index <= 8 else "very high", "prompt": row["prompt"], "options": options, "answerIndex": answer_index, "answer": row["answer"], "explanation": row["explanation"]})

    data = json.loads(DATA.read_text(encoding="utf-8-sig"))
    data["questions"] = [x for x in data.get("questions", []) if not (x.get("subjectId") == "pharmacology" and x.get("chapterTitle") == CHAPTER)] + questions

    if len(TOPICS) != 13 or len(questions) != 130:
        raise AssertionError(f"Expected 13 topics and 130 questions, got {len(TOPICS)} and {len(questions)}")
    if len({x["id"] for x in questions}) != 130:
        raise AssertionError("Duplicate question IDs")
    if any(x["answer"] != x["options"][x["answerIndex"]] for x in questions):
        raise AssertionError("Bad answer index")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Added {len(questions)} questions across {len(TOPICS)} topics for {CHAPTER}.")


if __name__ == "__main__":
    main()
