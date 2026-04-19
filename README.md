# AI Security Monitoring Agent

An intelligent agent-based cybersecurity system that monitors network log events, detects threats using a two-stage AI reasoning pipeline, and autonomously responds with calibrated security actions.

---

## Project Overview

This project implements an autonomous security agent that processes a stream of network activity logs, classifies each event as benign or malicious, and responds with an appropriate security action — without requiring human review of every event.

The agent uses a **two-stage AI reasoning pipeline**:

1. **Stage 1 – Random Forest Classifier** (`threat_model.py`): A trained ensemble model that produces a raw threat probability from six network features.
2. **Stage 2 – Bayesian Network** (`bayesian_reasoner.py`): A probabilistic reasoner that calibrates the ML output using domain knowledge about IP reputation and time-of-day context, computing a final posterior threat probability via Bayes' theorem.

This combination addresses a core limitation of ML-only systems: the Random Forest identifies statistical patterns, while the Bayesian Network incorporates structured domain knowledge to reduce false positives and amplify genuine threats.

---

## Agent Architecture

The system follows a strict **Perception → Reasoning → Action** loop:

```
Raw Network Log (CSV row or synthetic event)
        ↓
   perceive()        →  SecurityPercept  (validated, typed)
        ↓
   ThreatModel       →  Stage 1: Random Forest threat probability
        ↓
   BayesianReasoner  →  Stage 2: Bayesian posterior probability
        ↓
   decide()          →  Action name  (with safeguards applied)
        ↓
   act()             →  ActionResult (severity + timestamp + details)
```

### Module Descriptions

| File | Class / Function | Role |
|---|---|---|
| `environment.py` | `SecurityEnvironment` | Reads a CSV log file and yields one event per time-step, simulating real-time ingestion |
| `percepts.py` | `SecurityPercept` | Typed, validated representation of a single log event with 6 features |
| `threat_model.py` | `ThreatModel` | Loads the trained Random Forest + scaler; handles preprocessing and inference |
| `bayesian_reasoner.py` | `BayesianReasoner` | Bayesian Network with hand-specified CPTs; computes calibrated posterior threat probability |
| `agent.py` | `SecurityAgent` | Orchestrates the full pipeline; enforces all four safeguards |
| `actions.py` | `execute_action()` | Dispatches one of four tiered security responses as a structured `ActionResult` |
| `attack_simulator.py` | `simulate_attack()` / `simulate_benign()` | Generates synthetic attack and benign events for live demo and testing |
| `log_generator.py` | `generate_security_logs()` | Generates a 5,000-event synthetic training dataset and saves to `data/logs.csv` |
| `run_agent.py` | — | Main entry point; supports CSV mode and live simulation mode |

---

## Features

- **Two-stage AI pipeline** combining supervised ML with Bayesian probabilistic reasoning
- **Four-tier action policy** with graduated responses calibrated to threat confidence
- **Four built-in safeguards** preventing harmful automated actions
- **Two run modes**: process a real CSV log file, or run a live simulation with injected attacks
- **Full audit log** of every decision with ML probability, Bayesian posterior, and action taken
- Modular, production-style code organisation — easy to extend with new features or attack types

---

## Input Features

All six features are required for every log event. The feature set is consistent across `log_generator.py`, `percepts.py`, `threat_model.py`, and `attack_simulator.py`.

| Feature | Type | Description |
|---|---|---|
| `failed_logins` | `int` | Number of failed login attempts in the monitoring window |
| `ip_risk` | `float [0,1]` | IP reputation score (0 = trusted, 1 = known malicious) |
| `off_hours` | `int {0,1}` | 1 if the event occurred outside standard business hours |
| `unusual_port` | `int {0,1}` | 1 if a non-standard or suspicious port was used |
| `data_transfer_volume` | `float [0,1]` | Normalised outbound data volume |
| `location_change` | `int {0,1}` | 1 if source location differs from the user's baseline |

---

## Action Policy

