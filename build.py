import json, os, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'dist')
CDN = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/'
steam = json.load(open(os.path.join(ROOT, 'steam.json')))
e = html.escape

# ---------- data ----------
ONLINE = [
    # slug, name, appid, score, rec, review
    ('outer-wilds', 'Outer Wilds', '753640', 9.5, 'Recommended',
     "This seems weird to put in a detective category, but the amount of deduction you have to do to find all pieces of the puzzle is enough to place it in this category. The game is also top notch!"),
    ('return-of-the-obra-dinn', 'Return of the Obra Dinn', '653530', 9, 'Recommended',
     "If you want a game where you have to do everything yourself, you get zero hints, no handholding and only a small tutorial at the start. Return of the Obra Dinn is definitely for you."),
    ('the-incident-at-galley-house', 'The Incident at Galley House', '3641000', 8.5, 'Recommended',
     "A nice investigation game, with a lot of mystery surrounding it. Voice acting, story, the feeling, the deduction part. They were all on point in my opinion."),
    ('duck-detective-the-secret-salami', 'Duck Detective: The Secret Salami', '2637990', 8, 'Recommended',
     "A cozy detective game with nice voice overs, it's a mix of comedy and drama. Fun game, maybe not as hard as other games on this list, but it gets my approval because of the overall style."),
    ('the-rise-of-the-golden-idol', 'The Rise of the Golden Idol', '2716400', 8, 'Recommended',
     "Sequel to The Case of the Golden Idol, so the gameplay is the same, but I like the modern vibe of the game. It also has some new types of puzzles that are enjoyable."),
    ('the-case-of-the-golden-idol', 'The Case of the Golden Idol', '1677770', 7.5, 'Recommended',
     "A 'frozen painting' investigation game where you have to complete sentences to find out what happened. It has a compelling story, even if there isn't voice acting."),
    ('duck-detective-the-ghost-of-glamping', 'Duck Detective: The Ghost of Glamping', '2714620', 7.5, 'Recommended',
     "The sequel in the Duck Detective series. Honestly I found the story of the first game more compelling. This one has a more creepy and supernatural undertone to it, but still good enough."),
    ('unheard', 'Unheard', '942970', 7.5, 'Recommended',
     "Where a lot of games focus on the visuals, UNHEARD is all about the sounds. You're playing on a top down map, so you can't follow all conversations together."),
    ('shadows-of-doubt', 'Shadows of Doubt', '986130', 6.5, 'Not for me',
     "Is it me or is it so difficult to catch one perpetrator in this game? I like the amount of freedom you get and the endless possibilities, but it only got me hooked for a while."),
    ('the-painscreek-killings', 'The Painscreek Killings', '624270', 6, 'Recommended',
     "More of an 'investigation mystery' game. The deduction part was on the low side in my opinion, it was a lot of searching and walking. I liked the story though."),
    ('overboard', 'Overboard!', '1546920', 6, 'Not for me',
     "A game where you are the murderer and have to get away with it. It wasn't really my forte. Replaying the game to find other options didn't suit me, I wanted to see a 'reverse time' mechanic."),
    ('the-diary', 'The Diary', '2343880', 5, 'Not for me',
     "You don't need a lot of deductive reasoning in this game. The diary is the main piece of content you interact with. It has this cozy cutout feeling to it, but it's not really detective material."),
    ('the-roottrees-are-dead', 'The Roottrees are Dead', '2754380', 8.5, 'Recommended',
     "You search for information on an in-game web browser to fill in a giant family tree. This game is no walk in the park, I couldn't complete it without looking at hints online. Still a very good game with a lot of secrets, and big enough for a real detective mind. Completing the whole game can be hard, but it's worth playing."),
]
HERO = {'753640', '653530', '3641000', '2637990', '2716400'}

# Games that carry the "Deduction Detective" tag
DETECTIVE = {'outer-wilds', 'return-of-the-obra-dinn', 'the-incident-at-galley-house', 'duck-detective-the-secret-salami',
             'the-rise-of-the-golden-idol', 'the-case-of-the-golden-idol', 'duck-detective-the-ghost-of-glamping',
             'unheard', 'the-roottrees-are-dead'}

