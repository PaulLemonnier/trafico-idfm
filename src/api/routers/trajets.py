from fastapi import APIRouter, Header
from fastapi.encoders import jsonable_encoder

from src.api.domain.core import format_result, check_api_key
from src.api.domain.rer import compute_rer_route
from src.api.domain.metro import compute_metro_route
from src.api.models import RERRouteRequest, MetroRouteRequest


router = APIRouter(tags=["Trajets"])

@router.get("/status")
def status(x_api_key: str | None = Header(default=None)):
    check_api_key(x_api_key)
    return {"status": "online"}


@router.post("/trajet_rer")
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

@router.post("/trajet_metro")
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
