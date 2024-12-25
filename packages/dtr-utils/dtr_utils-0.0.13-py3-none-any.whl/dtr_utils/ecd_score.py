import nltk
import torch

nltk.download("punkt")
from sklearn.feature_extraction.text import CountVectorizer
import re
import numpy as np
from scipy.stats import entropy

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import spacy

from nltk.corpus import stopwords
import string


from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

import stanza

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

stanza.download("en")  # Download the English model if not already downloaded
# Check if GPU is available
use_gpu = torch.cuda.is_available()

# Initialize the Stanza pipeline with GPU if available
nlp = stanza.Pipeline(
    "en",
    processors="tokenize,ner",
    use_gpu=use_gpu,  # Set GPU usage based on availability
    batch_size=500,
    tokenize_batch_size=500,
)

# Initialize Stanza pipeline and NLTK stop words
# stanza_nlp = stanza.Pipeline(lang="en", processors="tokenize,ner")
stop_words = set(stopwords.words("english"))


# """# Alignment Scoring"""

# import spacy

# if spacy.prefer_gpu():
#     print("Using GPU")
# else:
#     print("Using CPU")

# nlp_spacy = spacy.load("en_core_web_sm")

import time


def get_entity_vector(global_vocab, text):
    vectorizer = CountVectorizer(vocabulary=list(global_vocab))
    X = vectorizer.fit_transform([text.lower()])
    text_vector = X.toarray()[0]
    return text_vector


def remove_stop_words(_string):
    doc = nlp(_string)
    entities = [ent.text.lower() for ent in doc.ents]
    # doc = nlp_spacy(_string)
    filtered_tokens = " ".join(
        [token.text.lower() for token in doc if not token.is_stop]
    )
    return filtered_tokens, entities


def preprocess(t1, t2):
    data = {"t1": dict(), "t2": dict()}
    t1 = t1.splitlines()
    t2 = t2.splitlines()
    for i in range(len(t1)):
        t1[i], entities = remove_stop_words(t1[i])
        for words in entities:
            if words not in data["t1"]:
                data["t1"][words] = {i}
            else:
                data["t1"][words].add(i)
    for i in range(len(t2)):
        t2[i], entities = remove_stop_words(t2[i])
        for words in entities:
            if words not in data["t2"]:
                data["t2"][words] = {i}
            else:
                data["t2"][words].add(i)
    global_vocab = get_global_vocab(t1, t2)
    common_ent = set(data["t1"].keys()).intersection(set(data["t2"].keys()))
    missing_ent = set(data["t1"].keys()).difference(set(data["t2"].keys()))
    extra_ent = set(data["t2"].keys()).difference(set(data["t1"].keys()))
    return data, global_vocab, common_ent, extra_ent, missing_ent, t1, t2


def get_global_vocab(t1, t2):
    global_vocab = set()
    for string in t1:
        words = string.split()
        for word in words:
            global_vocab.add(word)
    for string in t2:
        words = string.split()
        for word in words:
            global_vocab.add(word)

    return global_vocab


def get_kl_div(p, q):
    p = np.where(p == 0, 1e-10, p)
    q = np.where(q == 0, 1e-10, q)
    p = p / np.sum(p)
    q = q / np.sum(q)
    kl_divergence = np.sum(p * np.log(p / q))
    m = 0.5 * (p + q)
    kl_pm = entropy(p, m)
    kl_qm = entropy(q, m)
    js_divergence = 0.5 * (kl_pm + kl_qm)
    return js_divergence


def get_common_entity_kldiv(text1, text2, data, global_vocab, common_entity):
    kl_div = []
    for ent in common_entity:
        if ent == "," or ent == '"':
            continue
        line_nos_from_t1 = data["t1"][ent]
        line_nos_from_t2 = data["t2"][ent]
        t1 = " ".join([text1[lno] for lno in line_nos_from_t1])
        t2 = " ".join([text2[lno] for lno in line_nos_from_t2])
        v1 = get_entity_vector(global_vocab, t1)
        v2 = get_entity_vector(global_vocab, t2)
        # print("v1 -- ",v1)
        # print("v2 -- ",v2)
        kl_div.append(get_kl_div(v1, v2))
    return kl_div


