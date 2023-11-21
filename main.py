from datetime import datetime
from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from google.oauth2.service_account import Credentials
from aiogram.utils.executor import start_webhook
from googleapiclient.discovery import build
from config import TOKEN_API
from kbs.inline_kbs import get_kb, get_p_or_v_kb
from kbs.reply_kbs import get_start_kb, get_start_and_back_kb
from messages import *
from states import ProfileStatesGroup, AdminStatesGroup
import os
import logging

storage = MemoryStorage()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(TOKEN_API)
dp = Dispatcher(bot,
                storage=storage)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


#Google sheets
spreadsheet_id = '13JJbXiMBpSwTv1nSW9eoxuVp03GGbJ25y5YfWxlTPPU'
RANGE_NAME_1 = 'IT часть'
RANGE_NAME_2 = 'Оборудование'
RANGE_NAME_3 = 'Номер'
credentials = Credentials.from_service_account_file('beelinc-19f9d07341fe.json')
service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
#Google sheets

range_name = 'Номер!B1'

#Google sheets


async def select_number():
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    return result['values'][0][0]

async def update_number(item1):
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body={'values': [[item1]]}
    )
    request.execute()


async def append_it(item1, item2, item3, item4, item5, item6, item7, item8):
    values = [
        [item1, item2, item3, item4, item5, item6, item7, item8],
    ]
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=RANGE_NAME_1,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': values}
    )
    request.execute()


async def append_oborudovaniye(item1, item2, item3, item4, item5, item6):
    values = [
        [item1, item2, item3, item4, item5, item6],
    ]
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=RANGE_NAME_2,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': values}
    )
    request.execute()
#Google sheets


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text=start_msg,
                           reply_markup=get_kb())
    if state is None:
        return
    await state.finish()


@dp.callback_query_handler()
async def ikb_cb_handler(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'Horizon':
        async with state.proxy() as data:
            data['problem'] = callback_query.data
        await ProfileStatesGroup.it_problem_login.set()
        await bot.send_message(callback_query.from_user.id, text=login, reply_markup=get_start_and_back_kb())
        await callback_query.message.delete()

    if callback_query.data == 'ClarifyCRM':
        async with state.proxy() as data:
            data['problem'] = callback_query.data
        await ProfileStatesGroup.it_problem_login.set()
        await bot.send_message(callback_query.from_user.id, text=login, reply_markup=get_start_and_back_kb())
        await callback_query.message.delete()

    if callback_query.data == 'PK_problems':
        async with state.proxy() as data:
            data['problem'] = callback_query.data
        await ProfileStatesGroup.oborudovaniye_number.set()
        await bot.send_message(callback_query.from_user.id, text=ob_table_number,
                               reply_markup=get_start_and_back_kb())
        await callback_query.message.delete()

    if callback_query.data == 'other':
        async with state.proxy() as data:
            data['problem'] = callback_query.data
        await ProfileStatesGroup.it_problem_login.set()
        await bot.send_message(callback_query.from_user.id, text=login, reply_markup=get_start_and_back_kb())
        await callback_query.message.delete()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.it_problem_login)
async def check_info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Это не текст")


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.it_problem_login)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=start_msg,
                                   reply_markup=get_kb())
            await state.finish()
    else:
        async with state.proxy() as data:
            data['it_login'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=awp)
        await ProfileStatesGroup.it_problem_awp.set()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.it_problem_awp)
async def check_info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Это не текст")


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.it_problem_awp)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=login)
            await ProfileStatesGroup.it_problem_login.set()
    else:
        async with state.proxy() as data:
            data['it_awp'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=it_workplace)
        await ProfileStatesGroup.it_problem_workplace.set()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.it_problem_workplace)
async def check_info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Это не текст")


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.it_problem_workplace)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=awp)
            await ProfileStatesGroup.it_problem_awp.set()
    else:
        async with state.proxy() as data:
            data['it_workplace'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=it_desc)
        await ProfileStatesGroup.it_problem_info.set()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.it_problem_info)
async def check_info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Это не текст")


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.it_problem_info)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=it_workplace)
            await ProfileStatesGroup.it_problem_workplace.set()
    else:
        async with state.proxy() as data:
            data['it_info'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=what_you_want_to_send,
                               reply_markup=get_p_or_v_kb())
        await ProfileStatesGroup.it_problem_info.set()


@dp.message_handler(content_types=[*types.ContentTypes.PHOTO, *types.ContentTypes.TEXT],
                    state=ProfileStatesGroup.it_problem_photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=what_you_want_to_send,
                                   reply_markup=get_p_or_v_kb())
            await ProfileStatesGroup.it_problem_info.set()
    if message.photo:
        async with state.proxy() as data:
            num = await select_number()
            data['num'] = num
            data['it_photo'] = message.photo[0].file_id
            now = datetime.now()
            user_id = message.from_user.id
            response_date = now.strftime("%d.%m.%Y %H:%M:%S")
            await bot.send_photo(chat_id="-1001998156279",
                                 photo=data['it_photo'],
                                 caption=f"Номер заявки: {num}\n\n"
                                         f"Дата и время отклика: {response_date}\n\n"
                                         f"Логин: {data['it_login']}\n"
                                         f"Лог AWP: {data['it_awp']}\n"
                                         f"Номер места: {data['it_workplace']}\n"
                                         f"Описание проблемы: {data['it_info']}\n"
                                         f"User_id: {user_id}")


            # Google sheets
            await append_it(num, response_date, data['problem'], data['it_login'], data['it_awp'], data['it_workplace'],
                            data['it_info'], "Открыто")
            # Google sheets


            await bot.send_message(chat_id=message.from_user.id, text=success)
            await bot.send_message(chat_id=message.from_user.id, text=f"Номер заявки: {num}",
                                   reply_markup=get_start_kb())
            updated_num = int(num) + 1
            await update_number(updated_num)
            await state.finish()


