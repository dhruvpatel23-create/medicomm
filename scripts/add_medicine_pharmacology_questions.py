import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "Pharmacology"
CHAPTER_ORDER = 3
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
    ("Pharmacokinetics and Dose Individualization", [
        q("Bioavailability refers to the fraction of administered drug that", "Reaches systemic circulation unchanged", ["Binds plasma albumin irreversibly", "Is excreted in bile", "Crosses only the blood-brain barrier"], "Bioavailability determines the amount of active drug reaching systemic circulation."),
        q("First-pass metabolism most strongly reduces bioavailability after", "Oral administration", ["Intravenous bolus", "Intra-arterial infusion", "Intrathecal injection"], "Orally absorbed drugs pass through gut wall and liver before systemic circulation."),
        q("An elderly patient develops digoxin toxicity after dehydration and acute kidney injury. The main pharmacokinetic reason is", "Reduced renal clearance increases drug accumulation", ["Increased first-pass metabolism", "Reduced receptor affinity", "Loss of oral absorption"], "Digoxin is substantially renally cleared, so AKI raises serum levels and toxicity risk.", True),
        q("Volume of distribution is increased when a drug", "Leaves plasma extensively and distributes into tissues", ["Remains only inside albumin-bound plasma", "Is never absorbed", "Is eliminated before distribution"], "Large apparent volume of distribution reflects extensive tissue binding or partitioning."),
        q("The loading dose of a drug is mainly determined by", "Target concentration and volume of distribution", ["Renal clearance alone", "Half-life only", "Urine pH alone"], "Loading dose quickly fills the apparent distribution space to achieve a target level.", True),
        q("Maintenance dose is most directly related to", "Drug clearance and target steady-state concentration", ["Tablet color", "Only receptor number", "Route label alone"], "Maintenance dosing replaces drug removed per unit time."),
        q("A patient receiving vancomycin has rising trough levels after creatinine doubles. The best response is to", "Extend the dosing interval or reduce dose based on renal function and levels", ["Give larger doses because infection is severe", "Ignore levels if fever persists", "Switch to an oral placebo"], "Renally cleared drugs need dose adjustment and monitoring when kidney function worsens.", True),
        q("Steady state is usually reached after about", "Four to five half-lives", ["One absorption period", "One minute for all drugs", "Ten years for all drugs"], "Repeated dosing approaches steady state over several elimination half-lives."),
        q("A drug with zero-order elimination has", "A constant amount eliminated per unit time", ["A constant fraction eliminated per unit time", "No saturation possible", "Elimination independent of dose at all concentrations"], "Zero-order kinetics occur when elimination pathways are saturated."),
        q("A patient on phenytoin has disproportionate toxicity after a small dose increase. The explanation is", "Saturable metabolism causing nonlinear rise in concentration", ["Complete absence of absorption", "Immediate renal excretion", "Loss of protein binding only"], "Phenytoin can show capacity-limited metabolism, so small dose changes may sharply raise levels.", True),
    ]),
    ("Pharmacodynamics, Adverse Effects and Interactions", [
        q("Potency refers to the", "Dose or concentration needed to produce a given effect", ["Maximum effect a drug can produce", "Duration of patent protection", "Number of metabolites only"], "Potency compares how much drug is required for an effect."),
        q("Efficacy refers to the", "Maximum effect achievable by a drug", ["Fraction excreted unchanged", "Tablet dissolution time only", "Cost of therapy"], "Efficacy reflects maximal response, independent of dose needed to reach it."),
        q("A patient taking nitrates for angina develops severe hypotension after sildenafil. The mechanism is", "Additive cyclic GMP-mediated vasodilation", ["Reduced renal sodium loss", "Increased platelet production", "Dopamine receptor blockade"], "PDE-5 inhibitors amplify nitrate-mediated vasodilation and can cause dangerous hypotension.", True),
        q("A competitive antagonist shifts an agonist dose-response curve", "To the right with preserved maximum response if enough agonist is present", ["Downward with no receptor binding", "Left with higher potency", "Into a straight vertical line"], "Surmountable competitive antagonism reduces apparent potency but not maximal effect.", True),
        q("A partial agonist has lower intrinsic activity than a full agonist and can", "Antagonize a full agonist in the same receptor system", ["Always produce maximal tissue response", "Bind only enzymes", "Never activate receptors"], "Partial agonists occupy receptors but produce submaximal activation."),
        q("Idiosyncratic drug reactions are usually", "Unpredictable reactions not explained by usual pharmacologic action", ["Expected dose-dependent effects", "Always beneficial", "Proof of overdose"], "Idiosyncratic reactions are uncommon and patient-specific."),
        q("A patient on warfarin starts trimethoprim-sulfamethoxazole and presents with high INR and bleeding. The interaction is best described as", "Reduced warfarin metabolism and increased anticoagulant effect", ["Reduced warfarin absorption only", "Increased vitamin K synthesis", "Direct platelet transfusion"], "Several antibiotics inhibit warfarin metabolism or alter vitamin K balance, raising INR.", True),
        q("Therapeutic index compares", "Toxic dose to effective dose", ["Oral dose to intravenous dose", "Half-life to bioavailability", "Protein binding to tissue binding"], "A narrow therapeutic index means small concentration changes can cause toxicity."),
        q("A type A adverse drug reaction is generally", "Predictable and dose related", ["Never related to dose", "Always immune mediated", "Impossible to prevent"], "Type A reactions are augmented pharmacologic effects and often dose dependent."),
        q("A patient develops urticaria, wheeze and hypotension minutes after penicillin injection. The reaction is", "Immediate IgE-mediated anaphylaxis", ["Type A predictable toxicity", "Delayed renal clearance", "Therapeutic tolerance"], "Rapid multisystem allergic reaction after exposure is anaphylaxis and needs immediate treatment.", True),
    ]),
    ("Rational Prescribing and Special Populations", [
        q("Rational prescribing begins with", "Defining the therapeutic objective and choosing the safest effective option", ["Choosing the newest drug automatically", "Avoiding diagnosis", "Prescribing before history"], "Good prescribing links diagnosis, treatment goal, patient factors and evidence."),
        q("Medication reconciliation is important because it", "Detects omissions, duplications, interactions and incorrect doses across care transitions", ["Replaces clinical examination", "Eliminates the need for monitoring", "Applies only to surgery"], "Transitions of care are high-risk times for medication errors."),
        q("An older patient is admitted with confusion after starting a sedating antihistamine. The best interpretation is", "Anticholinergic adverse effect is more likely in older adults", ["Normal aging without drug contribution", "Mandatory meningitis", "Improved cognition from antihistamine"], "Older adults are vulnerable to anticholinergic delirium, urinary retention and falls.", True),
        q("Prescribing in pregnancy should consider", "Gestational age, fetal risk, maternal benefit and safer alternatives", ["Only maternal convenience", "That all drugs are harmless after implantation", "That no treatment is ever allowed"], "Risk-benefit assessment changes with trimester and disease severity."),
        q("Teratogenic risk is greatest for many structural malformations during", "Organogenesis in the first trimester", ["Late adulthood", "Before conception only", "After delivery"], "Major organ formation occurs early in pregnancy."),
        q("A pregnant patient has severe hypertension. The safest prescribing principle is to", "Treat maternal disease with agents known to be safer in pregnancy", ["Stop all antihypertensives regardless of BP", "Use ACE inhibitors routinely", "Ignore fetal and maternal risk"], "Untreated severe maternal hypertension is dangerous, but drug choice must avoid known fetal harm.", True),
        q("In liver disease, drug toxicity may increase because of impaired", "Metabolism, protein synthesis and biliary excretion", ["Bone conduction", "Retinal refraction", "Sweat gland number only"], "Hepatic dysfunction alters clearance and free drug concentration."),
        q("Polypharmacy is clinically important because it increases", "Drug interactions, adverse effects and prescribing cascades", ["Diagnostic certainty always", "Drug efficacy for every medicine", "Bioavailability of all drugs"], "More medicines create more opportunities for harm and interactions."),
        q("A patient has persistent cough after starting enalapril for hypertension. The appropriate change is", "Switch to an angiotensin receptor blocker if RAAS blockade is still desired", ["Double the ACE inhibitor dose", "Add codeine indefinitely", "Ignore because drug cough is impossible"], "ACE inhibitor cough often resolves after stopping the ACE inhibitor; ARBs avoid bradykinin accumulation.", True),
        q("When stopping long-term glucocorticoids, tapering is needed mainly to prevent", "Adrenal insufficiency from hypothalamic-pituitary-adrenal suppression", ["Immediate drug allergy", "Increased first-pass effect", "Permanent receptor activation"], "Chronic steroids suppress endogenous cortisol production, so abrupt withdrawal can be dangerous.", True),
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
                "id": f"medicine-pharmacology-{topic_slug}-{question_order:02d}",
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
    if len(questions) != 30:
        raise AssertionError(f"Expected 30 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 30:
        raise AssertionError("Duplicate pharmacology question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 30 Medicine Pharmacology questions.")


if __name__ == "__main__":
    main()
