import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_hypopyon_endophthalmitis(output_path):
    # Medical atlas illustration of anterior segment in Acute Post-Cataract Endophthalmitis
    # featuring intense ciliary injection, corneal haze, surgical incision, and layered Hypopyon
    # on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Scleral / Conjunctival Redness Gradients -->
        <radialGradient id="scleraFlush" cx="50%" cy="50%" r="50%">
          <stop offset="65%" stop-color="#fff5f5"/>
          <stop offset="85%" stop-color="#fca5a5"/>
          <stop offset="95%" stop-color="#ef4444"/>
          <stop offset="100%" stop-color="#991b1b"/>
        </radialGradient>
        
        <!-- Cornea Transparency / Edema -->
        <radialGradient id="corneaHaze" cx="48%" cy="46%" r="52%">
          <stop offset="0%" stop-color="#e0f2fe" stop-opacity="0.35"/>
          <stop offset="70%" stop-color="#bae6fd" stop-opacity="0.45"/>
          <stop offset="90%" stop-color="#7dd3fc" stop-opacity="0.6"/>
          <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.75"/>
        </radialGradient>
        
        <!-- Iris Texture / Color (Hazel Brown) -->
        <radialGradient id="irisGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#2a1810"/>
          <stop offset="35%" stop-color="#5c3822"/>
          <stop offset="75%" stop-color="#805030"/>
          <stop offset="100%" stop-color="#361f12"/>
        </radialGradient>
        
        <!-- Slit Beam Illumination Effect -->
        <linearGradient id="slitBeam" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8"/>
          <stop offset="50%" stop-color="#e0f2fe" stop-opacity="0.4"/>
          <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0"/>
        </linearGradient>

        <!-- Hypopyon Fluid Layer Gradient (Purulent white-yellow sterile exudate) -->
        <linearGradient id="hypopyonFill" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#fef9c3" stop-opacity="0.95"/>
          <stop offset="25%" stop-color="#fef08a"/>
          <stop offset="100%" stop-color="#eab308"/>
        </linearGradient>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Main Ocular Aperture (Eyelids framing the eye) -->
      <g id="eyelids_and_periorbita">
        <!-- Surrounding Skin -->
        <path d="M 120 450 C 120 220 380 140 600 140 C 820 140 1080 220 1080 450 C 1080 680 820 760 600 760 C 380 760 120 680 120 450 Z" 
              fill="#c29170" stroke="#8c5838" stroke-width="3"/>
        
        <!-- Palpebral Fissure Opening -->
        <path d="M 160 450 C 260 270 500 230 600 230 C 700 230 940 270 1040 450 C 940 630 700 670 600 670 C 500 670 260 630 160 450 Z" 
              fill="#fee2e2" id="palpebral_cut"/>
      </g>

      <!-- Bulbar Conjunctiva & Sclera with Ciliary Injection -->
      <g id="sclera_and_injection">
        <!-- Bulbar Sclera base -->
        <path d="M 160 450 C 260 270 500 230 600 230 C 700 230 940 270 1040 450 C 940 630 700 670 600 670 C 500 670 260 630 160 450 Z" 
              fill="url(#scleraFlush)"/>

        <!-- Engorged Ciliary & Conjunctival Blood Vessels (Perilimbal ciliary flush) -->
        <!-- Radially penetrating violaceous vessels towards cornea -->
        <g stroke="#b91c1c" stroke-linecap="round" opacity="0.85">
          <!-- Nasal Vessels -->
          <path d="M 180 440 Q 280 435 370 445" stroke-width="4.5" fill="none"/>
          <path d="M 200 410 Q 290 415 365 430" stroke-width="3.5" fill="none"/>
          <path d="M 210 470 Q 290 460 365 455" stroke-width="3.5" fill="none"/>
          <path d="M 240 370 Q 320 390 380 410" stroke-width="3" fill="none"/>
          <path d="M 240 530 Q 320 510 380 480" stroke-width="3" fill="none"/>

          <!-- Temporal Vessels -->
          <path d="M 1020 440 Q 920 435 830 445" stroke-width="4.5" fill="none"/>
          <path d="M 1000 410 Q 910 415 835 430" stroke-width="3.5" fill="none"/>
          <path d="M 990 470 Q 910 460 835 455" stroke-width="3.5" fill="none"/>
          <path d="M 960 370 Q 880 390 820 410" stroke-width="3" fill="none"/>
          <path d="M 960 530 Q 880 510 820 480" stroke-width="3" fill="none"/>

          <!-- Fine perilimbal ciliary flush ring -->
          <circle cx="600" cy="450" r="235" stroke="#dc2626" stroke-width="6" fill="none" opacity="0.6"/>
          <circle cx="600" cy="450" r="242" stroke="#991b1b" stroke-width="3" fill="none" opacity="0.5"/>
        </g>
      </g>

      <!-- Cornea / Limbus / Iris / Anterior Chamber Structure -->
      <!-- Center at cx=600, cy=450, Limbus radius = 220 -->
      <g id="cornea_and_anterior_segment">
        <!-- Corneal Limbus outline -->
        <circle cx="600" cy="450" r="220" fill="#1e293b" stroke="#7f1d1d" stroke-width="4"/>

        <!-- Iris -->
        <circle cx="600" cy="450" r="216" fill="url(#irisGrad)"/>
        <!-- Radial Iris crypts / trabeculae -->
        <g stroke="#3e2314" stroke-width="2" opacity="0.7">
          <line x1="600" y1="235" x2="600" y2="350"/>
          <line x1="600" y1="665" x2="600" y2="550"/>
          <line x1="385" y1="450" x2="500" y2="450"/>
          <line x1="815" y1="450" x2="700" y2="450"/>
          <line x1="450" y1="300" x2="530" y2="380"/>
          <line x1="750" y1="300" x2="670" y2="380"/>
          <line x1="450" y1="600" x2="530" y2="520"/>
          <line x1="750" y1="600" x2="670" y2="520"/>
        </g>

        <!-- Pupil & Pseudophakic Intraocular Lens (IOL) -->
        <!-- Pupil slightly sluggish/mid-dilated r=70 -->
        <circle cx="600" cy="450" r="72" fill="#0a0a0a" stroke="#451a03" stroke-width="3"/>
        
        <!-- IOL Optic Edge Reflex (Square-edge hydrophobic acrylic IOL reflex) -->
        <circle cx="600" cy="450" r="85" fill="none" stroke="#38bdf8" stroke-width="1.5" opacity="0.6"/>
        <path d="M 545 405 C 570 395 630 395 655 405" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.8"/>
        <!-- Inflammatory fibrin exudate strand in pupil -->
        <path d="M 560 430 Q 600 445 640 435" stroke="#fef08a" stroke-width="3" fill="none" opacity="0.85"/>

        <!-- Post-Cataract Clear-Corneal Incision Site (Superior Limbus at 11-12 o'clock) -->
        <g id="surgical_incision">
          <path d="M 540 236 C 570 230 630 230 660 236" fill="none" stroke="#ffffff" stroke-width="4"/>
          <path d="M 540 236 C 570 230 630 230 660 236" fill="none" stroke="#0284c7" stroke-width="2" stroke-dasharray="8,6"/>
          <!-- Incision hydration edema halo -->
          <ellipse cx="600" cy="242" rx="65" ry="16" fill="#bae6fd" opacity="0.4"/>
        </g>

        <!-- HYPOPYON (Layered purulent exudate in inferior anterior chamber) -->
        <!-- Horizontal fluid level in inferior angle between y=540 and y=665 -->
        <g id="hypopyon">
          <!-- Fluid-level horizontal meniscus -->
          <clipPath id="inferiorAngleClip">
            <circle cx="600" cy="450" r="216"/>
          </clipPath>
          
          <g clip-path="url(#inferiorAngleClip)">
            <!-- Layered purulent sediment (Hypopyon) -->
            <!-- Straight horizontal upper boundary at y=540 -->
            <path d="M 380 540 L 820 540 L 820 680 L 380 680 Z" fill="url(#hypopyonFill)"/>
            <!-- Meniscus highlight line -->
            <line x1="430" y1="540" x2="770" y2="540" stroke="#fefce8" stroke-width="3.5"/>
            <!-- Secondary purulent density gradation -->
            <path d="M 400 580 L 800 580 L 800 680 L 400 680 Z" fill="#ca8a04" opacity="0.45"/>
          </g>
        </g>

        <!-- Corneal Edema / Steamy Haze Overly -->
        <circle cx="600" cy="450" r="220" fill="url(#corneaHaze)"/>

        <!-- Slit-Lamp Optical Beam (Oblique slit beam highlighting cornea & AC flare) -->
        <path d="M 460 240 L 520 240 L 640 660 L 580 660 Z" fill="url(#slitBeam)" opacity="0.6"/>
        <path d="M 480 240 L 510 240 L 620 660 L 590 660 Z" fill="#ffffff" opacity="0.5"/>
      </g>

      <!-- Eyelashes & Upper/Lower Lid Margins -->
      <path d="M 160 450 C 260 270 500 230 600 230 C 700 230 940 270 1040 450" fill="none" stroke="#451a03" stroke-width="6"/>
      <path d="M 160 450 C 260 630 500 670 600 670 C 700 670 940 630 1040 450" fill="none" stroke="#451a03" stroke-width="4"/>

      <!-- NEUTRAL MARKER POINTER (Clean slim gold arrow pointing to the Hypopyon level) -->
      <g id="neutral_marker">
        <!-- Pointer line to Hypopyon at (600, 560) -->
        <path d="M 980 680 L 820 620 L 740 570" fill="none" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="740,570 755,572 748,582" fill="#f59e0b"/>
        
        <!-- Marker label pill -->
        <rect x="880" y="655" width="260" height="48" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="1010" y="685" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" text-anchor="middle">ANTERIOR CHAMBER</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/neet2018_q007_hypopyon.png")
    res = generate_hypopyon_endophthalmitis(out)
    print("NEET 2018 Q007 Hypopyon:", res, out.exists())
