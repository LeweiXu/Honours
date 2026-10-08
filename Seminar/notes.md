# Honours thesis seminar script

- **Duration:** 15 minutes, plus 5 minutes of questions.
- **Audience:** Generalist computer science students, mostly fourth-year honours students, plus a few professors.
- **Length:** slides 1 to 25 come to about 2,580 words, which is about 17 minutes at 150 words a minute. To get nearer 15, shorten the four system slides (11 to 14) to their first two and last bullets.
- Written to be spoken. Short forms are spelled out. Model, benchmark and conference names are left as they are.

## Slide 1: Title

- Hello everyone, my name is Lewei.
- This year I have been working on document understanding, and in particular on long documents with many pages.

## Slide 2: Table of contents

- I will start with a short introduction to the problem.
- Then I will go through the two papers that make up the thesis: a survey of the field, and an empirical study of where these systems fail.
- I will finish with a conclusion, and if there is time, a small proof of concept that puts the findings to work.

## Slide 3: Multi-page visually rich documents

- A document is more than its text.
- Its pages carry tables, charts, figures, photographs and handwriting, and the way these are laid out on the page also carries meaning.
- That mix is what we mean by visually rich.
- Multi-page adds one more layer. Meaning also runs between pages, for example when a sentence points to a figure many pages away.
- The research paper is born digital, so its text can be read straight from the file.
- The signed form is a scan with handwriting, so there is no text to read until something recognises it.

## Slide 4: What is document understanding?

- One broad definition is that a system can answer a question about the document accurately.
- To do that it first has to work out what is on each page. On the left, every coloured box is one element: a title, a paragraph, a chart, a table, a caption.
- Then it has to work out how the whole document is organised: which section a figure belongs to, and which caption goes with which table. That is the outline on the right.
- Now take the example question. Does the model that humans rated best in Table 6 also have the best citation recall in Table 3?
- Table 6 is on this page and Table 3 is on the previous one, so neither table answers it alone.

## Slide 5: Large language model assistants

- You have all used systems that do this.
- Here I gave Claude my thesis, which is almost one hundred pages, and asked it a difficult question.
- On the left you can see what it does. It plans, works out which pages it needs, and then reads them.
- On the right is the interesting part. It renders those pages and reads them as images, the way we would look at them.

## Slide 6: Real-world constraints

- But many real settings cannot use that product.
- Think of a hospital, a mining company or a law firm, with tens of thousands of documents to classify, summarise or extract from.
- Calling a commercial service fails for three reasons. The documents are private and cannot leave. The cost per call adds up at that volume. And their documents are unusual types the general model was not built for.
- So they run an open-weight model locally, and that means a fixed compute budget. Which pages we read, at what resolution, and how many times, all have to fit inside it.
- So the question behind this thesis is how to do document understanding under a fixed compute budget.

## Slide 7: Table of contents, survey

- The first part is the survey, which has been accepted at the EMNLP 2026 main conference.

## Slide 8: Survey, research gap and contributions

- The gap is simple to state.
- Systems for multi-page documents were built along parallel lines. Each line used its own terminology, and there was little comparison between them.
- Our survey does three things.
- It defines the problem as evidence management: deciding which evidence to select and reason over when the document cannot all be held at once.
- It gives a taxonomy with four architectural families.
- And it brings together the datasets and the open challenges.

## Slide 9: Multi-page architectural overview

- These are the four families, and they appeared roughly in this order.
- Page-to-document encoding models came first, from late 2023. They encode each page separately and then combine the pages inside one model.
- Then the field moved to large pretrained multimodal language models. The second family adapts such a model so that many pages fit inside its context.
- The third family is retrieval-augmented pipelines. They retrieve the relevant pages first, and only those pages go to the model.
- The fourth family, from 2025, is adaptive-trajectory pipelines. Here the model works in a loop. It decides what to look at next, and when it has seen enough to answer.
- Each family also has a typical weakness, shown in red at the bottom. I will come back to those with one example of each.

## Slide 10: Surveyed systems at a glance

- This is the main table of the survey. Every system we cover is here, grouped by family.
- I have framed five things worth noticing.
- One, the backbone. In the adaptive-trajectory family it is a general-purpose multimodal language model, typically used as it is, with no extra training or fine-tuning.
- Two, the modalities. The encoding models combine text, vision and layout. The models in the second family mostly use vision only.
- Three, search. It only appears once retrieval is separated from answering. Retrieval-augmented pipelines add a single retrieval step.
- Four, in the adaptive-trajectory family search becomes richer: iterative retrieval, query reformulation and navigation.
- Five, reasoning techniques such as reason-and-act loops and multiple agents are concentrated in that last family.
- Now one representative system from each family.

## Slide 11: Page-to-document encoding, Hi-VT5

