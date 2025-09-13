from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database import get_db
from models.memory import UserMemory

router = Router()

@router.message(Command("reset_memory"))
async def handle_reset_memory(message: Message):
    db = next(get_db())
    user_memory = db.query(UserMemory).filter(UserMemory.user_id == message.from_user.id).first()
    
    if user_memory:
        db.delete(user_memory)
        db.commit()
        await message.answer("✅ Память диалога очищена. Начинаем новый разговор.")
    else:
        await message.answer("🤔 У вас еще нет сохраненной истории диалога.")