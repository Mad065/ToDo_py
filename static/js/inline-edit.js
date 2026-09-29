// ═══════════════════════════════════════════════════════════
// inline-edit.js — Edición inline de nombres de lista
// ═══════════════════════════════════════════════════════════

document.querySelectorAll('[data-inline-edit]').forEach(input => {
  input.addEventListener('blur', () => input.closest('form').submit());
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') input.closest('form').submit();
  });
});
