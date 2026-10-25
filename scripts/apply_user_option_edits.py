"""Apply the user's exact correctOption/otherOptions edits, preserving key positions."""
import argparse
import json
import sqlite3
from pathlib import Path
from clean_correct_options import read, questions

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/topic-wise-local-rewrite'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    edits = read(OUT / 'correct-options-to-edit.json')['questions']
    with sqlite3.connect(OUT / 'work.sqlite') as db:
        original = {q['id']: q for raw, in db.execute('SELECT input FROM work') for q in [json.loads(raw)]}
    assert len(edits) == len({q['id'] for q in edits}) == len(original)
    assert {q['id'] for q in edits} == set(original)
    revisions = {}
    for edit in edits:
        old = original[edit['id']]
        assert edit['question'] == old['prompt'] and edit['answerIndex'] == old['answerIndex'], edit['id']
        assert edit['originalCorrectOption'] == old['answer'], edit['id']
        options = list(edit['otherOptions'])
        options.insert(edit['answerIndex'], edit['correctOption'])
        assert len(options) == 4 and all(isinstance(o, str) and o.strip() for o in options), edit['id']
        assert len({o.strip().casefold() for o in options}) == 4, edit['id']
        revisions[edit['id']] = dict(id=edit['id'], prompt=old['prompt'], beforeOptions=old['options'],
                                    beforeAnswer=old['answer'], answerIndex=old['answerIndex'], options=options)
    prepared, counts = [], {}
    for name in ['data/users.json', 'data/practice-question-bank.json', 'public/practice-question-bank.json',
                 'dist/practice-question-bank.json', 'runtime-data/users.json']:
        path = ROOT / name
        if not path.exists():
            continue
        bank = read(path)
        found, changed = set(), 0
        for q in questions(bank):
            r = revisions.get(q.get('id'))
            if not r:
                continue
            assert q['source'] == 'ai' and q['prompt'] == r['prompt'], q['id']
            assert q['answerIndex'] == r['answerIndex'], q['id']
            assert q['options'] in [r['beforeOptions'], r['options']], q['id']
            assert q['answer'] == q['options'][q['answerIndex']], q['id']
            found.add(q['id'])
            if q['options'] == r['options']:
                continue
            preserved = {k: v for k, v in q.items() if k not in ['options', 'answer']}
            q['options'] = r['options'].copy()
            q['answer'] = q['options'][q['answerIndex']]
            assert preserved == {k: v for k, v in q.items() if k not in ['options', 'answer']}
            changed += 1
        if not name.startswith('runtime-data/'):
            assert found == set(revisions), name
        counts[name] = changed
        prepared.append((path, bank, changed))
    actual = [r for r in revisions.values() if r['options'] != r['beforeOptions']]
    manifest = {'version': 1, 'source': 'User-edited correct-options-to-edit.json', 'questions': actual}
    if args.apply:
        for path, bank, changed in prepared:
            if changed:
                temp = path.with_suffix(path.suffix + '.option-edits.tmp')
                temp.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                temp.replace(path)
        (ROOT / 'data/topic-wise-user-option-edits.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = {'inputQuestions': len(edits), 'changedQuestions': len(actual), 'unchangedQuestions': len(edits)-len(actual),
              'applied': args.apply, 'files': counts}
    (OUT / 'user-edits-application-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
