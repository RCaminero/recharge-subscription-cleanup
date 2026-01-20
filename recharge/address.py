from recharge.client import get

def retrieve_address(address_id):
    res = get(f"/addresses/{address_id}")
    res.raise_for_status()
    return res.json()["address"]
