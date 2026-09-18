"""Recover question images on answer-key pages and normalize image formats."""
import hashlib
import io
import json
import re
from collections import defaultdict
import fitz
from PIL import Image
from audit_remaining_yellowfool import STAGE, ROOT
from clean_remaining_yellowfool import SUBJECTS
import import_yellowfool_pyqs as m

doc = fitz.open(str(m.DEFAULT_PDF_PATH))
issues = []
for sid in SUBJECTS:
    path = STAGE / f'{sid}.json'
    questions = json.loads(path.read_text(encoding='utf-8'))
    sessions = defaultdict(list)
    for q in questions:
        sessions[(q['sourcePdfPageStart'], q['sourcePdfPageEnd'])].append(q)
    recovered = 0
    for (start, end), batch in sessions.items():
        by_number = {q['sourceQuestionNumber']: q for q in batch}
        active = None
        for number in range(start, end + 1):
            page = doc[number - 1]
            text = page.get_text()
            positions = [(rect.y0, qn) for qn in by_number for rect in page.search_for(f'Question {qn}:') if not any(rect.intersects(r) for r in page.search_for(f'Solution to Question {qn}:'))]
            positions.sort()
            keys = page.search_for('Answer Key')
            details = page.search_for('Detailed Explanations')
            if details:
                stop = min(r.y0 for r in keys + details)
                for item in page.get_images(full=True):
                    for rect in page.get_image_rects(item[0]):
                        if rect.y1 > stop:
                            continue
                        preceding = [qn for y, qn in positions if y < rect.y0]
                        owner = preceding[-1] if preceding else active
                        if owner is None:
                            continue
                        q = by_number[owner]
                        img = doc.extract_image(item[0])
                        data = img['image']
                        if any(hashlib.sha256((ROOT / 'public' / url.lstrip('/')).read_bytes()).digest() == hashlib.sha256(data).digest() for url in q['imageUrls']):
                            continue
                        url = m.write_question_image(f"yellowfool-{q['id']}-p{number}-xref{item[0]}.{img['ext']}", data)
                        q['imageUrls'].append(url)
                        q['images'] = q['sourceImageUrls'] = q['imageUrls']
                        recovered += 1
                break
            if positions:
                active = positions[-1][1]
    for q in questions:
        urls = []
        for url in q['imageUrls']:
            if url.endswith(('.jp2', '.jpx')):
                image = Image.open(ROOT / 'public' / url.lstrip('/'))
                output = io.BytesIO()
                image.save(output, format='PNG')
                url = m.write_question_image(url.rsplit('/', 1)[-1].rsplit('.', 1)[0] + '.png', output.getvalue())
            with Image.open(ROOT / 'public' / url.lstrip('/')) as image:
                image.verify()
            urls.append(url)
        q['imageUrls'] = q['images'] = urls
        if urls:
            q['sourceImageUrls'] = urls
            q['atlasImageTargetUrls'] = [m.medicomm_atlas_image_url(q, i + 1) for i in range(len(urls))]
        if not urls:
            reference = bool(re.search(r'\b(shown|image|picture|given below)\b', q['prompt'], re.I))
            compact_options = all(re.fullmatch(r'[\d\s,()&.-]+(?:ONLY)?', option.strip(), re.I) for option in q['options'])
            if reference or compact_options:
                issues.append({'id': q['id'], 'prompt': q['prompt'], 'options': q['options'], 'reason': 'visual-reference' if reference else 'numbered-options'})
    path.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'{sid}: recovered {recovered} images on explanation-boundary pages', flush=True)
(STAGE / 'source-context-review.json').write_text(json.dumps(issues, indent=2, ensure_ascii=False), encoding='utf-8')
