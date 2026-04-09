import os

from pydantic import SecretStr

from src.dependencies import PGConnection, get_duckdb_connection
from src.services import get_service
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
        query_type = event.get("query_type")
        if not query_type:
            raise ValueError("Invalid query type")

        service = get_service(query_type=query_type)
        service(
            ddb=ddb,
            src_path=build_path(
                bucket=BUCKET, athena_dir="athena", query_type=query_type
            ),
        )

    return handler