# Not played yet: (name, steam appid, header path). Shown as "Under investigation", no page.
UPCOMING_ON = [
    ('Funeral for the Sun', '4088360', '4133ea3727c30395a6f6c6d3ed94eee63319650e/header.jpg?t=1794138405'),
    ('Mystery of the Malign', '3521490', '76b89c86bb472699e202f4cf99fdf656b03b5008/header.jpg?t=1793361798'),
    ('Psycho-Sleuth', '3432860', '33e3be2e4a8757667a6d1faa894ab7ec954c6c01/header.jpg?t=1793883448'),
    ('Legion Was Here', '3492120', '2d1de35b4953a8fe26bbbe6d6f22b83f2e271549/header.jpg?t=1788930612'),
    ('Detective Grimoire', '272600', 'header.jpg?t=1771579460'),
    ('The Operator', '1771980', 'header.jpg'),
    ('Murdered: Soul Suspect', '233290', 'header.jpg'),
]
NOW = UPCOMING_ON[3]  # currently playing: Legion Was Here (shown on the paper in the home hero)
UPCOMING_OFF = []  # offline games still to play; the panel stays hidden while this is empty

BGG = 'https://cf.geekdo-images.com/'
OFFLINE = [
    # slug, name, kind, players, time, note, img, case
    ('deception-murder-in-hong-kong', 'Deception: Murder in Hong Kong', 'Party', '4 to 12', '20 min',
     "The ideal detective game if you don't have a lot of players, but still want a good cat-and-mouse feel. In my opinion it's best with a lower amount of players, like 5 or 6, so everyone is more involved.",
     BGG + '1COY3oeK9aN2_XNimKaNww__itemrep/img/cAOvicFEw8eQs6D9b2G4E7MTp00=/fit-in/246x300/filters:strip_icc()/pic3033330.jpg', 'Case 03'),
    ('hidden-games-de-case-klein-apelroos', 'Hidden Games: De Case Klein-Apelroos', 'Box case', '1 to 6', '90 to 180 min',
     "My first physical case file: an envelope full of evidence and a few questions to solve. It's really fun to play with a small group and puzzle all clues together, but getting all evidence right at the beginning feels overwhelming. Overall it's worth it.",
     BGG + 'NFN-oNosuQqhPc-FYv4PAw__itemrep/img/Wqnu7w0r0Kqh0S-PBmtnCvp_lfQ=/fit-in/246x300/filters:strip_icc()/pic6163740.jpg', 'Reel'),
    ('dead-of-winter', 'Dead of Winter', 'Board game', '2 to 5', '60 to 120 min',
     "The game has strong RPG elements, which makes it very immersive. 3 to 4 players is perfect. You can also play with a traitor, which makes it much harder. I recommend playing with allies only.",
     BGG + 'g4mV4BH-ZrhMUVgil-yV1A__itemrep/img/Tc76KEZmrLgCrsvhQAW36iv7x9E=/fit-in/246x300/filters:strip_icc()/pic3016500.jpg', 'Case 05'),
    ('spyfall-2', 'Spyfall 2', 'Party', '3 to 12', '15 min',
     "Perfect as an icebreaker for game nights, or for larger groups that don't want a lot of rules. Easy, everyone can play.",
     BGG + '4nE3EGcIVJnItZOdZ2NrxA__itemrep/img/QYIEqFna0OPNhS6xUxM9o_jIiGc=/fit-in/246x300/filters:strip_icc()/pic4141398.jpg', 'Case 001'),
    ('the-werewolves-of-millers-hollow', "The Werewolves of Miller's Hollow", 'Party', '8 to 18', '30 min',
     "Easy, but you need to know the roles beforehand because they're not written on the cards. With enough cards, the only limit is your room capacity.",
     BGG + 'rZ0tOafAt1oue_7NKqELsg__itemrep/img/8Ku8ENBwf0oH1uWnMMoXKkRIRe0=/fit-in/246x300/filters:strip_icc()/pic7203269.jpg', 'Case 002'),
]

