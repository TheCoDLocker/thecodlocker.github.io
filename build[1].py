#!/usr/bin/env python3
"""
THE LOCKER — static site builder.
Edit data/players.json, then run:  python3 build.py
Output goes to the site/ folder. Upload that folder anywhere (Netlify, GitHub Pages).
"""
import json, os, shutil, html
from datetime import date

# ── CONFIG ──────────────────────────────────────────────────────────
SITE_URL  = "https://thecodlocker.com"   # change this if you later connect codlocker.com
SITE_NAME = "CODLOCKER"
TAGLINE   = "Every CDL pro. Every setting."
SEASON    = "Black Ops 7 · 2026 CDL Season"
# ────────────────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "site")

with open(os.path.join(ROOT, "data", "players.json")) as f:
    DATA = json.load(f)

TEAMS   = DATA["teams"]
# homepage order: teams in this sequence, players A–Z within each team
TEAM_ORDER = ["optic", "thieves", "m8", "faze", "falcons", "heretics", "koi", "g2", "carolina", "boston", "cloud9", "surge"]
PLAYERS = sorted(DATA["players"], key=lambda p: (TEAM_ORDER.index(p["team"]), p["tag"].lower()))

CSS = """
:root{
  --bg:#0E1114; --panel:#151A20; --panel2:#11151A; --line:#262D34;
  --text:#E9EDF0; --muted:#8A939C; --accent:#FF8A2A; --good:#3DDC84;
  --chamfer:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px));
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:'Barlow',system-ui,sans-serif;line-height:1.5}
body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(1000px 560px at 50% -10%,rgba(255,122,26,.14),transparent 60%),repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 1px,transparent 1px 3px)}
a{color:inherit;text-decoration:none}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
.display{font-family:'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.02em}
.mono{font-family:'IBM Plex Mono',monospace}

header.site{border-bottom:1px solid var(--accent);position:sticky;top:0;background:rgba(14,17,20,.92);backdrop-filter:blur(8px);z-index:10}
header.site .wrap{display:flex;align-items:center;gap:14px;height:58px}
.logo{font-family:'Barlow Condensed';font-weight:700;font-size:22px;letter-spacing:.06em;display:flex;align-items:center;gap:9px}
.logomark{height:30px;width:30px;object-fit:contain}
.logo b{color:var(--accent)}
.nav{display:flex;gap:16px;margin-left:auto}
.nav a{color:var(--muted);font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:13px}
.nav a:hover{color:var(--accent)}
.navbtn{background:var(--accent);color:#0E1114!important;padding:7px 16px;clip-path:polygon(0 0,calc(100% - 9px) 0,100% 9px,100% 100%,9px 100%,0 calc(100% - 9px));font-weight:700!important}
.navbtn:hover{background:#FFB01A;color:#0E1114!important}
.herocta{display:inline-block;margin-top:26px;background:var(--accent);color:#0E1114;font-family:'Barlow Condensed';font-weight:700;font-size:17px;text-transform:uppercase;letter-spacing:.08em;padding:13px 26px;clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,12px 100%,0 calc(100% - 12px))}
.herocta:hover{background:#FFB01A}
.herocta2{display:inline-block;margin-top:26px;margin-left:12px;background:transparent;color:var(--accent);border:2px solid var(--accent);font-family:'Barlow Condensed';font-weight:700;font-size:17px;text-transform:uppercase;letter-spacing:.08em;padding:11px 24px;clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,12px 100%,0 calc(100% - 12px))}
.herocta2:hover{background:var(--accent);color:#0E1114}
@media(max-width:560px){.herocta2{margin-left:0;margin-top:12px}}
.season{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.14em;margin-left:18px}
@media(max-width:680px){.season{display:none}}

.hero{padding:30px 0 24px;border-bottom:2px solid var(--accent)}
.hero h1{font-family:'Barlow Condensed';font-weight:700;font-size:clamp(30px,4.6vw,48px);line-height:1;text-transform:uppercase}
.hero h1 span{background:linear-gradient(90deg,#FF8A2A,#FFC24D);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{color:var(--muted);margin-top:14px;max-width:52ch}

.controls{padding:22px 0;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
#search{background:var(--panel);border:1px solid var(--line);color:var(--text);padding:10px 14px;font:inherit;width:min(320px,100%);clip-path:var(--chamfer)}
#search:focus{outline:2px solid var(--accent);outline-offset:1px}
.chip{background:var(--panel);border:1px solid var(--line);color:var(--muted);padding:7px 12px;font-size:12px;text-transform:uppercase;letter-spacing:.08em;cursor:pointer;font-family:'Barlow Condensed';font-weight:600}
.chip:hover{border-color:var(--chipcolor,var(--accent));color:var(--text)}
.chip[aria-pressed="true"]{color:#0E1114;background:var(--chipcolor,var(--accent));border-color:var(--chipcolor,var(--accent))}
.chip:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(238px,1fr));gap:11px;padding:4px 0 8px}
.counters{display:flex;gap:32px;margin-top:26px;flex-wrap:wrap}
.counters div{border-left:3px solid var(--accent);padding-left:13px}
.counters b{display:block;font-family:'Barlow Condensed';font-weight:700;font-size:34px;line-height:1}
.counters i{font-style:normal;font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.2em}
.teamsec{margin:26px 0 8px}
.teamhead{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.teamhead .trail{width:44px;height:9px;box-shadow:0 0 12px var(--team);background:var(--team);clip-path:polygon(0 0,100% 0,calc(100% - 8px) 100%,0 100%)}
.teamhead h2{font-family:'Barlow Condensed';font-weight:700;font-size:24px;text-transform:uppercase;letter-spacing:.03em}
.teamhead .tcount{color:var(--dim,#4a525a);font-size:11px;text-transform:uppercase;letter-spacing:.16em;font-family:'Barlow Condensed';margin-left:auto}
.cardstats{display:flex;gap:20px;margin-top:12px;border-top:1px solid var(--line);padding-top:9px}
.cardstats div b{display:block;font-family:'IBM Plex Mono';font-size:16px;font-weight:500;color:var(--text)}
.cardstats div i{font-style:normal;font-size:9px;color:#4a525a;text-transform:uppercase;letter-spacing:.18em}
.card{background:var(--panel);border:1px solid var(--line);clip-path:var(--chamfer);display:block;position:relative;padding:17px 18px 14px 18px;transition:transform .12s ease}
.card::before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:linear-gradient(90deg,var(--team) 0%,color-mix(in srgb,var(--team) 25%,transparent) 100%)}
.card::after{content:"";position:absolute;right:0;bottom:0;width:0;height:0;border-style:solid;border-width:0 0 14px 14px;border-color:transparent transparent var(--team) transparent;opacity:.55}
.card:hover{transform:translateY(-2px);border-color:var(--team);background:linear-gradient(180deg,color-mix(in srgb,var(--team) 10%,var(--panel)) 0%,var(--panel) 60%);filter:drop-shadow(0 0 14px color-mix(in srgb,var(--team) 45%,transparent))}
.card .tag{font-family:'Barlow Condensed';font-weight:700;font-size:27px;text-transform:uppercase;line-height:1}
.card .team{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.1em;margin-top:6px}
.card .status{margin-top:14px;font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}
.card .status.tracked{color:var(--good)}
.count{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.1em}

/* player page */
.lower-third{border-bottom:2px solid var(--team);padding:52px 0 30px;position:relative;overflow:hidden}
.lower-third::after{content:"";position:absolute;right:-70px;top:-50px;width:360px;height:360px;background:radial-gradient(closest-side,var(--team),transparent 70%);opacity:.16;pointer-events:none}
.lower-third .rail{height:7px;width:150px;background:linear-gradient(90deg,var(--team),transparent);box-shadow:0 0 14px var(--team);margin-bottom:20px}
.lower-third h1{font-family:'Barlow Condensed';font-weight:700;font-size:clamp(48px,9vw,92px);line-height:.9;text-transform:uppercase}
.lower-third .sub{display:flex;gap:14px;align-items:center;margin-top:12px;flex-wrap:wrap}
.lower-third .teamname{color:var(--team);font-family:'Barlow Condensed';font-weight:600;font-size:18px;text-transform:uppercase;letter-spacing:.06em}
.badge{font-size:10px;text-transform:uppercase;letter-spacing:.12em;padding:4px 8px;border:1px solid var(--line)}
.badge.unverified{color:var(--accent);border-color:var(--accent)}
.badge.verified{color:var(--good);border-color:var(--good);box-shadow:0 0 10px rgba(61,220,132,.35)}
.back{color:var(--muted);font-size:17px;font-weight:500;display:inline-block;padding:6px 0}
.back:hover{color:var(--accent)}
.pagemeta{color:var(--muted);font-size:13px}

.sheet{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;padding:32px 0}
.panel{background:var(--panel);border:1px solid var(--line);clip-path:var(--chamfer);padding:20px 22px}
.panel h2{font-family:'Barlow Condensed';font-weight:600;font-size:15px;text-transform:uppercase;letter-spacing:.16em;color:var(--accent);margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--line)}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:7px 0;border-bottom:1px dotted #20262d;font-size:14px}
.row:last-child{border-bottom:none}
.row .k{color:var(--muted)}
.row .v{font-family:'IBM Plex Mono';font-size:13px;text-align:right}
.row .v.empty{color:#4a525a}

.classes{padding:8px 0 64px}
.classes>h2{font-family:'Barlow Condensed';font-weight:700;font-size:26px;text-transform:uppercase;margin-bottom:16px}
.loadout{background:var(--panel);border:1px solid var(--line);clip-path:var(--chamfer);padding:20px 22px;margin-bottom:14px}
.loadout h3{font-family:'Barlow Condensed';font-weight:600;font-size:18px;text-transform:uppercase;letter-spacing:.04em}
.loadout .weapon{color:var(--team);font-family:'IBM Plex Mono';font-size:14px;margin:6px 0 12px}
.loadout ul{list-style:none;display:flex;flex-wrap:wrap;gap:8px}
section ul li{font-size:12px;font-family:'IBM Plex Mono';background:var(--panel2);border:1px solid var(--line);padding:5px 10px;list-style:none}\n.loadout li{font-size:12px;font-family:'IBM Plex Mono';background:var(--panel2);border:1px solid var(--line);padding:4px 8px}
.loadout .meta{margin-top:12px;color:var(--muted);font-size:13px}
.empty-note{color:var(--muted);background:var(--panel);border:1px dashed var(--line);padding:22px;font-size:14px}
.notice{margin:0 0 8px;padding:12px 16px;border-left:3px solid var(--accent);background:var(--panel);color:var(--muted);font-size:13px}
.source{color:var(--muted);font-size:13px;padding-bottom:40px}
.source a{color:var(--accent)}

footer{border-top:1px solid var(--line);padding:28px 0 44px;color:var(--muted);font-size:12px}
footer .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto}}

/* ── 2026 UI REFRESH ────────────────────────────────────────────────
   Presentation-only redesign. Existing data, URLs, SEO and ad code are
   intentionally untouched. Player cards remain text/data only. */
:root{
  --bg:#090C0F; --panel:#11161B; --panel2:#0D1217; --line:#222B33;
  --text:#F2F5F7; --muted:#919BA4; --accent:#FF6A1A; --good:#3DDC84;
}
body{
  background:
    radial-gradient(980px 520px at 76% 7%,rgba(255,106,26,.095),transparent 60%),
    linear-gradient(180deg,#080B0E 0%,#0B0F13 40%,#090C0F 100%);
}
body::before{
  background:
    linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.016) 1px,transparent 1px);
  background-size:38px 38px;
  opacity:.42;
}
.wrap{max-width:1280px;padding:0 24px}

header.site{
  border-bottom:1px solid #28313a;
  background:rgba(7,10,13,.92);
  box-shadow:0 10px 28px rgba(0,0,0,.28);
}
header.site .wrap{min-height:78px;height:auto;gap:18px}
.logo{font-size:clamp(30px,3vw,42px);gap:13px;line-height:1}
.logomark{
  width:58px;height:58px;
  filter:drop-shadow(0 0 10px rgba(255,106,26,.22));
}
.nav{gap:17px;align-items:center}
.nav a{font-size:13px;color:#A6AFB7;transition:color .15s ease,transform .15s ease}
.nav a:hover{color:#fff;transform:translateY(-1px)}
.navbtn{
  background:linear-gradient(180deg,#FF7B2A,#FF5D12);
  color:#090C0F!important;
  box-shadow:0 8px 18px rgba(255,106,26,.16);
}
.season{margin-left:4px}

.league-ticker{
  border-bottom:1px solid var(--line);
  background:#0B0F13;
  overflow-x:auto;
  scrollbar-width:thin;
}
.league-ticker-inner{
  min-height:44px;
  display:flex;
  align-items:center;
  white-space:nowrap;
  font-family:'IBM Plex Mono';
  font-size:11px;
  color:var(--muted);
}
.league-ticker span{padding:0 23px;border-right:1px solid #1D252C}
.league-ticker span:first-child{padding-left:0}
.league-ticker b{color:var(--accent)}

.hero{padding:54px 0 46px;border-bottom:1px solid #273039;overflow:hidden;position:relative}
.hero::before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(115deg,rgba(255,106,26,.035),transparent 38%);
}
.hero .wrap{position:relative}
.hero-layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,390px);gap:52px;align-items:center}
.hero-copy{position:relative;z-index:2}
.hero-eyebrow{
  color:var(--accent);font-family:'Barlow Condensed';font-weight:700;
  text-transform:uppercase;letter-spacing:.16em;font-size:13px;margin-bottom:12px;
}
.hero h1{font-size:clamp(48px,6.6vw,88px);max-width:9.6ch;line-height:.88;letter-spacing:-.01em}
.hero h1 span{background:none;color:var(--accent)}
.hero p{font-size:17px;max-width:58ch;margin-top:20px}
.hero-actions{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-top:28px}
.herocta,.herocta2{margin:0}
.herocta{background:linear-gradient(180deg,#FF7B2A,#FF5D12);padding:14px 25px;box-shadow:0 12px 25px rgba(255,106,26,.18)}
.herocta:hover{background:linear-gradient(180deg,#FF8C3A,#FF641A)}
.herocta2{color:#E7ECF0;border:1px solid #303A43;background:#11161B;padding:13px 22px}
.herocta2:hover{background:#151B21;color:#fff;border-color:#56616B}
.hero-emblem{min-height:315px;display:grid;place-items:center;position:relative}
.hero-emblem::before,.hero-emblem::after{
  content:"";position:absolute;border-radius:50%;pointer-events:none;
}
.hero-emblem::before{width:300px;height:300px;border:1px solid rgba(255,106,26,.24);box-shadow:0 0 65px rgba(255,106,26,.08) inset,0 0 40px rgba(255,106,26,.07)}
.hero-emblem::after{width:234px;height:234px;border:1px dashed rgba(255,106,26,.22)}
.hero-emblem-core{position:relative;z-index:2;width:205px;height:205px;display:grid;place-items:center}
.hero-emblem-core img{width:190px;height:190px;object-fit:contain;filter:drop-shadow(0 20px 26px rgba(0,0,0,.55)) drop-shadow(0 0 18px rgba(255,106,26,.24))}
.hero-emblem-label{
  position:absolute;bottom:7px;z-index:3;font-family:'IBM Plex Mono';font-size:10px;
  letter-spacing:.19em;text-transform:uppercase;color:#7E8992;
}

.home-dashboard{padding:0 24px}
.recent-strip{
  display:flex;gap:24px;flex-wrap:wrap;align-items:center;margin-top:22px;padding:14px 18px;
  background:linear-gradient(180deg,#12171C,#0F1419);border:1px solid #263039;
  clip-path:var(--chamfer);
}
.recent-label{font-family:'Barlow Condensed';font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
.recent-player{display:flex;gap:8px;align-items:baseline;color:var(--text);padding:4px 0}
.recent-player:hover .recent-tag{color:var(--accent)}
.recent-tag{font-family:'Barlow Condensed';font-weight:700;text-transform:uppercase;font-size:16px;transition:color .15s ease}
.recent-date{font-family:'IBM Plex Mono';font-size:10px;color:var(--muted)}
.counters{gap:12px;margin:12px 0 0}
.counters div{
  min-width:150px;border:1px solid #263039;border-left:3px solid var(--accent);
  background:linear-gradient(180deg,#11171C,#0E1318);padding:14px 18px;
  clip-path:var(--chamfer);
}
.counters b{font-size:31px}

.controls{
  margin-top:20px;padding:18px;background:#0E1318;border:1px solid #222C34;
  clip-path:var(--chamfer);
}
#search{width:min(390px,100%);padding:12px 15px;border-color:#303A43;background:#0A0F13}
.chip{padding:8px 12px;background:#11171C;border-color:#28323A;transition:transform .14s ease,border-color .14s ease,color .14s ease,background .14s ease}
.chip:hover{transform:translateY(-1px);box-shadow:0 5px 14px rgba(0,0,0,.18)}

.teamsec{
  margin:18px 0 14px;padding:18px;background:linear-gradient(180deg,rgba(18,24,30,.92),rgba(13,18,23,.92));
  border:1px solid #232D35;clip-path:var(--chamfer);
}
.teamhead{margin-bottom:14px}
.teamhead .trail{width:9px;height:30px;clip-path:none;box-shadow:0 0 14px color-mix(in srgb,var(--team) 35%,transparent)}
.teamhead h2{font-size:25px}
.teamhead h2 a{transition:color .15s ease}
.teamhead h2 a:hover{color:var(--team)!important}
.grid{grid-template-columns:repeat(auto-fill,minmax(205px,1fr));gap:11px;padding:0}
.card{
  min-height:126px;padding:17px 17px 14px;background:linear-gradient(180deg,#13191F,#0F1419);
  border:1px solid #28323A;clip-path:var(--chamfer);overflow:hidden;isolation:isolate;
  transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease,background .16s ease;
}
.card::before{height:3px;opacity:.9}
.card .tag{font-size:25px;transition:color .16s ease,text-shadow .16s ease,transform .16s ease}
.card .team{font-size:10px;margin-top:5px}
.cardstats{margin-top:12px;padding-top:9px;border-color:#252E36}
.cardstats div b{font-size:15px}

/* Strong player hover/focus highlight — team-colored, no player images. */
.card:hover,.card:focus-visible{
  transform:translateY(-4px);
  border-color:var(--team);
  background:linear-gradient(180deg,color-mix(in srgb,var(--team) 12%,#151B21),#10151A 72%);
  box-shadow:0 12px 28px rgba(0,0,0,.38),0 0 0 1px color-mix(in srgb,var(--team) 25%,transparent),0 0 24px color-mix(in srgb,var(--team) 18%,transparent);
  outline:none;
}
.card:hover .tag,.card:focus-visible .tag{color:#fff;text-shadow:0 0 12px color-mix(in srgb,var(--team) 42%,transparent);transform:translateX(2px)}
.card:hover .team,.card:focus-visible .team{color:#D5DCE1}
.card:hover .cardstats,.card:focus-visible .cardstats{border-top-color:color-mix(in srgb,var(--team) 42%,#252E36)}
.card:focus-visible{box-shadow:0 0 0 2px #090C0F,0 0 0 4px var(--team),0 12px 28px rgba(0,0,0,.4)}

.panel,.loadout{background:linear-gradient(180deg,#12181E,#0F1419);border-color:#27313A}
.lower-third{background:linear-gradient(180deg,rgba(255,255,255,.012),transparent);border-bottom-width:1px}
footer{background:#080B0E;border-color:#232C34}

@media(max-width:1060px){
  .nav{gap:11px}.nav a{font-size:12px}.season{display:none}
  .hero-layout{grid-template-columns:minmax(0,1fr) 300px;gap:28px}
  .hero-emblem::before{width:260px;height:260px}.hero-emblem::after{width:205px;height:205px}
  .hero-emblem-core img{width:165px;height:165px}
}
@media(max-width:820px){
  header.site .wrap{padding-top:10px;padding-bottom:10px;flex-wrap:wrap}
  .nav{width:100%;order:3;overflow-x:auto;flex-wrap:nowrap;padding-bottom:6px;scrollbar-width:thin}
  .hero{padding:40px 0 32px}.hero-layout{grid-template-columns:1fr}.hero-emblem{display:none}
  .home-dashboard{padding-left:16px;padding-right:16px}
}
@media(max-width:620px){
  .wrap{padding-left:16px;padding-right:16px}.logo{font-size:30px}.logomark{width:50px;height:50px}
  .hero h1{font-size:clamp(44px,15vw,66px)}.hero p{font-size:15px}
  .hero-actions{display:grid;grid-template-columns:1fr}.herocta,.herocta2{text-align:center;width:100%}
  .recent-strip{gap:10px 18px}.recent-label{width:100%}
  .counters{display:grid;grid-template-columns:1fr 1fr}.counters div{min-width:0}
  .controls{margin-left:16px;margin-right:16px}.controls.wrap{padding:14px}
  #search{width:100%}.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.card{min-height:118px;padding:15px 14px}.card .tag{font-size:22px}
  .teamsec{padding:14px}.teamhead .tcount{display:none}
}
@media(max-width:420px){
  .grid{grid-template-columns:1fr}.card{min-height:auto}
}

"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700'
         '&family=Barlow:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')

def esc(s):
    return html.escape(str(s))

def head(title, desc, canonical, include_ads=True, og_image=None, noindex=False):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="noindex,follow">' if noindex else ''}
<link rel="canonical" href="{canonical}">
{'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4248859491912544" crossorigin="anonymous"></script>' if include_ads else ''}
<link rel="icon" type="image/png" sizes="192x192" href="favicon.png">
<link rel="apple-touch-icon" href="favicon.png">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
{f'<meta property="og:image" content="{og_image}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{og_image}">' if og_image else ''}
<meta property="og:url" content="{canonical}">
{FONTS}
<style>{CSS}</style>
</head>"""

