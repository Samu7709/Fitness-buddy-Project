/**
 * ============================================================
 *  FITNESS BUDDY AI — Main JavaScript
 *  Handles: Dark Mode, Auto-resize textarea, Utils
 * ============================================================
 */

// ── Dark Mode ─────────────────────────────────────────────────────────────────
(function initTheme() {
  const saved = localStorage.getItem('fb_theme') || 'light';
  applyTheme(saved, false);
})();

function applyTheme(theme, save = true) {
  document.documentElement.setAttribute('data-theme', theme);
  const icon = document.getElementById('themeIcon');
  if (icon) {
    icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
  }
  if (save) localStorage.setItem('fb_theme', theme);
}

document.addEventListener('DOMContentLoaded', function () {

  // Theme toggle button
  const toggleBtn = document.getElementById('themeToggle');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme');
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  // Auto-resize chat textarea
  const chatInput = document.getElementById('chatInput');
  if (chatInput) {
    chatInput.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
  }

  // Animate on scroll — add 'visible' class when element enters viewport
  const observer = new IntersectionObserver(
    (entries) => entries.forEach(e => {
      if (e.isIntersecting) e.target.classList.add('visible');
    }),
    { threshold: 0.1 }
  );
  document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

  // Tooltip init (Bootstrap)
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el =>
    new bootstrap.Tooltip(el, { trigger: 'hover' })
  );

  // Add `enumerate` filter emulation for Jinja usage verification
  // (no-op in JS, just for reference)

  console.log('💪 Fitness Buddy AI — Loaded & Ready!');
});

// ── Utility: format numbers with commas ──────────────────────────────────────
function fmtNum(n) {
  return Number(n).toLocaleString('en-IN');
}

// ── Utility: debounce ─────────────────────────────────────────────────────────
function debounce(fn, delay) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), delay); };
}

// ── Utility: show toast notification ─────────────────────────────────────────
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = 'position:fixed;top:80px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:8px;';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  const colors = { success: '#16a34a', error: '#dc2626', warning: '#d97706', info: '#0891b2' };
  toast.style.cssText = `
    background:${colors[type] || '#4f46e5'};color:white;
    padding:12px 20px;border-radius:10px;font-size:.9rem;font-weight:500;
    box-shadow:0 4px 16px rgba(0,0,0,.2);
    animation:slideIn .3s ease;max-width:320px;
  `;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => { toast.style.animation = 'slideOut .3s ease forwards'; setTimeout(() => toast.remove(), 300); }, 3000);
}

// ── Add CSS for toast animations ──────────────────────────────────────────────
const toastStyle = document.createElement('style');
toastStyle.textContent = `
  @keyframes slideIn { from { transform: translateX(100%); opacity:0; } to { transform: translateX(0); opacity:1; } }
  @keyframes slideOut { from { transform: translateX(0); opacity:1; } to { transform: translateX(100%); opacity:0; } }
`;
document.head.appendChild(toastStyle);
