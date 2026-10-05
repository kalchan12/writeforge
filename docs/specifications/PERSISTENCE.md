# RightForge Persistence & Desktop Specification

## 1. Overview

RightForge adheres strictly to a **local-first, privacy-preserving architecture**. All user texts, author profiles, and revision audit logs are stored locally on the user's filesystem using an embedded SQLite database. No external database servers, cloud backends, or network telemetry are required.

---

## 2. Storage Architecture

The persistence layer is implemented in `engine/rightforge/storage/db.py` via the `DatabaseManager` class.

```
┌────────────────────────────────────────────────────────┐
│                   RightForge Services                  │
│   (FastAPI Backend / CLI / Desktop Launcher)           │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│         DatabaseManager (engine.storage.db)            │
│   - Connection pooling & Thread Safety                 │
│   - PRAGMA journal_mode = WAL;                         │
│   - PRAGMA synchronous = NORMAL;                       │
│   - PRAGMA foreign_keys = ON;                          │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│            SQLite File (data/rightforge.db)            │
│   ├── documents                                        │
│   ├── author_profiles                                  │
│   └── revision_logs                                    │
└────────────────────────────────────────────────────────┘
```

### 2.1 Default Locations & Configuration
- **Default Database Path**: `data/rightforge.db` relative to repository root.
- **Environment Override**: `RIGHTFORGE_DB_PATH` can be set to any arbitrary absolute or relative filesystem path (e.g. for testing or isolated environments).

### 2.2 Concurrency & WAL Mode
To support concurrent requests from the FastAPI async worker without database locks:
1. `PRAGMA journal_mode = WAL;` (Write-Ahead Logging) permits concurrent readers while a write is underway.
2. `PRAGMA synchronous = NORMAL;` optimizes write performance while maintaining durability against operating system crashes.
3. `sqlite3.connect(..., check_same_thread=False)` enables seamless multi-threaded FastAPI endpoint dispatch.

---

## 3. Database Schema

### 3.1 `documents`
Stores imported, analyzed, or generated documents.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | Unique document UUID |
| `text` | `TEXT` | `NOT NULL` | Raw text content |
| `metadata` | `TEXT` | `DEFAULT '{}'` | JSON serialized dictionary of metadata |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Ingestion timestamp |

### 3.2 `author_profiles`
Stores calculated authorial baselines for style comparison and guided revision.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | Unique profile UUID |
| `name` | `TEXT` | `NOT NULL` | Profile name (e.g., "Hemingway Style") |
| `description` | `TEXT` | `DEFAULT ''` | Profile notes or background |
| `sample_count` | `INTEGER` | `NOT NULL` | Number of documents aggregated |
| `baselines` | `TEXT` | `NOT NULL` | JSON serialized map of metric distributions |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Creation timestamp |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Last updated timestamp |

### 3.3 `revision_logs`
Maintains an immutable audit trail of all automated and guided revisions.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | Unique revision UUID |
| `original_text` | `TEXT` | `NOT NULL` | Text prior to revision |
| `revised_text` | `TEXT` | `NOT NULL` | Text produced by revision engine |
| `provider` | `TEXT` | `NOT NULL` | Inference provider (`ollama`, `mock`, etc.) |
| `model` | `TEXT` | `NOT NULL` | Model name / version |
| `score_deltas` | `TEXT` | `DEFAULT '{}'` | JSON serialized pre- and post-revision metrics |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Execution timestamp |

---

## 4. API Endpoints

The persistence layer exposes CRUD and audit operations across FastAPI endpoints:

- `POST /profiles/create`: Aggregates sample texts into an `AuthorProfile` and persists it to SQLite.
- `GET /profiles`: Returns a list of all persisted author profiles.
- `GET /profiles/{profile_id}`: Retrieves a specific author profile and baseline metrics.
- `POST /revision/execute`: Executes local LLM-assisted revision and automatically logs the input, output, provider, and metric deltas to SQLite.
- `GET /revision/logs?limit=50`: Returns the immutable revision audit trail.

---

## 5. Standalone Desktop Launcher

RightForge includes a dedicated Python launcher (`scripts/desktop_launcher.py`) that coordinates standalone local execution:

```bash
# Launch in development mode with automatic browser dispatch
python3 scripts/desktop_launcher.py

# Launch on custom ports with custom DB path without auto-opening browser
python3 scripts/desktop_launcher.py --api-port 8080 --web-port 3030 --no-browser --db-path /tmp/custom.db
```

### Lifecycle Management:
1. **Port Verification**: Checks for existing port conflicts before spawning.
2. **Process Management**: Concurrently spawns the FastAPI backend (`uvicorn`) and Next.js frontend (`npm run dev` or `npm run start`).
3. **Health Probing**: Polls `http://127.0.0.1:8000/health` and the web UI port until responsive.
4. **Browser Dispatch**: Invokes the operating system's default browser targeting the dashboard.
5. **Clean Teardown**: Traps `SIGINT` (Ctrl+C) and `SIGTERM`, gracefully shutting down child processes with timeout fallback to force termination.
