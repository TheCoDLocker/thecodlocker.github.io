# CODLOCKER — hero and editorial update (v31)

## Upload to GitHub Pages

1. Extract this ZIP.
2. Upload all the files and folders to your existing repository root, replacing the previous versions. `index.html`, `assets/`, `players/` and the other folders belong directly at the root.
3. Keep any existing `CNAME` file and your GitHub Pages repository settings. This archive does not supply a custom-domain file.
4. Wait for GitHub Pages to finish updating, then refresh. Use Ctrl+F5 on Windows or Cmd+Shift+R on Mac if you still see the old page.

The site remains plain HTML, CSS and JavaScript. There is no installation or build step. Include the two new CSS files in `assets/` when uploading.

## Hero

- New “Open the pro locker” heading in a charcoal panel with warm orange accents and the supplied CODLOCKER logo faded into the background.
- A framed search area, an explicit Search button and direct links to all players and the comparison page.
- More readable profile, team and setup counts.
- The existing four-player spotlight remains beside the introduction on desktop and moves below it on narrower screens.
- The hero uses a new, homepage-only stylesheet: `assets/hero-v31.css?v=31`.

## Guides and news

- Rewritten all six guides and nine news articles, including introductions, explanations, advice and headings.
- Updated the guide and news card summaries and the relevant page descriptions.
- Shorter paragraphs, more direct language and less repetitive hype.
- Removed unsupported claims about player motives, controller wear and settings being universally correct. BO7 reference values are distinguished from confirmed MW4 information.
- Preserved all original data tables, publication dates, player records and external source links. This was an editorial update, not a fresh verification of the news or player settings.
- Added article typography and spacing in `assets/editorial-v31.css?v=31`.

## Preserved

All original site paths and assets remain. Player search, filters, sorting, comparison, navigation and spotlight scripts are unchanged. The AdSense script, publisher ID, `ads.txt` and existing privacy/cookie pages are unchanged. Approval and live ad serving remain controlled by Google.

## Validation

- Parsed all 96 HTML pages and checked local links, anchor targets, duplicate IDs, headings and label targets.
- Compared every data table, existing asset, external script, canonical URL and external source link against the supplied archive.
- Checked JavaScript syntax and the search, directory and spotlight element hooks.
- Checked the new CSS delimiters and image references, and calculated heading widths with the supplied font across 320–1920px breakpoints.
- Live browser rendering and end-to-end interaction testing were not available. The responsive checks were static checks, not screenshots or device testing.
