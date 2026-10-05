# Security & Privacy Architecture

## 1. Threat Model & Privacy Stance

RightForge is designed to analyze sensitive, private, or proprietary text, including academic drafts, unpublished creative work, and research materials.

Our core security baseline rests on **local-first execution**:
* User text is processed entirely within the local runtime.
* No telemetry, usage statistics, or document snippets are transmitted to external servers.
* No cloud-based AI/LLM APIs are invoked without explicit, user-configured authorization.

## 2. Data Handling

* **Data Minimization**: In-memory analysis does not persist documents to disk unless the user explicitly requests storage or project saving.
* **Temporary Files**: Analysis routines must avoid creating temporary plaintext files in shared system directories (`/tmp`).
* **Cache Segregation**: If caching is implemented in future phases, cache keys must be hashed (e.g., SHA-256) and never expose raw content in plaintext logs.

## 3. Input Validation & API Boundary Security

* **Strict Schemas**: Every API endpoint must enforce strict Pydantic schemas on incoming payloads.
* **Payload Limits**: Future milestones handling large texts must enforce maximum request size limits to prevent memory exhaustion / denial of service.
* **Content Injection**: Parsers must sanitize or safely handle raw input, avoiding shell execution, unsafe serialization (no `pickle`), or dynamic code evaluation (`eval`).

## 4. File-System Security

* Safe file path resolution: Any file-handling component must validate paths against directory traversal (`../`) attacks.
* The application should operate with minimal local filesystem privileges.

## 5. Secrets & Dependency Management

* **No Hardcoded Secrets**: Secrets, keys, or credentials must never be committed to source control.
* **Dependency Auditing**: Keep dependencies minimal. Use `uv pip compile` / lockfiles and audit packages against known vulnerabilities.
* **Reproducible Environment**: Dependencies are explicitly declared in `pyproject.toml` and `package.json`.
