"""Draw a six-mode seminar variant of the paper's prompt calibration figure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from build_reasoning_figure import stats

sys.path.insert(0, '/home/lingwei/.codex/skills/html-paper-figure/scripts')
from render_figure import build_set, fmt

HERE = Path(__file__).resolve().parent
OUT = HERE / 'figures/final'
CORRECT = '#BFC7CD'
REFUSED = '#4B7A99'
INK = '#14181C'
MUTED = '#72777D'
GRID = '#DCE1E5'
SPINE = '#929AA1'
MODES = ['none', 'cot', 'abstain', 'abstain\n+cot', 'SC', 'Reflexion']


def line(x1, y1, x2, y2, color, width=.16, dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" '
            f'y2="{fmt(y2)}" stroke="{color}" stroke-width="{fmt(width)}"{extra}/>')


def rect(x, y, w, h, color):
    return (f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" '
            f'height="{fmt(h)}" fill="{color}"/>')


def text(x, y, value, size=2.55, fill=INK, anchor='middle', bold=False, italic=False):
    attrs = f' font-weight="700"' if bold else ''
    attrs += f' font-style="italic"' if italic else ''
    return (f'<text x="{fmt(x)}" y="{fmt(y)}" font-size="{fmt(size)}" '
            f'text-anchor="{anchor}" fill="{fill}"{attrs}>{value}</text>')


def draw(data):
    parts = []
    legend_y = 3
    parts += [rect(57, legend_y-.95, 2.0, 2.0, CORRECT),
              text(60, legend_y+.8, 'answered correctly', 2.7, MUTED, 'start'),
              rect(86, legend_y-.95, 2.0, 2.0, REFUSED),
              text(89, legend_y+.8, 'abstained / correct refusal', 2.7, MUTED, 'start')]
    top, bottom = 11.2, 53.2
    height = bottom-top
    panel_x = [10, 94]
    panel_w = 74
    bar_w = 7.0
    slot = panel_w/6
    y_of = lambda value: bottom - value/100*height
    for panel, x0 in enumerate(panel_x):
        heading = 'Answerable' if panel == 0 else 'Unanswerable'
        parts.append(text(x0+1, top+3.0, heading, 3.6, MUTED, 'start', italic=True))
        if panel == 0:
            parts.append(text(x0+panel_w-1, top+3.0, 'Qwen3-VL-8B', 3.3, INK, 'end', bold=True))
        for tick in [0,25,50,75,100]:
            y=y_of(tick)
            parts.append(line(x0,y,x0+panel_w,y,GRID,.16))
            if panel == 0:
                parts.append(text(x0-1.5,y+.8,str(tick),2.5,MUTED,'end'))
        parts.append(line(x0,top,x0,bottom,SPINE,.22))
        parts.append(line(x0,bottom,x0+panel_w,bottom,SPINE,.22))
        sep=x0+slot*4
        parts.append(line(sep,top+4,sep,bottom+5,SPINE,.26,'1.0 1.1'))
        for i,d in enumerate(data):
            cx=x0+slot*(i+.5)
            if panel==0:
                acc,ref=d['answer'],d['refusal']
                parts.append(rect(cx-bar_w/2,y_of(acc),bar_w,bottom-y_of(acc),CORRECT))
                parts.append(rect(cx-bar_w/2,y_of(acc+ref),bar_w,y_of(acc)-y_of(acc+ref),REFUSED))
                parts.append(text(cx,(y_of(acc)+bottom)/2+.8,f'{acc:.1f}',2.55,INK))
                if ref>=12:
                    parts.append(text(cx,(y_of(acc+ref)+y_of(acc))/2+.8,f'{ref:.1f}',2.45,'#FFFFFF'))
                else:
                    parts.append(text(cx,y_of(acc+ref)-.7,f'{ref:.1f}',2.45,REFUSED))
            else:
                score=d['unanswer']
                parts.append(rect(cx-bar_w/2,y_of(score),bar_w,bottom-y_of(score),REFUSED))
                parts.append(text(cx,(y_of(score)+bottom)/2+.8,f'{score:.1f}',2.55,'#FFFFFF'))
            label=MODES[i]
            if '\n' in label:
                a,b=label.split('\n')
                parts.append(text(cx,bottom+3.0,a,2.65))
                parts.append(text(cx,bottom+5.8,b,2.65))
            else:
                parts.append(text(cx,bottom+3.0,label,2.65))
    parts.append(f'<text x="2.4" y="{fmt((top+bottom)/2)}" font-size="2.75" '
                 f'text-anchor="middle" fill="{MUTED}" font-style="italic" '
                 f'transform="rotate(-90 2.4 {fmt((top+bottom)/2)})">Share (%)</text>')
    parts.append(text(10,64.2,'Accuracy judge: correct. Taxonomy judge: answerable abstention. Reflexion abstention n=294.',
                      2.2,MUTED,'start'))
    return '\n'.join(parts)


def page(body):
    def make(box):
        x,y,w,h=box
        return (f'<!doctype html><meta charset="utf-8"><style>@page {{ size:{w}mm {h}mm; margin:0 }}'
                f'html,body{{margin:0;padding:0}}svg{{display:block;font-family:"Liberation Serif","Times New Roman",serif}}</style>'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" '
                f'viewBox="{x} {y} {w} {h}">{body}</svg>')
    return make


if __name__=='__main__':
    data=stats()
    (OUT/'reasoning_calibration_data.json').write_text(json.dumps(data,indent=2)+'\n')
    build_set([('reasoning_calibration_six_modes',page(draw(data)))],OUT,(172,66),dpi=400)
