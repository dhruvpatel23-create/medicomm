"""Install only explicitly visually verified General Surgery replacements."""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'output/imagegen/general-surgery-img1'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, data):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)

def questions(node):
    if isinstance(node, dict):
        if node.get('subjectId') == 'general-surgery' and node.get('prompt'):
            yield node
        else:
            for value in node.values():
                yield from questions(value)
    elif isinstance(node, list):
        for value in node:
            yield from questions(value)

def main():
    review = read(FOLDER / 'review-manifest.json')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    replacements = {}
    records = []
    for asset in review['assets']:
        if asset['status'] != 'visually_verified':
            continue
        source = ROOT / asset['generatedFile']
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        assert digest == asset['sha256'], source
        for qid in asset['questionIds']:
            url = '/uploads/medicomm-img1-' + qid + '-' + digest[:10] + '.png'
            replacements[qid] = url
            records.append(dict(questionId=qid, sourceFile=asset['sourceUrl'], generatedFile=asset['generatedFile'], targetUrl=url, sha256=digest))
    banks = [ROOT / d / 'practice-question-bank.json' for d in ['data','public','dist']]
    loaded = [(p, read(p)) for p in banks]
    for p, bank in loaded:
        found = {q['id'] for q in questions(bank)}
        assert set(replacements) <= found, (p, set(replacements)-found)
    backup = FOLDER / ('backup-' + stamp)
    backup.mkdir()
    for p, _ in loaded:
        shutil.copy2(p, backup / (p.parent.name + '-practice-question-bank.json'))
    for rec in records:
        for directory in ['public','data','dist','runtime-data']:
            target = ROOT / directory / rec['targetUrl'].lstrip('/')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rec['generatedFile'], target)
            assert hashlib.sha256(target.read_bytes()).hexdigest() == rec['sha256']
    for p, bank in loaded:
        for q in questions(bank):
            if q['id'] in replacements:
                for field in ['imageUrls','images','atlasImageTargetUrls']:
                    q[field] = [replacements[q['id']]]
                q['imageReviewStatus'] = 'img1-visually-verified'
                q['assetNote'] = 'Original educational illustration; source and generated image visually compared for required features, orientation, and markers. General Surgery img1 batch.'
            elif q['id'] in ['aiims-2018-general-surgery-q012','neet-pg-2021-q144']:
                for field in ['imageUrls','images','atlasImageTargetUrls','explanationImageUrls']:
                    q[field] = []
                for field in ['imageUrl','image']:
                    q.pop(field, None)
                q['assetNote'] = ('Source PDF page 4679 verified: this question is text-only. The imported Kasai diagram belongs to question 13; source provenance retained.' if q['id']=='aiims-2018-general-surgery-q012' else 'Source PDF page 4911 verified: this trauma question is text-only. The imported Thiersch procedure image belongs to question 7; source provenance retained.')
        write(p, bank)
    write(FOLDER / 'installed-manifest.json', dict(installedAt=stamp, status='partial', totalSourceQuestions=review['questionCount'], installedCount=len(records), assets=records))
    print(f'Installed and hash-verified {len(records)} replacements in four asset directories and three banks.')

if __name__ == '__main__':
    main()
