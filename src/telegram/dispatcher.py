from aiogram import Dispatcher

from src.telegram.handlers import router

dp = Dispatcher()

dp.include_router(router)