import pandas as pd
from recharge.restore import restore_subscription

df = pd.read_csv("data/logs_cancel.csv")

for _, row in df.iterrows():
    restore_subscription(row.subscription_id)

print("Restore completed")
