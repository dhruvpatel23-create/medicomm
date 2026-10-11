import subprocess
import os
from pathlib import Path
from PIL import Image

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_html_to_png(html_content, output_png_path, width=1200, height=900):
    output_png_path = Path(output_png_path).resolve()
    temp_html = output_png_path.with_suffix('.html')
    
    # Wrap html to ensure exact sizing and zero margin
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: {width}px;
    height: {height}px;
    background-color: #000000;
    overflow: hidden;
  }}
</style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    temp_html.write_text(full_html, encoding='utf-8')
    
    cmd = [
        EDGE_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={width},{height}",
        "--hide-scrollbars",
        f"--screenshot={str(output_png_path)}",
        f"file:///{str(temp_html).replace(os.sep, '/')}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if output_png_path.exists():
        # Verify and resize/crop if necessary
        with Image.open(output_png_path) as im:
            if im.size != (width, height):
                # Crop or resize exactly to width, height
                cropped = im.crop((0, 0, width, height))
                cropped.save(output_png_path, "PNG")
        if temp_html.exists():
            temp_html.unlink()
        return True
    return False

if __name__ == "__main__":
    test_html = """
    <div style="width:1200px; height:900px; display:flex; align-items:center; justify-content:center; background:#000000;">
        <h1 style="color:#38bdf8; font-family:sans-serif; font-size:48px;">MEDICOMM ATLAS RENDERER READY</h1>
    </div>
    """
    out = Path("scripts/generate_14_oph_atlas/test_out.png")
    success = render_html_to_png(test_html, out, 1200, 900)
    print("Render success:", success, "Exists:", out.exists())
    if out.exists():
        im = Image.open(out)
        print("Image size:", im.size)
