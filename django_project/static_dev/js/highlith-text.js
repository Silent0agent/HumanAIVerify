(function() {
    const container = document.getElementById('task-content-container');
    const hiddenField = document.getElementById('highlighted_content') || document.getElementById('id_content') || document.querySelector('input[name="content"], input[name="highlighted_content"]');
    if (!container || !hiddenField) {
        console.warn('highlight: missing container or hiddenField', {
            container,
            hiddenField
        });
        return;
    }
    const pop = document.createElement('button');
    pop.type = 'button';
    pop.className = 'haiv-popover';
    pop.setAttribute('aria-hidden', 'true');
    pop.innerHTML = '<span class="label">Выделить</span>';
    document.body.appendChild(pop);
    let showTimeout = null;

    function syncHidden() {
        hiddenField.value = container.innerHTML;
    }

    function unwrapHighlight(span) {
        const parent = span.parentNode;
        while (span.firstChild) parent.insertBefore(span.firstChild, span);
        parent.removeChild(span);
        if (parent.normalize) parent.normalize();
        syncHidden();
    }

    function rangeIsInsideContainer(range) {
        if (!range) return false;
        const start = range.startContainer;
        const end = range.endContainer;
        return (container.contains(start) || container.isSameNode(start)) && (container.contains(end) || container.isSameNode(end));
    }

    function wrapRange(range, cls = 'haiv-highlight') {
        if (!range || range.collapsed) return false;
        if (!rangeIsInsideContainer(range)) return false;
        const ancestor = range.commonAncestorContainer;
        if (ancestor && ancestor.nodeType === Node.ELEMENT_NODE && ancestor.classList && ancestor.classList.contains(cls)) {
            return false;
        }
        const span = document.createElement('span');
        span.className = cls;
        try {
            range.surroundContents(span);
        } catch (err) {
            try {
                const frag = range.extractContents();
                span.appendChild(frag);
                range.insertNode(span);
            } catch (err2) {
                return false;
            }
        }
        const sel = window.getSelection();
        if (sel) sel.removeAllRanges();
        syncHidden();
        return true;
    }

    function wrapCurrentSelection() {
        const sel = window.getSelection();
        if (!sel || sel.isCollapsed || !sel.rangeCount) return false;
        const r = sel.getRangeAt(0).cloneRange();
        return wrapRange(r);
    }

    function positionPopoverAtRect(rect) {
        if (!rect) return hidePopover();
        const padding = 8;
        const popRect = pop.getBoundingClientRect();
        let left = rect.left + rect.width / 2 - popRect.width / 2;
        let top = rect.top - popRect.height - padding;
        if (top < 6) top = rect.bottom + padding;
        const minLeft = 6;
        const maxLeft = document.documentElement.clientWidth - popRect.width - 6;
        left = Math.max(minLeft, Math.min(maxLeft, left));
        pop.style.left = (left + window.scrollX) + 'px';
        pop.style.top = (top + window.scrollY) + 'px';
    }

    function showPopoverForRange(range) {
        if (!range || range.collapsed) return hidePopover();
        const rects = range.getClientRects();
        if (!rects || rects.length === 0) return hidePopover();
        let rect = null;
        for (let i = 0; i < rects.length; i++)
            if (rects[i].width > 0 || rects[i].height > 0) {
                rect = rects[i];
                break;
            }
        if (!rect) rect = rects[0];
        pop.classList.add('show');
        positionPopoverAtRect(rect);
    }

    function hidePopover() {
        pop.classList.remove('show');
        pop.style.left = '-9999px';
        pop.style.top = '-9999px';
    }
    container.addEventListener('mouseup', function() {
        clearTimeout(showTimeout);
        showTimeout = setTimeout(() => {
            const sel = window.getSelection();
            if (!sel || sel.isCollapsed || !sel.rangeCount) {
                hidePopover();
                return;
            }
            const r = sel.getRangeAt(0);
            if (!rangeIsInsideContainer(r)) {
                hidePopover();
                return;
            }
            showPopoverForRange(r);
        }, 10);
    });
    document.addEventListener('keyup', function(e) {
        const active = document.activeElement;
        if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.isContentEditable)) return;
        const interesting = ['Shift', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End', 'PageUp', 'PageDown'];
        if (!interesting.includes(e.key)) return;
        setTimeout(() => {
            const sel = window.getSelection();
            if (!sel || sel.isCollapsed || !sel.rangeCount) {
                hidePopover();
                return;
            }
            const r = sel.getRangeAt(0);
            if (!rangeIsInsideContainer(r)) {
                hidePopover();
                return;
            }
            showPopoverForRange(r);
        }, 10);
    });
    document.addEventListener('selectionchange', function() {
        const sel = window.getSelection();
        if (!sel || sel.isCollapsed || !sel.rangeCount) {
            hidePopover();
            return;
        }
        const r = sel.getRangeAt(0);
        if (!rangeIsInsideContainer(r)) {
            hidePopover();
            return;
        }
        if (pop.classList.contains('show')) showPopoverForRange(r);
    });
    pop.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const success = wrapCurrentSelection();
        hidePopover();
        if (success) {
            pop.classList.add('flash');
            setTimeout(() => pop.classList.remove('flash'), 300);
        }
    });
    document.addEventListener('pointerdown', function(e) {
        const t = e.target;
        if (!t) return;
        if (t === pop || pop.contains(t)) return;
        if (container.contains(t)) return;
        hidePopover();
        const sel = window.getSelection();
        sel && sel.removeAllRanges();
    });
    container.addEventListener('click', function(e) {
        const t = e.target;
        if (t && t.nodeType === Node.ELEMENT_NODE && t.classList.contains('haiv-highlight')) {
            unwrapHighlight(t);
            e.preventDefault();
            e.stopPropagation();
            hidePopover();
        }
    });
    document.addEventListener('DOMContentLoaded', syncHidden);
    const form = container.closest('form') || document.querySelector('form');
    if (form) form.addEventListener('submit', syncHidden, {
        passive: true
    });
    container.addEventListener('focusout', function() {
        setTimeout(() => {
            const active = document.activeElement;
            if (!container.contains(active) && !pop.contains(active)) hidePopover();
        }, 10);
    });
})();