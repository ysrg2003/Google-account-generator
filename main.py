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
logger = logging.getLogger("UltimateGhostEngine")

SESSION_ID = f"PRO_GHOST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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
        """توليد هوية رقمية معقدة لضمان تخطي الفلاتر"""
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

    # --- [ ميزات الأنسنة المضافة حديثاً ] ---
    def human_jitter(self, min_s=2, max_s=5):
        """توقف عشوائي لمحاكاة التردد البشري"""
        delay = random.uniform(min_s, max_s)
        time.sleep(delay)

    def human_mouse_move(self, element=None):
        """تحريك الماوس بشكل غير خطي فوق العنصر"""
        try:
            if element:
                box = element.bounding_box()
                if box:
                    self.page.mouse.move(
                        box['x'] + random.randint(0, int(box['width'])), 
                        box['y'] + random.randint(0, int(box['height'])),
                        steps=random.randint(5, 15)
                    )
            else:
                self.page.mouse.move(random.randint(100, 800), random.randint(100, 600), steps=10)
        except: pass

    def fake_scroll_behavior(self):
        """محاكاة قراءة الصفحة"""
        try:
            for _ in range(random.randint(2, 4)):
                self.page.mouse.wheel(0, random.randint(150, 400))
                time.sleep(random.uniform(0.3, 0.8))
            self.page.mouse.wheel(0, -random.randint(400, 800))
        except: pass

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

    def physical_click_fallback(self, element, label):
        """الضغط عبر إحداثيات الشاشة مع حركة ماوس بشرية"""
        try:
            self.human_mouse_move(element)
            box = element.bounding_box()
            if box:
                center_x = box['x'] + box['width'] / 2
                center_y = box['y'] + box['height'] / 2
                logger.info(f"🖱️ Physical Click at ({center_x}, {center_y}) for {label}")
                self.page.mouse.click(center_x, center_y)
                return True
        except: pass
        return False

    def deep_dom_discovery(self, keyword, action="input", value=None):
        logger.info(f"🔍 Deep Discovery Scan for: {keyword}")
        search_terms = keyword.lower().split('_')
        elements = self.page.query_selector_all("input:not([type='hidden']), button, div[role='button'], div[role='combobox'], div[role='radio'], [aria-label], [placeholder]")
        
        for el in elements:
            try:
                info = el.evaluate("el => (el.innerText + el.getAttribute('aria-label') + (el.name || '') + (el.placeholder || '') + (el.getAttribute('role') || '')).toLowerCase()")
                if any(term in info for term in search_terms):
                    logger.info(f"✨ Deep Match Found for {keyword}!")
                    el.scroll_into_view_if_needed()
                    self.human_mouse_move(el)
                    if action == "input":
                        el.click(force=True)
                        self.page.keyboard.press("Control+A")
                        self.page.keyboard.press("Backspace")
                        self.page.keyboard.type(str(value), delay=random.randint(100, 250))
                    else:
                        if not self.physical_click_fallback(el, keyword):
                            el.click(force=True)
                    return True
            except: continue
        return self.tab_navigation_fallback(keyword, action, value)

    def tab_navigation_fallback(self, keyword, action="input", value=None):
        logger.warning(f"⌨️ TAB Fallback for: {keyword}")
        self.page.keyboard.press("Control+Home") 
        time.sleep(0.5)
        for i in range(40):
            self.page.keyboard.press("Tab")
            time.sleep(random.uniform(0.1, 0.3))
            active_info = self.page.evaluate("() => document.activeElement.outerHTML.toLowerCase()")
            if any(term in active_info for term in keyword.lower().split('_')):
                if action == "input":
                    self.page.keyboard.type(str(value), delay=random.randint(100, 250))
                else:
                    self.page.keyboard.press("Enter")
                return True
        return False

    def autonomous_blind_discovery(self):
        """يتفاعل مع كل شيء متاح في الصفحة لكسر الجمود"""
        logger.warning("🚀 EXECUTING BLIND DISCOVERY...")
        all_elements = self.page.query_selector_all("input:not([type='hidden']), [role='combobox'], [role='radio'], select")
        
        for el in all_elements:
            try:
                if not el.is_visible(): continue
                name = (el.get_attribute("name") or "").lower()
                tag = el.tag_name().lower()

                if "pass" in name:
                    el.fill(self.identity['password'])
                elif tag == "input":
                    el.fill(self.identity['first_name'])
                self.human_jitter(1, 2)
            except: continue
        self.page.keyboard.press("Enter")

    def handle_password_matrix(self):
        """تعبئة تتابعية لحقول الباسوورد مع تأخير بشري"""
        logger.info("🔐 Deploying Stealth Password Matrix...")
        pwd = self.identity['password']
        self.take_evidence("PRE_PASS_MATRIX")
        try:
            fields = self.page.locator('input[type="password"]').all()
            if len(fields) >= 2:
                for i, field in enumerate(fields):
                    self.human_mouse_move(field)
                    field.click()
                    self.page.keyboard.type(pwd, delay=random.randint(100, 200))
                    logger.info(f"✅ Matrix: Filled field #{i+1}")
                    self.human_jitter(1, 3)
                return True
            # Fallback للبحث المباشر إذا لم يجد النوع
            self.smart_input(['input[name="Passwd"]'], pwd, "Passwd")
            self.smart_input(['input[name="ConfirmPasswd"]'], pwd, "ConfirmPasswd")
            return True
        except: return False

    def smart_input(self, selector_list, value, label):
        self.take_evidence(f"PRE_INPUT_{label}")
        self.human_jitter(1, 3)
        success = False
        for selector in selector_list:
            try:
                el = self.page.locator(selector).first
                if el.is_visible(timeout=5000):
                    self.human_mouse_move(el)
                    el.click()
                    self.page.keyboard.type(str(value), delay=random.randint(100, 250))
                    success = True
                    break
            except: continue
        
        if not success:
            success = self.deep_dom_discovery(label, "input", value)
        self.take_evidence(f"POST_INPUT_{label}")
        return success

    def smart_click(self, selector_list, label, is_optional=False):
        self.take_evidence(f"PRE_CLICK_{label}")
        self.human_jitter(2, 4)
        clicked = False
        for selector in selector_list:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=5000):
                    self.human_mouse_move(btn)
                    if not self.physical_click_fallback(btn, label):
                        btn.click(force=True)
                    clicked = True
                    break
            except: continue
        
        if not clicked and not is_optional:
            if not self.deep_dom_discovery(label, "click"):
                self.page.keyboard.press("Enter")
                clicked = True
        if clicked: self.take_evidence(f"POST_CLICK_{label}")

    def run_process(self):
        try:
            logger.info(f"Starting Engine for: {self.identity['first_name']}")
            self.page.goto("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp", wait_until="networkidle")
            self.human_jitter(3, 6)
            
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
                    self.page.locator(sel).click()
                    repeat = self.identity['month'] if "month" in sel else self.identity['gender']
                    for _ in range(repeat): self.page.keyboard.press("ArrowDown")
                    self.page.keyboard.press("Enter")
                except: self.deep_dom_discovery(sel, "click")
            
            self.smart_click(['#birthdaygenderNext'], "Next_Bio")

            # 3. اختيار الإيميل
            self.human_jitter(4, 7)
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

            self.smart_click(['#next', 'button'], "Next_Email")

            # 4. باسوورد (المصفوفة المطورة)
            self.human_jitter(3, 5)
            self.handle_password_matrix()
            self.smart_click(['#createpasswordNext', 'button'], "Next_Password")

            # 5. الموافقات
            self.fake_scroll_behavior()
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
        # استخدام User Agent ثابت ومعروف لتقليل الشك
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        UltimateEngine(page).run_process()
