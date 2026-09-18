"""Remove PDF navigation artifacts; explicitly label source explanation gaps."""
import html
import json
import re
from audit_remaining_yellowfool import STAGE

SUBJECTS = ['general-medicine', 'general-surgery', 'obgyn', 'pediatrics', 'orthopedics', 'psychiatry', 'dermatology', 'radiology']


def clean(text):
    text = re.sub(r"&(LT|GT|AMP|QUOT);", lambda m: m[0].lower(), text)
    return html.unescape(text).strip()


def main():
    for subject in SUBJECTS:
        path = STAGE / f"{subject}.json"
        questions = json.loads(path.read_text(encoding="utf-8"))
        gaps = 0
        for q in questions:
            fallback = q['explanation'] == f"Correct answer: {q['answer']}"
            q['prompt'] = clean(q['prompt'])
            q['options'] = [clean(re.split(r"\nAnswer Key\b", option)[0]) for option in q['options']]
            q['answer'] = q['options'][q['answerIndex']]
            q['explanation'] = clean(re.split(r"\n(?:\d+\n)?[A-Z &]+\nPYQs \(NEET", q['explanation'])[0])
            if fallback:
                q['explanation'] = f"Correct answer: {q['answer']}. The source PDF supplies the answer key but omits the detailed explanation for this question."
                q['sourceExplanationStatus'] = 'missing-in-pdf'
                gaps += 1
            if q['id'] == 'ini-cet-2024-general-surgery-q002':
                q['sourceExplanationStatus'] = 'truncated-in-pdf'
            assert 'Answer Key' not in ' '.join(q['options'])
            assert 'Chapter\nTitle\nPage' not in q['explanation']
        path.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'{subject}: {len(questions)} cleaned, {gaps} source explanation gaps')


if __name__ == '__main__':
    main()
