from functools import lru_cache

from fastapi import FastAPI

from app import config

app = FastAPI()


@lru_cache
def get_settings():
    return config.Settings()  # pyright: ignore[reportCallIssue]


@app.get('/health', status_code=200)
def get_health():
    return {'message': 'API is reachable'}
