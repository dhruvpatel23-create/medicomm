import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Health Planning and Management"
CHAPTER_ORDER = 18
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
    ("planning-principles", "Health Planning Principles", 1, [
        q("Health planning is best described as deciding in advance what is to be done, when, how and by whom to achieve what?", "Health objectives", ["Hospital decoration", "Drug branding", "Only staff transfer"], "Planning links needs, resources, activities and objectives."),
        q("The first step in health planning is usually assessment of what?", "Health needs and problems", ["Wall colour", "Final report printing", "Vehicle number"], "Planning begins with situation analysis and need assessment."),
        q("A plan should define objectives that are specific, measurable, achievable, relevant and what?", "Time-bound", ["Secret", "Unrelated", "Impossible"], "SMART objectives guide implementation and evaluation."),
        q("A district finds high maternal deaths and maps causes before choosing interventions. Which planning step is this?", "Situation analysis", ["Final evaluation", "Randomization", "Drug procurement only"], "Understanding the current situation precedes intervention selection.", True),
        q("Priority setting in health planning is needed because resources are usually what?", "Limited", ["Unlimited", "Always unused", "Irrelevant"], "Prioritization matches scarce resources to important and feasible problems."),
        q("The planning cycle includes analysis, objective setting, implementation and what?", "Evaluation", ["Incubation", "Sterilization only", "Certification"], "Evaluation checks whether planned objectives were achieved."),
        q("A target in health planning is usually a quantified statement of what?", "Expected achievement", ["Patient surname", "Doctor age", "Hospital address"], "Targets express measurable expected results."),
        q("A block sets a goal to raise full immunization coverage from 70 percent to 90 percent in one year. What is this?", "Specific measurable target", ["Case definition", "Null hypothesis", "Vital event"], "The statement quantifies desired achievement within a time period.", True),
        q("Intersectoral coordination in health planning means working with sectors such as education, water supply and what?", "Local administration", ["Only pharmacies", "Only laboratories", "Only examiners"], "Health outcomes often depend on action outside the health department."),
        q("A malaria plan includes drainage, larval control, diagnosis and community education. Which principle is shown?", "Integrated planning", ["Single isolated activity", "No coordination", "Only curative care"], "Integrated plans combine multiple complementary actions.", True),
    ]),
    ("management-functions", "Management Functions", 2, [
        q("Management is commonly described through functions such as planning, organizing, staffing, directing and what?", "Controlling", ["Chlorinating", "Randomizing", "Certifying death"], "Classical management functions include planning through control/evaluation."),
        q("Organizing in management mainly involves arranging people, resources and what?", "Activities", ["Weather", "Blood groups", "Birth order"], "Organization creates structure for work and resource use."),
        q("Staffing includes recruitment, training, placement and what?", "Supervision", ["Open dumping", "Vector breeding", "Water hardness"], "Staffing ensures appropriate human resources and support."),
        q("A medical officer assigns outreach sessions, vaccine carriers and staff roles for immunization day. Which function is this?", "Organizing", ["Mortality coding", "Sample blinding", "P value calculation"], "Organizing arranges resources and responsibilities for work.", True),
        q("Supervision is intended to guide, support and improve what?", "Performance", ["Chromosome number", "Rainfall", "Drug colour"], "Good supervision improves service quality and worker performance."),
        q("Monitoring means continuous observation of programme activities to ensure they are proceeding according to what?", "Plan", ["Myth", "Chance", "Genetic code"], "Monitoring tracks implementation while the programme is running."),
        q("Evaluation measures relevance, effectiveness, efficiency and what?", "Impact", ["Road width only", "Hospital paint", "Staff handwriting"], "Evaluation assesses results and value of a programme."),
        q("A PHC reviews monthly ANC coverage and corrects missed village visits. Which management activity is this?", "Monitoring and corrective action", ["Final autopsy", "Random sampling", "Drug trial blinding"], "Monitoring detects gaps and supports timely corrections.", True),
        q("Delegation means assigning authority and responsibility to whom?", "Subordinates", ["Only patients", "Only suppliers", "Only census officers"], "Delegation distributes work with appropriate authority and accountability."),
        q("A supervisor checks registers, observes vaccine storage and gives feedback to ANMs. Which function is shown?", "Supportive supervision", ["Mass media", "Vital registration", "Tertiary care only"], "Supervision combines observation, guidance and feedback.", True),
    ]),
    ("resources-logistics", "Resources and Logistics", 3, [
        q("Health resources include manpower, money, material and what?", "Time", ["Only slogans", "Only rainfall", "Only genetics"], "Planning requires human, financial, material and time resources."),
        q("Budgeting in health planning is the process of estimating financial requirements and what?", "Allocating funds", ["Measuring height", "Writing slogans", "Counting chromosomes"], "Budgets convert planned activities into financial terms."),
        q("Logistics management ensures the right item is available in the right quantity, condition, place and what?", "Time", ["Colour", "Language", "Disease only"], "Logistics aims for timely availability without stock-outs or wastage."),
        q("A subcentre has vaccine sessions cancelled because syringes were not supplied on time. Which management problem is this?", "Logistics failure", ["High fertility", "Good surveillance", "Perfect supervision"], "Essential supplies must be available when services are delivered.", True),
        q("Inventory control helps prevent both stock-outs and what?", "Overstocking or wastage", ["Birth registration", "Disease notification", "Counselling"], "Inventory control balances availability with efficient use."),
        q("The cold chain is a logistics system that maintains vaccines at recommended what?", "Temperature", ["P value", "Blood pressure", "Literacy rate"], "Cold chain preserves vaccine potency from storage to administration."),
        q("Human resource planning estimates required number, type and distribution of what?", "Health workers", ["Mosquito species", "Death certificates", "Drug labels only"], "HR planning matches workforce to service needs."),
        q("A district has enough nurses overall but none in remote PHCs. What planning issue is present?", "Maldistribution of human resources", ["Excess vital registration", "Too much evaluation", "Perfect equity"], "Distribution matters as much as total workforce availability.", True),
        q("Cost-effectiveness analysis compares costs with what?", "Health outcomes achieved", ["Poster colour", "Staff names", "Building height"], "Cost-effectiveness helps choose efficient interventions."),
        q("A programme chooses ORS distribution because it prevents many child deaths at low cost. Which concept is being used?", "Cost-effectiveness", ["Case fatality only", "Random error", "Genetic counselling"], "Cost-effective interventions provide large health gains for resources spent.", True),
    ]),
    ("implementation-evaluation", "Implementation and Evaluation", 4, [
        q("Implementation means putting a health plan into what?", "Action", ["Archive", "Autopsy", "Census only"], "Implementation converts planned activities into field operations."),
        q("Operational planning translates broad objectives into detailed activities, responsibilities and what?", "Timelines", ["Blood groups", "Drug taste", "Eye colour"], "Operational plans specify who does what, where and when."),
        q("Process indicators measure activities such as sessions held, visits made and what?", "Services delivered", ["Deaths prevented only", "Final disease reduction", "Genetic mutations"], "Process indicators track implementation activities."),
        q("An immunization plan reports number of outreach sessions conducted this month. Which indicator type is this?", "Process indicator", ["Outcome indicator only", "Impact indicator only", "Confounder"], "Sessions conducted reflect programme process.", True),
        q("Output indicators measure immediate results such as coverage and what?", "Service utilization", ["Rainfall", "Hospital paint", "Road length only"], "Outputs are direct products of programme activities."),
        q("Outcome indicators measure changes in health status, behaviour or what?", "Disease occurrence", ["Meeting duration only", "Register colour", "Staff age"], "Outcomes reflect effects beyond service delivery."),
        q("Impact indicators often measure long-term changes such as mortality reduction and what?", "Improved population health", ["Poster visibility", "Vehicle colour", "Speech length"], "Impact looks at broader and longer-term health gains."),
        q("After a TB control plan, cure rate improves and default rate falls. Which evaluation level is mainly shown?", "Outcome evaluation", ["Only input evaluation", "No evaluation", "Vital registration"], "Cure and default rates are outcome indicators for TB services.", True),
        q("A Gantt chart is useful in programme planning because it displays activities against what?", "Time schedule", ["Blood group", "Disease reservoir", "Sample size only"], "Gantt charts show activity timelines and progress."),
        q("A district plan fails because responsibilities were unclear and no timeline was assigned. Which planning component was weak?", "Operational planning", ["Genetic counselling", "Case definition", "Mass media only"], "Operational planning should specify activities, responsible persons and timeframes.", True),
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
                "id": f"community-medicine-health-planning-management-{slug}-{i:02d}",
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