LOG = [
    ('29 Aug 2026', 'Online', 'Reviewed The Incident at Galley House. 8,5/10.', '/game.html?g=the-incident-at-galley-house'),
    ('29 Aug 2026', 'Online', 'Reviewed Shadows of Doubt. 6,5/10, not for me.', '/game.html?g=shadows-of-doubt'),
    ('29 Aug 2026', 'Online', 'Reviewed Duck Detective: The Ghost of Glamping. 7,5/10.', '/game.html?g=duck-detective-the-ghost-of-glamping'),
    ('22 Nov 2025', 'Offline', 'Case 05: Dead of Winter.', '/box.html?g=dead-of-winter'),
    ('16 Nov 2025', 'Online', 'Case 04: The Roottrees are Dead. 8,5/10.', '/game.html?g=the-roottrees-are-dead'),
]

def sc(s):
    if s is None: return 'Not scored yet'
    return (('%g' % s).replace('.', ',')) + '/10'

def banner(appid): return CDN + appid + '/' + steam[appid]['h']
def hero(appid): return CDN + appid + '/library_hero.jpg'
def shots(appid): return [CDN + appid + '/' + s for s in steam[appid]['s']]

# ---------- layout ----------
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&family=Special+Elite&family=Courier+Prime:wght@400;700&display=swap">'

def page(title, active, body, desc='Deduction games on screen and on the table, reviewed by Gumshoematt.'):
    def nav(href, label, key):
        cls = ' class="on"' if key == active else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#0E1A16"><meta name="color-scheme" content="dark">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
{FONTS}<link rel="stylesheet" href="/style.css"></head>
<body><div class="grain">
<header class="top"><nav class="wrap nav">
<a class="logo" href="/">gumshoematt</a>
<div class="links">{nav('/', 'Home', 'home')}{nav('/online.html', 'Online games', 'online')}{nav('/offline.html', 'Offline games', 'offline')}<a class="follow" href="https://www.instagram.com/gumshoematt/">Follow Instagram</a><a class="follow" href="https://www.tiktok.com/@gumshoemattyt">Follow TikTok</a></div>
</nav></header>
{body}
<footer class="foot"><div class="wrap">
<div class="foot-row"><p class="tape big">Follow the trail.</p>
<div class="btns"><a class="btn ghost" href="https://www.instagram.com/gumshoematt/">Instagram</a><a class="btn ghost" href="https://www.tiktok.com/@gumshoemattyt">TikTok</a><a class="btn ghost" href="https://linktr.ee/gumshoematt">All links</a></div></div>
<div class="foot-meta"><span>© 2026 Gumshoematt</span><span>Game images belong to their publishers. No hints, no handholding.</span></div>
</div></footer>
</div><script src="/site.js"></script></body></html>'''

def online_card(g):
    slug, name, appid, s, rec, _ = g
    det = slug in DETECTIVE
    kind = 'Deduction Detective' if det else 'Other'
    tag = '<span class="tag">DEDUCTION DETECTIVE</span>' if det else ''
    return f'''<a class="card newsprint" href="/game.html?g={slug}" data-kind="{kind}" data-score="{s if s is not None else -1}" data-name="{e(name)}">
<img src="{banner(appid)}" alt="{e(name)}" loading="lazy" class="ban">
{tag}<span class="name">{e(name)}</span>
<span class="row"><span class="score">{sc(s)}</span><span class="more">Open file →</span></span></a>'''

def offline_card(o):
    slug, name, kind, players, time, note, img, case = o
    return f'''<a class="card newsprint" href="/box.html?g={slug}" data-kind="{e(kind)}" data-score="-1" data-name="{e(name)}">
<span class="boxwrap"><img class="bw-bg" src="{img}" alt="" aria-hidden="true" loading="lazy"><img class="bw-main" src="{img}" alt="{e(name)}" loading="lazy"></span>
<span class="tag">{e(kind.upper())} · {e(players)} PLAYERS</span>
<span class="row"><span class="name">{e(name)}</span><span class="score small">Not scored yet</span></span></a>'''

def filters(kinds, sorts):
    k = ''.join(f'<button type="button" class="chip{" on" if i == 0 else ""}" data-filter="{e(x)}">{e(x)}</button>' for i, x in enumerate(kinds))
    s = ''.join(f'<button type="button" class="sort{" on" if i == 0 else ""}" data-sort="{v}">{l}</button>' for i, (v, l) in enumerate(sorts))
    return f'<div class="filterbar"><div class="chips">{k}</div><div class="sorts"><span>Sort</span>{s}</div></div>'

DICT = '''<section class="wrap dict"><div class="dictentry newsprint"><p class="dhead"><b class="hw">Deduction detective</b><i>noun</i></p><p class="def">A game that makes you think. Hints are rare, so it's up to you to collect the clues, connect the dots and find the culprit.</p></div></section>'''

