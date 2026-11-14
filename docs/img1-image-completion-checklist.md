# /img1 Image Completion Checklist

Tracker for PYQ image batches completed using the new copyright-safe Medulla `/img1` style.

## Radiology and General Medicine complete — 15 November 2026

- Radiology: 80 source groups linked to 81 questions.
- General Medicine: 80 source groups linked to 81 questions. The final 20 groups used 16 new images and four reviewed reuses. The final review galleries and installation manifests are in `output/imagegen/general-medicine-img1/batch-05/` and `batch-06/`.
- Verified the image references in the data, public, and dist question banks and compared SHA-256 hashes across all four upload directories. The isolated frontend build passed. The local API returned 503 during the final live check.
- NEET PG 2024 General Medicine Q009 still has unreadable imported answer choices. Its four-panel ECG image was replaced.

## General Medicine batch 04 — 2 November 2026

- Source groups 46–60 reviewed and installed: 14 new built-in image_gen PNGs, one source-compared batch01 ECG reuse, and one lateral-sole stimulus correction (15 generation calls total).
- All four upload locations and three practice banks synchronized with backups; non-image content preserved. 30 live image hashes,60 asset copies,45 saved question references verified; readiness200/session401. Practice API requires authentication; no real-user login used.
- Plan,prompts,correction,source-comparison gallery,installation hashes and verification: `output/imagegen/general-medicine-img1/batch-04/`.
- Total completed:60 groups. Remaining:20. Next batch:61–75.

## General Medicine batch 03 — 1 November 2026

- Source groups 31–45 completed across 16 questions: 13 new built-in image_gen PNGs and two source-compared reuses (batch 01 ECG and batch 02 pleural-effusion image).
- 15 generation calls including two targeted corrections: inferior-lead P-wave amplitude and normal spirometry FEV1 endpoint/curve agreement.
- Source-versus-generated review completed for all images, including reflex instrument contact, abnormal clock numbers, ECG timing, graph values/axes, realistic CSF cytology and scan laterality.
- Four upload directories and all three practice banks synchronized with timestamped backups. Non-image content preserved; account storage untouched.
- Live verification: 30 image hashes, 60 asset-copy hashes, 48 question references; readiness 200 and unauthenticated sessions 401. Practice API requires authentication; saved bank references verified without real-user login.
- Plan, prompts, corrections, source-comparison gallery, installation hashes and verification: `output/imagegen/general-medicine-img1/batch-03/`.
- Total completed: 45 source groups. Remaining: 35. Next batch: indices 46–60.

## General Medicine batch 02 — 1 November 2026

- Next 15 source groups (indices 16–30) visually compared and installed: 14 new built-in image_gen PNGs and one reviewed reuse from batch 01.
- 16 generation calls: 14 initial images plus two corrections for timeline row alignment and realistic urinary-crystal microscopy.
- Removed the unrelated hypokalemia ECG from NEET PG 2019 General Medicine Q010 (Bundle of Kent); attached the reviewed replacement to Q011. All non-image content preserved.
- Assets synchronized and hash-verified in four upload directories and three practice banks, with timestamped backups. Live checks: 30 image hashes, readiness 200 and unauthenticated sessions 401; authenticated practice API returned 401, so 45 saved bank references verified directly.
- Review gallery, prompts, source plan, corrections, installation hashes and verification: `output/imagegen/general-medicine-img1/batch-02/`.
- Total completed: 30 source groups. Remaining: 50. Next batch: indices 31–45.

## General Medicine batch 01 — 1 November 2026