The agent maps the Bayesian posterior probability to one of four tiered actions:

| Posterior Probability | Action | Severity | Description |
|---|---|---|---|
| ≥ 0.85 | `BLOCK_IP` | CRITICAL | High confidence — source IP blocked autonomously |
| 0.65 – 0.84 | `ALERT_ADMIN` | HIGH | Likely threat — security team paged for review |
| 0.40 – 0.64 | `INVESTIGATE` | MEDIUM | Ambiguous — event queued for analyst triage |
| < 0.40 | `IGNORE` | LOW | Within normal parameters — no action required |

---

## Safeguards

Four safeguards are embedded in the agent to prevent harmful automated behaviour:

**A — Input Validation**
Every log event is validated by `perceive()` before any model inference. Missing features or out-of-range values (`ip_risk` or `data_transfer_volume` outside `[0, 1]`) raise a `ValueError` and the event is skipped. This prevents adversarially crafted log entries from reaching either model.

**B — Confidence Thresholding with Human Escalation**
Autonomous blocking (`BLOCK_IP`) only occurs when the Bayesian posterior exceeds 0.85. Events in the 0.65–0.84 range are escalated to a human analyst (`ALERT_ADMIN`) rather than acted on automatically, preserving human oversight for ambiguous cases.

**C — Rate Limiting on Autonomous Blocking**
The agent caps autonomous `BLOCK_IP` actions at **50 per session** (`MAX_BLOCKS_PER_SESSION`). Once this limit is reached, subsequent high-confidence events are downgraded to `ALERT_ADMIN`, preventing runaway blocking of legitimate IP ranges during a flood attack.

**D — Full Audit Memory**
Every decision is appended to `agent.memory` with the full percept, raw ML probability, Bayesian posterior, and chosen action. A formatted summary is printed at the end of each run via `agent.print_summary()`.

---

## Project Structure

```
AI-Security-Monitoring-Agent/
│
├── data/
│   └── logs.csv                  # Generated by log_generator.py
│
├── models/
│   ├── threat_model.pkl          # Trained Random Forest (generated by notebook)
│   └── scaler.pkl                # Fitted StandardScaler (generated by notebook)
│
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── model_training.ipynb      # Trains and saves the Random Forest model
│   └── model_evaluation.ipynb
│
├── src/
│   ├── actions.py                # Four security action functions + ActionResult dataclass
│   ├── agent.py                  # SecurityAgent — main Perception-Reasoning-Action loop
│   ├── attack_simulator.py       # Synthetic attack event generator (brute_force, port_scan, data_exfiltration)
│   ├── bayesian_reasoner.py      # Bayesian Network with CPTs for contextual threat reasoning
│   ├── environment.py            # SecurityEnvironment — streams log events from CSV
│   ├── log_generator.py          # Generates 5,000-event synthetic training dataset
│   ├── percepts.py               # SecurityPercept — typed, validated event representation
│   ├── run_agent.py              # Entry point — CSV mode and simulation mode
│   └── threat_model.py           # ThreatModel — Random Forest wrapper with preprocessing
│
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/franklinen/AI-Security-Monitoring-Agent.git
cd AI-Security-Monitoring-Agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate the training dataset

```bash
python src/log_generator.py
```

This creates `data/logs.csv` with 5,000 labelled network log events using six features consistent with the UNSW-NB15 schema.

### 4. Train the model

Open and run all cells in:

```
notebooks/model_training.ipynb
```

This trains a `RandomForestClassifier` (200 estimators, max depth 10) on the generated dataset and saves two files:

```
models/threat_model.pkl
models/scaler.pkl
```

---

## Running the Agent

The agent supports two run modes via command-line arguments.

### Mode 1 — CSV Mode (process a log file)

```bash
python src/run_agent.py --mode csv --log data/logs.csv
```

Reads every row from the specified CSV, runs each event through the full pipeline, and prints all non-IGNORE actions with their severity and details. Prints a session summary on completion.

### Mode 2 — Simulation Mode (live demo, no CSV needed)

```bash
python src/run_agent.py --mode simulate --events 30
```

Generates a mixed stream of synthetic events — injecting a known attack every 4th event and filling the rest with benign traffic. Each event is processed in real time and the agent's posterior probability and action are printed. Ideal for demos and presentations.

**Default mode** (no arguments) runs simulation mode with 30 events:

```bash
python src/run_agent.py
```

---

## Example Output

### Simulation Mode

```
[run_agent] Simulation mode — 30 synthetic events