def header_html(rel=""):
    return f"""<header class="site"><div class="wrap">
<a class="logo" href="{rel}index.html"><img src="{rel}logo.png" alt="CODLOCKER" class="logomark">COD<b>LOCKER</b></a>
<nav class="nav"><a href="classes.html" class="navbtn">Classes</a><a href="stats.html">Stats</a><a href="news.html">News</a><a href="guides.html">Guides</a><a href="compare.html">Compare</a><a href="about.html">About</a><a href="contact.html">Contact</a><a href="privacy.html">Privacy</a></nav>
<span class="season">{esc(SEASON)}</span>
</div></header>"""

def footer_html():
    return f"""<footer><div class="wrap">
<span>{esc(SITE_NAME)} — {esc(TAGLINE)}</span>
<span><a href="guides.html" style="color:inherit;text-decoration:underline">Guides</a> &nbsp;·&nbsp; <a href="verify.html" style="color:inherit;text-decoration:underline">How We Verify</a> &nbsp;·&nbsp; <a href="about.html" style="color:inherit;text-decoration:underline">About</a> &nbsp;·&nbsp; <a href="contact.html" style="color:inherit;text-decoration:underline">Contact</a> &nbsp;·&nbsp; <a href="privacy.html" style="color:inherit;text-decoration:underline">Privacy</a> &nbsp;·&nbsp; Fan-made. Not affiliated with Activision or the Call of Duty League.</span>
</div></footer>"""

# ── SETTINGS SHEET ──────────────────────────────────────────────────

# ── PLAYER PAGE PROSE ───────────────────────────────────────────────
def _league_stats():
    sens = [p["settings"]["horizontalSens"] for p in PLAYERS if p["settings"].get("horizontalSens")]
    fovs = [p["settings"]["fov"] for p in PLAYERS if p["settings"].get("fov")]
    return (sum(sens)/len(sens) if sens else 1.7), (sum(fovs)/len(fovs) if fovs else 100)

