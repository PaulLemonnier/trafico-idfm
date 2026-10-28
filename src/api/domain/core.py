import json
import pandas as pd
from fastapi import HTTPException

from src.config import settings


def check_api_key(x_api_key: str | None):
    if not x_api_key or x_api_key!=settings.API_KEY.get_secret_value():
        raise HTTPException(status_code=401, detail="Unauthorized")

def load_train_ref():
    with open('src/conf/ref.json', 'r', encoding="utf-8") as f:
        return json.loads(f.read())

def format_result(df_result: pd.DataFrame) -> str:
    """Format the DataFrame to obtain a formated string"""
    formated_result = ""
    shortname_destination = load_train_ref().get("shortname_destination")
    df_result = df_result.sort_values(by=["expected_departure_from_now"]).reset_index(drop=True).head(5)
    for index in df_result.index:
        train_delay = df_result.loc[index,"delay"] # train delay (ex: A l'heure)
        train_type = df_result.loc[index,"type"] # train type (ex: M8, RERA)
        train_destination = shortname_destination.get(df_result.loc[index,"destination"], df_result.loc[index,"destination"]) # train destination (ex: Cergy)
        expected_departure_from_now = df_result.loc[index,"expected_departure_from_now"] # number of minutes before departure (ex: 4)
        formated_expected_departure_time = df_result.loc[index,"formated_expected_departure_time"] # departure time (ex: 9:45)

        emote_train = "🚇" if train_type=="M8" else "🚆"
        delay_string = f" • ⚠️{train_delay}" if ("Retardé" in df_result.loc[index,"delay"]) else ""# f" • ✅{train_delay}"
        time_string = f" • {expected_departure_from_now} min 🕦 {formated_expected_departure_time}"
        formated_result += f"{emote_train}{train_type} → 📍 {train_destination}{time_string}{delay_string})\n\n"
    return formated_result