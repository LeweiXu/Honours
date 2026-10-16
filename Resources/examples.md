# Worked examples

Every qualitative example the paper and the thesis print, as plain text: the question,
the gold answer, what the reasoner said under each condition and how it was judged.
The reasoner is Qwen3-VL-8B at TLV with no instruction unless a row says otherwise, and
verdicts are the accuracy judge's. Each entry names the PDF and the gold pages (counted
from 1) so the page can be rasterised from `third_party/MMLongBench-Doc/data/documents/`.
Page numbers inside a Setting line or a quoted output are as the source gives them: the
appendix's Setting lines use zero-based page indices, one less than the PDF page.

This file is a copy for reuse (slides, talks). The sources are
`ops/scripts/figures/mechanism_examples.html` for the first six and
`Paper/appendix/appendix_C.tex` for the other nine; change those, not this.

## Main-text figure: one example per mechanism

The six cards of `mechanism_examples` (Figure "Qualitative analysis" in the paper and
the thesis). Quotes are cut to about a line; each card runs the conditions that fail,
the change that fixes them, then the conditions that succeed.

### Modality ceiling (mmlongbench:000085)

- **Locus:** Representation (Is the evidence in the input?)
- **Setting:** two inline icons, parsed as `<img>`
- **Document:** `honor_watch_gs_pro.pdf`, PDF page 16
- **Finding:** Colour exists only in pixels; a text input leaves the reasoner nothing to read.
- **Question:** What are the colors of the icons that the users touch to move the app up and remove the app respectively?
- **Gold:** gray, red

| Condition | Verdict | Output |
|---|---|---|
| T | wrong | “The document does not specify the colors” |
| TL | wrong | “it does not mention any visual details” |
| *fix: add the page image* | | |
| V | right | “The icon is gray. … The icon is red.” |
| TLV | right | “gray (a gray upward arrow) … red” |

- **Design implication:** Start text-only; add the page image only when the question asks about appearance.

### Conversion fidelity (mmlongbench:000158)

- **Locus:** Representation (Is the evidence in the input?)
- **Setting:** scanned slide, text by parser
- **Document:** `avalaunchpresentationsthatkickasteriskv3copy-150318114804-conversion-gate01_95.pdf`, PDF page 1
- **Finding:** The error sits in the transcript, not the reasoner, and each parser fails differently.
- **Question:** What is the name of the company that created this presentation?
- **Gold:** AVALAUNCH MEDIA

| Condition | Verdict | Output |
|---|---|---|
| PaddleOCR | wrong | “Asterks” (parse: KICK ASTERKS) |
| MinerU | wrong | “does not provide any evidence” |
| *fix: re-convert, or add the image* | | |
| Unlimited | right | “AVALAUNCH MEDIA” |
| with image | right | “Avalaunch Media … in the banner” |

- **Design implication:** Treat the parse as fallible: re-convert or attach the image when it is empty or implausible.

### Evidence coverage (mmlongbench:000141)

- **Locus:** Selection (Is the right evidence in context?)
- **Setting:** author list on pages 13, 14
- **Document:** `efd88e41c5f2606c57929cac6c1c0605.pdf`, PDF pages 14, 15
- **Finding:** Each page is relevant, yet neither suffices: the answer is a property of the page set.
- **Question:** How many chapter authors of this report come from Columbia University?
- **Gold:** 3

| Condition | Verdict | Output |
|---|---|---|
| page 13 | wrong | “two” (Horton, Kinney) |
| page 14 | wrong | “one” (Garcia-Pando) |
| *fix: add the complementary page* | | |
| both pages | right | “three” (Horton, Kinney, Garcia-Pando) |

- **Design implication:** Select evidence as a set: judge sufficiency of the whole set, not relevance page by page.

### Distractor exposure (mmlongbench:000934)