### Use ECD in trees


def alignment_score(t1, t2):
    data, global_vocab, common_entity, extra_entity, missing_entity, text1, text2 = (
        preprocess_batch(t1, t2)
    )

    if len(common_entity) == 0:
        kl_div = [1]
    else:
        kl_div = get_common_entity_kldiv(
            text1, text2, data, global_vocab, common_entity
        )

    return sum(kl_div) / len(kl_div)


# Recursive function to traverse the tree and print leaf nodes
def add_alignment_scores(node, context):
    # Base case: If the node is a leaf (no children), print the leaf node
    if not node.children:
        # print(f"Leaf Node: ({node.name}")
        t1 = node.name

        t2 = context

        score = alignment_score(t1, t2)
        # print(score)

        new_leaf = Node(score, parent=node)
        # node.children.append(new_leaf)

        return

    # Recursive case: Traverse the tree and visit each child
    for child in node.children:
        add_alignment_scores(child, context)


# # Optimized preprocessing function with caching of data and global vocab
# Initialize the data dictionary to store line indices for words/entities


def preprocess_batch(t1, t2):
    """
    Preprocess a batch of texts to extract entities and filtered tokens without stopwords.

    Args:
        texts (list): List of input texts (strings) to process.

    Returns:
        tuple: A tuple containing the following:
            - data: Dictionary with words as keys and their corresponding line indices as values.
            - global_vocab: Set of all unique words in both texts.
            - common_ent: Set of entities common to both texts.
            - missing_ent: Set of entities missing in one text but present in the other.
            - extra_ent: Set of entities extra in one text compared to the other.
            - filtered_texts: List of filtered texts (without stopwords and punctuation).
    """

    # # Replace \n with . in both t1 and t2
    t1 = t1.replace("\n", ". \n")
    t2 = t2.replace("\n", ". \n")

    data = {"t1": {}, "t2": {}}
    texts = [t1, t2]
    # Process texts in batches with Stanza
    docs = [nlp(text) for text in texts]  # Process the batch

    filtered_t1 = ""
    filtered_t2 = ""

    stop_words_set = set(stop_words)  # Assuming stop_words is a list, convert to a set

    # Iterate through the processed documents
    for j, doc in enumerate(docs):
        filtered_texts = []

        # Iterate over sentences and words in the document
        for i, sentence in enumerate(doc.sentences):

            entities = set()
            for ent in sentence.ents:
                # Add the named entity text to the entities set (lowercased)
                entities.add(ent.text.lower())

            # Iterate over words in the sentence to collect filtered tokens
            filtered_tokens = []
            for word in sentence.words:
                token = word.text.lower()

                # Filter out stop words and punctuation
                if token not in stop_words and token not in string.punctuation:
                    filtered_tokens.append(token)

            filtered_text = " ".join(filtered_tokens)
            filtered_texts.append(filtered_text)

            # print(filtered_tokens)
            # print(filtered_text)

            # Update the data dictionary with entities and their line indices
            if j == 0:
                variable = "t1"

            else:
                variable = "t2"

            # print(data[variable])
            for word in entities:
                if word not in data[variable]:
                    data[variable][word] = {i}
                else:
                    data[variable][word].add(i)

        if j == 0:
            filtered_t1 = filtered_texts
        else:
            filtered_t2 = filtered_texts
        # print(filtered_texts, "KK")

        # break

    # Compute global vocabulary
    global_vocab = set()
    for text in filtered_texts:
        global_vocab.update(text.split())

    # Compute common, missing, and extra entities
    t1_entities = set(data["t1"].keys())
    t2_entities = set(data["t2"].keys())

    common_ent = t1_entities.intersection(t2_entities)
    missing_ent = t1_entities.difference(t2_entities)
    extra_ent = t2_entities.difference(t1_entities)

    # print(data)

    return (
        data,
        global_vocab,
        common_ent,
        extra_ent,
        missing_ent,
        filtered_t1,
        filtered_t2,
    )
