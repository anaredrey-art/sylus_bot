import aiohttp
import json
from config import CRYPTOBOT_API_KEY

CRYPTOBOT_API_URL = "https://pay.crypt.bot/api/"

async def create_invoice(amount: float, currency: str, user_id: int):
    headers = {
        "Crypto-Pay-API-Token": CRYPTOBOT_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "amount": amount,
        "asset": "USDT" if currency == "USD" else currency,
        "description": f"Премиум подписка для пользователя {user_id}",
        "paid_btn_name": "callback",
        "paid_btn_url": f"https://t.me/your_bot?start=success_{user_id}",
        "payload": json.dumps({"user_id": user_id, "plan": "basic" if amount == 2 else "premium"})
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{CRYPTOBOT_API_URL}createInvoice", headers=headers, json=payload) as response:
            return await response.json()

async def check_invoice_status(user_id: int):
    headers = {
        "Crypto-Pay-API-Token": CRYPTOBOT_API_KEY
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{CRYPTOBOT_API_URL}getInvoices?user_id={user_id}", headers=headers) as response:
            data = await response.json()
            if data["ok"] and data["result"]["items"]:
                return data["result"]["items"][0]["status"] == "paid"
            return False