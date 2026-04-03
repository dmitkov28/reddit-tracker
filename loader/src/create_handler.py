import os

from pydantic import SecretStr

from src.dependencies import PGConnection, get_duckdb_connection
from src import services
from src.utils import build_path


def create_handler():
    BUCKET = os.environ["BUCKET"]
    PG_HOST = os.environ["PG_HOST"]
    PG_DB = os.environ["PG_DB"]
    PG_USER = os.environ["PG_USER"]
    PG_PASS = os.environ["PG_PASS"]

    pg_conn = PGConnection(
        pg_host=SecretStr(PG_HOST),
        pg_db=SecretStr(PG_DB),
        pg_user=SecretStr(PG_USER),
        pg_pass=SecretStr(PG_PASS),
    )
    ddb = get_duckdb_connection(pg_conn=pg_conn)

    def handler(event: dict, context: dict):
        s3 = event["Records"][0]["s3"]
        src_obj_key = s3["object"]["key"]

        path = build_path(bucket=BUCKET, athena_dir="athena")

        if path + "/subreddits" in src_obj_key:
            services.upsert_subreddits(ddb=ddb, src_path=path + "/subreddits/*")
            services.upsert_subreddit_subscribers(
                ddb=ddb, src_path=path + "/subreddits/*"
            )
    return handler