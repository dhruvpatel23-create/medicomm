import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_fish_hook_injury(output_path):
    # Medical atlas illustration: Penetrating ocular trauma by barbed fish hook
    # Showing the anterior segment, corneal impalement, and magnified anatomical inset
    # detailing the retention barb mechanism on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Cornea & Iris Gradients -->
        <radialGradient id="irisBlue" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#0284c7"/>
          <stop offset="50%" stop-color="#0369a1"/>
          <stop offset="85%" stop-color="#075985"/>
          <stop offset="100%" stop-color="#0c4a6e"/>
        </radialGradient>
        
        <radialGradient id="corneaGlow" cx="45%" cy="40%" r="55%">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.45"/>
          <stop offset="70%" stop-color="#38bdf8" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#0284c7" stop-opacity="0.4"/>
        </radialGradient>

        <!-- Sclera with Ciliary Injection -->
        <radialGradient id="scleraInj" cx="50%" cy="50%" r="50%">
          <stop offset="65%" stop-color="#ffffff"/>
          <stop offset="85%" stop-color="#fee2e2"/>
          <stop offset="95%" stop-color="#ef4444"/>
          <stop offset="100%" stop-color="#991b1b"/>
        </radialGradient>

        <!-- Metallic Fish Hook Steel Gradient -->
        <linearGradient id="hookSteel" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#f8fafc"/>
          <stop offset="25%" stop-color="#94a3b8"/>
          <stop offset="50%" stop-color="#cbd5e1"/>
          <stop offset="75%" stop-color="#475569"/>
          <stop offset="100%" stop-color="#1e293b"/>
        </linearGradient>

        <filter id="metalShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="4" dy="6" stdDeviation="6" flood-color="#000000" flood-opacity="0.7"/>
        </filter>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- MAIN CLINICAL EYE VIEW (Left portion: centered around cx=460, cy=460) -->
      <g id="clinical_eye_view">
        <!-- Eyelids / Periorbital frame -->
        <path d="M 120 460 C 220 260 400 220 500 220 C 600 220 740 260 840 460 C 740 660 600 700 500 700 C 400 700 220 660 120 460 Z" 
              fill="#c29170" stroke="#8c5838" stroke-width="3"/>
        
        <!-- Sclera with acute traumatic injection -->
        <path d="M 150 460 C 240 290 400 250 500 250 C 600 250 720 290 810 460 C 720 630 600 670 500 670 C 400 670 240 630 150 460 Z" 
              fill="url(#scleraInj)"/>

        <!-- Conjunctival Vessels radiating from trauma site -->
        <g stroke="#dc2626" stroke-linecap="round" fill="none" opacity="0.8">
          <path d="M 170 450 Q 280 440 360 450" stroke-width="4"/>
          <path d="M 200 400 Q 290 410 360 430" stroke-width="3"/>
          <path d="M 200 520 Q 290 510 360 490" stroke-width="3"/>
          <path d="M 780 440 Q 680 430 620 440" stroke-width="3.5"/>
          <path d="M 760 390 Q 670 410 620 430" stroke-width="3"/>
          <path d="M 760 530 Q 670 510 620 490" stroke-width="3"/>
        </g>

        <!-- Cornea & Limbus (cx=490, cy=460, r=160) -->
        <circle cx="490" cy="460" r="160" fill="#0f172a" stroke="#7f1d1d" stroke-width="3"/>
        <!-- Iris -->
        <circle cx="490" cy="460" r="156" fill="url(#irisBlue)"/>
        <!-- Pupil (Irregular traumatic corectopia peaked towards hook entry) -->
        <!-- Hook enters at 8 o'clock (cx=390, cy=520); pupil is pulled towards it -->
        <path d="M 440 490 C 450 440 480 410 520 420 C 560 430 570 480 540 510 C 500 540 430 530 440 490 Z" fill="#090d16"/>

        <!-- Corneal transparency / reflex -->
        <circle cx="490" cy="460" r="160" fill="url(#corneaGlow)"/>

        <!-- PENETRATING METALLIC FISH HOOK IN EYE -->
        <!-- Curved metallic hook with eyelet, shank, bend, point, and barb -->
        <g id="fish_hook_globe" filter="url(#metalShadow)">
          <!-- Hook Line / Filament attached to eyelet -->
          <path d="M 160 680 Q 240 640 310 600" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,2"/>

          <!-- Eyelet (Loop) at (310, 600) -->
          <circle cx="310" cy="600" r="14" fill="none" stroke="url(#hookSteel)" stroke-width="7"/>

          <!-- Shank -->
          <path d="M 318 593 L 400 525" stroke="url(#hookSteel)" stroke-width="11" stroke-linecap="round"/>

          <!-- Curved Bend entering cornea at (410, 515) -->
          <path d="M 400 525 C 430 500 455 520 445 560" fill="none" stroke="url(#hookSteel)" stroke-width="10"/>

          <!-- Point and Barb penetrating cornea into anterior chamber -->
          <path d="M 445 560 L 420 590" stroke="url(#hookSteel)" stroke-width="8" stroke-linecap="round"/>
          <!-- Sharp Barb backward spur -->
          <polygon points="428,575 442,568 434,582" fill="url(#hookSteel)"/>

          <!-- Wound Sealing / Localized corneal stromal edema halo -->
          <ellipse cx="420" cy="530" rx="30" ry="24" fill="#ffffff" opacity="0.55"/>
          <ellipse cx="420" cy="530" rx="14" ry="10" fill="#fef08a" opacity="0.8"/>
        </g>
      </g>

      <!-- MAGNIFIED INSET DIAGRAM (Right side: centered at cx=970, cy=450) -->
      <g id="magnified_inset">
        <!-- Inset Border / Container -->
        <rect x="760" y="160" width="410" height="580" rx="16" fill="#0b1329" stroke="#334155" stroke-width="2.5" filter="url(#metalShadow)"/>
        
        <!-- Header Pill -->
        <rect x="790" y="185" width="350" height="40" rx="20" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="965" y="211" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" text-anchor="middle">BARBED PENETRATION DETAIL</text>

        <!-- Cornea Cross-Section Layer Representation -->
        <!-- Epithelium, Stroma, Endothelium -->
        <g transform="translate(800, 360)">
          <!-- Corneal Stroma block -->
          <path d="M 30 0 C 120 20 220 20 310 0 L 310 100 C 220 120 120 120 30 100 Z" fill="#0369a1" opacity="0.6"/>
          <!-- Epithelium outer surface -->
          <path d="M 30 0 C 120 20 220 20 310 0" fill="none" stroke="#38bdf8" stroke-width="4"/>
          <!-- Endothelium inner surface -->
          <path d="M 30 100 C 120 120 220 120 310 100" fill="none" stroke="#38bdf8" stroke-width="4"/>

          <!-- Large Detailed Fish Hook Model inside corneal tissue -->
          <!-- Hook Shaft entering from outside (top-left) -->
          <path d="M 80 -80 C 130 -10 170 30 180 80 C 190 130 170 170 140 180 C 100 190 80 150 90 120" 
                fill="none" stroke="url(#hookSteel)" stroke-width="16" stroke-linecap="round"/>

          <!-- Sharp Penetrating Tip -->
          <polygon points="90,120 95,90 75,105" fill="#f8fafc"/>

          <!-- THE BARB (Engaging corneal tissue, preventing backward withdrawal) -->
          <path d="M 92 105 L 125 125 L 110 135 Z" fill="#f8fafc" stroke="#475569" stroke-width="1.5"/>

          <!-- Biomechanical Resistance Vector (Red arrows showing tissue entrapment) -->
          <!-- Attempted backward withdrawal vector -->
          <path d="M 180 180 L 220 220" stroke="#ef4444" stroke-width="3" fill="none" stroke-dasharray="6,4"/>
          <polygon points="175,175 190,178 178,190" fill="#ef4444"/>
          <text x="240" y="240" fill="#f87171" font-family="sans-serif" font-size="13" font-weight="700">TISSUE TRAP</text>
        </g>

        <!-- Descriptive Note inside inset -->
        <rect x="790" y="630" width="350" height="75" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>
        <text x="965" y="658" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="600" text-anchor="middle">Retrograde barb engages ocular stroma.</text>
        <text x="965" y="682" fill="#f59e0b" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Do not pull backward; requires advance &amp; cut.</text>
      </g>

      <!-- Connecting leader line from eye hook to inset -->
      <path d="M 430 540 C 580 520 680 400 760 380" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,4"/>
      <circle cx="430" cy="540" r="5" fill="#38bdf8"/>

      <!-- NEUTRAL MARKER POINTER TARGETING FOREIGN BODY -->
      <g id="neutral_marker">
        <path d="M 280 340 L 370 340 L 405 470" fill="none" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="405,470 395,458 408,458" fill="#f59e0b"/>
        
        <rect x="80" y="315" width="220" height="48" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="190" y="345" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" text-anchor="middle">FOREIGN BODY</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/q003_fish_hook.png")
    res = generate_fish_hook_injury(out)
    print("Q003 Fish Hook Injury:", res, out.exists())
