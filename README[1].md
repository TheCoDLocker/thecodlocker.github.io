# THE LOCKER — CDL Pro Settings & Classes

A static website tracking controller settings, sensitivities, and competitive classes for every player in the 2026 Call of Duty League (Black Ops 7). All 12 teams, 58 players, one page per player.

## How the project is laid out

```
cdl-locker/
├── data/players.json   ← the ONLY file you edit
├── build.py            ← generates the site from the data
└── site/               ← the finished website (upload this folder)
    ├── index.html
    ├── players/        ← one page per player (58 pages)
    ├── sitemap.xml
    └── robots.txt
```

## Adding a player's settings

1. Open `data/players.json`
2. Find the player and fill in their settings. Anything you don't know, leave as `null` and the site shows a dash. Example:

```json
{
  "slug": "simp",
  "tag": "Simp",
  "team": "faze",
  "verified": true,
  "source": "https://link-to-the-clip-or-stream",
  "lastUpdated": "2026-07-01",
  "settings": {
    "controller": "DualSense Edge",
    "buttonLayout": "Bumper Ping",
    "horizontalSens": 7,
    "verticalSens": 7,
    "adsMultiplier": 0.9,
    "responseCurve": "Dynamic",
    "fov": 110
  }
}
```

3. Rebuild the site:

```
python3 build.py
```

That's it — the player's page, the index card, and the sitemap all update.

**About `verified`:** keep it `false` until you've personally confirmed the settings from a stream, clip, or interview, and paste the link into `source`. Unverified pages show an orange "Unverified" badge and a disclaimer. This matters — sites like this live or die on whether people trust the numbers. The one pre-filled entry (Shotzzy) uses **placeholder values** so you can see the layout; replace them with real ones.

Where to find real settings: player Twitch/YouTube streams (they often scroll through settings when asked), TikTok clip accounts, event footage, and player interviews.

## Classes / loadouts

Each player has a `classes` array. Add one object per loadout:

```json
"classes": [{
  "name": "SMG build",
  "weapon": "Weapon name",
  "attachments": ["Barrel", "Stock", "Rear Grip", "Laser", "Magazine"],
  "perks": ["Perk 1", "Perk 2", "Perk 3"],
  "tactical": "Stim Shot",
  "lethal": "Semtex"
}]
```

## Putting it online (free)

**Netlify (easiest):** go to netlify.com, sign up, and drag the `site/` folder onto the deploy area. You get a live URL in seconds (e.g. `thelocker.netlify.app`). To update, rebuild and drag the folder again.

**GitHub Pages:** push the project to a GitHub repo, go to Settings → Pages, and set the source to the `site/` folder (or copy its contents to the repo root of a `gh-pages` branch).

**Custom domain (recommended for Google):** buy a domain (~$10–15/yr on Namecheap, Cloudflare, or Porkbun) and connect it in Netlify's domain settings. Then update `SITE_URL` at the top of `build.py` to your real domain and rebuild — this fixes the sitemap and canonical URLs.

## Getting on Google

1. Deploy the site with your domain and rebuild with the correct `SITE_URL`.
2. Go to **Google Search Console** (search.google.com/search-console), verify your domain.
3. Submit your sitemap: `https://your-domain.com/sitemap.xml`
4. Wait. New sites take days to weeks to get indexed, and longer to rank. Every player page is already set up with the title format people actually search ("Shotzzy Black Ops 7 settings"), meta descriptions, and canonical URLs.

What actually makes it rank over time: real, accurate, updated data. Pages that say "pending" won't rank — fill players in as you confirm their settings, starting with the most-searched names.

## Legal note

This is a fan site. Don't use CDL/team logos or Activision imagery without permission — team names and factual settings data are fine, logos and artwork are not. The footer already carries a "not affiliated" disclaimer; keep it.

## Changing the look

All styling lives in the `CSS` string in `build.py`. Team colors are in `data/players.json` under `teams` — they're approximations of each org's branding, tweak freely.
