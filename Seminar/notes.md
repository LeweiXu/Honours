# Honours thesis seminar script

- **Duration:** 15 minutes, plus 5 minutes of questions.
- **Audience:** Generalist computer science students, mostly fourth-year honours students, plus a few professors.
- **Length:** slides 1 to 18 come to about 1,730 words, which is about 12 minutes at 150 words a minute.
- Written to be spoken. Short forms are spelled out. Model, benchmark and conference names are left as they are.

## Slide 1: Title

- Hello everyone, my name is Lewei, and my thesis looks at long document understanding.

## Slide 2: Table of contents

- First, I’ll briefly introduce the problem and some background.
- Then I’ll cover the two papers that make up my thesis.
- The first is a survey of the field, and the second is an empirical study of where these systems fail and how we can improve them.

## Slide 3: Multi-page visually rich documents

- A visually rich document carries meaning through text, visual elements like charts and figures, and how they are laid out on the page.
- In a multi-page document, meaning also runs across pages.
- For example, a sentence might refer to a figure several pages away.

## Slide 4: What is document understanding?

- Document understanding includes tasks like information extraction and recovering document structure. For this talk, we’ll focus on answering natural-language questions about a document.
- To answer accurately, a system needs to find the relevant evidence and connect it, sometimes across multiple pages. The example here requires information from two different tables.
- With hundreds of pages, or a whole collection of documents, reading everything at full detail becomes expensive and may exceed what the model can process at once.
- The challenge is to find and combine the evidence we need without losing important details or being distracted by irrelevant content.

## Slide 5: Table of contents, survey

- So, moving on to the first part: our survey, which has been accepted at the EMNLP main conference.

## Slide 6: Survey, research gap and contributions

- Multi-page document-understanding systems developed along parallel lines, with different terminology and little comparison between them.
- Our survey organises the field through an evidence-management perspective: how systems preserve, find and use relevant evidence across a long document.
- Through this perspective, we group the systems we surveyed into four architectural families, which I’ll explain next.

## Slide 7: Multi-page architectural overview

- We organise these systems into four architectural families.

- First, page-to-document encoding models encode each page separately, exchange information across pages, and pass the representations to a decoder to answer the question.
- But processing more pages costs more, and compressing each page into a small representation can lose fine detail.

- The second family takes a different approach: it adapts a pretrained multimodal language model to read the document directly and answer within its context.
- But longer documents still cause performance to drop, and some cannot fit in the context window at all.

- To handle documents beyond that limit, retrieval-augmented pipelines first select relevant evidence, then give that smaller set to a model to answer, following a fixed workflow.
- The problem is that evidence missed during retrieval cannot be recovered by the answering stage.

- Adaptive-trajectory pipelines address this by letting a language model decide what to inspect next based on what it has already found, so it can gather more evidence before answering.
- But this can take many model calls, making the time and cost harder to bound.

## Slide 8: From research to products, language model assistants

- This research is applied directly in public-facing products, and you have probably used it: you upload a document to an assistant and ask it questions.
- Even earlier this year, these assistants worked like the second family. The full document text and the page images were fed to the model in one go.
- More recently they have moved to retrieval-augmented and adaptive-trajectory mechanisms.
- Here is an example. I gave Claude my thesis, which is almost one hundred pages, and asked it a difficult question.
- You can see it plan, locate the relevant pages, and then render those pages as images, so it reads them visually as well as through text.

## Slide 9: Surveyed systems at a glance

- This is the main table of the survey. Every system we cover is here, grouped by family.
- I have framed three things worth noticing.
- One, the names. We call the first two families models, because they are trained end to end, using components built specifically for that architecture.
- We call the last two families pipelines, because their components are often interchangeable, especially the backbone. You can see that in the backbone column, where many of them are tested with several different models.
- Two, the modalities. The encoding models combine text, vision and layout. The models in the second family mostly use vision only.
- Three, search. It only appears once retrieval is separated from answering, so only in the two pipeline families.
- Now one representative system from each family.

## Slide 10: Table of contents, empirical study

- The second part is the empirical study, which is under review at EACL.

## Slide 11: Real-world constraints

- The second paper starts from how document understanding is used in industry.
- There you usually have one specific task, such as classifying or extracting information, over thousands or even millions of documents.
- For example, a hospital extracting fields from scanned patient records, a mining company classifying and summarising technical and safety reports, a bank pulling figures out of annual reports, or a law firm finding clauses across contracts.
- Privacy or data-residency requirements can mean that no third-party service is allowed at all.
- Even without those concerns, the cost of a commercial service adds up at that volume.
- But the more important point is this. Either way, you cannot upload documents one by one into an online tool.
- So whether you call a commercial service or run a model locally, you have to build your own document understanding pipeline around a vision-language model, and it has to fit a compute budget.
- That raises the question the paper answers: where do such pipelines fail? We formalise failure into three failure modes.

## Slide 12: Empirical study, research gaps and contributions

- The survey leaves two gaps open.
- First, papers make competing claims about design, each tested on a different pipeline and dataset. Some say vision alone is enough, others want text as well. Some say retrieve more pages, others fewer.
- Second, nobody had studied empirically, from one end of the pipeline to the other, where document understanding systems actually fail.
- Our study makes three contributions.
- A unified view of failure, with three places it can happen that do not depend on the architecture.
- Controlled experiments in a single pipeline, repeated across two document collections and two independently developed model families.
- And practical guidance for building and deploying these systems under a compute budget, which is exactly the local setting I described earlier.

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

## Slide 15: Representation, when is visual reading worth its cost?

- The first point is about representation, and the question is when visual reading is worth its cost.
- Vision is expensive. Reading from images alone needs high resolution to work well, and every page image costs time. In our measurements, preparing the input took about twenty-six seconds per question with images, against under two seconds with text.
- Text, on the other hand, works like a cache. The text embedded in the file, or the output of a structure-aware parser, converts the document once into a form that is fast to use at inference time.
- How much of each you need depends heavily on the document type and the task. You can see that in the figure: the lines for different document domains behave very differently as we move from text to images. There is no one size fits all.
- And parsers are improving. Newer neural parsers can express visual content directly as text, for example turning a chart into a table. In our own runs the parser left charts as image placeholders, so this is a direction, not something our results show yet.
- So choose the representation for the document type and the task.

## Slide 16: Selection, how much evidence is enough?

- The second point is about selection.
- Retrieved evidence can look sufficient. The model produces an answer either way, and it is hard to know whether more context from the document would have changed it.
- Underneath that is a precision and recall trade-off. On the left, as we retrieve more pages, recall rises from 54 percent to 87 percent, but precision falls from 70 percent to 15 percent.
- If we retrieve too little, required evidence is simply missing. In our experiments, removing one required page halves accuracy.
- If we retrieve too much, the reasoner struggles to find and combine the evidence. On the right, every required page is present, and accuracy still falls as we add more pages.
- And there is no clear stopping signal. It is hard to retrieve only what is relevant, and hard to know when you have enough.
- We need enough evidence to establish the answer, not just enough to generate one.

## Slide 17: Reasoning, does the document support the question in the first place?

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

