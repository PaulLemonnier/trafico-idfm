from fastapi import FastAPI

from src.api.routers import trajets

app = FastAPI(
    title="API for Trafico",
    description="API permettant d'afficher les trains pour nos trajets individuel"
    )

app.include_router(trajets.router)

# Launch API
# python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
