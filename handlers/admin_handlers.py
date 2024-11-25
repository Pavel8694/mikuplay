from aiogram import Router, F, exceptions
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from database import Admin, Track
from sqlalchemy.future import select
from keyboards.buttons import cancel_button, back_to_menu_button
from handlers.user_handlers import show_user_menu
from functools import wraps
import logging
import asyncio

admin_router = Router()
logger = logging.getLogger(__name__)

MAIN_ADMIN_ID = 1331018098

class AddTrackState(StatesGroup):
    collecting_tracks = State()
    editing_track = State()
    adding_admin = State()
    removing_admin = State()
    deleting_track = State()
    replacing_audio = State()
    waiting_for_audio = State()

# Враппер для проверки прав администратора
def admin_only(callback_func):
    @wraps(callback_func)
    async def wrapper(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession, *args, **kwargs):
        if not await is_admin(callback_query.from_user.id, session):
            await callback_query.answer("⚠️ У вас нет прав для выполнения этого действия.", show_alert=True)
            return
        return await callback_func(callback_query, state, session, *args, **kwargs)
    return wrapper

async def is_admin(user_id: int, session: AsyncSession):
    if user_id == MAIN_ADMIN_ID:
        return True
    result = await session.execute(select(Admin).where(Admin.telegram_id == user_id))
    return result.scalars().first() is not None

@admin_router.message(Command("start"))
async def start_menu(message: Message, session: AsyncSession):
    if await is_admin(message.from_user.id, session):
        await show_admin_menu(message.answer)
        logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для админов.")
    else:
        await show_user_menu(message.answer)
        logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для юзеров.")

@admin_router.message(Command("menu"))
async def menu_command(message: Message, session: AsyncSession):
    if await is_admin(message.from_user.id, session):
        await show_admin_menu(message.answer)
        logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для админов.")
    else:
        await show_user_menu(message.answer)
        logger.info(f"💙 Пользователь @{message.from_user.username} ({message.from_user.id}) вызывает меню для юзеров.")

async def show_admin_menu(edit_function):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎵 Поиск треков", switch_inline_query_current_chat=""),
                InlineKeyboardButton(text="🧠 Настройки ИИ", callback_data="ai_button")
            ],
            [
                InlineKeyboardButton(text="➕ Добавить треки", callback_data="add_tracks"),
                InlineKeyboardButton(text="✏️ Редактировать трек", callback_data="edit_track")
            ],
            [
                InlineKeyboardButton(text="🔁 Заменить аудио-файл", callback_data="replace_audio"),
                InlineKeyboardButton(text="❌ Удалить трек", callback_data="delete_track")
            ],
            [
                InlineKeyboardButton(text="👤 Добавить администратора", callback_data="add_admin"),
                InlineKeyboardButton(text="🥵 Разжаловать администратора", callback_data="remove_admin")
            ],
            [
                InlineKeyboardButton(text="🆘 Помощь", callback_data="help_button"),
                InlineKeyboardButton(text="🫰 Поддержать проект", url="https://boosty.to/mikuplay")
            ],
            [
                InlineKeyboardButton(text="🔗 GitHub", url="https://github.com/Pavel8694/mikuplay"),
            ],
        ]
    )
    await edit_function('👋 *Приветствую вас в своей музыкальной обители, Пользователь Интернета!*\n\n👀 _Так-так, посмотрим... Ого! Похоже, вы являетесь администратором здесь! Добро пожаловать! Чувствуйте себя как дома. ᓚᘏᗢ_\n\n💬 *Кстати, ты можешь пообщаться со мной, обращаясь по имени. Пример:* `Мику, привет! Как дела?` _(Условия использования бота и ИИ читайте в меню "Помощь")_\n\n💙 *Выберите действие администратора:*', reply_markup=keyboard, parse_mode="Markdown")

