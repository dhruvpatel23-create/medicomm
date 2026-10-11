import json
from pathlib import Path

batch_dir = Path("output/imagegen/ophthalmology-2017-2019-img1")
with open(batch_dir / "question-details.json", "r", encoding="utf-8") as f:
    qlist = json.load(f)

cards_html = []
for idx, q in enumerate(qlist, 1):
    qid = q.get("id")
    year = q.get("exam_year", "")
    exam = q.get("exam", "")
    stem = q.get("prompt", "").replace("\n", "<br>")
    options = q.get("options", [])
    correct = q.get("correct_answer", "")
    explanation = q.get("explanation", "").replace("\n", "<br>")[:400] + "..."
    concept = q.get("concept", "")

    src_img = f"source-{qid}.jpg"
    gen_img = f"medicomm-img1-{qid}.png"

    options_html = "".join([f"<li>{opt}</li>" for opt in options])

    card = f"""
    <div class="review-card" id="{qid}">
      <div class="card-header">
        <span class="badge">#{idx}</span>
        <span class="badge exam">{exam} {year}</span>
        <span class="qid">{qid}</span>
      </div>
      
      <div class="comparison-grid">
        <div class="image-box">
          <div class="label">Original PYQ Source</div>
          <img src="{src_img}" alt="Original {qid}" loading="lazy" />
        </div>
        <div class="image-box highlight">
          <div class="label gen">Medicomm Educational Illustration (/img1)</div>
          <img src="{gen_img}" alt="Generated {qid}" loading="lazy" />
        </div>
      </div>

      <div class="details-section">
        <div class="stem"><strong>Question:</strong> {stem}</div>
        <div class="options">
          <strong>Options:</strong>
          <ul>{options_html}</ul>
        </div>
        <div class="explanation">
          <strong>Explanation / Concept:</strong> {explanation}
        </div>
      </div>
    </div>
    """
    cards_html.append(card)

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Medicomm /img1 Visual Verification Gallery - Ophthalmology 2017-2019</title>
<style>
  :root {{
    --bg: #090d16;
    --card-bg: #0f172a;
    --border: #1e293b;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --accent-gold: #f59e0b;
    --success: #10b981;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    padding: 30px;
  }}
  header {{
    max-width: 1400px;
    margin: 0 auto 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
  }}
  h1 {{ font-size: 28px; color: var(--accent); margin-bottom: 8px; }}
  p.subtitle {{ color: var(--text-muted); font-size: 15px; }}
  .gallery-container {{
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 36px;
  }}
  .review-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
  }}
  .card-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
  }}
  .badge {{
    background: var(--accent);
    color: #0f172a;
    font-weight: 700;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 6px;
  }}
  .badge.exam {{
    background: var(--accent-gold);
  }}
  .qid {{
    font-family: monospace;
    font-size: 14px;
    color: var(--text-muted);
  }}
  .comparison-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
  }}
  .image-box {{
    background: #000000;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .image-box.highlight {{
    border-color: var(--accent-gold);
  }}
  .label {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 10px;
    align-self: flex-start;
  }}
  .label.gen {{
    color: var(--accent-gold);
  }}
  .image-box img {{
    max-width: 100%;
    max-height: 480px;
    object-fit: contain;
    border-radius: 4px;
  }}
  .details-section {{
    background: #090e1a;
    border: 1px solid #1a2333;
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-size: 14px;
    line-height: 1.5;
  }}
  .options ul {{
    list-style-type: none;
    margin-top: 6px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }}
  .options li {{
    background: #131b2e;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 13px;
    color: #cbd5e1;
  }}
  .explanation {{
    color: var(--text-muted);
    font-size: 13px;
    border-top: 1px dashed var(--border);
    padding-top: 8px;
  }}
</style>
</head>
<body>
  <header>
    <h1>Medicomm /img1 Visual Verification Gallery: Ophthalmology 2017-2019</h1>
    <p class="subtitle">Complete batch of 27 questions: side-by-side inspection of original PYQ references vs. newly synthesized copyright-safe educational illustrations strictly following /img1 requirements.</p>
  </header>
  <div class="gallery-container">
    {"".join(cards_html)}
  </div>
</body>
</html>
"""

output_file = batch_dir / "review-gallery.html"
output_file.write_text(full_html, encoding="utf-8")
print(f"Updated {output_file} with {len(qlist)} questions.")
