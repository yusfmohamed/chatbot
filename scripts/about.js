// ──────────────────────────────────────────────
// about.js  –  About Us section logic
// ──────────────────────────────────────────────

// ── Scroll-in animation via IntersectionObserver ──
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

const aboutElements = document.querySelectorAll('.about-content, .contact-section');
aboutElements.forEach(el => observer.observe(el));

// ── Social icon hover effects ──
const socialLinks = document.querySelectorAll('.social-link');
socialLinks.forEach(link => {
    link.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-10px) scale(1.05)';
    });
    link.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// ── Contact messages LocalStorage helpers ──
const MESSAGES_KEY = 'chatbot_messages';

function getMessages() {
    return JSON.parse(localStorage.getItem(MESSAGES_KEY) || '[]');
}

function saveMessage(msg) {
    const messages = getMessages();
    messages.push(msg);
    localStorage.setItem(MESSAGES_KEY, JSON.stringify(messages));
}

// ── Inject success popup HTML + styles into page ──
function injectContactPopup() {
    const popup = document.createElement('div');
    popup.id = 'contactPopup';
    popup.innerHTML = `
        <div class="contact-popup-overlay" id="contactPopupOverlay">
            <div class="contact-popup-card" id="contactPopupCard">
                <div class="popup-icon-wrap">
                    <svg class="popup-checkmark" viewBox="0 0 52 52">
                        <circle class="popup-checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
                        <path class="popup-checkmark-check" fill="none" d="M14 27l8 8 16-16"/>
                    </svg>
                </div>
                <h3 class="popup-title">Message Sent!</h3>
                <p class="popup-body">
                    Thanks for reaching out.<br>
                    We'll get back to you as soon as possible.
                </p>
                <div class="popup-summary" id="popupSummary"></div>
                <button class="popup-close-btn" id="popupCloseBtn">Got it</button>
            </div>
        </div>
    `;
    document.body.appendChild(popup);

    const style = document.createElement('style');
    style.textContent = `
        .contact-popup-overlay {
            position: fixed;
            inset: 0;
            background: rgba(10,10,10,0.82);
            backdrop-filter: blur(10px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 99999;
            opacity: 0;
            transition: opacity 0.35s ease;
        }
        .contact-popup-overlay.show {
            display: flex;
            opacity: 1;
        }
        .contact-popup-card {
            background: rgba(20, 20, 35, 0.96);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 24px;
            padding: 3rem 2.5rem 2.5rem;
            width: 420px;
            max-width: 92vw;
            text-align: center;
            box-shadow: 0 0 0 1px rgba(255,255,255,0.04), 0 30px 70px rgba(0,0,0,0.6), 0 0 60px rgba(139,92,246,0.12);
            transform: translateY(30px) scale(0.95);
            transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        .contact-popup-overlay.show .contact-popup-card {
            transform: translateY(0) scale(1);
        }
        .popup-icon-wrap {
            width: 80px;
            height: 80px;
            margin: 0 auto 1.5rem;
        }
        .popup-checkmark {
            width: 80px;
            height: 80px;
            stroke: #10b981;
            stroke-width: 2;
        }
        .popup-checkmark-circle {
            stroke-dasharray: 166;
            stroke-dashoffset: 166;
            stroke-width: 2;
            stroke: #10b981;
            animation: popupStroke 0.6s cubic-bezier(0.65,0,0.45,1) 0.2s forwards;
        }
        .popup-checkmark-check {
            stroke-dasharray: 48;
            stroke-dashoffset: 48;
            stroke-width: 3;
            stroke-linecap: round;
            stroke-linejoin: round;
            animation: popupStroke 0.4s cubic-bezier(0.65,0,0.45,1) 0.8s forwards;
        }
        @keyframes popupStroke {
            100% { stroke-dashoffset: 0; }
        }
        .popup-title {
            font-size: 1.7rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.6rem;
            letter-spacing: -0.4px;
        }
        .popup-body {
            color: rgba(255,255,255,0.55);
            font-size: 0.95rem;
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }
        .popup-summary {
            background: rgba(139,92,246,0.1);
            border: 1px solid rgba(139,92,246,0.2);
            border-radius: 12px;
            padding: 0.9rem 1.2rem;
            margin-bottom: 1.8rem;
            text-align: left;
            font-size: 0.82rem;
            color: rgba(255,255,255,0.6);
            line-height: 1.9;
        }
        .popup-summary strong {
            color: #a78bfa;
            font-weight: 600;
        }
        .popup-close-btn {
            width: 100%;
            padding: 0.9rem;
            background: linear-gradient(135deg, #8b5cf6, #a855f7);
            border: none;
            border-radius: 12px;
            color: #fff;
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .popup-close-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 28px rgba(139,92,246,0.4);
        }
    `;
    document.head.appendChild(style);

    document.getElementById('popupCloseBtn').addEventListener('click', closeContactPopup);
    document.getElementById('contactPopupOverlay').addEventListener('click', function(e) {
        if (e.target === this) closeContactPopup();
    });
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeContactPopup();
    });
}

function showContactPopup(name, email, message) {
    const overlay = document.getElementById('contactPopupOverlay');
    const summary = document.getElementById('popupSummary');

    summary.innerHTML = `
        <div><strong>Name &nbsp;&nbsp;:</strong> ${name}</div>
        <div><strong>Email &nbsp;&nbsp;:</strong> ${email}</div>
        <div><strong>Message:</strong> ${message.length > 80 ? message.slice(0, 80) + '…' : message}</div>
    `;

    overlay.style.display = 'flex';
    requestAnimationFrame(() => {
        requestAnimationFrame(() => overlay.classList.add('show'));
    });
}

function closeContactPopup() {
    const overlay = document.getElementById('contactPopupOverlay');
    overlay.classList.remove('show');
    setTimeout(() => { overlay.style.display = 'none'; }, 350);
}

// ── Contact form submission ──
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const submitBtn    = this.querySelector('.form-submit-btn');
    const spanEl       = submitBtn.querySelector('span');
    const originalText = spanEl.textContent;

    const name    = document.getElementById('contactName').value.trim();
    const email   = document.getElementById('contactEmail').value.trim();
    const message = document.getElementById('contactMessage').value.trim();

    // Loading state
    submitBtn.classList.add('loading');
    spanEl.textContent = 'Sending...';
    submitBtn.disabled = true;

    setTimeout(() => {
        // Save to LocalStorage — Selenium can read chatbot_messages key
        saveMessage({
            id:     Date.now(),
            name,
            email,
            message,
            sentAt: new Date().toISOString(),
            status: 'received'
        });

        // Reset button
        submitBtn.classList.remove('loading');
        submitBtn.classList.add('success');
        spanEl.textContent = 'Message Sent!';
        submitBtn.disabled = false;
        contactForm.reset();

        // Show popup
        showContactPopup(name, email, message);

        // Reset button label after 3s
        setTimeout(() => {
            submitBtn.classList.remove('success');
            spanEl.textContent = originalText;
        }, 3000);

    }, 1500);
});

// ── Init ──
injectContactPopup();