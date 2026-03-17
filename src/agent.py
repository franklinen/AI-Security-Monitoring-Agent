class SecurityAgent:

    def __init__(self, model):

        self.model = model
        self.memory = []

    def perceive(self, event):

        percept = {
            "login_failures": event["failed_logins"],
            "traffic": event["traffic"],
            "port_scan": event["port_scan"]
        }

        return percept

    def decide(self, percept):

        prediction = self.model.predict([[
            percept["login_failures"],
            percept["traffic"],
            percept["port_scan"]
        ]])

        if prediction == 1:
            return "ALERT"

        return "IGNORE"