def player_blurb(p, team):
    s = p["settings"]
    avg_sens, avg_fov = _league_stats()
    name, tname = p["tag"], team["name"]
    h = sum(ord(c) for c in p["slug"])  # stable per-player variety seed
    def pick(*opts): return opts[h % len(opts)]
    parts = []
    if s.get("horizontalSens") is not None:
        hs, vs = s["horizontalSens"], s.get("verticalSens")
        if vs is not None and vs != hs:
            parts.append(pick(
                f"{name} runs a split sensitivity — {hs} horizontal, {vs} vertical — one of the few in the league who separates the two sticks.",
                f"Unusually for the CDL, {name} splits sens: {hs} on the horizontal against {vs} vertical.",
            ))
        else:
            if abs(hs-avg_sens) < 0.06:
                parts.append(pick(
                    f"{name} plays on a {hs} sensitivity, almost exactly the league average.",
                    f"At {hs}, {name}'s sensitivity sits right in the heart of where the CDL clusters.",
                    f"{name}'s {hs} sens is textbook CDL — the league's center of gravity is right around that number.",
                ))
            elif hs > avg_sens:
                parts.append(pick(
                    f"{name} plays a {hs} sensitivity — quicker than most of the league, which mostly lives between 1.6 and 1.9.",
                    f"At {hs}, {name} is on the faster end of the CDL's sens spectrum.",
                    f"{name}'s {hs} sens puts them among the league's faster wrists.",
                ))
            else:
                parts.append(pick(
                    f"{name} plays a {hs} sensitivity — slower and more deliberate than most of the league.",
                    f"At {hs}, {name} sits on the controlled end of the CDL's 1.6–1.9 band.",
                    f"{name} keeps it slow at {hs}, prioritizing repeatable micro-adjustments.",
                ))
    if s.get("fov") is not None:
        f = s["fov"]
        if f >= 105: parts.append(pick(
            f"The {f} FOV is among the widest in the league, trading target size for peripheral vision.",
            f"A {f} FOV is a lot of screen real estate — {name} clearly values seeing flanks over bigger targets.",
        ))
        elif f <= 99: parts.append(pick(
            f"The {f} FOV runs tighter than most pros, keeping targets larger on screen.",
            f"{name} zooms in at {f} FOV — smaller picture, bigger enemies.",
        ))
        else: parts.append(pick(
            f"The {f} FOV lands where most of the league has settled.",
            f"A {f} FOV — squarely in the CDL's comfort zone.",
        ))
    if s.get("controller"):
        c = s["controller"]
        extra = f", paired with {s['thumbsticks']}" if s.get("thumbsticks") else ""
        parts.append(pick(
            f"Hardware-wise, {name} plays on a {c}{extra}.",
            f"The controller of choice is a {c}{extra}.",
            f"In the hands: a {c}{extra}.",
        ))
    if s.get("grip") == "Claw":
        parts.append(pick(
            "A claw grip keeps the right thumb on the stick while the index finger covers face buttons — more common among pros than fans expect.",
            "Claw grip means never leaving the aim stick to jump or slide — a real edge in close fights, at the cost of hand strain.",
        ))
    if s.get("buttonLayout") and s.get("buttonLayout") not in ("Default",):
        parts.append(f"The {s['buttonLayout']} button layout is confirmed by the league's official player settings data.")
    dz = (s.get("deadzoneLeftMin"), s.get("deadzoneLeftMax"), s.get("deadzoneRightMin"), s.get("deadzoneRightMax"))
    if all(v is not None for v in dz):
        if dz == (1,75,3,99):
            parts.append("Deadzones follow the common 1/75 left, 3/99 right configuration.")
        else:
            parts.append(pick(
                f"Deadzones are personally tuned: {dz[0]}/{dz[1]} on the left stick, {dz[2]}/{dz[3]} on the right.",
                f"The deadzones — L {dz[0]}/{dz[1]}, R {dz[2]}/{dz[3]} — are {name}'s own tune rather than a stock configuration.",
            ))
    if not parts:
        mates = [q for q in PLAYERS if q["team"] == p["team"] and q["tag"] != name and q["settings"].get("horizontalSens")]
        mates_html = ""
        if mates:
            links = ", ".join(f'<a href="{q["slug"]}.html" style="color:var(--accent)">{esc(q["tag"])}</a>' for q in mates)
            mates_html = f'<p style="margin-top:12px">Verified settings are already up for {name}\'s teammates: {links}.</p>'
        layout_line = ""
        if s.get("buttonLayout"):
            layout_line = f" One thing is confirmed from the league\'s official player settings data: {name} plays on a {s['buttonLayout']} button layout."
        return (f"<p>{name} competes for {tname} in the 2026 Call of Duty League season on Black Ops 7. "
                f"We haven\'t published {name}\'s full controller settings yet — CODLOCKER only lists numbers verified from a player\'s own stream, chat commands, or official league data, and reliable values for {name} haven\'t surfaced.{layout_line}</p>"
                f"<p style=\"margin-top:12px\">While this page fills in, the league norms are a solid starting point: nearly every CDL pro plays between 1.6 and 1.9 sensitivity, a 98–105 FOV, Dynamic response curve with Default aim assist, and low stick deadzones.</p>"
                + mates_html)
    intro = pick(
        f"<p>{name} competes for {tname} in the 2026 CDL season. ",
        f"<p>{name} is part of the {tname} roster for the 2026 Call of Duty League season. ",
        f"<p>One of {tname}\'s 2026 CDL roster, {name}\'s setup breaks down like this. ",
    )
    return intro + " ".join(parts) + f" Settings update whenever {name} changes something — the date under the player name shows the last confirmed change.</p>"

SETUP_FIELDS  = [("controller","Controller"),("grip","Grip"),("thumbsticks","Thumbsticks"),("buttonLayout","Button layout"),("stickLayout","Stick layout")]
AIM_FIELDS    = [("horizontalSens","Horizontal sens"),("verticalSens","Vertical sens"),
                 ("adsMultiplier","ADS multiplier"),("responseCurve","Response curve"),
                 ("deadzoneLeftMin","Deadzone L min"),("deadzoneLeftMax","Deadzone L max"),
                 ("deadzoneRightMin","Deadzone R min"),("deadzoneRightMax","Deadzone R max"),
                 ("aimAssistType","Aim assist type")]
DISPLAY_FIELDS= [("fov","FOV")]

def rows(settings, fields):
    out = []
    for key, label in fields:
        v = settings.get(key)
        if v is None:
            out.append(f'<div class="row"><span class="k">{label}</span><span class="v empty">—</span></div>')
        else:
            out.append(f'<div class="row"><span class="k">{label}</span><span class="v">{esc(v)}</span></div>')
    return "\n".join(out)


def player_faq(p, team):
    s = p["settings"]; name = p["tag"]
    qas = []
    if s.get("horizontalSens") is not None:
        vs = s.get("verticalSens")
        a = f"{name} plays on a {s['horizontalSens']} sensitivity" + (f" horizontal and {vs} vertical" if vs is not None and vs != s['horizontalSens'] else " on both sticks") + ", with a Dynamic response curve and Default aim assist."
        qas.append((f"What sensitivity does {name} play on in Black Ops 7?", a))
    if s.get("controller"):
        a = f"{name} uses a {s['controller']}" + (f" with {s['thumbsticks']}" if s.get("thumbsticks") else "") + (f", playing {s['grip'].lower()} grip" if s.get("grip") else "") + "."
        qas.append((f"What controller does {name} use?", a))
    if s.get("fov") is not None:
        qas.append((f"What FOV does {name} play on?", f"{name} plays on a {s['fov']} FOV, within the 98–105 range most CDL pros use."))
    if all(s.get(k) is not None for k in ("deadzoneLeftMin","deadzoneLeftMax","deadzoneRightMin","deadzoneRightMax")):
        qas.append((f"What are {name}'s deadzone settings?", f"{name} runs a {s['deadzoneLeftMin']}/{s['deadzoneLeftMax']} left-stick deadzone and {s['deadzoneRightMin']}/{s['deadzoneRightMax']} on the right stick."))
    if not qas: return "", ""
    items = "".join(f'<div style="margin-bottom:18px"><h3 style="font-family:\'Barlow Condensed\';font-size:19px;text-transform:uppercase;letter-spacing:.04em;color:var(--text)">{esc(q)}</h3><p style="color:var(--muted);font-size:14px;margin-top:6px">{esc(a)}</p></div>' for q,a in qas)
    html_block = f'<section class="wrap" style="max-width:820px;padding:6px 0 44px"><div class="panel"><h2>Frequently asked</h2>{items}</div></section>'
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
    ld_script = f'<script type="application/ld+json">{json.dumps(ld)}</script>'
    return html_block, ld_script

def player_page(p):
    team = TEAMS[p["team"]]
    title = f'{p["tag"]} Black Ops 7 Settings & Classes — CDL 2026'
    desc  = (f'{p["tag"]}\'s Call of Duty: Black Ops 7 controller settings, sensitivity, FOV and '
             f'competitive classes. {team["name"]}, 2026 CDL season.')
    canonical = f'{SITE_URL}/{p["slug"]}.html'
    tracked = any(p["settings"].get(k) is not None for k in ("horizontalSens","controller","fov"))
    badge = ('<span class="badge verified">Verified</span>' if p.get("verified")
             else '<span class="badge unverified">Unverified</span>')
    has_any = any(p["settings"].get(k) is not None for k in ("horizontalSens","controller","fov","buttonLayout","grip"))

    notice = ""
    if has_any and not p.get("verified"):
        notice = '<div class="wrap"><p class="notice">These values haven\'t been verified yet. Treat them as a starting point, not gospel.</p></div>'

    if has_any:
        sheet = f"""<section class="sheet wrap">
<div class="panel"><h2>Setup</h2>{rows(p["settings"], SETUP_FIELDS)}</div>
<div class="panel"><h2>Aiming</h2>{rows(p["settings"], AIM_FIELDS)}</div>
<div class="panel"><h2>Display</h2>{rows(p["settings"], DISPLAY_FIELDS)}</div>
</section>"""
    else:
        sheet = f"""<section class="sheet wrap">
<div class="empty-note">We haven't tracked {esc(p["tag"])}'s Black Ops 7 settings yet. Check back — this page updates as settings are confirmed from streams and events.</div>
</section>"""

    loadouts = ""
    if p["classes"]:
        items = []
        for c in p["classes"]:
            atts = "".join(f"<li>{esc(a)}</li>" for a in c.get("attachments", []))
            perks = " · ".join(esc(x) for x in c.get("perks", []))
            meta_bits = []
            if perks: meta_bits.append(f"Perks: {perks}")
            if c.get("tactical"): meta_bits.append(f"Tactical: {esc(c['tactical'])}")
            if c.get("lethal"): meta_bits.append(f"Lethal: {esc(c['lethal'])}")
            meta = f'<p class="meta">{" &nbsp;|&nbsp; ".join(meta_bits)}</p>' if meta_bits else ""
            items.append(f"""<div class="loadout">
<h3>{esc(c.get("name","Class"))}</h3>
<p class="weapon">{esc(c.get("weapon",""))}</p>
<ul>{atts}</ul>
{meta}
</div>""")
        loadouts = f'<section class="classes wrap"><h2>Classes</h2>{"".join(items)}</section>'

    src = ""
    if p.get("source"):
        src = f'<div class="wrap source">Source: <a href="{esc(p["source"])}" rel="noopener">{esc(p["source"])}</a></div>'
    updated = f' · Updated {esc(p["lastUpdated"])}' if p.get("lastUpdated") else ""

    og = f"{SITE_URL}/og-{p['slug']}.png" if tracked else None
    faq_html, faq_ld = player_faq(p, team)
    return f"""{head(title, desc, canonical, include_ads=tracked, og_image=og, noindex=not tracked)}
<body style="--team:{team['color']}">
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="index.html">← All players</a>
<div class="rail" style="margin-top:18px"></div>
<h1>{esc(p["tag"])}</h1>
<div class="sub"><span class="teamname">{esc(team["name"])}</span>{badge}<span class="pagemeta">{esc(SEASON)}{updated}</span></div>
</div></div>
<section class="wrap" style="max-width:820px;padding-top:26px;color:var(--muted);font-size:15px;line-height:1.8">{player_blurb(p, team)}</section>
{notice}
{sheet}
{loadouts}
{faq_html}
{src}
{footer_html()}
{faq_ld}
</body></html>"""

