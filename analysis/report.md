# MOTIVATION
Identify measurements and values mentioned in patent descriptions to support complex questions. For example, given the sentence “The resulting BaCO3 had a crystallite size of between about 20 and 40 nm“, extract and store the information that crystallite size’ of ‘BaCO3’ was measured in the unit ‘nm’, and the value was between 20 and 40. Support for questions such as “give me all glass transition temperatures of polymers”

# CHALLENGES
Entity Recognition (+ disambiguation, + linking): chemical substances (e.g. BaCO3) , numerical values (e.g. 20, 40), measurements (e.g. nm)
Relation Extraction: e.g. crystallite_size(BaCO3,20-40nm)
Conceptualization / Abstraction: e.g. glass transition temperatures, polymers.
QA Corpora:
Creation: https://www.aclweb.org/anthology/2020.acl-main.84/

# APPROACHES

## APPROACH 1: Question Answering over KG (KGQA)
KGQA systems answer natural language queries posed over the KG. It requires reasoning over multiple edges of the KG to arrive at the right answer. Recent research on KGQA has proposed to reduce KG sparsity by performing missing link prediction based on embedding methods.
pros:
high response precision
natural language question
cons:
low response recall
It requires a large amount of labelled data.
response in formal language (e.g. sparql)
References:
Saxena, Apoorv, Aditay Tripathi and P. Talukdar. “Improving Multi-hop Question Answering over Knowledge Graphs using Knowledge Base Embeddings.” ACL (2020).

## APPROACH 2: Extractive Question-Answering (EQA)
The common goal of EQA is to find the span boundaries – the start and the end of the span from text evidence, which answers a given question.
pros:
natural language question and answer
cons:
it requires a verbalization of the KG content
References:
Chaybouti, Sofian, Achraf Saghe and A. Shabou. “EfficientQA : a RoBERTa Based Phrase-Indexed Question-Answering System.” ArXiv abs/2101.02157 (2021)
Fajcik, Martin, Josef Jon, Santosh Kesiraju and P. Smrz. “Rethinking the objectives of extractive question answering.” ArXiv abs/2008.12804 (2020)
Lewis, Patrick, Barlas Oğuz, Ruty Rinott, S. Riedel and Holger Schwenk. “MLQA: Evaluating Cross-lingual Extractive Question Answering.” ArXiv abs/1910.07475 (2020)

## APPROACH 3: Sentence Encoding
It uses a pre-trained sentence-BERT (SBERT) based model for sentence encoding. The model classifies similar natural-language patterns using a clustering algorithm. The patterns are used to extract relations between pairs of named entities in a given text corpus.
pros:
Unsupervised approach. It does not require labelled data.


References:
Elsahar, H., Demidova, E., Gottschalk, S., Gravier, C., Laforest, F.: Unsuper- vised open relation extraction. In: European Semantic Web Conference. pp. 12–16. Springer (2017)

EVALUATION:
precision, recall, f-measure (macro,micro)
