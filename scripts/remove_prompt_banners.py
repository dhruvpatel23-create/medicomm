import os
import json
import shutil

BASE_DIR = r"d:\medicomm\dhruv1"
IMG_DIR = os.path.join(BASE_DIR, r"output\imagegen\community-medicine-2020-2021-img1")
BRAIN_ASSETS_DIR = r"C:\Users\Hp\.gemini\antigravity\brain\369624d3-e2be-4cc6-95be-659410795a7a\assets"

SVGS = {}

# 1. Sharps Waste
SVGS["neet-pg-2020-community-medicine-q001"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="q1Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="trayGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="steelGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#cbd5e1"/>
      <stop offset="50%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#94a3b8"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" fill="url(#q1Bg)"/>

  <!-- Top Title Pill -->
  <rect x="200" y="40" width="600" height="48" rx="24" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="71" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700" text-anchor="middle" letter-spacing="1">BIOMEDICAL WASTE MANAGEMENT (BMW)</text>

  <text x="500" y="125" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" text-anchor="middle">Clinical Specimen Exhibit: Surgical &amp; Procedural Waste Items</text>

  <!-- Large Kidney Dish / Surgical Preparation Tray Centered -->
  <g transform="translate(100, 180)">
    <!-- Outer Tray Shadow & Rim -->
    <path d="M 80 80 C 200 30, 600 30, 720 80 C 830 130, 830 580, 700 660 C 580 740, 220 740, 100 660 C -30 580, -30 130, 80 80 Z" fill="url(#trayGrad)" stroke="#475569" stroke-width="4"/>
    <path d="M 100 100 C 210 60, 590 60, 700 100 C 795 145, 795 560, 680 635 C 570 710, 230 710, 120 635 C 5 560, 5 145, 100 100 Z" fill="#090d16" stroke="#334155" stroke-width="2"/>

    <!-- Item 1: Disposable Syringe with Fixed Needle -->
    <g transform="translate(200, 180) rotate(-15)">
      <!-- Needle -->
      <line x1="20" y1="50" x2="160" y2="50" stroke="#f8fafc" stroke-width="3"/>
      <polygon points="160,47 175,50 160,53" fill="#f8fafc"/>
      <!-- Hub -->
      <rect x="160" y="42" width="20" height="16" rx="3" fill="#38bdf8"/>
      <!-- Barrel -->
      <rect x="180" y="35" width="220" height="30" rx="4" fill="#334155" stroke="#94a3b8" stroke-width="2" opacity="0.8"/>
      <!-- Graduation Marks -->
      <line x1="220" y1="35" x2="220" y2="48" stroke="#f8fafc" stroke-width="2"/>
      <line x1="260" y1="35" x2="260" y2="48" stroke="#f8fafc" stroke-width="2"/>
      <line x1="300" y1="35" x2="300" y2="48" stroke="#f8fafc" stroke-width="2"/>
      <line x1="340" y1="35" x2="340" y2="48" stroke="#f8fafc" stroke-width="2"/>
      <line x1="380" y1="35" x2="380" y2="48" stroke="#f8fafc" stroke-width="2"/>
      <!-- Plunger -->
      <rect x="360" y="44" width="90" height="12" fill="#64748b"/>
      <rect x="445" y="32" width="10" height="36" rx="2" fill="#94a3b8"/>
      <text x="290" y="25" fill="#cbd5e1" font-family="sans-serif" font-size="14" font-weight="600">Hypodermic Needle &amp; Syringe</text>
    </g>

    <!-- Item 2: Surgical Scalpel Blade -->
    <g transform="translate(220, 360) rotate(10)">
      <path d="M 50 40 L 220 40 L 280 60 C 260 90, 180 90, 120 70 L 50 70 Z" fill="url(#steelGrad)" stroke="#64748b" stroke-width="2"/>
      <rect x="70" y="50" width="70" height="8" rx="2" fill="#1e293b"/>
      <text x="160" y="110" fill="#cbd5e1" font-family="sans-serif" font-size="14" font-weight="600">Surgical Scalpel Blade</text>
    </g>

    <!-- Item 3: Suture Needle with Thread -->
    <g transform="translate(480, 290)">
      <path d="M 60 80 A 60 60 0 0 1 140 160" fill="none" stroke="url(#steelGrad)" stroke-width="4"/>
      <polygon points="140,160 148,168 138,172" fill="#f8fafc"/>
      <path d="M 60 80 Q 40 40 20 60 T 0 100" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3,3"/>
      <text x="90" y="195" fill="#cbd5e1" font-family="sans-serif" font-size="14" font-weight="600">Curved Suture Needle</text>
    </g>

    <!-- Item 4: Broken Ampoule Head (Glass Sharp) -->
    <g transform="translate(260, 520)">
      <polygon points="40,30 70,10 90,35 80,70 30,65" fill="#64748b" opacity="0.6" stroke="#cbd5e1" stroke-width="2"/>
      <text x="110" y="55" fill="#cbd5e1" font-family="sans-serif" font-size="14" font-weight="600">Broken Glass Ampoule Head</text>
    </g>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 2. Chemical Waste
SVGS["neet-pg-2020-community-medicine-q008"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="q8Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="amberBottle" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#78350f"/>
      <stop offset="50%" stop-color="#b45309"/>
      <stop offset="100%" stop-color="#451a03"/>
    </linearGradient>
    <linearGradient id="chemFluid" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" fill="url(#q8Bg)"/>

  <!-- Top Title Pill -->
  <rect x="200" y="40" width="600" height="48" rx="24" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="71" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700" text-anchor="middle" letter-spacing="1">HOSPITAL WASTE SEGREGATION: CHEMICAL WASTE</text>

  <text x="500" y="125" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" text-anchor="middle">Laboratory &amp; Clinical Disinfection Byproducts</text>

  <!-- Laboratory Workbench Surface Centered -->
  <rect x="80" y="740" width="840" height="22" rx="4" fill="#334155"/>
  <rect x="100" y="762" width="800" height="60" fill="#0f172a" stroke="#1e293b"/>

  <!-- Chemical Bottle 1: Formalin / Spent Reagents -->
  <g transform="translate(140, 270)">
    <!-- Cap -->
    <rect x="65" y="0" width="70" height="50" rx="6" fill="#0f172a" stroke="#475569" stroke-width="2"/>
    <!-- Neck -->
    <rect x="75" y="50" width="50" height="35" fill="url(#amberBottle)"/>
    <!-- Bottle Body -->
    <rect x="20" y="85" width="160" height="385" rx="18" fill="url(#amberBottle)" stroke="#d97706" stroke-width="2.5"/>
    
    <!-- Chemical Label -->
    <rect x="35" y="160" width="130" height="200" rx="8" fill="#f8fafc" opacity="0.95"/>
    <text x="100" y="198" fill="#991b1b" font-family="sans-serif" font-size="15" font-weight="800" text-anchor="middle">10% FORMALIN</text>
    <text x="100" y="222" fill="#0f172a" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Spent Fixative</text>
    <line x1="45" y1="240" x2="155" y2="240" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Hazard Symbol -->
    <polygon points="100,258 128,286 100,314 72,286" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
    <text x="100" y="293" fill="#dc2626" font-family="sans-serif" font-size="18" font-weight="900" text-anchor="middle">☠</text>
    <text x="100" y="340" fill="#475569" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">CHEMICAL WASTE</text>
  </g>

  <!-- Chemical Container 2: Large Liquid Disinfectant Carboy -->
  <g transform="translate(380, 200)">
    <!-- Handle -->
    <path d="M 90 70 C 90 15, 170 15, 170 70" fill="none" stroke="#475569" stroke-width="14" stroke-linecap="round"/>
    <!-- Cap -->
    <rect x="180" y="35" width="50" height="40" rx="4" fill="#0284c7"/>
    <!-- Carboy Body -->
    <rect x="40" y="75" width="220" height="465" rx="24" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>
    <!-- Fluid level inside -->
    <rect x="48" y="180" width="204" height="350" rx="16" fill="url(#chemFluid)" opacity="0.6"/>

    <!-- Label -->
    <rect x="65" y="230" width="170" height="170" rx="8" fill="#ffffff" opacity="0.95"/>
    <text x="150" y="270" fill="#0369a1" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">SODIUM HYPOCHLORITE</text>
    <text x="150" y="295" fill="#0f172a" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">Disinfectant Solution</text>
    <line x1="80" y1="315" x2="220" y2="315" stroke="#cbd5e1" stroke-width="1.5"/>
    <polygon points="150,328 178,356 150,384 122,356" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
    <text x="150" y="364" fill="#d97706" font-family="sans-serif" font-size="16" font-weight="900" text-anchor="middle">⚠</text>
  </g>

  <!-- Chemical Bottle 3: Laboratory Solvent Bottle -->
  <g transform="translate(680, 310)">
    <!-- Cap -->
    <rect x="55" y="0" width="50" height="38" rx="4" fill="#334155"/>
    <rect x="65" y="38" width="30" height="28" fill="#1e293b"/>
    <rect x="20" y="66" width="120" height="364" rx="14" fill="#0f172a" stroke="#64748b" stroke-width="2"/>
    <rect x="35" y="140" width="90" height="160" rx="6" fill="#f8fafc" opacity="0.9"/>
    <text x="80" y="180" fill="#0f172a" font-family="sans-serif" font-size="14" font-weight="800" text-anchor="middle">LABORATORY</text>
    <text x="80" y="202" fill="#475569" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">REAGENTS</text>
    <line x1="45" y1="220" x2="115" y2="220" stroke="#cbd5e1" stroke-width="1"/>
    <text x="80" y="248" fill="#dc2626" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Liquid Waste</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 3. Gaussian Normal Distribution
SVGS["neet-pg-2020-community-medicine-q012"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="q12Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#030712"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="curveShade" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.02"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" fill="url(#q12Bg)"/>

  <!-- Top Title Pill -->
  <rect x="180" y="50" width="640" height="48" rx="24" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="81" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700" text-anchor="middle" letter-spacing="1">GAUSSIAN NORMAL DISTRIBUTION CURVE</text>

  <text x="500" y="135" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" text-anchor="middle">Study Parameters: Population Mean (μ) = 200  |  Standard Deviation (σ) = 20</text>

  <!-- Neutral Bell Curve Shading -->
  <path d="M 120 740 C 180 740, 240 738, 300 720 C 350 690, 380 620, 420 480 C 460 330, 480 280, 500 280 C 520 280, 540 330, 580 480 C 620 620, 650 690, 700 720 C 760 738, 820 740, 880 740 Z" fill="url(#curveShade)"/>

  <!-- Bell Curve Main Line -->
  <path d="M 120 740 C 180 740, 240 738, 300 720 C 350 690, 380 620, 420 480 C 460 330, 480 280, 500 280 C 520 280, 540 330, 580 480 C 620 620, 650 690, 700 720 C 760 738, 820 740, 880 740" fill="none" stroke="#38bdf8" stroke-width="4.5"/>

  <!-- Base Baseline Axis -->
  <line x1="90" y1="740" x2="910" y2="740" stroke="#64748b" stroke-width="3"/>
  <polygon points="915,740 900,733 900,747" fill="#64748b"/>
  <polygon points="85,740 100,733 100,747" fill="#64748b"/>

  <!-- Center Mean Axis Line -->
  <line x1="500" y1="280" x2="500" y2="740" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="6,4"/>
  <circle cx="500" cy="280" r="6" fill="#38bdf8"/>

  <!-- Vertical Divider Lines for Standard Deviations -->
  <!-- -1 SD (400) and +1 SD (600) -->
  <line x1="400" y1="540" x2="400" y2="740" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4"/>
  <line x1="600" y1="540" x2="600" y2="740" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,4"/>

  <!-- -2 SD (300) and +2 SD (700) -->
  <line x1="300" y1="720" x2="300" y2="740" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,3"/>
  <line x1="700" y1="720" x2="700" y2="740" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,3"/>

  <!-- -3 SD (200) and +3 SD (800) -->
  <line x1="200" y1="736" x2="200" y2="740" stroke="#475569" stroke-width="1"/>
  <line x1="800" y1="736" x2="800" y2="740" stroke="#475569" stroke-width="1"/>

  <!-- Axis Labels below baseline -->
  <text x="500" y="775" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="700" text-anchor="middle">Mean (μ)</text>
  <text x="500" y="810" fill="#f8fafc" font-family="sans-serif" font-size="24" font-weight="800" text-anchor="middle">200</text>

  <text x="400" y="775" fill="#94a3b8" font-family="sans-serif" font-size="15" font-weight="600" text-anchor="middle">μ - 1σ</text>
  <text x="400" y="810" fill="#e2e8f0" font-family="sans-serif" font-size="20" font-weight="700" text-anchor="middle">180</text>

  <text x="600" y="775" fill="#94a3b8" font-family="sans-serif" font-size="15" font-weight="600" text-anchor="middle">μ + 1σ</text>
  <text x="600" y="810" fill="#e2e8f0" font-family="sans-serif" font-size="20" font-weight="700" text-anchor="middle">220</text>

  <text x="300" y="775" fill="#64748b" font-family="sans-serif" font-size="14" font-weight="500" text-anchor="middle">μ - 2σ</text>
  <text x="300" y="810" fill="#cbd5e1" font-family="sans-serif" font-size="18" font-weight="600" text-anchor="middle">160</text>

  <text x="700" y="775" fill="#64748b" font-family="sans-serif" font-size="14" font-weight="500" text-anchor="middle">μ + 2σ</text>
  <text x="700" y="810" fill="#cbd5e1" font-family="sans-serif" font-size="18" font-weight="600" text-anchor="middle">240</text>

  <text x="200" y="775" fill="#475569" font-family="sans-serif" font-size="14" font-weight="500" text-anchor="middle">μ - 3σ</text>
  <text x="200" y="810" fill="#94a3b8" font-family="sans-serif" font-size="16" font-weight="600" text-anchor="middle">140</text>

  <text x="800" y="775" fill="#475569" font-family="sans-serif" font-size="14" font-weight="500" text-anchor="middle">μ + 3σ</text>
  <text x="800" y="810" fill="#94a3b8" font-family="sans-serif" font-size="16" font-weight="600" text-anchor="middle">260</text>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 4. Blood Bag vs Items A-D
SVGS["neet-pg-2020-community-medicine-q013"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="q13Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="bloodGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="70%" stop-color="#991b1b"/>
      <stop offset="100%" stop-color="#450a0a"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" fill="url(#q13Bg)"/>

  <!-- Top Title Pill -->
  <rect x="180" y="40" width="640" height="48" rx="24" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="71" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700" text-anchor="middle" letter-spacing="1">HOSPITAL CLINICAL WASTE DISPOSAL</text>

  <text x="500" y="125" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" text-anchor="middle">Biomedical Waste Categories: Clinical Item Evaluation</text>

  <!-- 4 Clinical Waste Items (Neutral Boxes A, B, C, D) Expanded Vertically -->
  <!-- Item A: Blood Bag -->
  <g transform="translate(80, 160)">
    <rect width="390" height="360" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="15" y="15" width="85" height="32" rx="6" fill="#1e293b"/>
    <text x="57" y="37" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">ITEM A</text>

    <!-- Blood Bag Vector -->
    <rect x="115" y="65" width="160" height="210" rx="18" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
    <rect x="122" y="120" width="146" height="150" rx="12" fill="url(#bloodGrad)"/>
    <rect x="130" y="135" width="130" height="75" rx="4" fill="#ffffff" opacity="0.9"/>
    <text x="195" y="162" fill="#991b1b" font-family="sans-serif" font-size="13" font-weight="800" text-anchor="middle">WHOLE BLOOD</text>
    <text x="195" y="185" fill="#0f172a" font-family="sans-serif" font-size="11" font-weight="600" text-anchor="middle">CPDA-1 Solution</text>
    <path d="M 195 275 L 195 315 C 195 335 240 335 240 345" fill="none" stroke="#ef4444" stroke-width="4"/>
    <text x="195" y="335" fill="#f8fafc" font-family="sans-serif" font-size="15" font-weight="700" text-anchor="middle">Blood Transfusion Bag</text>
  </g>

  <!-- Item B: Gloves -->
  <g transform="translate(530, 160)">
    <rect width="390" height="360" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="15" y="15" width="85" height="32" rx="6" fill="#1e293b"/>
    <text x="57" y="37" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">ITEM B</text>

    <!-- Pair of Gloves Vector -->
    <g transform="translate(130, 80)">
      <path d="M 30 190 L 30 110 C 30 90, 45 90, 45 110 L 45 60 C 45 45, 60 45, 60 60 L 60 50 C 60 35, 75 35, 75 50 L 75 65 C 75 50, 90 50, 90 65 L 90 120 C 100 120, 115 135, 105 150 L 95 190 Z" fill="#94a3b8" stroke="#cbd5e1" stroke-width="2"/>
      <path d="M 100 190 L 100 110 C 100 90, 115 90, 115 110 L 115 60 C 115 45, 130 45, 130 60 L 130 50 C 130 35, 145 35, 145 50 L 145 65 C 145 50, 160 50, 160 65 L 160 120 C 170 120, 185 135, 175 150 L 165 190 Z" fill="#64748b" stroke="#cbd5e1" stroke-width="2"/>
    </g>
    <text x="195" y="335" fill="#f8fafc" font-family="sans-serif" font-size="15" font-weight="700" text-anchor="middle">Disposable Latex Gloves</text>
  </g>

  <!-- Item C: Sharps -->
  <g transform="translate(80, 550)">
    <rect width="390" height="360" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="15" y="15" width="85" height="32" rx="6" fill="#1e293b"/>
    <text x="57" y="37" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">ITEM C</text>

    <!-- Sharps Vector -->
    <g transform="translate(75, 130)">
      <line x1="30" y1="50" x2="120" y2="50" stroke="#f8fafc" stroke-width="3"/>
      <polygon points="120,47 132,50 120,53" fill="#f8fafc"/>
      <rect x="132" y="42" width="18" height="16" rx="2" fill="#38bdf8"/>
      <rect x="150" y="36" width="130" height="28" rx="3" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
      <rect x="250" y="44" width="45" height="12" fill="#64748b"/>
    </g>
    <text x="195" y="335" fill="#f8fafc" font-family="sans-serif" font-size="15" font-weight="700" text-anchor="middle">Hypodermic Needles &amp; Sharps</text>
  </g>

  <!-- Item D: Urine Bag -->
  <g transform="translate(530, 550)">
    <rect width="390" height="360" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="15" y="15" width="85" height="32" rx="6" fill="#1e293b"/>
    <text x="57" y="37" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">ITEM D</text>

    <!-- Urine Collection Bag Vector -->
    <g transform="translate(130, 75)">
      <rect x="20" y="20" width="130" height="190" rx="12" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
      <rect x="26" y="90" width="118" height="115" rx="8" fill="#eab308" opacity="0.3"/>
      <line x1="35" y1="100" x2="65" y2="100" stroke="#cbd5e1" stroke-width="1.5"/>
      <line x1="35" y1="130" x2="75" y2="130" stroke="#cbd5e1" stroke-width="1.5"/>
      <line x1="35" y1="160" x2="65" y2="160" stroke="#cbd5e1" stroke-width="1.5"/>
      <path d="M 85 20 L 85 -10" stroke="#94a3b8" stroke-width="4"/>
    </g>
    <text x="195" y="335" fill="#f8fafc" font-family="sans-serif" font-size="15" font-weight="700" text-anchor="middle">Urinary Drainage Collector Bag</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 5. NACO STI Kits
SVGS["ini-cet-2021-community-medicine-q004"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#030712"/>

  <!-- Top Title Pill -->
  <rect x="180" y="40" width="640" height="48" rx="24" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="71" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">NACO SYNDROMIC MANAGEMENT OF STI / RTI</text>

  <text x="500" y="125" fill="#94a3b8" font-family="sans-serif" font-size="15" text-anchor="middle">Match the Color-Coded Drug Kits (Column I) with the Target Clinical Syndrome (Column II)</text>

  <!-- Column I Header -->
  <rect x="80" y="160" width="370" height="42" rx="8" fill="#1e293b"/>
  <text x="265" y="187" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">COLUMN I: COLOR-CODED KITS</text>

  <!-- Column II Header -->
  <rect x="550" y="160" width="370" height="42" rx="8" fill="#1e293b"/>
  <text x="735" y="187" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">COLUMN II: CLINICAL SYNDROMES</text>

  <!-- Row 1: Kit A vs Syndrome 1 -->
  <g transform="translate(80, 230)">
    <rect width="370" height="135" rx="12" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
    <rect x="15" y="15" width="70" height="35" rx="6" fill="#64748b"/>
    <text x="50" y="39" fill="#fff" font-family="sans-serif" font-size="17" font-weight="900" text-anchor="middle">A</text>
    <text x="110" y="42" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="800">KIT 1 (GREY)</text>
    <text x="25" y="95" fill="#94a3b8" font-family="sans-serif" font-size="14">Color Identification: Grey Packaging</text>
  </g>
  <g transform="translate(550, 230)">
    <rect width="370" height="135" rx="12" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="15" y="15" width="45" height="35" rx="6" fill="#334155"/>
    <text x="37" y="39" fill="#38bdf8" font-family="sans-serif" font-size="17" font-weight="800" text-anchor="middle">1</text>
    <text x="80" y="42" fill="#f8fafc" font-family="sans-serif" font-size="17" font-weight="700">Vaginal Discharge / Vaginitis</text>
    <text x="25" y="95" fill="#94a3b8" font-family="sans-serif" font-size="14">Syndromic presentation</text>
  </g>

  <!-- Row 2: Kit B vs Syndrome 2 -->
  <g transform="translate(80, 400)">
    <rect width="370" height="135" rx="12" fill="#064e3b" stroke="#10b981" stroke-width="2"/>
    <rect x="15" y="15" width="70" height="35" rx="6" fill="#10b981"/>
    <text x="50" y="39" fill="#064e3b" font-family="sans-serif" font-size="17" font-weight="900" text-anchor="middle">B</text>
    <text x="110" y="42" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="800">KIT 2 (GREEN)</text>
    <text x="25" y="95" fill="#a7f3d0" font-family="sans-serif" font-size="14">Color Identification: Green Packaging</text>
  </g>
  <g transform="translate(550, 400)">
    <rect width="370" height="135" rx="12" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="15" y="15" width="45" height="35" rx="6" fill="#334155"/>
    <text x="37" y="39" fill="#38bdf8" font-family="sans-serif" font-size="17" font-weight="800" text-anchor="middle">2</text>
    <text x="80" y="42" fill="#f8fafc" font-family="sans-serif" font-size="16" font-weight="700">Non-Herpetic Genital Ulcer</text>
    <text x="80" y="70" fill="#cbd5e1" font-family="sans-serif" font-size="14">(Allergic to Penicillin)</text>
  </g>

  <!-- Row 3: Kit C vs Syndrome 3 -->
  <g transform="translate(80, 570)">
    <rect width="370" height="135" rx="12" fill="#334155" stroke="#cbd5e1" stroke-width="2"/>
    <rect x="15" y="15" width="70" height="35" rx="6" fill="#f8fafc"/>
    <text x="50" y="39" fill="#0f172a" font-family="sans-serif" font-size="17" font-weight="900" text-anchor="middle">C</text>
    <text x="110" y="42" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="800">KIT 3 (WHITE)</text>
    <text x="25" y="95" fill="#e2e8f0" font-family="sans-serif" font-size="14">Color Identification: White Packaging</text>
  </g>
  <g transform="translate(550, 570)">
    <rect width="370" height="135" rx="12" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="15" y="15" width="45" height="35" rx="6" fill="#334155"/>
    <text x="37" y="39" fill="#38bdf8" font-family="sans-serif" font-size="17" font-weight="800" text-anchor="middle">3</text>
    <text x="80" y="42" fill="#f8fafc" font-family="sans-serif" font-size="17" font-weight="700">Non-Herpetic Genital Ulcer</text>
    <text x="25" y="95" fill="#94a3b8" font-family="sans-serif" font-size="14">Syndromic presentation</text>
  </g>

  <!-- Row 4: Kit D vs Syndrome 4 -->
  <g transform="translate(80, 740)">
    <rect width="370" height="135" rx="12" fill="#1e3a8a" stroke="#3b82f6" stroke-width="2"/>
    <rect x="15" y="15" width="70" height="35" rx="6" fill="#3b82f6"/>
    <text x="50" y="39" fill="#fff" font-family="sans-serif" font-size="17" font-weight="900" text-anchor="middle">D</text>
    <text x="110" y="42" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="800">KIT 4 (BLUE)</text>
    <text x="25" y="95" fill="#bfdbfe" font-family="sans-serif" font-size="14">Color Identification: Blue Packaging</text>
  </g>
  <g transform="translate(550, 740)">
    <rect width="370" height="135" rx="12" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="15" y="15" width="45" height="35" rx="6" fill="#334155"/>
    <text x="37" y="39" fill="#38bdf8" font-family="sans-serif" font-size="17" font-weight="800" text-anchor="middle">4</text>
    <text x="80" y="42" fill="#f8fafc" font-family="sans-serif" font-size="16" font-weight="700">Urethral / Cervical / Anorectal</text>
    <text x="80" y="70" fill="#cbd5e1" font-family="sans-serif" font-size="14">Discharge Syndrome</text>
  </g>

  <!-- Center Unconnected Question Marks -->
  <g fill="#94a3b8" font-family="sans-serif" font-size="24" font-weight="900" text-anchor="middle">
    <text x="500" y="305">?</text>
    <text x="500" y="475">?</text>
    <text x="500" y="645">?</text>
    <text x="500" y="815">?</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 6. Natural History Timeline
SVGS["ini-cet-2021-community-medicine-q006"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#030712"/>

  <!-- Top Title Pill -->
  <rect x="200" y="50" width="600" height="48" rx="24" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="81" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">NATURAL HISTORY OF INFECTIOUS DISEASE</text>

  <text x="500" y="135" fill="#94a3b8" font-family="sans-serif" font-size="16" text-anchor="middle">Chronological Disease Progression in an Individual Host</text>

  <!-- Timeline Main Axis Centered -->
  <line x1="120" y1="520" x2="880" y2="520" stroke="#334155" stroke-width="8" stroke-linecap="round"/>

  <!-- Point A: Exposure -->
  <g transform="translate(180, 520)">
    <circle cx="0" cy="0" r="18" fill="#0284c7" stroke="#38bdf8" stroke-width="4"/>
    <text x="0" y="-35" fill="#38bdf8" font-family="sans-serif" font-size="22" font-weight="800" text-anchor="middle">A</text>
    <text x="0" y="50" fill="#f8fafc" font-family="sans-serif" font-size="16" font-weight="700" text-anchor="middle">Point A</text>
    <text x="0" y="78" fill="#94a3b8" font-family="sans-serif" font-size="14" text-anchor="middle">Exposure to Agent</text>
  </g>

  <!-- Point B: Pathological Changes Begin -->
  <g transform="translate(400, 520)">
    <circle cx="0" cy="0" r="18" fill="#059669" stroke="#34d399" stroke-width="4"/>
    <text x="0" y="-35" fill="#34d399" font-family="sans-serif" font-size="22" font-weight="800" text-anchor="middle">B</text>
    <text x="0" y="50" fill="#f8fafc" font-family="sans-serif" font-size="16" font-weight="700" text-anchor="middle">Point B</text>
    <text x="0" y="78" fill="#94a3b8" font-family="sans-serif" font-size="14" text-anchor="middle">Pathological Onset</text>
  </g>

  <!-- Point C: PROMINENT QUESTION MARK [?] -->
  <g transform="translate(620, 520)">
    <circle cx="0" cy="0" r="34" fill="#ef4444" opacity="0.2"/>
    <circle cx="0" cy="0" r="24" fill="#dc2626" stroke="#f87171" stroke-width="5"/>
    
    <rect x="-35" y="-100" width="70" height="48" rx="8" fill="#dc2626" stroke="#fca5a5" stroke-width="2"/>
    <text x="0" y="-68" fill="#fff" font-family="sans-serif" font-size="24" font-weight="900" text-anchor="middle">C</text>
    
    <text x="0" y="50" fill="#f87171" font-family="sans-serif" font-size="18" font-weight="900" text-anchor="middle">POINT C</text>
    <text x="0" y="80" fill="#fca5a5" font-family="sans-serif" font-size="18" font-weight="800" text-anchor="middle">[ ? ]</text>
  </g>

  <!-- Point D: Medical Diagnosis -->
  <g transform="translate(820, 520)">
    <circle cx="0" cy="0" r="18" fill="#7c3aed" stroke="#a78bfa" stroke-width="4"/>
    <text x="0" y="-35" fill="#a78bfa" font-family="sans-serif" font-size="22" font-weight="800" text-anchor="middle">D</text>
    <text x="0" y="50" fill="#f8fafc" font-family="sans-serif" font-size="16" font-weight="700" text-anchor="middle">Point D</text>
    <text x="0" y="78" fill="#94a3b8" font-family="sans-serif" font-size="14" text-anchor="middle">Medical Diagnosis</text>
  </g>

  <!-- Stages of Disease Brackets -->
  <path d="M 180 370 L 180 350 L 400 350 L 400 335 L 400 350 L 620 350 L 620 370" fill="none" stroke="#64748b" stroke-width="2"/>
  <text x="400" y="320" fill="#cbd5e1" font-family="sans-serif" font-size="16" font-weight="700" text-anchor="middle">Stage of Subclinical Disease</text>

  <path d="M 620 370 L 620 350 L 720 350 L 720 335 L 720 350 L 820 350 L 820 370" fill="none" stroke="#64748b" stroke-width="2"/>
  <text x="720" y="320" fill="#cbd5e1" font-family="sans-serif" font-size="16" font-weight="700" text-anchor="middle">Stage of Clinical Disease</text>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 7. Vaccine Forest Plot
SVGS["ini-cet-2021-community-medicine-q007"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#030712"/>

  <!-- Top Title Pill -->
  <rect x="200" y="40" width="600" height="48" rx="24" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="71" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">VACCINE EFFICACY CLINICAL TRIAL: FOREST PLOT</text>

  <text x="500" y="125" fill="#94a3b8" font-family="sans-serif" font-size="15" text-anchor="middle">Comparison of Newer Candidate Vaccines vs. Standard Control</text>

  <!-- Plot Graph Area Centered & Expanded -->
  <rect x="80" y="160" width="840" height="740" rx="14" fill="#090d16" stroke="#1e293b" stroke-width="2"/>

  <!-- X-Axis Baseline -->
  <line x1="120" y1="810" x2="880" y2="810" stroke="#475569" stroke-width="3"/>

  <!-- Shaded Equivalence Margin Zone -->
  <rect x="360" y="180" width="280" height="630" fill="#38bdf8" opacity="0.06"/>

  <!-- Comparator Reference Zero Line (x=500) -->
  <line x1="500" y1="180" x2="500" y2="810" stroke="#cbd5e1" stroke-width="2"/>
  <text x="500" y="840" fill="#f8fafc" font-family="sans-serif" font-size="16" font-weight="700" text-anchor="middle">0</text>
  <text x="500" y="865" fill="#94a3b8" font-family="sans-serif" font-size="13" text-anchor="middle">(No Difference)</text>

  <!-- Lower Equivalence Margin -Delta (x=360) -->
  <line x1="360" y1="180" x2="360" y2="810" stroke="#f59e0b" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="360" y="840" fill="#f59e0b" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">-δ</text>
  <text x="360" y="865" fill="#f59e0b" font-family="sans-serif" font-size="13" text-anchor="middle">Non-inferiority limit</text>

  <!-- Upper Equivalence Margin +Delta (x=640) -->
  <line x1="640" y1="180" x2="640" y2="810" stroke="#f59e0b" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="640" y="840" fill="#f59e0b" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">+δ</text>
  <text x="640" y="865" fill="#f59e0b" font-family="sans-serif" font-size="13" text-anchor="middle">Upper margin</text>

  <text x="500" y="210" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="700" text-anchor="middle">ZONE OF EQUIVALENCE (-δ to +δ)</text>

  <!-- Vaccines Plotted -->
  <!-- Vaccine A -->
  <g transform="translate(0, 50)">
    <text x="140" y="245" fill="#f8fafc" font-family="sans-serif" font-size="17" font-weight="800">Vaccine A</text>
    <line x1="220" y1="240" x2="320" y2="240" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="220" y1="228" x2="220" y2="252" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="320" y1="228" x2="320" y2="252" stroke="#cbd5e1" stroke-width="3"/>
    <rect x="265" y="235" width="10" height="10" fill="#38bdf8"/>
  </g>

  <!-- Vaccine B -->
  <g transform="translate(0, 50)">
    <text x="140" y="355" fill="#f8fafc" font-family="sans-serif" font-size="17" font-weight="800">Vaccine B</text>
    <line x1="320" y1="350" x2="420" y2="350" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="320" y1="338" x2="320" y2="362" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="420" y1="338" x2="420" y2="362" stroke="#cbd5e1" stroke-width="3"/>
    <rect x="365" y="345" width="10" height="10" fill="#38bdf8"/>
  </g>

  <!-- Vaccine C -->
  <g transform="translate(0, 50)">
    <text x="140" y="465" fill="#f8fafc" font-family="sans-serif" font-size="17" font-weight="800">Vaccine C</text>
    <line x1="390" y1="460" x2="520" y2="460" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="390" y1="448" x2="390" y2="472" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="520" y1="448" x2="520" y2="472" stroke="#cbd5e1" stroke-width="3"/>
    <rect x="450" y="455" width="10" height="10" fill="#38bdf8"/>
  </g>

  <!-- Vaccine D -->
  <g transform="translate(0, 50)">
    <text x="140" y="575" fill="#f8fafc" font-family="sans-serif" font-size="17" font-weight="800">Vaccine D</text>
    <line x1="460" y1="570" x2="570" y2="570" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="460" y1="558" x2="460" y2="582" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="570" y1="558" x2="570" y2="582" stroke="#cbd5e1" stroke-width="3"/>
    <rect x="510" y="565" width="10" height="10" fill="#38bdf8"/>
  </g>

  <!-- Vaccine E -->
  <g transform="translate(0, 50)">
    <text x="140" y="685" fill="#f8fafc" font-family="sans-serif" font-size="17" font-weight="800">Vaccine E</text>
    <line x1="520" y1="680" x2="630" y2="680" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="520" y1="668" x2="520" y2="692" stroke="#cbd5e1" stroke-width="3"/>
    <line x1="630" y1="668" x2="630" y2="692" stroke="#cbd5e1" stroke-width="3"/>
    <rect x="570" y="675" width="10" height="10" fill="#38bdf8"/>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 8. Hospital Ward Bins
SVGS["ini-cet-2021-community-medicine-q011"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#030712"/>

  <!-- Top Title Pill -->
  <rect x="200" y="40" width="600" height="48" rx="24" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="71" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">HOSPITAL WARD WASTE DISPOSAL STATION</text>

  <text x="500" y="125" fill="#94a3b8" font-family="sans-serif" font-size="16" text-anchor="middle">Color-Coded Segregation Bins Arranged on Hospital Ward Corridor Floor</text>

  <!-- Floor Perspective Line -->
  <line x1="40" y1="810" x2="960" y2="810" stroke="#334155" stroke-width="2.5"/>

  <!-- 4 Clean Pedal Bins Centered & Expanded Vertically -->
  <!-- 1. BLACK BIN -->
  <g transform="translate(60, 180)">
    <rect width="190" height="540" rx="14" fill="#1e293b" stroke="#475569" stroke-width="3"/>
    <rect x="10" y="14" width="170" height="70" rx="8" fill="#0f172a" stroke="#64748b"/>
    <rect x="65" y="540" width="60" height="22" rx="4" fill="#334155"/>
    <text x="95" y="130" fill="#f8fafc" font-family="sans-serif" font-size="20" font-weight="900" text-anchor="middle">BLACK BIN</text>
    
    <g transform="translate(95, 290) scale(1.4)" stroke="#94a3b8" fill="none" stroke-width="3">
      <circle cx="0" cy="0" r="32"/>
      <path d="M -15 -10 L 0 -22 L 15 -10"/>
      <path d="M 22 0 L 10 18 L -5 18"/>
      <path d="M -18 8 L -18 -8 L -6 0"/>
    </g>
    <text x="95" y="380" fill="#94a3b8" font-family="sans-serif" font-size="15" font-weight="700" text-anchor="middle">General Waste</text>
  </g>

  <!-- 2. YELLOW BIN -->
  <g transform="translate(290, 180)">
    <rect width="190" height="540" rx="14" fill="#ca8a04" stroke="#eab308" stroke-width="3"/>
    <rect x="10" y="14" width="170" height="70" rx="8" fill="#facc15" stroke="#a16207"/>
    <rect x="65" y="540" width="60" height="22" rx="4" fill="#a16207"/>
    <text x="95" y="130" fill="#0f172a" font-family="sans-serif" font-size="20" font-weight="900" text-anchor="middle">YELLOW BIN</text>
    
    <g transform="translate(95, 290) scale(1.0)">
      <circle cx="0" cy="0" r="38" fill="#18181b"/>
      <circle cx="0" cy="0" r="24" fill="none" stroke="#facc15" stroke-width="4"/>
      <circle cx="0" cy="-16" r="14" fill="none" stroke="#facc15" stroke-width="4"/>
      <circle cx="-14" cy="8" r="14" fill="none" stroke="#facc15" stroke-width="4"/>
      <circle cx="14" cy="8" r="14" fill="none" stroke="#facc15" stroke-width="4"/>
      <circle cx="0" cy="0" r="8" fill="#facc15"/>
    </g>
    <text x="95" y="380" fill="#713f12" font-family="sans-serif" font-size="15" font-weight="800" text-anchor="middle">Biohazard</text>
  </g>

  <!-- 3. RED BIN -->
  <g transform="translate(520, 180)">
    <rect width="190" height="540" rx="14" fill="#991b1b" stroke="#ef4444" stroke-width="3"/>
    <rect x="10" y="14" width="170" height="70" rx="8" fill="#f87171" stroke="#7f1d1d"/>
    <rect x="65" y="540" width="60" height="22" rx="4" fill="#7f1d1d"/>
    <text x="95" y="130" fill="#f8fafc" font-family="sans-serif" font-size="20" font-weight="900" text-anchor="middle">RED BIN</text>
    
    <g transform="translate(95, 290) scale(1.0)">
      <circle cx="0" cy="0" r="38" fill="#18181b"/>
      <circle cx="0" cy="0" r="24" fill="none" stroke="#f87171" stroke-width="4"/>
      <circle cx="0" cy="-16" r="14" fill="none" stroke="#f87171" stroke-width="4"/>
      <circle cx="-14" cy="8" r="14" fill="none" stroke="#f87171" stroke-width="4"/>
      <circle cx="14" cy="8" r="14" fill="none" stroke="#f87171" stroke-width="4"/>
      <circle cx="0" cy="0" r="8" fill="#f87171"/>
    </g>
    <text x="95" y="380" fill="#fee2e2" font-family="sans-serif" font-size="15" font-weight="800" text-anchor="middle">Biohazard</text>
  </g>

  <!-- 4. BLUE BIN -->
  <g transform="translate(750, 180)">
    <rect width="190" height="540" rx="14" fill="#1e3a8a" stroke="#3b82f6" stroke-width="3"/>
    <rect x="10" y="14" width="170" height="70" rx="8" fill="#60a5fa" stroke="#1d4ed8"/>
    <rect x="65" y="540" width="60" height="22" rx="4" fill="#1e3a8a"/>
    <text x="95" y="130" fill="#f8fafc" font-family="sans-serif" font-size="20" font-weight="900" text-anchor="middle">BLUE BIN</text>
    
    <g transform="translate(95, 290)" stroke="#93c5fd" fill="none" stroke-width="3">
      <path d="M -14 -25 L 14 -25 L 14 -10 L 22 15 C 22 25, -22 25, -22 15 L -14 -10 Z"/>
    </g>
    <text x="95" y="380" fill="#bfdbfe" font-family="sans-serif" font-size="15" font-weight="800" text-anchor="middle">Glassware</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 9. Scatter Plot
SVGS["ini-cet-2021-community-medicine-q012"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#030712"/>

  <!-- Top Title Pill -->
  <rect x="220" y="40" width="560" height="46" rx="23" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="70" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">SUBGROUP BIVARIATE CORRELATION SCATTERGRAM</text>

  <text x="500" y="120" fill="#94a3b8" font-family="sans-serif" font-size="15" text-anchor="middle">Four Homogenous Population Samples: Height (X) vs. Weight (Y)</text>

  <!-- Plot Axes Centered -->
  <line x1="140" y1="800" x2="880" y2="800" stroke="#64748b" stroke-width="3"/>
  <line x1="140" y1="800" x2="140" y2="160" stroke="#64748b" stroke-width="3"/>
  <polygon points="885,800 870,792 870,808" fill="#64748b"/>
  <polygon points="140,155 132,170 148,170" fill="#64748b"/>

  <text x="510" y="845" fill="#f8fafc" font-family="sans-serif" font-size="17" font-weight="700" text-anchor="middle">HEIGHT (X)</text>
  <text x="80" y="480" fill="#f8fafc" font-family="sans-serif" font-size="17" font-weight="700" text-anchor="middle" transform="rotate(-90, 80, 480)">WEIGHT (Y)</text>

  <!-- Common Linear Trend Guide Line -->
  <line x1="220" y1="720" x2="780" y2="240" stroke="#64748b" stroke-width="2" stroke-dasharray="6,6" opacity="0.6"/>

  <!-- 4 Colored Groups Plotted with r=0.6 -->
  <!-- Group 1: Red -->
  <g fill="#ef4444">
    <circle cx="250" cy="700" r="5"/><circle cx="280" cy="680" r="6"/><circle cx="260" cy="660" r="5"/><circle cx="310" cy="690" r="5.5"/>
    <circle cx="290" cy="640" r="6"/><circle cx="320" cy="650" r="5"/><circle cx="340" cy="620" r="6"/><circle cx="350" cy="670" r="5"/>
    <circle cx="270" cy="710" r="4.5"/><circle cx="300" cy="670" r="5.5"/><circle cx="330" cy="700" r="5"/><circle cx="315" cy="630" r="6"/>
  </g>

  <!-- Group 2: Green -->
  <g fill="#10b981">
    <circle cx="380" cy="590" r="5"/><circle cx="410" cy="560" r="6"/><circle cx="390" cy="530" r="5.5"/><circle cx="430" cy="580" r="5"/>
    <circle cx="440" cy="520" r="6"/><circle cx="460" cy="550" r="5.5"/><circle cx="420" cy="500" r="6"/><circle cx="470" cy="570" r="5"/>
    <circle cx="400" cy="600" r="4.5"/><circle cx="450" cy="540" r="5.5"/><circle cx="480" cy="510" r="5"/><circle cx="435" cy="555" r="6"/>
  </g>

  <!-- Group 3: Blue -->
  <g fill="#3b82f6">
    <circle cx="510" cy="470" r="5"/><circle cx="540" cy="440" r="6"/><circle cx="520" cy="410" r="5.5"/><circle cx="560" cy="460" r="5"/>
    <circle cx="570" cy="400" r="6"/><circle cx="590" cy="430" r="5.5"/><circle cx="550" cy="380" r="6"/><circle cx="600" cy="450" r="5"/>
    <circle cx="530" cy="480" r="4.5"/><circle cx="580" cy="420" r="5.5"/><circle cx="610" cy="390" r="5"/><circle cx="565" cy="435" r="6"/>
  </g>

  <!-- Group 4: Orange -->
  <g fill="#f59e0b">
    <circle cx="650" cy="350" r="5"/><circle cx="680" cy="320" r="6"/><circle cx="660" cy="290" r="5.5"/><circle cx="700" cy="340" r="5"/>
    <circle cx="710" cy="280" r="6"/><circle cx="730" cy="310" r="5.5"/><circle cx="690" cy="260" r="6"/><circle cx="740" cy="330" r="5"/>
    <circle cx="670" cy="360" r="4.5"/><circle cx="720" cy="300" r="5.5"/><circle cx="750" cy="270" r="5"/><circle cx="705" cy="315" r="6"/>
  </g>

  <!-- Group Legend Boxes -->
  <g transform="translate(180, 890)">
    <circle cx="10" cy="10" r="8" fill="#ef4444"/>
    <text x="25" y="16" fill="#cbd5e1" font-family="sans-serif" font-size="15" font-weight="600">Sample 1: r₁ = 0.6</text>
    
    <circle cx="180" cy="10" r="8" fill="#10b981"/>
    <text x="195" y="16" fill="#cbd5e1" font-family="sans-serif" font-size="15" font-weight="600">Sample 2: r₂ = 0.6</text>

    <circle cx="350" cy="10" r="8" fill="#3b82f6"/>
    <text x="365" y="16" fill="#cbd5e1" font-family="sans-serif" font-size="15" font-weight="600">Sample 3: r₃ = 0.6</text>

    <circle cx="520" cy="10" r="8" fill="#f59e0b"/>
    <text x="535" y="16" fill="#cbd5e1" font-family="sans-serif" font-size="15" font-weight="600">Sample 4: r₄ = 0.6</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 10. Flow Cytometry Workstation Display
SVGS["ini-cet-2021-community-medicine-q013"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#030712"/>

  <!-- Top Title Pill -->
  <rect x="200" y="40" width="600" height="48" rx="24" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="71" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">FLOW CYTOMETRY DATA ACQUISITION WORKSTATION</text>

  <text x="500" y="125" fill="#94a3b8" font-family="sans-serif" font-size="16" text-anchor="middle">Graphical Data Representations: Panel A and Panel B</text>

  <!-- Panel A: Data Plot 1 -->
  <g transform="translate(60, 160)">
    <rect width="410" height="660" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="20" y="20" width="110" height="36" rx="6" fill="#1e293b"/>
    <text x="75" y="45" fill="#38bdf8" font-family="sans-serif" font-size="18" font-weight="800" text-anchor="middle">PANEL A</text>
    
    <!-- Coordinate axes -->
    <line x1="60" y1="560" x2="380" y2="560" stroke="#64748b" stroke-width="2.5"/>
    <line x1="60" y1="560" x2="60" y2="100" stroke="#64748b" stroke-width="2.5"/>
    
    <text x="220" y="605" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">Forward Scatter (FSC - Cell Size)</text>
    <text x="20" y="330" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle" transform="rotate(-90, 20, 330)">Side Scatter (SSC - Granularity)</text>

    <!-- Leukocyte Populations with Gate Outlines -->
    <ellipse cx="130" cy="490" rx="40" ry="30" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,3"/>
    <g fill="#38bdf8">
      <circle cx="120" cy="490" r="3.5"/><circle cx="130" cy="480" r="3"/><circle cx="140" cy="500" r="4"/><circle cx="125" cy="470" r="3"/>
      <circle cx="135" cy="495" r="2.5"/><circle cx="145" cy="485" r="3"/><circle cx="115" cy="485" r="3"/>
    </g>
    <text x="130" y="445" fill="#38bdf8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">Gate R1</text>

    <ellipse cx="220" cy="380" rx="35" ry="30" fill="none" stroke="#10b981" stroke-width="2" stroke-dasharray="4,3"/>
    <g fill="#10b981">
      <circle cx="210" cy="380" r="3.5"/><circle cx="220" cy="370" r="4"/><circle cx="230" cy="390" r="3"/><circle cx="215" cy="365" r="3.5"/>
    </g>
    <text x="220" y="335" fill="#10b981" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">Gate R2</text>

    <ellipse cx="290" cy="220" rx="55" ry="45" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,3"/>
    <g fill="#f59e0b">
      <circle cx="270" cy="220" r="3.5"/><circle cx="290" cy="210" r="4"/><circle cx="280" cy="240" r="3"/><circle cx="310" cy="230" r="3.5"/>
      <circle cx="300" cy="200" r="4"/><circle cx="265" cy="235" r="3"/><circle cx="315" cy="215" r="3.5"/>
    </g>
    <text x="290" y="165" fill="#f59e0b" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">Gate R3</text>
  </g>

  <!-- Panel B: Data Plot 2 -->
  <g transform="translate(530, 160)">
    <rect width="410" height="660" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="20" y="20" width="110" height="36" rx="6" fill="#1e293b"/>
    <text x="75" y="45" fill="#38bdf8" font-family="sans-serif" font-size="18" font-weight="800" text-anchor="middle">PANEL B</text>

    <line x1="60" y1="560" x2="380" y2="560" stroke="#64748b" stroke-width="2.5"/>
    <line x1="60" y1="560" x2="60" y2="100" stroke="#64748b" stroke-width="2.5"/>

    <text x="220" y="605" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">Fluorescence Intensity (Log Scale)</text>
    <text x="20" y="330" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle" transform="rotate(-90, 20, 330)">Cell Count (Events)</text>

    <!-- Bimodal Fluorescence Peaks Curve -->
    <path d="M 60 560 
             Q 90 560 120 380 
             Q 150 250 180 380 
             Q 210 530 240 545 
             Q 280 545 310 300 
             Q 340 180 360 340 
             Q 375 560 380 560 Z" 
          fill="#38bdf8" fill-opacity="0.25" stroke="#38bdf8" stroke-width="3"/>
    
    <text x="150" y="230" fill="#cbd5e1" font-family="sans-serif" font-size="13" text-anchor="middle">Peak 1</text>
    <text x="335" y="160" fill="#cbd5e1" font-family="sans-serif" font-size="13" text-anchor="middle">Peak 2</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 11. Skewness Distribution Curves
SVGS["ini-cet-2021-community-medicine-q015"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#030712"/>

  <!-- Top Title Pill -->
  <rect x="220" y="40" width="560" height="46" rx="23" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="70" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">STATISTICAL DISTRIBUTION FREQUENCY CURVES</text>

  <!-- 4-Panel Grid Labeled Neutrally 1, 2, 3, 4 Expanded Vertically -->
  <!-- Panel 1 (Top Left) -->
  <g transform="translate(60, 130)">
    <rect width="410" height="370" rx="12" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="20" y="20" width="70" height="35" rx="6" fill="#1e293b"/>
    <text x="55" y="44" fill="#38bdf8" font-family="sans-serif" font-size="18" font-weight="900" text-anchor="middle">1</text>
    
    <line x1="40" y1="300" x2="370" y2="300" stroke="#64748b" stroke-width="2"/>
    <path d="M 50 300 Q 120 300 160 220 Q 205 90 250 220 Q 290 300 360 300" fill="none" stroke="#38bdf8" stroke-width="3.5"/>
    <line x1="205" y1="90" x2="205" y2="300" stroke="#f8fafc" stroke-width="2" stroke-dasharray="4,3"/>
    <text x="205" y="335" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="600" text-anchor="middle">Central Tendency Point</text>
  </g>

  <!-- Panel 2 (Top Right) -->
  <g transform="translate(530, 130)">
    <rect width="410" height="370" rx="12" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="20" y="20" width="70" height="35" rx="6" fill="#1e293b"/>
    <text x="55" y="44" fill="#38bdf8" font-family="sans-serif" font-size="18" font-weight="900" text-anchor="middle">2</text>
    
    <line x1="40" y1="300" x2="370" y2="300" stroke="#64748b" stroke-width="2"/>
    <path d="M 50 300 Q 90 300 120 170 Q 140 90 170 150 Q 240 270 360 300" fill="none" stroke="#38bdf8" stroke-width="3.5"/>
    <line x1="140" y1="90" x2="140" y2="300" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="170" y1="150" x2="170" y2="300" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="210" y1="220" x2="210" y2="300" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
    <text x="140" y="330" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">A</text>
    <text x="170" y="330" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">B</text>
    <text x="210" y="330" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">C</text>
  </g>

  <!-- Panel 3 (Bottom Left) -->
  <g transform="translate(60, 530)">
    <rect width="410" height="370" rx="12" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="20" y="20" width="70" height="35" rx="6" fill="#1e293b"/>
    <text x="55" y="44" fill="#38bdf8" font-family="sans-serif" font-size="18" font-weight="900" text-anchor="middle">3</text>
    
    <line x1="40" y1="300" x2="370" y2="300" stroke="#64748b" stroke-width="2"/>
    <path d="M 50 300 Q 170 270 240 150 Q 270 90 290 170 Q 320 300 360 300" fill="none" stroke="#38bdf8" stroke-width="3.5"/>
    <line x1="200" y1="220" x2="200" y2="300" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="240" y1="150" x2="240" y2="300" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="270" y1="90" x2="270" y2="300" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
    <text x="200" y="330" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">A</text>
    <text x="240" y="330" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">B</text>
    <text x="270" y="330" fill="#94a3b8" font-family="sans-serif" font-size="12" text-anchor="middle">C</text>
  </g>

  <!-- Panel 4 (Bottom Right) -->
  <g transform="translate(530, 530)">
    <rect width="410" height="370" rx="12" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="20" y="20" width="70" height="35" rx="6" fill="#1e293b"/>
    <text x="55" y="44" fill="#38bdf8" font-family="sans-serif" font-size="18" font-weight="900" text-anchor="middle">4</text>
    
    <line x1="40" y1="300" x2="370" y2="300" stroke="#64748b" stroke-width="2"/>
    <path d="M 50 300 Q 100 300 130 220 Q 170 90 210 220 Q 240 300 290 300" fill="none" stroke="#38bdf8" stroke-width="3.5"/>
    <line x1="170" y1="90" x2="170" y2="300" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4,3"/>
    <circle cx="340" cy="300" r="6" fill="#f87171"/>
    <circle cx="368" cy="300" r="6" fill="#f87171"/>
    <text x="354" y="280" fill="#f87171" font-family="sans-serif" font-size="12" text-anchor="middle">Extreme Points</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 12. Kata Thermometer
SVGS["neet-pg-2021-community-medicine-q001"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="q1Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="bulbGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="40%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>
    <linearGradient id="spiritGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#b91c1c"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" fill="url(#q1Bg)"/>

  <!-- Top Title Pill -->
  <rect x="200" y="40" width="600" height="48" rx="24" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="71" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">ENVIRONMENTAL HEALTH INSTRUMENTATION</text>

  <text x="500" y="125" fill="#94a3b8" font-family="sans-serif" font-size="16" text-anchor="middle">Physical Hygiene &amp; Workplace Ventilation Assessment Apparatus</text>

  <!-- Thermometer Glass Stem Apparatus Centered -->
  <g transform="translate(320, 170)">
    <!-- Top Small Reservoir Bulb -->
    <ellipse cx="50" cy="50" rx="32" ry="26" fill="#e2e8f0" opacity="0.8" stroke="#94a3b8" stroke-width="2.5"/>
    <ellipse cx="50" cy="50" rx="18" ry="14" fill="url(#spiritGrad)"/>

    <!-- Stem Tube -->
    <rect x="35" y="70" width="30" height="500" rx="4" fill="#f8fafc" opacity="0.6" stroke="#94a3b8" stroke-width="2.5"/>
    <!-- Liquid Column Inside -->
    <rect x="46" y="200" width="8" height="390" fill="url(#spiritGrad)"/>

    <!-- Large Cylindrical Silvered Lower Bulb -->
    <rect x="23" y="560" width="54" height="200" rx="27" fill="url(#bulbGrad)" stroke="#cbd5e1" stroke-width="3"/>
    
    <!-- Scale Graduations on Stem (Only marked 95°F and 100°F) -->
    <!-- 100°F (37.8°C) Mark -->
    <line x1="20" y1="230" x2="65" y2="230" stroke="#f8fafc" stroke-width="3"/>
    <text x="80" y="236" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="800">100°F (37.8°C)</text>

    <!-- 95°F (35°C) Mark -->
    <line x1="20" y1="390" x2="65" y2="390" stroke="#f8fafc" stroke-width="3"/>
    <text x="80" y="396" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="800">95°F (35.0°C)</text>

    <!-- Bracket for Cooling Time -->
    <path d="M 230 230 L 250 230 L 250 310 L 265 310 L 250 310 L 250 390 L 230 390" fill="none" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="280" y="307" fill="#38bdf8" font-family="sans-serif" font-size="16" font-weight="700">Time Interval (T)</text>
    <text x="280" y="330" fill="#94a3b8" font-family="sans-serif" font-size="14">100°F to 95°F</text>
  </g>

  <!-- Digital Stopwatch Vector -->
  <g transform="translate(680, 520)">
    <circle cx="60" cy="80" r="60" fill="#0f172a" stroke="#64748b" stroke-width="4"/>
    <rect x="52" y="10" width="16" height="15" rx="2" fill="#94a3b8"/>
    <text x="60" y="90" fill="#f8fafc" font-family="monospace" font-size="22" font-weight="800" text-anchor="middle">00:48</text>
    <text x="60" y="165" fill="#94a3b8" font-family="sans-serif" font-size="13" text-anchor="middle">Stopwatch Timer</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 13. Rat Flea Vector Specimen
SVGS["neet-pg-2021-community-medicine-q002"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="fleaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#d97706"/>
      <stop offset="60%" stop-color="#b45309"/>
      <stop offset="100%" stop-color="#78350f"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" fill="#030712"/>

  <!-- Top Title Pill -->
  <rect x="200" y="40" width="600" height="48" rx="24" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="71" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">MEDICAL ENTOMOLOGY MICROSCOPIC SPECIMEN</text>

  <text x="500" y="125" fill="#94a3b8" font-family="sans-serif" font-size="16" text-anchor="middle">Whole Mount Slide Preparation (Lateral Profile View)</text>

  <!-- Microscope Field Circle Centered & Expanded -->
  <circle cx="500" cy="520" r="370" fill="#090d16" stroke="#1e293b" stroke-width="3"/>

  <!-- Flea Body Profile (Laterally Compressed) -->
  <g transform="translate(180, 170)">
    <!-- Abdomen Segments -->
    <path d="M 320 280 C 440 260, 520 340, 500 480 C 480 600, 360 620, 240 580 C 220 540, 230 460, 260 380 Z" fill="url(#fleaGrad)" stroke="#451a03" stroke-width="3"/>
    
    <path d="M 280 340 Q 380 380 470 380" stroke="#451a03" stroke-width="2.5" fill="none"/>
    <path d="M 260 410 Q 360 440 480 430" stroke="#451a03" stroke-width="2.5" fill="none"/>
    <path d="M 250 470 Q 350 500 460 490" stroke="#451a03" stroke-width="2.5" fill="none"/>
    <path d="M 240 530 Q 330 550 430 540" stroke="#451a03" stroke-width="2.5" fill="none"/>

    <!-- Thorax Segments -->
    <path d="M 220 280 L 320 280 L 260 390 L 180 380 Z" fill="url(#fleaGrad)" stroke="#451a03" stroke-width="3"/>

    <!-- Head: Smooth rounded anterior margin -->
    <path d="M 140 320 C 120 290, 140 250, 180 250 C 220 250, 230 280, 220 330 Z" fill="url(#fleaGrad)" stroke="#451a03" stroke-width="3"/>
    <circle cx="155" cy="275" r="5" fill="#000"/>
    
    <!-- Mouthparts -->
    <line x1="140" y1="320" x2="110" y2="390" stroke="#78350f" stroke-width="3"/>
    <line x1="145" y1="320" x2="125" y2="395" stroke="#78350f" stroke-width="2.5"/>

    <!-- Long Saltatorial Hind Jumping Leg -->
    <ellipse cx="280" cy="460" rx="35" ry="55" fill="url(#fleaGrad)" stroke="#451a03" stroke-width="2.5" transform="rotate(25, 280, 460)"/>
    <line x1="300" y1="500" x2="380" y2="620" stroke="#92400e" stroke-width="8"/>
    <line x1="380" y1="620" x2="480" y2="700" stroke="#92400e" stroke-width="6"/>
    <line x1="480" y1="700" x2="560" y2="740" stroke="#78350f" stroke-width="4"/>

    <!-- Middle & Front Legs -->
    <line x1="220" y1="380" x2="190" y2="480" stroke="#92400e" stroke-width="5"/>
    <line x1="190" y1="480" x2="220" y2="560" stroke="#92400e" stroke-width="4"/>
    <line x1="170" y1="360" x2="130" y2="450" stroke="#92400e" stroke-width="5"/>

    <!-- Spermatheca -->
    <path d="M 430 460 Q 450 440 460 460 Q 450 480 435 470 Z" fill="#451a03"/>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# 14. Delhi AQI Telemetry Table
SVGS["neet-pg-2021-community-medicine-q005"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <rect width="1000" height="1000" fill="#030712"/>

  <!-- Top Title Pill -->
  <rect x="180" y="50" width="640" height="48" rx="24" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="81" fill="#38bdf8" font-family="sans-serif" font-size="19" font-weight="700" text-anchor="middle" letter-spacing="1">NATIONAL AIR QUALITY INDEX (NAQI) MONITORING</text>

  <text x="500" y="135" fill="#94a3b8" font-family="sans-serif" font-size="16" text-anchor="middle">Delhi Ambient Air Quality Telemetry Report (4 Consecutive Days)</text>

  <!-- Station Data Table Centered & Expanded -->
  <g transform="translate(80, 180)">
    <rect width="840" height="660" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="0" y="0" width="840" height="75" rx="14" fill="#1e293b"/>
    <text x="420" y="46" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="800" text-anchor="middle">CENTRAL POLLUTION CONTROL BOARD (CPCB) MONITORING DATA</text>

    <!-- Table Header -->
    <text x="80" y="135" fill="#38bdf8" font-family="sans-serif" font-size="17" font-weight="700">Date</text>
    <text x="240" y="135" fill="#38bdf8" font-family="sans-serif" font-size="17" font-weight="700">Station Name</text>
    <text x="460" y="135" fill="#38bdf8" font-family="sans-serif" font-size="17" font-weight="700">PM 2.5 (µg/m³)</text>
    <text x="680" y="135" fill="#38bdf8" font-family="sans-serif" font-size="17" font-weight="700">Calculated AQI</text>
    <line x1="30" y1="165" x2="810" y2="165" stroke="#334155" stroke-width="2"/>

    <!-- Row 1: Nov 20 -->
    <text x="80" y="240" fill="#f8fafc" font-family="sans-serif" font-size="17">November 20</text>
    <text x="240" y="240" fill="#cbd5e1" font-family="sans-serif" font-size="17">Anand Vihar</text>
    <text x="480" y="240" fill="#cbd5e1" font-family="sans-serif" font-size="17">235</text>
    <text x="700" y="240" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="700">342</text>
    <line x1="30" y1="280" x2="810" y2="280" stroke="#1e293b" stroke-width="1.5"/>

    <!-- Row 2: Nov 21 -->
    <text x="80" y="355" fill="#f8fafc" font-family="sans-serif" font-size="17">November 21</text>
    <text x="240" y="355" fill="#cbd5e1" font-family="sans-serif" font-size="17">ITO Station</text>
    <text x="480" y="355" fill="#cbd5e1" font-family="sans-serif" font-size="17">280</text>
    <text x="700" y="355" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="700">388</text>
    <line x1="30" y1="395" x2="810" y2="395" stroke="#1e293b" stroke-width="1.5"/>

    <!-- Row 3: Nov 22 -->
    <text x="80" y="470" fill="#f8fafc" font-family="sans-serif" font-size="17">November 22</text>
    <text x="240" y="470" fill="#cbd5e1" font-family="sans-serif" font-size="17">R.K. Puram</text>
    <text x="480" y="470" fill="#cbd5e1" font-family="sans-serif" font-size="17">295</text>
    <text x="700" y="470" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="700">395</text>
    <line x1="30" y1="510" x2="810" y2="510" stroke="#1e293b" stroke-width="1.5"/>

    <!-- Row 4: Nov 23 (Target Row) -->
    <rect x="20" y="540" width="800" height="85" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
    <text x="80" y="592" fill="#38bdf8" font-family="sans-serif" font-size="18" font-weight="800">November 23</text>
    <text x="240" y="592" fill="#f8fafc" font-family="sans-serif" font-size="18" font-weight="700">Punjabi Bagh</text>
    <text x="480" y="592" fill="#f8fafc" font-family="sans-serif" font-size="18" font-weight="700">355</text>
    <text x="700" y="592" fill="#38bdf8" font-family="sans-serif" font-size="22" font-weight="900">407</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

# Write all 14 SVGs to IMG_DIR
for qid, svg_content in SVGS.items():
    file_path = os.path.join(IMG_DIR, f"medicomm-img1-{qid}.svg")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated clean SVG without prompt banners: medicomm-img1-{qid}.svg")

# Clean /img1 Prompts (Explicitly without question banners)
PROMPTS = {
    "neet-pg-2020-community-medicine-q001": (
        "/img1 Pure medical examination visual for Biomedical Waste Management: "
        "A realistic clinical illustration showing contaminated sharps waste items (disposable hypodermic needle with syringe barrel, "
        "surgical scalpel blade, curved suture needle, and broken glass ampoule shard) arranged on a stainless steel surgical kidney dish. "
        "Strictly the image illustration only: must NOT include question or prompt banners, must NOT show disposal containers, and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    ),
    "neet-pg-2020-community-medicine-q008": (
        "/img1 Pure medical examination visual for Hospital Waste Segregation: "
        "A detailed laboratory bench illustration displaying chemical waste containers: an amber chemical reagent bottle labeled 10% Formalin (Spent Fixative), "
        "a large blue liquid disinfectant carboy (Sodium Hypochlorite solution), and spent chemical solvent bottles with hazard diamonds. "
        "Strictly the image illustration only: must NOT include question or prompt banners, must NOT show disposal bags, and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    ),
    "neet-pg-2020-community-medicine-q012": (
        "/img1 Pure biostatistics examination visual of a Gaussian Normal Distribution Curve: "
        "A symmetrical bell-shaped normal curve on a dark background showing Mean (μ) = 200 at the center axis and standardized deviation ticks "
        "along the horizontal axis at 140 (μ-3σ), 160 (μ-2σ), 180 (μ-1σ), 200 (μ), 220 (μ+1σ), 240 (μ+2σ), and 260 (μ+3σ). "
        "Strictly the mathematical curve only: must NOT include question or prompt banners, must NOT shade intervals, and must NOT display percentages or answers. "
        "Single clean medicomm watermark."
    ),
    "neet-pg-2020-community-medicine-q013": (
        "/img1 Pure medical examination visual for Hospital Clinical Waste Segregation: "
        "A four-panel comparative exhibit displaying four common clinical hospital waste items labeled neutrally as Item A (Whole blood CPDA collection bag with tubing), "
        "Item B (Pair of disposable latex examination gloves), Item C (Hypodermic needle and syringe sharps), and Item D (Urinary drainage collector bag with graduated markings). "
        "Strictly the visual exhibit only: must NOT include question or prompt banners, must NOT show colored bins, and must NOT contain answers or hints. "
        "Single clean medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q004": (
        "/img1 Pure examination match-the-following visual for NACO Syndromic STI/RTI Management: "
        "Two-column structured match format: Column I displays four color-coded drug kits labeled Box A: Kit 1 (Grey), Box B: Kit 2 (Green), "
        "Box C: Kit 3 (White), and Box D: Kit 4 (Blue). Column II displays four randomized target clinical syndromes numbered 1 to 4: "
        "1 (Vaginal Discharge / Vaginitis), 2 (Non-Herpetic Genital Ulcer in Penicillin Allergic), 3 (Non-Herpetic Genital Ulcer), and 4 (Urethral/Cervical/Anorectal Discharge). "
        "Strictly the match board only: must NOT include question or prompt banners, must NOT draw matching lines, and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q006": (
        "/img1 Pure epidemiology examination visual of the Natural History of Disease Timeline: "
        "A horizontal progression flowchart displaying the timeline from Point A (Exposure / Infection), through the incubation interval to Point B (Pathological Onset), "
        "leading to a prominently highlighted red marker labeled POINT C with a large question mark [?], followed by Point D (Medical Diagnosis). "
        "Strictly the timeline graph only: must NOT include question or prompt banners, must NOT write 'Onset of Symptoms', and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q007": (
        "/img1 Pure biostatistics examination visual of a Clinical Trial Vaccine Efficacy Forest Plot: "
        "A clean forest plot graph displaying comparator reference line (0) and pre-specified equivalence boundaries (-δ non-inferiority limit and +δ upper limit). "
        "Plots candidate Vaccines A, B, C, D, and E with point estimates and horizontal 95% confidence interval whiskers. "
        "Strictly the statistical graph only: must NOT include question or prompt banners, and must NOT include interpretation boxes or answers. "
        "Single clean medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q011": (
        "/img1 Pure hospital ward examination visual for Biomedical Waste Segregation Bins: "
        "A realistic hospital corridor scene showing four standard pedal bins standing side-by-side labeled only by their bin colors: "
        "Black Bin (General Waste symbol), Yellow Bin (Biohazard symbol), Red Bin (Biohazard symbol), and Blue Bin (Glassware symbol). "
        "Strictly the bins graphic only: must NOT include question or prompt banners, must NOT list specific items, and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q012": (
        "/img1 Pure biostatistics examination visual of a Subgroup Bivariate Scattergram: "
        "Cartesian coordinate scatter plot of Height (X axis) versus Weight (Y axis) showing data points partitioned into four distinct homogenous color clusters: "
        "Sample 1 (r1 = 0.6), Sample 2 (r2 = 0.6), Sample 3 (r3 = 0.6), and Sample 4 (r4 = 0.6) along a linear regression trend. "
        "Strictly the scatter plot only: must NOT include question or prompt banners, and must NOT show calculation formulas or answers. "
        "Single clean medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q013": (
        "/img1 Pure laboratory examination visual of a Flow Cytometry Data Acquisition Display: "
        "A dual-panel flow cytometry software monitor: Panel A displays a 2D bivariate plot of Forward Scatter (FSC - Cell Size) versus Side Scatter (SSC - Internal Granularity) "
        "with gated cell populations labeled R1, R2, and R3. Panel B displays a curve plotting Cell Count (Events) against Fluorescence Intensity (Log Scale). "
        "Strictly the instrument monitor only: must NOT include question or prompt banners, and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    ),
    "ini-cet-2021-community-medicine-q015": (
        "/img1 Pure biostatistics examination visual of Four Frequency Distribution Curves: "
        "A comparative four-panel grid labeled neutrally as Graph 1, Graph 2, Graph 3, and Graph 4 displaying different distribution shapes: "
        "Graph 1 (Symmetrical bell curve), Graph 2 (Asymmetrical curve with peak on left and tail to the right), Graph 3 (Asymmetrical curve with tail to the left and peak on the right), "
        "and Graph 4 (Symmetrical curve with isolated extreme outlier data points plotted on the baseline). "
        "Strictly the distribution curves only: must NOT include question or prompt banners, and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    ),
    "neet-pg-2021-community-medicine-q001": (
        "/img1 Pure environmental hygiene examination visual of a Specialized Ventilation Thermometer: "
        "An accurate technical illustration of an environmental hygiene thermometer featuring a top reservoir bulb, glass capillary stem with only two graduation marks "
        "at 100°F (37.8°C) and 95°F (35.0°C), a red spirit column, and a large cylindrical silvered lower bulb (4 cm × 2 cm). Beside it, a digital stopwatch timing the interval. "
        "Strictly the physical apparatus only: must NOT include question or prompt banners, must NOT print instrument names, and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    ),
    "neet-pg-2021-community-medicine-q002": (
        "/img1 Pure medical entomology examination visual of an Arthropod Vector Specimen: "
        "A detailed whole mount microscopic preparation (lateral profile view) inside a circular microscope field displaying a flea specimen: "
        "Laterally compressed body, smooth rounded conical head, lack of genal and pronotal combs (smooth borders), thorax with vertical mesopleural suture, "
        "comma-shaped spermatheca in the abdomen, and enlarged saltatorial jumping hind legs. "
        "Strictly the microscopic slide only: must NOT include question or prompt banners, must NOT print species names, and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    ),
    "neet-pg-2021-community-medicine-q005": (
        "/img1 Pure environmental health examination visual of Ambient Air Quality Telemetry Data: "
        "A formal ambient air monitoring data table from the Central Pollution Control Board (CPCB) Delhi monitoring stations for four consecutive days: "
        "Nov 20 (Anand Vihar, PM2.5 = 235, AQI = 342), Nov 21 (ITO, PM2.5 = 280, AQI = 388), Nov 22 (R.K. Puram, PM2.5 = 295, AQI = 395), "
        "and Nov 23 (Punjabi Bagh, PM2.5 = 355, AQI = 407, highlighted row). "
        "Strictly the raw data telemetry table only: must NOT include question or prompt banners, must NOT include category columns, and must NOT reveal answers or hints. "
        "Single clean medicomm watermark."
    )
}

# Save prompts.json
prompts_file = os.path.join(IMG_DIR, "prompts.json")
with open(prompts_file, "w", encoding="utf-8") as f:
    json.dump(PROMPTS, f, indent=2)
print("Saved prompts.json")

# Update question-details.json
details_file = os.path.join(IMG_DIR, "question-details.json")
with open(details_file, "r", encoding="utf-8") as f:
    details = json.load(f)

for item in details:
    qid = item["id"]
    item["img1Prompt"] = PROMPTS.get(qid, "")
    item["svgFilename"] = f"medicomm-img1-{qid}.svg"
    item["uploadedUrl"] = f"/uploads/medicomm-img1-{qid}.svg"

with open(details_file, "w", encoding="utf-8") as f:
    json.dump(details, f, indent=2)
print("Saved question-details.json")

# Copy SVGs to all 4 destinations and brain assets
dest_dirs = [
    os.path.join(BASE_DIR, r"public\uploads"),
    os.path.join(BASE_DIR, r"data\uploads"),
    os.path.join(BASE_DIR, r"dist\uploads"),
    os.path.join(BASE_DIR, r"runtime-data\uploads"),
    BRAIN_ASSETS_DIR
]

for d in dest_dirs:
    os.makedirs(d, exist_ok=True)

for qid in PROMPTS.keys():
    svg_name = f"medicomm-img1-{qid}.svg"
    src_path = os.path.join(IMG_DIR, svg_name)
    if os.path.exists(src_path):
        for d in dest_dirs:
            shutil.copy2(src_path, os.path.join(d, svg_name))
print("Copied all SVGs to all 4 upload dirs and brain assets")

# Update 3 question banks
qb_paths = [
    os.path.join(BASE_DIR, r"data\practice-question-bank.json"),
    os.path.join(BASE_DIR, r"public\practice-question-bank.json"),
    os.path.join(BASE_DIR, r"dist\practice-question-bank.json"),
]

for qb_path in qb_paths:
    if not os.path.exists(qb_path):
        continue
    with open(qb_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = [0]
    def walk_and_update(node):
        if isinstance(node, dict):
            qid = node.get("id")
            if qid in PROMPTS:
                url = f"/uploads/medicomm-img1-{qid}.svg"
                prompt_text = PROMPTS[qid]
                node["imageUrls"] = [url]
                node["images"] = [url]
                node["atlasImageTargetUrls"] = [url]
                node["img1Prompt"] = prompt_text
                node["assetNote"] = f"/img1 Prompt: {prompt_text}"
                updated[0] += 1
            for k, v in node.items():
                walk_and_update(v)
        elif isinstance(node, list):
            for item in node:
                walk_and_update(item)

    walk_and_update(data)
    with open(qb_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Updated {updated[0]} nodes in {qb_path}")

# Rebuild HTML review gallery
gallery_html_path = os.path.join(IMG_DIR, "review-gallery.html")

gallery_items_html = []
for idx, item in enumerate(details, 1):
    qid = item["id"]
    year = item["year"]
    exam = item["exam"].upper()
    prompt = item["prompt"].replace("\n", "<br/>")
    ans = item["answer"]
    exp = item["explanation"].replace("\n", "<br/>")
    options = item["options"]
    img1_prompt = PROMPTS.get(qid, "")
    svg_filename = f"medicomm-img1-{qid}.svg"

    opts_html = "".join([
        f'<li class="opt {"opt-correct" if opt == ans else ""}"><strong>{"✓ " if opt == ans else "• "}</strong>{opt}</li>'
        for opt in options
    ])

    gallery_items_html.append(f"""
    <section class="q-card" id="{qid}">
      <div class="q-header">
        <span class="badge exam-badge">{exam}-{year}</span>
        <span class="badge num-badge">#{idx} of {len(details)}</span>
        <span class="qid-code">{qid}</span>
      </div>

      <div class="q-body">
        <div class="q-visual-col">
          <div class="img-wrapper">
            <img src="./{svg_filename}" alt="{qid} visual" loading="lazy" />
          </div>
          <div class="img-meta">
            <span class="file-tag">{svg_filename}</span>
            <span class="watermark-tag">Image Only | No Prompt Boxes | 1x Watermark</span>
          </div>
        </div>

        <div class="q-content-col">
          <div class="q-prompt-box">
            <h4>Question Prompt</h4>
            <p>{prompt}</p>
          </div>

          <div class="q-options-box">
            <h4>Options</h4>
            <ul class="opts-list">
              {opts_html}
            </ul>
          </div>

          <div class="q-exp-box">
            <h4>High-Yield Explanation</h4>
            <p>{exp}</p>
          </div>

          <div class="q-img1-box">
            <div class="img1-header">
              <span class="img1-badge">/img1 Generation Prompt (Pure Image Only)</span>
              <button class="copy-btn" onclick="navigator.clipboard.writeText(this.getAttribute('data-prompt'))" data-prompt="{img1_prompt.replace('"', '&quot;')}">Copy Prompt</button>
            </div>
            <pre class="prompt-text">{img1_prompt}</pre>
          </div>
        </div>
      </div>
    </section>
    """)

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Community Medicine 2020-2021 /img1 Gallery (Pure Images Only) | MediComm</title>
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: #0f172a;
      --card-border: #1e293b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --green: #10b981;
      --amber: #f59e0b;
      --purple: #a855f7;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 60px;
    }}
    header {{
      background: #0b1120;
      border-bottom: 1px solid var(--card-border);
      padding: 24px 40px;
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      backdrop-filter: blur(8px);
    }}
    .brand h1 {{
      font-size: 22px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .brand p {{
      font-size: 13px;
      color: var(--text-muted);
    }}
    .nav-stats {{
      display: flex;
      gap: 12px;
    }}
    .stat-pill {{
      background: #1e293b;
      border: 1px solid #334155;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      color: var(--accent);
    }}
    .container {{
      max-width: 1400px;
      margin: 32px auto;
      padding: 0 24px;
      display: flex;
      flex-direction: column;
      gap: 40px;
    }}
    .q-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }}
    .q-header {{
      background: #0b1120;
      border-bottom: 1px solid var(--card-border);
      padding: 14px 24px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .badge {{
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .exam-badge {{ background: #1e3a8a; color: #93c5fd; }}
    .num-badge {{ background: #1e293b; color: #cbd5e1; }}
    .qid-code {{ font-family: monospace; font-size: 13px; color: #64748b; margin-left: auto; }}
    .q-body {{
      display: grid;
      grid-template-columns: 520px 1fr;
      gap: 28px;
      padding: 24px;
    }}
    @media (max-width: 1080px) {{
      .q-body {{ grid-template-columns: 1fr; }}
    }}
    .q-visual-col {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .img-wrapper {{
      background: #030712;
      border: 1px solid #1e293b;
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      aspect-ratio: 1;
    }}
    .img-wrapper img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }}
    .img-meta {{
      display: flex;
      justify-content: space-between;
      font-size: 12px;
    }}
    .file-tag {{ font-family: monospace; color: #64748b; }}
    .watermark-tag {{ color: var(--green); font-weight: 600; }}
    .q-content-col {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .q-prompt-box h4, .q-options-box h4, .q-exp-box h4 {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--accent);
      margin-bottom: 6px;
    }}
    .q-prompt-box p {{
      font-size: 16px;
      font-weight: 600;
      color: #f1f5f9;
    }}
    .opts-list {{
      list-style: none;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}
    .opt {{
      background: #1e293b;
      border: 1px solid #334155;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 14px;
      color: #cbd5e1;
    }}
    .opt-correct {{
      background: rgba(16, 185, 129, 0.15);
      border-color: var(--green);
      color: #a7f3d0;
      font-weight: 700;
    }}
    .q-exp-box {{
      background: #090d16;
      border-left: 3px solid var(--accent);
      padding: 12px 16px;
      border-radius: 0 8px 8px 0;
      font-size: 13.5px;
      color: #cbd5e1;
    }}
    .q-img1-box {{
      background: #060911;
      border: 1px solid #1e293b;
      border-radius: 10px;
      padding: 14px;
      margin-top: auto;
    }}
    .img1-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    .img1-badge {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--amber);
    }}
    .copy-btn {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #e2e8f0;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .copy-btn:hover {{
      background: var(--accent);
      color: #020617;
      border-color: var(--accent);
    }}
    .prompt-text {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 12px;
      color: #94a3b8;
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.45;
    }}
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <h1>Community Medicine (PSM) 2020-2021 /img1 Gallery</h1>
      <p>Pure Medical Visuals Only | All Prompt &amp; Question Banners Removed | Strictly 1x Watermark</p>
    </div>
    <div class="nav-stats">
      <span class="stat-pill">14 Pure Visuals</span>
      <span class="stat-pill" style="color: #10b981;">✓ Zero Prompt Banners</span>
      <span class="stat-pill" style="color: #10b981;">✓ 1x medicomm Watermark</span>
    </div>
  </header>

  <main class="container">
    {"".join(gallery_items_html)}
  </main>
</body>
</html>
"""

with open(gallery_html_path, "w", encoding="utf-8") as f:
    f.write(full_html)
print(f"Generated clean review gallery without prompt banners: {gallery_html_path}")
