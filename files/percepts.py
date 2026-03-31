class SecurityPercept:
    """
    Structured representation of a single network log event.
    Transforms a raw log row into a typed object consumed by the agent.

    Features
    --------
    failed_logins        : int   – number of failed login attempts in the window
    ip_risk              : float – pre-computed IP reputation score  (0-1)
    off_hours            : int   – 1 if event occurred outside business hours
    unusual_port         : int   – 1 if a non-standard port was used
    data_transfer_volume : float – normalised outbound data volume (0-1)
    location_change      : int   – 1 if source location differs from baseline
    """

    FEATURE_NAMES = [
        "failed_logins",
        "ip_risk",
        "off_hours",
        "unusual_port",
        "data_transfer_volume",
        "location_change",
    ]

    def __init__(self, failed_logins, ip_risk, off_hours,
                 unusual_port, data_transfer_volume, location_change):
        self.failed_logins        = failed_logins
        self.ip_risk              = ip_risk
        self.off_hours            = off_hours
        self.unusual_port         = unusual_port
        self.data_transfer_volume = data_transfer_volume
        self.location_change      = location_change

    def to_feature_vector(self):
        """Return features as an ordered list for model input."""
        return [
            self.failed_logins,
            self.ip_risk,
            self.off_hours,
            self.unusual_port,
            self.data_transfer_volume,
            self.location_change,
        ]

    def __repr__(self):
        return (
            f"SecurityPercept(failed_logins={self.failed_logins}, "
            f"ip_risk={self.ip_risk:.2f}, off_hours={self.off_hours}, "
            f"unusual_port={self.unusual_port}, "
            f"data_transfer={self.data_transfer_volume:.2f}, "
            f"location_change={self.location_change})"
        )
