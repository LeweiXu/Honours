# Honours thesis seminar script

- **Duration:** 15 minutes, plus 5 minutes of questions.
- **Audience:** Generalist computer science students, mostly fourth-year honours students, plus a few professors.
- **Deck:** `Seminar_final.pptx`, 21 slides. Slides 1 to 19 are the talk, 20 and 21 are backup.
- **Length:** slides 1 to 19 are about 2,100 words, or 14.0 minutes at 150 words a minute, before pauses and slide changes.
- Written to be spoken. Short forms are spelled out. Model, benchmark and conference names are left as they are.
- After editing, run `~/miniconda3/bin/python update_notes.py` to put these notes into the presenter notes of the pptx.

## Slide 1: Title

- Hello everyone, my name is Lewei, and I’ve been working on document understanding for my honours project this year.

## Slide 2: Thesis overview

- The thesis has four chapters, built around three research questions and two papers.
- First, I’ll go through some background: why long documents are hard, and why we care about a fixed compute budget.
- The first paper is a survey of how multi-page document understanding systems are designed.
- The second is an empirical study of where and why these systems fail. We use those findings to derive practical recommendations for designing and deploying them.
- If we have time, I’ll also show a very simple method that uses the empirical findings to build a working document understanding system.

## Slide 3: Multi-page visually rich documents

- First, what do we mean by a visually rich document?
- Documents carry meaning through text, visual elements like charts and figures, and how they are laid out on a page.
- A multi-page document simply has two or more pages, but its meaning can be spread across those pages and connected between them.
- Here is an example from one of our benchmarks: a forty-page guidebook for international students.
- The question asks for the coffee shop nearest to a point marked on the campus map.
- The map is on page 34. The coffee shops and their addresses are in a table on page 16. Neither page answers the question on its own.
- This shows the three things that make long documents hard.
- They are long: a document can exceed what a model can read at once.
- The evidence is sparse: here, two pages out of forty matter.
- And they are structured: the answer depends on connecting a map on one page to a table on another.

## Slide 4: Why a fixed compute budget?

- We can already see document understanding in the language model assistants we use. You upload a document and ask questions about it.
- Here’s an example from last week. I uploaded my thesis, which is close to a hundred pages, to Claude and asked it for a difficult question over the document.
- It picks a question that needs a figure and a table, plans its steps, locates the pages, and reads those pages as images before answering.
- But assistants are just one application. In industry, you might have one or a few specific tasks to perform over thousands or millions of documents.
- One major concern is privacy. Medical, legal and financial records often cannot be sent to a third-party service.
- Another is cost. Even without privacy concerns, processing that volume through a commercial API can be very expensive.
- And specialist document types may need a model adapted to them.
- So real deployments often need local, open-weight models, and everything has to fit within a fixed compute budget.
- That turns design into a set of choices: which pages to read, at what resolution, and how many times.

## Slide 5: Survey: managing evidence at document scale

- This is our survey of the field, which we completed earlier this year.
- It has been accepted at the EMNLP main conference, a top-tier conference in natural language processing.
- The main gap we wanted to address was that approaches to long document understanding had developed largely along parallel lines.
- They use different terminology, and there is little comparison across these different lines of work.
- We use evidence management as a conceptual framework to organise the field. We ask how systems preserve, find and use evidence across a document.
- This lets us define a taxonomy of four architectural families, covering 46 systems, and consolidate 47 datasets.
- I’ll focus on those families today, rather than go through every contribution of the survey.

## Slide 6: Four architectural families

- The first family is page-to-document encoding models, an early approach that extends single-page architectures to the multi-page setting.
- Each page is encoded separately into a compact representation. Those representations are connected through a cross-page mechanism, such as attention, and passed to a decoder to generate the final answer.
- The limitation is that pages contain different amounts of information. Giving each page a fixed representation budget can lose fine-grained detail during encoding.

- The second family adapts a pretrained multimodal large language model to process the document within its context window.
- Adaptation can involve continued pretraining on document tasks or fine-tuning. Some systems also compress the representations to fit longer documents.
- But performance can still degrade as documents get longer, and some documents cannot fit at all.

- This motivates retrieval-augmented pipelines. Instead of fitting the whole document into the model, we retrieve relevant evidence and pass a smaller evidence set to a vision-language model.
- Retrieval can be sophisticated, but the workflow is fixed in advance. Evidence missed during retrieval cannot be recovered by the answering stage.

- Finally, adaptive-trajectory pipelines follow an agentic approach. The language model decides what evidence to collect, how to collect it, and when it has enough to answer.
- But those repeated calls can become expensive, and make the total time and compute cost harder to bound.
- The dates show roughly when each family is active in the papers we surveyed. Each one fixes the bottleneck of the one before, and moves it somewhere else.
- We call the first two families models, because they are trained end to end. We call the last two pipelines, because their components are interchangeable.

## Slide 7: Surveyed systems at a glance

- This is the main table of the survey, with the systems and papers we surveyed grouped by architectural family.
- There are three things I want to point out, framed on the table.
- First, the backbone column for the two pipeline families. Their components are often interchangeable, especially the backbone language model, so many are tested with several backbones.
- As language models get stronger, these pipelines can benefit from those improvements too.
- Second, the modalities. Some systems use vision only, reading the document through page images.
- Others combine vision with text and layout information. The text may be embedded in the document or extracted by a parser.
- This distinction will be important in the next part of the seminar.
- Third, search. It only appears once retrieval is separated from answering, in the two pipeline families.

## Slide 8: Inference-time strategies

- Around a frozen model, systems change how evidence is selected, how the model reasons over it, or let an agent go and acquire more.

## Slide 9: Training strategies and datasets

