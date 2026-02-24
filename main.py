from camoufox.sync_api import Camoufox
import os

def run():
    print("بدء تشغيل نظام Camoufox...")
    
    # إعداد المتصفح بوضع headless للعمل داخل GitHub Actions
    with Camoufox(headless=True) as browser:
        print("المتصفح يعمل الآن بنجاح.")
        
        # إنشاء صفحة جديدة (تلقائياً تكون في وضع التخفي مع بصمة إصبع فريدة)
        page = browser.new_page()
        
        # الرابط المطلوب
        url = "https://accounts.google.com/lifecycle/steps/signup/name?continue=https://www.google.com/&flowEntry=SignUp"
        
        try:
            print(f"جاري الانتقال إلى: {url}")
            # الانتظار حتى تستقر الشبكة لضمان تحميل الصفحة كاملة
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            print(f"العنوان الحالي للصفحة: {page.title()}")
            
            # التقاط صورة للشاشة (Full Page) للتأكد من المحتوى
            screenshot_path = "google_signup.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"تم بنجاح! تم حفظ لقطة الشاشة باسم: {screenshot_path}")
            
        except Exception as e:
            print(f"حدث خطأ أثناء التشغيل: {str(e)}")

if __name__ == "__main__":
    run()
