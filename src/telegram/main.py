import asyncio
import logging
from aiogram import Bot

from src.telegram.dispatcher import dp
from src.config import settings


async def launch_telegram_bot():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN.get_secret_value())

    me = await bot.get_me()
    logging.info("Bot connecté : @%s", me.username)

    await bot.delete_webhook(drop_pending_updates=False)
    logging.info("En attente des commandes Telegram...")
    await dp.start_polling(bot, allowed_updates=["channel_post"])

asyncio.run(launch_telegram_bot())

# Launch Telegram bot
# python -m src.telegram.main