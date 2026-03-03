const BASE_URL = "/api";

async function request<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  listDevices: () => request<Device[]>("/devices"),

  executeTask: (command: string, deviceId?: string) =>
    request<TaskResponse>("/tasks", {
      method: "POST",
      body: JSON.stringify({ command, device_id: deviceId }),
    }),

  listModels: () => request<ModelInfo[]>("/models"),

  switchModel: (model: string) =>
    request("/models/switch", {
      method: "POST",
      body: JSON.stringify({ model }),
    }),

  listScenarios: () => request<Scenario[]>("/scenarios"),

  voiceStatus: () => request<VoiceStatus>("/voice/status"),
};

interface Device {
  device_id: string;
  model: string;
  status: string;
  connection_type: string;
}

interface TaskResponse {
  task_id: string;
  status: string;
  command: string;
  actions: Record<string, unknown>[];
  error?: string;
}

interface ModelInfo {
  name: string;
  size: string;
  active: boolean;
}

interface Scenario {
  name: string;
  description: string;
  steps: Record<string, unknown>[];
}

interface VoiceStatus {
  stt_available: boolean;
  tts_available: boolean;
  wake_word_active: boolean;
}
