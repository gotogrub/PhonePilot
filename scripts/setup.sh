#!/usr/bin/env bash
set -euo pipefail

echo "=== PhonePilot Setup ==="

if ! command -v docker &>/dev/null; then
    echo "Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v adb &>/dev/null; then
    echo "ADB not found. Please install Android platform-tools."
    exit 1
fi

echo "Checking ADB devices..."
adb devices

echo "Copying environment config..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

echo "Building containers..."
docker compose build

echo "Starting Ollama and pulling model..."
docker compose up -d ollama
sleep 10
docker compose exec ollama ollama pull qwen2.5-vl:7b

echo "Starting all services..."
docker compose up -d

echo ""
echo "=== Setup Complete ==="
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API docs: http://localhost:8000/docs"
