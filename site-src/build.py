#!/usr/bin/env python3
"""Builds the Jackass Meshworks static site into ../jm-site.

Pages share one header/footer. Plugins live in PLUGINS below: add an entry and a
page function to add a product. Output is plain HTML, no build step on Cloudflare.
"""
import pathlib, html, hashlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "site"
SITE = "https://www.jackassmeshworks.com"
EMAIL = "support@jackassmeshworks.com"
YEAR = 2026

# ---- Plugins (order = order on the Plugins page) -------------------------------
PLUGINS = [
    {
        "slug": "clonesensor",
        "name": "CloneSensor",
        "accent": "#ffa300",          # CloneSensor orange (text accents)
        "accent2": "#9d00ef",         # CloneSensor purple (buttons, badges)
        "bg": "#1a1421",              # page background behind the horseshoes
        "peek": "assets/clonesensor/peek-purple.webp",  # corner donkey tinted to match
        "pattern_wash": 0.5,          # 0 = full-strength horseshoes, 1 = hidden
        "font": "Saira",
        "logo": "assets/clonesensor/logo-light.svg",
        "type_logo": "assets/clonesensor/type.svg",   # wordmark for the plugin card
        "animated_icon": True,
        "card_blurb": "Scatter clones across any surface with zero overlaps. Every clone is tested before it's placed.",
        "pitch": "Every clone is tested before it's placed. No movement. No jitter. No overlaps.",
        "intro": "CloneSensor places clones on a surface so they never occupy the same space. Each candidate is tested first: if the space is free, the clone is kept and that space is closed. If not, the candidate is thrown away. Nothing gets pushed apart afterward.",
        "status": "beta",
        "platforms": ["C4D"],
        "beta_url": "https://265069153872.gumroad.com/l/wznxwn",
        "beta_label": "Get the Free Beta",
        "requires": "Free beta · Version 1.0",
        "demo": {"mp4": "assets/clonesensor/clonesensor-demo.mp4", "poster": "assets/clonesensor/demo-poster.jpg", "controls": True},
        "card_media": None,
        "features": [
            ("Tested placement", "Each clone's shape is checked against space already reserved. A fit is kept, an overlap is discarded."),
            ("Repeatable results", "The same seed, Max Count, settings and surface give the same clones. Every time."),
            ("Seven sampling modes", "Random, Poisson Disk, Blue Noise, Grid, Hex Packing, Vertex and Polygon Center."),
            ("Layout presets", "Crowd, Seating, Festival, Parking and Booths, in real-world sizes for your project units."),
            ("Collision shapes", "Sphere, Bounding Box or Footprint, tested in 3D or along the surface, sized per asset or from a shared radius."),
            ("Keep away", "Edges, splines and fields refuse a point before any clone is made."),
            ("Fill Surface", "One click fills the whole surface. Spread Across Surface reaches separate floors and regions."),
            ("Rules engine", "Categories, weights, priorities and clearance between groups, measured instead of guessed."),
            ("Flexible output", "Instances, points or cloners, with viewport overlays and full solve statistics."),
        ],
        "benefits": [
            "No more hand-nudging intersecting clones before a render.",
            "Crowds, seating, festival grounds, parking and booth layouts from one generator.",
            "Same seed, same layout, so revisions and handoffs stay predictable.",
            "Works in centimeters, meters, feet, or whatever units the project uses.",
        ],
        "title": "CloneSensor for Cinema 4D (Free Beta)",
        "description": "CloneSensor is a predictive placement plugin for Cinema 4D. Every clone is tested before it's placed: no movement, no jitter, no overlaps. Free beta.",
    },
]

LOGO_DARK = "assets/jm-logo-black.webp"   # tan pages
LOGO_LIGHT = "assets/jm-logo-light.webp"  # dark product pages
PEEKS = {"plugins": "assets/peek-plugins.webp", "contact": "assets/peek-color.webp",
         "product": "assets/peek-dark.webp", "404": "assets/peek-color.webp"}
import json
BADGE = json.loads((pathlib.Path(__file__).parent / "badge.json").read_text())

CSS_V = hashlib.md5((OUT / "css/site.css").read_bytes()).hexdigest()[:8]

NAV = [("Home", "/"), ("Plugins", "/plugins"), ("About", "/about"), ("Contact", "/contact")]

e = html.escape


def head(title, description, path, accent=None, extra_font=None):
    full = title if title.startswith("Jackass Meshworks") else f"{title} | Jackass Meshworks"
    url = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jackass Meshworks">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{accent or '#9e987d'}">
