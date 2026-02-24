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

# --- إعداد السجلات الاحترافية ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UltimateGoogleBot")

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
        """توليد هوية رقمية معقدة وشاملة"""
        pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + "+*"
        pwd = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice("+*")
        ]
        pwd += [random.choice(pool) for _ in range(12)]
        random.shuffle(pwd)
        final_password = "".join(pwd)

        first = self.fake.first_name()
        last = self.fake.last_name()
        
        return {
            "id": str(uuid.uuid4()),
            "first_name": first,
            "last_name": last,
            "day": str(random.randint(1, 28)),
            "month": random.randint(1, 12),
            "year": str(random.randint(1990, 2003)),
            "gender": random.randint(1, 2), 
            "password": final_password,
            "username_choice": f"{first.lower()}{last.lower()}{random.randint(10000, 999999)}"
        }

    def take_evidence(self, action_label):
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

    # --- [ ميزة القناص الفيزيائي ] ---
    def physical_click_fallback(self, element, label):
        try:
            box = element.bounding_box()
            if box:
                center_x = box['x'] + box['width'] / 2
                center_y = box['y'] + box['height'] / 2
                logger.info(f"🖱️ Physical Click at ({center_x}, {center_y}) for {label}")
                self.page.mouse.click(center_x, center_y)
                return True
        except: pass
        return False

    # --- [ ميزة الاستكشاف العميق Deep DOM ] ---
    def deep_dom_discovery(self, keyword, action="input", value=None):
        logger.info(f"🔍 Deep Discovery Scan for: {keyword}")
        # تحسين: البحث عن كلمات جزئية لزيادة الدقة
        search_terms = keyword.lower().split('_')
        
        elements = self.page.query_selector_all("input:not([type='hidden']), button, div[role='button'], div[role='combobox'], div[role='radio'], [aria-label], [placeholder]")
        
        for el in elements:
            try:
                info = el.evaluate("el => (el.innerText + el.getAttribute('aria-label') + (el.name || '') + (el.placeholder || '') + (el.getAttribute('role') || '')).toLowerCase()")
                if any(term in info for term in search_terms):
                    logger.info(f"✨ Deep Match Found for {keyword}!")
                    el.scroll_into_view_if_needed()
                    if action == "input":
                        el.click(force=True)
                        self.page.keyboard.press("Control+A")
                        self.page.keyboard.press("Backspace")
                        self.page.keyboard.type(str(value), delay=random.randint(50, 150))
                    else:
                        if not self.physical_click_fallback(el, keyword):
                            el.click(force=True)
                    return True
            except: continue
        return self.tab_navigation_fallback(keyword, action, value)

    # --- [ خطة الطوارئ: TAB ] ---
    def tab_navigation_fallback(self, keyword, action="input", value=None):
        logger.warning(f"⌨️ TAB Fallback for: {keyword}")
        self.page.keyboard.press("Control+Home") 
        time.sleep(0.5)
        for i in range(40):
            self.page.keyboard.press("Tab")
            time.sleep(0.1)
            active_info = self.page.evaluate("() => document.activeElement.outerHTML.toLowerCase()")
            if any(term in active_info for term in keyword.lower().split('_')):
                if action == "input":
                    self.page.keyboard.type(str(value), delay=random.randint(50, 150))
                else:
                    self.page.keyboard.press("Enter")
                return True
        return False

    # --- [ الخطة النهائية: المستكشف الذاتي الوحشي ] ---
    def autonomous_blind_discovery(self):
        logger.warning("🚀 EXECUTING BLIND DISCOVERY: Interacting with ALL elements...")
        all_elements = self.page.query_selector_all("input:not([type='hidden']), [role='combobox'], [role='listbox'], [role='radio'], select, div[contenteditable='true']")
        
        for el in all_elements:
            try:
                if not el.is_visible(): continue
                role = (el.get_attribute("role") or "").lower()
                name = (el.get_attribute("name") or "").lower()
                tag = el.tag_name().lower()

                if role == "radio":
                    if not self.physical_click_fallback(el, "Auto_Radio"): el.click(force=True)
                    time.sleep(0.5)
                elif "pass" in name or "Pass" in name:
                    el.fill(self.identity['password'])
                elif tag == "select" or role in ["combobox", "listbox"]:
                    el.click(force=True)
                    for _ in range(3): self.page.keyboard.press("ArrowDown")
                    self.page.keyboard.press("Enter")
                elif tag == "input":
                    val = self.identity['username_choice'] if "User" in name or "Email" in name else self.identity['first_name']
                    el.fill(val)
            except: continue
        self.page.keyboard.press("Enter")
        time.sleep(2)

    # --- [ ميزة تعبئة الباسوورد التتابعي ] ---
    def handle_password_matrix(self):
        """الحل النهائي لتجاوز مشكلة حقل تأكيد كلمة المرور"""
        logger.info("🔐 Deploying Password Matrix Strategy...")
        pwd = self.identity['password']
        self.take_evidence("PRE_PASS_MATRIX")
        
        try:
            # 1. البحث عن كافة حقول الباسوورد
            fields = self.page.locator('input[type="password"]').all()
            if len(fields) >= 2:
                for i, field in enumerate(fields):
                    field.fill(pwd)
                    logger.info(f"✅ Matrix: Filled password field #{i+1}")
                return True
            
            # 2. إذا لم يجدها بالنوع، يبحث عنها بالاستكشاف العميق
            success1 = self.smart_input(['input[name="Passwd"]'], pwd, "Passwd")
            success2 = self.smart_input(['input[name="ConfirmPasswd"]'], pwd, "ConfirmPasswd")
            return success1 and success2
        except Exception as e:
            logger.error(f"Matrix Failure: {e}")
            return False

    def smart_input(self, selector_list, value, label):
        self.take_evidence(f"PRE_INPUT_{label}")
        success = False
        for selector in selector_list:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=5000)
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
                return False
        self.take_evidence(f"POST_INPUT_{label}")
        return True

    def smart_click(self, selector_list, label, is_optional=False):
        self.take_evidence(f"PRE_CLICK_{label}")
        clicked = False
        for selector in selector_list:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=5000):
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
            self.take_evidence(f"POST_CLICK_{label}")
            time.sleep(random.uniform(2, 4)) 
        elif not is_optional:
            raise Exception(f"CRITICAL: Failed to click {label}")

    def auto_skip_manager(self):
        skip_selectors = ['button:has-text("تخطي")', 'button:has-text("Skip")', 'button:has-text("Not now")']
        for _ in range(3):
            time.sleep(1.5)
            for selector in skip_selectors:
                try:
                    btn = self.page.locator(selector).first
                    if btn.is_visible(timeout=1000):
                        btn.click(force=True)
                        break
                except: continue

    def run_process(self):
        try:
            logger.info(f"Starting Engine for: {self.identity['first_name']}")
            self.page.goto("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp", wait_until="networkidle")
            
            # 1. الأسماء
            self.smart_input(['input[name="firstName"]'], self.identity['first_name'], "FirstName")
            self.smart_input(['input[name="lastName"]'], self.identity['last_name'], "LastName")
            self.smart_click(['#collectNameNext', 'button'], "Next_Names")

            # 2. الميلاد
            self.page.wait_for_load_state("networkidle")
            self.smart_input(['input[name="day"]'], self.identity['day'], "BirthDay")
            self.smart_input(['input[name="year"]'], self.identity['year'], "BirthYear")
            
            for sel in ['#month', '#gender']:
                try:
                    self.page.locator(sel).click(force=True)
                    time.sleep(1)
                    repeat = self.identity['month'] if "month" in sel else self.identity['gender']
                    for _ in range(repeat): self.page.keyboard.press("ArrowDown")
                    self.page.keyboard.press("Enter")
                except: self.deep_dom_discovery(sel, "click")
            
            self.smart_click(['#birthdaygenderNext'], "Next_Bio")

            # 3. اختيار الإيميل
            self.page.wait_for_load_state("networkidle")
            time.sleep(4)
            
            user_field = self.page.locator('input[name="Username"]').first
            if user_field.is_visible():
                self.smart_input(['input[name="Username"]'], self.identity['username_choice'], "Username")
            else:
                gmail_suggestions = self.page.get_by_text("@gmail.com")
                if gmail_suggestions.count() > 0:
                    self.physical_click_fallback(gmail_suggestions.first, "Gmail_Suggestion")
                else:
                    self.deep_dom_discovery("Create", "click")
                    self.smart_input(['input[name="Username"]'], self.identity['username_choice'], "Username")

            self.smart_click(['#next', 'button', '#selectionNext'], "Next_Email")

            # 4. باسوورد (استدعاء مصفوفة القوة الجديدة)
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)
            self.handle_password_matrix()
            self.smart_click(['#createpasswordNext', 'button'], "Next_Password")

            # 5. الموافقات
            self.auto_skip_manager()
            self.smart_click(['button:has-text("I agree"), button:has-text("أوافق")'], "Final_Agreement", True)

            logger.info("✅ Mission Accomplished.")

        except Exception as e:
            logger.error(f"❌ Critical Failure: {e}")
            self.take_evidence("FATAL_ERROR")
        finally:
            self._generate_final_report()

    def _generate_final_report(self):
        final_data = {"identity": self.identity, "steps": self.steps_log, "session": SESSION_ID}
        with open(os.path.join(REPORT_DIR, "master_trace.json"), "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    with Camoufox(headless=True, humanize=True) as browser:
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        UltimateEngine(page).run_process()
