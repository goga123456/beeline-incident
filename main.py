from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from keyboard import get_kb, get_p_or_v_kb
from db import Database
from messages import *
from states import ProfileStatesGroup

storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
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
    async with state.proxy() as data:
        data['it_description'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=what_you_want_to_send,
                           reply_markup=get_p_or_v_kb())


@dp.message_handler(lambda message: not message.photo, state=ProfileStatesGroup.it_problem_photo)
async def check_photo(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=this_is_not_photo)


@dp.message_handler(content_types=['photo'], state=ProfileStatesGroup.it_problem_photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
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
        await bot.send_message(chat_id=message.from_user.id, text=f"Номер заявки: {num}")
    db.numberplusone()
    await state.finish()


@dp.message_handler(lambda message: not message.video, state=ProfileStatesGroup.it_problem_video)
async def check_video(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=this_is_not_video)


@dp.message_handler(content_types=['video'], state=ProfileStatesGroup.it_problem_video)
async def load_video(message: types.Message, state: FSMContext) -> None:
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
        await bot.send_message(chat_id=message.from_user.id, text=f"Номер заявки: {num}")

    db.numberplusone()
    await state.finish()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.oborudovaniye_number)
async def check_oborudovaniye_table_number(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=this_is_not_text)


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.oborudovaniye_number)
async def oborudovaniye_table_number(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['onumber'] = message.text
    await bot.send_message(chat_id=message.from_user.id, text=oborudovaniye_problem_description)
    await ProfileStatesGroup.oborudovaniye_problem_info.set()


@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.oborudovaniye_problem_info)
async def check_oborudovaniye_info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=this_is_not_text)


@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.oborudovaniye_problem_info)
async def oborudovaniye_info(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        num = db.select_number()
        data['oinfo'] = message.text
        await bot.send_message(chat_id="94766813",
                               text=f"Номер заявки:{num}\n\n"
                                    f"1.Номер места: {data['onumber']}\n"
                                    f"2.Суть проблемы: {data['oinfo']}")
        # -952509631
        await bot.send_message(chat_id="-952509631",
                               text=f"Номер заявки:{num} \n\n"
                                    f"1.Номер места: {data['onumber']}\n"
                                    f"2.Суть проблемы: {data['oinfo']}")
        await bot.send_message(chat_id=message.from_user.id, text=success)
        await bot.send_message(chat_id=message.from_user.id, text=f"Номер заявки: {num}")
    db.numberplusone()
    await state.finish()


@dp.callback_query_handler()
async def ikb_cb_handler(callback_query: types.CallbackQuery):
    if callback_query.data == 'btn_it':
        await ProfileStatesGroup.it_problem_info.set()
        await bot.send_message(callback_query.from_user.id, text=it_msg)
        await callback_query.message.delete()

    if callback_query.data == 'btn_oborudovaniye':
        await ProfileStatesGroup.oborudovaniye_number.set()
        await bot.send_message(callback_query.from_user.id, text=oborudovaniye_table_number_msg)
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
        await bot.send_message(chat_id=callback_query.from_user.id, text=f"Номер заявки: {num}")
    await callback_query.message.delete()
    db.numberplusone()
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
