from aiogram import types


def start_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавить пару источник-получатель", callback_data="add_couple"),
        ],
        [
            types.InlineKeyboardButton(text="Удалить пару источник-получатель", callback_data="delete_couple")
        ],
        [
            types.InlineKeyboardButton(text="Добавить слово в черный список", callback_data="add_word_in_black_list")
        ],
        [
            types.InlineKeyboardButton(text="Удалить слово из черного списка", callback_data="delete_word_in_black_list")
        ],
        [
            types.InlineKeyboardButton(text="Старт", callback_data="start_transfer"),
            types.InlineKeyboardButton(text="Помощь", callback_data="help")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def back_key():
    buttons = [
        [
            types.InlineKeyboardButton(text="Назад", callback_data="back"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def add_channel_recipient_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавить канал-получатель", callback_data="add_channel_recipient"),
            types.InlineKeyboardButton(text="Назад", callback_data="back")
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
