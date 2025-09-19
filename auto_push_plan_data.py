import time
import hashlib
import subprocess
import os

FILE = "plan-data.json"
SLEEP = 30  # seconds

def get_file_hash(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

last_hash = get_file_hash(FILE)

while True:
    time.sleep(SLEEP)
    current_hash = get_file_hash(FILE)
    if last_hash != current_hash and current_hash != "":
        print(f"Detected change in {FILE}. Pushing to GitHub...")
        subprocess.run(["git", "add", FILE])
        subprocess.run(["git", "commit", "-m", "Auto-update plan-data.json"])
        subprocess.run(["git", "push"])
        last_hash = current_hash
    else:
        print(f"No change in {FILE}. Monitoring...")