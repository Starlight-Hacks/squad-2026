import logging

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware

from app.observability import setup_api_observability
from app.routers import auth, wallet, webhooks
from app.router import router as squad_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-5s [%(name)s] %(message)s',
)

app = FastAPI(title='Squad Hackathon (2026) API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exposes /metrics for Prometheus and sends traces to Tempo via OTLP.
Instrumentator().instrument(app).expose(app, include_in_schema=False)
setup_api_observability(app)

app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(webhooks.router)
app.include_router(squad_router)





@app.get('/', status_code=200)
def get_index():
    return {'message': "SAABI's API is online, please look at /docs for public endpoints"}

@app.get('/health', status_code=200)
def get_health():
    return {'message': 'API is reachable'}
