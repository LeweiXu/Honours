# Honours thesis seminar script

- **Duration:** 15 minutes, plus 5 minutes of questions.
- **Audience:** Generalist computer science students, mostly fourth-year honours students, plus a few professors.
- **Length:** slides 1 to 25 come to about 2,580 words, which is about 17 minutes at 150 words a minute. To get nearer 15, shorten the four system slides (11 to 14) to their first two and last bullets.
- Written to be spoken. Short forms are spelled out. Model, benchmark and conference names are left as they are.

## Slide 1: Title

- Hello everyone, my name is Lewei, and my thesis looks at long document understanding.

## Slide 2: Table of contents

- First, I’ll briefly introduce the problem and some background.
- Then I’ll cover the two papers that make up my thesis.
- The first is a survey of the field, and the second is an empirical study of where these systems fail and how we can improve them.

## Slide 3: Multi-page visually rich documents

- So, what is a visually rich document?
- Documents carry meaning not just through text, but also through visual information, such as charts, figures and handwriting, as you can see in these examples.
- Layout also matters: how information is arranged in the two-dimensional space of a page carries meaning too.
- That combination of text, visual information and layout is what we mean by visually rich.
- Multi-page documents add another layer of complexity, because meaning can run across pages.
- For example, a sentence might refer to a figure several pages away.

## Slide 4: What is document understanding?

- So, what is document understanding?
- It includes tasks such as information extraction and recovering a document’s structure. But for this talk, we’ll focus on answering natural-language questions about a document.
- To answer a question, a system needs to identify the relevant content and connect the evidence, either within one page or across multiple pages.
- For example, the question here compares two tables on different pages, so neither table alone is enough.

## Slide 5: Large language model assistants

- You may already have used this kind of document question answering yourselves: you upload a document to a language model assistant and ask it questions.
- Here, I gave Claude my thesis, which is almost one hundred pages, and asked it a particularly difficult question. It still did quite well.
- What I want to highlight is how it approaches the question. It uses an agentic workflow: it plans, locates the relevant pages, and inspects them before answering.
- You can also see it rendering those pages as images, so it reads the document visually as well as through text.
- This is a familiar example of document-understanding research reaching consumer-facing products. But it is only one part of how document understanding is used in practice.

## Slide 6: Real-world constraints

- In real-world and industrial settings, the task might be to classify, summarise or extract information from thousands, or even millions, of documents.
- These could be sensitive medical, financial, legal or operational records. Privacy or data-residency requirements may prevent organisations from sending them to third-party services.
- At that volume, commercial API costs can also become prohibitive. And specialised document types may require adapting the model to the task.
- Organisations may therefore need to run open-weight models locally, under fixed memory and compute budgets.
- In that setting, we care about both accuracy and efficiency: which pages to read, at what resolution, and how many times.
- That motivates the central question of my thesis: how can we improve document understanding under a fixed compute budget?

## Slide 7: Table of contents, survey

- So, moving on to the first part: our survey, which has been accepted at the EMNLP main conference.

## Slide 8: Survey, research gap and contributions

- A lot of multi-page document-understanding systems developed along parallel lines, with different terminology and little comparison between them.
- Our survey brings them together through the idea of evidence management: how these systems manage relevant evidence across a very long document.
- We organise these systems into four architectural families, which I’ll go through next.

## Slide 9: Multi-page architectural overview

- In the survey, we identified four architectural families. They emerged roughly in this order, although their development overlaps.

- First are page-to-document encoding models. Each page is encoded separately, combining its text, visual information and layout into a page representation.
- A cross-page mechanism, such as cross-page attention, connects these representations. A decoder then uses that information to generate an answer to the question. These systems are generally trained end to end.
- The problem is that cost grows with the number of pages, and compressing pages into small representations can lose fine detail.

- The second family takes a different approach: it adapts a pretrained large vision-language model to accept a multi-page document directly.
- The document goes through preprocessing, and all its pages are fed into the model’s context, rather than first retrieving a subset. This preprocessing can include compressing the visual tokens to make them fit.
- These systems build on the pretrained model’s capabilities, with further training on document data, either fine-tuning the model or training smaller adaptation modules.
- But longer documents are still difficult: the input is limited by the context window, and performance can fall even before that window is full.

- This motivates the third family, retrieval-augmented pipelines. We first retrieve evidence relevant to the question, then give that selected evidence to a model to answer.
- Retrieval can involve several stages, including reranking or multiple components described as agents. The important point is that the workflow is fixed in advance.
- This lets us handle documents that would not fit into the model all at once. But because the reasoner sees only selected evidence, anything missed by retrieval cannot be recovered during answering.

- That motivates the final family, adaptive-trajectory pipelines. Here, a language model controls the process, deciding what to inspect next based on what it has already found.
- It can retrieve more evidence or inspect another page before answering, rather than following a fixed sequence.
- The trade-off is that this trajectory can take many steps. Without explicit limits, the cost is hard to bound, and answering can become expensive and slow.

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

- Hi-VT5 is an example of page-to-document encoding. It builds on T5, a text encoder-decoder, and adds visual and layout information.
- Each page is encoded separately, together with the question, the recognised words and their positions, and patches of the page image.
- Ten learnable page tokens summarise the information on that page relevant to the question.
- Those tokens from all the pages are joined together and passed to the decoder to generate the answer. So the decoder reads the page summaries, rather than the full pages.

<!-- Reference, not spoken: https://arxiv.org/pdf/2212.05935 -->

## Slide 12: Adaptation of multimodal language models, Docopilot

- Docopilot is an example of adapting a pretrained multimodal model to read a multi-page document directly, without retrieval.
- The main idea is to teach it document-level dependencies through better training data. The authors build Doc-750K, with about 750,000 question-answer pairs from scientific papers and reviews.
- They fine-tune InternVL2 on a data mixture that includes this dataset. At inference time, page images and the question go into the model together, and it generates the answer directly.

<!-- Reference, not spoken: https://arxiv.org/html/2507.14675v1 -->

## Slide 13: Retrieval-augmented pipelines, MoLoRAG

- MoLoRAG is an example of a retrieval-augmented pipeline. There are three main parts.
- First, it builds a graph-based index: a visual retriever represents each page, and pages are connected based on their similarity.
- Second, it searches that graph, starting from pages similar to the question. A small vision-language model helps score their relevance, and the search selects the top K pages.
- Third, those top K pages are passed to a separate vision-language model, the reasoner, to answer the question.

<!-- Reference, not spoken: https://aclanthology.org/2025.emnlp-main.708/ -->

## Slide 14: Tool-augmented multi-agent pipelines, DocLens

- Finally, DocLens is a tool-augmented multi-agent framework from researchers at Google and Peking University.
- It has two main modules. The lens module first finds the evidence: a page navigator uses page images and OCR text to identify relevant pages, and an element localiser crops figures, charts and tables on those pages for closer inspection.
- The reasoning module then samples several candidate answers from that evidence. An adjudicator compares their reasoning and synthesises the final answer.
- So the main idea is to find the pages, zoom in on their elements, and compare candidate answers.


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
