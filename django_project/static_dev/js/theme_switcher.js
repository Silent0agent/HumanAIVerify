document.addEventListener('DOMContentLoaded', function() {
    const toggleSelectors = ['#themeDropdown', '.theme-dropdown'];

    function findToggles() {
        const set = new Set();
        toggleSelectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => set.add(el));
        });
        return Array.from(set);
    }

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
        if (!text) text = btn.innerText.replace('✔', '').trim();
        return text;
    }

    function getMenuIconSrc(theme) {
        const btn = document.querySelector('[data-bs-theme-value="' + theme + '"]');
        if (!btn) return null;
        const img = btn.querySelector('img');
        if (!img) return null;
        return img.src;
    }

    function markMenuSelected(theme) {
        document.querySelectorAll('[data-bs-theme-value]').forEach(btn => {
            const v = btn.getAttribute('data-bs-theme-value') || 'auto';
            const pressed = v === theme;
            btn.setAttribute('aria-pressed', pressed ? 'true' : 'false');
            const check = btn.querySelector('.check');
            if (check) {
                if (pressed) check.classList.remove('d-none');
                else check.classList.add('d-none');
            }
        });
    }

    function updateAllToggles(theme) {
        const final = theme || 'auto';
        const label = getMenuLabel(final);
        const iconSrc = getMenuIconSrc(final);
        const toggles = findToggles();
        toggles.forEach(toggleBtn => {
            let iconImg = toggleBtn.querySelector('img');
            let labelSpan = toggleBtn.querySelector('span');
            if (!iconImg) {
                iconImg = document.createElement('img');
                iconImg.width = 18;
                iconImg.height = 18;
                iconImg.className = 'me-2';
                toggleBtn.insertBefore(iconImg, toggleBtn.firstChild);
            }
            if (!labelSpan) {
                labelSpan = document.createElement('span');
                toggleBtn.appendChild(labelSpan);
            }
            if (labelSpan) labelSpan.textContent = label;
            if (iconSrc && iconImg) iconImg.src = iconSrc;
            toggleBtn.setAttribute('aria-label', label);
        });
        markMenuSelected(final);
    }

    function detectInitialTheme() {
        try {
            const ls = localStorage.getItem('theme');
            if (ls) return ls;
        } catch (e) {}
        const docTheme = document.documentElement.getAttribute('data-bs-theme');
        if (docTheme) return docTheme;
        const pressedEl = document.querySelector('[data-bs-theme-value][aria-pressed="true"]');
        if (pressedEl) return pressedEl.getAttribute('data-bs-theme-value') || 'auto';
        return 'auto';
    }

    // Инициализация
    updateAllToggles(detectInitialTheme());

    // Обработчики меню (один набор меню в DOM; достаточно слушать клики по ним)
    document.querySelectorAll('[data-bs-theme-value]').forEach(btn => {
        btn.addEventListener('click', function() {
            const v = this.getAttribute('data-bs-theme-value') || 'auto';
            try { localStorage.setItem('theme', v); } catch (e) {}
            updateAllToggles(v);
            setTimeout(() => location.reload(), 100);
        });
    });

    window.addEventListener('storage', function(e) {
        if (e.key === 'theme') updateAllToggles(e.newValue || 'auto');
    });

    const mo = new MutationObserver(records => {
        records.forEach(r => {
            if (r.attributeName === 'data-bs-theme') {
                const v = document.documentElement.getAttribute('data-bs-theme') || 'auto';
                updateAllToggles(v);
            }
        });
    });
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['data-bs-theme'] });
});