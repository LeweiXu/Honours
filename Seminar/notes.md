# Honours thesis seminar notes

## Seminar brief

- **Duration:** 15 minutes, plus 5 minutes of questions.
- **Audience:** Generalist computer science students, mostly fourth-year honours students, plus a few professors.
- **Thesis:** *Multi-Page Visually Rich Document Understanding: A Survey of System Design and an Empirical Attribution of Failure*, Lewei Xu. Source version: `Honours___Lewei_Xu-1.pdf`, the complete draft submitted for assessment.

## Slide 1: Title Slide

**Speaking cues**

- Hello everyone, my name is Lewei.
- This year, I’ve been working on document understanding.

**Transition:** Let me start with an outline of the seminar.

**On screen:** Thesis title and presenter name, Lewei Xu.

## Slide 2: Roadmap

**Speaking cues**

- Four parts: some background, then the survey, then the empirical study, then a small proof-of-concept method.
- The survey has been accepted to the EMNLP 2026 main conference. The empirical study is under review at EACL.

**Transition:** First, what do we mean by document understanding?

**On screen:** Four points: Background; the survey title in bold with authors and venue; the empirical paper the same way; the proof-of-concept method.

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

- Document understanding is a large field, such as research on upstream components like OCR models.
- But one broad way of defining document understanding is getting model or system to answer a natural language question over a document accurately.
- These models or systems can range from very simple ones like rule based lookup for information extraction or (as we'll see later) training vision language models, or leveraging pretrained general domain vision language models.
- Take these examples. The first is a simple fact lookup, and where to look may even be 
- The second asks us to read a table, including its layout. By the third, we have to compare values from two different tables and calculate the change.
- The last two go further. They ask us to connect claims with evidence across pages, and sometimes qualify the answer.
- We can ask all kinds of questions in natural language. The difficulty depends on what we need to find and put together.

**Transition:** Next, a brief history on document understanding.

**On screen:** Show five concrete example questions in increasing difficulty. These are illustrative until matched to specific pages from slide three; choose or adapt pages that contain the evidence before using them in the final deck.

1. What year was this report published?
2. According to the table, which region had the highest revenue in 2023?
3. How much did the leading region's revenue grow between the 2022 and 2023 results tables?
4. Does the growth described in the executive summary agree with the figures in the results table?
5. Across the report and its appendix, what evidence supports the conclusion that the new method improved performance, and what limitation qualifies that conclusion?

For the final slides, confirm that each question is answerable from the chosen document pages. The last two should visibly point to evidence on different pages.

**Source:** Thesis Chapter 1, Introduction, page 1, for the question-answering framing. The five questions above are illustrative seminar examples, not quoted benchmark questions.

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

## Slide 7: Survey of MP-VRDU

**Speaking cues**

- This is the survey, accepted to EMNLP 2026.
- I'll only cover the architecture overview, and mention the inference-time and training strategies in passing.
- I'm skipping the multimodal representation section, the datasets, and the open challenges.

**On screen:** Top half of the survey first page, with its section list on the right. Bold sections are the ones covered.

## Slide 8: Multi-page architectural overview

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

## Slide 9: Inference-time and training strategies

**Speaking cues**

- The rest of the survey is organised by three decisions: how to find evidence, how to reason over it, and how to go back for more.
- Each one can be done training-free around a frozen model, or trained into the model.

**Transition:** The survey maps the design choices. The second paper asks which of them actually matter.

**On screen:** Three columns: retrieval and navigation, reasoning strategies, agentic methods. Each lists the training-free and the trained variants.

## Slide 10: Empirical attribution study

**Speaking cues**

- This is the second paper, under review at EACL.
- When a system answers wrongly, different papers blame different things. We wanted to test that under controlled conditions.
- I'll cover the framework and the six findings, and skip the related work, discussion and deployment sections.

**On screen:** Top half of the paper first page, with its section list on the right. Bold sections are the ones covered.

## Slide 11: Attribution framework

**Speaking cues**

- Three places an answer can go wrong: representation, selection, and reasoning.
- Each has two mechanisms, which gives six things to test. One finding per mechanism follows.

**On screen:** The framework figure, with one diagnostic question under each locus.

## Slide 12: Modality ceiling

**Speaking cues**

- With text only, the model refuses chart and figure questions most. Adding page images brings refusal under 10% for every evidence type.
- Images alone are still worse than text plus images, 42.6% against 49.5%, because dense text and exact numbers are hard to read at limited resolution.

**On screen:** Table of abstention and accuracy by evidence source and representation.

## Slide 13: Conversion fidelity

**Speaking cues**

- Parser quality matters a lot with text alone: a 15.7-point spread on digital documents. Add the page image and it shrinks to 4.2.
- Same story the other way round: higher resolution helps images alone, and much less when parser text is there too.

**On screen:** Figure: accuracy by parser and scan status, and by image resolution.

## Slide 14: Evidence coverage

**Speaking cues**

- Take away one gold page and accuracy roughly halves, from 38.6% to 18.4% or 15.9%.
- It does not matter whether it was the highest or lowest ranked page, so retrieval rank does not tell you which page is safe to drop.

**On screen:** Figure: paired verdict transitions after removing or keeping gold pages.

## Slide 15: Distractor exposure

**Speaking cues**

- Here every gold page is kept and extra non-gold pages are added.
- Multi-hop accuracy drops from 43.9% to 35.1% after only three extra pages, then levels off. Single-hop declines slowly.

**On screen:** Figure: accuracy and step flips as non-gold pages are added.

## Slide 16: Evidence integration

**Speaking cues**

- With the gold pages supplied, a bigger model does better on multi-hop questions: 29.0% at 2B up to 49.9% at 32B.
- Single-hop improves too, so this is about using evidence in general, not only combining it.

**On screen:** Figure: single-hop and multi-hop accuracy across Qwen3-VL sizes.

## Slide 17: Response calibration

**Speaking cues**

- Telling the model it may abstain makes it refuse far more unanswerable questions, 13.2% to 76.1%, but it also starts refusing answerable ones.
- Asking it to reason first recovers most of the lost accuracy.

**On screen:** Figure: answerable accuracy and the two refusal rates across four prompt modes.

## Slide 18: Conclusion

**Speaking cues**

- Thank you. Happy to take questions.

**On screen:** Thank you, and nothing else.

## Slide 19: Simple method architecture

**Speaking cues**

- A proof of concept that applies the findings in one small system, with one model in three roles.
- The reader goes through pages in ranked order and records evidence. The synthesizer answers. The arbiter either accepts or sends the reader back for more.

**On screen:** The reader, synthesizer, arbiter loop, with one line under each role.

## Slide 20: Simple method results

**Speaking cues**

- 56.5% on MMLongBench-Doc and 61.3% on LongDocURL, the highest among systems on the same Qwen3-VL-8B backbone, with no training and a 4-bit model.
- Multi-page questions are still the weak spot, 39.2 against DocTrace's 41.1.

**On screen:** The results table under each benchmark's official protocol.

## Backup slides (21 onwards, no slide numbers)

For questions only.

- 21 to 25, survey: retrieval and navigation, reasoning strategies, agentic methods, training strategies, datasets.
- 26, 27, empirical setup: the pipeline and how a failure is isolated; the two datasets and the LLM judge.
- 28 to 30, transfer: the modality result on LongDocURL, distractors on Gemma3-12B, calibration on Gemma3-12B.
- 31, 32, deployment: representation cost, reasoner choice under a memory budget.
- 33, 34, method: how each finding maps to a design choice, and the inference cost.
