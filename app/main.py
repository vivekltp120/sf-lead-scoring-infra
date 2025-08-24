import time
from fastapi import FastAPI, HTTPException
from fastapi import Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from loguru import logger
from .model import ScoreRequest, ScoreResponse, ModelService
from .utils import get_request_id
app = FastAPI(title="Lead Scoring API", version="1.0.0")
from .utils import get_logger
logger = get_logger("app_main")



REQUEST_COUNT = Counter("requests_total", "Total requests", ["endpoint", "status"])
LATENCY = Histogram("request_latency_seconds", "Latency", ["endpoint"])

model_service = ModelService()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    try:
        resp = await call_next(request)
        status = resp.status_code
    except Exception as e:
        status = 500
        logger.exception("Unhandled exception")
        raise
    finally:
        dt = time.perf_counter() - start
        endpoint = request.url.path
        REQUEST_COUNT.labels(endpoint=endpoint, status=str(status)).inc()
        LATENCY.labels(endpoint=endpoint).observe(dt)
    return resp

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    return {"ready": model_service.ready}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/score", response_model=ScoreResponse)
async def score(req: ScoreRequest, request: Request):
    rid = get_request_id(request)
    t0 = time.perf_counter()
    try:
        result = await model_service.score(req)
    except ValueError as e:
        logger.warning(f"validation_error request_id={rid} msg={e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"scoring_failed request_id={rid}")
        raise HTTPException(status_code=500, detail="scoring_failed")
    latency_ms = int((time.perf_counter() - t0) * 1000)
    logger.info(f"scored request_id={rid} latency_ms={latency_ms} score={result.score}")
    return result
