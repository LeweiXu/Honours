# Honours thesis seminar script

- **Duration:** 15 minutes, plus 5 minutes of questions.
- **Audience:** Generalist computer science students, mostly fourth-year honours students, plus a few professors.
- **Length:** slides 1 to 18 come to about 2,126 words, or 14.2 minutes at 150 words a minute, before pauses and slide changes.
- Written to be spoken. Short forms are spelled out. Model, benchmark and conference names are left as they are.

## Slide 1: Title

- Hello everyone, my name is Lewei, and I’ve been working on document understanding for my honours project this year.

## Slide 2: Table of contents

- First, I’ll go through some background.
- Then I’ll cover the main contributions and findings of the two papers we completed this year.
- The first is a survey of document understanding. The second is an empirical study of how document understanding systems can fail and how we can address those failures.

## Slide 3: Multi-page visually rich documents

- First, what do we mean by a visually rich document?
- Documents can carry meaning through text, visual elements like charts and figures, and how they are laid out on a page.
- Here we have an academic paper, scanned forms and technical manuals. Each combines multiple sources of information in different ways.
- A multi-page document simply has two or more pages. Its meaning can also connect across those pages.
- For example, a paragraph in an academic paper might refer to a figure several pages away.
- To understand that reference, we need to connect the paragraph to the figure when we process the document.
- This brings us to document understanding over long documents.

## Slide 4: What is long document understanding?

- So, what is long document understanding?
- It includes tasks like information extraction and structure-aware parsing, among many others.
- But for this seminar, you can think of it as answering a natural-language question about a long, multi-page document.
- This is difficult for two main reasons.
- First, there is the sheer volume of information. We might be dealing with hundreds of pages, or even a whole collection of documents.
- Reading everything in full is expensive, and the input may not even fit in a single context window.
- Even when everything fits, current long-context language models can still struggle to use all that information to answer accurately.
- Second, the evidence required to answer a question can be sparse, scattered across several pages or across different documents in a collection.
- The system has to locate the right pieces of evidence and then connect them to answer the question.
- With that in mind, let’s move on to our survey of the different approaches to document understanding.

## Slide 5: Table of contents, survey

- This is our survey of the field, which we completed during the first semester.
- The paper has been accepted at the EMNLP main conference this year, a top-tier conference in natural language processing.

## Slide 6: Survey, research gap and contributions

- The main gap we wanted to address was that many different approaches to long document understanding had developed along parallel lines.
- They used different terminology, and there was very little comparison between those approaches.
- We use an evidence-management perspective to organise them: how systems preserve, find and use evidence across a document.
- This gives us a taxonomy of four architectural families.
- I’ll focus on those families today. There are other contributions in the survey, but going through all of them would take too long.

## Slide 7: Multi-page architectural overview

- The first family is page-to-document encoding models, one of the earlier approaches to long document understanding.
- Each page is encoded separately into a compact representation. Those representations are connected through a cross-page mechanism, such as attention, and passed to a decoder to generate the final answer.
- The limitation is that pages can contain very different amounts of information. Giving each page the same fixed representation budget can lose fine-grained detail during encoding.

- The second family adapts a pretrained multimodal large language model to read the document directly within its context window.
- This lets the model read richer page content directly, rather than only the compact summaries used by the first family.
- But performance can drop as documents get longer, and some documents cannot fit at all.
- Even when they fit, evidence scattered throughout a long context can be difficult for the model to locate and connect.

- This motivates retrieval-augmented pipelines. Instead of fitting the whole document into the model, we first retrieve relevant evidence and pass that smaller set to the answering model.
- These approaches follow a fixed workflow. Evidence missed during retrieval cannot be recovered during the answering stage.

- Finally, adaptive-trajectory pipelines follow an agentic approach. The language model decides what evidence to collect, how to collect it, and when it has enough to answer.
- It can gather more evidence based on what it has already found, but repeated calls make the time and cost harder to bound.
- We can see this kind of behaviour in language model assistants too.

## Slide 8: From research to products, language model assistants

- We can see these approaches in language model assistants, where you upload a document and ask questions about it.
- Putting all the text and page images directly into the model’s context resembles the second family, but long documents can run into context limits.
- Alternatively, an assistant can access the uploaded document through tools, retrieving or inspecting parts of it as needed.
- This resembles retrieval-augmented and adaptive-trajectory pipelines, which gather evidence before answering and can return for more when needed.
- Here, I gave Claude my thesis, which is almost one hundred pages, and asked a difficult question.
- You can see it plan, locate relevant pages and render them as images, so it reads the evidence visually as well as through text.

## Slide 9: Surveyed systems at a glance

- This is the main table of the survey, with the systems grouped by architectural family.
- There are two things I want to point out.
- First, we call the first two families models. Generally, they are trained end to end, with components built for that architecture.
- The last two families are pipelines. Their components are often interchangeable, especially the backbone language model.
- These techniques can often be applied to different backbones. As language models become stronger, the pipelines can benefit from those improvements too.
- Second, the modalities. Some systems use vision only, reading the document through page images.
- Others combine those images with text and layout information. The text may be embedded in the document or extracted by a parser.
- Layout information can describe where the text appears, using bounding boxes or coordinates on the page.
- So these systems differ in whether they read images alone or combine text, layout and vision. This distinction will be important in the empirical study.
- That brings us to the second paper.

