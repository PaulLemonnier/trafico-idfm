from src.services.telegram_api import api_client
from src.api.domain.rer import format_rer_payload


async def is_rer_delay(initial_station: str="Maisons-Laffitte", line: str="RERA", direction: str="right_destination") -> bool:
    """Check if there is a delay on the specified line"""
    payload = {
        "initial_station": initial_station,
        "line": line,
        "direction": direction,
    }
    data = await api_client.post_trajet_rer(payload)
    df_trains = format_rer_payload(data)
    return any(df_trains["delay"] != "À l'heure")