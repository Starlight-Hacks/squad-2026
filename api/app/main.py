from fastapi import FastAPI

from app.routers.auth import auth_router

app = FastAPI(title='Squad Hackathon (2026) API')

app.include_router(auth_router)


@app.get('/health', status_code=200)
def get_health():
    return {'message': 'API is reachable'}
