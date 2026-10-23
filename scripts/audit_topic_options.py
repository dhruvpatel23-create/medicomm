"""Offline audit and explicit, reviewed option edits. No API calls.

Run without arguments to audit. --apply installs only the human-reviewed sets
in reviewed_topic_options.py, preserving stems, explanations and answer indices.
The saved manifest doubles as a rollback record and server override for old DBs.
"""
import argparse
import collections
import json
from pathlib import Path

from reviewed_topic_options import REVISIONS

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/topic-wise-option-revisions.json'
OUT = ROOT / 'output/topic-wise-option-audit'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def questions(bank):
    yield from bank.get('questions', [])
    for subject in bank.get('subjects', []):
        yield from subject.get('questions', [])


def answer_index(q):
    index = q.get('answerIndex')
    if not isinstance(index, int):
        index = q['options'].index(q['answer'])
    if not 0 <= index < len(q['options']):
        raise ValueError(f'Invalid answer index: {q["id"]}')
    if q.get('answer') and q['answer'] != q['options'][index]:
        raise ValueError(f'Conflicting answer key: {q["id"]}')
    return index


def audit(bank):
    rows = []
    for q in questions(bank):
        if q.get('source') != 'ai':
            continue
        index = answer_index(q)
        lengths = list(map(len, q['options']))
        longest_wrong = max(length for i, length in enumerate(lengths) if i != index)
        rows.append({'id': q['id'], 'subject': q.get('subjectId'),
                     'lengths': lengths, 'answerIndex': index,
                     'correctToLongestDistractor': round(lengths[index] / max(1, longest_wrong), 3),
                     'reviewed': q['id'] in REVISIONS})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    source = read(ROOT / 'data/users.json')
    by_id = {q['id']: q for q in questions(source) if q.get('source') == 'ai'}
    existing = read(MANIFEST) if MANIFEST.exists() else {'version': 1, 'questions': []}
    old = {q['id']: q for q in existing['questions']}
    records = []
    for qid, options in REVISIONS.items():
        q = by_id[qid]
        index = answer_index(q)
        assert len(options) == len(q['options']) == 4, qid
        assert len(set(o.casefold().strip() for o in options)) == 4, qid
        assert all(isinstance(o, str) and o.strip() == o and o for o in options), qid
        record = old.get(qid) or {'id': qid, 'prompt': q['prompt'],
            'beforeOptions': q['options'], 'beforeAnswer': q['answer'],
            'answerIndex': index}
        assert q['prompt'] == record['prompt'] and index == record['answerIndex'], qid
        assert q['options'] in [record['beforeOptions'], record.get('options')], qid
        records.append({**record, 'options': options})
    lookup = {q['id']: q for q in records}
    prepared = []
    for name in ['data/users.json', 'data/practice-question-bank.json',
                 'public/practice-question-bank.json', 'dist/practice-question-bank.json']:
        path = ROOT / name
        if not path.exists():
            continue
        bank = read(path)
        changed = 0
        for q in questions(bank):
            revision = lookup.get(q.get('id'))
            if q.get('source') != 'ai' or not revision:
                continue
            assert q['prompt'] == revision['prompt'], q['id']
            assert answer_index(q) == revision['answerIndex'], q['id']
            assert q['options'] in [revision['beforeOptions'], revision['options']], q['id']
            if q['options'] != revision['options']:
                q['options'] = revision['options']
                q['answer'] = q['options'][revision['answerIndex']]
                changed += 1
        prepared.append((path, bank, changed))
    OUT.mkdir(parents=True, exist_ok=True)
    before = audit(source)
    result = next(bank for path, bank, _ in prepared if path == ROOT / 'data/users.json')
    after = audit(result)
    summary = {'total': len(before), 'reviewed': len(records),
               'soleLongestBefore': sum(r['correctToLongestDistractor'] > 1 for r in before),
               'soleLongestAfter': sum(r['correctToLongestDistractor'] > 1 for r in after),
               'unreviewedSoleLongest': sum(r['correctToLongestDistractor'] > 1 and not r['reviewed'] for r in after),
               'paidApiCalls': 0,
               'note': 'Longest-option status is a review signal, not proof that an option is defective. No automatic medical rewrites.'}
    (OUT / 'report.json').write_text(json.dumps({'summary': summary, 'questions': after}, indent=2), encoding='utf-8')
    pending = sorted((r for r in after if not r['reviewed'] and r['correctToLongestDistractor'] > 1), key=lambda r: -r['correctToLongestDistractor'])
    (OUT / 'pending-review.json').write_text(json.dumps(pending, indent=2), encoding='utf-8')
    if args.apply:
        MANIFEST.write_text(json.dumps({'version': 1, 'questions': records}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        for path, bank, changed in prepared:
            if changed:
                path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(f'{path.relative_to(ROOT)}: {changed} option sets updated')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
