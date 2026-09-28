"""Import the final-year Bhalani PDF, retaining source text and page references."""
import argparse
from collections import Counter
from difflib import SequenceMatcher
import hashlib
import json
import re
from pathlib import Path

import fitz
from import_short_notes import clean, slug

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = 'bhalani-final-year'
OUT = ROOT / 'output' / 'short-notes-final-year'
PAPERS = {
    'Medicine – I': ('general-medicine', 'General Medicine'),
    'Medicine – II': ('general-medicine', 'General Medicine'),
    'Surgery – I': ('general-surgery', 'General Surgery'),
    'Surgery – II': ('general-surgery', 'General Surgery'),
    'Orthopedics': ('orthopedics', 'Orthopedics'),
    'OBGY – I: Obstetrics': ('obgyn', 'Obstetrics and Gynaecology'),
    'OBGY - II: Gynaecology': ('obgyn', 'Obstetrics and Gynaecology'),
    'Paediatrics': ('pediatrics', 'Pediatrics'),
    'Ophthalmology': ('ophthalmology', 'Ophthalmology'),
    'ENT': ('ent', 'ENT'),
}
ENT_SECTIONS = {'Ear', 'Nose and Paranasal Sinuses', 'Oral Cavity and Salivary Glands',
                'Pharynx', 'Larynx and Trachea', 'Oesophagus', 'Recent Advances',
                'Clinical Methods in ENT', 'Operative Surgery'}


def display_text(text):
    text = clean(text)
    # Repair wrapping in examination references, without removing their history.
    text = re.sub(r'\(([SW])-\s+(\d{2})\)', r'(\1-\2)', text)
    corrections = {'Mestruation': 'Menstruation', 'Malpresentatiom': 'Malpresentation',
                   'Diorders': 'Disorders', 'Military Tuberculosis': 'Miliary Tuberculosis'}
    for original, corrected in corrections.items():
        text = text.replace(original, corrected)
    return text


def extract(pdf):
    subjects = {}
    subject = topic = parent_topic = pending = None
    paper = section = ''
    kind = last_heading_size = None
    last_number = 0
    audit, numbering, inferred_kinds = [], [], []
    numbered_by_page = Counter()

    def flush():
        nonlocal pending
        if pending is None:
            return
        raw = ' '.join(pending.pop('lines')).strip()
        assert raw, pending
        pending.update(sourceText=raw, prompt=display_text(raw),
                       emphasis=max([len(m) for m in re.findall(r'\*+', raw)] or [0]))
        topic['questions'].append(pending)
        pending = None

    with fitz.open(pdf) as doc:
        for page_num, page in enumerate(doc, 1):
            if page_num in (1, 2, 3, 25):
                continue  # Cover and examination-distribution tables, not prompts.
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    spans = [s for s in line['spans'] if s['text'].strip()]
                    if not spans:
                        continue
                    text = ''.join(s['text'] for s in line['spans']).strip()
                    size = round(max(s['size'] for s in spans))
                    audit.append(f'{page_num:03d} [{size}] {text}')
                    if text in PAPERS and size >= 23:
                        flush()
                        sid, title = PAPERS[text]
                        subject = subjects.setdefault(sid, {'id': sid, 'title': title,
                                                           'sourceId': SOURCE_ID, 'topics': []})
                        paper = text
                        section = ''
                        topic = parent_topic = None
                        kind = last_heading_size = None
                        continue
                    if text == 'SAQ' or text.startswith('LAQ'):
                        flush()
                        kind = 'short-note' if text == 'SAQ' else 'long-answer'
                        # TB is a smaller subheading inside Respiratory Medicine.
                        # Its short notes are followed by the parent chapter's LAQs.
                        if page_num == 19 and kind == 'long-answer':
                            assert parent_topic['title'] == 'Respiratory Medicine'
                            topic = parent_topic
                        last_heading_size = None
                        last_number = 0
                        continue
                    if size > 13:
                        flush()
                        if size == last_heading_size and topic is not None:
                            topic['title'] += ' ' + display_text(text)
                            topic['id'] = slug(paper + ' ' + section + ' ' + topic['title'])
                        else:
                            if subject['id'] == 'ent' and text in ENT_SECTIONS:
                                section = text
                            elif subject['id'] != 'ent' and size >= 18:
                                section = ''
                            if size == 14:
                                parent_topic = topic
                            topic = {'id': slug(paper + ' ' + section + ' ' + text),
                                     'title': display_text(text), 'sourcePaper': paper,
                                     'section': section, 'questions': []}
                            subject['topics'].append(topic)
                        last_heading_size = size
                        last_number = 0
                        kind = None
                        continue
                    last_heading_size = None
                    match = re.match(r'^(\d+)\.\s*(.*)', text)
                    if match:
                        flush()
                        assert topic is not None, (page_num, text)
                        if kind is None:
                            assert (page_num, topic['title']) in ((24, 'Drugs'), (77, 'Obstetrics')), (page_num, text)
                            kind = 'short-note'
                            inferred_kinds.append({'page': page_num, 'topic': topic['title'], 'kind': kind})
                        number = int(match[1])
                        if number != last_number + 1:
                            numbering.append({'page': page_num, 'topic': topic['title'],
                                              'previous': last_number, 'number': number, 'text': text})
                        last_number = number
                        numbered_by_page[page_num] += 1
                        pending = {'sourceNumber': match[1], 'kind': kind, 'sourcePage': page_num,
                                   'sourceId': SOURCE_ID, 'lines': [match[2]]}
                    else:
                        assert pending is not None, (page_num, text)
                        pending['lines'].append(text)
        flush()
        assert len(doc) == 104

    for subject in subjects.values():
        topics = {}
        for item in subject['topics']:
            if not item['questions']:
                continue
            if item['id'] in topics:
                topics[item['id']]['questions'].extend(item['questions'])
            else:
                topics[item['id']] = item
        subject['topics'] = list(topics.values())
        for topic in subject['topics']:
            for index, question in enumerate(topic['questions'], 1):
                question['id'] = f"{SOURCE_ID}-{subject['id']}-{topic['id']}-{index:03d}"
    return list(subjects.values()), audit, numbering, inferred_kinds, numbered_by_page


