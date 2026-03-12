import { useEffect } from "react";
import { api } from "../api/client";
import { useAppStore } from "../stores/appStore";

export function useDevice() {
  const { devices, selectedDevice, setDevices, setSelectedDevice } =
    useAppStore();

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const result = await api.listDevices();
        setDevices(result);
        if (!selectedDevice && result.length > 0) {
          setSelectedDevice(result[0].device_id);
        }
      } catch {
        setDevices([]);
      }
    };

    fetchDevices();
    const interval = setInterval(fetchDevices, 5000);
    return () => clearInterval(interval);
  }, [selectedDevice, setDevices, setSelectedDevice]);

  return { devices, selectedDevice, setSelectedDevice };
}
