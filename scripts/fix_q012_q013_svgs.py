import os

svg_neet_2020_q012 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="q12Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#030712"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="curveFill1SD" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.08"/>
    </linearGradient>
    <linearGradient id="curveFill2SD" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.04"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" fill="url(#q12Bg)"/>

  <!-- Top Title Pill -->
  <rect x="180" y="32" width="640" height="48" rx="24" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="63" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700" text-anchor="middle" letter-spacing="1">GAUSSIAN NORMAL DISTRIBUTION: EMPIRICAL RULE</text>

  <text x="500" y="112" fill="#94a3b8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" text-anchor="middle">Population Parameter Study: Mean (μ) = 200  |  Standard Deviation (σ) = 20</text>

  <!-- Bell Curve Shaded Areas -->
  <!-- 2SD area: 300 to 700 -->
  <path d="M 300 680 C 340 680, 360 620, 400 500 C 440 380, 470 280, 500 280 C 530 280, 560 380, 600 500 C 640 620, 660 680, 700 680 Z" fill="url(#curveFill2SD)"/>

  <!-- 1SD highlighted area: 400 to 600 -->
  <path d="M 400 680 C 420 620, 440 500, 470 340 C 485 285, 495 280, 500 280 C 505 280, 515 285, 530 340 C 560 500, 580 620, 600 680 Z" fill="url(#curveFill1SD)"/>

  <!-- Bell Curve Main Line -->
  <path d="M 120 680 C 180 680, 240 678, 300 660 C 350 635, 380 570, 420 450 C 460 320, 480 280, 500 280 C 520 280, 540 320, 580 450 C 620 570, 650 635, 700 660 C 760 678, 820 680, 880 680" fill="none" stroke="#38bdf8" stroke-width="4"/>

  <!-- Base Baseline Axis -->
  <line x1="100" y1="680" x2="900" y2="680" stroke="#64748b" stroke-width="2.5"/>

  <!-- Vertical Divider Lines for SDs -->
  <!-- Center Mean -->
  <line x1="500" y1="280" x2="500" y2="680" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="6,4"/>
  <circle cx="500" cy="280" r="6" fill="#f59e0b"/>

  <!-- -1 SD (400) and +1 SD (600) -->
  <line x1="400" y1="500" x2="400" y2="680" stroke="#10b981" stroke-width="2" stroke-dasharray="4,4"/>
  <line x1="600" y1="500" x2="600" y2="680" stroke="#10b981" stroke-width="2" stroke-dasharray="4,4"/>

  <!-- -2 SD (300) and +2 SD (700) -->
  <line x1="300" y1="660" x2="300" y2="680" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,3"/>
  <line x1="700" y1="660" x2="700" y2="680" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,3"/>

  <!-- -3 SD (200) and +3 SD (800) -->
  <line x1="200" y1="676" x2="200" y2="680" stroke="#475569" stroke-width="1"/>
  <line x1="800" y1="676" x2="800" y2="680" stroke="#475569" stroke-width="1"/>

  <!-- Axis Labels below baseline -->
  <!-- Labels: Standard deviations -->
  <text x="500" y="705" fill="#f59e0b" font-family="sans-serif" font-size="15" font-weight="700" text-anchor="middle">Mean (μ)</text>
  <text x="500" y="730" fill="#f8fafc" font-family="sans-serif" font-size="20" font-weight="800" text-anchor="middle">200</text>

  <text x="400" y="705" fill="#10b981" font-family="sans-serif" font-size="14" font-weight="600" text-anchor="middle">-1 σ</text>
  <text x="400" y="730" fill="#f8fafc" font-family="sans-serif" font-size="18" font-weight="700" text-anchor="middle">180</text>

  <text x="600" y="705" fill="#10b981" font-family="sans-serif" font-size="14" font-weight="600" text-anchor="middle">+1 σ</text>
  <text x="600" y="730" fill="#f8fafc" font-family="sans-serif" font-size="18" font-weight="700" text-anchor="middle">220</text>

  <text x="300" y="705" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="500" text-anchor="middle">-2 σ</text>
  <text x="300" y="730" fill="#94a3b8" font-family="sans-serif" font-size="16" font-weight="600" text-anchor="middle">160</text>

  <text x="700" y="705" fill="#94a3b8" font-family="sans-serif" font-size="14" font-weight="500" text-anchor="middle">+2 σ</text>
  <text x="700" y="730" fill="#94a3b8" font-family="sans-serif" font-size="16" font-weight="600" text-anchor="middle">240</text>

  <text x="200" y="705" fill="#64748b" font-family="sans-serif" font-size="13" font-weight="500" text-anchor="middle">-3 σ</text>
  <text x="200" y="730" fill="#64748b" font-family="sans-serif" font-size="15" font-weight="600" text-anchor="middle">140</text>

  <text x="800" y="705" fill="#64748b" font-family="sans-serif" font-size="13" font-weight="500" text-anchor="middle">+3 σ</text>
  <text x="800" y="730" fill="#64748b" font-family="sans-serif" font-size="15" font-weight="600" text-anchor="middle">260</text>

  <!-- Percentages inside the curve -->
  <text x="450" y="470" fill="#34d399" font-family="sans-serif" font-size="18" font-weight="700" text-anchor="middle">34.1%</text>
  <text x="550" y="470" fill="#34d399" font-family="sans-serif" font-size="18" font-weight="700" text-anchor="middle">34.1%</text>
  <text x="350" y="580" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="600" text-anchor="middle">13.6%</text>
  <text x="650" y="580" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="600" text-anchor="middle">13.6%</text>
  <text x="250" y="640" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="500" text-anchor="middle">2.1%</text>
  <text x="750" y="640" fill="#94a3b8" font-family="sans-serif" font-size="13" font-weight="500" text-anchor="middle">2.1%</text>

  <!-- Empirical Rule Bracket Callout for 68% -->
  <path d="M 405 210 L 405 190 L 500 190 L 500 175 L 500 190 L 595 190 L 595 210" fill="none" stroke="#10b981" stroke-width="2.5"/>
  <rect x="420" y="145" width="160" height="34" rx="8" fill="#065f46" stroke="#10b981" stroke-width="1.5"/>
  <text x="500" y="168" fill="#a7f3d0" font-family="sans-serif" font-size="16" font-weight="800" text-anchor="middle">68.2% of POPULATION</text>

  <!-- Summary High-Yield Comparison Table Card -->
  <rect x="120" y="760" width="760" height="175" rx="16" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>

  <!-- Row 1: 68% rule (Green Highlighted Box) -->
  <rect x="135" y="775" width="730" height="42" rx="10" fill="#064e3b" stroke="#059669" stroke-width="1.5"/>
  <text x="155" y="802" fill="#34d399" font-family="sans-serif" font-size="16" font-weight="800">✓ μ ± 1 SD (68.27%):</text>
  <text x="350" y="802" fill="#ecfdf5" font-family="sans-serif" font-size="16" font-weight="700">200 ± 20  =  [ 180 to 220 ]</text>
  <text x="740" y="802" fill="#a7f3d0" font-family="sans-serif" font-size="14" font-weight="600" text-anchor="middle">CORRECT ANSWER</text>

  <!-- Row 2: 95% rule -->
  <text x="155" y="845" fill="#38bdf8" font-family="sans-serif" font-size="15" font-weight="700">  μ ± 2 SD (95.45%):</text>
  <text x="350" y="845" fill="#f1f5f9" font-family="sans-serif" font-size="15" font-weight="600">200 ± 40  =  [ 160 to 240 ]</text>
  <text x="740" y="845" fill="#94a3b8" font-family="sans-serif" font-size="14">Two standard deviations</text>

  <!-- Row 3: 99.7% rule -->
  <text x="155" y="885" fill="#c084fc" font-family="sans-serif" font-size="15" font-weight="700">  μ ± 3 SD (99.73%):</text>
  <text x="350" y="885" fill="#f1f5f9" font-family="sans-serif" font-size="15" font-weight="600">200 ± 60  =  [ 140 to 260 ]</text>
  <text x="740" y="885" fill="#94a3b8" font-family="sans-serif" font-size="14">Three standard deviations</text>

  <!-- Key rule footer note -->
  <text x="500" y="922" fill="#64748b" font-family="sans-serif" font-size="13" font-style="italic" text-anchor="middle">Symmetrical Bell Curve: Mean = Median = Mode | Total Area under normal curve = 1 (100%)</text>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