@dp.message_handler(content_types=[*types.ContentTypes.VIDEO, *types.ContentTypes.TEXT],
                    state=ProfileStatesGroup.it_problem_video)
async def load_video(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=what_you_want_to_send,
                                   reply_markup=get_p_or_v_kb())
            await ProfileStatesGroup.it_problem_info.set()
    if message.video:
        async with state.proxy() as data:
            num = await select_number()
            data['it_video'] = message.video.file_id
            data['num'] = num
            now = datetime.now()
            response_date = now.strftime("%d.%m.%Y %H:%M:%S")
            user_id = message.from_user.id
            # -952509631
            await bot.send_video(chat_id="-1001998156279",
                                 video=data['it_video'],
                                 caption=f"Номер заявки: {num}\n\n"
                                         f"Дата и время отклика: {response_date}\n\n"
                                         f"Логин: {data['it_login']}\n"
                                         f"Лог AWP: {data['it_awp']}\n"
                                         f"Номер места: {data['it_workplace']}\n"
                                         f"Описание проблемы: {data['it_info']}\n"
                                         f"User_id: {user_id}")

            # Google sheets
            await append_it(num, response_date, data['problem'], data['it_login'], data['it_awp'], data['it_workplace'],
                            data['it_info'], "Открыто")
            # Google sheets

            await bot.send_message(chat_id=message.from_user.id, text=success)
            await bot.send_message(chat_id=message.from_user.id, text=f"Номер заявки: {num}",
                                   reply_markup=get_start_kb())
            updated_num = int(num) + 1
            await update_number(updated_num)
            await state.finish()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.oborudovaniye_number)
async def check_oborudovaniye_table_number(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=this_is_not_text)


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.oborudovaniye_number)
async def oborudovaniye_table_number(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=start_msg)
            await state.finish()

    else:
        async with state.proxy() as data:
            data['onumber'] = message.text
        await bot.send_message(chat_id=message.from_user.id,
                               text=oborudovaniye_desc_msg)
        await ProfileStatesGroup.oborudovaniye_desc.set()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.oborudovaniye_desc)
async def check_oborudovaniye_table_number(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=this_is_not_text)


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.oborudovaniye_desc)
async def oborudovaniye_table_number(message: types.Message, state: FSMContext) -> None:
    if message.text == "🔙":
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=ob_table_number)
            await ProfileStatesGroup.oborudovaniye_number.set()

    else:
        async with state.proxy() as data:
            num = await select_number()
            data['odesc'] = message.text
            data['num'] = num
            now = datetime.now()
            response_date = now.strftime("%d.%m.%Y %H:%M:%S")
            user_id = message.from_user.id
            await bot.send_message(chat_id="-1001998156279",
                                   text=f"Номер заявки:{num}\n\n"
                                        f"Дата и время отклика:{response_date}\n\n"
                                        f"Номер рабочего места: {data['onumber']}\n"
                                        f"Описание проблемы: {data['odesc']}\n"
                                        f"User_id: {user_id}")

            # Google sheets
            await append_oborudovaniye(num, response_date, data['problem'], data['onumber'], data['odesc'], "Открыто")
            # Google sheets


            # -952509631
            await bot.send_message(chat_id=message.from_user.id, text=success)
            await bot.send_message(chat_id=message.from_user.id, text=f"Номер заявки: {num}",
                                   reply_markup=get_start_kb())
            updated_num = int(num) + 1
            await update_number(updated_num)
            await state.finish()


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
        await bot.send_message(callback_query.from_user.id, text=it_desc, reply_markup=get_start_and_back_kb())
        await callback_query.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'btn_nothing', state=ProfileStatesGroup.it_problem_info)
async def process_callback_nothing(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        num = await select_number()
        data['num'] = num
        now = datetime.now()
        response_date = now.strftime("%d.%m.%Y %H:%M:%S")
        user_id = callback_query.from_user.id
        await bot.send_message(chat_id="-1001998156279",
                               text=f"Номер заявки: {num}\n\n"
                                    f"Дата и время отклика: {response_date}\n\n"
                                    f"Логин: {data['it_login']}\n"
                                    f"Лог AWP: {data['it_awp']}\n"
                                    f"Номер места: {data['it_workplace']}\n"
                                    f"Описание проблемы: {data['it_info']}\n"
                                    f"User_id: {user_id}")

        # Google sheets
        await append_it(num, response_date, data['problem'], data['it_login'], data['it_awp'], data['it_workplace'],
                        data['it_info'], "Открыто")
        # Google sheets

        await bot.send_message(chat_id=callback_query.from_user.id, text=success)
        await bot.send_message(chat_id=callback_query.from_user.id, text=f"Номер заявки: {num}",
                               reply_markup=get_start_kb())
    await callback_query.message.delete()
    updated_num = int(num) + 1
    await update_number(updated_num)
    await state.finish()


@dp.message_handler(commands=['admin'])
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id == 6478221968 or message.from_user.id == 94766813:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите chat_id")
        await AdminStatesGroup.chat_id.set()


@dp.message_handler(content_types=['text'], state=AdminStatesGroup.chat_id)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['chat_id'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите сообщение")
    await AdminStatesGroup.message.set()


@dp.message_handler(content_types=['text'], state=AdminStatesGroup.message)
async def load_it_info(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['message'] = message.text
    await bot.send_message(chat_id=data['chat_id'],
                           text=data['message'])
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
