from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.buttons import cancel_button, get_help_menu_keyboard, back_help_menu_keyboard
from database import Track
from middlewares import SearchCallbackData, SearchState
import logging

user_router = Router()
logger = logging.getLogger(__name__)

search_callback = SearchCallbackData

@user_router.message(Command("start"))
async def user_start(message: Message):
    await show_user_menu(message.answer)  # Используем message.answer для отправки нового сообщения
    logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для юзеров.")

@user_router.message(Command("menu"))
async def user_menu(message: Message):
    await show_user_menu(message.answer)  # Используем message.answer для отправки нового сообщения
    logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для юзеров.")

async def show_user_menu(edit_function):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎵 Поиск треков", switch_inline_query_current_chat=""),
                InlineKeyboardButton(text="🔍 Расширенный поиск", callback_data="start_search")
            ],
            [
                InlineKeyboardButton(text="🪪 Профиль", callback_data="profile_button"),
                InlineKeyboardButton(text="🛍️ Магазин", callback_data="shop_button")
            ],
            [
                InlineKeyboardButton(text="🧠 Настройки ИИ", callback_data="ai_button"),
                InlineKeyboardButton(text="🆘 Помощь", callback_data="help_button")
            ],
            [
                InlineKeyboardButton(text="🔗 GitHub", url="https://github.com/Pavel8694/mikuplay"),
                InlineKeyboardButton(text="🫰 Поддержать проект", url="https://boosty.to/mikuplay")
                
            ],
        ]
    )
    await edit_function('👋 *Приветствую вас в своей музыкальной обители, Пользователь Интернета!*\n\n'
                        '👀 _Так-так, посмотрим... Ого! Похоже, вы являетесь почётным посетителем здесь! Добро пожаловать! Чувствуйте себя как дома. ᓚᘏᗢ_\n\n'
                        '💬 *Кстати, ты можешь пообщаться со мной, обращаясь по имени или отвечая на мои сообщения. Пример:* `Мику, привет! Как дела?` _(Условия использования бота и ИИ читайте в меню "Помощь")_\n\n'
                        '💙 *Выберите действие почётного посетителя:*',
                        reply_markup=keyboard,
                        parse_mode="Markdown"
                        )
    
@user_router.callback_query(F.data == "help_button")
async def show_help_menu(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"🆘 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню помощи.")
    await callback_query.message.edit_text('💙 *MikuPlayBot* `alpha 0.1.8` *"Первый ПОИСК будущего"*\n\n'
                                           '_О проекте: MikuPlay — бесплатный open-source бот с искусственным интеллектом для общения (нейросеть с личностью Мику), быстрого поиска и скачивания музыки в Telegram со своей базой данных, пополняемой вручную. Доступен inline-режим для поиска. Работает как в личных сообщениях, так и в группах._\n\n'
                                           '🧡 *Powered by Meme Corp.*\n'
                                           '📧 *mikuplaybot@gmail.com*',
                                           parse_mode="Markdown",
                                           reply_markup=get_help_menu_keyboard
                                           )

