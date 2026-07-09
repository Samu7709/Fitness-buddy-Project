/**
 * ============================================================
 *  FITNESS BUDDY AI — Chatbot JavaScript
 *  Handles: send/receive messages, conversation history,
 *           typing animation, auto-scroll, suggestions
 * ============================================================
 */

// Conversation history (kept in memory for context)
let chatHistory = [];

/**
 * Handles Enter / Shift+Enter in the chat textarea.
 */
function handleChatKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
}

/**
 * Sends a suggestion chip message.
 */
function sendSuggestion(text) {
  const input = document.getElementById('chatInput');
  if (input) input.value = text;
  // Hide suggestions after first use
  const suggestionsEl = document.getElementById('suggestions');
  if (suggestionsEl) {
    suggestionsEl.style.transition = 'opacity .3s';
    suggestionsEl.style.opacity = '0';
    setTimeout(() => suggestionsEl.remove(), 300);
  }
  sendMessage();
}

/**
 * Main send message function.
 * Reads from #chatInput, appends to chat, calls /api/chat.
 */
async function sendMessage() {
  const input = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const message = (input.value || '').trim();

  if (!message) return;

  // Append user message to UI
  appendMessage('user', message);
  input.value = '';
  input.style.height = 'auto';

  // Disable send button while waiting
  if (sendBtn) sendBtn.disabled = true;

  // Add to history
  chatHistory.push({ role: 'user', content: message });

  // Show typing indicator
  showTyping(true);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: message,
        history: chatHistory.slice(-10),  // last 10 messages for context
      }),
    });

    if (!response.ok) throw new Error('API error: ' + response.status);

    const data = await response.json();
    const botReply = data.response || 'I had trouble understanding that. Could you rephrase?';

    // Add to history
    chatHistory.push({ role: 'assistant', content: botReply });

    // Simulate slight delay for realism
    await sleep(400);
    showTyping(false);

    // Append bot message
    appendMessage('bot', botReply, data.timestamp);

  } catch (error) {
    console.error('Chat error:', error);
    showTyping(false);
    appendMessage('bot',
      'Oops! I ran into a connection issue. Please check your internet and try again. 🔧',
      getCurrentTime()
    );
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    scrollToBottom();
  }
}

/**
 * Appends a message bubble to the chat window.
 * @param {string} role  - 'user' or 'bot'
 * @param {string} text  - Message content (supports line breaks)
 * @param {string} time  - Optional time string
 */
function appendMessage(role, text, time = null) {
  const messagesEl = document.getElementById('chatMessages');
  if (!messagesEl) return;

  const isBot = role === 'bot';
  const timestamp = time || getCurrentTime();

  // Format text: convert newlines to <br> and **bold** to <strong>
  const formattedText = formatMessage(text);

  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-message ${isBot ? 'bot-message' : 'user-message'}`;
  msgDiv.style.animation = 'fadeUp .3s ease both';

  msgDiv.innerHTML = `
    <div class="message-avatar ${isBot ? 'bot-avatar' : 'user-avatar'}">
      <i class="bi bi-${isBot ? 'lightning-charge-fill' : 'person-fill'}"></i>
    </div>
    <div class="message-bubble ${isBot ? 'bot-bubble' : 'user-bubble'}">
      ${formattedText}
      <div class="message-time">${timestamp}</div>
    </div>
  `;

  messagesEl.appendChild(msgDiv);
  scrollToBottom();
}

/**
 * Formats message text: markdown-lite — bold, line breaks, bullet lists.
 */
function formatMessage(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')   // **bold**
    .replace(/\*(.*?)\*/g, '<em>$1</em>')                // *italic*
    .replace(/`(.*?)`/g, '<code>$1</code>')              // `code`
    .replace(/\n\n/g, '</p><p>')                         // double newlines
    .replace(/\n/g, '<br>')                              // single newlines
    .replace(/^/,  '<p>').replace(/$/, '</p>');          // wrap in paragraph
}

/**
 * Shows or hides the typing indicator.
 */
function showTyping(show) {
  const indicator = document.getElementById('typingIndicator');
  if (!indicator) return;
  if (show) {
    indicator.classList.remove('d-none');
    scrollToBottom();
  } else {
    indicator.classList.add('d-none');
  }
}

/**
 * Scrolls the chat messages container to the bottom.
 */
function scrollToBottom() {
  const messagesEl = document.getElementById('chatMessages');
  if (messagesEl) {
    requestAnimationFrame(() => {
      messagesEl.scrollTop = messagesEl.scrollHeight;
    });
  }
}

/**
 * Clears the chat history and reloads the welcome message.
 */
function clearChat() {
  if (!confirm('Clear conversation history?')) return;
  chatHistory = [];
  const messagesEl = document.getElementById('chatMessages');
  if (messagesEl) {
    messagesEl.innerHTML = `
      <div class="chat-message bot-message">
        <div class="message-avatar bot-avatar">
          <i class="bi bi-lightning-charge-fill"></i>
        </div>
        <div class="message-bubble bot-bubble">
          <p class="mb-0">Chat cleared! 🔄 Ask me anything about fitness, nutrition, or wellness. I'm here to help! 💪</p>
          <div class="message-time">${getCurrentTime()}</div>
        </div>
      </div>
    `;
  }
}

/**
 * Returns current time as HH:MM string.
 */
function getCurrentTime() {
  return new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true });
}

/**
 * Sleep helper for artificial delay.
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ── Auto-resize textarea ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const chatInput = document.getElementById('chatInput');
  if (chatInput) {
    chatInput.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    // Focus the input on page load
    chatInput.focus();
  }
  scrollToBottom();
});
