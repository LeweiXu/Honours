"""The slide 3 example (one 40-page guidebook, the two pages a question needs) redrawn for
the thesis: smaller thumbnails, larger page crops, a taller canvas. Writes a PDF for
LaTeX and a PNG preview.

    python3 Seminar/make_thesis_multipage.py

Styling, fonts and colours come from make_final_figures.py; only the layout differs.
"""
import shutil, subprocess, tempfile
from pathlib import Path

from make_final_figures import FONT_CSS, FAMILY, GUIDE, NAVY, INK, MUTE, RULE, ORANGE, svg

HERE = Path(__file__).parent
PDF = HERE.parent / "Thesis" / "include" / "multipage_example.pdf"
PNG = HERE / "figures" / "final" / "multipage_thesis.png"

W, H = 874, 346                                   # CSS px; scales to the text width in LaTeX
PW, PH = 583.9, 796.5                             # guidebook page size in points
COLS, TW, TH, GAP, TOP = 8, 26, 35, 5, 46         # thumbnail grid: 8 x 5
CX, CY, CW, CH = 296, 104, 280, 200               # crops: left edge, top, width, height
CGAP = 14


def main():
    work = Path(tempfile.mkdtemp())
    subprocess.run(["pdftoppm", "-r", "72", "-png", str(GUIDE), str(work / "t")], check=True)
    for page in (16, 34):
        subprocess.run(["pdftoppm", "-r", "400", "-png", "-f", str(page), "-l", str(page),
                        str(GUIDE), str(work / "big")], check=True)

    def cell(i):
        return (i % COLS) * (TW + GAP), TOP + (i // COLS) * (TH + GAP)
    thumbs = []
    for i in range(40):
        x, y = cell(i)
        hit = (i + 1) in (16, 34)
        thumbs.append(f'<div class="th{" hit" if hit else ""}" style="left:{x}px; top:{y}px; '
                      f'background-image:url(t-{i + 1:02d}.png)">' + (f"<b>{i + 1}</b>" if hit else "") + "</div>")

    def crop(page, left, label, x0, x1, yc, marks):
        k = CW / ((x1 - x0) * PW)                 # px per point
        ox, oy = x0 * PW * k, yc * PH * k - CH / 2
        rings = "".join(
            f'<i style="left:{a * PW * k - ox:.1f}px; top:{b * PH * k - oy:.1f}px; width:{(c - a) * PW * k:.1f}px; '
            f'height:{(d - b) * PH * k:.1f}px; border-radius:{r}"></i>' for a, b, c, d, r in marks)
        return (f'<div class="crop" style="left:{left}px"><h5>Page {page} <span>{label}</span></h5>'
                f'<div class="win" style="background-image:url(big-{page}.png); background-size:{PW * k:.1f}px {PH * k:.1f}px; '
                f'background-position:{-ox:.1f}px {-oy:.1f}px">{rings}</div></div>')

    left2 = CX + CW + CGAP
    table = crop(16, CX, "table of coffee shops", .088, .522, .772, [(.108, .806, .495, .849, "3px")])
    campus = crop(34, left2, "campus map", .405, .725, .487, [(.538, .473, .578, .502, "50%")])

    x16, y16 = cell(15); x34, y34 = cell(33)
    a16 = (x16 + TW, y16 + TH / 2)
    a34 = (x34 + TW / 2, y34 + TH)
    win_top = CY + 18                              # crop heading is about 18 px tall
    bottom = win_top + CH + 10
    lines = svg(W, H, [
        f'<path d="M{a16[0]} {a16[1]} C {a16[0] + 30} {a16[1]}, {CX - 30} {win_top + 30}, {CX} {win_top + 30}" '
        f'fill="none" stroke="{ORANGE}" stroke-width="1.6"/>',
        f'<path d="M{a34[0]} {a34[1]} C {a34[0]} {bottom}, {a34[0] + 20} {bottom}, {a34[0] + 60} {bottom} '
        f'L {left2 - 20} {bottom} C {left2 - 6} {bottom}, {left2} {bottom - 4}, {left2} {win_top + CH}" '
        f'fill="none" stroke="{ORANGE}" stroke-width="1.6"/>',
    ])
    body = f"""
<div class="cap"><b>One document, 40 pages</b> international student guidebook</div>
{''.join(thumbs)}
<div class="lines">{lines}</div>
<div class="q"><b>Q</b><span>&ldquo;I&rsquo;m at the location &lsquo;J&rsquo; shown in the campus map. Tell me the name of the nearest coffee shop.&rdquo;</span></div>
<div class="a"><b>A</b><span><strong>Ten Years After Caf&eacute;.</strong> The table on page 16 gives its address, and the map on page 34 shows it is beside J.</span></div>
{table}{campus}
"""
    css = f"""
body{{position:relative;}}
.cap{{position:absolute; left:0; top:0; font-size:13px; color:{MUTE};}} .cap b{{display:block; color:{INK};}}
.th{{position:absolute; width:{TW}px; height:{TH}px; background-size:cover; border:1px solid {RULE}; opacity:.5;}}
.th.hit{{opacity:1; border:2px solid {ORANGE}; box-shadow:0 0 0 1.5px #fff, 0 1px 5px rgba(27,31,42,.35); z-index:2;}}
.th b{{position:absolute; left:-2px; top:-2px; background:{ORANGE}; color:#fff; font-size:10px; line-height:1; padding:1.5px 3px;}}
.lines{{position:absolute; left:0; top:0; z-index:1;}}
.q,.a{{position:absolute; left:{CX}px; width:{W - CX}px; display:flex; gap:8px; font-size:14px; line-height:1.28;}}
.q{{top:0; background:#EEF0F8; padding:6px 10px;}} .q b,.a b{{color:{NAVY}; font-size:15.5px; line-height:1.15;}}
.a{{top:50px; padding:0 10px; color:{MUTE};}} .a strong{{color:{INK};}}
.crop{{position:absolute; top:{CY}px; width:{CW}px; z-index:3;}}
.crop h5{{font-size:13px; font-weight:700; color:{ORANGE}; line-height:1; margin-bottom:5px;}}
.crop h5 span{{font-weight:400; color:{MUTE}; margin-left:4px;}}
.win{{position:relative; width:{CW}px; height:{CH}px; overflow:hidden; background-repeat:no-repeat; border:1.5px solid {ORANGE}; background-color:#fff;}}
.win i{{position:absolute; border:2px solid {ORANGE}; background:rgba(237,125,49,.14);}}
"""
    html = work / "multipage_thesis.html"
    html.write_text(
        f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{FONT_CSS}'
        f'@page{{size:{W}px {H}px; margin:0;}} *{{box-sizing:border-box; margin:0; padding:0; -webkit-print-color-adjust:exact; print-color-adjust:exact;}} '
        f'html,body{{width:{W}px; height:{H}px; overflow:hidden; background:#fff; font-family:{FAMILY}; color:{INK};}}{css}'
        f'</style></head><body>{body}</body></html>')
    pdf = work / "multipage_thesis.pdf"
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                    "--allow-file-access-from-files", f"--print-to-pdf={pdf}", html.as_uri()],
                   check=True, capture_output=True)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(pdf, PDF)
    subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", str(PDF), str(PNG.with_suffix(""))], check=True)
    print(PDF, PNG, sep="\n")


if __name__ == "__main__":
    main()
