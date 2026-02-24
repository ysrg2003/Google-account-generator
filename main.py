from camoufox.sync_api import Camoufox
import os

def run():
    # استخدام المتصفح مع إعدادات تناسب السيرفر
    with Camoufox(headless=True) as browser:
        print("جاري تشغيل المتصفح...")
        page = browser.new_page()
        
        url = "https://accounts.google.com/lifecycle/steps/signup/name?continue=https://www.google.com/&flowEntry=SignUp"
        
        try:
            page.goto(url, wait_until="networkidle")
            print(f"تم الوصول للرابط بنجاح: {page.title()}")
            
            # التقاط صورة وحفظها في المجلد الحالي
            page.screenshot(path="google_signup.png", full_page=True)
            print("تم حفظ لقطة الشاشة.")
            
        except Exception as e:
            print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    run()
