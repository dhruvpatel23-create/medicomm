"""Attach all source images between question headings, including tables."""
import json
import re
import sys
from collections import defaultdict
import import_yellowfool_pyqs as m
from audit_remaining_yellowfool import STAGE


def main():
    subject = sys.argv[1]
    path = STAGE / f'{subject}.json'
    questions = json.loads(path.read_text(encoding='utf-8'))
    reader = m.PdfReader(str(m.DEFAULT_PDF_PATH))
    texts = [''] * len(reader.pages)
    sessions = defaultdict(list)
    for q in questions:
        sessions[(q['sourcePdfPageStart'], q['sourcePdfPageEnd'])].append(q)
    added = 0
    for (start, end), batch in sessions.items():
        for page in range(start, end + 1):
            texts[page - 1] = m.clean_page_text(reader.pages[page - 1].extract_text() or '')
            if m.SOLUTION_HEADING.search(texts[page - 1]) or re.search(r'(?m)^Detailed Explanations\s*$', texts[page - 1]):
                break
        positions, images = m.chapter_layout(reader, {'startPage': start, 'endPage': end}, texts)
        for index, q in enumerate(batch):
            current = positions.get(q['sourceQuestionNumber'])
            following = positions.get(batch[index+1]['sourceQuestionNumber']) if index+1 < len(batch) else None
            if not current:
                continue
            # PDF content-stream order remains stable even for transformed images.
            candidates = [img for img in images if m.image_is_after_question_by_order(img, current, following)]
            urls = []
            for img in candidates:
                name = f"yellowfool-{q['examId']}-{subject}-q{q['questionNumber']:03d}-p{img['pageNumber']}-i{img['index']}{img['extension']}"
                urls.append(m.write_question_image(name, img['bytes']))
            if urls:
                added += len(set(urls) - set(q['imageUrls']))
                q['imageUrls'] = q['images'] = q['sourceImageUrls'] = urls
                q['atlasImageTargetUrls'] = [m.medicomm_atlas_image_url(q, i + 1) for i in range(len(urls))]
    path.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding='utf-8')
    missing = [q['id'] for q in questions if not q['imageUrls'] and re.search(r'\b(shown|image|picture|given below)\b', q['prompt'], re.I)]
    print(f'{subject}: {added} additional images; image-reference questions without images: {missing}', flush=True)


if __name__ == '__main__':
    main()
