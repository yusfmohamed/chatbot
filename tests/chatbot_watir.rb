# ══════════════════════════════════════════════════════════════════
#  chatbot_watir.rb  –  Watir UI Tests for ChatBot Website
#  Tests: Sign Up, Sign In, Validation, Logout, Contact Form, Chat
#  Run with: ruby tests/chatbot_watir.rb
# ══════════════════════════════════════════════════════════════════

require 'watir'
require 'webdrivers'

# ── CONFIG ────────────────────────────────────────────────────────
SITE_URL = 'http://127.0.0.1:5500/index.html'
CHAT_URL = 'http://127.0.0.1:5500/chat.html'
HEADLESS = false   # change to true to run without opening browser

# ── Test counters ─────────────────────────────────────────────────
$passed = 0
$failed = 0

def log(status, test_name, detail = '')
  icon = status ? '✅ PASS' : '❌ FAIL'
  status ? $passed += 1 : $failed += 1
  detail_str = detail.empty? ? '' : " → #{detail}"
  puts "  #{icon}: #{test_name}#{detail_str}"
end

# ── Driver setup ──────────────────────────────────────────────────
def make_browser
  options = Selenium::WebDriver::Chrome::Options.new
  options.add_argument('--start-maximized')
  options.add_argument('--headless=new') if HEADLESS
  Watir::Browser.new(:chrome, options: options)
end

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════

def clear_session(browser)
  browser.execute_script('sessionStorage.clear();')
end

def wait_for(browser, timeout: 8, &block)
  Watir::Wait.until(timeout: timeout, &block)
end

def open_signup_modal(browser)
  browser.element(css: '.sign-up-btn').click
  wait_for(browser) { browser.div(id: 'authOverlay').present? }
  browser.button(id: 'tabSignUp').click
  wait_for(browser) { browser.div(id: 'panelSignUp').present? }
  sleep 0.3
end

def open_signin_modal(browser)
  browser.element(css: '.sign-in-btn').click
  wait_for(browser) { browser.div(id: 'authOverlay').present? }
  wait_for(browser) { browser.div(id: 'panelSignIn').present? }
  sleep 0.3
end

def fill_signup_form(browser,
                     first: 'Youssef',    last: 'Mohamed',
                     gender: 'male',      nationality: 'Egyptian',
                     study: 'software_engineering',
                     username: 'youssef_test01',
                     gmail: 'youssef.test01@gmail.com',
                     password: 'SecurePass1!',
                     confirm: 'SecurePass1!')
  browser.text_field(id: 'suFirstName').set(first)
  browser.text_field(id: 'suLastName').set(last)
  browser.select_list(id: 'suGender').select_value(gender)
  browser.text_field(id: 'suNationality').set(nationality)
  browser.select_list(id: 'suStudy').select_value(study)
  browser.text_field(id: 'suUsername').set(username)
  browser.text_field(id: 'suGmail').set(gmail)
  browser.text_field(id: 'suPassword').set(password)
  browser.text_field(id: 'suConfirm').set(confirm)
end

def click_create_account(browser)
  browser.element(css: '#panelSignUp .auth-submit-btn').click
end

def close_modal_if_open(browser)
  btn = browser.button(id: 'authCloseBtn')
  if btn.exists? && btn.visible?
    btn.click
    sleep 0.5
  end
rescue
  # modal already closed — nothing to do
end

def signup_fresh_user(browser,
                      username: 'youssef_test01',
                      gmail: 'youssef.test01@gmail.com')
  open_signup_modal(browser)
  fill_signup_form(browser, username: username, gmail: gmail)
  click_create_account(browser)
  sleep 2.5   # auth.js delays modal close by 1.2 s then animates out
end

