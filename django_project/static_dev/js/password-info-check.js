(function () {
  const passwordFieldNames = ['password1','new_password1'];

  const commonPasswords = new Set([
    '123456','password','12345678','qwerty','12345','123456789','111111','1234567','sunshine',
    'qwerty123','iloveyou','princess','admin','welcome','666666','abc123', 'qwerty12345'
  ]);

  const modal = document.getElementById('passwordInfoModal');
  if (!modal) return;

  const liSimilar = modal.querySelector('li[data-rule="similar"]');
  const liLength  = modal.querySelector('li[data-rule="length"]');
  const liCommon  = modal.querySelector('li[data-rule="common"]');
  const liNumeric = modal.querySelector('li[data-rule="numeric"]');

  function mark(li, ok) {
    if (!li) return;
    li.classList.remove('text-success','text-danger');
    li.classList.add(ok ? 'text-success' : 'text-danger');
  }

  function updateInfoButtons(allOk) {
  const color = allOk ? '#198754' : '#dc3545';
  document.querySelectorAll('.password-info').forEach(btn => {
    btn.classList.remove('text-success','text-danger');
    btn.classList.add(allOk ? 'text-success' : 'text-danger');

    const svgs = btn.querySelectorAll('svg');
    svgs.forEach(svg => {
      try {
        svg.setAttribute('fill', color);
        svg.style.fill = color;
        svg.querySelectorAll('*').forEach(el => {
          el.setAttribute('fill', color);
          el.style.fill = color;
        });
      } catch (e) {
        console.warn('SVG color change failed', e);
      }
    });
  });
}


  function getPersonalValues() {
    const usernameInput = document.querySelector('input[name*=username], input[id*=username], input[name=user], input[id=user]');
    const emailInput = document.querySelector('input[name*=email], input[id*=email]');
    return {
      username: usernameInput ? (usernameInput.value || '') : '',
      emailLocal: emailInput ? (emailInput.value.split('@')[0] || '') : ''
    };
  }

  function isTooSimilar(password, personal) {
    if (!password) return true;
    const pw = password.toLowerCase();
    const checks = [];
    if (personal.username) checks.push(personal.username.toLowerCase());
    if (personal.emailLocal) checks.push(personal.emailLocal.toLowerCase());
    for (const p of checks) {
      if (!p) continue;
      if (p.length >= 3 && pw.includes(p)) return true;
      if (p.length < 3 && pw === p) return true;
    }
    return false;
  }

  function validate(password) {
    const personal = getPersonalValues();
    const okSimilar = !isTooSimilar(password, personal);
    const okLength = (password && password.length >= 8);
    const okCommon = !(password && commonPasswords.has(password.toLowerCase()));
    const okNumeric = !(password && /^[0-9]+$/.test(password));

    mark(liSimilar, okSimilar);
    mark(liLength, okLength);
    mark(liCommon, okCommon);
    mark(liNumeric, okNumeric);

    const allOk = !!(okSimilar && okLength && okCommon && okNumeric);
    updateInfoButtons(allOk);

    return { okSimilar, okLength, okCommon, okNumeric, allOk };
  }

  function attachToField(input) {
    if (!input) return;
    input.addEventListener('input', function () {
      validate(input.value);
    });
    input.addEventListener('focus', function () {
      validate(input.value);
    });
  }

  (function initPasswordInfoState() {
    const active = document.activeElement;
    let seedInput = null;
    if (active && active.tagName === 'INPUT' && active.type === 'password') {
        seedInput = active;
    } else {
        seedInput = document.querySelector('input[type="password"]:not([disabled])');
    }
    const seedValue = seedInput ? (seedInput.value || '') : '';
    const result = validate(seedValue || '');
    updateInfoButtons(result.allOk);
    })();

  passwordFieldNames.forEach(name => {
    document.querySelectorAll(`input[name="${name}"]`).forEach(attachToField);
  });

  modal.addEventListener('shown.bs.modal', function () {
    const active = document.activeElement;
    if (active && active.tagName === 'INPUT' && active.type === 'password') {
      validate(active.value);
    } else {
      const firstPw = document.querySelector('input[type="password"]:not([disabled])');
      if (firstPw) validate(firstPw.value);
    }
  });

  document.querySelectorAll('input[type="password"]').forEach(function (input) {
    if (input.value) validate(input.value);
  });

})();
