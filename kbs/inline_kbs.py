from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb1 = InlineKeyboardButton('Horizon', callback_data='Horizon')
    kb2 = InlineKeyboardButton('ClarifyCRM', callback_data='ClarifyCRM')
    kb3 = InlineKeyboardButton('Проблемы с компьютером', callback_data='PK_problems')
    kb4 = InlineKeyboardButton('AWP', callback_data='AWP')
    kb5 = InlineKeyboardButton('Другое', callback_data='other')
    kb.add(kb1, kb2).add(kb3).add(kb4, kb5)
    return kb
def ustraneno() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton('Устранено', callback_data='Устранено')
    b2 = InlineKeyboardButton('Не устранено', callback_data='Не устранено')
    kb.add(b1, b2)
    return kb
def get_p_or_v_kb() -> InlineKeyboardMarkup:
    kb2 = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton('Фото', callback_data='btn_photo')
    b2 = InlineKeyboardButton('Видео', callback_data='btn_video')
    b3 = InlineKeyboardButton('Ни то ни другое', callback_data='btn_nothing')
    b4 = InlineKeyboardButton('Назад', callback_data='Назад')
    kb2.add(b1, b2).add(b3).add(b4)
    return kb2


