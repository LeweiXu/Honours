"""Rewrite slides 15 and 17 of the seminar deck in place: new slide CSS block and markup,
the shared chrome and print rules left as they are."""
import json, re, sys
from pathlib import Path

SEM = Path.home() / "Honours" / "Seminar"
SCR = Path(__file__).parent
ACCENT, NAVY, LINE, INK = "#1A56B0", "#1F4E79", "#E2E6EA", "#14181C"
PALE = "#B9C7D8"      # the lighter partner of the accent
GREY = "#8A949E"

def swap(n, css, markup):
    p = SEM / f"slide{n}.html"
    s = p.read_text()
    a = s.index(f"  /* ================= SLIDE {n} ")
    b = s.index("  /* ---------- PRINT: one landscape page per slide ---------- */", a)
    s = s[:a] + css.rstrip() + "\n\n" + s[b:]
    a = s.index(f'<div class="slide s{n}">')
    b = s.index("</body>", a)
    s = s[:a] + markup.strip() + "\n" + s[b:]
    p.write_text(s)

def base_css(n, cols):
    return f"""  /* ================= SLIDE {n} ================= */
  .s{n} .body{{padding-top:22px;}}
  .s{n} .cols{{display:grid; grid-template-columns:{cols}; gap:26px; align-items:start;}}
  .s{n} .pt{{display:grid; grid-template-columns:34px 1fr; gap:9px; margin-bottom:11px;}}
  .s{n} .pt > i{{width:28px; height:28px; border-radius:50%; background:var(--accent); color:#fff; font-style:normal; font-size:15px; font-weight:700; display:flex; align-items:center; justify-content:center; margin-top:1px;}}
  .s{n} .pt h3{{font-size:21.5px; font-weight:700; line-height:1.2; margin-bottom:3px;}}
  .s{n} .pt p{{font-size:16.5px; line-height:1.3;}}
  .s{n} .ev{{display:flex; gap:12px; align-items:stretch;}}
  .s{n} .fg{{border:1.5px solid var(--line); padding:8px 10px 8px;}}
  .s{n} .fg h4{{font-size:15px; font-weight:700; line-height:1.2; margin-bottom:6px;}}
  .s{n} .fg p{{font-size:12.5px; line-height:1.28; font-style:italic; margin-top:5px;}}
  .s{n} .fg svg{{display:block;}}
  .s{n} .take{{margin-top:12px; border-left:5px solid var(--accent); padding:6px 0 6px 16px; font-size:21.5px; font-weight:700; font-style:italic; line-height:1.28;}}
  .s{n} .next{{position:absolute; left:64px; bottom:24px; font-size:15.5px; font-style:italic; max-width:760px;}}
  .s{n} .next b{{font-style:normal; font-weight:700; margin-right:6px;}}
"""

def pt(i, head, text):
    return f'<div class="pt"><i>{i}</i><div><h3>{head}</h3><p>{text}</p></div></div>'

T = lambda x, y, s, size=11, anchor="middle", fill=INK, weight=400, style="normal": (
    f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" '
    f'font-weight="{weight}" font-style="{style}">{s}</text>')
R = lambda x, y, w, h, fill: f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"/>'
L = lambda x1, y1, x2, y2, stroke=LINE, w=1, dash="": (
    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}"'
    + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
