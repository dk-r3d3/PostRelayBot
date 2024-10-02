import time

from aiogram import types, Router
from aiogram.filters import state
from aiogram.fsm.context import FSMContext

from config import bot, client
from utils.keyboards import start_keyboard, add_channel_recipient_keyboard, back_key, add_key_word_keyboard
from utils.support import check_channel_exists, format_channels, format_black_list
from database.views import add_channels, delete_channels, add_black_words, delete_black_word_view

router_channels = Router()
middle: list = []


class Form(state.StatesGroup):  # класс для хранения состояний
    waiting_for_message_url_origin = state.State()  # ожидание названия канала
    waiting_for_message_url_recipient = state.State()  # ожидание названия канала
    waiting_for_key_word = state.State()  # waiting for a keyword
    waiting_for_key_word_black = state.State()
    waiting_for_key_word_black_delete = state.State()
    waiting_for_message_delete = state.State()


@router_channels.callback_query(lambda c: c.data == 'back')
async def back(callback_query: types.CallbackQuery):
    channels = await format_channels(callback_query.from_user.id)
    black_list = await format_black_list(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Ваши пары каналов-источников и каналов-получателей:\n{channels}\n\n{black_list}',
                           reply_markup=start_keyboard())


@router_channels.callback_query(lambda c: c.data == 'add_couple')
async def add_channel_origin(callback_query: types.CallbackQuery, state: FSMContext):
    """Добавить пары"""
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Пожалуйста, введите название канала-источника\nв формате 't.me/channel_name':",
                           reply_markup=back_key())
    await state.set_state(Form.waiting_for_message_url_origin)


@router_channels.message(Form.waiting_for_message_url_origin)  # ожидаем сообщения с url от пользователя
async def get_url_from_user_origin(message: types.Message):
    channel_url = message.text
    check = await check_channel_exists(client, channel_url)
    time.sleep(1)
    if check:
        middle.append(channel_url)  # source
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Канал '{channel_url}' добавлен в список.",
                               reply_markup=add_channel_recipient_keyboard())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Данного канала не существует, попробуйте снова",
                               reply_markup=start_keyboard())


@router_channels.callback_query(lambda c: c.data == 'add_channel_recipient')
async def add_channel_recipient(callback_query: types.CallbackQuery, state: FSMContext):
    """Добавить канал-получатель"""
    await bot.edit_message_text(
        text="Пожалуйста, введите название канала-получателя\nв формате 't.me/channel_name':",
        message_id=callback_query.message.message_id,
        chat_id=callback_query.from_user.id
    )
    await state.set_state(Form.waiting_for_message_url_recipient)  # устанавливаем состояние написания сообщения


@router_channels.message(Form.waiting_for_message_url_recipient)  # ожидаем сообщения с url от пользователя
async def get_url_from_user_recipient(message: types.Message):
    channel_url = message.text
    check = await check_channel_exists(client, channel_url)
    time.sleep(1)
    if check:
        middle.append(channel_url)  # recipient
        await bot.send_message(message.from_user.id, f"Канал '{channel_url}' добавлен в список.",
                               reply_markup=add_key_word_keyboard())
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Данного канала не существует, попробуйте снова",
                               reply_markup=start_keyboard())


@router_channels.callback_query(lambda c: c.data == 'delete_couple')
async def delete_channels_couple(callback_query: types.CallbackQuery, state: FSMContext):
    """Удалить пару"""
    await bot.send_message(callback_query.from_user.id,
                           "Пожалуйста, введите название канала-источника, который хотите удалить\n"
                           "(будут удалены все пары с названием данного канала):")
    await state.set_state(Form.waiting_for_message_delete)  # устанавливаем состояние написания сообщения


@router_channels.message(Form.waiting_for_message_delete)
async def delete_channel(message: types.Message):
    channel_url = message.text
    await delete_channels(source=channel_url)
    await bot.send_message(message.from_user.id, f"Пара удалена")
    channels = await format_channels(message.from_user.id)
    black_list = await format_black_list(message.from_user.id)

    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Ваши пары каналов-источников и каналов-получателей:\n '
                                f'{channels}\n\n{black_list}', reply_markup=start_keyboard())


@router_channels.callback_query(lambda c: c.data == 'add_key_word')
async def add_key_word(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Введите ключевое слово, по которому будет осуществляться поиск.",
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id
                                )
    await state.set_state(Form.waiting_for_key_word)


@router_channels.callback_query(lambda c: c.data == 'add_word_in_black_list')
async def add_key_word_black(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Введите слово, которое хотели бы добавить в черный список:",
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id
                                )
    await state.set_state(Form.waiting_for_key_word_black)


@router_channels.message(Form.waiting_for_key_word_black)  # ожидаем сообщения с ключевым словом
async def add_key_word_fsm_black(message: types.Message):
    black_word = message.text
    await add_black_words(user_id=message.from_user.id,
                          black_word=black_word)

    channels = await format_channels(message.from_user.id)
    black_list = await format_black_list(message.from_user.id)

    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Ваши пары каналов-источников и каналов-получателей:\n '
                                f'{channels}\n\n{black_list}', reply_markup=start_keyboard())


@router_channels.callback_query(lambda c: c.data == 'delete_word_in_black_list')
async def delete_black_word(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id,
                           "Пожалуйста, введите слово, которое хотите удалить из черного списка: ")
    await state.set_state(Form.waiting_for_key_word_black_delete)  # устанавливаем состояние написания сообщения


@router_channels.message(Form.waiting_for_key_word_black_delete)
async def delete_black_word_fsm(message: types.Message):
    black_word = message.text
    await delete_black_word_view(word=black_word)
    await bot.send_message(message.from_user.id, f"Слово удалено из списка")

    channels = await format_channels(message.from_user.id)
    black_list = await format_black_list(message.from_user.id)

    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Ваши пары каналов-источников и каналов-получателей:\n '
                                f'{channels}\n\n{black_list}', reply_markup=start_keyboard())


@router_channels.message(Form.waiting_for_key_word)  # ожидаем сообщения с ключевым словом
async def add_key_word_fsm(message: types.Message):
    key_word = message.text
    await add_channels(user_id=message.from_user.id,
                       source_channel=middle[0],
                       recipient_channel=middle[1],
                       key_word=key_word)
    middle.clear()
    await bot.send_message(message.from_user.id, f"Поиск в данной паре будет осуществляться по слову - '{key_word}'")
    channels = await format_channels(message.from_user.id)

    black_list = await format_black_list(message.from_user.id)  # new

    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Ваши пары каналов-источников и каналов-получателей:\n '
                                f'{channels}\n\n{black_list}', reply_markup=start_keyboard())


@router_channels.callback_query(lambda c: c.data == 'without_a_keyword')
async def without_keyword(callback_query: types.CallbackQuery):
    await add_channels(user_id=callback_query.from_user.id,
                       source_channel=middle[0],
                       recipient_channel=middle[1],
                       key_word="None")
    middle.clear()
    channels = await format_channels(callback_query.from_user.id)

    black_list = await format_black_list(callback_query.from_user.id)  # new

    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f'Ключевое слово не задано, будут пересылаться все сообщения\n'
                                f'Ваши пары каналов-источников и каналов-получателей:\n '
                                f'{channels}\n\n{black_list}', reply_markup=start_keyboard())


@router_channels.callback_query(lambda c: c.data == 'help')
async def help_info(callback_query: types.CallbackQuery):

    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Помощь будет позже', reply_markup=back_key())
