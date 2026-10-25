"""Render the supplied portfolio content in the user's reference template."""
import hashlib
import json
from html import escape
from pathlib import Path
import shutil

root = Path(__file__).parent
data = json.loads((root / 'content.json').read_text())

def prose(value):
    text = escape(value)
    for title, *_ in data['works']:
        text = text.replace(escape(title), f'<em>{escape(title)}</em>')
    return text

def paragraphs(values, cls=''):
    return ''.join(f'<p class="{cls}">{prose(p)}</p>' for p in values)

dist = root / 'dist'
(dist / 'assets').mkdir(exist_ok=True)
landing_source = root / 'images/landing-page-web.jpg'
landing_version = hashlib.sha256(landing_source.read_bytes()).hexdigest()[:12]
landing_image_url = f'assets/landing-page.jpg?v={landing_version}'
shutil.copyfile(landing_source, dist / 'assets/landing-page.jpg')
css = (root / 'site/base.css').read_text().replace('__LANDING_IMAGE__', landing_image_url)
(dist / 'styles.css').write_text(css)
for source, target in [('content.css', 'content.css'), ('script.js', 'script.js'), ('favicon.svg', 'favicon.svg')]:
    shutil.copyfile(root / 'site' / source, dist / target)

photos = json.loads((root / 'image-manifest.json').read_text())
work_photos = [
    ['01.heic', '01_2.HEIC', '01_3heic.heic'],
    ['2_1.heic', '2_2.heic'],
    ['03_1.heic', '03_2.heic'],
    ['IMG_7632.HEIC'],
    ['05.heic'],
    ['06.heic'],
]

def photo_tag(photo, alt, loading='lazy'):
    return f'<img src="{escape(photo["src"])}" alt="{escape(alt)}" width="{photo["width"]}" height="{photo["height"]}" loading="{loading}">'

cards = []
work_order = [0, 5, 1, 2, 3, 4]
for i in work_order:
    title, medium, note, description = data['works'][i]
    label = escape(title)
    gallery = [{**photos[name], 'alt': f'{title} — view {index+1}'} for index, name in enumerate(work_photos[i])]
    picture = photo_tag(gallery[0], gallery[0]['alt'])
    thumbnails = ''
    if len(gallery) > 1:
        thumbnails = '<div class="work-thumbnails" aria-label="Additional views">' + ''.join(f'<button type="button" data-work="{i}" data-photo-index="{index}" aria-label="View {label}, photo {index+1}">{photo_tag(photo, photo["alt"])}</button>' for index, photo in enumerate(gallery)) + '</div>'
    cards.append(f'''<article class="work-item {'portrait-work' if i % 2 == 0 else 'wide-work'}" id="work-{i+1}" data-photos="{escape(json.dumps(gallery), quote=True)}">
      <button class="work-image artwork-button" data-work="{i}" aria-label="View {label} details">{picture}<span class="work-number">0{i+1}</span><span class="work-expand" aria-hidden="true">↗</span></button>
      {thumbnails}
      <div class="work-meta"><h2>{label}</h2><p>2026</p></div>
      <div class="artwork-description"><p class="medium"><strong>Medium:</strong> {escape(medium)}</p>{f'<p class="material-note">{escape(note)}</p>' if note else ''}{paragraphs(description)}</div>
    </article>''')

contact_content = (root / 'contact.html').read_text()

first_intro, rest_intro = data['intro'].split('. ', 1)
html = f'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f1efe8">
<title>Koketso Masemola — Becoming, in Layers</title><meta name="description" content="Becoming, in Layers (2026). Koketso Masemola explores fashion, cultural heritage and personal identity through textiles, photography and mixed media.">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="content.css"><script src="script.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><a class="wordmark" href="#home" aria-label="Koketso Masemola home">KM.</a><button class="menu-button" aria-expanded="false" aria-controls="navigation">Menu</button><nav class="nav" id="navigation" aria-label="Main navigation"><a href="#artworks">Artworks</a><a href="#archive">Archive</a><a href="#statement">Statement</a><a href="#catalogue">Catalogue</a><a href="#about">About</a><a href="#cv">CV</a><a href="#contact">Contact</a></nav></header>
<main id="main">
<section class="hero" id="home"><img src="{landing_image_url}" alt="A woman presenting the Becoming, in Layers exhibition, with a garment installation and textile artworks" width="2400" height="2355" fetchpriority="high"><div class="hero-shade"></div><div class="hero-title"><h1>Koketso<br>Masemola</h1><p class="hero-kicker">Multidisciplinary artist · South Africa</p><p><em>Becoming, in Layers</em><br>Fashion. Memory. Identity.</p></div><a class="hero-link" href="#artworks">View selected work <span aria-hidden="true">→</span></a></section>
<section class="intro section-pad" id="introduction"><h2 class="eyebrow">Becoming, in Layers / 2026</h2><div class="intro-copy"><p>{prose(first_intro)}.</p><p class="intro-secondary">{prose(rest_intro)}</p><a class="text-link" href="#statement">Read artist statement <span aria-hidden="true">→</span></a></div></section>
<section class="work section-pad" id="artworks"><div class="section-heading"><h2 class="eyebrow">Selected artworks</h2><p>2026</p></div><div class="work-grid">{''.join(cards)}</div><a class="outline-link" href="#catalogue">Explore the catalogue <span aria-hidden="true">→</span></a></section>
{(root / 'archive.html').read_text()}
<section class="full-statement section-pad" id="statement"><h2 class="eyebrow">Artist statement</h2><blockquote>{prose(data['statement'][0])}</blockquote><div class="statement-columns">{paragraphs(data['statement'][1:])}</div></section>
<section class="catalogue section-pad" id="catalogue"><div class="catalogue-cover" aria-hidden="true"><span>Koketso<br>Masemola</span><em>Becoming,<br>in Layers</em><small>Exhibition catalogue / 2026</small></div><div class="catalogue-copy"><p class="eyebrow">Exhibition catalogue</p><h2>Development of the<br>Additional Artworks</h2>{paragraphs(data['catalogue'])}</div></section>
<section class="about section-pad" id="about"><div class="about-image">{photo_tag(photos['Artist Bio.JPG'], 'Portrait of Koketso Masemola')}</div><div class="about-copy"><p class="eyebrow">Artist biography</p><h2>Koketso Masemola</h2>{paragraphs(data['bio'])}</div></section>
{(root / 'cv.html').read_text()}
</main>
{contact_content}
<dialog id="artwork-dialog" aria-labelledby="dialog-title"><button class="dialog-close" aria-label="Close artwork details">Close ×</button><div class="dialog-gallery"><div id="dialog-art"></div><div class="dialog-navigation" hidden><button type="button" id="previous-photo" aria-label="Previous artwork photograph">←</button><span id="photo-count" role="status"></span><button type="button" id="next-photo" aria-label="Next artwork photograph">→</button></div></div><div class="dialog-copy"><p class="eyebrow">Becoming, in Layers / 2026</p><h2 id="dialog-title"></h2><div id="dialog-description"></div></div></dialog>
</body></html>'''
(dist / 'index.html').write_text(html)
print('Built portfolio with all content, galleries, CV and contact form.')
