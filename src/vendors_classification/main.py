import logging

from fastapi import Request, FastAPI

from src.vendors_classification.app import execute

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Home365",
    version="0.0.1",
)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.post("/vendors_classification")
async def vendors_classification(request: Request):
    body = await request.json()
    return execute(body)
    
logger.info("Starting up")
