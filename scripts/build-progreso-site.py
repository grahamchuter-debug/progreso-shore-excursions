#!/usr/bin/env python3
"""Generate Progreso Shore Excursion static site pages."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "progresoshoreexcursion.com"
SITE = "Progreso Shore Excursion"
BASE_URL = f"https://{DOMAIN}"

HEAD_COMMON = """  <script src="https://cdn.tailwindcss.com"></script>
  <script src="js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/site.css" />"""

RETURN_BADGE = '<span class="return-to-ship-badge" role="status"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 17h18M5 17l2-8h10l2 8M9 9l1-4h4l1 4"/></svg>Return To Ship On Time</span>'

def snapshot(items: dict[str, str]) -> str:
    rows = "".join(
        f'<div class="cruise-snapshot__item"><dt>{k}</dt><dd>{v}</dd></div>'
        for k, v in items.items()
    )
    return f'''<aside class="cruise-snapshot mb-10 px-4 sm:px-0" aria-label="Cruise passenger snapshot">
  <h3 class="font-display font-bold text-lg text-gray-900 mb-4">Cruise Passenger Snapshot</h3>
  <dl class="cruise-snapshot__grid">{rows}</dl>
</aside>'''

def related_links(links: list[tuple[str, str]]) -> str:
    parts = []
    for i, (href, label) in enumerate(links):
        if i: parts.append('<span class="text-gray-300">·</span>')
        parts.append(f'<a href="{href}" class="text-ocean-600 hover:text-ocean-800 font-medium">{label}</a>')
    return f'''<nav class="mt-10 pt-8 border-t border-gray-100" aria-label="Related Progreso guides">
  <p class="text-sm font-semibold text-gray-900 mb-3">Plan your port day</p>
  <div class="flex flex-wrap gap-3 text-sm">{"".join(parts)}</div>
</nav>'''

def cta_section() -> str:
    return '''<section class="py-16 cta-gradient"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-white mb-4">Plan Your Port Day</h2>
  <p class="text-white/85 text-sm mb-6">Compare Progreso shore excursions, read the port guide and confirm departure times before you book.</p>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <a href="best-progreso-shore-excursions.html" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">View Progreso Excursions</a>
    <a href="progreso-cruise-port-guide.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Plan Your Port Day</a>
  </div>
</div></section>'''

def hero(path: str, *, breadcrumb: str | None = None, eyebrow: str, title_html: str, lead: str,
         image: str, aria: str, actions: str = "", tags: str = "") -> str:
    bc = ""
    if breadcrumb:
        bc = f'''<nav class="site-hero__breadcrumb flex items-center gap-2 mb-4 text-xs text-white/60" aria-label="Breadcrumb">
        <a href="index.html" class="hover:text-white transition-colors">Home</a>
        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-white/80">{breadcrumb}</span>
      </nav>'''
    tag_block = f'<div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">{tags}</div>' if tags else ""
    act_block = f'<div class="site-hero__actions flex flex-col sm:flex-row gap-3">{actions}</div>' if actions else '<div class="site-hero__actions flex flex-col sm:flex-row gap-3"></div>'
    return f'''<section class="site-hero">
  <div class="absolute inset-0 hero-bg-custom" style="background-image: linear-gradient(135deg, rgba(37, 99, 235, 0.75) 0%, rgba(249, 115, 22, 0.65) 50%, rgba(30, 58, 138, 0.55) 100%), url('images/{image}');" role="img" aria-label="{aria}"></div>
  <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl">{bc}
      <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
        <span class="w-2 h-2 rounded-full bg-pr-400 animate-pulse"></span>
        <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">{eyebrow}</span>
      </div>
      <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">{title_html}</h1>
      <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">{lead}</p>
      {act_block}
      {tag_block}
    </div>
  </div>
  <div class="absolute bottom-0 left-0 right-0"><svg viewBox="0 0 1440 48" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="site-hero__wave" aria-hidden="true"><path d="M0 24 C360 48 1080 0 1440 24 L1440 48 L0 48 Z" fill="white"/></svg></div>
</section>'''

def shell(filename: str, *, title: str, description: str, keywords: str, canonical: str,
          preload: str, page: str, hero_file: str, content_file: str, ld_json: dict | list) -> None:
    ld = json.dumps(ld_json, indent=2)
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canonical}" />
  <link rel="preload" as="image" href="images/{preload}" fetchpriority="high" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{BASE_URL}/images/{preload}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">
{ld}
  </script>
{HEAD_COMMON}
</head>
<body class="bg-white text-gray-800 antialiased" data-page="{page}" data-base="" data-hero="{hero_file}" data-content="{content_file}" data-trust-strip="partials/trust-strip.html">
  <div id="site-nav"></div>
  <div id="page-hero"></div>
  <div id="page-trust-strip"></div>
  <main id="page-content"></main>
  <div id="site-footer"></div>
  <script src="js/site.js"></script>
</body>
</html>'''
    (ROOT / filename).write_text(html)

def tour_content(name: str, badge: str, badge_class: str, intro: str, checklist: list[str],
                 image: str, alt: str, highlights: list[tuple[str, str, str, str]],
                 snap: dict[str, str], links: list[tuple[str, str]]) -> str:
    checks = "".join(f'<li class="flex gap-2 text-sm text-gray-600"><span class="text-ocean-500">✓</span>{c}</li>' for c in checklist)
    cards = ""
    for h_img, h_alt, h_title, h_desc in highlights:
        cards += f'''<div class="bg-white rounded-3xl overflow-hidden shadow-md border border-pr-100 flex flex-col">
      <div class="card-media h-40"><img src="images/{h_img}" alt="{h_alt}" width="400" height="240" loading="lazy" decoding="async" /></div>
      <div class="p-5"><h3 class="font-display font-semibold text-gray-900 mb-2">{h_title}</h3><p class="text-sm text-gray-600 leading-relaxed">{h_desc}</p></div>
    </div>'''
    return f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <div class="mb-3 flex flex-wrap gap-2"><span class="{badge_class}" role="status">{badge}</span> {RETURN_BADGE}</div>
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Why cruise passengers choose this excursion</h2>
    <p class="text-gray-600 leading-relaxed mb-6">{intro}</p>
    <ul class="space-y-3 mb-6">{checks}</ul>
    <p class="text-xs text-gray-500">Confirm departure times, inclusions and return policies with your operator before booking. Independent tours should plan a buffer before all aboard.</p>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="images/{image}" alt="{alt}" width="600" height="450" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="py-14 bg-amber-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-10"><h2 class="text-2xl sm:text-3xl font-display font-bold text-gray-900 mb-3">Tour Highlights</h2>
  <p class="text-gray-600 text-sm max-w-2xl mx-auto">What to expect on this Progreso shore excursion.</p></div>
  <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">{cards}</div>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot(snap)}</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(links)}</div></section>
{cta_section()}'''

# --- Heroes ---
(ROOT / "partials/hero-home.html").write_text(hero(
    "partials/hero-home.html", eyebrow="Progreso · Yucatan", image="hero-progreso.png",
    aria="Ancient Mayan pyramid at Chichen Itza with stone temple rising above jungle canopy in Yucatan Mexico",
    title_html='Progreso Shore<br/><span class="text-pr-300">Excursions</span><br/>from the Cruise Port',
    lead="Mayan ruins, cenotes, Merida, pink lagoon flamingos and Gulf beaches — the Yucatan shore excursions cruise passengers book from Progreso.",
    actions='''<a href="best-progreso-shore-excursions.html" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">View Progreso Excursions</a>
          <a href="progreso-cruise-port-guide.html" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Plan Your Port Day</a>''',
    tags='''<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Chichen Itza</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Cenotes</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Merida</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Pink Lagoon</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Cruise Passengers</span>'''
))

HERO_PAGES = [
    ("hero-best-excursions.html", "Best Excursions", "Yucatan Highlights", "best-progreso-excursions.png",
     "Comparison of top Progreso cruise shore excursions including ruins, cenotes and culture tours",
     "Best Progreso<br/><span class=\"text-pr-300\">Shore Excursions</span>",
     "Compare Chichen Itza, Uxmal, Merida, cenotes and nature tours timed for typical Progreso port calls."),
    ("hero-port-guide.html", "Port Guide", "Progreso Cruise Terminal", "progreso-port.png",
     "Progreso Mexico cruise port with long pier extending into Gulf of Mexico for passenger shore excursions",
     "Progreso Cruise<br/><span class=\"text-pr-300\">Port Guide</span>",
     "Where ships dock, how far Merida and ruins are, excursion timing and return-to-ship advice for first-time visitors."),
    ("hero-one-day.html", "One Day Itinerary", "Cruise Port Day", "one-day-progreso.png",
     "Mayan ruins and Yucatan cultural landmarks for cruise passengers planning one day in Progreso Mexico",
     "One Day in Progreso<br/><span class=\"text-pr-300\">from a Cruise Ship</span>",
     "Sample itineraries for short, medium and full port days — ruins, cenotes, Merida or beach time."),
    ("hero-chichen-itza.html", "Chichen Itza", "New Seven Wonders", "chichen-itza.png",
     "El Castillo pyramid at Chichen Itza Mayan archaeological site in Yucatan Mexico for cruise shore excursions",
     "Chichen Itza<br/><span class=\"text-pr-300\">from Progreso</span>",
     "Full-day shore excursion to Mexico's most famous Mayan ruins — pyramids, ball courts and guided history."),
    ("hero-uxmal.html", "Uxmal Ruins", "Puuc Architecture", "uxmal.png",
     "Uxmal Mayan ruins with ornate Puuc-style stone carvings in Yucatan Mexico for Progreso cruise excursions",
     "Uxmal Shore<br/><span class=\"text-pr-300\">Excursion</span>",
     "Less crowded alternative Mayan site with remarkable Puuc architecture — cultural depth without Chichen Itza crowds."),
    ("hero-merida.html", "Merida City", "Colonial Capital", "merida.png",
     "Colorful colonial buildings and cathedral in Merida Yucatan Mexico city tour from Progreso cruise port",
     "Merida City<br/><span class=\"text-pr-300\">Shore Excursion</span>",
     "Explore Yucatan's elegant capital — plazas, markets, mansions and authentic Yucatecan culture from Progreso."),
    ("hero-cenote.html", "Cenote Adventure", "Sacred Sinkholes", "cenote.png",
     "Turquoise cenote sinkhole with limestone walls and clear water for Yucatan shore excursion swimming",
     "Cenote Shore<br/><span class=\"text-pr-300\">Excursion</span>",
     "Swim crystal-clear cenotes the ancient Maya considered sacred — half-day adventure near Progreso."),
    ("hero-pink-lagoon.html", "Pink Lagoon", "Nature &amp; Ruins", "pink-lagoon.png",
     "Pink saltwater lagoon with flamingos and coastal wetlands in Yucatan Mexico nature shore excursion",
     "Pink Lagoon &amp;<br/><span class=\"text-pr-300\">Flamingos</span>",
     "Hidden-gem combo of Xcambo ruins, pink lagoon wetlands and flamingo spotting along the Yucatan coast."),
    ("hero-worth-visiting.html", "Worth Visiting?", "Cruise Planning", "progreso-intro.png",
     "Yucatan Mayan culture and Gulf coast scenery for cruise passengers evaluating Progreso Mexico port calls",
     "Is Progreso<br/><span class=\"text-pr-300\">Worth Visiting?</span>",
     "Honest guide for cruise passengers deciding whether Progreso delivers enough for your port day."),
    ("hero-vs-cozumel.html", "Progreso vs Cozumel", "Mexico Cruise Ports", "progreso-beach.png",
     "Gulf of Mexico beach and Yucatan interior excursions compared for Mexico cruise port planning",
     "Progreso vs Cozumel<br/><span class=\"text-pr-300\">Shore Excursions</span>",
     "Compare ruins-and-culture Progreso with reef-and-beach Cozumel to pick the right Mexico port day."),
]

for hf, crumb, eyebrow, img, aria, title, lead in HERO_PAGES:
    (ROOT / f"partials/{hf}").write_text(hero(
        f"partials/{hf}", breadcrumb=crumb, eyebrow=eyebrow, image=img, aria=aria,
        title_html=title, lead=lead))

print("Heroes written")

# --- Home content ---
(ROOT / "content/home.html").write_text('''<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-10">
    <div class="section-label mx-auto">Best Excursions</div>
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-4">Best Progreso Cruise Excursions</h2>
    <p class="text-gray-600 text-sm max-w-2xl mx-auto">Ranked for cruise schedules — Chichen Itza, Uxmal, Merida, cenotes, pink lagoon flamingos and Gulf beaches across Yucatan, Mexico.</p>
  </div>
  <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-pr-50 flex flex-col">
      <div class="card-media h-44"><img src="images/chichen-itza.png" alt="El Castillo pyramid at Chichen Itza Mayan ruins shore excursion from Progreso Yucatan cruise port" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Chichen Itza</h3><p class="text-sm text-gray-500 flex-1">Mexico's iconic Mayan pyramid and archaeological wonder.</p>
      <a href="chichen-itza-shore-excursion-progreso.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Ruins Tour</a></div>
    </div>
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-pr-50 flex flex-col">
      <div class="card-media h-44"><img src="images/cenote.png" alt="Turquoise Yucatan cenote sinkhole for Progreso cruise passenger swimming shore excursion" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Cenote Adventure</h3><p class="text-sm text-gray-500 flex-1">Sacred sinkholes with crystal-clear swimming.</p>
      <a href="cenote-shore-excursion-progreso.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Cenote Tour</a></div>
    </div>
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-pr-50 flex flex-col">
      <div class="card-media h-44"><img src="images/merida.png" alt="Colonial architecture and cathedral in Merida Yucatan city tour from Progreso cruise port" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Merida City Tour</h3><p class="text-sm text-gray-500 flex-1">Yucatan capital — plazas, culture and shopping.</p>
      <a href="merida-city-shore-excursion-progreso.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Merida Tour</a></div>
    </div>
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-pr-50 flex flex-col">
      <div class="card-media h-44"><img src="images/pink-lagoon.png" alt="Pink lagoon wetlands with flamingos on Yucatan nature shore excursion from Progreso cruise port" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Pink Lagoon</h3><p class="text-sm text-gray-500 flex-1">Xcambo ruins, flamingos and coastal wetlands.</p>
      <a href="pink-lagoon-and-flamingos-progreso.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Nature Tour</a></div>
    </div>
  </div>
  <p class="text-center mt-8"><a href="best-progreso-shore-excursions.html" class="text-ocean-600 font-semibold text-sm">See full comparison →</a></p>
</div></section>
<section class="pt-4 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <div class="inline-flex items-center gap-2 text-ocean-600 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-ocean-400"></div>Progreso Cruise Port</div>
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Why Cruise Passengers<br/><span class="text-ocean-600">Choose Progreso</span></h2>
    <p class="text-gray-600 leading-relaxed mb-5">Progreso is your gateway to interior Yucatan — not just another beach stop. From this Gulf port you reach <strong>Chichen Itza</strong>, <strong>Uxmal</strong>, colonial <strong>Merida</strong>, sacred <strong>cenotes</strong> and pink-lagoon wetlands with flamingos. Most port calls run <strong>8–10 hours</strong>, enough for a full ruins day or a balanced culture-and-nature itinerary.</p>
    <a href="progreso-cruise-port-guide.html" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Plan Your Port Day</a>
  </div>
  <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden">
    <img src="images/progreso-intro.png" alt="Yucatan Mayan pyramid and Gulf coast scenery representing Progreso Mexico cruise shore excursion destinations" width="800" height="600" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="py-16 bg-amber-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-12"><h2 class="text-3xl font-display font-bold text-gray-900">Featured Excursions</h2>
  <p class="text-gray-600 text-sm mt-3 max-w-xl mx-auto">Most-booked Progreso shore excursions for cruise passengers.</p></div>
  <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-pr-50 flex flex-col">
      <div class="card-media h-44"><img src="images/uxmal.png" alt="Uxmal Mayan ruins with Puuc architecture on shore excursion from Progreso Yucatan cruise port" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Uxmal Ruins</h3><p class="text-sm text-gray-500 flex-1">Less crowded Mayan site with ornate Puuc stonework.</p>
      <a href="uxmal-shore-excursion-progreso.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Uxmal Tour</a></div>
    </div>
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-pr-50 flex flex-col">
      <div class="card-media h-44"><img src="images/chichen-itza.png" alt="Chichen Itza El Castillo pyramid on full-day shore excursion from Progreso Mexico cruise port" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Chichen Itza &amp; Cenote</h3><p class="text-sm text-gray-500 flex-1">Ruins plus Ik Kil cenote swim in one long day.</p>
      <a href="chichen-itza-shore-excursion-progreso.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Chichen Itza</a></div>
    </div>
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-pr-50 flex flex-col">
      <div class="card-media h-44"><img src="images/merida.png" alt="Historic Merida Yucatan plaza and colonial buildings on cruise shore excursion from Progreso port" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Merida &amp; Shopping</h3><p class="text-sm text-gray-500 flex-1">City sights, markets and Yucatecan culture.</p>
      <a href="merida-city-shore-excursion-progreso.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Merida Tour</a></div>
    </div>
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-pr-50 flex flex-col">
      <div class="card-media h-44"><img src="images/progreso-beach.png" alt="Gulf of Mexico beach near Progreso Yucatan cruise port for passenger beach day shore excursions" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Beach &amp; Xcambo</h3><p class="text-sm text-gray-500 flex-1">Coastal ruins combo with beach club time.</p>
      <a href="pink-lagoon-and-flamingos-progreso.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Coastal Tour</a></div>
    </div>
  </div>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">''' + snapshot({
    "Typical Time In Port": "8–10 hours (typical)",
    "Best For": "Mayan ruins, cenotes, Merida, nature &amp; beaches",
    "Activity Level": "Varies — see comparison",
    "Family Friendly": "Good with age-appropriate tour picks",
    "Return To Ship Friendly": "Operators usually allow 60–90 min buffer",
    "Popular Excursion Types": "Chichen Itza, cenotes, Merida, Uxmal, pink lagoon",
}) + '''</div></section>
<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl font-display font-bold text-gray-900 text-center mb-10">Top Things To Do in Progreso</h2>
  <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Chichen Itza</h3><p class="text-gray-600">El Castillo pyramid and ball courts — the Yucatan's must-see Mayan site, roughly 2+ hours from port each way.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Uxmal Ruins</h3><p class="text-gray-600">Puuc-style architecture with fewer crowds than Chichen Itza — strong cultural alternative.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Merida</h3><p class="text-gray-600">Colonial plazas, mansions and markets — Yucatan's capital is about 30–45 minutes inland.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Cenote Swimming</h3><p class="text-gray-600">Ik Kil, Cuzama and reserve cenotes offer unforgettable freshwater swims in limestone caverns.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Pink Lagoon &amp; Flamingos</h3><p class="text-gray-600">Coastal wetlands and Xcambo ruins — a hidden-gem nature day along the Gulf shore.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Progreso Beach</h3><p class="text-gray-600">Gulf beaches and beach clubs near the pier when you want a relaxed half-day without long drives.</p></div>
  </div>
</div></section>
<section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="images/chichen-itza.png" alt="Chichen Itza Mayan pyramid El Castillo on shore excursion from Progreso Yucatan Mexico cruise port" width="600" height="450" loading="lazy" decoding="async" />
  </div>
  <div>
    <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Mayan Ruins From Progreso</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Progreso's real advantage is interior Yucatan access. <a href="chichen-itza-shore-excursion-progreso.html" class="text-ocean-600 font-medium">Chichen Itza</a> draws the biggest crowds but delivers the iconic pyramid experience. <a href="uxmal-shore-excursion-progreso.html" class="text-ocean-600 font-medium">Uxmal</a> suits travelers who want remarkable stonework with a more intimate feel.</p>
    <p class="text-gray-600 leading-relaxed mb-5">Full-day ruins tours need an early departure and a reliable return buffer. Confirm your ship's all-aboard time before booking any independent operator.</p>
    <a href="best-progreso-shore-excursions.html" class="text-ocean-600 font-semibold text-sm">Compare all excursions →</a>
  </div>
</div></div></section>
<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Cenotes &amp; Nature Near Progreso</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Yucatan's limestone peninsula is dotted with cenotes — natural sinkholes the Maya considered portals to the underworld. Half-day <a href="cenote-shore-excursion-progreso.html" class="text-ocean-600 font-medium">cenote excursions</a> pair well with shorter port calls or as add-ons to ruins tours.</p>
    <p class="text-gray-600 leading-relaxed mb-5">For something different, the <a href="pink-lagoon-and-flamingos-progreso.html" class="text-ocean-600 font-medium">pink lagoon and flamingo route</a> combines coastal wetlands, Xcambo archaeological site and birdwatching — a true hidden gem.</p>
    <a href="cenote-shore-excursion-progreso.html" class="text-ocean-600 font-semibold text-sm">Cenote excursions →</a>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="images/cenote.png" alt="Yucatan cenote with turquoise water and limestone walls for Progreso cruise passenger shore excursion swimming" width="600" height="450" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 text-center mb-4">Which Progreso Excursion Is Right for Me?</h2>
  <p class="text-center text-gray-600 text-sm max-w-2xl mx-auto mb-10">Match your port day to ruins, cenotes, Merida culture or coastal nature — timed for typical 8–10 hour Progreso cruise calls in Yucatan, Mexico.</p>
  <div class="overflow-x-auto rounded-3xl border border-pr-100 shadow-sm">
    <table class="w-full text-sm text-left min-w-[720px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold rounded-tl-3xl">Excursion</th>
        <th class="py-4 px-3 font-semibold">Duration</th>
        <th class="py-4 px-3 font-semibold">Best For</th>
        <th class="py-4 px-3 font-semibold">Activity Level</th>
        <th class="py-4 px-4 font-semibold rounded-tr-3xl">Details</th>
      </tr></thead>
      <tbody class="bg-white">
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="chichen-itza-shore-excursion-progreso.html" class="text-ocean-600">Chichen Itza</a></td><td class="py-4 px-3 text-gray-600">6–7 hrs</td><td class="py-4 px-3 text-gray-600">Iconic Mayan ruins</td><td class="py-4 px-3 text-gray-600">Moderate</td><td class="py-4 pl-3"><a href="chichen-itza-shore-excursion-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="uxmal-shore-excursion-progreso.html" class="text-ocean-600">Uxmal Ruins</a></td><td class="py-4 px-3 text-gray-600">5–6 hrs</td><td class="py-4 px-3 text-gray-600">Culture without crowds</td><td class="py-4 px-3 text-gray-600">Moderate</td><td class="py-4 pl-3"><a href="uxmal-shore-excursion-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="merida-city-shore-excursion-progreso.html" class="text-ocean-600">Merida City</a></td><td class="py-4 px-3 text-gray-600">5–6 hrs</td><td class="py-4 px-3 text-gray-600">Plazas, shopping &amp; food</td><td class="py-4 px-3 text-gray-600">Easy to moderate</td><td class="py-4 pl-3"><a href="merida-city-shore-excursion-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="cenote-shore-excursion-progreso.html" class="text-ocean-600">Cenote Adventure</a></td><td class="py-4 px-3 text-gray-600">4–5 hrs</td><td class="py-4 px-3 text-gray-600">Swimming &amp; nature</td><td class="py-4 px-3 text-gray-600">Moderate</td><td class="py-4 pl-3"><a href="cenote-shore-excursion-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="pink-lagoon-and-flamingos-progreso.html" class="text-ocean-600">Pink Lagoon</a></td><td class="py-4 px-3 text-gray-600">4–5 hrs</td><td class="py-4 px-3 text-gray-600">Flamingos &amp; Xcambo ruins</td><td class="py-4 px-3 text-gray-600">Easy to moderate</td><td class="py-4 pl-3"><a href="pink-lagoon-and-flamingos-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
      </tbody>
    </table>
  </div>
</div></section>
<section class="py-16 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 text-center mb-8">Progreso Shore Excursions FAQ</h2>
  <div class="space-y-4">
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">How long do cruise ships stay in Progreso?</summary>
      <p class="mt-4 text-sm text-gray-500">Most Progreso port calls are 8 to 10 hours — longer than many Caribbean stops. That makes full-day Chichen Itza or Uxmal tours feasible if you depart early.</p></details>
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">How far is Chichen Itza from Progreso cruise port?</summary>
      <p class="mt-4 text-sm text-gray-500">Chichen Itza is roughly 2 to 2.5 hours by coach from Progreso each way. Plan a 6–7 hour excursion with buffer time before all aboard.</p></details>
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Is Merida worth visiting from Progreso?</summary>
      <p class="mt-4 text-sm text-gray-500">Yes — Merida is Yucatan's cultural capital, about 30–45 minutes inland. City tours fit medium-length port calls without the long drives required for Chichen Itza.</p></details>
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Ruins or cenotes for a first Progreso visit?</summary>
      <p class="mt-4 text-sm text-gray-500">Chichen Itza for the bucket-list pyramid; cenotes for adventure and swimming. Many passengers combine ruins with a cenote stop on full-day tours — confirm the itinerary before booking.</p></details>
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Ship excursion or book independently in Progreso?</summary>
      <p class="mt-4 text-sm text-gray-500">Ship tours guarantee the vessel waits if the operator is late. Reputable Progreso operators plan returns with buffer — always confirm policies and your all-aboard time before booking ashore.</p></details>
  </div>
</div></section>''' + cta_section())

print("Home content written")

LINKS_DEFAULT = [
    ("progreso-cruise-port-guide.html", "Port Guide"),
    ("best-progreso-shore-excursions.html", "Best Excursions"),
    ("one-day-in-progreso-from-a-cruise-ship.html", "One Day Itinerary"),
    ("chichen-itza-shore-excursion-progreso.html", "Chichen Itza"),
    ("uxmal-shore-excursion-progreso.html", "Uxmal"),
    ("cenote-shore-excursion-progreso.html", "Cenotes"),
]

# Tour pages
(ROOT / "content/chichen-itza-shore-excursion-progreso.html").write_text(tour_content(
    "Chichen Itza", "Most Popular", "popular-badge",
    "Chichen Itza is the headline Progreso shore excursion — El Castillo pyramid, the Great Ball Court and temples that define Mayan archaeology. Full-day tours depart early from the Progreso cruise terminal and include guided commentary, with operators planning return times around your ship's all-aboard.",
    ["6–7 hour full-day format with early departure from Progreso pier.", "Guided walk through El Castillo, ball court and key temple complexes.", "Some tours add Cenote Ik Kil for a memorable swim after the ruins.", "Reputable operators build in 60–90 minute buffer before all aboard.", "Bring sun protection, water and comfortable walking shoes."],
    "chichen-itza.png", "El Castillo pyramid at Chichen Itza Mayan archaeological site on shore excursion from Progreso Yucatan cruise port",
    [("chichen-itza.png", "Chichen Itza El Castillo pyramid rising above jungle at Yucatan Mayan ruins shore excursion", "El Castillo Pyramid", "The iconic stepped pyramid — the most photographed structure in Yucatan."),
     ("cenote.png", "Cenote Ik Kil turquoise sinkhole swimming stop on Chichen Itza shore excursion from Progreso", "Cenote Ik Kil", "Optional cenote swim on combo tours — refreshing after hours in the sun."),
     ("chichen-itza.png", "Mayan ball court and stone architecture at Chichen Itza archaeological site Yucatan Mexico", "Ball Court & Temples", "Explore ceremonial platforms, the ball court and ancient city layout.")],
    {"Typical Time In Port": "8–10 hours needed", "Best For": "History buffs & first-time Yucatan visitors", "Activity Level": "Moderate — walking on uneven ground", "Family Friendly": "Good for school-age children and up", "Return To Ship Friendly": "Full-day tour — confirm buffer with operator", "Popular Excursion Types": "Chichen Itza, Chichen Itza + cenote"},
    LINKS_DEFAULT))

(ROOT / "content/uxmal-shore-excursion-progreso.html").write_text(tour_content(
    "Uxmal", "Best for History", "best-for-badge",
    "Uxmal rewards travelers who want deep Mayan culture without Chichen Itza crowds. The Puuc-style Governor's Palace and Magician's Pyramid showcase ornate stone mosaics and sophisticated urban planning — a highly cultural Progreso shore excursion with shorter drive times than Chichen Itza.",
    ["5–6 hour tours with less highway time than Chichen Itza routes.", "Puuc architecture — intricate stone lattice and geometric facades.", "Generally fewer visitors than Chichen Itza for a more intimate experience.", "Guided history explains Uxmal's role in the late Classic Maya period.", "Operators coordinate returns with Progreso cruise schedules."],
    "uxmal.png", "Uxmal Mayan ruins Governor's Palace with Puuc stone carvings on shore excursion from Progreso Yucatan",
    [("uxmal.png", "Uxmal Governor's Palace ornate Puuc Mayan stonework on Progreso cruise shore excursion", "Governor's Palace", "Remarkable stone mosaics — among the finest Puuc architecture."),
     ("uxmal.png", "Pyramid of the Magician at Uxmal Mayan archaeological site Yucatan Mexico", "Magician's Pyramid", "Distinctive oval pyramid dominating the ancient city core."),
     ("uxmal.png", "Uxmal Mayan ruins ceremonial plaza and stone structures for cultural shore excursion", "Ceremonial Plaza", "Walk ancient courtyards where Mayan elites once gathered.")],
    {"Typical Time In Port": "8–10 hours (typical)", "Best For": "Culture lovers avoiding big crowds", "Activity Level": "Moderate — walking & stairs", "Family Friendly": "Good with older children", "Return To Ship Friendly": "Usually 60–90 min buffer built in", "Popular Excursion Types": "Uxmal ruins, Uxmal + hacienda"},
    LINKS_DEFAULT))

(ROOT / "content/merida-city-shore-excursion-progreso.html").write_text(tour_content(
    "Merida", "Best for First-Time Visitors", "best-for-badge",
    "Merida is Yucatan's elegant colonial capital — pastel mansions, bustling plazas, cathedrals and markets just 30–45 minutes from Progreso. City tours suit cruise passengers who want authentic culture and shopping without the long drives required for interior ruins.",
    ["5–6 hour city tours from Progreso cruise terminal.", "Plaza Grande, Paseo de Montejo and historic centro sights.", "Time for markets, handicrafts and Yucatecan street food.", "Moderate activity — mostly walking on paved streets.", "Easier return timing than full-day Chichen Itza excursions."],
    "merida.png", "Colonial cathedral and plaza in Merida Yucatan on city shore excursion from Progreso cruise port",
    [("merida.png", "Merida Plaza Grande and colonial cathedral on Yucatan city tour from Progreso cruise port", "Plaza Grande", "Heart of Merida — cathedral, governor's palace and lively square."),
     ("merida.png", "Paseo de Montejo mansions and tree-lined boulevard in Merida Yucatan city sightseeing", "Paseo de Montejo", "Grand boulevard lined with historic mansions and cafés."),
     ("merida.png", "Local market and handicrafts shopping on Merida shore excursion from Progreso Yucatan", "Markets & Shopping", "Hamacas, guayaberas and regional crafts at local markets.")],
    {"Typical Time In Port": "6–10 hours", "Best For": "Culture, food & shopping", "Activity Level": "Easy to moderate — city walking", "Family Friendly": "Excellent for all ages", "Return To Ship Friendly": "Flexible — shorter drive than ruins", "Popular Excursion Types": "Merida city, Merida + hacienda"},
    LINKS_DEFAULT))

(ROOT / "content/cenote-shore-excursion-progreso.html").write_text(tour_content(
    "Cenote", "Best for Adventure", "best-for-badge",
    "Yucatan cenotes are natural sinkholes filled with crystal-clear freshwater — sacred to the ancient Maya and unforgettable to swim. Half-day Progreso cenote excursions visit reserves like Cuzama or natural parks, often combining mangroves, wildlife and a beach club finish.",
    ["4–5 hour half-day format suits shorter or combo port days.", "Swim in limestone caverns with turquoise water and stalactites.", "Cuzama route uses traditional horse-drawn rail carts to multiple cenotes.", "Life vests usually provided — confirm with your operator.", "Return timing more flexible than full-day Chichen Itza tours."],
    "cenote.png", "Turquoise Yucatan cenote sinkhole with limestone walls for Progreso cruise passenger swimming excursion",
    [("cenote.png", "Open cenote with clear turquoise water for swimming on Progreso Yucatan shore excursion", "Open Cenotes", "Sunlit sinkholes perfect for swimming and photography."),
     ("cenote.png", "Cavern cenote with stalactites and crystal water on Yucatan adventure tour from Progreso", "Cavern Cenotes", "Partially covered caves with dramatic rock formations."),
     ("progreso-beach.png", "Gulf beach club after cenote swim on half-day Progreso Yucatan cruise shore excursion", "Beach Finish", "Some tours end at a beach club for relaxation.")],
    {"Typical Time In Port": "6–10 hours", "Best For": "Swimmers & nature lovers", "Activity Level": "Moderate — swimming & steps", "Family Friendly": "Good — check minimum ages", "Return To Ship Friendly": "Half-day — usually comfortable buffer", "Popular Excursion Types": "Cuzama cenotes, cenote + beach"},
    LINKS_DEFAULT))

(ROOT / "content/pink-lagoon-and-flamingos-progreso.html").write_text(tour_content(
    "Pink Lagoon", "Hidden Gem", "hidden-gem-badge",
    "This coastal nature excursion combines Xcambo Mayan ruins, pink-hued lagoon wetlands and flamingo spotting along the Yucatan Gulf shore. It's a refreshing alternative to inland ruins — less driving, more wildlife, and a true hidden gem for Progreso cruise passengers.",
    ["4–5 hour coastal route with Xcambo archaeological site.", "Pink lagoon wetlands — seasonal color varies with salinity and light.", "Flamingo and shorebird viewing in Ría Lagartos biosphere area.", "Often pairs ruins walk with beach club or estuary time.", "Ideal when you want nature over another long highway day."],
    "pink-lagoon.png", "Pink lagoon wetlands with flamingos on hidden gem nature shore excursion from Progreso Yucatan cruise port",
    [("pink-lagoon.png", "Pink saltwater lagoon and coastal wetlands on Yucatan nature tour from Progreso", "Pink Lagoon", "Striking coastal wetlands — best color varies by season."),
     ("uxmal.png", "Xcambo Mayan ruins near Yucatan Gulf coast on shore excursion from Progreso cruise port", "Xcambo Ruins", "Coastal Mayan site — smaller but atmospheric and uncrowded."),
     ("pink-lagoon.png", "Flamingos and shorebirds in Yucatan wetland reserve on Progreso nature excursion", "Flamingo Spotting", "Seasonal flamingo colonies and diverse Gulf coast birdlife.")],
    {"Typical Time In Port": "6–10 hours", "Best For": "Nature lovers & photographers", "Activity Level": "Easy to moderate", "Family Friendly": "Good — wildlife appeals to kids", "Return To Ship Friendly": "Shorter drives — comfortable timing", "Popular Excursion Types": "Xcambo + beach, pink lagoon tour"},
    LINKS_DEFAULT))

print("Tour content written")

# Guide pages content
(ROOT / "content/best-progreso-shore-excursions.html").write_text(f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Best Progreso Shore Excursions</h2>
  <p class="text-gray-600 leading-relaxed text-sm">Operators meet at the <strong>Progreso cruise terminal</strong> — one of the world's longest piers — and plan returns with buffer before all aboard. Compare options below and confirm times before booking.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Typical Time In Port": "8–10 hours (typical)",
    "Best For": "Comparing all excursion types",
    "Activity Level": "Varies — see comparison",
    "Family Friendly": "Good with age-appropriate picks",
    "Return To Ship Friendly": "Operators usually allow 60–90 min buffer",
    "Popular Excursion Types": "See comparison table below",
})}</div></section>
<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 text-center mb-4">Which Progreso Excursion Is Right for Me?</h2>
  <p class="text-center text-gray-600 text-sm max-w-2xl mx-auto mb-10">Match your Progreso port day to Mayan ruins, cenotes, Merida culture or coastal nature.</p>
  <div class="overflow-x-auto rounded-3xl border border-pr-100 shadow-sm">
    <table class="w-full text-sm text-left min-w-[720px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold rounded-tl-3xl">Excursion</th>
        <th class="py-4 px-3 font-semibold">Duration</th>
        <th class="py-4 px-3 font-semibold">Best For</th>
        <th class="py-4 px-3 font-semibold">Activity Level</th>
        <th class="py-4 px-4 font-semibold rounded-tr-3xl">Details</th>
      </tr></thead>
      <tbody class="bg-white">
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="chichen-itza-shore-excursion-progreso.html" class="text-ocean-600">Chichen Itza</a> <span class="popular-badge text-[10px] py-0.5 px-2">Most Popular</span></td><td class="py-4 px-3 text-gray-600">6–7 hrs</td><td class="py-4 px-3 text-gray-600">Iconic pyramid &amp; ruins</td><td class="py-4 px-3 text-gray-600">Moderate</td><td class="py-4 pl-3"><a href="chichen-itza-shore-excursion-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="uxmal-shore-excursion-progreso.html" class="text-ocean-600">Uxmal Ruins</a> <span class="best-for-badge text-[10px] py-0.5 px-2">Best for History</span></td><td class="py-4 px-3 text-gray-600">5–6 hrs</td><td class="py-4 px-3 text-gray-600">Puuc architecture, fewer crowds</td><td class="py-4 px-3 text-gray-600">Moderate</td><td class="py-4 pl-3"><a href="uxmal-shore-excursion-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="merida-city-shore-excursion-progreso.html" class="text-ocean-600">Merida City</a> <span class="best-for-badge text-[10px] py-0.5 px-2">First-Timers</span></td><td class="py-4 px-3 text-gray-600">5–6 hrs</td><td class="py-4 px-3 text-gray-600">Culture, food &amp; shopping</td><td class="py-4 px-3 text-gray-600">Easy to moderate</td><td class="py-4 pl-3"><a href="merida-city-shore-excursion-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="cenote-shore-excursion-progreso.html" class="text-ocean-600">Cenote Adventure</a></td><td class="py-4 px-3 text-gray-600">4–5 hrs</td><td class="py-4 px-3 text-gray-600">Swimming &amp; nature</td><td class="py-4 px-3 text-gray-600">Moderate</td><td class="py-4 pl-3"><a href="cenote-shore-excursion-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-pr-50 hover:bg-sand-50/80"><td class="py-4 pr-4 font-semibold"><a href="pink-lagoon-and-flamingos-progreso.html" class="text-ocean-600">Pink Lagoon</a> <span class="hidden-gem-badge text-[10px] py-0.5 px-2">Hidden Gem</span></td><td class="py-4 px-3 text-gray-600">4–5 hrs</td><td class="py-4 px-3 text-gray-600">Flamingos &amp; Xcambo</td><td class="py-4 px-3 text-gray-600">Easy to moderate</td><td class="py-4 pl-3"><a href="pink-lagoon-and-flamingos-progreso.html" class="text-pr-600 font-medium text-xs">Guide →</a></td></tr>
      </tbody>
    </table>
  </div>
</div></section>
<section class="py-12 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Excursions by Traveler Type</h2>
  <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 text-sm">
    <div class="bg-sand-50 rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">First Timers</h3><p class="text-gray-600 mb-3">Chichen Itza for the bucket list or Merida for culture without long drives.</p><a href="chichen-itza-shore-excursion-progreso.html" class="text-ocean-600 font-semibold">Chichen Itza →</a></div>
    <div class="bg-sand-50 rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">History Buffs</h3><p class="text-gray-600 mb-3">Uxmal delivers Puuc stonework with fewer crowds than Chichen Itza.</p><a href="uxmal-shore-excursion-progreso.html" class="text-ocean-600 font-semibold">Uxmal →</a></div>
    <div class="bg-sand-50 rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Adventure</h3><p class="text-gray-600 mb-3">Cenote swimming in sacred sinkholes — half-day format.</p><a href="cenote-shore-excursion-progreso.html" class="text-ocean-600 font-semibold">Cenotes →</a></div>
    <div class="bg-ocean-50 rounded-3xl p-6 border border-ocean-100"><h3 class="font-display font-bold text-lg mb-2">Nature Lovers</h3><p class="text-gray-600 mb-3">Pink lagoon, flamingos and Xcambo ruins along the Gulf coast.</p><a href="pink-lagoon-and-flamingos-progreso.html" class="text-ocean-600 font-semibold">Pink Lagoon →</a></div>
    <div class="bg-ocean-50 rounded-3xl p-6 border border-ocean-100"><h3 class="font-display font-bold text-lg mb-2">Families</h3><p class="text-gray-600 mb-3">Merida city tours and beach combos suit mixed ages.</p><a href="merida-city-shore-excursion-progreso.html" class="text-ocean-600 font-semibold">Merida →</a></div>
    <div class="bg-ocean-50 rounded-3xl p-6 border border-ocean-100"><h3 class="font-display font-bold text-lg mb-2">Short Port Calls</h3><p class="text-gray-600 mb-3">Cenote half-day or Progreso beach — avoid full-day highway trips.</p><a href="progreso-cruise-port-guide.html" class="text-ocean-600 font-semibold">Port Guide →</a></div>
  </div>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{cta_section()}''')

(ROOT / "content/progreso-cruise-port-guide.html").write_text(f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4 text-center">Progreso Cruise Port Guide</h2>
  <p class="text-gray-600 leading-relaxed text-sm text-center">Practical advice for first-time cruise passengers docking in Progreso, Yucatan — pier layout, distances, timing and return-to-ship confidence.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Typical Time In Port": "8–10 hours (typical)",
    "Best For": "Gateway to Yucatan interior",
    "Activity Level": "Depends on excursion choice",
    "Family Friendly": "Good — plan age-appropriate tours",
    "Return To Ship Friendly": "Allow 60–90 min buffer on independent tours",
    "Popular Excursion Types": "Chichen Itza, Merida, cenotes, beaches",
})}</div></section>
<section class="py-12 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 space-y-8 text-sm text-gray-600 leading-relaxed">
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">Where do cruise ships dock?</h3>
  <p>Ships tie up at the <strong>Progreso International Terminal</strong> at the end of a very long pier — roughly 4 miles (6.5 km) into the Gulf of Mexico. Passengers reach shore by shuttle tram or walk depending on pier policies. The terminal area has shops, taxis and excursion meeting points.</p></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">How far is Merida from Progreso?</h3>
  <p>Merida is about <strong>30 km (19 miles)</strong> south — typically <strong>30–45 minutes</strong> by coach or taxi. Merida city tours are among the most practical Progreso shore excursions because drive time is manageable.</p></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">How far is Chichen Itza?</h3>
  <p>Chichen Itza is roughly <strong>2 to 2.5 hours each way</strong> from Progreso by highway. Only book full-day ruins tours if your port call is long enough — usually 8+ hours — and confirm the operator's return schedule against your all-aboard time.</p></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">Excursion timing tips</h3>
  <ul class="list-disc pl-5 space-y-2"><li>Full-day Chichen Itza tours depart early — often within an hour of docking.</li><li>Half-day cenote or beach tours offer more schedule flexibility.</li><li>Account for tram time from ship to terminal when meeting your guide.</li><li>Traffic on highway 261 can affect return times — reputable operators plan buffer.</li></ul></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">Return-to-ship advice</h3>
  <p>Ship excursions guarantee the vessel waits if the tour is late. Independent operators should state a return policy — look for tours that build in <strong>60–90 minutes</strong> before all aboard. Keep your cruise line's port contact number and confirm excursion end times the morning you dock.</p></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">First-time visitor tips</h3>
  <ul class="list-disc pl-5 space-y-2"><li>USD widely accepted; Mexican pesos (MXN) are official currency.</li><li>Bring sun protection — Yucatan sun is intense at ruins and cenotes.</li><li>Progreso is about culture and interior Yucatan, not Caribbean reef snorkeling.</li><li>Compare <a href="progreso-vs-cozumel-shore-excursions.html" class="text-ocean-600 font-medium">Progreso vs Cozumel</a> if your itinerary includes both Mexico ports.</li></ul></div>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{cta_section()}''')

print("Guide content part 1 written")

(ROOT / "content/one-day-in-progreso-from-a-cruise-ship.html").write_text(f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">One Day in Progreso from a Cruise Ship</h2>
  <p class="text-gray-600 text-sm">Sample itineraries for 6-hour, 8-hour and 10-hour port calls. Adjust based on your ship's actual schedule and confirm tour availability before booking.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Typical Time In Port": "8–10 hours (typical)",
    "Best For": "Planning your full port day",
    "Activity Level": "Varies by itinerary",
    "Family Friendly": "Choose itinerary to match ages",
    "Return To Ship Friendly": "Always keep 60–90 min buffer",
    "Popular Excursion Types": "See itineraries below",
})}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-3xl mx-auto px-4 space-y-10">
  <div class="bg-white rounded-3xl p-6 border border-pr-100 shadow-sm">
    <span class="popular-badge mb-3 inline-block">10-Hour Port Call</span>
    <h3 class="text-xl font-display font-bold text-gray-900 mb-3">Full Day: Chichen Itza + Cenote</h3>
    <ol class="text-sm text-gray-600 space-y-2 list-decimal pl-5">
      <li>Early departure from Progreso terminal (within 1 hour of docking).</li>
      <li>Coach to Chichen Itza — guided ruins walk (2–3 hours on site).</li>
      <li>Cenote Ik Kil swim stop on combo tours.</li>
      <li>Return to ship with 60–90 min buffer before all aboard.</li>
    </ol>
    <a href="chichen-itza-shore-excursion-progreso.html" class="inline-block mt-4 text-ocean-600 font-semibold text-sm">Chichen Itza guide →</a>
  </div>
  <div class="bg-white rounded-3xl p-6 border border-pr-100 shadow-sm">
    <span class="best-for-badge mb-3 inline-block">8-Hour Port Call</span>
    <h3 class="text-xl font-display font-bold text-gray-900 mb-3">Culture Day: Merida + Market</h3>
    <ol class="text-sm text-gray-600 space-y-2 list-decimal pl-5">
      <li>Morning coach to Merida (30–45 min from port).</li>
      <li>Plaza Grande, cathedral and Paseo de Montejo walking tour.</li>
      <li>Lunch and handicraft shopping at local markets.</li>
      <li>Afternoon return — comfortable timing for most 8-hour calls.</li>
    </ol>
    <a href="merida-city-shore-excursion-progreso.html" class="inline-block mt-4 text-ocean-600 font-semibold text-sm">Merida guide →</a>
  </div>
  <div class="bg-white rounded-3xl p-6 border border-pr-100 shadow-sm">
    <span class="hidden-gem-badge mb-3 inline-block">6–8 Hour Port Call</span>
    <h3 class="text-xl font-display font-bold text-gray-900 mb-3">Nature Day: Cenotes or Pink Lagoon</h3>
    <ol class="text-sm text-gray-600 space-y-2 list-decimal pl-5">
      <li>Half-day cenote tour (Cuzama or natural reserve) with swimming.</li>
      <li>Or coastal route: Xcambo ruins + pink lagoon flamingo spotting.</li>
      <li>Option to add beach club time near Progreso pier.</li>
      <li>Best choice when you want to avoid long highway drives.</li>
    </ol>
    <a href="cenote-shore-excursion-progreso.html" class="inline-block mt-4 text-ocean-600 font-semibold text-sm">Cenote guide →</a>
  </div>
  <div class="bg-white rounded-3xl p-6 border border-pr-100 shadow-sm">
    <h3 class="text-xl font-display font-bold text-gray-900 mb-3">Alternative: Uxmal for History Lovers</h3>
    <p class="text-sm text-gray-600">If Chichen Itza feels too crowded or too far, Uxmal offers a 5–6 hour cultural deep-dive with remarkable Puuc architecture. Fits 8–10 hour port calls well.</p>
    <a href="uxmal-shore-excursion-progreso.html" class="inline-block mt-4 text-ocean-600 font-semibold text-sm">Uxmal guide →</a>
  </div>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{cta_section()}''')

(ROOT / "content/is-progreso-worth-visiting.html").write_text(f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4 text-center">Is Progreso Worth Visiting on a Cruise?</h2>
  <p class="text-gray-600 text-sm text-center leading-relaxed">An honest look at what Progreso delivers for cruise passengers — and when another port day might suit you better.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Typical Time In Port": "8–10 hours (typical)",
    "Best For": "Yucatan culture &amp; ruins",
    "Activity Level": "Moderate on most top tours",
    "Family Friendly": "Yes with planning",
    "Return To Ship Friendly": "Plan buffer on highway excursions",
    "Popular Excursion Types": "Chichen Itza, Merida, cenotes",
})}</div></section>
<section class="py-12 bg-white"><div class="max-w-3xl mx-auto px-4 space-y-6 text-sm text-gray-600 leading-relaxed">
  <p><strong>Yes — if you want Mayan culture over beach lounging.</strong> Progreso is one of the best Mexico cruise ports for reaching Chichen Itza, Uxmal, Merida and cenotes. Unlike reef-focused Caribbean stops, Progreso positions you on the Yucatan Peninsula with long port times that make full-day inland tours realistic.</p>
  <p><strong>Progreso shines for history and adventure.</strong> Bucket-list ruins, sacred cenote swims, colonial Merida and pink-lagoon flamingos are experiences you cannot replicate at a typical beach-only port. The trade-off is drive time — Chichen Itza is 2+ hours each way.</p>
  <p><strong>Progreso may disappoint if you only want Caribbean beaches.</strong> The Gulf coast near the pier is pleasant but not the turquoise reef-and-snorkel experience of Cozumel. Beach days exist, but culture and ruins are the real draw. See our <a href="progreso-vs-cozumel-shore-excursions.html" class="text-ocean-600 font-medium">Progreso vs Cozumel comparison</a>.</p>
  <p><strong>Plan around your port time.</strong> With 8–10 hours you can do Chichen Itza or Uxmal comfortably. Shorter calls suit Merida, cenotes or coastal nature tours. Always confirm excursion duration and return time before booking.</p>
  <p><strong>Bottom line:</strong> Progreso is worth visiting for cruise passengers who prioritize Yucatan heritage. Skip the long highway tours if you prefer a relaxed beach day — but you would miss what makes this port special.</p>
</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-3xl mx-auto px-4">
  <h3 class="text-xl font-display font-bold text-gray-900 mb-4 text-center">Quick Verdict</h3>
  <div class="grid sm:grid-cols-2 gap-4 text-sm">
    <div class="bg-white rounded-2xl p-5 border border-green-200"><p class="font-semibold text-green-800 mb-2">Worth it for</p><ul class="text-gray-600 space-y-1"><li>• Mayan ruins (Chichen Itza, Uxmal)</li><li>• Cenote swimming</li><li>• Merida culture</li><li>• Nature &amp; flamingos</li></ul></div>
    <div class="bg-white rounded-2xl p-5 border border-pr-200"><p class="font-semibold text-pr-800 mb-2">Less ideal for</p><ul class="text-gray-600 space-y-1"><li>• Reef snorkeling only</li><li>• Very short port calls</li><li>• Passive beach-only days</li></ul></div>
  </div>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{cta_section()}''')

(ROOT / "content/progreso-vs-cozumel-shore-excursions.html").write_text(f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Progreso vs Cozumel Shore Excursions</h2>
  <p class="text-gray-600 text-sm">Both are popular Mexico cruise ports — but they deliver very different port days. Use this comparison to set expectations.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Typical Time In Port": "Progreso 8–10 hrs · Cozumel 6–10 hrs",
    "Best For": "Depends on your priorities",
    "Activity Level": "Both offer easy to strenuous options",
    "Family Friendly": "Both excellent with right picks",
    "Return To Ship Friendly": "Buffer on both — confirm operators",
    "Popular Excursion Types": "See comparison below",
})}</div></section>
<section class="py-12 bg-white"><div class="max-w-4xl mx-auto px-4">
  <div class="overflow-x-auto rounded-3xl border border-pr-100 shadow-sm">
    <table class="w-full text-sm text-left min-w-[600px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold">Factor</th>
        <th class="py-4 px-4 font-semibold">Progreso</th>
        <th class="py-4 px-4 font-semibold">Cozumel</th>
      </tr></thead>
      <tbody class="bg-white">
        <tr class="border-b border-pr-50"><td class="py-4 px-4 font-semibold text-gray-900">Main draw</td><td class="py-4 px-4 text-gray-600">Mayan ruins, cenotes, Merida, nature</td><td class="py-4 px-4 text-gray-600">Reef snorkeling, beach clubs, island tours</td></tr>
        <tr class="border-b border-pr-50"><td class="py-4 px-4 font-semibold text-gray-900">Signature excursion</td><td class="py-4 px-4 text-gray-600"><a href="chichen-itza-shore-excursion-progreso.html" class="text-ocean-600">Chichen Itza</a></td><td class="py-4 px-4 text-gray-600">Reef snorkel &amp; El Cielo</td></tr>
        <tr class="border-b border-pr-50"><td class="py-4 px-4 font-semibold text-gray-900">Drive to top attraction</td><td class="py-4 px-4 text-gray-600">2+ hrs to Chichen Itza</td><td class="py-4 px-4 text-gray-600">20 min to reefs &amp; beaches</td></tr>
        <tr class="border-b border-pr-50"><td class="py-4 px-4 font-semibold text-gray-900">Water activities</td><td class="py-4 px-4 text-gray-600">Cenotes, Gulf beaches</td><td class="py-4 px-4 text-gray-600">World-class reef snorkeling</td></tr>
        <tr class="border-b border-pr-50"><td class="py-4 px-4 font-semibold text-gray-900">Culture &amp; history</td><td class="py-4 px-4 text-gray-600">Excellent — interior Yucatan</td><td class="py-4 px-4 text-gray-600">Good — island ruins &amp; San Miguel</td></tr>
        <tr class="border-b border-pr-50"><td class="py-4 px-4 font-semibold text-gray-900">Best for</td><td class="py-4 px-4 text-gray-600">History &amp; adventure seekers</td><td class="py-4 px-4 text-gray-600">Beach &amp; snorkel lovers</td></tr>
        <tr><td class="py-4 px-4 font-semibold text-gray-900">Port character</td><td class="py-4 px-4 text-gray-600">Gulf gateway to Yucatan interior</td><td class="py-4 px-4 text-gray-600">Caribbean island resort vibe</td></tr>
      </tbody>
    </table>
  </div>
  <p class="mt-8 text-sm text-gray-600 leading-relaxed">If your itinerary includes both ports, do ruins in Progreso and snorkeling in Cozumel — you get the best of each. Neither port is "better"; they serve different cruise passenger goals.</p>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{cta_section()}''')

print("All content written")

PAGES = [
    ("index.html", "home", "partials/hero-home.html", "content/home.html", "hero-progreso.png",
     "Progreso Shore Excursion | Mayan Ruins, Cenotes &amp; Tours from Progreso Cruise Port",
     "Plan Progreso shore excursions for cruise passengers — Chichen Itza, Uxmal, Merida, cenotes, pink lagoon flamingos and Yucatan culture from Mexico cruise port.",
     "Progreso shore excursions, Progreso cruise excursions, Progreso cruise port excursions, Chichen Itza from Progreso",
     BASE_URL + "/",
     {"@context": "https://schema.org", "@graph": [
         {"@type": "WebSite", "name": SITE, "url": BASE_URL + "/", "description": "Planning guide for Progreso cruise shore excursions from Yucatan, Mexico"},
         {"@type": "LocalBusiness", "name": SITE, "url": BASE_URL + "/", "description": "Cruise passenger planning guide for Progreso, Yucatan shore excursions",
          "address": {"@type": "PostalAddress", "addressLocality": "Progreso", "addressRegion": "Yucatan", "addressCountry": "MX"},
          "areaServed": {"@type": "City", "name": "Progreso", "containedInPlace": {"@type": "AdministrativeArea", "name": "Yucatan"}}},
         {"@type": "TouristInformationCenter", "name": SITE, "url": BASE_URL + "/", "description": "Progreso cruise port excursion planning information"},
         {"@type": "FAQPage", "mainEntity": [
             {"@type": "Question", "name": "How long do cruise ships stay in Progreso?", "acceptedAnswer": {"@type": "Answer", "text": "Most Progreso port calls are 8 to 10 hours."}},
             {"@type": "Question", "name": "How far is Chichen Itza from Progreso cruise port?", "acceptedAnswer": {"@type": "Answer", "text": "Roughly 2 to 2.5 hours each way by coach."}},
             {"@type": "Question", "name": "Is Merida worth visiting from Progreso?", "acceptedAnswer": {"@type": "Answer", "text": "Yes — Merida is about 30-45 minutes inland with plazas, culture and shopping."}},
             {"@type": "Question", "name": "Ruins or cenotes for a first Progreso visit?", "acceptedAnswer": {"@type": "Answer", "text": "Chichen Itza for the iconic pyramid; cenotes for swimming adventure."}},
             {"@type": "Question", "name": "Ship excursion or book independently in Progreso?", "acceptedAnswer": {"@type": "Answer", "text": "Ship tours guarantee wait-if-late; reputable locals plan buffer returns."}},
         ]},
     ]}),
    ("best-progreso-shore-excursions.html", "excursions", "partials/hero-best-excursions.html", "content/best-progreso-shore-excursions.html", "best-progreso-excursions.png",
     "Best Progreso Shore Excursions | Compare Top Cruise Tours",
     "Compare the best Progreso shore excursions for cruise passengers — Chichen Itza, Uxmal, Merida, cenotes and pink lagoon tours with return-to-ship timing.",
     "best shore excursions in Progreso, Progreso cruise excursions, Progreso shore excursions comparison",
     BASE_URL + "/best-progreso-shore-excursions.html",
     {"@context": "https://schema.org", "@type": "TouristInformationCenter", "name": "Best Progreso Shore Excursions", "url": BASE_URL + "/best-progreso-shore-excursions.html", "description": "Comparison guide for Progreso cruise shore excursions"}),
    ("progreso-cruise-port-guide.html", "port", "partials/hero-port-guide.html", "content/progreso-cruise-port-guide.html", "progreso-port.png",
     "Progreso Cruise Port Guide | Pier, Timing &amp; Tips",
     "Progreso cruise port guide — where ships dock, distance to Merida and Chichen Itza, excursion timing and return-to-ship advice for first-time visitors.",
     "Progreso cruise port guide, Progreso cruise port excursions, Progreso pier",
     BASE_URL + "/progreso-cruise-port-guide.html",
     {"@context": "https://schema.org", "@type": "TouristInformationCenter", "name": "Progreso Cruise Port Guide", "url": BASE_URL + "/progreso-cruise-port-guide.html"}),
    ("one-day-in-progreso-from-a-cruise-ship.html", "oneday", "partials/hero-one-day.html", "content/one-day-in-progreso-from-a-cruise-ship.html", "one-day-progreso.png",
     "One Day in Progreso from a Cruise Ship | Itinerary Guide",
     "Sample one-day Progreso itineraries for cruise passengers — Chichen Itza, Merida, cenotes and nature tours timed for typical port calls.",
     "one day Progreso cruise ship, Progreso itinerary cruise",
     BASE_URL + "/one-day-in-progreso-from-a-cruise-ship.html",
     {"@context": "https://schema.org", "@type": "TouristInformationCenter", "name": "One Day in Progreso", "url": BASE_URL + "/one-day-in-progreso-from-a-cruise-ship.html"}),
    ("chichen-itza-shore-excursion-progreso.html", "chichen", "partials/hero-chichen-itza.html", "content/chichen-itza-shore-excursion-progreso.html", "chichen-itza.png",
     "Chichen Itza Shore Excursion from Progreso | Mayan Ruins Tour",
     "Chichen Itza shore excursion from Progreso cruise port — El Castillo pyramid, guided ruins tour and optional cenote with ship-timed returns.",
     "Chichen Itza from Progreso cruise port, Chichen Itza shore excursion Progreso",
     BASE_URL + "/chichen-itza-shore-excursion-progreso.html",
     {"@context": "https://schema.org", "@type": "TouristTrip", "name": "Chichen Itza Shore Excursion from Progreso", "description": "Full-day Mayan ruins shore excursion from Progreso cruise port.", "touristType": "Cruise passengers", "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL}}),
    ("uxmal-shore-excursion-progreso.html", "uxmal", "partials/hero-uxmal.html", "content/uxmal-shore-excursion-progreso.html", "uxmal.png",
     "Uxmal Shore Excursion from Progreso | Mayan Ruins Tour",
     "Uxmal shore excursion from Progreso — less crowded Puuc-style Mayan ruins with guided history and cruise-timed returns.",
     "Uxmal from Progreso cruise port, Uxmal shore excursion Progreso",
     BASE_URL + "/uxmal-shore-excursion-progreso.html",
     {"@context": "https://schema.org", "@type": "TouristTrip", "name": "Uxmal Shore Excursion from Progreso", "description": "Puuc Mayan ruins shore excursion from Progreso cruise port.", "touristType": "Cruise passengers", "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL}}),
    ("merida-city-shore-excursion-progreso.html", "merida", "partials/hero-merida.html", "content/merida-city-shore-excursion-progreso.html", "merida.png",
     "Merida City Shore Excursion from Progreso | Culture Tour",
     "Merida city shore excursion from Progreso cruise port — colonial plazas, markets, Yucatecan culture and shopping with manageable drive times.",
     "Merida shore excursion from Progreso, Merida city tour Progreso cruise",
     BASE_URL + "/merida-city-shore-excursion-progreso.html",
     {"@context": "https://schema.org", "@type": "TouristTrip", "name": "Merida City Shore Excursion from Progreso", "description": "Colonial city tour from Progreso cruise port.", "touristType": "Cruise passengers", "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL}}),
    ("cenote-shore-excursion-progreso.html", "cenote", "partials/hero-cenote.html", "content/cenote-shore-excursion-progreso.html", "cenote.png",
     "Cenote Shore Excursion from Progreso | Yucatan Adventure",
     "Progreso cenote excursion — swim sacred Yucatan sinkholes at Cuzama or natural reserves with half-day cruise-timed returns.",
     "Progreso cenote excursion, cenote shore excursion Progreso",
     BASE_URL + "/cenote-shore-excursion-progreso.html",
     {"@context": "https://schema.org", "@type": "TouristTrip", "name": "Cenote Shore Excursion from Progreso", "description": "Cenote swimming adventure from Progreso cruise port.", "touristType": "Cruise passengers", "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL}}),
    ("pink-lagoon-and-flamingos-progreso.html", "pinklagoon", "partials/hero-pink-lagoon.html", "content/pink-lagoon-and-flamingos-progreso.html", "pink-lagoon.png",
     "Pink Lagoon &amp; Flamingos Progreso Shore Excursion",
     "Pink lagoon Progreso shore excursion — Xcambo ruins, flamingo wetlands and coastal nature along the Yucatan Gulf shore.",
     "Pink lagoon Progreso shore excursion, flamingos Progreso, Xcambo ruins",
     BASE_URL + "/pink-lagoon-and-flamingos-progreso.html",
     {"@context": "https://schema.org", "@type": "TouristTrip", "name": "Pink Lagoon and Flamingos Progreso", "description": "Coastal nature shore excursion from Progreso cruise port.", "touristType": "Cruise passengers", "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL}}),
    ("is-progreso-worth-visiting.html", "worth", "partials/hero-worth-visiting.html", "content/is-progreso-worth-visiting.html", "progreso-intro.png",
     "Is Progreso Worth Visiting on a Cruise? | Honest Guide",
     "Is Progreso worth visiting on a cruise? Honest guide for passengers — Mayan ruins, cenotes, Merida vs beach-only expectations.",
     "is Progreso worth visiting cruise, Progreso cruise port worth it",
     BASE_URL + "/is-progreso-worth-visiting.html",
     {"@context": "https://schema.org", "@type": "TouristInformationCenter", "name": "Is Progreso Worth Visiting", "url": BASE_URL + "/is-progreso-worth-visiting.html"}),
    ("progreso-vs-cozumel-shore-excursions.html", "vscoz", "partials/hero-vs-cozumel.html", "content/progreso-vs-cozumel-shore-excursions.html", "progreso-beach.png",
     "Progreso vs Cozumel Shore Excursions | Mexico Cruise Ports",
     "Compare Progreso vs Cozumel shore excursions — ruins and cenotes vs reef snorkeling and beach clubs for Mexico cruise passengers.",
     "Progreso vs Cozumel shore excursions, Progreso or Cozumel cruise",
     BASE_URL + "/progreso-vs-cozumel-shore-excursions.html",
     {"@context": "https://schema.org", "@type": "TouristInformationCenter", "name": "Progreso vs Cozumel Shore Excursions", "url": BASE_URL + "/progreso-vs-cozumel-shore-excursions.html"}),
]

for fname, page, hero_f, content_f, preload, title, desc, kw, canon, ld in PAGES:
    shell(fname, title=title, description=desc, keywords=kw, canonical=canon,
          preload=preload, page=page, hero_file=hero_f, content_file=content_f, ld_json=ld)

# Sitemap
urls = [
    (BASE_URL + "/", "1.0", "weekly"),
    (BASE_URL + "/best-progreso-shore-excursions.html", "0.9", "monthly"),
    (BASE_URL + "/progreso-cruise-port-guide.html", "0.8", "monthly"),
    (BASE_URL + "/one-day-in-progreso-from-a-cruise-ship.html", "0.8", "monthly"),
    (BASE_URL + "/chichen-itza-shore-excursion-progreso.html", "0.9", "monthly"),
    (BASE_URL + "/uxmal-shore-excursion-progreso.html", "0.9", "monthly"),
    (BASE_URL + "/merida-city-shore-excursion-progreso.html", "0.9", "monthly"),
    (BASE_URL + "/cenote-shore-excursion-progreso.html", "0.9", "monthly"),
    (BASE_URL + "/pink-lagoon-and-flamingos-progreso.html", "0.9", "monthly"),
    (BASE_URL + "/is-progreso-worth-visiting.html", "0.8", "monthly"),
    (BASE_URL + "/progreso-vs-cozumel-shore-excursions.html", "0.8", "monthly"),
]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for loc, pri, freq in urls:
    sitemap += f"  <url><loc>{loc}</loc><lastmod>2026-06-09</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>\n"
sitemap += "</urlset>\n"
(ROOT / "sitemap.xml").write_text(sitemap)

(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

(ROOT / "wrangler.jsonc").write_text('''{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "progreso-shore-excursions",
  "compatibility_date": "2026-06-09",
  "observability": { "enabled": true },
  "assets": { "directory": "." },
  "routes": [{ "pattern": "progresoshoreexcursion.com", "custom_domain": true }]
}
''')

print("Shells, sitemap, robots, wrangler written — DONE")
