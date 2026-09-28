# Bhalani Final Year theory import

Source: `D:/medicomm/shortnotes/Bhalani Final Year.pdf` (104 pages).
Destination: `public/short-notes.json`, used by Theory → Short Notes and the server's answer-review lookup.

| Website subject | PDF pages | Topics | Questions |
| --- | --- | --- | --- |
| General Medicine | 4–24 | 28 | 516 |
| General Surgery | 26–42, 53–57 | 57 | 430 |
| Orthopedics | 43–52 | 39 | 125 |
| Obstetrics and Gynaecology | 58–77 | 63 | 305 |
| Pediatrics | 78–86 | 24 | 161 |
| New total | | 211 | 1,537 |

The new questions comprise 1,135 short-answer/short-note prompts and 402 long-answer prompts. All 1,793 earlier questions, their IDs, and subject data are unchanged. The combined library has 3,330 questions across 540 topics and 15 subjects.

## Source handling

- Cover and examination-distribution pages 1–3 and 25 are excluded.
- Pages 87–104 repeat the 87 Ophthalmology and 107 ENT questions already imported from the third-year PDF. All 194 prompts were compared in source order; differences are spelling/punctuation corrections already applied to the existing library. These entries are not duplicated or replaced.
- Original question text, PDF page, printed question number, paper, question type, exam-session references, and star counts are retained. Displayed prompts repair wrapped exam-session references and a few obvious spelling errors.
- Medicine's Psychiatry/Dermatology topics and Surgery's Anaesthesia/imaging topics remain within their source paper groupings.
- The smaller Tuberculosis subheading on page 19 contains short answers; the following respiratory long answers are grouped under the parent Respiratory Medicine topic.
- The source omits SAQ labels for Drugs on page 24 and Obstetrics on page 77. These lists are imported as short notes, up to their next explicit LAQ label.
- Five numbering irregularities on pages 6, 12, 38, and 56 were reviewed. They are source numbering errors, not missing questions or joined subparts; every entry is retained.
- Repeated Hand and Foot headings in Surgery I are combined into one topic. Separate paper groupings remain distinct.

## Reproduction and checks

Requires Python with PyMuPDF.

```powershell
python -X utf8 scripts/import_final_year_short_notes.py --audit-only
python -X utf8 scripts/import_final_year_short_notes.py
node scripts/check_short_notes.mjs
```

The importer compares every page's prompt count against an independent plain-text extraction, validates source numbering anomalies, preserves unrelated subjects, checks unique IDs, and can be rerun without changing the result. Source metadata records the PDF SHA-256 hash.

Extracted lines, the question audit, appendix comparisons, and the count report are stored under `output/short-notes-final-year`.

`scripts/check_short_notes_ui.cjs` checks all 15 subjects, question search, source labels, desktop/mobile layouts, drafts, uploads, and review behavior. It uses the local site at port 4173 and stubs AI responses.
