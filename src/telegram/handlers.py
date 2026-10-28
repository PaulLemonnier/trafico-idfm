from functools import wraps
import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.telegram.filter import is_allowed
from src.services.telegram_api import api_client

router = Router()

def handle_api_calls(error_msg="Échec de l'appel à l'API."):
    """Décorateur pour factoriser la vérification de sécurité et la gestion des erreurs."""
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            if not is_allowed(message):
                return
            try:
                return await func(message, *args, **kwargs)
            except httpx.HTTPError:
                await message.answer(error_msg)
        return wrapper
    return decorator


@router.channel_post(Command("status"))
@handle_api_calls("Erreur lors de l'appel au bot.")
async def status(message: Message):
    data = await api_client.get_status()
    await message.answer(f"BOT : OK\n{data.get('status', 'inconnu')}")


@router.channel_post(Command("tap"))
@handle_api_calls()
async def run_task_tap(message: Message):
    payload = {
        "initial_station": "Maisons-Laffitte",
        "line": "RERA",
        "direction": "right_destination",
    }
    data = await api_client.post_trajet_rer(payload)
    await message.answer(f"Trajet aller Paul :\n\n{data.get('infos')}")


@router.channel_post(Command("trp"))
@handle_api_calls()
async def run_task_trp(message: Message):
    payload = {
        "initial_station": "La Défense",
        "line": "RERA",
        "direction": "left_destination",
    }
    data = await api_client.post_trajet_rer(payload)
    await message.answer(f"Trajet retour Paul :\n\n{data.get('infos')}")


@router.channel_post(Command("tas"))
@handle_api_calls()
async def run_task_tas(message: Message):
    payload_1 = {
        "initial_station": "Maisons-Laffitte",
        "line": "RERA",
        "direction": "right_destination",
    }
    payload_2 = {
        "destination": "Opéra Métro 8 TO Créteil-Pointe du Lac",
        "line": "M8",
    }

    data_1 = await api_client.post_trajet_rer(payload_1)
    data_2 = await api_client.post_trajet_metro(payload_2)
    
    await message.answer(f"Trajet aller Sabrina :\n\n{data_1.get('infos')}\n{data_2.get('infos')}")


@router.channel_post(Command("trs"))
@handle_api_calls()
async def run_task_trs(message: Message):
    payload_1 = {
        "destination": "École Vétérinaire de Maisons-Alfort TO Balard",
        "line": "M8",
    }
    payload_2 = {
        "initial_station": "Opéra RER A",
        "line": "RERA",
        "direction": "left_destination",
    }

    data_1 = await api_client.post_trajet_metro(payload_1)
    data_2 = await api_client.post_trajet_rer(payload_2)
    
    await message.answer(f"Trajet retour Sabrina :\n\n{data_1.get('infos')}\n{data_2.get('infos')}")