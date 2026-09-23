"""Fictional data helpers. No host, filesystem, or network inspection occurs here."""
from random import choice, randint


def token(prefix: str, width: int = 4) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return f"{prefix}-" + "".join(choice(alphabet) for _ in range(width))


def session_snapshot() -> dict[str, str]:
    return {
        "session": token("BT", 5),
        "virtual_ip": f"10.{randint(60, 89)}.{randint(10, 99)}.{randint(10, 99)}",
        "node": f"VX-{randint(10, 99):02d}",
        "trace": token("TR", 4),
        "threat": f"TH-{randint(100, 999)}",
    }


def metric(low: int, high: int) -> str:
    return f"{randint(low, high)}%"


def nodes() -> list[tuple[str, int, int]]:
    names = ["NODE-01", "NODE-07", "NODE-13", "NODE-21", "NODE-42", "NODE-88"]
    positions = [(0.10, 0.30), (0.30, 0.15), (0.48, 0.42), (0.66, 0.20), (0.82, 0.48), (0.54, 0.78)]
    return [(name, int(x * 560), int(y * 260)) for name, (x, y) in zip(names, positions)]


def generated_key() -> str:
    return "SIM-" + "-".join(token("", 4).lstrip("-") for _ in range(3))


# Explicitly fictional UI copy used by the simulation.
FAKE_COMMANDS = [
    "> initialize --operation ZERO-DAY",
    "> generate-target --virtual",
    "> map-environment --simulation",
    "> analyze-surface --virtual",
    "> calculate-route --simulation",
    "> activate-nexus",
    "> run-countermeasure --test",
]

CALM_LOGS = [
    "Initializing operation...",
    "Establishing virtual session...",
    "Generating simulated target...",
    "Mapping virtual environment...",
    "Loading cognitive engine...",
    "Loading cryptographic module...",
    "Loading threat-analysis module...",
    "Loading visualization engine...",
    "Virtual telemetry synchronized.",
]

ESCALATION_LOGS = [
    "[!] ANOMALY DETECTED",
    "[!] VIRTUAL SECURITY LAYER RESPONDING",
    "[!] TRACE SIGNATURE GENERATED",
    "[!] COUNTERMEASURE PROTOCOL INITIALIZING...",
]

NEXUS_MESSAGES = [
    "Unusual activity pattern detected.",
    "Calculating simulated attack surface...",
    "Virtual vulnerability identified.",
    "Recommendation: Continue simulation.",
]

EASTER_EGGS = {
    "sudo coffee": ["Coffee level critically low.", "Human operator required.", "☕"],
    "whoami": ["You are...", "apparently very curious."],
    "hack nasa": ["Absolutely not. 😂", "SIMULATION MODE ONLY."],
}

if __name__ == "__main__":
    print(session_snapshot())
    print(generated_key())
    print(nodes())