## Slide 10: Table of contents, empirical study

- This brings us to our second paper, an empirical attribution study, which is currently under review.

## Slide 11: Real-world constraints

- As we saw earlier, language model assistants are just one application of document understanding.
- In industry, you might have one or a few specific tasks to perform over thousands or millions of documents.
- For example, extracting fields from scanned patient records in healthcare, or classifying and summarising technical and safety reports in mining and resources.
- One major concern is privacy. Data-residency or privacy requirements may prevent you from sending the documents to a third-party service.
- Another is cost. Even without privacy concerns, processing that volume through a commercial API can be very expensive.
- Uploading documents one by one to an assistant is not feasible at this scale. You may also need structured output that another system can process automatically.
- If third-party processing is permitted, you might use a model through an API. Otherwise, you may need to run a vision-language model locally.
- Either way, you still need to implement and deploy a document understanding system tailored to your task, documents and output requirements.
- Access to a model through an API does not necessarily give you the document-processing workflow behind the provider’s consumer assistant.
- You have to choose how to convert the documents, retrieve evidence, and use that evidence to get the best performance for your task.
- For specialist document types, you might also need additional training. All these choices have to fit within a fixed compute budget.
- These are the design and deployment choices that motivate our empirical study.

## Slide 12: Empirical study, research gaps and contributions

- There are two research gaps behind this study.
- First, papers make competing design claims, but test them on different pipelines and datasets. Some favour vision alone, others text and vision; some retrieve more pages, others fewer.
- Second, we wanted an end-to-end empirical account of where failures occur across a document understanding pipeline.
- Our first contribution is a unified view of failure, with three places an answer can go wrong, regardless of the architecture.
- Second, we run controlled interventions in a single pipeline, changing one stage at a time.
- We repeat experiments across different document collections and independently developed model families to check whether the findings transfer beyond one setting.
- Third, we use these results to give concrete guidance for designing and deploying systems under a compute budget.

## Slide 13: Attribution framework

- This is the framework. There are three places where an answer can go wrong.
- Representation is how the document is converted into what the model reads. Was the information preserved?
- Selection is which pages are put in front of the model. Did the information actually reach it?
- Reasoning is what the model does with those pages. Did it use them correctly?
- Each one has two mechanisms, which gives six in total. I will show results for each pair, and then a real example of each.

## Slide 14: Attribution by construction

- To separate the three, we use one deliberately simple pipeline with three stages: encode the pages, retrieve some of them, and answer in a single pass.
- Each experiment changes one stage and holds the other two fixed.
- We can also hand the model the annotated gold pages directly, which takes retrieval out of the picture.
- The main benchmark is MMLongBench-Doc, with one hundred and thirty-five long documents. It is the only one we know of that marks, for every question, the evidence pages, the type of evidence, and whether the question can be answered at all.
- We ran a lot of experiments this way. In the next three slides I will only discuss some of the more interesting and important points.

## Slide 15: Representation: when is visual reading worth its cost?

- The first point is about representation, and the question is when visual reading is worth its cost.
- Vision is expensive. Reading from images alone needs high resolution to work well, and every page image costs time. In our measurements, preparing the input took about twenty-six seconds per question with images, against under two seconds with text.
- Text, on the other hand, works like a cache. The text embedded in the file, or the output of a structure-aware parser, converts the document once into a form that is fast to use at inference time.
- On born-digital documents, text alone is already close: in the lower half of the table, adding images to parsed text gives under three points.
- So how much of each you need depends heavily on the document type and the task. In the upper half, chart and figure questions are refused far more often from text, and gain more than twenty points from images, while text and table questions gain little. There is no one size fits all.
- And parsers are improving. Newer neural parsers can express visual content directly as text, for example turning a chart into a table of its values. Our results do not show this yet, so I see it as a direction.
- So choose the representation for the document type and the task.

## Slide 16: Selection: how much evidence is enough?

- The second point is about selection.
- Retrieved evidence can look sufficient. The model produces an answer either way, and it is hard to know whether more context from the document would have changed it.
- Underneath that is a precision and recall trade-off.
- If we retrieve too little, required evidence is simply missing. In our experiments, removing one required page halves accuracy.
- If we retrieve too much, the reasoner struggles to find and combine the evidence. In the figure, every required page is present, and accuracy still falls as we add more pages, most sharply for multi-hop questions.
- And there is no clear stopping signal. It is hard to retrieve only what is relevant, and hard to know when you have enough.
- We need enough evidence to establish the answer, not just enough to generate one.

## Slide 17: Reasoning: does the document support the question?

