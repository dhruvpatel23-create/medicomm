import subprocess

def run(cmd):
    p = subprocess.run(cmd, cwd=r"D:\medullaprep\dhruv1", capture_output=True, text=True)
    return p.stdout.strip()

print("--- MODIFIED TRACKED FILES ---")
print(run(["git", "diff-files", "--name-status"]))

print("\n--- UNTRACKED FILES ---")
untracked = run(["git", "ls-files", "--others", "--exclude-standard"]).splitlines()
print(f"Total untracked: {len(untracked)}")
for f in untracked[:30]:
    print(" ", f)
