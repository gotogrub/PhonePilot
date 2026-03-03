import { useState, FormEvent } from "react";
import { api } from "../api/client";
import { useAppStore } from "../stores/appStore";

export function TaskInput() {
  const [command, setCommand] = useState("");
  const { selectedDevice, isExecuting, setExecuting, addAction } =
    useAppStore();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!command.trim() || isExecuting) return;

    const submittedCommand = command;
    setExecuting(true);
    setCommand("");
    addAction({
      step: -1,
      action: submittedCommand,
      result: "pending",
      timestamp: Date.now(),
    });
    try {
      const result = await api.executeTask(submittedCommand, selectedDevice ?? undefined);
      for (const action of result.actions) {
        addAction({
          step: (action as { step: number }).step,
          action: JSON.stringify(action),
          result: result.status,
          timestamp: Date.now(),
        });
      }
    } catch (err) {
      addAction({
        step: 0,
        action: submittedCommand,
        result: `Error: ${err}`,
        timestamp: Date.now(),
      });
    } finally {
      setExecuting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        placeholder="Enter command... e.g. 'Open Chrome'"
        disabled={isExecuting}
        className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-3
                   text-gray-100 placeholder-gray-500 focus:outline-none
                   focus:border-pilot-500 transition-colors disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={isExecuting || !command.trim()}
        className="px-6 py-3 bg-pilot-600 hover:bg-pilot-700 text-white
                   rounded-lg font-medium transition-colors disabled:opacity-50
                   disabled:cursor-not-allowed"
      >
        {isExecuting ? "Running..." : "Execute"}
      </button>
    </form>
  );
}
