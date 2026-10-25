"""Check generated pages, gallery images and deployable asset references."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

root = Path(__file__).parent
dist = root / 'dist'

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.anchors = []
        self.assets = []
        self.works = 0
        self.archive = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.anchors.append(attrs['href'][1:])
        if tag in ('img', 'script') and attrs.get('src'):
            self.assets.append(attrs['src'])
        if tag == 'link' and attrs.get('href'):
            self.assets.append(attrs['href'])
        if 'data-photos' in attrs:
            self.works += 1
            for photo in json.loads(attrs['data-photos']):
                self.assets.append(photo['src'])
        if 'data-archive' in attrs:
            self.archive += 1

parser = SiteParser()
parser.feed((dist / 'index.html').read_text())
assert len(parser.ids) == len(set(parser.ids)), 'Duplicate element IDs'
assert all(anchor in parser.ids for anchor in parser.anchors), 'Broken navigation links'
assert parser.works == 6 and parser.archive == 6, 'Missing artwork or archive entries'
for name in ('styles.css', 'content.css'):
    parser.assets.extend(re.findall(r'url\([\'"]?([^\)\'\"]+)', (dist / name).read_text()))
for asset in parser.assets:
    url = urlsplit(asset)
    if url.scheme or url.netloc:
        continue
    path = (dist / unquote(url.path).lstrip('/')).resolve()
    assert path.is_relative_to(dist.resolve()) and path.is_file(), f'Missing or invalid asset: {url.path}'
    if path.suffix.lower() in ('.jpg', '.jpeg'):
        assert path.read_bytes()[:2] == b'\xff\xd8', f'Non-JPEG content in {path.name}'
assert not list(dist.rglob('.env*')), 'Private configuration in public output'
assert not (dist / 'node_modules').exists(), 'Dependencies in public output'
print('Site check passed: six artworks, six archive entries, valid navigation and image assets.')
