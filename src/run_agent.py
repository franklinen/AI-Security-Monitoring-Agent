env = SecurityEnvironment("logs.csv")

agent = SecurityAgent(model)

while True:

    event = env.get_event()

    if event is None:
        break

    percept = agent.perceive(event)

    action = agent.decide(percept)

    print(action)