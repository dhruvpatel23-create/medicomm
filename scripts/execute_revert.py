import shutil
from pathlib import Path
import json

ROOT = Path(r"d:\medullaprep\dhruv1")
BACKUP = ROOT / "output" / "imagegen" / "ophthalmology-2017-2019-img1" / "backups" / "20261009T165020Z"

print(f"Using backup from: {BACKUP}")

# 1. Restore question bank files from backup
shutil.copy2(BACKUP / "data-practice-question-bank.json", ROOT / "data" / "practice-question-bank.json")
shutil.copy2(BACKUP / "public-practice-question-bank.json", ROOT / "public" / "practice-question-bank.json")
shutil.copy2(BACKUP / "dist-practice-question-bank.json", ROOT / "dist" / "practice-question-bank.json")
print("Restored practice-question-bank.json in data, public, dist.")

# 2. Delete installed 2017-2019 ophthalmology images from all 4 upload directories
manifest_path = ROOT / "output" / "imagegen" / "ophthalmology-2017-2019-img1" / "installed-manifest.json"
if manifest_path.is_file():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    deleted_count = 0
    for item in manifest.get("images", []):
        filename = item["filename"]
        atlas_alias = filename.replace("medicomm-img1-", "medicomm-atlas-")
        for d in ["public", "data", "dist", "runtime-data"]:
            f1 = ROOT / d / "uploads" / filename
            f2 = ROOT / d / "uploads" / atlas_alias
            if f1.is_file():
                f1.unlink()
                deleted_count += 1
            if f2.is_file():
                f2.unlink()
                deleted_count += 1
    print(f"Deleted {deleted_count} generated image files from upload directories.")

# 3. Update cache key in src/App.jsx to bust browser cache
app_file = ROOT / "src" / "App.jsx"
content = app_file.read_text(encoding="utf-8")
for line in content.splitlines():
    if "const PRACTICE_LIBRARY_CACHE_KEY =" in line:
        old_line = line
        new_line = 'const PRACTICE_LIBRARY_CACHE_KEY = "medicomm-practice-library-cache-v20261010-revert-oph-2017-2019";'
        content = content.replace(old_line, new_line)
        print(f"Updated cache key from:\n  {old_line}\nto:\n  {new_line}")
        break

app_file.write_text(content, encoding="utf-8")
print("Successfully reverted all changes to 2017-2019 ophthalmology images.")
