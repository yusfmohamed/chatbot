// ──────────────────────────────────────────────
// main.js  –  Get Started logic (auth-gated)
// ──────────────────────────────────────────────

// Page load fade animation
window.addEventListener('load', function () {
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach((el, index) => {
        setTimeout(() => el.classList.add('fade-in-active'), index * 200);
    });
});

// ── "Sign up first" error toast ──────────────
let errorTimer = null;

function showGetStartedError() {
    const el = document.getElementById('getStartedError');
    el.classList.add('show');
    clearTimeout(errorTimer);
    errorTimer = setTimeout(() => el.classList.remove('show'), 3500);
}

// ── Get Started button ────────────────────────
document.getElementById('getStartedBtn').addEventListener('click', function () {
    const session = sessionStorage.getItem('chatbot_session');

    if (!session) {
        // Not logged in → show error, then open sign-in modal after short delay
        showGetStartedError();
        setTimeout(() => {
            if (typeof openAuthModal === 'function') openAuthModal('signup');
        }, 1000);
        return;
    }

    // Logged in → go straight to chat
    const user = JSON.parse(session);
    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.style.display = 'flex';

    setTimeout(() => {
        window.location.href = `chat.html?username=${encodeURIComponent(user.username)}`;
    }, 1500);
});

// ── Hide Spline watermark ──────────────────────
setTimeout(() => {
    const splineViewer = document.querySelector('spline-viewer');
    if (splineViewer && splineViewer.shadowRoot) {
        const style = document.createElement('style');
        style.textContent = `.logo, .logo-container, .watermark { display: none !important; }`;
        splineViewer.shadowRoot.appendChild(style);
    }
}, 2000);