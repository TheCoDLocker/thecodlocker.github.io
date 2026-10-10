/* CODLOCKER v29. Progressive enhancements; static pages remain directly usable. */
(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const players = window.CODLOCKER_PLAYERS || [];
  const bySlug = new Map(players.map(p => [p.slug, p]));
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let toastTimer;
  function toast(message) {
    const box = $('.locker-toast');
    if (!box) return;
    clearTimeout(toastTimer);
    box.textContent = message;
    box.hidden = false;
    toastTimer = setTimeout(() => { box.hidden = true; }, 3600);
  }
  async function copy(text, message) {
    let copied = false;
    if (navigator.clipboard && window.isSecureContext) {
      try { await navigator.clipboard.writeText(text); copied = true; } catch (_) { /* Try the local-file compatible fallback. */ }
    }
    if (!copied) {
      const oldFocus = document.activeElement;
      const input = document.createElement('textarea');
      input.value = text;
      input.setAttribute('aria-label', 'Text to copy');
      input.style.cssText = 'position:fixed;left:0;top:0;width:1px;height:1px;opacity:0';
      document.body.appendChild(input);
      input.focus(); input.select();
      try { copied = document.execCommand('copy'); } catch (_) { copied = false; }
      input.remove();
      if (oldFocus && oldFocus.focus) oldFocus.focus({preventScroll:true});
    }
    toast(copied ? message : 'Copy was blocked by your browser. Please select and copy the values directly.');
  }
  // Compact, keyboard-accessible navigation.
  const header = $('header.site'), menu = $('.locker-menu');
  function closeMenu() {
    if (!menu) return;
    header.classList.remove('menu-open'); menu.setAttribute('aria-expanded', 'false');
  }
  if (menu) {
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open)); header.classList.toggle('menu-open', open);
    });
    $$('.nav a').forEach(a => a.addEventListener('click', closeMenu));
    document.addEventListener('click', e => { if (!header.contains(e.target)) closeMenu(); });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); }
    });
  }
  document.addEventListener('click', e => {
    if (!e.target.closest('.nav-team')) $$('.nav-team[open]').forEach(d => { d.open = false; });
  });
  // Shared player search, with arrow keys, Enter and Escape.
  const globalInput = $('#globalPlayerSearch'), results = $('#globalPlayerResults');
  if (globalInput && results) {
    let matches = [], active = -1;
    globalInput.setAttribute('role', 'combobox');
    globalInput.setAttribute('aria-autocomplete', 'list');
    globalInput.setAttribute('aria-expanded', 'false');
    globalInput.setAttribute('aria-controls', results.id);
    results.setAttribute('role', 'listbox'); results.setAttribute('aria-label', 'Matching players');
    const closeResults = () => {
      results.classList.remove('open'); globalInput.setAttribute('aria-expanded', 'false');
      globalInput.removeAttribute('aria-activedescendant'); active = -1;
    };
    const setActive = index => {
      active = index;
      $$('.header-result', results).forEach((a, i) => {
        a.classList.toggle('active', i === active); a.setAttribute('aria-selected', String(i === active));
      });
      const option = $$('.header-result', results)[active];
      if (option) { globalInput.setAttribute('aria-activedescendant', option.id); option.scrollIntoView({block:'nearest'}); }
    };
    const draw = () => {
      const q = globalInput.value.trim().toLowerCase();
      if (!q) { matches = []; results.replaceChildren(); closeResults(); return; }
      const words = q.split(/\s+/);
      matches = players.filter(p => words.every(w => (p.tag + ' ' + p.team).toLowerCase().includes(w))).slice(0, 8);
      results.innerHTML = matches.length ? matches.map((p, i) => `<a id="player-result-${i}" role="option" aria-selected="false" class="header-result" href="${escape(p.slug)}.html"><span><b>${escape(p.tag)}</b><span>${escape(p.team)}</span></span><em>OPEN ↗</em></a>`).join('') : '<div class="header-empty" role="status">No matching player or team.</div>';
      results.classList.add('open'); globalInput.setAttribute('aria-expanded', 'true');
      if (matches.length) setActive(0);
    };
    globalInput.addEventListener('input', draw); globalInput.addEventListener('focus', draw);
    globalInput.addEventListener('keydown', e => {
      if (e.key === 'Escape') { closeResults(); globalInput.blur(); }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (!results.classList.contains('open')) draw();
        if (matches.length) setActive((active + (e.key === 'ArrowDown' ? 1 : -1) + matches.length) % matches.length);
      }
      if (e.key === 'Enter' && matches[active]) { e.preventDefault(); location.href = matches[active].slug + '.html'; }
    });
    document.addEventListener('click', e => { if (!e.target.closest('.header-searchbox')) closeResults(); });
    document.addEventListener('keydown', e => {
      const el = e.target;
      if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey && !el.isContentEditable && !/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName)) {
        e.preventDefault(); globalInput.focus();
      }
    });
  }
  // The spotlight uses the exact values from the shipped player profiles.
  const spot = $('.locker-spotlight');
  if (spot) {
    const buttons = $$('[data-spot]', spot);
    buttons.forEach((button, i) => button.addEventListener('click', () => {
      const p = bySlug.get(button.dataset.spot);
      if (!p) return;
      spot.style.setProperty('--spot', p.color);
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      $('#spot-index').textContent = `0${i + 1} / 04`;
      $('#spot-content').innerHTML = `<a class="spot-profile" href="${escape(p.slug)}.html"><img class="spot-photo" src="${escape(p.image)}" alt="${escape(p.tag)}" width="512" height="512"><span class="spot-ghost" aria-hidden="true">${escape(p.tag.toUpperCase())}</span><div class="spot-identity"><span>${escape(p.team)}</span><h2>${escape(p.tag)}<span aria-hidden="true">↗</span></h2></div><div class="spot-stats"><div><span>Sensitivity</span><b>${escape(p.sens)}</b></div><div><span>Field of view</span><b>${escape(p.fov)}</b></div><div><span>Response curve</span><b>${escape(p.curve)}</b></div></div></a>`;
    }));
  }
  const directory = $('#players'), teams = $('.teams-list');
  if (directory && teams) {
    const search = $('#search'), chips = $$('.chip', directory), sorter = $('#lockerSort');
    const cards = $$('.locker-player', teams), sections = $$('.teamsec', teams), sortedGrid = $('.locker-sorted-grid', teams);
    const originalGrid = new Map(cards.map(wrapper => [wrapper, wrapper.parentElement]));
    const empty = $('.locker-empty', teams);
    let team = 'all';
    const number = (wrapper, key) => {
      const n = parseFloat($('.card', wrapper).dataset[key]);
      return Number.isFinite(n) ? n : -Infinity;
    };
    function filter() {
      const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      let visible = 0;
      cards.forEach(wrapper => {
        const card = $('.card', wrapper);
        const haystack = `${card.dataset.search || ''} ${card.dataset.sens} ${card.dataset.fov}`.toLowerCase();
        const match = (team === 'all' || card.dataset.team === team) && terms.every(q => haystack.includes(q));
        wrapper.hidden = !match;
        if (match) visible++;
      });
      const mode = sorter.value;
      sortedGrid.hidden = mode === 'team';
      if (mode === 'team') {
        cards.forEach(wrapper => originalGrid.get(wrapper).appendChild(wrapper));
        sections.forEach(section => { section.hidden = !$$('.locker-player', section).some(w => !w.hidden); });
      } else {
        sections.forEach(section => { section.hidden = true; });
        const ordered = [...cards].sort((x, y) => {
          if (mode === 'sens' || mode === 'fov') {
            const a = number(x, mode), b = number(y, mode);
            if (a !== b) return a > b ? -1 : 1;
          }
          return $('.tag', x).textContent.localeCompare($('.tag', y).textContent);
        });
        ordered.forEach(w => sortedGrid.appendChild(w));
      }
      $('#count').textContent = `${visible} of ${cards.length} players`;
      empty.hidden = visible !== 0;
    }
    chips.forEach(chip => chip.addEventListener('click', () => {
      team = chip.dataset.team;
      chips.forEach(c => c.setAttribute('aria-pressed', String(c === chip)));
      filter();
    }));
    search.addEventListener('input', filter); sorter.addEventListener('change', filter);
    $$('[data-view]').forEach(button => button.addEventListener('click', () => {
      teams.classList.toggle('is-compact', button.dataset.view === 'compact');
      $$('[data-view]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    }));
    $('[data-reset-filters]').addEventListener('click', () => {
      search.value = ''; team = 'all'; sorter.value = 'team';
      chips.forEach(c => c.setAttribute('aria-pressed', String(c.dataset.team === 'all')));
      filter(); search.focus();
    });
    $('.locker-quick-search').addEventListener('submit', e => {
      e.preventDefault(); search.value = $('#quickSearch').value; team = 'all';
      chips.forEach(c => c.setAttribute('aria-pressed', String(c.dataset.team === 'all')));
      filter(); directory.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
      search.focus({preventScroll:true});
    });
    filter();
    // Compare buttons are siblings of profile links, avoiding nested controls.
    let selected = [];
    const tray = $('.locker-compare-tray'), selectedBox = $('#lockerSelected'), compareLink = $('#lockerCompareLink');
    function drawSelection() {
      tray.hidden = selected.length === 0;
      selectedBox.innerHTML = selected.map(slug => `<button type="button" data-remove="${escape(slug)}" aria-label="Remove ${escape(bySlug.get(slug).tag)} from comparison">${escape(bySlug.get(slug).tag)}<span aria-hidden="true">×</span></button>`).join('') + (selected.length === 1 ? '<span>Choose one more pro</span>' : '');
      $$('[data-pick]').forEach(button => {
        const yes = selected.includes(button.dataset.pick);
        button.setAttribute('aria-pressed', String(yes));
        button.innerHTML = `<span aria-hidden="true">${yes ? '✓' : '＋'}</span> ${yes ? 'Selected' : 'Compare'}`;
        button.closest('.locker-player').classList.toggle('is-selected', yes);
      });
      const ready = selected.length === 2;
      compareLink.setAttribute('aria-disabled', String(!ready));
      if (ready) { compareLink.href = `compare.html?a=${encodeURIComponent(selected[0])}&b=${encodeURIComponent(selected[1])}`; compareLink.removeAttribute('tabindex'); }
      else { compareLink.removeAttribute('href'); compareLink.setAttribute('tabindex', '-1'); }
      document.body.style.paddingBottom = selected.length ? '190px' : '';
    }
    $$('[data-pick]').forEach(button => button.addEventListener('click', () => {
      const slug = button.dataset.pick;
      if (selected.includes(slug)) selected = selected.filter(s => s !== slug);
      else if (selected.length < 2) selected.push(slug);
      else { toast('Two players selected. Remove one to choose another.'); return; }
      drawSelection();
    }));
    selectedBox.addEventListener('click', e => {
      const b = e.target.closest('[data-remove]');
      if (!b) return;
      const removed = b.dataset.remove;
      selected = selected.filter(s => s !== removed); drawSelection();
      const replacement = $('[data-remove]', selectedBox) || $(`[data-pick="${removed}"]`);
      if (replacement) replacement.focus({preventScroll:true});
    });
    $('[data-clear-compare]').addEventListener('click', () => {
      const former = selected[0]; selected = []; drawSelection();
      const button = $(`[data-pick="${former}"]`); if (button) button.focus({preventScroll:true});
    });
    compareLink.addEventListener('click', e => { if (selected.length !== 2) e.preventDefault(); });
  }
  // Copy real recorded values from this profile, keeping unknowns explicitly absent.
  const copyProfile = $('[data-copy-profile]');
  if (copyProfile) copyProfile.addEventListener('click', () => {
    const name = $('.player-hero-id h1').textContent.trim();
    const teamName = $('.teamname').textContent.trim();
    const lines = [`${name} — ${teamName}`, $('.pagemeta').textContent.trim(), ''];
    ['controller-settings', 'graphics', 'hardware'].forEach(id => {
      const section = document.getElementById(id); if (!section) return;
      const values = [];
      const fov = $('.graphics-fov-value', section);
      if (fov) values.push('Field of view: ' + [...fov.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim());
      $$('.row', section).forEach(row => {
        const k = $('.k', row), v = $('.v', row);
        if (k && v && !v.classList.contains('empty') && v.textContent.trim() !== '—') values.push(`${k.textContent.trim()}: ${v.textContent.trim()}`);
      });
      if (values.length) lines.push($('.profile-section-head h2', section).textContent.toUpperCase(), ...values, '');
    });
    const canonical = $('link[rel=canonical]');
    lines.push('Only recorded values are included. See the profile for sources and verification notes.', canonical ? canonical.href : location.href);
    copy(lines.join('\n'), `${name}’s recorded settings copied.`);
  });
  // Comparison enhancements integrate with the existing renderer.
  const onlyDiff = $('#onlyDifferences');
  if (onlyDiff) {
    const a = $('#pa'), b = $('#pb');
    function syncComparison() {
      const rows = $$('#cmp tbody tr');
      rows.forEach(row => { row.hidden = onlyDiff.checked && !$('.diff', row); });
      let note = $('.locker-comparison-empty');
      if (!note) { note = document.createElement('p'); note.className = 'locker-comparison-empty compare-note'; $('#cmp').appendChild(note); }
      note.textContent = 'No differences among the settings recorded for both players.';
      note.hidden = !onlyDiff.checked || rows.some(r => !r.hidden);
      const findSlug = name => players.find(p => p.tag === name)?.slug;
      const sa = findSlug(a.value), sb = findSlug(b.value);
      if (sa && sb) {
        const url = new URL(location.href); url.searchParams.set('a', sa); url.searchParams.set('b', sb);
        try { history.replaceState(null, '', url); } catch (_) { /* file:// may disallow updating history. */ }
      }
    }
    onlyDiff.addEventListener('change', syncComparison);
    document.addEventListener('locker:comparison', syncComparison);
    $('#swapPlayers').addEventListener('click', () => {
      const first = a.value; a.value = b.value; b.value = first;
      a.dispatchEvent(new Event('change', {bubbles:true}));
    });
    $('#shareComparison').addEventListener('click', () => {
      // Share the site's canonical HTTPS page even when previewing a local ZIP.
      const canonical = $('link[rel=canonical]');
      const url = new URL(canonical ? canonical.href : location.href);
      url.searchParams.set('a', players.find(p => p.tag === a.value)?.slug || a.value);
      url.searchParams.set('b', players.find(p => p.tag === b.value)?.slug || b.value);
      copy(url.href, 'Comparison link copied.');
    });
    syncComparison();
  }
  // Make existing table sorting accessible without replacing its data or algorithm.
  $$('#ptable th').forEach(th => {
    th.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); th.click(); } });
    th.addEventListener('click', () => {
      $$('#ptable th').forEach(h => h.setAttribute('aria-sort', h === th ? (h.dataset.asc === '1' ? 'ascending' : 'descending') : 'none'));
    });
  });
  const top = $('.locker-top');
  if (top) {
    let scheduled = false;
    const showTop = () => { top.hidden = window.scrollY < 800; scheduled = false; };
    window.addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(showTop); } }, {passive:true});
    top.addEventListener('click', () => { window.scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); });
    showTop();
  }
})();


