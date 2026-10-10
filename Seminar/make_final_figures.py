"""Figures for Seminar_final.pptx: HTML drawn here, printed to PDF by headless Chrome, then
rasterised by pdftoppm.

    python3 make_final_figures.py            # write figures/final/*.png
    python3 make_final_figures.py --embed    # and swap them into Seminar_final.pptx

Each PNG is sized in inches to the picture box it fills on the slide. --embed replaces the
image behind the pictures named fig_* in the pptx and touches nothing else (needs python-pptx).
"""
import json, subprocess, sys, tempfile
from pathlib import Path

SEM = Path(__file__).parent
OUT = SEM / "figures" / "final"
PPTX = SEM / "Seminar_final.pptx"
GUIDE = Path.home() / "mpvrdu/.data/mmlongbench/documents/guojixueshengshenghuozhinanyingwen9.1.pdf"
WINFONTS = Path("/mnt/c/Windows/Fonts")

# the pptx's own colours
NAVY, INK, MUTE, RULE, ORANGE = "#27348B", "#1B1F2A", "#5A6072", "#C9CDD9", "#ED7D31"
PALE, GRID = "#BFC5E3", "#E6E8F0"
PX = 96      # CSS pixels per slide inch
SCALE = 4    # rasterise at 384 dpi

FONT_CSS = "".join(
    f"@font-face{{font-family:'Calibri'; src:url('file://{WINFONTS / f}'); font-weight:{w}; font-style:{s};}}"
    for f, w, s in (("calibri.ttf", 400, "normal"), ("calibrib.ttf", 700, "normal"),
                    ("calibrii.ttf", 400, "italic"), ("calibriz.ttf", 700, "italic"))
    if (WINFONTS / f).exists())
FAMILY = "Calibri, Carlito, sans-serif"

T = lambda x, y, s, size=11, anchor="middle", fill=INK, weight=400, style="normal": (
    f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" '
    f'font-weight="{weight}" font-style="{style}">{s}</text>')
R = lambda x, y, w, h, fill: f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"/>'
L = lambda x1, y1, x2, y2, stroke=GRID, w=1, dash="": (
    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}"'
    + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")

def svg(w, h, parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{FAMILY}">' + "".join(parts) + "</svg>")

def render(name, w, h, body, css="", workdir=None):
    """Print `body` as one w x h CSS pixel page and rasterise it into figures/final/<name>.png."""
    work = Path(workdir or tempfile.mkdtemp())
    html = work / f"{name}.html"
    html.write_text(
        f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{FONT_CSS}'
        f'@page{{size:{w}px {h}px; margin:0;}} *{{box-sizing:border-box; margin:0; padding:0; -webkit-print-color-adjust:exact; print-color-adjust:exact;}} html,body{{width:{w}px; height:{h}px; overflow:hidden; '
        f'background:#fff; font-family:{FAMILY}; color:{INK}; -webkit-font-smoothing:antialiased;}}{css}'
        f'</style></head><body>{body}</body></html>')
    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / f"{name}.png"
    pdf = work / f"{name}.pdf"
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                    "--allow-file-access-from-files", f"--print-to-pdf={pdf}", html.as_uri()],
                   check=True, capture_output=True)
    subprocess.run(["pdftoppm", "-r", str(PX * SCALE), "-png", "-singlefile", "-f", "1", "-l", "1",
                    str(pdf), str(png.with_suffix(""))], check=True)
    print(f"{png.relative_to(SEM)}  {w / PX:.2f} x {h / PX:.2f} in")

# ---------------------------------------------------------- slide 3: one long document

