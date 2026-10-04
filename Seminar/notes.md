# Honours thesis seminar notes

## Seminar brief

- **Duration:** 20 minutes.
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

- I’ll cover the work done this year in three parts.
- First, I'll quickly go over some background on document understanding.
- Then, the main ideas from the survey I wrote in the first semester, which has been accepted into a top-tier conference.
- Finally, the empirical study I wrote in the second semester which is about how document understanding can fail and how to mitigate these failures.

**Transition:** First, what do we mean by document understanding?

**On screen:** Three bullets:

- **Background** — Multi-page, visually rich document understanding.
- **Survey** — *Managing Evidence at Document Scale: A Survey of Multi-Page Visually Rich Document Understanding* (EMNLP 2026 main conference).
- **Empirical attribution study** — *Locating Failure in Multi-Page Visually Rich Document Understanding: An Empirical Attribution* (submitted to EACL; under review).

**Source:** Submitted thesis Section 1.2, page 2, for paper titles and status.

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

## Slide 5: Brief History

**Speaking cues**

- A useful starting point is with the MP-DocVQA paper from 2023.
- It introduced a benchmark with documents of up to twenty pages with questions answerable from a single page.
- It also introduced a baseline model called Hi-VT5 to answer natural language questions for this specific setting.
- This is considering the pivotal starting point for long document understanding research.
- A lot happened in between, and the field progressed rapidly with more difficult benchmarks and more sophisticated techniques that utilized vision language models as backbones, which we'll discuss in the survey.
- Newer benchmarks include documents that spand hundreds of pages and include questions that require combining evidence from various locations.
- Meanwhile, vision language models became better at reading text and page images.

**Transition:** Next, some motivation or use cases of document understanding.

**On screen:** Two simple parts. **Benchmarks:** MP-DocVQA (2023; up to 20 pages; one answer page) → MMLongBench-Doc and LongDocURL (longer documents; some questions span pages). **Models:** training models end-to-end -> leveraging general domain VLMs with increasing sophisticated training and training-free metods.

