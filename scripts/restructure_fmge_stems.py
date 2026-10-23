"""Restructure FMGE questions from their originals; never edit answer options."""
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('fmge', ROOT/'scripts/reword_fmge_stems.py')
fmge = importlib.util.module_from_spec(spec); spec.loader.exec_module(fmge)
AUDIT = ROOT/'output/fmge-wording/structural-revision.json'


def lower_article(text):
    return re.sub(r'^(The|A|An|This|These)\b', lambda m:m[0].lower(), text)


def request(text):
    raw = text.strip()
    tail = re.sub(r'[\s:?._-]+$', '', raw)
    # Keep every noun, qualifier, modality and negative in the requested proposition.
    verbs = r'(?:is|are|was|were|can|cannot|could|should|would|will|may|might|must|does|do|has|have|best|most|least|inhibits|prevents|causes|produces|increases|decreases|indicates|describes|represents|explains)'
    m = re.fullmatch(r'which(?:\s+one)?\s+of\s+(?:the\s+)?following\s*(?P<noun>.*?)\s*(?P<predicate>'+verbs+r'\b.*)', tail, re.I|re.S)
    if m:
        noun=m['noun'].strip(); predicate=m['predicate'].strip()
        noun=re.sub(r'\b(drug|agent|condition|disease|statement|organism|investigation|test|factor|method|feature|defect|marker|nerve|muscle|artery|vein|technique|treatment|diagnosis|cause|level|type|protein|vitamin|enzyme|hormone)$', lambda n: {'artery':'arteries','diagnosis':'diagnoses'}.get(n[0].lower(),n[0]+'s'), noun, flags=re.I)
        predicate=re.sub(r'^(is|are|was|were|has|have|can|could|should|would|will|may|might|must|does|do|did)\s+(he|she|it|they|you|we|the patient|this patient|the child|this child)\b', lambda m:m[2]+' '+m[1], predicate, flags=re.I)
        plural=bool(re.match(r'(are|were|do|have)\b',predicate,re.I))
        selection='the options that' if plural else 'the option that'
        prefix=('From the listed '+noun+', select ') if noun else 'Select '
        return prefix+selection+' '+predicate+'.', 'option-proposition'
    m = re.fullmatch(r'what\s+(is|are)\s+(.+?)\s+(?:called|termed|named|known as)',tail,re.I|re.S)
    if m: return 'Give the '+('names' if m[1].lower()=='are' else 'name')+' of '+lower_article(m[2])+'.','naming-request'
    m = re.fullmatch(r'what\s+(is|are)\s+(.+?)\s+(used for|used to do)',tail,re.I|re.S)
    if m: return 'State what '+lower_article(m[2])+' '+m[1]+' '+m[3]+'.','purpose-request'
    m = re.fullmatch(r'what\s+(?:is|are)\s+(.+)',tail,re.I|re.S)
    if m:
        if re.search(r'\b(?:for|to|by|with|in|at|from|of|against|during|after|before|diagnose|measure|treat|prevent|detect|identify)$',m[1],re.I):
            return raw,'retained-ambiguous-question'
        return 'Determine '+lower_article(m[1])+'.','direct-request'
    m = re.fullmatch(r'which\s+(?P<noun>.+?)\s+(?P<predicate>'+verbs+r'\b.*)',tail,re.I|re.S)
    if m:
        return 'Identify the '+m['noun']+' that '+m['predicate']+'.','named-proposition'
    m = re.fullmatch(r'which\s+(is|are)\s+(.+)',tail,re.I|re.S)
    if m: return 'Select the option that '+m[1]+' '+m[2]+'.','which-is'
    m = re.fullmatch(r'identify\s+(.+)',tail,re.I|re.S)
    if m: return 'Select the option identifying '+lower_article(m[1])+'.','identification-request'
    m = re.fullmatch(r'what\s+should\s+be\s+done\s+(.+)',tail,re.I|re.S)
    if m: return 'Select the action that should be taken '+m[1]+'.','action-request'
    m = re.fullmatch(r'how\s+(?:will|would)\s+you\s+manage\s+(.+)',tail,re.I|re.S)
    if m: return 'Choose how to manage '+m[1]+'.','management-request'
    m = re.fullmatch(r'calculate\s+(.+)',tail,re.I|re.S)
    if m: return 'Work out '+lower_article(m[1])+'.','calculation-request'
    # Convert a blank at the end of a copular stem to an explicit fact request.
    m = re.fullmatch(r'(?P<subject>[^?]+?)\s+(?:is|are)\s*(?:(?:the|a|an)\s*)?',tail,re.I|re.S)
    if m and not re.match(r'(which|what|where|when|how)\b',m['subject'],re.I):
        return 'Determine '+lower_article(m['subject'])+'.','factual-request'
    return raw, None


