// ═══════════════════════════════════════════════════════════
// app.js — Lógica compartida entre páginas
// ═══════════════════════════════════════════════════════════

// ── Modal de nueva tarea ──
const fab = document.getElementById('fab');
const overlay = document.getElementById('modal-overlay');
const cancelBtn = document.getElementById('modal-cancel');

if (fab && overlay) {
  fab.addEventListener('click', () => overlay.classList.add('open'));
}
if (cancelBtn && overlay) {
  cancelBtn.addEventListener('click', () => overlay.classList.remove('open'));
}
if (overlay) {
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.classList.remove('open');
  });
}

// ── Modal de configuración ──
const settingsBtn = document.getElementById('settings-btn');
const settingsOverlay = document.getElementById('settings-overlay');
const settingsClose = document.getElementById('settings-close');

if (settingsBtn && settingsOverlay) {
  settingsBtn.addEventListener('click', () => settingsOverlay.classList.add('open'));
}
if (settingsClose && settingsOverlay) {
  settingsClose.addEventListener('click', () => settingsOverlay.classList.remove('open'));
}
if (settingsOverlay) {
  settingsOverlay.addEventListener('click', (e) => {
    if (e.target === settingsOverlay) settingsOverlay.classList.remove('open');
  });
}

// ── Tecla Escape cierra todos los modales ──
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (overlay) overlay.classList.remove('open');
    if (settingsOverlay) settingsOverlay.classList.remove('open');
  }
});

// ── Temas de fondo ──
const themeGradients = {
  purple: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
  ocean: 'linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)',
  sunset: 'linear-gradient(135deg, #f12711 0%, #f5af19 100%)',
  forest: 'linear-gradient(135deg, #134e5e 0%, #71b280 100%)',
  midnight: 'linear-gradient(135deg, #232526 0%, #414345 100%)',
  candy: 'linear-gradient(135deg, #fc5c7d 0%, #6a82fb 100%)',
};

const swatches = document.querySelectorAll('.swatch');
const customColorsDiv = document.getElementById('custom-colors');
const colorInputs = [
  document.getElementById('color-1'),
  document.getElementById('color-2'),
  document.getElementById('color-3'),
];
const savedTheme = localStorage.getItem('todo-theme') || 'purple';
const savedCustomColors = JSON.parse(localStorage.getItem('todo-custom-colors') || '["#667eea","#764ba2","#f093fb"]');

function applyTheme(theme) {
  if (theme === 'custom') {
    const c = savedCustomColors;
    document.body.style.background = `linear-gradient(135deg, ${c[0]} 0%, ${c[1]} 50%, ${c[2]} 100%)`;
    if (customColorsDiv) customColorsDiv.style.display = 'block';
  } else {
    document.body.style.background = themeGradients[theme];
    if (customColorsDiv) customColorsDiv.style.display = 'none';
  }
  swatches.forEach(s => s.classList.toggle('active', s.dataset.theme === theme));
  localStorage.setItem('todo-theme', theme);
}

function applyCustomColors() {
  const c = colorInputs.map(i => i.value);
  savedCustomColors.splice(0, 3, ...c);
  localStorage.setItem('todo-custom-colors', JSON.stringify(c));
  if (localStorage.getItem('todo-theme') === 'custom') {
    document.body.style.background = `linear-gradient(135deg, ${c[0]} 0%, ${c[1]} 50%, ${c[2]} 100%)`;
  }
}

swatches.forEach(s => {
  s.addEventListener('click', () => applyTheme(s.dataset.theme));
});

colorInputs.forEach((input, i) => {
  if (input) {
    input.addEventListener('input', applyCustomColors);
    input.value = savedCustomColors[i];
  }
});

applyTheme(savedTheme);

// ── Blur slider ──
const blurSlider = document.getElementById('blur-slider');
const blurValue = document.getElementById('blur-value');
const savedBlur = localStorage.getItem('todo-blur') || 20;

function applyBlur(val) {
  document.documentElement.style.setProperty('--blur-amount', val + 'px');
  if (blurValue) blurValue.textContent = val + 'px';
  localStorage.setItem('todo-blur', val);
}

if (blurSlider) {
  blurSlider.addEventListener('input', () => applyBlur(blurSlider.value));
}
applyBlur(savedBlur);

// ── Toggle animaciones ──
const animToggle = document.getElementById('animations-toggle');
const savedAnim = localStorage.getItem('todo-animations') !== 'off';

function applyAnimations(enabled) {
  document.documentElement.classList.toggle('no-animations', !enabled);
  if (animToggle) animToggle.checked = enabled;
  localStorage.setItem('todo-animations', enabled ? 'on' : 'off');
}

if (animToggle) {
  animToggle.addEventListener('change', () => applyAnimations(animToggle.checked));
}
applyAnimations(savedAnim);
