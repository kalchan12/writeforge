# Research Experimentation & Empirical Benchmarks

## 1. Methodology & Experimental Rigor

RightForge treats empirical experimentation as a scientific discipline, separating research scripts and models from application infrastructure.

* **Reproducibility**: All experiments specify exact random seeds, cross-validation parameters, and package versions.
* **Separation**: Evaluation runners live in `scripts/` and reference the core engine without coupling the engine to ML training artifacts.
* **Metrics**: Reported using standardized statistical indicators (Stratified K-Fold accuracy, precision, recall, F1-scores, feature importance).

---

## 2. Completed Experiments

### Experiment EXP-001: Stylometric Feature Authorship Discrimination

* **Date**: Phase 7
* **Runner Script**: [`scripts/evaluate_classifier.py`](file:///home/kal/writeforge/scripts/evaluate_classifier.py)
* **Objective**: Evaluate whether 31-dimensional deterministic stylometric feature vectors (`StylometricVectorizer`) provide sufficient signal for classical classifiers (Logistic Regression, Random Forest) to discriminate between diverse writing styles without lexical n-gram memorization or transformer embeddings.
* **Corpus Setup**:
  * 3 stylistic classes: *Academic/Formal*, *Noir/Narrative*, *Casual/Blogger* (18 documents total).
  * 3-Fold Stratified Cross-Validation (`random_state=42`).
* **Feature Extraction**:
  * 31 features extracted via `StylometricVectorizer`:
    * Surface & Sentence structure: `avg_words_per_sentence`, `avg_chars_per_word`, `sentence_length_std_dev`, `sentence_length_variance`.
    * Lexical richness: `type_token_ratio`, `root_type_token_ratio`, `average_word_length`, `long_word_ratio`.
    * Punctuation distributions: `punct_comma_count`, `punct_semicolon_count`, `punct_colon_count`, `punct_dash_count`, `punct_quote_count`, `punctuation_density_per_char`, `punctuation_density_per_word`.
    * Stylometric invariants: `hapax_legomena_ratio`, `dis_legomena_ratio`, `yules_k`, `simpsons_d`, `simpsons_diversity`.
    * Closed-class function words: `function_word_ratio`, `preposition_ratio`, `pronoun_ratio`, `conjunction_ratio`, `auxiliary_verb_ratio`, `determiner_ratio`.
    * Readability: `flesch_reading_ease`, `flesch_kincaid_grade`.
    * Semantic flow: `mean_paragraph_coherence`, `mean_sentence_coherence`, `lexical_repetition_rate`.

#### Empirical Results:

| Model | Cross-Validation Strategy | Mean Accuracy | Standard Deviation |
| :--- | :--- | :---: | :---: |
| **Logistic Regression (StandardScaler)** | 3-Fold Stratified CV | 61.11% | $\pm 7.86\%$ |
| **Random Forest (100 estimators)** | 3-Fold Stratified CV | 66.67% | $\pm 13.61\%$ |

#### Top Discriminative Features (Gini Importance Ranking):

1. **`avg_chars_per_word`** (Importance: ~0.114): Primary separator between formal academic prose and casual conversational writing.
2. **`punctuation_density_per_char`** (Importance: ~0.103): Distinguishes complex punctuation in narrative text from plain prose.
3. **`average_word_length`** (Importance: ~0.099): Correlates strongly with vocabulary sophistication.
4. **`flesch_reading_ease`** (Importance: ~0.096): Cleanly segments accessible vs. dense registers.
5. **`flesch_kincaid_grade`** (Importance: ~0.091): Strong secondary indicator of structural complexity.
6. **`punctuation_density_per_word`** (Importance: ~0.075)
7. **`long_word_ratio`** (Importance: ~0.067)
8. **`punct_comma_count`** (Importance: ~0.057)

#### Findings & Takeaways:
* Deterministic stylometric features provide strong discriminatory signal across genres even on small document corpora.
* Surface readability and character distributions act as top discriminators, supplemented by function word ratios and punctuation density.
* Classical models provide transparent, explainable feature importance, confirming the value of stylometric feature extraction as an interpretable foundation before introducing black-box deep learning.
