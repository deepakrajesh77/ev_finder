document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('navToggle');
  const nav = document.querySelector('.main-nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', function () {
    nav.classList.toggle('open');
    toggle.textContent = nav.classList.contains('open') ? '✕' : '☰';
  });

  // Close the menu automatically if the viewport is resized back to desktop width
  window.addEventListener('resize', function () {
    if (window.innerWidth > 960 && nav.classList.contains('open')) {
      nav.classList.remove('open');
      toggle.textContent = '☰';
    }
  });

  // Close the menu after tapping a link (better mobile UX)
  nav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      nav.classList.remove('open');
      toggle.textContent = '☰';
    });
  });
});
