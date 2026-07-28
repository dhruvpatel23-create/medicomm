# Yellowfool PYQ Import Checklist

Source PDF: `F:\pyqs\Pyqs neet inict the yellowfool.pdf`

Importer: `npm run import:yellowfool -- --subject <#ec1386subject-id>`

Total audited questions: 5,007 (2,903 imported)

## Completed

- [x] Anesthesia - 103 questions imported with explanations
- [x] Anatomy - 276 questions imported with explanations
- [x] Physiology - 177 questions imported with explanations and images
- [x] Biochemistry - 266 questions imported with explanations and images
- [x] Pathology - 421 questions imported with explanations and 84 source images
- [x] Microbiology - 370 questions imported with explanations and 97 source images
- [x] Pharmacology - 407 questions imported with explanations and 19 source images
- [x] Community Medicine - 344 questions imported with explanations and 22 source images
- [x] Forensic Medicine - 210 questions imported with explanations and 29 source images
- [x] Ophthalmology - 190 questions imported with explanations and 55 source images
- [x] ENT - 139 questions imported with explanations and 44 source images

## Remaining Subjects

- [ ] Medicine - 488 questions
- [ ] Obstetrics & Gynecology - 448 questions
- [ ] Surgery - 408 questions
- [ ] Psychiatry - 235 questions
- [ ] Pediatrics - 211 questions
- [ ] Orthopedics - 175 questions
- [ ] Dermatology - 139 questions

## Missing Visual Recovery and Atlas Conversion

- [ ] Recover and import the 27 high-confidence missing question visuals from the selected subjects only, then convert all recovered visuals to the Medicomm atlas style.
  - [x] Batch 1 - 10 missing visuals recovered, converted, linked, and verified.
  - [x] Batch 2 - 10 missing visuals generated, linked, and synchronized.
  - [x] Batch 3 - 7 missing visuals generated, linked, and synchronized.
  - [x] Pathology - 11 missing visuals.
  - [x] Microbiology - 7 missing visuals.
  - [x] Biochemistry - 3 missing visuals.
  - [ ] Physiology - 2 missing visuals.
  - [x] Pharmacology - 2 missing visuals.
  - [ ] Anatomy - 2 missing visuals.
  - [ ] Verify each candidate against its source question and PDF page before extraction.
  - [ ] Preserve anatomy, orientation, labels, arrows, markers, and diagnostic details during conversion.
  - [ ] Convert the restored source image for `ini-cet-2022-anatomy-q004` to Medicomm atlas style.
  - [ ] Update `imageUrls`, `images`, `sourceImageUrls`, asset notes, and the atlas migration tracker.
  - [ ] Synchronize final assets across `public/uploads`, `dist/uploads`, and runtime data.
  - [ ] Verify every image on the website and confirm that no image-dependent question remains blank.

## Notes

- Import subject-wise, not all at once.
- Validate every batch for total count, answer keys, and non-empty explanations.
- The importer preserves source exam, year, chapter title, PDF page range, tags, and explanation text.
- The atlas-image follow-up pass is tracked separately in `docs/medicomm-atlas-image-migration.csv`.
- Current atlas checkpoint (2026-07-06): 392 of 504 tracker rows complete; Anatomy has all 133 complete, Anesthesia has all 14 complete, Physiology has 18 of 20 complete, Biochemistry has 21 of 24 complete, Pathology has all 90 complete, Microbiology has all 104 complete, and Pharmacology has 12 of 21 complete (9 remaining).
- Microbiology atlas conversion batches:
  - [x] Batch 1 - 10 images converted, linked, synchronized, and verified (37 of 104 complete).
  - [x] Batch 2 - 10 images converted, linked, synchronized, and verified (47 of 104 complete).
  - [x] Batch 3 - 10 images converted, linked, synchronized, and verified (57 of 104 complete).
  - [x] Batch 4 - 10 images converted, linked, synchronized, and verified (67 of 104 complete).
  - [x] Batch 5 - 10 images converted, linked, synchronized, and verified with a slightly darker Medicomm watermark (77 of 104 complete); the blocked NEET PG 2021 q004 clinical source was left pending and INI-CET 2022 q023 was completed in its place.
  - [x] Batch 6 - 10 images converted, linked, synchronized, and verified with the darker Medicomm watermark (87 of 104 complete).
  - [x] Batch 7 - 10 images converted, linked, synchronized, and verified with the darker Medicomm watermark (97 of 104 complete); the blocked NEET PG 2021 q004 clinical source remains pending.
  - [x] Final batch - 7 images converted, linked, synchronized, and verified with the darker Medicomm watermark (104 of 104 complete); NEET PG 2021 q004 was completed as a non-graphic medical cutaway.
- Pharmacology atlas conversion batches:
  - [x] Batch 1 - 10 images converted, linked, synchronized, and verified with the darker Medicomm watermark (12 of 21 complete); legacy Marrow watermarks removed before import.
- ENT atlas conversion batches:
  - [x] Batch 1 - 10 images converted, linked, synchronized, and verified with the darker Medicomm watermark (10 of 44 complete).
- Anesthesia atlas-image pass complete. The saved method is in `docs/medicomm-atlas-image-standard.md`.
- Website sync verified: the latest ten atlas URLs and PNGs are present in both `public/` and `dist/`.
