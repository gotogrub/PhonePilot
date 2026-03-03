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

- [Ollama](https://ollama.ai/) — local LLM runtime (installed on the host)
- [ADB](https://developer.android.com/tools/adb) — Android Debug Bridge
- [scrcpy](https://github.com/Genymobile/scrcpy) — screen mirroring (optional)

---

## Installation

### 1. Clone and configure

```bash
git clone https://github.com/gotogrub/PhonePilot.git
cd PhonePilot
cp .env.example .env
```

### 2. Install and start Ollama on the host

Ollama runs on the host machine by default. This is the recommended setup, especially if other services (Open WebUI, etc.) also depend on it.

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2.5-vl:7b
ollama serve
```

Verify Ollama is accessible:
```bash
curl http://localhost:11434/api/tags
```

### 3. Start ADB server on the host

The ADB server must run on the host so that Docker containers can connect to it:

```bash
# Start ADB server listening on all interfaces
adb kill-server
adb -a -P 5037 nodaemon server &

# Verify your device is visible
adb devices
```

### 4. Start PhonePilot

```bash
docker compose up -d
```

This starts 3 services:
- **backend** (FastAPI) — port 8000
- **frontend** (React + nginx) — port 3000
- **redis** — port 6379

### 5. Verify

```bash
docker compose ps
curl http://localhost:8000/devices
```

Open `http://YOUR_SERVER_IP:3000` in a browser.

---

## Running Ollama in Docker (alternative)

If you prefer running Ollama inside Docker instead of on the host:

```bash
docker compose -f docker-compose.yml -f docker-compose.ollama.yml up -d
```

This adds an Ollama container with GPU passthrough and overrides the backend to connect to it. Requires [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html):

```bash
sudo apt install nvidia-container-toolkit
sudo systemctl restart docker
```

Then pull a model inside the container:

```bash
docker compose exec ollama ollama pull qwen2.5-vl:7b
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
adb -a -P 5037 nodaemon server &
adb devices
```

Make sure USB debugging is enabled and the computer is authorized on the phone.

### Ollama connection refused

Ensure Ollama is running on the host:
```bash
ollama serve
curl http://localhost:11434/api/tags
```

If using Docker Ollama, check the container:
```bash
docker compose -f docker-compose.yml -f docker-compose.ollama.yml logs ollama
```

### Devices show as empty in UI

The backend uses `network_mode: host` and connects to the ADB server at `127.0.0.1:5037`. Make sure:
1. ADB server is running on the host (`adb -a -P 5037 nodaemon server &`)
2. The phone is authorized and visible (`adb devices` on host shows it)

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
