import pandas as pd
from recharge.retrieve import retrieve_subscription
from recharge.cancel import cancel_subscription
from recharge.payment import is_payment_valid
from datetime import datetime, timezone

# 1️⃣ Load the CSV file with subscriptions
df = pd.read_csv("data/subscriptions.csv")
logs = []

print(f"Total rows loaded: {len(df)}")

# 2️⃣ Group subscriptions by user email
grouped = df.groupby("user_email")

for user, subs in grouped:
    records = []
    print(f"\n--- Processing user: {user} ---")

    # 3️⃣ Iterate through each subscription for this user
    for _, row in subs.iterrows():
        try:
            sub = retrieve_subscription(row.subscription_id)

            # If the subscription is already cancelled in Recharge, skip it
            p_status = sub.get("status", "unknown").lower()
            if p_status == "cancelled":
                print(f"ID: {row.subscription_id} | Already cancelled (skipped)")
                continue

            # Check if the payment method is valid
            valid = is_payment_valid(sub)

            # Extra data for non-technical logs
            price = sub.get("price", 0)
            product = sub.get("product_title", "Product")
            next_ch = sub.get("next_charge_scheduled_at", "No date")

            records.append({
                "id": row.subscription_id,
                "csv_action": row.action,     # KEEP or CANCEL from CSV
                "payment_valid": valid,       # True / False based on payment health
                "price": price,
                "product": product,
                "next_charge": next_ch,
                "status": p_status
            })

            print(f"ID: {row.subscription_id} | Payment valid: {valid} | Status: {p_status}")

        except Exception as e:
            print(f"❌ Error fetching ID {row.subscription_id}: {e}")

    # 4️⃣ Separate subscriptions with valid payments
    valid_subs = [r for r in records if r["payment_valid"]]

    # 5️⃣ Apply business rules per subscription
    for r in records:
        action_taken = None
        human_reason = ""

        # 🔴 CASE A: Both payments invalid → use CSV rule
        if len(valid_subs) == 0:
            if r["csv_action"] == "CANCEL":
                kept = [s for s in records if s["id"] != r["id"]][0]
                action_taken = "CANCEL"
                human_reason = (
                    f"BOTH PAYMENTS FAILED: Both subscriptions have payment issues. "
                    f"We kept the other ${kept['price']} plan for manual recovery and cancelled this ${r['price']} plan "
                    f"to avoid broken duplicates."
                )

        # 🟡 CASE B: Only one valid → cancel the broken one
        elif len(valid_subs) == 1:
            if not r["payment_valid"]:
                action_taken = "CANCEL"
                other = valid_subs[0]
                human_reason = (
                    f"PAYMENT ISSUES: The bank rejected charges for this ${r['price']} plan. "
                    f"We kept the healthy ${other['price']} plan instead."
                )

        # 🟢 CASE C: Both valid → use CSV rule
        else:
            if r["csv_action"] == "CANCEL":
                action_taken = "CANCEL"
                kept = [s for s in valid_subs if s["id"] != r["id"]][0]
                human_reason = (
                    f"DUPLICATE CLEANUP: Customer has two healthy plans. "
                    f"We removed this one to prevent double-billing and kept the one charging on {kept['next_charge']}."
                )

        # 6️⃣ Execute cancellation and store log
        if action_taken == "CANCEL":
            print(f"⚠️ Action: Cancelling {r['id']} - {human_reason[:60]}...")
            cancel_subscription(r["id"], human_reason)

            logs.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "subscription_id": r["id"],
                "email": user,
                "final_action": "CANCEL",
                "explanation_for_team": human_reason,  # Clear, non-technical reason
                "product": r["product"],
                "price": f"${r['price']}"
            })

# 7️⃣ Save final log file
if logs:
    log_df = pd.DataFrame(logs)
    log_df.to_csv("data/logs_cancel.csv", index=False)
    print(f"\n✅ Process finished. Log saved with {len(logs)} records.")
else:
    print("\nℹ️ No active subscriptions required action.")