# ── INDEX ───────────────────────────────────────────────────────────
def index_page():
    title = "CDL Pro Settings & Classes — Every Black Ops 7 Pro | CODLOCKER"
    desc  = ("Controller settings, sensitivity, FOV and competitive classes for every Call of Duty "
             "League pro. All 12 teams, 2026 Black Ops 7 season.")
    tracked_count = sum(1 for p in PLAYERS if any(p["settings"].get(k) is not None for k in ("horizontalSens","controller","fov")))

    tracked_ps = [p for p in PLAYERS if p["settings"].get("horizontalSens") is not None]
    _sens = [p["settings"]["horizontalSens"] for p in tracked_ps]
    _fovs = [p["settings"]["fov"] for p in tracked_ps if p["settings"].get("fov") is not None]
    _claw = sum(1 for p in PLAYERS if p["settings"].get("grip")=="Claw")
    _last = max((p["lastUpdated"] for p in PLAYERS if p.get("lastUpdated")), default="")
    _builds = sum(len(w["builds"]) for w in DATA.get("metaClasses",{}).get("weapons",[]))
    ticker = (f'<div class="league-ticker"><div class="wrap league-ticker-inner">'
              f'<span>AVG SENS <b>{sum(_sens)/len(_sens):.2f}</b></span>'
              f'<span>AVG FOV <b>{sum(_fovs)/len(_fovs):.0f}</b></span>'
              f'<span>TRACKED <b>{len(tracked_ps)}/{len(PLAYERS)}</b></span>'
              f'<span>CLAW <b>{_claw}</b></span>'
              f'<span>LAST UPDATE <b>{_last}</b></span>'
              f'<span><a href="classes.html" style="color:inherit">META BUILDS <b>{_builds}</b></a></span>'
              f'</div></div>')
    recent = sorted([p for p in PLAYERS if p.get("lastUpdated")], key=lambda p: p["lastUpdated"], reverse=True)[:5]
    recent_html = ""
    if recent:
        items = "".join(f'<a class="recent-player" href="{p["slug"]}.html"><span class="recent-tag">{esc(p["tag"])}</span><span class="recent-date">{esc(p["lastUpdated"])}</span></a>' for p in recent)
        recent_html = f'<div class="recent-strip"><a href="updates.html" class="recent-label">Recently updated →</a>{items}</div>'
    chips = ['<button class="chip" data-team="all" aria-pressed="true">All teams</button>']
    for key in TEAM_ORDER:
        t = TEAMS[key]
        chips.append(f'<button class="chip" data-team="{key}" aria-pressed="false" style="--chipcolor:{t["color"]}">{esc(t["name"])}</button>')

    def card(p):
        t = TEAMS[p["team"]]
        tracked = any(p["settings"].get(k) is not None for k in ("horizontalSens","controller","fov"))
        s = p["settings"]
        if tracked:
            bits = []
            if s.get("horizontalSens") is not None: bits.append(f'<div><b>{esc(s["horizontalSens"])}</b><i>SENS</i></div>')
            if s.get("fov") is not None: bits.append(f'<div><b>{esc(s["fov"])}</b><i>FOV</i></div>')
            bottom = f'<div class="cardstats">{"".join(bits)}</div>' if bits else '<span class="status tracked">● Settings tracked</span>'
        else:
            bottom = '<span class="status">○ Pending</span>'
        return f"""<a class="card" href="{p["slug"]}.html" data-team="{p["team"]}" data-tag="{esc(p["tag"].lower())}" style="--team:{t["color"]}">
<span class="tag">{esc(p["tag"])}</span>
<span class="team" style="display:block">{esc(t["name"])}</span>
{bottom}
</a>"""

    sections = []
    for key in TEAM_ORDER:
        t = TEAMS[key]
        roster = [p for p in PLAYERS if p["team"] == key]
        cards = "".join(card(p) for p in roster)
        sections.append(f"""<section class="teamsec" data-team="{key}" style="--team:{t["color"]}">
<div class="teamhead"><span class="trail"></span><h2><a href="{key}.html" style="color:var(--text)">{esc(t["name"])}</a></h2><span class="tcount">{len(roster)} players</span></div>
<div class="grid">{cards}</div>
</section>""")

    js = """
const search=document.getElementById('search');
const chips=[...document.querySelectorAll('.chip')];
const cards=[...document.querySelectorAll('.card')];
const secs=[...document.querySelectorAll('.teamsec')];
const count=document.getElementById('count');
let team='all';
function apply(){
  const q=search.value.trim().toLowerCase();
  let n=0;
  cards.forEach(c=>{
    const ok=(team==='all'||c.dataset.team===team)&&c.dataset.tag.includes(q);
    c.style.display=ok?'':'none'; if(ok)n++;
  });
  secs.forEach(s=>{
    const any=[...s.querySelectorAll('.card')].some(c=>c.style.display!=='none');
    s.style.display=any?'':'none';
  });
  count.textContent=n+' players';
}
chips.forEach(ch=>ch.addEventListener('click',()=>{
  team=ch.dataset.team;
  chips.forEach(x=>x.setAttribute('aria-pressed',x===ch?'true':'false'));
  apply();
}));
search.addEventListener('input',apply);
apply();
"""
    return f"""{head(title, desc, SITE_URL + "/")}
<body>
{header_html()}
{ticker}
<div class="hero"><div class="wrap hero-layout">
<div class="hero-copy">
<div class="hero-eyebrow">The home of CDL settings</div>
<h1>Every CDL pro.<br><span>Every setting.</span></h1>
<p>Controller settings, sensitivities and competitive classes for all 12 Call of Duty League rosters — pulled from streams, events and interviews as they're confirmed.</p>
<div class="hero-actions">
<a class="herocta" href="classes.html">View Pro Meta Classes →</a>
<a class="herocta2" href="compare.html">Compare Players</a>
<a class="herocta2" href="stats.html">League Stats</a>
</div>
</div>
<div class="hero-emblem" aria-hidden="true">
<div class="hero-emblem-core"><img src="logo.png" alt=""></div>
<div class="hero-emblem-label">Pro settings database</div>
</div>
</div></div>
<div class="wrap home-dashboard">
{recent_html}
<div class="counters">
<div><b>{len(PLAYERS)}</b><i>Players</i></div>
<div><b>{len(TEAMS)}</b><i>Teams</i></div>
</div>
</div>
<div class="controls wrap">
<input id="search" type="search" placeholder="Search a player…" aria-label="Search players">
{"".join(chips)}
<span class="count" id="count"></span>
</div>
<main class="wrap" style="padding-bottom:72px">
{"".join(sections)}
</main>
<section class="wrap" style="max-width:820px;padding:10px 0 60px;color:var(--muted);font-size:15px;line-height:1.8;border-top:1px solid var(--line)">
<h2 style="font-family:'Barlow Condensed';font-weight:700;font-size:26px;text-transform:uppercase;color:var(--text);margin:34px 0 12px">What is CODLOCKER?</h2>
<p>CODLOCKER tracks the controller settings of every professional player in the Call of Duty League — sensitivity, FOV, deadzones, button layouts, grips, and the hardware in their hands — for the 2026 Black Ops 7 season. Every number is verified from the player's own stream, the league's official published data, or event broadcasts; where we don't have a confirmed value, the page shows a dash rather than a guess. See <a href="verify.html" style="color:var(--accent)">how we verify</a>.</p>
<p style="margin-top:12px">Beyond individual pages, the <a href="stats.html" style="color:var(--accent)">stats page</a> aggregates the whole league — averages, distributions, and a sortable table of every player — the <a href="compare.html" style="color:var(--accent)">compare tool</a> puts any two pros side by side, and the <a href="classes.html" style="color:var(--accent)">classes page</a> carries the exact competitive weapon builds with import codes. Pros change settings constantly, so every page shows its last confirmed update; recent changes and analysis land in <a href="news.html" style="color:var(--accent)">news</a>.</p>
</section>
{footer_html()}
<script>{js}</script>
</body></html>"""


# ── STATIC PAGES ────────────────────────────────────────────────────
def static_page(title, desc, slug, heading, body_html):
    canonical = f"{SITE_URL}/{slug}.html"
    return f"""{head(title, desc, canonical)}
<body>
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="index.html">← All players</a>
<div class="rail" style="margin-top:18px;background:var(--accent)"></div>
<h1 style="font-size:clamp(36px,6vw,60px)">{esc(heading)}</h1>
</div></div>
<section class="wrap" style="padding:34px 0 64px;max-width:760px">
{body_html}
</section>
{footer_html()}
</body></html>"""

ABOUT_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.75">
<p>CODLOCKER tracks the controller settings, sensitivities, and competitive classes of every player in the Call of Duty League — all 12 teams, updated throughout the 2026 Black Ops 7 season.</p>
<p style="margin-top:14px">Settings are sourced directly from the players themselves: Twitch chat commands on their own channels, live streams, event broadcasts, and interviews. A <b style="color:var(--good)">Verified</b> badge means the numbers were confirmed from one of those sources; <b style="color:var(--accent)">Unverified</b> means they are community-reported and pending confirmation. Pros tweak their setups constantly, so every player page shows when it was last updated.</p>
<p style="margin-top:14px">Spot something outdated or wrong? Settings change mid-season all the time — pages are corrected as new information is confirmed.</p>
<p style="margin-top:14px;color:var(--muted)">CODLOCKER is an independent fan project. It is not affiliated with, endorsed by, or connected to Activision, the Call of Duty League, or any CDL team or player.</p>
</div>
"""

CONTACT_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.75">
<p>Got a settings update, a correction, or something else? Reach out — corrections and fresh info are always welcome, especially with a source (a clip, VOD timestamp, or stream link).</p>
<p style="margin-top:22px;font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.12em">Email</p>
<p style="margin-top:6px"><a href="mailto:thecodlocker7@gmail.com" style="color:var(--accent);font-family:'IBM Plex Mono',monospace;font-size:17px">thecodlocker7@gmail.com</a></p>
<p style="margin-top:22px;color:var(--muted)">CODLOCKER is an independent fan project and is not affiliated with Activision, the Call of Duty League, or any team or player.</p>
</div>
"""


GUIDE_SETTINGS_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.8">
<p>Every setting on a pro's page changes how the game feels, but they don't all matter equally. This guide explains what each one actually does, what the league has collectively settled on, and what's worth copying versus what's personal preference.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">Sensitivity</h2>
<p>Sensitivity controls how fast your view rotates when you move the right stick. Across the CDL, almost the entire league sits between 1.6 and 1.9 — a far tighter band than the settings menu allows, and much lower than most casual players run. The reason is consistency: lower sens makes micro-adjustments repeatable, and pros win fights on centering and accuracy, not flick speed. A small number of players split their horizontal and vertical values, keeping vertical slightly different to fine-tune recoil control. If you take one thing from the pros, it's this: pick something in that 1.6–1.9 range and stop changing it.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">FOV (Field of View)</h2>
<p>FOV sets how much of the world fits on your screen. Higher values show more of your surroundings but make targets smaller; lower values zoom you in. The league clusters around 98–105, balancing peripheral information against target size. Players on the wider end are prioritizing map awareness for their role; players on the tighter end want bigger targets. Unlike sensitivity, FOV is genuinely personal — copy a pro's number as a starting point, then adjust to what your eyes prefer.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">Deadzones</h2>
<p>Deadzone minimums decide how far a stick must move before the game registers input; maximums decide where input caps out. Lower minimums mean faster response but risk stick drift on worn controllers. The de facto league standard is 1/75 on the left stick and 3/99 on the right — you'll see it on page after page across the site — with a handful of players running personal tunes. If your controller is new and drift-free, low minimums are free responsiveness; if you're getting phantom movement, raise the minimum until it stops.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">Response curve and aim assist</h2>
<p>This one's simple: the league runs Dynamic response curve and Default aim assist, essentially without exception. Dynamic front-loads stick response for faster initial aim while keeping fine control near center. There is no secret setting here — the pros use what the game gives everyone.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">Button layouts and grip</h2>
<p>Layouts vary more than any other setting — Default, Tactical, flipped variants, and one lone Bumper Jumper holdout are all represented, per the league's own published data. Tactical (crouch on the right stick) exists so players can slide and drop-shot without leaving the thumbstick, which is also why claw grip is common: it keeps aim and face buttons available at the same time. Many pros sidestep the tradeoff entirely with back paddles on custom controllers. This is the most personal category on the site — copy the concept (never leave your aim stick to press a button), not necessarily the exact layout.</p>
</div>
"""

GUIDE_CODES_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.8">
<p>Every build on our <a href="classes.html" style="color:var(--accent)">Pro Meta Classes</a> page includes a build code — a short string like A01-AV3HK-U2JA5-1. Here's what they are and how to use them.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">What a build code is</h2>
<p>Black Ops 7's gunsmith can export any weapon build as a shareable code. Import one and the game recreates the exact configuration — same attachments, same everything — with no manual setup. It's the fastest way to run precisely what the pros run, with zero transcription errors.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">How to import one</h2>
<p>Open the Gunsmith on the weapon, look for the build code option (shown alongside the build code display), choose enter/import code, and type the code exactly as shown, dashes included. Confirm, and the build applies. If a code won't accept, the usual culprits are a typo — the codes are case-sensitive — or attachments you haven't unlocked yet at your current weapon level.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">Why the pros all run the same builds</h2>
<p>Competitive Call of Duty runs under CDL rules plus GAs — gentlemen's agreements between the pro teams that ban attachments and weapons considered unhealthy for competition, on top of the official ruleset. By the time the bans settle, the viable pool is tiny: two Mod 15 configurations and effectively one MPC build. That's why our classes page is short — it isn't a sample of what pros use, it's the entire competitive meta.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">Should you run pro builds in pubs?</h2>
<p>They work anywhere, but remember what they're optimized for: mirrored fights on competitive maps against the best players alive, under restriction. In public matches, attachments the pros have GA'd away might serve you better. Use the pro builds when you're practicing for ranked or scrims — that's the environment they're tuned for.</p>
</div>
"""


