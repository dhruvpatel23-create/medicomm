---
name: img1
description: >-
  Generate copyright-safe Medicomm educational medical illustrations from source/PYQ references across all medical subjects (anatomy, pathology, microbiology, pharmacology, physiology, biochemistry, ophthalmology, ENT, community medicine, forensic medicine, anesthesia, etc.). Preserves scientific accuracy, visual logic, and exact marker endpoints while restyling markers. Trigger whenever the user mentions "/img1", asks for copyright-safe educational medical illustrations, or asks to replace medical PYQ images.
---

# /img1 - Medicomm Copyright-Safe Medical Illustration Generator

Use `/img1` when replacing source/PYQ images from any subject with copyright-safe Medicomm educational illustrations that preserve the question's scientific content, visual logic, and exact marker targets while restyling marker appearance. This recipe works for anatomy, pathology, microbiology, pharmacology, physiology, biochemistry, ophthalmology, ENT, community medicine, forensic medicine, anesthesia, and other medical subjects.

## Base Prompt

```text
Use case: scientific-educational. Generate ONE original Medicomm educational medical illustration from the provided source reference. Use the reference only to preserve factual medical/scientific content, viewing direction, crop, proportions, relationships, diagnostic features, graph/table/diagram layout when relevant, and the question's exact marked target; redraw everything with original design and rendering.

Style: slightly animated medical atlas style, restrained stylized 3D/cel shading, smooth rounded shading transitions, clear tasteful outlines, detailed believable anatomy, no faces or anthropomorphism unless the source requires a neutral anatomical body surface. Solid pure black #000000 background edge to edge, no panels, no borders, no UI.

Medical colors: natural ivory bones/tendons, muted coral muscles, red arteries, blue veins, pale yellow nerves, soft gray/ivory CNS white matter, muted pink-gray CNS gray matter, and subject-appropriate microscopy/specimen/diagram colors as applicable. Use a thin gold pointer or highlight only when the question marker requires it. Preserve original letter labels, arrows, probes, marker locations, highlighted regions, graph axes, table structure, stains, panels, and target endpoints. If numbered labels are part of the question, preserve them as question information.

Arrows and pointers must be precise and error-free. Keep arrow direction, endpoint, and target structure/feature faithful to the source and the question. Do not shift an arrow to a neighboring structure, nearby tissue, wrong graph point, wrong label, wrong organism part, wrong histology region, or wrong radiology finding. If an arrow endpoint is unclear in the source, use the question stem, answer, and explanation to place it on the medically correct target.

Marker styling: Redesign arrows to look different from the original reference: use slim shafts and small, clean arrowheads with a visibly different shape/style. Keep every arrow's direction, endpoint, and target unchanged. Change the fill and/or outline colour of numbered label circles to a contrasting colour different from the source, with clearly legible numbers. Preserve the exact numbers, label positions, and structure associations. Do not add circles where none exist. Preserve any medically meaningful colour coding and line-pattern distinctions; restyle only decorative marker features.

Watermark: add a small exact lowercase "medicomm" watermark in light gray at the bottom-left with safe margin. No publisher branding, no source watermark, no unrelated text.

Typography & Text Clarity: Render all text, numbers, axis labels, diagram annotations, and marker labels in crisp, large, high-contrast bold sans-serif lettering. Never use tiny, faint, or blurry fonts; all characters and numbers must be instantly legible and tack-sharp at high resolution across mobile and desktop displays.

Histology, Cytology & Microscopic Pathology: For histology, histopathology (H&E, PAS, reticulin, iron, etc.), cytology, blood smears, and tissue biopsies, DO NOT ANIMATE, cartoonize, or simplify into flat vector drawings. They MUST look like authentic clinical histological photomicrographs with genuine cellular morphology, realistic staining characteristics, and microscopic tissue architecture. NEVER add labels, text callouts, or titles naming the diagnostic feature, cell type, or pathology (e.g., NEVER label 'Anitschkow cell' or 'Aschoff nodule') as this gives away the answer directly. Markers must remain strictly neutral pointers without spoiler text.

Do not add the answer text or structure names unless that text is already necessary as part of the question image. Do not confuse the correct answer with the visual feature being marked; the marked feature may be an exception, nerve supply, derivative, territory, landmark, diagnostic region, organism component, histology feature, radiology sign, graph point, mechanism step, or instrument part. Maintain proportions, laterality, diagnostic landmarks, and question-critical relationships. 4:3 landscape unless the source/question requires a different aspect ratio, sharp readable composition, full required content uncropped.

Reference image 1 = original source reference only. If a second image is supplied, it is style/reference guidance only; do not copy unrelated subject content from it.
```

## Source-Specific Add-On

Append a specific content block for every image:

```text
Specific subject/content: [State the exact view, modality, specimen, diagram type, graph/table type, orientation, and crop.]

The question marker targets [exact structure/region/feature/data point]. Place the arrow/label/highlight endpoint on [precise landmark or feature], not on [common wrong neighboring structures/features]. Preserve [letters/numbers/probes/key text/panel order/axes/stain pattern] exactly. Arrows must be clean, readable, correctly directed, and endpoint-accurate. Do not add answer labels. Keep the black background and bottom-left medicomm watermark.
```

For realistic dissection or body-surface images that may trigger safety filtering, add:

```text
This is a non-graphic medical teaching illustration for anatomy students, not a photograph of a person. Use a clean stylized textbook model/cutaway with no gore and no sexual features. Preserve the same anatomical marker endpoint and educational content.
```

## Correction Prompt

Use this for targeted fixes when the generated image is mostly correct:

