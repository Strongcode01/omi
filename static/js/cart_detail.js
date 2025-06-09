// Confirm removal
document.querySelectorAll('a[href*="remove"]').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm('Remove this item from cart?')) e.preventDefault();
    });
  });