# /img1

Use `/img1` when replacing source/PYQ images from any subject with copyright-safe Medicomm educational illustrations that preserve the question's scientific content, visual logic, and marker exactly. This recipe works for anatomy, pathology, microbiology, pharmacology, physiology, biochemistry, ophthalmology, ENT, community medicine, forensic medicine, anesthesia, and other medical subjects.

## Base Prompt

```text
Use case: scientific-educational. Generate ONE original Medicomm educational medical illustration from the provided source reference. Use the reference only to preserve factual medical/scientific content, viewing direction, crop, proportions, relationships, diagnostic features, graph/table/diagram layout when relevant, and the question's exact marked target; redraw everything with original design and rendering.

Style: slightly animated medical atlas style, restrained stylized 3D/cel shading, smooth rounded shading transitions, clear tasteful outlines, detailed believable anatomy, no faces or anthropomorphism unless the source requires a neutral anatomical body surface. Solid pure black #000000 background edge to edge, no panels, no borders, no UI.

Medical colors: natural ivory bones/tendons, muted coral muscles, red arteries, blue veins, pale yellow nerves, soft gray/ivory CNS white matter, muted pink-gray CNS gray matter, and subject-appropriate microscopy/specimen/diagram colors as applicable. Use a thin gold pointer or highlight only when the question marker requires it. Preserve original letter labels, arrows, probes, marker locations, highlighted regions, graph axes, table structure, stains, panels, and target endpoints. If numbered labels are part of the question, preserve them as question information.

Arrows and pointers must be precise and error-free. Keep arrow direction, line style, endpoint, and target structure/feature faithful to the source and the question. Do not shift an arrow to a neighboring structure, nearby tissue, wrong graph point, wrong label, wrong organism part, wrong histology region, or wrong radiology finding. If an arrow endpoint is unclear in the source, use the question stem, answer, and explanation to place it on the medically correct target.

Watermark: add a small exact lowercase "medicomm" watermark in light gray at the bottom-left with safe margin. No publisher branding, no source watermark, no unrelated text.

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
- Arrows are visually clean, correctly directed, and medically accurate, with no endpoint mistakes.
- Letters, numbers, probes, arrows, panel order, and key text are preserved when question-critical.
- No answer text or new anatomy names were added.
- No publisher/source branding remains.
- Bottom-left `medicomm` watermark is subtle but visible.
- Image is usually 4:3 landscape on pure black background unless the source/question format requires otherwise.
- Output is educational and copyright-safe, not a close copy of the source rendering.

## Proven Batch Reference

The successful 2019 anatomy batch used this recipe and is saved at:

- `output/imagegen/anatomy-2019-animated/final-manifest.json`
- `output/imagegen/anatomy-2019-animated/generation-manifest.json`

Those manifests contain completed source-specific prompts for AIIMS 2019 and NEET PG 2019 anatomy images.
