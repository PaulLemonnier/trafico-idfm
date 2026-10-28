import json
import pandas as pd
from fastapi import HTTPException

from src.config import settings


def check_api_key(x_api_key: str | None):
    if not x_api_key or x_api_key!=settings.API_KEY.get_secret_value():
        raise HTTPException(status_code=401, detail="Unauthorized")

def load_train_ref():
    with open('src/conf/ref.json', 'r', encoding="utf-8") as f:
        return json.loads(f.read())
