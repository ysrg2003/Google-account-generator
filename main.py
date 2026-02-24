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

# إعداد السجلات بشكل احترافي ضخم
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UltimateGoogleBot")

# --- الحفاظ على نظام التسمية والمسارات الخاص بك بدقة ---
SESSION_ID = f"PRO_ENGINE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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
        """توليد هوية رقمية كاملة بعشوائية تامة وقواعد باسوورد صارمة (بدون تبسيط)"""
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
            "month": random.randint(1, 12), # نحتاجه كرقم للتعامل مع الأسهم
            "year": str(random.randint(1990, 2003)),
            "gender": random.randint(1, 2), # 1 للأنثى، 2 للذكر
            "password": final_password,
            "username_choice": f"{self.fake.user_name()}{random.randint(100, 9999)}"
        }

    def take_evidence(self, action_label):
        """توثيق مرئي فوري لكل حركة برمجية مع تفاصيل التوقيت"""
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
            logger.warning(f"Evidence capture failed: {e}")

    def smart_input(self, selector_list, value, label):
        """محرك الإدخال الذكي الأصلي مع تعزيز الانتظار"""
        self.take_evidence(f"PRE_INPUT_{label}")
        target = None
        for selector in selector_list:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=10000)
                el = self.page.locator(selector).first
                if el.is_visible():
                    target = el
                    break
            except: continue
        
        if not target:
            self.take_evidence(f"CRITICAL_NOT_FOUND_{label}")
            raise Exception(f"CRITICAL: Field {label} not found in DOM.")

        target.click()
        for char in str(value):
            self.page.keyboard.type(char, delay=random.randint(60, 200))
        
        self.take_evidence(f"POST_INPUT_{label}")
        time.sleep(random.uniform(0.5, 1.2))

    def smart_click(self, selector_list, label, is_optional=False):
        """محرك الضغط المتعدد (Multi-Selector Click Engine)"""
        self.take_evidence(f"PRE_CLICK_{label}")
        clicked = False
        for selector in selector_list:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=5000):
                    btn.click()
                    clicked = True
                    break
            except: continue
        
        if not clicked and not is_optional:
            # محاولة أخيرة عبر النص (في حال تغير الـ Selector)
            try:
                self.page.get_by_role("button").get_by_text("Next", exact=False).click()
                clicked = True
            except: pass

        if clicked:
            logger.info(f"Successfully clicked: {label}")
            self.take_evidence(f"POST_CLICK_{label}")
            time.sleep(random.uniform(2, 4)) 
        elif not is_optional:
            raise Exception(f"Failed to click required button: {label}")

    def auto_skip_manager(self):
        """مدير التخطي الذكي الكامل لمواجهة جدران الحماية"""
        skip_selectors = [
            'button:has-text("تخطي")', 'button:has-text("Skip")',
            'span:has-text("تخطي")', 'span:has-text("Skip")',
            '[aria-label*="تخطي"]', '[aria-label*="Skip"]',
            'button:has-text("ليس الآن")', 'button:has-text("Not now")'
        ]
        
        logger.info("Scanning for 'Skip' options...")
        for _ in range(3):
            time.sleep(1.5)
            found_skip = False
            for selector in skip_selectors:
                try:
                    btn = self.page.locator(selector).first
                    if btn.is_visible(timeout=1000):
                        btn.click()
                        found_skip = True
                        logger.info("✨ Skip detected and executed.")
                        self.page.wait_for_load_state("networkidle")
                        break
                except: continue
            if not found_skip: break

    def run_process(self):
        """العملية الكاملة (The Full Lifecycle) بدون أي اختصارات"""
        try:
            logger.info(f"Starting Engine for: {self.identity['first_name']}")
            
            # الرابط المباشر لضمان عدم التوهان
            self.page.goto("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp", wait_until="networkidle")
            
            # 1. الأسماء (Names Core)
            self.smart_input(['input[name="firstName"]', '#firstName'], self.identity['first_name'], "FirstName")
            self.smart_input(['input[name="lastName"]', '#lastName'], self.identity['last_name'], "LastName")
            self.smart_click(['#collectNameNext', 'button:has-text("Next")'], "Next_Step_Names")

            # 2. تاريخ الميلاد والجنس (إصلاح "عقدة" الـ Select بناءً على الصور)
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)
            
            # اليوم
            self.smart_input(['input[name="day"]', '#day'], self.identity['day'], "BirthDay")
            
            # محرك اختيار الشهر المتطور (محاكاة لوحة المفاتيح)
            try:
                logger.info("Engaging Keyboard Simulation for Month Selection...")
                self.page.locator('#month').click() # فتح القائمة
                time.sleep(1)
                # استخدام الأسهم بناءً على رقم الشهر المولد
                for _ in range(self.identity['month']):
                    self.page.keyboard.press("ArrowDown")
                    time.sleep(0.1)
                self.page.keyboard.press("Enter")
                self.take_evidence("MONTH_SELECTED_VIA_KEYS")
            except Exception as e:
                logger.error(f"Month Simulation Failed: {e}")

            # السنة
            self.smart_input(['input[name="year"]', '#year'], self.identity['year'], "BirthYear")
            
            # الجنس
            try:
                self.page.locator('#gender').click()
                time.sleep(1)
                for _ in range(self.identity['gender']):
                    self.page.keyboard.press("ArrowDown")
                self.page.keyboard.press("Enter")
                self.take_evidence("GENDER_SELECTED_VIA_KEYS")
            except: pass

            self.smart_click(['#birthdaygenderNext'], "Next_Step_Bio")

            # 3. اختيار الإيميل (Email Strategy)
            self.page.wait_for_load_state("networkidle")
            time.sleep(3)
            
            # فحص إذا كان هناك راديو بوتون (اقتراحات)
            radio_opt = self.page.locator('div[role="radio"]').first
            if radio_opt.is_visible(timeout=5000):
                radio_opt.click()
                self.take_evidence("Picked_Suggested_Email")
            else:
                self.smart_input(['input[name="Username"]'], self.identity['username_choice'], "Manual_Email")
            
            self.smart_click(['#next', 'button:has-text("Next")'], "Next_Step_Email")

            # 4. كلمات المرور (Security Layer)
            self.page.wait_for_load_state("networkidle")
            pwd = self.identity['password']
            self.smart_input(['input[name="Passwd"]'], pwd, "Password_Main")
            self.smart_input(['input[name="ConfirmPasswd"]'], pwd, "Password_Confirm")
            self.smart_click(['#createpasswordNext'], "Next_Step_Password")

            # 5. التخطي والموافقات النهائية
            self.page.wait_for_load_state("networkidle")
            self.auto_skip_manager()

            # 6. الموافقة النهائية
            agree_btn = self.page.locator('button:has-text("I agree"), button:has-text("أوافق")')
            if agree_btn.is_visible(timeout=5000):
                self.smart_click(['button:has-text("I agree")'], "Final_Agreement")

            logger.info("✅ Core Engine Finished the Mission.")

        except Exception as e:
            logger.error(f"❌ Critical Engine Failure: {e}")
            self.take_evidence("FATAL_ERROR_DUMP")
        finally:
            self._generate_final_report()

    def _generate_final_report(self):
        """توليد التقرير النهائي (The Master JSON Report)"""
        final_data = {
            "identity": self.identity,
            "trace": self.steps_log,
            "execution_status": "Finished",
            "metadata": {
                "session": SESSION_ID,
                "engine_version": "Ultimate_v2.1"
            }
        }
        with open(os.path.join(REPORT_DIR, "master_trace.json"), "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        logger.info(f"Report secured at: {REPORT_DIR}")

if __name__ == "__main__":
    # تشغيل المحرك مع Camoufox بكامل قوته
    with Camoufox(headless=True, humanize=True) as browser:
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        engine = UltimateEngine(page)
        engine.run_process()
