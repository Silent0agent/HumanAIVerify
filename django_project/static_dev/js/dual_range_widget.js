document.addEventListener('DOMContentLoaded', function() {
    const widgets = document.querySelectorAll('.js-dual-range-widget');

    widgets.forEach(function(widget) {
        const numberInput = widget.querySelector('input:not([type="range"])');
        const rangeInput = widget.querySelector('input[type="range"]');

        rangeInput.addEventListener('input', function() {
            numberInput.value = this.value;
        });

        numberInput.addEventListener('input', function() {
            rangeInput.value = this.value;
        });
    });
});