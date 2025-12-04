document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('themeDropdown');
  if (!toggleBtn) return;

  const labelSpan = toggleBtn.querySelector('span.d-none.d-sm-inline') || toggleBtn.querySelector('span');
  const iconImg = toggleBtn.querySelector('img');

  function getMenuLabel(theme) {
    const btn = document.querySelector('[data-bs-theme-value="' + theme + '"]');
    if (!btn) return theme.charAt(0).toUpperCase() + theme.slice(1);

    // try to find a text node inside the button (excluding hidden check marks)
    let text = '';
    btn.childNodes.forEach(node => {
      if (node.nodeType === Node.TEXT_NODE) {
        const t = node.textContent.trim();
        if (t) text = t;
      }
    });
    if (!text) {
      // fallback: use innerText and remove check sign if any
      text = btn.innerText.replace('✔', '').trim();
    }
    return text;
  }

  function getMenuIconSrc(theme) {
    const btn = document.querySelector('[data-bs-theme-value="' + theme + '"]');
    if (!btn) return null;
    const img = btn.querySelector('img, svg');
    if (!img) return null;
    // if <img>, return src; if svg sprite/inline, try to reuse src of <img> or do nothing
    if (img.tagName.toLowerCase() === 'img') return img.src;
    return null;
  }

  function updateToggle(theme) {
    const final = theme || 'auto';
    // label
    if (labelSpan) labelSpan.textContent = getMenuLabel(final);
    // icon
    const iconSrc = getMenuIconSrc(final);
    if (iconSrc && iconImg) iconImg.src = iconSrc;
  }

  // init from localStorage (use same key your theme code uses)
  const saved = localStorage.getItem('theme') || 'auto';
  updateToggle(saved);

  // update when user clicks a menu item
  document.querySelectorAll('[data-bs-theme-value]').forEach(btn => {
    btn.addEventListener('click', function () {
      const v = this.getAttribute('data-bs-theme-value') || 'auto';
      // some other script might set localStorage; we update toggle from v to reflect immediate choice
      updateToggle(v);
    });
  });
});