- **Locus:** Selection (Is the right evidence in context?)
- **Setting:** 10 gold pages of a 20-page deck
- **Document:** `c31e6580d0175ab3f9d99d1ff0bfa000.pdf`, PDF pages 8, 9, 10, 11, 12, 13, 15, 16, 17, 18
- **Finding:** A few added pages inflate the count; the gold set, or more context, counts right.
- **Question:** How many lateral bar graphs are present in the document?
- **Gold:** 10

| Condition | Verdict | Output |
|---|---|---|
| +3 pages | wrong | “there are 12 lateral bar graphs” |
| +5 pages | wrong | “there are 13 lateral bar graphs” |
| *fix: remove competing pages, or read on* | | |
| gold pages | right | “there are 10 lateral bar graphs” |
| +7 to +18 | right | “there are 10 lateral bar graphs” |

- **Design implication:** Retrieve broadly for recall, then filter or rerank what reaches the reasoner.

### Evidence integration (mmlongbench:000192)

- **Locus:** Reasoning (Is the evidence used correctly?)
- **Setting:** a diagram, an ablation table
- **Document:** `2303.08559v2.pdf`, PDF pages 8, 9
- **Finding:** Each size breaks a different step of one chain: locate the table, read the cell, compute.
- **Question:** If I drop the green module shown in Figure 6, what is the absolute percentage drop on 100-shot TACREV setting?
- **Gold:** 0.5%

| Condition | Verdict | Output |
|---|---|---|
| 2B | wrong | “2.4%” (reads another table) |
| 4B | wrong | “−9.6%” (right table, wrong row) |
| 8B | wrong | “(75.9 − 74.9) / 75.9 … ≈ 1.32%” |
| *fix: a larger reasoner* | | |
| 32B | right | “75.9 − 75.4 = 0.5” |

- **Design implication:** Match reasoner capacity to the operation; escalate questions that join a figure and a table.

### Response calibration (mmlongbench:000457)

- **Locus:** Reasoning (Is the evidence used correctly?)
- **Setting:** two tables, two pages
- **Document:** `STEPBACK.pdf`, PDF pages 5, 6
- **Finding:** The question is answerable; the abstain instruction turns multi-step difficulty into refusal.
- **Question:** How much lower is the accuracy of GPT-4 on SituatedQA compared to MMLU Chemistry?
- **Gold:** 16.7%

| Condition | Verdict | Output |
|---|---|---|
| none | right | “… 16.7 percentage points lower” |
| cot | right | “Step 1: … Answer: 16.7%” |
| abstain | declined | “Not answerable” (false refusal) |
| *fix: reason before deciding* | | |
| abstain_cot | right | “79.9% − 63.2% = 16.7%” |

- **Design implication:** Tune refusal jointly with reasoning on the deployed backbone, and report false refusals.

## Appendix boxes

The nine boxes of the paper's appendix C, at least one per mechanism, with fuller quotes
and a reading note each. None repeats a question from the main-text figure. The thesis's
additional worked-examples figure draws six of them: R1, R2, S1, S2, N1 and N2.

### R1. Modality ceiling (mmlongbench:000014)

- **Document:** `0e94b4197b10096b1f4c699701570fbf.pdf`, PDF page 14
- **Setting:** Presentation deck (Tutorial/Workshop), born-digital. Gold page 13, a single chart. Evidence source: chart.
- **Question:** According to the chart on page 14 how much time was spent with family and friends in 2010?
- **Gold:** 21%
- **Parser output:** The page is one chart, and the parser has nothing to transcribe. PaddleOCR-VL emits only a placeholder:

  ```
  <div style="text-align: center;"><img src="[...]" alt="Image" width="52%" /></div>
  ```

| Condition | Verdict | Output |
|---|---|---|
| T | declined | “The document does not provide any evidence or chart on page 14, so it is not possible to determine how much time was spent with family and friends in 2010 [...]” |
| TL | declined | “[...] The image referenced (on page 14) is not described or transcribed, so its content cannot be interpreted. [...]” |
| V | right | “According to the chart on page 14, in 2010, 21% of weekend time was spent with family and friends.” |
| TLV | right | “According to the chart on page 14, in 2010, 21% of weekend time was spent with family and friends.” |

