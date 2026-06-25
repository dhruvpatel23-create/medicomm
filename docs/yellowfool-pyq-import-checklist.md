# Yellowfool PYQ Import Checklist

Source PDF: `F:\pyqs\Pyqs neet inict the yellowfool.pdf`

Importer: `npm run import:yellowfool -- --subject <subject-id>`

Total audited questions: 5,007

## Completed

- [x] Anesthesia - 103 questions imported with explanations
- [x] Anatomy - 276 questions imported with explanations
- [x] Physiology - 177 questions imported with explanations and images
- [x] Biochemistry - 266 questions imported with explanations and images

## Remaining Subjects

- [ ] Medicine - 488 questions
- [ ] Obstetrics & Gynecology - 448 questions
- [ ] Pathology - 421 questions
- [ ] Surgery - 408 questions
- [ ] Pharmacology - 407 questions
- [ ] Microbiology - 370 questions
- [ ] Community Medicine - 344 questions
- [ ] Psychiatry - 235 questions
- [ ] Pediatrics - 211 questions
- [ ] Forensic Medicine - 210 questions
- [ ] Ophthalmology - 190 questions
- [ ] Orthopedics - 175 questions
- [ ] ENT - 139 questions
- [ ] Dermatology - 139 questions

## Notes

- Import subject-wise, not all at once.
- Validate every batch for total count, answer keys, and non-empty explanations.
- The importer preserves source exam, year, chapter title, PDF page range, tags, and explanation text.
- The atlas-image follow-up pass is tracked separately in `docs/medicomm-atlas-image-migration.csv`.
- Current atlas checkpoint (2026-06-25): 147 of 274 complete; Anatomy has 133 complete and Anesthesia has 14 complete.
- Anesthesia atlas-image pass complete. The saved method is in `docs/medicomm-atlas-image-standard.md`.
- Website sync verified: the latest ten atlas URLs and PNGs are present in both `public/` and `dist/`.
