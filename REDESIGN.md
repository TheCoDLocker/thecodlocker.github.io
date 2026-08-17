# CODLOCKER redesign (v6)

A visual redesign of the existing site, moving it toward the Claude Design
mockups in `../project/Pro Settings Site.dc.html` and making it considerably
more colourful. No content, data, or copy was changed.

Drop these files into the GitHub Pages root exactly as they are — internal
links are all relative and unchanged.

## What changed

### 1. Shared CSS extracted (`assets/`)

Every page carried the same ~85KB of inline `<style>` — 91 pages shared a
byte-identical 67.6KB core block, and all 92 shared two more. That is now:

| file | what | used by |
|---|---|---|
| `pages.css` | shared page core | 91 pages |
| `home.css` | homepage-only core | `index.html` |
| `site.css` | the old polish + square layers | all 92 |
| `teams.css` | team-page additions | 12 team pages |
| `fonts.css` | self-hosted webfaces | all 92 |
| `redesign.css` | **the new visual language** | all 92 |

Pages dropped from ~100KB to 14–40KB, and the shared CSS is now cached once
instead of re-downloaded per page. The extraction was verified pixel-identical
before any restyling began.

**All visual work now happens in `redesign.css`.** It loads last and restyles
the existing class names rather than replacing markup.

### 2. Colour: team colours now drive the UI

The twelve CDL team colours already existed in the markup but were nearly
invisible — a few hairlines and dots. They now drive panels, card glows,
portraits, table hovers, section headers and rails, so each team section reads
as its own colour while the near-black base holds it together.

Pages with no team to borrow from (stats, news, league research) rotate through
a supporting palette instead of repeating one orange:

- `--accent` orange — brand, primary CTAs
- `--verified` green — confirmed data, positive values
- `--info` cyan — comparison, informational
- `--violet` — league-wide aggregates
- `--gold` — rank 1, highlights
- `--hot` — differences in the compare table

Each hue keeps one meaning, so the extra colour adds information rather than
noise.

### 3. Player portraits

Every player now has a portrait — a generated avatar built from their team
colour and initials, so the site is complete with no image files at all.

**To use real photos:** drop `players/<slug>.webp` (e.g. `players/scump.webp`).
The photo takes over automatically; players without one keep their avatar, so a
partial set is fine. See `players/README.md`.

The `<img>` only becomes visible once it has actually loaded, so a missing file
can never flash a broken-image icon.

> Note: the photos themselves are not included. These are real people, and
> their images are generally owned by the photographers, teams or the league —
> worth sorting out licensing before publishing any.

### 4. Mockup components

- **Player hero** — portrait, headline stat tiles (sens / FOV / ADS / curve,
  read from each page's own data) and a compare link, matching the mockup's
  "config at a glance" opening.
- **Glass panels** — hairline team-coloured ring, inner top highlight and a
  soft outer bloom.
- **Blueprint grid + accent bloom** on every hero.
- **Compare** — portraits on both pros, and the two sides mirrored (A anchored
  left, B right) so they stay distinguishable even when both teams are red.
- **Stat tiles** — small letterspaced mono labels over large mono numerals.

### 5. Self-hosted fonts

Barlow, Barlow Condensed and IBM Plex Mono now ship from `assets/fonts/`
(220KB, woff2) instead of Google Fonts. Removes a render-blocking third-party
request, drops the external dependency, and avoids a flash of fallback text.

## Verified

All 92 pages render at 1440px and 390px with no console errors, no horizontal
overflow, no broken images. Directory search, header typeahead, compare
re-render and stats sorting all still work.

## Not done

- Real player photos (see above).
- The mockup's "copy this config" export — the mockup shows a download/copy
  action the site has no backing feature for, so it was left out rather than
  shipped as a dead button.
