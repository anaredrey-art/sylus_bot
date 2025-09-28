from aiogram import Router, F
from aiogram.types import Message
from services.silero_service import synthesize_speech
from database import get_db
from models.user import User

router = Router()

@router.message(F.text.startswith("🔊"))
async def handle_voice_choice(message: Message):
    voice_map = {
        "🔊 Голос 1 (Aidar)": "aidar",
        "🔊 Голос 2 (Baya)": "baya", 
        "🔊 Голос 3 (Kseniya)": "kseniya"
    }
    
    selected_voice = voice_map.get(message.text)
    if selected_voice:
        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        
        if user:
            user.voice_model = selected_voice
            db.commit()
            
            # Отправляем тестовое голосовое сообщение
            test_text = "Привет! Это тестовая озвучка вашего выбранного голоса."
            audio_path = await synthesize_speech(test_text, selected_voice)
            
            await message.answer_audio(
                audio=open(audio_path, 'rb'),
                caption=f"✅ Голос изменен на: {selected_voice}\n\nТестовое сообщение:"
            )
    else:
        await message.answer("Пожалуйста, выберите голос из предложенных вариантов.")