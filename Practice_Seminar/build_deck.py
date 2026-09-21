"""Stitch slide1..slide6 into one printable deck.html.

Each slideN.html is a standalone page: the same shared chrome CSS, then its own
block marked `/* ===== SLIDE n`, then the print rules. This pulls the chrome off
slide1, every slide's own block, and every slide's markup, and writes deck.html.

Run it again after editing any slide, or the deck drifts from the standalone files:
    python3 build_deck.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
MARK = '  /* ================= SLIDE '

# Which slides go into deck.html, in order.
DECK_SLIDES = [1, 2, 3, 4, 5, 6, 7]


def style_of(name):
    src = (ROOT / name).read_text()
    return re.search(r'<style>\n(.*?)\n</style>', src, re.S).group(1)


def markup_of(name):
    src = (ROOT / name).read_text()
    return re.search(r'(<div class="slide">.*?\n</div>)\n</body>', src, re.S).group(1)


s1 = style_of('slide1.html')
BASE = s1.split(MARK)[0].rstrip()
PRINT = '  /* ---------- PRINT' + s1.split('  /* ---------- PRINT')[1].rstrip()

blocks = []
for n in DECK_SLIDES:
    css = style_of(f'slide{n}.html')
    blocks.append(MARK + css.split(MARK)[1].split('  /* ---------- PRINT')[0].rstrip())

DECK = """
  /* ---------- DECK: slides stacked, one per printed page ---------- */
  html,body{height:auto;}
  body{
    display:flex; flex-direction:column; align-items:center;
    gap:44px; padding:44px 0;
  }
"""

DECK_PRINT = """
  /* ---------- DECK PRINT: keep the stack one slide per page ---------- */
  @media print{
    body{gap:0; padding:0;}
    .slide{break-inside:avoid; page-break-inside:avoid;}
  }
"""

slides = '\n\n'.join(markup_of(f'slide{n}.html') for n in DECK_SLIDES)

head = (ROOT / 'slide1.html').read_text().split('<style>')[0]
head = re.sub(r'<title>.*?</title>',
              '<title>MP-VRDU: Managing Evidence at Document Scale</title>', head, flags=re.S)

out = (head + '<style>\n' + BASE + '\n' + DECK + '\n' +
       '\n\n'.join(blocks) + '\n\n' + PRINT + '\n' + DECK_PRINT +
       '</style>\n</head>\n<body>\n\n' + slides + '\n\n</body>\n</html>\n')

(ROOT / 'deck.html').write_text(out)
print('deck.html written:', len(out), 'bytes;', out.count('<div class="slide">'), 'slides')
