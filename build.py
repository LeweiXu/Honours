#!/usr/bin/env python3
"""Build a slide deck: slide*.html -> deck.html -> deck.pdf -> deck.pptx.

Point it at a directory of standalone slide files and it writes all three
outputs next to them.

    python3 build.py Seminar
    python3 build.py Seminar --only 1,2,5
    python3 build.py Seminar --dpi 200 --no-pptx

Each slideN.html is a complete page: the shared chrome CSS, then its own block
marked `/* ================= SLIDE n`, then the print rules. Stage one lifts the
chrome off the first slide, every slide's own block, and every slide's markup,
and stitches them into deck.html. Rerun after editing any slide or the deck
drifts from the slide files.

Stage two prints deck.html through headless Chrome. Stage three rasterises those
pages with pdftoppm and wraps them in a pptx, one full-page image per slide, so
there are no fonts or colours left for PowerPoint to mis-render.

Needs google-chrome (or chromium) for the PDF and pdftoppm (poppler-utils) for
the pptx. Missing either one, that stage is skipped with a warning and the rest
still runs. No third-party Python packages.
"""
import argparse
import glob
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

MARK = '  /* ================= SLIDE '
PRINT_MARK = '  /* ---------- PRINT'

CHROME = next((c for c in ('google-chrome', 'google-chrome-stable', 'chromium',
                           'chromium-browser', 'chrome') if shutil.which(c)), None)

# 16:9 at 13.333 x 7.5in, in English Metric Units (914400 per inch)
SLIDE_W, SLIDE_H = 12192000, 6858000


# ---------------------------------------------------------------- stage 1: html

def find_slides(root, only):
    if only:
        paths = [root / f'slide{n}.html' for n in only]
        missing = [p.name for p in paths if not p.exists()]
        if missing:
            sys.exit(f'--only names slides that do not exist: {", ".join(missing)}')
        return paths
    paths = sorted(root.glob('slide*.html'),
                   key=lambda p: int(re.search(r'slide(\d+)', p.name).group(1)))
    if not paths:
        sys.exit(f'no slide*.html found in {root}')
    return paths


def style_of(path):
    return re.search(r'<style>\n(.*?)\n</style>', path.read_text(), re.S).group(1)


def markup_of(path):
    # the modifier class (slide s1, slide s2, ...) is what scopes each slide's
    # own CSS, so the pattern has to tolerate it
    m = re.search(r'(<div class="slide[^"]*">.*?\n</div>)\n</body>',
                  path.read_text(), re.S)
    if not m:
        sys.exit(f'{path.name}: no <div class="slide ...">...</div> right before </body>')
    return m.group(1)


# On screen the slides stack with breathing room; in print that spacing must go,
# and each slide must stay atomic so nothing fragments across a page boundary.
DECK_CSS = """
  /* ---------- DECK: slides stacked, one per printed page ---------- */
  html,body{height:auto;}
  body{
    display:flex; flex-direction:column; align-items:center;
    gap:44px; padding:44px 0;
  }
"""

DECK_PRINT_CSS = """
  /* ---------- DECK PRINT: must stay last, @media print adds no specificity ---------- */
  @media print{
    body{gap:0; padding:0;}
    .slide{break-inside:avoid; page-break-inside:avoid;}
  }
"""


def build_html(slides, out):
    first = style_of(slides[0])
    chrome_css = first.split(MARK)[0].rstrip()
    print_css = PRINT_MARK + first.split(PRINT_MARK)[1].rstrip()

    blocks = []
    for path in slides:
        css = style_of(path)
        if MARK not in css:
            sys.exit(f'{path.name} has no "{MARK.strip()}" marker comment')
        blocks.append(MARK + css.split(MARK)[1].split(PRINT_MARK)[0].rstrip())

    head = slides[0].read_text().split('<style>')[0]
    head = re.sub(r'<title>.*?</title>', f'<title>{out.stem}</title>', head, flags=re.S)

    out.write_text(
        head + '<style>\n' + chrome_css + '\n' + DECK_CSS + '\n' +
        '\n\n'.join(blocks) + '\n\n' + print_css + '\n' + DECK_PRINT_CSS +
        '</style>\n</head>\n<body>\n\n' +
        '\n\n'.join(markup_of(p) for p in slides) +
        '\n\n</body>\n</html>\n')
    return out


# ----------------------------------------------------------------- stage 2: pdf

