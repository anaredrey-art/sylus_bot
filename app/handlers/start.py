from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.voice_kb import get_voice_keyboard
from database import get_db
from models.user import User

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    db = next(get_db())
    
    # Проверяем существующего пользователя
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    if not user:
        # Регистрируем нового пользователя
        new_user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        db.add(new_user)
        db.commit()
    
    welcome_text = (
        "👋 Добро пожаловать в Sailus AI Chat!\n\n"
        "✨ Я ваш персональный ИИ-собеседник с поддержкой голосовых сообщений.\n"
        "🔊 Выберите preferred голос или настройте свой в меню.\n"
        "💎 После 15 сообщений доступна премиум-подписка с расширенными возможностями!\n\n"
        "🚀 Начните общение прямо сейчас!"
    )
    
    await message.answer(welcome_text, reply_markup=get_voice_keyboard())