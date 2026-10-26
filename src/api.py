
import os
import secrets

from fastapi import FastAPI, Header, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from dotenv import load_dotenv

from core import compute_rer_route, compute_metro_route, format_result

load_dotenv()

app = FastAPI(title="API for Trafico")

API_KEY = os.environ["API_KEY"]

class RERRouteRequest(BaseModel):
    user: str = "Paul"
    round_trip: str = "aller"
    initial_station: str = "Maisons-Laffitte"
    line: str = "rer_a"
    direction: str = "right_destination"

class MetroRouteRequest(BaseModel):
    user: str = "Sabrina"
    round_trip: str = "aller"
    destination: str = "Opéra Métro 8 TO Créteil-Pointe du Lac"
    line: str = "metro_8"


def check_api_key(x_api_key: str | None):
    if not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/status")
def status(x_api_key: str | None = Header(default=None)):
    check_api_key(x_api_key)
    return {"status": "online"}


@app.post("/trajet_rer")
def post_for_rer_route(
    payload: RERRouteRequest,
    x_api_key: str | None = Header(default=None)
    ):
    
    check_api_key(x_api_key)

    formated_train_route = format_result(compute_rer_route(initial_station=payload.initial_station, 
                                 line=payload.line, 
                                 direction=payload.direction
                                ))

    return jsonable_encoder({
        "taskName": f"Trajet {payload.round_trip} {payload.user}",
        "infos": formated_train_route
    })

@app.post("/trajet_metro")
def post_for_metro_route(
    payload: MetroRouteRequest,
    x_api_key: str | None = Header(default=None)
    ):
    
    check_api_key(x_api_key)

    formated_train_route = format_result(compute_metro_route(destination=payload.destination, line=payload.line))

    return jsonable_encoder({
        "taskName": f"Trajet {payload.round_trip} {payload.user}",
        "infos": formated_train_route
    })


# Launch API
# python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