def up_url(u): return CDN + u[1] + '/' + u[2]

def upcoming_slips(items, label):
    if not items: return ''
    s = ''.join(f'''<div class="slip kraft"><img src="{up_url(u)}" alt="" loading="lazy"><span class="name">{e(u[0])}</span><span class="pending">Under investigation</span></div>''' for u in items)
    return f'<span class="eyebrow">{label}</span><div class="slips">{s}</div>'

def upcoming_panel(eyebrow, title, items):
    if not items: return ''
    cards = ''.join(f'''<div class="card newsprint"><img src="{up_url(u)}" alt="{e(u[0])}" loading="lazy" class="ban"><span class="name">{e(u[0])}</span><span class="row"><span class="score small">Under investigation</span></span></div>''' for u in items)
    return f'''<section class="band"><div class="wrap archive"><div><span class="eyebrow">{eyebrow}</span><h2 class="big">{e(title)}</h2></div><p class="growing">Games I'm going to play. No verdict yet.</p><div class="grid">{cards}</div></div></section>'''

# ---------- home ----------
def home():
    top3 = ONLINE[:3]
    on = ''.join(f'''<a class="slip newsprint" href="/game.html?g={g[0]}"><img src="{banner(g[2])}" alt="" loading="lazy"><span class="name">{e(g[1])}</span><span class="stamp">{sc(g[3])}</span></a>''' for g in top3)
    off = ''.join(f'''<a class="slip kraft" href="/box.html?g={o[0]}"><img src="{o[6]}" alt="" loading="lazy" class="boxthumb"><span class="name">{e(o[1])}</span><span class="pending">Not scored yet</span></a>''' for o in OFFLINE[:2])
    log = ''.join(f'''<a class="logrow" href="{h}"><span class="date">{d}</span><span class="pill">{k.upper()}</span><span class="txt">{e(t)}</span><span class="more">Open →</span></a>''' for d, k, t, h in LOG)
    body = f'''
<section class="wrap hero-home">
<div class="col">
<div class="subjectwrap" id="subjectwrap" tabindex="0">
<div class="paper newsprint" aria-label="Currently playing: {e(NOW[0])}"><img src="{up_url(NOW)}" alt="" loading="lazy"><div class="ptxt"><span class="pnow">Currently playing</span><span class="pname">{e(NOW[0])}</span></div></div>
<div class="kraft subject"><div class="tab"></div>
<div class="subject-head"><span>SUBJECT FILE</span></div>
<div class="photo"><img src="/img/gumshoematt-desk.jpg" alt="Gumshoematt at his detective desk, on the phone"></div>
<div class="subject-foot"><span class="who">Gumshoematt</span><span class="redstamp">DETECTIVE WANNABE</span></div></div></div>
<h1>Playing detective,<br><em>or doing the work?</em></h1>
<p class="lede">I play deduction games on screen and on the table, and I tell you which ones are worth your evening. My picks, my scores.</p>
<p class="stats">{len(ONLINE)} online games on file · {len(OFFLINE)} on the table</p>
</div>
<div class="col">
<div class="head-line"><h2>Start here</h2><span>The best of both worlds</span></div>
<span class="eyebrow">ON SCREEN</span><div class="slips">{on}</div>
<span class="eyebrow">ON THE TABLE</span><div class="slips">{off}</div>
<div class="legend newsprint"><strong>How I score</strong><span>9–10 must play</span><span>7–8 worth your evening</span><span>6 or lower: not for me</span></div>
</div>
</section>
<section class="band"><div class="wrap split">
<div class="intro"><span class="eyebrow">CASE LOG</span><h2 class="big">Latest updates</h2><p class="muted">What I played, what I scored, what got added to the files.</p></div>
<div class="log newsprint">{log}</div></div></section>'''
    return page('Gumshoematt: detective games, reviewed', 'home', body)

