# Local LLM Integration Specification

## 1. Architectural Philosophy & Stance

RightForge integrates Large Language Models solely through a **local-first, privacy-preserving, zero-telemetry** architecture.

* **Local Inference**: Supports local inference daemons (primarily [Ollama](https://ollama.ai)) via HTTP interfaces running on localhost (`http://localhost:11434`).
* **Deterministic Fallbacks**: Equips the platform with `MockLLMProvider` for CI testing, offline builds, and environments without GPU/model acceleration.
* **Controlled Revision**: The LLM is never invoked in an open-ended conversational mode. It is conditioned strictly on diagnostic findings (`RevisionPlan`) produced by RightForge's deterministic stylometric analysis engines.
* **Anti-Hallucination & Plain Output**: System and user prompts enforce strict constraints prohibiting conversational preambles ("Sure, here is your text:"), apologies, or factual distortions.

---

## 2. Component Design

```text
                  ┌───────────────────────────────┐
                  │         Target Document       │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │        RevisionPlanner        │
                  └───────────────┬───────────────┘
                                  │
                       Generates RevisionPlan
                       (Goals + Sentence Targets)
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │     RevisionPromptBuilder     │
                  └───────────────┬───────────────┘
                                  │
                       Formats System & User Prompts
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │        BaseLLMProvider        │
                  │  (OllamaProvider / Mock)      │
                  └───────────────┬───────────────┘
                                  │
                       Generates Revised Text
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │       RevisionExecutor        │
                  │   (Pre/Post Metric Validation)│
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │    RevisionExecutionResult    │
                  └───────────────────────────────┘
```

---

## 3. Domain Model (`RevisionExecutionResult`)

```python
class RevisionExecutionResult(BaseModel):
    document_id: str | None = None
    original_text: str
    revised_text: str
    plan: RevisionPlan
    consistency_before: float | None = None
    consistency_after: float | None = None
    metrics_before: dict[str, float]
    metrics_after: dict[str, float]
    success: bool = True
    error_message: str | None = None
```

---

## 4. API Endpoints

### `POST /revision/execute`
* **Request**:
  ```json
  {
    "text": "The analytical engine weaves algebraical patterns...",
    "profile": { ... },
    "model": "llama3",
    "endpoint_url": "http://localhost:11434",
    "use_mock": false,
    "outlier_threshold": 2.0
  }
  ```
* **Response**: `RevisionExecutionResult` object.