/* ---------------------------------------------------------------------------
   Folded in from per-page inline copies (v30). These were byte-identical on
   up to 96 pages; keeping one cached copy removes ~100 KB of repeated HTML.
   --------------------------------------------------------------------------- */

/* --- nav current-page marker --- */
(function(){var p=(location.pathname.split("/").pop()||"index.html").toLowerCase();document.querySelectorAll(".nav a[href]").forEach(function(a){var h=(a.getAttribute("href")||"").split("/").pop().toLowerCase();if(h&&h===p)a.setAttribute("aria-current","page");});var d=document.querySelector(".nav-team");if(d&&d.querySelector('a[href="'+p+'"]'))d.setAttribute("data-current","");})();

/* --- player TOC scrollspy --- */
(function(){
  const toc=[...document.querySelectorAll('.player-toc a[data-section]')];
  const sections=toc.map(a=>document.getElementById(a.dataset.section)).filter(Boolean);
  if(!toc.length||!sections.length) return;
  const setActive=id=>toc.forEach(a=>a.classList.toggle('active',a.dataset.section===id));
  const update=()=>{
    const marker=window.scrollY+Math.min(180,window.innerHeight*.26);
    let current=sections[0].id;
    sections.forEach(sec=>{if(sec.offsetTop<=marker)current=sec.id;});
    if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-6)current=sections[sections.length-1].id;
    setActive(current);
  };
  toc.forEach(a=>a.addEventListener('click',()=>setActive(a.dataset.section)));
  window.addEventListener('scroll',update,{passive:true});
  window.addEventListener('resize',update,{passive:true});
  window.addEventListener('load',update);update();
})();

/* --- analysis-table scroll-end shadow --- */
(function(){var w=document.querySelectorAll(".pa-scroll");for(var i=0;i<w.length;i++){(function(o){var s=o.querySelector(".analysis-table-wrap");if(!s)return;function u(){var end=s.scrollLeft>=s.scrollWidth-s.clientWidth-1;if(end){o.setAttribute("data-scroll-end","");}else{o.removeAttribute("data-scroll-end");}}s.addEventListener("scroll",u,{passive:true});addEventListener("resize",u);u();})(w[i]);}})();
