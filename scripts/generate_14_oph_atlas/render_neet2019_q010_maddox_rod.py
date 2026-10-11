import sys
from pathlib import Path
from render_helper import render_html_to_png

def generate_maddox_rod_instrument(output_path):
    # Medical instrument atlas: Maddox Rod and Optical Principle
    # Detailed 3D rendering of the red grooved cylindrical trial lens instrument
    # alongside optical conversion of a point light source into a perpendicular red streak
    # on solid #000000 background.
    
    html = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#000000;">
      <defs>
        <!-- Trial Frame Metal Rim Gradient -->
        <linearGradient id="metalRim" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#f8fafc"/>
          <stop offset="30%" stop-color="#94a3b8"/>
          <stop offset="60%" stop-color="#cbd5e1"/>
          <stop offset="85%" stop-color="#64748b"/>
          <stop offset="100%" stop-color="#334155"/>
        </linearGradient>

        <!-- Red Glass Cylinders Gradient -->
        <linearGradient id="redCylinder" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ef4444"/>
          <stop offset="35%" stop-color="#f87171"/>
          <stop offset="60%" stop-color="#dc2626"/>
          <stop offset="100%" stop-color="#991b1b"/>
        </linearGradient>

        <!-- Red Glass Base Disc -->
        <radialGradient id="redGlassDisc" cx="45%" cy="45%" r="55%">
          <stop offset="0%" stop-color="#f87171" stop-opacity="0.9"/>
          <stop offset="70%" stop-color="#dc2626" stop-opacity="0.95"/>
          <stop offset="100%" stop-color="#7f1d1d" stop-opacity="1"/>
        </radialGradient>

        <!-- Optical Ray White Light Beam -->
        <linearGradient id="whiteBeam" x1="0%" y1="50%" x2="100%" y2="50%">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="80%" stop-color="#fef08a" stop-opacity="0.8"/>
          <stop offset="100%" stop-color="#fef08a" stop-opacity="0.2"/>
        </linearGradient>

        <!-- Focal Red Streak Glow -->
        <filter id="streakGlow" x="-50%" y="-20%" width="200%" height="140%">
          <feGaussianBlur stdDeviation="4" result="blur"/>
          <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
        <filter id="deviceShadow" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="8" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.85"/>
        </filter>
      </defs>

      <rect width="1200" height="900" fill="#000000"/>

      <!-- Header Pill -->
      <g id="header">
        <rect x="340" y="20" width="520" height="42" rx="21" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="600" y="47" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" text-anchor="middle" letter-spacing="1">OPHTHALMIC CLINICAL TRIAL INSTRUMENT</text>
      </g>

      <!-- ================= PART 1: 3D MADDOX ROD INSTRUMENT (Left Side: cx=380, cy=460) ================= -->
      <g id="maddox_rod_device" filter="url(#deviceShadow)">
        <!-- Long Metal Handle extending down-left -->
        <path d="M 330 650 L 160 840 L 140 820 L 310 630 Z" fill="url(#metalRim)" stroke="#334155" stroke-width="2"/>
        <!-- Handle Grip Ridges -->
        <line x1="170" y1="810" x2="185" y2="825" stroke="#1e293b" stroke-width="3"/>
        <line x1="190" y1="790" x2="205" y2="805" stroke="#1e293b" stroke-width="3"/>
        <line x1="210" y1="770" x2="225" y2="785" stroke="#1e293b" stroke-width="3"/>
        <line x1="230" y1="750" x2="245" y2="765" stroke="#1e293b" stroke-width="3"/>

        <!-- Circular Trial Frame Metal Rim (Outer ring diameter 380, center at 380, 440) -->
        <circle cx="380" cy="440" r="190" fill="url(#metalRim)" stroke="#1e293b" stroke-width="4"/>
        <circle cx="380" cy="440" r="172" fill="#0f172a" stroke="#475569" stroke-width="2"/>

        <!-- Red Glass Aperture (r=165) -->
        <circle cx="380" cy="440" r="165" fill="url(#redGlassDisc)"/>

        <!-- Series of Parallel Cylindrical Red Glass Rods (Horizontal orientation) -->
        <!-- Each rod is a plano-convex cylinder running horizontally across the disk -->
        <!-- Clipped to circular glass aperture -->
        <clipPath id="lensGlassClip">
          <circle cx="380" cy="440" r="165"/>
        </clipPath>

        <g clip-path="url(#lensGlassClip)">
          <!-- Draw parallel horizontal rods with convex highlight shading -->
          <!-- Rods from y=285 to y=595 with step 22px -->
          <g stroke="#7f1d1d" stroke-width="1.5">
            <!-- Rod 1 -->
            <rect x="200" y="280" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="287" x2="560" y2="287" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 2 -->
            <rect x="200" y="302" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="309" x2="560" y2="309" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 3 -->
            <rect x="200" y="324" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="331" x2="560" y2="331" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 4 -->
            <rect x="200" y="346" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="353" x2="560" y2="353" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 5 -->
            <rect x="200" y="368" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="375" x2="560" y2="375" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 6 -->
            <rect x="200" y="390" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="397" x2="560" y2="397" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 7 -->
            <rect x="200" y="412" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="419" x2="560" y2="419" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 8 -->
            <rect x="200" y="434" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="441" x2="560" y2="441" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 9 -->
            <rect x="200" y="456" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="463" x2="560" y2="463" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 10 -->
            <rect x="200" y="478" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="485" x2="560" y2="485" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 11 -->
            <rect x="200" y="500" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="507" x2="560" y2="507" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 12 -->
            <rect x="200" y="522" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="529" x2="560" y2="529" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 13 -->
            <rect x="200" y="544" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="551" x2="560" y2="551" stroke="#ffffff" stroke-width="2" opacity="0.6"/>

            <!-- Rod 14 -->
            <rect x="200" y="566" width="360" height="20" fill="url(#redCylinder)"/>
            <line x1="200" y1="573" x2="560" y2="573" stroke="#ffffff" stroke-width="2" opacity="0.6"/>
          </g>
        </g>

        <!-- Lens Edge Bevel & Highlights -->
        <circle cx="380" cy="440" r="165" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.5"/>
        <path d="M 260 320 C 320 280 440 280 500 320" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.7"/>
      </g>

      <!-- ================= PART 2: OPTICAL PRINCIPLE SCHEMATIC (Right Side: x=700 to 1140) ================= -->
      <g id="optical_principle_diagram" filter="url(#deviceShadow)">
        <rect x="680" y="140" width="480" height="660" rx="16" fill="#0b1329" stroke="#334155" stroke-width="2.5"/>
        
        <!-- Header -->
        <rect x="710" y="165" width="420" height="38" rx="19" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="920" y="190" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="700" text-anchor="middle">OPTICAL REFRACTION PRINCIPLE</text>

        <!-- 1. Point Light Source (Penlight spotlight at x=740, y=340) -->
        <g id="point_source">
          <circle cx="740" cy="340" r="14" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>
          <circle cx="740" cy="340" r="6" fill="#ffffff"/>
          <text x="740" y="380" fill="#fef08a" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">POINT SOURCE</text>
          <text x="740" y="398" fill="#94a3b8" font-family="sans-serif" font-size="11" text-anchor="middle">(Penlight Spot)</text>

          <!-- Diverging Rays towards cylinder -->
          <line x1="755" y1="340" x2="840" y2="290" stroke="#fef08a" stroke-width="2" stroke-dasharray="4,2"/>
          <line x1="755" y1="340" x2="840" y2="340" stroke="#ffffff" stroke-width="2.5"/>
          <line x1="755" y1="340" x2="840" y2="390" stroke="#fef08a" stroke-width="2" stroke-dasharray="4,2"/>
        </g>

        <!-- 2. Plano-Convex Red Cylindrical Lens Profile (x=850, y=280 to 400) -->
        <g id="cylindrical_lens_profile">
          <path d="M 850 280 C 880 340 880 340 850 400 Z" fill="url(#redCylinder)" stroke="#ef4444" stroke-width="2"/>
          <text x="860" y="430" fill="#f87171" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">CYLINDER</text>
        </g>

        <!-- 3. PERPENDICULAR LINE IMAGE / RED STREAK ON RETINA/VIEWER (x=1020) -->
        <g id="red_streak_image" filter="url(#streakGlow)">
          <!-- Continuous Vertical Red Focal Streak -->
          <line x1="1020" y1="230" x2="1020" y2="450" stroke="#ef4444" stroke-width="8" stroke-linecap="round"/>
          <line x1="1020" y1="230" x2="1020" y2="450" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>

          <text x="1020" y="480" fill="#f87171" font-family="sans-serif" font-size="13" font-weight="800" text-anchor="middle">RED LINE STREAK</text>
          <text x="1020" y="498" fill="#cbd5e1" font-family="sans-serif" font-size="11" text-anchor="middle">(Perpendicular 90°)</text>

          <!-- Light rays converging into vertical line -->
          <line x1="870" y1="300" x2="1015" y2="250" stroke="#f87171" stroke-width="1.8"/>
          <line x1="875" y1="340" x2="1015" y2="340" stroke="#f87171" stroke-width="2.5"/>
          <line x1="870" y1="380" x2="1015" y2="430" stroke="#f87171" stroke-width="1.8"/>
        </g>

        <!-- Clinical Takeaway Box inside card -->
        <rect x="710" y="540" width="420" height="230" rx="12" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="920" y="575" fill="#f59e0b" font-family="sans-serif" font-size="15" font-weight="800" text-anchor="middle">DIAGNOSTIC PRINCIPLE</text>
        
        <g fill="#cbd5e1" font-family="sans-serif" font-size="13" font-weight="500">
          <text x="730" y="612">• Series of high-power plano-convex cylinders</text>
          <text x="730" y="642">• Converts point light into a focal streak at 90°</text>
          <text x="730" y="672">• Horizontal rods → Vertical red streak</text>
          <text x="730" y="702">• Vertical rods → Horizontal red streak</text>
          <text x="730" y="732">• Dissociates fusion to measure heterophoria/tropia</text>
        </g>
      </g>

      <!-- NEUTRAL QUESTION MARKER POINTER TARGETING INSTRUMENT -->
      <g id="neutral_marker">
        <path d="M 200 190 L 290 190 L 350 280" fill="none" stroke="#f59e0b" stroke-width="3"/>
        <polygon points="350,280 338,270 350,265" fill="#f59e0b"/>
        
        <rect x="40" y="165" width="220" height="48" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
        <text x="150" y="195" fill="#f59e0b" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" text-anchor="middle">TEST INSTRUMENT</text>
      </g>
    </svg>
    """
    return render_html_to_png(html, output_path, 1200, 900)

if __name__ == "__main__":
    out = Path("scripts/generate_14_oph_atlas/neet2019_q010_maddox_rod.png")
    res = generate_maddox_rod_instrument(out)
    print("NEET 2019 Q010 Maddox Rod:", res, out.exists())