svg_neet_2020_q013 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <linearGradient id="q13Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="yellowBagGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fde047"/>
      <stop offset="60%" stop-color="#eab308"/>
      <stop offset="100%" stop-color="#ca8a04"/>
    </linearGradient>
    <linearGradient id="bloodGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="70%" stop-color="#991b1b"/>
      <stop offset="100%" stop-color="#450a0a"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" fill="url(#q13Bg)"/>

  <!-- Top Title Pill -->
  <rect x="180" y="32" width="640" height="48" rx="24" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
  <text x="500" y="63" fill="#eab308" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700" text-anchor="middle" letter-spacing="1">BIOMEDICAL WASTE: BLOOD BAG DISPOSAL</text>

  <!-- Left: Blood Bag Illustration -->
  <g transform="translate(100, 110)">
    <!-- Blood Bag Card Container -->
    <rect x="0" y="0" width="360" height="480" rx="20" fill="#090d16" stroke="#b91c1c" stroke-width="2"/>
    <text x="180" y="36" fill="#f87171" font-family="sans-serif" font-size="18" font-weight="800" text-anchor="middle">DISCARDED BLOOD BAG</text>

    <!-- Hanging Eyelet -->
    <rect x="155" y="55" width="50" height="16" rx="8" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
    <circle cx="180" cy="63" r="5" fill="#090d16"/>

    <!-- Plastic Blood Pouch Body -->
    <rect x="80" y="80" width="200" height="260" rx="28" fill="#1e293b" stroke="#64748b" stroke-width="2.5" opacity="0.8"/>
    <!-- Liquid Blood Fill inside pouch -->
    <rect x="88" y="140" width="184" height="190" rx="20" fill="url(#bloodGrad)"/>
    <!-- Blood meniscus wave -->
    <path d="M 88 140 Q 130 135 180 142 T 272 140 L 272 170 L 88 170 Z" fill="#b91c1c"/>

    <!-- Pouch Label -->
    <rect x="105" y="170" width="150" height="100" rx="6" fill="#ffffff" opacity="0.95"/>
    <text x="180" y="195" fill="#991b1b" font-family="sans-serif" font-size="14" font-weight="800" text-anchor="middle">WHOLE BLOOD (CPDA)</text>
    <text x="180" y="215" fill="#0f172a" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Unit No: 4092-B+</text>
    <line x1="120" y1="225" x2="240" y2="225" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="180" y="242" fill="#dc2626" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">EXPIRED / CONTAMINATED</text>
    <text x="180" y="258" fill="#475569" font-family="sans-serif" font-size="10" text-anchor="middle">Disposal Category: Biohazard</text>

    <!-- Transfusion Tubing extending down -->
    <path d="M 180 340 L 180 390 C 180 430 240 430 240 460 L 240 480" fill="none" stroke="#ef4444" stroke-width="6" stroke-linecap="round"/>
    <!-- Clamp -->
    <rect x="170" y="375" width="20" height="14" rx="3" fill="#38bdf8"/>

    <!-- Big Directional Arrow -->
    <g transform="translate(370, 220)">
      <path d="M 10 30 L 70 30 L 70 10 L 110 45 L 70 80 L 70 60 L 10 60 Z" fill="#eab308"/>
      <text x="60" y="105" fill="#fef08a" font-family="sans-serif" font-size="13" font-weight="700" text-anchor="middle">DISPOSE INTO</text>
    </g>
  </g>

  <!-- Right: Yellow BMW Biohazard Bag -->
  <g transform="translate(540, 110)">
    <!-- Yellow Bin / Bag Card Container -->
    <rect x="0" y="0" width="380" height="480" rx="20" fill="#090d16" stroke="#ca8a04" stroke-width="2"/>
    <text x="190" y="36" fill="#facc15" font-family="sans-serif" font-size="18" font-weight="800" text-anchor="middle">YELLOW NON-CHLORINATED BAG</text>

    <!-- Realistic Yellow Biohazard Bag Silhouette -->
    <!-- Tied Top Neck -->
    <path d="M 165 65 Q 190 75 215 65 L 205 95 Q 190 90 175 95 Z" fill="#ca8a04"/>
    <ellipse cx="190" cy="70" rx="25" ry="8" fill="#a16207"/>
    <!-- Tie band -->
    <rect x="175" y="90" width="30" height="8" rx="3" fill="#713f12"/>

    <!-- Bag Body Expanding Down -->
    <path d="M 175 95 C 130 110, 60 160, 60 250 C 60 360, 80 430, 100 445 C 130 455, 250 455, 280 445 C 300 430, 320 360, 320 250 C 320 160, 250 110, 205 95 Z" fill="url(#yellowBagGrad)" stroke="#a16207" stroke-width="2"/>

    <!-- Biohazard Symbol Emblem on Bag -->
    <g transform="translate(190, 240) scale(0.85)">
      <circle cx="0" cy="0" r="50" fill="#18181b" opacity="0.9"/>
      <!-- Biohazard Ring and Arcs -->
      <circle cx="0" cy="0" r="30" fill="none" stroke="#facc15" stroke-width="5"/>
      <circle cx="0" cy="-22" r="18" fill="none" stroke="#facc15" stroke-width="5"/>
      <circle cx="-19" cy="11" r="18" fill="none" stroke="#facc15" stroke-width="5"/>
      <circle cx="19" cy="11" r="18" fill="none" stroke="#facc15" stroke-width="5"/>
      <circle cx="0" cy="0" r="10" fill="#facc15"/>
    </g>

    <text x="190" y="325" fill="#18181b" font-family="sans-serif" font-size="20" font-weight="900" text-anchor="middle" letter-spacing="1">BIOHAZARD</text>
    <text x="190" y="350" fill="#713f12" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">INCINERATION ONLY</text>

    <!-- Key Highlight Pill -->
    <rect x="30" y="385" width="320" height="50" rx="10" fill="#18181b" stroke="#facc15" stroke-width="1.5"/>
    <text x="190" y="408" fill="#facc15" font-family="sans-serif" font-size="14" font-weight="800" text-anchor="middle">✓ BLOOD BAGS DISPOSED HERE</text>
    <text x="190" y="425" fill="#e2e8f0" font-family="sans-serif" font-size="12" text-anchor="middle">Non-chlorinated plastic prevents dioxin release</text>
  </g>

  <!-- Bottom Section: High-Yield BMW Classification Comparison -->
  <g transform="translate(80, 620)">
    <rect x="0" y="0" width="840" height="320" rx="18" fill="#090d16" stroke="#334155" stroke-width="1.5"/>
    <text x="420" y="36" fill="#38bdf8" font-family="sans-serif" font-size="18" font-weight="800" text-anchor="middle">BIOMEDICAL WASTE (BMW) MANAGEMENT - COLOR CODING COMPARISON</text>

    <!-- 4 Category Cards -->
    <!-- YELLOW -->
    <g transform="translate(20, 55)">
      <rect x="0" y="0" width="190" height="190" rx="12" fill="#1c1917" stroke="#eab308" stroke-width="2"/>
      <rect x="0" y="0" width="190" height="34" rx="12" fill="#ca8a04"/>
      <text x="95" y="23" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="800" text-anchor="middle">YELLOW BAG</text>
      
      <text x="15" y="58" fill="#fde047" font-family="sans-serif" font-size="12" font-weight="700">• BLOOD BAGS (Key!)</text>
      <text x="15" y="78" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• Human tissues / organs</text>
      <text x="15" y="98" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• Soiled cotton / gauze</text>
      <text x="15" y="118" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• Expired cytotoxics</text>
      <text x="15" y="138" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• Microbiology cultures</text>

      <rect x="10" y="152" width="170" height="28" rx="6" fill="#854d0e"/>
      <text x="95" y="171" fill="#fef08a" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Incineration / Deep Burial</text>
    </g>

    <!-- RED -->
    <g transform="translate(225, 55)">
      <rect x="0" y="0" width="190" height="190" rx="12" fill="#1c1917" stroke="#ef4444" stroke-width="1.5"/>
      <rect x="0" y="0" width="190" height="34" rx="12" fill="#dc2626"/>
      <text x="95" y="23" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="800" text-anchor="middle">RED BAG</text>
      
      <text x="15" y="58" fill="#fca5a5" font-family="sans-serif" font-size="12" font-weight="700">• URINE BAGS (Key!)</text>
      <text x="15" y="78" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• IV bottles &amp; tubings</text>
      <text x="15" y="98" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• Catheters &amp; syringes</text>
      <text x="15" y="118" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• Gloves &amp; vacutainers</text>
      <text x="15" y="138" fill="#94a3b8" font-family="sans-serif" font-size="11">(Recyclable plastics)</text>

      <rect x="10" y="152" width="170" height="28" rx="6" fill="#7f1d1d"/>
      <text x="95" y="171" fill="#fecaca" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Autoclave + Shredding</text>
    </g>

    <!-- WHITE -->
    <g transform="translate(430, 55)">
      <rect x="0" y="0" width="190" height="190" rx="12" fill="#1c1917" stroke="#94a3b8" stroke-width="1.5"/>
      <rect x="0" y="0" width="190" height="34" rx="12" fill="#64748b"/>
      <text x="95" y="23" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="800" text-anchor="middle">WHITE CONTAINER</text>
      
      <text x="15" y="58" fill="#e2e8f0" font-family="sans-serif" font-size="12" font-weight="700">• SHARPS WASTE</text>
      <text x="15" y="78" fill="#cbd5e1" font-family="sans-serif" font-size="11.5">• Needles &amp; scalpels</text>
      <text x="15" y="98" fill="#cbd5e1" font-family="sans-serif" font-size="11.5">• Surgical blades</text>
      <text x="15" y="118" fill="#cbd5e1" font-family="sans-serif" font-size="11.5">• Fixed-needle syringes</text>
      <text x="15" y="138" fill="#94a3b8" font-family="sans-serif" font-size="11">(Puncture-proof)</text>

      <rect x="10" y="152" width="170" height="28" rx="6" fill="#334155"/>
      <text x="95" y="171" fill="#e2e8f0" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Autoclave / Encapsulation</text>
    </g>

    <!-- BLUE -->
    <g transform="translate(635, 55)">
      <rect x="0" y="0" width="185" height="190" rx="12" fill="#1c1917" stroke="#3b82f6" stroke-width="1.5"/>
      <rect x="0" y="0" width="185" height="34" rx="12" fill="#2563eb"/>
      <text x="92" y="23" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="800" text-anchor="middle">BLUE BOX / BIN</text>
      
      <text x="15" y="58" fill="#93c5fd" font-family="sans-serif" font-size="12" font-weight="700">• GLASSWARE</text>
      <text x="15" y="78" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• Medicine vials/ampoules</text>
      <text x="15" y="98" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• Broken glass articles</text>
      <text x="15" y="118" fill="#e2e8f0" font-family="sans-serif" font-size="11.5">• Metallic orthopedic pins</text>
      <text x="15" y="138" fill="#94a3b8" font-family="sans-serif" font-size="11">(Cardboard box/bin)</text>

      <rect x="10" y="152" width="165" height="28" rx="6" fill="#1e3a8a"/>
      <text x="92" y="171" fill="#bfdbfe" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Disinfection / Autoclave</text>
    </g>

    <!-- High-Yield Callout Banner -->
    <rect x="20" y="260" width="800" height="46" rx="8" fill="#78350f" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="420" y="289" fill="#fef3c7" font-family="sans-serif" font-size="14" font-weight="700" text-anchor="middle">⚡ CRITICAL NEET-PG TRAP: BLOOD BAGS → YELLOW BAG  |  URINE BAGS → RED BAG</text>
  </g>

  <!-- Single Watermark -->
  <text x="40" y="970" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="500" letter-spacing="1">medicomm</text>
</svg>"""

out_dir = r"d:\medicomm\dhruv1\output\imagegen\community-medicine-2020-2021-img1"
with open(os.path.join(out_dir, "medicomm-img1-neet-pg-2020-community-medicine-q012.svg"), "w", encoding="utf-8") as f:
    f.write(svg_neet_2020_q012)
print("Updated medicomm-img1-neet-pg-2020-community-medicine-q012.svg")

with open(os.path.join(out_dir, "medicomm-img1-neet-pg-2020-community-medicine-q013.svg"), "w", encoding="utf-8") as f:
    f.write(svg_neet_2020_q013)
print("Updated medicomm-img1-neet-pg-2020-community-medicine-q013.svg")
