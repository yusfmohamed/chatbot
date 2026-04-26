// ══════════════════════════════════════════════════════
//  auth.js  –  Sign Up / Sign In  (SessionStorage-based)
//  Fields: firstName, lastName, gender, nationality,
//          fieldOfStudy, gmail, username, password
// ══════════════════════════════════════════════════════

// ── Storage helpers (sessionStorage only — no localStorage) ──────
const DB_KEY = 'chatbot_users';

function getUsers() {
    return JSON.parse(sessionStorage.getItem(DB_KEY) || '[]');
}
function saveUsers(users) {
    sessionStorage.setItem(DB_KEY, JSON.stringify(users));
}
function findUser(username) {
    return getUsers().find(u => u.username.toLowerCase() === username.toLowerCase());
}
function findUserByGmail(gmail) {
    return getUsers().find(u => u.gmail.toLowerCase() === gmail.toLowerCase());
}

// ── Toast ─────────────────────────────────────────────
function showToast(message, type = 'success') {
    let toast = document.getElementById('authToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'authToast';
        toast.className = 'auth-toast';
        document.body.appendChild(toast);
    }
    const icon = type === 'success' ? '✓' : '✕';
    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    toast.className = `auth-toast toast-${type} show`;
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.remove('show'), 3200);
}

