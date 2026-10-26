import re
import sys

with open(r"D:\medullaprep\dhruv1\scripts\grand_test\part2_block3.py", "r", encoding="utf-8") as f:
    code = f.read()

# Let's inspect options with brackets
pattern = re.compile(r'"options":\s*\[(.*?)\]', re.DOTALL)
matches = pattern.findall(code)

print(f"Found {len(matches)} options blocks.")
for idx, m in enumerate(matches):
    lines = [line.strip().strip('",') for line in m.split('\n') if line.strip().startswith('"')]
    for opt in lines:
        if '(' in opt:
            # check if numeric or scientific/chemical
            inner = re.findall(r'\((.*?)\)', opt)
            for inn in inner:
                if not any(c.isdigit() for c in inn) and inn.lower() not in ['pge1', 'pge2', 'ck7', 'pas', 'fsh', 'lh', 'tsh', 'hcg', 'b1', 'b6', 'b12', 'ct', 'mri']:
                    print(f"Block question index ~{idx+251}: {opt}")
