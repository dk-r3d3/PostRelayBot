from aiogram import types


def start_keyboard(recipient_channel):
    buttons_1 = [
        [
            types.InlineKeyboardButton(text="Добавить канал-получатель", callback_data="add_recipient_channel"),
        ],
        [
            types.InlineKeyboardButton(text="Добавить канал-источник", callback_data="add_source_channel")
        ],
        [
            types.InlineKeyboardButton(text="Удалить канал-источник", callback_data="delete_source_channel")
        ],
        [
            types.InlineKeyboardButton(text="Старт", callback_data="start_transfer"),
            types.InlineKeyboardButton(text="Помощь", callback_data="help")
        ]]
    buttons_2 = [
        [
            types.InlineKeyboardButton(text="Обновить канал-получатель", callback_data="update_recipient_channel"),
        ],
        [
            types.InlineKeyboardButton(text="Добавить канал-источник", callback_data="add_source_channel")
        ],
        [
            types.InlineKeyboardButton(text="Удалить канал-источник", callback_data="delete_source_channel")
        ],
        [
            types.InlineKeyboardButton(text="Старт", callback_data="start_transfer"),
            types.InlineKeyboardButton(text="Помощь", callback_data="help")
        ]
    ]
    if recipient_channel is None:
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_1)
    else:
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_2)
    return keyboard


def back_key():
    buttons = [
        [
            types.InlineKeyboardButton(text="Назад", callback_data="back"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def add_key_word_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавить ключевое слово", callback_data="add_key_word"),
        ],
        [
            types.InlineKeyboardButton(text="Продолжить", callback_data="without_a_keyword")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
