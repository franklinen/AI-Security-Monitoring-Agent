import pandas as pd

class SecurityEnvironment:

    def __init__(self, log_file):
        self.logs = pd.read_csv(log_file)
        self.time_step = 0

    def get_event(self):

        if self.time_step >= len(self.logs):
            return None

        event = self.logs.iloc[self.time_step]
        self.time_step += 1

        return event