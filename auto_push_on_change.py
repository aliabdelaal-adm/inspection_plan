#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Push on Change Script
==========================

هذا السكريبت يقوم بمراقبة الملفات المحددة ويقوم تلقائياً بعمل git add, commit, و push
عند اكتشاف أي تغيير على الملفات المراقبة.

المتطلبات (Requirements):
=========================
1. Python 3.6 أو أحدث
2. مكتبة watchdog: pip install watchdog
3. Git مثبت ومهيأ في النظام
4. Repository مهيأ مع remote origin

تعليمات التشغيل (Installation & Usage):
======================================

# 1. تثبيت مكتبة watchdog
pip install watchdog

# 2. التأكد من إعداد Git
git config --global user.name "اسمك"
git config --global user.email "بريدك@الإلكتروني.com"

# 3. تشغيل السكريبت
python auto_push_on_change.py

# 4. لإيقاف السكريبت، اضغط Ctrl+C

الإعدادات (Configuration):
==========================
يمكنك تعديل قائمة الملفات المراقبة في المتغير FILES_TO_MONITOR أدناه
"""

import os
import sys
import time
import subprocess
import logging
from datetime import datetime
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("ERROR: مكتبة watchdog غير مثبتة!")
    print("يرجى تثبيتها باستخدام الأمر: pip install watchdog")
    print("ERROR: watchdog library is not installed!")
    print("Please install it using: pip install watchdog")
    sys.exit(1)

# =============================================================================
# الإعدادات (Configuration)
# =============================================================================

# قائمة الملفات المراقبة - يمكن إضافة ملفات أخرى هنا
FILES_TO_MONITOR = [
    "plan-data.json",
    # يمكن إضافة ملفات أخرى هنا
    # "config.json",
    # "data.txt",
]

# رسالة الcommit الافتراضية
DEFAULT_COMMIT_MESSAGE = "Auto-update: تم تحديث الملفات تلقائياً"

# فترة التأخير قبل القيام بـ push (بالثواني) لتجنب commits متعددة سريعة
PUSH_DELAY = 5

# اسم الفرع للـ push
BRANCH_NAME = "main"

# =============================================================================
# إعداد نظام السجلات (Logging Setup)
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_push.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# =============================================================================
# فئة معالج الأحداث (Event Handler Class)
# =============================================================================

class FileChangeHandler(FileSystemEventHandler):
    """معالج أحداث تغيير الملفات"""
    
    def __init__(self):
        super().__init__()
        self.last_push_time = {}
        self.pending_files = set()
    
    def on_modified(self, event):
        """يتم استدعاؤها عند تعديل ملف"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        filename = file_path.name
        
        # التحقق من أن الملف في قائمة المراقبة
        if filename in FILES_TO_MONITOR:
            logger.info(f"🔍 اكتشاف تغيير في الملف: {filename}")
            logger.info(f"🔍 Detected change in file: {filename}")
            
            # إضافة الملف للقائمة المعلقة
            self.pending_files.add(filename)
            
            # تأخير معالجة الملف لتجنب commits متعددة سريعة
            current_time = time.time()
            self.last_push_time[filename] = current_time
            
            # معالجة الملف بعد التأخير المحدد
            self._schedule_push(filename, current_time)
    
    def _schedule_push(self, filename, scheduled_time):
        """جدولة عملية push بعد تأخير"""
        # انتظار فترة التأخير
        time.sleep(PUSH_DELAY)
        
        # التحقق من عدم حدوث تغييرات جديدة خلال فترة التأخير
        if (filename in self.last_push_time and 
            self.last_push_time[filename] == scheduled_time and
            filename in self.pending_files):
            
            self._push_changes(filename)
            self.pending_files.discard(filename)
    
    def _push_changes(self, filename):
        """تنفيذ عمليات git add, commit, push"""
        try:
            logger.info(f"🚀 بدء عملية رفع التغييرات للملف: {filename}")
            logger.info(f"🚀 Starting push process for file: {filename}")
            
            # التحقق من وجود الملف
            if not Path(filename).exists():
                logger.warning(f"⚠️  الملف غير موجود: {filename}")
                logger.warning(f"⚠️  File not found: {filename}")
                return
            
            # git add
            result = subprocess.run(
                ["git", "add", filename],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                logger.error(f"❌ خطأ في git add: {result.stderr}")
                logger.error(f"❌ Error in git add: {result.stderr}")
                return
            
            # التحقق من وجود تغييرات للcommit
            result = subprocess.run(
                ["git", "diff", "--cached", "--quiet"],
                capture_output=True
            )
            
            if result.returncode == 0:
                logger.info(f"ℹ️  لا توجد تغييرات جديدة في الملف: {filename}")
                logger.info(f"ℹ️  No new changes in file: {filename}")
                return
            
            # git commit
            commit_message = f"{DEFAULT_COMMIT_MESSAGE} - {filename} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                logger.error(f"❌ خطأ في git commit: {result.stderr}")
                logger.error(f"❌ Error in git commit: {result.stderr}")
                return
            
            logger.info(f"✅ تم commit بنجاح: {commit_message}")
            logger.info(f"✅ Committed successfully: {commit_message}")
            
            # git push
            result = subprocess.run(
                ["git", "push", "origin", BRANCH_NAME],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                logger.error(f"❌ خطأ في git push: {result.stderr}")
                logger.error(f"❌ Error in git push: {result.stderr}")
                return
            
            logger.info(f"🎉 تم رفع التغييرات بنجاح إلى فرع {BRANCH_NAME}")
            logger.info(f"🎉 Successfully pushed changes to {BRANCH_NAME} branch")
            
        except Exception as e:
            logger.error(f"❌ خطأ غير متوقع: {str(e)}")
            logger.error(f"❌ Unexpected error: {str(e)}")

# =============================================================================
# الدوال المساعدة (Helper Functions)
# =============================================================================

def check_git_setup():
    """التحقق من إعداد Git"""
    try:
        # التحقق من وجود Git
        result = subprocess.run(["git", "--version"], capture_output=True)
        if result.returncode != 0:
            logger.error("❌ Git غير مثبت أو غير متاح")
            logger.error("❌ Git is not installed or not available")
            return False
        
        # التحقق من وجود repository
        result = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True)
        if result.returncode != 0:
            logger.error("❌ المجلد الحالي ليس Git repository")
            logger.error("❌ Current directory is not a Git repository")
            return False
        
        # التحقق من وجود remote origin
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True)
        if result.returncode != 0:
            logger.error("❌ لا يوجد remote origin مهيأ")
            logger.error("❌ No remote origin configured")
            return False
        
        logger.info("✅ إعداد Git صحيح")
        logger.info("✅ Git setup is correct")
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في التحقق من Git: {str(e)}")
        logger.error(f"❌ Error checking Git setup: {str(e)}")
        return False

