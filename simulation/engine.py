"""Event-driven, local-only scenario engine for BLACKTRACE."""
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Event:
    delay_ms: int
    kind: str
    payload: object = None


class SimulationEngine:
    """Schedules visual events; it never executes commands or touches the OS."""

    def __init__(self, emit: Callable[[str, object], None]):
        self.emit = emit
        self.events: list[Event] = []
        self.index = 0
        self.paused = False
        self.running = False
        self.fast = False
        self._after_id: Optional[str] = None

    def load(self, events: list[Event]) -> None:
        self.stop()
        self.events = events
        self.index = 0
        self.paused = False

    def start(self) -> None:
        self.running = True
        self._schedule_next(80)

    def stop(self) -> None:
        self.running = False
        self.paused = False
        self._after_id = None

    def toggle_pause(self) -> bool:
        self.paused = not self.paused
        if self.running and not self.paused:
            self._schedule_next(80)
        return self.paused

    def accelerate(self) -> None:
        self.fast = True

    def _schedule_next(self, delay: int | None = None) -> None:
        if not self.running or self.paused or self.index >= len(self.events):
            if self.index >= len(self.events):
                self.running = False
            return
        event = self.events[self.index]
        self.index += 1
        # Tk's after is injected by the UI to keep this engine toolkit-agnostic.
        self.emit("schedule", (max(1, delay if delay is not None else (80 if self.fast else event.delay_ms)), event))

    def on_event_complete(self) -> None:
        self._schedule_next()


def build_scenario() -> list[Event]:
    events: list[Event] = [
        Event(450, "intro", "BLACKTRACE"),
        Event(1100, "intro", "ADVANCED CYBER OPERATIONS PLATFORM"),
        Event(700, "intro", "INITIALIZING..."),
        Event(700, "intro", "OPERATION: ZERO-DAY\\nMODE: SIMULATION\\nSECURITY LEVEL: OMEGA"),
        Event(900, "phase", "dashboard"),
    ]
    for line in [
        "Initializing operation...", "Establishing virtual session...", "Generating simulated target...",
        "Mapping virtual environment...", "Loading cognitive engine...", "Loading cryptographic module...",
        "Loading threat-analysis module...", "Loading visualization engine...", "Virtual telemetry synchronized.",
    ]:
        events.append(Event(520, "log", line))
    events += [
        Event(800, "nexus", "Unusual activity pattern detected."),
        Event(800, "nexus", "Calculating simulated attack surface..."),
        Event(800, "nexus", "Virtual vulnerability identified."),
        Event(800, "nexus", "Recommendation: Continue simulation."),
        Event(900, "log", "[!] ANOMALY DETECTED"),
        Event(800, "status", "UNKNOWN"),
        Event(1000, "log", "[!] VIRTUAL SECURITY LAYER RESPONDING"),
        Event(800, "status", "DETECTED"),
        Event(900, "countermeasure", 12), Event(450, "countermeasure", 27), Event(450, "countermeasure", 41),
        Event(450, "countermeasure", 68), Event(450, "countermeasure", 83), Event(450, "countermeasure", 97),
        Event(700, "countermeasure", 99), Event(2200, "trace", None), Event(1200, "failure", None),
        Event(1200, "reveal", None), Event(3000, "second_reveal", None),
    ]
    return events
