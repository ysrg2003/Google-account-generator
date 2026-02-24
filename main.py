import json
import time
import os
import random
import uuid
from datetime import datetime
from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError as PlaywrightTimeout

# إعدادات التوثيق
REPORT_DIR = f"automation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(f"{REPORT_DIR}/screenshots", exist_ok=True)

class AutomationEngine:
    def __init__(self, page):
        self.page = page
        self.history = []
        self.start_time = time.time()

    def log(self, action, status, details=None, error=None):
        """نظام تسجيل فائق الدقة"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": timestamp,
            "action": action,
            "status": status,
            "details": details,
            "error": str(error) if error else None,
            "url": self.page.url
        }
        self.history.append(log_entry)
        
        # التقاط صورة لكل حدث (قبل وبعد)
        shot_name = f"{log_entry['id']}_{action}.png"
        try:
            self.page.screenshot(path=f"{REPORT_DIR}/screenshots/{shot_name}", full_page=True)
            log_entry["screenshot"] = shot_name
        except:
            pass
            
        print(f"[{timestamp}] {action.upper()}: {status} | {details if details else ''}")

    def human_type(self, selector, text, label):
        """كتابة بشرية مع تأخيرات عشوائية وأخطاء مطبعية مصححة (اختياري)"""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=10000)
            element = self.page.locator(selector)
            element.click() # الضغط قبل الكتابة
            
            for char in text:
                self.page.keyboard.type(char)
                time.sleep(random.uniform(0.05, 0.2)) # سرعة كتابة متفاوتة
            
            self.log("typing", "success", {"field": label, "length": len(text)})
        except Exception as e:
            self.log("typing", "failed", {"field": label}, error=e)
            raise

    def smart_click(self, selectors, label):
        """محاولة الضغط باستخدام عدة محددات في حال تغير الكود المصدري"""
        success = False
        for selector in selectors:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=5000)
                self.page.click(selector)
                self.log("click", "success", {"label": label, "selector": selector})
                success = True
                break
            except:
                continue
        
        if not success:
            self.log("click", "failed", {"label": label})
            raise Exception(f"Could not click on {label}")

    def get_page_intel(self):
        """فحص عميق للصفحة لفهم الحقول المتاحة (فهم الكود المصدري)"""
        intel = self.page.evaluate("""() => {
            return {
                inputs: Array.from(document.querySelectorAll('input')).map(i => ({name: i.name, type: i.type, visible: i.offsetWidth > 0})),
                buttons: Array.from(document.querySelectorAll('button')).map(b => ({text: b.innerText, id: b.id})),
                title: document.title,
                url: location.href
            }
        }""")
        self.log("page_inspection", "success", intel)
        return intel

def run_mission():
    # إعدادات التخفي القصوى من Camoufox
    with Camoufox(
        headless=True,
        humanize=True,
        os=["windows", "macos"],
        screen={"width": 1920, "height": 1080}
    ) as browser:
        
        context = browser.new_context(
            locale="ar-EG",
            timezone_id="Africa/Cairo"
        )
        page = context.new_page()
        engine = AutomationEngine(page)

        # 1. الدخول والمراقبة
        target_url = "https://accounts.google.com/lifecycle/steps/signup/name?continue=https://www.google.com/&flowEntry=SignUp"
        engine.log("navigation", "start", {"target": target_url})
        page.goto(target_url, wait_until="networkidle")
        
        try:
            # 2. تحليل الصفحة (فهم الكود المصدري ديناميكياً)
            engine.get_page_intel()

            # 3. خطوة الأسماء
            engine.human_type('input[name="firstName"]', "ياسين", "الاسم الأول")
            engine.human_type('input[name="lastName"]', "الخالدي", "اسم العائلة")
            
            # الضغط على زر التالي (بمحددات متعددة)
            engine.smart_click([
                'button:has-text("التالي")', 
                'button:has-text("Next")', 
                '#accountDetailsNext button'
            ], "زر الانتقال لتاريخ الميلاد")

            # 4. انتظار تحميل صفحة البيانات الشخصية
            page.wait_for_load_state("networkidle")
            time.sleep(2)
            engine.get_page_intel() # فهم الصفحة الجديدة

            # 5. تعبئة التاريخ (التعامل مع Dropdowns والنصوص)
            engine.human_type('input[name="day"]', "12", "اليوم")
            
            # اختيار الشهر (جوجل يستخدم أحياناً Divs مخصصة أو Select)
            try:
                page.locator('select#month').select_option(value="3") # مارس
            except:
                engine.smart_click(['#month', '[aria-label="الشهر"]'], "فتح قائمة الشهور")
                page.click('text="مارس"')

            engine.human_type('input[name="year"]', "1992", "السنة")
            
            # اختيار الجنس
            engine.smart_click(['select#gender', '[aria-label="الجنس"]'], "اختيار الجنس")
            page.locator('select#gender').select_option(value="1") # ذكر

            engine.smart_click(['button:has-text("التالي")', 'button:has-text("Next")'], "زر الانتقال لاسم المستخدم")

            # 6. المرحلة النهائية (اختيار الإيميل والباسوورد)
            page.wait_for_load_state("networkidle")
            # ... استكمال بقية الحقول بنفس النمط الاحترافي ...

        except Exception as e:
            engine.log("mission_critical_failure", "error", error=e)
        
        finally:
            # تصدير التقرير النهائي الشامل
            report = {
                "summary": {
                    "total_steps": len(engine.history),
                    "duration": f"{time.time() - engine.start_time:.2f}s",
                    "final_url": page.url
                },
                "trace": engine.history
            }
            with open(f"{REPORT_DIR}/final_log.json", "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=4)
            print(f"🏁 تم حفظ التقرير الكامل في: {REPORT_DIR}")

if __name__ == "__main__":
    run_mission()
