from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_payment_keyboard(invoice_url: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Оплатить подписку", url=invoice_url)
    builder.button(text="✅ Проверить оплату", callback_data="check_payment")
    builder.button(text="❌ Отмена", callback_data="cancel_payment")
    builder.adjust(1)
    return builder.as_markup()