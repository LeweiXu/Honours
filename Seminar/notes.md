# Honours thesis seminar notes

## Slide 1: Title Slide

**Speaking cues**

- Hello everyone, my name is Lewei.
- This year, I’ve been working on document understanding.

**Transition:** Let me start with an outline of the seminar.

**On screen:** Thesis title and presenter name, Lewei Xu.

## Slide 2: Table of contents

**Speaking cues**

- An introduction, then the three parts of the thesis: the survey, the empirical study, and a small proof-of-concept method.

**Transition:** First, what do we mean by document understanding?

**On screen:** Five entries, with Introduction boxed.

## Slide 3: Multi-Page Visually Rich Documents

**Speaking cues**

- A document has pages that can contain text, tables, figures, and other visual content.
- As you can see in these examples, the meaning of a document is carried across content of varying modalities as well as the layout and structure within a page.
- This mix of prose and visual content is what we mean by *visually rich*.
- Multi-page simply means two or more pages, but it adds another layer of difficulty in that meaning can be carried between pages, for example a reference to a figure many pages apart.
- These examples also show how much the difficulty can vary.
- The born-digital research paper is relatively easy to read, with text we can extract directly.
- The scanned handwritten document is much harder, because the words are not available as embedded text.
- The scanned refrigerator manual looks clear to us, but its instructions also depend on the page layout.

**Transition:** So what does it mean to understand a document?

**On screen:** Show examples from thesis Figure 1.1: such as a born-digital research paper, a scanned handwritten document, and a scanned refrigerator technical manual. Keep this slide focused on the documents themselves.

**Source:** Thesis Figure 1.1, “Representative pages from MMLongBench-Doc,” page 3.

## Slide 4: What is document understanding?

**Speaking cues**

- One broad way of defining it is getting a system to answer a question over a document accurately.
- To do that it has to work out what is on each page: titles, paragraphs, charts, tables, captions.
- And it has to work out how the whole document is organised: which section a figure belongs to, which caption goes with which table.
- Take a question like the one on the right: does the model that humans rated best in Table 6 also have the best citation recall in Table 3? Table 6 is on this page and Table 3 is on the previous one, so neither answers it alone.
- A person does this without thinking. For a model it is hard, and it gets harder as the document gets longer.

**Transition:** You have all seen systems that do this.

**On screen:** Two pages with their layout elements boxed in colour, and an outline tree for the paper page on the right.

## Slide 5: LLM assistants

**Speaking cues**

- Everyone here has used these, so this is what it looks like from the outside.
- I gave Claude my thesis, which is almost 100 pages, and asked a hard question over it.
- It plans, works out which pages it needs, renders those pages and reads them as images, then answers.

**Transition:** That works for a consumer product. A lot of real settings cannot use it.

**On screen:** Left: the trajectory for a question over the thesis. Right: a zoomed view of the pages it rendered to read.

## Slide 6: Document understanding under real-world constraints

**Speaking cues**

