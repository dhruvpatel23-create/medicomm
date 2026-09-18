# USMLE Step 1 — Module 1 authoring review

## Scope and status

15 original integrated questions, authored using the project's [USMLE question-writing recipe](USMLE_Question_Writing_Recipe.html). Module 1 combines disciplines and organ systems. Modules 2–10 remain empty. This is a teaching block, not a claim to reproduce the examination's content proportions.

Each item has five choices, a single keyed answer, an explanation, a reasoning chain, an educational objective, individual option rationales, and source references. Topic and discipline labels are shown after checking an answer rather than before it. Four items use laboratory tables. The communication and biostatistics items complement the clinical mechanism and prediction questions.

Author source checks and numerical checks are complete. **Independent physician/subject-matter review has not been performed.** The recipe's independent-review checklist item therefore remains open; the items are not represented as clinically validated or official USMLE material.

## Source and concept audit

The local PDFs were read directly. PDF page numbers below are **one-based viewer pages**, which may differ from printed page numbers. References in the app identify them explicitly as PDF pages. No textbook images or copied vignettes were used.

| Item | Integrated endpoint | Source checked |
| --- | --- | --- |
| 1 | Oxidant-associated hemolysis → G6PD → NADPH-dependent glutathione regeneration | Vasudevan et al., *Textbook of Biochemistry for Medical Students*, 6th ed., chs. 10, 20, 23; PDF 131–132, 253, 286 |
| 2 | Cholera secretion → preserved sodium-glucose absorption → oral rehydration | Sastry & Bhat, *Essentials of Medical Microbiology*, 4th ed., ch. 42, PDF 953–955, 962–964; Khurana, *Medical Physiology for Undergraduate Students*, 1st ed., ch. 7.7, PDF 523–524; Goodman & Gilman, 14th ed., ch. 54, PDF 1115 |
| 3 | Bilateral renal artery stenosis → ACE inhibition → efferent dilation and lower GFR | Goodman & Gilman, 14th ed., ch. 30, PDF 612, 619 |
| 4 | Low-PTH hypocalcemia + thymic/T-cell deficiency → pharyngeal-pouch development | *Robbins & Cotran Pathologic Basis of Disease*, 10th ed., chs. 5–6, PDF 178–179, 252–253 |
| 5 | Terminal ileal loss → B12 depletion → impaired methylmalonyl-CoA mutase | Vasudevan et al., 6th ed., chs. 11, 34, PDF 149, 419–421 |
| 6 | Lateral medullary deficits → nucleus ambiguus and palatal/laryngeal weakness | B. D. Chaurasia, *Human Anatomy*, vol. 3, 6th ed., chs. 24–25, PDF 357–360, 399–400 |
| 7 | Hyperammonemia + low citrulline + orotic aciduria → OTC block and pyrimidine overflow | Vasudevan et al., 6th ed., chs. 14, 39, PDF 193–195, 482–483 |
| 8 | Salicylate exposure → simultaneous metabolic acidosis and respiratory alkalosis | Goodman & Gilman, 14th ed., ch. 42, PDF 858–859; *Harrison's Principles of Internal Medicine*, 20th ed., ch. 51, table 51-1, printed p. 315 / PDF 361 |
| 9 | Pulmonary-renal injury + linear IgG → alpha-3 type IV collagen antigen | Robbins & Cotran, 10th ed., chs. 6, 20, PDF 219, 911–913 |
| 10 | CF phenotype + Phe508del → misfolding, ER retention, proteasomal degradation | Robbins & Cotran, 10th ed., ch. 10, PDF 475–479 |
| 11 | TMP-SMX synergy → sequential microbial folate-pathway inhibition | Goodman & Gilman, 14th ed., ch. 57, PDF 1156–1157 |
| 12 | Activating KCNJ11 variant → drug-induced KATP closure → depolarization and calcium influx | Goodman & Gilman, 14th ed., ch. 51, PDF 1043, 1047–1049, 1052–1053 |
| 13 | ADA deficiency → dATP accumulation → inhibited ribonucleotide reductase | Vasudevan et al., 6th ed., ch. 39, PDF 480–483; Robbins & Cotran, 10th ed., ch. 6, PDF 251–252 |
| 14 | Treatment-related fear → empathic acknowledgment and open-ended exploration | *Clinical Methods*, 3rd ed., [ch. 3, The Medical Interview](https://www.ncbi.nlm.nih.gov/books/NBK349/); Goodman & Gilman, 14th ed., ch. 69, PDF 1356–1357 for hydroxyurea context |
| 15 | Prevalence + sensitivity/specificity → positive predictive value | *Clinical Methods*, 3rd ed., [ch. 6, Sensitivity, Specificity, and Predictive Value](https://www.ncbi.nlm.nih.gov/books/NBK383/) |

## Construction checks

- A knowledgeable learner can formulate the answer from the stem and lead-in before seeing choices.
- Each distractor includes a stated reason it does not fit this case or tested mechanism.
- No negative lead-ins, “all of the above,” or “none of the above.”
- Vignettes are original; no legacy pathology question was moved into the module.
- Clinical stems plus lead-ins are mostly around 80–100 words.
- Neonatal laboratory ranges are labeled as the laboratory's age-specific intervals.
- ADA-related dATP inhibition is described as a contributing mechanism, not the sole cause of lymphocyte toxicity.
- The KCNJ11 item explicitly establishes drug-induced channel closure to avoid assuming every mutation responds to sulfonylureas.
- The screening assay is hypothetical; stated operating characteristics are not attributed to a real clinical assay.
- Chapter-title corrections made during audit: Goodman & Gilman renin/angiotensin is ch. 30; the antimicrobial chapter is ch. 57, *DNA Disruptors: Sulfonamides, Quinolones, and Nitroimidazoles*.

## Numerical verification

- Item 8 anion gap: `140 − (100 + 14) = 26 mEq/L`.
- Item 8 expected PaCO2: `1.5 × 14 + 8 ± 2 = 29 ± 2 mm Hg`; observed 20 is below that range.
- Item 8 Henderson–Hasselbalch consistency: `6.1 + log10(14 / (0.03 × 20)) ≈ 7.47`.
- Item 15: 90 true positives, 45 false positives, 10 false negatives, 855 true negatives; `PPV = 90 / 135 ≈ 67%`.

## Implementation and validation

- Bank: [data/usmle-module-bank.json](../data/usmle-module-bank.json).
- Reproducible authoring source: [scripts/build_usmle_module_one.py](../scripts/build_usmle_module_one.py). Rebuilding updates Module 1 and preserves other modules.
- The API exposes `usmleModules` separately from both the PYQ subject directory and the legacy subject-specific USMLE bank.
- Existing quiz controls, local progress, account statistics, and bookmark lookup support module question IDs.
- `node scripts/check_usmle_modules.mjs`: passed bank structure, all eight discipline labels, numerical keys, live API metadata, and directory separation.
- Guest browser check: answered all 15 items, checked all explanations and references, saved/reopened a question, returned to modules, restored progress after reload, and checked mobile overflow. Passed with no browser errors.
- `npm run build -- --emptyOutDir false`: passed. Existing large-bundle warning remains.
