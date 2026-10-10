# CODLOCKER v29 — GitHub Pages root

## Upload

1. Extract the ZIP.
2. Upload **all of its files and folders** to your GitHub Pages repository root, replacing the existing versions. `index.html`, `assets/`, `players/` and the other folders must sit directly at the root.
3. Keep any custom `CNAME` file or repository settings that already exist in GitHub; neither is supplied by this archive.
4. Once GitHub Pages finishes updating, refresh the site. If your browser still displays the old version, use Ctrl+F5 (Windows) or Cmd+Shift+R (Mac).

This is the same plain HTML/CSS/JavaScript format as the supplied ZIP. No package installation, build command, framework migration or hosting service is required. `.nojekyll` keeps GitHub Pages serving the static files directly.

## What changed

- A new homepage opening with oversized condensed typography, orange accents, real supplied portraits, and a player spotlight switching between Dashy, Shotzzy, HyDra and Simp.
- The player database now sits ahead of the update log, with larger portrait cards and clearer sensitivity/FOV values.
- Player search supports multiple terms, alongside team filtering, alphabetical/sensitivity/FOV sorting and card/compact layouts.
- Select two players directly from the directory and open their comparison. Selections can be removed or cleared.
- Profile comparison links select the relevant player automatically. Comparisons also support swapping players, showing differences only and copying a URL.
- Pending database profiles are available in comparison selectors, explicitly marked as pending, with unconfirmed comparative values left empty.
- Player profiles have clearer headings, more readable settings tables, prominent FOV panels, collapsible FAQs and a button to copy recorded settings with the profile's source link.
- Shared navigation has a mobile menu, keyboard player search (press `/`, then use arrow keys and Enter), clear focus states and a skip link.
- Shared styling extends across all 96 HTML pages, including teams, stats, classes, guides and editorial pages.
- Back-to-top controls, copy feedback and reduced-motion support.
- Fixed an inherited CSS path to the existing logo and removed requests for absent portraits; initials remain as the fallback.

## Files

- `assets/locker.css`: new shared visual layer and responsive layouts.
- `assets/locker.js`: navigation, spotlight, directory, selection, copy and comparison interactions.
- `assets/locker-data.js`: searchable player metadata taken from the supplied site. Pending cards stay unconfirmed.
- All 96 HTML pages reference the new shared files. Existing paths, local images, self-hosted fonts, source links, metadata and external scripts are preserved.

Keep all three new assets with the updated HTML. Update the `v=29` cache query in the HTML if you revise these assets later. Player information is static; updates to a profile do not automatically rewrite the directory, comparison dataset or league aggregates.

## Validation

- Parsed all 96 HTML pages; checked local file links, anchor targets, duplicate IDs and inline JavaScript syntax.
- Checked new external JavaScript syntax and all relative stylesheet asset references.
- Exercised the existing comparison renderer with URL selections, invalid inputs, identical players, pending players and all 51 profile choices.
- Verified that original files, canonical metadata, external source links and external script references remain present.
- Browser visual and end-to-end interaction testing were not run in this environment. Responsive breakpoints are supplied for desktop, tablet and mobile.

This redesign uses the data and images in the supplied archive. It does not claim a fresh verification of player settings or news.
