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

get_amdin_menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Добавить треки", callback_data="add_tracks"),
                InlineKeyboardButton(text="✏️ Редактировать трек", callback_data="edit_track")
            ],
            [
                InlineKeyboardButton(text="🔁 Заменить аудио-файлы", callback_data="replace_audio"),
                InlineKeyboardButton(text="❌ Удалить трек", callback_data="delete_track")
            ],
            [
                InlineKeyboardButton(text="👤 Добавить администратора", callback_data="add_admin"),
                InlineKeyboardButton(text="🥵 Разжаловать администратора", callback_data="remove_admin")
            ],
            [
                InlineKeyboardButton(text="🆔 Получить ID профиля и чата", callback_data="get_ids"),
                InlineKeyboardButton(text="📂 Получить ID файла", callback_data="get_file_id")
            ],
            [
                InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="back_to_menu"),
            ]
        ]
    )

get_help_menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚠️ Дисклеймер", callback_data="disclaimer_button"),
                InlineKeyboardButton(text="©️ DMCA", callback_data="dmca_button"),
            ],
            [
                InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="back_to_menu"),
            ]
        ]
    )

back_help_menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="help_button"),
            ],
            [
                InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="back_to_menu"),
            ]
        ]
    )

back_admin_menu_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="admin_menu_button"),
            ],
            [
                InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="back_to_menu"),
            ]
        ]
    )
