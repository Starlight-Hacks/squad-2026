from fastapi import FastAPI

from app.routers import auth

app = FastAPI(title='Squad Hackathon (2026) API')

app.include_router(auth.router)


@app.get('/health', status_code=200)
def get_health():
    return {'message': 'API is reachable'}
