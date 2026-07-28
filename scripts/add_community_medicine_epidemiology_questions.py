import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Principles of Epidemiology and Epidemiological Methods"
CHAPTER_ORDER = 1
BASE = {
    "subjectId": "community-medicine",
    "subjectTitle": "Community Medicine",
    "chapterTitle": CHAPTER,
    "source": "ai",
    "sourcePdf": "parks 1.pdf",
    "chapterOrder": CHAPTER_ORDER,
    "imageUrls": [],
}


def q(prompt, answer, wrong, explanation, clinical=False):
    return {
        "prompt": prompt,
        "options": [answer, *wrong],
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": "moderate",
        "tags": ["clinical"] if clinical else [],
    }


TOPICS = [
    ("epidemiology-concepts", "Basic Concepts and Measures in Epidemiology", 1, [
        q("Which definition best describes epidemiology?", "Study of distribution and determinants of health-related states in populations", ["Treatment of individual patients only", "Study of hospital architecture", "Laboratory diagnosis of all infections"], "Epidemiology studies patterns, causes and control of health events in populations."),
        q("Incidence measures which aspect of disease occurrence?", "New cases occurring in a population during a specified period", ["All existing cases at one point", "Deaths among diagnosed cases only", "Number of hospital beds"], "Incidence quantifies new disease occurrence over time."),
        q("Prevalence is most directly influenced by incidence and what?", "Duration of disease", ["Specificity only", "Randomization only", "Blinding only"], "Prevalence is approximately incidence multiplied by average duration in stable conditions."),
        q("In a village of 10,000 people, 50 new cases of hepatitis A occur in June. Which measure is being calculated?", "Incidence", ["Point prevalence", "Case fatality rate", "Standard error"], "New cases over a period in a defined population represent incidence.", True),
        q("The numerator of a rate is usually included in what?", "Denominator population at risk", ["A separate unrelated population", "Only the exposed group always", "Only deaths from all causes"], "A valid rate relates events to the population at risk."),
        q("Case fatality rate indicates what?", "Proportion of diagnosed cases who die from the disease", ["Risk of developing disease among healthy people", "Screening test sensitivity", "Population birth rate"], "CFR measures severity or killing power among cases."),
        q("A carrier state is important epidemiologically because the person may do what?", "Transmit infection without obvious disease", ["Always become immune immediately", "Never shed organisms", "Only develop cancer"], "Carriers can maintain transmission despite absent or mild symptoms."),
        q("During a measles outbreak, 90 susceptible children are exposed and 72 become ill. Which measure is 80%?", "Attack rate", ["Infant mortality rate", "Point prevalence", "Specificity"], "Attack rate is cumulative incidence in an outbreak-exposed group.", True),
        q("Endemic disease refers to disease that is what?", "Constantly present at expected frequency in a population", ["Always imported from abroad", "Present only after disasters", "Always fatal"], "Endemicity means usual presence in a defined area or group."),
        q("A sudden excess of dengue cases above expected seasonal levels in a town is called what?", "Epidemic", ["Sporadic disease", "Eradication", "Elimination"], "An epidemic is occurrence clearly in excess of normal expectancy.", True),
    ]),
    ("study-designs-methods", "Epidemiological Study Designs and Methods", 2, [
        q("A descriptive epidemiological study primarily answers which question?", "Who, where and when disease occurs", ["Whether randomization succeeded", "Which drug is superior", "Exact cellular receptor mutation"], "Descriptive studies characterize distribution by person, place and time."),
        q("A case-control study starts with people selected on the basis of what?", "Disease status", ["Exposure status", "Random treatment assignment", "Birth cohort only"], "Case-control studies compare prior exposure among cases and controls."),
        q("A cohort study starts by classifying participants according to what?", "Exposure status", ["Outcome status", "Hospital ward only", "Blood group only"], "Cohort studies follow exposed and unexposed groups for outcome occurrence."),
        q("Smokers and non-smokers are followed for 10 years to compare lung cancer incidence. Which design is this?", "Cohort study", ["Case-control study", "Cross-sectional study", "Case report"], "Exposure groups followed over time indicate a cohort design.", True),
        q("Odds ratio is the usual measure of association in which analytical study?", "Case-control study", ["Randomized trial only", "Ecological map only", "Vital registration only"], "Case-control studies usually estimate association with odds ratio."),
        q("Relative risk is most directly estimated from which study design?", "Cohort study", ["Case-control study only", "Case series", "Single case report"], "Cohort designs can directly estimate incidence and risk ratio."),
        q("A cross-sectional study measures exposure and disease at what point?", "Same time", ["After randomization only", "Only after death", "Before study population is defined"], "Cross-sectional studies capture a snapshot of exposure and outcome."),
        q("A survey finds current hypertension prevalence and salt intake in adults on one visit. Which design is it?", "Cross-sectional study", ["Prospective cohort", "Case-control study", "Community trial"], "Exposure and outcome measured simultaneously indicate cross-sectional design.", True),
        q("Randomization in an intervention trial mainly helps achieve what?", "Comparable groups by distributing known and unknown confounders", ["Guaranteed absence of bias", "Higher prevalence", "Longer disease duration"], "Randomization reduces selection bias and confounding."),
        q("A new vaccine is allocated by random assignment and disease rates are compared later. Which design is this?", "Randomized controlled trial", ["Ecological study", "Case series", "Descriptive survey"], "Random allocation to intervention groups defines an RCT.", True),
    ]),
    ("bias-screening-causation", "Bias, Causation, Screening and Investigation of Epidemics", 3, [
        q("Confounding occurs when an observed association is distorted by what?", "A third factor related to both exposure and outcome", ["Perfect randomization", "High sensitivity only", "Short incubation period"], "A confounder is associated with exposure and independently affects outcome."),
        q("Selection bias results mainly from systematic error in what?", "Choosing or retaining study participants", ["Measuring atmospheric pressure", "Calculating birth weight", "Staining blood smears"], "Selection bias arises when study groups differ due to selection processes."),
        q("Recall bias is especially important in which study design?", "Case-control study", ["Double-blind randomized trial only", "Census enumeration only", "Vital registration"], "Cases may remember past exposures differently from controls."),
        q("Mothers of malformed babies remember drug exposure more completely than mothers of healthy babies. Which bias is likely?", "Recall bias", ["Lead-time bias", "Berkson bias only", "Random error only"], "Differential memory of past exposure is recall bias.", True),
        q("Sensitivity of a screening test measures its ability to identify whom?", "People who truly have the disease", ["People truly without disease", "Only exposed persons", "Only fatal cases"], "Sensitivity is the true-positive proportion among diseased individuals."),
        q("Specificity of a screening test measures its ability to identify whom?", "People who truly do not have the disease", ["All people with disease", "Only vaccinated persons", "Only severe cases"], "Specificity is the true-negative proportion among non-diseased individuals."),
        q("For rare diseases, a positive screening test is more likely to be false positive when which value is low?", "Positive predictive value", ["Sensitivity only", "Incidence density", "Attack rate"], "PPV is strongly affected by disease prevalence."),
        q("A screening camp uses a highly sensitive test first because the programme wants to minimize what?", "False negatives", ["False positives only", "Sample size", "Disease duration"], "High sensitivity helps rule out disease and reduces missed cases.", True),
        q("Temporal association is essential for causation because exposure must occur when?", "Before the outcome", ["After the outcome", "Only during treatment", "Only after death"], "A cause must precede its effect."),
        q("In a food poisoning outbreak, the first step after confirming diagnosis is usually to do what?", "Define cases and describe by time, place and person", ["Start a randomized trial", "Ignore mild cases", "Calculate national census"], "Outbreak investigation begins with case definition and descriptive epidemiology.", True),
    ]),
]


