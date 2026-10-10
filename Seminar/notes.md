# Honours thesis seminar script

- **Duration:** 15 minutes, plus 5 minutes of questions.
- **Audience:** Generalist computer science students, mostly fourth-year honours students, plus a few professors.
- **Length:** the main script (slides 1–18, skipping slide 14) is about 2,177 words, or 14.5 minutes at 150 words a minute, before pauses and slide changes.
- Written to be spoken. Short forms are spelled out. Model, benchmark and conference names are left as they are.

## Slide 1: Title

- Hello everyone, my name is Lewei, and I’ve been working on document understanding for my honours project this year.

## Slide 2: Table of contents

- First, I’ll go through some background.
- Then I’ll cover the main contributions and findings of the two papers we completed this year.
- The first is a survey of document understanding.
- The second is an empirical study of where document understanding systems fail. We use those findings to derive practical recommendations for designing and deploying these systems.
- If we have time, I’ll also show a very simple method that uses the empirical findings to build a working document understanding system.

## Slide 3: Multi-page visually rich documents

- First, what do we mean by a visually rich document?
- Documents carry meaning through text, visual elements like charts and figures, and how they are laid out on a page.
- Here we have some examples: an academic paper, scanned forms and technical manuals. Each combines multiple sources of information in different ways.
- A multi-page document simply has two or more pages, but its meaning can be spread across those pages and connected between them.
- For example, a paragraph in this academic paper might refer to a figure several pages away.
- To understand that reference, we need to connect the paragraph to the figure when we process the document.
- This brings us to document understanding over long documents.

## Slide 4: What is long document understanding?

- So, what is long document understanding?
- Document understanding itself includes tasks like information extraction and structure-aware parsing.
- But for this seminar, you can think of it as answering a natural-language question about a long, multi-page document.
- This is difficult for two main reasons.
- First, the sheer volume of information involved. We might be dealing with documents hundreds of pages long, or even a whole collection of documents.
- Reading everything in full is expensive. With a vision-language model as the backbone, the input might not even fit in a single context window.
- Even when everything fits, current long-context models can struggle to use all that information effectively and answer accurately.
- Second, the evidence required to answer a question or perform a task may be scattered across several pages, or across different documents in a collection.
- The system has to locate the right pieces of information and then connect them to answer the question.
- With that in mind, let’s move on to our survey of the different approaches to document understanding.

## Slide 5: Table of contents, survey

- This is our survey of the field, which we completed earlier this year.
- It has been accepted at the EMNLP main conference, a top-tier conference in natural language processing.

## Slide 6: Survey, research gap and contributions

- The main gap we wanted to address was that approaches to long document understanding had developed largely along parallel lines.
- They use different terminology, and individual papers often frame their contributions as addressing limitations of earlier approaches.
- But there is little comparison across these different lines of work.
- We use evidence management as a conceptual framework to organise the field. We ask how systems preserve, find and use evidence across a document.
- This lets us define a taxonomy of four architectural families.
- I’ll focus on those families today, rather than go through every contribution of the survey.

## Slide 7: Multi-page architectural overview

- The first family is page-to-document encoding models, an early approach that extends single-page architectures to the multi-page setting.
- Each page is encoded separately into a compact representation. Those representations are connected through a cross-page mechanism, such as attention, and passed to a decoder to generate the final answer.
- These models are generally trained end to end.
- The limitation is that pages contain different amounts of information. Giving each page a fixed representation budget can lose fine-grained detail during encoding.

- The second family adapts a pretrained multimodal large language model to process the document within its context window, rather than using a separate page-to-document architecture.
- Adaptation can involve continued pretraining on document tasks or fine-tuning, including low-rank adaptation. Some systems also compress the representations to fit longer documents.
- But, as we discussed earlier, performance can still degrade as documents get longer, and some documents cannot fit at all.

- This motivates retrieval-augmented pipelines, or RAG pipelines. Instead of fitting the whole document into the model, we retrieve relevant evidence and pass a smaller evidence set to a vision-language model.
- The answering model is often frozen, meaning it is used without additional training for that pipeline.
- Retrieval can be sophisticated, but the workflow is fixed in advance. Evidence missed during retrieval cannot be recovered by the answering stage.

- Finally, adaptive-trajectory pipelines follow an agentic approach. The language model decides what evidence to collect, how to collect it, and when it has enough to answer.
- It can gather more evidence based on what it has already found, making repeated calls as it works towards an answer.
- But those repeated calls can become expensive, and make the total time and compute cost harder to bound.
- We can see this kind of behaviour in language model assistants too.

## Slide 8: From research to products, language model assistants

- We can see these approaches in the language model assistants we use too. You upload a document and ask questions about it.
- If the assistant puts the text and page images straight into the model’s context, that resembles the second family we just saw.
- But that approach runs into context limits. You may have encountered an upload or length limit when trying to give an assistant a large document.
- We can also see assistants accessing documents through tools, which resembles the retrieval-augmented and adaptive-trajectory approaches.
- Here’s an example from last week. I uploaded my thesis, which is close to a hundred pages, to Claude and asked it a difficult question.
- In this example, it accesses the uploaded file through tool calls and renders specific pages as images to read them visually.
- So it can inspect relevant parts of the document as it goes, rather than relying only on the whole document being supplied in one context.
- In my informal testing, it handled the questions I tried well. That’s an illustration of the workflow, rather than a systematic evaluation.

