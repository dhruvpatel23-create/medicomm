import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_oculomotor_palsy(output_path):
    # Medical motility atlas: 9-cardinal positions of gaze showing Left Oculomotor (3rd Nerve) Palsy
    # Grid of 3x3 positions with labeled gaze directions on solid #000000 background.
    
    # We will generate individual eye pairs for each of the 9 gaze positions:
    # Patient has LEFT 3rd nerve palsy:
    # Right eye (viewer's left) behaves normally in all gazes.
    # Left eye (viewer's right) shows:
    # - Center: Ptosis + Down-and-out (hypo-exotropia) + dilated pupil when lid opened
    # - Elevation (Up, Up-Right, Up-Left): Severe impairment of elevation (SR, IO paralyzed)
    # - Depression (Down, Down-Right): Severe impairment of depression (IR paralyzed)
    # - Adduction (Right gaze): Cannot adduct past midline (MR paralyzed)
    # - Abduction (Left gaze): Normal abduction (LR6 intact)
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <radialGradient id="scleraShade" cx="50%" cy="50%" r="50%">
          <stop offset="70%" stop-color="#ffffff"/>
          <stop offset="100%" stop-color="#cbd5e1"/>
        </radialGradient>
        <linearGradient id="skinTile" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#f8dfcb"/>
          <stop offset="100%" stop-color="#e2ba99"/>
        </linearGradient>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Title / Header (Neutral Clinical Motility Grid) -->
      <g id="header">
        <rect x="360" y="20" width="480" height="42" rx="21" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="600" y="47" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" text-anchor="middle" letter-spacing="1">OCULAR MOTILITY EXAMINATION: 9 CARDINAL GAZES</text>
      </g>

      <!-- 9 Panels Grid Layout:
           Rows at y = 80, 340, 600
           Cols at x = 40, 420, 800
           Panel size: 360 x 240
      -->
      
      <!-- Macro helper in SVG using groups:
           Each panel has:
           - Frame: 360x240, rx=12, fill="#0f172a", stroke="#334155"
           - Gaze Label pill
           - Face cutaway / Eyes pair:
             Right eye center at cx=110, Left eye center at cx=250 (relative to panel)
      -->

      <!-- ================= ROW 1: UPWARD GAZES ================= -->
      
      <!-- Panel 1: DEXTROELEVATION (Up & Right) -->
      <g transform="translate(40, 80)">
        <rect width="360" height="240" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        <text x="180" y="32" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">UP &amp; RIGHT</text>
        
        <!-- Right Eye (Normal: looks Up & Right) -->
        <g transform="translate(100, 130)">
          <!-- Sclera -->
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <!-- Iris (shifted Up=-10, Right=-12) -->
          <circle cx="-12" cy="-10" r="16" fill="#3b2d1d"/>
          <circle cx="-12" cy="-10" r="6" fill="#000000"/>
          <circle cx="-14" cy="-12" r="2.5" fill="#ffffff"/>
          <path d="M -46 -2 Q 0 -30 46 -2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
        
        <!-- Left Eye (Impaired: fails to elevate / adduct, stays near midline/lower) -->
        <g transform="translate(260, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <!-- Iris (stuck in mild exotropia, limited elevation: cx=6, cy=0) -->
          <circle cx="6" cy="0" r="16" fill="#3b2d1d"/>
          <circle cx="6" cy="0" r="8" fill="#000000"/>
          <circle cx="4" cy="-2" r="2.5" fill="#ffffff"/>
          <path d="M -46 2 Q 0 -22 46 2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
      </g>

      <!-- Panel 2: ELEVATION (Straight Up) -->
      <g transform="translate(420, 80)">
        <rect width="360" height="240" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        <text x="180" y="32" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">STRAIGHT UP</text>
        
        <!-- Right Eye (Normal: looks Straight Up: cy=-12) -->
        <g transform="translate(100, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="-12" r="16" fill="#3b2d1d"/>
          <circle cx="0" cy="-12" r="6" fill="#000000"/>
          <circle cx="-2" cy="-14" r="2.5" fill="#ffffff"/>
          <path d="M -46 -2 Q 0 -32 46 -2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
        
        <!-- Left Eye (Impaired: fails to elevate, stays deviated out: cx=12, cy=2) -->
        <g transform="translate(260, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="12" cy="2" r="16" fill="#3b2d1d"/>
          <circle cx="12" cy="2" r="8" fill="#000000"/>
          <circle cx="10" cy="0" r="2.5" fill="#ffffff"/>
          <path d="M -46 2 Q 0 -20 46 2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
      </g>

      <!-- Panel 3: LAEVOELEVATION (Up & Left) -->
      <g transform="translate(800, 80)">
        <rect width="360" height="240" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        <text x="180" y="32" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">UP &amp; LEFT</text>
        
        <!-- Right Eye (Normal: adducts & elevates: cx=14, cy=-10) -->
        <g transform="translate(100, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="14" cy="-10" r="16" fill="#3b2d1d"/>
          <circle cx="14" cy="-10" r="6" fill="#000000"/>
          <circle cx="12" cy="-12" r="2.5" fill="#ffffff"/>
          <path d="M -46 -2 Q 0 -30 46 -2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
        
        <!-- Left Eye (Abducts with LR6, but cannot elevate: cx=18, cy=2) -->
        <g transform="translate(260, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="18" cy="2" r="16" fill="#3b2d1d"/>
          <circle cx="18" cy="2" r="8" fill="#000000"/>
          <circle cx="16" cy="0" r="2.5" fill="#ffffff"/>
          <path d="M -46 2 Q 0 -22 46 2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
      </g>


      <!-- ================= ROW 2: HORIZONTAL & PRIMARY GAZES ================= -->

      <!-- Panel 4: DEXTROVERSION (Right Gaze) -->
      <g transform="translate(40, 340)">
        <rect width="360" height="240" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        <text x="180" y="32" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">RIGHT GAZE</text>
        
        <!-- Right Eye (Normal: abducts fully to right: cx=-18, cy=0) -->
        <g transform="translate(100, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="-18" cy="0" r="16" fill="#3b2d1d"/>
          <circle cx="-18" cy="0" r="6" fill="#000000"/>
          <circle cx="-20" cy="-2" r="2.5" fill="#ffffff"/>
          <path d="M -46 0 Q 0 -26 46 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
        
        <!-- Left Eye (Impaired: fails to adduct, cannot cross midline: cx=0, cy=0) -->
        <g transform="translate(260, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="16" fill="#3b2d1d"/>
          <circle cx="0" cy="0" r="8" fill="#000000"/>
          <circle cx="-2" cy="-2" r="2.5" fill="#ffffff"/>
          <path d="M -46 0 Q 0 -22 46 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
      </g>

      <!-- Panel 5: PRIMARY POSITION (Center - Key Diagnostic Focus) -->
      <g transform="translate(420, 340)">
        <!-- Highlight border for primary gaze -->
        <rect width="360" height="240" rx="12" fill="#131d36" stroke="#f59e0b" stroke-width="2.5"/>
        <rect x="90" y="14" width="180" height="26" rx="13" fill="#f59e0b"/>
        <text x="180" y="32" fill="#0f172a" font-family="sans-serif" font-size="13" font-weight="800" text-anchor="middle">PRIMARY POSITION</text>
        
        <!-- Right Eye (Normal: looking straight ahead: cx=0, cy=0) -->
        <g transform="translate(100, 135)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="16" fill="#3b2d1d"/>
          <circle cx="0" cy="0" r="6" fill="#000000"/>
          <circle cx="-2" cy="-2" r="2.5" fill="#ffffff"/>
          <path d="M -46 0 Q 0 -26 46 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="45" fill="#94a3b8" font-family="sans-serif" font-size="12" font-weight="600" text-anchor="middle">Right Eye</text>
        </g>
        
        <!-- Left Eye (CLASSIC "DOWN AND OUT" + DILATED PUPIL + PTOSIS) -->
        <g transform="translate(260, 135)">
          <!-- Sclera -->
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <!-- Iris deviated OUT (cx=16) and DOWN (cy=8) -->
          <circle cx="16" cy="8" r="16" fill="#3b2d1d"/>
          <!-- DILATED PUPIL (Mydriasis, radius=9) -->
          <circle cx="16" cy="8" r="9" fill="#000000"/>
          <circle cx="14" cy="6" r="2.5" fill="#ffffff"/>
          
          <!-- Ptosis eyelid contour covering upper 60% of cornea/pupil -->
          <path d="M -46 -4 Q 0 16 46 6 L 46 -20 L -46 -20 Z" fill="#cf9f7e" stroke="#8a5a40" stroke-width="1.5"/>
          <path d="M -46 -4 Q 0 16 46 6" fill="none" stroke="#4a3020" stroke-width="2.5"/>
          
          <text x="0" y="45" fill="#f59e0b" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Left Eye</text>
        </g>
      </g>

      <!-- Panel 6: LAEVOVERSION (Left Gaze) -->
      <g transform="translate(800, 340)">
        <rect width="360" height="240" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        <text x="180" y="32" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">LEFT GAZE</text>
        
        <!-- Right Eye (Normal: adducts to left: cx=16, cy=0) -->
        <g transform="translate(100, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="16" cy="0" r="16" fill="#3b2d1d"/>
          <circle cx="16" cy="0" r="6" fill="#000000"/>
          <circle cx="14" cy="-2" r="2.5" fill="#ffffff"/>
          <path d="M -46 0 Q 0 -26 46 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
        
        <!-- Left Eye (NORMAL ABDUCTION: LR6 is intact! cx=18, cy=0) -->
        <g transform="translate(260, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="18" cy="0" r="16" fill="#3b2d1d"/>
          <circle cx="18" cy="0" r="8" fill="#000000"/>
          <circle cx="16" cy="-2" r="2.5" fill="#ffffff"/>
          <path d="M -46 0 Q 0 -26 46 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
      </g>


      <!-- ================= ROW 3: DOWNWARD GAZES ================= -->

      <!-- Panel 7: DEXTRODEPRESSION (Down & Right) -->
      <g transform="translate(40, 600)">
        <rect width="360" height="240" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        <text x="180" y="32" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">DOWN &amp; RIGHT</text>
        
        <!-- Right Eye (Normal: abducts & depresses: cx=-14, cy=10) -->
        <g transform="translate(100, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="-14" cy="10" r="16" fill="#3b2d1d"/>
          <circle cx="-14" cy="10" r="6" fill="#000000"/>
          <circle cx="-16" cy="8" r="2.5" fill="#ffffff"/>
          <path d="M -46 2 Q 0 24 46 2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
        
        <!-- Left Eye (Impaired: fails to adduct or depress normally: cx=8, cy=2) -->
        <g transform="translate(260, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="8" cy="2" r="16" fill="#3b2d1d"/>
          <circle cx="8" cy="2" r="8" fill="#000000"/>
          <circle cx="6" cy="0" r="2.5" fill="#ffffff"/>
          <path d="M -46 2 Q 0 16 46 2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
      </g>

      <!-- Panel 8: DEPRESSION (Straight Down) -->
      <g transform="translate(420, 600)">
        <rect width="360" height="240" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        <text x="180" y="32" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">STRAIGHT DOWN</text>
        
        <!-- Right Eye (Normal: depresses: cx=0, cy=12) -->
        <g transform="translate(100, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="12" r="16" fill="#3b2d1d"/>
          <circle cx="0" cy="12" r="6" fill="#000000"/>
          <circle cx="-2" cy="10" r="2.5" fill="#ffffff"/>
          <path d="M -46 2 Q 0 26 46 2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
        
        <!-- Left Eye (Impaired: fails to depress: IR paralyzed, mild intorsion by SO4, cx=14, cy=4) -->
        <g transform="translate(260, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="14" cy="4" r="16" fill="#3b2d1d"/>
          <circle cx="14" cy="4" r="8" fill="#000000"/>
          <circle cx="12" cy="2" r="2.5" fill="#ffffff"/>
          <path d="M -46 2 Q 0 18 46 2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
      </g>

      <!-- Panel 9: LAEVODEPRESSION (Down & Left) -->
      <g transform="translate(800, 600)">
        <rect width="360" height="240" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        <text x="180" y="32" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">DOWN &amp; LEFT</text>
        
        <!-- Right Eye (Normal: adducts & depresses: cx=14, cy=10) -->
        <g transform="translate(100, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="14" cy="10" r="16" fill="#3b2d1d"/>
          <circle cx="14" cy="10" r="6" fill="#000000"/>
          <circle cx="12" cy="8" r="2.5" fill="#ffffff"/>
          <path d="M -46 2 Q 0 24 46 2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
        
        <!-- Left Eye (Abducts with LR6, limited depression: cx=16, cy=6) -->
        <g transform="translate(260, 130)">
          <ellipse cx="0" cy="0" rx="46" ry="24" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="16" cy="6" r="16" fill="#3b2d1d"/>
          <circle cx="16" cy="6" r="8" fill="#000000"/>
          <circle cx="14" cy="4" r="2.5" fill="#ffffff"/>
          <path d="M -46 2 Q 0 22 46 2" fill="none" stroke="#94a3b8" stroke-width="2"/>
        </g>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/q017_oculomotor_palsy.png")
    res = generate_oculomotor_palsy(out)
    print("Q017 Oculomotor Palsy:", res, out.exists())
