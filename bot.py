import logging

from aiogram.utils import executor
from create_bot import dp

logging.basicConfig(level=logging.INFO)

from handlers import volunteer, admin


volunteer.registerHandlersClient(dp)

# bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
