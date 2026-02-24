import json
import time
import os
import random
import string
import logging
import uuid
import re
import numpy as np
from datetime import datetime
from faker import Faker
from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError

# --- إعداد السجلات الاحترافية ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GhostEngine_Pro")

SESSION_ID = f"PRO_ENGINE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
REPORT_DIR = os.path.join(os.getcwd(), SESSION_ID)
os.makedirs(os.path.join(REPORT_DIR, "screenshots"), exist_ok=True) 

class UltimateEngine:
    def __init__(self, page):
        self.page = page
        # 1. منطق التوافق: لغة متناسقة مع الموقع المختار
        self.fake = Faker(['en_US', 'ar_SA'])
        self.identity = self._generate_identity()
        self.steps_log = []
        self.step_idx = 0

    def _generate_identity(self):
        """توليد هوية رقمية معقدة وشاملة (كودك الأصلي)"""
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

    # --- [ 7. منطق الحركة غير الخطية للماوس (Bezier Curves) ] ---
    def _bezier_move(self, target_x, target_y):
        """تحريك الماوس بمعادلة بيزيه: $B(t) = (1-t)^2 P_0 + 2(1-t)t P_1 + t^2 P_2$"""
        try:
            # نقطة البداية الحالية (أو نقطة عشوائية)
            start_x = random.randint(0, 500)
            start_y = random.randint(0, 500)
            steps = random.randint(15, 30)
            t = np.linspace(0, 1, steps)
            
            # نقطة تحكم عشوائية لخلق انحناء طبيعي
            cx = start_x + (target_x - start_x) * random.uniform(0.1, 0.4)
            cy = start_y + (target_y - start_y) * random.uniform(0.6, 0.9)
            
            x_pts = (1-t)**2 * start_x + 2*(1-t)*t * cx + t**2 * target_x
            y_pts = (1-t)**2 * start_y + 2*(1-t)*t * cy + t**2 * target_y
            
            for x, y in zip(x_pts, y_pts):
                self.page.mouse.move(x, y)
                time.sleep(random.uniform(0.002, 0.005))
        except: pass

    # --- [ 4. منطق الكتابة البشرية (Natural Typing) ] ---
    def _human_type(self, text):
        """كتابة النص مع تأخير عشوائي (Action Jitter) وتصحيح وهمي"""
        for char in str(text):
            self.page.keyboard.type(char, delay=random.randint(100, 300))
            if random.random() > 0.97: # محاكاة خطأ مطبعي أحياناً
                time.sleep(random.uniform(0.1, 0.3))
                self.page.keyboard.press("Backspace")
                self.page.keyboard.type(char, delay=random.randint(50, 150))

    # --- [ 13. التمرير الوهمي (Fake Scrolling) ] ---
    def _human_scroll(self):
        for _ in range(random.randint(2, 4)):
            self.page.mouse.wheel(0, random.randint(300, 600))
            time.sleep(random.uniform(0.8, 1.5))
            if random.random() > 0.6: # صعود طفيف كأننا نقرأ
                self.page.mouse.wheel(0, -random.randint(100, 200))

    # --- [ 6. منطق تسخين الكوكيز (Pre-baked Cookies) ] ---
    def _pre_warmup(self):
        logger.info("🍪 Warming up browser with Google Search...")
        try:
            self.page.goto("https://www.google.com")
            time.sleep(random.uniform(2, 4))
            search_box = self.page.locator('textarea[name="q"], input[name="q"]').first
            if search_box.is_visible():
                self._bezier_move(500, 500) # تحريك وهمي
                search_box.click()
                self._human_type(random.choice(["top tech news 2026", "how to bake cake", "weather"]))
                self.page.keyboard.press("Enter")
                time.sleep(random.uniform(3, 5))
                self._human_scroll()
        except: pass

    def take_evidence(self, action_label):
        self.step_idx += 1
        ts = datetime.now().strftime("%H%M%S_%f")
        filename = f"{self.step_idx:03d}_{action_label}_{ts}.png"
        save_path = os.path.join(REPORT_DIR, "screenshots", filename)
        try:
            self.page.screenshot(path=save_path, full_page=True)
            self.steps_log.append({"step_index": self.step_idx, "label": action_label, "timestamp": ts, "url": self.page.url, "screenshot": filename})
        except: pass

    # --- [ ميزة القناص الفيزيائي المطورة ] ---
    def physical_click_fallback(self, element, label):
        try:
            box = element.bounding_box()
            if box:
                center_x = box['x'] + box['width'] / 2
                center_y = box['y'] + box['height'] / 2
                logger.info(f"🖱️ Physical Human Click for {label}")
                # 7+12. تحريك بالمنحنيات + التحويم قبل الضغط
                self._bezier_move(center_x, center_y)
                time.sleep(random.uniform(0.3, 0.8))
                self.page.mouse.click(center_x, center_y)
                return True
        except: pass
        return False

    # --- [ ميزة الاستكشاف العميق Deep DOM (كودك الأصلي بالكامل) ] ---
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
                    if action == "input":
                        self.physical_click_fallback(el, keyword)
                        self.page.keyboard.press("Control+A")
                        self.page.keyboard.press("Backspace")
                        self._human_type(value)
                    else:
                        if not self.physical_click_fallback(el, keyword): el.click(force=True)
                    return True
            except: continue
        return self.tab_navigation_fallback(keyword, action, value)

    # --- [ خطة الطوارئ: TAB (كودك الأصلي) ] ---
    def tab_navigation_fallback(self, keyword, action="input", value=None):
        logger.warning(f"⌨️ TAB Fallback for: {keyword}")
        self.page.keyboard.press("Control+Home") 
        time.sleep(0.5)
        for i in range(40):
            self.page.keyboard.press("Tab")
            time.sleep(random.uniform(0.1, 0.2))
            active_info = self.page.evaluate("() => document.activeElement.outerHTML.toLowerCase()")
            if any(term in active_info for term in keyword.lower().split('_')):
                if action == "input": self._human_type(value)
                else: self.page.keyboard.press("Enter")
                return True
        return False

    # --- [ الخطة النهائية: المستكشف الذاتي الوحشي (كودك الأصلي) ] ---
    def autonomous_blind_discovery(self):
        logger.warning("🚀 EXECUTING BLIND DISCOVERY...")
        all_elements = self.page.query_selector_all("input:not([type='hidden']), [role='combobox'], [role='listbox'], [role='radio'], select, div[contenteditable='true']")
        for el in all_elements:
            try:
                if not el.is_visible(): continue
                role = (el.get_attribute("role") or "").lower(); name = (el.get_attribute("name") or "").lower(); tag = el.tag_name().lower()
                if role == "radio":
                    self.physical_click_fallback(el, "Auto_Radio")
                    time.sleep(0.5)
                elif "pass" in name or "Pass" in name:
                    self.physical_click_fallback(el, "Auto_Pass"); self._human_type(self.identity['password'])
                elif tag == "select" or role in ["combobox", "listbox"]:
                    el.click(); [self.page.keyboard.press("ArrowDown") for _ in range(3)]; self.page.keyboard.press("Enter")
                elif tag == "input":
                    val = self.identity['username_choice'] if "User" in name or "Email" in name else self.identity['first_name']
                    self.physical_click_fallback(el, "Auto_Input"); self._human_type(val)
            except: continue
        self.page.keyboard.press("Enter")
        time.sleep(2)

    # --- [ ميزة تعبئة الباسوورد التتابعي (كودك الأصلي) ] ---
    def handle_password_matrix(self):
        logger.info("🔐 Deploying Password Matrix Strategy...")
        pwd = self.identity['password']
        self.take_evidence("PRE_PASS_MATRIX")
        try:
            fields = self.page.locator('input[type="password"]').all()
            if len(fields) >= 2:
                for i, field in enumerate(fields):
                    self.physical_click_fallback(field, f"PassField_{i}")
                    self._human_type(pwd)
                return True
            success1 = self.smart_input(['input[name="Passwd"]'], pwd, "Passwd")
            success2 = self.smart_input(['input[name="ConfirmPasswd"]'], pwd, "ConfirmPasswd")
            return success1 and success2
        except Exception as e:
            logger.error(f"Matrix Failure: {e}"); return False

    def smart_input(self, selector_list, value, label):
        self.take_evidence(f"PRE_INPUT_{label}")
        success = False
        for selector in selector_list:
            try:
                self.page.wait_for_selector(selector, state="visible", timeout=5000)
                el = self.page.locator(selector).first
                self.physical_click_fallback(el, label)
                self.page.keyboard.press("Control+A")
                self.page.keyboard.press("Backspace")
                self._human_type(value)
                success = True; break
            except: continue
        if not success:
            if not self.deep_dom_discovery(label, "input", value): return False
        self.take_evidence(f"POST_INPUT_{label}"); return True

    def smart_click(self, selector_list, label, is_optional=False):
        self.take_evidence(f"PRE_CLICK_{label}")
        clicked = False
        for selector in selector_list:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=5000):
                    clicked = self.physical_click_fallback(btn, label)
                    if clicked: break
            except: continue
        if not clicked and not is_optional:
            if not self.deep_dom_discovery(label, "click"):
                self.page.keyboard.press("Enter"); clicked = True
        if clicked:
            self.take_evidence(f"POST_CLICK_{label}")
            # 8+11. انتظار ذكي + تردد عشوائي
            time.sleep(random.uniform(3, 6)) 
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
                        self.physical_click_fallback(btn, "Skip"); break
                except: continue

    def run_process(self):
        try:
            # 6. التدفئة المسبقة
            self._pre_warmup()
            
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
                    el = self.page.locator(sel).first
                    self.physical_click_fallback(el, sel)
                    time.sleep(1)
                    repeat = self.identity['month'] if "month" in sel else self.identity['gender']
                    for _ in range(repeat): 
                        self.page.keyboard.press("ArrowDown")
                        time.sleep(0.1)
                    self.page.keyboard.press("Enter")
                except: self.deep_dom_discovery(sel, "click")
            
            self.smart_click(['#birthdaygenderNext'], "Next_Bio")

            # 3. اختيار الإيميل
            self.page.wait_for_load_state("networkidle")
            time.sleep(random.uniform(4, 6))
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

            # 4. باسوورد
            self.page.wait_for_load_state("networkidle"); time.sleep(2)
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
    # إعدادات التخفي: سنبقيها بسيطة جداً لتجنب أخطاء المسميات (UnknownProperty)
    # المكتبة ستفعل التمويه تلقائياً لأننا وضعنا humanize=True بالأسفل
    ghost_config = {
        "webrtc": "block",  # ضروري جداً لمنع تسريب IP السيرفر
    }
    
    os_choice = random.choice(["windows", "macos"])
    logger.info(f"🎭 Launching Engine with {os_choice} profile...")

    try:
        with Camoufox(
            headless=False,       # ليعمل داخل xvfb في GitHub Actions
            humanize=True,        # هذا الخيار هو "السحر" الذي يخفي البوت
            os=os_choice,
            config=ghost_config   
        ) as browser:
            
            # ضبط السياق ليكون متسقاً مع الهوية المختارة
            context = browser.new_context(
                locale="en-US",
                timezone_id="America/New_York",
                viewport={"width": 1366, "height": 768}
            )
            
            page = context.new_page()
            
            # استدعاء المحرك "المتوحش" الخاص بك
            UltimateEngine(page).run_process()
            
    except Exception as e:
        logger.error(f"❌ Initialization Error: {e}")

