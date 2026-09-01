#!/usr/bin/env python3
"""
سكربت لاسترجاع النسخة الاحتياطية

الاستخدام:
    python restore_backup.py
"""

import json
from pathlib import Path
from datetime import datetime

def list_backups():
    """عرض قائمة النسخ الاحتياطية المتوفرة"""
    backup_dir = Path("backups")
    
    if not backup_dir.exists():
        print("❌ مجلد النسخ الاحتياطية غير موجود!")
        return []
    
    # البحث عن جميع النسخ الاحتياطية
    backups = sorted(backup_dir.glob("users_backup_*.json"), reverse=True)
    latest = backup_dir / "users_latest.json"
    
    if latest.exists():
        backups.insert(0, latest)
    
    return backups

def show_backup_info(backup_file: Path):
    """عرض معلومات عن النسخة الاحتياطية"""
    try:
        data = json.loads(backup_file.read_text(encoding="utf-8"))
        count = len(data) if isinstance(data, list) else 0
        size = backup_file.stat().st_size
        modified = datetime.fromtimestamp(backup_file.stat().st_mtime)
        
        return {
            "count": count,
            "size": size,
            "modified": modified.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": str(e)}

def restore_from_backup(backup_file: Path):
    """استرجاع النسخة الاحتياطية"""
    try:
        # قراءة النسخة الاحتياطية
        data = json.loads(backup_file.read_text(encoding="utf-8"))
        
        if not isinstance(data, list):
            print("❌ صيغة الملف غير صحيحة!")
            return False
        
        # إنشاء مجلد data إذا لم يكن موجود
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        users_file = data_dir / "users.json"
        
        # نسخ احتياطية من الملف الحالي قبل الاستبدال
        if users_file.exists():
            backup_before = data_dir / f"users_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_before.write_text(users_file.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"✅ تم حفظ نسخة من الملف الحالي: {backup_before.name}")
        
        # استعادة النسخة الاحتياطية
        users_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        
        print(f"\n{'='*50}")
        print(f"✅ تم الاسترجاع بنجاح!")
        print(f"{'='*50}")
        print(f"📁 من: {backup_file.name}")
        print(f"📁 إلى: {users_file}")
        print(f"👥 عدد المشتركين: {len(data)}")
        print(f"{'='*50}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاسترجاع: {e}")
        return False

def main():
    print("="*50)
    print("🔄 أداة استرجاع النسخ الاحتياطية")
    print("="*50)
    print()
    
    # عرض قائمة النسخ الاحتياطية
    backups = list_backups()
    
    if not backups:
        print("❌ لا توجد نسخ احتياطية متوفرة!")
        print("\n💡 تأكد من:")
        print("   - وجود مجلد backups/")
        print("   - وجود ملفات نسخ احتياطية بصيغة users_backup_*.json")
        return
    
    print(f"📋 النسخ الاحتياطية المتوفرة ({len(backups)}):\n")
    
    for i, backup in enumerate(backups, 1):
        info = show_backup_info(backup)
        if "error" in info:
            print(f"{i}. {backup.name} - ❌ خطأ: {info['error']}")
        else:
            print(f"{i}. {backup.name}")
            print(f"   👥 المشتركين: {info['count']}")
            print(f"   📅 التاريخ: {info['modified']}")
            print(f"   💾 الحجم: {info['size']} بايت")
            print()
    
    # اختيار النسخة
    try:
        choice = input("اختر رقم النسخة للاسترجاع (أو 0 للإلغاء): ").strip()
        
        if choice == "0":
            print("❌ تم الإلغاء")
            return
        
        index = int(choice) - 1
        
        if index < 0 or index >= len(backups):
            print("❌ رقم غير صحيح!")
            return
        
        selected_backup = backups[index]
        
        # تأكيد الاسترجاع
        confirm = input(f"\n⚠️ هل أنت متأكد من استرجاع {selected_backup.name}? (yes/no): ").strip().lower()
        
        if confirm in ["yes", "y", "نعم"]:
            restore_from_backup(selected_backup)
        else:
            print("❌ تم الإلغاء")
            
    except ValueError:
        print("❌ يجب إدخال رقم صحيح!")
    except KeyboardInterrupt:
        print("\n❌ تم الإلغاء")

if __name__ == "__main__":
    main()
