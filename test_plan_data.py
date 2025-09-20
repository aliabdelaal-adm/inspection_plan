import json

with open("plan-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print("تمت قراءة الملف بنجاح!")
    print(data)
