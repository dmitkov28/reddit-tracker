from dataclasses import dataclass
import json
import boto3


class S3:
    def __init__(self, bucket: str):
        self._client = boto3.client("s3")
        self._bucket = bucket

    def get(self, key: str) -> dict | None:
        try:
            resp = self._client.get_object(Bucket=self._bucket, Key=key)
            return json.loads(resp["Body"].read())
        except self._client.exceptions.NoSuchKey:
            return None

    def put(self, key: str, data: dict | list) -> None:
        if isinstance(data, list):
            body = "\n".join(json.dumps(item) for item in data)
        else:
            body = json.dumps(data)
        self._client.put_object(
            Bucket=self._bucket,
            Key=key,
            Body=body,
            ContentType="application/json",
        )


@dataclass
class ThreadPartition:
    subreddit: str
    thread_id: str
    year: int
    month: int
    day: int

    def __str__(self):
        return f"threads/year={self.year}/month={self.month}/day={self.day}/thread={self.thread_id}.json"


@dataclass
class CommentPartition:
    subreddit: str
    thread_id: str
    year: int
    month: int
    day: int

    def __str__(self):
        return f"comments/year={self.year}/month={self.month}/day={self.day}/{self.thread_id}.json"
