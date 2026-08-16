import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
SUBJECT_ID = "general-medicine"
SUBJECT_TITLE = "General Medicine"
CHAPTER = "The Profession of Medicine"
CHAPTER_ORDER = 1
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
    ("Patient-Centered Clinical Method", [
        q("The central obligation of the physician-patient relationship is to", "Place the patient's welfare and informed choices at the center of care", ["Maximize investigations in every encounter", "Follow family preferences over patient preferences", "Avoid discussing uncertainty"], "Professional care combines beneficence, respect for autonomy and honest communication."),
        q("A complete clinical encounter should integrate disease diagnosis with assessment of", "The patient's illness experience, values and functional context", ["Only the final laboratory abnormality", "Only insurance eligibility", "Only the physician's preferred treatment"], "Good medicine treats the patient who has the disease, not only the disease label."),
        q("A 62-year-old with heart failure says she cannot take diuretics because she fears being unable to travel for work. The best next step is to", "Explore her goals and barriers before revising the treatment plan", ["Document noncompliance and end the visit", "Increase the dose without discussion", "Ask the family to decide for her"], "Adherence improves when the plan fits the patient's life and concerns.", True),
        q("Shared decision-making is most important when", "More than one medically reasonable option exists with different trade-offs", ["The diagnosis is already obvious", "The patient is unconscious without a surrogate", "A laboratory value is being transcribed"], "Preference-sensitive decisions require clear explanation of risks, benefits and alternatives."),
        q("The most useful opening question in history taking is usually one that", "Allows the patient to describe the problem in their own words", ["Immediately narrows to a yes-or-no symptom", "Tests medical terminology", "Avoids emotional content"], "An open beginning reveals symptoms, sequence and concerns that closed questions can miss."),
        q("A patient with newly diagnosed cancer asks, 'Am I going to die soon?' The best response is to", "Acknowledge the fear and ask what they understand before giving clear information", ["Say there is nothing to worry about", "Change the subject to chemotherapy protocols", "Give survival statistics without checking readiness"], "Serious conversations need empathy, assessment of understanding and honest information.", True),
        q("The main reason to summarize the patient's story back to them is to", "Confirm accuracy and show that their concerns were heard", ["Shorten documentation time only", "Avoid physical examination", "Replace diagnostic reasoning"], "Reflection catches errors and strengthens therapeutic alliance."),
        q("In chronic disease care, the physician's role includes helping the patient to", "Develop self-management skills and realistic goals", ["Depend completely on clinic visits", "Stop monitoring symptoms", "Avoid lifestyle discussions"], "Long-term outcomes depend heavily on informed patient participation."),
        q("A patient repeatedly misses diabetes visits because clinic timing conflicts with daily wages. The most patient-centered response is to", "Identify practical access barriers and arrange a feasible follow-up plan", ["Dismiss the patient from care immediately", "Assume lack of interest", "Prescribe insulin without education"], "Social and logistical barriers must be addressed as part of clinical care.", True),
        q("A hospitalized patient refuses a recommended procedure after understanding the risks. The physician should", "Respect the informed refusal and discuss alternative management", ["Proceed because the doctor knows best", "Ask security to compel consent", "Hide the refusal from the chart"], "Capacitous patients may refuse treatment even when refusal increases risk.", True),
    ]),
    ("Diagnostic Reasoning and Evidence", [
        q("A diagnostic hypothesis should be revised most strongly when", "New findings are inconsistent with the working diagnosis", ["The first impression feels familiar", "The patient is young", "A rare disease is interesting"], "Sound reasoning updates probability as new evidence arrives."),
        q("Premature closure in diagnosis means", "Accepting a diagnosis before adequate consideration of alternatives", ["Ordering too many follow-up appointments", "Documenting a differential diagnosis", "Repeating an abnormal test"], "Premature closure is a common cognitive error leading to missed diagnoses."),
        q("A 55-year-old with chest discomfort is diagnosed as gastritis without ECG despite diaphoresis and risk factors. The reasoning error is most likely", "Premature closure", ["Lead-time bias", "Verification bias in screening", "Ecological fallacy"], "Stopping at a benign explanation before excluding dangerous alternatives is premature closure.", True),
        q("The pretest probability of disease is mainly estimated from", "Clinical context, history, examination and disease prevalence", ["The reference range alone", "The cost of the test", "The brand of the analyzer"], "Test interpretation depends on probability before the test is ordered."),
        q("A highly sensitive test is most useful for", "Ruling out disease when the result is negative", ["Confirming disease whenever positive", "Replacing clinical examination", "Increasing disease prevalence"], "Sensitive tests have few false negatives, so a negative result reduces probability."),
        q("A highly specific test is most useful for", "Ruling in disease when the result is positive", ["Screening every low-risk person", "Ignoring false positives", "Estimating prognosis alone"], "Specific tests have few false positives, so a positive result is persuasive."),
        q("A low-risk patient requests a whole-body scan. The best explanation against indiscriminate testing is that it", "May produce false positives and downstream harm without likely benefit", ["Never finds disease", "Is unethical in every circumstance", "Cannot detect anatomical abnormalities"], "Testing low-probability populations can cause overdiagnosis, anxiety and invasive follow-up.", True),
        q("A D-dimer is negative in a patient with low clinical probability of pulmonary embolism. The appropriate interpretation is", "Pulmonary embolism is unlikely", ["Pulmonary embolism is confirmed", "CT pulmonary angiography is mandatory for all patients", "The assay proves myocardial infarction"], "A sensitive D-dimer helps exclude PE in low-probability patients.", True),
        q("Bayesian reasoning in clinical diagnosis means that", "Test results are interpreted by how much they change prior probability", ["Every disease is considered equally likely", "One positive test always proves disease", "Population data are ignored"], "Likelihood ratios modify the probability estimated before testing."),
        q("A patient has recurrent syncope. The physician documents arrhythmia, seizure, orthostatic hypotension and structural heart disease before testing. This is an example of", "Constructing a problem-based differential diagnosis", ["Therapeutic misconception", "Informed refusal", "Screening bias"], "A differential organizes plausible causes and guides targeted evaluation.", True),
    ]),
    ("Ethics, Consent and Confidentiality", [
        q("Valid informed consent requires disclosure, voluntariness and", "Decision-making capacity", ["A relative's signature in every case", "Payment before treatment", "Absence of all risk"], "Consent is valid only when a capable patient understands and freely chooses."),
        q("Decision-making capacity is task-specific and includes the ability to", "Understand, appreciate, reason about options and communicate a choice", ["Recite medical facts perfectly", "Agree with the physician", "Have no psychiatric diagnosis"], "Capacity concerns the decision at hand, not a global label."),
        q("A confused patient with sepsis refuses antibiotics but cannot explain the consequences. The physician should first", "Assess and treat reversible causes of impaired capacity while seeking surrogate input", ["Accept the refusal as fully informed", "Ignore the patient permanently", "Discharge immediately"], "Delirium can impair capacity and urgent care may require surrogate or emergency standards.", True),
        q("Confidentiality may be breached without consent when", "There is a serious, legally recognized risk to others or mandatory reporting requirement", ["The physician is curious", "The family asks casually", "The diagnosis is embarrassing"], "Confidentiality is strong but not absolute when law or serious preventable harm applies."),
        q("The ethical principle of autonomy primarily protects the patient's right to", "Make informed decisions about their own body and care", ["Demand ineffective treatment", "Avoid all documentation", "Override public health law"], "Autonomy requires respect for informed choices within professional and legal limits."),
        q("A patient with tuberculosis refuses isolation and plans to travel in a crowded bus. The physician's duty includes", "Taking public health steps to prevent serious transmission", ["Keeping the plan secret under all circumstances", "Providing only symptomatic treatment", "Calling relatives before notifying health authorities"], "Contagious diseases can create duties to protect others through lawful public health action.", True),
        q("Medical paternalism is least justified when", "A capable patient has made an informed preference-sensitive decision", ["Immediate emergency care is needed and no surrogate is available", "The patient lacks capacity", "Temporary stabilization is required"], "Capable informed patients should not be overruled merely because the clinician disagrees."),
        q("Truth telling in medicine is best understood as", "Clear, compassionate disclosure adjusted to the patient's readiness and preferences", ["Blunt delivery without empathy", "Withholding diagnosis routinely", "Only speaking to relatives"], "Honesty and compassion are both required in difficult conversations."),
        q("A family asks the doctor not to tell a competent patient about metastatic cancer. The best response is to", "Ask the patient how much information they want and whom they want involved", ["Promise the family secrecy", "Tell the family to leave permanently", "Document cure to reduce distress"], "The patient controls information preferences if they have capacity.", True),
        q("A medical student wants to post a de-identified rare case with enough details for recognition. The correct action is to", "Avoid posting unless proper consent and institutional rules are satisfied", ["Post if the name is removed", "Post only in a private social media group", "Change the patient's age by one year"], "Confidentiality can be breached even without names if details identify the patient.", True),
    ]),
    ("Quality, Safety and Systems of Care", [
        q("A systems approach to medical error emphasizes", "Designing processes that make correct action easier and harm less likely", ["Blaming the last person involved", "Hiding near misses", "Avoiding standardization"], "Most safety improvement comes from better systems, not individual blame alone."),
        q("A near miss is important because it", "Reveals a hazard before patient harm occurs", ["Is not worth reporting", "Always requires punishment", "Proves negligence"], "Near misses are valuable signals for prevention."),
        q("A nurse catches that a tenfold insulin dose was prescribed before administration. This event should be", "Reported and analyzed as a near miss", ["Ignored because no harm occurred", "Deleted from the chart", "Handled only by scolding the prescriber"], "Learning from intercepted errors improves future safety.", True),
        q("Root cause analysis is used after serious adverse events to", "Identify contributory system factors and prevention strategies", ["Assign legal guilt immediately", "Calculate hospital income", "Replace informed consent"], "RCA looks beyond the final act to conditions that allowed harm."),
        q("The safest handoff communication is one that", "Uses structured, concise transfer of diagnosis, status, risks and pending tasks", ["Relies on memory alone", "Mentions only the room number", "Avoids uncertainty"], "Structured handoffs reduce omissions during transitions of care."),
        q("A postoperative patient deteriorates overnight after abnormal vitals were not escalated during shift change. The best quality intervention is", "Create a reliable escalation and handoff process for abnormal vital signs", ["Tell staff to be more careful only", "Stop recording vital signs", "Avoid night admissions"], "A dependable trigger and communication process addresses the system failure.", True),
        q("Clinical practice guidelines are best used as", "Evidence-based aids adapted to the individual patient's context", ["Rigid rules that replace judgment", "Legal documents only", "Instructions to avoid explaining options"], "Guidelines support but do not replace individualized clinical reasoning."),
        q("Checklists improve safety mainly by", "Reducing omission of critical steps in complex workflows", ["Making expertise unnecessary", "Increasing paperwork for its own sake", "Preventing all complications"], "Checklists protect against predictable memory and coordination failures."),
        q("A central line team uses full barrier precautions and a checklist, then infection rates fall. This improvement targets", "Healthcare-associated bloodstream infection prevention", ["Genetic risk reduction", "Diagnostic lead-time bias", "Patient confidentiality"], "Insertion bundles reduce catheter-related bloodstream infections.", True),
        q("Open disclosure after a harmful medical error should include", "Honest explanation, apology where appropriate and steps to reduce future harm", ["Concealment until asked directly", "Blaming the patient", "Changing records to reduce liability"], "Transparency maintains trust and supports learning after harm.", True),
    ]),
    ("Professionalism, Learning and Society", [
        q("Professionalism in medicine includes competence, integrity, accountability and", "Commitment to patients and society", ["Personal convenience above all else", "Avoidance of teamwork", "Resistance to new evidence"], "Medicine is a social profession with duties beyond technical skill."),
        q("Lifelong learning is essential because medical practice", "Changes as evidence, technology and population needs evolve", ["Is fully mastered at graduation", "Does not depend on outcomes", "Rarely changes after textbooks"], "Continuing competence requires updating knowledge and skills."),
        q("A physician realizes a new drug they commonly prescribe has important updated safety restrictions. The professional response is to", "Review the evidence and adjust practice promptly", ["Ignore it until the next textbook edition", "Continue prescribing without discussion", "Delete patient messages about adverse effects"], "Professional competence requires responding to credible new safety information.", True),
        q("Conflict of interest is problematic because it can", "Bias judgment or undermine trust even when no harm is intended", ["Always proves corruption", "Only occurs with cash gifts", "Never affects prescribing"], "Financial and nonfinancial interests can influence decisions or perception."),
        q("The best response to a pharmaceutical gift that may influence prescribing is to", "Follow institutional policy and preserve independent clinical judgment", ["Accept it because all gifts are harmless", "Prescribe the company's drug preferentially", "Avoid telling patients about alternatives"], "Managing conflicts protects trust and decision quality."),
        q("A patient cannot afford the first-line medicine. Professional care requires the physician to", "Discuss affordable effective alternatives and access options", ["Prescribe the unaffordable drug anyway", "Withhold the diagnosis", "Assume the patient will be nonadherent"], "Cost is a real determinant of treatment success and should be addressed.", True),
        q("Cultural humility in clinical practice means", "Eliciting the patient's beliefs and avoiding assumptions while providing evidence-based care", ["Accepting harmful requests without discussion", "Using stereotypes to save time", "Avoiding interpreters"], "Respectful care asks rather than assumes and still explains medical reasoning."),
        q("A patient with limited English nods to a surgical consent discussion but cannot explain the operation. The best next step is", "Use a trained medical interpreter and reassess understanding", ["Proceed because nodding means consent", "Ask a child relative to translate complex risks", "Skip consent documentation"], "Language access is necessary for valid informed consent.", True),
        q("Team-based care is important because complex illness often requires", "Coordinated contributions from multiple health professionals", ["One physician making all decisions alone", "Avoiding nursing input", "Separating inpatient and outpatient information"], "Good outcomes depend on communication across disciplines and settings."),
        q("A junior doctor is asked to perform a procedure they have never done unsupervised. The professional response is to", "Seek supervision and disclose their level of experience", ["Attempt it silently", "Ask the patient not to worry", "Document it as completed by a senior"], "Recognizing limits and seeking help protects the patient and supports learning.", True),
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
                "id": f"medicine-profession-{topic_slug}-{question_order:02d}",
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
        if not (item.get("subjectId") in {SUBJECT_ID, "medicine"} and item.get("chapterTitle") == CHAPTER)
    ] + questions
    if len(questions) != 50:
        raise AssertionError(f"Expected 50 questions, got {len(questions)}")
    if len({item["id"] for item in questions}) != 50:
        raise AssertionError("Duplicate medicine question ids")
    if any(item["answer"] != item["options"][item["answerIndex"]] for item in questions):
        raise AssertionError("Answer mismatch found")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    for path in DATA_PATHS:
        update(path)
        print(f"Updated {path} with 50 Medicine Profession questions.")


if __name__ == "__main__":
    main()