**Source:** Submitted thesis Sections 1.3.1–1.3.3, pages 3–5, and Section 3.5, pages 31–34. [MP-DocVQA paper](https://doi.org/10.1016/j.patcog.2023.109834), published in 2023. The later benchmarks contain cross-page questions; not every question in them is multi-hop.

## Slide 6: Document questions in consumer assistants

**Speaking cues**

- Consumer facing products like GPT, Claude and NotebookLM, I'm sure everything here is familiar with these.
- Just a year or two back, we could upload relatively short documents and the model could answer relatively well.
- But document understanding using language models was still at its infancy at the time.
- What would happen is the whole document, including the parsed text output and an image of each page would be placed in the model's context.
- Which is why very quickly you'll see an error message saying "can't upload document, out of context".
- More recently, we've begun to see more sophisticated methods.
- Nowadays, when you upload a document, it actually gets placed on disk in the model's "working environment".
- The model can access the document using tool calls.
- Also with the "projects" feature, you can upload a lot of documents, and RAG techniques can be used retrieve information from these documents.

**Transition:** But, this is just a very specific use case for document understanding for the general public.

**On screen:** A familiar assistant answering a question about uploaded files. Show an error message saying "cannot upload document, out of context". Screenshot of current chatbot assistants accessing documents via tool calls, or RAG from projects.

**Source:** Submitted thesis Sections 1.3.2–1.3.3, pages 5–6. [ChatGPT Projects documentation](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) confirms uploaded project files can be used as context; [OpenAI file uploads FAQ](https://help.openai.com/en/articles/8555545-file-uploads-faq) confirms document search use cases. The precise file-handling path varies by product and configuration.

## Slide 7: Document understanding under real-world constraints

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

## Slide 9: Text modality, volume

**Speaking cues**

- The rest of the survey does get fairly technical, and theres a lot of content, so for the rest of the survey, i'll just quickly go over it so everyone can gain an appreciation of just how much research has been done in the field.

- Volume: the text across all the pages frequently exceeds the MLLM's context.
- Systems compress it into a fixed budget, train for a longer context, or index chunks and pass only the selected text to the reader.

**On screen:** All 160 pages of the 3M 2018 10-K as a contact sheet, about 89,000 words.

## Slide 10: Text modality, continuity

**Speaking cues**

- Continuity breaks when paragraphs, tables and sections span page boundaries.
- It is preserved with document-level layers over per-page representations, or with structure-aware chunking and adjacent-page expansion at retrieval time.

**On screen:** A sentence in a paper cut in half by the page 3 to page 4 break.

## Slide 11: Text modality, noise

**Speaking cues**

- Noise: OCR errors accumulate across the document, and they also end up in the retrieval index.
- Layout-aware OCR pipelines dampen it upstream, or low-confidence tokens are treated as soft cues downstream.

**On screen:** A handwritten power of attorney scan, with the raw Tesseract output under it.

## Slide 12: Text modality, heterogeneity

**Speaking cues**

- Heterogeneity: text density varies a lot from page to page, but almost every system uses fixed-budget allocation.
- Adaptive page selection is the rare question-conditioned exception.

**Transition:** Some evidence is difficult to recover from text alone. That is where page images matter.

**On screen:** Two pages from the same 10-K: page 55 with 75 words, page 68 with 946.

**Source:** Thesis Section 2.4.1, pages 11–12. Survey Section 4.1.

## Slide 13: Visual modality, resolution

**Speaking cues**

- Resolution: fine detail is only legible at high resolution, and token cost scales super-linearly with it, so it cannot be maintained at full document length.

**On screen:** The same chart cropped from the page rendered at 340 x 440 px and at 1275 x 1650 px.

## Slide 14: Visual modality, resolution trade-off

**Speaking cues**

- Token-reduction modules keep every page available at lower fidelity.
- The alternatives are thumbnail browsing with selective high-resolution inspection, or high-fidelity reading of only the retrieved pages, which inherits the selector's recall ceiling.

**On screen:** One 23-page Pew report twice: every page blurred, versus three sharp pages with the other twenty blank.

## Slide 15: Visual modality, multi-signal competition

**Speaking cues**

- Multi-signal competition: text-bearing pixels, non-textual evidence and layout cues share one per-page budget.
- Visual RAG keeps patch-level granularity, element-level cropping keeps fine structure, and OCR-augmented visual reading delegates the text so the visual budget can go to non-textual evidence.

**Transition:** Beyond text and images, a document has relationships that connect its pages.

**On screen:** One Pew report page with its body text, chart and source note outlined, and each one zoomed beside it.

**Source:** Thesis Section 2.4.2, page 12. Survey Section 4.2.

## Slide 16: Structure modality, hierarchy

**Speaking cues**

- Hierarchy: sections, headings and reading order organise the document as a whole rather than any single page.
- Explicit parsers recover it as outlines or hierarchical indices, or OCR-free backbones learn it end-to-end from page images.

**On screen:** The table of contents of the Pew report.

## Slide 17: Structure modality, cross-page references

**Speaking cues**

- Cross-page references: a pointer like "see Table 13" has to be resolved to its referent on another page, which ranking by surface similarity cannot do.
- Graph- and map-based methods represent the references as edges between document elements, with edge quality bounded by the extraction heuristics.

**On screen:** A sentence on page 4 of a paper that points to Table 13, which is on page 19 in an appendix.

## Slide 18: Structure modality, spanning elements

**Speaking cues**

- Spanning elements such as multi-page tables need a representation that bridges the page boundary without conflating distant content.
- Hierarchical indexing and context-fused page embeddings preserve the parent context.

**Transition:** Once the document is represented, how do we find the right evidence for a question?

**On screen:** A syllabus table that runs over pages 15 and 16, with the benchmark question that needs both halves: how many quizzes are in the course (six).

**Source:** Thesis Section 2.4.3, pages 12–13. Survey Section 4.3.

## Slide 19: Retrieval and navigation

**Speaking cues**

- Retrieval narrows a long document to compact evidence units: chunks, pages, or graph nodes.
- Similarity-based retrieval scores each evidence unit independently against the query. Sparse lexical signals like BM25 are the baseline, and dense retrieval uses late-interaction encoders like ColPali and ColQwen.
- Relation-aware retrieval goes along explicit document structure instead: tree-based over section hierarchies, or graph-based over cross-references.
- Independent scoring cannot follow cross-page references or multi-hop dependencies. Relation-aware methods can, but depend on parser quality.
- Evidence missed at retrieval is unrecoverable at generation.

**Transition:** Finding evidence is only part of the task. The model still has to reason with it.

**On screen:** Question → search or navigate → selected evidence. Use one example showing that two pages may both be needed.

**Source:** Thesis Section 2.5.1, pages 13–14.

## Slide 20: Reasoning strategies

**Speaking cues**

- Reasoning strategies act over a single evidence buffer assembled before the reasoning call.
- Sequential reasoning extends one thread: Chain-of-Thought binds evidence from different pages into one chain, and Self-Reflection revises a draft answer across rounds.
- Parallel exploration produces several paths over the same buffer: Self-Consistency takes the majority answer, and sampling-adjudication uses an LLM judge instead of a vote.
- Cost scales with the number of rounds or samples.
- None of it can recover what retrieval missed.

**Transition:** Some systems address missing evidence by letting the model look again.

**On screen:** Two evidence pages feeding into a short reasoning chain and answer. Keep the reasoning example simple.

**Source:** Thesis Section 2.5.2, pages 14–15.

## Slide 21: Agentic methods

**Speaking cues**

- Agentic methods put one or more LLM controllers in charge.
- ReAct and tool-augmented reasoning: one controller interleaves thought, action and observation, calling retrievers, parsers or OCR engines, or navigating a pre-built document representation.
- Multi-agent orchestration: modality-specialised decomposition splits text and visual evidence, role-specialised decomposition splits planning, execution, verification and synthesis.
- Because the trajectory is adaptive, compute scales with question difficulty rather than document length, and it lifts the single-step recall ceiling of retrieval-augmented pipelines.
- The cost is controllability: unbounded inference cost, and a controller can commit early to wrong evidence.

**Transition:** So far, these choices can happen at inference time. Training can also teach a system to make them.

**On screen:** A short loop: inspect → assess → search or inspect again → answer. Optionally show separate reader and checker roles.

**Source:** Thesis Sections 2.3.4 and 2.5.3, pages 10–11 and 15–16.

## Slide 22: Training strategies

**Speaking cues**

- Most systems adopt a backbone already pretrained on single-page data, so fine-tuning carries the weight.
- Trained retrieval components: modality-alignment, cross-page-fusion, and logical-relevance.
- Trained reasoning methods: trace-imitation first, then reward-driven training with GRPO.
- Trained agentic methods: trajectory-distillation from a stronger teacher, or reinforcement-learned policies.
- Parameter-efficient tuning and multi-stage curricula recur across all three.

**Transition:** That makes the available datasets a central part of the field.

**On screen:** A pipeline with three trainable stages highlighted: find, combine, decide the next action.

**Source:** Thesis Section 2.6, pages 17–19.

## Slide 23: Datasets

**Speaking cues**

- Datasets serve three roles: pretraining, fine-tuning, and benchmarking.
- Per-page annotation does not scale, so pretraining is the exception and fine-tuning has converged on LVLM-synthesised supervision over scraped PDFs.
- Benchmarks sit in three tiers, from single-page extractive baselines to long-document multimodal benchmarks, and reuse the same small pool of PDFs, which is a contamination risk.
- Answer-only accuracy masks retrieval failure, so we also want to know whether the right evidence was found and used.

**Transition:** The survey maps the design choices. But when a system gives a wrong answer, which part actually failed?

**On screen:** Three roles for datasets: pretrain, fine-tune, benchmark. Add a small answer-and-evidence check beside benchmarking.

**Source:** Thesis Section 2.7, pages 19–21.

## Slide 24: Why locate the failure?

**Speaking cues**

- The survey showed many possible ways to build these systems.
- But different papers give different explanations for why they fail.
- Maybe the page was read badly, maybe the right page was missed, or maybe the model could not use it.
- Those failures need different fixes, especially when we have a limited compute budget.
- That is the motivation for the empirical study.

**Transition:** I describe those possibilities as three failure loci.

**On screen:** One document question, one wrong answer, and three possible points of failure along a simple pipeline. Emphasize the diagnostic question, not detailed methods.

**Source:** Submitted thesis Section 3.1, pages 22–23.

## Slide 25: Three failure loci

**Speaking cues**

- I divide failures into three places in the pipeline.
- Representation asks whether we preserved the needed information from the page.
- Selection asks whether that information reached the model.
- Reasoning asks whether the model used it correctly.
- The order matters: we cannot reason over evidence that was lost or never selected.

**Transition:** We can test each stage by controlling what happens in the others.

**On screen:** Simplify thesis Figure 3.1 to document → representation → selection → reasoning → answer. Put one plain-language failure question under each of the three stages.

**Source:** Submitted thesis Section 3.3, pages 23–25; Figure 3.1.

## Slide 26: How we isolate a failure

**Speaking cues**

- The experiments use one simple pipeline throughout.
- First, we turn pages into text, images, or both.
- Then a retriever chooses pages, and a multimodal model answers from them.
- To isolate a failure, we change one condition while holding the others fixed.
- For some tests, we give the model the known evidence pages directly.

**Transition:** The first set of interventions changes what the model can see from a page.

**On screen:** Encoding → page retrieval → answer. Highlight one stage at a time; show “gold pages supplied” as a bypass around retrieval. Use thesis Table 3.1 as the detailed source, not as a full-size slide table.

**Source:** Submitted thesis Section 3.4.1, pages 25–26; Table 3.1.

## Slide 27: Representation experiments

**Speaking cues**

- The representation tests ask two questions.
- First, what can different inputs express? We compare text, layout, images, and their combinations.
- Second, how much information is lost when we convert the page?
- For that, we vary the parser and image resolution.
- The correct evidence pages are supplied, so retrieval is not the variable here.

**Transition:** Next, we control which of those pages are actually selected.

**On screen:** Two compact experiments: four representation options; then parser quality and image resolution. Label these “modality ceiling” and “conversion fidelity.”

**Source:** Submitted thesis Sections 3.3.1 and 3.4.2, pages 24 and 27–28.

## Slide 28: Selection experiments

**Speaking cues**

- For selection, we separate missing evidence from distracting extra content.
- We start with the pages known to contain the answer.
- In one test, we remove a required page.
- In another, we keep all required pages but add irrelevant ones.
- The encoding and reasoner stay fixed, so we can compare the two effects.

**Transition:** We then test failures that remain even when the evidence is present.

**On screen:** A complete evidence set branching into two conditions: one required page removed; extra irrelevant pages added. Label “coverage” and “distractor exposure.”

**Source:** Submitted thesis Sections 3.3.2 and 3.4.3, pages 24–25 and 28–29.

## Slide 29: Reasoning experiments

**Speaking cues**

- For reasoning, we again provide the known evidence pages.
- One test asks whether the model can combine facts from several pages.
- We compare evidence structures and a step-by-step reasoning prompt.
- Another test asks whether it should answer or abstain when evidence is insufficient.
- These are different reasoning problems, so we test them separately.

**Transition:** Two annotated benchmarks let us make these comparisons.

**On screen:** Two experiment cards: cross-page integration; answer versus abstain. Keep prompt text out of the main slide.

**Source:** Submitted thesis Sections 3.3.3 and 3.4.4, pages 25 and 29–30.

## Slide 30: Datasets make attribution possible

**Speaking cues**

- The main benchmark tells us which pages support each question and what kind of evidence is needed.
- It also includes questions that the document cannot answer.
- That lets us test coverage, representation, and abstention directly.
- A second benchmark checks the findings on longer documents.
- We track refusals and wrong answers as well as overall accuracy.

**Transition:** With the setup in place, let’s look at what fails first: representation.

**On screen:** Two benchmark cards: MMLongBench-Doc as the primary diagnostic dataset; LongDocURL as the secondary replication dataset. Show only the annotations relevant to the experiments.

**Source:** Submitted thesis Section 3.5, pages 31–34.

## Slide 31: Result: text and vision complement each other

**Speaking cues**

- When the correct pages are supplied, text alone still misses many visual questions.
- Adding the page image makes charts and figures much easier to answer.
- But images alone are also weaker than the combined input.
- The text channel helps with fine details that may be hard to read from the image.
- So text and vision complement each other, although the benefit depends on the document collection.

**Transition:** Preserving both channels helps, but the conversion into those channels can still fail.

**On screen:** Simplified comparison from thesis Table 3.13: overall accuracy 29.0% text only, 42.6% image only, 49.5% text + layout + image on MMLongBench-Doc. If space allows, show chart/figure rows to explain the visual benefit.

**Source:** Submitted thesis Section 3.6.1.1, pages 35–36; Table 3.13 and Figure 3.5. The percentages are condition-specific benchmark results.

## Slide 32: Result: conversion quality matters

**Speaking cues**

- Even a useful input type can fail if the page is converted badly.
- For scanned pages, the PDF’s embedded text may be absent or sparse.
- Parsers also differ in how well they recover text and structure.
- Adding the page image can compensate for some parser mistakes.
- Higher image resolution matters most when small visual details are essential.

**Transition:** After representation, the next question is whether the right evidence is selected.

**On screen:** One parser comparison for scanned pages, with and without the page image, from Figure 3.6. Optionally include a small high-versus-low resolution crop from Table 3.14.

**Source:** Submitted thesis Section 3.6.1.2, pages 36–37; Figure 3.6 and Table 3.14.

## Slide 33: Result: missing evidence is costly

**Speaking cues**

- Next, we remove one page that the question needs.
- Many answers that were correct become wrong immediately.
- This is especially difficult when the answer depends on several pages.
- The model usually cannot reconstruct a missing fact from the other pages.
- So finding all the required evidence is a hard constraint on the pipeline.

**Transition:** But what happens if retrieval brings back a few extra pages as well?

**On screen:** Thesis Figure 3.7, simplified to show correct → incorrect transitions when one gold page is removed. For MMLongBench-Doc, emphasize that 24.7–27.0% of previously correct answers break in the one-page-removal conditions.

**Source:** Submitted thesis Section 3.6.2.1, pages 37–38; Figure 3.7.

## Slide 34: Result: moderate distraction is less damaging

**Speaking cues**

- Now consider the opposite error: retrieval includes a few extra pages.
- Within the range we tested, accuracy changes much less than when required evidence is missing.
- There is still some decline, especially for questions needing several pages.
- But the two errors are not equally damaging.
- This suggests that retrieval should lean toward coverage when the later context can handle it.

**Transition:** Even with all the right pages present, the model can still struggle to combine them.

**On screen:** A compact visual from Table 3.15 comparing a complete gold set with the same set plus one to five distractor pages. Put “tested range” on the slide to bound the claim.

**Source:** Submitted thesis Section 3.6.2.2, pages 38–39; Table 3.15.

## Slide 35: Result: reasoning across pages remains hard

**Speaking cues**

- Even with all the correct pages supplied, cross-page questions remain difficult.
- Asking the model to reason step by step helps some of them.
- The benefit is especially noticeable for structured evidence such as tables.
- But the same prompt does not help every question or every benchmark.
- More reasoning is useful when it matches the actual task.

**Transition:** Reasoning also includes a decision about whether the evidence supports an answer.

**On screen:** Thesis Figure 3.9, simplified to show the cross-page gain on MMLongBench-Doc and the lack of the same gain on LongDocURL. Avoid presenting the prompt as a universal improvement.

**Source:** Submitted thesis Section 3.6.3.1, pages 39–41; Figure 3.9 and Table 3.16.

## Slide 36: Result: abstention is not well calibrated

**Speaking cues**

- Finally, the model must decide whether the available evidence supports an answer.
- An abstention instruction reduces unsupported answers by making the model more cautious.
- But it also makes the model refuse more questions that are answerable.
- The prompt changes its willingness to answer.
- It does not reliably improve its judgement of whether the evidence is sufficient.

**Transition:** These results suggest concrete design choices. I tested them together in a simple adaptive method.

**On screen:** Thesis Figure 3.10. Show both sides of the trade-off: refusal on unanswerable questions rises from 45.5% to 74.6%; refusal on answerable questions rises from 6.2% to 27.7%.

**Source:** Submitted thesis Section 3.6.3.2, pages 41–42; Figure 3.10.

## Slide 37: A simple adaptive method

**Speaking cues**

- The survey and experiments suggest several practical design principles.
- I put them together in a deliberately simple system.
- It keeps text and images, gathers evidence broadly, and presents selected pages in full when answering.
- It also checks whether the answer is supported before stopping.
- The goal is to validate the principles at the system level.

**Transition:** Here is how the evidence moves through the system.

**On screen:** Three principles mapped to the attribution pipeline: complementary text and vision → broad acquisition with selective presentation → reasoning and evidence check.

**Source:** Submitted thesis Chapter 4 introduction and Section 4.1, pages 49–50.

## Slide 38: Reader, synthesizer, arbiter

**Speaking cues**

- The method uses one underlying model in three roles.
- The reader works through ranked pages and records useful evidence.
- The synthesizer gets the most important pages in full, plus short records from other pages, and proposes an answer.
- The arbiter decides whether to accept it or send the reader back for more.
- That makes the amount of reading adapt to the question.

**Transition:** Does this simple combination actually work on the benchmark?

**On screen:** Thesis Figure 4.1, simplified: ranked pages → reader → synthesizer → arbiter → answer or continue. Label the full pages and compact records separately.

**Source:** Submitted thesis Section 4.1.1, pages 49–50; Figure 4.1.

## Slide 39: System-level validation and its cost

**Speaking cues**

- On the benchmark, the method reaches 54.5 percent under the official scorer.
- That is above the gold-page baseline using the same model family.
- It suggests that useful context can come from beyond the annotated answer pages.
- The gain is not uniform: cross-page questions are still hard.
- The system fits on one sixteen-gigabyte GPU, but the repeated reading makes it slow.

**Transition:** What should we take away from the thesis as a whole?

**On screen:** From thesis Table 4.1, show the official-score comparison: gold-page baseline **49.5%**, this method **54.5%**, and the strongest same-backbone published comparison **52.9%**. Add a small cost note from Table 4.2: mean peak memory **8.2 GiB**; median total latency about **9.3 minutes per question**. Do not compare scores from different evaluation protocols as though they were the same metric.

**Source:** Submitted thesis Sections 4.1.2–4.1.3, pages 51–53; Tables 4.1–4.2. The 54.5% result uses the official MMLongBench-Doc protocol.

## Slide 40: Conclusion

**Speaking cues**

- The main message is that long-document understanding depends on managing evidence well.
- The survey maps the ways systems preserve, find, and use information across pages.
- The empirical study shows where failures arise: representation, selection, or reasoning.
- The simple method shows these lessons can guide a working system.
- The same diagnostic view can help future systems improve. Thank you, and I’m happy to take questions.

**On screen:** One final pipeline: preserve → select → reason. Under it, the three thesis contributions: survey, failure attribution, system-level validation.

**Source:** Submitted thesis Section 4.3, page 56.
