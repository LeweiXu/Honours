"""Replace the three findings slides in the revised seminar deck."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Pt

from revise_final_slides_v2 import ASSETS, clear, header, notes, picture, textbox

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'Seminar_final_revised.pptx'
OUTPUT = HERE / 'Seminar_final_revised_v3_check.pptx'
BLUE = RGBColor(24, 79, 169)
INK = RGBColor(28, 36, 49)


def bullet(slide, content, x, y, w, h, size=10.5, color=INK, bold=False):
    shape = textbox(slide, content, x, y, w, h, size, color, bold)
    para = shape.text_frame.paragraphs[0]
    ppr = para._p.get_or_add_pPr()
    ppr.set('marL', '200000')
    ppr.set('indent', '-150000')
    marker = OxmlElement('a:buChar')
    marker.set('char', '•')
    ppr.append(marker)
    for run in para.runs:
        run.font.size = Pt(size)
    return shape


def representation(slide, template):
    clear(slide)
    header(slide, template, 'Finding 1 · Representation',
           'Chapter 3 · Empirical study · Under review')
    textbox(slide, 'The modality ceiling depends on the evidence and document type.',
            .45, .77, 9.1, .34, 14, BLUE, True)
    picture(slide, ASSETS / 'abstention_rungs_full.png', .48, 1.20, 4.64)
    textbox(slide, 'VISUAL EVIDENCE', 5.47, 1.36, 3.9, .25, 10, BLUE, True)
    bullet(slide, 'Chart: 19.1% with parser text, 45.5% with text + image.',
           5.47, 1.68, 3.95, .55, 12)
    bullet(slide, 'Figure: 23.8% with parser text, 44.8% with text + image.',
           5.47, 2.28, 3.95, .55, 12)
    textbox(slide, 'BORN-DIGITAL DOCUMENTS', 5.47, 2.98, 3.9, .25, 10, BLUE, True)
    bullet(slide, 'LongDocURL text gains 2.8 points with images; tables lose 1.3.',
           5.47, 3.28, 3.95, .64, 12)
    textbox(slide, 'COST AND FIDELITY', 5.47, 4.07, 3.9, .25, 10, BLUE, True)
    bullet(slide, 'Image-only prefill is about 21× embedded text.',
           5.47, 4.36, 3.95, .31, 11.5)
    bullet(slide, 'Text + low-res images keeps 90% of high-res accuracy.',
           5.47, 4.71, 3.95, .35, 11.5)
    notes(slide, [
        'This is Table 1 from the empirical paper, with every evidence-source row and all four representation modes. T is embedded text, TL parser text, TLV parser text plus image, and V image only. The table separates answerable-question abstention from answer accuracy.',
        'On MMLongBench-Doc, chart accuracy rises from 19.1 percent with parser text to 45.5 percent with parser text and the page image. Figure accuracy rises from 23.8 to 44.8 percent. Visual questions need the image. On born-digital LongDocURL, images add only 2.8 points on text questions, and table accuracy slips from 69.5 to 68.2 percent.',
        'Vision is expensive. On two V100 16 GB GPUs, image-only prefill takes 22.7 seconds against 1.1 seconds for embedded text, about 21 times as long. Text plus low-resolution images reaches 49.2 percent overall on 847 answerable questions, 90 percent of the 54.7 percent high-resolution result. This resolution result is discussed here but is not part of Table 1.',
    ])


def selection(slide, template):
    clear(slide)
    header(slide, template, 'Finding 2 · Selection',
           'Chapter 3 · Empirical study · Under review')
    textbox(slide, 'Gold evidence stays in context; extra pages still change the answer.',
            .45, .77, 9.1, .34, 14, BLUE, True)
    picture(slide, ASSETS / 'distractor_paper.png', .57, 1.21, 8.85)
    bullet(slide, '+3 distractors: multi-hop accuracy drops 43.9 → 35.1% for Qwen3 and 35.4 → 28.7% for Gemma-3.',
           .55, 4.51, 8.95, .31, 10.5, BLUE, True)
    bullet(slide, 'For Qwen3, 13.3% of answers break and 7.0% repair at +3; flips continue as more pages arrive.',
           .55, 4.84, 8.95, .31, 10.4)
    notes(slide, [
        'Figure 4 from the paper is the single unified distractor plot. Its panels show Qwen3-VL-8B and Gemma-3-12B on MMLongBench-Doc, plus Qwen3-VL-8B on LongDocURL. Every annotated gold page remains present; we add the highest-ranked non-gold pages.',
        'At plus three pages, Qwen3 multi-hop accuracy falls from 43.9 to 35.1 percent. Gemma-3 falls from 35.4 to 28.7 percent. The step-level bars show a mechanism behind the net loss: 13.3 percent of Qwen3 answers break while 7.0 percent repair at plus three.',
        'The repaired cases show that a non-gold page can still add a useful clue. More answers break than repair, and flips continue at later k values. Selection has to manage distractor exposure even when evidence recall is already complete.',
    ])


def reasoning(slide, template):
    clear(slide)
    header(slide, template, 'Finding 3 · Reasoning',
           'Chapter 3 · Empirical study · Under review')
    textbox(slide, 'Prompting and inference strategies have different accuracy and refusal trade-offs.',
            .45, .77, 9.1, .34, 13.7, BLUE, True)
    picture(slide, ASSETS / 'reasoning_calibration_six_modes.png', .45, 1.15, 9.1)
    bullet(slide, 'Abstain prompt: unanswerable correct 47.5 → 74.6%, but answerable correct 52.5 → 41.4%.',
           .5, 4.64, 9.0, .27, 10.4, BLUE, True)
    bullet(slide, 'Self-consistency adds 8.0 points answerable; Reflexion adds 13.9 points unanswerable vs plain.',
           .5, 4.95, 9.0, .24, 10.1)
    notes(slide, [
        'This new figure follows the paper prompt-calibration style and extends the Qwen3-VL-8B row from four prompt modes to six modes. A dotted line separates the two inference strategies, self-consistency and Reflexion, from the four prompt modes. The paper figure remains unchanged.',
        'The grey answerable segment is correctness from the accuracy judge. The blue segment above it is abstention on answerable questions from the taxonomy judge. Blue bars on unanswerable questions are correct results from the accuracy judge. These are judged outcomes, not string matches.',
        'An explicit abstain prompt moves unanswerable correctness from 47.5 to 74.6 percent, while answerable correctness falls from 52.5 to 41.4 percent. CoT plus abstain recovers answerable correctness to 53.0 percent and reaches 85.5 percent unanswerable correctness. Self-consistency reaches 60.6 percent answerable correctness, eight points above plain prompting, but 54.5 percent unanswerable correctness. Reflexion reaches 55.1 and 61.5 percent, gains of 2.5 and 13.9 points.',
        'The two strategy runs use 4-bit precision and different prompt settings, while the four prompt-mode runs use bf16, so these are observed comparisons rather than a matched causal estimate. Reflexion abstention is provisional, with rubric judgements for 294 of its 846 answerable accuracy cases. Self-consistency has 844 rubric-judged answerable cases.',
    ])


def main():
    deck = Presentation(SOURCE)
    template = Presentation(SOURCE).slides[11]
    assert len(deck.slides) == 21
    representation(deck.slides[11], template)
    selection(deck.slides[12], template)
    reasoning(deck.slides[13], template)
    deck.save(OUTPUT)
    print(OUTPUT)


if __name__ == '__main__':
    main()
