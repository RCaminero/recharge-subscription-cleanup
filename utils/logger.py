import csv
from datetime import datetime
import os

LOG_PATH = "data/logs/subscription_actions_log.csv"

def log_action(subscription_id, action, status, message=""):
    os.makedirs("data/logs", exist_ok=True)

    file_exists = os.path.isfile(LOG_PATH)

    with open(LOG_PATH, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "subscription_id",
                "action",
                "status",
                "timestamp",
                "message"
            ])

        writer.writerow([
            subscription_id,
            action,
            status,
            datetime.utcnow().isoformat(),
            message
        ])
