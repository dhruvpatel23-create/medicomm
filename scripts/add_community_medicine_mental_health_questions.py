import json
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
CHAPTER = "Mental Health"
CHAPTER_ORDER = 15
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
    ("concepts-burden", "Concepts and Burden of Mental Health", 1, [
        q("Mental health is not merely absence of mental illness but a state of well-being in which a person can cope and what?", "Contribute to community life", ["Avoid all work", "Never feel stress", "Remain isolated"], "Mental health includes functioning, coping, relationships and contribution."),
        q("Mental disorders are important in public health because they cause disability, suffering and what?", "Social and economic burden", ["Only skin rashes", "Only water pollution", "Only road widening"], "Mental illness affects individuals, families, productivity and health systems."),
        q("Common mental disorders in the community include depression, anxiety and what?", "Substance use disorders", ["Only cataract", "Only silicosis", "Only dental caries"], "Depression, anxiety and substance use are major community mental health problems."),
        q("A student has persistent low mood, loss of interest, poor sleep and impaired functioning for weeks. Which disorder is most likely?", "Depression", ["Simple shyness", "Acute appendicitis", "Heat stroke"], "Persistent low mood and anhedonia with dysfunction suggest depression.", True),
        q("Stigma in mental illness commonly leads to delayed care and what?", "Social exclusion", ["Improved access", "Earlier treatment always", "Better employment"], "Stigma prevents help-seeking and worsens social disadvantage."),
        q("Mental health promotion includes strengthening life skills, social support and what?", "Resilience", ["Open dumping", "Needle recapping", "Unsafe driving"], "Promotion builds coping capacity and supportive environments."),
        q("Severe mental disorders include schizophrenia, bipolar disorder and what?", "Severe depression", ["Only refractive error", "Only scabies", "Only fluorosis"], "Severe mental illness can markedly impair functioning and needs continuing care."),
        q("A man hears voices commenting on his actions and believes neighbours are controlling him. Which condition is suggested?", "Psychosis", ["Simple insomnia", "Anaemia", "Byssinosis"], "Hallucinations and delusions point toward psychosis.", True),
        q("Mental health is influenced by biological factors, psychological factors and what?", "Social determinants", ["Only blood group", "Only height", "Only eye colour"], "Poverty, trauma, housing, work and relationships affect mental health."),
        q("A woman with domestic violence exposure develops anxiety, sleep disturbance and fearfulness. Which public health concept is highlighted?", "Social determinants of mental health", ["Water hardness", "Vaccine potency", "Noise mapping only"], "Violence and unsafe social environments increase mental health risk.", True),
    ]),
    ("prevention-promotion", "Prevention and Mental Health Promotion", 2, [
        q("Primary prevention in mental health aims to reduce occurrence by addressing risk factors and promoting what?", "Protective factors", ["Only hospital admission", "Only drug dispensing", "Only compensation"], "Primary prevention reduces risk before illness develops."),
        q("School mental health programmes commonly focus on life skills, emotional support and what?", "Early identification of problems", ["Only exam ranking", "Only punishment", "Only eyesight testing"], "Schools can promote coping and identify children needing help."),
        q("Suicide prevention requires identifying warning signs, restricting means and what?", "Ensuring timely support and referral", ["Ignoring threats", "Public shaming", "Delaying care"], "Suicide prevention combines risk recognition, safety and urgent help."),
        q("A farmer expresses hopelessness, gives away belongings and has pesticide access. What is the immediate priority?", "Assess suicide risk and ensure safety", ["Ignore because it is attention seeking", "Advise more work only", "Send home alone"], "Suicidal warning signs need urgent risk assessment, supervision and referral.", True),
        q("Secondary prevention in mental health mainly involves early diagnosis and what?", "Prompt treatment", ["No follow-up", "Only terminal care", "Increased stigma"], "Early detection and treatment reduce severity and disability."),
        q("Tertiary prevention in chronic mental illness focuses on rehabilitation and prevention of what?", "Disability and relapse", ["All emotions", "All employment", "All social contact"], "Rehabilitation supports functioning and reduces chronic disability."),
        q("Community mental health education should reduce myths and encourage what?", "Help-seeking", ["Concealment", "Untreated isolation", "Blame of patients"], "Accurate information reduces stigma and improves treatment access."),
        q("A village health worker explains that depression is treatable and refers a patient to primary care. Which intervention is this?", "Mental health education and referral", ["Vector control", "Water chlorination", "Birth registration"], "Education and referral are key community mental health actions.", True),
        q("Workplace mental health promotion includes stress management, fair work conditions and what?", "Supportive supervision", ["Longer unsafe shifts", "Public humiliation", "No rest breaks"], "Healthy workplaces reduce stress and improve mental well-being."),
        q("Crisis helplines and gatekeeper training contribute mainly to prevention of what?", "Suicide", ["Dental fluorosis", "Silicosis", "Cholera"], "Accessible crisis support and trained gatekeepers help prevent suicide deaths.", True),
    ]),
    ("community-services", "Community Mental Health Services", 3, [
        q("Community mental health care aims to provide services close to home and integrate care with what?", "Primary health care", ["Only tertiary hospitals", "Only police stations", "Only schools"], "Integration with primary care improves access and continuity."),
        q("The district mental health approach emphasizes outpatient care, essential drugs, referral and what?", "Community awareness", ["Only large asylums", "Only private admission", "Only forensic care"], "District-level services include treatment, referral, training and IEC activities."),
        q("Decentralized mental health services reduce the need for long-stay institutional care and improve what?", "Accessibility", ["Stigma always", "Travel cost", "Untreated illness"], "Care near communities improves access and follow-up."),
        q("A patient with controlled schizophrenia needs regular medicines and family follow-up near his village. Which service model fits best?", "Community-based mental health care", ["Only distant custodial care", "No follow-up", "Emergency surgery"], "Stable severe mental illness can often be managed with community follow-up.", True),
        q("Primary care workers in mental health should be trained to identify common disorders and what?", "Refer severe or complex cases", ["Diagnose only by horoscope", "Avoid all counselling", "Stop all medicines"], "Training helps primary care detect, treat basic cases and refer when needed."),
        q("Continuity of care in mental illness is important because many disorders require what?", "Long-term follow-up", ["One visit only always", "No family involvement", "No medicines ever"], "Chronic and recurrent mental disorders need sustained care and support."),
        q("Family involvement in community mental health helps improve adherence, support and what?", "Relapse recognition", ["Stigma generation", "Isolation only", "Unsafe restraint"], "Families can notice relapse signs and support treatment when guided properly."),
        q("A person with epilepsy is labelled as possessed and hidden at home. What is the key community intervention?", "Health education and access to treatment", ["Increase stigma", "Avoid medical care", "Remove from school forever"], "Education corrects myths and links the person to effective care.", True),
        q("Rehabilitation for severe mental illness may include social skills training, vocational support and what?", "Community reintegration", ["Permanent exclusion", "No activity", "Only punishment"], "Rehabilitation aims to restore functioning and participation."),
        q("A recovered patient with mental illness is helped to return to work with follow-up support. This is an example of what?", "Psychosocial rehabilitation", ["Primary vaccination", "Water testing", "Mass chemoprophylaxis"], "Psychosocial rehabilitation supports independent and productive living.", True),
    ]),
    ("special-groups-substance", "Special Groups and Substance Use", 4, [
        q("Child mental health problems may present as learning difficulty, behavioural problems and what?", "Emotional symptoms", ["Only cataract", "Only hypertension", "Only fluorosis"], "Children may show emotional, behavioural or developmental problems."),
        q("Adolescent mental health programmes should address stress, substance use, sexuality and what?", "Life skills", ["Only tax filing", "Only retirement planning", "Only cataract surgery"], "Adolescents benefit from life skills, counselling and risk-behaviour prevention."),
        q("Postpartum mental health screening is important because mothers may develop depression and rarely what?", "Postpartum psychosis", ["Silicosis", "Byssinosis", "Lead line"], "Postpartum depression and psychosis can harm mother and infant if missed."),
        q("A mother two weeks after delivery is severely depressed, expresses guilt and has thoughts of harming herself. What should be done?", "Urgent mental health assessment and support", ["Reassure only without follow-up", "Leave her alone", "Delay care for months"], "Postpartum depression with self-harm thoughts needs urgent assessment and safety planning.", True),
        q("Elderly people are vulnerable to depression due to chronic illness, bereavement and what?", "Social isolation", ["Newborn screening", "Occupational dust", "High fertility"], "Isolation, loss and illness increase late-life depression risk."),
        q("Alcohol dependence is a public health problem because it contributes to injuries, family harm and what?", "Chronic disease", ["Improved nutrition always", "No social harm", "Only dental stains"], "Alcohol misuse causes health, social and economic harms."),
        q("Harmful substance use prevention includes health education, regulation of availability and what?", "Early counselling and treatment", ["Promotion of use", "No restriction", "Punishment without care only"], "Prevention and treatment both reduce substance-related harm."),
        q("A teenager is repeatedly absent from school, smells of alcohol and has falling grades. What is the appropriate response?", "Screen for substance use and counsel or refer", ["Expel without assessment", "Ignore until adulthood", "Give antibiotics only"], "Early identification and counselling can reduce adolescent substance harm.", True),
        q("Dementia is characterized by progressive impairment of memory and other cognitive functions causing what?", "Functional decline", ["Only fever", "Only cough", "Only skin rash"], "Dementia affects cognition enough to impair daily functioning."),
        q("An elderly man forgets familiar routes, misplaces money and cannot manage daily activities. Which condition should be suspected?", "Dementia", ["Simple tiredness", "Heat cramps", "Scabies"], "Progressive cognitive impairment with functional loss suggests dementia.", True),
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
                "id": f"community-medicine-mental-health-{slug}-{i:02d}",
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
