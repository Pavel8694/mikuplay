from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Кнопка для отмены действия
cancel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")]
    ]
)

back_to_menu_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="back_to_menu")]
    ]
)

get_ai_settings_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🗑 Очистить историю", callback_data="ai_clear"),
            ],
            [
                InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="back_to_menu"),
            ]
        ]
    )

get_ai_clear_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="ai_button"),
            ],
            [
                InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="back_to_menu"),
            ]
        ]
    )
