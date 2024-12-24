import nltk
import torch

nltk.download("punkt")
from sklearn.feature_extraction.text import CountVectorizer
import re
import numpy as np
from scipy.stats import entropy


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


### Use ECD in trees


def alignment_score(t1, t2):
    data, global_vocab, common_entity, extra_entity, missing_entity, text1, text2 = (
        preprocess(t1, t2)
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
        print(f"Leaf Node: ({node.name}")
        t1 = node.name

        t2 = context

        score = alignment_score(t1, t2)
        print(score)

        new_leaf = Node(score, parent=node)
        # node.children.append(new_leaf)

        return

    # Recursive case: Traverse the tree and visit each child
    for child in node.children:
        add_alignment_scores(child, context)
