# تعليمات تشغيل auto_push_on_change.py

## نظرة عامة
سكريبت Python لمراقبة تغييرات الملفات تلقائياً ورفعها إلى GitHub باستخدام مكتبة watchdog.

## المتطلبات الأساسية

### 1. Python 3.6 أو أحدث
تحقق من الإصدار:
```bash
python --version
```

### 2. Git مثبت ومهيأ
```bash
# التحقق من تثبيت Git
git --version

# إعداد Git (إذا لم يكن مهيأ من قبل)
git config --global user.name "اسمك"
git config --global user.email "بريدك@الإلكتروني.com"
```

### 3. Repository مهيأ مع remote origin
```bash
# التحقق من وجود remote origin
git remote -v
```

## التثبيت والإعداد

### 1. تثبيت مكتبة watchdog
```bash
pip install watchdog
```

### 2. على Windows (إضافي)
إذا واجهت مشاكل في التثبيت على Windows، جرب:
```cmd
pip install --user watchdog
```

## التشغيل

### طريقة التشغيل الأساسية
```bash
python auto_push_on_change.py
```

### تشغيل في الخلفية (Windows)
```cmd
# تشغيل في نافذة جديدة
start python auto_push_on_change.py

# أو استخدام PowerShell
Start-Process python -ArgumentList "auto_push_on_change.py"
```

### تشغيل في الخلفية (Linux/Mac)
```bash
nohup python auto_push_on_change.py &
```

## التخصيص

### إضافة ملفات جديدة للمراقبة
افتح `auto_push_on_change.py` وعدّل قائمة `FILES_TO_MONITOR`:

```python
FILES_TO_MONITOR = [
    "plan-data.json",
    "config.json",        # ملف جديد
    "data.txt",          # ملف آخر
]
```

### تغيير رسالة الcommit
```python
DEFAULT_COMMIT_MESSAGE = "رسالتك المخصصة"
```

### تغيير فترة التأخير
```python
PUSH_DELAY = 10  # 10 ثوانٍ بدلاً من 5
```

### تغيير اسم الفرع
```python
BRANCH_NAME = "develop"  # بدلاً من "main"
```

## الملفات المُنتجة

### auto_push.log
ملف سجل يحتوي على جميع العمليات والأخطاء:
- تغييرات الملفات المكتشفة
- عمليات Git المنفذة
- الأخطاء إن وجدت

## استكشاف الأخطاء

### خطأ: مكتبة watchdog غير مثبتة
```bash
pip install watchdog
```

### خطأ: Git غير مثبت
- قم بتثبيت Git من: https://git-scm.com/
- أعد تشغيل Command Prompt/Terminal

### خطأ: ليس Git repository
```bash
git init
git remote add origin <URL-REPOSITORY>
```

### خطأ: لا يوجد remote origin
```bash
git remote add origin <URL-REPOSITORY>
```

### خطأ في المصادقة مع GitHub
- تأكد من صحة بيانات المصادقة
- قد تحتاج لإعداد Personal Access Token

## نصائح للاستخدام

### 1. تشغيل مستمر
- شغل السكريبت عند بدء تشغيل النظام
- استخدم Task Scheduler على Windows
- استخدم crontab على Linux

### 2. مراقبة السجلات
راقب ملف `auto_push.log` للتأكد من عمل السكريبت بشكل صحيح.

### 3. اختبار قبل الاستخدام
- جرب تعديل `plan-data.json` يدوياً
- تأكد من حدوث commit و push تلقائياً
- راجع السجلات للتأكد من عدم وجود أخطاء

## إيقاف السكريبت
اضغط `Ctrl+C` في النافذة التي يعمل بها السكريبت.