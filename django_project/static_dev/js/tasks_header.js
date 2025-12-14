document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.getElementById('miniTabs');
    const indicatorWrap = document.getElementById('miniTabsIndicator');
    const createBtn = document.getElementById('createBtn');

    if (!tabs || !indicatorWrap) return;

    let bar = indicatorWrap.querySelector('div');
    if (!bar) {
        bar = document.createElement('div');
        indicatorWrap.appendChild(bar);
    }

    function normalizePath(p) {
        if (!p) return p;
        const url = new URL(p, location.origin);
        let path = url.pathname;
        if (path.length > 1 && path.endsWith('/')) path = path.slice(0, -1);
        return path;
    }

    function getActiveLink() {
        // 1) серверная подсветка
        const byServer = tabs.querySelector('.nav-link.purple');
        if (byServer) return byServer;

        const cur = normalizePath(location.pathname);
        const links = Array.from(tabs.querySelectorAll('.nav-link[href]'));
        for (const a of links) {
            const href = a.getAttribute('href');
            if (!href) continue;
            const norm = normalizePath(href);
            if (norm === cur) return a;
        }

        return tabs.querySelector('.nav-link');
    }

    function updateIndicator() {
        const link = getActiveLink();
        if (!link) { bar.style.opacity = '0'; return; }

        const linkRect = link.getBoundingClientRect();
        const wrapRect = tabs.getBoundingClientRect();

        const left = linkRect.left - wrapRect.left;
        const width = Math.max(8, linkRect.width);

        bar.style.width = width + 'px';
        bar.style.transform = `translateX(${left}px)`;
        bar.style.opacity = '1';
    }

    function updateCreateHref() {
        if (!createBtn) return;
        const link = getActiveLink();
        const url = link && link.dataset ? link.dataset.createUrl : null;
        if (url) createBtn.setAttribute('href', url);
        else createBtn.setAttribute('href', '#');
    }

    tabs.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            tabs.querySelectorAll('.nav-link').forEach(l => l.classList.remove('purple'));
            this.classList.add('purple');

            updateIndicator();
            updateCreateHref();
        });
    });

    window.addEventListener('resize', updateIndicator);
    window.addEventListener('orientationchange', updateIndicator);

    setTimeout(() => {
        updateIndicator();
        updateCreateHref();
    }, 40);
});