"""Merge Bhalani II Year questions without changing existing subjects or IDs."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import fitz
from import_short_notes import clean, slug

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = 'bhalani-ii-year'


def extract(pdf):
    subjects = {}
    subject = topic = pending = None
    paper = group = ''
    kind = None
    last_heading = None
    audit = []

    def flush():
        nonlocal pending
        if pending is None:
            return
        raw = ' '.join(pending.pop('lines')).strip()
        assert raw, pending
        pending.update(prompt=clean(raw), sourceText=raw,
                       emphasis=max([len(m) for m in re.findall(r'\*+', raw)] or [0]))
        pending['id'] = f"{SOURCE_ID}-{subject['id']}-{topic['id']}-{len(topic['questions']) + 1:03d}"
        topic['questions'].append(pending)
        pending = None

    with fitz.open(pdf) as doc:
        for page_num, page in enumerate(doc, 1):
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    spans = [s for s in line['spans'] if s['text'].strip()]
                    text = ''.join(s['text'] for s in line['spans']).strip()
                    if not text or not any(c.isalnum() for c in text):
                        continue
                    size = round(max(s['size'] for s in spans))
                    audit.append(f'{page_num:02d} [{size}] {text}')
                    if size >= 26:
                        flush()
                        name = text.split(':')[0].split(' Paper')[0]
                        sid = 'forensic-medicine' if name.startswith('Forensic') else slug(name)
                        subject = subjects.setdefault(sid, {'id': sid, 'title': name, 'sourceId': SOURCE_ID, 'topics': []})
                        paper = text
                        group = ''
                        topic = None
                        kind = None
                        last_heading = None
                    elif size > 13:
                        flush()
                        if last_heading == size and topic is not None:
                            topic['title'] += ' ' + clean(text)
                            topic['id'] = slug(paper + ' ' + topic['title'])
                            if size >= 20:
                                group = topic['title']
                        else:
                            if size >= 20:
                                group = clean(text)
                            topic = {'id': slug(paper + ' ' + text), 'title': clean(text),
                                     'section': group, 'sourcePaper': paper, 'questions': []}
                            subject['topics'].append(topic)
                        kind = None
                        last_heading = size
                    elif text in ('SN', 'LAQ'):
                        flush()
                        kind = 'short-note' if text == 'SN' else 'long-answer'
                        last_heading = None
                    else:
                        last_heading = None
                        match = re.match(r'^(\d+)\.\s*(.*)', text)
                        if match or pending is None:
                            flush()
                            assert topic is not None, (page_num, text)
                            # Two source topics omit SN; they are short-note prompts.
                            if kind is None:
                                assert topic['title'] in ('Medicolegal Aspects of Injuries', 'Abortion'), (page_num, text)
                                kind = 'short-note'
                            pending = {'sourceNumber': match[1] if match else None,
                                       'kind': kind, 'sourcePage': page_num, 'sourceId': SOURCE_ID,
                                       'lines': [match[2] if match else text]}
                        else:
                            pending['lines'].append(text)
        flush()
        source = {'id': SOURCE_ID, 'title': 'Bhalani II Year Final-1', 'fileName': pdf.name,
                  'pageCount': len(doc), 'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest()}
    for subject in subjects.values():
        subject['topics'] = [t for t in subject['topics'] if t['questions']]
        assert len({t['id'] for t in subject['topics']}) == len(subject['topics'])
    return list(subjects.values()), source, audit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf', nargs='?', type=Path,
                        default=ROOT.parent / 'shortnotes' / 'Bhalani II Year Final-1.pdf')
    args = parser.parse_args()
    subjects, source, audit = extract(args.pdf)
    destination = ROOT / 'public' / 'short-notes.json'
    bank = json.loads(destination.read_text(encoding='utf-8-sig'))
    incoming = {s['id'] for s in subjects}
    for subject in bank['subjects']:
        if subject['id'] in incoming and subject.get('sourceId') != SOURCE_ID:
            raise ValueError(f"Refusing to replace unrelated subject: {subject['id']}")
    bank['subjects'] = [s for s in bank['subjects'] if s.get('sourceId') != SOURCE_ID] + subjects
    bank['sources'] = [s for s in bank.get('sources', []) if s['id'] != SOURCE_ID] + [source]
    questions = [q for s in bank['subjects'] for t in s['topics'] for q in t['questions']]
    assert len({q['id'] for q in questions}) == len(questions)
    assert all(q['prompt'] and '\ufffd' not in q['prompt'] for q in questions)
    bank['questionCount'] = len(questions)
    destination.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    out = ROOT / 'output' / 'short-notes-second-year'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'extracted-lines.txt').write_text('\n'.join(audit), encoding='utf-8')
    (out / 'question-audit.txt').write_text('\n'.join(
        f"{s['title']} / {t['title']} / {q['kind']} / p{q['sourcePage']}: {q['prompt']}"
        for s in subjects for t in s['topics'] for q in t['questions']), encoding='utf-8')
    print(json.dumps({s['id']: {'topics': len(s['topics']), 'questions': sum(len(t['questions']) for t in s['topics'])} for s in subjects}, indent=2))


if __name__ == '__main__':
    main()
