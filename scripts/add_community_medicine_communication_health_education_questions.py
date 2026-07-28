import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Communication for Health Education"
CHAPTER_ORDER = 17
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
    ("health-education-principles", "Health Education Principles", 1, [
        q("Health education aims to bring about desirable changes in knowledge, attitude and what?", "Practice", ["Blood group", "Height only", "Genetic code"], "Health education targets KAP: knowledge, attitude and practice."),
        q("The first step in planning health education is usually to identify the health problem and whom?", "Target audience", ["Printing press", "Final examination date", "Hospital profit"], "Planning begins with needs assessment and defining the audience."),
        q("Health education should be based on people's needs, interests and what?", "Cultural background", ["Only doctor's preference", "Only drug brand", "Only hospital colour"], "Messages work better when matched to local culture and felt needs."),
        q("A health worker explains ORS preparation using locally available utensils in a village. Which principle is being applied?", "Relevance to local needs and resources", ["Randomization", "Blinding", "Compensation"], "Health education should be practical and suited to the audience context.", True),
        q("Participation in health education means the learner should be actively involved in what?", "Learning and decision-making", ["Silent memorization only", "Ignoring feedback", "Only receiving orders"], "Participation improves acceptance and behaviour change."),
        q("Motivation in health education is important because it helps convert knowledge into what?", "Action", ["Income certificate", "Birth registration only", "Laboratory staining"], "Motivation supports actual adoption of healthy practices."),
        q("Reinforcement in health education means repeating and supporting messages to improve what?", "Retention and practice", ["Noise exposure", "Water hardness", "Vector breeding"], "Repeated supportive messages help sustain learning and behaviour."),
        q("Mothers attend a session but do not breastfeed correctly until they practise positioning with feedback. What principle is highlighted?", "Learning by doing", ["Open dumping", "Passive listening only", "No evaluation"], "Skill-based behaviours are best taught with demonstration and practice.", True),
        q("Credibility of the communicator is important because it increases what?", "Acceptance of the message", ["Disease incidence automatically", "Drug toxicity", "Water contamination"], "People are more likely to accept trusted sources."),
        q("A community ignores a malaria message because the speaker is unfamiliar and dismisses local beliefs. Which factor is weak?", "Source credibility and audience understanding", ["Sample size", "Standard deviation", "Incubation period"], "Trust and cultural understanding influence message acceptance.", True),
    ]),
    ("communication-process", "Communication Process and Barriers", 2, [
        q("Communication is the process of transmitting a message from sender to whom?", "Receiver", ["Vector", "Reservoir", "Host cell only"], "Communication needs a sender, message, channel and receiver."),
        q("The medium through which a health message travels is called what?", "Channel", ["Bias", "Confounder", "Incidence"], "Channels include interpersonal, print, audio, visual and mass media routes."),
        q("Feedback in communication helps the sender know whether the message was what?", "Understood", ["Printed", "Expensive", "Sterilized"], "Feedback checks understanding and allows correction."),
        q("A mother nods during counselling but prepares ORS wrongly at home. What was missing?", "Effective feedback and demonstration", ["More jargon", "Less interaction", "No message"], "Feedback verifies whether the audience has understood the skill.", True),
        q("Noise in communication refers to any factor that does what?", "Interferes with message transmission", ["Improves clarity", "Replaces feedback", "Guarantees learning"], "Noise may be physical, psychological, semantic or cultural."),
        q("Using technical medical jargon with villagers is mainly which barrier?", "Semantic barrier", ["Mechanical barrier only", "Genetic barrier", "Vector barrier"], "Semantic barriers occur when words are not understood as intended."),
        q("Communication is most effective when the message is clear, simple and what?", "Audience appropriate", ["Long and complex", "Secret", "Contradictory"], "Audience-matched language improves understanding."),
        q("A health talk on contraception fails because men and elders who influence decisions were excluded. What barrier is likely?", "Social and cultural barrier", ["High validity", "Random error only", "Good reinforcement"], "Social decision-makers and cultural norms affect communication outcomes.", True),
        q("Two-way communication is better than one-way communication for behaviour change because it allows what?", "Interaction and clarification", ["No questions", "Only orders", "No feedback"], "Dialogue lets learners ask questions and resolve doubts."),
        q("A patient does not follow TB treatment because instructions were rushed and not checked. Which communication component failed?", "Feedback", ["Birth rate", "Specificity", "Cold chain"], "Checking understanding is essential for adherence counselling.", True),
    ]),
    ("methods-media", "Methods and Media", 3, [
        q("Individual health education is best suited for personal problems and what?", "Counselling", ["Mass rallies only", "Census enumeration", "Vector mapping"], "One-to-one methods allow privacy and personalization."),
        q("Group health education methods include lectures, demonstrations and what?", "Group discussion", ["Only radio broadcast", "Only newspaper", "Only medical record"], "Group discussion allows participation and peer learning."),
        q("Mass media methods are useful for reaching large populations quickly but usually have limited what?", "Personal feedback", ["Coverage", "Speed", "Message repetition"], "Mass media can spread messages widely but feedback is weaker."),
        q("A diabetic patient needs diet advice matched to income, habits and treatment. Which method is best?", "Individual counselling", ["Only poster display", "Only radio jingle", "Only newspaper advertisement"], "Personal counselling can tailor advice to the patient's situation.", True),
        q("Demonstration is most useful when the learner must acquire what?", "Practical skill", ["Only a definition", "Only a slogan", "Only a statistic"], "Demonstration teaches skills such as ORS preparation or handwashing technique."),
        q("Role play in health education is useful for practising communication and what?", "Problem-solving", ["Blood testing", "X-ray diagnosis", "Drug manufacturing"], "Role play helps learners rehearse real-life situations and responses."),
        q("Posters used in health education should be simple, attractive and focused on what?", "One main message", ["Many crowded messages", "Tiny unreadable text", "Only decorative design"], "A poster should communicate one clear idea quickly."),
        q("A nurse teaches handwashing by showing each step and asking mothers to repeat it. Which method is this?", "Demonstration and return demonstration", ["Mass media only", "Vital registration", "Case-control study"], "Return demonstration confirms that the skill was learned.", True),
        q("Audio-visual aids in health education are useful because they involve more than one what?", "Sense organ", ["Chromosome", "Disease reservoir", "Sampling unit"], "Audio-visual aids improve attention and retention by engaging multiple senses."),
        q("A village campaign uses folk songs to promote mosquito control. Why may this work well?", "It uses a culturally familiar medium", ["It avoids participation", "It hides the message", "It replaces all services"], "Local media improve acceptability and audience connection.", True),
    ]),
    ("planning-evaluation", "Planning and Evaluation", 4, [
        q("A health education programme should define objectives that are specific, measurable and what?", "Achievable", ["Secret", "Unrelated", "Impossible"], "Clear measurable objectives guide implementation and evaluation."),
        q("The intended group for a health education message is called the what?", "Target audience", ["Null hypothesis", "Control group always", "Sampling error"], "Messages should be designed for a defined audience."),
        q("Pre-testing a health education material means testing it with a small audience before what?", "Final use", ["Discarding it", "Stopping the programme", "Changing the disease"], "Pre-testing checks clarity, acceptability and interpretation."),
        q("A poster on exclusive breastfeeding is shown to a few mothers before printing widely. What is this step?", "Pre-testing", ["Tertiary prevention", "Random sampling only", "Disease notification"], "Pre-testing finds confusing wording or images before mass use.", True),
        q("Process evaluation assesses whether programme activities were carried out as what?", "Planned", ["Inherited", "Randomized", "Sterile"], "Process evaluation checks implementation, coverage and quality of activities."),
        q("Impact evaluation in health education measures immediate changes in knowledge, attitude or what?", "Practice", ["Rainfall", "Chromosome number", "Hospital building size"], "Impact focuses on short-term KAP or behavioural changes."),
        q("Outcome evaluation assesses longer-term changes such as disease reduction or what?", "Health status improvement", ["Poster colour", "Speaker height", "Meeting duration only"], "Outcome evaluation looks at final health effects."),
        q("After a handwashing campaign, children wash hands more often but diarrhoea rates are not yet measured. Which evaluation is shown?", "Impact evaluation", ["Outcome evaluation only", "No evaluation", "Vital registration"], "Behaviour change is an impact-level result.", True),
        q("IEC in public health stands for information, education and what?", "Communication", ["Calculation", "Certification", "Compensation"], "IEC combines message development and communication for health action."),
        q("A campaign has high attendance but no improvement in ORS preparation skill. What should be reviewed?", "Teaching method and learning evaluation", ["Only census data", "Only bed occupancy", "Only vector species"], "Attendance alone does not prove learning; methods and skill assessment need review.", True),
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
                "id": f"community-medicine-communication-health-education-{slug}-{i:02d}",
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
