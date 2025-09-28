from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from services.cryptobot_service import create_invoice, check_invoice_status
from keyboards.payment_kb import get_payment_keyboard
from database import get_db
from models.user import User, Subscription

router = Router()

@router.message(Command("premium"))
@router.message(F.text == "💎 Премиум подписка")
async def handle_premium_request(message: Message):
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    if not user or user.message_count < 15:
        await message.answer(
            "❌ Премиум-подписка доступна после отправки 15 сообщений.\n"
            f"📊 Ваш текущий счетчик: {user.message_count if user else 0}/15 сообщений"
        )
        return
    
    # Создаем инвойс в CryptoBot
    invoice = await create_invoice(
        amount=2.00,  # Базовая подписка $2
        currency="USD",
        user_id=user.telegram_id
    )
    
    if invoice and "result" in invoice:
        invoice_url = invoice["result"]["pay_url"]
        await message.answer(
            "💎 Выберите вариант подписки:\n\n"
            "• Basic ($2) - доступ ко всем голосам\n"
            "• Premium ($5) - эксклюзивные голоса + приоритет обработки\n\n"
            "👇 Нажмите кнопку ниже для оплаты",
            reply_markup=get_payment_keyboard(invoice_url)
        )

@router.callback_query(F.data == "check_payment")
async def handle_payment_check(callback: CallbackQuery):
    # Проверяем статус оплаты
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
    
    if user and await check_invoice_status(user.telegram_id):
        # Активируем подписку
        subscription = Subscription(
            user_id=user.id,
            plan_type="basic_2",
            is_active=True
        )
        db.add(subscription)
        db.commit()
        
        await callback.message.edit_text(
            "✅ Оплата подтверждена! Премиум-подписка активирована.\n\n"
            "✨ Теперь вам доступны:\n"
            "• Все голоса Silero TTS\n"
            "• Приоритетная обработка запросов\n"
            "• Эксклюзивные функции"
        )
    else:
        await callback.answer("❌ Оплата не найдена или еще не обработана", show_alert=True)