import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_titmus_stereotest(output_path):
    # Medical equipment atlas: Titmus Stereotest apparatus
    # Open booklet featuring the 3D stereoscopic housefly (vectograph) and graded test circles,
    # alongside polarizing 3D evaluation spectacles on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Booklet cover / page shading -->
        <linearGradient id="bookCover" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1e293b"/>
          <stop offset="100%" stop-color="#0f172a"/>
        </linearGradient>
        <linearGradient id="pageGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#f8fafc"/>
          <stop offset="70%" stop-color="#f1f5f9"/>
          <stop offset="100%" stop-color="#e2e8f0"/>
        </linearGradient>

        <!-- Polarizing lens gradient -->
        <radialGradient id="polarLens" cx="45%" cy="45%" r="55%">
          <stop offset="0%" stop-color="#334155"/>
          <stop offset="60%" stop-color="#1e293b"/>
          <stop offset="100%" stop-color="#0f172a"/>
        </radialGradient>

        <!-- Vectographic Housefly Body Gradients -->
        <radialGradient id="flyThorax" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#475569"/>
          <stop offset="70%" stop-color="#1e293b"/>
          <stop offset="100%" stop-color="#0f172a"/>
        </radialGradient>
        <linearGradient id="flyAbdomen" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#334155"/>
          <stop offset="25%" stop-color="#64748b"/>
          <stop offset="50%" stop-color="#334155"/>
          <stop offset="75%" stop-color="#64748b"/>
          <stop offset="100%" stop-color="#1e293b"/>
        </linearGradient>

        <!-- Translucent Veined Fly Wings with Vectograph Fringe -->
        <linearGradient id="wingShine" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#bae6fd" stop-opacity="0.6"/>
          <stop offset="50%" stop-color="#e0f2fe" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="#7dd3fc" stop-opacity="0.5"/>
        </linearGradient>

        <filter id="pageShadow" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="0" dy="15" stdDeviation="20" flood-color="#000000" flood-opacity="0.9"/>
        </filter>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- MAIN STEREO TEST BOOKLET (Open Binder: 740 x 780, centered at x=640, y=450) -->
      <g id="stereotest_booklet" filter="url(#pageShadow)">
        <!-- Leatherette Outer Binder -->
        <rect x="290" y="50" width="760" height="800" rx="16" fill="url(#bookCover)" stroke="#334155" stroke-width="3"/>
        <!-- Central Spine / Spiral wire -->
        <line x1="670" y1="50" x2="670" y2="850" stroke="#090d16" stroke-width="12"/>
        <line x1="670" y1="50" x2="670" y2="850" stroke="#475569" stroke-width="3" stroke-dasharray="16,8"/>

        <!-- LEFT PAGE (Pediatric & Graded Stereo Tests) -->
        <g id="left_page">
          <rect x="310" y="70" width="340" height="760" rx="8" fill="url(#pageGrad)" stroke="#cbd5e1" stroke-width="1.5"/>
          
          <!-- Section 1: Graded Circles (Wirt Rings) -->
          <text x="480" y="110" fill="#1e293b" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">GRADED STEREO CIRCLES</text>
          
          <!-- 3x3 Grid of Diamond Target Blocks -->
          <!-- We draw 9 diamond groups with 4 circles each -->
          <g transform="translate(340, 130)">
            <!-- Group 1 -->
            <rect x="0" y="0" width="80" height="80" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
            <circle cx="40" cy="22" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="22" cy="40" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="58" cy="40" r="9" fill="#0f172a" stroke="#0f172a" stroke-width="1"/> <!-- Disparity circle -->
            <circle cx="40" cy="58" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            
            <!-- Group 2 -->
            <rect x="100" y="0" width="80" height="80" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
            <circle cx="140" cy="22" r="9" fill="#0f172a"/>
            <circle cx="122" cy="40" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="158" cy="40" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="140" cy="58" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>

            <!-- Group 3 -->
            <rect x="200" y="0" width="80" height="80" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
            <circle cx="240" cy="22" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="222" cy="40" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="258" cy="40" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="240" cy="58" r="9" fill="#0f172a"/>

            <!-- Row 2 -->
            <rect x="0" y="100" width="80" height="80" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
            <circle cx="22" cy="140" r="9" fill="#0f172a"/>
            <circle cx="40" cy="122" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="58" cy="140" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="40" cy="158" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>

            <rect x="100" y="100" width="80" height="80" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
            <circle cx="140" cy="122" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="122" cy="140" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="158" cy="140" r="9" fill="#0f172a"/>
            <circle cx="140" cy="158" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>

            <rect x="200" y="100" width="80" height="80" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
            <circle cx="240" cy="122" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="222" cy="140" r="9" fill="#0f172a"/>
            <circle cx="258" cy="140" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
            <circle cx="240" cy="158" r="9" fill="none" stroke="#0f172a" stroke-width="2.5"/>
          </g>

          <!-- Section 2: Animal Figures for Children -->
          <text x="480" y="360" fill="#1e293b" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">ANIMAL TEST (CHILDREN)</text>
          <g transform="translate(340, 380)">
            <!-- 3 Rows of silhouetted animals -->
            <rect x="0" y="0" width="280" height="60" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
            <text x="140" y="36" fill="#475569" font-family="sans-serif" font-size="14" font-weight="600" text-anchor="middle">ROW A: 400 sec arc</text>

            <rect x="0" y="80" width="280" height="60" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
            <text x="140" y="116" fill="#475569" font-family="sans-serif" font-size="14" font-weight="600" text-anchor="middle">ROW B: 200 sec arc</text>

            <rect x="0" y="160" width="280" height="60" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
            <text x="140" y="196" fill="#475569" font-family="sans-serif" font-size="14" font-weight="600" text-anchor="middle">ROW C: 100 sec arc</text>
          </g>
        </g>

        <!-- RIGHT PAGE (The Iconic 3D Stereoscopic Housefly Vectograph) -->
        <g id="right_page">
          <rect x="690" y="70" width="340" height="760" rx="8" fill="url(#pageGrad)" stroke="#cbd5e1" stroke-width="1.5"/>
          
          <text x="860" y="110" fill="#1e293b" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">HOUSEFLY STEREO TEST</text>
          <text x="860" y="132" fill="#64748b" font-family="sans-serif" font-size="13" font-weight="600" text-anchor="middle">Gross Stereopsis: 3000 sec arc</text>

          <!-- Large Stereoscopic Housefly (Centered at cx=860, cy=440) -->
          <g id="vectograph_housefly" transform="translate(860, 440)">
            <!-- Polarization Double-Image Effect (Subtle cyan/red stereo offset halo) -->
            <g opacity="0.3" transform="translate(-4, 0)">
              <ellipse cx="0" cy="100" rx="42" ry="70" fill="#0284c7"/>
              <ellipse cx="-60" cy="30" rx="65" ry="120" transform="rotate(-35, -60, 30)" fill="#0284c7"/>
              <ellipse cx="60" cy="30" rx="65" ry="120" transform="rotate(35, 60, 30)" fill="#0284c7"/>
            </g>
            <g opacity="0.3" transform="translate(4, 0)">
              <ellipse cx="0" cy="100" rx="42" ry="70" fill="#e11d48"/>
              <ellipse cx="-60" cy="30" rx="65" ry="120" transform="rotate(-35, -60, 30)" fill="#e11d48"/>
              <ellipse cx="60" cy="30" rx="65" ry="120" transform="rotate(35, 60, 30)" fill="#e11d48"/>
            </g>

            <!-- Main Fly Body -->
            <!-- Head & Compound Eyes -->
            <circle cx="0" cy="-60" r="32" fill="#0f172a"/>
            <!-- Left Compound Eye -->
            <ellipse cx="-20" cy="-65" rx="16" ry="22" fill="#7f1d1d" stroke="#991b1b" stroke-width="1"/>
            <!-- Right Compound Eye -->
            <ellipse cx="20" cy="-65" rx="16" ry="22" fill="#7f1d1d" stroke="#991b1b" stroke-width="1"/>
            <!-- Antennae -->
            <path d="M -10 -85 Q -15 -105 -25 -110" fill="none" stroke="#0f172a" stroke-width="3"/>
            <path d="M 10 -85 Q 15 -105 25 -110" fill="none" stroke="#0f172a" stroke-width="3"/>

            <!-- Thorax (Strong broad segment) -->
            <ellipse cx="0" cy="5" rx="50" ry="46" fill="url(#flyThorax)" stroke="#0f172a" stroke-width="2"/>
            <!-- Thorax longitudinal stripes -->
            <path d="M -22 -30 L -22 40" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>
            <path d="M -8 -35 L -8 45" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>
            <path d="M 8 -35 L 8 45" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>
            <path d="M 22 -30 L 22 40" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>

            <!-- Abdomen (Segmented striped oval) -->
            <ellipse cx="0" cy="110" rx="46" ry="75" fill="url(#flyAbdomen)" stroke="#0f172a" stroke-width="2"/>
            <!-- Segment bands -->
            <path d="M -42 70 Q 0 82 42 70" stroke="#0f172a" stroke-width="3" fill="none"/>
            <path d="M -45 105 Q 0 118 45 105" stroke="#0f172a" stroke-width="3" fill="none"/>
            <path d="M -40 140 Q 0 152 40 140" stroke="#0f172a" stroke-width="3" fill="none"/>

            <!-- Transparent Veined Wings Spread Outwards -->
            <!-- Left Wing -->
            <g transform="rotate(-32, -30, -5)">
              <ellipse cx="-60" cy="40" rx="55" ry="135" fill="url(#wingShine)" stroke="#0284c7" stroke-width="2.5"/>
              <!-- Wing Veins -->
              <path d="M -30 -60 C -45 10 -55 80 -65 160" stroke="#0369a1" stroke-width="2" fill="none"/>
              <path d="M -45 10 C -70 40 -85 90 -95 130" stroke="#0369a1" stroke-width="1.5" fill="none"/>
              <path d="M -40 -10 C -20 40 -20 100 -35 150" stroke="#0369a1" stroke-width="1.5" fill="none"/>
            </g>

            <!-- Right Wing -->
            <g transform="rotate(32, 30, -5)">
              <ellipse cx="60" cy="40" rx="55" ry="135" fill="url(#wingShine)" stroke="#0284c7" stroke-width="2.5"/>
              <!-- Wing Veins -->
              <path d="M 30 -60 C 45 10 55 80 65 160" stroke="#0369a1" stroke-width="2" fill="none"/>
              <path d="M 45 10 C 70 40 85 90 95 130" stroke="#0369a1" stroke-width="1.5" fill="none"/>
              <path d="M 40 -10 C 20 40 20 100 35 150" stroke="#0369a1" stroke-width="1.5" fill="none"/>
            </g>

            <!-- Fly Legs (Jointed black legs) -->
            <path d="M -40 -10 L -90 -30 L -125 -10" stroke="#0f172a" stroke-width="4.5" fill="none"/>
            <path d="M 40 -10 L 90 -30 L 125 -10" stroke="#0f172a" stroke-width="4.5" fill="none"/>
            <path d="M -45 20 L -100 40 L -135 75" stroke="#0f172a" stroke-width="4.5" fill="none"/>
            <path d="M 45 20 L 100 40 L 135 75" stroke="#0f172a" stroke-width="4.5" fill="none"/>
            <path d="M -35 80 L -80 120 L -110 170" stroke="#0f172a" stroke-width="4.5" fill="none"/>
            <path d="M 35 80 L 80 120 L 110 170" stroke="#0f172a" stroke-width="4.5" fill="none"/>
          </g>
        </g>
      </g>

      <!-- POLARIZING 3D GLASSES (Foreground equipment at bottom-left: x=40, y=550) -->
      <g id="polarizing_glasses" filter="url(#pageShadow)" transform="translate(60, 520) scale(0.95)">
        <!-- Frames -->
        <rect x="0" y="30" width="280" height="90" rx="20" fill="#090d16" stroke="#475569" stroke-width="4"/>
        
        <!-- Left Lens (Polaroid Dark Gray) -->
        <rect x="20" y="42" width="105" height="66" rx="14" fill="url(#polarLens)" stroke="#64748b" stroke-width="2"/>
        <!-- Polarizing filter axis lines -->
        <line x1="30" y1="52" x2="115" y2="98" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.6"/>
        
        <!-- Bridge -->
        <path d="M 125 50 Q 140 42 155 50" fill="none" stroke="#475569" stroke-width="8"/>

        <!-- Right Lens (Polaroid Dark Gray) -->
        <rect x="155" y="42" width="105" height="66" rx="14" fill="url(#polarLens)" stroke="#64748b" stroke-width="2"/>
        <line x1="165" y1="98" x2="250" y2="52" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.6"/>

        <!-- Left Temple Piece (Folding back) -->
        <path d="M 0 45 L -45 10 L -50 -60" fill="none" stroke="#090d16" stroke-width="8"/>
        <!-- Right Temple Piece -->
        <path d="M 280 45 L 320 15 L 325 -55" fill="none" stroke="#090d16" stroke-width="8"/>

        <!-- Label Pill on Glasses -->
        <rect x="50" y="130" width="180" height="34" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="140" y="152" fill="#38bdf8" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">POLARIZING GLASSES</text>
      </g>

      <!-- NEUTRAL MARKER POINTER (Pointing to test booklet) -->
      <g id="neutral_marker">
        <path d="M 180 80 L 260 80 L 305 100" fill="none" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="305,100 292,94 296,106" fill="#f59e0b"/>
        
        <rect x="40" y="55" width="200" height="48" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="140" y="85" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" text-anchor="middle">TEST APPARATUS</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/q002_titmus_fly.png")
    res = generate_titmus_stereotest(out)
    print("Q002 Titmus Fly:", res, out.exists())
