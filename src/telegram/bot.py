
import asyncio
import logging
import httpx
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from src.config import settings

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN.get_secret_value()
API_URL = settings.API_URL.rstrip("/")
API_KEY = settings.API_KEY.get_secret_value()
ALLOWED_CHAT_ID = int(settings.ALLOWED_CHAT_ID)

dp = Dispatcher()


def is_allowed(message: Message) -> bool:
    return (
        message.chat.id == ALLOWED_CHAT_ID
        and message.sender_chat is not None
        and message.sender_chat.id == ALLOWED_CHAT_ID
    )


async def call_api(method: str, path: str, **kwargs) -> dict:
    async with httpx.AsyncClient(
        base_url=API_URL,
        timeout=30.0,
        headers={"X-API-Key": API_KEY},
    ) as client:
        response = await client.request(method, path, **kwargs)
        response.raise_for_status()
        return response.json()


@dp.channel_post(Command("status"))
async def status(message: Message):
    if not is_allowed(message):
        return
    try:
        data = await call_api("GET", "/status")
        await message.answer(f"BOT : OK\n{data.get('status', 'inconnu')}")
    except httpx.HTTPError:
        await message.answer("Erreur lors de l'appel au bot.")


@dp.channel_post(Command("tap"))
async def run_task_tap(message: Message):
    if not is_allowed(message):
        return
    try:
        json_payload = {
            "user" : "Paul",
            "round_trip" : "aller",
            "initial_station" : "Maisons-Laffitte",
            "line" : "rer_a",
            "direction" : "right_destination"
        }

        data = await call_api("POST", "/trajet_rer", json=json_payload)
        await message.answer(f"{data.get('taskName')} :\n\n{data.get('infos')}")
    except httpx.HTTPError:
        await message.answer("Échec de l'appel à l'API.")


@dp.channel_post(Command("trp"))
async def run_task_trp(message: Message):
    if not is_allowed(message):
        return
    try:
        json_payload = {
            "user" : "Paul",
            "round_trip" : "retour",
            "initial_station" : "La Défense",
            "line" : "rer_a",
            "direction" : "left_destination"
        }

        data = await call_api("POST", "/trajet_rer", json=json_payload)
        await message.answer(f"{data.get('taskName')} :\n\n{data.get('infos')}")
    except httpx.HTTPError:
        await message.answer("Échec de l'appel à l'API.")


@dp.channel_post(Command("tas"))
async def run_task_tas(message: Message):
    if not is_allowed(message):
        return
    try:
        json_payload_1 = {
            "user" : "Sabrina",
            "round_trip" : "aller",
            "initial_station" : "Maisons-Laffitte",
            "line" : "rer_a",
            "direction" : "right_destination"
        }

        data_1 = await call_api("POST", "/trajet_rer", json=json_payload_1)

        json_payload_2 = {
                    "user" : "Sabrina",
                    "round_trip" : "aller",
                    "destination" : "Opéra Métro 8 TO Créteil-Pointe du Lac",
                    "line" : "metro_8"
                }
        
        data_2 = await call_api("POST", "/trajet_metro", json=json_payload_2)
        await message.answer(f"{data_1.get('taskName')} :\n\n{data_1.get('infos')}\n{data_2.get('infos')}")
    except httpx.HTTPError:
        await message.answer("Échec de l'appel à l'API.")

@dp.channel_post(Command("trs"))
async def run_task_trs(message: Message):
    if not is_allowed(message):
        return
    try:
        json_payload_1 = {
                    "user" : "Sabrina",
                    "round_trip" : "retour",
                    "destination" : "École Vétérinaire de Maisons-Alfort TO Balard",
                    "line" : "metro_8"
                }
        
        data_1 = await call_api("POST", "/trajet_metro", json=json_payload_1)

        json_payload_2 = {
                    "user" : "Sabrina",
                    "round_trip" : "retour",
                    "initial_station" : "Opéra RER A",
                    "line" : "rer_a",
                    "direction" : "left_destination"
                }
        
        data_2 = await call_api("POST", "/trajet_rer", json=json_payload_2)
        await message.answer(f"{data_1.get('taskName')} :\n\n{data_1.get('infos')}\n{data_2.get('infos')}")
    except httpx.HTTPError:
        await message.answer("Échec de l'appel à l'API.")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    me = await bot.get_me()
    logging.info("Bot connecté : @%s", me.username)

    await bot.delete_webhook(drop_pending_updates=False)
    logging.info("En attente des commandes Telegram...")
    await dp.start_polling(bot, allowed_updates=["channel_post"])

if __name__ == "__main__":
    asyncio.run(main())

