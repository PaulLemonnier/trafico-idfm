from pydantic import BaseModel

class RERRouteRequest(BaseModel):
    user: str = "Paul"
    round_trip: str = "aller"
    initial_station: str = "Maisons-Laffitte"
    line: str = "RERA"
    direction: str = "right_destination"

class MetroRouteRequest(BaseModel):
    user: str = "Sabrina"
    round_trip: str = "aller"
    destination: str = "Opéra Métro 8 TO Créteil-Pointe du Lac"
    line: str = "M8"