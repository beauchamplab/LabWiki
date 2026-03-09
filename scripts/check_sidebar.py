#!/usr/bin/env python3
"""Quick check of sidebar hierarchy in built HTML."""
from html.parser import HTMLParser

class NavParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_nav = False
        self.depth = 0
        self.links = []
        self.current_text = ''

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        if 'site-nav' in cls:
            self.in_nav = True
        if self.in_nav:
            if tag == 'ul':
                self.depth += 1
            if tag == 'a' and 'nav-list-link' in cls:
                self.current_text = ''

    def handle_endtag(self, tag):
        if self.in_nav:
            if tag == 'a' and self.current_text:
                self.links.append((self.depth, self.current_text.strip()))
                self.current_text = ''
            if tag == 'ul':
                self.depth -= 1
            if tag == 'nav':
                self.in_nav = False

    def handle_data(self, data):
        if self.in_nav:
            self.current_text += data

with open('_site/pages/Beauchamp/index.html') as f:
    html = f.read()

p = NavParser()
p.feed(html)

beauchamp_depth = None
for depth, text in p.links:
    if text == 'Beauchamp Lab Wiki':
        beauchamp_depth = depth
        print(f'[Beauchamp Lab Wiki]')
        continue
    if beauchamp_depth is not None:
        rel = depth - beauchamp_depth
        if rel == 1:
            print(f'  +-- {text}')
        elif rel == 2:
            print(f'      +-- {text}')
        elif rel <= 0:
            break
