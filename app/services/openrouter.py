import aiohttp
import json
import logging
from config import OPENROUTER_API_URL, OPENROUTER_API_KEY
from services.prompts.sylus_prompt import SYLUS_PROMPT
from database import get_db
from models.memory import UserMemory

async def get_openrouter_response(user_id: int, user_message: str):
    db = next(get_db())
    
    # Получаем или создаем память пользователя
    user_memory = db.query(UserMemory).filter(UserMemory.user_id == user_id).first()
    
    if not user_memory:
        user_memory = UserMemory(user_id=user_id, memory_data={"history": []})
        db.add(user_memory)
        db.commit()
    
    # Обновляем историю диалога
    history = user_memory.memory_data.get("history", [])
    
    # Добавляем новое сообщение пользователя
    history.append({"role": "user", "content": user_message})
    
    # Ограничиваем длину истории
    if len(history) > SYLUS_PROMPT["max_history_length"]:
        history = history[-SYLUS_PROMPT["max_history_length"]:]
    
    # Формируем полный промпт с историей
    messages = [{"role": "system", "content": SYLUS_PROMPT["system"]}] + history
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Используем DeepSeek через OpenRouter
    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_API_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    ai_response = data["choices"][0]["message"]["content"]
                    
                    # Сохраняем ответ AI в историю
                    history.append({"role": "assistant", "content": ai_response})
                    user_memory.memory_data = {"history": history}
                    db.commit()
                    
                    return ai_response
                else:
                    logging.error(f"OpenRouter error: {response.status}")
                    return "❌ Ошибка при обработке запроса к AI"
    except Exception as e:
        logging.error(f"OpenRouter exception: {e}")
        return "❌ Временные проблемы с подключением. Попробуйте позже."