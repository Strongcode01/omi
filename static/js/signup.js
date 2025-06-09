// Signup form enhancements: e.g., real-time password strength meter
const pwd1 = document.querySelector('#id_password1');
const meter = document.createElement('div');
meter.id = 'pwd-meter';
pwd1.parentNode.insertBefore(meter, pwd1.nextSibling);
pwd1.addEventListener('input', () => {
  const strength = pwd1.value.length;
  meter.textContent = `Length: ${strength}`;
});