// ── Inject modal HTML ─────────────────────────────────
function injectAuthModal() {
    const html = `
    <!-- ══ AUTH OVERLAY ══ -->
    <div class="auth-overlay" id="authOverlay">
      <div class="auth-card" id="authCard">
        <button class="auth-close-btn" id="authCloseBtn" aria-label="Close">&times;</button>

        <!-- Header -->
        <div class="auth-header">
          <div class="auth-logo-badge">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/></svg>
            CHATBOT
          </div>
          <h2 class="auth-title" id="authTitle">Welcome Back</h2>
          <p class="auth-subtitle" id="authSubtitle">Sign in to continue your AI journey</p>
        </div>

        <!-- Tabs -->
        <div class="auth-tabs">
          <button class="auth-tab active" id="tabSignIn" onclick="switchTab('signin')">Sign In</button>
          <button class="auth-tab"        id="tabSignUp" onclick="switchTab('signup')">Sign Up</button>
        </div>

        <!-- ══ SIGN IN PANEL ══ -->
        <div class="auth-panel active" id="panelSignIn">
          <div class="auth-msg" id="signinMsg"></div>

          <div class="auth-field">
            <label>Username</label>
            <div style="position:relative">
              <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/></svg>
              <input class="auth-input" type="text" id="siUsername" placeholder="Your username" autocomplete="off">
            </div>
          </div>

          <div class="auth-field">
            <label>Password</label>
            <div style="position:relative">
              <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
              <input class="auth-input" type="password" id="siPassword" placeholder="Your password" style="padding-right:2.6rem">
              <button class="auth-eye-btn" type="button" onclick="toggleEye('siPassword',this)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
              </button>
            </div>
          </div>

          <button class="auth-submit-btn" onclick="handleSignIn()"><span>Sign In →</span></button>

          <p class="auth-switch">
            Don't have an account?
            <button class="auth-switch-link" onclick="switchTab('signup')">Create one</button>
          </p>
        </div>

        <!-- ══ SIGN UP PANEL ══ -->
        <div class="auth-panel" id="panelSignUp">
          <div class="auth-msg" id="signupMsg"></div>

          <!-- First + Last Name -->
          <div class="auth-row">
            <div class="auth-field">
              <label>First Name</label>
              <div style="position:relative">
                <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/></svg>
                <input class="auth-input" type="text" id="suFirstName" placeholder="First name">
              </div>
            </div>
            <div class="auth-field">
              <label>Last Name</label>
              <div style="position:relative">
                <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/></svg>
                <input class="auth-input" type="text" id="suLastName" placeholder="Last name">
              </div>
            </div>
          </div>

          <!-- Gender + Nationality -->
          <div class="auth-row">
            <div class="auth-field">
              <label>Gender</label>
              <div class="auth-select-wrap" style="position:relative">
                <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M17.58 4H14V2h6v6h-2V4.41l-3.83 3.83A5 5 0 0 1 15 12a5 5 0 0 1-5 5 5 5 0 0 1-5-5 5 5 0 0 1 5-5c1.03 0 1.98.31 2.77.84L16.17 4zM10 9a3 3 0 0 0-3 3 3 3 0 0 0 3 3 3 3 0 0 0 3-3 3 3 0 0 0-3-3zm-5 9h10v2H5z"/></svg>
                <select class="auth-input auth-select" id="suGender">
                  <option value="">Select...</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="prefer_not">Prefer not to say</option>
                </select>
              </div>
            </div>
            <div class="auth-field">
              <label>Nationality</label>
              <div style="position:relative">
                <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm6.93 6h-2.95c-.32-1.25-.78-2.45-1.38-3.56 1.84.63 3.37 1.9 4.33 3.56zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14C4.1 13.36 4 12.69 4 12s.1-1.36.26-2h3.38c-.08.66-.14 1.32-.14 2s.06 1.34.14 2H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56-1.84-.63-3.37-1.9-4.33-3.56zm2.95-8H5.08c.96-1.66 2.49-2.93 4.33-3.56C8.81 5.55 8.35 6.75 8.03 8zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96zM14.34 14H9.66c-.09-.66-.16-1.32-.16-2s.07-1.35.16-2h4.68c.09.65.16 1.32.16 2s-.07 1.34-.16 2zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95c-.96 1.66-2.49 2.93-4.33 3.56zM16.36 14c.08-.66.14-1.32.14-2s-.06-1.34-.14-2h3.38c.16.64.26 1.31.26 2s-.1 1.36-.26 2h-3.38z"/></svg>
                <input class="auth-input" type="text" id="suNationality" placeholder="e.g. Egyptian">
              </div>
            </div>
          </div>

          <!-- Field of Study -->
          <div class="auth-field">
            <label>Field of Study</label>
            <div class="auth-select-wrap" style="position:relative">
              <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3L1 9l4 2.18v6L12 21l7-3.82v-6l2-1.09V17h2V9L12 3zm6.82 6L12 12.72 5.18 9 12 5.28 18.82 9zM17 15.99l-5 2.73-5-2.73v-3.72L12 15l5-2.73v3.72z"/></svg>
              <select class="auth-input auth-select" id="suStudy">
                <option value="">Select your field...</option>
                <option value="computer_science">Computer Science</option>
                <option value="software_engineering">Software Engineering</option>
                <option value="information_technology">Information Technology</option>
                <option value="data_science">Data Science & AI</option>
                <option value="graphic_design">Graphic Design</option>
                <option value="business">Business Administration</option>
                <option value="engineering">Engineering</option>
                <option value="medicine">Medicine</option>
                <option value="law">Law</option>
                <option value="arts">Arts & Humanities</option>
                <option value="science">Natural Sciences</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>

          <!-- Username -->
          <div class="auth-field">
            <label>Username</label>
            <div style="position:relative">
              <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/></svg>
              <input class="auth-input" type="text" id="suUsername" placeholder="Choose a username" autocomplete="off">
            </div>
          </div>

          <!-- Gmail -->
          <div class="auth-field">
            <label>Gmail Address</label>
            <div style="position:relative">
              <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
              <input class="auth-input" type="email" id="suGmail" placeholder="yourname@gmail.com">
            </div>
          </div>

          <!-- Password -->
          <div class="auth-field">
            <label>Password</label>
            <div style="position:relative">
              <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
              <input class="auth-input" type="password" id="suPassword" placeholder="Create a password" style="padding-right:2.6rem" oninput="checkStrength(this.value)">
              <button class="auth-eye-btn" type="button" onclick="toggleEye('suPassword',this)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
              </button>
            </div>
            <div class="strength-bar-wrap">
              <div class="strength-seg" id="seg1"></div>
              <div class="strength-seg" id="seg2"></div>
              <div class="strength-seg" id="seg3"></div>
            </div>
            <div class="strength-label" id="strengthLabel">Enter a password</div>
          </div>

          <!-- Confirm Password -->
          <div class="auth-field">
            <label>Confirm Password</label>
            <div style="position:relative">
              <svg class="auth-field-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
              <input class="auth-input" type="password" id="suConfirm" placeholder="Repeat your password" style="padding-right:2.6rem">
              <button class="auth-eye-btn" type="button" onclick="toggleEye('suConfirm',this)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
              </button>
            </div>
          </div>

          <button class="auth-submit-btn" onclick="handleSignUp()"><span>Create Account →</span></button>

          <p class="auth-switch">
            Already have an account?
            <button class="auth-switch-link" onclick="switchTab('signin')">Sign In</button>
          </p>
        </div>

      </div><!-- /auth-card -->
    </div><!-- /auth-overlay -->

    <!-- Toast -->
    <div class="auth-toast" id="authToast"></div>
    `;
    document.body.insertAdjacentHTML('beforeend', html);
}

