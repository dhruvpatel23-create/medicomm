import json
import re
import fitz
from audit_remaining_yellowfool import STAGE
from clean_remaining_yellowfool import SUBJECTS
import import_yellowfool_pyqs as m

doc = fitz.open(str(m.DEFAULT_PDF_PATH))
rows = []
for subject in SUBJECTS:
    for q in json.loads((STAGE / f'{subject}.json').read_text(encoding='utf-8')):
        if q['imageUrls'] or not re.search(r'\b(shown|image|picture|given below)\b', q['prompt'], re.I):
            continue
        for number in range(q['sourcePdfPageStart'], q['sourcePdfPageEnd'] + 1):
            page = doc[number - 1]
            rects = page.search_for(f"Question {q['sourceQuestionNumber']}:")
            if not rects or 'Solution to Question' in page.get_text():
                continue
            start = rects[0].y0
            following = page.search_for(f"Question {q['sourceQuestionNumber']+1}:")
            stop = next((r.y0 for r in following if r.y0 > start), page.rect.height - 30)
            clip = fitz.Rect(0, max(0, start-3), page.rect.width, stop)
            target = STAGE / f"visual-review-{q['id']}.png"
            page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), clip=clip).save(str(target))
            row = {'id': q['id'], 'page': number, 'file': str(target), 'embeddedImages': len(page.get_images())}
            rows.append(row)
            print(json.dumps(row))
            break
(STAGE / 'visual-review.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
