import httpx
from src.config import settings

class APIClient:
    """Client API réutilisable gérant une seule instance d'AsyncClient."""

    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.API_URL.rstrip("/"),
            timeout=30.0,
            headers={"X-API-Key": settings.API_KEY.get_secret_value()},
        )

    async def close(self):
        """Ferme proprement le client HTTP à l'arrêt du bot."""
        await self.client.aclose()

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        response = await self.client.request(method, path, **kwargs)
        response.raise_for_status()
        return response.json()

    async def get_status(self) -> dict:
        return await self._request("GET", "/status")

    async def post_trajet_rer(self, payload: dict) -> dict:
        return await self._request("POST", "/trajet_rer", json=payload)

    async def post_trajet_metro(self, payload: dict) -> dict:
        return await self._request("POST", "/trajet_metro", json=payload)

api_client = APIClient()
