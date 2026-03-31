import pandas as pd


class SecurityEnvironment:
    """
    Simulates a stream of network log events for the agent to monitor.

    Reads a CSV file produced by log_generator.py or attack_simulator.py
    and yields one event per time-step, mimicking real-time ingestion.
    """

    REQUIRED_COLUMNS = [
        "failed_logins",
        "ip_risk",
        "off_hours",
        "unusual_port",
        "data_transfer_volume",
        "location_change",
    ]

    def __init__(self, log_file: str):
        self.logs = pd.read_csv(log_file)
        self._validate_columns()
        self.time_step = 0
        print(f"[Environment] Loaded {len(self.logs)} log events from '{log_file}'")

    def _validate_columns(self):
        missing = [c for c in self.REQUIRED_COLUMNS if c not in self.logs.columns]
        if missing:
            raise ValueError(
                f"Log file is missing required columns: {missing}. "
                f"Please regenerate using log_generator.py"
            )

    def get_event(self):
        """Return the next log event as a dict, or None when exhausted."""
        if self.time_step >= len(self.logs):
            return None
        event = self.logs.iloc[self.time_step].to_dict()
        self.time_step += 1
        return event

    def reset(self):
        """Restart the event stream from the beginning."""
        self.time_step = 0

    def __len__(self):
        return len(self.logs)
