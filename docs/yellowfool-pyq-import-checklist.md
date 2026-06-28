# Yellowfool PYQ Import Checklist

Source PDF: `F:\pyqs\Pyqs neet inict the yellowfool.pdf`

Importer: `npm run import:yellowfool -- --subject <subject-id>`

Total audited questions: 5,007

## Completed

- [x] Anesthesia - 103 questions imported with explanations
- [x] Anatomy - 276 questions imported with explanations
- [x] Physiology - 177 questions imported with explanations and images
- [x] Biochemistry - 266 questions imported with explanations and images
- [x] Pathology - 421 questions imported with explanations and 84 source images
- [x] Microbiology - 370 questions imported with explanations and 97 source images
- [x] Pharmacology - 407 questions imported with explanations and 19 source images

## Remaining Subjects

- [ ] Medicine - 488 questions
- [ ] Obstetrics & Gynecology - 448 questions
- [ ] Surgery - 408 questions
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
- Current atlas checkpoint (2026-06-28): 244 of 384 complete; Anatomy has 133 complete, Anesthesia has 14 complete, Physiology has 18 complete, Biochemistry has 19 complete, and Pathology has 60 of 84 complete.
- Anesthesia atlas-image pass complete. The saved method is in `docs/medicomm-atlas-image-standard.md`.
- Website sync verified: the latest ten atlas URLs and PNGs are present in both `public/` and `dist/`.
