# Topic-wise option review

The offline audit is `python scripts/audit_topic_options.py`. The report and remaining review queue are written to `output/topic-wise-option-audit/`. It makes no model or network calls. A longest answer is a review signal, not proof of a defective question.

Apply explicitly reviewed edits with `python scripts/audit_topic_options.py --apply`. The editorial source is `scripts/reviewed_topic_options.py`. Original options and answer positions are retained in `data/topic-wise-option-revisions.json`. Server-side overrides cover older stored copies only when the original stem, options, and key still match. Changed questions and official PYQs are not overwritten.

For new or revised topic-wise questions:

- Preserve the stem and the intended correct concept. Use four distinct, plausible options of the same clinical category and grammatical form.
- Give options comparable specificity and detail. Keep explanations, synonyms, teaching points, and mechanisms out of only the correct option; put teaching material in the explanation.
- Preserve essential negations, doses, units, durations, qualifiers, and combination treatments. Never shorten an answer automatically at punctuation or parentheses.
- Use parallel formats: all diagnostic names, all mechanisms, all regimens, or all comparable numerical ranges as the question requires. Expand or abbreviate equivalent nomenclature consistently across choices.
- Do not pad distractors, add random text, change the font or spacing to disguise length, or make the correct answer systematically shortest instead.
- Check that exactly one option is best for the unchanged stem. Review aggregate longest/shortest-answer rates as well as individual outliers.

The initial editorial pass covers 60 extreme cases. The subsequent correct-option-only cleanup scanned the remaining 7,522 flagged answers and shortened 710 using explicit approved removals in `data/topic-wise-correct-option-cleanup.json`. No distractor, stem, explanation, or answer index changes in this pass. The other 6,812 are unchanged, not certified bias-free.

Validate this cleanup with `python scripts/clean_correct_options.py`; add `--apply` to apply it to local banks. This is an offline, idempotent operation. Original wording is preserved in the manifest. The server and import sync apply these same approved changes to matching older stored copies. The report is `output/topic-wise-option-audit/correct-option-cleanup-report.json`. No paid model calls are made.
