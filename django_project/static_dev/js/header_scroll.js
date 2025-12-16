(function() {
    const header = document.querySelector('header.site-header');
    if (!header) return;
    const placeholder = document.createElement('div');
    placeholder.className = 'header-placeholder';
    header.parentNode.insertBefore(placeholder, header.nextSibling);

    let lastY = window.scrollY || 0;
    let ticking = false;
    let isFixed = false;
    let offcanvasOpen = false;

    const FIX_THRESHOLD = 10;
    const HIDE_THRESHOLD = 25;
    const SHOW_THRESHOLD = -25;

    function updatePlaceholder() {
        const h = header.offsetHeight;
        placeholder.style.transition = 'none';
        placeholder.style.height = isFixed ? h + 'px' : '0px';
        requestAnimationFrame(() => {
            placeholder.style.transition = '';
        });
    }

    function onScroll() {
        if (offcanvasOpen) {
            lastY = window.scrollY || 0;
            return;
        }
        const currentY = window.scrollY || 0;
        const delta = currentY - lastY;

        if (!isFixed && currentY > FIX_THRESHOLD) {
            header.classList.add('site-header--fixed');
            isFixed = true;
            updatePlaceholder();
        }

        if (isFixed && currentY <= FIX_THRESHOLD) {
            header.classList.remove('site-header--fixed', 'site-header--hidden');
            isFixed = false;
            updatePlaceholder();
            lastY = currentY;
            return;
        }

        if (isFixed) {
            if (delta > HIDE_THRESHOLD) {
                header.classList.add('site-header--hidden');
            } else if (delta < SHOW_THRESHOLD) {
                header.classList.remove('site-header--hidden');
            }
        }

        lastY = currentY;
    }

    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                onScroll();
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });

    window.addEventListener('resize', updatePlaceholder);
    document.addEventListener('DOMContentLoaded', function() {
        updatePlaceholder();
        if (window.scrollY > FIX_THRESHOLD) {
            header.classList.add('site-header--fixed');
            isFixed = true;
            updatePlaceholder();
        }

        const offcanvasEl = document.getElementById('headerOffcanvas');
        if (offcanvasEl) {
            offcanvasEl.addEventListener('show.bs.offcanvas', function() {
                offcanvasOpen = true;
                header.classList.remove('site-header--hidden');
                updatePlaceholder();
            });
            offcanvasEl.addEventListener('hidden.bs.offcanvas', function() {
                offcanvasOpen = false;
                updatePlaceholder();
            });
        }
    });
})();