# ---------- online ----------
def online():
    top = ONLINE[:5]
    tilts = [-4, -2, 0, 2, 4]
    bgs = ''.join(f'<img class="bg" data-i="{i}" src="{hero(g[2])}" alt="" aria-hidden="true">' for i, g in enumerate(top))
    folders = ''.join(f'''<a class="folder kraft" href="/game.html?g={g[0]}" data-i="{i}" data-name="{e(g[1])}" data-score="{sc(g[3])}" style="--t:{tilts[i]}deg;--l:{abs(i-2)*8}px;z-index:{10-abs(i-2)}"><span class="ftab">No. {i+1:03d}</span><img class="ficon" src="{banner(g[2])}" alt=""><span class="fname">{e(g[1])}</span><span class="fmore">Open file ↗</span></a>''' for i, g in enumerate(top))
    mob = ''.join(f'''<a class="mcard kraft" href="/game.html?g={g[0]}"><img src="{banner(g[2])}" alt="{e(g[1])}" loading="lazy"><span class="row"><span class="name">{e(g[1])}</span><span class="score">{sc(g[3])}</span></span></a>''' for g in top)
    cards = ''.join(online_card(g) for g in ONLINE)
    panel = upcoming_panel('UPCOMING · ON SCREEN', 'Waiting in evidence', UPCOMING_ON)
    body = f'''
<section class="files-hero desk">{bgs}<div class="shade"></div>
<div class="wrap fh-inner"><div class="fh-text"><span class="eyebrow" id="fh-eyebrow">FILE B · ON SCREEN</span><h1 id="fh-title">The best on file.</h1><span class="fh-score" id="fh-score"></span></div>
<div class="folders">{folders}</div></div></section>
<section class="wrap mob mlist"><span class="eyebrow">FILE B · ON SCREEN</span><h1>The best on file.</h1>{mob}</section>
{DICT}
<section class="band"><div class="wrap archive">
<div><span class="eyebrow">THE ARCHIVE</span><h2 class="big">Every game on file</h2></div>
{filters(['All', 'Deduction Detective'], [('score', 'Score'), ('name', 'A to Z')])}
<p class="growing">This shelf is still growing. {len(ONLINE)} games on file so far.</p>
<div class="grid" data-grid>{cards}</div></div></section>
{panel}'''
    return page('Online detective games | Gumshoematt', 'online', body)

# ---------- offline ----------
def offline():
    rings = '<span></span>' * 6
    cards = []
    n = len(OFFLINE)
    for i, o in enumerate(OFFLINE):
        slug, name, kind, players, time, note, img, case = o
        cls = 'kraft' if i % 2 == 0 else 'newsprint'
        cards.append(f'''<article class="flipcard {cls}" data-i="{i}" style="z-index:{n-i}"><div class="holes">{rings}</div>
<div class="fc-in"><div class="fc-img"><img class="fc-bg" src="{img}" alt="" aria-hidden="true"><img class="fc-main" src="{img}" alt="{e(name)}"><span class="tape">{e(kind.upper())}</span></div>
<div class="fc-body"><span class="eyebrow dark">CASE No. {i+1:03d}</span><h2>{e(name)}</h2><p>{e(note)}</p>
<div class="facts3"><div><span>PLAYERS</span>{e(players)}</div><div><span>TIME</span>{e(time)}</div><div><span>MY SCORE</span><b>Not scored yet</b></div></div>
<a class="btn solid" href="/box.html?g={slug}">Open the file →</a></div></div></article>''')
    mob = ''.join(f'''<a class="mcard kraft" href="/box.html?g={o[0]}"><span class="boxwrap"><img class="bw-bg" src="{o[6]}" alt="" aria-hidden="true" loading="lazy"><img class="bw-main" src="{o[6]}" alt="{e(o[1])}" loading="lazy"></span><span class="row"><span class="name">{e(o[1])}</span><span class="score small">Not scored yet</span></span></a>''' for o in OFFLINE)
    grid = ''.join(offline_card(o) for o in OFFLINE)
    panel = upcoming_panel('UPCOMING · ON THE TABLE', 'Next on the desk', UPCOMING_OFF)
    body = f'''
<section class="wrap pagehead desk"><span class="eyebrow">FILE A · ON THE TABLE</span><h1>The best on the table.</h1><p class="lede">Box cases, murder mysteries and party deduction I'd put on your table first. Flip through the stack.</p></section>
<section class="wrap stackwrap desk">
<div class="stack-ctrl"><span id="stack-pos">File 1 of {n}</span><div><button type="button" class="btn ghost" id="prev" aria-label="Previous file">←</button><button type="button" class="btn dark" id="next">Flip →</button></div></div>
<div class="stack" id="stack"><div class="rings">{rings}</div>{''.join(cards)}
<div class="stack-end"><p class="tape big">That's the whole stack.</p><button type="button" class="btn ghost" id="restart">Back to the top</button></div></div>
</section>
<section class="wrap mob mlist"><span class="eyebrow">FILE A · ON THE TABLE</span><h1>The best on the table.</h1>{mob}</section>
<section class="band"><div class="wrap archive">
<div><span class="eyebrow">THE ARCHIVE</span><h2 class="big">Every game on file</h2></div>
{filters(['All', 'Box case', 'Party', 'Board game'], [('name', 'A to Z')])}
<p class="growing">This shelf is still growing. {len(OFFLINE)} games on file so far.</p>
<div class="grid" data-grid>{grid}</div></div></section>
{panel}'''
    return page('Offline detective games | Gumshoematt', 'offline', body)

