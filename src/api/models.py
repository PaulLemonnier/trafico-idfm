from pydantic import BaseModel

class RERRouteRequest(BaseModel):
    initial_station: str = "Maisons-Laffitte"
    line: str = "RERA"
    direction: str = "right_destination"

class MetroRouteRequest(BaseModel):
    destination: str = "Opéra Métro 8 TO Créteil-Pointe du Lac"
    line: str = "M8"