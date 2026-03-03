import { create } from "zustand";

interface ActionEntry {
  step: number;
  action: string;
  result: string;
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

  setSelectedDevice: (id: string | null) => void;
  setDevices: (devices: Device[]) => void;
  addAction: (action: ActionEntry) => void;
  clearActions: () => void;
  setExecuting: (value: boolean) => void;
  setCurrentFrame: (frame: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  selectedDevice: null,
  devices: [],
  actions: [],
  isExecuting: false,
  currentFrame: null,

  setSelectedDevice: (id) => set({ selectedDevice: id }),
  setDevices: (devices) => set({ devices }),
  addAction: (action) =>
    set((state) => ({ actions: [...state.actions, action] })),
  clearActions: () => set({ actions: [] }),
  setExecuting: (value) => set({ isExecuting: value }),
  setCurrentFrame: (frame) => set({ currentFrame: frame }),
}));