VERIFY_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.8">
<p>Every number on CODLOCKER traces to one of three sources, in order of preference:</p>
<p style="margin-top:14px"><b>1. The player themselves.</b> Most settings come directly from a player's own Twitch channel — either shown on stream or via the chat commands (!sens, !fov, !controller, !deadzone) their own bots answer with. Nothing is closer to the source than the player's account publishing their own numbers.</p>
<p style="margin-top:14px"><b>2. Official league data.</b> The Call of Duty League publishes select player settings, including button layouts. Where the league has published a value, we use it and mark it accordingly.</p>
<p style="margin-top:14px"><b>3. Event broadcasts and interviews.</b> Settings visibly confirmed on official broadcasts or stated by the player in interviews.</p>
<p style="margin-top:14px">What we never do: guess, copy from unsourced lists, or fill a blank with a plausible number. A page showing a dash means we don't have a verified value — full stop. The <b style="color:var(--good)">Verified</b> badge means the page's data came from the sources above; <b style="color:var(--accent)">Unverified</b> marks community-reported values still awaiting confirmation.</p>
<p style="margin-top:14px">Pros change settings mid-season constantly, so every player page carries a last-updated date. Spot something stale or wrong? <a href="contact.html" style="color:var(--accent)">Tell us</a> — corrections with a source (clip, VOD timestamp, stream link) get fixed same-day.</p>
</div>
"""


DIAG = lambda f,alt: f'<img src="{f}" alt="{alt}" style="width:100%;display:block;border:1px solid var(--line);margin:20px 0" loading="lazy">'

GUIDE_DEADZONE_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.8">
<p>Deadzones are the least understood setting on any pro's sheet, and the one where copying blindly can actively hurt you. Here's how they work and how to read the league's numbers.</p>
""" + DIAG("diag-deadzone.png","Deadzone diagram: min deadzone ring and 75 max saturation inside full stick range") + """
<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:24px 0 10px;color:var(--accent)">Minimum deadzone</h2>
<p>The min value sets how far the stick must physically move before the game registers anything. Inside that ring, input is ignored. Every point of minimum is latency you added on purpose — so pros push it as low as their hardware allows. Our tracking shows most of the league bottoms the left stick at 0 and runs 2–5 on the right. The catch: a min of 0 on a controller with any wear means stick drift — your character creeps, your aim ghosts. The rule is simple: run the lowest value that gives you zero drift, and accept that on an older pad that number is higher than what the pros run on fresh customs.</p>
<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:24px 0 10px;color:var(--accent)">Maximum input threshold</h2>
<p>The max sets where the game reads "stick fully pushed." At 75, you hit full sprint or full turn speed at 75% of the stick's physical travel — the last quarter of movement does nothing extra, which effectively makes the stick respond faster without touching sensitivity. Right-stick max is 99 almost universally, but left-stick max is where players personalize: our data has starters anywhere from 60 to 75. Lower max = full movement input arrives sooner = snappier strafes.</p>
<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:24px 0 10px;color:var(--accent)">Reading a pro's numbers</h2>
<p>When a player page shows L 0/70 · R 3/99, that's: left stick registers instantly and maxes at 70% travel; right stick has a hair of buffer and uses nearly full travel. Compare a few pages and you'll see deadzones vary more than any other setting — because they're tuned to a specific controller in a specific condition, not to a feel preference. That's also why they're the one setting you should tune to <i>your</i> hardware rather than copy. Full per-player values are on every tracked page, and the <a href="deadzone-data-2026.html" style="color:var(--accent)">deadzone data article</a> covers what the league-wide pass found.</p>
</div>
"""

GUIDE_FOV_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.8">
<p>FOV is the most-copied setting after sensitivity, and the one where the tradeoff is easiest to actually see.</p>
""" + DIAG("diag-fov.png","FOV comparison: same enemy at 98 versus 106 field of view") + """
<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:24px 0 10px;color:var(--accent)">The tradeoff</h2>
<p>Field of view sets how many degrees of the world fit on your screen. Push it higher and you see more — flanks, lane edges, movement in your periphery — but everything shrinks, including the enemy you're shooting. Pull it lower and targets get bigger while your awarenessnarrows to a tunnel. Neither direction is free; the setting is a slider between information and target size.</p>
<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:24px 0 10px;color:var(--accent)">Where the league landed</h2>
<p>Across every tracked player, the CDL clusters between 98 and 105 — a strikingly narrow band out of the full range the menu offers. Below ~98, pros feel blind to flanks in respawn modes; above ~106, targets get small enough that centering suffers at range. Within the band, role explains most of the spread: aggressive SMG players skew higher (they need the map awareness for their movement), while some AR anchors sit lower for the bigger targets on long sightlines. Check any team page and you'll usually find both ends of the band on the same roster.</p>
<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:24px 0 10px;color:var(--accent)">Practical advice</h2>
<p>Two things matter more than the exact number. First, FOV interacts with sensitivity — raising FOV makes your sens feel slower (same rotation covers more visual ground), so change one at a time. Second, consistency beats optimization here like everywhere: pick something in the 98–105 band, give it a full week before judging, and stop moving it. If your aim feels off after a FOV change, that's usually the sens interaction, not the FOV itself.</p>
</div>
"""

GUIDE_CURVES_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.8">
<p>Response curve is the setting nobody experiments with — because the league solved it. Here's what it does and why every pro page on this site says the same thing.</p>
""" + DIAG("diag-curves.png","Response curve graph comparing dynamic, linear, and standard curves") + """
<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:24px 0 10px;color:var(--accent)">What a response curve is</h2>
<p>The curve maps physical stick movement to turn speed. Linear is one-to-one: 40% stick = 40% speed, honest but twitchy, because your first few millimeters of movement already swing your aim. Standard eases in slowly and ramps late — forgiving near center, sluggish when you commit. Dynamic flips that: it front-loads response so your initial movement translates fast, then flattens so you keep fine control near full deflection. On the graph, that's the orange curve rising steep and early.</p>
<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:24px 0 10px;color:var(--accent)">Why the league is unanimous</h2>
<p>Competitive CoD is won in the first tenth of a second of a gunfight, and Dynamic is simply the fastest curve to first response without giving up micro-adjustment. The result is on every page of this site: Dynamic response curve, Default aim assist, essentially without exception. There's no galaxy-brain alternative the pros are hiding — this is one of the rare settings with an actual right answer, and everyone converged on it years ago.</p>
<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:24px 0 10px;color:var(--accent)">Aim assist, briefly</h2>
<p>Default aim assist gives the standard slowdown bubble as your crosshair crosses a target. The alternative types trade that behavior for rotation styles that sound stronger on paper and test worse under pressure — which is why the league treats this the same as the curve: set it to Default and never think about it again. Spend your experimentation budget on sens and FOV, where preference actually exists; take the free answer here.</p>
</div>
"""

PRIVACY_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.75">
<p style="color:var(--muted);font-size:13px">Last updated: July 2026</p>
<p style="margin-top:14px">CODLOCKER is a static informational website. It does not require accounts, does not have login functionality, and does not ask for, collect, or store any personal information from visitors.</p>
<p style="margin-top:14px"><b>Hosting.</b> This site is hosted on GitHub Pages. Like most web hosts, GitHub may log basic technical information about visits (such as IP addresses) for security purposes. See <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" style="color:var(--accent)">GitHub's Privacy Statement</a> for details.</p>
<p style="margin-top:14px"><b>Fonts.</b> Pages load fonts from Google Fonts, which means your browser makes a request to Google's servers when the site loads. See <a href="https://policies.google.com/privacy" style="color:var(--accent)">Google's Privacy Policy</a> for how Google handles those requests.</p>
<p style="margin-top:14px"><b>Advertising and cookies.</b> This site uses Google AdSense to display advertising. Google and its partners may use cookies and similar technologies to serve ads, including personalized ads based on your visits to this and other websites. You can learn how Google uses data from sites like this one at <a href="https://policies.google.com/technologies/partner-sites" style="color:var(--accent)">policies.google.com/technologies/partner-sites</a>, and manage ad personalization at <a href="https://adssettings.google.com" style="color:var(--accent)">adssettings.google.com</a>. Users in the EEA/UK may be shown a consent prompt for personalized advertising.</p>
<p style="margin-top:14px"><b>Player information.</b> The site publishes gameplay-related information about professional Call of Duty League players (in-game settings and equipment) sourced from the players' own public streams, public chat commands, and public broadcasts.</p>
<p style="margin-top:14px">If this policy changes — for example, if analytics are added in the future — this page will be updated to reflect it.</p>
</div>
"""


# ── META CLASSES PAGE ───────────────────────────────────────────────
def classes_page():
    mc = DATA.get("metaClasses", {})
    title = "CDL Pro Meta Classes — MOD 15 & MPC Builds | CODLOCKER"
    desc  = "The exact MOD 15 and MPC classes CDL pros run in Black Ops 7 — attachments, build codes, and which players use each build."
    canonical = f"{SITE_URL}/classes.html"
    slug_by_tag = {p["tag"]: p["slug"] for p in PLAYERS}

    sections = []
    for w in mc.get("weapons", []):
        builds_html = []
        for b in w["builds"]:
            atts = "".join(f'<li style="font-size:12px;font-family:\'IBM Plex Mono\';background:var(--panel2);border:1px solid var(--line);padding:5px 10px">{esc(a)}</li>' for a in b["attachments"])
            sub = f'<p style="color:var(--muted);font-size:14px;margin-top:4px">{esc(b["sub"])}</p>' if b.get("sub") else ""
            code = ""
            if b.get("buildCode"):
                code = ('<div style="display:flex;align-items:center;gap:12px;margin-top:18px;flex-wrap:wrap">'
                        '<span style="font-family:\'Barlow Condensed\';font-size:12px;letter-spacing:.18em;color:var(--muted);text-transform:uppercase">Build code</span>'
                        f'<span style="font-family:\'IBM Plex Mono\';font-size:16px;color:var(--accent);background:#0d1014;border:1px solid var(--line);padding:6px 14px">{esc(b["buildCode"])}</span></div>')
            runby = ""
            if b.get("players"):
                links = ", ".join(
                    f'<a href="{slug_by_tag[t]}.html" style="color:var(--accent)">{esc(t)}</a>' if t in slug_by_tag else esc(t)
                    for t in b["players"])
                runby = ('<p style="margin-top:16px;color:var(--muted);font-size:14px">'
                         '<span style="font-family:\'Barlow Condensed\';font-size:12px;letter-spacing:.18em;text-transform:uppercase">Run by</span>'
                         f' &nbsp;{links}</p>')
            img_html = f'<img src="{esc(b["image"])}" alt="{esc(w["name"])} {esc(b["label"])} class Black Ops 7" style="width:100%;display:block;border-bottom:1px solid var(--line)" loading="lazy">' if b.get("image") else ""
            builds_html.append(f"""<div style="background:var(--panel);border:1px solid var(--line);clip-path:var(--chamfer);margin-bottom:22px">
{img_html}
<div style="padding:22px 26px 24px">
<h3 style="font-family:'Barlow Condensed';font-weight:700;font-size:24px;text-transform:uppercase;letter-spacing:.02em">{esc(b["label"])}</h3>
{sub}
<ul style="list-style:none;display:flex;flex-wrap:wrap;gap:9px;margin-top:16px;padding:0">{atts}</ul>
{code}
{runby}
</div>
</div>""")
        sections.append(f"""<section style="margin-bottom:52px">
<div style="display:flex;align-items:baseline;gap:14px;border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:20px">
<h2 style="font-family:'Barlow Condensed';font-weight:700;font-size:40px;text-transform:uppercase;line-height:1">{esc(w["name"])}</h2>
<span style="font-family:'Barlow Condensed';color:var(--accent);font-size:15px;letter-spacing:.18em;text-transform:uppercase">{esc(w["type"])}</span>
</div>
{"".join(builds_html)}
</section>""")

    note = f'<p class="notice" style="margin-bottom:26px">{esc(mc.get("note",""))}</p>' if mc.get("note") else ""

    return f"""{head(title, desc, canonical)}