def check_files():
    """التحقق من وجود الملفات المراقبة"""
    existing_files = []
    missing_files = []
    
    for filename in FILES_TO_MONITOR:
        if Path(filename).exists():
            existing_files.append(filename)
        else:
            missing_files.append(filename)
    
    if existing_files:
        logger.info(f"✅ الملفات الموجودة للمراقبة: {', '.join(existing_files)}")
        logger.info(f"✅ Existing files to monitor: {', '.join(existing_files)}")
    
    if missing_files:
        logger.warning(f"⚠️  الملفات غير الموجودة: {', '.join(missing_files)}")
        logger.warning(f"⚠️  Missing files: {', '.join(missing_files)}")
    
    return len(existing_files) > 0

# =============================================================================
# الدالة الرئيسية (Main Function)
# =============================================================================

def main():
    """الدالة الرئيسية لتشغيل مراقب الملفات"""
    print("=" * 60)
    print("🤖 Auto Push on Change - مراقب التغييرات التلقائي")
    print("=" * 60)
    
    # التحقق من إعداد Git
    if not check_git_setup():
        logger.error("❌ يرجى إعداد Git قبل تشغيل السكريبت")
        logger.error("❌ Please setup Git before running the script")
        sys.exit(1)
    
    # التحقق من وجود الملفات
    if not check_files():
        logger.error("❌ لا توجد ملفات للمراقبة")
        logger.error("❌ No files to monitor")
        sys.exit(1)
    
    # إنشاء معالج الأحداث والمراقب
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    
    try:
        # بدء المراقبة
        observer.start()
        logger.info("🔍 بدء مراقبة الملفات...")
        logger.info("🔍 Started monitoring files...")
        logger.info(f"📋 الملفات المراقبة: {', '.join(FILES_TO_MONITOR)}")
        logger.info(f"📋 Monitored files: {', '.join(FILES_TO_MONITOR)}")
        logger.info("⌨️  اضغط Ctrl+C لإيقاف المراقبة")
        logger.info("⌨️  Press Ctrl+C to stop monitoring")
        
        # الاستمرار في المراقبة
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف المراقبة بواسطة المستخدم")
        logger.info("🛑 Monitoring stopped by user")
        
    except Exception as e:
        logger.error(f"❌ خطأ في المراقبة: {str(e)}")
        logger.error(f"❌ Monitoring error: {str(e)}")
        
    finally:
        observer.stop()
        observer.join()
        logger.info("👋 تم إغلاق السكريبت")
        logger.info("👋 Script terminated")

# =============================================================================
# نقطة الدخول (Entry Point)
# =============================================================================

if __name__ == "__main__":
    main()