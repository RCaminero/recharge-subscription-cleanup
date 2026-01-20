import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.rechargeapps.com"

HEADERS = {
    "X-Recharge-Version": os.getenv("RECHARGE_API_VERSION"),
    "X-Recharge-Access-Token": os.getenv("RECHARGE_API_TOKEN"),
    "Content-Type": "application/json",
}

def get(endpoint):
    return requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)

def post(endpoint, payload=None):
    return requests.post(
        f"{BASE_URL}{endpoint}",
        json=payload,
        headers=HEADERS
    )