# ══════════════════════════════════════════════════════════════════
#  TEST 1 — Page loads correctly
# ══════════════════════════════════════════════════════════════════
def test_page_loads(browser)
  puts "\n📋 TEST 1: Page loads correctly"
  browser.goto(SITE_URL)
  sleep 1

  begin
    title = browser.title
    log('CHATBOT'.in?(title.upcase) || !title.empty?, 'Page title is set', "title='#{title}'")
  rescue => e
    log(false, 'Page title is set', e.message)
  end

  begin
    log(browser.element(css: '.navbar').exists?, 'Navbar is present')
  rescue => e
    log(false, 'Navbar is present', e.message)
  end

  begin
    log(browser.element(css: '.sign-in-btn').exists? &&
        browser.element(css: '.sign-up-btn').exists?,
        'Sign In and Sign Up buttons visible in navbar')
  rescue => e
    log(false, 'Sign In and Sign Up buttons visible in navbar', e.message)
  end

  begin
    log(browser.button(id: 'getStartedBtn').exists?, 'Get Started button present')
  rescue => e
    log(false, 'Get Started button present', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 2 — Sign Up modal opens with all fields
# ══════════════════════════════════════════════════════════════════
def test_signup_modal_opens(browser)
  puts "\n📋 TEST 2: Sign Up modal opens"
  browser.goto(SITE_URL)
  clear_session(browser)

  begin
    open_signup_modal(browser)
    log(true, 'Auth modal appears after clicking Sign Up')
  rescue => e
    log(false, 'Auth modal appears after clicking Sign Up', e.message)
    return
  end

  begin
    log(browser.div(id: 'panelSignUp').visible?, 'Sign Up panel is visible')
  rescue => e
    log(false, 'Sign Up panel is visible', e.message)
  end

  begin
    fields = %w[suFirstName suLastName suGender suNationality
                suStudy suUsername suGmail suPassword suConfirm]
    all_found = fields.all? { |f| browser.element(id: f).exists? }
    log(all_found, 'All 9 signup form fields are present')
  rescue => e
    log(false, 'All 9 signup form fields are present', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 3 — Successful Sign Up
# ══════════════════════════════════════════════════════════════════
def test_successful_signup(browser)
  puts "\n📋 TEST 3: Successful Sign Up"
  browser.goto(SITE_URL)
  clear_session(browser)

  begin
    open_signup_modal(browser)
    fill_signup_form(browser, username: 'youssef_test01',
                              gmail: 'youssef.test01@gmail.com')
    click_create_account(browser)
    sleep 2.5

    # Modal should have closed
    overlay_hidden = !browser.div(id: 'authOverlay').visible?
    log(overlay_hidden, 'Modal closes after successful sign up')

    # User saved in sessionStorage
    users_raw = browser.execute_script("return sessionStorage.getItem('chatbot_users');")
    if users_raw
      users = JSON.parse(users_raw)
      found = users.any? { |u| u['username'] == 'youssef_test01' }
      log(found, 'User saved in sessionStorage user list')
    else
      log(false, 'User saved in sessionStorage user list', 'key not found')
    end

    # Session created
    session_raw = browser.execute_script("return sessionStorage.getItem('chatbot_session');")
    log(!session_raw.nil?, 'Session stored in sessionStorage after signup')

    # Navbar greets the user
    navbar_text = browser.element(css: '.nav-container').text
    log(navbar_text.include?('youssef_test01'),
        'Navbar shows Hello @youssef_test01 after signup',
        "navbar='#{navbar_text.strip}'")
  rescue => e
    log(false, 'Successful Sign Up flow', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 4 — Duplicate username rejected
# ══════════════════════════════════════════════════════════════════
def test_duplicate_username(browser)
  puts "\n📋 TEST 4: Duplicate username is rejected"
  browser.goto(SITE_URL)

  begin
    open_signup_modal(browser)
    fill_signup_form(browser, username: 'youssef_test01',
                              gmail: 'different.email@gmail.com')
    click_create_account(browser)
    sleep 1

    msg = browser.div(id: 'signupMsg').text
    log(msg.downcase.include?('taken') || msg.downcase.include?('already'),
        'Error shown for duplicate username', "msg='#{msg}'")
  rescue => e
    log(false, 'Duplicate username rejected', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 5 — Invalid Gmail rejected
# ══════════════════════════════════════════════════════════════════
def test_invalid_gmail(browser)
  puts "\n📋 TEST 5: Invalid Gmail is rejected"
  browser.goto(SITE_URL)

  begin
    open_signup_modal(browser)
    fill_signup_form(browser, username: 'newuser_xyz99',
                              gmail: 'notvalid@yahoo.com')
    click_create_account(browser)
    sleep 1

    msg = browser.div(id: 'signupMsg').text
    log(msg.downcase.include?('gmail') || msg.downcase.include?('valid'),
        'Error shown for non-gmail address', "msg='#{msg}'")
  rescue => e
    log(false, 'Invalid Gmail rejected', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 6 — Password mismatch rejected
# ══════════════════════════════════════════════════════════════════
def test_password_mismatch(browser)
  puts "\n📋 TEST 6: Password mismatch is rejected"
  browser.goto(SITE_URL)

  begin
    open_signup_modal(browser)
    fill_signup_form(browser, username: 'newuser_abc88',
                              gmail: 'newuser.abc88@gmail.com',
                              password: 'SecurePass1!',
                              confirm: 'DifferentPass9!')
    click_create_account(browser)
    sleep 1

    msg = browser.div(id: 'signupMsg').text
    log(msg.downcase.include?('match') || msg.downcase.include?('password'),
        'Error shown for password mismatch', "msg='#{msg}'")
  rescue => e
    log(false, 'Password mismatch rejected', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 7 — Empty form rejected
# ══════════════════════════════════════════════════════════════════
def test_empty_form(browser)
  puts "\n📋 TEST 7: Empty Sign Up form is rejected"
  browser.goto(SITE_URL)

  begin
    open_signup_modal(browser)
    click_create_account(browser)
    sleep 1

    msg = browser.div(id: 'signupMsg').text
    log(!msg.strip.empty?, 'Error shown when form is empty', "msg='#{msg}'")
  rescue => e
    log(false, 'Empty form rejected', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 8 — Short password rejected
# ══════════════════════════════════════════════════════════════════
def test_short_password(browser)
  puts "\n📋 TEST 8: Short password (< 8 chars) is rejected"
  browser.goto(SITE_URL)

  begin
    open_signup_modal(browser)
    fill_signup_form(browser, username: 'shortpassuser1',
                              gmail: 'shortpass.user1@gmail.com',
                              password: 'abc',
                              confirm: 'abc')
    click_create_account(browser)
    sleep 1

    msg = browser.div(id: 'signupMsg').text
    log(msg.include?('8') || msg.downcase.include?('character') || msg.downcase.include?('short'),
        'Error shown for short password', "msg='#{msg}'")
  rescue => e
    log(false, 'Short password rejected', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 9 — Sign In modal opens
# ══════════════════════════════════════════════════════════════════
def test_signin_modal_opens(browser)
  puts "\n📋 TEST 9: Sign In modal opens"
  browser.goto(SITE_URL)
  clear_session(browser)

  begin
    open_signin_modal(browser)
    log(true, 'Auth modal appears after clicking Sign In')
    log(browser.div(id: 'panelSignIn').visible?, 'Sign In panel is visible')
    log(browser.text_field(id: 'siUsername').visible? &&
        browser.text_field(id: 'siPassword').visible?,
        'Username and Password fields are visible')
  rescue => e
    log(false, 'Sign In modal opens', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 10 — Successful Sign In
# ══════════════════════════════════════════════════════════════════
def test_successful_signin(browser)
  puts "\n📋 TEST 10: Successful Sign In"
  browser.goto(SITE_URL)

  begin
    open_signin_modal(browser)
    browser.text_field(id: 'siUsername').set('youssef_test01')
    browser.text_field(id: 'siPassword').set('SecurePass1!')
    browser.element(css: '#panelSignIn .auth-submit-btn').click
    sleep 2

    log(!browser.div(id: 'authOverlay').visible?,
        'Modal closes after successful sign in')

    session_raw = browser.execute_script("return sessionStorage.getItem('chatbot_session');")
    if session_raw
      session = JSON.parse(session_raw)
      log(session['username'] == 'youssef_test01',
          'Correct user stored in session',
          "username='#{session['username']}'")
    else
      log(false, 'Session stored after sign in')
    end

    navbar_text = browser.element(css: '.nav-container').text
    log(navbar_text.include?('youssef_test01') || navbar_text.include?('Hello'),
        'Navbar shows Hello @username after sign in')
  rescue => e
    log(false, 'Successful Sign In', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 11 — Wrong password rejected
# ══════════════════════════════════════════════════════════════════
def test_wrong_password(browser)
  puts "\n📋 TEST 11: Wrong password is rejected"
  browser.goto(SITE_URL)
  clear_session(browser)
  browser.refresh

  begin
    open_signin_modal(browser)
    browser.text_field(id: 'siUsername').set('youssef_test01')
    browser.text_field(id: 'siPassword').set('WrongPassword99!')
    browser.element(css: '#panelSignIn .auth-submit-btn').click
    sleep 1

    msg = browser.div(id: 'signinMsg').text
    log(msg.downcase.include?('incorrect') || msg.downcase.include?('password'),
        'Error shown for wrong password', "msg='#{msg}'")
  rescue => e
    log(false, 'Wrong password rejected', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 12 — Non-existent username rejected
# ══════════════════════════════════════════════════════════════════
def test_nonexistent_user(browser)
  puts "\n📋 TEST 12: Non-existent username is rejected"
  browser.goto(SITE_URL)
  clear_session(browser)
  browser.refresh

  begin
    open_signin_modal(browser)
    browser.text_field(id: 'siUsername').set('ghost_user_99999')
    browser.text_field(id: 'siPassword').set('SomePass123!')
    browser.element(css: '#panelSignIn .auth-submit-btn').click
    sleep 1

    msg = browser.div(id: 'signinMsg').text
    log(msg.downcase.include?('not found') || msg.downcase.include?('username'),
        'Error shown for non-existent username', "msg='#{msg}'")
  rescue => e
    log(false, 'Non-existent username rejected', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 13 — Logout works
# ══════════════════════════════════════════════════════════════════
def test_logout(browser)
  puts "\n📋 TEST 13: Logout works"
  browser.goto(SITE_URL)

  begin
    open_signin_modal(browser)
    browser.text_field(id: 'siUsername').set('youssef_test01')
    browser.text_field(id: 'siPassword').set('SecurePass1!')
    browser.element(css: '#panelSignIn .auth-submit-btn').click
    sleep 2

    browser.button(text: 'Log Out').click
    sleep 2

    session = browser.execute_script("return sessionStorage.getItem('chatbot_session');")
    log(session.nil?, 'Session cleared after logout')

    log(browser.element(css: '.sign-in-btn').visible?,
        'Sign In button visible again after logout')
  rescue => e
    log(false, 'Logout works', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 14 — ESC key closes modal
# ══════════════════════════════════════════════════════════════════
def test_esc_closes_modal(browser)
  puts "\n📋 TEST 14: ESC key closes modal"
  browser.goto(SITE_URL)
  clear_session(browser)

  begin
    open_signup_modal(browser)
    sleep 0.4
    browser.send_keys :escape
    sleep 1

    log(!browser.div(id: 'authOverlay').visible?,
        'Modal closes on ESC key press')
  rescue => e
    log(false, 'ESC key closes modal', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 15 — Tab switching Sign In ↔ Sign Up
# ══════════════════════════════════════════════════════════════════
def test_tab_switching(browser)
  puts "\n📋 TEST 15: Tab switching between Sign In and Sign Up"
  browser.goto(SITE_URL)
  clear_session(browser)

  begin
    open_signin_modal(browser)

    browser.button(id: 'tabSignUp').click
    sleep 0.4
    log(browser.div(id: 'panelSignUp').visible?,
        'Clicking Sign Up tab shows Sign Up panel')

    browser.button(id: 'tabSignIn').click
    sleep 0.4
    log(browser.div(id: 'panelSignIn').visible?,
        'Clicking Sign In tab shows Sign In panel')
  rescue => e
    log(false, 'Tab switching', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 16 — Contact form present and fillable
# ══════════════════════════════════════════════════════════════════
def test_contact_form(browser)
  puts "\n📋 TEST 16: Contact form fields are present and fillable"
  browser.goto(SITE_URL)

  begin
    browser.execute_script("document.getElementById('aboutSection').scrollIntoView();")
    sleep 1

    browser.text_field(id: 'contactName').set('Test User')
    browser.text_field(id: 'contactEmail').set('test@gmail.com')
    browser.textarea(id: 'contactMessage').set('This is a Watir test message.')
    log(true, 'Contact form is present and fillable')

    log(browser.element(css: '.form-submit-btn').visible?,
        'Contact form submit button is visible')
  rescue => e
    log(false, 'Contact form present and fillable', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 17 — Get Started blocked without login
# ══════════════════════════════════════════════════════════════════
def test_get_started_blocked_without_login(browser)
  puts "\n📋 TEST 17: Get Started is blocked when not logged in"
  browser.goto(SITE_URL)
  clear_session(browser)
  browser.refresh
  sleep 1

  begin
    browser.button(id: 'getStartedBtn').click
    sleep 1.5

    still_on_index = !browser.url.include?('chat.html')
    log(still_on_index, 'User stays on index page when not logged in',
        "url='#{browser.url}'")

    error_class = browser.div(id: 'getStartedError').attribute_value('class') || ''
    log(error_class.include?('show'),
        'Error toast shown telling user to sign up first')
  rescue => e
    log(false, 'Get Started blocked without login', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 18 — Sign Up → Get Started → redirects to chat
# ══════════════════════════════════════════════════════════════════
def test_signup_then_get_started(browser)
  puts "\n📋 TEST 18: Sign Up → Get Started → Chat page loads"
  browser.goto(SITE_URL)
  clear_session(browser)

  begin
    signup_fresh_user(browser, username: 'youssef_test01',
                               gmail: 'youssef.test01@gmail.com')

    browser.button(id: 'getStartedBtn').click

    # main.js shows loading overlay for 1.5 s then redirects
    wait_for(browser, timeout: 8) { browser.url.include?('chat.html') }

    log(browser.url.include?('chat.html'),
        'Redirected to chat.html after Get Started',
        "url='#{browser.url}'")

    log(browser.url.include?('youssef_test01'),
        'Username passed correctly in URL to chat page',
        "url='#{browser.url}'")
  rescue => e
    log(false, 'Sign Up then Get Started redirects to chat', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 19 — Chat page UI loads correctly
# ══════════════════════════════════════════════════════════════════
def test_chat_page_loads(browser)
  puts "\n📋 TEST 19: Chat page UI loads correctly"
  browser.goto("#{CHAT_URL}?username=youssef_test01")
  sleep 2

  begin
    log(browser.element(css: '.navbar').exists?, 'Chat page navbar is present')
  rescue => e
    log(false, 'Chat page navbar is present', e.message)
  end

  begin
    displayed = browser.element(id: 'username').text.strip
    log(displayed == 'youssef_test01',
        'Username displayed correctly in chat navbar',
        "shown='#{displayed}'")
  rescue => e
    log(false, 'Username displayed in chat navbar', e.message)
  end

  begin
    log(browser.div(id: 'chatMessages').exists?, 'Chat messages container is present')
  rescue => e
    log(false, 'Chat messages container is present', e.message)
  end

  begin
    log(browser.text_field(id: 'messageInput').visible? &&
        browser.button(id: 'sendButton').visible?,
        'Message input and Send button are visible')
  rescue => e
    log(false, 'Message input and Send button visible', e.message)
  end

  begin
    sleep 2   # api.js adds greeting on DOMContentLoaded
    count = browser.elements(css: '.bot-message').count
    log(count > 0, 'Bot greeting message appears on load',
        "bot messages found: #{count}")
  rescue => e
    log(false, 'Bot greeting message appears on load', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 20 — User can type and send a message
# ══════════════════════════════════════════════════════════════════
def test_chat_send_message(browser)
  puts "\n📋 TEST 20: User can type and send a message in chat"
  browser.goto("#{CHAT_URL}?username=youssef_test01")
  sleep 2

  begin
    browser.text_field(id: 'messageInput').set('Hello from Watir test!')
    log(browser.text_field(id: 'messageInput').value == 'Hello from Watir test!',
        'Text typed correctly into message input')

    browser.button(id: 'sendButton').click
    sleep 1

    log(browser.text_field(id: 'messageInput').value == '',
        'Input field cleared after sending message')

    count = browser.elements(css: '.user-message').count
    log(count > 0, 'User message appears in chat window',
        "user messages found: #{count}")

    log(browser.div(id: 'typingIndicator').exists?,
        'Typing indicator element exists in DOM')
  rescue => e
    log(false, 'User can type and send a message', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 21 — Chat logout returns to index
# ══════════════════════════════════════════════════════════════════
def test_chat_logout(browser)
  puts "\n📋 TEST 21: Chat page logout returns to index page"
  browser.goto("#{CHAT_URL}?username=youssef_test01")
  sleep 2

  begin
    browser.button(id: 'logoutBtn').click
    sleep 2

    on_index = browser.url.include?('index.html') || browser.url.end_with?('5500/')
    log(on_index, 'Logout from chat returns to index.html',
        "url='#{browser.url}'")
  rescue => e
    log(false, 'Chat logout returns to index', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 22 — Enter key sends message in chat
# ══════════════════════════════════════════════════════════════════
def test_chat_enter_key(browser)
  puts "\n📋 TEST 22: Enter key sends message in chat"
  browser.goto("#{CHAT_URL}?username=youssef_test01")
  sleep 2

  begin
    browser.text_field(id: 'messageInput').set('Testing Enter key in Watir')
    browser.text_field(id: 'messageInput').send_keys :return
    sleep 1

    log(browser.text_field(id: 'messageInput').value == '',
        'Enter key sends the message (input cleared after send)')

    count = browser.elements(css: '.user-message').count
    log(count > 0, 'Message appears in chat after Enter key',
        "user messages: #{count}")
  rescue => e
    log(false, 'Enter key sends message', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  TEST 23 — Password strength indicator updates
# ══════════════════════════════════════════════════════════════════
def test_password_strength_indicator(browser)
  puts "\n📋 TEST 23: Password strength indicator updates"
  browser.goto(SITE_URL)
  clear_session(browser)

  begin
    open_signup_modal(browser)

    # Weak password
    browser.text_field(id: 'suPassword').set('abc')
    sleep 0.4
    label = browser.div(id: 'strengthLabel').text
    log(label.downcase.include?('weak') || label.downcase.include?('short') ||
        label.downcase.include?('too'),
        'Weak password shows weak label', "label='#{label}'")

    # Strong password
    browser.text_field(id: 'suPassword').clear
    browser.text_field(id: 'suPassword').set('StrongPass99!')
    sleep 0.4
    label = browser.div(id: 'strengthLabel').text
    log(label.downcase.include?('strong'),
        'Strong password shows strong label', "label='#{label}'")
  rescue => e
    log(false, 'Password strength indicator updates', e.message)
  end

  close_modal_if_open(browser)
end

# ══════════════════════════════════════════════════════════════════
#  TEST 24 — Enter key submits Sign In form
# ══════════════════════════════════════════════════════════════════
def test_enter_key_signin(browser)
  puts "\n📋 TEST 24: Enter key submits Sign In form"
  browser.goto(SITE_URL)

  begin
    open_signin_modal(browser)
    browser.text_field(id: 'siUsername').set('youssef_test01')
    browser.text_field(id: 'siPassword').set('SecurePass1!')
    browser.text_field(id: 'siPassword').send_keys :return
    sleep 2

    log(!browser.div(id: 'authOverlay').visible?,
        'Enter key submits Sign In and closes modal')
  rescue => e
    log(false, 'Enter key submits Sign In form', e.message)
  end
end

# ══════════════════════════════════════════════════════════════════
#  MAIN — Run all tests
# ══════════════════════════════════════════════════════════════════
require 'json'

puts '=' * 60
puts '  🦁 ChatBot Watir Test Suite'
puts "  Make sure your site is running on: #{SITE_URL}"
puts '=' * 60

browser = make_browser

begin
  # ── Index page & auth tests ───────────────────────────────
  test_page_loads(browser)
  test_signup_modal_opens(browser)
  test_successful_signup(browser)
  test_duplicate_username(browser)
  test_invalid_gmail(browser)
  test_password_mismatch(browser)
  test_empty_form(browser)
  test_short_password(browser)
  test_signin_modal_opens(browser)
  test_successful_signin(browser)
  test_wrong_password(browser)
  test_nonexistent_user(browser)
  test_logout(browser)
  test_esc_closes_modal(browser)
  test_tab_switching(browser)
  test_contact_form(browser)
  test_password_strength_indicator(browser)
  test_enter_key_signin(browser)

  # ── Get Started + Chat page tests ─────────────────────────
  test_get_started_blocked_without_login(browser)
  test_signup_then_get_started(browser)
  test_chat_page_loads(browser)
  test_chat_send_message(browser)
  test_chat_logout(browser)
  test_chat_enter_key(browser)

ensure
  browser.close
end

puts "\n" + '=' * 60
puts "  Results: #{$passed} passed,  #{$failed} failed  (total #{$passed + $failed})"
puts '=' * 60