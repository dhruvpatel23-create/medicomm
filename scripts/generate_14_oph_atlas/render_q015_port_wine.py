import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_port_wine_stain(output_path):
    # Medical atlas illustration of a young pediatric face in neutral three-quarters / anterior view
    # displaying unilateral Port-Wine Stain (Nevus Flammeus) of Sturge-Weber syndrome
    # covering V1 and V2 dermatomes of the right face on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Gradients for Head & Face -->
        <linearGradient id="skinBase" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#f5d0b5"/>
          <stop offset="50%" stop-color="#e8be9e"/>
          <stop offset="100%" stop-color="#cf9f7e"/>
        </linearGradient>
        <radialGradient id="faceShade" cx="45%" cy="45%" r="55%">
          <stop offset="0%" stop-color="#ffdfcb"/>
          <stop offset="60%" stop-color="#e2b493"/>
          <stop offset="100%" stop-color="#b88362"/>
        </radialGradient>
        
        <!-- Port Wine Stain Vascular Capillary Malformation Pattern -->
        <linearGradient id="pwsGradient" x1="20%" y1="10%" x2="70%" y2="90%">
          <stop offset="0%" stop-color="#800020" stop-opacity="0.88"/>
          <stop offset="30%" stop-color="#931336" stop-opacity="0.85"/>
          <stop offset="70%" stop-color="#720a22" stop-opacity="0.90"/>
          <stop offset="100%" stop-color="#58081a" stop-opacity="0.85"/>
        </linearGradient>
        
        <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="3" result="blur"/>
          <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
        <filter id="pwsTexture" x="-10%" y="-10%" width="120%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise"/>
          <feColorMatrix type="matrix" values="1 0 0 0 0  0 0.2 0 0 0  0 0 0.3 0 0  0 0 0 0.7 0" in="noise" result="coloredNoise"/>
          <feBlend in="SourceGraphic" in2="coloredNoise" mode="multiply"/>
        </filter>
        
        <linearGradient id="hairGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#2a1a12"/>
          <stop offset="70%" stop-color="#190e08"/>
          <stop offset="100%" stop-color="#0a0503"/>
        </linearGradient>
      </defs>

      <!-- Background: Solid Pure Black #000000 -->
      <rect width="1200" height="900" fill="#000000"/>

      <!-- Subject Head Contour / Neck -->
      <g id="head_and_neck">
        <!-- Neck -->
        <path d="M 480 620 Q 480 780 430 870 L 770 870 Q 720 780 720 620 Z" fill="#dcae8d" stroke="#b08060" stroke-width="2"/>
        <path d="M 480 620 Q 600 660 720 620 Q 600 680 480 620 Z" fill="#bf8c6c" opacity="0.6"/>
        
        <!-- Ears -->
        <!-- Right Ear (Patient's right = viewer's left) -->
        <path d="M 390 400 C 350 420 340 480 370 530 C 390 560 410 560 415 540 Z" fill="#deb091" stroke="#b08060" stroke-width="2"/>
        <path d="M 375 430 C 360 450 360 490 380 520" fill="none" stroke="#9e6d4e" stroke-width="3"/>
        
        <!-- Left Ear (Patient's left = viewer's right) -->
        <path d="M 810 400 C 850 420 860 480 830 530 C 810 560 790 560 785 540 Z" fill="#e2b798" stroke="#b08060" stroke-width="2"/>
        <path d="M 825 430 C 840 450 840 490 820 520" fill="none" stroke="#9e6d4e" stroke-width="3"/>

        <!-- Head / Cranium Shape -->
        <path d="M 410 420 C 390 260 500 130 600 130 C 700 130 810 260 790 420 C 785 520 730 650 600 650 C 470 650 415 520 410 420 Z" 
              fill="url(#faceShade)" stroke="#b88362" stroke-width="2"/>
              
        <!-- Face Features -->
        <!-- Eyebrows -->
        <!-- Right Eyebrow -->
        <path d="M 450 365 Q 490 345 545 365" fill="none" stroke="#4a3020" stroke-width="5" stroke-linecap="round"/>
        <!-- Left Eyebrow -->
        <path d="M 655 365 Q 710 345 750 365" fill="none" stroke="#4a3020" stroke-width="5" stroke-linecap="round"/>

        <!-- Eyes -->
        <!-- Right Eye (underneath port-wine stain) -->
        <g id="rightEye">
          <!-- Sclera -->
          <path d="M 460 395 Q 500 375 540 395 Q 500 420 460 395 Z" fill="#f8fafc" stroke="#8a5a40" stroke-width="1.5"/>
          <!-- Iris -->
          <circle cx="500" cy="396" r="14" fill="#5c3826"/>
          <!-- Pupil -->
          <circle cx="500" cy="396" r="6" fill="#111111"/>
          <!-- Highlight -->
          <circle cx="497" cy="393" r="2.5" fill="#ffffff"/>
          <!-- Upper Eyelid crease -->
          <path d="M 455 390 Q 500 370 545 390" fill="none" stroke="#7a4628" stroke-width="2"/>
          <!-- Lower lid line -->
          <path d="M 468 405 Q 500 422 532 405" fill="none" stroke="#8a5a40" stroke-width="1.2"/>
        </g>

        <!-- Left Eye (Normal) -->
        <g id="leftEye">
          <!-- Sclera -->
          <path d="M 660 395 Q 700 375 740 395 Q 700 420 660 395 Z" fill="#f8fafc" stroke="#8a5a40" stroke-width="1.5"/>
          <!-- Iris -->
          <circle cx="700" cy="396" r="14" fill="#5c3826"/>
          <!-- Pupil -->
          <circle cx="700" cy="396" r="6" fill="#111111"/>
          <!-- Highlight -->
          <circle cx="697" cy="393" r="2.5" fill="#ffffff"/>
          <!-- Upper Eyelid crease -->
          <path d="M 655 390 Q 700 370 745 390" fill="none" stroke="#7a4628" stroke-width="2"/>
          <!-- Lower lid line -->
          <path d="M 668 405 Q 700 422 732 405" fill="none" stroke="#8a5a40" stroke-width="1.2"/>
        </g>

        <!-- Nose -->
        <g id="nose">
          <path d="M 595 365 L 592 460 Q 580 495 595 500 Q 600 502 605 500 Q 620 495 608 460" fill="none" stroke="#b07d5b" stroke-width="2"/>
          <!-- Nostrils -->
          <path d="M 578 495 Q 585 505 593 498" fill="none" stroke="#8a5538" stroke-width="2.5"/>
          <path d="M 622 495 Q 615 505 607 498" fill="none" stroke="#8a5538" stroke-width="2.5"/>
          <path d="M 570 488 Q 568 502 582 502" fill="none" stroke="#a06846" stroke-width="1.5"/>
          <path d="M 630 488 Q 632 502 618 502" fill="none" stroke="#a06846" stroke-width="1.5"/>
        </g>

        <!-- Lips / Mouth -->
        <g id="mouth">
          <!-- Upper Lip -->
          <path d="M 550 560 Q 580 548 600 555 Q 620 548 650 560 Q 600 568 550 560 Z" fill="#cf7a7a" stroke="#994d4d" stroke-width="1.5"/>
          <!-- Lower Lip -->
          <path d="M 552 562 Q 600 570 648 562 Q 600 600 552 562 Z" fill="#dc8a8a" stroke="#994d4d" stroke-width="1.5"/>
          <!-- Oral Commissures -->
          <circle cx="550" cy="560" r="2" fill="#7a3333"/>
          <circle cx="650" cy="560" r="2" fill="#7a3333"/>
        </g>

        <!-- UNILATERAL PORT-WINE STAIN (V1 & V2 DERMATOME DISTRIBUTION) -->
        <!-- Strictly respects facial midline (x=600) and covers right forehead, upper/lower eyelid, malar cheek, side of nose, and upper lip -->
        <g id="port_wine_stain" filter="url(#pwsTexture)">
          <path d="M 600 135 
                   C 510 140 440 210 420 300 
                   C 410 350 405 410 400 460
                   C 395 500 415 550 450 575
                   C 490 600 530 605 570 590
                   C 585 585 595 575 600 565
                   L 600 550
                   L 592 500
                   L 596 440
                   L 600 370
                   Z" 
                fill="url(#pwsGradient)" opacity="0.88" />
                
          <!-- Realistic capillary vascular borders & slight islands along V2 border -->
          <path d="M 450 550 C 470 580 520 595 570 580 C 550 565 500 555 450 550 Z" fill="#800020" opacity="0.6"/>
          <circle cx="435" cy="490" r="16" fill="#8a0c28" opacity="0.7"/>
          <circle cx="445" cy="520" r="14" fill="#800020" opacity="0.65"/>
          <circle cx="420" cy="420" r="18" fill="#720a22" opacity="0.75"/>
          <circle cx="510" cy="310" r="22" fill="#931336" opacity="0.55"/>
          <circle cx="460" cy="330" r="28" fill="#800020" opacity="0.65"/>
          <circle cx="550" cy="220" r="32" fill="#7a0a22" opacity="0.7"/>
        </g>

        <!-- Midline marker line / Facial symmetry balance -->
        <line x1="600" y1="130" x2="600" y2="640" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.4"/>

        <!-- Hair Outline -->
        <path d="M 390 380 C 370 240 460 80 600 80 C 740 80 830 240 810 380 
                 C 820 300 810 200 780 160 C 730 110 650 95 600 95 C 550 95 470 110 420 160 C 390 200 380 300 390 380 Z" 
              fill="url(#hairGrad)"/>
        <!-- Hair strands framing face -->
        <path d="M 400 330 C 430 230 500 170 580 180 C 520 185 450 230 420 310 Z" fill="#2a1a12"/>
        <path d="M 800 330 C 770 230 700 170 620 180 C 680 185 750 230 780 310 Z" fill="#2a1a12"/>
      </g>

      <!-- Anatomical / Clinical Labels (Professional Medical Atlas Styling, strictly neutral without spoilers) -->
      <!-- Dermatome indicator bracket / label -->
      <g id="neutral_markers">
        <!-- V1/V2 Area Pointer -->
        <path d="M 240 320 L 390 320 L 440 280" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
        <circle cx="440" cy="280" r="4.5" fill="#f59e0b"/>
        
        <rect x="70" y="295" width="220" height="48" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="180" y="325" fill="#f8fafc" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" text-anchor="middle">FACIAL LESION</text>
        
        <!-- Midline Pointer -->
        <path d="M 600 80 L 600 50 L 720 50" fill="none" stroke="#94a3b8" stroke-width="2"/>
        <circle cx="600" cy="80" r="4" fill="#94a3b8"/>
        <rect x="725" y="30" width="160" height="40" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="805" y="55" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600" text-anchor="middle">FACIAL MIDLINE</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/q015_port_wine.png")
    res = generate_port_wine_stain(out)
    print("Q015 Port Wine Stain:", res, out.exists())
