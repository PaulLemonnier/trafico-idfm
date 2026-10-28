import requests
import json

from src.config import settings


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
    # with open('src/data/output_payload.json', 'w', encoding="utf-8") as f:
    #     f.write(json.dumps(response.json(), indent=2, ensure_ascii=False))

    return response.json()