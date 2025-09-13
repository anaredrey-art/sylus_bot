from decouple import config
import os

BOT_TOKEN = config("BOT_TOKEN")
OPENROUTER_API_KEY = config("OPENROUTER_API_KEY")
CRYPTOBOT_API_KEY = config("CRYPTOBOT_API_KEY")

# Конфигурация для вебхуков (обязательно для Render)
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = int(os.getenv("PORT", 8000))

# URL вашего приложения на Render
RENDER_APP_NAME = config("RENDER_APP_NAME", default="sailus-bot")
WEBHOOK_URL = f"https://{RENDER_APP_NAME}.onrender.com"