def multipage():
    """A 40-page guidebook as thumbnails, with the two pages one question needs pulled out."""
    W, H = 874, 226
    work = Path(tempfile.mkdtemp())
    subprocess.run(["pdftoppm", "-r", "36", "-png", str(GUIDE), str(work / "t")], check=True)
    for page in (16, 34):
        subprocess.run(["pdftoppm", "-r", "260", "-png", "-f", str(page), "-l", str(page), str(GUIDE), str(work / "big")], check=True)
    PW, PH = 583.9, 796.5                      # page size in points
    tw, th, gap, top = 34, 46, 5, 22
    cells = []
    for i in range(40):
        x, y = (i % 10) * (tw + gap), top + (i // 10) * (th + gap)
        hit = (i + 1) in (16, 34)
        cells.append(f'<div class="th{" hit" if hit else ""}" style="left:{x}px; top:{y}px; '
                     f'background-image:url(t-{i + 1:02d}.png)">' + (f"<b>{i + 1}</b>" if hit else "") + "</div>")

    def crop(page, left, label, x0, x1, yc, marks):
        """Show the page strip x0..x1 (fractions of the page) centred on yc, 215 x 118 px."""
        cw, ch = 215, 118
        k = cw / ((x1 - x0) * PW)              # px per point
        ox, oy = x0 * PW * k, yc * PH * k - ch / 2
        rings = "".join(
            f'<i style="left:{a * PW * k - ox:.1f}px; top:{b * PH * k - oy:.1f}px; width:{(c - a) * PW * k:.1f}px; '
            f'height:{(d - b) * PH * k:.1f}px; border-radius:{r}"></i>' for a, b, c, d, r in marks)
        return (f'<div class="crop" style="left:{left}px"><h5>Page {page} <span>{label}</span></h5>'
                f'<div class="win" style="background-image:url(big-{page}.png); background-size:{PW * k:.1f}px {PH * k:.1f}px; '
                f'background-position:{-ox:.1f}px {-oy:.1f}px">{rings}</div></div>')

    table = crop(16, 425, "table of coffee shops", .088, .522, .765, [(.108, .806, .495, .849, "3px")])
    campus = crop(34, 659, "campus map", .385, .745, .485, [(.538, .473, .578, .502, "50%")])
    # thumbnail centres, for the lines out to the two crops
    c16 = (5 * (tw + gap) + tw, top + 1 * (th + gap) + th / 2)
    c34 = (3 * (tw + gap) + tw, top + 3 * (th + gap) + th / 2)
    lines = svg(W, H, [
        f'<path d="M{c16[0]} {c16[1]} C {c16[0] + 90} {c16[1]}, 340 96, 425 100" fill="none" stroke="{ORANGE}" stroke-width="1.6"/>',
        f'<path d="M{c34[0]} {c34[1]} C {c34[0] + 110} {c34[1]}, 330 216, 440 216 L 628 216 C 648 216, 652 210, 659 200" fill="none" stroke="{ORANGE}" stroke-width="1.6"/>',
    ])
    body = f"""
<div class="cap"><b>One document, 40 pages</b> international student guidebook</div>
{''.join(cells)}
<div class="lines">{lines}</div>
<div class="q"><b>Q</b><span>&ldquo;I&rsquo;m at the location &lsquo;J&rsquo; shown in the campus map. Tell me the name of the nearest coffee shop.&rdquo;</span></div>
{table}{campus}
<div class="a"><b>A</b><span><strong>Ten Years After Caf&eacute;.</strong> The table gives its address, the map shows it is beside J.</span></div>
"""
    css = f"""
body{{position:relative;}}
.cap{{position:absolute; left:0; top:0; font-size:12px; color:{MUTE};}} .cap b{{color:{INK}; margin-right:6px;}}
.th{{position:absolute; width:{tw}px; height:{th}px; background-size:cover; border:1px solid {RULE}; opacity:.5;}}
.th.hit{{opacity:1; border:2px solid {ORANGE}; box-shadow:0 0 0 1.5px #fff, 0 1px 5px rgba(27,31,42,.35); z-index:2;}}
.th b{{position:absolute; left:-2px; top:-2px; background:{ORANGE}; color:#fff; font-size:9.5px; line-height:1; padding:1.5px 3px;}}
.lines{{position:absolute; left:0; top:0; z-index:1;}}
.q,.a{{position:absolute; left:425px; width:449px; display:flex; gap:8px; font-size:12.5px; line-height:1.25;}}
.q{{top:0; background:#EEF0F8; padding:5px 9px;}} .q b,.a b{{color:{NAVY}; font-size:14px; line-height:1.1;}}
.a{{top:47px; padding:0 9px; color:{MUTE};}} .a strong{{color:{INK};}}
.crop{{position:absolute; top:70px; width:215px; z-index:3;}}
.crop h5{{font-size:11.5px; font-weight:700; color:{ORANGE}; line-height:1; margin-bottom:4px;}}
.crop h5 span{{font-weight:400; color:{MUTE}; margin-left:4px;}}
.win{{position:relative; width:215px; height:118px; overflow:hidden; background-repeat:no-repeat; border:1.5px solid {ORANGE}; background-color:#fff;}}
.win i{{position:absolute; border:2px solid {ORANGE}; background:rgba(237,125,49,.14);}}
"""
    render("multipage", W, H, body, css, work)

# ---------------------------------------------------------- slide 13: representation

RUNGS = ("T", "TL", "TLV", "V")
#: MMLongBench-Doc, the 201 answerable questions on scanned documents, Qwen3-VL-8B with gold
#: pages and no instruction (g4-faithfulness-full). Abstention from results.errcat.jsonl,
#: accuracy from results.jsonl.
SCANNED = [("Text",   [70.8, 18.5, 12.3, 12.3], [3.1, 36.9, 53.8, 47.7]),
           ("Layout", [52.6, 18.4, 0.0, 2.6],   [2.6, 23.7, 57.9, 47.4]),
           ("Table",  [81.2, 12.5, 6.2, 9.4],   [0.0, 62.5, 71.9, 59.4]),
           ("Chart",  [77.1, 43.8, 16.7, 12.5], [0.0, 6.2, 54.2, 52.1]),
           ("Figure", [61.3, 19.8, 4.7, 3.8],   [7.5, 34.0, 56.6, 51.9]),
           ("All",    [69.2, 21.9, 6.5, 6.0],   [4.0, 34.3, 61.2, 56.2])]
#: The LongDocURL block of ~/mpvrdu/tables/paper/abstention_rungs.tex.
LDU = [("Text",   [4.6, 3.5, 1.5, 1.6], [75.3, 79.5, 82.3, 74.0]),
       ("Layout", [2.1, 1.6, 0.7, 0.9], [48.7, 52.4, 56.3, 52.2]),
       ("Table",  [5.0, 3.2, 1.1, 0.8], [61.2, 69.5, 68.2, 57.3]),
       ("Figure", [6.7, 8.6, 1.5, 1.3], [62.5, 65.7, 73.4, 65.2]),
       ("All",    [4.7, 4.3, 1.3, 1.3], [63.7, 68.0, 71.9, 63.1])]

def rung_table():
    def cell(v, kind, best):
        rgb, top = ("90,96,114", .55) if kind == "abs" else ("39,52,139", .50)
        body = f"<b>{v:.1f}</b>" if best else f"{v:.1f}"
        return f'<td style="background:rgba({rgb},{v / 100 * top:.2f})">{body}</td>'
    out = ['<table><thead><tr><th></th><th colspan="4">Abstention (%)</th><th class="gap"></th>'
           '<th colspan="4">Accuracy (%)</th></tr><tr><th class="l">Evidence</th>'
           + "".join(f"<th>{r}</th>" for r in RUNGS) + '<th class="gap"></th>'
           + "".join(f"<th>{r}</th>" for r in RUNGS) + "</tr></thead><tbody>"]
    for title, block in (("MMLongBench-Doc, scanned documents", SCANNED), ("LongDocURL, born-digital", LDU)):
        out.append(f'<tr class="blk"><td colspan="10">{title}</td></tr>')
        for lab, ab, acc in block:
            name = f"<em>{lab}</em>" if lab == "All" else lab
            out.append(f'<tr><td class="l">{name}</td>' + "".join(cell(v, "abs", False) for v in ab)
                       + '<td class="gap"></td>' + "".join(cell(v, "acc", v == max(acc)) for v in acc) + "</tr>")
    css = f"""
table{{border-collapse:collapse; width:100%; height:100%; font-size:13px; line-height:1.1;}}
th,td{{padding:0 5px; text-align:right; white-space:nowrap;}}
thead th{{font-weight:700; text-align:center; border-bottom:1.3px solid {INK};}}
thead tr:first-child th{{border-bottom:none; padding-top:3px;}}
th.l,td.l{{text-align:left; padding-left:12px;}}
th.gap,td.gap{{padding:0; width:8px; border:none; background:none;}}
tr.blk td{{text-align:left; font-weight:700; padding-left:0; vertical-align:bottom; padding-bottom:3px; color:{NAVY};}}
tbody tr:last-child td{{border-bottom:1.3px solid {INK};}}
"""
    render("rung_table", 394, 327, "".join(out) + "</tbody></table>", css)

def complement():
    """Left: accuracy against resolution, image alone and with parser text. Right: each text
    source alone and with the page image. Qwen3-VL-8B, MMLongBench-Doc, 847 answerable."""
    W, H = 437, 264
    p = []
    # -- panel A
    p.append(T(0, 13, "Text covers for low resolution", 13.5, "start", INK, 700))
    x0, x1, yb, yt = 24, 206, 196, 44
    lo, hi = 30, 60
    X = [x0 + 26, (x0 + x1) / 2, x1 - 26]
    Y = lambda v: yb - (v - lo) / (hi - lo) * (yb - yt)
    for v in (30, 40, 50, 60):
        p.append(L(x0, Y(v), x1, Y(v)))
        p.append(T(x0 - 5, Y(v) + 3.5, str(v), 10.5, "end", MUTE))
    p.append(L(x0, Y(38.4), x1, Y(38.4), MUTE, 1.3, "4 3"))
    for vals, colour in (((37.8, 45.7, 50.2), PALE), ((49.2, 52.5, 54.7), NAVY)):
        pts = " ".join(f"{x:.1f},{Y(v):.1f}" for x, v in zip(X, vals))
        p.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="2.8"/>')
        for x, v in zip(X, vals):
            p.append(f'<circle cx="{x:.1f}" cy="{Y(v):.1f}" r="3.8" fill="{colour}"/>')
            above = colour == NAVY
            p.append(T(x, Y(v) + (-8 if above else 16), f"{v:.1f}", 12, "middle", NAVY if above else INK, 700 if above else 400))
    for x, lab, tok in zip(X, ("low", "medium", "high"), (285, 456, 736)):
        p.append(T(x, yb + 14, lab, 11.5))
        p.append(T(x, yb + 26, f"{tok} tok/page", 10, "middle", MUTE))
    ly = H - 8
    p.append(f'<circle cx="6" cy="{ly - 4}" r="3.8" fill="{NAVY}"/>'); p.append(T(14, ly, "text + image", 11.5, "start", NAVY, 700))
    p.append(f'<circle cx="84" cy="{ly - 4}" r="3.8" fill="{PALE}"/>'); p.append(T(92, ly, "image only", 11.5, "start"))
    p.append(L(146, ly - 4, 162, ly - 4, MUTE, 1.3, "4 3")); p.append(T(166, ly, "text only", 11.5, "start", MUTE))
    # -- panel B
    ox = 232
    p.append(T(ox, 13, "The image covers for parser noise", 13.5, "start", INK, 700))
    rows = (("MinerU 2.5", 26.8, 48.3), ("Embedded text", 31.9, 51.6), ("PaddleOCR-VL", 38.4, 52.5), ("Unlimited-OCR", 40.4, 53.4))
    bx0, bx1 = ox + 78, W - 22
    BX = lambda v: bx0 + (v - 20) / (60 - 20) * (bx1 - bx0)
    for v in (20, 30, 40, 50, 60):
        p.append(L(BX(v), yt - 6, BX(v), yb))
        p.append(T(BX(v), yb + 14, str(v), 10.5, "middle", MUTE))
    step = (yb - yt + 6) / 4
    for i, (name, a, b) in enumerate(rows):
        y = yt - 6 + step * (i + .5)
        p.append(T(bx0 - 8, y + 4, name, 11.5, "end"))
        p.append(L(BX(a), y, BX(b), y, PALE, 3.2))
        p.append(f'<circle cx="{BX(a):.1f}" cy="{y:.1f}" r="4.3" fill="#fff" stroke="{MUTE}" stroke-width="1.8"/>')
        p.append(f'<circle cx="{BX(b):.1f}" cy="{y:.1f}" r="4.8" fill="{NAVY}"/>')
        p.append(T(BX(a), y - 9, f"{a:.1f}", 11.5, "middle", MUTE))
        p.append(T(BX(b), y - 9, f"{b:.1f}", 12, "middle", NAVY, 700))
    p.append(f'<circle cx="{ox + 6}" cy="{ly - 4}" r="4.3" fill="#fff" stroke="{MUTE}" stroke-width="1.8"/>')
    p.append(T(ox + 15, ly, "text only", 11.5, "start", MUTE))
    p.append(f'<circle cx="{ox + 70}" cy="{ly - 4}" r="4.8" fill="{NAVY}"/>')
    p.append(T(ox + 79, ly, "text + image (medium)", 11.5, "start", NAVY, 700))
    render("complement", W, H, svg(W, H, p))

# ---------------------------------------------------------- slide 15: reasoning

def prompt_modes():
    """Qwen3-VL-8B under four prompts, gold pages. Answerable: correct (accuracy judge) under
    refused (taxonomy judge). Unanswerable: refused. From prompt_operating_points_backbone.csv."""
    W, H = 403, 317
    p = []
    modes = (("none", 52.5, 6.2, 45.5), ("cot", 53.1, 6.6, 43.0), ("abstain", 41.4, 27.7, 74.6), ("abstain\n+ cot", 53.0, 19.9, 85.5))
    yb, yt = 256, 30
    Y = lambda v: yb - v / 100 * (yb - yt)
    for g, (title, gx) in enumerate((("Answerable", 28), ("Unanswerable", 226))):
        gw = 172
        for v in (25, 50, 75, 100):
            p.append(L(gx, Y(v), gx + gw, Y(v)))
        p.append(L(gx, yb, gx + gw, yb, MUTE, 1.2))
        p.append(T(gx + 2, yt - 10, title, 13, "start", MUTE, 400, "italic"))
        slot = gw / 4
        for i, (name, corr, ref, unans) in enumerate(modes):
            cx, w = gx + slot * (i + .5), slot * .72
            if g == 0:
                p.append(R(cx - w / 2, Y(corr), w, yb - Y(corr), PALE))
                p.append(R(cx - w / 2, Y(corr + ref), w, Y(corr) - Y(corr + ref), NAVY))
                p.append(T(cx, (Y(corr) + yb) / 2 + 4, f"{corr:.1f}", 12.5))
                if ref > 12:
                    p.append(T(cx, (Y(corr + ref) + Y(corr)) / 2 + 4, f"{ref:.1f}", 12.5, "middle", "#fff", 700))
                else:
                    p.append(T(cx, Y(corr + ref) - 5, f"{ref:.1f}", 12.5, "middle", NAVY, 700))
            else:
                p.append(R(cx - w / 2, Y(unans), w, yb - Y(unans), NAVY))
                p.append(T(cx, (Y(unans) + yb) / 2 + 4, f"{unans:.1f}", 12.5, "middle", "#fff", 700))
            for k, part in enumerate(name.split("\n")):
                p.append(T(cx, yb + 15 + k * 12.5, part, 12))
    for v in (0, 50, 100):
        p.append(T(23, Y(v) + 3.5, str(v), 10.5, "end", MUTE))
    lx = 96
    p.append(R(lx, H - 14, 11, 11, PALE)); p.append(T(lx + 16, H - 4.5, "answered correctly", 12, "start"))
    p.append(R(lx + 132, H - 14, 11, 11, NAVY)); p.append(T(lx + 148, H - 4.5, "refused", 12, "start"))
    render("prompt_modes", W, H, svg(W, H, p))

def strategies():
    """Single pass against self-consistency and Reflexion, both pools, with seconds a question.
    Self-consistency is on 773 of 847 answerable questions."""
    W, H = 418, 317
    p = []
    rows = (("single pass", 52.5, 47.5, None), ("Self-consistency", 60.7, 55.8, "640 s a question"), ("Reflexion", 55.1, 61.5, "47 s a question"))
    yb, yt = 256, 30
    lo, hi = 30, 70
    Y = lambda v: yb - (v - lo) / (hi - lo) * (yb - yt)
    gx, gw = 28, W - 28
    for v in (30, 40, 50, 60, 70):
        p.append(L(gx, Y(v), gx + gw, Y(v)))
        p.append(T(gx - 5, Y(v) + 3.5, str(v), 10.5, "end", MUTE))
    p.append(L(gx, yb, gx + gw, yb, MUTE, 1.2))
    p.append(T(gx + 2, yt - 10, "Accuracy (%)", 13, "start", MUTE, 400, "italic"))
    slot = gw / 3
    for i, (name, ans, unans, cost) in enumerate(rows):
        cx, w = gx + slot * (i + .5), 40
        for k, (v, colour) in enumerate(((ans, PALE), (unans, NAVY))):
            x = cx + (k - 1) * (w + 4) + 2
            p.append(R(x, Y(v), w, yb - Y(v), colour))
            p.append(T(x + w / 2, Y(v) - 5, f"{v:.1f}", 12.5, "middle", NAVY if k else INK, 700 if k else 400))
        p.append(T(cx, yb + 15, name, 12.5, "middle", INK, 700 if i else 400))
        if cost:
            p.append(T(cx, yb + 28, cost, 11.5, "middle", MUTE, 400, "italic"))
    lx = 82
    p.append(R(lx, H - 14, 11, 11, PALE)); p.append(T(lx + 16, H - 4.5, "answerable", 12, "start"))
    p.append(R(lx + 92, H - 14, 11, 11, NAVY)); p.append(T(lx + 108, H - 4.5, "unanswerable (refusal credited)", 12, "start"))
    render("strategies", W, H, svg(W, H, p))

# ---------------------------------------------------------- into the pptx

def embed():
    """Point every picture named fig_<stem> at figures/final/<stem>.png, keeping its box."""
    from pptx import Presentation
    prs = Presentation(PPTX)
    for n, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            png = OUT / f"{shape.name[4:]}.png"
            if shape.name.startswith("fig_") and shape.shape_type == 13 and png.exists():
                _, rid = slide.part.get_or_add_image_part(str(png))
                shape._element.blipFill.blip.rEmbed = rid
                print(f"slide {n}: {shape.name}")
    prs.save(PPTX)

if __name__ == "__main__":
    multipage(); rung_table(); complement(); prompt_modes(); strategies()
    if "--embed" in sys.argv:
        embed()
