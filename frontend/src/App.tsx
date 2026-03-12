import { DeviceScreen } from "./components/DeviceScreen";
import { TaskInput } from "./components/TaskInput";
import { ActionLog } from "./components/ActionLog";
import { DeviceList } from "./components/DeviceList";
import { useAppStore } from "./stores/appStore";

function App() {
  const { selectedDevice } = useAppStore();

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-gray-800 px-6 py-4">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold text-pilot-400">PhonePilot</h1>
          <DeviceList />
        </div>
      </header>

      <main className="flex-1 flex max-w-7xl mx-auto w-full p-6 gap-6">
        <section className="flex-shrink-0 w-80">
          <DeviceScreen deviceId={selectedDevice} />
        </section>

        <section className="flex-1 flex flex-col gap-4">
          <TaskInput />
          <ActionLog />
        </section>
      </main>
    </div>
  );
}

export default App;