<body style="--team:#FF7A1A">
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="index.html">← All players</a>
<div class="rail" style="margin-top:18px;background:var(--accent)"></div>
<h1 style="font-size:clamp(40px,7vw,72px)">Pro Meta Classes</h1>
<div class="sub"><span class="pagemeta">{esc(SEASON)} · What the league actually runs</span></div>
</div></div>
<section class="wrap" style="padding:30px 0 64px;max-width:820px">
{note}
{"".join(sections)}
</section>
{footer_html()}
</body></html>"""



# ── SHARE CARDS ─────────────────────────────────────────────────────
def generate_share_cards():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("PIL missing — skipping share cards"); return
    FDIR = os.path.join(ROOT,"data","fonts")
    if not os.path.isdir(FDIR):
        print("fonts missing — skipping share cards"); return
    fb = lambda s: ImageFont.truetype(os.path.join(FDIR,"BarlowCondensed-Bold.ttf"), s)
    fsb= lambda s: ImageFont.truetype(os.path.join(FDIR,"BarlowCondensed-SemiBold.ttf"), s)
    fm = lambda s: ImageFont.truetype(os.path.join(FDIR,"IBMPlexMono-Medium.ttf"), s)
    W,H = 1200,630
    for p in PLAYERS:
        s = p["settings"]
        if not any(s.get(k) is not None for k in ("horizontalSens","controller","fov")): continue
        team = TEAMS[p["team"]]
        col = tuple(int(team["color"][j:j+2],16) for j in (1,3,5))
        img = Image.new("RGB",(W,H),(10,12,15))
        d = ImageDraw.Draw(img)
        for x in range(0,W,56): d.line([x,0,x,H],fill=(18,21,25))
        for y in range(0,H,56): d.line([0,y,W,y],fill=(18,21,25))
        d.rectangle([0,0,14,H],fill=col)
        d.rectangle([0,H-12,W,H],fill=(255,122,26))
        d.text((70,64),"CODLOCKER",font=fsb(34),fill=(138,147,156))
        d.text((70,150),p["tag"].upper(),font=fb(150),fill=(242,245,247))
        d.text((74,320),team["name"].upper(),font=fsb(40),fill=col)
        x = 70; y=420
        stats=[]
        if s.get("horizontalSens") is not None: stats.append((str(s["horizontalSens"]),"SENS"))
        if s.get("fov") is not None: stats.append((str(s["fov"]),"FOV"))
        if s.get("buttonLayout"): stats.append((s["buttonLayout"].upper(),"LAYOUT"))
        for val,lbl in stats[:3]:
            d.text((x,y),val,font=fb(72),fill=(255,138,42))
            w = d.textlength(val,font=fb(72))
            d.text((x,y+82),lbl,font=fsb(24),fill=(90,100,110))
            x += max(int(w),120)+70
        d.text((70,H-70),"THECODLOCKER.COM",font=fm(26),fill=(242,245,247))
        img.save(os.path.join(OUT,f"og-{p['slug']}.png"))

# ── STATS PAGE ──────────────────────────────────────────────────────
def stats_page():
    tracked = [p for p in PLAYERS if p["settings"].get("horizontalSens") is not None]
    sens = [p["settings"]["horizontalSens"] for p in tracked]
    fovs = [p["settings"]["fov"] for p in tracked if p["settings"].get("fov") is not None]
    avg_s = sum(sens)/len(sens); avg_f = sum(fovs)/len(fovs)
    def brand(c):
        c=(c or "").lower()
        if "marius" in c: return "Marius"
        if "battle beaver" in c: return "Battle Beaver"
        if "scuf" in c: return "SCUF"
        if "demonwork" in c: return "Demonwork"
        if "dualsense" in c or "default" in c or "edge" in c: return "Sony (default/Edge)"
        if c: return "Other"
        return None
    from collections import Counter
    brands = Counter(b for b in (brand(p["settings"].get("controller")) for p in PLAYERS) if b)
    claws = sorted(p["tag"] for p in PLAYERS if p["settings"].get("grip")=="Claw")
    def laycat(l):
        l=(l or "")
        if not l: return None
        if "Tactical" in l or "Stick and Move" in l: return "Tactical family"
        if "Default" in l or "Standard" in l: return "Default family"
        return "Other (Bumper Jumper etc.)"
    lays = Counter(c for c in (laycat(p["settings"].get("buttonLayout")) for p in PLAYERS) if c)
    from collections import Counter as _C
    sens_bins = _C()
    for v in sens:
        sens_bins[round(v*20)/20] += 1
    def bar_rows(counter, color="var(--accent)"):
        if not counter: return ""
        mx = max(counter.values())
        rows=[]
        for k,v in sorted(counter.items(), key=lambda kv:(-kv[1],str(kv[0]))):
            pct = int(v/mx*100)
            rows.append(f'<div style="display:flex;align-items:center;gap:12px;margin:7px 0"><span style="width:170px;font-family:\'Barlow Condensed\';font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)">{esc(k)}</span><div style="flex:1;background:var(--panel2);height:20px;border:1px solid var(--line)"><div style="width:{pct}%;height:100%;background:{color}"></div></div><span style="font-family:\'IBM Plex Mono\';font-size:14px;width:28px;text-align:right">{v}</span></div>')
        return "".join(rows)
    def sens_hist():
        if not sens_bins: return ""
        mx=max(sens_bins.values())
        cells=[]
        for k in sorted(sens_bins):
            h=int(sens_bins[k]/mx*120)+8
            cells.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px"><span style="font-family:\'IBM Plex Mono\';font-size:11px;color:var(--muted)">{sens_bins[k]}</span><div style="width:34px;height:{h}px;background:var(--accent)"></div><span style="font-family:\'IBM Plex Mono\';font-size:12px">{k}</span></div>')
        return '<div style="display:flex;align-items:flex-end;gap:10px;flex-wrap:wrap;padding:10px 0">'+"".join(cells)+"</div>"
    # sortable table
    rows=[]
    for p in PLAYERS:
        s=p["settings"]; t=TEAMS[p["team"]]
        rows.append(f'<tr onclick="location.href=\'{p["slug"]}.html\'" style="cursor:pointer"><td style="color:{t["color"]};font-family:\'Barlow Condensed\';font-weight:700;text-transform:uppercase">{esc(p["tag"])}</td><td>{esc(t["name"])}</td><td data-v="{s.get("horizontalSens") or 0}">{esc(s.get("horizontalSens") or "—")}</td><td data-v="{s.get("fov") or 0}">{esc(s.get("fov") or "—")}</td><td>{esc(s.get("buttonLayout") or "—")}</td><td>{esc(s.get("grip") or "—")}</td><td>{esc(s.get("controller") or "—")}</td></tr>')
    table_js = """
document.querySelectorAll('#ptable th').forEach((th,i)=>{
  th.addEventListener('click',()=>{
    const tb=document.querySelector('#ptable tbody');
    const rows=[...tb.rows];
    const num=th.dataset.num==='1';
    const asc=th.dataset.asc!=='1';
    document.querySelectorAll('#ptable th').forEach(x=>x.dataset.asc='');
    th.dataset.asc=asc?'1':'';
    rows.sort((a,b)=>{
      let av,bv;
      if(num){av=parseFloat(a.cells[i].dataset.v||0);bv=parseFloat(b.cells[i].dataset.v||0);}
      else{av=a.cells[i].textContent.toLowerCase();bv=b.cells[i].textContent.toLowerCase();}
      return (av>bv?1:av<bv?-1:0)*(asc?1:-1);
    });
    rows.forEach(r=>tb.appendChild(r));
  });
});"""
    title="CDL Settings Stats — League Averages & Breakdowns | CODLOCKER"
    desc="League-wide Black Ops 7 settings statistics for the CDL: average sensitivity, FOV distribution, controller brands, claw grip count, and button layout breakdown."
    return f"""{head(title, desc, f"{SITE_URL}/stats.html")}
<body style="--team:#FF8A2A">
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="index.html">← All players</a>
<div class="rail" style="margin-top:18px;background:var(--accent)"></div>
<h1 style="font-size:clamp(40px,7vw,72px)">League Stats</h1>
<div class="sub"><span class="pagemeta">{esc(SEASON)} · Generated from {len(tracked)} tracked players</span></div>
</div></div>
<section class="wrap" style="padding:34px 0 64px;max-width:860px">
<p style="color:var(--muted);font-size:15px;line-height:1.8;margin-bottom:30px">These numbers are computed live from every verified player on the site — no estimates, no filler. They update automatically whenever a player's settings change, so this page always reflects the league as it currently plays. For what the individual settings mean and which are worth copying, see the <a href="settings-explained.html" style="color:var(--accent)">settings guide</a>.</p>
<div class="counters" style="margin:0 0 34px">
<div><b>{avg_s:.2f}</b><i>Avg sens</i></div>
<div><b>{avg_f:.0f}</b><i>Avg FOV</i></div>
<div><b>{len(claws)}</b><i>Claw players</i></div>
<div><b>{len(tracked)}/{len(PLAYERS)}</b><i>Tracked</i></div>
</div>
<div class="panel" style="margin-bottom:22px"><h2>Sensitivity distribution</h2>{sens_hist()}</div>
<div class="panel" style="margin-bottom:22px"><h2>Controller brands</h2>{bar_rows(brands)}</div>
<div class="panel" style="margin-bottom:22px"><h2>Button layout families</h2>{bar_rows(lays)}<p style="color:var(--muted);font-size:13px;margin-top:10px">Per the league's official player settings data where available.</p></div>
<div class="panel" style="margin-bottom:22px"><h2>Confirmed claw players</h2><p style="font-size:14px;line-height:2">{", ".join(f'<a href="{q.lower().replace(" ","-")}.html" style="color:var(--accent)">{esc(q)}</a>' for q in claws)}</p></div>
<div class="panel"><h2>Every player, sortable — click a column</h2>
<div style="overflow-x:auto"><table id="ptable" style="width:100%;border-collapse:collapse;font-size:13px">
<thead><tr>
<th style="cursor:pointer;text-align:left;padding:8px;border-bottom:1px solid var(--line);font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.08em;color:var(--muted)">Player</th>
<th style="cursor:pointer;text-align:left;padding:8px;border-bottom:1px solid var(--line);font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.08em;color:var(--muted)">Team</th>
<th data-num="1" style="cursor:pointer;text-align:left;padding:8px;border-bottom:1px solid var(--line);font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.08em;color:var(--muted)">Sens</th>
<th data-num="1" style="cursor:pointer;text-align:left;padding:8px;border-bottom:1px solid var(--line);font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.08em;color:var(--muted)">FOV</th>
<th style="cursor:pointer;text-align:left;padding:8px;border-bottom:1px solid var(--line);font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.08em;color:var(--muted)">Layout</th>
<th style="cursor:pointer;text-align:left;padding:8px;border-bottom:1px solid var(--line);font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.08em;color:var(--muted)">Grip</th>
<th style="cursor:pointer;text-align:left;padding:8px;border-bottom:1px solid var(--line);font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.08em;color:var(--muted)">Controller</th>
</tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
<style>#ptable td{{padding:8px;border-bottom:1px solid #1b2128}}#ptable tbody tr:hover{{background:#171d24}}</style>
</div>
</section>
{footer_html()}
<script>{table_js}</script>
</body></html>"""

# ── COMPARE PAGE ────────────────────────────────────────────────────
def compare_page():
    tracked = [p for p in PLAYERS if p["settings"].get("horizontalSens") is not None]
    pdata = {p["tag"]: {"team": TEAMS[p["team"]]["name"], "color": TEAMS[p["team"]]["color"], "slug": p["slug"], **p["settings"]} for p in tracked}
    fields = [("horizontalSens","Horizontal sens"),("verticalSens","Vertical sens"),("adsMultiplier","ADS multiplier"),("fov","FOV"),("responseCurve","Response curve"),("deadzoneLeftMin","Deadzone L min"),("deadzoneLeftMax","Deadzone L max"),("deadzoneRightMin","Deadzone R min"),("deadzoneRightMax","Deadzone R max"),("buttonLayout","Button layout"),("grip","Grip"),("controller","Controller")]
    title="Compare CDL Pro Settings Side by Side | CODLOCKER"
    desc="Pick any two CDL pros and compare their Black Ops 7 settings side by side — sens, FOV, deadzones, layouts and controllers."
    js = "const P=" + json.dumps(pdata) + ";const F=" + json.dumps(fields) + """;
const a=document.getElementById('pa'),b=document.getElementById('pb'),out=document.getElementById('cmp');
const names=Object.keys(P).sort((x,y)=>x.toLowerCase()<y.toLowerCase()?-1:1);
for(const n of names){a.add(new Option(n,n));b.add(new Option(n,n));}
a.value=names[0];b.value=names[1]||names[0];
function fmt(v){return (v===null||v===undefined||v==="")?"—":v}
function render(){
  const pa=P[a.value],pb=P[b.value];
  let h='<table style="width:100%;border-collapse:collapse;font-size:14px"><thead><tr><th></th>';
  h+=`<th style="padding:10px;color:${pa.color};font-family:'Barlow Condensed';font-size:22px;text-transform:uppercase"><a href="${pa.slug}.html" style="color:inherit">${a.value}</a><div style="font-size:11px;color:#8A939C;letter-spacing:.1em">${pa.team}</div></th>`;
  h+=`<th style="padding:10px;color:${pb.color};font-family:'Barlow Condensed';font-size:22px;text-transform:uppercase"><a href="${pb.slug}.html" style="color:inherit">${b.value}</a><div style="font-size:11px;color:#8A939C;letter-spacing:.1em">${pb.team}</div></th></tr></thead><tbody>`;
  for(const [k,label] of F){
    const va=fmt(pa[k]),vb=fmt(pb[k]);
    const diff=(va!=="—"&&vb!=="—"&&String(va)!==String(vb));
    h+=`<tr><td style="padding:9px;color:#8A939C;border-bottom:1px solid #1b2128">${label}</td>`;
    h+=`<td style="padding:9px;text-align:center;border-bottom:1px solid #1b2128;font-family:'IBM Plex Mono';font-size:13px;${diff?'color:#FF8A2A':''}">${va}</td>`;
    h+=`<td style="padding:9px;text-align:center;border-bottom:1px solid #1b2128;font-family:'IBM Plex Mono';font-size:13px;${diff?'color:#FF8A2A':''}">${vb}</td></tr>`;
  }
  out.innerHTML=h+'</tbody></table><p style="color:#4a525c;font-size:12px;margin-top:12px">Orange = the two players differ on that setting.</p>';
}
a.onchange=render;b.onchange=render;render();"""
    return f"""{head(title, desc, f"{SITE_URL}/compare.html")}
