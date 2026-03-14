import { useState, FormEvent } from "react";
import { api } from "../api/client";
import { useAppStore } from "../stores/appStore";

function parseAction(raw: Record<string, unknown>): {
  actionType: string;
  reasoning: string;
  coords?: { x: number; y: number };
  text?: string;
  direction?: string;
  status: "success" | "error" | "skipped";
  error?: string;
} {
  const action = (raw.action ?? {}) as Record<string, unknown>;
  const result = (raw.result ?? {}) as Record<string, unknown>;
  const reasoning = (raw.reasoning as string) ?? "";
  const actionType = (action.action_type as string) ?? (action.skipped ? "skipped" : "unknown");
  const status = result.error ? "error" : result.status === "skipped" ? "skipped" : "success";

  return {
    actionType,
    reasoning,
    coords: action.x != null ? { x: action.x as number, y: action.y as number } : undefined,
    text: action.text as string | undefined,
    direction: action.direction as string | undefined,
    status,
    error: result.error as string | undefined,
  };
}

function formatLabel(p: ReturnType<typeof parseAction>): string {
  switch (p.actionType) {
    case "tap":
      return p.coords ? `Tap (${p.coords.x}, ${p.coords.y})` : "Tap";
    case "swipe":
      return `Swipe ${p.direction ?? "up"}${p.coords ? ` from (${p.coords.x}, ${p.coords.y})` : ""}`;
    case "type":
      return `Type "${p.text ?? ""}"`;
    case "back":
      return "Press Back";
    case "home":
      return "Press Home";
    case "wait":
      return "Wait";
    case "skipped":
      return "Skipped";
    default:
      return p.actionType;
  }
}

export function TaskInput() {
  const [command, setCommand] = useState("");
  const {
    selectedDevice,
    isExecuting,
    setExecuting,
    addAction,
    setAbortController,
    cancelTask,
  } = useAppStore();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!command.trim() || isExecuting) return;

    const submittedCommand = command;
    const controller = new AbortController();
    setAbortController(controller);
    setExecuting(true);
    setCommand("");
    addAction({
      step: -1,
      label: submittedCommand,
      status: "pending",
      timestamp: Date.now(),
    });
    try {
      const result = await api.executeTask(
        submittedCommand,
        selectedDevice ?? undefined,
        controller.signal,
      );
      for (const raw of result.actions) {
        const parsed = parseAction(raw);
        addAction({
          step: (raw as { step: number }).step,
          actionType: parsed.actionType,
          reasoning: parsed.reasoning,
          coordinates: parsed.coords,
          text: parsed.text,
          direction: parsed.direction,
          status: parsed.status,
          error: parsed.error,
          label: formatLabel(parsed),
          timestamp: Date.now(),
        });
      }
      addAction({
        step: -2,
        label: result.status === "completed" ? "Task completed" : "Task finished",
        status: result.error ? "error" : "success",
        error: result.error ?? undefined,
        timestamp: Date.now(),
      });
    } catch (err) {
      if ((err as Error).name === "AbortError") {
        addAction({
          step: -2,
          label: "Task cancelled",
          status: "error",
          timestamp: Date.now(),
        });
      } else {
        addAction({
          step: -2,
          label: `Error: ${err}`,
          status: "error",
          timestamp: Date.now(),
        });
      }
    } finally {
      setExecuting(false);
      setAbortController(null);
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
      {isExecuting ? (
        <button
          type="button"
          onClick={cancelTask}
          className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white
                     rounded-lg font-medium transition-colors"
        >
          Cancel
        </button>
      ) : (
        <button
          type="submit"
          disabled={!command.trim()}
          className="px-6 py-3 bg-pilot-600 hover:bg-pilot-700 text-white
                     rounded-lg font-medium transition-colors disabled:opacity-50
                     disabled:cursor-not-allowed"
        >
          Execute
        </button>
      )}
    </form>
  );
}
