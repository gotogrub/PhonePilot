<div align="center">

<img src="phone_pilot_logo.png" alt="PhonePilot Logo" width="200">

# PhonePilot

**Local AI agent for Android automation via voice and text**

*Control your phone with natural language. No clouds, full privacy.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-18-blue.svg)](https://react.dev)

</div>

---

## What is PhonePilot?

PhonePilot is a fully local AI agent that understands your Android screen through Vision-Language Models and executes actions via ADB. Give it a command in text or voice — it sees the screen, plans the steps, and taps/swipes/types for you.

```
"Open Telegram and send mom that I'll be home in an hour"
```

The agent captures a screenshot, analyzes it with a VLM (Qwen2.5-VL), determines what to tap, executes the action, verifies the result, and repeats until the task is done.

### Key Features

- **Vision-Language AI** — Understands screen content through Qwen2.5-VL, LLaVA, or any Ollama-compatible model
- **Voice Control** — Hands-free operation with wake word detection, STT (Whisper), and TTS (Piper)
- **Action Memory** — Remembers past actions, learns from failures, builds app knowledge
- **Scenario Automation** — Record, replay, and schedule action sequences
- **Multi-Device** — Control multiple Android devices simultaneously via USB or WiFi
- **Fully Local** — Everything runs on your machine. Zero cloud dependencies

---

## Architecture

```
┌──────────────────────────────────────────────────┐
│  Clients: Web UI / CLI / REST API / Voice        │
└──────────────────────┬───────────────────────────┘
                       │
              ┌────────▼────────┐
              │  FastAPI Gateway │
              │  /tasks /devices │
              │  /stream /voice  │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
    ┌─────▼─────┐ ┌───▼────┐ ┌────▼──────┐
    │ Task Queue │ │  VLM   │ │  Device   │
    │  (Redis)   │ │(Ollama)│ │  Manager  │
    └───────────┘ └────────┘ └───────────┘
          │            │            │
          └────────────┼────────────┘
                       │
              ┌────────▼────────┐
              │   Agent Core    │
              │ Screenshot →    │
              │ VLM Analysis →  │
              │ Action Plan →   │
              │ Execute → Verify│
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Android Device  │
              │  (ADB / scrcpy) │
              └─────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- [Ollama](https://ollama.ai/) with a VLM model
- Android device with USB debugging enabled
- ADB installed (`adb devices` shows your device)

### Setup

```bash
git clone https://github.com/gotogrub/PhonePilot.git
cd PhonePilot

# 1. Install & start Ollama on the host
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2.5-vl:7b

# 2. Start ADB server (accessible from Docker)
adb -a -P 5037 nodaemon server &

# 3. Start services
docker compose up -d

# 4. Open the UI
open http://localhost:3000
```

> Ollama runs on the host by default so it can be shared with other services.
> To run Ollama in Docker instead, see [docs/SETUP.md](docs/SETUP.md#running-ollama-in-docker-alternative).

### Development

```bash
# Start dev environment with hot-reload
./scripts/dev.sh

# Or run components separately:

# Backend
cd backend
pip install -r requirements-dev.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### CLI Usage

```bash
# Execute a command
phonepilot "open Chrome and search for weather"

# Specify device
phonepilot -d DEVICE_ID "take a screenshot"

# Start the API server
phonepilot --server
```

---

## Project Structure

```
phonepilot/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # FastAPI endpoints
│   │   ├── core/            # Agent, Planner, Executor
│   │   ├── device/          # ADB wrapper, scrcpy, device manager
│   │   ├── vlm/             # Ollama client, prompts, response parser
│   │   ├── voice/           # STT, TTS, wake word
│   │   ├── memory/          # SQLAlchemy models, action history
│   │   ├── scenarios/       # Record, playback, scheduling
│   │   └── workers/         # Background task execution
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/      # React UI components
│       ├── hooks/           # WebSocket, device hooks
│       ├── stores/          # Zustand state management
│       └── api/             # API client
├── docker/                  # Ollama, nginx configs
├── scripts/                 # Setup, dev, model download
├── docs/                    # Documentation
└── docker-compose.yml
```

---

## API

Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Execute a command |
| GET | `/devices` | List connected devices |
| WS | `/stream/{device_id}` | Live screen stream |
| GET | `/scenarios` | List scenarios |
| POST | `/scenarios` | Create scenario |
| POST | `/voice/command` | Voice command (audio upload) |
| GET | `/models` | List available VLM models |
| POST | `/models/switch` | Switch active model |

Full API documentation available at `http://localhost:8000/docs` (Swagger UI).

See [docs/API.md](docs/API.md) for detailed reference.

---

## Hardware Requirements

| | Minimum | Recommended |
|---|---------|-------------|
| GPU | 8GB VRAM (RTX 3070) | 16GB VRAM (RTX 4070 Ti / 5060 Ti) |
| RAM | 16GB | 32GB |
| CPU | 4 cores | 8 cores |
| Storage | 20GB | 50GB SSD |

### Model VRAM Usage

| Model | VRAM | Quality |
|-------|------|---------|
| Qwen2.5-VL-3B | ~6GB | Good |
| Qwen2.5-VL-7B | ~14GB | Great |
| LLaVA 1.6 7B | ~14GB | Good |

---

## Documentation

- [Setup Guide](docs/SETUP.md)
- [API Reference](docs/API.md)
- [Models Guide](docs/MODELS.md)
- [Scenarios Guide](docs/SCENARIOS.md)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

[Apache License 2.0](LICENSE)
