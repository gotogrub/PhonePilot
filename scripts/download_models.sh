#!/usr/bin/env bash
set -euo pipefail

OLLAMA_URL="${PHONEPILOT_OLLAMA_BASE_URL:-http://localhost:11434}"

echo "=== Downloading VLM Models ==="

echo "Pulling Qwen2.5-VL 7B (primary model)..."
ollama pull qwen2.5-vl:7b

echo ""
echo "Optional models:"
echo "  ollama pull qwen2.5-vl:3b    # Lighter, faster"
echo "  ollama pull llava:7b          # Alternative VLM"
echo ""
echo "Done. Available models:"
ollama list
