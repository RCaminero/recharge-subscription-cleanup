from recharge.client import post

def cancel_subscription(subscription_id, reason="cleanup"):
    payload = {
        "cancellation_reason": reason,
        "send_email": False
    }

    res = post(f"/subscriptions/{subscription_id}/cancel", payload)
    res.raise_for_status()
    return res.json()["subscription"]
