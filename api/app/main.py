from fastapi import FastAPI

app = FastAPI(title='Squad Hackathon (2026) API')


@app.get('/health', status_code=200)
def get_health():
    return {'message': 'API is reachable'}