@user_router.callback_query(F.data == "disclaimer_button")
async def show_help_menu(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню дисклеймера.")
    await callback_query.message.edit_text('⚠️ *Условия использования и дисклеймер:*\n'
                                           '*1.* Все композиции, представленные в данном боте, были взяты из открытых источников и предоставляются исключительно для ознакомительных целей.\n'
                                           '*2.* Мы не поощряем пиратство и всегда за использование лицензионного контента через соответствующие официальные сервисы с подписками. Если у вас есть возможность и желание поддержать любимого исполнителя, вас ничто не должно останавливать сделать это.\n'
                                           '*3.* Мы не несём ответственности за ответы нейросети и за запросы пользователей к ней. Вся ответственность за запросы пользователей лежит на самих пользователях.\n'
                                           '*4.* Функционал ИИ в данном боте представлен исключительно в развлекательных целях, и ответы нейросети могут содержать ошибки/отсебятину. Проверяйте важную информацию.\n'
                                           '*5.* Используя данного бота, вы автоматически соглашаетесь с этими условиями использования и дисклеймером.',
                                           parse_mode="Markdown",
                                           reply_markup=back_help_menu_keyboard
                                           )

@user_router.callback_query(F.data == "dmca_button")
async def show_help_menu(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"©️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню DMCA.")
    await callback_query.message.edit_text('©️ *DMCA:*\n'
                                           'Если вы считаете, что ваш контент не должен быть здесь, напишите нам на почту mikuplaybot@gmail.com с пометкой `нарушение авторских прав` или `DMCA`.',
                                           parse_mode="Markdown",
                                           reply_markup=back_help_menu_keyboard
                                           )
    
@user_router.callback_query(F.data == "profile_button")
async def show_help_menu(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"🪪 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню профиля.")
    await callback_query.answer("🪪 На данный момент функционал находится в разработке.", show_alert=True)
    
@user_router.callback_query(F.data == "shop_button")
async def show_help_menu(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"🛍️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню магазина.")
    await callback_query.answer("🛍️ На данный момент функционал находится в разработке.", show_alert=True)

# Обработчик для старта поиска
@user_router.callback_query(F.data == "start_search")
async def start_search(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"🔍 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в расширенный поиск треков.")
    # Устанавливаем состояние ожидания запроса
    await state.set_state(SearchState.waiting_for_query)
    await callback_query.message.edit_text(
        "🔍 *Введите полное/частичное название трека, имя исполнителя или ID для расширенного поиска.*\n\n✍️ *Пример для названия:* `Resist and Disorder`\n👤 *Пример для исполнителя:* `Rezodrone`\n🆔 *Пример для ID:* `85`",
        parse_mode="Markdown",
        reply_markup=cancel_button,
    )

# Обработчик для поиска по запросу
@user_router.message(StateFilter(SearchState.waiting_for_query))
async def handle_search_query(message: Message, session: AsyncSession, state: FSMContext):
    query = message.text.strip()
    if not query:
        await message.reply("❌ *Пожалуйста, введите запрос для поиска.*", parse_mode="Markdown")
        return

    try:
        # Отправляем начальное сообщение с результатами
        await search_tracks(message, session, query, page=1, send_new=True)
    except Exception as e:
        # Логируем ошибку
        logger.error(f"⚠️ Ошибка при расширенном поиске треков в чате {message.chat.id}: {e}")
        await message.reply("⚠️ *Произошла ошибка при выполнении поиска. Попробуйте снова.*", parse_mode="Markdown")
    finally:
        await state.clear()

# Обработчик для навигации по страницам
@user_router.callback_query(search_callback.filter())
async def handle_search_pagination(callback_query: CallbackQuery, callback_data: SearchCallbackData, session: AsyncSession):
    query = callback_data.query
    page = callback_data.page

    # Проверяем, находится ли пользователь на текущей странице
    for row in callback_query.message.reply_markup.inline_keyboard:
        for button in row:
            if button.text and button.text.startswith("[") and button.text.endswith("]"):
                current_page = int(button.text.strip("[]"))
                if page == current_page:
                    await callback_query.answer("📌 Вы уже на этой странице.", show_alert=False)
                    return

    try:
        # Редактируем сообщение при переходе по страницам
        await search_tracks(callback_query.message, session, query, page, send_new=False)
    except Exception as e:
        # Логируем ошибку
        logger.error(f"⚠️ Ошибка при навигации по страницам расширенного поиска треков в чате {callback_query.message.chat.id}: {e}")
        await callback_query.answer("⚠️ Произошла ошибка при обработке страницы.", show_alert=True)
    finally:
        await callback_query.answer()

# Функция поиска треков
async def search_tracks(message: Message, session: AsyncSession, query: str, page: int = 1, page_size: int = 10, send_new: bool = False):
    offset = (page - 1) * page_size
    results = []
    total_count = 0

    try:
        # Если запрос - это числовой ID, ищем только по ID
        if query.isdigit():
            track_id = int(query)
            track_result = await session.execute(select(Track).where(Track.id == track_id))
            tracks = track_result.scalars().all()
            total_count = len(tracks)
        else:
            # Ищем совпадения по названию или исполнителю
            track_result = await session.execute(
                select(Track)
                .where(
                    (Track.title_lower.ilike(f"%{query.lower()}%"))
                    | (Track.artist_lower.ilike(f"%{query.lower()}%"))
                )
                .offset(offset)
                .limit(page_size)
            )
            tracks = track_result.scalars().all()

            # Подсчитываем общее количество результатов для пагинации
            total_result = await session.execute(
                select(Track).where(
                    (Track.title_lower.ilike(f"%{query.lower()}%"))
                    | (Track.artist_lower.ilike(f"%{query.lower()}%"))
                )
            )
            total_count = len(total_result.scalars().all())

        # Формируем сообщение с результатами
        if tracks:
            for track in tracks:
                results.append(
                    f"🎵 *ID:* `{track.id}`\n*Название:* `{track.title}`\n*Исполнитель:* `{track.artist}`\n\n"
                )
            result_message = f"💁‍♀️ *Результаты расширенного поиска:*\n\n📄 _Страница {page}/{(total_count + page_size - 1) // page_size}_\n\n" + "".join(results)
        else:
            result_message = "❌ *Треки не найдены.*"

        # Создаём клавиатуру для пагинации
        total_pages = (total_count + page_size - 1) // page_size
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])

        # Кнопки быстрого перехода и страниц
        if total_pages > 1:
            row = []
            if page > 1:
                row.append(
                    InlineKeyboardButton(
                        text="⏮️",
                        callback_data=SearchCallbackData(query=query, page=1).pack()
                    )
                )

            # Отображение 5 кнопок для страниц
            start_page = max(1, page - 2)
            end_page = min(total_pages, start_page + 4)

            for p in range(start_page, end_page + 1):
                row.append(
                    InlineKeyboardButton(
                        text=f"[{p}]" if p == page else str(p),
                        callback_data=SearchCallbackData(query=query, page=p).pack()
                    )
                )

            if page < total_pages:
                row.append(
                    InlineKeyboardButton(
                        text="⏭️",
                        callback_data=SearchCallbackData(query=query, page=total_pages).pack()
                    )
                )

            keyboard.inline_keyboard.append(row)

        # Кнопка возвращения в главное меню
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data="back_to_menu"
            )
        ])

        # Отправляем новое сообщение или редактируем текущее
        if send_new:
            await message.answer(result_message, parse_mode="Markdown", reply_markup=keyboard)
        else:
            await message.edit_text(result_message, parse_mode="Markdown", reply_markup=keyboard)

    except Exception as e:
        # Логируем ошибку
        logger.error(f"⚠️ Ошибка при расширенном поиске треков: {e}")
        raise