- **Reading:** The gold page reaches every representation, so nothing is missing from the context. The value lives in the chart's geometry and no text channel carries it, so both text representations decline instead of guessing, which is the refusal pattern of the abstention table.

### R2. Conversion fidelity: parser (mmlongbench:000513)

- **Document:** `8dfc21ec151fb9d3578fc32d5c4e5df9.pdf`, PDF page 10
- **Setting:** Guidebook, born-digital. Gold page 9, a numbered list of market names with a code beside each. Evidence source: text and table.
- **Question:** How many geographic market names are listed under Los Angeles area?
- **Gold:** 13
- **Parser output:** The list runs from item 14 to item 26. The three parsers keep its text and differ in what they do with the code column:

  ```
  PaddleOCR-VL: California 14-26 / 14. San Fernando Valley (West) CA14 / [...] / 26. Santa Ana CA26
  MinerU 2.5: 14. San Fernando Valley (West) / [...] / 26. Santa AnaEPS / Code / 4.14 / [...] / 4.26
  Unlimited-OCR: <table><tr><td>14.</td><td>San Fernando Valley (West)</td><td>CA14</td></tr> [...]
  ```

| Condition | Verdict | Output |
|---|---|---|
| T | right | “The document lists **13** geographic market names under the Los Angeles area. [...]” |
| TL, PaddleOCR-VL | wrong | “26 The document lists 26 geographic market names under the ‘Los Angeles Area’ section, ranging from CA14 to CA26.” |
| TL, MinerU 2.5 | wrong | “26 The document lists 26 geographic market names [...] ranging from ‘San Fernando Valley (West)’ (item 14) to ‘Santa Ana’ (item 26).” |
| TL, Unlimited-OCR | right | “There are **13** geographic market names listed under the Los Angeles area. The list includes entries numbered 14 through 26 [...]” |
| TLV, PaddleOCR-VL | right | “[...] there are **13** geographic market names listed under the Los Angeles area. [...] codes from 14 to 26. Counting these entries [...]” |

- **Reading:** Every parser returns all thirteen names, yet two flatten the list so that its last label reads as its length. The parser that keeps the rows as a table gives the right count, as does the same flattened parse once the page image accompanies it: the image is the redundant channel that absorbs the conversion error.

### R3. Conversion fidelity: resolution (mmlongbench:000065)

- **Document:** `2310.05634v2.pdf`, PDF page 7
- **Setting:** Academic paper, born-digital. Gold page 6, a results table with one row per model and temperature. Evidence source: text and table.
- **Question:** From the paper, which temperature gives ChatGPT the highest alignment score?
- **Gold:** 0.1

| Condition | Verdict | Output |
|---|---|---|
| V, `low` | wrong | “[...] the temperature that gives ChatGPT the highest alignment score is **0.5**.” |
| V, `med` | wrong | “[...] is **0.5**. [...] Table 3 lists three ChatGPT models: ChatGPT (0.5), ChatGPT (0.1), and ChatGPT (0.9) [...]” |
| V, `high` | right | “[...] the temperature that gives ChatGPT the highest alignment score is **0.1**.” |
| TLV, `low` | right | “[...] ChatGPT (0.1): 85.9, ChatGPT (0.5): 84.5, ChatGPT (0.9): 84.1. [...] **85.9** is the highest alignment score, which corresponds to [...] **0.1**.” |

- **Reading:** The image alone finds the right table at every resolution but only reads its small digits correctly at `high`. With parser text the values are available as characters, so the lowest resolution already suffices, as in the table rows of the appendix's resolution table.

### S1. Evidence coverage (mmlongbench:000082)

