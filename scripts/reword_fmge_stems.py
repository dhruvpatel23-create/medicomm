"""Apply the conservative PYQ wording procedure to FMGE stems only."""
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pyq_wording', ROOT / 'scripts/reword_pyq_stems_v2.py')
wording = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wording)
AUDIT = ROOT / 'output/fmge-wording/changes.json'


def questions(value):
    if isinstance(value, dict):
        if 'prompt' in value and 'options' in value:
            yield value
        else:
            for child in value.values(): yield from questions(child)
    elif isinstance(value, list):
        for child in value: yield from questions(child)


def main():
    paths = [ROOT / folder / 'fmge-question-bank.json' for folder in ('data', 'public', 'dist')]
    paths = [p for p in paths if p.exists()]
    banks = [json.loads(p.read_text(encoding='utf-8-sig')) for p in paths]
    previous = json.loads(AUDIT.read_text(encoding='utf-8'))['changes'] if AUDIT.exists() else None
    changes = previous or []
    if previous is None:
        for q in questions(banks[0]):
            after, rules = wording.rewrite(q['prompt'])
            changes.append({'id': q['id'], 'before': q['prompt'], 'after': after, 'rules': rules,
                'unchangedFieldsSha256': wording.base.digest({k:v for k,v in q.items() if k != 'prompt'})})
    lookup = {c['id']:c for c in changes}
    assert len(lookup) == len(changes) == 2895, 'Unexpected FMGE question count.'
    for bank in banks:
        original = json.loads(json.dumps(bank))
        targets = list(questions(bank))
        assert {q['id'] for q in targets} == set(lookup)
        for q in targets:
            c = lookup[q['id']]
            assert q['prompt'] in (c['before'], c['after']), q['id']
            assert wording.base.digest({k:v for k,v in q.items() if k != 'prompt'}) == c['unchangedFieldsSha256'], q['id']
            assert re.findall(r'\d+(?:[.,]\d+)*', c['before']) == re.findall(r'\d+(?:[.,]\d+)*', c['after']), q['id']
            protected = r'\b(?:not|except|false|incorrect|never|always|least|most|only|all|no|none|without|cannot|unlikely)\b'
            assert Counter(re.findall(protected,c['before'].lower())) == Counter(re.findall(protected,c['after'].lower())), q['id']
            q['prompt'] = c['after']
        restored = json.loads(json.dumps(bank))
        old_prompts = {q['id']:q['prompt'] for q in questions(original)}
        for q in questions(restored): q['prompt'] = old_prompts[q['id']]
        assert restored == original, 'Non-stem data changed.'
    summary = {'total':len(changes), 'reworded':sum(c['before'] != c['after'] for c in changes),
        'retained_for_precision':sum(c['before'] == c['after'] for c in changes),
        'multiple_edits':sum(len(c['rules']) > 1 for c in changes),
        'checks':'Options, order, keys, explanations and all non-stem fields unchanged; numbers and negation qualifiers preserved.'}
    AUDIT.parent.mkdir(parents=True,exist_ok=True)
    AUDIT.write_text(json.dumps({'summary':summary,'changes':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for p,bank in zip(paths,banks): p.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__ == '__main__': main()
