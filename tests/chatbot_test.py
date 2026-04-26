# ══════════════════════════════════════════════════════════════════
#  chatbot_testing.py  –  Selenium UI Tests for ChatBot Website
#  Tests: Sign Up, Sign In, Validation, Logout, Contact Form, Chat
# ══════════════════════════════════════════════════════════════════

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# ── CONFIG ────────────────────────────────────────────────────────
SITE_URL = "http://127.0.0.1:5500/index.html"   # Change if your port is different
WAIT_SEC = 10                                     # Max seconds to wait for elements

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

# ── Driver setup ──────────────────────────────────────────────────
def make_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # uncomment to run without opening browser
    options.add_argument("--start-maximized")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

# ── Helper: open Sign Up modal ────────────────────────────────────
def open_signup_modal(driver, wait):
    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sign-up-btn")))
    btn.click()
    wait.until(EC.visibility_of_element_located((By.ID, "authOverlay")))
    wait.until(EC.element_to_be_clickable((By.ID, "tabSignUp"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "panelSignUp")))

# ── Helper: open Sign In modal ────────────────────────────────────
def open_signin_modal(driver, wait):
    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sign-in-btn")))
    btn.click()
    wait.until(EC.visibility_of_element_located((By.ID, "authOverlay")))
    wait.until(EC.visibility_of_element_located((By.ID, "panelSignIn")))

# ── Helper: fill Sign Up form ─────────────────────────────────────
def fill_signup_form(driver, wait,
                     first="Youssef", last="Ali",
                     gender="male", nationality="Egyptian",
                     study="software_engineering",
                     username="youssef_test01",
                     gmail="youssef.test01@gmail.com",
                     password="SecurePass1!",
                     confirm="SecurePass1!"):
    driver.find_element(By.ID, "suFirstName").clear()
    driver.find_element(By.ID, "suFirstName").send_keys(first)
    driver.find_element(By.ID, "suLastName").clear()
    driver.find_element(By.ID, "suLastName").send_keys(last)
    Select(driver.find_element(By.ID, "suGender")).select_by_value(gender)
    driver.find_element(By.ID, "suNationality").clear()
    driver.find_element(By.ID, "suNationality").send_keys(nationality)
    Select(driver.find_element(By.ID, "suStudy")).select_by_value(study)
    driver.find_element(By.ID, "suUsername").clear()
    driver.find_element(By.ID, "suUsername").send_keys(username)
    driver.find_element(By.ID, "suGmail").clear()
    driver.find_element(By.ID, "suGmail").send_keys(gmail)
    driver.find_element(By.ID, "suPassword").clear()
    driver.find_element(By.ID, "suPassword").send_keys(password)
    driver.find_element(By.ID, "suConfirm").clear()
    driver.find_element(By.ID, "suConfirm").send_keys(confirm)

# ── Helper: click Create Account ─────────────────────────────────
def click_create_account(driver):
    driver.find_elements(By.CSS_SELECTOR, "#panelSignUp .auth-submit-btn")[0].click()

# ── Helper: close modal if open ───────────────────────────────────
def close_modal_if_open(driver):
    try:
        close_btn = driver.find_element(By.ID, "authCloseBtn")
        if close_btn.is_displayed():
            close_btn.click()
            time.sleep(0.5)
    except:
        pass

# ── Helper: clear sessionStorage only (localStorage removed) ──────
def clear_storage(driver):
    driver.execute_script("sessionStorage.clear();")

# ── Helper: full signup flow ──────────────────────────────────────
def signup_fresh_user(driver, wait, username="youssef_test01",
                      gmail="youssef.test01@gmail.com"):
    open_signup_modal(driver, wait)
    fill_signup_form(driver, wait, username=username, gmail=gmail)
    click_create_account(driver)
    time.sleep(2.5)   # auth.js delays modal close by 1.2s then animates out

# ══════════════════════════════════════════════════════════════════
#  TEST 1 — Page loads correctly
# ══════════════════════════════════════════════════════════════════
def test_page_loads(driver, wait):
    print("\n📋 TEST 1: Page loads correctly")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        title = driver.title
        log("CHATBOT" in title.upper() or title != "", "Page title is set", f"title='{title}'")
    except:
        log(False, "Page title is set")

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar")))
        log(True, "Navbar is present")
    except:
        log(False, "Navbar is present")

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sign-in-btn")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sign-up-btn")))
        log(True, "Sign In and Sign Up buttons visible in navbar")
    except:
        log(False, "Sign In and Sign Up buttons visible in navbar")

    try:
        wait.until(EC.presence_of_element_located((By.ID, "getStartedBtn")))
        log(True, "Get Started button present")
    except:
        log(False, "Get Started button present")

