import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_choroidal_melanoma(output_path):
    # Medical atlas illustration of Posterior Pole Fundus showing Choroidal Melanoma
    # Large elevated pigmented dome-shaped mass in superotemporal fundus with orange lipofuscin clumps
    # and serous retinal detachment, on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Retinal Background Gradient (Warm orange-red tigroid fundus) -->
        <radialGradient id="fundusGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#ea580c"/>
          <stop offset="50%" stop-color="#c2410c"/>
          <stop offset="85%" stop-color="#9a3412"/>
          <stop offset="100%" stop-color="#431407"/>
        </radialGradient>

        <!-- Optic Disc Gradient -->
        <radialGradient id="discGrad" cx="42%" cy="46%" r="54%">
          <stop offset="0%" stop-color="#fef08a"/>
          <stop offset="45%" stop-color="#fde047"/>
          <stop offset="75%" stop-color="#f59e0b"/>
          <stop offset="100%" stop-color="#b45309"/>
        </radialGradient>

        <!-- Choroidal Melanoma Mass Gradient (Elevated dark brown/slate-gray tumor) -->
        <radialGradient id="melanomaMass" cx="45%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#44403c"/>
          <stop offset="35%" stop-color="#292524"/>
          <stop offset="75%" stop-color="#1c1917"/>
          <stop offset="100%" stop-color="#0c0a09"/>
        </radialGradient>

        <!-- Orange Pigment Clumps (Lipofuscin) -->
        <radialGradient id="lipofuscinGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#fb923c"/>
          <stop offset="60%" stop-color="#ea580c"/>
          <stop offset="100%" stop-color="#c2410c" stop-opacity="0"/>
        </radialGradient>

        <!-- Overlying Serous Subretinal Fluid Sheen -->
        <linearGradient id="fluidSheen" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.35"/>
          <stop offset="50%" stop-color="#fdba74" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0"/>
        </linearGradient>

        <!-- Filter for 3D elevation depth -->
        <filter id="tumorElevation" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="-10" dy="-10" stdDeviation="15" flood-color="#000000" flood-opacity="0.8"/>
        </filter>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Funduscopic Circular Field of View (Diameter 800px, cx=600, cy=450) -->
      <g id="fundus_field">
        <circle cx="600" cy="450" r="410" fill="url(#fundusGrad)" stroke="#1e293b" stroke-width="4"/>
        
        <!-- Subtle choroidal tessellation / tigroid background texture -->
        <g stroke="#7c2d12" stroke-width="2.5" opacity="0.3" stroke-linecap="round">
          <path d="M 280 400 Q 380 420 500 410" fill="none"/>
          <path d="M 310 500 Q 420 510 540 480" fill="none"/>
          <path d="M 300 600 Q 440 610 580 570" fill="none"/>
          <path d="M 640 620 Q 760 630 880 590" fill="none"/>
        </g>
      </g>

      <!-- Anatomical Landmarks -->
      <!-- Optic Disc at cx=440, cy=460 (Right Fundus: Disc is nasal = left) -->
      <g id="optic_disc">
        <ellipse cx="440" cy="460" rx="36" ry="44" fill="url(#discGrad)" stroke="#78350f" stroke-width="2"/>
        <!-- Physiological Cup -->
        <ellipse cx="436" cy="458" rx="16" ry="20" fill="#ffffff" opacity="0.85"/>
        <!-- Scleral crescent / pigment ring margin -->
        <path d="M 466 430 C 478 450 478 475 466 495" fill="none" stroke="#451a03" stroke-width="3"/>
      </g>

      <!-- Fovea / Macula at cx=620, cy=475 (Temporal to optic disc) -->
      <g id="fovea_macula">
        <circle cx="620" cy="475" r="45" fill="#9a3412" opacity="0.6"/>
        <!-- Foveal light reflex -->
        <circle cx="620" cy="475" r="6" fill="#7c2d12"/>
        <circle cx="619" cy="474" r="1.5" fill="#fef08a"/>
      </g>

      <!-- CHOROIDAL MELANOMA TUMOR MASS (Superotemporal Quadrant: cx=720, cy=310) -->
      <g id="choroidal_melanoma_mass" filter="url(#tumorElevation)">
        <!-- Tumor Dome Base -->
        <path d="M 570 330 
                 C 550 240 620 140 730 130 
                 C 840 120 940 190 950 290 
                 C 960 380 910 460 820 480 
                 C 720 500 610 450 570 330 Z" 
              fill="url(#melanomaMass)" stroke="#0c0a09" stroke-width="2"/>

        <!-- 3D Contour Shading rings showing steep elevated dome -->
        <path d="M 610 320 C 600 250 650 180 740 170 C 820 160 900 210 910 290 C 915 360 870 420 800 435 C 720 450 630 400 610 320 Z" 
              fill="#292524" opacity="0.7"/>

        <!-- Overlying Serous Retinal Detachment / Fluid Sheen -->
        <path d="M 570 330 C 550 240 620 140 730 130 C 840 120 940 190 950 290 C 880 340 750 380 570 330 Z" 
              fill="url(#fluidSheen)"/>

        <!-- Lipofuscin Orange Pigment Clumps (Pathognomonic hallmark) -->
        <g id="lipofuscin_clumps">
          <ellipse cx="680" cy="240" rx="22" ry="14" fill="url(#lipofuscinGlow)"/>
          <ellipse cx="740" cy="210" rx="30" ry="18" fill="url(#lipofuscinGlow)"/>
          <ellipse cx="800" cy="260" rx="25" ry="15" fill="url(#lipofuscinGlow)"/>
          <ellipse cx="760" cy="300" rx="35" ry="20" fill="url(#lipofuscinGlow)"/>
          <ellipse cx="700" cy="320" rx="28" ry="16" fill="url(#lipofuscinGlow)"/>
          <ellipse cx="840" cy="320" rx="20" ry="12" fill="url(#lipofuscinGlow)"/>
          <ellipse cx="790" cy="370" rx="32" ry="18" fill="url(#lipofuscinGlow)"/>
          <circle cx="730" cy="260" r="10" fill="#f97316"/>
          <circle cx="810" cy="290" r="8" fill="#f97316"/>
          <circle cx="770" cy="340" r="12" fill="#f97316"/>
        </g>
      </g>

      <!-- Retinal Vascular Arcades -->
      <!-- Vessels emerging from Optic Disc (440, 460) -->
      <g id="retinal_vessels" fill="none" stroke-linecap="round">
        <!-- Superior Temporal Arcade arching over and around the tumor -->
        <path d="M 440 450 C 470 380 530 290 620 230 C 700 180 820 160 920 170" stroke="#b91c1c" stroke-width="7"/>
        <path d="M 442 452 C 472 382 532 292 622 232 C 702 182 822 162 922 172" stroke="#dc2626" stroke-width="3"/>

        <!-- Superior Temporal Vein (darker, wider) -->
        <path d="M 436 450 C 460 370 510 270 590 200 C 680 150 800 130 900 140" stroke="#7f1d1d" stroke-width="9"/>

        <!-- Branches climbing over tumor surface (Intrinsic draping) -->
        <path d="M 620 230 C 670 260 740 280 820 290" stroke="#dc2626" stroke-width="3"/>
        <path d="M 700 180 C 730 220 780 250 840 260" stroke="#dc2626" stroke-width="2.5"/>

        <!-- Inferior Temporal Arcade -->
        <path d="M 440 470 C 470 550 540 640 650 690 C 760 730 880 720 950 670" stroke="#b91c1c" stroke-width="7"/>
        <path d="M 436 470 C 460 560 520 660 630 710 C 740 750 860 740 940 690" stroke="#7f1d1d" stroke-width="9"/>

        <!-- Nasal Vessels (heading to left border) -->
        <path d="M 430 450 C 390 400 340 360 260 340" stroke="#b91c1c" stroke-width="5"/>
        <path d="M 430 470 C 390 520 340 560 260 580" stroke="#b91c1c" stroke-width="5"/>
      </g>

      <!-- NEUTRAL QUESTION MARKER (Slim gold pointer directed at the choroidal mass) -->
      <g id="neutral_marker">
        <path d="M 1040 260 L 880 260 L 820 280" fill="none" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="820,280 835,274 832,286" fill="#f59e0b"/>
        
        <rect x="960" y="235" width="180" height="48" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="1050" y="265" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" text-anchor="middle">FUNDUS LESION</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/q001_choroidal_melanoma.png")
    res = generate_choroidal_melanoma(out)
    print("Q001 Choroidal Melanoma:", res, out.exists())