@user_router.message(Command("300bucks"))
async def three_hundred_bucks(message: Message):
    await message.reply_sticker(sticker="CAACAgIAAx0Cff1e_QABBWyeZ5J2lmJfS_jwMJCvgi4zBmZo-p8AAlkiAAKfBulKrMkUSVSLD-M2BA")
    logger.info(f"🥚 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает пасхалку по команде /300bucks.")

@user_router.message(Command("uhartem"))
async def uh_artem(message: Message):
    await message.reply_video(video="BAACAgIAAx0Cff1e_QABBZDcZ5lRBKXQhq_gfVIL3I3jPGpKS_0AAjMkAAIk2PFKFGSr57Eocj02BA")
    logger.info(f"🥚 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает пасхалку по команде /uhartem.")

@user_router.message(Command("meow1"))
async def meow_one(message: Message):
    await message.reply_photo(photo="AgACAgIAAx0Cff1e_QABBYhaZ5dkQL0-M8nzFDsLpUCQnefreUAAAivzMRtX2rhIm5ZoBNoaIy4BAAMCAAN5AAM2BA")
    logger.info(f"🥚 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает пасхалку по команде /meow1.")

@user_router.message(Command("meow2"))
async def meow_two(message: Message):
    await message.reply_sticker(sticker="CAACAgIAAx0Cff1e_QABBWtKZ5Jn-UmVstTiVs2dZg9ZFkUxKPAAAmhfAAI196lKPqUAAaJx38ApNgQ")
    logger.info(f"🥚 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает пасхалку по команде /meow2.")

