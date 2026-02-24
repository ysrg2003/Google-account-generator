import json
import time
import os
import random
import string
import logging
import uuid
from datetime import datetime
from faker import Faker
from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError

# إعداد السجلات بشكل احترافي
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UltimateGoogleBot")

# --- تصحيح المسارات: أبقيت على نظام التسمية الخاص بك مع إصلاح خطأ القوس ---
SESSION_ID = f"PRO_ENGINE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
REPORT_DIR = os.path.join(os.getcwd(), SESSION_ID)
os.makedirs(os.path.join(REPORT_DIR, "screenshots"), exist_ok=True) # تم إصلاح القوس هنا

class UltimateEngine:
    def __init__(self, page):
        self.page = page
        self.fake = Faker(['en_US', 'ar_SA'])
        self.identity = self._generate_identity()
        self.steps_log = []
        self.step_idx = 0

    def _generate_identity(self):
        """توليد هوية رقمية كاملة بعشوائية تامة وقواعد باسوورد صارمة"""
        pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + "+*"
        pwd = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice("+*")
        ]
        pwd += [random.choice(pool) for _ in range(10)]
        random.shuffle(pwd)
        final_password = "".join(pwd)

        return {
            "id": str(uuid.uuid4()),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "day": str(random.randint(1, 28)),
            "month": str(random.randint(1, 12)),
            "year": str(random.randint(1990, 2003)),
            "gender": str(random.choice([1, 2])), 
            "password": final_password,
            "username_choice": f"{self.fake.user_name()}{random.randint(100, 9999)}"
        }

    def take_evidence(self, action_label):
        """توثيق مرئي فوري لكل حركة برمجية"""
        self.step_idx += 1
        ts = datetime.now().strftime("%H%M%S_%f")
        filename = f"{self.step_idx:03d}_{action_label}_{ts}.png"
        save_path = os.path.join(REPORT_DIR, "screenshots", filename)
        
        try:
            self.page.screenshot(path=save_path, full_page=True)
            self.steps_log.append({
                "step_index": self.step_idx,
                "label": action_label,
                "timestamp": ts,
                "url": self.page.url,
                "screenshot": filename
            })
        except Exception as e:
            logger.warning(f"Could not take screenshot: {e}")

    def smart_input(self, selector_list, value, label):
        """محرك إدخال ذكي - مع إضافة ميزة الانتظار لتجاوز خطأ الـ DOM"""
        self.take_evidence(f"PRE_INPUT_{label}")
        target = None
        
        # إضافة انتظار صريح لضمان أن جوجل قامت بتحميل الحقل قبل البحث عنه
        # هذا هو الحل لخطأ 'FirstName not found'
        for selector in selector_list:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=10000)
                el = self.page.locator(selector).first
                if el.is_visible():
                    target = el
                    break
            except: continue
        
        if not target:
            # لقطة شاشة للخطأ قبل الانهيار لمعرفة ما تراه العين البرمجية
            self.take_evidence(f"CRITICAL_NOT_FOUND_{label}")
            raise Exception(f"CRITICAL: Field {label} not found in DOM.")

        target.click()
        for char in value:
            self.page.keyboard.type(char, delay=random.randint(60, 200))
        
        self.take_evidence(f"POST_INPUT_{label}")
        time.sleep(random.uniform(0.5, 1.2))

    def smart_click(self, selector_list, label, is_optional=False):
        """محرك ضغط يبحث عن الأزرار النصية أو البرمجية"""
        self.take_evidence(f"PRE_CLICK_{label}")
        clicked = False
        for selector in selector_list:
            try:
                # ننتظر الزر قليلاً قبل المحاولة
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=5000):
                    btn.click()
                    clicked = True
                    break
            except: continue
        
        if not clicked and not is_optional:
            try:
                self.page.get_by_role("button").get_by_text("التالي", exact=False).click()
                clicked = True
            except: pass

        if clicked:
            logger.info(f"Successfully clicked: {label}")
            self.take_evidence(f"POST_CLICK_{label}")
            time.sleep(random.uniform(2, 4)) 
        elif not is_optional:
            raise Exception(f"Failed to click required button: {label}")

    def auto_skip_manager(self):
        """مدير التخطي: يقوم بمسح الصفحة بحثاً عن خيارات التخطي"""
        skip_selectors = [
            'button:has-text("تخطي")', 'button:has-text("Skip")',
            'span:has-text("تخطي")', 'span:has-text("Skip")',
            '[aria-label*="تخطي"]', '[aria-label*="Skip"]',
            'button:has-text("ليس الآن")', 'button:has-text("Not now")'
        ]
        
        logger.info("Scanning for 'Skip' options...")
        for _ in range(3):
            time.sleep(1.5)
            # استخدام smart_click داخلياً للحفاظ على نفس المنطق
            found = False
            for selector in skip_selectors:
                try:
                    if self.page.locator(selector).first.is_visible(timeout=1000):
                        self.page.locator(selector).first.click()
                        logger.info("✨ Skip detected and executed.")
                        self.page.wait_for_load_state("networkidle")
                        found = True
                        break
                except: continue
            if not found: break

    def run_process(self):
        """تنفيذ العملية الكاملة دون اختصار"""
        try:
            logger.info(f"Starting Registration with Identity: {self.identity['first_name']}")
            
            # الانتقال للرابط المباشر لضمان عدم التوهان في صفحات جوجل الجانبية
            self.page.goto("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp", wait_until="networkidle")
            
            # 1. الأسماء
            self.smart_input(['input[name="firstName"]', '#firstName'], self.identity['first_name'], "FirstName")
            self.smart_input(['input[name="lastName"]', '#lastName'], self.identity['last_name'], "LastName")
            self.smart_click(['#collectNameNext', 'button:has-text("التالي")'], "Next_Step_Names")

            # 2. تاريخ الميلاد والجنس
            self.page.wait_for_load_state("networkidle")
            self.smart_input(['input[name="day"]'], self.identity['day'], "BirthDay")
            self.page.locator('select#month').select_option(value=self.identity['month'])
            self.smart_input(['input[name="year"]'], self.identity['year'], "BirthYear")
            self.page.locator('select#gender').select_option(value=self.identity['gender'])
            self.smart_click(['#birthdaygenderNext', 'button:has-text("التالي")'], "Next_Step_Bio")

            # 3. اختيار الإيميل
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)
            if self.page.locator('div[role="radio"]').first.is_visible(timeout=5000):
                self.page.locator('div[role="radio"]').first.click()
                self.take_evidence("Picked_Suggested_Email")
            else:
                self.smart_input(['input[name="Username"]'], self.identity['username_choice'], "Manual_Email")
            
            self.smart_click(['#next', 'button:has-text("التالي")'], "Next_Step_Email")

            # 4. كلمات المرور
            self.page.wait_for_load_state("networkidle")
            pwd = self.identity['password']
            self.smart_input(['input[name="Passwd"]'], pwd, "Password_Main")
            self.smart_input(['input[name="ConfirmPasswd"]'], pwd, "Password_Confirm")
            self.smart_click(['#createpasswordNext', 'button:has-text("التالي")'], "Next_Step_Password")

            # 5. معالجة صفحات التخطي
            self.page.wait_for_load_state("networkidle")
            self.auto_skip_manager()

            # 6. الموافقة النهائية
            if self.page.locator('button:has-text("أوافق"), button:has-text("I agree")').is_visible(timeout=5000):
                self.smart_click(['button:has-text("أوافق")', 'button:has-text("I agree")'], "Final_Agreement")

            logger.info("Mission Completed Successfully.")

        except Exception as e:
            logger.error(f"Critical Engine Failure: {e}")
            self.take_evidence("FATAL_ERROR")
        finally:
            self._generate_final_report()

    def _generate_final_report(self):
        final_data = {
            "identity": self.identity,
            "trace": self.steps_log,
            "execution_status": "Finished"
        }
        with open(os.path.join(REPORT_DIR, "master_trace.json"), "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        logger.info(f"Report generated at: {REPORT_DIR}")

if __name__ == "__main__":
    # استخدام Camoufox بكامل قوته التخفية
    with Camoufox(headless=True, humanize=True) as browser:
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        engine = UltimateEngine(page)
        engine.run_process()
