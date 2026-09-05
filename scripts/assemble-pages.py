#!/usr/bin/env python3
"""Assemble static Progreso pages from partials + content (no JS required for primary content)."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://progresoshoreexcursion.com"
SITE = "Progreso Shore Excursion"
TODAY = date.today().isoformat()

PAGES = {
    "index.html": {
        "slug": "",
        "title": "Progreso Shore Excursions | Mayan Ruins, Cenotes & Port-Day Planning",
        "description": "Independent planning guide for Progreso cruise passengers — Chichén Itzá, Uxmal, Mérida, cenotes and coastal nature, with honest timing notes for Yucatán port calls.",
        "page": "home",
        "hero": "partials/hero-home.html",
        "trust": "partials/trust-strip.html",
        "content": "content/home.html",
        "og_image": "images/hero-progreso.png",
        "schema": "home",
    },
    "best-progreso-shore-excursions.html": {
        "slug": "best-progreso-shore-excursions",
        "title": "Best Progreso Shore Excursions | Compare Cruise Port Options",
        "description": "Editorial comparison of Progreso shore excursions for cruise passengers — ruins, Mérida, cenotes and coastal nature against realistic port time.",
        "page": "excursions",
        "hero": "partials/hero-best-excursions.html",
        "content": "content/best-progreso-shore-excursions.html",
        "og_image": "images/best-progreso-excursions.png",
        "schema": "webpage",
    },
    "progreso-cruise-port-guide.html": {
        "slug": "progreso-cruise-port-guide",
        "title": "Progreso Cruise Port Guide | Pier, Timing & Yucatán Excursions",
        "description": "Progreso cruise port guide — long pier, terminal orientation, what fits a port day, and return planning for Chichén Itzá, Uxmal, Mérida and cenotes.",
        "page": "port",
        "hero": "partials/hero-port-guide.html",
        "content": "content/progreso-cruise-port-guide.html",
        "og_image": "images/progreso-port.png",
        "schema": "webpage",
    },
    "uxmal-shore-excursion-progreso.html": {
        "slug": "uxmal-shore-excursion-progreso",
        "title": "Uxmal Shore Excursion from Progreso | Puuc Ruins Planning Guide",
        "description": "Editorial guide to an Uxmal shore excursion from Progreso — Puuc architecture, port-day fit and honest planning notes. No live booking on this site.",
        "page": "uxmal",
        "hero": "partials/hero-uxmal.html",
        "content": "content/uxmal-shore-excursion-progreso.html",
        "og_image": "images/uxmal.png",
        "schema": "webpage",
    },
    "chichen-itza-shore-excursion-progreso.html": {
        "slug": "chichen-itza-shore-excursion-progreso",
        "title": "Chichén Itzá Shore Excursion from Progreso | Planning Guide",
        "description": "Plan a Chichén Itzá day from Progreso cruise port — drive-time context, site expectations and return-buffer thinking. Editorial only.",
        "page": "chichen",
        "hero": "partials/hero-chichen-itza.html",
        "content": "content/chichen-itza-shore-excursion-progreso.html",
        "og_image": "images/chichen-itza.png",
        "schema": "webpage",
    },
    "merida-city-shore-excursion-progreso.html": {
        "slug": "merida-city-shore-excursion-progreso",
        "title": "Mérida City Shore Excursion from Progreso | Culture Day Guide",
        "description": "Mérida from Progreso for cruise passengers — plazas, markets and culture with a shorter inland drive than Chichén Itzá.",
        "page": "merida",
        "hero": "partials/hero-merida.html",
        "content": "content/merida-city-shore-excursion-progreso.html",
        "og_image": "images/merida.png",
        "schema": "webpage",
    },
    "cenote-shore-excursion-progreso.html": {
        "slug": "cenote-shore-excursion-progreso",
        "title": "Cenote Shore Excursion from Progreso | Yucatán Swim Planning",
        "description": "Cenote swimming from Progreso — distinguish Cuzamá-style routes from Ik Kil-style open cenotes, with cruise-day timing notes.",
        "page": "cenote",
        "hero": "partials/hero-cenote.html",
        "content": "content/cenote-shore-excursion-progreso.html",
        "og_image": "images/cenote.png",
        "schema": "webpage",
    },
    "pink-lagoon-and-flamingos-progreso.html": {
        "slug": "pink-lagoon-and-flamingos-progreso",
        "title": "Pink Lagoon & Flamingos from Progreso | Xcambó Coastal Guide",
        "description": "Honest guide to pink-lagoon and flamingo-style days from Progreso — Xcambó and nearby coastal wetlands, not distant Las Coloradas.",
        "page": "pinklagoon",
        "hero": "partials/hero-pink-lagoon.html",
        "content": "content/pink-lagoon-and-flamingos-progreso.html",
        "og_image": "images/pink-lagoon.png",
        "schema": "webpage",
    },
    "one-day-in-progreso-from-a-cruise-ship.html": {
        "slug": "one-day-in-progreso-from-a-cruise-ship",
        "title": "One Day in Progreso from a Cruise Ship | Realistic Port Plans",
        "description": "Sample Progreso port-day scenarios for cruise passengers — shorter calls, culture days and full ruins days without schedule integration.",
        "page": "oneday",
        "hero": "partials/hero-one-day.html",
        "content": "content/one-day-in-progreso-from-a-cruise-ship.html",
        "og_image": "images/one-day-progreso.png",
        "schema": "webpage",
    },
    "is-progreso-worth-visiting.html": {
        "slug": "is-progreso-worth-visiting",
        "title": "Is Progreso Worth Visiting on a Cruise? | Honest Take",
        "description": "Is Progreso worth visiting on a cruise? Honest framing for Yucatán ruins and culture versus beach-only expectations.",
        "page": "worth",
        "hero": "partials/hero-worth-visiting.html",
        "content": "content/is-progreso-worth-visiting.html",
        "og_image": "images/progreso-intro.png",
        "schema": "webpage",
    },
    "progreso-vs-cozumel-shore-excursions.html": {
        "slug": "progreso-vs-cozumel-shore-excursions",
        "title": "Progreso vs Cozumel Shore Excursions | Mexico Cruise Ports",
        "description": "Compare Progreso and Cozumel for cruise passengers — Yucatán interior culture versus Caribbean reef and beach days.",
        "page": "vscoz",
        "hero": "partials/hero-vs-cozumel.html",
        "content": "content/progreso-vs-cozumel-shore-excursions.html",
        "og_image": "images/progreso-beach.png",
        "schema": "webpage",
    },
    "progreso-shore-excursions-faq.html": {
        "slug": "progreso-shore-excursions-faq",
        "title": "Progreso Shore Excursions FAQ | Cruise Passenger Answers",
        "description": "FAQ for Progreso cruise shore days — pier, timing, Chichén Itzá, Mérida, cenotes and independent versus organised options.",
        "page": "faq",
        "hero": "partials/hero-faq.html",
        "content": "content/progreso-shore-excursions-faq.html",
        "og_image": "images/progreso-port.png",
        "schema": "faq",
    },
    "about.html": {
        "slug": "about",
        "title": "About | Progreso Shore Excursion",
        "description": "About this independent Progreso cruise excursion and destination planning guide.",
        "page": "about",
        "hero": "",
        "content": "content/about.html",
        "og_image": "images/progreso-port.png",
        "schema": "webpage",
        "main_class": "pt-16",
    },
    "contact.html": {
        "slug": "contact",
        "title": "Contact | Progreso Shore Excursion",
        "description": "Contact the Progreso Shore Excursion planning guide by email.",
        "page": "contact",
        "hero": "",
        "content": "content/contact.html",
        "og_image": "images/progreso-port.png",
        "schema": "webpage",
        "main_class": "pt-16",
    },
    "privacy.html": {
        "slug": "privacy",
        "title": "Privacy | Progreso Shore Excursion",
        "description": "Privacy policy for progresoshoreexcursion.com.",
        "page": "privacy",
        "hero": "",
        "content": "content/privacy.html",
        "og_image": "images/progreso-port.png",
        "schema": "webpage",
        "main_class": "pt-16",
    },
    "terms.html": {
        "slug": "terms",
        "title": "Terms | Progreso Shore Excursion",
        "description": "Terms of use for the Progreso Shore Excursion planning site.",
        "page": "terms",
        "hero": "",
        "content": "content/terms.html",
        "og_image": "images/progreso-port.png",
        "schema": "webpage",
        "main_class": "pt-16",
    },
    "methodology.html": {
        "slug": "methodology",
        "title": "Methodology | Progreso Shore Excursion",
        "description": "How this Progreso cruise planning guide is researched and kept honest.",
        "page": "methodology",
        "hero": "",
        "content": "content/methodology.html",
        "og_image": "images/progreso-port.png",
        "schema": "webpage",
        "main_class": "pt-16",
    },
    "404.html": {
        "slug": "404",
        "title": "Page Not Found | Progreso Shore Excursion",
        "description": "The requested Progreso planning page was not found.",
        "page": "404",
        "hero": "",
        "content": "content/404.html",
        "og_image": "images/progreso-port.png",
        "schema": "webpage",
        "main_class": "pt-16",
        "noindex": True,
    },
}


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def canon_url(slug: str) -> str:
    return f"{DOMAIN}/" if not slug else f"{DOMAIN}/{slug}"


def extensionlessify_html(html: str) -> str:
    def repl(m: re.Match) -> str:
        attr, quote, url = m.group(1), m.group(2), m.group(3)
        if url.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
            return m.group(0)
        if url.startswith(("images/", "/images/", "css/", "/css/", "js/", "/js/", "partials/", "content/")):
            return m.group(0)
        parts = urlsplit(url)
        path = parts.path
        if path.endswith(".html"):
            if path.endswith("index.html"):
                path = path[: -len("index.html")] or "/"
            else:
                path = path[: -len(".html")]
            if path in ("", "index") or path.endswith("/index"):
                path = "/"
            if not path.startswith("/") and path != "":
                path = "/" + path
            if path == "":
                path = "/"
        elif path in ("index.html", "/index.html"):
            path = "/"
        rebuilt = path if path.startswith("/") else ("/" + path if path else "/")
        if parts.query:
            rebuilt += "?" + parts.query
        if parts.fragment:
            rebuilt += "#" + parts.fragment
        return f"{attr}={quote}{rebuilt}{quote}"

    return re.sub(r'(href|action)=([\'"])([^\'"]+)\2', repl, html)


FAQ_ENTITIES = [
    {
        "@type": "Question",
        "name": "How long do cruise ships typically stay in Progreso?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Many Progreso calls are relatively long by Caribbean standards, often in a broad 8–10 hour range, but always confirm your ship’s actual arrival, departure and all-aboard times.",
        },
    },
    {
        "@type": "Question",
        "name": "How far is Chichén Itzá from Progreso cruise port?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Chichén Itzá is a substantial inland drive from Progreso — commonly discussed as around two hours each way depending on traffic and stops. Treat it as a full-day commitment and confirm timings with any operator.",
        },
    },
    {
        "@type": "Question",
        "name": "Is Mérida a realistic option from Progreso?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. Mérida is much closer than Chichén Itzá and often suits cruise passengers who want culture, plazas and markets without a long highway day.",
        },
    },
    {
        "@type": "Question",
        "name": "Are pink-lagoon tours the same as Las Coloradas?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Not usually. Cruise-friendly pink-lagoon and flamingo days from Progreso typically focus on coastal wetlands and Xcambó nearer the port. Las Coloradas / Ría Lagartos are much farther east and are a different planning problem.",
        },
    },
    {
        "@type": "Question",
        "name": "Does this website sell tours or take payment?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. This is an independent editorial planning guide. It does not operate tours, sell tickets or take payment.",
        },
    },
]


def json_ld(meta: dict) -> str:
    slug = meta["slug"]
    url = canon_url(slug)
    graph: list[dict] = [
        {
            "@type": "WebSite",
            "name": SITE,
            "url": f"{DOMAIN}/",
            "description": "Independent cruise passenger planning guide for Progreso, Yucatán, Mexico.",
            "inLanguage": "en-GB",
            "publisher": {"@type": "Organization", "name": SITE, "url": f"{DOMAIN}/"},
        },
        {
            "@type": "Organization",
            "name": SITE,
            "url": f"{DOMAIN}/",
            "email": "hello@progresoshoreexcursion.com",
            "description": "Editorial planning website for Progreso cruise shore days. Not a tour operator and not affiliated with any cruise line.",
        },
        {
            "@type": "WebPage",
            "name": meta["title"],
            "url": url,
            "description": meta["description"],
            "isPartOf": {"@type": "WebSite", "name": SITE, "url": f"{DOMAIN}/"},
            "inLanguage": "en-GB",
        },
    ]
    if slug and slug != "404":
        graph.append(
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": meta["title"].split("|")[0].strip(),
                        "item": url,
                    },
                ],
            }
        )
    if meta.get("schema") == "faq":
        graph.append({"@type": "FAQPage", "mainEntity": FAQ_ENTITIES})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def build_head(meta: dict) -> str:
    url = canon_url(meta["slug"])
    og = f"{DOMAIN}/{meta['og_image']}"
    robots = '  <meta name="robots" content="noindex, follow" />\n' if meta.get("noindex") else ""
    preload = ""
    if meta.get("hero") == "partials/hero-home.html":
        preload = f'  <link rel="preload" as="image" href="/{meta["og_image"]}" fetchpriority="high" />\n'
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{meta["title"]}</title>
  <meta name="description" content="{meta["description"]}" />
{robots}  <link rel="canonical" href="{url}" />
{preload}  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{meta["title"]}" />
  <meta property="og:description" content="{meta["description"]}" />
  <meta property="og:image" content="{og}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta property="og:locale" content="en_GB" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{meta["title"]}" />
  <meta name="twitter:description" content="{meta["description"]}" />
  <meta name="twitter:image" content="{og}" />
  <script type="application/ld+json">
{json_ld(meta)}
  </script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
"""


