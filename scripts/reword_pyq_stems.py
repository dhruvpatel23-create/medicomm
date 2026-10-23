"""Conservative PYQ wording edits; no medical facts or option fields are rewritten."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANKS = [ROOT / folder / 'practice-question-bank.json' for folder in ('data', 'public', 'dist')]
AUDIT = ROOT / 'output/pyq-wording/changes.json'

# Only generic question framing and image/examination introductions are eligible.
RULES = [
    ('which-options', r'\bwhich\s+of\s+the\s+following\b', 'which of these'),
    ('which-one', r'\bwhich\s+one\s+of\s+the\s+following\b', 'which one of these'),
    ('all-options', r'\ball\s+of\s+the\s+following\b', 'all of these'),
    ('all-options-short', r'\ball\s+the\s+following\b', 'all these'),
    ('among-options', r'\bamong(?:st)?\s+the\s+following\b', 'among these'),
    ('regarding', r'\bregarding\b', 'concerning'),
    ('shown-below', r'\bshown\s+below\b', 'displayed below'),
    ('given-below', r'\bgiven\s+below\b', 'provided below'),
    ('image-below', r'\bimage\s+below\b', 'image presented below'),
    ('given-image', r'\bgiven\s+(?=image\b|picture\b|diagram\b|figure\b)', 'provided '),
    ('examination-introduction', r'\bon\s+examination\b', 'upon examination'),
    ('guideline-introduction', r'\bas\s+per\b', 'according to'),
    ('identify-imperative', r'^identify\b', 'select'),
    ('calculate-imperative', r'^calculate\b', 'determine'),
    ('which-fact', r'\bwhich(?=\s+(?:nerve|muscle|artery|vein|structure|condition|disease|drug|test|type|part|area|layer|joint|bone|cell|hormone|enzyme|vitamin|organ|vessel|finding|level|diagnosis|sign|fracture|symptom|investigation|treatment|imaging|compartment|method|protein|factor|stage|region|feature|site|mechanism|receptor|syndrome|number|dose|tumor|tumour|disorder)\b)', 'what'),
    ('image-reference', r'\bin\s+the\s+image\b', 'in the provided image'),
]

def same_case(old, new):
    if old.isupper(): return new.upper()
    if old[:1].isupper(): return new[:1].upper() + new[1:]
    return new

def rewrite(stem):
    for name, pattern, replacement in RULES:
        changed, count = re.subn(pattern, lambda m: same_case(m[0], replacement), stem, count=1, flags=re.I)
        if count: return changed, name
    # Reframe a direct final question without changing the requested fact.
    match = re.search(r'(?P<start>^|[.!?]\s+)(?P<ask>what\s+(?:is|are)\s+)(?P<fact>the\s+[^?]+)\?\s*$', stem, re.I)
    if match:
        prefix = same_case(match['ask'], 'Indicate ')
        return stem[:match.start('ask')] + prefix + match['fact'] + '.', 'direct-question-framing'
    # Short factual stems retain every original word; only the presentation changes.
    label = 'Complete the statement:' if re.search(r'_{2,}', stem) else 'Question:'
    if stem.isupper(): label = label.upper()
    return label + '\n' + stem, 'statement-framing' if re.search(r'_{2,}', stem) else 'answer-framing'

def selected(q):
    return q.get('source') in (None, 'official') and re.match(r'^(neet-pg|ini-cet|aiims)-', q.get('examId', ''))

def questions(bank):
    return [q for subject in bank['subjects'] for q in subject.get('questions', []) if selected(q)]

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    banks = [json.loads(p.read_text(encoding='utf-8-sig')) for p in BANKS]
    if AUDIT.exists():
        changes = json.loads(AUDIT.read_text(encoding='utf-8'))['changes']
    else:
        changes = []
        for q in questions(banks[0]):
            after, rule = rewrite(q['prompt'])
            changes.append({'id': q['id'], 'before': q['prompt'], 'after': after, 'rule': rule,
                'unchangedFieldsSha256': digest({k:v for k,v in q.items() if k != 'prompt'})})
    lookup = {q['id']: q for q in changes}
    assert len(lookup) == len(changes) == 5025, 'Unexpected target count; stop for review.'
    for bank in banks:
        target = questions(bank)
        assert {q['id'] for q in target} == set(lookup)
        original = json.loads(json.dumps(bank))
        for q in target:
            change = lookup[q['id']]
            assert q['prompt'] in (change['before'], change['after']), q['id']
            assert digest({k:v for k,v in q.items() if k != 'prompt'}) == change['unchangedFieldsSha256'], q['id']
            assert re.findall(r'\d+(?:[.,]\d+)*', change['before']) == re.findall(r'\d+(?:[.,]\d+)*', change['after']), q['id']
            protected = r'\b(?:not|except|false|incorrect|never|always|least|most|only|all|no|none|without|cannot|unlikely)\b'
            assert re.findall(protected, change['before'], re.I) == re.findall(protected, change['after'], re.I), q['id']
            q['prompt'] = change['after']
        # Whole-document equality after restoring only the edited stems.
        restored = json.loads(json.dumps(bank))
        old_prompts = {q['id']: q['prompt'] for q in questions(original)}
        for q in questions(restored): q['prompt'] = old_prompts[q['id']]
        assert restored == original, 'A non-prompt field changed.'
    summary = {'questions': len(changes), 'rules': dict(Counter(c['rule'] for c in changes)),
        'verified': 'Options, option order, answer keys, explanations, images, metadata, numbers and negation qualifiers preserved.'}
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text(json.dumps({'summary': summary, 'changes': changes}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    if args.apply:
        for p, bank in zip(BANKS, banks): p.write_text(json.dumps(bank, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'applied': args.apply, **summary}, indent=2))

if __name__ == '__main__': main()