@admin_router.callback_query(F.data == "add_tracks")
@admin_only
async def start_add_tracks(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    logger.info(f"⏳ Началось добавление треков пользователем @{callback_query.from_user.username} ({callback_query.from_user.id}).")
    await state.update_data(tracks=[])  # Инициализируем список треков
    await state.set_state(AddTrackState.collecting_tracks)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭️ Далее", callback_data="confirm_tracks")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")]
        ]
    )
    await callback_query.message.edit_text(
        '🎵 *Отправьте аудио-файлы для добавления. Когда закончите, вернитесь к этому сообщению и нажмите* ⏭️ *"Далее" или* ❌ *"Отменить".*\n\n_P. S. Не рекомендуется добавлять более 20-30 треков за раз (тестировалось максимум на 100 треках за раз) и треки, в названии/исполнителе которых есть странные символы, японские/китайские и любые другие иероглифы. Поиск на данный момент настраивался исключительно на работу с русскими и английскими буквами.\nКАТЕГОРИЧЕСКИ не рекомендуется добавлять аудио без названия/исполнителя (также с другим названием/исполнителем, не соответствующим добавляемому треку.) и с битрейтом ниже 320кб/с тех треков, которые доступны в нём и более высоком качестве. Моя музыкальная обитель должна состоять по большей части только из подлинных и высококачественных композиций!\nА вот что рекомендуется, так это подождать хотя бы 5-10 секунд, особенно если вы загрузили много треков. Спасибо! UwU_', 
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@admin_router.callback_query(F.data == "confirm_tracks")
@admin_only
async def confirm_tracks(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    tracks = data.get("tracks", [])

    if not tracks:
        await callback_query.message.edit_text("❌ *Не получено треков для добавления.*", reply_markup=back_to_menu_button, parse_mode="Markdown")
        logger.warning(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался подтвердить добавление без треков.")
        return

    track_info = "\n".join([f"*{track.title}* - _{track.artist}_" for track in tracks])
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="final_confirm_tracks")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")]
        ]
    )
    await callback_query.message.answer(
        f'👇 *Вы добавили следующие треки:*\n{track_info}\n\n✅ *Подтвердите или* ❌ *отмените действие.*\n\n_P. S. Если добавили много треков, придётся подождать, пока это сообщение не покажет текст об успешном добавлении треков. Треки и информация о них заносятся в базу данных эдакими "чанками" по 10 штук специально каждые 5.5 секунд, чтобы сильно не нагружать её._',
        reply_markup=keyboard, parse_mode="Markdown"
    )
    logger.info(f"📝 Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) получил список добавленных треков.")

