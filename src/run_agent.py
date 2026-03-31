from environment import SecurityEnvironment
from agent import SecurityAgent
from threat_model import ThreatModel

env = SecurityEnvironment("logs.csv")

model = ThreatModel()

agent = SecurityAgent(model)

while True:

    event = env.get_event()

    if event is None:
        break

    percept = agent.perceive(event)

    action = agent.decide(percept)

    print(action)