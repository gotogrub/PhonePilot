# API Reference

Base URL: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

---

## Tasks

### Execute Task

```
POST /tasks
```

Request body:
```json
{
  "command": "open Chrome and search for weather",
  "device_id": "DEVICE_SERIAL",
  "model": "qwen2.5-vl:7b"
}
```

`device_id` and `model` are optional. Defaults to first available device and configured model.

Response:
```json
{
  "task_id": "uuid",
  "status": "completed",
  "command": "open Chrome and search for weather",
  "actions": [
    {
      "step": 0,
      "action": {"action_type": "tap", "x": 540, "y": 1200},
      "result": {"status": "success"}
    }
  ],
  "error": null
}
```

### Get Task

```
GET /tasks/{task_id}
```

Returns task details and execution history.

---

## Devices

### List Devices

```
GET /devices
```

Response:
```json
[
  {
    "device_id": "R5CRA1XXXXX",
    "model": "Pixel 7",
    "status": "online",
    "connection_type": "usb"
  }
]
```

### Connect WiFi Device

```
POST /devices/connect
```

Request body:
```json
{
  "address": "192.168.1.100",
  "port": 5555
}
```

### Disconnect Device

```
POST /devices/{device_id}/disconnect
```

---

## Screen Stream

### WebSocket Stream

```
WS /stream/{device_id}
```

Receives JSON frames:
```json
{
  "type": "frame",
  "data": "base64_encoded_png",
  "device_id": "DEVICE_SERIAL"
}
```

Frames are sent approximately every 500ms.

---

## Scenarios

### List Scenarios

```
GET /scenarios
```

### Create Scenario

```
POST /scenarios
```

Request body:
```json
{
  "name": "morning_routine",
  "description": "Check weather and calendar",
  "steps": [
    {"action": "open", "target": "Weather", "wait": 2.0},
    {"action": "tap", "target": "today"},
    {"action": "open", "target": "Calendar"}
  ]
}
```

### Get / Update / Delete Scenario

```
GET    /scenarios/{name}
PUT    /scenarios/{name}
DELETE /scenarios/{name}
```

### Run Scenario

```
POST /scenarios/{name}/run
```

---

## Voice

### Voice Command

```
POST /voice/command
Content-Type: multipart/form-data
```

Upload audio file. Returns transcribed text and task result.

Response:
```json
{
  "text": "open settings",
  "task_id": "uuid",
  "status": "completed"
}
```

### Voice Status

```
GET /voice/status
```

Response:
```json
{
  "stt_available": true,
  "tts_available": true,
  "wake_word_active": false
}
```

---

## Models

### List Models

```
GET /models
```

Response:
```json
[
  {"name": "qwen2.5-vl:7b", "size": "4.7GB", "active": true},
  {"name": "llava:7b", "size": "4.5GB", "active": false}
]
```

### Switch Model

```
POST /models/switch
```

Request body:
```json
{
  "model": "llava:7b"
}
```