<link rel="icon" href="/assets/favicon.png" type="image/png">\n<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700{('&amp;family=' + extra_font + ':wght@400;600;700') if extra_font else ''}&amp;display=swap">
<link rel="stylesheet" href="/css/site.css?v={CSS_V}">
</head>"""


def header(current, dark=False):
    src = LOGO_LIGHT if dark else LOGO_DARK
    logo = (f'<img src="/{src}" width="199" height="61" alt="Jackass Meshworks">' if src
            else '<span class="ph-logo" aria-label="Jackass Meshworks"><b>Jackass</b><span>Meshworks</span></span>')
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if label == current else ""}>{label}</a>'
        for label, href in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <a class="logo" href="/">{logo}</a>
  <nav class="nav" aria-label="Main">{links}</nav>
</header>"""


def body_open(cls="", style="", peek=False):
    classes = " ".join(x for x in [cls, "has-peek" if peek else ""] if x)
    return f'\n<body{f" class=\"{classes}\"" if classes else ""}{f" style=\"{style}\"" if style else ""}>\n'


def footer(peek=None):
    src = PEEKS.get(peek, peek)
    p = f'\n<img class="peek" src="/{src}" alt="" width="602" height="630" decoding="async">' if peek else ""
    return f"""<footer class="site-footer"><p>&copy; {YEAR} Jackass Meshworks &middot; All rights reserved</p></footer>{p}
</body>
</html>
"""


def badge():
    """Layered donkey badge drawn from the parts in JM_LOGO_ANI_PARTS.ai.
    Circle is native SVG; each part is a small WebP so the CSS can animate it."""
    c = BADGE["circle"]
    def part(n, cls=""):
        m = BADGE[n]
        return f'<image class="{cls}" href="/assets/badge/{n}.webp" x="{m["x"]}" y="{m["y"]}" width="{m["w"]}" height="{m["h"]}"/>'
    return f"""<svg class="badge" viewBox="0 0 1100 1100" role="img" aria-label="The Jackass Meshworks donkey">
      <defs><clipPath id="badge-clip"><circle cx="{c['cx']}" cy="{c['cy']}" r="{c['R']}"/><rect x="0" y="0" width="1100" height="{c['cy']}"/></clipPath></defs>
      <g class="b-circle"><circle cx="{c['cx']}" cy="{c['cy']}" r="{(c['r']+c['R'])/2}" fill="#44542d" stroke="#000" stroke-width="{c['R']-c['r']+6}"/></g>
      <g clip-path="url(#badge-clip)"><g class="b-rise">
        {part('neck')}
        <g class="b-ear-l"><g class="b-flick">{part('ear-l')}</g></g>
        <g class="b-ear-r"><g class="b-flick">{part('ear-r')}</g></g>
        {part('head')}
        {part('tuft')}
        {part('lids', 'b-lids')}
      </g></g>
    </svg>"""


CS_ICON = json.loads((pathlib.Path(__file__).parent / "cs_icon.json").read_text())
CS_CX, CS_CY = 1922.5, 477.4          # center of the sensor rings
CS_ORDER = [4, 0, 6, 2, 7, 1, 5, 3]   # shuffled pop-in order of the 8 clones


