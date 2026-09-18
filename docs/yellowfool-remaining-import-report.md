# Yellowfool remaining-subject import

Imported 2026-09-16; local website verification completed 2026-09-17.

All 2,104 remaining source entries are represented by 2,103 questions: 1,706 newly added and 397 existing questions enriched in place. One identical Dermatology question was consolidated while retaining both PDF occurrence references.

| Subject | Source entries | New | Updated | Final PYQs | Source images |
| --- | ---: | ---: | ---: | ---: | ---: |
| general-medicine | 488 | 404 | 84 | 491 | 83 |
| general-surgery | 408 | 312 | 96 | 408 | 116 |
| obgyn | 448 | 358 | 90 | 451 | 65 |
| pediatrics | 211 | 170 | 41 | 212 | 34 |
| orthopedics | 175 | 150 | 25 | 176 | 79 |
| psychiatry | 115 | 95 | 20 | 115 | 4 |
| dermatology | 139 | 116 | 22 | 138 | 90 |
| radiology | 120 | 101 | 19 | 120 | 86 |

## Preservation and duplicate checks

- Existing question IDs, unmatched questions, AI content, and unselected subjects were preserved.
- Matched duplicates use the original website IDs plus `sourceQuestionId` for traceability. Longer existing stems retain transcribed laboratory values.
- Matching considered normalized stems, options, subject and exam; weaker candidates were reviewed. The unrelated pauci-immune question was retained.
- Both occurrences of the identical AIIMS 2019 Dermatology rash question map to one record through `sourceQuestionIds` and `additionalSourceOccurrences`.
- No exact stem-and-option duplicates remain within an exam and subject in the imported subjects. Questions repeated in different exam years retain their separate exam attribution.
- Existing alternate recalls with different stems/options were preserved when there was insufficient evidence to merge them.
- Source answer keys replace older answers for matched questions; changes are recorded in the companion JSON. This pass verifies transcription, not independent medical correctness.

## Corrected source indexing and extraction

- The old checklist counted 120 Radiology entries as Psychiatry NEET 2024. PDF chapter headings identify their actual subjects, exams and years; they now appear in Radiology. Psychiatry has 115 source questions.
- Removed answer-key headings from final options, table-of-contents text from final explanations, and encoded HTML comparison symbols.
- Recovered additional figures, tables, and images on pages shared with answer keys or explanations. Converted JPEG 2000 assets to browser-compatible PNG.
- The 557 source images are synchronized across public, data, runtime-data and dist uploads. Source images remain original; atlas conversion is separate.

## Source limitations

- Surgery INI-CET 2024 ends during explanation 2. Questions 3–33 have answer keys but no detailed explanations in this PDF. These 31 omissions and the truncated explanation are explicitly marked; no explanations were invented.
- 66 questions are flagged for missing referenced laboratory tables or numbered statements in the source. Where existing website text supplied the missing data, it was retained instead. Flags appear as source notes in explanations and as structured metadata.
- All source entries were imported, including incomplete ones. The flagged questions need a more complete source before they can be treated as fully usable standalone questions.

### Questions with missing source context

- `aiims-2018-general-medicine-q010`: The source PDF omits the investigation results referenced by this question.
- `ini-cet-2021-general-medicine-q013`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-general-medicine-q024`: The source PDF omits the investigation results referenced by this question.
- `ini-cet-2022-general-medicine-q003`: The source PDF omits the investigation results referenced by this question.
- `ini-cet-2022-general-medicine-q016`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-general-medicine-q019`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-general-medicine-q020`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-general-medicine-q030`: The source PDF omits the investigation results referenced by this question.
- `ini-cet-2022-general-medicine-q050`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-general-medicine-q059`: The source PDF omits the investigation results referenced by this question.
- `ini-cet-2023-general-medicine-q002`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-general-medicine-q010`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-general-medicine-q013`: The source PDF omits the investigation results referenced by this question.
- `ini-cet-2023-general-medicine-q014`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-general-medicine-q017`: The source PDF omits the investigation results referenced by this question.
- `ini-cet-2023-general-medicine-q018`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-general-medicine-q019`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-general-medicine-q025`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-general-medicine-q027`: The source PDF omits the investigation results referenced by this question.
- `ini-cet-2024-general-medicine-q017`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2024-general-medicine-q021`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2024-general-medicine-q031`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2024-general-medicine-q032`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2024-general-medicine-q041`: The source PDF omits the numbered statements or table referenced by this question.
- `aiims-2019-general-surgery-q066`: The source PDF omits the numbered statements or table referenced by this question.
- `aiims-2019-general-surgery-q071`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-general-surgery-q020`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-general-surgery-q027`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-general-surgery-q029`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-general-surgery-q002`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-general-surgery-q031`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-general-surgery-q040`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-general-surgery-q045`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-general-surgery-q011`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-general-surgery-q016`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2024-general-surgery-q001`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-obgyn-q009`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-obgyn-q018`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-obgyn-q021`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-obgyn-q022`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-obgyn-q037`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-obgyn-q025`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-obgyn-q041`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-obgyn-q044`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-obgyn-q009`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2024-obgyn-q027`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-pediatrics-q005`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-pediatrics-q007`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-pediatrics-q010`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-pediatrics-q012`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-pediatrics-q018`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-pediatrics-q020`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-pediatrics-q021`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-pediatrics-q001`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-pediatrics-q008`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2024-pediatrics-q006`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2024-pediatrics-q011`: The source PDF omits the numbered statements or table referenced by this question.
- `aiims-2019-orthopedics-q030`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-orthopedics-q007`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2021-orthopedics-q008`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-orthopedics-q011`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-psychiatry-q008`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2023-psychiatry-q005`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-dermatology-q004`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-dermatology-q013`: The source PDF omits the numbered statements or table referenced by this question.
- `ini-cet-2022-radiology-q004`: The source PDF omits the numbered statements or table referenced by this question.

## Verification

- Verified all 2,104 source references occur exactly once across 2,103 imported records.
- Checked four nonempty options, answer-index consistency, explanation presence, subject/exam-year mapping, and unique IDs.
- Confirmed live `/api/practice` returns the expected subject counts, question IDs, answers, options and image URLs.
- All 557 image URLs returned HTTP 200 with image content; files were decoded for integrity and checked in all four asset locations.
- Data and public banks were updated independently to preserve an existing unrelated Anatomy asset difference. Dist uses the public bank.
- Original banks are backed up under `output/yellowfool-remaining/backup-20260916-231943/`.

Companion audit: [yellowfool-remaining-import-report.json](yellowfool-remaining-import-report.json).

## Reproduction

The staged extraction files live under `output/yellowfool-remaining/`. Run the stage script per remaining subject (the Psychiatry pass also extracts Radiology), then the cleanup, content audit, image recovery, and asset finalization scripts. Review duplicate candidates before running `merge_remaining_yellowfool.py --apply`. The merge script contains the reviewed matches for this specific source snapshot. Run `verify_remaining_yellowfool.py` against the local server after importing. Do not use the original replacement importer over these completed subjects.
