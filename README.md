# AI-Security-Monitoring-Agent

This project implements an intelligent agent that monitors security logs and learns to detect suspicious activity.

## Project Motivation

Modern organizations generate massive volumes of security logs from authentication systems, network devices, and application servers. Security analysts are often overwhelmed by the number of alerts and events they must review, making it difficult to detect genuine threats quickly. As cyberattacks become more sophisticated, there is increasing demand for automated systems capable of monitoring system activity and identifying suspicious behavior in real time.

This project explores how Agentic AI techniques can be used to develop an intelligent monitoring system that learns to detect malicious activity from streaming security logs. Instead of relying solely on static rule-based detection systems, the agent continuously learns from observed events and feedback signals to improve its decision-making over time.

The goal of this project is to design and evaluate an adaptive security monitoring agent that can:

Analyze system activity logs

Detect suspicious behaviors such as brute-force attacks or data exfiltration

Learn optimal detection policies through interaction with an environment

Balance false positives and missed threats through a reward-driven learning strategy

This project demonstrates how intelligent agents and reinforcement learning concepts can be applied to cybersecurity monitoring systems.

## Agent Design

The system is designed using a reinforcement learning agent framework, where an intelligent agent interacts with a simulated security environment.
### Environment: 
The environment generates security log events representing user activities within a system. Each event contains behavioral indicators such as authentication attempts, network activity, and abnormal system usage patterns. 

### State Representation:

Each log event is represented as a feature vector describing system activity:

failed_logins – number of failed authentication attempts

ip_risk – reputation score of the originating IP address

off_hours – whether the event occurred outside normal operating hours

unusual_port – indicator of unusual port access

data_transfer_volume – normalized volume of data transferred

location_change – whether login location differs from previous login

These features represent the state observed by the agent.

### Actions:  
- 0 = Allow activity  
- 1 = Flag activity

### Reward Function:
The reward system reflects the operational priorities of security monitoring systems.
- True Positive = +10
- True Negative = +2
- False Positive = -3
- False Negative = -10

This reward structure penalizes missed attacks more heavily than false alarms, reflecting real-world cybersecurity risk management

## Cyberattack Simulation

To evaluate the agent's ability to detect malicious activity, the environment includes a cyberattack simulator that generates realistic threat scenarios.

Three common attack patterns are modeled:

### Brute Force Attack

An attacker repeatedly attempts to guess login credentials.

Typical characteristics:

- High number of failed login attempts

- High IP risk score

- Often occurs outside normal hours

- Login attempts from new geographic locations

### Port Scanning

An attacker probes network services to identify vulnerabilities.

Typical characteristics:

Unusual port access

Suspicious IP reputation

Moderate login anomalies

Elevated network activity

### Data Exfiltration

An attacker attempts to steal sensitive information.

Typical characteristics:

Large data transfer volumes

Off-hours activity

New login location

Moderate IP risk

The simulator mixes normal system activity and attack scenarios, producing a realistic dataset for training and evaluating the security monitoring agent.

## Learning Strategy

The project evaluates several agent strategies to demonstrate the effectiveness of adaptive learning in security monitoring.

### Random Baseline Agent

The baseline agent randomly classifies events as normal or suspicious. This provides a reference point for evaluating intelligent agents.

Expected performance: approximately random classification.

### Epsilon-Greedy Contextual Bandit Agent

The primary learning agent uses an epsilon-greedy contextual bandit strategy.

The agent learns a policy that maps security event features to actions.

Key properties:

- Exploration: occasionally tests new actions

- Exploitation: favors actions with historically higher rewards

- Online learning: continuously updates policy during interaction

This approach allows the agent to gradually improve its detection performance.

### Upper Confidence Bound (UCB) Agent

A second intelligent agent uses the Upper Confidence Bound (UCB) strategy.

This algorithm balances exploration and exploitation by selecting actions based on both:

expected reward

uncertainty of previous observations

The UCB agent tends to explore more systematically than the epsilon-greedy strategy.

## Evaluation Results

Agent performance is evaluated using several metrics commonly used in security monitoring systems.

Classification Metrics

The following metrics are computed:

- Accuracy – overall classification correctness

- Precision – proportion of flagged events that were actual attacks

- Recall (Detection Rate) – proportion of attacks successfully detected

High recall is particularly important for cybersecurity applications.

### Confusion Matrix

A confusion matrix is generated to visualize classification performance:

- True Positives (attacks correctly flagged)

- True Negatives (normal events correctly allowed)

- False Positives (false alarms)

- False Negatives (missed attacks)

### Learning Curve

The agent's cumulative reward is plotted over time to show learning progress.

An improving reward curve indicates that the agent is learning better security detection policies.

### Agent Comparison

Performance is compared across agents:

Agent	Expected Behavior
Random Agent	No learning, random detection
Bandit Agent	Learns detection policy
UCB Agent	More structured exploration

The intelligent agents demonstrate significantly improved detection performance compared to the baseline.

## Future Work

This project can be extended in several directions to build more advanced security monitoring systems.

### Integration with Real Security Datasets

Future work could incorporate real-world intrusion detection datasets such as:

UNSW-NB15

NSL-KDD

CICIDS datasets

This would allow the agent to be trained on realistic network traffic data.

### Streaming Security Monitoring

The system could be extended to process real-time log streams, enabling deployment as a live monitoring tool.

### Multi-Agent Security Systems

Multiple agents could collaborate to detect different categories of threats, including:

- network intrusion detection

- insider threat detection

- malware activity monitoring

### LLM-Powered Security Analysis

Large language models could be integrated to analyze unstructured log messages and assist the agent in identifying complex attack patterns.

### Dashboard and Visualization

A monitoring dashboard could be developed to display:

- detected threats

- alert statistics

- system activity patterns

This would allow security analysts to interact with the intelligent monitoring system.

