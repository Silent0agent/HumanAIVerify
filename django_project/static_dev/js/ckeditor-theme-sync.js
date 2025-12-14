(function() {
    function getSavedTheme() {
        return localStorage.getItem('theme') || 'auto';
    }

    function resolveEffectiveTheme(theme) {
        if (theme === 'auto') {
            return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        return theme;
    }

    function applyThemeToEditorContainers(theme) {
        const effective = resolveEffectiveTheme(theme);
        document.documentElement.setAttribute('data-theme', effective);

        document.querySelectorAll('.ck-editor').forEach(container => {
            container.classList.toggle('ck-theme-dark', effective === 'dark');
            container.classList.toggle('ck-theme-light', effective === 'light');
        });
    }

    window.addEventListener('theme:changed', function(e) {
        const theme = e && e.detail && e.detail.theme ? e.detail.theme : getSavedTheme();
        applyThemeToEditorContainers(theme);
    });

    document.addEventListener('DOMContentLoaded', function() {
        applyThemeToEditorContainers(getSavedTheme());
    });

    const obs = new MutationObserver(function() {
        applyThemeToEditorContainers(getSavedTheme());
    });

    obs.observe(document.body, { childList: true, subtree: true });

    window._applyCkeditorTheme = applyThemeToEditorContainers;
})();