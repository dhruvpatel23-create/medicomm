# Bhalani III year theory import

Source: `D:/medicomm/shortnotes/Bhalani  III year.pdf` (41 scanned pages).
Destination: `public/short-notes.json`, used by Theory → Short Notes and the server's answer-review question lookup.

| Website subject | PDF pages | Topics | Questions |
| --- | --- | --- | --- |
| Community Medicine (PSM I and II) | 1–23 | 67 | 402 |
| Ophthalmology | 24–29 | 19 | 87 |
| ENT | 30–41 | 47 | 107 |
| Total | 1–41 | 133 | 596 |

The import includes 443 short-note/short-answer questions and 153 long-answer questions. The existing 1,197 questions remain unchanged. Forensic Medicine continues to use the second-year PDF already imported.

## Extraction and review

Windows OCR extracted word coordinates from rendered pages. The importer reconstructs reading order and retains source pages, source numbering, paper, question type, emphasis, and source row references. All 41 page images were visually reviewed. `REVIEWED_LINES` records transcriptions that repair missing OCR words or punctuation; `PROMPT_CORRECTIONS` fixes obvious spelling errors only in displayed prompts. The original OCR files remain available for comparison.

All 598 numbered source entries are accounted for. Two are continuations of existing questions:

- Page 21, Communication for Health Education: LAQ entries 1 and 2 form one sentence.
- Page 22, Health Care of the Community: repeated entry 1 contains subparts (a) and (b) of one question.

The bank contains 596 complete prompts after these joins. The importer validates numbering sequences, topic and question ID uniqueness, and nonempty prompts, and refuses to overwrite unrelated subject data. Re-running it produces identical output.

## Reproduction

Requires Python with PyMuPDF and Windows OCR with an English language installed.

```powershell
python scripts/import_third_year_short_notes.py --prepare-ocr
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/ocr_short_notes.ps1 -ImageDirectory D:\medicomm\dhruv1\output\short-notes-third-year
python scripts/import_third_year_short_notes.py --audit-only
python scripts/import_third_year_short_notes.py
node scripts/check_short_notes.mjs
```

OCR caches, page images, extracted lines, question audit, and the count report are in `output/short-notes-third-year`. The OCR script skips existing cache files; use the same source PDF when reusing them. Source metadata includes the PDF SHA-256 hash.

`scripts/check_short_notes_ui.cjs` checks all ten subjects, including searches for repaired third-year prompts, correct source labels, and mobile layout. It uses the local site at port 4173 and stubs AI responses.
