"""Apply reviewed, additive Yellowfool imports while retaining existing IDs."""
import argparse
import copy
import json
import re
import shutil
from collections import Counter
from datetime import datetime

from audit_remaining_yellowfool import ROOT, STAGE, normalized, prompt
from clean_remaining_yellowfool import SUBJECTS
import import_yellowfool_pyqs as m


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    candidates = json.loads((STAGE / 'duplicate-candidates.json').read_text(encoding='utf-8'))
    # Reviewed against stems, options and source context; the pauci-immune
    # question is a different question and must remain untouched.
    matches = {r['newId']: r['oldId'] for r in candidates if r['oldId'] != 'neet-pg-2020-q286'}
    matches.update({'neet-pg-2022-general-surgery-q021': 'neet-pg-2022-q179',
                    'neet-pg-2022-pediatrics-q009': 'neet-pg-2022-q142'})
    assert len(matches) == len(set(matches.values()))
    incoming = {s: json.loads((STAGE / f'{s}.json').read_text(encoding='utf-8')) for s in SUBJECTS}
    assert sum(map(len, incoming.values())) == 2104
    contexts = json.loads((STAGE / 'source-context-review.json').read_text(encoding='utf-8'))
    context_gaps = {}
    for row in contexts:
        if row['id'] in {'aiims-2019-general-medicine-q037', 'aiims-2018-obgyn-q012'}:
            continue  # The referenced values are already present as text.
        numbered = row['reason'] == 'numbered-options'
        if numbered and row['id'] not in {'ini-cet-2022-general-medicine-q020', 'ini-cet-2023-general-medicine-q014'}:
            numbers = [int(n) for option in row['options'] for n in re.findall(r'\d+', option)]
            if max(numbers, default=99) > 6 or not any(re.search(r'[, &-]|ONLY', option) for option in row['options']):
                continue
        context_gaps[row['id']] = 'The source PDF omits the numbered statements or table referenced by this question.' if numbered else 'The source PDF omits the investigation results referenced by this question.'
    report = {'sourceQuestions': 2104, 'subjects': [], 'matches': matches, 'answerChanges': [], 'sourceGaps': [], 'contextGaps': [], 'sourceDuplicatesCollapsed': 1}
    outputs = []
    for target in m.TARGET_FILES:
        bank = json.loads(target.read_text(encoding='utf-8'))
        before = copy.deepcopy(bank)
        for subject in bank['subjects']:
            sid = subject['id']
            if sid not in incoming:
                continue
            old_by_id = {q['id']: q for q in subject['questions']}
            by_id = copy.deepcopy(old_by_id)
            added = updated = 0
            for source in incoming[sid]:
                q = copy.deepcopy(source)
                source_id = q['id']
                if source_id == 'aiims-2019-dermatology-q018':
                    keeper_question = by_id['aiims-2019-dermatology-q008']
                    keeper_question['sourceQuestionIds'].append(source_id)
                    keeper_question['additionalSourceOccurrences'] = [{'sourceQuestionId': source_id,
                        'sourcePdfPageStart': q['sourcePdfPageStart'], 'sourcePdfPageEnd': q['sourcePdfPageEnd']}]
                    continue
                keeper = matches.get(source_id, source_id)
                old = old_by_id.get(keeper)
                q['sourceQuestionId'] = source_id
                q['sourceQuestionIds'] = [source_id]
                q['id'] = keeper
                if old:
                    updated += 1
                    # Preserve transcribed lab tables and explanatory abbreviations.
                    if len(prompt(old)) > len(prompt(q)) * 1.08:
                        q['prompt'] = '\n'.join(filter(None, [old.get('subtopic'), old.get('prompt')]))
                        q['subtopic'] = ''
                    if not q['imageUrls'] and old.get('imageUrls'):
                        q['imageUrls'] = q['images'] = old['imageUrls']
                    if any('medicomm-atlas-' in url for url in old.get('imageUrls', [])):
                        q['imageUrls'] = q['images'] = old['imageUrls']
                    if target == m.TARGET_FILES[0] and normalized(old.get('answer', '')) != normalized(q['answer']):
                        report['answerChanges'].append({'id': keeper, 'old': old.get('answer'), 'source': q['answer']})
                else:
                    added += 1
                if source_id in context_gaps and not (old and len(prompt(old)) > len(prompt(source)) * 1.08):
                    q['sourceContentStatus'] = 'incomplete-in-pdf'
                    q['sourceContentNote'] = context_gaps[source_id]
                    q['explanation'] = 'Source note: ' + context_gaps[source_id] + '\n\n' + q['explanation']
                    if target == m.TARGET_FILES[0]:
                        report['contextGaps'].append({'id': keeper, 'sourceQuestionId': source_id, 'note': context_gaps[source_id]})
                by_id[keeper] = q
                if target == m.TARGET_FILES[0] and q.get('sourceExplanationStatus'):
                    report['sourceGaps'].append({'id': keeper, 'status': q['sourceExplanationStatus']})
            subject['questions'] = sorted(by_id.values(), key=lambda q: (int(q.get('year') or 0), str(q.get('examId') or ''), int(q.get('questionNumber') or 0)))
            subject['questionCount'] = len(subject['questions'])
            assert set(old_by_id) <= set(by_id), 'Existing ID lost'
            for old_id, old in old_by_id.items():
                if old_id not in matches.values() and old_id not in {q['id'] for q in incoming[sid]}:
                    assert by_id[old_id] == old, f'Unmatched question changed: {old_id}'
            if target == m.TARGET_FILES[0]:
                report['subjects'].append({'subject': sid, 'source': len(incoming[sid]), 'added': added, 'updated': updated,
                    'totalPyqs': sum(q.get('source') not in {'ai', 'usmle'} for q in subject['questions']),
                    'images': sum(len(q['imageUrls']) for q in incoming[sid])})
        m.recompute_exam_entries(bank)
        bank['exam']['questionCount'] = sum(len(s['questions']) for s in bank['subjects'])
        for old, new in zip(before['subjects'], bank['subjects']):
            if old['id'] not in SUBJECTS:
                assert old == new, f'Unselected subject changed: {old["id"]}'
        all_ids = [q['id'] for s in bank['subjects'] for q in s['questions']]
        assert len(all_ids) == len(set(all_ids)), 'Duplicate question IDs'
        imported = [q for s in bank['subjects'] if s['id'] in SUBJECTS for q in s['questions'] if q.get('sourceQuestionId')]
        assert Counter(source_id for q in imported for source_id in q['sourceQuestionIds']) == Counter(q['id'] for qs in incoming.values() for q in qs)
        for q in imported:
            assert len(q['options']) == 4 and all(q['options']) and q['prompt'] and q['explanation'], q['id']
            assert q['answer'] == q['options'][q['answerIndex']], q['id']
            assert q['subjectId'] in SUBJECTS and q['year'] == int(q['examId'][-4:]), q['id']
            for url in q.get('imageUrls', []):
                assert (ROOT / 'public' / url.lstrip('/')).is_file(), (q['id'], url)
        outputs.append((target, bank))
    (STAGE / 'merge-report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(report['subjects'], indent=2))
    print(f"Source gaps: {len(report['sourceGaps'])}; all preservation, ID, mapping, answer and image-path checks passed")
    if not args.apply:
        return
    backup = STAGE / ('backup-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
    backup.mkdir()
    for target, bank in outputs:
        shutil.copy2(target, backup / f'{target.parent.name}-practice-question-bank.json')
        temporary = target.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        temporary.replace(target)
    shutil.copy2(ROOT / 'public/practice-question-bank.json', ROOT / 'dist/practice-question-bank.json')
    for qs in incoming.values():
        for q in qs:
            for url in q.get('imageUrls', []):
                destination = ROOT / 'dist' / url.lstrip('/')
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / 'public' / url.lstrip('/'), destination)
    print(f'APPLIED; originals backed up in {backup}')


if __name__ == '__main__':
    main()
