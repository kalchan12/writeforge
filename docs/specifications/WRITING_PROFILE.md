# Writing Profile Specification

## 1. Overview

An **Author Writing Profile** (`engine/rightforge/models/profile.py`) represents the empirical, statistical stylistic signature of an author derived from a representative corpus of their verified writings.

Instead of reducing an author's voice to a single scalar value, RightForge profiles capture multi-dimensional baseline distributions across surface metrics, lexical richness, syntactic cadence, punctuation densities, and stylometric invariants.

---

## 2. Domain Models

### 2.1 MetricBaseline
Each individual metric in a profile is modeled by a `MetricBaseline`:
* `name`: Metric identifier (e.g., `avg_words_per_sentence`, `yules_k`, `type_token_ratio`).
* `mean`: Empirical average across the sample documents:
  $$\mu = \frac{1}{N} \sum_{i=1}^N x_i$$
* `variance`: Population variance:
  $$\sigma^2 = \frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2$$
* `std_dev`: Population standard deviation ($\sigma = \sqrt{\sigma^2}$).
* `min_value`: Minimum observed metric value ($\min_{i} x_i$).
* `max_value`: Maximum observed metric value ($\max_{i} x_i$).
* `sample_count`: Number of documents analyzed ($N$).
* `z_score(value)`: Standard score of an observation:
  $$z = \frac{x - \mu}{\sigma}$$
* `is_within_bounds(value, num_std_devs=2.0)`: Evaluates if an observed metric lies within the author's expected deviation envelope ($|z| \le \text{num\_std\_devs}$).

### 2.2 AuthorProfile
Container representing the complete authorial fingerprint:
* `id`: Unique UUID identifier.
* `author_name`: Author name or identifier.
* `document_count`: Number of aggregated sample documents.
* `baselines`: Map of metric names to their respective `MetricBaseline` objects.
* `metadata`: Freeform contextual dictionary (e.g., genre, era, corpus identifier).
* `created_at` / `updated_at`: UTC timestamps.

---

## 3. Profile Aggregation Engine (`engine/rightforge/profiles/aggregator.py`)

The `ProfileAggregator` accepts multiple `Document` instances (or raw text strings) and performs:
1. Multi-tier analysis across all documents via `BasicTextAnalyzer`, `LinguisticAnalyzer`, and `StylometryAnalyzer`.
2. Numerical extraction across all computed metric values.
3. Summary statistic generation (mean, variance, standard deviation, bounds).
4. Profile assembly and metadata preservation.

---

## 4. API Endpoints

### Create Profile
* **Endpoint**: `POST /profiles/create`
* **Request**:
  ```json
  {
    "author_name": "Jane Austen",
    "documents": [
      {"text": "Sample text from Pride and Prejudice...", "metadata": {}},
      {"text": "Sample text from Sense and Sensibility...", "metadata": {}}
    ],
    "metadata": {"period": "Regency", "genre": "novel"}
  }
  ```
* **Response**: `AuthorProfile` JSON structure with complete statistical baselines.
