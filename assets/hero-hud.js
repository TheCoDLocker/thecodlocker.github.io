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

  /* Headline decode: letters cycle through glyphs and settle left to right */
  const decodeEls = hero.querySelectorAll('[data-decode]');
  if (!still && decodeEls.length) {
    const glyphs = 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789/#%';
    const booting = document.documentElement.classList.contains('hx-boot');
    setTimeout(() => decodeEls.forEach((el, line) => {
      const final = el.textContent;
      const start = performance.now() + line * 160;
      const dur = 520;
      const step = now => {
        const t = (now - start) / dur;
        if (t >= 1) { el.textContent = final; return; }
        const settled = Math.max(0, Math.floor(t * final.length));
        let out = final.slice(0, settled);
        for (let i = settled; i < final.length; i++) {
          out += final[i] === ' ' || final[i] === '.' ? final[i] : glyphs[(Math.random() * glyphs.length) | 0];
        }
        el.textContent = out;
        requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }), booting ? 1150 : 120);
  }

  /* Crosshair and pointer readout */
  const reticle = hero.querySelector('.hx-reticle');
  const xOut = hero.querySelector('[data-hud="x"]');
  const yOut = hero.querySelector('[data-hud="y"]');
  const tag = reticle && reticle.querySelector('em');
  if (reticle && fine && !still) {
    let tx = 0, ty = 0, cx = 0, cy = 0, running = false, label = '';
    const frame = () => {
      cx += (tx - cx) * 0.22; cy += (ty - cy) * 0.22;
      reticle.style.setProperty('--x', cx + 'px');
      reticle.style.setProperty('--y', cy + 'px');
      if (Math.abs(tx - cx) > 0.3 || Math.abs(ty - cy) > 0.3) requestAnimationFrame(frame); else running = false;
    };
    hero.addEventListener('pointermove', e => {
      const r = hero.getBoundingClientRect();
      tx = e.clientX - r.left; ty = e.clientY - r.top;
      if (!hero.classList.contains('hx-aim')) { cx = tx; cy = ty; hero.classList.add('hx-aim'); }
      if (xOut) xOut.textContent = pad(tx, 4);
      if (yOut) yOut.textContent = pad(ty, 4);
      const card = e.target.closest && e.target.closest('.hx-card');
      const next = card ? card.dataset.name : '';
      if (next !== label) {
        label = next;
        reticle.style.setProperty('--rc', card ? card.style.getPropertyValue('--t') : 'var(--accent)');
        tag.textContent = card ? 'Target ' + next : '';
      }
      if (!running) { running = true; requestAnimationFrame(frame); }
    });
    hero.addEventListener('pointerleave', () => hero.classList.remove('hx-aim'));
  }

  /* Card rail: drag, native scroll, arrow keys, buttons, slow drift, endless loop */
  const rail = hero.querySelector('.hx-rail');
  if (!rail) return;
  const originals = [...rail.children];
  const total = originals.length;
  originals.forEach(li => {
    const copy = li.cloneNode(true);
    copy.setAttribute('aria-hidden', 'true');
    copy.inert = true;
    copy.querySelectorAll('[id]').forEach(n => n.removeAttribute('id'));
    rail.appendChild(copy);
  });
  let dragging = false;
  const countOut = hero.querySelector('[data-hud="card"]');
  const loopWidth = () => rail.children[total].offsetLeft - rail.children[0].offsetLeft;
  const stepWidth = () => rail.children[1].offsetLeft - rail.children[0].offsetLeft;
  const wrap = () => {
    const w = loopWidth();
    if (rail.scrollLeft >= w) rail.scrollLeft -= w;
    else if (rail.scrollLeft <= 0 && dragging) rail.scrollLeft += w;
  };
  const showCount = () => {
    if (!countOut) return;
    const i = Math.round((rail.scrollLeft % loopWidth()) / stepWidth()) % total;
    countOut.textContent = pad(i + 1, 2) + ' / ' + pad(total, 2);
  };
  rail.addEventListener('scroll', () => { wrap(); showCount(); }, {passive: true});

  // Drift: slow constant movement that pauses whenever someone is using the rail.
  let pausedUntil = 0, hovering = false, visible = true, last = 0, carry = 0;
  const pause = ms => { pausedUntil = performance.now() + ms; };
  const drift = now => {
    const dt = last ? Math.min(now - last, 50) : 16; last = now;
    const idle = !hovering && !dragging && visible && now > pausedUntil &&
      !rail.contains(document.activeElement) && !rail.querySelector('.is-flipped');
    if (idle) {
      carry += dt * 0.028;
      const whole = Math.floor(carry);
      if (whole) { rail.scrollLeft += whole; carry -= whole; }
    }
    requestAnimationFrame(drift);
  };
  if (!still) {
    rail.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') hovering = true; });
    rail.addEventListener('pointerleave', () => { hovering = false; });
    rail.addEventListener('touchstart', () => pause(5000), {passive: true});
    rail.addEventListener('wheel', () => pause(4000), {passive: true});
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(rail);
    }
    requestAnimationFrame(drift);
  }

  // Mouse drag to scroll. Touch keeps native swiping.
  let downX = 0, startLeft = 0, moved = false, pointerId = null;
  rail.addEventListener('pointerdown', e => {
    if (e.pointerType !== 'mouse' || e.button !== 0) return;
    pointerId = e.pointerId; downX = e.clientX; startLeft = rail.scrollLeft; moved = false;
  });
  rail.addEventListener('pointermove', e => {
    if (pointerId !== e.pointerId) return;
    const dx = e.clientX - downX;
    if (!dragging && Math.abs(dx) > 6) {
      dragging = moved = true; rail.classList.add('is-dragging'); rail.setPointerCapture(pointerId);
    }
    if (dragging) { rail.scrollLeft = startLeft - dx; }
  });
  const endDrag = () => {
    if (pointerId === null) return;
    pointerId = null;
    if (dragging) { dragging = false; rail.classList.remove('is-dragging'); pause(2500); }
  };
  rail.addEventListener('pointerup', endDrag);
  rail.addEventListener('pointercancel', endDrag);
  rail.addEventListener('click', e => { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
  rail.addEventListener('dragstart', e => e.preventDefault());

  const nudge = dir => {
    pause(4000);
    rail.scrollBy({left: dir * stepWidth(), behavior: still ? 'auto' : 'smooth'});
  };
  hero.querySelectorAll('[data-rail]').forEach(b => b.addEventListener('click', () => nudge(+b.dataset.rail)));
  rail.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); nudge(e.key === 'ArrowRight' ? 1 : -1); }
  });

  // Flip cards: tap the front for settings, tap again (or the x) to turn back.
  const setFlip = (card, on) => {
    card.classList.toggle('is-flipped', on);
    const front = card.querySelector('.hx-front'), back = card.querySelector('.hx-back');
    front.setAttribute('aria-expanded', String(on));
    front.inert = on; back.inert = !on;
    (on ? back.querySelector('a') : front).focus({preventScroll: true});
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
  showCount();
})();
