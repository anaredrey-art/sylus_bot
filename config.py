from decouple import config

BOT_TOKEN = config("BOT_TOKEN")
OPENROUTER_API_KEY = config("OPENROUTER_API_KEY")
OPENROUTER_API_URL = config("OPENROUTER_API_URL")
CRYPTOBOT_API_KEY = config("CRYPTOBOT_API_KEY")
CRYPTOBOT_API_URL = config("CRYPTOBOT_API_URL")

# Настройки БД
DATABASE_URL = "sqlite:///./sailus_bot.db"