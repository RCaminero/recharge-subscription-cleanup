import sys
from recharge.retrieve import retrieve_subscription

subscription_id = sys.argv[1]
sub = retrieve_subscription(subscription_id)

print("\n=== SUBSCRIPTION DATA ===\n")
for k, v in sub.items():
    print(f"{k}: {v}")
