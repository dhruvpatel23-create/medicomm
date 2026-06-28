# Medicomm Atlas Image Standard

Use this standard for all current and future medical question images that need cleanup or replacement.

## Source Rule

- Prefer the original source PDF image whenever available.
- Do not use previously generated replacement images as the edit target unless no source image exists.
- Preserve anatomy, proportions, orientation, relationships, arrows, and pointer lines exactly.

## Master Prompt

Create a professional 4K medical atlas vector illustration from the provided image.

- Remove original background completely.
- Use pure black background (#000000).
- Preserve all anatomical structures, proportions, orientation, and relationships exactly.
- Do not alter anatomy, invent structures, remove details, or add new annotations.
- Keep strong contrast, crisp edges, publication-quality textbook style.

Labels / arrows:

- If numbered labels exist, convert numbers to Roman numerals with teal circular markers and keep original pointer lines/arrows. Marker text must be high contrast: use white or bright yellow numerals inside dark green/teal markers, never dark numerals on dark markers.
- If arrows exist without numbered labels, preserve them exactly and add no labels or markers.
- If no arrows or labels exist, add none.

Text and watermark:

- Remove unrelated watermarking.
- Preserve only anatomically important text when required.
- Add subtle "medicomm" watermark in bottom-left corner, light gray, about 20% opacity, small and unobtrusive.

Style:

- Professional medical atlas illustration.
- Clean scientific diagram.
- Ultra-detailed, noise-free, centered, high-contrast, textbook-quality.
- Suitable for MBBS, MD, pathology, anatomy, embryology, surgery, and NEET PG preparation.

## Asset Naming

Use:

```text
medicomm-atlas-<exam>-<year>-<subject>-q<number>.png
```

Example:

```text
medicomm-atlas-aiims-2017-anatomy-q001.png
```

## Import Notes

- Store final atlas assets under `public/uploads/`.
- Update both `imageUrls` and `images` for the question.
- Add an `assetNote` explaining that the image is Medicomm atlas-style and generated from the original PDF image.
- Keep raw PDF extracts separately when useful for audit, using a `pdf-original-...` filename.
- Maintain the ordered migration tracker at `docs/medicomm-atlas-image-migration.csv`.
- For questions with multiple images, keep the original array order and use `-i1`, `-i2`, etc. in the atlas filename.

## Resume Point

Last checkpoint: 2026-06-28

- Tracker total: 384 images
- Completed: 244 images
- Remaining: 140 images
- Anatomy total: 133 images
- Anatomy completed: 133 images
- Anatomy remaining: 0 images
- Anesthesia total: 14 images
- Anesthesia completed: 14 images
- Anesthesia remaining: 0 images
- Physiology completed: 18 images
- Physiology remaining in Yellowfool physiology pass: 0 images; 2 older physiology tracker rows remain pending because their source files are missing.
- Biochemistry completed: 19 images
- Pathology total: 84 images
- Pathology completed: 60 images
- Pathology remaining: 24 images

Latest saved batch:

- Completed a 20-image pathology batch spanning H&E microscopy, blood smears, a nerve electron micrograph, a three-panel IHC plate, two instruments, and an autosomal-dominant pedigree; preserved diagnostic morphology, pointer endpoints, panel order, pale smear fields, and exact pedigree topology.
- Completed a 20-image pathology batch covering clinical photos, smears, labeled histology, gross specimens, pedigree/cascade diagrams, a 47,XXY karyotype, and lung ultrastructure; retained the larger, darker lower-left `medicomm` watermark.
- Completed the second 10-image pathology batch with a larger, darker, contrast-adjusted lower-left `medicomm` watermark. Explicitly preserved the CD19/CD40 axes in the Hyper-IgM flow-cytometry plate.
- Completed the first 10 pathology atlas images with conservative microscopy restoration and a visible lower-left `medicomm` watermark; rebuilt the stale pathology tracker from 11 legacy rows to all 84 Yellowfool source images.
- Completed 19 active biochemistry atlas images with conservative quality improvement, anatomy-style lower-left `medicomm` watermark, and source labels/diagnostic details preserved. The NEET PG 2024 John Doe/coproporphyrin item was changed to a text-only prompt.
- Verified each generated URL and PNG in `public/`, `dist/`, `data/`, and `runtime-data/` upload directories.
- Realistic dissection sources may trigger image safety filtering; retry them as clean, non-graphic textbook cutaways while preserving the original marker endpoint.
- The tracker CSV is authoritative. Start the next session by running the status and next commands below before generating anything.

Confirm the live checkpoint before resuming:

```powershell
python scripts/medicomm_atlas_migration.py status
python scripts/medicomm_atlas_migration.py next --limit 10
```

## Fast Built-in Workflow

Use the built-in image-generation tool. The paid API/CLI path is not required.

1. Read the next ordered tracker entries with `medicomm_atlas_migration.py next`.
2. Look up each question prompt and answer in `data/practice-question-bank.json` so the marked structure is understood.
3. Inspect every original image before generation. Use the raw `public/uploads/yellowfool-*` asset as the edit target.
4. For JP2 sources, create a temporary PNG under `tmp/imagegen/` for inspection and as the built-in edit target; keep the original JP2 recorded in the tracker.
5. Work in groups of three independent built-in image-generation calls for good throughput. Each image gets its own source-specific prompt.
6. Apply the master style above and explicitly lock:
   - anatomy, crop, orientation, and laterality;
   - marker text and location;
   - pointer-line direction and exact endpoint;
   - highlighted areas, probes, and important source text.
7. Inspect every output before import. Reject and regenerate mirrored anatomy, moved endpoints, renamed markers, or invented structures.
8. Import each accepted output immediately so progress is checkpointed:

```powershell
python scripts/medicomm_atlas_migration.py apply `
  --question-id <question-id> `
  --image-slot <slot> `
  --generated-path <generated-png> `
  --note "<source-specific preservation note>"
```

9. The apply helper copies the asset into all upload directories, updates `imageUrls`, `images`, `sourceImageUrls`, and `assetNote` in all three question-bank copies, then marks the tracker row done.
10. After each requested batch, verify the tracker counts, next item, and that every expected `public/uploads/medicomm-atlas-*.png` exists.

If a realistic dissection triggers image safety filtering, retry it as a clean, non-graphic medical textbook illustration while preserving the same anatomy and annotation endpoint.
