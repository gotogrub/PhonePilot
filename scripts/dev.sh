#!/usr/bin/env bash
set -euo pipefail

echo "=== PhonePilot Dev Environment ==="

if [ ! -f .env ]; then
    cp .env.example .env
fi

echo "Starting Redis..."
docker compose -f docker-compose.dev.yml up -d redis

echo "Starting backend..."
cd backend
pip install -r requirements-dev.txt -q
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "Starting frontend..."
cd frontend
npm install -q
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "Backend:  http://localhost:8000 (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo "API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
