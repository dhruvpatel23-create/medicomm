# /img1 Image Completion Checklist

Tracker for PYQ image batches completed using the new copyright-safe Medicomm `/img1` style.

## Summary

- Subjects started: 1
- Subject-year batches completed: 3
- Completed questions: 62 (45 from 2017–2019, 17 from 2020)
- Anatomy 2020: 17/18 questions installed using 16 unique images; one identical skull image reused.

## Completed Batches

| Subject | Year | Exams Covered | Images Done | Status | Manifest |
| --- | ---: | --- | ---: | --- | --- |
| Anatomy | 2017 | AIIMS 2017 | 16 | Done | `output/imagegen/anatomy-2017-img1/manifest.json` |
| Anatomy | 2018 | AIIMS 2018, NEET PG 2018 | 7 | Done | `output/imagegen/anatomy-2018-img1/manifest.json` |
| Anatomy | 2019 | AIIMS 2019, NEET PG 2019 | 22 | Done | `output/imagegen/anatomy-2019-animated/final-manifest.json` |
| Anatomy | 2020 | AIIMS/INI-CET 2020, NEET PG 2020 | 17/18 | Partial: AIIMS Q20 pending marker review | `output/imagegen/anatomy-2020-img1/final-manifest.json` |

## Subject Checklist

- [x] Anatomy
  - [x] 2017 image-based PYQs
  - [x] 2018 image-based PYQs
  - [x] 2019 image-based PYQs
  - [ ] 2020 image-based PYQs — 17 installed; `aiims-2020-anatomy-q020` pending

## Notes

- "Done" means the generated images are saved, copied into upload directories, linked in the question banks, and usable by the local website after cache/server refresh.
- Add each new completed subject-year batch here immediately after website verification.
- 2020: recovered the correct laryngeal reference for AIIMS Q14 from PDF page 86; the old mapping incorrectly reused the sphenoid image. All 17 installed question references and gallery image loads passed browser verification. Generation prompts and rejected cranial-nerve attempts are recorded in `output/imagegen/anatomy-2020-img1/generation-manifest.json`; do not regenerate accepted images when resuming.
