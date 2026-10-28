import pandas as pd
import json
from datetime import datetime
from zoneinfo import ZoneInfo

from src.services.idfm_api import request_api_info


paris_tz = ZoneInfo("Europe/Paris")


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

def compute_metro_route(destination: str="École Vétérinaire de Maisons-Alfort TO Balard", 
                        line: str="metro_8") -> pd.DataFrame:
    """Send the formated result with selected parameter"""
    # INFO: read ref.json
    with open('src/conf/ref.json', 'r', encoding="utf-8") as f:
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