// ── Tab switcher ──────────────────────────────────────
function switchTab(tab) {
    const isSignIn = tab === 'signin';
    document.getElementById('tabSignIn').classList.toggle('active', isSignIn);
    document.getElementById('tabSignUp').classList.toggle('active', !isSignIn);
    document.getElementById('panelSignIn').classList.toggle('active', isSignIn);
    document.getElementById('panelSignUp').classList.toggle('active', !isSignIn);
    document.getElementById('authTitle').textContent    = isSignIn ? 'Welcome Back'       : 'Create Account';
    document.getElementById('authSubtitle').textContent = isSignIn ? 'Sign in to continue your AI journey' : 'Join ChatBot and start exploring';
    clearMsgs();
}

function clearMsgs() {
    ['signinMsg', 'signupMsg'].forEach(id => {
        const el = document.getElementById(id);
        if (el) { el.className = 'auth-msg'; el.textContent = ''; }
    });
}

function showMsg(id, text, type) {
    const el = document.getElementById(id);
    el.textContent = text;
    el.className = `auth-msg ${type}`;
}

// ── Password eye toggle ───────────────────────────────
function toggleEye(inputId, btn) {
    const inp = document.getElementById(inputId);
    const show = inp.type === 'password';
    inp.type = show ? 'text' : 'password';
    btn.style.color = show ? 'rgba(139,92,246,0.8)' : 'rgba(255,255,255,0.35)';
}

// ── Password strength ─────────────────────────────────
function checkStrength(val) {
    const segs  = [document.getElementById('seg1'), document.getElementById('seg2'), document.getElementById('seg3')];
    const label = document.getElementById('strengthLabel');
    segs.forEach(s => s.className = 'strength-seg');

    if (!val) { label.textContent = 'Enter a password'; return; }

    let score = 0;
    if (val.length >= 8) score++;
    if (/[A-Z]/.test(val) && /[a-z]/.test(val)) score++;
    if (/[0-9]/.test(val) && /[^A-Za-z0-9]/.test(val)) score++;

    const levels = ['weak', 'medium', 'strong'];
    const labels = ['Weak — add numbers & symbols', 'Medium — add special characters', 'Strong password ✓'];
    for (let i = 0; i < score; i++) segs[i].classList.add(levels[score - 1]);
    label.textContent = labels[score - 1] || 'Too short';
}

// ── Open / close modal ────────────────────────────────
function openAuthModal(defaultTab = 'signin') {
    const overlay = document.getElementById('authOverlay');
    overlay.style.display = 'flex';
    setTimeout(() => overlay.classList.add('active'), 10);
    switchTab(defaultTab);
}

function closeAuthModal() {
    const overlay = document.getElementById('authOverlay');
    overlay.classList.remove('active');
    setTimeout(() => { overlay.style.display = 'none'; }, 350);
}

// ── Navbar: show "Hello @username" ────────────────────
function updateNavbarLoggedIn(user) {
    const authBtns = document.querySelector('.auth-buttons');
    if (!authBtns) return;

    authBtns.innerHTML = `
        <span class="navbar-greeting">
            Hello,&nbsp;<strong class="navbar-username">${user.username}</strong>
        </span>
        <button class="sign-up-btn logout-btn" onclick="handleLogout()">
            Log Out
        </button>
    `;

    // Inject greeting styles once
    if (!document.getElementById('navbarGreetingStyle')) {
        const style = document.createElement('style');
        style.id = 'navbarGreetingStyle';
        style.textContent = `
            .navbar-greeting {
                display: flex;
                align-items: center;
                gap: 0.3rem;
                color: rgba(255, 255, 255, 0.85);
                font-size: 0.95rem;
                font-weight: 500;
                letter-spacing: 0.01em;
                animation: greetingFadeIn 0.5s ease forwards;
            }
            .navbar-username {
                color: #a78bfa;
                font-weight: 700;
                font-size: 1rem;
            }
            .logout-btn {
                background: rgba(239, 68, 68, 0.15) !important;
                border: 1px solid rgba(239, 68, 68, 0.3) !important;
                color: #fca5a5 !important;
            }
            .logout-btn:hover {
                background: rgba(239, 68, 68, 0.28) !important;
            }
            @keyframes greetingFadeIn {
                from { opacity: 0; transform: translateX(10px); }
                to   { opacity: 1; transform: translateX(0); }
            }
        `;
        document.head.appendChild(style);
    }
}