- Pretraining is rare, fine-tuning carries most of the weight, and the benchmarks have grown from a few pages per document to hundreds.

## Slide 10: Open challenges

- The survey ends with five open challenges, and the one missing piece that motivates our second paper: an end-to-end account of where systems fail.

## Slide 11: Empirical study: locating failure in MP-VRDU

- This brings us to our second paper, an empirical attribution study, which is currently under review.
- The literature makes competing design claims. Some approaches favour vision alone, while others combine text and vision, each evaluated in a different setting.
- Prior studies show where accuracy drops, but not why. Failures at different stages produce the same wrong answer.
- This is our attribution framework, with three places where document understanding can fail.
- First, representation. We convert the document into text, rendered page images, or both. Was the information preserved during that conversion?
- Second, selection. We choose which pages reach the model. Did the required information actually reach it?
- Third, reasoning. Once the evidence is present in a usable representation, can the model use it correctly to produce an answer?
- From the results, we derive concrete guidance for deploying systems locally within a compute budget.

## Slide 12: Methodology: attribution by construction

- We use a simple encode, retrieve and answer pipeline, and each experiment changes one stage while holding the other two fixed.
- For representation, we vary the modality, the parser and the image resolution.
- For selection, we give the model the annotated gold pages, which bypasses retrieval, and then remove a page or add distractor pages.
- For reasoning, we vary the model size and the prompt, and we also try two strategies that spend more computation: self-consistency and Reflexion.
- The main benchmark is MMLongBench-Doc, with 135 documents and annotations for evidence pages, evidence type and answerability.
- Two model families and a second document collection provide checks on transfer.

## Slide 13: Finding 1, representation

- The first finding is about representation: text and vision are complementary, and neither alone is enough.
- The table shows how often the model declines to answer, and how often it is right, for each type of evidence and each representation.
- On scanned documents, the text embedded in the file is nearly useless. The model declines about 70 percent of questions. A parser recovers much of that, and adding the page image does best on every evidence type.
- On born-digital documents, in the lower half, text alone is already close, and the image adds only a few points.
- So how much of each you need depends heavily on the document type and the task. There is no one size fits all.
- The figure on the right shows why combining them works. Parser text alone answers 38 percent, a low-resolution image alone 38 percent, and together 49 percent. Text covers for low resolution.
- And the image covers for parser noise. Text only, the four text sources are 14 points apart. With the image added, they are 5 points apart.

## Slide 14: Finding 2, selection

- The second finding is about selection: evidence has to be selected as a set, not page by page.
- If we retrieve too little, required evidence is simply missing. Removing one gold page halves accuracy, from 38.6 to 18.4 percent, and the retrieval rank does not tell us which page is safe to lose.
- If we retrieve too much, the reasoner struggles to find and combine the evidence. On the right, every gold page is present, and accuracy still falls as we add more pages, most sharply for multi-hop questions.
- But the extra pages do not only hurt. With three added pages, 7 percent of questions flip from wrong to correct, while 13 percent break.
- After that first step, about 5 percent of answers flip in each direction every time we add more pages.
- So extra context repairs some answers while burying others, and there is no clear signal for when to stop.
- We need enough evidence to establish the answer, not just enough to generate one.

## Slide 15: Finding 3, reasoning

- The third finding is about reasoning.
- A question can contain a premise the document does not support. With no instruction, the model refuses only 45 percent of unanswerable questions and answers the rest fluently.
- Prompts change this behaviour. If we explicitly allow the model to say not answerable, it correctly refuses far more unanswerable questions, from 45.5 percent to 74.6 percent.
- But it also refuses more answerable ones, from 6.2 percent to 27.7 percent. Asking it to reason first wins most of that accuracy back.
- The second model family, Gemma-3 in the lower row, moves the same way.
- We can also spend more computation on reasoning. Self-consistency samples many reasoning paths and takes a vote. It adds about 8 points on answerable questions, at about 640 seconds a question.
- Reflexion lets the model retry after checking its own answer. It adds about 14 points on unanswerable questions, at about 47 seconds.
- These last numbers are preliminary, so I read them as a direction: more computation helps, at a price.

## Slide 16: From real failures to design

- Six mechanisms on real questions, two per failure point, each with the design choice it suggests.

## Slide 17: From findings to a simple method

- To check the findings, we put them into one small system. It is one model playing three roles.
- The reader goes through the pages in ranked order. For each page it sees both the text and the image, writes down any evidence it finds, and flags pages that may hold the answer.
- The synthesizer answers from the flagged pages in full and the short records of everything else.
- The arbiter cannot write an answer. It either accepts, or names a missing fact and sends the reader back for more pages.
- Each choice follows from a finding. Text and image together, for representation. Read broadly but pass on short records, for selection. And a separate step that judges whether the evidence is enough, for reasoning.

## Slide 18: Simple method: results

- All systems in this table use the same model with eight billion parameters.
- Ours reaches 56.5 percent on MMLongBench-Doc and 61.3 percent on LongDocURL, the highest in the table, without any training and with the model stored at four-bit precision.
- It is still behind the trained system DocTrace on questions that need several pages, 39.2 against 41.1.
- The cost is time: about eleven minutes per question on average.

## Slide 19: Conclusion

- To conclude, back to the three research questions.
- The survey organises the field. Understanding multi-page documents is a problem of evidence management, and four families of architecture handle it in different ways.
- The empirical study locates the failures. They sit at representation, at selection, or at reasoning, and each one needs a different fix.
- And a training-free system built on those findings is competitive under a fixed compute budget.
- Thank you. I am happy to take questions.

## Slide 20: Backup, deployment: accuracy and cost

- For questions: the accuracy and cost of each representation, retriever and reasoner choice.

## Slide 21: Backup, representative frameworks

- For questions: one example system from each of the four families.