@admin_router.callback_query(F.data == "final_confirm_tracks")
@admin_only
async def final_confirm_tracks(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    tracks = data.get("tracks", [])

    skipped_tracks = []  # Список для хранения пропущенных треков

    # Обработка треков батчами
    await process_tracks_in_batches(tracks, session, skipped_tracks, batch_size=10)

    await state.clear()
    
    if skipped_tracks:
        # Формируем сообщение с пропущенными треками
        skipped_info = "\n".join([f"{track.title}" for track in skipped_tracks])
        message = f"🤔 *Вроде, треки успешно добавлены.*\n\n⚠️ *Какие-то треки были пропущены, так как они уже существуют в базе данных:*\n_{skipped_info}_"
        logger.warning(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) попытался добавить уже существующие треки: {skipped_info}")
    else:
        message = "✅ *Все треки успешно добавлены.*"
        logger.info(f"✅ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) добавил {len(tracks)} трек(ов).")

    await callback_query.message.edit_text(message, reply_markup=back_to_menu_button, parse_mode="Markdown")

@admin_router.message(F.content_type == ContentType.AUDIO, StateFilter(AddTrackState.collecting_tracks))
async def collect_tracks(message: Message, state: FSMContext):
    audio = message.audio
    track_title = audio.title if audio.title else "Без названия"
    track_artist = audio.performer if audio.performer else "Неизвестный исполнитель"
    track_file_id = audio.file_id

    track_title_normalized = track_title.lower()
    track_artist_normalized = track_artist.lower()

    track = Track(
        title=track_title,
        artist=track_artist,
        file_id=track_file_id,
        title_lower=track_title_normalized,
        artist_lower=track_artist_normalized
    )

    # Получаем данные состояния
    data = await state.get_data()
    tracks = data.get("tracks", [])
    tracks.append(track)
    await state.update_data(tracks=tracks)

    # Логгирование добавленного трека
    logger.info(f"➕ Пользователь @{message.from_user.username} ({message.from_user.id}) добавил трек {track_title} исполнителя {track_artist}.")
    
async def process_tracks_in_batches(tracks, session, skipped_tracks, batch_size=10):
    for i in range(0, len(tracks), batch_size):
        batch = tracks[i:i + batch_size]
        for track in batch:
            # Проверяем, существует ли трек с таким же file_id
            existing_track = await session.execute(select(Track).where(Track.file_id == track.file_id))
            if existing_track.scalars().first():
                logger.warning(f"⚠️ Трек с file_id {track.file_id} уже существует. Пропускаем добавление.")
                skipped_tracks.append(track)  # Добавляем трек в список пропущенных
                continue  # Пропускаем добавление этого трека

            # Если трека нет, добавляем его в сессию
            session.add(track)
        
        try:
            await session.commit()
            logger.info(f"✅ Успешно добавлена группа из {len(batch)} треков.")
        except Exception as e:
            logger.error(f"⚠️ Ошибка при добавлении треков: {e}")
            await session.rollback()  # Откатываем транзакцию в случае ошибки

        # Делаем паузу, чтобы не превысить лимиты API
        await asyncio.sleep(5.5)  # Устанавливаем паузу в 5.5 секунд между обработкой батчей

# Функция для удаления трека (главный админ)
@admin_router.callback_query(F.data == "delete_track")
@admin_only
async def delete_track_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("⚠️ *Только главный администратор может удалять треки.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню удаления треков.")
        return

    await state.set_state(AddTrackState.deleting_track)
    await callback_query.message.edit_text("🆔 *Введите ID трека для удаления (он будет скрыт из поиска).*\n\n_P. S. Узнать ID нужного вам трека можно у главного администратора._", reply_markup=cancel_button, parse_mode="Markdown")
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню удаления треков.")

@admin_router.message(StateFilter(AddTrackState.deleting_track))
async def delete_track(message: Message, session: AsyncSession, state: FSMContext):
    try:
        track_id = int(message.text)
        track_result = await session.execute(select(Track).where(Track.id == track_id))
        track = track_result.scalars().first()
        if track:
            track.file_id = None
            await session.commit()
            await message.reply("✅ *Трек успешно скрыт из поиска.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"✅ Главный администратор @{message.from_user.username} ({message.from_user.id}) скрыл трек с ID {track_id}.")
            await state.clear()
        else:
            await message.reply("❌ *Трек с таким ID не найден.*", reply_markup=back_to_menu_button, parse_mode="Markdown")
            logger.info(f"❌ Пользователь @{message.from_user.username} ({message.from_user.id}) пытался скрыть трек с ID {track_id}, но его нет в моей базе.")
    except Exception as e:
        logger.error(f"⚠️ Ошибка при удалении трека: {e}")
        await message.reply("⚠️ *Ошибка при удалении трека. Проверьте введенные данные.*", reply_markup=back_to_menu_button, parse_mode="Markdown")

# Функция для замены аудио-файла
@admin_router.callback_query(F.data == "replace_audio")
@admin_only
async def replace_audio_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("⚠️ *Только главный администратор может заменять треки.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню замены треков.")
        return

    await state.set_state(AddTrackState.replacing_audio)
    await callback_query.message.edit_text("🆔 *Введите ID трека, для которого нужно заменить аудио-файл:*\n\n_P. S. Узнать ID нужного вам трека можно у главного администратора._", reply_markup=cancel_button, parse_mode="Markdown")
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню замены треков.")

@admin_router.message(StateFilter(AddTrackState.replacing_audio))
async def receive_track_id(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text:
        await message.reply("❌ *Пожалуйста, введите ID трека в виде текста.*", parse_mode="Markdown", reply_markup=cancel_button)
        logger.info(f"❌ Пользователь @{message.from_user.username} ({message.from_user.id}) пытался ввести ID трека не в виде текста.")
        return

    try:
        track_id = int(message.text)
        await state.update_data(track_id=track_id)
        await state.set_state(AddTrackState.waiting_for_audio)
        await message.reply("🎵 *Теперь отправьте новый аудио-файл для замены.*\n\n_P. S. Не отправляйте больше одного аудио-файла для избежания ошибок и проблем._", reply_markup=cancel_button, parse_mode="Markdown")
        logger.info(f"✅ Пользователь @{message.from_user.username} ({message.from_user.id}) ввёл корректный ID трека. Жду аудио-файл.")
    except ValueError:
        await message.reply("❌ *Пожалуйста, введите корректный ID трека.*", parse_mode="Markdown", reply_markup=cancel_button)
        logger.info(f"❌ Пользователь @{message.from_user.username} ({message.from_user.id}) ввёл некорректный ID трека: {track_id}.")

@admin_router.message(F.content_type == ContentType.AUDIO, StateFilter(AddTrackState.waiting_for_audio))
async def replace_audio(message: Message, session: AsyncSession, state: FSMContext):
    try:
        data = await state.get_data()
        track_id = data.get("track_id")

        if track_id is None:
            await message.reply("❌ *Не найден ID трека. Пожалуйста, начните сначала.*", parse_mode="Markdown", reply_markup=cancel_button)
            logger.info(f'❌ Пользователь @{message.from_user.username} ({message.from_user.id}) получил ошибку: "Не найден ID трека. Пожалуйста, начните сначала.".')
            await state.clear()
            return

        track_result = await session.execute(select(Track).where(Track.id == track_id))
        track = track_result.scalars().first()

        if track:
            # Получаем данные из нового аудио-файла
            track_title = message.audio.title if message.audio.title else "Без названия"
            track_artist = message.audio.performer if message.audio.performer else "Неизвестный исполнитель"
            track_file_id = message.audio.file_id

            # Обновляем информацию о треке
            track.title = track_title
            track.artist = track_artist
            track.file_id = track_file_id
            track.title_lower = track_title.lower()
            track.artist_lower = track_artist.lower()

            await session.commit()
            await message.reply("✅ *Аудио-файл и информация о треке успешно заменены.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"✅ Главный администратор @{message.from_user.username} ({message.from_user.id}) заменил файл и обновил информацию для трека с ID {track_id}.")
            await state.clear()
        else:
            await message.reply("❌ *Трек с таким ID не найден.*", parse_mode="Markdown", reply_markup=cancel_button)
            logger.info(f"❌ Пользователь @{message.from_user.username} ({message.from_user.id}) пытался обновить аудио-файл и информацию трека с ID {track_id}, но его нет в моей базе.")
            await state.clear()
    except Exception as e:
        logger.error(f"⚠️ Ошибка при замене аудио-файла: {e}")
        await message.reply("⚠️ *Ошибка при замене аудио-файла. Проверьте введенные данные.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        await state.clear()
        
@admin_router.callback_query(F.data == "edit_track")
@admin_only
async def edit_track_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("❌ *Только главный администратор может изменять информацию о треках.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        logger.info(f"❌ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню изменения информации о треках.")
        return
    
    await state.set_state(AddTrackState.editing_track)
    await callback_query.message.edit_text(
        "🆔 *Введите ID трека для редактирования и новые данные в формате:*\n`ID`\n`Название`\n`Исполнитель`\n\n_P. S. Это изменит лишь записи в БД, мета-данные треков останутся прежними! Если хотите заменить метаданные, измените их в самом MP3 файле и замените его в боте. Узнать ID нужного вам трека можно у главного администратора._",
        reply_markup=cancel_button,  # Используем кнопку отмены
        parse_mode="Markdown"
    )
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню редактирования информации о треках.")

@admin_router.message(StateFilter(AddTrackState.editing_track))
async def edit_track(message: Message, session: AsyncSession, state: FSMContext):
    try:
        data = message.text.split("\n")
        track_id = int(data[0])
        new_title = data[1]
        new_artist = data[2]

        track_result = await session.execute(select(Track).where(Track.id == track_id))
        track = track_result.scalars().first()
        if track:
            track.title = new_title
            track.artist = new_artist
            track.title_lower = new_title.lower()
            track.artist_lower = new_artist.lower()
            await session.commit()
            await message.reply("✅ *Трек успешно обновлен.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"✅ Пользователь @{message.from_user.username} ({message.from_user.id}) отредактировал данные трека с ID {track_id}.")
            await state.clear()
        else:
            await message.reply("❌ *Трек с таким ID не найден.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"❌ Пользователь @{message.from_user.username} ({message.from_user.id}) пытался отредактировать данные трека с ID {track_id}, но его нет в моей базе.")
    except Exception as e:
        logger.error(f"⚠️ Ошибка при редактировании трека: {e}")
        await message.reply("⚠️ *Ошибка при редактировании трека. Проверьте введенные данные.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        
@admin_router.callback_query(F.data == "add_admin")
@admin_only
async def add_admin_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("❌ *Только главный администратор может добавлять других администраторов.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        logger.info(f"❌ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню добавления администраторов.")
        return
    
    await state.set_state(AddTrackState.adding_admin)
    await callback_query.message.edit_text("🆔 *Введите ID нового администратора.*", reply_markup=cancel_button, parse_mode="Markdown")
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл в меню добавления администраторов.")

@admin_router.message(StateFilter(AddTrackState.adding_admin))
async def add_admin(message: Message, session: AsyncSession, state: FSMContext):
    try:
        new_admin_id = int(message.text)
        new_admin = Admin(telegram_id=new_admin_id)
        session.add(new_admin)
        await session.commit()
        await message.reply("✅ *Администратор успешно добавлен.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        logger.info(f"✅ Главный администратор @{message.from_user.username} ({message.from_user.id}) добавил администратора с ID {new_admin_id}.")
        await state.clear()
    except Exception as e:
        logger.error(f"⚠️ Ошибка при добавлении администратора: {e}")
        await message.reply("⚠️ *Ошибка: проверьте правильность введённых данных.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        
@admin_router.callback_query(F.data == "remove_admin")
@admin_only
async def remove_admin_command(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback_query.from_user.id != MAIN_ADMIN_ID:
        await callback_query.message.edit_text("❌ *Только главный администратор может разжаловать администраторов.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        logger.info(f"❌ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) пытался зайти в меню разжалования администраторов.")
        return
    
    await state.set_state(AddTrackState.removing_admin)
    await callback_query.message.edit_text("🆔 *Введите ID администратора, которого нужно разжаловать.*", reply_markup=cancel_button, parse_mode="Markdown")
    logger.info(f"⚠️ Пользователь @{callback_query.from_user.username} ({callback_query.from_user.id}) зашёл меню разжалования администраторов.")

@admin_router.message(StateFilter(AddTrackState.removing_admin))
async def remove_admin(message: Message, session: AsyncSession, state: FSMContext):
    try:
        admin_id_to_remove = int(message.text)

        # Проверяем, существует ли администратор с таким ID
        admin_result = await session.execute(select(Admin).where(Admin.telegram_id == admin_id_to_remove))
        admin = admin_result.scalars().first()

        if admin:
            await session.delete(admin)
            await session.commit()
            await message.reply("✅ *Администратор успешно разжалован.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"✅ Главный администратор @{message.from_user.username} ({message.from_user.id}) разжаловал администратора с ID {admin_id_to_remove}.")
        else:
            await message.reply("❌ *Администратор с таким ID не найден.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
            logger.info(f"❌ Главный администратор @{message.from_user.username} ({message.from_user.id}) пытался разжаловать администратора с ID {admin_id_to_remove}, но его нет в моей базе.")
        
        await state.clear()

    except ValueError:
        await message.reply("⚠️ *Пожалуйста, введите корректный ID администратора.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
    except Exception as e:
        logger.error(f"⚠️ Ошибка при разжаловании администратора: {e}")
        await message.reply("⚠️ *Ошибка при разжаловании администратора. Попробуйте еще раз.*", parse_mode="Markdown", reply_markup=back_to_menu_button)
        await state.clear()