- The third point is about reasoning.
- A question can contain a premise the document does not support. Here the question asks which YouTube video the slides use, and the document mentions no video at all. With no instruction, the model answers fluently that it is a clip from Breaking Bad.
- Prompts change this behaviour. If we explicitly allow the model to say not answerable, it correctly refuses far more unanswerable questions, from 45.5 percent to 74.6 percent.
- But it also refuses more answerable ones, from 6.2 percent to 27.7 percent. So refining the prompt means balancing unsupported answers against unnecessary refusals.
- There are further options, such as Reflexion and self-consistency, which spend more computation on reasoning.
- Before asking whether the answer is correct, ask whether the evidence supports giving that answer.

## Slide 18: Conclusion

- To conclude.
- The survey organises the field. Understanding multi-page documents is a problem of evidence management, and four families of architecture handle it in different ways.
- The empirical study locates the failures. They sit at representation, at selection, or at reasoning, and each one needs a different fix.
- Thank you. I am happy to take questions.

---

# After the conclusion: proof of concept

Not part of the fifteen minutes. Use if there is time, or if a question asks for it. About 230 words.

## Slide 19: Table of contents, proof of concept

- If there is time, I can show a small proof of concept that puts the findings into one system.

## Slide 20: From findings to a simple method

- It is one model playing three roles.
- The reader goes through the pages in ranked order. For each page it sees both the text and the image, writes down any evidence it finds, and flags pages that may hold the answer.
- The synthesizer answers from the flagged pages in full and the short records of everything else.
- The arbiter cannot write an answer. It either accepts, or names a missing fact and sends the reader back for more pages.
- Each choice follows from a finding. Text and image together, for representation. Read broadly but pass on short records, for selection. And a separate step that judges whether the evidence is enough, for reasoning.

## Slide 21: Simple method results

- All systems in this table use the same model with eight billion parameters.
- Ours reaches 56.5 percent on MMLongBench-Doc and 61.3 percent on LongDocURL, the highest in the table, without any training and with the model stored at four-bit precision.
- It is still behind the trained system DocTrace on questions that need several pages, 39.2 against 41.1.
- The cost is time: about eleven minutes per question on average, in about eight gigabytes of memory.

---

# Appendix slides (22 to 44)

For questions only.

- 22 to 25, one example system per family. Notes for these are below.
- 26 to 31, survey: inference-time and training strategies, retrieval and navigation, reasoning strategies, agentic methods, training strategies, datasets.
- 32, datasets and evaluation for the empirical study, including the judge.
- 33 to 38, the six quantitative findings one at a time, at full size.
- 39 to 41, the qualitative examples for each failure mode, two per slide.
- 42, the deployment table: accuracy and cost of each representation, retriever and reasoner.
- 43, 44, the method: how each finding maps to a design choice, and the inference cost.

## Slide 22: Page-to-document encoding, Hi-VT5

- Hi-VT5 is an example of page-to-document encoding. It builds on T5, a text encoder-decoder, and adds visual and layout information.
- Each page is encoded separately, together with the question, the recognised words and their positions, and patches of the page image.
- Ten learnable page tokens summarise the information on that page relevant to the question.
- Those tokens from all the pages are joined together and passed to the decoder to generate the answer. So the decoder reads the page summaries, rather than the full pages.

<!-- Reference, not spoken: https://arxiv.org/pdf/2212.05935 -->

## Slide 23: Adaptation of multimodal language models, DocSLM

- DocSLM is an example of the second family. It is a small vision-language model, designed to read long documents under limited memory.
- The first idea is compression. A hierarchical compressor jointly encodes the visual, text and layout information of each page into a fixed 576 tokens, however much text the page holds.
- The second idea is streaming. The document is split into segments, which are processed one at a time. Each segment either gives an answer or abstains.
- An uncertainty calibrator then keeps the answer with the lowest uncertainty. That is what the figure shows.

<!-- Reference, not spoken: https://arxiv.org/abs/2511.11313 -->

## Slide 24: Retrieval-augmented pipelines, MoLoRAG

- MoLoRAG is an example of a retrieval-augmented pipeline. There are three main parts.
- First, it builds a graph-based index: a visual retriever represents each page, and pages are connected based on their similarity.
- Second, it searches that graph, starting from pages similar to the question. A small vision-language model helps score their relevance, and the search selects the top K pages.
- Third, those top K pages are passed to a separate vision-language model, the reasoner, to answer the question.

<!-- Reference, not spoken: https://aclanthology.org/2025.emnlp-main.708/ -->

## Slide 25: Adaptive-trajectory pipelines, SimpleDoc

- Finally, SimpleDoc is an example of an adaptive-trajectory pipeline. It has two stages.
- In pre-processing, every page is indexed twice: as a visual embedding, and as a short summary written by a vision-language model.
- To answer a question, pages are first shortlisted by embedding similarity. A language model then re-ranks them using the summaries.
- A single reasoning agent reads those pages together with a working memory of earlier notes. It either answers, or issues a refined query to retrieve more pages.
- So the number of retrieval rounds depends on the question, rather than being fixed in advance.

