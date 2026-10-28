import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.api.domain.core import load_train_ref
from src.services.idfm_api import request_api_info

paris_tz = ZoneInfo("Europe/Paris")

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


def compute_rer_route(initial_station: str="Maisons-Laffitte", 
                        line: str="rer_a", 
                        direction: str="right_destination") -> pd.DataFrame:
    """Send the formated result with selected parameter"""
    # INFO: read ref.json
    ref = load_train_ref()

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

def format_rer_result(df_result: pd.DataFrame) -> str:
    """Format the DataFrame to obtain a formated string"""
    formated_result = ""
    shortname_destination = load_train_ref().get("shortname_destination")
    df_result = df_result.sort_values(by=["expected_departure_from_now"]).reset_index(drop=True).head(5)
    for index in df_result.index:
        train_delay = df_result.loc[index,"delay"] # train delay (ex: A l'heure)
        train_type = df_result.loc[index,"type"] # train type (ex: RERA)
        train_destination = shortname_destination.get(df_result.loc[index,"destination"], df_result.loc[index,"destination"]) # train destination (ex: Cergy)
        expected_departure_from_now = df_result.loc[index,"expected_departure_from_now"] # number of minutes before departure (ex: 4)
        formated_expected_departure_time = df_result.loc[index,"formated_expected_departure_time"] # departure time (ex: 9:45)

        delay_string = f" • ⚠️{train_delay}" if ("Retardé" in df_result.loc[index,"delay"]) else ""# f" • ✅{train_delay}"
        time_string = f" • {expected_departure_from_now} min 🕦 {formated_expected_departure_time}"
        formated_result += f"🚆{train_type} → 📍 {train_destination}{time_string}{delay_string}\n\n"
    return formated_result