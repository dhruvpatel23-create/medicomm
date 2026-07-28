import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Genetics and Health"
CHAPTER_ORDER = 14
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
    ("basic-genetics", "Basic Genetics and Inheritance", 1, [
        q("The basic unit of heredity is called what?", "Gene", ["Chromatid only", "Ribosome", "Lysosome"], "Genes carry hereditary information and influence traits."),
        q("Human somatic cells normally contain how many chromosomes?", "46 chromosomes", ["23 chromosomes", "44 chromosomes", "69 chromosomes"], "Most human body cells are diploid with 46 chromosomes."),
        q("Autosomal dominant disorders usually appear in which pattern in a family pedigree?", "Vertical transmission across generations", ["Only males affected", "Only siblings with unaffected parents", "Only maternal relatives"], "Autosomal dominant traits often affect successive generations."),
        q("A child has an affected parent and a dominant single-gene disorder. What is the approximate risk to each child if the parent is heterozygous?", "50 percent", ["0 percent", "25 percent", "100 percent always"], "A heterozygous affected parent transmits the mutant allele to half of children on average.", True),
        q("Autosomal recessive disorders commonly occur when both parents are what?", "Carriers", ["Always affected", "Unrelated to genes", "Only elderly"], "Carrier parents can have affected children despite being clinically normal."),
        q("Consanguineous marriage increases risk mainly of which type of genetic disorders?", "Autosomal recessive disorders", ["Only X-linked dominant disorders", "Only mitochondrial disorders", "Only chromosomal nondisjunction"], "Related parents are more likely to share recessive disease alleles."),
        q("X-linked recessive disorders usually affect males more often because males have how many X chromosomes?", "One", ["Two", "Three", "None"], "A male with a pathogenic allele on his single X chromosome expresses the disorder."),
        q("A boy has haemophilia and his maternal uncle was also affected. Which inheritance pattern is suggested?", "X-linked recessive inheritance", ["Autosomal dominant inheritance", "Mitochondrial inheritance only", "Polygenic inheritance"], "Haemophilia classically follows X-linked recessive inheritance.", True),
        q("Multifactorial inheritance results from interaction of multiple genes and what?", "Environmental factors", ["Only blood group", "Only vaccine status", "Only birth order"], "Many common diseases reflect genetic susceptibility plus environmental influences."),
        q("A family has several members with hypertension, obesity and diabetes without a single-gene pattern. Which inheritance concept fits best?", "Multifactorial inheritance", ["Simple Mendelian dominant only", "Y-linked inheritance", "Chromosomal deletion only"], "Common chronic diseases often have polygenic and environmental determinants.", True),
    ]),
    ("genetic-diseases", "Genetic Diseases and Chromosomal Disorders", 2, [
        q("Down syndrome is most commonly due to trisomy of which chromosome?", "Chromosome 21", ["Chromosome 13", "Chromosome 18", "Chromosome X only"], "Trisomy 21 is the commonest chromosomal cause of Down syndrome."),
        q("The risk of Down syndrome increases with increasing what?", "Maternal age", ["Paternal height", "Birth order only", "Infant diet"], "Advanced maternal age increases risk of meiotic nondisjunction."),
        q("Turner syndrome usually has which chromosomal pattern?", "45,X", ["47,XXY", "47,XXX", "Trisomy 21"], "Turner syndrome is monosomy X or related sex-chromosome mosaicism."),
        q("A newborn has hypotonia, flat facial profile, single palmar crease and congenital heart disease. Which condition is likely?", "Down syndrome", ["Turner syndrome", "Klinefelter syndrome", "Phenylketonuria only"], "These are classic clinical features of Down syndrome.", True),
        q("Klinefelter syndrome is classically associated with which karyotype?", "47,XXY", ["45,X", "46,XY normal always", "47,XYY only"], "Klinefelter syndrome is most commonly 47,XXY."),
        q("Sickle cell disease is inherited in which pattern?", "Autosomal recessive", ["Autosomal dominant", "X-linked dominant", "Mitochondrial"], "Sickle cell disease occurs when both beta-globin alleles are affected."),
        q("Thalassaemia prevention in public health relies strongly on screening, carrier detection and what?", "Genetic counselling", ["Mass antibiotics", "Water chlorination only", "Vector fogging"], "Carrier screening and counselling help couples understand reproductive risk."),
        q("A couple are both beta-thalassaemia carriers. What is the chance of an affected child in each pregnancy?", "25 percent", ["0 percent", "50 percent", "100 percent"], "Two carrier parents have a one in four risk of an affected child per pregnancy.", True),
        q("Phenylketonuria causes preventable intellectual disability if untreated and is detected by what?", "Newborn screening", ["Audiometry only", "Mantoux test", "Pap smear"], "Newborn screening allows early dietary treatment of phenylketonuria."),
        q("A neonate detected with congenital hypothyroidism on screening is treated early to prevent what?", "Neurodevelopmental impairment", ["Silicosis", "Lead colic", "Cataract only"], "Early treatment prevents avoidable intellectual disability and developmental delay.", True),
    ]),
    ("prevention-screening-counselling", "Prevention, Screening and Counselling", 3, [
        q("Genetic counselling is a communication process that helps families understand genetic risk and what?", "Options for prevention or management", ["Only hospital billing", "Only school admission", "Only drug pricing"], "Counselling supports informed decisions about testing, reproduction and care."),
        q("Primary prevention of genetic disease includes avoiding consanguineous marriage where relevant and what?", "Preventing exposure to mutagens and teratogens", ["Ignoring family history", "Stopping immunization", "Open waste dumping"], "Primary prevention reduces occurrence by reducing risks before disease appears."),
        q("Secondary prevention of genetic disease mainly involves early detection through screening and what?", "Prompt intervention", ["Only terminal care", "No follow-up", "Increasing exposure"], "Screening is useful when early treatment or reproductive planning can reduce harm."),
        q("A woman with previous child affected by neural tube defect asks for prevention before pregnancy. Which measure is important?", "Periconceptional folic acid", ["Avoid all antenatal visits", "Only iron after delivery", "No dietary advice"], "Folic acid before conception and early pregnancy reduces neural tube defect risk.", True),
        q("Prenatal diagnosis is most useful when a pregnancy is at high risk for what?", "Serious fetal genetic disorder", ["Only mild fever", "Only maternal myopia", "Only adult hypertension"], "Prenatal testing is offered when inherited or chromosomal disease risk is significant."),
        q("Amniocentesis is a prenatal diagnostic procedure that samples what?", "Amniotic fluid", ["Maternal saliva", "Umbilical skin", "Placental air"], "Amniotic fluid contains fetal cells and biochemical markers for testing."),
        q("Carrier screening is especially useful for diseases that are common in a population and have what?", "Detectable carrier state", ["No genetic basis", "No counselling value", "Only infectious spread"], "Carrier detection allows risk estimation before affected births occur."),
        q("A couple with family history of haemophilia seeks advice before pregnancy. Which service is most appropriate?", "Genetic counselling", ["Only mass deworming", "Only cataract screening", "Only BP camp"], "Genetic counselling explains inheritance, testing and reproductive options.", True),
        q("Newborn screening programmes should target conditions where early diagnosis leads to what?", "Effective treatment or prevention of disability", ["No change in outcome", "Only cosmetic diagnosis", "Delayed care"], "Screening is justified when early action improves health outcomes."),
        q("A positive screening test for a genetic disorder should usually be followed by what?", "Confirmatory diagnostic testing", ["Immediate stigma", "No counselling", "Discarding records"], "Screening identifies risk; diagnosis requires confirmatory testing.", True),
    ]),
    ("community-public-health", "Community Genetics and Public Health", 4, [
        q("Community genetics applies genetic knowledge to improve health at which level?", "Population level", ["Only autopsy table", "Only private laboratory", "Only hospital accounts"], "Community genetics uses prevention, screening and counselling for populations."),
        q("Genetic registers can help provide follow-up, counselling and what?", "Risk assessment for relatives", ["Public entertainment", "Drug advertising", "Road licensing"], "Registers help identify families needing services while respecting confidentiality."),
        q("Confidentiality in genetic services is important because genetic information may affect whom?", "Family members", ["Only hospital furniture", "Only road traffic", "Only weather reports"], "Genetic results can have implications for relatives and future children."),
        q("A public health programme screens newborns for treatable metabolic diseases. Which level of prevention is this?", "Secondary prevention", ["Primordial prevention only", "Tertiary prevention only", "No prevention"], "Newborn screening detects disease early so treatment can prevent disability.", True),
        q("Teratogens are harmful exposures during pregnancy that may cause what?", "Congenital anomalies", ["Only adult hypertension", "Only senile cataract", "Only occupational asthma"], "Teratogens can disrupt fetal development and produce birth defects."),
        q("Rubella immunization before pregnancy helps prevent which fetal condition?", "Congenital rubella syndrome", ["Sickle cell disease", "Down syndrome", "Haemophilia A"], "Preventing maternal rubella protects the fetus from congenital rubella syndrome."),
        q("Fetal alcohol exposure can lead to growth restriction, facial features and what?", "Neurodevelopmental problems", ["Silicosis", "Malaria", "Scabies"], "Alcohol is a teratogen affecting growth and brain development."),
        q("A pregnant woman takes an unprescribed teratogenic drug in early pregnancy. What is the main concern?", "Risk of congenital malformation", ["Immediate occupational silicosis", "Only dental caries", "Only measles"], "Early organogenesis is a sensitive period for teratogenic malformations.", True),
        q("Public education in genetics should reduce stigma and improve understanding of what?", "Inheritance and prevention options", ["Only hospital rankings", "Only drug brand names", "Only bed numbers"], "Education helps families seek counselling and avoid blame or myths."),
        q("Screening relatives of an index case with hereditary disease is called what?", "Cascade screening", ["Mass randomization", "Cold-chain monitoring", "Vector surveillance"], "Cascade screening traces at-risk relatives from a known affected person.", True),
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
                "id": f"community-medicine-genetics-health-{slug}-{i:02d}",
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
