# ══════════════════════════════════════════════════════════════════
#  chatbot_testing.py  –  Selenium UI Tests for ChatBot Website
#  Tests: Sign Up, Sign In, Validation, Logout, Contact Form
# ══════════════════════════════════════════════════════════════════

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

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
    """Clicks the navbar Sign Up button and waits for the modal to appear."""
    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sign-up-btn")))
    btn.click()
    # Wait for the injected overlay to become visible
    wait.until(EC.visibility_of_element_located((By.ID, "authOverlay")))
    # Make sure we're on the Sign Up tab
    wait.until(EC.element_to_be_clickable((By.ID, "tabSignUp"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "panelSignUp")))

# ── Helper: open Sign In modal ────────────────────────────────────
def open_signin_modal(driver, wait):
    """Clicks the navbar Sign In button and waits for the modal to appear."""
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

# ── Helper: click the Create Account button ───────────────────────
def click_create_account(driver):
    btns = driver.find_elements(By.CSS_SELECTOR, "#panelSignUp .auth-submit-btn")
    btns[0].click()

# ── Helper: close modal if open ───────────────────────────────────
def close_modal_if_open(driver):
    try:
        close_btn = driver.find_element(By.ID, "authCloseBtn")
        if close_btn.is_displayed():
            close_btn.click()
            time.sleep(0.5)
    except:
        pass

# ── Helper: clear localStorage & sessionStorage ───────────────────
def clear_storage(driver):
    driver.execute_script("localStorage.clear(); sessionStorage.clear();")

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

        # Wait for success message or modal to close
        time.sleep(2)

        # Check: toast message OR navbar updated OR modal closed
        toast_visible = False
        navbar_updated = False
        modal_closed = False

        try:
            toast = driver.find_element(By.ID, "authToast")
            toast_visible = "show" in toast.get_attribute("class") and toast.is_displayed()
        except:
            pass

        try:
            navbar_text = driver.find_element(By.CSS_SELECTOR, ".nav-container").text
            navbar_updated = "youssef_test01" in navbar_text or "Hello" in navbar_text
        except:
            pass

        try:
            overlay = driver.find_element(By.ID, "authOverlay")
            modal_closed = not overlay.is_displayed()
        except:
            modal_closed = True

        log(toast_visible or navbar_updated or modal_closed,
            "Sign Up succeeds (toast shown / navbar updated / modal closed)")

        # Check user saved in localStorage
        users_raw = driver.execute_script("return localStorage.getItem('chatbot_users');")
        import json
        if users_raw:
            users = json.loads(users_raw)
            found = any(u.get("username") == "youssef_test01" for u in users)
            log(found, "User saved in localStorage")
        else:
            log(False, "User saved in localStorage", "localStorage empty")

        # Check session set
        session_raw = driver.execute_script("return sessionStorage.getItem('chatbot_session');")
        log(session_raw is not None, "Session stored in sessionStorage after signup")

    except Exception as e:
        log(False, "Successful Sign Up flow", str(e))

    time.sleep(1.5)  # let modal close animation finish

