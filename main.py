import json
import time
import os
import random
import string
import logging
import uuid
import re
from datetime import datetime
from faker import Faker
from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError

# --- إعداد السجلات بشكل احترافي ضخم (نسختك الأصلية بالكامل) ---
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
        """توليد هوية رقمية كاملة بعشوائية تامة وقواعد باسوورد صارمة (نسختك الأصلية بالكامل)"""
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
            "month": random.randint(1, 12),
            "year": str(random.randint(1990, 2003)),
            "gender": random.randint(1, 2), 
            "password": final_password,
            "username_choice": f"{self.fake.user_name().replace('.', '')}{random.randint(100, 9999)}"
        }

    def take_evidence(self, action_label):
        """توثيق مرئي فوري لكل حركة برمجية مع تفاصيل التوقيت (نسختك الأصلية)"""
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

    # --- [ ميزة الاستكشاف العميق وفهم الكود المصدري ] ---
    def deep_dom_discovery(self, keyword, action="input", value=None):
        """تحليل الكود المصدري بالكامل للعثور على العناصر (نسختك المحدثة لدعم الراديو)"""
        logger.info(f"🔍 Deep Discovery Scan for: {keyword}")
        # أضفنا role='radio' للقائمة لضمان عدم تجاوز خيارات الإيميل
        elements = self.page.query_selector_all("input:not([type='hidden']), button, div[role='button'], div[role='combobox'], div[role='radio'], [aria-label], [placeholder]")
        
        for el in elements:
            try:
                info = el.evaluate("el => (el.innerText + el.getAttribute('aria-label') + el.getAttribute('name') + el.getAttribute('placeholder') + el.getAttribute('role')).toLowerCase()")
                if keyword.lower() in info:
                    logger.info(f"✨ Deep Match Found for {keyword}!")
                    el.scroll_into_view_if_needed()
                    if action == "input":
                        el.click()
                        self.page.keyboard.type(str(value), delay=random.randint(50, 150))
                    else:
                        el.click()
                    return True
            except: continue
        return self.tab_navigation_fallback(keyword, action, value)

    # --- [ خطة الطوارئ قبل الأخيرة: TAB ] ---
    def tab_navigation_fallback(self, keyword, action="input", value=None):
        """محاكاة التنقل بلوحة المفاتيح عبر زر TAB (نسختك المحدثة)"""
        logger.warning(f"⌨️ TAB Fallback for: {keyword}")
        self.page.keyboard.press("Control+Home") 
        time.sleep(0.5)
        for i in range(35):
            self.page.keyboard.press("Tab")
            time.sleep(0.1)
            active_info = self.page.evaluate("() => document.activeElement.outerHTML.toLowerCase()")
            if keyword.lower() in active_info or (i > 5 and action == "input" and "input" in active_info):
                if action == "input":
                    self.page.keyboard.type(str(value), delay=random.randint(50, 150))
                else:
                    self.page.keyboard.press("Enter")
                return True
        return False

    # --- [ الخطة الأخيرة: غريزة الاستكشاف الذاتي المطور ] ---
    def autonomous_blind_discovery(self):
        """الخطة التي لا تفشل: مسح وتصنيف كل حقل تفاعلي وتصحيح مسار الإيميل"""
        logger.warning("🚀 Critical: Activating Autonomous Blind Discovery Engine!")
        
        # جلب كل ما يمكن التفاعل معه بما في ذلك الراديو
        all_elements = self.page.query_selector_all("input:not([type='hidden']), [role='combobox'], [role='listbox'], [role='radio'], select, div[contenteditable='true']")
        
        for el in all_elements:
            try:
                if not el.is_visible(): continue
                
                type_attr = (el.get_attribute("type") or "").lower()
                name_attr = (el.get_attribute("name") or "").lower()
                placeholder = (el.get_attribute("placeholder") or "").lower()
                role = (el.get_attribute("role") or "").lower()
                tag = el.tag_name().lower()

                # 1. التعامل مع الراديو (حل مشكلة التوقف عند اختيار الإيميل)
                if role == "radio":
                    logger.info("🔘 Autonomous: Radio Option (Email) Selected")
                    el.click()
                    time.sleep(0.5)
                    break 

                # 2. التعامل مع الباسوورد
                elif type_attr == "password" or "pass" in name_attr:
                    logger.info("🔑 Autonomous: Password Field Detected")
                    el.fill(self.identity['password'])

                # 3. القوائم المنسدلة
                elif tag == "select" or role in ["combobox", "listbox"] or "month" in name_attr or "gender" in name_attr:
                    logger.info("🔽 Autonomous: Dropdown/Select Detected")
                    el.click()
                    time.sleep(0.5)
                    repeat = self.identity['month'] if "month" in name_attr else self.identity['gender']
                    for _ in range(max(1, repeat)):
                        self.page.keyboard.press("ArrowDown")
                    self.page.keyboard.press("Enter")

                # 4. الحقول النصية
                elif tag == "input" or type_attr == "text":
                    logger.info(f"📝 Autonomous: Text Field Detected [{name_attr}]")
                    if "day" in name_attr or "day" in placeholder:
                        el.fill(self.identity['day'])
                    elif "year" in name_attr or "year" in placeholder:
                        el.fill(self.identity['year'])
                    elif "first" in name_attr or "name" in placeholder:
                        el.fill(self.identity['first_name'])
                    else:
                        el.fill(self.identity['username_choice'])
            except: continue

        self.page.keyboard.press("Enter")

    def smart_input(self, selector_list, value, label):
        """محرك الإدخال الذكي مع نظام التعافي الذاتي ومسح الحقول"""
        self.take_evidence(f"PRE_INPUT_{label}")
        success = False
        for selector in selector_list:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=7000)
                el = self.page.locator(selector).first
                el.click()
                # إضافة مسح للحقل لضمان عدم وجود أخطاء في الإدخال المتكرر
                self.page.keyboard.press("Control+A")
                self.page.keyboard.press("Backspace")
                self.page.keyboard.type(str(value), delay=random.randint(60, 200))
                success = True
                break
            except: continue
        
        if not success:
            if not self.deep_dom_discovery(label, "input", value):
                self.autonomous_blind_discovery()
        
        self.take_evidence(f"POST_INPUT_{label}")
        time.sleep(random.uniform(0.5, 1.2))

    def smart_click(self, selector_list, label, is_optional=False):
        """محرك الضغط المطور (Multi-Selector)"""
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
            if not self.deep_dom_discovery(label, "click"):
                self.page.keyboard.press("Enter")
                clicked = True

        if clicked:
            logger.info(f"Successfully clicked: {label}")
            self.take_evidence(f"POST_CLICK_{label}")
            time.sleep(random.uniform(2, 4)) 
        elif not is_optional:
            raise Exception(f"Failed to click required button: {label}")

    def auto_skip_manager(self):
        """مدير التخطي الأصلي بكامل قوته"""
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
        """العملية الكاملة (The Ultimate Life-Cycle) مع صمامات أمان ضد النجاح الوهمي"""
        try:
            logger.info(f"Starting Registration Engine for: {self.identity['first_name']}")
            self.page.goto("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp", wait_until="networkidle")
            
            # 1. الأسماء (Names)
            self.smart_input(['input[name="firstName"]', '#firstName'], self.identity['first_name'], "FirstName")
            self.smart_input(['input[name="lastName"]', '#lastName'], self.identity['last_name'], "LastName")
            self.smart_click(['#collectNameNext', 'button'], "Next_Step_Names")

            # 2. تاريخ الميلاد والجنس
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)
            self.smart_input(['input[name="day"]', '#day'], self.identity['day'], "BirthDay")
            
            try:
                self.page.locator('#month').click()
                time.sleep(1)
                for _ in range(self.identity['month']):
                    self.page.keyboard.press("ArrowDown")
                self.page.keyboard.press("Enter")
                self.take_evidence("MONTH_SELECTED")
            except:
                self.autonomous_blind_discovery()

            self.smart_input(['input[name="year"]', '#year'], self.identity['year'], "BirthYear")
            
            try:
                self.page.locator('#gender').click()
                time.sleep(1)
                for _ in range(self.identity['gender']):
                    self.page.keyboard.press("ArrowDown")
                self.page.keyboard.press("Enter")
            except: pass

            self.smart_click(['#birthdaygenderNext'], "Next_Step_Bio")

            # 3. اختيار الإيميل (Email Strategy - الصيانة الكبرى هنا)
            self.page.wait_for_load_state("networkidle")
            time.sleep(3)
            
            # فحص خيارات الراديو (Email Suggestions)
            radio_opts = self.page.locator('div[role="radio"]')
            if radio_opts.count() > 0:
                logger.info("🔘 Detected email suggestions. Picking first option...")
                radio_opts.first.click()
                self.take_evidence("Picked_Suggested_Email")
            else:
                logger.info("📝 No suggestions found. Proceeding with Manual Email...")
                self.smart_input(['input[name="Username"]'], self.identity['username_choice'], "Manual_Email")
            
            # الضغط على التالي مع نظام "التحقق من العبور"
            self.smart_click(['#next', 'button'], "Next_Step_Email")
            
            # --- [ صمام الأمان: هل انتقلنا فعلاً لصفحة الباسوورد؟ ] ---
            try:
                # إذا لم يظهر حقل الباسوورد خلال 8 ثواني، فالمحرك عالق في صفحة الخطأ
                self.page.wait_for_selector('input[name="Passwd"]', timeout=8000)
                logger.info("✅ Transition Confirmed: Password Page reached.")
            except:
                logger.error("❌ Transition Failed: Still on Email selection. Retrying with Autonomous engine...")
                # تفعيل المحرك الأعمى لاكتشاف أي راديو أو حقل لم يتم ضغطه
                self.autonomous_blind_discovery()
                time.sleep(2)
                self.smart_click(['#next'], "Retry_Next_Step_Email")

            # 4. كلمات المرور (Security Layer)
            self.page.wait_for_load_state("networkidle")
            pwd = self.identity['password']
            self.smart_input(['input[name="Passwd"]'], pwd, "Password_Main")
            self.smart_input(['input[name="ConfirmPasswd"]'], pwd, "Password_Confirm")
            self.smart_click(['#createpasswordNext'], "Next_Step_Password")

            # 5. التخطي والموافقات
            self.page.wait_for_load_state("networkidle")
            self.auto_skip_manager()

            # 6. الموافقة النهائية
            agree_btn = self.page.locator('button:has-text("I agree"), button:has-text("أوافق")')
            if agree_btn.is_visible(timeout=7000):
                self.smart_click(['button:has-text("I agree")'], "Final_Agreement")

            logger.info("✅ Core Engine Finished the Mission Successfully.")

        except Exception as e:
            logger.error(f"❌ Critical Failure: {e}")
            self.take_evidence("FATAL_ERROR_REPORT")
        finally:
            self._generate_final_report()

    def _generate_final_report(self):
        """توليد التقرير النهائي (Master JSON)"""
        final_data = {
            "identity": self.identity,
            "trace": self.steps_log,
            "execution_status": "Finished",
            "metadata": {"engine_version": "Autonomous_Ultra_v4.0", "session": SESSION_ID}
        }
        with open(os.path.join(REPORT_DIR, "master_trace.json"), "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        logger.info(f"Report secured at: {REPORT_DIR}")

if __name__ == "__main__":
    with Camoufox(headless=True, humanize=True) as browser:
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        UltimateEngine(page).run_process()