def assemble_page(filename: str, meta: dict) -> str:
    nav = extensionlessify_html(read("partials/nav.html"))
    footer = extensionlessify_html(read("partials/footer.html"))
    hero = extensionlessify_html(read(meta["hero"])) if meta.get("hero") else ""
    trust = extensionlessify_html(read(meta["trust"])) if meta.get("trust") else ""
    content = extensionlessify_html(read(meta["content"]))
    main_class = meta.get("main_class", "")
    main_attr = f' class="{main_class}"' if main_class else ""
    body = f"""<body class="bg-white text-gray-800 antialiased" data-page="{meta["page"]}" data-static="1">
  <div id="site-nav" data-inlined="true">{nav}</div>
  <div id="page-hero" data-inlined="true">{hero}</div>
  <div id="page-trust-strip" data-inlined="true">{trust}</div>
  <main id="page-content"{main_attr}>{content}</main>
  <div id="site-footer" data-inlined="true">{footer}</div>
  <script src="/js/site.js"></script>
</body>
</html>
"""
    return build_head(meta) + body


PRIORITY = {
    "": 1.0,
    "best-progreso-shore-excursions": 0.9,
    "progreso-cruise-port-guide": 0.9,
    "uxmal-shore-excursion-progreso": 0.9,
    "chichen-itza-shore-excursion-progreso": 0.9,
    "merida-city-shore-excursion-progreso": 0.85,
    "cenote-shore-excursion-progreso": 0.85,
    "pink-lagoon-and-flamingos-progreso": 0.8,
    "one-day-in-progreso-from-a-cruise-ship": 0.85,
    "progreso-shore-excursions-faq": 0.7,
}


def write_sitemap() -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for _, meta in PAGES.items():
        if meta.get("noindex") or meta["slug"] == "404":
            continue
        slug = meta["slug"]
        pri = PRIORITY.get(slug, 0.6)
        lines += [
            "  <url>",
            f"    <loc>{canon_url(slug)}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            f"    <changefreq>{'weekly' if pri >= 1 else 'monthly'}</changefreq>",
            f"    <priority>{pri:.1f}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n",
        encoding="utf-8",
    )


def main() -> None:
    for filename, meta in PAGES.items():
        html = assemble_page(filename, meta)
        (ROOT / filename).write_text(html, encoding="utf-8")
        print(f"wrote {filename}")
    write_sitemap()
    write_robots()
    print(f"sitemap urls: {sum(1 for m in PAGES.values() if not m.get('noindex') and m['slug'] != '404')}")


if __name__ == "__main__":
    main()
