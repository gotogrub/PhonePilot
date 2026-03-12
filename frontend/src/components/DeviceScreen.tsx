import { useCallback } from "react";
import { useWebSocket } from "../hooks/useWebSocket";
import { useAppStore } from "../stores/appStore";

interface Props {
  deviceId: string | null;
}

export function DeviceScreen({ deviceId }: Props) {
  const { currentFrame, setCurrentFrame } = useAppStore();

  const wsUrl = deviceId
    ? `ws://${window.location.host}/stream/${deviceId}`
    : null;

  const onMessage = useCallback(
    (data: unknown) => {
      const msg = data as { type: string; data: string };
      if (msg.type === "frame") {
        setCurrentFrame(msg.data);
      }
    },
    [setCurrentFrame]
  );

  useWebSocket(wsUrl, { onMessage });

  return (
    <div className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
      <div className="px-4 py-2 border-b border-gray-800 text-sm text-gray-400">
        {deviceId ?? "No device"}
      </div>
      <div className="aspect-[9/19.5] bg-black flex items-center justify-center">
        {currentFrame ? (
          <img
            src={`data:image/png;base64,${currentFrame}`}
            alt="Device screen"
            className="w-full h-full object-contain"
          />
        ) : (
          <span className="text-gray-600 text-sm">No signal</span>
        )}
      </div>
    </div>
  );
}
