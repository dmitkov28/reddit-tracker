import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


def lambda_handler(event: dict, context: dict):
    bucket = os.environ["BUCKET"]
    fetcher_function_name = os.environ["FETCHER"]

    key = "subreddits.json"

    logger.info("Reading config", extra={"bucket": bucket, "key": key})

    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    config = json.loads(response["Body"].read())
    logger.info("Config loaded", extra={"config": config})

    lambda_client = boto3.client("lambda", region_name="eu-central-1")
    for subreddit in config:

        payload = {"subreddit": subreddit}
        response = lambda_client.invoke(
            FunctionName=fetcher_function_name,
            InvocationType="Event",
            Payload=json.dumps(payload),
        )
        logger.info("Invocation", extra=response)

    return
