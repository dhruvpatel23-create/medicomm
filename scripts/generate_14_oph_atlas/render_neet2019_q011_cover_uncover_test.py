import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_cover_uncover_test(output_path):
    # Medical diagnostic atlas: Cover-Uncover Test for Strabismus
    # 3-stage clinical procedure showing binocular fixation, occluder placement (cover test),
    # and uncover phase demonstrating corrective refixation movements on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Occluder Paddle Gradient -->
        <linearGradient id="occluderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#475569"/>
          <stop offset="40%" stop-color="#1e293b"/>
          <stop offset="100%" stop-color="#0f172a"/>
        </linearGradient>

        <radialGradient id="irisHazel" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#3b2d1d"/>
          <stop offset="70%" stop-color="#5c3822"/>
          <stop offset="100%" stop-color="#2a1810"/>
        </radialGradient>

        <filter id="panelShadow" x="-5%" y="-5%" width="110%" height="110%">
          <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.8"/>
        </filter>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Header Pill -->
      <g id="header">
        <rect x="330" y="20" width="540" height="42" rx="21" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="600" y="47" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" text-anchor="middle" letter-spacing="1">STRABISMUS DIAGNOSTIC EVALUATION</text>
      </g>

      <!-- 3 Horizontal Clinical Panels:
           Rows at y = 80, 340, 600
           Panel dimensions: width=1120, height=240
      -->

      <!-- ================= STAGE 1: BINOCULAR FIXATION (BASELINE) ================= -->
      <g transform="translate(40, 80)" filter="url(#panelShadow)">
        <rect width="1120" height="240" rx="14" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        
        <!-- Stage Label -->
        <rect x="25" y="20" width="260" height="36" rx="18" fill="#1e293b" stroke="#475569" stroke-width="1"/>
        <text x="155" y="43" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">1. BINOCULAR FIXATION</text>
        <text x="155" y="90" fill="#cbd5e1" font-family="sans-serif" font-size="13" font-weight="600" text-anchor="middle">Both eyes open</text>
        <text x="155" y="115" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">Left eye fixing on target</text>
        <text x="155" y="140" fill="#f59e0b" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Right eye deviated outward (Tropia)</text>

        <!-- Fixation Target (Star at cx=640, cy=35) -->
        <g transform="translate(640, 35)">
          <circle cx="0" cy="0" r="14" fill="#f59e0b"/>
          <text x="0" y="4" fill="#0f172a" font-family="sans-serif" font-size="12" font-weight="900" text-anchor="middle">★</text>
          <text x="0" y="26" fill="#f59e0b" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">TARGET</text>
        </g>

        <!-- Right Eye (Deviated OUT: Exotropia, cx=480, cy=135) -->
        <g transform="translate(480, 135)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <!-- Iris turned outward towards right side (viewer's left = patient's temporal: cx=-18, cy=0) -->
          <circle cx="-18" cy="0" r="22" fill="url(#irisHazel)"/>
          <circle cx="-18" cy="0" r="8" fill="#000000"/>
          <circle cx="-21" cy="-3" r="3" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -36 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#f59e0b" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Right Eye (Exotropia)</text>
          <!-- Misaligned visual axis line -->
          <line x1="-18" y1="-20" x2="-60" y2="-90" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,3"/>
        </g>

        <!-- Left Eye (Fixating target straight ahead: cx=800, cy=135) -->
        <g transform="translate(800, 135)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <!-- Iris centered looking straight: cx=0, cy=0 -->
          <circle cx="0" cy="0" r="22" fill="url(#irisHazel)"/>
          <circle cx="0" cy="0" r="8" fill="#000000"/>
          <circle cx="-3" cy="-3" r="3" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -36 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#10b981" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Left Eye (Fixating)</text>
          <!-- Direct visual axis line straight to target -->
          <line x1="0" y1="-20" x2="-145" y2="-80" stroke="#10b981" stroke-width="2" stroke-dasharray="4,3"/>
        </g>
      </g>


      <!-- ================= STAGE 2: COVER TEST (OCCLUDER PLACED ON FIXING EYE) ================= -->
      <g transform="translate(40, 340)" filter="url(#panelShadow)">
        <!-- Highlight border for active test phase -->
        <rect width="1120" height="240" rx="14" fill="#111c38" stroke="#38bdf8" stroke-width="2.5"/>
        
        <!-- Stage Label -->
        <rect x="25" y="20" width="260" height="36" rx="18" fill="#0284c7"/>
        <text x="155" y="43" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="800" text-anchor="middle">2. COVER TEST</text>
        <text x="155" y="90" fill="#bae6fd" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Cover fixing Left eye</text>
        <text x="155" y="115" fill="#f8fafc" font-family="sans-serif" font-size="12" text-anchor="middle">Observe uncovered Right eye</text>
        <text x="155" y="140" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="800" text-anchor="middle">Right eye SHIFTS INWARD to fixate!</text>

        <!-- Fixation Target -->
        <g transform="translate(640, 35)">
          <circle cx="0" cy="0" r="14" fill="#f59e0b"/>
          <text x="0" y="4" fill="#0f172a" font-family="sans-serif" font-size="12" font-weight="900" text-anchor="middle">★</text>
        </g>

        <!-- Right Eye (UNCOVERED: Makes corrective nasal saccade to fixate target!) -->
        <g transform="translate(480, 135)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <!-- Iris now centered (shifted from -18 to 0): cx=0, cy=0 -->
          <circle cx="0" cy="0" r="22" fill="url(#irisHazel)"/>
          <circle cx="0" cy="0" r="8" fill="#000000"/>
          <circle cx="-3" cy="-3" r="3" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -36 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#38bdf8" font-family="sans-serif" font-size="13" font-weight="800" text-anchor="middle">Right Eye REFIXATES</text>
          
          <!-- Movement vector arrow indicating adduction (inward shift towards center) -->
          <g stroke="#38bdf8" stroke-width="3" fill="none">
            <path d="M -26 -15 Q -10 -25 5 -15"/>
            <polygon points="5,-15 -2,-22 0,-10" fill="#38bdf8"/>
          </g>
          <line x1="0" y1="-20" x2="145" y2="-80" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,3"/>
        </g>

        <!-- Left Eye (OCCLUDED BY BLACK PADDLE) -->
        <g transform="translate(800, 135)">
          <!-- Obscured eye underneath -->
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#94a3b8" opacity="0.3"/>
          
          <!-- Opaque Black Occluder Paddle placed over left eye -->
          <!-- Handle extending down-right -->
          <path d="M 40 40 L 160 110 L 145 130 L 25 60 Z" fill="url(#occluderGrad)" stroke="#64748b" stroke-width="1.5"/>
          <!-- Circular Occluder Disk (r=50) -->
          <circle cx="0" cy="0" r="54" fill="url(#occluderGrad)" stroke="#38bdf8" stroke-width="3"/>
          <text x="0" y="5" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="800" text-anchor="middle">OCCLUDER</text>
        </g>
      </g>


      <!-- ================= STAGE 3: UNCOVER TEST (OCCLUDER REMOVED) ================= -->
      <g transform="translate(40, 600)" filter="url(#panelShadow)">
        <rect width="1120" height="240" rx="14" fill="#0b1329" stroke="#1e293b" stroke-width="2"/>
        
        <!-- Stage Label -->
        <rect x="25" y="20" width="260" height="36" rx="18" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
        <text x="155" y="43" fill="#10b981" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">3. UNCOVER TEST</text>
        <text x="155" y="90" fill="#cbd5e1" font-family="sans-serif" font-size="13" font-weight="600" text-anchor="middle">Remove occluder paddle</text>
        <text x="155" y="115" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">Left eye recovers fixation</text>
        <text x="155" y="140" fill="#f59e0b" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Right eye returns outward</text>

        <!-- Fixation Target -->
        <g transform="translate(640, 35)">
          <circle cx="0" cy="0" r="14" fill="#f59e0b"/>
          <text x="0" y="4" fill="#0f172a" font-family="sans-serif" font-size="12" font-weight="900" text-anchor="middle">★</text>
        </g>

        <!-- Right Eye (Deviates back outward: cx=-18, cy=0) -->
        <g transform="translate(480, 135)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="-18" cy="0" r="22" fill="url(#irisHazel)"/>
          <circle cx="-18" cy="0" r="8" fill="#000000"/>
          <circle cx="-21" cy="-3" r="3" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -36 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#f59e0b" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Right Eye (Returns Outward)</text>
          
          <!-- Movement arrow pointing outward -->
          <g stroke="#f59e0b" stroke-width="2.5" fill="none">
            <path d="M 0 -15 Q -10 -22 -24 -15"/>
            <polygon points="-24,-15 -17,-22 -17,-10" fill="#f59e0b"/>
          </g>
        </g>

        <!-- Left Eye (Refixates target: cx=0, cy=0) with occluder swinging away -->
        <g transform="translate(800, 135)">
          <ellipse cx="0" cy="0" rx="65" ry="34" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="22" fill="url(#irisHazel)"/>
          <circle cx="0" cy="0" r="8" fill="#000000"/>
          <circle cx="-3" cy="-3" r="3" fill="#ffffff"/>
          <path d="M -65 0 Q 0 -36 65 0" fill="none" stroke="#94a3b8" stroke-width="2"/>
          <text x="0" y="55" fill="#10b981" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Left Eye (Re-fixates)</text>

          <!-- Occluder removed (drawn faded / moved away) -->
          <g opacity="0.35" transform="translate(110, 40)">
            <circle cx="0" cy="0" r="35" fill="url(#occluderGrad)" stroke="#64748b" stroke-width="2"/>
            <path d="M 25 25 L 85 85" stroke="#64748b" stroke-width="6"/>
          </g>
        </g>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/neet2019_q011_cover_uncover_test.png")
    res = generate_cover_uncover_test(out)
    print("NEET 2019 Q011 Cover Uncover Test:", res, out.exists())