## Slide 9: Surveyed systems at a glance

- This is the main table of the survey, with the systems and papers we surveyed grouped by architectural family.
- There are two things I want to point out.
- First, we call the first two families models. They are generally trained end to end, with components built for that architecture.
- We call the last two families pipelines because their components are often interchangeable, especially the backbone language model.
- That means the same techniques can often be applied to different backbones. As language models get stronger, these pipelines can benefit from those improvements too.
- Second, the modalities. Some systems use vision only, reading the document through page images.
- Others combine vision with text and layout information. The text may be embedded in the document or extracted by a parser.
- Layout describes where the text appears, for example through bounding boxes or coordinates on the page.
- So the distinction is between reading page images alone and combining text, layout and vision. This will be important in the next part of the seminar.
- That brings us to our second paper.

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

- The literature makes competing design claims. Some approaches favour vision alone, while others combine text and vision, each evaluated in a different setting.
- We also found limited end-to-end empirical analysis of document understanding for these design and deployment decisions.
- Our study provides a unified view of where document understanding systems can fail.
- We run controlled interventions in a single pipeline, with checks across document collections and model families.
- From those results, we derive concrete guidance for designing and deploying systems within a compute budget.

## Slide 13: Attribution framework

- This is our attribution framework, with three places where document understanding can fail.
- First, representation. We convert the document into text, rendered page images, or both, for retrieval and the answering model. Was the information preserved during that conversion?
- Second, selection. We choose which evidence reaches the model, usually whole pages in these pipelines. Did the required information actually reach it?
- Third, reasoning. Once the evidence is present in a usable representation, can the model use it correctly to produce an answer?
- In agentic systems, these operations can repeat as the model inspects more of the document. For our experiments, we use a simple encode, retrieve and answer pipeline.
- We change one stage while holding the other two fixed. Giving the model annotated evidence pages directly lets us bypass retrieval.
- I’ll move straight to the main results, starting with representation.

## Slide 14: Attribution by construction [skip during the main talk]

Presenter note: Skip this slide to save time. The essential experimental setup is now included in the slide 13 notes. Keep this slide available for questions.

- Each experiment changes one stage and holds the other two fixed.
- Annotated gold pages bypass retrieval.
- The main benchmark is MMLongBench-Doc, with 135 documents and annotations for evidence pages, evidence type and answerability.
- Two model families and a second document collection provide checks on transfer.

## Slide 15: Representation: when is visual reading worth its cost?

- The first point is about representation, and the question is when visual reading is worth its cost.
- Vision is expensive. In our measurements the same question takes about nine hundred input tokens whether we feed it as text or as page images, but reading it as images takes twenty-one times longer: about twenty-three seconds per question against one second. It also needs more memory: with images added to parsed text, eleven percent of questions ran out of memory on our cards, against one percent for text.
- And yet most systems read everything visually. They are either vision only, or text plus image, applied to every page of every document.
- What we show empirically is that the best choice depends on the document type and on the task. The top half of the table is scanned documents. There is no text layer, so embedded text answers almost nothing and the model mostly refuses. A parser recovers some of it, and the image is what gets you to fifty or sixty percent.
- The bottom half is born-digital documents. There, text alone is already close, and adding the image gives about three points overall. By task, text and table questions gain little from the image, while figures gain the most.
- The figure on the right is the second finding: the modalities are complementary. Parsed text alone answers thirty-eight percent, a low-resolution image alone also thirty-eight, and together forty-nine. That works because they fail on different questions. Only twenty-two percent are answered by both, and when we give the model both it keeps most of what either one answers alone.
- So each hides the other's weakness. In the top panel, with text present, a low-resolution image is nearly as good as a high-resolution one without it. In the bottom panel, with the image present, the gap between the worst and the best parser shrinks from fourteen points to five.
- Many systems already rely on this effect. What we add is the measurement, and the reason: the two channels lose different things. A parser drops charts and figures, low resolution drops small text and numbers.
- For deployment, this means choose rather than default. If you know the document type or the task, fix the modality: images for scans, cached parser text for reports and tables. For mixed collections, choose per question, which is what tool-using agents are starting to do.
- So there is no one size fits all. Choose modalities for the document and the task, and combine cheap ones before paying for resolution.

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
- A question can contain a premise the document does not support. Here the question asks which YouTube video the slides use, and the document mentions no video at all. With no instruction, the model answers fluently that it is a clip from Breaking Bad. Overall it refuses only forty-five percent of unanswerable questions.
- Prompts move this trade-off, which is the left figure. If we explicitly allow the model to say not answerable, it refuses seventy-five percent of unanswerable questions, but it also refuses twenty-eight percent of answerable ones, up from six.
- Asking it to reason step by step first, and then allowing abstention, wins the accuracy back, to fifty-one percent, and refuses even more of the unanswerable questions, eighty-six percent.
- The right figure is what happens when we spend more computation on reasoning instead. Self-consistency samples forty reasoning paths and takes a majority vote. It adds about eight points on answerable questions, but it costs over ten minutes per question on our hardware. That run is still finishing, so the number is preliminary.
- Reflexion lets the model evaluate its own answer and retry. It adds fourteen points on unanswerable questions and costs under a minute. But its self-check accepts ninety-four percent of its own answers, so the retries rarely fire, and they do not rescue the hard answerable questions.
- So more computation helps, at a price, and neither method replaces checking the evidence.
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

