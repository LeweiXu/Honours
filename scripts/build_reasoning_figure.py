"""Build the seminar reasoning comparison from judged result rows."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path('/home/lingwei/mpvrdu')
OUT = Path(__file__).resolve().parent / 'figures/final'
sys.path.insert(0, '/home/lingwei/.codex/skills/html-paper-figure/scripts')
from render_figure import build_set


def rows(tag, group, judge, condition=None):
    path = ROOT / 'results/cache' / tag / 'full' / group / ('results.errcat.jsonl' if judge == 'taxonomy' else 'results.jsonl')
    result = [json.loads(line) for line in path.open()]
    result = [r for r in result if r['status'] == 'ok' and r['representation'] == 'TLV'
              and r['model_spec'].startswith('qwen3vl-8b-local')]
    if condition:
        result = [r for r in result if r['condition'] == condition]
    return result


def joined(tag, group, judge, condition):
    if tag == 'g4-sc-cot-tlv':
        return sum((rows(f'g4-sc-cot-tlv-p{i}', group, judge, condition) for i in range(1, 4)), [])
    return rows(tag, group, judge, condition)


def stats():
    specs = [
        ('Plain', 'g4-faithfulness-full', 'g3-faithfulness-full', 'none'),
        ('CoT', 'g4-faithfulness-full', 'g3-faithfulness-full', 'cot'),
        ('Abstain', 'g4-faithfulness-full', 'g3-faithfulness-full', 'abstain'),
        ('CoT + abstain', 'g4-abstaincot-tlv', 'g3-abstaincot-tlv', 'abstain_cot'),
        ('Self-consistency', 'g4-sc-cot-tlv', 'g3-sc-cot-tlv', 'sc_cot'),
        ('Reflexion', 'g4-reflexion-tlv', 'g3-reflexion-tlv', 'reflexion'),
    ]
    result = []
    for label, g4, g3, mode in specs:
        ans = 'G4_faithfulness_answerable'
        una = 'G3_hallucination'
        a = joined(g4, ans, 'accuracy', 'oracle__' + mode)
        t = joined(g4, ans, 'taxonomy', 'oracle__' + mode)
        u = joined(g3, una, 'accuracy', 'retrieved_text_k3__' + mode)
        assert a and t and u, (label, len(a), len(t), len(u))
        result.append(dict(label=label, answer=100 * sum(r['correct'] for r in a) / len(a),
                           refusal=100 * sum(r['abstained'] for r in t) / len(t),
                           unanswer=100 * sum(r['correct'] for r in u) / len(u),
                           n_answer=len(a), n_refusal=len(t), n_unanswer=len(u)))
    assert result[0]['n_answer'] == 847 and result[4]['n_answer'] == 847
    assert result[5]['n_refusal'] == 294
    return result


def svg_text(x, y, value, size=2.9, weight=400, fill='#273343', anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{html.escape(str(value))}</text>'


def page(data):
    w, h = 174, 65
    col_x = [48, 90, 132]
    colors = ['#294c9b', '#d57632', '#16817e']
    labels = ['ANSWERABLE CORRECT', 'ANSWERABLE ABSTAINED', 'UNANSWERABLE CORRECT']
    items = []
    for x, title, color in zip(col_x, labels, colors):
        items.append(svg_text(x, 7, title, 2.65, 700, color))
        items.append('<line x1="%s" y1="10" x2="%s" y2="10" stroke="#d9dee5" stroke-width=".16"/>' % (x, x+36))
        for v in [0, 50, 100]:
            xx = x + v * .29
            items.append(f'<line x1="{xx:.2f}" y1="11" x2="{xx:.2f}" y2="55" stroke="#e8ebef" stroke-width=".14"/>')
            items.append(svg_text(xx, 61, str(v), 2.4, 400, '#687688', 'middle'))
    items.append(svg_text(3, 7, 'PROMPT / STRATEGY', 2.65, 700, '#536174'))
    for i, d in enumerate(data):
        y = 15 + 7.25 * i
        if i == 4:
            items.append(f'<line x1="3" y1="{y-5.0:.2f}" x2="169" y2="{y-5.0:.2f}" stroke="#8d9aa8" stroke-dasharray="1.2 1.2" stroke-width=".2"/>')
        items.append(svg_text(3, y + 1.6, d['label'], 3.1, 700 if i >= 4 else 400))
        for j, (field, color) in enumerate(zip(['answer', 'refusal', 'unanswer'], colors)):
            x = col_x[j]
            value = d[field]
            bw = value * .29
            items.append(f'<rect x="{x}" y="{y-1.4:.2f}" width="{bw:.2f}" height="4.1" rx=".45" fill="{color}"/>')
            items.append(svg_text(x+30.3, y+1.6, f'{value:.1f}', 2.75, 700, '#26374a'))
    items.append(svg_text(3, 64, 'Qwen3-VL-8B · gold pages (answerable), retrieved k=3 (unanswerable) · %', 2.35, 400, '#66768a'))
    svg = '\n'.join(items)
    def make(box):
        x, y, cw, ch = box
        return (f'<!doctype html><meta charset="utf-8"><style>@page {{ size:{cw}mm {ch}mm; margin:0 }}'
                f'html,body{{margin:0;padding:0}} svg{{display:block;font-family:Arial,"Liberation Sans",sans-serif}}</style>'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{cw}mm" height="{ch}mm" viewBox="{x} {y} {cw} {ch}">{svg}</svg>')
    return (w, h), make


if __name__ == '__main__':
    data = stats()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'reasoning_data.json').write_text(json.dumps(data, indent=2) + '\n')
    slot, make = page(data)
    build_set([('reasoning_comparison', make)], OUT, slot, dpi=400)
    print(json.dumps(data, indent=2))
