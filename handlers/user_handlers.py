from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from keyboards.buttons import back_to_menu_button
import logging

user_router = Router()
logger = logging.getLogger(__name__)

@user_router.message(Command("start"))
async def user_start(message: Message):
    await show_user_menu(message.answer)  # Используем message.answer для отправки нового сообщения
    logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для юзеров.")

@user_router.message(Command("menu"))
async def user_menu(message: Message):
    await show_user_menu(message.answer)  # Используем message.answer для отправки нового сообщения
    logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для юзеров.")
    
@user_router.message(Command("help"))
async def user_help(message: Message):
    await show_help_menu(message.answer)  # Используем message.answer для отправки нового сообщения
    logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для помощи.")

async def show_user_menu(edit_function):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎵 Поиск треков", switch_inline_query_current_chat=""),
                InlineKeyboardButton(text="🫰 Поддержать проект", url="https://boosty.to/mikuplay")
            ],
        ]
    )
    await edit_function("👋 *Приветствую вас в своей музыкальной обители, Пользователь Интернета!*\n\n👀 _Так-так, посмотрим... Ого! Похоже, вы являетесь почётным посетителем здесь! Добро пожаловать! Чувствуйте себя как дома. ᓚᘏᗢ_\n\n🆘 *Вызвать меню помощи можно командой* `/help`*.*\n\n🚧 *В данный момент функционал почётных посетителей ограничен и бот находится в разработке.*", reply_markup=keyboard, parse_mode="Markdown")
    
async def show_help_menu(edit_function):
    await edit_function('💙 *MikuPlayBot* `alpha 0.1.6` *"Первый звук будущего"*\n\n_О проекте: MikuPlay — бесплатный бот для быстрого поиска и скачивания музыки в Telegram со своей базой данных, пополняемой вручную. Доступен inline-режим для поиска. Работает как в личных сообщениях, так и в группах._\n\n🧡 *Powered by Meme Corp.*\n📧 *mikuplaybot@memecorp.ru*\n🌐 *team.memecorp.ru*\n\n*Дисклеймер:*\nВсе композиции, представленные в данном боте, были взяты из открытых источников и предоставляются исключительно для ознакомительных целей. Мы не поощряем пиратство и всегда за использование лицензионного контента через соответствующие официальные сервисы с подписками.\n\n*DMCA:*\nЕсли вы считаете, что ваш контент не должен быть здесь, напишите нам на почту mikuplaybot@memecorp.ru с пометкой "нарушение авторских прав" или "DMCA".', parse_mode="Markdown", reply_markup=back_to_menu_button)
