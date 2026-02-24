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
        pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + "+*"
        pwd = [random.choice(string.ascii_uppercase), random.choice(string.ascii_lowercase), random.choice(string.digits), random.choice("+*")]
        pwd += [random.choice(pool) for _ in range(12)]
        random.shuffle(pwd)
        return {
            "id": str(uuid.uuid4()),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "day": str(random.randint(1, 28)),
            "month": random.randint(1, 12),
            "year": str(random.randint(1990, 2003)),
            "gender": random.randint(1, 2), 
            "password": "".join(pwd),
            "username_choice": f"{self.fake.user_name().replace('.', '')}{random.randint(1000, 99999)}"
        }

    def take_evidence(self, action_label):
        self.step_idx += 1
        ts = datetime.now().strftime("%H%M%S_%f")
        filename = f"{self.step_idx:03d}_{action_label}.png"
        path = os.path.join(REPORT_DIR, "screenshots", filename)
        try:
            self.page.screenshot(path=path, full_page=True)
            self.steps_log.append({"step": self.step_idx, "label": action_label, "screenshot": filename})
        except: pass

    # --- [ الخطة 1: القناص الفيزيائي ] ---
    def physical_click(self, element, label):
        try:
            box = element.bounding_box()
            if box:
                cx, cy = box['x'] + box['width']/2, box['y'] + box['height']/2
                logger.info(f"🖱️ Physical Click: {label} at ({cx}, {cy})")
                self.page.mouse.click(cx, cy)
                return True
        except: return False

    # --- [ الخطة 2: استكشاف الكود المصدري Deep DOM ] ---
    def deep_dom_discovery(self, keyword, action="input", value=None):
        logger.info(f"🔍 Deep DOM Search: {keyword}")
        elements = self.page.query_selector_all("input:not([type='hidden']), button, [role='button'], [role='radio'], [placeholder], div")
        for el in elements:
            try:
                # فحص شامل لكل النصوص والسمات المرتبطة بالعنصر
                info = el.evaluate("el => (el.innerText + el.getAttribute('aria-label') + el.getAttribute('name') + el.getAttribute('placeholder') + el.getAttribute('role') + el.id).toLowerCase()")
                if keyword.lower() in info and el.is_visible():
                    el.scroll_into_view_if_needed()
                    if action == "input":
                        el.click(force=True)
                        self.page.keyboard.type(str(value), delay=100)
                    else:
                        if not self.physical_click(el, keyword): el.click(force=True)
                    return True
            except: continue
        return False

    # --- [ الخطة 3: التنقل عبر TAB ] ---
    def tab_fallback(self, keyword, action="input", value=None):
        logger.warning(f"⌨️ TAB Navigation: {keyword}")
        self.page.keyboard.press("Control+Home")
        for _ in range(45):
            self.page.keyboard.press("Tab")
            time.sleep(0.1)
            active_info = self.page.evaluate("() => document.activeElement.outerHTML.toLowerCase()")
            if keyword.lower() in active_info:
                if action == "input": self.page.keyboard.type(str(value))
                else: self.page.keyboard.press("Enter")
                return True
        return False

    # --- [ الخطة 4: إعادة تشغيل جميع الخطط واستكشاف كل شيء (The Monster) ] ---
    def autonomous_blind_discovery(self):
        """يتفاعل مع كل عنصر تفاعلي في الصفحة بالترتيب"""
        logger.warning("🚀 CRITICAL: Unleashing Autonomous Blind Discovery Engine!")
        
        # 1. التفاعل مع الحقول والقوائم والراديو
        all_els = self.page.query_selector_all("input:not([type='hidden']), [role='radio'], [role='combobox'], select, div[contenteditable='true']")
        for el in all_els:
            try:
                if not el.is_visible(): continue
                name = (el.get_attribute("name") or "").lower()
                role = (el.get_attribute("role") or "").lower()
                tag = el.tag_name().lower()

                if "pass" in name or "Pass" in name or el.get_attribute("type") == "password":
                    el.fill(self.identity['password'])
                elif role == "radio" or "option" in role:
                    self.physical_click(el, "Auto_Radio")
                elif tag == "select" or "month" in name or "gender" in name:
                    el.click()
                    self.page.keyboard.press("ArrowDown")
                    self.page.keyboard.press("Enter")
                elif tag == "input" and not el.input_value():
                    val = self.identity['username_choice'] if "user" in name else self.identity['first_name']
                    el.fill(val)
            except: continue

        # 2. البحث عن أزرار الاستمرار والضغط عليها
        time.sleep(1)
        self.page.keyboard.press("Enter") # محاولة الضغط على Enter أولاً
        
        btn_keywords = ["Next", "التالي", "Agree", "أوافق", "Skip", "تخطي", "Submit"]
        for kw in btn_keywords:
            if self.deep_dom_discovery(kw, "click"):
                logger.info(f"✨ Autonomous Engine found and clicked: {kw}")
                break

    def smart_input(self, selector_list, value, label):
        self.take_evidence(f"PRE_{label}")
        success = False
        # جولة 1: المحاولة المباشرة
        for s in selector_list:
            try:
                el = self.page.locator(s).first
                if el.is_visible(timeout=4000):
                    el.click(force=True)
                    el.fill(str(value))
                    success = True; break
            except: continue
        
        # جولة 2: الخطط الاحتياطية المتسلسلة
        if not success:
            logger.warning(f"Plan A failed for {label}. Executing deep recovery...")
            if not self.deep_dom_discovery(label, "input", value):
                if not self.tab_fallback(label, "input", value):
                    self.autonomous_blind_discovery()
        
        self.take_evidence(f"POST_{label}")

    def smart_click(self, selector_list, label, is_optional=False):
        self.take_evidence(f"PRE_CLICK_{label}")
        success = False
        for s in selector_list:
            try:
                btn = self.page.locator(s).first
                if btn.is_visible(timeout=4000):
                    if not self.physical_click(btn, label): btn.click(force=True)
                    success = True; break
            except: continue
        
        if not success and not is_optional:
            if not self.deep_dom_discovery(label, "click"):
                if not self.tab_fallback(label, "click"):
                    self.page.keyboard.press("Enter")
        
        self.take_evidence(f"POST_CLICK_{label}")
        time.sleep(random.uniform(2, 4))

    def run_process(self):
        try:
            logger.info("Starting Registration Process...")
            self.page.goto("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp", wait_until="networkidle")
            
            # 1. المرحلة الأولى: الأسماء
            self.smart_input(['input[name="firstName"]'], self.identity['first_name'], "FirstName")
            self.smart_input(['input[name="lastName"]'], self.identity['last_name'], "LastName")
            self.smart_click(['#collectNameNext', 'button'], "Next_Step_Names")

            # 2. المرحلة الثانية: الميلاد
            self.page.wait_for_load_state("networkidle")
            self.smart_input(['input[name="day"]'], self.identity['day'], "BirthDay")
            self.smart_input(['input[name="year"]'], self.identity['year'], "BirthYear")
            
            for sel in ['#month', '#gender']:
                try:
                    self.page.locator(sel).click(force=True)
                    time.sleep(0.5)
                    repeat = self.identity['month'] if "month" in sel else self.identity['gender']
                    for _ in range(repeat): self.page.keyboard.press("ArrowDown")
                    self.page.keyboard.press("Enter")
                except: self.deep_dom_discovery(sel, "click")
            
            self.smart_click(['#birthdaygenderNext'], "Next_Step_Bio")

            # 3. المرحلة الثالثة: الإيميل
            self.page.wait_for_load_state("networkidle")
            time.sleep(3)
            
            # فحص خيارات الراديو (Suggestions) أولاً
            radio_opts = self.page.locator('div[role="radio"]')
            if radio_opts.count() > 0:
                self.physical_click(radio_opts.first, "Gmail_Radio_Option")
            else:
                self.smart_input(['input[name="Username"]'], self.identity['username_choice'], "Manual_Email")

            self.smart_click(['#next', 'button'], "Next_Step_Email")

            # حارس البوابة (التحقق من العبور لصفحة الباسوورد)
            try:
                self.page.wait_for_selector('input[name="Passwd"]', timeout=8000)
            except:
                logger.warning("Stuck at Email screen. Unleashing the Monster...")
                self.autonomous_blind_discovery()

            # 4. المرحلة الرابعة: الباسوورد
            self.smart_input(['input[name="Passwd"]'], self.identity['password'], "Password_Main")
            self.smart_input(['input[name="ConfirmPasswd"]'], self.identity['password'], "Password_Confirm")
            self.smart_click(['#createpasswordNext'], "Next_Step_Password")

            # 5. المرحلة الخامسة: التخطي والموافقات
            self.smart_click(['button:has-text("Skip")', 'button:has-text("تخطي")'], "Skip_Phone", True)
            self.smart_click(['button:has-text("I agree")', 'button:has-text("أوافق")'], "Final_Agreement", True)

            logger.info("✅ Core Engine Finished the Mission Successfully.")

        except Exception as e:
            logger.error(f"❌ Critical Failure: {e}")
            self.take_evidence("FATAL_ERROR")
        finally:
            self._generate_final_report()

    def _generate_final_report(self):
        final_data = {"identity": self.identity, "trace": self.steps_log, "metadata": {"engine": "v5.0_Full_Monster"}}
        with open(os.path.join(REPORT_DIR, "master_trace.json"), "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    with Camoufox(headless=True, humanize=True) as browser:
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        UltimateEngine(page).run_process()