def svg(w, h, parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="Calibri, Carlito, sans-serif">' + "".join(parts) + "</svg>")

# ------------------------------------------------------------------ slide 15

scan = json.loads((SCR / "figures" / "scan_table.json").read_text())["scanned"]
RUNGS = ("T", "TL", "TLV", "V")
SCANNED = [(lab, [scan[f"{lab}|{r}"][0] for r in RUNGS], [scan[f"{lab}|{r}"][1] for r in RUNGS])
           for lab in ("Text", "Layout", "Table", "Chart", "Figure", "All")]
#: The LongDocURL block of the paper's abstention table, unchanged.
LDU = [("Text", [4.6, 3.5, 1.5, 1.6], [71.8, 75.6, 78.2, 70.0]),
       ("Layout", [2.1, 1.6, 0.7, 0.9], [45.0, 49.2, 51.3, 49.3]),
       ("Table", [5.0, 3.2, 1.1, 0.8], [57.7, 65.6, 63.6, 52.4]),
       ("Figure", [6.7, 8.6, 1.5, 1.3], [59.9, 62.8, 69.9, 61.9]),
       ("All", [4.7, 4.3, 1.3, 1.3], [60.3, 64.5, 67.3, 59.4])]

def table_html():
    def cell(v, kind, best):
        alpha = (v / 100) * (0.55 if kind == "abs" else 0.75)
        rgb = "31,78,121" if kind == "abs" else "27,175,122"
        body = f"<b>{v:.1f}</b>" if best else f"{v:.1f}"
        return f'<td style="background:rgba({rgb},{alpha:.2f})">{body}</td>'
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
    return "".join(out) + "</tbody></table>"

def complement_svg():
    W, H = 316, 372
    p = []
    # -- panel A: accuracy against resolution, with and without parser text
    p.append(T(0, 12, "Text covers for low resolution", 13, "start", INK, 700))
    x0, x1, yb, yt = 34, 224, 150, 30
    lo, hi = 30, 60
    X = [x0 + 18, (x0 + x1) / 2, x1 - 18]
    Y = lambda v: yb - (v - lo) / (hi - lo) * (yb - yt)
    for v in (30, 40, 50, 60):
        p.append(L(x0, Y(v), x1, Y(v)))
        p.append(T(x0 - 5, Y(v) + 3.5, str(v), 10.5, "end", GREY))
    p.append(L(x0, Y(38.4), x1, Y(38.4), GREY, 1.4, "4 3"))
    p.append(T(x1 + 5, Y(38.4) + 9, "text only 38.4", 11, "start", GREY))
    for vals, colour, label, dy in (((37.8, 45.7, 50.2), PALE, "image only", 4), ((49.2, 52.5, 54.7), ACCENT, "text + image", 4)):
        pts = " ".join(f"{x:.1f},{Y(v):.1f}" for x, v in zip(X, vals))
        p.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="2.6"/>')
        for x, v in zip(X, vals):
            p.append(f'<circle cx="{x:.1f}" cy="{Y(v):.1f}" r="3.6" fill="{colour}"/>')
            above = colour == ACCENT
            p.append(T(x, Y(v) + (-7 if above else 15), f"{v:.1f}", 11.5, "middle", ACCENT if above else INK, 700 if above else 400))
        p.append(T(x1 + 5, Y(vals[-1]) + dy, label, 11.5, "start", ACCENT if colour == ACCENT else INK, 700 if colour == ACCENT else 400))
    for x, lab, tok in zip(X, ("low", "medium", "high"), (285, 456, 736)):
        p.append(T(x, yb + 13, lab, 11))
        p.append(T(x, yb + 25, f"{tok} tok/page", 9.5, "middle", GREY))
    # -- panel B: each text source alone and with the page image
    top = 205
    p.append(T(0, top, "The image covers for parser noise", 13, "start", INK, 700))
    rows = (("MinerU 2.5", 26.8, 48.3), ("Embedded text", 31.9, 51.6), ("PaddleOCR-VL", 38.4, 52.5), ("Unlimited-OCR", 40.4, 53.4))
    bx0, bx1 = 92, 300
    BX = lambda v: bx0 + (v - 20) / (60 - 20) * (bx1 - bx0)
    for v in (20, 30, 40, 50, 60):
        p.append(L(BX(v), top + 12, BX(v), top + 12 + 4 * 27))
        p.append(T(BX(v), top + 12 + 4 * 27 + 12, str(v), 10.5, "middle", GREY))
    for i, (name, a, b) in enumerate(rows):
        y = top + 26 + i * 27
        p.append(T(bx0 - 8, y + 4, name, 11.5, "end"))
        p.append(L(BX(a), y, BX(b), y, PALE, 3))
        p.append(f'<circle cx="{BX(a):.1f}" cy="{y}" r="4.2" fill="#fff" stroke="{GREY}" stroke-width="1.8"/>')
        p.append(f'<circle cx="{BX(b):.1f}" cy="{y}" r="4.6" fill="{ACCENT}"/>')
        p.append(T(BX(a) - 8, y + 4, f"{a:.1f}", 11, "end", GREY))
        p.append(T(BX(b) + 8, y + 4, f"{b:.1f}", 11.5, "start", ACCENT, 700))
    ly = top + 12 + 4 * 27 + 30
    p.append(f'<circle cx="{bx0 - 60}" cy="{ly - 4}" r="4.2" fill="#fff" stroke="{GREY}" stroke-width="1.8"/>')
    p.append(T(bx0 - 52, ly, "text only", 11, "start", GREY))
    p.append(f'<circle cx="{bx0 + 16}" cy="{ly - 4}" r="4.6" fill="{ACCENT}"/>')
    p.append(T(bx0 + 24, ly, "text + image (medium)", 11, "start", ACCENT, 700))
    return svg(W, H, p)

css15 = base_css(15, "480px 1fr") + """  .s15 table{border-collapse:collapse; font-size:12.5px; line-height:1.2;}
  .s15 th, .s15 td{padding:2.6px 4px; text-align:right; white-space:nowrap;}
  .s15 thead th{font-weight:700; text-align:center; border-bottom:1.2px solid var(--ink);}
  .s15 thead tr:first-child th{border-bottom:none; padding-bottom:1px;}
  .s15 th.l, .s15 td.l{text-align:left; padding-left:10px;}
  .s15 th.gap, .s15 td.gap{padding:0; width:5px; border:none; background:none;}
  .s15 tr.blk td{text-align:left; font-weight:700; padding-top:6px; padding-left:0; background:none;}
  .s15 tbody tr.blk + tr td{border-top:none;}
  .s15 td b{color:var(--ink) !important;}
  .s15 .fg.t{flex:none; width:326px;}
  .s15 .fg.c{flex:1; min-width:0;}
  .s15 .fg.c svg{width:100%; height:auto;}
"""
left15 = "".join([
    pt(1, "Vision is expensive",
       "At the same 900 input tokens, page images take <b>21&times; longer</b> to read than text "
       "(22.7 s against 1.1 s a question) and run out of memory on 11% of questions, against 1%."),
    pt(2, "Yet most systems read everything visually",
       "Vision only, or text plus image, for every page. But the best choice depends on the "
       "<b>document type</b> and the <b>task</b>: scans have no text layer; born-digital text and "
       "tables gain little from the image; charts and figures need it."),
    pt(3, "Modalities are complementary",
       "Text alone 38%, a low-resolution image alone 38%, together 49%. They fail on "
       "<b>different questions</b> (only 22% are answered by both), so parser noise and low "
       "resolution cover for each other."),
    pt(4, "Deployment: choose, don&rsquo;t default",
       "A known document type or task fixes the modality: images for scans, cached parser text for "
       "reports and tables. Mixed collections: choose per question, as tool-using agents are "
       "starting to."),
])
slide15 = f"""
<div class="slide s15">

  <h1>Representation: When Is Visual Reading Worth Its Cost?</h1>

  <div class="body">
    <div class="cols">
      <div>{left15}</div>
      <div class="ev">
        <div class="fg t"><h4>By evidence source and representation</h4>{table_html()}<p>T embedded text, TL parsed text, TLV parsed text plus page image, V page image.</p></div>
        <div class="fg c"><h4>Each modality hides the other&rsquo;s weakness</h4>{complement_svg()}</div>
      </div>
    </div>
    <div class="take">No one size fits all: choose modalities for the document and the task, and combine cheap ones before paying for resolution.</div>
  </div>

  <div class="next"><b>Next</b>Once the pages are readable, which ones should the model see?</div>

  <div class="corner"><i>Background</i><i>Survey</i><i class=on>Empirical</i><b>15</b> / 18</div>

</div>
"""
swap(15, css15, slide15)

# ------------------------------------------------------------------ slide 17

def prompt_svg():
    """Qwen3-VL-8B under four prompts: answerable (correct under refused) and unanswerable refused."""
    W, H = 366, 300
    p = []
    modes = (("none", 49.5, 6.2, 45.5), ("cot", 50.2, 6.6, 43.0), ("abstain", 40.0, 27.7, 74.6), ("abstain\n+ cot", 50.7, 19.9, 85.5))
    yb, yt = 240, 34
    Y = lambda v: yb - v / 100 * (yb - yt)
    for g, (title, gx) in enumerate((("Answerable", 30), ("Unanswerable", 206))):
        gw = 150
        for v in (25, 50, 75, 100):
            p.append(L(gx, Y(v), gx + gw, Y(v)))
        p.append(L(gx, yb, gx + gw, yb, GREY, 1.2))
        p.append(T(gx + 2, yt - 8, title, 12, "start", GREY, 400, "italic"))
        slot = gw / 4
        for i, (name, corr, ref, unans) in enumerate(modes):
            cx, w = gx + slot * (i + .5), slot * .66
            if g == 0:
                p.append(R(cx - w / 2, Y(corr), w, yb - Y(corr), PALE))
                p.append(R(cx - w / 2, Y(corr + ref), w, Y(corr) - Y(corr + ref), ACCENT))
                p.append(T(cx, (Y(corr) + yb) / 2 + 4, f"{corr:.0f}", 12))
                if ref > 12:
                    p.append(T(cx, (Y(corr + ref) + Y(corr)) / 2 + 4, f"{ref:.0f}", 12, "middle", "#fff", 700))
                else:
                    p.append(T(cx, Y(corr + ref) - 4, f"{ref:.0f}", 12, "middle", ACCENT, 700))
            else:
                p.append(R(cx - w / 2, Y(unans), w, yb - Y(unans), ACCENT))
                p.append(T(cx, (Y(unans) + yb) / 2 + 4, f"{unans:.0f}", 12, "middle", "#fff", 700))
            for k, part in enumerate(name.split("\n")):
                p.append(T(cx, yb + 14 + k * 12, part, 11))
    for v in (0, 50, 100):
        p.append(T(25, Y(v) + 3.5, str(v), 10.5, "end", GREY))
    lx = 62
    p.append(R(lx, H - 14, 10, 10, PALE)); p.append(T(lx + 14, H - 5, "answered correctly", 11.5, "start"))
    p.append(R(lx + 130, H - 14, 10, 10, ACCENT)); p.append(T(lx + 144, H - 5, "refused", 11.5, "start"))
    return svg(W, H, p)

def strategy_svg():
    """Single pass against the two strategies: answerable and unanswerable accuracy, and cost."""
    W, H = 366, 300
    p = []
    rows = (("single pass", 52.5, 47.5, None), ("Self-\nconsistency", 60.7, 55.8, "640 s"), ("Reflexion", 55.1, 61.5, "47 s"))
    yb, yt = 240, 34
    lo, hi = 30, 70
    Y = lambda v: yb - (v - lo) / (hi - lo) * (yb - yt)
    gx, gw = 30, 326
    for v in (30, 40, 50, 60, 70):
        p.append(L(gx, Y(v), gx + gw, Y(v)))
        p.append(T(gx - 5, Y(v) + 3.5, str(v), 10.5, "end", GREY))
    p.append(L(gx, yb, gx + gw, yb, GREY, 1.2))
    p.append(T(gx + 2, yt - 8, "Accuracy (%)", 12, "start", GREY, 400, "italic"))
    slot = gw / 3
    for i, (name, ans, unans, cost) in enumerate(rows):
        cx, w = gx + slot * (i + .5), 34
        for k, (v, colour) in enumerate(((ans, PALE), (unans, ACCENT))):
            x = cx + (k - 1) * (w + 4) + 2
            p.append(R(x, Y(v), w, yb - Y(v), colour))
            p.append(T(x + w / 2, Y(v) - 4, f"{v:.1f}", 12, "middle", ACCENT if k else INK, 700 if k else 400))
        for k, part in enumerate(name.split("\n")):
            p.append(T(cx, yb + 14 + k * 12, part, 11.5, "middle", INK, 700 if i else 400))
        if cost:
            p.append(T(cx, yb + 14 + len(name.split("\n")) * 12 + 1, f"{cost} a question", 11, "middle", GREY, 400, "italic"))
    lx = 74
    H2 = H
    p.append(R(lx, H - 14, 10, 10, PALE)); p.append(T(lx + 14, H - 5, "answerable", 11.5, "start"))
    p.append(R(lx + 96, H - 14, 10, 10, ACCENT)); p.append(T(lx + 110, H - 5, "unanswerable (refusal credited)", 11.5, "start"))
    return svg(W, H, p)

css17 = base_css(17, "408px 1fr") + """  .s17 .pt{margin-bottom:13px;}
  .s17 .fg{flex:1; min-width:0;}
  .s17 .eg{font-size:15px; line-height:1.3; border-left:3px solid var(--line); padding-left:10px; margin:6px 0 0;}
  .s17 .eg span{font-weight:700; margin-right:5px;}
  .s17 .eg span.x{color:#B42318;} .s17 .eg span.v{color:#157F3B;}
"""
left17 = "".join([
    pt(1, "Unsupported premises",
       "A model answers fluently even when the document does not support the question. With no "
       "instruction it refuses only <b>45%</b> of unanswerable questions."
       '</p><p class="eg">&ldquo;Which YouTube does the slides use&hellip;?&rdquo; The document mentions no video.<br>'
       '<span class="x">&#10007;</span>&ldquo;A clip from <em>Breaking Bad</em>&hellip;&rdquo; '
       '<span class="v">&#10003;</span>&ldquo;Not answerable&rdquo; once it may abstain.'),
    pt(2, "Prompts move the trade-off",
       "Permitting abstention lifts refusal to <b>75%</b>, but also refuses 28% of answerable "
       "questions. Reasoning first, then abstaining, wins the accuracy back (51%) and refuses more "
       "of the unanswerable (86%)."),
    pt(3, "More computation helps, at a price",
       "<b>Self-consistency</b> (40 sampled reasoning paths, majority vote) adds 8 points on "
       "answerable questions, at 640 s a question. <b>Reflexion</b> (retry on its own evaluation) "
       "adds 14 on unanswerable ones at 47 s, though its self-check passes 94% of its answers."),
])
slide17 = f"""
<div class="slide s17">

  <h1>Reasoning: Does the Document Support the Question?</h1>

  <div class="body">
    <div class="cols">
      <div>{left17}</div>
      <div class="ev">
        <div class="fg"><h4>Prompting: answering and refusing</h4>{prompt_svg()}<p>Qwen3-VL-8B with gold pages, share of questions (%).</p></div>
        <div class="fg"><h4>Spending more computation on reasoning</h4>{strategy_svg()}<p>Self-consistency on 773 of 847 answerable questions so far; single pass is the uninstructed prompt.</p></div>
      </div>
    </div>
    <div class="take">Before asking whether the answer is correct, ask whether the evidence supports giving that answer.</div>
  </div>

  <div class="next"><b>Next</b>To conclude.</div>

  <div class="corner"><i>Background</i><i>Survey</i><i class=on>Empirical</i><b>17</b> / 18</div>

</div>
"""
swap(17, css17, slide17)
print("slides 15 and 17 rewritten")
