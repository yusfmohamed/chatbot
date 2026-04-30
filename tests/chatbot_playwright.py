# ══════════════════════════════════════════════════════════════════
#  chatbot_playwright.py  –  Playwright UI Tests for ChatBot Website
#  Tests: Sign Up, Sign In, Validation, Logout, Contact Form, Chat
# ══════════════════════════════════════════════════════════════════

from playwright.sync_api import sync_playwright, expect
import time
import json

# ── CONFIG ────────────────────────────────────────────────────────
SITE_URL    = "http://127.0.0.1:5500/index.html"
CHAT_URL    = "http://127.0.0.1:5500/chat.html"
HEADLESS    = False   # Set True to run without opening a browser window

# ── Test counters ─────────────────────────────────────────────────
passed = 0
failed = 0

def log(status, test_name, detail=""):
    global passed, failed
    icon = "✅ PASS" if status else "❌ FAIL"
    if status:
        passed += 1
    else:
        failed += 1
    detail_str = f" → {detail}" if detail else ""
    print(f"  {icon}: {test_name}{detail_str}")

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════

def clear_session(page):
    """Wipe sessionStorage so each test starts clean."""
    page.evaluate("sessionStorage.clear()")

def open_signup_modal(page):
    """Click Sign Up in navbar and switch to the Sign Up tab."""
    page.click(".sign-up-btn")
    page.wait_for_selector("#authOverlay", state="visible")
    page.click("#tabSignUp")
    page.wait_for_selector("#panelSignUp", state="visible")

def open_signin_modal(page):
    """Click Sign In in navbar and wait for the panel."""
    page.click(".sign-in-btn")
    page.wait_for_selector("#authOverlay", state="visible")
    page.wait_for_selector("#panelSignIn",  state="visible")

def fill_signup_form(page,
                     first="Youssef",    last="Mohamed",
                     gender="male",      nationality="Egyptian",
                     study="software_engineering",
                     username="youssef_test01",
                     gmail="youssef.test01@gmail.com",
                     password="SecurePass1!",
                     confirm="SecurePass1!"):
    page.fill("#suFirstName",   first)
    page.fill("#suLastName",    last)
    page.select_option("#suGender", gender)
    page.fill("#suNationality", nationality)
    page.select_option("#suStudy",  study)
    page.fill("#suUsername",    username)
    page.fill("#suGmail",       gmail)
    page.fill("#suPassword",    password)
    page.fill("#suConfirm",     confirm)

def click_create_account(page):
    page.locator("#panelSignUp .auth-submit-btn").click()

def close_modal_if_open(page):
    try:
        btn = page.locator("#authCloseBtn")
        if btn.is_visible():
            btn.click()
            page.wait_for_timeout(400)
    except:
        pass

def signup_fresh_user(page, username="youssef_test01",
                      gmail="youssef.test01@gmail.com"):
    """Full sign-up flow. Call clear_session(page) first."""
    open_signup_modal(page)
    fill_signup_form(page, username=username, gmail=gmail)
    click_create_account(page)
    page.wait_for_timeout(2500)   # auth.js delays modal close by 1.2 s

# ══════════════════════════════════════════════════════════════════
#  TEST 1 — Page loads correctly
# ══════════════════════════════════════════════════════════════════
def test_page_loads(page):
    print("\n📋 TEST 1: Page loads correctly")
    page.goto(SITE_URL)
    page.wait_for_load_state("domcontentloaded")

    try:
        title = page.title()
        log("CHATBOT" in title.upper() or title != "", "Page title is set", f"title='{title}'")
    except Exception as e:
        log(False, "Page title is set", str(e))

    try:
        page.wait_for_selector(".navbar", timeout=5000)
        log(True, "Navbar is present")
    except:
        log(False, "Navbar is present")

    try:
        page.wait_for_selector(".sign-in-btn", timeout=5000)
        page.wait_for_selector(".sign-up-btn", timeout=5000)
        log(True, "Sign In and Sign Up buttons visible in navbar")
    except:
        log(False, "Sign In and Sign Up buttons visible in navbar")

    try:
        page.wait_for_selector("#getStartedBtn", timeout=5000)
        log(True, "Get Started button present")
    except:
        log(False, "Get Started button present")

