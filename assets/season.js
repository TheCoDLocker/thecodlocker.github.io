/* CODLOCKER v40: season switch (MW4 by default, 2026 Black Ops 7 archive on request). */
(() => {
  'use strict';
  const root = document.documentElement;
  const tabs = [...document.querySelectorAll('[data-season-tab]')];
  const panels = [...document.querySelectorAll('[data-season-panel]')];
  if (!tabs.length && !panels.length) return;

  function current() { return root.getAttribute('data-season') === 'bo7' ? 'bo7' : 'mw4'; }

  function writeUrl(season) {
    try {
      const url = new URL(location.href);
      if (season === 'bo7') url.searchParams.set('season', 'bo7');
      else url.searchParams.delete('season');
      if (url.hash === '#archive' && season === 'mw4') url.hash = '';
      history.replaceState(null, '', url);
    } catch (_) { /* file:// previews may block history updates */ }
  }

  function apply(season, opts = {}) {
    root.classList.add('sj');
    root.setAttribute('data-season', season);
    tabs.forEach(t => {
      const on = t.dataset.seasonTab === season;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
    });
    if (opts.url !== false) writeUrl(season);
    document.dispatchEvent(new CustomEvent('locker:season', {detail: {season}}));
    spy();
  }

  tabs.forEach(t => {
    t.addEventListener('click', () => apply(t.dataset.seasonTab));
    t.addEventListener('keydown', e => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      const next = tabs[(tabs.indexOf(t) + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length];
      apply(next.dataset.seasonTab); next.focus();
    });
  });

  // Links that jump into the other season (TOC footer, "2026 archive" mentions).
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-season-jump]');
    if (!a) return;
    e.preventDefault();
    apply(a.dataset.seasonJump);
    const id = (a.getAttribute('href') || '').replace(/^#/, '');
    const target = id === 'archive' ? document.getElementById('season-bo7') : document.getElementById(id);
    if (target) target.scrollIntoView({block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
  });

  // A hash that points inside the archive (old links to #graphics, #faq) opens the archive.
  function fromHash() {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return null;
    if (id === 'archive') return 'bo7';
    const el = document.getElementById(id);
    const panel = el && el.closest('[data-season-panel]');
    return panel ? panel.dataset.seasonPanel : null;
  }
  window.addEventListener('hashchange', () => {
    const s = fromHash();
    if (s && s !== current()) {
      apply(s, {url: false});
      const el = document.getElementById(location.hash.slice(1));
      if (el) el.scrollIntoView({block: 'start'});
    }
  });

  // Section highlighter for the profile rail, counting only visible sections.
  const toc = [...document.querySelectorAll('.player-toc a[data-section]')];
  function spy() {
    if (!toc.length) return;
    const links = toc.filter(a => a.offsetParent !== null);
    const sections = links.map(a => document.getElementById(a.dataset.section)).filter(el => el && el.offsetParent !== null);
    if (!sections.length) return;
    const marker = window.scrollY + Math.min(180, window.innerHeight * .26);
    let id = sections[0].id;
    sections.forEach(sec => { if (sec.getBoundingClientRect().top + window.scrollY <= marker) id = sec.id; });
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 6) id = sections[sections.length - 1].id;
    toc.forEach(a => a.classList.toggle('active', a.dataset.section === id));
  }
  if (toc.length) {
    toc.forEach(a => a.addEventListener('click', () => toc.forEach(x => x.classList.toggle('active', x === a))));
    let queued = false;
    const onScroll = () => { if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; spy(); }); } };
    window.addEventListener('scroll', onScroll, {passive: true});
    window.addEventListener('resize', onScroll, {passive: true});
    window.addEventListener('load', spy);
  }

  const start = fromHash() || current();
  apply(start, {url: false});
  if (start === 'bo7' && location.hash && location.hash !== '#archive') {
    const el = document.getElementById(location.hash.slice(1));
    if (el) requestAnimationFrame(() => el.scrollIntoView({block: 'start'}));
  }
})();

/* Classes page: filter the build list by gun or by player. Without JS every card stays visible. */
(() => {
  'use strict';
  const rail = document.querySelector('[data-class-filter]');
  if (!rail) return;
  const links = [...rail.querySelectorAll('[data-cf]')];
  const gunCards = [...document.querySelectorAll('.gun-card[data-cf]')];
  const cards = [...document.querySelectorAll('[data-class-card]')];
  const count = document.getElementById('classCount');
  const list = document.getElementById('all-classes');
  const label = {};
  links.forEach(a => { const b = a.querySelector('b'); label[a.dataset.cf] = b ? b.textContent : a.dataset.cf; });
  const smooth = () => matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';

  function run(key, push) {
    const parts = key === 'all' ? ['all'] : key.split(':');
    const kind = parts[0], value = parts[1];
    let shown = 0;
    cards.forEach(c => {
      const on = kind === 'all' || c.dataset[kind] === value;
      c.hidden = !on;
      if (on) shown++;
    });
    links.forEach(a => {
      const on = a.dataset.cf === key;
      a.classList.toggle('active', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
    gunCards.forEach(g => g.classList.toggle('active', g.dataset.cf === key));
    if (count) {
      count.textContent = kind === 'all'
        ? `Showing all ${cards.length} classes.`
        : `Showing ${shown} of ${cards.length} classes: ${label[key] || value}.`;
    }
    if (push) {
      try { history.replaceState(null, '', kind === 'all' ? location.pathname + location.search : `${location.pathname}${location.search}#${kind}-${value}`); } catch (_) { /* file:// */ }
    }
  }

  [...links, ...gunCards].forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    run(a.dataset.cf, true);
    if (list && (a.classList.contains('gun-card') || list.getBoundingClientRect().top < 0)) list.scrollIntoView({block: 'start', behavior: smooth()});
  }));

  function fromHash(scroll) {
    const m = /^#(gun|player)-([a-z0-9-]+)$/.exec(location.hash || '');
    if (m && links.some(a => a.dataset.cf === `${m[1]}:${m[2]}`)) {
      run(`${m[1]}:${m[2]}`, false);
      if (scroll && list) requestAnimationFrame(() => list.scrollIntoView({block: 'start'}));
      return;
    }
    // a link straight to one card: make sure the card is not filtered out
    const card = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (card && card.hasAttribute('data-class-card') && card.hidden) {
      run('all', false);
      requestAnimationFrame(() => card.scrollIntoView({block: 'start'}));
    }
  }
  window.addEventListener('hashchange', () => fromHash(true));
  fromHash(true);
})();
