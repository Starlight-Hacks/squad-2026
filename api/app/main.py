import logging

from fastapi import FastAPI

from app.routers import auth, webhooks

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5s [%(name)s] %(message)s',
)

app = FastAPI(title='Squad Hackathon (2026) API')

app.include_router(auth.router)
app.include_router(webhooks.router)


@app.get('/health', status_code=200)
def get_health():
    return {'message': 'API is reachable'}
