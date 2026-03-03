import { useAppStore } from "../stores/appStore";

export function ActionLog() {
  const { actions, clearActions } = useAppStore();

  return (
    <div className="flex-1 bg-gray-900 rounded-xl border border-gray-800 flex flex-col">
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800">
        <span className="text-sm text-gray-400">Action Log</span>
        {actions.length > 0 && (
          <button
            onClick={clearActions}
            className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
          >
            Clear
          </button>
        )}
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {actions.length === 0 ? (
          <p className="text-gray-600 text-sm text-center py-8">
            No actions yet. Enter a command to get started.
          </p>
        ) : (
          actions.map((entry, i) =>
            entry.step === -1 ? (
              <div
                key={i}
                className="text-sm bg-gray-800 rounded-lg px-3 py-2 mt-2 first:mt-0"
              >
                <div className="text-pilot-400 font-medium">&gt; {entry.action}</div>
                <div className="text-gray-500 text-xs mt-1">
                  {new Date(entry.timestamp).toLocaleTimeString()}
                </div>
              </div>
            ) : (
              <div
                key={i}
                className="text-sm border-l-2 border-pilot-600 pl-3 py-1"
              >
                <div className="text-gray-300 font-mono">{entry.action}</div>
                <div className="text-gray-500 text-xs mt-1">
                  {entry.result} &middot;{" "}
                  {new Date(entry.timestamp).toLocaleTimeString()}
                </div>
              </div>
            )
          )
        )}
      </div>
    </div>
  );
}
