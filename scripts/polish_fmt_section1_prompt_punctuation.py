import json
import re
from pathlib import Path

DATA_PATHS = [Path("runtime-data/users.json"), Path("data/users.json")]
PREFIX = "fmt-section1-"

PROMPT_OVERRIDES = {
    "fmt-section1-legal-identification-death-courts-law-03": "What must a dying declaration relate to in order to be admissible?",
    "fmt-section1-legal-identification-death-courts-law-04": "A conscious burns patient tells the magistrate that her husband poured kerosene and lit the match. She dies the next day. What is this statement best treated as?",
    "fmt-section1-legal-identification-death-courts-law-08": "A doctor receives a court summons for the original wound certificate but sends only a photocopy without permission. What is the main legal problem?",
    "fmt-section1-legal-identification-death-courts-law-10": "In court, a forensic expert says an injury is possible by the alleged weapon but cannot identify the assailant. What does medical evidence mainly establish?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-asphyxia-general-06": "How should general asphyxial signs be interpreted in forensic practice?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-cold-electricity-03": "In which type of injury is a Joule burn seen?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-corrosives-irritants-05": "What is oxalic acid poisoning notable for?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-drowning-03": "Where are washerwoman changes seen after immersion?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-drowning-05": "Where should diatoms be found for the diatom test to support antemortem drowning?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-hanging-strangulation-06": "In which setting is fracture of the hyoid bone more common?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-neurotoxic-asphyxiant-poisons-06": "How does carbon monoxide cause hypoxia?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-sexual-offences-03": "Which tests may be used for semen detection?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-starvation-neglect-08": "A detainee alleges beating on the soles; examination shows tender patterned bruising over the plantar surfaces with difficulty walking. What is this consistent with?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-thermal-burns-08": "A charred body has splits over joints without bleeding or tissue reaction. How should these findings be interpreted?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-thermal-burns-09": "Heat stroke is characterized by hyperthermia with what key clinical feature?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-toxicology-general-01": "How does a poison cause harm after entering the body?",
    "fmt-section1-postmortem-trauma-asphyxia-toxicology-toxicology-general-08": "After gastric lavage in suspected poisoning, the first wash and vomitus are saved, sealed and labeled. Why is this done?",
}


def sentence_case(text):
    return text[:1].upper() + text[1:] if text else text


