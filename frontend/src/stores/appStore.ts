import { create } from "zustand";

export interface ActionEntry {
  step: number;
  actionType?: string;
  reasoning?: string;
  coordinates?: { x: number; y: number };
  text?: string;
  direction?: string;
  status: "success" | "error" | "skipped" | "pending";
  error?: string;
  label: string;
  timestamp: number;
}

interface Device {
  device_id: string;
  model: string;
  status: string;
  connection_type: string;
}

interface AppState {
  selectedDevice: string | null;
  devices: Device[];
  actions: ActionEntry[];
  isExecuting: boolean;
  currentFrame: string | null;
  abortController: AbortController | null;

  setSelectedDevice: (id: string | null) => void;
  setDevices: (devices: Device[]) => void;
  addAction: (action: ActionEntry) => void;
  clearActions: () => void;
  setExecuting: (value: boolean) => void;
  setCurrentFrame: (frame: string | null) => void;
  setAbortController: (ctrl: AbortController | null) => void;
  cancelTask: () => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  selectedDevice: null,
  devices: [],
  actions: [],
  isExecuting: false,
  currentFrame: null,
  abortController: null,

  setSelectedDevice: (id) => set({ selectedDevice: id }),
  setDevices: (devices) => set({ devices }),
  addAction: (action) =>
    set((state) => ({ actions: [...state.actions, action] })),
  clearActions: () => set({ actions: [] }),
  setExecuting: (value) => set({ isExecuting: value }),
  setCurrentFrame: (frame) => set({ currentFrame: frame }),
  setAbortController: (ctrl) => set({ abortController: ctrl }),
  cancelTask: () => {
    const ctrl = get().abortController;
    if (ctrl) ctrl.abort();
    set({ isExecuting: false, abortController: null });
  },
}));