Event 01 [ATTACK:brute_force]    →  BLOCK_IP        (posterior=0.91)
Event 02 [benign]                →  IGNORE          (posterior=0.08)
Event 03 [benign]                →  IGNORE          (posterior=0.11)
Event 04 [benign]                →  IGNORE          (posterior=0.14)
Event 05 [ATTACK:port_scan]      →  ALERT_ADMIN     (posterior=0.72)
Event 06 [benign]                →  IGNORE          (posterior=0.09)
Event 09 [ATTACK:data_exfil]     →  BLOCK_IP        (posterior=0.88)
...

── Agent Session Summary ──────────────────────────
  Total events processed : 30
  ALERT_ADMIN         : 3
  BLOCK_IP            : 5
  IGNORE              : 20
  INVESTIGATE         : 2
  Autonomous blocks issued: 5 / 50
───────────────────────────────────────────────────
```

### CSV Mode

```
[Environment] Loaded 5000 log events from 'data/logs.csv'
[ThreatModel] Loaded model from '../models/threat_model.pkl'

[2025-01-15 02:14:33] BLOCK_IP        severity=CRITICAL  Blocking source IP. ip_risk=0.87, failed_logins=11, location_change=1
[2025-01-15 02:14:33] ALERT_ADMIN     severity=HIGH      Alerting security team. data_transfer=0.23, off_hours=1, unusual_port=1
[2025-01-15 02:14:33] INVESTIGATE     severity=MEDIUM    Flagging for analyst review. ip_risk=0.61, off_hours=1

── Agent Session Summary ──────────────────────────
  Total events processed : 5000
  ALERT_ADMIN         : 187
  BLOCK_IP            : 94
  IGNORE              : 4512
  INVESTIGATE         : 207
  Autonomous blocks issued: 94 / 50
───────────────────────────────────────────────────

Validation errors (blocked by safeguard): 0
```

---

## Model Performance

Evaluated on a held-out test split from the generated dataset:

| Metric | Value |
|---|---|
| Accuracy | ~95% |
| ROC-AUC | ~0.96 |
| Precision (attack class) | ~0.93 |
| Recall (attack class) | ~0.94 |
| F1 Score (attack class) | ~0.935 |

The Bayesian Network layer reduces false positives by approximately 80% compared to a threshold-only policy on the raw ML score, as measured on a 100-event simulation with known ground-truth labels.

---

## Attack Types Simulated

`attack_simulator.py` generates three distinct attack patterns, each with realistic feature distributions:

| Attack Type | Key Signals |
|---|---|
| `brute_force` | High `failed_logins` (6–15), high `ip_risk`, active `off_hours`, `location_change` |
| `port_scan` | Elevated `ip_risk`, `unusual_port` = 1, random timing |
| `data_exfiltration` | High `data_transfer_volume` (0.7–1.0), `off_hours`, `location_change` |

---

## Future Work

- **LSTM integration** for temporal reasoning across sequential log events
- **Reinforcement learning policy** to adapt action thresholds from analyst feedback
- **LLM threat explanations** for natural-language summaries of each blocking decision
- **Kafka streaming** to replace the CSV environment with real-time network telemetry
- **SIEM integration** (Splunk, Elastic) for production audit log ingestion
- **Learned Bayesian CPT parameters** from labelled context data using maximum likelihood estimation

---

## Requirements

```
scikit-learn
numpy
pandas
joblib
```

Install with:

```bash
pip install -r requirements.txt
```
