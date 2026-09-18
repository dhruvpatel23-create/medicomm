"""Verify persisted banks and the running API after the remaining-subject import."""
import gzip
import json
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from audit_remaining_yellowfool import ROOT, STAGE, prompt, normalized
from clean_remaining_yellowfool import SUBJECTS

bank = json.loads((ROOT / 'data/practice-question-bank.json').read_text(encoding='utf-8'))
response = urllib.request.urlopen('http://127.0.0.1:4174/api/practice', timeout=30)
raw = response.read()
live = json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)
rows = []
urls = set()
coverage = []
for subject in bank['subjects']:
    if subject['id'] not in SUBJECTS:
        continue
    official = [q for q in subject['questions'] if q.get('source') not in {'ai', 'usmle'}]
    actual = next(s for s in live['subjects'] if s['id'] == subject['id'])['questions']
    assert {q['id'] for q in actual} == {q['id'] for q in official}, subject['id']
    by_id = {q['id']: q for q in actual}
    fingerprints = defaultdict(list)
    for q in official:
        fingerprints[(q['examId'], prompt(q), tuple(sorted(map(normalized, q['options']))))].append(q['id'])
        if not q.get('sourceQuestionId'):
            continue
        coverage.extend(q['sourceQuestionIds'])
        assert q['answer'] == q['options'][q['answerIndex']]
        assert len(q['options']) == 4 and all(q['options']) and q['explanation']
        assert by_id[q['id']]['options'] == q['options']
        assert by_id[q['id']]['answer'] == q['answer']
        assert by_id[q['id']]['imageUrls'] == q['imageUrls']
        assert 'Answer Key' not in ' '.join(q['options'])
        assert 'Chapter\nTitle\nPage' not in q['explanation']
        urls.update(q['imageUrls'])
    duplicates = [v for v in fingerprints.values() if len(v) > 1]
    assert not duplicates, duplicates
    rows.append({'subject': subject['id'], 'livePyqs': len(actual)})
expected = [q['id'] for sid in SUBJECTS for q in json.loads((STAGE / f'{sid}.json').read_text(encoding='utf-8'))]
assert Counter(coverage) == Counter(expected)
assert len(coverage) == 2104


def check_image(url):
    with urllib.request.urlopen('http://127.0.0.1:4174' + url, timeout=30) as result:
        assert result.status == 200 and result.headers['Content-Type'].startswith('image/'), url
        assert len(result.read()) > 0, url
    for folder in ['data', 'public', 'runtime-data', 'dist']:
        assert (ROOT / folder / url.lstrip('/')).is_file(), (folder, url)


with ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(check_image, sorted(urls)))
result = {'sourceEntriesVerified': len(coverage), 'uniqueQuestionsVerified': len(set(coverage)) - 1,
          'imageUrlsVerified': len(urls), 'subjects': rows, 'sameExamExactDuplicates': 0}
(STAGE / 'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
