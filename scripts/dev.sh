#!/usr/bin/env bash
set -e

# Change directory to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=========================================================="
echo " Starting RightForge Development Environment"
echo "=========================================================="

# 1. Check Python virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    if command -v uv >/dev/null 2>&1; then
        uv venv
        source .venv/bin/activate
        uv pip install -e ".[dev]"
    else
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -e ".[dev]"
    fi
else
    source .venv/bin/activate
fi

# 2. Check frontend dependencies
if [ ! -d "apps/web/node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install --prefix apps/web
fi

# Clean shutdown handler
cleanup() {
    echo ""
    echo "Shutting down RightForge services..."
    if [ -n "$API_PID" ] && kill -0 "$API_PID" 2>/dev/null; then
        kill "$API_PID" 2>/dev/null || true
    fi
    if [ -n "$WEB_PID" ] && kill -0 "$WEB_PID" 2>/dev/null; then
        kill "$WEB_PID" 2>/dev/null || true
    fi
    wait 2>/dev/null || true
    echo "All services stopped."
}
trap cleanup SIGINT SIGTERM EXIT

# 3. Start FastAPI backend
echo "Starting FastAPI Backend on http://localhost:8000 ..."
python -m uvicorn apps.api.main:app --reload --port 8000 &
API_PID=$!

# 4. Start Next.js frontend
echo "Starting Next.js Frontend on http://localhost:3000 ..."
npm run dev --prefix apps/web &
WEB_PID=$!

echo "=========================================================="
echo " RightForge is running:"
echo "   - Web UI:      http://localhost:3000"
echo "   - API Service: http://localhost:8000"
echo "   - API Docs:    http://localhost:8000/docs"
echo " Press Ctrl+C to terminate both servers."
echo "=========================================================="

# Wait for both processes
wait "$API_PID" "$WEB_PID" 2>/dev/null || true
