import re
from collections import Counter, defaultdict
from transformers import AutoTokenizer
import stanza


# Define the NgramModel class
class NgramModel:
    def __init__(
        self,
        model_checkpoint,
        nlp_model="en",
        use_gpu=True,
        batch_size=500,
        tokenize_batch_size=500,
    ):
        # Load the model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

        # Initialize the stanza NLP pipeline for named entity recognition (NER)
        stanza.download(nlp_model)
        self.nlp = stanza.Pipeline(
            nlp_model,
            processors="tokenize,ner",
            use_gpu=use_gpu,
            batch_size=batch_size,
            tokenize_batch_size=tokenize_batch_size,
        )

    def kneser_ney_smoothing(self, ngram_counts, lower_order_counts, discount=0.75):
        """
        Apply Kneser-Ney smoothing to n-gram counts.

        Args:
            ngram_counts (Counter): Counts of n-grams (e.g., 4-grams or 3-grams).
            lower_order_counts (Counter): Counts of (n-1)-grams (e.g., 3-grams or 2-grams).
            discount (float): Discounting parameter.

        Returns:
            defaultdict: Smoothed probabilities.
        """
        continuation_counts = Counter()

        lower_counts = Counter()

        for ngram in ngram_counts:
            lower_ngram = ngram[1:]
            continuation_counts[lower_ngram] += 1
            lower_counts[lower_ngram] += 1

        def continuation_probability(word):
            return continuation_counts[word] / sum(continuation_counts.values())

        probabilities = defaultdict(lambda: defaultdict(float))

        for ngram, count in ngram_counts.items():
            lower_ngram = ngram[:-1]
            lower_count = lower_order_counts[lower_ngram]
            discounted_count = max(count - discount, 0)
            lambda_factor = (discount / lower_count) * len(continuation_counts)
            probabilities[lower_ngram][ngram[-1]] = (
                discounted_count / lower_count
            ) + lambda_factor * continuation_probability(ngram[-1])

        return probabilities

    def create_ngrams(self, tokens, n):
        return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]

    def get_ngram_tokens(
        self,
        input_tokens,
        context_text,
        two_gram_probs,
        three_gram_probs,
        four_gram_probs,
        top_k=4,
    ):
        context_tokens = self.tokenizer.tokenize(context_text)

        __token_pob__ = {}

        num = 0
        while __token_pob__ == {} and num < 3:
            probs = [four_gram_probs, three_gram_probs, two_gram_probs][num]
            __inputs__ = tuple(input_tokens[-(3 - num) :])
            __token_pob__ = probs.get(__inputs__, {})
            num += 1

        sorted_tokens = sorted(__token_pob__.items(), key=lambda x: x[1], reverse=True)[
            :top_k
        ]

        return [
            (self.tokenizer.convert_tokens_to_string([token]), prob, "n-gram")
            for token, prob in sorted_tokens
        ]

    def get_entities(self, context):
        doc = self.nlp(context)

        entities = [
            ent.text.lower() for ent in doc.ents
        ]  # Get all named entities as a list of strings
        # print("Entities :", entities, "\n\n")

        # Initialize a list to store the tokenized entities
        tokenized_entities = []

        # Tokenize each entity and store in the list
        for entity in entities:
            tokens = self.tokenizer.tokenize(entity)
            tokenized_entities.extend(tokens)

        entity_tokens = [
            self.tokenizer.convert_tokens_to_string([item])
            for item in tokenized_entities
        ]

        entities.extend(entity_tokens)

        special_characters = [
            "!",
            '"',
            "#",
            "$",
            "%",
            "&",
            "'",
            "(",
            ")",
            "*",
            "+",
            ",",
            "-",
            ".",
            "/",
            ":",
            ";",
            "<",
            "=",
            ">",
            "?",
            "@",
            "[",
            "\\",
            "]",
            "^",
            "_",
            "`",
            "{",
            "|",
            "}",
            "~",
        ]

        # Remove special characters from entities
        entities = [item for item in entities if item not in special_characters]

        return entities

    def extract_and_rank_n_grams(self, text, n=5):
        """Extract n-grams from the beginning of each sentence."""
        # Split text into sentences
        sentences = re.split(r"(?<=[.!?]) +", text)
        n_grams = []

        for sentence in sentences:
            # Tokenize the sentence into words
            words = sentence.split()
            # Take the first n words if there are enough words in the sentence
            if len(words) >= n:
                n_gram = " ".join(words[:n])
                n_grams.append(n_gram)
                # print(n_gram, "Check")

        return Counter(n_grams).most_common()

    def get_ngram_probs(self, sample_text):
        context_tokens = self.tokenizer.tokenize(sample_text)

        four_grams = self.create_ngrams(context_tokens, 4)
        three_grams = self.create_ngrams(context_tokens, 3)
        two_grams = self.create_ngrams(context_tokens, 2)
        one_grams = self.create_ngrams(context_tokens, 1)

        # Count the occurrences of each n-gram
        four_gram_counts = Counter(four_grams)
        three_gram_counts = Counter(three_grams)
        two_gram_counts = Counter(two_grams)
        one_gram_counts = Counter(one_grams)

        # Apply Kneser-Ney smoothing iteratively
        two_gram_probs = self.kneser_ney_smoothing(two_gram_counts, one_gram_counts)
        three_gram_probs = self.kneser_ney_smoothing(three_gram_counts, two_gram_counts)
        four_gram_probs = self.kneser_ney_smoothing(four_gram_counts, three_gram_counts)

        return two_gram_probs, three_gram_probs, four_gram_probs
