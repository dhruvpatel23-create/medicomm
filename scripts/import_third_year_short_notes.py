"""Import reviewed OCR from the scanned Bhalani III year PDF."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from import_short_notes import clean, slug

ROOT = Path(__file__).resolve().parents[1]
OCR_DIR = ROOT / 'output' / 'short-notes-third-year'
SOURCE_ID = 'bhalani-iii-year'

# Page:row references point to the untouched OCR audit. These transcriptions were
# checked against every scanned page, including words swallowed beside asterisks.
REVIEWED_LINES = {
    '01:24': '2. International [Death Certificate]* (Pg. 64)',
    '01:29': '7. Case Control Study* - confounding factors',
    '02:24': '1. Randomized Controlled Trials**** - steps*, types; planning, conduct with a suitable',
    '04:04': '3. Immunization against H1N1* (Pg. 171)',
    '04:16': '2. MDR - TB**',
    '08:11': '1. Syndromic Approach for Urethral Discharge of of Male Patient',
    '12:03': '6. Indicators/Indices of Thermal Comfort*',
    '12:28': '2. Air Pollution**** - sources**, indicators, causative factors*, measures for control***;',
    '13:09': '8. Eugenics** (Pg. 888)',
    '13:14': '3. Measures of Central Tendency****',
    '16:08': '6. Integrated Management of Neonatal and Childhood Illness (IMNCI)** (Pg. 497)',
    '16:15': 'describe*; Preventable Blindness in India - important causes',
    '17:21': '3. Integrated Child Development Scheme**** - services provided**; beneficiaries',
    '17:22': '4. Gender Bias** and Girl Child* (Pg. 640)',
    '18:31': '13. Milk Borne Diseases',
    '19:05': '2. Milk Borne Diseases - epidemiology, prevention, control measures',
    '19:06': '3. Iodine Deficiency - various associated disorders, National Iodine Deficiency Disorders -',
    '20:04': '3. Sickness Absenteeism******',
    '20:14': 'Role of Factory Medical Officer in Prevention of Occupational Diseases',
    '20:15': '2. Pneumoconiosis** - define**, Asbestosis - epidemiology, preventive measures;',
    '20:33': '5. Mental Ill Health - causes*',
    '21:18': '3. Health Education*** - define***, approaches***, models; principles**; aims, objectives',
    '21:27': '7. PERT** (Pg. 935)',
    '21:28': '8. Work Sampling*',
    '22:03': 'Analysis in detail',
    '22:11': '6. Primary Health Care - elements (Pg. 951)',
    '22:21': '2. Primary Health Care****** - define*****, principles****, elements**; functions*;',
    '22:23': '3. ASHA - describe role in Public Health Delivery',
    '22:28': '1. UNICEF*** - activities in India*',
    '24:07': '5. Myopia***** - management; treatment options (Pg. 41)',
    '24:12': '2. Spring Catarrh/Vernal Catarrh*',
    '25:01': '1. Bacterial Corneal Ulcer***** - stages*, clinical features*****, management*****;',
    '25:12': '1. Pterygium*** (Pg. 87)',
    '25:21': '1. Acute Iridocyclitis/Anterior Uveitis** - etiopathogenesis*, clinical features**,',
    '26:21': '1. Primary Open Angle Glaucoma**** - stages, clinical features****, treatment****;',
    '26:24': 'Glaucoma***** - diagnosis, management*****, clinical features*****;',
    '26:30': '1. Diabetic Retinopathy********* - classification',
    '27:03': 'Neuro-Opthalmology',
    '27:17': '2. Hordeolum Externum/External Hordoleum* (Pg. 367)',
    '27:22': '1. Chronic Dacryocystitis**',
    '28:15': '4. Atropine** (Pg. 572)',
    '28:16': '5. Anti-Fungal Drugs (Pg. 448)',
    '29:03': '2. Redness of Eyes* - causes*, how to differentiate; Acute Red Eye*** - causes*;',
    '30:18': '1. Noise Induced Hearing Loss (NIHL)',
    '31:04': '1. Bithermal (Caloric Test)**',
    '32:05': '2. Safe Type of Chronic Suppurative Otitis Media** (Mucosal Disease) - clinical features**,',
    '32:06': 'management**; etiopathogenesis',
    '35:03': '1. Epistaxis**** - define**, causes***, clinical features, management***; differential',
    '36:14': '1. Quinsy/Peritonsillar Abscess****',
    '37:12': '1. Stidor** - define, causes**, management*; laryngeal causes, clinical picture, signs,',
    '38:12': '1. Tracheostomy**** - enumerate complications***, post-tracheostomy care;',
    '39:12': '1. Foreign Body in Oesophagus** (Pg. 395)',
}
# Consecutive headings which are line wraps, rather than parent/child headings.
HEADING_WRAPS = {'17:17', '23:10', '23:14', '30:08', '38:10', '39:15'}
ENT_SECTIONS = {'Ear', 'Nose and Paranasal Sinuses', 'Oral Cavity and Salivary Glands',
                'Pharynx', 'Larynx and Trachea', 'Oesophagus', 'Recent Advances',
                'Clinical Methods in ENT', 'Operative Surgery'}
PROMPT_CORRECTIONS = {
    'Concepts of Heath': 'Concepts of Health', 'Neuro-Opthalmology': 'Neuro-Ophthalmology',
    'Obsesity': 'Obesity', 'ofa Person': 'of a Person', 'Intrautrine': 'Intrauterine',
    'Fluorisis': 'Fluorosis', 'Rockfeller': 'Rockefeller', 'Phacoemusification': 'Phacoemulsification',
    'Buphthalmous': 'Buphthalmos', 'Hordoleum': 'Hordeolum', 'Rienke': 'Reinke',
    'Stidor': 'Stridor', 'Plummer Winson': 'Plummer Vinson', 'Sinuse Surgery': 'Sinus Surgery',
    'Sistrunks': "Sistrunk's", 'of of Male': 'of Male',
}


def display_text(text):
    text = clean(text)
    for original, corrected in PROMPT_CORRECTIONS.items():
        text = text.replace(original, corrected)
    return text


def rows(page):
    lines = json.loads((OCR_DIR / f'page-{page:02d}.ocr.json').read_text(encoding='utf-8-sig'))
    words = [w for line in lines for w in line['words']]
    scale = 4 / 3 if page == 1 else 1
    for w in words:
        for key in ('x', 'y', 'width', 'height'):
            w[key] *= scale
    groups = []
    for word in sorted(words, key=lambda w: w['y'] + w['height'] / 2):
        cy = word['y'] + word['height'] / 2
        if not groups or abs(cy - groups[-1][0]) > 11:
            groups.append((cy, [word]))
        else:
            groups[-1][1].append(word)
    result = []
    for _, group in groups:
        group.sort(key=lambda w: w['x'])
        text = ' '.join(w['text'] for w in group)
        if 'CamScanner' in text:
            continue
        result.append({'text': text, 'height': round(max(w['height'] for w in group)),
                       'x': round(min(w['x'] for w in group))})
    return result


def extract():
    subjects = []
    subject = topic = pending = None
    paper = section = ''
    kind = None
    last_number = 0
    numbered_rows = 0
    consumed_rows = 0

    def flush():
        nonlocal pending
        if pending is None:
            return
        raw = ' '.join(pending.pop('lines'))
        raw = re.sub(r'\*(?:\s+\*)+', lambda m: m[0].replace(' ', ''), raw)
        prompt = display_text(raw)
        # The source repeats "3." within this one question.
        prompt = re.sub(r'^3\. (?=Unsafe Type)', '', prompt)
        assert len(prompt) > 3 and not prompt.startswith(('(Pg.', '-')), pending
        pending.update(sourceText=raw, prompt=prompt,
                       emphasis=max([len(s) for s in re.findall(r'\*+', raw)] or [0]))
        pending['id'] = f"{SOURCE_ID}-{subject['id']}-{topic['id']}-{len(topic['questions']) + 1:03d}"
        topic['questions'].append(pending)
        pending = None

    for page in range(1, 42):
        for index, row in enumerate(rows(page)):
            key = f'{page:02d}:{index:02d}'
            text = REVIEWED_LINES.get(key, row['text'])
            if not any(c.isalnum() for c in text):
                continue
            if key in ('01:00', '16:00', '24:00', '30:00'):
                flush()
                if page in (1, 24, 30):
                    sid, title = {1: ('community-medicine', 'Community Medicine'),
                                  24: ('ophthalmology', 'Ophthalmology'), 30: ('ent', 'ENT')}[page]
                    subject = {'id': sid, 'title': title, 'sourceId': SOURCE_ID, 'topics': []}
                    subjects.append(subject)
                paper = {1: 'PSM - I', 16: 'PSM - II', 24: 'Ophthalmology', 30: 'ENT'}[page]
                section = ''
                topic = None
                kind = None
                continue
            if text == 'SAQ' or text.startswith('LAQ'):
                flush()
                kind = 'short-note' if text == 'SAQ' else 'long-answer'
                last_number = 0
                continue
            match = re.match(r'^(\d+|I|II)\.\s*(.*)', text)
            if match:
                numbered_rows += 1
                number = int({'I': '1', 'II': '11'}.get(match[1], match[1]))
                # Two numbering errors in the source split a single prompt.
                if key in ('21:17', '22:20'):
                    assert pending is not None
                    pending['lines'].append(match[2])
                    pending['sourceRows'].append(key)
                    consumed_rows += 1
                    if key == '21:17':
                        last_number = number
                    continue
                flush()
                assert topic is not None and kind is not None, (key, text)
                assert number == last_number + 1, (key, number, last_number, text)
                last_number = number
                pending = {'sourceNumber': str(number), 'kind': kind, 'sourcePage': page,
                           'sourceId': SOURCE_ID, 'sourceRows': [key], 'lines': [match[2]]}
                consumed_rows += 1
            elif row['x'] < 160:
                flush()
                if key in HEADING_WRAPS:
                    topic['title'] += ' ' + display_text(text)
                    topic['id'] = slug(paper + ' ' + section + ' ' + topic['title'])
                    continue
                if subject['id'] == 'ent' and text in ENT_SECTIONS:
                    section = text
                elif subject['id'] != 'ent' and row['height'] >= 28:
                    section = ''
                # Parent headings are removed only if they contain no questions.
                topic = {'id': slug(paper + ' ' + section + ' ' + text), 'title': display_text(text),
                         'section': section, 'sourcePaper': paper, 'questions': []}
                subject['topics'].append(topic)
                kind = None
                last_number = 0
            else:
                assert pending is not None, (key, text)
                pending['lines'].append(text)
                pending['sourceRows'].append(key)
    flush()
    assert consumed_rows == numbered_rows
    for subject in subjects:
        subject['topics'] = [t for t in subject['topics'] if t['questions']]
        assert len({t['id'] for t in subject['topics']}) == len(subject['topics']), subject['id']
    return subjects, numbered_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit-only', action='store_true')
    parser.add_argument('--prepare-ocr', action='store_true', help='Render input pages before running ocr_short_notes.ps1')
    args = parser.parse_args()
    pdf = ROOT.parent / 'shortnotes' / 'Bhalani  III year.pdf'
    if args.prepare_ocr:
        import fitz
        OCR_DIR.mkdir(parents=True, exist_ok=True)
        with fitz.open(pdf) as document:
            assert len(document) == 41
            for index, page in enumerate(document, 1):
                scale = 1.5 if index == 1 else 2
                page.get_pixmap(matrix=fitz.Matrix(scale, scale)).save(OCR_DIR / f'page-{index:02d}.png')
        print('Rendered 41 pages. Run ocr_short_notes.ps1, then this importer.')
        return
    audit = '\n'.join(f"{page:02d}:{i:02d} h{row['height']:02d} x{row['x']:03d} {row['text']}"
                      for page in range(1, 42) for i, row in enumerate(rows(page)))
    (OCR_DIR / 'extracted-lines.txt').write_text(audit, encoding='utf-8')
    subjects, numbered_rows = extract()
    questions = [q for s in subjects for t in s['topics'] for q in t['questions']]
    assert len(questions) == numbered_rows - 2
    report = {'numberedSourceEntries': numbered_rows, 'mergedContinuationEntries': 2,
              'questionCount': len(questions), 'subjects': {
                  s['id']: {'topics': len(s['topics']), 'questions': sum(len(t['questions']) for t in s['topics'])}
                  for s in subjects}}
    (OCR_DIR / 'question-audit.txt').write_text('\n'.join(
        f"{s['title']} / {t['sourcePaper']} / {t['title']} / {q['kind']} / p{q['sourcePage']}: {q['prompt']}"
        for s in subjects for t in s['topics'] for q in t['questions']), encoding='utf-8')
    (OCR_DIR / 'import-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    if not args.audit_only:
        source = {'id': SOURCE_ID, 'title': 'Bhalani III year', 'fileName': pdf.name,
                  'pageCount': 41, 'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
                  'extraction': 'Windows OCR with page-by-page visual review'}
        destination = ROOT / 'public' / 'short-notes.json'
        bank = json.loads(destination.read_text(encoding='utf-8-sig'))
        incoming = {s['id'] for s in subjects}
        assert not any(s['id'] in incoming and s.get('sourceId') != SOURCE_ID for s in bank['subjects'])
        bank['subjects'] = [s for s in bank['subjects'] if s.get('sourceId') != SOURCE_ID] + subjects
        bank['sources'] = [s for s in bank.get('sources', []) if s['id'] != SOURCE_ID] + [source]
        all_questions = [q for s in bank['subjects'] for t in s['topics'] for q in t['questions']]
        assert len({q['id'] for q in all_questions}) == len(all_questions)
        assert all(q['prompt'] and '\ufffd' not in q['prompt'] for q in all_questions)
        bank['questionCount'] = len(all_questions)
        destination.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
