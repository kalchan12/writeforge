# Development Guide

## 1. Prerequisites

* **Python**: 3.12 or newer
* **uv**: Fast Python package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
* **Node.js**: 20.x or newer
* **npm**: 10.x or newer

## 2. Setting Up the Environment

### Backend & Core Engine

```bash
# Clone the repository
cd rightforge

# Create a virtual environment with uv
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install package in editable mode with development dependencies
uv pip install -e ".[dev]"
```

### Frontend

```bash
cd apps/web
npm install
cd ../..
```

## 3. Running Services

### Start API Server
```bash
source .venv/bin/activate
uvicorn apps.api.main:app --reload --port 8000
```
Verify:
```bash
curl http://localhost:8000/health
```

### Start Web Application
```bash
cd apps/web
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

## 4. Running Tests

```bash
source .venv/bin/activate
pytest
```

To run with verbose output:
```bash
pytest -v
```

## 5. Adding Dependencies

* **Python Dependencies**:
  Add runtime dependencies to `project.dependencies` in `pyproject.toml`.
  Add test/dev dependencies to `project.optional-dependencies.dev` in `pyproject.toml`.
  Always provide a documented rationale in `docs/ai/DECISIONS.md` before adding heavy or external network dependencies.
* **Frontend Dependencies**:
  Add via `npm install <package>` in `apps/web/`.

## 6. Development Workflow for Agents

Always follow the 11-step loop defined in `docs/ai/AGENTS.md`. Never start coding without inspecting current state and reading `PLAN.md`.
