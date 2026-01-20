import os
from dotenv import load_dotenv

load_dotenv()

RECHARGE_API_TOKEN = os.getenv("RECHARGE_API_TOKEN")
RECHARGE_API_VERSION = os.getenv("RECHARGE_API_VERSION")
RECHARGE_BASE_URL = os.getenv("RECHARGE_BASE_URL")

HEADERS = {
    "X-Recharge-Access-Token": RECHARGE_API_TOKEN,
    "X-Recharge-Version": RECHARGE_API_VERSION,
    "Content-Type": "application/json"
}
