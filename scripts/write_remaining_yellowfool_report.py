import json
from collections import Counter
from audit_remaining_yellowfool import ROOT, STAGE

report = json.loads((STAGE / 'merge-report.json').read_text(encoding='utf-8'))
verification = json.loads((STAGE / 'verification.json').read_text(encoding='utf-8'))
report['verification'] = verification
(ROOT / 'docs/yellowfool-remaining-import-report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
lines = [
    '# Yellowfool remaining-subject import', '',
    'Imported 2026-09-16; local website verification completed 2026-09-17.', '',
    'All 2,104 remaining source entries are represented by 2,103 questions: 1,706 newly added and 397 existing questions enriched in place. One identical Dermatology question was consolidated while retaining both PDF occurrence references.', '',
    '| Subject | Source entries | New | Updated | Final PYQs | Source images |',
    '| --- | ---: | ---: | ---: | ---: | ---: |',
]
for row in report['subjects']:
    lines.append(f"| {row['subject']} | {row['source']} | {row['added']} | {row['updated']} | {row['totalPyqs']} | {row['images']} |")
lines += [
    '', '## Preservation and duplicate checks', '',
    '- Existing question IDs, unmatched questions, AI content, and unselected subjects were preserved.',
    '- Matched duplicates use the original website IDs plus `sourceQuestionId` for traceability. Longer existing stems retain transcribed laboratory values.',
    '- Matching considered normalized stems, options, subject and exam; weaker candidates were reviewed. The unrelated pauci-immune question was retained.',
    '- Both occurrences of the identical AIIMS 2019 Dermatology rash question map to one record through `sourceQuestionIds` and `additionalSourceOccurrences`.',
    '- No exact stem-and-option duplicates remain within an exam and subject in the imported subjects. Questions repeated in different exam years retain their separate exam attribution.',
    '- Existing alternate recalls with different stems/options were preserved when there was insufficient evidence to merge them.',
    '- Source answer keys replace older answers for matched questions; changes are recorded in the companion JSON. This pass verifies transcription, not independent medical correctness.',
    '', '## Corrected source indexing and extraction', '',
    '- The old checklist counted 120 Radiology entries as Psychiatry NEET 2024. PDF chapter headings identify their actual subjects, exams and years; they now appear in Radiology. Psychiatry has 115 source questions.',
    '- Removed answer-key headings from final options, table-of-contents text from final explanations, and encoded HTML comparison symbols.',
    '- Recovered additional figures, tables, and images on pages shared with answer keys or explanations. Converted JPEG 2000 assets to browser-compatible PNG.',
    '- The 557 source images are synchronized across public, data, runtime-data and dist uploads. Source images remain original; atlas conversion is separate.',
    '', '## Source limitations', '',
    '- Surgery INI-CET 2024 ends during explanation 2. Questions 3–33 have answer keys but no detailed explanations in this PDF. These 31 omissions and the truncated explanation are explicitly marked; no explanations were invented.',
    f"- {len(report['contextGaps'])} questions are flagged for missing referenced laboratory tables or numbered statements in the source. Where existing website text supplied the missing data, it was retained instead. Flags appear as source notes in explanations and as structured metadata.",
    '- All source entries were imported, including incomplete ones. The flagged questions need a more complete source before they can be treated as fully usable standalone questions.',
    '', '### Questions with missing source context', '',
]
for row in report['contextGaps']:
    lines.append(f"- `{row['sourceQuestionId']}`: {row['note']}")
lines += [
    '', '## Verification', '',
    '- Verified all 2,104 source references occur exactly once across 2,103 imported records.',
    '- Checked four nonempty options, answer-index consistency, explanation presence, subject/exam-year mapping, and unique IDs.',
    '- Confirmed live `/api/practice` returns the expected subject counts, question IDs, answers, options and image URLs.',
    '- All 557 image URLs returned HTTP 200 with image content; files were decoded for integrity and checked in all four asset locations.',
    '- Data and public banks were updated independently to preserve an existing unrelated Anatomy asset difference. Dist uses the public bank.',
    '- Original banks are backed up under `output/yellowfool-remaining/backup-20260916-231943/`.',
    '', 'Companion audit: [yellowfool-remaining-import-report.json](yellowfool-remaining-import-report.json).',
    '', '## Reproduction', '',
    'The staged extraction files live under `output/yellowfool-remaining/`. Run the stage script per remaining subject (the Psychiatry pass also extracts Radiology), then the cleanup, content audit, image recovery, and asset finalization scripts. Review duplicate candidates before running `merge_remaining_yellowfool.py --apply`. The merge script contains the reviewed matches for this specific source snapshot. Run `verify_remaining_yellowfool.py` against the local server after importing. Do not use the original replacement importer over these completed subjects.',
]
(ROOT / 'docs/yellowfool-remaining-import-report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('Completion report and machine-readable audit written.')
