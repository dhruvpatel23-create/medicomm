import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_anterior_ethmoidal_block(output_path):
    # Medical atlas illustration: Anterior Ethmoidal Nerve Block
    # Anatomical technique showing syringe needle insertion at medial orbital wall
    # 1 cm above medial canthal ligament directed along the fronto-ethmoidal suture
    # on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Skin / Facial Shading -->
        <radialGradient id="faceTone" cx="50%" cy="50%" r="55%">
          <stop offset="0%" stop-color="#fed7aa"/>
          <stop offset="60%" stop-color="#fdba74"/>
          <stop offset="100%" stop-color="#c2410c" stop-opacity="0.6"/>
        </radialGradient>

        <!-- Bone Ivory Gradient (Medial orbital wall cutaway) -->
        <linearGradient id="boneGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fef3c7"/>
          <stop offset="50%" stop-color="#fde68a"/>
          <stop offset="100%" stop-color="#d97706"/>
        </linearGradient>

        <!-- Syringe Glass & Metal Gradients -->
        <linearGradient id="syringeGlass" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8"/>
          <stop offset="30%" stop-color="#e0f2fe" stop-opacity="0.5"/>
          <stop offset="70%" stop-color="#bae6fd" stop-opacity="0.6"/>
          <stop offset="100%" stop-color="#ffffff" stop-opacity="0.8"/>
        </linearGradient>
        <linearGradient id="needleSteel" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#f8fafc"/>
          <stop offset="50%" stop-color="#94a3b8"/>
          <stop offset="100%" stop-color="#475569"/>
        </linearGradient>

        <!-- Anesthetic Fluid Blue Gradient -->
        <linearGradient id="localAnesthetic" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.7"/>
          <stop offset="100%" stop-color="#0284c7" stop-opacity="0.7"/>
        </linearGradient>

        <filter id="shadow3D" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="8" dy="12" stdDeviation="15" flood-color="#000000" flood-opacity="0.8"/>
        </filter>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Header Pill -->
      <g id="header">
        <rect x="330" y="20" width="540" height="42" rx="21" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="600" y="47" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" text-anchor="middle" letter-spacing="1">REGIONAL OPHTHALMIC ANESTHESIA TECHNIQUE</text>
      </g>

      <!-- MAIN ANATOMICAL FIELD (Right eye / medial orbit view: centered at cx=500, cy=460) -->
      <g id="anatomical_head_cutaway" filter="url(#shadow3D)">
        <!-- Cranial / Orbital Base -->
        <!-- Nasal root / bridge (left side, x=240 to 340) -->
        <path d="M 280 180 C 290 280 300 360 280 440 C 260 520 230 600 210 680 L 380 720 C 420 620 440 540 440 460 C 440 380 420 260 380 180 Z" 
              fill="#e2ba99" stroke="#b08060" stroke-width="2"/>

        <!-- Orbit & Globe Profile (Right Eye) -->
        <!-- Medial Canthus at (410, 460) -->
        <!-- Eyebrow / Supraorbital Ridge (y=240 to 260) -->
        <path d="M 330 240 Q 480 200 640 230 Q 720 250 800 300" stroke="#4a3020" stroke-width="16" stroke-linecap="round" fill="none"/>
        
        <!-- Upper Eyelid -->
        <path d="M 410 460 C 480 340 660 340 730 460" fill="none" stroke="#b08060" stroke-width="4"/>
        <path d="M 410 460 C 480 360 660 360 730 460 C 660 540 480 540 410 460 Z" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>

        <!-- Cornea & Iris (Looking straight) -->
        <ellipse cx="580" cy="455" rx="55" ry="50" fill="#3b2d1d" stroke="#1c1917" stroke-width="2"/>
        <circle cx="580" cy="455" r="20" fill="#000000"/>
        <circle cx="574" cy="450" r="6" fill="#ffffff"/>

        <!-- Lower Eyelid -->
        <path d="M 410 460 C 480 540 660 540 730 460" fill="none" stroke="#b08060" stroke-width="3"/>

        <!-- Medial Canthal Tendon (Ligament) Landmark -->
        <!-- Extends horizontally from medial canthus to anterior lacrimal crest -->
        <path d="M 370 460 L 415 460" stroke="#f1f5f9" stroke-width="7" stroke-linecap="round"/>
        <text x="360" y="490" fill="#cbd5e1" font-family="sans-serif" font-size="12" font-weight="600">Medial Canthal Tendon</text>

        <!-- Medial Orbital Wall Cutaway (Bone layer: Ethmoid lamina papyracea & Frontal bone) -->
        <path d="M 350 280 C 370 340 375 400 365 460 L 340 460 C 350 400 345 340 330 280 Z" 
              fill="url(#boneGrad)" stroke="#b45309" stroke-width="1.5"/>

        <!-- Anterior Ethmoidal Foramen Location (Deep along medial roof junction) -->
        <circle cx="360" cy="340" r="6" fill="#000000" stroke="#f59e0b" stroke-width="2"/>
        <text x="230" y="345" fill="#f59e0b" font-family="sans-serif" font-size="12" font-weight="700">Ant. Ethmoidal Foramen</text>
        <line x1="315" y1="340" x2="350" y2="340" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3,3"/>

        <!-- Exact Injection Site Landmark: 1 cm above medial canthus and slightly posterior -->
        <!-- Needle Entry Point at (385, 390) -->
        <circle cx="385" cy="390" r="7" fill="#ef4444" stroke="#ffffff" stroke-width="2"/>
        <text x="430" y="380" fill="#ef4444" font-family="sans-serif" font-size="13" font-weight="800">1 cm Above Medial Canthus</text>
        <line x1="420" y1="382" x2="395" y2="388" stroke="#ef4444" stroke-width="1.5"/>
      </g>

      <!-- LOCAL ANESTHETIC SYRINGE & NEEDLE APPARATUS -->
      <!-- Positioned entering medial orbit at (385, 390) directed posteriorly towards (360, 340) -->
      <g id="syringe_apparatus" filter="url(#shadow3D)">
        <!-- Needle Shaft (25G, 3.5 cm long, angled into medial orbital wall) -->
        <!-- From Syringe Hub (520, 520) to Entry Point (385, 390) and continuing into tissue to (360, 340) -->
        <!-- Deep tissue segment (dashed line) -->
        <line x1="385" y1="390" x2="360" y2="340" stroke="#38bdf8" stroke-width="3" stroke-dasharray="4,3"/>
        
        <!-- External needle shaft -->
        <line x1="520" y1="520" x2="385" y2="390" stroke="url(#needleSteel)" stroke-width="4.5"/>
        <line x1="520" y1="520" x2="385" y2="390" stroke="#ffffff" stroke-width="1.5"/>

        <!-- Luer-Lock Needle Hub at (520, 520) -->
        <g transform="translate(520, 520) rotate(44)">
          <rect x="-10" y="-12" width="20" height="24" rx="3" fill="#64748b" stroke="#334155" stroke-width="1.5"/>

          <!-- Syringe Barrel (3 ml / 5 ml medical syringe) -->
          <!-- Barrel Dimensions: width=40, length=240 -->
          <!-- Glass / Polypropylene cylinder -->
          <rect x="-20" y="12" width="40" height="220" rx="6" fill="url(#syringeGlass)" stroke="#38bdf8" stroke-width="2"/>

          <!-- Local Anesthetic Liquid Column -->
          <rect x="-18" y="70" width="36" height="158" fill="url(#localAnesthetic)"/>

          <!-- Syringe Plunger & Rubber Stopper -->
          <!-- Rubber Piston at y=70 -->
          <rect x="-19" y="55" width="38" height="18" rx="3" fill="#1e293b" stroke="#0f172a" stroke-width="1"/>
          <!-- Plunger Shaft -->
          <rect x="-6" y="-80" width="12" height="135" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5"/>
          <!-- Plunger Thumb Flange -->
          <ellipse cx="0" cy="-80" rx="25" ry="8" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>

          <!-- Graduation Marks (ml calibration lines) -->
          <g stroke="#ffffff" stroke-width="1.5" opacity="0.8">
            <line x1="-18" y1="80" x2="-8" y2="80"/>
            <line x1="-18" y1="110" x2="-2" y2="110"/>
            <line x1="-18" y1="140" x2="-8" y2="140"/>
            <line x1="-18" y1="170" x2="-2" y2="170"/>
            <line x1="-18" y1="200" x2="-8" y2="200"/>
          </g>

          <!-- Syringe Finger Flanges at base -->
          <path d="M -40 230 L 40 230" stroke="#cbd5e1" stroke-width="8" stroke-linecap="round"/>
        </g>
      </g>

      <!-- INSET PROCEDURE INFO / ANATOMICAL EXPLANATION BOX (Right side: x=780, y=560) -->
      <g id="procedure_guide">
        <rect x="760" y="580" width="400" height="240" rx="14" fill="#0b1329" stroke="#334155" stroke-width="2"/>
        <text x="960" y="618" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">ANATOMICAL LANDMARKS</text>
        
        <g fill="#cbd5e1" font-family="sans-serif" font-size="13" font-weight="500">
          <text x="790" y="655">• Insertion point: 1 cm above medial canthus</text>
          <text x="790" y="685">• 0.5 cm posterior to anterior lacrimal crest</text>
          <text x="790" y="715">• Trajectory: Hugs medial orbital wall periosteum</text>
          <text x="790" y="745">• Depth: ~2.5 - 3.0 cm towards foramen</text>
          <text x="790" y="775">• Anesthetizes: Roof of nasal cavity &amp; ethmoids</text>
        </g>
      </g>

      <!-- NEUTRAL QUESTION MARKER POINTER -->
      <g id="neutral_marker">
        <path d="M 220 220 L 310 220 L 370 370" fill="none" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="370,370 358,360 370,355" fill="#f59e0b"/>
        
        <rect x="40" y="195" width="220" height="48" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="150" y="225" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" text-anchor="middle">PROCEDURE SITE</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/q013_anterior_ethmoidal_block.png")
    res = generate_anterior_ethmoidal_block(out)
    print("Q013 Anterior Ethmoidal Block:", res, out.exists())
