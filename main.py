from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
import os
import logging
from ReplyKeyboard import get_start_and_back_kb
from keyboard import get_kb, get_p_or_v_kb, get_start_kb
from db import Database
from messages import *
from states import ProfileStatesGroup

storage = MemoryStorage()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

dp = Dispatcher(bot,
                storage=storage)

db = Database('Database.db')


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text=start_msg,
                           reply_markup=get_kb())
    if state is None:
        return
    await state.finish()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.it_problem_info)
async def check_info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=this_is_not_text)


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.it_problem_info)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=start_msg,
                                   reply_markup=get_kb())
            await state.finish()
    else:
        async with state.proxy() as data:
            data['it_description'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=what_you_want_to_send,
                               reply_markup=get_p_or_v_kb())


@dp.message_handler(content_types=[*types.ContentTypes.ANY], state=ProfileStatesGroup.it_problem_photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=what_you_want_to_send,
                                   reply_markup=get_p_or_v_kb())
            await ProfileStatesGroup.it_problem_info.set()
    else:
        async with state.proxy() as data:
            num = db.select_number()
            desc = data['it_description']
            data['it_photo'] = message.photo[0].file_id
            await bot.send_photo(chat_id="94766813",
                                 photo=data['it_photo'],
                                 caption=f"Номер заявки: {num}\n\n{desc}")
            # -952509631
            await bot.send_photo(chat_id="-952509631",
                                 photo=data['it_photo'],
                                 caption=f"Номер заявки: {num}\n\n{desc}")
            await bot.send_message(chat_id=message.from_user.id, text=success)
            await bot.send_message(chat_id=message.from_user.id, text=f"Номер заявки: {num}", reply_markup=get_start_kb())
        db.numberplusone()
        await state.finish()





@dp.message_handler(content_types=[*types.ContentTypes.ANY], state=ProfileStatesGroup.it_problem_video)
async def load_video(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=what_you_want_to_send,
                                   reply_markup=get_p_or_v_kb())
            await ProfileStatesGroup.it_problem_info.set()
    else:
        async with state.proxy() as data:
            num = db.select_number()
            desc = data['it_description']
            data['it_video'] = message.video.file_id
            await bot.send_video(chat_id="94766813",
                                 video=data['it_video'],
                                 caption=f"Номер заявки: {num}\n\n{desc}")
            # -952509631
            await bot.send_video(chat_id="-952509631",
                                 video=data['it_video'],
                                 caption=f"Номер заявки: {num}\n\n{desc}")
            await bot.send_message(chat_id=message.from_user.id, text=success)
            await bot.send_message(chat_id=message.from_user.id, text=f"Номер заявки: {num}", reply_markup=get_start_kb())

        db.numberplusone()
        await state.finish()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.oborudovaniye_number_and_desc)
async def check_oborudovaniye_table_number(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=this_is_not_text)


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.oborudovaniye_number_and_desc)
async def oborudovaniye_table_number(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=start_msg,
                                   reply_markup=get_kb())
            await state.finish()

    else:
        async with state.proxy() as data:
            num = db.select_number()
            data['onumber_and_desc'] = message.text
            await bot.send_message(chat_id="94766813",
                                   text=f"Номер заявки:{num}\n\n"
                                        f"Номер рабочего места и суть проблемы:\n{data['onumber_and_desc']}")

            # -952509631
            await bot.send_message(chat_id="-952509631",
                                   text=f"Номер заявки:{num}\n\n"
                                        f"Номер рабочего места и суть проблемы:\n{data['onumber_and_desc']}")
            await bot.send_message(chat_id=message.from_user.id, text=success)
            await bot.send_message(chat_id=message.from_user.id, text=f"Номер заявки: {num}", reply_markup=get_start_kb())

        await state.finish()
        db.numberplusone()




@dp.callback_query_handler()
async def ikb_cb_handler(callback_query: types.CallbackQuery):
    if callback_query.data == 'btn_it':
        await ProfileStatesGroup.it_problem_info.set()
        await bot.send_message(callback_query.from_user.id, text=it_msg, reply_markup=get_start_and_back_kb())
        await callback_query.message.delete()

    if callback_query.data == 'btn_oborudovaniye':
        await ProfileStatesGroup.oborudovaniye_number_and_desc.set()
        await bot.send_message(callback_query.from_user.id, text=oborudovaniye_table_number_and_desc_msg, reply_markup=get_start_and_back_kb())
        await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'btn_photo', state=ProfileStatesGroup.it_problem_info)
async def process_callback_photo(callback_query: types.CallbackQuery):
    await ProfileStatesGroup.it_problem_photo.set()
    await bot.send_message(callback_query.from_user.id,
                           text=photo)
    await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'btn_video', state=ProfileStatesGroup.it_problem_info)
async def process_callback_video(callback_query: types.CallbackQuery):
    await ProfileStatesGroup.it_problem_video.set()
    await bot.send_message(callback_query.from_user.id,
                           text=video)
    await callback_query.message.delete()

@dp.callback_query_handler(lambda c: c.data == 'Назад', state=ProfileStatesGroup.it_problem_info)
async def process_callback_video(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await ProfileStatesGroup.it_problem_info.set()
        await bot.send_message(callback_query.from_user.id, text=it_msg, reply_markup=get_start_and_back_kb())
        await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'btn_nothing', state=ProfileStatesGroup.it_problem_info)
async def process_callback_nothing(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        num = db.select_number()
        desc = data['it_description']
        await bot.send_message(chat_id="94766813",
                               text=f"Номер заявки:{num} \n\nСуть проблемы: {desc}")
        await bot.send_message(chat_id="-952509631",
                               text=f"Номер заявки:{num} \n\nСуть проблемы: {desc}")
        await bot.send_message(chat_id=callback_query.from_user.id, text=success)
        await bot.send_message(chat_id=callback_query.from_user.id, text=f"Номер заявки: {num}", reply_markup=get_start_kb())
    await callback_query.message.delete()
    db.numberplusone()
    await state.finish()

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
