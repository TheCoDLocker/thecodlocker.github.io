# Player photos

Optional. Every player already renders a generated team-coloured avatar, so the
site is complete without anything in this folder.

To use a real photo instead, drop a file named after the player's slug:

    players/scump.webp
    players/abezy.webp

`.webp` is what the markup requests. The `<img>` removes itself when the file is
missing, so a partial set is fine — players without a photo keep their avatar.

Slugs match the page filenames (`scump.html` -> `scump.webp`).
Portraits render square; faces sit best around 22% from the top.

## Current contents

48 portraits, built from the CDL 2026 cutout set. 512x512 WebP, ~20 KB each,
990 KB for the folder.

Each one is cropped head-and-shoulders around the detected face and composited
onto the same team-colour gradient the CSS avatar draws, so a photo tile and an
avatar tile sit next to each other without a seam. The source cutouts are
transparent; they are flattened here on purpose, because a transparent portrait
lets the avatar's initials show through behind the player's head.

**No photo yet** (these five keep their generated avatar, which is fine):
`hide`, `neptune`, `pred`, `scump`, `standy`.

**No page yet:** `gwinn.webp` and `knox.webp` are in this folder but have no
matching `.html`. They are unused until those pages exist — harmless, ~40 KB.

To regenerate or add to the set, the crop is: face box from an OpenCV frontal
cascade, square side = 3.15x the face width, face centre placed 40% down.