```text
Change ONLY [the incorrect marker/endpoint/label/highlight/anatomical segment]. Keep all other anatomy, crop, background, style, watermark, labels, and existing correct markers unchanged.

Current issue: [describe what is wrong and where it is].
Correct target: [describe exact corrected location, preferably with visual coordinates if reviewing a generated image].
Avoid: [neighboring wrong structures].
```

## Acceptance Checklist

- Source orientation, laterality, crop, modality, panel order, graph/table layout, and proportions are preserved.
- Marker endpoint is on the tested structure/feature/data point, not merely near the answer concept.
- Arrows have slim shafts and visibly different arrowhead styling from the source, while remaining correctly directed and endpoint-accurate.
- Numbered label circles use a different, high-contrast fill and/or outline colour from the source; numbers, positions, associations, and meaningful colour coding are preserved.
- Letters, numbers, probes, arrows, panel order, and key text are preserved when question-critical.
- All text, numbers, letters, axis values, and markers are bold, high-contrast, crisp, and effortlessly legible with zero blurriness.
- No answer text or new anatomy names were added.
- No publisher/source branding remains.
- Bottom-left `medicomm` watermark is subtle but visible.
- Image is usually 4:3 landscape on pure black background unless the source/question format requires otherwise.
- Output is educational and copyright-safe, not a close copy of the source rendering.

## Mandatory Question Review & Visual Verification Protocol ("Review of Questions")

Before finalizing, installing, or shipping any generated `/img1` image across any subject:
1. **Explicit Source-vs-Generated Comparison**: Directly inspect and compare the generated image against the original source PYQ image. Never finalize without visual inspection.
2. **Scientific & Graph Accuracy**:
   - Check all axis labels, units, and orientations (e.g., `Efficacy (%)`, `Log [concentration]`, log vs. linear scales).
   - Verify all tick marks and tick intervals (e.g., 0, 10, 20, ..., 100%).
   - Verify every curve trajectory: full agonists, partial agonists, competitive vs. non-competitive antagonist shifts, inverse agonists. **NEVER flatten partial agonists to zero baseline**.
   - Verify all reference lines, thresholds, and drop lines (e.g., 50% maximal effect horizontal line dropping to `ED50 [A]` and `ED50 [B]`).
3. **No Glitches or Distracting Clutter**:
   - Do NOT produce crude, distorted, or glitchy wireframe curves.
   - Do NOT add extraneous artificial badge overlays (e.g. big colored letter bubbles) that obscure the curve data unless present in the source.
4. **No Spoilers**:
   - Strictly avoid adding answer labels or diagnostic terms (e.g., "(Full Agonist)", diagnosis names in pathology) that give away the question answer directly.
5. **Multi-Directory Deployment & Sync**:
   - Only deploy to all four directories (`public/uploads/`, `data/uploads/`, `dist/uploads/`, `runtime-data/uploads/`) and update question bank targets after verification passes 100%.

## Proven Batch References

- **2019 Anatomy Batch**: `output/imagegen/anatomy-2019-animated/final-manifest.json`
- **2022-2024 Physiology Batch**: `output/imagegen/physiology-2022-2024-img1/installed-manifest.json`
- **2020-2024 Biochemistry Batch**: `output/imagegen/biochemistry-2020-2024-img1/installed-manifest.json`

## Installation & Deployment Method (Guaranteed Browser & Server Sync)

To ensure the local server and web browser immediately reflect newly generated `/img1` illustrations without serving stale images from cache:

### 1. Multi-Directory Asset Installation
Copy generated assets (`.png`, `.svg`, `.webp`) into all four application upload directories:
- `public/uploads/` (Vite static public asset root)
- `data/uploads/` (backend repo data)
- `dist/uploads/` (production bundle directory)
- `runtime-data/uploads/` (live server runtime directory)

### 2. Question Bank Update Across All Targets
Update the question metadata (`imageUrls`, `images`, `atlasImageTargetUrls`, and `assetNote`) across all three question bank files:
- `data/practice-question-bank.json`
- `public/practice-question-bank.json`
- `dist/practice-question-bank.json`

Create a timestamped backup before writing changes, and save an `installed-manifest.json` recording every question ID, source file, target URL, and SHA-256 hash.

### 3. Server In-Memory Cache Invalidation
Ensure `server.mjs` checks file `mtime` with `statSync(practiceQuestionBankPath).mtimeMs` inside `readPracticeQuestionBank()` so that disk changes to the question bank are picked up dynamically. If running a detached Node server, restart it (`node server.mjs`) on port 4174 so the process clears its memory cache.

### 4. Client Browser Cache Busting
The React frontend caches questions in `localStorage` using `PRACTICE_LIBRARY_CACHE_KEY` in `src/App.jsx`.
- When releasing a new subject batch or question updates, bump `PRACTICE_LIBRARY_CACHE_KEY` (e.g., `medicomm-practice-library-cache-vYYYYMMDD-<subject>`).
- Rebuild the frontend bundle with `npm run build`.
- This automatically invalidates any stale `localStorage` cache in user browsers upon reload, forcing a fresh fetch from `/api/practice`.

### 5. Automated Verification Protocol
Before marking the batch complete, verify:
1. Query `http://127.0.0.1:4174/api/practice` and `http://127.0.0.1:4173/api/practice` to confirm the questions return the updated `/uploads/medicomm-img1-...` URLs.
2. Perform HTTP `GET` requests against all installed URLs through both ports `4173` and `4174` and assert `HTTP 200` with non-zero payload size.
3. Advise the user to perform a hard refresh (**Ctrl + F5** / **Shift + Reload**) in their browser.