- 15 source groups (AIIMS 2017–2019 and NEET PG 2018) replaced with 15 original built-in image_gen PNGs; source-versus-output review completed.
- 17 tool calls total: 15 initial images and two ECG lead-label corrections. Repeated ECGs have different arrow information and were kept separate.
- Removed the unrelated adjacent-question ECG from AIIMS 2018 General Medicine Q001; clinical content preserved.
- Four upload directories and all three question banks synchronized, with timestamped backups and SHA-256 verification. Account storage untouched.
- Plan, prompts, corrections, visual reviews, source comparisons and installation manifest: `output/imagegen/general-medicine-img1/batch-01/`.
- Live images verified on both ports; readiness 200 and unauthenticated sessions 401. Practice API requires authentication; bank references verified directly without a real-user login.
- 65 source groups remain; next batch starts at indices 16–30.

## Radiology batch 01 — 30 October 2026

- 15 original PNG images generated with the built-in image tool and visually compared with source references.
- Scope: next 15 pending NEET-PG Radiology source groups (2018–2019); previously saved images were retained.
- Preserved projection, laterality, modality, findings and exact pointer targets. No watermarks or added answer labels; original matching-question terms and scan order retained.
- One IVP image corrected before installation to restore the bilateral intravesical cobra-head sacs and radiolucent halos.
- Installed and hash-verified in all four upload directories and linked in all three question banks. Non-image question fields preserved; original sources and timestamped bank backups retained.
- Removed an incorrect chest-radiograph attachment from `neet-pg-2019-radiology-q004` (cerebral infarct). Its source belongs to `neet-pg-2019-radiology-q005`, which received the replacement.
- Prompts and visual review: `output/imagegen/radiology-img1/batch-01/review-manifest.json`.
- Installation, hashes and backups: `output/imagegen/radiology-img1/batch-01/installed-manifest.json`.
- Root Radiology review manifest and source-group registry updated so the next batch can resume without regenerating these assets.

## Pathology 2020 installation (Batch 1 of 5) — 2026-09-26

- Installed 14 reviewed assets: 14 original SVG vector atlas medical illustrations & diagrams.
- Critical bugfixes: Corrected legacy mapping errors where `neet-pg-2020-pathology-q003` was mapped to kidney biopsy instead of Papillary Thyroid Carcinoma Orphan Annie eye nuclei, and `neet-pg-2020-pathology-q022` was mapped to metaplasia diagram instead of Myocardial Contraction Band Necrosis.
- Copied assets to `public/uploads/`, `data/uploads/`, `dist/uploads/`, and `runtime-data/uploads/` and updated image references in all three practice question banks (`data/`, `public/`, `dist/`).
- Bumped `PRACTICE_LIBRARY_CACHE_KEY` in `src/App.jsx` to `medicomm-practice-library-cache-v20260926-path2020` and re-built production bundle (`npm run build`).
- Verified HTTP 200 delivery and non-zero byte counts across both Vite (4173) and API (4174).
- Preserved question stems, options, answers, explanations, and non-image fields completely.
- Installation manifest: `output/imagegen/pathology-2020-img1/installed-manifest.json`; review gallery: `output/imagegen/pathology-2020-img1/review-gallery.html` and `public/pathology-2020-gallery.html`.

## Biochemistry 2017–2019 installation — 2026-09-26

- Installed 5 reviewed assets: 3 PNG medical illustrations and 2 original SVG vector diagrams/charts.
- Copied assets to `public/`, `data/`, `dist/`, and `runtime-data/` uploads and updated image references in all three practice question banks.
- Bumped `PRACTICE_LIBRARY_CACHE_KEY` in `src/App.jsx` and re-built production bundle (`npm run build`).
- Verified HTTP 200 delivery and byte counts across both Vite (4173) and API (4174).
- Preserved question stems, options, answers, explanations, and non-image fields completely.
- Installation manifest: `output/imagegen/biochemistry-2017-2019-img1/installed-manifest.json`; review gallery: `output/imagegen/biochemistry-2017-2019-img1/review-gallery.html` and `public/biochemistry-2017-2019-gallery.html`.

## Biochemistry 2020–2024 installation — 2026-09-26

