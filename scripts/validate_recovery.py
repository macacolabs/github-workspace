"""Validate recovery learning material, links, named anchors and visual contracts.
Run: python scripts/validate_recovery.py
Read-only: does not modify source or contact GitHub.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.refs = []
        self.images = []
        self.h1 = 0
        self.forms = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])
        if tag == "img":
            self.images.append(a)
        if tag == "h1":
            self.h1 += 1
        if tag in ("input", "textarea", "form"):
            self.forms += 1

pages = {}
for path in ROOT.rglob("*.html"):
    page = Page()
    page.feed(path.read_text(encoding="utf-8-sig"))
    pages[path.resolve()] = page

errors = []
recovery = sorted((ROOT / "labs/recovery").glob("*.html"))
if len(recovery) != 8:
    errors.append("Expected 8 recovery pages")
for path in recovery:
    page = pages[path.resolve()]
    if page.h1 != 1 or page.forms:
        errors.append(f"Invalid title/form contract: {path.name}")
    if len(page.ids) != len(set(page.ids)):
        errors.append(f"Duplicate anchor: {path.name}")
    for a in page.images:
        if not all(a.get(key) for key in ("alt", "width", "height")):
            errors.append(f"Image lacks alt/dimensions: {path.name}")
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
        if not target.exists():
            errors.append(f"Missing target: {path.name}: {ref}")
        if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"Missing anchor: {path.name}: {ref}")
    if path.name[:2].isdigit() and int(path.name[:2]) <= 5:
        text = path.read_text(encoding="utf-8")
        for section in ("내부에서는", "시작 상태", "진단", "선택", "검증", "멈춰야"):
            if section not in text:
                errors.append(f"Missing teaching section {section}: {path.name}")
        if not page.images:
            errors.append(f"Missing diagram: {path.name}")

for path in (ROOT / "assets/visuals").glob("*.svg"):
    svg = ET.parse(path).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    if svg.find(ns + "title") is None or svg.find(ns + "desc") is None:
        errors.append(f"Missing SVG description: {path.name}")

for folder in ("chapters", "labs"):
    for path in (ROOT / folder).glob("*.html"):
        text = path.read_text(encoding="utf-8-sig")
        if "recovery/" not in text:
            errors.append(f"No recovery connection: {path.name}")

if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS recovery_pages={len(recovery)} links, anchors, image descriptions, learning sections, existing-page connections")
