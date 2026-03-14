import { useAppStore, ActionEntry } from "../stores/appStore";

const STATUS_STYLES = {
  success: "border-green-600",
  error: "border-red-500",
  skipped: "border-yellow-600",
  pending: "border-gray-600",
};

const STATUS_DOT = {
  success: "bg-green-500",
  error: "bg-red-500",
  skipped: "bg-yellow-500",
  pending: "bg-gray-500",
};

function ActionItem({ entry }: { entry: ActionEntry }) {
  if (entry.step === -1) {
    return (
      <div className="text-sm bg-gray-800 rounded-lg px-3 py-2 mt-3 first:mt-0">
        <div className="text-pilot-400 font-medium">&gt; {entry.label}</div>
        <div className="text-gray-500 text-xs mt-1">
          {new Date(entry.timestamp).toLocaleTimeString()}
        </div>
      </div>
    );
  }

  if (entry.step === -2) {
    return (
      <div
        className={`text-sm rounded-lg px-3 py-2 mt-1 ${
          entry.status === "error"
            ? "bg-red-950/50 text-red-400"
            : "bg-green-950/50 text-green-400"
        }`}
      >
        {entry.label}
        {entry.error && (
          <span className="text-red-500 ml-2 text-xs">{entry.error}</span>
        )}
      </div>
    );
  }

  return (
    <div
      className={`text-sm border-l-2 ${STATUS_STYLES[entry.status]} pl-3 py-1.5`}
    >
      <div className="flex items-center gap-2">
        <span
          className={`w-1.5 h-1.5 rounded-full ${STATUS_DOT[entry.status]}`}
        />
        <span className="text-gray-200 font-medium">{entry.label}</span>
        <span className="text-gray-600 text-xs">step {entry.step}</span>
      </div>
      {entry.reasoning && (
        <div className="text-gray-500 text-xs mt-0.5 ml-3.5 italic">
          {entry.reasoning}
        </div>
      )}
      {entry.error && (
        <div className="text-red-400 text-xs mt-0.5 ml-3.5">
          {entry.error}
        </div>
      )}
      <div className="text-gray-600 text-xs mt-0.5 ml-3.5">
        {new Date(entry.timestamp).toLocaleTimeString()}
      </div>
    </div>
  );
}

function LoadingIndicator() {
  return (
    <div className="flex items-center gap-2 text-sm text-pilot-400 px-3 py-2">
      <div className="flex gap-1">
        <span className="w-1.5 h-1.5 bg-pilot-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
        <span className="w-1.5 h-1.5 bg-pilot-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
        <span className="w-1.5 h-1.5 bg-pilot-400 rounded-full animate-bounce" />
      </div>
      <span>Agent is thinking...</span>
    </div>
  );
}

export function ActionLog() {
  const { actions, clearActions, isExecuting } = useAppStore();

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
      <div className="flex-1 overflow-y-auto p-4 space-y-1">
        {actions.length === 0 && !isExecuting ? (
          <p className="text-gray-600 text-sm text-center py-8">
            No actions yet. Enter a command to get started.
          </p>
        ) : (
          <>
            {actions.map((entry, i) => (
              <ActionItem key={i} entry={entry} />
            ))}
            {isExecuting && <LoadingIndicator />}
          </>
        )}
      </div>
    </div>
  );
}
