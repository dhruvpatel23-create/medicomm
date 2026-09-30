# Project Guidelines and Command Shortcuts

## `/img1` Command

When the user types `/img1` or refers to `/img1`, apply the copyright-safe Medicomm educational illustration recipe:
- Skill location: [`.agents/skills/img1/SKILL.md`](file:///f:/dhruv1/.agents/skills/img1/SKILL.md)
- Reference document: [`docs/img1.md`](file:///f:/dhruv1/docs/img1.md)

### Purpose
Replace source/PYQ images across all medical subjects (anatomy, pathology, microbiology, pharmacology, physiology, biochemistry, ophthalmology, ENT, PSM, FMT, anesthesia, etc.) with copyright-safe Medicomm educational illustrations that preserve factual scientific content, visual logic, and exact marker targets while restyling markers and visual presentation.

Always adhere to the Base Prompt, Source-Specific Add-On, Safety Disclaimer (when applicable), Correction Prompt format, Mandatory Question Review & Visual Verification Protocol, and Acceptance Checklist defined in [`.agents/skills/img1/SKILL.md`](file:///f:/dhruv1/.agents/skills/img1/SKILL.md).

### Mandatory Question Review & Visual Verification Protocol ("Review of Questions")
Before finalizing or shipping any generated `/img1` image:
1. **Source Comparison**: Perform an explicit side-by-side visual and scientific review against the original source PYQ reference image.
2. **Fact & Curve Verification**: Verify every graph axis, tick mark, log/linear scale, curve trajectory (especially partial agonists, competitive vs. non-competitive shifts), threshold values, reference lines (e.g., 50% ED50 drop lines), and marker endpoints.
3. **No Glitches or Flattened Elements**: Ensure partial agonists are never flattened to baseline, no curves are missing, and no glitchy wireframes or artificial badges obscure the data.
4. **No Spoiler Text**: Ensure labels do not give away question answers (e.g., do NOT write "Full Agonist" or pathology diagnoses directly on test markers).
5. **Multi-Directory Sync & Build**: Only deploy across all four upload directories and question bank targets after verification is satisfied.

