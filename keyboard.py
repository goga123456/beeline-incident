from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb1 = InlineKeyboardButton('IT проблема', callback_data='btn_it')
    kb2 = InlineKeyboardButton('Оборудование', callback_data='btn_oborudovaniye')
    kb.add(kb1, kb2)
    return kb


def get_p_or_v_kb() -> InlineKeyboardMarkup:
    kb2 = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton('Фото', callback_data='btn_photo')
    b2 = InlineKeyboardButton('Видео', callback_data='btn_video')
    b3 = InlineKeyboardButton('Ни то ни другое', callback_data='btn_nothing')
    kb2.add(b1, b2).add(b3)
    return kb2
