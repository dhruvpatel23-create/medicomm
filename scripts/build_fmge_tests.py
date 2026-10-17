"""Build reproducible FMGE tests from existing exam recalls; never invent filler.

The supplied FMGE_Subject_Wise_Guide.pdf is the blueprint, not an official bulletin.
Run from the repository root: python scripts/build_fmge_tests.py
"""
import collections
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = [
    ('anatomy', 'Anatomy', 17), ('physiology', 'Physiology', 17),
    ('biochemistry', 'Biochemistry', 17), ('pathology', 'Pathology', 13),
    ('microbiology', 'Microbiology', 13), ('pharmacology', 'Pharmacology', 13),
    ('forensic-medicine', 'Forensic Medicine', 10), ('general-medicine', 'General Medicine', 33),
    ('psychiatry', 'Psychiatry', 5), ('dermatology', 'Dermatology & STD', 5),
    ('radiotherapy', 'Radiotherapy', 5), ('general-surgery', 'General Surgery', 32),
    ('anesthesia', 'Anesthesiology', 5), ('orthopedics', 'Orthopedics', 5),
    ('radiology', 'Radiodiagnosis', 5), ('pediatrics', 'Pediatrics', 15),
    ('ophthalmology', 'Ophthalmology', 15), ('ent', 'ENT', 15),
    ('obgyn', 'Obstetrics & Gynecology', 30), ('community-medicine', 'Community Medicine (PSM)', 30),
]
ALIASES = {'Anaesthesia': 'anesthesia', 'Surgery': 'general-surgery', 'Medicine': 'general-medicine',
           'PSM': 'community-medicine', 'Gynaecology & Obstetrics': 'obgyn', 'Orthopaedics': 'orthopedics',
           'Forensic Medicine': 'forensic-medicine'}
# Radiation oncology is integrated into several source subjects. Explicitly
# classify these existing exam questions instead of substituting diagnostic imaging.
RADIOTHERAPY = {
    'fmge-2020-august-q110', 'fmge-2020-august-q214', 'fmge-2020-august-q261',
    'fmge-2020-december-q147', 'fmge-2021-december-q139', 'fmge-2022-june-q065',
    'fmge-2022-june-q262', 'fmge-2024-june-q035', 'fmge-2024-june-q046',
    'fmge-2025-january-part-2-q060', 'neet-pg-2020-q074', 'neet-pg-2020-q093',
    'neet-pg-2018-radiology-q009', 'aiims-2020-radiology-q001',
}
# The radiation-pneumonitis recall states the imaging finding in words; its
# accompanying source image adds no data needed to answer this question.
SELF_CONTAINED_WITH_SOURCE_IMAGE = {'fmge-2025-january-part-2-q060'}
CONFLICTED_RECALLS = {'fmge-2022-june-q052', 'neet-pg-2020-q074'}

def normalized(text):
    return re.sub(r'[^a-z0-9]', '', str(text).lower())

def clean(text):
    return re.sub(r'\s+', ' ', str(text or '')).strip()

def clean_prompt(text):
    text = clean(text)
    match = re.match(r'^(?:Q(?:uestion)?\.?\s*)?(\d{1,3})[.)]\s+(?=[A-Za-z])', text, re.I)
    if not match:
        return text
    remainder = text[match.end():]
    return text if re.search(r'(?:^|\s)' + str(int(match.group(1)) + 1) + r'[.)]\s+[A-Za-z]', remainder) else remainder