def build_pdf(html, out, wait_ms):
    """Print the stacked deck through headless Chrome.

    The @page rule in the slide CSS sets the page size, so nothing here needs to
    name one. virtual-time-budget is what gives the webfonts time to land; too
    short and the deck prints in a fallback face.
    """
    flags = ['--headless', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
             f'--virtual-time-budget={wait_ms}', f'--print-to-pdf={out}']
    # the flag that suppresses Chrome's own date/URL header was renamed; older
    # builds only know the old spelling, so fall back rather than print furniture
    for suppress in ('--no-pdf-header-footer', '--print-to-pdf-no-header'):
        r = subprocess.run([CHROME, *flags, suppress, html.as_uri()],
                           capture_output=True, text=True)
        if r.returncode == 0 and out.exists():
            return out
    sys.exit(f'chrome failed to print {html.name}:\n{r.stderr.strip()[:800]}')


# ---------------------------------------------------------------- stage 3: pptx
#
# A pptx is a zip of OOXML parts. Writing it by hand keeps this script free of
# third-party packages; the parts below are the minimum PowerPoint will open:
# a presentation, one master, one blank layout, a theme, and one slide per page
# holding a single full-bleed picture.

XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
NS_P = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" ' \
       'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ' \
       'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
REL_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
EMPTY_TREE = (
    '<p:spTree>'
    '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
    '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
    '</p:spTree>'
)


def rels(*entries):
    body = ''.join(
        f'<Relationship Id="{rid}" Type="{REL_NS}/{kind}" Target="{target}"/>'
        for rid, kind, target in entries)
    return (XML + '<Relationships xmlns="http://schemas.openxmlformats.org/'
            f'package/2006/relationships">{body}</Relationships>')


def theme_xml():
    """One neutral theme. Nothing reads from it, but the master requires one."""
    def scheme():
        slots = [('dk1', 'sysClr', 'windowText'), ('lt1', 'sysClr', 'window'),
                 ('dk2', 'srgbClr', '44546A'), ('lt2', 'srgbClr', 'E7E6E6')]
        out = ''
        for name, tag, val in slots:
            inner = (f'<a:sysClr val="{val}" lastClr="'
                     f'{"000000" if val == "windowText" else "FFFFFF"}"/>'
                     if tag == 'sysClr' else f'<a:srgbClr val="{val}"/>')
            out += f'<a:{name}>{inner}</a:{name}>'
        for i, val in enumerate(('4472C4', 'ED7D31', 'A5A5A5', 'FFC000',
                                 '5B9BD5', '70AD47'), 1):
            out += f'<a:accent{i}><a:srgbClr val="{val}"/></a:accent{i}>'
        out += '<a:hlink><a:srgbClr val="0563C1"/></a:hlink>'
        out += '<a:folHlink><a:srgbClr val="954F72"/></a:folHlink>'
        return out

    fill = ('<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
            '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
            '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>')
    line = ('<a:ln w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill>'
            '<a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>')
    return (
        XML +
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'name="Deck"><a:themeElements>'
        f'<a:clrScheme name="Deck">{scheme()}</a:clrScheme>'
        '<a:fontScheme name="Deck">'
        '<a:majorFont><a:latin typeface="Calibri Light"/><a:ea typeface=""/>'
        '<a:cs typeface=""/></a:majorFont>'
        '<a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/>'
        '<a:cs typeface=""/></a:minorFont></a:fontScheme>'
        '<a:fmtScheme name="Deck">'
        f'<a:fillStyleLst>{fill}</a:fillStyleLst>'
        f'<a:lnStyleLst>{line * 3}</a:lnStyleLst>'
        '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle>'
        '<a:effectStyle><a:effectLst/></a:effectStyle>'
        '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
        f'<a:bgFillStyleLst>{fill}</a:bgFillStyleLst>'
        '</a:fmtScheme></a:themeElements>'
        '<a:objectDefaults/><a:extraClrSchemeLst/></a:theme>')


