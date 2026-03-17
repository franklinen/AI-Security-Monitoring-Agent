# AI-Security-Monitoring-Agent

An agent-based cybersecurity system that uses machine learning to detect threats in network logs and autonomously respond with security actions.

## Project Overview

This project implements an intelligent security agent that monitors network activity, detects potential cyber threats using a trained machine learning model, and takes appropriate actions such as blocking IPs or alerting administrators.

The system follows a Perception → Reasoning → Action architecture inspired by modern agentic AI systems.

## Project Motivation

With the increasing volume of network traffic, manual monitoring is inefficient and error-prone. This project demonstrates how AI agents + machine learning can:

Automate intrusion detection

Reduce response time to threats

Provide scalable security monitoring

Simulate real-world cybersecurity workflows

This aligns with real-world Security Operations Center (SOC) automation.


## Agent Architecture

The system is built using a modular agent-based design:

Environment → Percepts → Threat Model → Agent → Actions
Components:

Environment (environment.py)
Simulates incoming network log events

Percepts (percepts.py)
Transforms raw logs into structured features

Threat Model (threat_model.py)
Machine learning model that predicts threat probability

Agent (agent.py)
Makes decisions based on model outputs

Actions (actions.py)
Defines possible security responses

## System Workflow

Network Logs (CSV)
        ↓
Feature Processing
        ↓
ML Threat Detection Model
        ↓
Agent Decision Engine
        ↓
Security Action (BLOCK / ALERT / IGNORE)

## Cyberattack Simulation

The system uses a dataset of network activity logs to simulate real-world cyber threats such as:

Unauthorized access attempts

Abnormal traffic spikes

Suspicious login behavior

Potential intrusion patterns

The agent processes each event sequentially and reacts in real time.

## Learning Strategy

The threat detection model is trained using supervised machine learning:

 - Model: Random Forest Classifier

 - Input: Network activity features

 - Output: Probability of malicious activity

Key Steps:

 - Data preprocessing and scaling

 - Model training and validation

 - Performance evaluation using ROC-AUC
 
## Evaluation Results

Example performance metrics:

Accuracy: ~95%

ROC-AUC: ~0.96

Precision/Recall: High for attack detection

Evaluation includes:

Confusion matrix

Classification report

ROC curve analysis

## Project Structure

AI-Security-Monitoring-Agent
│
├── data/
│   └── logs.csv
│
├── models/
│   ├── threat_model.pkl
│   └── scaler.pkl
│
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── model_training.ipynb
│   └── model_evaluation.ipynb
│
├── src/
│   ├── actions.py
│   ├── agent.py
│   ├── environment.py
│   ├── percepts.py
│   ├── threat_model.py
│   └── run_agent.py
│
├── requirements.txt
└── README.md

## Installation & Setup
#### Clone Repository

git clone https://github.com/franklinen/AI-Security-Monitoring-Agent.git
cd AI-Security-Monitoring-Agent

#### Install Dependencies

pip install -r requirements.txt


##Train Model

####Run the notebook:

notebooks/model_training.ipynb

This generates:

models/threat_model.pkl
models/scaler.pkl

####Run the Agent

python src/run_agent.py

Example Output

BLOCK_IP
ALERT_ADMIN
IGNORE
INVESTIGATE

Each action corresponds to a detected threat level.

## 🧩 Key Features

✅ Agent-based architecture

✅ Real-time threat detection simulation

✅ Machine learning integration

✅ Modular and scalable design

✅ Production-style code organization

## 🔮 Future Work

This project can be extended into a full-scale AI security platform:

🔹 Deep Learning (LSTM for sequential attack detection)

🔹 Reinforcement Learning for adaptive response strategies

🔹 LLM integration for threat explanation

🔹 Real-time streaming with Kafka

🔹 Dashboard for monitoring (Streamlit / Dash)

🔹 Integration with SIEM tools

## 💡 Skills Demonstrated

Machine Learning & Model Deployment

Agent-Based System Design

Python Software Engineering

Cybersecurity Analytics

Data Preprocessing & Feature Engineering

End-to-End ML Pipeline Development

## 👤 Author

Frankline Ononiwu
Senior Machine Learning Engineer | Data Scientist