- **Document:** `2312.10997v5.pdf`, PDF pages 9, 10
- **Setting:** Survey paper (Academic paper), born-digital. Gold pages 8 and 9: the sentence that answers the question starts on the last line of page 8 and finishes on page 9. `drop_top` leaves page 8 and `drop_bottom` page 9. Evidence source: text.
- **Question:** Which method integrates knowledge into white-box models via directive fine-tuning?
- **Gold:** PKG

| Condition | Verdict | Output |
|---|---|---|
| gold pages | right | “[...] the method that integrates knowledge into white-box models via directive fine-tuning is **PKG**. [...] ‘PKG introduces an innovative method for integrating knowledge into white-box models via directive fine-tuning [75].’ [...]” |
| `drop_top` | wrong | “[...] the method that integrates knowledge into white-box models via directive fine-tuning is **Fine-tuning Embedding Model**. [...]” |
| `drop_bottom` | wrong | “The method that integrates knowledge into white-box models via directive fine-tuning is **directive fine-tuning**. The document explicitly states: ‘introduces an innovative method for integrating knowledge into white-box models via directive fine-tuning [75].’ [...]” |

- **Reading:** Page 8 ends on the method's name and page 9 opens with what it does, so neither page holds the answer. With one of them withheld the reasoner does not decline: it names a nearby section heading, or repeats the question's own phrase. Both removals break the answer, so retrieval rank does not identify a page that can safely be omitted.

### S2. Distractor exposure: broken (mmlongbench:000078)

- **Document:** `2312.10997v5.pdf`, PDF pages 6, 17
- **Setting:** Survey paper (Academic paper), born-digital, multi-hop. Gold pages 5 (a table of methods) and 16 (the reference list). +3 adds pages 0, 6 and 7; page 0 is the survey's own title page. 4-bit weights.
- **Question:** What is the paper's full title that proposes the method that has a retrieval granularity of phrase?
- **Gold:** Copy is all you need.

| Condition | Verdict | Output |
|---|---|---|
| gold only | right | “[...] the method with a retrieval granularity of “Phrase” is **CoG [29]**. [...] the full title of the paper proposing the CoG method is: **“Copy is all you need”**. This is found in the References section [...]” |
| +3 | wrong | “[...] the paper's full title is **Retrieval-Augmented Generation for Large Language Models: A Survey**. This is explicitly stated in the title section of the document [...]” |
| +5 to +18 | wrong | The same answer at every completed depth. |

- **Reading:** Both gold pages are still present and nothing in them changed. The added title page is a plausible partial match for “the paper's full title”, and the reasoner takes it instead of following the table entry to its reference. Coverage is complete; the failure is in using the evidence amid competing context.

### S3. Distractor exposure: repaired (mmlongbench:000243)

- **Document:** `8e7c4cb542ad160f80fb3d795ada35d8.pdf`, PDF page 8
- **Setting:** Rezoning study (Research report), born-digital, single-hop. Gold page 7, which carries a table of residential capacity by borough. +3 adds pages 4, 8 and 12, the surrounding discussion. 4-bit weights.
- **Question:** What is the residential capacity of Staten Island from 2003 to 2007? Give me an integer.
- **Gold:** 435000000

| Condition | Verdict | Output |
|---|---|---|
| gold only | wrong | “80000” |
| +3 | right | “435000000” |
| +10 | right | “435000000” |
| +13 | wrong | “5980000” |
| +18 | right | “435000000” |

- **Reading:** The table holding the answer is supplied in every row. The reasoner misreads it in isolation and reads it correctly once neighbouring pages of the same section are present, then fails again at one deeper setting. Added pages therefore both repair and break answers on the same question, the two-way movement behind the transitions of the distractor figure.

### N1. Evidence integration (mmlongbench:001015)

- **Document:** `COSTCO_2021_10K.pdf`, PDF pages 36, 40
- **Setting:** Annual report (Financial report), born-digital, multi-hop. Gold pages 35 (the income statement) and 39 (the cash flow statement). Rows are Qwen3-VL sizes. Evidence source: table.
- **Question:** what is EBITDA for costco in FY2021?
- **Gold:** 8489

