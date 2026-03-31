"""
run_agent.py – Main entry point for the AI Security Monitoring Agent.

USAGE
-----
  # Mode 1: process a CSV log file
  python src/run_agent.py --mode csv --log data/logs.csv

  # Mode 2: live simulation with injected attacks (no CSV needed)
  python src/run_agent.py --mode simulate --events 30

AGENT PIPELINE (per event)
--------------------------
  Raw log event
      ↓  perceive()     → SecurityPercept (validated, typed)
      ↓  ThreatModel    → Stage 1: Random Forest threat probability
      ↓  BayesianReasoner→ Stage 2: Bayesian posterior (calibrated)
      ↓  decide()       → action name (with safeguards)
      ↓  act()          → ActionResult (structured response)
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from environment import SecurityEnvironment
from threat_model import ThreatModel
from agent import SecurityAgent
from attack_simulator import simulate_attack, simulate_benign


def run_csv_mode(log_path: str):
    """Process all events from a CSV log file."""
    print(f"\n[run_agent] CSV mode — processing '{log_path}'\n")

    env   = SecurityEnvironment(log_path)
    model = ThreatModel()
    agent = SecurityAgent(model)

    processed = 0
    errors    = 0

    while True:
        event = env.get_event()
        if event is None:
            break

        try:
            percept     = agent.perceive(event)
            action_name = agent.decide(percept)
            result      = agent.act(action_name, percept)

            # Only print non-IGNORE actions to reduce noise
            if action_name != "IGNORE":
                print(
                    f"[{result.timestamp}] {result.action_name:<15} "
                    f"severity={result.severity:<8}  {result.details}"
                )
            processed += 1

        except ValueError as e:
            print(f"[SAFEGUARD] Skipping event: {e}")
            errors += 1

    agent.print_summary()
    print(f"Validation errors (blocked by safeguard): {errors}")


def run_simulation_mode(n_events: int = 30):
    """
    Run a live simulation mixing normal traffic with injected attacks.
    Useful for demonstrating the agent without a CSV file.
    """
    print(f"\n[run_agent] Simulation mode — {n_events} synthetic events\n")

    model = ThreatModel()
    agent = SecurityAgent(model)

    import numpy as np
    np.random.seed(0)

    for i in range(n_events):
        # Inject an attack every ~4 events; rest is benign traffic
        event = simulate_attack() if i % 4 == 0 else simulate_benign()
        attack_label = event.get("attack_type", "none")

        try:
            percept     = agent.perceive(event)
            action_name = agent.decide(percept)
            result      = agent.act(action_name, percept)

            tag = f"[ATTACK:{attack_label}]" if attack_label != "none" else "[benign]       "
            print(
                f"Event {i+1:02d} {tag}  →  {result.action_name:<15} "
                f"(posterior={agent.memory[-1]['posterior']:.2f})"
            )

        except ValueError as e:
            print(f"[SAFEGUARD] Event {i+1:02d}: {e}")

    agent.print_summary()


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Security Monitoring Agent")
    parser.add_argument(
        "--mode", choices=["csv", "simulate"], default="simulate",
        help="Run mode: 'csv' reads a log file, 'simulate' uses synthetic events"
    )
    parser.add_argument(
        "--log", default="data/logs.csv",
        help="Path to CSV log file (csv mode only)"
    )
    parser.add_argument(
        "--events", type=int, default=30,
        help="Number of synthetic events to generate (simulate mode only)"
    )

    args = parser.parse_args()

    if args.mode == "csv":
        run_csv_mode(args.log)
    else:
        run_simulation_mode(args.events)
