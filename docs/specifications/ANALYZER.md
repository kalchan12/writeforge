# Analyzer Engine Specification

## 1. Overview

The analyzer engine (`engine/rightforge/analysis/`) is responsible for extracting quantifiable properties and linguistic metrics from text documents.

## 2. Core Interface Contract

Analyzers in RightForge follow a composable, functional design:

```python
class BaseAnalyzer(ABC):
    """Abstract base class for all metric analyzers."""

    @abstractmethod
    def analyze(self, target: Document | str) -> AnalysisResult:
        """Extract a collection of MetricResults from the given Document or text string."""
        pass
```

* **Input**: An instance of `rightforge.models.Document` or raw text string.
* **Output**: A structured `rightforge.models.AnalysisResult` containing named `MetricResult` records.
* **Side-Effects**: Analyzers must be stateless and free of side-effects.

---

## 3. Implemented Analyzers

### BasicTextAnalyzer (`engine/rightforge/analysis/basic.py`)

Calculates deterministic surface text metrics without machine learning or external network dependencies.

#### Metrics Extracted:

1. **`character_count`** ($C_{\text{total}}$):
   * Total raw characters in text: $\text{len}(text)$.
2. **`non_whitespace_char_count`** ($C_{\text{non-ws}}$):
   * Character count excluding all whitespace (`\s`).
3. **`word_count`** ($N_{\text{words}}$):
   * Total tokenized word count via Unicode word boundary pattern (ignoring standalone numbers and symbols).
4. **`sentence_count`** ($N_{\text{sent}}$):
   * Total sentences segmented on terminal punctuation (`.`, `!`, `?`, including trailing quotes), excluding known abbreviations and decimal numbers.
5. **`paragraph_count`** ($N_{\text{para}}$):
   * Paragraph count delimited by consecutive newlines (`\n\s*\n+`).
6. **`avg_words_per_sentence`**:
   * Mean sentence length in words: $\frac{N_{\text{words}}}{N_{\text{sent}}}$ (or $0.0$ if $N_{\text{sent}} = 0$).
7. **`avg_chars_per_word`**:
   * Average word length in characters: $\frac{\sum_{w \in W} \text{len}(w)}{N_{\text{words}}}$ (or $0.0$ if $N_{\text{words}} = 0$).
8. **`min_sentence_length`**:
   * Word count of shortest sentence.
9. **`max_sentence_length`**:
   * Word count of longest sentence.
10. **`sentence_length_std_dev`**:
    * Population standard deviation of sentence lengths:
      $$\sigma = \sqrt{\frac{1}{N_{\text{sent}}} \sum_{i=1}^{N_{\text{sent}}} (l_i - \mu)^2}$$
      (or $0.0$ if $N_{\text{sent}} \le 1$).

---

## 4. API Endpoint Contract

* **Endpoint**: `POST /analysis/basic`
* **Request Body**:
  ```json
  {
    "text": "String content to analyze",
    "metadata": {}
  }
  ```
* **Response**: `AnalysisResult` JSON containing `document_id`, `metrics`, and `metadata`.
