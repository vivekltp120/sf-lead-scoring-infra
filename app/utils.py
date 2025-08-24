from fastapi import Request
from loguru import logger
import os, sys, json
import logging
import watchtower

def setup_logging():
    # Structured JSON logging to STDOUT (12-factor)
    logger.remove()
    logger.add(sys.stdout, serialize=True, backtrace=False, diagnose=False, level=os.getenv("LOG_LEVEL", "INFO"))

def get_request_id(request: Request) -> str:
    return request.headers.get("x-request-id", "unknown")


def get_logger(service_name: str="sf-scoring", log_group: str = "/sf-lead-scoring/app"):
    """
    Returns a logger that streams to AWS CloudWatch
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)

    if not any(isinstance(h, watchtower.CloudWatchLogHandler) for h in logger.handlers):
        handler = watchtower.CloudWatchLogHandler(log_group=log_group)
        logger.addHandler(handler)

    return logger