- Installed 16 reviewed assets: 11 PNG medical illustrations and 5 original SVG vector charts.
- 1 metadata cleanup: removed accidental duplicate image from `ini-cet-2024-biochemistry-q002` (text-only theory question).
- Copied assets to `public/`, `data/`, `dist/`, and `runtime-data/` uploads and updated image references in all three practice question banks.
- Preserved question stems, options, answers, explanations, and non-image fields completely.
- Installation manifest: `output/imagegen/biochemistry-2020-2024-img1/installed-manifest.json`; review gallery: `output/imagegen/biochemistry-2020-2024-img1/review-gallery.html`.

## Physiology 2022–2024 installation — 2026-09-25

- Installed 16 previously reviewed assets: 5 AI-generated PNG illustrations and 11 original SVG charts.
- Copied assets to public/data/dist/runtime-data uploads and updated image references in all three practice question banks.
- Preserved question text, options, answers, explanations, and original source-image references.
- Verified all 16 question links through the running API and confirmed served image bytes match the saved assets.
- Installation manifest: `output/imagegen/physiology-2022-2024-img1/installed-manifest.json`; original prompts and review records remain alongside it.

## Summary

- Subjects started: 3 (Anatomy, Physiology, Biochemistry)
- Subject-year batches completed: 6
- Completed questions: 103; 19 existing atlas images pending future /img1 conversion
- Anatomy 2020: 17/18 questions installed using 16 unique images; one identical skull image reused.
- Biochemistry 2017–2019: 5 installed assets across 5 questions.
- Biochemistry 2020–2024: 16 installed assets across 17 questions (1 text-only cleanup).

## Completed Batches

| Subject | Year | Exams Covered | Images Done | Status | Manifest |
| --- | ---: | --- | ---: | --- | --- |
| Pathology | 2020 | AIIMS 2020, NEET PG 2020 | 14 | Done | `output/imagegen/pathology-2020-img1/installed-manifest.json` |
| Anatomy | 2017 | AIIMS 2017 | 16 | Done | `output/imagegen/anatomy-2017-img1/manifest.json` |
| Anatomy | 2018 | AIIMS 2018, NEET PG 2018 | 7 | Done | `output/imagegen/anatomy-2018-img1/manifest.json` |
| Anatomy | 2019 | AIIMS 2019, NEET PG 2019 | 22 | Done | `output/imagegen/anatomy-2019-animated/final-manifest.json` |
| Anatomy | 2020 | AIIMS/INI-CET 2020, NEET PG 2020 | 17/18 | Partial: AIIMS Q20 pending marker review | `output/imagegen/anatomy-2020-img1/final-manifest.json` |
| Physiology | 2022–2024 | INI-CET & NEET PG (2022–2024) | 16 | Done | `output/imagegen/physiology-2022-2024-img1/installed-manifest.json` |
| Biochemistry | 2017–2019 | AIIMS & NEET PG (2017–2019) | 5 | Done | `output/imagegen/biochemistry-2017-2019-img1/installed-manifest.json` |
| Biochemistry | 2020–2024 | INI-CET & NEET PG (2020–2024) | 16 | Done (16 installed, 1 text cleanup) | `output/imagegen/biochemistry-2020-2024-img1/installed-manifest.json` |

## Subject Checklist

- [ ] Pathology
  - [x] 2020 image-based PYQs — 14 installed (Batch 1 of 5)
  - [ ] 2021 image-based PYQs (Batch 2)
  - [ ] 2022 image-based PYQs (Batch 3)
  - [ ] 2023 image-based PYQs (Batch 4)
  - [ ] 2024 image-based PYQs (Batch 5)
- [x] Anatomy
  - [x] 2017 image-based PYQs
  - [x] 2018 image-based PYQs
  - [x] 2019 image-based PYQs
  - [ ] 2020 image-based PYQs — 17 installed; `aiims-2020-anatomy-q020` pending
- [x] Physiology
  - [x] 2022–2024 image-based PYQs — 16 installed
