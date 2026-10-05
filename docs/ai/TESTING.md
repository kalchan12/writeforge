# Testing Philosophy & Guidelines

## 1. Testing Philosophy

* **Deterministic by Default**: Unit tests for core analyzers must be deterministic. Given the same input, they must assert exact mathematical or linguistic values, not merely check for truthiness or execution without errors.
* **Fast Execution**: Unit tests should complete in seconds. Do not introduce slow network or external model downloads into unit test runs.
* **Separation of Concerns**: Unit tests verify isolated engine algorithms; integration tests verify API serialization, HTTP responses, and component interactions.

## 2. Test Directory Structure

```text
tests/
├── unit/            # Fast, pure unit tests for engine models & analyzers
│   ├── test_imports.py
│   └── test_domain_models.py
├── integration/     # Service and endpoint tests (FastAPI TestClient)
│   └── test_health.py
└── fixtures/        # Standardized, versioned text samples for testing
    └── .gitkeep
```

## 3. Writing Effective Tests

### Unit Tests
* Place in `tests/unit/`.
* Test edge cases:
  * Empty text (`""`).
  * Whitespace only (`"   \n\t  "`).
  * Single words, single sentences.
  * Complex punctuation (em dashes, semicolons, multiple quotation marks).
  * Unicode characters and diacritics.

### Integration Tests
* Place in `tests/integration/`.
* Use `fastapi.testclient.TestClient`.
* Assert HTTP status codes and exact response schema shapes.

### Fixtures Policy
* Fixtures in `tests/fixtures/` should be short, royalty-free, or synthetic text passages.
* Do not check large corpora into version control. Use `data/` (gitignored) for research corpora.