def build():
    fmge = json.loads((ROOT/'data/fmge-question-bank.json').read_text(encoding='utf-8-sig'))
    practice = json.loads((ROOT/'data/practice-question-bank.json').read_text(encoding='utf-8-sig'))
    raw = [(q, ALIASES.get(q.get('subject'), q.get('subject', '').lower()), 'fmge') for s in fmge['sessions'] for q in s['questions']]
    raw += [(q, s['id'], 'practice') for s in practice['subjects'] for q in s['questions'] if q.get('source') == 'official']
    subjects = {s[0] for s in BLUEPRINT}
    rejected = collections.Counter()
    pools = collections.defaultdict(list)
    seen = set()
    # Reject contradictory keys for an identical stem/options, across both banks.
    keys = collections.defaultdict(set)
    for q, _, _ in raw:
        if isinstance(q.get('answerIndex'), int) and 0 <= q['answerIndex'] < len(q.get('options', [])):
            keys[normalized(q.get('prompt')) + '|'+ '|'.join(sorted(normalized(o) for o in q['options']))].add(normalized(q['options'][q['answerIndex']]))
    for q, subject, origin in raw:
        if q['id'] in RADIOTHERAPY:
            subject = 'radiotherapy'
        options = [clean(o) for o in q.get('options', [])]
        prompt, explanation = clean_prompt(q.get('prompt')), clean(q.get('explanation'))
        answer = q.get('answerIndex')
        reason = None
        if q['id'] in CONFLICTED_RECALLS: reason = 'conflicting recall variants'
        elif subject not in subjects: reason = 'unmapped subject'
        elif len(options) != 4 or len(set(map(normalized, options))) != 4 or any(not o for o in options): reason = 'invalid options'
        elif type(answer) is not int or not 0 <= answer < 4: reason = 'invalid key'
        elif q.get('answer') and normalized(q['answer']) != normalized(options[answer]): reason = 'key mismatch'
        elif len(keys[normalized(q.get('prompt')) + '|' + '|'.join(sorted(normalized(o) for o in q['options']))]) > 1: reason = 'conflicting source keys'
        elif q.get('reviewNote'): reason = 'unresolved editorial flag'
        elif (len(prompt) < 45 and q['id'] != 'neet-pg-2018-radiology-q009') or len(explanation) < 100: reason = 'insufficient stem or rationale'
        elif q['id'] not in SELF_CONTAINED_WITH_SOURCE_IMAGE and any(q.get(k) for k in ['imageUrls', 'images', 'imageUrl', 'image', 'explanationImageUrls']): reason = 'image question reserved for reviewed image tests'
        elif re.search(r'(shown|given|following|below|above).{0,35}(image|figure|diagram|photograph|picture)|(?:image|figure|diagram|photograph|picture).{0,30}(shown|given|below|above)|identify the (instrument|image|figure|procedure)|match the following', prompt, re.I): reason = 'missing visual or matching context'
        elif re.search(r'placeholder|sample question|test question|lorem ipsum|option [abcd]$', prompt, re.I): reason = 'placeholder'
        fingerprint = normalized(prompt)
        if not reason and fingerprint in seen: reason = 'duplicate stem'
        if reason:
            rejected[reason] += 1
            continue
        seen.add(fingerprint)
        pools[subject].append({
            'id': q['id'], 'subjectId': subject, 'subjectTitle': dict((s[0], s[1]) for s in BLUEPRINT)[subject],
            'prompt': prompt, 'options': options, 'answerIndex': answer, 'explanation': explanation,
            'topic': clean(q.get('topic')), 'source': q.get('source', 'official'),
            'sourceBank': origin, 'sourceExam': q.get('examTitle') or q.get('sourceExam') or 'Exam recall',
            'sourcePdf': q.get('sourcePdf'), 'sourcePage': q.get('sourcePdfPageStart'),
        })
    tests = [{'id': f'fmge-practice-{i}', 'title': f'TEST{i}', 'questions': []} for i in range(1, 4)]
    reused = []
    for subject, _, count in BLUEPRINT:
        pool = pools[subject]
        # Prioritize FMGE clinical stems, then substantive questions from the
        # broader exam library. Hash breaks ties reproducibly, not bank order.
        pool.sort(key=lambda q: (q['sourceBank'] != 'fmge', -min(len(q['prompt']), 350), hashlib.sha256(q['id'].encode()).hexdigest()))
        if len(pool) < count:
            raise ValueError(f'{subject}: only {len(pool)} eligible questions; need {count}')
        for i, test in enumerate(tests):
            chosen = [pool[(i*count+j) % len(pool)] for j in range(count)]
            if (i+1)*count > len(pool): reused.append({'subject': subject, 'test': test['id'], 'poolSize': len(pool)})
            test['questions'].extend(chosen)
    for test in tests:
        # Interleave subjects, with exactly 150 questions in each timed part.
        test['questions'].sort(key=lambda q: hashlib.sha256((test['id']+q['id']).encode()).hexdigest())
        assert len(test['questions']) == 300
        assert len({q['id'] for q in test['questions']}) == 300
    document = {'version': 'fmge-guide-v1', 'guide': 'FMGE_Subject_Wise_Guide.pdf',
                'blueprint': [{'id': s, 'title': title, 'count': count} for s, title, count in BLUEPRINT],
                'parts': 2, 'questionsPerPart': 150, 'minutesPerPart': 150, 'passMark': 150,
                'tests': tests}
    (ROOT/'data/fmge-practice-tests.json').write_text(json.dumps(document, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    report = {'tests': [{ 'id': t['id'], 'questions': len(t['questions']), 'sources': dict(collections.Counter(q['sourceBank'] for q in t['questions'])) } for t in tests],
              'eligibleBySubject': {s: len(pools[s]) for s, _, _ in BLUEPRINT}, 'excluded': dict(rejected),
              'crossTestReuse': reused, 'uniqueQuestions': len({q['id'] for t in tests for q in t['questions']}),
              'reviewScope': 'Structural and source-quality screening of existing exam recalls; not a claim of independent clinical validation of every answer.'}
    (ROOT/'docs/fmge-practice-test-selection.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    build()
