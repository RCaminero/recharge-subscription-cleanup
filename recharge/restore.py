from recharge.client import post

def restore_subscription(subscription_id):
    res = post(f"/subscriptions/{subscription_id}/activate")
    res.raise_for_status()
    return res.json()["subscription"]
