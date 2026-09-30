# /img1 Image Completion Checklist

Tracker for PYQ image batches completed using the new copyright-safe Medulla `/img1` style.

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