# ---------- game pages ----------
def game_page(i, g):
    slug, name, appid, s, rec, review = g
    st = steam[appid]
    related = sorted([x for x in ONLINE if x[0] != slug and x[3] is not None], key=lambda x: abs((x[3]) - (s if s is not None else 8)))[:3]
    rel = ''.join(f'''<a class="card newsprint" href="/game.html?g={x[0]}"><img src="{banner(x[2])}" alt="{e(x[1])}" loading="lazy" class="ban"><span class="row"><span class="name">{e(x[1])}</span><span class="score">{sc(x[3])}</span></span></a>''' for x in related)
    ev = ''.join(f'<a href="{u}" target="_blank" rel="noopener"><img src="{u}" alt="{e(name)} screenshot {k+1}" loading="lazy"></a>' for k, u in enumerate(shots(appid)))
    verdict = {'Recommended': 'RECOMMENDED', 'Not for me': 'NOT FOR ME', 'On file': 'ON FILE'}[rec]
    body = f'''
<div class="wrap crumbs"><a href="/online.html">← Online games</a><span> / Case No. {i+1:03d}</span></div>
<section class="wrap gtop">
<div class="gbanner"><img src="{banner(appid)}" alt="{e(name)}"><span class="tape">CASE No. {i+1:03d} · ON SCREEN</span></div>
<div class="ghead"><span class="eyebrow">{e(st['dev'].upper())} · {e(st['rel'])}</span><h1>{e(name)}</h1>
<div class="scorecard kraft"><span class="lbl">GUMSHOE SCORE</span><span class="num">{sc(s).replace('/10','') if s is not None else '?'}<small>/10</small></span><span class="verdict">{verdict}</span></div></div>
</section>
<section class="wrap gbody">
<div class="take"><span class="eyebrow">MY TAKE</span><p>{e(review)}</p><span class="sig">Matthias</span></div>
<div class="facts"><div><span>DEVELOPER</span>{e(st['dev'])}</div><div><span>RELEASED</span>{e(st['rel'])}</div><div><span>MY VERDICT</span>{e(rec)}</div></div>
<div><span class="eyebrow">EVIDENCE</span><div class="evidence">{ev}</div></div>
<div class="btns"><a class="btn solid light" href="https://store.steampowered.com/app/{appid}/">Get it on Steam →</a><a class="btn ghost" href="https://store.steampowered.com/curator/46277857/">Follow my Steam curator page</a></div>
</section>
<section class="band"><div class="wrap archive"><h2 class="mid">Related cases</h2><div class="grid">{rel}</div></div></section>'''
    return [f'{name}: review | Gumshoematt', body]