def cs_icon(mode="loop", uid="cs"):
    """CloneSensor icon, animated from the real icon paths.
    loop: dot pings twice, outer ring locks on, clones pop in at random, hold, reset (7s).
    once: same build-up in 3.4s, then stays complete (product page)."""
    loop = mode == "loop"
    dur = 7.0 if loop else 3.4
    pct = (lambda sec: f"{sec / dur * 100:.2f}%")
    css = []
    # pings: thin rings that grow out from the sensor and fade
    ping_starts = [0.15, 0.75, 1.35, 1.95] if loop else [0.05, 0.45, 0.85]
    ping_life = 1.3 if loop else 0.9
    for i, t in enumerate(ping_starts):
        a, b = pct(t), pct(min(t + ping_life, dur))
        css.append(f"@keyframes {uid}-ping{i}{{0%,{a}{{transform:scale(1);opacity:0}}"
                   f"{pct(t + .02)}{{opacity:.9}}{b}{{transform:scale(9);opacity:0}}100%{{transform:scale(9);opacity:0}}}}"
                   f".{uid} .p{i}{{animation:{uid}-ping{i} {dur}s linear {'infinite' if loop else '1 both'}}}")
    # outer ring locks on after the pings
    ring_t = 2.2 if loop else 1.15
    end = (f"{pct(6.25)}{{opacity:1;transform:none}}{pct(6.6)},100%{{opacity:0;transform:scale(.9)}}" if loop
           else "100%{opacity:1;transform:none}")
    css.append(f"@keyframes {uid}-ring{{0%,{pct(ring_t)}{{opacity:0;transform:scale(1.35)}}"
               f"{pct(ring_t + .35)}{{opacity:1;transform:none}}{end}}}"
               f".{uid} .ring{{animation:{uid}-ring {dur}s cubic-bezier(.2,1.3,.4,1) {'infinite' if loop else '1 both'}}}")
    # clones pop in one at a time, in shuffled order
    c0, step = (2.6, 0.32) if loop else (1.45, 0.2)
    for rank, idx in enumerate(CS_ORDER):
        t = c0 + rank * step
        end = (f"{pct(6.25)}{{opacity:1;transform:none}}{pct(6.6)},100%{{opacity:0;transform:scale(.6)}}" if loop
               else "100%{opacity:1;transform:none}")
        css.append(f"@keyframes {uid}-c{idx}{{0%,{pct(t)}{{opacity:0;transform:scale(.2)}}"
                   f"{pct(t + .12)}{{opacity:1;transform:scale(1.18)}}{pct(t + .26)}{{transform:none}}{end}}}"
                   f".{uid} .c{idx}{{animation:{uid}-c{idx} {dur}s ease-out {'infinite' if loop else '1 both'}}}")
    # the dot gives a small pulse each time it pings
    css.append(f".{uid} .dot{{animation:{uid}-dot {ping_starts[1]-ping_starts[0]:.2f}s ease-out {len(ping_starts)} both}}"
               f"@keyframes {uid}-dot{{0%{{transform:scale(1)}}25%{{transform:scale(1.12)}}100%{{transform:none}}}}")
    css.append(f".{uid} g,.{uid} path,.{uid} circle{{transform-box:fill-box;transform-origin:center}}"
               f"@media (prefers-reduced-motion:reduce){{.{uid} *{{animation:none!important;opacity:1}}.{uid} .ping{{display:none}}}}")
    o = CS_ICON["orange"]; pu = CS_ICON["purple"]
    pings = "".join(f'<circle class="ping p{i}" cx="{CS_CX}" cy="{CS_CY}" r="142" fill="none" stroke="#ffa300" stroke-width="3" vector-effect="non-scaling-stroke" opacity="0"/>'
                    for i in range(len(ping_starts)))
    clones = "".join(f'<path class="c{i}" fill="#9d00ef" d="{x["d"]}"/>' for i, x in enumerate(pu))
    vb = '-1700 -440 5800 3280' if loop else '0 0 2400 2400'
    return (f'<svg class="cs-icon cs-{mode} {uid}" viewBox="{vb}" role="img" aria-label="CloneSensor icon">'
            f'<style>{"".join(css)}</style>{pings}'
            f'<path class="ring" fill="#ffa300" d="{o[1]["d"]}"/><path class="dot" fill="#ffa300" d="{o[0]["d"]}"/>{clones}</svg>')


def video(media, cls, alt):
    if not media:
        return f'<div class="{cls}"><div class="ph" style="height:100%">{e(alt)}</div></div>'
    attrs = 'controls playsinline preload="none"' if media.get("controls") else 'autoplay muted loop playsinline preload="metadata"'
    return (f'<div class="{cls}"><video {attrs} '
            f'poster="/{media["poster"]}" aria-label="{e(alt)}"><source src="/{media["mp4"]}" type="video/mp4"></video></div>')


def write(name, text):
    (OUT / name).write_text(text)


# ---- Pages ----------------------------------------------------------------------
def home():
    write("index.html", head("Jackass Meshworks", "Forensic-grade workflow tools for 3D artists. Cinema 4D plugins built by a small workshop.", "/")
          + '\n<body>\n' + header("Home") + f"""
<main id="main">
  <section class="hero">
    {badge()}
    <h1 class="tagline">Forensic-grade workflow tools for 3D artists.</h1>
  </section>
</main>
""" + footer())


def about():
    write("about.html", head("About", "Jackass Meshworks builds clean, reliable tools and workflows for motion designers working in Cinema 4D and After Effects.", "/about")
          + '\n<body>\n' + header("About") + f"""
<main id="main">
  <section class="hero">
    {badge()}
    <h1 class="lede">Jackass Meshworks builds clean, reliable tools and workflows for motion designers. Everything here is designed to reduce friction, improve clarity, and make your Cinema 4D and After Effects pipelines faster and more organized.</h1>
  </section>
</main>
""" + footer())


def contact():
    write("contact.html", head("Contact", "Questions, ideas, or bug reports for Jackass Meshworks. Every note goes straight to the creator.", "/contact")
          + body_open(peek=True) + header("Contact") + f"""
<main id="main">
  <section class="contact">
    <h1 class="lede">Got a question, idea, or issue? Drop me a message. Jackass Meshworks is a small workshop, so every note goes straight to the creator.</h1>
    <a class="email" href="mailto:{EMAIL}">{EMAIL}</a>
  </section>
</main>
""" + footer(peek="contact"))


