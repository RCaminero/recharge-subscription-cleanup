from datetime import datetime, timezone
from recharge.address import retrieve_address
from recharge.payment_method import retrieve_payment_method


def is_payment_valid(subscription):
    """
    Determines if a subscription has a truly valid payment method.

    Combines:
    1) Business safety rules (status, retries, queued charges, next charge date)
    2) Real Recharge payment method validation (address → payment_method → status)

    IMPORTANT:
    - If Recharge API blocks or fails at any step, we ASSUME VALID
      to avoid canceling healthy subscriptions by mistake.
    """

    # -------------------------
    # 1️⃣ ORIGINAL BUSINESS RULES (HARD FAILURES)
    # -------------------------
    if subscription.get("max_retries_reached") is True:
        return False

    if subscription.get("status") != "active":
        return False

    if subscription.get("has_queued_charges") is False:
        return False

    # 🔥 next_charge_scheduled_at must exist and be in the future
    next_charge = subscription.get("next_charge_scheduled_at")

    if not next_charge:
        return False

    try:
        if isinstance(next_charge, str):
            if "T" in next_charge:
                next_charge_dt = datetime.fromisoformat(
                    next_charge.replace("Z", "+00:00")
                )
            else:
                next_charge_dt = datetime.strptime(next_charge, "%Y-%m-%d")
                next_charge_dt = next_charge_dt.replace(tzinfo=timezone.utc)
        else:
            next_charge_dt = next_charge

        now = datetime.now(timezone.utc)

        if next_charge_dt <= now:
            return False

    except Exception as e:
        print(f"❌ Invalid next_charge_scheduled_at format: {next_charge} | {e}")
        return False

    # -------------------------
    # 2️⃣ REAL PAYMENT METHOD VALIDATION (SAFE MODE)
    # -------------------------
    address_id = subscription.get("address_id")

    if not address_id:
        print("⚠️ No address_id found, assuming VALID")
        return True

    try:
        # A) Get address
        address = retrieve_address(address_id)
        payment_method_id = address.get("payment_method_id")

        if not payment_method_id:
            print("⚠️ No payment_method_id on address, assuming INVALID")
            return False

        # B) Get payment method directly
        payment_method = retrieve_payment_method(payment_method_id)
        pm_status = payment_method.get("status", "").lower()

        # Recharge official statuses:
        # unvalidated → OK (don't cancel)
        # valid       → OK
        # invalid     → BAD
        # empty       → BAD

        if pm_status in ["invalid", "empty"]:
            return False

        if pm_status in ["valid", "unvalidated"]:
            return True

        # Unknown status → be safe
        print(f"⚠️ Unknown payment status '{pm_status}', assuming VALID")
        return True

    except Exception as e:
        # 🔥 CRITICAL: NEVER auto-cancel if Recharge blocks API calls
        print(
            f"⚠️ Payment lookup failed for sub {subscription.get('id')} | {e} | Assuming VALID"
        )
        return True
