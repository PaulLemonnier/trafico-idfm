import pandas as pd
from fastapi import HTTPException

from src.config import settings


def check_api_key(x_api_key: str | None):
    if not x_api_key or x_api_key!=settings.API_KEY.get_secret_value():
        raise HTTPException(status_code=401, detail="Unauthorized")

def format_result(df_result: pd.DataFrame) -> str:
    """Format the DataFrame to obtain a formated string"""
    formated_result = ""
    df_result = df_result.sort_values(by=["expected_departure_from_now"]).reset_index(drop=True).head(5)
    for index in df_result.index:
        delay_string = f" ; {df_result.loc[index,"delay"]}" if ("delay" in df_result.columns) else ""
        formated_result += f"{df_result.loc[index,"type"]}->{df_result.loc[index,"destination"]} [{index + 1}] : {df_result.loc[index,"expected_departure_from_now"]} min ({df_result.loc[index,"formated_expected_departure_time"]}{delay_string})\n"
    return formated_result