# Research Experimentation Guidelines

## 1. Methodology & Experimental Rigor

RightForge treats empirical experimentation as a first-class citizen while keeping experimental code cleanly decoupled from the production runtime.

* **Reproducibility**: All experiments must specify exact seeds, package versions, hardware characteristics, and dataset splits.
* **Separation**: Scripts and experimental notebooks live in `scripts/` or dedicated evaluation suites, never inside `engine/rightforge/` or `apps/`.
* **Standard Metrics**: Evaluation must report standardized statistical metrics (e.g., Pearson/Spearman correlation, ROC-AUC, macro-F1, error distributions).

## 2. Dataset Management Policy

* **Raw Datasets (`data/raw/`)**: Downloaded or imported corpora remain untouched and uncommitted to git.
* **Processed Datasets (`data/processed/`)**: Normalized, tokenized, or anonymized datasets with documented transformations.
* **Sample Fixtures (`data/samples/`, `tests/fixtures/`)**: Minimal, vetted sample texts used for automated regression tests.

## 3. Experiment Lifecycle

1. **Hypothesis**: Formulate a measurable linguistic or stylometric hypothesis.
2. **Dataset Selection**: Define test corpora and baseline splits.
3. **Execution**: Run evaluation via reproducible script in `scripts/`.
4. **Log Results**: Document outcomes and findings in this directory before incorporating any heuristic into core engine algorithms.
