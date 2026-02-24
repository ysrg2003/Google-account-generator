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

# إعداد المسارات والتقارير
SESSION_ID = f"TRACE_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
REPORT_DIR = os.path.join(os.getcwd(), SESSION_ID)
os.makedirs(os.path.join(REPORT_DIR, "screenshots"), exist_ok=True)

class UltimateEngine:
    def __init__(self, page):
        self.page = page
        self.fake = Faker(['en_US', 'ar_SA'])
        self.identity = self._generate_identity()
        self.steps_log = []
        self.step_idx = 0

    def _generate_identity(self):
        """توليد هوية رقمية كاملة بعشوائية تامة وقواعد باسوورد صارمة"""
        # توليد الباسوورد المطلوب: 10+ خانات، كبير، صغير، أرقام، رموز (+، *)
        pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + "+*"
        pwd = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice("+*")
        ]
        # إكمال الطول إلى 14 خانة بعشوائية
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
            "gender": str(random.choice([1, 2])), # 1 ذكر، 2 أنثى
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
        """محرك إدخال ذكي يحاكي البشر ويبحث عن الحقل بأكثر من طريقة"""
        self.take_evidence(f"PRE_INPUT_{label}")
        target = None
        for selector in selector_list:
            try:
                el = self.page.locator(selector).first
                if el.is_visible(timeout=5000):
                    target = el
                    break
            except: continue
        
        if not target:
            raise Exception(f"CRITICAL: Field {label} not found in DOM.")

        target.click()
        # محاكاة الكتابة البشرية البطيئة مع أخطاء طفيفة وسرعات متغيرة
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
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=4000):
                    btn.click()
                    clicked = True
                    break
            except: continue
        
        if not clicked and not is_optional:
            # محاولة أخيرة بناءً على النص
            try:
                self.page.get_by_role("button").get_by_text("التالي", exact=False).click()
                clicked = True
            except: pass

        if clicked:
            logger.info(f"Successfully clicked: {label}")
            self.take_evidence(f"POST_CLICK_{label}")
            time.sleep(random.uniform(2, 4)) # انتظار استجابة السيرفر
        elif not is_optional:
            raise Exception(f"Failed to click required button: {label}")

    def auto_skip_manager(self):
        """مدير التخطي: يقوم بمسح الصفحة بحثاً عن خيارات التخطي في صفحات (الهاتف، الاسترداد، الخدمات)"""
        skip_selectors = [
            'button:has-text("تخطي")', 'button:has-text("Skip")',
            'span:has-text("تخطي")', 'span:has-text("Skip")',
            '[aria-label*="تخطي"]', '[aria-label*="Skip"]',
            'button:has-text("ليس الآن")', 'button:has-text("Not now")'
        ]
        
        logger.info("Scanning for 'Skip' options...")
        # التحقق المتكرر لأن جوجل قد تظهر عدة صفحات اختيارية
        for _ in range(3):
            time.sleep(1.5)
            if self.smart_click(skip_selectors, "SKIP_ACTION", is_optional=True):
                logger.info("✨ Skip detected and executed.")
                self.page.wait_for_load_state("networkidle")
            else:
                break

    def run_process(self):
        """تنفيذ العملية الكاملة دون اختصار"""
        try:
            logger.info(f"Starting Registration with Identity: {self.identity['first_name']}")
            self.page.goto("https://accounts.google.com/lifecycle/steps/signup/name?continue=https://www.google.com/&flowEntry=SignUp", wait_until="networkidle")
            
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
            # اختيار أول إيميل مقترح إذا وجد، وإلا الكتابة يدوياً
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

            # 5. معالجة صفحات التخطي (رقم الهاتف / الاسترداد)
            self.page.wait_for_load_state("networkidle")
            self.auto_skip_manager()

            # 6. الموافقة النهائية (إذا وصلنا لها)
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
    with Camoufox(headless=True, humanize=True) as browser:
        page = browser.new_page()
        # تعيين دقة الشاشة لمحاكاة سطح المكتب
        page.set_viewport_size({"width": 1920, "height": 1080})
        engine = UltimateEngine(page)
        engine.run_process()