<body style="--team:#FF8A2A">
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="index.html">← All players</a>
<div class="rail" style="margin-top:18px;background:var(--accent)"></div>
<h1 style="font-size:clamp(40px,7vw,72px)">Compare Players</h1>
<div class="sub"><span class="pagemeta">Side-by-side settings for any two tracked pros</span></div>
</div></div>
<section class="wrap" style="padding:30px 0 64px;max-width:760px">
<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:22px">
<select id="pa" style="flex:1;min-width:200px;background:var(--panel);border:1px solid var(--line);color:var(--text);padding:11px 14px;font:inherit"></select>
<select id="pb" style="flex:1;min-width:200px;background:var(--panel);border:1px solid var(--line);color:var(--text);padding:11px 14px;font:inherit"></select>
</div>
<div class="panel" id="cmp"></div>
<p style="color:var(--muted);font-size:14px;line-height:1.8;margin-top:18px">Every value comes from the players' verified settings pages. Differences light up in orange — and if you compare enough pairs, a pattern emerges: pros at the very top of the game differ on almost everything inside the league's standard band, which is the strongest evidence that within that range, the right settings are the ones comfortable for you.</p>
</section>
{footer_html()}
<script>{js}</script>
</body></html>"""


# ── TEAM PAGES ──────────────────────────────────────────────────────
def team_page(key):
    t = TEAMS[key]
    roster = [p for p in PLAYERS if p["team"] == key]
    tracked = [p for p in roster if p["settings"].get("horizontalSens") is not None]
    title = f'{t["name"]} Player Settings — CDL 2026 | CODLOCKER'
    desc = f'Controller settings, sensitivity, FOV and layouts for the full {t["name"]} roster in the 2026 Call of Duty League season.'
    canonical = f'{SITE_URL}/{key}.html'

    # written intro from the data
    parts = [f'{t["name"]} field a {len(roster)}-player roster in the 2026 CDL season, and CODLOCKER has verified settings for {len(tracked)} of them.' if tracked else f'{t["name"]} field a {len(roster)}-player roster in the 2026 CDL season; verified settings for the roster are still being confirmed.']
    if len(tracked) >= 2:
        svals = [p["settings"]["horizontalSens"] for p in tracked]
        lo, hi = min(svals), max(svals)
        if lo == hi:
            parts.append(f'The whole tracked roster plays on a {lo} sensitivity.')
        else:
            parts.append(f'Sensitivities on the team run from {lo} up to {hi}, all inside the band nearly the entire league occupies.')
        fovs = [p["settings"]["fov"] for p in tracked if p["settings"].get("fov")]
        if fovs:
            parts.append(f'FOVs range {min(fovs)}–{max(fovs)}.' if min(fovs)!=max(fovs) else f'Everyone tracked runs a {fovs[0]} FOV.')
    claws = [p["tag"] for p in roster if p["settings"].get("grip")=="Claw"]
    if claws:
        parts.append(("Claw grip is represented by " + ", ".join(claws) + ".") if len(claws)>1 else f"{claws[0]} plays claw.")
    intro = "<p>" + " ".join(parts) + " Click any player for their full settings sheet — deadzones, controller, layout and update history.</p>"

    def row(p):
        s = p["settings"]
        return f'<tr onclick="location.href=\'{p["slug"]}.html\'" style="cursor:pointer"><td style="font-family:\'Barlow Condensed\';font-weight:700;text-transform:uppercase;font-size:17px"><a href="{p["slug"]}.html" style="color:var(--text)">{esc(p["tag"])}</a></td><td>{esc(s.get("horizontalSens") or "—")}</td><td>{esc(s.get("fov") or "—")}</td><td>{esc(s.get("buttonLayout") or "—")}</td><td>{esc(s.get("grip") or "—")}</td></tr>'

    table = ('<div class="panel" style="margin-top:24px"><div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:14px">'
             '<thead><tr>' + "".join(f'<th style="text-align:left;padding:9px;border-bottom:1px solid var(--line);font-family:\'Barlow Condensed\';text-transform:uppercase;letter-spacing:.08em;color:var(--muted)">{h}</th>' for h in ["Player","Sens","FOV","Layout","Grip"]) + '</tr></thead>'
             '<tbody>' + "".join(row(p) for p in roster) + '</tbody></table></div>'
             '<style>td{padding:9px;border-bottom:1px solid #1b2128}tbody tr{transition:background .1s ease}tbody tr:hover{background:#171d24;outline:2px solid var(--team);outline-offset:-2px}tbody tr:hover td:first-child a{color:var(--team)}</style></div>')

    return f"""{head(title, desc, canonical)}
<body style="--team:{t['color']}">
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="index.html">← All players</a>
<div class="rail"></div>
<h1 style="font-size:clamp(40px,7vw,76px)">{esc(t["name"])}</h1>
<div class="sub"><span class="pagemeta">{esc(SEASON)} · {len(tracked)}/{len(roster)} tracked</span></div>
</div></div>
<section class="wrap" style="padding:30px 0 64px;max-width:860px;color:var(--muted);font-size:15px;line-height:1.8">
{intro}
{table}
</section>
{footer_html()}
</body></html>"""

GUIDE_COMFORT_BODY = """
<div style="color:var(--text);font-size:15px;line-height:1.8">
<p>The most common question this site gets asked, one way or another: should I just copy a pro's settings? The honest answer is more useful than a yes or no — and the data on this site makes the case better than opinion can.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">Settings matter — up to a boundary</h2>
<p>Look across every tracked player on this site and a clear pattern shows up: nearly the entire league plays inside a fairly narrow band. Sensitivity between roughly 1.6 and 1.9. FOV between about 98 and 105. Dynamic response curve, default aim assist, deadzones at or near 1/75 and 3/99. That convergence is not a coincidence — it's dozens of full-time professionals, competing for real money, independently arriving at the same neighborhood. Settings far outside that band carry a genuine cost: a 4.0 sensitivity makes micro-adjustments unrepeatable; a bottomed-out FOV blinds you to flanks. In that sense, settings absolutely matter, and the league's band tells you where the functional range is.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">Inside the boundary, it's preference — and the pros prove it</h2>
<p>Here's the part people miss: within that band, the diversity is everywhere. Players at the very top of the game run 1.6 and 1.9 against each other. Some split horizontal and vertical sens; most don't. FOVs span the whole 98–105 window on the same rosters. Layouts range across Default, Tactical, flipped variants, and one lone Bumper Jumper. Some of the best players alive claw; teammates of theirs with identical trophies don't. If there were one objectively correct configuration inside the band, the most competitive controller players on earth would have found it and converged on it. They haven't — because inside the functional range, the differences are comfort, not correctness.</p>

<h2 style="font-family:'Barlow Condensed';font-size:26px;text-transform:uppercase;margin:28px 0 10px;color:var(--accent)">What to actually do</h2>
<p>Use the pros to find the range, and use yourself to find the spot. Pick a sensitivity inside 1.6–1.9 — a favorite player's number is a fine starting point — and an FOV around 100. Then play, adjust toward what feels natural, and once it feels right, stop touching it. Consistency beats optimization: the pro whose settings you copied has run essentially the same numbers for years, and that stability is a bigger part of their aim than the numbers themselves. Constantly cycling settings in search of a magic configuration is worse than settling on comfortable ones, because your aim never gets to build on a stable foundation.</p>

<p style="margin-top:14px">So copy the band, not the player. The range on this site is the league's collective answer to what works; where you land inside it should be yours.</p>
</div>
"""


# ── NEWS ────────────────────────────────────────────────────────────
NEWS_ARTICLES = [
 {"slug":"ewc-2026-paris-bo7-finale","date":"2026-08-07",
  "title":"EWC Is Live in Paris — and It's the Last BO7 Event Ever",
  "teaser":"16 teams, $1.8 million, and the final tournament of the Black Ops 7 era. What's at stake and what we're watching.",
  "body":"""
<p>The Esports World Cup's Call of Duty bracket is running right now at the Paris Expo, August 5 through 9. Group stage first, two groups of eight, then a single-elim playoff over the weekend. $1.8 million in the pool.</p>
<p style="margin-top:14px">Two storylines carry the event. FaZe just won Champs in Vegas three weeks ago and can close the season with the double — CDL title and EWC in the same month. OpTic are the defending EWC champs from last year and lost that Vegas final 5–2, so they've got their own reasons. Falcons, Gentle Mates and 100 Thieves round out the teams people actually expect to make noise.</p>
<p style="margin-top:14px">The bigger deal, honestly: this is the last professional Black Ops 7 event, period. Once Paris wraps on the 9th, the game's competitive era is over and Modern Warfare 4 takes the calendar. Every setting on this site — every sens, every deadzone tune, every GA'd build — is a snapshot of a game that's about to be history.</p>
<p style="margin-top:14px">Which also means the fun part is coming. New game, new settings menus, new metas, and a couple months of pros figuring their setups out in public. We'll be tracking all of it here from day one of MW4. Until then: enjoy the last weekend of BO7.</p>
"""},
 {"slug":"deadzone-data-2026","date":"2026-07-26",
  "title":"The Deadzone Data: What the League Actually Runs",
  "teaser":"We did a precision pass on deadzones across the league. The standard everyone quotes isn't the standard.",
  "body":"""
<p>Ask anyone what pros run for deadzones and you'll hear the same answer: 1/75 left, 3/99 right. We just finished going player by player and that answer is wrong, or at least lazy.</p>
<p style="margin-top:14px">The actual norm on the left stick minimum is 0. Not 1. Shotzzy, Simp, HyDra, Mercules, aBeZy, Nastie, 04, Neptune, Exnid — all of them bottom it out completely. No buffer at all. That works because they're on fresh custom controllers that don't drift. Copy it on a year-old pad and you'll be spinning in the spawn.</p>
<p style="margin-top:14px">Left-stick maxes are all over the place too. <a href="alluka.html" style="color:var(--accent)">Alluka</a> caps at 60, <a href="sib.html" style="color:var(--accent)">Sib</a> and <a href="nium.html" style="color:var(--accent)">Nium</a> at 65, <a href="kips.html" style="color:var(--accent)">Kips</a> and <a href="abezy.html" style="color:var(--accent)">aBeZy</a> at 70. That just means full movement input kicks in before the stick hits the edge. Right-stick minimums run anywhere from 2 to 5 depending on the player, and <a href="ghosty.html" style="color:var(--accent)">Ghosty</a> is doing his own thing entirely — 3/99 on both sticks.</p>
<p style="margin-top:14px">Takeaway: deadzones are the most personal setting in the game. Sens and FOV cluster hard. Deadzones don't, because they're tuned to a specific physical controller in a specific condition. Exact values for every tracked player are on their pages.</p>
"""},
 {"slug":"faze-vegas-champs-2026-settings","date":"2026-07-20",
  "title":"FaZe Vegas Won It All. Their Settings Are Boring. That's the Point.",
  "teaser":"The world champions play on numbers half the league uses. What that tells you about copying pros.",
  "body":"""
<p>FaZe Vegas are your 2026 world champions — 5–2 over OpTic in the Vegas grand final, no three-peat. Simp took MVP for his third ring, first player to get three without all of them coming on OpTic. First rings for Abuzah and 04. Second for Drazah.</p>
<p style="margin-top:14px">So what do the champions play on? Nothing special, and that's the honest headline. <a href="simp.html" style="color:var(--accent)">Simp</a>: 1.7 both sticks, 100 FOV, Marius. <a href="abuzah.html" style="color:var(--accent)">Abuzah</a>: 1.65, claw. <a href="04.html" style="color:var(--accent)">04</a>: 1.7 at 102. <a href="drazah.html" style="color:var(--accent)">Drazah</a>: 1.7 at 100 on a Battle Beaver. You could swap those numbers with the team they beat and nobody would notice.</p>
<p style="margin-top:14px">People go looking for the secret in the settings. There isn't one. The gap between winning and losing that final lived somewhere settings can't reach. If anything, the champions' numbers being this ordinary is the strongest argument for the advice we keep giving: take a number from inside the league's band, get comfortable, stop fiddling.</p>
<p style="margin-top:14px">All four sheets are on their player pages, deadzones and hardware included.</p>
"""},
 {"slug":"two-build-league","date":"2026-07-22",
  "title":"The Two-Build League",
  "teaser":"The entire competitive weapon meta is three builds. Here's how it got that narrow.",
  "body":"""
<p>The full list of guns the pros run: two Mod 15 setups and one MPC. That's it. That's the meta.</p>
<p style="margin-top:14px">It gets that narrow because of GAs — gentlemen's agreements. On top of the official CDL ruleset, the teams collectively ban whatever attachments and weapons they decide are unhealthy for competition. Nobody enforces it but everybody honors it, and by the time the bans settle each season there's almost nothing left to choose from.</p>
<p style="margin-top:14px">The two Mod 15 builds differ on exactly one slot that matters. The Quickstep Foregrip version — <a href="huke.html" style="color:var(--accent)">Huke</a>, <a href="hydra.html" style="color:var(--accent)">HyDra</a>, <a href="cellium.html" style="color:var(--accent)">Cellium</a> run it — buys movement. The Fusion Barrel version — <a href="dashy.html" style="color:var(--accent)">Dashy</a>, <a href="scrap.html" style="color:var(--accent)">Scrap</a>, <a href="renkor.html" style="color:var(--accent)">RenKoR</a> — spends the slot on range instead. Same sight, same grip, same stock. It comes down to role and taste, not one being correct.</p>
<p style="margin-top:14px">Both builds plus the MPC class are on the <a href="classes.html" style="color:var(--accent)">classes page</a> with import codes. Type the code in gunsmith and you're running exactly what they run.</p>
"""},
]

def news_article_page(a):
    title = f'{a["title"]} | CODLOCKER'
    canonical = f'{SITE_URL}/{a["slug"]}.html'
    return f"""{head(title, a["teaser"], canonical)}
