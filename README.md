# AI-Security-Monitoring-Agent

This project implements an intelligent agent that monitors security logs and learns to detect suspicious activity.

## Overview

Modern security systems generate large volumes of logs that are difficult for human analysts to monitor manually. This project demonstrates how an intelligent agent can automatically detect suspicious events using a contextual bandit approach.

## Agent Design

Environment: Stream of simulated security events  
State: Event features (failed logins, IP risk, off-hours activity, unusual ports)  
Actions:  
- 0 = Allow activity  
- 1 = Flag activity  

Reward System:
- True Positive = +5
- True Negative = +1
- False Positive = -2
- False Negative = -6

The agent uses an epsilon-greedy contextual bandit strategy to balance exploration and exploitation.

## Project Structure
