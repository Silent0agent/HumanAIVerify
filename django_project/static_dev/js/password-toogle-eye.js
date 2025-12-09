document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.password-eye').forEach(btn => {
    btn.addEventListener('click', function () {
      const input = wrapper.querySelector('input');
      const iconShow = btn.querySelector('.icon-show');
      const iconHide = btn.querySelector('.icon-hide');

      if (!input || !iconShow || !iconHide) return;

      if (input.type === 'password') {
        input.type = 'text';
        iconShow.classList.add('d-none');
        iconHide.classList.remove('d-none');
      } else {
        input.type = 'password';
        iconShow.classList.remove('d-none');
        iconHide.classList.add('d-none');
      }
    });
  });
});