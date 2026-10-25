"""Apply approved correct-option-only edits offline; never truncate by regex.

The reviewed manifest records the original options and approved shortened answer.
All other options, stems, explanations, IDs and answer indices must stay identical.
Run without --apply to validate and report; use --apply to update local banks.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/topic-wise-correct-option-cleanup.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def questions(bank):
    yield from bank.get('questions', [])
    for subject in bank.get('subjects', []):
        yield from subject.get('questions', [])


def validate_revision(revision):
    index = revision['answerIndex']
    before, after = revision['beforeOptions'], revision['options']
    assert len(before) == len(after) == 4, revision['id']
    assert [i for i in range(4) if before[i] != after[i]] == [index], revision['id']
    assert revision['beforeAnswer'] == before[index], revision['id']
    assert 0 < len(after[index]) < len(before[index]), revision['id']
    assert after[index].strip() == after[index], revision['id']
    assert len(set(s.casefold().strip() for s in after)) == 4, revision['id']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--manifest', type=Path, default=MANIFEST)
    parser.add_argument('--report', type=Path,
                        default=ROOT / 'output/topic-wise-option-audit/correct-option-cleanup-report.json')
    args = parser.parse_args()
    manifest = read(args.manifest)
    scope = set(manifest['scopeQuestionIds'])
    revisions = {r['id']: r for r in manifest['questions']}
    assert len(revisions) == len(manifest['questions'])
    assert set(revisions) <= scope
    for revision in revisions.values():
        validate_revision(revision)
    prepared = []
    for name in ['data/users.json', 'data/practice-question-bank.json',
                 'public/practice-question-bank.json', 'dist/practice-question-bank.json']:
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
            assert q['answer'] == q['options'][q['answerIndex']], q['id']
            assert q['options'] in [r['beforeOptions'], r['options']], q['id']
            found.add(q['id'])
            if q['options'] == r['options']:
                continue
            preserved = {k: v for k, v in q.items() if k not in ['options', 'answer']}
            q['options'] = r['options'].copy()
            q['answer'] = q['options'][q['answerIndex']]
            assert preserved == {k: v for k, v in q.items() if k not in ['options', 'answer']}
            changed += 1
        assert found == set(revisions), name
        prepared.append((path, bank, changed))
    report = {'screened': len(scope), 'shortened': len(revisions),
              'unchanged': len(scope - set(revisions)), 'paidApiCalls': 0,
              'policy': 'Only explicitly approved redundant wording removed. Unchanged does not mean certified bias-free.',
              'unchangedQuestionIds': sorted(scope - set(revisions))}
    out = args.report
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    if args.apply:
        # All files are validated before the first write. Re-running is idempotent.
        for path, bank, changed in prepared:
            if changed:
                path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(f'{path.relative_to(ROOT)}: {changed} correct options updated')
    print(json.dumps({k: v for k, v in report.items() if k != 'unchangedQuestionIds'}))


if __name__ == '__main__':
    main()
