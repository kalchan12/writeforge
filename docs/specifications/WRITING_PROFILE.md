# Writing Profile & Comparison Specification

## 1. Overview

An **Author Writing Profile** (`engine/rightforge/models/profile.py`) represents the empirical, statistical stylistic signature of an author derived from a representative corpus of their verified writings.

The **Profile Comparator** (`engine/rightforge/profiles/comparator.py`) enables evaluating arbitrary candidate drafts against an author's baseline, quantifying metric deviations ($z$-scores), identifying stylistic anomalies/outliers, and calculating a composite stylistic consistency score.

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
* `min_value` / `max_value`: Observed empirical extrema.
* `sample_count`: Number of documents analyzed ($N$).
* `z_score(value)`: Standard score of an observation:
  $$z = \frac{x - \mu}{\sigma}$$
* `is_within_bounds(value, num_std_devs=2.0)`: Checks if an observed value is within the designated tolerance band ($|z| \le \text{num\_std\_devs}$).

### 2.2 MetricDeviation
Measures how an observed metric in a candidate document compares to the baseline:
* `metric_name`: Name of metric.
* `observed_value`: Value measured in candidate text.
* `baseline_mean`: Author's baseline mean.
* `baseline_std_dev`: Author's baseline standard deviation.
* `z_score`: Standard score ($z$).
* `absolute_z_score`: $|z|$.
* `is_outlier`: Boolean flag indicating whether $|z| > \text{threshold}$ (default: $2.0\sigma$).

### 2.3 ConsistencyReport
Composite evaluation outcome:
* `author_profile_id`: Reference author profile UUID.
* `author_name`: Author name.
* `consistency_score`: Normalized continuous rating in $[0.0, 1.0]$.
  * Computed via Gaussian-decay penalty across all evaluated metrics:
    $$s_i = \exp\left(-\frac{1}{2} \left(\frac{|z_i|}{2.0}\right)^2\right), \quad \text{score} = \frac{1}{M} \sum_{i=1}^M s_i$$
  * Yields $1.00$ for identical metric values, remains $\ge 0.88$ for values within $1\sigma$, and decays gracefully as deviations increase.
* `evaluated_metrics_count`: Count of metrics compared.
* `outlier_count`: Count of flagged outliers.
* `outliers`: List of flagged outlier metric names.
* `deviations`: Detailed mapping of metric name to `MetricDeviation`.
* `summary`: Plain-text qualitative overview.

---

## 3. API Endpoints

### 3.1 Create Profile
* **Endpoint**: `POST /profiles/create`
* **Request**:
  ```json
  {
    "author_name": "Jane Austen",
    "documents": [
      {"text": "Sample 1...", "metadata": {}},
      {"text": "Sample 2...", "metadata": {}}
    ],
    "metadata": {"period": "Regency"}
  }
  ```
* **Response**: `AuthorProfile` JSON.

### 3.2 Compare Document to Profile
* **Endpoint**: `POST /profiles/compare`
* **Request**:
  ```json
  {
    "profile": { ... AuthorProfile ... },
    "text": "Candidate draft to evaluate...",
    "outlier_threshold": 2.0
  }
  ```
* **Response**: `ConsistencyReport` JSON.