def offline_page(i, o):
    slug, name, kind, players, time, note, img, case = o
    others = ''.join(offline_card(x) for x in OFFLINE if x[0] != slug)[:]
    body = f'''
<div class="wrap crumbs"><a href="/offline.html">← Offline games</a><span> / {e(case)}</span></div>
<section class="wrap gtop">
<div class="gbox kraft"><img src="{img}" alt="{e(name)}"><span class="tape">{e(kind.upper())}</span></div>
<div class="ghead"><span class="eyebrow">ON THE TABLE · {e(case.upper())}</span><h1>{e(name)}</h1>
<div class="scorecard kraft"><span class="lbl">GUMSHOE SCORE</span><span class="num pend">Not scored yet</span></div></div>
</section>
<section class="wrap gbody">
<div class="take"><span class="eyebrow">MY TAKE</span><p>{e(note)}</p><span class="sig">Matthias</span></div>
<div class="facts"><div><span>TYPE</span>{e(kind)}</div><div><span>PLAYERS</span>{e(players)}</div><div><span>TIME</span>{e(time)}</div></div>
<div class="btns"><a class="btn ghost" href="https://www.instagram.com/gumshoematt/">See the post on Instagram</a></div>
</section>
<section class="band"><div class="wrap archive"><h2 class="mid">More on the table</h2><div class="grid">{others}</div></div></section>'''
    return [f'{name} | Gumshoematt', body]

# ---------- write ----------
def w(path, text):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(text)

shutil.rmtree(OUT, ignore_errors=True)

# Free demos: (name, steam appid of the full game, note, played: True/False)
DEMOS = []

def demos():
    if DEMOS:
        cards = ''.join(f'''<a class="card newsprint" href="https://store.steampowered.com/app/{d[1]}/" data-kind="{'Played' if d[3] else 'Not played yet'}" data-score="-1" data-name="{e(d[0])}">
<img src="{CDN}{d[1]}/header.jpg" alt="{e(d[0])}" loading="lazy" class="ban">
<span class="tag">{'PLAYED' if d[3] else 'NOT PLAYED YET'} · FREE DEMO</span><span class="name">{e(d[0])}</span>
<span class="note">{e(d[2])}</span><span class="row"><span class="score small">Free</span><span class="more">Try it on Steam →</span></span></a>''' for d in DEMOS)
    else:
        cards = '<p class="empty newsprint">No demos on file yet. The first ones are on their way.</p>'
    body = f'''
<section class="wrap pagehead"><span class="eyebrow">FILE C · FREE TO TRY</span><h1>Free demos.</h1><p class="lede">Detective game demos you can play for free. Try the case before you buy the game.</p></section>
<section class="band"><div class="wrap archive">
<div><span class="eyebrow">THE ARCHIVE</span><h2 class="big">Every demo on file</h2></div>
{filters(['All', 'Played', 'Not played yet'], [('name', 'A to Z')])}
<p class="growing">This shelf is still growing. {len(DEMOS)} demos on file so far.</p>
<div class="grid" data-grid>{cards}</div></div></section>'''
    return page('Free detective game demos | Gumshoematt', 'demos', body)

w('index.html', home()); w('online.html', online()); w('offline.html', offline())
compact = {
 'cdn': CDN,
 'g': [[g[0], g[1], g[2], g[3], g[4], g[5], steam[g[2]]['h'], steam[g[2]]['dev'], steam[g[2]]['rel'], steam[g[2]]['s'], steam[g[2]].get('price','')] for g in ONLINE],
 'checked': '9 Nov 2026',
 'b': [list(o) for o in OFFLINE]}
w('data.js', 'window.GM=' + json.dumps(compact, separators=(',', ':'), ensure_ascii=False) + ';')
shell = page('Gumshoematt', '{ACTIVE}', '<main id="gm-page"></main>').replace('<script src="/site.js"></script>', '<script src="/data.js"></script><script src="/site.js"></script>')
w('game.html', shell.replace('{ACTIVE}', 'x').replace('<a href="/online.html">', '<a href="/online.html" class="on">'))
w('box.html', shell.replace('{ACTIVE}', 'x').replace('<a href="/offline.html">', '<a href="/offline.html" class="on">'))
shutil.copytree(os.path.join(ROOT, 'img'), os.path.join(OUT, 'img')); shutil.copy(os.path.join(ROOT, 'style.css'), OUT); shutil.copy(os.path.join(ROOT, 'site.js'), OUT)
open(os.path.join(OUT, 'vercel.json'), 'w').write(json.dumps({'cleanUrls': False}))
print('built', sum(len(f) for _, _, f in os.walk(OUT)), 'files')
