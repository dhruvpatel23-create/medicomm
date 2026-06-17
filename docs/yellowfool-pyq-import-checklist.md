# Yellowfool PYQ Import Checklist

Source PDF: `F:\pyqs\Pyqs neet inict the yellowfool.pdf`

Importer: `npm run import:yellowfool -- --subject <subject-id>`

Total audited questions: 5,103

## Completed

- [x] Anesthesia - 103 questions imported with explanations

## Remaining Subjects

- [ ] Medicine - 488 questions
- [ ] Obstetrics & Gynecology - 448 questions
- [ ] Pathology - 421 questions
- [ ] Surgery - 408 questions
- [ ] Pharmacology - 407 questions
- [ ] Anatomy - 372 questions
- [ ] Microbiology - 370 questions
- [ ] Community Medicine - 344 questions
- [ ] Biochemistry - 266 questions
- [ ] Psychiatry - 235 questions
- [ ] Pediatrics - 211 questions
- [ ] Forensic Medicine - 210 questions
- [ ] Ophthalmology - 190 questions
- [ ] Physiology - 177 questions
- [ ] Orthopedics - 175 questions
- [ ] ENT - 139 questions
- [ ] Dermatology - 139 questions

## Notes

- Import subject-wise, not all at once.
- Validate every batch for total count, answer keys, and non-empty explanations.
- The importer preserves source exam, year, chapter title, PDF page range, tags, and explanation text.
- Some image-based questions currently retain text references to images; image extraction should be handled as a follow-up pass.
