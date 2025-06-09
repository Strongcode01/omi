// Warn before leaving unsaved form
window.addEventListener('beforeunload', e => {
    if (document.querySelector('textarea').value) {
      e.returnValue = 'You have unsaved changes. Continue?';
    }
  });