@user_router.message(Command("hleb"))
async def hleb(message: Message):
    await message.reply_document(document="CgACAgIAAx0Cff1e_QABBXGoZ5OC4VxdklHfPdR7NdWyLllaGzQAAmlIAALREVlLZhWEYRK2J-I2BA")
    logger.info(f"🥚 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает пасхалку по команде /hleb.")
    
@user_router.message(Command("dante1"))
async def dante_one(message: Message):
    await message.reply_document(document="CgACAgIAAx0Cff1e_QABBeTWZ65fjCZYbGfHRxfFatDrh_TvI0UAAr5vAAJ0uVlJcAy-RkS5Nrc2BA")
    logger.info(f"🥚 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает пасхалку по команде /dante1.")
    
@user_router.message(Command("dante2"))
async def dante_two(message: Message):
    await message.reply_document(document="CgACAgQAAxkBAAJlKWe4WMRzeYpyfbds6mrFXWwmM18RAAIHBQAC0V59Uocj2rHW1Zb7NgQ")
    logger.info(f"🥚 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает пасхалку по команде /dante2.")

@user_router.message(Command("uwy"))
async def uwy(message: Message):
    await message.reply_sticker(sticker="CAACAgIAAx0Cff1e_QABBaKwZ53RO9uR-_K7HlQclQOcOePrwP4AAvNYAAKmMmhLgY19Cupue5g2BA")
    logger.info(f"🥚 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает пасхалку по команде /uwy.")

pivas_text = """
🍺 <b>[Текст песни «фотографирую пивас»]</b> 🍻

<b>[Припев]</b>
<b><i>Я каждый вечер пью пивас
Двадцать литров все за раз
Без тебя, без тебя
Без тебя
Я каждый вечер пью пивас
Двадцать литров все за раз
Без тебя, без тебя
Без тебя</i></b>

<b>[Бридж]</b>
<b><i>Уйди, моя печень в жизни гаснет
Становлюсь холодным
Молчи, пиво вечно, всё не важно
Я умру свободным</i></b>

<b>[Предприпев]</b>
<b><i>Я не вижу лиц
Я вижу своё пивко
И среди всего я люблю только его
Просто прекрати про-про-протрезвлять мои ёбаные сны</i></b>

<b>[Припев]</b>
<b><i>Я каждый вечер пью пивас
Двадцать литров все за раз
Без тебя, без тебя
Без тебя
Я каждый вечер пью пивас
Двадцать литров все за раз
Без тебя, без тебя
Без тебя</i></b>

<b>[Куплет]</b>
<b><i>Все эти люди, что я облевал
Весь этот кринж мне пора бы забыть
Думаю, что я остался один
Но уже никогда не бухаю один</i></b>

<b>[Бридж]</b>
<b><i>Уйди, моя печень в жизни гаснет
Становлюсь холодным
Молчи, пиво вечно, всё не важно
Я умру свободным</i></b>

<b>[Предприпев]</b>
<b><i>Я не вижу лиц
Я вижу своё пивко
И среди всего я люблю только его
Просто прекрати про-про-протрезвлять мои ёбаные сны</i></b>

<b>[Припев]</b>
<b><i>Я каждый вечер пью пивас
Двадцать литров все за раз
Без тебя, без тебя
Без тебя
Я каждый вечер пью пивас
Двадцать литров все за раз
Без тебя, без тебя
Без тебя</i></b>

<b><i><a href="https://genius.com/2077-pivzavod2077-photographing-beer-lyrics">[Источник текста]</a></i></b>
"""

@user_router.message(Command("pivas2077"))
async def pivas2077(message: Message):
    await message.reply(pivas_text,
                        parse_mode="HTML"
                        )
    logger.info(f"🥚 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает пасхалку по команде /pivas2077.")
