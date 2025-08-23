from fastapi import Request
from loguru import logger
import os, sys, json

def setup_logging():
    # Structured JSON logging to STDOUT (12-factor)
    logger.remove()
    logger.add(sys.stdout, serialize=True, backtrace=False, diagnose=False, level=os.getenv("LOG_LEVEL", "INFO"))

def get_request_id(request: Request) -> str:
    return request.headers.get("x-request-id", "unknown")
