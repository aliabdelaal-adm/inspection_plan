import json
import sys
import io

# ضمان الطباعة بترميز UTF-8 حتى على ويندوز
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("plan-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print("تمت قراءة الملف بنجاح!")
    print(data)