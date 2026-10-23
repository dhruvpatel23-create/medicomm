"""Second wording pass: multiple local edits, preserving the original factual content."""
import argparse
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('base', ROOT / 'scripts/reword_pyq_stems.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
AUDIT = ROOT / 'output/pyq-wording/revision-2.json'
EXTRA = [
    ('true-about', r'\btrue\s+about\b', 'true with respect to'),
    ('false-about', r'\bfalse\s+about\b', 'false with respect to'),
    ('statement-about', r'\bstatement\s+about\b', 'statement concerning'),
    ('statements-about', r'\bstatements\s+about\b', 'statements concerning'),
    ('investigation-wording', r'\brevealed\b', 'showed'),
    ('complaint-present', r'\bcomplains\s+of\b', 'reports'),
    ('complaint-past', r'\bcomplained\s+of\b', 'reported'),
    ('complaint-description', r'\bpresents\s+with\s+complaints\s+of\b', 'reports'),
    ('complaint-description-past', r'\bpresented\s+with\s+complaints\s+of\b', 'reported'),
    ('case-reference', r'\bin\s+this\s+case\b', 'in this situation'),
    ('patient-reference', r'\bin\s+this\s+patient\b', 'in the patient described'),
    ('history-reference', r'\bfor\s+the\s+last\b', 'for the past'),
    ('examination-timing', r'\bduring\s+examination\b', 'during the examination'),
    ('shown-image', r'\bshown\s+in\s+the\s+image\b', 'displayed in the image'),
    ('marked-arrow', r'\bmarked\s+by\s+the\s+arrow\b', 'indicated by the arrow'),
    ('marked-asterisk', r'\bmarked\s+with\s+the\s+asterisk\b', 'indicated by the asterisk'),
    ('match-instruction', r'\bmatch\s+the\s+following\b', 'pair the following'),
    ('sequence-instruction', r'\barrange\s+the\s+following\b', 'place the following'),
    ('manage-question', r'\bhow\s+will\s+you\s+manage\s+this\s+patient\?', 'how would you manage the patient described?'),
    ('advice-question', r'\bwhat\s+would\s+your\s+advice\s+be\?', 'what advice would you give?'),
    ('next-question', r'\bwhat\s+should\s+be\s+done\s+next\?', 'what should the next step be?'),
]


def replace_once(text, pattern, replacement):
    return re.subn(pattern, lambda m: base.same_case(m[0], replacement), text, count=1, flags=re.I)


def rewrite(original):
    text = original
    rules = []
    # Apply several compatible edits rather than stopping after the first synonym.
    for name, pattern, replacement in base.RULES + EXTRA:
        if name in ('which-fact', 'image-reference'): continue
        revised, count = replace_once(text, pattern, replacement)
        if count:
            text = revised
            rules.append(name)
        if len(rules) >= 5: break
    # Convert direct fact requests to an imperative without altering their object.
    pattern = r'(?P<boundary>^|[.!?]\s+)(?P<ask>what\s+(?:is|are)\s+)(?P<fact>(?:the|this|these|a|an|his|her|its)\s+[^?]+)\?'
    match = re.search(pattern, text, re.I)
    if match:
        text = text[:match.start('ask')] + base.same_case(match['ask'], 'Specify ') + match['fact'] + '.' + text[match.end():]
        rules.append('fact-request')
    # A final copular fill-in stem can be asked as a direct question.
    if 'fact-request' not in rules:
        pattern = r'(?P<boundary>^|[.!?]\s+)(?P<subject>[^.!?]+?)\s+(?P<verb>is|are)\s*(?:(?:the|a|an)\s*)?(?:_{2,}\s*)?[:?.]?\s*$'
        match = re.search(pattern, text, re.I)
        if match and not re.match(r'(what|which|where|when|how)\b', match['subject'], re.I):
            subject = match['subject']
            prefix = base.same_case(subject, 'What ' + match['verb'].lower() + ' ')
            text = text[:match.start('subject')] + prefix + subject + '?'
            rules.append('factual-statement-to-question')
    # Reorder passive factual prompts into direct questions; keep their facts verbatim.
    if not rules:
        pattern = r'(?P<boundary>^|[.!?]\s+)(?P<subject>[^.!?]+?)\s+(?P<verb>is|are)\s+(?P<action>seen|found|located|situated|used|derived|formed|secreted|supplied|innervated|caused|produced|obtained|associated)\s+(?P<prep>in|by|from|for|with|at)\s*(?:_{2,}\s*)?[:?.]?\s*$'
        match = re.search(pattern, text, re.I)
        if match and not re.match(r'(what|which|where|when|how)\b', match['subject'], re.I):
            prefix = base.same_case(match['subject'], match['prep'].capitalize() + ' which of the listed options ' + match['verb'].lower() + ' ')
            text = text[:match.start('subject')] + prefix + match['subject'] + ' ' + match['action'] + '?'
            rules.append('passive-statement-to-question')
    # Preserve all modal verbs and clinical content when restating an interrogative.
    if not rules:
        match = re.search(r'(?P<boundary>^|[.!?]\s+)(?P<ask>(?:which|what)\s+(?!(?:is|are|was|were|do|does|did|can|could|will|would|shall|should|may|might|must|has|have|had)\b)[^?]+)\?\s*$', text, re.I)
        if match:
            ask = match['ask']
            if not ask.isupper(): ask = ask[:1].lower() + ask[1:]
            text = text[:match.start('ask')] + base.same_case(match['ask'], 'Indicate ') + ask + '.'
            rules.append('indirect-question-request')

    # Remaining short interrogatives use equivalent question wording, not labels.
    if not rules:
        for name, pattern, replacement in [
            ('which-fact', r'\bwhich(?=\s+(?:nerve|muscle|artery|vein|structure|condition|disease|drug|test|type|part|area|layer|joint|bone|cell|hormone|enzyme|vitamin|organ|vessel|finding|level|diagnosis|sign|fracture|symptom|investigation|treatment|compartment|method|protein|factor|stage|region|feature|site|mechanism|receptor|syndrome|number|dose|tumor|tumour|disorder|gene|pump|channel)\b)', 'what'),
            ('what-kind', r'\bwhat\s+kind\s+of\b', 'which type of'),
            ('which-marked', r'\bwhich\s+of\s+the\s+marked\b', 'which of the indicated'),
            ('which-is', r'^which\s+is\b', 'what is'),
            ('which-are', r'^which\s+are\b', 'what are'),
            ('image-reference', r'\bthe\s+given\b', 'the provided'),
        ]:
            revised, count = replace_once(text, pattern, replacement)
            if count:
                text = revised
                rules.append(name)
                break
    # Do not manufacture a paraphrase when the remaining stem is a terse factual fragment.
    return text, rules or ['retained-for-precision']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    previous = json.loads(base.AUDIT.read_text(encoding='utf-8'))['changes']
    changes = []
    for item in previous:
        after, rules = rewrite(item['before'])
        protected = r'\b(?:not|except|false|incorrect|never|always|least|most|only|all|no|none|without|cannot|unlikely)\b'
        assert Counter(re.findall(protected, item['before'].lower())) == Counter(re.findall(protected, after.lower())), item['id']
        assert re.findall(r'\d+(?:[.,]\d+)*', item['before']) == re.findall(r'\d+(?:[.,]\d+)*', after), item['id']
        changes.append({**item, 'previousEdit': item['after'], 'after': after, 'rules': rules})
    lookup = {c['id']: c for c in changes}
    banks = [json.loads(p.read_text(encoding='utf-8-sig')) for p in base.BANKS]
    assert len(lookup) == 5025
    for bank in banks:
        before = json.loads(json.dumps(bank))
        targets = base.questions(bank)
        assert {q['id'] for q in targets} == set(lookup)
        for q in targets:
            c = lookup[q['id']]
            assert q['prompt'] in (c['previousEdit'], c['after']), q['id']
            assert base.digest({k:v for k,v in q.items() if k != 'prompt'}) == c['unchangedFieldsSha256'], q['id']
            q['prompt'] = c['after']
        restored = json.loads(json.dumps(bank))
        originals = {q['id']:q['prompt'] for q in base.questions(before)}
        for q in base.questions(restored): q['prompt'] = originals[q['id']]
        assert restored == before, 'Non-stem data changed.'
    summary = {'total': len(changes), 'reworded': sum(c['before'] != c['after'] for c in changes),
        'retained_for_precision': sum(c['before'] == c['after'] for c in changes),
        'multiple_edits': sum(len(c['rules']) > 1 for c in changes),
        'checks': 'All non-stem fields identical; original numbers and negation qualifiers preserved.'}
    AUDIT.write_text(json.dumps({'summary':summary,'changes':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.apply:
        for p,bank in zip(base.BANKS,banks): p.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'applied':args.apply,**summary},indent=2))

if __name__ == '__main__': main()
