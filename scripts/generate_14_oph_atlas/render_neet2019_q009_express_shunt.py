import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_express_glaucoma_shunt(output_path):
    # Medical surgical atlas: Ex-PRESS Miniature Glaucoma Filtration Shunt
    # Detailed 3D anatomical cutaway of limbal angle showing scleral flap dissection,
    # implantation of miniature steel shunt into anterior chamber, and aqueous drainage
    # on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Tissue Gradients -->
        <!-- Cornea Glassy Blue -->
        <linearGradient id="corneaCut" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#bae6fd" stop-opacity="0.9"/>
          <stop offset="50%" stop-color="#7dd3fc" stop-opacity="0.8"/>
          <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.85"/>
        </linearGradient>

        <!-- Sclera Dense Fibrous White/Ivory -->
        <linearGradient id="scleraCut" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#f8fafc"/>
          <stop offset="60%" stop-color="#e2e8f0"/>
          <stop offset="100%" stop-color="#cbd5e1"/>
        </linearGradient>

        <!-- Scleral Flap (Dissected partial-thickness roof) -->
        <linearGradient id="flapCut" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="100%" stop-color="#cbd5e1"/>
        </linearGradient>

        <!-- Iris Brown -->
        <linearGradient id="irisCut" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#78350f"/>
          <stop offset="50%" stop-color="#92400e"/>
          <stop offset="100%" stop-color="#451a03"/>
        </linearGradient>

        <!-- Ciliary Body / Choroid -->
        <linearGradient id="ciliaryCut" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#831843"/>
          <stop offset="100%" stop-color="#500724"/>
        </linearGradient>

        <!-- Stainless Steel Shunt Metallic Gradient -->
        <linearGradient id="steelShunt" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#f8fafc"/>
          <stop offset="30%" stop-color="#94a3b8"/>
          <stop offset="60%" stop-color="#f1f5f9"/>
          <stop offset="85%" stop-color="#64748b"/>
          <stop offset="100%" stop-color="#334155"/>
        </linearGradient>

        <!-- Aqueous Flow Vector Gradient -->
        <linearGradient id="aqueousFlow" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#38bdf8"/>
          <stop offset="100%" stop-color="#0284c7"/>
        </linearGradient>

        <filter id="shuntShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="6" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.8"/>
        </filter>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Header Pill -->
      <g id="header">
        <rect x="340" y="20" width="520" height="42" rx="21" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="600" y="47" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" text-anchor="middle" letter-spacing="1">SURGICAL GLAUCOMA FILTRATION ANATOMY</text>
      </g>

      <!-- MAIN ANATOMICAL CUTAWAY (Centered at cx=580, cy=460) -->
      <g id="anterior_segment_cutaway" filter="url(#shuntShadow)">
        <!-- Anterior Chamber Background (Deep black/blue aqueous space) -->
        <path d="M 300 360 C 450 340 700 360 850 500 L 700 680 C 560 620 400 540 300 360 Z" fill="#030712"/>

        <!-- 1. Ciliary Body & Supraciliary Space (Lower right: x=650 to 950, y=560 to 760) -->
        <path d="M 660 640 C 720 600 800 600 880 620 L 940 720 C 850 720 740 700 660 640 Z" 
              fill="url(#ciliaryCut)" stroke="#500724" stroke-width="2"/>

        <!-- 2. Iris (Extending into anterior chamber towards pupil: x=480 to 700, y=550 to 620) -->
        <path d="M 700 620 C 640 600 580 570 480 550 C 470 545 470 535 480 535 C 570 545 640 570 710 590 Z" 
              fill="url(#irisCut)" stroke="#451a03" stroke-width="2"/>
        <!-- Pupil Aperture label / space at (460, 540) -->
        <text x="440" y="525" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="600">Pupil</text>

        <!-- 3. Scleral Bed (Base of sclera: x=680 to 1050, y=340 to 600) -->
        <path d="M 680 440 C 740 430 840 440 1020 480 L 1020 660 C 880 640 760 620 680 580 Z" 
              fill="url(#scleraCut)" stroke="#94a3b8" stroke-width="2"/>

        <!-- 4. Cornea (Anterior curved dome: x=240 to 650, y=260 to 450) -->
        <path d="M 240 380 C 350 260 520 250 640 320 L 680 430 C 560 380 400 380 280 460 Z" 
              fill="url(#corneaCut)" stroke="#0284c7" stroke-width="2.5"/>
        <text x="380" y="310" fill="#bae6fd" font-family="sans-serif" font-size="15" font-weight="700">Cornea</text>

        <!-- 5. Partial-Thickness Scleral Flap (Dissected roof hinged at limbus: x=640 to 920, y=280 to 410) -->
        <!-- Flap is lifted/elevated slightly to show sub-flap drainage pathway -->
        <path d="M 640 320 C 720 280 820 290 920 330 L 920 370 C 820 340 730 330 670 380 Z" 
              fill="url(#flapCut)" stroke="#64748b" stroke-width="2"/>
        <text x="820" y="275" fill="#f8fafc" font-family="sans-serif" font-size="14" font-weight="700">Scleral Flap (Roof)</text>
        <path d="M 820 285 L 820 320" stroke="#f8fafc" stroke-width="1.5" stroke-dasharray="3,3"/>

        <!-- Subconjunctival Filtering Space / Bleb above flap -->
        <path d="M 620 260 C 750 220 880 230 1000 310" fill="none" stroke="#f43f5e" stroke-width="3" stroke-dasharray="6,4"/>
        <text x="960" y="240" fill="#f43f5e" font-family="sans-serif" font-size="13" font-weight="700">Filtering Bleb</text>

        <!-- ================= THE EX-PRESS® MINI GLAUCOMA SHUNT ================= -->
        <!-- Miniature biocompatible steel tube (~2.64 mm in scale) -->
        <!-- Position: Tube shaft inserted through limbus / trabecular meshwork at (660, 420) -->
        <!-- Distal beveled tip enters anterior chamber at (550, 470) parallel to iris plane -->
        <!-- Proximal retention plate/flange rests in scleral bed at (750, 380) -->
        <g id="express_shunt_device">
          <!-- External Flange / Plate resting in scleral bed at (750, 380) -->
          <ellipse cx="760" cy="380" rx="14" ry="24" transform="rotate(-28, 760, 380)" 
                   fill="url(#steelShunt)" stroke="#1e293b" stroke-width="2"/>
          <ellipse cx="760" cy="380" rx="7" ry="14" transform="rotate(-28, 760, 380)" fill="#0f172a"/>

          <!-- Tube Shaft (Cylindrical titanium/steel tube) -->
          <!-- Runs from (760, 380) down-left to (560, 475) -->
          <path d="M 750 365 L 570 455 L 580 478 L 760 388 Z" 
                fill="url(#steelShunt)" stroke="#1e293b" stroke-width="2"/>

          <!-- Retention Spur / Barb on side of shaft (prevents extrusion) -->
          <polygon points="690,400 705,385 715,410" fill="url(#steelShunt)" stroke="#0f172a" stroke-width="1.5"/>

          <!-- Distal Beveled Intracameral Tip (resting in AC, oriented bevel-up) -->
          <polygon points="570,455 535,472 560,488 580,478" fill="url(#steelShunt)" stroke="#1e293b" stroke-width="2"/>
          <!-- Hollow Lumen Orifice at tip -->
          <ellipse cx="548" cy="475" rx="6" ry="11" transform="rotate(-30, 548, 475)" fill="#020617"/>

          <!-- Metallic Highlight glint along top ridge -->
          <line x1="755" y1="370" x2="550" y2="465" stroke="#ffffff" stroke-width="2.5" opacity="0.9"/>
        </g>

        <!-- Aqueous Humor Drainage Flow Vectors (Cyan animated arrows) -->
        <!-- Flow from Anterior Chamber -> into distal lumen -> out of proximal flange -> under scleral flap -->
        <g stroke="#38bdf8" stroke-width="3" fill="none" stroke-linecap="round">
          <!-- Flow into shunt lumen -->
          <path d="M 480 495 Q 515 485 540 478" marker-end="url(#arrowCyan)"/>
          <!-- Flow out of proximal flange into scleral space -->
          <path d="M 770 380 Q 820 370 860 360"/>
          <path d="M 770 395 Q 830 405 880 410"/>
        </g>
      </g>

      <!-- INSET SCHEMATIC: DEVICE SCHEMATIC (Bottom-left: x=80, y=620) -->
      <g id="device_specs">
        <rect x="60" y="620" width="380" height="230" rx="14" fill="#0b1329" stroke="#334155" stroke-width="2"/>
        <text x="250" y="655" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="800" text-anchor="middle">IMPLANT SPECIFICATIONS</text>
        <g fill="#cbd5e1" font-family="sans-serif" font-size="13" font-weight="500">
          <text x="85" y="692">• Biocompatible 316L Stainless Steel</text>
          <text x="85" y="722">• Length: ~2.64 mm, External Ø: 400 µm</text>
          <text x="85" y="752">• Beveled tip placed parallel to iris plane</text>
          <text x="85" y="782">• Retention spur prevents dislodgement</text>
          <text x="85" y="812">• Diverts aqueous under partial-thickness flap</text>
        </g>
      </g>

      <!-- NEUTRAL QUESTION MARKER POINTER (Slim gold arrow targeting the implant) -->
      <g id="neutral_marker">
        <path d="M 680 160 L 680 320 L 670 390" fill="none" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="670,390 662,376 675,374" fill="#f59e0b"/>
        
        <rect x="560" y="115" width="240" height="48" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="680" y="145" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" text-anchor="middle">DRAINAGE DEVICE</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/neet2019_q009_express_shunt.png")
    res = generate_express_glaucoma_shunt(out)
    print("NEET 2019 Q009 Ex-PRESS Shunt:", res, out.exists())
