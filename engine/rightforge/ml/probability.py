"""Language and probability models for text perplexity and burstiness evaluation."""

from abc import ABC, abstractmethod
from collections import Counter, defaultdict
import math
from typing import Sequence

from rightforge.text.segmentation import tokenize_words

DEFAULT_REFERENCE_CORPUS = [
    "The analytical engine weaves algebraical patterns just as the Jacquard loom weaves flowers and leaves.",
    "A journey of a thousand miles begins with a single step forward into the unknown horizon.",
    "It is a truth universally acknowledged that a single man in possession of a good fortune must be in want of a wife.",
    "The quick brown fox jumps over the lazy dog in the sunny afternoon meadow.",
    "Science is the systematic enterprise that builds and organizes knowledge in the form of testable explanations.",
    "All human actions have one or more of these seven causes: chance, nature, compulsion, habit, reason, passion, desire.",
    "The artist is the creator of beautiful things. To reveal art and conceal the artist is art's aim.",
    "In the middle of difficulty lies opportunity, waiting for those who persevere with patience and intellect.",
    "Writing is an exploration where you start from nothing and learn as you proceed along the structured path.",
    "Language is the dress of thought, reflecting every subtlety of character, reason, and emotional depth.",
    "The machine does not isolate man from the great problems of nature but plunges him more deeply into them.",
    "To be or not to be, that is the fundamental question of existence, consciousness, and human purpose.",
    "Deep in the quiet forest, ancient trees stood witness to the passage of centuries and silent seasons.",
    "Empirical evidence gathered through rigorous methodology forms the bedrock of modern scientific discovery.",
    "Clear prose indicates clear thinking, while muddled sentences betray confusion and lack of rigorous discipline.",
    "Every word chosen by a careful author carries weight, cadence, intention, and acoustic texture.",
]


class BaseProbabilityModel(ABC):
    """Abstract base class for probability models scoring token sequences."""

    @abstractmethod
    def score_tokens(self, tokens: list[str]) -> list[float]:
        """Compute conditional log-probabilities ln(P(w_i | context)) for a sequence of tokens."""
        pass

    def score_sentence(self, tokens: list[str]) -> tuple[float, float]:
        """Compute perplexity and mean log-probability for a token sequence.

        Returns:
            Tuple of (perplexity, mean_logprob).
        """
        if not tokens:
            return 1.0, 0.0

        logprobs = self.score_tokens(tokens)
        if not logprobs:
            return 1.0, 0.0

        mean_logprob = sum(logprobs) / len(logprobs)
        # Perplexity = exp(-mean_logprob)
        perplexity = math.exp(-mean_logprob)
        return round(perplexity, 4), round(mean_logprob, 4)


class NgramProbabilityModel(BaseProbabilityModel):
    """Deterministic n-gram language model with Lidstone smoothing.

    Operates purely in memory with zero external weights or network calls,
    providing fully reproducible log-probability and perplexity scoring.
    """

    def __init__(
        self,
        reference_corpus: Sequence[str] | None = None,
        smoothing_k: float = 0.5,
    ) -> None:
        self.smoothing_k = smoothing_k
        self.unigram_counts: Counter[str] = Counter()
        self.bigram_counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
        self.total_tokens: int = 0
        self.vocab: set[str] = set()

        corpus = list(reference_corpus) if reference_corpus is not None else DEFAULT_REFERENCE_CORPUS
        self.train(corpus)

    def train(self, texts: Sequence[str]) -> None:
        """Update n-gram frequency distributions with provided text corpus."""
        for text in texts:
            words = tokenize_words(text, lowercase=True)
            if not words:
                continue

            prev = "<s>"
            self.unigram_counts[prev] += 1
            for word in words:
                self.unigram_counts[word] += 1
                self.bigram_counts[prev][word] += 1
                self.vocab.add(word)
                self.total_tokens += 1
                prev = word
            self.bigram_counts[prev]["</s>"] += 1
            self.unigram_counts["</s>"] += 1

    def score_tokens(self, tokens: list[str]) -> list[float]:
        """Calculate conditional log probabilities for each token using smoothed bigram modeling."""
        if not tokens:
            return []

        vocab_size = max(len(self.vocab), 1)
        logprobs: list[float] = []
        prev = "<s>"

        for token in tokens:
            word = token.lower()
            context_count = self.unigram_counts.get(prev, 0)
            bigram_count = self.bigram_counts[prev].get(word, 0)

            if context_count > 0:
                # Conditional probability P(word | prev) with Lidstone smoothing
                prob = (bigram_count + self.smoothing_k) / (
                    context_count + self.smoothing_k * vocab_size
                )
            else:
                # Backoff to smoothed unigram distribution
                word_unigram = self.unigram_counts.get(word, 0)
                prob = (word_unigram + self.smoothing_k) / (
                    self.total_tokens + self.smoothing_k * (vocab_size + 1)
                )

            # Guard against potential underflow or non-positive values
            prob = max(prob, 1e-12)
            logprobs.append(math.log(prob))
            prev = word

        return logprobs
