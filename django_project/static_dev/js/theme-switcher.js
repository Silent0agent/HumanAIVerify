document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('themeDropdown');
    if (!toggleBtn) return;

    const labelSpan = toggleBtn.querySelector('span.d-none.d-sm-inline') || toggleBtn.querySelector('span');
    const iconImg = toggleBtn.querySelector('img');

    function getMenuLabel(theme) {
        const btn = document.querySelector('[data-bs-theme-value="' + theme + '"]');
        if (!btn) return theme.charAt(0).toUpperCase() + theme.slice(1);

        let text = '';
        btn.childNodes.forEach(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                const t = node.textContent.trim();
                if (t) text = t;
            }
        });
        if (!text) {
            text = btn.innerText.replace('✔', '').trim();
        }
        return text;
    }

    function getMenuIconSrc(theme) {
        const btn = document.querySelector('[data-bs-theme-value="' + theme + '"]');
        if (!btn) return null;
        const img = btn.querySelector('img, svg');
        if (!img) return null;
        if (img.tagName.toLowerCase() === 'img') return img.src;
        return null;
    }

    function updateToggle(theme) {
        const final = theme || 'auto';
        if (labelSpan) labelSpan.textContent = getMenuLabel(final);
        const iconSrc = getMenuIconSrc(final);
        if (iconSrc && iconImg) iconImg.src = iconSrc;
    }

    const saved = localStorage.getItem('theme') || 'auto';
    updateToggle(saved);

    document.querySelectorAll('[data-bs-theme-value]').forEach(btn => {
        btn.addEventListener('click', function() {
            const v = this.getAttribute('data-bs-theme-value') || 'auto';
            updateToggle(v);
        });
    });
});