import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_ffa_macular_ischemia(output_path):
    # Medical angiographic atlas: Fundus Fluorescein Angiography (FFA) in Diabetic Macular Ischemia
    # High-contrast fluorescein angiogram of the central macula showing pathologically enlarged FAZ,
    # capillary drop-out / non-perfusion, and microaneurysms on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Fluorescein Background Glow -->
        <radialGradient id="ffaChoroid" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#334155"/>
          <stop offset="45%" stop-color="#1e293b"/>
          <stop offset="80%" stop-color="#0f172a"/>
          <stop offset="100%" stop-color="#020617"/>
        </radialGradient>

        <!-- Hyperfluorescent vessel glow filter -->
        <filter id="vesselGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="1.5" result="blur"/>
          <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>

        <!-- Enlarged FAZ Ischemia Gradient (Hypofluorescent central void) -->
        <radialGradient id="fazIschemia" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#000000"/>
          <stop offset="65%" stop-color="#020617"/>
          <stop offset="85%" stop-color="#0f172a" stop-opacity="0.8"/>
          <stop offset="100%" stop-color="#1e293b" stop-opacity="0"/>
        </radialGradient>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Circular FFA Angiographic Field (Diameter 800px, centered at cx=600, cy=450) -->
      <g id="ffa_field">
        <circle cx="600" cy="450" r="410" fill="url(#ffaChoroid)" stroke="#334155" stroke-width="4"/>

        <!-- Diffuse background choroidal flush with micro-speckle texture -->
        <circle cx="600" cy="450" r="400" fill="#1e293b" opacity="0.4"/>
      </g>

      <!-- RETINAL VASCULAR NETWORK (MACULAR ARCADES & PERIFOVEAL VESSELS) -->
      <g id="retinal_vessels" filter="url(#vesselGlow)">
        <!-- Superior Major Arcade Vessels arching across top -->
        <g stroke="#ffffff" fill="none" stroke-linecap="round">
          <!-- Superior Artery & Vein -->
          <path d="M 280 200 C 400 160 550 140 700 150 C 850 170 960 220 1020 280" stroke-width="9"/>
          <path d="M 290 220 C 410 180 560 160 710 170 C 840 190 940 240 1000 300" stroke-width="5" stroke="#cbd5e1"/>

          <!-- Inferior Major Arcade Vessels arching across bottom -->
          <path d="M 280 700 C 400 740 550 760 700 750 C 850 730 960 680 1020 620" stroke-width="9"/>
          <path d="M 290 680 C 410 720 560 740 710 730 C 840 710 940 660 1000 600" stroke-width="5" stroke="#cbd5e1"/>

          <!-- Secondary Branches descending into parafovea -->
          <!-- Superior descending branches -->
          <path d="M 450 180 C 470 240 480 300 480 360" stroke-width="4.5"/>
          <path d="M 550 160 C 560 230 580 300 570 350" stroke-width="4"/>
          <path d="M 660 160 C 670 220 660 280 670 340" stroke-width="4"/>
          <path d="M 780 180 C 770 240 750 300 730 350" stroke-width="4.5"/>
          <path d="M 880 210 C 850 270 820 330 790 380" stroke-width="4"/>

          <!-- Inferior ascending branches -->
          <path d="M 450 720 C 470 660 480 600 480 540" stroke-width="4.5"/>
          <path d="M 550 740 C 560 670 580 600 570 550" stroke-width="4"/>
          <path d="M 660 740 C 670 680 660 620 670 560" stroke-width="4"/>
          <path d="M 780 720 C 770 660 750 600 730 550" stroke-width="4.5"/>
          <path d="M 880 690 C 850 630 820 570 790 520" stroke-width="4"/>

          <!-- Temporal & Nasal horizontal feeding branches -->
          <path d="M 330 400 C 380 410 430 420 470 430" stroke-width="3.5"/>
          <path d="M 330 500 C 380 490 430 480 470 470" stroke-width="3.5"/>
          <path d="M 920 400 C 870 410 820 420 780 430" stroke-width="3.5"/>
          <path d="M 920 500 C 870 490 820 480 780 470" stroke-width="3.5"/>
        </g>
      </g>

      <!-- PATHOLOGICAL CAPILLARY DROPOUT & ENLARGED FOVEAL AVASCULAR ZONE (FAZ) -->
      <!-- Normal FAZ is ~500µm; here it is enlarged to >1500µm with ragged, blunted borders -->
      <g id="enlarged_faz_and_dropout">
        <!-- Huge dark hypofluorescent core at center (cx=610, cy=450) -->
        <path d="M 520 430 
                 C 510 380 550 340 600 330 
                 C 660 320 710 350 720 390 
                 C 740 430 730 480 700 510 
                 C 670 550 610 570 560 550 
                 C 520 530 510 480 520 430 Z" 
              fill="url(#fazIschemia)" stroke="#090d16" stroke-width="3"/>

        <!-- Pruned, truncated capillary terminals ending abruptly around the margin -->
        <g stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" opacity="0.9">
          <!-- Abruptly ending capillaries with dilated bulbous ends -->
          <line x1="480" y1="360" x2="520" y2="390"/>
          <circle cx="520" cy="390" r="3" fill="#ffffff"/>

          <line x1="570" y1="350" x2="580" y2="340"/>
          <circle cx="580" cy="340" r="3" fill="#ffffff"/>

          <line x1="670" y1="340" x2="685" y2="355"/>
          <circle cx="685" cy="355" r="3" fill="#ffffff"/>

          <line x1="730" y1="350" x2="720" y2="390"/>
          <circle cx="720" cy="390" r="3" fill="#ffffff"/>

          <line x1="780" y1="430" x2="735" y2="445"/>
          <circle cx="735" cy="445" r="3" fill="#ffffff"/>

          <line x1="780" y1="470" x2="725" y2="480"/>
          <circle cx="725" cy="480" r="3" fill="#ffffff"/>

          <line x1="730" y1="550" x2="695" y2="525"/>
          <circle cx="695" cy="525" r="3" fill="#ffffff"/>

          <line x1="570" y1="550" x2="575" y2="540"/>
          <circle cx="575" cy="540" r="3" fill="#ffffff"/>

          <line x1="480" y1="540" x2="530" y2="515"/>
          <circle cx="530" cy="515" r="3" fill="#ffffff"/>
        </g>

        <!-- Capillary Non-Perfusion Area (Dark avascular triangle between 7 o'clock and 9 o'clock) -->
        <path d="M 370 440 C 430 420 480 440 480 520 C 430 550 380 520 370 440 Z" fill="#030712" stroke="#0f172a" stroke-width="2"/>

        <!-- Microaneurysms (Hyperfluorescent pinpoint dots) -->
        <g fill="#ffffff" filter="url(#vesselGlow)">
          <circle cx="490" cy="320" r="3"/>
          <circle cx="510" cy="340" r="2.5"/>
          <circle cx="460" cy="370" r="3.2"/>
          <circle cx="640" cy="310" r="2.8"/>
          <circle cx="710" cy="320" r="3.5"/>
          <circle cx="760" cy="370" r="2.5"/>
          <circle cx="790" cy="410" r="3"/>
          <circle cx="810" cy="460" r="3.2"/>
          <circle cx="760" cy="510" r="2.8"/>
          <circle cx="710" cy="570" r="3"/>
          <circle cx="640" cy="580" r="2.5"/>
          <circle cx="520" cy="580" r="3.5"/>
          <circle cx="440" cy="480" r="2.8"/>
          <circle cx="410" cy="430" r="3.2"/>
        </g>
      </g>

      <!-- TWO EXACT NEUTRAL QUESTION MARKERS (Faithful to question stem & explanation) -->
      <!-- Marker 1: ARROW A (Targeting Enlarged FAZ at cx=610, cy=450) -->
      <g id="marker_arrow_a">
        <!-- Slim gold arrow shaft & arrowhead -->
        <path d="M 800 240 L 690 330 L 635 390" fill="none" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="635,390 650,382 642,395" fill="#f59e0b"/>
        
        <rect x="760" y="200" width="230" height="46" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="875" y="229" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" text-anchor="middle">ENLARGED FAZ</text>
      </g>

      <!-- Marker 2: ARROW B (Targeting Capillary Non-Perfusion Area at cx=420, cy=480) -->
      <g id="marker_arrow_b">
        <!-- Slim cyan arrow shaft & arrowhead -->
        <path d="M 220 620 L 330 560 L 395 500" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <polygon points="395,500 382,508 388,495" fill="#38bdf8"/>

        <rect x="90" y="605" width="250" height="46" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="215" y="634" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" text-anchor="middle">NON-PERFUSION AREA</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/q009_ffa_macular_ischemia.png")
    res = generate_ffa_macular_ischemia(out)
    print("Q009 FFA Macular Ischemia:", res, out.exists())