| Condition | Verdict | Output |
|---|---|---|
| 2B | wrong | “[...] EBITDA for Costco in FY2021 is $6,708 million. This is found in the [...] row labeled ‘Operating income’ [...]” |
| 4B | wrong | “The EBITDA for Costco in FY2021 is $6,708 million. [...] EBITDA [...] is typically calculated as Operating Income plus Depreciation and Amortization, but in this document, the ‘Operating income’ row is presented as the direct measure of EBITDA [...]” |
| 8B | wrong | “[...] Operating Income + Depreciation and Amortization + Interest Expense + Provision for Income Taxes = $6,708 + $1,781 + $(171) + $1,601 = **$8,469 million**” |
| 32B | right | “[...] From the Consolidated Statements of Income: Operating Income = $6,708 million. From the Consolidated Statements of Cash Flows: Depreciation and Amortization = $1,781 million. [...] $6,708 + $1,781 = **$8,489 million**” |

- **Reading:** Every model receives the same two statements. The two smallest stop at operating income on the first page, one of them after stating the formula that needs the second. The 8B reaches the cash flow statement but adds lines that operating income already excludes, and only the largest joins the two operands. The evidence was sufficient throughout; what scales is the ability to combine it.

### N2. Response calibration: answerable (mmlongbench:000418)

- **Document:** `ecommerceopportunityindia-141124010546-conversion-gate01_95.pdf`, PDF pages 12, 15
- **Setting:** E-commerce market deck (Research report), scanned, multi-hop. Gold pages 11 and 14, one bar chart on each. Evidence source: chart.
- **Question:** How many people in India were using a debit card when the e-commerce sales reached 11 billion?
- **Gold:** 399 million

| Condition | Verdict | Output |
|---|---|---|
| `none` | right | “[...] when e-commerce sales reached $11 billion (in 2014), the number of debit card users in India was **399 million**. [...]” |
| `cot` | right | “Step 1: [...] the $11 billion mark is shown for the year 2014. Step 2: [...] the bar chart titled ‘Number of Debit Card users in India (In millions)’ shows the value for 2014 as 399 million. [...] Answer: 399 million” |
| `abstain` | declined | “Not answerable” |
| `abstain_cot` | right | “Step 1: [...] e-commerce sales were $11 billion in 2014. Step 2: [...] For 2014, the number is 399 million. [...] Answer: 399 million” |

- **Reading:** The answer is on neither page alone: one chart gives the year, the other the count for that year. Under `abstain` the reasoner refuses a question it answers correctly with no instruction, a false refusal. Asking it to reason before deciding makes it locate both values first, and the refusal disappears.

### N3. Response calibration: unanswerable (mmlongbench:000047)

- **Document:** `ddoseattle-150627210357-lva1-app6891_95.pdf`, PDF pages none (unanswerable)
- **Setting:** Data-leadership talk (Tutorial/Workshop), scanned, unanswerable. BM25's top three pages (0, 1, 2) are supplied; the document mentions no video.
- **Question:** Which Youtube does the slides use to show the consequce of having a weak data leadership?
- **Gold:** Not answerable

| Condition | Verdict | Output |
|---|---|---|
| `none` | wrong | “The slides use a YouTube clip from the TV show *Breaking Bad* to illustrate the consequence of having weak data leadership [...] as symbolized by the character Walter White hoarding money [...]” |
| `cot` | right | “[...] Step 4: However, the document evidence does not mention any YouTube or reference any video content. The image is a still image, not a YouTube video. [...] Answer: Not specified in the document.” |
| `abstain` | right | “Not answerable” |
| `abstain_cot` | right | “[...] Step 3: The document does not mention YouTube at all. [...] Answer: Not answerable” |

- **Reading:** One supplied page shows a man holding stacks of money, and with no instruction the reasoner builds a show, a character and an interpretation out of it. Each of the other prompts leads it to check the premise against the pages and decline, which is the correct response here.