- In the industry, such as in the medical field or mining industry, various organisations may want to perform some sort of document understanding task.
- This could be classification, summarisation or maybe information extraction requiring structured output over tens of thousands of documents.
- Documents could be highly sensitive and have data-residency requirements, so they can't be sent to a third party API.
- Sheer volumne of some workloads makes third party APIs simply too costly to be worth the cost (cost outweighs the benefits).
- And so, the more viable option is to perform these tasks locally using open-weight pre-trained VLMs on consumer hardware, not massive datacenters. 
- Cost and efficiency are big concerns are still ongoing areas of research for effient document understanding tasks.
- The specific document type as well could be very unique, so various training or fine-tuning techniques may have to be utilized.
- Research mainly focuses on this aspect: developing techniques and architectures for document understanding under fixed compute budgets, although all these techniques can be applied to consumer facing products (which is why we've seen so much development in recent years).

**Transition:** Next, let's discuss the survey of the field.

**On screen:** A large collection of reports, records, and scanned forms feeding into a local document system. Show two example tasks—classification and information extraction—and label the constraints: privacy, cost, and fixed compute. (just a suggestion, figure something out for this slide, some text as well to motivate the problem, title of slide should also be shorter and concise)

**Source:** Thesis Section 3.1, page 23. The examples motivate the research rather than report experimental findings.

## Slide 7: Table of contents: survey

**Speaking cues**

- The first part is the survey, accepted at the EMNLP 2026 main conference.

**On screen:** The contents with the survey boxed, showing the paper title, authors and venue.

## Slide 8: Survey: research gap and contributions

**Speaking cues**

- Multi-page systems were built along parallel lines with different terminology, and no survey treated multi-page as its own problem.
- The survey defines it as a problem of evidence management, gives a taxonomy, and consolidates the datasets and open challenges.
- I'll only show the architecture overview and mention the strategies in passing.

**On screen:** The gap on the left with a small diagram, three contributions on the right.

## Slide 9: Multi-page architectural overview

**Speaking cues**

- In the survey, we found that architectures for long document understanding could be grouped into these 4 families that we defined.
- These groups also follow a rough trend for how the field approached long document understanding.

- Around 2023-2024 with the mp-docvqa benchmark, we have these page-to-document models, and this includes the hi-vt5 baseline we discussed earlier.
- This was a somewhat naive but at the time very sound approach to the multi-page problem.
- The idea was quite simple, prior to 2023, a lot of research was done on single-page document understanding.
- These worked by training some form of vision language transformer model end-to-end to do question answering.
- If we want to scale to multiple pages, we could just combine these single page transformers, use the latent or hidden state of each page, perform some cross-page mechanism to learn cross-page structure or evidence integration, then put this final hidden state into a decoder to answer the question.
- The problem with these models is that page grows with page count linearly, and these models would struggle as soon as documents got decently long.

- At the time, with multimodal LLMs emerging, the field quickly pivoted to using pretrained these vision language models
- The idea was basically to use various techniques to adapt a general domain pretrained MLLM for long document understanding tasks.
- These techniques range from various document preprocessing before the document even reaches language model
- To doing continued pretraining on the language model itself on document understanding tasks
- Or parameter efficient fine tuning, indicated by the snowflake/flame
- The problem with this approach is the context length cap of the language model itself

- Next is basically just RAG. When RAG became a thing in 2024-2025, the field applied it to document understanding.
- We realized that answering a question over a document generally doesn't require the whole document.
- We only need to find the relevant evidence to answer the question.
- We can use various techniques to retrieve answer relevant evidence to have the language model which is generally frozen to answer the question
- This successfully avoids the context window problem, but instead shifts the problem to evidence retrieval.
- Techniques for this architecture can be very sophisticated, such as adaptive reranking and query reformulation to iteratively gather evidence
- This is why we avoid calling it "RAG pipelines" but rather "retrieval-augmented pipelines"

- Finally, in 2025ish, "agentic" systems became popular. 
- This is where we augment a langauge model to act iteratively in a loop for whatever task it is trying to complete.
- For long document understanding, a simple way to understand this is we have an agent that is given the question to answer and some instruction
- It needs to decide how to gather evidence, if more evidence is required to answer the question, and decide when to stop and answer the question when it deems enough evidence has been gathered.


**Transition:**

**On screen:** Simplified thesis Figure 2.1 showing the four architecture families. Keep one pathway per family.

**Source:** Thesis Sections 2.1–2.3, pages 7–11; Figure 2.1.

## Slide 10: Surveyed systems at a glance

**Speaking cues**

- This is the main table of the survey: every system we cover, grouped by the four families.
- First, the backbone. In the adaptive-trajectory family it is a general-domain MLLM, typically used as is, with no extra training or fine-tuning.
- Then three more things. Modalities: the encoding models fuse text, vision and layout, while the MLLM-centric ones are mostly vision only.
- Search only shows up once retrieval is separated from generation. Retrieval-augmented pipelines add one dense or joint retrieval step. Adaptive-trajectory pipelines add iterative retrieval, query reformulation and navigation.
- And reasoning techniques like ReAct and multi-agent designs concentrate in that last family.
- Next, one representative system from each family.

**On screen:** Table 1 of the survey on the left with five framed regions, numbered notes on the right.

## Slide 11: Page-to-document encoding: Hi-VT5

**Speaking cues**

- Hi-VT5 came with the MP-DocVQA benchmark in 2023.
- Each page goes through its own encoder with OCR text, layout and image patches. A few learnable page tokens summarise each page, and the decoder only reads those tokens.
- The limit is that a page gets squeezed into a few tokens, and cost grows with the number of pages.

**On screen:** The Hi-VT5 architecture figure, two bullets on how it works, one line on its limit.

## Slide 12: MLLM-centric adaptation: Docopilot

**Speaking cues**

- Docopilot is a native multi-page MLLM: the whole document goes into the context and there is no retrieval step.
- What makes it work is training data. They built Doc-750K from papers on Sci-Hub, arXiv and OpenReview.
- The limit is the context window, and accuracy already drops well before it is full.

**On screen:** The Doc-750K data pipeline figure, two bullets, one limit.

## Slide 13: Retrieval-augmented: MoLoRAG

**Speaking cues**

- MoLoRAG builds a graph over the pages and has a vision-language model walk it.
- Each page gets a semantic score and a logical relevance score, so it can reach pages that do not look similar to the question but are needed to answer it.
- The top pages go to a frozen model. Anything the traversal misses cannot be recovered afterwards.

**On screen:** The MoLoRAG framework figure, two bullets, one limit.

## Slide 14: Adaptive-trajectory: DocLens

**Speaking cues**

- DocLens has two parts. The lens module finds the relevant pages and then zooms into the figures, tables and text on them.
- The reasoning module samples several answers and an adjudicator picks one.
- It is accurate, but it makes many model calls per question, so the cost is hard to bound.

**On screen:** The DocLens workflow figure, two bullets, one limit.

## Slide 15: Table of contents: empirical study

**Speaking cues**

- The second part is the empirical study, under review at EACL.

**On screen:** The contents with the empirical study boxed, showing the paper title, authors and venue.

## Slide 16: Empirical study: research gap and contributions

**Speaking cues**

- Papers disagree about what matters: vision only or text plus vision, retrieve more or retrieve less. Each claim comes from a different pipeline and dataset, so they cannot be compared.
- The contribution is a framework of three failure loci, controlled interventions in one pipeline, and a check that the findings transfer.

**On screen:** The gap on the left with the three disagreements, three contributions on the right.

## Slide 17: One wrong answer, three possible causes

**Speaking cues**

- A real question from the benchmark: a 17-page course syllabus, and the question is how many quizzes there are in the whole course.
- The answer is six, but the table runs over two pages: four quizzes on one, two on the next.
- Say the system answers four instead of six.
- Maybe page 16 was converted badly and the quiz lines were lost. That is a representation failure.
- Maybe page 16 was never retrieved. That is a selection failure.
- Or maybe both pages arrived fine and the model still miscounted. That is a reasoning failure.
- The final accuracy number looks the same in all three cases, but the fix is different each time.

**Transition:** That is the framework.

**On screen:** The two pages and the question on the left. Three rows on the right: representation, selection, reasoning. The wrong answer of four is a hypothetical, the question is real.

## Slide 18: Attribution framework

**Speaking cues**

- Three places an answer can go wrong: representation, selection, and reasoning.
- Each has two mechanisms, which gives six things to test. One finding per mechanism follows.

**On screen:** The framework figure, with one diagnostic question under each locus.

## Slide 19: Attribution by construction

**Speaking cues**

- To separate the three, we use one simple pipeline: encode the pages, retrieve some, and answer in one pass.
- Each experiment changes one stage and holds the other two fixed.
- We can also hand the model the annotated gold pages directly, which takes retrieval out of the picture.
- Each result slide has a small strip at the top right showing which stage is being changed.

**On screen:** Encode, retrieve, answer as three boxes, with two bullets on gold pages and the dataset.

## Slide 20: Modality ceiling

**Speaking cues**

- With text only, the model refuses chart and figure questions most. Adding page images brings refusal under 10% for every evidence type.
- Images alone are still worse than text plus images, 42.6% against 49.5%, because dense text and exact numbers are hard to read at limited resolution.

**On screen:** Table of abstention and accuracy by evidence source and representation.

## Slide 21: Conversion fidelity

**Speaking cues**

- Parser quality matters a lot with text alone: a 15.7-point spread on digital documents. Add the page image and it shrinks to 4.2.
- Same story the other way round: higher resolution helps images alone, and much less when parser text is there too.

**On screen:** Figure: accuracy by parser and scan status, and by image resolution.

## Slide 22: Evidence coverage

**Speaking cues**

- Take away one gold page and accuracy roughly halves, from 38.6% to 18.4% or 15.9%.
- It does not matter whether it was the highest or lowest ranked page, so retrieval rank does not tell you which page is safe to drop.

**On screen:** Figure: paired verdict transitions after removing or keeping gold pages.

## Slide 23: Distractor exposure

**Speaking cues**

- Here every gold page is kept and extra non-gold pages are added.
- Multi-hop accuracy drops from 43.9% to 35.1% after only three extra pages, then levels off. Single-hop declines slowly.

**On screen:** Figure: accuracy and step flips as non-gold pages are added.

## Slide 24: Evidence integration

**Speaking cues**

- With the gold pages supplied, a bigger model does better on multi-hop questions: 29.0% at 2B up to 49.9% at 32B.
- Single-hop improves too, so this is about using evidence in general, not only combining it.

**On screen:** Figure: single-hop and multi-hop accuracy across Qwen3-VL sizes.

## Slide 25: Response calibration

**Speaking cues**

- Telling the model it may abstain makes it refuse far more unanswerable questions, 13.2% to 76.1%, but it also starts refusing answerable ones.
- Asking it to reason first recovers most of the lost accuracy.

**On screen:** Figure: answerable accuracy and the two refusal rates across four prompt modes.

## Slide 26: Table of contents: proof of concept

**Speaking cues**

- The last part is a small proof of concept.

**On screen:** The contents with the proof of concept boxed.

## Slide 27: From findings to a simple method

**Speaking cues**

- The last part is a proof of concept: put the findings into one small system and see if they hold up.
- It is one model in three roles. The reader goes through pages in ranked order and records evidence. The synthesizer answers. The arbiter accepts, or sends the reader back.
- Each design choice comes from a finding: read text and image together, read broadly but pass on compact records, and have a separate step decide whether the evidence is enough.

**On screen:** The reader, synthesizer, arbiter loop, with one design choice under each of representation, selection and reasoning.

## Slide 28: Simple method results

**Speaking cues**

- 56.5% on MMLongBench-Doc and 61.3% on LongDocURL, the highest among systems on the same Qwen3-VL-8B backbone, with no training and a 4-bit model.
- Multi-page questions are still the weak spot, 39.2 against DocTrace's 41.1.

**On screen:** The results table under each benchmark's official protocol.

## Slide 29: Conclusion

**Speaking cues**

- To sum up: the survey organises the field around evidence management, the empirical study locates where failures come from, and the proof of concept shows the findings hold in a working system.
- Thank you. Happy to take questions.

**On screen:** Three cards restating the contributions, then thank you.

## Backup slides (30 onwards, no slide numbers)

For questions only.

- 30 to 35, survey: inference-time and training strategies, retrieval and navigation, reasoning strategies, agentic methods, training strategies, datasets.
- 36, 37, empirical setup: the pipeline and how a failure is isolated; the two datasets and the LLM judge.
- 38 to 40, transfer: the modality result on LongDocURL, distractors on Gemma3-12B, calibration on Gemma3-12B.
- 41, 42, deployment: representation cost, reasoner choice under a memory budget.
- 43, 44, method: how each finding maps to a design choice, and the inference cost.
