"""The slide 3 figure (one 40-page guidebook, the two pages a question needs) as a PDF for
the thesis, with the caption reading "International Student Guidebook 40 pages".

    python3 Seminar/make_thesis_multipage.py

The layout is make_final_figures.multipage() unchanged. This swaps in its own render step
so the PDF is kept, and leaves the slide PNG alone.
"""
import shutil, subprocess
from pathlib import Path

import make_final_figures as mf

HERE = Path(__file__).parent
PDF = HERE.parent / "Thesis" / "include" / "multipage_example.pdf"
PNG = HERE / "figures" / "final" / "multipage_thesis.png"

OLD_CAP = '<b>One document, 40 pages</b> international student guidebook'
NEW_CAP = 'International Student Guidebook <b>40 pages</b>'


def render(name, w, h, body, css="", workdir=None):
    assert OLD_CAP in body and ".cap b{" in css
    body = body.replace(OLD_CAP, NEW_CAP)
    css = css.replace(".cap b{", ".cap b{margin-left:6px; ").replace("margin-right:6px;", "")
    work = Path(workdir)
    html = work / f"{name}.html"
    html.write_text(
        f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{mf.FONT_CSS}'
        f'@page{{size:{w}px {h}px; margin:0;}} *{{box-sizing:border-box; margin:0; padding:0; -webkit-print-color-adjust:exact; print-color-adjust:exact;}} html,body{{width:{w}px; height:{h}px; overflow:hidden; '
        f'background:#fff; font-family:{mf.FAMILY}; color:{mf.INK}; -webkit-font-smoothing:antialiased;}}{css}'
        f'</style></head><body>{body}</body></html>')
    pdf = work / f"{name}.pdf"
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                    "--allow-file-access-from-files", f"--print-to-pdf={pdf}", html.as_uri()],
                   check=True, capture_output=True)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(pdf, PDF)
    subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", str(PDF), str(PNG.with_suffix(""))], check=True)
    print(PDF, PNG, sep="\n")


if __name__ == "__main__":
    mf.render = render
    mf.multipage()
