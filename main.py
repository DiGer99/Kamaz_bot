from aiogram import Bot, Dispatcher
import asyncio
import logging
from config_data.config import load_config, Config
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from handlers.user_handlers import user_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from middlewares.middleware import ScheduleMiddleware


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] #%(levelname)-8s %(filename)s'
                               '%(lineno)s - %(message)s')
    config: Config = load_config()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()

    redis = Redis()
    storage = RedisStorage(redis=redis)

    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    dp.include_router(user_router)
    dp.update.middleware(ScheduleMiddleware(scheduler=scheduler))

    logger.debug('Bot on')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
