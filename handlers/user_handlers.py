import time
import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import create_inline_keyboard, create_reply_keyboard
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU
from services.services import Schedule, parse_sptbx
from lexicon.lexicon import LST_SCHEDULE
from apscheduler.schedulers.asyncio import AsyncIOScheduler


user_router = Router()
schedule = Schedule(10, 16, LST_SCHEDULE)


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=create_reply_keyboard(2,  'Сегодня', 'Завтра', 'Раписание игр',
                                                            'Расписание по датам',
                                                            'Расписание на неделю'))


@user_router.message(F.text == 'Расписание по датам')
async def process_days_command(message: Message):
    await message.answer(text='Выберите день, на который хотите посмотреть расписание...',
                         reply_markup=create_inline_keyboard(3, *schedule.schedule().keys()))


@user_router.message(F.text == 'Сегодня')
async def process_days_command(message: Message):
    today = f'{datetime.datetime.now().day}.{datetime.datetime.now().month}'
    await message.answer(text=f'<b>Расписание на сегодня:</b>\n'
                              f'{schedule.schedule()[today]}')


# Реализация таймдельты !!!!
@user_router.message(F.text == 'Завтра')
async def process_days_command(message: Message):
    t_delta = datetime.timedelta(days=1)
    tommorow_date = datetime.datetime.now() + t_delta
    t_day, month = tommorow_date.day, tommorow_date.month
    today = f'{t_day}.{month}'
    await message.answer(text=f'<b>Расписание на завтра:</b>\n'
                              f'{schedule.schedule()[today]}')


# Реализация таймдельты !!!!
@user_router.message(Command(commands='remind'))
async def process_remind_command(message: Message, scheduler: AsyncIOScheduler, bot: Bot):
    t_delta = datetime.timedelta(days=1)
    tommorow_date = datetime.datetime.now() + t_delta
    t_day, month = tommorow_date.day, tommorow_date.month
    await message.answer(text='Напоминания включены!')
    scheduler.add_job(bot.send_message, 'cron', hour=21,
                      args=(message.chat.id,
                            f'<b>Расписание на завтра:</b>{schedule.schedule()[f'{t_day}.{month}']}'))


@user_router.message(F.text == 'Расписание на неделю')
async def process_schedule_for_week(message: Message):
    await message.answer(text=schedule.get_sch_week())


@user_router.message(F.text == 'Раписание игр')
async def process_games_schedule(message: Message):
    await message.answer(LEXICON_RU['schedule_games'])


@user_router.callback_query(F.data)
async def process_days_inline_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'<b>Расписание на {callback.data}</b>:\n{schedule.schedule()[callback.data]}'
    )
    await callback.answer()

