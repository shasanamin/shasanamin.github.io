/* Click the gold for another line. No navigation, storage, or extra controls. */
(() => {
  'use strict';
  const pocket = document.querySelector('[data-nuggets]');
  if (!pocket) return;
  let nuggets;
  try { nuggets = JSON.parse(pocket.querySelector('#nugget-data').textContent); }
  catch (_) { return; } // The native disclosure remains usable.
  if (!Array.isArray(nuggets) || !nuggets.length) return;

  const discovery = pocket.querySelector('details');
  const trigger = pocket.querySelector('summary');
  const quote = pocket.querySelector('.nugget-quote');
  const seen = new Set();
  let current;
  let fontRequested = false;

  trigger.addEventListener('click', event => {
    event.preventDefault();
    let choices = nuggets.filter(item => !seen.has(item.id));
    if (!choices.length) {
      seen.clear();
      choices = nuggets.filter(item => item.id !== current?.id);
    }
    current = choices[Math.floor(Math.random() * choices.length)] || nuggets[0];
    seen.add(current.id);
    quote.textContent = current.text;
    quote.lang = current.lang;
    quote.dir = current.dir || 'auto';
    quote.dataset.nuggetId = current.id;
    discovery.open = true;
    trigger.setAttribute('aria-label', 'Discover another gold nugget');

    if (current.lang === 'ur' && !fontRequested) {
      fontRequested = true;
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400&display=swap';
      document.head.append(link);
    }
  });
})();
