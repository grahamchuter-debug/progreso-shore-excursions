/**
 * Progressive enhancement for inlined static pages.
 * Mobile nav: native button, aria-expanded, Escape close.
 */
(function () {
  function setActiveNav() {
    const page = document.body.dataset.page;
    if (!page) return;
    document.querySelectorAll('[data-nav]').forEach(function (link) {
      const isActive = link.dataset.nav === page;
      link.classList.toggle('text-ocean-600', isActive);
      link.classList.toggle('font-semibold', isActive);
      link.classList.toggle('text-gray-600', !isActive);
      if (isActive) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  }

  function wireMobileNav() {
    const nav = document.querySelector('#site-nav nav');
    if (!nav) return;
    const btn = nav.querySelector('#mobile-nav-toggle, button[aria-controls="mobile-nav-panel"]');
    const panel = nav.querySelector('#mobile-nav-panel, [data-mobile-panel]');
    if (!btn || !panel) return;
    if (btn.dataset.wired === 'true') return;
    btn.dataset.wired = 'true';

    function setOpen(open) {
      panel.classList.toggle('hidden', !open);
      if (open) panel.removeAttribute('hidden');
      else panel.setAttribute('hidden', '');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }

    setOpen(false);

    btn.addEventListener('click', function () {
      const open = panel.classList.contains('hidden');
      setOpen(open);
    });

    panel.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        setOpen(false);
      });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    setActiveNav();
    wireMobileNav();
  });
})();
