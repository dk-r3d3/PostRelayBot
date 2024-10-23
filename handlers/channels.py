import time
import logging

from aiogram import types, Router
from aiogram.filters import state
from aiogram.fsm.context import FSMContext

from config import bot, client
from utils.keyboards import start_keyboard, back_key, add_key_word_keyboard
from utils.support import check_channel_exists, format_channels, menu
from database.views import add_recipient, add_source, delete_source, get_recipient, update_recipient_in_db
from handlers.transfer import stop_transfer_monitoring

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router_channels = Router()
middle: dict = {}


class Form(state.StatesGroup):  # класс для хранения состояний
    waiting_for_message_url_recipient = state.State()  # ожидание названия канала
    waiting_for_message_url_origin = state.State()  # ожидание названия канала
    waiting_for_message_delete = state.State()
    waiting_for_message_update = state.State()
    waiting_for_key_word = state.State()  # waiting for a keyword


@router_channels.callback_query(lambda c: c.data == 'back')
async def back(callback_query: types.CallbackQuery):
    recipient_channel = await get_recipient(callback_query.from_user.id)
    source_channels = await format_channels(callback_query.from_user.id)

    await menu(callback_query.message.chat.id, recipient_channel, source_channels, start_keyboard(recipient_channel))


@router_channels.callback_query(lambda c: c.data == 'add_recipient_channel')
async def add_channel_recipient(callback_query: types.CallbackQuery, state: FSMContext):
    """Добавить получатель"""
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Пожалуйста, введите название канала-получателя\nв формате 't.me/channel_name':",
                           reply_markup=back_key())
    await state.set_state(Form.waiting_for_message_url_recipient)


@router_channels.message(Form.waiting_for_message_url_recipient)  # ожидаем сообщения с url от пользователя
async def get_url_from_user_recipient(message: types.Message):
    channel_url = message.text
    check = await check_channel_exists(client, channel_url)
    time.sleep(1)
    if check:
        await add_recipient(message.from_user.id, channel_url)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Канал '{channel_url}' добавлен в список.")

        recipient_channel = await get_recipient(message.from_user.id)
        source_channels = await format_channels(message.from_user.id)

        await menu(message.chat.id, recipient_channel, source_channels, start_keyboard(recipient_channel))
    else:
        recipient_channel = await get_recipient(message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Данного канала не существует, либо его url скрыт, попробуйте снова",
                               reply_markup=start_keyboard(recipient_channel))


@router_channels.callback_query(lambda c: c.data == 'add_source_channel')
async def add_channel_source(callback_query: types.CallbackQuery, state: FSMContext):
    """Добавить канал-источник"""
    await bot.edit_message_text(
        text="Пожалуйста, введите название канала-источника\nв формате 't.me/channel_name':",
        message_id=callback_query.message.message_id,
        chat_id=callback_query.from_user.id
    )
    await state.set_state(Form.waiting_for_message_url_origin)  # устанавливаем состояние написания сообщения


@router_channels.message(Form.waiting_for_message_url_origin)
async def get_url_from_user_source(message: types.Message):
    channel_url = message.text
    check = await check_channel_exists(client, channel_url)
    time.sleep(1)
    if check:
        middle[message.from_user.id] = channel_url
        await bot.send_message(message.from_user.id,
                               f"Вы можете добавить список ключевых слов для поиска в данном канале",
                               reply_markup=add_key_word_keyboard())
    else:
        recipient_channel = await get_recipient(message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Данного канала не существует, попробуйте снова",
                               reply_markup=start_keyboard(recipient_channel))


@router_channels.callback_query(lambda c: c.data == 'delete_source_channel')
async def delete_channel_source(callback_query: types.CallbackQuery, state: FSMContext):
    """Удалить источник"""
    await bot.send_message(callback_query.from_user.id,
                           "Пожалуйста, введите название канала-источника, который хотите удалить\n")
    await state.set_state(Form.waiting_for_message_delete)  # устанавливаем состояние написания сообщения


@router_channels.message(Form.waiting_for_message_delete)
async def delete_channel(message: types.Message):
    user_id = message.from_user.id
    channel_url = message.text
    try:
        await delete_source(source=channel_url)

        await stop_transfer_monitoring(user_id)
        await bot.send_message(message.from_user.id, f"Канал-источник удален из списка")

        recipient_channel = await get_recipient(user_id)
        source_channels = await format_channels(user_id)
        await menu(message.chat.id, recipient_channel, source_channels, start_keyboard(recipient_channel))
    except Exception as E:
        """ДОРАБОТАТЬ"""
        logger.info("delete_channel - EXCEPT : %s", E)
        await bot.send_message(message.from_user.id, f"Данного канала нет в списке.", reply_markup=back_key())


@router_channels.callback_query(lambda c: c.data == 'update_recipient_channel')
async def update_recipient(callback_query: types.CallbackQuery, state: FSMContext):
    """Обновить канал-получатель"""
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Введите название нового канала-получателя:",
                           reply_markup=back_key())
    await state.set_state(Form.waiting_for_message_update)  # устанавливаем состояние написания сообщения


@router_channels.message(Form.waiting_for_message_update)  # ожидаем сообщения с url от пользователя
async def get_url_from_user_recipient_update(message: types.Message):
    user_id = message.from_user.id
    channel_url = message.text
    check = await check_channel_exists(client, channel_url)
    time.sleep(1)
    if check:
        await update_recipient_in_db(user_id, channel_url)
        await stop_transfer_monitoring(user_id)
        await bot.send_message(chat_id=user_id,
                               text=f"Канал-получатель изменен на '{channel_url}'")

        recipient_channel = await get_recipient(user_id)
        source_channels = await format_channels(user_id)

        await menu(message.chat.id, recipient_channel, source_channels, start_keyboard(recipient_channel))
    else:
        recipient_channel = await get_recipient(user_id)
        await bot.send_message(chat_id=user_id,
                               text=f"Данного канала не существует, либо его url скрыт, попробуйте снова",
                               reply_markup=start_keyboard(recipient_channel))


@router_channels.callback_query(lambda c: c.data == 'add_key_word')
async def add_key_word(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Через запятую введите ключевые слова по которым будет осуществляться поиск",
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id
                                )
    await state.set_state(Form.waiting_for_key_word)


@router_channels.message(Form.waiting_for_key_word)  # ожидаем сообщения с ключевым словом
async def add_key_word_fsm(message: types.Message):
    key_word = message.text
    await add_source(user_id=message.from_user.id,
                     source_channel=middle[message.from_user.id],
                     key_word=key_word)
    middle.clear()
    await bot.send_message(message.from_user.id, f"Поиск в данном канале будет осуществляться по слову - '{key_word}'")

    recipient_channel = await get_recipient(message.from_user.id)
    source_channels = await format_channels(message.from_user.id)

    await menu(message.chat.id, recipient_channel, source_channels, start_keyboard(recipient_channel))


@router_channels.callback_query(lambda c: c.data == 'without_a_keyword')
async def without_keyword(callback_query: types.CallbackQuery):
    await add_source(user_id=callback_query.from_user.id,
                     source_channel=middle[callback_query.from_user.id],
                     key_word='None')
    middle.clear()

    recipient_channel = await get_recipient(callback_query.from_user.id)
    source_channels = await format_channels(callback_query.from_user.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f'Ключевое слово не задано, из данного канала будут пересылаться все сообщения!\n')
    await menu(callback_query.message.chat.id, recipient_channel, source_channels, start_keyboard(recipient_channel))


@router_channels.callback_query(lambda c: c.data == 'help')
async def help_info(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Помощь будет позже', reply_markup=back_key()
                           )
