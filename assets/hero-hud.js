/* Homepage hero: HUD readouts, crosshair, headline decode and the player card rail.
   Everything here is enhancement: without it the hero still shows the headline,
   search and a scrollable row of cards. */
(function () {
  const hero = document.querySelector('.hx-hero');
  if (!hero) return;
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const pad = (n, w) => String(Math.max(0, Math.round(n))).padStart(w, '0');

  /* Scroll readout */
  const scrollOut = hero.querySelector('[data-hud="scroll"]');
  if (scrollOut) {
    const tick = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      scrollOut.textContent = pad(max > 0 ? scrollY / max * 100 : 0, 3);
    };
    addEventListener('scroll', tick, {passive: true});
    tick();
  }

  /* Headline decode: letters cycle through glyphs and settle left to right.
     Every word is locked to its finished width before the scramble starts, and
     the scramble waits for the headline font, so no line can rewrap and nothing
     else on the page moves while it runs. */
  const words = [...hero.querySelectorAll('[data-decode] .hx-word')];
  if (!still && words.length) {
    const glyphs = 'ABCDEFGHKNPRSTUVXYZ0123456789';
    const booting = document.documentElement.classList.contains('hx-boot');
    const fontReady = document.fonts && document.fonts.load
      ? Promise.race([document.fonts.load('700 100px "Barlow Condensed"'), new Promise(r => setTimeout(r, 2500))])
      : Promise.resolve();
    fontReady.then(() => {
      const finals = words.map(w => w.textContent);
      const widths = words.map(w => w.getBoundingClientRect().width);
      words.forEach((w, i) => { w.style.width = widths[i] + 'px'; });
      const lines = [...hero.querySelectorAll('[data-decode]')].map(line => words.filter(w => line.contains(w)));
      const run = () => lines.forEach((ws, n) => {
        const text = ws.map(w => finals[words.indexOf(w)]);
        const count = text.join('').length;
        const start = performance.now() + n * 160, dur = 520;
        const step = now => {
          const t = Math.max(0, (now - start) / dur);
          const settled = t >= 1 ? count : Math.floor(t * count);
          let idx = 0;
          ws.forEach((w, k) => {
            let out = '';
            for (const ch of text[k]) {
              out += idx < settled || ch === '.' ? ch : glyphs[(Math.random() * glyphs.length) | 0];
              idx++;
            }
            w.textContent = out;
          });
          if (t < 1) requestAnimationFrame(step);
          else ws.forEach(w => { w.style.width = ''; });
        };
        requestAnimationFrame(step);
      });
      setTimeout(run, booting ? Math.max(0, 1100 - performance.now()) : 0);
    });
  }

  /* Crosshair and pointer readout. Over the search box or the hero buttons the
     crosshair snaps to the control's centre and brackets it, like aim assist. */
  const reticle = hero.querySelector('.hx-reticle');
  const xOut = hero.querySelector('[data-hud="x"]');
  const yOut = hero.querySelector('[data-hud="y"]');
  const tag = reticle && reticle.querySelector('em');
  if (reticle && fine && !still) {
    let tx = 0, ty = 0, cx = 0, cy = 0, running = false, label = null, locked = null;
    const frame = () => {
      const k = locked ? 0.3 : 0.22;
      cx += (tx - cx) * k; cy += (ty - cy) * k;
      reticle.style.setProperty('--x', cx + 'px');
      reticle.style.setProperty('--y', cy + 'px');
      if (Math.abs(tx - cx) > 0.3 || Math.abs(ty - cy) > 0.3) requestAnimationFrame(frame); else running = false;
    };
    const lockOn = el => {
      locked = el;
      hero.classList.toggle('hx-locked', !!el);
      if (!el) return;
      const h = hero.getBoundingClientRect(), r = el.getBoundingClientRect(), gap = 8;
      reticle.style.setProperty('--lx', (r.left - h.left - gap) + 'px');
      reticle.style.setProperty('--ly', (r.top - h.top - gap) + 'px');
      reticle.style.setProperty('--lw', (r.width + gap * 2) + 'px');
      reticle.style.setProperty('--lh', (r.height + gap * 2) + 'px');
      reticle.dataset.tagPos = el.dataset.lockPos || 'below';
    };
    const aim = (e, el) => {
      const h = hero.getBoundingClientRect();
      if (el) {
        const r = el.getBoundingClientRect();
        tx = r.left + r.width / 2 - h.left; ty = r.top + r.height / 2 - h.top;
      } else {
        tx = e.clientX - h.left; ty = e.clientY - h.top;
      }
    };
    hero.addEventListener('pointermove', e => {
      const target = e.target.closest ? e.target : null;
      const lockEl = target && target.closest('[data-lock]');
      if (lockEl !== locked) lockOn(lockEl);
      aim(e, lockEl);
      if (!hero.classList.contains('hx-aim')) { cx = tx; cy = ty; hero.classList.add('hx-aim'); }
      if (xOut) xOut.textContent = pad(tx, 4);
      if (yOut) yOut.textContent = pad(ty, 4);
      const card = target && target.closest('.hx-card');
      const next = lockEl ? 'lock:' + lockEl.dataset.lock : card ? 'card:' + card.dataset.name : '';
      if (next !== label) {
        label = next;
        reticle.style.setProperty('--rc', card ? card.style.getPropertyValue('--t') : 'var(--accent)');
        tag.textContent = lockEl ? 'Lock // ' + lockEl.dataset.lock : card ? 'Target ' + card.dataset.name : '';
      }
      if (!running) { running = true; requestAnimationFrame(frame); }
    });
    hero.addEventListener('pointerleave', () => { hero.classList.remove('hx-aim'); lockOn(null); label = null; });
    addEventListener('scroll', () => { if (locked) lockOn(locked); }, {passive: true});
  }

  /* Card rail. The slow drift runs as a browser animation, so it stays smooth even
     while the page is still loading; dragging, swiping, the arrow buttons and keys
     take over from it and hand back after a pause. Endless loop via a copy of the row. */
  const rail = hero.querySelector('.hx-rail');
  if (!rail) return;
  const view = rail.parentElement;
  const originals = [...rail.children];
  const total = originals.length;
  originals.forEach(li => {
    const copy = li.cloneNode(true);
    copy.setAttribute('aria-hidden', 'true');
    copy.setAttribute('data-clone', '');
    copy.querySelectorAll('button, a').forEach(n => n.setAttribute('tabindex', '-1'));
    rail.appendChild(copy);
  });
  view.classList.add('is-live');
  const countOut = hero.querySelector('[data-hud="card"]');
  const SPEED = 0.03; // pixels per millisecond
  let W = 1, step = 1, padL = 0, anim = null;
  const measure = () => {
    padL = rail.children[0].offsetLeft;
    W = (rail.children[total].offsetLeft - padL) || 1;
    step = (rail.children[1].offsetLeft - padL) || 1;
  };
  const makeAnim = () => {
    if (still || !rail.animate) return null;
    const a = rail.animate([{transform: 'translate3d(0,0,0)'}, {transform: `translate3d(${-W}px,0,0)`}],
      {duration: W / SPEED, iterations: Infinity, easing: 'linear'});
    a.cancel();
    return a;
  };
  const mod = v => ((v % W) + W) % W;
  measure(); anim = makeAnim();

  let off = 0, auto = false, target = null, vel = 0, dragging = false, hovering = false, visible = true, pid = null;
  let flipped = false, keyFocus = false, pausedUntil = 0, startAt = Infinity, shown = -1, last = 0;
  const pause = ms => { pausedUntil = Math.max(pausedUntil, performance.now() + ms); };
  const showCount = x => {
    const i = Math.floor((x + step / 2) / step) % total;
    if (countOut && i !== shown) { shown = i; countOut.textContent = pad(i + 1, 2) + ' / ' + pad(total, 2); }
  };
  const apply = () => { const x = mod(off); rail.style.transform = `translate3d(${-x}px,0,0)`; showCount(x); };
  const toManual = () => {
    if (!auto) return;
    if (anim.currentTime != null) off = anim.currentTime * SPEED;
    anim.cancel(); auto = false; apply();
  };
  const toAuto = () => {
    off = mod(off);
    anim.currentTime = off / SPEED;
    anim.play(); auto = true;
  };
  const held = () => hovering || !visible || flipped || keyFocus;
  const frame = now => {
    const dt = last ? Math.min(now - last, 50) : 16; last = now;
    if (!auto) {
      if (!dragging && target !== null) {
        const d = target - off;
        off += still ? d : d * Math.min(1, dt * 0.012);
        if (Math.abs(target - off) < 0.4) { off = target; target = null; }
        apply();
      } else if (!dragging && Math.abs(vel) > 0.01) {
        off += vel * dt; vel *= Math.pow(0.94, dt / 16); apply();
      }
      if (anim && pid === null && !dragging && target === null && Math.abs(vel) <= 0.01 &&
          now > startAt && now > pausedUntil && !held()) toAuto();
    } else {
      const h = held();
      if (h && anim.playState === 'running') anim.pause();
      else if (!h && anim.playState === 'paused') anim.play();
      if (anim.currentTime != null) showCount(mod(anim.currentTime * SPEED));
    }
    requestAnimationFrame(frame);
  };
  // Start drifting a moment after the page has finished loading, then fetch the
  // remaining card photos in idle time so none pop in as the row moves.
  const begin = () => {
    startAt = performance.now() + 600;
    const warm = () => rail.querySelectorAll('img[loading="lazy"]').forEach(img => { img.loading = 'eager'; });
    setTimeout(() => (window.requestIdleCallback ? requestIdleCallback(warm) : warm()), 1500);
  };
  if (document.readyState === 'complete') begin(); else addEventListener('load', begin, {once: true});
  addEventListener('resize', () => {
    toManual(); measure();
    if (anim) { anim.cancel(); anim = makeAnim(); }
    apply();
  });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(view);
  }
  view.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') hovering = true; });
  view.addEventListener('pointerleave', () => { hovering = false; });
  view.addEventListener('focusin', () => { keyFocus = !!view.querySelector(':focus-visible'); });
  view.addEventListener('focusout', () => setTimeout(() => { keyFocus = !!view.querySelector(':focus-visible'); }));

  // Drag with a mouse or swipe with a finger; a vertical swipe still scrolls the page.
  let x0 = 0, y0 = 0, off0 = 0, lastX = 0, lastT = 0, moved = false;
  view.addEventListener('pointerdown', e => {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    toManual();
    pid = e.pointerId; x0 = lastX = e.clientX; y0 = e.clientY; off0 = off;
    lastT = performance.now(); moved = false; vel = 0; target = null;
  });
  view.addEventListener('pointermove', e => {
    if (pid !== e.pointerId) return;
    const dx = e.clientX - x0, dy = e.clientY - y0;
    if (!dragging) {
      if (Math.abs(dx) < 6 && Math.abs(dy) < 6) return;
      if (Math.abs(dy) > Math.abs(dx)) { pid = null; return; }
      dragging = moved = true; view.classList.add('is-dragging'); view.setPointerCapture(pid);
    }
    const now = performance.now();
    vel = vel * 0.6 + (-(e.clientX - lastX) / Math.max(1, now - lastT)) * 0.4;
    lastX = e.clientX; lastT = now;
    off = off0 - dx; apply();
  });
  const endDrag = () => {
    if (pid === null) return;
    pid = null;
    if (!dragging) return;
    dragging = false; view.classList.remove('is-dragging');
    vel = performance.now() - lastT > 80 ? 0 : Math.max(-2.5, Math.min(2.5, vel));
    pause(3000);
  };
  view.addEventListener('pointerup', endDrag);
  view.addEventListener('pointercancel', endDrag);
  view.addEventListener('click', e => { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
  view.addEventListener('dragstart', e => e.preventDefault());
  view.addEventListener('wheel', e => {
    if (Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return;
    e.preventDefault(); toManual(); target = null; vel = 0; off += e.deltaX; apply(); pause(3000);
  }, {passive: false});

  const nudge = dir => {
    toManual(); pause(4000); vel = 0;
    target = (Math.round((target ?? off) / step) + dir) * step;
  };
  hero.querySelectorAll('[data-rail]').forEach(b => b.addEventListener('click', () => nudge(+b.dataset.rail)));
  view.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); nudge(e.key === 'ArrowRight' ? 1 : -1); }
  });
  // Tabbing to a card that is off screen brings it into view.
  view.addEventListener('scroll', () => { view.scrollLeft = 0; });
  view.addEventListener('focusin', e => {
    view.scrollLeft = 0;
    const li = e.target.closest('.hx-rail > li');
    if (!li || li.hasAttribute('data-clone')) return;
    toManual();
    const x = li.offsetLeft - mod(target ?? off);
    if (x < 0 || x + li.offsetWidth > view.clientWidth) target = (target ?? off) + (x - padL);
    pause(4000);
  });

  // Flip cards: tap the front for settings, tap again (or the x) to turn back.
  const setFlip = (card, on) => {
    card.classList.toggle('is-flipped', on);
    const front = card.querySelector('.hx-front'), back = card.querySelector('.hx-back');
    front.setAttribute('aria-expanded', String(on));
    front.inert = on; back.inert = !on;
    flipped = !!rail.querySelector('.hx-card.is-flipped');
    if (!card.closest('[data-clone]')) (on ? back.querySelector('a') : front).focus({preventScroll: true});
  };
  rail.addEventListener('click', e => {
    const card = e.target.closest('.hx-card');
    if (!card || e.target.closest('a')) return;
    if (e.target.closest('.hx-front')) {
      rail.querySelectorAll('.hx-card.is-flipped').forEach(c => c !== card && setFlip(c, false));
      setFlip(card, true);
    } else if (e.target.closest('.hx-back')) {
      setFlip(card, false);
    }
  });
  rail.addEventListener('keydown', e => {
    const card = e.target.closest('.hx-card.is-flipped');
    if (card && e.key === 'Escape') setFlip(card, false);
  });
  apply();
  requestAnimationFrame(frame);
})();
