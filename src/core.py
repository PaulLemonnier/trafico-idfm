import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.config import settings


paris_tz = ZoneInfo("Europe/Paris")

HOST = "https://prim.iledefrance-mobilites.fr/"
BASE_URL = "marketplace/stop-monitoring"
API_KEY = settings.IDFM_API_KEY.get_secret_value()

def request_api_info(params: dict[str,str]) -> dict:
    """Request the IDFM API with the selected lines"""
    headers = {"Accept": "application/json", "apikey": API_KEY}
    response = requests.get(HOST + BASE_URL, params=params, headers=headers, timeout=20)
    # print("URL called :", response.url)
    # print("HTTP status code:", response.status_code)

    # INFO: Insert data inside file
    # with open('../data/output_payload.json', 'w', encoding="utf-8") as f:
    #     f.write(json.dumps(response.json(), indent=2, ensure_ascii=False))

    return response.json()

def format_rer_payload(payload:dict) -> pd.DataFrame:
    """Format the API output payload to render a pandas DataFrame with selected column"""
    
    visits: list = (payload.get("Siri")
            .get("ServiceDelivery")
            .get("StopMonitoringDelivery")[0]
            .get("MonitoredStopVisit"))


    # INFO: Structuration of the data
    trains = []
    for visit in visits:
        journey = visit.get("MonitoredVehicleJourney")
        destination = journey.get("DestinationName")[0].get("value")
        platform = journey.get("MonitoredCall").get("DeparturePlatformName").get("value")
        expected_departure = journey.get("MonitoredCall").get("ExpectedDepartureTime")
        aimed_departure = journey.get("MonitoredCall").get("AimedDepartureTime")
        train_name = journey.get("VehicleJourneyName")[0].get("value")
        trains.append({"destination": destination, 
                       "platform": platform, 
                       "expected_departure": expected_departure,
                       "aimed_departure": aimed_departure,
                       "train_name": train_name,
                    })

    df_trains = pd.DataFrame(trains)

    df_trains.dropna(inplace=True)


    # INFO: column creation for datetime format
    df_trains["expected_departure_time"] = df_trains["expected_departure"].apply(
        lambda x: datetime.fromisoformat(str(x)).astimezone(ZoneInfo("Europe/Paris"))
        )    
    df_trains["aimed_departure_time"] = df_trains["aimed_departure"].apply(
        lambda x: datetime.fromisoformat(str(x)).astimezone(ZoneInfo("Europe/Paris"))
        ) 

    print(df_trains["expected_departure"].head())
    print(df_trains["expected_departure_time"].head())

    # INFO: column creation for time readability
    df_trains["formated_expected_departure_time"] = df_trains["expected_departure_time"].dt.strftime("%H:%M")
    df_trains["expected_departure_from_now"] = ((df_trains["expected_departure_time"] - datetime.now(paris_tz)).dt.total_seconds() / 60).round().astype(int)
    # df_trains["actual_time"] = datetime.now(paris_tz)
    
    # INFO : column creation for delay of train
    delay_duration = (df_trains["expected_departure_time"] - df_trains["aimed_departure_time"])
    delay_minutes = delay_duration.dt.total_seconds().div(60).round().astype(int)
    
    df_trains["delay"] = np.where(
        delay_duration > timedelta(minutes=1),
        "Retardé (" + delay_minutes.astype(str) + " min)",
        "À l'heure"
    )
    
    df_trains.drop(columns=["expected_departure", "expected_departure_time", 
                            "aimed_departure" , "aimed_departure_time"], inplace=True)

    return df_trains

def format_metro_payload(payload:dict) -> pd.DataFrame:
    """Format the API output payload Metro to render a pandas DataFrame with selected column"""
    
    visits: list = (payload.get("Siri")
            .get("ServiceDelivery")
            .get("StopMonitoringDelivery")[0]
            .get("MonitoredStopVisit"))


    # INFO: Structuration of the data
    trains = []
    for visit in visits:
        journey = visit.get("MonitoredVehicleJourney")
        destination = journey.get("DestinationName")[0].get("value")
        expected_departure = journey.get("MonitoredCall").get("ExpectedDepartureTime")
        trains.append({"destination": destination, 
                       "expected_departure": expected_departure
                    })


    df_trains = pd.DataFrame(trains)

    df_trains.dropna(inplace=True)


    # INFO: column creation for datetime format
    df_trains["expected_departure_time"] = df_trains["expected_departure"].apply(
        lambda x: datetime.fromisoformat(str(x)).astimezone(ZoneInfo("Europe/Paris"))
        )

    # INFO: column creation for time readability
    df_trains["formated_expected_departure_time"] = df_trains["expected_departure_time"].dt.strftime("%H:%M")
    df_trains["expected_departure_from_now"] = ((df_trains["expected_departure_time"] - datetime.now(paris_tz)).dt.total_seconds() / 60).round().astype(int)
    # df_trains["actual_time"] = datetime.now(paris_tz)

    df_trains.drop(columns=["expected_departure", "expected_departure_time"], inplace=True)

    return df_trains


def compute_rer_route(initial_station: str="Maisons-Laffitte", 
                        line: str="rer_a", 
                        direction: str="right_destination") -> pd.DataFrame:
    """Send the formated result with selected parameter"""
    # INFO: read ref.json
    with open('../conf/ref.json', 'r', encoding="utf-8") as f:
        ref = json.loads(f.read())

    id_monitoring = ref["monitoring"][initial_station]
    id_line = ref["line"][line]

    params = {
        "MonitoringRef": f"STIF:StopArea:SP:{id_monitoring}:",
        "LineRef": f"STIF:Line::{id_line}:"
    }

    data = request_api_info(params)
    df_trains = format_rer_payload(data)
    df_trains["type"] = line
    return df_trains[df_trains["destination"].isin(ref[direction])]

def compute_metro_route(destination: str="École Vétérinaire de Maisons-Alfort TO Balard", 
                        line: str="metro_8") -> pd.DataFrame:
    """Send the formated result with selected parameter"""
    # INFO: read ref.json
    with open('../conf/ref.json', 'r', encoding="utf-8") as f:
        ref = json.loads(f.read())

    id_monitoring = ref["monitoring"][destination]
    id_line = ref["line"][line]

    params = {
        "MonitoringRef": f"STIF:StopArea:SP:{id_monitoring}:",
        "LineRef": f"STIF:Line::{id_line}:"
    }

    data = request_api_info(params)
    df_trains = format_metro_payload(data)
    df_trains["type"] = line
    return df_trains

def format_result(df_result: pd.DataFrame) -> str:
    """Format the DataFrame to obtain a formated string"""
    formated_result = ""
    df_result = df_result.sort_values(by=["expected_departure_from_now"]).reset_index(drop=True).head(5)
    for index in df_result.index:
        delay_string = f" ; {df_result.loc[index,"delay"]}" if ("delay" in df_result.columns) else ""
        formated_result += f"{df_result.loc[index,"type"]}->{df_result.loc[index,"destination"]} [{index + 1}] : {df_result.loc[index,"expected_departure_from_now"]} min ({df_result.loc[index,"formated_expected_departure_time"]}{delay_string})\n"
    return formated_result