def normalized(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())


def compare_appendix(appendix, bank):
    comparisons = []
    for subject in appendix:
        existing = next(s for s in bank['subjects'] if s['id'] == subject['id'])
        old = [q for t in existing['topics'] for q in t['questions']]
        new = [q for t in subject['topics'] for q in t['questions']]
        assert len(old) == len(new), (subject['id'], len(old), len(new))
        for previous, current in zip(old, new):
            ratio = SequenceMatcher(None, normalized(previous['prompt']), normalized(current['prompt'])).ratio()
            comparisons.append({'subject': subject['id'], 'page': current['sourcePage'],
                                'similarity': round(ratio, 4), 'existing': previous['prompt'], 'appendix': current['prompt']})
    return comparisons


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf', nargs='?', type=Path, default=ROOT.parent / 'shortnotes' / 'Bhalani Final Year.pdf')
    parser.add_argument('--audit-only', action='store_true')
    args = parser.parse_args()
    all_subjects, audit, numbering, inferred, numbered_by_page = extract(args.pdf)
    subjects = [s for s in all_subjects if s['id'] not in ('ent', 'ophthalmology')]
    appendix = [s for s in all_subjects if s['id'] in ('ent', 'ophthalmology')]
    destination = ROOT / 'public' / 'short-notes.json'
    bank = json.loads(destination.read_text(encoding='utf-8-sig'))
    comparisons = compare_appendix(appendix, bank)
    questions = [q for s in subjects for t in s['topics'] for q in t['questions']]
    assert Counter(q['sourcePage'] for q in questions) == Counter({p: n for p, n in numbered_by_page.items() if p <= 86})
    # Independent plain-text extraction must agree on every page, not just totals.
    with fitz.open(args.pdf) as document:
        raw_counts = Counter({p: len(re.findall(r'^\s*\d+\.\s', page.get_text(), re.M))
                              for p, page in enumerate(document, 1) if 4 <= p <= 86 and p != 25})
    assert Counter(q['sourcePage'] for q in questions) == raw_counts
    # These five numbering errors were checked in the source; none drops a prompt.
    assert [(n['page'], n['previous'], n['number']) for n in numbering] == [
        (6, 1, 3), (6, 5, 5), (12, 1, 1), (38, 1, 1), (56, 1, 1)]
    report = {'sourcePages': 104, 'questionCount': len(questions),
              'subjects': {s['id']: {'topics': len(s['topics']), 'questions': sum(len(t['questions']) for t in s['topics'])} for s in subjects},
              'kinds': dict(Counter(q['kind'] for q in questions)),
              'numberingIrregularities': numbering, 'inferredQuestionTypes': inferred,
              'existingAppendixQuestions': len(comparisons),
              'appendixMinimumSimilarity': min(c['similarity'] for c in comparisons)}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'extracted-lines.txt').write_text('\n'.join(audit), encoding='utf-8')
    (OUT / 'question-audit.txt').write_text('\n'.join(
        f"{s['title']} / {t['sourcePaper']} / {t['title']} / {q['kind']} / p{q['sourcePage']}: {q['prompt']}"
        for s in subjects for t in s['topics'] for q in t['questions']), encoding='utf-8')
    (OUT / 'appendix-comparison.json').write_text(json.dumps(comparisons, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUT / 'import-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if not args.audit_only:
        assert min(c['similarity'] for c in comparisons) >= .8, 'Review appendix differences before importing.'
        incoming = {s['id'] for s in subjects}
        assert not any(s['id'] in incoming and s.get('sourceId') != SOURCE_ID for s in bank['subjects'])
        bank['subjects'] = [s for s in bank['subjects'] if s.get('sourceId') != SOURCE_ID] + subjects
        source = {'id': SOURCE_ID, 'title': 'Bhalani Final Year', 'fileName': args.pdf.name,
                  'pageCount': 104, 'sha256': hashlib.sha256(args.pdf.read_bytes()).hexdigest()}
        bank['sources'] = [s for s in bank.get('sources', []) if s['id'] != SOURCE_ID] + [source]
        all_questions = [q for s in bank['subjects'] for t in s['topics'] for q in t['questions']]
        assert len({q['id'] for q in all_questions}) == len(all_questions)
        assert all(q['prompt'] and '\ufffd' not in q['prompt'] for q in all_questions)
        bank['questionCount'] = len(all_questions)
        destination.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
