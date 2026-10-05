# Analyzer Engine Specification

## 1. Overview

The analyzer engine (`engine/rightforge/analysis/`) is responsible for extracting quantifiable properties and linguistic metrics from text documents. It utilizes composable, deterministic analyzers built in pure Python.

> **Research Boundary Note**: None of the metrics computed by these analyzers indicate whether a text was authored by an AI system. They represent purely empirical, mathematical, and linguistic characteristics of the input text.

## 2. Core Interface Contract

Analyzers in RightForge inherit from `BaseAnalyzer` (`engine/rightforge/analysis/base.py`):

```python
class BaseAnalyzer(ABC):
    """Abstract base class for all modular metric analyzers."""

    @abstractmethod
    def analyze(self, target: Document | str) -> list[MetricResult]:
        """Extract a list of MetricResult items from target."""
        pass
```

* **Input**: An instance of `rightforge.models.Document` or raw text string.
* **Output**: A list of `rightforge.models.MetricResult` objects, or packaged in an `AnalysisResult`.
* **State & Side-Effects**: All analyzers are stateless and deterministic.

---

## 3. Implemented Analyzers

### 3.1 BasicTextAnalyzer (`engine/rightforge/analysis/basic.py`)
Surface document statistics:
* `character_count`: Total characters including whitespace.
* `non_whitespace_char_count`: Characters excluding whitespace.
* `word_count`: Total words extracted via word boundary tokenization.
* `sentence_count`: Sentences segmented on terminal punctuation.
* `paragraph_count`: Paragraphs delimited by blank lines.
* `avg_words_per_sentence`: $\frac{N_{\text{words}}}{N_{\text{sent}}}$ (or 0.0 if $N_{\text{sent}} = 0$).
* `avg_chars_per_word`: $\frac{\sum \text{len}(w)}{N_{\text{words}}}$ (or 0.0 if $N_{\text{words}} = 0$).
* `min_sentence_length` / `max_sentence_length`: Word counts of shortest / longest sentences.
* `sentence_length_std_dev`: Population standard deviation of sentence lengths in words.

### 3.2 LexicalAnalyzer (`engine/rightforge/analysis/lexical.py`)
Measures vocabulary richness and lexical diversity:
* `total_word_count`: Total token count ($N$).
* `unique_word_count`: Count of unique vocabulary types ($V$) normalized to lowercase.
* `type_token_ratio` (TTR): Ratio of vocabulary to total words: $\frac{V}{N}$.
  * *Known Limitation*: TTR decreases monotonically as document length increases.
* `root_type_token_ratio` (Guiraud's R): $\frac{V}{\sqrt{N}}$ (partially compensates for text length differences).
* `average_word_length`: Mean characters per word token.
* `long_word_count` / `long_word_ratio`: Frequency and proportion of words with length $\ge 7$ characters.

### 3.3 SentenceAnalyzer (`engine/rightforge/analysis/sentence.py`)
Measures sentence architecture, variance, and rhythm:
* `sentence_count`: Total sentences.
* `sentence_length_mean`: Mean sentence word count.
* `sentence_length_variance`: Population variance of sentence lengths.
* `sentence_length_std_dev`: Population standard deviation ($\sigma$).
* `shortest_sentence_length` / `longest_sentence_length`: Minimum and maximum sentence lengths in words.

### 3.4 PunctuationAnalyzer (`engine/rightforge/analysis/punctuation.py`)
Measures mark frequencies and punctuation density:
* Specific mark counts: `punct_comma_count`, `punct_period_count`, `punct_semicolon_count`, `punct_colon_count`, `punct_parentheses_count`, `punct_question_count`, `punct_exclamation_count`, `punct_dash_count` (hyphen, en-dash, em-dash), `punct_quote_count`.
* `total_punctuation_count`: Sum of all tracked punctuation marks.
* `punctuation_density_per_char`: $\frac{\text{total punctuation}}{\text{total characters}}$.
* `punctuation_density_per_word`: $\frac{\text{total punctuation}}{\text{total words}}$.

### 3.5 LinguisticAnalyzer (`engine/rightforge/analysis/linguistic.py`)
Composite pipeline orchestrating `LexicalAnalyzer`, `SentenceAnalyzer`, and `PunctuationAnalyzer`, returning a unified `AnalysisResult`.

---

## 4. API Endpoints

### 4.1 Basic Analysis
* **Endpoint**: `POST /analysis/basic`
* **Request**: `{"text": "..."}`
* **Response**: `AnalysisResult` with surface metrics.

### 4.2 Linguistic Analysis
* **Endpoint**: `POST /analysis/linguistic`
* **Request**: `{"text": "..."}`
* **Response**: `AnalysisResult` with lexical, sentence, and punctuation metrics.