# ══════════════════════════════════════════════════════════════════
#  TEST 2 — Sign Up modal opens with all fields
# ══════════════════════════════════════════════════════════════════
def test_signup_modal_opens(page):
    print("\n📋 TEST 2: Sign Up modal opens")
    page.goto(SITE_URL)
    clear_session(page)

    try:
        open_signup_modal(page)
        log(True, "Auth modal appears after clicking Sign Up")
    except Exception as e:
        log(False, "Auth modal appears after clicking Sign Up", str(e))
        return

    try:
        log(page.locator("#panelSignUp").is_visible(), "Sign Up panel is visible")
    except:
        log(False, "Sign Up panel is visible")

    try:
        fields = ["suFirstName", "suLastName", "suGender", "suNationality",
                  "suStudy", "suUsername", "suGmail", "suPassword", "suConfirm"]
        all_found = all(page.locator(f"#{f}").count() > 0 for f in fields)
        log(all_found, "All 9 signup form fields are present")
    except Exception as e:
        log(False, "All 9 signup form fields are present", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 3 — Successful Sign Up
# ══════════════════════════════════════════════════════════════════
def test_successful_signup(page):
    print("\n📋 TEST 3: Successful Sign Up")
    page.goto(SITE_URL)
    clear_session(page)

    try:
        open_signup_modal(page)
        fill_signup_form(page, username="youssef_test01",
                         gmail="youssef.test01@gmail.com")
        click_create_account(page)
        page.wait_for_timeout(2500)

        # Modal should be hidden
        overlay_hidden = not page.locator("#authOverlay").is_visible()
        log(overlay_hidden, "Modal closes after successful sign up")

        # sessionStorage has the user list
        users_raw = page.evaluate("sessionStorage.getItem('chatbot_users')")
        if users_raw:
            users = json.loads(users_raw)
            found = any(u.get("username") == "youssef_test01" for u in users)
            log(found, "User saved in sessionStorage user list")
        else:
            log(False, "User saved in sessionStorage user list", "key not found")

        # Session created
        session_raw = page.evaluate("sessionStorage.getItem('chatbot_session')")
        log(session_raw is not None, "Session stored in sessionStorage after signup")

        # Navbar greets the user
        navbar_text = page.locator(".nav-container").inner_text()
        log("youssef_test01" in navbar_text,
            "Navbar shows Hello @youssef_test01 after signup",
            f"navbar='{navbar_text.strip()}'")

    except Exception as e:
        log(False, "Successful Sign Up flow", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 4 — Duplicate username rejected
# ══════════════════════════════════════════════════════════════════
def test_duplicate_username(page):
    print("\n📋 TEST 4: Duplicate username is rejected")
    page.goto(SITE_URL)

    try:
        open_signup_modal(page)
        fill_signup_form(page, username="youssef_test01",
                         gmail="different.email@gmail.com")
        click_create_account(page)
        page.wait_for_timeout(1000)

        msg = page.locator("#signupMsg").inner_text()
        log("taken" in msg.lower() or "already" in msg.lower(),
            "Error shown for duplicate username", f"msg='{msg}'")
    except Exception as e:
        log(False, "Duplicate username rejected", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 5 — Invalid Gmail rejected
# ══════════════════════════════════════════════════════════════════
def test_invalid_gmail(page):
    print("\n📋 TEST 5: Invalid Gmail is rejected")
    page.goto(SITE_URL)

    try:
        open_signup_modal(page)
        fill_signup_form(page, username="newuser_xyz99",
                         gmail="notvalid@yahoo.com")
        click_create_account(page)
        page.wait_for_timeout(1000)

        msg = page.locator("#signupMsg").inner_text()
        log("gmail" in msg.lower() or "valid" in msg.lower(),
            "Error shown for non-gmail address", f"msg='{msg}'")
    except Exception as e:
        log(False, "Invalid Gmail rejected", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 6 — Password mismatch rejected
# ══════════════════════════════════════════════════════════════════
def test_password_mismatch(page):
    print("\n📋 TEST 6: Password mismatch is rejected")
    page.goto(SITE_URL)

    try:
        open_signup_modal(page)
        fill_signup_form(page, username="newuser_abc88",
                         gmail="newuser.abc88@gmail.com",
                         password="SecurePass1!",
                         confirm="DifferentPass9!")
        click_create_account(page)
        page.wait_for_timeout(1000)

        msg = page.locator("#signupMsg").inner_text()
        log("match" in msg.lower() or "password" in msg.lower(),
            "Error shown for password mismatch", f"msg='{msg}'")
    except Exception as e:
        log(False, "Password mismatch rejected", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 7 — Empty form rejected
# ══════════════════════════════════════════════════════════════════
def test_empty_form(page):
    print("\n📋 TEST 7: Empty Sign Up form is rejected")
    page.goto(SITE_URL)

    try:
        open_signup_modal(page)
        click_create_account(page)
        page.wait_for_timeout(1000)

        msg = page.locator("#signupMsg").inner_text()
        log(msg.strip() != "", "Error shown when form is empty", f"msg='{msg}'")
    except Exception as e:
        log(False, "Empty form rejected", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 8 — Short password rejected
# ══════════════════════════════════════════════════════════════════
def test_short_password(page):
    print("\n📋 TEST 8: Short password (< 8 chars) is rejected")
    page.goto(SITE_URL)

    try:
        open_signup_modal(page)
        fill_signup_form(page, username="shortpassuser1",
                         gmail="shortpass.user1@gmail.com",
                         password="abc", confirm="abc")
        click_create_account(page)
        page.wait_for_timeout(1000)

        msg = page.locator("#signupMsg").inner_text()
        log("8" in msg or "character" in msg.lower() or "short" in msg.lower(),
            "Error shown for short password", f"msg='{msg}'")
    except Exception as e:
        log(False, "Short password rejected", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 9 — Sign In modal opens
# ══════════════════════════════════════════════════════════════════
def test_signin_modal_opens(page):
    print("\n📋 TEST 9: Sign In modal opens")
    page.goto(SITE_URL)
    clear_session(page)

    try:
        open_signin_modal(page)
        log(True, "Auth modal appears after clicking Sign In")
        log(page.locator("#panelSignIn").is_visible(), "Sign In panel is visible")
        log(page.locator("#siUsername").is_visible() and
            page.locator("#siPassword").is_visible(),
            "Username and Password fields are visible")
    except Exception as e:
        log(False, "Sign In modal opens", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 10 — Successful Sign In
# ══════════════════════════════════════════════════════════════════
def test_successful_signin(page):
    print("\n📋 TEST 10: Successful Sign In")
    page.goto(SITE_URL)

    try:
        open_signin_modal(page)
        page.fill("#siUsername", "youssef_test01")
        page.fill("#siPassword", "SecurePass1!")
        page.locator("#panelSignIn .auth-submit-btn").click()
        page.wait_for_timeout(2000)

        log(not page.locator("#authOverlay").is_visible(),
            "Modal closes after successful sign in")

        session_raw = page.evaluate("sessionStorage.getItem('chatbot_session')")
        if session_raw:
            session = json.loads(session_raw)
            log(session.get("username") == "youssef_test01",
                "Correct user stored in session",
                f"username='{session.get('username')}'")
        else:
            log(False, "Session stored after sign in")

        navbar_text = page.locator(".nav-container").inner_text()
        log("youssef_test01" in navbar_text or "Hello" in navbar_text,
            "Navbar shows Hello @username after sign in")

    except Exception as e:
        log(False, "Successful Sign In", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 11 — Wrong password rejected
# ══════════════════════════════════════════════════════════════════
def test_wrong_password(page):
    print("\n📋 TEST 11: Wrong password is rejected")
    page.goto(SITE_URL)
    clear_session(page)
    page.reload()

    try:
        open_signin_modal(page)
        page.fill("#siUsername", "youssef_test01")
        page.fill("#siPassword", "WrongPassword99!")
        page.locator("#panelSignIn .auth-submit-btn").click()
        page.wait_for_timeout(1000)

        msg = page.locator("#signinMsg").inner_text()
        log("incorrect" in msg.lower() or "password" in msg.lower(),
            "Error shown for wrong password", f"msg='{msg}'")
    except Exception as e:
        log(False, "Wrong password rejected", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 12 — Non-existent username rejected
# ══════════════════════════════════════════════════════════════════
def test_nonexistent_user(page):
    print("\n📋 TEST 12: Non-existent username is rejected")
    page.goto(SITE_URL)
    clear_session(page)
    page.reload()

    try:
        open_signin_modal(page)
        page.fill("#siUsername", "ghost_user_99999")
        page.fill("#siPassword", "SomePass123!")
        page.locator("#panelSignIn .auth-submit-btn").click()
        page.wait_for_timeout(1000)

        msg = page.locator("#signinMsg").inner_text()
        log("not found" in msg.lower() or "username" in msg.lower(),
            "Error shown for non-existent username", f"msg='{msg}'")
    except Exception as e:
        log(False, "Non-existent username rejected", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 13 — Logout works
# ══════════════════════════════════════════════════════════════════
def test_logout(page):
    print("\n📋 TEST 13: Logout works")
    page.goto(SITE_URL)

    try:
        open_signin_modal(page)
        page.fill("#siUsername", "youssef_test01")
        page.fill("#siPassword", "SecurePass1!")
        page.locator("#panelSignIn .auth-submit-btn").click()
        page.wait_for_timeout(2000)

        page.get_by_text("Log Out").click()
        page.wait_for_timeout(2000)

        session = page.evaluate("sessionStorage.getItem('chatbot_session')")
        log(session is None, "Session cleared after logout")

        log(page.locator(".sign-in-btn").is_visible(),
            "Sign In button visible again after logout")

    except Exception as e:
        log(False, "Logout works", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 14 — ESC key closes modal
# ══════════════════════════════════════════════════════════════════
def test_esc_closes_modal(page):
    print("\n📋 TEST 14: ESC key closes modal")
    page.goto(SITE_URL)
    clear_session(page)

    try:
        open_signup_modal(page)
        page.wait_for_timeout(400)
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)

        log(not page.locator("#authOverlay").is_visible(),
            "Modal closes on ESC key press")
    except Exception as e:
        log(False, "ESC key closes modal", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 15 — Tab switching Sign In ↔ Sign Up
# ══════════════════════════════════════════════════════════════════
def test_tab_switching(page):
    print("\n📋 TEST 15: Tab switching between Sign In and Sign Up")
    page.goto(SITE_URL)
    clear_session(page)

    try:
        open_signin_modal(page)

        page.click("#tabSignUp")
        page.wait_for_timeout(400)
        log(page.locator("#panelSignUp").is_visible(),
            "Clicking Sign Up tab shows Sign Up panel")

        page.click("#tabSignIn")
        page.wait_for_timeout(400)
        log(page.locator("#panelSignIn").is_visible(),
            "Clicking Sign In tab shows Sign In panel")

    except Exception as e:
        log(False, "Tab switching", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 16 — Contact form present and fillable
# ══════════════════════════════════════════════════════════════════
def test_contact_form(page):
    print("\n📋 TEST 16: Contact form fields are present and fillable")
    page.goto(SITE_URL)

    try:
        page.evaluate("document.getElementById('aboutSection').scrollIntoView()")
        page.wait_for_timeout(800)

        page.wait_for_selector("#contactName", state="visible")
        page.fill("#contactName",    "Test User")
        page.fill("#contactEmail",   "test@gmail.com")
        page.fill("#contactMessage", "This is a Playwright test message.")
        log(True, "Contact form is present and fillable")

        log(page.locator(".form-submit-btn").is_visible(),
            "Contact form submit button is visible")
    except Exception as e:
        log(False, "Contact form present and fillable", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 17 — Get Started blocked without login
# ══════════════════════════════════════════════════════════════════
def test_get_started_blocked_without_login(page):
    print("\n📋 TEST 17: Get Started is blocked when not logged in")
    page.goto(SITE_URL)
    clear_session(page)
    page.reload()
    page.wait_for_load_state("domcontentloaded")

    try:
        page.click("#getStartedBtn")
        page.wait_for_timeout(1500)

        still_on_index = "chat.html" not in page.url
        log(still_on_index, "User stays on index page when not logged in",
            f"url='{page.url}'")

        error_cls = page.locator("#getStartedError").get_attribute("class") or ""
        log("show" in error_cls, "Error toast shown telling user to sign up first")

    except Exception as e:
        log(False, "Get Started blocked without login", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 18 — Sign Up → Get Started → redirects to chat
# ══════════════════════════════════════════════════════════════════
def test_signup_then_get_started(page):
    print("\n📋 TEST 18: Sign Up → Get Started → Chat page loads")
    page.goto(SITE_URL)
    clear_session(page)

    try:
        # Sign up
        signup_fresh_user(page, username="youssef_test01",
                          gmail="youssef.test01@gmail.com")

        # Click Get Started
        page.click("#getStartedBtn")

        # main.js shows loading overlay for 1.5 s then redirects
        page.wait_for_url("**/chat.html**", timeout=8000)

        log("chat.html" in page.url,
            "Redirected to chat.html after Get Started", f"url='{page.url}'")

        log("youssef_test01" in page.url,
            "Username passed correctly in URL", f"url='{page.url}'")

    except Exception as e:
        log(False, "Sign Up then Get Started redirects to chat", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 19 — Chat page UI loads correctly
# ══════════════════════════════════════════════════════════════════
def test_chat_page_loads(page):
    print("\n📋 TEST 19: Chat page UI loads correctly")
    page.goto(f"{CHAT_URL}?username=youssef_test01")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    try:
        page.wait_for_selector(".navbar", timeout=5000)
        log(True, "Chat page navbar is present")
    except:
        log(False, "Chat page navbar is present")

    try:
        displayed = page.locator("#username").inner_text().strip()
        log(displayed == "youssef_test01",
            "Username displayed correctly in chat navbar",
            f"shown='{displayed}'")
    except Exception as e:
        log(False, "Username displayed in chat navbar", str(e))

    try:
        page.wait_for_selector("#chatMessages", timeout=5000)
        log(True, "Chat messages container is present")
    except:
        log(False, "Chat messages container is present")

    try:
        log(page.locator("#messageInput").is_visible() and
            page.locator("#sendButton").is_visible(),
            "Message input and Send button are visible")
    except Exception as e:
        log(False, "Message input and Send button visible", str(e))

    try:
        page.wait_for_timeout(2000)   # api.js adds greeting on DOMContentLoaded
        count = page.locator(".bot-message").count()
        log(count > 0, "Bot greeting message appears on load",
            f"bot messages found: {count}")
    except Exception as e:
        log(False, "Bot greeting message appears on load", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 20 — User can type and send a message
# ══════════════════════════════════════════════════════════════════
def test_chat_send_message(page):
    print("\n📋 TEST 20: User can type and send a message in chat")
    page.goto(f"{CHAT_URL}?username=youssef_test01")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    try:
        page.fill("#messageInput", "Hello, this is a Playwright test!")
        log(page.input_value("#messageInput") == "Hello, this is a Playwright test!",
            "Text typed correctly into message input")

        page.click("#sendButton")
        page.wait_for_timeout(1000)

        log(page.input_value("#messageInput") == "",
            "Input field cleared after sending message")

        count = page.locator(".user-message").count()
        log(count > 0, "User message appears in chat window",
            f"user messages found: {count}")

        log(page.locator("#typingIndicator").count() > 0,
            "Typing indicator element exists in DOM")

    except Exception as e:
        log(False, "User can type and send a message", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 21 — Chat logout returns to index
# ══════════════════════════════════════════════════════════════════
def test_chat_logout(page):
    print("\n📋 TEST 21: Chat page logout returns to index page")
    page.goto(f"{CHAT_URL}?username=youssef_test01")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1500)

    try:
        page.click("#logoutBtn")
        page.wait_for_url("**/index.html**", timeout=5000)

        on_index = "index.html" in page.url or page.url.endswith("5500/")
        log(on_index, "Logout from chat returns to index.html",
            f"url='{page.url}'")
    except Exception as e:
        log(False, "Chat logout returns to index", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 22 — Enter key sends message in chat
# ══════════════════════════════════════════════════════════════════
def test_chat_enter_key(page):
    print("\n📋 TEST 22: Enter key sends message in chat")
    page.goto(f"{CHAT_URL}?username=youssef_test01")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(2000)

    try:
        page.fill("#messageInput", "Testing Enter key in Playwright")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

        log(page.input_value("#messageInput") == "",
            "Enter key sends the message (input cleared after send)")

        count = page.locator(".user-message").count()
        log(count > 0, "Message appears in chat after Enter key",
            f"user messages: {count}")

    except Exception as e:
        log(False, "Enter key sends message", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 23 — Password strength indicator updates
# ══════════════════════════════════════════════════════════════════
def test_password_strength_indicator(page):
    print("\n📋 TEST 23: Password strength indicator updates")
    page.goto(SITE_URL)
    clear_session(page)

    try:
        open_signup_modal(page)

        # Weak password
        page.fill("#suPassword", "abc")
        page.wait_for_timeout(300)
        label_text = page.locator("#strengthLabel").inner_text()
        log("weak" in label_text.lower() or "short" in label_text.lower() or "too" in label_text.lower(),
            "Weak password shows weak label", f"label='{label_text}'")

        # Strong password
        page.fill("#suPassword", "")
        page.fill("#suPassword", "StrongPass99!")
        page.wait_for_timeout(300)
        label_text = page.locator("#strengthLabel").inner_text()
        log("strong" in label_text.lower(),
            "Strong password shows strong label", f"label='{label_text}'")

    except Exception as e:
        log(False, "Password strength indicator updates", str(e))

    close_modal_if_open(page)

# ══════════════════════════════════════════════════════════════════
#  TEST 24 — Enter key submits Sign In form
# ══════════════════════════════════════════════════════════════════
def test_enter_key_signin(page):
    print("\n📋 TEST 24: Enter key submits Sign In form")
    page.goto(SITE_URL)

    try:
        open_signin_modal(page)
        page.fill("#siUsername", "youssef_test01")
        page.fill("#siPassword", "SecurePass1!")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

        log(not page.locator("#authOverlay").is_visible(),
            "Enter key submits Sign In and closes modal")

    except Exception as e:
        log(False, "Enter key submits Sign In form", str(e))

# ══════════════════════════════════════════════════════════════════
#  MAIN — Run all tests
# ══════════════════════════════════════════════════════════════════
def run_all_tests():
    print("=" * 60)
    print("  🎭 ChatBot Playwright Test Suite")
    print("  Make sure your site is running on:", SITE_URL)
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=80)
        page    = browser.new_page()

        try:
            # ── Index page & auth tests ───────────────────────
            test_page_loads(page)
            test_signup_modal_opens(page)
            test_successful_signup(page)
            test_duplicate_username(page)
            test_invalid_gmail(page)
            test_password_mismatch(page)
            test_empty_form(page)
            test_short_password(page)
            test_signin_modal_opens(page)
            test_successful_signin(page)
            test_wrong_password(page)
            test_nonexistent_user(page)
            test_logout(page)
            test_esc_closes_modal(page)
            test_tab_switching(page)
            test_contact_form(page)
            test_password_strength_indicator(page)
            test_enter_key_signin(page)

            # ── Get Started + Chat page tests ─────────────────
            test_get_started_blocked_without_login(page)
            test_signup_then_get_started(page)
            test_chat_page_loads(page)
            test_chat_send_message(page)
            test_chat_logout(page)
            test_chat_enter_key(page)

        finally:
            browser.close()

    print("\n" + "=" * 60)
    print(f"  Results: {passed} passed,  {failed} failed  (total {passed + failed})")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()