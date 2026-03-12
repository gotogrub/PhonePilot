# Setup Guide

## Prerequisites

### System Requirements

- **OS**: Linux (recommended), macOS, Windows with WSL2
- **Python**: 3.11 or newer
- **Node.js**: 20 or newer
- **Docker**: 24+ with Docker Compose v2
- **GPU**: NVIDIA GPU with 8+ GB VRAM (for VLM inference)

### Android Device

1. Enable **Developer Options**: Settings > About Phone > Tap "Build Number" 7 times
2. Enable **USB Debugging**: Settings > Developer Options > USB Debugging
3. Connect via USB and authorize the computer when prompted

### Software

- [Ollama](https://ollama.ai/) — local LLM runtime
- [ADB](https://developer.android.com/tools/adb) — Android Debug Bridge
- [scrcpy](https://github.com/Genymobile/scrcpy) — screen mirroring (optional)

---

## Installation

### Automated Setup

```bash
git clone https://github.com/your-username/phonepilot.git
cd phonepilot
./scripts/setup.sh
```

This will:
1. Check prerequisites (Docker, ADB)
2. Create `.env` from template
3. Build Docker containers
4. Pull the Qwen2.5-VL model
5. Start all services

### Manual Setup

#### 1. Clone and configure

```bash
git clone https://github.com/your-username/phonepilot.git
cd phonepilot
cp .env.example .env
```

Edit `.env` to match your setup.

#### 2. Install Ollama and pull a model

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2.5-vl:7b
```

#### 3. Start with Docker Compose

```bash
docker compose up -d
```

#### 4. Verify

```bash
# Check services
docker compose ps

# Check ADB
adb devices

# Open UI
open http://localhost:3000

# Check API
curl http://localhost:8000/devices
```

---

## Development Setup

For development with hot-reload:

```bash
./scripts/dev.sh
```

Or manually:

```bash
# Terminal 1: Redis
docker compose -f docker-compose.dev.yml up -d redis

# Terminal 2: Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload

# Terminal 3: Frontend
cd frontend
npm install
npm run dev
```

---

## WiFi ADB Setup

To connect your device wirelessly:

```bash
# With device connected via USB:
adb tcpip 5555

# Disconnect USB, then:
adb connect 192.168.1.YOUR_DEVICE_IP:5555
```

Or use the API:

```bash
curl -X POST http://localhost:8000/devices/connect \
  -H "Content-Type: application/json" \
  -d '{"address": "192.168.1.100", "port": 5555}'
```

---

## Troubleshooting

### ADB device not found

```bash
adb kill-server
adb start-server
adb devices
```

Make sure USB debugging is enabled and the computer is authorized.

### Ollama connection refused

Ensure Ollama is running:
```bash
ollama serve
```

### GPU not detected in Docker

Install the NVIDIA Container Toolkit:
```bash
sudo apt install nvidia-container-toolkit
sudo systemctl restart docker
```

### Slow inference

- Use a smaller model: `ollama pull qwen2.5-vl:3b`
- Reduce screenshot resolution in config
- Ensure GPU is being used (check `nvidia-smi`)
