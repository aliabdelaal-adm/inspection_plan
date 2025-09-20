import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FILE = "plan-data.json"
COMMIT_MESSAGE = "auto: push on plan-data.json change"

# قائمة الترميزات الشائعة للمحاولة
ENCODINGS = ["utf-8", "windows-1256", "cp1256", "cp1252", "latin1"]

def read_file_with_best_encoding(filepath):
    for encoding in ENCODINGS:
        try:
            with open(filepath, "r", encoding=encoding) as f:
                data = f.read()
            print(f"تمت قراءة الملف بنجاح باستخدام الترميز: {encoding}")
            return data, encoding
        except Exception as e:
            print(f"فشل الترميز {encoding}: {e}")
    print("لم ينجح أي ترميز في قراءة الملف.")
    return None, None

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.file_encoding = None  # سيتم تعيين الترميز الناجح عند أول تعديل

    def on_modified(self, event):
        if event.src_path.endswith(WATCHED_FILE):
            print(f"{WATCHED_FILE} has been modified. Trying to read with best encoding...")
            data = None
            # إذا لم يتم تحديد الترميز مسبقاً، جرب جميع الترميزات
            if not self.file_encoding:
                data, encoding = read_file_with_best_encoding(WATCHED_FILE)
                if data is not None:
                    self.file_encoding = encoding
                else:
                    print("فشل في قراءة الملف بأي ��رميز.")
                    return
            else:
                # إذا تم تحديد الترميز مسبقاً، استخدمه مباشرة
                try:
                    with open(WATCHED_FILE, "r", encoding=self.file_encoding) as f:
                        data = f.read()
                except Exception as e:
                    print(f"فشل قراءة الملف بالترميز {self.file_encoding}: {e}")
                    self.file_encoding = None
                    return
            # إذا تمت القراءة بنجاح، أكمل إجراءات git
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