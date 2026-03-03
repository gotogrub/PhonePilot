import shutil

import pytest

requires_ollama = pytest.mark.skipif(
    not shutil.which("ollama"),
    reason="Ollama not available",
)

requires_adb = pytest.mark.skipif(
    not shutil.which("adb"),
    reason="ADB not available",
)


@requires_ollama
@pytest.mark.asyncio
async def test_list_models(client):
    response = await client.get("/models")
    assert response.status_code in (200, 500)


@requires_adb
@pytest.mark.asyncio
async def test_list_devices(client):
    response = await client.get("/devices")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_scenarios(client):
    response = await client.get("/scenarios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_voice_status(client):
    response = await client.get("/voice/status")
    assert response.status_code == 200
    data = response.json()
    assert "stt_available" in data
