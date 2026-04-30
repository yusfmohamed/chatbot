// Get username from URL parameters
function getUsername() {
    const urlParams = new URLSearchParams(window.location.search);
    const username = urlParams.get('username');
    return username || 'User';
}

let storedUsername = getUsername();

// Insert username into welcome text
document.getElementById('username').textContent = storedUsername;

// Logout functionality
document.getElementById('logoutBtn').addEventListener('click', () => {
    window.location.href = 'index.html';
});

// DOM elements
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const typingIndicator = document.getElementById('typingIndicator');

// 🔑 Gemini API Key
const GEMINI_API_KEY = "Add Your Gemini API Key Here";

// ✅ Updated correct model names (2026)
const MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash-001",
];

// Helper: Get user avatar
function getUserAvatar() {
    return storedUsername.charAt(0).toUpperCase();
}

// Helper: Format time
function formatTime() {
    return new Date().toLocaleTimeString();
}

// Add message
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    const avatar = isUser ? getUserAvatar() : '🤖';
    const avatarClass = isUser ? 'user-avatar' : 'bot-avatar';

    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="${avatarClass}">${avatar}</div>
            <div class="message-text">
                <p>${text}</p>
            </div>
        </div>
        <div class="message-time">${formatTime()}</div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Typing indicator
function showTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.classList.add('active');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function hideTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.classList.remove('active');
    }
}

// ✅ Call Gemini API with correct headers and model fallback
async function callGeminiAPI(message) {
    for (const model of MODELS) {
        try {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-goog-api-key': GEMINI_API_KEY   // ✅ correct header
                },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: message }] }],
                    generationConfig: {
                        temperature: 0.9,
                        maxOutputTokens: 1000
                    }
                })
            });

            const data = await response.json();

            if (!response.ok) {
                console.warn(`Model ${model} failed (${response.status}):`, data?.error?.message);
                continue;
            }

            console.log(`✅ Success with model: ${model}`);
            return data.candidates[0].content.parts[0].text;

        } catch (error) {
            console.warn(`Model ${model} threw an error:`, error.message);
            continue;
        }
    }

    return "⚠️ All models failed. Check your API key at aistudio.google.com";
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    sendButton.disabled = true;
    messageInput.disabled = true;

    addMessage(message, true);
    messageInput.value = '';

    showTypingIndicator();

    try {
        const aiResponse = await callGeminiAPI(message);
        hideTypingIndicator();
        addMessage(aiResponse);
    } catch (error) {
        hideTypingIndicator();
        addMessage("⚠️ Oops, something went wrong.");
        console.error(error);
    } finally {
        sendButton.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

// Events
if (sendButton) {
    sendButton.addEventListener('click', sendMessage);
}

if (messageInput) {
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    messageInput.focus();
}

// ✅ Static greeting - no API call on load
document.addEventListener('DOMContentLoaded', function () {
    addMessage(`👋 Hello ${storedUsername}! How can I help you today?`);
});