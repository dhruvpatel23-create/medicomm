import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_swinging_flashlight_test(output_path):
    # Medical diagnostic atlas: Swinging Flashlight Test (RAPD / Relative Afferent Pupillary Defect)
    # 4-stage clinical sequence demonstrating pupillary constriction vs paradoxical dilation
    # on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Beam of Penlight -->
        <linearGradient id="lightBeam" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#fef08a" stop-opacity="0.95"/>
          <stop offset="50%" stop-color="#fde047" stop-opacity="0.5"/>
          <stop offset="100%" stop-color="#ca8a04" stop-opacity="0.05"/>
        </linearGradient>

        <!-- Penlight Torch Body Gradient -->
        <linearGradient id="torchBody" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#64748b"/>
          <stop offset="50%" stop-color="#cbd5e1"/>
          <stop offset="100%" stop-color="#334155"/>
        </linearGradient>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Header Pill -->
      <g id="header">
        <rect x="320" y="20" width="560" height="44" rx="22" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="600" y="49" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" text-anchor="middle" letter-spacing="1">SWINGING FLASHLIGHT TEST (PUPILLARY REFLEX)</text>
      </g>

      <!-- 4 Horizontal Sequential Panels:
           Rows at y = 80, 280, 480, 680
           Panel dimensions: width=1120, height=185
      -->

      <!-- ================= PANEL 1: BASELINE ================= -->
      <g transform="translate(40, 80)">
        <rect width="1120" height="185" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        
        <!-- Step Badge -->
        <rect x="25" y="20" width="220" height="34" rx="17" fill="#1e293b" stroke="#475569" stroke-width="1"/>
        <text x="135" y="42" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">STEP 1: AMBIENT LIGHT</text>
        <text x="135" y="85" fill="#64748b" font-family="sans-serif" font-size="12" text-anchor="middle">Equal baseline resting pupils</text>
        <text x="135" y="110" fill="#64748b" font-family="sans-serif" font-size="12" text-anchor="middle">Both pupils equal (4 mm)</text>

        <!-- Right Eye (Viewer's Left, cx=440, cy=95) -->
        <g transform="translate(440, 95)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="24" fill="#3b2d1d"/>
          <!-- Pupil: 4mm (r=12) -->
          <circle cx="0" cy="0" r="12" fill="#000000"/>
          <circle cx="-3" cy="-3" r="3" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -38 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="600" text-anchor="middle">Right Eye: 4 mm</text>
        </g>

        <!-- Left Eye (Viewer's Right, cx=800, cy=95) -->
        <g transform="translate(800, 95)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="24" fill="#3b2d1d"/>
          <!-- Pupil: 4mm (r=12) -->
          <circle cx="0" cy="0" r="12" fill="#000000"/>
          <circle cx="-3" cy="-3" r="3" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -38 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="600" text-anchor="middle">Left Eye: 4 mm</text>
        </g>
      </g>

      <!-- ================= PANEL 2: LIGHT ON LEFT EYE ================= -->
      <g transform="translate(40, 280)">
        <rect width="1120" height="185" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        
        <!-- Step Badge -->
        <rect x="25" y="20" width="220" height="34" rx="17" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
        <text x="135" y="42" fill="#10b981" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">STEP 2: LIGHT ON LEFT EYE</text>
        <text x="135" y="85" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">Normal afferent pathway</text>
        <text x="135" y="110" fill="#38bdf8" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Both pupils CONSTRICT (2 mm)</text>

        <!-- Right Eye (Consensual constriction: r=6) -->
        <g transform="translate(440, 95)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="24" fill="#3b2d1d"/>
          <!-- Pupil: 2mm (r=6) -->
          <circle cx="0" cy="0" r="6" fill="#000000"/>
          <circle cx="-2" cy="-2" r="2" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -38 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#10b981" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Right Eye: 2 mm (Consensual)</text>
        </g>

        <!-- Left Eye (Direct constriction: r=6) with torch beam -->
        <g transform="translate(800, 95)">
          <!-- Torch Light Beam -->
          <polygon points="0,-75 -60,20 60,20" fill="url(#lightBeam)"/>
          <!-- Torch Penlight Body -->
          <rect x="-8" y="-120" width="16" height="45" rx="3" fill="url(#torchBody)" stroke="#1e293b"/>
          <circle cx="0" cy="-75" r="8" fill="#fde047"/>

          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="24" fill="#3b2d1d"/>
          <!-- Pupil: 2mm (r=6) -->
          <circle cx="0" cy="0" r="6" fill="#000000"/>
          <circle cx="-2" cy="-2" r="2" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -38 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#10b981" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Left Eye: 2 mm (Direct)</text>
        </g>
      </g>

      <!-- ================= PANEL 3: LIGHT SWUNG TO RIGHT EYE (KEY FINDING) ================= -->
      <g transform="translate(40, 480)">
        <!-- Highlighted border for abnormal step -->
        <rect width="1120" height="185" rx="12" fill="#171221" stroke="#f59e0b" stroke-width="2.5"/>
        
        <!-- Step Badge -->
        <rect x="25" y="20" width="230" height="34" rx="17" fill="#f59e0b"/>
        <text x="140" y="42" fill="#0f172a" font-family="sans-serif" font-size="13" font-weight="800" text-anchor="middle">STEP 3: SWUNG TO RIGHT EYE</text>
        <text x="140" y="85" fill="#fca5a5" font-family="sans-serif" font-size="12" font-weight="600" text-anchor="middle">Defective afferent input</text>
        <text x="140" y="110" fill="#f59e0b" font-family="sans-serif" font-size="13" font-weight="800" text-anchor="middle">Both pupils DILATE (5 mm)!</text>

        <!-- Right Eye (Abnormal response: paradoxically dilates to r=16) with torch beam -->
        <g transform="translate(440, 95)">
          <!-- Torch Light Beam -->
          <polygon points="0,-75 -60,20 60,20" fill="url(#lightBeam)"/>
          <rect x="-8" y="-120" width="16" height="45" rx="3" fill="url(#torchBody)" stroke="#1e293b"/>
          <circle cx="0" cy="-75" r="8" fill="#fde047"/>

          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="24" fill="#3b2d1d"/>
          <!-- Pupil: 5mm (r=16 - DILATED!) -->
          <circle cx="0" cy="0" r="16" fill="#000000"/>
          <circle cx="-4" cy="-4" r="3.5" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -38 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#f59e0b" font-family="sans-serif" font-size="13" font-weight="800" text-anchor="middle">Right Eye: 5 mm (Dilates)</text>
        </g>

        <!-- Left Eye (Consensually dilates with Right eye: r=16) -->
        <g transform="translate(800, 95)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="24" fill="#3b2d1d"/>
          <!-- Pupil: 5mm (r=16 - DILATED!) -->
          <circle cx="0" cy="0" r="16" fill="#000000"/>
          <circle cx="-4" cy="-4" r="3.5" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -38 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#f59e0b" font-family="sans-serif" font-size="13" font-weight="800" text-anchor="middle">Left Eye: 5 mm (Dilates)</text>
        </g>
      </g>

      <!-- ================= PANEL 4: LIGHT BACK TO LEFT EYE ================= -->
      <g transform="translate(40, 680)">
        <rect width="1120" height="185" rx="12" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        
        <!-- Step Badge -->
        <rect x="25" y="20" width="220" height="34" rx="17" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
        <text x="135" y="42" fill="#10b981" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">STEP 4: SWUNG BACK TO LEFT</text>
        <text x="135" y="85" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">Afferent input restored</text>
        <text x="135" y="110" fill="#38bdf8" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Both pupils RE-CONSTRICT (2 mm)</text>

        <!-- Right Eye (Consensual re-constriction: r=6) -->
        <g transform="translate(440, 95)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="24" fill="#3b2d1d"/>
          <circle cx="0" cy="0" r="6" fill="#000000"/>
          <circle cx="-2" cy="-2" r="2" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -38 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#10b981" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Right Eye: 2 mm (Re-constricts)</text>
        </g>

        <!-- Left Eye (Direct re-constriction: r=6) with torch beam -->
        <g transform="translate(800, 95)">
          <polygon points="0,-75 -60,20 60,20" fill="url(#lightBeam)"/>
          <rect x="-8" y="-120" width="16" height="45" rx="3" fill="url(#torchBody)" stroke="#1e293b"/>
          <circle cx="0" cy="-75" r="8" fill="#fde047"/>

          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="24" fill="#3b2d1d"/>
          <circle cx="0" cy="0" r="6" fill="#000000"/>
          <circle cx="-2" cy="-2" r="2" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -38 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#10b981" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Left Eye: 2 mm (Re-constricts)</text>
        </g>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/q006_swinging_flashlight.png")
    res = generate_swinging_flashlight_test(out)
    print("Q006 Swinging Flashlight:", res, out.exists())
