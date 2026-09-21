#!/usr/bin/env python3
"""Stitch slide1.html .. slideN.html into one printable deck.html.

Each slideN.html is a standalone page: shared chrome CSS, then its own block
marked `/* ================= SLIDE n`, then the print rules. This pulls the
chrome off slide 1, every slide's own block, and every slide's markup.

Run it again after editing any slide, or the deck drifts from the slide files.

    python3 build_deck.py [slides-dir] [--only 1,2,3,4]

--only picks which slides go into the deck, in that order. Without it every
slide*.html in the directory is included, numerically sorted. Use it to hold
slides back from the deck while keeping their files.
"""
import re
import sys
import pathlib

ONLY = None
argv = sys.argv[1:]
if '--only' in argv:
    i = argv.index('--only')
    ONLY = [int(x) for x in argv[i + 1].split(',')]
    del argv[i:i + 2]

ROOT = pathlib.Path(argv[0] if argv else __file__).resolve()
ROOT = ROOT if ROOT.is_dir() else ROOT.parent
MARK = '  /* ================= SLIDE '
PRINT_MARK = '  /* ---------- PRINT'

if ONLY:
    SLIDES = [ROOT / f'slide{n}.html' for n in ONLY]
    missing = [p.name for p in SLIDES if not p.exists()]
    if missing:
        sys.exit(f'--only names slides that do not exist: {", ".join(missing)}')
else:
    SLIDES = sorted(
        ROOT.glob('slide*.html'),
        key=lambda p: int(re.search(r'slide(\d+)', p.name).group(1)),
    )
if not SLIDES:
    sys.exit(f'no slide*.html found in {ROOT}')


def style_of(path):
    return re.search(r'<style>\n(.*?)\n</style>', path.read_text(), re.S).group(1)


def markup_of(path):
    # the modifier class (slide s1, slide s2, ...) is what scopes each slide's
    # own CSS, so the pattern has to tolerate it
    return re.search(r'(<div class="slide[^"]*">.*?\n</div>)\n</body>',
                     path.read_text(), re.S).group(1)


first = style_of(SLIDES[0])
BASE = first.split(MARK)[0].rstrip()
PRINT = PRINT_MARK + first.split(PRINT_MARK)[1].rstrip()

blocks = []
for path in SLIDES:
    css = style_of(path)
    if MARK not in css:
        sys.exit(f'{path.name} has no "{MARK.strip()}" marker comment')
    blocks.append(MARK + css.split(MARK)[1].split(PRINT_MARK)[0].rstrip())

# On screen the slides stack with breathing room; in print that spacing must go,
# and each slide must stay atomic so nothing fragments across a page boundary.
DECK = """
  /* ---------- DECK: slides stacked, one per printed page ---------- */
  html,body{height:auto;}
  body{
    display:flex; flex-direction:column; align-items:center;
    gap:44px; padding:44px 0;
  }
"""

DECK_PRINT = """
  /* ---------- DECK PRINT: must stay last, @media print adds no specificity ---------- */
  @media print{
    body{gap:0; padding:0;}
    .slide{break-inside:avoid; page-break-inside:avoid;}
  }
"""

head = SLIDES[0].read_text().split('<style>')[0]
head = re.sub(r'<title>.*?</title>', '<title>Deck</title>', head, flags=re.S)

out = (head + '<style>\n' + BASE + '\n' + DECK + '\n' +
       '\n\n'.join(blocks) + '\n\n' + PRINT + '\n' + DECK_PRINT +
       '</style>\n</head>\n<body>\n\n' +
       '\n\n'.join(markup_of(p) for p in SLIDES) +
       '\n\n</body>\n</html>\n')

(ROOT / 'deck.html').write_text(out)
print(f'deck.html written: {len(out)} bytes, {len(SLIDES)} slides '
      f'({", ".join(p.name for p in SLIDES)})')
