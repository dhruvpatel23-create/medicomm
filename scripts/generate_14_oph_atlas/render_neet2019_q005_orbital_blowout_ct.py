import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_orbital_blowout_ct(output_path):
    # Medical radiological atlas: Coronal CT Scan of Orbit Blowout Fracture
    # Bone/soft-tissue window displaying floor fracture, herniation of orbital contents
    # into the maxillary sinus ("Hanging Drop / Tear Drop Sign") on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Radiological CT Density Gradients -->
        <!-- Cortical Bone Gradient (Dense white to bright ivory) -->
        <linearGradient id="boneCT" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="50%" stop-color="#f1f5f9"/>
          <stop offset="100%" stop-color="#cbd5e1"/>
        </linearGradient>

        <!-- Soft Tissue / Muscle Gray -->
        <linearGradient id="muscleCT" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#64748b"/>
          <stop offset="100%" stop-color="#475569"/>
        </linearGradient>

        <!-- Orbital Fat / Low Density Gray -->
        <radialGradient id="fatCT" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#334155"/>
          <stop offset="100%" stop-color="#1e293b"/>
        </radialGradient>

        <!-- Maxillary Sinus Fluid Level (Hemo-antrum) -->
        <linearGradient id="sinusFluid" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#475569"/>
          <stop offset="100%" stop-color="#334155"/>
        </linearGradient>

        <filter id="ctScanGlow" x="-5%" y="-5%" width="110%" height="110%">
          <feGaussianBlur stdDeviation="0.8" result="blur"/>
          <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Header Pill -->
      <g id="header">
        <rect x="340" y="20" width="520" height="42" rx="21" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="600" y="47" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" text-anchor="middle" letter-spacing="1">CORONAL CT SCAN: MID-FACE &amp; ORBITS</text>
      </g>

      <!-- Orientation Indicators (Radiological Right vs Left) -->
      <text x="120" y="90" fill="#94a3b8" font-family="sans-serif" font-size="16" font-weight="800">R</text>
      <text x="1080" y="90" fill="#94a3b8" font-family="sans-serif" font-size="16" font-weight="800">L</text>

      <!-- MAIN CT SCAN ANATOMY (Coronal Slice centered at x=600, y=470) -->
      <g id="ct_anatomy" filter="url(#ctScanGlow)">
        <!-- Cranial Vault & Superior Orbital Roofs (Thick bone: y=160 to 220) -->
        <path d="M 220 220 C 320 160 480 150 600 150 C 720 150 880 160 980 220" fill="none" stroke="url(#boneCT)" stroke-width="14" stroke-linecap="round"/>
        <!-- Frontal Sinuses / Crista Galli -->
        <path d="M 580 160 L 580 230 L 620 230 L 620 160 Z" fill="#000000" stroke="url(#boneCT)" stroke-width="5"/>

        <!-- Central Nasal Anatomy (Nasal Septum & Ethmoid Air Cells: x=520 to 680) -->
        <g id="ethmoid_and_septum">
          <!-- Nasal Septum (Vertical midline bone: x=600, y=240 to 620) -->
          <line x1="600" y1="240" x2="600" y2="620" stroke="url(#boneCT)" stroke-width="7"/>

          <!-- Ethmoid Sinus Air Cells (Black pockets with delicate white trabeculae) -->
          <rect x="525" y="240" width="70" height="150" fill="#000000" stroke="url(#boneCT)" stroke-width="3"/>
          <line x1="525" y1="290" x2="595" y2="290" stroke="url(#boneCT)" stroke-width="2"/>
          <line x1="525" y1="340" x2="595" y2="340" stroke="url(#boneCT)" stroke-width="2"/>

          <rect x="605" y="240" width="70" height="150" fill="#000000" stroke="url(#boneCT)" stroke-width="3"/>
          <line x1="605" y1="290" x2="675" y2="290" stroke="url(#boneCT)" stroke-width="2"/>
          <line x1="605" y1="340" x2="675" y2="340" stroke="url(#boneCT)" stroke-width="2"/>

          <!-- Medial Orbital Walls (Lamina Papyracea: thin white lines) -->
          <line x1="520" y1="230" x2="520" y2="400" stroke="url(#boneCT)" stroke-width="3.5"/>
          <line x1="680" y1="230" x2="680" y2="400" stroke="url(#boneCT)" stroke-width="3.5"/>

          <!-- Inferior Nasal Turbinates & Hard Palate -->
          <path d="M 550 500 Q 580 520 570 560" stroke="url(#boneCT)" stroke-width="5" fill="none"/>
          <path d="M 650 500 Q 620 520 630 560" stroke="url(#boneCT)" stroke-width="5" fill="none"/>
          <!-- Hard Palate at y=640 -->
          <line x1="380" y1="640" x2="820" y2="640" stroke="url(#boneCT)" stroke-width="9"/>
        </g>

        <!-- ================= PATIENT'S LEFT ORBIT (NORMAL CONTRALATERAL SIDE: Viewer's Right) ================= -->
        <g id="normal_left_orbit">
          <!-- Bony Orbit Cavity (x=680 to 950, y=220 to 420) -->
          <!-- Lateral Orbital Wall / Zygoma -->
          <path d="M 940 230 C 970 320 960 410 930 460" stroke="url(#boneCT)" stroke-width="12" fill="none"/>

          <!-- INTACT ORBITAL FLOOR (Smooth thin continuous white line at y=420) -->
          <path d="M 680 410 C 740 422 840 422 920 415" stroke="url(#boneCT)" stroke-width="4.5" fill="none"/>

          <!-- Orbital Cavity Contents (Fat & Muscles) -->
          <ellipse cx="800" cy="320" rx="100" ry="80" fill="url(#fatCT)"/>
          
          <!-- Globe / Optic Nerve / Muscles -->
          <!-- Superior Rectus -->
          <ellipse cx="800" cy="245" rx="30" ry="12" fill="url(#muscleCT)"/>
          <!-- Medial Rectus -->
          <ellipse cx="715" cy="320" rx="14" ry="30" fill="url(#muscleCT)"/>
          <!-- Lateral Rectus -->
          <ellipse cx="885" cy="320" rx="14" ry="30" fill="url(#muscleCT)"/>
          <!-- INTACT INFERIOR RECTUS MUSCLE (Resting cleanly on intact floor at y=400) -->
          <ellipse cx="800" cy="398" rx="34" ry="14" fill="url(#muscleCT)"/>

          <!-- Left Maxillary Sinus (Normal air-filled black cavity: x=680 to 920, y=430 to 630) -->
          <path d="M 680 430 L 920 430 L 900 630 L 680 630 Z" fill="#000000" stroke="url(#boneCT)" stroke-width="4"/>
          <!-- Lateral sinus wall -->
          <path d="M 920 430 C 940 520 920 600 900 630" stroke="url(#boneCT)" stroke-width="8" fill="none"/>
        </g>

        <!-- ================= PATIENT'S RIGHT ORBIT (FRACTURED BLOWOUT SIDE: Viewer's Left) ================= -->
        <g id="fractured_right_orbit">
          <!-- Lateral Orbital Wall / Zygoma -->
          <path d="M 260 230 C 230 320 240 410 270 460" stroke="url(#boneCT)" stroke-width="12" fill="none"/>

          <!-- Orbital Cavity Contents -->
          <ellipse cx="400" cy="320" rx="100" ry="80" fill="url(#fatCT)"/>
          
          <!-- Superior Rectus -->
          <ellipse cx="400" cy="245" rx="30" ry="12" fill="url(#muscleCT)"/>
          <!-- Medial Rectus -->
          <ellipse cx="485" cy="320" rx="14" ry="30" fill="url(#muscleCT)"/>
          <!-- Lateral Rectus -->
          <ellipse cx="315" cy="320" rx="14" ry="30" fill="url(#muscleCT)"/>

          <!-- FRACTURED DISRUPTED ORBITAL FLOOR -->
          <!-- Floor bone is shattered/displaced: broken fragments at (330, 415) and (480, 420) -->
          <line x1="280" y1="415" x2="330" y2="415" stroke="url(#boneCT)" stroke-width="4.5"/>
          <line x1="470" y1="420" x2="520" y2="410" stroke="url(#boneCT)" stroke-width="4.5"/>
          <!-- Depressed bone splinter dangling in defect -->
          <line x1="340" y1="435" x2="375" y2="470" stroke="url(#boneCT)" stroke-width="3.5"/>

          <!-- Right Maxillary Sinus (x=280 to 520, y=430 to 630) -->
          <path d="M 280 430 L 520 430 L 520 630 L 300 630 Z" fill="#000000" stroke="url(#boneCT)" stroke-width="4"/>
          <!-- Lateral sinus wall -->
          <path d="M 280 430 C 260 520 280 600 300 630" stroke="url(#boneCT)" stroke-width="8" fill="none"/>

          <!-- PATHOGNOMONIC "HANGING DROP" / "TEAR DROP" SIGN -->
          <!-- Herniation of orbital fat & Inferior Rectus Muscle complex sagging into the maxillary sinus! -->
          <!-- Smooth rounded dependent herniated mass protruding from y=410 down to y=530 -->
          <path d="M 335 415 
                   C 330 460 340 520 395 530 
                   C 450 530 465 470 470 415 Z" 
                fill="url(#muscleCT)" stroke="#94a3b8" stroke-width="2"/>
          
          <!-- Herniated orbital fat core inside the prolapsed pouch -->
          <ellipse cx="400" cy="460" rx="35" ry="30" fill="url(#fatCT)"/>
          <!-- Entrapped, swollen Inferior Rectus Muscle at the dependent pole (cx=400, cy=495) -->
          <ellipse cx="400" cy="495" rx="32" ry="18" fill="#475569" stroke="#64748b" stroke-width="2"/>

          <!-- Fluid / Blood level in dependent right maxillary sinus (Hemo-antrum at base: y=575 to 630) -->
          <path d="M 285 575 L 515 575 L 515 628 L 295 628 Z" fill="url(#sinusFluid)"/>
          <line x1="285" y1="575" x2="515" y2="575" stroke="#94a3b8" stroke-width="2.5"/>
          <text x="400" y="605" fill="#94a3b8" font-family="sans-serif" font-size="12" font-weight="600" text-anchor="middle">Air-Fluid Level</text>
        </g>
      </g>

      <!-- NEUTRAL QUESTION MARKER POINTER (Slim gold arrow targeting the hanging drop mass) -->
      <g id="neutral_marker">
        <path d="M 190 490 L 290 490 L 375 505" fill="none" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="375,505 360,500 364,512" fill="#f59e0b"/>
        
        <rect x="40" y="465" width="220" height="48" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="150" y="495" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" text-anchor="middle">FRACTURE DEFECT</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/neet2019_q005_orbital_blowout_ct.png")
    res = generate_orbital_blowout_ct(out)
    print("NEET 2019 Q005 Orbital Blowout CT:", res, out.exists())