def build():
    out = []
    for slug, topic, order, rows in TOPICS:
        for i, row in enumerate(rows, 1):
            shift = (order + i) % 4
            opts = row["options"][shift:] + row["options"][:shift]
            ans = row["answer"]
            out.append({
                **BASE,
                **row,
                "id": f"community-medicine-epidemiology-{slug}-{i:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": order,
                "options": opts,
                "answerIndex": opts.index(ans),
                "answer": ans,
            })
    return out


def validate(qs):
    if len(qs) != 30:
        raise ValueError(f"Expected 30, got {len(qs)}")
    if len({q["id"] for q in qs}) != 30:
        raise ValueError("Duplicate IDs")
    for _, topic, _, _ in TOPICS:
        topic_qs = [q for q in qs if q["topic"] == topic]
        clinical = sum("clinical" in q.get("tags", []) for q in topic_qs)
        if len(topic_qs) != 10 or clinical < 3:
            raise ValueError(f"{topic}: {len(topic_qs)} questions, {clinical} clinical")
    for item in qs:
        if item["answer"] != item["options"][item["answerIndex"]]:
            raise ValueError(item["id"])


def update(path, qs):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    ids = {q["id"] for q in qs}
    data["questions"] = [q for q in data.get("questions", []) if q.get("id") not in ids] + qs
    data["questions"].sort(key=lambda q: q.get("id", ""))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    qs = build()
    validate(qs)
    for path in DATA_PATHS:
        update(path, qs)
        print(f"Added {len(qs)} community medicine questions to {path}.")
    for _, topic, _, _ in TOPICS:
        print(f"- {topic}: 10 questions")


if __name__ == "__main__":
    main()