def build_pptx(images, out):
    n = len(images)
    z = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)

    overrides = ''.join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType='
        '"application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, n + 1))
    z.writestr('[Content_Types].xml', XML +
               '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
               '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
               '<Default Extension="xml" ContentType="application/xml"/>'
               '<Default Extension="png" ContentType="image/png"/>'
               '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
               '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
               '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
               '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
               f'{overrides}</Types>')

    z.writestr('_rels/.rels', rels(('rId1', 'officeDocument', 'ppt/presentation.xml')))

    # rId1 is the master, then one rId per slide in order
    sld_ids = ''.join(f'<p:sldId id="{255 + i}" r:id="rId{i + 1}"/>'
                      for i in range(1, n + 1))
    z.writestr('ppt/presentation.xml', XML +
               f'<p:presentation {NS_P}>'
               '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
               f'<p:sldIdLst>{sld_ids}</p:sldIdLst>'
               f'<p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}"/>'
               '<p:notesSz cx="6858000" cy="9144000"/>'
               '</p:presentation>')
    z.writestr('ppt/_rels/presentation.xml.rels', rels(
        ('rId1', 'slideMaster', 'slideMasters/slideMaster1.xml'),
        *[(f'rId{i + 1}', 'slide', f'slides/slide{i}.xml') for i in range(1, n + 1)],
        (f'rId{n + 2}', 'theme', 'theme/theme1.xml')))

    z.writestr('ppt/slideMasters/slideMaster1.xml', XML +
               f'<p:sldMaster {NS_P}><p:cSld>{EMPTY_TREE}</p:cSld>'
               '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" '
               'accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" '
               'accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
               '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
               '</p:sldMaster>')
    z.writestr('ppt/slideMasters/_rels/slideMaster1.xml.rels', rels(
        ('rId1', 'slideLayout', '../slideLayouts/slideLayout1.xml'),
        ('rId2', 'theme', '../theme/theme1.xml')))

    z.writestr('ppt/slideLayouts/slideLayout1.xml', XML +
               f'<p:sldLayout {NS_P} type="blank" preserve="1">'
               f'<p:cSld name="Blank">{EMPTY_TREE}</p:cSld>'
               '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
    z.writestr('ppt/slideLayouts/_rels/slideLayout1.xml.rels', rels(
        ('rId1', 'slideMaster', '../slideMasters/slideMaster1.xml')))

    z.writestr('ppt/theme/theme1.xml', theme_xml())

    for i, img in enumerate(images, 1):
        z.write(img, f'ppt/media/image{i}.png')
        z.writestr(f'ppt/slides/slide{i}.xml', XML +
                   f'<p:sld {NS_P}><p:cSld><p:spTree>'
                   '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
                   '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
                   '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
                   '<p:pic><p:nvPicPr>'
                   f'<p:cNvPr id="2" name="Slide {i}"/>'
                   '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/>'
                   '</p:nvPicPr>'
                   '<p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
                   f'<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_W}" cy="{SLIDE_H}"/></a:xfrm>'
                   '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
                   '</p:pic></p:spTree></p:cSld>'
                   '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
        z.writestr(f'ppt/slides/_rels/slide{i}.xml.rels', rels(
            ('rId1', 'slideLayout', '../slideLayouts/slideLayout1.xml'),
            ('rId2', 'image', f'../media/image{i}.png')))

    z.close()
    return out


def rasterise(pdf, tmp, dpi):
    subprocess.run(['pdftoppm', '-png', '-r', str(dpi), str(pdf),
                    os.path.join(tmp, 'page')], check=True, capture_output=True)
    return sorted(glob.glob(os.path.join(tmp, 'page*.png')))


# ------------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('slides_dir', help='directory holding slide1.html, slide2.html, ...')
    ap.add_argument('--only', help='comma-separated slide numbers, in deck order')
    ap.add_argument('--name', default='deck', help='output basename (default: deck)')
    ap.add_argument('--dpi', type=int, default=144,
                    help='raster DPI for the pptx; 144 gives 1920x1080 (default: 144)')
    ap.add_argument('--wait', type=int, default=6000,
                    help='ms to let webfonts load before printing (default: 6000)')
    ap.add_argument('--no-pdf', action='store_true', help='stop after deck.html')
    ap.add_argument('--no-pptx', action='store_true', help='stop after deck.pdf')
    args = ap.parse_args()

    root = pathlib.Path(args.slides_dir).resolve()
    if not root.is_dir():
        sys.exit(f'not a directory: {root}')
    only = [int(x) for x in args.only.split(',')] if args.only else None

    slides = find_slides(root, only)
    html = build_html(slides, root / f'{args.name}.html')
    print(f'{html.name:<12} {len(slides)} slides  '
          f'({", ".join(p.name for p in slides)})')

    if args.no_pdf:
        return
    if not CHROME:
        print('! no chrome/chromium on PATH, skipping pdf and pptx')
        return
    pdf = build_pdf(html, root / f'{args.name}.pdf', args.wait)
    print(f'{pdf.name:<12} {pdf.stat().st_size // 1024} KB')

    if args.no_pptx:
        return
    if not shutil.which('pdftoppm'):
        print('! no pdftoppm on PATH (apt install poppler-utils), skipping pptx')
        return
    with tempfile.TemporaryDirectory() as tmp:
        images = rasterise(pdf, tmp, args.dpi)
        if len(images) != len(slides):
            print(f'! pdf has {len(images)} pages for {len(slides)} slides')
        pptx = build_pptx(images, root / f'{args.name}.pptx')
    print(f'{pptx.name:<12} {pptx.stat().st_size // 1024} KB  '
          f'({len(images)} pages at {args.dpi} dpi)')


if __name__ == '__main__':
    main()
