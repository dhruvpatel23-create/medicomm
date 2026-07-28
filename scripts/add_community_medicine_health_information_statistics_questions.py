import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Health Information and Basic Medical Statistics"
CHAPTER_ORDER = 16
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
    ("health-information", "Health Information System", 1, [
        q("A health information system is used to collect, process, analyse and use data for what?", "Health planning and management", ["Hospital decoration", "Drug taste improvement", "Road construction only"], "Health information supports planning, monitoring, evaluation and decision-making."),
        q("Good health information should be reliable, timely, complete and what?", "Relevant", ["Secret", "Decorative", "Expensive only"], "Useful information must be accurate, timely, complete and relevant to decisions."),
        q("Vital registration mainly records births, deaths and what?", "Causes of death", ["Only hospital bills", "Only school marks", "Only vaccine colour"], "Vital registration provides legal and demographic information including cause-specific mortality."),
        q("A district officer uses monthly malaria case reports to detect a sudden rise. Which function of health information is this?", "Surveillance", ["Randomization", "Blinding", "Drug dispensing"], "Routine reporting can detect changes in disease occurrence.", True),
        q("Census provides information on size, composition and distribution of what?", "Population", ["Only bacteria", "Only hospital beds", "Only medicines"], "Census is a major source of population denominator data."),
        q("Notification of disease means reporting specified diseases to whom?", "Public health authorities", ["Newspaper only", "Patient relatives only", "Pharmacy vendors"], "Notifiable disease reporting enables public health action."),
        q("Medical certification of cause of death improves the quality of what statistics?", "Mortality statistics", ["Weather statistics", "Drug stock statistics", "School attendance only"], "Accurate cause-of-death certification improves mortality data."),
        q("A doctor writes cardiac arrest as the only cause on a death certificate after long tuberculosis illness. What is the main problem?", "Immediate mode of death is recorded instead of underlying cause", ["Too many diagnoses", "No signature needed", "Excess demographic detail"], "Death certification should capture the disease sequence and underlying cause.", True),
        q("Health management information systems are especially useful for monitoring service coverage and what?", "Programme performance", ["Only staff birthdays", "Only wall paint", "Only patient handwriting"], "HMIS data help track indicators, services and programme gaps."),
        q("If immunization coverage reports are incomplete from several subcentres, what data quality problem is present?", "Incomplete reporting", ["Perfect validity", "Excess sensitivity", "Random allocation"], "Missing reports reduce reliability of district coverage estimates.", True),
    ]),
    ("data-presentation", "Data, Tables and Diagrams", 2, [
        q("Data collected for a specific study for the first time are called what?", "Primary data", ["Secondary data", "Tertiary prevention", "Nominal scale only"], "Primary data are collected directly for the current purpose."),
        q("Hospital records and census reports used for analysis are examples of what?", "Secondary data", ["Primary data always", "Experimental allocation", "Clinical examination only"], "Secondary data already exist before the current analysis."),
        q("Qualitative data describe attributes such as sex, blood group and what?", "Disease status", ["Weight in kilograms only", "Height in centimetres only", "Serum sodium value"], "Qualitative variables are categories rather than numerical measurements."),
        q("Birth weight measured in kilograms is which type of variable?", "Quantitative variable", ["Nominal variable only", "Ordinal category only", "Not data"], "Weight is a numerical measurement and is quantitative.", True),
        q("A frequency distribution shows how observations are arranged according to what?", "Values or classes", ["Doctor names only", "Hospital floors", "Drug brands only"], "Frequency tables summarize how often each value or class occurs."),
        q("A bar diagram is most suitable for presenting what type of data?", "Discrete or categorical data", ["Continuous frequency distribution only", "Survival time curve only", "Correlation only"], "Bar charts compare separate categories."),
        q("A histogram is used to display frequency distribution of what?", "Continuous data", ["Nominal categories only", "Family names", "Hospital departments only"], "Histograms show frequencies across continuous class intervals."),
        q("A health worker compares malaria cases in four villages by village name. Which diagram is suitable?", "Bar diagram", ["Histogram", "Scatter diagram", "Life table"], "Village-wise counts are categorical comparisons and suit a bar diagram.", True),
        q("A pie chart is used to show parts of a whole as what?", "Proportions or percentages", ["Standard deviations only", "Confidence limits only", "Regression equations"], "Pie diagrams display component percentages of a total."),
        q("A scatter diagram is useful for studying relation between two what?", "Quantitative variables", ["Death certificates only", "Nominal labels only", "Treatment guidelines"], "Scatter plots show paired numerical observations and possible correlation.", True),
    ]),
    ("central-tendency-variation", "Averages and Variation", 3, [
        q("The arithmetic mean is calculated by dividing the sum of observations by what?", "Number of observations", ["Highest value", "Lowest value", "Range only"], "Mean equals total divided by the number of observations."),
        q("The median is the value that divides an ordered series into how many equal parts?", "Two equal parts", ["Three equal parts", "Four equal parts", "Ten equal parts"], "Median is the middle value after arranging observations."),
        q("The mode is the observation that occurs with what?", "Highest frequency", ["Lowest value", "Largest standard deviation", "Zero frequency"], "Mode is the most frequent value."),
        q("In a highly skewed income distribution, which average is usually more appropriate?", "Median", ["Mean always", "Mode never", "Range"], "Median is less affected by extreme values than mean.", True),
        q("Range is calculated as the difference between the highest value and what?", "Lowest value", ["Mean", "Median", "Mode"], "Range is the simplest measure of dispersion."),
        q("Standard deviation measures dispersion of observations around which value?", "Mean", ["Mode only", "Sample size only", "P value"], "Standard deviation describes spread around the mean."),
        q("Coefficient of variation is useful for comparing variability between series because it is what?", "Relative measure of dispersion", ["Measure of central tendency", "Type of graph", "Sampling method"], "CV expresses standard deviation as a percentage of the mean."),
        q("Two clinics have mean waiting times of 20 minutes, but one has much larger standard deviation. What does this indicate?", "Waiting times are more variable in that clinic", ["Mean is impossible", "No patients attended", "Only categorical data"], "A larger SD means more spread around the mean.", True),
        q("Percentiles divide ordered data into how many equal parts?", "Hundred", ["Two", "Four", "Ten"], "Percentiles divide observations into 100 equal parts."),
        q("A child's weight is at the 3rd percentile for age. What does this primarily indicate?", "Low position compared with reference population", ["Exactly 3 kg weight", "No need for assessment", "Always genetic disease"], "Percentiles show relative position in a reference distribution.", True),
    ]),
    ("probability-tests", "Probability and Tests of Significance", 4, [
        q("Probability expresses the chance of occurrence of an event and ranges from zero to what?", "One", ["Ten", "Hundred", "Infinity"], "Probability ranges from 0 to 1."),
        q("The null hypothesis usually states that there is what?", "No real difference or association", ["Always a large effect", "Only clinical cure", "No sample size"], "Statistical tests commonly begin with a hypothesis of no difference."),
        q("A p value less than the chosen significance level suggests rejecting which hypothesis?", "Null hypothesis", ["Alternative hypothesis always", "Study population", "Sampling frame"], "A small p value indicates the data are unlikely under the null hypothesis."),
        q("A trial reports p < 0.05 for difference in cure rates. What does this usually mean?", "The difference is statistically significant at 5 percent level", ["The treatment is always clinically important", "The study has no bias", "The sample is census"], "Statistical significance means chance is an unlikely explanation at the chosen level.", True),
        q("Type I error means rejecting a null hypothesis when it is actually what?", "True", ["False", "Not stated", "Clinical"], "Type I error is a false positive conclusion."),
        q("Type II error means failing to reject a null hypothesis when it is actually what?", "False", ["True", "Perfect", "Measured"], "Type II error is a false negative conclusion."),
        q("The chi-square test is commonly used to test association between what type of variables?", "Categorical variables", ["Only means of two groups", "Only paired blood pressure values", "Only survival time"], "Chi-square compares observed and expected frequencies in categories."),
        q("A researcher compares anaemia prevalence between boys and girls. Which test is commonly appropriate?", "Chi-square test", ["Paired t-test only", "Correlation coefficient only", "ANOVA always"], "Sex and anaemia status are categorical variables.", True),
        q("Student's t-test is commonly used to compare means when data are approximately what?", "Normally distributed", ["Only nominal", "Only ordinal", "Always censored"], "The t-test compares means under normality assumptions."),
        q("A study compares mean haemoglobin between two independent treatment groups. Which test is commonly used?", "Unpaired t-test", ["Chi-square test only", "Median test always", "Life table only"], "An unpaired t-test compares means between two independent groups.", True),
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
                "id": f"community-medicine-health-information-statistics-{slug}-{i:02d}",
                "topic": topic,
                "topicTitle": topic,
                "topicOrder": order,
                "options": opts,
                "answerIndex": opts.index(ans),
                "answer": ans,
            })
    return out


def validate(qs):
    if len(qs) != 40:
        raise ValueError(f"Expected 40, got {len(qs)}")
    if len({q["id"] for q in qs}) != 40:
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
