# Analyzer Engine Specification

## 1. Overview

The analyzer engine (`engine/rightforge/analysis/`) is responsible for extracting quantifiable properties, linguistic structures, and stylometric characteristics from text documents. It utilizes composable, deterministic analyzers built in pure Python.

> **Research Boundary Note**: None of the metrics computed by these analyzers indicate whether a text was authored by an AI system. They represent empirical, mathematical, stylistic, and linguistic characteristics of the input text.

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

### 3.5 StylometryAnalyzer (`engine/rightforge/analysis/stylometry.py`)
Measures authorial fingerprints, vocabulary concentration, function words, and readability:
* **Hapax Legomena** ($V_1$): Count and ratio of words appearing exactly once (`hapax_legomena_count`, `hapax_legomena_ratio`).
* **Dis Legomena** ($V_2$): Count and ratio of words appearing exactly twice (`dis_legomena_count`, `dis_legomena_ratio`).
* **Yule's K Characteristic**:
  $$K = 10^4 \cdot \frac{\sum_{i=1}^{\infty} i^2 V_i - N}{N^2}$$
  Measures vocabulary concentration independent of text length.
* **Simpson's D Index & Diversity**:
  $$D = \frac{\sum n_i (n_i - 1)}{N (N - 1)}, \quad \text{Diversity} = 1 - D$$
* **Function Words**:
  Frequencies of closed-class topic-neutral words resistant to intentional masking:
  * `function_word_count` / `function_word_ratio`
  * `preposition_ratio`
  * `pronoun_ratio`
  * `conjunction_ratio`
  * `auxiliary_verb_ratio`
  * `determiner_ratio`
* **Readability Indices**:
  * `total_syllables` and `syllables_per_word` (rule-based phonetic syllable estimation).
  * **Flesch Reading Ease**:
    $$\text{FRE} = 206.835 - 1.015 \left(\frac{N_{\text{words}}}{N_{\text{sent}}}\right) - 84.6 \left(\frac{N_{\text{syllables}}}{N_{\text{words}}}\right)$$
  * **Flesch-Kincaid Grade Level**:
    $$\text{FKGL} = 0.39 \left(\frac{N_{\text{words}}}{N_{\text{sent}}}\right) + 11.8 \left(\frac{N_{\text{syllables}}}{N_{\text{words}}}\right) - 15.59$$

### 3.6 LinguisticAnalyzer (`engine/rightforge/analysis/linguistic.py`)
Composite pipeline orchestrating `LexicalAnalyzer`, `SentenceAnalyzer`, and `PunctuationAnalyzer`.

---

## 4. API Endpoints

* **POST /analysis/basic**: Surface text statistics.
* **POST /analysis/linguistic**: Lexical diversity, sentence distribution, and punctuation analysis.
* **POST /analysis/stylometry**: Vocabulary invariants, function word usage, and readability scores.