def rewrite(original):
    rules=[]
    # Separate the final request from the vignette, retaining the vignette's chronology.
    candidates=list(re.finditer(r'(?:^|[.!?]\s+)(?P<ask>(?:which|what|identify|calculate|how|where|when)\b)',original,re.I))
    if candidates:
        match=candidates[-1]; start=match.start('ask')
        case=original[:start].strip(); query=original[start:].strip()
        transformed,rule=request(query)
        # Do not move trailing laboratory tables, answer lists, or multiple questions.
        if case and len(case)>45 and query.count('?')<=1 and len(query)<450 and not re.search(r'\n\s*(?:\d+[.)]|[A-D][.)]|pH\b|Na\b|HCO3\b)',query,re.I):
            text=transformed+'\n\n'+case
            rules=['question-before-vignette']+([rule] if rule else [])
        else:
            text=original[:start]+transformed
            if rule:rules.append(rule)
    else:
        text,rule=request(original)
        if rule:rules.append(rule)
    # A demographic rephrasing keeps the exact age, unit and patient description.
    age=r'\b(?P<article>a|an)\s+(?P<age>\d+)\s*[- ]\s*(?P<unit>year|month|week|day)[- ]old\s+(?P<person>man|woman|male(?:\s+patient)?|female(?:\s+patient)?|boy|girl|child|infant|patient)\b'
    def age_replacement(m):
        article='A' if m['article'][0].isupper() else 'a'
        return article+' '+m['person']+' aged '+m['age']+' '+m['unit']+('' if m['age']=='1' else 's')
    text,count=re.subn(age,age_replacement,text,flags=re.I)
    if count:rules.append('age-description')
    # Use the prior conservative rewrite only where no structural rewrite applies.
    if not rules:
        text,previous_rules=fmge.wording.rewrite(original)
        rules=previous_rules
    if original.isupper(): text=text.upper()
    return text,rules


def main():
    previous=json.loads(fmge.AUDIT.read_text(encoding='utf-8'))['changes']
    changes=[]
    for c in previous:
        after,rules=rewrite(c['before'])
        # Reordering a request may reorder numbers; each numeric value must remain.
        numbers=r'\d+(?:[.,]\d+)*'
        assert Counter(re.findall(numbers,c['before']))==Counter(re.findall(numbers,after)),c['id']
        protected=r'\b(?:not|except|false|incorrect|never|always|least|most|only|all|no|none|without|cannot|unlikely)\b'
        assert Counter(re.findall(protected,c['before'].lower()))==Counter(re.findall(protected,after.lower())),c['id']
        changes.append({**c,'previousEdit':c['after'],'after':after,'rules':rules})
    lookup={c['id']:c for c in changes};assert len(lookup)==2895
    paths=[ROOT/folder/'fmge-question-bank.json' for folder in ('data','public','dist')]
    paths=[p for p in paths if p.exists()]
    banks=[json.loads(p.read_text(encoding='utf-8-sig')) for p in paths]
    for bank in banks:
        original=json.loads(json.dumps(bank));old_prompts={q['id']:q['prompt'] for q in fmge.questions(original)}
        for q in fmge.questions(bank):
            c=lookup[q['id']]
            assert q['prompt'] in (c['previousEdit'],c['after']),q['id']
            assert fmge.wording.base.digest({k:v for k,v in q.items() if k!='prompt'})==c['unchangedFieldsSha256'],q['id']
            q['prompt']=c['after']
        restored=json.loads(json.dumps(bank))
        for q in fmge.questions(restored):q['prompt']=old_prompts[q['id']]
        assert restored==original,'A non-stem field changed.'
    summary={'total':len(changes),'structurally_rewritten':sum(any(r in c['rules'] for r in ['question-before-vignette','option-proposition','direct-request','named-proposition','which-is','identification-request','action-request','management-request','calculation-request','factual-request','age-description','naming-request','purpose-request']) for c in changes),'unchanged':sum(c['before']==c['after'] for c in changes)}
    AUDIT.write_text(json.dumps({'summary':summary,'changes':changes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    import sys
    if '--apply' in sys.argv:
        for p,b in zip(paths,banks):p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