// ── SIGN IN handler ───────────────────────────────────
function handleSignIn() {
    clearMsgs();
    const username = document.getElementById('siUsername').value.trim();
    const password = document.getElementById('siPassword').value;

    if (!username || !password) {
        showMsg('signinMsg', 'Please fill in all fields.', 'error'); return;
    }

    const user = findUser(username);
    if (!user) {
        showMsg('signinMsg', 'Username not found. Please sign up first.', 'error'); return;
    }
    if (user.password !== btoa(password)) {
        showMsg('signinMsg', 'Incorrect password. Please try again.', 'error'); return;
    }

    // Store session
    const sessionData = {
        username: user.username,
        firstName: user.firstName,
        lastName: user.lastName,
        gmail: user.gmail,
        fieldOfStudy: user.fieldOfStudy
    };
    sessionStorage.setItem('chatbot_session', JSON.stringify(sessionData));

    closeAuthModal();
    showToast(`Welcome back, ${user.firstName}! 👋`, 'success');
    updateNavbarLoggedIn(user);
}

// ── SIGN UP handler ───────────────────────────────────
function handleSignUp() {
    clearMsgs();

    const firstName   = document.getElementById('suFirstName').value.trim();
    const lastName    = document.getElementById('suLastName').value.trim();
    const gender      = document.getElementById('suGender').value;
    const nationality = document.getElementById('suNationality').value.trim();
    const study       = document.getElementById('suStudy').value;
    const username    = document.getElementById('suUsername').value.trim();
    const gmail       = document.getElementById('suGmail').value.trim();
    const password    = document.getElementById('suPassword').value;
    const confirm     = document.getElementById('suConfirm').value;

    // Validation
    if (!firstName || !lastName || !gender || !nationality || !study || !username || !gmail || !password || !confirm) {
        showMsg('signupMsg', 'Please fill in all fields.', 'error'); return;
    }
    if (!/^[^\s@]+@gmail\.com$/i.test(gmail)) {
        showMsg('signupMsg', 'Please enter a valid @gmail.com address.', 'error'); return;
    }
    if (password.length < 8) {
        showMsg('signupMsg', 'Password must be at least 8 characters.', 'error'); return;
    }
    if (password !== confirm) {
        showMsg('signupMsg', 'Passwords do not match.', 'error'); return;
    }
    if (findUser(username)) {
        showMsg('signupMsg', 'Username already taken. Choose another.', 'error'); return;
    }
    if (findUserByGmail(gmail)) {
        showMsg('signupMsg', 'This Gmail is already registered.', 'error'); return;
    }

    // Save new user into sessionStorage user list
    const users = getUsers();
    const newUser = {
        firstName, lastName, gender, nationality,
        fieldOfStudy: study, username, gmail,
        password: btoa(password),
        createdAt: new Date().toISOString()
    };
    users.push(newUser);
    saveUsers(users);

    // Store session
    const sessionData = { username, firstName, lastName, gmail, fieldOfStudy: study };
    sessionStorage.setItem('chatbot_session', JSON.stringify(sessionData));

    showMsg('signupMsg', '✓ Account created! Logging you in...', 'success');
    showToast(`Welcome, @${username}! You're all set 🎉`, 'success');

    setTimeout(() => {
        closeAuthModal();
        updateNavbarLoggedIn(newUser);
    }, 1200);
}

// ── Logout ────────────────────────────────────────────
function handleLogout() {
    sessionStorage.removeItem('chatbot_session');
    location.reload();
}

// ── Restore session on page load ──────────────────────
function checkSession() {
    const raw = sessionStorage.getItem('chatbot_session');
    if (raw) {
        const user = JSON.parse(raw);
        updateNavbarLoggedIn(user);
    }
}

// ── Wire up navbar Sign In / Sign Up buttons ──────────
function wireNavButtons() {
    const signInBtn = document.querySelector('.sign-in-btn');
    const signUpBtn = document.querySelector('.sign-up-btn');
    if (signInBtn) signInBtn.addEventListener('click', () => openAuthModal('signin'));
    if (signUpBtn) signUpBtn.addEventListener('click', () => openAuthModal('signup'));
}

// ── Init ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    injectAuthModal();

    document.getElementById('authCloseBtn').addEventListener('click', closeAuthModal);

    document.getElementById('authOverlay').addEventListener('click', function (e) {
        if (e.target === this) closeAuthModal();
    });

    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') closeAuthModal();
    });

    document.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
            if (document.getElementById('panelSignIn').classList.contains('active')) handleSignIn();
            if (document.getElementById('panelSignUp').classList.contains('active')) handleSignUp();
        }
    });

    wireNavButtons();
    checkSession();
});