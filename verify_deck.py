#!/usr/bin/env python3
"""Check that a deck actually exports the way it looks.

For a directory of slideN.html plus deck.html, this:
  1. screenshots every slide to PNG so you can look at them
  2. prints deck.html to PDF and checks page count and page size
  3. prints each slide standalone and diffs it against the matching deck page

A nonzero diff means the stacked deck and the standalone slide disagree, which
is nearly always a print-CSS problem (see "Known traps" in SKILL.md).

    python3 verify_deck.py [slides-dir] [--only 1,2,3,4] [--out DIR]

Needs a Chrome/Chromium binary and pdftoppm (poppler-utils). No Python deps.
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

CHROME = next((c for c in ('google-chrome', 'google-chrome-stable', 'chromium',
                           'chromium-browser', 'chrome') if shutil.which(c)), None)


def chrome(*args):
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-sandbox',
                    '--hide-scrollbars', *args],
                   check=True, capture_output=True)


def read_ppm(path):
    """Minimal binary-PPM reader so this script needs no Pillow."""
    data = path.read_bytes()
    fields, i = [], 0
    while len(fields) < 4:
        while data[i:i + 1].isspace():
            i += 1
        if data[i:i + 1] == b'#':
            while data[i:i + 1] not in (b'\n', b''):
                i += 1
            continue
        j = i
        while not data[j:j + 1].isspace():
            j += 1
        fields.append(data[i:j])
        i = j
    w, h = int(fields[1]), int(fields[2])
    return w, h, data[i + 1: i + 1 + w * h * 3]


def mean_diff(a, b):
    """Mean absolute channel difference over a stride-sampled subset."""
    wa, ha, pa = read_ppm(a)
    wb, hb, pb = read_ppm(b)
    if (wa, ha) != (wb, hb):
        return None
    step, total, n = 301, 0, 0
    for k in range(0, len(pa), step):
        total += abs(pa[k] - pb[k])
        n += 1
    return total / n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slides_dir', nargs='?', default='.')
    ap.add_argument('--only', help='comma-separated slide numbers the deck contains, '
                                   'in order (default: every slide*.html found)')
    ap.add_argument('--out', help='where to put screenshots (default: <slides-dir>/_check)')
    args = ap.parse_args()

    if not CHROME:
        sys.exit('no chrome/chromium binary found')
    if not shutil.which('pdftoppm'):
        sys.exit('pdftoppm not found (install poppler-utils)')

    root = pathlib.Path(args.slides_dir).resolve()
    deck = root / 'deck.html'
    if not deck.exists():
        sys.exit(f'{deck} not found (run build_deck.py first)')

    if args.only:
        slides = [root / f'slide{n.strip()}.html' for n in args.only.split(',')]
        missing = [p.name for p in slides if not p.exists()]
        if missing:
            sys.exit(f'--only names slides that do not exist: {", ".join(missing)}')
    else:
        slides = sorted(root.glob('slide*.html'),
                        key=lambda p: int(re.search(r'slide(\d+)', p.name).group(1)))
    out = pathlib.Path(args.out) if args.out else root / '_check'
    out.mkdir(parents=True, exist_ok=True)

    print(f'{len(slides)} slides in {root}\n')

    print('screenshots')
    for p in slides:
        shot = out / f'{p.stem}.png'
        chrome('--window-size=1400,900', f'--screenshot={shot}',
               '--virtual-time-budget=8000', p.as_uri())
        print(f'  {shot}')

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        deck_pdf = out / 'deck.pdf'
        chrome('--no-pdf-header-footer', f'--print-to-pdf={deck_pdf}',
               '--virtual-time-budget=12000', deck.as_uri())

        raw = deck_pdf.read_bytes()
        pages = raw.count(b'/Type /Page') - raw.count(b'/Type /Pages')
        boxes = set(re.findall(rb'/MediaBox \[[^\]]*\]', raw))
        ok = pages == len(slides)
        print(f'\nprint: {pages} pages ({"ok" if ok else "EXPECTED " + str(len(slides))}), '
              f'size {b" ".join(sorted(boxes)).decode()}')
        if len(boxes) > 1:
            print('  WARNING: pages are not all the same size')

        subprocess.run(['pdftoppm', '-r', '96', str(deck_pdf), str(tmp / 'dk')], check=True)

        print('\ndeck page vs standalone slide')
        worst = 0.0
        for n, p in enumerate(slides, 1):
            one_pdf = tmp / f'one{n}.pdf'
            chrome('--no-pdf-header-footer', f'--print-to-pdf={one_pdf}',
                   '--virtual-time-budget=8000', p.as_uri())
            subprocess.run(['pdftoppm', '-r', '96', '-f', '1', '-l', '1',
                            str(one_pdf), str(tmp / f'one{n}')], check=True)
            deck_page = tmp / f'dk-{n}.ppm'
            if not deck_page.exists():
                print(f'  page {n}: MISSING from deck')
                ok = False
                continue
            d = mean_diff(tmp / f'one{n}-1.ppm', deck_page)
            if d is None:
                print(f'  page {n}: size mismatch')
                ok = False
                continue
            worst = max(worst, d)
            flag = '' if d < 1.0 else '   <-- DIFFERS'
            print(f'  page {n}  {p.name:<16} meandiff={d:.2f}{flag}')
            ok = ok and d < 1.0

        print(f'\n{"PASS" if ok else "FAIL"} (worst diff {worst:.2f}; '
              f'under 1.0 is antialiasing noise)')
        print(f'screenshots in {out}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
