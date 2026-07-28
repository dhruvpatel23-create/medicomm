import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Demography and Family Planning"
CHAPTER_ORDER = 6
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
    ("demographic-indicators", "Demographic Indicators and Population Dynamics", 1, [
        q("Demography is best described as the scientific study of what?", "Human population", ["Hospital buildings", "Only bacteria", "Drug metabolism"], "Demography studies size, composition, distribution and changes in human populations."),
        q("Crude birth rate is expressed as number of live births per year per how many population?", "1000 mid-year population", ["100 population", "10,000 pregnant women", "100,000 live births"], "CBR is live births in a year per 1000 mid-year population."),
        q("Crude death rate is calculated using deaths in a year divided by which denominator?", "Mid-year population", ["Only live births", "Only pregnant women", "Only hospital admissions"], "CDR uses total deaths per 1000 mid-year population."),
        q("A district with 25,000 live births in a population of 10 lakh has which crude birth rate?", "25 per 1000 population", ["2.5 per 1000 population", "250 per 1000 population", "25 per 100 live births"], "25,000 divided by 1,000,000 multiplied by 1000 gives 25 per 1000.", True),
        q("Age-sex pyramid with broad base indicates what?", "High birth rate", ["Very old population only", "Zero fertility", "No dependency"], "A broad base reflects a large proportion of children and high fertility."),
        q("Dependency ratio compares dependent age groups with which population?", "Working-age population", ["Only newborns", "Only deaths", "Only married women"], "Dependency ratio relates children and elderly to working-age population."),
        q("Natural growth rate of population depends on birth rate and what?", "Death rate", ["Literacy rate only", "Hospital bed ratio", "Sex ratio only"], "Natural increase is births minus deaths, excluding migration."),
        q("A state has falling death rate but persistently high birth rate. Which demographic effect is expected?", "Rapid population growth", ["Population disappearance", "Zero dependency", "Immediate ageing only"], "Declining mortality with high fertility produces rapid growth.", True),
        q("Sex ratio in India is commonly expressed as number of females per how many males?", "1000 males", ["100 males", "1000 females", "100 live births"], "Sex ratio is females per 1000 males."),
        q("A low child sex ratio most directly suggests concern about what?", "Gender bias affecting survival or birth", ["High vaccine potency", "Low rainfall only", "Better dependency ratio"], "Low child sex ratio may reflect sex-selective practices and differential care.", True),
    ]),
    ("fertility-mortality-migration", "Fertility, Mortality, Migration and Population Transition", 2, [
        q("General fertility rate uses live births in a year per 1000 women of which age group?", "15-49 years", ["0-5 years", "60 years and above", "All males"], "GFR relates live births to women in reproductive age group."),
        q("Total fertility rate estimates the average number of children a woman would have under what condition?", "Current age-specific fertility rates continue", ["All women are infertile", "Death rate becomes zero", "Only male births are counted"], "TFR summarizes fertility across reproductive ages."),
        q("Replacement level fertility is approximately what TFR value?", "2.1", ["1.0", "5.5", "10.0"], "A TFR around 2.1 replaces the population over time under low mortality conditions."),
        q("A district TFR falls from 4.0 to 2.1 over two decades. What does this indicate?", "Movement toward replacement fertility", ["Rising fertility", "No demographic change", "Immediate population extinction"], "TFR near 2.1 indicates replacement-level fertility.", True),
        q("Infant mortality rate is deaths under one year per 1000 what?", "Live births", ["Mid-year population", "Pregnancies", "Women aged 15-49"], "IMR uses infant deaths per 1000 live births."),
        q("Neonatal mortality refers to deaths occurring within what age period?", "First 28 days of life", ["First 5 years", "First year after infancy", "Adolescence"], "Neonatal mortality covers deaths from birth to 28 completed days."),
        q("Maternal mortality ratio uses maternal deaths per 100,000 what?", "Live births", ["Mid-year population", "Women above 60", "Hospital beds"], "MMR is maternal deaths per 100,000 live births."),
        q("A village has high infant deaths from diarrhoea and pneumonia. Which indicator will be directly affected?", "Infant mortality rate", ["Sex ratio only", "Crude birth rate only", "Contraceptive prevalence only"], "Deaths below one year increase IMR.", True),
        q("Demographic transition describes population change with social development from high birth and death rates to what?", "Low birth and death rates", ["High birth and zero death rates", "Only migration increase", "No population structure"], "Demographic transition moves toward low fertility and low mortality."),
        q("Large movement of workers from rural areas to cities is an example of what?", "Migration", ["Fecundity", "Stillbirth", "Life table only"], "Migration is population movement across areas.", True),
    ]),
    ("family-planning-methods", "Family Planning Methods and Contraceptive Technology", 3, [
        q("Family planning primarily helps couples decide what?", "Number and spacing of children", ["Only child sex", "Only hospital type", "Only vaccine brand"], "Family planning enables informed decisions about timing, spacing and number of children."),
        q("Barrier contraceptives prevent pregnancy mainly by blocking what?", "Sperm entry into female reproductive tract", ["Ovulation in all users", "Breastfeeding", "Menstruation permanently"], "Condoms and diaphragms act as physical barriers."),
        q("Combined oral contraceptive pills prevent pregnancy mainly by inhibiting what?", "Ovulation", ["Fertilization after implantation", "Milk production only", "Sperm production permanently"], "Combined pills suppress gonadotropins and ovulation."),
        q("A lactating woman 2 months postpartum with exclusive breastfeeding and amenorrhoea asks about contraception. Which method may apply temporarily?", "Lactational amenorrhoea method", ["Calendar method after menopause", "Vasectomy for woman", "Emergency contraception daily"], "LAM can be effective when criteria are met: exclusive breastfeeding, amenorrhoea and less than 6 months postpartum.", True),
        q("Copper IUCD primarily acts by producing which effect?", "Local spermicidal inflammatory reaction", ["Permanent ovarian failure", "Increased implantation", "Raised prolactin only"], "Copper IUCD acts locally in uterus and impairs sperm function/fertilization."),
        q("Emergency contraception is most effective when used when after unprotected intercourse?", "As early as possible", ["Only after pregnancy is confirmed", "After one month", "Only after delivery"], "Emergency contraception should be taken soon after exposure, within recommended time limits."),
        q("Male sterilization is called what?", "Vasectomy", ["Tubectomy", "Hysterectomy", "Oophorectomy"], "Vasectomy interrupts vas deferens for male sterilization."),
        q("A man after vasectomy asks when he can stop other contraception. What is the correct advice?", "After semen analysis confirms azoospermia or as per protocol", ["Immediately the same day always", "After fever develops", "Never needs follow-up"], "Residual sperm may remain after vasectomy; follow-up advice is required.", True),
        q("Female sterilization usually interrupts which structure?", "Fallopian tubes", ["Ovarian follicles", "Cervix only", "Vagina"], "Tubal occlusion prevents ovum and sperm from meeting."),
        q("A woman with heavy menstrual bleeding wants long-term reversible contraception. Which option may also reduce bleeding?", "Levonorgestrel intrauterine system", ["Copper IUCD always", "Withdrawal", "Calendar method only"], "Hormonal intrauterine systems can reduce menstrual bleeding and provide contraception.", True),
    ]),
    ("programme-counselling-unmet-need", "Family Welfare Programme, Counselling and Unmet Need", 4, [
        q("India's family welfare programme emphasizes which approach?", "Voluntary and informed choice", ["Coercion", "Only one method for all", "No counselling"], "Modern family welfare stresses cafeteria approach and informed consent."),
        q("Eligible couple is commonly defined as a currently married couple in which the wife is in what age group?", "15-49 years", ["0-5 years", "50-80 years", "Only above 60 years"], "Eligible couple registers traditionally include married women of reproductive age."),
        q("Contraceptive prevalence rate measures proportion of eligible couples doing what?", "Using a contraceptive method", ["Having fever", "Migrating", "Delivering in hospital only"], "CPR indicates contraceptive use among eligible couples."),
        q("A couple wants to delay first pregnancy for 2 years but uses no contraception. This is an example of what?", "Unmet need for family planning", ["Completed fertility", "Sterility", "Maternal mortality"], "Unmet need exists when pregnancy is not desired soon or anymore but contraception is not used.", True),
        q("The cafeteria approach in family planning means providing what?", "Choice among multiple contraceptive methods", ["Only sterilization", "Only oral pills", "Only no method"], "Clients should choose from a range of suitable methods."),
        q("Good contraceptive counselling must include method benefits, side effects and what?", "Warning signs and follow-up advice", ["Only price", "Only brand name", "Only provider preference"], "Informed counselling covers use, adverse effects, warning signs and follow-up."),
        q("Spacing methods are especially useful for couples who want what?", "Delay or space births", ["Permanent end of fertility only", "Treatment of infertility", "Sex selection"], "Spacing methods help avoid closely spaced pregnancies."),
        q("A woman chooses an IUCD after counselling but has symptoms of pelvic infection. What should be done first?", "Assess and treat infection before insertion", ["Insert immediately without examination", "Ignore symptoms", "Perform vasectomy"], "Active pelvic infection is a contraindication until evaluated/treated.", True),
        q("Postpartum family planning is important because it helps prevent what?", "Closely spaced pregnancies", ["All congenital anomalies", "All neonatal infections", "All abortions forever"], "Healthy spacing improves maternal and child outcomes."),
        q("A health worker records eligible couples, method use and follow-up. Which programme function is this?", "Family planning register and tracking", ["Cancer registry only", "Vector density survey", "Death certification only"], "Tracking eligible couples supports counselling, supplies and follow-up.", True),
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
                "id": f"community-medicine-demography-family-planning-{slug}-{i:02d}",
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
