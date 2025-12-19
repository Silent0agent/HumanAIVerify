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

    function getMenuIconHTML(theme) {
        const btn = document.querySelector('[data-bs-theme-value="' + theme + '"]');
        if (!btn) return null;
        const svg = btn.querySelector('svg');
        if (!svg) return null;
        return svg.innerHTML;
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
        const iconHTML = getMenuIconHTML(final);
        const toggles = findToggles();

        toggles.forEach(toggleBtn => {
            let iconSvg = toggleBtn.querySelector('svg');
            let labelSpan = toggleBtn.querySelector('span');

            if (!iconSvg && iconHTML) {
                iconSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                iconSvg.setAttribute('class', 'bi me-2');
                iconSvg.setAttribute('width', '18');
                iconSvg.setAttribute('height', '18');
                iconSvg.setAttribute('fill', 'currentColor');
                iconSvg.setAttribute('viewBox', '0 0 16 16');
                toggleBtn.insertBefore(iconSvg, toggleBtn.firstChild);
            }

            if (!labelSpan) {
                labelSpan = document.createElement('span');
                toggleBtn.appendChild(labelSpan);
            }

            if (labelSpan) labelSpan.textContent = label;

            if (iconHTML && iconSvg) {
                iconSvg.innerHTML = iconHTML;
            }

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
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    const initTheme = detectInitialTheme();
    updateAllToggles(initTheme);
    if (initTheme !== 'auto') {
        document.documentElement.setAttribute('data-bs-theme', initTheme);
    }

    document.querySelectorAll('[data-bs-theme-value]').forEach(btn => {
        btn.addEventListener('click', function() {
            const v = this.getAttribute('data-bs-theme-value') || 'auto';
            try { localStorage.setItem('theme', v); } catch (e) {}

            if (v === 'auto') {
                const sysDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                document.documentElement.setAttribute('data-bs-theme', sysDark ? 'dark' : 'light');
            } else {
                document.documentElement.setAttribute('data-bs-theme', v);
            }
            
            updateAllToggles(v);
        });
    });


    window.addEventListener('storage', function(e) {
        if (e.key === 'theme') {
            const newTheme = e.newValue || 'auto';
            updateAllToggles(newTheme);
            if (newTheme === 'auto') {
                 const sysDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                 document.documentElement.setAttribute('data-bs-theme', sysDark ? 'dark' : 'light');
            } else {
                 document.documentElement.setAttribute('data-bs-theme', newTheme);
            }
        }
    });
});