#!/usr/bin/env python3
"""Render a thesis LaTeX table to a PNG that matches the thesis PDF.

    python3 table_png.py Thesis/empirical/findings_tables/ladder.tex
    python3 table_png.py <table.tex> --out Seminar/figures/ladder.png --dpi 300
    python3 table_png.py <table.tex> --caption          # keep the thesis caption
    python3 table_png.py <table.tex> --rows 1-6,12      # keep only some body rows

The table file is dropped into a document whose class, font, text width and
caption settings are copied from Thesis/include/packages.tex, so a cell lands
where it lands in the thesis. The `preview` package crops the page to the float,
and pdftoppm rasterises it.

Why the float wrapper stays: `\\caption` only works inside one, and preview's
`floats` option is what makes a floating table render in place. Don't strip the
`\\begin{table}` or the caption errors out.

Citations are stubbed, since a standalone table has no bibliography:
`Foo~\\citep{bar}` renders as `Foo`. Fine for slides, wrong for anything that
needs the reference.

Needs pdflatex and pdftoppm. No third-party Python packages.
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

# a4 with the thesis's 2.5cm side margins
TEXT_WIDTH = '16cm'

# Mirrors Thesis/include/packages.tex, minus everything that only matters to a
# full document (page geometry furniture, headers, bibliography, hyperref).
PREAMBLE = r"""\documentclass[%(pt)spt]{report}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage[australian]{babel}
\usepackage[dvipsnames,svgnames,table]{xcolor}
\usepackage[a4paper,left=2.5cm,right=2.5cm,top=2.5cm,bottom=3cm]{geometry}
\usepackage{setspace}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{longtable}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{rotating}
\usepackage{tikz}
\usepackage{adjustbox}
\usepackage{tabularx}
\usepackage{makecell}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}
\usepackage{enumitem}
\usepackage{float}
\setstretch{1.1}
\captionsetup{labelsep=space,labelfont=bf,font=singlespacing}
%(stubs)s
\usepackage[active,tightpage,floats]{preview}
\setlength{\PreviewBorder}{%(border)s}
\begin{document}
\input{table.tex}
\end{document}
"""

# A standalone table has no bibliography and no cross-reference targets, so
# anything that would print a number is swallowed rather than left to error.
STUBS = r"""\makeatletter
\newcommand{\gobbleopt}[1]{}
\renewcommand{\cite}[2][]{}
\newcommand{\citep}[2][]{}
\newcommand{\citet}[2][]{}
\newcommand{\citeauthor}[2][]{}
\newcommand{\citeyear}[2][]{}
\makeatother"""


def strip_caption(tex):
    """Drop \\caption[...]{...}, brace-matched so nested braces survive."""
    out, i = [], 0
    while True:
        m = re.compile(r'\\caption\*?\s*(\[)?').search(tex, i)
        if not m:
            out.append(tex[i:])
            return ''.join(out)
        out.append(tex[i:m.start()])
        j = m.end()
        if m.group(1):                       # skip the optional short caption
            j = skip_group(tex, j - 1, '[', ']')
        while j < len(tex) and tex[j].isspace():
            j += 1
        if j < len(tex) and tex[j] == '{':
            j = skip_group(tex, j, '{', '}')
        i = j


def skip_group(tex, start, open_c, close_c):
    """Index just past the group that starts at `start`."""
    depth, i = 0, start
    while i < len(tex):
        if tex[i] == '\\':
            i += 2
            continue
        if tex[i] == open_c:
            depth += 1
        elif tex[i] == close_c:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return i


def parse_rows(spec):
    keep = set()
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-')
            keep.update(range(int(a), int(b) + 1))
        else:
            keep.add(int(part))
    return keep


def select_rows(tex, keep):
    """Keep only the listed body rows, counting rows between \\midrule and
    \\bottomrule. Rules and group headers (no & in the line) are kept."""
    lines = tex.split('\n')
    out, n, in_body = [], 0, False
    for line in lines:
        bare = line.strip()
        if bare.startswith('\\midrule') or bare.startswith('\\cmidrule'):
            in_body = True
            out.append(line)
            continue
        if bare.startswith('\\bottomrule'):
            in_body = False
            out.append(line)
            continue
        if in_body and '&' in bare and bare.endswith('\\\\'):
            n += 1
            if n in keep:
                out.append(line)
            continue
        out.append(line)
    return '\n'.join(out)


def render(src, out, dpi, caption, width, pt, border, rows):
    tex = src.read_text()
    if not caption:
        tex = strip_caption(tex)
    if rows:
        tex = select_rows(tex, parse_rows(rows))
    # \textwidth inside the table (adjustbox, tabularx) must be the thesis's,
    # not this document's, or a wide table scales to the wrong size
    tex = f'\\setlength{{\\textwidth}}{{{width}}}\n\\setlength{{\\linewidth}}{{{width}}}\n{tex}'

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / 'table.tex').write_text(tex)
        (tmp / 'doc.tex').write_text(PREAMBLE % {
            'pt': pt, 'stubs': STUBS, 'border': border})
        r = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'doc.tex'],
            cwd=tmp, capture_output=True, text=True)
        pdf = tmp / 'doc.pdf'
        if r.returncode or not pdf.exists():
            log = (tmp / 'doc.log').read_text() if (tmp / 'doc.log').exists() else r.stdout
            err = [l for l in log.splitlines() if l.startswith('!')]
            sys.exit(f'pdflatex failed on {src.name}:\n  ' +
                     '\n  '.join(err[:6] or log.splitlines()[-12:]))
        subprocess.run(['pdftoppm', '-png', '-r', str(dpi), '-singlefile',
                        str(pdf), str(tmp / 'page')], check=True, capture_output=True)
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(tmp / 'page.png', out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('table', help='a .tex file holding one table float')
    ap.add_argument('--out', help='output .png (default: alongside, same stem)')
    ap.add_argument('--dpi', type=int, default=300, help='raster DPI (default: 300)')
    ap.add_argument('--caption', action='store_true',
                    help='keep the thesis caption (default: drop it)')
    ap.add_argument('--width', default=TEXT_WIDTH,
                    help=f'text width the table lays out against (default: {TEXT_WIDTH})')
    ap.add_argument('--pt', type=int, default=11, help='base font size (default: 11)')
    ap.add_argument('--border', default='2pt', help='crop padding (default: 2pt)')
    ap.add_argument('--rows', help='body rows to keep, e.g. "1-6,12"')
    args = ap.parse_args()

    for tool in ('pdflatex', 'pdftoppm'):
        if not shutil.which(tool):
            sys.exit(f'{tool} not found on PATH')

    src = pathlib.Path(args.table).resolve()
    if not src.exists():
        sys.exit(f'no such file: {src}')
    out = pathlib.Path(args.out) if args.out else src.with_suffix('.png')

    render(src, out, args.dpi, args.caption, args.width, args.pt, args.border, args.rows)
    print(f'{out}  ({out.stat().st_size // 1024} KB at {args.dpi} dpi)')


if __name__ == '__main__':
    main()
