from recharge.client import get

def retrieve_payment_method(payment_method_id):
    res = get(f"/payment_methods/{payment_method_id}")
    res.raise_for_status()
    return res.json()["payment_method"]