# ══════════════════════════════════════════════════════════════════
#  TEST 4 — Duplicate username rejected
# ══════════════════════════════════════════════════════════════════
def test_duplicate_username(driver, wait):
    print("\n📋 TEST 4: Duplicate username is rejected")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        open_signup_modal(driver, wait)
        # Same username as TEST 3
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
                         gmail="notvalid@yahoo.com")   # not @gmail.com
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
        # Don't fill anything — just click submit
        click_create_account(driver)
        time.sleep(1)

        msg = driver.find_element(By.ID, "signupMsg")
        log(msg.text != "", "Error shown when form is empty", f"msg='{msg.text}'")
    except Exception as e:
        log(False, "Empty form rejected", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 8 — Short password rejected (< 8 chars)
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
    time.sleep(1)

    try:
        open_signin_modal(driver, wait)
        log(True, "Auth modal appears after clicking Sign In")

        panel = driver.find_element(By.ID, "panelSignIn")
        log(panel.is_displayed(), "Sign In panel is visible")

        username_field = driver.find_element(By.ID, "siUsername")
        password_field = driver.find_element(By.ID, "siPassword")
        log(username_field.is_displayed() and password_field.is_displayed(),
            "Username and Password fields are visible")
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

        # Click Sign In button
        signin_btn = driver.find_element(By.CSS_SELECTOR, "#panelSignIn .auth-submit-btn")
        signin_btn.click()
        time.sleep(2)

        # Check modal closed
        overlay = driver.find_element(By.ID, "authOverlay")
        modal_closed = not overlay.is_displayed()
        log(modal_closed, "Modal closes after successful sign in")

        # Check session set
        import json
        session_raw = driver.execute_script("return sessionStorage.getItem('chatbot_session');")
        if session_raw:
            session = json.loads(session_raw)
            log(session.get("username") == "youssef_test01",
                "Correct user stored in session", f"username='{session.get('username')}'")
        else:
            log(False, "Session stored after sign in")

        # Check navbar updated
        navbar_text = driver.find_element(By.CSS_SELECTOR, ".nav-container").text
        log("youssef_test01" in navbar_text or "Hello" in navbar_text,
            "Navbar updated with username after sign in")

    except Exception as e:
        log(False, "Successful Sign In", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 11 — Wrong password rejected
# ══════════════════════════════════════════════════════════════════
def test_wrong_password(driver, wait):
    print("\n📋 TEST 11: Wrong password is rejected")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        # Log out first if session active
        driver.execute_script("sessionStorage.clear();")
        driver.refresh()
        time.sleep(1)

        open_signin_modal(driver, wait)
        driver.find_element(By.ID, "siUsername").send_keys("youssef_test01")
        driver.find_element(By.ID, "siPassword").send_keys("WrongPassword99!")

        signin_btn = driver.find_element(By.CSS_SELECTOR, "#panelSignIn .auth-submit-btn")
        signin_btn.click()
        time.sleep(1)

        msg = driver.find_element(By.ID, "signinMsg")
        log("incorrect" in msg.text.lower() or "password" in msg.text.lower() or "wrong" in msg.text.lower(),
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
    time.sleep(1)

    try:
        driver.execute_script("sessionStorage.clear();")
        driver.refresh()
        time.sleep(1)

        open_signin_modal(driver, wait)
        driver.find_element(By.ID, "siUsername").send_keys("ghost_user_99999")
        driver.find_element(By.ID, "siPassword").send_keys("SomePass123!")

        signin_btn = driver.find_element(By.CSS_SELECTOR, "#panelSignIn .auth-submit-btn")
        signin_btn.click()
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
        # Sign in first
        open_signin_modal(driver, wait)
        driver.find_element(By.ID, "siUsername").send_keys("youssef_test01")
        driver.find_element(By.ID, "siPassword").send_keys("SecurePass1!")
        driver.find_element(By.CSS_SELECTOR, "#panelSignIn .auth-submit-btn").click()
        time.sleep(2)

        # Click Log Out button
        logout_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Log Out')]")
        ))
        logout_btn.click()
        time.sleep(2)

        # Check session cleared
        session = driver.execute_script("return sessionStorage.getItem('chatbot_session');")
        log(session is None, "Session cleared after logout")

        # Check Sign In / Sign Up buttons are back
        signin_visible = driver.find_element(By.CSS_SELECTOR, ".sign-in-btn").is_displayed()
        log(signin_visible, "Sign In button visible again after logout")

    except Exception as e:
        log(False, "Logout works", str(e))

# ══════════════════════════════════════════════════════════════════
#  TEST 14 — Modal closes with ESC key
# ══════════════════════════════════════════════════════════════════
def test_esc_closes_modal(driver, wait):
    print("\n📋 TEST 14: ESC key closes modal")
    driver.get(SITE_URL)
    driver.execute_script("sessionStorage.clear();")
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
#  TEST 15 — Tab switch between Sign In and Sign Up
# ══════════════════════════════════════════════════════════════════
def test_tab_switching(driver, wait):
    print("\n📋 TEST 15: Tab switching between Sign In and Sign Up")
    driver.get(SITE_URL)
    driver.execute_script("sessionStorage.clear();")
    time.sleep(1)

    try:
        open_signin_modal(driver, wait)

        # Switch to Sign Up tab
        driver.find_element(By.ID, "tabSignUp").click()
        time.sleep(0.5)
        signup_panel = driver.find_element(By.ID, "panelSignUp")
        log(signup_panel.is_displayed(), "Clicking Sign Up tab shows Sign Up panel")

        # Switch back to Sign In tab
        driver.find_element(By.ID, "tabSignIn").click()
        time.sleep(0.5)
        signin_panel = driver.find_element(By.ID, "panelSignIn")
        log(signin_panel.is_displayed(), "Clicking Sign In tab shows Sign In panel")

    except Exception as e:
        log(False, "Tab switching", str(e))

    close_modal_if_open(driver)

# ══════════════════════════════════════════════════════════════════
#  TEST 16 — Contact form present
# ══════════════════════════════════════════════════════════════════
def test_contact_form(driver, wait):
    print("\n📋 TEST 16: Contact form fields are present and fillable")
    driver.get(SITE_URL)
    time.sleep(1)

    try:
        # Scroll down to contact form
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

    finally:
        driver.quit()
        print("\n" + "=" * 60)
        print(f"  Results: {passed} passed,  {failed} failed  (total {passed+failed})")
        print("=" * 60)