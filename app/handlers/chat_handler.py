from aiogram import Router, F
from aiogram.types import Message
from services.openrouter_service import get_openrouter_response
from services.silero_service import synthesize_speech
from database import get_db
from models.user import User, Subscription

router = Router()

@router.message(F.text & ~F.text.startswith("🔊") & ~F.text.startswith("💎"))
async def handle_chat_message(message: Message):
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    if not user:
        await message.answer("Пожалуйста, начните с команды /start")
        return
    
    # Увеличиваем счетчик сообщений
    user.message_count += 1
    db.commit()
    
    # Проверяем是否需要 подписку
    requires_subscription = user.message_count >= 15
    
    if requires_subscription:
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user.id, 
            Subscription.is_active == True
        ).first()
        
        if not subscription:
            await message.answer(
                "❌ Вы исчерпали лимит бесплатных сообщений (15).\n"
                "💎 Для продолжения общения приобретите премиум-подписку:\n\n"
                "Используйте команду /premium или кнопку в меню"
            )
            return
    
    # Получаем ответ от Open Router с учетом истории
    ai_response = await get_openrouter_response(user.id, message.text)
    
    # Если у пользователя есть подписка, предлагаем озвучку
    if requires_subscription and subscription:
        # Синтезируем речь
        audio_path = await synthesize_speech(ai_response, user.voice_model)
        
        await message.answer(ai_response)
        await message.answer_audio(audio=open(audio_path, 'rb'))
    else:
        await message.answer(ai_response)