from fastapi import Request
import logging
import watchtower
import boto3



def get_request_id(request: Request) -> str:
    return request.headers.get("x-request-id", "unknown")


def get_logger(service_name: str="sf-scoring", log_group: str = "/sf-lead-scoring/app"):
    """
    Returns a logger that streams to AWS CloudWatch
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)

    if not any(isinstance(h, watchtower.CloudWatchLogHandler) for h in logger.handlers):

        handler = watchtower.CloudWatchLogHandler(log_group_name=log_group,boto3_client=boto3.client("logs", region_name="us-east-1"))
        logger.addHandler(handler)
        
        handler = watchtower.CloudWatchLogHandler(log_group_name=log_group)

    return logger