- Hi-VT5 was introduced in 2023 together with the first multi-page benchmark, Multi-Page DocVQA. That benchmark has about forty-six thousand questions over six thousand scanned documents of up to twenty pages.
- The model is built on T5, which is a text encoder and decoder.
- Each page goes through the encoder separately. The encoder receives the question, the recognised words on that page with their positions, and patches of the page image.
- It also receives ten learnable page tokens. Their job is to summarise whatever on that page matters for the question.
- The decoder never sees the full pages. It only reads the page tokens from all the pages, joined together, and writes the answer.
- The weakness is compression. A whole page is squeezed into ten tokens, so fine detail is lost, and memory still grows with every page added.

## Slide 12: Adaptation of multimodal language models, Docopilot

- Docopilot takes the opposite approach to retrieval. The whole document goes into the model's context and the model reads it directly.
- Their real contribution is data. Existing models were trained on single images, so they built a dataset called Doc-750K.
- It has about seven hundred and fifty thousand question and answer pairs and over three million page images, taken from papers on Sci-Hub and arXiv and from reviews on OpenReview. That is the pipeline in the figure.
- They then fine-tune an existing model, InternVL2, on this data, in two sizes of two billion and eight billion parameters.
- The weakness is the context window. A document that does not fit cannot be read at all, and accuracy already falls well before that limit.

## Slide 13: Retrieval-augmented pipelines, MoLoRAG

- MoLoRAG is a retrieval method. Its starting point is that ordinary retrieval only finds pages that look similar to the question.
- But some pages are needed for the answer without looking similar at all. The authors call this logical relevance.
- First, every page is embedded with a visual retriever called ColPali. Two pages are linked whenever their embeddings are similar enough, which gives a graph of pages.
- For a question, the search starts from the few most similar pages.
- A small vision-language model then looks at each of those pages and scores how logically relevant it is to the question. That score is combined with the similarity score.
- The search then moves out to the neighbours of the best pages, and repeats for a fixed number of steps.
- At the end, all visited pages are ranked again and the top few go to a frozen model that writes the answer.
- The weakness is shared by the whole family. A page the search never reaches cannot be recovered later.

## Slide 14: Adaptive-trajectory pipelines, DocLens

- DocLens is built from four agents arranged in two modules, and it relies on document parsing tools.
- The first module is the lens. Its page navigator runs optical character recognition on every page, then shows a model the question together with the page images and their text, and asks which pages hold the evidence.
- It asks several times and keeps every page that was named, which gives ninety-seven percent recall of the evidence pages.
- Then the element localiser runs layout detection on those pages and crops out each figure, chart and table, so the model can look at them closely.
- The second module does the reasoning. An answer sampler writes several answers, each with its reasoning.
- Then an adjudicator compares those lines of reasoning and chooses the most consistent one.
- Paired with Gemini 2.5 Pro, it scores 67.6 percent on MMLongBench-Doc, the first system above human experts on that benchmark.
- The weakness is cost. It makes many calls to a large model for every question, which is hard to bound and does not suit the local setting.

## Slide 15: Table of contents, empirical study

- The second part is the empirical study, which is under review at EACL.

## Slide 16: Empirical study, research gaps and contributions

- The survey leaves two gaps open.
- First, papers make competing claims about design, each tested on a different pipeline and dataset. Some say vision alone is enough, others want text as well. Some say retrieve more pages, others fewer.
- Second, nobody had studied empirically, from one end of the pipeline to the other, where document understanding systems actually fail.
- Our study makes three contributions.
- A unified view of failure, with three places it can happen that do not depend on the architecture.
- Controlled experiments in a single pipeline, repeated across two document collections and two independently developed model families.
- And practical guidance for building and deploying these systems under a compute budget, which is exactly the local setting I described earlier.

## Slide 17: Attribution framework

- This is the framework. There are three places where an answer can go wrong.
- Representation is how the document is converted into what the model reads. Was the information preserved?
- Selection is which pages are put in front of the model. Did the information actually reach it?
- Reasoning is what the model does with those pages. Did it use them correctly?
- Each one has two mechanisms, which gives six in total. I will show results for each pair, and then a real example of each.

## Slide 18: Attribution by construction

- To separate the three, we use one deliberately simple pipeline with three stages: encode the pages, retrieve some of them, and answer in a single pass.
- Each experiment changes one stage and holds the other two fixed.
- We can also hand the model the annotated gold pages directly, which takes retrieval out of the picture.
- The main benchmark is MMLongBench-Doc, with one hundred and thirty-five long documents. It is the only one we know of that marks, for every question, the evidence pages, the type of evidence, and whether the question can be answered at all.

## Slide 19: Representation, results

- First, representation.
- The table on the left compares four inputs: embedded text, parsed text, parsed text with page images, and images alone.
- With text only, the model refuses chart and figure questions far more often, because the information is simply not there. Adding page images brings refusal under ten percent for every type of evidence.
- But images alone are not the best either: 42.6 percent, against 49.5 percent for text and images together. Dense text and exact numbers are hard to read from an image.
- On the right is conversion quality. With text alone, the choice of parser changes accuracy by 15.7 points on digital documents. Add the page image and that shrinks to 4.2.

## Slide 20: Representation, design and deployment