- [x] Biochemistry
  - [x] 2017–2019 image-based PYQs — 5 installed
  - [x] 2020–2024 image-based PYQs — 16 installed, 1 text cleanup

## Notes

- "Done" means the generated images are saved, copied into upload directories, linked in the question banks, and usable by the local website after cache/server refresh.
- Add each new completed subject-year batch here immediately after website verification.
- 2020: recovered the correct laryngeal reference for AIIMS Q14 from PDF page 86; the old mapping incorrectly reused the sphenoid image. All 17 installed question references and gallery image loads passed browser verification. Generation prompts and rejected cranial-nerve attempts are recorded in `output/imagegen/anatomy-2020-img1/generation-manifest.json`; do not regenerate accepted images when resuming.

## Anatomy 2021–2022 credit-saving pass — 2026-09-19

- [ ] 2021: 11 converted; 10 existing atlas images pending future /img1 conversion.
- [ ] 2022: 8 converted; 9 existing atlas images pending future /img1 conversion.
- Both years cover INI-CET and NEET PG. Existing atlas images were reused to reduce credit usage; this was not a full style redraw.
- 19 replacements installed in public/data/dist/runtime-data uploads; all three question banks updated, preserving all non-image fields.
- All 38 image loads, question references, and mobile gallery layouts passed browser verification.
- Final two label edits were installed without an additional visual review, at user request. The initially blocked pelvic-floor generation succeeded as a label-only edit.
- Final manifest and prompts: output/imagegen/anatomy-2021-2022-img1/final-manifest.json. Generation history: irst-pass-generation-manifest.json, correction-manifest.json, inal-edits.json in the same directory. Built-in image generation used.
- Galleries: /anatomy-2021-gallery.html and /anatomy-2022-gallery.html.

## Future /img1 conversion queue: 19 reused anatomy images

Current website images remain installed. Convert these in a future pass; do not regenerate them now. Machine-readable queue: docs/img1-pending-anatomy-2021-2022.json.

- [ ] ini-cet-2021-anatomy-q001
- [ ] ini-cet-2021-anatomy-q002
- [ ] ini-cet-2021-anatomy-q003
- [ ] ini-cet-2021-anatomy-q005
- [ ] ini-cet-2021-anatomy-q010
- [ ] ini-cet-2021-anatomy-q014
- [ ] ini-cet-2021-anatomy-q015
- [ ] ini-cet-2021-anatomy-q016
- [ ] ini-cet-2021-anatomy-q022
- [ ] neet-pg-2021-anatomy-q003
- [ ] ini-cet-2022-anatomy-q004
- [ ] ini-cet-2022-anatomy-q022
- [ ] ini-cet-2022-anatomy-q024
- [ ] ini-cet-2022-anatomy-q027
- [ ] ini-cet-2022-anatomy-q030
- [ ] ini-cet-2022-anatomy-q033
- [ ] neet-pg-2022-anatomy-q001
- [ ] neet-pg-2022-anatomy-q003
- [ ] neet-pg-2022-anatomy-q005


## Anatomy 2023?2024 recovery ? 2026-09-22

- 28 prior generated images recovered and mapped to their original question IDs; 18 had remained only in the generator output folder.
- 4 new images saved with built-in image generation; 32 images now saved, not yet installed.
- Two clinical infant references blocked by the image tool: INI-CET 2023 Q18 and NEET PG 2024 Q5. No repeat attempts.
- NEET PG 2024 Q6 draft needs its thoracoacromial artery label endpoint corrected.
- NEET PG 2024 Q1 has no source image; the skull image belongs to Q2. Existing association needs cleanup.
- Gallery: output/imagegen/anatomy-2023-2024-img1/review-gallery.html. Prompts, paths, checksums and statuses are in review-manifest.json; new prompts are in resume-prompts.json.
- All 32 PNG files validated; detailed review and website installation remain pending.
