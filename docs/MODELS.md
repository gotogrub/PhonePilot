# Models Guide

PhonePilot uses Vision-Language Models (VLMs) to understand Android screenshots and determine actions.

## Supported Models

All models are served through [Ollama](https://ollama.ai/).

### Qwen2.5-VL (Recommended)

| Variant | VRAM | Speed | Quality |
|---------|------|-------|---------|
| qwen2.5-vl:3b | ~6GB | Fast | Good for simple tasks |
| qwen2.5-vl:7b | ~14GB | Medium | Best balance |
| qwen2.5-vl:72b | ~40GB | Slow | Highest accuracy |

```bash
ollama pull qwen2.5-vl:7b
```

### LLaVA

| Variant | VRAM | Speed | Quality |
|---------|------|-------|---------|
| llava:7b | ~14GB | Medium | Good |
| llava:13b | ~26GB | Slow | Better |

```bash
ollama pull llava:7b
```

## Choosing a Model

**8GB VRAM (RTX 3070, 4060):**
- Use `qwen2.5-vl:3b` — fast, handles basic navigation well

**16GB VRAM (RTX 4070 Ti, 5060 Ti):**
- Use `qwen2.5-vl:7b` — recommended default, great accuracy

**24GB+ VRAM (RTX 3090, 4090):**
- Use `qwen2.5-vl:7b` with room for concurrent tasks
- Or try larger models for complex multi-step tasks

## Switching Models

### Via API

```bash
curl -X POST http://localhost:8000/models/switch \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen2.5-vl:3b"}'
```

### Via UI

Use the model selector in the web interface settings.

### Via Environment

Set in `.env`:
```
PHONEPILOT_DEFAULT_MODEL=qwen2.5-vl:7b
```

## Model Performance Tips

1. **Keep models loaded** — First inference is slow due to model loading. Subsequent requests are faster
2. **Match model to task** — Use lighter models for simple taps, heavier for complex navigation
3. **Monitor VRAM** — Run `nvidia-smi` to check GPU memory usage
4. **Quantization** — Ollama models are already quantized. Lower quant = less VRAM but lower quality
