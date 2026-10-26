# -*- coding: utf-8 -*-
import sys, json, os, re
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(r'D:\medullaprep\dhruv1\scripts\grand_test')
import part2_block1
import part2_block2
import part2_block3

all_p2 = part2_block1.QUESTIONS + part2_block2.QUESTIONS + part2_block3.QUESTIONS
print(f'Total Part 2 questions: {len(all_p2)}')

textbooks = ['harrison', 'robbins', 'guyton', 'ganong', 'bailey & love', 'bailey and love', 'ghai', 'park', 'dutta', 'shaw', 'nelson', 'first aid', 'marriott']

from collections import Counter
subjects = Counter(q['subjectId'] for q in all_p2)
print('Subject distribution:')
for s, c in sorted(subjects.items()):
    print(f'  {s}: {c}')

errors = []
for idx, q in enumerate(all_p2):
    expected_id = f'fmge-gt1-q{idx+151:03d}'
    qid = q['id']
    if qid != expected_id:
        errors.append(f'ID mismatch: expected {expected_id}, got {qid}')
    if len(q['options']) != 4:
        errors.append(f'{qid}: does not have 4 options')
    if not (0 <= q['answerIndex'] <= 3):
        errors.append(f'{qid}: invalid answerIndex {q["answerIndex"]}')
    for opt in q['options']:
        if opt.endswith(';'):
            errors.append(f'{qid}: option ends with semicolon: {opt}')
        if '(' in opt and not any(c.isdigit() for c in opt):
            errors.append(f'{qid}: option has explanatory bracket: {opt}')
        if opt.lower() in ['all of the above', 'none of the above', 'both a and b']:
            errors.append(f'{qid}: prohibited option text: {opt}')
            
    full_text = (q['prompt'] + ' ' + q['explanation']).lower()
    for tb in textbooks:
        if re.search(r'\b' + re.escape(tb) + r'\b', full_text):
            if tb == 'park' and any(k in full_text for k in ['parkinson', 'parkland', 'car park']):
                continue
            if tb == 'harrison' and any(k in full_text for k in ['sulcus', 'groove']):
                continue
            errors.append(f'{qid}: mentions textbook {tb}')

if errors:
    print(f'Found {len(errors)} errors!')
    for err in errors[:15]:
        print(' -', err)
else:
    print('SUCCESS: All 150 questions in Part 2 passed 100% of all audit and validation checks!')
    out_path = r'D:\medullaprep\dhruv1\scripts\grand_test\part2_complete.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_p2, f, indent=2, ensure_ascii=False)
    print(f'Part 2 saved to: {out_path}, size: {os.path.getsize(out_path)} bytes')
