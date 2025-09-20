import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FILE = "plan-data.json"
COMMIT_MESSAGE = "auto: push on plan-data.json change"

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(WATCHED_FILE):
            print(f"{WATCHED_FILE} has been modified. Reading content with cp1256 encoding...")
            try:
                with open(WATCHED_FILE, "r", encoding="cp1256") as f:
                    data = f.read()
                print("File content read successfully (no Unicode errors).")
            except Exception as e:
                print(f"Error reading file: {e}")
                return

            try:
                subprocess.run(["git", "add", WATCHED_FILE], check=True)
                subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
                subprocess.run(["git", "push"], check=True)
                print("Changes pushed to git.")
            except subprocess.CalledProcessError as e:
                print(f"Git command failed: {e}")

if __name__ == "__main__":
    print(f"Watching file: {WATCHED_FILE}")
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()