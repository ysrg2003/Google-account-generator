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

    # --- [ ميزة القناص الفيزيائي: الضغط عبر الإحداثيات ] ---
    def physical_click_fallback(self, element, label):
        """الضغط الفيزيائي عبر إحداثيات الماوس لتجاوز الحاويات المعقدة"""
        try:
            box = element.bounding_box()
            if box:
                center_x = box['x'] + box['width'] / 2
                center_y = box['y'] + box['height'] / 2
                logger.info(f"🖱️ Physical Click [X:{center_x} Y:{center_y}] for {label}")
                self.page.mouse.click(center_x, center_y)
                return True
        except: pass
        return False

    def deep_dom_discovery(self, keyword, action="input", value=None):
        """تحليل الكود المصدري بالكامل للعثور على العناصر مع دعم الضغط الفيزيائي"""
        logger.info(f"🔍 Deep Discovery Scan for: {keyword}")
        elements = self.page.query_selector_all("input:not([type='hidden']), button, div[role='button'], div[role='combobox'], div[role='radio'], [aria-label], [placeholder]")
        
        for el in elements:
            try:
                info = el.evaluate("el => (el.innerText + el.getAttribute('aria-label') + el.getAttribute('name') + el.getAttribute('placeholder') + el.getAttribute('role')).toLowerCase()")
                if keyword.lower() in info:
                    logger.info(f"✨ Deep Match Found for {keyword}!")
                    el.scroll_into_view_if_needed()
                    if action == "input":
                        el.click(force=True)
                        self.page.keyboard.type(str(value), delay=random.randint(50, 150))
                    else:
                        if not self.physical_click_fallback(el, keyword):
                            el.click(force=True)
                    return True
            except: continue
        return self.tab_navigation_fallback(keyword, action, value)

    def tab_navigation_fallback(self, keyword, action="input", value=None):
        """خطة الطوارئ: التنقل بلوحة المفاتيح TAB"""
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

    def autonomous_blind_discovery(self):
        """الخطة التي لا تفشل: اكتشاف العناصر بالذكاء الغريزي والضغط الفيزيائي"""
        logger.warning("🚀 Critical: Activating Autonomous Blind Discovery Engine!")
        all_elements = self.page.query_selector_all("input:not([type='hidden']), [role='combobox'], [role='listbox'], [role='radio'], select, div[contenteditable='true']")
        
        for el in all_elements:
            try:
                if not el.is_visible(): continue
                
                type_attr = (el.get_attribute("type") or "").lower()
                name_attr = (el.get_attribute("name") or "").lower()
                placeholder = (el.get_attribute("placeholder") or "").lower()
                role = (el.get_attribute("role") or "").lower()
                tag = el.tag_name().lower()

                if role == "radio":
                    logger.info("🔘 Autonomous: Radio Detected - Executing Physical Click")
                    if not self.physical_click_fallback(el, "Radio_Option"):
                        el.click(force=True)
                    time.sleep(0.5)
                    break 

                elif type_attr == "password" or "pass" in name_attr:
                    logger.info("🔑 Autonomous: Password Field Detected")
                    el.fill(self.identity['password'])

                elif tag == "select" or role in ["combobox", "listbox"] or "month" in name_attr or "gender" in name_attr:
                    logger.info("🔽 Autonomous: Dropdown Detected")
                    el.click(force=True)
                    time.sleep(0.5)
                    repeat = self.identity['month'] if "month" in name_attr else self.identity['gender']
                    for _ in range(max(1, repeat)): self.page.keyboard.press("ArrowDown")
                    self.page.keyboard.press("Enter")

                elif tag == "input" or type_attr == "text":
                    logger.info(f"📝 Autonomous: Text Field Detected [{name_attr}]")
                    if "day" in name_attr or "day" in placeholder: el.fill(self.identity['day'])
                    elif "year" in name_attr or "year" in placeholder: el.fill(self.identity['year'])
                    elif "first" in name_attr or "name" in placeholder: el.fill(self.identity['first_name'])
                    else: el.fill(self.identity['username_choice'])
            except: continue
        self.page.keyboard.press("Enter")

    def smart_input(self, selector_list, value, label):
        self.take_evidence(f"PRE_INPUT_{label}")
        success = False
        for selector in selector_list:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=7000)
                el = self.page.locator(selector).first
                el.click(force=True)
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
        self.take_evidence(f"PRE_CLICK_{label}")
        clicked = False
        for selector in selector_list:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=5000):
                    # نجمع بين الضغط العادي والفيزيائي لضمان الكسر
                    if not self.physical_click_fallback(btn, label):
                        btn.click(force=True)
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
        skip_selectors = ['button:has-text("تخطي")', 'button:has-text("Skip")', 'button:has-text("Not now")']
        logger.info("Scanning for 'Skip' options...")
        for _ in range(3):
            time.sleep(1.5)
            found_skip = False
            for selector in skip_selectors:
                try:
                    btn = self.page.locator(selector).first
                    if btn.is_visible(timeout=1000):
                        btn.click(force=True)
                        found_skip = True
                        logger.info("✨ Skip executed.")
                        self.page.wait_for_load_state("networkidle")
                        break
                except: continue
            if not found_skip: break

    def run_process(self):
        try:
            logger.info(f"Starting Registration Engine for: {self.identity['first_name']}")
            self.page.goto("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp", wait_until="networkidle")
            
            # 1. الأسماء
            self.smart_input(['input[name="firstName"]', '#firstName'], self.identity['first_name'], "FirstName")
            self.smart_input(['input[name="lastName"]', '#lastName'], self.identity['last_name'], "LastName")
            self.smart_click(['#collectNameNext', 'button'], "Next_Step_Names")

            # 2. الميلاد والجنس
            self.page.wait_for_load_state("networkidle")
            self.smart_input(['input[name="day"]', '#day'], self.identity['day'], "BirthDay")
            
            try:
                self.page.locator('#month').click(force=True)
                time.sleep(1)
                for _ in range(self.identity['month']): self.page.keyboard.press("ArrowDown")
                self.page.keyboard.press("Enter")
            except: self.autonomous_blind_discovery()

            self.smart_input(['input[name="year"]', '#year'], self.identity['year'], "BirthYear")
            
            try:
                self.page.locator('#gender').click(force=True)
                time.sleep(1)
                for _ in range(self.identity['gender']): self.page.keyboard.press("ArrowDown")
                self.page.keyboard.press("Enter")
            except: pass

            self.smart_click(['#birthdaygenderNext'], "Next_Step_Bio")

            # 3. اختيار الإيميل (الإصلاح الجذري: خطة @gmail الفيزيائية) 📧
            self.page.wait_for_load_state("networkidle")
            time.sleep(random.uniform(3, 5))
            
            email_selected = False
            # البحث النصي عن @gmail في كامل الشاشة (تخطي الحاويات)
            gmail_locator = self.page.get_by_text("@gmail.com")
            
            if gmail_locator.count() > 0:
                logger.info(f"🔘 Found {gmail_locator.count()} @gmail options. Executing physical selection...")
                if self.physical_click_fallback(gmail_locator.first, "Gmail_Option"):
                    email_selected = True
            
            if not email_selected:
                # محاولة البحث عن خيار "Create/إنشاء"
                create_manual = self.page.locator('text=/Create|إنشاء/').first
                if create_manual.is_visible():
                    create_manual.click(force=True)
                    self.smart_input(['input[name="Username"]'], self.identity['username_choice'], "Manual_Email")
                    email_selected = True

            self.smart_click(['#next', 'button'], "Next_Step_Email")
            
            # --- حارس البوابة (Gatekeeper Transition) ---
            try:
                self.page.wait_for_selector('input[name="Passwd"]', timeout=12000)
                logger.info("✅ Transition Confirmed: Password Page reached.")
            except:
                logger.error("❌ Transition Failed. Trying Emergency ENTER & Tab Sequence...")
                self.page.keyboard.press("Enter")
                time.sleep(3)
                if not self.page.locator('input[name="Passwd"]').is_visible():
                    self.autonomous_blind_discovery()

            # 4. كلمات المرور
            pwd = self.identity['password']
            self.smart_input(['input[name="Passwd"]'], pwd, "Password_Main")
            self.smart_input(['input[name="ConfirmPasswd"]'], pwd, "Password_Confirm")
            self.smart_click(['#createpasswordNext'], "Next_Step_Password")

            # 5. التخطي والموافقات
            self.page.wait_for_load_state("networkidle")
            self.auto_skip_manager()

            # 6. الموافقة النهائية
            agree_btn = self.page.locator('button:has-text("I agree"), button:has-text("أوافق")')
            if agree_btn.is_visible(timeout=10000):
                self.smart_click(['button:has-text("I agree")'], "Final_Agreement")

            logger.info("✅ Core Engine Finished Successfully.")

        except Exception as e:
            logger.error(f"❌ Critical Failure: {e}")
            self.take_evidence("FATAL_ERROR_REPORT")
        finally:
            self._generate_final_report()

    def _generate_final_report(self):
        """توليد التقرير النهائي (Master JSON) - نسختك الأصلية"""
        final_data = {
            "identity": self.identity,
            "trace": self.steps_log,
            "execution_status": "Finished",
            "metadata": {"engine_version": "Autonomous_Ultra_v5.0", "session": SESSION_ID}
        }
        with open(os.path.join(REPORT_DIR, "master_trace.json"), "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        logger.info(f"Report secured at: {REPORT_DIR}")

if __name__ == "__main__":
    with Camoufox(headless=True, humanize=True) as browser:
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        UltimateEngine(page).run_process()
