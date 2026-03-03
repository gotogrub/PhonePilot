import { useDevice } from "../hooks/useDevice";

export function DeviceList() {
  const { devices, selectedDevice, setSelectedDevice } = useDevice();

  if (devices.length === 0) {
    return (
      <span className="text-sm text-gray-500">No devices connected</span>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-400">Device:</span>
      <select
        value={selectedDevice ?? ""}
        onChange={(e) => setSelectedDevice(e.target.value)}
        className="bg-gray-800 border border-gray-700 rounded-md px-3 py-1.5
                   text-sm text-gray-200 focus:outline-none focus:border-pilot-500"
      >
        {devices.map((d) => (
          <option key={d.device_id} value={d.device_id}>
            {d.model} ({d.connection_type})
          </option>
        ))}
      </select>
    </div>
  );
}
