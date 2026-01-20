def is_payment_valid(subscription):
    """
    Define si una suscripción tiene pago válido
    """
    if subscription.get("max_retries_reached"):
        return False

    if subscription.get("status") != "active":
        return False

    if subscription.get("has_queued_charges") is False:
        return False

    return True
