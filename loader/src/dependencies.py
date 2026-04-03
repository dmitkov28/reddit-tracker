import duckdb
from pydantic import BaseModel, SecretStr


class PGConnection(BaseModel):
    pg_host: SecretStr
    pg_db: SecretStr
    pg_user: SecretStr
    pg_pass: SecretStr


def get_duckdb_connection(pg_conn: PGConnection) -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect(":memory:")
    conn.execute("SET home_directory='/tmp'")
    conn.execute("INSTALL httpfs")
    conn.execute("LOAD httpfs")
    conn.execute("SET s3_region='eu-central-1'")

    conn.execute("INSTALL postgres; LOAD postgres;")
    conn.execute(
        f"""
        ATTACH 'host={pg_conn.pg_host.get_secret_value()} port=5432 dbname={pg_conn.pg_db.get_secret_value()} user={pg_conn.pg_user.get_secret_value()} password={pg_conn.pg_pass.get_secret_value()}' AS pg (TYPE POSTGRES);
        """
    )

    # Performance optimizations
    conn.execute("SET threads=4")  # Increase threads for better S3 parallelism
    conn.execute("SET memory_limit='1GB'")  # Increase if Lambda has more memory

    # HTTP/S3 optimizations - CRITICAL for speed
    conn.execute("SET http_timeout=30000")
    conn.execute("SET http_retries=3")
    conn.execute("SET s3_url_style='path'")
    conn.execute("SET http_keep_alive=true")

    # Aggressive caching and parallelism
    conn.execute("SET enable_http_metadata_cache=true")
    conn.execute("SET enable_object_cache=true")  # Cache S3 objects
    # conn.execute("SET object_cache_size='256MB'")  # Adjust based on file sizes

    # Parquet-specific optimizations
    conn.execute("SET binary_as_string=false")  # Faster binary handling
    # conn.execute("SET enable_p   rofiling=false")  # Disable profiling overhead

    # Memory optimizations
    conn.execute("SET preserve_insertion_order=false")
    conn.execute("SET force_compression='uncompressed'")
    conn.execute("SET temp_directory='/tmp'")
    return conn
