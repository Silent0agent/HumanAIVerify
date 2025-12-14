(function() {
    const header = document.querySelector('header.py-3.mb-4.border-bottom');
    if (!header) return;
    header.classList.add('site-header');

    const placeholder = document.createElement('div');
    placeholder.className = 'header-placeholder';
    header.parentNode.insertBefore(placeholder, header.nextSibling);

    let lastY = window.scrollY || 0;
    let ticking = false;
    let isFixed = false;

    function updatePlaceholder() {
        const h = header.offsetHeight;
        placeholder.style.height = isFixed ? h + 'px' : '0px';
    }

    function onScroll() {
        const currentY = window.scrollY || 0;
        const delta = currentY - lastY;

        if (!isFixed && currentY > 10) {
            header.classList.add('site-header--fixed');
            isFixed = true;
            updatePlaceholder();
        }
        if (isFixed && currentY <= 10) {
            header.classList.remove('site-header--fixed', 'site-header--hidden');
            isFixed = false;
            updatePlaceholder();
            lastY = currentY;
            return;
        }

        if (isFixed) {
            if (delta > 10) {
                header.classList.add('site-header--hidden');
            } else if (delta < -10) {
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
        if (window.scrollY > 10) {
            header.classList.add('site-header--fixed');
            isFixed = true;
            updatePlaceholder();
        }
    });
})();