- Here are two real examples.
- On the left, the question asks for the colours of two icons. With text only the model says the document does not specify the colours. Colour exists only in pixels. Add the image and it answers grey and red.
- On the right, a scanned slide. One parser misreads the company name, another finds nothing. A better parser, or simply adding the image, fixes it.
- For design, this means text and vision are complementary. Start from reliable embedded text, add the image when the question is about appearance or the text looks wrong, and parse again when the text is not good enough.
- For deployment, images are expensive. Preparing the input takes about twenty-six seconds per question with images, against under two seconds for text. So the choice of modality and the number of pages have to be set together.

## Slide 21: Selection, results

- Next, selection.
- On the left we take questions that need several pages and remove just one of them. Accuracy falls from 38.6 percent to 18.4 percent, so about half.
- It makes almost no difference whether we remove the page the retriever ranked highest or lowest. So the ranking does not tell us which page is safe to lose.
- On the right we do the opposite. We keep every gold page and add extra pages that look relevant but are not needed.
- For questions that need several pages, three extra pages are enough to drop accuracy from 43.9 percent to 35.1 percent.

## Slide 22: Selection, design and deployment

- Two examples again.
- On the left, a question asks how many authors come from Columbia University. The list runs over two pages. Given one page the model says two, given the other it says one. Only with both pages does it say three.
- On the right, the question is how many bar graphs are in the document. With a few extra pages the model counts twelve or thirteen instead of ten.
- For design, select evidence as a set, not page by page. Retrieve broadly, then filter or rerank what reaches the model.
- For deployment, a strong visual retriever raises recall at five pages from 58 percent to 81 percent, but it needs a graphics card and far more time per question. So judge retrieval by the final answers and the total time.

## Slide 23: Reasoning, results

- Finally, reasoning. Here the model is given exactly the right pages.
- On the left we change the size of the model, from two billion to thirty-two billion parameters.
- Accuracy on questions that need several pieces of evidence rises from 29 percent to almost 50 percent.
- But questions that need one piece improve just as much, so the gap between the two stays. A bigger model is better at everything. It does not make combining evidence easier.
- On the right we tell the model it may answer "not answerable".
- It then correctly refuses far more questions that have no answer, from 45.5 percent to 74.6 percent.
- But it also starts refusing questions that do have an answer. That goes from 6.2 percent to 27.7 percent.

## Slide 24: Reasoning, design and deployment

- The examples.
- On the left, a question joins a diagram with a table. The smallest model reads the wrong table. The next reads the right table but the wrong row. The next reads the right numbers and then divides when it should subtract. Only the largest model gets it right.
- On the right, the answer needs two numbers from two tables. Told that it may refuse, the model says not answerable. Told to reason first, it finds both numbers and subtracts them.
- For design, match the size of the model and the way it reasons to what the task needs, and have it reason before it refuses.
- For deployment, storing the model at lower precision keeps accuracy and saves memory, but it is not faster. If memory is the limit, prefer a larger model at lower precision. If time is the limit, prefer a faster model.

## Slide 25: Conclusion

- To conclude.
- The survey organises the field. Understanding multi-page documents is a problem of evidence management, and four families of architecture handle it in different ways.
- The empirical study locates the failures. They sit at representation, at selection, or at reasoning, and each one needs a different fix.
- Thank you. I am happy to take questions.

---

# After the conclusion: proof of concept

Not part of the fifteen minutes. Use if there is time, or if a question asks for it. About 230 words.

## Slide 26: Table of contents, proof of concept

- If there is time, I can show a small proof of concept that puts the findings into one system.

## Slide 27: From findings to a simple method

- It is one model playing three roles.
- The reader goes through the pages in ranked order. For each page it sees both the text and the image, writes down any evidence it finds, and flags pages that may hold the answer.
- The synthesizer answers from the flagged pages in full and the short records of everything else.
- The arbiter cannot write an answer. It either accepts, or names a missing fact and sends the reader back for more pages.
- Each choice follows from a finding. Text and image together, for representation. Read broadly but pass on short records, for selection. And a separate step that judges whether the evidence is enough, for reasoning.

## Slide 28: Simple method results

- All systems in this table use the same model with eight billion parameters.
- Ours reaches 56.5 percent on MMLongBench-Doc and 61.3 percent on LongDocURL, the highest in the table, without any training and with the model stored at four-bit precision.
- It is still behind the trained system DocTrace on questions that need several pages, 39.2 against 41.1.
- The cost is time: about eleven minutes per question on average, in about eight gigabytes of memory.

---

# Appendix slides (29 to 44)

For questions only. No script.

- 29 to 34, survey: inference-time and training strategies, retrieval and navigation, reasoning strategies, agentic methods, training strategies, datasets.
- 35, datasets and evaluation for the empirical study, including the judge.
- 36 to 41, the six quantitative findings one at a time, at full size.
- 42, the deployment table: accuracy and cost of each representation, retriever and reasoner.
- 43, 44, the method: how each finding maps to a design choice, and the inference cost.
