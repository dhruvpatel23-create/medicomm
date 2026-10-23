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

The current editorial pass covers 60 extreme cases. This is not a completed bank-wide review. The rest of the bank remains in the review queue; no unreviewed question is silently rewritten or removed.
