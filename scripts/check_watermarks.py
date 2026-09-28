import os
import glob

files = glob.glob(r"d:\medicomm\dhruv1\output\imagegen\community-medicine-2020-2021-img1\*.svg")
print(f"Total SVGs found: {len(files)}")
for f in sorted(files):
    name = os.path.basename(f)
    with open(f, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
    wm_lines = [l.strip() for l in lines if "medicomm" in l.lower()]
    print(f"{name} -> {len(wm_lines)} matches: {wm_lines}")
