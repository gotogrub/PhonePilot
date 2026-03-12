from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RecordedStep:
    action: str
    target: str | None = None
    value: str | None = None
    timestamp: float = 0.0
    screenshot_before: str | None = None
    screenshot_after: str | None = None


@dataclass
class Recording:
    name: str
    steps: list[RecordedStep] = field(default_factory=list)
    started_at: datetime | None = None
    finished_at: datetime | None = None


class ScenarioRecorder:
    def __init__(self):
        self._recording: Recording | None = None
        self._is_recording = False

    def start(self, name: str):
        self._recording = Recording(name=name, started_at=datetime.now())
        self._is_recording = True

    def add_step(self, step: RecordedStep):
        if self._is_recording and self._recording:
            self._recording.steps.append(step)

    def stop(self) -> Recording | None:
        self._is_recording = False
        if self._recording:
            self._recording.finished_at = datetime.now()
        return self._recording

    @property
    def is_recording(self) -> bool:
        return self._is_recording
