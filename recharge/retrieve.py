from recharge.client import get

def retrieve_subscription(subscription_id):
    res = get(f"/subscriptions/{subscription_id}")
    res.raise_for_status()
    return res.json()["subscription"]