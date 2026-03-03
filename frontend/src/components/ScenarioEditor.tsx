import { useState } from "react";

interface Step {
  action: string;
  target: string;
  value: string;
}

export function ScenarioEditor() {
  const [name, setName] = useState("");
  const [steps, setSteps] = useState<Step[]>([]);

  const addStep = () => {
    setSteps([...steps, { action: "tap", target: "", value: "" }]);
  };

  const removeStep = (index: number) => {
    setSteps(steps.filter((_, i) => i !== index));
  };

  const updateStep = (index: number, field: keyof Step, value: string) => {
    const updated = [...steps];
    updated[index] = { ...updated[index], [field]: value };
    setSteps(updated);
  };

  return (
    <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
      <h3 className="text-lg font-medium mb-4">Scenario Editor</h3>

      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Scenario name"
        className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2
                   text-sm mb-4 focus:outline-none focus:border-pilot-500"
      />

      <div className="space-y-2 mb-4">
        {steps.map((step, i) => (
          <div key={i} className="flex gap-2 items-center">
            <select
              value={step.action}
              onChange={(e) => updateStep(i, "action", e.target.value)}
              className="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-sm"
            >
              <option value="tap">Tap</option>
              <option value="swipe">Swipe</option>
              <option value="type">Type</option>
              <option value="wait">Wait</option>
              <option value="open">Open App</option>
            </select>
            <input
              value={step.target}
              onChange={(e) => updateStep(i, "target", e.target.value)}
              placeholder="Target"
              className="flex-1 bg-gray-800 border border-gray-700 rounded px-2 py-1 text-sm"
            />
            <button
              onClick={() => removeStep(i)}
              className="text-red-400 hover:text-red-300 text-sm px-2"
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      <button
        onClick={addStep}
        className="text-sm text-pilot-400 hover:text-pilot-300"
      >
        + Add Step
      </button>
    </div>
  );
}
