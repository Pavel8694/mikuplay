from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from handlers.admin_handlers import show_admin_menu, is_admin
from handlers.user_handlers import show_user_menu
import logging

common_router = Router()
logger = logging.getLogger(__name__)

@common_router.callback_query(F.data == "cancel_action")
async def cancel_action(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if await state.get_state() is None:
        await callback_query.answer("⚠️ Действие уже отменено.", show_alert=True)
        logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) попытался отменить неактивное действие.")
        return

    await state.clear()
    await callback_query.answer("✅ Действие отменено.")
    logger.info(f"✅ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) отменил действие и вернулся в главное меню.")
    
    # Проверяем, является ли пользователь администратором и показываем соответствующее меню
    if await is_admin(callback_query.from_user.id, session):
        await show_admin_menu(callback_query.message.edit_text)
    else:
        await show_user_menu(callback_query.message.edit_text)
        
@common_router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()
    await callback_query.answer("🔁 Возвращаемся в главное меню.")
    logger.info(f"🔁 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) вернулся в главное меню.")
    
    # Проверяем, является ли пользователь администратором и показываем соответствующее меню
    if await is_admin(callback_query.from_user.id, session):
        await show_admin_menu(callback_query.message.edit_text)
    else:
        await show_user_menu(callback_query.message.edit_text)