def polish(prompt):
    text = str(prompt).strip()
    text = re.sub(r"\s+", " ", text)
    text = text.rstrip(" .:")

    lower = text.lower()
    if lower.startswith("the main objective of ") and lower.endswith(" is to determine"):
        subject = text[22:-15].strip()
        return f"What is the main objective of {subject}?"
    if lower.startswith("in ") and lower.endswith(" should be preserved in"):
        prefix, subject = text[:-23].split(",", 1)
        return f"{sentence_case(prefix.strip())}, what should {subject.strip()} be preserved in?"
    if lower.endswith("the purpose is"):
        prefix = text[:-14].strip().rstrip(".")
        return f"{prefix}. What is the purpose?"
    if lower.endswith("this procedure is"):
        prefix = text[:-17].strip().rstrip(".")
        return f"{prefix}. What is this procedure?"
    if lower.startswith("in decomposed bodies, identification is aided by"):
        return "In decomposed bodies, which findings are most useful for identification?"
    if lower.endswith("the main evidentiary weakness is"):
        prefix = text[:-32].strip().rstrip(".")
        return f"{prefix}. What is the main evidentiary weakness?"
    if lower.endswith("the likely mechanism is"):
        prefix = text[:-24].strip().rstrip(".")
        return f"{prefix}. What is the likely mechanism?"
    if lower.endswith("cause is"):
        prefix = text[:-8].strip().rstrip(".")
        return f"{prefix}. What is the cause?"
    if lower.endswith("the likely poison is"):
        prefix = text[:-20].strip().rstrip(".")
        return f"{prefix}. What is the likely poison?"
    if lower.endswith("the diagnosis is"):
        prefix = text[:-16].strip().rstrip(".")
        return f"{prefix}. What is the diagnosis?"
    if lower.endswith("the death is most consistent with"):
        prefix = text[:-34].strip().rstrip(".")
        return f"{prefix}. The death is most consistent with what?"
    if lower.endswith("these findings favor"):
        prefix = text[:-20].strip().rstrip(".")
        return f"{prefix}. These findings favor which diagnosis?"
    if lower.endswith("the best diagnosis is"):
        prefix = text[:-22].strip().rstrip(".")
        return f"{prefix}. What is the best diagnosis?"
    if lower.endswith("one who"):
        return f"{sentence_case(text)} does what?"
    if lower.endswith("failure to"):
        prefix = text[:-10].strip().rstrip(".")
        return f"{prefix}. The failure was to do what?"
    if lower.endswith("explained by"):
        subject = text[:-12].strip()
        return f"What explains {subject[:1].lower() + subject[1:]}?"
    if lower.endswith("results in"):
        subject = text[:-10].strip()
        return f"{sentence_case(subject)} results in what?"
    if lower.endswith("age estimation in"):
        subject = text[:-17].strip()
        return f"{sentence_case(subject)} is most useful for age estimation in whom?"
    if lower.endswith("adult age mainly from"):
        subject = text[:-22].strip()
        return f"{sentence_case(subject)} estimates adult age mainly from what?"
    if lower.endswith("is mainly caused by") or lower.endswith("are mainly caused by"):
        subject = re.sub(r"\s+(is|are)\s+mainly\s+caused\s+by$", "", text, flags=re.I).strip()
        return f"What mainly causes {subject[:1].lower() + subject[1:]}?"
    if lower.endswith("is formed by"):
        subject = text[:-12].strip()
        return f"What forms {subject[:1].lower() + subject[1:]}?"
    if lower.endswith("is favored by"):
        subject = text[:-13].strip()
        return f"What conditions favor {subject[:1].lower() + subject[1:]}?"
    if lower.endswith("occurs fastest in"):
        subject = text[:-18].strip()
        return f"{sentence_case(subject)} occurs fastest in which environment?"
    if lower.endswith("associated with"):
        subject = text[:-15].strip()
        return f"{sentence_case(subject)} is classically associated with what?"
    if lower.endswith("produced by"):
        subject = text[:-11].strip()
        return f"What produces {subject[:1].lower() + subject[1:]}?"
    if lower.endswith("may occur in"):
        subject = text[:-12].strip()
        return f"{sentence_case(subject)} may occur in which setting?"
    if lower.endswith("injury to"):
        subject = text[:-9].strip()
        return f"{sentence_case(subject)} involves injury to what?"
    if lower.endswith("due to"):
        subject = text[:-6].strip()
        return f"What is {subject[:1].lower() + subject[1:]} due to?"
    if lower.endswith("can result from"):
        subject = text[:-16].strip()
        return f"What can {subject[:1].lower() + subject[1:]} result from?"
    if lower.endswith(" because it relates to"):
        subject = text[:-22].strip()
        return f"What must {subject[:1].lower() + subject[1:]} relate to?"
    if lower.endswith(" is best treated as"):
        prefix = text[:-19].strip()
        return f"{prefix}. What is it best treated as?"
    if lower.endswith(" is primarily"):
        subject = text[:-13].strip()
        return f"What is {subject[:1].lower() + subject[1:]} primarily?"
    if lower.endswith(" is paid to a witness for"):
        subject = text[:-25].strip()
        return f"What is {subject[:1].lower() + subject[1:]} paid to a witness for?"
    if lower.endswith(" mainly establishes"):
        prefix = text[:-19].strip()
        return f"{prefix}. What does medical evidence mainly establish?"
    if lower.endswith(" is ethically weak mainly because"):
        prefix = text[:-33].strip()
        return f"{prefix}. Why is this ethically weak?"
    if lower.endswith(" may be breached when"):
        subject = text[:-21].strip()
        return f"When may {subject[:1].lower() + subject[1:]} be breached?"
    if lower.endswith(" relates to"):
        subject = text[:-10].strip()
        return f"What does {subject[:1].lower() + subject[1:]} relate to?"
    if lower.endswith(" is best regarded as"):
        subject = text[:-19].strip()
        return f"What is {subject[:1].lower() + subject[1:]} best regarded as?"
    if lower.endswith(" is commonly seen around the"):
        subject = text[:-29].strip()
        return f"{sentence_case(subject)} is commonly seen around which structure?"
    if lower.endswith(" primarily affects the"):
        subject = text[:-22].strip()
        return f"{sentence_case(subject)} primarily affects which region?"
    if lower.endswith(" classically involves the"):
        subject = text[:-25].strip()
        return f"{sentence_case(subject)} classically involves which structure?"
    if lower.endswith(" commonly injures the"):
        subject = text[:-21].strip()
        return f"{sentence_case(subject)} commonly injures which region?"
    if lower.endswith(" typically has"):
        subject = text[:-14].strip()
        return f"What features does {subject[:1].lower() + subject[1:]} typically have?"
    if lower.endswith(" is usually"):
        subject = text[:-11].strip()
        return f"What is {subject[:1].lower() + subject[1:]} usually?"
    if lower.endswith(" means"):
        subject = text[:-6].strip()
        return f"What does {subject[:1].lower() + subject[1:]} mean?"
    if lower.endswith(" refers to"):
        subject = text[:-9].strip()
        return f"What does {subject[:1].lower() + subject[1:]} refer to?"
    if lower.endswith(" is caused by"):
        subject = text[:-13].strip()
        return f"What causes {subject[:1].lower() + subject[1:]}?"
    if lower.endswith(" is due to"):
        subject = text[:-9].strip()
        return f"What is {subject[:1].lower() + subject[1:]} due to?"
    if lower.endswith(" is used to"):
        subject = text[:-10].strip()
        return f"What is {subject[:1].lower() + subject[1:]} used to do?"
    if lower.endswith(" is used in assessment of"):
        subject = text[:-25].strip()
        return f"{sentence_case(subject)} is used in the assessment of what?"
    if lower.endswith(" is usually"):
        return f"{sentence_case(text)} what?"
    if lower.endswith(" is to determine"):
        subject = text[:-15].strip()
        return f"What does {subject[:1].lower() + subject[1:]} determine?"
    if lower.endswith(" should include"):
        subject = text[:-15].strip()
        return f"What should {subject[:1].lower() + subject[1:]} include?"
    if lower.endswith(" should be preserved in"):
        subject = text[:-23].strip()
        return f"What should {subject[:1].lower() + subject[1:]} be preserved in?"
    if lower.endswith(" is usually conducted on requisition from"):
        subject = text[:-41].strip()
        return f"{sentence_case(subject)} is usually conducted on requisition from whom?"
    if lower.endswith(" is legally used to"):
        subject = text[:-19].strip()
        return f"What is {subject[:1].lower() + subject[1:]} legally used to do?"
    if lower.endswith(" requires a doctor to"):
        subject = text[:-21].strip()
        return f"What does {subject[:1].lower() + subject[1:]} require a doctor to do?"
    if lower.endswith(" primarily"):
        return f"{sentence_case(text)} what?"
    if lower.endswith(" mainly by"):
        subject = text[:-9].strip()
        return f"{sentence_case(subject)} occurs mainly by what mechanism?"
    if lower.endswith(" most commonly uses variation in"):
        subject = text[:-34].strip()
        return f"{sentence_case(subject)} most commonly uses variation in what?"
    if lower.endswith(" is especially useful when testing"):
        subject = text[:-36].strip()
        return f"When is {subject[:1].lower() + subject[1:]} especially useful?"
    if lower.endswith(" is meant to prove that a sample was"):
        subject = text[:-38].strip()
        return f"What is {subject[:1].lower() + subject[1:]} meant to prove about a sample?"
    if lower.endswith(" should"):
        return f"{sentence_case(text)} what?"
    if lower.endswith(" is"):
        return f"{sentence_case(text)} what?"
    if lower.endswith(" are"):
        return f"{sentence_case(text)} what?"
    if lower.endswith(" include"):
        return f"{sentence_case(text)} what?"

    if text.endswith(("?", ".")):
        return text
    return f"{text}."


def update(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    changed = 0
    bad = []
    for item in data.get("questions", []):
        if not str(item.get("id", "")).startswith(PREFIX):
            continue
        new_prompt = PROMPT_OVERRIDES.get(item.get("id"), polish(item.get("prompt", "")))
        if new_prompt != item.get("prompt"):
            item["prompt"] = new_prompt
            changed += 1
        if not item["prompt"].endswith(("?", ".")):
            bad.append(item["id"])
        if item["options"][item["answerIndex"]] != item["answer"]:
            raise ValueError(f"Answer mismatch: {item['id']}")
    if bad:
        raise ValueError(f"Unpunctuated prompts: {bad[:5]}")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main():
    for path in DATA_PATHS:
        print(f"Polished {update(path)} FMT prompts in {path}.")


if __name__ == "__main__":
    main()
