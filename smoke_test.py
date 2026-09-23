from simulation.engine import build_scenario
from simulation.fake_data import EASTER_EGGS, nodes, session_snapshot

scenario = build_scenario()
assert scenario[-1].kind == "second_reveal"
assert len(nodes()) == 6
assert set(("session", "virtual_ip", "node", "trace", "threat")) <= session_snapshot().keys()
assert all(key in EASTER_EGGS for key in ("sudo coffee", "whoami", "hack nasa"))
print(f"smoke test: OK ({len(scenario)} scheduled visual events)")
