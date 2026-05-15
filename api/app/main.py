import logging

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from api.app.routers import discovery
from app.routers import auth, webhooks

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-5s [%(name)s] %(message)s',
)

app = FastAPI(title='Squad Hackathon (2026) API')

# CORS for saabi Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://saabi.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(webhooks.router, prefix="/webhooks")
app.include_router(discovery.router, prefix="/discovery")


@app.get('/health', status_code=200)
def get_health():
    return {'message': 'API is reachable'}
