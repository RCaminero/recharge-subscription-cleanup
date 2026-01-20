import sys
from recharge.payment_method import retrieve_payment_method

payment_method_id = sys.argv[1]
sub = retrieve_payment_method(payment_method_id)

print("\n=== PAYMENT METHOD DATA ===\n")
for k, v in sub.items():
    print(f"{k}: {v}")
