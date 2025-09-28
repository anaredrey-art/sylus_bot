import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from database import Base, engine

# Добавляем путь к app в sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH, WEB_SERVER_HOST, WEB_SERVER_PORT
from handlers.start import router as start_router
from handlers.voice_handler import router as voice_router
from handlers.payment_handler import router as payment_router
from handlers.chat_handler import router as chat_router
from handlers.memory_handler import router as memory_router

async def on_startup(bot: Bot):
    # Создаем таблицы в базе данных
    Base.metadata.create_all(bind=engine)
    
    # Устанавливаем вебхук
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    logging.info("Бот запущен и вебхук установлен")

async def on_shutdown(bot: Bot):
    # Удаляем вебхук при завершении
    await bot.delete_webhook()
    logging.info("Бот остановлен")

def create_app():
    # Создаем экземпляр бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(voice_router)
    dp.include_router(payment_router)
    dp.include_router(chat_router)
    dp.include_router(memory_router)
    
    # Регистрируем обработчики запуска/остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Создаем aiohttp приложение
    app = web.Application()
    
    # Создаем обработчик вебхуков
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    
    # Регистрируем обработчик
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    # Настраиваем приложение
    setup_application(app, dp, bot=bot)
    
    return app

if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    
    # Запуск приложения
    app = create_app()
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)