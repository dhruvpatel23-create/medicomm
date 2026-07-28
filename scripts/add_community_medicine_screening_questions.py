import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Screening for Disease"
CHAPTER_ORDER = 2
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
    ("screening-for-disease", "Screening for Disease", 1, [
        q("Screening is best defined as the presumptive identification of unrecognized disease by which method?", "Tests or examinations applied rapidly to apparently healthy people", ["Definitive treatment of confirmed cases", "Autopsy examination only", "Random allocation to a drug trial"], "Screening separates apparently well persons who probably have disease from those who probably do not."),
        q("A screening test should ideally be applied to which group?", "Apparently healthy persons at risk", ["Only terminally ill patients", "Only confirmed cases after diagnosis", "Only hospital staff"], "Screening targets people without recognized symptoms but with possible risk."),
        q("The purpose of screening is mainly to achieve what?", "Earlier detection and better outcome", ["Replace all diagnostic tests", "Avoid follow-up confirmation", "Increase disease duration"], "Screening is useful when early detection leads to effective intervention."),
        q("A woman with no breast symptoms undergoes mammography as part of a programme. What is this activity?", "Screening", ["Clinical diagnosis", "Tertiary prevention only", "Case fatality measurement"], "A test applied to an apparently healthy person for early disease detection is screening.", True),
        q("Sensitivity of a screening test means its ability to correctly identify which persons?", "Those who truly have the disease", ["Those who truly do not have disease", "Those who refuse testing", "Those already cured"], "Sensitivity is the proportion of diseased persons who test positive."),
        q("Specificity of a screening test means its ability to correctly identify which persons?", "Those who truly do not have the disease", ["Those who truly have disease", "Only severe cases", "Only vaccinated persons"], "Specificity is the proportion of non-diseased persons who test negative."),
        q("A highly sensitive screening test is especially useful when the programme wants to minimize which error?", "False negatives", ["False positives only", "Sampling frame errors", "Observer blinding"], "High sensitivity reduces missed cases."),
        q("A blood bank uses a very sensitive HIV screening test. What is the main reason?", "To avoid missing infected donations", ["To estimate birth rate", "To measure herd immunity", "To confirm AIDS staging"], "For serious transmissible disease, missing true positives is especially dangerous.", True),
        q("Positive predictive value is the proportion of test-positive persons who actually have what?", "Disease", ["No disease", "Prior vaccination", "Complete immunity"], "PPV answers: if the test is positive, how likely is disease present?"),
        q("Negative predictive value is the proportion of test-negative persons who actually are what?", "Disease-free", ["Diseased", "Exposed", "Dead from disease"], "NPV answers: if the test is negative, how likely is disease absent?"),
        q("When disease prevalence falls, what usually happens to positive predictive value?", "It decreases", ["It always increases", "It becomes equal to sensitivity", "It becomes unrelated to false positives"], "For rare disease, a larger share of positive tests may be false positives."),
        q("A rare cancer is screened in a low-risk population and many positives are false alarms. Which test property is most affected by low prevalence?", "Positive predictive value", ["Sensitivity", "Biological half-life", "Incubation period"], "Low prevalence reduces PPV even when sensitivity and specificity are acceptable.", True),
        q("Reliability of a screening test refers mainly to what?", "Consistency or repeatability of results", ["Ability to cure disease", "Cost of treatment only", "Presence of symptoms"], "A reliable test gives consistent results on repeated application."),
        q("Validity of a screening test refers mainly to what?", "Ability to distinguish diseased from non-diseased persons", ["Popularity of the test", "Ease of transport only", "Number of staff trained"], "Validity concerns accuracy, commonly expressed by sensitivity and specificity."),
        q("Lead-time bias makes survival after screening appear longer because diagnosis is made when?", "Earlier in the natural history of disease", ["After death", "Only after symptoms become severe", "Only after treatment failure"], "Earlier diagnosis can lengthen measured survival time without changing time of death."),
        q("A screening programme reports improved 5-year survival but mortality rate is unchanged. Which bias may explain this?", "Lead-time bias", ["Recall bias only", "Berkson bias", "Ecological fallacy"], "Screening can appear to improve survival by advancing diagnosis time without reducing mortality.", True),
        q("A disease suitable for screening should have which characteristic?", "Recognizable latent or early asymptomatic stage", ["No treatment available", "Extremely rare with no risk group", "Diagnosis possible only at autopsy"], "Screening is worthwhile when disease can be detected before symptoms and treated effectively.", True),
        q("The screening test itself should be acceptable because this mainly improves what?", "Participation and coverage", ["Virulence", "Case fatality", "Mutation rate"], "Unacceptable tests reduce uptake and programme effectiveness."),
        q("Multiphasic screening means applying what?", "Two or more screening tests together", ["Only one confirmatory diagnostic test", "Treatment without diagnosis", "Autopsy after death"], "Multiphasic screening uses multiple tests in one encounter."),
        q("After a positive screening test, the next appropriate step is usually what?", "Diagnostic confirmation", ["Immediate lifelong treatment without confirmation", "Ignore the result", "Remove the person from population statistics"], "Screening tests are presumptive and positive results need diagnostic work-up.", True),
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
                "id": f"community-medicine-screening-{slug}-{i:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": order,
                "options": opts,
                "answerIndex": opts.index(ans),
                "answer": ans,
            })
    return out


def validate(qs):
    if len(qs) != 20:
        raise ValueError(f"Expected 20, got {len(qs)}")
    if len({q["id"] for q in qs}) != 20:
        raise ValueError("Duplicate IDs")
    if sum("clinical" in q.get("tags", []) for q in qs) < 6:
        raise ValueError("Expected at least 6 clinical/application questions")
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
    print("- Screening for Disease: 20 questions")


if __name__ == "__main__":
    main()