# ══════════════════════════════════════════════════════════════════
#  TEST 2 — Sign Up modal opens
# ══════════════════════════════════════════════════════════════════
def test_signup_modal_opens(driver, wait):
    print("\n📋 TEST 2: Sign Up modal opens")
    driver.get(SITE_URL)
    clear_storage(driver)
    time.sleep(1)

    try:
        open_signup_modal(driver, wait)
        log(True, "Auth modal appears after clicking Sign Up")
    except Exception as e:
        log(False, "Auth modal appears after clicking Sign Up", str(e))
        return

    try:
        panel = driver.find_element(By.ID, "panelSignUp")
        log(panel.is_displayed(), "Sign Up panel is visible")
    except:
        log(False, "Sign Up panel is visible")

    try:
        fields = ["suFirstName", "suLastName", "suGender", "suNationality",
                  "suStudy", "suUsername", "suGmail", "suPassword", "suConfirm"]
        all_found = all(driver.find_element(By.ID, f) for f in fields)
        log(all_found, "All 9 signup form fields are present")
    except Exception as e:
        log(False, "All 9 signup form fields are present", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 3 — Successful Sign Up
# ══════════════════════════════════════════════════════════════════
def test_successful_signup(driver, wait):
    print("\n📋 TEST 3: Successful Sign Up")
    driver.get(SITE_URL)
    clear_storage(driver)
    time.sleep(1)

    try:
        open_signup_modal(driver, wait)
        fill_signup_form(driver, wait,
                         username="youssef_test01",
                         gmail="youssef.test01@gmail.com")
        click_create_account(driver)
        time.sleep(2.5)

        toast_visible = False
        try:
            toast = driver.find_element(By.ID, "authToast")
            toast_visible = "show" in toast.get_attribute("class") and toast.is_displayed()
        except:
            pass

        navbar_updated = False
        try:
            navbar_text = driver.find_element(By.CSS_SELECTOR, ".nav-container").text
            navbar_updated = "youssef_test01" in navbar_text or "Hello" in navbar_text
        except:
            pass

        modal_closed = False
        try:
            overlay = driver.find_element(By.ID, "authOverlay")
            modal_closed = not overlay.is_displayed()
        except:
            modal_closed = True

        log(toast_visible or navbar_updated or modal_closed,
            "Sign Up succeeds (toast / navbar updated / modal closed)")

        # ✅ Check sessionStorage — NOT localStorage (localStorage was removed)
        users_raw = driver.execute_script("return sessionStorage.getItem('chatbot_users');")
        if users_raw:
            users = json.loads(users_raw)
            found = any(u.get("username") == "youssef_test01" for u in users)
            log(found, "User saved in sessionStorage user list")
        else:
            log(False, "User saved in sessionStorage user list", "chatbot_users key not found")

        session_raw = driver.execute_script("return sessionStorage.getItem('chatbot_session');")
        log(session_raw is not None, "Session stored in sessionStorage after signup")

        try:
            navbar_text = driver.find_element(By.CSS_SELECTOR, ".nav-container").text
            log("youssef_test01" in navbar_text,
                "Navbar shows Hello @youssef_test01 after signup",
                f"navbar='{navbar_text.strip()}'")
        except Exception as e:
            log(False, "Navbar shows Hello @username", str(e))

    except Exception as e:
        log(False, "Successful Sign Up flow", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 4 — Duplicate username rejected
# ══════════════════════════════════════════════════════════════════
def test_duplicate_username(driver, wait):
    print("\n📋 TEST 4: Duplicate username is rejected")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        open_signup_modal(driver, wait)
        fill_signup_form(driver, wait,
                         username="youssef_test01",
                         gmail="different.email@gmail.com")
        click_create_account(driver)
        time.sleep(1)

        msg = driver.find_element(By.ID, "signupMsg")
        log("taken" in msg.text.lower() or "already" in msg.text.lower(),
            "Error shown for duplicate username", f"msg='{msg.text}'")
    except Exception as e:
        log(False, "Duplicate username rejected", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 5 — Invalid Gmail rejected
# ══════════════════════════════════════════════════════════════════
def test_invalid_gmail(driver, wait):
    print("\n📋 TEST 5: Invalid Gmail is rejected")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        open_signup_modal(driver, wait)
        fill_signup_form(driver, wait,
                         username="newuser_xyz99",
                         gmail="notvalid@yahoo.com")
        click_create_account(driver)
        time.sleep(1)

        msg = driver.find_element(By.ID, "signupMsg")
        log("gmail" in msg.text.lower() or "valid" in msg.text.lower(),
            "Error shown for non-gmail address", f"msg='{msg.text}'")
    except Exception as e:
        log(False, "Invalid Gmail rejected", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 6 — Password mismatch rejected
# ══════════════════════════════════════════════════════════════════
def test_password_mismatch(driver, wait):
    print("\n📋 TEST 6: Password mismatch is rejected")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        open_signup_modal(driver, wait)
        fill_signup_form(driver, wait,
                         username="newuser_abc88",
                         gmail="newuser.abc88@gmail.com",
                         password="SecurePass1!",
                         confirm="DifferentPass9!")
        click_create_account(driver)
        time.sleep(1)

        msg = driver.find_element(By.ID, "signupMsg")
        log("match" in msg.text.lower() or "password" in msg.text.lower(),
            "Error shown for password mismatch", f"msg='{msg.text}'")
    except Exception as e:
        log(False, "Password mismatch rejected", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 7 — Empty form rejected
# ══════════════════════════════════════════════════════════════════
def test_empty_form(driver, wait):
    print("\n📋 TEST 7: Empty Sign Up form is rejected")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        open_signup_modal(driver, wait)
        click_create_account(driver)
        time.sleep(1)

        msg = driver.find_element(By.ID, "signupMsg")
        log(msg.text != "", "Error shown when form is empty", f"msg='{msg.text}'")
    except Exception as e:
        log(False, "Empty form rejected", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 8 — Short password rejected
# ══════════════════════════════════════════════════════════════════
def test_short_password(driver, wait):
    print("\n📋 TEST 8: Short password (< 8 chars) is rejected")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        open_signup_modal(driver, wait)
        fill_signup_form(driver, wait,
                         username="shortpassuser1",
                         gmail="shortpass.user1@gmail.com",
                         password="abc",
                         confirm="abc")
        click_create_account(driver)
        time.sleep(1)

        msg = driver.find_element(By.ID, "signupMsg")
        log("8" in msg.text or "character" in msg.text.lower() or "short" in msg.text.lower(),
            "Error shown for short password", f"msg='{msg.text}'")
    except Exception as e:
        log(False, "Short password rejected", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 9 — Sign In modal opens
# ══════════════════════════════════════════════════════════════════
def test_signin_modal_opens(driver, wait):
    print("\n📋 TEST 9: Sign In modal opens")
    driver.get(SITE_URL)
    clear_storage(driver)
    time.sleep(1)

    try:
        open_signin_modal(driver, wait)
        log(True, "Auth modal appears after clicking Sign In")
        log(driver.find_element(By.ID, "panelSignIn").is_displayed(), "Sign In panel is visible")
        u = driver.find_element(By.ID, "siUsername")
        p = driver.find_element(By.ID, "siPassword")
        log(u.is_displayed() and p.is_displayed(), "Username and Password fields are visible")
    except Exception as e:
        log(False, "Sign In modal opens", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 10 — Successful Sign In
# ══════════════════════════════════════════════════════════════════
def test_successful_signin(driver, wait):
    print("\n📋 TEST 10: Successful Sign In")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        open_signin_modal(driver, wait)
        driver.find_element(By.ID, "siUsername").send_keys("youssef_test01")
        driver.find_element(By.ID, "siPassword").send_keys("SecurePass1!")
        driver.find_element(By.CSS_SELECTOR, "#panelSignIn .auth-submit-btn").click()
        time.sleep(2)

        overlay = driver.find_element(By.ID, "authOverlay")
        log(not overlay.is_displayed(), "Modal closes after successful sign in")

        session_raw = driver.execute_script("return sessionStorage.getItem('chatbot_session');")
        if session_raw:
            session = json.loads(session_raw)
            log(session.get("username") == "youssef_test01",
                "Correct user stored in session", f"username='{session.get('username')}'")
        else:
            log(False, "Session stored after sign in")

        navbar_text = driver.find_element(By.CSS_SELECTOR, ".nav-container").text
        log("youssef_test01" in navbar_text or "Hello" in navbar_text,
            "Navbar shows Hello @username after sign in")

    except Exception as e:
        log(False, "Successful Sign In", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 11 — Wrong password rejected
# ══════════════════════════════════════════════════════════════════
def test_wrong_password(driver, wait):
    print("\n📋 TEST 11: Wrong password is rejected")
    driver.get(SITE_URL)
    clear_storage(driver)
    driver.refresh()
    time.sleep(1)

    try:
        open_signin_modal(driver, wait)
        driver.find_element(By.ID, "siUsername").send_keys("youssef_test01")
        driver.find_element(By.ID, "siPassword").send_keys("WrongPassword99!")
        driver.find_element(By.CSS_SELECTOR, "#panelSignIn .auth-submit-btn").click()
        time.sleep(1)

        msg = driver.find_element(By.ID, "signinMsg")
        log("incorrect" in msg.text.lower() or "password" in msg.text.lower(),
            "Error shown for wrong password", f"msg='{msg.text}'")
    except Exception as e:
        log(False, "Wrong password rejected", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 12 — Non-existent username rejected
# ══════════════════════════════════════════════════════════════════
def test_nonexistent_user(driver, wait):
    print("\n📋 TEST 12: Non-existent username is rejected")
    driver.get(SITE_URL)
    clear_storage(driver)
    driver.refresh()
    time.sleep(1)

    try:
        open_signin_modal(driver, wait)
        driver.find_element(By.ID, "siUsername").send_keys("ghost_user_99999")
        driver.find_element(By.ID, "siPassword").send_keys("SomePass123!")
        driver.find_element(By.CSS_SELECTOR, "#panelSignIn .auth-submit-btn").click()
        time.sleep(1)

        msg = driver.find_element(By.ID, "signinMsg")
        log("not found" in msg.text.lower() or "username" in msg.text.lower(),
            "Error shown for non-existent username", f"msg='{msg.text}'")
    except Exception as e:
        log(False, "Non-existent username rejected", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 13 — Logout works
# ══════════════════════════════════════════════════════════════════
def test_logout(driver, wait):
    print("\n📋 TEST 13: Logout works")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        open_signin_modal(driver, wait)
        driver.find_element(By.ID, "siUsername").send_keys("youssef_test01")
        driver.find_element(By.ID, "siPassword").send_keys("SecurePass1!")
        driver.find_element(By.CSS_SELECTOR, "#panelSignIn .auth-submit-btn").click()
        time.sleep(2)

        logout_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Log Out')]")
        ))
        logout_btn.click()
        time.sleep(2)

        session = driver.execute_script("return sessionStorage.getItem('chatbot_session');")
        log(session is None, "Session cleared after logout")

        signin_visible = driver.find_element(By.CSS_SELECTOR, ".sign-in-btn").is_displayed()
        log(signin_visible, "Sign In button visible again after logout")

    except Exception as e:
        log(False, "Logout works", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 14 — ESC key closes modal
# ══════════════════════════════════════════════════════════════════
def test_esc_closes_modal(driver, wait):
    print("\n📋 TEST 14: ESC key closes modal")
    driver.get(SITE_URL)
    clear_storage(driver)
    time.sleep(1)

    try:
        open_signup_modal(driver, wait)
        time.sleep(0.5)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)
        overlay = driver.find_element(By.ID, "authOverlay")
        log(not overlay.is_displayed(), "Modal closes on ESC key press")
    except Exception as e:
        log(False, "ESC key closes modal", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 15 — Tab switching
# ══════════════════════════════════════════════════════════════════
def test_tab_switching(driver, wait):
    print("\n📋 TEST 15: Tab switching between Sign In and Sign Up")
    driver.get(SITE_URL)
    clear_storage(driver)
    time.sleep(1)

    try:
        open_signin_modal(driver, wait)
        driver.find_element(By.ID, "tabSignUp").click()
        time.sleep(0.5)
        log(driver.find_element(By.ID, "panelSignUp").is_displayed(),
            "Clicking Sign Up tab shows Sign Up panel")
        driver.find_element(By.ID, "tabSignIn").click()
        time.sleep(0.5)
        log(driver.find_element(By.ID, "panelSignIn").is_displayed(),
            "Clicking Sign In tab shows Sign In panel")
    except Exception as e:
        log(False, "Tab switching", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 16 — Contact form present and fillable
# ══════════════════════════════════════════════════════════════════
def test_contact_form(driver, wait):
    print("\n📋 TEST 16: Contact form fields are present and fillable")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        driver.execute_script("document.getElementById('aboutSection').scrollIntoView();")
        time.sleep(1)
        name_field  = wait.until(EC.presence_of_element_located((By.ID, "contactName")))
        email_field = driver.find_element(By.ID, "contactEmail")
        msg_field   = driver.find_element(By.ID, "contactMessage")
        name_field.send_keys("Test User")
        email_field.send_keys("test@gmail.com")
        msg_field.send_keys("This is a test message from Selenium.")
        log(True, "Contact form is present and fillable")
        submit_btn = driver.find_element(By.CSS_SELECTOR, ".form-submit-btn")
        log(submit_btn.is_displayed(), "Contact form submit button is visible")
    except Exception as e:
        log(False, "Contact form present and fillable", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 17 — Get Started blocked without login
# ══════════════════════════════════════════════════════════════════
def test_get_started_blocked_without_login(driver, wait):
    print("\n📋 TEST 17: Get Started is blocked when not logged in")
    driver.get(SITE_URL)
    clear_storage(driver)
    driver.refresh()
    time.sleep(1)

    try:
        btn = wait.until(EC.element_to_be_clickable((By.ID, "getStartedBtn")))
        btn.click()
        time.sleep(1.5)

        still_on_index = "chat.html" not in driver.current_url
        log(still_on_index, "User stays on index page when not logged in",
            f"url='{driver.current_url}'")

        try:
            error_toast = driver.find_element(By.ID, "getStartedError")
            toast_shown = "show" in error_toast.get_attribute("class")
            log(toast_shown, "Error toast shown telling user to sign up first")
        except:
            log(False, "Error toast shown telling user to sign up first")

    except Exception as e:
        log(False, "Get Started blocked without login", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 18 — Sign Up → Get Started → lands on chat page
# ══════════════════════════════════════════════════════════════════
def test_signup_then_get_started(driver, wait):
    print("\n📋 TEST 18: Sign Up → Get Started → Chat page loads")
    driver.get(SITE_URL)
    clear_storage(driver)
    time.sleep(1)

    try:
        # Step 1: Sign up a fresh user
        signup_fresh_user(driver, wait,
                          username="youssef_test01",
                          gmail="youssef.test01@gmail.com")

        # Step 2: Click Get Started (now logged in)
        get_started = wait.until(EC.element_to_be_clickable((By.ID, "getStartedBtn")))
        get_started.click()

        # Step 3: main.js shows loading overlay for 1.5s then redirects
        time.sleep(3.5)

        # Step 4: Verify on chat page
        on_chat = "chat.html" in driver.current_url
        log(on_chat, "Redirected to chat.html after Get Started",
            f"url='{driver.current_url}'")

        # Step 5: Verify username passed in URL
        username_in_url = "youssef_test01" in driver.current_url
        log(username_in_url, "Username passed correctly in URL to chat page",
            f"url='{driver.current_url}'")

    except Exception as e:
        log(False, "Sign Up then Get Started redirects to chat", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 19 — Chat page UI loads correctly
# ══════════════════════════════════════════════════════════════════
def test_chat_page_loads(driver, wait):
    print("\n📋 TEST 19: Chat page UI loads correctly")
    driver.get("http://127.0.0.1:5500/chat.html?username=youssef_test01")
    time.sleep(2)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar")))
        log(True, "Chat page navbar is present")
    except:
        log(False, "Chat page navbar is present")

    try:
        username_el = driver.find_element(By.ID, "username")
        displayed = username_el.text.strip()
        log(displayed == "youssef_test01",
            "Username displayed correctly in chat navbar", f"shown='{displayed}'")
    except Exception as e:
        log(False, "Username displayed in chat navbar", str(e))

    try:
        wait.until(EC.presence_of_element_located((By.ID, "chatMessages")))
        log(True, "Chat messages container is present")
    except:
        log(False, "Chat messages container is present")

    try:
        msg_input = driver.find_element(By.ID, "messageInput")
        send_btn  = driver.find_element(By.ID, "sendButton")
        log(msg_input.is_displayed() and send_btn.is_displayed(),
            "Message input and Send button are visible")
    except Exception as e:
        log(False, "Message input and Send button visible", str(e))

    try:
        time.sleep(2)   # api.js adds greeting on DOMContentLoaded
        messages = driver.find_elements(By.CSS_SELECTOR, ".bot-message")
        log(len(messages) > 0, "Bot greeting message appears on load",
            f"bot messages found: {len(messages)}")
    except Exception as e:
        log(False, "Bot greeting message appears on load", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 20 — User can type and send a message in chat
# ══════════════════════════════════════════════════════════════════
def test_chat_send_message(driver, wait):
    print("\n📋 TEST 20: User can type and send a message in chat")
    driver.get("http://127.0.0.1:5500/chat.html?username=youssef_test01")
    time.sleep(2)

    try:
        msg_input = wait.until(EC.presence_of_element_located((By.ID, "messageInput")))
        msg_input.send_keys("Hello, this is a test message!")

        log(msg_input.get_attribute("value") == "Hello, this is a test message!",
            "Text typed correctly into message input")

        driver.find_element(By.ID, "sendButton").click()
        time.sleep(1)

        log(msg_input.get_attribute("value") == "",
            "Input field cleared after sending message")

        user_messages = driver.find_elements(By.CSS_SELECTOR, ".user-message")
        log(len(user_messages) > 0, "User message appears in chat window",
            f"user messages found: {len(user_messages)}")

        try:
            typing = driver.find_element(By.ID, "typingIndicator")
            log(True, "Typing indicator element exists in DOM")
        except:
            log(False, "Typing indicator element exists in DOM")

    except Exception as e:
        log(False, "User can type and send a message", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 21 — Chat logout returns to index
# ══════════════════════════════════════════════════════════════════
def test_chat_logout(driver, wait):
    print("\n📋 TEST 21: Chat page logout returns to index page")
    driver.get("http://127.0.0.1:5500/chat.html?username=youssef_test01")
    time.sleep(2)

    try:
        logout_btn = wait.until(EC.element_to_be_clickable((By.ID, "logoutBtn")))
        logout_btn.click()
        time.sleep(2)

        on_index = "index.html" in driver.current_url or driver.current_url.endswith("5500/")
        log(on_index, "Logout from chat returns to index.html",
            f"url='{driver.current_url}'")
    except Exception as e:
        log(False, "Chat logout returns to index", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 22 — Enter key sends message in chat
# ══════════════════════════════════════════════════════════════════
def test_chat_enter_key(driver, wait):
    print("\n📋 TEST 22: Enter key sends message in chat")
    driver.get("http://127.0.0.1:5500/chat.html?username=youssef_test01")
    time.sleep(2)

    try:
        msg_input = wait.until(EC.presence_of_element_located((By.ID, "messageInput")))
        msg_input.send_keys("Testing enter key send")
        msg_input.send_keys(Keys.RETURN)
        time.sleep(1)

        log(msg_input.get_attribute("value") == "",
            "Enter key sends the message (input cleared after send)")

        user_messages = driver.find_elements(By.CSS_SELECTOR, ".user-message")
        log(len(user_messages) > 0, "Message appears in chat after Enter key",
            f"user messages: {len(user_messages)}")

    except Exception as e:
        log(False, "Enter key sends message", str(e))

# ══════════════════════════════════════════════════════════════════
#  MAIN — Run all tests
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  🤖 ChatBot Selenium Test Suite")
    print("  Make sure your site is running on:", SITE_URL)
    print("=" * 60)

    driver = make_driver()
    wait   = WebDriverWait(driver, WAIT_SEC)

    try:
        # ── Index page & auth tests ───────────────────────────
        test_page_loads(driver, wait)
        test_signup_modal_opens(driver, wait)
        test_successful_signup(driver, wait)
        test_duplicate_username(driver, wait)
        test_invalid_gmail(driver, wait)
        test_password_mismatch(driver, wait)
        test_empty_form(driver, wait)
        test_short_password(driver, wait)
        test_signin_modal_opens(driver, wait)
        test_successful_signin(driver, wait)
        test_wrong_password(driver, wait)
        test_nonexistent_user(driver, wait)
        test_logout(driver, wait)
        test_esc_closes_modal(driver, wait)
        test_tab_switching(driver, wait)
        test_contact_form(driver, wait)

        # ── Get Started + Chat page tests ─────────────────────
        test_get_started_blocked_without_login(driver, wait)
        test_signup_then_get_started(driver, wait)
        test_chat_page_loads(driver, wait)
        test_chat_send_message(driver, wait)
        test_chat_logout(driver, wait)
        test_chat_enter_key(driver, wait)

    finally:
        driver.quit()
        print("\n" + "=" * 60)
        print(f"  Results: {passed} passed,  {failed} failed  (total {passed + failed})")
        print("=" * 60)