/* Theme is set before paint. Everything else enhances the static document. */
(() => {
  'use strict';
  const root = document.documentElement;
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let preference;
  try { preference = localStorage.getItem('theme'); } catch (_) { /* Storage may be blocked. */ }
  if (preference !== 'light' && preference !== 'dark') preference = null;
  const applyTheme = () => {
    const theme = preference || (systemTheme.matches ? 'dark' : 'light');
    root.dataset.theme = theme;
    const toggle = document.querySelector('.theme-toggle');
    if (toggle) {
      const label = `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`;
      toggle.setAttribute('aria-label', label);
      toggle.title = label;
    }
  };
  applyTheme();
  root.classList.add('js');
  systemTheme.addEventListener('change', applyTheme);
  window.addEventListener('storage', (event) => {
    if (event.key === 'theme' || event.key === null) {
      preference = event.newValue === 'light' || event.newValue === 'dark' ? event.newValue : null;
      applyTheme();
    }
  });

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href]').forEach((link) => {
      if (/^https?:$/.test(link.protocol) && link.origin !== window.location.origin) {
        link.target = '_blank';
        link.relList.add('external', 'nofollow', 'noopener');
      }
    });

    const themeToggle = document.querySelector('.theme-toggle');
    themeToggle.hidden = false;
    applyTheme();
    themeToggle.addEventListener('click', () => {
      preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('theme', preference); } catch (_) { /* Keep the in-page preference. */ }
      applyTheme();
    });

    const menuToggle = document.querySelector('.menu-toggle');
    const navigation = document.querySelector('#navigation');
    const mobile = window.matchMedia('(max-width: 576px)');
    const setMenu = (open) => {
      navigation.classList.toggle('is-open', open);
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.setAttribute('aria-label', `${open ? 'Close' : 'Open'} navigation`);
    };
    menuToggle.hidden = false;
    menuToggle.addEventListener('click', () => setMenu(menuToggle.getAttribute('aria-expanded') !== 'true'));
    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a') && mobile.matches) setMenu(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menuToggle.focus();
      }
    });
    mobile.addEventListener('change', () => setMenu(false));

    const progress = document.querySelector('.reading-progress span');
    let framePending = false;
    const updateProgress = () => {
      const distance = root.scrollHeight - window.innerHeight;
      const ratio = distance > 0 ? Math.min(1, Math.max(0, window.scrollY / distance)) : 0;
      progress.style.transform = `scaleX(${ratio})`;
      framePending = false;
    };
    const requestProgress = () => {
      if (!framePending) {
        framePending = true;
        window.requestAnimationFrame(updateProgress);
      }
    };
    document.querySelectorAll('.paper-bibtex').forEach((disclosure) => {
      const copy = disclosure.querySelector('.bibtex-copy');
      const text = disclosure.querySelector('.bibtex-text');
      const status = disclosure.querySelector('.bibtex-status');
      copy.hidden = false;
      copy.addEventListener('click', async () => {
        status.textContent = '';
        try {
          await navigator.clipboard.writeText(text.value);
          status.textContent = 'Copied.';
        } catch (_) {
          text.focus();
          text.select();
          status.textContent = 'Citation selected. Use your device’s copy command.';
        }
      });
      disclosure.addEventListener('toggle', () => {
        if (!disclosure.open) status.textContent = '';
        requestProgress();
      });
    });
    // Citation resizing and disclosure change the document's scrollable height.
    if ('ResizeObserver' in window) new ResizeObserver(requestProgress).observe(document.body);
    window.addEventListener('scroll', requestProgress, { passive: true });
    window.addEventListener('resize', requestProgress);
    window.addEventListener('load', requestProgress);
    if (document.fonts) document.fonts.ready.then(requestProgress);
    updateProgress();
  });
})();