def plugins_page():
    cards = []
    for p in PLUGINS:
        pills = ""  # platform pills (C4D etc.) hidden on cards for now
        if p["status"] == "beta":
            pills += '<span class="pill pill-accent">Beta</span>'
        cards.append(f"""    <a class="card" href="/{p['slug']}" style="--card-accent:{p['accent']}">
      {('<div class="card-media card-media-icon">' + cs_icon('loop', 'csl') + '</div>') if p.get('animated_icon') else video(p['card_media'], 'card-media', p['name'] + ' preview')}
      <div class="card-body">
        <h2>{(f'<img src="/{p["type_logo"]}" width="705" height="106" alt="{e(p["name"])}">') if p.get('type_logo') else e(p['name'])}</h2>
        <p>{e(p['card_blurb'])}</p>
        <div class="pills">{pills}</div>
      </div>
    </a>""")
    write("plugins.html", head("Plugins", "Cinema 4D plugins from Jackass Meshworks. CloneSensor, predictive clone placement, is now in free beta.", "/plugins")
          + body_open(peek=True) + header("Plugins") + """
<main id="main">
  <h1 class="visually-hidden">Plugins</h1>
  <div class="plugin-grid">
""" + "\n".join(cards) + """
  </div>
</main>
""" + footer(peek="plugins"))


def product_page(p):
    mark = cs_icon("once", "cso") if p.get("animated_icon") else ""
    beta = '<span class="beta">Free Beta</span>' if p["status"] == "beta" else ""
    name = (f'<img class="product-logo" src="/{p["logo"]}" width="734" height="182" alt="{e(p["name"])}">' if p.get("logo") else e(p["name"]))
    feats = "\n".join(f'      <li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in p["features"])
    bens = "\n".join(f'      <li>{e(b)}</li>' for b in p["benefits"])
    write(f"{p['slug']}.html", head(p["title"], p["description"], f"/{p['slug']}", p["accent"], p.get("font"))
          + body_open("product", f'--product-bg:{p.get("bg", "#4c4134")};--pattern-wash:{p.get("pattern_wash", 0)};--accent:{p["accent"]};--accent-2:{p.get("accent2", p["accent"])};--product-font:"{p.get("font", "Oswald")}"', peek=True) + header("Plugins", dark=True) + f"""
<main id="main">
  <section class="product-hero">
    {mark}
    <h1 class="product-name">{name}</h1>
    {beta}
    <p class="product-pitch">{e(p['pitch'])}</p>
    <div class="cta-row">
      <a class="btn" href="{e(p['beta_url'])}">{e(p['beta_label'])}</a>
      <a class="btn btn-ghost" href="#features">See features</a>
    </div>
    <p class="fine">{e(', '.join(p['platforms']))} &middot; {e(p['requires'])}</p>
  </section>

  {video(p['demo'], 'demo', p['name'] + ' demo video')}

  <p class="intro">{e(p.get('intro', ''))}</p>

  <section class="section" id="features" aria-labelledby="f-title">
    <h2 class="section-title" id="f-title">Features</h2>
    <ul class="features">
{feats}
    </ul>
  </section>

  <section class="section" aria-labelledby="b-title">
    <h2 class="section-title" id="b-title">Workflow benefits</h2>
    <ul class="benefits">
{bens}
    </ul>
  </section>

  <aside class="callout">
    <h2>This is a beta</h2>
    <p>{e(p['name'])} is ready for real scenes, and your feedback shapes version one. Found a bug or have an idea? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </aside>
</main>
""" + footer(peek=p.get("peek", "product")))


def not_found():
    write("404.html", head("Page not found", "This page doesn't exist.", "/404")
          + body_open(peek=True) + header("") + """
<main id="main">
  <section class="hero">
    <h1 class="tagline">This page wandered off.</h1>
    <p class="lede"><a href="/">Back to the home page</a> or <a href="/plugins">see the plugins</a>.</p>
  </section>
</main>
""" + footer(peek="404"))


def extras():
    urls = ["/", "/plugins", "/about", "/contact"] + [f"/{p['slug']}" for p in PLUGINS]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    # Cloudflare Pages: old Framer URLs go somewhere useful (302 = temporary, they'll return)
    write("_redirects", "/autorename-c4d /plugins 302\n/autorename-tut /plugins 302\n/tagradar-c4d /plugins 302\n/tagradar-tut /plugins 302\n/plugins/clonesensor /clonesensor 301\n")
    write("_headers", """/assets/*
  Cache-Control: public, max-age=31536000, immutable
/css/*
  Cache-Control: public, max-age=86400
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
""")


if __name__ == "__main__":
    home(); about(); contact(); plugins_page()
    for p in PLUGINS:
        product_page(p)
    not_found(); extras()
    print("built", sorted(x.name for x in OUT.iterdir()))