<body style="--team:#FF8A2A">
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="news.html">← All news</a>
<div class="rail" style="margin-top:18px;background:var(--accent)"></div>
<h1 style="font-size:clamp(32px,5.4vw,54px);line-height:1.02">{esc(a["title"])}</h1>
<div class="sub"><span class="pagemeta">{esc(a["date"])} · CODLOCKER</span></div>
</div></div>
<section class="wrap" style="padding:32px 0 64px;max-width:760px;color:var(--text);font-size:15px;line-height:1.85">
{a["body"]}
</section>
{footer_html()}
</body></html>"""

def news_index_page():
    title = "News & Analysis | CODLOCKER"
    desc = "Settings analysis and CDL news from CODLOCKER — what the league runs and what changed."
    cards = ""
    for a in sorted(NEWS_ARTICLES, key=lambda x: x["date"], reverse=True):
        cards += f"""<a href="{a["slug"]}.html" style="display:block;background:var(--panel);border:1px solid var(--line);clip-path:var(--chamfer);padding:24px 28px;margin-bottom:16px;color:var(--text)">
<span style="font-family:'IBM Plex Mono';font-size:12px;color:var(--accent)">{esc(a["date"])}</span>
<h2 style="font-family:'Barlow Condensed';font-weight:700;font-size:27px;text-transform:uppercase;line-height:1.06;margin-top:6px">{esc(a["title"])}</h2>
<p style="color:var(--muted);font-size:14px;margin-top:8px">{esc(a["teaser"])}</p>
</a>"""
    return f"""{head(title, desc, f"{SITE_URL}/news.html")}
<body style="--team:#FF8A2A">
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="index.html">← All players</a>
<div class="rail" style="margin-top:18px;background:var(--accent)"></div>
<h1 style="font-size:clamp(40px,7vw,72px)">News &amp; Analysis</h1>
<div class="sub"><span class="pagemeta">{esc(SEASON)}</span></div>
</div></div>
<section class="wrap" style="padding:32px 0 64px;max-width:820px">
{cards}
</section>
{footer_html()}
</body></html>"""


# ── UPDATES LOG ─────────────────────────────────────────────────────
def updates_page():
    title = "Settings Update Log | CODLOCKER"
    desc = "A running log of when each CDL pro's settings were last confirmed or changed on CODLOCKER."
    dated = sorted([p for p in PLAYERS if p.get("lastUpdated")], key=lambda p: p["lastUpdated"], reverse=True)
    from itertools import groupby
    groups = ""
    for date_key, items in groupby(dated, key=lambda p: p["lastUpdated"]):
        rows = ""
        for p in items:
            t = TEAMS[p["team"]]
            rows += f'<a href="{p["slug"]}.html" style="display:flex;gap:12px;align-items:baseline;padding:7px 0;border-bottom:1px dotted #1b2128;color:var(--text)"><span style="font-family:\'Barlow Condensed\';font-weight:700;text-transform:uppercase;font-size:17px;color:{t["color"]}">{esc(p["tag"])}</span><span style="color:var(--muted);font-size:13px">{esc(t["name"])} — settings confirmed or revised</span></a>'
        groups += f'<div style="margin-bottom:26px"><h2 style="font-family:\'IBM Plex Mono\';font-size:15px;color:var(--accent);margin-bottom:8px">{esc(date_key)}</h2>{rows}</div>'
    return f"""{head(title, desc, f"{SITE_URL}/updates.html")}
<body style="--team:#FF8A2A">
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="index.html">← All players</a>
<div class="rail" style="margin-top:18px;background:var(--accent)"></div>
<h1 style="font-size:clamp(38px,6.5vw,64px)">Update Log</h1>
<div class="sub"><span class="pagemeta">Every confirmation and revision, by date</span></div>
</div></div>
<section class="wrap" style="padding:30px 0 64px;max-width:760px">
<p style="color:var(--muted);font-size:14px;line-height:1.8;margin-bottom:26px">Pros change settings constantly. This log shows when each player's page last had values confirmed or revised, newest first — if a player you follow isn't recent, their settings simply haven't changed (or changed somewhere we haven't caught yet: <a href="contact.html" style="color:var(--accent)">tips welcome</a>).</p>
{groups}
</section>
{footer_html()}
</body></html>"""


def guides_hub_page():
    title = "Settings Guides | CODLOCKER"
    desc = "Guides to every Black Ops 7 controller setting — sensitivity, FOV, deadzones, response curves, build codes — grounded in what CDL pros actually run."
    entries = [
        ("settings-explained.html","Pro Settings, Explained","Every setting on a player page — what it does, what the league runs, what's worth copying."),
        ("deadzones-guide.html","Deadzones, Properly","Min and max thresholds, why most pros run a 0 left min, and how to tune yours."),
        ("fov-guide.html","FOV: The Real Tradeoff","Information versus target size, and why the league lives between 98 and 105."),
        ("curves-guide.html","Response Curves & Aim Assist","What Dynamic actually does and why the entire league runs it."),
        ("settings-comfort.html","Do Settings Matter?","The case for copying the band, not the player."),
        ("build-codes.html","Build Codes","How to import the pros' exact classes in seconds."),
    ]
    cards = "".join(f'''<a href="{u}" style="display:block;background:var(--panel);border:1px solid var(--line);padding:22px 26px;margin-bottom:14px;color:var(--text)">
<h2 style="font-family:'Barlow Condensed';font-weight:700;font-size:25px;text-transform:uppercase">{t}</h2>
<p style="color:var(--muted);font-size:14px;margin-top:6px">{s}</p></a>''' for u,t,s in entries)
    return f"""{head(title, desc, f"{SITE_URL}/guides.html")}
<body style="--team:#FF8A2A">
{header_html()}
<div class="lower-third"><div class="wrap">
<a class="back" href="index.html">← All players</a>
<div class="rail" style="margin-top:18px;background:var(--accent)"></div>
<h1 style="font-size:clamp(40px,7vw,72px)">Settings Guides</h1>
<div class="sub"><span class="pagemeta">Grounded in what the league actually runs</span></div>
</div></div>
<section class="wrap" style="padding:32px 0 64px;max-width:820px">
{cards}
</section>
{footer_html()}
</body></html>"""

# ── SITEMAP / ROBOTS ────────────────────────────────────────────────
def sitemap():
    today = date.today().isoformat()
    urls = [f"<url><loc>{SITE_URL}/</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/classes.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/stats.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/settings-comfort.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/verify.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/guides.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/deadzones-guide.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/fov-guide.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/curves-guide.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/news.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/updates.html</loc><lastmod>{today}</lastmod></url>",
            *[f"<url><loc>{SITE_URL}/{_a['slug']}.html</loc><lastmod>{_a['date']}</lastmod></url>" for _a in NEWS_ARTICLES],
            *[f"<url><loc>{SITE_URL}/{_tk}.html</loc><lastmod>{today}</lastmod></url>" for _tk in TEAM_ORDER],
            f"<url><loc>{SITE_URL}/compare.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/settings-explained.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/build-codes.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/about.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/contact.html</loc><lastmod>{today}</lastmod></url>",
            f"<url><loc>{SITE_URL}/privacy.html</loc><lastmod>{today}</lastmod></url>"]
    for p in PLAYERS:
        if any(p["settings"].get(k) is not None for k in ("horizontalSens","controller","fov")):
            urls.append(f"<url><loc>{SITE_URL}/{p['slug']}.html</loc><lastmod>{today}</lastmod></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")

# ── BUILD ───────────────────────────────────────────────────────────
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(index_page())
for p in PLAYERS:
    with open(os.path.join(OUT, p["slug"] + ".html"), "w") as f:
        f.write(player_page(p))
for _tk in TEAM_ORDER:
    with open(os.path.join(OUT, _tk + ".html"), "w") as f:
        f.write(team_page(_tk))
with open(os.path.join(OUT, "settings-comfort.html"), "w") as f:
    f.write(static_page("Do Pro Settings Actually Matter? Finding Your Range", "Why CDL pros converge on a settings band, why the diversity inside it proves preference matters, and how to pick what is comfortable for you.", "settings-comfort", "Do Settings Matter?", GUIDE_COMFORT_BODY))
with open(os.path.join(OUT, "stats.html"), "w") as f:
    f.write(stats_page())
with open(os.path.join(OUT, "compare.html"), "w") as f:
    f.write(compare_page())
generate_share_cards()
with open(os.path.join(OUT, "classes.html"), "w") as f:
    f.write(classes_page())
with open(os.path.join(OUT, "guides.html"), "w") as f:
    f.write(guides_hub_page())
with open(os.path.join(OUT, "deadzones-guide.html"), "w") as f:
    f.write(static_page("Deadzones in Black Ops 7 — What CDL Pros Run & How to Tune Yours", "How min and max deadzones work, why most pros run a 0 left-stick minimum, and how to set yours by hardware, not by copying.", "deadzones-guide", "Deadzones, Properly", GUIDE_DEADZONE_BODY))
with open(os.path.join(OUT, "fov-guide.html"), "w") as f:
    f.write(static_page("Best FOV in Black Ops 7 — What CDL Pros Use & Why", "The FOV tradeoff explained with the league's actual range: why pros cluster between 98 and 105 and how to pick within it.", "fov-guide", "FOV: The Real Tradeoff", GUIDE_FOV_BODY))
with open(os.path.join(OUT, "curves-guide.html"), "w") as f:
    f.write(static_page("Response Curve & Aim Assist in Black Ops 7 — The Pro Standard", "What Dynamic response curve does, why the whole CDL runs it with Default aim assist, and what that means for your settings.", "curves-guide", "Response Curves & Aim Assist", GUIDE_CURVES_BODY))
with open(os.path.join(OUT, "settings-explained.html"), "w") as f:
    f.write(static_page("CDL Pro Settings Explained — Sens, FOV, Deadzones & Layouts", "What every controller setting on a CDL pro page means, what the league runs, and what is worth copying.", "settings-explained", "Pro Settings, Explained", GUIDE_SETTINGS_BODY))
with open(os.path.join(OUT, "build-codes.html"), "w") as f:
    f.write(static_page("Black Ops 7 Build Codes — How to Import Pro Classes", "What build codes are, how to import the CDL pro Mod 15 and MPC classes, and why the whole league runs the same builds.", "build-codes", "Build Codes, Explained", GUIDE_CODES_BODY))
with open(os.path.join(OUT, "updates.html"), "w") as f:
    f.write(updates_page())
with open(os.path.join(OUT, "news.html"), "w") as f:
    f.write(news_index_page())
for _a in NEWS_ARTICLES:
    with open(os.path.join(OUT, _a["slug"] + ".html"), "w") as f:
        f.write(news_article_page(_a))
with open(os.path.join(OUT, "verify.html"), "w") as f:
    f.write(static_page("How CODLOCKER Verifies Pro Settings", "Where every number on CODLOCKER comes from: players' own streams, official league data, and event broadcasts — never guesses.", "verify", "How We Verify", VERIFY_BODY))
with open(os.path.join(OUT, "404.html"), "w") as f:
    f.write(static_page("Page Not Found — CODLOCKER", "That page does not exist. Browse every CDL pro instead.", "404", "Page Not Found", '<div style="color:var(--muted);font-size:15px;line-height:1.8"><p>That page doesn\'t exist — the player may have left the league, or the link is old.</p><p style="margin-top:14px"><a href="index.html" class="herocta" style="margin-top:6px">Browse every player →</a></p></div>'))
with open(os.path.join(OUT, "about.html"), "w") as f:
    f.write(static_page("About CODLOCKER — CDL Pro Settings", "What CODLOCKER is, how settings are sourced and verified.", "about", "About CODLOCKER", ABOUT_BODY))
with open(os.path.join(OUT, "contact.html"), "w") as f:
    f.write(static_page("Contact — CODLOCKER", "Send settings updates and corrections to CODLOCKER.", "contact", "Contact", CONTACT_BODY))
with open(os.path.join(OUT, "privacy.html"), "w") as f:
    f.write(static_page("Privacy Policy — CODLOCKER", "CODLOCKER privacy policy.", "privacy", "Privacy Policy", PRIVACY_BODY))
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write(sitemap())
for _im in os.listdir(os.path.join(ROOT, "data", "img")):
    shutil.copy(os.path.join(ROOT, "data", "img", _im), os.path.join(OUT, _im))
shutil.copy(os.path.join(ROOT, "data", "favicon.png"), os.path.join(OUT, "favicon.png"))
shutil.copy(os.path.join(ROOT, "data", "logo.png"), os.path.join(OUT, "logo.png"))
shutil.copy(os.path.join(ROOT, "data", "favicon.ico"), os.path.join(OUT, "favicon.ico"))
with open(os.path.join(OUT, "ads.txt"), "w") as f:
    f.write("google.com, pub-4248859491912544, DIRECT, f08c47fec0942fa0\n")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")

print(f"Built site/ — index + {len(PLAYERS)} player pages + sitemap")
