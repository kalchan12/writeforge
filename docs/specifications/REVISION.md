# Controlled Revision Engine Specification

## 1. Overview & Purpose

The **Controlled Revision Engine** produces actionable, rule-governed recommendations for revising text documents toward target stylistic profiles and addressing stylistic anomalies.

Rather than generating unconstrained text replacements or evasive modifications, the engine formulates structured revision strategies containing:
1. **Global Stylistic Goals (`RevisionGoal`)**: Metric-level directional guidance (e.g. increase sentence length variation, reduce average clause length, enhance vocabulary richness).
2. **Granular Sentence Interventions (`SentenceRevisionTarget`)**: Sentence-specific diagnoses with prescriptive writing advice (e.g., partitioning run-on sentences, diversifying monotonous cadence, breaking repetitive sentence openers).

---

## 2. Domain Models

```python
class RevisionGoal(BaseModel):
    metric_name: str
    description: str
    current_value: float
    target_value: float
    direction: str       # 'increase' | 'decrease' | 'maintain'
    severity: str        # 'low' | 'medium' | 'high'

class SentenceRevisionTarget(BaseModel):
    sentence_index: int
    original_text: str
    issue_type: str      # 'excessive_length' | 'cadence_monotony' | 'repetitive_opener' | 'lexical_redundancy'
    suggestion: str
    priority: int        # 1 (high), 2 (medium), 3 (low)

class RevisionPlan(BaseModel):
    document_id: str | None
    target_author: str | None
    goals: list[RevisionGoal]
    sentence_targets: list[SentenceRevisionTarget]
    total_suggestions: int
    summary: str
```

---

## 3. Heuristics & Detection Rules

### 3.1 Sentence-Level Rules
* **Excessive Length (`excessive_length`)**:
  * Trigger: Word count $> 35$ (or $> 1.75 \times \text{profile\_mean}$).
  * Rationale: Long compound clauses cause cognitive fatigue and reduce readability.
  * Prescription: Partition into distinct clauses.
* **Cadence Monotony (`cadence_monotony`)**:
  * Trigger: Three consecutive sentences with word count delta $\le 2$ words.
  * Rationale: Uniform sentence length produces robotic, flat cadence (low burstiness).
  * Prescription: Introduce staccato phrasing or an expansive compound structure to restore rhythmic variance.
* **Repetitive Openers (`repetitive_opener`)**:
  * Trigger: Consecutive sentences starting with the identical grammatical token.
  * Rationale: Over-reliance on repetitive sentence heads weakens rhetorical momentum.
  * Prescription: Invert sentence clauses or introduce adverbial/transitional openers.
* **Lexical Redundancy (`lexical_redundancy`)**:
  * Trigger: Content word (non-function word) appears $\ge 3$ times within a single sentence.
  * Rationale: Verbatim repetition within tight spans indicates limited lexical entropy.
  * Prescription: Substitute with contextual synonyms or rephrase.

### 3.2 Global Goal Derivation
* **Profile-Guided Mode**: Evaluates deviations using `ProfileComparator`. Outlier metrics ($|z| \ge \text{threshold}$) are mapped to `RevisionGoal` items targeted directly at the author's baseline distribution.
* **Standalone Mode**: Applies intrinsic readability and cadence heuristics (e.g. flagging overly dense average sentence lengths or low length standard deviations).

---

## 4. API Endpoints

### `POST /revision/plan`
* **Request**:
  ```json
  {
    "text": "The analytical engine weaves algebraical patterns...",
    "profile": { ... },
    "outlier_threshold": 2.0
  }
  ```
* **Response**: `RevisionPlan` JSON object.
